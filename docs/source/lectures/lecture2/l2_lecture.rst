====================================================
Lecture
====================================================


The Sensor Challenge in ADS
---------------------------

No single sensor technology can meet all the requirements for autonomous
driving. This fundamental limitation drives the need for multi-sensor fusion.

.. admonition:: The Complementarity Principle (Luo, 1989)
   :class: important

   Different sensor technologies have unique strengths and weaknesses that
   balance each other out. By combining them, you can create a perception
   system that is more robust, reliable, and capable than any single sensor
   alone.

.. list-table:: Sensor Capability Comparison
   :widths: 20 20 20 20 20
   :header-rows: 1
   :class: compact-table

   * - Capability
     - Camera
     - LiDAR
     - RADAR
     - IMU/GNSS
   * - Day/Night
     - Fair
     - Good
     - Good
     - N/A
   * - Adverse Weather
     - Poor
     - Fair
     - Good
     - N/A
   * - Object Classification
     - Excellent
     - Poor
     - Poor
     - N/A
   * - Range Accuracy
     - Poor (mono)
     - Excellent
     - Good
     - Moderate
   * - Velocity Measurement
     - Poor
     - Fair
     - Excellent
     - Good
   * - Angular Resolution
     - Excellent
     - Good
     - Poor
     - N/A
   * - Cost
     - Low
     - High
     - Medium
     - Medium


Sensor Technologies Deep Dive
------------------------------

Camera Systems
~~~~~~~~~~~~~~

Cameras provide the richest semantic information of any AV sensor. They are
the **only** sensor that can reliably read traffic lights and signs.

**How cameras are used in autonomous driving:**

- **Object classification and recognition** -- Deep learning classifies
  objects (cars, pedestrians, cyclists, traffic cones).
- **Semantic segmentation and lane detection** -- Pixel-level understanding
  of road, sidewalk, sky.
- **Traffic light and sign recognition** -- Color and detail interpretation
  that no other sensor can provide.

**Key technical specifications:**

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Resolution**
     - 1--12+ MP. Critical for identifying small or distant objects.
   * - **Frame Rate**
     - 30--60 Hz. Essential for tracking fast-moving objects.
   * - **Dynamic Range**
     - 120+ dB. Ability to see detail in both shadows and highlights.
   * - **Field of View**
     - 30--180 degrees. Mix of narrow (telephoto) and wide (fisheye).

**Camera types:**

