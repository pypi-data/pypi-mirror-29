

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Winterthur follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Winterthur uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.winterthur.png
  :target: https://travis-ci.org/OneGov/onegov.winterthur
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.winterthur/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.winterthur?branch=master
  :alt: Project Coverage

Latest PyPI Release
-------------------

.. image:: https://badge.fury.io/py/onegov.winterthur.svg
    :target: https://badge.fury.io/py/onegov.winterthur
    :alt: Latest PyPI Release

License
-------
onegov.winterthur is released under GPLv2

Changelog
---------

0.1.3 (2018-03-08)
~~~~~~~~~~~~~~~~~~~~~

- Fixes iframe height being calculated incorrectly.
  [href]

0.1.2 (2018-03-01)
~~~~~~~~~~~~~~~~~~~~~

- Applies Winterthur's CD to the framed version.
  [href]

0.1.1 (2018-02-06)
~~~~~~~~~~~~~~~~~~~~~

- Adds a frame-ancestors whitelist.
  [href]

0.1.0 (2018-01-31)
~~~~~~~~~~~~~~~~~~~~~

- Initial Release.
  [href]



