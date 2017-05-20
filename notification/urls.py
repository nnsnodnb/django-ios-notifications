from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^receive$', device_token_receive, name='device_token_receive'),
    url(r'^send/(?P<mode>\d+)/(?P<device_token>\w+$)', send_notification_with_device_token,
        name='send_notification_with_device_token'),
]
