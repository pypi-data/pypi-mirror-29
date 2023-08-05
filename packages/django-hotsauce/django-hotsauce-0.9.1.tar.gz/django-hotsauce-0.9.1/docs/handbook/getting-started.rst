Getting Started
================

:Author: Etienne Robillard <tkadm30@yandex.com>
:Version: 0.8.2

This is some quick notes for getting started, assuming you have read already
the INSTALL file

Example
-------

helloworld
++++++++++

The ``examples/standalone.py`` script is a full example of Django-hotsauce
API ::

    #!/usr/local/bin/python
    # -*- coding: utf-8 -*-
    """
    Self-contained demo script that bootstraps the helloworld
    app and launch a WSGI server on localhost:8000. 

    """

    import sys, os, logging
    
    #Setup logging
    log = logging.getLogger('notmm.controllers.wsgi')

    #Import LazySettings, a proxy over Django settings API
    from notmm.utils.django_settings import LazySettings
    #Configuration stuff
    from notmm.utils.configparse import has_conf, loadconf
    #Basic HTTP server
    from notmm.http import get_bind_addr, HTTPServer
    #Import WSGIController
    from notmm.controllers.wsgi import WSGIController

    #Initialize the settings 
    settings = LazySettings()

    class ConfigurationError(Exception):
        pass

    #Load the configuration from development.ini 
    if has_conf(os.getcwd(), 'development.ini'):
        app_conf = loadconf('development.ini')
        #Get the host/port using get_bind_addr.
        bind_addr = get_bind_addr(app_conf, 'httpserver')
    else:
        raise ConfigurationError('development.ini not found!')

    def main(app_label):
        """Launch a simple WSGI app in stand-alone mode. 
    
        """
        #Setup basic site environment
        sys.path.extend(['lib', 'lib/site-packages'])

        if settings.DEBUG:
            log.debug("Found %d settings!"%settings.count())

        #Setup default controller 
        wsgi_app = WSGIController(settings=settings)
 
        #Init the HTTP server
        WSGIServer = HTTPServer(wsgi_app, bind_addr)
        try:
            log.info("Starting HTTP server on %s:%d" % bind_addr)
            WSGIServer.serve()
        except (SystemExit, KeyboardInterrupt):
            log.info('Shutting down HTTP server...')
            sys.exit(2)

    if __name__ == '__main__':
        # Run the "helloworld" app. (see development.ini)
        main(app_label='helloworld')

Basic configuration
+++++++++++++++++++

First, copy ``extras/djangorc.sample`` to ``/etc/djangorc`` and edit it with 
your favorite text editor. 

For this example, we'll use the ``djangorc`` located in the ``examples`` directory. ::

    
    #!/bin/sh
    # source this file with bash for instant Django
    # usage: source ./djangorc
    # hack hack hack ...

    #Path to a custom Django installation
    DJANGO_HOME=/usr/local/share/django

    #The "app" root directory.
    ROOTDIR=`cd -P -- "$(dirname -- "$0")/" && pwd -P`

    #Location of the application modules. Notice we add $DJANGO_HOME
    #to this variable.
    PYTHONPATH="$ROOTDIR/lib:$ROOTDIR/lib/site-packages:$DJANGO_HOME"
    
    #Specify which settings module to use
    DJANGO_SETTINGS_MODULE=local_settings

    export ROOTDIR PYTHONPATH DJANGO_SETTINGS_MODULE

Next you can take a peek at the ``helloworld`` app located in the ``examples/lib`` directory.
    
helloworld/config/settings.py
+++++++++++++++++++++++++++++

Setup a minimal settings module for your environment. ::

    #Global settings for the helloworld app, to be overrided in local_settings.py.
    from django.conf.global_settings import *
    
    #Location of static files
    from pkg_resources import resource_filename
    MEDIA_ROOT=resource_filename('helloworld', 'static')
    
    #Required by Django
    ROOT_URLCONF='helloworld.config.urls'
    #Required by Django
    MEDIA_URL="http://localhost/media/img/"
    #Required by Django
    TEMPLATE_CONTEXT_PROCESSORS = (
        'helloworld.config.context_processors.request',
    )
    #Required by Django
    SECRET_KEY='12345va1110ht'

    #For debugging, set this to True
    DEBUG=True

    #Disable Django I18N support
    USE_I18N=False

    #Custom error handlers mapping (required)
    CUSTOM_ERROR_HANDLERS = (
        ('handle302', 'helloworld.handlers.handle302'),
        ('handle400', 'helloworld.handlers.handle400'),
        ('handle500', 'helloworld.handlers.handle500')
    )

    #For backward-compatibility with Django.
    #Import templates from the package name.
    TEMPLATE_DIRS = (
        (resource_filename('helloworld', 'templates')),
    )

    # Specify which template loader to use (New)
    TEMPLATE_LOADER = 'notmm.utils.template.backends.CachedTemplateLoader'

    # Logging options
    LOGGING_FORMAT = '[%(levelname)-5s] - [%(asctime)-15s] - [%(name)-5s] - %(message)s' 
    # Where to send application errors 
    LOGGING_ERROR_LOG = '/var/log/django.log'

To start the ``helloworld`` app in standalone mode, run ::

    % source /etc/djangorc
    % python ./standalone.py
    DEBUG:Found 151 settings!
    INFO:Initializing on 2017-07-01 06:54:19 CDT -0500
    INFO:Starting HTTP server on http://localhost:8000/
    INFO:Django-hotsauce 0.7.2 (Open Source Edition)
    INFO:Starting HTTP server on localhost:8000

Alternatively, you can run the following from the examples directory ::

    % source ./djangorc
    % /usr/bin/python2.7 ../tools/httpserver.py -d -c conf/debug.ini --disable-auth --settings=local_settings helloworld
    

See also
--------

* `Development wiki <https://www.isotopesoftware.ca/wiki/DjangoHotSauce>`_
* `Getting Started Tutorial <https://www.isotopesoftware.ca/wiki/DjangoHotSauce/GettingStarted>`_
