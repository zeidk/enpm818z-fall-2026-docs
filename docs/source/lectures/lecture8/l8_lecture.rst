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
   - learned predictors: what they read and write, three well-known
     designs, how they are trained and scored, and pedestrians and cyclists;
   - the terms of the Intelligent Driver Model, one by one.

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
(:math:`v_x`, :math:`v_y`, in m/s). Before each new set of detections,
:math:`\Delta t` = 0.1 s later, it predicts the state with constant
velocity:

.. math::

   p_x \leftarrow p_x + v_x\,\Delta t, \qquad p_y \leftarrow p_y + v_y\,\Delta t

- The tracker needs **one** step: where to look for the object among the
  next detections. A new detection then corrects it.
- The planner needs **many** steps: where the object will be 1, 2, ..., 5 s
  from now. No detection corrects those until they happen.
- Constant velocity has no turn in it: a car that is turning is predicted to
  drive straight on.


.. _l8-lec-tempe:

The Tempe Crash, March 2018
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tempe, Arizona, at night (L1 and L5): a developmental test vehicle in
automated mode hits a pedestrian walking a bicycle across the road, outside
a crosswalk. L5 showed the crash from the tracker's side. The report of the
NTSB (National Transportation Safety Board) also says what happened to the
prediction. ADS is the vehicle's automated driving system (NTSB, 2019):

.. note::

   "The ADS detected the pedestrian 5.6 seconds before impact. Although the
   ADS continued to track the pedestrian until the crash, it never
   accurately classified her as a pedestrian or **predicted her path**."

   "If the perception process changed the classification of a detected
   object, it no longer considered the tracking history of that object when
   generating a new trajectory."

- A prediction is built from the track's history. With the history thrown
  away at every new class, the system had no path for her across the road.
- The system saw an emergency only when she was in the vehicle's path:
  1.2 s before impact (L5).


.. _l8-lec-needs:

What the Planner Needs from Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Trajectory prediction
   :class: note

   For each road user near the AV, from its past track and the map: its
   future positions over a time horizon (here every 0.1 s for 5 s), how sure
   each one is, and, when it could do different things, several futures with
   a probability each.

1. **Where:** a position at each future time. The planner
   checks its own path against each of them, time by time.
2. **How sure:** an uncertainty that grows with the horizon. The planner
   keeps more room where it is larger.
3. **Which future:** a car at a junction may go straight on or turn. Each
   option is one predicted future with its own probability.


.. _l8-lec-how-far:

How Far Ahead to Predict
~~~~~~~~~~~~~~~~~~~~~~~~

