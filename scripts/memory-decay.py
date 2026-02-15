#!/usr/bin/env python3
"""
Memory Decay — Project Ocean
Archives observations based on age + importance. Importance extends life.
Run daily via cron: 0 6 * * * python3 /path/to/repo/scripts/memory-decay.py

Rules:
  - importance < 0.2 → archive regardless of age
  - past max_age + importance < 0.4 → archive
  - past max_age + importance 0.4-0.7 → flag for review
  - past max_age + importance >= 0.7 → auto-extend max_age
  - importance >= 0.8 → max_age doubles
  - importance >= 0.9 → max_age triples

Also applies neglect penalty: observations not referenced in 14+ days lose importance.

Zero external dependencies. Python stdlib only.
"""

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS = ["captain", "scout", "shield", "hawk", "signal", "watchtower"]
DRY_RUN = "--dry-run" in sys.argv
VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv
NOW = datetime.now()


def parse_frontmatter(text):
    """Minimal YAML frontmatter parser."""
    fm = {}
    if not text.startswith("---"):
        return fm, text, None, None
    end = text.find("---", 3)
    if end == -1:
        return fm, text, None, None
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
    return fm, body, 3, end


def serialize_frontmatter(fm):
    """Serialize frontmatter dict back to YAML-like string."""
    lines = ["---"]
    # Maintain a sensible key order
    key_order = [
        "tags", "importance", "created", "max_age", "source",
        "refs", "ref_by", "backlinks", "verified", "promoted",
        "promoted_from", "promoted_at", "last_referenced", "neglect_note",
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


def write_observation(filepath, fm, body):
    """Write observation back with updated frontmatter."""
    content = serialize_frontmatter(fm) + "\n" + body + "\n"
    filepath.write_text(content, encoding="utf-8")


def parse_max_age_days(max_age_str):
    """Parse '14d', '30d' etc. Returns None for 'permanent'."""
    if not max_age_str or str(max_age_str) == "permanent":
        return None
    m = re.match(r"(\d+)d", str(max_age_str))
    return int(m.group(1)) if m else None


def get_age_days(fm):
    """Get observation age in days."""
    created = fm.get("created", "")
    if not created:
        return 0
    try:
        return (NOW - datetime.strptime(str(created), "%Y-%m-%d")).days
    except ValueError:
        return 0


def get_effective_max_days(fm):
    """Max age adjusted by importance."""
    days = parse_max_age_days(fm.get("max_age", "30d"))
    if days is None:
        return None  # permanent
    importance = float(fm.get("importance", 0.5))
    if importance >= 0.9:
        days *= 3
    elif importance >= 0.8:
        days *= 2
    return days


def apply_neglect_penalty(fm, filepath):
    """
    If observation hasn't been referenced in 14+ days since creation,
    reduce importance by 0.1 per 14-day period of neglect.
    Only applies once per decay run (tracks via last_referenced or created date).
    """
    importance = float(fm.get("importance", 0.5))
    refs = int(fm.get("refs", 0))
    age = get_age_days(fm)

    # If it has references, no neglect penalty
    if refs > 0:
        return importance

    # No penalty in first 14 days
    if age <= 14:
        return importance

    # Calculate neglect periods (14-day blocks past the first 14 days)
    neglect_periods = (age - 14) // 14
    if neglect_periods <= 0:
        return importance

    # Cap penalty: max 0.3 reduction from neglect
    penalty = min(neglect_periods * 0.1, 0.3)
    new_importance = max(importance - penalty, 0.0)

    if new_importance != importance and VERBOSE:
        print(f"    Neglect penalty: {filepath.name} importance {importance:.2f} → {new_importance:.2f} (unreferenced {age}d)")

    return round(new_importance, 2)


def process_vault(agent_name, vault_dir, archive_dir):
    """Process all observations in a vault. Returns stats dict."""
    stats = {"archived": 0, "extended": 0, "flagged": 0, "penalized": 0}
    if not vault_dir.exists():
        return stats
    archive_dir.mkdir(parents=True, exist_ok=True)

    for f in sorted(vault_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm, body, _, _ = parse_frontmatter(text)
        importance = float(fm.get("importance", 0.5))
        age = get_age_days(fm)
        max_days = get_effective_max_days(fm)
        modified = False

        # 1. Apply neglect penalty
        new_importance = apply_neglect_penalty(fm, f)
        if new_importance != importance:
            fm["importance"] = new_importance
            importance = new_importance
            stats["penalized"] += 1
            modified = True

        # 2. Archive if importance critically low (regardless of age)
        if importance < 0.2:
            if DRY_RUN:
                print(f"  [DRY RUN] Archive (low importance {importance:.2f}): {f.name}")
            else:
                if modified:
                    write_observation(f, fm, body)
                shutil.move(str(f), str(archive_dir / f.name))
                print(f"  Archived (importance {importance:.2f}): {f.name}")
            stats["archived"] += 1
            continue

        # 3. Check max_age expiry
        if max_days is not None and age > max_days:
            if importance < 0.4:
                # Archive
                if DRY_RUN:
                    print(f"  [DRY RUN] Archive (expired, importance {importance:.2f}): {f.name}")
                else:
                    if modified:
                        write_observation(f, fm, body)
                    shutil.move(str(f), str(archive_dir / f.name))
                    print(f"  Archived (expired {age}d > {max_days}d, importance {importance:.2f}): {f.name}")
                stats["archived"] += 1
            elif importance < 0.7:
                # Flag for review
                if VERBOSE or DRY_RUN:
                    print(f"  [REVIEW] Expired but mid-importance ({importance:.2f}): {f.name}")
                stats["flagged"] += 1
                if modified and not DRY_RUN:
                    write_observation(f, fm, body)
            else:
                # Auto-extend: bump max_age by 50%
                raw_days = parse_max_age_days(fm.get("max_age", "30d"))
                if raw_days:
                    new_max = int(raw_days * 1.5)
                    fm["max_age"] = f"{new_max}d"
                    modified = True
                    if VERBOSE or DRY_RUN:
                        print(f"  [EXTEND] {f.name}: max_age {raw_days}d → {new_max}d (importance {importance:.2f})")
                    stats["extended"] += 1
                    if not DRY_RUN:
                        write_observation(f, fm, body)
        else:
            # Not expired — just save if modified
            if modified and not DRY_RUN:
                write_observation(f, fm, body)

    return stats


def main():
    print(f"Memory Decay — {NOW.strftime('%Y-%m-%d %H:%M')}")
    print(f"Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}\n")

    total = {"archived": 0, "extended": 0, "flagged": 0, "penalized": 0}

    for agent in AGENTS:
        vault = REPO_ROOT / "agents" / agent / "memory" / "vault"
        archive = REPO_ROOT / "agents" / agent / "memory" / "archive"
        stats = process_vault(agent, vault, archive)
        for k in total:
            total[k] += stats[k]
        if any(stats.values()):
            print(f"  {agent}: archived={stats['archived']} extended={stats['extended']} flagged={stats['flagged']} penalized={stats['penalized']}")

    # Shared
    shared_vault = REPO_ROOT / "shared" / "observations"
    shared_archive = REPO_ROOT / "shared" / "observations" / "archive"
    if shared_vault.exists():
        stats = process_vault("shared", shared_vault, shared_archive)
        for k in total:
            total[k] += stats[k]
        if any(stats.values()):
            print(f"  shared: archived={stats['archived']} extended={stats['extended']} flagged={stats['flagged']}")

    print(f"\nSummary: archived={total['archived']} extended={total['extended']} flagged={total['flagged']} penalized={total['penalized']}")


if __name__ == "__main__":
    main()
