

.. image:: https://raw.githubusercontent.com/OneGov/onegov.notice/master/docs/onegov.notice.png
  :alt: States

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Notice follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Notice uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.notice.png
  :target: https://travis-ci.org/OneGov/onegov.notice
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.notice/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.notice?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://img.shields.io/pypi/v/onegov.notice.svg
  :target: https://pypi.python.org/pypi/onegov.notice
  :alt: Latest PyPI Release

License
-------
onegov.notice is released under GPLv2

Changelog
---------
0.6.0 (2018-03-12)
~~~~~~~~~~~~~~~~~~~

- Allows to search by notice id.
  [msom]

0.5.0 (2018-02-07)
~~~~~~~~~~~~~~~~~~~

- Allows to search by author name and place.
  [msom]

0.4.0 (2018-02-06)
~~~~~~~~~~~~~~~~~~~

- Adds author fields (name, date, place) to notices.
  [msom]

- Requires Python 3.6.
  [href]

0.3.0 (2017-10-26)
~~~~~~~~~~~~~~~~~~~

- Adds categories and organizations to notices.
  [msom]

0.2.0 (2017-10-13)
~~~~~~~~~~~~~~~~~~~

- Allows to sort by group and user names.
  [msom]

- Allows to sarch categories, organizations, group names and user names.
  [msom]

0.1.2 (2017-08-30)
~~~~~~~~~~~~~~~~~~~

- Sorts by first issue date by default.
  [msom]

0.1.1 (2017-08-28)
~~~~~~~~~~~~~~~~~~~

- Adds an intialization function for searches to the collection.
  [msom]

0.1.0 (2017-08-21)
~~~~~~~~~~~~~~~~~~~

- First version.
  [msom]

0.0.13 (2017-08-18)
~~~~~~~~~~~~~~~~~~~

- Allows to filter notices by a user group IDs.
  [msom]

0.0.12 (2017-08-18)
~~~~~~~~~~~~~~~~~~~

- Nothing.
  [msom]

0.0.11 (2017-08-18)
~~~~~~~~~~~~~~~~~~~

- Adds groups to notices.
  [msom]

0.0.10 (2017-08-17)
~~~~~~~~~~~~~~~~~~~

- Uses latest onegov.user.
  [msom]

0.0.9 (2017-08-17)
~~~~~~~~~~~~~~~~~~~

- Adds missing constructor argument.
  [msom]

0.0.8 (2017-08-16)
~~~~~~~~~~~~~~~~~~~

- Nothing.
  [msom]

0.0.7 (2017-08-16)
~~~~~~~~~~~~~~~~~~~

- Adds an 'accepted' state.
  [msom]

0.0.6 (2017-08-15)
~~~~~~~~~~~~~~~~~~~

- Adds an issues column to the notices.
  [msom]

0.0.5 (2017-08-11)
~~~~~~~~~~~~~~~~~~~

- Fix default direction when ordering notices.
  [msom]

0.0.4 (2017-08-11)
~~~~~~~~~~~~~~~~~~~

- Allows to order notices.
  [msom]

- Adds an issue date column to the notices.
  [msom]

0.0.3 (2017-08-09)
~~~~~~~~~~~~~~~~~~~

- Adds an organization column to the notices.
  [msom]

0.0.2 (2017-08-09)
~~~~~~~~~~~~~~~~~~~

- Allows to filter notices by a search term.
  [msom]

- Allows to filter notices by user IDs.
  [msom]

0.0.1 (2017-07-14)
~~~~~~~~~~~~~~~~~~

- Initial Release


