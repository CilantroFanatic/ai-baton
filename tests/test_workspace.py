from pathlib import Path

import pytest

from ai_baton.commands import init, workspace


@pytest.fixture
def isolated_global_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    # Never touch the developer's real ~/.ai-baton/config.json during tests.
    config_file = tmp_path / "home" / ".ai-baton" / "config.json"
    fallback = tmp_path / "home" / "ai-baton-workspace"
    monkeypatch.setattr(workspace, "GLOBAL_CONFIG_FILE", config_file)
    monkeypatch.setattr(workspace, "FALLBACK_WORKSPACE", fallback)
    return config_file


def test_resolve_default_workspace_falls_back_when_no_config(
    isolated_global_config: Path,
) -> None:
    assert workspace.resolve_default_workspace() == workspace.FALLBACK_WORKSPACE


def test_set_then_resolve_default_workspace_persists_the_choice(
    isolated_global_config: Path, tmp_path: Path
) -> None:
    chosen = tmp_path / "somewhere-else" / "my-workspace"

    workspace.set_default_workspace(chosen)

    assert workspace.resolve_default_workspace() == chosen
    assert isolated_global_config.is_file()


def test_malformed_global_config_falls_back_silently(
    isolated_global_config: Path,
) -> None:
    isolated_global_config.parent.mkdir(parents=True)
    isolated_global_config.write_text("{not valid json")

    assert workspace.resolve_default_workspace() == workspace.FALLBACK_WORKSPACE


def test_set_default_workspace_preserves_other_config_keys(
    isolated_global_config: Path, tmp_path: Path
) -> None:
    isolated_global_config.parent.mkdir(parents=True)
    isolated_global_config.write_text('{"some_other_setting": true}')

    workspace.set_default_workspace(tmp_path / "chosen")

    import json

    data = json.loads(isolated_global_config.read_text())
    assert data["some_other_setting"] is True
    assert data["workspace"] == str(tmp_path / "chosen")


def test_list_projects_with_no_argument_uses_resolved_default(
    isolated_global_config: Path, tmp_path: Path
) -> None:
    chosen = tmp_path / "custom-root"
    workspace.set_default_workspace(chosen)
    init.run(chosen / "thesis")

    lines = workspace.list_projects()  # no explicit workspace argument

    assert any(str(chosen) in line for line in lines)
    assert any("thesis" in line for line in lines)


def test_list_projects_reports_missing_workspace(tmp_path: Path) -> None:
    missing = tmp_path / "does-not-exist"
    lines = workspace.list_projects(missing)
    assert any("no workspace" in line for line in lines)


def test_list_projects_finds_a_project(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    project = ws / "thesis"
    init.run(project)
    (project / "status" / "CURRENT_STATUS.md").write_text(
        "Last updated: 2026-01-01\n\n## Current goal\n\nFinish chapter 3.\n"
    )

    lines = workspace.list_projects(ws)

    assert any("thesis" in line and "Finish chapter 3." in line for line in lines)


def test_list_projects_does_not_show_template_placeholder_as_a_goal(
    tmp_path: Path,
) -> None:
    ws = tmp_path / "ws"
    project = ws / "fresh"
    init.run(project)  # status/CURRENT_STATUS.md still has "(fill in)" placeholders

    lines = workspace.list_projects(ws)

    assert any(line.strip() == "fresh" for line in lines)
    assert not any("fill in" in line for line in lines)


def test_list_projects_skips_dirs_without_protocol(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    ws.mkdir()
    (ws / "not-a-project").mkdir()

    lines = workspace.list_projects(ws)

    assert any("no ai-baton projects found" in line for line in lines)
    assert not any("not-a-project" in line for line in lines)


def test_upsert_project_writes_a_manifest_entry(tmp_path: Path) -> None:
    ws = tmp_path / "ws"

    workspace.upsert_project(ws, "thesis", "Finish chapter 3")

    import json

    data = json.loads((ws / workspace.MANIFEST_FILE).read_text())
    assert data["projects"]["thesis"]["description"] == "Finish chapter 3"
    assert "updated" in data["projects"]["thesis"]


def test_upsert_project_ignores_empty_description(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    workspace.upsert_project(ws, "thesis", "Finish chapter 3")

    workspace.upsert_project(ws, "thesis", None)

    import json

    data = json.loads((ws / workspace.MANIFEST_FILE).read_text())
    assert data["projects"]["thesis"]["description"] == "Finish chapter 3"


def test_list_projects_prefers_the_manifest_over_reading_status(
    tmp_path: Path,
) -> None:
    ws = tmp_path / "ws"
    project = ws / "thesis"
    init.run(project)
    (project / "status" / "CURRENT_STATUS.md").write_text(
        "Last updated: 2026-01-01\n\n## Current goal\n\nReal file says X.\n"
    )
    workspace.upsert_project(ws, "thesis", "Manifest says Y")

    lines = workspace.list_projects(ws)

    assert any("Manifest says Y" in line for line in lines)
    assert not any("Real file says X" in line for line in lines)


def test_list_projects_backfills_the_manifest_for_a_project_missing_from_it(
    tmp_path: Path,
) -> None:
    ws = tmp_path / "ws"
    project = ws / "thesis"
    init.run(project)
    (project / "status" / "CURRENT_STATUS.md").write_text(
        "Last updated: 2026-01-01\n\n## Current goal\n\nFinish chapter 3.\n"
    )
    # No manifest exists yet -- simulates a project created before this
    # feature, or without the CLI.

    lines = workspace.list_projects(ws)
    assert any("Finish chapter 3." in line for line in lines)

    import json

    data = json.loads((ws / workspace.MANIFEST_FILE).read_text())
    assert data["projects"]["thesis"]["description"] == "Finish chapter 3."


def test_list_projects_does_not_open_a_sibling_projects_status_file_when_cached(
    tmp_path: Path,
) -> None:
    """Once the manifest has an entry, list_projects must not need to read
    that project's status file at all -- the whole point of the cache is to
    avoid opening other projects' files (see SKILL.md Step 1)."""
    ws = tmp_path / "ws"
    project = ws / "thesis"
    init.run(project)
    workspace.upsert_project(ws, "thesis", "Cached goal")
    status_file = project / "status" / "CURRENT_STATUS.md"
    status_file.unlink()  # if list_projects tried to read it, this would raise

    lines = workspace.list_projects(ws)

    assert any("Cached goal" in line for line in lines)
