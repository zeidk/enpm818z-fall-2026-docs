====================================================
Lecture
====================================================


The Localization Problem
-------------------------

.. admonition:: Core Question
   :class: note

   **"Where am I?"** -- Autonomous vehicles need to know their pose
   (position + orientation) in a global or local reference frame with
   sufficient accuracy and reliability to plan safe trajectories.

Required accuracy varies by task:

.. list-table::
   :widths: 35 25 40
   :header-rows: 1
   :class: compact-table

   * - Task
     - Required accuracy
     - Method
   * - Highway lane keeping
     - ~20 cm lateral
     - GPS + IMU + map
   * - Urban lane-level routing
     - ~10 cm lateral
     - RTK-GPS or LiDAR scan matching
   * - Parking slot detection
     - ~5 cm
     - LiDAR SLAM or HD map matching
   * - High-speed overtaking
     - ~10 cm (velocity critical)
     - RTK + IMU tight coupling

Coordinate Systems and Transformations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AV systems use a hierarchy of coordinate frames. Understanding transforms
between them is fundamental.

.. list-table::
   :widths: 20 80
   :class: compact-table

   * - **WGS84**
     - World Geodetic System 1984. GPS coordinates: latitude, longitude,
       altitude. Ellipsoidal model of the Earth.
   * - **ENU / NED**
     - Local Cartesian frames: East-North-Up or North-East-Down. Centered
       at a reference GPS point. Units: meters.
   * - **Map frame**
     - Arbitrary origin fixed during operation. HD map coordinates live here.
   * - **Odom frame**
     - Continuous odometry origin. Drifts over time but smooth short-term.
   * - **Base link**
     - Vehicle body frame. Origin at vehicle center (or rear axle center).
   * - **Sensor frames**
     - Each sensor has its own frame. Extrinsic calibration defines the
       transform to base link.

A rigid body transform between frames :math:`A` and :math:`B` is a
**homogeneous transformation matrix**:

.. math::

   T_{AB} = \begin{bmatrix} R_{AB} & t_{AB} \\ 0 & 1 \end{bmatrix} \in SE(3)

where :math:`R_{AB} \in SO(3)` is a :math:`3 \times 3` rotation matrix and
:math:`t_{AB} \in \mathbb{R}^3` is a translation vector.


GNSS-Based Localization
------------------------

GPS / GNSS Fundamentals
~~~~~~~~~~~~~~~~~~~~~~~~

Global Navigation Satellite Systems (GNSS) include GPS (US), GLONASS (Russia),
Galileo (EU), and BeiDou (China). The receiver computes position by measuring
**pseudoranges** to multiple satellites:

.. math::

   \rho_i = \| \mathbf{p}_{sat,i} - \mathbf{p}_{recv} \| + c \cdot \delta t + \epsilon_i

where :math:`\mathbf{p}_{sat,i}` is the known satellite position,
:math:`\mathbf{p}_{recv}` is the unknown receiver position, :math:`c` is
the speed of light, :math:`\delta t` is clock offset, and :math:`\epsilon_i`
includes atmospheric delays and multipath errors.

Standard GPS accuracy: **1-5 meters** (civilian L1 signal). Not sufficient
for AV lane-level localization.

RTK-GPS (Real-Time Kinematic)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RTK uses a **base station** at a precisely known location to compute and
broadcast correction signals in real time. The rover receiver applies these
corrections to resolve carrier-phase ambiguities.

.. tab-set::

   .. tab-item:: How RTK Works

      1. Base station measures carrier phase of GPS signals.
      2. Computes corrections (residual errors).
      3. Broadcasts corrections via radio or internet (NTRIP protocol).
      4. Rover applies corrections and resolves integer ambiguities.
      5. Result: centimeter-level positioning (1-2 cm horizontal, 2-5 cm vertical).

   .. tab-item:: Limitations

      - Requires base station within ~20-50 km.
      - Initialization ("fixing") takes 30-120 seconds.
      - Performance degrades in urban canyons (multipath from buildings).
      - No satellite signal in tunnels, underground parking.

