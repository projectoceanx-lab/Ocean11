#!/usr/bin/env python3
"""
Content preflight linter for Ocean dual-track assets.

Checks:
- blocked phrase detection
- caution phrase warnings
- CTA allowlist enforcement
- single-CTA enforcement
- channel-required footer token checks

Usage:
  python3 scripts/content-preflight-lint.py --channel email --asset-file draft.txt --json
  python3 scripts/content-preflight-lint.py --channel social --text "..." --cta "See If You Qualify"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in YAML: {path}")
    return data


def normalize(text: str) -> str:
    return text.casefold()


def find_substring_hits(text: str, phrases: list[str]) -> list[str]:
    folded = normalize(text)
    hits = []
    for phrase in phrases:
        if normalize(phrase) in folded:
            hits.append(phrase)
    return hits


def extract_caution_phrases(lexicon: dict) -> list[str]:
    caution_raw = lexicon.get("caution_phrases", [])
    caution = []
    for item in caution_raw:
        if isinstance(item, dict) and item.get("phrase"):
            caution.append(str(item["phrase"]))
        elif isinstance(item, str):
            caution.append(item)
    return caution


def count_cta_hits(text: str, cta_allowlist: list[str]) -> list[str]:
    folded = normalize(text)
    matched = []
    for cta in cta_allowlist:
        if normalize(cta) in folded:
            matched.append(cta)
    return matched


def lint_content(
    text: str,
    channel: str,
    lexicon: dict,
    channel_rules: dict,
    explicit_cta: str | None = None,
) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    blocked_phrases = [str(p) for p in lexicon.get("blocked_phrases", [])]
    caution_phrases = extract_caution_phrases(lexicon)
    cta_allowlist = [str(c) for c in lexicon.get("cta_allowlist", [])]

    channel_config = (channel_rules.get("channels") or {}).get(channel, {})
    if not channel_config:
        errors.append(f"Unknown channel rules for '{channel}'.")
        return {
            "channel": channel,
            "pass": False,
            "errors": errors,
            "warnings": warnings,
            "info": info,
        }

    blocked_hits = find_substring_hits(text, blocked_phrases)
    if blocked_hits:
        errors.append(f"Blocked phrase(s) found: {', '.join(blocked_hits)}")

    caution_hits = find_substring_hits(text, caution_phrases)
    if caution_hits:
        warnings.append(f"Caution phrase(s) present: {', '.join(caution_hits)}")

    matched_ctas = count_cta_hits(text, cta_allowlist)
    if explicit_cta:
        if explicit_cta not in cta_allowlist:
            errors.append(f"Explicit CTA is not allowlisted: '{explicit_cta}'")
        else:
            info.append(f"Explicit CTA validated: {explicit_cta}")

    if channel_config.get("single_primary_cta", False):
        unique_ctas = sorted(set(matched_ctas))
        if len(unique_ctas) == 0:
            warnings.append("No allowlisted CTA detected in asset body.")
        if len(unique_ctas) > 1:
            errors.append(
                "Multiple CTA intents found for single-CTA channel: "
                + ", ".join(unique_ctas)
            )

    required_footer_tokens = channel_config.get("require_footer_tokens") or []
    for token in required_footer_tokens:
        if normalize(token) not in normalize(text):
            errors.append(f"Missing required token for {channel}: '{token}'")

    if channel_config.get("require_unsubscribe", False):
        if "unsubscribe" not in normalize(text):
            errors.append("Missing unsubscribe instruction/token for email channel.")

    passed = len(errors) == 0
    return {
        "channel": channel,
        "pass": passed,
        "errors": errors,
        "warnings": warnings,
        "info": info,
        "detected_ctas": sorted(set(matched_ctas)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ocean content preflight lint")
    parser.add_argument("--channel", required=True, choices=["email", "social"])
    parser.add_argument("--asset-file", type=Path, help="Path to content file")
    parser.add_argument("--text", help="Inline content text")
    parser.add_argument("--cta", help="Explicit CTA to validate")
    parser.add_argument(
        "--lexicon",
        type=Path,
        default=Path("config/copy_lexicon.yaml"),
        help="Path to copy lexicon YAML",
    )
    parser.add_argument(
        "--channel-rules",
        type=Path,
        default=Path("skills/ocean-content-loop/rules/channel_requirements.yaml"),
        help="Path to channel requirements YAML",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.asset_file and not args.text:
        print("Error: provide either --asset-file or --text", file=sys.stderr)
        return 2

    if args.asset_file and args.text:
        print("Error: provide only one of --asset-file or --text", file=sys.stderr)
        return 2

    if args.asset_file:
        text = args.asset_file.read_text(encoding="utf-8")
    else:
        text = args.text or ""

    lexicon = load_yaml(args.lexicon)
    channel_rules = load_yaml(args.channel_rules)

    result = lint_content(
        text=text,
        channel=args.channel,
        lexicon=lexicon,
        channel_rules=channel_rules,
        explicit_cta=args.cta,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status = "PASS" if result["pass"] else "FAIL"
        print(f"Preflight {status} [{result['channel']}]")
        if result["errors"]:
            print("Errors:")
            for err in result["errors"]:
                print(f"- {err}")
        if result["warnings"]:
            print("Warnings:")
            for warn in result["warnings"]:
                print(f"- {warn}")
        if result["info"]:
            print("Info:")
            for note in result["info"]:
                print(f"- {note}")

    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
