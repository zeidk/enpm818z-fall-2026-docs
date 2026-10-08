#!/usr/bin/env python3
"""Coverage of the six-camera rig of Exercise 2, on a BEV grid.

L5, Multi-Camera Fusion in BEV Space. Do Exercise 2 by hand first, then run
this script to check your sketch and your answers.

For every BEV cell on the ground, the script counts how many cameras see it.
A camera sees a point when the point is in front of it and inside both its
horizontal and its vertical field of view. Exercise 2 gives only the
horizontal FOV (110 deg); the vertical FOV follows from the image size, which
is a parameter here (1600 x 900 by default, as in nuScenes).

The vertical FOV matters on the ground: a camera 1.5 m up cannot see the
ground right below it, so there is a blind ring around the car even where
the horizontal fields overlap.

Frames: ego x forward, y right, z up. Yaw is measured from +x toward +y
(toward the right), as in Exercise 2 (Front-Left has yaw -55 deg).

Examples
--------
    python3 multicam_coverage.py
    python3 multicam_coverage.py --image 1600 1200     # a 4:3 sensor: taller vertical FOV
    python3 multicam_coverage.py --range 20 --save coverage.png

Requires only NumPy and Matplotlib.
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np

# Exercise 2: name, (x, y, z) in meters, yaw in degrees, horizontal FOV in degrees
RIG = [
    ("Front",       (2.0, 0.0, 1.5),    0.0, 110.0),
    ("Front-Left",  (1.5, -0.8, 1.5), -55.0, 110.0),
    ("Front-Right", (1.5, 0.8, 1.5),   55.0, 110.0),
    ("Rear",        (-2.0, 0.0, 1.5), 180.0, 110.0),
    ("Rear-Left",   (-1.5, -0.8, 1.5), -125.0, 110.0),
    ("Rear-Right",  (-1.5, 0.8, 1.5),  125.0, 110.0),
]
CAR_LENGTH, CAR_WIDTH = 4.5, 1.8          # the ego car's footprint, centered at the origin
PEDESTRIAN = (0.0, -3.0)                  # Exercise 2, question 3
PEDESTRIAN_HEIGHT = 1.7


def camera_frame(points, cam):
    """Ego points (N, 3) in one camera's frame: forward, right, up."""
    _, (cx, cy, cz), yaw_deg, _ = cam
    yaw = np.radians(yaw_deg)
    d = points - np.array([cx, cy, cz])
    forward = d[:, 0] * np.cos(yaw) + d[:, 1] * np.sin(yaw)
    right = -d[:, 0] * np.sin(yaw) + d[:, 1] * np.cos(yaw)
    return forward, right, d[:, 2]


