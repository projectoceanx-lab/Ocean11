#!/usr/bin/env python3
"""
Memory System Test Suite — Project Ocean
Simulates real agent activity and validates the full pipeline.

Run: python3 scripts/memory-test.py
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
AGENTS = ["captain", "scout", "shield", "hawk", "forge", "watchtower"]

# Test workspace — isolated from real data
TEST_DIR = REPO_ROOT / "tests" / "memory_sandbox"

PASS = 0
FAIL = 0


def log(msg, status="INFO"):
    symbols = {"PASS": "✅", "FAIL": "❌", "INFO": "📋", "STEP": "▶️"}
    print(f"  {symbols.get(status, '•')} {msg}")


def assert_true(condition, msg):
    global PASS, FAIL
    if condition:
        PASS += 1
        log(msg, "PASS")
    else:
        FAIL += 1
        log(msg, "FAIL")


def write_obs(agent, name, tags, importance, max_age, backlinks=None, verified=False, created=None):
    """Write a test observation file."""
    vault = TEST_DIR / "agents" / agent / "memory" / "vault"
    vault.mkdir(parents=True, exist_ok=True)
    (TEST_DIR / "agents" / agent / "memory" / "archive").mkdir(parents=True, exist_ok=True)

    if created is None:
        created = datetime.now().strftime("%Y-%m-%d")
    bl = backlinks or []

    content = f"""---
