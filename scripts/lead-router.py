#!/usr/bin/env python3
"""
Lead Router — Project Ocean
Given a lead_id, determines the best offer(s) to route it to.
"""

import sys
import os
import json
from datetime import datetime, timezone
from pathlib import Path

import httpx
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

# Source → channel mapping
SOURCE_TO_CHANNEL = {
    "fb": "web",
    "revpie": "web",
    "organic": "web",
    "form": "web",
    "email": "email",
    "call": "call",
}

SCHEDULE_WEEKDAY_ONLY = {"M-F"}

# ---------------------------------------------------------------------------
# Supabase helpers
# ---------------------------------------------------------------------------

def sb_get(table: str, params: dict | None = None) -> list[dict]:
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    r = httpx.get(url, headers=HEADERS, params=params or {}, timeout=15)
    r.raise_for_status()
    return r.json()


def sb_rpc(fn: str, body: dict) -> list[dict]:
    url = f"{SUPABASE_URL}/rest/v1/rpc/{fn}"
    r = httpx.post(url, headers=HEADERS, json=body, timeout=15)
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------------
# Core routing
# ---------------------------------------------------------------------------

def fetch_lead(lead_id: str) -> dict:
    rows = sb_get("leads", {"id": f"eq.{lead_id}", "select": "*"})
    if not rows:
        raise SystemExit(f"❌ Lead {lead_id} not found")
    return rows[0]


def fetch_active_offers() -> list[dict]:
    return sb_get("everflow_offers", {"status": "eq.active", "select": "*"})


def is_weekday() -> bool:
    return datetime.now(timezone.utc).weekday() < 5  # Mon=0 .. Fri=4


def check_cap(offer_id: int) -> dict:
    """Call check_offer_cap RPC. Returns dict with can_submit, reason, daily_remaining, weekly_remaining."""
    result = sb_rpc("check_offer_cap", {"p_offer_id": offer_id})
    if isinstance(result, list) and result:
        return result[0]
    return result


def route_lead(lead_id: str) -> None:
    lead = fetch_lead(lead_id)
    offers = fetch_active_offers()

    lead_channel = SOURCE_TO_CHANNEL.get(lead.get("source", ""), "web")
    lead_state = (lead.get("state") or "").upper()
    lead_debt = float(lead.get("debt_amount") or 0)
    lead_name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
    weekday = is_weekday()

    eligible: list[dict] = []
    excluded: list[dict] = []

    for o in offers:
        oid = o["offer_id"]
        oname = o["offer_name"]
        buyer = o["buyer_short"]
        cpa = float(o["cpa"])
        ch = o["channel"]
        reason = None

        # 1. Channel match
        if ch != "any" and ch != lead_channel:
            reason = f"channel mismatch ({ch} only, lead is {lead_channel})"

        # 2. State exclusion
        if not reason:
            excl = o.get("excluded_states") or []
            if lead_state and lead_state in [s.upper() for s in excl]:
                reason = f"state excluded ({lead_state})"

        # 3. Schedule
        if not reason:
            sched = (o.get("schedule") or "7days").strip()
            if sched in SCHEDULE_WEEKDAY_ONLY and not weekday:
                reason = "M-F only (today is weekend)"

        # 4. Min debt
        if not reason:
            min_debt = o.get("min_debt_amount")
            if min_debt and lead_debt < float(min_debt):
                reason = f"min debt ${min_debt:,.0f} (lead has ${lead_debt:,.0f})"

        # 5. Cap check (only if passed other filters)
        cap_info = None
        if not reason:
            cap_info = check_cap(oid)
            if not cap_info.get("can_submit"):
                reason = cap_info.get("reason", "cap reached")

        if reason:
            excluded.append({"offer": o, "reason": reason})
        else:
            eligible.append({"offer": o, "cap": cap_info})

    # Sort eligible by CPA descending
    eligible.sort(key=lambda x: float(x["offer"]["cpa"]), reverse=True)

    # ---------------------------------------------------------------------------
    # Output
    # ---------------------------------------------------------------------------
    debt_type = lead.get("debt_type") or "unknown"
    print(f"\nLEAD ROUTING — Lead {lead_id}")
    print(f"Lead: {lead_name} | {lead_state or '??'} | ${lead_debt:,.0f} {debt_type} debt | Source: {lead.get('source', '?')}")
    print()

    if eligible:
        print("Eligible Offers (ranked by CPA):")
        for i, e in enumerate(eligible, 1):
            o = e["offer"]
            cap = e["cap"]
            excl_note = ""
            if o.get("excluded_states"):
                excl_note = f", NO {','.join(o['excluded_states'])}"
            wr = cap.get("weekly_remaining", "?")
            wc = o.get("weekly_cap") or "∞"
            print(f"  {i}. Offer {o['offer_id']} — {o['buyer_short']} ${float(o['cpa']):.0f} ({o['channel']}{excl_note}) — {wr}/{wc} weekly remaining")
    else:
        print("⚠️  No eligible offers found!")

    if excluded:
        print("\nExcluded:")
        for x in excluded:
            o = x["offer"]
            print(f"  - Offer {o['offer_id']} — {o['buyer_short']} ${float(o['cpa']):.0f} — {x['reason']}")

    if eligible:
        top = eligible[0]["offer"]
        print(f"\nRECOMMENDED: Offer {top['offer_id']} — {top['buyer_short']} ${float(top['cpa']):.0f} (highest CPA with available cap)")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lead-router.py <lead_id>")
        sys.exit(1)
    route_lead(sys.argv[1])
