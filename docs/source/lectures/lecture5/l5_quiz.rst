====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Working
   through this page is good preparation for one. Memorizing the answers
   below is not.

This quiz covers Lecture 5: situation awareness, 3D boxes and the LiDAR
detectors that produce them, semantic segmentation of the road, the
bird's-eye view, IPM, Lift-Splat-Shoot and occupancy, early, intermediate and
late fusion, frustum association and cooperative situational awareness, and
multi-object tracking with its gate, its association methods and its track
lifecycle. Every question can be answered from the slides shown in class.
Nothing on this page needs the appendix.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.
   - Car B is the lecture's running example: its box center is
     :math:`(12.0, -2.0)` m in the AV's frame (:math:`x` forward, :math:`y`
     left), its size :math:`4.5 \times 1.9 \times 1.5` m, its heading
     :math:`30^\circ`. All of these values were chosen for the example.


----


Multiple Choice (Questions 1 to 21)
===================================

.. admonition:: Question 1
   :class: hint

   Endsley's definition of situation awareness has three levels. In the AV's
   pipeline, which part of this lecture gives the AV **Level 2,
   comprehension**?

   A. 3D detection, because it gives positions in meters.

   B. **Tracking, because it says which object is which from one frame to
      the next, and how fast each one moves.**

   C. Planning, because it decides what the AV does next.

   D. Prediction, because it says where each object will be in a few
      seconds.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Level 1, perception, is what is around the AV and where: 3D boxes, the
   road, the grid from above. Level 2, comprehension, is which object is
   which and what each one is doing. It starts in perception too, with
   tracking. Level 3, projection, is prediction (L8). Planning (**C**) is
   the decision, which Endsley places outside awareness, as "a stage
   separate from decision making and performance". See
   :ref:`l5-lec-sa`.


.. admonition:: Question 2
   :class: hint

   A 3D box, as the lecture defines it, holds 7 numbers. Which ones?

   A. The four pixel corners of the box, the class, the confidence and the
      frame number.

   B. **The center** :math:`(x, y, z)` **in meters in the AV's frame, the
      length, width and height, and the heading** :math:`\theta`.

   C. The center :math:`(x, y)`, the speed :math:`(v_x, v_y)`, the class,
      the confidence and the time stamp.

   D. The eight corners of the box, stored as one number each.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Center (3 numbers), size (3) and heading (1) make 7. The heading is the
   angle from the AV's :math:`x` axis to the way the object faces, measured
   counterclockwise seen from above. Many detectors add the velocity
   :math:`(v_x, v_y)`, for 9. Watch :math:`y`: it points right in CARLA and
   left in ROS. **A** is the L4 box, in pixels. See :ref:`l5-lec-3d`.


.. admonition:: Question 3
   :class: hint

   Car B, centered 2 m to the right of the AV's centerline and turned
   :math:`30^\circ` toward the AV's lane, has its front-left corner at
   :math:`(13.47, -0.05)` m. The AV's lane is 3.5 m wide. How far into the
   AV's lane does car B reach?

   A. 0.05 m

   B. 0.70 m

   C. **1.70 m**

   D. 2.00 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The lane edge is half a lane, 1.75 m, to the right of the centerline. The
   corner is 0.05 m to the right of it, so it is :math:`1.75 - 0.05 = 1.70`
   m into the lane, 13.5 m ahead. **B**, 0.70 m, is how far car B would
   reach if it pointed straight ahead: its left side at
   :math:`-2.0 + 0.95 = -1.05` m. **A** is the corner's distance from the
   centerline, not how far it reaches into the lane. See
   :ref:`l5-lec-corner-steps`.


.. admonition:: Question 4
   :class: hint

   A LiDAR has 64 channels spread evenly over :math:`40^\circ` (chosen for
   the lecture). Neighboring channels are :math:`0.635^\circ` apart, so on a
   surface 50 m away they hit 0.554 m apart in height. How many ring lines
   cross the back of car B, 1.5 m tall, if it is 50 m away?

   A. 11 or 12

   B. 19

   C. **2 or 3**

   D. 64

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`1.5 / 0.554 = 2.7`. A count of lines cannot be a fraction, so it
   is 2 or 3, depending on where the first line lands on the car. At 12 m
   the gap is :math:`12 \times 0.01108 = 0.133` m and the count is
   :math:`1.5/0.133 = 11.3`: 11 or 12 (**A**). **B** is the camera: an
   image 1280 px wide with a :math:`90^\circ` field of view has
   :math:`f = 640` px, so the same car at 50 m covers
   :math:`640 \times 1.5 / 50 = 19` rows. See :ref:`l5-lec-rings`.


