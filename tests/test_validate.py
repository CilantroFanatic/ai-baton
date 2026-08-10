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


def test_aws_key_pattern_is_flagged(tmp_path: Path) -> None:
    _scaffold_minimum(tmp_path)
    (tmp_path / "evidence" / "notes.md").write_text(
        "accidentally pasted: AKIAIOSFODNN7EXAMPLE\n"
    )

    result = validate.run(tmp_path)

    assert any("AWS Access Key ID" in e for e in result.errors)


def test_private_key_block_is_flagged(tmp_path: Path) -> None:
    _scaffold_minimum(tmp_path)
    (tmp_path / "evidence" / "notes.md").write_text(
        "-----BEGIN RSA PRIVATE KEY-----\nMIIExample==\n-----END RSA PRIVATE KEY-----\n"
    )

    result = validate.run(tmp_path)

    assert any("PEM private key block" in e for e in result.errors)


def test_secret_value_is_never_echoed_in_the_error(tmp_path: Path) -> None:
    _scaffold_minimum(tmp_path)
    secret = "AKIAIOSFODNN7EXAMPLE"
    (tmp_path / "evidence" / "notes.md").write_text(f"key: {secret}\n")

    result = validate.run(tmp_path)

    assert not any(secret in e for e in result.errors)
    assert any("redacted" in e for e in result.errors)


def test_ordinary_content_does_not_false_positive_as_a_secret(tmp_path: Path) -> None:
    _scaffold_minimum(tmp_path)
    (tmp_path / "evidence" / "notes.md").write_text(
        "Normal notes about the project, a UUID like "
        "550e8400-e29b-41d4-a716-446655440000, and a sentence with the "
        "word skeleton in it.\n"
    )

    result = validate.run(tmp_path)

    assert result.ok


def test_unrelated_sibling_content_is_not_scanned(tmp_path: Path) -> None:
    # Regression test: a real user ran `ai-baton init` directly on a large,
    # pre-existing directory (their whole ~/Documents) that also contained
    # unrelated projects with node_modules/ full of third-party READMEs with
    # their own (unrelated, often broken-looking) relative links. validate
    # scanned all of it and produced thousands of false-positive "broken
    # link" errors that had nothing to do with the ai-baton project itself.
    _scaffold_minimum(tmp_path)
    vendor_readme = (
        tmp_path
        / "some-other-project"
        / "node_modules"
        / "some-package"
        / "README.md"
    )
    vendor_readme.parent.mkdir(parents=True)
    vendor_readme.write_text("[nowhere](./does-not-exist-either.md)\n")

    result = validate.run(tmp_path)

    assert result.ok
    assert not any("some-other-project" in e for e in result.errors)