The prediction must reach at least as far ahead as the AV needs to react and
stop. Our AV drives at 8 m/s (GP4's default ``target_speed``). We chose the
reaction time and the braking for this example.

1. Reacting (sensing, deciding) takes 0.5 s. The AV drives
   8 × 0.5 = 4.0 m in it.
2. Braking at 3 m/s² takes 8 / 3 = 2.67 s, over speed × speed / (2 ×
   braking) = 8 × 8 / (2 × 3) = 10.67 m.
3. In all: 0.5 + 2.67 = 3.17 s and 4.0 + 10.67 = 14.67 m.

So the prediction must reach at least 3.17 s ahead. Today we predict 5 s
ahead (chosen): that covers the 3.17 s, with room to slow down gently
instead of braking hard.


.. _l8-lec-datasets:

Prediction Windows in Public Datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public datasets of recorded traffic, used to train and score predictors, fix
two windows: **observed**, how much past track the predictor reads, and
**predicted**, how far ahead it must predict.

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
   * - **Today** (chosen)
     - 2 s
     - 5 s

Today we read 2 s of track, as Argoverse does.


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
     - **Today**
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

Learned predictors (in :doc:`Going Further <l8_appendix>`) can work at any
of the three levels.


.. _l8-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

After this lecture, you can:

1. say what a planner needs from prediction, and how far ahead it must look;
2. predict a road user's motion by hand with constant velocity (CV),
   constant turn rate (CTRV) and constant turn rate and acceleration (CTRA),
   and say why their error grows with the horizon;
3. score a prediction with ADE, FDE and the miss rate, and several
   predictions with minADE and minFDE; check whether an uncertainty is
   honest;
4. use the map's lanes as candidate paths and give each one a probability
   with Bayes' rule;
5. model another driver's intent, its reaction to the car ahead (the IDM),
   and its gap acceptance.


.. _l8-lec-scene:

The Scene
---------

We set up one junction of Town01, the town of L7, with three road users.

**What it is for:** every predictor is compared on the same scene, against a
truth we know.

**Where the numbers come from.** The lanes are CARLA's: read from
``Town01.xodr`` with ``carla.Map``, with no CARLA server. The motion is
ours: simulated in Python on those lanes, so the truth is known exactly.
Every speed and every braking is chosen, and these notes say so.


.. _l8-lec-junction:

The Junction, from Town01's Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/scene_map.png
   :alt: A top view of a T-junction from Town01's map, x east from 98 to 214 meters, y north from minus 24 to 12 meters. A road runs east to west with one lane each way, a white dashed center line, and a side road leaving the junction to the south. Tag 1: the AV, a black car on the south lane at x 107, facing east. Tag 2: car A, an orange car on the north lane at x 175, facing west. Tag 3: car B, a gray car on the north lane at x 201, facing west. Tag 4: a red cross in the junction at x 156, y minus 2, where the left turn from the north lane crosses the AV's lane.
   :width: 95%
   :align: center

   A T-junction of Town01, from above, :math:`x` east and :math:`y` north in
   meters, all at :math:`t` = 0. **1:** the AV, on the south lane, facing
   east. **2:** car A and **3:** car B, on the north lane, facing west.
   **4:** the red cross, where A's left turn would cross the AV's lane.

:math:`t` is the time in seconds, and :math:`t` = 0 is now. **1** is the
AV, **2** car A and **3** car B. **4**, the red cross, is where A's left
turn would cross the AV's lane.

Measured on the map: the lanes are 4.0 m wide. A's left turn is about a
quarter circle, 23.07 m long, so its radius is 23.07 / (π/2) = 14.7 m.


.. _l8-lec-truth:

The Truth We Simulated
~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/scene_truth.png
   :alt: The same top view with each road user's next 5 seconds drawn as a line with a dot every second, and the three cars faded at their positions now. The AV's black line runs east along its lane from x 107 to about 147, labeled 5 s at its end. Car A's orange line runs west, then curves left through the junction into the side road, ending at x 154, y minus 7, labeled 5 s. Car B's gray line runs west along the north lane from x 201 to about 166, under car A's line where they overlap. Dark tags 1, 2 and 3 mark the AV, car A and car B; a red cross with tag 4, in the junction at x 156, y minus 2, marks where car A's turn crosses the AV's lane.
   :width: 95%
   :align: center

   Where each road user really goes over the next 5 s, a dot every second.
   **1:** the AV, black, east along its lane. **2:** car A, orange, west and
   then left into the side road. **3:** car B, gray, west along the north
   lane, under A's line where they overlap. **4:** the red cross, where A's
   turn crosses the AV's lane.

Each line is where a road user really goes over the next 5 s, with a dot
every second. We chose this motion; the AV does not know it.

- **1** The AV drives east at 8 m/s, straight on. It reaches the red cross
  (**4**) at :math:`t` = 6.08 s.
- **2** Car A drove at 8 m/s until :math:`t` = −2 s, and has braked at
  1.0 m/s² since. It turns left at 5.0 m/s and is in the AV's lane from
  :math:`t` = 3.4 to 4.3 s.
- **3** Car B follows A, with 22.3 m between A's rear and B's front, and
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

We predict car A from its track alone, with three models: constant
velocity, constant turn rate, and constant turn rate and acceleration.

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

For the first 2 s the error stays at 1.5 m or less. Once A turns, each
second adds meters.


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
- With a turn rate near 0, CTRV's formula divides by almost 0: code must
  switch to CV there.

.. tip::

   See "CTRV, written out" and "CTRA: CTRV with a changing speed" in
   :doc:`Going Further <l8_appendix>`.


.. _l8-lec-all-three:

CV, CTRV and CTRA from t = 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/ctra_now.png
   :alt: The same close-up of the junction with car A at x 175. The black truth curves left into the side road. Three predictions run west along the north lane: blue CV straight to x 145; purple dashed CTRV bending slightly south, ending at x 145, y minus 2.6; brown dash-dotted CTRA shorter, slowing, ending at x 157, y minus 0.3. None follows the truth into the side road.
   :width: 70%
   :align: center

   Car A's three physics predictions from :math:`t` = 0, a dot every second.
   Black: the truth. Blue: CV, straight west. Purple dashed: CTRV, bending
   a little south. Brown dash-dotted: CTRA, shorter because it slows. None
   follows the truth into the side road.

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

CTRA uses A's braking, so it keeps A closer to the junction. None of the
three knows the turn is coming: at :math:`t` = 0, A has not started it.


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

Error Against Horizon, on 2417 Predictions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/err_horizon.png
   :alt: Two panels of mean error in meters against horizon from 0 to 5 seconds, a gray dotted line at 2 meters. Left, no turn in the next 5 s, 1329 predictions: blue CV rises slowly to 4.0 meters at 5 seconds; purple dashed CTRV to 10.5; brown dash-dotted CTRA to 16.1. Right, a turn in the next 5 s, 1088 predictions: all three rise steeply and close together, CV to 21.7, CTRV to 20.1, CTRA to 19.1 meters.
   :width: 95%
   :align: center

   Mean error against horizon on our test set. **Left:** no turn in the
   next 5 s, 1329 predictions. **Right:** a turn in the next 5 s, 1088
   predictions. Blue: CV. Purple dashed: CTRV. Brown dash-dotted: CTRA.
   Gray dotted line: 2 m, the error the next section counts as a miss.

**Our test set:** every way through the junction, at 6 to 10 m/s, with
random braking and turn speeds (chosen), one prediction every 0.5 s. CV's
mean error at 1, 3 and 5 s is 0.52, 1.80 and 4.01 m with no turn, and 1.54,
9.19 and 21.71 m with a turn. The gray dotted line is at 2 m, the error the
next section counts as a miss.

.. tip::

   See "How the test set is built" in :doc:`Going Further <l8_appendix>`.


.. _l8-lec-why-grows:

Why the Error Grows, and Why More Terms Do Not Help
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Any error in the speed grows with time.** 0.1 m/s off is 0.5 m after
   5 s. A speed that changes (a driver slowing for no reason we can see)
   adds more.
2. **A physics model cannot see a maneuver coming.** Before the turn,
   A's turn rate is 0. Only a predictor that knows the junction can read
   A's braking as a turn. With a turn ahead, all three models
   are 19 to 22 m off at 5 s.
3. **Each extra term is carried 5 s ahead.** With no turn, CTRV's turn rate
   and CTRA's braking often come from a turn that is ending or braking that
   will stop: 10.5 and 16.1 m against CV's 4.0 m.

.. note::

   With no turn ahead, CV's mean error stays under 2 m for 3 s (1.80 m). With a turn
   ahead, every model is past 2 m before 2 s. Beyond that, the AV needs to
   know **what the road user can do**: the next sections add the maneuvers
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

We score a whole prediction with one number (ADE, FDE), call it a hit or a
miss, and check the uncertainty it reports.

**What it is for:** with scores we compare predictors and tell when a prediction's own uncertainty can be trusted.


.. _l8-lec-ade-fde:

ADE and FDE
~~~~~~~~~~~

.. admonition:: Definition: ADE and FDE
   :class: note

   **Displacement error** at one time: the distance between the predicted
   and the true position. **ADE** (average displacement error): its average
   over every predicted time. **FDE** (final displacement error): its value
   at the last predicted time (Chang et al., 2019; Wilson et al., 2021).

Car A's CV prediction, with only the five whole seconds:

1. The errors at 1 to 5 s: 0.52, 1.50, 2.58, 6.01 and 12.35 m.
2. ADE: (0.52 + 1.50 + 2.58 + 6.01 + 12.35) / 5 = 22.96 / 5 = 4.59 m.
3. FDE: the last one, **12.35** m.

Over all 50 predicted times (every 0.1 s from 0.1 to 5.0 s), the ADE is
3.37 m. From now on, ADE uses all 50.


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
     - **No turn** (1329)
     -
     -
     - **A turn** (1088)
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
     - 1.67
     - 4.01
     - 37.9%
     - 8.34
     - 21.71
     - 99.6%
   * - CTRV
     - 3.93
     - 10.50
     - 62.6%
     - 7.29
     - 20.14
     - 99.7%
   * - CTRA
     - 5.89
     - 16.13
     - 79.3%
     - 7.04
     - 19.07
     - 99.3%

- With a turn ahead, the physics models miss almost every time.
- With no turn, CV is the best of the three, and still misses 37.9% of the
  time at 5 s: our simulated drivers never hold a speed exactly (a slow
  random acceleration, 0.3 m/s² standard deviation, chosen).


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
They grow because the fitted velocity has an error, and because CV allows
the speed to drift (0.5 m/s per :math:`\sqrt{\text{s}}`, chosen).

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - :math:`h`
     - :math:`\sigma`
     - **95% radius**
   * - 1 s
     - 0.29 m
     - 0.72 m
   * - 3 s
     - 1.50 m
     - 3.68 m
   * - 5 s
     - 3.23 m
     - 7.91 m

:math:`\sigma` is the standard deviation of the position, per axis. The 95%
radius is 2.45 × :math:`\sigma` (2.45 = :math:`\sqrt{5.99}`, rounded; the appendix says why).
The truth is inside at 1, 2 and 3 s, outside at 4 and 5 s.

.. tip::

   See "CV's uncertainty, term by term" and "Why the 95% region's radius is
   2.45σ" in :doc:`Going Further <l8_appendix>`.


.. _l8-lec-honest:

How Often the Region Holds the Truth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/coverage.png
   :alt: Percent of true positions inside CV's 95 percent region against horizon, 0 to 5 seconds. A red line at 95 percent is labeled 95 percent: what the region promises. A solid blue line, no turn, rises from about 57 to about 85 percent and stays between 81 and 85 percent. A dashed blue line, a turn, starts near 45 percent and falls to about 5 percent at 5 seconds.
   :width: 70%
   :align: center

   The share of true positions inside CV's 95% region, against horizon, on
   our test set. Red: 95%, what the region promises. Solid blue: no turn.
   Dashed blue: a turn.

A 95% region must hold the truth 95% of the time. On our test set, at 1, 3
and 5 s:

- no turn: 81.1, 85.2 and 81.1%: a little too sure;
- a turn: 42.8, 15.3 and 4.8%: far too sure.

The region only covers CV's own kind of error: a slightly wrong speed. It
knows nothing about a turn.

.. note::

   L6 checked a localizer the same way (NIS, integrity). For a predictor:
   count how often the truth falls in its region, separately for turns.


.. _l8-lec-scoring-summary:

Physics Models, Scored
~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Summary: physics models, scored
   :class: tip

   - **Car A, from t = 0:** CV's FDE 12.35 m, CTRV's 10.00 m, CTRA's
     7.26 m: three misses. A had not started its turn.
   - **The test set:** with no turn, CV's mean error stays under 2 m for 3 s (1.80 m) and
     is the best of the three. With a turn ahead, all three are past 2 m
     before 2 s, and miss at 5 s almost every time (99.3 to 99.7%).
   - **Uncertainty:** CV's 95% region held the truth 81 to 85% of the time
     with no turn, 4.8% at 5 s with one.
   - **So:** for more than a second or two near a junction, the predictor
     must consider what the road user **could do**: several futures.


.. _l8-lec-futures:

Several Futures
---------------

A prediction gives several futures for each road user, each with a
probability, and we score them.

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
into the side road. A right turn is not possible from A's lane.

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

At 5 s, point **3** is 7.21 m from each future, toward the junction's
corner. No driver in A's lane ends up at point **3**.

Its FDE against the truth is 5.92 m, a miss, while the left-turn future
alone is off by 1.88 m.

.. note::

   A predictor trained to give one answer with the smallest mean squared
   error learns to give point **3**, the average. So predictors give
   **several** futures instead.


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

1. minADE: the smaller of 0.86 and 3.55, so 0.86 m.
2. minFDE: the smaller of 1.88 and 13.06, so 1.88 m. That is under 2 m, so
   **not** a miss. A miss now means that **no** mode ends within 2 m.

.. note::

   The best of :math:`K` asks: was the truth among the futures the
   predictor offered? It does not look at the probabilities.


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
  future. For car A: 0.87.

.. note::

   Car A's prediction is a good one: two modes, the left turn 1.88 m from
   the truth, with 0.87 of the probability.


.. _l8-lec-planner-two:

What the Planner Does with Two Futures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AV's own plan is 8 m/s, straight on. It reaches the point where A's left
turn crosses its lane at :math:`t` = 6.08 s.

1. For each mode, find when it puts car A in the AV's lane: the left turn,
   from :math:`t` = 3.2 to 4.0 s; straight on, never.
2. Weigh each mode by its probability: 0.87 for the one that crosses.
3. Plan so that the AV is not at the crossing while a likely mode is. At
   8 m/s the AV arrives at 6.08 s, after A has left the lane, so it can keep
   its speed. A plan that reached the crossing near :math:`t` = 4 s would
   have to slow down.

.. note::

   Which modes count, and how much room to keep for each, is the planner's
   job (L9). The prediction's job: offer every likely future, with honest
   probabilities and times.


.. _l8-lec-map:

Using the Map
-------------

The futures come from the map's lanes, and their probabilities come from
Bayes' rule applied to the track.

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
- Our script reads them with ``carla.Map`` from ``Town01.xodr``, with no
  CARLA server: ``junction.get_waypoints()`` gives each way's first and last
  waypoint, and each lane is followed from there.

.. important::

   **The plan for car A, in four steps:** we put A on each lane, give each
   path the speed it expects, check which path explains A's motion, and
   turn that into probabilities.


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

   Before the junction, the two lanes are one: offset and heading cannot
   tell them apart. Only A's **speed** can, so far. Once A starts turning,
   its heading leaves the straight lane's.


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

   Each mode's predicted future follows its lane at its own speed. Straight
   on keeps 5.99 m/s. Left brakes evenly to 5.42 m/s by the junction, holds
   it through the turn, then speeds up.


.. _l8-lec-step3-likelihood:

Step 3: How Well Each Path Explains A's Speed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A bell curve scores how far A's speed is from each path's expected speed.
This score is the **likelihood**, :math:`e^{-\frac12 (\Delta v / \sigma)^2}`,
where :math:`\Delta v` is A's speed minus the path's, and :math:`\sigma` =
1.0 m/s (chosen: drivers differ by about that much).

1. Left: :math:`\Delta v` = 5.988 − 6.512 = −0.524 m/s;
   :math:`e^{-\frac12 (0.524)^2} = e^{-0.137}` = **0.872**.
2. Straight on: :math:`\Delta v` = 5.988 − 8.000 = −2.012 m/s;
   :math:`e^{-\frac12 (2.012)^2} = e^{-2.024}` = **0.132**.
3. Heading and offset: the same for both lanes here (0.973 and 0.995), so
   they change nothing.

.. note::

   A drives 2.01 m/s slower than a car going straight on would, and only
   0.52 m/s slower than a car about to turn. The slowing down is the
   evidence.


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
   likelihoods divided by their sum, 0.872 / (0.872 + 0.132) = 0.87. A
   prior from data (how often drivers turn left here) would change that.

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
5.42 m/s, and A turns at 5.0 m/s (our choice for the truth). The error grows
by about 0.4 m every second.

CV, for comparison: FDE 12.35 m.


.. _l8-lec-map-test:

Map-Aware Prediction on the Test Set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/test_scores.png
   :alt: A bar chart of mean FDE at 5 seconds, in meters, on the test set's predictions with a turn ahead. Blue CV 21.7, purple CTRV 20.1, brown CTRA 19.1, green map most likely mode 5.6, and a hatched green bar, map best of the modes, 1.9. A gray dotted line at 2 meters.
   :width: 70%
   :align: center

   Mean FDE at 5 s on the test set's predictions with a turn ahead. Blue:
   CV. Purple: CTRV. Brown: CTRA. Green: the map's most likely mode.
   Hatched green: the best of the map's modes (minFDE). Gray dotted line:
   2 m, the miss threshold.

With a turn ahead (1088 predictions):

- The most likely mode has a mean FDE of 5.61 m and misses 53.6% of the
  time.
- The best of the modes has a mean minFDE of 1.92 m and misses 40.5% of the
  time.
- The true path gets 0.68 of the probability on average, and at least half
  of it 82% of the time.

With no turn, the most likely mode's mean FDE is 4.07 m, CV's 4.01 m; the
best of the modes, 1.08 m.


.. _l8-lec-map-wrong:

Where Map-Aware Prediction Goes Wrong
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **The speed along the path.** The right lane at the wrong speed still
   misses: our test set's drivers turn at 1.5 to 2.5 m/s² sideways, and the
   predictor assumes 2.0.
2. **A driver who does not look like the rule.** A car cruising at 6 m/s on
   an 8 m/s street looks like a car about to turn.
3. **Off the map.** A car that leaves its lane (a U-turn, parking, avoiding
   something) has no lane to follow. Pedestrians and cyclists follow few
   lanes at all.
4. **A wrong map.** If roadworks close a lane, L7's map is out of date.

.. note::

   Keep a physics mode next to the lane modes. When no lane fits (a large
   offset or heading gap on every lane), the physics mode takes the
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

Our predictor used lanes as modes, and probabilities from rules we chose (a
turn speed, a :math:`\sigma`). Learned predictors learn the turn speeds,
:math:`\sigma`'s and priors that we chose by hand, from recorded driving.

**What it is for:** you will know the names and the shape of the predictors
that production systems and the benchmarks use.

What they read, what they write, and how they are scored is in
:doc:`Going Further <l8_appendix>`, to read after class.


.. _l8-lec-drivers:

Other Drivers
-------------

Drivers react to each other: car B to car A, and car A to the AV.

**What it is for:** predictions then agree with each other, and the AV knows
that its own motion changes what others do.

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
     - A turn or a stop may be ahead. Step 4 got P(left) = 0.87 from A's
       speed alone.
   * - Position in the lane
     - A car drifting toward a lane boundary may change lanes (Autoware
       Foundation, map-based prediction).
   * - Turn signal
     - A camera can read it, but drivers forget it, or leave it on.
   * - Where the lane goes
     - Only some maneuvers are possible from a lane: no right turn from
       A's.


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

The Intelligent Driver Model (IDM), by Hand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The IDM is a model of a driver following another car (Treiber et al.,
2000): accelerate toward a desired speed, brake when the gap gets smaller
than a desired gap.

.. math::

   a = a_{\max}\Big[\,1 - \Big(\frac{v}{v_0}\Big)^{4} - \Big(\frac{s^*}{s}\Big)^2\,\Big],
   \qquad s^* = s_0 + v\,T + \frac{v\,\Delta v}{2\sqrt{a_{\max}\,b}}

- :math:`a`: B's acceleration (negative is braking).
- :math:`v`: B's speed; :math:`s`: the gap to A; :math:`\Delta v`: how fast
  B closes in; :math:`s^*`: the gap B wants.
- The paper's values: desired time gap :math:`T` = 1.6 s, top acceleration
  :math:`a_{\max}` = 0.73 m/s², comfortable braking :math:`b` = 1.67 m/s²,
  smallest gap :math:`s_0` = 2 m. Desired speed :math:`v_0` = 9 m/s
  (chosen).

1. From the tracks: :math:`v` = 7.76 m/s, A's speed 5.99 m/s, so
   :math:`\Delta v` = 7.76 − 5.99 = 1.77 m/s; :math:`s` = 22.25 m.
2. :math:`s^*` = 2 + 7.76 × 1.6 + 7.76 × 1.77 / (2 × 1.104) = 20.64 m, where
   :math:`\sqrt{a_{\max}\,b} = \sqrt{0.73 \times 1.67}` = 1.104.
3. :math:`a` = 0.73 × [1 − 0.553 − (20.64 / 22.25)²] = 0.73 × (0.447 −
   0.861) = **−0.30** m/s²: B starts to brake.

.. tip::

   See "The IDM's terms, one by one" in :doc:`Going Further <l8_appendix>`.


.. _l8-lec-gap:

Car A Waits for a Gap in the AV's Lane
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A turns left across oncoming traffic: on a green light it must give way to
the AV.

.. admonition:: Definition: Critical headway (gap acceptance)
   :class: note

   The shortest gap, in seconds, that a driver accepts to make a maneuver
   across traffic. The Highway Capacity Manual's base value for a left turn
   from the major street of a two-lane road: **4.1 s**, as reproduced in
   the McTrans Center's users guide (McTrans Center, HCS Two-Way Stop
   Controlled Intersections Users Guide).

