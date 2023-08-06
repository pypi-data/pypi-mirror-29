.. _yaml:

YAML configuration files
========================

Some plugins try to guess the appropriate required values, but it is not always possible. For instance, plugin :ref:`Readthedocs` cannot guess the documentation URL, since it can differ from ``http://<PypiPackageName>.readthedocs.io`` (for instance, the documentation URL of `sphinxcontrib-packages <http://pypi.python.org/pypi/sphinxcontrib-packages>`_ is http://packages.readthedocs.io and not http://spinxcontrib-packages.readthedocs.io). Thus, it may be necessary to provide additional information. This can be done using YAML files.

Processing YAML files
---------------------

Configuration files can be processed by both :mod:`pypimonitor` command line interface, and by the :mod:`pypimonitor.httpd` web sever. See the relevant documentation for more information.

Writing YAML files
------------------

.. _yamlexample:

Example
"""""""

The `example page <_static/spalax.html>`_ is produced using the following YAML file:

.. literalinclude:: ../examples/spalax.yaml
   :language: yaml
   :linenos:
   
Configuration options
"""""""""""""""""""""

The YAML configuration is a dictionary, with the following keys : `default`, `cells`, `packages`. There can be additionnal keys, used by somme :mod:`cell plugins <pypimonitor.cell>`  (at the time I am writing this, no plugin uses this). 

In the following example, the YAML configuration file is reffered as a Python :class:`dict`.

.. _celloption:

``cell`` option
^^^^^^^^^^^^^^^

The cell plugin used to render column `foo` of line `mypackage` is the plugin having as keyword (by order of precedence):

- value of `config['packages']['mypackage']['foo']['cell']` (to explicitely set the plugin to use for a single package);
- value of `config['default']['foo']['cell']` (to explicitely set the default plugin to use for a whole column);
- `foo` (at last, the column reference is used as the cell plugin keyword);
- the default :ref:`error` plugin.


``packages``
^^^^^^^^^^^^

This is a dictionary of dictionaries: the keys are the pypi package names, and the values are either nothing (if the default values are sufficient to process this package), or a dictionary of cell options: the keys of this "sub-dictionary" are the cell names, and the values are dictionary of cell options.

For instance, in the :ref:`example <yamlexample>`:

* package `fullcoverage` uses only default values, so it is mentionned without options;
* however, package `sphinxcontrib-packages` has, as a value, ``{'readthedocs': {'slug': 'packages'}}``, which means that options ``{'slug': 'packages'}`` is passed to the :ref:`Readthedocs` plugin (which means that the documentation URL is http://packages.readthedocs.io instead of http://sphinxcontrib-packages.readthedocs.io).

.. _configcells:

``cells``
^^^^^^^^^
If `config['cells']` is not defined, the list of columns is deduced from the cells used in the package options. This option has two purposes:

* explicitely set the list of columns (for instance, in :ref:`the example <yamlexample>`, since `color` is never referenced in package options (every package use the default options for this plugin), it would not appear in the generated HTML file if it were not present in the `config['cells']` list);
* set the order of those columns.

The values of this list can be:

* a :mod:`cell plugin <pypimonitor.cell>` keyword, in which case, unless :ref:`otherwise specified <celloption>`, the plugin used to render this cell is the corresponding plugin, and the title of the column is the title of this plugin;
* or an arbitrary text, in which case each package has to :ref:`explicitely define <configcells>` its cell plugin for this cell, or the cell plugin to use has to be defined in the ``default`` value (see :ref:`default`).

.. _default:

``default``
^^^^^^^^^^^

Default cell parameters can be set, and apply to every package (unless a different parameter is set specifically for this program). This option is a dictonary, where:

* keys are the column names (as referenced in the ``cells`` option);
* values are dictionary of options, which are applied to every package, unless the package explicitely specified a different option.

For instance, in :ref:`the example <yamlexample>` the ``default`` configuration contains::

  CI:
    cell: gitlabci
    server: http://framagit.org
    user: spalax

This means that, unless a package specifies something else:

* the plugin used to render the cells is :ref:`gitlabci`;
* the gitlab server is http://framagit.org (and not the plugin default http://gitlab.com);
* the user is `spalax <http://framagit.org/spalax>`_.
