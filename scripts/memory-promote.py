#!/usr/bin/env python3
"""
Memory Promote — Project Ocean
Promotes high-confidence agent observations to the shared directory.
Observations with confidence >= threshold and verified=true get promoted.

Usage:
  python3 scripts/memory-promote.py                          # Auto-promote (confidence >= 0.8)
  python3 scripts/memory-promote.py --threshold 0.7          # Lower threshold
  python3 scripts/memory-promote.py --agent hawk              # Only from hawk
  python3 scripts/memory-promote.py --file obs-2026-02-15-001.md --agent scout  # Specific file

Zero external dependencies.
"""

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS = ["captain", "scout", "shield", "hawk", "signal", "watchtower"]
SHARED_DIR = REPO_ROOT / "shared" / "observations"


def parse_frontmatter(text):
    """Minimal YAML frontmatter parser."""
    fm = {}
    if not text.startswith("---"):
        return fm, text
    end = text.find("---", 3)
    if end == -1:
        return fm, text
    raw = text[3:end].strip()
    body = text[end + 3:].strip()
    for line in raw.split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            fm[key] = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
        elif re.match(r'^-?\d+(\.\d+)?$', val):
            fm[key] = float(val) if "." in val else int(val)
        elif val.lower() in ("true", "false"):
            fm[key] = val.lower() == "true"
        else:
            fm[key] = val.strip("'\"")
    return fm, body


def add_promoted_metadata(text, source_agent):
    """Add promoted_from and promoted_at to frontmatter."""
    if not text.startswith("---"):
        return text
    end = text.find("---", 3)
    if end == -1:
        return text
    fm_section = text[3:end].rstrip()
    rest = text[end:]
    promoted_lines = f"\npromoted_from: {source_agent}\npromoted_at: {datetime.now().strftime('%Y-%m-%d')}"
    return "---" + fm_section + promoted_lines + "\n" + rest


def promote_file(filepath, source_agent, dry_run=False):
    """Promote a single observation file to shared."""
    SHARED_DIR.mkdir(parents=True, exist_ok=True)
    dest = SHARED_DIR / filepath.name
    if dest.exists():
        print(f"  SKIP (already exists in shared): {filepath.name}")
        return False
    if dry_run:
        print(f"  [DRY RUN] Would promote: {filepath.name} from {source_agent}")
        return True

    text = filepath.read_text(encoding="utf-8")
    promoted = add_promoted_metadata(text, source_agent)
    dest.write_text(promoted, encoding="utf-8")
    print(f"  Promoted: {filepath.name} ({source_agent} → shared/observations/)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Promote observations to shared vault")
    parser.add_argument("--agent", "-a", help="Only promote from specific agent")
    parser.add_argument("--threshold", "-t", type=float, default=0.8, help="Min confidence (default 0.8)")
    parser.add_argument("--file", "-f", help="Promote specific file by name")
    parser.add_argument("--dry-run", action="store_true", help="Preview without promoting")
    parser.add_argument("--require-verified", action="store_true", help="Only promote verified observations")
    args = parser.parse_args()

    agents = [args.agent] if args.agent else AGENTS
    promoted = 0

    for agent in agents:
        vault = REPO_ROOT / "agents" / agent / "memory" / "vault"
        if not vault.exists():
            continue

        for f in sorted(vault.glob("*.md")):
            if args.file and f.name != args.file:
                continue

            text = f.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(text)

            confidence = fm.get("confidence", 0)
            if isinstance(confidence, str):
                try:
                    confidence = float(confidence)
                except ValueError:
                    confidence = 0

            if confidence < args.threshold:
                continue

            if args.require_verified and not fm.get("verified", False):
                continue

            if promote_file(f, agent, dry_run=args.dry_run):
                promoted += 1

    print(f"\nTotal promoted: {promoted}")


if __name__ == "__main__":
    main()
