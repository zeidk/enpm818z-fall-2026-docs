"""Figures for the reading preread/nonlinear-filters.rst (instructor only).

    /usr/bin/python3 tools/make_filters_figures.py

road_30_top.png: the scene of "A straight line keeps a bell curve a bell curve", seen from
above. The AV drives d = 20 +- 1 m along a road at 30 degrees from east; x = d cos 30 is how
far east it gets. Colors follow the graph after it (bell_1_line.png): the distance driven in
gray, the distance east in blue. Writes docs/source/_static/images/filters/, 300 dpi, white.
"""
import math
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                    # noqa: E402
from matplotlib import font_manager                                # noqa: E402
from matplotlib.patches import Arc, Circle, Polygon                # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
SLIDES = ROOT.parents[1] / "latex/enpm818z-fall-2026-latex/slides"
sys.path.insert(0, str(SLIDES / "lectures/lecture3/figures/svg"))
from avdraw import draw_av                                          # noqa: E402
from PIL import Image                                               # noqa: E402

for f in ("FiraSans-Regular.otf", "FiraSans-Bold.otf"):
    font_manager.fontManager.addfont(str(SLIDES / "font/firasans" / f))
plt.rcParams.update({"font.family": "Fira Sans", "font.size": 11})

INK, GRAY, BLUE, ROAD = "#222222", "#747474", "#2a78d6", "#e6e6e6"
OUT = ROOT / "docs/source/_static/images/filters"
OUT.mkdir(parents=True, exist_ok=True)



def save(fig, path):
    """Save at 300 dpi as RGB: an alpha channel fails tools/check_figures.py."""
    fig.savefig(path, dpi=300, facecolor="white")
    Image.open(path).convert("RGB").save(path, dpi=(300, 300))

def tag(ax, x, y, n):
    """A numbered tag: a dark circle with a white bold number."""
    ax.add_patch(Circle((x, y), 0.55, color=INK, zorder=20))
    ax.text(x, y, str(n), color="white", ha="center", va="center", fontsize=10,
            fontweight="bold", zorder=21)


def road_30_top():
    th = math.radians(30.0)
    u = (math.cos(th), math.sin(th))            # along the road
    n = (-math.sin(th), math.cos(th))           # across it, to the left
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    # The road: 4 m wide, centered on the AV's path, from 2 m behind the start to 24 m.
    a, b, w = -2.0, 24.0, 2.0
    corners = [(a * u[0] + s * w * n[0], a * u[1] + s * w * n[1]) for s in (-1, 1)]
    corners += [(b * u[0] + s * w * n[0], b * u[1] + s * w * n[1]) for s in (1, -1)]
    ax.add_patch(Polygon(corners, closed=True, color=ROAD, zorder=1))
    # The AV at the start, base link on (0, 0), heading 30 degrees.
    draw_av(ax, 0.0, 0.0, 30.0)
    # Where it ends: d from 19 to 21 m along the road (gray), d = 20 marked, with a faint
    # copy of the AV there.
    e = {d: (d * u[0], d * u[1]) for d in (19.0, 20.0, 21.0)}
    draw_av(ax, e[20][0], e[20][1], 30.0, tint=GRAY, alpha=0.35)
    ax.plot([e[19][0], e[21][0]], [e[19][1], e[21][1]], color=GRAY, lw=6, solid_capstyle="butt", zorder=6)
    ax.plot(*e[20], "o", color=INK, ms=5, zorder=7)
    # Straight down to the plot's east axis: x from 19 cos 30 to 21 cos 30 (blue).
    y0 = -2.0
    for d in (19.0, 21.0):
        ax.plot([e[d][0], e[d][0]], [e[d][1], y0], color=BLUE, lw=0.9, ls=(0, (3, 3)), zorder=4)
    ax.plot([e[20][0], e[20][0]], [e[20][1], y0], color=INK, lw=0.9, ls=(0, (1, 2)), zorder=4)
    ax.plot([e[19][0], e[21][0]], [y0, y0], color=BLUE, lw=6, solid_capstyle="butt", zorder=6,
            clip_on=False)
    ax.plot([0, 0], [0, y0], color=INK, lw=0.9, ls=(0, (1, 2)), zorder=4)
    # The 30 degree angle between east and the road, at the start.
    ax.plot([0, 6.0], [0, 0], color=INK, lw=0.9, zorder=4)
    ax.add_patch(Arc((0, 0), 9.0, 9.0, theta1=0, theta2=30, color=INK, lw=1.0, zorder=4))
    ax.text(4.9, 1.15, "30°", fontsize=11, zorder=8)
    # Tags, each beside its own mark.
    tag(ax, -1.6, 2.6, 1)                       # the AV at the start
    tag(ax, e[19][0] - 1.6, e[19][1] + 1.6, 2)  # where it ends, d = 19 to 21 m
    tag(ax, e[21][0] + 1.2, y0 + 1.0, 3)        # how far east, x
    ax.set_xlim(-3.5, 24.5)
    ax.set_ylim(y0, 13.5)
    ax.set_aspect("equal")
    ax.set_xlabel("east (m)")
    ax.set_ylabel("north (m)")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    path = OUT / "road_30_top.png"
    save(fig, path)
    print(path, "x =", ", ".join(f"{d * u[0]:.2f}" for d in (19, 20, 21)))


