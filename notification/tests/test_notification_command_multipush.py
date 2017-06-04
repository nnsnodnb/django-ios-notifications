from unittest import TestCase
from django.core.management import call_command


class ManagementCommandsMultiPushTest(TestCase):

    def setUp(self):
        self.command_name = 'multipush'
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

    def tearDown(self):
        pass

    def test_without_device_tokens_and_title(self):
        args = []
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *args, **self.options)

    def test_with_device_token_for_all_without_title(self):
        args = []
        self.options['all'] = True
        with self.assertRaises(SystemExit):
            call_command(self.command_name, *args, **self.options)
