/*
 * Read the Docs version menu: shape and logo.
 *
 * Read the Docs adds <readthedocs-flyout> to every page it hosts. The
 * menu is a Lit element with an open shadow root, so the site's CSS can
 * reach it only through custom properties (colors and font, in my.css).
 * This script appends one more stylesheet inside the shadow root for
 * what custom properties cannot do: rounded corners, a border, a shadow,
 * the search box, and a dark logo on the light theme. Every value is a
 * theme variable, so the menu follows the light/dark toggle.
 *
 * On a local build there is no menu, and this script does nothing.
 */
(function () {
  "use strict";

  const CSS = `
    .container {
      border: 1px solid var(--pst-color-border);
      border-radius: 0.5rem;
      box-shadow: 0 0.25rem 1rem var(--pst-color-shadow);
    }
    header {
      border-radius: 0.5rem 0.5rem 0 0;
    }
    header > img.logo {
      filter: var(--enpm-flyout-logo-filter, none);
    }
    header svg {
      color: var(--pst-color-text-muted);
    }
    dd a:hover {
      color: var(--pst-color-link-hover);
      text-decoration: underline;
    }
    dd input {
      background-color: var(--pst-color-background);
      color: var(--pst-color-text-base);
      border: 1px solid var(--pst-color-border);
      border-radius: 0.25rem;
    }
  `;

  function style(element) {
    const root = element.shadowRoot;
    if (!root || element.hasAttribute("data-enpm-styled")) {
      return;
    }
    const sheet = new CSSStyleSheet();
    sheet.replaceSync(CSS);
    // Append, so the menu's own sheet stays and ours wins ties.
    root.adoptedStyleSheets = [...root.adoptedStyleSheets, sheet];
    element.setAttribute("data-enpm-styled", "");
  }

  function styleAll() {
    document.querySelectorAll("readthedocs-flyout").forEach(style);
  }

  // The menu is defined and inserted by Read the Docs after the page loads.
  customElements.whenDefined("readthedocs-flyout").then(function () {
    styleAll();
    new MutationObserver(styleAll).observe(document.body, {
      childList: true,
      subtree: true,
    });
  });
})();
