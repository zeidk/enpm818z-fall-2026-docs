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


Kalman Filter
--------------

The **Kalman Filter (KF)** is the optimal linear state estimator under
Gaussian noise assumptions. It tracks a hidden state :math:`\mathbf{x}` by
alternating between **predict** and **update** steps.

State Space Model
~~~~~~~~~~~~~~~~~~

.. math::

   \text{Process model:} \quad \mathbf{x}_k = F_k \mathbf{x}_{k-1} + B_k \mathbf{u}_k + \mathbf{w}_k, \quad \mathbf{w}_k \sim \mathcal{N}(0, Q_k)

   \text{Measurement model:} \quad \mathbf{z}_k = H_k \mathbf{x}_k + \mathbf{v}_k, \quad \mathbf{v}_k \sim \mathcal{N}(0, R_k)

where:

- :math:`\mathbf{x}_k` -- state vector (e.g., position, velocity)
- :math:`F_k` -- state transition matrix
- :math:`\mathbf{u}_k` -- control input; :math:`B_k` -- control matrix
- :math:`Q_k` -- process noise covariance
- :math:`\mathbf{z}_k` -- measurement vector
- :math:`H_k` -- measurement matrix (maps state to measurement space)
- :math:`R_k` -- measurement noise covariance

Predict Step
~~~~~~~~~~~~~

.. math::

   \hat{\mathbf{x}}_{k|k-1} = F_k \hat{\mathbf{x}}_{k-1|k-1} + B_k \mathbf{u}_k

   P_{k|k-1} = F_k P_{k-1|k-1} F_k^T + Q_k

The prior state estimate :math:`\hat{\mathbf{x}}_{k|k-1}` and its uncertainty
:math:`P_{k|k-1}` are propagated forward using the process model. Uncertainty
grows (P increases) as we predict further ahead without new measurements.

Update Step
~~~~~~~~~~~~

.. math::

   K_k = P_{k|k-1} H_k^T \left( H_k P_{k|k-1} H_k^T + R_k \right)^{-1}

   \hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + K_k \left( \mathbf{z}_k - H_k \hat{\mathbf{x}}_{k|k-1} \right)

   P_{k|k} = (I - K_k H_k) P_{k|k-1}

The **innovation** :math:`\tilde{\mathbf{y}}_k = \mathbf{z}_k - H_k \hat{\mathbf{x}}_{k|k-1}`
is the discrepancy between the predicted measurement and the actual measurement.
The posterior state estimate corrects the prior by a weighted fraction of the
innovation.

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


CARLA Hands-On: Camera + LiDAR + RADAR Fusion
------------------------------------------------

In the CARLA assignment, you will implement a simplified late-fusion pipeline:

.. code-block:: python

   import carla
   import numpy as np

   # 1. Spawn sensors
   world = client.get_world()
   bp_lib = world.get_blueprint_library()

   camera_bp = bp_lib.find('sensor.camera.rgb')
   lidar_bp = bp_lib.find('sensor.lidar.ray_cast')
   radar_bp = bp_lib.find('sensor.other.radar')

   camera_bp.set_attribute('image_size_x', '1280')
   camera_bp.set_attribute('image_size_y', '720')
   lidar_bp.set_attribute('channels', '64')
   lidar_bp.set_attribute('range', '100')
   radar_bp.set_attribute('horizontal_fov', '30')
   radar_bp.set_attribute('range', '100')

   # 2. Attach to ego vehicle
   camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
   lidar_transform  = carla.Transform(carla.Location(x=0.0, z=2.4))
   radar_transform  = carla.Transform(carla.Location(x=2.0, z=1.0))

   camera = world.spawn_actor(camera_bp, camera_transform, attach_to=ego)
   lidar  = world.spawn_actor(lidar_bp,  lidar_transform,  attach_to=ego)
   radar  = world.spawn_actor(radar_bp,  radar_transform,  attach_to=ego)

   # 3. Fusion: inverse-variance weighting on range estimates
   def fuse_range(lidar_range, lidar_var, radar_range, radar_var):
       w_lidar = 1.0 / lidar_var
       w_radar = 1.0 / radar_var
       return (w_lidar * lidar_range + w_radar * radar_range) / (w_lidar + w_radar)

.. note::

   The full assignment will guide you through synchronizing sensor timestamps,
   projecting LiDAR points onto the camera image, and implementing a simple
   Kalman filter for object tracking across frames.


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
