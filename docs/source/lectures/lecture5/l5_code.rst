====================================================
Code
====================================================

The L5 hands-on is four ROS 2 packages in
`enpm818z-fall-2026-carla-ros
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros>`_:
``l5_bev_demo`` for the BEV and Occupancy section, ``l5_box_demo`` for the 3D
Detection section (:ref:`below <l5-box-demo>`), ``l5_seg_demo`` for the
Segmentation section (:ref:`below <l5-seg-demo>`), and ``l5_tracking_demo`` for
the Tracking section (:ref:`below <l5-tracking-demo>`).

``l5_bev_demo`` builds
**three bird's-eye views of the same CARLA scene**, none of them learned. Each
one is the geometry of a method from the BEV and Occupancy section, so you can
see what the method does before a network is trained to do it.

.. figure:: /_static/images/L5/l5_bev_demo_all_four.png
   :alt: Four square top views of the same moment in CARLA, front up, the AV outlined in white in the middle of each. LiDAR height: rings of colored points on the road, a curb curving along the right. LiDAR occupancy: mostly white free space, with gray unknown wedges behind the buildings and the curb, widest on the right. Camera IPM: the road from above, a crosswalk and a yellow center line ahead, and the buildings on both sides smeared into long streaks pointing away from the AV. Semantic lift-splat: the road in purple, lane markings in green, sidewalks in pink on both sides, the AV's own body in dark blue, and far rows of road breaking into separate lines.
   :align: center
   :width: 100%

   One moment, four views, saved by the package's ``snapshot`` tool: grid
   50 m x 50 m, 0.2 m cells, front up (CARLA 0.9.16, Town10HD). In the IPM view
   the buildings, which are not on the ground, smear outward; in the semantic
   view the far road thins into rows, and the roof cameras see the AV's own body.

.. list-table::
   :widths: 22 26 22 30
   :header-rows: 1
   :class: compact-table

   * - **View**
     - **Topic**
     - **Built from**
     - **Slides**
   * - LiDAR height map
     - ``/l5/bev/lidar_height``
     - the bridge's LiDAR
     - PointPillars, Steps 1 to 3
   * - LiDAR occupancy grid
     - ``/l5/bev/occupancy``
     - the bridge's LiDAR
     - Occupancy; BEV and occupancy in industry
   * - Camera IPM
     - ``/l5/bev/ipm``
     - 4 roof RGB cameras
     - Before learning: IPM; IPM breaks for anything above the road
   * - Semantic lift-splat
     - ``/l5/bev/semantic``
     - 4 roof semantic and depth cameras
     - Lift-Splat-Shoot; Lift, by hand; Splat, by hand


Run it
------

The CARLA server must be running, and the L2 bridge must own the clock:

.. code-block:: bash

   cd ~/enpm818z_ws
   colcon build --symlink-install --packages-select l2_carla_demo l5_seg_demo l5_bev_demo
   source install/setup.bash

   ros2 launch l2_carla_demo demo.launch.py rviz:=false     # terminal 1
   ros2 launch l5_bev_demo bev.launch.py                    # terminal 2

   # save one moment as PNG files
   ros2 run l5_bev_demo snapshot --ros-args -p out:=bev_snapshot

RViz opens with the occupancy grid and the point cloud under the AV, the AV's
body, and the three BEV images and the front camera in their own panels. ``bev.launch.py rviz:=false`` runs
without it. ``snapshot`` writes ``lidar_height.png``, ``occupancy.png``,
``ipm.png``, ``semantic.png`` and ``all_four.png``, then exits.


The grid
--------

All four views share one grid, set in ``config/bev.yaml``: 250 x 250 cells of
0.2 m, from :math:`-25` to 25 m around the AV, in the ``ego_vehicle`` frame
(:math:`x` forward, :math:`y` left, :math:`z` up, origin on the ground under the
car). A point :math:`(x, y)` falls in cell

.. math::

   i = \left\lfloor \frac{x + 25}{0.2} \right\rfloor, \qquad
   j = \left\lfloor \frac{y + 25}{0.2} \right\rfloor

