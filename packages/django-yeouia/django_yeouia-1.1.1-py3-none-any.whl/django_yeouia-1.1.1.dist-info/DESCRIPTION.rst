Yummy Email Or Username Insensitive Auth
========================================

model backend for Django
========================

|Build Status| |Coverage Status|

Instructions
------------

-  ``pip install django-yeouia``
-  Add
   ``AUTHENTICATION_BACKENDS = ['yeouia.backends.YummyEmailOrUsernameInsensitiveAuth']``
   to your ``settings.py``
-  Enjoy

Requirements
------------

Tested for

-  Python 2.7, 3.4, 3.5, 3.6
-  Django 1.11, 2.0

May work otherwise, but you should run tests :P

Case Insensitive ?
------------------

Django’s default auth username is *not* case insensitive. (See
`#2273 <https://code.djangoproject.com/ticket/2273>`__ and
`#25617 <https://code.djangoproject.com/ticket/25617>`__)

But… Who cares ?

This backend tries:

1. username, case sensitive
2. username, case insensitive
3. email, case insensitive

And follows `#20760 <https://code.djangoproject.com/ticket/20760>`__.

.. |Build Status| image:: https://travis-ci.org/nim65s/django-YummyEmailOrUsernameInsensitiveAuth.svg?branch=master
   :target: https://travis-ci.org/nim65s/django-YummyEmailOrUsernameInsensitiveAuth
.. |Coverage Status| image:: https://coveralls.io/repos/github/nim65s/django-EmailOrUsernameAuth/badge.svg?branch=master
   :target: https://coveralls.io/github/nim65s/django-EmailOrUsernameAuth?branch=master


