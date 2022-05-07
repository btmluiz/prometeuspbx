from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView as _LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView

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


class DashboardFormViewMixin(object):
    def render_to_response(self, context, **response_kwargs):
        if not context:
            context = {}
        context["menu"] = menu.items
        return super().render_to_response(context, **response_kwargs)


class DashboardHomeView(View, DashboardViewMixin):
    def get(self, request):
        return self.render(request, "ui/dashboard/pages/home.html")


class DashboardUsersView(View, DashboardViewMixin):
    def get(self, request):
        users = User.objects.all()
        return self.render(
            request, "ui/dashboard/pages/list_users.html", {"users": users}
        )


class DashboardEditUserView(SingleObjectMixin, View, DashboardViewMixin):
    model = User
    fields = ["first_name", "last_name", "email"]
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

            print(form.errors)
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


class DashboardCreateUser(DashboardFormViewMixin, CreateView):
    model = User
    form_class = forms.UserCreateForm
    template_name = "ui/forms/user/create.html"
