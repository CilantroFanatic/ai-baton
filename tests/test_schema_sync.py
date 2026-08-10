from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_root_and_packaged_schema_copies_match() -> None:
    """The repo-root schemas/ copy (referenced by SPEC.md) and the copy
    shipped inside the package (loaded at runtime by validate.py) must stay
    identical — this test exists so they can't silently drift apart.
    """
    root = (REPO_ROOT / "schemas" / "memory-frontmatter.schema.json").read_text()
    packaged = (
        REPO_ROOT
        / "src"
        / "ai_handoff_protocol"
        / "schemas"
        / "memory-frontmatter.schema.json"
    ).read_text()
    assert root == packaged
