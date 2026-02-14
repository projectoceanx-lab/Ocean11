# Stealth Browser Skill

Anti-detection browser automation using Camoufox for form filling and web scraping.

## Capabilities
- **Form Detection** — Identify and map debt relief lead forms on target sites
- **Form Filling** — Automated, human-like form submission with realistic typing delays
- **Anti-Detection** — Camoufox browser fingerprint randomization, canvas/WebGL spoofing
- **Proxy Rotation** — Residential proxy integration (Smartproxy/Bright Data/IPRoyal)
- **Session Management** — Persistent browser profiles, cookie handling
- **Screenshot Capture** — Evidence capture for compliance audit trail

## Dependencies
- `camoufox` — Anti-detection Firefox fork
- Residential proxy provider credentials (see `.env`)

## Usage
```python
# Scout uses this skill for lead acquisition
from skills.stealth_browser import StealthBrowser

browser = StealthBrowser(proxy=env.PROXY_HOST)
browser.navigate("https://example-debt-form.com")
browser.fill_form({
    "first_name": lead.first_name,
    "last_name": lead.last_name,
    "email": lead.email,
    "phone": lead.phone,
    "debt_amount": lead.debt_amount
})
browser.submit()
```

## Configuration
```yaml
proxy:
  host: ${PROXY_HOST}
  port: ${PROXY_PORT}
  username: ${PROXY_USERNAME}
  password: ${PROXY_PASSWORD}
  rotation: per_request    # or per_session
  
browser:
  headless: true
  typing_delay_ms: 50-150  # Randomized human-like delay
  page_load_timeout: 30
  max_retries: 3
```

## Used By
- **Scout** — Primary user for lead acquisition forms

## Notes
- Rotate proxies every 5-10 requests minimum
- Never reuse the same fingerprint on the same domain within 24h
- Log all form submission attempts (success/failure) to agent_activity
