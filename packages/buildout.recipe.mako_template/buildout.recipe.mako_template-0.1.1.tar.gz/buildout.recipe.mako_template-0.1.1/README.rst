.. image:: https://img.shields.io/pypi/v/buildout.recipe.mako_template.svg
        :target: https://pypi.python.org/pypi/buildout.recipe.mako_template

.. image:: https://img.shields.io/travis/enkidulan/buildout.recipe.mako_template.svg
        :target: https://travis-ci.org/enkidulan/buildout.recipe.mako_template

.. image:: https://api.codeclimate.com/v1/badges/260655c1feb4cf8cd6bb/maintainability
   :target: https://codeclimate.com/github/enkidulan/buildout.recipe.mako_template/maintainability
   :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/260655c1feb4cf8cd6bb/test_coverage
   :target: https://codeclimate.com/github/enkidulan/buildout.recipe.mako_template/test_coverage
   :alt: Test Coverage

*****************************
buildout.recipe.mako_template
*****************************

A buildout recipe for making files out of Mako templates, with focus on
manageability of large number of templates.

The reasons behind creating this 'another' template recipe for buildout are wish of having:

* ``mako`` with all power of python and good scoping in templates,
* simple listing of ``source : destinatoin`` mapping,
* and collision detection.

Recipe Options
==============

* ``files``: list of couples of templates and targets files paths separated by ``:`` symbol.
  It allow to specify if target should be executable, and to ignore a collision.
  Line has following format:

  ``source:target[:is_executable(true or false)[:collision_allowed(just a flag))]]``

* ``directories`` : list of lookup directories of the ``mako`` templates. Templates
  file paths are relative to these directories. (default: ${buildout:directory})

Additional options are simply forwarded to the templates, and options from all the
other parts are made available through ``parts[<part-name>][<option-name>]``.

Minimal Example
===============

``buildout.cfg``:

.. code-block:: ini

    [buildout]
    parts = foo


    [foo]
    recipe = buildout.recipe.mako_template
    author = Me
    files = foo_1.sh.mako : foo_1.sh

``foo_1.sh.mako``:

.. code-block:: mako

    echo Hello ${author}!

Will result in creation of ``foo_1.sh``:

.. code-block:: shell

    echo Hello Me!


Larger Example
==============

.. code-block:: ini

    [buildout]
    parts = docker-compose

    [project]
    name = MyProject

    [docker-compose]
    recipe = buildout.recipe.mako_template
    directories = ${buildout:directory}/templates
    gateway_ports = 8080:8080
    files =
        backend.dockerfile.mako  : .docker/backend.dockerfile
        frontend.dockerfile.mako : .docker/frontend.dockerfile
        gateway.dockerfile.mako  : .docker/gateway.dockerfile
        docker-compose.yaml.mako : docker-compose.yaml

``docker-compose.yaml.mako``:

.. code-block:: mako

    ...
    gateway:
        container_name: ${parts['project']['name']}_gateway
        ports:
          - "${gateway_ports}"
    ...


Collision detection
===================

Cases where one's template target are overridden by another template
are detected automatically. For example, case:

.. code-block:: ini

    files =
        foo_1.sh.mako : foo_1.sh
        foo_2.sh.mako : foo_1.sh  # overwrites ``target`` form above

will result in a build fail with the message:

.. code-block:: bash

    Target collision is detected at 'foo_2.sh.mako : foo_1.sh'


Yet in some cases, it may be a desirable behavior, so it's possible to allow
overwriting by adding ``collision_allowed`` flag.
