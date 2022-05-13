from django.apps import apps as global_apps
from django.db import models, DEFAULT_DB_ALIAS, router
from django.dispatch import receiver

from core.models import Model, User

# Create your models here.
from pbx.models_sip import SipEndpoint


class Context(Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Extension(Model):
    number = models.CharField(max_length=10)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    context = models.ForeignKey(
        Context,
        on_delete=models.SET_NULL,
        null=True,
        default=Context.objects.filter(name="default").first(),
    )


@receiver(models.signals.post_save, sender=Extension)
def post_create_extension(sender, instance, created, *args, **kwargs):
    if created:
        SipEndpoint.objects.create_extension(
            instance,
            username=instance.username,
            password=instance.password,
            context=instance.context,
        )


@receiver(models.signals.post_migrate)
def create_default_context(
    app_config, using=DEFAULT_DB_ALIAS, apps=global_apps, *args, **kwargs
):

    if not app_config.models_module:
        return

    try:
        Context = apps.get_model("pbx", "Context")
        pass
    except (ModuleNotFoundError, LookupError):
        return

    if not router.allow_migrate_model(using, Context):
        return

    if Context.objects.filter(name="default").exists():
        return

    context = Context.objects.create(name="default")
    context.save()
