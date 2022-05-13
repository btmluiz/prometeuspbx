from django.utils.translation import gettext_lazy as _

from pbx import views
from ui.pages.base import UIPage

DEFAULT_SECTION = "pbx"
BASE_PATH = "pbx"


class PBXExtensions(UIPage):
    path = "extensions/"
    path_name = "pbx-extensions"
    view = views.ExtensionsView
    menu_label = _("Extensions")
    menu_icon = "phone"
    menu_has_sub_path = True


class PBXExtensionCreate(UIPage):
    path = "extensions/create/"
    path_name = "pbx-extension-create"
    view = views.ExtensionCreateView


class PBXExtensionEdit(UIPage):
    path = "extensions/<uuid:pk>/edit/"
    path_name = "pbx-extension-edit"
    view = views.ExtensionEditView


class PBXMonitor(UIPage):
    path = "monitor/"
    path_name = "pbx-monitor"
    view = views.MonitorView
    menu_label = _("Monitor")
    menu_icon = "monitor"


ui_patterns = [
    PBXExtensions,
    PBXExtensionCreate,
    PBXExtensionEdit,
    PBXMonitor,
]
