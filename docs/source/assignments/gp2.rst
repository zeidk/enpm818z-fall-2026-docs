====================================================
GP2: Perception (YOLO vs. RT-DETR)
====================================================

The Situation
-------------

Your team works at a small company that tests robotaxis on the streets of a
quiet town, CARLA's Town01. The car already carries the sensor rig your
team built in GP1. Its front camera sends 20 images every second.

Last week a safety driver wrote this in the test log: *at 9 pm, a person in
a dark jacket stepped off the curb in front of the car, and the car reacted
late.* Next month the company wants to start night service. Before that,
the perception lead asks your team to choose the detector that will read
the front camera. There are two candidates, both from L4:

- **YOLOv8s**, a one-stage network. It is fast, and it needs NMS to remove
  duplicate boxes.
- **RT-DETR-L**, a transformer. It is newer and larger, and it needs no NMS.

The perception lead writes three questions on the whiteboard:

1. **Which one finds more of the cars and people around us,** by day and
   by night?
2. **Is it fast enough?** A new image arrives every 50 ms. The detector
   must finish before the next one, and leave time for tracking and
   planning.
3. **Does it let the tracker keep one ID per person?** The planner must
   know that the person crossing now is the same person it saw a second
   ago, or it cannot predict where that person will walk next.

Nobody can answer these from the models' published scores. Those scores
come from COCO, a set of photos. They say nothing about this camera, at
this height and pitch, on these streets, at night. Your team needs its own
test: drive the route by day and by night, know where every car and every
person really was, and score each detector against that.

CARLA knows where everything is. That is what GP2 is built on.

.. card::
   :class-card: sd-bg-dark sd-text-white sd-shadow-sm

   **GP2: At a Glance**

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 2 weeks: posted **Wednesday, October 14**, due **Thursday,
          October 29**
      * - **Weight**
        - 27.2% of the course grade (34.0% of the project grade)
      * - **Lectures**
        - L3 (Kalman filter), L4 (detection and its grading), L5 (tracking)
      * - **Pre-read**
        - :doc:`/preread/detector-grading`: every score in GP2, step by step
      * - **Team Size**
        - 4 students, the GP1 team
      * - **Submission**
        - Canvas + the ``gp2`` branch of your GP1 repository


.. admonition:: AI Disclosure (required)
   :class: warning

   You may use AI tools on GP2. You must say so in your ``README.md``.

   Name the tool and describe how you used it, two or three sentences per
   team member. Disclosure carries no penalty. **Undisclosed use is a
   violation of the Code of Academic Integrity.**

   Your team is responsible for every line you submit. Any member may be
   asked, in class or office hours, to walk through any part of the code:
   why it works, what would break it, what you would change. **Work that
   cannot be explained does not count**, even if it runs.

   Read :ref:`ai-disclosure` for the full rules on what is permitted and
   what is not.


Overview
--------

GP2 answers the perception lead's three questions with numbers from your
own drives. Both models stay as they are: COCO-pretrained, as in L4. **GP2
trains nothing.** The work is in measuring them fairly.

.. figure:: /_static/images/GP2/gp2_pipeline.png
   :alt: A diagram in two parts. Top, Offline: grade both detectors on your two drives. Your team's two drives, given, clear and night, feed two data boxes. The camera image goes to Task 2, YOLOv8s and RT-DETR-L. The depth image, semantic image, camera pose, K and the actors' 3D boxes go to Task 1, ground truth. Both tasks feed a box of files, detections_yolo.json, detections_detr.json and gt.json, which feeds Task 3, AP and mAP, and Task 4, the tracker with ID switches and MOTA. Both feed Task 5, the report: which detector? Bottom, Live: the same detector code as a ROS 2 node. replay_drive.py plays a drive as a camera on /carla/camera/rgb/image to Task 2's detector_node, which uses detector_core and publishes /perception/detections as a Detection2DArray, read by GP3's fusion.
   :align: center
   :width: 100%

   What you build. **Top:** the offline test on your team's two drives;
   every score comes from them. **Bottom:** the same detector code, as the
   ROS 2 node that GP3 will read, fed here by a drive played as a camera.
   Each task has its own color.

1. **Ground truth (Task 1).** You cannot grade a detector without knowing
   where the objects really are. CARLA knows every vehicle's and every
   person's 3D box. Task 1 turns those 3D boxes into the 2D boxes your
   camera would see.
2. **The detectors (Task 2).** Both models behind one function, run on
   every recorded image and timed, and the same function inside a ROS 2
   node.
3. **Grading (Task 3).** AP and mAP for each model, by day and by night,
   exactly as L4's appendix defines them, checked against COCO's own code.
4. **Tracking (Task 4).** A detector that is right in most frames can
   still make a tracker lose a person's ID. Task 4 builds an image tracker
   in the style of SORT (L5) and counts how often that happens.
5. **The decision (Task 5).** The report answers the three questions, with
   your numbers.

.. list-table::
   :widths: 24 20 56
   :header-rows: 1
   :class: compact-table

   * - **Task**
     - **Lecture**
     - **What it gives the comparison**
   * - 1. Ground truth (20 pts)
     - L2, L4
     - The boxes every detection is graded against, for your camera rig.
   * - 2. Detector node (15 pts)
     - L4
     - Both models behind one interface, and their time per image.
   * - 3. Detector grading (25 pts)
     - L4
     - AP per class and mAP, for each model, by day and by night.
   * - 4. Image tracker (25 pts)
     - L3, L5
     - ID switches and MOTA for each model.
   * - 5. Report (15 pts)
     - all
     - The recommendation, with the numbers behind it.

.. important::

   **Every team's numbers are different.** Your ground truth comes from your
   GP1 camera rig: its position, pitch, image size and field of view. Two
   teams that run the same code on the same traffic still get different
   boxes and different scores. The figures on this page come from a **demo
   rig** that no team has (the GP1 starter's placeholder: camera 1.5 m
   forward, 1.6 m up, no pitch, 1280 x 720, 90 deg).


Learning Objectives
-------------------

After completing GP2, you will be able to:

