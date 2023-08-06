===============================
django-pgcli
===============================

.. image:: https://img.shields.io/travis/ashchristopher/django-pgcli.svg
        :target: https://travis-ci.org/ashchristopher/django-pgcli

.. image:: https://img.shields.io/pypi/v/django-pgcli.svg
        :target: https://pypi.python.org/pypi/django-pgcli


Alternate database runtime for Django that replaces psql with pgcli when
calling the Django `dbshell` management command.

* Free software: BSD license

Installation
------------

Installation is as simple as::

    $ pip install django-pgcli

Add ``django_pgcli`` to your ``INSTALLED_APPS`` setting.

    INSTALLED_APPS = [
        ...,
        'django_pgcli',
    ]

Usage
-----
Call the `dbshell` command.

    ./manage.py dbshell




History
-------

0.0.2 (2015-04-26)
---------------------
* Fixed typo in README.rst

0.0.1 (2015-04-25)
---------------------

* Initial release.


