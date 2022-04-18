from django.shortcuts import render

# Create your views here.
from django.views import View

from ui import forms


class LoginView(View):
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, "../ui/templates/ui/login/signin.html", {"form": form})