PPP (Precise Point Positioning)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PPP uses precise satellite orbit and clock corrections broadcast globally
(no local base station needed). Accuracy: ~5-10 cm after convergence (30-60
minutes). Used for offline post-processing and emerging real-time services
(PPP-RTK targets cm-level in <1 minute).

.. admonition:: AV Reality
   :class: warning

   GNSS alone is insufficient for production AV systems because of urban
   canyon multipath, tunnel outages, and multipath interference. GNSS
   provides the global reference frame; other sensors (LiDAR, IMU) maintain
   accuracy when GNSS is unreliable.


Dead Reckoning
---------------

Dead reckoning estimates the current pose by integrating motion measurements
from the prior known pose, without requiring external reference.

:math:`\hat{\mathbf{x}}_k = \hat{\mathbf{x}}_{k-1} \oplus \Delta \mathbf{x}_k`

where :math:`\oplus` denotes pose composition in SE(3) and :math:`\Delta \mathbf{x}_k`
is the incremental motion estimate.

Wheel Odometry
~~~~~~~~~~~~~~~

Integrates wheel encoder measurements to estimate 2D pose. **The model
must match the vehicle**, and cars are not differential-drive robots.

.. tab-set::

   .. tab-item:: Ackermann (cars) -- use this one

      A passenger car steers its front wheels and cannot change heading
      without moving forward. Heading rate comes from the **steering
      angle** via the bicycle model (L10), not from a left/right wheel
      speed difference:

      .. math::

         \Delta d &= \frac{\Delta d_{RL} + \Delta d_{RR}}{2}
           \quad \text{(rear wheels: undriven by steering)} \\
         \Delta \theta &= \frac{\Delta d}{L_{wb}} \tan \delta

      where :math:`L_{wb}` is the wheelbase (front axle to rear axle) and
      :math:`\delta` is the road-wheel steering angle. Integration then
      uses the midpoint heading:

      .. math::

         x_{k+1} &= x_k + \Delta d \cos(\theta_k + \Delta\theta/2) \\
         y_{k+1} &= y_k + \Delta d \sin(\theta_k + \Delta\theta/2) \\
         \theta_{k+1} &= \theta_k + \Delta\theta

      In practice the yaw rate is taken from the **IMU gyroscope**
      instead, which is far more accurate than differentiating a
      steering-angle sensor.

   .. tab-item:: Differential drive (not cars)

      For a two-wheeled robot that steers by driving its wheels at
      different speeds:

      .. math::

         \Delta d = \frac{\Delta d_L + \Delta d_R}{2}, \quad
         \Delta \theta = \frac{\Delta d_R - \Delta d_L}{b}

      where :math:`b` is the **track width** between the two wheels.

      .. warning::

         This model appears in most robotics textbooks and is wrong for
         a car. On an Ackermann vehicle the left/right rear wheel speed
         difference during a turn is a small geometric side-effect, not
         the steering input, and it vanishes entirely when driving
         straight. Applying this formula to a car gives a heading
         estimate dominated by tyre-radius mismatch and noise.

**Error sources**: wheel slip (especially on turns, wet roads), uneven terrain
(suspension deflection changes wheel-ground contact), encoder resolution,
and tyre radius changing with load, temperature, and pressure.

**Drift behaviour**: distance error grows roughly linearly with distance
travelled, but a *heading* bias causes position error to grow
**quadratically** -- which is why a small uncorrected yaw error is far
more damaging than a scale error.

Visual Odometry (VO)
~~~~~~~~~~~~~~~~~~~~~~

Estimates camera motion by tracking/matching feature points across consecutive
frames:

1. Detect keypoints (ORB, SIFT, SuperPoint).
2. Match keypoints between frames.
3. Compute the essential matrix :math:`E` using RANSAC.
4. Decompose :math:`E = [\mathbf{t}]_\times R` to recover rotation and
   (scale-ambiguous) translation, where :math:`[\mathbf{t}]_\times` is the
   skew-symmetric matrix of the translation vector:

   .. math::

      [\mathbf{t}]_\times = \begin{bmatrix}
        0 & -t_z & t_y \\ t_z & 0 & -t_x \\ -t_y & t_x & 0
      \end{bmatrix}

   The decomposition yields **four** candidate :math:`(R, \mathbf{t})`
   solutions; the correct one is selected by the cheirality check --
   requiring triangulated points to lie in front of both cameras.
