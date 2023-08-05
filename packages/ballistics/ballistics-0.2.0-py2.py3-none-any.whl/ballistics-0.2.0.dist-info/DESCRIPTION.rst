========
Overview
========



A python package for calculating ballistics solutions.

* Free software: MIT license

Installation
============

::

    pip install ballistics

Documentation
=============

https://python-ballistics.readthedocs.io/

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

0.2.0 (2018-02-10)
------------------

* Free Recoil Energy solver added to extras module.

0.1.1 (2018-02-07)
------------------

* Implementation no longer supports PyPy (for now).

0.1.0 (2018-02-06)
------------------

* First release on PyPI.


