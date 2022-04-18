import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class User(AbstractUser, Model):
    pass
