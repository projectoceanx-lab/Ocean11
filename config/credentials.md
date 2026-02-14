# Credentials Checklist — Project Ocean

Track what's been provided and what's still pending.

## Core Infrastructure
- [ ] **OpenRouter API key** — routes to Kimi, DeepSeek, GLM, Qwen, GPT-5-nano
- [ ] **Anthropic API key** — fallback for complex tasks
- [ ] **Supabase URL + anon key + service role key** — central database
- [ ] **LangSmith API key** — agent observability (Phase 1)
- [ ] **xAI/Grok API key** — X/Twitter monitoring

## Lead Acquisition
- [ ] **Residential proxy provider** — credentials + API (for stealth browser)
- [ ] **Fast Debt API key** — lead enrichment (income, employment, debt verification)
- [ ] **Domain list** — for landing pages + email warming

## Traffic & Spend
- [ ] **Everflow API key + account ID** — offer tracking, conversion postbacks
- [ ] **RevPie login + API key** — aged leads, traffic source
- [ ] **Facebook Ads app ID + access token** — media buying

## Delivery
- [ ] **Ringba account + API key** — call routing & tracking
- [ ] **ESP API keys** — SendGrid/Mailgun/custom (email sends)
- [ ] **Salesforce credentials** — if reusing warmed ESPs from Zappian

## Accounts
- [ ] **Gmail account** — Ocean's own (separate from personal)
- [ ] **GitHub repo** — created under Ocean's GitHub account

## Notes
- Each credential goes in `.env` (never committed to git)
- Captain tracks spend credentials, Shield audits access
- Watchtower monitors API health/rate limits
