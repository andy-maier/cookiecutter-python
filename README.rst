Cookiecutter template for Python projects
=========================================

This is a template for the popular
`cookiecutter <https://cookiecutter.readthedocs.io/en/latest/>`_ project
for generating a Python project.

The generated Python project features the following:

* Use of GitHub (github.com) as a repository. This only affects links generated
  in the documentation and readme files and can easily be adjusted by you
  to something else after creating the project.
* Use of GNU Make for encapsulating the typical actions such as install,
  test, etc. Each invocation of make operates in the currently active
  Python environment that has previously been activated by the user.
* Use of Tox for running make in a number of virtual Python environments that
  are automatically created by Tox.
* Use of GitHub Actions as a CI system for testing and publishing.
* Use of Sphinx for generating documentation for the Python package, that is
  ready to be published on ReadTheDocs.
* Use of coveralls for reporting and comparing test coverage.
* Use of Python source code checkers: flake8, ruff, pylint.
* Use of Python security checkers: safety, bandit.
* Selection of the license to be used for the new project.
* Support for publishing the package to Pypi and the documentation to ReadTheDocs.
* Use of semantic versioning (M.N.P).

Usage
-----

1.  If you don't have cookiecutter installed yet, install it so that it is
    useable at the OS level (i.e. without requiring a virtual Python
    environment).

    In macOS, install it as an OS-level package:

    .. code-block:: bash

        $ brew install cookiecutter

    On any platform, you can install it as a command that creates its own
    virtual Python environment:

    .. code-block:: bash

        $ pipx install cookiecutter

2.  In the directory where you want the subdirectory for the new Python project
    to be created, issue:

    .. code-block:: bash

        $ cookiecutter https://github.com/andy-maier/cookiecutter-python

    You will be prompted for the following input parameters:

    * ``project_name`` - A project name for use in titles, docs, etc. May contain
      blanks and mixed case.
    * ``short_description`` - A short (one-line) description of the project.
    * ``pypi_package_name`` - The name of the distribution package on Pypi.
      Should be lower case, and dashes (preferred) or underscores can be used
      for word separation.
      Must not contain any other special characters.
    * ``python_package_name`` - The name of the Python package to import.
      Should be lower case with underscores for word separation.
      Must not contain any other special characters.
    * ``package_version`` - Initial package version in M.N.P syntax (the project
      uses semantic versioning).
    * ``github_org`` - Name of the GitHub organization that contains the project
      repo.
    * ``github_repo`` - Name of the GitHub repository within the GitHub
      organization.
    * ``author_full_name`` - Full name of the author. Will be used as author and
      maintainer in the package metadata.
    * ``author_email`` - Email address of the author. Will be used as author and
      maintainer email in the package metadata.
    * ``package_type`` - Selection of the type of package (CLI, library, ...).
    * ``license`` - Selection of the license you want to use (in new PEP 639 format).
    * ``with_readthedocs`` - Choose whether to build docs with Sphinx and publish on ReadTheDocs.org.
    * ``with_changelog`` - Choose whether to build a change log with towncrier (requires with_readthedocs).
    * ``with_jupyter_notebook`` - Choose whether to install Jupyter Notebook.
    * ``with_install_test`` - Choose whether to include ability for install testing.
    * ``with_end2end_test`` - Choose whether to include ability for end2end testing.
    * ``with_slack_notification`` - Choose whether to post CI results on a Slack channel.

    This creates the new project in a subdirectory named ``new_{github_repo}``.

    To see which targets the Makefile supports, issue in the new directory:

    .. code-block:: bash

        $ make help

