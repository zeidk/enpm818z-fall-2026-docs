====================================================
GP3: Fusion & Localization
====================================================

.. card::
   :class-card: sd-bg-dark sd-text-white sd-shadow-sm

   **GP3 -- At a Glance**

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 3 weeks (Week 8 -- Week 11)
      * - **Weight**
        - 25 points (25% of final project)
      * - **Lectures**
        - L6--L7
      * - **Team Size**
        - 4 students
      * - **Submission**
        - Canvas + GitHub repository link


Overview
--------

In GP3 you will extend the ADS pipeline built in GP1 and GP2 by adding
**sensor fusion** and **vehicle localization**. The core challenge is
combining your camera-based object detections (from GP2) with LiDAR
point cloud data to produce accurate **3D object positions**, and
implementing an **Extended Kalman Filter (EKF)** that fuses GNSS and
IMU measurements to provide a reliable estimate of the vehicle's pose.

By the end of GP3, your pipeline will output:

- ``/perception/fused_objects`` -- 3D bounding box detections with class labels and confidence.
- ``/localization/pose`` -- EKF-estimated vehicle pose (position + heading).
- ``/localization/odom`` -- Odometry message for downstream planning.

These two outputs serve as the primary inputs for GP4 (Planning & Control).


Learning Objectives
-------------------

After completing GP3, you will be able to:

- Project camera bounding boxes into 3D space using the LiDAR frustum
  association technique.
- Cluster LiDAR point clouds and match clusters to 2D detections.
- Derive and implement the Extended Kalman Filter prediction and update
  steps for a nonlinear vehicle motion model.
- Fuse GNSS position fixes with IMU angular velocity and wheel speed
  using configurable noise covariance matrices.
- Evaluate localization accuracy using Absolute Pose Error (APE) and
  Relative Pose Error (RPE).
- Quantitatively compare fused 3D object positions against CARLA
  ground-truth objects.
- Produce architecture diagrams, formulation write-ups, and
  quantitative results suitable for a technical report.


Provided Resources
------------------

The following files are provided by the instructor on Canvas and the
course GitHub repository. **Do not re-implement these utilities from
scratch** -- integrate them into your package.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - File
     - Description
   * - ``ekf_template.py``
     - EKF skeleton with pre-defined state vector ``[x, y, theta, v]``,
       placeholder matrices ``F``, ``H``, ``Q``, ``R``, and stub methods
       ``predict()`` and ``update()``. You fill in the math.
   * - ``fusion_utils.py``
     - Utility functions for camera-LiDAR association: ``project_to_image()``,
       ``get_frustum_points()``, ``nearest_neighbor_match()``, and
       ``compute_centroid()``.
   * - ``ground_truth_logger.py``
     - ROS 2 node that subscribes to the CARLA ground-truth actor list and
       logs vehicle pose and object positions to CSV for evaluation.
   * - ``evaluate_localization.py``
     - Computes APE and RPE from trajectory CSV files using the ``evo``
       toolkit format. Generates trajectory comparison plots.
   * - ``carla_config.yaml`` (updated)
     - Example config snippet showing new fusion-related parameters to
       add to your existing ``carla_config.yaml``.

.. note::

   All provided scripts are importable as Python modules. Place them in
   your ``ads_pipeline/`` package directory and add them to
   ``setup.py`` data files if needed.


Tasks
-----

GP3 is worth **100 internal points** (scaled to 25% of the project grade).
Complete all four tasks. The bonus task (Task 4) can push your score above
100, but total project weight is capped at 25 points.

