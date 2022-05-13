from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, logout, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.models import User
from ui import forms
from ui.menu import menu


# Create your views here.


def handler404(request, *args, **kwargs):
    response = render(request, "ui/404.html", status=404)
    return response


def handler500(request, *args, **kwargs):
    response = render(request, "ui/500.html", status=500)
    return response


class UiLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "ui/login/signin.html"
    extra_context = None
    redirect_authenticated_user = False
    redirect_field_name = REDIRECT_FIELD_NAME
    authentication_form = None
    next_page = None


class UiViewMixin(object):
    permissions = []
    require_login = True

    def __init__(self, permissions=None, *args, **kwargs):
        if permissions is None:
            permissions = []
        self.permissions = permissions
        super().__init__(*args, **kwargs)

    def get_dashboard_context(self, context):
        if not context:
            context = {}
        context["menu"] = menu.items(self.request.user)
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.require_login and request.user.is_authenticated:
            if self.check_user_permissions(request.user, self.permissions):
                return super().dispatch(request, *args, **kwargs)
            else:
                return self.permission_denied(request)
        else:
            return HttpResponseRedirect(str(settings.LOGIN_URL))

    @staticmethod
    def permission_denied(request):
        return render(request, "ui/403.html", status=403)

    @staticmethod
    def check_user_permissions(user, permissions):
        return user.has_perms(permissions)


class UiFormFieldPermissionsMixin:
    fields_permission = {}

    def get_fields(self, data):
        fields_data = {}
        for field_name, value in data.items():
            if (
                field_name in self.fields_permission
                and self.request.user.has_perms(self.fields_permission[field_name])
            ) or field_name not in self.fields_permission:
                fields_data[field_name] = value

        return fields_data


class UiFormFieldMixin(UiFormFieldPermissionsMixin):
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.get_fields(self.request.POST),
                    "files": self.get_fields(self.request.FILES),
                }
            )
        return kwargs


class UiView(UiViewMixin, View):
    def render(
        self,
        request,
        template_name,
        context=None,
        content_type=None,
        status=None,
        using=None,
    ):
        context = self.get_dashboard_context(context)
        return render(request, template_name, context, content_type, status, using)


class UiTemplateViewMixin(UiViewMixin):
    permissions = []
    require_login = True

    def render_to_response(self, context, **response_kwargs):
        context = self.get_dashboard_context(context)
        return super().render_to_response(context, **response_kwargs)


class UiTemplateView(UiTemplateViewMixin, TemplateView):
    pass


class UiListView(UiTemplateViewMixin, ListView):
    pass


class UiCreateView(UiTemplateViewMixin, CreateView):
    pass


class UiUpdateView(UiTemplateViewMixin, UpdateView):
    pass


class UiDeleteView(UiTemplateViewMixin, DeleteView):
    pass


