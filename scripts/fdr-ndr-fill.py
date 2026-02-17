#!/usr/bin/env python3
"""
FDR / NDR Debt Relief Form Filler
Freedom Debt Relief & National Debt Relief share the same form.
NDR entry redirects to FDR's apply domain.

Flow:
  FDR: 3-step flow (debt slider -> state -> contact info)
  NDR: 2-step flow (debt dropdown -> contact info) then redirects to /personalizesavings

Usage:
    python3 scripts/fdr-ndr-fill.py --offer fdr --dry-run
    python3 scripts/fdr-ndr-fill.py --offer ndr --offer-id 4905
    python3 scripts/fdr-ndr-fill.py --offer ndr --safe-submit-probe --offer-id 4905
    python3 scripts/fdr-ndr-fill.py --offer fdr --lead-id <uuid> --offer-id 4930
    python3 scripts/fdr-ndr-fill.py --offer fdr --first-name John --last-name Doe \
        --email john@test.com --phone 5125550199 --state TX --debt-amount 25000

Requires: playwright, httpx, python-dotenv
"""
import argparse, asyncio, json, os, sys, time, random, uuid
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load .env early
from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

CHROMIUM_PATH = "/Users/arifkhan/Library/Caches/ms-playwright/chromium_headless_shell-1208"

FDR_URL = "https://www.freedomdebtrelief.com"
NDR_URL = "https://start.nationaldebtrelief.com/apply"

# Everflow tracking URLs — ALWAYS use these instead of direct buyer URLs
EVERFLOW_URLS_PATH = PROJECT_ROOT / "config" / "everflow_urls.json"

def load_everflow_url(offer_id: int | None) -> str | None:
    """Load the Everflow tracking URL for a given offer ID."""
    if not offer_id:
        return None
    try:
        with open(EVERFLOW_URLS_PATH) as f:
            urls = json.load(f)
        entry = urls.get(str(offer_id))
        if entry and entry.get("url"):
            return entry["url"]
        print(f"[!] No Everflow URL found for offer_id={offer_id}")
        return None
    except FileNotFoundError:
        print(f"[!] Everflow URLs file not found: {EVERFLOW_URLS_PATH}")
        return None

# State name → abbreviation mapping for the combobox
STATE_MAP = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
}

# NDR dropdown debt ranges (labels use en-dash per actual form)
NDR_DEBT_RANGES = [
    (0, 4999, "$0 – $4,999"),
    (5000, 7499, "$5,000 – $7,499"),
    (7500, 9999, "$7,500 – $9,999"),
    (10000, 14999, "$10,000 – $14,999"),
    (15000, 19999, "$15,000 – $19,999"),
    (20000, 29999, "$20,000 – $29,999"),
    (30000, 39999, "$30,000 – $39,999"),
    (40000, 49999, "$40,000 – $49,999"),
    (50000, 59999, "$50,000 – $59,999"),
    (60000, 69999, "$60,000 – $69,999"),
    (70000, 79999, "$70,000 – $79,999"),
    (80000, 89999, "$80,000 – $89,999"),
    (90000, 99999, "$90,000 – $99,999"),
    (100000, 999999, "$100,000+"),
]

TEST_LEAD = {
    "first_name": "John",
    "last_name": "TestLead",
    "email": "testlead.ocean@gmail.com",
    "phone": "5125550199",
    "state": "TX",
    "debt_amount": "25000",
}


def is_ndr_live_submit_request(method: str, url: str) -> bool:
    """True only for real NDR form submission calls (not page navigation GETs)."""
    if method.upper() != "POST":
        return False
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if "nationaldebtrelief.com" not in host:
        return False
    return parsed.path.rstrip("/") == "/details"


def should_block_live_submit_request(offer: str, method: str, url: str) -> bool:
    """Network guard matcher used by safe test mode."""
    if offer != "ndr":
        return False
    return is_ndr_live_submit_request(method, url)


def get_supabase_headers():
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    return url, headers


