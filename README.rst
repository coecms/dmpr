====
dmpr
====

ARCCSS Data Publication Tool

.. image:: https://readthedocs.org/projects/dmpr/badge/?version=latest
  :target: https://readthedocs.org/projects/dmpr/?badge=latest
.. image:: https://travis-ci.org/coecms/dmpr.svg?branch=master
  :target: https://travis-ci.org/coecms/dmpr
.. image:: https://circleci.com/gh/coecms/dmpr.svg?style=shield
  :target: https://circleci.com/gh/coecms/dmpr
.. image:: http://codecov.io/github/coecms/dmpr/coverage.svg?branch=master
  :target: http://codecov.io/github/coecms/dmpr?branch=master
.. image:: https://landscape.io/github/coecms/dmpr/master/landscape.svg?style=flat
  :target: https://landscape.io/github/coecms/dmpr/master
.. image:: https://codeclimate.com/github/coecms/dmpr/badges/gpa.svg
  :target: https://codeclimate.com/github/coecms/dmpr
.. image:: https://badge.fury.io/py/dmpr.svg
  :target: https://pypi.python.org/pypi/dmpr

.. content-marker-for-sphinx

-------
Install
-------

Conda install::

    conda install -c coecms dmpr

Pip install (into a virtual environment)::

    pip install dmpr

---
Use
---

Get help::

    dmpr --help

Convert output files to compressed CF-NetCDF::

    dmpr standardise --model MOM --output cfoutput.nc output1.nc output2.nc


-------
Develop
-------

Development install::

    git clone https://github.com/coecms/dmpr
    cd dmpr
    conda env create -f conda/dev-environment.yml
    source activate dmpr-dev
    pip install -e '.[dev]'

or::

    module load conda/analysis3
    install -e '.[dev]' --user

Run tests::

    py.test

Build documentation::

    python setup.py build_sphinx

Upload documentation::

    git subtree push --prefix docs/_build/html/ origin gh-pages

