#!/usr/bin/env python3
"""
Stealth Browser — Project Ocean
================================
Provides a stealth browser session using Camoufox (Firefox anti-detection)
with IPRoyal residential proxy support.

Usage as module:
    from stealth_browser import get_stealth_browser, get_stealth_page
    
    # Async context manager
    async with get_stealth_browser() as (browser, page):
        await page.goto("https://example.com")
        # ... do stuff
    
Usage as CLI (test):
    python3 scripts/stealth_browser.py                    # Test with ipcheck
    python3 scripts/stealth_browser.py --url https://reddit.com  # Scrape a URL
    python3 scripts/stealth_browser.py --bot-check        # Run bot detection tests
"""

import asyncio
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def get_proxy_config() -> dict | None:
    """Get IPRoyal proxy config from .env"""
    host = os.environ.get("PROXY_HOST")
    port = os.environ.get("PROXY_PORT")
    user = os.environ.get("PROXY_USER")
    pwd = os.environ.get("PROXY_PASS")
    if host and port and user and pwd:
        return {
            "server": f"http://{host}:{port}",
            "username": user,
            "password": pwd,
        }
    return None


@asynccontextmanager
async def get_stealth_browser(headless=True, use_proxy=True):
    """
    Async context manager that yields (browser, page) with Camoufox stealth.
    Falls back to Playwright + stealth plugin if Camoufox not available.
    """
    proxy = get_proxy_config() if use_proxy else None
    browser = None
    
    try:
        # Try Camoufox first (best anti-detection)
        from camoufox.async_api import AsyncCamoufox
        
        camoufox_opts = {
            "headless": headless,
            "geoip": True,  # Match geolocation to proxy IP
        }
        if proxy:
            camoufox_opts["proxy"] = {
                "server": proxy["server"],
                "username": proxy["username"],
                "password": proxy["password"],
            }
        
        async with AsyncCamoufox(**camoufox_opts) as browser:
            page = await browser.new_page()
            print("[*] Browser: Camoufox (stealth Firefox)")
            if proxy:
                print(f"[*] Proxy: {os.environ.get('PROXY_HOST')} (US residential)")
            yield browser, page
            
    except (ImportError, Exception) as e:
        print(f"[!] Camoufox error: {e}, falling back to Playwright + stealth")
        
        # Fallback: Playwright Chromium + stealth plugin
        from playwright.async_api import async_playwright
        
        pw_manager = async_playwright()
        pw = await pw_manager.start()
        try:
            launch_args = {"headless": headless}
            if proxy:
                launch_args["proxy"] = proxy
            
            browser = await pw.chromium.launch(**launch_args)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                ),
            )
            page = await context.new_page()
            
            # Apply stealth patches
            try:
                from playwright_stealth import stealth_async
                await stealth_async(page)
                print("[*] Browser: Playwright Chromium + stealth plugin")
            except ImportError:
                print("[*] Browser: Playwright Chromium (NO stealth!)")
            
            if proxy:
                print(f"[*] Proxy: {os.environ.get('PROXY_HOST')} (US residential)")
            
            yield browser, page
        finally:
            if browser:
                await browser.close()
            await pw.stop()


async def test_stealth(url=None, bot_check=False):
    """Test the stealth browser"""
    async with get_stealth_browser() as (browser, page):
        # 1. IP check
        await page.goto("https://ipv4.icanhazip.com", timeout=15000)
        ip = (await page.inner_text("body")).strip()
        print(f"\n✅ IP Address: {ip}")
        
        # 2. Bot detection test
        if bot_check:
            print("\n--- Bot Detection Tests ---")
            await page.goto("https://bot.sannysoft.com/", timeout=20000)
            await page.wait_for_timeout(3000)
            
            # Check key indicators
            results = await page.evaluate("""() => {
                const rows = document.querySelectorAll('table tr');
                const checks = {};
                rows.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    if (cells.length >= 2) {
                        const test = cells[0]?.textContent?.trim();
                        const result = cells[1]?.textContent?.trim();
                        const passed = cells[1]?.classList?.contains('passed') || 
                                       result?.toLowerCase() === 'ok' ||
                                       !cells[1]?.classList?.contains('failed');
                        if (test) checks[test] = {result, passed};
                    }
                });
                return checks;
            }""")
            
            for test, info in results.items():
                icon = "✅" if info.get("passed") else "❌"
                print(f"  {icon} {test}: {info.get('result', '?')}")
            
            # Screenshot
            ss_path = PROJECT_ROOT / "tmp" / "bot-check.png"
            ss_path.parent.mkdir(exist_ok=True)
            await page.screenshot(path=str(ss_path), full_page=True)
            print(f"\n📸 Screenshot: {ss_path}")
        
        # 3. Custom URL
        if url:
            print(f"\n--- Loading: {url} ---")
            await page.goto(url, timeout=20000)
            await page.wait_for_timeout(2000)
            title = await page.title()
            print(f"Title: {title}")
            print(f"URL: {page.url}")
            
            ss_path = PROJECT_ROOT / "tmp" / "stealth-browse.png"
            ss_path.parent.mkdir(exist_ok=True)
            await page.screenshot(path=str(ss_path), full_page=True)
            print(f"📸 Screenshot: {ss_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Stealth Browser Test")
    parser.add_argument("--url", help="URL to visit")
    parser.add_argument("--bot-check", action="store_true", help="Run bot detection test")
    args = parser.parse_args()
    
    asyncio.run(test_stealth(url=args.url, bot_check=args.bot_check))
