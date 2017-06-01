from django.contrib import admin
from .models import DeviceToken, CertFile


class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_token', 'uuid', 'user')
    list_display_links = ('id', 'device_token', 'uuid', 'user')

admin.site.register(DeviceToken, DeviceTokenAdmin)
