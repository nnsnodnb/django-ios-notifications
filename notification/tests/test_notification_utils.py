from unittest import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..utils import send_notification, upload_certificate, UPLOAD_DIR
from ..models import CertFile

import os


class UtilsSendNotificationTest(TestCase):

    def setUp(self):
        self.cert_model = CertFile(filename='test.pem')
        self.cert_model.save()
        self.device_token_hex = '8a0d7cba3ffad34bd3dcb37728080a95d6ee78a83a68ead033614acbab9b7e76'
        with open(UPLOAD_DIR + '/test.pem', 'w') as f:
            for _ in range(10):
                f.write('test_pem test_pem\n')
            f.close()

    def tearDown(self):
        self.cert_model.delete()
        if os.path.isfile(UPLOAD_DIR + '/test.pem'):
            os.remove(UPLOAD_DIR + '/test.pem')

    def test_use_sandbox_notification(self):
        try:
            # python3
            with self.assertRaises(FileNotFoundError):
                send_notification(message='test case',
                                  device_token=self.device_token_hex,
                                  use_sandbox=True)
        except:
            # python2
            with self.assertRaises(IOError):
                send_notification(message='test case',
                                  device_token=self.device_token_hex,
                                  use_sandbox=True)

    def test_use_sandbox_notification_for_value_error(self):
        with self.assertRaises(CertFile.DoesNotExist):
            send_notification(message='test case',
                              device_token=self.device_token_hex,
                              use_sandbox=False)


class UtilsUploadCertificateTest(TestCase):

    def setUp(self):
        self.cert_file = os.path.dirname(os.path.abspath(__file__)) + '/files/test.pem'
        self.dummy_file = os.path.dirname(os.path.abspath(__file__)) + '/files/dummy.dummy'
        self.cert_model = CertFile(filename='test.pem')
        self.duplicate_test = False
        with open(UPLOAD_DIR + '/test.pem', 'w') as f:
            for _ in range(10):
                f.write('test_pem test_pem\n')
            f.close()

    def tearDown(self):
        if self.duplicate_test:
            CertFile.objects.all().delete()
            self.duplicate_test = False
        if os.path.isfile(UPLOAD_DIR + '/test.pem'):
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
        self.duplicate_test = True
        with open(self.cert_file, 'rb+') as f:
            upload_file = SimpleUploadedFile(f.name, f.read())
            result = upload_certificate(upload_file, target_mode=0)
            self.assertEqual(result, {'error': None})
