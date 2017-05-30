from django.conf.urls import url
from django.contrib.auth.views import login, logout
from .views import *


urlpatterns = [
    url(r'^receive$', device_token_receive, name='device_token_receive'),
    url(r'^send/(?P<mode>\d+)/(?P<device_token>\w+$)', send_notification_with_device_token,
        name='send_notification_with_device_token'),
    url(r'^cert_upload$', cert_upload, name='cert_upload'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}, name='logout'),
]
