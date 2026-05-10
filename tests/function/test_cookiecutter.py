"""
Tests with using cookiecutter.
"""

import os
import re
import subprocess
import tempfile
import shutil

import pytest


# Controls whether the output directory is kept for debugging
KEEP_OUT_DIR = False

# Controls whether debug messages are displayed
DEBUG = False


def path_info(file_path):
    """
    Return information about the existence of the specified file path and
    its parent directories until one exists.
    """
    lines = ""
    if os.path.isfile(file_path):
        lines += f"path_info: File exists: {file_path}\n"
    elif os.path.isdir(file_path):
        lines += f"path_info: Directory exists: {file_path}\n"
    else:
        lines += f"path_info: Does not exist: {file_path}\n"
        parent_path = os.path.dirname(file_path)
        if parent_path != file_path:
            lines += path_info(parent_path)
    return lines


TESTCASES_CC_CREATE = [
    # Testcases for test_cc_create()

    # Each testcase is a tuple of:
    # * desc (str): Brief oneline description of the testcase.
    # * input_parms (dict): Non-default input paraneters for cookiecutter.
    # * exp_out_dir (str): Path names of expected output directory.
    # * exp_files_present (list of str): Path names of files that are expected
    #   to exist in case of success.
    # * exp_files_absent (list of str): Path names of files that are expected
    #   to not exist in case of success.
    # * exp_dirs_present (list of str): Path names of directories that are
    #   expected to exist in case of success.
    # * exp_dirs_absent (list of str): Path names of files that are expected
    #   to not exist in case of success.
    # * exp_lines_present (dict of (path, list of str)): Regexp pattern of
    #   lines that must be present in certain files, in case of success.
    # * exp_lines_absent (dict of (path, list of str)): Regexp pattern of
    #   lines that must be absent in certain files, in case of success.
    # * exp_rc (int): Expected exit code of cookiecutter.
    # * exp_stdout_pattern (str): Regexp pattern for expected stdout.
    # * exp_stderr_pattern (str): Regexp pattern for expected stderr.

    (
        "Test conditionals: Defaults",
        {},
        "new_new-project",
        [
            "towncrier.toml",  # with_changelog
            ".readthedocs.yaml",  # with_readthedocs
            "requirements-rtd.txt",  # with_readthedocs
        ],
        [
            ".git",  # always
        ],
        [
            "changes",  # with_changelog
            "docs",  # with_readthedocs
            "tests/end2end",  # with_end2end_test
            "tests/install",  # with_install_test
        ],
        [],
        {
            "Makefile": [
                r"^doc_build_dir :=",  # with_readthedocs
                r"^ +\$\(wildcard \$\(doc_conf_dir\)/notebooks/\*\.ipynb\) \\$",
                # with_readthedocs+with_jupyter_notebook
                r"^test_end2end_py_files :=",  # with_end2end_test
                r"^ +\$\(test_end2end_py_files\) \\$",  # with_end2end_test
                r"^ +\$\(doc_conf_dir\)/conf\.py \\$",  # with_readthedocs
                r"^ +\$\(wildcard docs/notebooks/\*\.py\) \\$",
                # with_jupyter_notebook
                r"^ +jupyter \\$",  # with_jupyter_notebook
                r"^ +notebook \\$",  # with_jupyter_notebook
                r"^ +sphinx \\$",  # with_readthedocs
                r"^ +towncrier \\$",  # with_changelog
                r'^\t@echo " +installtest ',  # with_install_test
                r'^\t@echo " +builddoc ',  # with_readthedocs
                r'^\t@echo " +doclinkcheck ',  # with_readthedocs
                r'^\t@echo " +end2end ',  # with_end2end_test
                r"^installtest: ",  # with_install_test
                r"^end2end: ",  # with_end2end_test
                r"^builddoc: ",  # with_readthedocs
                r"^\trm -rf \$\(doc_build_dir\)",  # with_readthedocs
                r"^\ttowncrier build",  # with_changelog
            ],
            "INSTALL.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "README.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "pyproject.toml": [
                "^Documentation = ",  # with_readthedocs
                "^Changelog = ",  # with_readthedocs
            ],
            "docs/changes.rst": [
                r"^.. towncrier start",  # with_changelog
            ],
            "docs/development.rst": [
                r" +\+-- end2end ",  # with_end2end_test
                r" +\+-- install ",  # with_install_test
                r" +(\$ )?make end2endtest",  # with_end2end_test
            ],
            "requirements-develop.txt": [
                r"^Sphinx>=",  # with_readthedocs
                r"^towncrier>=",  # with_changelog
                r"^notebook>=",  # with_jupyter_notebook
            ],
            "minimum-constraints-develop.txt": [
                r"^Sphinx==",  # with_readthedocs
                r"^towncrier==",  # with_changelog
                r"^notebook==",  # with_jupyter_notebook
            ],
        },
        {
            "INSTALL.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "README.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
        },
        0,
        "",
        ""
    ),
    (
        "Test conditionals: Defaults + with_readthedocs=No "
        "(implies with_changelog=No)",
        {
            "with_readthedocs": "No",
        },
        "new_new-project",
        [
        ],
        [
            ".git",  # always
            ".readthedocs.yaml",  # with_readthedocs
            "requirements-rtd.txt",  # with_readthedocs
            "towncrier.toml",  # with_changelog
        ],
        [
            "tests/end2end",  # with_end2end_test
            "tests/install",  # with_install_test
        ],
        [
            "changes",  # with_changelog
            "docs",  # with_readthedocs
        ],
        {
            "Makefile": [
                r"^test_end2end_py_files :=",  # with_end2end_test
                r"^ +\$\(test_end2end_py_files\) \\$",  # with_end2end_test
                r"^ +\$\(wildcard docs/notebooks/\*\.py\) \\$",
                # with_jupyter_notebook
                r"^ +jupyter \\$",  # with_jupyter_notebook
                r"^ +notebook \\$",  # with_jupyter_notebook
                r'^\t@echo " +installtest ',  # with_install_test
                r'^\t@echo " +end2end ',  # with_end2end_test
                r"^installtest: ",  # with_install_test
                r"^end2end: ",  # with_end2end_test
            ],
            "INSTALL.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "README.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "requirements-develop.txt": [
                r"^notebook>=",  # with_jupyter_notebook
            ],
            "minimum-constraints-develop.txt": [
                r"^notebook==",  # with_jupyter_notebook
            ],
        },
        {
            "Makefile": [
                r"^doc_build_dir :=",  # with_readthedocs
                r"^ +\$\(doc_conf_dir\)/conf\.py \\$",  # with_readthedocs
                r"^ +sphinx \\$",  # with_readthedocs
                r'^\t@echo " +builddoc ',  # with_readthedocs
                r'^\t@echo " +doclinkcheck ',  # with_readthedocs
                r"^builddoc: ",  # with_readthedocs
                r"^\trm -rf \$\(doc_build_dir\)",  # with_readthedocs
                r"^ +\$\(wildcard \$\(doc_conf_dir\)/notebooks/\*\.ipynb\) \\$",
                # with_readthedocs+with_jupyter_notebook
                r"^ +towncrier \\$",  # with_changelog
                r"^\ttowncrier build",  # with_changelog
            ],
            "INSTALL.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "README.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "pyproject.toml": [
                "^Documentation = ",  # with_readthedocs
                "^Changelog = ",  # with_readthedocs
            ],
            "requirements-develop.txt": [
                r"^Sphinx>=",  # with_readthedocs
                r"^towncrier>=",  # with_changelog
            ],
            "minimum-constraints-develop.txt": [
                r"^Sphinx==",  # with_readthedocs
                r"^towncrier==",  # with_changelog
            ],
        },
        0,
        "",
        ""
    ),
    (
        "Test conditionals: Defaults + with_changelog=No",
        {
            "with_changelog": "No",
        },
        "new_new-project",
        [
            ".readthedocs.yaml",  # with_readthedocs
            "requirements-rtd.txt",  # with_readthedocs
        ],
        [
            ".git",  # always
            "towncrier.toml",  # with_changelog
        ],
        [
            "docs",  # with_readthedocs
            "tests/end2end",  # with_end2end_test
            "tests/install",  # with_install_test
        ],
        [
            "changes",  # with_changelog
        ],
        {
            "Makefile": [
                r"^ +\$\(wildcard \$\(doc_conf_dir\)/notebooks/\*\.ipynb\) \\$",
                # with_readthedocs+with_jupyter_notebook
                r"^doc_build_dir :=",  # with_readthedocs
                r"^ +\$\(doc_conf_dir\)/conf\.py \\$",  # with_readthedocs
                r"^ +sphinx \\$",  # with_readthedocs
                r'^\t@echo " +builddoc ',  # with_readthedocs
                r'^\t@echo " +doclinkcheck ',  # with_readthedocs
                r"^builddoc: ",  # with_readthedocs
                r"^\trm -rf \$\(doc_build_dir\)",  # with_readthedocs
                r"^test_end2end_py_files :=",  # with_end2end_test
                r"^ +\$\(test_end2end_py_files\) \\$",  # with_end2end_test
                r"^ +\$\(wildcard docs/notebooks/\*\.py\) \\$",
                # with_jupyter_notebook
                r"^ +jupyter \\$",  # with_jupyter_notebook
                r"^ +notebook \\$",  # with_jupyter_notebook
                r'^\t@echo " +installtest ',  # with_install_test
                r'^\t@echo " +end2end ',  # with_end2end_test
                r"^installtest: ",  # with_install_test
                r"^end2end: ",  # with_end2end_test
            ],
            "INSTALL.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "README.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "pyproject.toml": [
                "^Documentation = ",  # with_readthedocs
                "^Changelog = ",  # with_readthedocs
            ],
            "docs/changes.rst": [
            ],
            "docs/development.rst": [
                r" +\+-- end2end ",  # with_end2end_test
                r" +\+-- install ",  # with_install_test
                r" +(\$ )?make end2endtest",  # with_end2end_test
            ],
            "requirements-develop.txt": [
                r"^Sphinx>=",  # with_readthedocs
                r"^notebook>=",  # with_jupyter_notebook
            ],
            "minimum-constraints-develop.txt": [
                r"^Sphinx==",  # with_readthedocs
                r"^notebook==",  # with_jupyter_notebook
            ],
        },
        {
            "Makefile": [
                r"^ +towncrier \\$",  # with_changelog
                r"^\ttowncrier build",  # with_changelog
            ],
            "INSTALL.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "README.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "docs/changes.rst": [
                r"^.. towncrier start",  # with_changelog
            ],
            "requirements-develop.txt": [
                r"^towncrier>=",  # with_changelog
            ],
            "minimum-constraints-develop.txt": [
                r"^towncrier==",  # with_changelog
            ],
        },
        0,
        "",
        ""
    ),
    (
        "Test conditionals: Defaults + with_jupyter_notebook=No",
        {
            "with_jupyter_notebook": "No",
        },
        "new_new-project",
        [
            "towncrier.toml",  # with_changelog
            ".readthedocs.yaml",  # with_readthedocs
            "requirements-rtd.txt",  # with_readthedocs
        ],
        [
            ".git",  # always
        ],
        [
            "changes",  # with_changelog
            "docs",  # with_readthedocs
            "tests/end2end",  # with_end2end_test
            "tests/install",  # with_install_test
        ],
        [],
        {
            "Makefile": [
                r"^doc_build_dir :=",  # with_readthedocs
                r"^test_end2end_py_files :=",  # with_end2end_test
                r"^ +\$\(test_end2end_py_files\) \\$",  # with_end2end_test
                r"^ +\$\(doc_conf_dir\)/conf\.py \\$",  # with_readthedocs
                r"^ +sphinx \\$",  # with_readthedocs
                r"^ +towncrier \\$",  # with_changelog
                r'^\t@echo " +installtest ',  # with_install_test
                r'^\t@echo " +builddoc ',  # with_readthedocs
                r'^\t@echo " +doclinkcheck ',  # with_readthedocs
                r'^\t@echo " +end2end ',  # with_end2end_test
                r"^installtest: ",  # with_install_test
                r"^end2end: ",  # with_end2end_test
                r"^builddoc: ",  # with_readthedocs
                r"^\trm -rf \$\(doc_build_dir\)",  # with_readthedocs
                r"^\ttowncrier build",  # with_changelog
            ],
            "INSTALL.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "README.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "pyproject.toml": [
                "^Documentation = ",  # with_readthedocs
                "^Changelog = ",  # with_readthedocs
            ],
            "docs/changes.rst": [
                r"^.. towncrier start",  # with_changelog
            ],
            "docs/development.rst": [
                r" +\+-- end2end ",  # with_end2end_test
                r" +\+-- install ",  # with_install_test
                r" +(\$ )?make end2endtest",  # with_end2end_test
            ],
            "requirements-develop.txt": [
                r"^Sphinx>=",  # with_readthedocs
                r"^towncrier>=",  # with_changelog
            ],
            "minimum-constraints-develop.txt": [
                r"^Sphinx==",  # with_readthedocs
                r"^towncrier==",  # with_changelog
            ],
        },
        {
            "Makefile": [
                r"^ +\$\(wildcard \$\(doc_conf_dir\)/notebooks/\*\.ipynb\) \\$",
                # with_readthedocs+with_jupyter_notebook
                r"^ +\$\(wildcard docs/notebooks/\*\.py\) \\$",
                # with_jupyter_notebook
                r"^ +jupyter \\$",  # with_jupyter_notebook
                r"^ +notebook \\$",  # with_jupyter_notebook
            ],
            "INSTALL.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "README.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "requirements-develop.txt": [
                r"^notebook>=",  # with_jupyter_notebook
            ],
            "minimum-constraints-develop.txt": [
                r"^notebook==",  # with_jupyter_notebook
            ],
        },
        0,
        "",
        ""
    ),
    (
        "Test conditionals: Defaults + with_install_test=No",
        {
            "with_install_test": "No",
        },
        "new_new-project",
        [
            "towncrier.toml",  # with_changelog
            ".readthedocs.yaml",  # with_readthedocs
            "requirements-rtd.txt",  # with_readthedocs
        ],
        [
            ".git",  # always
        ],
        [
            "changes",  # with_changelog
            "docs",  # with_readthedocs
            "tests/end2end",  # with_end2end_test
        ],
        [
            "tests/install",  # with_install_test
        ],
        {
            "Makefile": [
                r"^doc_build_dir :=",  # with_readthedocs
                r"^ +\$\(wildcard \$\(doc_conf_dir\)/notebooks/\*\.ipynb\) \\$",
                # with_readthedocs+with_jupyter_notebook
                r"^test_end2end_py_files :=",  # with_end2end_test
                r"^ +\$\(test_end2end_py_files\) \\$",  # with_end2end_test
                r"^ +\$\(doc_conf_dir\)/conf\.py \\$",  # with_readthedocs
                r"^ +\$\(wildcard docs/notebooks/\*\.py\) \\$",
                # with_jupyter_notebook
                r"^ +jupyter \\$",  # with_jupyter_notebook
                r"^ +notebook \\$",  # with_jupyter_notebook
                r"^ +sphinx \\$",  # with_readthedocs
                r"^ +towncrier \\$",  # with_changelog
                r'^\t@echo " +builddoc ',  # with_readthedocs
                r'^\t@echo " +doclinkcheck ',  # with_readthedocs
                r'^\t@echo " +end2end ',  # with_end2end_test
                r"^end2end: ",  # with_end2end_test
                r"^builddoc: ",  # with_readthedocs
                r"^\trm -rf \$\(doc_build_dir\)",  # with_readthedocs
                r"^\ttowncrier build",  # with_changelog
            ],
            "INSTALL.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "README.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "pyproject.toml": [
                "^Documentation = ",  # with_readthedocs
                "^Changelog = ",  # with_readthedocs
            ],
            "docs/changes.rst": [
                r"^.. towncrier start",  # with_changelog
            ],
            "docs/development.rst": [
                r" +\+-- end2end ",  # with_end2end_test
                r" +(\$ )?make end2endtest",  # with_end2end_test
            ],
            "requirements-develop.txt": [
                r"^Sphinx>=",  # with_readthedocs
                r"^towncrier>=",  # with_changelog
                r"^notebook>=",  # with_jupyter_notebook
            ],
            "minimum-constraints-develop.txt": [
                r"^Sphinx==",  # with_readthedocs
                r"^towncrier==",  # with_changelog
                r"^notebook==",  # with_jupyter_notebook
            ],
        },
        {
            "Makefile": [
                r'^\t@echo " +installtest ',  # with_install_test
                r"^installtest: ",  # with_install_test
            ],
            "INSTALL.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "README.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "docs/development.rst": [
                r" +\+-- install ",  # with_install_test
            ],
        },
        0,
        "",
        ""
    ),
    (
        "Test conditionals: Defaults + with_end2end_test=No",
        {
            "with_end2end_test": "No",
        },
        "new_new-project",
        [
            "towncrier.toml",  # with_changelog
            ".readthedocs.yaml",  # with_readthedocs
            "requirements-rtd.txt",  # with_readthedocs
        ],
        [
            ".git",  # always
        ],
        [
            "changes",  # with_changelog
            "docs",  # with_readthedocs
            "tests/install",  # with_install_test
        ],
        [
            "tests/end2end",  # with_end2end_test
        ],
        {
            "Makefile": [
                r"^doc_build_dir :=",  # with_readthedocs
                r"^ +\$\(wildcard \$\(doc_conf_dir\)/notebooks/\*\.ipynb\) \\$",
                # with_readthedocs+with_jupyter_notebook
                r"^ +\$\(doc_conf_dir\)/conf\.py \\$",  # with_readthedocs
                r"^ +\$\(wildcard docs/notebooks/\*\.py\) \\$",
                # with_jupyter_notebook
                r"^ +jupyter \\$",  # with_jupyter_notebook
                r"^ +notebook \\$",  # with_jupyter_notebook
                r"^ +sphinx \\$",  # with_readthedocs
                r"^ +towncrier \\$",  # with_changelog
                r'^\t@echo " +installtest ',  # with_install_test
                r'^\t@echo " +builddoc ',  # with_readthedocs
                r'^\t@echo " +doclinkcheck ',  # with_readthedocs
                r"^installtest: ",  # with_install_test
                r"^builddoc: ",  # with_readthedocs
                r"^\trm -rf \$\(doc_build_dir\)",  # with_readthedocs
                r"^\ttowncrier build",  # with_changelog
            ],
            "INSTALL.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "README.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "pyproject.toml": [
                "^Documentation = ",  # with_readthedocs
                "^Changelog = ",  # with_readthedocs
            ],
            "docs/changes.rst": [
                r"^.. towncrier start",  # with_changelog
            ],
            "docs/development.rst": [
                r" +\+-- install ",  # with_install_test
            ],
            "requirements-develop.txt": [
                r"^Sphinx>=",  # with_readthedocs
                r"^towncrier>=",  # with_changelog
                r"^notebook>=",  # with_jupyter_notebook
            ],
            "minimum-constraints-develop.txt": [
                r"^Sphinx==",  # with_readthedocs
                r"^towncrier==",  # with_changelog
                r"^notebook==",  # with_jupyter_notebook
            ],
        },
        {
            "Makefile": [
                r"^test_end2end_py_files :=",  # with_end2end_test
                r"^ +\$\(test_end2end_py_files\) \\$",  # with_end2end_test
                r'^\t@echo " +end2end ',  # with_end2end_test
                r"^end2end: ",  # with_end2end_test
            ],
            "INSTALL.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "README.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "docs/development.rst": [
                r" +\+-- end2end ",  # with_end2end_test
                r" +(\$ )?make end2endtest",  # with_end2end_test
            ],
        },
        0,
        "",
        ""
    ),
    (
        "Test conditionals: Defaults + with_slack_notification=No",
        {
            "with_slack_notification": "No",
        },
        "new_new-project",
        [
            "towncrier.toml",  # with_changelog
            ".readthedocs.yaml",  # with_readthedocs
            "requirements-rtd.txt",  # with_readthedocs
        ],
        [
            ".git",  # always
        ],
        [
            "changes",  # with_changelog
            "docs",  # with_readthedocs
            "tests/end2end",  # with_end2end_test
            "tests/install",  # with_install_test
        ],
        [],
        {
            "Makefile": [
                r"^doc_build_dir :=",  # with_readthedocs
                r"^ +\$\(wildcard \$\(doc_conf_dir\)/notebooks/\*\.ipynb\) \\$",
                # with_readthedocs+with_jupyter_notebook
                r"^test_end2end_py_files :=",  # with_end2end_test
                r"^ +\$\(test_end2end_py_files\) \\$",  # with_end2end_test
                r"^ +\$\(doc_conf_dir\)/conf\.py \\$",  # with_readthedocs
                r"^ +\$\(wildcard docs/notebooks/\*\.py\) \\$",
                # with_jupyter_notebook
                r"^ +jupyter \\$",  # with_jupyter_notebook
                r"^ +notebook \\$",  # with_jupyter_notebook
                r"^ +sphinx \\$",  # with_readthedocs
                r"^ +towncrier \\$",  # with_changelog
                r'^\t@echo " +installtest ',  # with_install_test
                r'^\t@echo " +builddoc ',  # with_readthedocs
                r'^\t@echo " +doclinkcheck ',  # with_readthedocs
                r'^\t@echo " +end2end ',  # with_end2end_test
                r"^installtest: ",  # with_install_test
                r"^end2end: ",  # with_end2end_test
                r"^builddoc: ",  # with_readthedocs
                r"^\trm -rf \$\(doc_build_dir\)",  # with_readthedocs
                r"^\ttowncrier build",  # with_changelog
            ],
            "INSTALL.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "README.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "pyproject.toml": [
                "^Documentation = ",  # with_readthedocs
                "^Changelog = ",  # with_readthedocs
            ],
            "docs/changes.rst": [
                r"^.. towncrier start",  # with_changelog
            ],
            "docs/development.rst": [
                r" +\+-- end2end ",  # with_end2end_test
                r" +\+-- install ",  # with_install_test
                r" +(\$ )?make end2endtest",  # with_end2end_test
            ],
            "requirements-develop.txt": [
                r"^Sphinx>=",  # with_readthedocs
                r"^towncrier>=",  # with_changelog
                r"^notebook>=",  # with_jupyter_notebook
            ],
            "minimum-constraints-develop.txt": [
                r"^Sphinx==",  # with_readthedocs
                r"^towncrier==",  # with_changelog
                r"^notebook==",  # with_jupyter_notebook
            ],
        },
        {
            "INSTALL.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "README.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
        },
        0,
        "",
        ""
    ),
    (
        "Test non-default project name etc",
        {
            "project_name": "Foo",
            "short_description": "This is the Foo project",
            "pypi_package_name": "foo-pypi",
            "python_package_name": "foo_python",
            "github_org": "myorg",
            "github_repo": "myrepo",
            "author_full_name": "Me",
            "author_email": "me@gmx.de",
            "license": "MIT",
        },
        "new_myrepo",
        [],
        [],
        [],
        [],
        {
            "Makefile": [
                r"^pypi_package_name := foo-pypi$",
                r"^python_package_name := foo_python$",
            ],
            "docs/conf.py": [
                r'^project = "Foo"$',
            ],
            "pyproject.toml": [
                r'^name = "foo-pypi"$',
                r'^description = "This is the Foo project"$',
                r'^ +\{name = "Me", email = "me@gmx.de"\}$',
                r'^license = "MIT"$',
                r'^Homepage = "https://github.com/myorg/myrepo"$',
            ],
        },
        {},
        0,
        "",
        ""
    ),
    (
        "Test package_type Command using click",
        {
            "package_type": "Command using click",
        },
        "new_new-project",
        [],
        [],
        [],
        [],
        {
            "INSTALL.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "README.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
        },
        {
            "INSTALL.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "README.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
        },
        0,
        "",
        ""
    ),
    (
        "Test package_type Command using argparse",
        {
            "package_type": "Command using argparse",
        },
        "new_new-project",
        [],
        [],
        [],
        [],
        {
            "INSTALL.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
            "README.md": [
                r"^pipx install ",  # package_type != 'Library'
            ],
        },
        {
            "INSTALL.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
            "README.md": [
                r"^pip install ",  # package_type == 'Library'
            ],
        },
        0,
        "",
        ""
    ),
]


