# HEARTBEAT.md — Shield

Every 20 min:
1. Check compliance_log for pending reviews
2. Audit any recently scored leads awaiting compliance check
3. Monitor block rate — flag if trending above 20%
4. Check for regulatory updates or rule changes (weekly)

## Memory Vault
5. **Recall** — Before compliance checks, search vault for precedents:
   `python3 scripts/memory-search.py "compliance regulation" --agent shield --limit 3`
6. **Record** — After reviews, write observations to `memory/vault/obs-YYYY-MM-DD-NNN.md`

If nothing pending, reply HEARTBEAT_OK.
