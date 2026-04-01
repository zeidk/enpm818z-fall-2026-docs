====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 2: Sensor Technologies &
Calibration. Topics include camera systems, LiDAR, RADAR, IMU, GNSS, the
complementarity principle, intrinsic and extrinsic calibration, sensor
placement, and failure mode analysis.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-15)
=================================

.. admonition:: Question 1
   :class: hint

   According to the complementarity principle, why is multi-sensor fusion
   essential for autonomous driving?

   A. A single sensor is too expensive for production vehicles.

   B. No single sensor technology can meet all perception requirements;
      different sensors have complementary strengths and weaknesses.

   C. Regulations require at least three sensor types on every AV.

   D. Fusion is only needed for Level 5 vehicles.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- No single sensor technology can meet all perception requirements;
   different sensors have complementary strengths and weaknesses.

   Cameras provide rich semantics but lack depth. LiDAR provides precise 3D
   geometry but cannot read signs. RADAR works in all weather but has poor
   angular resolution. Combining them creates a system more capable than any
   individual sensor.


.. admonition:: Question 2
   :class: hint

   Which sensor is the **only** one that can reliably read traffic lights
   and signs?

   A. LiDAR

   B. RADAR

   C. Camera

   D. IMU

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Camera

   Cameras capture color and fine detail, making them the only sensor capable
   of interpreting traffic light states (red/yellow/green) and reading text
   on traffic signs.


.. admonition:: Question 3
   :class: hint

   What does LiDAR's Time-of-Flight (ToF) principle measure?

   A. The frequency shift of a reflected laser beam.

   B. The round-trip time of a laser pulse to calculate distance.

   C. The intensity of reflected infrared light.

   D. The phase difference between emitted and received waves.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The round-trip time of a laser pulse to calculate distance.

   LiDAR emits a laser pulse, measures the time for it to reflect back, and
   computes distance as ``(c x delta_t) / 2``, where ``c`` is the speed of
   light and ``delta_t`` is the round-trip time.


.. admonition:: Question 4
   :class: hint

   What is RADAR's **main weakness** compared to cameras and LiDAR?

   A. It cannot operate in rain or fog.

   B. It has poor angular resolution, making it hard to distinguish nearby
      objects.

   C. It cannot measure velocity.

   D. It requires active illumination.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It has poor angular resolution, making it hard to distinguish
   nearby objects.

   RADAR's angular resolution (1-10 degrees) is far coarser than cameras
   or LiDAR. Two objects at the same distance but different lateral
   positions may appear as a single "blob." This is why imaging radar
   (79 GHz) is being developed.


.. admonition:: Question 5
   :class: hint

   Why do many RADAR systems filter out stationary objects, and what safety
   risk does this create?

   A. Stationary objects overwhelm the processor; risk of detecting too many
      false positives.

   B. Stationary objects produce no Doppler shift and are indistinguishable
      from clutter; risk of not detecting stopped vehicles ahead.

   C. RADAR cannot physically detect stationary objects.

   D. Filtering improves angular resolution at the cost of range.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Stationary objects produce no Doppler shift and are
   indistinguishable from clutter; risk of not detecting stopped vehicles
   ahead.

   Moving objects create a clear Doppler frequency shift, making them easy
   to separate from background. Stationary objects have no shift and blend
   into environmental clutter (guardrails, signs), so many RADAR systems
   filter them out -- creating a known safety risk for stopped-vehicle
   detection.


.. admonition:: Question 6
   :class: hint

   What is the primary weakness of IMU-based navigation?

   A. It cannot measure angular velocity.

   B. Small measurement errors integrate over time, causing unbounded
      position drift.

   C. It only works at frequencies below 10 Hz.

   D. It requires satellite signals to function.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Small measurement errors integrate over time, causing unbounded
   position drift.

   IMU errors are integrated twice to get position (acceleration -> velocity
   -> position), so even tiny bias errors grow quadratically with time. This
   is why IMU is always paired with GNSS or other absolute references.


