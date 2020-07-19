#!/usr/bin/env python
"""
Python setup script for the {{ cookiecutter.project_name }} project.
"""

import sys
import os
import re
# setuptools needs to be imported before distutils in order to work.
import setuptools
from distutils import log  # pylint: disable=wrong-import-order


def get_version(version_file):
    """
    Execute the specified version file and return the value of the __version__
    global variable that is set in the version file.

    Note: Make sure the version file does not depend on any packages in the
    requirements list of this package (otherwise it cannot be executed in
    a fresh Python environment).
    """
    with open(version_file, 'r') as fp:
        version_source = fp.read()
    _globals = {}
    exec(version_source, _globals)  # pylint: disable=exec-used
    return _globals['__version__']


def get_requirements(requirements_file):
    """
    Parse the specified requirements file and return a list of its non-empty,
    non-comment lines. The returned lines are without any trailing newline
    characters.
    """
    with open(requirements_file, 'r') as fp:
        lines = fp.readlines()
    reqs = []
    for line in lines:
        line = line.strip('\n')
        if not line.startswith('#') and line != '':
            reqs.append(line)
    return reqs


def read_file(a_file):
    """
    Read the specified file and return its content as one string.
    """
    with open(a_file, 'r') as fp:
        content = fp.read()
    return content


class PytestCommand(setuptools.Command):
    """
    Base class for setup.py commands for executing tests for this package
    using pytest.

    Note on the class name: Because distutils.dist._show_help() shows the class
    name for the setup.py command name instead of invoking get_command_name(),
    the classes that get registered as commands must have the command name.
    """

    description = None  # Set by subclass
    my_test_dirs = None  # Set by subclass

    user_options = [
        (
            'pytest-options=',  # '=' indicates it requires an argument
            None,  # no short option
            "additional options for pytest, as one argument"
        ),
    ]

    def initialize_options(self):
        """
        Standard method called by setup to initialize options for the command.
        """
        # pylint: disable=attribute-defined-outside-init
        self.test_opts = None
        self.test_dirs = None
        self.pytest_options = None
        # pylint: enable=attribute-defined-outside-init

    def finalize_options(self):
        """
        Standard method called by setup to finalize options for the command.
        """
        # pylint: disable=attribute-defined-outside-init
        self.test_opts = [
            '--color=yes',
            '-s',
            '-W', 'default',
            '-W', 'ignore::PendingDeprecationWarning',
        ]
        if sys.version_info[0] == 3:
            self.test_opts.extend([
                '-W', 'ignore::ResourceWarning',
            ])
        self.test_dirs = self.my_test_dirs
        # pylint: enable=attribute-defined-outside-init

    def run(self):
        """
        Standard method called by setup to execute the command.
        """

        # deferred import so install does not depend on it
        import pytest  # pylint: disable=import-outside-toplevel

        args = self.test_opts
        if self.pytest_options:
            args.extend(self.pytest_options.split(' '))
        args.extend(self.test_dirs)

        if self.dry_run:
            self.announce("Dry-run: pytest {}".format(' '.join(args)),
                          level=log.INFO)
            return 0

        self.announce("pytest {}".format(' '.join(args)),
                      level=log.INFO)
        rc = pytest.main(args)
        return rc


class test(PytestCommand):
    # pylint: disable=invalid-name
    """
    Setup.py command for executing unit and function tests.
    """
    description = "{{ cookiecutter.project_name }}: Run unit tests using pytest"
    my_test_dirs = ['tests/unittest']


class end2endtest(PytestCommand):
    # pylint: disable=invalid-name
    """
    Setup.py command for executing end2end tests.
    """
    description = "{{ cookiecutter.project_name }}: Run end2end tests using pytest"
    my_test_dirs = ['tests/end2endtest']

    def finalize_options(self):
        PytestCommand.finalize_options(self)  # old-style class
        self.test_opts.extend([
            '-v', '--tb=short',
        ])


# pylint: disable=invalid-name
requirements = get_requirements('requirements.txt')
install_requires = [req for req in requirements
                    if req and not re.match(r'[^:]+://', req)]
dependency_links = [req for req in requirements
                    if req and re.match(r'[^:]+://', req)]
test_requirements = get_requirements('test-requirements.txt')

package_version = get_version(os.path.join('{{ cookiecutter.package_name }}', '_version.py'))

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

# Docs on setup():
# * https://docs.python.org/2.7/distutils/apiref.html?
#   highlight=setup#distutils.core.setup
# * https://setuptools.readthedocs.io/en/latest/setuptools.html#
#   new-and-changed-setup-keywords
setuptools.setup(
    name='{{ cookiecutter.package_name }}',
    version=package_version,
    packages=[
        '{{ cookiecutter.package_name }}',
    ],
    include_package_data=True,  # Includes MANIFEST.in files into sdist (only)
    scripts=[
        # add any scripts
    ],
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={
        "test": test_requirements,
    },
    cmdclass={
        'test': test,
        'end2endtest': end2endtest,
    },
    description="{{ cookiecutter.short_description }}",
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    maintainer="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    maintainer_email='{{ cookiecutter.email }}',
    url='https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.github_repo }}',
    project_urls={
        'Bug Tracker': 'https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.github_repo }}/issues',
        'Documentation': 'https://{{ cookiecutter.package_name }}.readthedocs.io/en/latest/',
        'Source Code': 'https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.github_repo }}',
    },
{%- if cookiecutter.command_line_interface != 'None' %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.package_name }}={{ cookiecutter.package_name }}.cli:main',
        ],
    },
{%- endif %}

    options={'bdist_wheel': {'universal': True}},
    zip_safe=True,  # This package can safely be installed from a zip file
    platforms='any',

    # Keep these Python versions in sync with {{ cookiecutter.package_name }}/__init__.py
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