def h(x):
    """The range from the AV at x to the landmark 10 m off the road beside x = 20."""
    return math.sqrt((20.0 - x) ** 2 + 10.0 ** 2)


def slope(x):
    return -(20.0 - x) / h(x)


def label(ax, xy, text, xytext, color=INK, ha="left"):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=10.5, color=color, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=color, lw=0.8, shrinkA=2, shrinkB=3), zorder=30)


def range_axes(ax, x0, x1, y0, y1):
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_xlabel("AV's position along the road, $x$ (m)")
    ax.set_ylabel("range to the landmark (m)")
    ax.grid(color="#e6e6e6", lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


GREEN, ORANGE, PURPLE = "#1baf7a", "#eb6834", "#7b3fa0"
READ = 10.77                                   # what the camera reads: the AV is really at 16 m


def run1():
    """Run 1, a good estimate at 15.5 m: the surprise, the slope, the move."""
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    xs = [14.0 + i * 0.01 for i in range(321)]
    ax.plot(xs, [h(x) for x in xs], color=INK, lw=2.6, zorder=3)
    e, he, k = 15.5, h(15.5), slope(15.5)
    ax.plot(xs, [he + k * (x - e) for x in xs], color=PURPLE, lw=1.6, ls=(0, (6, 4)), zorder=4)
    ax.axhline(READ, color="#888888", lw=1.2, ls=(0, (2, 3)), zorder=2)
    # The slope triangle, to the left of the estimate: 1 m along x, 0.41 m of range.
    ax.plot([e - 1.0, e, e], [he - k, he - k, he], color=PURPLE, lw=1.2, zorder=4)
    ax.text(e - 0.5, he - k + 0.03, "1 m", color=PURPLE, ha="center", fontsize=10.5)
    ax.text(e + 0.04, he - k / 2, "0.41 m", color=PURPLE, va="center", fontsize=10.5)
    # The surprise: from what the filter expects down to what the camera reads.
    ax.annotate("", xy=(e, READ), xytext=(e, he), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4), zorder=6)
    # The move, along the reading line, and the new estimate.
    new = e + (READ - he) / k
    ax.annotate("", xy=(new, READ - 0.05), xytext=(e, READ - 0.05),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6), zorder=6)
    ax.plot(e, he, "o", color=GREEN, ms=9, mec="white", zorder=8)
    ax.plot(new, READ, "X", color=GREEN, ms=10, mec="white", zorder=9)
    ax.plot(16.0, h(16.0), "o", color=INK, ms=6, zorder=8)
    label(ax, (e, he), "the estimate, 15.5 m:\nthe filter expects 10.97 m", (14.1, 11.1))
    label(ax, (e, (he + READ) / 2), "surprise: 0.20 m less range", (14.1, 10.87))
    ax.text(17.15, READ + 0.02, "the camera reads 10.77 m", color="#555555", ha="right", va="bottom", fontsize=10.5)
    label(ax, ((e + new) / 2, READ - 0.05), "move: 0.20 / 0.41 = 0.48 m", (14.1, 10.55), color=GREEN)
    label(ax, (new, READ), "new estimate, 15.98 m", (15.2, 10.4), color=GREEN)
    label(ax, (16.0, h(16.0)), "the AV really is at 16 m", (16.3, 11.02))
    ax.text(16.75, h(16.75) + 0.05, "the real range, $h(x)$", fontsize=10.5, ha="left", va="bottom", rotation=-14)
    label(ax, (16.75, he + k * 1.25), "the tangent at 15.5 m", (15.95, 10.36), color=PURPLE)
    range_axes(ax, 14.0, 17.2, 10.3, 11.45)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "ekf_run1.png")
    print("run1: slope", round(k, 3), "new", round(new, 3))