.. dropdown:: Task 1: Camera-LiDAR Fusion Node (30 pts)
   :icon: gear
   :class-container: sd-border-primary

   Implement ``fusion_node.py``, a ROS 2 node that subscribes to 2D
   detections from GP2 and the raw LiDAR point cloud, and publishes 3D
   object detections.

   **Subscriptions:**

   - ``/perception/detections`` -- ``vision_msgs/Detection2DArray`` (from GP2 YOLO or DETR node)
   - ``/carla/lidar/points`` -- ``sensor_msgs/PointCloud2``

   **Publications:**

   - ``/perception/fused_objects`` -- ``vision_msgs/Detection3DArray``

   **Algorithm -- Frustum-Based Association:**

   1. For each 2D bounding box ``(u_min, v_min, u_max, v_max)`` in the
      detection array, use the camera intrinsic matrix ``K`` to back-project
      the four corners to rays in camera space.
   2. Use the extrinsic calibration (camera-to-LiDAR transform ``T_cl``)
      to transform the frustum into LiDAR frame.
   3. Retain all LiDAR points whose ``(u, v)`` projection falls within the
      bounding box **and** whose range is within ``[min_range, max_range]``.
   4. Run DBSCAN clustering on the retained points. Select the largest
      cluster as the associated object.
   5. Compute the 3D centroid of the cluster. Publish as ``Detection3D``
      with ``results[0].hypothesis.class_id`` and
      ``results[0].hypothesis.score`` copied from the 2D detection.

   **Edge Cases (required handling):**

   - If no LiDAR points fall within the frustum (occlusion, range limit,
     sensor dropout), publish the detection with ``bbox.center.position.z = -1``
     as a sentinel value and log a ``WARN`` message.
   - If multiple clusters are found, pick the cluster closest to the camera.
   - The node must work with both YOLO and DETR detection outputs from GP2
     without modification (both use ``Detection2DArray``).

   **Provided helper code (from** ``fusion_utils.py`` **):**

   .. code-block:: python

      from fusion_utils import get_frustum_points, compute_centroid

      def associate_lidar_to_detection(detection, cloud_array, K, T_cl,
                                       min_range=1.0, max_range=50.0):
          """
          Returns the 3D centroid (x, y, z) in LiDAR frame for a single
          Detection2D, or None if no points are found in the frustum.

          Parameters
          ----------
          detection   : vision_msgs/Detection2D
          cloud_array : np.ndarray, shape (N, 3), LiDAR points in LiDAR frame
          K           : np.ndarray, shape (3, 3), camera intrinsic matrix
          T_cl        : np.ndarray, shape (4, 4), camera-to-LiDAR extrinsic
          min_range   : float, minimum LiDAR range to consider (metres)
          max_range   : float, maximum LiDAR range to consider (metres)
          """
          bbox = detection.bbox
          u_min = bbox.center.position.x - bbox.size_x / 2.0
          u_max = bbox.center.position.x + bbox.size_x / 2.0
          v_min = bbox.center.position.y - bbox.size_y / 2.0
          v_max = bbox.center.position.y + bbox.size_y / 2.0

          frustum_pts = get_frustum_points(
              cloud_array, K, T_cl,
              u_min, u_max, v_min, v_max,
              min_range, max_range
          )

          if frustum_pts.shape[0] == 0:
              return None

          return compute_centroid(frustum_pts)

   **Node skeleton:**

   .. code-block:: python

      import rclpy
      from rclpy.node import Node
      from sensor_msgs.msg import PointCloud2
      from vision_msgs.msg import Detection2DArray, Detection3DArray, Detection3D
      import numpy as np
      import sensor_msgs_py.point_cloud2 as pc2
      from fusion_utils import get_frustum_points, compute_centroid

      class FusionNode(Node):
          def __init__(self):
              super().__init__('fusion_node')
              # Declare parameters
              self.declare_parameter('camera_frame', 'camera_front')
              self.declare_parameter('lidar_frame', 'lidar_top')
              self.declare_parameter('min_range', 1.0)
              self.declare_parameter('max_range', 50.0)

              # Load calibration (K and T_cl) -- implement load_calibration()
              self.K, self.T_cl = self.load_calibration()

              # Subscribers
              self.det_sub = self.create_subscription(
                  Detection2DArray, '/perception/detections',
                  self.detections_callback, 10)
              self.lidar_sub = self.create_subscription(
                  PointCloud2, '/carla/lidar/points',
                  self.lidar_callback, 10)

              # Publisher
              self.fused_pub = self.create_publisher(
                  Detection3DArray, '/perception/fused_objects', 10)

              self.latest_cloud = None

          def lidar_callback(self, msg):
              pts = pc2.read_points_numpy(msg, field_names=('x', 'y', 'z'),
                                          skip_nans=True)
              self.latest_cloud = pts

          def detections_callback(self, msg):
              # TODO: implement fusion logic here
              pass

          def load_calibration(self):
              # TODO: load K and T_cl from config or TF tree
              raise NotImplementedError

      def main(args=None):
          rclpy.init(args=args)
          node = FusionNode()
          rclpy.spin(node)
          node.destroy_node()
          rclpy.shutdown()

   .. tip::

      Synchronize the LiDAR and camera messages using
      ``message_filters.ApproximateTimeSynchronizer`` for production-quality
      fusion. For this project, caching the latest cloud and matching on
      detection arrival is acceptable if you document the latency assumption.

