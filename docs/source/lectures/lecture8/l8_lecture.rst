====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L8, the slides shown in class and
   the reading slide that goes with them, in the same order and with the
   same sections. You can read them at home. The deck keeps more material in
   its appendix, on :doc:`the appendix page <l8_appendix>`, "Going Further":

   - how speed, heading, turn rate and braking are read from a track (the
     least-squares fit, written out);
   - CTRV and CTRA written out, and how our test set is built;
   - CV's uncertainty term by term, why the 95% region's radius is
     2.45 times :math:`\sigma`, and Waymo's miss rate and mAP;
   - the three map scores written out, P(left) as car A approaches the
     junction, and Autoware's map-based prediction;
   - the Intelligent Driver Model's parameters, and the gap at which car B
     follows steadily.

   The hands-on commands are on :doc:`the Code page <l8_code>`. The papers
   and pages cited below are listed in full on :doc:`the References page
   <l8_references>`.


.. _l8-lec-introduction:

Introduction
------------

.. note::

   **L5** follows every road user: a track with a position and a velocity.
   **L7** gives the AV a route. **L8** says where the other road users
   **will be** over the next few seconds, so that the planner (L9) can keep
   clear of them.

.. figure:: /_static/images/L8/pred_stack.png
   :alt: A block diagram. Two gray input boxes on the left: tracks (L5, GP3), each road user's position and velocity; and the map (L7), lanes and junctions. Each has an arrow into a green box labeled prediction (today). A green arrow leads from prediction to a box labeled planning (L9), and an arrow from planning to a box labeled control (L10). Below prediction, a green box lists its output: for each road user, over the next few seconds, 1. where it will be, 2. how sure that is, 3. which of several futures, how likely.
   :width: 95%
   :align: center

   Where prediction sits. Its two inputs are the tracks of L5 (and GP3) and
   the map of L7. Its output goes to planning (L9), and planning's output to
   control (L10). For each road user, over the next few seconds, prediction
   gives **1** where it will be, **2** how sure that is, and **3** which of
   several futures, and how likely each one is.


.. _l8-lec-one-step:

L5's Tracker Predicts One Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L5's tracker keeps, for each road user, a state
:math:`[\,p_x,\ p_y,\ v_x,\ v_y\,]`: its position east and north
(:math:`p_x`, :math:`p_y`, in m) and its velocity east and north
(:math:`v_x`, :math:`v_y`, in m/s). New detections come every
:math:`\Delta t` = 0.1 s. Before each set arrives, the tracker predicts the
state with constant velocity:

.. math::

   p_x \leftarrow p_x + v_x\,\Delta t, \qquad p_y \leftarrow p_y + v_y\,\Delta t

- The tracker needs **one** step: where to look for the object among the
  next detections. A new detection then corrects it.
- The planner needs **many** steps: where the object will be 1, 2, ..., 5 s
  from now. No detection corrects those until they happen.
- The predictor runs as often as the tracker: each new set of tracks, every
  0.1 s, gives a new 5 s prediction that replaces the last one. Apollo and
  Autoware also run their predictor on each new output of the tracker
  (Apollo Auto, ``prediction_component.cc``; Autoware Foundation,
  ``callbacks.cpp``).
- Constant velocity has no turn in it: a car that is turning is predicted to
  drive straight on.


.. _l8-lec-tempe:

The Tempe Crash, March 2018
~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the NTSB report on the Uber test vehicle (NTSB, 2019). ADS means its
automated driving system.

.. note::

   "The ADS detected the pedestrian 5.6 seconds before impact. Although the
   ADS continued to track the pedestrian until the crash, it never
   accurately classified her as a pedestrian or **predicted her path**"
   (bold ours).

   "If the perception process changed the classification of a detected
   object, it no longer considered the tracking history of that object when
   generating a new trajectory".

- A prediction is built from the track's history. The history was thrown
  away every time her class (the object type) changed, so the system had no
  path for her across the road.
- The system saw an emergency only when she was in the vehicle's path:
  1.2 s before impact (L5).


.. _l8-lec-needs:

What the Planner Needs from Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The planner here is the AV's **motion planner** (L9): it chooses the AV's
own path and speed for the next few seconds, and chooses again as it drives.

.. admonition:: Definition: Trajectory prediction
   :class: note

   For each road user near the AV, from its past track and the map: its
   future positions over a time horizon (here every 0.1 s for 5 s), how sure
   each one is, and, when it could do different things, several futures with
   a probability each.

1. **Where:** a position at each future time. The planner
   checks its own path against each of them, time by time.
2. **How sure:** an uncertainty that grows with the horizon. The planner
   keeps more room where the uncertainty is larger. A road user hidden for a
   moment (behind a truck, say) has gaps in its track, so its prediction is
   less sure.
3. **Which future:** a car at a junction may go straight on or turn. Each
   option is one predicted future with its own probability.


.. _l8-lec-how-far:

How Far Ahead to Predict
~~~~~~~~~~~~~~~~~~~~~~~~

The prediction must reach at least as far ahead as the AV needs to react and
stop. Our AV drives at 8 m/s (GP4's default ``target_speed``). We chose the
reaction time and the braking for this example.

.. figure:: /_static/images/L8/stopping_side.png
   :alt: A side view of the road, to scale, with a distance axis from 0 to 16 meters: distance driven since the AV sees the problem. A faded gray car stands with its front bumper at 0. A black car, the same AV, stands with its front bumper at about 14.7 meters. A darker gray band runs from 0 to 4 meters and a lighter gray band from 4 to 14.7 meters, with dashed vertical lines at 0, 4 and 14.7. Above the road, a double arrow from 0 to 4 marked tag 1 and a double arrow from 4 to 14.7 marked tag 2. Below the road, a double arrow from 0 to 14.7 marked tag 3.
   :width: 95%
   :align: center

   The AV from the side, drawn to scale. Faded: the AV when it sees a
   problem; black: where it stands still. **1:** reacting, 4.0 m. **2:**
   braking, 10.67 m. **3:** in all, 14.67 m.

1. Reacting (sensing, deciding) takes 0.5 s: 8 × 0.5 = 4.0 m. The AV
   drives 4.0 m before its brakes even start.
2. Braking at 3 m/s² takes 8 / 3 = 2.67 s. While braking, the speed falls
   evenly from 8 to 0 m/s, so the average speed is 8 / 2 = 4 m/s, and the
   AV drives 4 × 2.67 = 10.67 m more before it stops.
3. In all: 0.5 + 2.67 = 3.17 s and 4.0 + 10.67 = 14.67 m. From the moment
   the AV sees a problem, it needs 3.17 s and 14.67 m to stand still.

So the prediction must reach at least 3.17 s ahead. Today we predict 5 s
ahead (chosen), with room to slow down gently instead of braking hard.


.. _l8-lec-datasets:

Prediction Windows in Public Datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public datasets of recorded traffic, used to train and score predictors, fix
two windows: **observed**, how much past track the predictor reads, and
**predicted**, how far ahead it must predict.

.. figure:: /_static/images/L8/dataset_windows.png
   :alt: Four horizontal bars on a time axis from minus 6 to 8 seconds, with a dotted line at 0, now. For each row, a light gray bar to the left of 0 is the observed past and a dark bar to the right is the predicted future, each labeled with its length. Argoverse: 2 s and 3 s. Argoverse 2: 5 s and 6 s. Waymo Open Motion: 1 s and 8 s. This lecture: 2 s and 5 s.
   :width: 95%
   :align: center

   Each dataset's two windows on one time axis, with now at 0. Gray: the
   observed past; dark: the predicted future. Each bar is labeled with its
   length.

The table gives the same windows. They come from the papers of Argoverse,
Argoverse 2 and Waymo Open Motion; this lecture's windows are chosen.

.. list-table::
   :widths: 50 25 25
   :header-rows: 1
   :class: compact-table

   * - **Dataset**
     - **Observed**
     - **Predicted**
   * - Argoverse (Chang et al., 2019)
     - 2 s
     - 3 s
   * - Argoverse 2 (Wilson et al., 2021)
     - 5 s
     - 6 s
   * - Waymo Open Motion (Ettinger et al., 2021)
     - 1 s
     - 8 s
   * - **In this lecture** (chosen)
     - 2 s
     - 5 s


.. _l8-lec-three-kinds:

Three Kinds of Motion Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In their survey, Lefèvre, Vasquez and Laugier sort prediction models into
three levels (Lefèvre et al., 2014):

.. list-table::
   :widths: 20 50 30
   :header-rows: 1
   :class: compact-table

   * - **Level**
     - **In the survey's words**
     - **Section today**
   * - Physics-based
     - "the motion of vehicles only depends on the laws of physics"
     - Physics Models
   * - Maneuver-based
     - "the future motion of a vehicle also depends on the maneuver that
       the driver intends to perform"
     - Several Futures, Using the Map
   * - Interaction-aware
     - "take into account the inter-dependencies between vehicles'
       maneuvers"
     - Other Drivers

:ref:`Learned predictors <l8-lec-learned>`, later in this lecture, can work
at any of the three levels.


.. _l8-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

After this lecture, you can:

1. say what a **planner** needs from **prediction**, and how far ahead it
   must look (the **horizon**);
2. predict a road user's motion by hand with **constant velocity (CV)**,
   **constant turn rate and velocity (CTRV)** and **constant turn rate and
   acceleration (CTRA)**, and say why their error grows with the horizon;
3. score a prediction with **ADE**, **FDE** and the **miss rate**, and
   several predictions with **minADE** and **minFDE**; check whether an
   **uncertainty** is honest;
4. use the map's **lanes as candidate paths** and give each one a
   probability with **Bayes' rule**;
5. say what a **learned predictor** reads and writes, and how it is trained
   and scored;
6. model another driver's **intent**, its reaction to the car ahead (the
   **IDM**), and its **gap acceptance**.