5. (Stereo VO) Use the stereo baseline to recover metric scale.

**Monocular VO**: scale-ambiguous; scale drift over long sequences.
**Stereo VO**: metric scale recovered from baseline; drift ~0.5-1% of distance.

LiDAR Odometry
~~~~~~~~~~~~~~~

Estimates motion by matching consecutive LiDAR scans (see ICP below).
**Drift**: ~0.1-0.5% of distance for state-of-the-art systems (LOAM).
Higher accuracy than VO due to direct 3D metric measurements.

Drift Comparison
~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 25 25 20
   :header-rows: 1
   :class: compact-table

   * - Method
     - Typical drift
     - Frequency
     - 3D?
   * - Wheel odometry
     - 1-5% of distance
     - 100-1000 Hz
     - No (2D)
   * - Visual odometry (mono)
     - 0.5-2% (scale drift)
     - 10-30 Hz
     - Yes
   * - Visual odometry (stereo)
     - 0.5-1%
     - 10-30 Hz
     - Yes
   * - LiDAR odometry
     - 0.1-0.5%
     - 10-20 Hz
     - Yes
   * - IMU (integrated)
     - Diverges in seconds
     - 100-1000 Hz
     - Yes


Probabilistic Localization
---------------------------

Rather than a single pose estimate, probabilistic localization maintains a
**belief** -- a probability distribution over possible poses.

EKF Localization
~~~~~~~~~~~~~~~~~

Given a known map of landmarks :math:`m = \{m_1, \ldots, m_N\}`:

1. **Predict**: propagate pose estimate using motion model (wheel odometry or
   IMU).
2. **Update**: when a landmark is observed, compute expected observation
   :math:`h(\mathbf{x}, m_j)` and update using the EKF equations from
   :doc:`L3 </lectures/lecture3/l3_index>`.

The observation function :math:`h` is typically nonlinear (e.g., range-bearing
to a known landmark), requiring the EKF's Jacobian linearization.

MCL: Monte Carlo Localization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Prerequisite Recap (ENPM673)
   :class: note

   In ENPM673, you implemented a particle filter for robot localization
   (predict with motion model, weight by sensor likelihood, resample).
   MCL (also called AMCL) applies this same algorithm to AV pose estimation
   using LiDAR scans against a reference map.

**LiDAR Sensor Model.** The sensor update step scores each particle by how
well the vehicle's actual LiDAR scan matches a simulated scan from that
particle's hypothesized pose. The map-based sensor model works as follows:

1. For each particle, perform **ray-casting** against a 2D occupancy grid or
   3D voxel map to compute the expected scan from that pose.
2. Compare the expected scan to the actual scan using a likelihood function
   (e.g., beam model with Gaussian noise, or likelihood field model that
   queries the distance to the nearest obstacle for each measured endpoint).
3. Assign the particle a weight proportional to the scan match score.

**Adaptive Particle Count (KLD-Sampling).** Standard MCL uses a fixed number
of particles :math:`N`. AMCL adjusts :math:`N` dynamically using
**KLD-sampling** (Kullback-Leibler divergence sampling):

- When the particle distribution is converged (vehicle well-localized), fewer
  particles are needed -- :math:`N` shrinks, reducing CPU load.
- When the distribution is spread out (high uncertainty, e.g., after
  initialization or GPS dropout), :math:`N` grows to cover the hypothesis
  space adequately.
- The bound is derived from the KL divergence between the true posterior and
  the sample-based approximation, guaranteeing a maximum approximation error
  with probability :math:`1 - \delta`.

**Operating Modes.**

- **Global localization**: particles are initialized uniformly across the
  entire map. The filter converges to the correct pose as scans accumulate.
  Required at startup when no GPS prior is available.
- **Pose tracking**: particles are initialized around a known pose (e.g., from
  GPS). The filter tracks incremental motion. Much faster convergence.
