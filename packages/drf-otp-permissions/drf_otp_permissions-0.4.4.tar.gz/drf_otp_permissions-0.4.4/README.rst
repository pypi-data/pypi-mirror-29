Django REST Framework OTP Permissions
=====================================

Add one time password permission to your Django REST Framework API.

Install
-------

Use :code:`pip` to install.

    $ pip install drf_otp_permissions

Usage
-----

Use :code:`IsValidOneTimePassword` as one of your :code:`permission_classes`.
Provide your key file path in :code:`get_otp_key_location`.

.. code-block:: python

    from drf_otp_permissions.permissions import IsValidOneTimePassword

    class MyAPIView(DjangoRESTAPIView):
        get_otp_key_location = 'path/to/your/key'
        permission_classes = (IsValidOneTimePassword,)