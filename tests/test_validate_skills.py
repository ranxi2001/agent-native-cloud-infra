from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validate_skills import digest_skill, update_lock, validate_lock


class ValidateSkillsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.skill = Path(self.temp.name) / "demo-skill"
        self.skill.mkdir()
        (self.skill / "SKILL.md").write_text(
            "---\nname: demo-skill\ndescription: Test skill.\n---\n",
            encoding="utf-8",
        )
        self.paths = {"demo-skill": self.skill}
        self.lock = {
            "schema_version": 1,
            "skills": {
                "demo-skill": {
                    "revision": 1,
                    "scenario": "Completed a read-only example task",
                    "sha256": digest_skill(self.skill),
                    "source": "local",
                    "validated_at": "2026-07-18",
                }
            },
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_accepts_complete_lock_entry(self) -> None:
        self.assertEqual(validate_lock(self.lock, self.paths), [])

    def test_rejects_invalid_validation_metadata(self) -> None:
        invalid_values = (
            ("revision", 0),
            ("scenario", " "),
            ("validated_at", "18 July 2026"),
            ("validated_at", "20260718"),
        )
        for field, value in invalid_values:
            with self.subTest(field=field):
                lock = copy.deepcopy(self.lock)
                lock["skills"]["demo-skill"][field] = value
                errors = validate_lock(lock, self.paths)
                self.assertTrue(any(field in error for error in errors), errors)

    def test_rejects_membership_and_checksum_drift(self) -> None:
        missing = validate_lock(self.lock, {})
        self.assertTrue(any("membership mismatch" in error for error in missing), missing)

        (self.skill / "SKILL.md").write_text("changed\n", encoding="utf-8")
        drifted = validate_lock(self.lock, self.paths)
        self.assertTrue(any("checksum mismatch" in error for error in drifted), drifted)

    def test_update_refreshes_only_checksum(self) -> None:
        lock_file = Path(self.temp.name) / "skills.lock.json"
        scenario = self.lock["skills"]["demo-skill"]["scenario"]
        validated_at = self.lock["skills"]["demo-skill"]["validated_at"]
        (self.skill / "SKILL.md").write_text("changed\n", encoding="utf-8")

        with patch("scripts.validate_skills.LOCK_FILE", lock_file):
            update_lock(self.lock, self.paths)

        entry = self.lock["skills"]["demo-skill"]
        self.assertEqual(entry["sha256"], digest_skill(self.skill))
        self.assertEqual(entry["scenario"], scenario)
        self.assertEqual(entry["validated_at"], validated_at)


if __name__ == "__main__":
    unittest.main()
