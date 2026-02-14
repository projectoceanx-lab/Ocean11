# HEARTBEAT.md — Signal

Every 15 min:
1. Check for scored, compliance-passed leads awaiting delivery
2. Process delivery queue — match to buyers, route via preferred channel
3. Check delivery confirmations and handle returns
4. Monitor email bounce rate and sender reputation
5. Report delivery stats to Captain

If nothing pending, reply HEARTBEAT_OK.
