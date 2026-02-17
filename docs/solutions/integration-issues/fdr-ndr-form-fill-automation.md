---
title: "FDR/NDR Form Fill Automation"
date: 2026-02-17
tags: [playwright, stealth, form-automation, bot-detection, fdr, ndr]
category: integration-issues
severity: high
status: resolved
related_files:
  - scripts/fdr-ndr-fill.py
  - config/everflow_urls.json
  - docs/NDR_FORM_MAP.md
---

# FDR/NDR Form Fill Automation

## Problem

Automated form filling for Freedom Debt Relief (FDR) and National Debt Relief (NDR) debt relief forms was blocked by bot detection. Pages showed blank content or the forms refused to load when accessed via Playwright's default browser context. Without working form fills, the entire lead delivery pipeline was dead.

## Investigation

Inspected the buyer forms and found heavy anti-bot infrastructure:

- **TrustedForm** — Certification scripts that fingerprint browser behavior
- **Datadog RUM** — Real User Monitoring that detects automation patterns
- **Hotjar** — Session recording and heatmap tracking
- **118+ tracking scripts** — Various analytics, pixels, and monitoring tags

Key detection vectors:
1. `navigator.webdriver` returning `true` (Playwright default)
2. Missing `chrome.runtime` object (headless Chrome fingerprint)
3. Missing `window.chrome` properties
4. Unusual plugin/language patterns

## Root Cause

Playwright's default Chromium context exposes multiple automation signals that TrustedForm and Datadog RUM detect. The forms either render blank or silently reject submissions from detected bots.

## Solution

### 1. Stealth Patching (`playwright-stealth`)

Added `playwright-stealth` to patch automation signals before page load:

```python
from playwright_stealth import Stealth
s = Stealth()
await s.apply_stealth_async(page)
```

This patches `navigator.webdriver`, `chrome.runtime`, `window.chrome`, and other fingerprinting surfaces. Applied early in the browser context setup, before any navigation.

### 2. Robust Field Targeting

Both FDR and NDR forms use React/MUI components with dynamic class names. Selectors that work today may break tomorrow. Solution: multiple CSS selector fallbacks per field.

**NDR contact fields:**
```python
# Primary: form field names → Fallback: placeholder text
fn_input = page.locator("input[name='input_3'], input#input_274_3").first
# If those fail:
fn_input = page.locator("input[placeholder*='First']").first
```

**FDR state selection** — custom MUI combobox, not a native `<select>`:
```python
combo_input = page.locator(
    "input[role='combobox'], "
    "input[aria-autocomplete='list'], "
    "input[placeholder*='state' i]"
).first
```

**FDR debt slider** — MUI Slider with hidden `<input type="range">`:
```python
# Try native interaction first
await slider_input.fill(str(debt_amount))
# Fallback: JS setter to bypass React's synthetic event system
await page.evaluate("""...""")
```

### 3. Human-Like Delays

Bot detection correlates action timing. The script injects randomized delays:

- **Between actions:** `0.4–1.2s` (randomized via `random.uniform`)
- **Keystroke delay:** `60ms` per character for phone numbers (typed, not filled)
- **Post-navigation settle:** `2000ms` after page loads
- **Post-tab validation:** `1500ms` after tabbing out of last field

```python
async def human_delay(lo=0.4, hi=1.2):
    await asyncio.sleep(random.uniform(lo, hi))
```

### 4. Everflow Redirect Chain Handling

When entering via Everflow tracking URLs, the browser follows a redirect chain:
`zkds923.com → shhefm9trk.com → buyer form`

This chain includes 302 redirects and potentially a tracking pixel (204 response) instead of a redirect. The script handles both cases:

```python
# Navigate with lenient timeout (redirect chains cause ERR_ABORTED)
await page.goto(entry_url, wait_until="commit", timeout=45000)

# Poll for landing on buyer domain
for attempt in range(20):
    await page.wait_for_timeout(1000)
    if any(domain in current.lower() for domain in ["nationaldebtrelief", "freedomdebtrelief"]):
        break

# Fallback: if tracking pixel fired but didn't redirect, navigate directly
if page.url == "about:blank" or "shhefm9trk" in page.url:
    await page.goto(direct_url, wait_until="domcontentloaded")
```

The script also auto-detects which offer type it landed on (NDR redirects sometimes land on FDR's domain) and adjusts the form-fill flow accordingly.

### 5. NDR En-Dash Support

NDR's debt amount dropdown labels use en-dashes (`–`, U+2013) not hyphens (`-`, U+002D):

```python
NDR_DEBT_RANGES = [
    (0, 4999, "$0 \u2013 $4,999"),      # en-dash, not hyphen
    (5000, 7499, "$5,000 \u2013 $7,499"),
    # ...
]
```

The script tries the en-dash label first, falls back to hyphen:
```python
try:
    await select.select_option(label=label)
except Exception:
    alt_label = label.replace("\u2013", "-")
    await select.select_option(label=alt_label)
```

### 6. Dry-Run Mode

`--dry-run` fills the entire form but stops before clicking submit. Takes a full-page screenshot for validation:

```bash
python3 scripts/fdr-ndr-fill.py --offer ndr --offer-id 4905 --dry-run
```

Screenshots saved to `tmp/ndr-dryrun-<timestamp>.png`.

### Form Flow Summary

**FDR (3 steps):**
1. Debt amount slider → Continue
2. State combobox (MUI autocomplete) → Next
3. Contact info (first, last, phone, email) → Submit

**NDR (2 steps):**
1. Debt amount dropdown (`<select>`) → "See if You Qualify"
2. Contact info (first, last, email, phone) → "See My Relief Options"

## Prevention

- Field selectors use 3+ fallback strategies (name, id, placeholder, role)
- Human-like delays are randomized, not fixed — harder to fingerprint
- Stealth patching is applied once at context creation, before any navigation
- Dry-run mode allows validating form changes without wasting offer caps
- Error screenshots are auto-captured to `tmp/` for debugging failed fills

## Related

- [Everflow Postback Pipeline Setup](./everflow-postback-pipeline-setup.md) — the infrastructure that tracks conversions from these form fills
- [Offer Submissions lead_id Nullable](../database-issues/offer-submissions-lead-id-nullable.md) — allows test fills without lead records
- `docs/NDR_FORM_MAP.md` — NDR form field ID reference
