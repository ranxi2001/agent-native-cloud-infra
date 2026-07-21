#!/usr/bin/env python3
"""Manage project context and isolated contribution lanes for this workstation."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "workstation.toml"
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
BRANCH_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
REMOTE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
MOUNT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
VALID_STATUSES = {"planned", "active", "paused", "archived"}
ALWAYS_LOAD_BUDGET_BYTES = 256 * 1024
ALWAYS_LOAD_BUDGET_FILES = 6
TASK_STATUSES = (
    "planned",
    "researching",
    "ready",
    "implementing",
    "validating",
    "awaiting-approval",
    "upstream",
    "blocked",
    "done",
    "dropped",
)


class WorkstationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Workspace:
    root: Path
    project_dir: Path
    lanes_dir: Path
    worktrees_dir: Path
    context_dir: Path
    context_cache_dir: Path


@dataclass(frozen=True)
class Knowledge:
    ref: str
    always_load: tuple[str, ...]
    mounts: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class Project:
    source: Path
    id: str
    display_name: str
    status: str
    path: Path
    lane: Path
    upstream_repo: str
    upstream_url: str
    upstream_remote: str
    fork_url: str
    fork_remote: str
    default_branch: str
    learning_branch: str
    domains: tuple[str, ...]
    native_skill_globs: tuple[str, ...]
    commands: dict[str, tuple[str, ...]]
    knowledge: Knowledge | None

    def public(self) -> dict[str, Any]:
        data = asdict(self)
        data["source"] = str(self.source)
        data["path"] = str(self.path)
        data["lane"] = str(self.lane)
        data["domains"] = list(self.domains)
        data["native_skill_globs"] = list(self.native_skill_globs)
        data["commands"] = {key: list(value) for key, value in self.commands.items()}
        if self.knowledge:
            data["knowledge"] = {
                "ref": self.knowledge.ref,
                "always_load": list(self.knowledge.always_load),
                "mounts": dict(self.knowledge.mounts),
            }
        return data


def resolve_path(root: Path, raw: str) -> Path:
    path = Path(raw).expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def require_string(doc: dict[str, Any], key: str, source: Path) -> str:
    value = doc.get(key)
    if not isinstance(value, str):
        raise WorkstationError(f"{source}: {key} must be a string")
    return value


def optional_string(doc: dict[str, Any], key: str, default: str, source: Path) -> str:
    value = doc.get(key, default)
    if not isinstance(value, str):
        raise WorkstationError(f"{source}: {key} must be a string")
    return value


def safe_relative_path(value: str, source: Path, field: str) -> str:
    if not value or "\\" in value:
        raise WorkstationError(f"{source}: {field} must be a safe POSIX relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise WorkstationError(f"{source}: {field} must be a safe relative path")
    if path.parts[0] == ".git":
        raise WorkstationError(f"{source}: {field} cannot expose .git")
    return path.as_posix()


def knowledge_paths_from_config(knowledge: Knowledge) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys((*knowledge.always_load, *(path for _, path in knowledge.mounts)))
    )


def load_registry(config_path: Path) -> tuple[Workspace, list[Project]]:
    config_path = config_path.expanduser().resolve()
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise WorkstationError(f"cannot load {config_path}: {exc}") from exc

    if config.get("schema_version") != 1:
        raise WorkstationError(f"{config_path}: unsupported schema_version")
    workspace_doc = config.get("workspace")
    if not isinstance(workspace_doc, dict):
        raise WorkstationError(f"{config_path}: missing [workspace]")

    root = config_path.parent
    workspace = Workspace(
        root=root,
        project_dir=resolve_path(root, require_string(workspace_doc, "project_dir", config_path)),
        lanes_dir=resolve_path(root, require_string(workspace_doc, "lanes_dir", config_path)),
        worktrees_dir=resolve_path(root, require_string(workspace_doc, "worktrees_dir", config_path)),
        context_dir=resolve_path(
            root,
            optional_string(workspace_doc, "context_dir", ".context", config_path),
        ),
        context_cache_dir=resolve_path(
            root,
            optional_string(
                workspace_doc,
                "context_cache_dir",
                ".cache/context",
                config_path,
            ),
        ),
    )
    for name, path in (
        ("context_dir", workspace.context_dir),
        ("context_cache_dir", workspace.context_cache_dir),
    ):
        if path == root or root not in path.parents:
            raise WorkstationError(f"{config_path}: workspace.{name} must stay below {root}")

    projects: list[Project] = []
    seen: set[str] = set()
    for source in sorted(workspace.project_dir.glob("*.toml")):
        try:
            doc = tomllib.loads(source.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise WorkstationError(f"cannot load {source}: {exc}") from exc
        if doc.get("schema_version") != 1:
            raise WorkstationError(f"{source}: unsupported schema_version")

        project_id = require_string(doc, "id", source)
        if not ID_PATTERN.fullmatch(project_id):
            raise WorkstationError(f"{source}: invalid id {project_id!r}")
        if project_id in seen:
            raise WorkstationError(f"duplicate project id: {project_id}")
        seen.add(project_id)

        status = require_string(doc, "status", source)
        if status not in VALID_STATUSES:
            raise WorkstationError(f"{source}: invalid status {status!r}")
        domains = doc.get("domains", [])
        native_skill_globs = doc.get("native_skill_globs", [])
        commands_doc = doc.get("commands", {})
        knowledge_doc = doc.get("knowledge")
        if not isinstance(domains, list) or not all(isinstance(item, str) for item in domains):
            raise WorkstationError(f"{source}: domains must be an array of strings")
        if not isinstance(commands_doc, dict):
            raise WorkstationError(f"{source}: [commands] must be a table")
        if not isinstance(native_skill_globs, list) or not all(
            isinstance(item, str) and item and not Path(item).is_absolute() and ".." not in Path(item).parts
            for item in native_skill_globs
        ):
            raise WorkstationError(f"{source}: native_skill_globs must contain safe relative globs")
        commands: dict[str, tuple[str, ...]] = {}
        for name, values in commands_doc.items():
            if not isinstance(name, str) or not isinstance(values, list) or not all(
                isinstance(item, str) for item in values
            ):
                raise WorkstationError(f"{source}: command values must be arrays of strings")
            commands[name] = tuple(values)

        knowledge: Knowledge | None = None
        if knowledge_doc is not None:
            if not isinstance(knowledge_doc, dict):
                raise WorkstationError(f"{source}: [knowledge] must be a table")
            knowledge_ref = require_string(knowledge_doc, "ref", source)
            if not BRANCH_PATTERN.fullmatch(knowledge_ref) or ".." in knowledge_ref:
                raise WorkstationError(f"{source}: invalid knowledge ref {knowledge_ref!r}")
            always_load_doc = knowledge_doc.get("always_load", [])
            mounts_doc = knowledge_doc.get("mounts", {})
            if not isinstance(always_load_doc, list) or not all(
                isinstance(item, str) for item in always_load_doc
            ):
                raise WorkstationError(f"{source}: knowledge.always_load must be strings")
            if not isinstance(mounts_doc, dict) or not all(
                isinstance(name, str) and isinstance(path, str)
                for name, path in mounts_doc.items()
            ):
                raise WorkstationError(f"{source}: [knowledge.mounts] must map names to paths")
            always_load = tuple(
                safe_relative_path(item, source, "knowledge.always_load")
                for item in always_load_doc
            )
            mounts: list[tuple[str, str]] = []
            for name, path in sorted(mounts_doc.items()):
                if (
                    not MOUNT_NAME_PATTERN.fullmatch(name)
                    or name in {"source", "intern", "context.json"}
                ):
                    raise WorkstationError(f"{source}: invalid knowledge mount name {name!r}")
                mounts.append(
                    (name, safe_relative_path(path, source, f"knowledge.mounts.{name}"))
                )
            knowledge = Knowledge(
                ref=knowledge_ref,
                always_load=always_load,
                mounts=tuple(mounts),
            )
            if not knowledge_paths_from_config(knowledge):
                raise WorkstationError(f"{source}: [knowledge] must declare at least one path")

        project = Project(
            source=source,
            id=project_id,
            display_name=require_string(doc, "display_name", source),
            status=status,
            path=resolve_path(root, require_string(doc, "path", source)),
            lane=resolve_path(root, require_string(doc, "lane", source)),
            upstream_repo=require_string(doc, "upstream_repo", source),
            upstream_url=require_string(doc, "upstream_url", source),
            upstream_remote=require_string(doc, "upstream_remote", source),
            fork_url=require_string(doc, "fork_url", source),
            fork_remote=require_string(doc, "fork_remote", source),
            default_branch=require_string(doc, "default_branch", source),
            learning_branch=require_string(doc, "learning_branch", source),
            domains=tuple(domains),
            native_skill_globs=tuple(native_skill_globs),
            commands=commands,
            knowledge=knowledge,
        )
        for branch_name in (project.default_branch, project.learning_branch):
            if branch_name and (not BRANCH_PATTERN.fullmatch(branch_name) or ".." in branch_name):
                raise WorkstationError(f"{source}: invalid branch name {branch_name!r}")
        for remote_name in (project.upstream_remote, project.fork_remote):
            if not REMOTE_PATTERN.fullmatch(remote_name):
                raise WorkstationError(f"{source}: invalid remote name {remote_name!r}")
        if not REPOSITORY_PATTERN.fullmatch(project.upstream_repo):
            raise WorkstationError(f"{source}: invalid upstream_repo {project.upstream_repo!r}")
        projects.append(project)
    return workspace, projects


def select_projects(projects: list[Project], ids: Iterable[str]) -> list[Project]:
    wanted = list(ids)
    if not wanted:
        return projects
    by_id = {project.id: project for project in projects}
    missing = [project_id for project_id in wanted if project_id not in by_id]
    if missing:
        raise WorkstationError(f"unknown project(s): {', '.join(missing)}")
    return [by_id[project_id] for project_id in wanted]


def run_git(project: Project, *args: str, timeout: int = 15) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", "-C", str(project.path), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise WorkstationError(f"git failed for {project.id}: {exc}") from exc


def git_output(project: Project, *args: str) -> str | None:
    result = run_git(project, *args)
    return result.stdout.strip() if result.returncode == 0 else None


def project_status(project: Project) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": project.id,
        "status": project.status,
        "path": str(project.path),
        "exists": project.path.exists(),
        "git": False,
        "branch": None,
        "head": None,
        "dirty": None,
        "tracking": None,
        "ahead": None,
        "behind": None,
        "canonical": None,
        "canonical_ahead": None,
        "canonical_behind": None,
    }
    if not project.path.exists():
        return result
    inside = git_output(project, "rev-parse", "--is-inside-work-tree")
    if inside != "true":
        return result
    result["git"] = True
    branch = git_output(project, "symbolic-ref", "--quiet", "--short", "HEAD")
    result["head"] = git_output(project, "rev-parse", "--short=12", "HEAD")
    result["branch"] = branch or (f"detached@{result['head']}" if result["head"] else "detached")
    porcelain = git_output(project, "status", "--porcelain")
    result["dirty"] = len(porcelain.splitlines()) if porcelain else 0
    tracking = git_output(project, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    result["tracking"] = tracking
    if tracking:
        counts = git_output(project, "rev-list", "--left-right", "--count", f"HEAD...{tracking}")
        if counts:
            ahead, behind = counts.split()
            result["ahead"] = int(ahead)
            result["behind"] = int(behind)
    canonical = f"{project.upstream_remote}/{project.default_branch}"
    if ref_exists(project, canonical):
        result["canonical"] = canonical
        counts = git_output(project, "rev-list", "--left-right", "--count", f"HEAD...{canonical}")
        if counts:
            ahead, behind = counts.split()
            result["canonical_ahead"] = int(ahead)
            result["canonical_behind"] = int(behind)
    return result


def print_table(headers: list[str], rows: list[list[str]]) -> None:
    widths = [len(header) for header in headers]
    for row in rows:
        widths = [max(width, len(value)) for width, value in zip(widths, row)]
    print("  ".join(header.ljust(width) for header, width in zip(headers, widths)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(value.ljust(width) for value, width in zip(row, widths)))


def command_list(projects: list[Project], as_json: bool) -> int:
    if as_json:
        print(json.dumps([project.public() for project in projects], indent=2, sort_keys=True))
        return 0
    rows = [
        [project.id, project.status, str(project.path), ",".join(project.domains)]
        for project in projects
    ]
    print_table(["PROJECT", "STATE", "PATH", "DOMAINS"], rows)
    return 0


def command_status(projects: list[Project], as_json: bool) -> int:
    statuses = [project_status(project) for project in projects]
    if as_json:
        print(json.dumps(statuses, indent=2, sort_keys=True))
        return 0
    rows: list[list[str]] = []
    for item in statuses:
        sync = "-"
        if item["tracking"]:
            sync = f"+{item['ahead']}/-{item['behind']}"
        canonical_sync = "-"
        if item["canonical"]:
            canonical_sync = f"+{item['canonical_ahead']}/-{item['canonical_behind']}"
        rows.append(
            [
                item["id"],
                item["branch"] or ("missing" if not item["exists"] else "not-git"),
                "-" if item["dirty"] is None else str(item["dirty"]),
                item["tracking"] or "-",
                sync,
                canonical_sync,
            ]
        )
    print_table(["PROJECT", "BRANCH", "DIRTY", "TRACKING", "SYNC", "UPSTREAM"], rows)
    return 0


def canonical_repo(url: str) -> str:
    value = url.strip().removesuffix(".git").rstrip("/")
    value = re.sub(r"^git@github\.com:", "github.com/", value)
    value = re.sub(r"^(https?|ssh)://(git@)?", "", value)
    return value.lower()


def remote_url(project: Project, name: str) -> str | None:
    return git_output(project, "remote", "get-url", name)


def remote_push_url(project: Project, name: str) -> str | None:
    return git_output(project, "remote", "get-url", "--push", name)


def ref_exists(project: Project, ref: str) -> bool:
    return run_git(project, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").returncode == 0


def knowledge_ref_sha(project: Project) -> str | None:
    if not project.knowledge:
        return None
    return git_output(project, "rev-parse", f"{project.knowledge.ref}^{{commit}}")


def knowledge_paths(project: Project) -> tuple[str, ...]:
    if not project.knowledge:
        return ()
    return knowledge_paths_from_config(project.knowledge)


def git_path_exists(project: Project, ref: str, path: str) -> bool:
    return run_git(project, "cat-file", "-e", f"{ref}:{path}").returncode == 0


def git_path_size(project: Project, ref: str, path: str) -> int | None:
    if git_output(project, "cat-file", "-t", f"{ref}:{path}") != "blob":
        return None
    size = git_output(project, "cat-file", "-s", f"{ref}:{path}")
    return int(size) if size and size.isdigit() else None


def always_load_size(project: Project) -> int | None:
    if not project.knowledge:
        return None
    sizes = [
        git_path_size(project, project.knowledge.ref, path)
        for path in project.knowledge.always_load
    ]
    return sum(size for size in sizes if size is not None) if all(
        size is not None for size in sizes
    ) else None


def git_worktrees(project: Project) -> list[dict[str, str]]:
    output = git_output(project, "worktree", "list", "--porcelain")
    if not output:
        return []
    worktrees: list[dict[str, str]] = []
    for block in output.split("\n\n"):
        record: dict[str, str] = {}
        for line in block.splitlines():
            key, _, value = line.partition(" ")
            if key in {"worktree", "HEAD", "branch"}:
                record[key.lower()] = value
        if "worktree" in record:
            worktrees.append(record)
    return worktrees


def git_output_at(path: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def worktree_is_clean(path: Path) -> bool:
    status = git_output_at(path, "status", "--porcelain")
    return status == ""


def discover_knowledge_worktree(project: Project, sha: str) -> Path | None:
    expected_branch = f"refs/heads/{project.learning_branch}" if project.learning_branch else ""
    for item in git_worktrees(project):
        path = Path(item["worktree"])
        if (
            item.get("branch") == expected_branch
            and item.get("head") == sha
            and path.is_dir()
            and worktree_is_clean(path)
        ):
            return path.resolve()
    return None


def remove_generated_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def extract_git_archive(archive: bytes, destination: Path) -> None:
    root = destination.resolve()
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar:
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
                raise WorkstationError(f"unsafe path in knowledge archive: {member.name!r}")
            target = destination.joinpath(*relative.parts)
            resolved_parent = target.parent.resolve()
            if resolved_parent != root and root not in resolved_parent.parents:
                raise WorkstationError(f"knowledge archive escapes snapshot: {member.name!r}")
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                target.chmod(member.mode & 0o777)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if member.isfile():
                source = tar.extractfile(member)
                if source is None:
                    raise WorkstationError(f"cannot read knowledge archive member {member.name!r}")
                with source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)
                target.chmod(member.mode & 0o777)
                continue
            if member.issym():
                link = PurePosixPath(member.linkname)
                if link.is_absolute():
                    raise WorkstationError(f"absolute symlink in knowledge archive: {member.name!r}")
                resolved_link = (target.parent / Path(*link.parts)).resolve()
                if resolved_link != root and root not in resolved_link.parents:
                    raise WorkstationError(f"knowledge symlink escapes snapshot: {member.name!r}")
                target.symlink_to(member.linkname)
                continue
            raise WorkstationError(f"unsupported knowledge archive member: {member.name!r}")


def materialize_knowledge_snapshot(
    workspace: Workspace,
    project: Project,
    sha: str,
) -> Path:
    paths = knowledge_paths(project)
    fingerprint = hashlib.sha256("\n".join(paths).encode()).hexdigest()[:12]
    parent = workspace.context_cache_dir / "snapshots" / project.id
    destination = parent / f"{sha}-{fingerprint}"
    marker = destination / ".context-snapshot.json"
    if marker.is_file():
        return destination
    parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        remove_generated_path(destination)
    staging = Path(tempfile.mkdtemp(prefix=".snapshot-", dir=parent))
    try:
        try:
            result = subprocess.run(
                ["git", "-C", str(project.path), "archive", "--format=tar", sha, "--", *paths],
                check=False,
                capture_output=True,
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise WorkstationError(f"cannot archive knowledge for {project.id}: {exc}") from exc
        if result.returncode != 0:
            detail = result.stderr.decode(errors="replace").strip()
            raise WorkstationError(f"cannot archive knowledge for {project.id}: {detail}")
        extract_git_archive(result.stdout, staging)
        (staging / ".context-snapshot.json").write_text(
            json.dumps(
                {"project": project.id, "ref": project.knowledge.ref, "sha": sha, "paths": paths},
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        try:
            os.replace(staging, destination)
        except OSError:
            if marker.is_file():
                remove_generated_path(staging)
            else:
                raise
    except Exception:
        if staging.exists():
            remove_generated_path(staging)
        raise
    return destination


def context_overlay_path(workspace: Workspace, project: Project) -> Path:
    return workspace.context_dir / "projects" / project.id


def read_context_metadata(workspace: Workspace, project: Project) -> dict[str, Any] | None:
    metadata = context_overlay_path(workspace, project) / "context.json"
    try:
        value = json.loads(metadata.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def context_overlay_state(workspace: Workspace, project: Project, sha: str | None) -> str:
    overlay = context_overlay_path(workspace, project)
    if not overlay.exists():
        return "missing"
    metadata = read_context_metadata(workspace, project)
    if not metadata:
        return "broken"
    if metadata.get("ref") != project.knowledge.ref or metadata.get("sha") != sha:
        return "stale"
    source_value = metadata.get("source")
    mode = metadata.get("mode")
    if not isinstance(source_value, str):
        return "broken"
    source = Path(source_value)
    if mode == "worktree":
        expected_branch = f"refs/heads/{project.learning_branch}"
        if (
            not source.is_dir()
            or git_output_at(source, "rev-parse", "HEAD") != sha
            or git_output_at(source, "symbolic-ref", "--quiet", "HEAD") != expected_branch
            or not worktree_is_clean(source)
        ):
            return "stale"
    elif mode == "snapshot":
        if not (source / ".context-snapshot.json").is_file():
            return "broken"
    else:
        return "broken"
    expected_links = ("source", "intern", *(name for name, _ in project.knowledge.mounts))
    if any(not (overlay / name).is_symlink() or not (overlay / name).exists() for name in expected_links):
        return "broken"
    return "current"


def _sync_project_context_locked(workspace: Workspace, project: Project) -> dict[str, str]:
    if not project.knowledge:
        raise WorkstationError(f"{project.id}: no [knowledge] configuration")
    if not project.path.is_dir() or git_output(project, "rev-parse", "--is-inside-work-tree") != "true":
        raise WorkstationError(f"{project.id}: repository is not available")
    sha = knowledge_ref_sha(project)
    if not sha:
        raise WorkstationError(f"{project.id}: knowledge ref {project.knowledge.ref} is unavailable")
    missing = [
        path for path in knowledge_paths(project) if not git_path_exists(project, project.knowledge.ref, path)
    ]
    if missing:
        raise WorkstationError(f"{project.id}: missing knowledge path(s): {', '.join(missing)}")

    source = discover_knowledge_worktree(project, sha)
    mode = "worktree"
    if source is None:
        source = materialize_knowledge_snapshot(workspace, project, sha)
        mode = "snapshot"

    projects_dir = workspace.context_dir / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{project.id}-", dir=projects_dir))
    destination = context_overlay_path(workspace, project)
    backup = projects_dir / f".{project.id}.previous"
    try:
        (staging / "source").symlink_to(project.path, target_is_directory=True)
        (staging / "intern").symlink_to(source, target_is_directory=True)
        source_root = source.resolve()
        for name, relative in project.knowledge.mounts:
            target = source.joinpath(*PurePosixPath(relative).parts)
            if not target.exists():
                raise WorkstationError(f"{project.id}: resolved knowledge path is absent: {relative}")
            resolved_target = target.resolve()
            if resolved_target != source_root and source_root not in resolved_target.parents:
                raise WorkstationError(f"{project.id}: knowledge mount escapes source: {relative}")
            (staging / name).symlink_to(target, target_is_directory=target.is_dir())
        (staging / "context.json").write_text(
            json.dumps(
                {
                    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "mode": mode,
                    "project": project.id,
                    "ref": project.knowledge.ref,
                    "sha": sha,
                    "source": str(source),
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        if os.path.lexists(backup):
            remove_generated_path(backup)
        if os.path.lexists(destination):
            os.replace(destination, backup)
        os.replace(staging, destination)
        if os.path.lexists(backup):
            remove_generated_path(backup)
    except Exception:
        if staging.exists():
            remove_generated_path(staging)
        if not os.path.lexists(destination) and os.path.lexists(backup):
            os.replace(backup, destination)
        raise
    return {
        "project": project.id,
        "mode": mode,
        "ref": project.knowledge.ref,
        "sha": sha,
        "source": str(source),
        "overlay": str(destination),
    }


def sync_project_context(workspace: Workspace, project: Project) -> dict[str, str]:
    lock_dir = workspace.context_dir / ".locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / f"{project.id}.lock"
    with lock_path.open("a", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        return _sync_project_context_locked(workspace, project)


def command_context_sync(workspace: Workspace, projects: list[Project], as_json: bool) -> int:
    results = [sync_project_context(workspace, project) for project in projects]
    if as_json:
        print(json.dumps(results, indent=2, sort_keys=True))
        return 0
    rows = [
        [item["project"], item["mode"], item["ref"], item["sha"][:12], item["overlay"]]
        for item in results
    ]
    print_table(["PROJECT", "MODE", "REF", "SHA", "OVERLAY"], rows)
    return 0


def instruction_context(project: Project) -> tuple[list[str], list[str]]:
    instructions: list[str] = []
    skills: list[str] = []
    if not project.path.exists() or git_output(project, "rev-parse", "--is-inside-work-tree") != "true":
        return instructions, skills

    instruction_names = (
        "AGENTS.md",
        "CONTRIBUTING.md",
        "CONTRIBUTING.rst",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/pull_request_template.md",
    )
    for name in instruction_names:
        local = project.path / name
        if local.is_file():
            instructions.append(str(local))

    local_skill_root = project.path / ".agents" / "skills"
    if local_skill_root.is_dir():
        skills.extend(str(path) for path in sorted(local_skill_root.glob("*/SKILL.md")))
    for pattern in project.native_skill_globs:
        skills.extend(
            str(path) for path in sorted(project.path.glob(pattern)) if path.is_file()
        )

    learning_ref = f"{project.fork_remote}/{project.learning_branch}"
    if project.learning_branch and ref_exists(project, learning_ref):
        for name in instruction_names:
            if name.startswith("CONTRIBUTING.") or str(project.path / name) in instructions:
                continue
            if run_git(project, "cat-file", "-e", f"{learning_ref}:{name}").returncode == 0:
                instructions.append(f"{learning_ref}:{name}")
        tree = git_output(project, "ls-tree", "-r", "--name-only", learning_ref, "--", ".agents/skills")
        if tree:
            for name in tree.splitlines():
                if name.endswith("/SKILL.md"):
                    ref_name = f"{learning_ref}:{name}"
                    if ref_name not in skills:
                        skills.append(ref_name)
    return instructions, skills


def build_knowledge_context(workspace: Workspace, project: Project) -> dict[str, Any] | None:
    if not project.knowledge:
        return None
    sha = knowledge_ref_sha(project)
    metadata = read_context_metadata(workspace, project)
    return {
        "ref": project.knowledge.ref,
        "sha": sha,
        "always_load": [f"{project.knowledge.ref}:{path}" for path in project.knowledge.always_load],
        "always_load_bytes": always_load_size(project),
        "mounts": dict(project.knowledge.mounts),
        "overlay": str(context_overlay_path(workspace, project)),
        "overlay_state": context_overlay_state(workspace, project, sha),
        "source_mode": metadata.get("mode") if metadata else None,
        "source": metadata.get("source") if metadata else None,
    }


def build_context(workspace: Workspace, project: Project) -> dict[str, Any]:
    instructions, skills = instruction_context(project)
    data = project.public()
    data["repository"] = project_status(project)
    data["instructions"] = instructions
    data["skills"] = skills
    data["profile"] = str(project.lane / "PROJECT.md")
    data["backlog"] = str(project.lane / "BACKLOG.md")
    data["tasks"] = str(project.lane / "tasks")
    data["knowledge_context"] = build_knowledge_context(workspace, project)
    return data


def command_context(workspace: Workspace, project: Project, as_json: bool) -> int:
    context = build_context(workspace, project)
    if as_json:
        print(json.dumps(context, indent=2, sort_keys=True))
        return 0
    print(f"Project: {project.display_name} ({project.id})")
    print(f"State: {project.status}")
    print(f"Repository: {project.path}")
    print(f"Lane: {project.lane}")
    print(f"Profile: {context['profile']}")
    print(f"Backlog: {context['backlog']}")
    print(f"Tasks: {context['tasks']}")
    print(f"Upstream: {project.upstream_repo} [{project.default_branch}]")
    learning_branch = (
        f"{project.fork_remote}/{project.learning_branch}"
        if project.learning_branch
        else "(not configured)"
    )
    print(f"Learning branch: {learning_branch}")
    knowledge = context["knowledge_context"]
    if knowledge:
        short_sha = knowledge["sha"][:12] if knowledge["sha"] else "unavailable"
        print(f"Knowledge ref: {knowledge['ref']}@{short_sha}")
        print(f"Context overlay: {knowledge['overlay']} [{knowledge['overlay_state']}]")
        if knowledge["always_load_bytes"] is not None:
            print(f"Always-load budget: {knowledge['always_load_bytes']}/{ALWAYS_LOAD_BUDGET_BYTES} bytes")
        print("Always load:")
        for item in knowledge["always_load"] or ["(none configured)"]:
            print(f"  - {item}")
    print("Instructions:")
    for item in context["instructions"] or ["(none discovered)"]:
        print(f"  - {item}")
    print("Project skills:")
    for item in context["skills"] or ["(none discovered)"]:
        print(f"  - {item}")
    print("Commands:")
    for kind, commands in sorted(project.commands.items()):
        print(f"  {kind}: {', '.join(commands) if commands else '(discover during onboarding)'}")
    return 0


def knowledge_doctor_messages(
    workspace: Workspace,
    project: Project,
    strict_context: bool,
) -> list[tuple[str, str]]:
    if not project.knowledge:
        return []
    sha = knowledge_ref_sha(project)
    if not sha:
        return [("ERROR", f"{project.id}: knowledge ref {project.knowledge.ref} is unavailable")]
    messages: list[tuple[str, str]] = []
    for path in knowledge_paths(project):
        if not git_path_exists(project, project.knowledge.ref, path):
            messages.append(
                ("ERROR", f"{project.id}: knowledge path is absent at {project.knowledge.ref}: {path}")
            )
    load_size = always_load_size(project)
    if len(project.knowledge.always_load) > ALWAYS_LOAD_BUDGET_FILES:
        messages.append(
            (
                "WARN",
                f"{project.id}: always-load file count exceeds {ALWAYS_LOAD_BUDGET_FILES}",
            )
        )
    if load_size is not None and load_size > ALWAYS_LOAD_BUDGET_BYTES:
        messages.append(
            (
                "WARN",
                f"{project.id}: always-load context is {load_size} bytes; "
                f"budget is {ALWAYS_LOAD_BUDGET_BYTES}",
            )
        )
    state = context_overlay_state(workspace, project, sha)
    if state == "current":
        metadata = read_context_metadata(workspace, project) or {}
        messages.append(
            (
                "OK",
                f"{project.id}: context overlay is current ({metadata.get('mode', 'unknown')}@{sha[:12]})",
            )
        )
    elif state == "missing":
        messages.append(
            (
                "ERROR" if strict_context else "INFO",
                f"{project.id}: context overlay is not materialized; run context-sync {project.id}",
            )
        )
    else:
        messages.append(
            (
                "ERROR" if strict_context else "WARN",
                f"{project.id}: context overlay is {state}; run context-sync {project.id}",
            )
        )
    return messages


def doctor_messages(
    workspace: Workspace,
    project: Project,
    strict_context: bool = False,
) -> list[tuple[str, str]]:
    messages: list[tuple[str, str]] = []
    lane_files = (project.lane / "PROJECT.md", project.lane / "BACKLOG.md", project.lane / "tasks")
    for lane_file in lane_files:
        if not lane_file.exists():
            messages.append(("ERROR", f"{project.id}: missing lane path {lane_file}"))
    task_root = project.lane / "tasks"
    if task_root.is_dir():
        for task_dir in sorted(path for path in task_root.iterdir() if path.is_dir()):
            task_file = task_dir / "task.toml"
            if not task_file.is_file():
                messages.append(("ERROR", f"{project.id}: missing task state {task_file}"))
                continue
            task = read_task(task_file)
            if "error" in task:
                messages.append(("ERROR", f"{project.id}: invalid task state {task_file}"))
            elif task.get("project") != project.id or task.get("slug") != task_dir.name:
                messages.append(("ERROR", f"{project.id}: task identity mismatch {task_file}"))
            elif task.get("status") not in TASK_STATUSES:
                messages.append(
                    ("ERROR", f"{project.id}: invalid task status in {task_file}")
                )
    if not project.path.exists():
        level = "ERROR" if project.status == "active" else "INFO"
        messages.append((level, f"{project.id}: repository path is absent ({project.path})"))
        return messages
    if git_output(project, "rev-parse", "--is-inside-work-tree") != "true":
        level = "ERROR" if project.status == "active" else "WARN"
        messages.append((level, f"{project.id}: path is not a Git worktree"))
        return messages

    expected_remotes = (
        (project.upstream_remote, project.upstream_url, "upstream"),
        (project.fork_remote, project.fork_url, "fork"),
    )
    for remote, expected, role in expected_remotes:
        if not expected:
            if role == "fork":
                messages.append(("INFO", f"{project.id}: personal fork is not registered yet"))
            continue
        actual = remote_url(project, remote)
        remote_level = "ERROR" if project.status == "active" and role == "upstream" else "WARN"
        if actual is None:
            messages.append((remote_level, f"{project.id}: missing {role} remote {remote!r}"))
        elif canonical_repo(actual) != canonical_repo(expected):
            messages.append(
                (remote_level, f"{project.id}: {remote} points to {actual}, expected {expected}")
            )
        if role == "upstream" and actual is not None:
            push_url = remote_push_url(project, remote)
            if push_url and push_url.upper() not in {"DISABLED", "NO_PUSH"}:
                messages.append(
                    (
                        "ERROR" if project.status == "active" else "WARN",
                        f"{project.id}: canonical upstream push URL is enabled ({push_url})",
                    )
                )

    default_refs = (
        f"{project.upstream_remote}/{project.default_branch}",
        f"{project.fork_remote}/{project.default_branch}",
        project.default_branch,
    )
    if not any(ref_exists(project, ref) for ref in default_refs):
        messages.append(("WARN", f"{project.id}: no local ref for default branch {project.default_branch}"))
    learning_refs = (project.learning_branch, f"{project.fork_remote}/{project.learning_branch}")
    if project.learning_branch and not any(ref_exists(project, ref) for ref in learning_refs):
        messages.append(("INFO", f"{project.id}: learning branch {project.learning_branch} is not available"))
    instructions, _ = instruction_context(project)
    if not any(item.endswith("AGENTS.md") for item in instructions):
        messages.append(("INFO", f"{project.id}: no AGENTS.md discovered on the worktree or learning ref"))
    messages.extend(knowledge_doctor_messages(workspace, project, strict_context))
    if not messages:
        messages.append(("OK", f"{project.id}: repository registration looks consistent"))
    return messages


def command_doctor(
    workspace: Workspace,
    projects: list[Project],
    as_json: bool,
    strict_context: bool,
) -> int:
    checks: list[dict[str, str]] = []
    if sys.version_info < (3, 11):
        checks.append({"level": "ERROR", "message": "Python 3.11 or newer is required"})
    else:
        checks.append({"level": "OK", "message": f"Python {sys.version.split()[0]}"})
    for project in projects:
        checks.extend(
            {"level": level, "message": message}
            for level, message in doctor_messages(workspace, project, strict_context)
        )
    if as_json:
        print(json.dumps(checks, indent=2, sort_keys=True))
    else:
        for check in checks:
            print(f"{check['level']:<5} {check['message']}")
    return 1 if any(check["level"] == "ERROR" for check in checks) else 0


def toml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def write_flat_toml(path: Path, data: dict[str, Any], key_order: tuple[str, ...]) -> None:
    """Atomically write the flat scalar schema used by task state files."""

    def encode(value: Any) -> str:
        if isinstance(value, str):
            return toml_quote(value)
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, int):
            return str(value)
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            return "[" + ", ".join(toml_quote(item) for item in value) + "]"
        raise WorkstationError(f"unsupported TOML value for {path}: {value!r}")

    ordered = [key for key in key_order if key in data]
    ordered.extend(sorted(key for key in data if key not in ordered))
    content = "\n".join(f"{key} = {encode(data[key])}" for key in ordered) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def command_project_add(args: argparse.Namespace, workspace: Workspace, projects: list[Project]) -> int:
    if not ID_PATTERN.fullmatch(args.project):
        raise WorkstationError("project id must use lowercase letters, digits, and hyphens")
    if args.status not in VALID_STATUSES:
        raise WorkstationError(f"invalid status: {args.status}")
    if not REPOSITORY_PATTERN.fullmatch(args.upstream_repo):
        raise WorkstationError("upstream repo must use OWNER/REPO format")
    for remote_name in (args.upstream_remote, args.fork_remote):
        if not REMOTE_PATTERN.fullmatch(remote_name):
            raise WorkstationError(f"invalid remote name: {remote_name}")
    for branch_name in (args.default_branch, args.learning_branch):
        if branch_name and (not BRANCH_PATTERN.fullmatch(branch_name) or ".." in branch_name):
            raise WorkstationError(f"invalid branch name: {branch_name}")
    if any(project.id == args.project for project in projects):
        raise WorkstationError(f"project already exists: {args.project}")
    source = workspace.project_dir / f"{args.project}.toml"
    lane = workspace.lanes_dir / args.project
    if source.exists() or lane.exists():
        raise WorkstationError(f"project files already exist for {args.project}")

    project_path = Path(args.path).expanduser()
    if not project_path.is_absolute():
        project_path = workspace.root / project_path
    try:
        stored_path = os.path.relpath(project_path.resolve(), workspace.root)
    except ValueError:
        stored_path = str(project_path.resolve())
    lane_value = str(lane.relative_to(workspace.root))
    values = {
        "id": args.project,
        "display_name": args.name,
        "status": args.status,
        "path": stored_path,
        "lane": lane_value,
        "upstream_repo": args.upstream_repo,
        "upstream_url": args.upstream_url,
        "upstream_remote": args.upstream_remote,
        "fork_url": args.fork_url or "",
        "fork_remote": args.fork_remote,
        "default_branch": args.default_branch,
        "learning_branch": args.learning_branch,
    }
    lines = ["schema_version = 1"]
    lines.extend(f"{key} = {toml_quote(value)}" for key, value in values.items())
    lines.append("domains = []")
    lines.append("native_skill_globs = []")
    lines.extend(["", "[commands]", "build = []", "test = []", "verify = []", "generate = []", ""])
    workspace.project_dir.mkdir(parents=True, exist_ok=True)
    source.write_text("\n".join(lines), encoding="utf-8")
    (lane / "tasks").mkdir(parents=True, exist_ok=False)
    (lane / "PROJECT.md").write_text(
        f"# {args.name}\n\nStatus: `{args.status}`\n\n"
        "## Sources\n\n- Add exact upstream refs and inspection dates.\n\n"
        "## Architecture\n\n- Map entry points, control plane, data plane, and tests.\n\n"
        "## Contribution Contract\n\n- Record current build, test, DCO, template, and reviewer rules.\n",
        encoding="utf-8",
    )
    (lane / "BACKLOG.md").write_text(
        f"# {args.name} Backlog\n\n| Priority | Candidate | Evidence | Status | Next action |\n"
        "| --- | --- | --- | --- | --- |\n",
        encoding="utf-8",
    )
    print(f"registered {args.project} in {source}")
    return 0


def write_task_files(
    task_dir: Path, project: Project, args: argparse.Namespace, worktree: Path | None
) -> None:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    task_dir.mkdir(parents=True, exist_ok=False)
    metadata = {
        "schema_version": 1,
        "project": project.id,
        "slug": args.slug,
        "title": args.title or args.slug.replace("-", " ").title(),
        "status": "planned",
        "created_at": timestamp,
        "updated_at": timestamp,
        "issue": args.issue or "",
        "branch": args.branch or "",
        "base": args.base or "",
        "worktree": str(worktree) if worktree else "",
    }
    write_flat_toml(
        task_dir / "task.toml",
        metadata,
        (
            "schema_version",
            "project",
            "slug",
            "title",
            "status",
            "created_at",
            "updated_at",
            "issue",
            "branch",
            "base",
            "worktree",
        ),
    )
    title = args.title or args.slug.replace("-", " ").title()
    (task_dir / "brief.md").write_text(
        f"# {title}\n\n## Problem\n\n## Scope\n\n## Non-Goals\n\n"
        "## File Matrix\n\n| Area | Why | Risk | Validation |\n| --- | --- | --- | --- |\n\n"
        "## Plan\n\n## Decision Log\n",
        encoding="utf-8",
    )
    (task_dir / "evidence.md").write_text(
        "# Evidence\n\n| Time | Kind | Source / command | Result | Claim supported |\n"
        "| --- | --- | --- | --- | --- |\n",
        encoding="utf-8",
    )
    (task_dir / "upstream-draft.md").write_text(
        "# Upstream Draft\n\nTarget: not selected\n\nNo upstream action is authorized by this file. "
        "Obtain approval for the exact target and text before posting.\n",
        encoding="utf-8",
    )


def choose_base(project: Project, requested: str | None) -> str:
    candidates = [requested] if requested else [
        f"{project.upstream_remote}/{project.default_branch}",
        f"{project.fork_remote}/{project.default_branch}",
        project.default_branch,
    ]
    for candidate in candidates:
        if candidate and ref_exists(project, candidate):
            return candidate
    raise WorkstationError(
        f"cannot resolve a base ref for {project.id}; fetch remotes or pass --base explicitly"
    )


def command_task_create(args: argparse.Namespace, workspace: Workspace, project: Project) -> int:
    if not ID_PATTERN.fullmatch(args.slug):
        raise WorkstationError("task slug must use lowercase letters, digits, and hyphens")
    task_dir = project.lane / "tasks" / args.slug
    if task_dir.exists():
        raise WorkstationError(f"task already exists: {task_dir}")
    worktree: Path | None = None
    if args.worktree:
        if not args.branch or not BRANCH_PATTERN.fullmatch(args.branch) or ".." in args.branch:
            raise WorkstationError("--worktree requires a valid --branch")
        if not project.path.exists():
            raise WorkstationError(f"repository does not exist: {project.path}")
        worktree = workspace.worktrees_dir / project.id / args.slug
        if worktree.exists():
            raise WorkstationError(f"worktree path already exists: {worktree}")
        base = choose_base(project, args.base)
        worktree.parent.mkdir(parents=True, exist_ok=True)
        result = run_git(project, "worktree", "add", "-b", args.branch, str(worktree), base, timeout=120)
        if result.returncode != 0:
            raise WorkstationError(result.stderr.strip() or "git worktree add failed")
        args.base = base
    write_task_files(task_dir, project, args, worktree)
    print(f"created task {project.id}/{args.slug}")
    if worktree:
        print(f"worktree: {worktree}")
    return 0


def read_task(task_file: Path) -> dict[str, Any]:
    try:
        data = tomllib.loads(task_file.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return {"path": str(task_file.parent), "error": str(exc)}
    data["path"] = str(task_file.parent)
    return data


def command_task_list(projects: list[Project], as_json: bool) -> int:
    tasks: list[dict[str, Any]] = []
    for project in projects:
        task_root = project.lane / "tasks"
        if task_root.is_dir():
            tasks.extend(read_task(path) for path in sorted(task_root.glob("*/task.toml")))
    if as_json:
        print(json.dumps(tasks, indent=2, sort_keys=True))
        return 0
    rows = [
        [
            str(task.get("project", "?")),
            str(task.get("slug", "?")),
            str(task.get("status", "?")),
            str(task.get("branch", "-")) or "-",
            str(task.get("title", "?")),
        ]
        for task in tasks
    ]
    print_table(["PROJECT", "TASK", "STATE", "BRANCH", "TITLE"], rows)
    return 0


def command_task_status(project: Project, slug: str, status: str) -> int:
    if not ID_PATTERN.fullmatch(slug):
        raise WorkstationError("task slug must use lowercase letters, digits, and hyphens")
    task_file = project.lane / "tasks" / slug / "task.toml"
    if not task_file.is_file():
        raise WorkstationError(f"task does not exist: {project.id}/{slug}")
    task = read_task(task_file)
    if "error" in task:
        raise WorkstationError(f"cannot read {task_file}: {task['error']}")
    task.pop("path", None)
    if task.get("project") != project.id or task.get("slug") != slug:
        raise WorkstationError(f"task identity mismatch in {task_file}")
    task["status"] = status
    task["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    write_flat_toml(
        task_file,
        task,
        (
            "schema_version",
            "project",
            "slug",
            "title",
            "status",
            "created_at",
            "updated_at",
            "issue",
            "branch",
            "base",
            "worktree",
        ),
    )
    print(f"updated {project.id}/{slug} to {status}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="list registered projects")
    list_parser.add_argument("--json", action="store_true")

    status_parser = subparsers.add_parser("status", help="show local Git state")
    status_parser.add_argument("projects", nargs="*")
    status_parser.add_argument("--json", action="store_true")

    doctor_parser = subparsers.add_parser("doctor", help="validate workstation registration")
    doctor_parser.add_argument("projects", nargs="*")
    doctor_parser.add_argument("--json", action="store_true")
    doctor_parser.add_argument(
        "--context",
        action="store_true",
        help="require configured context overlays to be current",
    )

    context_parser = subparsers.add_parser("context", help="show one project's complete context")
    context_parser.add_argument("project")
    context_parser.add_argument("--json", action="store_true")

    context_sync = subparsers.add_parser(
        "context-sync",
        help="materialize project knowledge overlays",
    )
    context_sync.add_argument("projects", nargs="*")
    context_sync.add_argument("--json", action="store_true")

    add_parser = subparsers.add_parser("project-add", help="create a project registration and lane")
    add_parser.add_argument("project")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--path", required=True)
    add_parser.add_argument("--upstream-repo", required=True)
    add_parser.add_argument("--upstream-url", required=True)
    add_parser.add_argument("--upstream-remote", default="upstream")
    add_parser.add_argument("--fork-url")
    add_parser.add_argument("--fork-remote", default="origin")
    add_parser.add_argument("--default-branch", default="main")
    add_parser.add_argument("--learning-branch", default="intern")
    add_parser.add_argument("--status", choices=sorted(VALID_STATUSES), default="planned")

    task_create = subparsers.add_parser("task-create", help="create an isolated contribution task")
    task_create.add_argument("project")
    task_create.add_argument("slug")
    task_create.add_argument("--title")
    task_create.add_argument("--issue")
    task_create.add_argument("--worktree", action="store_true")
    task_create.add_argument("--branch")
    task_create.add_argument("--base")

    task_list = subparsers.add_parser("task-list", help="list contribution tasks")
    task_list.add_argument("projects", nargs="*")
    task_list.add_argument("--json", action="store_true")

    task_status = subparsers.add_parser("task-status", help="update a task's lifecycle state")
    task_status.add_argument("project")
    task_status.add_argument("slug")
    task_status.add_argument("status", choices=TASK_STATUSES)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        workspace, projects = load_registry(args.config)
        if args.command == "list":
            return command_list(projects, args.json)
        if args.command == "status":
            return command_status(select_projects(projects, args.projects), args.json)
        if args.command == "doctor":
            return command_doctor(
                workspace,
                select_projects(projects, args.projects),
                args.json,
                args.context,
            )
        if args.command == "context":
            return command_context(
                workspace,
                select_projects(projects, [args.project])[0],
                args.json,
            )
        if args.command == "context-sync":
            selected = select_projects(projects, args.projects)
            if not args.projects:
                selected = [project for project in selected if project.knowledge]
            return command_context_sync(workspace, selected, args.json)
        if args.command == "project-add":
            return command_project_add(args, workspace, projects)
        if args.command == "task-create":
            return command_task_create(args, workspace, select_projects(projects, [args.project])[0])
        if args.command == "task-list":
            return command_task_list(select_projects(projects, args.projects), args.json)
        if args.command == "task-status":
            return command_task_status(
                select_projects(projects, [args.project])[0], args.slug, args.status
            )
        raise WorkstationError(f"unsupported command: {args.command}")
    except WorkstationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
