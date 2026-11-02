"""range_road_top.png: the range example seen from above (preread/nonlinear-filters.rst).

    /usr/bin/python3 tools/filters_figs/range_road_top.py

To scale, in meters. The AV drives east (to the right) in a one-lane road; its position along
the road is x, measured at its base link (the middle of the rear axle). A landmark stands 10 m
off the AV's path, beside x = 20. The AV is really at x = 16, so the range is
h(16) = sqrt(4^2 + 10^2). The two runs' estimates, 15.5 m and 10 m, are marked in the colors of
ekf_run1.png (green) and ekf_run2.png (orange). Style and helpers come from
tools/make_filters_figures.py; the car is the L3 deck's draw_av (imported there).
"""
import pathlib
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import make_filters_figures as mf                                   # noqa: E402
import matplotlib.pyplot as plt                                     # noqa: E402
from matplotlib.patches import Rectangle                            # noqa: E402

INK, GRAY, GREEN, ORANGE, ROAD = mf.INK, mf.GRAY, mf.GREEN, mf.ORANGE, mf.ROAD
h, label = mf.h, mf.label
X_TRUE, LX, LY = 16.0, 20.0, 10.0          # the AV, and the landmark beside x = 20, 10 m off
HALF = 1.9                                 # half the lane width (m)


def dim(ax, x0, x1, y, text, color=INK):
    """A two-headed dimension arrow from x0 to x1 at height y, its text under the middle."""
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<|-|>", color=color, lw=1.1, shrinkA=0, shrinkB=0), zorder=6)
    ax.text((x0 + x1) / 2, y - 0.35, text, color=color, ha="center", va="top", fontsize=10.5)


def main():
    fig, ax = plt.subplots(figsize=(8.0, 5.2))
    ax.add_patch(Rectangle((-1.0, -HALF), 24.0, 2 * HALF, color=ROAD, lw=0, zorder=1))
    ax.text(-0.6, HALF - 0.45, "the road", color="#555555", fontsize=10.5, va="top", zorder=8)
    ax.annotate("", xy=(6.5, -0.9), xytext=(2.5, -0.9),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2), zorder=6)
    ax.text(6.8, -0.9, "the AV drives this way", fontsize=10.5, va="center", zorder=8)
    # The AV, really at 16 m: its base link (the middle of the rear axle) is the white dot.
    mf.draw_av(ax, X_TRUE, 0.0, 0.0)
    # The landmark, 10 m off the AV's path, beside x = 20.
    ax.add_patch(Rectangle((LX - 0.45, LY - 0.45), 0.9, 0.9, color=INK, lw=0, zorder=7))
    ax.text(LX + 0.8, LY, "the landmark", fontsize=10.5, va="center", zorder=8)
    ax.plot([LX, LX], [0, LY], color=GRAY, lw=1.0, ls=(0, (2, 3)), zorder=4)
    ax.text(LX + 0.35, 6.2, "10 m", color=GRAY, fontsize=10.5, va="center", zorder=8)
    # The range: the straight line from the AV to the landmark.
    r = h(X_TRUE)
    ax.plot([X_TRUE, LX], [0, LY], color=INK, lw=2.4, zorder=9)
    ax.plot(X_TRUE, 0, "o", color="white", mec=INK, mew=1.2, ms=6, zorder=10)
    label(ax, (18.2, 5.5), f"the range from\nthe AV at 16 m: {r:.2f} m", (9.6, 8.2))
    # The two runs' estimates, as markers just above the road.
    for e, col, run in ((15.5, GREEN, "run 1"), (10.0, ORANGE, "run 2")):
        ax.plot(e, HALF + 0.55, "v", color=col, ms=10, zorder=8)
    label(ax, (15.5, HALF + 0.75), "run 1: the estimate, 15.5 m", (6.2, 5.0), color=GREEN)
    label(ax, (10.0, HALF + 0.75), "run 2: the estimate, 10 m", (1.0, 3.6), color=ORANGE)
    # The two legs of the right triangle, under the road.
    dim(ax, 0.0, X_TRUE, -2.9, f"$x$ = {X_TRUE:g} m")
    dim(ax, X_TRUE, LX, -2.9, f"20 $-$ $x$ = {LX - X_TRUE:g} m", color="#555555")
    ax.plot([0, 0], [-HALF, -3.4], color=INK, lw=0.8, zorder=4)
    ax.plot([LX, LX], [-HALF, -3.4], color=GRAY, lw=0.8, ls=(0, (2, 3)), zorder=4)
    ax.set_xlim(-1.0, 23.0)
    ax.set_ylim(-4.6, 11.2)
    ax.set_aspect("equal")
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.set_yticks([0, 5, 10])
    ax.set_xlabel("position along the road, $x$ (m)")
    ax.set_ylabel("across the road (m)")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    path = mf.OUT / "range_road_top.png"
    mf.save(fig, path)
    print(path, f"h(16) = {r:.3f} m")


if __name__ == "__main__":
    main()
