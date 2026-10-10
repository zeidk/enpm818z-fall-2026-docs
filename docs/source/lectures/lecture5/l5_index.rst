====================================================================
L5: Perception II, 3D Detection, BEV, Fusion & Tracking
====================================================================

Overview
--------

**L4 ended with a detector. Its box is in pixels, in one image, at one
instant. This lecture turns it into what the rest of the AV can use.**

L4 made a table of what perception hands to the rest of the AV, and each row
still has something missing. Each section of this lecture fills one row:

- **3D detection.** Prediction and planning need each object's position,
  size and heading in meters, not pixels. LiDAR detectors work on a view
  from above (PointPillars, CenterPoint).
- **Segmentation.** The planner needs the road itself: a class for every
  pixel, and the road seen from above.
- **BEV and occupancy.** The **bird's-eye view** (BEV) puts every camera in
  one grid on the ground (IPM, Lift-Splat-Shoot). **Occupancy** marks the
  ground that is taken by anything at all, with or without a class.
- **Fusion.** The AV has a camera, a LiDAR and a radar, and every answer has
  to come out as one. Early, intermediate and late fusion, and other
  vehicles' detections shared over V2X.
- **Tracking.** A speed needs the same object from one frame to the next:
  one Kalman filter per object (from L3), data association with a gate, and
  a track lifecycle that keeps identity stable.

The lecture frames all of it with Endsley's **situation awareness**: today
covers Level 1 (perception) and Level 2 (comprehension, through tracking).
Level 3, projection, is prediction in L9.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Read a **3D box** and say why LiDAR detectors work on a view from above.
- Say what **semantic** segmentation gives the planner, and why the road is
  segmented from above.
- Explain why the **bird's-eye view** helps, and what **occupancy** adds to
  boxes.
- Place a design in **early**, **intermediate** or **late** fusion, and
  project a LiDAR point into a camera box by hand.
- Run one cycle of a **multi-object tracker**: predict, gate, associate, and
  manage the track lifecycle.

.. admonition:: Materials in revision
   :class: note

   The lecture notes, their appendix, the exercises, the quiz and the
   references are rewritten from the current slide deck and will be
   published here soon.

The **code** for this lecture is published: :doc:`l5_code`, with the four
hands-on packages (``l5_box_demo``, ``l5_seg_demo``, ``l5_bev_demo`` and
``l5_tracking_demo``).

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l5_code


Next Steps
----------

- **Next class, L7: Localization and SLAM.** Where the AV itself is. Today
  needed it twice without saying so: sharing detections over V2X needs the
  sender's position, and the tracker's fixed frame needs the AV's.
- **Level 3, projection**, where everyone will be in a few seconds, is L9,
  Prediction.
- **Before next class:** run the four hands-on packages on the
  :doc:`Code page <l5_code>`.
