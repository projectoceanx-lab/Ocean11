-- ============================================================
-- OFFER CAPS & POSTBACK TRACKING — Extension Schema
-- Project Ocean — Cap Management at Everflow Offer ID Level
-- Run this in Supabase SQL Editor AFTER schema.sql
-- ============================================================

-- ============================================================
-- EVERFLOW_OFFERS — Our Everflow offer catalog with caps
-- ============================================================
CREATE TABLE IF NOT EXISTS everflow_offers (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    offer_id        INTEGER NOT NULL UNIQUE,                         -- Everflow offer ID (e.g., 4930)
    offer_name      TEXT NOT NULL,                                   -- e.g., "FDR - CPL - Email"
    buyer_name      TEXT NOT NULL,                                   -- e.g., "Freedom Debt Relief"
    buyer_short     VARCHAR(10) NOT NULL,                            -- e.g., "FDR", "NDR", "JGW"
    cpa             NUMERIC(8, 2) NOT NULL,                          -- Payout per confirmed conversion
    channel         TEXT NOT NULL CHECK (channel IN ('web', 'email', 'call', 'any')),
    vertical        TEXT NOT NULL DEFAULT 'debt_relief',
    
    -- Cap configuration (set by AK from buyer relationships)
    weekly_cap      INTEGER,                                         -- Max confirmed conversions per week (NULL = unlimited)
    daily_cap       INTEGER,                                         -- Max confirmed conversions per day (NULL = unlimited)
    
    -- Running counts (reset by cron)
    weekly_submissions  INTEGER NOT NULL DEFAULT 0,                  -- Forms we filled this week
    weekly_conversions  INTEGER NOT NULL DEFAULT 0,                  -- Everflow postback confirmations this week
    daily_submissions   INTEGER NOT NULL DEFAULT 0,                  -- Forms we filled today
    daily_conversions   INTEGER NOT NULL DEFAULT 0,                  -- Everflow postback confirmations today
    
    -- Safety: stop submitting at this % of cap (prevents over-delivery while postbacks pending)
    cap_safety_pct  NUMERIC(3, 2) NOT NULL DEFAULT 0.80,            -- Stop at 80% of cap by default
    
    -- Restrictions
    excluded_states TEXT[] DEFAULT '{}',                              -- States NOT to send (e.g., '{CA,NY}')
    schedule        TEXT DEFAULT 'M-F',                               -- M-F, 7days, weekends
    min_debt_amount NUMERIC(12, 2),                                  -- Minimum debt for this offer
    max_debt_amount NUMERIC(12, 2),                                  -- Maximum debt (NULL = no max)
    
    -- Tracking URLs
    everflow_url    TEXT,                                             -- Everflow tracking/click URL
    form_url        TEXT,                                             -- Buyer's actual form URL
    
    -- Status
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'paused', 'capped', 'expired')),
    notes           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ef_offers_offer_id ON everflow_offers(offer_id);
CREATE INDEX idx_ef_offers_buyer_short ON everflow_offers(buyer_short);
CREATE INDEX idx_ef_offers_status ON everflow_offers(status);

CREATE TRIGGER ef_offers_updated_at
    BEFORE UPDATE ON everflow_offers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- OFFER_SUBMISSIONS — Every form fill attempt we make
-- ============================================================
CREATE TABLE IF NOT EXISTS offer_submissions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    offer_id        INTEGER NOT NULL REFERENCES everflow_offers(offer_id),
    lead_id         UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    
    -- Submission details
    status          TEXT NOT NULL DEFAULT 'submitted'
                    CHECK (status IN ('submitted', 'converted', 'rejected', 'duplicate', 'expired')),
    submitted_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Everflow postback data (filled when postback fires)
    conversion_id   TEXT,                                            -- Everflow conversion/transaction ID
    converted_at    TIMESTAMPTZ,
    payout          NUMERIC(8, 2),                                   -- Actual payout from postback
    rejection_reason TEXT,                                           -- If rejected: reason from buyer
    
    -- Metadata
    everflow_click_id TEXT,                                          -- aff_click_id we sent
    postback_raw    JSONB DEFAULT '{}'::jsonb,                       -- Full postback payload for audit
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_submissions_offer_id ON offer_submissions(offer_id);
CREATE INDEX idx_submissions_lead_id ON offer_submissions(lead_id);
CREATE INDEX idx_submissions_status ON offer_submissions(status);
CREATE INDEX idx_submissions_submitted_at ON offer_submissions(submitted_at DESC);
-- Prevent duplicate submissions: same lead to same offer
CREATE UNIQUE INDEX idx_submissions_dedup ON offer_submissions(offer_id, lead_id);

