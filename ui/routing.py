from django.urls import path

from ui import consumers

websocket_urlpatterns = [
    path("", consumers.DashboardSocket.as_asgi(), name="dashboard-ui-socket"),
]
