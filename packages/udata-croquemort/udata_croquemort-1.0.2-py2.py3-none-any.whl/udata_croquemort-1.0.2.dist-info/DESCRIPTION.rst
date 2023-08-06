uData-croquemort
================

This plugin provides integration between uData and Croquemort link checker.

Compatibility
-------------

**udata-croquemort** requires Python 2.7+ and `uData`_.

Installation
------------

Install `uData`_.

Remain in the same virtual environment (for Python) and use the same version of npm (for JS).

Install **udata-croquemort**:

.. code-block:: shell

    pip install udata-croquemort



Modify your local configuration file of **udata** (typically, `udata.cfg`) as following:

.. code-block:: python

    PLUGINS = ['croquemort']
    LINKCHECKING_DEFAULT_LINKCHECKER = 'croquemort'
    CROQUEMORT_URL = 'http://localhost:8000'
    CROQUEMORT_NB_RETRY = 10
    CROQUEMORT_DELAY = 1



.. _uData: https://github.com/opendatateam/udata

Changelog
=========

1.0.2 (2018-03-13)
------------------

- Switch to pytest

1.0.1 (2017-10-20)
------------------

- Fix setup.py version

1.0.0 (2017-10-20)
------------------

- Stable version

0.0.1 (2017-10-03)
------------------

- Initial release