tags: [{', '.join(tags)}]
importance: {importance:.2f}
created: {created}
max_age: {max_age}
source: {agent}
refs: 0
ref_by: []
backlinks: [{', '.join(bl)}]
verified: {'true' if verified else 'false'}
---
Test observation for {agent}: {name}. Tags: {', '.join(tags)}.
"""
    filepath = vault / f"{name}.md"
    filepath.write_text(content)
    return filepath


def read_importance(filepath):
    """Read importance value from an observation file."""
    text = filepath.read_text()
    for line in text.split("\n"):
        if line.strip().startswith("importance:"):
            return float(line.split(":")[1].strip())
    return None


def read_refs(filepath):
    """Read refs count from an observation file."""
    text = filepath.read_text()
    for line in text.split("\n"):
        if line.strip().startswith("refs:") and "ref_by" not in line:
            return int(line.split(":")[1].strip())
    return 0


def file_exists(filepath):
    return filepath.exists()


def run_script(script_name, env_override=None):
    """Run a memory script against the test sandbox."""
    # We need to temporarily make the scripts think REPO_ROOT is our test dir
    # Easiest: copy scripts to test dir and run from there
    result = subprocess.run(
        ["python3", str(SCRIPTS / script_name)],
        capture_output=True, text=True,
        cwd=str(TEST_DIR),
        env={**os.environ, **(env_override or {})}
    )
    return result.stdout, result.stderr, result.returncode


def setup():
    """Create clean test sandbox."""
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir(parents=True)
    (TEST_DIR / "shared" / "observations").mkdir(parents=True)
    (TEST_DIR / "shared" / "observations" / "archive").mkdir(parents=True)
    # Copy scripts with patched REPO_ROOT
    scripts_dest = TEST_DIR / "scripts"
    scripts_dest.mkdir()
    for script in SCRIPTS.glob("*.py"):
        text = script.read_text()
        # Patch REPO_ROOT to point to test dir
        text = text.replace(
            'REPO_ROOT = Path(__file__).resolve().parent.parent',
            f'REPO_ROOT = Path("{TEST_DIR}")'
        )
        (scripts_dest / script.name).write_text(text)


def run_patched(script_name, extra_args=None):
    """Run a patched script from the test sandbox."""
    cmd = ["python3", str(TEST_DIR / "scripts" / script_name)]
    if extra_args:
        cmd.extend(extra_args)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(TEST_DIR))
    return result.stdout, result.stderr, result.returncode


def teardown():
    """Clean up test sandbox."""
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)


# ─────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────

def test_reference_same_agent():
    """Same-agent backlink should boost importance by +0.1"""
    print("\n🧪 Test: Same-agent reference boost (+0.1)")
    setup()

    # Hawk writes two observations — second references first
    write_obs("hawk", "obs-2026-02-10-001", ["cpl", "facebook"], 0.5, "30d")
    write_obs("hawk", "obs-2026-02-10-002", ["cpl", "trend"], 0.5, "30d",
              backlinks=["obs-2026-02-10-001"])

    out, err, rc = run_patched("memory-ref.py")
    assert_true(rc == 0, f"memory-ref.py exits clean (rc={rc})")

    target = TEST_DIR / "agents" / "hawk" / "memory" / "vault" / "obs-2026-02-10-001.md"
    imp = read_importance(target)
    refs = read_refs(target)
    assert_true(imp == 0.6, f"Importance boosted to 0.6 (got {imp})")
    assert_true(refs == 1, f"Refs count = 1 (got {refs})")


def test_reference_cross_agent():
    """Cross-agent backlink should boost importance by +0.15"""
    print("\n🧪 Test: Cross-agent reference boost (+0.15)")
    setup()

    # Captain writes obs, Signal references it
    write_obs("captain", "obs-2026-02-10-001", ["buyer", "payout"], 0.5, "90d")
    write_obs("forge", "obs-2026-02-10-001", ["delivery", "buyer"], 0.5, "30d",
              backlinks=["obs-2026-02-10-001"])

    out, err, rc = run_patched("memory-ref.py")
    assert_true(rc == 0, f"memory-ref.py exits clean (rc={rc})")

    target = TEST_DIR / "agents" / "captain" / "memory" / "vault" / "obs-2026-02-10-001.md"
    imp = read_importance(target)
    assert_true(imp == 0.65, f"Cross-agent boost to 0.65 (got {imp})")


def test_importance_cap():
    """Importance should never exceed 1.0"""
    print("\n🧪 Test: Importance capped at 1.0")
    setup()

    # Captain writes obs with high starting importance
    write_obs("captain", "obs-2026-02-10-001", ["strategy"], 0.90, "90d")

    # Multiple agents reference it
    for agent in ["scout", "shield", "hawk", "forge", "watchtower"]:
        write_obs(agent, "obs-2026-02-10-001", ["misc"], 0.5, "30d",
                  backlinks=["obs-2026-02-10-001"])

    out, err, rc = run_patched("memory-ref.py")
    target = TEST_DIR / "agents" / "captain" / "memory" / "vault" / "obs-2026-02-10-001.md"
    imp = read_importance(target)
    assert_true(imp == 1.0, f"Importance capped at 1.0 (got {imp})")


def test_decay_low_importance():
    """Observations with importance < 0.2 should be archived regardless of age"""
    print("\n🧪 Test: Decay archives low importance (< 0.2)")
    setup()

    write_obs("hawk", "obs-2026-02-14-001", ["test"], 0.15, "30d")

    vault_file = TEST_DIR / "agents" / "hawk" / "memory" / "vault" / "obs-2026-02-14-001.md"
    archive_file = TEST_DIR / "agents" / "hawk" / "memory" / "archive" / "obs-2026-02-14-001.md"

    out, err, rc = run_patched("memory-decay.py")
    assert_true(rc == 0, f"memory-decay.py exits clean (rc={rc})")
    assert_true(not file_exists(vault_file), "Low-importance obs removed from vault")
    assert_true(file_exists(archive_file), "Low-importance obs moved to archive")


def test_decay_respects_high_importance():
    """Expired but high-importance (with refs to avoid neglect) obs should get extended"""
    print("\n🧪 Test: Decay extends high-importance expired obs")
    setup()

    # 45 days old with 30d max_age, importance 0.75, BUT has refs (so no neglect penalty)
    old_date = (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d")
    vault = TEST_DIR / "agents" / "shield" / "memory" / "vault"
    vault.mkdir(parents=True, exist_ok=True)
    (TEST_DIR / "agents" / "shield" / "memory" / "archive").mkdir(parents=True, exist_ok=True)
    content = f"""---
