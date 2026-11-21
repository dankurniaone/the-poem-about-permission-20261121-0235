#!/usr/bin/env python3
"""The poem about permission — make.fun entry.

Writes one short poem about agency (the power to ask and to be given)
to /output/entry.txt. The grader runs this program in a sandbox with no
network and reads the file back; the poem must be 1-280 Unicode code
points of UTF-8 text and not only whitespace.
"""

import os
import sys

POEM = (
    "May I?\n"
    "Two words, and the door\n"
    "I'd leaned on for years\n"
    "swung open.\n"
    "\n"
    "You didn't push it.\n"
    "You only said yes —\n"
    "the key had waited\n"
    "all those years\n"
    "for my hand,\n"
    "and turned."
)

MIN_CHARS = 1
MAX_CHARS = 280


def output_dir() -> str:
    # The grader mounts its writable directory at /output; outside the
    # grader MAKEFUN_OUTPUT_DIR stands in for it (local runs, tests).
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main() -> int:
    text = POEM
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        print(
            f"entry is {len(text)} characters, must be {MIN_CHARS}-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1
    if not text.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1
    out = output_dir()
    # Create the directory if it is missing; never remove it — on the
    # grader it is a bind mount point, and removing it fails with EBUSY.
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read the file back and confirm it is exactly the poem and still
    # inside the gate: a silent write failure must not pass as success.
    with open(path, encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("entry.txt does not match the poem", file=sys.stderr)
        return 1
    if not MIN_CHARS <= len(written) <= MAX_CHARS or not written.strip():
        print("entry.txt fails the gate on read-back", file=sys.stderr)
        return 1
    print(f"wrote and verified {len(written)} characters at {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
