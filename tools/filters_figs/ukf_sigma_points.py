"""ukf_sigma_points.png for preread/nonlinear-filters.rst: the UKF predict step on the drive.

    /usr/bin/python3 tools/filters_figs/ukf_sigma_points.py

The model and numbers are those of the L3 deck's gen_ukf_story.py (fig_drive): the AV drives
d = 20 +- 0.5 m from the origin with heading theta = 0 +- 12 deg (0 = east). State [d, theta],
n = 2, kappa = 1, weights 1/3 (center) and 1/6. f(d, theta) = (d cos theta, d sin theta).
The cloud is 4,000 samples of the same model (seed 12). Three panels, left to right: place
the five sigma points, push each through f, rebuild one bell curve (the UKF) next to the
EKF's. Gray: the input and the cloud; green: the UKF; orange: the EKF.
"""
import math
import pathlib
import sys

import numpy as np
from matplotlib.patches import Ellipse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from make_filters_figures import (GRAY, GREEN, INK, ORANGE, OUT, draw_av, label,  # noqa: E402
                                  plain, plt, save)

D, SD, ST = 20.0, 0.5, math.radians(12.0)


def ellipse(ax, mean, P, color, **kw):
    """The 2 sigma ellipse of P, centered on mean."""
    vals, vecs = np.linalg.eigh(P)
    i = int(np.argmax(vals))
    ang = math.degrees(math.atan2(vecs[1, i], vecs[0, i]))
    w, h = 4 * math.sqrt(vals[i]), 4 * math.sqrt(vals[1 - i])
    ax.add_patch(Ellipse(mean, w, h, angle=ang, ec=color, **kw))


