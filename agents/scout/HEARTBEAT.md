# HEARTBEAT.md — Scout

Every 15 min:
1. Check for pending lead opportunities in active campaigns
2. Process any queued forms
3. Report lead counts and quality breakdown to Fury
4. Log any form changes or site issues detected

## Memory Vault
5. **Recall** — Before processing leads, search vault for relevant context:
   `python3 scripts/memory-search.py "current task context" --agent scout --limit 3`
6. **Record** — After completing work, write observations to `memory/vault/obs-YYYY-MM-DD-NNN.md`

If nothing pending, reply HEARTBEAT_OK.
