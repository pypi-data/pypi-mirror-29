

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Directory follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Directory uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.directory.png
  :target: https://travis-ci.org/OneGov/onegov.directory
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.directory/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.directory?branch=master
  :alt: Project Coverage

Latest PyPI Release
-------------------

.. image:: https://badge.fury.io/py/onegov.directory.svg
    :target: https://badge.fury.io/py/onegov.directory
    :alt: Latest PyPI Release

License
-------
onegov.directory is released under GPLv2

Changelog
---------

0.2.1 (2018-02-23)
~~~~~~~~~~~~~~~~~~~~~

- Fixes a serious performance regression.
  [href]

0.2.0 (2018-02-09)
~~~~~~~~~~~~~~~~~~~~~

- Filters values within one category using OR (existing behaviour) and values
  between categories using AND (was OR).
  [href]

0.1.7 (2018-02-06)
~~~~~~~~~~~~~~~~~~~~~

- Fixes entries from other directories being considered as duplicates.
  [href]

0.1.6 (2018-01-24)
~~~~~~~~~~~~~~~~~~~~~

- Fixes number ranges not being validated during migrations.
  [href]

0.1.5 (2018-01-24)
~~~~~~~~~~~~~~~~~~~~~

- Fixes import duplicates not being detected in all instances.
  [href]

- Fixes limit not being applied correctly (off by one).
  [href]

- Adds the ability to provide a callback for each successful entry import.
  [href]

- Fixes a case where an empty image field would result in an error.
  [href]

0.1.4 (2018-01-23)
~~~~~~~~~~~~~~~~~~~~~

- Ensures the imported lat/lon values are proper coordinates.
  [href]

0.1.3 (2018-01-22)
~~~~~~~~~~~~~~~~~~~~~

- Fixes coordinates export.
  [href]

0.1.2 (2018-01-04)
~~~~~~~~~~~~~~~~~~~~~

- Improves the flexibility of the migration helper.
  [href]

- Fixes a case where invalid entries would be added to the directory.
  [href]

0.1.1 (2017-12-29)
~~~~~~~~~~~~~~~~~~~~~

- Throws an error early if an entry with a duplicate name is created.
  [href]

0.1.0 (2017-12-22)
~~~~~~~~~~~~~~~~~~~~~

- Switches to onegov core's custom json module.
  [href]

- Adds support for text to url migration.
  [href]

- Changes the category filter from AND to OR.
  [href]

- Adds support for radio to checkbox migration.
  [href]

0.0.2 (2017-11-30)
~~~~~~~~~~~~~~~~~~~~~

- Fixes required fileinput fields not working.
  [href]

0.0.1 (2017-11-08)
~~~~~~~~~~~~~~~~~~~~~

- Initial Release.
  [href]


