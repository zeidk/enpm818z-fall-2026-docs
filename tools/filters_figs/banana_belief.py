"""banana_belief.png: where the AV could be after 20 m with a wide heading spread.

    /usr/bin/python3 tools/filters_figs/banana_belief.py

Model and draws from the deck's gen_breaks.py (panel 2_banana): seed 12, 500 draws,
distance 20 +- 0.5 m, heading 0 +- 12 deg (both chosen for the example). The EKF puts its
mean at the full 20 m and its 2-sigma ellipse comes from the tangent at heading 0:
0.5 m along the road, 20 m x 12 deg (in rad) across it.
Writes docs/source/_static/images/filters/banana_belief.png, 300 dpi, RGB, white.
"""
import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Rectangle

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from make_filters_figures import (BLUE, GRAY, INK, ORANGE, OUT, ROAD, draw_av,  # noqa: E402
                                  label, save)


def main():
    rng = np.random.default_rng(12)
    n, d0, sd, sig = 500, 20.0, 0.5, np.radians(12.0)
    d = rng.normal(d0, sd, n)
    th = rng.normal(0.0, sig, n)
    px, py = d * np.cos(th), d * np.sin(th)
    mx, my = float(px.mean()), float(py.mean())

    fig, ax = plt.subplots(figsize=(10.0, 6.0))
    lane = 3.5                    # two lanes; the AV drives in the right-hand one, centered on y = 0
    x0, x1 = -4.0, 37.0
    ax.add_patch(Rectangle((x0, -lane / 2), x1 - x0, 2 * lane, fc=ROAD, ec="none", zorder=0))
    ax.plot([x0, x1], [lane / 2, lane / 2], color="white", lw=2, ls=(0, (6, 5)), zorder=1)
    for sgn in (-1, 1):           # the heading spread, +-1 sigma
        ax.plot([0, 24 * np.cos(sig)], [0, sgn * 24 * np.sin(sig)], color=GRAY, lw=1.4,
                ls=(0, (4, 3)), zorder=2)
    arc = np.linspace(-2.6 * sig, 2.6 * sig, 120)       # every spot 20 m from the start
    ax.plot(20 * np.cos(arc), 20 * np.sin(arc), color=GRAY, lw=1.3, ls=(0, (1.5, 2.5)), zorder=2)
    ax.scatter(px, py, s=8, color=BLUE, alpha=0.5, lw=0, zorder=3)
    draw_av(ax, 0.0, 0.0, 0.0)
    ax.annotate("", xy=(7.5, 0), xytext=(4.0, 0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8), zorder=6)
    e_w, e_h = 2 * 2 * sd, 2 * 2 * d0 * sig            # the EKF's 2-sigma ellipse
    ax.add_patch(Ellipse((d0, 0.0), e_w, e_h, fill=False, ec=ORANGE, lw=2.2, ls=(0, (5, 3)),
                         zorder=4))
    ax.plot(d0, 0.0, "o", ms=7, color=ORANGE, mec="white", mew=1.4, zorder=6)
    ax.plot(mx, my, "X", ms=9, color=INK, mec="white", mew=1.3, zorder=7)

    label(ax, (1.2, 1.0), "the AV, heading east", (-3.5, 6.5))
    label(ax, (10.0, -10.0 * np.tan(sig)), "heading spread:\n±12° (1σ)", (2.0, -6.0),
          color="#555555")
    a = 2.45 * sig
    label(ax, (20 * np.cos(a), 20 * np.sin(a)), "every spot 20 m\nfrom the start", (6.0, 9.6),
          color="#555555")
    label(ax, (18.7, 9.3), "where the AV could be\nafter 20 m: 500 draws", (25.5, 8.0),
          color=BLUE)
    yy = -4.0
    label(ax, (d0 + sd * 2 * np.sqrt(1 - (yy / (e_h / 2)) ** 2), yy),
          "the EKF's 2σ ellipse:\nstraight, from one tangent", (25.5, -5.0), color=ORANGE)
    label(ax, (d0 + 0.25, 0.15), f"the EKF's mean: {d0:.2f} m ahead", (25.5, 2.4), color=ORANGE)
    label(ax, (mx - 0.2, my - 0.2), f"the real middle:\n{mx:.2f} m ahead", (8.5, -9.0))

    ax.set_xlim(x0, x1)
    ax.set_ylim(-11.5, 11.5)
    ax.set_aspect("equal")
    ax.set_xlabel("east (m)")
    ax.set_ylabel("north (m)")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "banana_belief.png")
    print(f"banana: EKF mean {d0:.2f} m, real middle {mx:.3f} m ahead ({my:.3f} m north), "
          f"sigma ahead {px.std():.3f} m; EKF 2-sigma ellipse {e_w:.2f} x {e_h:.2f} m")


if __name__ == "__main__":
    main()
