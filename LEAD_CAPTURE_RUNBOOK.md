# LEAD_CAPTURE_RUNBOOK

## Purpose
Daily retrieval/export of storefront leads when checkout/API is offline.

## Where leads are stored
- Browser localStorage key: `ocean_lead_queue_v1`
- Scope: per browser + device profile (not synced automatically)

## Daily SOP (exact)
1. Open any storefront page with lead capture form.
2. Click **Export leads CSV** (for ops spreadsheet) and **Export leads JSON** (backup).
3. Save files with date in shared folder (example: `exports/leads/2026-02-21/`).
4. Click **Open Email Draft** for newest urgent leads and send immediately to `project.oceanx@gmail.com`.
5. Import CSV into your working tracker.

## Manual browser retrieval (if export buttons not used)
1. Open page in the same browser profile used for capture.
2. Open DevTools Console.
3. Run:
   ```js
   JSON.parse(localStorage.getItem('ocean_lead_queue_v1') || '[]')
   ```
4. Copy output into `.json` backup file.

## CSV conversion snippet (console fallback)
```js
const rows = JSON.parse(localStorage.getItem('ocean_lead_queue_v1') || '[]');
const h = ['name','email','telegram','offerInterest','painPoint','sourceOffer','capturedAt'];
const esc = v => /[",\n]/.test(String(v||'')) ? `"${String(v).replace(/"/g,'""')}"` : String(v||'');
const csv = [h.join(',')].concat(rows.map(r => h.map(k => esc(r[k])).join(','))).join('\n');
console.log(csv);
```

## Data fields captured
- `name` (required)
- `email` (required)
- `telegram` (optional)
- `offerInterest` (required)
- `painPoint` (required)
- `sourceOffer`
- `capturedAt` (ISO timestamp)

## Validation rules live on page
- Name min 2 chars
- Valid email format
- Offer selection required
- Pain point min 10 chars

## Note
This fallback path has no external API dependency and works fully client-side.