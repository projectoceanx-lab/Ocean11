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

### 6. Residential Proxy Support

The script supports IPRoyal residential proxies for US-geolocated sessions, gated behind the `PROXY_URL` env var:

```python
proxy_url = os.environ.get("PROXY_URL")
if proxy_url:
    launch_args["proxy"] = {
        "server": f"http://{os.environ.get('PROXY_HOST', 'geo.iproyal.com')}:{os.environ.get('PROXY_PORT', '12321')}",
        "username": os.environ.get("PROXY_USER", ""),
        "password": os.environ.get("PROXY_PASS", ""),
    }
```

**Env vars:** `PROXY_URL` (enable flag), `PROXY_HOST` (default `geo.iproyal.com`), `PROXY_PORT` (default `12321`), `PROXY_USER`, `PROXY_PASS`. Each browser session gets a fresh IP via IPRoyal's per-session rotation. Without `PROXY_URL` set, the script connects directly.

### 7. Custom User Agent

To avoid headless detection by TrustedForm/Datadog, the browser context uses a hardcoded Chrome 131 macOS user agent string instead of Playwright's default:

```python
context = await browser.new_context(
    viewport={"width": 1280, "height": 900},
    user_agent=(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
)
```

This is set at context creation alongside stealth patching, so every page within the session carries the same fingerprint.

### 8. Submit Button Disabled Polling

FDR's React form disables the submit button until all client-side validations pass. The script polls `is_disabled()` up to 20 times (500ms intervals = 10s max) before attempting the click:

```python
for _ in range(20):
    disabled = await submit_btn.is_disabled()
    if not disabled:
        break
    await page.wait_for_timeout(500)
else:
    print("[!] Submit button still disabled after 10s — attempting anyway")
```

If the button is still disabled after 10s, the script clicks anyway — sometimes the disabled state is a CSS artifact rather than a real React guard.

### 9. Success Detection Heuristics

After clicking submit, the script can't rely on a single success signal. It checks multiple heuristics:

**NDR** (`fdr-ndr-fill.py:430-435`):
```python
success = (
    "thank" in content.lower()
    or "results" in current_url.lower()
    or "confirmation" in content.lower()
    or "details" not in current_url  # navigated away from /details = likely success
)
```

**FDR** (`fdr-ndr-fill.py:611-616`):
```python
success = (
    "thank" in content.lower()
    or "results" in current_url.lower()
    or "confirmation" in content.lower()
    or "contact-info" not in current_url  # navigated away = likely success
)
```

The last check in each is form-specific: NDR checks if the URL left `/details`, FDR checks if it left `/contact-info`. A screenshot is always saved regardless of the heuristic result.

### 10. Dry-Run Mode

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

## Known Issues

- **Stale comment in `log_submission()`** (`fdr-ndr-fill.py:162`): The docstring says `lead_id is NOT NULL in the DB schema`, but `lead_id` was made nullable in the [offer submissions migration](../database-issues/offer-submissions-lead-id-nullable.md). The comment is outdated — the function's logic (skip DB insert when `lead_id is None`) is correct, but the comment should reference the nullable schema.

## Related

- [Everflow Postback Pipeline Setup](./everflow-postback-pipeline-setup.md) — the infrastructure that tracks conversions from these form fills
- [Offer Submissions lead_id Nullable](../database-issues/offer-submissions-lead-id-nullable.md) — allows test fills without lead records
- `docs/NDR_FORM_MAP.md` — NDR form field ID reference