def load_lead_from_db(lead_id: str) -> dict:
    import httpx
    url, headers = get_supabase_headers()
    resp = httpx.get(
        f"{url}/rest/v1/leads?id=eq.{lead_id}&select=*",
        headers=headers,
    )
    resp.raise_for_status()
    rows = resp.json()
    if not rows:
        print(f"ERROR: No lead found with id={lead_id}")
        sys.exit(1)
    row = rows[0]
    form_data = row.get("form_data") or {}
    return {
        "first_name": row.get("first_name", ""),
        "last_name": row.get("last_name", ""),
        "email": row.get("email", ""),
        "phone": row.get("phone", ""),
        "state": form_data.get("state", row.get("state", "")),
        "debt_amount": str(row.get("debt_amount", "25000")),
    }


def check_offer_cap(offer_id: int) -> bool:
    """Call check_offer_cap RPC. Returns True if OK to proceed, False if capped."""
    import httpx
    url, headers = get_supabase_headers()
    try:
        resp = httpx.post(
            f"{url}/rest/v1/rpc/check_offer_cap",
            headers=headers,
            json={"p_offer_id": offer_id},
        )
        resp.raise_for_status()
        result = resp.json()
        # RPC returns [{can_submit: bool, reason: str, ...}]
        if isinstance(result, list) and result:
            return result[0].get("can_submit", True)
        if isinstance(result, dict):
            return result.get("can_submit", True)
        return True
    except Exception as e:
        print(f"[!] Cap check failed: {e} — proceeding cautiously")
        return True


def log_submission(offer_id: int, lead: dict, aff_click_id: str, success: bool, dry_run: bool, lead_id: str | None = None):
    """Log to offer_submissions table (matches offer_caps_schema.sql).

    NOTE: offer_submissions.lead_id is nullable (see db/migrations/).
    If no lead_id is provided (CLI-only / test runs), we skip the DB insert
    and just log locally. Production runs via the queue always have a lead_id.
    """
    import httpx
    url, headers = get_supabase_headers()
    headers["Prefer"] = "return=representation"

    if lead_id is None:
        print(f"[⚠] No lead_id — skipping DB log (CLI/test mode). offer_id={offer_id} click={aff_click_id}")
        return

    row = {
        "offer_id": offer_id,
        "lead_id": lead_id,
        "everflow_click_id": aff_click_id,
        "status": "submitted",
    }
    try:
        resp = httpx.post(f"{url}/rest/v1/offer_submissions", headers=headers, json=row)
        resp.raise_for_status()
        stored = resp.json()
        print(f"[✓] Submission logged: {stored[0]['id'] if stored else 'ok'}")
    except Exception as e:
        print(f"[✗] Failed to log submission: {e}")


def pick_ndr_debt_label(amount: int) -> str:
    """Find the NDR dropdown option text that matches the debt amount."""
    for low, high, label in NDR_DEBT_RANGES:
        if low <= amount <= high:
            return label
    if amount >= 100000:
        return "$100,000+"
    return "$20,000 – $29,999"  # fallback


def state_abbr_to_name(abbr: str) -> str:
    return STATE_MAP.get(abbr.upper(), abbr)


async def human_delay(lo=0.4, hi=1.2):
    await asyncio.sleep(random.uniform(lo, hi))


