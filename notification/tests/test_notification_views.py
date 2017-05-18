from django.test.client import RequestFactory
from unittest import TestCase
from ..views import device_token_receive


class NotificationViewsTestCase(TestCase):

    def test_device_token_receive(self):
        rf = RequestFactory()
        get_request = rf.get('/hello/')
        post_request = rf.post('/submit/', {'foo': 'bar'})
