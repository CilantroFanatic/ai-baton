from pathlib import Path

import pytest

from ai_baton import __version__, cli


def test_version_flag_reports_the_installed_version(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--version"])

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert __version__ in captured.out


def test_version_is_not_the_stale_hardcoded_0_0_1() -> None:
    # Regression: __version__ used to be hand-written in __init__.py and
    # never got bumped alongside pyproject.toml across a dozen releases.
    # Now it's read from installed package metadata, so this can't drift.
    assert __version__ != "0.0.1"


def test_unwritable_path_gives_a_clean_error_not_a_traceback(capsys, tmp_path: Path) -> None:
    # A path under a location that can't be created (parent doesn't exist
    # and isn't creatable) used to raise a raw Python traceback.
    bad_path = tmp_path / "does-not-exist-and-is-read-only" / "project"
    tmp_path.chmod(0o500)  # read-only: nothing can be created under it
    try:
        exit_code = cli.main(["init", str(bad_path)])
    finally:
        tmp_path.chmod(0o700)  # restore so pytest can clean up tmp_path

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Traceback" not in captured.err
    assert "ERROR" in captured.err
    assert "try again" in captured.err


def test_init_via_cli_still_works_normally(tmp_path: Path, capsys) -> None:
    exit_code = cli.main(["init", str(tmp_path / "proj")])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "create" in captured.out
    assert (tmp_path / "proj" / "PROTOCOL.md").is_file()


def test_workspace_set_via_cli_persists_and_list_picks_it_up(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ai_baton.commands import workspace as workspace_cmd

    monkeypatch.setattr(workspace_cmd, "GLOBAL_CONFIG_FILE", tmp_path / "config.json")
    chosen = tmp_path / "my-chosen-workspace"

    exit_code = cli.main(["workspace", "set", str(chosen)])
    capsys.readouterr()

    assert exit_code == 0
    assert workspace_cmd.resolve_default_workspace() == chosen


def test_list_via_cli_reports_missing_workspace(tmp_path: Path, capsys) -> None:
    exit_code = cli.main(["list", str(tmp_path / "no-workspace-here")])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "no workspace at" in captured.out
