from django.apps import apps as global_apps
from django.core.exceptions import ValidationError
from django.db import models, DEFAULT_DB_ALIAS, router
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from core.models import Model, User
from pbx.models.sip import SipEndpoint


# from pbx.models_sip import SipEndpoint

# Create your models here.


class Context(Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

    @property
    def context_dialplan(self):
        return f"{str(self.id)}"


def validate_user_exists(value):
    if not User.objects.filter(id=value).exists():
        raise ValidationError(
            _("User with id {} does not exist").format(value), code="invalid"
        )


class Extension(Model):
    number = models.CharField(max_length=10)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    user = models.UUIDField(null=True, blank=True, validators=[validate_user_exists])
    context = models.ForeignKey(Context, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.context:
            self.context = Context.objects.filter(name="default").first()
        super().save(*args, **kwargs)


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

    if not app_config.models_module or using != "asterisk":
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


@receiver(models.signals.post_save, sender=Context)
def on_create_context(sender, instance, *args, **kwargs):
    pass


@receiver(models.signals.post_delete, sender=User)
def on_user_delete(sender, instance, *args, **kwargs):
    Extension.objects.filter(user=instance.id).delete()
