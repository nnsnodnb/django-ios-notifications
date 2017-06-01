from django.contrib.auth.models import User, AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from django.test import Client
from django.test.client import RequestFactory
from unittest import TestCase
from ..models import DeviceToken
from ..views import device_token_receive, send_notification_with_device_token, cert_upload

import json
import os


class NotificationViewDeviceTokenReceiveTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.device_token = '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76'
        self.uuid = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'

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
        factory = RequestFactory()
        self.request = factory.get('/send/')
        self.device_token_hex = '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76'
        self.wrong_token = '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e79'
        self.uuid = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
        self.cert_file_path = os.path.dirname(os.path.abspath(__file__)) + '/cert.pem'
        self.super_user = User.objects.create_superuser(username='super_user',
                                                        password='test_case_for_super_user',
                                                        email='super_user@localhost')
        self.super_user.save()
        self.general_user = User.objects.create_user(username='general_user',
                                                     password='test_case_for_general_user')
        self.general_user.save()

        self.device_token = DeviceToken(device_token=self.device_token_hex,
                                        uuid=self.uuid)
        self.device_token.save()

    def tearDown(self):
        self.super_user.delete()
        self.general_user.delete()
        DeviceToken.objects.all().delete()

    def test_target_develop_wrong_device_token_is_anonymous(self):
        """
        Target: Develop
        Device token is wrong.
        Message is not here.
        Request by anonymous.
        """
        self.request.user = AnonymousUser()
        response = send_notification_with_device_token(self.request,
                                                       mode=0,
                                                       device_token=self.wrong_token,
                                                       execute=False)
        self.assertEqual(response.status_code, 401)

    def test_target_develop_wrong_device_token_is_super_user(self):
        """
        Target: Development
        Device token is wrong.
        Message is not here.
        Request by super user.
        """
        self.request.user = self.super_user
        response = send_notification_with_device_token(self.request,
                                                       mode=0,
                                                       device_token=self.wrong_token,
                                                       execute=False)
        self.assertEqual(response.status_code, 404)

    def test_target_develop_wrong_device_token_is_general_user(self):
        """
        Target: Develop
        Device token is wrong.
        Message is not here.
        Request by general user.
        """
        self.request.user = self.general_user
        response = send_notification_with_device_token(self.request,
                                                       mode=0,
                                                       device_token=self.wrong_token,
                                                       execute=False)
        self.assertEqual(response.status_code, 401)

    def test_target_develop_match_device_token_is_anonymous(self):
        """
        Target: Develop
        Device token is match.
        Message is not here.
        Request by anonymous. 
        """
        self.request.user = AnonymousUser()
        response = send_notification_with_device_token(self.request,
                                                       mode=0,
                                                       device_token=self.wrong_token,
                                                       execute=False)
        self.assertEqual(response.status_code, 401)

    def test_target_develop_match_device_token_is_super_user(self):
        """
        Target: Develop
        Device token is match.
        Message is not here.
        Request by super user.
        """
        self.request.user = self.super_user
        response = send_notification_with_device_token(self.request,
                                                       mode=0,
                                                       device_token=self.device_token_hex.encode(),
                                                       execute=False)
        self.assertEqual(response.status_code, 200)

    def test_target_develop_match_device_token_is_general_user(self):
        """
        Target: Develop
        Device token is match.
        Message is not here.
        Request by general user.
        """
        self.request.user = self.general_user
        response = send_notification_with_device_token(self.request,
                                                       mode=0,
                                                       device_token=self.device_token_hex.encode(),
                                                       execute=False)
        self.assertEqual(response.status_code, 401)

    def test_target_distribute_wrong_device_token_is_anonymous(self):
        """
        Target: Distribute
        Device token is wrong.
        Message is not here.
        Request by anonymous.
        """
        self.request.user = AnonymousUser()
        response = send_notification_with_device_token(self.request,
                                                       mode=1,
                                                       device_token=self.wrong_token,
                                                       execute=False)
        self.assertEqual(response.status_code, 401)

    def test_target_distribute_wrong_device_token_is_super_user(self):
        """
        Target: Distribute
        Device token is wrong.
        Message is not here.
        Request by super user.
        """
        self.request.user = self.super_user
        response = send_notification_with_device_token(self.request,
                                                       mode=1,
                                                       device_token=self.wrong_token,
                                                       execute=False)
        self.assertEqual(response.status_code, 404)

    def test_target_distribute_wrong_device_token_is_general_user(self):
        """
        Target: Distribute
        Device token is wrong.
        Message is not here.
        Request by general user.
        """
        self.request.user = self.general_user
        response = send_notification_with_device_token(self.request,
                                                       mode=1,
                                                       device_token=self.wrong_token,
                                                       execute=False)
        self.assertEqual(response.status_code, 401)

    def test_target_distribute_match_device_token_is_anonymous(self):
        """
        Target: Distribute
        Device token is match.
        Message is not here.
        Request by anonymous. 
        """
        self.request.user = AnonymousUser()
        response = send_notification_with_device_token(self.request,
                                                       mode=1,
                                                       device_token=self.wrong_token,
                                                       execute=False)
        self.assertEqual(response.status_code, 401)

    def test_target_distribute_match_device_token_is_super_user(self):
        """
        Target: Distribute
        Device token is match.
        Message is not here.
        Request by super user.
        """
        self.request.user = self.super_user
        response = send_notification_with_device_token(self.request,
                                                       mode=1,
                                                       device_token=self.device_token_hex.encode(),
                                                       execute=False)
        self.assertEqual(response.status_code, 200)

    def test_target_distribute_match_device_token_is_general_user(self):
        """
        Target: Distribute
        Device token is match.
        Message is not here.
        Request by general user.
        """
        self.request.user = self.general_user
        response = send_notification_with_device_token(self.request,
                                                       mode=1,
                                                       device_token=self.device_token_hex.encode(),
                                                       execute=False)
        self.assertEqual(response.status_code, 401)

    def test_target_wrong_is_super_user(self):
        """
        Target: Wrong
        """
        self.request.user = self.super_user
        response = send_notification_with_device_token(self.request,
                                                       mode=2,
                                                       device_token=self.device_token_hex.encode(),
                                                       execute=False)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'check your mode number(0 or 1).')

    def test_target_develop_match_device_token_is_super_user_is_message(self):
        """
        Target: Develop
        Device token is match.
        Message is here.
        Request by super user.
        """
        request = HttpRequest()
        request.user = self.super_user
        request.GET['message'] = 'test case'

        response = send_notification_with_device_token(request, 0, self.device_token_hex, execute=False)
        self.assertEqual(response.status_code, 200)

    def test_execute_send_notification_is_super_user(self):
        self.request.user = self.super_user
        response = send_notification_with_device_token(self.request,
                                                       mode=0,
                                                       device_token=self.device_token_hex.encode(),
                                                       execute=True)
        self.assertEqual(response.status_code, 404)


