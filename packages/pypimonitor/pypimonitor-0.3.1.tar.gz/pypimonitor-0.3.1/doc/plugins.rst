.. module:: pypimonitor.cell

Cell plugins
============

The content of cells is rendered by plugins. A :ref:`predefined list
<pluginlist>` is detailed below, but you can also :ref:`writeplugin`.

.. _pluginlist:

List of plugins
---------------

Base plugins
^^^^^^^^^^^^

``color``
"""""""""

Produce a square of the same color of the corresponding download chart line. Takes no arguments.

``empty``
"""""""""

Produce an empty cell. Takes no arguments.

.. _error:

``error``
"""""""""

Produce a text corresponding to an error (this is used internally). Takes no arguments.

``html``
""""""""

Copy raw html code.

* ``html`` (required)
  The raw html code to render.

``link``
""""""""

Produce a link to an URL.

* ``href`` (required)
  URL of the ressource to link to.

* ``content`` (defaults to the `href` argument)
  The text of the link.

Gitlab
^^^^^^

.. _gitlabci:

``gitlabci``
""""""""""""

Produce a badge for latest `gitlabCI <//about.gitlab.com/gitlab-ci/>`__ build.

* ``server`` (default `http://gitlab.com`)
  URL of the gitlab server.

* ``user`` (required)
  Name of the user owning the package.

* ``slug``
  Repository name, if different from the pypi package name.

Those options, combined, should produce the package URL: ``{server}/{user}/{slug}``.

``gitlabcicoverage``
""""""""""""""""""""

Produce a test coverage badge for latest `gitlabCI <//about.gitlab.com/gitlab-ci/>`__ build.

* ``server`` (default `http://gitlab.com`)
  URL of the gitlab server.

* ``user`` (required)
  Name of the user owning the package.

* ``slug``
  Repository name, if different from the pypi package name.

Those options, combined, should produce the package URL: ``{server}/{user}/{slug}``.

PyPI
^^^^

``homepage``
""""""""""""""""""""""

Package home page, retrieved from Pypi metadata.

* ``homepage`` (default to pypi home page value)
  Project home page, if different from the value retrieved from pypi.

`Readthedocs <http://readthedocs.io>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _Readthedocs:

``readthedocs``
"""""""""""""""

`Readthedocs <http://readthedocs.io>`__ build badge.

* ``slug``
  Repository name, if different from the pypi package name.

* ``branch``
  Branch name, if the default branch should not be used.

* ``lang``
  Documentation language, if the default lang should not be used.

`Shields <http://shields.io>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pypiddownloads``
""""""""""""""""""

Badge displaying Pypi daily download statistics.

``pypiwdownloads``
""""""""""""""""""

Badge displaying Pypi weekly download statistics.

``pypimdownloads``
""""""""""""""""""

Badge displaying Pypi monthly download statistics.

``pypiversion``
"""""""""""""""

Badge displaying Pypi version.

`Travis <http://travis-ci.org/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``travisci``
""""""""""""

`Travis <http://travis-ci.org/>`_ badge.

* ``user`` (required)
  Travis username.

* ``slug``
  Repository name, if different from the pypi package name.

.. _writeplugin:

Write your own
--------------

The HTML page is generated using the `Jinja2 <http://jinja.pocoo.org/>`_
template system, but you don't *have to* use it for your plugins.

A plugin is an object, subclass of :class:`Cell`. The
:meth:`Cell.render` method must be implemented: it is the
method that is called to fill a cell. Since for many usage, your plugin will
simply be a template, you can use the :class:`Jinja2` class,
which makes this a lot easier. Both classes makes it easy to define
:ref:`default and required arguments <defaultrequired>`, and to :ref:`log errors <errors>`.

Raw
^^^

.. autoclass:: Cell
   :members: render, render_error, keyword, title, default, required

Jinja2
^^^^^^

.. autoclass:: Jinja2
   :members: keyword, template

.. _defaultrequired:

Default and Required arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A built-in feature eases processing default and required arguments, for simple
cases. This is automatically done before calling the
:meth:`Cell.render` method.

If your plugin has absolute default values for some arguments, those can be set
in the :attr:`Cell.default` dictionary. Keys are arguments,
and values are default values for these arguments.

If your plugin has required arguments (plugin cannot work without those
arguments), they can be listed in the :attr:`Cell.required`
list. Using a cell without setting one of those arguments will display an
error.

For more complex cases (either `foo` or `bar` should be set; `foo` default
value is `bar` if `baz` is not set, `None` otherwise; `foo` is required only if
`bar` is not set; etc.), you have to implement it by hand in the
:meth:`Cell.render` method.

.. _errors:

Errors
^^^^^^

To display an error (both in the generated HTML page, and in the log), the
:class:`Cell` class has a :meth:`Cell.render_error` method. This is to be used
as::

    class Foo(Cell):
        keyword = 'foo'

        def render(self, context, package, cell):
            if not 'bar' in cell:
                return self.render_error(context, self.keyword, package, "Error: argument 'bar' missing.")
            return "<p>" + cell['bar'] + "</p>"
