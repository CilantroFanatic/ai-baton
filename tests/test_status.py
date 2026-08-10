from pathlib import Path

import pytest

from ai_baton.commands import status

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_PROJECT = REPO_ROOT / "examples" / "demo-project"


def test_status_concatenates_read_order() -> None:
    output = status.run(DEMO_PROJECT)

    assert "PROTOCOL.md" in output
    assert "memory/INDEX.md" in output
    assert "status/CURRENT_STATUS.md" in output
    assert output.index("===== PROTOCOL.md") < output.index("===== memory/INDEX.md")
    assert output.index("===== memory/INDEX.md") < output.index("===== status/CURRENT_STATUS.md")


def test_status_raises_when_missing_files(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        status.run(tmp_path)
