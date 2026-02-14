# Ringba Skill

Call routing and tracking platform for routing leads to buyers via phone.

## Capabilities
- **Call Routing** — Route inbound/outbound calls to matched buyers
- **IVR Configuration** — Set up automated call flows with qualification questions
- **Buyer Routing Rules** — Route by geo, time of day, buyer cap, priority weight
- **Call Tracking** — Track duration, disposition, recording URLs
- **Real-time Reporting** — Live call volume, conversion rates, revenue per call

## Dependencies
- Ringba account with API access
- `RINGBA_API_KEY`, `RINGBA_ACCOUNT_ID` in `.env`

## Usage
```python
from skills.ringba import RingbaClient

ringba = RingbaClient()

# Route a lead to call
ringba.initiate_call(
    lead_phone="+15551001",
    buyer_id="buyer_123",
    campaign_id="camp_456"
)

# Check call status
status = ringba.get_call_status(call_id="call_789")
```

## Used By
- **Signal** — Call-based lead delivery to buyers
