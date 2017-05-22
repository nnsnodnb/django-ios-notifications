from apns import APNs, Frame, Payload

import os
import time


def send_notification(message, device_token, use_sandbox=True):
    apns = APNs(use_sandbox=use_sandbox,
                cert_file=os.path.dirname(os.path.abspath(__file__)) + '/cert.pem',
                enhanced=True)

    payload = Payload(alert=message, sound='default', badge=1)

    frame = Frame()
    identifier = 1
    expiry = int(time.time() + 3600)
    priority = 10
    frame.add_item(device_token, payload, identifier, expiry, priority)
    apns.gateway_server.send_notification_multiple(frame)