class UiMultiFormView(UiTemplateView):
    forms_class = {}
    default_form = None
    success_url = None
    success_messages = {}
    form_permissions = {}
    fields_permission = {}

    def post(self, request, *args, **kwargs):
        form_type = request.POST.get("form_type", "form")

        if form_type in self.form_permissions and not self.check_user_permissions(
            request.user, permissions=self.form_permissions[form_type]
        ):
            return self.permission_denied(request)

        form_class = self.get_form_class(form_type)

        form_kwargs = self.get_form_kwargs(
            form_type,
            {
                "instance": self.object,
                "data": request.POST,
                "files": request.FILES,
            },
        )

        form = form_class(**form_kwargs)

        if not form.is_valid():
            return self.render_to_response(
                self.get_context_data(
                    form_kwargs={
                        form_type: form,
                    },
                    form_type=form_type,
                )
            )

        self.perform_success(request, form_type)
        self.perform_save(form_type, form)
        return HttpResponseRedirect(self.get_success_url())

    def perform_save(self, form_type, form):
        return form.save()

    def perform_success(self, request, form_type):
        message = self.get_success_message(form_type)
        if message:
            messages.success(request, message)

    def get_context_data(self, **kwargs):
        form_kwargs = kwargs.pop("form_kwargs", {})
        resp = {**self.get_forms(**form_kwargs), **super().get_context_data(**kwargs)}
        print(resp)
        return resp

    def get_forms(self, **kwargs):
        new_kwargs = {}
        for key in self.forms_class.keys():
            form = kwargs.get(key, None)

            new_kwargs["form_%s" % key] = (
                self.get_form_class(key)(**self.get_form_kwargs(key))
                if not form
                else form
            )

        if self.default_form:
            if not kwargs.get("form", None):
                new_kwargs["form"] = self.get_form_class("form")(
                    **self.get_default_form_kwargs()
                )

        return new_kwargs

    def get_form_class(self, form_type):
        excluded_fields = self.get_excluded_fields(form_type)

        form = self.forms_class.get(form_type, self.default_form)

        if excluded_fields and self.model:
            return modelform_factory(self.model, form=form, exclude=excluded_fields)

        return form

    def get_excluded_fields(self, form_type):
        """
        :param form_type: str
        :return: tuple(str)
        """
        exclude_fields = []

        if form_type not in self.fields_permission:
            return ()

        for field, perms in self.fields_permission[form_type].items():
            if not self.request.user.has_perms(perms):
                exclude_fields.append(field)
        return tuple(exclude_fields)

    def get_success_message(self, form_type):
        return (
            self.success_messages[form_type]
            if form_type in self.success_messages
            else None
        )

    def get_form_kwargs(self, form_type, kwargs=None):
        if not kwargs:
            kwargs = {}
        return {"instance": self.object, **kwargs}

    def get_default_form_kwargs(self):
        return {"instance": self.object}

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)


class UiSingleObjectMixin(SingleObjectMixin):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class UiHomeView(UiTemplateView):
    template_name = "ui/dashboard/home/home.html"


class UiUsersView(UiListView):
    model = User
    paginate_by = 10
    template_name = "ui/dashboard/users/list_users.html"


class UiEditUserView(UiSingleObjectMixin, UiMultiFormView):
    model = User
    template_name = "ui/forms/user/update.html"
    forms_class = {"set_password": forms.SetPasswordForm}
    default_form = forms.UserEditForm
    success_messages = {
        "form": _("User edited"),
    }
    form_permissions = {
        "set_password": ["can_change_users_password"],
    }
    fields_permission = {
        "form": {
            "user_permissions": ["can_set_permission"],
            "is_superuser": ["is_superuser"],
            "is_active": ["can_inactivate_users"],
        }
    }

    def get_success_url(self):
        return reverse("ui:dashboard-user-edit", kwargs={"pk": self.get_object().pk})


class UiCreateUserView(UiCreateView):
    model = User
    form_class = forms.UserCreateForm
    template_name = "ui/forms/user/create.html"

    def get_success_url(self):
        return reverse("ui:dashboard-user-edit", kwargs={"pk": self.object.pk})


class UiDeleteUserView(UiDeleteView):
    model = User
    template_name = "ui/forms/user/delete.html"
    context_object_name = "user_object"
    success_url = reverse_lazy("ui:dashboard-users")


class UiSettingsView(UiMultiFormView):
    template_name = "ui/forms/settings/edit.html"
    forms_class = {
        "change_password": forms.ChangePasswordForm,
    }
    default_form = forms.AccountInfoForm
    success_url = reverse_lazy("ui:dashboard-settings")
    success_messages = {
        "form": _("User edited"),
        "change_password": _("Password changed"),
    }

    def get(self, request, *args, **kwargs):
        self.object = request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = request.user
        return super().post(request, *args, **kwargs)

    def perform_save(self, form_type, form):
        instance = super().perform_save(form_type, form)
        if form_type == "change_password":
            update_session_auth_hash(self.request, instance)
        return instance


class UiLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("ui:login"))
