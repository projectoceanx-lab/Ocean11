# Ocean Content Loop Skill

Closed-loop content operations for Project Ocean. This skill turns copy production into a deterministic system:

Draft -> preflight lint -> Shield gate -> publish -> checkpoint metrics -> rule updates.

## Capabilities
- **Dual-track generation**: Email + social variants from one objective.
- **Preflight enforcement**: Blocks risky copy before compliance review.
- **Shield gating**: Every asset receives pass/flag/block disposition.
- **Performance checkpoints**: 24h, 72h, 7d metric capture.
- **Learning loop**: Promote winning patterns and block failing patterns.

## Source Of Truth
- `docs/VOICE_GUIDE.md`
- `config/copy_lexicon.yaml`
- `docs/COPY_PREFLIGHT_CHECKLIST.md`
- `workflows/content-growth-loop.yaml`

## Directory Layout
- `templates/email_sequence_blocks.md` — modular email structures
- `templates/social_post_blocks.md` — social post structures
- `templates/cta_matrix.md` — CTA/channel objective mapping
- `templates/failure_patterns.md` — repeat failure catalog
- `rules/allowed_claims.yaml` — allowed language scaffolding
- `rules/blocked_claims.yaml` — hard-stop language
- `rules/channel_requirements.yaml` — channel-specific must-have rules

## Usage
1. Draft variants with one objective at a time.
2. Run `scripts/content-preflight-lint.py` before Shield review.
3. Route assets to Shield and record result in `content_reviews`.
4. Publish only `approved` assets.
5. Log performance in `content_performance`.
6. Write `content_learning_events` and update rules files weekly.

## Guardrails
- Never bypass Shield for publish/send.
- Never use blocked claims, even for test variants.
- Optimize on qualified intent metrics first, not vanity views.

## Used By
- **Hawk** — drafting, channel execution, optimization.
- **Shield** — compliance gate.
- **Ocean/Fury** — weekly decision packets and scale/kill decisions.
