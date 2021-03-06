import json
import os.path
import sys

from django.core.management.base import BaseCommand

from notification.apns.apns import APNs, Payload, PayloadAlert
from notification.models import DeviceToken, CertFile

CERT_FILE_UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'files/'
)
PYTHON_VERSION = sys.version_info


class Command(BaseCommand):

    help = 'Send Push Notification to single device token.'

    def add_arguments(self, parser):
        parser.add_argument(
            "-s", "--sandbox",
            action="store_true",
            dest="sandbox",
            default=False,
            help="Use apple sandbox.",
        )
        parser.add_argument(
            '-t', '--token',
            action='store',
            type=str,
            metavar='DEVICE_TOKEN',
            dest='device_token',
            help='Target device token.',
        )
        parser.add_argument(
            '--title',
            action='store',
            type=str,
            metavar='TITLE',
            dest='title',
            help='Title displayed in push notification.',
        )
        parser.add_argument(
            '--subtitle',
            action='store',
            type=str,
            metavar='SUBTITLE',
            dest='subtitle',
            help='Subtitle displayes in push notification.',
        )
        parser.add_argument(
            '--body',
            action='store',
            type=str,
            metavar='BODY',
            dest='body',
            help='Body displayed in push notification.',
        )
        parser.add_argument(
            '--sound',
            action='store',
            type=str,
            metavar='SOUND',
            dest='sound',
            default='default',
            help='Sounds to be heard when push notification is received.',
        )
        parser.add_argument(
            '--badge',
            action='store',
            type=int,
            metavar='BADGE',
            dest='badge',
            default=1,
            help='Badge displayed on application icon.',
        )
        parser.add_argument(
            '-c', '--contentavailable',
            action='store_true',
            dest='content_available',
            default=False,
            help='Use content-available. (Support for iOS7 or higher)',
        )
        parser.add_argument(
            '-m', '--mutablecontent',
            action='store_true',
            dest='mutable_content',
            default=False,
            help='Use mutable-content. (Support for iOS9 or higher)',
        )
        parser.add_argument(
            '-e', '--extra',
            action='store',
            type=str,
            metavar='EXTRA',
            dest='extra',
            help='Custom notification payload values as a JSON dictionary. (-e or --extra)'
        )

    def handle(self, *args, **options):
        if options['device_token'] is None:
            raise ValueError('Please specify a device token (-t or --token)')

        if options['title'] is None:
            raise ValueError('Please input title in push notification (--title)')

        custom = None
        if options['extra'] is not None:
            extra = options['extra'].replace('\'', '\"')
            custom = json.loads(extra)

        DeviceToken.objects.get(device_token=options['device_token'])
        cert_file = CertFile.objects.get(target_mode=int(not options['sandbox']), is_use=True)

        apns = APNs(use_sandbox=options['sandbox'], cert_file=CERT_FILE_UPLOAD_DIR + cert_file.filename)

        payload_alert = PayloadAlert(title=options['title'], subtitle=options['subtitle'], body=options['body'])
        payload = Payload(alert=payload_alert if payload_alert.body is not None else payload_alert.title,
                          sound=options['sound'],
                          badge=options['badge'],
                          content_available=options['content_available'],
                          mutable_content=options['mutable_content'],
                          custom=custom)

        apns.gateway_server.send_notification(options['device_token'], payload)
