from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from notification.apns.apns import APNs, Frame, Payload, PayloadAlert
from notification.models import DeviceToken, CertFile

import json
import logging
import os.path
import random
import sys
import time


CERT_FILE_UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'files/'
)


class Command(BaseCommand):

    help = 'Send Push Notification to multi device tokens.'

    def __init__(self):
        self.frame = Frame()
        self.expiry = int(time.time() + 3600)
        self.priority = 10

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
            nargs='+',
            type=str,
            dest='device_tokens',
            help='Target device tokens.',
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
            '--custom',
            action='store',
            type=str,
            metavar='STR_JSON',
            dest='custom',
            help='Attach custom JSON.'
        )

    def handle(self, *args, **options):
        error = False
        if options['device_tokens'] is None:
            try:
                raise ValueError('Please specify a device tokens (-t or --token)')
            except ValueError as e:
                error = True
                logging.error(e)

        if options['title'] is None:
            try:
                raise ValueError('Please input title in push notification (--title)')
            except ValueError as e:
                error = True
                logging.error(e)

        if error:
            sys.exit()

        if options['custom'] is not None:
            options['custom'] = options['custom'].replace('\"', '\'')
            try:
                json.loads(options['custom'])
            except json.decoder.JSONDecodeError as e:
                logging.error(e)

        device_tokens = list(filter(lambda device_token:
                                    DeviceToken.objects.filter(device_token=device_token).count() > 0,
                                    options['device_tokens']))

        _ = map(lambda item: logging.warning('There is no match for the specified device token: {}'.format(item)),
                list(set(options['device_tokens']) - set(device_tokens)))

        try:
            cert_file = CertFile.objects.get(target_mode=int(not options['sandbox']), is_use=True)
        except ObjectDoesNotExist:
            sys.exit(logging.error('Certificate file has not been uploaded'))

        apns = APNs(use_sandbox=options['sandbox'], cert_file=CERT_FILE_UPLOAD_DIR + cert_file.filename, enhanced=True)

        identifier = random.getrandbits(32)
        payload_alert = PayloadAlert(title=options['title'], subtitle=options['subtitle'], body=options['body'])
        payload = Payload(alert=payload_alert if payload_alert.body is not None else payload_alert.title,
                          sound=options['sound'],
                          badge=options['badge'],
                          content_available=options['content_available'],
                          mutable_content=options['mutable_content'],
                          custom=options['custom'])

        _ = map(lambda device_token:
                apns.gateway_server.send_notification(device_token, payload, identifier=identifier),
                device_tokens)
