====================================================
GP3: Fusion & Localization
====================================================

.. admonition:: The Situation
   :class: story

   Your team's GP2 report chose the detector for the robotaxi in Town01. The
   car now sees the person in the dark jacket: a box in the camera image,
   20 times a second.

   To decide whether to brake, the planning lead needs three things that a
   box in the image does not give, all on one map:

   1. **Where is our car?** GNSS gives a position about once every 0.1 s, but
      it can drop out, and the company has just moved the GNSS antenna to a
      new spot on the roof.
   2. **Where is each person and each car around us,** in meters, on the same
      map?
   3. **How fast is each one moving?** The planner keeps a 3.0 m clearance
      around every object, and it needs the speed to know where the
      object will be next.

   GP3 builds all three, from the sensor rig, the detector and the tracker
   your team already has.

.. card:: GP3: At a Glance
   :class-card: sd-shadow-sm

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - Posted **Sunday, November 1**, due **Thursday, November 19**
      * - **Weight**
        - 25% of the group-project grade: 21.25% of the final project grade,
          17.0% of the course grade
      * - **Lectures**
        - L2 (projection), L3 (EKF, NIS, gating), L5 (frustum association,
          tracking), L6 (GNSS, dead reckoning, APE)
      * - **Starter code**
        - `gp3_starter <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/tree/main/gp3_starter>`__
          and `ads_msgs <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/tree/main/ads_msgs>`__
          in the course repository
      * - **Team Size**
        - 3 students, the GP1 team
      * - **Submission**
        - Canvas + the ``gp3`` branch of your GP1 repository


.. admonition:: AI Disclosure (required)
   :class: warning

   You may use AI tools on GP3. You must say so in your ``README.md``.

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

GP3 puts your car and every object around it on one map. You record a drive
with your own GP1 node, and every later task works on that recording.

