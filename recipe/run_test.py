import sys
from subprocess import call
from pathlib import Path

FAIL_UNDER = "63"
COV = ["coverage"]
RUN = ["run", f"--source=schedula", "--branch", "--apend", "-m"]
TEST = ["unittest", "discover", "--start-directory", "src/tests", "--pattern",  "test_*.py"]
HELP_CLI = [
    ["schedula.cli"],
    ["schedula.cli", "form"],
]
REPORT = ["report", "--show-missing", "--skip-covered", f"--fail-under={FAIL_UNDER}"]


if __name__ == "__main__":
    Path("src/tests/utils/test_form.py").unlink()
    sys.exit(
        # run the cli
        any(
            call([*COV, *cli, "--help"])
            for cli in HELP_CLI
        )
        # run the tests
        or call([*COV, *RUN, *TEST])
        # maybe run coverage
        or call([*COV, *REPORT])
    )
