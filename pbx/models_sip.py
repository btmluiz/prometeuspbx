import uuid

from django.db import models, transaction

from pbx.sip_choices import (
    SipAuthTypeChoices,
    SipCIDPrivacyChoices,
    SipConnectedLineMethodChoices,
    SipDirectMediaGlareMigrationChoices,
    SHAChoices,
    DTLSSetupChoices,
    YesNoChoices,
    DTMFModesChoices,
    RedirectMethodChoices,
    T38UDPTlEcChoices,
)


# Create your models here.


class SipManager(models.Manager):
    @transaction.atomic
    def create_extension(self, extension, username, password, context, allow=None):
        if not allow:
            allow = "ulaw,alaw"

        sip_aor = SipAor(sip_id=username, extension=extension)
        sip_auth = SipAuth(
            sip_id=username, username=username, password=password, extension=extension
        )
        sip_endpoint = SipEndpoint(
            sip_id=username,
            aors=sip_aor,
            auth=sip_auth,
            context=context,
            allow=allow,
            extension=extension,
        )

        sip_aor.save(using=self._db)
        sip_auth.save(using=self._db)
        sip_endpoint.save(using=self._db)
        return sip_endpoint


class ModelSip(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_column="pk"
    )
    sip_id = models.CharField(max_length=255, db_column="id", unique=True, blank=True)
    extension = models.ForeignKey("pbx.Extension", on_delete=models.CASCADE)

    objects = SipManager()

    @property
    def sip_pk(self):
        return self.sip_id

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class SipAor(ModelSip):
    contact = models.CharField(max_length=255, blank=True, null=True)
    default_expiration = models.IntegerField(blank=True, null=True, default=120)
    mailboxes = models.CharField(max_length=80, blank=True, null=True)
    max_contacts = models.IntegerField(blank=True, null=True, default=5)
    minimum_expiration = models.IntegerField(blank=True, null=True, default=60)
    remove_existing = models.TextField(blank=True, null=True)
    qualify_frequency = models.IntegerField(blank=True, null=True, default=60)
    authenticate_qualify = models.BooleanField(default=True)
    maximum_expiration = models.IntegerField(blank=True, null=True, default=3600)
    outbound_proxy = models.CharField(max_length=40, blank=True, null=True)
    support_path = models.BooleanField(default=True)
    qualify_timeout = models.FloatField(blank=True, null=True)
    voicemail_extension = models.CharField(max_length=40, blank=True, null=True)


