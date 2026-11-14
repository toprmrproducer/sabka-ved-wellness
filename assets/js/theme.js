/* Sabka Ved Wellness theme switch. Loaded in <head> so the stored choice applies before first paint.
 * Stores "dark" or "light" in localStorage; with no stored choice the OS preference wins (CSS media query). */
(function () {
  'use strict';
  var KEY = 'svw-theme';
  var root = document.documentElement;
  try {
    var saved = localStorage.getItem(KEY);
    if (saved === 'dark' || saved === 'light') root.setAttribute('data-theme', saved);
  } catch (e) { /* storage blocked: follow the OS setting */ }

  function current() {
    var t = root.getAttribute('data-theme');
    if (t) return t;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function label() {
    var dark = current() === 'dark';
    var btns = document.querySelectorAll('.theme-toggle');
    for (var i = 0; i < btns.length; i++) {
      btns[i].setAttribute('aria-pressed', dark ? 'true' : 'false');
      btns[i].setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
      btns[i].setAttribute('title', dark ? 'Light theme' : 'Dark theme');
    }
  }
  document.addEventListener('click', function (e) {
    var b = e.target && e.target.closest ? e.target.closest('.theme-toggle') : null;
    if (!b) return;
    e.preventDefault();
    var next = current() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem(KEY, next); } catch (err) { /* ignore */ }
    label();
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', label);
  else label();
  if (window.matchMedia) {
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    if (mq.addEventListener) mq.addEventListener('change', label);
  }
})();
