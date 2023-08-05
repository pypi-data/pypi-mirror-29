# -*- makefile -*-
# Top-level Makefile for building the notmm toolkit.

SHELL:= /bin/sh
TOPDIR= .
CURDIR= $(TOPDIR)
PREFIX?= /usr/local
OBJDIR= $(TOPDIR)/build
LIBDIR= $(TOPDIR)/lib
DOCDIR= $(TOPDIR)/docs
DISTDIR= $(TOPDIR)/dist
SRCDIR= $(LIBDIR)
#DESTDIR= $(PREFIX)
#LANG=C;

# Debian stuff; Keep this if you're a maintainer and want to
# build a deb archive.
# DEBIANROOT= $(TOPDIR)/debian
#FAKEROOT= $(DEBIANROOT)/$(PACKAGE_NAME)

### Module Options ###
# Documentation building and install
ENABLE_DOCS?="YES" # Set to "NO" to disable building docs

WITH_DOXYGEN?="YES"
WITH_SPHINX?="YES"

WITH_PYPY?="YES"

#HTML documentation will be installed into this dir
DOCPREFIX?=$(PREFIX)/share/doc/notmm

#Sphinx will install HTML files into this dir
DOCROOT?=$(TOPDIR)/docs/build/html
ifndef WITHOUT_DOXYGEN
    DOXYGEN_DESTDIR="${DOCPREFIX}/doxygen"
    DOXYGEN_SRCDIR=$(TOPDIR)/doxygen # XXX: should be ${DOCDIR}/build/doxygen
    DOXYGEN_BUILDDIR=$(DOXYGEN_SRCDIR)
endif

ifdef WITH_PYTHON3
    PYTHON=/usr/bin/python3
else
ifdef WITH_PYPY
    PYTHON=/usr/bin/pypy
else    
    PYTHON=/usr/bin/python
endif  
endif

# Define this to build custom WSGI controllers with
# Cython. (experimental)
# WITH_CYTHON?="YES"
# Define this to build HTML pages for C modules
# WITH_CYTHON_HTMLDOC?="YES"

# WITH_OPTIMIZED_CFLAGS?="YES"

CYTHON?= $(PREFIX)/bin/cython
ENV?= /usr/bin/env
ECHO?= /bin/echo
DOXYGEN?= /usr/bin/doxygen
FIND?= /usr/bin/find
GREP?= grep -E
HG?= hg
INSTALL?= install
MAKE?= make
MD5SUM?= md5sum
MKDIR?= mkdir
PYLINT?= pylint
PYLINTFLAGS?= --init-import=y
RM?= /bin/rm
SUDO?= sudo
TRUE?= true
WHICH?= which
XARGS?= xargs

distfiles=$(ls "$DISTDIR/*.*")

all: build 

build: clean
	$(PYTHON) setup.py build
clean:
#-fakeroot $(MAKE) -f $(DEBIANROOT)/rules clean
	$(RM) -rf $(OBJDIR) MANIFEST $(DOXYGEN_BUILDDIR) *-stamp*
	$(RM) -rf $(DOCDIR)/build
changelog:
	$(HG) log > CHANGES
check:
	$(ECHO) 'Sorry, "make check" is not implemented yet.'
develop:
	$(PYTHON) setup.py develop || $(TRUE)
distclean: clean
	$(FIND) $(TOPDIR) -type f -name "*.py[co]" -exec $(RM) -f '{}' ';' || $(TRUE)
	$(FIND) $(TOPDIR) -type f -name "*.sw[po]" -exec $(RM) -f '{}' ';' || $(TRUE)
	$(FIND) $(TOPDIR) -type f -name "1" -exec $(RM) -f '{}' ';' || $(TRUE)

doxygen: distclean
	$(DOXYGEN) $(TOPDIR)/docs/Doxyfile
help:
	$(PYTHON) setup.py --help
install: build
	$(PYTHON) setup.py install --prefix=$(PREFIX) $(COMPILE)
installdocs: builddocs
##@echo "===> Creating new documentation set..."
##$(MKDIR) ${DOCPREFIX} 
ifdef WITH_SPHINX
	@echo "===> Installing Sphinx-generated HTML documentation..."
	for f in `dir $(DOCROOT)`; do \
	 $(INSTALL) -v -C "$(DOCROOT)/$$f" "${DOCPREFIX}/$$f" || $(TRUE); \
	done; 
	@echo "===> API documentation installed to $(DOCPREFIX)."
endif
builddocs: html
ifndef WITHOUT_DOXYGEN
	@echo "===> Building API documentation (Doxygen)"
	$(MAKE) doxygen && DOCBUILDSTATE=1
endif
#By default HTML documentation should always be rebuilt
installdocs: builddocs
ifeq (DOCBUILDSTATE, 1)
	for f in `dir $(DOXYGEN_SRCDIR)`; do \
	 $(INSTALL) -v -C "$(DOXYGEN_SRCDIR)/$$f" "$(DOXYGEN_DESTDIR)/$$f" || $(TRUE); \
	done;
endif
html:
	$(MAKE) -C ${DOCDIR} -f Makefile html
###administrative commands, for maintainers or
###core developers only (ie: distro package builders) 
manifest:
	$(HG) -q manifest > MANIFEST
md5:
	@for f in "${distfiles}"; do \
		$(MD5SUM) $$f >> CHECKSUMS.txt || $(TRUE);\
	@done;  	
bdist_egg:
	$(PYTHON) setup.py bdist --formats=egg
bdist_zip:
	$(PYTHON) setup.py bdist --formats=zip
bdist_rpm:
	$(PYTHON) setup.py bdist --formats=rpm
bdist_deb: sdist
	dpkg-buildpackage -i -I -rfakeroot || $(TRUE)
sdist: distclean manifest changelog
	$(PYTHON) setup.py sdist $(COMPILE)
test: check
	$(MAKE) -C tests -f Makefile 
lint:
	$(PYLINT) $(PYLINTFLAGS) $(SRCDIR)/notmm 
update:
	$(HG) up -r tip
version:
	$(PYTHON) setup.py --version

