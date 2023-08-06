=============================
JPT Django Utils
=============================

.. image:: https://badge.fury.io/py/jpt-django-utils.svg
    :target: https://badge.fury.io/py/jpt-django-utils

.. image:: https://travis-ci.com/jptd/JPT-django-utils.svg?token=whRx2vqBkv8CM6GEdmEf&branch=develop
    :target: https://travis-ci.com/jptd/JPT-django-utils

Re-usable Django utils.

Documentation
-------------

The full documentation is at https://JPT-DJANGO-UTILS.readthedocs.io.

Quickstart
----------

Install JPT Django Utils::

    pip install jpt-django-utils

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'jpt_django_utils.apps.JptDjangoUtilsConfig',
        ...
    )

Add JPT Django Utils's URL patterns:

.. code-block:: python

    from jpt_django_utils import urls as jpt_django_utils_urls


    urlpatterns = [
        ...
        url(r'^', include(jpt_django_utils_urls)),
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
