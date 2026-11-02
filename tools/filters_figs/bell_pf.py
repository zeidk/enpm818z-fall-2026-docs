"""bell_pf.png: 200 random headings pushed through x = 20 cos(theta), for the reading
preread/nonlinear-filters.rst ("The Particle Filter").

    /usr/bin/python3 tools/filters_figs/bell_pf.py

Same three panels, left to right, as bell_curve.png (tools/make_filters_figures.py):
what the AV knows, the function, what you get. The random numbers repeat the deck's
gen_bells.py (L3 bell_5_pf): one generator, seed 818, first 400,000 headings for the true
output, then 200 headings for the particles. The 400,000 are the same draw bell_curve()
uses, so the true mean, 16.95 m, matches that figure.

Dots are stacked: each dot is one point, and each stack holds the points that fall in one
bin (2.5 deg in Step 1, 0.5 m in Step 3). A stack is drawn to the same density scale as the
curve behind it, so the two can be compared: one dot is 1 / (200 x 2.5) = 0.002 per degree in
Step 1 and 1 / (200 x 0.5) = 0.01 per m in Step 3. Both y axes are labeled and numbered.
"""
import math
import pathlib
import sys

import numpy as np

sys.dont_write_bytecode = True          # importing the style also imports the deck's avdraw.py
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from make_filters_figures import (INK, GRAY, BLUE, PURPLE, OUT, bell, label,  # noqa: E402
                                  plain, plt, save)

TH0, SIG = 30.0, 12.0
NPTS = 200


def stack(ax, values, bins, color, ms):
    """One dot per value, piled in its bin; dot j of a stack sits at height (j + 0.5) * unit."""
    width = bins[1] - bins[0]
    unit = 1.0 / (len(values) * width)            # one dot, in density units
    idx = np.digitize(values, bins) - 1
    for b in np.unique(idx):
        n = int(np.sum(idx == b))
        xc = bins[b] + width / 2
        ax.plot([xc] * n, (np.arange(n) + 0.5) * unit, "o", color=color, ms=ms, mec="white",
                mew=0.4, zorder=5, clip_on=False)
    return unit


def three_steps():
    """Three panels read left to right, every y axis labeled and numbered."""
    fig, axs = plt.subplots(1, 3, figsize=(10.6, 3.7))
    for ax, t in zip(axs, ("Step 1: what the AV knows", "Step 2: the function", "Step 3: what you get")):
        ax.set_title(t, fontsize=12, fontweight="bold", loc="left")
        plain(ax)
    return fig, axs


def main():
    rng = np.random.default_rng(818)
    true_x = 20 * np.cos(np.radians(rng.normal(TH0, SIG, 400_000)))
    p_th = rng.normal(TH0, SIG, NPTS)
    p_x = 20 * np.cos(np.radians(p_th))
    t_mean, p_mean = float(true_x.mean()), float(p_x.mean())

    fig, axs = three_steps()

    # Step 1: the input bell curve, and the 200 random headings stacked under it.
    th = np.linspace(-10, 70, 300)
    axs[0].fill_between(th, bell(th, TH0, SIG), color=GRAY, alpha=0.3, lw=0)
    axs[0].plot(th, bell(th, TH0, SIG), color=INK, lw=2)
    stack(axs[0], p_th, np.arange(-10, 72.5, 2.5), PURPLE, 3.0)
    axs[0].set_xlabel("heading, $\\theta$ (deg)")
    axs[0].set_ylabel("probability density (per degree)")
    axs[0].set_xlim(-10, 70)
    axs[0].set_ylim(0, 0.046)
    axs[0].text(-8, 0.0435, "$\\theta$ = 30° ± 12°", fontsize=10.5, va="center")
    label(axs[0], (49.2, 0.0108), "200 random\nheadings", (51.0, 0.024), color=PURPLE)

    # Step 2: each point goes through the real curve. One point is followed with a guide.
    axs[1].plot(th, 20 * np.cos(np.radians(th)), color=INK, lw=2.4, zorder=3)
    axs[1].plot(p_th, p_x, "o", color=PURPLE, ms=3.0, mec="white", mew=0.4, zorder=5)
    i = int(np.argmin(np.abs(p_th - 45.0)))       # the point nearest 45 deg
    axs[1].plot([p_th[i], p_th[i], -10], [6, p_x[i], p_x[i]], color=INK, lw=0.9, ls=(0, (1, 2)),
                zorder=2)
    axs[1].set_xlim(-10, 70)
    axs[1].set_ylim(6, 21.5)
    axs[1].set_xlabel("heading, $\\theta$ (deg)")
    axs[1].set_ylabel("distance east, $x$ (m)")
    axs[1].text(-8, 7.0, "$x$ = 20 cos $\\theta$:\na curve", fontsize=10.5)
    label(axs[1], (p_th[i], p_x[i]), f"one point: {p_th[i]:.1f}°\ngives {p_x[i]:.2f} m",
          (46.0, 18.6), color=PURPLE)

    # Step 3: where the 200 points land, over the true output (400,000 points).
    axs[2].hist(true_x, bins=np.arange(6, 20.25, 0.25), density=True, color=BLUE, alpha=0.18,
                edgecolor="none", zorder=1)
    axs[2].hist(true_x, bins=np.arange(6, 20.25, 0.25), density=True, histtype="step",
                color=BLUE, lw=0.9, zorder=2)
    stack(axs[2], p_x, np.arange(6, 20.5, 0.5), PURPLE, 3.0)
    axs[2].axvline(t_mean, color=INK, lw=1.4, zorder=6)
    axs[2].axvline(p_mean, color=PURPLE, lw=1.4, ls=(0, (3, 2)), zorder=6)
    axs[2].set_xlim(6, 21)
    axs[2].set_xticks([7.5, 10.0, 12.5, 15.0, 17.5, 20.0])
    axs[2].set_ylim(0, 0.46)
    axs[2].set_xlabel("distance east, $x$ (m)")
    axs[2].set_ylabel("probability density (per m)")
    axs[2].text(6.3, 0.445, "dots: where the\n200 points land", fontsize=10.5, color=PURPLE, va="top")
    label(axs[2], (p_mean, 0.315), f"mean of the dots:\n{p_mean:.2f} m", (8.0, 0.315), color=PURPLE)
    label(axs[2], (t_mean, 0.225), f"true mean:\n{t_mean:.2f} m", (11.0, 0.225))
    label(axs[2], (8.5, 0.012), "blue: the true shape\n(400,000 points)", (6.6, 0.135), color=BLUE)

    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "bell_pf.png")
    print(f"bell_pf: true mean {t_mean:.3f} m, mean of {NPTS} points {p_mean:.3f} m, "
          f"followed point {p_th[i]:.2f} deg -> {p_x[i]:.2f} m, "
          f"headings {p_th.min():.1f} to {p_th.max():.1f} deg, x {p_x.min():.2f} to {p_x.max():.2f} m")


if __name__ == "__main__":
    main()
