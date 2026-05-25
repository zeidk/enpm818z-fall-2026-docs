====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 7: Localization & SLAM.
Topics include the localization problem, coordinate frames, GNSS/RTK,
dead reckoning (wheel/visual/LiDAR odometry), probabilistic localization
(EKF, MCL), scan matching (ICP), HD map localization, SLAM formulation,
SLAM frontend and backend, loop closure, evaluation metrics, and modern
LiDAR SLAM systems.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-10)
=================================

.. admonition:: Question 1
   :class: hint

   What is the typical horizontal accuracy of standard civilian GPS without
   any corrections, and why is this insufficient for autonomous driving
   lane-keeping?

   A. 1-5 mm; unnecessary precision wastes compute.

   B. 1-5 m; lane widths are approximately 3-4 m, requiring <20 cm for
      reliable lane-level localization.

   C. 10-50 m; cannot distinguish even road segments.

   D. 1-5 cm; sufficient for all AV applications.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- 1-5 m; lane widths are approximately 3-4 m, requiring <20 cm
   for reliable lane-level localization.

   Standard GPS (civilian L1 signal) achieves 1-5 m accuracy under good
   conditions, degrading further in urban canyons due to multipath. With
   lane widths of ~3.5 m, a 5 m position error means the vehicle cannot
   determine which lane it is in, let alone where within the lane. RTK-GPS
   or LiDAR scan matching is required for lane-level localization.


.. admonition:: Question 2
   :class: hint

   **RTK-GPS** achieves centimeter-level accuracy by:

   A. Using more satellites simultaneously than standard GPS.

   B. Applying corrections computed by a nearby base station at a precisely
      known location, enabling carrier-phase integer ambiguity resolution.

   C. Operating at a higher signal frequency (L5 band) than standard GPS.

   D. Averaging position estimates over multiple minutes to reduce noise.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Applying corrections computed by a nearby base station at a
   precisely known location, enabling carrier-phase integer ambiguity
   resolution.

   RTK stands for Real-Time Kinematic. The base station measures carrier-
   phase signals from GPS satellites and, knowing its exact position,
   computes the residual errors. These corrections are broadcast to the
   rover. By resolving the integer ambiguity in the carrier phase (wavelength
   ~19 cm for L1), the rover achieves 1-2 cm horizontal accuracy.


.. admonition:: Question 3
   :class: hint

   Which dead reckoning method has the **lowest positional drift** per unit
   distance traveled?

   A. Wheel odometry

   B. Monocular visual odometry

   C. LiDAR odometry

   D. IMU integration (without external corrections)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- LiDAR odometry

   LiDAR odometry (e.g., LOAM) achieves ~0.1-0.5% drift per distance
   traveled by directly measuring 3D geometry via scan matching. Wheel
   odometry drifts 1-5% due to wheel slip and terrain. Stereo visual
   odometry drifts 0.5-1%. IMU integration diverges within seconds due to
   gyroscope and accelerometer bias accumulation.


.. admonition:: Question 4
   :class: hint

   In **Iterative Closest Point (ICP)**, what is the role of the
   **correspondence step**?

   A. Compute the SVD of the cross-covariance matrix to find the optimal
      rotation and translation.

   B. For each point in the source cloud, find its nearest neighbor in the
      target cloud to establish point pairs for optimization.

   C. Apply motion distortion correction to each scan point using IMU data.

   D. Select keyframes by comparing the distance traveled since the last
      keyframe.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- For each point in the source cloud, find its nearest neighbor
   in the target cloud to establish point pairs for optimization.

   ICP alternates between two steps: (1) correspondence -- find nearest
   neighbors between current aligned source and target to form point pairs
   (p_i, q_i); (2) minimize -- solve for the rigid transform T that minimizes
   sum||q_i - T*p_i||^2 using SVD. The process repeats until convergence
   (translation/rotation change below threshold).


