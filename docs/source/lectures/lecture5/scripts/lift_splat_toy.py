#!/usr/bin/env python3
"""Lift-Splat with a depth DISTRIBUTION per pixel, on a toy scene.

L5, Camera-to-BEV Projection: Lift-Splat-Shoot. The CARLA hands-on lifts
each pixel to ONE 3D point, using ground-truth depth. A real LSS network does
not know the depth: each pixel predicts a probability for each of D depth
bins, and lifts its feature to D points along its ray, weighted by those
probabilities. Splat then pools every point into a BEV cell.

This script does exactly that, with no network: you choose how sure the
"network" is about depth, and watch the BEV result.

    sharp    a narrow Gaussian around the true depth (sigma 0.5 m)
    blurred  a wide Gaussian (sigma 4 m)
    uniform  no depth information at all: every bin gets 1/D

The scene has three cars. Only pixels that see a car carry a feature (1.0);
ground and sky carry 0. The feature is "this pixel sees a car".

Frames: ego x forward, y right, z up (CARLA's vehicle frame, as in Exercise 2;
the ROS package l5_bev_demo uses ROS's y left, so flip the sign of y to compare).

Examples
--------
    python3 lift_splat_toy.py                         # sharp depth, sum pooling
    python3 lift_splat_toy.py --depth uniform
    python3 lift_splat_toy.py --pool max
    python3 lift_splat_toy.py --save lss.png

Requires only NumPy and Matplotlib.
"""

import argparse

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

IMG_W, IMG_H = 200, 100
HFOV_DEG = 90.0
CAM_H = 1.5                     # every camera is 1.5 m up, looking along +x

DEPTH_MIN, DEPTH_MAX, DEPTH_STEP = 2.0, 50.0, 1.0   # the bins of Exercise 3

# Cars: (x_min, x_max, y_min, y_max), 1.5 m tall, ego frame
CARS = [(10.0, 14.5, -3.9, -2.1),
        (25.0, 29.5, 3.1, 4.9),
        (40.0, 44.5, -1.9, -0.1)]
CAR_HEIGHT = 1.5

BEV_X = (0.0, 52.0)
BEV_Y = (-16.0, 16.0)
BEV_RES = 0.5


def intrinsics():
    fx = (IMG_W / 2.0) / np.tan(np.radians(HFOV_DEG) / 2.0)
    return fx, IMG_W / 2.0, IMG_H / 2.0


def render(cam_y):
    """Ray cast the cars for a camera at (0, cam_y, CAM_H), pitch 0.

    Returns the feature image (1 where a pixel sees a car) and the true depth
    of each pixel along the optical axis (inf where it sees no car).
    """
    fx, cx, cy = intrinsics()
    u, v = np.meshgrid(np.arange(IMG_W) + 0.5, np.arange(IMG_H) + 0.5)
    # Optical ray (x right, y down, z forward) in ego axes: (z, x, -y)
    d = np.stack([np.ones_like(u), (u - cx) / fx, -(v - cy) / fx], axis=-1)
    origin = np.array([0.0, cam_y, CAM_H])
    depth = np.full((IMG_H, IMG_W), np.inf)
    for x0, x1, y0, y1 in CARS:
        lo = np.array([x0, y0, 0.0])
        hi = np.array([x1, y1, CAR_HEIGHT])
        with np.errstate(divide="ignore", invalid="ignore"):
            t1 = (lo - origin) / d
            t2 = (hi - origin) / d
        t_near = np.nanmax(np.minimum(t1, t2), axis=-1)
        t_far = np.nanmin(np.maximum(t1, t2), axis=-1)
        hit = (t_near <= t_far) & (t_near > 0)
        depth = np.where(hit & (t_near < depth), t_near, depth)  # d[...,0] = 1, so t is depth
    feature = np.isfinite(depth).astype(float)
    return feature, depth


