.. pypimonitor documentation master file, created by
   sphinx-quickstart on Sat May 28 11:40:01 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pypimonitor's documentation!
=======================================

An HTML dashboard to monitor your `PyPI packages <http://pypi.python.org>`_. It
displays a line charts showing the evolution of downloads across versions, and
a set of badges (download statistics, `readthedocs <http://readthedocs.io>`__ badge,
continuous integration, etc.). See :ref:`the example <example>` below.

It can only monitor stuff that is not on Pypi, but less information will be available.

It is available as a :mod:`command line interface <pypimonitor>` that generates
the HTML code, and as a :mod:`web server <pypimonitor.httpd>`, to generate and
serve this dashboard.

Contents:

.. toctree::
   :maxdepth: 2

   module
   yaml
   plugins

.. _example:

Example
=======

The :ref:`example configuration file <yamlexample>` produces the following output (click to enlarge).

|example|

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |example| image:: _static/spalax.png
  :target: http://spalax.frama.io/pypimonitor
