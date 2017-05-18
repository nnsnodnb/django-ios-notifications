from django.core.urlresolvers import resolve
from unittest import TestCase
from ..views import device_token_receive


class NotificationUrlsTestCase(TestCase):

    def test_url_resolves_to_device_token_receive(self):
        found = resolve('/receive')
        self.assertEqual(found.func, device_token_receive)