def depth_distribution(true_depth, mode):
    """Probability of each depth bin, for every pixel: shape (H, W, D)."""
    centers = np.arange(DEPTH_MIN, DEPTH_MAX, DEPTH_STEP) + DEPTH_STEP / 2
    if mode == "uniform":
        probs = np.ones(true_depth.shape + centers.shape)
    else:
        sigma = 0.5 if mode == "sharp" else 4.0
        z = np.where(np.isfinite(true_depth), true_depth, 0.0)[..., None]
        probs = np.exp(-0.5 * ((centers - z) / sigma) ** 2)
    probs /= probs.sum(axis=-1, keepdims=True)
    return centers, probs


def lift(feature, probs, centers, cam_y):
    """Every pixel becomes D points along its ray: positions and weights."""
    fx, cx, cy = intrinsics()
    u, v = np.meshgrid(np.arange(IMG_W) + 0.5, np.arange(IMG_H) + 0.5)
    xn = ((u - cx) / fx)[..., None]
    yn = ((v - cy) / fx)[..., None]
    x = np.broadcast_to(centers, probs.shape)        # depth along +x
    y = cam_y + x * xn
    z = CAM_H - x * yn
    weight = feature[..., None] * probs              # the "outer product" of LSS
    return x.ravel(), y.ravel(), z.ravel(), weight.ravel()


def splat(x, y, weight, pool):
    """Pool lifted points into the BEV grid (rows: x forward, cols: y right)."""
    rows = int((BEV_X[1] - BEV_X[0]) / BEV_RES)
    cols = int((BEV_Y[1] - BEV_Y[0]) / BEV_RES)
    r = ((x - BEV_X[0]) / BEV_RES).astype(int)
    c = ((y - BEV_Y[0]) / BEV_RES).astype(int)
    ok = (r >= 0) & (r < rows) & (c >= 0) & (c < cols) & (weight > 0)
    grid = np.zeros((rows, cols))
    if pool == "sum":
        np.add.at(grid, (r[ok], c[ok]), weight[ok])
    else:
        np.maximum.at(grid, (r[ok], c[ok]), weight[ok])
    return grid, ok


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--depth", choices=["sharp", "blurred", "uniform"], default="sharp")
    parser.add_argument("--pool", choices=["sum", "max"], default="sum")
    parser.add_argument("--save", help="write the figure to this file instead of showing it")
    args = parser.parse_args()

    feature, depth = render(0.0)
    centers, probs = depth_distribution(depth, args.depth)
    x, y, z, w = lift(feature, probs, centers, 0.0)
    grid, ok = splat(x, y, w, args.pool)

    D = len(centers)
    print(f"D = {D} depth bins, {IMG_H} x {IMG_W} pixels: {IMG_H * IMG_W * D} lifted points")
    print(f"car pixels (feature mass): {w.sum():.1f}; "
          f"mass inside the BEV grid: {w[ok].sum():.1f}; grid.sum(): {grid.sum():.1f}")

    fig, ax = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={"width_ratios": [1.2, 1]})
    ax[0].imshow(feature, cmap="gray_r", vmin=0, vmax=1)
    ax[0].set_title("Front camera: pixels with a car feature (black)")
    ax[0].set_xlabel("u (pixels)")
    ax[0].set_ylabel("v (pixels)")
    extent = [BEV_Y[0], BEV_Y[1], BEV_X[0], BEV_X[1]]
    im = ax[1].imshow(np.flipud(grid), cmap="viridis", extent=extent, aspect="equal")
    for x0, x1, y0, y1 in CARS:
        ax[1].add_patch(patches.Rectangle((y0, x0), y1 - y0, x1 - x0, fill=False,
                                          edgecolor="red", linewidth=1.2))
    ax[1].plot(0.0, 0.3, marker="^", color="white", markersize=8)   # the camera
    ax[1].set_title(f"BEV, depth {args.depth}, {args.pool} pooling\n(red: true car footprints)")
    ax[1].set_xlabel("y, right (m)")
    ax[1].set_ylabel("x, forward (m)")
    fig.colorbar(im, ax=ax[1], shrink=0.8, label="pooled feature")
    fig.tight_layout()
    if args.save:
        fig.savefig(args.save, dpi=110)
        print(f"wrote {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
