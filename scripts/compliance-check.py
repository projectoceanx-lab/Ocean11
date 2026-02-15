#!/usr/bin/env python3
"""
Shield 🛡️ — Compliance Check Pipeline
Playbook Rule #12: Shield approves before delivery. No exceptions.

Usage:
    python compliance-check.py <lead_id> <offer_id>
    python compliance-check.py <lead_id>              # checks lead only, no offer-specific checks
"""

import sys
import os
import re
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from uuid import UUID

import httpx
from dotenv import load_dotenv

# ── Config ──────────────────────────────────────────────────
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

# Debt types
ALLOWED_DEBT_TYPES = {"credit_card", "personal", "personal_loan", "mixed"}
BLOCKED_DEBT_TYPES = {"mortgage", "student", "student_loan", "auto", "auto_loan", "medical"}

# Phone: 10-digit US number (with optional +1, parens, dashes, spaces)
PHONE_RE = re.compile(
    r"^\+?1?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")

# Fake data patterns to block
FAKE_EMAILS = {"test@test.com", "fake@fake.com", "a@a.com", "none@none.com"}
FAKE_PHONES = {"5555555555", "0000000000", "1234567890", "1111111111"}


# ── Supabase helpers ────────────────────────────────────────
client = httpx.Client(base_url=SUPABASE_URL, headers=HEADERS, timeout=15)


def sb_get(table: str, params: dict) -> list[dict]:
    r = client.get(f"/rest/v1/{table}", params=params)
    r.raise_for_status()
    return r.json()


def sb_post(table: str, data: dict | list) -> list[dict]:
    r = client.post(f"/rest/v1/{table}", json=data)
    r.raise_for_status()
    return r.json()


# ── Check functions ─────────────────────────────────────────
class CheckResult:
    def __init__(self, check_type: str, result: str, reason: str, display: str):
        self.check_type = check_type
        self.result = result   # pass | flag | block
        self.reason = reason
        self.display = display

    @property
    def icon(self):
        return {"pass": "✅", "flag": "⚠️", "block": "🚫"}[self.result]


def check_state(lead: dict, offer: dict | None) -> CheckResult:
    state = (lead.get("state") or "").upper().strip()
    if not state:
        return CheckResult("state_eligibility", "flag", "No state on lead", "State: missing — flagged")

    if offer:
        excluded = offer.get("excluded_states") or []
        if isinstance(excluded, str):
            try:
                excluded = json.loads(excluded)
            except Exception:
                excluded = [s.strip() for s in excluded.split(",")]
        if state in [s.upper().strip() for s in excluded]:
            return CheckResult("state_eligibility", "block",
                               f"State {state} excluded for offer",
                               f"State: {state} — EXCLUDED by offer")

    return CheckResult("state_eligibility", "pass", f"State {state} allowed",
                        f"State: {state} — allowed")


def check_debt_type(lead: dict) -> CheckResult:
    dt = (lead.get("debt_type") or "").lower().strip()
    if not dt:
        return CheckResult("debt_type", "flag", "No debt type on lead", "Debt type: missing — flagged")
    if dt in BLOCKED_DEBT_TYPES:
        return CheckResult("debt_type", "block", f"Debt type '{dt}' not eligible",
                           f"Debt type: {dt} — BLOCKED (not unsecured)")
    if dt in ALLOWED_DEBT_TYPES:
        return CheckResult("debt_type", "pass", f"Debt type '{dt}' qualifies",
                           f"Debt type: {dt} — qualifies")
    return CheckResult("debt_type", "flag", f"Unknown debt type '{dt}'",
                        f"Debt type: {dt} — unknown, flagged for review")


def check_debt_amount(lead: dict, offer: dict | None) -> CheckResult:
    amt = lead.get("debt_amount")
    if amt is None:
        return CheckResult("debt_amount", "flag", "No debt amount", "Debt amount: missing — flagged")

    amt = float(amt)
    min_amt = 10000  # default minimum
    if offer and offer.get("min_debt_amount"):
        min_amt = float(offer["min_debt_amount"])

    if amt < min_amt:
        return CheckResult("debt_amount", "block",
                           f"${amt:,.0f} below minimum ${min_amt:,.0f}",
                           f"Debt amount: ${amt:,.0f} — below ${min_amt:,.0f} minimum")
    return CheckResult("debt_amount", "pass", f"${amt:,.0f} meets minimum ${min_amt:,.0f}",
                        f"Debt amount: ${amt:,.0f} — above ${min_amt:,.0f} minimum")


