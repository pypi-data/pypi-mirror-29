.. image:: https://travis-ci.org/bartTC/django-generic-flatblocks.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-generic-flatblocks

.. image:: https://codecov.io/github/bartTC/django-generic-flatblocks/coverage.svg?branch=master
    :target: https://codecov.io/github/bartTC/django-generic-flatblocks?branch=master

=========================
django-generic-flatblocks
=========================

If you want to add tiny snippets of text to your site, manageable by the admin
backend, you would use either `django-chunks`_ or `django-flatblocks`_.
However, both of them have one problem: you are limited to a predefined
content field; a "text" field in chunks and a "title" and "text" field in
flatblocks.

django-generic-flatblocks solves this problem as it knows nothing about the
content itself. You *attach* your hand made content node (a simple model) where
you can define any fields you want.

.. _`django-flatblocks`: http://github.com/zerok/django-flatblocks/tree/master
.. _`django-chunks`: http://code.google.com/p/django-chunks/

Documentation
=============

Documenation is available online under:

    http://readthedocs.org/docs/django-generic-flatblocks/en/latest/


Changelog
=========

v1.2 (2018-02-18):
------------------

- Django 2.0 compatibility and tests.

v1.1.1 (2017-04-30):
--------------------

- Django 1.11 compatibility and tests.

v1.1 (2017-03-18):
------------------

- Django 1.10 compatibility and tests.
- Python 3.6 compatibility.
- `TEMPLATE_DEBUG` setting is no longer honored to raise individual
  errors, in favor of standard `DEBUG`.

v1.0 (2016-03-23):
------------------

- Code cleanup and update for Django 1.8+. Python3 Support. Better
  test integration. Better docs.

v0.9.1 (2010-03-22):
--------------------

- Django 1.2 compatibility! Fixed a bug where tests did not pass
  under Django 1.2. Thanks to Brian Rosner for this.

v0.9 (2010-02-25):
------------------

- Fixed a bug where an integer was not allowed as a part of a slug.

v0.4 (2009-09-08):
------------------

- Added Danish translation.
- Added better documentation.
- Added unittests.
- If you fetch a not existing "primary key" object the templatetag
  will fail silently if settings.TEMPLATE_DEBUG is False.

v0.3.0 (2009-03-21):
--------------------

- Added the *into* argument. You can now display any instance directly
  without creating and rendering a template.

v0.2.1 (2009-03-20):
--------------------

- You can now pass a context variable with a integer to fetch a specific
  object.

v0.2.0 (2009-03-20):
--------------------

- Added the ability to pass an integer as slug. This will cause that the
  templatetag fetches the specific *for* model with the primary key named
  in *slug*.

v0.1.2 (2009-03-20):
--------------------

- Switched from distutils to setuptools. Fixed whitespace.

v0.1.1 (2009-03-15):
--------------------

- Fixed wrong upload path of a contributed, generic block

v0.1 (2009-03-13):
------------------

- Initial release


