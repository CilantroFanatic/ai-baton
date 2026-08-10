from __future__ import annotations

from pathlib import Path

# Mirrors SPEC.md section 4's mandatory read order (steps 1-3; step 4 is
# task-specific and not something this command can know about).
READ_ORDER = [
    "PROTOCOL.md",
    "memory/INDEX.md",
    "status/CURRENT_STATUS.md",
]


def run(target: Path) -> str:
    """Concatenate the mandatory read-order files into one printable blob.

    Meant to be piped straight into a fresh AI session or read by a human
    as the "cold start" context for a project.
    """
    sections = []
    for rel in READ_ORDER:
        path = target / rel
        if not path.is_file():
            raise FileNotFoundError(
                f"expected {rel} under {target}, not found (run 'init' first?)"
            )
        sections.append(f"===== {rel} =====\n{path.read_text(encoding='utf-8').rstrip()}\n")
    return "\n".join(sections)
