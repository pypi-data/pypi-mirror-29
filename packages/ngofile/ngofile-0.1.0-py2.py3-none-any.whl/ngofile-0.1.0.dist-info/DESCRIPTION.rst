========
Overview
========



misc file utilities

* Free software: GNU General Public License v3

Installation
============

::

    pip install ngofile

Documentation
=============

https://python-ngofile.readthedocs.io/

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

0.1.0 (2018-01-02)
------------------

* First release on PyPI.