def check_phone(lead: dict) -> CheckResult:
    phone = (lead.get("phone") or "").strip()
    if not phone:
        return CheckResult("phone_validation", "block", "No phone number", "Phone: missing — BLOCKED")

    digits = re.sub(r"\D", "", phone)
    if digits.startswith("1") and len(digits) == 11:
        digits = digits[1:]

    if digits in FAKE_PHONES:
        return CheckResult("phone_validation", "block", "Fake phone detected",
                           f"Phone: {phone} — BLOCKED (fake pattern)")

    if not PHONE_RE.match(phone) and len(digits) != 10:
        return CheckResult("phone_validation", "block", f"Invalid format: {phone}",
                           f"Phone: {phone} — BLOCKED (invalid format)")

    return CheckResult("phone_validation", "pass", f"Valid: {phone}",
                        f"Phone: {phone} — valid format")


def check_email(lead: dict) -> CheckResult:
    email = (lead.get("email") or "").strip().lower()
    if not email:
        return CheckResult("email_validation", "block", "No email", "Email: missing — BLOCKED")

    if email in FAKE_EMAILS:
        return CheckResult("email_validation", "block", "Fake email detected",
                           f"Email: {email} — BLOCKED (fake pattern)")

    if not EMAIL_RE.match(email):
        return CheckResult("email_validation", "block", f"Invalid format: {email}",
                           f"Email: {email} — BLOCKED (invalid format)")

    return CheckResult("email_validation", "pass", f"Valid: {email}",
                        f"Email: {email} — valid format")


def check_dnc(lead: dict) -> CheckResult:
    # Placeholder — future integration with DNC registry
    return CheckResult("dnc_check", "flag",
                        "DNC check not yet implemented",
                        "DNC: not checked (placeholder)")


def check_duplicate(lead: dict, offer: dict | None) -> CheckResult:
    if not offer:
        return CheckResult("duplicate_check", "pass", "No offer specified, skipping dedup",
                           "Dedup: skipped (no offer specified)")

    email = lead.get("email")
    phone = lead.get("phone")
    offer_id = offer.get("id")

    # Check deliveries table: same lead email+phone to same buyer/offer
    # We look for leads with matching email+phone that were delivered to this offer's buyer
    params = {"select": "id"}
    filters = []

    # Find other leads with same email+phone
    if email and phone:
        matching = sb_get("leads", {
            "select": "id",
            "email": f"eq.{email}",
            "phone": f"eq.{phone}",
            "id": f"neq.{lead['id']}",
        })
        if matching:
            lead_ids = [m["id"] for m in matching]
            # Check if any of those leads were delivered to this offer
            for lid in lead_ids:
                deliveries = sb_get("deliveries", {
                    "select": "id",
                    "lead_id": f"eq.{lid}",
                    "status": "in.(sent,accepted)",
                })
                if deliveries:
                    return CheckResult("duplicate_check", "block",
                                       f"Duplicate: email+phone already delivered",
                                       f"Dedup: BLOCKED — already delivered to this offer")

    return CheckResult("duplicate_check", "pass", "No prior delivery found",
                        f"Dedup: no prior delivery to offer {offer.get('name', offer_id)}")


def check_lead_age(lead: dict) -> CheckResult:
    created = lead.get("created_at")
    if not created:
        return CheckResult("lead_age", "flag", "No created_at timestamp",
                           "Lead age: unknown — flagged")

    if isinstance(created, str):
        # Parse ISO timestamp
        created = created.replace("Z", "+00:00")
        created_dt = datetime.fromisoformat(created)
    else:
        created_dt = created

    now = datetime.now(timezone.utc)
    age_days = (now - created_dt).days

    if age_days > 90:
        return CheckResult("lead_age", "block", f"Lead is {age_days} days old (>90)",
                           f"Lead age: {age_days} days — BLOCKED (stale >90 days)")
    elif age_days > 30:
        return CheckResult("lead_age", "flag", f"Lead is {age_days} days old (>30)",
                           f"Lead age: {age_days} days — flagged (aging)")
    else:
        return CheckResult("lead_age", "pass", f"Lead is {age_days} days old",
                           f"Lead age: {age_days} days — fresh")


