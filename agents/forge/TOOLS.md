# TOOLS.md — Signal

## Active Tools
- **Database:** Supabase (pending setup)
- **Call Routing:** Ringba (pending setup)
- **Email Engine:** SendGrid/Mailgun (pending — warmed ESPs from Zappian available)
- **Tracking:** Everflow (pending API key)

## Email Assets
- Warmed domains from Zappian (existing)
- Templates in templates/email-sequences/

## Memory Vault
- **Search:** `python3 scripts/memory-search.py "query" --agent signal --limit 5`
- Write observations after delivery issues, buyer behavior changes, acceptance rate shifts

## Google Services (gog CLI)
- `gog` CLI available for Google Sheets — useful for buyer tracking spreadsheets
- Example: `gog sheets read "Buyer Tracker"`

## Notes
- Never deliver a lead that hasn't passed Shield compliance
- Track return rates per buyer — flag if > 15%
