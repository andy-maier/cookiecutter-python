Cookiecutter template for Python projects
=========================================

This is a template for the popular
`cookiecutter <https://cookiecutter.readthedocs.io/en/latest/>`_ project.

The generated project is a Python project that supports:

* Make - for encapsulating commands for the current active Python environment
* Tox - for creating multiple virtual Python environments and testing therein
* Testing on Travis CI & Appveyor CI
* Building docs for deployment to RTD


Usage
-----

If you don't have cookiecutter installed, issue (ideally in a virtual Python
environment):

.. code-block:: bash

    $ pip install cookiecutter

In the directory where you want the subdirectory for the new Python project to
be created, issue:

.. code-block:: bash

    $ cookiecutter https://github.com/andy-maier/cookiecutter-python

You will be prompted for the following input variables:

* project_name: A project name for use in titles, docs, etc. May contain blanks
  and mixed case.
* short_description: A short (one-line) description of the project.
* package_name: The name of the package on PyPI and of the Python package to
  import. Should be lower case with no other special characters than
  underscores.
* package_version: Initial package version in M.N.P syntax (the project uses
  semantic versioning).
* github_org: Name of the GitHub organization that contains the project repo.
* github_repo: Name of the GitHub repository within the GitHub organization
* full_name: Full name of the author. Will be used as author and maintainer in
  setup.py
* email: Email address of the author. Will be used as author and maintainer
  email in setup.py
* pypi_username: Username to be used on PyPI. Is needed for badges on the
  README page.
* appveyor_username: Username to be used on PyPI. Is needed for badges on the
  README page.
* command_line_interface: Selection of command line packages that you want to
  use.
* open_source_license: Selection of license that you want to use.

To see which targets the Makefile supports, issue in the new directory:

.. code-block:: bash

    $ make help


License
-------

This cookiecutter template is provided under the
`Apache 2.0 license <LICENSE>`_.
