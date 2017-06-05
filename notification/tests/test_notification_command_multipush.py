from unittest import TestCase
from django.core.management import call_command
from notification.models import DeviceToken, CertFile


class ManagementCommandsMultiPushTest(TestCase):

    def setUp(self):
        self.command_name = 'multipush'
        self.args = []
        self.options = {'verbosity': 1,
                        'settings': None,
                        'pythonpath': None,
                        'traceback': False,
                        'no_color': False,
                        'sandbox': False,
                        'device_tokens': None,
                        'all': False,
                        'title': None,
                        'subtitle': None,
                        'body': None,
                        'sound': 'default',
                        'badge': 1,
                        'content_available': False,
                        'mutable_content': False,
                        'extra': None}
        CertFile(filename='cert.pem').save()
        self.device_token = DeviceToken(device_token='8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76',
                                        uuid='XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX')
        self.device_token.save()

    def tearDown(self):
        self.args = []
        self.options = {'verbosity': 1,
                        'settings': None,
                        'pythonpath': None,
                        'traceback': False,
                        'no_color': False,
                        'sandbox': False,
                        'device_tokens': None,
                        'all': False,
                        'title': None,
                        'subtitle': None,
                        'body': None,
                        'sound': 'default',
                        'badge': 1,
                        'content_available': False,
                        'mutable_content': False,
                        'extra': None}
        CertFile.objects.all().delete()
        self.device_token.delete()

    def test_without_device_tokens_and_title(self):
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_with_device_token_for_specified_and_title(self):
        self.options['sandbox'] = True
        self.options['device_tokens'] = [self.device_token.device_token]
        self.options['title'] = 'test case title'
        CertFile.objects.all().delete()
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_with_device_token_for_all_without_title(self):
        self.options['all'] = True
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_target_develop_with_device_token_for_all_and_title_without_cert(self):
        self.options['sandbox'] = True
        self.options['all'] = True
        self.options['title'] = 'test case title'
        CertFile.objects.all().delete()
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_valid_custom(self):
        self.options['extra'] = "{'key':'value'}"
        self.options['sandbox'] = True
        self.options['all'] = True
        self.options['title'] = 'test case title'
        CertFile.objects.all().delete()
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_invalid_custom(self):
        self.options['extra'] = "{'key':'value','key2'}"
        self.options['sandbox'] = True
        self.options['all'] = True
        self.options['title'] = 'test case title'
        CertFile.objects.all().delete()
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)
