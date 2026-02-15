#!/usr/bin/env python3
"""
Memory Decay — Project Ocean
Archives observations that have fully decayed past their useful life.
Run daily via cron: 0 6 * * * python3 /path/to/repo/scripts/memory-decay.py

Zero external dependencies. Python stdlib only.
"""

import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS = ["captain", "scout", "shield", "hawk", "signal", "watchtower"]
DRY_RUN = "--dry-run" in sys.argv


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
        else:
            fm[key] = val.strip("'\"")
    return fm, body


def is_fully_decayed(fm):
    """Check if observation is past its decay window."""
    decay = fm.get("decay", "")
    created = fm.get("created", "")
    if not decay or not created:
        return False
    try:
        created_dt = datetime.strptime(str(created), "%Y-%m-%d")
    except ValueError:
        return False
    m = re.match(r'(linear|exponential)-(\d+)d', decay)
    if not m:
        return False
    days = int(m.group(2))
    age = (datetime.now() - created_dt).days
    return age > days


def process_vault(vault_dir, archive_dir):
    """Move fully decayed observations to archive."""
    if not vault_dir.exists():
        return 0
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived = 0
    for f in sorted(vault_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        if is_fully_decayed(fm):
            dest = archive_dir / f.name
            if DRY_RUN:
                print(f"  [DRY RUN] Would archive: {f.name} (created: {fm.get('created')}, decay: {fm.get('decay')})")
            else:
                shutil.move(str(f), str(dest))
                print(f"  Archived: {f.name} → archive/")
            archived += 1
    return archived


def main():
    print(f"Memory Decay — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    if DRY_RUN:
        print("Mode: DRY RUN (no files moved)\n")
    else:
        print("Mode: LIVE\n")

    total = 0
    for agent in AGENTS:
        vault = REPO_ROOT / "agents" / agent / "memory" / "vault"
        archive = REPO_ROOT / "agents" / agent / "memory" / "archive"
        count = process_vault(vault, archive)
        if count:
            print(f"  {agent}: {count} observation(s) archived")
        total += count

    # Shared observations
    shared_vault = REPO_ROOT / "shared" / "observations"
    shared_archive = REPO_ROOT / "shared" / "observations" / "archive"
    count = process_vault(shared_vault, shared_archive)
    if count:
        print(f"  shared: {count} observation(s) archived")
    total += count

    print(f"\nTotal archived: {total}")


if __name__ == "__main__":
    main()