class SipAuth(ModelSip):
    auth_type = models.CharField(
        max_length=255, blank=True, null=True, choices=SipAuthTypeChoices.choices
    )
    nonce_lifetime = models.IntegerField(blank=True, null=True)
    md5_cred = models.CharField(max_length=40, blank=True, null=True)
    password = models.CharField(max_length=80)
    realm = models.CharField(max_length=40, blank=True, null=True)
    username = models.CharField(max_length=40, unique=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    oauth_clientid = models.CharField(max_length=255, blank=True, null=True)
    oauth_secret = models.CharField(max_length=255, blank=True, null=True)

    def save(self, **kwargs):
        self.sip_id = self.username
        return super().save(**kwargs)


class SipEndpoint(ModelSip):
    accept_multiple_sdp_answers = models.BooleanField(default=False)
    accountcode = models.CharField(max_length=80, blank=True, null=True)
    acl = models.CharField(max_length=40, blank=True)
    aggregate_mwi = models.BooleanField(default=True)
    allow = models.CharField(max_length=200, default="alaw,ulaw")
    allow_overlap = models.BooleanField(default=True)
    allow_subscribe = models.BooleanField(default=True)
    allow_transfer = models.BooleanField(default=True)
    allow_unauthenticated_options = models.BooleanField(default=False)
    aors = models.ForeignKey(
        SipAor, to_field="sip_id", on_delete=models.CASCADE, db_column="aors"
    )
    asymmetric_rtp_codec = models.BooleanField(default=False)
    auth = models.ForeignKey(
        SipAuth, to_field="sip_id", on_delete=models.CASCADE, db_column="auth"
    )
    bind_rtp_to_media_address = models.BooleanField(default=False)
    bundle = models.BooleanField(default=False)
    call_group = models.CharField(max_length=40, blank=True, null=True)
    callerid = models.CharField(max_length=40, blank=True, null=True)
    callerid_privacy = models.CharField(
        max_length=40,
        default=SipCIDPrivacyChoices.ALLOWED_NOT_SCREENED,
        choices=SipCIDPrivacyChoices.choices,
    )
    callerid_tag = models.CharField(max_length=40, blank=True, null=True)
    codec_prefs_incoming_answer = models.CharField(
        max_length=128, blank=True, null=True
    )
    codec_prefs_incoming_offer = models.CharField(max_length=128, blank=True, null=True)
    codec_prefs_outgoing_answer = models.CharField(
        max_length=128, blank=True, null=True
    )
    codec_prefs_outgoing_offer = models.CharField(max_length=128, blank=True, null=True)
    connected_line_method = models.CharField(
        max_length=40,
        default=SipConnectedLineMethodChoices.INVITE,
        choices=SipConnectedLineMethodChoices.choices,
    )
    contact_acl = models.CharField(max_length=40, blank=True, null=True)
    contact_deny = models.CharField(max_length=95, blank=True, null=True)
    contact_permit = models.CharField(max_length=95, blank=True, null=True)
    contact_user = models.CharField(max_length=80, blank=True, null=True)
    context = models.CharField(max_length=40, blank=True, null=True)
    cos_audio = models.IntegerField(blank=True, null=True)
    cos_video = models.IntegerField(blank=True, null=True)
    deny = models.CharField(max_length=95, blank=True, null=True)
    device_state_busy_at = models.IntegerField(blank=True, null=True)
    direct_media = models.BooleanField(default=False)
    direct_media_glare_mitigation = models.CharField(
        max_length=40,
        default=SipDirectMediaGlareMigrationChoices.NONE,
        choices=SipDirectMediaGlareMigrationChoices.choices,
    )
    direct_media_method = models.CharField(
        max_length=40,
        default=SipConnectedLineMethodChoices.INVITE,
        choices=SipDirectMediaGlareMigrationChoices.choices,
    )
    disable_direct_media_on_nat = models.BooleanField(default=False)
    disallow = models.CharField(max_length=200, default="all")
    dtls_auto_generate_cert = models.BooleanField(default=False)
    dtls_ca_file = models.CharField(max_length=200, blank=True, null=True)
    dtls_ca_path = models.CharField(max_length=200, blank=True, null=True)
    dtls_cert_file = models.CharField(max_length=200, blank=True, null=True)
    dtls_cipher = models.CharField(max_length=200, blank=True, null=True)
    dtls_fingerprint = models.CharField(
        max_length=40, default=SHAChoices.SHA_256, choices=SHAChoices.choices
    )
    dtls_private_key = models.CharField(max_length=200, blank=True, null=True)
    dtls_rekey = models.CharField(max_length=40, blank=True, null=True)
    dtls_setup = models.CharField(
        max_length=40, default=DTLSSetupChoices.ACTIVE, choices=DTLSSetupChoices.choices
    )
    dtls_verify = models.CharField(
        max_length=10, default=YesNoChoices.NO, choices=YesNoChoices.choices
    )
    dtmf_mode = models.CharField(
        max_length=40,
        default=DTMFModesChoices.RFC4733,
        choices=DTMFModesChoices.choices,
    )
    external_media_address = models.CharField(max_length=40, blank=True, null=True)
    fax_detect = models.BooleanField(default=False)
    fax_detect_timeout = models.IntegerField(blank=True, default=0)
    follow_early_media_fork = models.BooleanField(default=True)
    force_avp = models.BooleanField(default=False)
    force_rport = models.BooleanField(default=True)
    from_domain = models.CharField(max_length=255, blank=True, null=True)
    from_user = models.CharField(max_length=40, blank=True, null=True)
    g726_non_standard = models.BooleanField(default=False)
    ice_support = models.BooleanField(default=False)
    identify_by = models.CharField(max_length=80, blank=True, null=True)
    ignore_183_without_sdp = models.BooleanField(default=False)
    inband_progress = models.BooleanField(default=False)
    incoming_mwi_mailbox = models.CharField(max_length=40, blank=True, null=True)
    language = models.CharField(max_length=40, blank=True, null=True)
    mailboxes = models.CharField(max_length=40, blank=True, null=True)
    max_audio_streams = models.IntegerField(blank=True, default=1)
    max_video_streams = models.IntegerField(blank=True, default=1)
    media_address = models.CharField(max_length=40, blank=True, null=True)
    media_encryption = models.CharField(
        max_length=10, default=YesNoChoices.NO, choices=YesNoChoices.choices
    )
    media_encryption_optimistic = models.BooleanField(default=False)
    media_use_received_transport = models.BooleanField(default=False)
    message_context = models.CharField(max_length=40, blank=True, null=True)
    moh_passthrough = models.BooleanField(default=False)
    moh_suggest = models.CharField(max_length=40, blank=True, default="default")
    mwi_from_user = models.CharField(max_length=40, blank=True, null=True)
    mwi_subscribe_replaces_unsolicited = models.BooleanField(default=False)
    named_call_group = models.CharField(max_length=40, blank=True, null=True)
    named_pickup_group = models.CharField(max_length=40, blank=True, null=True)
    notify_early_inuse_ringing = models.BooleanField(default=False)
    one_touch_recording = models.BooleanField(default=False)
    outbound_auth = models.CharField(max_length=40, blank=True, null=True)
    outbound_proxy = models.CharField(max_length=40, blank=True, null=True)
    permit = models.CharField(max_length=95, blank=True, null=True)
    pickup_group = models.CharField(max_length=40, blank=True, null=True)
    preferred_codec_only = models.BooleanField(default=False)
    record_off_feature = models.CharField(
        max_length=40, blank=True, default="automixmon"
    )
    record_on_feature = models.CharField(
        max_length=40, blank=True, default="automixmon"
    )
    redirect_method = models.CharField(
        max_length=40,
        default=RedirectMethodChoices.USER,
        choices=RedirectMethodChoices.choices,
    )
    refer_blind_progress = models.BooleanField(default=False)
    rel100 = models.BooleanField(db_column="100rel", default=True)
    rewrite_contact = models.BooleanField(default=True)
    rpid_immediate = models.BooleanField(default=False)
    rtcp_mux = models.BooleanField(default=False)
    rtp_engine = models.CharField(max_length=40, blank=True, null=True)
    rtp_ipv6 = models.BooleanField(default=False)
    rtp_keepalive = models.IntegerField(blank=True, default=0)
    rtp_symmetric = models.BooleanField(default=True)
    rtp_timeout = models.IntegerField(blank=True, default=0)
    rtp_timeout_hold = models.IntegerField(blank=True, default=0)
    sdp_owner = models.CharField(max_length=40, blank=True, null=True)
    sdp_session = models.CharField(max_length=40, blank=True, null=True)
    send_connected_line = models.BooleanField(default=True)
    send_diversion = models.BooleanField(default=True)
    send_history_info = models.BooleanField(default=False)
    send_pai = models.BooleanField(default=False)
    send_rpid = models.BooleanField(default=False)
    set_var = models.TextField(blank=True, null=True)
    srtp_tag_32 = models.BooleanField(default=False)
    stir_shaken = models.BooleanField(default=False)
    sub_min_expiry = models.IntegerField(blank=True, default=0)
    subscribe_context = models.CharField(max_length=40, blank=True, null=True)
    suppress_q850_reason_headers = models.BooleanField(default=False)
    t38_udptl = models.BooleanField(default=False)
    t38_udptl_ec = models.CharField(
        max_length=40, default=T38UDPTlEcChoices.NONE, choices=T38UDPTlEcChoices.choices
    )
    t38_udptl_ipv6 = models.BooleanField(default=False)
    t38_udptl_maxdatagram = models.IntegerField(blank=True, default=0)
    t38_udptl_nat = models.BooleanField(default=False)
    timers = models.BooleanField(default=True)
    timers_min_se = models.IntegerField(blank=True, default=90)
    timers_sess_expires = models.IntegerField(blank=True, default=1800)
    tone_zone = models.CharField(max_length=40, blank=True, null=True)
    tos_audio = models.CharField(max_length=10, blank=True, null=True)
    tos_video = models.CharField(max_length=10, blank=True, null=True)
    transport = models.CharField(
        max_length=40, blank=True, null=True, default="transport-udp"
    )
    trust_connected_line = models.BooleanField(default=True)
    trust_id_inbound = models.BooleanField(default=False)
    trust_id_outbound = models.BooleanField(default=False)
    use_avpf = models.BooleanField(default=False)
    use_ptime = models.BooleanField(default=False)
    user_eq_phone = models.BooleanField(default=False)
    voicemail_extension = models.CharField(max_length=40, blank=True, null=True)
    webrtc = models.BooleanField(default=False)

    def save(self, **kwargs):
        self.sip_id = self.auth.sip_pk
        return super().save(**kwargs)


class SipContact(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    uri = models.CharField(max_length=255, null=True, default=None)
    expiration_time = models.IntegerField(null=True, default=None)
    qualify_frequency = models.IntegerField(null=True, default=None)
    outbound_proxy = models.CharField(max_length=255, null=True, default=None)
    path = models.TextField()
    user_agent = models.CharField(max_length=255, null=True, default=None)
    qualify_timeout = models.FloatField(null=True, default=None)
    reg_server = models.CharField(max_length=255, null=True, default=None)
    authenticate_qualify = models.SlugField(
        choices=YesNoChoices.choices, default=None, null=True
    )
    via_addr = models.CharField(max_length=255, null=True, default=None)
    via_port = models.IntegerField(null=True, default=None)
    call_id = models.CharField(max_length=255, null=True, default=None)
    endpoint = models.CharField(max_length=255, null=True, default=None)
    prune_on_boot = models.SlugField(
        choices=YesNoChoices.choices, default=None, null=True
    )

    class Meta:
        unique_together = (
            "id",
            "reg_server",
        )
