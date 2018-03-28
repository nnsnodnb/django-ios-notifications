from django.contrib import admin
from .models import DeviceToken, CertFile


class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_token', 'uuid', 'user')
    list_display_links = ('id', 'device_token', 'uuid', 'user')


admin.site.register(DeviceToken, DeviceTokenAdmin)


class CertFileAdmin(admin.ModelAdmin):
    readonly_fields = ('filename', 'target_mode', 'is_use', 'date')
    list_display = ('id', 'filename', 'target_mode', 'is_use', 'date')
    list_display_links = ('id', 'filename', 'target_mode')


admin.site.register(CertFile, CertFileAdmin)
