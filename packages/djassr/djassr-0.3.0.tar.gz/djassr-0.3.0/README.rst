========
 Djassr
========

Django rest framework views to get a S3 signed url to PUT or GET to AWS S3

.. note::
  This views doesn't provide any authentication nor permission classes. This means that *ANYONE* can have access to them if your API is public. It's highly recomended to add `authentication_classes` and `permission_classes`.

Example `views.py`

::

   import djassr

   class MyS3PUTSignatureAPIView(djassr.GetPUTSignature):
       authentication_classes = (TokenAuthentication, )
       permission_classes = (IsAuthenticated,)

.. note::
   File names are replaced by a `uuid.uuid4` + the extension. For example "myfile.png" will become "7afad9bc-00d3-46ed-86bf-5ccc52eebd50.png". You can overwrite the `get_object_name` method of the `GetPUTSignature` and `GetPUTPublicSignature`.


.. note::
   The duration of the link is by default 60 seconds. To change this you can set `DJASSR_DEFAULT_EXPIRE` in your `settings.py` or overwrite the `get_expire` method for the signature class. The method must return an integer wich is the time in seconds the link will be valid.

Install
=======
::

   $ pip install djassr


Usage
=====
In `urls.py`

::

   ...
   url('^put_signed_url/$', djassr.views.GetPUTSignature.as_view()),
   ...

Demo
====

You can look at and run the demo project.

::

   pip install -r requirements-dev.txt
   pip install -e ../
   cd demop
   python manage.py migrate
   python manage.py runserver

Go to http://localhost:8000/api/


Running Tests
=============
::

   python runtests.py [tests.<tests_module>[.<TestClass>[.<test_method>]]]
