"""range_curve.png: the range from four positions, from above and as a graph
(preread/nonlinear-filters.rst, "The range curve has no single slope").

    /usr/bin/python3 tools/filters_figs/range_curve.py

Left, the road from above, to scale: the landmark 10 m off the AV's path beside x = 20, and the
line of sight from x = 4, 10, 16 and 19 m, each with its range h(x) and, at 4 and 19 m, its angle
off the road. A faint AV marks where the AV really is, 16 m. Right, a graph (not the road): the
range h(x) = sqrt((20 - x)^2 + 10^2) against x, with the same four positions. Style and helpers
come from tools/make_filters_figures.py; the car is the L3 deck's draw_av (imported there).
"""
import math
import pathlib
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import make_filters_figures as mf                                   # noqa: E402
import matplotlib.pyplot as plt                                     # noqa: E402
from matplotlib.patches import Arc, Rectangle                       # noqa: E402

INK, GRAY, ROAD = mf.INK, mf.GRAY, mf.ROAD
h, label = mf.h, mf.label
LX, LY, HALF = 20.0, 10.0, 1.9
POS = (4.0, 10.0, 16.0, 19.0)


def angle(px):
    """The line of sight's angle off the road, in degrees."""
    return math.degrees(math.atan2(LY, LX - px))


def road(ax):
    ax.add_patch(Rectangle((2.0, -HALF), 20.0, 2 * HALF, color=ROAD, lw=0, zorder=1))
    mf.draw_av(ax, 16.0, 0.0, 0.0, tint=GRAY, alpha=0.35, z=2)
    ax.add_patch(Rectangle((LX - 0.45, LY - 0.45), 0.9, 0.9, color=INK, lw=0, zorder=7))
    ax.text(LX - 0.8, LY + 0.2, "the landmark", fontsize=10.5, ha="right", va="center", zorder=8)
    for px in POS:
        ax.plot([px, LX], [0, LY], color=INK, lw=1.4, zorder=4)
        ax.plot(px, 0, "o", color=INK, mec="white", mew=1.2, ms=7, zorder=6)
    # Range labels: on the lines from 4 and 10 m, beside the close lines from 16 and 19 m.
    for px, t in ((4.0, 0.45), (10.0, 0.5)):
        u = ((LX - px) / h(px), LY / h(px))
        ax.text(px + t * h(px) * u[0], t * h(px) * u[1], f"{h(px):.2f} m", fontsize=10.5,
                ha="center", va="center", rotation=angle(px), rotation_mode="anchor", zorder=8,
                bbox=dict(fc="white", ec="none", pad=1.0))
    u = ((LX - 16.0) / h(16.0), LY / h(16.0))
    ax.text(16.0 + 0.5 * h(16.0) * u[0] - 0.75 * u[1], 0.5 * h(16.0) * u[1] + 0.75 * u[0],
            f"{h(16.0):.2f} m", fontsize=10.5, ha="center", va="center", rotation=angle(16.0),
            rotation_mode="anchor", zorder=8)
    label(ax, (19.0 + 0.45, 4.5), f"{h(19.0):.2f} m", (20.6, 4.5))
    # The angle off the road at 4 m and at 19 m.
    for px, r, tx, ty in ((4.0, 3.2, 7.4, 0.9), (19.0, 1.5, 20.7, 0.9)):
        ax.add_patch(Arc((px, 0), 2 * r, 2 * r, theta1=0, theta2=angle(px), color=INK, lw=1.0, zorder=5))
        ax.text(tx, ty, f"{angle(px):.0f}°", fontsize=10.5, va="center", zorder=8)
    ax.text(2.3, -1.3, "the road", color="#555555", fontsize=10.5, va="center", zorder=8)
    label(ax, (15.6, -1.0), "the faint AV: where the AV really is", (5.0, -3.1), color="#555555")
    ax.set_xlim(2.0, 22.0)
    ax.set_ylim(-3.8, 11.4)
    ax.set_aspect("equal")
    ax.set_xticks(POS)
    ax.set_yticks([0, 5, 10])
    ax.set_xlabel("position along the road, $x$ (m)")
    ax.set_ylabel("across the road (m)")
    ax.set_title("The road from above", fontsize=12, fontweight="bold", loc="left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def graph(ax):
    xs = [3.0 + i * 0.02 for i in range(851)]
    ax.plot(xs, [h(x) for x in xs], color=INK, lw=2.6, zorder=3)
    for px in POS:
        ax.plot([px, px], [8.5, h(px)], color=GRAY, lw=0.9, ls=(0, (1, 2)), zorder=2)
        ax.plot(px, h(px), "o", color=INK, mec="white", mew=1.2, ms=8, zorder=6)
    label(ax, (4.0, h(4.0)), f"from 4 m: {h(4.0):.2f} m", (5.6, 19.4))
    label(ax, (10.0, h(10.0)), f"from 10 m: {h(10.0):.2f} m", (11.2, 15.6))
    label(ax, (16.0, h(16.0)), f"from 16 m:\n{h(16.0):.2f} m", (12.4, 9.7))
    label(ax, (19.0, h(19.0)), f"from 19 m: {h(19.0):.2f} m", (16.4, 12.6))
    label(ax, (7.0, h(7.0)), "the range, $h(x)$", (4.6, 13.2))
    mf.range_axes(ax, 3.0, 21.0, 8.5, 20.5)
    ax.set_xticks(POS)
    ax.set_title("A graph, not the road: range against position", fontsize=12, fontweight="bold",
                 loc="left")


def main():
    fig, axs = plt.subplots(1, 2, figsize=(11.0, 4.6), gridspec_kw={"width_ratios": [1.0, 1.0]})
    road(axs[0])
    graph(axs[1])
    fig.patch.set_facecolor("white")
    fig.tight_layout(w_pad=2.5)
    path = mf.OUT / "range_curve.png"
    mf.save(fig, path)
    print(path)
    for px in POS:
        print(f"  x = {px:4.1f} m: range {h(px):.2f} m, {angle(px):.1f} deg off the road, "
              f"slope {mf.slope(px):.3f}")


if __name__ == "__main__":
    main()
