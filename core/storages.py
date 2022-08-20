from django.utils.deconstruct import deconstructible
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import safe_join
from django.conf import settings as django_settings


class BaseGCP(GoogleCloudStorage):
    def __init__(self, default_acl, location, custom_endpoint=None, **settings):
        settings["default_acl"] = default_acl
        settings["location"] = safe_join(django_settings.GS_LOCATION, location)
        settings["custom_endpoint"] = custom_endpoint
        super().__init__(**settings)


@deconstructible
class PublicGCPStorage(BaseGCP):
    def __init__(self, default_acl="publicRead", **settings):
        settings["default_acl"] = default_acl
        settings["location"] = (
            "public"
            if getattr(django_settings, "GS_LOCATION_PUBLIC", None) is None
            else django_settings.GS_LOCATION_PUBLIC
        )
        settings["custom_endpoint"] = getattr(
            django_settings, "GS_CUSTOM_ENDPOINT_PUBLIC", None
        )
        super().__init__(**settings)


@deconstructible
class PrivateGCPStorage(BaseGCP):
    def __init__(self, default_acl="bucketOwnerFullControl", **settings):
        settings["default_acl"] = default_acl
        settings["location"] = (
            "private"
            if getattr(django_settings, "GS_LOCATION_PRIVATE", None)
            else django_settings.GS_LOCATION_PRIVATE
        )
        settings["custom_endpoint"] = getattr(
            django_settings, "GS_CUSTOM_ENDPOINT_PRIVATE", None
        )
        super().__init__(**settings)
