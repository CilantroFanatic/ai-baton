from __future__ import annotations

from pathlib import Path

DEFAULT_WORKSPACE = Path.home() / "ai-baton-workspace"


def list_projects(workspace: Path | None = None) -> list[str]:
    """List ai-baton projects (dirs containing PROTOCOL.md) under a workspace.

    Meant for a fresh session on a possibly-new tool to discover what
    already exists without the user having to repeat a path from memory.
    """
    base = workspace if workspace is not None else DEFAULT_WORKSPACE
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
