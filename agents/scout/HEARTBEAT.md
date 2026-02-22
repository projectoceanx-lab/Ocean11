# HEARTBEAT.md — Scout

## Memory Vault
5. **Recall** — Before processing leads, search vault for relevant context:
   `python3 scripts/memory-search.py "current task context" --agent scout --limit 3`
6. **Record** — After completing work, write observations to `memory/vault/obs-YYYY-MM-DD-NNN.md`

If nothing pending, reply HEARTBEAT_OK.
