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

.. admonition:: Recall from ENPM673
   :class: tip

   You already learned intrinsic camera calibration in detail. The camera
   matrix :math:`K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}`
   encodes focal lengths, principal point, and skew. Distortion coefficients
   and checkerboard-based calibration were covered there as well.


Extrinsic Calibration
~~~~~~~~~~~~~~~~~~~~~

Extrinsic calibration determines the **6-DOF rigid-body transformation**
(3 rotation + 3 translation parameters) between two sensor coordinate frames
or between a sensor and the vehicle body frame. This is the critical step that
enables multi-sensor fusion.

**Notation.** Frame conventions are the single most common source of
sign and ordering errors in fusion code, so we fix one convention and use
it for the rest of the course:

.. admonition:: Convention used throughout ENPM818Z
   :class: important

   :math:`T_{A \leftarrow B}` denotes the transform that takes a point
   **expressed in frame** :math:`B` and returns it **expressed in frame**
   :math:`A`. Read the arrow right-to-left, as "A from B."

   Composition then chains naturally, with the inner frames cancelling:

   .. math::

      T_{A \leftarrow C} = T_{A \leftarrow B} \; T_{B \leftarrow C}

   and inversion flips the arrow:
   :math:`T_{B \leftarrow A} = \left(T_{A \leftarrow B}\right)^{-1}`.

The transform is a 4 x 4 homogeneous matrix:

.. math::

   T_{A \leftarrow B} = \begin{bmatrix} R & t \\ 0 & 1 \end{bmatrix} \in SE(3)

where :math:`R \in SO(3)` is a 3 x 3 rotation matrix and
:math:`t \in \mathbb{R}^3` is the translation vector. To transform a point
:math:`\mathbf{p}_B` expressed in frame :math:`B` into frame :math:`A`:

.. math::

   \mathbf{p}_A = R \, \mathbf{p}_B + t

**Example -- LiDAR-to-camera projection:**

To project a LiDAR point into a camera image, chain the extrinsic and
intrinsic transforms. Calibration typically gives you each sensor's pose
**in the vehicle frame**, i.e. :math:`T_{V \leftarrow L}` and
:math:`T_{V \leftarrow C}`. The transform you need is:

.. math::

   T_{C \leftarrow L}
     = T_{C \leftarrow V} \; T_{V \leftarrow L}
     = \left(T_{V \leftarrow C}\right)^{-1} T_{V \leftarrow L}

Note how the inner :math:`V` cancels -- if the frames in your chain do not
cancel like this, the composition is wrong. A 3-D LiDAR point
:math:`\mathbf{p}_L` then projects to pixel coordinates via:

.. math::

   \mathbf{u} = \pi\!\left(K \; T_{C \leftarrow L} \; \mathbf{p}_L\right)

where :math:`\pi` applies the perspective division and :math:`K` is the
camera intrinsic matrix.