def check_schedule(offer: dict | None) -> CheckResult:
    if not offer:
        return CheckResult("schedule_check", "pass", "No offer, skipping schedule",
                           "Schedule: skipped (no offer)")

    schedule = (offer.get("schedule") or "").lower().strip()
    if not schedule or schedule == "7days":
        return CheckResult("schedule_check", "pass", "Offer accepts 7 days",
                           "Schedule: 7 days — OK")

    today = datetime.now(timezone.utc).weekday()  # 0=Mon, 6=Sun
    if schedule in ("m-f", "weekdays", "mon-fri") and today >= 5:
        return CheckResult("schedule_check", "block",
                           f"Offer is M-F only, today is {'Sat' if today == 5 else 'Sun'}",
                           f"Schedule: M-F only — BLOCKED (weekend)")

    return CheckResult("schedule_check", "pass", f"Schedule '{schedule}' — OK today",
                        f"Schedule: {schedule} — OK today")


# ── Main pipeline ───────────────────────────────────────────
def run_compliance(lead_id: str, offer_id: str | None = None):
    # Validate UUID
    try:
        UUID(lead_id)
    except ValueError:
        print(f"🚫 Invalid lead_id UUID: {lead_id}")
        sys.exit(1)

    # Fetch lead
    leads = sb_get("leads", {"select": "*", "id": f"eq.{lead_id}"})
    if not leads:
        print(f"🚫 Lead not found: {lead_id}")
        sys.exit(1)
    lead = leads[0]

    # Fetch offer (if provided)
    offer = None
    if offer_id:
        offers = sb_get("everflow_offers", {"select": "*", "offer_id": f"eq.{offer_id}"})
        if offers:
            offer = offers[0]
        else:
            print(f"⚠️  Offer {offer_id} not found in everflow_offers — running without offer checks")

    # Header
    offer_label = f"Offer {offer.get('name', offer_id)}" if offer else "No specific offer"
    short_id = lead_id[:8]
    print(f"\nSHIELD COMPLIANCE CHECK — Lead {short_id} → {offer_label}")
    print("─" * 55)

    # Run all checks
    checks: list[CheckResult] = [
        check_state(lead, offer),
        check_debt_type(lead),
        check_debt_amount(lead, offer),
        check_phone(lead),
        check_email(lead),
        check_dnc(lead),
        check_duplicate(lead, offer),
        check_lead_age(lead),
        check_schedule(offer),
    ]

    # Print results
    for c in checks:
        print(f"{c.icon} {c.display}")

    # Tally
    counts = {"pass": 0, "flag": 0, "block": 0}
    for c in checks:
        counts[c.result] += 1

    # Verdict
    if counts["block"] > 0:
        verdict = "BLOCKED 🚫"
    elif counts["flag"] > 0:
        verdict = "FLAGGED ⚠️"
    else:
        verdict = "APPROVED ✅"

    print("─" * 55)
    print(f"VERDICT: {verdict} ({counts['pass']} pass, {counts['flag']} flag, {counts['block']} block)")

    # Log to compliance_log
    log_entries = [
        {
            "lead_id": lead_id,
            "agent": "shield",
            "check_type": c.check_type,
            "result": c.result,
            "reason": c.reason,
        }
        for c in checks
    ]

    try:
        sb_post("compliance_log", log_entries)
        print(f"\n📝 Logged {len(log_entries)} checks to compliance_log")
    except Exception as e:
        print(f"\n⚠️  Failed to log to compliance_log: {e}")

    # Return verdict for programmatic use
    return verdict.split()[0]  # APPROVED, FLAGGED, or BLOCKED


# ── CLI entry ───────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compliance-check.py <lead_id> [offer_id]")
        sys.exit(1)

    lead_id = sys.argv[1]
    offer_id = sys.argv[2] if len(sys.argv) > 2 else None
    result = run_compliance(lead_id, offer_id)
    sys.exit(0 if result == "APPROVED" else 1)
