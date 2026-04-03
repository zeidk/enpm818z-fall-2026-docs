====================================================
Lecture
====================================================


Why Sensor Fusion Is Essential
--------------------------------

Each sensor modality has complementary strengths and weaknesses. Relying on
any single sensor creates gaps in perception that can lead to safety-critical
failures.

.. list-table::
   :widths: 15 28 28 29
   :header-rows: 1
   :class: compact-table

   * - Property
     - Camera
     - LiDAR
     - RADAR
   * - **Resolution**
     - Very high (megapixels)
     - Medium (64-128 beams)
     - Low (sparse)
   * - **Range**
     - 50-200 m (visual range)
     - 50-200 m
     - 200-300 m
   * - **Night performance**
     - Poor (needs illumination)
     - Good
     - Excellent
   * - **Rain / fog**
     - Degraded
     - Degraded
     - Robust
   * - **Depth accuracy**
     - Low (inferred)
     - High (direct ToF)
     - High (direct)
   * - **Velocity measurement**
     - Indirect (optical flow)
     - Via scan matching
     - Direct (Doppler)
   * - **Semantic richness**
     - Very high (texture, color)
     - Low (geometry only)
     - Very low
   * - **Cost**
     - Low
     - High ($5K-$75K)
     - Low-medium

.. admonition:: Key Point
   :class: important

   Fusion exploits the **complementary** nature of these sensors. A camera-only
   system fails in fog; a LiDAR-only system misses semantic classes; a RADAR-only
   system cannot detect lane markings. Together, the combined system is more
   accurate, reliable, and complete than any individual sensor.


Sensor Relationships
---------------------

.. tab-set::

   .. tab-item:: Complementary

      Sensors measure **different physical phenomena** and provide non-overlapping
      information. Combining them adds new capabilities.

      *Example*: Camera detects traffic light color; LiDAR measures precise
      distance. Neither alone can both classify the light AND measure its range.

   .. tab-item:: Competitive (Redundant)

      Sensors measure the **same quantity** using different physical principles.
      Fusion improves accuracy and provides fallback if one sensor fails.

      *Example*: Both LiDAR and RADAR can measure the distance to the car ahead.
      Fusing their measurements reduces variance. If the LiDAR is occluded by
      rain, RADAR maintains coverage.

   .. tab-item:: Cooperative

      Sensors work together where the output of one sensor **contextualizes** the
      output of another.

      *Example*: IMU provides high-frequency motion data (100-1000 Hz) that
      enables precise interpolation of LiDAR scan points (acquired at 10-20 Hz),
      correcting for motion distortion during the scan.


Fusion Architectures
---------------------

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Early Fusion (Raw Data)
      :class-card: sd-border-info

      Combine raw sensor data before any feature extraction. Example: project
      LiDAR points onto camera image and concatenate depth as extra channels.

      **Pros**: maximum information available.
      **Cons**: modality mismatch (resolution, format), requires careful
      alignment, high data volume.

   .. grid-item-card:: Intermediate Fusion (Feature-Level)
      :class-card: sd-border-info

      Each sensor extracts features independently; features are fused in a
      shared representation space. Example: BEVFusion -- camera BEV features
      + LiDAR BEV features fused by concatenation or attention.

      **Pros**: balances information richness with compute efficiency.
      **Cons**: features must be aligned (requires calibration).

   .. grid-item-card:: Late Fusion (Decision-Level)
      :class-card: sd-border-info

      Each sensor produces independent outputs (detections, tracks); fusion
      occurs at the decision level. Example: camera 3D boxes + LiDAR 3D boxes
      → fused object list via weighted averaging or NMS.

      **Pros**: simple, modular, each sensor stack is independently testable.
      **Cons**: information lost at intermediate stages; fusion cannot recover
      complementary features.


Kalman Filter for Sensor Fusion
---------------------------------

.. admonition:: Recap from ENPM673
   :class: note

   In ENPM673, you derived the Kalman Filter from first principles: the
   linear-Gaussian state space model, the predict-update cycle, and the
   Kalman Gain as a trust dial between prediction and measurement. Here
   we focus on **applying** the KF framework to multi-sensor fusion in
   autonomous driving.

