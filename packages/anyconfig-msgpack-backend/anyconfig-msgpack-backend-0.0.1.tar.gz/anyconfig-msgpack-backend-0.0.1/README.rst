==================================
python-anyconfig-msgpack-backend
==================================

.. .. image:: https://img.shields.io/pypi/v/anyconfig-msgpack-backend.svg
   :target: https://pypi.python.org/pypi/anyconfig-msgpack-backend/
   :alt: [Latest Version]

.. image:: https://img.shields.io/travis/ssato/python-anyconfig-msgpack-backend.svg
   :target: https://travis-ci.org/ssato/python-anyconfig-msgpack-backend
   :alt: Test status

.. image:: https://img.shields.io/coveralls/ssato/python-anyconfig-msgpack-backend.svg
   :target: https://coveralls.io/r/ssato/python-anyconfig-msgpack-backend
   :alt: Coverage Status

.. image:: https://landscape.io/github/ssato/python-anyconfig-msgpack-backend/master/landscape.png
   :target: https://landscape.io/github/ssato/python-anyconfig-msgpack-backend/master
   :alt: Code Health

This is a backend module for python-anyconfig to support to load and dump
MessagePack data files.

- Author: Satoru SATOH <ssato@redhat.com>
- License: MIT

SEE ALSO:

- python-anyconfig: https://pypi.python.org/pypi/anyconfig
- MessagePack: http://msgpack.org
- Download:

  - PyPI: https://pypi.python.org/pypi/anyconfig-msgpack-backend
  - Copr RPM repos: https://copr.fedoraproject.org/coprs/ssato/python-anyconfig/

Build & Install
================

If you're Fedora or Red Hat Enterprise Linux user, try::

  $ python setup.py srpm && mock dist/<package>-<ver_dist>.src.rpm
  
or::

  $ python setup.py rpm

and install built RPMs. 

Otherwise, try usual ways to build and/or install python modules such like
'python setup.py bdist', etc.

.. vim:sw=2:ts=2:et:
