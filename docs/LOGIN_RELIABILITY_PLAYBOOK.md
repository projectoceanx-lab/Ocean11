# LOGIN_RELIABILITY_PLAYBOOK.md — Everflow / RevPie / Facebook

Owner: Fury  
Ops Monitoring Owner: Vision  
Execution Owner: Peter (fallback)  
Status: ACTIVE

## Objective
Keep authenticated access reliable for critical media ops dashboards (Everflow, RevPie, Facebook Ads) with minimum downtime and clear recovery paths.

## 3-Layer Access Architecture

### Layer 1 (Primary): Chrome Relay Session (`profile=chrome`)
Use the OpenClaw Chrome extension relay on your real signed-in tab.

Why:
- Reuses existing trusted login + cookies
- Better with MFA and anti-bot systems
- Most stable for interactive dashboard work

Rule:
- Human performs initial auth
- Agent operates only after relay is attached and tab badge is ON

### Layer 2 (Backup): Dedicated Ops Browser Profile
Use isolated `profile=openclaw` for scripted tasks and non-sensitive navigation.

Why:
- Repeatable environment
- Easier diagnostics
- Lower personal account risk

### Layer 3 (Scale): API-first where available
Move repetitive checks/configs to APIs (Everflow/reporting, etc.) once credentials are available.

Why:
- Less UI brittleness
- Better audit trail
- Faster automation

## Pre-Flight Checklist (MANDATORY before media tasks)
1. Browser service up (`browser status`)
2. Target profile healthy (`chrome` relay preferred for login-sensitive actions)
3. Auth check: no login redirect on target platform
4. Required tab attached (for relay)
5. Evidence capture enabled (URL + screenshot target state)

If any check fails: STOP task and run recovery path.

## Recovery Matrix

### Failure: Relay not attached / no connected tab
- Ask AK to click OpenClaw Browser Relay toolbar button on the target tab (badge ON)
- Re-run pre-flight

### Failure: Browser control timeout / CDP error
- Restart browser profile (openclaw)
- Re-open target URL
- If still failing, switch to relay path or manual handoff

### Failure: Session expired / login page shown
- Human re-auth (AK)
- Agent resumes from checkpoint

### Failure: Platform blocks automation (captcha/challenge)
- Pause automation
- Human clears challenge
- Resume at next deterministic step

## Platform SOP

### Everflow
- Primary route: Chrome relay tab
- Validation endpoint after action: postback row visible in `/postbacks`
- Success evidence: row ID, status, method, URL screenshot

### RevPie
- Primary route: Chrome relay tab
- Critical actions: whitelist/blacklist, bid changes
- Success evidence: changed row + timestamp screenshot

### Facebook Ads
- Primary route: Chrome relay tab only
- No blind destructive actions without explicit approval
- Success evidence: campaign/ad set status + timestamp

## Vision Monitoring Rules
- Every 4h active-window check:
  - Browser profile health
  - Auth redirect detection for Everflow/RevPie/FB
  - Alert on unhealthy state immediately
- Daily summary:
  - Login health status by platform (Green/Yellow/Red)
  - Incidents + recoveries

## Non-Negotiables
- No password sharing in chat
- No marking tasks done without proof bundle:
  1) URL
  2) screenshot or visible UI row evidence
  3) key field verification
  4) timestamp
