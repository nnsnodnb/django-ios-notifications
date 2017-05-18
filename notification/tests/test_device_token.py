from ..models import DeviceToken
from django.contrib.auth.models import User
from unittest import TestCase

import six


class DeviceTokenTestCase(TestCase):

    def tearDown(self):
        DeviceToken.objects.all().delete()
        User.objects.all().delete()

    def test_no_device_token(self):
        device_tokens = DeviceToken.objects.all()
        six.assertCountEqual(self, device_tokens, [])

    def test_one_device_token_without_user(self):
        device_token = DeviceToken()
        device_token.device_token = '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76'
        device_token.uuid = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
        device_token.save()

        get_device_token = DeviceToken.objects.filter().first()
        self.assertEqual(device_token.device_token, get_device_token.device_token)
        self.assertEqual(device_token.uuid, get_device_token.uuid)
        self.assertEqual(device_token.user, get_device_token.user)
        self.assertIsNone(get_device_token.user)

    def test_one_device_token_with_user(self):
        device_token = DeviceToken()
        device_token.device_token = '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76'
        device_token.uuid = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'

        user = User.objects.create_user(username='test_case',
                                        email='test_case@localhost',
                                        password='test_case_test_case')
        user.save()

        device_token.user = user
        device_token.save()

        get_device_token = DeviceToken.objects.filter().first()
        self.assertEqual(device_token.device_token, get_device_token.device_token)
        self.assertEqual(device_token.uuid, get_device_token.uuid)
        self.assertEqual(device_token.user, get_device_token.user)
        self.assertIsNotNone(get_device_token.user)

        get_user = User.objects.filter().first()
        self.assertEqual(user, get_user)
