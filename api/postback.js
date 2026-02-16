export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  const SUPABASE_URL = process.env.SUPABASE_URL;
  const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;
  const POSTBACK_SECRET = process.env.POSTBACK_SECRET || '';

  if (!SUPABASE_URL || !SUPABASE_KEY) {
    return res.status(500).json({ success: false, message: 'Missing Supabase env vars' });
  }

  const q = req.query || {};
  const click_id = q.click_id;
  const offer_id = q.offer_id;
  const payout = q.payout;
  const txn_id = q.txn_id;
  const secret = q.secret;

  const headers = {
    apikey: SUPABASE_KEY,
    Authorization: `Bearer ${SUPABASE_KEY}`,
    'Content-Type': 'application/json',
    Prefer: 'return=representation',
  };

  async function sb(path, init = {}) {
    const r = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, {
      ...init,
      headers: { ...headers, ...(init.headers || {}) },
    });
    const text = await r.text();
    let data = null;
    try { data = text ? JSON.parse(text) : null; } catch { data = text; }
    return { ok: r.ok, status: r.status, data };
  }

  // Health mode
  if (!click_id && (q.health === '1' || q.ping === '1')) {
    return res.status(200).json({ success: true, service: 'ocean-postback', status: 'ok' });
  }

  if (POSTBACK_SECRET && secret !== POSTBACK_SECRET) {
    return res.status(403).json({ success: false, message: 'Invalid secret' });
  }

  if (!click_id) {
    return res.status(400).json({ success: false, message: 'Missing click_id' });
  }

  try {
    // 1) log raw postback (best effort)
    await sb('postback_log', {
      method: 'POST',
      body: JSON.stringify({
        source_ip: req.headers['x-forwarded-for'] || req.socket?.remoteAddress || null,
        method: 'GET',
        query_params: q,
        offer_id: offer_id ? Number(offer_id) : null,
        click_id,
        payout: payout ? Number(payout) : null,
        processed: false,
      }),
    });

    // 2) find submission by click id
    const subResp = await sb(
      `offer_submissions?everflow_click_id=eq.${encodeURIComponent(click_id)}&status=eq.submitted&limit=1`
    );
    const subs = Array.isArray(subResp.data) ? subResp.data : [];

    if (!subs.length) {
      return res.status(404).json({ success: false, message: 'No matching submission' });
    }

    const sub = subs[0];

    // 3) mark submission converted
    await sb(`offer_submissions?id=eq.${sub.id}`, {
      method: 'PATCH',
      body: JSON.stringify({
        status: 'converted',
        converted_at: new Date().toISOString(),
        payout: payout ? Number(payout) : null,
        conversion_id: txn_id || null,
      }),
    });

    // 4) increment offer conversion counters
    const offerResp = await sb(
      `everflow_offers?offer_id=eq.${sub.offer_id}&select=daily_conversions,weekly_conversions,weekly_cap`
    );
    const offers = Array.isArray(offerResp.data) ? offerResp.data : [];
    if (offers.length) {
      const o = offers[0];
      const newDaily = Number(o.daily_conversions || 0) + 1;
      const newWeekly = Number(o.weekly_conversions || 0) + 1;
      const upd = { daily_conversions: newDaily, weekly_conversions: newWeekly };
      if (o.weekly_cap && newWeekly >= Number(o.weekly_cap)) upd.status = 'capped';

      await sb(`everflow_offers?offer_id=eq.${sub.offer_id}`, {
        method: 'PATCH',
        body: JSON.stringify(upd),
      });
    }

    // 5) mark lead delivered
    await sb(`leads?id=eq.${sub.lead_id}`, {
      method: 'PATCH',
      body: JSON.stringify({ status: 'delivered' }),
    });

    // 6) mark postback log processed
    await sb(`postback_log?click_id=eq.${encodeURIComponent(click_id)}&processed=eq.false`, {
      method: 'PATCH',
      body: JSON.stringify({ processed: true, processed_at: new Date().toISOString() }),
    });

    return res.status(200).json({
      success: true,
      message: 'Conversion recorded',
      click_id,
      offer_id: sub.offer_id,
      txn_id: txn_id || null,
    });
  } catch (e) {
    return res.status(500).json({ success: false, message: String(e) });
  }
}
