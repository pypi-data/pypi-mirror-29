========
Overview
========



The Python ballistics package is a collection of functions to help analyze and understand the motion of an un-powered
(i.e. not a rocket, missile, etc) projectile from the muzzle to the target. The ``ballistics.extras`` module contains
related functions that aren't strictly related to the study of ballistics but have proven interesting or useful.

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

0.4.0
-----
* Recoil Impulse solver added to extras module.
* Firearm Code made optional for all Recoil solvers.

0.3.0 (2018-02-12)
------------------
* Recoil Velocity solver added to extras module.

0.2.0 (2018-02-10)
------------------
* Free Recoil Energy solver added to extras module.

0.1.1 (2018-02-07)
------------------
* Implementation no longer supports PyPy (for now).

0.1.0 (2018-02-06)
------------------
* First release on PyPI.