KF Equations -- Quick Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: KF Predict-Update Summary
   :class: hint

   .. math::

      \textbf{Predict:} \quad \hat{\mathbf{x}}_{k|k-1} = F_k \hat{\mathbf{x}}_{k-1|k-1} + B_k \mathbf{u}_k, \quad P_{k|k-1} = F_k P_{k-1|k-1} F_k^T + Q_k

      \textbf{Update:} \quad K_k = P_{k|k-1} H_k^T (H_k P_{k|k-1} H_k^T + R_k)^{-1}

      \hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + K_k (\mathbf{z}_k - H_k \hat{\mathbf{x}}_{k|k-1}), \quad P_{k|k} = (I - K_k H_k) P_{k|k-1}

Kalman Gain Intuition
~~~~~~~~~~~~~~~~~~~~~~

.. math::

   K_k = \frac{P_{k|k-1} H_k^T}{H_k P_{k|k-1} H_k^T + R_k}
       \approx \frac{\text{prior uncertainty}}{\text{prior uncertainty} + \text{measurement noise}}

.. list-table::
   :widths: 40 60
   :class: compact-table

   * - :math:`K_k \to 0` (small gain)
     - Measurement very noisy (:math:`R_k` large) OR prior very certain
       (:math:`P_{k|k-1}` small). Trust the prediction, barely update.
   * - :math:`K_k \to H^{-1}` (large gain)
     - Measurement very accurate (:math:`R_k` small) OR prior very uncertain
       (:math:`P_{k|k-1}` large). Trust the measurement, update aggressively.

.. admonition:: Engineering Intuition
   :class: tip

   Think of :math:`K_k` as a "trust dial" between prediction and measurement.
   When your model is confident and sensors are noisy, trust the model. When
   sensors are accurate and your model is uncertain (e.g., at startup), trust
   the sensors.

KF for Multi-Sensor Fusion in AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider tracking a vehicle ahead of the ego car. We define a state vector
that captures the target's position, velocity, and range-rate:

.. math::

   \mathbf{x} = \begin{bmatrix} x \\ y \\ z \\ \dot{x} \\ \dot{y} \\ \dot{z} \end{bmatrix}

Three sensors observe this target, each measuring a different subset of the
state through its own measurement matrix :math:`H`.

**LiDAR** -- measures 3D position directly:

.. math::

   \mathbf{z}^{L} = \begin{bmatrix} x \\ y \\ z \end{bmatrix}, \quad
   H^{L} = \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 \end{bmatrix}

**RADAR** -- measures range :math:`r = \sqrt{x^2+y^2}` and range-rate
:math:`\dot{r}`. For a target directly ahead (small bearing), the linearized
measurement simplifies to:

.. math::

   \mathbf{z}^{R} = \begin{bmatrix} x \\ \dot{x} \end{bmatrix}, \quad
   H^{R} = \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 \end{bmatrix}

**Camera** -- provides bearing (lateral pixel position maps to :math:`y`
offset after projection):

.. math::

   \mathbf{z}^{C} = \begin{bmatrix} y \end{bmatrix}, \quad
   H^{C} = \begin{bmatrix} 0 & 1 & 0 & 0 & 0 & 0 \end{bmatrix}

Sequential Update Procedure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At each time step, run the **predict** step once using the constant-velocity
process model, then apply the **update** step sequentially for each sensor
that delivers a measurement:

1. **Predict** :math:`\hat{\mathbf{x}}_{k|k-1}`, :math:`P_{k|k-1}` using :math:`F` and :math:`Q`.
2. **Update with LiDAR**: use :math:`H^{L}`, :math:`R^{L}`, :math:`\mathbf{z}^{L}` to obtain :math:`\hat{\mathbf{x}}_{k|L}`, :math:`P_{k|L}`.
3. **Update with RADAR**: using the posterior from step 2 as the new prior, apply :math:`H^{R}`, :math:`R^{R}`, :math:`\mathbf{z}^{R}`.
4. **Update with Camera**: again chain the posterior, applying :math:`H^{C}`, :math:`R^{C}`, :math:`\mathbf{z}^{C}`.

The order of sensor updates does not affect the final result (the KF update
is associative for independent measurements). Each update further reduces the
covariance :math:`P`, fusing complementary information from all three modalities.

Sensor Noise and Environmental Conditions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each sensor's measurement noise covariance :math:`R` reflects both intrinsic
sensor precision and current environmental conditions:

