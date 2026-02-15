# Memory Architecture — Project Ocean

ClawVault-inspired memory system. Zero dependencies. Filesystem only.

## Overview

Every agent has a **memory vault** — a directory of markdown observation files with YAML frontmatter. Observations decay over time, can be searched with TF-IDF, and high-confidence observations get promoted to a shared directory all agents can read.

```
repo/
├── agents/{name}/memory/
│   ├── vault/          # Active observations (markdown + YAML frontmatter)
│   └── archive/        # Decayed observations (auto-moved by decay script)
├── shared/observations/ # Promoted high-confidence observations (read by all)
└── scripts/
    ├── memory-search.py   # TF-IDF search across vaults
    ├── memory-decay.py    # Archive expired observations (daily cron)
    └── memory-promote.py  # Promote high-confidence obs to shared/
```

## Observation Format

```markdown
---
tags: [campaign, ctr, insurance]
confidence: 0.82
created: 2026-02-15
decay: linear-30d
source: watchtower
backlinks: [obs-2026-02-14-003]
verified: false
---
Insurance vertical CTR dropped 12% week-over-week...
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `tags` | Yes | Searchable topic tags |
| `confidence` | Yes | 0.0-1.0 — how certain is this observation |
| `created` | Yes | YYYY-MM-DD |
| `decay` | Yes | `linear-Nd` or `exponential-Nd` — lifespan in days |
| `source` | Yes | Which agent wrote it |
| `backlinks` | No | References to related observations |
| `verified` | No | Set to `true` when confirmed by another agent or human |

### Naming Convention

`obs-YYYY-MM-DD-NNN.md` where NNN is a sequence number (001, 002, ...).

### Decay Guidelines

| Type | Decay | Use For |
|------|-------|---------|
| Tactical | `linear-14d` | Daily metrics, system status |
| Operational | `linear-30d` | Campaign performance, source changes |
| Strategic | `linear-90d` | Buyer relationships, pricing |
| Compliance | `linear-180d` | Regulatory changes, legal |
| Permanent | (no decay) | Core business rules, SOPs |

## Scripts

### Search: `memory-search.py`

```bash
# Search your own vault + shared
python3 scripts/memory-search.py "CPL trend" --agent hawk --limit 5

# Search everything
python3 scripts/memory-search.py "buyer acceptance" --all --limit 10

# Filter by tags
python3 scripts/memory-search.py "compliance" --tags tcpa,regulation

# JSON output (for programmatic use)
python3 scripts/memory-search.py "cost spike" --agent watchtower --json
```

### Decay: `memory-decay.py`

```bash
# Preview what would be archived
python3 scripts/memory-decay.py --dry-run

# Run (moves expired files to archive/)
python3 scripts/memory-decay.py

# Cron (daily at 6 AM):
# 0 6 * * * cd /path/to/repo && python3 scripts/memory-decay.py
```

### Promote: `memory-promote.py`

```bash
# Auto-promote all observations with confidence >= 0.8
python3 scripts/memory-promote.py

# Lower threshold
python3 scripts/memory-promote.py --threshold 0.7

# Only verified observations
python3 scripts/memory-promote.py --require-verified

# Specific file
python3 scripts/memory-promote.py --file obs-2026-02-15-001.md --agent shield
```

## Agent Conventions

### Writing Observations (After Every Task)

After completing a significant task, write an observation:

1. Generate a filename: `obs-YYYY-MM-DD-NNN.md`
2. Write to your `memory/vault/` directory
3. Include all frontmatter fields
4. Keep the body concise — facts, numbers, decisions, not narratives

### Recalling Observations (Before Responding)

Before making decisions or responding to queries:

```bash
python3 scripts/memory-search.py "relevant query" --agent YOUR_NAME --limit 3
```

This is added to each agent's HEARTBEAT.md as a recall step.

### Backlinks

When an observation references another, add the filename to `backlinks`. This creates a web of connected knowledge:

```yaml
backlinks: [obs-2026-02-14-003, obs-2026-02-13-001]
```

## Confidence Levels

| Level | Range | Meaning |
|-------|-------|---------|
| Speculative | 0.3-0.5 | Hypothesis, early signal |
| Probable | 0.5-0.7 | Pattern observed, needs confirmation |
| Confident | 0.7-0.85 | Verified by data, actionable |
| Certain | 0.85-1.0 | Confirmed by multiple sources or human |

## How Search Works

1. Loads all `.md` files from vault directories
2. Parses frontmatter, filters by decay/confidence
3. Builds TF-IDF index (term frequency × inverse document frequency)
4. Ranks by cosine similarity × confidence × decay_weight
5. Returns top N results with snippets

No vector DB. No embeddings. No external dependencies. Just math on text.
