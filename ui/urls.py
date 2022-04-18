from django.urls import path, include

from ui import views, pages

namespace = "ui"

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("dashboard/", include(pages.ui_patterns.urls)),
]
