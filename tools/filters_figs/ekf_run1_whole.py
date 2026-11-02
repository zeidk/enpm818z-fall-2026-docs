"""ekf_run1_whole.png: run 1 on the whole range curve (preread/nonlinear-filters.rst,
"The surprise says the AV is farther ahead").

    /usr/bin/python3 tools/filters_figs/ekf_run1_whole.py

The AV is really at 16 m, so a perfect reading is h(16) = 10.77 m. Run 1's estimate is 15.5 m,
where the filter expects h(15.5). The tangent at 15.5 m meets the reading line at the new
estimate. The gray box marks the part drawn close up in ekf_run1.png, the page's next figure;
its limits are those of run1() in tools/make_filters_figures.py. Labels and colors match that
close-up: green for run 1, purple for the tangent, gray dotted for the reading.
"""
import pathlib
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import make_filters_figures as mf                                   # noqa: E402
import matplotlib.pyplot as plt                                     # noqa: E402
from matplotlib.patches import Rectangle                            # noqa: E402

INK, GRAY, GREEN, PURPLE = mf.INK, mf.GRAY, mf.GREEN, mf.PURPLE
h, slope, label = mf.h, mf.slope, mf.label
X_TRUE, E = 16.0, 15.5
ZOOM = (14.0, 17.2, 10.3, 11.45)            # x0, x1, y0, y1 of ekf_run1.png


def main():
    read = h(X_TRUE)
    he, k = h(E), slope(E)
    new = E + (read - he) / k
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    xs = [4.0 + i * 0.02 for i in range(801)]
    ax.plot(xs, [h(x) for x in xs], color=INK, lw=2.6, zorder=3)
    tx = [11.5 + i * 0.02 for i in range(301)]
    ax.plot(tx, [he + k * (x - E) for x in tx], color=PURPLE, lw=1.6, ls=(0, (6, 4)), zorder=4)
    ax.axhline(read, color="#888888", lw=1.2, ls=(0, (2, 3)), zorder=2)
    ax.plot([X_TRUE, X_TRUE], [8.6, read], color="#888888", lw=1.2, ls=(0, (2, 3)), zorder=2)
    x0, x1, y0, y1 = ZOOM
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec=GRAY, lw=0.9, zorder=2))
    ax.plot(E, he, "o", color=GREEN, ms=9, mec="white", zorder=9)
    ax.plot(new, read, "X", color=GREEN, ms=10, mec="white", zorder=10)
    ax.text(4.3, read + 0.15, f"the camera reads {read:.2f} m", color="#555555", ha="left", va="bottom",
            fontsize=10.5)
    label(ax, (E, he), f"the estimate, {E:g} m:\nthe filter expects {he:.2f} m", (9.0, 15.4), color=GREEN)
    label(ax, (E - 0.05, (he + read) / 2), f"surprise: {he - read:.2f} m less range", (7.0, 9.6))
    label(ax, (12.0, he + k * (12.0 - E)), f"the tangent at {E:g} m", (7.6, 12.3), color=PURPLE)
    label(ax, (new, read), f"where the tangent meets\nthe reading: {new:.2f} m", (17.0, 13.6), color=GREEN)
    label(ax, (X_TRUE, 9.3), "the AV really is at 16 m", (16.6, 9.3))
    label(ax, (x1, y1 - 0.3), "drawn close up\nin the next figure", (17.7, 11.75), color="#555555")
    ax.text(6.3, h(6.3) + 0.35, "the real range, $h(x)$", fontsize=10.5, rotation=-27)
    mf.range_axes(ax, 4.0, 20.0, 8.6, 19.4)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    path = mf.OUT / "ekf_run1_whole.png"
    mf.save(fig, path)
    print(path, f"read {read:.3f}, expect {he:.3f}, surprise {read - he:.3f}, slope {k:.3f}, new {new:.3f}")


if __name__ == "__main__":
    main()
