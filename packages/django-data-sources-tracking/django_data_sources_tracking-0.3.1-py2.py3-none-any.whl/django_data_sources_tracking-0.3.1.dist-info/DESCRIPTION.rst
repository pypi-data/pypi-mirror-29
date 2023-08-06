=============================
Django Data Tracking
=============================

.. image:: https://badge.fury.io/py/django-data-sources-tracking.svg
    :target: https://badge.fury.io/py/django-data-sources-tracking

.. image:: https://travis-ci.org/chopdgd/django-data-sources-tracking.svg?branch=develop
    :target: https://travis-ci.org/chopdgd/django-data-sources-tracking

.. image:: https://codecov.io/gh/chopdgd/django-data-sources-tracking/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/chopdgd/django-data-sources-tracking

.. image:: https://pyup.io/repos/github/chopdgd/django-data-sources-tracking/shield.svg
    :target: https://pyup.io/repos/github/chopdgd/django-data-sources-tracking/
    :alt: Updates

.. image:: https://pyup.io/repos/github/chopdgd/django-data-sources-tracking/python-3-shield.svg
    :target: https://pyup.io/repos/github/chopdgd/django-data-sources-tracking/
    :alt: Python 3


Django app for dealing with files/data sources and tracking them. Useful for tracking public annotations or bfx pipeline outputs

Documentation
-------------

The full documentation is at https://django-data-sources-tracking.readthedocs.io.

Quickstart
----------

Install Django Data Tracking::

    pip install django-data-sources-tracking

Add it to your `INSTALLED_APPS` (along with DRF and django-filters):

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'rest_framework',
        'django_filters',
        ...
        'data_sources_tracking',
        'user_activities',
        ...
    )

Add Django Data Tracking's URL patterns:

.. code-block:: python

    from data_sources_tracking import urls as data_sources_tracking_urls


    urlpatterns = [
        ...
        url(r'^', include(data_sources_tracking_urls, namespace='data_sources_tracking')),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.1.0 (2017-12-29)
++++++++++++++++++

* First release on PyPI.
* Initial models and REST API

0.2.0 (2018-01-05)
++++++++++++++++++

`Full Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.1.0...v0.2.0)>`_

* Improved REST API filters

0.2.1 (2018-01-09)
++++++++++++++++++

`Full Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.2.0...v0.2.1)>`_

* Updated packages and fixed issue with migrations

0.2.2 (2018-01-12)
++++++++++++++++++

`Full Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.2.1...v0.2.2)>`_

* Fixed route names for SimpleRouter

0.3.0 (2018-02-09)
++++++++++++++++++

`Full Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.2.2...v0.3.0)>`_

0.3.1 (2018-03-014)
++++++++++++++++++

`Full Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.3.0...v0.3.1)>`_

* Updated requirements
* Updated choices for file type choices to be more comprehensive


