"""PrometeusPBX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include

if "ui" in settings.PROMETEUSPBX_CONFIG["modules"]:
    handler500 = "ui.views.handler500"

urlpatterns = [
    path("", include("core.urls")),
    #    path('admin/', admin.site.urls),
]

for module in settings.PROMETEUSPBX_CONFIG["modules"]:
    try:
        p = path("", include(("%s.urls" % module, module), namespace=module))

        urlpatterns.append(p)
    except ModuleNotFoundError:
        pass
