====================================================
L1: Course Introduction & AV Landscape
====================================================

Overview
--------

This lecture introduces ENPM818Z and provides a comprehensive overview of the
autonomous vehicle (AV) landscape. You will learn about the core technologies
that enable self-driving capabilities, the current state of the industry, and
the key challenges that remain. The lecture also covers the course structure,
grading policies, development environment setup (Ubuntu, ROS 2, VS Code, Git),
and an introduction to the CARLA simulator that will be used throughout the
semester.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Define key AV terminology: Dynamic Driving Task (DDT), Operational Design
  Domain (ODD), ADAS vs. ADS.
- Explain the SAE J3016 levels of driving automation (Levels 0--5).
- Describe the current industry landscape, including major players and their
  deployment status.
- Identify the core technical challenges in autonomous driving: perception,
  prediction, planning, control, and validation.
- Summarize the key safety standards (ISO 26262, ISO 21448/SOTIF) and the
  evolving regulatory landscape.
- Set up the development environment: Ubuntu, ROS 2, VS Code, and Git.
- Explain the CARLA simulator architecture and its role in this course.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l1_lecture
   l1_quiz
   l1_references


Next Steps
----------

- In the next lecture, we will cover **Sensor Technologies & Calibration**:

  - Camera, LiDAR, RADAR, IMU, and GNSS systems.
  - Intrinsic and extrinsic calibration.
  - Sensor placement, coverage, and complementarity.

- Complete your development environment setup if not finished in class.
- Install CARLA following the :doc:`setup guide </carla/carla>`.
- Read the `SAE J3016 Standard <https://www.sae.org/standards/content/j3016_202104/>`_.