class CertUploadTest(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client_csrf = Client()
        self.super_user = User.objects.create_superuser(username='super_user',
                                                        password='test_case_for_super_user',
                                                        email='super_user@localhost')
        self.super_user.save()
        self.general_user = User.objects.create_user(username='general_user',
                                                     password='test_case_for_general_user')
        self.general_user.save()
        self.cert_file = os.path.dirname(os.path.abspath(__file__)) + '/files/test.pem'

    def tearDown(self):
        self.client = None
        self.client_csrf = None
        self.super_user.delete()
        self.general_user.delete()
        if not os.path.isfile(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/files/test.pem'):
            return
        os.remove(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/files/test.pem')

    def test_method_get_by_super_user(self):
        self.client.login(username=self.super_user.username, password='test_case_for_super_user')
        response = self.client.get('/cert_upload')
        self.assertEqual(response.status_code, 200)

    def test_method_get_by_general_user(self):
        self.client.login(username=self.general_user.username, password='test_case_for_general_user')
        response = self.client.get('/cert_upload')
        self.assertEqual(response.status_code, 302)

    def test_method_post_without_csrf_by_super_user(self):
        self.client.login(username=self.super_user.username, password='test_case_for_super_user')
        response = self.client.post('/cert_upload')
        self.assertEqual(response.status_code, 403)

    def test_method_post_without_csrf_by_general_user(self):
        self.client.login(username=self.general_user.username, password='test_case_for_general_user')
        response = self.client.post('/cert_upload')
        self.assertEqual(response.status_code, 403)

    def test_method_post_with_csrf_by_super_user(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.super_user
        request.content_type = 'multipart/form-data'
        request.POST['target'] = 0
        with open(self.cert_file, 'rb') as f:
            request.FILES['cert_file'] = SimpleUploadedFile(f.name, f.read())

        response = cert_upload(request)
        self.assertEqual(response.status_code, 200)

    def test_method_post_with_csrf_by_general_user(self):
        self.client_csrf.login(username=self.general_user.username, password='test_case_for_general_user')
        response = self.client_csrf.post('/cert_upload')
        self.assertEqual(response.status_code, 302)

    def test_method_post_with_csrf_by_super_user_parameter_invalid(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.super_user
        request.content_type = 'multipart/form-data'
        request.POST['target'] = 0

        response = cert_upload(request)
        self.assertEqual(response.status_code, 400)
