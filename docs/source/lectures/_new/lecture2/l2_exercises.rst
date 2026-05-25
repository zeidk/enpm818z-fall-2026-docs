====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 2. Exercises cover sensor characteristics, calibration
math, and hands-on CARLA sensor work.


.. dropdown:: Exercise 1 -- Sensor Trade-Off Analysis
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Build intuition for the strengths and weaknesses of each sensor
   modality used in autonomous driving.


   .. raw:: html

      <hr>


   **Specification**

   Complete the following comparison table using values from the lecture
   or reasonable estimates.

   .. list-table::
      :widths: 20 16 16 16 16 16
      :header-rows: 1
      :class: compact-table

      * - Property
        - Camera
        - LiDAR
        - RADAR
        - IMU
        - GNSS
      * - Max range (m)
        -
        -
        -
        -
        -
      * - Angular resolution
        -
        -
        -
        -
        -
      * - Works in heavy rain?
        -
        -
        -
        -
        -
      * - Works at night?
        -
        -
        -
        -
        -
      * - Provides velocity?
        -
        -
        -
        -
        -
      * - Relative cost
        -
        -
        -
        -
        -

   Below the table, write a short paragraph (3--5 sentences) explaining
   why **no single sensor** is sufficient for an L4 ADS.

   **Deliverable**

   Completed table and written explanation.


.. dropdown:: Exercise 2 -- Intrinsic Matrix Computation
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice computing the camera intrinsic matrix from CARLA sensor
   parameters and projecting a 3D point to pixel coordinates.


   .. raw:: html

      <hr>


   **Specification**

   A CARLA camera has the following parameters:

   - Image width: ``1280`` pixels
   - Image height: ``720`` pixels
   - Field of view: ``90°``

   1. Compute the focal length:

      .. math::

         f_x = f_y = \frac{w}{2 \tan(\text{fov} / 2)}

   2. Write the full **3 × 3 intrinsic matrix** :math:`K`. Show all
      entries.

   3. A 3D point in camera coordinates is located at
      :math:`\mathbf{p}_c = (5, 0, 10)` (x = 5 m right, y = 0 m,
      z = 10 m forward). Project it using:

      .. math::

         \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \frac{1}{z} K \, \mathbf{p}_c

      Report the pixel coordinates :math:`(u, v)`.

   4. Is this point inside the image bounds? Show your reasoning.

   **Deliverable**

   Handwritten or typed solution showing all intermediate steps.


.. dropdown:: Exercise 3 -- Extrinsic Calibration
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice constructing SE(3) extrinsic transformation matrices
   between sensors on an autonomous vehicle.


   .. raw:: html

      <hr>


   **Specification**

   A LiDAR is mounted on the vehicle roof at position
   ``(0, 0, 2.5)`` m relative to the vehicle frame, with no rotation.
   A front-facing camera is mounted at ``(2.0, 0, 1.5)`` m with a
   **10° downward pitch** (rotation about the x-axis).

   1. Write the **4 × 4 extrinsic matrix**
      :math:`T_{\text{lidar}}^{\text{vehicle}}` for the LiDAR.

   2. Write the **4 × 4 extrinsic matrix**
      :math:`T_{\text{camera}}^{\text{vehicle}}` for the camera.
      Include the rotation matrix for a 10° pitch.

   3. Derive the transform
      :math:`T_{\text{lidar}}^{\text{camera}} = (T_{\text{camera}}^{\text{vehicle}})^{-1} \cdot T_{\text{lidar}}^{\text{vehicle}}`
      that converts a point from LiDAR coordinates to camera
      coordinates.

   4. Transform the LiDAR point :math:`(10, 0, 0.5)` into camera
      coordinates using :math:`T_{\text{lidar}}^{\text{camera}}`.

   **Deliverable**

   All three 4 × 4 matrices written out with numerical entries, plus
   the transformed point.


.. dropdown:: Exercise 4 -- Sensor Degradation Experiment
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Investigate how weather conditions affect LiDAR point cloud density
   in simulation vs. reality.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``sensor_degradation.py`` that performs the
   following:

   1. Spawn an ego vehicle with a LiDAR sensor
      (``sensor.lidar.ray_cast``, 64 channels, 10 Hz, 100 m range)
      in Town03.
   2. For each weather condition below, set the weather and record the
      **number of points returned** per scan for **10 consecutive
      frames**:

      - ``ClearNoon``
      - ``HardRainNoon``
      - ``SoftFogNoon``

   3. Print the **mean and standard deviation** of point counts per
      condition.

   **Written analysis**

   Answer the following:

   - Does the point count change across weather conditions in CARLA?
   - On real LiDAR hardware, heavy rain can reduce point returns by
     **20--40%**. Why does CARLA's ray-cast LiDAR not model this?
   - What implications does this have for sim-to-real transfer of
     perception algorithms?

   **Deliverable**

   The script, printed results table, and written analysis (5--8
   sentences).


.. dropdown:: Exercise 5 -- LiDAR-to-Camera Projection
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Combine the intrinsic and extrinsic matrices from Exercises 2 and 3
   to project LiDAR points onto a camera image.


   .. raw:: html

      <hr>


   **Specification**

   Using the intrinsic matrix :math:`K` from Exercise 2 and the
   extrinsic transform :math:`T_{\text{lidar}}^{\text{camera}}` from
   Exercise 3, project the following LiDAR points onto the image plane.

   .. list-table::
      :widths: 25 25 25 25
      :header-rows: 1
      :class: compact-table

      * - Point (x, y, z) in LiDAR
        - Point in camera frame
        - Pixel (u, v)
        - In image bounds?
      * - (10.0, 0.0, 0.5)
        -
        -
        -
      * - (20.0, 3.0, -0.5)
        -
        -
        -
      * - (-5.0, 0.0, 0.5)
        -
        -
        -

   1. Complete the table by transforming each point to camera
      coordinates, then projecting to pixels.
   2. Which points are **behind the camera** (negative z in camera
      frame) and should be filtered out?
   3. Which points fall **outside the image bounds** (1280 × 720)?

   **Deliverable**

   Completed table with all intermediate values shown.