.. _l8-lec-scene:

The Scene
---------

We take a junction of Town01, the town of L7, with the AV and two cars, and
simulate their motion.

**What it is for:** every predictor is compared on the same scene, against a
truth we know.

**Where the numbers come from.** The lanes are CARLA's: read from
``Town01.xodr`` with ``carla.Map``, with no CARLA server. The motion is
ours: simulated in Python on those lanes, so the truth is known exactly.
We chose every speed and every braking rate, and these notes say so.


.. _l8-lec-junction:

The Junction, from Town01's Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/scene_map.png
   :alt: A top view of a T-junction from Town01's map, x east from 98 to 214 meters, y north from minus 24 to 12 meters. A road runs east to west with one lane each way, a white dashed center line, and a side road leaving the junction to the south. Tag 1: the AV, a black car on the south lane at x 108, facing east. Tag A: car A, an orange car on the north lane at x 174, facing west. Tag B: car B, a gray car on the north lane at x 201, facing west. A red cross in the junction at x 156, y minus 2, with no tag.
   :width: 95%
   :align: center

   A T-junction of Town01, from above, :math:`x` east and :math:`y` north in
   meters, all at :math:`t` = 0. **1:** the AV, on the south lane, facing
   east. **A:** car A and **B:** car B, on the north lane, facing west. The
   red cross: where A's left turn would cross the AV's lane.

**1** is the AV, **A** car A and **B** car B, all at :math:`t` = 0, which
is now. :math:`t` is the time in seconds; a negative :math:`t` is the past.
The red cross is where A's left turn would cross the AV's lane.

Measured on the map: the lanes are 4.0 m wide. A's left turn is about a
quarter circle, 23.07 m long. A quarter circle turns π/2 = 1.571 rad, and
length = radius × angle, so the radius is 23.07 / 1.571 = 14.7 m.


.. _l8-lec-truth:

The Truth We Simulated
~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/scene_truth.png
   :alt: The same top view with each road user's next 5 seconds drawn as a line with a dot every second, and the three cars faded at their positions now. The AV's black line runs east along its lane from x 107 to about 147, labeled 5 s at its end. Car A's orange line runs west, then curves left through the junction into the side road, ending at x 154, y minus 7, labeled 5 s. Car B's gray line runs west along the north lane from x 201 to about 164, under car A's line where they overlap. Dark tags 1, A and B mark the AV, car A and car B; a red cross with no tag, in the junction at x 156, y minus 2, marks where car A's turn crosses the AV's lane.
   :width: 95%
   :align: center

   Where each road user really goes over the next 5 s, a dot every second.
   **1:** the AV, black, east along its lane. **A:** car A, orange, west and
   then left into the side road. **B:** car B, gray, west along the north
   lane, under A's line where they overlap. The red cross: where A's turn
   crosses the AV's lane.

Each line is where a road user really goes over the next 5 s, with a dot
every second. We chose this motion; the AV does not know it.

- **1** The AV drives east at 8 m/s, straight on. It reaches the red cross
  at :math:`t` = 6.08 s.
- **A** Car A drove at 8 m/s until :math:`t` = −2 s, then braked at
  1.0 m/s²: 6.0 m/s now, 5.0 m/s at :math:`t` = 1 s. It turns left at
  5.0 m/s and is in the AV's lane from :math:`t` = 3.4 to 4.3 s.
- **B** Car B follows A, with 22.3 m between A's rear and B's front, and
  goes straight on.


.. _l8-lec-known:

What the AV Knows at t = 0
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Known**
     - **Not known**
   * - Each car's **track**: its position every 0.1 s for the last 2 s,
       with a random error of 0.05 m (one standard deviation per axis,
       chosen as what a tracker might give).
     - Where A and B will go: no turn signal in our scene.
   * - The **map**: every lane, where it goes, how it bends.
     - Their speeds to come.
   * - Its own plan: 8 m/s, straight on.
     - How each driver decides when to brake, turn or go.

.. admonition:: You first
   :class: hint

   Will A turn or go straight on? Which cue did you use? See
   :ref:`l8-lec-intent`.

.. important::

   **The question for the rest of the lecture:** from what the AV knows,
   predict car A's next 5 s, and say how sure that is. A is the hard one: it
   may cross the AV's lane.


.. _l8-lec-handson-scene:

Hands-On, Part 1: the Scene
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The hands-on script is in the course's Python repo, folder ``lecture8``
(`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture8>`__).
Its ``scene`` part shows the junction over time. The commands are on
:doc:`the Code page <l8_code>`.

.. admonition:: What to look at
   :class: hint

   1. Drag the **now** slider from −2 to 3 s. The dots are the tracked
      positions the AV sees.
   2. At which time can you first tell, by eye, that car A is slowing down?
      That it turns?


.. _l8-lec-physics:

Physics Models
--------------

We start with car A's track alone and the laws of motion. We try three
models, each with one more term than the last: constant velocity, constant
turn rate and velocity, and constant turn rate and acceleration.

**What it is for:** these are the simplest predictors, and every other
method is compared with them.

A physics model takes the road user's motion **now** (speed, heading, turn
rate, braking) and assumes it does not change.


.. _l8-lec-fit:

Step 1: Read Car A's Motion from Its Track
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/track_fit.png
   :alt: Car A's speed in meters per second against time from minus 2 to 0 seconds. A black line, the true speed, falls straight from 8.0 to 6.0. A light blue shaded band covers the last 1.5 seconds, tag 1 near its bottom. A blue dashed line, the speed from the fit, runs inside the band just under the black line and ends at a blue dot at time 0, at 5.99 meters per second, tag 2 below it. The legend, top right, says the AV does not know the true speed.
   :width: 70%
   :align: center

   Car A's speed against time, 0 = now. Black: the true speed, which the AV
   does not know. Blue dashed: the speed from the fit. **1:** the shaded
   band, the last 1.5 s of track used for the fit. **2:** the blue dot, the
   fit's speed now, 5.99 m/s.

We fit the constant-acceleration curve closest to the last 1.5 s (chosen) of A's 2 s of track
(**1**): 16 positions, by least squares. At :math:`t` = 0 (**2**) the fit
gives:

- speed **5.99** m/s;
- heading 1.86° south of west;
- turn rate (how fast the heading changes) **0.049** rad/s;
- braking **0.96** m/s².

The truth: 6.01 m/s, 0 rad/s and 1.0 m/s².

.. tip::

   See "Reading speed, heading, turn rate and braking from a track" in
   :doc:`Going Further <l8_appendix>` for the fit, written out.


.. _l8-lec-cv:

Step 2: Constant Velocity, by Hand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Constant velocity (CV):** the road user keeps the velocity it has now.

.. math::

   x(h) = x_0 + v_x\,h, \qquad y(h) = y_0 + v_y\,h

:math:`h` is the horizon: how far ahead, in seconds. From the fit (rounded):
:math:`x_0` = 174.59 m, :math:`y_0` = 1.98 m; :math:`v_x` = −5.985 m/s,
:math:`v_y` = −0.194 m/s (west, a little south).

1. :math:`h` = 1 s: :math:`x` = 174.59 − 5.985 = 168.60 m;
   :math:`y` = 1.98 − 0.194 = 1.79 m.
2. :math:`h` = 3 s: :math:`x` = 174.59 − 3 × 5.985 = 156.64 m;
   :math:`y` = 1.98 − 3 × 0.194 = 1.40 m.
3. :math:`h` = 5 s: :math:`x` = 174.59 − 5 × 5.985 = 144.67 m;
   :math:`y` = 1.98 − 5 × 0.194 = 1.01 m.

.. note::

   CV says that car A drives on west, past the junction, at 5.99 m/s. In
   truth, at :math:`h` = 5 s car A is at (154.08, −6.98) m: in the side
   road, after a left turn.


