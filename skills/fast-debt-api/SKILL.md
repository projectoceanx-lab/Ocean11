# Fast Debt API Skill

Lead enrichment service for verifying and enhancing debt relief lead data.

## Capabilities
- **Income Verification** — Verify reported income range against data sources
- **Employment Check** — Confirm employment status and employer
- **Debt Verification** — Cross-reference reported debt amounts and types
- **Credit Indicators** — Soft credit data points (no hard pull)
- **Contact Validation** — Phone line type (mobile/landline), email deliverability

## Dependencies
- Fast Debt API account
- `FAST_DEBT_API_KEY`, `FAST_DEBT_BASE_URL` in `.env`

## Usage
```python
from skills.fast_debt_api import FastDebtClient

fda = FastDebtClient()

# Enrich a lead
enrichment = fda.enrich(
    first_name="Alice",
    last_name="Williams",
    email="alice.w@example.com",
    phone="+15551001",
    state="CA",
    zip="90210"
)

# Returns:
# {
#   "income_verified": true,
#   "income_range": "50k-75k",
#   "employment_status": "employed",
#   "employer": "Acme Corp",
#   "debt_indicators": {"credit_card": 22000, "total": 25000},
#   "phone_type": "mobile",
#   "email_valid": true,
#   "confidence_score": 87
# }
```

## Cost
- ~$0.10-0.50 per enrichment call (volume dependent)
- Budget: ~$50/month at 10 leads/day

## Used By
- **Scout** — Lead enrichment after initial acquisition
