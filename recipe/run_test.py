import sys
from subprocess import call
from pathlib import Path

FAIL_UNDER = "63"
COV = ["coverage"]
UNLINK = [
    "src/tests/utils/test_form.py",
]
RUN = ["run", "--source=schedula", "--branch", "--append", "-m"]
TEST = [
    "unittest",
    "discover",
    "--start-directory",
    "src/tests",
    "--pattern",
    "test_*.py",
]
CLI = [
    ["schedula.cli", "--help"],
    ["schedula.cli", "form", "--help"],
]
REPORT = ["report", "--show-missing", "--skip-covered", f"--fail-under={FAIL_UNDER}"]


def do(args: list[str]) -> int:
    print(">>>", *args, flush=True)
    return call(args)


if __name__ == "__main__":
    [Path(p).unlink() for p in UNLINK]
    sys.exit(
        # run the cli
        any(do([*COV, *RUN, *cli]) for cli in CLI)
        # run the tests
        or do([*COV, *RUN, *TEST])
        # maybe run coverage
        or do([*COV, *REPORT])
    )
