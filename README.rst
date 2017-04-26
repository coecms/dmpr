====
dmpr
====

ARCCSS Data Publication Tool

.. image:: https://readthedocs.org/projects/dmpr/badge/?version=latest
  :target: https://readthedocs.org/projects/dmpr/?badge=latest
.. image:: https://travis-ci.org/ScottWales/dmpr.svg?branch=master
  :target: https://travis-ci.org/ScottWales/dmpr
.. image:: https://circleci.com/gh/ScottWales/dmpr.svg?style=shield
  :target: https://circleci.com/gh/ScottWales/dmpr
.. image:: http://codecov.io/github/ScottWales/dmpr/coverage.svg?branch=master
  :target: http://codecov.io/github/ScottWales/dmpr?branch=master
.. image:: https://landscape.io/github/ScottWales/dmpr/master/landscape.svg?style=flat
  :target: https://landscape.io/github/ScottWales/dmpr/master
.. image:: https://codeclimate.com/github/ScottWales/dmpr/badges/gpa.svg
  :target: https://codeclimate.com/github/ScottWales/dmpr
.. image:: https://badge.fury.io/py/dmpr.svg
  :target: https://pypi.python.org/pypi/dmpr

.. content-marker-for-sphinx

-------
Install
-------

Conda install::

    conda install -c ScottWales dmpr

Pip install (into a virtual environment)::

    pip install dmpr

---
Use
---

Get help::

    dmpr --help

Post process a model run::

    dmpr post --rundir /path/to/configs output1 output2

List registered data management plans::

    dmpr dmp list

Export data management plan 51::

    dmpr dmp export --format=json 51

-------
Develop
-------

Development install::

    git clone https://github.com/ScottWales/dmpr
    cd dmpr
    conda env create -f conda/dev-environment.yml
    source activate dmpr-dev
    pip install -e '.[dev]'

Run tests::

    py.test

Build documentation::

    python setup.py build_sphinx

Upload documentation::

    git subtree push --prefix docs/_build/html/ origin gh-pages

