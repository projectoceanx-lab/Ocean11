(function () {
  const CHECKOUT_URL = '';
  const OFFER_NAME = "Overnight Launch Kit (Docs Mirror)";
  const STORAGE_KEY = 'ocean_lead_queue_v1';

  const cta = document.getElementById('primaryCta');
  const msg = document.getElementById('ctaMessage');
  const fallback = document.getElementById('manualFallback');
  const form = document.getElementById('leadCaptureForm');
  const success = document.getElementById('leadSuccess');
  const exportJsonBtn = document.getElementById('exportJsonBtn');
  const exportCsvBtn = document.getElementById('exportCsvBtn');
  const mailtoBtn = document.getElementById('mailtoBtn');

  function getQueue() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
    catch { return []; }
  }

  function setQueue(leads) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(leads));
  }

  function escapeCsv(value) {
    const text = String(value || '');
    return /[",
]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
  }

  function download(filename, content, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function showFallback(text) {
    if (fallback) fallback.hidden = false;
    if (msg) msg.textContent = text;
  }

  function onPrimaryClick() {
    if (CHECKOUT_URL && /^https?:\/\//.test(CHECKOUT_URL)) {
      window.location.href = CHECKOUT_URL;
      return;
    }
    showFallback('Checkout is not connected yet. Complete the lead form below so we can follow up with manual invoice and delivery.');
  }

  function validate(data) {
    const errors = [];
    if (!data.name || data.name.length < 2) errors.push('Name is required (min 2 characters).');
    if (!/^\S+@\S+\.\S+$/.test(data.email || '')) errors.push('A valid email is required.');
    if (!data.offerInterest) errors.push('Please select your offer interest.');
    if (!data.painPoint || data.painPoint.length < 10) errors.push('Pain point is required (min 10 characters).');
    return errors;
  }

  function buildMailto(data) {
    const subject = encodeURIComponent(`${OFFER_NAME} - Lead Capture`);
    const body = encodeURIComponent(
      `New lead captured for ${OFFER_NAME}

` +
      `Name: ${data.name}
` +
      `Email: ${data.email}
` +
      `Telegram: ${data.telegram || 'Not provided'}
` +
      `Offer Interest: ${data.offerInterest}
` +
      `Pain Point: ${data.painPoint}
` +
      `Captured At: ${data.capturedAt}`
    );
    return `mailto:project.oceanx@gmail.com?subject=${subject}&body=${body}`;
  }

  function saveLead(data) {
    const queue = getQueue();
    queue.push(data);
    setQueue(queue);
  }

  function onLeadSubmit(e) {
    e.preventDefault();
    const data = {
      name: (form.name.value || '').trim(),
      email: (form.email.value || '').trim(),
      telegram: (form.telegram.value || '').trim(),
      offerInterest: form.offerInterest.value,
      painPoint: (form.painPoint.value || '').trim(),
      sourceOffer: OFFER_NAME,
      capturedAt: new Date().toISOString()
    };

    const errors = validate(data);
    if (errors.length) {
      showFallback(errors[0]);
      return;
    }

    saveLead(data);
    const mailtoLink = buildMailto(data);
    if (mailtoBtn) mailtoBtn.href = mailtoLink;

    if (success) success.hidden = false;
    showFallback('Lead saved locally. Next step: click "Open Email Draft" to send immediately, or export leads from this browser.');
    form.reset();
  }

  function exportJson() {
    const queue = getQueue();
    if (!queue.length) return showFallback('No saved leads yet. Submit a lead first.');
    download(`ocean-leads-${new Date().toISOString().slice(0,10)}.json`, JSON.stringify(queue, null, 2), 'application/json');
  }

  function exportCsv() {
    const queue = getQueue();
    if (!queue.length) return showFallback('No saved leads yet. Submit a lead first.');
    const headers = ['name','email','telegram','offerInterest','painPoint','sourceOffer','capturedAt'];
    const lines = [headers.join(',')].concat(queue.map(row => headers.map(h => escapeCsv(row[h])).join(',')));
    download(`ocean-leads-${new Date().toISOString().slice(0,10)}.csv`, lines.join('
'), 'text/csv');
  }

  if (cta) cta.addEventListener('click', onPrimaryClick);
  if (form) form.addEventListener('submit', onLeadSubmit);
  if (exportJsonBtn) exportJsonBtn.addEventListener('click', exportJson);
  if (exportCsvBtn) exportCsvBtn.addEventListener('click', exportCsv);
})();
