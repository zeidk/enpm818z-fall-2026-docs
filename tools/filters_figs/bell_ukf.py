"""bell_ukf.png for preread/nonlinear-filters.rst: the UKF on the heading example.

    /usr/bin/python3 tools/filters_figs/bell_ukf.py

theta = 30 +- 12 deg through x = 20 cos theta, the example of bell_curve.png, in the same
three panels read left to right. The UKF places three sigma points (n = 1, kappa = 2,
n + kappa = 3, weights 2/3 and 1/6), pushes each through the real curve and rebuilds one
bell curve from where they land. The true output is the histogram of bell_curve(): the
same seed (818) and the same 400,000 samples. Green is the UKF, blue the true output.
"""
import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from make_filters_figures import (BLUE, GRAY, GREEN, INK, OUT, bell, label,  # noqa: E402
                                  plt, save, three_steps)


def main():
    n, kappa = 1, 2.0
    step = math.sqrt(n + kappa) * 12.0
    pts = np.array([30.0 - step, 30.0, 30.0 + step])               # deg
    w = np.array([0.5 / (n + kappa), kappa / (n + kappa), 0.5 / (n + kappa)])
    wtxt = ("1/6", "2/3", "1/6")
    land = 20 * np.cos(np.radians(pts))                            # m
    u_mu = float(w @ land)
    u_sig = float(np.sqrt(w @ (land - u_mu) ** 2))
    rng = np.random.default_rng(818)                               # as bell_curve()
    xs = 20 * np.cos(np.radians(rng.normal(30, 12, 400_000)))
    t_mu, t_sig = float(xs.mean()), float(xs.std())

    fig, axs = three_steps(None, None, None)
    for ax, t in zip(axs, ("Step 1: place three points", "Step 2: push each through the curve",
                           "Step 3: average with the weights")):
        ax.set_title(t, fontsize=12, fontweight="bold", loc="left")

    # Step 1: the heading bell curve and the three sigma points on it.
    th = np.linspace(-10, 70, 300)
    axs[0].fill_between(th, bell(th, 30, 12), color=GRAY, alpha=0.3, lw=0)
    axs[0].plot(th, bell(th, 30, 12), color=INK, lw=2)
    axs[0].set_xlabel("heading, $\\theta$ (deg)")
    axs[0].set_ylabel("probability density (per degree)")
    axs[0].text(-9, 0.0385, "$\\theta$ = 30° ± 12°", fontsize=10.5)
    for p, wt in zip(pts, wtxt):
        b = bell(p, 30, 12)
        axs[0].plot([p, p], [0, b], color=GREEN, lw=1.2, ls=(0, (1, 2)))
        axs[0].plot(p, b, "o", color=GREEN, ms=9, mec="white", zorder=8)
        text = f"{p:.1f}".replace(".0", "") + f"°\nweight {wt}"
        if wt == "2/3":
            axs[0].text(p, b + 0.0025, text, color=GREEN, fontsize=10, ha="center", va="bottom")
        else:                                   # the side points: labels in the empty corners
            label(axs[0], (p, b), text, (-9.0 if p < 30 else 52.0, 0.024), color=GREEN)
    axs[0].set_ylim(0, 0.046)                                  # as bell_curve.png

    # Step 2: the real curve; each point goes up to it and across to x.
    axs[1].plot(th, 20 * np.cos(np.radians(th)), color=INK, lw=2.4)
    for p, y in zip(pts, land):
        axs[1].plot([p, p, -10], [6, y, y], color=GREEN, lw=0.9, ls=(0, (1, 2)))
        axs[1].plot(p, y, "o", color=GREEN, ms=9, mec="white", zorder=8)
    for p, y, dx, dy in zip(pts, land, (2.5, 2.5, 2.5), (0.55, 0.55, 0.55)):
        axs[1].text(p + dx, y + dy, f"{y:.2f} m", color=GREEN, fontsize=10, ha="left",
                    va="bottom")
    axs[1].set_xlim(-10, 70)
    axs[1].set_ylim(6, 21.5)
    axs[1].set_xlabel("heading, $\\theta$ (deg)")
    axs[1].set_ylabel("distance east, $x$ (m)")
    axs[1].text(33, 20.9, "$x$ = 20 cos $\\theta$:\nthe real curve", fontsize=10.5, va="top")

    # Step 3: the true output (as in bell_curve.png) and the UKF's rebuilt bell curve.
    axs[2].hist(xs, bins=np.arange(6, 20.25, 0.25), density=True, color=BLUE, alpha=0.35,
                edgecolor=BLUE, lw=0.6)
    x = np.linspace(6, 21, 400)
    axs[2].plot(x, bell(x, u_mu, u_sig), color=GREEN, lw=2.4, zorder=6)
    for y, wt in zip(land, wtxt):
        axs[2].plot(y, 0.0, "o", color=GREEN, ms=8, mec="white", zorder=8, clip_on=False)
    axs[2].set_xlim(6, 21)
    axs[2].set_xticks([10, 15, 20])             # as bell_curve.png
    axs[2].set_ylim(0, 0.42)
    axs[2].set_xlabel("distance east, $x$ (m)")
    axs[2].set_ylabel("probability density (per m)")
    axs[2].text(6.3, 0.40, f"true: {t_mu:.2f} ± {t_sig:.2f} m", fontsize=10.5, color=BLUE,
                va="top")
    axs[2].text(6.3, 0.345, f"UKF: {u_mu:.2f} ± {u_sig:.2f} m", fontsize=10.5, color=GREEN,
                va="top")
    label(axs[2], (u_mu - 2.2, bell(u_mu - 2.2, u_mu, u_sig)), "the UKF's bell curve",
          (7.0, 0.22), color=GREEN)
    label(axs[2], (12.64, 0.004), "where the\nthree points land", (7.0, 0.09), color=GREEN)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "bell_ukf.png")
    print("bell_ukf: points", np.round(pts, 2), "land", np.round(land, 3),
          f"UKF {u_mu:.3f} +- {u_sig:.3f}, true {t_mu:.3f} +- {t_sig:.3f}")


if __name__ == "__main__":
    main()
