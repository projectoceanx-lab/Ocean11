# NDR Form Map — National Debt Relief Application

**URL:** https://start.nationaldebtrelief.com/apply  
**Mapped:** 2026-02-17 (revalidated live 2026-02-18)  
**Status:** ✅ Revised — 3-step flow confirmed; network-level test-safe submit guard implemented

---

## 1. Form Flow Overview

The NDR application is a **3-step funnel**:

| Step | URL | Page Title |
|------|-----|------------|
| **Step 1** | `/apply` | "Get Debt Relief" — Debt amount selector |
| **Step 2** | `/details?debtAmountLow=X&debtAmountHigh=Y&sourcePage=apply` | "Take The Next Steps Toward Financial Stability" — Contact info |
| **Step 3** | `/personalizesavings?ndrUID=...&prospectId=...` | "Do You Qualify for Debt Relief?" — Address + DOB soft-pull step |

**Observed submit behavior (live, 2026-02-18):**
- Step 2 submits via `POST /details?...` (HTTP 200)
- Then client redirects to `/personalizesavings` with `ndrUID`, `prospectId`, debt range params
- Session storage persists `userData`, `prospectId`, and `redirectParams`

---

## 2. Step-by-Step Field Schema

### Step 1: Debt Amount Selection (`/apply`)

| Field | Element | Name | Type | Required | Options |
|-------|---------|------|------|----------|---------|
| Debt Amount | `<select>` | (dropdown) | combobox | Yes | See below |

**Debt Amount Options (value → label):**
- `$100,000+`
- `$90,000 – $99,999`
- `$80,000 – $89,999`
- `$70,000 – $79,999`
- `$60,000 – $69,999`
- `$50,000 – $59,999`
- `$40,000 – $49,999`
- `$30,000 – $39,999`
- `$20,000 – $29,999`
- `$15,000 – $19,999`
- `$10,000 – $14,999`
- `$7,500 – $9,999`
- `$5,000 – $7,499`
- `$0 – $4,999`

**CTA Button:** "See if You Qualify" (labeled "Let's Go")

**Navigation:** Selecting an amount and clicking the button navigates to `/details` with query params:
- `debtAmountLow` (numeric, e.g., `20000`)
- `debtAmountHigh` (numeric, e.g., `29999`)
- `sourcePage=apply`

### Step 2: Contact Information (`/details`)

| Field | Input Name | DOM ID | Type | Required | Placeholder | Validation |
|-------|-----------|--------|------|----------|-------------|------------|
| First Name | `input_3` | `input_274_3` | text | ✅ Yes | "First Name" | Standard text |
| Last Name | `input_4` | `input_274_4` | text | ✅ Yes | "Last Name" | Standard text |
| Email | `input_8` | `input_274_8` | email | ✅ Yes | "Email" | HTML5 email validation |
| Phone Number | `input_76` | `phone` | text (inputMode=numeric) | ✅ Yes | "Phone Number" | Auto-formats while typing to `(XXX) XXX-XXXX` |

**CTA Button:** "See My Relief Options"

**Form Method (observed):** `POST` to `/details?...` followed by client-side redirect to Step 3.

**Consent Language:** By clicking submit, user agrees to auto-dialed/AI voicebot calls, SMS (max 2/day, 7/week), email marketing, Privacy Policy, and Terms (including arbitration). **This is TCPA consent language.**

### Step 3: Personalize Savings (`/personalizesavings`)

| Field | Element | Required | Placeholder | Notes |
|-------|---------|----------|-------------|-------|
| Address | text input | ✅ Yes | "Address" | Has "Enter it manually" fallback |
| Date of Birth | text input | ✅ Yes | "MM-DD-YYYY" | Soft credit-pull consent step |

**CTA Button:** "Submit"

**Key disclosure:** Step 3 explicitly requests authorization for a secure soft credit pull and states no credit-score impact.

---

## 3. Hidden Fields & Tracking Parameters

### Hidden Form Fields (Step 2)