.. _l8-lec-cv-truth:

CV Against the Truth
~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/cv_vs_truth.png
   :alt: A close-up top view of the junction, x from 136 to 184 meters. Car A, orange, at x 175 on the north lane, facing west. A black line, the truth, runs west and curves left into the side road with a dot every second, ending at y minus 7. A blue line, constant velocity, runs straight west along the north lane with a dot every second. Tags 1, 2 and 3 mark the blue dots at 1, 3 and 5 seconds; red dotted lines join each to the truth's dot at the same time: hidden under the dots at 1 second, short at 3 seconds, long at 5 seconds.
   :width: 70%
   :align: center

   A close-up of the junction. Black: the truth. Blue: CV. Both have a dot
   every second. **1**, **2** and **3:** CV's position after 1, 3 and 5 s.
   The red dotted lines join a CV dot to the truth's dot at the same time:
   that distance is CV's error.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Horizon**
     - **CV's error**
   * - 1 s
     - 0.52 m
   * - 2 s
     - 1.50 m
   * - 3 s
     - 2.58 m
   * - 4 s
     - 6.01 m
   * - 5 s
     - 12.35 m

For the first 2 s the error stays at 1.5 m or less. Then A turns, and each
second adds more: 1.08, then 3.43, then 6.34 m.


.. _l8-lec-ctrv:

Constant Turn Rate: CTRV and CTRA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: CTRV and CTRA
   :class: note

   **Constant turn rate and velocity (CTRV):** the road user keeps its speed
   and its turn rate, so it drives on a circle. **Constant turn rate and
   acceleration (CTRA):** the same, with its speed changing at a constant
   rate (Schubert et al., 2008).

- The circle's radius is speed / turn rate. For car A now:
  5.99 / 0.049 = 122 m, nearly straight.
- That 0.049 rad/s is not a turn: A drives straight now. It comes from the
  0.05 m errors in the track.
- That radius divides by the turn rate. Near 0 that is a division by
  almost 0, so code must switch to CV there.

.. tip::

   See "CTRV, written out" and "CTRA: CTRV with a changing speed" in
   :doc:`Going Further <l8_appendix>`.


.. _l8-lec-all-three:

CV, CTRV and CTRA from t = 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/ctra_now.png
   :alt: The same close-up of the junction with car A at x 175. The black truth curves left into the side road. Three predictions run west along the north lane: blue CV straight to x 145; purple dashed CTRV bending slightly south, ending at x 145, y minus 2.6; dark gold dash-dotted CTRA shorter, slowing, ending at x 157, y minus 0.3. None follows the truth into the side road.
   :width: 70%
   :align: center

   Car A's three physics predictions from :math:`t` = 0, a dot every second.
   Black: the truth. Blue: CV, straight west. Purple dashed: CTRV, bending
   a little south. Dark gold dash-dotted: CTRA, shorter because it slows.
   None follows the truth into the side road.

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - **Model**
     - **Error at 3 s**
     - **Error at 5 s**
   * - CV
     - 2.58 m
     - 12.35 m
   * - CTRV
     - 2.65 m
     - 10.00 m
   * - CTRA
     - 1.89 m
     - 7.26 m

CTRA uses A's braking, so it keeps A closer to the junction. At
:math:`t` = 0, A has not started the turn.


.. _l8-lec-midturn:

CTRV in the Middle of the Turn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/ctrv_midturn.png
   :alt: A close-up of the junction and the side road, with car A in the middle of its left turn at t equals 3 seconds, facing west-south-west. The black truth curves into the side road and runs straight south. A blue CV line runs straight off to the west-south-west. A purple dashed CTRV line curves with the truth for the first second, then swings wider; a faint purple dotted circle of radius about 15 meters continues it all the way round, through the side road and back.
   :width: 50%
   :align: center

   Car A at :math:`t` = 3 s, in the middle of its left turn. Black: the
   truth, into the side road and then straight south. Blue: CV, straight on
   to the west-south-west. Purple dashed: CTRV over the next 3 s; the
   purple dotted circle is where CTRV's circle would go on.

