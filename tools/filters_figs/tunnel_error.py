"""tunnel_error.png: the error of two answers from the same particle crowd, over the tunnel
drive, for the reading preread/nonlinear-filters.rst ("The particle filter hands-on").

    /usr/bin/python3 tools/filters_figs/tunnel_error.py

Same run as tunnel_belief.py: the hands-on's run_pf(), 2,000 particles, camera sigma 1 m,
seed 1. Error = |answer - true position|. The heaviest cluster is h["best"], the weighted
average h["mean"]. The errors run from under a millimeter to 300 m, so the y axis is linear
from 0 to 1 m and logarithmic above (symlog, linthresh 1 m).
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
from make_filters_figures import INK, GRAY, ORANGE, PURPLE, OUT, plt, save   # noqa: E402
import pf_tunnel as pf                                                        # noqa: E402

T = 12.0


def main():
    d, mp = pf.load(os.path.join(PF_DIR, "pf_drive.csv"), os.path.join(PF_DIR, "tunnel_map.csv"))
    h = pf.run_pf(d, mp, 2000, pf.SIGMA_CAM, seed=1, keep_every=10**9)
    t = d["t"]
    e_best = np.abs(h["best"] - d["true_s"])
    e_mean = np.abs(h["mean"] - d["true_s"])
    niches = [t[i] for i in range(len(t)) if d["match"][i] == "niche"]

    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    for tn in niches:
        ax.axvline(tn, color=GRAY, lw=0.9, alpha=0.6, zorder=1)
        ax.text(tn, 1150, "niche", ha="center", va="bottom", fontsize=9.5, color=GRAY)
    ax.axvline(T, color=INK, lw=1.0, ls=(0, (1, 2)), zorder=1)
    ax.text(T + 0.4, 450, "12 s", fontsize=10, ha="left", va="center")
    ax.axhline(1.0, color=INK, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.text(42.8, 1.12, "1 m", fontsize=10, ha="right", va="bottom")
    ax.plot(t, e_mean, color=ORANGE, lw=3.2, zorder=3)
    ax.plot(t, e_best, color=PURPLE, lw=1.8, zorder=4)
    ax.text(6.5, 330, "weighted average", color=ORANGE, fontsize=10.5, ha="center", va="bottom")
    ax.text(6.5, 0.75, "heaviest cluster", color=PURPLE, fontsize=10.5, ha="center", va="center")
    ax.text(26.8, 4.0, "the two answers\nagree: the crowd\nis in one place", color=INK, fontsize=10.5,
            ha="center", va="center")
    ax.set_yscale("symlog", linthresh=1.0, linscale=1.0)
    ax.set_ylim(0, 1000)
    ax.set_yticks([0, 0.5, 1, 10, 100, 1000])
    ax.set_yticklabels(["0", "0.5", "1", "10", "100", "1000"])
    ax.minorticks_off()
    ax.set_xlim(0, t[-1])
    ax.set_xlabel("time (s)")
    ax.set_ylabel("error (m)\nlinear to 1 m, log above")
    ax.grid(axis="y", color="#e6e6e6", lw=0.8, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "tunnel_error.png")

    def first_below(e, lim):
        bad = np.where(e >= lim)[0]
        return t[bad[-1] + 1] if len(bad) else t[0]

    i14 = (t > niches[0]) & (t < niches[1])
    i21 = (t > niches[1]) & (t < niches[2])
    print(f"tunnel_error: heaviest cluster under 1 m from {first_below(e_best, 1.0):.1f} s "
          f"(largest after: {e_best[t >= first_below(e_best, 1.0)].max():.2f} m); weighted average "
          f"under 1 m from {first_below(e_mean, 1.0):.1f} s")
    print(f"  weighted average error: {e_mean[t < niches[0]].min():.0f} to {e_mean[t < niches[0]].max():.0f} m "
          f"before {niches[0]:.1f} s; {e_mean[i14].min():.0f} to {e_mean[i14].max():.0f} m between "
          f"{niches[0]:.1f} and {niches[1]:.1f} s; {e_mean[i21].min():.1f} to {e_mean[i21].max():.1f} m "
          f"between {niches[1]:.1f} and {niches[2]:.1f} s; at {T:.0f} s {e_mean[int(round(T / pf.DT))]:.0f} m")
    print(f"  smallest error plotted: {min(e_best.min(), e_mean.min()):.3f} m; "
          f"largest after {niches[2]:.1f} s: {max(e_best[t >= niches[2]].max(), e_mean[t >= niches[2]].max()):.2f} m")


if __name__ == "__main__":
    main()
