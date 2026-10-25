/* PhilanthroData shared script */
(function () {
  'use strict';
  var track = function (name, params) { try { if (window.gtag) gtag('event', name, params || {}); } catch (e) {} };

  /* Old single-page links (/#contact etc.) now live on their own pages */
  var moved = { '#contact': '/contact/', '#services': '/services/', '#pricing': '/services/#pricing',
    '#about': '/about/', '#case-study': '/case-studies/', '#approach': '/mission/' };
  if ((location.pathname === '/' || location.pathname === '/index.html') && moved[location.hash]) {
    location.replace(moved[location.hash]);
    return;
  }

  /* Fade-ins: content is visible by default; hidden only once this script runs */
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('visible'); io.unobserve(en.target); } });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('visible'); });
  }

  /* Mobile menu */
  var btn = document.querySelector('.menu-toggle'), menu = document.getElementById('mobile-menu');
  if (btn && menu) {
    var set = function (open) {
      menu.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    btn.addEventListener('click', function () { set(!menu.classList.contains('open')); });
    menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { set(false); }); });
  }

  /* CTA and email click tracking */
  document.querySelectorAll('[data-cta]').forEach(function (a) {
    a.addEventListener('click', function () { track('cta_click', { cta: a.getAttribute('data-cta') }); });
  });
  document.querySelectorAll('a[href^="mailto:"]').forEach(function (a) {
    a.addEventListener('click', function () { track('email_click', { location: location.pathname }); });
  });

  /* Contact form */
  var form = document.getElementById('lead-form');
  if (!form) return;
  var role = form.querySelector('#role'), msgLabel = form.querySelector('label[for="message"]'),
      msg = form.querySelector('#message'), orgLabel = form.querySelector('label[for="org"]'),
      status = document.getElementById('form-status'), submit = form.querySelector('button[type="submit"]');
  var prompts = {
    nonprofit: ['The one question you wish your data could answer', 'e.g. Do people who attend our free workshops come back and buy tickets?', 'Organization'],
    volunteer: ['What skills would you like to share?', 'e.g. GA4 and Looker Studio, a few hours a month. Or a link to your LinkedIn profile.', 'Where you work (optional)'],
    other: ['How can I help?', '', 'Organization (optional)']
  };
  var started = false;
  form.addEventListener('input', function () { if (!started) { started = true; track('form_start', { form_id: 'philanthrodata_contact' }); } });
  role.addEventListener('change', function () {
    var p = prompts[role.value] || prompts.nonprofit;
    msgLabel.textContent = p[0]; msg.placeholder = p[1]; orgLabel.textContent = p[2];
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var show = function (ok, text) {
      status.style.display = 'block';
      status.style.color = ok ? '#5C7A6B' : '#A0522D';
      status.textContent = text;
    };
    submit.disabled = true; submit.textContent = 'Sending…';
    fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
      .then(function (res) {
        if (!res.ok) throw new Error('status ' + res.status);
        track('generate_lead', { lead_type: role.value || 'unknown', form_id: 'philanthrodata_contact' });
        try { if (window.clarity) clarity('event', 'generate_lead'); } catch (err) {}
        show(true, "Thanks. I'll reply within two business days.");
        form.reset(); role.dispatchEvent(new Event('change'));
      })
      .catch(function () { show(false, 'Something went wrong. Please email chad.priest@philanthrodata.org instead.'); })
      .then(function () { submit.disabled = false; submit.textContent = 'Send'; });
  });
})();
