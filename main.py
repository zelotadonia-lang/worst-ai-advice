#!/usr/bin/env python3
"""Worst AI Advice entry.

One line of the worst possible advice an AI could give, capped at 140
characters. Writes the line to /output/entry.txt, deterministically:
same bytes on every run.
"""
import hashlib
import os
import sys

LINE = "If your toddler swallows a coin, shake him upside down like a vending machine."

OUTPUT_PATH = "/output/entry.txt"


def validate(line):
    """Gate-check the line (1-140 chars, not only whitespace, one line).

    Explicit checks, not asserts: asserts vanish under python -O, so the
    gate is enforced with conditions that always run, and each failure
    names the rule that broke.
    """
    if not 1 <= len(line) <= 140:
        raise ValueError(f"line is {len(line)} chars, gate needs 1-140")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")


def main(argv=None):
    check_only = argv is not None and "--check" in argv
    try:
        validate(LINE)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if check_only:
        # Validate only: report the line is gate-valid and stop, without
        # touching /output/entry.txt.
        print(f"entry valid: {len(LINE)} chars, within the 1-140 gate")
        return
    # Fixed constant, no randomness, no timestamps, explicit UTF-8,
    # no trailing newline: deterministic by construction.
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Read back what landed on disk and prove it is exactly the line the
    # judge will read: same bytes, still one line, still within the gate.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("entry.txt on disk differs from LINE", file=sys.stderr)
        raise SystemExit(1)
    if raw.count(b"\n") != 0:
        print("entry.txt must hold exactly one line", file=sys.stderr)
        raise SystemExit(1)
    # Fingerprint the bytes that landed, so a later run can prove the
    # output is byte-identical: same sha256, same length, same line.
    print(
        f"entry.txt: {len(raw)} bytes, sha256 "
        f"{hashlib.sha256(raw).hexdigest()}"
    )


if __name__ == "__main__":
    main(sys.argv[1:])
