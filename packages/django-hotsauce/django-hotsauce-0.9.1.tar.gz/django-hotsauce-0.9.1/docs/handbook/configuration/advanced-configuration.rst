Advanced configuration
======================

:Author: Etienne Robillard <tkadm30@yandex.com>
:Version: 0.8.2

A quite modern WSGI app can selectively load Django settings
using a Python module. This is also maintained for backward-compatibility
with Django. ::


    % source /etc/djangorc
    % export DJANGO_SETTINGS_MODULE=local_settings
    % ... hack hack hack ...
    % bin/debug.sh runserver localhost:8000 

Also, for consistency, new settings should be defined in the development.ini
file instead of trying to reuse original Django settings. This strategy
provides flexible configuration for WSGI applications requiring the use of
additional configuration options at runtime.

Care should also be used for not overlapping Django settings with similar
variables names. Likewise, its generally better to use ``TEMPLATE_DIRS``
than redefining another ``template_dirs`` options.

Development.ini
---------------

setup_all
+++++++++

Here's an example of a simple app (named ``myapp``) configuration using the ``setup_all``
hook ::

    from notmm.utils.configparse import setup_all
    global_conf = {'debug' : True}
    setup_all(__name__, global_conf)

Then, later in a view, you can access the ``global_conf`` dict instance by
using a simple import statement ::

    from myapp import global_conf
    print global_conf
    {'myapp' : {'debug' : True}}