| Name | ID | Purpose | Sample Value |
|------|-----|---------|-------------|
| `xxTrustedFormCertUrl` | `xxTrustedFormCertUrl_1` | TrustedForm certificate URL | `https://cert.trustedform.com/{hash}` |
| `xxTrustedFormToken` | `xxTrustedFormToken_1` | TrustedForm token (same as cert URL) | `https://cert.trustedform.com/{hash}` |
| `xxTrustedFormPingUrl` | `xxTrustedFormPingUrl_1` | TrustedForm ping URL | `https://ping.trustedform.com/{hash}` |

### URL Parameters Passed Between Steps

| Param | Example | Purpose |
|-------|---------|---------|
| `debtAmountLow` | `20000` | Lower bound of debt range |
| `debtAmountHigh` | `29999` | Upper bound of debt range |
| `sourcePage` | `apply` | Source page identifier |

### Cookies Set

| Cookie | Purpose |
|--------|---------|
| `visitorId` | Visitor tracking (e.g., `ecca21051771098844`) |
| `_gcl_au` | Google Ads click attribution |
| `_fbp` | Facebook Pixel |
| `_ga` | Google Analytics |
| `_axwrt` | Attribution tracking |
| `_evga_*` | Evergage/Salesforce personalization |
| `_sfid_*` | Salesforce anonymous ID |
| `attr_first` | First-touch attribution (source/medium/campaign) |
| `DD_SessionTraceID` | Datadog session tracing |
| `pscd` | Cross-domain tracking (`join.nationaldebtrelief.com`) |

---

## 4. Validation Rules

| Field | Validation |
|-------|-----------|
| Debt Amount | Must select non-default option (not "How Big Is Your Debt?") |
| First Name | Required, standard text (no pattern constraint in HTML) |
| Last Name | Required, standard text |
| Email | Required, HTML5 `type=email` validation |
| Phone | Required, `inputMode=numeric`; confirmed live auto-format to `(XXX) XXX-XXXX` |

**No CAPTCHA detected.** No reCAPTCHA, hCaptcha, or Cloudflare Turnstile observed across Steps 1-3.

---

## 5. Anti-Bot / Friction Points

### ⚠️ TrustedForm (ActiveProspect)
- **Script:** `cdn.trustedform.com/trustedform-1.11.4.js`
- **Impact:** Records mouse movements, keystrokes, scroll behavior, time-on-page. Generates a certificate URL proving genuine human interaction.
- **Risk Level:** 🔴 HIGH — This is the primary anti-bot defense. TrustedForm certificates are required by many lead buyers for TCPA compliance. Automated form fills without realistic human behavior will generate invalid/suspicious certificates.

### ⚠️ Datadog RUM (Real User Monitoring)
- **Detected:** `DD_RUM` present, `DD_SessionTraceID` cookie
- **Impact:** Tracks page load times, user interactions, JS errors. Can detect automation patterns (instant form fills, no mouse events, unusual timing).
- **Risk Level:** 🟡 MEDIUM

### 📊 Heavy Ad/Analytics Stack (118 scripts total)
- Google Tag Manager (`GTM-TWWRTTXL`)
- Google Ads (`AW-987901937`)
- Google Analytics 4 (`G-8P960Y0ZN7`)
- Facebook Pixel
- TikTok Pixel (`CKDF81BC77UE2IQFF4LG`)
- Bing UET (`4056672`)
- Taboola pixel
- Outbrain pixel
- AdRoll
- Hotjar (`182527`) — **session recording**
- Tomi.ai
- Segment CDP
- Salesforce/Evergage

### 🔒 No CAPTCHA
No reCAPTCHA, hCaptcha, or Turnstile detected on either step. This could change dynamically based on traffic patterns or bot scores.

---

## 6. Recommended Human-Simulation Actions for Automation

### Critical Requirements