- A small fraction of random particles can be injected each cycle to enable
  **kidnapped robot recovery** -- detecting and recovering from sudden
  relocations (e.g., a localization failure after passing through a tunnel).

**Integration with ROS 2 Nav2.** The ``nav2_amcl`` package provides a
production-ready AMCL implementation for the ROS 2 navigation stack:

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Input**
     - 2D laser scan (``sensor_msgs/LaserScan``), odometry, and a 2D
       occupancy grid map (``nav_msgs/OccupancyGrid``)
   * - **Output**
     - Corrected pose as the ``map`` → ``odom`` transform on ``/tf``
   * - **Key parameters**
     - ``min_particles`` / ``max_particles`` (KLD bounds),
       ``laser_model_type`` (beam or likelihood field),
       ``recovery_alpha_slow`` / ``recovery_alpha_fast`` (random particle
       injection rates for kidnapped-robot recovery)

Key advantage: MCL handles the **global localization** problem (starting
without a prior pose) and recovers from **kidnapped robot** scenarios
(sudden relocation), which EKF cannot.


Map-Based Localization
-----------------------

Scan Matching with ICP
~~~~~~~~~~~~~~~~~~~~~~~

**Iterative Closest Point (ICP)** is the core algorithm for aligning a
source point cloud :math:`\mathcal{P}` to a target point cloud :math:`\mathcal{Q}`:

.. math::

   T^* = \argmin_{T} \sum_{i} \| q_i - T p_i \|^2

where :math:`(p_i, q_i)` are corresponding point pairs. ICP alternates between:

1. **Correspondence**: find nearest neighbor in :math:`\mathcal{Q}` for each
   point in :math:`T \cdot \mathcal{P}`.
2. **Minimize**: solve for the optimal rigid transform using SVD (the
   Kabsch algorithm):

   .. math::

      [U, S, V^T] = \text{SVD}(H) \quad \text{where } H = \sum_i (p_i - \bar{p})(q_i - \bar{q})^T

      R = V D U^T, \quad t = \bar{q} - R \bar{p}

   where :math:`D = \text{diag}(1, 1, \det(VU^T))`.

   .. warning::

      The :math:`D` term is not optional. Without it, degenerate or
      noisy correspondences can produce a matrix with
      :math:`\det = -1` -- a **reflection** rather than a rotation. It
      minimizes the cost function perfectly while describing a physically
      impossible motion, and it is a classic silent ICP failure.

3. **Update**: apply transform and check convergence.

ICP Variants
~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Variant
     - Improvement
   * - **Point-to-plane ICP**
     - Minimizes distance from source point to target surface (normal).
       Converges ~10x faster than point-to-point.
   * - **NDT (Normal Distributions Transform)**
     - Represents target cloud as a grid of Gaussians. Robust to outliers,
       no explicit correspondences needed. Used in Autoware.
   * - **GICP (Generalized ICP)**
     - Treats both clouds as Gaussians; maximum likelihood formulation.
       More robust and accurate than standard ICP.

HD Map Localization
~~~~~~~~~~~~~~~~~~~~

HD (High-Definition) maps contain centimeter-accurate road geometry, lane
markings, signs, and semantic features. The vehicle localizes by matching
current sensor observations to the HD map:

1. LiDAR scan → extract lane markings, curbs, poles.
2. Match extracted features to HD map features.
3. Compute 6-DoF pose correction.
4. Fuse with GNSS and IMU via EKF.

**Advantages**: globally consistent, no accumulated drift.
**Disadvantages**: HD maps cost millions to create and maintain; they go stale
(road construction, seasonal changes). Requires prior map of the operating area.


SLAM Problem Formulation
--------------------------

In SLAM, the vehicle simultaneously estimates its trajectory and builds a
map from scratch -- no prior map is assumed.

.. math::

   p(\mathbf{x}_{0:t}, m \mid \mathbf{z}_{1:t}, \mathbf{u}_{1:t})

where:

