from django.apps import AppConfig
from django.db.models.signals import post_migrate

from core.management import create_permissions


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        post_migrate.connect(
            create_permissions,
            dispatch_uid="prometeuspbx.core.management.create_permissions",
        )
