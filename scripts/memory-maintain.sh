#!/bin/bash
# Memory Maintenance — Project Ocean
# Smart maintenance: skips if nothing changed since last run.
#
# Usage:
#   ./scripts/memory-maintain.sh           # Smart run (skip if no changes)
#   ./scripts/memory-maintain.sh --force   # Force full run
#   ./scripts/memory-maintain.sh --dry-run # Preview all steps

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
STAMP_FILE="$SCRIPT_DIR/.last-maintenance"
FLAGS="${1:-}"

echo "========================================"
echo "Ocean Memory Maintenance"
echo "$(date '+%Y-%m-%d %H:%M')"
echo "========================================"

# Smart skip: check if any vault files changed since last run
if [ "$FLAGS" != "--force" ] && [ "$FLAGS" != "--dry-run" ] && [ -f "$STAMP_FILE" ]; then
    LAST_RUN=$(cat "$STAMP_FILE")
    CHANGED=$(find "$REPO_DIR/agents"/*/memory/vault -name "*.md" -newer "$STAMP_FILE" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$CHANGED" = "0" ]; then
        echo ""
        echo "No vault changes since last run ($LAST_RUN). Skipping."
        echo "Use --force to run anyway."
        echo "========================================"
        exit 0
    fi
    echo ""
    echo "$CHANGED file(s) changed since $LAST_RUN"
fi

echo ""

# Count observations for stats
TOTAL_OBS=$(find "$REPO_DIR/agents"/*/memory/vault -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
SHARED_OBS=$(find "$REPO_DIR/shared/observations" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
ARCHIVED=$(find "$REPO_DIR/agents"/*/memory/archive -name "*.md" 2>/dev/null | wc -l | tr -d ' ' || echo 0)
echo "Vault: $TOTAL_OBS active | Shared: $SHARED_OBS promoted | Archive: $ARCHIVED decayed"
echo ""

# Map maintain flags to script-appropriate flags
SCRIPT_FLAGS=""
if [ "$FLAGS" = "--dry-run" ]; then
    SCRIPT_FLAGS="--dry-run"
fi

# Step 1: Resolve references and update importance
echo "--- Step 1: Reference Tracking ---"
python3 "$SCRIPT_DIR/memory-ref.py" $SCRIPT_FLAGS
echo ""

# Step 2: Apply decay (archive stale, extend important)
echo "--- Step 2: Decay ---"
python3 "$SCRIPT_DIR/memory-decay.py" $SCRIPT_FLAGS
echo ""

# Step 3: Promote qualifying observations to shared
echo "--- Step 3: Promotion ---"
python3 "$SCRIPT_DIR/memory-promote.py" $SCRIPT_FLAGS
echo ""

# Update timestamp (unless dry-run)
if [ "$FLAGS" != "--dry-run" ]; then
    date '+%Y-%m-%d %H:%M' > "$STAMP_FILE"
fi

# Post-run stats
TOTAL_OBS_AFTER=$(find "$REPO_DIR/agents"/*/memory/vault -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
SHARED_AFTER=$(find "$REPO_DIR/shared/observations" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
ARCHIVED_AFTER=$(find "$REPO_DIR/agents"/*/memory/archive -name "*.md" 2>/dev/null | wc -l | tr -d ' ' || echo 0)

echo "========================================"
echo "After: Vault $TOTAL_OBS_AFTER | Shared $SHARED_AFTER | Archive $ARCHIVED_AFTER"
echo "Maintenance complete."
echo "========================================"
