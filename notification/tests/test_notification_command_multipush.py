from unittest import TestCase
from django.core.management import call_command


class ManagementCommandsMultiPushTest(TestCase):

    def setUp(self):
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

    def test_without_device_tokens(self):
        args = []
        
        call_command('multipush', *args, **self.options)
