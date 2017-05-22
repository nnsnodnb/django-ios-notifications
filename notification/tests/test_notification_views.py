from django.contrib.auth.models import User
from django.test.client import RequestFactory
from unittest import TestCase
from ..models import DeviceToken
from ..views import device_token_receive

import json
import os


class NotificationViewDeviceTokenReceiveTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.device_token = '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76'
        self.uuid = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'

    def tearDown(self):
        DeviceToken.objects.all().delete()

    def tearDown(self):
        DeviceToken.objects.all().delete()

    def test_device_token_receive_with_all_parameter(self):
        parameter = {'device_token': self.device_token,
                     'uuid': self.uuid}
        request = self.factory.put('/receive/',
                                   json.dumps(parameter))
        request.content_type = 'application/json'
        response = device_token_receive(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'result': 'success'})

    def test_device_token_receive_with_only_device_token(self):
        parameter = {'device_token': self.device_token}
        request = self.factory.put('/receive/',
                                   json.dumps(parameter))
        request.content_type = 'application/json'
        response = device_token_receive(request)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'error': 'Bad Request'})

    def test_device_token_receive_with_only_uuid(self):
        parameter = {'uuid': self.uuid}
        request = self.factory.put('/receive/',
                                   json.dumps(parameter))
        request.content_type = 'application/json'
        response = device_token_receive(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'error': 'Bad Request'})

    def test_device_token_receive_without_parameter(self):
        request = self.factory.put('/receive/')
        response = device_token_receive(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'error': 'Bad Request'})

    def test_device_token_receive_with_twice(self):
        device_token = DeviceToken()
        device_token.device_token = '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76'
        device_token.uuid = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
        device_token.save()

        parameter = {'device_token': 'ec203ae05072eaa39474fd4bd06c3b36344602295078615cef67fcbdb7e94aef',
                     'uuid': 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'}
        request = self.factory.put('/receive/',
                                   json.dumps(parameter))
        request.content_type = 'application/json'
        response = device_token_receive(request)
        self.assertEqual(response.status_code, 200)

        get_device_token = DeviceToken.objects.get(uuid='XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX')
        self.assertNotEqual(device_token.device_token, get_device_token.device_token)
        self.assertEqual(get_device_token.device_token, 'ec203ae05072eaa39474fd4bd06c3b36344602295078615cef67fcbdb7e94aef')
        self.assertEqual(get_device_token.uuid, 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX')

    def test_device_token_receive_method_get(self):
        request = self.factory.get('/receive/')
        response = device_token_receive(request)
        self.assertEqual(response.status_code, 405)

    def test_device_token_receive_method_post(self):
        request = self.factory.post('/receive/')
        response = device_token_receive(request)
        self.assertEqual(response.status_code, 405)

    def test_device_token_receive_method_delete(self):
        request = self.factory.delete('/receive/')
        response = device_token_receive(request)
        self.assertEqual(response.status_code, 405)


class NotificationViewsSendNotificationWithDeviceTokenTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.device_token = '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76'
        self.uuid = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
        self.cert_file_path = os.path.dirname(os.path.abspath(__file__)) + '/cert.pem'
        self.super_user = User.objects.create_superuser(username='super_user',
                                                        password='test_case_for_super_user',
                                                        email='super_user@localhost')
        self.super_user.save()
        self.general_user = User.objects.create_user(username='general_user',
                                                     password='test_case_for_general_user')
        self.general_user.save()

    def tearDown(self):
        self.super_user.delete()
        self.general_user.delete()
        if not os.path.isfile(self.cert_file_path):
            return
        os.remove(self.cert_file_path)

    def test_target_develop_is_device_token_is_not_message_is_super_user(self):
        # Target: Development
        # Device token is here.
        # Message is not here.
        # Request by super user
        device_token = DeviceToken(device_token=self.device_token,
                                   uuid=self.uuid)
        device_token.save()
        f = open(self.cert_file_path, 'w')
        f.write('test_case_test_case_test_case')
        f.close()
        request = self.factory.get('/send/0/' + self.device_token)
        request.user = self.super_user
        response = send_notification_with_device_token(request)
        self.assertEqual(response.status_code, 200)
