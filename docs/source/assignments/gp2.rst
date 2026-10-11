====================================================
GP2: Perception (YOLO vs. RT-DETR)
====================================================

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

L4 compared two detectors on one image: **YOLOv8s**, a one-stage CNN that
needs NMS (non-maximum suppression, the step that removes duplicate boxes),
and **RT-DETR-L**, a transformer that needs no NMS. GP2 asks which of the
two your AV should run, and answers it with numbers from your own drives.

Both models stay as they are: COCO-pretrained, as in L4. **GP2 trains
nothing.** The work is in measuring them fairly:

1. **Ground truth.** You cannot grade a detector without knowing where the
   objects really are. CARLA knows: every vehicle and pedestrian has a 3D
   box. Task 1 turns those 3D boxes into the 2D boxes your camera would see.
2. **The detector as a ROS 2 node.** Task 2 wraps both models in one node
   that publishes ``vision_msgs/Detection2DArray``. GP3 reads it.
3. **Grading.** Task 3 computes AP and mAP, exactly as L4's appendix
   defines them, and checks your code against COCO's own.
4. **Tracking.** A detector that is right in each frame can still give a
   tracker a hard time. Task 4 builds an image tracker in the style of SORT
   (L5) and counts how often it loses an object's identity.
5. **The decision.** Task 5 is the report: which model, by day and by
   night, inside the 50 ms budget from L4, and why.

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
   boxes and different scores.


Learning Objectives
-------------------

After completing GP2, you will be able to:

- Project a 3D box from the simulator into the image, and decide which of
  its pixels the camera really sees.
- Run two pretrained detectors behind one ROS 2 interface and measure their
  time per image.
- Compute precision, recall, AP and mAP from scratch, and check the result
  against a reference implementation.
- Track boxes in the image with a Kalman filter, IoU matching and the
  Hungarian algorithm, and measure the result with ID switches and MOTA.
- Recommend a detector for an AV from measured accuracy, time and tracking
  behavior.


.. _gp2-provided-resources:

Provided Resources
------------------

GP2 adds files to the ``ads_pipeline`` package you built in GP1. Keep
working in the same private repository, on a new branch:

.. code-block:: bash

   cd ~/enpm818z_ws/src/enpm818z-fall-2026-carla-ros
   git pull

   cd ../GP1_TeamX
   git checkout -b gp2 gp1-final
   cp -r ../enpm818z-fall-2026-carla-ros/gp2_starter/ads_pipeline/. ads_pipeline/

None of the GP2 files has the same name as a GP1 file, so the copy adds
files and changes nothing you wrote.

Then install the Python packages that are not part of ROS 2:

.. code-block:: bash

   pip install ultralytics pycocotools scipy

We used Ultralytics 8.3.227. Ultralytics downloads the weights,
``yolov8s.pt`` and ``rtdetr-l.pt``, the first time you load each model.

Add the detector node to ``setup.py`` and its message packages to
``package.xml``:

.. code-block:: python

   # setup.py, in console_scripts
   'detector_node = ads_pipeline.detector_node:main',

.. code-block:: xml

   <!-- package.xml -->
   <exec_depend>vision_msgs</exec_depend>
   <exec_depend>cv_bridge</exec_depend>
   <exec_depend>python3-scipy</exec_depend>

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
     - **Task 1.** The frame loader, the camera transform, the near-plane
       clipping and the assembly of a frame's ground truth are given.
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
     - Records a drive with your rig. See :ref:`gp2-recording`.
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
   own tests, and the tests need neither CARLA nor the other tasks. A team
   of four can start all four on day one, one person each.

Run the tests from the package root:

.. code-block:: bash

   cd ~/enpm818z_ws/src/GP1_TeamX/ads_pipeline
   python3 -m pytest test/ -k gp2 -v


.. _gp2-recording:

Recording Your Drives
---------------------

Every number in GP2 comes from two drives that you record once:
``recordings/clear`` (``ClearNoon``) and ``recordings/night``
(``ClearNight``). Start CARLA, then from the package root:

