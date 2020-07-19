{{ cookiecutter.project_name }} - {{ cookiecutter.short_description }}
===============================

.. image:: https://badge.fury.io/py/{{ cookiecutter.package_name }}.svg
    :target: https://pypi.python.org/pypi/{{ cookiecutter.package_name }}/
    :alt: Version on Pypi

.. image:: https://travis-ci.org/{{ cookiecutter.github_org }}/{{ cookiecutter.github_repo }}.svg?branch=master
    :target: https://travis-ci.org/github/{{ cookiecutter.github_org }}/{{ cookiecutter.github_repo }}/builds
    :alt: Travis test status (master)

.. # Update the URL in the Appveyor image link below to match the
.. # "SVG branchimage URL" from the "master branch status badge" section on
.. # the Settings -> Badges page of the project on Appveyor.
.. image:: https://ci.appveyor.com/api/projects/status/UPDATE-THIS/branch/master?svg=true
    :target: https://ci.appveyor.com/project/{{ cookiecutter.appveyor_username }}/{{ cookiecutter.github_repo }}/history
    :alt: Appveyor test status (master)

.. image:: https://readthedocs.org/projects/{{ cookiecutter.package_name }}/badge/?version=latest
    :target: https://readthedocs.org/projects/{{ cookiecutter.package_name }}/builds/
    :alt: Docs build status (master)

.. image:: https://coveralls.io/repos/github/{{ cookiecutter.github_org }}/{{ cookiecutter.github_repo }}/badge.svg?branch=master
    :target: https://coveralls.io/github/{{ cookiecutter.github_org }}/{{ cookiecutter.github_repo }}?branch=master
    :alt: Test coverage (master)


Overview
--------

TBD

Installation
------------

To install the latest released version of the {{ cookiecutter.package_name }}
package into your active Python environment:

.. code-block:: bash

    $ pip install {{ cookiecutter.package_name }}

This will also install any prerequisite Python packages.

For more details and alternative ways to install, see
`Installation`_.

.. _Installation: https://{{ cookiecutter.package_name }}.readthedocs.io/en/stable/intro.html#installation

Documentation
-------------

* `Documentation for latest released version <https://{{ cookiecutter.package_name }}.readthedocs.io/en/stable/>`_

Change History
--------------

* `Change history for latest released version <https://{{ cookiecutter.package_name }}.readthedocs.io/en/stable/changes.html>`_

Quick Start
-----------

The following simple example script lists the namespaces and the Interop
namespace in a particular WBEM server:

.. code-block:: python

    #!/usr/bin/env python

    import {{ cookiecutter.package_name }}

    ... (tbd) ...

Contributing
------------

For information on how to contribute to the
{{ cookiecutter.project_name }} project, see
`Contributing <https://{{ cookiecutter.package_name }}.readthedocs.io/en/stable/development.html#contributing>`_.


License
-------

The {{ cookiecutter.project_name }} project is provided under the
`{{ cookiecutter.open_source_license }} <https://raw.githubusercontent.com/{{ cookiecutter.github_org }}/{{ cookiecutter.github_repo }}/master/LICENSE>`_.
