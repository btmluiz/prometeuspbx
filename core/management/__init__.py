from django.apps import apps as global_apps
from django.db import DEFAULT_DB_ALIAS, router
from django.utils.module_loading import import_string


def create_permissions(
    app_config, verbosity=2, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs
):
    if not app_config.models_module:
        return

    try:
        PERMISSIONS = import_string("%s.permissions.PERMISSIONS" % app_config.name)
        Permission = apps.get_model("core", "Permission")
    except (ModuleNotFoundError, LookupError):
        return

    if not router.allow_migrate_model(using, Permission):
        return

    formatted_perms = {}

    for perm in PERMISSIONS:
        if type(perm) in (list, tuple) and len(perm) == 2:
            formatted_perms[perm[0]] = perm[1]
        else:
            raise SyntaxError("Permission must be a list or tuple and have 2 values")

    all_perms_query = Permission.objects.using(using).filter(
        codename__in=formatted_perms.keys()
    )

    all_perms = set(all_perms_query.values_list("codename"))

    perms = [
        Permission(codename=codename, name=name, app_label=app_config.name)
        for codename, name in formatted_perms.items()
        if (codename,) not in all_perms
    ]

    Permission.objects.using(using).bulk_create(perms)
    if verbosity >= 2:
        for perm in perms:
            print("Adding permission '%s'" % perm)

    delete_permission = Permission.objects.filter(app_label=app_config.name).exclude(
        pk__in=[perm.pk for perm in all_perms_query],
    )
    delete_permission.delete()
