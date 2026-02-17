# POSTBACK E2E Validation Report

**Date/Time (Asia/Dubai):** Tue 2026-02-17 01:31–01:32 GMT+4  
**Endpoint under test:** `https://ocean11-postback-three.vercel.app`  
**Source code reference:** `api/postback.js`, `vercel.json`

---

## Scope
Validated:
1. `/health` response
2. Secret gate behavior
3. Sample `click_id` behavior
4. End-to-end DB-backed conversion flow (create realistic test records, hit postback, verify status transition)

---

## 1) `/health` response ✅

### Request
`GET https://ocean11-postback-three.vercel.app/health`

### Evidence
- HTTP status: **200**
- Body:

```json
{"success":true,"service":"ocean-postback","status":"ok"}
```

---

## 2) Secret gate behavior ✅

### A) Missing secret
Request: `GET /postback` (no query params)

- HTTP status: **403**
- Body:

```json
{"success":false,"message":"Invalid secret"}
```

### B) Wrong secret
Request: `GET /postback?click_id=sample_click_123&secret=wrong_secret`

- HTTP status: **403**
- Body:

```json
{"success":false,"message":"Invalid secret"}
```

### C) Correct secret + unknown click_id
Request used valid configured `POSTBACK_SECRET`.

- HTTP status: **404**
- Body:

```json
{"success":false,"message":"No matching submission"}
```

This confirms secret validation is active and enforced before click lookup.

---

## 3) Sample `click_id` behavior ✅

With valid secret and `click_id=sample_click_123` (not present in DB), API returns:

- HTTP status: **404**
- Message: **"No matching submission"**

Expected behavior based on code path in `api/postback.js`:
- Finds `offer_submissions` where `everflow_click_id == click_id` and `status == submitted`
- If none found, returns 404.

---

## 4) Full E2E DB-backed conversion validation ✅

A realistic test flow was executed against live Supabase via service role credentials and live Vercel endpoint.

### Test data created
- `offer_id`: `4930` (active offer pulled from `everflow_offers`)
- `lead_id`: `f9875ea8-f526-433e-80cd-71ac794a0d7e`
- `submission_id`: `74bf96dd-e5d1-4fa8-8008-983037089156`
- `everflow_click_id`: `e2e_click_20260216T213134Z_80192888`

### Pre-postback state
- `offer_submissions.status`: `submitted`
- `offer_submissions.converted_at`: `null`
- `offer_submissions.payout`: `null`
- `leads.status`: `new`

### Postback fired
`GET /postback?click_id=e2e_click_20260216T213134Z_80192888&offer_id=4930&payout=12.34&txn_id=txn_20260216t213134z&secret=<valid>`

### API response
- HTTP status: **200**
- Body:

```json
{
  "success": true,
  "message": "Conversion recorded",
  "click_id": "e2e_click_20260216T213134Z_80192888",
  "offer_id": 4930,
  "txn_id": "txn_20260216t213134z"
}
```

### Post-postback DB verification
- `offer_submissions.status`: **converted**
- `offer_submissions.converted_at`: **set** (`2026-02-16T21:31:37.389+00:00`)
- `offer_submissions.payout`: **12.34**
- `offer_submissions.conversion_id`: **txn_20260216t213134z**
- `leads.status`: **delivered**
- `postback_log.processed`: **true**
- `postback_log.processed_at`: **set** (`2026-02-16T21:31:38.875+00:00`)

Conclusion: status transition and logging pipeline worked end-to-end on live infra.

---

## Observed code/env gaps (actionable)

1. **Validation ordering returns 403 before 400 for missing click_id**
   - Current code checks secret before `click_id` presence.
   - Operational effect: malformed requests without secret never reveal missing `click_id` error.

2. **No idempotent success on repeated same click postback**
   - After first conversion, second attempt likely returns 404 (because lookup requires `status=submitted`).
   - Consider idempotent handling (e.g., return 200 with already-converted state) for network retries from upstream.

3. **Security model is static shared secret only**
   - No signed hash/HMAC over payload and no timestamp/nonce verification.
   - Consider stronger verification if partner supports it.

4. **Hard dependency on Supabase service env vars at runtime**
   - Missing `SUPABASE_URL` or `SUPABASE_SERVICE_ROLE_KEY` returns 500 (`Missing Supabase env vars`).
   - Ensure env parity across all Vercel environments (prod/preview/dev).

---

## Final verdict

**PASS** — Live endpoint behavior is correct for health, secret gate, unknown click handling, and full conversion status transition with DB-backed test records.
