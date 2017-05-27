from .apns.apns import APNs, Frame, Payload
from .models import CertFile


import os
import time

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/files/'


def send_notification(message, device_token, use_sandbox=True):
    apns = APNs(use_sandbox=use_sandbox,
                cert_file=os.path.dirname(os.path.abspath(__file__)) + '/files/cert.pem',
                enhanced=True)

    payload = Payload(alert=message, sound='default', badge=1)

    frame = Frame()
    identifier = 1
    expiry = int(time.time() + 3600)
    priority = 10
    frame.add_item(device_token, payload, identifier, expiry, priority)
    apns.gateway_server.send_notification_multiple(frame)


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
