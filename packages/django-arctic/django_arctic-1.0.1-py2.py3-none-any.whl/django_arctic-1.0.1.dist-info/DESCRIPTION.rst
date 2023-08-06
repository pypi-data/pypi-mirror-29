Django Arctic
=============

|PyPi version| |Build Status| |Coverage Status| |Read the Docs|

Django Arctic is a framework that speeds up the creation of custom
content management systems. It provides a Bootstrap 4 based user
interface, role based authentication and a number of generic Django
Views that provide great looking and feature-rich lists and forms.

-  The ListViews support sorting, searching, links, nested fields,
   custom columns and data sources not only from databases but also from
   APIs
-  The FormViews have enhanced widgets for DateTime, AutoComplete and
   MultiSelect and also support custom layouts without having to create
   extra templates.

.. figure:: docs/img/arctic_screenshot.png
   :alt: arctic screenshot

   arctic screenshot

Why
---

There are a lot of content management systems in the market that are a
good fit for the creation of many web sites. Most CMS's make assumptions
about the data model for posts, authentication and the administration
interface.

There is however a tipping point, where customizing a CMS product is so
extensive that it ends up being better to use some lower level
framework.

This is the case that Arctic wants to solve, creation of a CMS with a
high degree of customization. Instead of being a ready-to-use CMS,
Arctic is a framework that facilitates the construction of content
management systems.

Compatibility
-------------

-  Python 2.7, 3.5, 3.6
-  Django 1.10, 1.11, 2.0

.. |PyPi version| image:: https://img.shields.io/pypi/v/django-arctic.svg
   :target: https://pypi.python.org/pypi/django-arctic/
.. |Build Status| image:: https://travis-ci.org/sanoma/django-arctic.svg?branch=develop
   :target: https://travis-ci.org/sanoma/django-arctic
.. |Coverage Status| image:: https://coveralls.io/repos/github/sanoma/django-arctic/badge.svg?branch=develop
   :target: https://coveralls.io/github/sanoma/django-arctic
.. |Read the Docs| image:: https://readthedocs.org/projects/django-arctic/badge/?version=latest
   :target: https://django-arctic.readthedocs.io/en/latest/