- :math:`\mathbf{x}_{0:t}` -- vehicle trajectory (sequence of poses)
- :math:`m` -- map (set of landmarks, point cloud, or dense voxel map)
- :math:`\mathbf{z}_{1:t}` -- all measurements (LiDAR scans, image features)
- :math:`\mathbf{u}_{1:t}` -- all control inputs (odometry)

The chicken-and-egg problem: accurate mapping requires knowing the pose;
accurate pose estimation requires knowing the map.

.. admonition:: SLAM is the AV chicken-and-egg
   :class: note

   HD map localization requires a pre-built HD map. But building that HD map
   required SLAM. In practice: SLAM is used offline to build maps; HD map
   localization is used online during operation.


SLAM Frontend
--------------

The frontend processes raw sensor data to produce odometry estimates and
detect loop closures.

Scan Acquisition and Preprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **Motion distortion**
     - LiDAR scans take 50-100 ms to complete. During this time, the vehicle
       moves. Each point is captured at a slightly different vehicle pose.
       IMU data is used to de-skew the scan -- correcting each point to the
       pose at the scan start time.
   * - **Ground removal**
     - Remove points belonging to the ground plane (RANSAC plane fitting).
       Reduces data and avoids matching ground points across scans.
   * - **Downsampling**
     - Voxel grid filter: retain one point per voxel. Reduces compute while
       preserving structure.
   * - **Range filtering**
     - Remove points beyond useful range (e.g., > 80 m) and very close range
       (< 0.5 m) artifacts.

Feature Extraction
~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Edge Features (LOAM)

      Points with large **curvature** values lie on edges (corners, poles).
      Computed as:

      .. math::

         c = \frac{1}{|S| \cdot \|p_i\|} \left\| \sum_{j \in S, j \neq i} (p_j - p_i) \right\|

      High curvature → edge feature. Low curvature → planar feature.

   .. tab-item:: Planar Features (LOAM)

      Points with **small curvature** lie on flat surfaces (walls, ground).
      Selected from each scan ring as the points with minimum curvature.

   .. tab-item:: 3D Descriptors

      For place recognition and loop closure: FPFH, SHOT, or learned
      descriptors (FCGF, D3Feat). Encode local geometry around each keypoint
      into a descriptor vector.

ICP-Based Scan-to-Scan Matching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The frontend matches each new scan to the previous scan (scan-to-scan) or
to a local map (scan-to-map):

.. code-block:: text

   # Pseudocode: LOAM-style frontend
   for each new_scan:
       # 1. Preprocessing
       new_scan = remove_motion_distortion(new_scan, imu_data)
       new_scan = voxel_downsample(new_scan, voxel_size=0.2)

       # 2. Feature extraction
       edges, planes = extract_loam_features(new_scan)

       # 3. Scan matching (edge-to-edge, plane-to-plane)
       T_delta = icp_feature_match(edges, planes, local_map)

       # 4. Update pose estimate
       current_pose = current_pose @ T_delta

       # 5. Keyframe selection
       if is_keyframe(T_delta):
           add_keyframe(current_pose, new_scan)
           update_local_map()

Keyframe Strategy
~~~~~~~~~~~~~~~~~~

Not every scan is a keyframe. Keyframes are selected when the vehicle has
moved sufficiently (e.g., >0.5 m or >10 deg rotation from the last keyframe).

- **Too frequent**: high memory use, backend overwhelmed.
- **Too sparse**: large gaps in map coverage, ICP initialization failures.


SLAM Backend
-------------

The backend refines the entire trajectory and map globally by solving a
**pose graph optimization** problem.

Pose Graph Formulation
~~~~~~~~~~~~~~~~~~~~~~~

A **pose graph** has:

- **Nodes**: :math:`x_i \in SE(3)` -- the estimated pose at each keyframe.
- **Edges**: constraints between poses. Each edge :math:`(i, j)` represents
  a relative pose measurement :math:`z_{ij}` with information matrix
  :math:`\Omega_{ij}`:

.. math::

   F = \sum_{(i,j) \in \mathcal{E}} e_{ij}^T \Omega_{ij} e_{ij}

   e_{ij} = \text{Log}(T_{ij}^{-1} \cdot x_i^{-1} \cdot x_j)

