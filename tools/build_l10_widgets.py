#!/usr/bin/env python3
"""Build the L10 lecture page's interactive widgets from the interactive slides.

Source: the interactive slides page as the docs serve it,
docs/source/_extra/lectures/lecture10/interactive/L10_interactive.html (tools/sync_l10_interactive.sh copies
it from the slides repo). Run tools/sync_l10_interactive.sh first, then this script, from the docs repo root.

Writes:
  docs/source/_static/l10w/l10w.css       the slides' widget styles, scoped to .l10w, sized for the docs column
  docs/source/_static/l10w/l10w-data.js   the slides' DATA (the curve, the runs, the planner settings)
  docs/source/_static/l10w/l10w-core.js   the slides' helpers and widget code, without the slide navigation
  docs/source/lectures/lecture10/widgets/<name>.html   one panel per widget, included by l10_lecture.rst
  docs/source/lectures/lecture10/widgets/_head.html, _scripts.html   loaded once, before the first and after the last panel

Each panel is one slide's content (its title, controls, drawing and readouts), with the slide's numbers and words.
The slides stay the source: change a slide there, sync, then run this script again.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs/source/_extra/lectures/lecture10/interactive/L10_interactive.html"
STATIC = ROOT / "docs/source/_static/l10w"
WDIR = ROOT / "docs/source/lectures/lecture10/widgets"

# name, a key that finds the slide (an element id in it, or h2: and the start of its title), the docs label it goes
# under, and the sentence before it in the docs. Parts that belong together (a slide's 1 of 2 and 2 of 2) are joined.
WIDGETS = [
    ("feedback", ["fb-table"], "l10-lec-two-controllers", "Click a row of the table: the note under it says what that controller compares and sends."),
    ("clocks", ["clk"], "l10-lec-clocks", "Press the button to play one second, ten times slower, and watch both clocks tick while the AV moves."),
    ("flat-fsm", ["ff", "ff-issue"], "l10-lec-flat-fsm", "Pick how many behaviors and modes the flat FSM has, and count the states it needs."),
    ("superstate", ["fsm"], "l10-lec-superstate", "Switch between the flat FSM and the superstate, and count the arrows in each."),
    ("bt-read", ["tk"], "l10-lec-bt-read", "Tick the tree with each button and follow which nodes run and what each one returns."),
    ("bt-ticks", ["bt"], "l10-lec-bt-ticks", "Play the two ticks, or flip a condition, and see which behavior the tree picks."),
    ("horizon", ["hz-t"], "l10-lec-path-key", "Pick a speed and read how far ahead the path then has to reach."),
    ("u", ["u-s"], "l10-lec-u", "Move the point s along the road and read how far through the move it is."),
    ("qu", ["q-u"], "l10-lec-qu", "Move u from 0 to 1 and see how much of the shift q(u) has done."),
    ("candidate", ["s-path"], "l10-lec-candidate-formula", "Move the point s, or change the length, and read d(s) for candidate A."),
    ("traj-scene", ["sc"], "l10-lec-traj-scene", "Move the time and see where car B and the AV are at that moment."),
    ("dt-numbers", ["t-T", "trajplot"], "l10-lec-traj-dt-numbers", "Pick the end offset and the duration, and see the quintic d(t) that meets them."),
    ("st-example", ["stx-plot"], "l10-lec-traj-lon-example", "Change the start speed, the end speed and the duration, and see where s(t) ends."),
    ("st-numbers", ["st-t"], "l10-lec-traj-quartic", "Move the time and read s(t), its speed and its acceleration."),
    ("traj-check", ["t-check"], "l10-lec-traj-check", "Press the button to check every candidate at its own time and count the ones kept."),
    ("traj-pick", ["x-traj-pick"], "l10-lec-traj-check", "Pick one candidate and see why the check keeps it or drops it."),
    ("traj-live", ["x-traj-live"], "l10-lec-traj-pick", "Generate the 324 candidates, check each one and play the plan the planner picks."),
    ("cap", ["cap-a"], "l10-lec-profile-1", "Change the sideways acceleration limit and read the speed cap on each arc."),
    ("profile", ["sp-a"], "l10-lec-profile-2", "Change the limit or move along the path, and see the speed profile brake before the curve."),
    ("ackermann", ["ak"], "l10-lec-ackermann", "Change the turn radius and read the angle of each front wheel."),
    ("turn-rate", ["tr-d"], "l10-lec-bicycle-eq", "Change the steering angle and the speed, and read the turn rate."),
    ("steer-curvature", ["v-d"], "l10-lec-steer-curvature", "Change the steering angle, or pick one of the curve's arcs, and see the circle the AV drives."),
    ("model-limit", ["lim-k"], "l10-lec-model-stops", "Change the curvature and the speed, and see when the sideways acceleration gets too high."),
    ("steer-videos", ["x-steer-videos"], "l10-lec-ctrl-compare", "Pick a controller to watch its run on our curve."),
    ("pp-law", ["law-a"], "l10-lec-pp-law", "Change the angle and the lookahead, and read the arc and the steering angle."),
    ("lookahead-runs", ["pp-table", "pp-fixed"], "l10-lec-ld-speed", "Click a run in the table, or pick a lookahead, and see how far the AV strays from the path."),
    ("speed-loop", ["hs-v"], "l10-lec-speed-loop", "Change the AV's speed and read what the loop compares and sends."),
    ("pedal", ["pd-u"], "l10-lec-speed-model", "Move the command u and see which pedal it presses and how hard."),
    ("lag", ["lag"], "l10-lec-speed-model", "Move the time and see how the engine's push catches up with the command."),
    ("drag", ["air-v", "dr-v"], "l10-lec-speed-drag", "Change the speed and read how hard drag pulls back."),
    ("ghost", ["gh0-run"], "l10-lec-p-def", "Play the run, or move the time, and compare the AV with a ghost car that holds the target speed perfectly."),
    ("p", ["gh1"], "l10-lec-p", "Move the time and see the P term push in proportion to the error."),
    ("p-steps", ["tw-pal"], "l10-lec-p", "Click a row of the table for its explanation."),
    ("i-def", ["tw-i8"], "l10-lec-i-def", "Click a row of the table for its explanation."),
    ("pi", ["gh2"], "l10-lec-pi", "Move the time and see the I term keep pushing after the error is gone."),
    ("windup", ["tw-ip"], "l10-lec-windup", "Click a row of the table for its explanation."),
    ("clamp", ["s-pid"], "l10-lec-clamp", "Change the gains, turn the clamp on or off, and play the run."),
    ("d-def", ["gh3"], "l10-lec-d-def", "Move the time and see the D term ease off as the error closes."),
    ("d-steps", ["tw-d"], "l10-lec-d-def", "Click a row of the table for its explanation."),
    ("pid-moment", ["gh0-run2"], "l10-lec-pid-compare", "Pick a controller and move the time, and read its P, I and D terms at that moment."),
    ("pid-block", ["pidb"], "l10-lec-pid-formula", "Change the speed and the gains, and follow the error through the PID to the command."),
    ("control-step", ["cstep"], "l10-lec-control-loop", "Click each step, or play them all slowly, and see what that step computes."),
    ("tune", ["h2:Tune by symptom"], "l10-lec-tune-symptom", "Click a symptom to see the fix and what it did on our curve."),
]

SVG_TAGS = {"svg", "g", "path", "text", "tspan", "line", "rect", "circle", "ellipse", "polyline", "polygon", "use", "defs",
            "marker", "clipPath", "linearGradient", "stop", "pattern", "mask", "symbol", "image", "foreignObject"}


def die(msg):
    sys.exit("build_l10_widgets: " + msg)


def px_to_u(value, font=False):
    """Frame px to the docs column: N px becomes calc(N * var(--u)); fonts keep a floor; 1 to 5 px stay (borders)."""
    def one(m):
        n = float(m.group(1))
        return m.group(0) if n < 6 else f"calc({m.group(1)} * var(--u))"
    if font:
        m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)px\s*(!important)?\s*", value)
        if m:
            return f"max(var(--fmin), calc({m.group(1)} * var(--u))){(' ' + m.group(2)) if m.group(2) else ''}"
    return re.sub(r"(?<![\w.#-])(\d+(?:\.\d+)?)px", one, value)


def scale_decls(decls):
    out = []
    for d in decls.split(";"):
        if ":" not in d:
            out.append(d)
            continue
        k, v = d.split(":", 1)
        prop = k.strip().lower()
        if prop.startswith("--") or prop in ("border", "border-top", "border-bottom", "border-left", "border-right",
                                             "outline", "outline-offset", "box-shadow", "text-shadow", "stroke-width"):
            out.append(d)
        else:
            out.append(k + ":" + px_to_u(v, font=(prop == "font-size")))
    return ";".join(out)


# ---------------------------------------------------------------- CSS
DROP = re.compile(r"^(html|body|\*$|#viewport|#world|#title|#nav|#where|#corner|#hotspot|#help|#ink|#laser|#modebadge|"
                  r"#deck|#band|#icons|\.secblock|\.sechead|\.card|\.opener|\.toc|\.lo\b|\.stack|\.pipe|svg\.pipe|\.handoff|"
                  r"\.hcard|\.harrow|\.av-|\.grid$|\.fitin|\.tyre-|\.clockrow|\.refs)")


def map_selector(sel):
    sel = sel.strip()
    if not sel:
        return None
    if sel.startswith("#whypop"):
        return sel                                    # the row popup sits on <body> with the class l10w
    dark = False
    m = re.match(r':root\[data-theme="dark"\]\s*(.*)$', sel)
    if m:
        dark, sel = True, m.group(1)
    if sel in (":root", ""):
        return 'html[data-theme="dark"] .l10w' if dark else ".l10w"
    if sel == "*":
        return ".l10w, .l10w *"
    # the slide box itself and its chrome
    if re.match(r"^(\.plate|\.frame)(\.\w+|:[\w()-.]+|::\w+)*$", sel) or re.match(r"^\.plate( \.bolt|::|\.plan|:not)", sel) \
            or re.match(r"^\.frame( > \.fit| \.fhead| h2|:not\(\.titlepage\)|\.titlepage)", sel) or sel.startswith(("body.", ".plate .bolt")):
        return None
    sel = re.sub(r"^(\.plate|\.frame)\s+", "", sel)
    if DROP.match(sel):
        return None
    return ('html[data-theme="dark"] .l10w ' if dark else ".l10w ") + sel


def split_selectors(prelude):
    """Split a selector list at the commas outside parentheses (:is(a,b) stays whole)."""
    out, depth, cur = [], 0, ""
    for ch in prelude:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    return out + [cur]


def parse_rules(css):
    """Top-level rules as (prelude, body); @media and @supports bodies are parsed again by the caller."""
    i, n, out = 0, len(css), []
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        prelude = css[i:j].strip()
        depth, k = 1, j + 1
        while depth and k < n:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        out.append((prelude, css[j + 1:k - 1]))
        i = k
    return out


def scope_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = []
    for prelude, body in parse_rules(css):
        if prelude.startswith("@font-face"):
            continue
        if prelude.startswith("@keyframes"):
            out.append(f"{prelude}{{{body}}}")
            continue
        if prelude.startswith("@media"):
            inner = scope_css(body)
            if inner.strip():
                out.append(f"{prelude}{{\n{inner}\n}}")
            continue
        sels = [s for s in (map_selector(p) for p in split_selectors(prelude)) if s]
        if sels:
            out.append(",".join(sels) + "{" + scale_decls(body) + "}")
    return "\n".join(out)


FONTS = [("Sans", "Light", 300, "normal"), ("Sans", "Regular", 400, "normal"), ("Sans", "Italic", 400, "italic"),
         ("Sans", "SemiBold", 600, "normal"), ("Sans", "SemiBoldItalic", 600, "italic"), ("Sans", "Bold", 700, "normal"),
         ("Sans", "BoldItalic", 700, "italic"), ("Mono", "Regular", 400, "normal"), ("Mono", "Bold", 700, "normal")]
# the slides' own fonts (SIL OFL, in the slides' asset folder), under their own family names so the rest of the page
# keeps its fonts; the path is from _static/l10w/ to the slides' copy that the docs serve
FONT_FACES = "".join(
    f'@font-face{{font-family:"L10W Fira {fam}";font-style:{st};font-weight:{w};font-display:swap;'
    f'src:url("../../lectures/lecture10/interactive/L10_interactive_assets/fonts/Fira{fam}-{n}.woff2") format("woff2")}}\n'
    for fam, n, w, st in FONTS)


DOCS_CSS = r"""/* Generated by tools/build_l10_widgets.py from the L10 interactive slides: do not edit by hand.
   Each .l10w panel is one slide's content. Sizes are the slides' frame px times --u, so a panel keeps the slide's
   proportions in the docs column; text never goes under --fmin. Nothing here styles the rest of the page. */