.. dropdown:: Task 2: EKF Localization Node (35 pts)
   :icon: gear
   :class-container: sd-border-primary

   Implement ``localization_node.py`` using the provided ``ekf_template.py``
   skeleton. The EKF estimates the vehicle's 2D pose and speed.

   **State Vector:**

   .. math::

      \mathbf{x} = \begin{bmatrix} x \\ y \\ \theta \\ v \end{bmatrix}

   where ``(x, y)`` is position in the map frame, ``theta`` is heading
   (radians), and ``v`` is forward speed (m/s).

   **Prediction Step -- Bicycle Model:**

   Given IMU angular velocity ``omega`` (rad/s) and elapsed time ``dt``:

   .. math::

      \mathbf{x}_{k|k-1} = \begin{bmatrix}
          x_{k-1} + v_{k-1} \cos(\theta_{k-1}) \, dt \\
          y_{k-1} + v_{k-1} \sin(\theta_{k-1}) \, dt \\
          \theta_{k-1} + \omega \, dt \\
          v_{k-1}
      \end{bmatrix}

   The Jacobian ``F`` linearizes this around the current state estimate.

   **Update Step -- GNSS Measurement:**

   GNSS provides ``(lat, lon)`` which must be converted to local Cartesian
   ``(x_gps, y_gps)`` using a fixed reference origin. The measurement
   model is:

   .. math::

      \mathbf{z}_k = \mathbf{H} \mathbf{x}_k + \mathbf{v}_k, \quad
      \mathbf{H} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \end{bmatrix}

   **Subscriptions:**

   - ``/carla/imu/data`` -- ``sensor_msgs/Imu``
   - ``/carla/gnss/fix`` -- ``sensor_msgs/NavSatFix``

   **Publications:**

   - ``/localization/pose`` -- ``geometry_msgs/PoseStamped``
   - ``/localization/odom`` -- ``nav_msgs/Odometry``

   **Parameters (configurable via** ``ekf_config.yaml`` **):**

   .. code-block:: yaml

      ekf_node:
        ros__parameters:
          # Process noise covariance Q (diagonal entries)
          q_x: 0.1        # position uncertainty per step (m^2)
          q_y: 0.1
          q_theta: 0.01   # heading uncertainty (rad^2)
          q_v: 0.5        # speed uncertainty (m^2/s^2)
          # Measurement noise covariance R (GNSS, diagonal entries)
          r_x: 1.0        # GNSS x noise (m^2)
          r_y: 1.0        # GNSS y noise (m^2)
          # GNSS reference origin (set from first fix)
          gnss_origin_lat: 0.0
          gnss_origin_lon: 0.0

   **EKF template usage:**

   .. code-block:: python

      from ekf_template import EKFBase
      import numpy as np

      class VehicleEKF(EKFBase):
          """Concrete EKF for bicycle model + GNSS update."""

          def __init__(self, Q, R):
              # State: [x, y, theta, v]
              x0 = np.zeros(4)
              P0 = np.eye(4) * 1.0
              super().__init__(x0, P0, Q, R)

          def f(self, x, u, dt):
              """Non-linear process model. u = [omega] (IMU yaw rate)."""
              omega = u[0]
              x_new = np.array([
                  x[0] + x[3] * np.cos(x[2]) * dt,
                  x[1] + x[3] * np.sin(x[2]) * dt,
                  x[2] + omega * dt,
                  x[3]   # constant velocity assumption
              ])
              return x_new

          def F_jacobian(self, x, u, dt):
              """Jacobian of f w.r.t. state x."""
              F = np.eye(4)
              F[0, 2] = -x[3] * np.sin(x[2]) * dt  # df_x / d_theta
              F[0, 3] =  np.cos(x[2]) * dt           # df_x / dv
              F[1, 2] =  x[3] * np.cos(x[2]) * dt   # df_y / d_theta
              F[1, 3] =  np.sin(x[2]) * dt           # df_y / dv
              return F

          def h(self, x):
              """Measurement model: observe (x, y) from GNSS."""
              return x[:2]

          def H_jacobian(self, x):
              """Jacobian of h w.r.t. state x."""
              H = np.zeros((2, 4))
              H[0, 0] = 1.0
              H[1, 1] = 1.0
              return H

   .. warning::

      Normalize ``theta`` to ``[-pi, pi]`` after every prediction and update
      step. Angle wraparound is the most common source of EKF divergence in
      student implementations.

