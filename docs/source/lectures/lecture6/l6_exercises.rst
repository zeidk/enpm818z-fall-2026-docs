====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 6. Exercises cover Kalman filter fusion, sensor noise
modeling, and multi-sensor integration.


.. dropdown:: Exercise 1 -- Kalman Filter Fusion (Pen and Paper)
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Work through a sequential multi-sensor Kalman filter update by hand
   to see how fusing sensors reduces uncertainty.


   .. raw:: html

      <hr>


   **Specification**

   A vehicle is tracked with state
   :math:`\mathbf{x} = [x, y, v_x, v_y]^T`. Two sensors provide
   measurements:

   - **LiDAR**: measures :math:`(x, y)` with
     :math:`R_L = \text{diag}(0.1, 0.1)`
   - **RADAR**: measures :math:`(x, v_x)` with
     :math:`R_R = \text{diag}(0.5, 0.2)`

   1. Write the **measurement matrix** :math:`H_L` for LiDAR (2 × 4).
   2. Write the **measurement matrix** :math:`H_R` for RADAR (2 × 4).
   3. After the predict step, the state is
      :math:`\hat{\mathbf{x}}^- = [10, 5, 3, 0]^T` with
      :math:`P^- = \text{diag}(1, 1, 0.5, 0.5)`.
      Perform a **sequential update**:

      - First, update with LiDAR measurement
        :math:`z_L = [10.2, 4.8]^T`.
      - Then, update with RADAR measurement
        :math:`z_R = [10.15, 3.1]^T`.

   4. Compute the **trace of** :math:`P` after each update. Does it
      decrease with each sensor? Why?

   **Deliverable**

   Full matrix calculations for both updates, plus trace values.


.. dropdown:: Exercise 2 -- Fusion Architecture Comparison
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Reason about when to use early, intermediate, or late fusion for
   different sensing scenarios.


   .. raw:: html

      <hr>


   **Specification**

   For each scenario below, recommend **early**, **intermediate
   (feature-level)**, or **late (decision-level)** fusion and justify
   in 2--3 sentences.

   .. list-table::
      :widths: 50 20 30
      :header-rows: 1
      :class: compact-table

      * - Scenario
        - Fusion Level
        - Justification
      * - Combining RGB image + LiDAR point cloud for 3D detection
        -
        -
      * - Merging two overlapping RADAR sensors for redundancy
        -
        -
      * - Using camera class label + LiDAR distance for final object list
        -
        -
      * - BEVFusion-style camera-LiDAR fusion for BEV segmentation
        -
        -
      * - Fusing GNSS + IMU for vehicle pose estimation
        -
        -

   **Deliverable**

   Completed table with clear justifications.


.. dropdown:: Exercise 3 -- Sensor Noise Modeling
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Understand how environmental conditions affect measurement noise
   and the downstream impact on Kalman filter behavior.


   .. raw:: html

      <hr>


   **Specification**

   Baseline measurement noise covariances:

   - :math:`R_{\text{camera}} = \text{diag}(5, 5)` pixels
   - :math:`R_{\text{lidar}} = \text{diag}(0.1, 0.1)` m
   - :math:`R_{\text{radar}} = \text{diag}(0.5, 0.2)` m, m/s

   1. Under **heavy rain**, propose multiplicative inflation factors
      for each :math:`R`. Justify each factor in one sentence.
   2. Under **nighttime** conditions, which sensor is most affected?
      Which is completely unaffected? Why?
   3. If :math:`R_{\text{camera}}` is inflated by 10× in fog, how does
      the **Kalman gain** for camera measurements change? Does the
      filter trust the camera more or less?
   4. A colleague suggests setting :math:`R_{\text{camera}} = \infty`
      (i.e., ignoring the camera) in heavy fog. What are the pros and
      cons of this approach?

   **Deliverable**

   Written answers with noise factor table and Kalman gain reasoning.


.. dropdown:: Exercise 4 -- Inverse Variance Weighting
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice the simplest form of sensor fusion: inverse variance
   weighted averaging.


   .. raw:: html

      <hr>


   **Specification**

   Two sensors estimate the position of a vehicle:

   - Sensor A: :math:`x_A = 10.3` m, :math:`\sigma_A = 0.5` m
   - Sensor B: :math:`x_B = 10.8` m, :math:`\sigma_B = 1.5` m

   1. Compute the **inverse variance weighted** fused estimate:

      .. math::

         \hat{x} = \frac{x_A / \sigma_A^2 + x_B / \sigma_B^2}
                        {1 / \sigma_A^2 + 1 / \sigma_B^2}

   2. Compute the **fused standard deviation** :math:`\sigma_f`.
   3. Which sensor contributes more to the final estimate? By what
      ratio?
   4. If Sensor B's noise increases to :math:`\sigma_B = 10` m, what
      does :math:`\hat{x}` converge to? What does this tell you about
      the behavior of inverse variance weighting?

   **Deliverable**

   All calculations shown with final numerical results.


.. dropdown:: Exercise 5 -- Multi-Sensor KF in CARLA
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Implement sequential Kalman filter fusion in CARLA and visualize
   how adding sensors reduces estimation uncertainty.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``multisensor_kf.py`` that performs the following:

   1. Spawn an ego vehicle and a lead vehicle driving ahead in Town03.
   2. Collect synchronized measurements from three sensors:

      - **LiDAR**: nearest cluster centroid distance.
      - **RADAR**: range and range-rate.
      - **Camera**: estimated distance from bounding box width.

   3. Implement a 4-state KF (:math:`[x, y, v_x, v_y]`) with
      **sequential updates**: LiDAR first, then RADAR, then camera.
   4. Log the **trace of** :math:`P` after each sensor update at every
      timestep.
   5. Plot the covariance trace over time for three configurations:

      - LiDAR only
      - LiDAR + RADAR
      - LiDAR + RADAR + camera

   **Expected result**

   The plot should show that adding each sensor progressively reduces
   the covariance trace.

   **Deliverable**

   The script and a plot (PNG or PDF) showing covariance trace for
   all three configurations.
