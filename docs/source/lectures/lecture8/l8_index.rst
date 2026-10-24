=====================================
L8: Prediction and Behavior Modeling
=====================================

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
- **Physics models.** Constant velocity (CV), constant turn rate (CTRV) and
  constant turn rate and acceleration (CTRA). From :math:`t` = 0, all three
  miss A's turn: CV ends 12.35 m off.
- **Scoring.** ADE, FDE and the miss rate (FDE above 2 m), on car A and on a
  test set of 2417 predictions. CV's 95% region, and a check of whether it
  is honest.
- **Several futures.** Two modes for car A, left and straight on, scored
  with minADE and minFDE.
- **Using the map.** The map's lanes are the candidate paths, and Bayes'
  rule gives each one a probability from A's speed: 0.87 for the left
  turn, which ends 1.88 m from the truth.
- **Other drivers.** Car B follows car A (the Intelligent Driver Model,
  IDM), and car A waits for a gap in the AV's lane: the AV's own plan
  changes what A does.

Learned predictors (VectorNet, MultiPath, MTR, Social LSTM) are in
:doc:`Going Further <l8_appendix>`, to read after class.


Learning Objectives
-------------------

After this lecture, you can:

- Say what a planner needs from **prediction**, and how far ahead it must
  look.
- Predict a road user's motion by hand with **constant velocity (CV)**,
  **constant turn rate (CTRV)** and **constant turn rate and acceleration
  (CTRA)**, and say why their error grows with the horizon.
- Score a prediction with **ADE, FDE and the miss rate**, and several
  predictions with **minADE and minFDE**; check whether an uncertainty is
  honest.
- Use the **map's lanes as candidate paths** and give each one a
  probability with **Bayes' rule**.
- Model another driver's **intent**, its reaction to the car ahead (the
  **IDM**), and its **gap acceptance**.


Lecture Materials
-----------------

- :doc:`l8_lecture`: the notes, following the slides shown in class.
- :doc:`Going Further <l8_appendix>`: the deck's appendix (the track fit,
  CTRV and CTRA written out, the test set, CV's uncertainty and its 95%
  region, Waymo's miss rate and mAP, the three map scores, P(left) over
  time, Autoware's map-based prediction, learned predictors, and the IDM's
  terms).
- :doc:`l8_code`: the hands-on, four parts on the junction (``scene``,
  ``physics``, ``modes`` and ``interact``), and Foxglove.
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
  <l8_code>`, and read, in :doc:`Going Further <l8_appendix>`, the sections
  on CTRV, on the region's honesty check and on learned predictors.
- **Post-work:** record 30 s of your GP stack and open the recording in
  Foxglove (see :doc:`l8_code`).
