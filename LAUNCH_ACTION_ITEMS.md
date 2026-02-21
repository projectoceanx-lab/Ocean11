# Launch Action Items (True Blockers Only)

## Blocker 1 — Vercel deployment billing lock (external)
Attempted deploy command:
```bash
npx vercel --prod storefront/overnight-launch-kit --yes
```
Result:
- Vercel CLI ran successfully, but deployment failed with **402 overdue team balance** on team `arifs-projects-aacf12b1`.
- Billing URL returned by CLI:
  `https://vercel.com/teams/arifs-projects-aacf12b1/settings/billing`

### Next-step commands (after billing is resolved)
```bash
cd /Users/arifkhan/Desktop/Ocean11
npx vercel --prod storefront/overnight-launch-kit --yes
```

## Blocker 2 — Checkout credentials missing (external)
No Stripe/PayPal/Gumroad credentials are available in this repo context, so live self-serve checkout cannot be wired autonomously.

### Next-step commands (example with Stripe Payment Link)
1) Create payment link in Stripe dashboard for product `Overnight Launch Kit` at `$79`.
2) Replace CTA target in storefront page with the live URL.
3) Redeploy storefront.
