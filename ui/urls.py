from django.urls import path, include

from ui import views, pages

namespace = "ui"

urlpatterns = [
    path("", views.UiLoginView.as_view(), name="login"),
    path("dashboard/", include(pages.ui_patterns.urls)),
    path("dashboard/logout/", views.UiLogoutView.as_view(), name="logout"),
]
