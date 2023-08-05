.. -*- mode: rst -*-


safe-cast
---------

Safe casting of Python base types.


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


.. |docs| image:: https://readthedocs.org/projects/safe-cast/badge/?style=flat
    :target: http://safe-cast.readthedocs.io
    :alt: Documentation Status

.. |hits| image:: http://hits.dwyl.io/TuneLab/safe-cast.svg
    :target: http://hits.dwyl.io/TuneLab/safe-cast
    :alt: Hit Count

.. |contributors| image:: https://img.shields.io/github/contributors/TuneLab/safe-cast.svg
    :target: https://github.com/TuneLab/safe-cast/graphs/contributors
    :alt: Contributors

.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: License Status
    :target: https://opensource.org/licenses/MIT

.. |travis| image:: https://travis-ci.org/TuneLab/safe-cast.svg?branch=master
    :target: https://travis-ci.org/TuneLab/safe-cast
    :alt: Travis

.. |coveralls| image:: https://coveralls.io/repos/github/TuneLab/safe-cast/badge.svg?branch=master
    :target: https://coveralls.io/github/TuneLab/safe-cast?branch=master
    :alt: Code Coverage Status

.. |requires| image:: https://requires.io/github/TuneLab/safe-cast/requirements.svg?branch=master
     :target: https://requires.io/github/TuneLab/safe-cast/requirements/?branch=master
     :alt: Requirements Status

.. |version| image:: https://img.shields.io/pypi/v/safe-cast.svg?style=flat
    :target: https://pypi.python.org/pypi/safe-cast
    :alt: PyPI Package latest release

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/safe-cast.svg?style=flat
    :target: https://pypi.python.org/pypi/safe-cast
    :alt: Supported versions

.. end-badges


Functions
---------

+-----------------------------------------------+------------------------------------------------------------------+
| Function                                      | Purpose                                                          |
+===============================================+==================================================================+
| ``safe_cast(val, to_type, default=None)``     | Cast value to requested type, if failed, then used default.      |
+-----------------------------------------------+------------------------------------------------------------------+
| ``safe_str(val, default=None)``               | Cast value to type string, if failed, then used default.         |
+-----------------------------------------------+------------------------------------------------------------------+
| ``safe_float(val, ndigits=2, default=None)``  | Cast value to type float, if failed, then used default.          |
+-----------------------------------------------+------------------------------------------------------------------+
| ``safe_int(val, default=None)``               | Cast value to type int, if failed, then used default.            |
+-----------------------------------------------+------------------------------------------------------------------+
| ``safe_dict(val, default=None)``              | Cast value to type dictionary, if failed, then used default.     |
+-----------------------------------------------+------------------------------------------------------------------+
| ``safe_smart_cast(val)``                      | Determine type based upon value, and cast to that type.          |
+-----------------------------------------------+------------------------------------------------------------------+
| ``safe_cost(val)``                            | Cast value to type float by 4 decimal points.                    |
+-----------------------------------------------+------------------------------------------------------------------+
| ``safe_fraction(val)``                        | Cast fraction to type float, if failed, then used default.       |
+-----------------------------------------------+------------------------------------------------------------------+


Usage
-----

``safe_cast(val, to_type, default=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Safely cast a value to type, and if failed, returned default if exists.

    Optional: Pass default value. Returned if casting fails.

    :param val: Value to be cast.
    :param to_type: Safely cast to a specific type.
    :param default: Default if casting fails.
    :return: Return casted value or default.

``safe_int(val, default=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Safely cast a value to an integer.

    Optional: Pass default value. Returned if casting fails.

    :param val: Value to be cast to int.
    :param default: Default if casting fails.
    :return: Return int casted value or default.

``safe_float(val, ndigits=2, default=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Safely cast a value to float, remove ',' if exists to ensure strings "1,234.5" are transformed to become "1234.5".

    Optional: Pass default value. Returned if casting fails.

    :param val: Value to be cast to float.
    :param ndigits: Number of digits in float.
    :param default: Default if casting fails.
    :return: Return float casted value or default.

``safe_str(val, default=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Safely cast a value to a string.

    Optional: Pass default value. Returned if casting fails.

    :param val: Value to be cast to string.
    :param default: Default if casting fails.
    :return: Return string casted value or default.

``safe_dict(val, default=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Safely cast a value to a dictionary.

    Optional: Pass default value. Returned if casting fails.

    :param val: Value to be cast to dictionary.
    :param default: Default if casting fails.
    :return: Return dictionary casted value or default.

``safe_smart_cast(val)``
~~~~~~~~~~~~~~~~~~~~~~~~
    Safely cast a value to the best matching type.
    Optional: Pass default value. Returned if casting fails.

    :param val: Value to be smartly cast.
    :return: Typed value

``safe_fraction(fraction, ndigits=2, default=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Safely cast a fraction string to float.

    Optional: Pass default value. Returned if casting fails.

    :param fraction: Value of fraction to be cast to float.
    :param ndigits: Number of digits in float.
    :param default: Default if casting fails.
    :return: Return float casted value or default.