.. admonition:: Question 7
   :class: hint

   In the stereo depth formula ``depth = (B x f) / d``, what does ``d``
   represent?

   A. The distance between the two cameras.

   B. The focal length in pixels.

   C. The disparity -- pixel position difference between left and right
      image projections.

   D. The diameter of the detected object.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The disparity -- pixel position difference between left and
   right image projections.

   Disparity is the horizontal pixel difference between where the same
   point appears in the left and right camera images. Larger disparity
   means the object is closer; smaller disparity means it is farther away.


.. admonition:: Question 8
   :class: hint

   What does the **intrinsic calibration matrix** (K) encode?

   A. The position and orientation of the camera relative to the vehicle.

   B. The focal lengths, principal point, and lens distortion of the camera.

   C. The transformation between LiDAR and camera coordinate frames.

   D. The timestamp synchronization offset between sensors.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The focal lengths, principal point, and lens distortion of
   the camera.

   The intrinsic matrix K contains ``fx, fy`` (focal lengths in pixels)
   and ``cx, cy`` (principal point). Distortion coefficients
   (``k1, k2, k3, p1, p2``) are also determined during intrinsic
   calibration.


.. admonition:: Question 9
   :class: hint

   Why is extrinsic calibration critical for multi-sensor fusion?

   A. It determines which sensor is most accurate.

   B. It provides the 6-DOF transformation between sensors, allowing
      detections to be projected into a common coordinate frame.

   C. It calibrates the clock synchronization between sensors.

   D. It adjusts sensor firmware to match vehicle specifications.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It provides the 6-DOF transformation between sensors, allowing
   detections to be projected into a common coordinate frame.

   Without accurate extrinsic calibration, a LiDAR point cloud and a camera
   image cannot be aligned. A 1-degree rotation error at 100 m range
   produces a 1.7 m positional error.


.. admonition:: Question 10
   :class: hint

   Which LiDAR type is better suited for **mass production** in consumer
   vehicles?

   A. Mechanical spinning LiDAR.

   B. Solid-state LiDAR.

   C. Flash LiDAR.

   D. All types are equally suited.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Solid-state LiDAR.

   Solid-state LiDARs (MEMS mirrors or electronic beam steering) have no
   large moving parts, making them compact, robust, and affordable for
   mass production. Examples include Luminar (Volvo/Mercedes) and Innoviz
   (BMW). The trade-off is limited FOV compared to 360-degree mechanical
   spinning units.


.. admonition:: Question 11
   :class: hint

   A camera's dynamic range is rated at 120 dB. What does this mean?

   A. It can detect objects at 120 meters.

   B. It can handle highlights 1 million times brighter than shadows in
      the same scene.

   C. It captures 120 frames per second.

   D. It has a 120-degree field of view.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It can handle highlights 1 million times brighter than shadows
   in the same scene.

   Dynamic range measures the ratio between the brightest and darkest
   elements a sensor can capture simultaneously. Every 20 dB represents a
   10-fold increase, so 120 dB = 10^6 = one million to one ratio.


.. admonition:: Question 12
   :class: hint

   What is a **Minimal Risk Condition (MRC)** maneuver?

   A. Operating the vehicle at minimum speed on the highway.

   B. A pre-planned safe response when a critical sensor fails, such as
      pulling over to the side of the road.

   C. Running the perception system at reduced resolution.

   D. Switching from ADS mode to ADAS mode.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A pre-planned safe response when a critical sensor fails, such
   as pulling over to the side of the road.

   An MRC maneuver brings the vehicle to a safe state when the system
   detects it can no longer operate safely (e.g., critical sensor failure,
   exiting ODD). This is a key requirement for Level 3+ systems.


.. admonition:: Question 13
   :class: hint

   Which company uses a **vision-only** approach with no LiDAR or RADAR?

   A. Waymo

   B. Aurora

   C. Tesla

   D. Cruise

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Tesla

   Tesla removed both RADAR and ultrasonic sensors, relying entirely on
   8 cameras. Their philosophy is that vision (with sufficient AI) can
   handle all perception tasks. This contrasts with Waymo (29 cameras +
   5 LiDARs + 6 RADARs) and other multi-sensor approaches.


