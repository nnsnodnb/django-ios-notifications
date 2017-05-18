from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^receive$', device_token_receive, name='device_token_receive'),
]
