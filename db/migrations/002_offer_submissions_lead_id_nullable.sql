-- Migration: Make offer_submissions.lead_id nullable
-- Reason: CLI/test form fills don't always have a lead record.
--         Production queue runs always provide lead_id.
-- Run this in Supabase SQL Editor.
-- Date: 2026-02-17

ALTER TABLE offer_submissions ALTER COLUMN lead_id DROP NOT NULL;

-- Also update the dedup index to handle NULLs properly
-- (NULL != NULL in SQL, so the unique index won't prevent dupes with NULL lead_id)
DROP INDEX IF EXISTS idx_submissions_dedup;
CREATE UNIQUE INDEX idx_submissions_dedup ON offer_submissions(offer_id, lead_id) WHERE lead_id IS NOT NULL;