.. admonition:: Question 5
   :class: hint

   **Monte Carlo Localization (MCL/AMCL)** has an advantage over EKF
   localization because it can:

   A. Run faster than EKF on embedded hardware.

   B. Handle global localization (no initial pose given) and recovery from
      the "kidnapped robot" problem, which EKF cannot.

   C. Use fewer parameters than EKF.

   D. Provide a closed-form analytical solution to the posterior distribution.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Handle global localization (no initial pose given) and recovery
   from the "kidnapped robot" problem, which EKF cannot.

   EKF maintains a single Gaussian estimate of pose -- if the initialization
   is wrong or the vehicle is suddenly teleported (kidnapped), the single
   Gaussian cannot represent multiple hypotheses. MCL represents the belief
   as N particles spread across the entire map, naturally supporting multiple
   hypotheses. As measurements arrive, particles in wrong locations get low
   weight and die off; correct particles survive.


.. admonition:: Question 6
   :class: hint

   In the SLAM pose graph, what does a **loop closure edge** represent?

   A. A constraint between consecutive keyframes from scan-to-scan ICP.

   B. A constraint between two non-consecutive keyframes that were identified
      as the same location (the vehicle revisited a prior area), verified
      by ICP.

   C. A GPS measurement at a specific keyframe position.

   D. The initial pose prior used to anchor the first node.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A constraint between two non-consecutive keyframes that were
   identified as the same location (the vehicle revisited a prior area),
   verified by ICP.

   Loop closure edges connect keyframe i to keyframe j (where j >> i+1) when
   place recognition detects that the current scan matches a previous keyframe.
   The relative transform is computed by ICP and added as a long-range edge.
   During pose graph optimization, this edge pulls the two distant keyframes
   into alignment, distributing the accumulated drift correction across the
   entire trajectory.


.. admonition:: Question 7
   :class: hint

   **LOAM** (LiDAR Odometry and Mapping) achieves high-accuracy odometry by:

   A. Using a particle filter to track the vehicle pose.

   B. Matching edge features (high curvature points) and planar features
      (low curvature points) between scans using point-to-edge and
      point-to-plane distance minimization.

   C. Aligning raw LiDAR point clouds using standard point-to-point ICP.

   D. Fusing LiDAR with GPS measurements via a Kalman filter.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Matching edge features (high curvature points) and planar features
   (low curvature points) between scans using point-to-edge and point-to-plane
   distance minimization.

   LOAM extracts features based on local curvature: high curvature → edge
   features (on sharp corners and poles); low curvature → planar features
   (on flat walls and ground). Matching edge-to-edge and plane-to-plane
   (rather than arbitrary point-to-point) is more discriminative and produces
   better-constrained, more accurate scan matching results.


.. admonition:: Question 8
   :class: hint

   The **Absolute Pose Error (APE)** metric measures:

   A. The drift rate per meter of trajectory (local accuracy).

   B. The RMSE between estimated and ground-truth poses over the full
      trajectory (global accuracy).

   C. The number of loop closures detected per kilometer.

   D. The processing time per LiDAR scan.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The RMSE between estimated and ground-truth poses over the full
   trajectory (global accuracy).

   APE aligns the estimated trajectory to the ground truth (removing
   global gauge freedom) and then measures the RMSE of pose errors at
   each timestep. It reflects the overall quality of the map and the
   effectiveness of loop closure. Relative Pose Error (RPE) measures
   drift over fixed intervals -- a complementary local accuracy metric.