.. list-table::
   :widths: 18 27 27 28
   :header-rows: 1
   :class: compact-table

   * - Condition
     - Camera :math:`R^{C}`
     - LiDAR :math:`R^{L}`
     - RADAR :math:`R^{R}`
   * - Clear day
     - Low (sharp images)
     - Low (clean returns)
     - Low
   * - Heavy rain
     - **High** (blur, glare)
     - Moderate (scattering)
     - Low (robust to rain)
   * - Night
     - **High** (low contrast)
     - Low (active sensor)
     - Low (active sensor)
   * - Fog
     - **High** (occlusion)
     - **High** (backscatter)
     - Low (penetrates fog)
   * - Direct sunlight
     - Moderate (saturation)
     - Moderate (solar noise)
     - Low

.. admonition:: Adaptive Noise Tuning
   :class: tip

   In practice, the :math:`R` matrices are not static. Production AV stacks
   **adapt** :math:`R` at runtime based on weather classification, sensor
   health monitors, and signal-to-noise diagnostics. For example, when a rain
   detector triggers, :math:`R^{C}` is inflated so the Kalman gain
   automatically down-weights camera measurements in favor of RADAR.


Extended Kalman Filter (EKF)
-----------------------------

The standard KF assumes **linear** process and measurement models. Most AV
applications are nonlinear (e.g., vehicle dynamics with heading angle, radar
measurement in polar coordinates).

The **Extended Kalman Filter (EKF)** linearizes nonlinear functions via their
**Jacobian** (first-order Taylor expansion):

.. math::

   \mathbf{x}_k = f(\mathbf{x}_{k-1}, \mathbf{u}_k) + \mathbf{w}_k

   \mathbf{z}_k = h(\mathbf{x}_k) + \mathbf{v}_k

EKF Equations
~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Predict

      .. math::

         \hat{\mathbf{x}}_{k|k-1} = f(\hat{\mathbf{x}}_{k-1|k-1}, \mathbf{u}_k)

         P_{k|k-1} = F_k P_{k-1|k-1} F_k^T + Q_k

         \text{where } F_k = \left. \frac{\partial f}{\partial \mathbf{x}} \right|_{\hat{\mathbf{x}}_{k-1|k-1}}

   .. tab-item:: Update

      .. math::

         H_k = \left. \frac{\partial h}{\partial \mathbf{x}} \right|_{\hat{\mathbf{x}}_{k|k-1}}

         K_k = P_{k|k-1} H_k^T (H_k P_{k|k-1} H_k^T + R_k)^{-1}

         \hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + K_k(\mathbf{z}_k - h(\hat{\mathbf{x}}_{k|k-1}))

         P_{k|k} = (I - K_k H_k) P_{k|k-1}

.. admonition:: EKF Limitation
   :class: warning

   The Jacobian linearization is only accurate near the expansion point. For
   highly nonlinear functions, the linearization error can cause the EKF to
   diverge or produce overconfident (underestimated) covariance estimates.


Unscented Kalman Filter (UKF)
------------------------------

The **Unscented Kalman Filter (UKF)** avoids explicit Jacobian computation by
using **sigma points** -- a carefully chosen set of sample points that capture
the mean and covariance of the prior distribution.

.. admonition:: Core Idea
   :class: note

   "It is easier to approximate a probability distribution than it is to
   approximate an arbitrary nonlinear function." -- Julier & Uhlmann (1997)

Sigma Point Generation
~~~~~~~~~~~~~~~~~~~~~~~

For a state of dimension :math:`n`, generate :math:`2n+1` sigma points:

.. math::

   \mathcal{X}_0 = \hat{\mathbf{x}}

   \mathcal{X}_i = \hat{\mathbf{x}} + \left(\sqrt{(n+\lambda)P}\right)_i, \quad i = 1,\ldots,n

   \mathcal{X}_{i+n} = \hat{\mathbf{x}} - \left(\sqrt{(n+\lambda)P}\right)_i, \quad i = 1,\ldots,n

where :math:`\lambda = \alpha^2(n+\kappa) - n` is a scaling parameter.

Each sigma point is propagated through the **full nonlinear function** (no
linearization). The posterior mean and covariance are recovered as
weighted averages of the propagated sigma points.

UKF vs EKF
~~~~~~~~~~~

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - Property
     - EKF
     - UKF
   * - Linearization
     - First-order Taylor (Jacobian)
     - None (sigma points)
   * - Accuracy
     - First-order accurate
     - Second-order accurate
   * - Compute
     - Jacobian evaluation (complex for large state)
     - :math:`2n+1` nonlinear evaluations (simple)
   * - Implementation
     - Requires analytical Jacobians
     - Only needs :math:`f()` and :math:`h()` functions


