from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class DeviceToken(models.Model):
    device_token = models.CharField(blank=False, default='', max_length=255)
    uuid = models.CharField(blank=False, default='', max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, default=None)


class CertFile(models.Model):
    filename = models.CharField(blank=False, default='cert.pem', max_length=100)
    target_mode = models.IntegerField(blank=False, default=0)
    is_use = models.BooleanField(blank=False, default=True)
    date = models.DateTimeField(blank=False, default=now)
