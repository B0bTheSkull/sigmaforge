"""Command-line interface for SigmaForge."""

import argparse
import sys
from pathlib import Path

from sigmaforge import __version__
from sigmaforge.converter import SUPPORTED_TARGETS, convert_rule
from sigmaforge.validator import validate_rule


def cmd_validate(args: argparse.Namespace) -> int:
    rule_path = Path(args.rule)
    if not rule_path.exists():
        print(f"error: rule file not found: {rule_path}", file=sys.stderr)
        return 2

    result = validate_rule(rule_path)
    if result.valid:
        print(f"OK {rule_path.name} — valid")
        for rule in result.rules:
            print(f"  ID:         {rule['id']}")
            print(f"  Title:      {rule['title']}")
            print(f"  Status:     {rule['status']}")
            print(f"  Logsource:  {rule['logsource']}")
            print(f"  Detection:  {rule['detection_summary']}")
        return 0

    print(f"FAIL {rule_path.name} — invalid")
    for err in result.errors:
        print(f"  {err}")
    return 1


def cmd_convert(args: argparse.Namespace) -> int:
    rule_path = Path(args.rule)
    if not rule_path.exists():
        print(f"error: rule file not found: {rule_path}", file=sys.stderr)
        return 2

    if args.target not in SUPPORTED_TARGETS:
        print(f"error: unsupported target '{args.target}'", file=sys.stderr)
        print(f"available: {', '.join(SUPPORTED_TARGETS)}", file=sys.stderr)
        return 2

    try:
        queries = convert_rule(rule_path, args.target)
    except Exception as e:
        print(f"error: conversion failed: {e}", file=sys.stderr)
        return 1

    if not args.no_header:
        print(f"=== {rule_path.name} -> {args.target} ===")
    for q in queries:
        print(q)
    return 0


def cmd_list_targets(args: argparse.Namespace) -> int:
    for t in SUPPORTED_TARGETS:
        print(t)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sigmaforge",
        description="Sigma rule writer, validator, and multi-backend converter.",
    )
    p.add_argument("--version", action="version", version=f"sigmaforge {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate", help="Validate a Sigma rule file")
    v.add_argument("rule", help="Path to rule YAML")
    v.set_defaults(func=cmd_validate)

    c = sub.add_parser("convert", help="Convert a Sigma rule to a target query language")
    c.add_argument("rule", help="Path to rule YAML")
    c.add_argument(
        "--target",
        required=True,
        help=f"Backend target ({', '.join(SUPPORTED_TARGETS)})",
    )
    c.add_argument("--no-header", action="store_true", help="Suppress the header line")
    c.set_defaults(func=cmd_convert)

    lt = sub.add_parser("list-targets", help="List available conversion targets")
    lt.set_defaults(func=cmd_list_targets)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
