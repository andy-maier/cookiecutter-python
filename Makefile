# Makefile
#
# make command: GNU make
#
# Supported OS platforms:
#     Linux, UNIX, macOS (using the bash shell)
#     Windows with UNIX-like env such as CygWin (using the bash shell)
#     native Windows with CMD.EXE (the Makefile uses 'wsl bash' as a shell)
#     native Windows with WSL (using the bash shell)
#
# The following commands are used:
#     bash internal commands (rm, find, cat, mv, cp, env, sort, ls, if, which, ...)
#     python (can be overridden with PYTHON_CMD env var)
#     pip (can be overridden with PIP_CMD env var)
#     git

# No built-in rules needed:
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:

# Determine the OS platform make runs on.
ifeq ($(OS),Windows_NT)
  ifdef PWD
    PLATFORM := Windows_UNIX
    SHELL := $(shell which bash)
  else
    PLATFORM := Windows_native
    SHELL := wsl bash
  endif
  .SHELLFLAGS := -c
else
  # Values: Linux, UNIX, Darwin
  PLATFORM := $(shell uname -s)
  SHELL := $(shell which bash)
  .SHELLFLAGS := -c
endif

# Python / Pip commands
ifndef PYTHON_CMD
  PYTHON_CMD := python
endif
ifndef PIP_CMD
  PIP_CMD := pip
endif

# Package level
ifndef PACKAGE_LEVEL
  PACKAGE_LEVEL := latest
endif
ifeq ($(PACKAGE_LEVEL),minimum)
  pip_level_opts := -c minimum-constraints-develop.txt
else
  ifeq ($(PACKAGE_LEVEL),latest)
    pip_level_opts := --upgrade --upgrade-strategy eager
  else
    $(error Error: Invalid value for PACKAGE_LEVEL variable: $(PACKAGE_LEVEL))
  endif
endif

# Run type (normal, scheduled, release, local)
ifndef RUN_TYPE
  RUN_TYPE := local
endif

# Python major and minor version as a short identifier
pymn := $(shell $(PYTHON_CMD) -c "import sys; sys.stdout.write(f'py{sys.version_info[0]}{sys.version_info[1]}')")

# Directory with test source files
test_dir := tests

# Source files with test code
test_py_files := \
    $(wildcard $(test_dir)/function/*.py) \
    $(wildcard $(test_dir)/function/*/*.py) \
		$(wildcard $(test_dir)/function/*/*/*.py) \

# Directory for .done files
done_dir := done

# Flake8 config file
flake8_rc_file := .flake8

# Ruff config file
ruff_rc_file := .ruff.toml

# PyLint config file
pylint_rc_file := .pylintrc

# PyLint additional options
pylint_opts := --disable=fixme

# Source files for check (with Flake8, Ruff, PyLint)
check_py_files := \
    $(test_py_files) \

# Packages whose dependencies are checked using pip-missing-reqs
check_reqs_packages := \
    cookiecutter \
    pip_check_reqs \
    pipdeptree \
    pytest \
    flake8 \
    ruff \
    pylint \

# Pytest options
pytest_general_opts := -s --color=yes
ifdef TESTCASES
  pytest_test_opts := $(TESTOPTS) -k '$(TESTCASES)'
else
  pytest_test_opts := $(TESTOPTS)
endif

.PHONY: help
help:
	@echo "Makefile for $(pypi_package_name) project"
	@echo "Package version will be: $(package_version)"
	@echo ""
	@echo "Make targets:"
	@echo "  develop           - Prepare the development environment by installing prerequisites"
	@echo "  flake8            - Run Flake8 on sources"
	@echo "  ruff              - Run Ruff (an alternate lint tool) on sources"
	@echo "  pylint            - Run PyLint on sources"
	@echo "  check_reqs        - Perform missing dependency checks"
	@echo "  test              - Run tests"
	@echo "  all               - Combined target: Do all of the above"
	@echo "  check             - Combined target: flake8, ruff, pylint"
	@echo "  clean             - Remove any temporary files"
	@echo "  clobber           - Remove any temporary files and build products"
	@echo "  platform          - Display the information about the platform as seen by make"
	@echo "  env               - Display the environment as seen by make"
	@echo "  pip_list          - Display the installed Python packages as seen by make"
	@echo ""
	@echo "Environment variables:"
	@echo "  TESTCASES=...     - Testcase filter for pytest -k"
	@echo "  TESTOPTS=...      - Options for pytest"
	@echo "  PACKAGE_LEVEL     - Package level to be used for installing dependent Python"
	@echo "      packages in 'install' and 'develop' targets:"
	@echo "        latest        - Latest package versions available on Pypi"
	@echo "        minimum       - Minimum versions as defined in minimum-constraints*.txt"
	@echo "      Optional, defaults to 'latest'."
	@echo "  PYTHON_CMD=...    - Name of python command. Default: python"
	@echo "  PIP_CMD=...       - Name of pip command. Default: pip"

.PHONY: _always
_always:

.PHONY: all
all: develop flake8 ruff pylint check_reqs test
	@echo "Makefile: $@ done."

.PHONY: check
check: flake8 ruff pylint

.PHONY: platform
platform:
ifeq ($(PLATFORM),Linux)
	@echo "Makefile: Installing ld to get Linux distributions"
	$(PYTHON_CMD) -m pip -q install ld
