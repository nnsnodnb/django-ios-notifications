from django.test.client import RequestFactory
from unittest import TestCase
from ..views import device_token_receive

import json


class NotificationViewsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

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
        parameter = {'device_token': '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76',
                     'uuid': 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'}
        request = self.factory.put('/receive/',
                                   json.dumps(parameter))
        request.content_type = 'application/json'
        for _ in range(2):
            response = device_token_receive(request)
        self.assertEqual(response.status_code, 200)

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
