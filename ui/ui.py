from django.utils.translation import gettext_lazy as _

from ui import views
from ui.pages.base import UIPage


class DashboardHomePage(UIPage):
    path = ""
    path_name = "dashboard-home"
    view = views.DashboardHomeView.as_view()
    menu_label = _("Home")
    menu_icon = "home"
    menu_section = "dashboard"


class DashboardUsersPage(UIPage):
    path = "users"
    path_name = "dashboard-users"
    view = views.DashboardUsersView.as_view()
    menu_label = _("Users")
    menu_icon = "user"
    menu_section = "dashboard"
    menu_has_sub_path = True


class DashboardCreateUserPage(UIPage):
    path = "users/create/"
    path_name = "dashboard-user-create"
    view = views.DashboardCreateUser.as_view()


class DashboardEditUserPage(UIPage):
    path = "users/<uuid:pk>/"
    path_name = "dashboard-user-edit"
    view = views.DashboardEditUserView.as_view()


ui_patterns = [
    DashboardHomePage,
    DashboardUsersPage,
    DashboardCreateUserPage,
    DashboardEditUserPage,
]
