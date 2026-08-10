from __future__ import annotations

from datetime import date
from pathlib import Path

DIRS = ["memory", "status", "evidence", "handover", "archive"]

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

# (destination relative to project root, template filename)
TEMPLATED_FILES = [
    ("PROTOCOL.md", "PROTOCOL.md.tmpl"),
    ("memory/INDEX.md", "memory_INDEX.md.tmpl"),
    ("status/CURRENT_STATUS.md", "status_CURRENT_STATUS.md.tmpl"),
    ("handover/README.md", "handover_README.md.tmpl"),
    ("archive/README.md", "archive_README.md.tmpl"),
]


def run(target: Path) -> list[str]:
    """Scaffold the ai-baton directory structure under `target`.

    Existing files and directories are left untouched — init is safe to
    re-run on a project that already has content in it. Returns a list of
    human-readable messages describing what happened.
    """
    messages: list[str] = []
    target.mkdir(parents=True, exist_ok=True)

    for name in DIRS:
        d = target / name
        if d.exists():
            messages.append(f"skip   {name}/ (already exists)")
        else:
            d.mkdir(parents=True)
            messages.append(f"create {name}/")

    today = date.today().isoformat()
    for rel_dest, template_name in TEMPLATED_FILES:
        _write_from_template(target / rel_dest, template_name, today, messages)

    return messages


def _write_from_template(
    dest: Path, template_name: str, today: str, messages: list[str]
) -> None:
    if dest.exists():
        messages.append(f"skip   {dest} (already exists)")
        return
    content = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    content = content.format(date=today)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    messages.append(f"create {dest}")
