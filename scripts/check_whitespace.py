#!/usr/bin/env python3
"""Check whitespace in tracked, staged, and untracked workstation files."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
    )


def report_failure(result: subprocess.CompletedProcess[bytes]) -> None:
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)


def check_diff(root: Path, *args: str) -> bool:
    result = run_git(root, "diff", *args, "--check")
    if result.returncode != 0:
        report_failure(result)
        return False
    return True


def untracked_files(root: Path) -> list[str]:
    result = run_git(root, "ls-files", "--others", "--exclude-standard", "-z")
    if result.returncode != 0:
        report_failure(result)
        raise RuntimeError("cannot list untracked files")
    return [os.fsdecode(name) for name in result.stdout.split(b"\0") if name]


def check_untracked(root: Path, path: str) -> bool:
    result = run_git(root, "diff", "--no-index", "--check", "--", os.devnull, path)
    if result.returncode not in (0, 1):
        report_failure(result)
        return False
    if result.stdout or result.stderr:
        report_failure(result)
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Git worktree to check")
    root = parser.parse_args().root.expanduser().resolve()

    valid = check_diff(root)
    valid = check_diff(root, "--cached") and valid
    try:
        paths = untracked_files(root)
    except RuntimeError:
        return 1
    for path in paths:
        valid = check_untracked(root, path) and valid
    if valid:
        print(f"validated whitespace in Git state and {len(paths)} untracked file(s)")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
