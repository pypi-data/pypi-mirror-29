Modules
=======

.. module:: pypimonitor

``pypimonitor``
---------------

This plugin can be called to generate an HTML page, whose code is printed to standard output.

.. argparse::
   :module: pypimonitor.__main__
   :func: commandline_parser

.. module:: pypimonitor.httpd

``pypimonitor.httpd``
---------------------

Alternatively, this module can sever the web pages, to be accessible from a web browser. If served on http://localhost, the following URLs are available:

* http://localhost (and http://localhost/index.html): If no GET arguments are given, display an index page, with a form to ask to render some pages. It also accepts GET arguments to specify which packages to process, and which cell plugins to use.
* http://localhost/foo/bar: When running the server, a directory ``DIR`` is given as argument. When calling this URL, a file ``DIR/foo/bar.yaml`` is searched, and if it exists, this file :ref:`is processed <yaml>` to render the HTML page.