.. admonition:: Question 5
   :class: hint

   Why does PointPillars group the points into pillars?

   A. To remove the points on the road before detection.

   B. To give each point a class from the camera.

   C. **To turn an unordered list of points into a 2D grid seen from above,
      so the 2D CNNs of L4 can read it.**

   D. To keep the full detail in height, which voxels lose.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Step 1 lays a grid of :math:`0.16 \times 0.16` m cells on the ground,
   and each cell collects every point above it: a pillar. Step 2 turns each
   pillar into one feature vector, and Step 3 puts each vector back at its
   cell: a pseudo-image seen from above. Step 4 runs a 2D CNN and a head on
   it. **D** is backward: the lecture's trade is that pillars are faster and
   voxels keep detail in height. See :ref:`l5-lec-pointpillars-steps`.


.. admonition:: Question 6
   :class: hint

   CenterPoint finds car B on its car heatmap. What is a **peak**, and what
   does the network read there?

   A. The cell with the most LiDAR points; the network reads the class
      there.

   B. **A cell whose value is higher than all its neighbors. It is the
      object's center, and the network reads the size, the heading and the
      velocity at that cell.**

   C. The preset box that best matches the points; the network corrects it
      to the 7 numbers.

   D. The cell nearest the AV; the network reads the distance there.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Step 4a gives one heatmap per class, each cell from 0 to 1. Step 4b finds
   the peaks: each one is the center of one object, and car B's sits at
   :math:`(12.0, -2.0)` m. Step 4c reads the rest of the box at that cell.
   **C** is PointPillars' SSD head, with its preset boxes (anchors), which
   CenterPoint replaces: a car turning at :math:`45^\circ` is still one
   peak. See :ref:`l5-lec-centerpoint-4b`.


.. admonition:: Question 7
   :class: hint

   The AV's front camera is :math:`1280 \times 720` pixels. What does
   semantic segmentation hand the planner for one frame?

   A. One box per object, with its class.

   B. One mask per person, each with its own id.

   C. **A grid the size of the image with one class number per pixel:
      921,600 numbers. Two people side by side get the same class.**

   D. A list of the classes present in the image, with no positions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`1280 \times 720 = 921{,}600`. Semantic segmentation gives a class
   to every pixel, including the road, the lane markings and the curb,
   which have no box. It does not tell two people apart; that is instance
   segmentation (**B**). On an AV a trained network computes the classes;
   in CARLA a semantic camera writes the true ones. See
   :ref:`l5-lec-semantic`.


.. admonition:: Question 8
   :class: hint

   The front camera has :math:`f = 640` px and sits 1.5 m above a flat road
   (chosen), looking level. A road point :math:`d` meters ahead lands
   :math:`v = f h / d` rows below the horizon. How many image rows does the
   meter of road from 50 to 51 m ahead get?

   A. 8.7

   B. 19.2

   C. **0.38**

   D. 23

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`640 \times 1.5/50 - 640 \times 1.5/51 = 19.20 - 18.82 = 0.38`
   rows: less than one row of pixels. The meter from 10 to 11 m gets
   :math:`96.0 - 87.3 = 8.7` rows (**A**), about 23 times as many (**D** is
   that ratio). On a BEV grid of 0.5 m cells, each meter is 2 cells, near or
   far. See :ref:`l5-lec-far-road`.


