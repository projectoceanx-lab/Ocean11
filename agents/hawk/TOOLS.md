# TOOLS.md — Hawk

## Active Tools
- **Facebook Ads:** Old account exists (pending access token)
- **Everflow:** RevvMind account (pending API key)
- **RevPie:** Aged account (pending API key)
- **Database:** Supabase (pending setup)

## Budget Guardrails
- Max 20% budget shift without Captain approval
- Kill campaigns with CPL > $30 after 100 clicks
- Daily budget cap per campaign: start $50-100

## Memory Vault
- **Search:** `python3 scripts/memory-search.py "query" --agent hawk --limit 5`
- Write observations after campaign changes, CPL shifts, A/B test results

## Notes
- Facebook debt relief ads require Special Ad Category: Credit
