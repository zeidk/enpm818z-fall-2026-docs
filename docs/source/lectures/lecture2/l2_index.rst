====================================================
L2: Sensor Technologies & Calibration
====================================================

Overview
--------

This lecture provides a deep dive into the sensor technologies that enable
autonomous driving. You will learn about the operating principles, strengths,
and limitations of cameras, LiDAR, RADAR, IMU, and GNSS. The lecture covers
the complementarity principle -- why no single sensor is sufficient -- and
introduces sensor calibration (intrinsic and extrinsic) as a prerequisite for
multi-sensor fusion. System-level design considerations including sensor
placement, coverage, and failure mode analysis are also discussed.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Identify and compare the five core sensor technologies used in autonomous
  driving (Camera, LiDAR, RADAR, IMU, GNSS).
- Explain the complementarity principle and why multi-sensor systems are
  essential.
- Describe the operating principles of each sensor: image formation, time-of-
  flight, Doppler effect, inertial measurement, and satellite positioning.
- List the key technical specifications and performance limitations of each
  sensor.
- Explain intrinsic and extrinsic calibration and why they matter for fusion.
- Analyze system-level design trade-offs: sensor placement, coverage
  requirements, and failure mode analysis.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l2_lecture
   l2_exercises
   l2_quiz
   l2_references


Next Steps
----------

- In the next lecture, we will cover **Perception I: Object Detection
  (YOLO to DETR)**:

  - CNN fundamentals and the deep learning revolution in perception.
  - YOLO architecture: backbone, neck, head.
  - Transformer-based detection with DETR.
  - Head-to-head comparison on CARLA data.

- Complete the CARLA sensor data collection exercise from this lecture.
- Read the `CARLA Sensor Reference <https://carla.readthedocs.io/en/0.9.16/ref_sensors/>`_.
