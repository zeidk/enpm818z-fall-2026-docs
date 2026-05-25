====================================================
L3: Probabilistic State Estimation & Fusion
====================================================

Overview
--------

Robust autonomous driving rests on a probabilistic foundation: every
sensor measurement is noisy, every motion model is approximate, and the
job of the AV stack is to track belief about the world over time rather
than to commit to single point estimates. This lecture introduces that
foundation -- the Bayesian filtering family (Kalman, Extended Kalman,
Unscented Kalman, Particle) and the classical multi-sensor fusion
architectures built on top of it. You will derive each filter from
first principles, work through their AV-specific failure modes, and
implement a multi-sensor Kalman filter in CARLA. The deep-learning
fusion techniques that complement these tools (cross-attention,
BEVFusion) appear later, alongside perception in L6.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain why sensor fusion is essential for accuracy, reliability, and
  coverage in autonomous driving.
- Distinguish complementary, competitive (redundant), and cooperative
  sensor relationships.
- Compare early (raw data), intermediate (feature-level), and late
  (decision-level) fusion architectures.
- Derive and apply the Kalman Filter prediction and update equations,
  and explain the Kalman Gain intuition.
- Describe the Extended Kalman Filter (EKF) and how Jacobian
  linearization handles nonlinear dynamics.
- Describe the Unscented Kalman Filter (UKF) and how sigma-point
  sampling avoids Jacobian computation.
- Explain the Particle Filter and when it is preferred over KF/EKF/UKF.
- Formulate the data association problem and describe common solutions
  (NN, GNN, JPDA, MHT).
- Apply weighted averaging and inverse-variance weighting for fusing
  independent Gaussian estimates.
- Implement a multi-sensor Kalman Filter in CARLA and reason about
  degraded-weather performance.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l3_lecture
   l3_exercises
   l3_quiz
   l3_references


Next Steps
----------

- In the next lecture, we will cover **Perception I: Object Detection
  (YOLO to DETR)**:

  - CNN fundamentals and the YOLO architecture family (v1 -> v11).
  - DETR and the transformer-based detection paradigm.
  - Trade-offs between CNN-based and transformer-based detectors.
  - Deployment patterns: detector-as-ROS-2-node, model optimization.

- Review the original Kalman (1960) paper or a linear algebra refresher
  if matrix operations feel unfamiliar.
- Explore the ``filterpy`` Python library for practical KF/UKF
  implementation: `https://filterpy.readthedocs.io
  <https://filterpy.readthedocs.io>`_.
