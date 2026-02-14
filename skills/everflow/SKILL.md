# Everflow Skill

Affiliate and offer tracking platform integration for campaign management and conversion tracking.

## Capabilities
- **Offer Management** — Create/edit offers, set payout terms
- **Conversion Tracking** — Fire postbacks on successful lead delivery
- **Affiliate Reporting** — Pull performance data by offer, affiliate, date range
- **Click Tracking** — Track inbound clicks to landing pages
- **Campaign Analytics** — Revenue, conversions, EPC, CR by source

## Dependencies
- Everflow account with API access
- `EVERFLOW_API_KEY`, `EVERFLOW_ACCOUNT_ID` in `.env`

## Usage
```python
from skills.everflow import EverflowClient

ef = EverflowClient()

# Fire conversion postback
ef.fire_postback(offer_id="123", transaction_id="txn_abc", payout=55.00)

# Get campaign performance
stats = ef.get_stats(offer_id="123", date_from="2026-02-01", date_to="2026-02-14")
```

## Used By
- **Hawk** — Campaign performance analysis
- **Signal** — Conversion postbacks on delivery
