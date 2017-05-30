import django
from django.conf.urls import *


def _patterns():
    return [
        url(r'^', include('notification.urls', namespace='notification')),
    ]

urlpatterns = _patterns()

