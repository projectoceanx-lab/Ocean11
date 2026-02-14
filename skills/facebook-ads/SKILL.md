# Facebook Ads Skill

Facebook/Meta Ads API integration for paid lead acquisition campaigns.

## Capabilities
- **Campaign Creation** — Create campaigns with debt relief targeting
- **Ad Set Management** — Audience targeting, budget setting, scheduling
- **Ad Creative** — Create/update ad copy and creative assets
- **Budget Management** — Adjust daily budgets, pause underperformers
- **Reporting** — Pull spend, impressions, clicks, CPL, conversions
- **A/B Testing** — Split test audiences, creatives, landing pages

## Dependencies
- Facebook Business account with ad access
- `FACEBOOK_APP_ID`, `FACEBOOK_APP_SECRET`, `FACEBOOK_ACCESS_TOKEN`, `FACEBOOK_AD_ACCOUNT_ID` in `.env`

## Usage
```python
from skills.facebook_ads import FacebookAdsClient

fb = FacebookAdsClient()

# Get campaign performance
stats = fb.get_campaign_stats(
    campaign_id="123456789",
    date_from="2026-02-01",
    date_to="2026-02-14",
    fields=["spend", "impressions", "clicks", "actions"]
)

# Adjust budget
fb.update_budget(campaign_id="123456789", daily_budget=75.00)

# Pause underperformer
fb.pause_campaign(campaign_id="123456789")
```

## Important Notes
- Debt relief ads require **Special Ad Category: Credit** on Facebook
- All ads must include required FTC disclaimers
- Landing pages must be compliant (Shield reviews before launch)

## Used By
- **Hawk** — Campaign creation, optimization, reporting
