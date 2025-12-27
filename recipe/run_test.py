import sys
import subprocess
from pathlib import Path

FAIL_UNDER = "57"
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
    rc = 1
    for i in range(5):
        print(f"[{i + 1}/5] >>>", *args, flush=True)
        proc = subprocess.Popen(args)
        try:
            rc = proc.wait(timeout=60)
        except TimeoutError:
            print("!!! failed after 60s, retrying...", flush=True)
            proc.kill()
            proc.terminate()
        else:
            break

    return rc


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