endif
	@echo "Makefile: Platform information as seen by make:"
	@echo "Platform detected by Makefile: $(PLATFORM)"
	@$(PYTHON_CMD) -c "import platform; print(f'Platform detected by Python: {platform.platform()}')"
	@$(PYTHON_CMD) -c "import platform; print(f'HW platform detected by Python: {platform.machine()}')"
ifeq ($(PLATFORM),Linux)
	@$(PYTHON_CMD) -c "import ld; d=ld.linux_distribution(); print(f'Linux distro detected by ld: {d[0]} {d[1]}')"
endif
	@echo "Shell used for make commands: $(SHELL)"
	@echo "Shell flags used for make commands: $(.SHELLFLAGS)"
	@echo ""
	@echo "Shell version:"
	$(SHELL) --version
	@echo ""
	@echo "Make version: $(MAKE_VERSION)"
	@echo "Python command name: $(PYTHON_CMD)"
	@echo "Python command location: $(shell which $(PYTHON_CMD))"
	@echo "Python version: $(shell $(PYTHON_CMD) --version)"
	@echo "Pip command name: $(PIP_CMD)"
	@echo "Pip command location: $(shell which $(PIP_CMD))"
	@echo "Pip version: $(shell $(PIP_CMD) --version)"

.PHONY: env
env:
	@echo "Makefile: Environment variables as seen by make:"
	env | sort

.PHONY: pip_list
pip_list:
	@echo "Makefile: Python packages as seen by make:"
	$(PIP_CMD) list

.PHONY: develop
develop: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: $@ done."

$(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done: requirements-develop.txt minimum-constraints-develop.txt
	rm -f $@
	@echo "Makefile: Installing development requirements with PACKAGE_LEVEL=$(PACKAGE_LEVEL)"
	$(PYTHON_CMD) -m pip install $(pip_level_opts) -r requirements-develop.txt
	echo "done" >$@
	@echo "Makefile: Done installing development requirements"

.PHONY: flake8
flake8: $(done_dir)/flake8_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: $@ done."

$(done_dir)/flake8_$(pymn)_$(PACKAGE_LEVEL).done: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(flake8_rc_file) $(check_py_files)
	@echo "Makefile: Running Flake8"
	rm -f $@
	flake8 --config $(flake8_rc_file) $(check_py_files)
	echo "done" >$@
	@echo "Makefile: Done running Flake8"

.PHONY: ruff
ruff: $(done_dir)/ruff_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: $@ done."

$(done_dir)/ruff_$(pymn)_$(PACKAGE_LEVEL).done: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(ruff_rc_file) $(check_py_files)
	@echo "Makefile: Running Ruff"
	rm -f $@
	ruff check --unsafe-fixes --config $(ruff_rc_file) $(check_py_files)
	echo "done" >$@
	@echo "Makefile: Done running Ruff"

.PHONY: pylint
pylint: $(done_dir)/pylint_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: $@ done."

$(done_dir)/pylint_$(pymn)_$(PACKAGE_LEVEL).done: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(pylint_rc_file) $(check_py_files)
	@echo "Makefile: Running Pylint"
	rm -f $@
	pylint $(pylint_opts) --rcfile=$(pylint_rc_file) --output-format=text $(check_py_files)
	echo "done" >$@
	@echo "Makefile: Done running Pylint"

.PHONY: check_reqs
check_reqs: $(done_dir)/check_reqs_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: $@ done."

$(done_dir)/check_reqs_$(pymn)_$(PACKAGE_LEVEL).done: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done minimum-constraints-develop.txt
	rm -f $@
ifeq ($(PLATFORM),Windows_native)
# Reason for skipping on Windows is https://github.com/r1chardj0n3s/pip-check-reqs/issues/67
	@echo "Makefile: Warning: Skipping the checking of missing dependencies of site-packages directory on native Windows" >&2
else
	@echo "Makefile: Checking missing dependencies of some development packages in our minimum versions"
	@rc=0; for pkg in $(check_reqs_packages); do dir=$$($(PYTHON_CMD) -c "import $${pkg} as m,os; dm=os.path.dirname(m.__file__); d=dm if not dm.endswith('site-packages') else m.__file__; print(d)"); cmd="pip-missing-reqs $${dir} --requirements-file=minimum-constraints-develop.txt"; echo $${cmd}; $${cmd}; rc=$$(expr $${rc} + $${?}); done; exit $${rc}
	@echo "Makefile: Done checking missing dependencies of some development packages in our minimum versions"
endif
	echo "done" >$@

.PHONY: test
test: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(test_py_files)
	PYTHONPATH=. pytest $(pytest_general_opts) $(pytest_test_opts) $(test_dir)/function
	@echo "Makefile: $@ done."

.PHONY: clean
clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.tmp' -delete
	find . -type f -name 'tmp_*' -delete
	find . -type f -name '.DS_Store' -delete
	find . -type d -name '__pycache__' | xargs -n 1 rm -rf
	find . -type d -name '.pytest_cache' | xargs -n 1 rm -rf
	find . -type d -name '.ruff_cache' | xargs -n 1 rm -rf
	rm -f MANIFEST MANIFEST.in
	rm -rf build .cache
	@echo "Makefile: $@ done."

.PHONY: clobber
clobber: clean
	rm -f $(done_dir)/*.done
	rm -rf htmlcov .tox
	@echo "Makefile: $@ done."
