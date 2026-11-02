"""tunnel_clusters.png: how many places the particle crowd is in, over the tunnel drive, for the
reading preread/nonlinear-filters.rst ("The particle filter hands-on: finding a lost AV").

    /usr/bin/python3 tools/filters_figs/tunnel_clusters.py

Same run as tunnel_belief.py: the hands-on's run_pf(), 2,000 particles, camera sigma 1 m,
seed 1. The count is the hands-on's n_clusters: clusters holding more than 2% of the weight.
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
from make_filters_figures import INK, GRAY, PURPLE, OUT, plt, save   # noqa: E402
import pf_tunnel as pf                                                # noqa: E402

T = 12.0


def main():
    d, mp = pf.load(os.path.join(PF_DIR, "pf_drive.csv"), os.path.join(PF_DIR, "tunnel_map.csv"))
    h = pf.run_pf(d, mp, 2000, pf.SIGMA_CAM, seed=1, keep_every=10**9)
    t, nc = d["t"], h["n_clusters"]
    niches = [t[i] for i in range(len(t)) if d["match"][i] == "niche"]

    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    for tn in niches:
        ax.axvline(tn, color=GRAY, lw=0.9, alpha=0.6, zorder=1)
        ax.text(tn, 26.3, "niche", ha="center", va="bottom", fontsize=9.5, color=GRAY, clip_on=False)
    ax.axvline(T, color=INK, lw=1.0, ls=(0, (1, 2)), zorder=1)
    ax.text(T + 0.4, 21.0, "12 s", fontsize=10, ha="left", va="center")
    ax.step(t, nc, where="post", color=PURPLE, lw=2.2, zorder=3)
    # Each level, labeled where it starts.
    changes = [0] + [i for i in range(1, len(t)) if nc[i] != nc[i - 1]]
    shown = {}
    for i in changes:
        if t[i] < 0.5 and i != 0:
            continue                          # the 22 / 23 flicker in the first half second
        shown[int(nc[i])] = t[i]
    notes = {23: "23 at the start:\none per light", 4: "4 after the\nfirst niche"}
    ends = changes[1:] + [len(t)]
    for n, t0 in shown.items():
        text = notes.get(n, str(n))
        if n == 1:
            text = f"1 from {t0:.1f} s on"
        if n == 23:
            ax.text(2.6, 22.0, text, fontsize=10.5, color=PURPLE, va="center", ha="left")
        elif n == 18:
            ax.text(0.9, n + 0.5, text, fontsize=10.5, color=PURPLE, va="bottom", ha="left")
        elif n == 4:
            ax.text(t0 + 0.5, n + 0.5, text, fontsize=10.5, color=PURPLE, va="bottom", ha="left")
        else:
            ax.text(t0 + 0.6, n + 0.5, text, fontsize=10.5, color=PURPLE, va="bottom", ha="left")
    ax.set_xlim(0, t[-1])
    ax.set_ylim(0, 26)
    ax.set_yticks([0, 5, 10, 15, 20, 25])
    ax.set_xlabel("time (s)")
    ax.set_ylabel("number of places (clusters)")
    ax.grid(axis="y", color="#e6e6e6", lw=0.8, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "tunnel_clusters.png")
    print("tunnel_clusters: niche matches at", ", ".join(f"{x:.1f}" for x in niches), "s")
    for i in changes:
        print(f"  t = {t[i]:4.1f} s: {nc[i]} clusters")


if __name__ == "__main__":
    main()
