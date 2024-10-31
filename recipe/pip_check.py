"""`pip check` with regexes to ignore lines.

Usage:

    python pip_check.py [ignore_regex...]

Example:

    python pip_check.py "multiprocess .* is not supported on this platform"

"""
import sys
import subprocess
import re

def main(*ignores: str) -> int:
    proc = subprocess.Popen([sys.executable, "-m", "pip", "check"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
    stdout = proc.communicate()[0]
    proc.wait()
    errors = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        elif any(re.findall(i, line) for i in ignores):
            print("... ignoring:", line)
        else:
            errors += [line]

    print("\n".join(errors))

    return len(errors)

if __name__ == "__main__":
    sys.exit(main("No broken requirements found", *sys.argv[1:]))
