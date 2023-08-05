Deployment
==========

:Author: Etienne Robillard <tkadm30@yandex.com>
:Version: 0.8.2

This document should gives you a brief overview of how to deploy django-hotsauce for production mode using the ``nginx`` webserver. Currently, you can deploy django-hotsauce using either FastCGI or uWSGI backends. 

FastCGI
-------

FastCGI is the legacy backend used for deploying django-hotsauce with nginx. There's multiple Python libraries available to deploy a WSGI app with FastCGI, however we recommend using the ``gevent-fastcgi`` library.

Example script
++++++++++++++

Here's a template you can use to bootstrap your wsgi application with ``gevent-fastcgi`` ::

    #!/usr/bin/env python
    from notmm.controllers.wsgi import WSGIController
    from gevent_fastcgi.server import FastCGIServer
    from gevent_fastcgi.wsgi import WSGIRequestHandler

    handler = WSGIRequestHandler(WSGIController())
    s = FastCGIServer(('127.0.0.1', 8808), handler)
    s.serve_forever()

Then simply save this as ``dispatch.fcgi`` and run the script from the command line to initialize the fastcgi backend ::

    $ python dispatch.fcgi &

Nginx configuration
+++++++++++++++++++

Edit your nginx.conf file and add the following ::

    server {
        ...
        location / {
          # host and port to fastcgi server
    	  fastcgi_pass 127.0.0.1:8000;
	      include fastcgi_params;
        }
     }   


uWSGI
-----

uWSGI is a modern and high-performance web application backend which works very well with nginx. It supports ``gevent`` and the WSGI protocol natively. 

Example script
++++++++++++++

Here's a template you can use to bootstrap django-hotsauce with uWSGI. ::

    #!/usr/bin/env python
    from notmm.controllers.wsgi import WSGIController

    def application(environ, start_response):

        wsgi_app = WSGIController()
        return wsgi_app(environ, start_response)

Nginx configuration
+++++++++++++++++++

Edit your nginx.conf file and add the following ::

    server {
        ...

        location / {
            uwsgi_pass 127.0.0.1:8000; 
            include uwsgi_params;
        }
    }

