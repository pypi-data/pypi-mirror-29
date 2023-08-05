BaseController API
===================

:Author: Etienne Robillard <tkadm30@yandex.com>
:Version: 0.8.2

Introduction
-------------

The ``notmm.controllers`` package provides a high-performance API for Django apps
to extend from the ``BaseController`` class.

Modules
--------

``BaseController``
~~~~~~~~~~~~~~~~~~~

The ``notmm.controllers.base.BaseController`` module requires the ``Cython`` and ``Werkzeug`` libraries to operate properly. It's purpose is to provide an abstract base class 
and a set of common methods to derived subclasses.


``WSGIController``
~~~~~~~~~~~~~~~~~~~

The ``notmm.controllers.wsgi.WSGIController`` class provides the core wrapper for Django apps to extend from. It is essentially a thin but valid WSGI middleware to sit between Django and the webserver. Django 1.11 or higher is recommended for optimal results. 

In addition, the ``WSGIController`` supports many exclusive features
such as:

- Thread-local request/response handling based on Werkzeug and Gevent
- Customized Django exception handling
- Django settings autoloading via Proxy-style attribute delegation
- Allow developers to embed Django applications using a shared library..
- Makes the Pylons developers to build pyramids instead of pylons.. :)

Exception Handling
-------------------

.. The following is out-of-date...

To register a custom WSGI response handler ::

    from notmm.controllers.wsgi import WSGIController
    
    wsgi_app = WSGIController()
    wsgi_app.sethandle('handle401', 'myapp.views.handle401')
    wsgi_app.sethandle('handle404', 'myapp.views.handle404')
    wsgi_app.sethandle('handle500', 'myapp.views.handle500') 

Notes
------

* The name `BaseController' is inspired from the Pylons (Pyramid) framework.

See Also
---------

The ``session`` and ``authentication`` chapters.

