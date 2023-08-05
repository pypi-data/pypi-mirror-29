===================
djangocms-page-meta
===================

|Gitter| |PyPiVersion| |PyVersion| |Status| |TestCoverage| |CodeClimate| |License|

Meta tag information for django CMS 3 pages

Python: 2.7, 3.4, 3.5. 3.6

Django: 1.8 to 1.11

django CMS: 3.4 (and develop/3.5)

.. warning:: Since version 0.7, the support for Python 2.6, Python 3.3, Django<1.8 and django CMS<3.2
             has been dropped


**********
Quickstart
**********

#. A working django CMS environment is required for djangocms-page-meta to work. Refer to `django CMS documentation`_ for how to install and configure django CMS.

#. Install djangocms-page-meta::

        $ pip install djangocms-page-meta

   or from the repository::

        pip install -e git+https://github.com/nephila/djangocms-page-meta#egg=djangocms-page-meta

#. Then add it to INSTALLED_APPS along with its dependencies::

        'filer',
        'meta',
        'easy_thumbnails',
        'djangocms_page_meta',

#. Synchronize the database with syncdb::

        $ python manage.py syncdb

   or migrate::

        $ python manage.py migrate

#. Configuration:

   See `configuration`_ section in the documentation.

#. That's all!

Dependencies
============

* `django-filer`_ >= 1.2
* `django-meta`_  >= 1.3

*************
Documentation
*************

For package documentation see https://djangocms-page-meta.readthedocs.io/.


.. _django-filer: https://pypi.python.org/pypi/django-filer
.. _django-meta: https://pypi.python.org/pypi/django-meta
.. _configuration: https://djangocms-page-meta.readthedocs.io//en/latest/configuration.html
.. _django CMS documentation: https://django-cms.readthedocs.io/en/latest


.. |Gitter| image:: https://img.shields.io/badge/GITTER-join%20chat-brightgreen.svg?style=flat-square
    :target: https://gitter.im/nephila/applications
    :alt: Join the Gitter chat

.. |PyPiVersion| image:: https://img.shields.io/pypi/v/djangocms-page-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-page-meta
    :alt: Latest PyPI version

.. |PyVersion| image:: https://img.shields.io/pypi/pyversions/djangocms-page-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-page-meta
    :alt: Python versions

.. |Status| image:: https://img.shields.io/travis/nephila/djangocms-page-meta.svg?style=flat-square
    :target: https://travis-ci.org/nephila/djangocms-page-meta
    :alt: Latest Travis CI build status

.. |TestCoverage| image:: https://img.shields.io/coveralls/nephila/djangocms-page-meta/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-page-meta?branch=master
    :alt: Test coverage

.. |License| image:: https://img.shields.io/github/license/nephila/djangocms-page-meta.svg?style=flat-square
   :target: https://pypi.python.org/pypi/djangocms-page-meta/
    :alt: License

.. |CodeClimate| image:: https://codeclimate.com/github/nephila/djangocms-page-meta/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-page-meta
   :alt: Code Climate




*******
History
*******

0.8.1 (2018-02-17)
==================

* Fix duplicate GenericMetaAttribute on publish
* Fix error on Divio cloud when description fields length is not set

0.8.0 (2018-01-14)
==================

* Add Django 1.11 support
* Add django CMS 3.5 support
* Drop django CMS 3.2, 3.3
* Add support for filer canonical URL
* Do not fail if request is not in context
* Make HTML and twitter description fields length configurable

0.7.0 (2016-12-04)
==================

* Drop Django 1.7 and below
* Drop django CMS 3.1 and below
* Add Django 1.10 support

0.6.3 (2016-10-22)
==================

* Added support for django CMS 3.4

0.6.2 (2016-08-01)
==================

* Conditionally show page description field if not empty

0.6.1 (2016-06-20)
==================

* Drop unique index on generic meta attributes

0.6 (2016-06-05)
================

* Let settings be used as defaults
* Added support for fb_pages attribute
* Added support for generic meta attributes

0.5.11 (2016-03-17)
===================

* Make object type not required

0.5.10 (2016-03-03)
===================

* Fix handling Google+ author URL

0.5.9 (2016-02-25)
==================

* Fix issue with Django 1.9

0.5.8 (2016-02-23)
==================

* Improve Aldryn support
* Catch AttributeError in get_page_meta

0.5.7 (2016-01-09)
==================

* Fix handling of pages in non existing languages
* Add support for Aldryn environment

0.5.6 (2015-10-03)
==================

* Fix error when retrieing tags from djangocms-page-tags
* Add support for django CMS 3.2
* Add support for Django 1.8

0.5.5 (2015-08-21)
==================

* Different approach at fix error when page is None
* Better fallback mechanism
* Update i18n

0.5.4 (2015-08-08)
==================

* Fix error when page is None
* Code cleanup
* Add pep8/isort to tests
* Add missing migration

0.5.3 (2015-06-29)
==================

* Fix Django 1.7 migration
* Update testing configuration

0.5.2 (2015-06-28)
==================

* Compatibility with django CMS 3.1.1

0.5.1 (2015-06-06)
==================

* Make south migrations indipendent from djangocms-helper

0.5 (2015-06-06)
================

* Add support for custom user model
* Fix the length of SEO fields
* Use djangocms-helper for tests
* Add support for Django 1.7
* Add support for django CMS 3.1

0.4.1 (2014-08-10)
==================

* Minor fixes

0.4.0 (2014-04-19)
==================

* django CMS 3 final release support
* Moved some code to external django-meta-mixin application

0.3.3 (2014-03-23)
==================

* Better support for sn-dependent descriptions

0.3.2 (2014-03-07)
==================

* Add different descriptions for each supported social network

0.3.1 (2014-02-13)
==================

* Fix permission name

0.3.0 (2014-02-02)
==================

* Fix for django CMS 3 develop update

0.2.1 (2014-01-26)
==================

* Vendorizing django-meta compatibility templatetags

0.2.0 (2014-01-22)
==================

* Put toolbar menu items in a submenu

0.1.0 (2014-01-21)
==================

* Experimental release.


