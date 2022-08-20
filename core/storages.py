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
        super().__init__(
            default_acl,
            location=getattr(django_settings, "GS_LOCATION_PUBLIC", "public"),
            custom_endpoint=getattr(django_settings, "GS_CUSTOM_ENDPOINT_PUBLIC", None),
            **settings
        )


@deconstructible
class PrivateGCPStorage(BaseGCP):
    def __init__(self, default_acl="bucketOwnerFullControl", **settings):
        super().__init__(
            default_acl,
            location=getattr(django_settings, "GS_LOCATION_PRIVATE", "private"),
            custom_endpoint=getattr(
                django_settings, "GS_CUSTOM_ENDPOINT_PRIVATE", None
            ),
            **settings
        )
