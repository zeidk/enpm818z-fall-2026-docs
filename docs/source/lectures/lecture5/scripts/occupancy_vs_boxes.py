#!/usr/bin/env python3
"""Occupancy grid vs. detection boxes, in BEV.

L5, 3D Occupancy Networks and "Occupancy vs. Detection: When to Use Which".
A detector reports only the classes it was trained on, as boxes. An
occupancy grid reports, for every cell, whether something is there, whatever
it is. This script builds both views of one scene and asks a planner's
question: is the lane ahead clear?

The scene, seen from above: a parked car, a pedestrian, two concrete barriers, and a
fallen ladder lying across the ego lane. The ladder is in no class the
detector knows.

How the occupancy grid is built (2D, for one sensor at the origin):
    * a 360 deg scanner casts beams and returns the range to the first hit;
    * every cell a beam passes through gets evidence for FREE;
    * the cell where it stops gets evidence for OCCUPIED;
    * evidence adds up in log-odds, l = log(p / (1 - p)), one scan after another.
Cells no beam reaches keep l = 0: p = 0.5, UNKNOWN.

Frames: ego x forward, y right, z up. The plots show y to the right and x up.

Examples
--------
    python3 occupancy_vs_boxes.py
    python3 occupancy_vs_boxes.py --beam-step 2.0      # a coarser scanner
    python3 occupancy_vs_boxes.py --scans 1 --noise 0.10
    python3 occupancy_vs_boxes.py --save occupancy.png

Requires only NumPy and Matplotlib.
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np

MAX_RANGE = 30.0
GRID_X = (-10.0, 30.0)
GRID_Y = (-15.0, 15.0)

L_FREE, L_OCC, L_CLAMP = -0.4, 0.85, 4.0   # log-odds per observation, and the clamp

EGO_HALF_WIDTH = 0.9      # the ego car is 1.8 m wide
LANE_MARGIN = 0.2         # the corridor the planner checks: |y| < 1.1 m
CORRIDOR_X = (2.5, 25.0)


def rectangle(cx, cy, length, width, yaw_deg):
    """The four edges of a rotated rectangle, as (start, end) segments."""
    yaw = np.radians(yaw_deg)
    along = np.array([np.cos(yaw), np.sin(yaw)]) * length / 2
    across = np.array([-np.sin(yaw), np.cos(yaw)]) * width / 2
    c = np.array([cx, cy])
    corners = [c + along + across, c - along + across, c - along - across, c + along - across]
    return [(corners[i], corners[(i + 1) % 4]) for i in range(4)]


# The scene: name, edges, and whether the detector knows the class.
CAR = ("car", rectangle(12.0, -4.0, 4.5, 1.8, 0.0), True)
LADDER = ("ladder", rectangle(16.0, 0.2, 2.6, 0.12, 25.0), False)
BARRIER_L = ("barrier", [(np.array([-10.0, -6.5]), np.array([30.0, -6.5]))], False)
BARRIER_R = ("barrier", [(np.array([-10.0, 6.0]), np.array([30.0, 6.0]))], False)
SEGMENT_OBJECTS = [CAR, LADDER, BARRIER_L, BARRIER_R]
PEDESTRIAN = (7.0, 3.2, 0.3)   # x, y, radius: the detector knows this class


def cast(angles):
    """Range to the first hit for each beam from the origin (inf: nothing within range)."""
    dirs = np.stack([np.cos(angles), np.sin(angles)], axis=-1)       # (B, 2), x and y
    best = np.full(len(angles), np.inf)
    for _, edges, _ in SEGMENT_OBJECTS:
        for a, b in edges:
            e = b - a
            denom = dirs[:, 0] * (-e[1]) - dirs[:, 1] * (-e[0])
            with np.errstate(divide="ignore", invalid="ignore"):
                t = (a[0] * (-e[1]) - a[1] * (-e[0])) / denom          # along the beam
                s = (dirs[:, 0] * a[1] - dirs[:, 1] * a[0]) / denom    # along the edge
            hit = (np.abs(denom) > 1e-12) & (t > 0) & (s >= 0) & (s <= 1)
            best = np.where(hit & (t < best), t, best)
    px, py, pr = PEDESTRIAN
    b = dirs @ np.array([px, py])
    disc = b ** 2 - (px ** 2 + py ** 2 - pr ** 2)
    with np.errstate(invalid="ignore"):
        t = b - np.sqrt(disc)
    hit = (disc >= 0) & (t > 0)
    best = np.where(hit & (t < best), t, best)
    return np.where(best <= MAX_RANGE, best, np.inf)


def update(logodds, angles, ranges, res):
    """Add one scan's evidence to the log-odds grid."""
    rows, cols = logodds.shape
    for ang, rng in zip(angles, ranges):
        end = rng if np.isfinite(rng) else MAX_RANGE
        t = np.arange(0.0, end - res / 2, res / 2)                    # free samples
        fx, fy = t * np.cos(ang), t * np.sin(ang)
        r = ((fx - GRID_X[0]) / res).astype(int)
        c = ((fy - GRID_Y[0]) / res).astype(int)
        ok = (r >= 0) & (r < rows) & (c >= 0) & (c < cols)
        cells = np.unique(r[ok] * cols + c[ok])                       # each cell once per beam
        hit_cell = None
        if np.isfinite(rng):
            hr = int((rng * np.cos(ang) - GRID_X[0]) / res)
            hc = int((rng * np.sin(ang) - GRID_Y[0]) / res)
            if 0 <= hr < rows and 0 <= hc < cols:
                hit_cell = hr * cols + hc
                cells = cells[cells != hit_cell]
        logodds.flat[cells] += L_FREE
        if hit_cell is not None:
            logodds.flat[hit_cell] += L_OCC
    np.clip(logodds, -L_CLAMP, L_CLAMP, out=logodds)