.. code-block:: bash

   python3 tools/record_gp2.py --config config/carla_config.yaml \
       --weather ClearNoon --out recordings/clear
   python3 tools/record_gp2.py --config config/carla_config.yaml \
       --weather ClearNight --out recordings/night

What the recorder does:

- It loads your GP1 town, spawns your vehicle at your spawn point and puts
  an RGB, a depth and a semantic camera on your ``camera_rgb_front`` mount,
  with your image size and field of view.
- It adds 80 vehicles and 150 pedestrians, and drives your vehicle on
  autopilot in synchronous mode.
- Your vehicle ignores red lights. It still brakes for vehicles and
  pedestrians. In our test drive it otherwise stood at one red light for
  most of the drive, and a camera that does not move makes tracking too
  easy.
- It saves 600 frames at 20 Hz, 30 s of driving: the image, the depth and
  semantic images, the camera's pose and intrinsic matrix, and the 3D box
  corners of every vehicle and pedestrian within 80 m, parked cars
  included.
- **The same seed gives the same traffic.** The clear and the night drive
  differ only in the light, so any difference in the scores comes from the
  light.

On our test rig the clear drive took 822 MB and the night drive 543 MB,
most of it PNG images. Add ``recordings/`` to ``.gitignore``.

.. warning::

   **The tracker needs the drive at 20 Hz.** On a 60 s test drive, saving
   every fourth frame, 29% of the boxes moved so far between two saved
   frames that they overlapped their previous box with IoU below 0.3, the
   tracker's limit. Saving every frame of the same drive, it was 6.5%.


Tasks
-----

.. dropdown:: Task 1: Ground Truth from CARLA (20 pts)
   :icon: goal
   :class-container: sd-border-primary

   **Goal:** For every saved frame, the 2D box around each vehicle and
   pedestrian the camera sees.

   **Two steps per actor.**

   1. **Project its 3D box.** The 8 corners go from the world into the
      camera's optical frame, then through :math:`K` into pixels, as in L2
      and GP1. The box around the 8 projected corners says where the actor
      can be. This box is loose: it holds background around the actor.
   2. **Keep the actor's own pixels.** Inside that loose box, a pixel shows
      the actor when its semantic tag is the actor's class and its depth
      lies within the actor's own depth range. The final box is drawn around
      those pixels.

   .. figure:: /_static/images/GP2/gp2_loose_vs_tight.png
      :alt: A camera frame from a CARLA drive. A dark jeep is close ahead in the same lane, seen from behind. An orange box, the projection of the jeep's 3D box, reaches well past the jeep on the left, the right and below. A green box, drawn around the pixels that show the jeep, fits its outline.
      :align: center
      :width: 90%

      A jeep 1.9 to 5.9 m ahead of the camera. Orange: the projection of its
      3D box. Green: the box around the pixels that show it. RT-DETR-L's box
      for the jeep overlaps the green box with IoU 0.97, and the orange box
      with IoU 0.53.

   **Why the second step matters.** In the figure the detector is right.
   Graded against the orange box, its IoU is 0.53, just above the 0.5
   threshold of mAP@0.5 and below every stricter one. The closer the actor,
   the looser the projected box. On a 300-frame test drive, projected boxes
   as ground truth gave YOLOv8s an mAP@0.5 of 0.533 and RT-DETR-L 0.625.
   Pixel boxes on the same drive gave 0.600 and 0.718.

   **What you write,** in ``gt_boxes.py``:

   - ``project_points(points_world, T_opt_world, K)``: pixel coordinates
     and depth of N world points. CARLA's axes are x forward, y right, z up;
     the optical frame is x right, y down, z forward.
   - ``box_from_corners(uv, z, width, height)``: the box around the
     projected points, clipped to the image, or ``None`` when a point is
     behind the near plane, the box is outside the image, or it is smaller
     than 8 px.
   - ``actor_pixels(box, z_corners, depth, semantic, tags)``: the mask of
     the pixels that show the actor.

   **Given:** ``clip_near``. A car beside your vehicle can have corners
   behind the camera. Those corners have no pixel, but the front of the car
   is still in the image. ``clip_near`` cuts the 3D box at 0.1 m in front of
   the camera before it is projected.

   **Steps:**

   1. Make ``test/test_gp2_ground_truth.py`` pass.
   2. Run ``tools/grade.py`` on a drive. Before your Task 3 works, it stops
      after writing ``gt.json``; that is enough for now.
   3. Draw three frames of each drive and look at them:

      .. code-block:: bash

         python3 tools/show_frame.py --rec recordings/clear --frames 50 300 550 \
             --out results/gp2/overlays

   **Deliverables:**

   - The tests pass.
   - ``results/gp2/overlays/``: three frames of each drive, with ground
     truth drawn.
   - In the report: one frame where your ground truth is wrong or open to
     argument, and why. Some cases we saw: a pedestrian's swinging arm
     outside the box, two cars close together merged into one box, a car
     seen through a fence.

