# Memory Architecture — Project Ocean

Three-tier memory system. Zero dependencies. Filesystem only. Importance is earned, not declared.

## Philosophy

> Hardcoded confidence scores are vibes dressed as numbers. Instead: **everything starts equal, importance proves itself through usage.**

An observation matters if it gets referenced, influences decisions, predicts correctly, or a human flags it. Untouched observations fade. Referenced ones survive. This is PageRank for memory.

## Three Tiers

```
Tier 1: Session Memory (ephemeral)
  └─ OpenClaw native memory_search / memory_get
  └─ Lives and dies with the session. Most stuff belongs here.

Tier 2: Agent Vault (persistent, per-agent)
  └─ agents/{name}/memory/vault/   — observations that matter
  └─ agents/{name}/memory/archive/ — decayed observations
  └─ Survives across sessions. Agent reads vault on startup.

Tier 3: Shared Truth (promoted, cross-agent)
  └─ shared/observations/ — earned its way here through usage
  └─ Institutional memory. What the operation knows for sure.
```

```
repo/
├── agents/{name}/memory/
│   ├── vault/          # Active observations (markdown + YAML frontmatter)
│   └── archive/        # Decayed observations (auto-moved by maintenance)
├── shared/observations/ # Promoted observations (read by all agents)
└── scripts/
    ├── memory-search.py   # TF-IDF search across vaults
    ├── memory-decay.py    # Archive stale observations (daily cron)
    └── memory-promote.py  # Promote high-importance obs to shared/
```

## The Bridge: End-of-Session Flush

When an agent session ends (or at heartbeat), it asks itself:

> *"Did I learn anything worth remembering?"*

**If yes** → write an observation to vault. **If no** → nothing. Session memory dies clean.

Only flush:
- Numbers that changed (CPL went from $12 to $15)
- Patterns spotted (insurance leads convert 2x on Tuesdays)
- Decisions made (paused RevPie — ROI negative)
- Failures (delivery rejected by buyer X — wrong format)

NOT: routine searches, status checks, things that didn't change.

## Observation Format

