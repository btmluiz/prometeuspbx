import uuid

from django.contrib.auth.models import (
    AbstractUser,
    _user_get_permissions,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class PermissionManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, codename, *args, **kwargs):
        return self.get(codename=codename)


class Permission(models.Model):
    name = models.CharField(_("name"), max_length=255)
    codename = models.SlugField(_("codename"), unique=True)
    app_label = models.CharField(max_length=40)

    objects = PermissionManager()

    class Meta:
        verbose_name = _("permission")
        verbose_name_plural = _("permissions")
        ordering = ["codename"]

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.codename,)


class GroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Group(models.Model):
    name = models.CharField(_("name"), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission, verbose_name=_("permissions"), blank=True
    )

    objects = GroupManager()

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class PermissionsMixin(models.Model):
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_group_set",
        related_query_name="user_group",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_perm_set",
        related_query_name="user_perm",
    )

    class Meta:
        abstract = True

    def get_user_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has directly.
        Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "user")

    def get_group_permissions(self):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return [
            perm.codename
            for perm in Permission.objects.filter(group__in=self.groups.all())
        ]

    def get_all_permissions(self):
        return [
            perm.codename for perm in self.user_permissions.all()
        ] + self.get_group_permissions()

    def has_perm(self, perm):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return perm in self.get_all_permissions()

    def has_perms(self, perm_list):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        if self.is_active and self.is_superuser:
            return True
        return all(self.has_perm(perm) for perm in perm_list)


class Model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class User(PermissionsMixin, AbstractUser, Model):
    class Meta:
        ordering = ["first_name", "last_name"]

    def get_full_name(self):
        full_name = super().get_full_name()

        if full_name == "":
            return self.get_username()
        else:
            return full_name
