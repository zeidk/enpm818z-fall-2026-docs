====================================================
L2: Sensor Technologies & Calibration
====================================================

Overview
--------

**The lecture opens in CARLA.** Before any of the physics, you meet the
simulator you will build on all semester: its client-server architecture, why
the course ships its own ROS 2 bridge, why you must run it in synchronous mode,
the limits of what it actually models, and a live demonstration that spawns an
ego vehicle with a camera and a LiDAR. That demonstration hard-codes the sensor
mounting offsets -- which is precisely the problem the rest of the evening is
about.

The lecture then provides a deep dive into the sensor technologies that enable
autonomous driving. You will learn about the operating principles, strengths,
and limitations of cameras, LiDAR, RADAR, ultrasonic sensors, IMU, and GNSS.
It covers the complementarity principle -- why no single sensor is
sufficient -- and then treats sensor calibration as the prerequisite for
multi-sensor fusion: intrinsic and extrinsic calibration, the transform
convention used for the rest of the course, LiDAR-to-camera projection, and
time synchronization. System-level design considerations including sensor
placement, coverage, and failure mode analysis are also discussed.

CARLA returns twice more. In **System Design**, sensor placement is expressed
concretely as CARLA attachment transforms -- how to derive mounting positions
from the vehicle's own bounding box, and why ``AttachmentType.Rigid`` is the
only correct choice for a sensor you intend to calibrate. The lecture then
closes back in CARLA, projecting LiDAR points into the camera image -- the task
that needs everything in between, and the core of GP1.

.. note::

   Installing CARLA is **not** covered in lecture. It is pre-read and
   setup-guide material (:doc:`Ubuntu 22.04 <../../carla/ubuntu22>`,
   :doc:`Ubuntu 24.04 <../../carla/ubuntu24>`), and having it running is the
   Week 3 setup milestone.

.. note::

   A map is treated here only as a **prior**, which is what you need in
   order to read the industry sensor-configuration comparison. HD map
   *layers* and map-based localization are covered in
   :doc:`L7 <../lecture7/l7_index>`; the map formats that encode them
   (OpenDRIVE, Lanelet2) and how routing consumes them are covered in
   :doc:`L8 <../lecture8/l8_index>`.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Identify and compare the six sensor modalities used in autonomous driving
  (Camera, LiDAR, RADAR, Ultrasonic, IMU, GNSS).
- Explain the complementarity principle and why multi-sensor systems are
  essential, and classify a sensor pair as complementary, competitive, or
  cooperative.
- Describe the operating principles of each sensor: image formation, time-of-
  flight, Doppler effect, inertial measurement, and satellite positioning.
- List the key technical specifications and performance limitations of each
  sensor, and name each one's dominant failure mode.
- Explain intrinsic and extrinsic calibration and why they matter for fusion.
- Chain transforms with the course convention :math:`T_{A \leftarrow B}` and
  check a composition by cancelling inner frames.
- Project a LiDAR point into a camera image, and predict the error that a
  small extrinsic rotation error produces at range.
- Explain why time synchronization is half of calibration, and convert a
  timing skew into a position error at speed.
- Analyze system-level design trade-offs: sensor placement, coverage
  requirements, and failure mode analysis.
- Describe CARLA's client-server model, explain why a sensor's attachment
  transform *is* an extrinsic, and spawn a sensor suite in synchronous mode.
- Express a sensor placement as a CARLA ``Transform``, derive mounting
  positions from ``vehicle.bounding_box.extent``, and explain why a
  spring-arm attachment breaks the fixed extrinsic that calibration assumes.


.. admonition:: Materials in revision
   :class: note

   The lecture notes, exercises, quiz and references for this lecture are
   being revised against the current slide deck and are not published yet.
   This page will link to them once they are ready.


Next Steps
----------

- In the next lecture, we will cover **L3: Probabilistic State Estimation
  & Fusion**:

  - Fusion architectures: early (raw), intermediate (feature), late (decision).
  - Uncertainty, and why inverse-variance weighting is the right average.
  - The Kalman filter from first principles, then the EKF and UKF.
  - Data association: which measurement belongs to which track.

- Everything you calibrate in this lecture is what L3 fuses. Placement today,
  fusion next week.
- Complete the CARLA sensor exercise from this lecture. Task 3 -- projecting
  LiDAR into the camera image -- is the one that matters, and it is the core
  of GP1.
- Read the `CARLA Sensor Reference <https://carla.readthedocs.io/en/0.9.16/ref_sensors/>`_.
