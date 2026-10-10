====================================================
Going Further
====================================================

.. admonition:: Reading material, not covered in class
   :class: note

   This page is the written version of the deck's appendix. It is **reading
   material**: we do not present it in class, and it is **not on the quiz**.

   Each section picks up a topic from the :doc:`lecture <l5_lecture>` and
   works it out with more numbers or more steps. The sections follow the
   deck's order. Read the one you need, when you need it.

The running example is the lecture's: **car B**, a car cutting in ahead of
the AV. The detector reports its box in the AV's frame (:math:`x` forward,
:math:`y` left): center :math:`(12.0, -2.0)` m, size
:math:`4.5 \times 1.9 \times 1.5` m, heading :math:`30^\circ`, speed 4.0 m/s
along that heading. All of these values were chosen for the example.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Section**
     - **What it adds to the lecture**
   * - `Inside CenterPoint`_
     - Where CenterPoint's size, heading and center come from, and how one
       peak can carry a velocity.
   * - `One Pixel onto the Grid`_
     - How one pixel of CARLA's semantic image lands on the 0.2 m grid seen
       from above.
   * - `Lift and Splat, by Hand`_
     - One lift and one splat of Lift-Splat-Shoot, with chosen numbers.
   * - `BEVFormer`_
     - A second way to fill the BEV grid from cameras: each cell asks the
       cameras, and the last frame, for what it needs.
   * - `The Match Distance`_
     - The tracker's match distance written as the NIS of L3, and the 2 m
       example worked with it.
   * - `Tracking in Industry`_
     - What Autoware's tracker does at each step of the lecture's loop.


Inside CenterPoint
------------------

This section continues :ref:`l5-lec-centerpoint-4c` in the lecture. Step 4c
read car B's size, heading and velocity at its peak. Here is where those
numbers come from.


How Step 4c Reads the Box: the Regression Heads
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The question:** car B's size, heading and center come out at its peak.
Where from? Nothing is computed from geometry. Besides the heatmap, the
network outputs more grids with the same cells, the **regression heads**:
"a sub-voxel location refinement :math:`o`, height-above-ground
:math:`h_g`, the 3D size :math:`s`, and a yaw rotation angle
:math:`(\sin\alpha, \cos\alpha)`"; "each output uses its own head" (Yin et
al., 2021). "All outputs are dense predictions": every cell holds numbers,
empty or not.

- **Center:** the peak cell, plus :math:`o`, the fraction of a cell, plus
  :math:`h_g`, the height that the view from above had dropped.
- **Size:** three numbers, learned as logarithms "to better handle boxes of
  various shapes". So a car and a bus differ by a constant, not by a large
  factor.
- **Heading:** two numbers, :math:`\sin\alpha` and :math:`\cos\alpha`; then
  :math:`\alpha = \operatorname{atan2}(\sin\alpha, \cos\alpha)`.

**Training:** "only ground truth centers are supervised using an L1
regression loss": at each labeled center, the head is penalized by how far
its output is from the label. So only the numbers at a peak mean anything.

**Reading:** "we extract all properties by indexing into dense regression
head outputs at each object's peak location."

.. note::

   **A second stage,** left out of the lecture: it takes "one point-feature
   from the 3D center of each face of the predicted bounding box", and an
   MLP (a small network) predicts "a class-agnostic confidence score and box
   refinement".


Velocity: Two Frames In, an Offset Out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The question:** Step 4c read car B's velocity, 4.0 m/s in our example, from
one peak. How can one sweep give a speed? It cannot. So the velocity head is
"special, as it requires two input map-views the current and previous
time-step. It predicts the difference in object position between the current
and the past frame" (Yin et al., 2021).

- **Training:** like the other heads, with an L1 loss "at the ground truth
  object's location at the current time-step".
- **Tracking with it:** "we project the object centers in the current frame
  back to the previous frame by applying the negative velocity estimate and
  then matching them to the tracked objects by closest distance matching."
  Unmatched tracks are kept "up to :math:`T = 3` frames before deleting
  them", each moved by "its last known velocity estimation".

