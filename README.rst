django-ios-notifications
========================

.. image:: https://travis-ci.org/nnsnodnb/django-ios-notifications.svg?branch=master
    :target: https://travis-ci.org/nnsnodnb/django-ios-notifications
.. image:: https://coveralls.io/repos/github/nnsnodnb/django-ios-notifications/badge.svg?branch=master
    :target: https://coveralls.io/github/nnsnodnb/django-ios-notifications?branch=master
.. image:: https://badge.fury.io/py/ios-notification.svg
    :target: https://pypi.python.org/pypi/ios-notification
.. image:: https://img.shields.io/pypi/pyversions/ios-notification.svg
   :target: https://pypi.python.org/pypi/ios-notification
.. image:: https://img.shields.io/pypi/status/ios-notification.svg
   :target: https://pypi.python.org/pypi/ios-notification
.. image:: https://img.shields.io/pypi/wheel/ios-notification.svg
   :target: https://pypi.python.org/pypi/ios-notification
.. image:: https://img.shields.io/pypi/format/ios-notification.svg
   :target: https://pypi.python.org/pypi/ios-notification
.. image:: https://img.shields.io/pypi/implementation/ios-notification.svg
   :target: https://pypi.python.org/pypi/ios-notification
.. image:: https://img.shields.io/pypi/l/ios-notification.svg
   :target: https://pypi.python.org/pypi/ios-notification
.. image:: https://readthedocs.org/projects/ios-notifications/badge/?version=latest
   :target: http://ios-notifications.readthedocs.io/?badge=latest
   :alt: Documentation Status

A Django plugin for Apple Push Notification Service.

Supported python versions
~~~~~~~~~~~~~~~~~~~~~~~~~

2.7, 3.4, 3.5, 3.6

Supported django versions
~~~~~~~~~~~~~~~~~~~~~~~~~

1.7 - 1.11, 2.0 (Only Python3.x or later)

Installation
------------

.. code:: bash

    $ pip install ios-notification

Add ``notification`` into ``INSTALLED_APPS`` in ``settings.py`` file

.. code:: python

    INSTALLED_APPS += (
        'notification',
    )

Add ``notification`` routing in ``urls.py`` file

.. code:: python

    from django.conf.urls import include

    urlpatterns += (
        url(r'^ios/', include('notification.urls', namespace='notification')),
    )

Author
------

nnsnodnb

LICENSE
-------

MIT License