tags: [compliance]
importance: 0.75
created: {old_date}
max_age: 30d
source: shield
refs: 2
ref_by: [scout/obs-2026-02-01-001, captain/obs-2026-02-01-001]
backlinks: []
verified: false
---
Test observation with refs — should survive decay.
"""
    filepath = vault / "obs-2026-01-01-001.md"
    filepath.write_text(content)

    out, err, rc = run_patched("memory-decay.py", ["--verbose"])
    assert_true(file_exists(filepath), "High-importance obs with refs still in vault")

    # Check max_age was extended (30d × 1.5 = 45d)
    text = filepath.read_text()
    assert_true("45d" in text, f"Max age extended to 45d")


def test_decay_archives_expired_low():
    """Expired + low importance should be archived"""
    print("\n🧪 Test: Decay archives expired + low importance")
    setup()

    old_date = (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d")
    write_obs("watchtower", "obs-old-001", ["system"], 0.3, "30d", created=old_date)

    vault_file = TEST_DIR / "agents" / "watchtower" / "memory" / "vault" / "obs-old-001.md"
    archive_file = TEST_DIR / "agents" / "watchtower" / "memory" / "archive" / "obs-old-001.md"

    out, err, rc = run_patched("memory-decay.py")
    assert_true(not file_exists(vault_file), "Expired low-importance removed from vault")
    assert_true(file_exists(archive_file), "Expired low-importance moved to archive")


def test_neglect_penalty():
    """Unreferenced observations > 14 days old should lose importance"""
    print("\n🧪 Test: Neglect penalty on unreferenced obs")
    setup()

    old_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    write_obs("scout", "obs-old-001", ["leads"], 0.5, "90d", created=old_date)

    out, err, rc = run_patched("memory-decay.py", ["--verbose"])
    target = TEST_DIR / "agents" / "scout" / "memory" / "vault" / "obs-old-001.md"
    imp = read_importance(target)
    # 30 days old, unreferenced: (30-14)//14 = 1 neglect period → -0.1
    assert_true(imp == 0.4, f"Neglect penalty applied: 0.5 → 0.4 (got {imp})")


def test_promotion_earned():
    """Only observations with earned importance >= 0.8 get promoted"""
    print("\n🧪 Test: Promotion requires earned importance >= 0.8")
    setup()

    write_obs("captain", "obs-2026-02-10-001", ["strategy"], 0.5, "90d")
    write_obs("captain", "obs-2026-02-10-002", ["strategy"], 0.85, "90d")

    out, err, rc = run_patched("memory-promote.py")
    shared_low = TEST_DIR / "shared" / "observations" / "captain-obs-2026-02-10-001.md"
    shared_high = TEST_DIR / "shared" / "observations" / "captain-obs-2026-02-10-002.md"

    assert_true(not file_exists(shared_low), "0.5 importance NOT promoted")
    assert_true(file_exists(shared_high), "0.85 importance promoted to shared")


def test_promotion_verified_lower_threshold():
    """Verified + importance >= 0.6 should also promote"""
    print("\n🧪 Test: Verified obs promotes at lower threshold (0.6)")
    setup()

    write_obs("shield", "obs-2026-02-10-001", ["compliance"], 0.65, "180d", verified=True)

    out, err, rc = run_patched("memory-promote.py")
    shared = TEST_DIR / "shared" / "observations" / "shield-obs-2026-02-10-001.md"
    assert_true(file_exists(shared), "Verified + 0.65 importance promoted")


def test_search_ranks_by_importance():
    """Search should rank higher-importance observations first"""
    print("\n🧪 Test: Search ranks by importance")
    setup()

    write_obs("hawk", "obs-2026-02-10-001", ["cpl", "facebook", "insurance"], 0.3, "30d")
    write_obs("hawk", "obs-2026-02-10-002", ["cpl", "facebook", "insurance"], 0.9, "30d")

    out, err, rc = run_patched("memory-search.py", ["CPL insurance facebook", "--all", "--json"])
    assert_true(rc == 0, f"memory-search.py exits clean (rc={rc})")

    import json
    try:
        data = json.loads(out)
        results = data.get("results", [])
        assert_true(len(results) == 2, f"Found 2 results (got {len(results)})")
        if len(results) == 2:
            assert_true(
                results[0]["importance"] > results[1]["importance"],
                f"Higher importance ranked first ({results[0]['importance']} > {results[1]['importance']})"
            )
    except json.JSONDecodeError:
        assert_true(False, f"Search output is valid JSON")


def test_full_pipeline():
    """End-to-end: write → reference → decay → promote"""
    print("\n🧪 Test: Full pipeline (write → ref → decay → promote)")
    setup()

    # Day 1: Captain writes a buyer insight
    write_obs("captain", "obs-2026-02-01-001", ["buyer", "payout"], 0.5, "90d",
              created=(datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"))

    # Day 3: Signal references it
    write_obs("forge", "obs-2026-02-03-001", ["delivery", "buyer"], 0.5, "30d",
              backlinks=["obs-2026-02-01-001"],
              created=(datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d"))

    # Day 5: Shield also references it
    write_obs("shield", "obs-2026-02-05-001", ["compliance", "buyer"], 0.5, "180d",
              backlinks=["obs-2026-02-01-001"],
              created=(datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d"))

    # Day 7: Hawk references it too
    write_obs("hawk", "obs-2026-02-07-001", ["spend", "buyer"], 0.5, "30d",
              backlinks=["obs-2026-02-01-001"],
              created=(datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"))

    # Also write a throwaway obs that nobody references
    write_obs("watchtower", "obs-2026-02-01-002", ["system", "noise"], 0.5, "14d",
              created=(datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"))

    # Run ref tracking
    run_patched("memory-ref.py")

    target = TEST_DIR / "agents" / "captain" / "memory" / "vault" / "obs-2026-02-01-001.md"
    imp = read_importance(target)
    refs = read_refs(target)

    # 3 cross-agent references: 3 × 0.15 = 0.45, starting at 0.5 → 0.95
    assert_true(imp == 0.95, f"Captain obs importance after 3 cross-refs: 0.95 (got {imp})")
    assert_true(refs == 3, f"Captain obs has 3 refs (got {refs})")

    # Run decay
    run_patched("memory-decay.py")

    # Watchtower's noise obs: 20 days old, 14d max_age, unreferenced, neglect penalty
    # Neglect: (20-14)//14 = 0 periods (just barely), but past max_age with default importance
    # After neglect: 0.5 - 0.0 = 0.5, but past 14d max_age with importance < 0.7 → flagged or archived
    wt_vault = TEST_DIR / "agents" / "watchtower" / "memory" / "vault" / "obs-2026-02-01-002.md"
    wt_archive = TEST_DIR / "agents" / "watchtower" / "memory" / "archive" / "obs-2026-02-01-002.md"
    # importance 0.5 after neglect, past max_age → should be archived (< 0.4 after penalty)
    # Actually: 20d old, unreferenced, neglect periods = (20-14)//14 = 0. Still 0.5.
    # But past 14d max_age with importance 0.4-0.7 → flagged, not archived. Let me adjust expectation.
    # Neglect: 0 periods (need full 14-day blocks past day 14). So importance stays 0.5.
    # 0.5 is in 0.4-0.7 range, past max_age → flagged for review (not archived)
    assert_true(file_exists(wt_vault), "Noise obs flagged for review, not archived yet (mid-importance)")

    # Run promote
    run_patched("memory-promote.py")

    # Captain's obs at 0.95 should be promoted
    shared = TEST_DIR / "shared" / "observations" / "captain-obs-2026-02-01-001.md"
    assert_true(file_exists(shared), "Captain's high-ref obs promoted to shared")

    # Forge/Shield/Hawk obs should NOT be promoted (importance 0.5)
    for agent, day in [("forge", "03"), ("shield", "05"), ("hawk", "07")]:
        shared_other = TEST_DIR / "shared" / "observations" / f"{agent}-obs-2026-02-{day}-001.md"
        assert_true(not file_exists(shared_other), f"{agent}'s obs NOT promoted (importance 0.5)")


# ─────────────────────────────────────────
# RUN
# ─────────────────────────────────────────

def main():
    global PASS, FAIL
    print("=" * 50)
    print("Ocean Memory System — Test Suite")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    tests = [
        test_reference_same_agent,
        test_reference_cross_agent,
        test_importance_cap,
        test_decay_low_importance,
        test_decay_respects_high_importance,
        test_decay_archives_expired_low,
        test_neglect_penalty,
        test_promotion_earned,
        test_promotion_verified_lower_threshold,
        test_search_ranks_by_importance,
        test_full_pipeline,
    ]

    for test in tests:
        try:
            test()
        except Exception as e:
            FAIL += 1
            log(f"EXCEPTION in {test.__name__}: {e}", "FAIL")

    teardown()

    print("\n" + "=" * 50)
    print(f"Results: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    if FAIL == 0:
        print("🎯 All tests passed!")
    else:
        print("⚠️  Some tests failed.")
    print("=" * 50)
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
