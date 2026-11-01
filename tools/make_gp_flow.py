#!/usr/bin/env python3
"""Draws how the earlier group projects feed GP3 and GP4.

    /usr/bin/python3 tools/make_gp_flow.py

Writes docs/source/_static/images/GP3/gp3_flow.png and
docs/source/_static/images/GP4/gp4_flow.png (300 dpi, white background).
One color per project, the same in both figures. Solid arrows carry a ROS 2
topic; dashed arrows mean "reuses the code of".
"""
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt                      # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch   # noqa: E402

ROOT = Path(__file__).resolve().parents[1] / 'docs' / 'source' / '_static' / 'images'
COLOR = {'GP1': '#2e7d32', 'GP2': '#1565c0', 'GP3': '#6a1b9a', 'GP4': '#c62828',
         'given': '#555555'}
FILL = {'GP1': '#e8f5e9', 'GP2': '#e3f2fd', 'GP3': '#f3e5f5', 'GP4': '#ffebee',
        'given': '#f5f5f5'}


class Fig:
    def __init__(self, w, h):
        self.fig, self.ax = plt.subplots(figsize=(w, h))
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(0, h)
        self.ax.axis('off')
        self.fig.patch.set_facecolor('white')
        self.box_at = {}

    def box(self, key, x, y, w, h, title, body, who, dashed=False):
        self.ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.12',
            linewidth=2.6, edgecolor=COLOR[who], facecolor=FILL[who],
            linestyle='--' if dashed else '-'))
        self.ax.text(x + w / 2, y + h * 0.66, title, ha='center', va='center',
                     fontsize=13, fontweight='bold', color='black')
        self.ax.text(x + w / 2, y + h * 0.30, body, ha='center', va='center',
                     fontsize=11, color='#222222', linespacing=1.25)
        self.box_at[key] = (x, y, w, h)

    def side(self, key, where):
        x, y, w, h = self.box_at[key]
        return {'r': (x + w, y + h / 2), 'l': (x, y + h / 2), 't': (x + w / 2, y + h),
                'b': (x + w / 2, y), 'tr': (x + w * 0.8, y + h), 'br': (x + w * 0.8, y),
                'tl': (x + w * 0.2, y + h), 'bl': (x + w * 0.2, y),
                'rt': (x + w, y + h * 0.75), 'rb': (x + w, y + h * 0.25),
                'lt': (x, y + h * 0.75), 'lb': (x, y + h * 0.25)}[where]

    def arrow(self, a, b, label='', reuse=False, rad=0.0, label_at=0.5, dy=0.14):
        p, q = self.side(*a), self.side(*b)
        self.ax.add_patch(FancyArrowPatch(
            p, q, arrowstyle='-|>', mutation_scale=18, linewidth=2.0,
            color='#888888' if reuse else '#444444', linestyle=(0, (5, 4)) if reuse else '-',
            connectionstyle=f'arc3,rad={rad}', shrinkA=2, shrinkB=2))
        if label:
            mx = p[0] + (q[0] - p[0]) * label_at
            my = p[1] + (q[1] - p[1]) * label_at + dy
            self.ax.text(mx, my, label, ha='center', va='bottom', fontsize=10.5,
                         color='#555555' if reuse else '#333333',
                         style='italic' if reuse else 'normal',
                         bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                                   edgecolor='none'))

    def path(self, pts, label='', at=None, ha='center', va='bottom', reuse=False):
        """An arrow along straight segments through pts, the head at the end.
        The label goes at `at` (x, y)."""
        col = '#888888' if reuse else '#444444'
        ls = (0, (5, 4)) if reuse else '-'
        for a, b in zip(pts[:-2], pts[1:-1]):
            self.ax.plot([a[0], b[0]], [a[1], b[1]], color=col, linewidth=2.0, linestyle=ls,
                         solid_capstyle='butt')
        self.ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle='-|>',
                                          mutation_scale=18, linewidth=2.0, color=col,
                                          linestyle=ls, shrinkA=0, shrinkB=1))
        if label:
            self.ax.text(*at, label, ha=ha, va=va, fontsize=10.5,
                         color='#555555' if reuse else '#333333',
                         style='italic' if reuse else 'normal')

    def legend_row(self, x, y, items):
        for who, text in items:
            self.ax.add_patch(FancyBboxPatch((x, y - 0.12), 0.38, 0.24,
                                             boxstyle='round,pad=0.01,rounding_size=0.05',
                                             linewidth=2.2, edgecolor=COLOR[who],
                                             facecolor=FILL[who]))
            self.ax.text(x + 0.52, y, text, va='center', fontsize=11)
            x += 0.95 + 0.15 * len(text)

    def legend(self, x, y, items):
        for i, (who, text) in enumerate(items):
            yy = y - i * 0.42
            self.ax.add_patch(FancyBboxPatch((x, yy - 0.12), 0.38, 0.24,
                                             boxstyle='round,pad=0.01,rounding_size=0.05',
                                             linewidth=2.2, edgecolor=COLOR[who],
                                             facecolor=FILL[who]))
            self.ax.text(x + 0.55, yy, text, va='center', fontsize=11)

    def save(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.fig.savefig(path, dpi=300, facecolor='white', bbox_inches='tight',
                         pad_inches=0.15)
        plt.close(self.fig)
        print(path)


def gp3():
    f = Fig(22.2, 11.0)
    T, M = 6.4, 3.2                       # bottoms of the top and middle rows
    f.box('sm', 0.3, T, 3.6, 2.0, 'GP1 sensor_manager', 'your rig in CARLA,\nground truth, traffic\n(Task 1)', 'GP1')
    f.box('bag', 0.3, M, 3.6, 2.0, 'your drive', 'a 90 s bag (Task 1)', 'given')
    f.box('det', 5.4, T, 3.6, 2.0, 'GP2 detector_node', 'boxes in the image', 'GP2')
    f.box('out', 5.4, M, 3.6, 2.0, 'gnss_outage', 'drops the fixes in\nyour outage window', 'given')
    f.box('fus', 10.4, T, 3.6, 2.0, 'fusion_node', 'each box on the map\n(Task 3)', 'GP3')
    f.box('loc', 10.4, M, 3.6, 2.0, 'localization_node', 'EKF: your car on the map\n(Task 2)', 'GP3')
    f.box('trk', 15.4, T, 3.6, 2.0, 'tracker_node', 'ID and speed per object\n(Task 4)', 'GP3')
    f.box('gp4', 20.3, M, 1.7, 5.2, 'GP4', 'planner,\nbehavior,\ncontroller', 'GP4', dashed=True)
    f.box('proj', 10.4, 9.3, 3.6, 1.5, 'GP1 lidar_projection', 'K and the extrinsic', 'GP1')
    f.box('bt', 15.4, 9.3, 3.6, 1.5, 'GP2 box_tracker', 'Kalman filter, matching', 'GP2')
    f.path([(2.1, T), (2.1, M + 2.0)], 'records', at=(2.25, 5.75), ha='left', va='center')
    f.path([(3.9, 4.75), (4.5, 4.75), (4.5, 8.85), (11.2, 8.85), (11.2, T + 2.0)],
           'LiDAR', at=(7.2, 8.9))
    f.path([(3.9, 4.45), (4.95, 4.45), (4.95, 7.4), (5.4, 7.4)], 'camera',
           at=(5.05, 5.8), ha='left', va='center')
    f.path([(3.9, 3.85), (5.4, 3.85)], 'GNSS', at=(4.65, 3.75), va='top')
    f.path([(2.1, M), (2.1, 2.55), (12.2, 2.55), (12.2, M)], 'IMU', at=(7.2, 2.6))
    f.path([(9.0, 4.2), (10.4, 4.2)], 'fix_used', at=(9.7, 4.3))
    f.path([(9.0, 7.4), (10.4, 7.4)], 'boxes', at=(9.7, 7.5))
    f.path([(12.2, M + 2.0), (12.2, T)], 'pose', at=(12.3, 5.8), ha='left', va='center')
    f.path([(14.0, 7.4), (15.4, 7.4)], 'objects', at=(14.7, 7.5))
    f.path([(19.0, 7.4), (20.3, 7.4)], 'tracks', at=(19.65, 7.5))
    f.path([(14.0, 4.2), (20.3, 4.2)], 'pose', at=(17.2, 4.3))
    f.path([(12.9, 9.3), (12.9, T + 2.0)], 'reuses', at=(13.0, 8.85), ha='left', va='center',
           reuse=True)
    f.path([(17.2, 9.3), (17.2, T + 2.0)], 'reuses', at=(17.3, 8.85), ha='left', va='center',
           reuse=True)
    f.legend_row(3.0, 1.4, [('GP1', 'from GP1'), ('GP2', 'from GP2'), ('GP3', 'GP3: yours'),
                            ('GP4', 'next: GP4'), ('given', 'given or data')])
    f.save(ROOT / 'GP3' / 'gp3_flow.png')


def gp4():
    f = Fig(22.6, 9.6)
    T, M, B = 6.4, 3.2, 0.2
    f.box('sm', 0.3, T, 3.6, 2.0, 'GP1 sensor_manager', 'your rig in CARLA, lock step:\napplies the command (Task 1)', 'GP1')
    f.box('det', 5.4, T, 3.6, 2.0, 'GP2 detector_node', 'boxes in the image', 'GP2')
    f.box('fus', 10.4, T, 3.6, 2.0, 'GP3 fusion_node', 'objects on the map', 'GP3')
    f.box('trk', 15.4, T, 3.6, 2.0, 'GP3 tracker_node', 'ID and speed per object', 'GP3')
    f.box('loc', 5.4, M, 3.6, 2.0, 'GP3 localization_node', 'EKF pose and speed', 'GP3')
    f.box('pl', 10.4, M, 3.6, 2.0, 'planner_node', 'A* route, two triggers\n(Task 2)', 'GP4')
    f.box('bh', 15.4, M, 3.6, 2.0, 'behavior_node', 'state and target speed\n(Task 4)', 'GP4')
    f.box('gt', 20.2, M, 2.3, 2.0, 'ground truth', 'traffic light,\nspeedometer', 'given')
    f.box('ct', 10.4, B, 3.6, 2.0, 'controller_node', 'Pure Pursuit and PID\n(Task 3)', 'GP4')
    f.path([(3.9, 7.4), (5.4, 7.4)], 'camera', at=(4.65, 7.5))
    f.path([(9.0, 7.4), (10.4, 7.4)], 'boxes', at=(9.7, 7.5))
    f.path([(14.0, 7.4), (15.4, 7.4)], 'objects', at=(14.7, 7.5))
    f.path([(2.9, T + 2.0), (2.9, 8.95), (11.2, 8.95), (11.2, T + 2.0)], 'LiDAR', at=(7.0, 9.0))
    f.path([(3.9, 6.8), (4.6, 6.8), (4.6, 4.2), (5.4, 4.2)], 'IMU, GNSS',
           at=(4.7, 5.8), ha='left', va='center')
    f.path([(9.0, 4.2), (10.4, 4.2)], 'pose', at=(9.7, 4.3))
    f.path([(17.2, T), (17.2, M + 2.0)], 'tracks', at=(17.3, 5.8), ha='left', va='center')
    f.path([(15.9, T), (15.9, 5.8), (13.2, 5.8), (13.2, M + 2.0)], 'standing vehicles',
           at=(14.55, 5.85))
    f.path([(14.0, 4.2), (15.4, 4.2)], 'path', at=(14.7, 4.3))
    f.path([(20.2, 4.2), (19.0, 4.2)], 'light', at=(19.6, 4.3))
    f.path([(11.2, 8.95), (19.6, 8.95), (19.6, 4.7), (19.0, 4.7)], 'LiDAR',
           at=(19.7, 6.8), ha='left', va='center')
    f.path([(12.2, M), (12.2, B + 2.0)], 'path', at=(12.3, 2.7), ha='left', va='center')
    f.path([(17.2, M), (17.2, 1.2), (14.0, 1.2)], 'target speed', at=(15.6, 1.25))
    f.path([(7.2, M), (7.2, 1.4), (10.4, 1.4)], 'pose', at=(8.8, 1.45))
    f.path([(21.35, M), (21.35, 0.7), (14.0, 0.7)], 'speed', at=(17.6, 0.75))
    f.path([(10.4, 0.7), (0.9, 0.7), (0.9, T)], '/control/vehicle_cmd', at=(5.0, 0.75))
    f.legend_row(1.4, 2.4, [('GP1', 'GP1'), ('GP2', 'GP2'), ('GP3', 'GP3')])
    f.legend_row(1.4, 1.85, [('GP4', 'GP4: yours'), ('given', 'given')])
    f.save(ROOT / 'GP4' / 'gp4_flow.png')


if __name__ == '__main__':
    gp3()
    gp4()
