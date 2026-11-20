"""Light and dark versions of figures that a script writes straight to PNG (the filters reading).

    /usr/bin/python3 tools/run_svg.py OUTDIR tools/make_filters_figures.py
    /usr/bin/python3 tools/run_svg.py OUTDIR tools/filters_figs/bell_ekf.py

Runs a matplotlib figure script with every savefig sent to OUTDIR/png/<name> instead of its real
path, plus OUTDIR/svg/<stem>.svg, so nothing published changes. Compare OUTDIR/png with the
published PNGs (same pixels: the SVG is the published figure), then make the pair with the slides
repo's slides/figures/make_themed.py OUTDIR <names> and copy OUTDIR/themed/<name>.png and
<name>_dark.png into _static/images/<folder>/. The filters scripts read Fira Sans from
slides/font/firasans in the slides repo: link that folder to latex-common/font for the run."""
import os, runpy, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure
out = Path(sys.argv[1]).resolve(); (out / "png").mkdir(parents=True, exist_ok=True); (out / "svg").mkdir(exist_ok=True)
orig = Figure.savefig
def savefig(self, fname, *a, **k):
    p = Path(str(fname))
    orig(self, out / "png" / p.name, *a, **k)
    k2 = {kk: v for kk, v in k.items() if kk not in ("dpi", "format", "pil_kwargs", "metadata")}
    orig(self, out / "svg" / (p.stem + ".svg"), *a, format="svg", **k2)
Figure.savefig = savefig
import matplotlib.pyplot as plt
plt.savefig = lambda fname, *a, **k: savefig(plt.gcf(), fname, *a, **k)
script = sys.argv[2]; sys.argv = [script] + sys.argv[3:]; sys.path.insert(0, str(Path(script).resolve().parent))
os.chdir(Path(script).resolve().parent.parent if "filters_figs" in script else Path.cwd())
runpy.run_path(script, run_name="__main__")
