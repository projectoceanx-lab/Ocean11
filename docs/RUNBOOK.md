# Runbook — Operations Guide

## Starting the System

### Full Start
```bash
# 1. Start OpenClaw gateway
openclaw gateway start

# 2. Verify all agents are running
openclaw gateway status
```

All 6 agents should show as active. Fury initializes first and confirms the others.

### Start a Single Agent
If an agent crashed or needs restart:
```bash
# Restart specific agent session
openclaw gateway restart
# Then check the agent's heartbeat
```

## Stopping the System

### Graceful Shutdown
```bash
openclaw gateway stop
```

### Emergency Stop
If something is burning money (runaway AI calls, etc.):
```bash
openclaw gateway stop
# Then check .env and fix the issue before restarting
```

## Daily Operations

### Morning Checklist (Fury handles this, but verify manually if needed)
1. Check P&L from yesterday: `SELECT * FROM pnl_daily ORDER BY date DESC LIMIT 1;`
2. Check lead pipeline: `SELECT status, COUNT(*) FROM leads GROUP BY status;`
3. Check buyer caps reset: `SELECT name, current_daily_count, daily_cap FROM buyers;`
4. Check compliance: `SELECT result, COUNT(*) FROM compliance_log WHERE checked_at > NOW() - INTERVAL '24h' GROUP BY result;`

### Weekly
1. Review total P&L: `SELECT SUM(revenue), SUM(gross_profit) FROM pnl_daily WHERE date > NOW() - INTERVAL '7 days';`
2. Review buyer return rates
3. Review campaign CPL trends
4. Check AI cost burn rate

## Common Issues

### Agent Not Responding
**Symptom:** Agent's heartbeat shows as stale in Watchtower
**Fix:**
1. Check OpenClaw gateway status
2. Verify API keys in `.env` are valid
3. Check the agent's model is available on OpenRouter
4. Restart the gateway

### High AI Costs
**Symptom:** Watchtower alerts on cost > $15/day
**Fix:**
1. Check `agent_activity` for unusual volume: `SELECT agent_name, COUNT(*) FROM agent_activity WHERE created_at > NOW() - INTERVAL '1h' GROUP BY agent_name;`
2. Look for infinite loops (agent calling itself repeatedly)
3. Pause the offending agent
4. Check if a model switched to a more expensive one

### Leads Not Delivering
**Symptom:** Scored leads piling up, no deliveries
**Fix:**
1. Check Signal is running
2. Check buyers have available cap: `SELECT name, current_daily_count, daily_cap FROM buyers WHERE status = 'active';`
3. Check Shield isn't blocking everything: `SELECT result, COUNT(*) FROM compliance_log WHERE checked_at > NOW() - INTERVAL '24h' GROUP BY result;`
4. Verify Ringba / email engine connections

### Compliance Block Rate > 20%
**Symptom:** Shield is blocking too many leads
**Fix:**
1. Review recent blocks: `SELECT cl.reason, COUNT(*) FROM compliance_log cl WHERE cl.result = 'block' AND cl.checked_at > NOW() - INTERVAL '24h' GROUP BY cl.reason ORDER BY COUNT(*) DESC;`
2. Identify the pattern (bad source? state issue? data quality?)
3. Fix upstream — talk to Scout about lead quality
4. If it's a legitimate compliance issue, that's working as intended

### Database Approaching Limits
**Symptom:** Watchtower alerts on row count > 8K (Supabase free tier)
**Fix:**
1. Archive old delivered/rejected leads
2. Clean up agent_activity (keep last 30 days)
3. Consider upgrading to Supabase Pro ($25/mo)

## Escalation

| Severity | Who Handles | Action |
|----------|------------|--------|
| Low | Watchtower auto-resolves | Log and monitor |
| Medium | Fury adjusts strategy | Alert Arif if persists > 24h |
| High | Fury + Arif | Immediate notification |
| Critical | System pause | Stop gateway, notify Arif, investigate |

## Useful SQL Queries

```sql
-- Today's P&L snapshot
SELECT * FROM pnl_daily WHERE date = CURRENT_DATE;

-- Lead quality distribution (last 7 days)
SELECT quality_tier, COUNT(*), AVG(quality_score)
FROM leads WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY quality_tier ORDER BY quality_tier;

-- Buyer performance
SELECT b.name, COUNT(d.id) as delivered, 
       SUM(CASE WHEN d.status = 'accepted' THEN 1 ELSE 0 END) as accepted,
       SUM(d.payout) as total_revenue
FROM buyers b LEFT JOIN deliveries d ON b.id = d.buyer_id
GROUP BY b.name;

-- AI cost trend (last 7 days)
SELECT date, cost_ai FROM pnl_daily ORDER BY date DESC LIMIT 7;

-- Agent activity volume (last 24h)
SELECT agent_name, action, COUNT(*)
FROM agent_activity WHERE created_at > NOW() - INTERVAL '24h'
GROUP BY agent_name, action ORDER BY agent_name, COUNT(*) DESC;
```
