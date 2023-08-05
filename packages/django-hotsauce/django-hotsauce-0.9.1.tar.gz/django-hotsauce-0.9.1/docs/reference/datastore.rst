========================
Thread-Local Storage API 
========================

:Author: Etienne Robillard <tkadm30@yandex.com>
:Version: 0.8.2

The ``notmm.datastore.threadlocal`` module provides a simple
thread-local storage backend based on ``gevent``. 

Example
-------

To store and retrieve Django settings with ``gevent``, you can do the following ::

    >>> from notmm.datastore.threadlocal import ThreadLocalStore
    >>> store = ThreadLocalStore('local_settings')
    >>> store.loads()

Then you can lookup any settings using the ``store`` object ::

    >>> store.DEBUG
    True

