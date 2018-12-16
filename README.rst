========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        |
        | |landscape|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/py-usecase/badge/?style=flat
    :target: https://readthedocs.org/projects/py-usecase
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/bagerard/py-usecase.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/bagerard/py-usecase

.. |requires| image:: https://requires.io/github/bagerard/py-usecase/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/bagerard/py-usecase/requirements/?branch=master

.. |landscape| image:: https://landscape.io/github/bagerard/py-usecase/master/landscape.svg?style=flat
    :target: https://landscape.io/github/bagerard/py-usecase/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/usecase.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/usecase

.. |commits-since| image:: https://img.shields.io/github/commits-since/bagerard/py-usecase/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/bagerard/py-usecase/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/usecase.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/usecase

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/usecase.svg
    :alt: Supported versions
    :target: https://pypi.org/project/usecase

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/usecase.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/usecase


.. end-badges

Boilerplate for using a use case layer

* Free software: MIT license

Installation
============

::

    pip install usecase

Documentation
=============


https://py-usecase.readthedocs.io/


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
