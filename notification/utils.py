from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from OpenSSL import crypto
from .apns.apns import APNs, Payload
from .models import CertFile

import os
import os.path

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/files/'


def send_notification(message, device_token, use_sandbox=True):
    try:
        cert_file = CertFile.objects.get(target_mode=0 if use_sandbox else 1, is_use=True)
        apns = APNs(use_sandbox=use_sandbox,
                    cert_file=UPLOAD_DIR + cert_file.filename,
                    key_file=UPLOAD_DIR + cert_file.filename)

        payload = Payload(alert=message, sound='default', badge=1)

        apns.gateway_server.send_notification(device_token, payload)

    except ObjectDoesNotExist:
        raise CertFile.DoesNotExist


def upload_certificate(cert_file, target_mode):
    if os.path.splitext(cert_file.name)[1] != '.pem':
        return {'error': 'wrong'}

    cert_files = CertFile.objects.filter(target_mode=target_mode, is_use=True)
    if cert_files.count() == 1:
        current_file = cert_files.first()
        current_file.is_use = False
        current_file.save()
        if os.path.isfile(UPLOAD_DIR + current_file.filename):
            os.remove(UPLOAD_DIR + current_file.filename)

    destination = open(os.path.join(UPLOAD_DIR, cert_file.name), 'wb+')
    for chunk in cert_file.chunks():
        destination.write(chunk)
    destination.close()

    pem_file = open(os.path.join(UPLOAD_DIR, cert_file.name), 'rb').read()
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem_file)
    expire_date = datetime.strptime(cert.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")

    CertFile(filename=cert_file.name, target_mode=target_mode, is_use=True, expire_date=expire_date).save()

    return {'error': None}
