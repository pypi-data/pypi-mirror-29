.. README.rst
.. Copyright (c) 2018 Pablo Acosta-Serafini
.. See LICENSE for details


.. image:: https://badge.fury.io/py/pytest-pmisc.svg
    :target: https://pypi.python.org/pypi/pytest-pmisc
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/l/pytest-pmisc.svg
    :target: https://pypi.python.org/pypi/pytest-pmisc
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/pytest-pmisc.svg
    :target: https://pypi.python.org/pypi/pytest-pmisc
    :alt: Python versions supported

.. image:: https://img.shields.io/pypi/format/pytest-pmisc.svg
    :target: https://pypi.python.org/pypi/pytest-pmisc
    :alt: Format

|

.. image::
    https://readthedocs.org/projects/pip/badge/?version=stable
    :target: http://pip.readthedocs.org/en/stable/?badge=stable
    :alt: Documentation status

|

Description
===========

.. role:: bash(code)
	:language: bash

This module contains a simple Pytest plugin for the pmisc test module.

When using the functions in the `test
<https://pmisc.readthedocs.io/en/stable/api.html#test>`_ module of the
`pmisc <http://pmisc.readthedocs.io>`_ package
(`assert_arg_invalid <http://pmisc.readthedocs.io/en/stable/api.html#pmisc.assert_arg_invalid>`_,
`assert_exception <http://pmisc.readthedocs.io/en/stable/api.html#pmisc.assert_exception>`_,
`assert_prop <http://pmisc.readthedocs.io/en/stable/api.html#pmisc.assert_prop>`_,
`assert_ro_prop <http://pmisc.readthedocs.io/en/stable/api.html#pmisc.assert_ro_prop>`_, and
`compare_strings <http://pmisc.readthedocs.io/en/stable/api.html#pmisc.compare_strings>`_), 
`Pytest <http://docs.pytest.org/en/latest/>`_ assertion failure reports stop at
the code line using these functions and do not continue into the pmisc test
module.  This focuses attention on the actual assertion failing, and improves
clarity and conciseness

Interpreter
===========

The plugin has been developed and tested with Python 2.7, 3.5 and 3.6 under
Linux (Debian, Ubuntu), Apple OS X and Microsoft Windows

Installing
==========

.. code-block:: bash

	$ pip install pytest-pmisc

Documentation
=============

Available at `Read the Docs <http://pytest-pmisc.readthedocs.io>`_

.. include:: ../CHANGELOG.rst

License
=======

.. include:: ../LICENSE
