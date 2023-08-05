***********************
coverage_python_version
***********************

.. image:: https://img.shields.io/pypi/v/coverage_python_version.svg
   :target: https://pypi.python.org/pypi/coverage_python_version
.. image:: https://img.shields.io/pypi/l/coverage_python_version.svg
   :target: https://pypi.python.org/pypi/coverage_python_version


Overview
--------
``coverage_python_version`` is a `coverage.py`_ plugin that provides a very
basic means for you to exclude code from your coverage measurements based on
the version of Python that it is executed on.

.. _coverage.py: https://coverage.readthedocs.io


Usage
-----
1. Add ``coverage_python_version`` to ``plugins`` option in the ``run`` section
   of your ``coverage.py`` configuration.

2. Use the comment ``# pragma: PY2`` to notate blocks of code that should be
   measured under Python 2, and ``# pragma: PY3`` to notate blocks for Python
   3.


License
-------
``coverage_python_version`` is released under the terms of the `MIT License`_.

.. _MIT License: https://opensource.org/licenses/MIT



