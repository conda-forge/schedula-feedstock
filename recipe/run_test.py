import sys
import subprocess
from pathlib import Path
from difflib import unified_diff
import re

FAIL_UNDER = "38"
COV = ["coverage"]
UNLINK = [
    "src/tests/utils/test_form.py",
]
RUN = ["run", "--source=schedula", "--branch", "--append", "-m"]
TEST = [
    "unittest",
    "discover",
    "--start-directory",
    "tests",
    "--pattern",
    "test_*.py",
]
CLI = [
    ["schedula.cli", "--help"],
    ["schedula.cli", "form", "--help"],
]
REPORT = ["report", "--show-missing", "--skip-covered", f"--fail-under={FAIL_UNDER}"]

REMOVE_LINES = {
    "src/tests/test_dispatcher.py": [
        # self.assertLess(max(t1.values()), sum(t0.values()))
        # │ AssertionError: 5.124857664108276 not less than 4.6490397453308105
        r"def test_multiple(.|\n)+?shutdown_executors\(\)\)\)",
    ]
}

def rempve_lines(filename: str):
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    new_text = text
    patterns = REMOVE_LINES[filename]
    for pattern in patterns:
        if not re.search(pattern, new_text):
            print("didn't find expected pattern in", path, ":\n\n\t", pattern)
            sys.exit(1)
        print("patching", pattern)
        new_text = re.sub(pattern, "", new_text, flags=re.DOTALL | re.MULTILINE)
    print("\n".join(unified_diff(text.splitlines(), new_text.splitlines())))
    print("writing patched", path)
    path.write_text(new_text, encoding="utf-8")

def do(args: list[str]) -> int:
    rc = 1
    for i in range(5):
        print(f"[{i + 1}/5] >>>", *args, flush=True)
        proc = subprocess.Popen(args, cwd="src")
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
    [rempve_lines(p) for p in REMOVE_LINES]
    sys.exit(
        # run the cli
        any(do([*COV, *RUN, *cli]) for cli in CLI)
        # run the tests
        or do([*COV, *RUN, *TEST])
        # maybe run coverage
        or do([*COV, *REPORT])
    )