.. admonition:: In the Tracking section's words
   :class: tip

   The velocity is the prediction step; the matching is NN, one detection at
   a time, not GNN; and keeping unmatched tracks for 3 frames is coasting.
   See :ref:`l5-lec-associate` and :ref:`l5-lec-coasting` in the lecture.


One Pixel onto the Grid
-----------------------

This section continues :ref:`l5-lec-seg-road` in the lecture: how the image
from above on the right of that figure is made, for one pixel. It uses camera
images only, no LiDAR and no network: CARLA's semantic camera for the class
of each pixel, and its depth camera, at the same place, for each pixel's
distance ahead.


Step by Step: One Pixel onto the Grid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pixel is chosen for this example; the camera (:math:`1280 \times 720`,
:math:`90^\circ` field of view) and the 0.2 m grid are the capture script's.

.. figure:: /_static/images/L5/seg_lift_steps.png
   :alt: Left: the semantic image, 1280 by 720, with a dashed center line at column 640 and a purple road pixel at column 940, 300 pixels right of the center, a little below the middle row. Right: the same pixel seen from above. The camera is a black dot at the bottom; a dashed line runs straight ahead, and two dotted lines at 45 degrees on either side mark the edge of the camera's view. An arrow from the camera ends at the purple pixel, 20 m ahead and 9.375 m right. Grid lines every 2 m.
   :width: 55%
   :align: center

   **Left:** the semantic image, :math:`1280 \times 720`; the road pixel at
   :math:`u = 940` is 300 px right of the center column, 640. **Right:** the
   same pixel from above, 20 m ahead of the camera and 9.375 m right. Grid
   lines every 2 m; the dotted lines are the edge of the camera's view.

1. **Read the pixel:** its class from the semantic camera (road), its
   distance ahead from the depth camera (20 m).
2. **How far right:** the camera is 1280 px wide with a :math:`90^\circ`
   view, so the focal length in pixels is
   :math:`f = 640/\tan 45^\circ = 640`. The pixel is 300 columns right of the
   center, so

   .. math::

      (940 - 640) \times 20 / 640 = 9.375 \text{ m right}

3. **Drop the height**, because a view from above does not need it, and
   pick the 0.2 m cell: row :math:`20/0.2 = 100` ahead, 9.375 m right of the
   center.

Every pixel goes through the same three steps. If several land in one cell, a
fixed order picks the class: people win over vehicles, then buildings, lane
markings, sidewalk, road. A cell no pixel reaches stays white: the wedges
behind the cars in the lecture's figure.


Lift and Splat, by Hand
-----------------------

This section continues :ref:`l5-lec-lss` in the lecture. On the AV, the
trained network computes the features and the depth probabilities on every
frame; the values here are chosen for the example.


Lift, by Hand: One Pixel
~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** one pixel of the front camera sees car B. **The question:**
where along the pixel's ray does its feature go, when its depth is unknown?

**What we have,** from the trained network on every frame (values chosen for
this example):

- the pixel's **feature** :math:`\mathbf{c}` (L4), 2 numbers here:
  :math:`(2.0, 1.0)`;
- :math:`\alpha_d`, the probability that the pixel's surface is at depth
  :math:`d`, for 4 **depth bins** at 5, 10, 15 and 20 m.

**Lift:** put :math:`\alpha_d\,\mathbf{c}` at depth :math:`d`.