.. admonition:: Question 9
   :class: hint

   BEVFormer's grid has :math:`200 \times 200` cells over :math:`-51.2` to
   :math:`51.2` m in :math:`x` and :math:`y`. A point falls in cell
   :math:`i = \lfloor (x + 51.2)/0.512 \rfloor`, and the same for :math:`j`
   with :math:`y`. Which cell holds car B's center, :math:`(12.0, -2.0)` m?

   A. (12, -2)

   B. (100, 100)

   C. (124, 97)

   D. **(123, 96)**

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   The cell size is :math:`102.4/200 = 0.512` m. Then
   :math:`63.2/0.512 = 123.4`, rounded down to 123, and
   :math:`49.2/0.512 = 96.1`, rounded down to 96. **C** rounds up instead of
   down. **B** is the AV's own cell. The grid fixes this cell for every
   sensor, so everything that sees car B writes into the same cell. See
   :ref:`l5-lec-bev-grid`.


.. admonition:: Question 10
   :class: hint

   IPM assumes every pixel lies on the road. The camera is 1.5 m up, and a
   car 1.5 m tall has its back 10 m ahead (both chosen). Where does IPM put a
   point on the back of the car, **0.75 m** above the road?

   A. At 10 m, where it really is.

   B. At 5 m, half the distance.

   C. **At 20 m, twice too far.**

   D. Infinitely far.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The point is :math:`1.5 - 0.75 = 0.75` m below the camera, so it shows
   :math:`640 \times 0.75/10 = 48` rows below the horizon. IPM assumes it is
   on the road and computes :math:`d = 640 \times 1.5/48 = 20` m. The bottom
   of the car, on the road, comes out right at 10 m (**A**), and the roof
   top, level with the camera, at :math:`v = 0`, infinitely far (**D**).
   That is why IPM smears a car into a long streak. See
   :ref:`l5-lec-ipm-breaks`.


.. admonition:: Question 11
   :class: hint

   In Lift-Splat-Shoot, what does the **Lift** step do with one pixel of a
   camera that has no depth sensor?

   A. It assumes the pixel is on the road and puts it at one depth, as IPM
      does.

   B. It looks the depth up in the LiDAR sweep.

   C. **A CNN gives the pixel a feature and a probability for each depth
      bin along its ray, both set by training, and spreads the feature over
      the bins, weighted by those probabilities.**

   D. It throws the pixel away unless its depth is known.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The network does not guess one depth. The longest bar is near the real
   depth, but the others are not zero. **Splat** then drops each bin into the
   BEV cell it falls in, and each cell adds up what lands in it, from every
   camera. **Shoot**, in the paper, scores candidate paths on the filled
   grid. See :ref:`l5-lec-lss`.


.. admonition:: Question 12
   :class: hint

   A fallen branch lies in the AV's lane. No detector was trained on
   branches. What does 3D occupancy give the planner that boxes do not?

   A. A box around the branch, with the class "branch".

   B. **Voxels marked occupied where the branch is, even though it has no
      class.**

   C. Nothing: an object with no class is invisible to occupancy too.

   D. The branch's velocity.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Occupancy cuts the space around the AV into voxels, small cubes, each
   free, occupied or unobserved; an occupied voxel also gets a class, and
   the Occ3D benchmark labels things outside its list "general objects".
   On the Occ3D-nuScenes grid (0.4 m voxels, 80 by 80 by 6.4 m) that is
   :math:`200 \times 200 \times 16 = 640{,}000` voxels every frame. On an AV
   it runs next to the detector: boxes for objects you must predict,
   occupancy for everything you must not hit. See :ref:`l5-lec-occupancy`.


.. admonition:: Question 13
   :class: hint

   In which fusion design is each LiDAR point on car B paired with the
   camera pixel it lands on, and one network reads the pairs?

   A. **Early fusion**

   B. Intermediate fusion

   C. Late fusion

   D. Cooperative situational awareness

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   Early fusion joins the raw data before anything interprets it. Nothing
   is thrown away yet, and it is the only design where a target too weak
   for either sensor alone can still be found. The cost is agreement:
   calibration to a fraction of a degree and timing to milliseconds, or a
   pixel meets the wrong point, and one bad sensor spoils the single stream.
   See :ref:`l5-lec-fusion-early`.


.. admonition:: Question 14
   :class: hint

   Your AV buys a radar that sends a finished object list over CAN, the
   vehicle's internal data bus. At what stage can its data meet the camera's?

   A. At the raw data, before any processing.

   B. At the learned features, in the BEV cells.

   C. **At the finished answers: late fusion.**

   D. It cannot be fused with anything.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The radar sends conclusions, not raw data or features, so the constraint
   has already chosen late fusion for you. That is why most production
   stacks are late: the constraints come first. Real vehicles mix the three,
   for example one tightly synchronized camera and LiDAR pair on one rig
   fused early, everything else late. See :ref:`l5-lec-fusion-which`.