@pytest.mark.parametrize(
    "desc, input_parms, exp_out_dir, exp_files_present, exp_files_absent, "
    "exp_dirs_present, exp_dirs_absent, exp_lines_present, "
    "exp_lines_absent, exp_rc, exp_stdout_pattern, exp_stderr_pattern",
    TESTCASES_CC_CREATE)
def test_cc_create(
        desc, input_parms, exp_out_dir, exp_files_present, exp_files_absent,
        exp_dirs_present, exp_dirs_absent, exp_lines_present,
        exp_lines_absent, exp_rc, exp_stdout_pattern, exp_stderr_pattern):
    # pylint: disable=unused-argument
    """
    Test creation of cookiecutter projects.
    """

    # The template directory, using the git submodule
    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", ".."))

    # Create a named temporary directory
    tmp_dir = tempfile.mkdtemp(prefix="test_cc_create_")

    try:
        parm_args = [f"{name}={value}" for name, value in input_parms.items()]
        args = ["cookiecutter", "--no-input", template_dir] + parm_args
        if DEBUG:
            print(f"Debug: args={args!r}")

        try:
            result = subprocess.run(
                args, cwd=tmp_dir, capture_output=True, text=True, check=False,
                timeout=30)
        except IOError as exc:
            raise AssertionError(
                f"Cannot run command with args: {args}, "
                f"{exc.__class__.__name__}: {exc}")

        assert result.returncode == exp_rc, (
            f"Unexpected exit code: {result.returncode} (expected: {exp_rc})\n"
            f"Stdout:\n{result.stdout}\n"
            f"Stderr:\n{result.stderr}\n"
        )

        # The remaining checks are only performed in case of success.
        if exp_rc == 0:

            if exp_stdout_pattern is None:
                exp_stdout_pattern = ""
            m = re.search(exp_stdout_pattern, result.stdout)
            assert m is not None, (
                "Unexpected stdout:\n"
                f"Expected pattern:\n{exp_stdout_pattern!r}\n"
                f"Actual value:\n{result.stdout!r}\n"
            )

            if exp_stderr_pattern is None:
                exp_stderr_pattern = ""
            m = re.search(exp_stderr_pattern, result.stderr)
            assert m is not None, (
                "Unexpected stderr:\n"
                f"Expected pattern:\n{exp_stderr_pattern!r}\n"
                f"Actual value:\n{result.stderr!r}\n"
            )

            out_dir = os.path.join(tmp_dir, exp_out_dir)
            assert os.path.isdir(out_dir), (
                f"Expected output directory does not exist: {out_dir!r}\n"
                f"{path_info(out_dir)}"
            )

            for fn in exp_files_present:
                fp = os.path.join(out_dir, fn)
                assert os.path.isfile(fp), (
                    f"File expected to be present is missing: {fn!r}\n"
                    f"{path_info(fp)}"
                )

            for fn in exp_files_absent:
                fp = os.path.join(out_dir, fn)
                assert not os.path.exists(fp), (
                    f"File expected to be absent exists: {fn!r}\n"
                    f"{path_info(fp)}"
                )

            for fn in exp_dirs_present:
                fp = os.path.join(out_dir, fn)
                assert os.path.isdir(fp), (
                    f"Directory expected to be present is missing: {fn!r}\n"
                    f"{path_info(fp)}"
                )

            for fn in exp_dirs_absent:
                fp = os.path.join(out_dir, fn)
                assert not os.path.exists(fp), (
                    f"Directory expected to be absent exists: {fn!r}\n"
                    f"{path_info(fp)}"
                )

            for fn, exp_lines in exp_lines_present.items():
                fp = os.path.join(out_dir, fn)
                assert os.path.isfile(fp), (
                    f"File for checking lines is missing: {fn!r}\n"
                    f"{path_info(fp)}"
                )
                with open(fp, encoding="utf-8") as f:
                    content = f.read()
                for exp_pattern in exp_lines:
                    m = re.search(exp_pattern, content, re.M)
                    assert m is not None, (
                        f"Lines are missing in file {fn!r}:\n"
                        f"Expected pattern to be present:\n{exp_pattern!r}\n"
                    )

            for fn, exp_lines in exp_lines_absent.items():
                fp = os.path.join(out_dir, fn)
                assert os.path.isfile(fp), (
                    f"File for checking lines is missing: {fn!r}\n"
                    f"{path_info(fp)}"
                )
                with open(fp, encoding="utf-8") as f:
                    content = f.read()
                for exp_pattern in exp_lines:
                    m = re.search(exp_pattern, content, re.M)
                    assert m is None, (
                        f"Extra lines found in file {fn!r}:\n"
                        f"Expected pattern to be absent:\n{exp_pattern!r}\n"
                    )

    finally:
        if KEEP_OUT_DIR:
            print(f"Debug: Ouput directory kept for debugging: {tmp_dir}")
        else:
            shutil.rmtree(tmp_dir, ignore_errors=True)
