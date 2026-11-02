"""ekf_bend_ellipses.png: EKF predict only on the hands-on's bend, Q left out.

    /usr/bin/python3 tools/filters_figs/ekf_bend_ellipses.py

Model from the deck's gen_ekf_story.py (fig_ellipse), which follows f and jacobian_f in
carla-python lecture3/curved_tunnel/ekf_curve.py: 10 m/s, 60 m radius, 0.1 s steps, 30 steps.
Start: sigma 0.3 m east and north, heading sigma 3 deg (chosen for this example), Q = 0.
Writes docs/source/_static/images/filters/ekf_bend_ellipses.png, 300 dpi, RGB, white.
"""
import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from make_filters_figures import GRAY, INK, ORANGE, OUT, label, save  # noqa: E402

V, DT, R = 10.0, 0.1, 60.0                  # m/s, s, m: the hands-on's speed, step, bend


def run():
    om = V / R
    x = np.array([0.0, 0.0, 0.0])
    P = np.diag([0.3 ** 2, 0.3 ** 2, np.radians(3.0) ** 2])
    states, covs = [x.copy()], [P.copy()]
    for _ in range(30):
        F = np.array([[1, 0, -V * DT * np.sin(x[2])],
                      [0, 1, V * DT * np.cos(x[2])],
                      [0, 0, 1]])
        x = np.array([x[0] + V * DT * np.cos(x[2]), x[1] + V * DT * np.sin(x[2]), x[2] + om * DT])
        P = F @ P @ F.T
        states.append(x.copy())
        covs.append(P.copy())
    return np.array(states), covs


def along_across(P2, th):
    """1-sigma along and across the direction of travel."""
    u = np.array([np.cos(th), np.sin(th)])
    n = np.array([-np.sin(th), np.cos(th)])
    return float(np.sqrt(u @ P2 @ u)), float(np.sqrt(n @ P2 @ n))


def ellipse(P2, n_sigma=2.0):
    vals, vecs = np.linalg.eigh(P2)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]
    ang = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))
    w, h = 2 * n_sigma * np.sqrt(np.maximum(vals, 0))
    return w, h, ang


def main():
    S, covs = run()
    fig, ax = plt.subplots(figsize=(9.6, 4.15))
    ax.plot(S[:, 0], S[:, 1], color=INK, lw=2.2, zorder=3)
    ax.plot(S[::5, 0], S[::5, 1], "o", color=INK, ms=5, zorder=4)
    for k in (0, 10, 20, 30):
        w, h, ang = ellipse(covs[k][:2, :2])
        ax.add_patch(Ellipse(S[k, :2], w, h, angle=ang, fc=ORANGE, alpha=0.18, ec="none", zorder=2))
        ax.add_patch(Ellipse(S[k, :2], w, h, angle=ang, fill=False, ec=ORANGE, lw=1.8, zorder=2))
        th = S[k, 2]
        ax.annotate("", xy=(S[k, 0] + 2.4 * np.cos(th), S[k, 1] + 2.4 * np.sin(th)),
                    xytext=(S[k, 0], S[k, 1]),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4), zorder=5)
        if k < 30:                          # below the ellipse
            ax.text(S[k, 0], S[k, 1] - 2 * np.sqrt(covs[k][1, 1]) - 0.3, f"{k / 10:.0f} s",
                    fontsize=10.5, color=GRAY, ha="center", va="top", zorder=6)
        else:                               # above and left of it
            ax.text(S[k, 0] - 1.2, S[k, 1] + 2 * np.sqrt(covs[k][1, 1]) - 0.4,
                    f"{k / 10:.0f} s", fontsize=10.5, color=GRAY, ha="right", va="top", zorder=6)
    a0, c0 = along_across(covs[0][:2, :2], S[0, 2])
    a3, c3 = along_across(covs[30][:2, :2], S[30, 2])
    label(ax, (0.0, 0.3), f"at 0 s: σ = {a0:.1f} m each way,\nheading σ = 3°",
          (-1.5, 6.3))
    vals = np.sqrt(np.linalg.eigvalsh(covs[30][:2, :2]))
    label(ax, (S[30, 0] + 0.45, S[30, 1] - 2.9),
          f"at 3 s: σ = {vals[1]:.2f} m the long way,\n{vals[0]:.2f} m the short way",
          (23.0, -1.6), color=ORANGE)
    th3 = S[30, 2]
    label(ax, (S[30, 0] + 2.4 * np.cos(th3), S[30, 1] + 2.4 * np.sin(th3)), "the heading",
          (32.8, 10.8))
    xm = 15.0
    label(ax, (xm, float(np.interp(xm, S[:, 0], S[:, 1]))),
          "the estimate: an arc\nfrom the real f", (9.0, 4.6))
    ax.text(-1.5, 11.6, "each ellipse: 2σ", fontsize=10.5, color=ORANGE, ha="left", va="top")
    ax.set_aspect("equal")
    ax.set_xlim(-2, 37)
    ax.set_ylim(-3.0, 12)
    ax.set_xlabel("east (m)")
    ax.set_ylabel("north (m)")
    ax.grid(color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    save(fig, OUT / "ekf_bend_ellipses.png")
    for k in (0, 10, 20, 30):
        a, c = along_across(covs[k][:2, :2], S[k, 2])
        ev = np.sqrt(np.linalg.eigvalsh(covs[k][:2, :2]))
        w_, h_, ang_ = ellipse(covs[k][:2, :2])
        tilt = (ang_ - np.degrees(S[k, 2])) % 180
        print(f"  ellipse axes (1 sigma): long {ev[1]:.3f} m, short {ev[0]:.3f} m; "
              f"long axis {tilt:.1f} deg from the heading")
        print(f"t {k / 10:.0f} s: pos ({S[k, 0]:.2f}, {S[k, 1]:.2f}) heading "
              f"{np.degrees(S[k, 2]):.2f} deg, sigma along {a:.3f} across {c:.3f} m")


if __name__ == "__main__":
    main()
