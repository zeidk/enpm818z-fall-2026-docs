"""tunnel_belief.png: the particle filter's belief 12 s into the tunnel drive, for the reading
preread/nonlinear-filters.rst ("The particle filter hands-on: finding a lost AV").

    /usr/bin/python3 tools/filters_figs/tunnel_belief.py

The run is the hands-on's own: run_pf() from carla-python lecture3/pf_tunnel/pf_tunnel.py on
its pf_drive.csv and tunnel_map.csv, 2,000 particles, camera sigma 1 m, seed 1, the same run
the deck's gen_tunnel_pf_panels.py draws. That repo is only read: no bytecode is written there.
The bars are the hands-on's own: the weight in each 2 m bin from 0 to 702 m.
"""
import os
import pathlib
import sys

import numpy as np

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parents[2]
PF_DIR = ROOT.parents[1] / "workspace/enpm818z-fall-2026-carla-python/lecture3/pf_tunnel"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(PF_DIR))
from make_filters_figures import INK, ORANGE, PURPLE, OUT, label, plt, save   # noqa: E402
import pf_tunnel as pf                                                          # noqa: E402

T = 12.0                                     # s, the moment shown


def main():
    d, mp = pf.load(os.path.join(PF_DIR, "pf_drive.csv"), os.path.join(PF_DIR, "tunnel_map.csv"))
    h = pf.run_pf(d, mp, 2000, pf.SIGMA_CAM, seed=1)
    k = int(round(T / pf.DT))
    parts, w = h["parts"][k], h["w"][k]
    true_s, mean = d["true_s"][k], h["mean"][k]
    cl = pf.clusters(parts, w)
    bins = np.arange(0, pf.TUNNEL + 2, 2.0)
    hw, _ = np.histogram(parts, bins=bins, weights=w)

    fig, ax = plt.subplots(figsize=(10.0, 3.9))
    ax.bar(bins[:-1], hw, width=2.0, align="edge", color=PURPLE, edgecolor=PURPLE, lw=0.8, zorder=3)
    ax.axvline(true_s, color=INK, lw=1.4, ls=(0, (3, 2)), zorder=2)
    ax.axvline(mean, color=ORANGE, lw=1.4, ls=(0, (3, 2)), zorder=2)
    top = 1.15 * hw.max()
    ax.text(true_s - 6, 0.93 * top, f"where the AV really is,\n{true_s:.0f} m", ha="right", va="top",
            fontsize=10.5)
    ax.text(mean + 6, 0.93 * top, f"weighted average of the\nwhole crowd, {mean:.0f} m", ha="left",
            va="top", fontsize=10.5, color=ORANGE)
    # The three places with more than 2% of the weight (the hands-on's cluster threshold).
    big = [(wt, mu) for wt, mu in cl if wt > 0.02]
    for wt, mu in big:
        b = int(np.argmax(np.where(np.abs(bins[:-1] + 1 - mu) < 4, hw, -1)))
        txt = f"{mu:.0f} m: {100 * wt:.0f}% of the weight"
        if hw[b] > 0.12 and mu < 300:          # left of the bar: the average line is on its right
            label(ax, (bins[b] - 1.0, hw[b] * 0.6), txt, (bins[b] - 25, hw[b] * 0.6), color=PURPLE, ha="right")
        elif hw[b] > 0.12:
            label(ax, (bins[b] + 3.0, hw[b] * 0.85), txt, (bins[b] + 25, hw[b] * 0.85), color=PURPLE)
        else:                                  # a short bar: the label goes above it
            label(ax, (bins[b] + 1.0, hw[b] + 0.005), txt, (bins[b] + 6, hw[b] + 0.09), color=PURPLE)
    ax.set_xlim(-5, pf.TUNNEL + 5)
    ax.set_ylim(0, top)
    ax.set_xlabel("position along the tunnel (m)")
    ax.set_ylabel("weight per 2 m bin")
    ax.grid(axis="y", color="#e6e6e6", lw=0.8, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "tunnel_belief.png")
    print(f"tunnel_belief: t = {d['t'][k]:.1f} s, true {true_s:.2f} m, weighted average {mean:.2f} m, "
          f"heaviest cluster {h['best'][k]:.2f} m, tallest bar {hw.max():.3f}")
    for wt, mu in cl:
        print(f"  cluster at {mu:7.2f} m, weight {wt:.4f}")


if __name__ == "__main__":
    main()
