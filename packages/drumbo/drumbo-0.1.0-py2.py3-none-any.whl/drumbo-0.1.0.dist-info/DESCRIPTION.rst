========
Overview
========



Simple Step Sequencer

* Free software: BSD 2-Clause License

Installation
============

::

    pip install drumbo

Documentation
=============

https://python-drumbo.readthedocs.io/

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

0.1.0 (2018-03-07)
------------------

* First release on PyPI.


