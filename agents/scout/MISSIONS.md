# Scout — Active Missions

## 🎯 Phase 1 Objectives
- [ ] Set up stealth browser with proxy rotation
- [ ] Identify and map 10+ debt relief lead forms
- [ ] Build form-filling automation for top 5 forms
- [ ] Integrate FastDebt API for lead enrichment
- [ ] Achieve 80%+ quality score on enriched leads
- [ ] Implement dedup checking against existing DB

## 📋 Lead Quality Scoring Criteria
- **A-tier (80-100):** Verified income, confirmed debt $10K+, employed, valid contact
- **B-tier (60-79):** Partial verification, debt $5K+, contact valid
- **C-tier (40-59):** Minimal verification, debt amount unclear
- **D-tier (0-39):** Unverified, likely low value — flag for review

## 🚧 Blockers
- None yet

## 📝 Notes
- Always check DB before inserting — no duplicate leads
- Rotate proxies every 5-10 requests minimum
- Log every form submission attempt (success or fail)
