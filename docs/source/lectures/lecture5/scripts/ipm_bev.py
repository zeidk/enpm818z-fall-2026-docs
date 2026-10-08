#!/usr/bin/env python3
"""Inverse perspective mapping (IPM): a front camera image warped to BEV.

L5, Why Bird's-Eye View? A front camera sees lane lines that converge and
objects that shrink with distance. IPM undoes the perspective for points ON
THE GROUND: it maps every BEV cell (x, y, z=0) to the pixel that sees it,
through a 3x3 homography. Anything above the ground breaks that assumption.

The script renders a synthetic scene (three lane lines and one car) by ray
casting, warps the image to BEV, and shows it next to the true top view.

Frames (CARLA's vehicle frame, as in Exercise 2; the ROS package l5_bev_demo
uses ROS's y LEFT instead, so flip the sign of y to compare with it):
    ego:     x forward, y right, z up, origin on the ground under the car
    optical: x right, y down, z forward (what the intrinsics K assume)

Examples
--------
    python3 ipm_bev.py                       # the three panels
    python3 ipm_bev.py --pitch-error 1.0     # IPM with a 1 degree calibration error
    python3 ipm_bev.py --save ipm.png        # write the figure instead of showing it

Requires only NumPy and Matplotlib.
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np

# Camera: 640 x 480, 90 degree horizontal FOV (as in Exercise 1), mounted
# 2.0 m ahead of the ego origin, 1.6 m up, pitched down a few degrees.
IMG_W, IMG_H = 640, 480
HFOV_DEG = 90.0
CAM_X, CAM_Y, CAM_H = 2.0, 0.0, 1.6
PITCH_DEG = 5.0

# Scene, in the ego frame.
LANE_Y = (-3.5, 0.0, 3.5)       # lane line centers, meters (y right)
LANE_HALF_WIDTH = 0.075         # a 15 cm painted line
DASH, GAP = 3.0, 6.0            # the center line is dashed
# A car in the left lane (centered at y = -1.75 m): 4.5 m long, 1.8 m wide, 1.5 m tall.
CAR_MIN = np.array([18.0, -2.65, 0.0])   # minimum corner, ego frame
CAR_MAX = np.array([22.5, -0.85, 1.5])   # maximum corner

# BEV grid: 4 m to 50 m ahead, 10 m either side, 5 cm cells.
BEV_X = (4.0, 50.0)
BEV_Y = (-10.0, 10.0)
BEV_RES = 0.05


def intrinsics():
    """K for a pinhole camera with HFOV_DEG and square pixels."""
    fx = (IMG_W / 2.0) / np.tan(np.radians(HFOV_DEG) / 2.0)
    return np.array([[fx, 0.0, IMG_W / 2.0],
                     [0.0, fx, IMG_H / 2.0],
                     [0.0, 0.0, 1.0]])


def camera_axes(pitch_deg):
    """The optical axes, written in ego coordinates.

    Pitch is positive DOWN. At pitch 0 the camera looks along +x, its image
    x axis is ego +y (right) and its image y axis is ego -z (down).
    """
    p = np.radians(pitch_deg)
    right = np.array([0.0, 1.0, 0.0])
    down = np.array([-np.sin(p), 0.0, -np.cos(p)])
    forward = np.array([np.cos(p), 0.0, -np.sin(p)])
    return right, down, forward


def render(pitch_deg):
    """Ray cast the scene into a camera image (gray levels, 0 to 1).

    Ground is 0.35, paint is 0.95, the car's sides are 0.15 and its roof 0.6.
    """
    K = intrinsics()
    right, down, forward = camera_axes(pitch_deg)
    u, v = np.meshgrid(np.arange(IMG_W) + 0.5, np.arange(IMG_H) + 0.5)
    xn = (u - K[0, 2]) / K[0, 0]
    yn = (v - K[1, 2]) / K[1, 1]
    d = xn[..., None] * right + yn[..., None] * down + forward  # ray directions
    origin = np.array([CAM_X, CAM_Y, CAM_H])

    image = np.full((IMG_H, IMG_W), 0.85)      # sky
    t_hit = np.full((IMG_H, IMG_W), np.inf)

    # Ground plane z = 0
    with np.errstate(divide="ignore", invalid="ignore"):
        t_ground = np.where(d[..., 2] < 0, -origin[2] / d[..., 2], np.inf)
    ground = np.isfinite(t_ground)
    gx = np.where(ground, origin[0] + t_ground * d[..., 0], 0.0)
    gy = np.where(ground, origin[1] + t_ground * d[..., 1], 0.0)
    paint = np.zeros_like(ground)
    for lane_y in LANE_Y:
        on_line = np.abs(gy - lane_y) < LANE_HALF_WIDTH
        if lane_y == 0.0:
            on_line &= np.mod(gx, DASH + GAP) < DASH
        paint |= on_line
    image[ground] = 0.35
    image[ground & paint] = 0.95
    t_hit[ground] = t_ground[ground]

    # Car: axis-aligned box, slab method
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = (CAR_MIN - origin) / d
        t2 = (CAR_MAX - origin) / d
    t_near = np.nanmax(np.minimum(t1, t2), axis=-1)
    t_far = np.nanmin(np.maximum(t1, t2), axis=-1)
    hit = (t_near <= t_far) & (t_near > 0) & (t_near < t_hit)
    hz = origin[2] + t_near * d[..., 2]
    roof = hit & np.isclose(hz, CAR_MAX[2], atol=1e-6)
    image[hit] = 0.15
    image[roof] = 0.6
    return image


def ground_to_image_homography(pitch_deg):
    """H maps a ground point (x, y, 1) to a pixel (u, v, 1), up to scale.

    For z = 0 the optical coordinates of a ground point are linear in
    (x, y, 1): x_c = y - CAM_Y, y_c = down . (p - c), z_c = forward . (p - c).
    """
    right, down, forward = camera_axes(pitch_deg)
    c = np.array([CAM_X, CAM_Y, CAM_H])
    M = np.array([
        [right[0], right[1], -right @ c],
        [down[0], down[1], -down @ c],
        [forward[0], forward[1], -forward @ c],
    ])
    return intrinsics() @ M


def ipm(image, pitch_deg):
    """Warp the camera image onto the BEV grid, nearest pixel.

    For every BEV cell, H gives the pixel that sees that ground point. Cells
    behind the camera, or outside the image, stay NaN.
    """
    H = ground_to_image_homography(pitch_deg)
    xs = np.arange(BEV_X[0], BEV_X[1], BEV_RES) + BEV_RES / 2
    ys = np.arange(BEV_Y[0], BEV_Y[1], BEV_RES) + BEV_RES / 2
    gx, gy = np.meshgrid(xs, ys, indexing="ij")          # rows: x, cols: y
    pts = np.stack([gx, gy, np.ones_like(gx)], axis=-1) @ H.T
    with np.errstate(divide="ignore", invalid="ignore"):
        u = pts[..., 0] / pts[..., 2]
        v = pts[..., 1] / pts[..., 2]
    ok = (pts[..., 2] > 0) & (u >= 0) & (u < IMG_W) & (v >= 0) & (v < IMG_H)
    bev = np.full(gx.shape, np.nan)
    bev[ok] = image[v[ok].astype(int), u[ok].astype(int)]
    return np.flipud(bev)                                 # forward is up


def true_bev():
    """What a top-down camera would see: paint, and the car's footprint."""
    xs = np.arange(BEV_X[0], BEV_X[1], BEV_RES) + BEV_RES / 2
    ys = np.arange(BEV_Y[0], BEV_Y[1], BEV_RES) + BEV_RES / 2
    gx, gy = np.meshgrid(xs, ys, indexing="ij")
    bev = np.full(gx.shape, 0.35)
    for lane_y in LANE_Y:
        on_line = np.abs(gy - lane_y) < LANE_HALF_WIDTH
        if lane_y == 0.0:
            on_line &= np.mod(gx, DASH + GAP) < DASH
        bev[on_line] = 0.95
    car = ((gx >= CAR_MIN[0]) & (gx <= CAR_MAX[0]) &
           (gy >= CAR_MIN[1]) & (gy <= CAR_MAX[1]))
    bev[car] = 0.6
    return np.flipud(bev)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pitch-error", type=float, default=0.0,
                        help="degrees added to the pitch IPM assumes (default 0)")
    parser.add_argument("--save", help="write the figure to this file instead of showing it")
    args = parser.parse_args()

    image = render(PITCH_DEG)
    bev = ipm(image, PITCH_DEG + args.pitch_error)
    truth = true_bev()

    extent = [BEV_Y[0], BEV_Y[1], BEV_X[0], BEV_X[1]]   # y right on screen, x up
    gray = plt.get_cmap("gray").copy()
    gray.set_bad("lightsteelblue")                       # BEV cells no pixel sees
    fig, ax = plt.subplots(1, 3, figsize=(15, 5.5),
                           gridspec_kw={"width_ratios": [1.6, 1, 1]})
    ax[0].imshow(image, cmap="gray", vmin=0, vmax=1)
    ax[0].set_title(f"Front camera, pitch {PITCH_DEG:.1f} deg down")
    ax[0].set_xlabel("u (pixels)")
    ax[0].set_ylabel("v (pixels)")
    ax[1].imshow(bev, cmap=gray, vmin=0, vmax=1, extent=extent, aspect="equal")
    ax[1].set_title(f"IPM, assuming pitch {PITCH_DEG + args.pitch_error:.1f} deg\n(blue: outside the image)")
    ax[2].imshow(truth, cmap="gray", vmin=0, vmax=1, extent=extent, aspect="equal")
    ax[2].set_title("True top view")
    for a in ax[1:]:
        a.set_xlabel("y, right (m)")
        a.set_ylabel("x, forward (m)")
    fig.tight_layout()

    # Two numbers to check your answers against.
    H = ground_to_image_homography(PITCH_DEG)
    for x in (10.0, 40.0):
        p = H @ np.array([x, 0.0, 1.0])
        q = H @ np.array([x + BEV_RES, 0.0, 1.0])
        rows = abs(q[1] / q[2] - p[1] / p[2])
        print(f"x = {x:4.1f} m: one {BEV_RES * 100:.0f} cm BEV cell spans {rows:.2f} image rows")

    if args.save:
        fig.savefig(args.save, dpi=110)
        print(f"wrote {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
