from unittest import TestCase
from django.core.management import call_command
from notification.models import DeviceToken


class ManagementCommandsSinglePushTest(TestCase):

    def setUp(self):
        self.command_name = 'singlepush'
        self.args = []
        self.options = {'verbosity': 1,
                        'settings': None,
                        'pythonpath': None,
                        'traceback': False,
                        'no_color': False,
                        'sandbox': False,
                        'device_token': None,
                        'title': None,
                        'subtitle': None,
                        'body': None,
                        'sound': 'default',
                        'badge': 1,
                        'content_available': False,
                        'mutable_content': False,
                        'extra': None}
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
                        'device_token': None,
                        'title': None,
                        'subtitle': None,
                        'body': None,
                        'sound': 'default',
                        'badge': 1,
                        'content_available': False,
                        'mutable_content': False,
                        'extra': None}
        self.device_token.delete()

    def test_without_device_token_and_title(self):
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_with_device_token_and_title(self):
        self.options['sandbox'] = True
        self.options['device_token'] = self.device_token.device_token
        self.options['title'] = 'test case title'
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_with_device_token_without_title(self):
        self.options['device_token'] = self.device_token.device_token
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_target_develop_with_device_token_and_title_without_cert(self):
        self.options['sandbox'] = True
        self.options['device_token'] = self.device_token.device_token
        self.options['title'] = 'test case title'
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_valid_custom(self):
        self.options['extra'] = "{'key':'value'}"
        self.options['sandbox'] = True
        self.options['device_token'] = self.device_token.device_token
        self.options['title'] = 'test case title'
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_invalid_custom(self):
        self.options['extra'] = "{'key':'value','key2'}"
        self.options['sandbox'] = True
        self.options['device_token'] = self.device_token.device_token
        self.options['title'] = 'test case title'
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)

    def test_not_match_device_token(self):
        self.options['sandbox'] = True
        self.options['device_token'] = '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e75'
        self.options['title'] = 'test case title'
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *self.args, **self.options)