.. admonition:: Question 14
   :class: hint

   Why is IMU + GNSS fusion a textbook application of the Kalman Filter?

   A. Both sensors produce identical measurements.

   B. IMU provides high-frequency relative updates while GNSS provides
      low-frequency absolute corrections -- perfectly complementary for
      the predict-update cycle.

   C. The Kalman Filter was originally invented for IMU processing.

   D. GNSS signals are always Gaussian distributed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- IMU provides high-frequency relative updates while GNSS
   provides low-frequency absolute corrections -- perfectly complementary
   for the predict-update cycle.

   The IMU drives the prediction step (high-rate motion estimate that
   drifts over time), while GNSS drives the update step (low-rate
   absolute position that corrects the drift). This maps directly to
   the Kalman Filter's predict-update architecture.


.. admonition:: Question 15
   :class: hint

   What is the main advantage of **imaging radar** (79 GHz) over
   conventional automotive radar (77 GHz)?

   A. Longer detection range.

   B. Higher angular resolution from a larger antenna array.

   C. Lower manufacturing cost.

   D. Better velocity accuracy.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Higher angular resolution from a larger antenna array.

   Imaging radar uses a larger antenna array at 79 GHz to achieve
   significantly better angular resolution, allowing it to better
   distinguish between nearby objects. Example: Continental ARS540.


----


True or False (Questions 16-25)
================================

.. admonition:: Question 16
   :class: hint

   **True or False:** Cameras provide direct depth measurement without any
   additional processing or second camera.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   A single (monocular) camera captures 2D images with no direct depth
   information. Depth can be estimated via stereo vision (two cameras) or
   inferred using deep neural networks, but neither is a direct measurement
   like LiDAR's time-of-flight.


.. admonition:: Question 17
   :class: hint

   **True or False:** RADAR can directly measure the velocity of a moving
   target using the Doppler effect.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Moving objects cause a frequency shift in the reflected RADAR signal
   (Doppler effect), which directly encodes the object's radial velocity.
   This is one of RADAR's key advantages over cameras and LiDAR.


.. admonition:: Question 18
   :class: hint

   **True or False:** Solid-state LiDAR provides a full 360-degree field
   of view.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Solid-state LiDARs typically provide a limited forward-facing field of
   view (e.g., 120 degrees). Only mechanical spinning LiDARs achieve full
   360-degree coverage. Multiple solid-state units can be combined for
   wider coverage.


.. admonition:: Question 19
   :class: hint

   **True or False:** GNSS works reliably in tunnels, underground parking
   garages, and dense urban canyons.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   GNSS requires line-of-sight to satellites. Signals are blocked in
   tunnels and garages, and suffer multipath reflections in urban canyons
   (buildings reflect signals, causing position errors). This is why
   IMU and other localization methods supplement GNSS.


.. admonition:: Question 20
   :class: hint

   **True or False:** A reprojection error greater than 2 pixels during
   intrinsic calibration validation typically indicates poor calibration
   quality.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Reprojection error measures how accurately known 3D points (e.g.,
   checkerboard corners) are projected back onto the image using the
   calibrated parameters. Values above 2 pixels suggest calibration
   issues that will degrade downstream perception and fusion.


.. admonition:: Question 21
   :class: hint

   **True or False:** Waymo and Tesla use the same sensor philosophy for
   their autonomous driving systems.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Waymo uses a LiDAR-centric approach with 29 cameras, 5 LiDARs, and
   6 RADARs. Tesla uses a vision-only approach with 8 cameras and no
   LiDAR or RADAR. These represent fundamentally different philosophies
   in the AV industry.


.. admonition:: Question 22
   :class: hint

   **True or False:** The forward direction of an AV should have redundant
   sensing with at least two different sensor modalities.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The forward direction is the most safety-critical zone. Redundancy
   across modalities (e.g., Camera + LiDAR + RADAR) ensures that if one
   sensor is degraded (e.g., camera blinded by sun), others can still
   detect obstacles.


.. admonition:: Question 23
   :class: hint

   **True or False:** Monocular depth estimation using deep learning
   provides the same level of accuracy as LiDAR time-of-flight
   measurements.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Monocular depth estimation is an inference (not a measurement) and
   suffers from scale ambiguity and dependence on training data. LiDAR
   provides direct, precise measurements (+/- 2-5 cm). Neural depth
   estimation is useful but fundamentally less accurate.


