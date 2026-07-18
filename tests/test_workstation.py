from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import tomllib
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "workstation.py"


class WorkstationCLITest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.workspace = self.root / "workspace"
        self.repo = self.root / "demo-repo"
        (self.workspace / "projects").mkdir(parents=True)
        for lane_name in ("demo", "planned"):
            lane = self.workspace / "lanes" / lane_name
            (lane / "tasks").mkdir(parents=True)
            (lane / "PROJECT.md").write_text(f"# {lane_name}\n", encoding="utf-8")
            (lane / "BACKLOG.md").write_text(f"# {lane_name} backlog\n", encoding="utf-8")
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Test User")
        self.git("config", "user.email", "test@example.com")
        (self.repo / "README.md").write_text("# Demo\n", encoding="utf-8")
        native_skill = self.repo / "native-skills" / "runtime.md"
        native_skill.parent.mkdir()
        native_skill.write_text("# Runtime skill\n", encoding="utf-8")
        template = self.repo / ".github" / "pull_request_template.md"
        template.parent.mkdir()
        template.write_text("# PR template\n", encoding="utf-8")
        self.git("add", "README.md", ".github/pull_request_template.md", "native-skills/runtime.md")
        self.git("commit", "-m", "initial")
        self.git("remote", "add", "origin", "https://github.com/example/demo-fork.git")
        self.git("remote", "add", "upstream", "https://github.com/example/demo.git")
        self.git("remote", "set-url", "--push", "upstream", "DISABLED")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("update-ref", "refs/remotes/upstream/main", "HEAD")
        self.make_learning_ref()

        self.config = self.workspace / "workstation.toml"
        self.config.write_text(
            textwrap.dedent(
                """\
                schema_version = 1

                [workspace]
                project_dir = "projects"
                lanes_dir = "lanes"
                worktrees_dir = ".worktrees"
                """
            ),
            encoding="utf-8",
        )
        (self.workspace / "projects" / "demo.toml").write_text(
            textwrap.dedent(
                f"""\
                schema_version = 1
                id = "demo"
                display_name = "Demo"
                status = "active"
                path = {json.dumps(str(self.repo))}
                lane = "lanes/demo"
                upstream_repo = "example/demo"
                upstream_url = "https://github.com/example/demo.git"
                upstream_remote = "upstream"
                fork_url = "https://github.com/example/demo-fork.git"
                fork_remote = "origin"
                default_branch = "main"
                learning_branch = "intern"
                domains = ["sandbox"]
                native_skill_globs = ["native-skills/*.md"]

                [commands]
                build = ["make build"]
                test = ["make test"]
                """
            ),
            encoding="utf-8",
        )
        (self.workspace / "projects" / "planned.toml").write_text(
            textwrap.dedent(
                f"""\
                schema_version = 1
                id = "planned"
                display_name = "Planned"
                status = "planned"
                path = {json.dumps(str(self.root / 'missing'))}
                lane = "lanes/planned"
                upstream_repo = "example/planned"
                upstream_url = "https://github.com/example/planned.git"
                upstream_remote = "upstream"
                fork_url = ""
                fork_remote = "origin"
                default_branch = "main"
                learning_branch = "intern"
                domains = []
                native_skill_globs = []

                [commands]
                build = []
                test = []
                """
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )

    def make_learning_ref(self) -> None:
        self.git("switch", "-c", "intern")
        (self.repo / "AGENTS.md").write_text("# Agent rules\n", encoding="utf-8")
        skill = self.repo / ".agents" / "skills" / "demo-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("# Demo skill\n", encoding="utf-8")
        self.git("add", "AGENTS.md", ".agents")
        self.git("commit", "-m", "add learning context")
        self.git("update-ref", "refs/remotes/origin/intern", "HEAD")
        self.git("switch", "main")
        self.git("branch", "-D", "intern")

    def cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--config", str(self.config), *args],
            cwd=self.workspace,
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if check and result.returncode != 0:
            self.fail(f"command failed: {result.args}\nstdout={result.stdout}\nstderr={result.stderr}")
        return result

    def test_list_and_status_json(self) -> None:
        listed = json.loads(self.cli("list", "--json").stdout)
        self.assertEqual([item["id"] for item in listed], ["demo", "planned"])

        statuses = json.loads(self.cli("status", "demo", "planned", "--json").stdout)
        self.assertEqual(statuses[0]["branch"], "main")
        self.assertEqual(statuses[0]["dirty"], 0)
        self.assertEqual(statuses[0]["canonical"], "upstream/main")
        self.assertEqual(statuses[0]["canonical_ahead"], 0)
        self.assertEqual(statuses[0]["canonical_behind"], 0)
        self.assertFalse(statuses[1]["exists"])

    def test_context_reads_learning_ref_without_switching(self) -> None:
        context = json.loads(self.cli("context", "demo", "--json").stdout)
        self.assertIn("origin/intern:AGENTS.md", context["instructions"])
        self.assertIn(
            "origin/intern:.agents/skills/demo-skill/SKILL.md",
            context["skills"],
        )
        self.assertIn(str(self.repo / "native-skills" / "runtime.md"), context["skills"])
        self.assertIn(
            str(self.repo / ".github" / "pull_request_template.md"),
            context["instructions"],
        )
        branch = self.git("branch", "--show-current").stdout.strip()
        self.assertEqual(branch, "main")

    def test_doctor_treats_missing_planned_repo_as_info(self) -> None:
        result = self.cli("doctor", "--json")
        checks = json.loads(result.stdout)
        planned = [item for item in checks if item["message"].startswith("planned:")]
        self.assertEqual(planned[0]["level"], "INFO")
        self.assertFalse(any(item["level"] == "ERROR" for item in checks))

    def test_doctor_rejects_missing_active_upstream_remote(self) -> None:
        self.git("remote", "remove", "upstream")

        result = self.cli("doctor", "demo", "--json", check=False)

        self.assertEqual(result.returncode, 1)
        checks = json.loads(result.stdout)
        self.assertTrue(
            any(
                item["level"] == "ERROR" and "missing upstream remote" in item["message"]
                for item in checks
            ),
            checks,
        )

    def test_doctor_rejects_wrong_active_upstream_url(self) -> None:
        self.git("remote", "set-url", "upstream", "https://github.com/example/wrong.git")

        result = self.cli("doctor", "demo", "--json", check=False)

        self.assertEqual(result.returncode, 1)
        checks = json.loads(result.stdout)
        self.assertTrue(
            any(
                item["level"] == "ERROR" and "expected https://github.com/example/demo.git" in item["message"]
                for item in checks
            ),
            checks,
        )

    def test_doctor_rejects_enabled_active_upstream_push(self) -> None:
        self.git(
            "remote",
            "set-url",
            "--push",
            "upstream",
            "https://github.com/example/demo.git",
        )

        result = self.cli("doctor", "demo", "--json", check=False)

        self.assertEqual(result.returncode, 1)
        checks = json.loads(result.stdout)
        self.assertTrue(
            any(
                item["level"] == "ERROR" and "upstream push URL is enabled" in item["message"]
                for item in checks
            ),
            checks,
        )

    def test_task_create_writes_structured_state_and_evidence_files(self) -> None:
        self.cli(
            "task-create",
            "demo",
            "fix-timeout",
            "--title",
            "Fix timeout cleanup",
            "--issue",
            "https://github.com/example/demo/issues/1",
        )
        task_dir = self.workspace / "lanes" / "demo" / "tasks" / "fix-timeout"
        metadata = tomllib.loads((task_dir / "task.toml").read_text(encoding="utf-8"))
        self.assertEqual(metadata["status"], "planned")
        self.assertEqual(metadata["project"], "demo")
        self.assertTrue((task_dir / "brief.md").is_file())
        self.assertTrue((task_dir / "evidence.md").is_file())
        self.assertTrue((task_dir / "upstream-draft.md").is_file())

        self.cli("task-status", "demo", "fix-timeout", "researching")
        updated = tomllib.loads((task_dir / "task.toml").read_text(encoding="utf-8"))
        self.assertEqual(updated["status"], "researching")
        self.assertIn("updated_at", updated)

    def test_task_create_can_add_isolated_worktree(self) -> None:
        self.cli(
            "task-create",
            "demo",
            "docs-fix",
            "--worktree",
            "--branch",
            "docs/fix",
        )
        worktree = self.workspace / ".worktrees" / "demo" / "docs-fix"
        self.assertTrue((worktree / ".git").is_file())
        metadata = tomllib.loads(
            (self.workspace / "lanes" / "demo" / "tasks" / "docs-fix" / "task.toml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(metadata["branch"], "docs/fix")
        self.assertEqual(metadata["base"], "upstream/main")
        self.assertEqual(metadata["worktree"], str(worktree))

    def test_task_slug_rejects_path_traversal(self) -> None:
        result = self.cli("task-create", "demo", "../escape", check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("task slug", result.stderr)
        self.assertFalse((self.workspace / "lanes" / "demo" / "escape").exists())

    def test_doctor_rejects_task_status_drift(self) -> None:
        self.cli("task-create", "demo", "drifted-task")
        task_file = self.workspace / "lanes" / "demo" / "tasks" / "drifted-task" / "task.toml"
        content = task_file.read_text(encoding="utf-8").replace(
            'status = "planned"', 'status = "WATCH / OPEN"'
        )
        task_file.write_text(content, encoding="utf-8")

        result = self.cli("doctor", "demo", "--json", check=False)
        self.assertEqual(result.returncode, 1)
        checks = json.loads(result.stdout)
        self.assertTrue(
            any("invalid task status" in item["message"] for item in checks),
            checks,
        )

    def test_project_add_creates_profile_without_cloning_or_forking(self) -> None:
        target = self.root / "new-repo"
        self.cli(
            "project-add",
            "new-project",
            "--name",
            "New Project",
            "--path",
            str(target),
            "--upstream-repo",
            "example/new-project",
            "--upstream-url",
            "https://github.com/example/new-project.git",
        )
        config = tomllib.loads(
            (self.workspace / "projects" / "new-project.toml").read_text(encoding="utf-8")
        )
        self.assertEqual(config["status"], "planned")
        self.assertEqual(config["path"], os.path.relpath(target, self.workspace))
        self.assertFalse(target.exists())
        self.assertTrue((self.workspace / "lanes" / "new-project" / "PROJECT.md").is_file())


if __name__ == "__main__":
    unittest.main()