.. dropdown:: Task 3: Evaluation (20 pts)
   :icon: gear
   :class-container: sd-border-primary

   Quantitatively evaluate both the fusion and localization components.

   **3.1 -- Fusion Evaluation**

   Use ``ground_truth_logger.py`` (provided) to record CARLA ground-truth
   3D object positions at each timestep. Compare against your
   ``/perception/fused_objects`` output.

   For each object class (vehicle, pedestrian, cyclist), compute:

   - **Mean 3D Position Error (m):** Euclidean distance between fused
     centroid and ground-truth centroid, averaged over all matched detections.
   - **Match rate (%):** Fraction of ground-truth objects that have at least
     one fused detection within 2 m.

   Report results in a table per class:

   .. code-block:: python

      import numpy as np

      def mean_3d_position_error(fused_positions, gt_positions):
          """
          fused_positions, gt_positions: list of np.ndarray shape (3,)
          Returns mean Euclidean error in metres.
          """
          errors = [np.linalg.norm(f - g)
                    for f, g in zip(fused_positions, gt_positions)]
          return np.mean(errors), np.std(errors)

   **3.2 -- Localization Evaluation**

   Use the provided ``evaluate_localization.py`` script:

   .. code-block:: bash

      # Record EKF output and ground truth to CSV first, then:
      python evaluate_localization.py \
          --est  ekf_trajectory/ekf_pose.csv \
          --ref  ground_truth/gt_pose.csv \
          --plot evaluation/plots/

   The script reports:

   - **APE (Absolute Pose Error):** RMSE of position error over entire run.
   - **RPE (Relative Pose Error):** Mean error over fixed-length sub-segments.
   - Trajectory overlay plot and error-over-time plot.

   **3.3 -- Multi-Town Testing**

   Run your full GP3 pipeline (sensors + detection + fusion + EKF) in at
   least **two CARLA towns** with different road layouts and conditions
   (e.g., Town01 and Town05). Report evaluation metrics for each town
   separately and discuss differences.

   .. important::

      Include **all evaluation CSV files and generated plots** in your
      submission under ``evaluation/``. The grader will re-run
      ``evaluate_localization.py`` to verify your reported numbers.

.. dropdown:: Task 4: LiDAR Odometry -- Bonus (10 pts)
   :icon: gear
   :class-container: sd-border-primary

   Implement ICP (Iterative Closest Point) scan matching as an additional
   localization measurement source and fuse it into the EKF.

   **Requirements:**

   1. Implement ``lidar_odometry_node.py`` that subscribes to
      ``/carla/lidar/points`` and publishes relative pose increments on
      ``/localization/lidar_odom_delta`` using ICP between consecutive scans.
      You may use ``open3d.pipelines.registration.registration_icp`` or
      ``scikit-learn``'s nearest-neighbor routines.

   2. Add a second EKF update step in ``localization_node.py`` that
      ingests the LiDAR odometry delta as an additional measurement
      ``z_lidar = [dx, dy, dtheta]``.

   3. Compare localization APE **with and without** LiDAR odometry fusion
      and report the reduction in error.

   .. code-block:: python

      import open3d as o3d

      def icp_scan_match(source_pts, target_pts, threshold=0.5):
          """
          Estimate rigid transform T aligning source -> target using ICP.
          Returns 4x4 transform matrix.
          """
          src = o3d.geometry.PointCloud()
          src.points = o3d.utility.Vector3dVector(source_pts)
          tgt = o3d.geometry.PointCloud()
          tgt.points = o3d.utility.Vector3dVector(target_pts)

          result = o3d.pipelines.registration.registration_icp(
              src, tgt, threshold,
              np.eye(4),
              o3d.pipelines.registration.TransformationEstimationPointToPoint()
          )
          return result.transformation

   .. note::

      ICP scan matching can be slow on dense point clouds. Downsample to
      a voxel grid (e.g., 0.2 m) before running ICP to keep the update
      rate above 5 Hz.

