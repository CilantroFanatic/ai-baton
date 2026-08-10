from __future__ import annotations

import datetime as _dt
import json
import re
from dataclasses import dataclass, field
from datetime import date as date_cls
from pathlib import Path

import yaml
from jsonschema import Draft7Validator

REQUIRED_DIRS = ["memory", "status", "evidence", "handover", "archive"]
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "memory-frontmatter.schema.json"
CONFIG_FILE = ".ai-baton.json"

STALE_STATUS_DAYS = 30

# Rough chars-per-token estimate (no tokenizer dependency -- this is a
# heads-up, not a precise budget). ~50,000 chars is generous headroom for
# an actively curated memory/ (SPEC.md 3.1: one fact per file, kept
# short) before it's worth archiving stale entries out of the active index.
DEFAULT_MEMORY_SIZE_WARNING_CHARS = 50_000

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n?", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# Heuristic safety net for SPEC.md section 6.6 ("never write credentials
# into any file here"), not a comprehensive secrets scanner -- high-
# confidence, well-known formats only, to keep false positives low.
SECRET_PATTERNS = [
    ("AWS Access Key ID", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("Slack token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("Anthropic API key", re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}")),
    ("API key (sk- prefix)", re.compile(r"sk-(?!ant-)[A-Za-z0-9]{20,}")),
    (
        "PEM private key block",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    (
        "JWT-looking token",
        re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    ),
]


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def run(target: Path) -> Result:
    result = Result()
    config = _load_config(target, result)
    _check_required_dirs(target, result)
    _check_protocol_file(target, result)
    _check_current_status(target, result)
    _check_memory_frontmatter(target, result)
    _check_internal_links(target, result)
    _check_no_secrets(target, result)
    _check_memory_size(target, result, config)
    return result


def _load_config(target: Path, result: Result) -> dict:
    """Optional per-project overrides, e.g. {"memory_size_warning_chars": N}.

    Missing file is normal (defaults apply). A present-but-malformed file is
    reported as a warning rather than silently ignored or crashing validate.
    """
    config_path = target / CONFIG_FILE
    if not config_path.is_file():
        return {}
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.warnings.append(f"{CONFIG_FILE}: invalid JSON, ignoring it ({exc})")
        return {}
    if not isinstance(data, dict):
        result.warnings.append(f"{CONFIG_FILE}: expected a JSON object, ignoring it")
        return {}
    return data


def _check_required_dirs(target: Path, result: Result) -> None:
    for name in REQUIRED_DIRS:
        if not (target / name).is_dir():
            result.errors.append(f"missing required directory: {name}/")


def _check_protocol_file(target: Path, result: Result) -> None:
    if not (target / "PROTOCOL.md").is_file():
        result.errors.append("missing PROTOCOL.md")


def _check_current_status(target: Path, result: Result) -> None:
    status_file = target / "status" / "CURRENT_STATUS.md"
    if not status_file.is_file():
        result.errors.append("missing status/CURRENT_STATUS.md")
        return

    text = status_file.read_text(encoding="utf-8")
    if not text.strip():
        result.errors.append("status/CURRENT_STATUS.md is empty")
        return

    match = re.search(r"Last updated:\s*(\d{4}-\d{2}-\d{2})", text)
    if not match:
        result.warnings.append(
            "status/CURRENT_STATUS.md has no 'Last updated: YYYY-MM-DD' line"
        )
        return

    last_updated = date_cls.fromisoformat(match.group(1))
    age_days = (date_cls.today() - last_updated).days
    if age_days > STALE_STATUS_DAYS:
        result.warnings.append(
            f"status/CURRENT_STATUS.md last updated {last_updated.isoformat()} "
            f"({age_days} days ago) — may be stale"
        )


def _check_memory_frontmatter(target: Path, result: Result) -> None:
    memory_dir = target / "memory"
    if not memory_dir.is_dir():
        return

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft7Validator(schema)

    for path in sorted(memory_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(target)
        match = FRONTMATTER_RE.match(text)
        if not match:
            result.errors.append(f"{rel}: missing YAML frontmatter")
            continue
        try:
            data = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as exc:
            result.errors.append(f"{rel}: invalid YAML frontmatter ({exc})")
            continue
        # YAML auto-parses unquoted YYYY-MM-DD scalars into date objects;
        # the schema (and the spec) treat `date` as a plain string.
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (_dt.date, _dt.datetime)):
                    data[key] = value.isoformat()
        for err in sorted(validator.iter_errors(data), key=str):
            result.errors.append(f"{rel}: {err.message}")


def _protocol_markdown_files(target: Path):
    """Markdown files that are actually part of the protocol.

    Top-level files directly in `target`, plus everything under the
    protocol's own directories (memory/, status/, evidence/, handover/,
    archive/). Deliberately does NOT recurse into arbitrary sibling content
    `target` happens to contain -- an unrelated project, a node_modules/,
    anything not defined as part of a conforming project by SPEC.md section
    3. `validate` has no business scanning content it isn't responsible for.
    """
    for path in sorted(target.glob("*.md")):
        if path.is_file():
            yield path
    for name in REQUIRED_DIRS:
        base = target / name
        if base.is_dir():
            for path in sorted(base.rglob("*.md")):
                if path.is_file():
                    yield path


def _check_internal_links(target: Path, result: Result) -> None:
    for path in _protocol_markdown_files(target):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(target)
        for link in LINK_RE.findall(text):
            if "://" in link or link.startswith("#") or link.startswith("mailto:"):
                continue
            link_path = link.split("#", 1)[0].strip()
            if not link_path:
                continue
            resolved = (path.parent / link_path).resolve()
            if not resolved.exists():
                result.errors.append(f"{rel}: broken link to '{link}'")


def _check_memory_size(target: Path, result: Result, config: dict) -> None:
    memory_dir = target / "memory"
    if not memory_dir.is_dir():
        return

    threshold = config.get("memory_size_warning_chars", DEFAULT_MEMORY_SIZE_WARNING_CHARS)
    if not isinstance(threshold, (int, float)) or threshold <= 0:
        result.warnings.append(
            f"{CONFIG_FILE}: memory_size_warning_chars must be a positive number, "
            f"ignoring it and using the default ({DEFAULT_MEMORY_SIZE_WARNING_CHARS})"
        )
        threshold = DEFAULT_MEMORY_SIZE_WARNING_CHARS

    total_chars = sum(
        path.stat().st_size for path in memory_dir.rglob("*.md") if path.is_file()
    )
    if total_chars > threshold:
        result.warnings.append(
            f"memory/ is {total_chars:,} characters (over the {int(threshold):,} "
            "warning threshold) — every session that reads memory/INDEX.md and "
            "what it links to pays for this in tokens. Either archive entries "
            "that are still true but rarely needed (SPEC.md section 3.5), or "
            f"raise the threshold by adding {{\"memory_size_warning_chars\": N}} "
            f"to {CONFIG_FILE} in the project root."
        )


def _check_no_secrets(target: Path, result: Result) -> None:
    for path in _protocol_markdown_files(target):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(target)
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                # Never echo the matched text itself -- that would print the
                # very thing this check exists to keep out of view.
                result.errors.append(
                    f"{rel}: looks like it contains a {name} (value redacted) — "
                    "SPEC.md section 6.6: never write credentials into these "
                    "files. Remove it, and rotate the credential if it's real."
                )
