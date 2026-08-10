from pathlib import Path

from ai_baton.commands import validate

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_PROJECT = REPO_ROOT / "examples" / "demo-project"


def _scaffold_minimum(tmp_path: Path) -> None:
    for name in ["memory", "status", "evidence", "handover", "archive"]:
        (tmp_path / name).mkdir()
    (tmp_path / "PROTOCOL.md").write_text("protocol\n")
    (tmp_path / "status" / "CURRENT_STATUS.md").write_text("Last updated: 2026-01-01\n")


def test_demo_project_validates_clean() -> None:
    result = validate.run(DEMO_PROJECT)
    assert result.errors == []


def test_missing_required_dir_is_an_error(tmp_path: Path) -> None:
    for name in ["memory", "status", "evidence", "handover"]:
        (tmp_path / name).mkdir()
    (tmp_path / "PROTOCOL.md").write_text("protocol\n")
    (tmp_path / "status" / "CURRENT_STATUS.md").write_text("Last updated: 2026-01-01\n")

    result = validate.run(tmp_path)

    assert any("archive" in e for e in result.errors)
    assert not result.ok


def test_missing_protocol_file_is_an_error(tmp_path: Path) -> None:
    _scaffold_minimum(tmp_path)
    (tmp_path / "PROTOCOL.md").unlink()

    result = validate.run(tmp_path)

    assert any("PROTOCOL.md" in e for e in result.errors)


def test_invalid_frontmatter_is_an_error(tmp_path: Path) -> None:
    _scaffold_minimum(tmp_path)
    bad = tmp_path / "memory" / "bad.md"
    bad.write_text("---\nid: x\n---\n\nno date, no confidence, no source\n")

    result = validate.run(tmp_path)

    assert any("bad.md" in e for e in result.errors)


def test_missing_frontmatter_is_an_error(tmp_path: Path) -> None:
    _scaffold_minimum(tmp_path)
    (tmp_path / "memory" / "no-frontmatter.md").write_text("just prose, no frontmatter\n")

    result = validate.run(tmp_path)

    assert any("missing YAML frontmatter" in e for e in result.errors)


def test_broken_link_is_an_error(tmp_path: Path) -> None:
    _scaffold_minimum(tmp_path)
    note = tmp_path / "memory" / "note.md"
    note.write_text(
        "---\nid: note\ndate: 2026-01-01\nconfidence: verified\nsource: x\n---\n\n"
        "[nowhere](./does-not-exist.md)\n"
    )

    result = validate.run(tmp_path)

    assert any("broken link" in e for e in result.errors)


def test_stale_status_is_a_warning_not_an_error(tmp_path: Path) -> None:
    _scaffold_minimum(tmp_path)
    (tmp_path / "status" / "CURRENT_STATUS.md").write_text("Last updated: 2000-01-01\n")

    result = validate.run(tmp_path)

    assert result.ok
    assert any("stale" in w for w in result.warnings)