.. dropdown:: Task 5: Report (15 pts)
   :icon: gear
   :class-container: sd-border-primary

   Write a **4--5 page technical report** (PDF, double-column preferred)
   covering the following sections. Use your own words -- do not copy
   template text.

   **Required Sections:**

   1. **Architecture Diagram** -- Draw the full ROS 2 node and topic graph
      for your GP3 pipeline. Show all nodes (from GP1, GP2, and GP3),
      all topics, and data flow directions. Tools: ``rqt_graph``, draw.io,
      or PlantUML.

   2. **EKF Formulation** -- Present the mathematical formulation:
      state vector definition, process model ``f(x, u)``, Jacobian ``F``,
      measurement model ``h(x)``, Jacobian ``H``, and noise matrices ``Q``
      and ``R``. Show the full predict/update equations.

   3. **Quantitative Results** -- Tables and plots:

      - Fusion: mean 3D position error per class (Town01, Town05)
      - Localization: APE and RPE (Town01, Town05)
      - EKF trajectory overlay plot

   4. **Error Analysis** -- When does fusion fail? (Occlusion? Long range?
      Adverse weather?) When does the EKF drift? (Sharp turns? GNSS outage?)
      Support your analysis with specific timestamped examples from your
      evaluation data.

   5. **Conclusion** -- Key lessons learned and identified improvements.

   .. tip::

      Use ``rqt_graph`` to auto-generate a screenshot of your node/topic
      graph and annotate it in a drawing tool. This is the fastest way to
      produce a clean architecture diagram.


Folder Structure
----------------

Your submission must follow this exact directory layout:

.. code-block:: text

   GP3_Team{X}/
   ├── ads_pipeline/              # Extended from GP2
   │   ├── ads_pipeline/
   │   │   ├── __init__.py
   │   │   ├── sensor_manager.py     # From GP1
   │   │   ├── detector_node.py      # From GP2
   │   │   ├── fusion_node.py        # NEW
   │   │   ├── localization_node.py  # NEW
   │   │   ├── ekf_template.py       # Provided (copied here)
   │   │   └── fusion_utils.py       # Provided (copied here)
   │   ├── config/
   │   │   ├── carla_config.yaml     # Updated with fusion params
   │   │   ├── detector_config.yaml  # From GP2
   │   │   └── ekf_config.yaml       # NEW
   │   ├── launch/
   │   │   ├── sensors_launch.py     # From GP1
   │   │   ├── perception_launch.py  # From GP2
   │   │   └── fusion_launch.py      # NEW
   │   ├── models/                   # From GP2 (YOLO/DETR weights)
   │   ├── package.xml
   │   └── setup.py
   ├── evaluation/
   │   ├── ground_truth/             # CSV files from ground_truth_logger
   │   ├── ekf_trajectory/           # CSV files of EKF pose estimates
   │   ├── fusion_results/           # Per-class 3D error CSVs
   │   └── plots/                    # Trajectory and error plots (PNG/PDF)
   └── report.pdf

Replace ``{X}`` with your team number (e.g., ``GP3_Team3``).


Submission
----------

.. important::

   **Submission Instructions**

   Submit a single ``.zip`` archive named ``GP3_TeamX.zip`` (replace ``X``
   with your team number) to **Canvas** by the deadline.

   - **Deadline:** End of Week 11 (see Canvas for exact date/time)
   - **Late policy:** 10% deduction per day, maximum 3 days late
   - **One submission per team** -- designate one member to submit
   - Include **all** evaluation files, plots, and ``report.pdf`` inside the archive
   - Your ``ads_pipeline`` package must build cleanly with
     ``colcon build --packages-select ads_pipeline``

   Canvas submissions only. Email submissions will not be graded.


Submission Checklist
--------------------

