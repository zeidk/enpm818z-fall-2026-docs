"""pf_cycle_steps.png: one particle filter cycle (predict, weigh, resample) in one dimension,
for the reading preread/nonlinear-filters.rst ("One cycle: predict, weigh, resample").

    /usr/bin/python3 tools/filters_figs/pf_cycle_steps.py

The model and the random numbers repeat the deck's gen_pf_cycle.py (L3 pf_cycle): seed 3,
40 particles near 8 m (sigma 1.6 m), predict 10 m/s for 1 s plus a kick of sigma 1.2 m, a
sign match at z = 20.5 m with sigma 1.5 m, then rng.choice for the resample.

Display only: in Step 3 the columns of copies of two particles that sit closer than one dot
width are spread apart (at most a few tenths of a meter) so each column can be seen and counted.
"""
import pathlib
import sys

import numpy as np

sys.dont_write_bytecode = True          # importing the style also imports the deck's avdraw.py
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from make_filters_figures import INK, GRAY, PURPLE, OUT, label, plt, save   # noqa: E402

N = 40
V, DT, SIG_Q = 10.0, 1.0, 1.2          # motion: 10 m/s for 1 s, then a kick
Z, SIG_R = 20.5, 1.5                   # the sign match and its sigma
XLO, XHI = 3.0, 27.0
GAP = 0.2                              # m, one dot width at this scale


def spread(xs, gap):
    """Spread sorted column positions so neighbors are at least gap apart, each group kept
    centered on its own mean."""
    xs = list(xs)
    groups = [[x] for x in xs]
    while True:
        pos = []
        for g in groups:
            c = float(np.mean(g))
            pos.append([c + gap * (j - (len(g) - 1) / 2) for j in range(len(g))])
        merged = False
        for i in range(len(groups) - 1):
            if pos[i + 1][0] - pos[i][-1] < gap - 1e-9:
                groups[i] = groups[i] + groups[i + 1]
                del groups[i + 1]
                merged = True
                break
        if not merged:
            return [p for g in pos for p in g]


def strip(ax, title):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    ax.grid(axis="x", color="#e6e6e6", lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def main():
    rng = np.random.default_rng(3)
    x0 = rng.normal(8.0, 1.6, N)                              # last cycle's particles
    x1 = x0 + V * DT + rng.normal(0, SIG_Q, N)                # predict
    lik = np.exp(-0.5 * ((Z - x1) / SIG_R) ** 2)              # weigh
    w = lik / lik.sum()
    idx = rng.choice(N, N, p=w)                               # resample
    x2 = x1[idx]
    u, counts = np.unique(np.round(x2, 6), return_counts=True)

    fig, axs = plt.subplots(3, 1, figsize=(10.0, 7.4), sharex=True,
                            gridspec_kw={"height_ratios": [0.8, 1.15, 1.15]})

    # Step 1: predict. The crowd moves 10 m and spreads.
    ax = axs[0]
    strip(ax, "Step 1: predict")
    ax.set_ylim(-0.5, 1.3)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.axhline(0, color="#cccccc", lw=1.0, zorder=1)
    ax.plot(x0, np.zeros(N), "o", color=GRAY, alpha=0.55, ms=6, mec="none", zorder=3)
    ax.plot(x1, np.zeros(N), "o", color=PURPLE, alpha=0.8, ms=6, mec="none", zorder=4)
    ax.annotate("", xy=(x1.mean() - 3.0, 0.75), xytext=(x0.mean() + 3.0, 0.75),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
    ax.text((x0.mean() + x1.mean()) / 2, 0.95, "each moves 10 m/s for 1 s, plus its own random kick",
            ha="center", va="bottom", fontsize=10.5)
    ax.text(x0.mean(), 0.35, "the 40 particles, last cycle", ha="center", fontsize=10.5, color=GRAY)
    ax.text(x1.mean() + 0.6, 0.35, "after predict: more spread out", ha="center", fontsize=10.5,
            color=PURPLE)

    # Step 2: weigh. Nothing moves; each particle gets a score.
    ax = axs[1]
    strip(ax, "Step 2: weigh")
    xx = np.linspace(XLO, XHI, 600)
    score = np.exp(-0.5 * ((Z - xx) / SIG_R) ** 2)
    ax.fill_between(xx, score, color=INK, alpha=0.07, lw=0, zorder=1)
    ax.plot(xx, score, color=INK, lw=1.6, zorder=2)
    ax.axvline(Z, color=GRAY, lw=1.2, ls=(0, (2, 3)), zorder=2)
    ax.scatter(x1, np.zeros(N), s=6 + 900 * w, color=PURPLE, edgecolor="white", linewidth=0.8,
               zorder=5, clip_on=False)
    ax.set_ylim(0, 1.25)
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_ylabel("score")
    ax.text(Z + 0.3, 1.1, f"the sign match: z = {Z:.1f} m, $\\sigma$ = {SIG_R:.1f} m", color="#555555",
            fontsize=10.5, va="center")
    label(ax, (Z - 1.6, float(np.exp(-0.5 * (1.6 / SIG_R) ** 2))),
          "the score: how well a particle\nhere explains the reading", (8.0, 0.75))
    k = int(np.argmax(w))
    label(ax, (x1[k] + 0.1, 0.05), f"big dot: heavy,\nweight {w[k]:.3f}", (23.4, 0.45), color=PURPLE)
    j = int(np.argmin(x1))
    label(ax, (x1[j], 0.02), "tiny dot: far from the match,\nweight close to 0", (4.0, 0.25),
          color=PURPLE)

    # Step 3: resample. Copies of the heavy particles, stacked; the light ones are gone.
    ax = axs[2]
    strip(ax, "Step 3: resample")
    shown = spread(u, GAP)
    for xs, c in zip(shown, counts):
        ax.plot([xs] * c, np.arange(1, c + 1), "o", color=PURPLE, ms=5.5, mec="white", mew=0.6,
                zorder=5, clip_on=False)
    ax.set_ylim(0, 8.6)
    ax.set_yticks([1, 3, 5, 7])
    ax.set_ylabel("copies")
    top = int(np.argmax(counts))
    label(ax, (shown[top] + 0.2, counts[top]),
          f"{counts[top]} copies of the particle at {u[top]:.2f} m", (22.5, 7.0), color=PURPLE)
    ax.text(4.0, 5.0, f"40 particles again,\nbut only {len(u)} different ones", fontsize=10.5,
            color=PURPLE, va="center")
    ax.set_xlim(XLO, XHI)
    ax.set_xlabel("position along the tunnel (m)")

    fig.patch.set_facecolor("white")
    fig.tight_layout(h_pad=1.0)
    save(fig, OUT / "pf_cycle_steps.png")
    print(f"heaviest particle at {x1[np.argmax(w)]:.2f} m")
    print(f"pf_cycle_steps: last cycle {x0.min():.2f} to {x0.max():.2f} m, after predict "
          f"{x1.min():.2f} to {x1.max():.2f} m, resampled {x2.min():.2f} to {x2.max():.2f} m; "
          f"{len(u)} distinct of {N}; heaviest weight {w.max():.3f}; tallest stack {counts.max()} at "
          f"{u[top]:.2f} m; largest display shift {max(abs(a - b) for a, b in zip(shown, u)):.2f} m; "
          f"N_eff {1 / np.sum(w ** 2):.1f}")


if __name__ == "__main__":
    main()