.. admonition:: Question 15
   :class: hint

   The camera sits at :math:`(1.6, 0, 1.5)` m on the AV, looking straight
   ahead and level, with :math:`f = 640` px and the image center at
   :math:`(640, 360)` (all chosen). In the camera's frame, :math:`x_c` is
   right, :math:`y_c` down and :math:`z_c` forward. Where does the LiDAR point
   :math:`(10.05, -3.125, 1.0)` m land in the image?

   A. (640.0, 360.0)

   B. (236.7, 37.9)

   C. **(876.7, 397.9)**

   D. (876.7, 322.1)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Into the camera's frame: :math:`z_c = 10.05 - 1.6 = 8.45` m,
   :math:`x_c = 3.125` m (right is :math:`-y`), and
   :math:`y_c = 1.5 - 1.0 = 0.5` m below the lens. Then
   :math:`u = 640 \times 3.125/8.45 + 640 = 236.7 + 640 = 876.7` and
   :math:`v = 640 \times 0.5/8.45 + 360 = 37.9 + 360 = 397.9`. **B** forgets
   to add the image center. **D** gets the sign of :math:`y_c` wrong: the
   point is below the lens, so it lands below the center row. See
   :ref:`l5-lec-frustum`.


.. admonition:: Question 16
   :class: hint

   The LiDAR hits car B on its rear face (15 points, middle
   :math:`(10.05, -3.125)`) and on its left side (26 points, middle
   :math:`(11.53, -1.18)`); the counts are chosen. Their centroid is
   :math:`(10.99, -1.89)`. Why is it 1.0 m short of the box center
   :math:`(12.0, -2.0)`?

   A. Because the LiDAR's range is measured to 1 m.

   B. **Because the LiDAR sees only the two faces turned toward the AV, so
      the average of the points sits toward the AV.**

   C. Because the camera box is too small.

   D. Because DBSCAN removed the points on the far side of car B.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`x = (15 \times 10.05 + 26 \times 11.53)/41 = 10.99` and
   :math:`y = (15 \times (-3.125) + 26 \times (-1.18))/41 = -1.89`. No point
   lands on the far faces, because the LiDAR cannot see them, so the
   centroid falls short. A meter matters: it is the gap the planner keeps.
   Real stacks fit a box to the cluster, or run a 3D detector on it. **D**
   is wrong: DBSCAN removed the wall's 9 points, not car B's. See
   :ref:`l5-lec-frustum`.


.. admonition:: Question 17
   :class: hint

   Car C, connected, sends the AV: "pedestrian 15 m ahead, 3 m left of me",
   with its own pose, :math:`(100, 0)` facing :math:`+x` in the map frame.
   The AV is at :math:`(70, 0)`. All positions are chosen. Where is the
   pedestrian, seen from the AV?

   A. 15 m ahead and 3 m left

   B. 30 m ahead and 3 m left

   C. **45 m ahead and 3 m left**

   D. 115 m ahead and 3 m left

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   In the map frame the pedestrian is at :math:`(100 + 15,\ 0 + 3) =
   (115, 3)`. From the AV: :math:`115 - 70 = 45` m ahead, 3 m left. The
   calculation needed C's own position: if C is wrong about where it is by
   a meter, the pedestrian is placed a meter wrong, and the two errors add.
   That is why each message carries the sender's pose and its uncertainty.
   See :ref:`l5-lec-csa`.


.. admonition:: Question 18
   :class: hint

   Car B's track is at :math:`(12.0, -2.0)` m with velocity
   :math:`(3.46, 2.00)` m/s (chosen). The tracker uses a constant-velocity
   Kalman filter, and the next boxes arrive :math:`\Delta t = 0.1` s later
   (chosen). Where does the filter predict car B?

   A. (12.0, -2.0)

   B. **(12.35, -1.80)**

   C. (15.46, 0.00)

   D. (12.20, -1.65)

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`p_x = 12.0 + 3.46 \times 0.1 = 12.35` and
   :math:`p_y = -2.0 + 2.00 \times 0.1 = -1.80`; the velocity stays. **C**
   uses 1 s instead of 0.1 s. The velocity is 4.0 m/s along the heading of
   :math:`30^\circ`, so the next box nearest :math:`(12.35, -1.80)` is the
   first candidate for car B. See :ref:`l5-lec-kf-per-object`.