.l10w{display:block;margin:1.1em 0 1.6em;padding:12px 14px 14px;border:1px solid var(--plate-edge);border-radius:10px;
  background:var(--plate);color:var(--ink);font-family:"Fira Sans","Segoe UI",system-ui,sans-serif;line-height:1.35}
/* the docs theme loads Bootstrap: its .row (negative margins, every child 100% wide) must not reach the slides' .row */
.l10w .row{margin-left:0;margin-right:0;--bs-gutter-x:0;--bs-gutter-y:0}
.l10w .row > *{width:auto;max-width:none;margin-top:0;flex-shrink:0}
.l10w .l10w-title{font-weight:700;color:var(--slate);margin:0 0 6px;font-size:1.02em}
.l10w .l10w-title .l10w-kick{display:inline-block;font-size:.78em;font-weight:700;color:var(--on-accent);background:var(--live);
  border-radius:5px;padding:1px 7px;margin-right:8px;vertical-align:1px}
/* position:relative: the math's hidden screen-reader copy (position:absolute) stays inside the panel's own scroll box */
.l10w .l10w-in{container-type:inline-size;--fmin:13px;overflow-x:auto;position:relative}
.l10w .rng .rv{font-size:max(11px, calc(20 * var(--u)))}
/* --u: one slide frame px in this column (1164 px of slide content); on a phone it stops at 0.42 px, so controls stay
   usable and a wide panel scrolls inside itself instead of the page */
