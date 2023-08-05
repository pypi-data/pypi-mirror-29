========
Overview
========



Django Authentication and Authorisation using Auth0 and Python Social Auth

Warning, this library is under active development, it is also not 1.0 yet, and has a sort of 'production' user already. Documentation, bugs, features, and pretty much everything is in flux.


* Free software: BSD license

Installation
============

::

    pip install django-auth0-user

Documentation
=============

https://django-auth0-user.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.1.0 (2017-09-18)
------------------

* First release on PyPI.


