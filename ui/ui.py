from django.utils.translation import gettext_lazy as _

from ui import views
from ui.pages.base import UIPage


class UiHomePage(UIPage):
    path = ""
    path_name = "dashboard-home"
    view = views.UiHomeView
    menu_label = _("Home")
    menu_icon = "home"
    menu_section = "dashboard"


class UiUsersPage(UIPage):
    path = "users"
    path_name = "dashboard-users"
    view = views.UiUsersView
    menu_label = _("Users")
    menu_icon = "user"
    menu_section = "dashboard"
    menu_has_sub_path = True
    permissions = ["can_list_users"]


class UiCreateUserPage(UIPage):
    path = "users/create/"
    path_name = "dashboard-user-create"
    view = views.UiCreateUserView
    permissions = ["can_create_users"]


class UiEditUserPage(UIPage):
    path = "users/<uuid:pk>/edit/"
    path_name = "dashboard-user-edit"
    view = views.UiEditUserView
    permissions = ["can_edit_users"]


class UiDeleteUserPage(UIPage):
    path = "users/<uuid:pk>/delete/"
    path_name = "dashboard-user-delete"
    view = views.UiDeleteUserView
    permissions = ["can_delete_users"]


class UiSettingsPage(UIPage):
    path = "settings/"
    path_name = "dashboard-settings"
    view = views.UiSettingsView
    menu_label = _("Settings")
    menu_icon = "settings"
    menu_has_sub_path = True


ui_patterns = [
    UiHomePage,
    UiUsersPage,
    UiCreateUserPage,
    UiEditUserPage,
    UiDeleteUserPage,
    UiSettingsPage,
]
