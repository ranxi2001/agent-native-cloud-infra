#!/usr/bin/env python3
"""Validate or refresh deterministic checksums for workstation-local skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents" / "skills"
LOCK_FILE = ROOT / "skills.lock.json"


def digest_skill(path: Path) -> str:
    digest = hashlib.sha256()
    files = [
        candidate
        for candidate in sorted(path.rglob("*"))
        if candidate.is_file() and "__pycache__" not in candidate.parts
    ]
    for candidate in files:
        relative = candidate.relative_to(path).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(candidate.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def load_lock() -> dict[str, Any]:
    try:
        data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot load {LOCK_FILE}: {exc}") from exc
    if data.get("schema_version") != 1 or not isinstance(data.get("skills"), dict):
        raise RuntimeError(f"invalid lock schema: {LOCK_FILE}")
    return data


def local_skills() -> dict[str, Path]:
    return {
        path.name: path
        for path in sorted(SKILLS_ROOT.iterdir())
        if path.is_dir() and (path / "SKILL.md").is_file()
    }


def update_lock(data: dict[str, Any], paths: dict[str, Path]) -> None:
    locked = data["skills"]
    if set(locked) != set(paths):
        missing = sorted(set(paths) - set(locked))
        stale = sorted(set(locked) - set(paths))
        raise RuntimeError(f"lock membership mismatch; add={missing}, remove={stale}")
    for name, path in paths.items():
        entry = locked[name]
        if not isinstance(entry, dict) or entry.get("source") != "local":
            raise RuntimeError(f"invalid lock entry for {name}")
        entry["sha256"] = digest_skill(path)
    LOCK_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_lock(data: dict[str, Any], paths: dict[str, Path]) -> list[str]:
    errors: list[str] = []
    locked = data["skills"]
    if set(locked) != set(paths):
        errors.append(
            f"skill membership mismatch: local={sorted(paths)}, lock={sorted(locked)}"
        )
    for name in sorted(set(locked) & set(paths)):
        entry = locked[name]
        if not isinstance(entry, dict):
            errors.append(f"{name}: lock entry must be an object")
            continue
        if entry.get("source") != "local":
            errors.append(f"{name}: unsupported source {entry.get('source')!r}")
        revision = entry.get("revision")
        if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
            errors.append(f"{name}: revision must be a positive integer")
        scenario = entry.get("scenario")
        if not isinstance(scenario, str) or not scenario.strip():
            errors.append(f"{name}: scenario must be a non-empty string")
        validated_at = entry.get("validated_at")
        try:
            if not isinstance(validated_at, str):
                raise ValueError
            if date.fromisoformat(validated_at).isoformat() != validated_at:
                raise ValueError
        except ValueError:
            errors.append(f"{name}: validated_at must use YYYY-MM-DD")
        expected = entry.get("sha256")
        actual = digest_skill(paths[name])
        if expected != actual:
            errors.append(f"{name}: checksum mismatch; run scripts/validate_skills.py --update")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true", help="refresh checksums")
    args = parser.parse_args()
    try:
        data = load_lock()
        paths = local_skills()
        if args.update:
            update_lock(data, paths)
            print(f"updated {len(paths)} skill checksums")
            return 0
        errors = validate_lock(data, paths)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated {len(paths)} locked skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