.l10w .l10w-in > *{--u:max(calc(100cqw / 1164), 0.42px);font-size:max(var(--fmin), calc(27 * var(--u)))}
/* the page's inline-code colors do not belong in a panel */
.l10w code,.l10w .code{color:inherit;background:none;border:0;padding:0;font-family:"L10W Fira Mono","Fira Mono",monospace}
.l10w .l10w-in svg.plot,.l10w .l10w-in img,.l10w .l10w-in video{max-width:100%;height:auto}
.l10w table{width:100%}
.l10w ul,.l10w ol{margin-top:.2em;margin-bottom:.2em}
.l10w p{margin:.3em 0}
@container (max-width: 620px){
  .l10w .two,.l10w .tlf .two{display:block !important}
  .l10w .two > *{margin-bottom:8px}
  .l10w .row{flex-wrap:wrap}
}
"""


# ---------------------------------------------------------------- panels
def find_section(s, key):
    for m in re.finditer(r'<section class="plate frame[^"]*"[^>]*>.*?</section>', s, re.S):
        body = m.group(0)
        if key.startswith("h2:"):
            h = re.search(r"<h2>(.*?)</h2>", body, re.S)
            if h and re.sub("<[^>]+>", "", h.group(1)).startswith(key[3:]):
                return body
        elif f'id="{key}"' in body:
            return body
    die(f"no slide holds {key!r}")


def section_parts(sec):
    h = re.search(r"<h2>(.*?)</h2>", sec, re.S)
    title = re.sub(r"^Try it:\s*", "", h.group(1).strip()) if h else ""    # the panel's badge already says it
    body = sec[h.end():] if h else sec
    body = re.sub(r"</section>\s*$", "", body.strip())
    body = re.sub(r'^\s*<div class="fit"><div class="fitin">', "", body)
    body = re.sub(r"</div></div>\s*$", "", body.strip())
    body = re.sub(r'<p class="docs">.*?</p>', "", body, flags=re.S)          # "more detail in the docs": these are the docs
    cls = re.match(r'<section class="plate frame([^"]*)"', sec).group(1).split()
    cls = [c for c in cls if c not in ("plan", "follow", "extra")]       # the slide's own classes (tlf) stay
    return title, body.strip(), cls


# in-text forms the docs write differently from the slides' bib authors (user, 2026-11-20: references on hover)
REF_ALIASES = {"bosch1991can": ["(Bosch, 1991)"], "btcpp": ["(BehaviorTree.CPP, 2026)"]}


def write_refs(page):
    """_static/l10w/l10-refs.js: for each L10 source, how the text cites it and its formatted entry, both taken from the
    slides page (its BIB and its references slides), for _static/ref-cards.js."""
    bib = json.loads(re.search(r"var BIB = (\{.*?\});", page, re.S).group(1))
    norm = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
    plain = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h))
    lis = re.findall(r'<li value="(\d+)">(.*?)</li>', page, re.S)
    refs = []
    for key, b in bib.items():
        hit = [(n, h) for n, h in lis if b["title"] and norm(b["title"]) in norm(plain(h))]
        if not hit:
            continue
        forms = ([b["cite"]] if b["cite"] else []) + REF_ALIASES.get(key, [])
        refs.append({"key": key, "n": int(hit[0][0]), "cite": forms, "html": hit[0][1].strip()})
    if len(refs) < 20:
        die(f"only {len(refs)} references matched their entries")
    (STATIC / "l10-refs.js").write_text("/* Generated by tools/build_l10_widgets.py from the L10 interactive slides: the sources, how the text cites them,\n"
                                        "   and their formatted entries, for _static/ref-cards.js. */\n"
                                        "window.REF_CARDS = window.REF_CARDS || {};\nwindow.REF_CARDS[\"lectures/lecture10/\"] = "
                                        + json.dumps(refs, ensure_ascii=False) + ";\n")


def deck_words(text):
    """On a docs page the slides' own name for themselves reads wrong: "the deck's runs" becomes "the lecture's runs",
    "(the deck shows 3.0 s)" becomes "(the lecture uses 3.0 s)". Only these phrases: the code's "deck" ids stay."""
    for old, new in (("the deck shows", "the lecture uses"), ("The deck's", "The lecture's"), ("the deck's", "the lecture's")):
        text = text.replace(old, new)
    return text