Predict again from :math:`t` = 3 s, in the middle of the turn. The fit gives
4.98 m/s and 0.331 rad/s: a circle of radius 4.98 / 0.331 = 15.0 m (the
lane's radius is 14.7 m).

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - **Horizon**
     - **CV**
     - **CTRV**
   * - 1 s
     - 1.96 m
     - 1.14 m
   * - 2 s
     - 6.24 m
     - 3.06 m
   * - 3 s
     - 11.82 m
     - 4.81 m

The lane straightens after the turn, but CTRV's circle keeps turning
(dotted).


.. _l8-lec-err-horizon:

Error Against Horizon, on 2476 Predictions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/err_horizon.png
   :alt: Two panels of mean error in meters against horizon from 0 to 5 seconds, a gray dotted line at 2 meters. Left, no turn in the next 5 s, 1381 predictions: blue CV rises slowly to 3.6 meters at 5 seconds; purple dashed CTRV to 10.1; dark gold dash-dotted CTRA to 15.2. Right, a turn in the next 5 s, 1095 predictions: all three rise steeply and close together, CV to 20.8, CTRV to 19.1, CTRA to 18.3 meters.
   :width: 95%
   :align: center

   Mean error against horizon on our test set. **Left:** no turn in the
   next 5 s, 1381 predictions. **Right:** a turn in the next 5 s, 1095
   predictions. Blue: CV. Purple dashed: CTRV. Dark gold dash-dotted: CTRA.
   Gray dotted line: 2 m, the error the next section counts as a miss.

**Our test set:** every way through the junction, at 6 to 10 m/s, with
random braking and turn speeds (chosen). From each drive we scored one
prediction every 0.5 s. CV's mean error at 1, 3 and 5 s is 0.49, 1.65 and
3.64 m with no turn, and 1.44, 8.74 and 20.84 m with a turn. The gray dotted line is at 2 m, the error the
next section counts as a miss.

.. tip::

   See "How the test set is built" in :doc:`Going Further <l8_appendix>`.


.. _l8-lec-why-grows:

Why the Error Grows, and Why More Terms Do Not Help
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Any error in the speed grows with time.** 0.1 m/s off is 0.5 m after
   5 s. A speed that changes (a driver slowing for no reason we can see)
   adds more.
2. **A physics model has no term for a maneuver that has not started.**
   Before the turn, A's turn rate is 0. Only a predictor that knows the
   junction can read A's braking as a turn. With a turn ahead, all three
   models are 18 to 21 m off at 5 s.
3. **Each extra term is carried 5 s ahead.** With no turn, CTRV's turn rate
   and CTRA's speed change (braking before a turn, speeding up after it)
   often come from a turn that is ending or a speed change that will stop:
   10.1 and 15.2 m against CV's 3.6 m.

.. note::

   With a turn ahead, every model is past 2 m before 2 s: the AV needs to
   know **what the road user can do**. The next sections add the maneuvers
   and the map.


.. _l8-lec-handson-physics:

Hands-On, Part 2: Physics Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``physics`` part of the hands-on script draws CV, CTRV and CTRA for car
A, from any "now". The commands are on :doc:`the Code page <l8_code>`.

.. admonition:: What to look at
   :class: hint

   1. At now = 0: read each model's error at 5 s in the right panel's title
      (FDE, defined in the next section). Which is smallest, and why?
   2. Move now from 0 to 3.0 s, 0.5 s at a time. When does CTRV beat CV at
      5 s? When does it lose?
   3. Where is CTRA worst: while A brakes, or while it speeds up after the
      turn?


.. _l8-lec-scoring:

Scoring
-------

The physics models gave an error at each second, which is hard to compare.
We now score a whole prediction with one number (ADE, FDE), call it a hit or
a miss, and check the uncertainty it reports.

**What it is for:** with scores we compare predictors and tell when a prediction's own uncertainty can be trusted.


.. _l8-lec-ade-fde:

ADE: the Average Displacement Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **displacement error** at one time is the distance between the
predicted and the true position.

.. admonition:: Definition: Average displacement error (ADE)
   :class: note

   The displacement error averaged over every predicted time (Chang et al.,
   2019; Wilson et al., 2021).

   .. math::

      \mathrm{ADE} = \frac{1}{N}\sum_{i=1}^{N} \lVert \hat{p}_i - p_i \rVert

   :math:`N`: the number of predicted times; :math:`\hat{p}_i`: the
   predicted position at the :math:`i`-th time; :math:`p_i`: the true
   position then; :math:`\lVert\cdot\rVert`: the distance between them.

Car A's CV prediction, with only the five whole seconds (:math:`N` = 5):

1. The errors at 1 to 5 s: 0.52, 1.50, 2.58, 6.01 and 12.35 m.
2. ADE: (0.52 + 1.50 + 2.58 + 6.01 + 12.35) / 5 = 22.96 / 5 = 4.59 m.

Over all 50 predicted times (every 0.1 s from 0.1 to 5.0 s, :math:`N` =
50), the ADE is 3.37 m. From now on, ADE uses all 50.


.. _l8-lec-fde:

FDE: the Final Displacement Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Final displacement error (FDE)
   :class: note

   The displacement error at the last predicted time (Chang et al., 2019;
   Wilson et al., 2021).

   .. math::

      \mathrm{FDE} = \lVert \hat{p}_N - p_N \rVert

   :math:`\hat{p}_N`: the predicted position at the last time,
   :math:`N`; :math:`p_N`: the true position then.

Car A's CV prediction:

1. The last predicted time is 5.0 s, the end of the horizon.
2. FDE: the error at 5.0 s, **12.35** m.

Car A's errors grow with time, so its FDE (12.35 m) is far above its ADE
(3.37 m).


.. _l8-lec-miss:

A Miss
~~~~~~

.. note::

   Argoverse 2's miss rate: "the proportion of test samples where none of
   the forecasted trajectories were within 2.0 meters of ground truth
   according to endpoint error" (Wilson et al., 2021).

For one prediction, a **miss** means its FDE is above 2.0 m.

- Car A's CV prediction has an FDE of 12.35 m: a miss. CTRV (10.00 m) and
  CTRA (7.26 m) miss too.
- We count misses, not only the mean: a planner must know whether each car
  is within half a lane of where it was predicted (2 m of our 4.0 m lane).
- Waymo's dataset uses thresholds that depend on the horizon and the speed,
  and separate ones along and across the lane (Ettinger et al., 2021).

.. tip::

   See "Waymo's miss rate and mAP" in :doc:`Going Further <l8_appendix>`.


.. _l8-lec-test-scores:

Scores on Our Test Set
~~~~~~~~~~~~~~~~~~~~~~

Mean ADE and FDE (m) over a 5 s horizon, and the miss rate (FDE above 2 m).
The number of predictions in each group is in brackets.

.. list-table::
   :widths: 13 14 14 15 14 14 16
   :header-rows: 2
   :class: compact-table

   * -
     - **No turn** (1381)
     -
     -
     - **A turn** (1095)
     -
     -
   * -
     - ADE
     - FDE
     - miss rate
     - ADE
     - FDE
     - miss rate
   * - CV
     - 1.52
     - 3.64
     - 35.9%
     - 7.95
     - 20.84
     - 99.3%
   * - CTRV
     - 3.75
     - 10.05
     - 60.7%
     - 6.87
     - 19.14
     - 99.5%
   * - CTRA
     - 5.55
     - 15.22
     - 78.5%
     - 6.71
     - 18.32
     - 98.3%

- With a turn ahead, the physics models miss almost every time.
- With no turn, CV is the best of the three, and still misses 35.9% of the
  time. The misses come from cars on a turning route, braking before the
  turn or speeding up after it: CV misses 76.3% of those 625 predictions,
  and 2.5% of the 756 on straight routes.


.. _l8-lec-cv-region:

CV's 95% Region
~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/cv_region.png
   :alt: The close-up of the junction with car A at x 175. The blue CV line runs west with a dot every second; around each dot a light blue circle, the 95 percent region, small at 1 second and larger every second, the one at 5 seconds about 16 meters across. The black truth curves left into the side road: its dots at 1, 2 and 3 seconds lie inside the circles of the same time; its dots at 4 and 5 seconds lie outside.
   :width: 70%
   :align: center

   CV's prediction for car A, blue, with its 95% region around each
   one-second dot: the light blue circles. Black: the truth. Its dots at 1,
   2 and 3 s are inside the circle of the same time; at 4 and 5 s they are
   outside.

The light blue circles show where CV says the truth is, 95% of the time.
:math:`\sigma` is the standard deviation of the position, per axis. The
circles grow almost only because CV lets the speed drift (0.5 m/s per
:math:`\sqrt{\text{s}}`, chosen); the fitted velocity's error adds under 3%
of the variance from 1 s on.

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - :math:`h`
     - :math:`\sigma`
     - **95% radius**
   * - 1 s
     - 0.293 m
     - 0.72 m
   * - 3 s
     - 1.50 m
     - 3.68 m
   * - 5 s
     - 3.23 m
     - 7.91 m

The 95% radius is 2.45 × :math:`\sigma` (2.45 = :math:`\sqrt{5.99}`,
rounded; the appendix says why). The truth is inside at 1, 2 and 3 s,
outside at 4 and 5 s.

.. tip::

   See "CV's uncertainty, term by term" and "Why the 95% region's radius is
   2.45σ" in :doc:`Going Further <l8_appendix>`.


.. _l8-lec-honest:

How Often the Region Holds the Truth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/coverage.png
   :alt: Percent of true positions inside CV's 95 percent region against horizon, 0 to 5 seconds. A dark dotted line at 95 percent is labeled 95 percent: what the region promises. A solid blue line, no turn, rises from about 58 to about 85 percent and stays between 81 and 86 percent from 1 second on. A dashed blue line, a turn, starts near 47 percent, peaks near 52 percent at 0.4 seconds and falls to about 7 percent at 5 seconds.
   :width: 70%
   :align: center

   The share of true positions inside CV's 95% region, against horizon, on
   our test set. Dark dotted line: 95%, what the region promises. Solid
   blue: no turn. Dashed blue: a turn.

A 95% region must hold the truth 95% of the time. On our test set, at 1, 3
and 5 s:

- no turn: 81.5, 85.6 and 82.6%. Two groups hide in that average:
  straight routes, 100% (too wide); turning routes before the turn, 59 to
  68% (too narrow);
- a turn: 46.5, 20.4 and 7.2%: far too narrow.

Chance alone moves each number by about 2 points (counted by drive). CV's
region has no term for a turn or a speed change.

.. note::

   L6 checked a localizer this way (normalized innovation squared, NIS).
   Check a predictor's region the same way, for each kind of motion.


.. _l8-lec-scoring-summary:

Physics Models, Scored
~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Summary: physics models, scored
   :class: tip

   - **Car A, from t = 0:** CV's FDE 12.35 m, CTRV's 10.00 m, CTRA's
     7.26 m: three misses. A had not started its turn.
   - **The test set:** with no turn, CV's mean error stays under 2 m for
     3 s (1.65 m) and is the best of the three. With a turn ahead, all
     three are past 2 m before 2 s, and miss at 5 s almost every time (98.3
     to 99.5%).
   - **Uncertainty:** CV's 95% region held the truth 82 to 86% of the time
     with no turn, 7.2% at 5 s with one.
   - **So:** for more than a second or two near a junction, the predictor
     must consider what the road user **could do**: several futures.


.. _l8-lec-futures:

Several Futures
---------------

One predicted future is wrong whenever the car turns and the model does
not. So a prediction now gives several futures for each road user, each with
a probability, and we learn to score them.

**What it is for:** the planner can then know that car A may turn, before A
turns.


.. _l8-lec-two-things:

Car A Can Do Two Things
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/two_futures.png
   :alt: The close-up of the junction with car A at x 175 facing west. Two green predicted lines leave it, each with a dot every second: a thick solid one curving left into the side road, labeled left turn, p = 0.87, and a dashed one running straight west, labeled straight on, p = 0.13.
   :width: 70%
   :align: center

   Car A's two predicted futures, a dot every second. Thick green: the left
   turn, probability 0.87. Dashed green: straight on, probability 0.13.

A's lane splits at the junction: **straight on** to the west, or **left**
into the side road. No road leaves the junction to A's right.

These are two predicted futures, each with a probability. How we got 0.87
and 0.13 is the next section (:ref:`l8-lec-map`); here, what to do with
them.


.. _l8-lec-average:

The Average of Two Futures Is Not a Future
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/mean_of_modes.png
   :alt: The close-up of the junction with car A at x 175. Tag 1: the end of the green left-turn line in the side road. Tag 2: the end of the green dashed straight line, far west on A's lane. Tag 3: a red dot at the end of a red dotted line between them; the line starts along A's lane and bends south-west across the junction toward its south-west corner.
   :width: 70%
   :align: center

   **1:** the left turn. **2:** straight on. **3:** their average, point by
   point: the red dotted line, ending at the red dot.

At 5 s, point **3** is 7.21 m from each future, inside the AV's own lane,
facing against its traffic. No driver in A's lane ends up there.

Its FDE against the truth is 5.92 m, a miss, while the left-turn future
alone is off by 1.88 m.

.. note::

   If half the drivers in A's place turn and half go straight on, a
   predictor trained to give one answer with the smallest mean squared error
   learns to give point **3**, the average. So predictors give **several**
   futures instead.


.. _l8-lec-multimodal:

Multimodal Prediction
~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Multimodal prediction
   :class: note

   A prediction made of :math:`K` future trajectories for one road user,
   each called a **mode**, each with a probability; the :math:`K`
   probabilities add up to 1.

Car A at :math:`t` = 0, with :math:`K` = 2 modes, each scored against the
truth:

.. list-table::
   :widths: 24 19 19 19 19
   :header-rows: 1
   :class: compact-table

   * - **Mode**
     - **Probability**
     - **ADE**
     - **FDE**
     -
   * - left turn
     - 0.87
     - 0.86 m
     - 1.88 m
     - a hit
   * - straight on
     - 0.13
     - 3.55 m
     - 13.06 m
     - a miss


.. _l8-lec-minade:

minADE and minFDE
~~~~~~~~~~~~~~~~~

.. note::

   "We use minADE and minFDE as the metrics; they evaluate the average and
   endpoint L2 distance respectively, between the best forecasted
   trajectory and the ground truth" (Wilson et al., 2021). L2 distance is
   the ordinary straight-line distance.

Car A, with :math:`K` = 2:

1. The best mode ends closest to the truth: the left turn (1.88 against
   13.06 m).
2. minFDE = that mode's FDE, 1.88 m; minADE = its ADE, 0.86 m.
3. 1.88 m is under 2 m, so **not** a miss. A miss now means that **no** mode
   ends within 2 m.

.. note::

   minADE and minFDE check only whether the truth was among the futures the
   predictor offered; they ignore the probabilities.


.. _l8-lec-score-probs:

Scoring the Probabilities
~~~~~~~~~~~~~~~~~~~~~~~~~

More modes lower minFDE. Imagine a predictor that gives car A six modes,
spread over every lane and speed. One of them will land near the truth,
whatever A does: its minFDE looks very good.

- **What it costs the planner:** the AV must keep clear of every mode it
  takes seriously. Six spread modes leave it little room.
- **What catches it:** a score that uses the probabilities. Waymo's dataset
  ranks the modes by their confidence and computes a mean average precision
  (mAP) (Ettinger et al., 2021).
- **Our simpler check:** the probability a predictor gives to the true
  future. For car A: 0.87. Whether such probabilities come true as often as
  they say, we check on the test set (:ref:`l8-lec-calibration`).


.. _l8-lec-planner-two:

What the Planner Does with Two Futures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AV's own plan is 8 m/s, straight on.

.. figure:: /_static/images/L8/lane_timeline.png
   :alt: A timeline from 0 to 8 seconds, time from now, with three rows. Row tag 1: a green bar from 3.2 to 4.0 seconds. Row tag 2: empty. Row tag 3: an orange bar from 3.4 to 4.3 seconds. A black vertical line at 6.08 seconds, tag 4.
   :width: 95%
   :align: center

   When car A is in the AV's lane, against the time from now. **1:** the
   left turn mode (probability 0.87), 3.2 to 4.0 s. **2:** the straight on
   mode (0.13): never, so its row is empty. **3:** the truth, what A did,
   3.4 to 4.3 s. **4:** the AV reaches the point where A's turn crosses its
   lane, at 6.08 s.

1. For each mode, find when it puts car A in the AV's lane, and weigh it by
   its probability: 0.87 for the one that crosses.
2. Plan so that the AV is not at the crossing while a likely mode is. The
   AV arrives at 6.08 s, after A has left the lane, so it keeps its speed. A
   plan that reached the crossing near :math:`t` = 4 s would have to slow
   down.

.. note::

   Which modes count, and how much room to keep for each, is the planner's
   job (L9). The prediction's job: every likely future, with its times and
   its probability.


.. _l8-lec-map:

Using the Map
-------------

A car drives where the map has lanes. So each lane car A can take gives one
future, and Bayes' rule, applied to A's track, gives each future its
probability.

**What it is for:** the predictor then knows that car A can turn, and how
likely the turn is.

Lefèvre calls this maneuver-based: the driver picks a maneuver (a
lane through the junction), and the motion follows it (Lefèvre et al.,
2014).


.. _l8-lec-candidates:

The Map's Lanes Are the Candidate Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- A car on a road follows a lane. Where the lane splits, each branch is a
  possible future path: one mode.
- Town01's map lists, for junction 54, every way through it: six, two from
  each arm. Car A's arm has two: **straight on** (23.12 m inside the
  junction) and **left** (23.07 m, radius 14.7 m).

