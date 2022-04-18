from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView as _LoginView
from django.shortcuts import render
from django.views import View

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


class DashboardHomeView(View, DashboardViewMixin):
    def get(self, request):
        return self.render(request, "ui/dashboard/pages/home.html")


class DashboardUsersView(View, DashboardViewMixin):
    def get(self, request):
        users = User.objects.all()
        return self.render(
            request, "ui/dashboard/pages/list_users.html", {"users": users}
        )
