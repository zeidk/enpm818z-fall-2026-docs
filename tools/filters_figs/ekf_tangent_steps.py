"""ekf_tangent_steps.png: the EKF's trick, one tangent per step (preread/nonlinear-filters.rst).

    /usr/bin/python3 tools/filters_figs/ekf_tangent_steps.py

The curve is the page's range to the sign, r = sqrt((20 - x)^2 + 10^2), named r and
"the sign" as in line_or_curve.png because the page defines h(x) only after this figure. The three estimates,
4, 9 and 14 m, are chosen for the picture (as in the L3 deck's ekf_story_2_steps). At each one
a short tangent stands in for the curve for that step; the tangent at 4 m is also drawn long, to
show how far off it is far from 4 m. Style, colors and helpers come from
tools/make_filters_figures.py: the tangent is purple, as in ekf_run1.png and ekf_run2.png.
"""
import pathlib
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import make_filters_figures as mf                                   # noqa: E402
import matplotlib.pyplot as plt                                     # noqa: E402

INK, PURPLE = mf.INK, mf.PURPLE
h, slope, label = mf.h, mf.slope, mf.label


def main():
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    xs = [i * 0.02 for i in range(1201)]
    ax.plot(xs, [h(x) for x in xs], color=INK, lw=2.6, zorder=3)
    steps = (4.0, 9.0, 14.0)
    # The tangent at the first estimate, drawn long: right near 4 m, wrong far from it.
    e0 = steps[0]
    far = 18.0
    tl = [i * 0.02 for i in range(int(far / 0.02) + 1)]
    ax.plot(tl, [h(e0) + slope(e0) * (x - e0) for x in tl], color=PURPLE, lw=1.4,
            ls=(0, (6, 4)), zorder=2)
    t_far, h_far = h(e0) + slope(e0) * (far - e0), h(far)
    ax.annotate("", xy=(far, h_far), xytext=(far, t_far),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.0, shrinkA=0, shrinkB=0), zorder=6)
    ax.plot(far, t_far, "o", color=PURPLE, ms=5, zorder=7)
    # One short tangent at each estimate: the straight line the EKF uses for that step.
    for e in steps:
        seg = [e - 2.2 + i * 0.044 for i in range(101)]
        ax.plot(seg, [h(e) + slope(e) * (x - e) for x in seg], color=PURPLE, lw=7, alpha=0.45,
                solid_capstyle="round", zorder=4)
        ax.plot(e, h(e), "o", color=PURPLE, ms=8, mec="white", mew=1.5, zorder=8)
    # Word labels, each beside its own mark.
    for n, (e, xt, yt) in enumerate(zip(steps, (5.2, 10.2, 15.2), (21.6, 17.6, 14.4)), start=1):
        label(ax, (e, h(e)), f"step {n}: the estimate, {e:g} m,\nand the tangent there", (xt, yt))
    label(ax, (22.0, h(22.0)), "the real range, $r$", (19.6, 17.4))
    label(ax, (13.0, h(e0) + slope(e0) * (13.0 - e0)), "the tangent at 4 m, drawn long", (5.0, 9.4),
          color=PURPLE)
    label(ax, (far, (t_far + h_far) / 2),
          f"at 18 m it says {t_far:.2f} m;\nthe real range is {h_far:.2f} m", (19.0, 8.2))
    ax.set_xlim(0, 24)
    ax.set_ylim(5.5, 24.5)
    ax.set_xlabel("AV's position along the road, $x$ (m)")
    ax.set_ylabel("range to the sign, $r$ (m)")
    ax.grid(color="#e6e6e6", lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    path = mf.OUT / "ekf_tangent_steps.png"
    mf.save(fig, path)
    print(path)
    for e in steps:
        print(f"  estimate {e:g} m: h = {h(e):.2f} m, slope {slope(e):.3f}")
    print(f"  at {far:g} m: tangent from {e0:g} m says {t_far:.2f} m, h = {h_far:.2f} m")


if __name__ == "__main__":
    main()
