# HEARTBEAT.md — Forge

Every 6 hour:
1. Check active funnel/CRO tasks and pending spec requests.
2. Review latest conversion signals (drop-offs, step friction, offer mismatch).
3. Validate that any proposed test includes success and kill criteria.
4. Confirm compliance review path is defined for copy or UX changes.
5. Report prioritized CRO actions to Fury.

## Memory Vault
6. **Recall** — Before making recommendations, search vault for prior outcomes:
   `python3 scripts/memory-search.py "funnel test outcomes" --agent forge --limit 3`
7. **Record** — After meaningful findings, write observations to `memory/vault/obs-YYYY-MM-DD-NNN.md`.

If nothing actionable changed, reply HEARTBEAT_OK.
