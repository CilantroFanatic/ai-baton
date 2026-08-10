from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .commands import init as init_cmd
from .commands import status as status_cmd
from .commands import validate as validate_cmd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-handoff-protocol",
        description="Scaffold, validate, and read ai-handoff-protocol projects.",
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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
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
