# 🛠️ Project Ocean — Setup Guide

This guide walks you through setting up Project Ocean from scratch. No coding experience needed.

---

## Step 1: Install OpenClaw

1. Go to [openclaw.com](https://openclaw.com) and download for your OS
2. Follow the installation instructions
3. Verify it works:
   ```bash
   openclaw gateway status
   ```
   You should see "Gateway is running" or similar

## Step 2: Clone This Repo

```bash
cd ~
git clone https://github.com/ak-eyther/project-ocean.git
cd project-ocean
```

## Step 3: Set Up Credentials

```bash
cp .env.example .env
```

Open `.env` in any text editor (TextEdit, VS Code, nano) and fill in each key. See `config/credentials.md` for a checklist of what you need.

**Priority order** (get these first):
1. ✅ OpenRouter API key — needed for all agents to work
2. ✅ Supabase URL + keys — needed for database
3. ✅ Proxy credentials — needed for stealth browser
4. ⬜ Everything else can be added as you activate each feature

## Step 4: Set Up Database

1. Go to [supabase.com](https://supabase.com) and create a free project
2. Go to **SQL Editor** in the dashboard
3. Copy the contents of `db/schema.sql` and paste it in the editor
4. Click **Run** — this creates all the tables
5. (Optional) Run `db/seed.sql` to add test data
6. Copy your project URL and keys from **Settings → API** into `.env`

## Step 5: Configure OpenClaw

Copy the Ocean config into your OpenClaw workspace:
```bash
cp config/openclaw.yaml ~/.openclaw/config.yaml
```

Edit the config to point to your `.env` file location if needed.

## Step 6: Start the Agents

```bash
openclaw gateway start
```

The 6 agents will initialize:
- **Fury** — starts first, orchestrates everything
- **Scout** — begins monitoring for lead opportunities
- **Shield** — stands by for compliance checks
- **Hawk** — connects to ad platforms
- **Signal** — readies delivery channels
- **Watchtower** — begins system monitoring

## Step 7: Verify Everything Works

Check agent status:
```bash
openclaw gateway status
```

You should see all 6 agents listed as active.

## Step 8: Load Test Data (Optional)

Run the seed file to populate test leads and buyers:
- Go to Supabase SQL Editor
- Paste and run `db/seed.sql`
- Fury should pick up the test data in the next standup cycle

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Gateway not running" | Run `openclaw gateway start` |
| Agent not responding | Check `.env` has the right API keys |
| Database errors | Make sure you ran `db/schema.sql` first |
| Proxy errors | Verify proxy credentials in `.env` |
| High AI costs | Check Watchtower logs — may be a runaway loop |

## Getting Help

- Check `docs/RUNBOOK.md` for common operations
- Review agent logs in the OpenClaw dashboard
- Watchtower will alert you if something breaks
