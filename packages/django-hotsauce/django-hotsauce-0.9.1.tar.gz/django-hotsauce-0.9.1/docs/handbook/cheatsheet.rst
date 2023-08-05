Tips and Tricks
================

:Author: Etienne Robillard <tkadm30@yandex.com>
:Version: 0.8.2

The following list proposes simple tips and tricks for 
working with the django-hotsauce toolkit. Most of them can be used
in standard Django apps with moderate efforts to boost your 
productivity while making kick-ass websites.

SQLAlchemy integration
-----------------------

Here's a simple recipe which uses ``SQLAlchemy`` and
the ``with_session`` decorator to make a custom SQL 
query in a standard Django view. ::

    from notmm.utils.template import direct_to_template
    from notmm.dbapi.backends.sql import with_session
    
    from myapp.config import database as db

    @with_session(engine=db.engine)     
    def index(request):
        # get the ScopedSession instance
        Session = request.environ.get('_scoped_session')
        # now do something with the Session 
        data = {
          'user' : Session.query('User').filter_by(...).first()
          }
        # close the session  
        Session.close()

        return direct_to_template(request, extra_context=data)

Lazier Django Settings
-----------------------

Here is an example using thread-local as a way to 
store custom data ::

    from notmm.utils.django_settings import LazySettings

    # then simply initialize the LazySettings object
    # for getting a Django-like settings module.
    settings = LazySettings()
    # load settings from this module
    settings.loads('myapp.settings')
    settings.clear()  # remove all settings and set initialized=False
    settings.count()  # return a int

