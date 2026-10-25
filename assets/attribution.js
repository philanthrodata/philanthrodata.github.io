/* PhilanthroData lead attribution.
   Remembers how a visitor first arrived (UTM tags, Google Ads click ID, referring site, landing page)
   so it can be sent with a form, instead of every lead showing up as "direct" or "offline".

   Stored in this browser only (localStorage "pd_attrib", 90 days). Nothing is sent anywhere
   until the visitor submits a form. No cookies, no third-party scripts.

   - first: set on the first visit and kept (first touch)
   - last:  replaced whenever the visitor arrives with new UTM tags or a click ID (last touch)

   Any POST form on the site gets these as hidden fields (utm_source, utm_medium, utm_campaign,
   utm_content, utm_term, gclid, referrer, landing_page), first touch.
   Other scripts can read window.pdAttribution() -> { first: {...}, last: {...} }. */
(function () {
  "use strict";
  var KEY = "pd_attrib", DAYS = 90;
  var FIELDS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid", "referrer", "landing_page"];

  function read() {
    try {
      var d = JSON.parse(localStorage.getItem(KEY) || "null");
      if (d && d.t && Date.now() - d.t < DAYS * 864e5) return d;
    } catch (e) {}
    return null;
  }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} }

  function current() {
    var q = new URLSearchParams(location.search), touch = {}, tagged = false;
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid"].forEach(function (k) {
      var v = (q.get(k) || "").trim().slice(0, 200);
      if (v) { touch[k] = v; tagged = true; }
    });
    var ref = "";
    try {
      if (document.referrer) {
        var r = new URL(document.referrer);
        if (r.hostname.replace(/^www\./, "") !== location.hostname.replace(/^www\./, "")) ref = r.origin + r.pathname;
      }
    } catch (e) {}
    if (ref) touch.referrer = ref.slice(0, 200);
    touch.landing_page = (location.origin + location.pathname).slice(0, 200);
    return { touch: touch, tagged: tagged, external: !!ref };
  }

  var data = read(), now = current();
  if (!data) {
    data = { t: Date.now(), first: now.touch, last: now.touch };
    save(data);
  } else if (now.tagged || now.external) {
    data.last = now.touch;
    save(data);
  }

  window.pdAttribution = function () { return { first: data.first || {}, last: data.last || {} }; };

  function fill() {
    var first = data.first || {};
    var forms = document.querySelectorAll('form[method="POST"], form[method="post"]');
    Array.prototype.forEach.call(forms, function (f) {
      if (f.querySelector('input[name="utm_source"]')) return;
      FIELDS.forEach(function (k) {
        if (!first[k]) return;
        var i = document.createElement("input");
        i.type = "hidden"; i.name = k; i.value = first[k];
        f.appendChild(i);
      });
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fill); else fill();
})();
