#!/usr/bin/env python3
"""
Render modular HTML email templates using lightweight placeholders.

Supported syntax:
- {{variable}}
- {{#if variable}} ... {{/if}}

Values ending with `_html` are inserted as raw HTML.
All other values are HTML-escaped.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


VAR_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")
IF_RE = re.compile(
    r"\{\{#if\s+([a-zA-Z0-9_]+)\s*\}\}(.*?)\{\{/if\}\}",
    re.DOTALL,
)


def read_data(args: argparse.Namespace) -> dict:
    if args.data_file and args.data_json:
        raise ValueError("Use either --data-file or --data-json, not both.")
    if not args.data_file and not args.data_json:
        raise ValueError("Provide --data-file or --data-json.")

    if args.data_file:
        raw = args.data_file.read_text(encoding="utf-8")
    else:
        raw = args.data_json

    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("Template data must be a JSON object.")
    return data


def render_conditionals(template: str, data: dict) -> str:
    previous = None
    current = template
    while previous != current:
        previous = current

        def replace(match: re.Match) -> str:
            key = match.group(1)
            block = match.group(2)
            value = data.get(key)
            return block if value else ""

        current = IF_RE.sub(replace, current)
    return current


def render_variables(template: str, data: dict) -> str:
    def replace(match: re.Match) -> str:
        key = match.group(1)
        value = data.get(key, "")
        if value is None:
            value = ""
        text = str(value)
        if key.endswith("_html"):
            return text
        return html.escape(text, quote=True)

    return VAR_RE.sub(replace, template)


def active_placeholders(template: str) -> set[str]:
    return set(VAR_RE.findall(template))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render dynamic email HTML template")
    parser.add_argument("--template", type=Path, required=True, help="Template file path")
    parser.add_argument("--data-file", type=Path, help="Path to JSON payload file")
    parser.add_argument("--data-json", help="Inline JSON payload")
    parser.add_argument("--output", type=Path, help="Output file path (stdout if omitted)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if unresolved placeholders remain after rendering",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = read_data(args)

    template = args.template.read_text(encoding="utf-8")
    with_conditionals = render_conditionals(template, data)

    missing_keys = sorted(k for k in active_placeholders(with_conditionals) if k not in data)
    if args.strict and missing_keys:
        print(f"Missing required variables: {missing_keys}", file=sys.stderr)
        return 1

    rendered = render_variables(with_conditionals, data)

    unresolved = VAR_RE.findall(rendered)
    if args.strict and unresolved:
        print(
            f"Unresolved placeholders remain: {sorted(set(unresolved))}",
            file=sys.stderr,
        )
        return 1

    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2)