.. dropdown:: Task 2: The Detector Node (15 pts)
   :icon: device-camera-video
   :class-container: sd-border-primary

   **Goal:** Both models behind one function, used by the grading tools and
   by a ROS 2 node.

   **What you write:**

   - ``detector_core.load_model(model_type, weights, device)``: an
     Ultralytics ``YOLO`` for ``'yolo'``, an ``RTDETR`` for ``'detr'``, a
     ``ValueError`` for anything else.
   - ``detector_core.predict(model, bgr, conf, device)``: run the model at
     ``imgsz`` 640 and NMS IoU 0.7, keep only person, car, truck and bus,
     and map them to GP2's two classes with ``COCO_TO_GP2``.
   - ``detector_node.to_detection_array(dets, header)``: one
     ``Detection2D`` per detection, with the box center and size in pixels
     and one hypothesis (class and score).

   **Two confidence settings.** For grading, ``predict`` keeps every box
   down to confidence 0.001: AP needs the whole ranked list (L4's
   appendix). The node uses ``confidence_threshold`` (0.5 by default),
   because a planner should not see a box at 0.001.

   **Steps:**

   1. Make ``test/test_gp2_detector.py`` pass.
   2. Run both models on both drives. **Close CARLA first:**

      .. code-block:: bash

         python3 tools/run_detector.py --rec recordings/clear --model yolo --weights yolov8s.pt
         python3 tools/run_detector.py --rec recordings/clear --model detr --weights rtdetr-l.pt
         # and the same two for recordings/night

   3. Run the node live, with your GP1 sensors:

      .. code-block:: bash

         ros2 launch ads_pipeline sensors_launch.py
         ros2 launch ads_pipeline perception_launch.py model_type:=detr weights:=rtdetr-l.pt
         ros2 topic hz /perception/detections

   **Measuring the time.** ``run_detector.py`` times each call to your
   ``predict``, with the image already in memory, and reports the median
   over the drive after two warm-up calls. L4 asks you to say how a time
   was measured: the GPU, plugged in or on battery, and the method. Our
   numbers, on an RTX 4060 laptop GPU, plugged in:

   .. list-table::
      :widths: 40 30 30
      :header-rows: 1
      :class: compact-table

      * - Median time per image
        - YOLOv8s
        - RT-DETR-L
      * - clear drive, 600 images
        - 14.9 ms
        - 26.3 ms
      * - night drive, 600 images
        - 12.3 ms
        - 26.4 ms

   .. warning::

      **CARLA running on the same GPU ruins the measurement.** With CARLA
      running asynchronously beside it, our YOLOv8s median went from about
      15 ms to 271 ms.

   **Deliverables:**

   - The tests pass.
   - ``results/gp2/node.png``: the annotated image from
     ``/perception/annotated_image`` with each model, and the ``ros2 topic
     hz`` output in ``results/gp2/node_hz.txt``.
   - In the report: the median times, measured as above.

