# Content Growth Loop Spec

Owner: Ocean  
Execution agents: Hawk + Shield  
Status: Implemented in repo (workflow + schema + lint + skill pack)

## Goal
Operationalize a compliance-first, self-improving content loop for dual-track channels (email and social).

## Interface Contracts

### 1) Generation Request (logical contract)
```yaml
channel: email|social
objective: qualified_clicks|lead_starts|trust_build
audience_segment: string
offer_context: debt_relief|personal_loan_cross_sell
cta: string
variant_count: integer
constraints:
  single_cta: true
  allowed_phrases_only: true
  compliance_footer_required: boolean
```

### 2) Review Result
```yaml
asset_id: uuid
reviewer: shield
result: pass|flag|block
reason_codes:
  - blocked_phrase
  - unsupported_claim
  - missing_footer
  - multi_cta_conflict
required_fixes: [string]
```

### 3) Performance Checkpoint
```yaml
asset_id: uuid
checkpoint: 24h|72h|7d
metrics:
  impressions: int
  clicks: int
  qualified_clicks: int
  lead_starts: int
decision: scale|hold|kill|rewrite
```

## Storage Tables
- `content_assets`
- `content_reviews`
- `content_performance`
- `content_learning_events`

See migration: `db/migrations/003_content_growth_loop_tables.sql`.

## Execution Flow
1. Draft assets in `content_assets` (status `draft`).
2. Run lint: `scripts/content-preflight-lint.py`.
3. Shield review logs to `content_reviews`.
4. Publish only `approved`.
5. Write checkpoints to `content_performance`.
6. Convert outcomes into `content_learning_events`.

## Test Scenarios
1. Blocked phrase exists -> lint fails.
2. Email missing required footer token -> lint fails.
3. Multiple CTA phrases in one asset -> lint fails for single-CTA channels.
4. Review result `block` -> asset cannot be marked `published`.
5. Checkpoint uniqueness -> one row per `(asset_id, checkpoint)`.

## Acceptance Criteria
1. Every published asset has one Shield review record.
2. Every asset has max one row per checkpoint (`24h`, `72h`, `7d`).
3. Zero policy-bypass path from draft to publish.
4. Weekly summary can be generated from DB tables without manual reconstruction.