.. _l8-lec-plan:

The Plan for Car A, in Four Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/lane_plan.png
   :alt: A flowchart. A gray box, car A's track and the map's lanes, has an arrow into Step 1, put A on each candidate lane; an arrow to Step 2, the speed each path expects here; an arrow down to Step 3, how well each path explains A's speed; an arrow left to Step 4, Bayes' rule; a green arrow left to a green box, one probability for each lane.
   :width: 90%
   :align: center

   From car A's track and the map's lanes to one probability for each lane.
   **Step 1:** put A on each candidate lane. **Step 2:** the speed each path
   expects here. **Step 3:** how well each path explains A's speed.
   **Step 4:** Bayes' rule.


.. _l8-lec-step1-lane:

Step 1: Put Car A on Each Candidate Lane
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each candidate lane, we find the lane point nearest A's fitted
position:

1. **Distance to the junction** along the lane: **6.51** m. It is the same
   for both lanes: they share A's road up to the junction.
2. **Offset** from the lane's center: 0.07 m.
3. **Heading** against the lane's: 1.86° apart.

.. note::

   Before the junction, the two lanes share one line: offset and heading
   cannot tell them apart (each path's heading and offset scores, 0.973 and
   0.995, are the same). Only A's **speed** can, so far. Once A starts
   turning, its heading leaves the straight lane's.


.. _l8-lec-step2-speed:

Step 2: The Speed Each Path Expects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Straight on:** the street's speed, 8 m/s (chosen: the speed our cars
cruise at). **Left:** slow enough for the turn.

1. The turn speed for a sideways acceleration of 2.0 m/s² (chosen) is
   :math:`v = \sqrt{2.0 \times 14.7} = \sqrt{29.4}` = 5.42 m/s.
2. A driver who brakes at 1.0 m/s² (chosen) and reaches 5.42 m/s at the
   junction, 6.51 m away, drives now at
   :math:`\sqrt{\text{turn speed}^2 + 2 \times \text{braking} \times
   \text{distance}} = \sqrt{5.42^2 + 2 \times 1.0 \times 6.51} =
   \sqrt{42.4}` = 6.51 m/s. The speed has the same digits as the distance,
   by chance.
3. So straight on expects **8.00** m/s here, and left expects **6.51** m/s.
   A drives at **5.99** m/s.

.. note::

   The expected speed is only for scoring. Each mode's predicted future
   starts from A's own 5.99 m/s: straight on keeps it; left brakes evenly to
   5.42 m/s by the junction (at 0.50 m/s²), holds it through the turn, then
   speeds up.


.. _l8-lec-step2-graph:

Step 2, as a Graph: A's Speed Against Each Path's
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a graph, not a picture of the road: it plots each path's expected
speed against the distance to the junction.

.. figure:: /_static/images/L8/speed_expect.png
   :alt: A graph of speed in meters per second, 3.5 to 8.5, against distance to the junction in meters, 0 to 25. A dashed green line at 8 meters per second runs across. A solid green curve rises from 5.42 at 0 meters to 8 at about 17.3 meters, then runs flat at 8. An orange dot at 6.51 meters and 5.99 meters per second, just below the curve. A short solid segment from the dot up to the curve, tag 1; a dotted segment from the dot level up to the dashed line, tag 2. A gray dotted vertical line at 17.3 meters, tag 3.
   :width: 95%
   :align: center

   The speed each path expects against the distance to the junction. Solid
   green: left; dashed green: straight on. Orange dot: car A, 5.99 m/s at
   6.51 m. **1:** how much slower A is than left expects. **2:** how much
   slower A is than straight on expects. **3:** 17.3 m from the junction,
   where left's curve reaches 8 m/s.

**1** Left: A drives 6.51 − 5.99 = 0.52 m/s slower than this path expects.
**2** Straight on: A drives 8.00 − 5.99 = 2.01 m/s slower than this path
expects. **3** Step 2's formula, solved for the distance, puts left's 8 m/s
at (8² − 5.42²) / (2 × 1.0) = 17.3 m from the junction. Farther than that,
both paths expect 8 m/s, so speed cannot tell them apart.


.. _l8-lec-step3-likelihood:

Step 3: A Bell Curve Scores Each Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`\Delta v` is A's speed minus the speed a path expects here. The
closer :math:`\Delta v` is to 0, the better the path explains A's speed, and
the higher its **likelihood**.

.. figure:: /_static/images/L8/bell_curve.png
   :alt: A bell curve of likelihood, 0 to 1, against delta v, A's speed minus the path's expected speed, from minus 3.5 to 3.5 meters per second. The curve peaks at 1 at delta v equals 0, marked by a dotted vertical line. Two green dots on the curve, each with a green dashed line down to the axis: tag 1 at about minus 0.5, likelihood about 0.87; tag 2 at about minus 2.0, likelihood about 0.13.
   :width: 80%
   :align: center

   The likelihood against :math:`\Delta v`. **1:** left. **2:** straight
   on.

