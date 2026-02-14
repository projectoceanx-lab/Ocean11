# Email Sequence: Welcome / Post-Submission

## Email 1 — Immediate (0 min after submission)

**Subject:** {{first_name}}, your debt relief options are ready
**From:** Ocean Financial <support@[ocean-domain].com>

Hi {{first_name}},

Thank you for reaching out. We've matched you with debt relief programs based on your profile.

**Your next step:** A debt specialist will call you at {{phone}} within the next few minutes to discuss your options — no obligation, completely free.

If you'd rather explore on your own first, [view your matched options here]({{offer_wall_url}}).

To your financial freedom,
Ocean Financial Team

*You're receiving this because you submitted a request at [domain]. [Unsubscribe]({{unsubscribe_url}})*

---

## Email 2 — If no call connected (4 hours)

**Subject:** {{first_name}}, we tried to reach you
**From:** Ocean Financial <support@[ocean-domain].com>

Hi {{first_name}},

We attempted to reach you by phone but couldn't connect. Your matched debt relief options are still available:

→ [View your options]({{offer_wall_url}})

Or reply to this email with a good time to call, and we'll reach out then.

Best,
Ocean Financial Team

*[Unsubscribe]({{unsubscribe_url}})*

---

## Email 3 — Follow-up (48 hours)

**Subject:** Still thinking about debt relief, {{first_name}}?
**From:** Ocean Financial <support@[ocean-domain].com>

Hi {{first_name}},

Just checking in. Many people in your situation have reduced their debt by 30-50% through the programs we recommended.

Your personalized options are still available: [See them here]({{offer_wall_url}})

No pressure — but the sooner you explore, the sooner you can start saving.

Best,
Ocean Financial Team

*[Unsubscribe]({{unsubscribe_url}})*

---

## Notes for Signal Agent
- **Warm-up required:** New domains start at 50 emails/day, increase 20% weekly
- **Sender reputation:** Monitor bounce rate (<2%), complaint rate (<0.1%)
- **Personalization:** Always use first_name, debt_amount range, state
- **Compliance:** Every email MUST have unsubscribe link (CAN-SPAM)
- **Timing:** Email 1 instant, Email 2 only if Ringba shows no connect, Email 3 at 48h
- **Kill switch:** If complaint rate >0.3%, pause ALL sends immediately