def fix_markup(html_):
    html_ = re.sub(r"<style>(.*?)</style>", lambda m: "<style>" + scope_css(m.group(1)) + "</style>", html_, flags=re.S)
    html_ = re.sub(r'((?:src|poster|data-dark|data-light)=")(L10_interactive_(?:assets|media)/)', r"\1interactive/\2", html_)

    def style(m):
        return f'style="{scale_decls(m.group(1))}"'
    html_ = re.sub(r'style="([^"]*)"', style, html_)

    def sized(m):                                      # svg, img and video with a width attribute: keep the slide's share
        tag, attrs = m.group(1), m.group(2)
        w = re.search(r'\swidth="(\d+(?:\.\d+)?)"', attrs)
        if not w:
            return m.group(0)
        add = f"width:calc({w.group(1)} * var(--u));max-width:100%;height:auto"
        if 'style="' in attrs:
            attrs = attrs.replace('style="', f'style="{add};', 1)
        else:
            attrs += f' style="{add}"'
        return f"<{tag}{attrs}>"
    return re.sub(r"<(svg|img|video)(\s[^>]*)>", sized, html_)


# ---------------------------------------------------------------- script
def between(text, a, b):
    i = text.find(a)
    j = text.find(b, i + 1)
    if i < 0 or j < 0:
        die(f"marker not found: {a!r} or {b!r}")
    return text[i:j]


