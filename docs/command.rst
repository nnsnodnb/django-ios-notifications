.. index:: Push Notification commands

=======
Command
=======

.. index:: Single push notification

Single push notification
------------------------
Send a push notification to one device token.

.. index::
    single: Single push notification; Sample command

Sample command
~~~~~~~~~~~~~~

.. code:: bash

    $ cd /path/to/your_django_project/
    $ python manage.py singlepush (--sandbox) \
                                  --token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
                                  --title Notification's\ title \
                                  (--subtitle Notification's\ subtitle) \
                                  (--body Notification's\ body) \
                                  (--sound default) \
                                  (--badge 1) \
                                  (--contentavailable) \
                                  (--mutablecontent) \
                                  (--extra '{"key":"value","key2":"value2"}')

.. index::
    single: Single push notification; About each argument for single push notification

About each argument for single push notification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cssclass:: table-bordered

+--------------------------------+----------------------------------------------------------+-----------+----------+
| Argument name                  | Description                                              | Required  | Default  |
+================================+==========================================================+===========+==========+
| ``--sandbox``, ``-s``          | Use apple sandbox.                                       | NO        | False    |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--token``, ``-t``            | Target device token.                                     | YES       | None     |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--title``                    | Title displayed in push notification.                    | YES       | None     |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--subtitle``                 | Subtitle displayed in push notification.                 | NO        | None     |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--body``                     | Body displayed in push notification.                     | NO        | None     |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--sound``                    | Sounds to be heard when push notification is received.   | NO        | default  |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--badge``                    | Badge displayed on application icon.                     | NO        | 0        |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--contentavailable``, ``-c`` | Use content-available. (Support for iOS7 or higher)      | NO        | False    |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--mutablecontent``, ``-m``   | Use mutable-content. (Support for iOS9 or higher)        | NO        | False    |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--extra``, ``-e``            | Custom notification payload values as a JSON dictionary. | NO        | None     |
+--------------------------------+----------------------------------------------------------+-----------+----------+

.. index:: Multiple push notifications

Multiple push notifications
---------------------------
Send push notifications to some device tokens.

.. index::
    single: Multiple push notifications; Sample command

Sample command
~~~~~~~~~~~~~~

.. code:: bash

    $ cd /path/to/your_django_project/
    $ python manage.py multipush (--sandbox) \
                                 -t XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY \
                                 (--all) \
                                 --title Notification's\ title \
                                 (--subtitle Notification's\ subtitle) \
                                 (--body Notification's\ body) \
                                 (--sound default) \
                                 (--badge 1) \
                                 (--contentavailable) \
                                 (--mutablecontent) \
                                 (--extra '{"key":"value","key2":"value2"}')

.. index::
    single: Multiple push notifications; About each argument for multiple push notifications

About each argument for multiple push notification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cssclass:: table-bordered

+--------------------------------+----------------------------------------------------------+-----------+----------+
| Argument name                  | Description                                              | Required  | Default  |
+================================+==========================================================+===========+==========+
| ``--sandbox``, ``-s``          | Use apple sandbox.                                       | NO        | False    |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--token``, ``-t``            | Target device token.                                     | YES       | None     |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--all``, ``-a``              | Target all device tokens.                                | NO        | False    |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--title``                    | Title displayed in push notification.                    | YES       | None     |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--subtitle``                 | Subtitle displayed in push notification.                 | NO        | None     |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--body``                     | Body displayed in push notification.                     | NO        | None     |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--sound``                    | Sounds to be heard when push notification is received.   | NO        | default  |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--badge``                    | Badge displayed on application icon.                     | NO        | 0        |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--contentavailable``, ``-c`` | Use content-available. (Support for iOS7 or higher)      | NO        | False    |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--mutablecontent``, ``-m``   | Use mutable-content. (Support for iOS9 or higher)        | NO        | False    |
+--------------------------------+----------------------------------------------------------+-----------+----------+
| ``--extra``, ``-e``            | Custom notification payload values as a JSON dictionary. | NO        | None     |
+--------------------------------+----------------------------------------------------------+-----------+----------+
