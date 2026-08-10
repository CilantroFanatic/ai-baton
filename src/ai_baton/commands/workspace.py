from __future__ import annotations

import json
from pathlib import Path

FALLBACK_WORKSPACE = Path.home() / "ai-baton-workspace"
GLOBAL_CONFIG_FILE = Path.home() / ".ai-baton" / "config.json"


def resolve_default_workspace() -> Path:
    """Where `ai-baton list`/the skill look when no path is given.

    Checks ~/.ai-baton/config.json's "workspace" key first -- set once,
    the first time a user picks (or confirms) where their workspace should
    live, so later sessions don't have to ask again. Falls back to
    ~/ai-baton-workspace if there's no config, or it's malformed/unusable.
    """
    if GLOBAL_CONFIG_FILE.is_file():
        try:
            data = json.loads(GLOBAL_CONFIG_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return FALLBACK_WORKSPACE
        configured = data.get("workspace") if isinstance(data, dict) else None
        if isinstance(configured, str) and configured.strip():
            return Path(configured).expanduser()
    return FALLBACK_WORKSPACE


def set_default_workspace(path: Path) -> None:
    """Persist the user's chosen workspace root for future sessions."""
    GLOBAL_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if GLOBAL_CONFIG_FILE.is_file():
        try:
            existing = json.loads(GLOBAL_CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(existing, dict):
                data = existing
        except json.JSONDecodeError:
            pass
    data["workspace"] = str(path)
    GLOBAL_CONFIG_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def list_projects(workspace: Path | None = None) -> list[str]:
    """List ai-baton projects (dirs containing PROTOCOL.md) under a workspace.

    Meant for a fresh session on a possibly-new tool to discover what
    already exists without the user having to repeat a path from memory.
    """
    base = workspace if workspace is not None else resolve_default_workspace()
    if not base.is_dir():
        return [f"no workspace at {base} (nothing created there yet)"]

    lines: list[str] = [f"workspace: {base}"]
    found = False
    for entry in sorted(base.iterdir()):
        if not entry.is_dir() or not (entry / "PROTOCOL.md").is_file():
            continue
        found = True
        goal = _current_goal(entry)
        lines.append(f"  {entry.name}: {goal}" if goal else f"  {entry.name}")

    if not found:
        lines.append("  (no ai-baton projects found)")
    return lines


def _current_goal(project: Path) -> str | None:
    status_file = project / "status" / "CURRENT_STATUS.md"
    if not status_file.is_file():
        return None
    lines = status_file.read_text(encoding="utf-8").splitlines()
    try:
        heading = next(i for i, line in enumerate(lines) if line.strip() == "## Current goal")
    except StopIteration:
        return None
    placeholders = {"...", "(fill in)"}
    for line in lines[heading + 1 :]:
        stripped = line.strip()
        if stripped.startswith("##"):
            break
        if stripped and stripped not in placeholders:
            return stripped
    return None