1. **TrustedForm compliance is the #1 priority.** The bot MUST:
   - Generate realistic mouse movements (move to each field, hover, natural curves)
   - Type characters with variable delays (80-200ms per keystroke, occasional pauses)
   - Spend realistic time on each step (Step 1: 5-15s, Step 2: 20-45s)
   - Scroll the page naturally before/during interaction
   - Tab between fields OR click into each field (mix behaviors)

2. **Playwright setup:**
   - Use `stealth` plugin to avoid navigator/webdriver detection
   - Randomize viewport size within common ranges (1366x768, 1440x900, 1920x1080)
   - Set realistic User-Agent strings
   - Disable `navigator.webdriver` flag
   - Use residential proxies (US-based, rotating)

3. **Form fill sequence:**
   ```
   Step 1:
   1. Wait 2-5s after page load
   2. Scroll down slightly
   3. Move mouse to debt amount dropdown
   4. Click dropdown, wait 500-1000ms
   5. Select debt amount
   6. Move mouse to "Let's Go" button
   7. Wait 1-3s
   8. Click button
   
   Step 2:
   1. Wait 2-4s after page load
   2. Click into First Name field
   3. Type first name (variable speed)
   4. Tab or click to Last Name
   5. Type last name
   6. Tab or click to Email
   7. Type email
   8. Tab or click to Phone
   9. Type phone (watch for auto-formatting mask)
   10. Wait 2-5s (simulate reading consent text)
   11. Click "See My Relief Options"

   Step 3:
   1. Wait for `/personalizesavings` URL and heading
   2. If test-only run, STOP before entering Address/DOB unless explicitly approved
   3. For live delivery flow, fill Address and DOB with compliant handling
   4. Submit only when buyer-routing and compliance gates are green
   ```

4. **Phone number handling (confirmed):** Type digits only (`press_sequentially`-style). Client auto-formats and payload carries formatted value `(415) 555-0199`.

5. **Session continuity:** Ensure cookies persist between Step 1 → Step 2 and Step 2 → Step 3, especially `visitorId`, `DD_SessionTraceID`, and TrustedForm fields.

6. **TrustedForm certificate:** On submit path, `api.trustedform.com/certs` + snapshot/fingerprint/event calls fire. Capture `xxTrustedFormCertUrl` for consent proof.

7. **Test-safe interception (implemented):** `scripts/fdr-ndr-fill.py` now supports `--safe-submit-probe` (NDR-only), which hard-blocks network `POST /details?...` requests before prospect creation while still exercising submit flow.
   - Example: `python3 scripts/fdr-ndr-fill.py --offer ndr --safe-submit-probe --offer-id 4905`

---

## 7. Architecture Notes

- **Likely Next.js App Router stack.** `_rsc` requests observed during transition to `/personalizesavings`.
- **Hybrid flow:** URL navigation is multi-page, but submission and redirection logic is JS-managed.
- **Form IDs suggest Gravity Forms** or similar WordPress form builder (pattern: `input_274_3` = form 274, field 3).
- **Cross-domain:** References to `join.nationaldebtrelief.com` in cookies suggest multiple entry points.
- **Step 2 submit path:** `POST /details?...` then redirect to `/personalizesavings?...` with generated IDs.

---

## 8. Blockers & Open Questions

| Item | Status | Notes |
|------|--------|-------|
| Post-submission behavior | ✅ Confirmed | `POST /details?...` then redirect to `/personalizesavings?...` with `prospectId` and `ndrUID` |
| Phone mask behavior | ✅ Confirmed | Typing digits auto-formats to `(XXX) XXX-XXXX`; payload uses formatted value |
| Test-safe submit interception | ✅ Resolved | Use `--safe-submit-probe` in `scripts/fdr-ndr-fill.py` to block `POST /details` at the network layer |
| Rate limiting | ❓ Unknown | May have IP-based rate limits on submissions |
| Geographic restrictions | ❓ Unknown | "Not available in all states" — may reject certain state-based leads |
| Dynamic CAPTCHA | ❓ Unknown | May trigger CAPTCHA after N submissions from same IP |
| Jornaya/LeadID | ❌ Not detected | Only TrustedForm found — no Jornaya LeadiD token |
