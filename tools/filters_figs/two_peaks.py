"""two_peaks.png for preread/nonlinear-filters.rst: a two-peaked belief against one bell curve.

    /usr/bin/python3 tools/filters_figs/two_peaks.py

The numbers are those of the L3 deck's gen_breaks.py (breaks_3b_bells): two identical
ceiling lights at 0 m and 25 m; the honest belief is two bell curves, one under each light,
sigma 1.3 m, half the weight each. The one bell curve with the same mean and spread has
mean 12.5 m and sigma sqrt(1.3^2 + 12.5^2) = 12.57 m. The AV is really at 0 m. A graph of
probability density along the tunnel, not a map. Blue: the honest belief (the particle
filter's crowd on the next figures is blue too); orange, dashed: the one bell curve a
Kalman filter can hold.
"""
import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from make_filters_figures import BLUE, INK, ORANGE, OUT, bell, label, plain, plt, save  # noqa: E402

LIGHT, LIGHT_EDGE = "#f2c14e", "#b9861a"


def main():
    spk, mu = 1.3, 12.5
    sbell = math.hypot(spk, mu)
    xs = np.linspace(-15, 40, 1200)
    two = 0.5 * bell(xs, 0, spk) + 0.5 * bell(xs, 25, spk)
    one = bell(xs, mu, sbell)
    # Check: the two-peaked belief has this mean and spread.
    dx = xs[1] - xs[0]
    m2 = float((xs * two).sum() * dx)
    s2 = float(math.sqrt(((xs - m2) ** 2 * two).sum() * dx))

    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    plain(ax)
    ax.fill_between(xs, two, color=BLUE, alpha=0.18, lw=0, zorder=2)
    ax.plot(xs, two, color=BLUE, lw=2.4, zorder=3)
    ax.fill_between(xs, one, color=ORANGE, alpha=0.12, lw=0, zorder=2)
    ax.plot(xs, one, color=ORANGE, lw=2.4, ls=(0, (5, 3)), zorder=4)
    ax.plot([mu, mu], [0, bell(mu, mu, sbell)], color=ORANGE, lw=1.4, ls=(0, (1, 2)), zorder=3)
    for lx in (0.0, 25.0):                     # where the lights are along the tunnel
        ax.plot(lx, 0.178, marker="s", ms=11, color=LIGHT, mec=LIGHT_EDGE, mew=1.2,
                clip_on=False, zorder=6)
        ax.text(lx + 1.3, 0.178, f"a light at {lx:.0f} m", fontsize=10.5, va="center",
                color="#555555")
    ax.plot(0, 0.0, marker="P", ms=12, color=INK, mec="white", mew=1.2, zorder=7, clip_on=False)
    label(ax, (1.2, 0.12), "the honest belief: two peaks,\nσ = 1.3 m each,\nhalf the weight each",
          (4.5, 0.13), color=BLUE)
    ax.plot([18.0, 23.8], [0.135, 0.12], color=BLUE, lw=0.8, zorder=30)   # to the other peak
    label(ax, (33.0, bell(33.0, mu, sbell)), f"one bell curve with\nthe same mean\n"
          f"and spread: σ = {sbell:.1f} m", (28.0, 0.075), color=ORANGE)
    label(ax, (mu, 0.02), f"its mean, {mu} m: between\nthe lights, where the honest\n"
          "belief is near zero", (4.5, 0.075), color=ORANGE)
    label(ax, (-0.4, 0.004), "the AV is\nreally at 0 m", (-14.0, 0.06))
    ax.set_xlim(-15, 40)
    ax.set_ylim(0, 0.19)
    ax.set_yticks([0, 0.05, 0.10, 0.15])
    ax.set_xticks([-10, 0, 10, 12.5, 20, 25, 30, 40])
    ax.set_xticklabels(["−10", "0", "10", "12.5", "20", "25", "30", "40"])
    ax.set_xlabel("position along the tunnel (m)")
    ax.set_ylabel("probability density (per m)")
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "two_peaks.png")
    print(f"two peaks: mean {m2:.3f} m, sigma {s2:.3f} m, peak {two.max():.4f} per m; "
          f"one bell: sigma {sbell:.3f} m, peak {one.max():.4f} per m; "
          f"honest belief at 12.5 m: {0.5 * bell(12.5, 0, spk) + 0.5 * bell(12.5, 25, spk):.2e}")


if __name__ == "__main__":
    main()
