==========
 DataCite
==========

.. image:: https://img.shields.io/travis/inveniosoftware/datacite.svg
   :target: https://travis-ci.org/inveniosoftware/datacite

.. image:: https://img.shields.io/coveralls/inveniosoftware/datacite.svg
   :target: https://coveralls.io/r/inveniosoftware/datacite?branch=master

.. image:: https://img.shields.io/pypi/v/datacite.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/datacite/

.. image:: https://img.shields.io/pypi/dm/datacite.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/datacite/

.. image:: https://img.shields.io/github/license/inveniosoftware/datacite.svg
   :target: https://github.com/inveniosoftware/datacite/blob/master/LICENSE

.. image:: https://img.shields.io/github/tag/inveniosoftware/datacite.svg
   :target: https://github.com/inveniosoftware/datacite/releases/




About
=====

Python API wrapper for the DataCite Metadata Store API and DataCite XML
generation.


Installation
============
The datacite package is on PyPI so all you need is: ::

    pip install datacite


Documentation
=============

Documentation is readable at http://datacite.readthedocs.io/ or can be
built using Sphinx: ::

    pip install datacite[docs]
    python setup.py build_sphinx


Testing
=======
Running the test suite is as simple as: ::

    pip install -e .[all]
    ./run-tests.sh


Changes
=======
Version v1.0.1 (released 2018-03-08):

- Fixes schema location url for DataCite v4.1

Version v1.0.0 (released 2018-02-28):

- Adds full support for DataCite Metadata Schema v4.1 XML generation.

Version v0.3.0 (released 2016-11-18):

- Adds full support for DataCite Metadata Schema v4.0 XML generation.

- Adds the message from the server in the error exceptions.

Version v0.2.2 (released 2016-09-23):

- Fixes issue with generated order of nameIdentifier and affiliation tags.

Version v0.2.1 (released 2016-03-29):

- Fixes issue with JSON schemas not being included when installing from PyPI.

Version v0.2.0 (released 2016-03-21):

- Adds DataCite XML generation support.

Version 0.1 (released 2015-02-25):

- Initial public release.


