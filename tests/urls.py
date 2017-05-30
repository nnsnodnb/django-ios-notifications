import django
try:
    from django.conf.urls import *
except ImportError:
    from django.conf.urls.defaults import *


def _patterns():
    if django.VERSION >= (1, 9):
        return [
            url(r'^', include('notification.urls', namespace='notification')),
        ]
    else:
        return patterns('',
                        url(r'^', include('notification.urls', namespace='notification')),)

urlpatterns = _patterns()

