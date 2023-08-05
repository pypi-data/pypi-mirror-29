About
=====

``mkinxs`` allows you to integrate several ``sphinx`` documentation
projects into one Home Documentation listing them and allowing you to
have cross projects documentation with ``mkdocs``.

Any ``sphinx`` module can be used as long as ``make html`` works and the
built code is in ``your_project/build``

Install
=======

``pip install mkinx``

Getting Started
===============

Start you Home Documentation with

::

    mkinx init your_project

Start the server with

::

    mkinx serve

Optionnaly you can specify a port with ``mkinx serve -s your_port``

Build the documentation with

::

    mkinx build [FLAGS]

Flags being:

::

      -v, --verbose                             verbose flag (Sphinx will stay verbose)
      -A, --all                                 Build doc for all projects
      -F, --force                               force the build, no verification asked
      -o, --only_index                          only build projects listed in the Documentation's Home
      -p, --projects [PROJECTS [PROJECTS ...]]  list of projects to build


