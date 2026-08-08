/* The Tech Docket — measurement layer.
 *
 * Loaded as an EXTERNAL file on purpose: the site allows exactly one inline
 * script (the pre-paint theme toggle, id="ttd-theme"). Everything here is
 * out-of-line so that policy holds.
 *
 * What runs:
 *   1. GA4 (G-7M4KPLZK1B)  — traffic, channels, engagement time.
 *   2. PostHog (US cloud)  — session replay + heatmaps, cookie-light
 *                            (persistence:"memory", so no PostHog cookies).
 *   3. scroll_75           — one event per page when the reader passes 75%
 *                            of the document. This is a tracked KPI.
 *
 * The GoatCounter counter stays where it is (end of <body>); the engine's
 * feedback loop reads its API to score which articles earned attention.
 *
 * Deployed 2026-08-08.
 */
(function () {
  "use strict";

  var GA4_ID = "G-7M4KPLZK1B";
  var POSTHOG_KEY = "phc_rkUE7oawq7TRahVzPT3Jz4BFZH9W4LcjPmrGWdvZxcKP";
  var POSTHOG_HOST = "https://us.i.posthog.com";
  var POSTHOG_ASSETS = "https://us-assets.i.posthog.com";

  /* ---------------- GA4 ----------------
     The gtag loader tag is in <head>; this defines the queue and configures
     the property. Both orderings are safe — gtag() only pushes to dataLayer. */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag("js", new Date());
  gtag("config", GA4_ID, {
    send_page_view: true,
    anonymize_ip: true
  });

  /* ---------------- PostHog ----------------
     Loaded async, then initialised on load. Avoids shipping PostHog's
     inline bootstrap stub, which would breach the one-inline-script rule. */
  var ph = document.createElement("script");
  ph.src = POSTHOG_ASSETS + "/static/array.js";
  ph.async = true;
  ph.onload = function () {
    if (!window.posthog || !window.posthog.init) { return; }
    window.posthog.init(POSTHOG_KEY, {
      api_host: POSTHOG_HOST,
      persistence: "memory",
      autocapture: true,
      capture_pageview: true,
      capture_pageleave: true,
      disable_session_recording: false,
      enable_heatmaps: true,
      person_profiles: "identified_only"
    });
  };
  document.head.appendChild(ph);

  /* ---------------- scroll depth ----------------
     Fires once, at 75% of scrollable height. Passive listener, self-removing,
     rAF-throttled — no measurable effect on scrolling. */
  var fired = false;
  var ticking = false;

  function measure() {
    ticking = false;
    if (fired) { return; }
    var doc = document.documentElement;
    var scrollable = doc.scrollHeight - window.innerHeight;
    if (scrollable <= 0) { return; }
    var pct = (window.scrollY || doc.scrollTop) / scrollable;
    if (pct < 0.75) { return; }

    fired = true;
    window.removeEventListener("scroll", onScroll);

    var payload = { path: location.pathname, percent: 75 };
    try { gtag("event", "scroll_75", payload); } catch (e) {}
    try {
      if (window.posthog && window.posthog.capture) {
        window.posthog.capture("scroll_75", payload);
      }
    } catch (e) {}
  }

  function onScroll() {
    if (ticking) { return; }
    ticking = true;
    window.requestAnimationFrame(measure);
  }

  window.addEventListener("scroll", onScroll, { passive: true });
})();
