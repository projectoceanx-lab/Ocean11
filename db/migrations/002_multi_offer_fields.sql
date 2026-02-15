-- ============================================================
-- Migration 002: Multi-offer field mapping support
-- Run after 001_initial.sql
-- 
-- Problem: Each debt relief offer (JGW, NDR, FDR, Pacific Debt)
-- has different form fields. We need a flexible schema.
--
-- Solution: Common fields as columns + JSONB for offer-specific.
-- offer_fields table maps each offer's form to our DB.
-- ============================================================

-- New common fields (discovered from JG Wentworth mapping)
ALTER TABLE leads ADD COLUMN IF NOT EXISTS date_of_birth DATE;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS address1 TEXT;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS address2 TEXT;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS city TEXT;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS property_status TEXT 
    CHECK (property_status IN ('rent', 'own_with_mortgage', 'own_outright', NULL));
ALTER TABLE leads ADD COLUMN IF NOT EXISTS annual_income NUMERIC(12, 2);

-- Flexible JSONB for offer-specific fields
ALTER TABLE leads ADD COLUMN IF NOT EXISTS form_data JSONB DEFAULT '{}'::jsonb;

-- Which offer generated this lead
ALTER TABLE leads ADD COLUMN IF NOT EXISTS offer_name TEXT;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_leads_form_data ON leads USING gin(form_data);
CREATE INDEX IF NOT EXISTS idx_leads_offer_name ON leads(offer_name);
CREATE INDEX IF NOT EXISTS idx_leads_annual_income ON leads(annual_income);

-- ============================================================
-- OFFER_FIELDS — Field mapping registry per offer/target
-- Scout reads this to know what to fill per target.
-- When we add a new offer, we INSERT rows here — no schema change needed.
-- ============================================================
CREATE TABLE IF NOT EXISTS offer_fields (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    offer_name      TEXT NOT NULL,
    offer_url       TEXT NOT NULL,
    field_name      TEXT NOT NULL,
    api_name        TEXT NOT NULL,
    field_type      TEXT NOT NULL,
    db_column       TEXT,
    options         JSONB,
    required        BOOLEAN DEFAULT false,
    step_number     INTEGER,
    notes           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(offer_name, field_name)
);

CREATE INDEX IF NOT EXISTS idx_offer_fields_offer ON offer_fields(offer_name);
ALTER TABLE offer_fields ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Service role full access" ON offer_fields FOR ALL USING (auth.role() = 'service_role');
