/*
 * References on hover (user, 2026-11-20: "Mousehover a referenced paper to see the full paper ... Use a fancy window").
 *
 * A lecture's sources come from window.REF_CARDS["lectures/lectureN/"], written by that lecture's generator (L10:
 * tools/build_l10_widgets.py, from the interactive slides): for each source, how the text cites it, "(Werling et
 * al., 2010)", its number on the references page, and its formatted entry. On the lecture's pages, each such citation
 * in the text opens a card beside it with the full reference. Hover shows the card; a click (or Enter) pins it, so its
 * links can be followed; a second click on the citation (or the close button) unpins it, never Esc or a click
 * elsewhere (user, 2026-11-21: "to pin and unpin a citation, click on the citation. do not use Esc to unpin"). The
 * references page itself is skipped:
 * its cards already show every entry. Colors are the theme's, so the card follows light and dark.
 */
(function () {
  "use strict";
  var all = window.REF_CARDS || {}, path = location.pathname, refs = null;
  Object.keys(all).forEach(function (k) { if (path.indexOf("/" + k) >= 0) refs = all[k]; });
  if (!refs || /references(\.html)?$/.test(path.replace(/\/$/, ""))) return;
  var root = document.querySelector("article.bd-article") || document.querySelector("main") || document.body;

  /* each in-text form to its source; a form two sources share is left alone; an empty form is dropped */
  var flat = function (t) { return t.replace(/\s+/g, " "); };
  var byForm = {};
  refs.forEach(function (r) { r.cite.forEach(function (c) { c = flat(c || "").trim(); if (c) (byForm[c] = byForm[c] || []).push(r); }); });
  var forms = Object.keys(byForm).filter(function (c) { return byForm[c].length === 1; });
  if (!forms.length) return;
  var esc = function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); };
  var re = new RegExp(forms.map(function (c) { return esc(c).replace(/ /g, "\\s+"); }).join("|"), "g");

  var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: function (n) {
    var p = n.parentElement;
    if (!p || p.closest("script, style, pre, code, svg, .math, mjx-container, .katex, .refcite, a, button, .headerlink")) return NodeFilter.FILTER_REJECT;
    re.lastIndex = 0; return re.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP; } });
  var nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(function (n) {
    var t = n.nodeValue, frag = document.createDocumentFragment(), last = 0, m; re.lastIndex = 0;
    while ((m = re.exec(t))) {
      frag.appendChild(document.createTextNode(t.slice(last, m.index)));
      var hit = byForm[flat(m[0])]; if (!hit) { frag.appendChild(document.createTextNode(m[0])); last = m.index + m[0].length; continue; }
      var s = document.createElement("span"); s.className = "refcite"; s.tabIndex = 0;
      s.dataset.key = hit[0].key; s.textContent = m[0];
      frag.appendChild(s); last = m.index + m[0].length; }
    frag.appendChild(document.createTextNode(t.slice(last))); n.parentNode.replaceChild(frag, n); });

  var byKey = {}; refs.forEach(function (r) { byKey[r.key] = r; });
  var card = document.createElement("div"); card.id = "refcard"; card.setAttribute("role", "dialog"); card.setAttribute("aria-label", "Reference");
  document.body.appendChild(card);
  var pinned = null, hideT = null;
  var BOOK = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M4 21.5A2.5 2.5 0 0 1 6.5 19H20v3H6.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>';
  function escHtml(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;"); }

  function place(el) {
    var r = el.getBoundingClientRect(), W = document.documentElement.clientWidth, H = innerHeight, g = 12;
    var w = Math.min(520, W - 2 * g); card.style.width = w + "px";
    var h = card.offsetHeight, below = H - r.bottom, above = r.top;
    var top = below >= h + g || below >= above ? r.bottom + 10 : r.top - h - 10;
    var left = Math.max(g, Math.min(W - w - g, r.left + r.width / 2 - w / 2));
    card.style.top = (Math.max(g, top) + scrollY) + "px"; card.style.left = (left + scrollX) + "px";
    card.classList.toggle("up", top < r.top); }
  function show(el) {
    clearTimeout(hideT); var r = byKey[el.dataset.key]; if (!r) return;
    card.innerHTML = '<div class="rc-h">' + BOOK + '<div><div class="rc-t">Reference [' + r.n + ']</div><div class="rc-k">' +
      escHtml(r.cite[0]) + '</div></div><button class="rc-x" aria-label="close">×</button></div>' +
      '<div class="rc-b">' + r.html + '</div><div class="rc-f">' +
      (pinned ? "Pinned: the links work. Click the citation again to unpin." : "Click the citation to pin this card.") + "</div>";
    card.querySelector(".rc-x").onclick = function (e) { e.stopPropagation(); unpin(); };
    card.style.display = "block"; place(el); requestAnimationFrame(function () { card.classList.add("show"); }); }
  function hide() { if (pinned) return; card.classList.remove("show"); hideT = setTimeout(function () { if (!pinned) card.style.display = "none"; }, 160); }
  function pin(el) { if (pinned) pinned.classList.remove("on"); pinned = el; el.classList.add("on"); card.classList.add("pinned"); show(el); }
  function unpin() { if (pinned) pinned.classList.remove("on"); pinned = null; card.classList.remove("pinned"); hide(); }

  root.querySelectorAll(".refcite").forEach(function (el) {
    el.addEventListener("mouseenter", function () { if (!pinned) show(el); });
    el.addEventListener("mouseleave", hide);
    el.addEventListener("focus", function () { if (!pinned) show(el); });
    el.addEventListener("blur", hide);
    el.addEventListener("click", function (e) { e.stopPropagation(); if (pinned === el) unpin(); else pin(el); });
    el.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); if (pinned === el) unpin(); else pin(el); } }); });
  card.addEventListener("click", function (e) { e.stopPropagation(); });
  addEventListener("resize", function () { if (pinned) place(pinned); });
})();