3. To put that project on GitHub, the following steps represent a proven
   practice. You may choose to do that differently, though.

   The ``{x}`` notation is used to refer to the value of cookiecutter input
   parameter ``x``.

   - On GitHub (https://github.com), create a new repository
     ``{github_org}/{github_repo}``.

   - On GitHub, change the settings of the new repo:

     - In Options:

       - Disallow merge commits.
       - Automatically delete head branches.

   - Clone that repo to your workstation and go to its working directory:

     .. code-block:: bash

         $ git clone git@github.com:{github_org}/{github_repo}.git
         $ cd {github_repo}

   - Set user name and email in your local config of the cloned repo:

     .. code-block:: bash

         $ git config --local --add user.name "{full_name}"
         $ git config --local --add user.email {email}

   - Add, commit and push the generated cookiecutter project to the repo,
     creating a ``main`` branch:

     .. code-block:: bash

         $ git checkout -b main
         $ mv ../new_{github_repo}/* .
         $ git add --all
         $ git commit -sm "Initial project as generated by cookiecutter"
         $ git push --set-upstream origin main

   - On GitHub, go to Settings / Branches and add a branch protection rule for
     branch "main".

   - Testing with GitHub Actions is automatically enabled since a workflow
     file `.github/workflows/test.yml` has been created.

4.  To enable coverage reporting to Coveralls:

    - Have a user on Coveralls (https://coveralls.io), have it authorized
      for your GitHub account, and log in to Coveralls.

    - In the left hand menu, add a repo and turn the new GitHub repo on.

5.  To enable publishing the documentation to ReadTheDocs:

    Perform this step only when cookiecutter parameter ``with_readthedocs`` was
    selected.

    - `Log in to ReadtheDocs.org <https://app.readthedocs.org/accounts/login/>`_
      (or `sign up <https://app.readthedocs.org/accounts/signup/>`_ if you do
      not have a user yet).

    - Go to "My Projects", select "Import a project", sync to get the repo list
      updated, and select the new repo.

    - On the "Project Details" page, change the name of the ReadTheDocs project
      from its default to the Pypi package name.

      Since ReadTheDocs project names are global, that name may be taken
      already, in which case you need to find a new unused name.

    - Adjust the ``<readthedocs_name>`` placeholder to the ReadTheDocs project
      name in the following files:

      - ``README.rst``
      - ``INSTALL.md``
      - ``pyproject.toml``
      - ``docs/development.rst``
      - ``.github/workflows/publish.rst``

6.  To enable publishing the package on Pypi:

    - Have or create a user on Pypi (https://pypi.python.org). The project
      on Pypi is created when the first version of the package is uploaded.

7.  To enable posting CI results on a Slack channel:

    Perform this step only when cookiecutter parameter ``with_slack_notifications``
    was selected.

    1.  Create the Slack incoming webhook

        - Go to https://api.slack.com/apps and click "Create New App".
        - Choose "From scratch", give it a name, and select your workspace.
        - In the left sidebar, go to "Incoming Webhooks".
        - Toggle "Activate Incoming Webhooks" to ON.
        - Click "Add New Webhook to Workspace".
        - Select the channel you want to post to, then click "Allow".
        - Copy the generated webhook URL — it looks like:
          ``https://hooks.slack.com/services/T00000000/B00000000/XXXXXXX``

    2.  Store the webhook URL as a GitHub secret

        - In your GitHub repo, go to Settings → Secrets and variables → Actions.
        - Click "New repository secret".
        - Name it ``SLACK_HOOK`` and paste the generated webhook URL.
        - Click "Add secret".

        Note: The name must be ``SLACK_HOOK`` - this is the name used
        by the notify.yml Actions workflow.

8.  Download the license file:

    The new project uses the license file named ``LICENSE``. By default, that
    file has the "Apache-2.0" license.

    If you selected a different license for the cookiecutter parameter
    "license", download the corresponding license file under the name
    ``LICENSE``. A good starting point for finding the license and download
    links is https://spdx.org/licenses/.

Development of this repo
------------------------

Command to create the submodule::

    git submodule add --name 'new_{[ cookiecutter.github_repo ]}' https://github.com/andy-maier/cookiecutter-python-package 'new_{[ cookiecutter.github_repo ]}'

License
-------

This cookiecutter template is provided under the
`Apache 2.0 license <LICENSE>`_.
