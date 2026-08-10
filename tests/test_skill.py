import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "ai-baton"
SKILL_FILE = SKILL_DIR / "SKILL.md"

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def test_skill_file_exists():
    assert SKILL_FILE.is_file()


def test_skill_name_matches_directory_name():
    # Per the Agent Skills spec, a skill's frontmatter `name` must match its
    # parent directory name, or the skill silently fails to load in tools
    # that implement the spec.
    text = SKILL_FILE.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    assert match, "SKILL.md must start with YAML frontmatter"
    data = yaml.safe_load(match.group(1))
    assert data["name"] == SKILL_DIR.name


def test_skill_has_a_description():
    text = SKILL_FILE.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    data = yaml.safe_load(match.group(1))
    assert isinstance(data.get("description"), str)
    assert len(data["description"]) > 20