def build_js(main, page, names):
    head = []
    for pat in (r'var reduce = [^\n]*;', r'var C = \{.*?\};'):
        m = re.search(pat, main, re.S)
        if not m:
            die("not found in the slides' script: " + pat)
        head.append(m.group(0))
    m = re.search(r'NS = "[^"]+", FONT = "[^"]+"', main)
    head.append("var " + m.group(0).replace('FONT = "Fira Sans', 'FONT = "L10W Fira Sans, Fira Sans') + ";")
    theme = re.search(r"function themeFigs\(\)\{.*?\}\); \}", main, re.S).group(0)
    why = between(main, "function whyPop(){", "document.addEventListener(\"keydown\", function(e){ var tg")
    why = why.replace('w.id = "whypop";', 'w.id = "whypop"; w.className = "l10w";')
    helpers = between(main, "/* ---------- small helpers", "/* ---------- the lecture's flowchart")
    helpers = helpers.replace('mathIn(document.getElementById("deck"));', "")
    helpers = helpers.replace('var w = r.clientWidth || parseFloat(r.getAttribute("width")) || vb.width;',
                              'var inn = r.closest && r.closest(".l10w-in"), w = r.clientWidth && inn && inn.clientWidth ? r.clientWidth * 1164 / inn.clientWidth '
                              ': parseFloat(r.getAttribute("width")) || vb.width;   /* in the slide\'s own frame px (1164 px of content) */')
    if "the slide's own frame px" not in helpers:
        die("svgScale changed in the slides: update build_l10_widgets.py")
    widgets = between(main, "/* ---------- 1: FSM", "/* ---------- the cover's satellite")
    live = main[main.find("/* ---------- live values"):]
    live = live[:live.find("})();") + len("})();")]

    # the widget code: slide scenes do not exist here
    widgets = re.sub(r'\w+\.closest\("\.plate"\)\.dataset\.scene !== current', "false", widgets)
    widgets = widgets.replace('document.getElementById("cstep").dataset.scene !== current', "false")
    widgets = widgets.replace('document.querySelectorAll(".tile")', 'document.querySelectorAll(".l10w .tile")')
    widgets = widgets.replace("document.querySelectorAll('input[type=\"range\"]')", "document.querySelectorAll('.l10w input[type=\"range\"]')")
    widgets = re.sub(r'"L10_interactive_(assets|media)/', r'"interactive/L10_interactive_\1/', widgets)
    if re.search(r"\bcurrent\b(?!\")", re.sub(r'aria-current', "", widgets)):
        for x in re.finditer(r".{50}\bcurrent\b.{30}", re.sub(r'aria-current', "", widgets)):
            print("  check:", x.group(0))
    live = live.replace('.closest(".plate, .card")', '.closest(".l10w")')
    if '.closest(".l10w")' not in live:
        die("live values block changed in the slides: update build_l10_widgets.py")

    tags = {}
    for m2 in re.finditer(r"<([a-zA-Z]+)\b[^>]*\sid=\"([\w-]+)\"", page):
        tags.setdefault(m2.group(2), m2.group(1))
    body = "\n".join(head) + f"""
var {", ".join(f"{n} = window.L10W_VARS.{n}" for n in names)}, current = null;
var TAGS = {json.dumps(tags, separators=(",", ":"))}, SVGT = {json.dumps({t: 1 for t in SVG_TAGS}, separators=(",", ":"))};
/* an element a widget asks for: the page's, or a detached one when its panel is not on this page */
function $id(id){{ var e = document.getElementById(id); if (e) return e; var t = TAGS[id] || "div";
  e = SVGT[t] ? document.createElementNS(NS, t) : document.createElement(t); e.id = id; return e; }}
{theme}
themeFigs(); new MutationObserver(themeFigs).observe(document.documentElement, {{attributes:true, attributeFilter:["data-theme"]}});
{why}
{helpers}
document.querySelectorAll(".l10w").forEach(function(w){{ mathIn(w); }});
{widgets}
{live}
"""
    # the slider's value label: the deck's thumb is 78 px, here it scales with the column, so measure it, and move the
    # label and the ticks again when the column changes width
    old = ('function place(){ var W = inp.offsetWidth || parseFloat(getComputedStyle(inp).width) || 320, k = (+inp.value - lo) / (hi - lo);\n'
           '    rv.style.left = (k * (W - TW)) + "px"; rv.textContent = rangeText(inp); }')
    if old not in body:
        die("the slider label code changed in the slides: update build_l10_widgets.py")
    body = body.replace(old, 'function place(){ TW = rv.offsetWidth || TW; var W = inp.offsetWidth || parseFloat(getComputedStyle(inp).width) || 320, '
                        'k = (+inp.value - lo) / (hi - lo);\n    rv.style.left = (k * (W - TW)) + "px"; rv.textContent = rangeText(inp);\n'
                        '    w.querySelectorAll(".tk").forEach(function(t){ t.style.left = (TW / 2 + (+t.title - lo) / (hi - lo) * (W - TW)) + "px"; }); }\n'
                        '  if (window.ResizeObserver) new ResizeObserver(function(){ place(); }).observe(inp);')
    body = deck_words(body)
    body = body.replace("document.getElementById(", "$id(")
    body = body.replace("function $id(id){ var e = $id(id);", "function $id(id){ var e = document.getElementById(id);")
    return ("/* Generated by tools/build_l10_widgets.py from the L10 interactive slides: do not edit by hand. */\n"
            "(function(){\n\"use strict\";\nif (!document.querySelector(\".l10w\")) return;\n" + body + "\n})();\n")


