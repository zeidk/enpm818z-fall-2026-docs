====================================================================
L6: Localization and SLAM
====================================================================

Overview
--------

**L5 found where everything else is, relative to the AV. L6 finds where the
AV itself is**, and how far off it may be: 0.29 m on a local street (Reid
et al., 2019). That answer is the AV's **pose**: its position
:math:`(x, y)` in the map frame, and its heading :math:`\theta`.

The lecture follows one recorded drive through a CARLA town, with sensor
errors we chose, so every method runs on the same data:

- **GNSS and RTK.** GNSS gives the AV's position on Earth, a few meters off,
  until tall buildings block the sky and the fixes stop. RTK removes most of
  the error near a base station, but not a bounce at the AV.
- **Dead reckoning.** The AV's own wheels and gyro carry the pose through
  the gap, but their small errors add up, and a heading error matters most.
- **Fusion in the EKF.** An extended Kalman filter combines the two: a pose
  that is smooth between fixes and pulled back at each one, yet still
  drifting while GNSS is out. One number scores each run: the absolute pose
  error (APE).
- **Against a map.** A map stops the drift: the LiDAR scan is compared with
  the map, many guesses at once to find the AV (Monte Carlo localization,
  MCL), then one guess moved until the scan lies on the map (scan
  registration, with ICP).
- **SLAM.** How that map is built in the first place: a pose graph, and a
  loop closure that removes the drift.

**Losing GNSS removes one input, not the pose.**

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Say what each localization sensor measures, and how each one goes wrong.
- Predict how **dead reckoning** drifts, and why a heading error matters
  most.
- Read a fused filter's error and its own uncertainty over a **GNSS
  outage**, and measure a run with the **absolute pose error (APE)**.
- Localize against a map with **Monte Carlo localization (MCL)**, and match
  a scan to a map with **ICP** (iterative closest point), one iteration in
  outline.
- Explain how a **loop closure** corrects a drifted trajectory in **SLAM**
  (simultaneous localization and mapping).

Lecture Materials
-----------------

- :doc:`l6_lecture`: the notes, following the slides shown in class.
- :doc:`Going Further <l6_appendix>`: the deck's appendix (the error bound,
  RTK, ICP by SVD, which way to score a scan, NDT, the likelihood field,
  integrity, pose-graph least squares, APE and RPE).
- :doc:`l6_code`: the hands-on, five parts on one recorded drive (``gnss``,
  ``dr``, ``ekf``, ``mcl`` and ``icp``).
- :doc:`l6_exercises`, :doc:`l6_quiz` and :doc:`l6_references`.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l6_lecture
   l6_appendix
   l6_code
   l6_exercises
   l6_quiz
   l6_references


Next Steps
----------

- **Next class, L7: Route Planning.** With the AV's pose on
  the map, find a route to the goal.
- **Before then:** run the four hands-on parts on the
  :doc:`Code page <l6_code>`; read the sections on ICP and the pose graph in
  :doc:`Going Further <l6_appendix>`; and read the two SLAM reading pages,
  :doc:`SLAM with a LiDAR </preread/slam-lidar>` and
  :doc:`Visual SLAM </preread/slam-visual>`.
