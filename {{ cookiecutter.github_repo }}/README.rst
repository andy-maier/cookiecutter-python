{{ cookiecutter.project_name }} - {{ cookiecutter.short_description }}
===============================

.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.package_name }}.svg
    :target: https://pypi.python.org/pypi/{{ cookiecutter.package_name }}/
    :alt: Version on Pypi

.. # .. image:: https://img.shields.io/pypi/dm/{{ cookiecutter.package_name }}.svg
.. #     :target: https://pypi.python.org/pypi/{{ cookiecutter.package_name }}/
.. #     :alt: Pypi downloads

.. image:: https://travis-ci.org/{{ cookiecutter.package_name }}/{{ cookiecutter.package_name }}.svg?branch=master
    :target: https://travis-ci.org/{{ cookiecutter.package_name }}/{{ cookiecutter.package_name }}
    :alt: Travis test status (master)

.. image:: https://ci.appveyor.com/api/projects/status/i022iaeu3dao8j5x/branch/master?svg=true
    :target: https://ci.appveyor.com/project/{{ cookiecutter.appveyor_username }}/{{ cookiecutter.package_name }}
    :alt: Appveyor test status (master)

.. image:: https://readthedocs.org/projects/{{ cookiecutter.package_name }}/badge/?version=latest
    :target: https://{{ cookiecutter.package_name }}.readthedocs.io/en/latest/
    :alt: Docs build status (master)

.. image:: https://img.shields.io/coveralls/{{ cookiecutter.package_name }}/{{ cookiecutter.package_name }}.svg
    :target: https://coveralls.io/r/{{ cookiecutter.package_name }}/{{ cookiecutter.package_name }}
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