def detector_boxes():
    """What a car/pedestrian detector reports: axis-aligned boxes for known classes."""
    boxes = []
    for name, edges, known in SEGMENT_OBJECTS:
        if known:
            pts = np.array([p for e in edges for p in e])
            boxes.append((name, pts[:, 0].min(), pts[:, 0].max(), pts[:, 1].min(), pts[:, 1].max()))
    px, py, pr = PEDESTRIAN
    boxes.append(("pedestrian", px - pr, px + pr, py - pr, py + pr))
    return boxes


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--beam-step", type=float, default=0.5, help="degrees between beams (default 0.5)")
    parser.add_argument("--res", type=float, default=0.2, help="grid cell size, m (default 0.2)")
    parser.add_argument("--scans", type=int, default=5, help="scans to accumulate (default 5)")
    parser.add_argument("--noise", type=float, default=0.02, help="range noise sigma, m (default 0.02)")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--save", help="write the figure to this file instead of showing it")
    args = parser.parse_args()

    rng_gen = np.random.default_rng(args.seed)
    angles = np.radians(np.arange(0.0, 360.0, args.beam_step))
    rows = int((GRID_X[1] - GRID_X[0]) / args.res)
    cols = int((GRID_Y[1] - GRID_Y[0]) / args.res)
    logodds = np.zeros((rows, cols))
    true_ranges = cast(angles)
    for _ in range(args.scans):
        noisy = true_ranges + rng_gen.normal(0.0, args.noise, size=true_ranges.shape)
        update(logodds, angles, noisy, args.res)
    p = 1.0 - 1.0 / (1.0 + np.exp(logodds))

    # The planner's question: is the corridor ahead clear?
    xs = GRID_X[0] + (np.arange(rows) + 0.5) * args.res
    ys = GRID_Y[0] + (np.arange(cols) + 0.5) * args.res
    gx, gy = np.meshgrid(xs, ys, indexing="ij")
    half = EGO_HALF_WIDTH + LANE_MARGIN
    corridor = (np.abs(gy) < half) & (gx >= CORRIDOR_X[0]) & (gx <= CORRIDOR_X[1])
    occupied = p > 0.7
    blocked = corridor & occupied
    boxes = detector_boxes()
    box_in = [b for b in boxes if b[2] >= CORRIDOR_X[0] and b[1] <= CORRIDOR_X[1]
              and b[4] > -half and b[3] < half]
    print(f"{len(angles)} beams, {args.scans} scan(s), {args.res} m cells")
    print(f"detector boxes in the corridor: {[b[0] for b in box_in] or 'none'} -> "
          f"{'blocked' if box_in else 'clear'}")
    if blocked.any():
        print(f"occupancy cells in the corridor with p > 0.7: {blocked.sum()}, "
              f"nearest at x = {gx[blocked].min():.1f} m -> blocked")
    else:
        print("occupancy cells in the corridor with p > 0.7: 0 -> clear")
    print(f"cells still unknown (p = 0.5): {(logodds == 0).sum()} of {logodds.size}")

    extent = [GRID_Y[0], GRID_Y[1], GRID_X[0], GRID_X[1]]
    fig, ax = plt.subplots(1, 3, figsize=(16, 6.5))
    # 1. The scene, with every 8th beam
    for ang, r in zip(angles[::8], true_ranges[::8]):
        end = r if np.isfinite(r) else MAX_RANGE
        ax[0].plot([0, end * np.sin(ang)], [0, end * np.cos(ang)], color="orange", lw=0.4)
    for name, edges, _ in SEGMENT_OBJECTS:
        for a, b in edges:
            ax[0].plot([a[1], b[1]], [a[0], b[0]], color="red" if name == "ladder" else "black", lw=2)
    ax[0].add_patch(plt.Circle((PEDESTRIAN[1], PEDESTRIAN[0]), PEDESTRIAN[2], color="black"))
    ax[0].set_title("Scene and beams (ladder in red)")
    # 2. Occupancy probability
    ax[1].imshow(np.flipud(p), cmap="gray_r", vmin=0, vmax=1, extent=extent)
    ax[1].set_title("Occupancy: black occupied, white free, gray unknown")
    # 3. Detector boxes
    ax[2].set_facecolor("whitesmoke")
    for name, x0, x1, y0, y1 in boxes:
        ax[2].add_patch(plt.Rectangle((y0, x0), y1 - y0, x1 - x0, fill=False, edgecolor="blue", lw=2))
        ax[2].text(y1 + 0.3, x0, name, color="blue", fontsize=9)
    ax[2].set_title("Detector: boxes for known classes only")
    for a in ax:
        a.add_patch(plt.Rectangle((-half, CORRIDOR_X[0]), 2 * half, CORRIDOR_X[1] - CORRIDOR_X[0],
                                  fill=False, edgecolor="green", lw=1.5, ls="--"))
        a.plot(0, 0, marker="^", color="green", markersize=10)
        a.set_xlim(GRID_Y)
        a.set_ylim(GRID_X)
        a.set_aspect("equal")
        a.set_xlabel("y, right (m)")
        a.set_ylabel("x, forward (m)")
    fig.suptitle("Green dashes: the corridor the planner needs clear")
    fig.tight_layout()
    if args.save:
        fig.savefig(args.save, dpi=100)
        print(f"wrote {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
