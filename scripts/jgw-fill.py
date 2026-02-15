#!/usr/bin/env python3
"""
JG Wentworth Debt Relief Form Filler
Gravity Forms (gform_48), 10 steps, single-page wizard.

Usage:
    python3 scripts/jgw-fill.py                    # dry run with test data
    python3 scripts/jgw-fill.py --submit           # actually submit
    python3 scripts/jgw-fill.py --headless          # headless mode
    python3 scripts/jgw-fill.py --lead-id <uuid>   # fill from DB lead

Requires: playwright (pip install playwright && playwright install chromium)
"""
import argparse, asyncio, json, os, sys, time, random
from pathlib import Path
from datetime import datetime

# Add project root
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Test lead data (used when no --lead-id provided)
# ---------------------------------------------------------------------------
TEST_LEAD = {
    "debt_amount": "25000",
    "employment_status": "employed",
    "annual_income": "65000",
    "property_status": "rent",
    "first_name": "John",
    "last_name": "TestLead",
    "email": "testlead.ocean@gmail.com",
    "phone": "(512) 555-0199",
    "address1": "123 Test Street",
    "address2": "",
    "city": "Austin",
    "state": "TX",
    "zip_code": "78701",
    "date_of_birth": "01/15/1985",
    "ssn": "000-00-0000",  # Fake — never real SSN
}

URL = "https://www.jgwentworth.com/debt-relief"


