.. image:: https://img.shields.io/pypi/v/jaraco.geo.svg
   :target: https://pypi.org/project/jaraco.geo

.. image:: https://img.shields.io/pypi/pyversions/jaraco.geo.svg

.. image:: https://img.shields.io/travis/jaraco/jaraco.geo/master.svg
   :target: https://travis-ci.org/jaraco/jaraco.geo

.. image:: https://readthedocs.org/projects/jaracogeo/badge/?version=latest
   :target: https://jaracogeo.readthedocs.io/en/latest/?badge=latest

Geographic support library

Requirements
============

The current geotrans2 dynamic libraries are currently built only
for Windows, so support for other platforms is currently not present.
However, the DMS class should be usable in a pure Python environment.

Contents
========

``jaraco.geo`` includes an object named DMS for storing and manipulating
values in degrees, minutes, and seconds. See the jaraco.geo module for
details and documentation.

``jaraco.geo`` also implements geotrans2 by the `NGA
<http://www.nga.mil>`_. See the tests directory in the
repository for sample usage.