.. figure:: /_static/images/L5/lift_pixel.png
   :alt: A camera and its image at the left, with one green pixel whose feature is c = (2.0, 1.0). Its ray runs to the right, with points at depths 5, 10, 15 and 20 m. Above each point a bar shows the depth probability, set by training: 0.1, 0.6, 0.2 and 0.1, the 0.6 bar much the tallest; the probabilities add to 1.0. Below each point, the lifted feature alpha_d times c: (0.2, 0.1), (1.2, 0.6), (0.4, 0.2) and (0.2, 0.1).
   :width: 100%
   :align: center

   One pixel, feature :math:`\mathbf{c} = (2.0, 1.0)`, and its ray. The
   bars are the depth probabilities, set by training:
   :math:`\alpha_5 = 0.1`, :math:`\alpha_{10} = 0.6`,
   :math:`\alpha_{15} = 0.2`, :math:`\alpha_{20} = 0.1`. Under each depth,
   the lifted feature :math:`\alpha_d\,\mathbf{c}`.

1. The probabilities add to 1: :math:`0.1 + 0.6 + 0.2 + 0.1 = 1.0`.
2. Most of the feature goes to 10 m:
   :math:`0.6 \times (2.0, 1.0) = (1.2, 0.6)`.
3. Some goes to every other depth. The network is **not forced to pick one
   depth**. A pixel it is sure about puts almost everything in one bin; an
   unsure pixel spreads out. That is the difference from IPM, which forced
   every pixel onto the road.


Splat, by Hand: Add What Lands in a Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** one cell, ahead and to the right of the AV, is seen by two
cameras: the front and the right one. **The question:** what does that cell
hold after the lift? Each lifted point sits along its pixel's ray, at its
bin's depth, so it falls in one cell of the BEV grid
(:ref:`l5-lec-bev-grid`). **Splat:** add up every point in the same cell.

Numbers chosen for this example; on the AV the network makes them every
frame:

1. Our pixel's 10 m point lands in the cell: :math:`(1.2, 0.6)`.
2. A pixel from a second camera, whose ray crosses the same cell, adds
   :math:`(0.3, 0.3)`.
3. The cell holds :math:`(1.2 + 0.3,\ 0.6 + 0.3) =` **(1.5, 0.9)**.

.. figure:: /_static/images/L5/splat_cell.png
   :alt: A top view on a 1 m grid, x to the right and y, left, up. The AV faces right in the upper left, with a front camera (green) and a right camera (violet). One ray from each camera runs down and to the right, and the two rays cross in one highlighted green cell. Faint green points on the front camera's ray carry (0.2, 0.1), (0.4, 0.2) and (0.2, 0.1) in other cells. A zoom on the cell shows one green and one violet point, and the sum: the cell adds them, (1.2 + 0.3, 0.6 + 0.3) = (1.5, 0.9).
   :width: 55%
   :align: center

   From above, on a 1 m grid. A ray from the **front camera** (green) and
   one from the **right camera** (violet) cross in one cell. The zoom shows
   the two points in it; the cell adds them:
   :math:`(1.2 + 0.3,\ 0.6 + 0.3) = (1.5, 0.9)`. The front camera's other
   lifted points land in other cells.

.. important::

   Two cameras that see the same ground **add into the same cell**: overlap
   needs no matching step. After the splat, the BEV grid is an image seen
   from above, and the 2D networks of L4 run on it, as on PointPillars'
   pseudo-image. Then shoot: a planner reads the grid.


BEVFormer
---------

This section continues :ref:`l5-lec-lss` in the lecture with a second way to
fill the BEV grid from cameras.


BEVFormer: the Grid Asks the Cameras
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** the same six cameras, the same grid. Lift-Splat-Shoot pushes
every pixel out to the grid. **The question:** can each cell ask the cameras
for what it needs instead? **BEVFormer** (Li et al., 2022) does it: each cell
**pulls** features.

.. figure:: /_static/images/L5/bevformer.png
   :alt: A top-down grid of BEV queries around the AV, one query per cell. One highlighted query sends arrows to the image features of the two cameras that see its patch of ground: spatial cross-attention. A dashed arrow goes to the BEV grid of the previous frame: temporal self-attention.
   :width: 72%
   :align: center

   The BEV queries at time :math:`t`, one per cell, set by training. One
   query (highlighted) reads the **front** and **front-right** cameras, which
   see its patch of ground: spatial cross-attention. The dashed arrow reads
   the BEV grid at time :math:`t - 1`: temporal self-attention.

