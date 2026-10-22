/* ── RATES TOGGLE: standard / promo, shareable via ?rates=promo ── */
const rateButtons = document.querySelectorAll('.lb-toggle-btn');

function setRates(mode) {
  document.body.dataset.rates = mode;
  rateButtons.forEach(btn => {
    btn.setAttribute('aria-pressed', String(btn.dataset.rates === mode));
  });
  const url = new URL(window.location);
  if (mode === 'promo') url.searchParams.set('rates', 'promo');
  else url.searchParams.delete('rates');
  history.replaceState(null, '', url);
}

rateButtons.forEach(btn => {
  btn.addEventListener('click', () => setRates(btn.dataset.rates));
});

const initial = new URLSearchParams(window.location.search).get('rates');
setRates(initial === 'promo' ? 'promo' : 'standard');

/* ── PRINT ── */
document.getElementById('lb-print').addEventListener('click', () => window.print());