.. tab-set::

   .. tab-item:: Telephoto (Long-Range)

      - Narrow FOV for highway driving and high-speed ACC.
      - **Example:** Tesla HW4 upgraded to ~5 MP cameras.
      - **Suppliers:** Bosch (MPC3), Continental, Magna.

   .. tab-item:: Fisheye (Wide-Angle)

      - Essential for 360-degree awareness, parking, cross-traffic.
      - **Example:** Waymo custom "perimeter" cameras for full surround view.
      - **Suppliers:** Valeo (surround-view systems, bird's-eye view).

   .. tab-item:: Stereo

      - Two cameras for geometric depth via triangulation.
      - **Depth formula:** ``depth = (B x f) / d``

        - ``B`` = baseline (distance between cameras)
        - ``f`` = focal length
        - ``d`` = disparity (pixel difference between left/right projections)

      - **Example:** Subaru EyeSight -- stereo vision for AEB and ACC.

   .. tab-item:: Monocular Depth

      - Infers 3D depth from a single 2D image using deep neural networks.
      - Learns perspective, relative size, and semantic context.
      - **Pros:** Single inexpensive camera.
      - **Cons:** Estimation (not measurement); scale ambiguity.

**Performance degradation factors:** Low light (noise, blur), rain (distortion),
snow/fog (contrast loss), direct sunlight (flare, oversaturation).


LiDAR Systems
~~~~~~~~~~~~~

LiDAR provides precise 3D geometry, independent of lighting conditions.

**How LiDAR is used:**

- **Object detection** -- Precise 3D bounding boxes (shape, size, location).
- **Localization** -- Matching live scans to HD maps for centimeter-level
  accuracy.
- **Free space detection** -- Distinguishing solid objects from drivable space.

**Operating principle -- Time-of-Flight (ToF):**

.. math::

   \text{distance} = \frac{c \times \Delta t}{2}

where :math:`c` is the speed of light and :math:`\Delta t` is the round-trip
time of the laser pulse.

**Key specifications:**

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Range**
     - 10 m -- 250+ m
   * - **Points per Second**
     - 300K -- 2M+
   * - **Accuracy**
     - +/- 2--5 cm
   * - **Beams/Lines**
     - 16 -- 128

.. tab-set::

   .. tab-item:: Mechanical Spinning

      - Physically spinning laser diodes for 360-degree FOV.
      - **Example:** Velodyne "puck" sensors.
      - **Pros:** Full 360-degree view.
      - **Cons:** Large, expensive, moving parts wear out.

   .. tab-item:: Solid-State

      - MEMS mirrors or electronic beam steering; no large moving parts.
      - **Examples:** Luminar (Volvo/Mercedes), Innoviz (BMW).
      - **Pros:** Compact, robust, affordable for mass production.
      - **Cons:** Limited forward-facing FOV.

**Limitations:** Adverse weather (laser absorbed/scattered by particles),
low-reflectivity surfaces (dark/matte materials absorb laser light).


RADAR Systems
~~~~~~~~~~~~~

RADAR excels in all-weather operation and direct velocity measurement.

**How RADAR is used:**

- **Long-range tracking (ACC)** -- Excellent range and weather immunity.
- **Blind spot monitoring** -- Short-range RADARs at vehicle corners.
- **Redundant collision warning** -- Backup when camera/LiDAR are degraded.

**Key strength -- Doppler Effect:**

Moving objects create a clear Doppler shift, making them easy to detect even
in clutter. However, stationary objects produce no shift and are often filtered
out -- a known safety risk.

**Key specifications:**

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Frequency**
     - 77 GHz (automotive standard); 79 GHz for imaging radar.
   * - **Range Resolution**
     - 0.1--1.0 m.
   * - **Angular Resolution**
     - 1--10 degrees (RADAR's main weakness).
   * - **Velocity Accuracy**
     - +/- 0.1 km/h.

**Limitations:** Low angular resolution (car and motorcycle at same distance
look like one "blob"), multipath reflections ("ghost" objects), stationary
object filtering (risk of not detecting stopped vehicles).


IMU and GNSS
~~~~~~~~~~~~

**IMU (Inertial Measurement Unit):**

- Measures linear acceleration (accelerometers) and angular velocity
  (gyroscopes).
- **Strength:** High-frequency (>100 Hz), continuous relative motion updates.
- **Weakness (drift):** Small errors integrate over time, causing unbounded
  position error growth.

**GNSS (Global Navigation Satellite System):**

- Measures absolute position (latitude, longitude, altitude).
- **Strength:** Global position reference that does not drift.
- **Weaknesses:** Low update rate (1--20 Hz), signal blockage in tunnels and
  urban canyons, multipath from buildings.

**IMU + GNSS fusion:**

- IMU provides smooth high-frequency motion estimates between GPS fixes.
- GNSS provides periodic absolute corrections to prevent IMU drift.
- This is the foundation of nearly all modern vehicle navigation systems and
  a textbook application of the Kalman Filter.


Sensor Calibration
------------------

Calibration is the process of determining the parameters that relate sensor
measurements to the physical world. Without proper calibration, multi-sensor
fusion is impossible.

Intrinsic Calibration
~~~~~~~~~~~~~~~~~~~~~

Determines the internal parameters of a camera:

.. math::

   K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}

- :math:`f_x, f_y` -- focal lengths in pixels.
- :math:`c_x, c_y` -- principal point (optical center).
- **Distortion coefficients** (:math:`k_1, k_2, k_3, p_1, p_2`) model lens
  distortion.

**Methods:** Checkerboard or AprilTag patterns with OpenCV, MATLAB, or Kalibr.

**Validation:** Reprojection error should be < 2 pixels.


Extrinsic Calibration
~~~~~~~~~~~~~~~~~~~~~

Determines the 6-DOF transformation (rotation + translation) between sensors
or between a sensor and the vehicle frame.

- Essential for projecting LiDAR points onto camera images.
- Essential for fusing detections from multiple sensors into a common
  coordinate frame.

**Methods:** Target-based (checkerboard visible to both sensors),
targetless (mutual information), tools (OpenCV, Kalibr, Autoware calibration
toolkit).

.. important::

   Poor calibration is one of the most common causes of fusion failure.
   A 1-degree rotation error at 100 m range produces a 1.7 m positional
   error.


System Design & Integration
----------------------------

Sensor Placement and Coverage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Coverage requirements:**

- **360-degree awareness** with no blind spots.
- **Range diversity:** near-field (<30 m), mid-field (30--80 m), far-field
  (80+ m).
- **Redundancy** in critical areas (forward direction needs Camera + LiDAR +
  RADAR).
- **Overlap zones** for robust fusion and seamless tracking.

**Common placement patterns:**

.. list-table::
   :widths: 20 80
   :class: compact-table

   * - **Forward**
     - Long-range RADAR + telephoto camera + primary LiDAR.
   * - **Side**
     - Short-range RADARs for blind spots + fisheye cameras.
   * - **Rear**
     - Rear-view camera + short-range RADARs for cross-traffic.


Failure Mode Analysis
~~~~~~~~~~~~~~~~~~~~~

- **Single point of failure** -- Avoid by ensuring redundancy. If forward
  LiDAR fails in snow, RADAR must still detect stopped vehicles.
- **Degraded mode operation** -- Define minimum sensor set for safe operation.
  Example: disable lane-keeping but keep ACC at lower speed with RADAR only.
- **Detection and notification** -- Constant self-diagnostics. If data is
  missing or wildly inconsistent, alert the driver or execute a Minimal Risk
  Condition (MRC) maneuver (pull over safely).


Design Trade-Offs Discussion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Highway Priority ($5K Budget)

      - **Primary ($2,000):** High-quality long-range RADAR for all-weather ACC.
      - **Secondary ($1,500):** High-resolution telephoto camera for classification.
      - **Tertiary ($1,000):** Forward solid-state LiDAR for stationary objects.
      - **Ancillary ($500):** Basic side sensors for blind-spot monitoring.

   .. tab-item:: Urban Priority ($5K Budget)

      - **Primary ($2,000):** Four corner RADARs for 360-degree awareness.
      - **Secondary ($1,500):** Surround-view camera system (4--6 cameras).
      - **Tertiary ($500):** Standard forward ADAS module for low-speed AEB.
      - **Omitted:** LiDAR sacrificed to afford essential 360-degree coverage.


Industry Sensor Configurations
------------------------------

.. list-table::
   :widths: 20 20 15 15 15 15
   :header-rows: 1
   :class: compact-table

   * - Company
     - Philosophy
     - Cameras
     - LiDARs
     - RADARs
     - GNSS/IMU
   * - **Waymo**
     - LiDAR-centric
     - 29
     - 5
     - 6
     - Yes
   * - **Tesla**
     - Vision-only
     - 8
     - 0
     - 0
     - Yes
   * - **Cruise**
     - Multi-sensor
     - 21
     - 5
     - 5
     - Yes
   * - **Aurora**
     - Long-range LiDAR
     - Yes
     - FirstLight (400 m+)
     - Imaging
     - Yes
   * - **Mobileye**
     - Camera-first
     - 8--11
     - Optional
     - Optional
     - Yes

.. tip::

   There is no universal "best" sensor configuration. The right choice depends
   on the ODD, cost constraints, and the fusion architecture.
