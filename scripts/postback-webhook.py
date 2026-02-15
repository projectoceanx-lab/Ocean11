#!/usr/bin/env python3
"""
Everflow Postback Webhook — Project Ocean
==========================================
Receives conversion postbacks from Everflow and updates cap counts.

Deploy: Any Python-capable host (Railway, Vercel, VPS, or even localhost + ngrok for testing)

Everflow sends: GET /postback?click_id={aff_click_id}&offer_id={offer_id}&payout={payout}&txn_id={transaction_id}

Usage:
  python3 postback-webhook.py                    # Runs on port 8787
  PORT=9090 python3 postback-webhook.py          # Custom port
"""

import os
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

import httpx

SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY') or os.environ['SUPABASE_SERVICE_KEY']
PORT = int(os.environ.get('POSTBACK_PORT', 8787))
# Optional: shared secret to verify postbacks are from Everflow
POSTBACK_SECRET = os.environ.get('POSTBACK_SECRET', '')

HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}


def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}", flush=True)


def log_postback(params, source_ip, method='GET'):
    """Log raw postback to postback_log table"""
    try:
        httpx.post(
            f"{SUPABASE_URL}/rest/v1/postback_log",
            headers=HEADERS,
            json={
                'source_ip': source_ip,
                'method': method,
                'query_params': params,
                'offer_id': int(params.get('offer_id', [0])[0]) or None,
                'click_id': params.get('click_id', [None])[0],
                'payout': float(params.get('payout', [0])[0]) or None,
                'processed': False
            },
            timeout=10
        )
    except Exception as e:
        log(f"WARNING: Failed to log postback: {e}")


def process_conversion(click_id, offer_id, payout, txn_id):
    """Process a conversion postback — update submission + offer counts"""
    
    # 1. Find matching submission
    resp = httpx.get(
        f"{SUPABASE_URL}/rest/v1/offer_submissions"
        f"?everflow_click_id=eq.{click_id}&status=eq.submitted&limit=1",
        headers=HEADERS,
        timeout=10
    )
    submissions = resp.json()
    
    if not submissions:
        log(f"WARNING: No matching submission for click_id={click_id}")
        return False, "No matching submission"
    
    sub = submissions[0]
    sub_id = sub['id']
    sub_offer_id = sub['offer_id']
    lead_id = sub['lead_id']
    
    # 2. Update submission → converted
    httpx.patch(
        f"{SUPABASE_URL}/rest/v1/offer_submissions?id=eq.{sub_id}",
        headers=HEADERS,
        json={
            'status': 'converted',
            'converted_at': datetime.utcnow().isoformat(),
            'payout': float(payout) if payout else None,
            'conversion_id': txn_id,
        },
        timeout=10
    )
    
    # 3. Increment conversion counts on offer
    offer_resp = httpx.get(
        f"{SUPABASE_URL}/rest/v1/everflow_offers?offer_id=eq.{sub_offer_id}&select=daily_conversions,weekly_conversions,weekly_cap",
        headers=HEADERS,
        timeout=10
    )
    offer_data = offer_resp.json()
    if offer_data:
        o = offer_data[0]
        new_daily = (o.get('daily_conversions') or 0) + 1
        new_weekly = (o.get('weekly_conversions') or 0) + 1
        
        update = {
            'daily_conversions': new_daily,
            'weekly_conversions': new_weekly,
        }
        # Auto-cap if weekly limit hit
        if o.get('weekly_cap') and new_weekly >= o['weekly_cap']:
            update['status'] = 'capped'
            log(f"ALERT: Offer {sub_offer_id} hit weekly cap ({o['weekly_cap']})")
        
        httpx.patch(
            f"{SUPABASE_URL}/rest/v1/everflow_offers?offer_id=eq.{sub_offer_id}",
            headers=HEADERS,
            json=update,
            timeout=10
        )
    
    # 4. Update lead status → delivered
    httpx.patch(
        f"{SUPABASE_URL}/rest/v1/leads?id=eq.{lead_id}",
        headers=HEADERS,
        json={'status': 'delivered'},
        timeout=10
    )
    
    # 5. Mark postback_log as processed
    httpx.patch(
        f"{SUPABASE_URL}/rest/v1/postback_log?click_id=eq.{click_id}&processed=eq.false",
        headers=HEADERS,
        json={'processed': True, 'processed_at': datetime.utcnow().isoformat()},
        timeout=10
    )
    
    log(f"CONVERSION: offer={sub_offer_id} click={click_id} payout=${payout} txn={txn_id}")
    return True, "Conversion recorded"


class PostbackHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        client_ip = self.client_address[0]
        
        # Health check
        if parsed.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'service': 'ocean-postback'}).encode())
            return
        
        # Postback endpoint
        if parsed.path == '/postback':
            # Optional secret check
            if POSTBACK_SECRET and params.get('secret', [None])[0] != POSTBACK_SECRET:
                log(f"REJECTED: Invalid secret from {client_ip}")
                self.send_response(403)
                self.end_headers()
                return
            
            # Log raw postback first (always)
            log_postback(params, client_ip)
            
            click_id = params.get('click_id', [None])[0]
            offer_id = params.get('offer_id', [None])[0]
            payout = params.get('payout', [None])[0]
            txn_id = params.get('txn_id', [None])[0]
            
            if not click_id:
                log(f"BAD REQUEST: No click_id from {client_ip}")
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing click_id')
                return
            
            try:
                success, msg = process_conversion(click_id, offer_id, payout, txn_id)
                self.send_response(200 if success else 404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': success, 'message': msg}).encode())
            except Exception as e:
                log(f"ERROR processing postback: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
            return
        
        # Cap status endpoint — check all offer caps
        if parsed.path == '/caps':
            try:
                resp = httpx.get(
                    f"{SUPABASE_URL}/rest/v1/everflow_offers"
                    f"?select=offer_id,buyer_short,cpa,weekly_cap,weekly_submissions,weekly_conversions,daily_submissions,daily_conversions,status"
                    f"&order=cpa.desc",
                    headers=HEADERS,
                    timeout=10
                )
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(resp.json(), indent=2).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
            return
        
        self.send_response(404)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default request logging — we have our own"""
        pass


def main():
    server = HTTPServer(('0.0.0.0', PORT), PostbackHandler)
    log(f"Ocean Postback Webhook running on port {PORT}")
    log(f"Endpoints:")
    log(f"  GET /postback?click_id=X&offer_id=Y&payout=Z&txn_id=T")
    log(f"  GET /caps       — View all offer cap statuses")
    log(f"  GET /health     — Health check")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("Shutting down...")
        server.server_close()


if __name__ == '__main__':
    main()
