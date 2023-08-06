Unix: |Unix Build Status| Windows: |Windows Build Status|\ Metrics:
|Coverage Status| |Scrutinizer Code Quality|\ Usage: |PyPI Version|

Overview
========

Every project should utilize logging, but sometimes the required
boilerplate is too much. Instead of including this:

.. code:: python

    import logging 

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(name)s: %(message)s",
    )

    log = logging.getLogger(__name__)

    def greet(name):
        log.info("Hello, %s!", name)

with this package you can simply:

.. code:: python

    import log

    def greet(name):
        log.info("Hello, %s!", name)

It will produce the exact same standard library ``logging`` records
behind the scenes.

Installation
============

.. code:: sh

    $ pip install minilog

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
