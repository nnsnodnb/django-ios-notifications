============
Introduction
============

A Django plugin for Apple Push Notification Service.
====================================================

Supported python versions
-------------------------

2.7, 3.4, 3.5, 3.6

Supported django versions
-------------------------

1.7 - 1.11

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
