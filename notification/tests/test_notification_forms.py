from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import TestCase
from ..forms import CertFileUploadForm, NotificationSendForm

import os


class CertFileUploadFormTest(TestCase):

    def setUp(self):
        self.cert_file = os.path.dirname(os.path.abspath(__file__)) + '/files/test.pem'

    def tearDown(self):
        self.cert_file = '/'

    def test_is_valid_cert_form(self):
        with open(self.cert_file, 'rb') as f:
            post_parameter = {'target': 0}
            file_parameter = {'cert_file': SimpleUploadedFile(f.name, f.read())}
            form = CertFileUploadForm(post_parameter, file_parameter)
            self.assertTrue(form.is_valid())

    def test_is_invalid(self):
        with open(self.cert_file, 'rb') as f:
            file_parameter = {'cert_file': SimpleUploadedFile(f.name, f.read())}
            form = CertFileUploadForm(files=file_parameter)
            self.assertFalse(form.is_valid())


class NotificationSendFormTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_valid_notification_send_form(self):
        post_parameter = {'target': 0,
                          'title': 'test title',
                          'subtitle': 'test subtitle',
                          'body': 'test body',
                          'sound': 'default',
                          'badge': 1,
                          'content_available': False,
                          'mutable_content': False,
                          'extra': ''}
        form = NotificationSendForm(post_parameter)
        self.assertTrue(form.is_valid())

    def test_is_invalid(self):
        post_parameter = {}
        form = NotificationSendForm(post_parameter)
        self.assertFalse(form.is_valid())
