"""Build the L8 hands-on as one page that runs in the browser (Pyodide: Python in WebAssembly).

    /usr/bin/python3 tools/make_l8_handson_html.py [--l8 PATH] [--out PATH]

Reads l8sim.py, l8_handson.py and l8_scene.npz from the carla-python repo's lecture8 folder
and writes docs/source/_static/handson/l8_handson.html. The page has one tab per hands-on part
(scene, physics, modes, interact), each with the now slider of l8_handson.py, and a tab with
l8sim.py that students can edit and rerun. Rebuild the page after any change to those files.
"""
import argparse
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
L8_DEFAULT = ROOT.parents[1] / "workspace" / "enpm818z-fall-2026-carla-python" / "lecture8"
OUT_DEFAULT = ROOT / "docs" / "source" / "_static" / "handson" / "l8_handson.html"
PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/"

# Each part: the slider's range (as in l8_handson.py) and the deck's hands-on questions.
PARTS = [
    ("scene", "Part 1: the scene", -2.0, [
        "Drag the <b>now</b> slider from &minus;2 to 3 s. The dots are the tracked positions the AV sees.",
        "At which time can you first tell, by eye, that car A is slowing down? That it turns?"]),
    ("physics", "Part 2: physics models", -0.5, [
        "At now = 0: read each model's error at 5 s in the right panel's title (FDE). Which is smallest, and why?",
        "Move now from 0 to 3.0 s, 0.5 s at a time. When does CTRV beat CV at 5 s? When does it lose?",
        "Where is CTRA worst: while A brakes, or while it speeds up after the turn?"]),
    ("modes", "Part 3: two futures", -0.5, [
        "Move the <b>now</b> slider from &minus;0.5 to 1.0 s. Watch the line widths (the probabilities) and P(left) on the right.",
        "In the <b>l8sim.py</b> tab, set <code>SIG_V = 0.5</code>, then <code>2.0</code>. What happens to P(left) at t = 0, and why?",
        "Set <code>A_LAT = 1.5</code>. Does the left mode's FDE go down? Why?"]),
    ("interact", "Part 4: drivers who react", -0.5, [
        "Run 1: compare B's speed from CV and from the IDM. At what time do the two speed curves start to differ?",
        "Tick <b>AV 24 m closer</b> (run 2). Read A's gap in the title. Which of the two \"most likely mode\" lines matches the truth?",
        "In the <b>l8sim.py</b> tab, set <code>GAP = 2.5</code>. What does A do in run 2 now? And car B, behind it?"]),
]

GLUE = r'''
import sys, io, base64, importlib
sys.path.insert(0, "/home/pyodide")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import l8sim
import l8_handson as H
_cache = {}

def _setup():
    if "o" not in _cache:
        sc = l8sim.load_scene()
        _cache.update(sc=sc, o=l8sim.our_scene(sc), o2=l8sim.our_scene(sc, av_closer=24.0))

def render(part, now, closer=False):
    _setup()
    if part not in _cache:
        fig = plt.figure(figsize=(13, 6.5))
        extra = {"o2": _cache["o2"]} if part == "interact" else {}
        upd = H.PARTS[part](fig, _cache["sc"], _cache["o"], now, **extra)
        fig.subplots_adjust(bottom=0.1, top=0.86, wspace=0.25)
        _cache[part] = (fig, upd)
    fig, upd = _cache[part]
    fig._l8_now = lambda: now
    if part == "interact":
        check = fig._l8_check
        check.ax.set_visible(False)          # the page's own checkbox replaces it
        if check.get_status()[0] != bool(closer):
            check.set_active(0)              # runs the script's toggle, which redraws
        for artist in check.ax.get_children():
            artist.set_visible(False)        # its tick mark too
    upd(now)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=80)
    return base64.b64encode(buf.getvalue()).decode()

def reload_sim(src):
    with open("/home/pyodide/l8sim.py", "w") as f:
        f.write(src)
    importlib.reload(l8sim)
    importlib.reload(H)
    for k in list(_cache):
        if k in H.PARTS:
            plt.close(_cache[k][0])
        del _cache[k]
'''

PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>L8 hands-on in the browser</title>
<style>
  :root { --bg: #ffffff; --fg: #1e2939; --muted: #5b6573; --line: #d5d9de; --accent: #2d6ca2; --panel: #f4f6f8; }
  @media (prefers-color-scheme: dark) {
    :root { --bg: #16191d; --fg: #e6e9ed; --muted: #a3acb8; --line: #333a42; --accent: #6aa8de; --panel: #1f2328; }
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.5 system-ui, sans-serif; }
  main { max-width: 1100px; margin: 0 auto; padding: 16px; }
  h1 { font-size: 1.4rem; margin: 0.2rem 0 0.4rem; }
  p.lead { color: var(--muted); margin: 0 0 1rem; }
  #status { padding: 8px 12px; background: var(--panel); border: 1px solid var(--line); border-radius: 6px; margin-bottom: 12px; }
  .tabs { display: flex; flex-wrap: wrap; gap: 4px; border-bottom: 1px solid var(--line); }
  .tabs button { font: inherit; background: none; color: var(--muted); border: 1px solid transparent;
                 border-bottom: none; padding: 8px 12px; cursor: pointer; border-radius: 6px 6px 0 0; }
  .tabs button[aria-selected="true"] { color: var(--fg); border-color: var(--line); background: var(--bg);
                 margin-bottom: -1px; font-weight: 600; }
  .panel { padding: 14px 0; }
  .panel[hidden] { display: none; }
  .controls { display: flex; flex-wrap: wrap; align-items: center; gap: 16px; margin: 8px 0; }
  .controls input[type=range] { width: min(420px, 70vw); }
  .plot { width: 100%; border: 1px solid var(--line); border-radius: 6px; background: #fff; min-height: 120px; }
  ol { margin: 0.4rem 0 0.6rem 1.2rem; padding: 0; }
  textarea { width: 100%; height: 60vh; font: 13px/1.4 ui-monospace, monospace; color: var(--fg);
             background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 8px; }
  button.act { font: inherit; padding: 6px 14px; border-radius: 6px; border: 1px solid var(--accent);
               background: var(--accent); color: #fff; cursor: pointer; }
  button.act.secondary { background: none; color: var(--accent); }
  pre.err { white-space: pre-wrap; color: #c0392b; }
  code { font-family: ui-monospace, monospace; }
</style>
</head>
<body>
<main>
<h1>L8 hands-on: where will the others be?</h1>
<p class="lead">The same Python as <code>l8_handson.py</code> and <code>l8sim.py</code>, running in your browser
(numpy and matplotlib, no CARLA, no ROS). The first load downloads Python, so it takes a while.</p>
<div id="status" role="status">Loading Python in the browser...</div>
<div class="tabs" role="tablist" id="tabs"></div>
<div id="panels"></div>
</main>
<script src="__PYODIDE__pyodide.js"></script>
<script>
const PARTS = __PARTS__;
const SRC = __SRC__;
const NPZ_B64 = "__NPZ__";
const GLUE = __GLUE__;
let py = null, busy = false, pending = null;
const status = document.getElementById("status");

function el(tag, attrs = {}, html = "") {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (html) e.innerHTML = html;
  return e;
}

function buildTabs() {
  const tabs = document.getElementById("tabs"), panels = document.getElementById("panels");
  const all = PARTS.map(p => ({id: p[0], label: p[1]})).concat([{id: "code", label: "l8sim.py"}]);
  all.forEach((t, i) => {
    const b = el("button", {role: "tab", id: "tab-" + t.id, "aria-controls": "panel-" + t.id,
                            "aria-selected": i === 0 ? "true" : "false"}, t.label);
    b.onclick = () => select(t.id);
    tabs.appendChild(b);
  });
  for (const [id, label, lo, qs] of PARTS) {
    const p = el("section", {class: "panel", id: "panel-" + id, role: "tabpanel", "aria-labelledby": "tab-" + id});
    p.appendChild(el("ol", {}, qs.map(q => "<li>" + q + "</li>").join("")));
    const c = el("div", {class: "controls"});
    const lab = el("label", {}, "now: <output id='v-" + id + "'>0.0</output> s ");
    const r = el("input", {type: "range", id: "now-" + id, min: lo, max: 3, step: 0.1, value: 0});
    lab.appendChild(r); c.appendChild(lab);
    if (id === "interact") {
      const cl = el("label", {}, " AV 24 m closer (run 2)");
      const cb = el("input", {type: "checkbox", id: "closer"});
      cl.prepend(cb); c.appendChild(cl);
      cb.onchange = () => draw(id);
    }
    r.oninput = () => { document.getElementById("v-" + id).textContent = Number(r.value).toFixed(1); draw(id); };
    p.appendChild(c);
    p.appendChild(el("img", {class: "plot", id: "img-" + id, alt: label + ": the plot for the chosen now"}));
    p.appendChild(el("pre", {class: "err", id: "err-" + id}));
    p.hidden = id !== PARTS[0][0];
    panels.appendChild(p);
  }
  const p = el("section", {class: "panel", id: "panel-code", role: "tabpanel", "aria-labelledby": "tab-code"});
  p.hidden = true;
  p.appendChild(el("p", {}, "Edit <code>l8sim.py</code> (for example <code>SIG_V</code>, <code>A_LAT</code> or " +
                            "<code>GAP</code>), then press <b>Apply</b>: every tab reruns with your version."));
  const ta = el("textarea", {id: "src", spellcheck: "false", "aria-label": "l8sim.py source"});
  ta.value = SRC.l8sim;
  p.appendChild(ta);
  const c = el("div", {class: "controls"});
  const apply = el("button", {class: "act"}, "Apply");
  const reset = el("button", {class: "act secondary"}, "Reset to the original");
  apply.onclick = () => applySrc(ta.value);
  reset.onclick = () => { ta.value = SRC.l8sim; applySrc(ta.value); };
  c.appendChild(apply); c.appendChild(reset);
  p.appendChild(c);
  p.appendChild(el("pre", {class: "err", id: "err-code"}));
  panels.appendChild(p);
}

function select(id) {
  document.querySelectorAll(".tabs button").forEach(b => b.setAttribute("aria-selected", b.id === "tab-" + id));
  document.querySelectorAll(".panel").forEach(p => p.hidden = p.id !== "panel-" + id);
  if (id !== "code" && !document.getElementById("img-" + id).src) draw(id);
}

async function draw(id) {
  if (!py) return;
  if (busy) { pending = id; return; }
  busy = true;
  const now = Number(document.getElementById("now-" + id).value);
  const closer = id === "interact" && document.getElementById("closer").checked;
  const err = document.getElementById("err-" + id);
  try {
    const b64 = py.globals.get("render")(id, now, closer);
    document.getElementById("img-" + id).src = "data:image/png;base64," + b64;
    err.textContent = "";
  } catch (e) { err.textContent = String(e); }
  busy = false;
  if (pending) { const p = pending; pending = null; draw(p); }
}

async function applySrc(src) {
  const err = document.getElementById("err-code");
  status.textContent = "Running your l8sim.py...";
  try {
    py.globals.get("reload_sim")(src);
    err.textContent = "";
    for (const [id] of PARTS) document.getElementById("img-" + id).removeAttribute("src");
    status.textContent = "Your l8sim.py is in use. Open a part's tab to see it.";
  } catch (e) { err.textContent = String(e); status.textContent = "l8sim.py has an error (see below)."; }
}

async function main() {
  buildTabs();
  try {
    py = await loadPyodide();
    status.textContent = "Loading numpy and matplotlib...";
    await py.loadPackage(["numpy", "matplotlib"]);
    py.FS.writeFile("/home/pyodide/l8sim.py", SRC.l8sim);
    py.FS.writeFile("/home/pyodide/l8_handson.py", SRC.handson);
    py.FS.writeFile("/home/pyodide/l8_scene.npz", Uint8Array.from(atob(NPZ_B64), c => c.charCodeAt(0)));
    status.textContent = "Simulating the scene...";
    await py.runPythonAsync(GLUE);
    status.textContent = "Ready. Drag a slider; each part redraws for that moment.";
    draw(PARTS[0][0]);
  } catch (e) {
    status.textContent = "Python could not start: " + e;
  }
}
main();
</script>
</body>
</html>
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--l8", type=Path, default=L8_DEFAULT, help="the carla-python lecture8 folder")
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    a = ap.parse_args()
    src = {"l8sim": (a.l8 / "l8sim.py").read_text(), "handson": (a.l8 / "l8_handson.py").read_text()}
    npz = base64.b64encode((a.l8 / "l8_scene.npz").read_bytes()).decode()
    page = (PAGE.replace("__PYODIDE__", PYODIDE)
                .replace("__PARTS__", json.dumps(PARTS))
                .replace("__SRC__", json.dumps(src))
                .replace("__GLUE__", json.dumps(GLUE))
                .replace("__NPZ__", npz))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(page)
    print(f"wrote {a.out} ({a.out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