.. admonition:: Question 9
   :class: hint

   Why is **motion distortion correction** necessary for LiDAR scans in a
   moving vehicle?

   A. LiDAR sensors have a calibration error that must be corrected offline.

   B. A spinning LiDAR scan takes 50-100 ms to complete; during this time the
      vehicle moves, so each point is captured at a different vehicle pose.
      Without correction, the scan appears sheared/distorted.

   C. LiDAR returns require temperature correction to compute accurate ranges.

   D. Multiple LiDAR returns from the same surface must be averaged.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A spinning LiDAR scan takes 50-100 ms to complete; during this
   time the vehicle moves, so each point is captured at a different vehicle
   pose. Without correction, the scan appears sheared/distorted.

   At 50 km/h, a vehicle moves ~1.4 m during a 100 ms scan. Points at the
   start of the scan are displaced ~1.4 m relative to the end-of-scan points.
   IMU data (100-1000 Hz) is interpolated to compute the vehicle pose at
   each point's acquisition time, and each point is transformed to the
   common reference pose (e.g., scan start or scan center).


.. admonition:: Question 10
   :class: hint

   **LIO-SAM** improves on LOAM by:

   A. Removing the need for LiDAR entirely, using cameras and IMU.

   B. Tightly coupling IMU pre-integration with LiDAR scan matching in a
      unified factor graph (GTSAM), enabling accurate real-time SLAM with
      GPS and loop closure.

   C. Using neural network-based scan matching instead of ICP.

   D. Operating at 100 Hz by reducing scan resolution.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Tightly coupling IMU pre-integration with LiDAR scan matching
   in a unified factor graph (GTSAM), enabling accurate real-time SLAM with
   GPS and loop closure.

   LIO-SAM adds three key improvements over LOAM: (1) tight IMU integration
   via pre-integration factors for high-frequency motion estimates, (2) a
   full factor graph backend (GTSAM) that jointly optimizes IMU, LiDAR, GPS,
   and loop closure constraints, and (3) efficient sliding window map
   representation. This makes it robust to aggressive motions and suitable
   for long-duration outdoor mapping.


----


True or False (Questions 11-15)
================================

.. admonition:: Question 11
   :class: hint

   **True or False:** Dead reckoning methods like wheel odometry produce
   position estimates with bounded error -- the error does not grow
   indefinitely over time.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Dead reckoning error is **unbounded** -- it accumulates over time (or
   distance traveled) through integration. Systematic errors (e.g., slight
   wheel diameter miscalibration) cause the error to grow linearly with
   distance; random noise causes it to grow as a random walk (proportional
   to sqrt of distance). Without external corrections (GPS, scan matching,
   landmarks), any dead reckoning method will eventually lose track of
   the vehicle's true position.


.. admonition:: Question 12
   :class: hint

   **True or False:** In the SLAM problem, the vehicle must have a pre-built
   map of the environment before it can operate.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   SLAM (Simultaneous Localization and Mapping) is specifically designed
   for operation WITHOUT a prior map. The vehicle builds the map from scratch
   using sensor observations while simultaneously estimating its own position
   within that growing map. This is in contrast to map-based localization
   (e.g., HD map matching), which requires a pre-built map.


.. admonition:: Question 13
   :class: hint

   **True or False:** Loop closure detection can reduce the accumulated
   drift in a SLAM trajectory even if the loop closure occurs only once
   at the very end of a long mission.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A single loop closure edge in the pose graph, added at the end of a long
   trajectory, creates a constraint between the start and end of the loop.
   Pose graph optimization distributes this correction across all
   intermediate poses in the loop, reducing the drift from meters to
   centimeters throughout the entire trajectory. This is the power of global
   backend optimization -- it retroactively corrects the entire history.


.. admonition:: Question 14
   :class: hint

   **True or False:** Point-to-plane ICP is generally faster to converge
   than standard point-to-point ICP when matching planar surfaces.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Point-to-plane ICP minimizes the distance from each source point to the
   tangent plane at the corresponding target point (using surface normals).
   This objective provides a more accurate gradient for optimization near
   flat surfaces -- the most common geometry in man-made environments.
   Empirically, point-to-plane converges in ~5-10 iterations vs. ~30-50 for
   point-to-point, on typical urban LiDAR scans.


