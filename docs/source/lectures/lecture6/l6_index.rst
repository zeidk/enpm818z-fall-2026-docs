====================================================
L6: Multi-Sensor Fusion
====================================================

Overview
--------

No single sensor provides complete, reliable information about the world at
all times and under all conditions. This lecture covers the theory and practice
of **multi-sensor fusion** for autonomous driving, starting from the fundamental
motivation and progressing through classical probabilistic filters (Kalman, EKF,
UKF, Particle) to modern deep learning fusion architectures. You will learn how
to combine camera, LiDAR, and RADAR data into a unified, accurate, and robust
representation of the vehicle's environment.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain why sensor fusion is essential for accuracy, reliability, and coverage
  in autonomous driving.
- Distinguish complementary, competitive (redundant), and cooperative sensor
  relationships.
- Compare early (raw data), intermediate (feature-level), and late (decision-level)
  fusion architectures.
- Derive and apply the Kalman Filter prediction and update equations.
- Explain Kalman Gain behavior and its intuitive interpretation.
- Describe the Extended Kalman Filter (EKF) and how Jacobian linearization
  handles nonlinear dynamics.
- Describe the Unscented Kalman Filter (UKF) and how sigma-point sampling
  avoids Jacobian computation.
- Explain the Particle Filter and when it is preferred over KF/EKF/UKF.
- Formulate the data association problem and describe common solutions.
- Apply weighted averaging and inverse variance weighting for sensor fusion.
- Describe cross-attention fusion as a modern deep learning approach.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l6_lecture
   l6_quiz
   l6_references

Next Steps
----------

- The next lecture covers **Localization & SLAM**: coordinate systems, GNSS/RTK,
  dead reckoning, probabilistic localization, scan matching, pose graph
  optimization, and loop closure detection.
- Review the original Kalman (1960) paper or a linear algebra refresher if
  matrix operations feel unfamiliar.
- Explore the ``filterpy`` Python library for practical KF/UKF implementation:
  `https://filterpy.readthedocs.io <https://filterpy.readthedocs.io>`_.