CREATE TRIGGER submissions_updated_at
    BEFORE UPDATE ON offer_submissions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- POSTBACK_LOG — Raw log of every Everflow postback received
-- ============================================================
CREATE TABLE IF NOT EXISTS postback_log (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    received_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_ip       TEXT,
    method          TEXT,                                             -- GET or POST
    query_params    JSONB DEFAULT '{}'::jsonb,                       -- Full query string as JSON
    body            JSONB DEFAULT '{}'::jsonb,                       -- POST body if any
    offer_id        INTEGER,                                         -- Parsed from postback
    click_id        TEXT,                                             -- Parsed aff_click_id
    payout          NUMERIC(8, 2),                                   -- Parsed payout amount
    processed       BOOLEAN NOT NULL DEFAULT FALSE,                  -- Has this been matched to a submission?
    processed_at    TIMESTAMPTZ,
    error           TEXT                                              -- If processing failed
);

CREATE INDEX idx_postback_log_received ON postback_log(received_at DESC);
CREATE INDEX idx_postback_log_processed ON postback_log(processed);
CREATE INDEX idx_postback_log_click_id ON postback_log(click_id);

-- ============================================================
-- CAP CHECK FUNCTION — Call before every submission
-- Returns: can_submit (boolean), reason (text), remaining (integer)
-- ============================================================
CREATE OR REPLACE FUNCTION check_offer_cap(p_offer_id INTEGER)
RETURNS TABLE(can_submit BOOLEAN, reason TEXT, daily_remaining INTEGER, weekly_remaining INTEGER) AS $$
DECLARE
    v_offer everflow_offers%ROWTYPE;
    v_daily_remaining INTEGER;
    v_weekly_remaining INTEGER;
    v_daily_safe_limit INTEGER;
    v_weekly_safe_limit INTEGER;
BEGIN
    SELECT * INTO v_offer FROM everflow_offers WHERE offer_id = p_offer_id;
    
    IF NOT FOUND THEN
        RETURN QUERY SELECT FALSE, 'Offer not found'::TEXT, 0, 0;
        RETURN;
    END IF;
    
    IF v_offer.status != 'active' THEN
        RETURN QUERY SELECT FALSE, ('Offer status: ' || v_offer.status)::TEXT, 0, 0;
        RETURN;
    END IF;
    
    -- Check daily cap (if set)
    IF v_offer.daily_cap IS NOT NULL THEN
        v_daily_safe_limit := FLOOR(v_offer.daily_cap * v_offer.cap_safety_pct);
        v_daily_remaining := v_daily_safe_limit - v_offer.daily_submissions;
        IF v_daily_remaining <= 0 THEN
            RETURN QUERY SELECT FALSE, 'Daily cap reached (safety limit)'::TEXT, 0, 
                COALESCE(v_offer.weekly_cap - v_offer.weekly_submissions, 999);
            RETURN;
        END IF;
    ELSE
        v_daily_remaining := 999;
    END IF;
    
    -- Check weekly cap (if set)
    IF v_offer.weekly_cap IS NOT NULL THEN
        v_weekly_safe_limit := FLOOR(v_offer.weekly_cap * v_offer.cap_safety_pct);
        v_weekly_remaining := v_weekly_safe_limit - v_offer.weekly_submissions;
        IF v_weekly_remaining <= 0 THEN
            RETURN QUERY SELECT FALSE, 'Weekly cap reached (safety limit)'::TEXT, v_daily_remaining, 0;
            RETURN;
        END IF;
    ELSE
        v_weekly_remaining := 999;
    END IF;
    
    RETURN QUERY SELECT TRUE, 'OK'::TEXT, v_daily_remaining, v_weekly_remaining;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- INCREMENT SUBMISSION COUNT — Call after every form fill
-- ============================================================
CREATE OR REPLACE FUNCTION increment_submission(p_offer_id INTEGER)
RETURNS VOID AS $$
BEGIN
    UPDATE everflow_offers 
    SET daily_submissions = daily_submissions + 1,
        weekly_submissions = weekly_submissions + 1,
        updated_at = NOW()
    WHERE offer_id = p_offer_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- RECORD CONVERSION — Call when Everflow postback fires
-- ============================================================
CREATE OR REPLACE FUNCTION record_conversion(
    p_click_id TEXT,
    p_payout NUMERIC DEFAULT NULL,
    p_conversion_id TEXT DEFAULT NULL
)
RETURNS TABLE(success BOOLEAN, message TEXT) AS $$
DECLARE
    v_submission offer_submissions%ROWTYPE;