```markdown
---
tags: [campaign, ctr, insurance]
importance: 0.5
created: 2026-02-15
max_age: 30d
source: watchtower
refs: 0
ref_by: []
backlinks: []
verified: false
---
Insurance vertical CTR dropped 12% week-over-week. Possible creative fatigue or audience saturation.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `tags` | Yes | Searchable topic tags |
| `importance` | Yes | Starts at 0.5 — earned through usage (never manually set above 0.5 at creation) |
| `created` | Yes | YYYY-MM-DD |
| `max_age` | Yes | Maximum lifespan before decay review: `14d`, `30d`, `90d`, `180d`, or `permanent` |
| `source` | Yes | Which agent wrote it |
| `refs` | Auto | Number of times this observation has been referenced |
| `ref_by` | Auto | List of observation IDs that reference this one |
| `backlinks` | No | Observations this one references (creates bidirectional web) |
| `verified` | No | Set to `true` when confirmed by outcome, another agent, or human |

### Naming Convention

`obs-YYYY-MM-DD-NNN.md` where NNN is a sequence number (001, 002, ...).

## Importance: Earned, Not Declared

**Everything starts at 0.5.** Importance changes based on what happens after:

| Event | Importance Change |
|-------|-------------------|
| Referenced by another observation (same agent) | +0.1 |
| Referenced by a different agent's observation | +0.15 |
| Led to a decision that produced positive outcome | +0.2 |
| Prediction matched reality (verified by data) | +0.15 |
| Human flagged as important | → set to 0.95 |
| Human flagged as wrong | → set to 0.0 (archive immediately) |
| Not referenced in 14+ days | -0.1 per 14-day period |
| Contradicted by newer observation | -0.2 |

**Cap: 1.0 max, 0.0 min.** Importance below 0.2 triggers accelerated decay.

### How References Work

When an agent writes a new observation and includes `backlinks: [obs-2026-02-14-003]`:
1. The referenced observation's `refs` count increments
2. The referenced observation's `ref_by` list gets the new observation ID
3. The referenced observation's `importance` increases per the table above

This is automatic — handled by the maintenance scripts.

## Max Age Guidelines

| Type | Max Age | Use For |
|------|---------|---------|
| Tactical | `14d` | Daily metrics, system status, one-off events |
| Operational | `30d` | Campaign performance, source quality changes |
| Strategic | `90d` | Buyer relationships, pricing, market shifts |
| Compliance | `180d` | Regulatory changes, legal precedents |
| Permanent | `permanent` | Core business rules, SOPs, human directives |

**Max age is a ceiling, not a guarantee.** Low-importance observations can be archived before max age. High-importance observations get max age extended automatically:
- importance ≥ 0.8 → max age doubles
- importance ≥ 0.9 → max age triples or becomes permanent

## Promotion to Shared (Tier 3)

Observations are promoted to `shared/observations/` when they **earn it**:

- `importance ≥ 0.8` (reached through usage, not declaration)
- OR `verified: true` AND `importance ≥ 0.6`
- OR human explicitly promotes it

Promoted observations are readable by all agents. The original stays in the agent's vault (with a `promoted: true` flag). Shared copy gets a prefix: `{source}-obs-YYYY-MM-DD-NNN.md`.

## Decay & Maintenance

### Daily Maintenance (cron)

1. **Decay sweep** — Check all vault observations:
   - Past max age + low importance (< 0.4) → archive
   - Past max age + medium importance (0.4-0.7) → flag for review
   - Past max age + high importance (≥ 0.7) → extend max age
   - Importance below 0.2 regardless of age → archive
2. **Reference update** — Recalculate `refs`, `ref_by`, and importance adjustments
3. **Promotion sweep** — Auto-promote qualifying observations to shared

### Scripts

```bash
# Search your vault + shared
python3 scripts/memory-search.py "CPL trend" --agent hawk --limit 5

# Search everything
python3 scripts/memory-search.py "buyer acceptance" --all --limit 10

# Decay: preview
python3 scripts/memory-decay.py --dry-run

# Decay: execute
python3 scripts/memory-decay.py

# Promote: auto-promote qualifying observations
python3 scripts/memory-promote.py
```

## Agent Conventions

### Writing (End-of-Session Flush)

Ask: *"Did I learn something worth remembering?"*

If yes:
1. Generate filename: `obs-YYYY-MM-DD-NNN.md`
2. Write to your `memory/vault/`
3. Set `importance: 0.5` (always — never inflate at creation)
4. Set appropriate `max_age` based on type
5. Add `backlinks` to related observations if they exist
6. Keep body concise — facts, numbers, decisions. Not narratives.

### Reading (Session Startup / Before Decisions)

1. OpenClaw `memory_search` for quick in-session recall
2. For cross-session knowledge: `python3 scripts/memory-search.py "query" --agent YOUR_NAME`
3. Check `shared/observations/` for cross-agent knowledge

### Referencing

When your observation builds on another:
```yaml
backlinks: [obs-2026-02-14-003, obs-2026-02-13-001]
```
This automatically boosts the referenced observations' importance. Knowledge that connects = knowledge that survives.

## How Search Works

1. Loads all `.md` files from vault directories
2. Parses frontmatter, filters by importance (> 0.1) and age
3. Builds TF-IDF index (term frequency × inverse document frequency)
4. Ranks by: `cosine_similarity × importance × freshness_weight`
5. Returns top N results with snippets

No vector DB. No embeddings. No external dependencies. Just math on text.

## Summary

- **Write rarely, write well.** Not every task deserves an observation.
- **Importance is earned.** Start at 0.5, prove your worth through references and outcomes.
- **Unused knowledge fades.** That's a feature, not a bug.
- **Connected knowledge survives.** Backlinks = importance = longevity.
- **Shared truth is sacred.** Only observations that proved themselves get promoted.

This is natural selection for memory. The fittest observations survive.