the formula from the slide "The BEV grid: from meters to a cell". The images
are drawn front up and left on the left, so image row :math:`= 249 - i` and
column :math:`= 249 - j`, and the four views line up cell for cell.


The nodes
---------

.. list-table::
   :widths: 18 82
   :header-rows: 1
   :class: compact-table

   * - **Node**
     - **What it does**
   * - ``surround_rig``
     - Attaches four cameras to the bridge's vehicle (``role_name`` ``ego``):
       front, left, right and rear, 0.3 m above the roof, tilted 30 degrees
       down, 100 degree field of view, 480 x 360, 10 Hz. At each place, an RGB,
       a semantic segmentation and a depth camera with the same pose. Publishes
       ``/l5/<camera>/rgb``, ``/l5/<camera>/semantic`` (the class tag),
       ``/l5/<camera>/depth`` (meters), ``/l5/<camera>/camera_info``, and the
       static transforms to each camera. Once, latched, it also publishes
       ``/l5/<camera>/ego_mask``: the pixels where the camera sees the AV
       itself, whose true depth puts them inside the AV's bounding box (26.8
       percent of the front image, the hood). ``l5_seg_demo``'s ``seg_eval``
       uses it to leave the AV out of the grade. It never ticks the simulator.
   * - ``lidar_bev``
     - Drops the points inside the AV's footprint (the lowest beams hit its own
       roof), then builds the **height map**, the tallest point in each cell,
       and the **occupancy grid**: per 1 degree ray, free up to the farthest
       return, occupied where a point is 0.3 to 2.5 m above the ground, unknown
       behind the nearest obstacle (Autoware's three steps).
   * - ``ipm_bev``
     - Maps each cell's ground point :math:`(x, y, 0)` into each camera with the
       mounting transform and the pinhole model, once, then warps every frame
       with ``cv2.remap``. Where cameras overlap, the one that looks most
       directly at the cell wins.
   * - ``semantic_bev``
     - Lifts every pixel to 3D at its true depth from CARLA's depth camera,
       and splats its class into the cell under it. People and vehicles win a
       cell over lane markings, and lane markings over the road.
   * - ``snapshot``
     - Saves the four views as PNG files and exits.

**Checked:** CARLA's depth is measured along the camera's optical axis, so the
lifted point is :math:`((u - c_u)d/f,\ (v - c_v)d/f,\ d)`. With that reading,
road pixels land within 0.01 m of the ground across the whole front image;
taking the depth along each pixel's ray instead puts the image edges about
0.46 m above the road.

**Speed,** measured with the bridge and all 12 rig cameras running: the server
ran slower than real time, the LiDAR arrived at 13 to 16 Hz instead of 20 and
the rig's cameras at 3 to 5 Hz instead of 10. The BEV nodes kept up with their
inputs. Lower ``image_width`` and ``image_height`` in ``config/bev.yaml`` on a
slower machine.


Tasks
-----

1. **The grid.** Car B on the slides sits at :math:`(12.0, -2.0)` m. Compute its
   cell :math:`(i, j)` on this grid by hand, then find it in ``ipm.png``.
2. **IPM.** Find a car or a building in ``ipm.png``. How long is its streak, in cells?
   Explain the length with the slide "IPM breaks for anything above the road".
   Then find a lane line: is it straight, and the right width?
3. **Lift-splat.** In ``semantic.png`` the far road breaks into separate rows.
   Explain the gaps with the slide "The camera squeezes the far road into a few
   rows". Set ``stride: 2`` in ``config/bev.yaml``: what happens near the AV,
   and far away?
4. **Occupancy.** Find a gray (unknown) wedge in ``occupancy.png``. What object
   casts it? Compare the same place in ``semantic.png``: which view tells the
   planner more, and which one is honest about what it did not see?
5. **Side by side.** Name one thing each view gets right that the other two get
   wrong.


.. _l5-box-demo:

3D Detection: ``l5_box_demo``
-----------------------------

A 3D detector reports, per object, the 7 numbers of a 3D box: center, length,
width, height and heading. ``l5_box_demo`` produces them from the L2 bridge's
LiDAR with **no learning**: it clusters the points (the same steps as
``l5_tracking_demo``'s detector), then fits a rotated box to each cluster seen
from above by **L-shape fitting**. It is the step the Frustum Association
slides mean by "real stacks fit a box to the cluster".

.. figure:: /_static/images/L5/l5_box_snapshot.png
   :alt: A top view in the AV's frame, x forward to the right from minus 30 to 30 m and y, left, up from minus 20 to 20 m, with the AV as a black triangle at the origin. Gray dots are the LiDAR points left after the ground is removed. Light blue rectangles with a dark blue outline are the fitted boxes, each with a thin line along its long side, the heading axis. Red crosses mark each cluster's centroid. Green dashed rectangles are CARLA's true vehicle boxes. Ahead and to the left, three fitted boxes sit inside their true boxes, a fourth true box holds only a small box, and a fifth, behind other cars, has no points and no box. Behind and to the right, one car is split into a thin box along its side and a short box at its end nearest the AV. A wall along y equal to 15 m gives several long thin boxes that match no vehicle, and small clusters elsewhere give thin boxes or lone centroids.
   :align: center
   :width: 100%

   One LiDAR sweep, saved by the package's ``snapshot`` tool with the evaluation
   on (CARLA 0.9.16, Town10HD, 40 vehicles on autopilot). Where the LiDAR sees
   two faces of a car, the box covers the car; a car hidden behind another has
   no box; one car splits into two clusters; walls and fences give boxes too,
   since this detector has no classes.

.. code-block:: bash

   cd ~/enpm818z_ws
   colcon build --symlink-install \
     --packages-select l2_carla_demo l5_tracking_demo l5_box_demo
   source install/setup.bash

   ros2 launch l2_carla_demo demo.launch.py rviz:=false      # terminal 1
   ros2 run l5_tracking_demo spawn_traffic                    # terminal 2: 40 vehicles
   ros2 launch l5_box_demo boxes.launch.py evaluate:=true     # terminal 3
   ros2 run l5_box_demo snapshot --ros-args -p out:=boxes.png

   # track the boxes instead of the centroids
   ros2 launch l5_tracking_demo tracking.launch.py source:=boxes

RViz shows the LiDAR, the boxes with their size and heading, the AV's body, and
the front camera in its own panel, so you can see what each box is.

**The fit.** For each direction :math:`\theta` from 0 to 89 degrees, in steps of
1 degree, the points are projected on :math:`e_1 = (\cos\theta, \sin\theta)`
and :math:`e_2 = (-\sin\theta, \cos\theta)`; the rectangle with those axes that
just holds the points has four edges. The direction scores the sum over points
of :math:`1 / \max(d, d_0)`, :math:`d` being a point's distance to its nearest
edge, and the best direction gives the box. This is the search-based fitting
with the closeness criterion of X. Zhang, W. Xu, C. Dong and J. M. Dolan,
"Efficient L-Shape Fitting for Vehicle Detection Using Laser Scanners", IEEE
Intelligent Vehicles Symposium (IV), 2017, pp. 54 to 59. The paper gives no
values for the step or :math:`d_0`; the package uses those of Autoware's
``autoware_shape_estimation``, which runs the same method: 1 degree,
:math:`d_0 = 0.1` m, and points farther than 0.4 m from every edge do not vote.
Length is the longer side, the heading runs along it, and the height is the
highest point of the cluster above the road.

**The heading is known modulo 180 degrees:** one sweep shows a rectangle, not
which end is the front. Every published heading is in :math:`[-90, 90)`
degrees.

**Car B, by hand.** ``test/test_lshape.py`` fits car B of the slides, center
:math:`(12.0, -2.0)` m, 4.5 :math:`\times` 1.9 m, heading 30 degrees, from 15
points on its rear and 26 on its left side, as on the Frustum slides. The
centroid is :math:`(10.99, -1.89)`, 1.0 m short; the fitted box is centered at
:math:`(11.93, -2.00)`, 4.41 :math:`\times` 1.91 m, heading 29 degrees.

Box results
~~~~~~~~~~~

With ``evaluate:=true`` the node grades every sweep against CARLA's true boxes
at the same simulation time (vehicles, plus the parked cars built into the map,
within 30 m of the AV), with the nuScenes definitions: a box matches a vehicle
when their centers are within 0.5, 1, 2 or 4 m on the ground, and for matches
within 2 m it measures the center error, the size error (ASE, 1 minus the IoU
of the aligned boxes) and the heading error, here modulo 180 degrees. A vehicle
is "visible" when at least 5 of the kept LiDAR points fall in its box.

Two runs of 120 s (40 vehicles, about 2,400 sweeps each, 3.1 visible vehicles
per sweep within 30 m), course laptop:

.. list-table::
   :widths: 52 24 24
   :header-rows: 1
   :class: compact-table

   * - **Measured**
     - **Run A**
     - **Run B**
   * - recall within 2 m, visible vehicles
     - 0.57
     - 0.60
   * - precision within 2 m
     - 0.13
     - 0.12
   * - center error, mean (median)
     - 0.91 m (0.75)
     - 0.94 m (0.72)
   * - **centroid error, same objects**, mean (median)
     - 1.29 m (1.19)
     - 1.44 m (1.46)
   * - size error ASE
     - 0.70
     - 0.65
   * - length error, mean
     - :math:`-1.94` m
     - :math:`-1.76` m
   * - heading error mod 180, median (mean)
     - 3.2 deg (34.3)
     - 2.6 deg (27.1)

- **The box moves the center 0.4 to 0.5 m closer** to the truth than the
  centroid, because it covers the side the LiDAR cannot see.
- **The heading is right when the fit works** (median under 3.5 degrees). The
  mean is far higher: a car seen from one face only gives a thin box whose long
  side can be the car's width, a 90 degree error.
- **The boxes are too small**, about 1.8 to 1.9 m short: a box only covers the
  points it sees. Autoware corrects this with each class's typical size.
- **Most boxes are not vehicles**: walls, fences, poles and trees also form
  clusters, and this detector has no classes, so the precision is low.

Tracking the boxes instead of the centroids, on the same runs
(``l5_tracking_demo``'s evaluator, three runs): the tracks' mean position error
went from 1.42, 1.31 and 1.64 m to 1.09, 1.02 and 1.26 m; the ID switches did
not change in a consistent way (72, 83, 78 against 75, 80, 65).

The package README has five tasks: car B by hand, the closeness score against
:math:`\theta`, the heading ambiguity, split clusters with a larger
``cell_size``, and tracking the boxes.


.. _l5-seg-demo:

Segmentation: ``l5_seg_demo``
-----------------------------

Semantic segmentation gives a class to every pixel: road, sidewalk, car, sky.
On an AV a trained network computes the classes from the camera image, every
frame; in CARLA a semantic segmentation camera writes the true class of every
pixel. ``l5_seg_demo`` does both on the L2 bridge's front camera
(1280 :math:`\times` 720) and compares them pixel by pixel.

.. figure:: /_static/images/L5/l5_seg_snapshot.png
   :alt: Four panels of one moment in CARLA, seen from the AV's front camera on a street lined with palm trees. Panel 1, the camera image: a black car close on the left in the next lane, a curving road with a double yellow center line, a sidewalk and bus shelter on the right, buildings on the left and far ahead, a pale sky. Panel 2, the network's classes: the road purple, the black car dark blue, the sidewalk pink, trees olive, buildings dark gray, the sky blue; the palm trees are thick blobs, and a building-colored patch covers part of the sky on the right. Panel 3, CARLA's true classes: the same scene with sharp outlines, the lane markings in bright green, every palm frond and lamp pole drawn, the bus shelter and small props in teal. Panel 4, where panels 2 and 3 agree: mostly green; red along the outlines of the palm trees, the poles and the car's edges, a large red patch in the sky at the top right, a red strip along the curb; light gray where the pixel is not graded, on the bus shelter, signs and props. A legend at the bottom names each class color and agree, differ and not graded.
   :align: center
   :width: 100%

   One moment, saved by the package's ``snapshot`` tool (CARLA 0.9.16,
   Town10HD). On this frame the network agrees with CARLA on 89.75 percent of
   the graded pixels, mIoU 0.392; the close car has an IoU of 0.925. It misses
   the thin objects (poles, palm fronds), calls part of the sky building, and
   paints the lane markings road: its training labels have no lane-marking
   class.

.. code-block:: bash

   python3 -m pip install --user --break-system-packages transformers   # once

   cd ~/enpm818z_ws
   colcon build --symlink-install \
     --packages-select l2_carla_demo l5_tracking_demo l5_seg_demo
   source install/setup.bash

   ros2 launch l2_carla_demo demo.launch.py rviz:=false      # terminal 1
   ros2 run l5_tracking_demo spawn_traffic                    # terminal 2: 40 vehicles
   ros2 launch l5_seg_demo seg.launch.py evaluate:=true       # terminal 3
   ros2 run l5_seg_demo snapshot --ros-args -p out:=seg.png -p skip:=20

   # also YOLOv8s-seg's instance masks, as on the reading slides
   ros2 launch l5_seg_demo seg.launch.py instances:=true

**The network.** SegFormer-B0 trained on Cityscapes (Hugging Face model
``nvidia/segformer-b0-finetuned-cityscapes-1024-1024``; E. Xie et al.,
"SegFormer: Simple and Efficient Design for Semantic Segmentation with
Transformers", NeurIPS 2021): a Transformer encoder, attention between image
patches as in L4's ViT, then a small decoder that gives 19 scores per pixel,
one per class. Its weights were set by training, on photos of German streets,
not on CARLA. The first run downloads them (15 MB) into
``~/.cache/enpm818z-weights/huggingface``. They are licensed for research or
evaluation only (NVIDIA Source Code License for SegFormer, section 3.3).

**The LiDAR, painted.** ``seg_lidar`` projects every LiDAR point into the
camera image, with the bridge's extrinsics (tf) and intrinsics (camera info),
and gives the point the network's class at that pixel. It publishes the result
on ``/l5/seg/lidar_classes``, and RViz's 3D view shows it around the AV's body.
Points the camera does not see stay gray: in a measured run, the camera saw 14
to 15 percent of each sweep. This is the projection step of the Fusion section,
and the idea of PointPainting (S. Vora, A. H. Lang, B. Helou and O. Beijbom,
"PointPainting: Sequential Fusion for 3D Object Detection", CVPR 2020), which
appends the network's class scores to each point; ``seg_lidar`` keeps only the
winning class. The LiDAR sits on the roof and the camera at the windshield, so a
point hidden from the camera behind a car still lands on the car's pixels and
turns "car".

**The answer key.** The bridge has no semantic camera, so ``seg_truth``
attaches one to the AV at the same place as the bridge's front camera, with the
same size and field of view; it logs the check (0.00 mm apart in every run).
Both cameras fire on the same tick, so their images carry the same time stamp,
and ``seg_eval`` grades only pairs from the same tick.

**The grade.** For each class :math:`c`, summed over every graded pixel of
every paired frame: TP (true positive), truth :math:`c` and network :math:`c`;
FP (false positive), network :math:`c` but truth not; FN (false negative),
truth :math:`c` but network not. Then

.. math::

   \mathrm{IoU}(c) = \frac{TP}{TP + FP + FN},

the pixels both call :math:`c` divided by the pixels either calls :math:`c`.
mIoU is the mean over the classes CARLA showed during the run.

**Two class lists.** CARLA 0.9.16's tags 1 to 19 are the 19 Cityscapes classes
in the same order and colors, so the network's class :math:`t` is CARLA's tag
:math:`t + 1`. CARLA's lane markings (tag 24) are graded as road: Cityscapes'
road includes "the markings on the road", so **this network cannot find lane
lines**. In every run it called 99.6 to 99.9 percent of CARLA's lane-marking
pixels road. CARLA's other tags (static, dynamic, other, water, ground,
bridge, rail track, guard rail, unlabeled) are not graded.

Segmentation results
~~~~~~~~~~~~~~~~~~~~

Course laptop (RTX 4060 laptop GPU), CARLA 0.9.16 on the same GPU, Town10HD,
39 or 40 vehicles, no pedestrians, three runs of about 120 s. One 1280
:math:`\times` 720 image takes 19.6 ms in float16 on an idle GPU (34.2 ms in
float32) and 29 to 34 ms in the node with CARLA rendering. The node grades 3
to 11 frames per second: most of the bridge's 3.7 MB images, sent with
best-effort delivery, never arrive (43 to 46 of 160 in an 8 s test).

.. list-table::
   :widths: 40 20 20 20
   :header-rows: 1
   :class: compact-table

   * - **IoU, summed over the run**
     - **run 1**
     - **run 2**
     - **run 3**
   * - frames graded
     - 795
     - 875
     - 504
   * - **mIoU**
     - **0.408**
     - **0.339**
     - **0.390**
   * - road (with lane markings)
     - 0.988
     - 0.962
     - 0.989
   * - building
     - 0.885
     - 0.876
     - 0.886
   * - sky
     - 0.847
     - 0.858
     - 0.847
   * - vegetation
     - 0.778
     - 0.696
     - 0.778
   * - sidewalk
     - 0.547
     - 0.600
     - 0.563
   * - car
     - 0.506
     - 0.395
     - 0.396
   * - pole
     - 0.130
     - 0.259
     - 0.128
   * - traffic light
     - 0.048
     - 0.122
     - 0.049

Runs 1 and 3 drove the same route. Big, flat classes score above 0.7. The
network finds cars (92 percent of the true car pixels in run 3) but draws them
too big, so the car IoU stays near 0.4 to 0.5. Thin objects fail: in run 3 it
called 62 percent of the pole pixels and 80 percent of the traffic-light
pixels building. The network was trained on real streets and tested on a
rendered town; this gap is why AV teams test on their own data.

``l5_bev_demo`` can splat this network's classes instead of CARLA's:
``ros2 launch l5_bev_demo bev.launch.py labels:=network``. The lane lines then
disappear from the grid seen from above.

The package README has six tasks: the class map, IoU by hand, summed against
averaged IoU, thin objects, float16, and the network's classes from above.


.. _l5-tracking-demo:

Tracking: ``l5_tracking_demo``
------------------------------

A multi-object tracker, exactly as in the Tracking section: one
constant-velocity Kalman filter per object, the gate
:math:`\varepsilon = \boldsymbol{\nu}^\top S^{-1} \boldsymbol{\nu} < 9.21`,
GNN or NN association, and the track lifecycle (tentative, confirmed after 3
detections in 5 frames, coasting, deleted after 1.0 s with no detection). It
runs live on the L2 bridge, and an evaluator grades it against CARLA's ground
truth, which a real AV never has.

**How the gate is computed.** The threshold, 9.21, is fixed: the 99 percent
value of a chi-square with 2 degrees of freedom (``gate`` in
``config/tracker.yaml``; the 99 percent is our choice). Every frame, the
tracker predicts each track (:math:`P \leftarrow F P F^\top + Q`), then computes
:math:`\varepsilon` for every track and detection pair, with
:math:`S = H P H^\top + R`, and lets a pair match only if
:math:`\varepsilon < 9.21`. It never builds the gate as a region in meters. A
coasting track gets no update, so :math:`P` and :math:`S` grow, the same miss
gives a smaller :math:`\varepsilon`, and the region where
:math:`\varepsilon < 9.21` grows. Only ``snapshot`` draws the gate, for the
picture: the dashed ellipse where :math:`\varepsilon = 9.21`. RViz draws each
track's 1-sigma position ellipse from :math:`P` alone, which grows the same way
while the track coasts.

.. figure:: /_static/images/L5/l5_tracking_snapshot.png
   :alt: A top view in the AV's frame, x forward to the right from minus 20 to 35 m and y, left, up from minus 20 to 20 m. The AV is a black box at the origin, moving at 3.0 m/s. Gray outlines are CARLA's vehicles: one just ahead in the AV's lane, one ahead and to the right, a turning car farther ahead on the right, a car behind and parked cars on the left. Green dots are confirmed tracks, each with an ID, a dashed gate ellipse and a velocity arrow: track 16 sits on the rear face of the car ahead, tracks 425 and 426 on the car ahead and to the right, track 158 on the front face of the car behind. Orange coasting tracks sit on the car ahead and to the right and just behind the turning car. A row of green confirmed tracks along y equal to minus 14 m and a few along y equal to 17 m match no CARLA vehicle. Gray tentative tracks have large gates. Blue crosses mark this frame's detections. The title reads 23 detections; tracks 6 tentative, 23 confirmed, 13 coasting.
   :align: center
   :width: 100%

   One frame of the LiDAR pipeline, saved by the package's ``snapshot`` tool
   (CARLA 0.9.16, Town10HD, 60 vehicles on autopilot). Each track sits on the
   face of its car turned toward the AV, not at its center: the LiDAR only sees
   that face. The row of tracks with no gray outline is on things that are not
   CARLA vehicles (parked cars that are part of the map, poles, trees).

.. code-block:: bash

   cd ~/enpm818z_ws
   colcon build --symlink-install --packages-select l2_carla_demo l5_tracking_demo
   source install/setup.bash

   ros2 launch l2_carla_demo demo.launch.py rviz:=false      # terminal 1
   ros2 run l5_tracking_demo spawn_traffic                    # terminal 2: 40 vehicles
   ros2 launch l5_tracking_demo tracking.launch.py            # terminal 3

   # variants
   ros2 launch l5_tracking_demo tracking.launch.py source:=boxes   # l5_box_demo's boxes
   ros2 launch l5_tracking_demo tracking.launch.py source:=truth association:=nn
   ros2 launch l5_tracking_demo tracking.launch.py source:=truth flip_prob:=0.3 \
       reset_on_class_change:=true evaluate:=true out:=eval.json
   ros2 run l5_tracking_demo snapshot --ros-args -p out:=tracking.png -p min_ego_speed:=3.0

The tracker itself, ``tracker_core.py``, has no ROS in it, and
``test/test_tracker_core.py`` runs the slides' numbers through it: car B
predicted to :math:`(12.35, -1.80)`, :math:`\varepsilon` = 400 and 0.44 for the
same 2 m, and the exercise "two tracks, three detections" (NN gives 7.0 or
2.5 depending on the order, GNN gives 2.5).

Tracker nodes
~~~~~~~~~~~~~

.. list-table::
   :widths: 18 82
   :header-rows: 1
   :class: compact-table

   * - **Node**
     - **What it does**
   * - ``detector``
     - A LiDAR detector with no learning: drops the points on the AV itself and
       the ground (keeps 0.3 to 2.5 m above the road), joins the touching
       cells of a 0.4 m grid into clusters, and gives one detection per
       cluster of 5 or more points and at most 7 m across: its centroid, in the
       fixed frame ``map``, with :math:`R = 0.5^2 I` m². The centroid falls
       short of the center (Frustum Association, Step 3).
   * - ``truth_detector``
     - CARLA's own vehicles within 40 m, with what you choose added: noise
       (0.3 m), misses (10 percent), clutter (0.5 false detections per frame)
       and wrong class labels (``flip_prob``). Use it to change one effect at a
       time.
   * - ``tracker``
     - The tracker. Publishes the confirmed and coasting tracks
       (``/l5/tracks``), every track as JSON (``/l5/tracks/json``) and RViz
       markers: gray tentative, green confirmed, orange coasting, with the
       1-sigma ellipse and a velocity arrow of 1 s of travel. RViz also shows
       the AV's body and the front camera.
   * - ``evaluate``
     - Compares detections and tracks with CARLA's vehicles within 30 m, at
       the same simulation time; a match is within 3 m. Reports the detection
       rate, recall, false tracks, ID switches, and position and speed errors.
   * - ``snapshot``
     - Saves one frame as a PNG, in the AV's frame.
   * - ``spawn_traffic``
     - Spawns vehicles on CARLA's autopilot; Ctrl+C removes them.

**Launch arguments:** ``source`` (``lidar`` or ``truth``), ``association``
(``gnn`` or ``nn``), ``nn_order`` (``ascending``: the oldest track chooses
first), ``cost`` (``epsilon``, or ``likelihood`` =
:math:`\varepsilon + \ln|S|`), ``confirmed_first`` (true),
``reset_on_class_change`` (false), ``flip_prob`` (0.0), ``evaluate`` (false),
``out`` and ``rviz``. Every other number is in ``config/tracker.yaml``.

Confirmed tracks first
~~~~~~~~~~~~~~~~~~~~~~

The slides rank pairs by :math:`\varepsilon` alone. A new track has a large
:math:`S`, so it looks close to everything, and GNN, which minimizes the
total, hands it the detection of an older track whenever that lowers the sum:
the object changes ID. Real trackers match the confirmed and coasting tracks
first, and the tentative tracks only on the detections left over (DeepSORT
calls it a matching cascade). That is ``confirmed_first``, on by default.

Tracker results
~~~~~~~~~~~~~~~

Measured on the course laptop (RTX 4060, CARLA 0.9.16, Town10HD, the bridge
at 20 Hz with its 32-channel LiDAR, 60 vehicles on autopilot), 150 s per run.
The settings compared in one table ran side by side on the **same**
detections. Vehicles within 30 m of the AV count, hidden ones included.

.. list-table::
   :widths: 34 22 22 22
   :header-rows: 1
   :class: compact-table

   * - **LiDAR detector**, 3034 sweeps
     - **GNN, confirmed first**
     - **NN, oldest first**
     - **GNN, all at once**
   * - detection rate
     - 0.56
     - 0.56
     - 0.56
   * - recall (vehicles with a track)
     - 0.60
     - 0.60
     - 0.60
   * - false tracks per frame
     - 16.7
     - 15.4
     - 18.4
   * - ID switches
     - 119
     - 161
     - 202
   * - mean position error
     - 1.33 m
     - 1.33 m
     - 1.31 m

.. list-table::
   :widths: 34 22 22 22
   :header-rows: 1
   :class: compact-table

   * - **Truth detector**, 1489 frames
     - **GNN, confirmed first**
     - **NN, oldest first**
     - **GNN, all at once**
   * - detection rate
     - 0.89
     - 0.89
     - 0.89
   * - recall
     - 0.998
     - 0.998
     - 0.998
   * - false tracks per frame
     - 0.49
     - 0.50
     - 1.19
   * - ID switches
     - 31
     - 32
     - 147

- With the LiDAR, 44 percent of the vehicles within 30 m gave no cluster
  within 3 m, mostly because something stood between them and the LiDAR. Most
  "false tracks" are real things that are not CARLA vehicles.
- With the truth detector, GNN and NN gave about the same result: in normal
  traffic, two vehicles rarely compete for one detection. Without
  ``confirmed_first``, GNN was much worse in both runs.
- **Tempe**, with ``flip_prob: 0.3`` on the truth detector: with
  ``reset_on_class_change`` off, recall 0.998, 28 ID switches and a mean speed
  error of 0.61 m/s; with it on, recall 0.357, 849 ID switches and 1.39 m/s.
  Every restart throws the velocity away: no history, no velocity, no
  predicted path.

Tracker tasks
~~~~~~~~~~~~~

1. **The exercise.** Change the epsilon table in ``test/test_tracker_core.py``
   and predict NN's and GNN's answers before you run the test.
2. **A wrong R.** Give the truth detector ``noise_sigma: 1.0`` and
   ``reported_sigma: 0.5``: the detections claim to be twice as precise as they
   are. What happens to the ID switches, and why?
3. **NN against GNN.** Script two vehicles crossing close to each other and run
   the truth source. Can you reproduce the exercise's order effect with
   ``nn_order``?
4. **Confirmed first.** Turn ``confirmed_first`` off with GNN and watch RViz:
   which tracks take the detections?
5. **Tempe.** Run ``flip_prob:=0.3`` with ``reset_on_class_change`` off and
   on, and watch the velocity arrows.