Our car A decides 6 m before the junction (chosen). Run 1 is the scene so
far:

1. At that moment the AV is 6.0 s from the point where A's turn crosses its
   lane.
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

Run 2 has the same history for A and B; only the AV starts 24 m further
east, so 24 m closer to the crossing. **1** marks where A reaches the
junction, **2** when the AV has passed.

1. Gap: 24 m at the AV's 8 m/s is 3 s less, 6.0 − 24 / 8 = 3.0 s. That is
   below 4.1 s, so A stops and waits.
2. The AV passes at 3.64 s (**2**); A goes at 4.64 s.
3. Left mode, AV ignored: FDE 18.31 m. With the gap rule: 0.86 m.

.. note::

   A's track up to :math:`t` = 0 is the same in both runs. What A does next
   depends on where the **AV** is: the AV's motion is an input to A's
   prediction.


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
   center. A check of current positions first finds A in the AV's lane at
   :math:`t` = 3.4 s, when it is there.
2. **Predicted positions:** at :math:`t` = 0, the left mode (probability
   0.87) already puts A in the AV's lane from :math:`t` = 3.2 to 4.0 s.

.. note::

   The prediction warns the AV at :math:`t` = 0, 3.4 s earlier: time to
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

   1. Run 1: compare B's speed from CV and from the IDM. When do they part?
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

   Car A was braking 6.5 m before the junction; the physics models said
   "straight on" (CV's FDE 12.35 m). The map gave two futures; A's speed
   made the left turn 0.87 likely, and that mode ended 1.88 m from the
   truth. Car B needed A's prediction (IDM: 0.92 m against CV's 3.55 m), and
   A's own choice needed the AV's position (run 2).

- **L9, Motion Planning:** paths for the AV that keep clear of every likely
  future of every road user.

**Before next class**

- Run the four hands-on parts on :doc:`the Code page <l8_code>`.
- Read, in :doc:`Going Further <l8_appendix>`, the sections on CTRV, on the
  region's honesty check and on learned predictors.


.. _l8-lec-foxglove:

Foxglove, Next to RViz
~~~~~~~~~~~~~~~~~~~~~~

In the GPs you watch your ROS 2 topics in RViz. Foxglove is a second viewer:
it connects to a running ROS 2 system through ``foxglove_bridge``, and it
opens ROS 2 recordings (``.mcap`` files) (`Foxglove's ROS 2 guide
<https://docs.foxglove.dev/docs/getting-started/frameworks/ros2>`__). The
commands to install the bridge, connect and record are on :doc:`the Code
page <l8_code>`.

- Foxglove needs a free account. Sign up with your umd.edu address: the
  Academic plan costs nothing.
- **Post-work:** record 30 s of your GP stack and open the recording in
  Foxglove.


.. rubric:: Image credits

The vehicle icons in the figures on this page were created by Stone from the
`Noun Project <https://thenounproject.com>`_. The lanes in every top view
come from CARLA's ``Town01.xodr``.