**1** Left: :math:`\Delta v` = 5.988 − 6.512 = −0.524 m/s, likelihood
0.872. **2** Straight on: :math:`\Delta v` = 5.988 − 8.000 = −2.012 m/s,
likelihood 0.132.


.. _l8-lec-step3-words:

Step 3: The Bell Curve's Formula, in Words
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The curve is :math:`e^{-\frac12 (\Delta v / \sigma)^2}`, with
:math:`\sigma` = 1.0 m/s (chosen: drivers differ by about that much). Read
it from the inside out:

1. :math:`\Delta v / \sigma`: how far A's speed is from the path's, counted
   in :math:`\sigma`'s.
2. Square it, then halve it: a speed too low and a speed too high count the
   same, and the score drops faster as the gap grows.
3. Take :math:`e` to the minus that: 1 when the speeds match; at one
   :math:`\sigma` off, :math:`e^{-0.5}` = 0.61; at two :math:`\sigma` off,
   :math:`e^{-2}` = 0.14.

.. note::

   Car A: left, :math:`e^{-\frac12 (0.524)^2} = e^{-0.137}` = 0.872;
   straight on, :math:`e^{-\frac12 (2.012)^2} = e^{-2.024}` = 0.132. A
   likelihood is at most 1; Step 4 turns the likelihoods into
   probabilities.


.. _l8-lec-step4-bayes:

Step 4: Bayes' Rule Turns the Scores into Probabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before looking at the track, each path is equally likely: its **prior** is
0.5 (chosen). Bayes' rule: multiply each prior by the path's likelihood,
then divide by the sum, so the probabilities add up to 1.

1. Left: 0.5 × 0.872 = 0.436. Straight on: 0.5 × 0.132 = 0.066.
2. Sum: 0.436 + 0.066 = 0.502.
3. P(left) = 0.436 / 0.502 = **0.87**; P(straight on) = 0.066 / 0.502 =
   **0.13**.

.. note::

   The two 0.5 priors cancel: with equal priors, the probabilities are the
   likelihoods divided by their sum, 0.872 / (0.872 + 0.132) = 0.87. That
   sum, 1.004, is close to 1 by chance, so the probabilities show the same
   digits as the likelihoods. A prior from data (how often drivers turn
   left here) would change them.

In papers this is written P(maneuver | track, map): here the maneuver is
the lane path, the track gives A's speed, and the map gives each path's
expected speed.

.. tip::

   See "All three scores, written out" and "P(left) as car A approaches" in
   :doc:`Going Further <l8_appendix>`.


.. _l8-lec-map-truth:

The Map-Aware Prediction Against the Truth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/modes_vs_truth.png
   :alt: The close-up of the junction with car A at x 175. The thick green left-turn mode, p = 0.87, curves into the side road; the green dashed straight-on mode, p = 0.13, runs west. The black truth follows the green left-turn line into the side road, its dots a little short of the green dots.
   :width: 70%
   :align: center

   Car A's two modes against the truth, a dot every second. Thick green:
   the left turn, probability 0.87. Dashed green: straight on, 0.13. Black:
   the truth. Its dots fall a little short of the left mode's dots.

The left mode's error at 1 to 5 s: 0.20, 0.62, 1.04, 1.46 and 1.88 m.

The mode picks the right lane but drives it a little too fast: it turns at
5.42 m/s, and A turns at 5.0 m/s (our choice for the truth). 5.42 − 5.0 =
0.42 m/s too fast, so the mode gains about 0.42 m on A every second.

CV, for comparison: FDE 12.35 m.


.. _l8-lec-map-test:

Map-Aware Prediction on the Test Set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/test_scores.png
   :alt: A bar chart of mean FDE at 5 seconds, in meters, on the test set's predictions with a turn ahead. Blue CV 20.8, purple CTRV 19.1, dark gold CTRA 18.3, green map most likely mode 5.0, and a hatched green bar, map best of the modes, 1.8. A gray dotted line at 2 meters.
   :width: 70%
   :align: center

   Mean FDE at 5 s on the test set's predictions with a turn ahead. Blue:
   CV. Purple: CTRV. Dark gold: CTRA. Green: the map's most likely mode.
   Hatched green: the best of the map's modes (minFDE). Gray dotted line:
   2 m, the miss threshold.

With a turn ahead (1095 predictions):

- The true path is the most likely mode 84% of the time.
- Still, the most likely mode misses 50.5% of the time (mean FDE 4.98 m):
  the right lane, at the wrong speed.

With no turn, the most likely mode is no better than CV: FDE 3.91 against
3.64 m, and it misses more (49.5 against 35.9%). In 1 of 10 of these
predictions, its most likely mode is the wrong lane.


.. _l8-lec-calibration:

Calibration: How Often the Probabilities Come True
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Calibration
   :class: note

   A predictor is calibrated when, of all the futures it gives a
   probability :math:`p`, a fraction :math:`p` comes true (Guo et al.,
   2017). Of 100 modes given 0.8, about 80 should be the true path.

Our test set: every mode of every prediction (4896 modes), in four groups by
its probability. Each dot is a group; its bar shows how far chance alone
moves it.