- Project a 3D box from the simulator into the image, and decide which of
  its pixels the camera really sees.
- Run two pretrained detectors behind one ROS 2 interface and measure their
  time per image.
- Compute precision, recall, AP and mAP from scratch, explain what
  mAP\@0.5 and mAP\@0.5:0.95 measure, and check your result against a
  reference implementation.
- Track boxes in the image with a Kalman filter, IoU matching and the
  Hungarian algorithm, and measure the result with ID switches and MOTA.
- Recommend a detector for an AV from measured accuracy, time and tracking
  behavior.


.. _gp2-provided-resources:

Provided Resources
------------------

GP2 adds files to the ``ads_pipeline`` package you built in GP1. Keep
working in the same private repository, on a new branch.

1. Update the course repository:

   .. code-block:: bash

      cd ~/enpm818z_ws/src/enpm818z-fall-2026-carla-ros && git pull

2. Start the ``gp2`` branch from your GP1 submission:

   .. code-block:: bash

      cd ~/enpm818z_ws/src/GP1_TeamX && git checkout -b gp2 gp1-final

3. Copy the GP2 files into your package:

   .. code-block:: bash

      cp -r ../enpm818z-fall-2026-carla-ros/gp2_starter/ads_pipeline/. ads_pipeline/

   None of the GP2 files has the same name as a GP1 file, so the copy adds
   files and changes nothing you wrote.

4. Install the Python packages that are not part of ROS 2:

   .. code-block:: bash

      pip install ultralytics pycocotools scipy

   We used Ultralytics 8.3.227. Ultralytics downloads the weights,
   ``yolov8s.pt`` and ``rtdetr-l.pt``, the first time you load each model.

5. Add the detector node to ``setup.py``, in ``console_scripts``:

   .. code-block:: python

      'detector_node = ads_pipeline.detector_node:main',

6. Add its packages to ``package.xml``:

   .. code-block:: xml

      <exec_depend>vision_msgs</exec_depend>
      <exec_depend>cv_bridge</exec_depend>
      <exec_depend>python3-scipy</exec_depend>

Folder Structure
~~~~~~~~~~~~~~~~

GP2 adds these files to your GP1 repository, on the ``gp2`` branch:

.. code-block:: text

   GP1_Team{X}/
   ├── ads_pipeline/
   │   ├── ads_pipeline/
   │   │   ├── gt_boxes.py            # Task 1
   │   │   ├── detector_core.py       # Task 2
   │   │   ├── detector_node.py       # Task 2
   │   │   ├── detection_eval.py      # Task 3
   │   │   └── box_tracker.py         # Task 4
   │   ├── launch/
   │   │   └── perception_launch.py   # Provided
   │   ├── tools/                     # Provided
   │   ├── test/
   │   │   └── test_gp2_*.py          # Provided
   │   ├── recordings/                # your team's drives (not committed)
   │   │   ├── clear/
   │   │   └── night/
   │   ├── package.xml                # + vision_msgs, cv_bridge, python3-scipy
   │   └── setup.py                   # + detector_node
   ├── results/
   │   └── gp2/
   │       ├── overlays/              # Task 1: 3 frames per drive
   │       ├── node_yolo.png          # Task 2
   │       ├── node_detr.png          # Task 2
   │       ├── node_hz.txt            # Task 2
   │       ├── clear_results.json     # Tasks 3 and 4
   │       ├── night_results.json     # Tasks 3 and 4
   │       └── coco_check.txt         # Task 3
   └── gp2_report.pdf                 # Task 5

Do not commit ``recordings/`` or the ``.pt`` weight files.

What the starter contains
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 34 20 46
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **State**
     - **What you do with it**
   * - ``ads_pipeline/gt_boxes.py``
     - 3 functions missing
     - **Task 1.** The frame loader, the camera transform, the walker
       margin, the near-plane clipping and the assembly of a frame's ground
       truth are given.
   * - ``ads_pipeline/detector_core.py``
     - 2 functions missing
     - **Task 2.** ``load_model`` and ``predict``.
   * - ``ads_pipeline/detector_node.py``
     - 1 function missing
     - **Task 2.** The node is given; ``to_detection_array`` is yours.
   * - ``launch/perception_launch.py``
     - Complete
     - Starts the node. Every parameter is a launch argument.
   * - ``ads_pipeline/detection_eval.py``
     - 4 functions missing
     - **Task 3.** IoU and the class mapping are given.
   * - ``ads_pipeline/box_tracker.py``
     - 6 functions missing
     - **Task 4.** The lifecycle constants, the track record and the ID
       switch count are given.
   * - ``tools/record_gp2.py``
     - Complete
     - How your drives were recorded (:ref:`gp2-recording`). You do not
       need to run it.
   * - ``tools/replay_drive.py``
     - Complete
     - Plays a drive's images as a live camera topic, for the node (Task 2).
   * - ``tools/run_detector.py``
     - Complete
     - Runs your ``detector_core`` on every frame of a drive and times it.
   * - ``tools/grade.py``
     - Complete
     - Runs your Tasks 1, 3 and 4 on a drive and prints the results.
   * - ``tools/check_coco.py``
     - Complete
     - Compares your mAP with COCO's own code (Task 3).
   * - ``tools/show_frame.py``
     - Complete
     - Draws ground truth and detections on a frame.
   * - ``test/test_gp2_*.py``
     - Complete
     - The checks for every function you write. They run without CARLA.

.. note::

   **Nothing in the starter is a solution.** Every function that raises
   ``NotImplementedError`` is deliberate, and a submission that still raises
   one has not completed that task.

.. tip::

   **The four coding tasks do not wait for each other.** Each one has its
   own tests, and the tests need neither the drives nor the other tasks. A
   team of four can start all four on day one, one person each.

Run the tests from the package root:

.. code-block:: bash

   cd ~/enpm818z_ws/src/GP1_TeamX/ads_pipeline && python3 -m pytest test/ -k gp2 -v


.. _gp2-recording:

Your Team's Drives
------------------

Every number in GP2 comes from two recorded drives, the same 30 s of
traffic once by day (``ClearNoon``) and once by night (``ClearNight``),
seen through **your team's GP1 camera rig**. We recorded them for you. You
work only on these recordings: GP2 needs no CARLA.

