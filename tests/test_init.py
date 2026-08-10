from pathlib import Path

from ai_baton.commands import init


def test_init_creates_expected_structure(tmp_path: Path) -> None:
    messages = init.run(tmp_path)

    for name in ["memory", "status", "evidence", "handover", "archive"]:
        assert (tmp_path / name).is_dir()

    assert (tmp_path / "PROTOCOL.md").is_file()
    assert (tmp_path / "memory" / "INDEX.md").is_file()
    assert (tmp_path / "status" / "CURRENT_STATUS.md").is_file()
    assert (tmp_path / "handover" / "README.md").is_file()
    assert (tmp_path / "archive" / "README.md").is_file()
    assert any(m.startswith("create") for m in messages)


def test_init_status_template_has_last_updated_line(tmp_path: Path) -> None:
    init.run(tmp_path)
    text = (tmp_path / "status" / "CURRENT_STATUS.md").read_text()
    assert "Last updated:" in text


def test_init_is_idempotent_and_does_not_overwrite(tmp_path: Path) -> None:
    init.run(tmp_path)

    custom = "Last updated: 2020-01-01\nUpdated by: someone\n\nmy own status\n"
    status_file = tmp_path / "status" / "CURRENT_STATUS.md"
    status_file.write_text(custom)

    messages = init.run(tmp_path)

    assert status_file.read_text() == custom
    assert any("skip" in m for m in messages)