Particle Filter
----------------

The **Particle Filter (PF)** is a sequential Monte Carlo method for Bayesian
estimation. It represents the posterior distribution as a **set of weighted
samples (particles)**.

.. math::

   p(\mathbf{x}_k | \mathbf{z}_{1:k}) \approx \sum_{i=1}^{N} w_k^{(i)} \delta(\mathbf{x}_k - \mathbf{x}_k^{(i)})

Algorithm
~~~~~~~~~~

.. code-block:: text

   Initialize N particles: x^(i) ~ p(x_0), w^(i) = 1/N

   For each time step k:
   1. PREDICT: Propagate each particle through process model
              x^(i) ~ p(x_k | x^(i)_{k-1})  [sample from process noise]

   2. UPDATE:  Weight each particle by measurement likelihood
              w^(i) = p(z_k | x^(i))

   3. NORMALIZE: w^(i) = w^(i) / sum_j w^(j)

   4. RESAMPLE: Draw N new particles with replacement, proportional to weights
              [eliminates low-weight particles, duplicates high-weight ones]

Advantages and Limitations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Advantages
      :class-card: sd-border-success

      - Handles **non-Gaussian** noise (multi-modal posteriors, heavy tails)
      - Handles **nonlinear** models without any approximation
      - Can represent **multi-hypothesis** scenarios (e.g., ambiguous localization)
      - Simple to implement -- only needs sampling and likelihood evaluation

   .. grid-item-card:: Limitations
      :class-card: sd-border-warning

      - **Computationally expensive**: accuracy scales with particle count N
      - **Curse of dimensionality**: number of particles needed grows
        exponentially with state dimension
      - **Particle collapse**: with insufficient particles, all weight
        concentrates on a few samples (degeneracy)


Filter Comparison Table
------------------------

.. list-table::
   :widths: 18 20 20 20 22
   :header-rows: 1
   :class: compact-table

   * - Property
     - KF
     - EKF
     - UKF
     - Particle Filter
   * - Model type
     - Linear
     - Nonlinear (linearized)
     - Nonlinear
     - Nonlinear
   * - Noise distribution
     - Gaussian
     - Gaussian
     - Gaussian
     - Arbitrary
   * - Accuracy
     - Optimal (linear)
     - 1st-order
     - 2nd-order
     - Asymptotically exact
   * - Multi-modal
     - No
     - No
     - No
     - Yes
   * - Compute cost
     - Low
     - Medium
     - Medium
     - High
   * - AV use case
     - Simple tracking
     - Object tracking, SLAM
     - IMU/GPS fusion
     - Localization (AMCL)


Data Association Problem
-------------------------

In multi-sensor, multi-object scenarios, we must answer: **which measurement
belongs to which tracked object?**

This is the **data association problem**. Incorrect association causes Kalman
filter divergence and track confusion.

.. tab-set::

   .. tab-item:: Nearest Neighbor (NN)

      Assign each measurement to the nearest existing track (by Mahalanobis
      or Euclidean distance). Simple but fails in cluttered scenes.

   .. tab-item:: Global Nearest Neighbor (GNN)

      Solve the **global** optimal assignment using the Hungarian algorithm on
      a cost matrix built from all measurement-track distances. Optimal for
      a single assignment step.

   .. tab-item:: JPDA

      **Joint Probabilistic Data Association**: instead of hard assignment,
      computes a probability distribution over all possible assignments and
      updates each track as a weighted mixture. Robust in high-clutter
      environments.

   .. tab-item:: MHT

      **Multiple Hypothesis Tracking**: maintains a tree of all possible
      assignment hypotheses across multiple time steps. Most accurate but
      exponential complexity without pruning.

.. admonition:: Mahalanobis Distance
   :class: note

   The Mahalanobis distance accounts for track uncertainty (covariance):

   .. math::

      d_M(\mathbf{z}, \hat{\mathbf{z}}) = \sqrt{(\mathbf{z} - \hat{\mathbf{z}})^T S^{-1} (\mathbf{z} - \hat{\mathbf{z}})}

   where :math:`S = H P H^T + R` is the innovation covariance. This is
   preferred over Euclidean distance because it accounts for how uncertain
   the prediction is in each direction.


Weighted Averaging and Inverse Variance Weighting
---------------------------------------------------