.. admonition:: Before You Submit -- Check Every Item
   :class: tip

   - [ ] ``fusion_node.py`` runs and publishes ``/perception/fused_objects``
   - [ ] ``localization_node.py`` runs and publishes ``/localization/pose``
         and ``/localization/odom``
   - [ ] ``fusion_launch.py`` launches all GP3 nodes together with GP1 and GP2
   - [ ] ``ekf_config.yaml`` is present and loaded by the launch file
   - [ ] Evaluation CSVs are present in ``evaluation/ground_truth/`` and
         ``evaluation/ekf_trajectory/``
   - [ ] Evaluation plots are present in ``evaluation/plots/``
   - [ ] Results tested in at least 2 CARLA towns
   - [ ] ``report.pdf`` is present, 4--5 pages, includes architecture diagram
         and EKF formulation
   - [ ] ``colcon build`` succeeds with no errors
   - [ ] Folder is named ``GP3_TeamX/`` (correct team number)
   - [ ] Archive is named ``GP3_TeamX.zip``
   - [ ] Peer evaluation form submitted on Canvas separately


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Component
     - Points
     - Criteria
   * - Camera-LiDAR Fusion
     - 30
     - Frustum association implemented correctly; ``Detection3DArray``
       published on correct topic; occlusion/range edge cases handled;
       works with both YOLO and DETR outputs; 3D position error < 1.5 m
       on average for vehicles.
   * - EKF Localization
     - 35
     - State vector correct; prediction step uses bicycle model; Jacobian
       ``F`` analytically derived; GNSS update step implemented; ``Q``
       and ``R`` configurable via parameters; heading normalization
       applied; APE < 2.0 m in Town01 straight roads.
   * - Evaluation
     - 20
     - Fusion 3D error table with per-class breakdown; APE and RPE
       reported; trajectory overlay plot; error-over-time plot; at least
       2 towns tested; ``evaluate_localization.py`` re-runs successfully
       on submitted CSVs.
   * - Report
     - 15
     - Architecture diagram shows all nodes and topics; EKF formulation
       section includes ``f``, ``F``, ``h``, ``H``, ``Q``, ``R``;
       quantitative tables match submitted CSVs; error analysis discusses
       specific failure cases; 4--5 pages.
   * - LiDAR Odometry (Bonus)
     - +10
     - ICP scan matching implemented and publishing delta poses; second
       EKF update step consumes LiDAR odometry; APE reduction
       demonstrated quantitatively.


Common Mistakes
---------------

.. danger::

   **Avoid These Common Errors**

   - **Forgetting to convert GNSS to Cartesian.** Raw ``(lat, lon)``
     cannot be used directly as EKF measurements. You must convert to a
     local Cartesian frame using a fixed reference origin. Use
     ``pyproj.Transformer`` or the haversine formula.

   - **Not normalizing heading.** After every EKF predict/update step,
     wrap ``theta`` to ``[-pi, pi]``. Failure to do this causes the EKF
     to diverge on long runs with turns.

   - **Ignoring time synchronization.** Fusing a LiDAR cloud from time
     ``t-0.5s`` with a detection at time ``t`` produces incorrect
     associations. Cache the most recent cloud with its timestamp and
     warn if the age exceeds 100 ms.

   - **Hardcoding calibration values.** Camera intrinsics ``K`` and the
     camera-to-LiDAR extrinsic ``T_cl`` must be loaded from config, not
     hardcoded. Different CARLA vehicle setups have different calibrations.

   - **Publishing an empty** ``Detection3DArray`` **on no detections.**
     Always publish the message (even if empty) so downstream nodes
     do not stall waiting for their first message.

   - **Submitting without evaluation files.** The grader needs your
     trajectory CSVs to re-run ``evaluate_localization.py``. Missing
     files result in zero points for the evaluation component.

   - **Copying EKF code without understanding it.** You must be able to
     explain every line of your EKF during office hours or the final
     presentation. The template is a scaffold -- the math is yours to fill in.


Tips for Success
----------------

.. tip::

   **Set up the pipeline incrementally.** First verify that
   ``/carla/lidar/points`` is publishing in RViz before writing the
   fusion node. Then test frustum projection on a static scene before
   running with the full detection pipeline.

.. tip::

   **Tune Q and R empirically.** Start with large ``R`` (low trust in
   GNSS) and reduce it once your prediction step is verified. A good
   sanity check: set ``Q = 0`` and ``R = 0`` and confirm the filter
   runs at sensor rate without crashing before adding noise.

.. tip::

   **Use RViz for visual debugging.** Publish the LiDAR frustum points
   as a ``sensor_msgs/PointCloud2`` on a debug topic to verify that
   your frustum association is selecting the right points. Visualize
   the EKF pose as a ``PoseStamped`` arrow in RViz alongside the
   CARLA ground-truth pose.

.. tip::

   **Divide the work clearly.** A natural split: one member on
   ``fusion_node.py``, one on ``localization_node.py``, one on
   evaluation scripts and plots, one on the report. All members
   should understand all components before submission.

.. tip::

   **Test in Town05 early.** Town05 has more complex intersections and
   varying road widths than Town01. EKF drift tends to be larger in
   Town05 due to sharper turns -- leave time to retune ``Q`` before the
   deadline.
