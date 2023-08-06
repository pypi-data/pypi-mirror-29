
pytest-monkeytype
=================

|Build Status| |License| |PyPI Python| |PyPI Version| |PyPI Status|
|PyPI Wheel|

`MonkeyType <https://github.com/Instagram/MonkeyType>`__ as a
`pytest <https://docs.pytest.org/en/latest/>`__ plugin.

::

    pip install pytest-monkeytype

    # Generate annotations by running your pytest tests as usual:
    py.test --monkeytype-output=./monkeytype.sqlite3

    # Get a listing of modules annotated by monkeytype
    monkeytype list-modules 

    # Generate a stub file for those annotations using monkeytype:
    monkeytype stub some.module

    # Apply these annotations directly
    monkeytype apply some.module

This project is inspired by
`pytest-annotate <https://github.com/kensho-technologies/pytest-annotate>`__

.. |Build Status| image:: https://travis-ci.org/mariusvniekerk/pytest-monkeytype.svg?branch=master
   :target: https://travis-ci.org/mariusvniekerk/pytest-monkeytype
.. |License| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0
.. |PyPI Python| image:: https://img.shields.io/pypi/pyversions/pytest-monkeytype.svg
   :target: https://pypi.python.org/pypi/pytest-monkeytype
.. |PyPI Version| image:: https://img.shields.io/pypi/v/pytest-monkeytype.svg
   :target: https://pypi.python.org/pypi/pytest-monkeytype
.. |PyPI Status| image:: https://img.shields.io/pypi/status/pytest-monkeytype.svg
   :target: https://pypi.python.org/pypi/pytest-monkeytype
.. |PyPI Wheel| image:: https://img.shields.io/pypi/wheel/pytest-monkeytype.svg
   :target: https://pypi.python.org/pypi/pytest-monkeytype