For simple sensor fusion of independent estimates :math:`\hat{x}_1, \hat{x}_2`
with variances :math:`\sigma_1^2, \sigma_2^2`:

.. math::

   w_i = \frac{1/\sigma_i^2}{\sum_j 1/\sigma_j^2}

   \hat{x}_{fused} = \sum_i w_i \hat{x}_i

   \sigma_{fused}^2 = \frac{1}{\sum_i 1/\sigma_i^2}

This is **optimal** for unbiased, independent, Gaussian-distributed estimates.
More uncertain sensors receive lower weight automatically.

*Example*: GPS position variance :math:`\sigma_{GPS}^2 = 4 \text{ m}^2`,
LiDAR scan-match position variance :math:`\sigma_{LiDAR}^2 = 0.01 \text{ m}^2`.
The fused estimate will be almost entirely determined by LiDAR -- correctly so.


Deep Learning Fusion: Cross-Attention
---------------------------------------

Modern deep learning approaches replace hand-crafted fusion rules with
**learned attention mechanisms**.

Cross-Attention Fusion
~~~~~~~~~~~~~~~~~~~~~~~

Given LiDAR BEV features :math:`\mathbf{F}_L \in \mathbb{R}^{H \times W \times C}`
and camera BEV features :math:`\mathbf{F}_C \in \mathbb{R}^{H \times W \times C}`:

.. math::

   \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V

   Q = \mathbf{F}_L W_Q, \quad K = \mathbf{F}_C W_K, \quad V = \mathbf{F}_C W_V

The LiDAR features **query** the camera features -- each LiDAR BEV cell attends
to the most relevant camera BEV cells, learning to weight semantic camera
information based on geometric LiDAR context.

BEVFusion (MIT) Example
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **Camera branch**
     - LSS-based camera-to-BEV transform → camera BEV features
   * - **LiDAR branch**
     - Voxel encoder → sparse 3D conv → BEV feature map
   * - **Fusion**
     - Concatenate camera + LiDAR BEV features → channel fusion conv
   * - **Output**
     - Fused BEV features → detection/segmentation heads

Performance on nuScenes: 70.2 NDS vs. 65.0 for LiDAR-only -- camera fusion
adds semantic richness that improves small object detection.


CARLA Hands-On: Multi-Sensor Kalman Filter
------------------------------------------------

This exercise implements a multi-sensor fusion pipeline using the Kalman Filter
framework discussed in this lecture. You will fuse CARLA's camera, LiDAR, and
RADAR data to track vehicles ahead of the ego car in real time.


Task 1: Spawn Multi-Sensor Suite and Collect Synchronized Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Connect to CARLA, spawn an ego vehicle on autopilot, and attach three sensors.
A ``SensorManager`` class stores the latest reading from each sensor with
timestamps so that we can collect synchronized snapshots at 10 Hz.

.. code-block:: python

   import carla
   import numpy as np
   import time

   # ---------- Sensor Manager ----------
   class SensorManager:
       """Stores the latest reading from each sensor with timestamps."""

       def __init__(self):
           self.latest = {}   # sensor_name -> (timestamp, data)

       def make_callback(self, sensor_name):
           def callback(data):
               self.latest[sensor_name] = (data.timestamp, data)
           return callback

       def get_snapshot(self):
           """Return a copy of the latest readings from all sensors."""
           return dict(self.latest)

   # ---------- CARLA setup ----------
   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   world = client.get_world()
   bp_lib = world.get_blueprint_library()

   # Spawn ego vehicle
   vehicle_bp = bp_lib.find('vehicle.tesla.model3')
   spawn_point = world.get_map().get_spawn_points()[0]
   ego = world.spawn_actor(vehicle_bp, spawn_point)
   ego.set_autopilot(True)

   # ---------- Sensor blueprints ----------
   camera_bp = bp_lib.find('sensor.camera.rgb')
   camera_bp.set_attribute('image_size_x', '1280')
   camera_bp.set_attribute('image_size_y', '720')
   camera_bp.set_attribute('fov', '90')

   lidar_bp = bp_lib.find('sensor.lidar.ray_cast')
   lidar_bp.set_attribute('channels', '64')
   lidar_bp.set_attribute('range', '100')
   lidar_bp.set_attribute('rotation_frequency', '10')
   lidar_bp.set_attribute('points_per_second', '100000')

   radar_bp = bp_lib.find('sensor.other.radar')
   radar_bp.set_attribute('horizontal_fov', '30')
   radar_bp.set_attribute('range', '100')

   # ---------- Attach sensors ----------
   camera = world.spawn_actor(
       camera_bp,
       carla.Transform(carla.Location(x=1.5, z=2.4)),
       attach_to=ego)
   lidar = world.spawn_actor(
       lidar_bp,
       carla.Transform(carla.Location(x=0.0, z=2.4)),
       attach_to=ego)
   radar = world.spawn_actor(
       radar_bp,
       carla.Transform(carla.Location(x=2.0, z=1.0)),
       attach_to=ego)

   # ---------- Register callbacks ----------
   sm = SensorManager()
   camera.listen(sm.make_callback('camera'))
   lidar.listen(sm.make_callback('lidar'))
   radar.listen(sm.make_callback('radar'))

   # ---------- Collect at 10 Hz ----------
   snapshots = []
   for _ in range(200):          # 20 seconds of data
       world.tick()
       snap = sm.get_snapshot()
       if len(snap) == 3:        # all three sensors have data
           snapshots.append(snap)
       time.sleep(0.1)