def sees(points, cam, vfov_deg, max_range):
    """True for each point inside the camera's frustum and range."""
    hfov_deg = cam[3]
    forward, right, up = camera_frame(points, cam)
    with np.errstate(divide="ignore", invalid="ignore"):
        in_h = np.abs(right / forward) <= np.tan(np.radians(hfov_deg) / 2)
        in_v = np.abs(up / forward) <= np.tan(np.radians(vfov_deg) / 2)
    in_range = np.hypot(forward, right) <= max_range
    return (forward > 0) & in_h & in_v & in_range


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--image", type=int, nargs=2, default=(1600, 900), metavar=("W", "H"),
                        help="image size in pixels, for the vertical FOV (default 1600 900)")
    parser.add_argument("--range", type=float, default=12.0,
                        help="half-size of the plotted area and camera range, m (default 12)")
    parser.add_argument("--res", type=float, default=0.05, help="BEV cell size, m (default 0.05)")
    parser.add_argument("--save", help="write the figure to this file instead of showing it")
    args = parser.parse_args()

    w, h = args.image
    vfov = 2 * np.degrees(np.arctan(np.tan(np.radians(RIG[0][3]) / 2) * h / w))
    print(f"image {w} x {h}: horizontal FOV {RIG[0][3]:.0f} deg, vertical FOV {vfov:.1f} deg")

    # Ground cells
    r = args.range
    xs = np.arange(-r, r, args.res) + args.res / 2
    ys = np.arange(-r, r, args.res) + args.res / 2
    gx, gy = np.meshgrid(xs, ys, indexing="ij")
    ground = np.stack([gx.ravel(), gy.ravel(), np.zeros(gx.size)], axis=-1)
    count = np.zeros(gx.size, dtype=int)
    for cam in RIG:
        count += sees(ground, cam, vfov, r)
    count = count.reshape(gx.shape)

    on_car = (np.abs(gx) <= CAR_LENGTH / 2) & (np.abs(gy) <= CAR_WIDTH / 2)
    near = (np.hypot(gx, gy) <= 5.0) & ~on_car
    cell = args.res ** 2
    print(f"ground within 5 m of the origin, off the car: {near.sum() * cell:.1f} m^2, "
          f"of which no camera sees {((count == 0) & near).sum() * cell:.1f} m^2")
    print(f"ground seen by 2 or more cameras (within {r:.0f} m): {(count >= 2).sum() * cell:.1f} m^2")

    # Exercise 2, question 2: angular overlap of Front and Front-Left
    f_lo, f_hi = 0.0 - 55.0, 0.0 + 55.0
    fl_lo, fl_hi = -55.0 - 55.0, -55.0 + 55.0
    print(f"Front covers yaw [{f_lo:.0f}, {f_hi:.0f}] deg, Front-Left [{fl_lo:.0f}, {fl_hi:.0f}] deg: "
          f"overlap {max(0.0, min(f_hi, fl_hi) - max(f_lo, fl_lo)):.0f} deg")

    # Exercise 2, question 3: the pedestrian, sampled from feet to head
    zs = np.linspace(0.0, PEDESTRIAN_HEIGHT, 18)
    body = np.stack([np.full_like(zs, PEDESTRIAN[0]), np.full_like(zs, PEDESTRIAN[1]), zs], axis=-1)
    seen_by = []
    for cam in RIG:
        seen = sees(body, cam, vfov, r)
        if seen.any():
            seen_by.append(cam[0])
            print(f"{cam[0]:>11} sees the pedestrian from z = {zs[seen].min():.2f} m "
                  f"to z = {zs[seen].max():.2f} m")
    if not seen_by:
        print(f"no camera sees the pedestrian at x = {PEDESTRIAN[0]} m, y = {PEDESTRIAN[1]} m")

    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    cmap = plt.get_cmap("viridis", 4)
    im = ax.imshow(np.flipud(np.minimum(count, 3)), cmap=cmap, vmin=-0.5, vmax=3.5,
                   extent=[-r, r, -r, r], origin="upper")
    # The plot's horizontal axis is ego y (right) and its vertical axis is ego x (forward).
    ax.add_patch(plt.Rectangle((-CAR_WIDTH / 2, -CAR_LENGTH / 2), CAR_WIDTH, CAR_LENGTH,
                               facecolor="white", edgecolor="black"))
    for name, (cx, cy, _), yaw, _ in RIG:
        ax.plot(cy, cx, "ko", markersize=4)
        ax.arrow(cy, cx, 1.2 * np.sin(np.radians(yaw)), 1.2 * np.cos(np.radians(yaw)),
                 head_width=0.25, color="black")
    ax.plot(PEDESTRIAN[1], PEDESTRIAN[0], marker="*", color="red", markersize=14)
    ax.set_xlabel("y, right (m)")
    ax.set_ylabel("x, forward (m)")
    ax.set_title(f"Cameras that see each ground cell (vertical FOV {vfov:.1f} deg)\n"
                 "red star: the pedestrian of question 3")
    cb = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3], shrink=0.8)
    cb.ax.set_yticklabels(["0 (blind)", "1", "2", "3 or more"])
    fig.tight_layout()
    if args.save:
        fig.savefig(args.save, dpi=110)
        print(f"wrote {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