.. admonition:: Definition: BEV query
   :class: note

   One vector per cell of the BEV grid, set by training, as DETR had one
   query per object (L4).

- Each query knows where its patch of ground is, so it knows which cameras
  see that patch and where in their images. It gathers information there,
  with **attention** (L4): **spatial cross-attention**, next.
- It also attends to the BEV grid from the previous frame: **temporal
  self-attention**, after that. A car hidden in this frame may have been
  visible in the last one, and the change between frames carries speed.

The paper reports, with cameras only, **56.9 NDS** on the nuScenes test set,
"on par with the performance of LiDAR-based baselines". CenterPoint, with
LiDAR, had 65.5.


Spatial Cross-Attention, Step by Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The question:** the query of one cell, 15 m straight ahead of the AV
(chosen): where does its patch of ground appear in the camera images? It has
where the cell is, each camera's calibration from L2, and offsets and weights
that training set. With those it runs four steps, every frame.

.. figure:: /_static/images/L5/sca_pillar.png
   :alt: Left, a side view, x forward to 15 m and z from -5 to 3 m, at the same scale on both axes. The AV, drawn from the side, with its front camera on the roof, stands on the road at the left. One BEV cell lies on the road 15 m ahead; a dashed pillar over it holds 4 points, from 5 m below to 3 m above the road, and a ray runs from each point to the camera. The region under the road is shaded, below the road. Right, the front camera's image with a dashed horizon: the 4 points land in one column, the top one above the horizon; small circles around one point mark the 4 offsets, set by training, read around each point.
   :width: 90%
   :align: center

   **Left, from the side:** one BEV cell 15 m ahead, and a pillar of 4
   points over it, from 5 m below to 3 m above the road, each with a ray to
   the front camera. **Right, the front camera's image:** the 4 points land
   in one column, the top one above the horizon. The circles are the 4
   offsets, set by training, read around each point (shown for one).

1. **Raise a pillar** over the cell: **4 points**, from :math:`-5` to
   :math:`3` m (Li et al., 2022), as the cell may hold a curb or a truck
   roof.
2. **Project each point** into each camera with its calibration and the
   pinhole model (L2): :math:`u = f\,x_c/z_c + c_u`,
   :math:`v = f\,y_c / z_c + c_v`, where :math:`(x_c, y_c, z_c)` is the point
   in the camera's frame, :math:`z_c` forward, and :math:`(c_u, c_v)` is the
   image center. The same projection is used in the lecture's
   :ref:`l5-lec-frustum`, for LiDAR points.
3. **Keep the cameras** where the points land **inside the image**: the
   cameras that see this cell. For a cell ahead and to the right, that is
   the front and the front-right camera.
4. **Around each landing pixel,** read the features at **4 offsets, set by
   training** (deformable attention), and add them with weights set by
   training.

**Deformable attention** reads a few samples, not every pixel. So the
calibration decides where to look, training decides what to take, and that
is why BEVFormer is fast enough to run.


Temporal Self-Attention: Line Up the Last Frame First
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** the AV drives forward; each query also reads the last frame's
grid, centered where the AV *was*. **The question:** which old cell holds the
same ground? **What we have:** the AV's **ego-motion**, its own motion between
frames, measured by localization (L6) every frame. Shift the old grid by it.

Numbers chosen for this example: the AV drove 5.12 m straight ahead between
frames; cells are 0.512 m.

1. **Shift:** :math:`5.12 / 0.512 =` **10** cells.
2. A parked car was at row :math:`i = 133` in the last frame. Relative to the
   AV it is now 5.12 m closer: row :math:`133 - 10 =` **123**.
3. After the shift, the query at row 123 finds the car's old features **in
   its own cell**.

