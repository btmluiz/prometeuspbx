from channels.routing import URLRouter
from django.conf import settings
from django.urls import path

websocket_urlpatterns = []

if "ui" in settings.PROMETEUSPBX_CONFIG["modules"]:
    import ui.routing

    websocket_urlpatterns.append(
        path("ws/dashboard/", URLRouter(ui.routing.websocket_urlpatterns))
    )
