from ui import views
from ui.pages import UIPage
from django.utils.translation import gettext_lazy as _


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


ui_patterns = [DashboardHomePage, DashboardUsersPage]
