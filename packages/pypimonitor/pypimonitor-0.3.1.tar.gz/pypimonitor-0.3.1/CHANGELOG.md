* pypimonitor 0.3.1 (2018-03-07)

    * Explicit support for python3.5, python3.6.
    * Packages (or anything) can be monitored, even if they are not on Pypi.
    * Spaces surrounding package and user names (provided by the web form) are now ignored.
    * Remove individual charts from generated output (since each line can be disabled by clicking on the legend).
    * It is now possible to set a custom homepage value for any package.
    * Several minor chart improvements.
    * Minor code and documentation improvements.

    -- Louis Paternault <spalax+python@gresille.org>

* pypimonitor 0.3.0 (2016-10-14)

    * New cell plugins:
        * gitlabcicoverage: test coverage for gitlab-CI.

    -- Louis Paternault <spalax+python@gresille.org>

* pypimonitor 0.2.0 (2016-07-03)

    * Takes arguments (which packages to monitor) from a yaml file, or from `pkg=`, `cols=`, `user=`.
    * Now has two modes: command line and web server.
    * Name changed from "pypistats" to "pypimonitor".
    * Use chartsjs.org to draw line charts (was morrisjs before).
    * Package names are now case insensitive.
    * Cell/badges are extensible using plugins.
    * If served by the web server, it is possible to submit a new request using a form.
    * Better error handling
    * New cell types:
        * empty: empty cell;
        * link: hyperlin;
        * html: raw html code;
        * color: show the color of the line charts
        * and more…

    -- Louis Paternault <spalax+python@gresille.org>

* pypimonitor 0.1.0 (2016-03-17)

    * First version. Everything will change in next version.

    -- Louis Paternault <spalax+python@gresille.org>
