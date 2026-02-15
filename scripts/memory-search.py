#!/usr/bin/env python3
"""
Memory Vault Search — Project Ocean
Indexes and searches agent observations using keyword + TF-IDF scoring.
Zero external dependencies. Python stdlib only.

Usage:
  python3 scripts/memory-search.py "query" --agent watchtower --limit 5
  python3 scripts/memory-search.py "CPL insurance" --all --limit 10
  python3 scripts/memory-search.py "buyer payout" --tags revenue,buyer
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS = ["captain", "scout", "shield", "hawk", "signal", "watchtower"]
SHARED_DIR = REPO_ROOT / "shared" / "observations"
INDEX_CACHE = REPO_ROOT / "scripts" / ".memory-index.json"


def parse_frontmatter(text):
    """Parse YAML-like frontmatter from markdown. Minimal parser, no yaml import."""
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
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        # Parse lists: [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            items = [x.strip().strip("'\"") for x in val[1:-1].split(",")]
            fm[key] = [x for x in items if x]
        # Parse numbers
        elif re.match(r'^-?\d+(\.\d+)?$', val):
            fm[key] = float(val) if "." in val else int(val)
        # Parse booleans
        elif val.lower() in ("true", "false"):
            fm[key] = val.lower() == "true"
        else:
            fm[key] = val.strip("'\"")
    return fm, body


def load_observations(agent=None, include_shared=True, min_confidence=0.0):
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
            confidence = fm.get("confidence", 1.0)
            if isinstance(confidence, str):
                try:
                    confidence = float(confidence)
                except ValueError:
                    confidence = 0.5
            if confidence < min_confidence:
                continue
            # Check decay
            if is_decayed(fm):
                continue
            obs.append({
                "path": str(f),
                "filename": f.name,
                "frontmatter": fm,
                "body": body,
                "confidence": confidence,
                "source": fm.get("source", f.parent.parent.parent.name),
                "tags": fm.get("tags", []),
                "created": fm.get("created", ""),
            })
    return obs


def is_decayed(fm):
    """Check if an observation has decayed past its useful life."""
    decay = fm.get("decay", "")
    created = fm.get("created", "")
    if not decay or not created:
        return False
    try:
        created_dt = datetime.strptime(str(created), "%Y-%m-%d")
    except ValueError:
        return False
    now = datetime.now()
    # Parse decay spec: "linear-30d" means fully decayed after 30 days
    m = re.match(r'(linear|exponential)-(\d+)d', decay)
    if not m:
        return False
    days = int(m.group(2))
    age = (now - created_dt).days
    return age > days


def decay_weight(fm):
    """Calculate decay weight (1.0 = fresh, 0.0 = fully decayed)."""
    decay = fm.get("decay", "")
    created = fm.get("created", "")
    if not decay or not created:
        return 1.0
    try:
        created_dt = datetime.strptime(str(created), "%Y-%m-%d")
    except ValueError:
        return 1.0
    now = datetime.now()
    m = re.match(r'(linear|exponential)-(\d+)d', decay)
    if not m:
        return 1.0
    mode, days = m.group(1), int(m.group(2))
    age = (now - created_dt).days
    if age >= days:
        return 0.0
    if mode == "linear":
        return 1.0 - (age / days)
    else:  # exponential
        return math.exp(-3 * age / days)  # e^(-3) ≈ 0.05 at full decay


def tokenize(text):
    """Simple tokenizer: lowercase, split on non-alphanumeric, remove stopwords."""
    stops = {"the", "a", "an", "is", "was", "are", "were", "be", "been", "being",
             "have", "has", "had", "do", "does", "did", "will", "would", "could",
             "should", "may", "might", "shall", "can", "to", "of", "in", "for",
             "on", "with", "at", "by", "from", "as", "into", "through", "during",
             "before", "after", "above", "below", "between", "and", "but", "or",
             "not", "no", "nor", "so", "yet", "both", "either", "neither", "each",
             "every", "all", "any", "few", "more", "most", "other", "some", "such",
             "than", "too", "very", "just", "also", "this", "that", "these", "those",
             "it", "its", "i", "we", "you", "he", "she", "they", "me", "him", "her",
             "us", "them", "my", "your", "his", "our", "their"}
    tokens = re.findall(r'[a-z0-9]+', text.lower())
    return [t for t in tokens if t not in stops and len(t) > 1]


def compute_tfidf(observations):
    """Compute TF-IDF vectors for all observations."""
    # Document frequency
    df = Counter()
    doc_tokens = []
    n = len(observations)
    for obs in observations:
        text = " ".join(obs.get("tags", [])) + " " + obs["body"]
        tokens = tokenize(text)
        doc_tokens.append(tokens)
        unique = set(tokens)
        for t in unique:
            df[t] += 1

    # IDF
    idf = {}
    for term, count in df.items():
        idf[term] = math.log((n + 1) / (count + 1)) + 1

    # TF-IDF per doc
    tfidf_vecs = []
    for tokens in doc_tokens:
        tf = Counter(tokens)
        total = len(tokens) or 1
        vec = {}
        for t, count in tf.items():
            vec[t] = (count / total) * idf.get(t, 1)
        tfidf_vecs.append(vec)

    return tfidf_vecs, idf


def search(query, observations, tfidf_vecs, idf, tag_filter=None, limit=5):
    """Search observations by query. Returns ranked results."""
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    # Query TF-IDF
    qtf = Counter(query_tokens)
    total = len(query_tokens)
    query_vec = {t: (c / total) * idf.get(t, 1) for t, c in qtf.items()}

    results = []
    for i, obs in enumerate(observations):
        # Tag filter
        if tag_filter:
            obs_tags = set(obs.get("tags", []))
            if not obs_tags.intersection(tag_filter):
                continue

        # Cosine similarity
        doc_vec = tfidf_vecs[i]
        dot = sum(query_vec.get(t, 0) * doc_vec.get(t, 0) for t in set(list(query_vec) + list(doc_vec)))
        mag_q = math.sqrt(sum(v ** 2 for v in query_vec.values())) or 1
        mag_d = math.sqrt(sum(v ** 2 for v in doc_vec.values())) or 1
        sim = dot / (mag_q * mag_d)

        # Weight by confidence and decay
        confidence = obs.get("confidence", 1.0)
        dw = decay_weight(obs.get("frontmatter", {}))
        score = sim * confidence * dw

        if score > 0.001:
            results.append({
                "score": round(score, 4),
                "file": obs["filename"],
                "path": obs["path"],
                "source": obs["source"],
                "tags": obs.get("tags", []),
                "confidence": confidence,
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
    parser.add_argument("--min-confidence", type=float, default=0.0, help="Minimum confidence threshold")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-shared", action="store_true", help="Exclude shared observations")
    args = parser.parse_args()

    agent = args.agent if args.agent and not args.all else None
    include_shared = not args.no_shared
    tag_filter = set(args.tags.split(",")) if args.tags else None

    observations = load_observations(agent=agent, include_shared=include_shared,
                                     min_confidence=args.min_confidence)
    if not observations:
        if args.json:
            print(json.dumps({"results": [], "total": 0}))
        else:
            print("No observations found.")
        return

    tfidf_vecs, idf = compute_tfidf(observations)
    results = search(args.query, observations, tfidf_vecs, idf,
                     tag_filter=tag_filter, limit=args.limit)

    if args.json:
        print(json.dumps({"results": results, "total": len(results)}, indent=2))
    else:
        if not results:
            print("No matching observations.")
            return
        print(f"Found {len(results)} result(s):\n")
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['score']:.3f}] {r['file']}")
            print(f"     Source: {r['source']} | Tags: {', '.join(r['tags'])} | Confidence: {r['confidence']}")
            print(f"     {r['snippet']}")
            print()


if __name__ == "__main__":
    main()
