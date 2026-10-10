====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Seven take-home exercises built on the Lecture 5 slides shown in class, and
on the same running example: **car B**, a car cutting in ahead of the AV.
Exercises 1 to 6 are paper and arithmetic: reading a 3D box and counting
LiDAR rings, the road from the image to the grid, IPM and occupancy,
frustum association, one tracker cycle, and data association with NN and
GNN. Exercise 7 runs the four ROS packages of :doc:`l5_code` in CARLA.

.. note::

   Exercises 1 to 6 can be done with a calculator, but you will learn more by
   writing ten lines of NumPy and checking your arithmetic against it. They
   need no CARLA.

   **Frames.** Every position on this page is in the AV's frame, as in the
   lecture: :math:`x` forward, :math:`y` **left**, :math:`z` up, in meters. A
   point to the right of the AV has a negative :math:`y`. CARLA's own
   vehicle frame has :math:`y` pointing right; flip the sign of :math:`y` to
   compare.

   **Car B** (values chosen for the lecture): center :math:`(12.0, -2.0)` m,
   size :math:`4.5 \times 1.9 \times 1.5` m, heading :math:`30^\circ`, speed
   4.0 m/s along its heading. The AV's lane is 3.5 m wide, centered on
   :math:`y = 0`. Numbers that are not the lecture's are marked "chosen for
   this exercise".


