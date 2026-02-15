#!/bin/bash
# Memory Maintenance — Project Ocean
# Run daily via cron: 0 6 * * * /path/to/repo/scripts/memory-maintain.sh
# Order matters: ref → decay → promote
#
# Usage:
#   ./scripts/memory-maintain.sh           # Live run
#   ./scripts/memory-maintain.sh --dry-run # Preview all steps

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
FLAGS="${1:-}"

echo "========================================"
echo "Ocean Memory Maintenance"
echo "$(date '+%Y-%m-%d %H:%M')"
echo "========================================"
echo ""

# Step 1: Resolve references and update importance
echo "--- Step 1: Reference Tracking ---"
python3 "$SCRIPT_DIR/memory-ref.py" $FLAGS
echo ""

# Step 2: Apply decay (archive stale, extend important)
echo "--- Step 2: Decay ---"
python3 "$SCRIPT_DIR/memory-decay.py" $FLAGS
echo ""

# Step 3: Promote qualifying observations to shared
echo "--- Step 3: Promotion ---"
python3 "$SCRIPT_DIR/memory-promote.py" $FLAGS
echo ""

echo "========================================"
echo "Maintenance complete."
echo "========================================"