.. dropdown:: Task 3: Grading the Detectors (25 pts)
   :icon: checklist
   :class-container: sd-border-primary

   **Goal:** AP per class, mAP@0.5 and mAP@0.5:0.95, as L4's appendix
   defines them.

   **What you write,** in ``detection_eval.py``:

   - ``match_frame(dets, gts, iou_thr)``: go through one frame's
     detections from the highest score down; each takes the unmatched
     ground-truth box of its class with the highest IoU, if that IoU is at
     least ``iou_thr``.
   - ``pr_curve(scored, n_gt)``: precision and recall after each detection,
     over all frames.
   - ``average_precision(precision, recall)``: the 101-point AP.
   - ``mean_ap(frames)``: AP for each class at each of the 10 IoU
     thresholds, 0.50 to 0.95, and the two means.

   **Steps:**

   1. Make ``test/test_gp2_detection_eval.py`` pass. One test is L4's
      worked example: 3 people, 5 detections, AP = 92.5 / 101 = 0.916.
   2. Grade both drives:

      .. code-block:: bash

         python3 tools/grade.py --rec recordings/clear
         python3 tools/grade.py --rec recordings/night

   3. Check your mAP against pycocotools, the code COCO publishes for its
      own benchmark, on the same boxes:

      .. code-block:: bash

         python3 tools/check_coco.py --rec recordings/clear --model yolo

      Do it for both models and both drives. **The two must agree within
      0.005.** Our solution agreed to all four decimals it prints. A bigger
      gap means a bug in your matching or your AP.

   **Deliverables:**

   - The tests pass.
   - ``results/gp2/clear_results.json`` and ``night_results.json``, as
     ``grade.py`` writes them, and the four ``check_coco.py`` lines in
     ``results/gp2/coco_check.txt``.
   - In the report: a table of AP@0.5 per class, mAP@0.5 and mAP@0.5:0.95
     for each model and drive.

.. dropdown:: Task 4: The Image Tracker (25 pts)
   :icon: git-commit
   :class-container: sd-border-primary

   **Goal:** Follow each detection from frame to frame in the image, and
   count how often an object's track ID changes.

   L5's tracker followed objects on the ground, in meters. This one works in
   pixels, the way SORT does (L5):

   - **The state** of each track is its box's center and size and how fast
     they change, 8 numbers. A constant-velocity Kalman filter (L3) predicts
     it one frame ahead.
   - **The cost** of pairing a track with a detection is 1 minus their IoU.
     The Hungarian algorithm (``scipy.optimize.linear_sum_assignment``)
     picks the pairs with the lowest total cost. A pair below IoU 0.3 is
     never matched.
   - **The lifecycle:** a new track is reported from its third matched
     frame and deleted after 5 frames with no match. Tracks of different
     classes never match.

   **What you write,** in ``box_tracker.py``: ``BoxKalman`` (its
   ``__init__``, ``predict`` and ``update``), ``iou_cost``, ``associate`` and
   ``BoxTracker.step``. The noise values are in ``BoxKalman``'s docstring.

   **How it is measured.** ``grade.py`` runs your tracker on each model's
   detections at confidence ``--conf`` and above (0.5 by default), and
   matches its tracks to the ground truth in each frame. Each ground-truth
   box has the CARLA actor ID, so it counts:

   - an **ID switch** when an actor's track ID differs from the one it had
     the last time it was matched;
   - **MOTA** (multiple object tracking accuracy), from Bernardin and
     Stiefelhagen, "Evaluating Multiple Object Tracking Performance: The
     CLEAR MOT Metrics", 2008:

     .. math::

        \text{MOTA} = 1 - \frac{\sum_t (m_t + fp_t + mme_t)}{\sum_t g_t}

     with, in frame :math:`t`, :math:`m_t` the misses, :math:`fp_t` the
     false tracks, :math:`mme_t` the ID switches and :math:`g_t` the
     ground-truth boxes. 1 is perfect. ``grade.py`` counts the ID switches
     in a simpler way than the paper does.

   ``grade.py`` also prints a row named ``truth``: your tracker run on the
   ground truth itself, a perfect detector. On our clear drive that row
   gave MOTA 0.927 and 3 ID switches. **If your truth row is far below
   that, the bug is in your tracker, not in a detector.**

   **Steps:**

   1. Make ``test/test_gp2_tracker.py`` pass.
   2. Run ``grade.py`` on both drives and read the truth row first.
   3. Run it at three confidence cuts, for example ``--conf 0.3``,
      ``0.5`` and ``0.7``, and pick one.

   **Deliverables:**

   - The tests pass.
   - In the report: ID switches and MOTA for each model and drive at your
     chosen cut, with the truth row; why you chose that cut.

