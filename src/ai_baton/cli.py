from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .commands import init as init_cmd
from .commands import skill as skill_cmd
from .commands import status as status_cmd
from .commands import validate as validate_cmd
from .commands import workspace as workspace_cmd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-baton",
        description="Scaffold, validate, and read ai-baton projects.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init", help="Scaffold the protocol directory structure."
    )
    init_parser.add_argument(
        "path", nargs="?", default=".", help="Target directory (default: current directory)."
    )

    validate_parser = subparsers.add_parser(
        "validate", help="Check protocol conformance."
    )
    validate_parser.add_argument(
        "path", nargs="?", default=".", help="Project directory to validate (default: current directory)."
    )

    status_parser = subparsers.add_parser(
        "status", help="Print the mandatory read-order context (PROTOCOL.md + memory index + current status)."
    )
    status_parser.add_argument(
        "path", nargs="?", default=".", help="Project directory (default: current directory)."
    )

    skill_parser = subparsers.add_parser(
        "skill", help="Install the Agent Skills SKILL.md so an AI tool follows the protocol automatically."
    )
    skill_subparsers = skill_parser.add_subparsers(dest="skill_command", required=True)
    skill_install_parser = skill_subparsers.add_parser(
        "install",
        help="Write SKILL.md into skills/ directories (default: the global Claude Code and Agent Skills locations).",
    )
    skill_install_parser.add_argument(
        "targets",
        nargs="*",
        help="Base directories to install into (each gets <target>/ai-baton/SKILL.md). "
        "Default: ~/.claude/skills and ~/.agents/skills.",
    )

    list_parser = subparsers.add_parser(
        "list", help="List ai-baton projects found under a workspace directory."
    )
    list_parser.add_argument(
        "workspace",
        nargs="?",
        default=None,
        help="Workspace directory to scan (default: ~/ai-baton-workspace).",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "skill" and args.skill_command == "install":
        targets = [Path(t).resolve() for t in args.targets] or None
        for message in skill_cmd.install(targets):
            print(message)
        return 0

    if args.command == "list":
        workspace = Path(args.workspace).resolve() if args.workspace else None
        for line in workspace_cmd.list_projects(workspace):
            print(line)
        return 0

    target = Path(args.path).resolve()

    if args.command == "init":
        for message in init_cmd.run(target):
            print(message)
        return 0

    if args.command == "validate":
        result = validate_cmd.run(target)
        for warning in result.warnings:
            print(f"WARN  {warning}")
        for error in result.errors:
            print(f"ERROR {error}")
        if result.ok:
            print("validate: OK")
            return 0
        print(f"validate: {len(result.errors)} error(s)")
        return 1

    if args.command == "status":
        try:
            print(status_cmd.run(target))
        except FileNotFoundError as exc:
            print(f"ERROR {exc}", file=sys.stderr)
            return 1
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2  # pragma: no cover — argparse exits before this via parser.error


if __name__ == "__main__":
    sys.exit(main())
