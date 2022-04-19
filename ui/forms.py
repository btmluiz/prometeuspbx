from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _

from core.models import User


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control-lg"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control-lg"}),
    )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
