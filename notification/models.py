from django.db import models
from django.contrib.auth.models import User


class DeviceToken(models.Model):
    device_token = models.CharField(blank=False, default='', max_length=255)
    uuid = models.CharField(blank=False, default='', max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, default=None)

