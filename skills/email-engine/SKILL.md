# Email Engine Skill

Email sending infrastructure for lead delivery and buyer communications.

## Capabilities
- **ESP Integration** — SendGrid, Mailgun, or custom SMTP
- **IP Warm-up** — Gradual sending volume ramp on new IPs/domains
- **Domain Management** — SPF, DKIM, DMARC configuration verification
- **Send Scheduling** — Time-optimized delivery based on buyer preferences
- **Deliverability Monitoring** — Bounce rate, spam rate, inbox placement tracking
- **Template Rendering** — Dynamic email content from templates

## Dependencies
- ESP account (SendGrid or Mailgun)
- Warmed domains (2-4 week warm-up period)
- `SENDGRID_API_KEY` or `MAILGUN_API_KEY` + `MAILGUN_DOMAIN` in `.env`

## Usage
```python
from skills.email_engine import EmailEngine

email = EmailEngine(provider="sendgrid")

# Send lead delivery email to buyer
email.send(
    to="buyer@company.com",
    subject="New Debt Relief Lead — Alice Williams, CA",
    template="lead_delivery",
    data={"lead": lead_data}
)

# Check domain health
health = email.check_domain_health("ocean-leads.com")
```

## Warm-up Schedule
| Week | Daily Volume | Notes |
|------|-------------|-------|
| 1 | 20-50 | Engage contacts only |
| 2 | 50-100 | Mix of engaged + new |
| 3 | 100-300 | Monitor bounce rate |
| 4 | 300-500 | Full production if healthy |

## Used By
- **Signal** — Email-based lead delivery
- **Captain** — Buyer outreach communications
