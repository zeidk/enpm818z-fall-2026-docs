====================================================================
L6: Localization and SLAM
====================================================================

Overview
--------

**L5 finds where everything else is, relative to the AV. L6 finds where the
AV is in the world.**

That answer is the AV's **pose**: its position :math:`(x, y)` in the map
frame, and its heading :math:`\theta`. L5 needed it twice without saying so:
the tracker follows each object in a frame that stays fixed while the AV
drives, and a message shared over V2X is useless unless it says where the
sender is. Every method in this lecture runs on one recorded CARLA drive,
with sensor errors we chose, so the methods can be compared on the same data:

- **GNSS and RTK.** GNSS is the only sensor that says where the AV is on
  Earth with no map and no starting point. In a city it goes wrong in two
  ways: a blocked sky (an outage) and multipath. RTK cancels the errors a
  base station and the car share, but not the ones at the car alone.
- **Dead reckoning.** The pose from the car's own speed and turn rate. It
  bridges a short gap and drifts, and a heading error matters most.
- **Fusion in the EKF.** L3's extended Kalman filter combines GNSS with the
  wheels and the gyro. The lecture shows what the filter does, from results
  files; GP3 asks you to build it. One number scores each run: the absolute
  pose error (APE).
- **Against a map.** The LiDAR scan matched to a point map: Monte Carlo
  localization (MCL), L3's particle filter given a map, and ICP scan
  matching. NDT, the scan matcher Autoware uses, is named.
- **Integrity.** How the AV checks its pose without knowing the truth: the
  NIS gate, the alert limit, the protection level, and a second independent
  source.
- **SLAM.** How the map is made: a pose graph, and a loop closure that
  corrects a drifted trajectory.

The lecture compares every method against one published accuracy
requirement for a passenger car on a local street: an error bound of 0.29 m
(Reid et al., 2019).

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Say what each localization sensor measures, and how each one goes wrong.
- Predict how **dead reckoning** drifts, and why a heading error matters
  most.
- Read a fused filter's error and its own uncertainty over a **GNSS
  outage**, and measure a run with the **absolute pose error (APE)**.
- Localize against a map with **Monte Carlo localization (MCL)**, and match
  a scan to a map with **ICP**, one iteration by hand.
- Check whether a localizer is honest, and say why it needs a second
  source.
- Explain how a **loop closure** corrects a drifted trajectory in
  **SLAM**.

Lecture Materials
-----------------

- :doc:`l6_lecture`: the notes, following the slides shown in class.
- :doc:`Going Further <l6_appendix>`: the deck's appendix (RTK, ICP by SVD,
  NDT, the likelihood field, pose-graph least squares, APE and RPE).
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

- **Next class, L7: Navigation and Route Planning.** With the AV's pose on
  the map, find a route to the goal.
- **Before next class:** run the four hands-on parts on the
  :doc:`Code page <l6_code>`, and read the sections on ICP and the pose graph
  in :doc:`Going Further <l6_appendix>`.
