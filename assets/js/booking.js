/* Sabka Ved Wellness booking form handler.
 * Webflow forms post to Webflow's servers and fail off-Webflow, so this script takes over submit.
 * It registers a capture-phase listener on document (loaded before webflow.js) and stops the event
 * before Webflow's own handler sees it.
 *
 * WA_NUMBER: clinic WhatsApp number, digits only with country code (for example 9199XXXXXXXX).
 * While it is empty, nothing is sent anywhere and the visitor is told to call or WhatsApp the clinic.
 */
(function () {
  'use strict';
  var WA_NUMBER = '';

  var DONE_PENDING = 'Thank you. Online booking is opening shortly. Please call or WhatsApp the clinic to confirm your slot.';
  var DONE_WA = 'Thank you. WhatsApp has opened with your request filled in. Please press send there so the clinic can confirm your slot.';

  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function todayISO() {
    var d = new Date();
    return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
  }
  function val(form, name) {
    var el = form.querySelector('[name="' + name + '"]');
    if (!el) return '';
    if (el.type === 'checkbox') return el.checked;
    return (el.value || '').trim();
  }
  function field(form, name) { return form.querySelector('[name="' + name + '"]'); }

  function validate(form) {
    var errs = [];
    var name = val(form, 'Name');
    var phone = val(form, 'Phone').replace(/[\s\-()]/g, '');
    var age = val(form, 'Age');
    var date = val(form, 'Preferred-Date');
    if (name.length < 2) errs.push(['Name', 'Please enter your full name.']);
    if (!/^(\+?91)?[6-9]\d{9}$/.test(phone)) errs.push(['Phone', 'Please enter a valid 10-digit Indian mobile number.']);
    var a = parseInt(age, 10);
    if (!(a >= 1 && a <= 110)) errs.push(['Age', 'Please enter your age in years.']);
    if (!date) errs.push(['Preferred-Date', 'Please choose a preferred date.']);
    else if (date < todayISO()) errs.push(['Preferred-Date', 'Please choose today or a later date.']);
    if (!val(form, 'Therapy')) errs.push(['Therapy', 'Please select a therapy or consultation.']);
    if (!val(form, 'Gender')) errs.push(['Gender', 'Please select an option for gender.']);
    if (!val(form, 'Consent')) errs.push(['Consent', 'Please tick the box to confirm you understand this is a request.']);
    return errs;
  }

  function message(form) {
    var lines = [
      'Appointment request: Sabka Ved Wellness',
      'Name: ' + val(form, 'Name'),
      'Phone: ' + val(form, 'Phone'),
      'Age: ' + val(form, 'Age'),
      'Gender: ' + val(form, 'Gender'),
      'Preferred date: ' + val(form, 'Preferred-Date'),
      'Therapy: ' + val(form, 'Therapy')
    ];
    var msg = val(form, 'Message');
    if (msg) lines.push('Message: ' + msg);
    return lines.join('\n');
  }

  function boxes(form) {
    var wrap = form.parentNode;
    return { done: wrap.querySelector('.w-form-done'), fail: wrap.querySelector('.w-form-fail') };
  }

  function onSubmit(e) {
    var form = e.target;
    if (!form || form.tagName !== 'FORM' || !form.hasAttribute('data-booking')) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    e.stopPropagation();

    var b = boxes(form);
    Array.prototype.forEach.call(form.querySelectorAll('[aria-invalid]'), function (el) {
      el.removeAttribute('aria-invalid');
      el.style.borderColor = '';
    });
    var errs = validate(form);
    if (errs.length) {
      errs.forEach(function (er) {
        var el = field(form, er[0]);
        if (el) { el.setAttribute('aria-invalid', 'true'); el.style.borderColor = '#c0392b'; }
      });
      if (b.fail) {
        var box = b.fail.querySelector('div') || b.fail;
        box.textContent = errs.map(function (er) { return er[1]; }).join(' ');
        b.fail.style.display = 'block';
      }
      var first = field(form, errs[0][0]);
      if (first && first.focus) first.focus();
      return;
    }
    if (b.fail) b.fail.style.display = 'none';

    var text = DONE_PENDING;
    if (WA_NUMBER) {
      window.open('https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(message(form)), '_blank', 'noopener');
      text = DONE_WA;
    }
    if (b.done) {
      var d = b.done.querySelector('div') || b.done;
      d.textContent = text;
      form.style.display = 'none';
      b.done.style.display = 'block';
      b.done.setAttribute('tabindex', '-1');
      if (b.done.focus) b.done.focus();
    }
  }

  document.addEventListener('submit', onSubmit, true);

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('form[data-booking] input[type="date"]'), function (el) {
      el.min = todayISO();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
