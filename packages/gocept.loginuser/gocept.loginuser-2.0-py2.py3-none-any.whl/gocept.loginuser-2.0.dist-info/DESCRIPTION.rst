=================================
The gocept.loginuser distribution
=================================

Sqlalchemy user object and password management.

This package is compatible with Python version 2.7.


===========================
Developing gocept.loginuser
===========================

:Author:
    `gocept <http://gocept.com/>`_ <mail@gocept.com>

:PyPI page:
    https://pypi.python.org/pypi/gocept.loginuser

:Issues:
    `report by e-mail <mail@gocept.com>`_

:Source code:
    https://bitbucket.org/gocept/gocept.loginuser

:Current change log:
    https://bitbucket.org/gocept/gocept.loginuser/raw/tip/CHANGES.txt


===============================
Change log for gocept.loginuser
===============================

2.0 (2018-02-16)
================

- Passwords are now saved in LDAP style: ``{SHA256}adkjiois34jhdi``.

  Attention: If the hash does not start with name of an encryption scheme,
  plaintext password is assumed instead of bcrypt, which was assumed in 1.x.

  Migration:

  - Passwords, that start with ``SHA256:``: Replace the prefix with
    ``{SHA256}``.
  - Passwords without prefix: Add ``{BCRYPT}`` as prefix.

- Drop support for Python 2.6 and 3.3.

- Add support for Python 3.6.


1.3 (2017-04-25)
================

- Fix setup.py


1.2 (2015-09-24)
================

- Add support for Python 3.3 up to 3.5.


1.1 (2015-02-09)
================

- Allow for the password hash to specify the hashing algorithm inline (made
  sha256 available so far).


1.0.1 (2015-01-07)
==================

- Fixed brown-bag release.


1.0 (2015-01-07)
================

initial release


