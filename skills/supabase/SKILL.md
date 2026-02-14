# Supabase Skill

PostgreSQL database access via Supabase for all CRUD operations and analytics queries.

## Capabilities
- **Lead CRUD** — Insert, update, query, and deduplicate leads
- **Buyer Management** — Query buyer availability, update caps, track payouts
- **P&L Queries** — Daily/weekly/monthly profit and loss aggregation
- **Campaign Tracking** — Update spend, lead counts, CPL calculations
- **Compliance Logging** — Write audit trail entries
- **Agent Activity** — Log all agent actions for observability

## Dependencies
- Supabase project (free tier works for Phase 1)
- `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` in `.env`

## Usage
```python
from skills.supabase import SupabaseClient

db = SupabaseClient()

# Insert a lead
db.insert("leads", {
    "source": "fb",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "debt_amount": 25000,
    "status": "new"
})

# Check for duplicates
exists = db.query("leads", filters={"email": "john@example.com"})

# Get today's P&L
pnl = db.query("pnl_daily", filters={"date": "2026-02-14"})

# Get available buyers
buyers = db.query("buyers", filters={
    "status": "active",
    "current_daily_count.lt": "daily_cap"
})
```

## Used By
- **All agents** — Central data store
