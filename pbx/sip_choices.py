from django.db import models
from django.utils.translation import gettext_lazy as _


class SipAuthTypeChoices(models.TextChoices):
    USER_PASSWORD = "userpass", _("User Password")
    MD5 = "md5", _("md5")
    GOOGLE_OAUTH = "google_oauth", _("google_oauth")


class SipCIDPrivacyChoices(models.TextChoices):
    ALLOWED_NOT_SCREENED = "allowed_not_screened", _("allowed_not_screened")
    ALLOWED_PASSED_SCREENED = "allowed_passed_screened", _("allowed_passed_screened")
    ALLOWED_FAILED_SCREENED = "allowed_failed_screened", _("allowed_failed_screened")
    ALLOWED = "allowed", _("allowed")
    PROHIB_NOT_SCREENED = "prohib_not_screened"
    PROHIB = "prohib", _("prohib")
    UNAVAILABLE = "unavailable", _("unavailable")


class SipConnectedLineMethodChoices(models.TextChoices):
    INVITE = "invite", _("invite")
    RE_INVITE = "reinvite", _("reinvite")
    UPDATE = "update", _("update")


class SipDirectMediaGlareMigrationChoices(models.TextChoices):
    NONE = "none", _("none")
    OUTGOING = "outgoing", _("outgoing")
    INCOMING = "incoming", _("incoming")


class SHAChoices(models.TextChoices):
    SHA_1 = "SHA-1", _("SHA-1")
    SHA_256 = "SHA-256", _("SHA-256")


class DTLSSetupChoices(models.TextChoices):
    ACTIVE = "active", _("active")
    PASSIVE = "passive", _("passive")
    ACTPASS = "actpass", _("actpass")


class DTMFModesChoices(models.TextChoices):
    RFC4733 = "rfc4733", _("rfc4733")
    IN_BAND = "inband", _("inband")
    INFO = "info", _("info")
    AUTO = "auto", _("auto")
    AUTO_INFO = "auto_info", _("auto_info")


class T38UDPTlEcChoices(models.TextChoices):
    NONE = "none", _("none")
    FEC = "fec", _("fec")
    REDUNDANCY = "redundancy", _("redundancy")


class RedirectMethodChoices(models.TextChoices):
    USER = "user", _("user")
    URI_CORE = "uri_core", _("uri_core")
    URI_PJSIP = "uri_pjsip", _("uri_pjsip")


class YesNoChoices(models.TextChoices):
    YES = "yes", _("yes")
    NO = "no", _("no")
