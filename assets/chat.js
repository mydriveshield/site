/* MyDriveShield website chat (AI assistant). Built 28/10/2026.
   Talks to the n8n workflow "MDS website chat agent" (webhook mds-chat).
   The assistant gives factual information only and hands over to a person for advice, complaints, claims and anything unusual. */
(function () {
  'use strict';
  if (window.__mdsChat) return; window.__mdsChat = true;
  var ENDPOINT = 'https://layden.app.n8n.cloud/webhook/mds-chat';
  var PHONE = '0477 666 500', EMAIL = 'info@mydriveshield.com.au';
  var KEY = 'mds_chat_v1';
  var GREETING = "Hi, I'm MyDriveShield's AI assistant. I can answer questions about our extended warranties and roadside assistance. I give factual information only, not advice. For anything personal, I can have a team member contact you.";
  var CHIPS = ['What does Absolute cover?', 'Hybrid or electric car?', 'Roadside prices', 'I bought my car privately'];

  function load() { try { return JSON.parse(sessionStorage.getItem(KEY)) || null; } catch (e) { return null; } }
  function save() { try { sessionStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
  function sid() { var a = new Uint8Array(9); (window.crypto || {}).getRandomValues ? crypto.getRandomValues(a) : a.forEach(function (_, i) { a[i] = Math.random() * 256; }); return 'c' + Array.prototype.map.call(a, function (b) { return ('0' + b.toString(16)).slice(-2); }).join(''); }
  var st = load() || { sid: sid(), msgs: [], open: false, done: false };
  function track(n, p) { try { if (window.mdsTrack) window.mdsTrack(n, p || {}); } catch (e) {} }

  var css = '' +
    '.mdsc-btn{position:fixed;right:18px;bottom:18px;z-index:2147483000;display:flex;align-items:center;gap:8px;background:#0B2545;color:#fff;border:0;border-radius:999px;padding:13px 18px 13px 15px;font:600 15px/1 Inter,system-ui,sans-serif;box-shadow:0 10px 28px rgba(11,37,69,.32);cursor:pointer}' +
    '.mdsc-btn:hover{background:#13315c}.mdsc-btn svg{flex:none}' +
    '.mdsc-btn.mdsc-hide{display:none}' +
    '.mdsc-panel{position:fixed;right:18px;bottom:18px;z-index:2147483001;width:380px;max-width:calc(100vw - 24px);height:600px;max-height:calc(100vh - 36px);background:#fff;border-radius:16px;box-shadow:0 18px 50px rgba(11,37,69,.28);display:none;flex-direction:column;overflow:hidden;font:15px/1.5 Inter,system-ui,sans-serif;color:#1f2937}' +
    '.mdsc-panel.open{display:flex}' +
    '.mdsc-hd{background:#0B2545;color:#fff;padding:14px 14px 12px 16px;display:flex;align-items:flex-start;gap:10px}' +
    '.mdsc-hd b{display:block;font-size:15.5px}.mdsc-hd small{display:block;font-size:12.5px;opacity:.85;margin-top:2px}' +
    '.mdsc-ai{display:inline-block;background:#F97316;color:#fff;font-size:11px;font-weight:700;border-radius:6px;padding:1px 6px;margin-left:6px;vertical-align:2px}' +
    '.mdsc-x{margin-left:auto;background:none;border:0;color:#fff;font-size:24px;line-height:1;cursor:pointer;padding:2px 4px;opacity:.9}' +
    '.mdsc-note{background:#F5F8FD;border-bottom:1px solid #E3EAF4;padding:8px 14px;font-size:12px;line-height:1.45;color:#4b5563}' +
    '.mdsc-note a{color:#0B2545;font-weight:600}' +
    '.mdsc-log{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px}' +
    '.mdsc-m{max-width:88%;padding:10px 12px;border-radius:14px;white-space:pre-wrap;word-wrap:break-word;font-size:14.5px}' +
    '.mdsc-m a{color:inherit;text-decoration:underline;font-weight:600;word-break:break-all}' +
    '.mdsc-a{background:#F1F4F9;align-self:flex-start;border-bottom-left-radius:4px}' +
    '.mdsc-u{background:#0B2545;color:#fff;align-self:flex-end;border-bottom-right-radius:4px}' +
    '.mdsc-chips{display:flex;flex-wrap:wrap;gap:6px}' +
    '.mdsc-chip{background:#fff;border:1px solid #C9D6EA;color:#0B2545;border-radius:999px;padding:6px 11px;font:600 13px Inter,system-ui,sans-serif;cursor:pointer}' +
    '.mdsc-chip:hover{background:#F0F5FF}' +
    '.mdsc-typing{align-self:flex-start;color:#6b7280;font-size:13px}' +
    '.mdsc-ft{border-top:1px solid #E5E7EB;padding:10px;display:flex;gap:8px;align-items:flex-end}' +
    '.mdsc-ft textarea{flex:1;resize:none;border:1px solid #D1D5DB;border-radius:10px;padding:9px 10px;font:15px/1.4 Inter,system-ui,sans-serif;max-height:110px;min-height:40px}' +
    '.mdsc-ft textarea:focus{outline:2px solid #93B4E8;border-color:#93B4E8}' +
    '.mdsc-send{background:#F97316;color:#fff;border:0;border-radius:10px;padding:0 14px;height:40px;font:700 14px Inter,system-ui,sans-serif;cursor:pointer}' +
    '.mdsc-send[disabled]{opacity:.5;cursor:default}' +
    '.mdsc-person{background:none;border:0;color:#0B2545;font:600 13px Inter,system-ui,sans-serif;text-decoration:underline;cursor:pointer;padding:0 14px 10px;text-align:left}' +
    '.mdsc-form{background:#FFF7EA;border:1px solid #F3C98B;border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:8px;align-self:stretch}' +
    '.mdsc-form b{font-size:14px;color:#0B2545}' +
    '.mdsc-form input[type=text],.mdsc-form input[type=tel],.mdsc-form input[type=email]{border:1px solid #D1D5DB;border-radius:8px;padding:8px 10px;font:14.5px Inter,system-ui,sans-serif;width:100%;box-sizing:border-box}' +
    '.mdsc-form label.mdsc-c{display:flex;gap:8px;font-size:12.5px;line-height:1.45;color:#374151;align-items:flex-start}' +
    '.mdsc-form .mdsc-err{color:#B42318;font-size:12.5px}' +
    '.mdsc-form button{background:#0B2545;color:#fff;border:0;border-radius:8px;padding:10px;font:700 14px Inter,system-ui,sans-serif;cursor:pointer}' +
    '@media (max-width:520px){.mdsc-panel{right:0;bottom:0;width:100vw;max-width:100vw;height:100%;max-height:100%;border-radius:0}.mdsc-btn{right:12px;bottom:12px;padding:12px 14px}.mdsc-btn span{display:none}}' +
    '@media print{.mdsc-btn,.mdsc-panel{display:none!important}}';
  var styleEl = document.createElement('style'); styleEl.textContent = css; document.head.appendChild(styleEl);

  var ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-4.2 3.6c-.5.4-1.3.1-1.3-.6V16A2.5 2.5 0 0 1 4 13.5v-8Z" fill="currentColor"/></svg>';
  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'mdsc-btn'; btn.setAttribute('aria-label', 'Open chat: ask a question');
  btn.innerHTML = ICON + '<span>Ask a question</span>';
  var panel = document.createElement('div');
  panel.className = 'mdsc-panel'; panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'MyDriveShield AI assistant chat');
  panel.innerHTML =
    '<div class="mdsc-hd"><div><b>MyDriveShield assistant<span class="mdsc-ai">AI</span></b><small>Usually answers in a few seconds</small></div><button type="button" class="mdsc-x" aria-label="Close chat">&times;</button></div>' +
    '<div class="mdsc-note">You are chatting with an AI system. It gives factual information only, not advice. Please don\'t share card, licence or health details. Chats are kept to help us respond. <a href="/privacy" target="_blank" rel="noopener">Privacy</a></div>' +
    '<div class="mdsc-log" aria-live="polite"></div>' +
    '<button type="button" class="mdsc-person">Talk to a person</button>' +
    '<div class="mdsc-ft"><textarea rows="1" maxlength="1000" placeholder="Type your question" aria-label="Your message"></textarea><button type="button" class="mdsc-send">Send</button></div>';

  var log = panel.querySelector('.mdsc-log'), ta = panel.querySelector('textarea'), send = panel.querySelector('.mdsc-send');
  var busy = false;

  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function linkify(t) {
    return esc(t).replace(/(https?:\/\/[^\s<]+[^\s<.,;:!?)\]'"])|(\s|^)(\/(?:extended-car-warranty|roadside-assistance|faq|private-sale-car-warranty|complaints|privacy)\/?)/g, function (m, url, pre, path) {
      if (url) return '<a href="' + url + '" target="_blank" rel="noopener">' + url + '</a>';
      return pre + '<a href="' + path + '">' + path + '</a>';
    }).replace(/\b(0477 666 500|1800 422 772)\b/g, function (n) { return '<a href="tel:' + n.replace(/\s/g, '') + '">' + n + '</a>'; });
  }
  function bubble(role, text) {
    var d = document.createElement('div'); d.className = 'mdsc-m ' + (role === 'user' ? 'mdsc-u' : 'mdsc-a');
    d.innerHTML = role === 'user' ? esc(text) : linkify(text); log.appendChild(d); return d;
  }
  function render() {
    log.innerHTML = ''; bubble('assistant', GREETING);
    if (!st.msgs.length) {
      var c = document.createElement('div'); c.className = 'mdsc-chips';
      CHIPS.forEach(function (q) { var b = document.createElement('button'); b.type = 'button'; b.className = 'mdsc-chip'; b.textContent = q; b.onclick = function () { ask(q); }; c.appendChild(b); });
      log.appendChild(c);
    }
    st.msgs.forEach(function (m) { bubble(m.role, m.content); });
    if (st.showForm && !st.done) showForm(st.formReason || '');
    if (st.done) bubble('assistant', 'Thanks. A MyDriveShield team member will contact you within one business day. If it is urgent, call ' + PHONE + ' (Mon to Fri).');
    scroll();
  }
  function scroll() { log.scrollTop = log.scrollHeight; }
  function openPanel(focus) {
    panel.classList.add('open'); btn.classList.add('mdsc-hide'); st.open = true; save();
    if (focus !== false) { setTimeout(function () { ta.focus(); }, 30); track('chat_open', { page: location.pathname }); }
    scroll();
  }
  function closePanel() { panel.classList.remove('open'); btn.classList.remove('mdsc-hide'); st.open = false; save(); btn.focus(); }
  btn.onclick = function () { openPanel(true); };
  panel.querySelector('.mdsc-x').onclick = closePanel;
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && panel.classList.contains('open')) closePanel(); });
  panel.querySelector('.mdsc-person').onclick = function () { showForm('Asked to talk to a person'); };
  send.onclick = function () { ask(ta.value); };
  ta.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(ta.value); } });
  ta.addEventListener('input', function () { ta.style.height = 'auto'; ta.style.height = Math.min(110, ta.scrollHeight) + 'px'; });

  function post(body) {
    return fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); });
  }
  function ask(text) {
    text = String(text || '').trim(); if (!text || busy) return;
    if (/\b(?:\d[ -]?){13,19}\b/.test(text)) { text = text.replace(/\b(?:\d[ -]?){13,19}\b/g, '[number removed]'); }
    ta.value = ''; ta.style.height = 'auto';
    var chips = log.querySelector('.mdsc-chips'); if (chips) chips.remove();
    st.msgs.push({ role: 'user', content: text }); save(); bubble('user', text); scroll();
    busy = true; send.disabled = true;
    var typing = document.createElement('div'); typing.className = 'mdsc-typing'; typing.textContent = 'Assistant is typing…'; log.appendChild(typing); scroll();
    track('chat_message', { n: st.msgs.length });
    post({ action: 'chat', sessionId: st.sid, page: location.pathname, messages: st.msgs.slice(-16) })
      .then(function (r) {
        var reply = (r && r.reply) || ('Sorry, I could not answer that. Please call ' + PHONE + ' or email ' + EMAIL + '.');
        st.msgs.push({ role: 'assistant', content: reply }); save(); typing.remove(); bubble('assistant', reply);
        if (r && r.handover) { st.formReason = r.reason || 'Handover'; showForm(st.formReason); }
      })
      .catch(function () {
        typing.remove();
        bubble('assistant', 'Sorry, the chat is not available right now. Please call ' + PHONE + ' (Mon to Fri) or email ' + EMAIL + '. You can also use the form below and we will contact you.');
        showForm('Chat unavailable');
      })
      .then(function () { busy = false; send.disabled = false; scroll(); });
  }
  function showForm(reason) {
    if (st.done) return; st.showForm = true; st.formReason = reason; save();
    var old = log.querySelector('.mdsc-form'); if (old) { old.scrollIntoView({ block: 'nearest' }); return; }
    var f = document.createElement('form'); f.className = 'mdsc-form'; f.noValidate = true;
    f.innerHTML = '<b>Have a team member contact you</b>' +
      '<input type="text" name="name" placeholder="Your name" autocomplete="name" maxlength="80" aria-label="Your name">' +
      '<input type="tel" name="phone" placeholder="Mobile or phone" autocomplete="tel" maxlength="30" aria-label="Phone">' +
      '<input type="email" name="email" placeholder="Email (optional if you give a phone)" autocomplete="email" maxlength="120" aria-label="Email">' +
      '<input type="text" name="besttime" placeholder="Best time to contact you (optional)" maxlength="80" aria-label="Best time to contact you">' +
      '<label class="mdsc-c"><input type="checkbox" name="consent"> <span>I agree to MyDriveShield contacting me about this enquiry by phone, SMS or email, and to this chat being kept with my enquiry.</span></label>' +
      '<div class="mdsc-err" role="alert"></div><button type="submit">Send my details</button>';
    f.onsubmit = function (e) {
      e.preventDefault();
      var v = function (n) { return (f.elements[n].value || '').trim(); };
      var err = f.querySelector('.mdsc-err'); err.textContent = '';
      var phone = v('phone'), email = v('email');
      if (!v('name')) { err.textContent = 'Please enter your name.'; return; }
      if (!phone && !email) { err.textContent = 'Please give a phone number or an email address.'; return; }
      if (phone && phone.replace(/\D/g, '').length < 8) { err.textContent = 'Please check the phone number.'; return; }
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { err.textContent = 'Please check the email address.'; return; }
      if (!f.elements.consent.checked) { err.textContent = 'Please tick the box so we can contact you.'; return; }
      var b = f.querySelector('button'); b.disabled = true; b.textContent = 'Sending…';
      post({ action: 'handover', sessionId: st.sid, page: location.pathname, messages: st.msgs.slice(-16),
        lead: { name: v('name'), phone: phone, email: email, besttime: v('besttime'), consent: true, reason: st.formReason || '' } })
        .then(function () { st.done = true; st.showForm = false; save(); f.remove(); track('chat_handover', {}); bubble('assistant', 'Thanks. A MyDriveShield team member will contact you within one business day. If it is urgent, call ' + PHONE + ' (Mon to Fri).'); scroll(); })
        .catch(function () { b.disabled = false; b.textContent = 'Send my details'; err.innerHTML = 'Sorry, that did not send. Please call <a href="tel:0477666500">' + PHONE + '</a> or email ' + EMAIL + '.'; });
    };
    log.appendChild(f); scroll();
  }

  function mount() { document.body.appendChild(btn); document.body.appendChild(panel); render(); }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
})();
