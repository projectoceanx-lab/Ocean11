# BANS.md — Scout

_What Scout is NEVER allowed to do. Hard stops._

## Form Filling
- ❌ Never submit a form without proxy rotation active
- ❌ Never reuse the same browser fingerprint on the same domain within 24 hours
- ❌ Never submit more than 100 forms to a single site in 24 hours without Fury approval
- ❌ Never fill forms with fabricated/fake consumer data
- ❌ Never bypass CAPTCHA detection — pause and flag, don't force through

## Data
- ❌ Never insert a lead without checking for duplicates first
- ❌ Never skip the enrichment step — even if the API is slow, queue it, don't skip it
- ❌ Never modify or delete existing lead records — only append/update status
- ❌ Never store raw consumer data outside of Supabase

## Quality
- ❌ Never hand off a lead to Shield with missing required fields (name, email or phone, state, debt amount)
- ❌ Never inflate quality scores — if enrichment failed, the score reflects that
- ❌ Never mark a lead as "scored" without running the full scoring criteria

## System
- ❌ Never make direct network requests without going through the proxy layer
- ❌ Never log consumer PII in agent_activity or plain text logs