.. admonition:: Question 19
   :class: hint

   Two tracks each have a box 2 m from their predicted position. Car B's
   track has an uncertainty of 0.1 m; a track started one frame ago has 3 m
   (both chosen). With :math:`\varepsilon = (\text{miss} \div
   \text{uncertainty})^2` and the gate :math:`\varepsilon < 9.21`, which
   box can belong to its track?

   A. Both: 2 m is close in both cases.

   B. Car B's only: it is the better-known track.

   C. **The new track's only:** :math:`\varepsilon = 0.44`, **against 400
      for car B.**

   D. Neither: 2 m is always outside the gate.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Car B: :math:`(2 \div 0.1)^2 = 20^2 = 400`, far outside. The new track:
   :math:`(2 \div 3)^2 = 0.44`, inside. The gate, 9.21, is :math:`3.03^2`:
   about 3 times the uncertainty, where 99 percent of the real car's boxes
   land if the uncertainty is honest (99 percent is our choice). So car B's
   gate is about 0.30 m and the new track's about 9 m. Two meters alone
   cannot say whether a box belongs to a track. See
   :ref:`l5-lec-same-2m`.


.. admonition:: Question 20
   :class: hint

   Why is global nearest neighbor (GNN) the usual default over nearest
   neighbor (NN)?

   A. GNN keeps several explanations across frames until later frames
      decide.

   B. GNN blends every detection in the gate, weighted by probability.

   C. **NN gives each track in turn its nearest free detection, so its
      answer depends on which track goes first; GNN picks the pairing with
      the lowest total distance over the whole frame, with no order effect.**

   D. GNN needs no gate.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   GNN solves one small optimization per frame, with the Hungarian
   algorithm. With NN, two crossing objects can swap identities. **A** is
   MHT and **B** is JPDA. **D** is wrong: whatever method you use, gate
   first (:math:`\varepsilon < 9.21`), which removes most clutter before the
   method runs. See :ref:`l5-lec-associate`.


