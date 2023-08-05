=======
Install
=======


:Author: Etienne Robillard <tkadm30@yandex.com>
:Version: 0.8.2

The django-hotsauce library can be installed normally using the ``setuptools``
extension.

You can also verify if ``setuptools`` is installed and working properly 
using the following one-liner: ::

    % python -c 'import setuptools'

To install non-interactively third-party python bindings required to properly
build django-hotsauce, use the ``bootstrap`` script and the name of the Python
interpreter to use for the whole install process. 

For example, to develop a WSGI application with Python 2.7, one could do: ::

    % ./bootstrap python2.7

To complete the install using ``llvm-gcc`` as the host compiler: ::

    % export CC=llvm-gcc
    % export LD=llvm-ld
    % sudo make 

(Note that you should use GNU make and not /usr/bin/make if you're
using a *BSD system. On Linux, gmake should be aliased as /usr/bin/make.)

The old way: ::

    % python setup.py build 
    % python setup.py install --prefix=/usr/local

To develop locally, you can use the "develop" command provided by
setuptools to install a symlink to the source directory: ::

    % sudo make develop

Note: This is the recommended method to install django-hotsauce.

To build the documentation, Sphinx and Doxygen are needed. Sphinx
is used to build the standard documentation and Doxygen for the API
documentation: ::

    % sudo make doxygen          # generate the API docs
    % make -f docs/Makefile html # generate the HTML docs (work-in-progress)

