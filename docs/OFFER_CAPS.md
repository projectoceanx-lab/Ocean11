# Offer Caps & Restrictions — Everflow (RevvMind)

_Source: Everflow offers page + AK direct. Caps updated weekly (Monday 9AM IST cron)._
_Last updated: Feb 15, 2026_

## ⚠️ CRITICAL BUSINESS LOGIC — How Caps Work

```
Our Form Fill → Advertiser checks (dedup + quality) → Accept or Reject
      ↓                                                      ↓
  "Submission"                                     Everflow pixel fires
  (our count)                                              ↓
                                                    "Conversion"
                                                  (COUNTS TOWARD CAP)
```

- **Submissions ≠ Conversions.** Not every fill succeeds. Buyers check for duplicates, quality, state eligibility.
- **Cap = max confirmed conversions** (Everflow postbacks), NOT submissions.
- **Postbacks can be delayed** — sometimes hours or next day.
- **We track both:** submissions (to avoid flooding) and conversions (real cap count).
- **Safety buffer:** Stop submitting at 1.5x the cap to account for pending postbacks.
- **Schema:** `db/offer_caps_schema.sql` — tables + helper functions
- **Weekly cron:** Monday 9AM IST — Captain asks AK for updated caps

## Debt Relief Offers

| ID | Buyer | Offer Name | CPA | Channel | Days | States Excluded | Weekly Cap | Notes |
|---|---|---|---|---|---|---|---|---|
| 4930 | FDR | Freedom Debt Relief - Email only - M-F Drops Only | $60 | Email | M-F | ❓ | ❓ "Ask for Cap" | Highest payout, volume limited |
| 4907 | Cliqsilver | Credit Card Debt Cpl-sq | $30 | Web | ❓ | ❓ | ❓ | |
| 4906 | JGW | JG Wentworth (nc-21805786) | $25 | Web | ❓ | ❓ | ❓ | |
| 4905 | NDR | National Debt Relief - W | $50 | Web | ❓ | ❓ | ❓ | |
| 4836 | NDR | NDR (Mon-Fri) Private-CPL (Budgeted) | $45 | Email | M-F | ❓ | ❓ "Budgeted" | |
| 4783 | NDR | NDR -SQ | $24 | Email | ❓ | ❓ | ❓ | |
| 4740 | NDR | NDR Email Only (Budgeted) | $16 | Email | ❓ | ❓ | ❓ "Budgeted" | Lowest debt CPA |
| 4737 | JGW | JGW Debt Settlement M-F {US} | $22 | Email | M-F | ❓ | ❓ | |
| 4718 | JGW | JGW Debt Settlement [MKP] | $24 | Email | ❓ | ❓ | ❓ | Marketplace |
| 4633 | JGW | JGW CPL - Email weekends! (NO CA) | $24 | Email | 7 days | CA excluded | ❓ | Only offer accepting weekends |

## Loan Offers (Zappian Legacy)

| ID | Name | Category | CPA | Channel |
|---|---|---|---|---|
| 3228 | Maxloanusa.com_ZM_025_PUB | Personal Loan | CPS 100% | Email+SMS |
| 2884 | Rapidfundonline.com | Payday Loan | CPS 100% | Email |
| 2256 | 1stlendingusa.com_ZM_025 | Personal Loan | CPS 100% | Email |
| 1901 | eloantoday.com_ZM_025 | Personal Loan | CPS 100% | Email+SMS |
| 176 | Brighterloan.com_ZM_025 | Personal Loan | CPS 100% | Email |

## What We Know from Offer Names (Inferred)
- **M-F** = Monday to Friday only (offers 4930, 4836, 4737)
- **Budgeted** = Weekly/monthly cap exists (offers 4836, 4740)
- **NO CA** = California excluded (offer 4633)
- **Ask for Cap** = Must request cap from network (offer 4930)
- **Email** channel = email-sourced leads only
- **Web** = web/display traffic leads

## What We NEED from AK (Arif provides caps directly)
AK manages buyer relationships and communicates caps to Captain. Captain routes leads accordingly.

- [ ] Daily/weekly/monthly cap per offer
- [ ] Full state exclusion list per offer
- [ ] Minimum debt amount requirements per buyer
- [ ] Lead freshness requirements (how old can the lead be?)
- [ ] Duplicate window (how long before same lead can be resubmitted?)
- [ ] Accepted hours for lead delivery (timezone?)
- [ ] Any suppression/DNC requirements beyond standard

## FDR Offer Detail (Verified from Everflow)
- **Everflow ID:** 4930
- **Caps in system:** None set (all dashes)
- **Targeting:** US only, no state exclusions in system
- **Payout:** Base CPA $60, no tiers
- **Creatives:** 2 HTML email templates provided
- **Subject lines:** 100+ provided (debt relief themed)
- **From lines:** Multiple variations (Debt_Relief, Partner, Associate, etc.)
- **Suppression file:** URL provided in Everflow
- **Unsub URL:** Provided
