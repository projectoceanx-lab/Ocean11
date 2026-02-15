#!/usr/bin/env python3
"""
Memory Reference Tracker — Project Ocean
Scans all observations, resolves backlinks, and updates importance scores.

This is the PageRank engine. Run after decay, before promote.

What it does:
  1. Scans all vault observations for backlinks
  2. Updates ref counts and ref_by lists on referenced observations
  3. Adjusts importance based on reference events:
     - Referenced by same agent: +0.1
     - Referenced by different agent: +0.15
  4. Caps importance at 1.0

Usage:
  python3 scripts/memory-ref.py              # Update all
  python3 scripts/memory-ref.py --dry-run    # Preview changes
  python3 scripts/memory-ref.py --verbose    # Show all reference resolutions

Zero external dependencies.
"""

import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS = ["captain", "scout", "shield", "hawk", "signal", "watchtower"]
DRY_RUN = "--dry-run" in sys.argv
VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv


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


def load_all_observations():
    """Load all observations with their paths and agent names."""
    obs = {}  # agent/filename -> {path, fm, body, agent}
    for agent in AGENTS:
        vault = REPO_ROOT / "agents" / agent / "memory" / "vault"
        if not vault.exists():
            continue
        for f in sorted(vault.glob("*.md")):
            text = f.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)
            key = f"{agent}/{f.name}"
            obs[key] = {
                "path": f,
                "filename": f.name,
                "fm": fm,
                "body": body,
                "agent": agent,
            }
    return obs


def resolve_references(obs):
    """
    Build reference graph from backlinks.
    Returns: dict of filename -> {new_refs: int, new_ref_by: [str], importance_delta: float, cross_agent: bool}
    """
    # Build: who references whom
    ref_graph = defaultdict(list)  # target_filename -> [(source_filename, source_agent)]

    for obs_key, data in obs.items():
        backlinks = data["fm"].get("backlinks", [])
        source_agent = data["agent"]
        for target in backlinks:
            # Normalize: ensure .md extension
            target_name = target if target.endswith(".md") else target + ".md"
            # Try to find target in any agent's vault
            for agent in AGENTS:
                candidate_key = f"{agent}/{target_name}"
                if candidate_key in obs:
                    ref_graph[candidate_key].append((obs_key, source_agent))
                    break
            else:
                if VERBOSE:
                    print(f"  [WARN] Backlink target not found: {target_name} (from {obs_key})")

    # Calculate updates
    updates = {}
    for target_key, references in ref_graph.items():
        if target_key not in obs:
            continue

        target_data = obs[target_key]
        target_agent = target_data["agent"]
        current_refs = int(target_data["fm"].get("refs", 0))
        current_ref_by = target_data["fm"].get("ref_by", [])
        current_importance = float(target_data["fm"].get("importance", 0.5))

        new_ref_by = list(set(current_ref_by))  # dedupe existing
        importance_delta = 0.0

        for source_key, source_agent in references:
            source_id = source_key.replace(".md", "")
            if source_id not in new_ref_by:
                new_ref_by.append(source_id)
                # New reference — calculate importance boost
                if source_agent != target_agent:
                    importance_delta += 0.15  # Cross-agent reference
                else:
                    importance_delta += 0.1   # Same-agent reference

        new_refs = len(new_ref_by)
        new_importance = min(current_importance + importance_delta, 1.0)

        # Only update if something changed
        if new_refs != current_refs or importance_delta > 0:
            updates[target_key] = {
                "new_refs": new_refs,
                "new_ref_by": new_ref_by,
                "old_importance": current_importance,
                "new_importance": round(new_importance, 2),
                "delta": round(importance_delta, 2),
                "cross_agent_refs": sum(1 for _, sa in references if sa != target_agent),
            }

    return updates


def apply_updates(obs, updates):
    """Write updated frontmatter back to files."""
    applied = 0
    for filename, update in updates.items():
        data = obs[filename]
        fm = data["fm"]
        body = data["body"]
        filepath = data["path"]

        old_imp = update["old_importance"]
        new_imp = update["new_importance"]

        if DRY_RUN:
            print(f"  [DRY RUN] {filename}: refs={update['new_refs']}, importance {old_imp:.2f} → {new_imp:.2f} (Δ{update['delta']:+.2f})")
        else:
            fm["refs"] = update["new_refs"]
            fm["ref_by"] = update["new_ref_by"]
            fm["importance"] = update["new_importance"]
            content = serialize_frontmatter(fm) + "\n" + body + "\n"
            filepath.write_text(content, encoding="utf-8")
            print(f"  Updated: {filename} refs={update['new_refs']} importance {old_imp:.2f} → {new_imp:.2f}")
        applied += 1

    return applied


def main():
    print(f"Memory Reference Tracker — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}\n")

    obs = load_all_observations()
    print(f"Loaded {len(obs)} observations across {len(AGENTS)} agents\n")

    if not obs:
        print("No observations found.")
        return

    updates = resolve_references(obs)

    if not updates:
        print("No reference updates needed.")
        return

    applied = apply_updates(obs, updates)
    print(f"\nUpdated: {applied} observation(s)")


if __name__ == "__main__":
    main()
