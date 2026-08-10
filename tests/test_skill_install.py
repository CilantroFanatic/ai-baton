from pathlib import Path

from ai_baton.commands import skill

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_packaged_skill_matches_canonical_copy() -> None:
    # The repo-root .agents/skills/ai-baton/SKILL.md (what ships in the repo
    # and gets symlinked by contributors) and the copy packaged inside
    # src/ai_baton/skill/ (what `pip install`-ed users get via `ai-baton
    # skill install`) must stay identical.
    canonical = (
        REPO_ROOT / ".agents" / "skills" / "ai-baton" / "SKILL.md"
    ).read_text()
    packaged = (REPO_ROOT / "src" / "ai_baton" / "skill" / "SKILL.md").read_text()
    assert canonical == packaged


def test_install_writes_skill_into_each_target(tmp_path: Path) -> None:
    target_a = tmp_path / "a"
    target_b = tmp_path / "b"

    messages = skill.install([target_a, target_b])

    for target in (target_a, target_b):
        dest = target / "ai-baton" / "SKILL.md"
        assert dest.is_file()
        assert dest.read_text() == skill.PACKAGED_SKILL.read_text()
    assert len(messages) == 2


def test_install_is_safe_to_rerun(tmp_path: Path) -> None:
    skill.install([tmp_path])
    skill.install([tmp_path])  # should just overwrite, not error
    assert (tmp_path / "ai-baton" / "SKILL.md").is_file()
