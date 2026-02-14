# RevPie Skill

Aged lead marketplace and traffic source for acquiring pre-generated debt relief leads.

## Capabilities
- **Aged Lead Purchase** — Buy leads 30-90 days old at discounted rates
- **Campaign Management** — Set filters (state, debt type, amount range)
- **Real-time Leads** — Access to real-time lead flow when available
- **Lead Filtering** — Filter by vertical, geography, debt amount, recency
- **Budget Management** — Set daily/total spend caps

## Dependencies
- RevPie account with API access
- `REVPIE_API_KEY`, `REVPIE_USERNAME`, `REVPIE_PASSWORD` in `.env`

## Usage
```python
from skills.revpie import RevPieClient

rp = RevPieClient()

# Search available leads
leads = rp.search_leads(
    vertical="debt_relief",
    states=["CA", "TX", "FL"],
    min_debt=10000,
    max_age_days=60,
    limit=20
)

# Purchase a batch
order = rp.purchase(lead_ids=[l.id for l in leads], budget_cap=500.00)
```

## Used By
- **Scout** — Supplementary lead sourcing (alongside form filling)
- **Hawk** — Budget allocation decisions for RevPie channel
