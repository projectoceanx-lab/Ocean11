(function () {
  const cta = document.getElementById('primaryCta');
  const msg = document.getElementById('ctaMessage');

  function manualCheckoutNotice() {
    msg.textContent = 'Checkout link not connected in this repo yet. Morning fallback: collect buyer email + send Stripe/PayPal invoice manually.';
  }

  if (cta) cta.addEventListener('click', manualCheckoutNotice);
})();