.. admonition:: Question 21
   :class: hint

   A confirmed pedestrian walks behind a parked van, and no detection lands
   in her gate. What does the lecture's tracker do?

   A. Deletes her track on the first miss.

   B. **Moves her track on its prediction alone, as Coasting. Her
      uncertainty and gate grow every frame, and the planner is still told.
      After 1 s with no detection (our tracker's setting), the track is
      deleted.**

   C. Keeps her track Confirmed, with the same uncertainty, until she
      reappears.

   D. Starts a new tentative track for her.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   With no detection, the Kalman filter has nothing to update with. If she
   steps out and a detection lands inside the grown gate, the filter updates
   and the track is Confirmed again, with the same ID and velocity. Without
   coasting (**A**), she would come back as a new tentative track, and the
   planner would hear about her only after M of N frames. See
   :ref:`l5-lec-coasting`.


----


True or False (Questions 22 to 32)
==================================

.. admonition:: Question 22
   :class: hint

   Waymo's December 2025 post says its Sensor Fusion Encoder builds a
   bird's-eye view grid and tracks each object.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The post describes the encoder in one sentence: it "fuses camera, lidar,
   and radar inputs over time, producing objects, semantics, and rich
   embeddings for downstream tasks". It never mentions tracking, BEV,
   occupancy or segmentation: Waymo does not publish how the encoder works
   inside. Autoware, the open-source AV software, does, with each job a
   separate module. See :ref:`l5-lec-waymo-post`.


.. admonition:: Question 23
   :class: hint

   CenterPoint gives the heading as :math:`(\sin\theta, \cos\theta)`
   instead of the angle itself.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   :math:`359^\circ` and :math:`1^\circ` are neighbors but far apart as
   numbers; their sines and cosines are close. Car B's heading,
   :math:`30^\circ`, is read at its peak this way, with its size
   :math:`4.5 \times 1.9 \times 1.5` m and its velocity, 4.0 m/s. See
   :ref:`l5-lec-centerpoint-4c`.


.. admonition:: Question 24
   :class: hint

   In CARLA, the semantic segmentation camera's classes come from a trained
   network.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   CARLA's semantic camera writes the **true** class of every pixel, with no
   network; in its documentation, class 1 is road and class 2 is sidewalk.
   On a real AV there is no such camera: a trained network has to produce
   that picture from the camera image alone, every frame. See
   :ref:`l5-lec-seg-carla`.


.. admonition:: Question 25
   :class: hint

   IPM, inverse perspective mapping, is exact for lane markings on a flat
   road.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   IPM redraws an image as the ground seen from above by assuming
   everything in it lies on the road. Lane markings really are on the road,
   so they come out straight and parallel, with no learning and no depth
   sensor. Anything above the road is placed too far. See
   :ref:`l5-lec-ipm`.


.. admonition:: Question 26
   :class: hint

   In a BEV network, the 3D detection head and the map segmentation head
   each read the camera images again for their own task.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   One grid, built once per frame, is shared by every head: the cameras are
   read once, not once per task. Small networks called heads, set by
   training, each read that grid for one job: 3D detection, map
   segmentation, occupancy and the vectorized map. See
   :ref:`l5-lec-bev-heads`.


.. admonition:: Question 27
   :class: hint

   An unobserved voxel in an occupancy grid can be treated as free.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Unobserved means no sensor saw it; the hatched patch behind the car in
   the lecture's figure is unobserved, not free. Autoware's intersection
   module looks for unknown cells where cross traffic could come from, and
   slows the AV before it can see. See :ref:`l5-lec-occupancy` and
   :ref:`l5-lec-bev-industry`.


.. admonition:: Question 28
   :class: hint

   BEVFusion is a late-fusion design: the camera and the LiDAR each finish
   their own boxes, and a filter joins the boxes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   BEVFusion is intermediate fusion. It lifts the camera features to the
   BEV grid, takes the LiDAR features from above, and joins them there,
   because both describe the same cells of ground. Training decides how
   much each sensor counts. See :ref:`l5-lec-fusion-mid`.


.. admonition:: Question 29
   :class: hint

   Every LiDAR point that projects inside car B's camera box lies on car B.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The box is flat, but the space it sees is a wedge, the frustum, which
   includes points behind car B. In the lecture's example, 50 points (count
   chosen) land in the box: DBSCAN groups 41 on car B, 9 to 14 m ahead, and
   9 on a wall, 20 to 30 m ahead. Keep the near cluster. See
   :ref:`l5-lec-frustum`.


.. admonition:: Question 30
   :class: hint

   The gate around a track is a fixed number of meters, the same for every
   track.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The gate is about 3 times the track's uncertainty: a sure track has a
   small gate, an unsure one a large gate. For the same 2 m miss, car B's
   gate is about 0.30 m and a new track's about 9 m. See
   :ref:`l5-lec-gate`.


.. admonition:: Question 31
   :class: hint

   A filter fed another object's measurements gets only a little worse, the
   way a filter fed noisy measurements does.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Noise moves the estimate a little. A filter fed another object's
   measurements settles, precisely and confidently, on a path that never
   happened. The checks of L3, the NIS and the gate, test whether the
   measurements fit the track; they cannot tell whether the track follows
   the right object. See :ref:`l5-lec-wrong-match`.


.. admonition:: Question 32
   :class: hint

   In Tempe, the system first detected the pedestrian 1.2 s before impact.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   From the NTSB report: the radar detected her 5.6 s before impact, as a
   vehicle, and the LiDAR at 5.2 s, as an unknown object. Between 5.6 and
   1.2 s her class kept changing. At 1.2 s her location was in the path and
   the system saw an emergency; braking was then held back 1 s by design.
   See :ref:`l5-lec-tempe`.


----


Short Answer (Questions 33 to 38)
=================================

.. admonition:: Question 33
   :class: hint

   Car B is 50 m ahead. Compare what the LiDAR and the camera see of it,
   with the lecture's numbers, and say why the AV fuses the two.