.. code-block:: text

   Task 1: GP1 sensor_manager  ->  your drive: camera, LiDAR, IMU, GNSS, ground truth
       |
   Task 2: EKF (IMU + GNSS)    ->  /localization/pose
       |
   GP2 detector_node (camera)  ->  boxes in the image
       |
   Task 3: fusion (GP1 projection + LiDAR + pose)  ->  objects on the map
       |
   Task 4: tracker (GP2's, in meters)  ->  /perception/tracks: ID, position, speed
       |
   GP4: the planner and the behavior node

.. list-table::
   :widths: 26 14 60
   :header-rows: 1
   :class: compact-table

   * - **Task**
     - **Lecture**
     - **What it adds**
   * - 1. Record your drive (10 pts)
     - L2
     - 90 s of driving in Town01, recorded with your GP1 node, with the
       ground truth that grades everything else.
   * - 2. EKF localization (30 pts)
     - L3, L6
     - Your car's position, heading and speed on the map, from the IMU and
       GNSS, through a GNSS outage.
   * - 3. Camera-LiDAR fusion (25 pts)
     - L2, L5
     - Each detection from GP2, placed on the map with the LiDAR.
   * - 4. Tracking on the map (20 pts)
     - L3, L5
     - One ID and one speed per object, from GP2's tracker moved into meters.
   * - 5. Report (15 pts)
     - all
     - How far off a person's map position is, and why.

**What GP3 reuses.** Every task starts from code your team wrote:

.. list-table::
   :widths: 24 40 36
   :header-rows: 1
   :class: compact-table

   * - **Task**
     - **Your code it builds on**
     - **What is new**
   * - 1. Record
     - GP1: ``sensor_manager.py``, its YAML, ``record_launch.py``
     - Your GNSS antenna position; ground truth and traffic after each tick
   * - 2. EKF
     - GP1's IMU and GNSS topics; the Kalman filter's predict and update
     - ``f``, ``F``, ``h``, ``H``, and the order of predict and update
   * - 3. Fusion
     - GP2's ``detector_node.py``; GP1's ``lidar_projection.py``
       (``build_intrinsic_matrix``, ``build_extrinsic``)
     - The points inside each box, the nearest cluster, its map position
   * - 4. Tracker
     - GP2's ``box_tracker.py`` (``associate``, the lifecycle constants)
     - The state in meters, and the Mahalanobis gate instead of IoU

.. note::

   **If GP2 did not work for your team,** use the GP2 reference
   implementation released on Canvas: GP3 Task 3 needs a working
   ``detector_node``.


Learning Objectives
-------------------

After completing GP3, you will be able to:

- Record a drive with ground truth and check that its frames agree.
- Derive the Jacobians of a nonlinear motion model and of a GNSS model with
  an antenna offset, and check them against finite differences.
- Run an EKF on two sensors that arrive at different rates, and measure it
  with APE and the NIS check.
- Explain what happens to a filter in a GNSS outage when nothing measures
  the speed.
- Place 2D detections on the map with the LiDAR, and measure the position
  error against the truth.
- Track objects on the map with a Kalman filter and a Mahalanobis gate, and
  measure ID switches, MOTA and speed error.
- Split an object's map error into the part that comes from localization and
  the part that comes from fusion.


.. _gp3-provided-resources:

Provided Resources
------------------

GP3 adds files to the ``ads_pipeline`` package you extended in GP2. Keep
working in the same private repository, on a new branch.

1. Update the course repository:

   .. code-block:: bash

      cd ~/enpm818z_ws/src/enpm818z-fall-2026-carla-ros && git pull

2. Build the message package GP3 adds, ``ads_msgs`` (one tracked object:
   its ID, class, position, velocity and covariance):

   .. code-block:: bash

      cd ~/enpm818z_ws && colcon build --packages-select ads_msgs && source install/setup.bash

3. Start the ``gp3`` branch from your GP2 submission:

   .. code-block:: bash

      cd ~/enpm818z_ws/src/GP1_TeamX && git checkout -b gp3 gp2-final

4. Copy the GP3 files into your package. **Before you copy,** check that
   none of them already exists in your package:

   .. code-block:: bash

      (cd ../enpm818z-fall-2026-carla-ros/gp3_starter/ads_pipeline && find . -type f -printf '%P\n') | while read -r f; do [ -e "ads_pipeline/$f" ] && echo "already exists: ads_pipeline/$f"; done

   No output means the copy only adds files. Then copy:

   .. code-block:: bash

      cp -r ../enpm818z-fall-2026-carla-ros/gp3_starter/ads_pipeline/. ads_pipeline/

5. Add the GP3 nodes to ``setup.py``, in ``console_scripts``:

   .. code-block:: python

      'gnss_outage = ads_pipeline.gnss_outage:main',
      'localization_node = ads_pipeline.localization_node:main',
      'fusion_node = ads_pipeline.fusion_node:main',
      'tracker_node = ads_pipeline.tracker_node:main',

6. Add the message package to ``package.xml``:

   .. code-block:: xml

      <exec_depend>ads_msgs</exec_depend>

7. Check: ``python3 -m pytest test/ -k gp3`` runs. Most GP3 tests fail with
   ``NotImplementedError`` until you write the functions marked YOURS.

Folder Structure
~~~~~~~~~~~~~~~~

GP3 adds these files to your repository, on the ``gp3`` branch:

.. code-block:: text

   GP1_Team{X}/
   ├── ads_pipeline/
   │   ├── ads_pipeline/
   │   │   ├── sensor_manager.py      # Task 1: yours, from GP1, extended
   │   │   ├── ground_truth.py        # Provided
   │   │   ├── traffic.py             # Provided
   │   │   ├── geo.py                 # Provided
   │   │   ├── gnss_outage.py         # Provided
   │   │   ├── ekf_core.py            # Task 2
   │   │   ├── localization_node.py   # Task 2
   │   │   ├── fusion_core.py         # Task 3
   │   │   ├── fusion_node.py         # Provided
   │   │   ├── map_tracker.py         # Task 4
   │   │   └── tracker_node.py        # Provided
   │   ├── config/
   │   │   ├── carla_config.yaml      # Task 1: your GNSS mount
   │   │   ├── ekf_config.yaml        # Task 2: your antenna, Q and R
   │   │   └── fusion_config.yaml     # Provided
   │   ├── launch/
   │   │   ├── record_gp3_launch.py   # Provided
   │   │   └── gp3_launch.py          # Provided
   │   ├── tools/                     # Provided: the evaluators
   │   ├── test/
   │   │   └── test_gp3_*.py          # Provided
   │   ├── test_data/noisy_dets.json  # Provided: Task 4's day-1 input
   │   ├── package.xml                # + ads_msgs
   │   └── setup.py                   # + the four GP3 nodes
   ├── results/
   │   └── gp3/                       # every result file the tasks name
   ├── README.md                      # with your AI disclosure
   └── gp3_report.pdf                 # Task 5

Your drive and the run bags stay out of git: add ``gp3_data/`` (or wherever
you keep them) to ``.gitignore``. A 90 s drive's size depends on your
camera's image size. We measured 4.3 GiB at 1024 x 576, 6.6 GiB at
1280 x 720, 10.0 GiB at 1600 x 900 and 14.3 GiB at 1920 x 1080. Check your
free disk space before you record.

What the starter contains
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 20 50
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **Status**
     - **What it does**
   * - ``ground_truth.py``
     - Given
     - Publishes the car's true pose (``/ground_truth/ego``) and the true
       boxes of the vehicles and pedestrians within 80 m
       (``/ground_truth/objects``), in the map frame. Grading only: no node
       of yours may read them.
   * - ``traffic.py``
     - Given
     - 80 vehicles and 150 pedestrians, the same traffic for the same seed,
       as in GP2's drives.
   * - ``geo.py``
     - Given
     - Latitude and longitude to the map frame (see Task 2).
   * - ``gnss_outage.py``
     - Given
     - Drops the GNSS fixes inside your team's outage window, so your EKF
       sees no fix there.
   * - ``ekf_core.py``
     - **Yours:** ``f``, ``F_jacobian``, ``h``, ``H_jacobian``
     - The EKF. ``predict`` and ``update`` are given.
   * - ``localization_node.py``
     - **Yours:** ``on_imu``, ``on_gnss``
     - The EKF as a ROS 2 node; publishes ``/localization/pose`` and
       ``/localization/odom``.
   * - ``fusion_core.py``
     - **Yours:** ``associate_lidar_to_detection``, ``to_map``
     - Given: the projection that keeps each point with its pixel, ground
       removal and DBSCAN.
   * - ``fusion_node.py``
     - Given
     - Pairs each GP2 box with the LiDAR sweep of the same stamp, publishes
       ``/perception/fused_objects``.
   * - ``map_tracker.py``
     - **Yours:** ``MapKalman``, ``mahalanobis_cost``, ``MapTracker.step``
     - GP2's tracker on the map.
   * - ``tracker_node.py``
     - Given
     - Publishes ``/perception/tracks`` (``ads_msgs``), what GP4 reads.
   * - ``tools/ape.py``, ``fusion_eval.py``, ``track_eval.py``
     - Given
     - Score a run against the ground truth (see each task).


Your Team's Values
------------------

Each team has its own GNSS antenna position on the roof and its own GNSS
outage window. Find your rig letter on Canvas (the same rig as in GP1 and
GP2).

.. GP3-TEAM-CONFIG-BEGIN (generated by tools/make_gp3_configs.py)

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Rig
     - Antenna x (m, forward)
     - Antenna y (m, left)
     - Outage start (s)
     - Outage end (s)
   * - A
     - -1.22
     - -0.72
     - 35.2
     - 58.3
   * - B
     - -1.44
     - +0.19
     - 40.7
     - 60.4
   * - C
     - -1.41
     - -0.20
     - 38.7
     - 57.1
   * - D
     - +1.46
     - -0.46
     - 32.8
     - 49.9
   * - E
     - -1.11
     - -0.61
     - 44.4
     - 64.1

.. GP3-TEAM-CONFIG-END

How to read the table:

- **Antenna x and y** are the antenna's position in the vehicle frame, in
  meters: x forward, **y to the left**, from the car's origin. They go into
  ``ekf_config.yaml`` as ``antenna_x`` and ``antenna_y``.
- Your GP1 YAML uses CARLA's axes, where **y points right**. So the mount
  ``mounts.gnss_link`` gets ``x`` = antenna x and ``y`` = **minus** antenna y.
  For example, an antenna at y = +0.40 (left) is ``y: -0.40`` in the YAML.
- **The outage** is in seconds after the first GNSS fix of your drive. It
  goes to ``gp3_launch.py`` as ``outage_start_s`` and ``outage_end_s``.

.. important::

   **Every team's numbers are different.** The antenna offset changes your
   ``h`` and ``H``, and the grader runs your nodes on a second drive of your
   rig that you have not seen. Code from another team gives wrong positions
   on it.


Tasks
-----

GP3 is worth **100 points**. Run every command from the package root,
``ads_pipeline/``, with ROS 2 and your workspace sourced.

.. dropdown:: Task 1: Record Your Drive (10 pts)
   :icon: goal
   :class-container: sd-border-primary

   GP3 works on one 90 s drive in Town01, recorded with your GP1 node and
   your rig. This task extends ``sensor_manager.py`` so the drive has the
   ground truth and the traffic GP3 needs.

   **Step 1: Your GNSS mount.** In your ``config/carla_config.yaml``, set
   ``mounts.gnss_link`` ``x`` and ``y`` from Your Team's Values (``y`` is
   minus the table's antenna y). Keep ``z``.

   **Step 2: Extend sensor_manager.py.** Add these parameters to your
   parameter list, with these defaults:

   .. code-block:: python

      ('ground_truth', False), ('ignore_lights', False), ('max_sim_s', 0.0),
      ('traffic.vehicles', 0), ('traffic.walkers', 0), ('traffic.seed', 818),

   Then:

   1. Import ``from ads_pipeline import traffic`` and
      ``from ads_pipeline.ground_truth import GroundTruth``.
   2. After the vehicle and its sensors exist (and after autopilot is set):
      create ``self.gt = GroundTruth(self, self.world, self.vehicle)`` when
      ``ground_truth`` is true, and call ``traffic.spawn(self.client,
      self.world, <traffic manager port>, <vehicles>, <walkers>, <seed>,
      exclude_index=<your spawn_index>)`` when a count is above 0. Add the
      actors it returns to the list your node destroys.
   3. When ``ignore_lights`` is true and autopilot is on, call
      ``traffic_manager.ignore_lights_percentage(self.vehicle, 100.0)``. A
      car that waits at a red light for half the drive gives the EKF and the
      tracker little to do.
   4. In your tick callback, right after ``world.tick()``, call
      ``self.gt.publish(<sim time>)``, so the truth has the same stamp as
      the sensors.
   5. Write ``time_is_up(sim_now, sim_start, max_sim_s)``, a module-level
      function: true once ``max_sim_s`` seconds of simulated time have
      passed since ``sim_start``, and never when ``max_sim_s`` is 0. When it
      is true, stop ticking and shut the node down
      (``rclpy.try_shutdown()``), so the recording ends by itself.
   6. Stop the walker controllers before you destroy them
      (``actor.type_id == 'controller.ai.walker'``: call ``actor.stop()``).

   **Step 3: Record.** Set ``traffic.vehicles: 80`` and
   ``traffic.walkers: 150`` in your YAML, start CARLA, then:

   .. code-block:: bash

      ros2 launch ads_pipeline record_gp3_launch.py config:=$PWD/config/carla_config.yaml \
          out:=$HOME/gp3_data/drive duration:=90.0

   The launch file turns on autopilot, the ground truth and
   ``ignore_lights``, and records only the topics GP3 needs. Our recording
   took 118 s of wall time for 90 s of driving (1280 x 720 camera, 6.6 GiB;
   sizes for the other image sizes are under Folder Structure). On GP1's
   slowest machine (about 11 times slower than real time) it would take
   about 17 minutes.

   **Step 4: Evidence.** Save into ``results/gp3/``:

   - ``drive_info.txt``: the output of ``ros2 bag info`` on your drive. It
     must show 1800 camera frames (90 s at 20 Hz) and about 900 GNSS fixes.
   - ``playback.txt``: while ``ros2 bag play`` replays the drive, the output
     of ``ros2 topic hz`` on ``/carla/gnss/fix`` and ``/carla/imu/data``,
     and of ``ros2 topic echo --once`` on ``/ground_truth/ego``. It shows
     that the bag replays.

   **Tests:** ``python3 -m pytest test/test_gp3_ground_truth.py -v``.

.. dropdown:: Task 2: EKF Localization (30 pts)
   :icon: goal
   :class-container: sd-border-primary

   The EKF estimates your car's state on the map:

   .. math::

      \mathbf{x} = \begin{bmatrix} x & y & \theta & v \end{bmatrix}^T

   where :math:`(x, y)` is the car's origin on the map in meters,
   :math:`\theta` its heading in radians (0 along the map's x axis,
   counterclockwise positive) and :math:`v` its forward speed in m/s.

   **Prediction.** Between two IMU messages, :math:`dt` seconds apart, the
   heading turns at the IMU's yaw rate :math:`\omega` (rad/s), and the
   speed stays the same:

   .. math::

      x_{k} = x_{k-1} + v_{k-1} \cos\theta_{k-1}\, dt, \quad
      y_{k} = y_{k-1} + v_{k-1} \sin\theta_{k-1}\, dt, \quad
      \theta_{k} = \theta_{k-1} + \omega\, dt, \quad
      v_{k} = v_{k-1}

   Nothing in this model measures the speed directly: only the GNSS fixes,
   through the change in position, correct it. In the outage there are no
   fixes, so the speed stays at its last estimate.

   **Update.** The GNSS measures the antenna, not the car's origin. The
   antenna sits at :math:`(d_x, d_y)` in the vehicle frame (your team's
   values), so the measurement model is

   .. math::

      h(\mathbf{x}) = \begin{bmatrix}
         x + d_x \cos\theta - d_y \sin\theta \\
         y + d_x \sin\theta + d_y \cos\theta
      \end{bmatrix}

   **Yours, in ekf_core.py:** ``f``, ``F_jacobian``, ``h``, ``H_jacobian``.
   Derive both Jacobians on paper first; the tests compare them with finite
   differences at four headings.

   **Yours, in localization_node.py:** ``on_imu`` and ``on_gnss``, the order
   of predict and update. The IMU arrives at 20 Hz and the GNSS at 10 Hz, so
   half the IMU stamps also have a fix. Use the given ``Clock``: it returns
   how far to predict for each message's stamp, and 0 for a second message
   at the same stamp, so you never predict twice for one instant. Use the
   stamps, never the wall clock: a bag played at ``--rate 0.25`` must give
   the same answer.

   **The first state.** While the car stands still, nothing shows its
   heading, and the motion model cannot tell heading :math:`\theta` at speed
   :math:`v` from heading :math:`\theta + \pi` at speed :math:`-v`. Started
   at heading 0, our filter settled on the wrong one on two of five drives,
   3 m off for the whole drive. So ``on_gnss`` waits until the antenna has
   moved ``INIT_DISTANCE`` (3 m) from the first fix, and sets the first
   state with the given ``initial_state``: the heading is the direction of
   that move.

   **The map frame.** ``geo.py`` turns latitude and longitude into the map
   frame that GP1's ``sensor_manager`` publishes and the ground truth uses.
   Two facts about CARLA, measured on Town01: one degree is 111,275.5 m
   there, and **latitude grows toward the map's minus y**, because the map
   frame flips CARLA's y axis. ``geo.py`` handles both; anchor it at
   Town01's origin, latitude 0 and longitude 0 (in ``ekf_config.yaml``).

   **Run it.** ``gp3_launch.py`` replays your drive through the GNSS outage
   relay, your EKF, GP2's detector, fusion and the tracker, and records the
   outputs:

   .. code-block:: bash

      ros2 launch ads_pipeline gp3_launch.py bag:=$HOME/gp3_data/drive \
          config:=$PWD/config/carla_config.yaml ekf_config:=$PWD/config/ekf_config.yaml \
          fusion_config:=$PWD/config/fusion_config.yaml weights:=yolov8s.pt \
          outage_start_s:=<yours> outage_end_s:=<yours> out:=$HOME/gp3_data/run_ekf \
          nis_csv:=../results/gp3/nis.csv
      python3 -m tools.ape --bag $HOME/gp3_data/run_ekf --outage <start> <end> \
          --nis ../results/gp3/nis.csv --csv ../results/gp3/ape.csv

   ``ape.py`` prints the APE RMSE over the whole drive, inside the outage,
   and with GNSS, and the NIS verdict. "With GNSS" leaves out the outage and
   the 3 s after it: the first fixes after an outage still carry the error
   it built up, and the filter needs a moment to remove it.

   **Tune Q and R.** The starter's ``ekf_config.yaml`` is not tuned. Measure
   R from your rig's GNSS noise (it is in your GP1 YAML, in degrees), then
   tune Q until the NIS check says consistent. Report what you tried.

   **Our reference** on a demo drive (rig A's values, 90 s, a 23.1 s
   outage): APE RMSE 0.43 m with GNSS and 17.95 m inside the outage, with
   the NIS consistent (mean 1.94, 95.4% of fixes inside the band). With an
   untuned Q (``q_v`` 0.1), the outage APE was 29.59 m.

   **Evidence** in ``results/gp3/``: ``ape.txt`` (the output of ``ape.py``),
   ``ape.csv``, ``nis.csv``.

   **Tests:** ``python3 -m pytest test/test_gp3_ekf.py test/test_gp3_ape.py -v``.

.. dropdown:: Task 3: Camera-LiDAR Fusion (25 pts)
   :icon: goal
   :class-container: sd-border-primary

   ``fusion_node`` turns each GP2 detection into one point on the map, as in
   frustum association:

   1. Project the LiDAR sweep of the box's stamp into the image with your
      GP1 ``K`` and extrinsic (given: ``project_keep_points``; the published
      cloud has ROS axes, y left, and GP1's extrinsic expects CARLA's, y
      right, so it flips y for the projection only).
   2. Drop the points within 0.3 m of the road (given: ``remove_ground``).
      Without this, the road in front of a person's feet, inside the
      person's box, can be the nearest cluster.
   3. **Yours:** ``associate_lidar_to_detection``. Keep the points inside
      the box and between ``min_range`` and ``max_range`` from the LiDAR,
      group them with DBSCAN, and return the centroid of the cluster nearest
      the LiDAR.
   4. **Yours:** ``to_map``. Move that centroid from the LiDAR frame to the
      vehicle frame, then onto the map with the car's pose.

   **Start on day 1:** run the fusion with the true pose
   (``pose_topic:=/ground_truth/ego``), so your fusion does not wait for your
   EKF.

   **Score it.** Run ``gp3_launch.py`` twice, once with
   ``pose_topic:=/localization/pose`` (your EKF) and once with
   ``pose_topic:=/ground_truth/ego`` (the truth), then for each:

   .. code-block:: bash

      python3 -m tools.fusion_eval --bag $HOME/gp3_data/run_truth \
          --rig config/carla_config.yaml --drive $HOME/gp3_data/drive

   ``fusion_eval.py`` counts a true object only when the sensors can see it:
   inside the camera's field of view, within 60 m, and with at least 5 LiDAR
   points of the same sweep inside its box (as nuScenes does). A fused
   object matches a true one of the same class within 3 m: the LiDAR sees
   a car's near side, so the cluster's center falls short of the box's
   center, by up to half the car's length. It prints the share of true
   objects matched and the mean position error, by distance from the car.

   **Our reference** (YOLOv8s, rig A's demo drive), vehicles: with the true
   pose, 37.7% of the visible vehicles matched, mean error 1.61 m; with the
   EKF pose, 25.8%, 1.66 m. The demo drive had only 27 visible pedestrian
   instances, too few to compare.

   **Evidence:** ``fusion_truth.txt`` and ``fusion_ekf.txt``.

   **Tests:** ``python3 -m pytest test/test_gp3_fusion.py test/test_gp3_fusion_eval.py -v``.

.. dropdown:: Task 4: Tracking on the Map (20 pts)
   :icon: goal
   :class-container: sd-border-primary

   ``map_tracker.py`` is GP2's ``BoxTracker`` moved from pixels to meters.
   It imports ``CONFIRM_HITS``, ``MAX_MISSES``, ``Track`` and ``associate``
   from your ``box_tracker.py``. What changes:

   - **The state** is :math:`[x, y, v_x, v_y]` on the map, in meters and
     m/s, with a constant-velocity model over the time between two stamps.
     ``R_STD``, ``Q_ACC`` and ``V_STD0`` are given at the top of the file.
   - **The cost** of pairing a track with a detection is the Mahalanobis
     distance of the innovation, :math:`\nu^T S^{-1} \nu`, not
     1 minus IoU.
   - **The gate** is 9.21, the chi-square 99% bound for 2 values: a pair with a larger distance is never
     matched.

   **Yours:** ``MapKalman`` (``__init__``, ``predict``, ``update``),
   ``mahalanobis_cost`` and ``MapTracker.step``.

   **Start on day 1:** ``test_data/noisy_dets.json`` holds 1800 frames of
   detections made from the truth of a reference drive, each moved by noise
   of 1.29 m per axis, with 10% removed, and the truth beside them. Run your
   tracker on it before your fusion works.

   **Score it** on both runs of Task 3:

   .. code-block:: bash

      python3 -m tools.track_eval --bag $HOME/gp3_data/run_truth \
          --rig config/carla_config.yaml --drive $HOME/gp3_data/drive

   It prints ID switches, MOTA (as in GP2) and the mean speed error against
   the truth. **Our reference,** true pose: MOTA 0.145, 27 ID switches,
   speed error 1.07 m/s. MOTA is low because it also counts every visible
   vehicle the detector missed.

   **Evidence:** ``tracks_truth.txt`` and ``tracks_ekf.txt``.

   **Tests:** ``python3 -m pytest test/test_gp3_tracker.py test/test_gp3_track_eval.py -v``.

.. dropdown:: Task 5: Report (15 pts)
   :icon: goal
   :class-container: sd-border-primary

   ``gp3_report.pdf``, at most 5 pages. Every number in it must match a
   file in ``results/gp3/``.

   1. **The error budget.** How far off is an object's map position, and
      how much of that comes from your EKF and how much from your fusion?
      Use the two runs of Task 3: with the true pose, only fusion is wrong;
      with your EKF, both are.
   2. **The outage.** Plot your EKF's position error and its own
      1-sigma (from ``/localization/odom``'s covariance) against time, with
      the outage marked. What did the filter do, and why? Look at the speed:
      what did the car do during your outage, and what did the filter
      assume?
   3. **Q and R.** What you measured for R, what you tried for Q, and the
      NIS verdict of your final choice.
   4. **One failure,** with its time: a missed person, an ID switch or a
      false object. What each node published at that moment, and the cause.
   5. AI disclosure in ``README.md``, per member.


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
     - Starter copied, ``ads_msgs`` built, Task 1 recorded
     - ``drive_info.txt`` shows 1800 camera frames
   * - 3 to 8
     - Tasks 2, 3 and 4: one person per task; fusion uses the true pose and
       the tracker uses ``noisy_dets.json`` until the others are ready
     - Each task's tests pass
   * - 9 to 10
     - Everything on your drive, both poses
     - The six result files are saved
   * - 11 to 13
     - Task 5 and the submission
     - Checklist below fully ticked
   * - 14 to 15
     - **Slack**
     - Nothing scheduled


Submission
----------

.. important::

   **Submission Instructions**

   1. Push the ``gp3`` branch to your team's private repository.
   2. Keep the instructor, GitHub user ``rubixcubic``, as a collaborator.
   3. Tag the submission commit: ``git tag gp3-final && git push --tags``.
   4. Submit the repository link and ``gp3_report.pdf`` on Canvas by the
      deadline.
   5. Email your peer evaluation within 48 hours (see
      :ref:`peer-evaluation`).


Submission Checklist
--------------------

.. admonition:: Before Submitting: Check Every Item
   :class: tip

   **Build and tests**

   - [ ] ``colcon build --packages-up-to ads_pipeline`` succeeds.
   - [ ] ``python3 -m pytest test/ -k gp3`` passes, with nothing skipped.

   **Task 1**

   - [ ] ``mounts.gnss_link`` set from Your Team's Values (y with its sign
         flipped).
   - [ ] ``results/gp3/drive_info.txt`` and ``playback.txt`` saved.

   **Tasks 2 to 4**

   - [ ] ``ekf_config.yaml`` holds your antenna, your R and your tuned Q.
   - [ ] ``ape.txt``, ``ape.csv``, ``nis.csv`` saved.
   - [ ] ``fusion_truth.txt``, ``fusion_ekf.txt``, ``tracks_truth.txt``,
         ``tracks_ekf.txt`` saved.
   - [ ] No node of yours subscribes to ``/ground_truth/*``.

   **Repository**

   - [ ] No bags committed.
   - [ ] AI use disclosed in ``README.md``, two or three sentences per
         member.
   - [ ] Commit tagged ``gp3-final`` and pushed.
   - [ ] ``gp3_report.pdf`` submitted on Canvas.
   - [ ] Peer evaluation emailed within 48 hours (see :ref:`peer-evaluation`).


Grading Rubric
--------------

Total: **100 points**, scaled to 25% of the group-project grade (21.25% of
the final project grade).

The grader also runs your nodes on a **held-out drive**: a second 90 s
drive of your rig, with a different start and different traffic, that you
have not seen. "Reference" below means our reference solution on that same
drive. The factors (1.5 times, 0.8 times) are the margins chosen for GP3.

.. list-table::
   :widths: 26 10 64
   :header-rows: 1
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - Task 1: Recording
     - 10
     - **3** the ground-truth tests pass. **3** the GNSS mount is right: on
       your drive, the fixes land about 0.7 m from where your antenna
       really was (your rig's GNSS noise), not farther. **4**
       ``drive_info.txt`` and ``playback.txt``.
   * - Task 2: EKF
     - 30
     - **10** the EKF tests pass. **8** held-out APE with GNSS at most 1.5
       times the reference's. **6** held-out APE inside the outage
       at most 1.5 times the reference's. **6** NIS consistent, with Q and R
       explained.
   * - Task 3: Fusion
     - 25
     - **10** the fusion tests pass. **8** held-out, true pose: vehicles
       matched at least 0.8 times the reference's share, mean error at most
       1.5 times the reference's. **7** both runs on your drive, in
       ``fusion_truth.txt`` and ``fusion_ekf.txt``.
   * - Task 4: Tracking
     - 20
     - **8** the tracker tests pass. **7** held-out, true pose: ID switches
       at most 1.5 times the reference's and MOTA at least the reference's
       minus 0.1. **5** both runs on your drive, with one ID switch shown.
   * - Task 5: Report
     - 15
     - **5** the error budget. **5** the outage, with the plot and the
       cause. **3** Q, R and NIS. **2** one failure, with its time.

.. note::

   **Individual grade** = 60% team grade for GP3 + 40% peer review score, as
   for every project (:ref:`peer-evaluation`).


Common Mistakes
---------------

.. danger::

   - **The GNSS mount's y sign.** The table's antenna y points left; the
     YAML's y points right. A wrong sign moves your antenna to the other
     side of the car, and every fix lands 2 times your antenna y away from
     where the EKF expects it.
   - **Starting at heading 0.** The filter can settle on the opposite
     heading with a negative speed. Set the first state from the first move
     (``initial_state``).
   - **Predicting twice for one instant.** A GNSS fix and an IMU message
     often share a stamp. Use the ``Clock``: it returns 0 the second time.
   - **Using the wall clock.** ``dt`` comes from the message stamps. With
     the wall clock, a replay at another rate gives another answer.
   - **Anchoring at the first fix.** The map origin is latitude 0,
     longitude 0 in Town01. Anchored at the first fix, your EKF is in a
     different frame from the ground truth, and APE is the distance between
     the two frames.
   - **Reading the ground truth in a node.** ``/ground_truth/*`` is for
     grading. The grader checks your nodes' subscriptions.
   - **Committing a bag.** Your drive is several GB.
