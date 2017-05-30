from unittest import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..utils import send_notification, upload_certificate, UPLOAD_DIR
from ..models import CertFile

import os


class UtilsSendNotificationTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_use_sandbox_notification(self):
        pass


class UtilsUploadCertificateTest(TestCase):

    def setUp(self):
        self.cert_file = os.path.dirname(os.path.abspath(__file__)) + '/files/test.pem'
        self.dummy_file = os.path.dirname(os.path.abspath(__file__)) + '/files/dummy.dummy'
        self.cert_model = CertFile(filename='test.pem')
        self.duplicate_test = False

    def tearDown(self):
        if self.duplicate_test:
            CertFile.objects.all().delete()
            self.duplicate_test = False
        if not os.path.isfile(UPLOAD_DIR + '/test.pem'):
            return
        os.remove(UPLOAD_DIR + '/test.pem')

    def test_upload_certificate_for_success(self):
        with open(self.cert_file, 'rb+') as f:
            upload_file = SimpleUploadedFile(f.name, f.read())
            result = upload_certificate(upload_file, target_mode=0)
            self.assertEqual(result, {'error': None})

    def test_upload_certificate_for_wrong_name(self):
        with open(self.dummy_file, 'rb+') as f:
            result = upload_certificate(f, target_mode=0)
            self.assertEqual(result, {'error': 'wrong'})

    def test_upload_certificate_for_success_with_duplication_file_name(self):
        self.cert_model.save()
        self.duplicate_test = True
        with open(self.cert_file, 'rb+') as f:
            upload_file = SimpleUploadedFile(f.name, f.read())
            result = upload_certificate(upload_file, target_mode=0)
            self.assertEqual(result, {'error': None})