1. Download your team's archive, ``team_X_drives.tar``, where ``X`` is your
   team number on Canvas (``team_3_drives.tar`` for Team3), and the file
   ``SHA256SUMS`` from the same folder (link on Canvas), into
   ``~/Downloads``.
2. Check that the download is complete. The line for your archive must end
   in ``OK``:

   .. code-block:: bash

      cd ~/Downloads && sha256sum -c --ignore-missing SHA256SUMS

   Anything else (``FAILED``, or no line for your archive) means the
   download stopped early: download the archive again.
3. Unpack it in your package root. It creates ``recordings/clear`` and
   ``recordings/night``:

   .. code-block:: bash

      cd ~/enpm818z_ws/src/GP1_TeamX/ads_pipeline && tar xf ~/Downloads/team_X_drives.tar

4. Add ``recordings/`` to ``.gitignore``. The team archives are 1.1 GB to
   2.8 GB, depending on your camera's image size.

.. figure:: /_static/images/GP2/gp2_scene_day_night.png
   :alt: Two views from a camera behind and above the demo car, a dark blue sedan driving on a two-lane road between trees and rocks, at the same moment of two drives, t = 20.0 s. Left, ClearNoon: bright daylight; a man in a yellow jacket walks on the left sidewalk, a man in a gray shirt and a smaller person on the right sidewalk, cars far ahead, and a 90 speed sign on the right. Right, ClearNight: the same scene in the dark, lit by a few street lamps; the people and the far cars are much harder to see.
   :align: center
   :width: 100%

   The demo drive at 20 s, seen from behind the car (this camera is only for
   this figure; your drives hold your front camera). **Left:** ClearNoon.
   **Right:** ClearNight. Same seed, so the same people and cars stand in
   the same places: only the light changes.

**What a drive folder holds.** 600 frames, numbered ``00000`` to
``00599``, 20 per second:

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **What it is**
   * - ``rgb/00000.png``
     - The color image your camera saw. The detectors run on it.
   * - ``depth/00000.npz``
     - The **depth image**: for every pixel, the distance along the
       camera's optical axis, in meters (NumPy, key ``depth``).
   * - ``semantic/00000.png``
     - The **semantic image**: for every pixel, CARLA's class of the
       object it shows (cars 14, trucks 15, buses 16, pedestrians 12).
   * - ``meta/00000.json``
     - The camera's pose in the world, its intrinsic matrix :math:`K`, and
       the 8 corners of every vehicle's and pedestrian's 3D box within
       80 m, parked cars included, each with its CARLA ID.

``gt_boxes.load_frame`` reads all four for you. Task 1 needs every one of
them; the detectors need only ``rgb``.

**How we recorded them** (``tools/record_gp2.py``, in the starter so you
can read it; you do not need to run it):

- We loaded Town01, spawned your vehicle at your spawn point, and put three
  cameras on your ``camera_rgb_front`` mount, with your pitch, image size
  and field of view: the color, depth and semantic cameras.
- We added 80 vehicles and 150 pedestrians and drove your vehicle on
  autopilot, in synchronous mode, so every saved frame's three images and
  3D boxes come from the same instant.
- Your vehicle ignored red lights. It still braked for vehicles and
  pedestrians. In one test drive it otherwise stood at one red light for
  most of the 30 s, and a camera that does not move makes tracking too
  easy.
- **The same seed gave the same traffic** by day and by night, so any
  difference in your scores comes from the light.

.. note::

   **Why 20 frames a second.** On a 60 s test drive, saving every fourth
   frame, 29% of the boxes moved so far between two saved frames that they
   overlapped their previous box with IoU below 0.3, the tracker's limit
   (Task 4). Saving every frame of the same drive, it was 6.5%.


Tasks
-----

