/*
 * Open the "More detail" box a link points at.
 *
 * The lecture decks link to a closed dropdown by its anchor
 * (l10_lecture.html#l10-more-pp-steps). The browser scrolls to the box but
 * leaves it closed. This script opens the <details> element the URL's hash
 * names, or the one that holds it, on page load and whenever the hash
 * changes, then scrolls it into view.
 */
(function () {
  function openTarget() {
    if (!location.hash) return;
    var el = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!el) return;
    var box = el.tagName === "DETAILS" ? el : el.closest("details");
    if (!box) return;
    box.open = true;
    el.scrollIntoView();
  }
  document.addEventListener("DOMContentLoaded", openTarget);
  window.addEventListener("hashchange", openTarget);
})();
