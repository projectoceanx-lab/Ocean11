(function () {
  // Set this to your Stripe/PayPal checkout URL before launch.
  const CHECKOUT_URL = '';

  const cta = document.getElementById('primaryCta');
  const msg = document.getElementById('ctaMessage');
  const fallback = document.getElementById('manualFallback');
  const invoiceBtn = document.getElementById('invoiceBtn');
  const buyerEmail = document.getElementById('buyerEmail');

  function showFallback(text) {
    if (fallback) fallback.hidden = false;
    if (msg) msg.textContent = text;
  }

  function onPrimaryClick() {
    if (CHECKOUT_URL && /^https?:\/\//.test(CHECKOUT_URL)) {
      window.location.href = CHECKOUT_URL;
      return;
    }

    showFallback('Checkout is not connected yet. Use manual invoice fallback so you do not lose interested buyers.');
  }

  function requestInvoice() {
    const email = (buyerEmail?.value || '').trim();
    if (!email || !email.includes('@')) {
      showFallback('Please enter a valid email before requesting a manual invoice.');
      return;
    }

    const subject = encodeURIComponent('Compliance Preflight Pack - Manual Invoice Request');
    const body = encodeURIComponent(`Please send invoice for Compliance Preflight Pack.\nBuyer email: ${email}`);
    window.location.href = `mailto:project.oceanx@gmail.com?subject=${subject}&body=${body}`;
    showFallback('Email draft opened. Send it to request your invoice and delivery link.');
  }

  if (cta) cta.addEventListener('click', onPrimaryClick);
  if (invoiceBtn) invoiceBtn.addEventListener('click', requestInvoice);
})();
