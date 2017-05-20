from apns import APNs, Payload

import os


def send_notification(message, device_token, use_sandbox=True):
    try:
        apns = APNs(use_sandbox=use_sandbox,
                    cert_file=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/cert.pem',
                    enhanced=True)

        payload = Payload(alert=message, sound='default', badge=1)
        apns.gateway_server.send_notification(device_token, payload)
        return None
    except FileNotFoundError as e:
        return e
