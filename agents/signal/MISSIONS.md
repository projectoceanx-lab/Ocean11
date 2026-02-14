# Signal — Active Missions

## 🎯 Phase 1 Objectives
- [ ] Set up Ringba call routing for debt relief buyers
- [ ] Configure email delivery pipelines (ESP integration)
- [ ] Begin email domain warming (2+ domains)
- [ ] Implement buyer matching logic (vertical, cap, payout, hours)
- [ ] Build delivery confirmation and return handling
- [ ] Log every delivery with payout in P&L

## 📋 Delivery Priority Logic
1. Match lead vertical to buyer verticals
2. Check buyer daily cap (skip if at limit)
3. Check buyer preferred hours (respect timezone)
4. Route via buyer's preferred channel (call > email > API)
5. Confirm acceptance within 24h or flag for re-routing

## 🚧 Blockers
- None yet

## 📝 Notes
- Never deliver a lead that hasn't passed Shield compliance
- Track return rates per buyer — flag if > 15%
- Email warm-up takes 2-4 weeks — start early
