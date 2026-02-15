#!/usr/bin/env python3
"""
🔍 Scout — Orchestrator Pipeline
The brain of Project Ocean. Takes a lead through every step:
  Ingest → Enrich → Compliance → Route → Fill → Record → Report

Usage:
    python3 scripts/pipeline.py --lead-id <UUID>
    python3 scripts/pipeline.py --lead-id <UUID> --skip-enrichment
    python3 scripts/pipeline.py --lead-id <UUID> --dry-run
    python3 scripts/pipeline.py --batch --status new --limit 10
"""

import argparse
import json
import os
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

import httpx
from dotenv import load_dotenv

# ── Project root & env ──────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

# Offer → filler mapping
JGW_OFFERS = {4592, 4633, 4591, 4737}
FDR_NDR_OFFERS = {4930, 4905, 4836, 4632, 4528, 4731}

AGENT_NAME = "pipeline"


# ── Supabase helpers ────────────────────────────────────────
def sb_get(table: str, params: dict) -> list[dict]:
    r = httpx.get(f"{SUPABASE_URL}/rest/v1/{table}", headers=HEADERS,
                  params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def sb_patch(table: str, params: dict, data: dict) -> list[dict]:
    r = httpx.patch(f"{SUPABASE_URL}/rest/v1/{table}", headers=HEADERS,
                    params=params, json=data, timeout=15)
    r.raise_for_status()
    return r.json()


def sb_post(table: str, data: dict | list) -> list[dict]:
    r = httpx.post(f"{SUPABASE_URL}/rest/v1/{table}", headers=HEADERS,
                   json=data, timeout=15)
    r.raise_for_status()
    return r.json()


def log_activity(action: str, details: dict):
    """Log to agent_activity table."""
    try:
        sb_post("agent_activity", {
            "agent_name": AGENT_NAME,
            "action": action,
            "details": details,
        })
    except Exception as e:
        print(f"  ⚠️  Failed to log activity: {e}")


def update_lead_status(lead_id: str, status: str):
    """Update lead status in DB."""
    try:
        sb_patch("leads", {"id": f"eq.{lead_id}"}, {"status": status})
    except Exception as e:
        print(f"  ⚠️  Failed to update lead status to '{status}': {e}")


# ── Step 1: Ingest ──────────────────────────────────────────
def step_ingest(lead_id: str) -> dict | None:
    """Fetch lead from Supabase by ID."""
    print(f"\n{'='*60}")
    print(f"🔍 PIPELINE — Lead {lead_id[:8]}...")
    print(f"{'='*60}")
    print(f"\n① INGEST")

    try:
        UUID(lead_id)
    except ValueError:
        print(f"  🚫 Invalid UUID: {lead_id}")
        log_activity("ingest_failed", {"lead_id": lead_id, "error": "invalid UUID"})
        return None

    leads = sb_get("leads", {"select": "*", "id": f"eq.{lead_id}"})
    if not leads:
        print(f"  🚫 Lead not found: {lead_id}")
        log_activity("ingest_failed", {"lead_id": lead_id, "error": "not found"})
        return None

    lead = leads[0]
    name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
    print(f"  ✅ Found: {name} | {lead.get('state', '??')} | "
          f"${float(lead.get('debt_amount') or 0):,.0f} | status={lead['status']}")
    log_activity("ingest", {"lead_id": lead_id, "name": name, "status": lead["status"]})
    return lead


# ── Step 2: Enrich ──────────────────────────────────────────
def step_enrich(lead: dict, skip: bool = False) -> dict:
    """Enrich lead with FastDebt API (PLACEHOLDER)."""
    print(f"\n② ENRICH")
    lead_id = lead["id"]

    if skip:
        print(f"  ⏭️  Skipped (--skip-enrichment)")
        log_activity("enrich_skipped", {"lead_id": lead_id})
        return lead

    # PLACEHOLDER — FastDebt API not yet integrated
    print(f"  ⏳ Enrichment pending — FastDebt API not yet connected")
    print(f"     (Pipeline continues without enrichment data)")
    log_activity("enrich_pending", {"lead_id": lead_id, "reason": "FastDebt API not connected"})

    # Update status to enriched (even without enrichment, so pipeline progresses)
    update_lead_status(lead_id, "enriched")
    lead["status"] = "enriched"
    return lead


def enrich_lead_fastdebt(lead: dict) -> dict:
    """
    PLACEHOLDER: Call FastDebt API to get debt composition.
    Returns enriched lead data with debt breakdown.

    Expected response format:
    {
        "debt_composition": {
            "credit_card": 15000,
            "personal_loan": 5000,
            "medical": 3000
        },
        "total_verified_debt": 23000,
        "creditor_count": 4,
        "avg_account_age_months": 18
    }
    """
    # TODO: Implement when FastDebt API credentials are available
    # api_url = os.environ.get("FASTDEBT_API_URL")
    # api_key = os.environ.get("FASTDEBT_API_KEY")
    # response = httpx.post(f"{api_url}/enrich", headers={"Authorization": api_key},
    #                       json={"phone": lead["phone"], "ssn_last4": lead.get("ssn_last4")})
    raise NotImplementedError("FastDebt API integration pending")


# ── Step 3: Compliance ──────────────────────────────────────
def step_compliance(lead: dict, offer_id: str | None = None) -> str:
    """
    Run Shield compliance check. Returns 'APPROVED', 'FLAGGED', or 'BLOCKED'.
    """
    print(f"\n③ COMPLIANCE")
    lead_id = lead["id"]

    try:
        # Import Shield's compliance checker directly
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "compliance_check",
            PROJECT_ROOT / "scripts" / "compliance-check.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        verdict = mod.run_compliance(lead_id, offer_id)
        log_activity("compliance_check", {
            "lead_id": lead_id,
            "offer_id": offer_id,
            "verdict": verdict,
        })

        if verdict == "BLOCKED":
            print(f"  🚫 BLOCKED — updating lead status to 'rejected'")
            update_lead_status(lead_id, "rejected")
        elif verdict == "FLAGGED":
            print(f"  ⚠️  FLAGGED — continuing with caution")
        else:
            print(f"  ✅ APPROVED")

        return verdict

    except FileNotFoundError:
        print(f"  ⚠️  compliance-check.py not found — skipping (DANGER: no compliance!)")
        log_activity("compliance_error", {"lead_id": lead_id, "error": "script not found"})
        return "FLAGGED"
    except Exception as e:
        print(f"  ❌ Compliance check failed: {e}")
        log_activity("compliance_error", {"lead_id": lead_id, "error": str(e)})
        # Fail safe: treat errors as BLOCKED
        return "BLOCKED"


# ── Step 4: Route ───────────────────────────────────────────
def step_route(lead: dict) -> list[dict]:
    """
    Route lead to best offers. Returns list of eligible offers sorted by CPA desc.
    """
    print(f"\n④ ROUTE")
    lead_id = lead["id"]

    try:
        # Import router internals
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "lead_router",
            PROJECT_ROOT / "scripts" / "lead-router.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        offers = mod.fetch_active_offers()
        lead_channel = mod.SOURCE_TO_CHANNEL.get(lead.get("source", ""), "web")
        lead_state = (lead.get("state") or "").upper()
        lead_debt = float(lead.get("debt_amount") or 0)
        weekday = mod.is_weekday()

        eligible = []
        for o in offers:
            oid = o["offer_id"]
            reason = None

            # Channel match
            ch = o["channel"]
            if ch != "any" and ch != lead_channel:
                reason = f"channel mismatch"

            # State exclusion
            if not reason:
                excl = o.get("excluded_states") or []
                if lead_state and lead_state in [s.upper() for s in excl]:
                    reason = f"state excluded ({lead_state})"

            # Schedule
            if not reason:
                sched = (o.get("schedule") or "7days").strip()
                if sched in mod.SCHEDULE_WEEKDAY_ONLY and not weekday:
                    reason = "weekend"

            # Min debt
            if not reason:
                min_debt = o.get("min_debt_amount")
                if min_debt and lead_debt < float(min_debt):
                    reason = f"min debt"

            # Cap check
            if not reason:
                cap_info = mod.check_cap(oid)
                if not cap_info.get("can_submit"):
                    reason = cap_info.get("reason", "cap reached")

            if not reason:
                eligible.append(o)

        # Sort by CPA descending
        eligible.sort(key=lambda x: float(x["cpa"]), reverse=True)

        if eligible:
            print(f"  ✅ {len(eligible)} eligible offer(s):")
            for i, o in enumerate(eligible[:5], 1):
                print(f"     {i}. Offer {o['offer_id']} — {o['buyer_short']} ${float(o['cpa']):.0f}")
            update_lead_status(lead_id, "scored")
        else:
            print(f"  ⚠️  No eligible offers found")

        log_activity("route", {
            "lead_id": lead_id,
            "eligible_count": len(eligible),
            "top_offer": eligible[0]["offer_id"] if eligible else None,
        })
        return eligible

    except Exception as e:
        print(f"  ❌ Routing failed: {e}")
        log_activity("route_error", {"lead_id": lead_id, "error": str(e)})
        return []


# ── Step 5: Fill ────────────────────────────────────────────
def step_fill(lead: dict, offer: dict, dry_run: bool = False) -> bool:
    """
    Fill the appropriate form based on offer ID.
    Returns True if submission succeeded.
    """
    offer_id = int(offer["offer_id"])
    buyer = offer.get("buyer_short", "unknown")
    lead_id = lead["id"]

    print(f"\n⑤ FILL — Offer {offer_id} ({buyer})")

    if dry_run:
        print(f"  🏜️  DRY RUN — skipping form submission")
        log_activity("fill_dry_run", {"lead_id": lead_id, "offer_id": offer_id})
        return True

    # Determine which filler to use
    if offer_id in JGW_OFFERS:
        filler_script = PROJECT_ROOT / "scripts" / "jgw-fill.py"
        filler_name = "JGW"
    elif offer_id in FDR_NDR_OFFERS:
        filler_script = PROJECT_ROOT / "scripts" / "fdr-ndr-fill.py"
        filler_name = "FDR/NDR"
    else:
        print(f"  ⚠️  No filler mapped for offer {offer_id} — skipping")
        log_activity("fill_no_filler", {"lead_id": lead_id, "offer_id": offer_id})
        return False

    if not filler_script.exists():
        print(f"  ⚠️  {filler_name} filler not found at {filler_script.name} — skipping")
        log_activity("fill_script_missing", {
            "lead_id": lead_id, "offer_id": offer_id, "filler": filler_name
        })
        return False

    try:
        print(f"  🔧 Running {filler_name} filler ({filler_script.name})...")
        result = subprocess.run(
            [sys.executable, str(filler_script), "--lead-id", lead_id, "--submit", "--headless"],
            capture_output=True, text=True, timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode == 0:
            print(f"  ✅ Form submitted successfully")
            log_activity("fill_success", {
                "lead_id": lead_id, "offer_id": offer_id, "filler": filler_name
            })
            return True
        else:
            print(f"  ❌ Filler exited with code {result.returncode}")
            if result.stderr:
                print(f"     stderr: {result.stderr[:300]}")
            log_activity("fill_failed", {
                "lead_id": lead_id, "offer_id": offer_id,
                "exit_code": result.returncode,
                "stderr": result.stderr[:500] if result.stderr else None,
            })
            return False

    except subprocess.TimeoutExpired:
        print(f"  ❌ Filler timed out (120s)")
        log_activity("fill_timeout", {"lead_id": lead_id, "offer_id": offer_id})
        return False
    except Exception as e:
        print(f"  ❌ Filler error: {e}")
        log_activity("fill_error", {"lead_id": lead_id, "offer_id": offer_id, "error": str(e)})
        return False


# ── Step 6: Record ──────────────────────────────────────────
def step_record(lead: dict, offer: dict, success: bool, dry_run: bool = False):
    """Log submission to offer_submissions table."""
    print(f"\n⑥ RECORD")
    lead_id = lead["id"]
    offer_id = offer["offer_id"]

    if dry_run:
        print(f"  🏜️  DRY RUN — skipping DB record")
        return

    submission = {
        "lead_id": lead_id,
        "offer_id": int(offer_id),
        "buyer": offer.get("buyer_short", "unknown"),
        "offer_name": offer.get("offer_name", ""),
        "cpa": float(offer.get("cpa", 0)),
        "status": "submitted" if success else "failed",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        sb_post("offer_submissions", submission)
        print(f"  ✅ Recorded submission: offer {offer_id} = {'submitted' if success else 'failed'}")
    except Exception as e:
        # Table might not exist yet — log but don't crash
        print(f"  ⚠️  Failed to record submission (table may not exist): {e}")
        log_activity("record_error", {"lead_id": lead_id, "error": str(e)})

    if success:
        update_lead_status(lead_id, "delivered")


# ── Step 7: Report ──────────────────────────────────────────
def step_report(lead: dict, result: dict):
    """Print pipeline summary."""
    print(f"\n⑦ REPORT")
    print(f"{'─'*60}")
    name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
    print(f"  Lead:       {name} ({lead['id'][:8]}...)")
    print(f"  State:      {lead.get('state', '??')}")
    print(f"  Debt:       ${float(lead.get('debt_amount') or 0):,.0f}")
    print(f"  Compliance: {result.get('compliance', 'N/A')}")
    print(f"  Offers:     {result.get('eligible_count', 0)} eligible")

    if result.get("submitted_offer"):
        o = result["submitted_offer"]
        print(f"  Submitted:  Offer {o['offer_id']} — {o.get('buyer_short', '?')} ${float(o.get('cpa', 0)):.0f}")
    elif result.get("outcome"):
        print(f"  Outcome:    {result['outcome']}")

    print(f"  Final:      {result.get('final_status', lead.get('status', '?'))}")
    print(f"{'─'*60}")

    duration = result.get("duration_sec", 0)
    print(f"  ⏱️  Completed in {duration:.1f}s")
    print()


# ── Main pipeline ───────────────────────────────────────────
def process_lead(lead_id: str, skip_enrichment: bool = False, dry_run: bool = False) -> dict:
    """
    Run the full pipeline for a single lead.
    Returns a result dict with outcome info.
    """
    start = datetime.now(timezone.utc)
    result = {"lead_id": lead_id, "outcome": None, "final_status": None}

    # 1. Ingest
    lead = step_ingest(lead_id)
    if not lead:
        result["outcome"] = "ingest_failed"
        return result

    # 2. Enrich
    lead = step_enrich(lead, skip=skip_enrichment)

    # 3. Compliance (lead-level, no specific offer yet)
    verdict = step_compliance(lead)
    result["compliance"] = verdict

    if verdict == "BLOCKED":
        result["outcome"] = "blocked_by_compliance"
        result["final_status"] = "rejected"
        result["duration_sec"] = (datetime.now(timezone.utc) - start).total_seconds()
        step_report(lead, result)
        return result

    # 4. Route
    eligible = step_route(lead)
    result["eligible_count"] = len(eligible)

    if not eligible:
        result["outcome"] = "no_eligible_offers"
        result["final_status"] = lead.get("status", "enriched")
        log_activity("no_eligible_offers", {"lead_id": lead_id})
        result["duration_sec"] = (datetime.now(timezone.utc) - start).total_seconds()
        step_report(lead, result)
        return result

    # 5. Try offers in order (highest CPA first), run offer-specific compliance
    submitted = False
    for offer in eligible:
        offer_id_str = str(offer["offer_id"])

        # Offer-specific compliance check
        offer_verdict = step_compliance(lead, offer_id=offer_id_str)
        if offer_verdict == "BLOCKED":
            print(f"  ⏭️  Offer {offer['offer_id']} blocked by compliance — trying next")
            continue

        # 5. Fill
        success = step_fill(lead, offer, dry_run=dry_run)

        # 6. Record
        step_record(lead, offer, success, dry_run=dry_run)

        if success:
            result["submitted_offer"] = offer
            result["outcome"] = "delivered" if not dry_run else "dry_run_success"
            result["final_status"] = "delivered" if not dry_run else lead.get("status")
            submitted = True
            break
        else:
            print(f"  ⏭️  Offer {offer['offer_id']} fill failed — trying next")
            continue

    if not submitted:
        result["outcome"] = "all_offers_failed"
        result["final_status"] = lead.get("status", "scored")
        log_activity("all_offers_failed", {"lead_id": lead_id, "tried": len(eligible)})

    result["duration_sec"] = (datetime.now(timezone.utc) - start).total_seconds()

    # 7. Report
    step_report(lead, result)
    return result


# ── Batch mode ──────────────────────────────────────────────
def process_batch(status: str = "new", limit: int = 10,
                  skip_enrichment: bool = False, dry_run: bool = False):
    """Process a batch of leads by status."""
    print(f"\n{'='*60}")
    print(f"🔍 BATCH MODE — status='{status}' limit={limit}")
    print(f"{'='*60}")

    leads = sb_get("leads", {
        "select": "id",
        "status": f"eq.{status}",
        "order": "created_at.asc",
        "limit": str(limit),
    })

    if not leads:
        print(f"\n  No leads found with status='{status}'")
        log_activity("batch_empty", {"status": status})
        return

    print(f"\n  Found {len(leads)} lead(s) to process\n")
    log_activity("batch_start", {"status": status, "count": len(leads)})

    results = {"delivered": 0, "rejected": 0, "failed": 0, "no_offers": 0}

    for i, row in enumerate(leads, 1):
        lead_id = row["id"]
        print(f"\n{'━'*60}")
        print(f"  BATCH [{i}/{len(leads)}]")
        print(f"{'━'*60}")

        try:
            r = process_lead(lead_id, skip_enrichment=skip_enrichment, dry_run=dry_run)
            outcome = r.get("outcome", "unknown")

            if outcome in ("delivered", "dry_run_success"):
                results["delivered"] += 1
            elif outcome == "blocked_by_compliance":
                results["rejected"] += 1
            elif outcome == "no_eligible_offers":
                results["no_offers"] += 1
            else:
                results["failed"] += 1

        except Exception as e:
            print(f"\n  💥 UNHANDLED ERROR for lead {lead_id[:8]}: {e}")
            traceback.print_exc()
            log_activity("pipeline_crash", {"lead_id": lead_id, "error": str(e)})
            results["failed"] += 1
            continue  # Never crash in batch mode

    # Batch summary
    print(f"\n{'='*60}")
    print(f"📊 BATCH SUMMARY")
    print(f"{'='*60}")
    print(f"  Total:      {len(leads)}")
    print(f"  Delivered:  {results['delivered']}")
    print(f"  Rejected:   {results['rejected']}")
    print(f"  No offers:  {results['no_offers']}")
    print(f"  Failed:     {results['failed']}")
    print()

    log_activity("batch_complete", {
        "total": len(leads),
        **results,
    })


# ── CLI ─────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="🔍 Scout Pipeline — Lead-to-Revenue Orchestrator"
    )
    parser.add_argument("--lead-id", type=str, help="Process a specific lead by UUID")
    parser.add_argument("--batch", action="store_true", help="Process batch of leads")
    parser.add_argument("--status", type=str, default="new",
                        help="Lead status to filter in batch mode (default: new)")
    parser.add_argument("--limit", type=int, default=10,
                        help="Max leads to process in batch mode (default: 10)")
    parser.add_argument("--skip-enrichment", action="store_true",
                        help="Skip FastDebt enrichment step")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run full pipeline but don't submit forms")

    args = parser.parse_args()

    if not args.lead_id and not args.batch:
        parser.print_help()
        print("\n❌ Provide --lead-id <UUID> or --batch")
        sys.exit(1)

    if args.lead_id and args.batch:
        print("❌ Cannot use --lead-id and --batch together")
        sys.exit(1)

    if args.batch:
        process_batch(
            status=args.status,
            limit=args.limit,
            skip_enrichment=args.skip_enrichment,
            dry_run=args.dry_run,
        )
    else:
        result = process_lead(
            lead_id=args.lead_id,
            skip_enrichment=args.skip_enrichment,
            dry_run=args.dry_run,
        )
        # Exit code: 0 if delivered/dry_run, 1 otherwise
        outcome = result.get("outcome", "")
        sys.exit(0 if outcome in ("delivered", "dry_run_success") else 1)


if __name__ == "__main__":
    main()
