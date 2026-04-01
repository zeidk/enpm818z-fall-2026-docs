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

Integrates wheel encoder measurements to estimate 2D pose:

.. math::

   \Delta d = \frac{\Delta d_L + \Delta d_R}{2}, \quad \Delta \theta = \frac{\Delta d_R - \Delta d_L}{L}

   x_{k+1} = x_k + \Delta d \cos(\theta_k + \Delta\theta/2)

   y_{k+1} = y_k + \Delta d \sin(\theta_k + \Delta\theta/2)

   \theta_{k+1} = \theta_k + \Delta\theta

**Error sources**: wheel slip (especially on turns, wet roads), uneven terrain
(suspension deflection changes wheel-ground contact), encoder resolution.
Drift accumulates quadratically over distance (systematic) or as a random walk.

Visual Odometry (VO)
~~~~~~~~~~~~~~~~~~~~~~

Estimates camera motion by tracking/matching feature points across consecutive
frames:

1. Detect keypoints (ORB, SIFT, SuperPoint).
2. Match keypoints between frames.
3. Compute essential matrix :math:`E` using RANSAC.
4. Decompose :math:`E = R t^{\times}` to get rotation and (scale-ambiguous) translation.
5. (Stereo VO) Use stereo baseline to recover metric scale.

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
   :math:`h(\mathbf{x}, m_j)` and update using the EKF equations from L6.

The observation function :math:`h` is typically nonlinear (e.g., range-bearing
to a known landmark), requiring the EKF's Jacobian linearization.

MCL: Monte Carlo Localization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**MCL** (also called **AMCL** -- Adaptive MCL) uses a particle filter to
represent the pose belief. It is the standard algorithm for robot localization
in ROS.

.. code-block:: text

   Initialize N particles uniformly (or from GPS prior)

   Loop:
   1. MOTION UPDATE: sample new particle from motion model
      x^(i) ~ p(x_t | x^(i)_{t-1}, u_t)    [add process noise to odometry]

   2. SENSOR UPDATE: weight by LiDAR scan likelihood
      w^(i) = p(z_t | x^(i), map)           [compare scan to map raycast]

   3. RESAMPLE: resample N particles by weight

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
2. **Minimize**: solve for optimal rigid transform T using SVD:

   .. math::

      [U, S, V^T] = \text{SVD}(H) \quad \text{where } H = \sum_i (p_i - \bar{p})(q_i - \bar{q})^T

      R = V U^T, \quad t = \bar{q} - R \bar{p}

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

.. code-block:: python

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

   After 100 m of LOAM operation (~0.5% drift), the map has accumulated
   ~0.5 m of error. After 1 km, ~5 m error -- unusable for lane-level
   driving. A single correct loop closure over 1 km reduces this error
   to sub-centimeter level by distributing the correction across the
   entire trajectory.


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
      - Performance: ~5-10 cm APE on KITTI odometry benchmark (top result in 2014).
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

CARLA SLAM Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~

In the CARLA assignment for this lecture, you will:

1. Collect LiDAR point clouds at 10 Hz while driving through Town03.
2. Implement voxel downsampling and motion distortion correction using
   the IMU data.
3. Apply Open3D's point-to-plane ICP to estimate scan-to-scan transforms.
4. Accumulate poses into a trajectory and visualize the reconstructed map.
5. Compare your trajectory against CARLA's ground-truth transform using EVO.

.. code-block:: python

   import open3d as o3d
   import numpy as np

   def icp_registration(source, target, init_transform=np.eye(4), threshold=0.3):
       """Point-to-plane ICP registration."""
       source.estimate_normals(
           o3d.geometry.KDTreeSearchParamHybrid(radius=0.5, max_nn=30))
       target.estimate_normals(
           o3d.geometry.KDTreeSearchParamHybrid(radius=0.5, max_nn=30))

       result = o3d.pipelines.registration.registration_icp(
           source, target, threshold, init_transform,
           o3d.pipelines.registration.TransformationEstimationPointToPlane(),
           o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=50))

       return result.transformation, result.inlier_rmse


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
