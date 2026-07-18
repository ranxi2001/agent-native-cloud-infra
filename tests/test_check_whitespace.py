from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_whitespace.py"


class CheckWhitespaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        subprocess.run(
            ["git", "init", "-b", "main"],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        )

    def check(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.repo)],
            cwd=self.repo,
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def test_accepts_clean_untracked_and_staged_files_on_unborn_branch(self) -> None:
        (self.repo / "untracked.txt").write_text("clean\n", encoding="utf-8")
        (self.repo / "staged.txt").write_text("also clean\n", encoding="utf-8")
        self.git("add", "staged.txt")

        result = self.check()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("1 untracked file", result.stdout)

    def test_rejects_untracked_trailing_whitespace(self) -> None:
        (self.repo / "bad.txt").write_text("bad \n", encoding="utf-8")

        result = self.check()

        self.assertEqual(result.returncode, 1)
        self.assertIn("trailing whitespace", result.stdout)

    def test_rejects_staged_trailing_whitespace(self) -> None:
        (self.repo / "bad.txt").write_text("bad \n", encoding="utf-8")
        self.git("add", "bad.txt")

        result = self.check()

        self.assertEqual(result.returncode, 1)
        self.assertIn("trailing whitespace", result.stdout)

    def test_rejects_unstaged_trailing_whitespace(self) -> None:
        path = self.repo / "tracked.txt"
        path.write_text("clean\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        path.write_text("bad \n", encoding="utf-8")

        result = self.check()

        self.assertEqual(result.returncode, 1)
        self.assertIn("trailing whitespace", result.stdout)


if __name__ == "__main__":
    unittest.main()
