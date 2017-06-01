from unittest import TestCase
from django.core.management import call_command


class ManagementCommandsSinglePushTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hoge(self):
        args = []
        opts = {}
        call_command('singlepush', *args, **opts)
