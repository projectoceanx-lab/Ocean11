#!/usr/bin/env python3
"""
Memory Promote — Project Ocean
Promotes observations that EARNED their way to shared status.

Promotion criteria (earned, not declared):
  - importance >= 0.8 (reached through references/usage)
  - OR verified=true AND importance >= 0.6
  - OR explicitly requested (--force)

Usage:
  python3 scripts/memory-promote.py                    # Auto-promote qualifying obs
  python3 scripts/memory-promote.py --agent hawk        # Only from hawk
  python3 scripts/memory-promote.py --force --file obs-2026-02-15-001.md --agent scout
  python3 scripts/memory-promote.py --dry-run           # Preview

Zero external dependencies.
"""

import argparse
import re
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
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            fm[key] = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
        elif re.match(r"^-?\d+(\.\d+)?$", val):
            fm[key] = float(val) if "." in val else int(val)
        elif val.lower() in ("true", "false"):
            fm[key] = val.lower() == "true"
        else:
            fm[key] = val.strip("'\"")
    return fm, body


def serialize_frontmatter(fm):
    """Serialize frontmatter dict to YAML-like string."""
    lines = ["---"]
    key_order = [
        "tags", "importance", "created", "max_age", "source",
        "refs", "ref_by", "backlinks", "verified",
        "promoted", "promoted_from", "promoted_at",
    ]
    written = set()
    for key in key_order:
        if key in fm:
            lines.append(_fmt_kv(key, fm[key]))
            written.add(key)
    for key, val in fm.items():
        if key not in written:
            lines.append(_fmt_kv(key, val))
    lines.append("---")
    return "\n".join(lines)


def _fmt_kv(key, val):
    if isinstance(val, list):
        inner = ", ".join(str(v) for v in val)
        return f"{key}: [{inner}]"
    elif isinstance(val, bool):
        return f"{key}: {'true' if val else 'false'}"
    elif isinstance(val, float):
        return f"{key}: {val:.2f}"
    else:
        return f"{key}: {val}"


def qualifies_for_promotion(fm, force=False):
    """Check if observation has earned promotion."""
    if force:
        return True
    if fm.get("promoted", False):
        return False  # Already promoted

    importance = float(fm.get("importance", 0.5))
    verified = fm.get("verified", False)

    # Earned importance >= 0.8
    if importance >= 0.8:
        return True
    # Verified + decent importance
    if verified and importance >= 0.6:
        return True

    return False


def promote_file(filepath, source_agent, fm, body, dry_run=False):
    """Promote observation to shared. Updates source file with promoted flag."""
    SHARED_DIR.mkdir(parents=True, exist_ok=True)

    # Shared copy gets source prefix
    shared_name = f"{source_agent}-{filepath.name}"
    dest = SHARED_DIR / shared_name

    if dest.exists():
        print(f"  SKIP (already in shared): {shared_name}")
        return False

    if dry_run:
        importance = float(fm.get("importance", 0.5))
        refs = int(fm.get("refs", 0))
        print(f"  [DRY RUN] Would promote: {filepath.name} from {source_agent} (importance={importance:.2f}, refs={refs})")
        return True

    # Write promoted copy to shared
    shared_fm = dict(fm)
    shared_fm["promoted_from"] = source_agent
    shared_fm["promoted_at"] = datetime.now().strftime("%Y-%m-%d")
    shared_content = serialize_frontmatter(shared_fm) + "\n" + body + "\n"
    dest.write_text(shared_content, encoding="utf-8")

    # Mark source as promoted
    fm["promoted"] = True
    source_content = serialize_frontmatter(fm) + "\n" + body + "\n"
    filepath.write_text(source_content, encoding="utf-8")

    importance = float(fm.get("importance", 0.5))
    print(f"  Promoted: {filepath.name} → shared/{shared_name} (importance={importance:.2f})")
    return True


def main():
    parser = argparse.ArgumentParser(description="Promote earned observations to shared vault")
    parser.add_argument("--agent", "-a", help="Only promote from specific agent")
    parser.add_argument("--file", "-f", help="Promote specific file by name")
    parser.add_argument("--force", action="store_true", help="Force promote (bypass importance check)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without promoting")
    args = parser.parse_args()

    agents = [args.agent] if args.agent else AGENTS
    promoted = 0
    scanned = 0

    print(f"Memory Promote — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    if args.force:
        print("Force: ON (bypassing importance check)")
    print()

    for agent in agents:
        vault = REPO_ROOT / "agents" / agent / "memory" / "vault"
        if not vault.exists():
            continue

        for f in sorted(vault.glob("*.md")):
            if args.file and f.name != args.file:
                continue
            scanned += 1

            text = f.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)

            if not qualifies_for_promotion(fm, force=args.force):
                continue

            if promote_file(f, agent, fm, body, dry_run=args.dry_run):
                promoted += 1

    print(f"\nScanned: {scanned} | Promoted: {promoted}")


if __name__ == "__main__":
    main()