.. dropdown:: Task 1: Ground Truth from CARLA (20 pts)
   :icon: goal
   :class-container: sd-border-primary

   **Goal:** Write the code that computes, for every saved frame, the 2D
   box around each vehicle and pedestrian the camera sees. These boxes are
   the answer key that every detection in GP2 is graded against.

   .. admonition:: Tools for this task
      :class: tools

      **You write the projection yourself,** in NumPy. No library call does
      it for you; it is the same calculation as L2 and GP1 Task 5.

      - **Class code to start from:** L2's ``project()`` in
        `lecture2/lidar_to_camera.py <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/blob/main/lecture2/lidar_to_camera.py#L90-L127>`__
        (course Python repo), and GP1's ``project_lidar_to_image()`` in
        `gp1_starter/.../lidar_projection.py <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/gp1_starter/ads_pipeline/ads_pipeline/lidar_projection.py#L74-L103>`__
        (course ROS 2 repo). Both carry points into the camera's frame, apply
        :math:`K` and divide by the depth. **One difference:** both drop
        the points behind the camera; your ``project_points`` must return a
        row for every point, with its depth.
      - **Given in** ``gt_boxes.py``: ``world_to_optical`` (the 4 x 4 matrix
        from world to optical frame, axis relabelling included),
        ``load_frame`` (the frame's :math:`K`, depth image, semantic image
        and actors' corners), ``clip_near``, ``widen_walker`` and
        ``ground_truth``.
      - **NumPy you will need:** ``@`` (matrix product), ``np.hstack`` (to
        add a column of ones for homogeneous points), ``np.clip``,
        ``np.isin`` (is a tag one of the class's tags) and ``np.nonzero``.
      - **To look at your boxes:** ``tools/show_frame.py``.

   .. figure:: /_static/images/GP2/gp2_camera_gt.png
      :alt: The demo car's front camera at 20 seconds into the clear drive. A two-lane road between trees on the left and rocks on the right. Blue boxes surround three people: a man in a yellow jacket on the left sidewalk, a man in a gray shirt on the right sidewalk, and a small distant person on the right. Green boxes surround three cars far ahead in the distance.
      :align: center
      :width: 90%

      The ground truth for one frame of the demo drive, the same moment as
      the figure above, seen from the front camera. **Green:** vehicles.
      **Blue:** pedestrians. Each box fits the pixels where the camera sees
      that actor.

   **Two steps per actor.**

   1. **Project its 3D box.** You write this step in ``project_points``.
      Each of the 8 corners, a world point :math:`P`, is first written as
      :math:`[P, 1]` and multiplied by ``T_opt_world`` (given by
      ``world_to_optical``), which puts it in the camera's optical frame:
      :math:`(x, y, z)`, with :math:`z` the depth. Then :math:`K` and a
      division by :math:`z` give the pixel: :math:`u = f x / z + c_u`,
      :math:`v = f y / z + c_v`. The box around the 8 pixels says where the
      actor can be. This box is loose: it holds road and sky around the
      actor.
   2. **Keep the actor's own pixels.** Inside that loose box, a pixel shows
      the actor when its semantic tag is the actor's class and its depth
      lies within the actor's own depth range. The final box is drawn around
      those pixels. A pixel nearer than the actor shows something in front
      of it, so a partly hidden actor gets a box around the part you can
      see.

   .. figure:: /_static/images/GP2/gp2_loose_vs_tight.png
      :alt: A camera frame from the demo drive. A black and white police car is parked at the left of the road, 5.5 to 10.7 meters away, seen at an angle. An orange box, the projection of its 3D box, reaches past the car on the left and well below it. A green box, drawn around the pixels that show the car, fits the car's outline.
      :align: center
      :width: 90%

      A police car 5.5 to 10.7 m ahead, seen at an angle. **Orange:** the
      projection of its 3D box (step 1). **Green:** the box around the
      pixels that show it (step 2). RT-DETR-L's box (not drawn) overlaps the
      green box with IoU 0.955 and the orange box with IoU 0.672.

   **Why the second step matters.** In the figure, the detector is right.
   Graded against the orange box, it looks only half right. On the demo
   drive by day, orange boxes as the answer key give RT-DETR-L an
   mAP\@0.5 of 0.608 and YOLOv8s 0.566. Green boxes, on the same
   detections, give 0.895 and 0.765. The detectors did not change; the
   answer key did. :doc:`/preread/detector-grading` explains IoU and mAP\@0.5.

   **What you write,** in ``gt_boxes.py``:

   - ``project_points(points_world, T_opt_world, K)``: the pixel coordinates
     and the depth of N world points. CARLA's axes are x forward, y right,
     z up; the optical frame is x right, y down, z forward. GP1 Task 5
     did the same for LiDAR points.
   - ``box_from_corners(uv, z, width, height)``: the box around the
     projected points, clipped to the image, or ``None`` when a point is
     behind the near plane, the box is outside the image, or it is smaller
     than 8 px.
   - ``actor_pixels(box, z_corners, depth, semantic, tags)``: the mask of
     the pixels that show the actor.

   **Given:**

   - ``clip_near``. A car beside your vehicle can have corners behind the
     camera. Those corners have no pixel, but the front of the car is still
     in the image. ``clip_near`` cuts the 3D box at 0.1 m in front of the
     camera before it is projected.
   - ``widen_walker``. CARLA's box for a person is tight around the body at
     rest, and a stride or a swinging arm reaches past it. ``widen_walker``
     makes it 0.3 m wider in every horizontal direction. We measured this
     against CARLA's instance camera, which labels each pixel with the
     actor it shows: without the margin, 32% of our pedestrian boxes
     matched it with IoU 0.9 or more; with it, 98.7%.

   **Steps:**

   1. Make the ground-truth tests pass:

      .. code-block:: bash

         python3 -m pytest test/test_gp2_ground_truth.py -v

   2. Run the grader on a drive. Before your Task 3 works, it stops after
      writing ``gt.json``; that is enough for now:

      .. code-block:: bash

         python3 tools/grade.py --rec recordings/clear

   3. Draw three frames of each drive and look at every box:

      .. code-block:: bash

         python3 tools/show_frame.py --rec recordings/clear --frames 50 300 550 --out results/gp2/overlays

      .. code-block:: bash

         python3 tools/show_frame.py --rec recordings/night --frames 50 300 550 --out results/gp2/overlays

   **Deliverables:**

   - Make every test in ``test/test_gp2_ground_truth.py`` pass.
   - Save three frames of each drive with the ground truth drawn, in
     ``results/gp2/overlays/``.
   - In the report, show one frame where your ground truth is wrong or open
     to argument, and explain why. Cases we saw: two cars close together
     merged into one box, and a car seen through a fence.

.. dropdown:: Task 2: The Detector Node (15 pts)
   :icon: device-camera-video
   :class-container: sd-border-primary

   **Goal:** Put both detectors behind one function, time them on your two
   drives, and run them live as a ROS 2 node. The grading tools and the node
   call the same function, so the detector you deploy is the detector you
   graded.

   .. admonition:: Tools for this task
      :class: tools

      - **Ultralytics** (``pip install ultralytics``): the classes ``YOLO``
        and ``RTDETR`` load a model from its weights file;
        ``model.predict(image, imgsz=..., conf=..., iou=..., device=...,
        verbose=False)`` runs it. Each result's ``boxes`` holds ``xyxy``,
        ``conf`` and ``cls``, and ``names`` maps a class number to its COCO
        name. See Ultralytics'
        `predict guide <https://docs.ultralytics.com/modes/predict/>`__.
      - **Class code to start from:** L4's ``run()`` in
        `lecture4/compare_detectors.py <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/blob/main/lecture4/compare_detectors.py#L64-L71>`__
        runs a model on one frame and reads its boxes.
      - **The message:** ``vision_msgs/Detection2D``, defined in
        `Detection2D.msg <https://github.com/ros-perception/vision_msgs/blob/ros2/vision_msgs/msg/Detection2D.msg>`__:
        a header, a list of hypotheses (class and score) and a 2D box.
      - **Given:** ``COCO_TO_GP2`` and the settings ``IMGSZ``, ``CONF`` and
        ``NMS_IOU`` in ``detector_core.py``; the node in
        ``detector_node.py``; ``launch/perception_launch.py``;
        ``tools/run_detector.py`` for the timing.

   **What you write:**

   - ``detector_core.load_model(model_type, weights, device)``: an
     Ultralytics ``YOLO`` for ``'yolo'``, an ``RTDETR`` for ``'detr'``, a
     ``ValueError`` for anything else.
   - ``detector_core.predict(model, bgr, conf, device)``: run the model at
     ``imgsz`` 640 and NMS IoU 0.7, keep only the COCO classes person, car,
     truck and bus, and map them to GP2's two classes with
     ``COCO_TO_GP2`` (person is a pedestrian; car, truck and bus are
     vehicles).
   - ``detector_node.to_detection_array(dets, header)``: one
     ``Detection2D`` per detection, with the box center and size in pixels
     and one hypothesis (class and score), stamped with the camera's header
     so GP3 can pair it with the LiDAR sweep from the same instant.

   **Two confidence settings.** For grading, ``predict`` keeps every box
   down to confidence 0.001: AP needs the whole ranked list
   (:doc:`/preread/detector-grading`). The node keeps only boxes at or above
   ``confidence_threshold`` (0.5 by default), because a planner should not
   act on a box at 0.001.

   .. figure:: /_static/images/GP2/gp2_two_models.png
      :alt: Four panels of the same camera frame, 20 seconds into the demo drive: YOLOv8s on the left, RT-DETR-L on the right, the clear drive on top, the night drive below. Thin green and blue boxes show the ground truth, three cars far ahead and three people; red boxes show the detections at confidence 0.5. Titles: YOLOv8s, clear: 4 boxes, 4 of 6 objects found. RT-DETR-L, clear: 6 boxes, 5 of 6 objects found. YOLOv8s, night: 2 boxes, 2 of 6 objects found; only the two near people have red boxes. RT-DETR-L, night: 6 boxes, 5 of 6 objects found.
      :align: center
      :width: 100%

      One frame, both models, both drives, at confidence 0.5. **Red:** a
      detection. **Green and blue:** the ground truth; where a red box
      covers it, the detection matched it (IoU 0.5 or more). At night
      YOLOv8s keeps the two near people and loses the three far cars and
      the far person.

   **Steps:**

   1. Make the detector tests pass:

      .. code-block:: bash

         python3 -m pytest test/test_gp2_detector.py -v

   2. Run both models on both drives, with nothing else using the GPU
      (see the warning below). YOLOv8s on the clear drive:

      .. code-block:: bash

         python3 tools/run_detector.py --rec recordings/clear --model yolo --weights yolov8s.pt

      RT-DETR-L on the clear drive:

      .. code-block:: bash

         python3 tools/run_detector.py --rec recordings/clear --model detr --weights rtdetr-l.pt

      YOLOv8s on the night drive:

      .. code-block:: bash

         python3 tools/run_detector.py --rec recordings/night --model yolo --weights yolov8s.pt

      RT-DETR-L on the night drive:

      .. code-block:: bash

         python3 tools/run_detector.py --rec recordings/night --model detr --weights rtdetr-l.pt

   3. Run the node live, on a drive played as a camera. Build and source
      your workspace, then start the detector, here RT-DETR-L:

      .. code-block:: bash

         ros2 launch ads_pipeline perception_launch.py model_type:=detr weights:=rtdetr-l.pt

      In a second terminal, play the night drive on your GP1 camera's topic,
      20 images a second, from the package root:

      .. code-block:: bash

         python3 tools/replay_drive.py --rec recordings/night

      In a third terminal, check that detections arrive about 20 times a
      second:

      .. code-block:: bash

         ros2 topic hz /perception/detections

      To see the boxes, open ``/perception/annotated_image`` in
      ``rqt_image_view`` or RViz2. On the demo drive, replayed by day into
      RT-DETR-L, the node published 235 messages in 12 s, 228 of them with
      at least one box.

   **Measuring the time.** ``run_detector.py`` times each call to your
   ``predict``, with the image already in memory, and reports the median
   over the drive after two warm-up calls. L4 asks you to say how a time
   was measured: the GPU, plugged in or on battery, and the method.

   .. figure:: /_static/images/GP2/gp2_latency.png
      :alt: A horizontal bar chart of the median time per image on the demo drives, with a dashed line at the 50 ms budget for 20 Hz. YOLOv8s clear 14.1 ms, YOLOv8s night 11.6 ms, RT-DETR-L clear 26.5 ms, RT-DETR-L night 26.6 ms. The axis label says RTX 4060 laptop GPU, plugged in, CARLA closed.
      :align: center
      :width: 80%

      Median time per image on the demo drives, against L4's 50 ms budget.
      Both fit; RT-DETR-L uses about half of the budget by itself
      (:math:`26.5 / 50 = 53\%`).

   .. warning::

      **Anything else on the GPU ruins the measurement.** With CARLA
      running beside it, our YOLOv8s median went from about 15 ms to
      271 ms. Close CARLA, games and other training runs before you time.

   **Deliverables:**

   - Make every test in ``test/test_gp2_detector.py`` pass.
   - Save one frame of ``/perception/annotated_image`` for each model,
     ``results/gp2/node_yolo.png`` and ``results/gp2/node_detr.png``, and
     save the ``ros2 topic hz`` output in ``results/gp2/node_hz.txt``.
   - In the report, give each model's median time per image on each drive,
     and say how you measured it: the GPU, plugged in or on battery, and the
     method.

.. dropdown:: Task 3: Grading the Detectors (25 pts)
   :icon: checklist
   :class-container: sd-border-primary

   **Goal:** Write the code that grades a detector against your ground
   truth, then compute AP per class, mAP\@0.5 and mAP\@0.5:0.95 for each
   model on each drive.

   .. admonition:: Tools for this task
      :class: tools

      **You write the matching, the curve and AP yourself,** in plain
      Python and NumPy. pycocotools is only the check.

      - **The method:** :doc:`/preread/detector-grading`, and L4's appendix
        (:doc:`/lectures/lecture4/l4_appendix`), which computes AP by hand.
      - **Given in** ``detection_eval.py``: ``iou(a, b)``, ``COCO_TO_GP2``,
        ``GP2_CLASSES`` and ``IOU_THRESHOLDS``.
      - **NumPy you will need:** ``np.cumsum`` (running counts of true and
        false positives), ``np.linspace(0, 1, 101)`` (the 101 recalls) and
        ``np.mean``.
      - **Given tools:** ``tools/grade.py`` runs your code on a drive;
        ``tools/check_coco.py`` compares your mAP with pycocotools
        (``pip install pycocotools``).

   **Read** :doc:`/preread/detector-grading` **first.** It explains each step with
   figures and worked examples. In short:

   - A detection is **right** (a true positive) when it overlaps an
     unclaimed object of its class with IoU at least :math:`t`, the IoU
     threshold.
   - Going down the detections from the most confident, precision and
     recall after each one draw the **precision-recall curve**. **AP** is
     the average precision along that curve, read at 101 recalls.
   - **mAP\@0.5** is the mean of the vehicle AP and the pedestrian AP, with
     :math:`t = 0.5`. The 0.5 is the IoU threshold, not a confidence.
     **mAP\@0.5:0.95** averages the mAP over the 10 thresholds 0.50, 0.55,
     ..., 0.95: it also rewards boxes that fit tightly.

   **What you write,** in ``detection_eval.py``:

   - ``match_frame(dets, gts, iou_thr)``: go through one frame's
     detections from the highest score down; each takes the unmatched
     ground-truth box of its class with the highest IoU, if that IoU is at
     least ``iou_thr``.
   - ``pr_curve(scored, n_gt)``: precision and recall after each detection,
     over all frames.
   - ``average_precision(precision, recall)``: the 101-point AP.
   - ``mean_ap(frames)``: AP for each class at each of the 10 IoU
     thresholds, and the two means.

   **Steps:**

   1. Make the evaluation tests pass. One test is L4's worked example: 3
      people, 5 detections, AP = 92.5 / 101 = 0.916.

      .. code-block:: bash

         python3 -m pytest test/test_gp2_detection_eval.py -v

   2. Grade the clear drive:

      .. code-block:: bash

         python3 tools/grade.py --rec recordings/clear

      and the night drive:

      .. code-block:: bash

         python3 tools/grade.py --rec recordings/night

   3. Check your mAP against pycocotools, the code COCO publishes for its
      own benchmark, on the same boxes. For example, YOLOv8s on the clear
      drive:

      .. code-block:: bash

         python3 tools/check_coco.py --rec recordings/clear --model yolo

      Do it for both models (``--model yolo``, ``--model detr``) and both
      drives. **The two must agree within 0.005.** Our solution agreed to
      all four decimals it prints. A bigger gap means a bug in your
      matching or your AP.

   **Deliverables:**

   - Make every test in ``test/test_gp2_detection_eval.py`` pass.
   - Copy the ``results.json`` that ``grade.py`` writes in each drive's
     folder to ``results/gp2/clear_results.json`` and
     ``results/gp2/night_results.json``.
   - Save the four ``check_coco.py`` lines (two models, two drives) in
     ``results/gp2/coco_check.txt``.
   - In the report, give a table of AP\@0.5 per class, mAP\@0.5 and
     mAP\@0.5:0.95 for each model and drive, like the one in
     :ref:`gp2-demo-results`.

.. dropdown:: Task 4: The Image Tracker (25 pts)
   :icon: git-commit
   :class-container: sd-border-primary

   **Goal:** Write an image tracker that follows each detection from frame
   to frame, run it on each model's detections, and count how often an
   object's track ID changes.

   .. admonition:: Tools for this task
      :class: tools

      - **Class code to start from:** L5's tracking demo,
        `l5_tracking_demo/tracker_core.py <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l5_tracking_demo/l5_tracking_demo/tracker_core.py>`__.
        Its ``KalmanCV`` (`lines 38 to 92 <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l5_tracking_demo/l5_tracking_demo/tracker_core.py#L38-L92>`__)
        is a constant-velocity Kalman filter on a position in meters, and
        its ``associate_gnn`` (`lines 119 to 138 <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l5_tracking_demo/l5_tracking_demo/tracker_core.py#L119-L138>`__)
        pairs tracks and detections with the Hungarian algorithm. Yours
        works on a box in pixels, with an IoU cost instead of a distance.
      - **The equations:** L3's Kalman filter (predict, then update).
      - **SciPy:** ``scipy.optimize.linear_sum_assignment(cost)`` returns
        the rows and columns of the lowest-cost pairing.
      - **Given in** ``box_tracker.py``: ``box_to_z`` and ``z_to_box``
        (box to measurement and back), the ``Track`` record, the lifecycle
        constants and ``count_id_switches``; ``iou`` comes from
        ``detection_eval.py``.

   L5's tracker followed objects on the ground, in meters. This one works
   in pixels, the way SORT does (L5). Each frame it does four things:

   1. **Predict.** Each track's Kalman filter moves its box one frame ahead.
   2. **Pair.** The cost of pairing a track with a detection is
      :math:`1 - \text{IoU}` of their boxes. The Hungarian algorithm
      (``scipy.optimize.linear_sum_assignment``) picks the pairs with the
      lowest total cost. A pair below IoU 0.3 is never matched (the gate).
      Tracks of different classes never match.
   3. **Update.** Each matched track's filter takes the detection's box as
      its measurement.
   4. **Manage the tracks.** An unmatched detection starts a new track. A
      new track is reported from its third matched frame, so one false box
      does not become an object. A track with no match for 5 frames is
      deleted.

   **The filter is L3's Kalman filter (KF), not the EKF.** The state is the
   box's center and size and how fast they change:
   :math:`x = [c_x, c_y, w, h, \dot c_x, \dot c_y, \dot w, \dot h]`, in
   pixels and pixels per frame. Both models are linear:

   - **Motion** (constant velocity): :math:`x_{k+1} = F x_k`, where
     :math:`F` adds each speed to its value once per frame.
   - **Measurement:** the detector reports the box itself,
     :math:`z = [c_x, c_y, w, h] = H x` with :math:`H = [I \;\; 0]`.

   L3 needed the EKF for an AV that steers: one step moves it by
   :math:`v\,\Delta t\cos\theta`, and no fixed matrix gives
   :math:`\cos\theta`. Nothing like that appears here, so the KF's
   equations apply exactly, with no Jacobians. The noise values are in
   ``BoxKalman``'s docstring.

   **What you write,** in ``box_tracker.py``: ``BoxKalman`` (its
   ``__init__``, ``predict`` and ``update``), ``iou_cost``, ``associate``
   and ``BoxTracker.step``.

   **How it is measured.** ``grade.py`` runs your tracker on each model's
   detections at confidence ``--conf`` and above (0.5 by default), and
   matches its tracks to the ground truth in each frame. Each ground-truth
   box has the CARLA actor ID, so ``grade.py`` counts:

   - an **ID switch** when an actor's track ID differs from the one it had
     the last time it was matched;
   - **MOTA** (multiple object tracking accuracy, Bernardin and
     Stiefelhagen, "Evaluating Multiple Object Tracking Performance: The
     CLEAR MOT Metrics", 2008):

     .. math::

        \text{MOTA} = 1 - \frac{\sum_t (m_t + fp_t + mme_t)}{\sum_t g_t}

     with, in frame :math:`t`, :math:`m_t` the misses, :math:`fp_t` the
     false tracks, :math:`mme_t` the ID switches and :math:`g_t` the
     ground-truth boxes. 1 is perfect. ``grade.py`` counts the ID switches
     in a simpler way than the paper does.

   .. figure:: /_static/images/GP2/gp2_track_timeline.png
      :alt: Two timeline panels, YOLOv8s on top and RT-DETR-L below, for six actors of the clear demo drive: pedestrians 346, 286, 328 and 321 and vehicles 210 and 256, over about 23 seconds. A gray line shows the frames where each actor is in the ground truth; colored bars show when a confirmed track covers it, one color per track ID; black crosses mark ID switches. YOLOv8s: 7 switches, 5 of them on pedestrian 321 between 4 and 8 seconds, whose bar is broken into many pieces. RT-DETR-L: 3 switches, one each on pedestrians 346 and 328 and vehicle 210.
      :align: center
      :width: 100%

      Six actors of the demo drive by day, tracked at confidence 0.5.
      **Gray:** the actor is in the ground truth. **A colored bar:** a
      confirmed track covers it, one color per track ID. **A cross:** an ID
      switch. YOLOv8s loses pedestrian 321 again and again between 4 and
      8 s, and each new detection after a gap can start a new track.

   ``grade.py`` also prints a row named ``truth``: your tracker run on the
   ground truth itself, a perfect detector. On the demo drive that row gave
   MOTA 0.874 and 5 ID switches. **If your truth row is much lower than
   that, the bug is in your tracker, not in a detector.**

   **Steps:**

   1. Make the tracker tests pass:

      .. code-block:: bash

         python3 -m pytest test/test_gp2_tracker.py -v

   2. Run ``grade.py`` on both drives (as in Task 3) and read the truth row
      first.
   3. Run it at three confidence cuts and pick one. For example, the clear
      drive at 0.3:

      .. code-block:: bash

         python3 tools/grade.py --rec recordings/clear --conf 0.3

      then ``--conf 0.5`` and ``--conf 0.7``, and the same on the night
      drive.

   **Choosing the cut is a trade-off.** A low cut gives the tracker more
   boxes: fewer misses, but more false and flickering boxes, so more ID
   switches. A high cut gives fewer switches but more misses. On the demo
   drive by day:

   .. list-table::
      :widths: 28 24 24 24
      :header-rows: 1
      :class: compact-table

      * - Confidence cut
        - 0.3
        - 0.5
        - 0.7
      * - YOLOv8s: ID switches, MOTA
        - 31, 0.530
        - 13, 0.458
        - 7, 0.303
      * - RT-DETR-L: ID switches, MOTA
        - 81, 0.407
        - 17, 0.651
        - 4, 0.582

   **Deliverables:**

   - Make every test in ``test/test_gp2_tracker.py`` pass.
   - In the report, give the ID switches and MOTA for each model and drive
     at the confidence cut you chose, next to the truth row, and explain
     why you chose that cut.

.. dropdown:: Task 5: The Report (15 pts)
   :icon: file
   :class-container: sd-border-primary

   **Goal:** Write a report that answers the perception lead's three
   questions with your own numbers and recommends one detector.

   .. admonition:: Tools for this task
      :class: tools

      - **Your numbers:** ``results.json`` in each recording folder, written
        by ``tools/grade.py``, and the times printed by
        ``tools/run_detector.py``.
      - **Your figures:** ``tools/show_frame.py --dets yolo`` (or ``detr``)
        draws a frame with the ground truth and one model's detections.
      - **Plots,** if you add any: Matplotlib, from the JSON files.

   Answer each question with a number from Tasks 2 to 4, and say which
   drive and model it comes from.

   1. **The budget.** L4 gives each frame 50 ms at 20 Hz. How much of it
      does each model use on your GPU, and what is left for tracking and
      planning?
   2. **Night.** Which model loses more AP at night, and in which class?
      Show one night frame where a model misses an object it found by day,
      drawn with ``show_frame.py --dets``.
   3. **Tracking.** Which model gives your tracker more ID switches at your
      cut? Find the cause in the detections, with a count. Two places to
      start: how often a model gives two boxes of the same class with IoU
      above 0.5 in one frame (car, truck and bus are all ``vehicle`` in
      GP2), and how often a track's object goes undetected for a few frames.
   4. **The recommendation.** Which model should your AV run, by day and by
      night? Give the trade-off in numbers.

   **Deliverables:**

   - Write ``gp2_report.pdf``, at most 6 pages: the tables from Tasks 2 to
     4, the Task 1 ground-truth frame, and your answers to the four
     questions above.
   - Submit it on Canvas and put a copy at the top of your repository.


.. _gp2-demo-results:

What the Demo Drive Gave
------------------------

These are our results on the demo rig, with the reference solution, so you
know what a working pipeline looks like. Your rig gives different numbers.
Do not copy these into your report.

.. list-table::
   :widths: 22 13 13 13 13 13 13
   :header-rows: 1
   :class: compact-table

   * - Drive, model
     - AP\@0.5 vehicle
     - AP\@0.5 pedestrian
     - mAP\@0.5
     - mAP\@0.5:0.95
     - ms per image
     - ID switches, MOTA (cut 0.5)
   * - clear, YOLOv8s
     - 0.719
     - 0.812
     - 0.765
     - 0.501
     - 14.1
     - 13, 0.458
   * - clear, RT-DETR-L
     - 0.911
     - 0.879
     - 0.895
     - 0.627
     - 26.5
     - 17, 0.651
   * - night, YOLOv8s
     - 0.654
     - 0.673
     - 0.664
     - 0.449
     - 11.6
     - 5, 0.358
   * - night, RT-DETR-L
     - 0.813
     - 0.749
     - 0.781
     - 0.546
     - 26.6
     - 16, 0.552

The truth row gave MOTA 0.874 and 5 ID switches on both drives (the ground
truth is the same by day and by night). pycocotools agreed with our mAP to
all four printed decimals on all four rows.

On a test drive with another rig, the answers changed: by day at cut 0.5,
RT-DETR-L gave about three times as many ID switches as YOLOv8s, and at
night YOLOv8s had the higher mAP\@0.5. The rig changes the answer, which
is why each team measures its own.


Suggested Schedule
------------------

The plan below finishes on day 13 of 15 and leaves two days of slack.

.. list-table::
   :widths: 14 40 46
   :header-rows: 1
   :class: compact-table

   * - Days
     - Milestone
     - Done when
   * - 1 to 2
     - Starter copied, packages installed, both drives unpacked
     - ``recordings/clear`` and ``recordings/night`` hold 600 frames each;
       ``pytest -k gp2`` runs
   * - 3 to 7
     - Tasks 1 to 4, one person each
     - Each task's tests pass
   * - 8 to 10
     - Everything on both drives
     - ``grade.py`` prints all rows; ``check_coco.py`` agrees; the node
       runs live
   * - 11 to 13
     - Task 5, overlays, submission
     - Checklist below fully ticked
   * - 14 to 15
     - **Slack**
     - Nothing scheduled


Submission
----------

.. important::

   **Submission Instructions**

   1. Push the ``gp2`` branch to your team's private repository.
   2. Add the instructor, GitHub user ``rubixcubic``, as a collaborator on
      the repository (Settings > Collaborators). The repository is private,
      so without this the grader cannot see or grade your work.
   3. Tag the submission commit: ``git tag gp2-final && git push --tags``.
   4. Submit the repository link and ``gp2_report.pdf`` on Canvas by the
      deadline.
   5. Email your peer evaluation within 48 hours (see
      :ref:`peer-evaluation`).


Submission Checklist
--------------------

.. admonition:: Before Submitting: Check Every Item
   :class: tip

   **Build and tests**

   - [ ] ``colcon build --packages-up-to ads_pipeline`` succeeds.
   - [ ] ``python3 -m pytest test/ -k gp2`` passes, with nothing skipped.

   **Ground truth (Task 1)**

   - [ ] Your team's drives unpacked in ``recordings/``, 600 frames each.
   - [ ] Overlays show boxes on the actors, by day and by night.

   **Detector (Task 2)**

   - [ ] ``ros2 launch ads_pipeline perception_launch.py model_type:=detr``
         starts RT-DETR-L (the log line says ``detr``).
   - [ ] ``/perception/detections`` publishes while ``replay_drive.py``
         plays a drive.
   - [ ] Times measured with nothing else on the GPU.

   **Grading and tracking (Tasks 3 and 4)**

   - [ ] ``check_coco.py`` agrees within 0.005 for both models and drives.
   - [ ] The truth row is in your report, next to both models.

   **Repository**

   - [ ] No recordings or weights committed.
   - [ ] ``rubixcubic`` added as a collaborator on the private repository.
   - [ ] Commit tagged ``gp2-final`` and pushed.
   - [ ] ``gp2_report.pdf`` submitted on Canvas.


Grading Rubric
--------------

Total: **100 points**, scaled to 34.0% of the project grade.

.. list-table::
   :widths: 30 12 58
   :header-rows: 1
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - Task 1: Ground truth
     - 20
     - **10** the ground-truth tests pass. **5** overlays with correct boxes
       on both drives. **5** one ground-truth error found and explained.
   * - Task 2: Detector node
     - 15
     - **5** the detector tests pass. **5** the node runs live with both
       models, set from the launch file. **5** times measured and reported
       as L4 asks.
   * - Task 3: Detector grading
     - 25
     - **10** the evaluation tests pass. **10** ``check_coco.py`` within
       0.005 for both models and drives. **5** the results table.
   * - Task 4: Image tracker
     - 25
     - **10** the tracker tests pass. **5** the truth row. **10** ID switches
       and MOTA for both models and drives, and the choice of confidence cut
       explained.
   * - Task 5: Report
     - 15
     - **4** the budget. **4** night, with the failure frame. **4** the
       tracking cause, with a count. **3** the recommendation.

.. note::

   **Individual grade** = 60% project grade + 40% peer review score, as for
   every project (:ref:`peer-evaluation`).


Common Mistakes
---------------

.. danger::

   - **Grading with confidence 0.5.** AP needs every box down to 0.001.
     Cutting at 0.5 throws away the low end of the precision-recall curve
     and changes the score.
   - **Reading mAP\@0.5 as a confidence.** The 0.5 is the IoU threshold.
     AP already averages over every confidence cut.
   - **Timing with something else on the GPU.** See Task 2: the time grows
     many times over.
   - **Using another team's drives.** Your drives are recorded with your
     rig, and graders check your numbers against them.
   - **Every COCO class counted.** A traffic light is not a vehicle. Keep
     only person, car, truck and bus.
   - **The y axis.** CARLA's y points right and its z up; the optical frame's
     y points down. The projection tests check both signs.
   - **Committing the recordings.** Two drives are over 1 GB.