def load_lead_from_db(lead_id: str) -> dict:
    """Load lead data from Supabase. Returns dict matching TEST_LEAD shape."""
    try:
        import httpx
    except ImportError:
        print("ERROR: httpx required for DB access. pip install httpx")
        sys.exit(1)

    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")

    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

    resp = httpx.get(
        f"{url}/rest/v1/leads?id=eq.{lead_id}&select=*",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    resp.raise_for_status()
    rows = resp.json()
    if not rows:
        print(f"ERROR: No lead found with id={lead_id}")
        sys.exit(1)

    row = rows[0]
    form_data = row.get("form_data") or {}

    return {
        "debt_amount": str(row.get("debt_amount", "")),
        "employment_status": form_data.get("employment_status", "employed"),
        "annual_income": str(row.get("annual_income", "")),
        "property_status": row.get("property_status", "rent"),
        "first_name": row.get("first_name", ""),
        "last_name": row.get("last_name", ""),
        "email": row.get("email", ""),
        "phone": row.get("phone", ""),
        "address1": row.get("address1", ""),
        "address2": row.get("address2", ""),
        "city": row.get("city", ""),
        "state": form_data.get("state", ""),
        "zip_code": form_data.get("zip_code", ""),
        "date_of_birth": row.get("date_of_birth", ""),
        "ssn": "000-00-0000",  # NEVER pull real SSN
    }


async def fill_form(lead: dict, headless: bool = True, submit: bool = False):
    """Fill the JGW debt relief form step by step."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("ERROR: playwright required. pip install playwright && playwright install chromium")
        sys.exit(1)

    async with async_playwright() as p:
        launch_opts = {"headless": headless}
        # IPRoyal residential proxy (US)
        proxy_url = os.environ.get("PROXY_URL")
        if proxy_url:
            launch_opts["proxy"] = {
                "server": f"http://{os.environ.get('PROXY_HOST', 'geo.iproyal.com')}:{os.environ.get('PROXY_PORT', '12321')}",
                "username": os.environ.get("PROXY_USER", ""),
                "password": os.environ.get("PROXY_PASS", ""),
            }
            print(f"[*] Using proxy: {os.environ.get('PROXY_HOST', 'geo.iproyal.com')}")
        browser = await p.chromium.launch(**launch_opts)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        )
        page = await context.new_page()

        print(f"[*] Navigating to {URL}")
        await page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_selector("#gform_48", timeout=15000)
        print("[✓] Form loaded")

        async def human_delay():
            """Random delay to mimic human behavior."""
            await asyncio.sleep(random.uniform(0.5, 1.5))

        # Gravity Forms page → next button ID mapping
        NEXT_BTNS = {
            1: "gform_next_button_48_98",
            2: "gform_next_button_48_101",
            3: "gform_next_button_48_100",
            4: "gform_next_button_48_103",
            5: "gform_next_button_48_108",
            6: "gform_next_button_48_107",
            7: "gform_next_button_48_104",
            8: "gform_next_button_48_105",
            9: "gform_next_button_48_106",
        }

        async def click_continue(step: int):
            """Click Continue and wait for next page to become visible (AJAX)."""
            next_page = step + 1
            btn_id = NEXT_BTNS[step]

            # Direct DOM manipulation — show next page, hide current
            # This bypasses Gravity Forms AJAX validation (server validates on final submit)
            await page.evaluate(f"""(() => {{
                document.getElementById('gform_page_48_{step}').style.display = 'none';
                document.getElementById('gform_page_48_{next_page}').style.display = 'block';
                // Update Gravity Forms internal page tracking
                const target = document.getElementById('gform_target_page_number_48');
                const source = document.getElementById('gform_source_page_number_48');
                if (target) target.value = '{next_page}';
                if (source) source.value = '{step}';
            }})()""")
            await human_delay()

        async def set_value(selector: str, value: str):
            """Set input value using native Playwright interaction for proper event handling."""
            # Use JS to make element visible/scrollable first
            await page.evaluate(f"""(() => {{
                const el = document.querySelector('{selector}');
                if (el) el.scrollIntoView({{block: 'center'}});
            }})()""")
            await page.wait_for_timeout(200)
            loc = page.locator(selector)
            try:
                await loc.click(timeout=5000)
                await loc.fill("", timeout=2000)
                await loc.type(value, delay=40)
            except Exception:
                # Fallback: JS if element isn't interactable
                await page.evaluate(f"""(() => {{
                    const el = document.querySelector('{selector}');
                    const nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
                    nativeSetter.call(el, '{value}');
                    el.dispatchEvent(new Event('input', {{bubbles: true}}));
                    el.dispatchEvent(new Event('change', {{bubbles: true}}));
                    el.dispatchEvent(new Event('blur', {{bubbles: true}}));
                }})()""")
            await human_delay()

        # ── Step 1: Debt Amount ──
        print("[1/10] Debt Amount")
        await set_value("#input_48_111", lead["debt_amount"])
        await click_continue(1)

        # ── Step 2: Employment Status ──
        print("[2/10] Employment Status")
        emp_value = lead["employment_status"]
        await page.evaluate(f"document.querySelector(\"input[name='input_37'][value='{emp_value}']\").click()")
        await human_delay()
        await click_continue(2)

        # ── Step 3: Annual Income ──
        print("[3/10] Annual Income")
        await set_value("#input_48_84", lead["annual_income"])
        await click_continue(3)

        # ── Step 4: Property Status ──
        print("[4/10] Property Status")
        prop_value = lead["property_status"]
        await page.evaluate(f"document.querySelector(\"input[name='input_35'][value='{prop_value}']\").click()")
        await human_delay()
        await click_continue(4)

        # ── Step 5: First Name + Last Name ──
        print("[5/10] Name")
        await set_value("#input_48_1", lead["first_name"])
        await set_value("#input_48_3", lead["last_name"])
        await click_continue(5)

        # ── Step 6: Email ──
        print("[6/10] Email")
        await set_value("#input_48_26", lead["email"])
        await click_continue(6)

        # ── Step 7: Phone ──
        # Phone uses inputmask "(999) 999-9999"
        print("[7/10] Phone")
        phone_digits = ''.join(c for c in lead["phone"] if c.isdigit())
        formatted = f"({phone_digits[:3]}) {phone_digits[3:6]}-{phone_digits[6:]}" if len(phone_digits) == 10 else lead["phone"]

        # Phone has inputmask — need native typing, but element might be "hidden" by Playwright
        # since we're manipulating DOM directly. Use JS to ensure visibility + focus, then type.
        await page.evaluate("""(() => {
            const el = document.getElementById('input_48_28');
            el.scrollIntoView({block: 'center'});
        })()""")
        await page.wait_for_timeout(300)
        phone_loc = page.locator("#input_48_28")
        try:
            await phone_loc.click(timeout=3000)
            await phone_loc.press_sequentially(phone_digits, delay=100)
            await page.keyboard.press("Tab")
        except Exception:
            # Fallback: set via inputmask API
            formatted = f"({phone_digits[:3]}) {phone_digits[3:6]}-{phone_digits[6:]}" if len(phone_digits) == 10 else lead["phone"]
            await page.evaluate(f"""(() => {{
                const el = document.getElementById('input_48_28');
                if (el.inputmask) el.inputmask.setValue('{formatted}');
                const ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
                ns.call(el, '{formatted}');
                el.dispatchEvent(new Event('input', {{bubbles: true}}));
                el.dispatchEvent(new Event('change', {{bubbles: true}}));
            }})()""")
        await human_delay()
        phone_val = await page.evaluate("document.getElementById('input_48_28').value")
        print(f"    Phone value set: {phone_val}")

        await click_continue(7)

        # ── Step 8: Address ──
        print("[8/10] Address")
        await set_value("#input_48_89", lead["address1"])
        if lead.get("address2"):
            await set_value("#input_48_90", lead["address2"])
        await set_value("#input_48_91", lead["city"])
        await page.evaluate(f"""(() => {{
            const sel = document.getElementById('input_48_109');
            sel.value = '{lead["state"]}';
            sel.dispatchEvent(new Event('change', {{bubbles: true}}));
        }})()""")
        await human_delay()
        await set_value("#input_48_92", lead["zip_code"])
        await click_continue(8)

        # ── Step 9: Date of Birth ──
        print("[9/10] Date of Birth")
        await set_value("#input_48_85", lead["date_of_birth"])
        await click_continue(9)

        # ── Step 10: SSN (final) ──
        print("[10/10] SSN")
        await set_value("#input_48_94", lead["ssn"])

        if submit:
            print("[!] SUBMITTING FORM...")
            await page.locator("#gform_submit_button_48").click()
            await page.wait_for_timeout(5000)
            # Check for confirmation
            content = await page.content()
            if "thank" in content.lower() or "confirmation" in content.lower():
                print("[✓] Form submitted successfully!")
            else:
                print("[?] Form submitted but no clear confirmation detected")
                # Save screenshot for review
                ss_path = PROJECT_ROOT / "tmp" / f"jgw-submit-{int(time.time())}.png"
                ss_path.parent.mkdir(exist_ok=True)
                await page.screenshot(path=str(ss_path), full_page=True)
                print(f"    Screenshot: {ss_path}")
        else:
            print("[DRY RUN] Form filled but NOT submitted. Add --submit to submit.")
            # Screenshot the final state
            ss_path = PROJECT_ROOT / "tmp" / f"jgw-dryrun-{int(time.time())}.png"
            ss_path.parent.mkdir(exist_ok=True)
            await page.screenshot(path=str(ss_path), full_page=True)
            print(f"    Screenshot: {ss_path}")

        await browser.close()

    return True


async def fill_and_store(lead: dict, headless: bool, submit: bool, store: bool):
    """Fill form and optionally store lead in Supabase."""
    success = await fill_form(lead, headless=headless, submit=submit)

    if store and success:
        try:
            import httpx
            from dotenv import load_dotenv
            load_dotenv(PROJECT_ROOT / ".env")

            url = os.environ["SUPABASE_URL"]
            key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

            # Parse DOB to date format if provided as MM/DD/YYYY
            dob = lead.get("date_of_birth", "")
            dob_iso = None
            if dob:
                try:
                    dob_iso = datetime.strptime(dob, "%m/%d/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    dob_iso = None

            lead_row = {
                "first_name": lead["first_name"],
                "last_name": lead["last_name"],
                "email": lead["email"],
                "phone": lead["phone"],
                "debt_amount": int(lead["debt_amount"].replace(",", "").replace("$", "")),
                "annual_income": int(lead["annual_income"].replace(",", "").replace("$", "")),
                "property_status": lead["property_status"],
                "address1": lead["address1"],
                "address2": lead.get("address2", ""),
                "city": lead["city"],
                "state": lead["state"],
                "zip": lead.get("zip_code", ""),
                "source": "jgwentworth_form_fill",
                "form_url": "https://www.jgwentworth.com/debt-relief",
                "employment_status": lead["employment_status"],
                "status": "new",
                "form_data": json.dumps({
                    "offer": "jgwentworth",
                    "submitted": submit,
                    # SSN intentionally excluded
                }),
            }
            if dob_iso:
                lead_row["date_of_birth"] = dob_iso

            resp = httpx.post(
                f"{url}/rest/v1/leads",
                headers={
                    "apikey": key,
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation",
                },
                json=lead_row,
            )
            resp.raise_for_status()
            stored = resp.json()
            print(f"[✓] Lead stored in DB: {stored[0]['id']}")
        except Exception as e:
            print(f"[✗] Failed to store lead: {e}")


def main():
    parser = argparse.ArgumentParser(description="JGW Debt Relief Form Filler")
    parser.add_argument("--submit", action="store_true", help="Actually submit the form")
    parser.add_argument("--headless", action="store_true", help="Run headless (no browser window)")
    parser.add_argument("--lead-id", help="Load lead data from DB by UUID")
    parser.add_argument("--no-store", action="store_true", help="Don't store lead in DB after fill")
    args = parser.parse_args()

    if args.lead_id:
        lead = load_lead_from_db(args.lead_id)
        print(f"[*] Loaded lead {args.lead_id} from DB")
    else:
        lead = TEST_LEAD.copy()
        print("[*] Using test lead data")

    print(f"[*] Lead: {lead['first_name']} {lead['last_name']}, ${lead['debt_amount']} debt, {lead['state']}")
    print(f"[*] Mode: {'SUBMIT' if args.submit else 'DRY RUN'} | {'Headless' if args.headless else 'Visible'}")

    asyncio.run(fill_and_store(
        lead,
        headless=args.headless,
        submit=args.submit,
        store=not args.no_store,
    ))


if __name__ == "__main__":
    main()
