"""bell_ekf.png: the EKF pushes the heading bell curve through the tangent at 30 degrees.

    /usr/bin/python3 tools/filters_figs/bell_ekf.py

Same three steps, layout, seed (818) and sample count (400,000) as bell_curve() in
tools/make_filters_figures.py, so the two figures compare panel by panel. Model from the
deck's gen_bells.py (panel 3_ekf): x = 20 cos(theta), theta = 30 +- 12 deg, tangent at 30.
Writes docs/source/_static/images/filters/bell_ekf.png, 300 dpi, RGB, white.
"""
import math
import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from make_filters_figures import (BLUE, GRAY, INK, ORANGE, OUT, bell, label,  # noqa: E402
                                  plain, save)


def three_steps():
    """One row of three panels, read left to right. Every axis keeps its ticks and label:
    the bell and histogram panels show probability density."""
    fig, axs = plt.subplots(1, 3, figsize=(10.6, 3.7))
    for ax, t in zip(axs, ("Step 1: what the AV knows", "Step 2: the function", "Step 3: what you get")):
        ax.set_title(t, fontsize=12, fontweight="bold", loc="left")
        plain(ax)
    axs[0].set_ylabel("probability density (per degree)")
    axs[2].set_ylabel("probability density (per m)")
    return fig, axs


def main():
    fig, axs = three_steps()
    th = np.linspace(-10, 70, 300)
    x30 = 20 * math.cos(math.radians(30))
    k = -20 * math.sin(math.radians(30)) * math.pi / 180.0       # tangent slope, m per degree
    e_sig = abs(k) * 12.0                                         # EKF spread, m
    e_lo, e_hi = x30 - e_sig, x30 + e_sig

    # Step 1: the heading, exactly as in bell_curve.png.
    axs[0].fill_between(th, bell(th, 30, 12), color=GRAY, alpha=0.3, lw=0)
    axs[0].plot(th, bell(th, 30, 12), color=INK, lw=2)
    axs[0].axvspan(18, 42, color=GRAY, alpha=0.25, lw=0)
    axs[0].set_xlabel("heading, $\\theta$ (deg)")
    axs[0].text(-9, 0.0385, "$\\theta$ = 30° ± 12°", fontsize=10.5)
    axs[0].text(30, 0.043, "18° to 42°", fontsize=10, color="#555555", ha="center")
    axs[0].set_ylim(0, 0.046)

    # Step 2: the curve and, in orange, the tangent the EKF uses in its place.
    axs[1].plot(th, 20 * np.cos(np.radians(th)), color=INK, lw=2.4, zorder=3)
    axs[1].plot(th, x30 + k * (th - 30), color=ORANGE, lw=2.0, ls=(0, (5, 3)), zorder=4)
    axs[1].axvspan(18, 42, color=GRAY, alpha=0.25, lw=0)
    axs[1].axhspan(e_lo, e_hi, color=ORANGE, alpha=0.15, lw=0)
    axs[1].plot([30, 30, -10], [6, x30, x30], color=INK, lw=0.9, ls=(0, (1, 2)))
    axs[1].plot(30, x30, "o", color=ORANGE, ms=8, mec="white", zorder=6)
    axs[1].set_xlim(-10, 70)
    axs[1].set_ylim(6, 21.5)
    axs[1].set_xlabel("heading, $\\theta$ (deg)")
    axs[1].set_ylabel("distance east, $x$ (m)")
    axs[1].text(-8, 7.0, "$x$ = 20 cos $\\theta$:\nthe curve", fontsize=10.5)
    label(axs[1], (12, x30 + k * (12 - 30)), "the tangent at 30°:\na straight line", (40, 20.75),
          color=ORANGE)
    axs[1].text(56, (e_lo + e_hi) / 2, f"{e_lo:.2f} to\n{e_hi:.2f} m", fontsize=10, color=ORANGE,
                ha="center", va="center")

    # Step 3: the true output (blue bars, same samples as bell_curve.png) and the EKF's bell.
    rng = np.random.default_rng(818)
    xs = 20 * np.cos(np.radians(rng.normal(30, 12, 400_000)))
    t_mean, t_sig = float(xs.mean()), float(xs.std())
    axs[2].hist(xs, bins=np.arange(6, 20.25, 0.25), density=True, color=BLUE, alpha=0.35,
                edgecolor=BLUE, lw=0.6)
    xx = np.linspace(6, 24, 600)
    axs[2].plot(xx, bell(xx, x30, e_sig), color=ORANGE, lw=2.2, ls=(0, (5, 3)), zorder=4)
    axs[2].axvline(t_mean, ymax=0.86, color=INK, lw=1.6, zorder=3)
    axs[2].axvline(x30, ymax=0.86, color=ORANGE, lw=1.4, zorder=3)
    axs[2].axvline(20, ymax=0.62, color="#888888", lw=0.9, ls=(0, (1, 2)), zorder=2)
    axs[2].set_xlim(6, 24)
    axs[2].set_ylim(0, 0.42)
    axs[2].set_xlabel("distance east, $x$ (m)")
    axs[2].text(6.3, 0.41, f"the EKF:\n{x30:.2f} ± {e_sig:.2f} m", fontsize=10.5, color=ORANGE,
                va="top")
    axs[2].text(6.3, 0.32, f"the truth:\n{t_mean:.2f} ± {t_sig:.2f} m", fontsize=10.5,
                color=BLUE, va="top")
    label(axs[2], (t_mean, 0.235), f"true mean,\n{t_mean:.2f} m", (7.0, 0.235))
    label(axs[2], (x30, 0.345), f"EKF mean,\n{x30:.2f} m", (19.0, 0.345), color=ORANGE)
    xs_spill = 21.0
    label(axs[2], (xs_spill, float(bell(xs_spill, x30, e_sig))), "above 20 m:\nimpossible",
          (21.0, 0.21), color=ORANGE)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "bell_ekf.png")
    above = 0.5 * math.erfc((20 - x30) / (e_sig * math.sqrt(2)))
    print(f"bell_ekf: slope {k:.4f} m/deg, EKF {x30:.3f} +- {e_sig:.3f} m "
          f"({e_lo:.2f} to {e_hi:.2f}); truth {t_mean:.3f} +- {t_sig:.3f} m; "
          f"EKF mass above 20 m {above:.3f}; max sample {xs.max():.4f}")


if __name__ == "__main__":
    main()