.. dropdown:: Exercise 1. Reading a 3D Box, and the Rings That Find It
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Turn a 3D box into the corner that matters to the planner, and count how
   many LiDAR rings and camera rows land on car B, near and far.

   .. raw:: html

      <hr>

   **Part A. The corners**

   From the center :math:`C`, the forward direction is
   :math:`(\cos\theta, \sin\theta)` and the left direction is
   :math:`(-\sin\theta, \cos\theta)`. A corner is :math:`C`, plus or minus
   half the length along the forward direction, plus or minus half the width
   along the left direction.

   1. Compute car B's front-left corner. How far into the AV's lane does it
      reach?
   2. Compute the other three corners: front-right, rear-left and
      rear-right. Which corner is nearest the AV, whose base link is at the
      origin?
   3. Suppose car B pointed straight ahead (:math:`\theta = 0`), with the
      same center and size. How far into the AV's lane would its left side
      reach?
   4. Now turn it to :math:`\theta = 45^\circ` (chosen for this exercise).
      Where is the front-left corner, and how far into the AV's lane does it
      reach? Has it crossed the AV's centerline?

   .. raw:: html

      <hr>

   **Part B. Rings and rows**

   The lecture's LiDAR has 64 channels (chosen) spread evenly from
   :math:`+10^\circ` to :math:`-30^\circ` (CARLA's defaults). Car B is 1.5 m
   tall.

   5. Compute the angle between neighboring channels, the gap between
      neighboring rings on car B's back at 12 m and at 50 m, and the number
      of ring lines at each distance.
   6. Repeat at 25 m (chosen for this exercise).
   7. CARLA's default LiDAR has 32 channels over the same :math:`40^\circ`.
      Repeat question 5 with 32 channels. The lecture says 32 channels would
      halve every count: check it.
   8. The camera is 1280 px wide with a :math:`90^\circ` field of view, so
      :math:`f = 640` px. How many rows of pixels does car B cover at 12 m,
      25 m and 50 m?

   .. raw:: html

      <hr>

   **Part C. The heading**

   9. CenterPoint reads the heading as :math:`(\sin\theta, \cos\theta)`.
      Compute both pairs for :math:`359^\circ` and :math:`1^\circ`, and the
      difference of the angles themselves. Why does the pair make a better
      training target?

   .. raw:: html

      <hr>

   **Deliverable**

   The four corners with the arithmetic, the three "how far into the lane"
   answers, a table of rings and rows against distance, and two sentences on
   what the table says about fusion.

   .. dropdown:: Guidance
      :color: success

      Question 1, from the lecture: half the length is 2.25 m and half the
      width 0.95 m. Front center:
      :math:`(12.0 + 2.25 \cos 30^\circ,\ -2.0 + 2.25 \sin 30^\circ) = (13.95, -0.875)`.
      Front-left: :math:`(13.95 - 0.95 \sin 30^\circ,\ -0.875 + 0.95 \cos 30^\circ) = (13.47, -0.05)`.
      The corner is 5 cm right of the centerline, so it reaches
      :math:`1.75 - 0.05 =` **1.70 m** into the AV's lane, 13.5 m ahead.

      Question 2: with :math:`\cos 30^\circ = 0.866` and
      :math:`\sin 30^\circ = 0.5`:

      .. list-table::
         :widths: 30 35 35
         :header-rows: 1
         :class: compact-table

         * - **Corner**
           - **Position (m)**
           - **Distance from the AV (m)**
         * - front-left
           - (13.47, -0.05)
           - 13.47
         * - front-right
           - (14.42, -1.70)
           - 14.52
         * - rear-left
           - (9.58, -2.30)
           - **9.85**
         * - rear-right
           - (10.53, -3.95)
           - 11.24

      The rear-left corner is nearest. The rear face and the left side are
      the two faces turned toward the AV: the faces the LiDAR hits in the
      lecture's frustum example.

      Question 3: the left side would be at
      :math:`y = -2.0 + 0.95 = -1.05` m, so it would reach
      :math:`1.75 - 1.05 =` **0.70 m** into the lane. The heading adds a
      full meter.

      Question 4: :math:`\cos 45^\circ = \sin 45^\circ = 0.707`. Front
      center: :math:`(12.0 + 1.59,\ -2.0 + 1.59) = (13.59, -0.41)`.
      Front-left: :math:`(13.59 - 0.67,\ -0.41 + 0.67) = (12.92, 0.26)`.
      The corner is 0.26 m **left** of the centerline: it has crossed it, and
      reaches :math:`1.75 + 0.26 =` **2.01 m** into the AV's lane.

      Question 5, from the lecture: :math:`40^\circ/(64 - 1) = 0.635^\circ`,
      and :math:`\tan 0.635^\circ = 0.01108`. At 12 m the gap is
      :math:`12 \times 0.01108 = 0.133` m and
      :math:`1.5/0.133 = 11.3`: **11 or 12** lines. At 50 m the gap is
      0.554 m and :math:`1.5/0.554 = 2.7`: **2 or 3** lines. A count of lines
      cannot be a fraction; which of the two depends on where the first line
      lands.

      Question 6: :math:`25 \times 0.01108 = 0.277` m and
      :math:`1.5/0.277 = 5.4`: 5 or 6 lines.

      Question 7: :math:`40^\circ/(32 - 1) = 1.290^\circ`, and
      :math:`\tan 1.290^\circ = 0.02252`. At 12 m the gap is 0.270 m and
      :math:`1.5/0.270 = 5.5`: 5 or 6 lines. At 50 m the gap is 1.126 m and
      :math:`1.5/1.126 = 1.3`: 1 or 2 lines. (At 25 m, for the table below:
      0.563 m and :math:`1.5/0.563 = 2.7`, 2 or 3 lines.) The counts drop from 11.3 to
      5.5 and from 2.7 to 1.3: about half, because 31 gaps are about half of
      63.

      Question 8: :math:`640 \times 1.5/d`: **80** rows at 12 m, **38.4** at
      25 m, **19.2** at 50 m (the lecture rounds it to 19).

      .. list-table::
         :widths: 25 25 25 25
         :header-rows: 1
         :class: compact-table

         * - **Distance**
           - **64 channels**
           - **32 channels**
           - **Camera rows**
         * - 12 m
           - 11 or 12
           - 5 or 6
           - 80
         * - 25 m
           - 5 or 6
           - 2 or 3
           - 38.4
         * - 50 m
           - 2 or 3
           - 1 or 2
           - 19.2

      Question 9: :math:`359^\circ` gives
      :math:`(\sin, \cos) = (-0.0175, 0.9998)` and :math:`1^\circ` gives
      :math:`(0.0175, 0.9998)`: almost the same pair. As angles, the two
      differ by :math:`358^\circ`. A network trained on the angle would be
      punished for answering :math:`359^\circ` when the label is
      :math:`1^\circ`, although the two headings are only :math:`2^\circ`
      apart.

      For the sentences: the LiDAR measures distance well and sees little
      far away; the camera sees detail and guesses distance. That is why the
      AV fuses them.


.. dropdown:: Exercise 2. From the Image to the Grid
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See with numbers why the road is segmented and mapped from above, and put
   points on the lecture's BEV grids.

   .. raw:: html

      <hr>

   **Part A. A class for every pixel**

   1. The front camera is :math:`1280 \times 720` pixels. How many class
      numbers does semantic segmentation hand the planner per frame?
   2. Two pedestrians stand side by side. What does semantic segmentation
      say about them, and which kind of segmentation tells them apart?

   .. raw:: html

      <hr>

   **Part B. The far road in the image**

   The front camera has :math:`f = 640` px and sits :math:`h = 1.5` m above a
   flat road (chosen), looking level. A road point :math:`d` meters ahead
   lands :math:`v = f h / d` rows below the horizon.

   3. How many image rows does one meter of road get from 10 to 11 m, from
      20 to 21 m (chosen for this exercise) and from 50 to 51 m?
   4. In the lecture's CARLA frame, a lane marking was measured 9 pixels
      wide at 10 m. Its width in pixels shrinks as :math:`1/d`. Predict its
      width at 20 m, and compare with the 4 pixels measured there. Predict it
      at 40 m (chosen for this exercise).
   5. On a BEV grid of 0.5 m cells, how many cells does one meter of road
      get at 10 m and at 50 m?

   .. raw:: html

      <hr>

   **Part C. Meters to a cell**

   BEVFormer's grid: :math:`200 \times 200` cells over :math:`-51.2` to
   :math:`51.2` m in :math:`x` and :math:`y`. :math:`i` counts cells along
   :math:`x` (forward), :math:`j` along :math:`y` (left), and
   :math:`\lfloor\cdot\rfloor` rounds down.

   6. Compute the cell size, and the cell of car B's center.
   7. Compute the cells of a pedestrian at :math:`(30.0, 5.0)` m and of a
      parked car behind the AV at :math:`(-10.0, 3.5)` m (both chosen for
      this exercise). Which cell is the AV's own?
   8. The ROS package ``l5_bev_demo`` uses another grid (see
      :doc:`l5_code`): :math:`250 \times 250` cells of 0.2 m, from
      :math:`-25` to 25 m, with :math:`i = \lfloor (x + 25)/0.2 \rfloor`.
      Compute car B's cell on it. How many cells does each grid have, and
      what does each one cover?

   .. raw:: html

      <hr>

   **Deliverable**

   The counts for questions 1, 3 and 5, the two width predictions, and the
   cells of questions 6 to 8.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`1280 \times 720 =` **921,600** class numbers, one
      per pixel.

      Question 2: both get the class "person": semantic segmentation does
      not tell them apart. Instance segmentation gives each one its own
      mask; panoptic segmentation gives every pixel a class and an object id
      on things like people and cars.

      Question 3:

      - 10 to 11 m: :math:`96.0 - 87.3 =` **8.7** rows (the lecture).
      - 20 to 21 m: :math:`640 \times 1.5/20 - 640 \times 1.5/21 = 48.0 - 45.7 =`
        **2.3** rows.
      - 50 to 51 m: :math:`19.20 - 18.82 =` **0.38** rows (the lecture),
        less than one row: about 23 times fewer than at 10 m.

      Question 4: :math:`9 \times 10/20 = 4.5` pixels at 20 m, close to the 4
      measured (a width in whole pixels cannot be 4.5). At 40 m:
      :math:`9 \times 10/40 = 2.25` pixels.

      Question 5: 2 cells at both distances. On the grid, every cell has the
      same size in meters, so distances on the grid are distances on the
      road.

      Question 6, from the lecture: :math:`102.4/200 = 0.512` m. Car B:
      :math:`i = \lfloor 63.2/0.512 \rfloor = \lfloor 123.4 \rfloor = 123`,
      :math:`j = \lfloor 49.2/0.512 \rfloor = \lfloor 96.1 \rfloor = 96`.

      Question 7: pedestrian,
      :math:`i = \lfloor 81.2/0.512 \rfloor = \lfloor 158.6 \rfloor = 158`,
      :math:`j = \lfloor 56.2/0.512 \rfloor = \lfloor 109.8 \rfloor = 109`.
      Parked car, :math:`i = \lfloor 41.2/0.512 \rfloor = \lfloor 80.5 \rfloor = 80`,
      :math:`j = \lfloor 54.7/0.512 \rfloor = \lfloor 106.8 \rfloor = 106`. The
      AV at :math:`(0, 0)`:
      :math:`\lfloor 51.2/0.512 \rfloor = 100`, cell (100, 100).

      Question 8: :math:`i = \lfloor 37.0/0.2 \rfloor = 185` and
      :math:`j = \lfloor 23.0/0.2 \rfloor = 115`. Car B's center sits exactly
      on a cell corner on this grid, so a center a hair smaller in :math:`x`
      or :math:`y` would land one cell lower. BEVFormer's grid has
      :math:`200 \times 200 = 40{,}000` cells over
      :math:`102.4 \times 102.4` m; ``l5_bev_demo``'s has
      :math:`250 \times 250 = 62{,}500` cells over :math:`50 \times 50` m:
      more cells, a smaller area, finer cells.


.. dropdown:: Exercise 3. IPM and Occupancy
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Work out where IPM puts each part of a car, and size an occupancy grid.

   .. raw:: html

      <hr>

   **Part A. IPM, point by point**

   IPM assumes every pixel lies on the road and computes
   :math:`d = f h / v`. Same camera: :math:`f = 640` px,
   :math:`h = 1.5` m, looking level. A car 1.5 m tall has its back 10 m ahead
   (chosen). A point :math:`z` meters up is :math:`h - z` below the camera, so
   it lands :math:`v = f (h - z)/d` rows below the horizon.

   1. A pixel lands 96 rows below the horizon. Where does IPM put it?
   2. Compute :math:`v` and IPM's distance for points on the back of the car
      at :math:`z = 0` (the bottom), 0.5 m, 0.75 m, 1.0 m and 1.4 m (0.5, 1.0
      and 1.4 m chosen for this exercise), and at the roof top, 1.5 m.
   3. Show that for a point :math:`z` up on a surface :math:`d` ahead, IPM's
      distance is :math:`d \, h/(h - z)`. What does that formula say about a
      lane marking?
   4. In ``l5_bev_demo``'s IPM view, the buildings smear into long streaks
      pointing away from the AV. Explain why with question 3.

   .. raw:: html

      <hr>

   **Part B. Occupancy**

   5. The Occ3D-nuScenes benchmark uses 0.4 m voxels over :math:`-40` to
      :math:`40` m in :math:`x` and :math:`y`, and :math:`-1` to 5.4 m in
      :math:`z`. How many voxels is that per frame?
   6. Halve the voxel to 0.2 m (chosen for this exercise). How many voxels
      now, and by what factor did the count grow?
   7. Each voxel is free, occupied or unobserved. A truck stands to the
      right of the AV, and the space behind it is hidden from every sensor.
      Which label does that space get, and why must the planner not treat
      it as free?
   8. A fallen branch lies in the lane, and no detector was trained on
      branches. What does a 3D detector report, and what does occupancy
      report?

   .. raw:: html

      <hr>

   **Deliverable**

   A table of :math:`z`, :math:`v` and IPM's distance for question 2, the
   formula of question 3, the voxel counts, and a sentence each for
   questions 4, 7 and 8.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`d = 640 \times 1.5/96 =` **10.0** m (the lecture).

      Question 2:

      .. list-table::
         :widths: 30 30 40
         :header-rows: 1
         :class: compact-table

         * - :math:`z` **(m)**
           - :math:`v = 640 (1.5 - z)/10`
           - **IPM's distance** :math:`640 \times 1.5 / v`
         * - 0 (bottom)
           - 96
           - 10 m: right
         * - 0.5
           - 64
           - 15 m
         * - 0.75
           - 48
           - **20 m**: twice too far (the lecture)
         * - 1.0
           - 32
           - 30 m
         * - 1.4
           - 6.4
           - 150 m
         * - 1.5 (roof top)
           - 0
           - infinite

      Question 3: substitute :math:`v = f (h - z)/d` into :math:`f h / v`:
      :math:`f h \cdot d / (f (h - z)) = d \, h / (h - z)`. For a lane
      marking, :math:`z = 0`, so IPM's distance is :math:`d`: exact. The
      higher the point, the smaller :math:`h - z`, and the farther IPM puts
      it; at the camera's height it never meets the ground.

      Question 4: a building's wall rises from the road. Its foot is placed
      right, and every point above the foot is placed farther and farther
      away, so the wall becomes a streak pointing away from the camera, as
      the car does in the lecture's figure.

      Question 5, from the lecture: :math:`80/0.4 = 200` cells each way and
      :math:`6.4/0.4 = 16` layers: :math:`200 \times 200 \times 16 =`
      **640,000** voxels every frame.

      Question 6: :math:`400 \times 400 \times 32 = 5{,}120{,}000` voxels,
      8 times as many: halving the voxel doubles the count along each of the
      three axes.

      Question 7: **unobserved**: no sensor saw it. It may hold a pedestrian
      about to step out. Autoware's intersection module looks for such
      unknown cells and slows the AV before it can see.

      Question 8: the detector finds only the classes it was trained on, so
      it reports no box, and to the planner the branch does not exist. Occupancy
      marks the branch's voxels occupied: the branch has no class, but it
      occupies voxels (Occ3D labels such things "general objects").


.. dropdown:: Exercise 4. Frustum Association, and Fusion Beyond the AV
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Project LiDAR points into a camera box by hand, see why the box alone is
   not enough, find car B's position, and place a pedestrian that another
   vehicle sees.

   .. raw:: html

      <hr>

   **Part A. Projecting into the image**

   The camera's mount (chosen in the lecture): at :math:`(1.6, 0, 1.5)` m on
   the AV, looking straight ahead and level. Its frame: :math:`x_c` right,
   :math:`y_c` down, :math:`z_c` forward. Its image: :math:`1280 \times 720`,
   :math:`f = 640` px, center :math:`(c_u, c_v) = (640, 360)`. The pinhole
   model (L2): :math:`u = f x_c / z_c + c_u` and :math:`v = f y_c / z_c + c_v`.
   The camera detector's box on car B runs :math:`u` from 640 to 925 and
   :math:`v` from 355 to 485 (values chosen in the lecture).

   1. Project the lecture's point, the middle of car B's rear face at
      :math:`(10.05, -3.125)`, 1.0 m up. Is it inside the box?
   2. Project car B's front-left corner and rear-right corner (Exercise 1),
      both 1.0 m up. Where do they land? Compare their :math:`u` with the
      box's left and right edges.
   3. Project a point at the top of car B, 1.5 m up, anywhere on the car,
      and the bottom of car B's rear-left corner, on the road. Compare with
      the box's top and bottom edges.

   .. raw:: html

      <hr>

   **Part B. The box picks too much**

   4. A wall stands behind car B. Project two wall points, 1.0 m up, at
      :math:`(25, -10)` and :math:`(25, -11)` (chosen for this exercise).
      Which one passes the inside-the-box test?
   5. The lecture's sweep has 50 points in the box (count chosen): 41 on
      car B, 9 to 14 m ahead, and 9 on the wall, 20 to 30 m ahead. Which
      step separates them, and which cluster do you keep?

   .. raw:: html

      <hr>

   **Part C. One position for car B**

   6. Car B's 41 points: 15 along its rear face, middle
      :math:`(10.05, -3.125)`, and 26 along its left side, middle
      :math:`(11.53, -1.18)` (counts chosen, points spread evenly). Compute
      the centroid and its distance from the box center.
   7. ``l5_box_demo``'s test fits a box to the same 41 points by L-shape
      fitting (see :doc:`l5_code`). Its result is given there: center
      :math:`(11.93, -2.00)` m, :math:`4.41 \times 1.91` m, heading
      :math:`29^\circ`. How much closer to the true center is it than the
      centroid, and why?

   .. raw:: html

      <hr>

   **Part D. Where the sensors meet**

   8. Place each of Autoware's packages in early, intermediate or late
      fusion: ``pointpainting`` (the camera detector's class scores appended
      to each LiDAR point, then CenterPoint), ``bevfusion`` (camera and LiDAR
      features on one BEV grid) and ``roi_cluster_fusion`` (LiDAR clusters
      projected onto the image; a cluster that overlaps a camera box takes
      its label). How is ``roi_cluster_fusion`` related to Parts A to C?

   .. raw:: html

      <hr>

   **Part E. A pedestrian the AV cannot see**

   In the map frame (:math:`x` along the road, :math:`y` left; positions
   chosen in the lecture), connected car C at :math:`(100, 0)`, facing
   :math:`+x`, sends "pedestrian 15 m ahead, 3 m left of me". The AV is at
   :math:`(70, 0)`.

   9. Where is the pedestrian in the map frame, and seen from the AV?
   10. Suppose C's localization is wrong and C believes it is at
       :math:`(101, 0)` (chosen for this exercise). Where does the AV now
       place the pedestrian? What must every V2X message carry, so the AV
       can judge it?

   .. raw:: html

      <hr>

   **Deliverable**

   The projections with their arithmetic, the inside or outside verdict for
   each point, the centroid, the three placements of question 8, and the
   pedestrian's position in both cases of Part E.

   .. dropdown:: Guidance
      :color: success

      Question 1, from the lecture: :math:`z_c = 10.05 - 1.6 = 8.45` m,
      :math:`x_c = 3.125` m (right is :math:`-y`),
      :math:`y_c = 1.5 - 1.0 = 0.5` m. Then
      :math:`u = 640 \times 3.125/8.45 + 640 = 876.7` and
      :math:`v = 640 \times 0.5/8.45 + 360 = 397.9`.
      :math:`640 \le 876.7 \le 925` and :math:`355 \le 397.9 \le 485`:
      **inside**.

      Question 2: front-left :math:`(13.47, -0.05)`: :math:`z_c = 11.87`,
      :math:`x_c = 0.05`, so :math:`u = 642.8` and :math:`v = 387.0`.
      Rear-right :math:`(10.53, -3.95)`: :math:`z_c = 8.93`,
      :math:`x_c = 3.95`, so :math:`u = 923.1` and :math:`v = 395.9`. These
      are car B's leftmost and rightmost points in the image, and they sit
      just inside the box's edges, 640 and 925: the box is the outline of car
      B as the camera sees it.

      Question 3: a point 1.5 m up is level with the lens, so
      :math:`y_c = 0` and :math:`v = 360`, wherever it is on the car: just
      below the box's top edge, 355. The bottom of the rear-left corner,
      :math:`(9.58, -2.30)` on the road, is the nearest point of car B:
      :math:`z_c = 7.98`, :math:`y_c = 1.5`, so
      :math:`v = 640 \times 1.5/7.98 + 360 = 480.4`, just above the bottom
      edge, 485.

      Question 4: :math:`(25, -10)`: :math:`z_c = 23.4`, :math:`x_c = 10`, so
      :math:`u = 913.5`, :math:`v = 373.7`: **inside**.
      :math:`(25, -11)`: :math:`u = 940.9`: outside. The box is flat, but the
      space it sees is a wedge, the frustum, and it includes points far behind
      car B.

      Question 5: clustering. DBSCAN groups points that have enough neighbors
      within a set distance (both settings chosen by the engineer). Keep the
      big, near cluster: car B's 41 points.

      Question 6, from the lecture:
      :math:`x = (15 \times 10.05 + 26 \times 11.53)/41 = 10.99` and
      :math:`y = (15 \times (-3.125) + 26 \times (-1.18))/41 = -1.89`. Its
      distance from :math:`(12.0, -2.0)` is
      :math:`\sqrt{1.01^2 + 0.11^2} = 1.0` m: the LiDAR sees only the two
      faces turned toward the AV, so the average sits toward the AV.

      Question 7: the fitted center is :math:`\sqrt{0.07^2 + 0^2} = 0.07` m
      from the true center, against 1.0 m for the centroid. The box covers
      the sides the LiDAR cannot see: it fits a rectangle to the two visible
      faces, and the rectangle's center is behind them. That is what the
      lecture means by "real stacks fit a box to the cluster".

      Question 8: ``pointpainting`` is **early** (each raw point takes on
      class scores). ``bevfusion`` is **intermediate** (features on one
      grid). ``roi_cluster_fusion`` is **late** (finished clusters and
      finished camera boxes), and it is frustum association turned around:
      cluster the LiDAR points first, then project each cluster into the
      image, and match it to a camera box with IoU (L4).

      Question 9, from the lecture: :math:`(100 + 15,\ 0 + 3) = (115, 3)` in
      the map frame, so :math:`115 - 70 =` **45** m ahead of the AV and 3 m
      left.

      Question 10: :math:`(101 + 15,\ 3) = (116, 3)`, so 46 m ahead: C's
      1 m error moves the pedestrian 1 m. The two errors add, the way
      variances added in L3. Every message must carry the object's position,
      its uncertainty, a time stamp and the sender's own pose, with its
      uncertainty.


.. dropdown:: Exercise 5. One Tracker Cycle by Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run one cycle of the lecture's tracker on car B: predict, gate, and the
   track lifecycle.

   .. raw:: html

      <hr>

   **Part A. Predict**

   Car B's track (values chosen in the lecture): position
   :math:`(12.0, -2.0)` m, velocity :math:`(3.46, 2.00)` m/s, in fixed ground
   coordinates. State :math:`\mathbf{x} = [p_x, p_y, v_x, v_y]^\top`,
   constant velocity, :math:`\hat{\mathbf{x}}^{-} = F \hat{\mathbf{x}}`.

   1. Check the velocity: what speed and heading does
      :math:`(3.46, 2.00)` m/s give?
   2. Predict car B for :math:`\Delta t = 0.1` s, as in the lecture, and for
      :math:`\Delta t = 0.2` s (chosen for this exercise: one frame was
      lost).
   3. Write :math:`F` for :math:`\Delta t = 0.1` s and multiply it by the
      state. Which entries of :math:`F` carry the motion?

   .. raw:: html

      <hr>

   **Part B. Gate**

   This frame (:math:`\Delta t = 0.1` s), a box arrives at
   :math:`(12.65, -1.40)` m (chosen for this exercise). The lecture's score:
   :math:`\varepsilon = (\text{miss} \div \text{uncertainty})^2`, and a box
   can belong to the track only if :math:`\varepsilon < 9.21`.

   4. Compute the miss, the distance from the prediction to the box.
   5. Compute :math:`\varepsilon` if car B's uncertainty is 0.1 m, 0.2 m and
      0.5 m (each chosen for this exercise). For which ones is the box inside
      the gate?
   6. The gate, :math:`\varepsilon < 9.21`, is about 3 times the
      uncertainty. Compute the gate's radius in meters for each of the three
      uncertainties. Why does the lecture call 9.21 "3.03 squared"?

   .. raw:: html

      <hr>

   **Part C. The lifecycle**

   The tracker confirms a track that passes **M of N**, 3 detections in the
   last 5 frames (the lecture's example), and deletes a confirmed track after
   1 s with no detection (the lecture's tracker setting). Frames come every
   0.1 s. H is a frame with a detection in the track's gate, M a frame with
   none.

   7. A new detection starts track A. Its next frames read: H, H, M, H, H
      (frame 1 is the first H). At which frame is A confirmed? What is the
      planner told before that?
   8. Track Z starts on a reflection: H, M, M, M, M. What happens to it, and
      why is that the right outcome?
   9. Confirmed track A then gets no detection for 6 frames, then a
      detection inside its grown gate. What is its status during the 6
      frames, and after? What does the planner hear?
   10. How many frames in a row with no detection does a confirmed track
       survive before it is deleted?

   .. raw:: html

      <hr>

   **Deliverable**

   The two predictions, the miss and the three :math:`\varepsilon` with their
   verdicts, and a status table for tracks A and Z frame by frame.

   .. dropdown:: Guidance
      :color: success

      Question 1: speed :math:`\sqrt{3.46^2 + 2.00^2} = 4.0` m/s, and heading
      :math:`\arctan(2.00/3.46) = 30^\circ`: the velocity carries the
      heading, which is why the heading is not in the state.

      Question 2: :math:`\Delta t = 0.1` s:
      :math:`(12.0 + 0.346,\ -2.0 + 0.200) = (12.35, -1.80)` (the lecture).
      :math:`\Delta t = 0.2` s: :math:`(12.0 + 0.692,\ -2.0 + 0.400) = (12.69, -1.60)`.
      The velocity stays :math:`(3.46, 2.00)` in both.

      Question 3:

      .. math::

         F = \begin{bmatrix} 1 & 0 & 0.1 & 0\\ 0 & 1 & 0 & 0.1\\
                             0 & 0 & 1 & 0\\ 0 & 0 & 0 & 1 \end{bmatrix},
         \qquad
         F \begin{bmatrix} 12.0\\ -2.0\\ 3.46\\ 2.00 \end{bmatrix}
         = \begin{bmatrix} 12.35\\ -1.80\\ 3.46\\ 2.00 \end{bmatrix}

      The two :math:`\Delta t` entries add the velocity times the time to the
      position.

      Question 4: the box is 0.30 m ahead and 0.40 m to the left of
      :math:`(12.35, -1.80)`:
      :math:`\sqrt{0.30^2 + 0.40^2} = 0.50` m.

      Question 5: :math:`(0.5 \div 0.1)^2 = 25`: outside.
      :math:`(0.5 \div 0.2)^2 = 6.25`: inside.
      :math:`(0.5 \div 0.5)^2 = 1.0`: inside. The same 0.5 m is far for a
      sure track and close for an unsure one.

      Question 6: the gate's edge is where
      :math:`(\text{miss} \div \text{uncertainty})^2 = 9.21`, so
      :math:`\text{miss} = \sqrt{9.21} \times \text{uncertainty} = 3.03 \times`
      the uncertainty: 0.30 m, 0.61 m and 1.52 m. 9.21 is the 99 percent
      line for 2 numbers, :math:`x` and :math:`y`; the 99 percent is the
      lecture's choice.

      Question 7: after frame 4, A has 3 detections (frames 1, 2 and 4) in
      its last 5 frames: **Confirmed at frame 4**. Until then it is
      Tentative, and the planner is not told about it.

      Question 8: Z has 1 detection in its 5 frames, so it fails 3 of 5 and
      is **deleted**. It never became Confirmed, so the planner never heard
      of it. Starting a track on every detection would track every false
      alarm; the M of N test is what removes them.

      Question 9: **Coasting** during the 6 frames: the track moves on its
      prediction alone, its uncertainty and gate grow every frame, and the
      planner is still told, so it can slow down for an object it cannot
      see. The detection inside the grown gate updates the filter, and the
      track is **Confirmed** again, with the same ID and its velocity.

      Question 10: :math:`1.0/0.1 = 10` frames.

      .. list-table::
         :widths: 16 14 14 14 14 14 14
         :header-rows: 1
         :class: compact-table

         * - **Frame**
           - 1
           - 2
           - 3
           - 4
           - 5
           - after
         * - **A**
           - H, Tentative
           - H, Tentative
           - M, Tentative
           - H, **Confirmed**
           - H, Confirmed
           - 6 M: Coasting; then H: Confirmed
         * - **Z**
           - H, Tentative
           - M, Tentative
           - M, Tentative
           - M, Tentative
           - M, **Deleted**
           -


.. dropdown:: Exercise 6. Two Tracks, Three Detections
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Pair detections with tracks by hand, with nearest neighbor (NN) and global
   nearest neighbor (GNN), and see what each gets wrong.

   .. raw:: html

      <hr>

   **Specification**

   Car B cuts in just behind car D, which is ahead in the AV's lane. The
   tracker predicted both cars (the crosses); this frame, the detector reports
   three boxes (the red dots).

   .. figure:: /_static/images/L5/assoc_scene.png
      :alt: A top view, x forward to the right. The AV at the left, facing right, in its lane between two dashed lines; car B's lane to the right. Two crosses are the predicted positions: track B, blue, in the right part of the AV's lane, and track D, orange, ahead in the AV's lane. Each sits in a dashed circle of the same color, its gate. Three red dots are the boxes: 1 inside track B's gate only, behind and right of the blue cross; 2 between the crosses, inside both gates; 3 at the edge of track D's gate, ahead and right of the orange cross.
      :width: 60%
      :align: center

   Both tracks have :math:`\sigma = 1.2` m (chosen), so each gate is a circle
   of radius :math:`\sqrt{9.21} \times 1.2 = 3.64` m. The table gives
   :math:`\varepsilon = d^2/1.2^2` for every track and box, where :math:`d`
   is the distance between them in the drawing (positions chosen). A smaller
   :math:`\varepsilon` means closer; above 9.21 is outside the gate.

   .. list-table::
      :widths: 25 25 25 25
      :header-rows: 1
      :class: compact-table

      * - :math:`\varepsilon`
        - **box 1**
        - **box 2**
        - **box 3**
      * - **track B**
        - 5.4
        - 4.5
        - 47.3
      * - **track D**
        - 47.0
        - 5.9
        - 8.5

   1. Run **NN** with track B first, then with track D first. Same answer?
   2. What does **GNN** choose? Give its total.
   3. One box is left over. Name two things it could be, and how the
      **lifecycle** tells them apart.
   4. If the tracker **swaps** B and D, what does the planner believe? Why is
      that worse than losing both tracks?

   **Deliverable**

   Written answers, with the pairs and totals for questions 1 and 2.

   .. dropdown:: Answer
      :color: success

      Question 1. **B first:** B takes box 2, its nearest (4.5). D is left
      with box 1 (47.0, outside the gate) and box 3 (8.5): D takes 3. Total
      :math:`4.5 + 8.5 = 13.0`. **D first:** D takes box 2 (5.9). B takes box
      1 (5.4). Total :math:`5.9 + 5.4 = 11.3`. The order changed the answer:
      same code, same data, a different result depending on list order.

      Question 2. GNN tries every pairing inside the gates: B with 1 and D
      with 2 is :math:`5.4 + 5.9 = 11.3`; B with 2 and D with 3 is
      :math:`4.5 + 8.5 = 13.0`; B with 1 and D with 3 is
      :math:`5.4 + 8.5 = 13.9`. It picks **11.3**, B with 1 and D with 2,
      whatever the order.

      .. figure:: /_static/images/L5/assoc_graph_gnn.png
         :alt: A graph with tracks B and D on the left and boxes 1, 2 and 3 on the right, each line labeled with epsilon. B to 1 (5.4) and D to 2 (5.9) are thick green lines, GNN's choice; B to 2 (4.5) and D to 3 (8.5) are faint; B to 3 (47.3) and D to 1 (47.0) are dashed, outside the gate. Caption: GNN, total 5.4 + 5.9 = 11.3.
         :width: 45%
         :align: center

      Question 3. Box 3 is left over: a new object, or clutter (a false
      detection from noise or a reflection). It starts a **tentative** track.
      A real object keeps being detected and passes M of N in the next frames;
      clutter does not, and its track is deleted. The tracker does not have to
      be right this frame, only within a few frames.

      Question 4. **A swap is worse than a loss.** Lost tracks coast, then are
      deleted; if the cars are seen again, they restart as tentative tracks.
      The system knows it has less information, and the planner can slow down.
      Swapped tracks stay **confirmed**, each with the other car's history:
      the planner believes two confident velocities, both wrong.


.. dropdown:: Exercise 7. The Four Packages in CARLA
   :icon: number
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   **Goal**

   Run the lecture's four hands-on packages and compare what you see with
   the slides: boxes from LiDAR, segmentation graded against CARLA's truth,
   the views from above, and the tracker.

   .. raw:: html

      <hr>

   **Specification**

   The packages are in the course ROS repository. The commands, the
   settings and the course laptop's measured results are on
   :doc:`l5_code`. Each package needs a running CARLA server and the L2
   bridge. Your numbers will differ from the Code page's: they depend on the
   town, the traffic and your machine. Say on what hardware you measured.

   .. raw:: html

      <hr>

   **Part A. Boxes from LiDAR:** ``l5_box_demo``

   1. Run it with ``evaluate:=true``. Compare the box center's error with the
      bare centroid's. Which is closer to the truth, and why?
   2. Find a wall or a fence in RViz. Does it get a box? Why does that lower
      the precision?
   3. Find a car seen from one face only. Look at its heading. Why can one
      sweep not tell a car's front from its back?

   .. raw:: html

      <hr>

   **Part B. Segmentation:** ``l5_seg_demo``

   4. Run it with ``evaluate:=true`` and read the IoU of each class in the
      log. Which classes score high, and which fail?
   5. What happens to CARLA's lane markings? Explain from the network's
      training classes.

   .. raw:: html

      <hr>

   **Part C. Views from above:** ``l5_bev_demo``

   6. Save a snapshot. In ``ipm.png``, find a building or a car: how is it
      drawn? Explain with Exercise 3.
   7. In ``semantic.png``, the far road breaks into rows. Explain with
      Exercise 2, Part B.
   8. In ``occupancy.png``, find a gray (unknown) wedge. What casts it?

   .. raw:: html

      <hr>

   **Part D. The tracker:** ``l5_tracking_demo``

   9. Run the default (GNN) and ``association:=nn``, and count the ID
      switches of each.
   10. Run ``source:=truth flip_prob:=0.3`` with ``reset_on_class_change``
       off, then on. Watch the velocity arrows. Which part of the lecture
       does the second run reproduce?

   .. raw:: html

      <hr>

   **Deliverable**

   One snapshot per package, your measured numbers next to the Code page's,
   and a sentence for each question.

   .. dropdown:: What to expect
      :color: warning

      The numbers below are the Code page's, measured on the course laptop
      (CARLA 0.9.16, Town10HD); yours will differ.

      Question 1: over two runs of 120 s, the box center's mean error was
      0.91 m and 0.94 m, against 1.29 m and 1.44 m for the centroid of the
      same objects: the box moves the center 0.4 to 0.5 m closer, because it
      covers the side the LiDAR cannot see. The centroid falls short of the
      center, as in the lecture's frustum example.

      Question 2: yes. Walls, fences, poles and trees also form clusters,
      and this detector has no classes, so most boxes are not vehicles. The
      measured precision within 2 m was 0.13 and 0.12.

      Question 3: one sweep shows a rectangle, not which end is the front,
      so the heading is known only up to :math:`180^\circ`. A car seen from
      one face only gives a thin box whose long side can be the car's width:
      a :math:`90^\circ` error. Trained detectors like CenterPoint close this
      gap.

      Question 4: big, flat classes score high: road (with lane markings)
      0.962 to 0.989, building 0.876 to 0.886, sky 0.847 to 0.858 over three
      runs. Thin objects fail: pole 0.128 to 0.259, traffic light 0.048 to
      0.122. The network was trained on real streets and tested on a
      rendered town.

      Question 5: they come out as road. The network was trained on
      Cityscapes, which has no lane-marking class and counts the markings as
      road. In every run it called 99.6 to 99.9 percent of CARLA's
      lane-marking pixels road. This network cannot find lane lines.

      Question 6: it smears into a long streak pointing away from the AV.
      Its foot is placed right, and every point above the road is placed too
      far, farther the higher it is (Exercise 3, question 3).

      Question 7: a meter of far road is less than one image row (0.38 rows
      at 50 m with the lecture's camera), so far away the pixels land in
      separate rows of cells with gaps between them.

      Question 8: an object between the LiDAR and the space behind it: a
      car, a building or a wall. Behind the nearest obstacle the cell is
      unknown, not free.

      Question 9: on the Code page's LiDAR run (3034 sweeps), GNN with
      confirmed tracks first gave 119 ID switches and NN, oldest first, 161.
      With the truth detector, the two were close (31 and 32): in normal
      traffic, two vehicles rarely compete for one detection.

      Question 10: Tempe. With ``reset_on_class_change`` off, the Code page
      measured recall 0.998, 28 ID switches and a mean speed error of
      0.61 m/s; with it on, recall 0.357, 849 ID switches and 1.39 m/s. Every
      restart throws the velocity away: no history, no velocity, no
      predicted path.
