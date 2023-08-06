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
