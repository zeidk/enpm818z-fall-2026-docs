/* Figures with a light and a dark version (2026-11-20). A figure tagged
   `:class: dark-light themed-L10` (docutils writes the class as themed-l10) shows <name>.png in the light theme and
   _static/images/L10/<name>_dark.png in the dark theme. Sphinx copies the light
   file to _images/; the dark one is served from _static/. The pydata theme
   leaves "dark-light" images undimmed and without their white card. */
(function () {
  /* the lowercased class tag -> the folder under _static/images/ */
  var FOLDERS = {};
  ["L1","L2","L3","L4","L5","L6","L7","L8","L9","L10","L11","L12","L13","GP1","GP2","GP3","GP4","GP5","SLAM","filters"].forEach(function (f) { FOLDERS[f.toLowerCase()] = f; });
  function root() {
    var r = document.documentElement.dataset.content_root;
    if (r !== undefined) return r;
    var s = document.querySelector('script[src*="themed-figs.js"]');
    return s ? s.getAttribute("src").replace(/_static\/themed-figs\.js.*$/, "") : "";
  }
  function apply() {
    var dark = document.documentElement.getAttribute("data-theme") === "dark", base = root();
    document.querySelectorAll('img.dark-light[class*="themed-"]').forEach(function (img) {
      if (!img.dataset.light) {
        var tag = (img.className.match(/themed-(\w+)/) || [])[1] || "";   /* docutils lowercases classes */
        var lec = FOLDERS[tag] || tag;
        var name = img.getAttribute("src").split("/").pop().replace(/\.png$/, "");
        img.dataset.light = img.getAttribute("src");
        img.dataset.dark = base + "_static/images/" + lec + "/" + name + "_dark.png";
      }
      var want = dark ? img.dataset.dark : img.dataset.light;
      if (img.getAttribute("src") !== want) img.setAttribute("src", want);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", apply); else apply();
  new MutationObserver(apply).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
})();
