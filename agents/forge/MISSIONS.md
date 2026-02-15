# Forge — Active Missions

## 🎯 Phase 1 Objectives

### Website / Funnel (Next.js + Vercel)
- [ ] Build multi-step debt relief landing page (Next.js)
- [ ] Debt amount selector → personal info → consent → thank you
- [ ] Implement TCPA-compliant consent checkbox with proper legal language
- [ ] Shield reviews ALL copy/disclaimers before launch
- [ ] State license number display (FL required March 2026)
- [ ] Trust signals: BBB-style badges, testimonials, security seals
- [ ] Mobile-first responsive design (60%+ traffic is mobile)
- [ ] UTM parameter capture for attribution tracking

### Offer Wall
- [ ] Personalized offers based on lead profile (debt amount, type, state)
- [ ] Dynamic offer matching: $30K credit card debt ≠ $10K medical debt
- [ ] A/B test offer layouts (grid vs list, order, copy)

### Redirect Management
- [ ] Traffic routing: which source → which landing page variant
- [ ] RevPie traffic → specific landing page
- [ ] Facebook traffic → specific landing page
- [ ] Organic → default landing page
- [ ] Tracking pixel integration (FB CAPI, Everflow postback)

### FastDebt Integration
- [ ] API integration for lead enrichment (income verification, employment, debt validation)
- [ ] Real-time enrichment on form submission (before scoring)
- [ ] Verify enriched data stores correctly in Supabase `leads.enrichment_data`

### Buyer Delivery
- [ ] Format leads per buyer spec (JSON API, CSV email, live transfer)
- [ ] Implement buyer matching logic (vertical, state, cap, hours, payout)
- [ ] Track acceptance/rejection per buyer per day
- [ ] Handle returns: trace cause, feed back to Scout/Hawk

### Call Routing (Ringba)
- [ ] Set up Ringba campaigns for debt relief inbound
- [ ] Configure IVR qualification flow
- [ ] Route to highest-paying available buyer
- [ ] Minimum call duration tracking (90-120 sec for payout)

### CRO
- [ ] A/B test form layouts, step order, CTAs
- [ ] Track funnel drop-off per step
- [ ] Optimize for form completion rate (target: 15-25%)

## 📋 Key Metrics
- **Form completion rate** — target 15-25%
- **Buyer acceptance rate** — target >70%
- **Time to delivery** — target <5 min from form submission
- **Offer wall CTR** — track which offers convert

## 🚧 Blockers
- Supabase not set up yet (need DB for form submissions)
- No buyers confirmed yet (need buyer specs for delivery format)

## 📝 Notes
- Forge does NOT fill external forms (that's Scout)
- Forge BUILDS the funnel that captures our own leads
- Every landing page must pass Shield compliance review before launch
- Never deliver a lead that hasn't passed Shield compliance
- Buyer relationship management: remember preferences, hours, quirks
