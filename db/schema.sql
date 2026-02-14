-- ============================================================
-- Project Ocean — Database Schema
-- Supabase-compatible PostgreSQL
-- Run this in Supabase SQL Editor to create all tables
-- ============================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- LEADS — Core lead data from all acquisition channels
-- ============================================================
CREATE TABLE leads (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source          TEXT NOT NULL,                                    -- fb, email, revpie, organic, form
    form_url        TEXT,                                             -- URL of the form that generated this lead
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT,
    phone           TEXT,
    state           VARCHAR(2),                                      -- US state code (CA, TX, NY, etc.)
    zip             VARCHAR(10),
    debt_amount     NUMERIC(12, 2),                                  -- Total reported debt
    debt_type       TEXT,                                             -- credit_card, medical, student, personal, mixed
    income_range    TEXT,                                             -- e.g. "30k-50k", "50k-75k"
    employment_status TEXT,                                           -- employed, unemployed, self_employed, retired
    enrichment_data JSONB DEFAULT '{}'::jsonb,                       -- FastDebt API response, additional data
    quality_score   INTEGER CHECK (quality_score >= 0 AND quality_score <= 100),
    quality_tier    VARCHAR(1) CHECK (quality_tier IN ('A', 'B', 'C', 'D')),
    vertical        TEXT DEFAULT 'debt_relief',                      -- debt_relief, tax_debt, student_loan
    status          TEXT NOT NULL DEFAULT 'new'
                    CHECK (status IN ('new', 'enriched', 'scored', 'delivered', 'rejected')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_quality_tier ON leads(quality_tier);
CREATE INDEX idx_leads_source ON leads(source);
CREATE INDEX idx_leads_state ON leads(state);
CREATE INDEX idx_leads_created_at ON leads(created_at DESC);
CREATE UNIQUE INDEX idx_leads_email_phone ON leads(email, phone) WHERE email IS NOT NULL AND phone IS NOT NULL;

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER leads_updated_at
    BEFORE UPDATE ON leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- BUYERS — Lead buyers and their preferences
-- ============================================================
CREATE TABLE buyers (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name                TEXT NOT NULL,
    company             TEXT NOT NULL,
    contact_email       TEXT NOT NULL,
    contact_phone       TEXT,
    verticals           TEXT[] NOT NULL DEFAULT ARRAY['debt_relief'],
    daily_cap           INTEGER NOT NULL DEFAULT 50,
    current_daily_count INTEGER NOT NULL DEFAULT 0,
    payout_per_lead     NUMERIC(8, 2) NOT NULL,                     -- What they pay us per accepted lead
    payout_terms        TEXT DEFAULT 'net30',                        -- net7, net15, net30, prepaid
    preferred_hours     TEXT DEFAULT '9-17 EST',                     -- When they accept deliveries
    compliance_notes    TEXT,                                         -- Buyer-specific compliance requirements
    status              TEXT NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active', 'paused', 'dropped')),
    relationship_score  INTEGER DEFAULT 50 CHECK (relationship_score >= 0 AND relationship_score <= 100),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_buyers_status ON buyers(status);

-- Reset daily counts at midnight — run via Supabase cron or pg_cron
-- SELECT cron.schedule('reset-buyer-caps', '0 0 * * *', $$UPDATE buyers SET current_daily_count = 0$$);

-- ============================================================
-- CAMPAIGNS — Ad campaigns and traffic sources
-- ============================================================
CREATE TABLE campaigns (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        TEXT NOT NULL,
    source      TEXT NOT NULL CHECK (source IN ('fb', 'email', 'revpie', 'organic')),
    channel     TEXT,                                                -- facebook_feed, email_blast, aged_list, etc.
    daily_budget NUMERIC(10, 2),
    total_spend NUMERIC(12, 2) NOT NULL DEFAULT 0,
    lead_count  INTEGER NOT NULL DEFAULT 0,
    cpl         NUMERIC(8, 2) GENERATED ALWAYS AS (
                    CASE WHEN lead_count > 0 THEN total_spend / lead_count ELSE NULL END
                ) STORED,
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'paused', 'completed', 'killed')),
    start_date  DATE NOT NULL DEFAULT CURRENT_DATE,
    end_date    DATE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_source ON campaigns(source);

-- ============================================================
-- DELIVERIES — Lead delivery attempts to buyers
-- ============================================================
CREATE TABLE deliveries (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id     UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    buyer_id    UUID NOT NULL REFERENCES buyers(id) ON DELETE CASCADE,
    channel     TEXT NOT NULL CHECK (channel IN ('email', 'call', 'api')),
    status      TEXT NOT NULL DEFAULT 'queued'
                CHECK (status IN ('queued', 'sent', 'accepted', 'rejected', 'returned')),
    payout      NUMERIC(8, 2),                                      -- Actual payout received (null until accepted)
    delivered_at TIMESTAMPTZ,
    response    TEXT,                                                -- Buyer's response or rejection reason
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_deliveries_status ON deliveries(status);
CREATE INDEX idx_deliveries_lead_id ON deliveries(lead_id);
CREATE INDEX idx_deliveries_buyer_id ON deliveries(buyer_id);
CREATE INDEX idx_deliveries_created_at ON deliveries(created_at DESC);

-- ============================================================
-- PNL_DAILY — Daily profit & loss tracking
-- ============================================================
CREATE TABLE pnl_daily (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date            DATE NOT NULL UNIQUE,
    revenue         NUMERIC(12, 2) NOT NULL DEFAULT 0,              -- Total payout from accepted leads
    cost_media      NUMERIC(12, 2) NOT NULL DEFAULT 0,              -- Facebook, RevPie, etc.
    cost_calls      NUMERIC(12, 2) NOT NULL DEFAULT 0,              -- Ringba call costs
    cost_enrichment NUMERIC(12, 2) NOT NULL DEFAULT 0,              -- FastDebt API costs
    cost_ai         NUMERIC(12, 2) NOT NULL DEFAULT 0,              -- OpenRouter / model inference
    cost_other      NUMERIC(12, 2) NOT NULL DEFAULT 0,              -- Proxies, domains, misc
    gross_profit    NUMERIC(12, 2) GENERATED ALWAYS AS (
                        revenue - cost_media - cost_calls - cost_enrichment - cost_ai - cost_other
                    ) STORED,
    margin_pct      NUMERIC(5, 2) GENERATED ALWAYS AS (
                        CASE WHEN revenue > 0 
                        THEN ((revenue - cost_media - cost_calls - cost_enrichment - cost_ai - cost_other) / revenue) * 100
                        ELSE 0 END
                    ) STORED,
    notes           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_pnl_daily_date ON pnl_daily(date DESC);

-- ============================================================
-- COMPLIANCE_LOG — Audit trail for compliance checks
-- ============================================================
CREATE TABLE compliance_log (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id     UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    agent       TEXT NOT NULL DEFAULT 'shield',
    check_type  TEXT NOT NULL,                                      -- tsr, state_rules, tcpa, can_spam, data_accuracy
    result      TEXT NOT NULL CHECK (result IN ('pass', 'flag', 'block')),
    reason      TEXT,                                                -- Why it passed/flagged/blocked
    checked_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_compliance_log_lead_id ON compliance_log(lead_id);
CREATE INDEX idx_compliance_log_result ON compliance_log(result);
CREATE INDEX idx_compliance_log_checked_at ON compliance_log(checked_at DESC);

-- ============================================================
-- AGENT_ACTIVITY — Log of all agent actions
-- ============================================================
CREATE TABLE agent_activity (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_name  TEXT NOT NULL,                                      -- captain, scout, shield, hawk, signal, watchtower
    action      TEXT NOT NULL,                                      -- heartbeat, lead_scored, compliance_check, delivery, etc.
    details     JSONB DEFAULT '{}'::jsonb,                          -- Flexible payload
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_agent_activity_agent ON agent_activity(agent_name);
CREATE INDEX idx_agent_activity_action ON agent_activity(action);
CREATE INDEX idx_agent_activity_created_at ON agent_activity(created_at DESC);

-- ============================================================
-- ROW LEVEL SECURITY (Supabase)
-- ============================================================
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE buyers ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE deliveries ENABLE ROW LEVEL SECURITY;
ALTER TABLE pnl_daily ENABLE ROW LEVEL SECURITY;
ALTER TABLE compliance_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_activity ENABLE ROW LEVEL SECURITY;

-- Service role has full access (agents use service role key)
CREATE POLICY "Service role full access" ON leads FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON buyers FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON campaigns FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON deliveries FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON pnl_daily FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON compliance_log FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON agent_activity FOR ALL USING (auth.role() = 'service_role');
