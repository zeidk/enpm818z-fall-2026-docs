import os, sys
from datetime import date

project = "ENPM818Z Fall 2026"
author = "Z. Kootbally"
copyright = f"{date.today().year}, {author}"
release = "v1.0"

extensions = [
    "myst_parser",
    "sphinx.ext.autosummary",
    "sphinxcontrib.mermaid",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_proof",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
]

plantuml = "https://www.plantuml.com/plantuml/png/"
plantuml_output_format = "png"

# Prerender options for better performance
katex_prerender = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
proof_numbered = {
    "theorem": True,
    "lemma": True,
    "algorithm": True,
    "example": False,
}

todo_include_todos = True

templates_path = ["_templates"]
# ---------------------------------------------------------------------------
# What is published.
#
# L1 to L4 are published in full.
#
# L5: the index and code pages are published; the lecture, appendix,
# exercises, quiz and references pages are held back until the user
# publishes them. All five are rewritten from the deck (2026-10-09).
#
# L6 to L14 are hidden completely: they do not match the syllabus yet and
# open one at a time as their decks are finished. To reopen lecture N:
#   1. remove N from HIDDEN_LECTURES below,
#   2. restore its line in the toctree of lectures/index.rst,
#   3. turn its plain-text tags ("L7") back into links,
#      :doc:`L7 </lectures/lecture7/l7_index>`, in the glossary and on the
#      pages that mention it.
# The source files stay on disk.
# ---------------------------------------------------------------------------
HIDDEN_LECTURES = range(6, 15)

exclude_patterns = [
    f"lectures/lecture5/l5_{page}.rst"
    for page in ("lecture", "appendix", "exercises", "quiz", "references")
]
exclude_patterns += [f"lectures/lecture{n}/**" for n in HIDDEN_LECTURES]

# GP2--GP4 are held back until they are posted. Remove an entry here (and
# restore its toctree line in assignments/index.rst) to publish it.
exclude_patterns += [f"assignments/gp{n}.rst" for n in range(2, 5)]

# ---------------------------------------------------------------------------
# PyData Sphinx Theme
# ---------------------------------------------------------------------------
html_theme = "pydata_sphinx_theme"

html_theme_options = {
    # Logo (place files in _static/images/)
    "logo": {
        # No text: the logo already says ENPM818Z, and both linked to the home page.
        "alt_text": "ENPM818Z Fall 2026, home",
        "image_light": "_static/images/enpm818z_logo_light.svg",
        "image_dark": "_static/images/enpm818z_logo_dark.svg",
    },
    # Header / navbar icon links
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/zeidk/enpm818z-fall-2026-docs",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
    "back_to_top_button": True,
    # Light/dark mode toggle
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    # Navigation
    "header_links_before_dropdown": 7,
    "navigation_depth": 3,
    "show_nav_level": 1,
    "show_toc_level": 1,
    "show_prev_next": True,
    # Footer
    "footer_start": ["copyright"],
    "footer_end": ["theme-version"],
    # Syntax highlighting for light and dark modes
    "pygments_light_style": "igor",
    "pygments_dark_style": "nord",
}

# Edit on GitHub button
html_context = {
    "github_user": "zeidk",
    "github_repo": "enpm818z-fall-2026-docs",
    "github_version": "main",
    "doc_path": "docs/source",
    "default_mode": "dark",
}

numfig = True
numfig_format = {
    "pseudocode": "Algorithm %s",
}

html_static_path = ["_static"]
master_doc = "index"

html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css", "my.css"
]

html_js_files = [
    # Shape of the Read the Docs version menu; see the file's header.
    ("flyout-style.js", {"defer": "defer"}),
]