======
Routes
======

* :ref:`receive`
* :ref:`send`
* :ref:`cert_upload`
* :ref:`login`
* :ref:`logout`

Detail
======

.. _receive:

------------
``/receive``
------------

Send device token http://127.0.0.1:8000/receive with UUID.

Request parameters
------------------

.. cssclass:: table-bordered

+--------------+--------+----------+------------+
| Name         | Type   | Required | Note       |
+==============+========+==========+============+
| device_token | String | YES      | 64 letters |
+--------------+--------+----------+------------+
| uuid         | String | YES      | 36 letters |
+--------------+--------+----------+------------+

* Request method: ``PUT``
* Content-Type: ``application/json``
* Model: ``notification.models.DeviceToken``
* Success response: ``{"result": "success"}``
* Failure response: ``{"error": "Bad Request"}``

``notification.models.DeviceToken`` has ``user`` field so you can also associate users by applying ``django.contrib.auth.models.User``.

Sample Request
--------------

.. code:: bash

    $ curl -X PUT http://127.0.0.1:8000/receive \
      -d '{"device_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"}'

.. _send:

---------
``/send``
---------

It is possible to send a push notification easily.

Real route is ``/send/<TARGET_MODE>/<DEVICE_TOKEN>``.

TARGET_MODE
-----------

* Development: ``0``
* Distribution: ``1``

DEVICE_TOKEN
------------

* Device token registered DATABSE.

Request parameter
-----------------

+--------------+--------+----------+-------------+
| Name         | Type   | Required | Note        |
+==============+========+==========+=============+
| message      | String | NO       | URL encoded |
+--------------+--------+----------+-------------+

* Request method: ``GET``

Sample Request
--------------

Use sandbox
^^^^^^^^^^^

.. code::

    http://127.0.0.1:8000/send/0/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX?message=test%20push%20notification

NOT use sandbox
^^^^^^^^^^^^^^^

.. code::

    http://127.0.0.1:8000/send/1/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

.. _cert_upload:

``/cert_upload``
----------------

Upload push notifications' certificates by superuser.

.. note::

    * PEM file not locked.
    * Secure PEM file which is not double transfer etc.

.. _login:

``/login``
----------

Login to session.

.. _logout:

``/logout``
-----------

Logout from session.