async def fill_form(lead: dict, offer: str, dry_run: bool, offer_id: int | None,
                    headless: bool = True, safe_submit_probe: bool = False):
    from playwright.async_api import async_playwright

    if safe_submit_probe and dry_run:
        print("[✗] --safe-submit-probe cannot be combined with --dry-run.")
        return False

    if safe_submit_probe and offer != "ndr":
        print("[✗] --safe-submit-probe currently supports --offer ndr only.")
        return False

    aff_click_id = str(uuid.uuid4())
    debt_amount = int(lead["debt_amount"].replace(",", "").replace("$", ""))
    state_name = state_abbr_to_name(lead["state"])

    # CRITICAL: Use Everflow tracking URL so clicks are attributed to us
    everflow_url = load_everflow_url(offer_id)
    if everflow_url:
        entry_url = everflow_url
        print(f"[*] Entry via EVERFLOW: {entry_url}")
    else:
        # Fallback to direct URL only if no offer_id provided (local testing only)
        entry_url = NDR_URL if offer == "ndr" else FDR_URL
        print(f"[⚠] WARNING: No Everflow URL — using DIRECT entry (clicks NOT tracked!)")
        print(f"[⚠] Pass --offer-id to use Everflow tracking. Direct URL: {entry_url}")
    print(f"[*] Lead: {lead['first_name']} {lead['last_name']}, ${debt_amount}, {lead['state']}")
    print(f"[*] aff_click_id: {aff_click_id}")
    mode = "DRY RUN" if dry_run else ("SAFE SUBMIT PROBE" if safe_submit_probe else "SUBMIT")
    print(f"[*] Mode: {mode}")

    # Cap check
    if offer_id and not dry_run and not safe_submit_probe:
        if not check_offer_cap(offer_id):
            print("[✗] Offer cap reached — aborting.")
            return False

    async with async_playwright() as p:
        launch_args = {"headless": headless}
        # Let Playwright find its own installed chromium
        # IPRoyal residential proxy (US) — rotates per session
        proxy_url = os.environ.get("PROXY_URL")
        if proxy_url:
            launch_args["proxy"] = {
                "server": f"http://{os.environ.get('PROXY_HOST', 'geo.iproyal.com')}:{os.environ.get('PROXY_PORT', '12321')}",
                "username": os.environ.get("PROXY_USER", ""),
                "password": os.environ.get("PROXY_PASS", ""),
            }
            print(f"[*] Using proxy: {os.environ.get('PROXY_HOST', 'geo.iproyal.com')}")

        browser = await p.chromium.launch(**launch_args)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            ),
        )
        page = await context.new_page()
        blocked_requests: list[dict[str, str]] = []

        async def safe_submit_route(route):
            request = route.request
            if safe_submit_probe and should_block_live_submit_request(offer, request.method, request.url):
                blocked_requests.append(
                    {
                        "method": request.method,
                        "url": request.url,
                        "blocked_at": datetime.now(timezone.utc).isoformat(),
                    }
                )
                print(f"[SAFE] Blocked live submit: {request.method} {request.url}")
                await route.abort("blockedbyclient")
                return
            await route.continue_()

        if safe_submit_probe:
            await page.route("**/*", safe_submit_route)
            print("[*] Safe submit probe armed: network-level submit blocking is active.")

        # Stealth: patch navigator.webdriver, chrome.runtime, etc.
        try:
            from playwright_stealth import Stealth
            s = Stealth()
            await s.apply_stealth_async(page)
            print("[*] Stealth mode: ON")
        except Exception as e:
            print(f"[!] Stealth setup failed ({e}), running without stealth")

        try:
            # ── Navigate (via Everflow redirect if applicable) ──
            print(f"[*] Navigating to: {entry_url}")

            if everflow_url:
                # Everflow redirect chain involves multiple 302s + a final tracking pixel
                # that may use JS redirect. Strategy: navigate and keep retrying until
                # we land on the buyer's actual page.
                try:
                    await page.goto(entry_url, wait_until="commit", timeout=45000)
                except Exception:
                    pass  # ERR_ABORTED is expected during redirect chains

                # Wait for the page to settle on the final destination
                print("[*] Following Everflow redirect chain...")
                for attempt in range(20):
                    await page.wait_for_timeout(1000)
                    current = page.url
                    # Check if we've landed on the buyer's page
                    if any(domain in current.lower() for domain in [
                        "nationaldebtrelief", "freedomdebtrelief", "apply",
                    ]):
                        break
                    # If page has content, check for JS redirects
                    if current != "about:blank" and "zkds923" not in current:
                        try:
                            content = await page.content()
                            if len(content) > 500:  # Substantial page loaded
                                break
                        except Exception:
                            pass

                print(f"[*] Landed on: {page.url}")
                await page.wait_for_timeout(2000)

                # If we're still stuck, the tracking pixel (204) didn't redirect.
                # This means the offer's tracking is set up to fire a pixel, not redirect.
                # In that case, we need to visit the direct buyer URL but AFTER the
                # Everflow click was registered (which it was via the 302 chain).
                if page.url == "about:blank" or "shhefm9trk" in page.url:
                    direct_url = NDR_URL if offer == "ndr" else FDR_URL
                    print(f"[*] Tracking pixel fired (click registered). Navigating to buyer: {direct_url}")
                    await page.goto(direct_url, wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(2000)

                # Detect which form we actually landed on
                landed_url = page.url.lower()
                if "nationaldebtrelief" in landed_url or "start.national" in landed_url:
                    detected_offer = "ndr"
                elif "freedomdebtrelief" in landed_url:
                    detected_offer = "fdr"
                else:
                    detected_offer = offer
                    print(f"[!] Unknown landing domain: {page.url} — using --offer={offer}")

                if detected_offer != offer:
                    print(f"[*] Auto-detected offer type: {detected_offer} (overriding --offer={offer})")
                    offer = detected_offer

                if safe_submit_probe and offer != "ndr":
                    print(f"[✗] Safe submit probe requires NDR landing, got '{offer}'. Aborting.")
                    await browser.close()
                    return False
            else:
                await page.goto(entry_url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(2000)

            # ── STEP 1: Debt Amount ──
            print("[1/3] Debt Amount")

            if offer == "ndr":
                # NDR: 2-step flow — select debt dropdown, then contact info on /details
                label = pick_ndr_debt_label(debt_amount)
                print(f"  NDR dropdown: selecting '{label}'")
                select = page.locator("select").first
                await select.wait_for(timeout=10000)
                # Try by label first, fall back to matching by text content
                try:
                    await select.select_option(label=label)
                except Exception:
                    # Try with hyphen instead of en-dash
                    alt_label = label.replace("–", "-")
                    await select.select_option(label=alt_label)
                await human_delay()
                # Click CTA — could be "See if You Qualify" or "Let's Go"
                cta = page.get_by_role("button", name="See if You Qualify").or_(
                    page.get_by_role("link", name="See if You Qualify")
                ).or_(
                    page.get_by_role("button", name="Let's Go")
                ).or_(
                    page.locator("button[type='submit'], a.cta-button, input[type='submit']")
                )
                await cta.first.click(timeout=10000)
                print("  → Moving to contact info (Step 2)...")
                # NDR goes to /details with query params — NOT to FDR
                await page.wait_for_url("**/details**", timeout=30000)
                await page.wait_for_timeout(2000)

                # ── NDR STEP 2: Contact Info (no state step) ──
                print("[2/2] Contact Info (NDR)")

                # Use actual form field IDs from NDR_FORM_MAP
                fn_input = page.locator("input[name='input_3'], input#input_274_3").first
                try:
                    await fn_input.wait_for(timeout=10000)
                except Exception:
                    fn_input = page.locator("input[placeholder*='First']").first
                    await fn_input.wait_for(timeout=10000)
                await fn_input.click()
                await fn_input.fill(lead["first_name"])
                await human_delay(0.3, 0.7)

                ln_input = page.locator("input[name='input_4'], input#input_274_4").first
                try:
                    await ln_input.wait_for(timeout=5000)
                except Exception:
                    ln_input = page.locator("input[placeholder*='Last']").first
                    await ln_input.wait_for(timeout=5000)
                await ln_input.click()
                await ln_input.fill(lead["last_name"])
                await human_delay(0.3, 0.7)

                em_input = page.locator("input[name='input_8'], input#input_274_8, input[type='email']").first
                try:
                    await em_input.wait_for(timeout=5000)
                except Exception:
                    em_input = page.locator("input[placeholder*='Email']").first
                    await em_input.wait_for(timeout=5000)
                await em_input.click()
                await em_input.fill(lead["email"])
                await human_delay(0.3, 0.7)

                phone_digits = ''.join(c for c in lead["phone"] if c.isdigit())
                ph_input = page.locator("input[name='input_76'], input#phone, input[type='tel']").first
                try:
                    await ph_input.wait_for(timeout=5000)
                except Exception:
                    ph_input = page.locator("input[placeholder*='Phone']").first
                    await ph_input.wait_for(timeout=5000)
                await ph_input.click()
                await ph_input.type(phone_digits, delay=60)
                await human_delay(0.3, 0.7)

                await page.keyboard.press("Tab")
                await page.wait_for_timeout(1500)

                submit_btn = page.locator(
                    "button:has-text('See My Relief Options'), "
                    "input[type='submit'], "
                    "button[type='submit']"
                ).first

                if dry_run:
                    print("[DRY RUN] Form filled — NOT submitting.")
                    ss_path = PROJECT_ROOT / "tmp" / f"ndr-dryrun-{int(time.time())}.png"
                    ss_path.parent.mkdir(exist_ok=True)
                    await page.screenshot(path=str(ss_path), full_page=True)
                    print(f"  Screenshot: {ss_path}")
                    if offer_id:
                        log_submission(offer_id, lead, aff_click_id, success=True, dry_run=True)
                    await browser.close()
                    return True

                if safe_submit_probe:
                    print("[!] SAFE SUBMIT PROBE (NDR): clicking submit with network guard.")
                else:
                    print("[!] SUBMITTING (NDR)...")
                await submit_btn.click(timeout=10000)
                await page.wait_for_timeout(5000)

                current_url = page.url

                if safe_submit_probe:
                    if not blocked_requests:
                        print("[✗] Safe submit probe failed: no blocked POST /details was observed.")
                        ss_path = PROJECT_ROOT / "tmp" / f"ndr-safeprobe-missed-{int(time.time())}.png"
                        ss_path.parent.mkdir(exist_ok=True)
                        await page.screenshot(path=str(ss_path), full_page=True)
                        print(f"  Screenshot: {ss_path}")
                        await browser.close()
                        return False

                    blocked = blocked_requests[-1]
                    print(f"[✓] Safe submit probe blocked request: {blocked['method']} {blocked['url']}")
                    success = "personalizesavings" not in current_url.lower()
                    if not success:
                        print("[✗] Unsafe outcome: reached /personalizesavings despite submit guard.")
                    else:
                        print("[✓] Safe probe succeeded: submit path blocked before live prospect creation.")

                    ss_path = PROJECT_ROOT / "tmp" / f"ndr-safeprobe-{int(time.time())}.png"
                    ss_path.parent.mkdir(exist_ok=True)
                    await page.screenshot(path=str(ss_path), full_page=True)
                    print(f"  Screenshot: {ss_path}")
                    await browser.close()
                    return success

                content = await page.content()
                success = (
                    "thank" in content.lower()
                    or "results" in current_url.lower()
                    or "confirmation" in content.lower()
                    or "details" not in current_url
                )
                print(f"[{'✓' if success else '?'}] NDR submission {'successful' if success else 'unclear result'}")
                ss_path = PROJECT_ROOT / "tmp" / f"ndr-submit-{int(time.time())}.png"
                ss_path.parent.mkdir(exist_ok=True)
                await page.screenshot(path=str(ss_path), full_page=True)
                print(f"  Screenshot: {ss_path}")
                if offer_id:
                    log_submission(offer_id, lead, aff_click_id, success=success, dry_run=False)
                await browser.close()
                return success

            else:
                # FDR: slider-based. Set the slider value then click Continue.
                # The slider is an MUI Slider — we can set it via the input or drag.
                # Try setting the hidden input value and dispatching events.
                # First look for the slider input
                print(f"  FDR slider: setting to ${debt_amount:,}")

                # Try to find and interact with slider input
                try:
                    slider_input = page.locator("input[type='range']").first
                    await slider_input.wait_for(timeout=8000)
                    await slider_input.fill(str(debt_amount))
                    await slider_input.dispatch_event("input")
                    await slider_input.dispatch_event("change")
                except Exception:
                    # Fallback: use JS to set slider value
                    await page.evaluate(f"""(() => {{
                        const input = document.querySelector('input[type="range"]');
                        if (input) {{
                            const nativeSetter = Object.getOwnPropertyDescriptor(
                                HTMLInputElement.prototype, 'value').set;
                            nativeSetter.call(input, '{debt_amount}');
                            input.dispatchEvent(new Event('input', {{bubbles: true}}));
                            input.dispatchEvent(new Event('change', {{bubbles: true}}));
                        }}
                    }})()""")

                await human_delay()

                # Click Continue
                continue_btn = page.get_by_role("button", name="Continue").or_(
                    page.get_by_role("link", name="Continue")
                ).or_(
                    page.locator("button:has-text('Continue')")
                )
                await continue_btn.first.click(timeout=10000)
                print("  → Moving to state selection...")
                await page.wait_for_url("**/home/states**", timeout=30000)
                await page.wait_for_timeout(2000)

            # ── STEP 2: State Selection ──
            print(f"[2/3] State: {lead['state']} ({state_name})")

            # Custom MUI combobox — searchable. Click to open, type state name, select.
            # Look for the combobox input
            combo_input = page.locator(
                "input[role='combobox'], "
                "input[aria-autocomplete='list'], "
                "input[placeholder*='state' i], "
                "input[placeholder*='State' i], "
                "input[aria-label*='state' i]"
            ).first

            try:
                await combo_input.wait_for(timeout=10000)
            except Exception:
                # Broader search: any visible text input on the states page
                combo_input = page.locator("input[type='text']").first
                await combo_input.wait_for(timeout=10000)

            # Clear existing value and type state name
            await combo_input.click()
            await human_delay(0.3, 0.6)
            await combo_input.fill("")
            await combo_input.type(state_name, delay=50)
            await human_delay(0.5, 1.0)

            # Wait for dropdown option and click it
            option = page.locator(
                f"li[role='option']:has-text('{state_name}'), "
                f"[role='option']:has-text('{state_name}'), "
                f".MuiAutocomplete-option:has-text('{state_name}')"
            ).first
            try:
                await option.wait_for(timeout=5000)
                await option.click()
            except Exception:
                # Fallback: press Enter to select first match
                await page.keyboard.press("ArrowDown")
                await page.keyboard.press("Enter")
            await human_delay()

            # Click Next
            next_btn = page.get_by_role("button", name="Next").or_(
                page.locator("button:has-text('Next')")
            )
            await next_btn.first.click(timeout=10000)
            print("  → Moving to contact info...")
            await page.wait_for_url("**/home/contact-info**", timeout=30000)
            await page.wait_for_timeout(2000)

            # ── STEP 3: Contact Info ──
            print("[3/3] Contact Info")

            # Fill first name
            fn_input = page.locator("input[name='firstName'], input#firstName, input[autocomplete='given-name']").first
            await fn_input.wait_for(timeout=10000)
            await fn_input.click()
            await fn_input.fill(lead["first_name"])
            await human_delay(0.3, 0.7)

            # Fill last name
            ln_input = page.locator("input[name='lastName'], input#lastName, input[autocomplete='family-name']").first
            await ln_input.click()
            await ln_input.fill(lead["last_name"])
            await human_delay(0.3, 0.7)

            # Fill phone
            phone_digits = ''.join(c for c in lead["phone"] if c.isdigit())
            ph_input = page.locator("input[name='phone'], input#phone, input[type='tel']").first
            await ph_input.click()
            await ph_input.type(phone_digits, delay=60)
            await human_delay(0.3, 0.7)

            # Fill email
            em_input = page.locator("input[name='email'], input#email, input[type='email'], input[autocomplete='email']").first
            await em_input.click()
            await em_input.fill(lead["email"])
            await human_delay(0.3, 0.7)

            # Tab out to trigger validation
            await page.keyboard.press("Tab")
            await page.wait_for_timeout(1500)

            # Wait for submit button to become enabled
            submit_btn = page.locator(
                "button:has-text('Click to see your results'), "
                "button:has-text('See your results'), "
                "button[type='submit']"
            ).first

            if dry_run:
                print("[DRY RUN] Form filled — NOT submitting.")
                ss_path = PROJECT_ROOT / "tmp" / f"fdr-ndr-dryrun-{int(time.time())}.png"
                ss_path.parent.mkdir(exist_ok=True)
                await page.screenshot(path=str(ss_path), full_page=True)
                print(f"  Screenshot: {ss_path}")
                # Log as dry run
                if offer_id:
                    log_submission(offer_id, lead, aff_click_id, success=True, dry_run=True)
                await browser.close()
                return True

            if safe_submit_probe:
                print("[✗] Safe submit probe currently supports NDR only. Aborting before FDR submit.")
                await browser.close()
                return False

            # Wait for button to be enabled (React validation)
            print("  Waiting for submit button to enable...")
            try:
                await submit_btn.wait_for(state="visible", timeout=5000)
                # Poll for enabled state
                for _ in range(20):
                    disabled = await submit_btn.is_disabled()
                    if not disabled:
                        break
                    await page.wait_for_timeout(500)
                else:
                    print("[!] Submit button still disabled after 10s — attempting anyway")
            except Exception as e:
                print(f"[!] Button wait issue: {e}")

            print("[!] SUBMITTING...")
            await submit_btn.click(timeout=10000)
            await page.wait_for_timeout(5000)

            # Check for success
            current_url = page.url
            content = await page.content()
            success = (
                "thank" in content.lower()
                or "results" in current_url.lower()
                or "confirmation" in content.lower()
                or "contact-info" not in current_url  # navigated away = likely success
            )

            if success:
                print("[✓] Form submitted successfully!")
            else:
                print("[?] Submitted but unclear result")

            ss_path = PROJECT_ROOT / "tmp" / f"fdr-ndr-submit-{int(time.time())}.png"
            ss_path.parent.mkdir(exist_ok=True)
            await page.screenshot(path=str(ss_path), full_page=True)
            print(f"  Screenshot: {ss_path}")

            if offer_id:
                log_submission(offer_id, lead, aff_click_id, success=success, dry_run=False)

            await browser.close()
            return success

        except Exception as e:
            print(f"[✗] Error: {e}")
            ss_path = PROJECT_ROOT / "tmp" / f"fdr-ndr-error-{int(time.time())}.png"
            ss_path.parent.mkdir(exist_ok=True)
            try:
                await page.screenshot(path=str(ss_path), full_page=True)
                print(f"  Error screenshot: {ss_path}")
            except Exception:
                pass
            await browser.close()
            return False


def main():
    parser = argparse.ArgumentParser(description="FDR/NDR Debt Relief Form Filler")
    parser.add_argument("--offer", required=True, choices=["fdr", "ndr"], help="Which offer entry point")
    parser.add_argument("--offer-id", type=int, help="Offer ID for cap check and logging")
    parser.add_argument("--dry-run", action="store_true", help="Fill but don't submit")
    parser.add_argument(
        "--safe-submit-probe",
        action="store_true",
        help="NDR-only: click submit but block live POST /details so no prospect is created",
    )
    parser.add_argument("--headless", action="store_true", default=True, help="Run headless (default)")
    parser.add_argument("--no-headless", action="store_true", help="Show browser window")
    parser.add_argument("--lead-id", help="Load lead from Supabase by UUID")
    # CLI lead data overrides
    parser.add_argument("--first-name", help="First name")
    parser.add_argument("--last-name", help="Last name")
    parser.add_argument("--email", help="Email")
    parser.add_argument("--phone", help="Phone (digits only or formatted)")
    parser.add_argument("--state", help="State abbreviation (e.g. TX)")
    parser.add_argument("--debt-amount", help="Debt amount (e.g. 25000)")

    args = parser.parse_args()
    if args.safe_submit_probe and args.dry_run:
        parser.error("--safe-submit-probe cannot be combined with --dry-run.")
    if args.safe_submit_probe and args.offer != "ndr":
        parser.error("--safe-submit-probe currently supports --offer ndr only.")

    headless = not args.no_headless

    # Build lead data
    if args.lead_id:
        lead = load_lead_from_db(args.lead_id)
        print(f"[*] Loaded lead {args.lead_id} from DB")
    elif args.first_name and args.last_name and args.email and args.phone and args.state and args.debt_amount:
        lead = {
            "first_name": args.first_name,
            "last_name": args.last_name,
            "email": args.email,
            "phone": args.phone,
            "state": args.state,
            "debt_amount": args.debt_amount,
        }
        print("[*] Using CLI-provided lead data")
    else:
        lead = TEST_LEAD.copy()
        print("[*] Using test lead data (no --lead-id or full CLI args provided)")

    # CLI overrides on top of DB/test data
    if args.first_name: lead["first_name"] = args.first_name
    if args.last_name: lead["last_name"] = args.last_name
    if args.email: lead["email"] = args.email
    if args.phone: lead["phone"] = args.phone
    if args.state: lead["state"] = args.state
    if args.debt_amount: lead["debt_amount"] = args.debt_amount

    success = asyncio.run(fill_form(
        lead=lead,
        offer=args.offer,
        dry_run=args.dry_run,
        offer_id=args.offer_id,
        headless=headless,
        safe_submit_probe=args.safe_submit_probe,
    ))

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
