from django import forms

from pbx import models, models_sip


class ExtensionEditForm(forms.ModelForm):
    class Meta:
        model = models.Extension
        fields = ("number", "username", "password", "user", "context")


class SipAorForm(forms.ModelForm):
    class Meta:
        model = models_sip.SipAor
        exclude = ("extension", "sip_id", "id")


class SipAuthForm(forms.ModelForm):
    class Meta:
        model = models_sip.SipAuth
        exclude = ("extension", "sip_id", "id", "username", "password")


class SipEndpointForm(forms.ModelForm):
    class Meta:
        model = models_sip.SipEndpoint
        exclude = ("extension", "sip_id", "id", "auth", "aors", "context", "contact")