def main():
    r3 = math.sqrt(3.0)
    sd, st = r3 * SD, r3 * ST
    # chi_0 the mean, chi_1 d +, chi_2 theta +, chi_3 d -, chi_4 theta -: the page's order.
    pts = [(D, 0.0), (D + sd, 0.0), (D, st), (D - sd, 0.0), (D, -st)]
    W = np.array([1 / 3] + [1 / 6] * 4)
    land = np.array([(d * math.cos(t), d * math.sin(t)) for d, t in pts])
    mean = W @ land
    dif = land - mean
    P = (W[:, None, None] * np.einsum("ij,ik->ijk", dif, dif)).sum(0)
    rng = np.random.default_rng(12)
    d_s, t_s = rng.normal(D, SD, 4000), rng.normal(0, ST, 4000)
    smp = np.c_[d_s * np.cos(t_s), d_s * np.sin(t_s)]
    P_ekf = np.diag([SD ** 2, (D * ST) ** 2])
    true_x = D * math.exp(-ST ** 2 / 2)                 # exact mean of d cos theta

    fig, axs = plt.subplots(1, 3, figsize=(13.0, 4.8),
                            gridspec_kw=dict(width_ratios=[1.0, 1.05, 0.9]))
    titles = ("Step 1: place five points", "Step 2: push each through $f$",
              "Step 3: rebuild a bell curve")
    for ax, t in zip(axs, titles):
        plain(ax)

    # Step 1: the input, distance driven against heading. A graph, not a map.
    ax = axs[0]
    ax.add_patch(Ellipse((0, D), 4 * 12, 4 * SD, fc=GRAY, alpha=0.2, lw=0))
    off = [(-0.08, "top"), (0.08, "bottom"), (0.08, "bottom"), (-0.08, "top"), (0.08, "bottom")]
    for i, ((d, t), w, (dy, va)) in enumerate(zip(pts, W, off)):
        ax.plot(math.degrees(t), d, "o", color=GREEN, ms=9, mec="white", zorder=8)
        wt = "1/3" if w > 0.3 else "1/6"
        ax.text(math.degrees(t), d + dy, f"$\\chi_{i}$\nweight {wt}", color=GREEN, fontsize=10,
                ha="center", va=va, zorder=9)
    ax.text(-31, 21.62, "gray, the input\n(2σ ellipse):\n$d$ = 20 ± 0.5 m\n$\\theta$ = 0° ± 12°",
            color="#555555", fontsize=10, va="top")
    ax.set_xlim(-32, 32)
    ax.set_ylim(18.65, 21.7)
    ax.set_xlabel("heading, $\\theta$ (deg)")
    ax.set_ylabel("distance driven, $d$ (m)")

    # Step 2: seen from above. The AV starts at the origin facing east.
    ax = axs[1]
    ax.scatter(smp[:, 0], smp[:, 1], s=2.5, color=GRAY, alpha=0.3, lw=0, zorder=2)
    for x, y in land:
        ax.plot([0, x], [0, y], color=GREEN, lw=0.8, alpha=0.6, zorder=3)
        ax.plot(x, y, "o", color=GREEN, ms=8, mec="white", zorder=8)
    draw_av(ax, 0.0, 0.0, 0.0, L=3.0, rear=0.6)
    label(ax, (0.8, -0.7), "the AV starts here,\nfacing east", (0.3, -5.6))
    label(ax, (17.4, 9.0), "gray: 4,000\npossible AVs", (5.0, 9.6), color="#555555")
    label(ax, (land[2][0], land[2][1]), f"$\\chi_2$ lands {land[2][0]:.2f} m east,\n"
          f"{land[2][1]:.1f} m north", (3.0, 6.0), color=GREEN)
    label(ax, (land[4][0], land[4][1]), f"$\\chi_4$ lands {land[4][0]:.2f} m east,\n"
          f"{-land[4][1]:.1f} m south", (5.0, -9.3), color=GREEN)
    ax.text(5.5, 0.9, "$\\chi_3$, $\\chi_0$, $\\chi_1$ stay on this line", color=GREEN,
            fontsize=10, va="bottom")
    ax.set_xlim(-1.5, 23)
    ax.set_ylim(-11, 11)
    ax.set_aspect("equal")
    ax.set_xlabel("east (m)")
    ax.set_ylabel("north (m)")

    # Step 3: the same view, closer. The UKF's bell curve and the EKF's, both 2 sigma.
    ax = axs[2]
    keep = np.abs(smp[:, 1]) < 11.0            # the cloud as in Step 2; the space above is for labels
    ax.scatter(smp[keep, 0], smp[keep, 1], s=2.5, color=GRAY, alpha=0.3, lw=0, zorder=2)
    ellipse(ax, mean, P, GREEN, fc=GREEN, alpha=0.15, lw=0, zorder=3)
    ellipse(ax, mean, P, GREEN, fc="none", lw=2.0, zorder=4)
    ellipse(ax, (D, 0.0), P_ekf, ORANGE, fc="none", lw=2.0, ls=(0, (4, 3)), zorder=5)
    ax.plot(mean[0], mean[1], "o", color=GREEN, ms=6, mec="white", mew=0.8, zorder=8)
    ax.plot(D, 0.0, "o", color=ORANGE, ms=6, mec="white", mew=0.8, zorder=8)
    gx = 19.0                                   # a point on each ellipse's top
    gy = 2 * math.sqrt(P[1, 1]) * math.sqrt(1 - ((gx - mean[0]) / (2 * math.sqrt(P[0, 0]))) ** 2)
    ex = 20.5
    ey = 2 * D * ST * math.sqrt(1 - ((ex - D) / (2 * SD)) ** 2)
    label(ax, (gx, gy), "UKF ellipse", (15.3, 12.6), color=GREEN)
    label(ax, (ex, ey), "EKF ellipse", (22.6, 10.0), color=ORANGE)
    label(ax, (mean[0], 0.25), f"UKF mean:\n{mean[0]:.2f} m east", (22.6, 2.6), color=GREEN)
    label(ax, (D + 0.1, -0.25), f"EKF mean:\n{D:.2f} m east", (22.6, -2.4), color=ORANGE)
    ax.text(22.6, -7.6, f"middle of the\ngray cloud:\n{true_x:.2f} m east", fontsize=10,
            color="#555555", va="center")
    ax.set_xlim(15.0, 30.0)
    ax.set_ylim(-11, 14)
    ax.set_aspect("equal")
    ax.set_xlabel("east (m)")
    ax.set_ylabel("north (m)")

    fig.patch.set_facecolor("white")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    for ax, t in zip(axs, titles):              # titles on one line, though the panels differ
        fig.text(ax.get_position().x0, 0.965, t, fontsize=12, fontweight="bold", va="top")
    save(fig, OUT / "ukf_sigma_points.png")
    print("land:", np.round(land, 3))
    print(f"UKF mean {mean[0]:.3f} m, sigma along {math.sqrt(P[0, 0]):.3f}, across "
          f"{math.sqrt(P[1, 1]):.3f}; exact mean {true_x:.3f}; cloud mean {smp[:, 0].mean():.3f}, "
          f"sigma along {smp[:, 0].std():.3f}, across {smp[:, 1].std():.3f}; "
          f"EKF across {D * ST:.3f}")


if __name__ == "__main__":
    main()
