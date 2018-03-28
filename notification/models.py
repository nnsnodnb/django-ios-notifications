from django.conf import settings
from django.db import models
from django.utils.timezone import now


class DeviceToken(models.Model):
    device_token = models.CharField(blank=False, default='', max_length=255)
    uuid = models.CharField(blank=False, default='', max_length=255)
    use_sandbox = models.BooleanField(blank=False, default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Device Tokens'
        verbose_name_plural = 'Device Token'

    def __str__(self):
        return self.device_token


class CertFile(models.Model):
    filename = models.CharField(blank=False, default='cert.pem', max_length=100)
    target_mode = models.IntegerField(blank=False, default=0)
    is_use = models.BooleanField(blank=False, default=True)
    date = models.DateTimeField(blank=False, default=now)

    class Meta:
        verbose_name = 'Certificate files'
        verbose_name_plural = 'Certificate file'

    def __str__(self):
        return self.filename