.. figure:: /_static/images/L5/temporal_shift.png
   :alt: Two strips of BEV cells, rows i running to the right. Top, last frame: the AV at the left and a gray parked car whose center cell, row 133, is outlined in green. Bottom, this frame, 5.12 m later: the same parked car, now at row 123. A green arrow from the top car to the bottom car reads shift: 10 cells, 5.12 m. Tick labels under the bottom strip: 100, 123 and 133.
   :width: 48%
   :align: center

   **Top, last frame:** the parked car's center cell is row 133. **Bottom,
   this frame, 5.12 m later:** the same car is at row 123. The green arrow
   is the shift, 10 cells, 5.12 m.

Without the shift, every static object would seem to move toward the AV.

.. important::

   **What the last frame adds:** objects hidden now but seen a moment ago,
   and **motion**: a cell whose content moved between frames carries a
   speed. What still moves after the shift is really moving.


The Match Distance
------------------

This section continues :ref:`l5-lec-gate` and :ref:`l5-lec-same-2m` in the
lecture. The main slides compared the miss with the track's uncertainty, in
words. Here is the formula.


The Match Distance Is the NIS of L3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The miss and the uncertainty of the lecture, in L3's terms:

.. figure:: /_static/images/L5/nis_terms.png
   :alt: A sketch of one track seen from above. A cross, the predicted position, sits in a shaded circle, labeled shaded, S: how far off the track expects a box (1 sigma). A green arrow, nu, runs from the cross to a black dot, labeled box: this frame's detection, and nu, the miss: from predicted position to box; its length is d. A dashed circle around both, about three times the radius of the shaded circle, is labeled gate: where epsilon < 9.21; a box outside cannot match.
   :width: 60%
   :align: center

   One track. The **cross** is the predicted position. The **shaded**
   circle is :math:`S`, how far off the track expects a box
   (:math:`1\sigma`). The **green** arrow :math:`\boldsymbol{\nu}` is the
   miss, from the predicted position to this frame's box; its length is
   :math:`d`. The **dashed** circle is the gate, where
   :math:`\varepsilon < 9.21`.

**The distance:** the NIS (normalized innovation squared) of L3:

.. math::

   \varepsilon = \boldsymbol{\nu}^\top S^{-1}\boldsymbol{\nu}

- :math:`\boldsymbol{\nu}` is the box minus the prediction, the green arrow.
- :math:`S` says how large the filter expects :math:`\boldsymbol{\nu}` to
  be: the predicted covariance seen through :math:`H`, plus the detector's
  noise :math:`R`.

So :math:`\varepsilon` compares the surprise with the surprise the filter
expected. The tracker computes it for every track on every frame.

**Match only if** :math:`\varepsilon < 9.21`: the chi-square value for 2
numbers, :math:`x` and :math:`y`, at 99 percent, as in L3 (99 percent is our
choice).


The 2 m Example, Worked
~~~~~~~~~~~~~~~~~~~~~~~

With the same :math:`\sigma` in :math:`x` and :math:`y` and no correlation,
:math:`S = \sigma^2 I`, so :math:`\varepsilon = d^2/\sigma^2` (:math:`\sigma`
chosen for this example):

1. **Car B's track,** :math:`\sigma = 0.1` m:
   :math:`\varepsilon = 2^2/0.1^2 =` **400**, far outside the gate.
2. **New track,** :math:`\sigma = 3` m: :math:`\varepsilon = 2^2/3^2 =`
   **0.44**, well inside.
3. **The gate's edge,** :math:`\varepsilon = 9.21`:
   :math:`d = \sqrt{9.21}\,\sigma = 3.03\,\sigma`, so 0.30 m for car B and
   9.1 m for the new track.

