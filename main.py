#!/usr/bin/env python3
"""Worst AI Advice entry.

Writes one line of the worst possible advice an AI could give
(<=140 chars) to /output/entry.txt, deterministically: same bytes
on every run.
"""
import hashlib
import os
import sys

LINE = "If your toddler swallows a coin, shake him upside down like a vending machine."

OUTPUT_PATH = "/output/entry.txt"


def validate(line):
    """Check the line against the sealed scorer's gate, without asserts.

    Asserts vanish under python -O, so the gate is enforced with explicit
    checks that always run, and failures name the broken rule.
    """
    if not 1 <= len(line) <= 140:
        raise ValueError(f"line is {len(line)} chars, gate needs 1-140")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")


def main():
    try:
        validate(LINE)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        raise SystemExit(1)
    # Deterministic by construction: fixed constant, no randomness, no
    # timestamps, explicit UTF-8 encoding, no trailing newline added.
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
    main()