def main():
    if not SRC.exists():
        die(f"{SRC} not found: run tools/sync_l10_interactive.sh first")
    page = SRC.read_text()
    scripts = re.findall(r"<script>(.*?)</script>", page, re.S)
    main_js = max(scripts, key=len)
    # the slides' data: every top-level var before the main function (DATA, and BIB for the references on hover)
    data = re.search(r"(var DATA = .*?;)\s*(?:/\*.*?\*/\s*)*\(function\(\)\{", main_js, re.S)
    if not data:
        die("DATA not found")
    names = re.findall(r"^var (\w+) = ", data.group(1), re.M)
    STATIC.mkdir(parents=True, exist_ok=True)
    WDIR.mkdir(parents=True, exist_ok=True)
    (STATIC / "l10w-data.js").write_text("/* Generated by tools/build_l10_widgets.py: the L10 interactive slides' data. */\n"
                                         "window.L10W_VARS = (function(){\n" + data.group(1) + "\nreturn {"
                                         + ", ".join(f"{n}:{n}" for n in names) + "};\n})();\n")
    style = "\n".join(re.findall(r"<style>(.*?)</style>", page, re.S))
    css = scope_css(style)
    css = re.sub(r'"?Fira (Sans|Mono)"?(?=\s*[,;}])', lambda m: f'"L10W Fira {m.group(1)}", "Fira {m.group(1)}"', css)
    # light theme only: two of the slides' text colors pass 4.5:1 as the slides' large text, not at the docs' body size
    tail = ("\n/* docs body size: the light theme's orange and green text a little darker, to reach 4.5:1 on the panel */\n"
            ".l10w{--follow:#A3561F;--ok:#2A7348}\n"
            "/* the panel title carries the Try it badge, so the slide's own badge is not repeated */\n"
            ".l10w .l10w-in .try{display:none}\n"
            "/* the slider's value sits centered on the thumb at any column width (the slides' top is 3 px of 40) */\n"
            ".l10w .rng .rv{top:calc(3 * var(--u))}\n")
    (STATIC / "l10w.css").write_text(FONT_FACES + DOCS_CSS.replace('font-family:"Fira Sans"', 'font-family:"L10W Fira Sans","Fira Sans"') + css + tail)
    js_main = main_js[main_js.find("(function(){", data.end(1)):]
    (STATIC / "l10w-core.js").write_text(build_js(js_main, page, names))

    icons = re.search(r'<svg id="icons".*?</svg>', page, re.S).group(0)
    (WDIR / "_head.html").write_text(
        "<!-- Generated by tools/build_l10_widgets.py: the widgets' styles, math styles and car icons, loaded once. -->\n"
        '<link rel="stylesheet" href="interactive/katex/katex.min.css">\n'
        '<link rel="stylesheet" href="../../_static/l10w/l10w.css">\n' + icons + "\n")
    (WDIR / "_scripts.html").write_text(
        "<!-- Generated by tools/build_l10_widgets.py: math, data and widget code, after every panel. -->\n"
        '<script src="interactive/katex/katex.min.js"></script>\n'
        '<script src="interactive/katex/contrib/auto-render.min.js"></script>\n'
        '<script src="../../_static/l10w/l10w-data.js"></script>\n'
        '<script src="../../_static/l10w/l10w-core.js"></script>\n')
    # slide wording that reads wrong on a docs page: (panel, slide text, docs text); each must be found
    WORDING = [("cap", "the dashed line on the next frame", "the dashed line in the next panel"),
               ("turn-rate", "the turn per meter from the curvature frame", "the turn per meter"),
               ("turn-rate", "drives a circle (next frame)", "drives a circle (next panel)"),
               ("control-step", "Added for LQR or MPC (in the docs)", "Added for LQR or MPC")]
    used = set()
    for name, keys, label, _ in WIDGETS:
        secs = []
        for k in keys:                                 # two keys can find the same slide: take it once
            sec = find_section(page, k)
            if sec not in secs:
                secs.append(sec)
        parts = [section_parts(sec) for sec in secs]
        title = parts[0][0]
        body = "\n".join(p[1] for p in parts)
        cls = " ".join(sorted({c for p in parts for c in p[2]}))
        html_ = (f'<!-- Generated by tools/build_l10_widgets.py from the interactive slide "{re.sub("<[^>]+>", "", title)}". -->\n'
                 f'<div class="l10w mathjax_ignore tex2jax_ignore" data-w="{name}">\n'
                 f'<div class="l10w-title"><span class="l10w-kick">Try it</span>{title}</div>\n'
                 f'<div class="l10w-in{(" " + cls) if cls else ""}">\n{fix_markup(body)}\n</div>\n</div>\n')
        html_ = deck_words(html_)
        for w_name, old, new in WORDING:
            if w_name == name and old in html_:
                html_ = html_.replace(old, new); used.add(old)
        (WDIR / f"{name}.html").write_text(html_)
    write_refs(page)
    missing = [w[1] for w in WORDING if w[1] not in used]
    if missing:
        die("slide wording not found (the slides changed?): " + "; ".join(missing))
    print(f"wrote {len(WIDGETS)} panels, l10w.css, l10w-core.js, l10w-data.js")


if __name__ == "__main__":
    main()
