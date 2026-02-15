#!/usr/bin/env python3
"""
Memory Vault Search — Project Ocean
Indexes and searches agent observations using TF-IDF scoring.
Ranks by: cosine_similarity × importance × freshness_weight
Zero external dependencies. Python stdlib only.

Usage:
  python3 scripts/memory-search.py "query" --agent watchtower --limit 5
  python3 scripts/memory-search.py "CPL insurance" --all --limit 10
  python3 scripts/memory-search.py "buyer payout" --tags revenue,buyer
  python3 scripts/memory-search.py "compliance" --min-importance 0.6
"""

import argparse
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS = ["captain", "scout", "shield", "hawk", "forge", "watchtower"]
SHARED_DIR = REPO_ROOT / "shared" / "observations"

STOPWORDS = {
    "the", "a", "an", "is", "was", "are", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "and", "but", "or",
    "not", "no", "nor", "so", "yet", "both", "either", "neither", "each",
    "every", "all", "any", "few", "more", "most", "other", "some", "such",
    "than", "too", "very", "just", "also", "this", "that", "these", "those",
    "it", "its", "i", "we", "you", "he", "she", "they", "me", "him", "her",
    "us", "them", "my", "your", "his", "our", "their",
}


def parse_frontmatter(text):
    """Minimal YAML frontmatter parser. No external deps."""
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


def parse_max_age_days(max_age_str):
    """Parse max_age like '14d', '30d', '90d', '180d'. Returns days or None for 'permanent'."""
    if not max_age_str or max_age_str == "permanent":
        return None
    m = re.match(r"(\d+)d", str(max_age_str))
    return int(m.group(1)) if m else None


def freshness_weight(fm):
    """Calculate freshness: 1.0 = brand new, approaches 0.0 near max_age. Importance extends life."""
    created = fm.get("created", "")
    max_age = fm.get("max_age", "30d")
    importance = float(fm.get("importance", 0.5))

    if not created:
        return 1.0

    try:
        created_dt = datetime.strptime(str(created), "%Y-%m-%d")
    except ValueError:
        return 1.0

    days = parse_max_age_days(max_age)
    if days is None:  # permanent
        return 1.0

    # Importance extends effective max_age
    if importance >= 0.9:
        days *= 3
    elif importance >= 0.8:
        days *= 2

    age = (datetime.now() - created_dt).days
    if age >= days:
        return 0.05  # Not zero — still findable if searched directly
    return 1.0 - (0.95 * age / days)  # Linear decay from 1.0 to 0.05


def load_observations(agent=None, include_shared=True, min_importance=0.0):
    """Load all observation files from vault directories."""
    obs = []
    dirs = []
    if agent:
        dirs.append(REPO_ROOT / "agents" / agent / "memory" / "vault")
    else:
        for a in AGENTS:
            dirs.append(REPO_ROOT / "agents" / a / "memory" / "vault")
    if include_shared:
        dirs.append(SHARED_DIR)

    for d in dirs:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            text = f.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)

            importance = float(fm.get("importance", 0.5))
            if importance < min_importance:
                continue
            # Skip archived-level importance
            if importance < 0.1:
                continue

            obs.append({
                "path": str(f),
                "filename": f.name,
                "frontmatter": fm,
                "body": body,
                "importance": importance,
                "source": fm.get("source", "unknown"),
                "tags": fm.get("tags", []),
                "created": fm.get("created", ""),
                "refs": int(fm.get("refs", 0)),
                "verified": fm.get("verified", False),
            })
    return obs


def tokenize(text):
    """Lowercase, split on non-alphanumeric, remove stopwords."""
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


def compute_tfidf(observations):
    """Compute TF-IDF vectors for all observations."""
    df = Counter()
    doc_tokens = []
    n = len(observations)

    for obs in observations:
        # Tags are weighted — appear twice in the token stream
        tag_text = " ".join(obs.get("tags", [])) * 2
        text = tag_text + " " + obs["body"]
        tokens = tokenize(text)
        doc_tokens.append(tokens)
        for t in set(tokens):
            df[t] += 1

    idf = {term: math.log((n + 1) / (count + 1)) + 1 for term, count in df.items()}

    tfidf_vecs = []
    for tokens in doc_tokens:
        tf = Counter(tokens)
        total = len(tokens) or 1
        vec = {t: (count / total) * idf.get(t, 1) for t, count in tf.items()}
        tfidf_vecs.append(vec)

    return tfidf_vecs, idf


def cosine_sim(vec_a, vec_b):
    """Cosine similarity between two sparse vectors (dicts)."""
    all_keys = set(list(vec_a) + list(vec_b))
    dot = sum(vec_a.get(t, 0) * vec_b.get(t, 0) for t in all_keys)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values())) or 1
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values())) or 1
    return dot / (mag_a * mag_b)


def search(query, observations, tfidf_vecs, idf, tag_filter=None, limit=5):
    """Search observations by query. Returns ranked results."""
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    qtf = Counter(query_tokens)
    total = len(query_tokens)
    query_vec = {t: (c / total) * idf.get(t, 1) for t, c in qtf.items()}

    results = []
    for i, obs in enumerate(observations):
        if tag_filter:
            if not set(obs.get("tags", [])).intersection(tag_filter):
                continue

        sim = cosine_sim(query_vec, tfidf_vecs[i])
        importance = obs["importance"]
        fw = freshness_weight(obs["frontmatter"])

        # Final score: similarity × importance × freshness
        score = sim * importance * fw

        if score > 0.001:
            results.append({
                "score": round(score, 4),
                "file": obs["filename"],
                "path": obs["path"],
                "source": obs["source"],
                "tags": obs.get("tags", []),
                "importance": importance,
                "refs": obs["refs"],
                "verified": obs["verified"],
                "created": obs.get("created", ""),
                "snippet": obs["body"][:200].replace("\n", " "),
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def main():
    parser = argparse.ArgumentParser(description="Search Ocean memory vault")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--agent", "-a", help="Search specific agent's vault")
    parser.add_argument("--all", action="store_true", help="Search all agents")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Max results")
    parser.add_argument("--tags", "-t", help="Filter by tags (comma-separated)")
    parser.add_argument("--min-importance", type=float, default=0.0, help="Minimum importance threshold")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-shared", action="store_true", help="Exclude shared observations")
    args = parser.parse_args()

    agent = args.agent if args.agent and not args.all else None
    include_shared = not args.no_shared
    tag_filter = set(args.tags.split(",")) if args.tags else None

    observations = load_observations(
        agent=agent, include_shared=include_shared, min_importance=args.min_importance
    )
    if not observations:
        if args.json:
            print(json.dumps({"results": [], "total": 0}))
        else:
            print("No observations found.")
        return

    tfidf_vecs, idf = compute_tfidf(observations)
    results = search(args.query, observations, tfidf_vecs, idf, tag_filter=tag_filter, limit=args.limit)

    if args.json:
        print(json.dumps({"results": results, "total": len(results)}, indent=2))
    else:
        if not results:
            print("No matching observations.")
            return
        print(f"Found {len(results)} result(s):\n")
        for i, r in enumerate(results, 1):
            verified = " ✓" if r["verified"] else ""
            refs = f" refs:{r['refs']}" if r["refs"] else ""
            print(f"  {i}. [{r['score']:.3f}] {r['file']}{verified}{refs}")
            print(f"     Source: {r['source']} | Tags: {', '.join(r['tags'])} | Importance: {r['importance']}")
            print(f"     {r['snippet']}")
            print()


if __name__ == "__main__":
    main()