where :math:`\text{Log}` is the Lie algebra logarithm that converts an SE(3)
transform to a 6D vector. Minimizing F gives the maximum likelihood trajectory.

This is solved with **nonlinear least squares** (Gauss-Newton or Levenberg-
Marquardt), implemented in libraries like g2o, GTSAM, and Ceres Solver.

Loop Closure Detection
~~~~~~~~~~~~~~~~~~~~~~~

Without loop closure, SLAM drift accumulates without bound. Loop closure
detects when the vehicle **revisits a previously mapped area** and adds a
long-range edge to the pose graph, correcting accumulated drift globally.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Detection (Place Recognition)
      :class-card: sd-border-info

      Match current scan against all previous keyframes using:

      - **Scan context** (Kim & Kim, 2018): compact 2D histogram encoding
        of the 3D scene structure. Fast retrieval via KD-tree.
      - **FPFH descriptors + RANSAC**: geometric verification.
      - **Neural: PointNetVLAD, MinkLoc3D**: learned place recognition.

   .. grid-item-card:: Verification (Geometric)
      :class-card: sd-border-info

      Once a candidate loop is found, verify with ICP. Accept only if
      ICP converges to a consistent transform with low residual error.

      Reject false positives: use a minimum overlap threshold and a
      maximum residual threshold.

.. admonition:: Why Loop Closure Matters
   :class: important

   Odometry drift is **unbounded**: at ~0.5% translational drift, 100 m
   of driving accumulates ~0.5 m of error and 1 km accumulates ~5 m --
   already unusable for lane-level driving, and it keeps growing.

   A correct loop closure adds a constraint saying "these two poses are
   the same place." The optimizer then distributes the accumulated error
   backwards across the whole loop, so drift becomes **bounded by the
   loop-closure constraint's own accuracy** (typically a few centimetres
   to tens of centimetres, set by the ICP registration quality) rather
   than growing with distance travelled.

   .. warning::

      Loop closure bounds error; it does not eliminate it. Claims of
      "sub-centimetre after loop closure" are not achievable in practice
      -- the corrected trajectory is only as good as the registration
      that produced the constraint. And a **false** loop closure is far
      worse than none at all: it warps the entire map irrecoverably,
      which is why geometric verification is mandatory before accepting
      a candidate.


SLAM Evaluation Metrics
------------------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Metric
     - Definition
     - Notes
   * - **APE**
     - Absolute Pose Error: RMSE between estimated and ground-truth poses
       at each timestep
     - Global accuracy; sensitive to loop closure quality
   * - **RPE**
     - Relative Pose Error: RMSE of relative transforms over a fixed
       interval (e.g., 100 m)
     - Local accuracy; measures odometry drift rate
   * - **Map consistency**
     - Overlap IoU of map with ground-truth HD map or aerial survey
     - End-to-end mapping quality
   * - **Runtime**
     - Processing time per scan (Hz)
     - Must exceed sensor rate (>10 Hz for 10 Hz LiDAR)

The **EVO** tool provides standardized APE/RPE computation from trajectory
files in TUM, KITTI, and ROS bag formats.


Modern LiDAR SLAM Systems
--------------------------