.. dropdown:: Task 5: The Report (15 pts)
   :icon: file
   :class-container: sd-border-primary

   **Goal:** Decide which detector your AV runs, from your own numbers.

   Answer each question with a number from Tasks 2 to 4, and say which
   drive and model it comes from.

   1. **The budget.** L4 gives each frame 50 ms at 20 Hz. How much of it
      does each model use on your GPU, and what is left for tracking and
      planning?
   2. **Night.** Which model loses more AP at night, and in which class?
      Show one night frame where a model misses an object it found by day,
      drawn with ``show_frame.py --dets``.
   3. **Tracking.** Which model gives your tracker more ID switches? Find
      the cause in the detections, with a count. One place to start: how
      often a model gives two boxes of the same class with IoU above 0.5 in
      one frame. Car, truck and bus are all ``vehicle`` in GP2.
   4. **The recommendation.** Which model should your AV run, by day and by
      night? Give the trade-off in numbers.

   **Deliverables:** ``gp2_report.pdf``, at most 6 pages, with the tables
   from Tasks 2 to 4, the Task 1 ground-truth frame, and the answers above.


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
     - Starter copied, packages installed, both drives recorded
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


Folder Structure
----------------

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
   │   ├── package.xml                # + vision_msgs, cv_bridge, python3-scipy
   │   └── setup.py                   # + detector_node
   ├── results/
   │   └── gp2/
   │       ├── overlays/              # Task 1: 3 frames per drive
   │       ├── node.png               # Task 2
   │       ├── node_hz.txt            # Task 2
   │       ├── clear_results.json     # Tasks 3 and 4
   │       ├── night_results.json     # Tasks 3 and 4
   │       └── coco_check.txt         # Task 3
   └── gp2_report.pdf                 # Task 5

Do not commit ``recordings/`` or the ``.pt`` weight files.

.. important::

   **Submission Instructions**

   1. Push the ``gp2`` branch to your team's private repository. The
      instructor, ``rubixcubic``, is already a collaborator from GP1.
   2. Tag the submission commit: ``git tag gp2-final && git push --tags``.
   3. Submit the repository link and ``gp2_report.pdf`` on Canvas by the
      deadline.
   4. Email your peer evaluation within 48 hours (see
      :ref:`peer-evaluation`).


Submission Checklist
--------------------

.. admonition:: Before Submitting: Check Every Item
   :class: tip

   **Build and tests**

   - [ ] ``colcon build --packages-up-to ads_pipeline`` succeeds.
   - [ ] ``python3 -m pytest test/ -k gp2`` passes, with nothing skipped.

   **Ground truth (Task 1)**

   - [ ] Both drives recorded with your GP1 rig, 600 frames each.
   - [ ] Overlays show boxes on the actors, by day and by night.

   **Detector (Task 2)**

   - [ ] ``ros2 launch ads_pipeline perception_launch.py model_type:=detr``
         starts RT-DETR-L (the log line says ``detr``).
   - [ ] ``/perception/detections`` publishes while CARLA runs.
   - [ ] Times measured with CARLA closed.

   **Grading and tracking (Tasks 3 and 4)**

   - [ ] ``check_coco.py`` agrees within 0.005 for both models and drives.
   - [ ] The truth row is in your report, next to both models.

   **Repository**

   - [ ] No recordings or weights committed.
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
   - **Timing with CARLA running.** See Task 2: the time grows many times
     over.
   - **Recording with another rig.** The recorder reads your
     ``carla_config.yaml``. If you changed the camera after GP1, put your
     GP1 rig back.
   - **Every COCO class counted.** A traffic light is not a vehicle. Keep
     only person, car, truck and bus.
   - **The y axis.** CARLA's y points right and its z up; the optical frame's
     y points down. The projection tests check both signs.
   - **Committing the recordings.** Two drives are over 1 GB.