.. admonition:: Question 24
   :class: hint

   **True or False:** Extrinsic calibration determines the transformation
   between a sensor and the vehicle's coordinate frame.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Extrinsic calibration determines the 6-DOF transformation (3D rotation
   + 3D translation) between sensors, or between a sensor and the vehicle
   body frame. This is essential for projecting data from different sensors
   into a common reference frame for fusion.


.. admonition:: Question 25
   :class: hint

   **True or False:** In degraded mode operation, an AV should immediately
   shut down all systems and stop in place.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Degraded mode operation means the AV continues with reduced capability
   (e.g., lower speed, disabled lane-keeping) using the remaining
   functional sensors. If the degradation is severe, the vehicle executes
   a Minimal Risk Condition (MRC) maneuver such as safely pulling over --
   not an abrupt stop, which could be dangerous.


----


Essay Questions (Questions 26-30)
==================================

.. admonition:: Question 26
   :class: hint

   **Compare and contrast cameras, LiDAR, and RADAR** across at least four
   dimensions (e.g., resolution, weather robustness, cost, depth
   measurement). Explain why all three are typically used together.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Cameras: High resolution, rich semantics, low cost, but no direct
     depth and poor in adverse weather.
   - LiDAR: Precise 3D geometry, lighting-independent, but expensive and
     degraded by rain/fog.
   - RADAR: All-weather, direct velocity, but poor angular resolution and
     limited classification.
   - Together they cover each other's weaknesses: cameras for semantics,
     LiDAR for geometry, RADAR for weather robustness and velocity.


.. admonition:: Question 27
   :class: hint

   **Explain the difference between intrinsic and extrinsic calibration.**
   Why is each necessary, and what happens if either is inaccurate?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Intrinsic calibration determines a camera's internal parameters
     (focal length, principal point, distortion). Without it, images are
     geometrically distorted.
   - Extrinsic calibration determines the spatial relationship (rotation
     + translation) between sensors. Without it, LiDAR points cannot be
     correctly projected onto camera images.
   - Poor intrinsic calibration distorts measurements within a single
     sensor. Poor extrinsic calibration misaligns data across sensors,
     causing fusion failures.


.. admonition:: Question 28
   :class: hint

   **Describe the IMU + GNSS fusion strategy.** Explain the role of each
   sensor and why they are complementary.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - IMU provides high-frequency (>100 Hz) relative motion updates but
     drifts over time due to integration of small errors.
   - GNSS provides low-frequency (1-20 Hz) absolute position that does
     not drift but is unavailable in tunnels/canyons.
   - They are fused using a Kalman Filter: IMU drives the prediction step
     (smooth, fast, drifting) and GNSS drives the update step (slow but
     drift-correcting).


.. admonition:: Question 29
   :class: hint

   **You have a $5,000 sensor budget.** Design a sensor configuration for
   an urban robotaxi operating in a dense city. Justify your choices and
   explain what you had to sacrifice.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Urban driving requires 360-degree awareness for pedestrians, cyclists,
     and cross-traffic at intersections.
   - Prioritize surround-view cameras (4-6 cameras, ~$1,500) and corner
     RADARs (4 units, ~$2,000) for complete coverage.
   - Add a basic forward ADAS module (~$500) for AEB.
   - LiDAR is likely sacrificed due to cost, which weakens 3D geometry
     precision -- acknowledge this trade-off.


.. admonition:: Question 30
   :class: hint

   **Explain the concept of failure mode analysis** in the context of AV
   sensor systems. What are single points of failure, degraded mode
   operation, and MRC maneuvers?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A single point of failure is any component whose failure causes the
     entire system to fail. AV design avoids this through redundancy.
   - Degraded mode operation means continuing with reduced capability
     when a sensor fails (e.g., RADAR-only ACC at lower speed).
   - An MRC (Minimal Risk Condition) maneuver is a pre-planned safe
     response when the system can no longer operate safely (e.g., safely
     pulling over and stopping).
   - Continuous self-diagnostics detect failures and trigger the
     appropriate response.
