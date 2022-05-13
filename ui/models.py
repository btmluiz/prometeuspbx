from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from core.models import Model, User


# Create your models here.


class Notification(Model):
    class TypeChoices(models.TextChoices):
        TOAST = "toast", "Toast"

    title = models.CharField(max_length=40, blank=True, null=True)
    content = models.TextField()
    type = models.SlugField(choices=TypeChoices.choices, default=TypeChoices.TOAST)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


@receiver(models.signals.post_save, sender=Notification)
def handle_notification(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    if instance.user:
        print("sending notification to: ui_%s" % instance.user.pk)
        async_to_sync(channel_layer.group_send)(
            "ui_%s" % str(instance.user.pk),
            {
                "type": "send_notification",
                "data": {
                    "type": instance.type,
                    "title": instance.title,
                    "content": instance.content,
                },
            },
        )
