"""
Tests for running make commands in a repo created with cookiecutter.
"""

import os
import re
import tempfile
import shutil
import venv

import pytest

from ..utils.utils import run_args

# Controls whether the output directory is kept for debugging
KEEP_OUT_DIR = False

# Controls whether the 'make' command output is shown for debugging
SHOW_MAKE = False


TESTCASES_CC_MAKE = [
    # Testcases for test_cc_make()

    # Each testcase is a tuple of:
    # * desc (str): Brief oneline description of the testcase.
    # * input_parms (dict): Non-default input parameters for cookiecutter.
    # * out_dir (str): Relative path name of output directory.
    # * cmd_args (list of str): Command args to run in created repo.
    # * exp_rc (int): Expected exit code of command.
    # * exp_stdout_pattern (str): Regexp pattern for expected command stdout.
    # * exp_stderr_pattern (str): Regexp pattern for expected command stderr.

    (
        "Run make help",
        {},
        "new_new-project",
        ["make", "help"],
        0,
        r"Make targets:",
        ""
    ),
    (
        "Run make pip_list",
        {},
        "new_new-project",
        ["make", "pip_list"],
        0,
        r"Makefile: Python packages as seen by make",
        ""
    ),
    (
        "Run make install",
        {},
        "new_new-project",
        ["make", "install"],
        0,
        r"Makefile: install done",
        ""
    ),
    (
        "Run make check",
        {},
        "new_new-project",
        ["make", "check"],
        0,
        r"Makefile: check done",
        ""
    ),
    (
        "Run make unittest",
        {},
        "new_new-project",
        ["make", "unittest"],
        0,
        r"Makefile: unittest done",
        ""
    ),
]


@pytest.mark.parametrize(
    "desc, input_parms, out_dir, cmd_args, exp_rc, exp_stdout_pattern, "
    "exp_stderr_pattern",
    TESTCASES_CC_MAKE)
def test_cc_make(
        desc, input_parms, out_dir, cmd_args, exp_rc, exp_stdout_pattern,
        exp_stderr_pattern):
    # pylint: disable=unused-argument
    """
    Test running make commands in a repo created by cookiecutter.
    """

    # The template directory, using the git submodule
    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", ".."))

    try:

        # Create a named temporary directory
        tmp_dir = tempfile.mkdtemp(prefix="test_cc_make_")

        # The repo main directory
        out_dir = os.path.join(tmp_dir, out_dir)

        # Create the repo using cookiecutter
        parm_args = [f"{name}={value}" for name, value in input_parms.items()]
        result = run_args(
            args=["cookiecutter", "--no-input", template_dir] + parm_args,
            cwd=tmp_dir, check=True)

        # Initialize the repo for git and create a first commit so that
        # author creation works
        run_args(args=["git", "init"],
                 cwd=out_dir, check=True)
        run_args(args=["git", "config", "user.email", "ci@example.com"],
                 cwd=out_dir, check=True)
        run_args(args=["git", "config", "user.name", "CI"],
                 cwd=out_dir, check=True)
        run_args(args=["git", "add", "--all"],
                 cwd=out_dir, check=True)
        run_args(args=["git", "commit", "-asm", "Initial commit"],
                 cwd=out_dir, check=True)

        # Create a virtual Python environment since the 'make' commands install
        # Python packages
        venv_dir = os.path.join(tmp_dir, ".venv")
        venv.create(venv_dir, with_pip=True, clear=True)

        # Determine the code directory of the virtual Python environment
        venv_bin_dir = os.path.join(venv_dir, "bin")
        if not os.path.isdir(venv_bin_dir):
            venv_bin_dir = os.path.join(venv_dir, "Scripts")  # On Windows
        if not os.path.isdir(venv_bin_dir):
            raise AssertionError(
                "Cannot find code directory in virtual Python environment "
                f"directory: {venv_dir}")

        # Prepare the environment for running the 'make' command
        env = dict(os.environ)

        # "Activate" the virtual Python environment
        env["PATH"] = f"{venv_bin_dir}{os.pathsep}{env['PATH']}"
        env["VIRTUAL_ENV"] = str(venv_dir)

        # Prevent the parent Python interpreter from leaking in
        env["PYTHONHOME"] = ""

        # Remove our own test env vars from the environment, since they are not
        # meant for the 'make test' commands of the created repo.
        if env.get("TESTOPTS"):
            del env["TESTOPTS"]
        if env.get("TESTCASES"):
            del env["TESTCASES"]

        # Remove any Python/Pip command overrides from the environment, since
        # the virtual Python environment provides the default commands.
        if env.get("PYTHON_CMD"):
            del env["PYTHON_CMD"]
        if env.get("PIP_CMD"):
            del env["PIP_CMD"]

        # Set RUN_TYPE to 'normal' to have tolerant handling of safety issues.
        env["RUN_TYPE"] = "normal"

        # PACKAGE_LEVEL is passed through.

        # Run the 'make' command to be tested
        result = run_args(args=cmd_args, cwd=out_dir, timeout=600, env=env)

        if SHOW_MAKE:
            cmd_str = " ".join(cmd_args)
            print(f"\nDebug: Output of '{cmd_str}':")
            print(result.stdout)
            print(f"Debug: End of output of '{cmd_str}'")

        assert result.returncode == exp_rc, (
            f"Unexpected exit code: {result.returncode} (expected: {exp_rc})\n"
            f"Stdout:\n{result.stdout}\n"
            f"Stderr:\n{result.stderr}\n"
        )

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

    finally:
        if KEEP_OUT_DIR:
            print(f"Debug: Ouput directory kept for debugging: {tmp_dir}")
        else:
            shutil.rmtree(tmp_dir, ignore_errors=True)