Task 2: Implement a Linear Kalman Filter for Vehicle Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define the state vector :math:`\mathbf{x} = [x, y, v_x, v_y]^T` for tracking
a vehicle ahead. The constant-velocity model uses :math:`\Delta t = 0.1\,\text{s}`.

.. code-block:: python

   class KalmanFilter:
       """Linear Kalman Filter for 2D vehicle tracking."""

       def __init__(self, dt=0.1):
           self.dt = dt

           # State vector: [x, y, vx, vy]
           self.x = np.zeros(4)

           # State covariance
           self.P = np.eye(4) * 100.0  # large initial uncertainty

           # State transition (constant velocity)
           self.F = np.array([
               [1, 0, dt,  0],
               [0, 1,  0, dt],
               [0, 0,  1,  0],
               [0, 0,  0,  1],
           ])

           # Process noise
           q = 0.5   # acceleration noise std
           self.Q = np.array([
               [dt**4/4,       0, dt**3/2,       0],
               [      0, dt**4/4,       0, dt**3/2],
               [dt**3/2,       0,   dt**2,       0],
               [      0, dt**3/2,       0,   dt**2],
           ]) * q**2

           # Default measurement model: observe position only
           self.H = np.array([
               [1, 0, 0, 0],
               [0, 1, 0, 0],
           ])

           # Default measurement noise (overridden per sensor)
           self.R = np.eye(2)

       def predict(self):
           """Predict step: propagate state and covariance forward."""
           self.x = self.F @ self.x
           self.P = self.F @ self.P @ self.F.T + self.Q

       def update(self, z, R=None):
           """Update step: incorporate measurement z with noise R."""
           if R is None:
               R = self.R
           H = self.H
           y = z - H @ self.x                       # innovation
           S = H @ self.P @ H.T + R                  # innovation covariance
           K = self.P @ H.T @ np.linalg.inv(S)       # Kalman gain
           self.x = self.x + K @ y
           self.P = (np.eye(4) - K @ H) @ self.P


Task 3: Sequential Multi-Sensor Update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract range estimates from each sensor and apply the KF update sequentially.
Each sensor uses a different measurement noise covariance reflecting its
precision. Printing the covariance trace after each update shows how
uncertainty decreases as sensors are fused.