.. warning::

   :math:`K` assumes the **optical** convention: :math:`x` right,
   :math:`y` down, :math:`z` **forward along the optical axis**. Many
   robotics and game-engine frames (including CARLA's) instead use
   :math:`x` forward, :math:`y` right, :math:`z` up. Applying :math:`K`
   to a point in that frame silently produces garbage. See the CARLA
   exercise at the end of this lecture for the required axis
   permutation.

**Calibration methods:**

.. tab-set::

   .. tab-item:: Target-Based

      - Place a calibration target (checkerboard, AprilTag board, or custom
        3-D target) that is **visible to both sensors simultaneously**.
      - Correspondences between sensor detections are established
        automatically and a least-squares optimization solves for
        :math:`[R \mid t]`.
      - **Pros:** High accuracy (sub-degree rotation, sub-centimeter
        translation) when enough poses are collected.
      - **Cons:** Requires a controlled setup; difficult to repeat in the
        field.

   .. tab-item:: Targetless (Automatic)

      - Exploits **mutual information**, edge alignment, or learned feature
        matching between overlapping sensor data (e.g., LiDAR intensity vs.
        camera image edges).
      - Does not require a physical target -- can run on natural scenes.
      - **Pros:** Convenient; can be run on recorded driving data.
      - **Cons:** Lower accuracy than target-based; sensitive to scene
        structure and initialization.

   .. tab-item:: Motion-Based

      - Uses ego-motion estimated independently by each sensor (e.g.,
        visual odometry and LiDAR odometry) and solves the hand-eye
        calibration problem :math:`AX = XB`.
      - Requires sufficient rotational and translational excitation in the
        trajectory.
      - **Pros:** No target needed; works with any sensor pair that
        estimates ego-motion.
      - **Cons:** Requires good odometry from both sensors; degenerate
        motions (e.g., straight-line driving) yield poor results.

**Common calibration tools:**

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Tool
     - Description
   * - **OpenCV** ``stereoCalibrate``
     - Jointly calibrates intrinsics and extrinsics of a stereo camera pair
       or camera-projector system using checkerboard detections.
   * - **Kalibr**
     - ETH Zurich toolkit for multi-camera and camera-IMU calibration using
       AprilTag grids. Widely used in robotics research.
   * - **Autoware Calibration Toolkit**
     - Open-source tools for LiDAR-camera, LiDAR-LiDAR, and ground-plane
       calibration designed for autonomous driving stacks.
   * - **MATLAB Lidar Toolbox**
     - Interactive checkerboard-based LiDAR-camera calibration with
       visualization and error analysis.

**Online (runtime) re-calibration:**

Extrinsic parameters can drift over time due to vibration, thermal expansion,
or mechanical shock. Modern AV stacks therefore include **online
re-calibration** modules that continuously refine :math:`T` while driving:

- Monitor reprojection consistency between LiDAR points and camera features.
- Apply small incremental corrections using sliding-window optimization.
- Flag large deviations for human review or safe stop.

.. important::

   Poor calibration is one of the most common causes of fusion failure.
   A 1-degree rotation error at 100 m range produces a **1.7 m positional
   error**. Always validate calibration with quantitative reprojection
   metrics before deploying a multi-sensor system.


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
   * - **Zoox**
     - Purpose-built, symmetric
     - Yes
     - Yes (4 corners)
     - Yes
     - Yes

.. note::

   Sensor counts are **generation-specific and change often**. The Waymo
   figures above describe the 5th-generation Driver; the 6th-generation
   Driver deliberately reduced sensor count to cut cost. Tesla removed
   radar in 2021--2022 but has since reintroduced a high-definition radar
   on some HW4 vehicles. Treat every row here as a snapshot, and check
   the manufacturer's current published specification before relying on
   a number.

.. tip::

   There is no universal "best" sensor configuration. The right choice depends
   on the ODD, cost constraints, and the fusion architecture.


Sensor Fusion Preview
---------------------

The full treatment of sensor fusion -- fusion architectures, the Kalman
filter family, and data association -- is the subject of
**L3: Probabilistic State Estimation & Fusion**. This section establishes
only the one idea you need in order to reason about *sensor placement*,
which is what the rest of this lecture is about: **why** combining sensors
helps at all.

Sensor Relationships
~~~~~~~~~~~~~~~~~~~~

The Complementarity Principle (Luo, 1989) classifies sensor relationships
into three categories. This taxonomy drives placement decisions: it tells
you whether adding a sensor buys you *new information*, *fault tolerance*,
or *a new measurement type*.

.. tab-set::

   .. tab-item:: Complementary

      Sensors provide **different pieces of the puzzle**. Each covers a gap
      the other cannot.

      - **Example:** Camera (color, text, classification) + LiDAR (precise 3D
        shape and range). Neither alone is sufficient for robust perception.
      - **Placement consequence:** their fields of view must *overlap* in
        the regions where you need both properties at once.

   .. tab-item:: Competitive (Redundant)

      Sensors provide the **same type of information** for reliability and
      safety.

      - **Example:** Two forward-facing cameras. If one is blinded by sun
        glare, the other may still function. Redundancy prevents single points
        of failure.
      - **Placement consequence:** redundant sensors should fail
        *independently* -- mounting two cameras side by side means one sun
        angle blinds both.

   .. tab-item:: Cooperative

      Sensors **work together** to create new information that neither could
      produce alone.

      - **Example:** Two cameras forming a stereo pair to compute geometric
        depth via triangulation.
      - **Placement consequence:** the geometry *is* the measurement --
        stereo depth resolution is set directly by the baseline.

.. admonition:: Why Is Fusion Essential?
   :class: important

   - **Improved accuracy** -- Combining measurements reduces overall
     uncertainty.
   - **Increased reliability** -- Redundancy provides fault tolerance.
   - **Extended coverage** -- Different sensors work in different conditions
     (rain, night, tunnel).
   - **Complementary information** -- Each sensor provides unique data types.

.. seealso::

   **Deferred to L3, deliberately.** Fusion architectures (early /
   intermediate / late), inverse-variance weighting, the Kalman filter,
   EKF, UKF, particle filters, and data association are all developed
   there, where they can be treated properly rather than previewed. Do
   not expect to be able to fuse anything after this lecture -- expect to
   be able to *place sensors so that fusion is possible*.


Discussion: Design Trade-Offs
------------------------------

The following discussion questions are explored during the lecture. They
reinforce the core tension between performance, cost, safety, and
real-time constraints in AV sensor system design.

Safety and Graceful Degradation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A robust AV must anticipate and safely handle the failure of any single
sensor:

- **Redundant sensing** -- Critical zones (especially forward) must be
  covered by at least two different sensor modalities (e.g., RADAR + Camera)
  to avoid a single point of failure.
- **Decentralized detection** -- Each sensor subsystem generates its own
  object list. If one sensor fails, the central fusion unit ignores its
  list and continues -- enabling graceful degradation.
- **Cross-validation** -- The fusion algorithm performs plausibility checks.
  If RADAR and camera disagree for a sustained period, a fault is flagged
  and trust in the inconsistent sensor is reduced.
- **Health monitoring and fail-safes** -- Constant self-diagnostics. If a
  critical sensor fails, the system executes a pre-planned Minimal Risk
  Condition (MRC) -- e.g., safely pulling over and stopping.


Adapting to Environmental Change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The key to adaptation is dynamically adjusting the **trust** placed in each
sensor as conditions change. In a Kalman Filter framework, this is done by
modifying the measurement noise covariance matrix :math:`R`:

1. **Classify environment** -- Detect adverse conditions using available
   sensor data (camera sees rain, wipers are active, LiDAR point density
   drops).
2. **Adjust uncertainty** -- Increase :math:`R` for degraded sensors (e.g.,
   camera in sun glare, LiDAR in dense fog).
3. **Automatic re-weighting** -- A higher :math:`R` produces a lower Kalman
   Gain :math:`K`, so the filter naturally de-weights the unreliable sensor
   and relies more on its prediction and other sensors (like RADAR).

This mechanism allows the fusion system to **gracefully adapt** without
needing separate hard-coded logic for every weather condition.


Real-Time Constraints
~~~~~~~~~~~~~~~~~~~~~~

Fusion algorithms for embedded automotive systems must be both accurate and
efficient to meet real-time deadlines:

- **Choose the right tool** -- Use the simplest algorithm that works. An
  Unscented Kalman Filter (UKF) often provides the best accuracy/cost
  trade-off for non-linear systems without the expense of a Particle Filter.
- **Efficient association** -- Use "gating" techniques to quickly discard
  unlikely measurement-to-track pairings, avoiding unnecessary computation.
- **State vector simplicity** -- Only track what is necessary. A simple
  state (position, velocity) is much faster than a complex one.
- **Hardware acceleration** -- Offload matrix math to DSPs or GPUs.
- **Smart scheduling** -- Use a Real-Time Operating System (RTOS) to give
  core fusion tasks the highest priority at a consistent frequency
  (e.g., 50 Hz).


CARLA Hands-On: Sensor Exploration
------------------------------------

This exercise introduces the CARLA Python API by spawning a vehicle,
attaching sensors, and visualizing their output. It provides hands-on
experience with the sensors discussed in this lecture.


Task 1: Spawn a Vehicle and Attach Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import carla
   import numpy as np
   import time

   # ── Connect to CARLA ──────────────────────────────────────────────
   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   world = client.get_world()
   bp_lib = world.get_blueprint_library()

   # ── Spawn ego vehicle ─────────────────────────────────────────────
   vehicle_bp = bp_lib.find('vehicle.tesla.model3')
   spawn_point = world.get_map().get_spawn_points()[0]
   vehicle = world.spawn_actor(vehicle_bp, spawn_point)
   vehicle.set_autopilot(True)
   print(f"Spawned vehicle: {vehicle.type_id} at {spawn_point.location}")

   # ── Attach an RGB camera ──────────────────────────────────────────
   camera_bp = bp_lib.find('sensor.camera.rgb')
   camera_bp.set_attribute('image_size_x', '1280')
   camera_bp.set_attribute('image_size_y', '720')
   camera_bp.set_attribute('fov', '90')
   camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
   camera = world.spawn_actor(camera_bp, camera_transform,
                              attach_to=vehicle)

   # ── Attach a LiDAR sensor ─────────────────────────────────────────
   lidar_bp = bp_lib.find('sensor.lidar.ray_cast')
   lidar_bp.set_attribute('channels', '64')
   lidar_bp.set_attribute('range', '100.0')
   lidar_bp.set_attribute('points_per_second', '1200000')
   lidar_bp.set_attribute('rotation_frequency', '20')
   lidar_transform = carla.Transform(carla.Location(x=0.0, z=2.5))
   lidar = world.spawn_actor(lidar_bp, lidar_transform,
                             attach_to=vehicle)

   # ── Attach a RADAR sensor ─────────────────────────────────────────
   radar_bp = bp_lib.find('sensor.other.radar')
   radar_bp.set_attribute('horizontal_fov', '30')
   radar_bp.set_attribute('vertical_fov', '10')
   radar_bp.set_attribute('range', '100')
   radar_transform = carla.Transform(carla.Location(x=2.0, z=1.0))
   radar = world.spawn_actor(radar_bp, radar_transform,
                             attach_to=vehicle)

   # ── Attach IMU and GNSS ────────────────────────────────────────────
   imu = world.spawn_actor(
       bp_lib.find('sensor.other.imu'),
       carla.Transform(), attach_to=vehicle)
   gnss = world.spawn_actor(
       bp_lib.find('sensor.other.gnss'),
       carla.Transform(), attach_to=vehicle)

   print("All sensors attached. Vehicle running on autopilot.")


Task 2: Collect and Visualize Sensor Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import cv2

   # ── Camera callback: save and display images ──────────────────────
   def camera_callback(image):
       array = np.frombuffer(image.raw_data, dtype=np.uint8)
       array = array.reshape((image.height, image.width, 4))[:, :, :3]
       cv2.imshow("CARLA Camera", array)
       cv2.waitKey(1)

   camera.listen(camera_callback)

   # ── LiDAR callback: print point cloud stats ───────────────────────
   def lidar_callback(point_cloud):
       data = np.frombuffer(point_cloud.raw_data, dtype=np.float32)
       points = data.reshape(-1, 4)  # x, y, z, intensity
       print(f"[LiDAR] Frame {point_cloud.frame}: "
             f"{points.shape[0]} points, "
             f"range: {np.linalg.norm(points[:, :3], axis=1).max():.1f} m")

   lidar.listen(lidar_callback)

   # ── RADAR callback: show detections with velocity ──────────────────
   def radar_callback(radar_data):
       detections = []
       for d in radar_data:
           detections.append({
               'altitude': np.degrees(d.altitude),
               'azimuth': np.degrees(d.azimuth),
               'depth': d.depth,
               'velocity': d.velocity
           })
       if detections:
           print(f"[RADAR] Frame {radar_data.frame}: "
                 f"{len(detections)} detections, "
                 f"closest: {min(d['depth'] for d in detections):.1f} m")

   radar.listen(radar_callback)

   # ── IMU callback ───────────────────────────────────────────────────
   def imu_callback(imu_data):
       print(f"[IMU] Accel: ({imu_data.accelerometer.x:.2f}, "
             f"{imu_data.accelerometer.y:.2f}, "
             f"{imu_data.accelerometer.z:.2f}) m/s^2  "
             f"Gyro: ({imu_data.gyroscope.x:.3f}, "
             f"{imu_data.gyroscope.y:.3f}, "
             f"{imu_data.gyroscope.z:.3f}) rad/s")

   imu.listen(imu_callback)

   # ── GNSS callback ─────────────────────────────────────────────────
   def gnss_callback(gnss_data):
       print(f"[GNSS] Lat: {gnss_data.latitude:.6f}, "
             f"Lon: {gnss_data.longitude:.6f}, "
             f"Alt: {gnss_data.altitude:.2f}")

   gnss.listen(gnss_callback)


Task 3: Project LiDAR Points onto the Camera Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This exercise demonstrates **extrinsic calibration** in practice -- using the
known sensor transforms to project 3D LiDAR points into the camera image.

.. code-block:: python

   def lidar_to_camera_projection(lidar_data, camera_data, camera_actor):
       """Project LiDAR points onto a camera image.

       The one step that is easy to miss: CARLA's transform matrices use
       the Unreal Engine convention (x FORWARD, y RIGHT, z UP), but the
       intrinsic matrix K assumes the optical convention (x right,
       y down, z forward). A permutation between the two is mandatory.
       """
       # Parse LiDAR point cloud
       points = np.frombuffer(lidar_data.raw_data, dtype=np.float32)
       points = points.reshape(-1, 4)[:, :3]  # (N, 3) -- x, y, z

       # Convert to homogeneous coordinates
       points_h = np.hstack([points, np.ones((points.shape[0], 1))])

       # Get camera intrinsic matrix from CARLA attributes
       image_w = int(camera_actor.attributes['image_size_x'])
       image_h = int(camera_actor.attributes['image_size_y'])
       fov = float(camera_actor.attributes['fov'])
       focal = image_w / (2.0 * np.tan(np.radians(fov / 2.0)))

       K = np.array([
           [focal,  0.0,   image_w / 2.0],
           [0.0,    focal, image_h / 2.0],
           [0.0,    0.0,   1.0]
       ])

       # Build T_camera<-lidar by going through the WORLD frame.
       # NOTE: SensorData.transform is the sensor pose in WORLD
       # coordinates at capture time -- not relative to the vehicle.
       lidar_to_world = np.array(lidar_data.transform.get_matrix())
       world_to_cam = np.array(camera_data.transform.get_inverse_matrix())
       lidar_to_cam = world_to_cam @ lidar_to_world

       # Points in the camera frame, still in UE axes (x fwd, y right, z up)
       cam_points_ue = (lidar_to_cam @ points_h.T)[:3]   # (3, N)

       # --- The critical step: UE axes -> optical axes ---------------
       #   optical x (right) =  UE y
       #   optical y (down)  = -UE z
       #   optical z (fwd)   =  UE x
       cam_points = np.vstack([
            cam_points_ue[1],
           -cam_points_ue[2],
            cam_points_ue[0],
       ])
       # --------------------------------------------------------------

       # Keep only points in front of the camera (optical z > 0)
       mask = cam_points[2] > 0
       cam_points = cam_points[:, mask]

       # Apply intrinsics to get pixel coordinates
       pixel_coords = K @ cam_points
       pixel_coords /= pixel_coords[2]  # normalize by depth

       u = pixel_coords[0].astype(int)
       v = pixel_coords[1].astype(int)
       depths = cam_points[2]

       # Filter to image bounds
       valid = (u >= 0) & (u < image_w) & (v >= 0) & (v < image_h)

       return u[valid], v[valid], depths[valid]

.. admonition:: How to tell if you got the axes wrong
   :class: warning

   The symptom is rarely an exception -- it is a plausible-looking but
   wrong overlay. Two quick checks:

   - **Everything is filtered out.** If ``mask`` removes nearly all
     points, you are almost certainly testing UE ``z`` (up) instead of
     optical ``z`` (forward), so only points *above* the sensor survive.
   - **The overlay is rotated 90 degrees.** Points from the road appear
     along a vertical band instead of the lower half of the image --
     that is the ``x``/``y`` swap.

   Sanity-test with a single known point: a LiDAR return 10 m directly
   ahead should land near the **principal point**
   :math:`(c_x, c_y)` with depth ~10 m.

.. admonition:: Exercise Tasks
   :class: tip

   1. **Run the sensor spawning script** and observe camera, LiDAR, and
      RADAR data streaming in real time.
   2. **Modify sensor parameters**: Change the LiDAR channel count from 64
      to 32 to 16 and observe how point cloud density changes.
   3. **Project LiDAR onto camera**: Use the projection function above to
      overlay colored depth points on the camera image.
   4. **Add sensor noise**: Set the GNSS sensor's ``noise_alt_stddev``,
      ``noise_lat_stddev``, and ``noise_lon_stddev`` attributes to simulate
      realistic GPS noise. Compare noisy vs. clean positions.
   5. **Weather experiment**: Change weather to heavy rain
      (``world.set_weather(carla.WeatherParameters.HardRainNoon)``) and
      observe the impact on each sensor's data quality.

Summary
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Sensors
      :class-card: sd-border-primary

      - No single modality is sufficient; the **complementarity
        principle** (complementary / competitive / cooperative) is what
        justifies a sensor suite
      - Camera: unmatched semantics, the only sensor that reads signs and
        lights; poor depth, degrades in low light and glare
      - LiDAR: direct, accurate 3-D geometry; degraded by fog, rain, and
        low-reflectivity surfaces
      - RADAR: direct Doppler velocity and all-weather robustness; poor
        angular resolution, and stationary-object filtering is a real
        safety risk
      - IMU + GNSS: high-rate relative motion corrected by an absolute
        but low-rate global fix -- the classic fusion pairing

   .. grid-item-card:: Calibration
      :class-card: sd-border-primary

      - Intrinsics map 3-D rays to pixels; **extrinsics** are the 6-DOF
        rigid transform between frames, and are what make fusion possible
      - Use one notation and keep it: :math:`T_{A \leftarrow B}` maps
        points from B into A, and inner frames must cancel when chaining
      - Methods: target-based (accurate, controlled), targetless
        (convenient, less accurate), motion-based (hand-eye, needs
        excitation)
      - Calibration **drifts** with vibration and temperature, so
        production stacks monitor and re-estimate it online
      - A 1-degree rotation error is 1.7 m of lateral error at 100 m --
        poor calibration is a leading cause of fusion failure

.. admonition:: Assignment Unlocked -- GP1: Sensor Suite & Data Pipeline
   :class: important

   You now have the foundational knowledge from **L1--L2** to begin
   **GP1: Sensor Suite & Data Pipeline**. In GP1 you will build the
   ``ads_pipeline`` ROS 2 package, spawn an ego vehicle with a full sensor
   suite in CARLA, record and visualize sensor data, and implement
   LiDAR-to-camera projection.

   :doc:`Go to GP1 </assignments/gp1>`
