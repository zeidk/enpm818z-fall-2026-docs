===============================================
L8: Trajectory Prediction and Behavior Modeling
===============================================

Overview
--------

**L5 follows every road user, and L7 gives the AV a route. L8 says where the
other road users will be over the next few seconds,** so that the planner
(L9) can keep clear of them. A prediction gives, for each road user, its
future positions over a time horizon, how sure each one is, and, when it
could do different things, several futures with a probability each.

The lecture follows one T-junction of CARLA's Town01. The AV drives east at
8 m/s. Car A, on the other lane, brakes for a left turn across the AV's
lane, and car B follows car A. The lanes come from CARLA's map file; the
motion is simulated, so the truth is known. Every method today predicts car
A's next 5 s:

- **How far ahead.** At 8 m/s, the AV needs 3.17 s to react and stop, so
  we predict 5 s ahead (chosen).
- **Physics models.** Constant velocity (CV), constant turn rate and
  velocity (CTRV) and constant turn rate and acceleration (CTRA). From :math:`t` = 0, all three
  miss car A's turn: CV ends 12.35 m off.
- **Scoring.** ADE, FDE and the miss rate (FDE above 2 m), on car A and on a
  test set of 2476 predictions. CV's 95% region, and how often it really
  holds the truth.
- **Several futures.** Two modes for car A, left and straight on, scored
  with minADE and minFDE.
- **Using the map.** The map's lanes are the candidate paths, and Bayes'
  rule gives each one a probability from car A's speed: 0.87 for the left
  turn, which ends 1.88 m from the truth. Calibration checks how often such
  probabilities come true on the test set.
- **Learned predictors.** What they read and write, three well-known
  designs (VectorNet, MultiPath, MTR), what Waymo and Tesla say they use,
  how they are trained and scored, and pedestrians and cyclists.
- **Other drivers.** Car B follows car A (the Intelligent Driver Model,
  IDM), and car A waits for a gap in the AV's lane: the AV's own plan
  changes what car A does. Post-encroachment time (PET) says how close the two
  runs came.


Learning Objectives
-------------------

After this lecture, you can:

- Say what a **planner** needs from **prediction**, and how far ahead it
  must look (the **horizon**).
- Predict a road user's motion by hand with **constant velocity (CV)**,
  **constant turn rate and velocity (CTRV)** and **constant turn rate and acceleration
  (CTRA)**, and say why their error grows with the horizon.
- Score a prediction with **ADE**, **FDE** and the **miss rate**, and
  several predictions with **minADE** and **minFDE**; check whether an
  **uncertainty** is honest.
- Use the **map's lanes as candidate paths** and give each one a
  probability with **Bayes' rule**.
- Say what a **learned predictor** reads and writes, and how it is trained
  and scored.
- Model another driver's **intent**, its reaction to the car ahead (the
  **IDM**), and its **gap acceptance**.


Lecture Materials
-----------------

- :doc:`l8_lecture`: the notes, following the slides shown in class.
- :doc:`Going Further <l8_appendix>`: the deck's appendix (the track fit,
  the test set, CV's uncertainty and its 95%
  region, Waymo's miss rate and mAP, the three map scores, P(left) over
  time, Autoware's map-based prediction, and the IDM's parameters).
- :doc:`l8_code`: the hands-on, four parts on the junction (``scene``,
  ``physics``, ``modes`` and ``interact``).
- :doc:`Foxglove: A Second Viewer for ROS 2 </preread/foxglove>`: the reading
  that goes with L8, with a live demo of its predictions in Foxglove.
- :doc:`l8_exercises`, :doc:`l8_quiz` and :doc:`l8_references`.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l8_lecture
   l8_appendix
   l8_code
   l8_exercises
   l8_quiz
   l8_references


Next Steps
----------

- **Next class, L9: Motion Planning.** Paths for the AV that keep clear of
  every likely future of every road user.
- **Before then:** run the four hands-on parts on the :doc:`Code page
  <l8_code>`, and read :doc:`Going Further <l8_appendix>` (four parts,
  listed at the top of that page).
- **Post-work:** read :doc:`Foxglove </preread/foxglove>`, then record 30 s
  of your GP stack and open the recording in Foxglove.
