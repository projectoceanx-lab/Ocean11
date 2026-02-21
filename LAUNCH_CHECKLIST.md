# Morning Launch Checklist (<20 minutes)

## 0–5 min: Unblock deploy
1. Open Vercel billing page and clear overdue balance.
2. In terminal:
   ```bash
   cd /Users/arifkhan/Desktop/Ocean11
   npx vercel --prod storefront/overnight-launch-kit --yes
   ```
3. Copy live URL.

## 5–10 min: Connect checkout
1. Create Stripe/PayPal payment link for `$79`.
2. Update CTA in `storefront/overnight-launch-kit/script.js` (or `index.html`) to use live payment URL.
3. Redeploy with same Vercel command.

## 10–15 min: Final QA
1. Open live page on mobile + desktop.
2. Validate CTA click opens checkout link.
3. Confirm product files are zipped/ready from `products/overnight-launch-kit/`.

## 15–20 min: Publish + distribute
1. Post launch announcement to your operator audience/email/social.
2. Include urgency line: “$79 for first 20 buyers, then $129.”
3. Start manual fulfillment fallback (invoice + file send) if checkout has any issue.
