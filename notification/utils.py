from django.core.exceptions import ObjectDoesNotExist
from .apns.apns import APNs, Payload
from .models import CertFile


import os

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/files/'


def send_notification(message,
                      device_tokens,
                      sound='default',
                      badge=1,
                      content_available=False,
                      mutable_content=False,
                      custom=None,
                      use_sandbox=True,
                      payload_alert=None):
    try:
        cert_file = CertFile.objects.get(target_mode=0 if use_sandbox else 1, is_use=True)
        apns = APNs(use_sandbox=use_sandbox,
                    cert_file=UPLOAD_DIR + cert_file.filename,
                    enhanced=True)
        payload = Payload(alert=payload_alert or message,
                          sound=sound,
                          badge=badge,
                          content_available=content_available,
                          mutable_content=mutable_content,
                          custom=custom)
        for device_token in device_tokens:
            apns.gateway_server.send_notification(device_token, payload=payload)
    except ObjectDoesNotExist:
        raise CertFile.DoesNotExist


def upload_certificate(cert_file, target_mode):
    if not cert_file.name.endswith('.pem'):
        return {'error': 'wrong'}

    cert_files = CertFile.objects.filter(target_mode=target_mode, is_use=True)
    if cert_files.count() == 1:
        current_file = cert_files.first()
        current_file.is_use = False
        current_file.save()
        if os.path.isfile(UPLOAD_DIR + current_file.filename):
            os.remove(UPLOAD_DIR + current_file.filename)

    destination = open(UPLOAD_DIR + cert_file.name, 'wb+')
    for chunk in cert_file.chunks():
        destination.write(chunk)
    destination.close()

    CertFile(filename=cert_file.name, target_mode=target_mode, is_use=True).save()

    return {'error': None}
