"""ekf_feedback_loop.png: the EKF's divergence loop, as a diagram.

    /usr/bin/python3 tools/filters_figs/ekf_feedback_loop.py

Text and layout from the deck's gen_ekf_story.py (fig_loop), in the page's colors: gray for
the starting point, orange for the EKF's loop.
Writes docs/source/_static/images/filters/ekf_feedback_loop.png, 300 dpi, RGB, white.
"""
import pathlib
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from make_filters_figures import GRAY, INK, ORANGE, OUT, save  # noqa: E402

FS = 11.5


def box(ax, xy, text, color, w, h=1.15, fc="white"):
    x, y = xy
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.08,rounding_size=0.18",
                                fc=fc, ec=color, lw=1.8))
    ax.text(x, y, text, ha="center", va="center", fontsize=FS, color=INK)


def arrow(ax, a, b, color, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16,
                                 connectionstyle=f"arc3,rad={rad}", color=color, lw=1.6))


def main():
    fig, ax = plt.subplots(figsize=(9.1, 4.1))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(0, 13.55)
    ax.set_ylim(0, 6)
    ax.axis("off")

    start, top, right, bottom, left = (1.9, 5.1), (6.3, 5.1), (9.5, 2.9), (6.3, 0.75), (3.0, 2.9)
    box(ax, start, "The estimate is\na little off", GRAY, w=2.9)
    box(ax, top, "The tangent is drawn\nin the wrong place", ORANGE, w=3.3)
    box(ax, right, "The correction is\nthe wrong size", ORANGE, w=3.0)
    box(ax, bottom, "If it is far enough off,\nthe next estimate is worse", ORANGE, w=3.6)
    box(ax, left, "The next tangent is\ndrawn at that estimate", ORANGE, w=3.2)
    arrow(ax, (3.45, 5.1), (4.55, 5.1), GRAY)
    arrow(ax, (7.9, 4.75), (9.3, 3.55), ORANGE, rad=-0.25)
    arrow(ax, (9.3, 2.25), (8.15, 1.1), ORANGE, rad=-0.25)
    arrow(ax, (4.45, 1.1), (3.0, 2.25), ORANGE, rad=-0.25)
    arrow(ax, (3.0, 3.55), (4.55, 4.75), ORANGE, rad=-0.25)
    ax.text(6.3, 2.9, "each turn\nstarts from\na worse place", ha="center", va="center",
            fontsize=FS - 1, color=ORANGE)
    box(ax, (12.27, 3.0), "Meanwhile\nP shrinks at\nevery update,\nright or wrong.\n\n"
        "Confident\nand wrong:\ndivergence", ORANGE, w=2.05, h=3.3, fc="#fbede8")
    fig.patch.set_facecolor("white")
    save(fig, OUT / "ekf_feedback_loop.png")


if __name__ == "__main__":
    main()
