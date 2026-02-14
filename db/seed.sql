-- ============================================================
-- Project Ocean — Seed Data (Test)
-- Run after schema.sql to populate test data
-- ============================================================

-- Test Buyers
INSERT INTO buyers (name, company, contact_email, contact_phone, verticals, daily_cap, payout_per_lead, payout_terms, preferred_hours, status)
VALUES
    ('John Smith', 'Debt Solutions Inc', 'john@debtsolutions.example.com', '+1-555-0101',
     ARRAY['debt_relief'], 25, 55.00, 'net15', '9-17 EST', 'active'),
    ('Sarah Johnson', 'Freedom Financial Partners', 'sarah@freedomfp.example.com', '+1-555-0102',
     ARRAY['debt_relief', 'tax_debt'], 50, 65.00, 'net30', '8-18 EST', 'active');

-- Test Campaign
INSERT INTO campaigns (name, source, channel, daily_budget, total_spend, lead_count, status)
VALUES
    ('FB Debt Relief v1', 'fb', 'facebook_feed', 100.00, 0, 0, 'active');

-- Test Leads
INSERT INTO leads (source, first_name, last_name, email, phone, state, zip, debt_amount, debt_type, income_range, employment_status, quality_score, quality_tier, status)
VALUES
    ('fb', 'Alice', 'Williams', 'alice.w@example.com', '+1-555-1001', 'CA', '90210', 25000.00, 'credit_card', '50k-75k', 'employed', 85, 'A', 'scored'),
    ('fb', 'Bob', 'Martinez', 'bob.m@example.com', '+1-555-1002', 'TX', '75001', 18000.00, 'medical', '30k-50k', 'employed', 72, 'B', 'scored'),
    ('revpie', 'Carol', 'Davis', 'carol.d@example.com', '+1-555-1003', 'NY', '10001', 42000.00, 'mixed', '75k-100k', 'self_employed', 91, 'A', 'enriched'),
    ('email', 'David', 'Lee', 'david.l@example.com', '+1-555-1004', 'FL', '33101', 8500.00, 'personal', '25k-35k', 'employed', 55, 'C', 'new'),
    ('organic', 'Eva', 'Brown', 'eva.b@example.com', '+1-555-1005', 'IL', '60601', 35000.00, 'credit_card', '50k-75k', 'unemployed', 68, 'B', 'new');

-- Test P&L entry
INSERT INTO pnl_daily (date, revenue, cost_media, cost_calls, cost_enrichment, cost_ai, cost_other, notes)
VALUES
    (CURRENT_DATE, 0, 0, 0, 0, 0, 0, 'Day 1 — system initialized, no activity yet');
