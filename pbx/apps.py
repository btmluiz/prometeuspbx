from django.apps import AppConfig


class PbxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pbx"
    models_module = "pbx.models"