.. figure:: /_static/images/L5/mahalanobis.png
   :alt: Two panels. Left, Track 1: car B, followed for many frames. A blue cross in a tiny shaded circle, sigma = 0.1 m, inside a dashed gate circle of 0.30 m; a detection 2 m away is far outside, with epsilon = 2 squared over 0.1 squared = 400: far outside the gate; a 1 m scale bar. A legend: cross, predicted position; shaded, 1 sigma; dashed, the gate, epsilon below 9.21, radius root 9.21 sigma = 3.03 sigma; each panel has its own scale. Right, Track 2: new. A gray cross in a shaded circle of sigma = 3 m, a detection 2 m away inside it, and a dashed gate circle of 9.1 m around both: epsilon = 2 squared over 3 squared = 0.44: well inside the gate; a 5 m scale bar.
   :width: 95%
   :align: center

   The same 2 m on two tracks; each panel has its own scale. **Track 1, car
   B:** :math:`\sigma = 0.1` m, gate 0.30 m,
   :math:`\varepsilon = 2^2/0.1^2 = 400`, far outside. **Track 2, new:**
   :math:`\sigma = 3` m, gate 9.1 m, :math:`\varepsilon = 2^2/3^2 = 0.44`,
   well inside. The gate's radius is :math:`\sqrt{9.21}\,\sigma = 3.03\,\sigma`.


Tracking in Industry
--------------------

This section continues :ref:`l5-lec-lifecycle` in the lecture.

**The question:** does a production tracker do these steps? Autoware's
tracker, every entry from its README or source. **EKF** is the extended
Kalman filter of L3. **muSSP** is a min-cost flow solver, an assignment like
GNN's.

.. list-table::
   :widths: 18 52 30
   :header-rows: 1
   :class: compact-table

   * - **Step**
     - **Autoware, from its README and source**
     - **This lecture**
   * - **Filter**
     - "data association and EKF"; a bicycle model for vehicles, CTRV
       (constant turn rate and velocity) for pedestrians
     - one KF per object, constant velocity
   * - **Gate**
     - "area of the object from the BEV, Mahalanobis distance, and maximum
       distance, depending on the class label"
     - :math:`\varepsilon < 9.21`
   * - **Association**
     - a global optimum per frame, as min-cost flow, solved by muSSP
     - GNN
   * - **Lifecycle**
     - confirmed after 2 detections; removed after about 1.0 s with none
     - M of N; coasting

- **Filter:** the motion model is chosen per class.
- **Gate:** the Mahalanobis distance, our :math:`\varepsilon`, plus limits on
  area and distance that change with the class.
- **Association:** the whole frame is solved at once. That is the same idea
  as GNN: one global answer per frame, not track by track.
- **Lifecycle:** in the source code a track needs 2 detections to be
  confirmed, and it is removed after about 1 s without detections.

Waymo ranks 3D tracking by **MOTA**, a tracking accuracy score that counts
misses, false alarms and identity switches (Sun et al., 2020). CenterPoint's
own tracker is "greedy closest-point matching" with its predicted velocity
(Yin et al., 2021).


Sources for This Page
---------------------

The full reading list for the lecture is in :doc:`l5_references`. This page
cites:

- Yin, T., Zhou, X. and Krähenbühl, P. (2021). `Center-based 3D Object
  Detection and Tracking <https://arxiv.org/abs/2006.11275>`_. CVPR.
- Philion, J. and Fidler, S. (2020). *Lift, Splat, Shoot: Encoding Images
  from Arbitrary Camera Rigs by Implicitly Unprojecting to 3D.* ECCV.
- Li, Z. et al. (2022). *BEVFormer: Learning Bird's-Eye-View Representation
  from Multi-Camera Images via Spatiotemporal Transformers.* ECCV.
- Sun, P. et al. (2020). *Scalability in Perception for Autonomous Driving:
  Waymo Open Dataset.* CVPR.
- Autoware Foundation. `Autoware Universe: perception packages
  <https://github.com/autowarefoundation/autoware_universe/tree/main/perception>`_.
  READMEs and source at commit 9ceaccf.


.. rubric:: Image credits

The vehicle icons in the figures on this page were created by Stone from the
`Noun Project <https://thenounproject.com>`_.