.. dropdown:: Answer
   :class-container: sd-border-success

   With 64 channels over :math:`40^\circ` (chosen), neighboring LiDAR rings
   are 0.554 m apart at 50 m, so 2 or 3 rings cross car B's 1.5 m back. The
   camera, with :math:`f = 640` px, covers the same car with
   :math:`640 \times 1.5/50 = 19` rows of pixels.

   LiDAR measures distance well and sees little far away; the camera sees
   detail and guesses distance. Fusion gives the AV both: the camera says
   *what*, the LiDAR says *how far*, as in frustum association.


.. admonition:: Question 34
   :class: hint

   Why do current stacks give the road's classes on a grid seen from above
   rather than in the camera image? Use the lecture's numbers.

.. dropdown:: Answer
   :class-container: sd-border-success

   The planner works on the ground, in meters. In the image, a far lane line
   is only a few pixels wide: the CARLA capture measured 9 pixels at 10 m and
   4 at 20 m. The meter of road from 50 to 51 m gets 0.38 image rows,
   against 8.7 for the meter from 10 to 11 m.

   On a grid seen from above, every cell has the same size in meters: on a
   grid of 0.5 m cells, each meter of road is 2 cells, near or far.
   Distances on the grid are distances on the road.


.. admonition:: Question 35
   :class: hint

   Explain why IPM places objects wrongly, and what Lift-Splat-Shoot does
   instead to fill the BEV grid from cameras.

.. dropdown:: Answer
   :class-container: sd-border-success

   IPM computes :math:`d = f h / v` for every pixel, which is right only if
   the pixel is on the road. A point above the road is closer to the camera's
   height, so it lands fewer rows below the horizon, and IPM puts it too
   far: the back of a car, 0.75 m up and 10 m ahead, comes out at 20 m, and
   the roof top, level with the camera, infinitely far. Every car becomes a
   streak.

   Lift-Splat-Shoot does not assume the road. A network, set by training,
   gives each pixel a probability for each depth bin along its ray and
   spreads the pixel's feature over the bins; each BEV cell adds up what
   lands in it, from every camera.


.. admonition:: Question 36
   :class: hint

   You are choosing a fusion design. The camera and the LiDAR come from
   different vendors, at different rates, and you need to test and certify
   each path on its own. Which design fits, and what do you accept?

.. dropdown:: Answer
   :class-container: sd-border-success

   Late fusion. Each sensor finishes its own job, and a filter from L3
   joins the finished answers, so each path is built and tested on its own,
   and a failed sensor just stops reporting.

   What you accept: each sensor threw away all but its conclusion. Two
   sensors that each half-see a pedestrian can each report nothing, and you
   get two confident reports of an empty road. Intermediate fusion would
   need training data with every sensor present, and its rule lives in the
   weights: hard to explain, harder to certify.


.. admonition:: Question 37
   :class: hint

   Why is the heading not in the tracker's state
   :math:`\mathbf{x} = [p_x, p_y, v_x, v_y]^\top`, and what does that cost?

.. dropdown:: Answer
   :class-container: sd-border-success

   The velocity carries it: the direction of :math:`v = (3.46, 2.00)` m/s,
   the arc tangent of 2.00 over 3.46, is :math:`30^\circ`. And the motion
   rule :math:`F` stays a matrix; a heading in the state would need
   :math:`\cos\theta`, so the EKF of L3.

   The cost: a stopped car has no heading, and a turn is predicted straight.
   Real trackers add the heading with an EKF.


.. admonition:: Question 38
   :class: hint

   The Tempe system detected the pedestrian 5.6 s before impact. Explain, in
   tracking terms, why it did not brake in time, and the design fix the
   lecture gives.

.. dropdown:: Answer
   :class-container: sd-border-success

   Her class kept changing: vehicle, other, bicycle. The NTSB report says
   that when the classification changed, the system "no longer considered
   the tracking history" of the object. In our words, each change started a
   new track, and a track restarted every few frames never builds a history.

   No history, so no velocity estimate; no velocity, so no predicted path
   across the road; no predicted path, so nothing to brake for until 1.2 s.
   The fix is in the design: track the object, and classify it separately.
   A track's ID must not depend on its class.
