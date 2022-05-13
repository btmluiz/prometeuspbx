from django.urls import reverse

from pbx import models, forms
from ui.views import (
    UiTemplateView,
    UiListView,
    UiCreateView,
    UiMultiFormView,
    UiSingleObjectMixin,
)


# Create your views here.


class ExtensionsView(UiListView):
    model = models.Extension
    paginate_by = 10
    template_name = "pbx/pages/extensions/index.html"


class ExtensionCreateView(UiCreateView):
    model = models.Extension
    fields = ["number", "username", "password", "user", "context"]
    template_name = "pbx/pages/extensions/forms/create.html"

    def get_success_url(self):
        return reverse("ui:pbx-extension-edit", kwargs={"pk": self.object.pk})


class ExtensionEditView(UiSingleObjectMixin, UiMultiFormView):
    model = models.Extension
    forms_class = {
        "sip": forms.SipAorForm,
        "auth": forms.SipAuthForm,
        "endpoint": forms.SipEndpointForm,
    }
    default_form = forms.ExtensionEditForm
    template_name = "pbx/pages/extensions/forms/edit.html"

    def get_form_kwargs(self, form_type, kwargs=None):
        if not kwargs:
            kwargs = {}

        if form_type == "form":
            return super().get_form_kwargs(form_type, kwargs)
        else:
            instance = self.get_form_class(form_type)._meta.model(extension=self.object)
            return {"instance": instance, **kwargs}


class MonitorView(UiTemplateView):
    template_name = "pbx/pages/monitor/index.html"
