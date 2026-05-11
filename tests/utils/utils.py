"""
Utility functions for testing.
"""

import os
import subprocess


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


def run_args(args, cwd, *, check=False, timeout=30, env=None):
    """
    Execute the args as a child process, capturing stdout and stderr.
    """
    try:
        result = subprocess.run(
            args, cwd=cwd, capture_output=True, text=True, check=check,
            timeout=timeout, env=env)
    except IOError as exc:
        raise AssertionError(
            f"Cannot run command: {args}, "
            f"{exc.__class__.__name__}: {exc}")
    except subprocess.CalledProcessError as exc:
        raise AssertionError(
            f"Cannot run command: {args}, "
            f"{exc.__class__.__name__}: {exc}\n"
            f"stdout: {exc.stdout}\n"
            f"stderr: {exc.stderr}\n")
    return result
