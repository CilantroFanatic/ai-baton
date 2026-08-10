from pathlib import Path

from ai_baton.commands import init, workspace


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