.. tab-set::

   .. tab-item:: LOAM (2014)

      **LiDAR Odometry and Mapping** (Zhang & Singh, RSS 2014).

      - Frontend: edge + planar feature extraction and matching (scan-to-map).
      - Backend: none (no pose graph, no loop closure).
      - Performance: ~0.55% average translational error on the KITTI
        odometry benchmark -- the top-ranked method at publication.
        (KITTI scores odometry as *relative* translation/rotation error
        over 100--800 m sub-sequences, expressed as a percentage; it does
        not report an absolute pose error in centimetres.)
      - Limitation: drift accumulates without loop closure; memory grows unbounded.
      - Legacy: LOAM's feature extraction approach inspired all later systems.

   .. tab-item:: LeGO-LOAM (2018)

      **Lightweight and Ground-Optimized LOAM** (Shan & Englot, IROS 2018).

      - Adds explicit ground segmentation before feature extraction.
      - Two-step optimization: ground plane features first (z, roll, pitch),
        then edge features (x, y, yaw).
      - Pose graph backend with loop closure.
      - Designed for ground vehicles; 30% compute reduction vs. LOAM.
      - Widely used in AV research and robotics competitions.

   .. tab-item:: LIO-SAM (2020)

      **Tightly-Coupled LiDAR Inertial Odometry via Smoothing and Mapping**
      (Shan et al., IROS 2020).

      - Tightly couples IMU pre-integration with LiDAR scan matching.
      - Factor graph backend (GTSAM): LiDAR, IMU, GPS, and loop closure
        factors in a single unified optimization.
      - Real-time at 10 Hz; excellent for outdoor environments.
      - De facto standard for LiDAR-IMU SLAM research.

   .. tab-item:: KISS-ICP (2023)

      **Keep It Small and Simple** (Vizzo et al., RA-L 2023).

      - Remarkably simple design: adaptive threshold ICP on raw point clouds.
      - No feature extraction, no map management, no loop closure.
      - Achieves competitive accuracy with state-of-the-art systems on
        multiple benchmarks.
      - Highlights that well-designed ICP with adaptive parameters can
        compete with complex feature-based systems.

CARLA Hands-On: LiDAR Odometry and Mapping
--------------------------------------------

This exercise builds a minimal LiDAR odometry system: collect scans,
register consecutive scans with ICP, chain the transforms into a
trajectory, and measure how far it has drifted from ground truth.

Task 1: Collect Synchronized LiDAR and Ground-Truth Poses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import carla
   import numpy as np
   import open3d as o3d

   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   world = client.load_world('Town03')

   # Synchronous mode -- essential here, because scan-to-scan
   # registration assumes a fixed time step between scans (see L3).
   settings = world.get_settings()
   settings.synchronous_mode = True
   settings.fixed_delta_seconds = 0.1          # 10 Hz
   world.apply_settings(settings)
   tm = client.get_trafficmanager()
   tm.set_synchronous_mode(True)

   bp_lib = world.get_blueprint_library()
   vehicle = world.spawn_actor(
       bp_lib.find('vehicle.tesla.model3'),
       world.get_map().get_spawn_points()[0])
   vehicle.set_autopilot(True, tm.get_port())

   lidar_bp = bp_lib.find('sensor.lidar.ray_cast')
   lidar_bp.set_attribute('channels', '64')
   lidar_bp.set_attribute('range', '80')
   lidar_bp.set_attribute('points_per_second', '1000000')
   lidar_bp.set_attribute('rotation_frequency', '10')   # match the tick
   lidar = world.spawn_actor(
       lidar_bp, carla.Transform(carla.Location(z=2.4)), attach_to=vehicle)

   scans, gt_poses = [], []

   def lidar_callback(data):
       pts = np.frombuffer(data.raw_data, dtype=np.float32).reshape(-1, 4)
       scans.append(pts[:, :3].copy())
       # Ground-truth pose for evaluation ONLY -- never feed this to ICP
       gt_poses.append(np.array(data.transform.get_matrix()))

   lidar.listen(lidar_callback)

   try:
       for _ in range(600):        # 60 s at 10 Hz
           world.tick()
   finally:
       lidar.destroy()
       vehicle.destroy()
       settings.synchronous_mode = False
       settings.fixed_delta_seconds = None
       world.apply_settings(settings)
       tm.set_synchronous_mode(False)

Task 2: Preprocess and Register Consecutive Scans
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def to_o3d(points, voxel_size=0.2, z_min=-1.6):
       """Numpy -> Open3D cloud, with ground removed and downsampling."""
       # Dropping the ground plane matters: it is a large, locally flat
       # region that constrains z/roll/pitch well but slides freely in
       # x/y, so leaving it in lets ICP converge to a confidently wrong
       # answer along the direction of travel.
       pts = points[points[:, 2] > z_min]
       pcd = o3d.geometry.PointCloud()
       pcd.points = o3d.utility.Vector3dVector(pts)
       return pcd.voxel_down_sample(voxel_size)

   def icp_registration(source, target, init_transform=np.eye(4),
                        threshold=0.5):
       """Point-to-plane ICP registration (converges faster than point-to-point)."""
       for cloud in (source, target):
           cloud.estimate_normals(
               o3d.geometry.KDTreeSearchParamHybrid(radius=1.0, max_nn=30))

       result = o3d.pipelines.registration.registration_icp(
           source, target, threshold, init_transform,
           o3d.pipelines.registration.TransformationEstimationPointToPlane(),
           o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=50))

       return result.transformation, result.inlier_rmse, result.fitness