def run2():
    """Run 2, a poor estimate at 10 m: the tangent is steeper than the real drop."""
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    xs = [4.0 + i * 0.02 for i in range(801)]
    ax.plot(xs, [h(x) for x in xs], color=INK, lw=2.6, zorder=3)
    e, he, k = 10.0, h(10.0), slope(10.0)
    tx = [6.0 + i * 0.02 for i in range(451)]
    ax.plot(tx, [he + k * (x - e) for x in tx], color=PURPLE, lw=1.6, ls=(0, (6, 4)), zorder=4)
    ax.axhline(READ, color="#888888", lw=1.2, ls=(0, (2, 3)), zorder=2)
    # The real drop from 10 m to 16 m, as a straight line: 0.56 m per meter.
    ax.plot([e, 16.0], [he, h(16.0)], color=ORANGE, lw=1.2, ls=(0, (1, 2)), zorder=4)
    ax.annotate("", xy=(e, READ), xytext=(e, he), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4), zorder=6)
    new = e + (READ - he) / k
    ax.plot(e, he, "o", color=ORANGE, ms=9, mec="white", zorder=8)
    ax.plot(new, READ, "X", color=ORANGE, ms=10, mec="white", zorder=9)
    ax.plot(16.0, h(16.0), "o", color=INK, ms=6, zorder=8)
    # The miss, under the reading line.
    ax.annotate("", xy=(16.0, READ - 0.45), xytext=(new, READ - 0.45),
                arrowprops=dict(arrowstyle="<|-|>", color=ORANGE, lw=1.2), zorder=6)
    ax.text((new + 16.0) / 2, READ - 0.6, "1.23 m short", color=ORANGE, ha="center", va="top", fontsize=10.5)
    label(ax, (e, he), "the estimate, 10 m:\nthe filter expects 14.14 m", (11.2, 16.6))
    label(ax, (e, 12.4), "surprise: 3.37 m less range", (4.4, 12.4), ha="left")
    ax.text(4.3, READ + 0.15, "the camera reads 10.77 m", color="#555555", ha="left", va="bottom", fontsize=10.5)
    label(ax, (12.5, he + k * 2.5), "the tangent at 10 m:\n0.71 m less range per meter", (12.9, 14.8), color=PURPLE)
    label(ax, (13.0, (he + h(16.0)) / 2 + 0.0), "the real drop from 10 m to 16 m:\n0.56 m per meter", (14.2, 13.3), color=ORANGE)
    label(ax, (new, READ), "new estimate, 14.77 m", (11.0, 9.75), color=ORANGE)
    label(ax, (16.0, h(16.0)), "the AV really\nis at 16 m", (17.2, 12.0))
    ax.text(6.3, h(6.3) + 0.35, "the real range, $h(x)$", fontsize=10.5, rotation=-27)
    range_axes(ax, 4.0, 20.0, 9.3, 19.2)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "ekf_run2.png")
    print("run2: slope", round(k, 3), "chord", round((h(16.0) - he) / 6.0, 3), "new", round(new, 3))


if __name__ == "__main__":
    road_30_top()
    run1()
    run2()
