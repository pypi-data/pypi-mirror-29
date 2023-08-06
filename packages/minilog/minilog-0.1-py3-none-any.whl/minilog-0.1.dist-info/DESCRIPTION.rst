Unix: |Unix Build Status| Windows: |Windows Build Status|\ Metrics:
|Coverage Status| |Scrutinizer Code Quality|\ Usage: |PyPI Version|

Overview
========

Instead of including this boilerplate in every module:

.. code:: python

    import logging

    log = logging.getLogger(__name__)

    def foobar(name):
        log.info("Hello, %s!", name)

with this package you can simply:

.. code:: python

    import log

    def foobar(name):
        log.info("Hello, %s!", name)

It will produce the exact same standard library ``logging`` records
behind the scenes.

Installation
============

.. code:: sh

    $ pip install minilog

Setup
=====

Optionally, change for format for all logging handlers:

.. code:: python

    log.init("%(levelname)s: %(name)s: %(message)s")

.. |Unix Build Status| image:: https://img.shields.io/travis/jacebrowning/minilog/develop.svg
   :target: https://travis-ci.org/jacebrowning/minilog
.. |Windows Build Status| image:: https://img.shields.io/appveyor/ci/jacebrowning/minilog/develop.svg
   :target: https://ci.appveyor.com/project/jacebrowning/minilog
.. |Coverage Status| image:: https://img.shields.io/coveralls/jacebrowning/minilog/develop.svg
   :target: https://coveralls.io/r/jacebrowning/minilog
.. |Scrutinizer Code Quality| image:: https://img.shields.io/scrutinizer/g/jacebrowning/minilog.svg
   :target: https://scrutinizer-ci.com/g/jacebrowning/minilog/?branch=develop
.. |PyPI Version| image:: https://img.shields.io/pypi/v/minilog.svg
   :target: https://pypi.python.org/pypi/minilog

Revision History
================

0.1 (2018/03/03)
----------------

-  Initial release.


