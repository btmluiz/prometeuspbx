# Generated by Django 4.1 on 2022-08-25 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pbx", "0016_recreate_extensions"),
    ]

    operations = [
        migrations.RunSQL(
            sql="create or replace view pbx_sipendpoint_view as select id::text as id, accept_multiple_sdp_answers, "
            "accountcode, acl, aggregate_mwi, allow, allow_overlap, allow_subscribe, allow_transfer, "
            "allow_unauthenticated_options, asymmetric_rtp_codec, bind_rtp_to_media_address, bundle, "
            "call_group, callerid, callerid_privacy, callerid_tag, codec_prefs_incoming_answer, "
            "codec_prefs_incoming_offer, codec_prefs_outgoing_answer, codec_prefs_outgoing_offer, "
            "connected_line_method, contact_acl, contact_deny, contact_permit, contact_user, context, "
            "cos_audio, cos_video, deny, device_state_busy_at, direct_media, direct_media_glare_mitigation, "
            "direct_media_method, disable_direct_media_on_nat, disallow, dtls_auto_generate_cert, "
            "dtls_ca_file, dtls_ca_path, dtls_cert_file, dtls_cipher, dtls_fingerprint, dtls_private_key, "
            "dtls_rekey, dtls_setup, dtls_verify, dtmf_mode, external_media_address, fax_detect, "
            "fax_detect_timeout, follow_early_media_fork, force_avp, force_rport, from_domain, from_user, "
            "g726_non_standard, ice_support, identify_by, ignore_183_without_sdp, inband_progress, "
            "incoming_mwi_mailbox, language, mailboxes, max_audio_streams, max_video_streams, media_address, "
            "media_encryption, media_encryption_optimistic, media_use_received_transport, message_context, "
            "moh_passthrough, moh_suggest, mwi_from_user, mwi_subscribe_replaces_unsolicited, named_call_group, "
            "named_pickup_group, notify_early_inuse_ringing, one_touch_recording, outbound_auth, outbound_proxy, "
            "permit, pickup_group, preferred_codec_only, record_off_feature, record_on_feature, redirect_method, "
            'refer_blind_progress, "100rel", rewrite_contact, rpid_immediate, rtcp_mux, rtp_engine, rtp_ipv6, '
            "rtp_keepalive, rtp_symmetric, rtp_timeout, rtp_timeout_hold, sdp_owner, sdp_session, "
            "send_connected_line, send_diversion, send_history_info, send_pai, send_rpid, set_var, srtp_tag_32, "
            "stir_shaken, sub_min_expiry, subscribe_context, suppress_q850_reason_headers, t38_udptl, "
            "t38_udptl_ec, t38_udptl_ipv6, t38_udptl_maxdatagram, t38_udptl_nat, timers, timers_min_se, "
            "timers_sess_expires, tone_zone, tos_audio, tos_video, transport, trust_connected_line, "
            "trust_id_inbound, trust_id_outbound, use_avpf, use_ptime, user_eq_phone, voicemail_extension, "
            "webrtc, aors::text as aors, auth::text as auth from pbx_sipendpoint",
            reverse_sql="drop view if exists pbx_sipendpoint_view",
        ),
        migrations.RunSQL(
            sql="create or replace view pbx_sipaor_view as select id::text as id, contact, "
            "default_expiration, mailboxes, max_contacts, minimum_expiration, remove_existing,"
            " qualify_frequency, authenticate_qualify, maximum_expiration, outbound_proxy, "
            "support_path, qualify_timeout, voicemail_extension from pbx_sipaor",
            reverse_sql="drop view if exists pbx_sipaor_view",
        ),
        migrations.RunSQL(
            sql="create or replace view pbx_dialplan_view as select id::text as id, "
            "exten, priority, app, appdata, context_id::text as context from pbx_dialplan",
            reverse_sql="drop view if exists pbx_dialplan_view",
        ),
    ]
