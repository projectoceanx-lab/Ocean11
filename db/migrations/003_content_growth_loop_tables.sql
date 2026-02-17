-- ============================================================
-- Migration 003: Content growth loop tables
-- Run after initial schema + offer-cap migrations.
-- Adds dual-track content operations tables for Hawk/Shield loop.
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- CONTENT_ASSETS — Generated copy variants across channels
-- ============================================================
CREATE TABLE IF NOT EXISTS content_assets (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_key       TEXT NOT NULL,
    channel         TEXT NOT NULL CHECK (channel IN ('email', 'social')),
    asset_type      TEXT NOT NULL,
    objective       TEXT NOT NULL DEFAULT 'qualified_clicks',
    audience_segment TEXT,
    offer_context   TEXT NOT NULL DEFAULT 'debt_relief',
    variant_id      TEXT NOT NULL,
    copy_text       TEXT NOT NULL,
    cta             TEXT,
    status          TEXT NOT NULL DEFAULT 'draft'
                    CHECK (status IN ('draft', 'approved', 'blocked', 'published')),
    created_by      TEXT NOT NULL DEFAULT 'hawk',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(channel, batch_key, variant_id)
);

CREATE INDEX IF NOT EXISTS idx_content_assets_channel_status ON content_assets(channel, status);
CREATE INDEX IF NOT EXISTS idx_content_assets_objective ON content_assets(objective);
CREATE INDEX IF NOT EXISTS idx_content_assets_created_at ON content_assets(created_at DESC);

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS content_assets_updated_at ON content_assets;
CREATE TRIGGER content_assets_updated_at
    BEFORE UPDATE ON content_assets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- CONTENT_REVIEWS — Shield review outcomes per content asset
-- ============================================================
CREATE TABLE IF NOT EXISTS content_reviews (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id        UUID NOT NULL REFERENCES content_assets(id) ON DELETE CASCADE,
    reviewer        TEXT NOT NULL DEFAULT 'shield',
    result          TEXT NOT NULL CHECK (result IN ('pass', 'flag', 'block')),
    reason          TEXT,
    reason_codes    TEXT[] DEFAULT ARRAY[]::TEXT[],
    required_fixes  JSONB DEFAULT '[]'::jsonb,
    checked_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_content_reviews_asset ON content_reviews(asset_id);
CREATE INDEX IF NOT EXISTS idx_content_reviews_result ON content_reviews(result);
CREATE INDEX IF NOT EXISTS idx_content_reviews_checked_at ON content_reviews(checked_at DESC);

-- ============================================================
-- CONTENT_PERFORMANCE — Checkpoint metrics for each asset
-- ============================================================
CREATE TABLE IF NOT EXISTS content_performance (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id        UUID NOT NULL REFERENCES content_assets(id) ON DELETE CASCADE,
    checkpoint      TEXT NOT NULL CHECK (checkpoint IN ('24h', '72h', '7d')),
    impressions     INTEGER NOT NULL DEFAULT 0 CHECK (impressions >= 0),
    clicks          INTEGER NOT NULL DEFAULT 0 CHECK (clicks >= 0),
    qualified_clicks INTEGER NOT NULL DEFAULT 0 CHECK (qualified_clicks >= 0),
    lead_starts     INTEGER NOT NULL DEFAULT 0 CHECK (lead_starts >= 0),
    cpl_proxy       NUMERIC(10, 2),
    notes           TEXT,
    captured_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(asset_id, checkpoint)
);

CREATE INDEX IF NOT EXISTS idx_content_performance_asset ON content_performance(asset_id);
CREATE INDEX IF NOT EXISTS idx_content_performance_checkpoint ON content_performance(checkpoint);
CREATE INDEX IF NOT EXISTS idx_content_performance_captured_at ON content_performance(captured_at DESC);

-- ============================================================
-- CONTENT_LEARNING_EVENTS — Rule and pattern updates by outcome
-- ============================================================
CREATE TABLE IF NOT EXISTS content_learning_events (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id        UUID REFERENCES content_assets(id) ON DELETE SET NULL,
    event_type      TEXT NOT NULL CHECK (event_type IN ('promote_rule', 'add_block', 'rewrite_pattern')),
    rule_delta      JSONB NOT NULL DEFAULT '{}'::jsonb,
    confidence      NUMERIC(4, 3) CHECK (confidence >= 0 AND confidence <= 1),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_content_learning_events_type ON content_learning_events(event_type);
CREATE INDEX IF NOT EXISTS idx_content_learning_events_created_at ON content_learning_events(created_at DESC);

-- ============================================================
-- RLS + service role policy
-- ============================================================
ALTER TABLE content_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_performance ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_learning_events ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_policies
        WHERE schemaname = 'public'
          AND tablename = 'content_assets'
          AND policyname = 'Service role full access'
    ) THEN
        CREATE POLICY "Service role full access"
            ON content_assets FOR ALL USING (auth.role() = 'service_role');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_policies
        WHERE schemaname = 'public'
          AND tablename = 'content_reviews'
          AND policyname = 'Service role full access'
    ) THEN
        CREATE POLICY "Service role full access"
            ON content_reviews FOR ALL USING (auth.role() = 'service_role');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_policies
        WHERE schemaname = 'public'
          AND tablename = 'content_performance'
          AND policyname = 'Service role full access'
    ) THEN
        CREATE POLICY "Service role full access"
            ON content_performance FOR ALL USING (auth.role() = 'service_role');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_policies
        WHERE schemaname = 'public'
          AND tablename = 'content_learning_events'
          AND policyname = 'Service role full access'
    ) THEN
        CREATE POLICY "Service role full access"
            ON content_learning_events FOR ALL USING (auth.role() = 'service_role');
    END IF;
END $$;