.. figure:: /_static/images/L8/reliability.png
   :alt: A square plot of share that came true, 0 to 1, against probability given, 0 to 1 (each dot is placed at its group's mean). A gray dashed diagonal, tag 1. Four green dots with error bars: near 0.06 and 0.09, at 0.5 and 0.5, at 0.81 and 0.73 with a long bar, tag 2, below the diagonal, and near 0.99 and 0.98.
   :width: 55%
   :align: center

   The share of each group's modes that came true against the probability
   given (the group's mean). Each dot: a group; its bar: how far chance
   alone moves it. **1:** the diagonal, where a perfectly calibrated
   predictor's dots sit. **2:** the group of car A's 0.87 (0.7 to 0.9):
   given 0.810 on average, came true 0.729.

The table gives the same four groups:

.. list-table::
   :widths: 28 24 24 24
   :header-rows: 1
   :class: compact-table

   * - **Probability given**
     - **Mean given**
     - **Came true**
     - **Modes**
   * - 0 to 0.3
     - 0.061
     - 0.091
     - 904
   * - 0.3 to 0.7
     - 0.500
     - 0.500
     - 3032
   * - 0.7 to 0.9
     - 0.810
     - 0.729
     - 240
   * - 0.9 to 1
     - 0.986
     - 0.976
     - 720

Modes from one drive are not independent, so chance is counted by redrawing
whole drives at random: it moves the 0.729 by about 0.06. The gap,
0.810 − 0.729 = 0.081, is only 1.3 times that: this test set cannot show
whether the predictor is too sure in the group of car A's 0.87.


.. _l8-lec-map-wrong:

Where Map-Aware Prediction Goes Wrong
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **The speed along the path.** The right lane at the wrong speed still
   misses: our test set's drivers turn at 1.5 to 2.5 m/s² sideways, and the
   predictor assumes 2.0.
2. **A driver who does not look like the rule.** A car cruising at 6 m/s on
   an 8 m/s street looks like a car about to turn.
3. **Off the map.** A car that leaves its lane (a U-turn, parking, avoiding
   something) has no lane to follow. Pedestrians and cyclists often have no
   lane to follow.
4. **A wrong map.** If roadworks close a lane, L7's map is out of date.

.. note::

   Keep a physics mode next to the lane modes. When no lane fits (a large
   offset or heading gap on every lane), the physics mode gets most of the
   probability.

.. tip::

   See "In industry: Autoware's map-based prediction" in :doc:`Going
   Further <l8_appendix>`.


.. _l8-lec-handson-modes:

Hands-On, Part 3: Two Futures and Their Probabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``modes`` part of the hands-on script draws car A's two futures, with
line widths that show their probabilities, and P(left) against time on the
right. The commands are on :doc:`the Code page <l8_code>`.

.. admonition:: What to look at
   :class: hint

   1. Move now from −0.5 to 1.0 s. Watch the line widths (the
      probabilities) and P(left) on the right.
   2. In ``l8sim.py``, set ``SIG_V = 0.5``, then ``2.0``. ``SIG_V`` is the
      :math:`\sigma` of Step 3, 1.0 m/s in the lecture. What happens to
      P(left) at :math:`t` = 0, and why?
   3. Set ``A_LAT = 1.5``. ``A_LAT`` is the sideways acceleration of Step 2,
      2.0 m/s² in the lecture. Does the left mode's FDE go down? Why?


.. _l8-lec-learned:

Learned Predictors
------------------

So far we chose the turn speeds, the :math:`\sigma`'s and the priors by
hand. A learned predictor has no such values to choose: training on
recorded driving sets its network's weights instead.

**What it is for:** you will know the names of the predictors that
production systems and the benchmarks use, and what they read and output.


.. _l8-lec-learned-io:

What a Learned Predictor Reads and Writes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/learned_io.png
   :alt: A block diagram. Three gray input boxes on the left: 1. every road user's last few seconds of track; 2. the map's lanes, as polylines (lists of points); 3. traffic lights, the road user's type (car, cyclist). Each has an arrow into a central box: a neural network, weights set by training. Two green arrows lead out to two green boxes: K future tracks for each road user, and one probability for each of them.
   :width: 90%
   :align: center

   A learned predictor. Its inputs: **1** every road user's last few
   seconds of track; **2** the map's lanes, as polylines (lists of points);
   **3** traffic lights and the road user's type (car, cyclist). A neural
   network, with weights set by training, writes :math:`K` future tracks for
   each road user and one probability for each of them.

- The output is the same as our map-aware predictor's: :math:`K` modes and
  their probabilities.
- What changes: a learned predictor has no turn speeds or
  :math:`\sigma`'s to choose. Its network's weights are **set by
  training** on recorded tracks, and they do the job our hand-chosen values
  did.


.. _l8-lec-learned-designs:

Three Well-Known Designs
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 45 35
   :header-rows: 1
   :class: compact-table

   * - **Model**
     - **Main idea, in the paper's words**
     - **In our terms**
   * - VectorNet (Gao et al., 2020)
     - "Observed agent trajectories and map features are represented as
       sequence of vectors"
     - lanes and tracks as lists of points, like our scene file
   * - MultiPath (Chai et al., 2019)
     - "predicts a discrete distribution over the anchors and, for each
       anchor, regresses offsets from anchor waypoints along with
       uncertainties"
     - anchors: typical trajectories, clustered from training tracks. Each
       plays a candidate lane's part: a probability, a shift, a
       :math:`\sigma`
   * - MTR (Shi et al., 2022)
     - "a small set of learnable motion query pairs. Each motion query pair
       takes charge of trajectory prediction and refinement for a specific
       motion mode"
     - one learned query per likely end region (clustered from training
       tracks)

MTR's authors report it "ranking 1st on the leaderboards of Waymo Open
Motion Dataset" (Shi et al., 2022).


.. _l8-lec-learned-industry:

What Waymo and Tesla Say They Use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Neither source below names the model that runs in the cars. What each says
in public:

- **Waymo** (2025): its large model has a "World Decoder" that reads the
  output of two encoders, one of them for the fused sensor data, "to
  predict other road users behaviors". The car runs
  smaller models trained from it, "optimized for real-time onboard
  deployment" (Waymo, 2025).
- **Tesla** (2022): "Relying purely on collision checks with marginal
  predictions will only get you so far because you will miss out on a lot
  of valid interactions" (Tesla, AI Day 2022). A marginal prediction
  predicts each road user alone.
- **Tesla** (2024): FSD runs on "end-to-end neural networks" (Tesla, Q1 2024
  Update). The update does not say whether a separate prediction step
  remains.

.. note::

   Both use neural networks, so their predictors are **learned**. Tesla's
   2022 quote says that predicting each road user alone is not enough: the
   point of Lefèvre's third level, **interaction-aware**
   (:ref:`l8-lec-drivers`).


.. _l8-lec-learned-train:

How Learned Predictors Are Trained and Scored
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Data:** recorded scenes, each cut into an observed part and a future
   part, with the windows of :ref:`l8-lec-datasets`.
2. **Training**, in one common form: the network predicts :math:`K` modes;
   the one nearest the true future is moved toward it, and its probability
   is raised.
3. **Scores:** the same as ours (minADE, minFDE, the miss rate; Waymo adds
   mAP), on the benchmark's test scenes.

.. note::

   **Why CV still matters:** it is a common baseline for learned models,
   and a simple prediction to fall back on. On our test set with no turn,
   CV's mean error stays under 2 m for 3 s.


.. _l8-lec-learned-peds:

Pedestrians and Cyclists
~~~~~~~~~~~~~~~~~~~~~~~~

- They do not keep to lanes: a pedestrian can turn on the spot or step off
  the curb. Sidewalks and crosswalks show where they usually walk.
- They move in groups and avoid each other. Social LSTM learns that from
  crowds: each person's prediction depends on the people near them (Alahi et
  al., 2016).
- Their uncertainty spreads in every direction: at 1.4 m/s (chosen, a
  walking pace), after 3 s a pedestrian can be anywhere in a circle of
  radius 1.4 × 3 = 4.2 m, curb and road included. A car stays along its
  lane.

.. note::

   Tempe again: a track that restarts at every new class has no history,
   and a predictor with no history has nothing to predict from (NTSB, 2019).


.. _l8-lec-drivers:

Other Drivers
-------------

Until now we predicted each road user alone. But drivers react to each
other: car B to car A, and car A to the AV.

**What it is for:** B's prediction then uses A's, A's uses the AV's plan,
and the AV knows that its own motion changes what others do.

Models that do this are the third of Lefèvre's levels, interaction-aware
(Lefèvre et al., 2014).


.. _l8-lec-intent:

Intent: What the Driver Means to Do
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Intent
   :class: note

   The maneuver a driver means to make next (turn left, go straight on,
   change lanes, stop). A predictor cannot measure it; it infers it from cues.

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Cue**
     - **What it says, and how far to trust it**
   * - Slowing down
     - A turn or a stop may be ahead. :ref:`Step 4 (Bayes' rule)
       <l8-lec-step4-bayes>` got P(left) = 0.87 from A's speed alone.
   * - Position in the lane
     - A car drifting toward a lane boundary may change lanes (Autoware
       Foundation, map-based prediction).
   * - Turn signal
     - A camera can read it, but drivers forget it, or leave it on.
   * - Where the lane goes
     - Only some maneuvers are possible: no road leaves the junction to
       A's right.


.. _l8-lec-b-slows:

Car B Slows Because Car A Slows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/b_speed.png
   :alt: Car B's speed in meters per second against time from minus 2 to 5 seconds, a gray dotted vertical line at 0 labeled now. The black truth falls from 8.0 to about 6.5 at 3.2 seconds, then rises to about 7.3 at 5 seconds. A blue line, CV, stays flat at 7.76 from 0 to 5 seconds. A green dashed line, the IDM behind A's likely future, follows the truth down to about 6.75 at 3 seconds and back up to about 7.6.
   :width: 70%
   :align: center

   Car B's speed against time; the dotted line is now. Black: the truth.
   Blue: CV, which holds B's speed. Green dashed: the IDM, a driver model,
   following A's most likely future.

At :math:`t` = 0 there are 22.3 m between A's rear and B's front. A brakes
for its turn, so B must slow too, until A leaves its lane.

- CV keeps B at 7.76 m/s: FDE 3.55 m.
- A driver model (the IDM, next) that follows A's most likely future: FDE
  0.92 m.

In truth, B is slowest at :math:`t` = 3.2 s, at 6.48 m/s.

.. note::

   To predict B, predict A first. A predictor that treats each road user
   alone cannot.


.. _l8-lec-idm:

The Intelligent Driver Model (IDM): B's Acceleration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A model of a driver following another car (Treiber et al., 2000):

.. math::

   a = a_{\max}\Big[\,1 - \Big(\frac{v}{v_0}\Big)^{4} - \Big(\frac{s^*}{s}\Big)^2\,\Big]

- :math:`a`: B's acceleration; :math:`v`: B's speed; :math:`s`: the gap from
  B's front to A's rear; :math:`s^*`: the gap B wants (next section).
- :math:`a_{\max}` = 0.73 m/s²: B's top acceleration (the paper's value).
  :math:`v_0` = 9 m/s: the speed B would like to drive (chosen).
- :math:`1 - (v / v_0)^4`: on an empty road, B speeds up, less and less as
  :math:`v` nears :math:`v_0`.
- :math:`(s^* / s)^2`: grows as the gap :math:`s` shrinks; it is 1 when
  :math:`s` equals the gap B wants, :math:`s^*`. B brakes when this term is larger than the free-road
  term (step 5 of :ref:`l8-lec-idm-hand`).

.. tip::

   See "The IDM's parameters, and steady following" in :doc:`Going Further
   <l8_appendix>`.


.. _l8-lec-idm-gap:

The IDM: the Gap B Wants
~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   s^* = s_0 + v\,T + \frac{v\,\Delta v}{2\sqrt{a_{\max}\,b}}

- :math:`s_0` = 2 m: the smallest gap, even when B stands still.
- :math:`v\,T`, with :math:`T` = 1.6 s: B keeps 1.6 s of driving between
  itself and A.
