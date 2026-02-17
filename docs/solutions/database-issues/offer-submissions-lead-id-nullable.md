---
title: "Offer Submissions lead_id Nullable"
date: 2026-02-17
tags: [supabase, migration, offer-submissions, schema]
category: database-issues
severity: medium
status: resolved
related_files:
  - db/migrations/002_offer_submissions_lead_id_nullable.sql
  - db/offer_caps_schema.sql
  - scripts/fdr-ndr-fill.py
---

# Offer Submissions lead_id Nullable

## Problem

`offer_submissions.lead_id` was defined as `NOT NULL` in the original schema (`db/offer_caps_schema.sql`), blocking CLI and test form fills that don't have a corresponding lead record in the `leads` table. Every `--dry-run` or manual test required creating a throwaway lead first, adding friction to the development workflow.

## Investigation

The form fill script (`scripts/fdr-ndr-fill.py`) supports three modes:

1. **Production** — Lead exists in DB, `--lead-id <uuid>` passed, `lead_id` available
2. **CLI test** — Manual args (`--first-name`, `--email`, etc.), no lead record
3. **Default test** — Uses hardcoded `TEST_LEAD`, no lead record

Modes 2 and 3 had no `lead_id` to insert. The script was working around this by skipping the DB insert entirely:

```python
if lead_id is None:
    print(f"[!] No lead_id -- skipping DB log (CLI/test mode)")
    return
```

This meant test submissions were invisible to the pipeline — no cap tracking, no postback matching, no audit trail.

## Root Cause

The original schema enforced referential integrity too tightly:

```sql
lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE
```

This is correct for production but blocks test/development workflows where form fills happen independently of lead acquisition.

## Solution

### Migration (`db/migrations/002_offer_submissions_lead_id_nullable.sql`)

```sql
-- Make lead_id nullable
ALTER TABLE offer_submissions ALTER COLUMN lead_id DROP NOT NULL;

-- Recreate dedup index to handle NULLs
-- (SQL: NULL != NULL, so the old UNIQUE index wouldn't prevent dupes with NULL lead_id)
DROP INDEX IF EXISTS idx_submissions_dedup;
CREATE UNIQUE INDEX idx_submissions_dedup
  ON offer_submissions(offer_id, lead_id)
  WHERE lead_id IS NOT NULL;
```

Key detail on the dedup index: In PostgreSQL, `NULL != NULL` always evaluates to `NULL` (not `TRUE`). A `UNIQUE` index on `(offer_id, lead_id)` without the `WHERE` clause would allow unlimited rows with the same `offer_id` and `NULL lead_id` — defeating deduplication. The partial index `WHERE lead_id IS NOT NULL` preserves dedup for production submissions while allowing multiple test submissions.

### What This Enables

- **Test submissions are logged** — Cap counters, click IDs, and statuses are tracked even without a lead
- **Postbacks can match test submissions** — `everflow_click_id` matching works regardless of `lead_id`
- **Decouples acquisition from delivery** — Lead acquisition (Scout) and form delivery (Signal) can operate independently
- **No throwaway leads** — No more polluting the `leads` table with fake test data

## Prevention

- Schema changes that enforce `NOT NULL` on foreign keys should consider whether the referenced entity always exists at insert time
- Test/development workflows should be first-class considerations in schema design
- Migration files go in `db/migrations/` with sequential numbering and descriptive names

## Related

- [Everflow Postback Pipeline Setup](../integration-issues/everflow-postback-pipeline-setup.md) — the pipeline that uses `offer_submissions`
- [FDR/NDR Form Fill Automation](../integration-issues/fdr-ndr-form-fill-automation.md) — the script that creates submissions
