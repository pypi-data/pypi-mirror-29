.. -*- mode: rst -*-

pytz-convert
------------

Python extension for package `pytz <https://pypi.python.org/pypi/pytz>`_.


Badges
------

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs| |license|
    * - info
      - |hits| |contributors|
    * - tests
      - |travis| |coveralls|
    * - package
      - |version| |supported-versions|
    * - other
      - |requires|

.. |docs| image:: https://readthedocs.org/projects/pytz-convert/badge/?style=flat
    :target: http://pytz-convert.readthedocs.io
    :alt: Documentation Status

.. |hits| image:: http://hits.dwyl.io/TuneLab/pytz-convert.svg
    :target: http://hits.dwyl.io/TuneLab/pytz-convert
    :alt: Hit Count

.. |contributors| image:: https://img.shields.io/github/contributors/TuneLab/pytz-convert.svg
    :target: https://github.com/TuneLab/pytz-convert/graphs/contributors
    :alt: Contributors

.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: License Status
    :target: https://opensource.org/licenses/MIT

.. |travis| image:: https://travis-ci.org/TuneLab/pytz-convert.svg?branch=master
    :target: https://travis-ci.org/TuneLab/pytz-convert
    :alt: Travis-CI Build Status

.. |coveralls| image:: https://coveralls.io/repos/TuneLab/pytz-convert/badge.svg?branch=master&service=github
    :target: https://coveralls.io/r/TuneLab/pytz-convert?branch=master
    :alt: Code Coverage Status

.. |requires| image:: https://requires.io/github/TuneLab/pytz-convert/requirements.svg?branch=master
    :target: https://requires.io/github/TuneLab/pytz-convert/requirements/?branch=master
    :alt: Requirements Status

.. |version| image:: https://img.shields.io/pypi/v/pytz-convert.svg?style=flat
    :target: https://pypi.python.org/pypi/pytz-convert
    :alt: PyPI Package latest release

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pytz-convert.svg?style=flat
    :target: https://pypi.python.org/pypi/pytz-convert
    :alt: Supported versions

.. end-badges


Install
-------

.. code-block:: bash

    pip install pytz-convert


Architecture
------------

``pytz-convert`` is an extension of the `pytz <https://pypi.python.org/pypi/pytz>`_ providing functions for converting timezone names, abbreviations, and offsets.


Functions
---------

- ``convert_bing_ads_tz``: Convert **Bing timezone name** to **Standard timezone name**.
- ``convert_tz_abbrev_to_tz_hours()``: Convert **timezone abbreviation** to **timezone hours**.
- ``convert_tz_abbrev_to_tz_offset()``: Convert **timezone abbreviation** to **timezone offset**.
- ``convert_tz_abbrev_to_tz_seconds()``: Convert **timezone abbreviation** to **timezone seconds**.
- ``convert_tz_hours_to_tz_offset()``: Convert **timezone hours** into **timezone offset**.
- ``convert_tz_name_to_date_tz_abbrev()``: Convert **timezone name + date** to **timezone abbreviation**.
- ``convert_tz_name_to_date_tz_offset()``: Convert **timezone name + date** to **timezone offset**.
- ``convert_tz_name_to_now_tz_abbrev()``: Convert **timezone name + current date** to current **timezone abbreviation**.
- ``convert_tz_name_to_now_tz_offset()``: Convert **timezone name + current date** to current **timezone offset**.
- ``convert_tz_offset_and_date_to_tz_name()``: Convert **timezone offset + date** to **timezone name**.
- ``convert_tz_offset_to_now_tz_abbrev()``: Convert **timezone offset + current date** to current **timezone abbreviation**.
- ``convert_tz_offset_to_tz_hours()``: Convert **timezone offset** to **hours**.
- ``convert_tz_offset_to_tz_minutes()``: Convert **timezone offset** to **minutes**.
- ``convert_tz_offset_to_tz_seconds()``: Convert **timezone offset** to **seconds**.
- ``parse_gmt_offset_timezone()``: Parse GMT string into **timezone name** and **timezone offset**.
- ``validate_tz_abbrev()``: Validate **timezone abbreviation**.
- ``validate_tz_name()``: Validate **timezone name**.

Requirements
------------

``pytz-convert`` module is built upon Python 3 and has dependencies upon
several Python modules available within `Python Package Index PyPI <https://pypi.python.org/pypi>`_.

.. code-block:: bash

    make install-requirements

or


.. code-block:: bash

    python3 -m pip uninstall --yes --no-input -r requirements.txt
    python3 -m pip install --upgrade -r requirements.txt


Dependencies
------------

- `pytz <https://pypi.python.org/pypi/pytz>`_
- `python-dateutil <https://pypi.python.org/pypi/python-dateutil>`_


.. :changelog:

Release History
===============

0.2.8 (2018-02-16)
------------------
- migrate to github/TuneLab.

0.2.3 (2018-01-25)
------------------
- migrate to github/tuneinc.
- LICENSE: MIT

0.2.0 (2017-12-10)
------------------
- readthedocs.org

0.1.0 (2017-11-25)
------------------
- README
- Tests

0.0.5 (2017-06-15)
------------------
* Add BING_TIMEZONES_TO_PREFERRED dict that maps bing tz names to pytz tz names
* Add convert_bing_ads_tz function

0.0.1 (2016-11-17)
------------------
* Initial release