- :math:`\Delta v`: B's speed minus A's, how fast B closes in. With
  :math:`b` = 1.67 m/s², a comfortable braking, the last term adds room when
  B closes in fast.
- :math:`T`, :math:`b` and :math:`s_0` are the paper's values (Treiber et
  al., 2000).


.. _l8-lec-idm-hand:

The IDM, by Hand, for Car B
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. From the tracks: :math:`v` = 7.76 m/s, A's 5.99, so :math:`\Delta v` =
   7.76 − 5.99 = 1.77 m/s; :math:`s` = 22.25 m.
2. The gap B wants: :math:`\sqrt{a_{\max}\,b} = \sqrt{0.73 \times 1.67}` =
   1.104, so :math:`s^*` = 2 + 7.76 × 1.6 + 7.76 × 1.77 / (2 × 1.104) =
   2 + 12.42 + 6.22 = 20.64 m.
3. The free-road term: 1 − (7.76 / 9)⁴ = 1 − 0.553 = 0.447.
4. The gap term: (20.64 / 22.25)² = 0.861.
5. The gap term is 0.861 − 0.447 = 0.414 larger, so B's acceleration
   :math:`a` is 0.73 × 0.414 = **0.30** m/s² of braking: B starts to brake.


.. _l8-lec-gap:

Car A Waits for a Gap in the AV's Lane
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A turns left across oncoming traffic, so it must give way to the AV.

.. admonition:: Definition: Critical headway (gap acceptance)
   :class: note

   The shortest gap, in seconds, that a driver accepts to make a maneuver
   across traffic. The Highway Capacity Manual's base value for a left turn
   from the major street of a two-lane road, at a junction with stop signs
   on the side street: **4.1 s**, as reproduced in the McTrans Center's
   users guide (McTrans Center, HCS Two-Way Stop Controlled Intersections
   Users Guide). We use it for car A (chosen).

Our car A decides 6 m before the junction (chosen). Run 1 is the scene so
far:

1. At that moment the AV is 48 m from the point where A's turn crosses its
   lane: 48 / 8 = 6.0 s (we placed it there).
2. 6.0 s ≥ 4.1 s: A turns without stopping.


.. _l8-lec-run2:

A Second Run, with the AV 24 m Closer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/run2.png
   :alt: Car A's meters driven against time from 0 to 5 seconds, in the second run. A gray dotted horizontal line near 6.5 meters, tag 1 above it: A reaches the junction there. The black truth rises to about 5.5 meters by 1.5 seconds and stays there: A waits. A green dashed line, the left mode with the AV ignored, rises straight to about 27 meters. A solid green line, the left mode with the gap rule, follows the truth, flat, and starts rising after about 4 seconds. A dash-dotted vertical line at 3.64 seconds, tag 2 beside it: the AV has passed.
   :width: 70%
   :align: center

   Run 2: car A's meters driven against time, 0 = now. **1:** the gray
   dotted line, where A reaches the junction. **2:** the dash-dotted line,
   when the AV has passed, 3.64 s. Black: the truth, A waits. Green dashed:
   the left mode with the AV ignored. Solid green: the left mode with the
   gap rule.

Run 2: only the AV starts 24 m further east, so 24 m closer to the
crossing. **1** A reaches the junction; **2** the AV has passed.

1. Gap: 6.0 − 24 / 8 = 3.0 s, below 4.1 s: A stops and waits.
2. The AV reaches the crossing at 6.08 − 3 = 3.08 s and is a car length past
   it at 3.08 + 4.5 / 8 = 3.64 s (**2**). The gap rule says A goes then; our
   driver waits 1 s more (chosen): 4.64 s.
3. Left mode, AV ignored: FDE 18.31 m. With the gap rule: 0.86 m, from that
   1 s.

.. note::

   Same track for A up to :math:`t` = 0, different futures: the **AV's**
   motion is an input to A's prediction.


.. _l8-lec-pet:

Post-Encroachment Time: How Close the Two Runs Came
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Post-encroachment time (PET)
   :class: note

   "Post-encroachment time is the time between when the first vehicle last
   occupied a position and the time when the second vehicle subsequently
   arrived to the same position" (Gettman et al., 2008). A larger PET is a
   wider margin.

.. figure:: /_static/images/L8/pet_timeline.png
   :alt: A timeline from 0 to 8 seconds, time from now, in two parts. Run 1: an orange bar for car A from 3.19 to 4.09 seconds and a black bar for the AV from 5.63 to 6.19, with a double arrow between them, tag 1. Run 2: a black bar for the AV from 2.63 to 3.19 seconds, a double arrow from 3.19 to 8, tag 2, and an orange arrow for car A pointing right from 8 seconds.
   :width: 95%
   :align: center

   When each car's body is on the red cross, against the time from now:
   run 1 on top, run 2 below. Orange: car A; black: the AV. **1:** run 1's
   PET, from A leaving to the AV arriving. **2:** run 2's PET so far, from
   the AV leaving to the end of the run at 8 s; the orange arrow: A has not
   arrived by then.

The bars show when each car's body is on the red cross. The body runs from
the rear bumper, 0.9 m behind the car's position, to the front bumper, 3.6 m
ahead of it.

- **1** Run 1: A leaves at 4.09 s, the AV arrives at 5.63 s.
  PET = 5.63 − 4.09 = 1.54 s.
- **2** Run 2: the AV leaves at 3.19 s; A has not arrived when the run ends,
  at 8.0 s. PET is more than 8.0 − 3.19 = 4.81 s.

.. note::

   ADE and FDE say how good a prediction is; PET says how close two road
   users come. A planner can compute PET on a predicted future too, before
   the cars get there.


.. _l8-lec-av-plan:

The AV's Plan Changes the Other Drivers' Futures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   "Our key insight is that an autonomous car's actions will actually
   affect what other cars will do in response, whether the car is aware of
   it or not" (Sadigh et al., 2016).

- In run 2, an AV that arrived 1 s later would give A a 3.0 + 1 = 4.0 s
  gap: still below 4.1 s, so A would still wait. Arriving 2 s later gives
  5.0 s, and A would go.
- So predicting A needs the AV's plan, and choosing the plan needs A's
  prediction. Planners either alternate (predict, plan, predict again) or
  solve both together.
- Our predictor used one fixed gap, 4.1 s, for every driver. Real drivers'
  gaps vary.


.. _l8-lec-behavior:

What a Behavior Layer Gets from Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A behavior layer chooses what the AV does next (keep going, slow down, stop)
from the objects around it. There are two ways to look at car A at
:math:`t` = 0:

1. **Current position only:** A is in the other lane, 4 m from the AV's lane
   center. A check that uses only current positions sees A in the AV's
   lane at :math:`t` = 3.4 s, when A is already there.
2. **Predicted positions:** at :math:`t` = 0, the left mode (P(left) =
   0.87) already puts A in the AV's lane from :math:`t` = 3.2 to 4.0 s.

.. note::

   The prediction warns the AV 3.4 s earlier, at :math:`t` = 0: time to
   ease off gently instead of braking hard. GP4's behavior node reads
   current fused objects; a predicted path is the next input to add.


.. _l8-lec-handson-interact:

Hands-On, Part 4: Drivers Who React
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``interact`` part of the hands-on script shows B, A and the AV: car A's
meters driven on the left, car B's speed on the right. The commands are on
:doc:`the Code page <l8_code>`.

.. admonition:: What to look at
   :class: hint

   1. Run 1: compare B's speed from CV and from the IDM. At what time do the
      two speed curves start to differ?
   2. Tick **AV 24 m closer** (run 2). Read A's gap in the title. Which of
      the two "most likely mode" lines matches the truth?
   3. In ``l8sim.py``, set ``GAP = 2.5``. ``GAP`` is the critical headway,
      4.1 s in the lecture. What does A do in run 2 now? And car B, behind
      it?


.. _l8-lec-next:

Next Class
----------

.. admonition:: Today
   :class: important

   Car A, braking, was 6.5 m before the junction at :math:`t` = 0; the
   physics models said "straight on" (CV's FDE 12.35 m). The map gave two
   futures; A's speed made the left turn 0.87 likely, and that mode ended
   1.88 m from the truth. Car B needed A's prediction (FDE: IDM 0.92 m, CV
   3.55 m), and A's own choice needed the AV's position (run 2).

- **L9, Motion Planning:** paths for the AV that keep clear of every likely
  future of every road user.

**Before next class**

- Run the four hands-on parts on :doc:`the Code page <l8_code>`.
- Read :doc:`Going Further <l8_appendix>`: four parts, listed at the top of
  that page.
- Read :doc:`Foxglove: A Second Viewer for ROS 2 </preread/foxglove>` and try
  its layout.


.. rubric:: Image credits

The vehicle icons in the figures on this page were created by Stone from the
`Noun Project <https://thenounproject.com>`_. The lanes in every top view
come from CARLA's ``Town01.xodr``.
