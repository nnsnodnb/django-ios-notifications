from django.test.client import RequestFactory
from unittest import TestCase
from ..models import DeviceToken
from ..views import device_token_receive

import json


class NotificationViewsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        DeviceToken.objects.all().delete()

    def test_device_token_receive_with_all_parameter(self):
        parameter = {'device_token': '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76',
                     'uuid': 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'}
        request = self.factory.put('/receive/',
                                   json.dumps(parameter))
        request.content_type = 'application/json'
        response = device_token_receive(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'result': 'success'})

    def test_device_token_receive_with_only_device_token(self):
        parameter = {'device_token': '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76'}
        request = self.factory.put('/receive/',
                                   json.dumps(parameter))
        request.content_type = 'application/json'
        response = device_token_receive(request)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'error': 'Bad Request'})

    def test_device_token_receive_with_only_uuid(self):
        parameter = {'uuid': 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'}
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
