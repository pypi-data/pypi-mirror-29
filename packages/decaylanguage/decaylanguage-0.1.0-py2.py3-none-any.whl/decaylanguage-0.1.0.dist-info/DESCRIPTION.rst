========
Overview
========



A language to describe particle decays, and tools to work with them.

* Free software: BSD 3-Clause License

Installation
============

::

    pip install decaylanguage

Documentation
=============

https://decaylanguage.readthedocs.io/

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

0.1.0 (2018-03-13)
------------------

* First release on PyPI.


