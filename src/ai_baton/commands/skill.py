from __future__ import annotations

from pathlib import Path

SKILL_NAME = "ai-baton"
PACKAGED_SKILL = Path(__file__).resolve().parent.parent / "skill" / "SKILL.md"

DEFAULT_TARGETS = [
    Path.home() / ".claude" / "skills",
    Path.home() / ".agents" / "skills",
]


def install(targets: list[Path] | None = None) -> list[str]:
    """Write the packaged SKILL.md into one or more skills/ directories.

    Each target gets a `<target>/ai-baton/SKILL.md`. With no targets, installs
    into both of the well-known global locations (Claude Code's own lookup
    path, and the shared Agent Skills convention other tools scan).
    """
    messages: list[str] = []
    dirs = targets if targets else DEFAULT_TARGETS
    content = PACKAGED_SKILL.read_text(encoding="utf-8")
    for base in dirs:
        dest_dir = base / SKILL_NAME
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / "SKILL.md"
        dest_file.write_text(content, encoding="utf-8")
        messages.append(f"installed {dest_file}")
    return messages
