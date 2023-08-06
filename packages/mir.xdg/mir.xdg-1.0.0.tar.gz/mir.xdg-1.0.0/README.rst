mir.xdg README
====================

.. image:: https://circleci.com/gh/darkfeline/mir.xdg.svg?style=shield
   :target: https://circleci.com/gh/darkfeline/mir.xdg
   :alt: CircleCI
.. image:: https://codecov.io/gh/darkfeline/mir.xdg/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/darkfeline/mir.xdg
   :alt: Codecov
.. image:: https://badge.fury.io/py/mir.xdg.svg
   :target: https://badge.fury.io/py/mir.xdg
   :alt: PyPI Release
.. image:: https://readthedocs.org/projects/mir-xdg/badge/?version=latest
   :target: http://mir-xdg.readthedocs.io/en/latest/
   :alt: Latest Documentation

Template project for Python projects under the mir namespace.

Before running any other make command, run::

  $ pipenv install --dev

To build an installable wheel, run::

  $ make wheel

To build a source distribution, run::

  $ make sdist

To run tests, run::

  $ make check

To build docs, run::

  $ make html

To build a TAGS file, run::

  $ make TAGS

To clean up all built files, run::

  $ make distclean
