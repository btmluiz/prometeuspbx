from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.contrib.auth.views import LoginView as _LoginView
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView

from core.models import User
from ui import forms

# Create your views here.
from ui.menu import menu


class LoginView(_LoginView):
    form_class = forms.LoginForm
    template_name = "ui/login/signin.html"
    extra_context = None
    redirect_authenticated_user = False
    redirect_field_name = REDIRECT_FIELD_NAME
    authentication_form = None
    next_page = None


class DashboardViewMixin(object):
    @staticmethod
    def render(
        request,
        template_name,
        context=None,
        content_type=None,
        status=None,
        using=None,
    ):
        if not context:
            context = {}
        context["menu"] = menu.items
        return render(request, template_name, context, content_type, status, using)


class DashboardTemplateViewMixin(object):
    def render_to_response(self, context, **response_kwargs):
        if not context:
            context = {}
        context["menu"] = menu.items
        return super().render_to_response(context, **response_kwargs)


class DashboardMultiFormView(DashboardTemplateViewMixin, TemplateView):
    forms_class = {}
    default_form = None
    success_url = None

    def post(self, request, *args, **kwargs):
        form_type = request.POST.get("form_type", None)
        form_class = self.forms_class.get(form_type, self.default_form)
        form_kwargs = {"instance": self.object, "data": request.POST}

        form = form_class(**form_kwargs)
        if not form.is_valid():
            return self.render_to_response(
                self.get_context_data(
                    form_kwargs={[form_type if form_type else "form"]: form}
                )
            )

        self.perform_save(form)
        return HttpResponseRedirect(self.get_success_url())

    def perform_save(self, form):
        return form.save()

    def get_context_data(self, **kwargs):
        form_kwargs = kwargs.pop("form_kwargs", {})
        return {**self.get_forms(**form_kwargs), **super().get_context_data(**kwargs)}

    def get_forms(self, **kwargs):
        new_kwargs = {}
        for key in self.forms_class.keys():
            form = kwargs.get(key, None)

            print(form)

            new_kwargs["form_%s" % key] = (
                self.forms_class[key](**self.get_form_kwargs(key)) if not form else form
            )

        if self.default_form:
            if not kwargs.get("form", None):
                new_kwargs["form"] = self.default_form(**self.get_default_form_kwargs())

        return new_kwargs

    def get_form_kwargs(self, form_type):
        return {"instance": self.object}

    def get_default_form_kwargs(self):
        return {"instance": self.object}

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)


class DashboardHomeView(View, DashboardViewMixin):
    def get(self, request):
        return self.render(request, "ui/dashboard/home/home.html")


class DashboardUsersView(DashboardTemplateViewMixin, ListView):
    model = User
    paginate_by = 10
    template_name = "ui/dashboard/users/list_users.html"


class DashboardEditUserView(SingleObjectMixin, View, DashboardViewMixin):
    model = User
    template_name = "ui/forms/user/update.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return self.render(
            request,
            self.template_name,
            {"object": self.object, **self.get_forms()},
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_type = request.POST.get("form_type", None)

        form_kwargs = {"instance": self.object, "data": request.POST}

        if form_type == "set-password":
            form = forms.SetPasswordForm(**form_kwargs)

            if not form.is_valid():
                return self.render(
                    request,
                    self.template_name,
                    self.get_default_context(form_kwargs={"form_set_password": form}),
                )
        else:
            form = forms.UserEditForm(**form_kwargs)
            if not form.is_valid():
                print(form)
                return self.render(
                    request,
                    self.template_name,
                    self.get_default_context(form_kwargs={"form_update": form}),
                )

        self.peform_save(form)
        return HttpResponseRedirect(self.get_success_url())

    def peform_save(self, form):
        return form.save()

    def get_default_context(self, form_kwargs=None, **kwargs):
        return {"object": self.object, **self.get_forms(**form_kwargs), **kwargs}

    def get_forms(self, form_update=None, form_set_password=None):
        if not form_update:
            form_update = forms.UserEditForm(instance=self.object)

        if not form_set_password:
            form_set_password = forms.SetPasswordForm(instance=self.object)

        return {
            "form_update": form_update,
            "form_set_password": form_set_password,
        }

    def get_success_url(self):
        return reverse("ui:dashboard-user-edit", kwargs={"pk": self.get_object().pk})


class DashboardCreateUserView(DashboardTemplateViewMixin, CreateView):
    model = User
    form_class = forms.UserCreateForm
    template_name = "ui/forms/user/create.html"

    def get_success_url(self):
        return reverse("ui:dashboard-user-edit", kwargs={"pk": self.object.pk})


class DashboardDeleteUserView(DashboardTemplateViewMixin, DeleteView):
    model = User
    template_name = "ui/forms/user/delete.html"
    context_object_name = "user_object"
    success_url = reverse_lazy("ui:dashboard-users")


class DashboardSettingsView(DashboardMultiFormView):
    template_name = "ui/forms/settings/edit.html"
    forms_class = {
        "change_password": forms.ChangePasswordForm,
    }
    default_form = forms.UserEditForm
    success_url = reverse_lazy("ui:dashboard-settings")

    def get(self, request, *args, **kwargs):
        self.object = request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = request.user
        return super().post(request, *args, **kwargs)


class DashboardLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("ui:login"))