BEGIN
    -- Find the submission by click_id
    SELECT * INTO v_submission 
    FROM offer_submissions 
    WHERE everflow_click_id = p_click_id AND status = 'submitted'
    LIMIT 1;
    
    IF NOT FOUND THEN
        RETURN QUERY SELECT FALSE, 'No matching submission for click_id: ' || p_click_id;
        RETURN;
    END IF;
    
    -- Update submission
    UPDATE offer_submissions 
    SET status = 'converted',
        converted_at = NOW(),
        payout = COALESCE(p_payout, payout),
        conversion_id = p_conversion_id,
        updated_at = NOW()
    WHERE id = v_submission.id;
    
    -- Increment conversion counts on offer
    UPDATE everflow_offers 
    SET daily_conversions = daily_conversions + 1,
        weekly_conversions = weekly_conversions + 1,
        updated_at = NOW()
    WHERE offer_id = v_submission.offer_id;
    
    -- Update lead status to delivered
    UPDATE leads SET status = 'delivered', updated_at = NOW()
    WHERE id = v_submission.lead_id;
    
    RETURN QUERY SELECT TRUE, 'Conversion recorded for offer ' || v_submission.offer_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- DAILY RESET — Run at midnight EST via cron
-- Resets daily counts, checks if weekly cap hit → marks offer capped
-- ============================================================
CREATE OR REPLACE FUNCTION reset_daily_caps()
RETURNS VOID AS $$
BEGIN
    UPDATE everflow_offers 
    SET daily_submissions = 0, 
        daily_conversions = 0,
        -- If weekly cap hit, mark as capped
        status = CASE 
            WHEN weekly_cap IS NOT NULL AND weekly_conversions >= weekly_cap THEN 'capped'
            ELSE 'active'
        END,
        updated_at = NOW()
    WHERE status IN ('active', 'capped');
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- WEEKLY RESET — Run Monday midnight EST via cron
-- ============================================================
CREATE OR REPLACE FUNCTION reset_weekly_caps()
RETURNS VOID AS $$
BEGIN
    UPDATE everflow_offers 
    SET weekly_submissions = 0, 
        weekly_conversions = 0,
        status = 'active',  -- Re-activate capped offers for new week
        updated_at = NOW()
    WHERE status IN ('active', 'capped');
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- RLS for new tables
-- ============================================================
ALTER TABLE everflow_offers ENABLE ROW LEVEL SECURITY;
ALTER TABLE offer_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE postback_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access" ON everflow_offers FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON offer_submissions FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON postback_log FOR ALL USING (auth.role() = 'service_role');

-- ============================================================
-- SEED: Real Everflow offers (from AK's account)
-- Caps: 50/week each for NDR, FDR, JGW (AK confirmed Feb 15)
-- ============================================================
INSERT INTO everflow_offers (offer_id, offer_name, buyer_name, buyer_short, cpa, channel, weekly_cap, schedule, notes) VALUES
-- FDR
(4930, 'FDR - CPL - Email', 'Freedom Debt Relief', 'FDR', 60.00, 'email', 50, 'M-F', 'Email only, M-F drops. Highest CPA.'),
-- NDR  
(4905, 'NDR Private - CPL - Budgeted', 'National Debt Relief', 'NDR', 50.00, 'web', 50, 'M-F', 'Web traffic, M-F. $50 CPA tier.'),
(4836, 'NDR Private - CPL - Budgeted (Email)', 'National Debt Relief', 'NDR', 45.00, 'email', 50, 'M-F', 'Email channel. M-F only.'),
(4632, 'NDR - CPL (weekends)', 'National Debt Relief', 'NDR', 24.00, 'web', 50, '7days', 'Weekends included. Lower CPA.'),
(4528, 'NDR Private - CPL - Email Only', 'National Debt Relief', 'NDR', 16.00, 'email', 50, '7days', 'Email only, lowest NDR tier.'),
-- JGW
(4633, 'JGW CPL weekends (NO CA)', 'JG Wentworth', 'JGW', 24.00, 'web', 50, '7days', 'Excludes California.'),
(4737, 'JGW Debt Settlement M-F', 'JG Wentworth', 'JGW', 22.00, 'email', 50, 'M-F', 'Email, M-F only.'),
(4592, 'JGW - CPL', 'JG Wentworth', 'JGW', 25.00, 'web', 50, 'M-F', 'Web traffic, M-F. Primary JGW offer.'),
(4591, 'JGW CPL (Call Center)', 'JG Wentworth', 'JGW', 24.00, 'call', 50, 'M-F', 'Call center channel.'),
-- Cliqsilver
(4731, 'Cliqsilver - CPL', 'Cliqsilver', 'CLIQ', 30.00, 'web', 50, 'M-F', 'Web traffic, M-F.')
ON CONFLICT (offer_id) DO NOTHING;
