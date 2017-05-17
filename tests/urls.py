import django
try:
    from django.conf.urls import *
except ImportError:
    from django.conf.urls.defaults import *


def _patterns():
    if django.VERSION >= (1, 9):
        return []
    else:
        return patterns('',)

urlpatterns = _patterns()