.. admonition:: Question 15
   :class: hint

   **True or False:** HD map-based localization suffers from accumulated
   drift over long drives because it integrates odometry without correction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   HD map-based localization does NOT accumulate drift. The HD map provides
   a globally consistent reference frame. At each step, the current sensor
   scan is matched against the global HD map to compute a position correction
   -- this measurement-to-map comparison anchors the pose estimate to the
   global frame. The limitation of HD maps is not drift but rather their
   cost to create, maintain, and update when the environment changes.


----


Essay Questions (Questions 16-18)
===================================

.. admonition:: Question 16
   :class: hint

   **Explain the SLAM frontend and backend** as a two-stage processing
   pipeline. What does each stage produce, and why must they work together
   for accurate long-range mapping?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Frontend: processes raw LiDAR scans in real time to produce a local
     odometry estimate (incremental pose changes) and detects potential
     loop closure candidates. It includes preprocessing (motion distortion,
     downsampling), feature extraction, ICP scan matching, and keyframe
     selection. Frontend must run faster than the sensor rate (>10 Hz for
     a 10 Hz LiDAR).
   - Backend: receives keyframes and their relative pose constraints from
     the frontend and solves a global pose graph optimization problem to
     find the maximum-likelihood trajectory. When loop closures are added,
     the backend redistributes drift corrections across the entire history.
   - Why both are needed: the frontend provides the real-time incremental
     estimates and detects loop candidates; but without the backend's global
     optimization, drift accumulates indefinitely. Without the frontend's
     real-time operation, the backend has no input. Together they achieve
     real-time, globally consistent mapping.
   - Example: after 500 m, the frontend has 5 m of drift. One loop closure
     detected by the frontend triggers backend optimization, reducing APE
     to <5 cm across the entire 500 m trajectory.


.. admonition:: Question 17
   :class: hint

   **Describe why loop closure is critical for SLAM** and how place
   recognition enables it. What happens to the map quality if loop
   closure fails?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - SLAM odometry (frontend) accumulates drift -- typically 0.1-0.5% of
     distance for LiDAR SLAM. Over 1 km, this means 1-5 m of accumulated
     error. Without correction, the map shows the start and end of a loop
     as two separate locations (map "split"), making the map inconsistent.
   - Loop closure detects that the vehicle is revisiting a known location
     by comparing the current scan's global descriptor (Scan Context,
     FPFH) against all stored keyframe descriptors. When a match is found,
     ICP verifies the relative transform.
   - The verified loop closure edge is added to the pose graph. Backend
     optimization distributes the correction: all keyframes in the loop
     are adjusted to make the loop geometrically consistent.
   - Without loop closure: maps of large environments (>100 m) are
     unusable for localization because the start and end of a revisited
     area appear at different locations. The map cannot be used for
     place recognition in future operations.


.. admonition:: Question 18
   :class: hint

   **Compare GNSS-based localization and LiDAR scan matching** as
   localization methods for autonomous driving. In what environments does
   each perform best, and how do production AV systems combine them?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - GNSS (especially RTK): provides global, drift-free localization but
     fails in urban canyons (multipath), tunnels, and underground areas.
     Accuracy: 1-2 cm (RTK) under open sky; degrades to meters or loss
     of fix in dense urban environments. No map required.
   - LiDAR scan matching: provides high-accuracy local positioning (0.1-0.5%
     drift for odometry; centimeter-level for map-based matching against
     HD maps) but requires a pre-built map and accumulates drift without
     loop closure. Works in tunnels, indoor parking, urban canyons.
   - Production systems (Waymo, Cruise, Mobileye): use a tight EKF/factor
     graph fusion of GNSS, LiDAR scan matching against HD maps, and IMU.
     GNSS provides the global anchor; LiDAR provides accuracy in GNSS-denied
     environments; IMU fills short gaps at high frequency.
   - The HD map acts as the "long-term memory" -- accumulated drift from
     LiDAR odometry is corrected at each map feature observation, providing
     globally consistent, centimeter-accurate localization in all covered
     environments.