.. code-block:: python

   # ---------- Measurement noise per sensor ----------
   R_lidar  = np.diag([0.1, 0.1])   # high precision
   R_radar  = np.diag([0.5, 0.5])   # moderate precision
   R_camera = np.diag([2.0, 2.0])   # low precision

   def lidar_measurement(lidar_data, ego_transform):
       """Nearest point cluster in the forward cone (+-15 deg, <80 m)."""
       points = np.frombuffer(lidar_data.raw_data, dtype=np.float32)
       points = points.reshape(-1, 4)[:, :3]        # x, y, z
       forward = points[points[:, 0] > 0]            # positive-x is forward
       angles = np.abs(np.arctan2(forward[:, 1], forward[:, 0]))
       mask = angles < np.radians(15)
       cone = forward[mask]
       if len(cone) == 0:
           return None
       nearest_idx = np.argmin(np.linalg.norm(cone[:, :2], axis=1))
       return cone[nearest_idx, :2]                  # (x, y) in sensor frame

   def radar_measurement(radar_data):
       """Closest RADAR detection by depth."""
       detections = []
       for det in radar_data:
           detections.append([det.depth, det.azimuth, det.altitude])
       if not detections:
           return None
       detections = np.array(detections)
       closest = detections[np.argmin(detections[:, 0])]
       depth, azimuth = closest[0], closest[1]
       x = depth * np.cos(azimuth)
       y = depth * np.sin(azimuth)
       return np.array([x, y])

   def camera_measurement(image_data, known_vehicle_width=1.8, focal_px=640):
       """Estimate distance from bounding-box width (pinhole model)."""
       # Placeholder: assume bbox_width_px is obtained from a detector
       bbox_width_px = 80  # example value
       if bbox_width_px < 5:
           return None
       depth = (known_vehicle_width * focal_px) / bbox_width_px
       return np.array([depth, 0.0])   # assume centered (x = depth, y ~ 0)

   # ---------- Run sequential fusion loop ----------
   kf = KalmanFilter(dt=0.1)

   for snap in snapshots:
       kf.predict()
       print(f"After predict  -> cov trace: {np.trace(kf.P):.4f}")

       # LiDAR update
       _, lidar_data = snap['lidar']
       z_lidar = lidar_measurement(lidar_data, ego.get_transform())
       if z_lidar is not None:
           kf.update(z_lidar, R=R_lidar)
           print(f"  + LiDAR      -> cov trace: {np.trace(kf.P):.4f}")

       # RADAR update
       _, radar_data = snap['radar']
       z_radar = radar_measurement(radar_data)
       if z_radar is not None:
           kf.update(z_radar, R=R_radar)
           print(f"  + RADAR      -> cov trace: {np.trace(kf.P):.4f}")

       # Camera update
       _, camera_data = snap['camera']
       z_camera = camera_measurement(camera_data)
       if z_camera is not None:
           kf.update(z_camera, R=R_camera)
           print(f"  + Camera     -> cov trace: {np.trace(kf.P):.4f}")

       print(f"  Fused state: x={kf.x[0]:.2f}, y={kf.x[1]:.2f}, "
             f"vx={kf.x[2]:.2f}, vy={kf.x[3]:.2f}\n")


Task 4: Weather Degradation Experiment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Exercise Tasks
   :class: tip

   1. Run the tracker under three weather conditions: **clear**, **rain**,
      and **fog**. Use ``world.set_weather()`` with CARLA weather presets.

   2. For **rain**: inflate camera :math:`R` by 5x and LiDAR :math:`R` by 2x
      (water droplets degrade both optical and LiDAR signals).

      .. code-block:: python

         R_camera_rain = R_camera * 5.0
         R_lidar_rain  = R_lidar  * 2.0
         R_radar_rain  = R_radar          # unchanged

   3. For **fog**: inflate camera :math:`R` by 10x, LiDAR :math:`R` by 5x,
      keep RADAR :math:`R` unchanged (millimeter waves penetrate fog).

      .. code-block:: python

         R_camera_fog = R_camera * 10.0
         R_lidar_fog  = R_lidar  * 5.0
         R_radar_fog  = R_radar           # unchanged

   4. Plot the covariance trace over time for each weather condition.
      Observe how the KF automatically shifts trust toward RADAR in
      adverse weather because inflated :math:`R` values reduce the Kalman
      gain for degraded sensors.

   5. Compare the fused position estimate error against single-sensor
      estimates under each weather condition. Verify that the fused
      estimate consistently achieves lower error than any individual sensor.

.. note::

   This exercise demonstrates the core fusion concepts used in
   **GP3 (Fusion & Localization)**, where students will implement a full
   EKF fusing GNSS, IMU, and LiDAR for vehicle pose estimation.


Summary
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Fusion Foundations
      :class-card: sd-border-primary

      - Sensors: complementary (camera + LiDAR + RADAR)
      - Architectures: early, intermediate (feature-level), late (decision)
      - Weighted averaging: optimal for independent Gaussian estimates

   .. grid-item-card:: Probabilistic Filters
      :class-card: sd-border-primary

      - KF: linear, Gaussian, optimal
      - EKF: nonlinear via Jacobian, 1st-order
      - UKF: nonlinear via sigma points, 2nd-order, no Jacobian needed
      - PF: arbitrary distributions, high compute
      - Data association: NN, GNN, JPDA, MHT