Task 3: Chain Transforms into a Trajectory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pose = np.eye(4)
   trajectory = [pose.copy()]
   prev = to_o3d(scans[0])

   for i in range(1, len(scans)):
       curr = to_o3d(scans[i])

       # Constant-velocity initial guess: assume this frame's motion
       # resembles the last one. ICP is local, so a good seed is the
       # difference between converging and diverging.
       if len(trajectory) >= 2:
           init = np.linalg.inv(trajectory[-2]) @ trajectory[-1]
       else:
           init = np.eye(4)

       T_delta, rmse, fitness = icp_registration(curr, prev, init)

       if fitness < 0.3:
           print(f"Frame {i}: ICP failed (fitness={fitness:.2f}), "
                 f"falling back to constant velocity")
           T_delta = init

       pose = pose @ T_delta
       trajectory.append(pose.copy())
       prev = curr

Task 4: Evaluate Against Ground Truth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Exercise Tasks
   :class: tip

   1. **Plot the trajectory** against ground truth (top-down x-y). The
      shapes should agree early and diverge progressively -- that
      divergence *is* the drift.
   2. **Quantify the drift.** Compute final position error as a
      percentage of total path length, and compare against the
      0.1--0.5% figure quoted for LOAM earlier in this lecture. Expect
      to do worse: you have no feature extraction and no backend.
   3. **Vary the voxel size** (0.1, 0.2, 0.5, 1.0 m). Plot registration
      time and drift against voxel size. Where is the knee?
   4. **Remove the ground-removal step** and re-run. Explain the change
      in longitudinal drift using the degeneracy argument above.
   5. **Break it deliberately**: replace the constant-velocity seed with
      ``np.eye(4)`` and drive a fast, curving route. Count how many
      frames report ``fitness < 0.3``. This is why every production
      system seeds ICP with IMU or wheel odometry.
   6. **Export to TUM format** and compute APE/RPE with ``evo``:

      .. code-block:: bash

         evo_ape tum groundtruth.txt estimated.txt -va --plot
         evo_rpe tum groundtruth.txt estimated.txt --delta 100 \
                 --delta_unit m -va

      Note how RPE stays roughly constant while APE grows without bound
      -- the signature of drift with no loop closure.


Summary
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Localization Methods
      :class-card: sd-border-primary

      - GNSS: global reference, 1-5 m accuracy (standard), 1-2 cm (RTK)
      - Dead reckoning: wheel, visual, LiDAR odometry -- drift accumulates
      - Probabilistic: EKF localization, MCL/AMCL (particle filter)
      - Map-based: ICP scan matching, HD map feature matching

   .. grid-item-card:: SLAM
      :class-card: sd-border-primary

      - Problem: simultaneous pose estimation and map building
      - Frontend: preprocessing, feature extraction, ICP, keyframe selection
      - Backend: pose graph optimization, loop closure detection
      - Systems: LOAM, LeGO-LOAM, LIO-SAM, KISS-ICP
      - Metrics: APE (global), RPE (local drift rate)

.. admonition:: Assignment Unlocked -- GP3: Fusion & Localization
   :class: important

   You now have the foundational knowledge from **L3 and L7** to begin
   **GP3: Fusion & Localization**. In GP3 you will implement camera-LiDAR
   frustum fusion for 3D object detection, build an Extended Kalman Filter
   that fuses GNSS and IMU for vehicle localization, and evaluate both
   against CARLA ground truth.

   :doc:`Go to GP3 </assignments/gp3>`
