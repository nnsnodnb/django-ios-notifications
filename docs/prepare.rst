=======
Prepare
=======

Set up
======

settings.py
~~~~~~~~~~~

Add ``notification`` into ``INSTALLED_APPS`` in ``settings.py`` file

.. code:: python

    INSTALLED_APPS += (
        'notification',
    )

urls.py
~~~~~~~

Add ``notification`` routing in ``urls.py`` file

.. code:: python

    from django.conf.urls import include

    urlpatterns += (
        url(r'^ios/', include('notification.urls', namespace='notification')),
    )

Migration
~~~~~~~~~

.. code:: bash

    $ python manage.py migrate

Prepare application
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ python manage.py createsuperuser
    $ python manage.py runserver

Please access http://127.0.0.1:8000/cert_upload and login **by superuser**, then upload push notification's certificate.

.. warning::


    * PEM file not locked.
    * Secure PEM file which is not double transfer etc.

.. code:: bash

    $ openssl pkcs12 -in hoge.p12 -out hoge.pem -nodes -clcerts
