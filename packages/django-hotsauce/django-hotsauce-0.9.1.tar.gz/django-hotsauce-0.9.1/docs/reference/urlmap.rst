Mapping routes
===============

:Author: Etienne Robillard <tkadm30@yandex.com>
:Version: 0.8.2

What is it
-----------

A replacement for the ``django.core.urlresolvers`` package. The replacement
should be backward-compatible with Django.

How does it work
-----------------

The class ``notmm.utils.urlmap.RegexURLMap`` provides a simple wrapper to group
distinct urls to logical groups using the ``add_routes`` method. This method can 
be called a number of times to provide a elegant yet robust way to separate urls in
distinct categories. ::


    from notmm.utils.urlmap import RegexURLMap, url
    urlpatterns = RegexURLMap()
    urlpatterns.add_routes('myapp.facebook', 
        url(r'^register.php$', 'example_exploit', {}),
        )
    urlpatterns.add_routes('google_appengine.make_poo',
        url(r'^index.php$', 'poo_callback', {}),
        )

It should also be noted that you can also call ``urlpatterns.include(someobj)`` to
include another urls module. ::

    from notmm.utils.urlmap import RegexURLMap

    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = RegexURLMap(label="django admin")
    urlpatterns.include(admin.site.urls)
    
Upgrading
----------

To upgrade from standard Django urlpatterns to ``notmm.utils.urlmap.RegexURLMap``, change the line ::

    from django.conf.urls.defaults import * 

to ::

    from notmm.utils.urlmap import RegexURLMap, url
    
Then you should define a default ``urlpatterns`` instance or 
upgrade the previous one to the ``RegexURLMap`` API. You can also 
at this point add new endpoints (packages) using the ``add_routes`` method.

TODO
----------

- More tests is needed for interoperability with Django 1.3, 1.4
- Allow urlmap.URLMap to fetch urlpatterns objects from a backend db.
- Integration with webdav, to allow saving and deletion of urlpatterns 
- Make a separate ``urlmap`` package for easier access to the programming
  interfaces.


