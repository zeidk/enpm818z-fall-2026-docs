/* Desktop hide/unhide for the left section navigation, with memory.
 *
 * The theme ships a .primary-toggle button, a hidden checkbox and a click
 * handler, all built for mobile, where "checked" means the drawer is OPEN.
 * On desktop the sidebar is shown by default, so the meaning is inverted.
 * Sharing the theme's handler caused two problems:
 *
 *   - after collapsing, the theme focused the first link inside the
 *     sidebar we had just hidden, so focus landed on nothing;
 *   - the two handlers had to agree about the checkbox, which is fragile.
 *
 * So on desktop we intercept the click during the CAPTURE phase on
 * document, before it reaches the button, and handle it ourselves. Below
 * 960px we do nothing at all and the theme behaves exactly as shipped.
 */
(function () {
  "use strict";

  var KEY = "pst-primary-sidebar-collapsed";
  var CLS = "pst-primary-collapsed";
  var WIDE = "(min-width: 960px)";
  var root = document.documentElement;

  function isWide() {
    return window.matchMedia(WIDE).matches;
  }

  function read() {
    try {
      return localStorage.getItem(KEY) === "1";
    } catch (e) {
      return false; // blocked storage: start expanded
    }
  }

  function write(collapsed) {
    try {
      localStorage.setItem(KEY, collapsed ? "1" : "0");
    } catch (e) {
      /* the toggle still works for this page */
    }
  }

  // Apply the stored state before first paint, so nothing flashes.
  if (read()) {
    root.classList.add(CLS);
  }

  document.addEventListener(
    "click",
    function (ev) {
      if (!isWide()) {
        return; // mobile: leave the theme's drawer alone
      }
      var target = ev.target;
      if (!target || !target.closest) {
        return;
      }
      if (!target.closest(".primary-toggle")) {
        return;
      }

      // Stop the event before the theme's own handler sees it.
      ev.preventDefault();
      ev.stopPropagation();

      var collapsed = !root.classList.contains(CLS);
      root.classList.toggle(CLS, collapsed);
      write(collapsed);

      // Keep the theme's checkbox in step, so that resizing down to
      // mobile does not start with the drawer in a stale state.
      var box = document.getElementById("pst-primary-sidebar-checkbox");
      if (box) {
        box.checked = false;
      }
    },
    true // capture: runs before the listener on the button itself
  );
})();
