"""
cookiecutter hook script that runs after the project has been created.

The script runs with the generated project directory as its current directory.

The script file itself is a Jinja2-rendered template that has access to the
cookiecutter variables.
"""

import os
import shutil

# Files that will be removed when the corresponding cookiecutter variable
# indicates the feature is not enabled.
# Path names must be relative to the project main directory.
REMOVE_FILES = {
    "with_changelog": ["changes", "towncrier.toml"],
    "with_readthedocs": ["docs", ".readthedocs.yaml"],
    "with_jupyter_notebook": [],
    "with_install_test": ["tests/install"],
    "with_end2end_test": ["tests/end2end"],
    "with_slack_notification": [],
    "always": [".git"],
}

# The conditional cookiecutter variables
VARIABLES = {
    "with_changelog": "{[ cookiecutter.with_changelog ]}",
    "with_readthedocs": "{[ cookiecutter.with_readthedocs ]}",
    "with_jupyter_notebook": "{[ cookiecutter.with_jupyter_notebook ]}",
    "with_install_test": "{[ cookiecutter.with_install_test ]}",
    "with_end2end_test": "{[ cookiecutter.with_end2end_test ]}",
    "with_slack_notification": "{[ cookiecutter.with_slack_notification ]}",
    "always": "No",
}

# Remove the files for the features that are disabled
for var, files in REMOVE_FILES.items():
    if VARIABLES[var].lower() != "yes":
        for f in files:
            path = os.path.join(os.getcwd(), f)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
