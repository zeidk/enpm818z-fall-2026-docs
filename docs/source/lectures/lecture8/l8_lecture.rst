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
   - how our test set is built;
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

   In **L5**, we tracked every road user with one Kalman filter per object:
   an ID, a position and a velocity (top left in the figure below). In
   **L7**, we read the map's lanes and junctions to give the AV a route
   (bottom left). Today, trajectory prediction reads both and says, for each road user,
   where it **will be** over the next few seconds, how sure that is, and how
   likely each possible future is. The planner (L9) uses that to keep the AV
   clear of them, and control (L10) drives the plan.

.. figure:: /_static/images/L8/pred_stack.png
   :alt: A block diagram. Two gray input boxes on the left: tracks (L5), each road user's position and velocity; and the map (L7), lanes and junctions. Each has an arrow into a magenta box labeled trajectory prediction (today). A magenta arrow leads from prediction to a box labeled planning (L9), and an arrow from planning to a box labeled control (L10). Below prediction, a magenta box lists its output: for each road user, over the next few seconds, 1. where it will be, and how sure that is, 2. which of several futures, how likely.
   :width: 95%
   :align: center

   Where trajectory prediction sits. Its two inputs are the tracks of L5 and
   the map of L7. Its output goes to planning (L9), and planning's output to
   control (L10). For each road user, over the next few seconds, prediction
   gives **1** where it will be, and how sure that is, and **2** which of
   several futures, and how likely each one is.


.. _l8-lec-terms:

What Trajectory Prediction Means
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Trajectory prediction
   :class: note

   For each road user near the AV, from its past track and the map: its
   future positions over a time horizon, how sure each one is, and, when it
   could do different things, several futures with a probability each.

In this lecture, "prediction" always means trajectory prediction.

The words in it:

- **Road user:** anything that moves on or near the road: a car, a cyclist,
  a pedestrian.
- **Track** (L5): one road user followed over time: an ID, and its position
  and velocity from a Kalman filter.
- **Trajectory** (L7): a path with a time at each point. A predicted
  trajectory says where the road user will be, and when.
- **Horizon:** how far ahead the prediction reaches. Ours: 5 s, in 50 steps
  of 0.1 s.


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

- The tracker needs **one** step: where the object will be 0.1 s from now,
  so it knows where to look among the next detections. When that detection
  arrives, it corrects the step.
- The planner needs **many** steps: where the object will be every 0.1 s, up
  to 5 s from now (50 steps). No detection can correct a step until its
  moment comes.
- The predictor runs as often as the tracker: each new set of tracks, every
  0.1 s, gives a new 5 s prediction that replaces the last one. Apollo and
  Autoware also run their predictor on each new output of the tracker
  (Apollo Auto, ``prediction_component.cc``; Autoware Foundation,
  ``callbacks.cpp``).
- Constant velocity has no turn in it: a car that is turning is predicted to
  drive straight on.


One Step for the Tracker, 50 for the Planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/steps_timeline.png
   :alt: A time axis from minus 0.5 to 5 seconds, time from now, with a dotted line at 0 and two rows. Row tracker: six dark dots from minus 0.5 to 0 seconds, tag 1, and one blue circle at 0.1 seconds with a dark dot inside it, tag 2. Row planner: the same six dark dots, then 50 blue circles, one every 0.1 seconds from 0.1 to 5 seconds, tag 3.
   :width: 95%
   :align: center

   A time axis, not a picture of the road. Dark dots are detections; blue
   circles are predicted steps. **1:** detections, one every 0.1 s, up to
   now (:math:`t` = 0). **2:** the tracker predicts one step, 0.1 s ahead,
   then moves that prediction part of the way toward the next detection
   (L3's Kalman update). **3:** the planner needs
   50 steps, up to 5 s ahead; no detection corrects them until each moment
   comes.


.. _l8-lec-tempe:

The Tempe Crash, March 2018
~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the NTSB report on the Uber test vehicle (NTSB, 2019). ADS means its
automated driving system.

.. note::

   "The ADS detected the pedestrian 5.6 seconds before impact. Although the
   ADS continued to track the pedestrian until the crash, it never
   accurately classified her as a pedestrian or **predicted her path**".

   "If the perception process changed the classification of a detected
   object, it no longer considered the tracking history of that object when
   generating a new trajectory".

The report's table of what the ADS recorded shows what it predicted for her.

.. figure:: /_static/images/L8/tempe_paths.png
   :alt: A road seen from above, north to the right: a bicycle lane at the bottom, then the right and left through lanes, then the area where two left-turn lanes form, up to the median. Tag 1: a black car in the right lane, facing right. Tag 2: a dark arrow straight down across the lanes, ending in the right lane ahead of the car. Three gray rings, with no tag, on that arrow: one near its start, one in the turn-lane area, one in the right lane. Tag 3: a magenta arrow that starts on the dark arrow in the left through lane and points right, along that lane.
   :width: 80%
   :align: center

   Lane widths from the report; along the road, not to scale. **1:** the
   test vehicle, in the right lane at 45 mph. **2:** her path across the
   lanes, pushing a bicycle. **Gray rings:** at each class change, the ADS
   predicted she would stay put. **3:** while her class held (vehicle or
   bicycle), it predicted she would follow the left through lane, as a
   vehicle or a bicycle would: that class's goal. The goal set the
   direction; her history only adjusted it. Even her longest hold, 1.1 s as
   a bicycle (2.6 to 1.5 s before impact), gave a path along the lane.

.. important::

   **Why the lane, when it tracked her moving across?** Each path started
   from her class's goal: a vehicle or a bicycle in a lane gets "a goal of
   traveling in the direction of traffic in that lane" (NTSB, 2019). Her
   history only adjusted that path, and at each class change the ADS stopped
   using it. Only a pedestrian could get a path from its sideways motion,
   and the ADS never classed her as one. So it never predicted her crossing.

The system saw an emergency only when she was already in the vehicle's
path: 1.2 s before impact.


.. _l8-lec-needs:

What the Planner Needs from Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The planner here is the AV's **motion planner** (L9): it chooses the AV's
own path and speed for the next few seconds, and chooses again as it drives.
From each prediction it needs three things:

1. **Where:** the road user's position at each future time. At each of
   those times, the planner checks that the AV's own planned position stays
   clear of it.
2. **How sure:** an uncertainty that grows with the horizon. Where it is
   larger, the planner keeps the AV farther from the predicted position. A
   road user hidden for a
   moment (behind a truck, say) has gaps in its track, so its prediction is
   less sure.
3. **Which future:** a car at a junction may go straight on or turn. Each
   option is one predicted future with its own probability.


.. _l8-lec-how-far:

How Far Ahead to Predict
~~~~~~~~~~~~~~~~~~~~~~~~

The prediction must reach at least as far ahead as the AV needs to react and
stop. The AV drives at 8 m/s and sees an obstacle in its lane. **1:** it
reacts: it senses the obstacle and decides to brake. **2:** then it brakes
until it stops. **3** is the whole stop. We chose the reaction time and the
braking rate for this example.

.. figure:: /_static/images/L8/stopping_side.png
   :alt: A side view of the road, to scale, with a distance axis from 0 to 16 meters: distance driven since the AV sees the obstacle. A faded gray car, the AV when it sees the obstacle, has its front bumper at 0, with three short gray speed lines behind it to show it is moving. A black car, the same AV once it has stopped, stands with its front bumper at about 14.7 meters, just short of a red traffic cone, the obstacle, at about 15.6 meters. A darker gray band runs from 0 to 4 meters and a lighter gray band from 4 to 14.7 meters, with dashed vertical lines at 0, 4 and 14.7. Above the road, a double arrow from 0 to 4 marked tag 1 and a double arrow from 4 to 14.7 marked tag 2. Below the road, a double arrow from 0 to 14.7 marked tag 3.
   :width: 95%
   :align: center

   The same AV twice, from the side, drawn to scale. Faded: when it first
   sees an obstacle, at 8 m/s; black: once it has stopped. **1:** reacting,
   4.0 m. **2:** braking, 10.67 m. **3:** in all, 14.67 m.

The numbers:

1. **Reaction time**, to sense the obstacle and decide to brake: 0.5 s
   (chosen). The AV drives 8 × 0.5 = 4.0 m before its brakes even start.
2. **Braking time:** the speed drops 3 m/s every second (3 m/s², chosen), so
   slowing from 8 to 0 m/s takes 8 / 3 = 2.67 s. The speed falls evenly, so
   its average is halfway between 8 and 0: (8 + 0) / 2 = 4 m/s. The AV drives
   4 × 2.67 = 10.67 m more before it stops.
3. **Stopping time:** the reaction time plus the braking time, 0.5 + 2.67 =
   3.17 s, from seeing the obstacle to standing still. The distance is
   4.0 + 10.67 = 14.67 m.

Stopping is not the only answer: the AV may move to the next lane instead,
and that takes its own time. But the AV must be able to stop whatever else
it plans, so the stop sets the minimum: the prediction must reach at least
3.17 s ahead. We chose 5 s, 5 − 3.17 = 1.83 s longer than that minimum. In
general, the horizon must cover the
longest maneuver the planner considers.


.. _l8-lec-datasets:

Prediction Windows in Public Datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public datasets of recorded traffic, used to train and score predictors, set
two time windows: **observed**, how much past track the predictor reads, and
**predicted**, how far ahead it must predict.

.. figure:: /_static/images/L8/dataset_windows.png
   :alt: Four horizontal bars on a time axis from minus 6 to 8 seconds, with a dotted line at 0, now. For each row, a light gray bar to the left of 0 is the observed past and a dark bar to the right is the predicted future, each labeled with its length. Argoverse: 2 s and 3 s. Argoverse 2: 5 s and 6 s. Waymo Open Motion: 1 s and 8 s. This lecture: 2 s and 5 s.
   :width: 95%
   :align: center

   Each dataset's two windows on one time axis, with now at 0. Gray: the
   observed past; dark: the predicted future. Each bar is labeled with its
   length.

The table gives the same windows. They come from the papers of Argoverse,
Argoverse 2 and Waymo Open Motion. We read 2 s, as Argoverse does, and predict
5 s, enough for the 3.17 s stop.

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

Three Levels of Motion Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

A :ref:`learned predictor <l8-lec-learned>`, later in this lecture, can be
built at any of the three levels.


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

We take a junction with the AV and two cars, and simulate their motion.

**What it is for:** every predictor is compared on the same scene, against a
truth we know.

**Where the numbers come from.** The lanes are CARLA's: read from
``Town01.xodr`` with ``carla.Map``, with no CARLA server. The motion is
ours: simulated in Python on those lanes, so the truth is known exactly.
We chose every speed and every braking rate, and these notes say so.


.. _l8-lec-junction:

The Junction, from the Map
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/scene_map.png
   :alt: A top view of a T-junction from the map, x east from 98 to 214 meters, y north from minus 24 to 12 meters. A road runs east to west with one lane each way, a white dashed center line, and a side road leaving the junction to the south. The junction is shaded tan; the rest of the road is gray. Tag 1: the AV, a black car on the south lane at x 108, facing east. Tag A: car A, a green car on the north lane at x 174, facing west. Tag B: car B, a gray car on the north lane at x 201, facing west. A red cross in the junction at x 156, y minus 2, with no tag.
   :width: 95%
   :align: center

   A T-junction of Town01, from above, :math:`x` east and :math:`y` north in
   meters, all at :math:`t` = 0. The junction is shaded tan. **1:** the AV,
   on the south lane, facing east. **A:** car A and **B:** car B, on the north
   lane, facing west. The red cross: where car A's left turn would cross the
   AV's lane.

**1** is the AV, **A** car A and **B** car B, all at :math:`t` = 0, which
is now. :math:`t` is the time in seconds; a negative :math:`t` is the past.
The red cross is where car A's left turn would cross the AV's lane.

Measured on the map: the lanes are 4.0 m wide. Car A's left turn is about a
quarter circle, 23.07 m long. A quarter circle turns π/2 = 1.571 rad, and
length = radius × angle, so the radius is 23.07 / 1.571 = 14.7 m.


.. _l8-lec-truth:

The Truth We Simulated
~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/scene_truth.png
   :alt: The same top view, the junction shaded tan, with each road user's next 5 seconds drawn as a line with a dot every second, and the three cars faded at their positions now. The AV's black line runs east along its lane from x 107 to about 147, labeled 5 s at its end. Car A's green line runs west, then curves left through the junction into the side road, ending at x 154, y minus 7, labeled 5 s. Car B's gray line runs west along the north lane from x 201 to about 164, under car A's line where they overlap. Dark tags 1, A and B mark the AV, car A and car B; a red cross with no tag, in the junction at x 156, y minus 2, marks where car A's turn crosses the AV's lane.
   :width: 95%
   :align: center

   Where each road user really goes over the next 5 s, a dot every second;
   the junction is shaded tan.
   **1:** the AV, black, east along its lane. **A:** car A, green, west and
   then left into the side road. **B:** car B, gray, west along the north
   lane, under car A's line where they overlap. The red cross: where car A's turn
   crosses the AV's lane.

Each line is where a road user really goes over the next 5 s, with a dot
every second. We chose this motion; the AV does not know it.

- **1** The AV drives east at 8 m/s, straight on. It reaches the red cross
  at :math:`t` = 6.08 s.
- **A** Car A is slowing down for the junction. Two seconds ago
  (:math:`t` = −2 s) it drove at 8 m/s; since then it loses 1.0 m/s every
  second: 6.0 m/s now, 5.0 m/s one second from now. It turns left at
  5.0 m/s and is in the AV's lane from 3.4 to 4.3 s from now.
- **B** Car B follows car A, with 22.3 m between car A's rear and B's front, and
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
     - Where car A and B will go: no turn signal in our scene.
   * - The **map**: every lane, where it goes, how it bends.
     - Their speeds to come.
   * - Its own plan: 8 m/s, straight on.
     - How each driver decides when to brake, turn or go.

.. admonition:: You first
   :class: hint

   Will car A turn or go straight on? Which cue did you use? See
   :ref:`l8-lec-intent`.

.. important::

   **The question for the rest of the lecture:** from what the AV knows,
   predict car A's next 5 s, and say how sure that is. Car A is the hard one: it
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

.. dropdown:: Answers, from the simulation
   :class-container: sd-border-success

   - **Slowing:** car A brakes from :math:`t` = −2 s, the slider's start. Its
     dots, one every 0.1 s, are 0.80 m apart then, 0.70 m at −1 s, 0.60 m
     at 0 and 0.50 m from 1 s on, so the eye sees them close up slowly.
   - **Turning:** car A enters the junction at 1.2 s, but its heading starts to
     change only at 2.3 s. It is 0.5 m off its straight line at 2.8 s (ten
     times the track's 0.05 m noise) and 1 m off at 3.1 s, so by eye about
     2.5 to 3 s. The map-aware prediction already gives the left turn 0.87
     at :math:`t` = 0.


.. _l8-lec-physics:

Physics Models
--------------

We start with car A's track alone and the laws of motion. We try three
models, each with one more term than the last: constant velocity, constant
turn rate and velocity, and constant turn rate and acceleration.

**What it is for:** these are the simplest predictors, and every other
method is compared with them.

A physics model takes the road user's motion **now** (speed, heading, turn
rate: how fast the heading changes, braking) and assumes it does not change.


.. _l8-lec-fit:

Step 1: Read Car A's Motion from Its Track
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/track_fit.png
   :alt: Car A's speed in meters per second against time from minus 2 to 0 seconds. A black line, the true speed, falls straight from 8.0 to 6.0. A light blue band covers the last 1.5 seconds. A blue dashed line, the speed from the fit, runs inside the band just under the black line and ends at a blue dot at time 0, at 5.99 meters per second. The legend, bottom left, names the true speed (the AV does not know it), the speed from the fit, the band (the last 1.5 seconds of track, used for the fit) and the dot (the fit's speed now).
   :width: 60%
   :align: center

   Car A's speed against time, 0 = now. The legend names each line, the
   band and the dot.

Every physics model starts from car A's motion now, read from its track by
a **fit**: among all the paths a car with constant acceleration could
drive, the AV picks the one closest to the tracked positions (the smallest
total of squared distances: least squares). The AV keeps 2 s of track; the
fit uses only the newest 1.5 s, the blue band (16 positions; both chosen: a
shorter window follows a change in car A's motion sooner, a longer one averages
out more of the track's noise). The dashed line is the speed along the
fitted path.

.. note::

   **What the graph shows:** the fit's speed (dashed) stays on the true
   speed (black), which the AV cannot see. At :math:`t` = 0 the fit reads
   5.99 m/s against the true 6.01, and a braking of 0.96 m/s² against the
   true 1.0. (It also reads a heading 1.86° south of west, not shown.)

.. tip::

   See "Reading speed, heading, turn rate and braking from a track" in
   :doc:`Going Further <l8_appendix>` for the fit, written out.


.. _l8-lec-cv:

Step 2: Constant Velocity, by Hand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Constant velocity (CV)
   :class: note

   A physics model: the road user keeps the velocity it has now, the same
   speed and the same heading, for the whole horizon. Its predicted path is
   a straight line:

   .. math::

      x(h) = x_0 + v_x\,h, \qquad y(h) = y_0 + v_y\,h

   :math:`(x_0, y_0)`: its position now; :math:`(v_x, v_y)`: its velocity
   now; :math:`h`: the horizon, how far ahead in seconds.

At :math:`t` = 0, from one position and one velocity, the AV predicts car
A's position at 50 horizons at once: :math:`h` = 0.1, 0.2, …, 5.0 s. From
the fit (rounded): :math:`x_0` = 174.59 m, :math:`y_0` = 1.98 m;
:math:`v_x` = −5.985 m/s, :math:`v_y` = −0.194 m/s (west, a little south).

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - :math:`h` (s)
     - :math:`x` = 174.59 − 5.985 × :math:`h` (m)
     - :math:`y` = 1.98 − 0.194 × :math:`h` (m)
   * - 0.1
     - 173.99
     - 1.96
   * - 0.2
     - 173.39
     - 1.94
   * - …
     - …
     - …
   * - 1.0
     - 168.60
     - 1.79
   * - 3.0
     - 156.64
     - 1.40
   * - 5.0
     - 144.67
     - 1.01

0.1 s later, the AV does it again from the new track, and the new 50
replace these.

.. note::

   CV says that car A drives on west, past the junction, at 5.99 m/s. In
   truth, at :math:`h` = 5 s car A is at (154.08, −6.98) m: in the side
   road, after a left turn.


.. _l8-lec-cv-truth:

CV Against the Truth
~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/cv_vs_truth.png
   :alt: A close-up top view of the junction, x from 136 to 184 meters. Car A, green, at x 175 on the north lane, facing west. A black line, the truth, runs west and curves left into the side road with a dot every second, ending at y minus 7. A blue line, constant velocity, runs straight west along the north lane with a dot every second. Tags 1, 2 and 3 mark the blue dots at 1, 3 and 5 seconds; red dotted lines join each to the truth's dot at the same time: hidden under the dots at 1 second, short at 3 seconds, long at 5 seconds.
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

For the first 2 s the error stays at 1.5 m or less. Then car A turns, and each
second the error grows more: by 1.08, then 3.43, then 6.34 m. **For car A,
CV can be trusted for about 2 s, until car A turns; then it is far off.**
To see whether that holds for other road users, we test CV on
2476 predictions (:ref:`l8-lec-err-horizon`).


.. _l8-lec-ctrv:

CTRV: Constant Turn Rate and Velocity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CV cannot follow a road user that is turning or braking. CTRV adds a turn,
and CTRA, next, also a speed change. We test whether they predict better
than CV.

.. admonition:: Definition: Turn rate
   :class: note

   How fast a road user's heading changes, in radians per second. A car that
   drives straight has a turn rate of 0; a car driving at speed :math:`v` on
   a circle of radius :math:`r` has a turn rate of :math:`v / r`.

.. admonition:: Definition: Constant turn rate and velocity (CTRV)
   :class: note

   The road user keeps its speed :math:`v` and its turn rate :math:`\omega`,
   so it drives on a circle of radius :math:`v / \omega` (Schubert et al.,
   2008). From its position now :math:`(x_0, y_0)` and its heading now
   :math:`\theta_0` (radians, from east, counterclockwise), its position
   :math:`h` seconds ahead:

   .. math::

      x(h) = x_0 + \frac{v}{\omega}\big[\sin(\theta_0 + \omega h) - \sin\theta_0\big],
      \qquad
      y(h) = y_0 + \frac{v}{\omega}\big[\cos\theta_0 - \cos(\theta_0 + \omega h)\big]

- Car A, from Step 1's fit: 5.99 m/s and 0.049 rad/s, a radius of
  5.99 / 0.049 = 122 m. CTRV is 0.15 m from CV's straight line after 1 s,
  and 3.65 m after 5 s: almost a lane (4.0 m).
- That 0.049 rad/s is not a turn: car A drives straight now. Each tracked
  position is off by about 0.05 m at random, and the fit reads that small
  zigzag as a slight turn.
- Near :math:`\omega` = 0 the formula divides by almost 0, so the code
  switches to CV below 0.001 rad/s.


.. _l8-lec-ctra:

CTRA: CTRV with a Changing Speed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Constant turn rate and acceleration (CTRA)
   :class: note

   CTRV (turn rate :math:`\omega`, heading now :math:`\theta_0`, position
   now :math:`(x_0, y_0)`), with the speed changing at a constant rate
   :math:`a`: :math:`v(t) = v_0 + a t`, where :math:`v_0` is the speed now
   and :math:`t` the time from now (Schubert et al., 2008). The position
   :math:`h` seconds ahead is the velocity added up over time:

   .. math::

      x(h) = x_0 + \int_0^h (v_0 + a t)\cos(\theta_0 + \omega t)\,dt, \qquad
      y(h) = y_0 + \int_0^h (v_0 + a t)\sin(\theta_0 + \omega t)\,dt

- Schubert, Richter and Wanielik give these integrals in closed form
  (Schubert et al., 2008). Our code (``l8sim.py``) adds them up in steps of
  0.01 s instead.
- Car A, from Step 1's fit: braking at 0.96 m/s² from 5.99 m/s, it would
  stop after 5.99 / 0.96 = 6.2 s, past our 5 s horizon.
- A braking car's speed reaches 0 and would then go negative: the car would
  drive backward. The code holds the speed at 0 from then on.


.. _l8-lec-all-three:

CV, CTRV and CTRA from t = 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are three separate predictions from the same fit at :math:`t` = 0,
made only to compare the models. An AV runs the one it keeps, every 0.1 s;
the test set decides which.

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

CTRA uses car A's braking, so its car A slows down and stays closer to the junction.
None of the three predicts the turn: at :math:`t` = 0, car A has not started
it.


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
(dotted). **So: CTRV beats CV only once a turn is under way, for about a
second** (3.06 m off at 2 s).


.. _l8-lec-err-horizon:

Error Against Horizon, on 2476 Predictions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/err_horizon.png
   :alt: Two panels of mean error in meters against horizon from 0 to 5 seconds, each with a legend at the top left (CV, CTRV, CTRA, truth with error 0), a black line at 0 meters for the truth, and a gray dotted line at 2 meters. Left, no turn in the next 5 s, 1381 predictions: blue CV rises slowly to 3.6 meters at 5 seconds; purple dashed CTRV to 10.1; dark gold dash-dotted CTRA to 15.2. Right, a turn in the next 5 s, 1095 predictions: all three rise steeply and close together, CV to 20.8, CTRV to 19.1, CTRA to 18.3 meters.
   :width: 95%
   :align: center

   Mean error against horizon on our test set. Each prediction is scored
   against its own car's truth, so the truth is the black line at 0; the
   gray dotted line is 2 m, the miss threshold.

**Our test set:** every way through the junction, at 6 to 10 m/s, with
random braking and turn speeds (chosen); one prediction every 0.5 s of each
drive, each scored against the true path of its own car, not car A's. We
split the predictions afterwards, from the truth: a turn means the car's true
heading changes by more than 20° in the next 5 s. The models never see that
split.

- **Left, no turn in the next 5 s (1381 predictions):** CV stays closest to
  the truth, under 2 m up to 3.5 s (0.49, 1.65 and 3.64 m at 1, 3 and 5 s).
  CTRV and CTRA pass 2 m at 2.1 and 1.7 s: their extra terms hurt.
- **Right, a turn in the next 5 s (1095 predictions):** all three pass 2 m by
  1.4 s (CV at 1.3 s) and end 18 to 21 m off: none sees the turn coming.

.. tip::

   See "How the test set is built" in :doc:`Going Further <l8_appendix>`.


.. _l8-lec-why-grows:

Why the Error Grows, and Why More Terms Do Not Help
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Any error in the speed grows with time.** 0.1 m/s off is 0.5 m after
   5 s. A speed that changes (a driver slowing for no reason we can see)
   adds more.
2. **A physics model has no term for a maneuver that has not started.**
   Before the turn, car A's turn rate is 0. Only a predictor that knows the
   junction can read car A's braking as a turn. With a turn ahead, all three
   models are 18 to 21 m off at 5 s.
3. **Each extra term is kept for all 5 s.** A turn rate or a braking rate
   read from the track often belongs to a turn that is ending or a slow-down
   about to stop, yet CTRV and CTRA keep it to the end. With no turn ahead,
   their errors at 5 s are 10.1 and 15.2 m, against CV's 3.6 m.

.. note::

   With a turn ahead, every model's mean error passes 2 m by 1.4 s. To do
   better, a predictor must know **which ways the road user can go**: the
   map's lanes.


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
   3. Where is CTRA worst: while car A brakes, or while it speeds up after the
      turn?


.. _l8-lec-scoring:

Scoring
-------

The physics models gave an error at each second, and the best model depends
on the second: for car A, CV beats CTRV at 3 s (2.58 against 2.65 m), and
CTRV beats CV at 5 s (10.00 against 12.35 m). We now score a whole
prediction with one number (ADE, FDE), call it a hit or a miss, and check
the uncertainty it reports.

**What it is for:** with scores we compare predictors and tell when a prediction's own uncertainty can be trusted.

A prediction is scored by how far its positions are from the truth. The
public benchmarks use two such scores, ADE and FDE, and count a miss when the
last position is too far off. The truth is known only after the 5 s have
passed, so the AV never computes these scores while it drives. We compute
them afterwards, on drives whose truth we know, to compare predictors and to
decide which one the AV can trust, and for how long. A paper's benchmark
defines the scores and ranks predictors on the paper's data. It cannot tell
us how a predictor does on our roads. So we compute the same scores on our
own test set, 2476 predictions from our simulated drives. The verdict on CV,
under 2 m up to 3.5 s with no turn, came from these scores.

.. figure:: /_static/images/L8/score_loops.png
   :alt: Two boxed rows joined by arrows. Top row, on the car, while it drives (every 0.1 seconds): sensors, tracker (L5), predictor: next 5 seconds (highlighted), planner (L9), control (L10), each feeding the next; under them: used once, replaced 0.1 seconds later: no truth yet, no score. An arrow labeled recorded goes down to the bottom row, afterwards, off the car (once the truth is known): each prediction, and the truth; then scores: ADE, FDE, minADE, minFDE, misses; then decide: which predictor, how far ahead to trust it. A magenta arrow labeled next software version goes from the decision back up to the car.
   :width: 95%
   :align: center

   When the scores are computed. On the car, each prediction is used once
   and replaced 0.1 s later, before its truth exists, so it is never scored
   there. Afterwards, off the car, each prediction is compared with the
   truth. The scores decide which predictor the next software version
   uses, and how far ahead to trust it.


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
   In words: at each predicted time, measure how far the prediction is from
   the truth; add the :math:`N` distances and divide by :math:`N`.

**The idea:** one number for the whole predicted path. At every predicted
time, the planner checks the AV's planned position against the road user's
predicted position, so an error at any of those times matters.

Car A's CV prediction, with only the five whole seconds (:math:`N` = 5):

1. The errors at 1 to 5 s: 0.52, 1.50, 2.58, 6.01 and 12.35 m.
2. ADE: (0.52 + 1.50 + 2.58 + 6.01 + 12.35) / 5 = 22.96 / 5 = 4.59 m.

In words: over those five times, CV put car A 4.59 m from where it really
was, on average: more than a lane width (4.0 m).

**ADE depends on N.** With all 50 predicted times (every 0.1 s,
:math:`N` = 50), the same prediction's ADE is 3.37 m, not 4.59 m. Why lower:
in the last second, the error climbs from 6.54 m (at 4.1 s) to 12.35 m (at
5.0 s). :math:`N` = 5 counts only the 12.35; :math:`N` = 50 counts all ten,
which average 9.30 m. The same happens in every second. So two ADEs
compare only with the same :math:`N` and the same horizon. From now on,
:math:`N` = 50.


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

**The idea:** where the road user ends up, at the end of the horizon, where
the error is largest. The miss, next, is built on it.

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

We take Argoverse 2's threshold, 2.0 m: for one prediction, a **miss** means
its FDE is above 2.0 m, and a **hit** means 2.0 m or less. Only the FDE
decides; the ADE plays no part.

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
- "No turn" means no turn within the next 5 s. There CV is the best of the
  three, and still misses 35.9% of the time. Most misses come from cars that
  turn earlier or later on their route, braking before the turn or speeding
  up after it: CV misses 76.3% of those 625 predictions, and 2.5% of the 756
  on straight routes.


.. _l8-lec-cv-region:

CV's 95% Region
~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/cv_region.png
   :alt: The close-up of the junction with car A at x 175. The blue CV line runs west with a dot every second; around each dot a light blue circle, the 95 percent region, small at 1 second and larger every second, the one at 5 seconds about 16 meters across. The black truth curves left into the side road: its dots at 1, 2 and 3 seconds lie inside the circles of the same time; its dots at 4 and 5 seconds lie outside.
   :width: 70%
   :align: center

   CV's prediction for car A, blue, with its 95% region around each
   one-second dot: the light blue circles. Each dot is labeled with its time,
   1 s to 5 s, on CV's line and on the truth. Black: the truth. Its dots at 1,
   2 and 3 s are inside the circle of the same time; at 4 and 5 s they are
   outside.

Each light blue circle is CV's answer to "how sure?": at that time, CV
expects car A inside it 95 times out of 100. **For car A:** the truth is
inside the circle at 1, 2 and 3 s, outside at 4 and 5 s. Car A turns, and CV's
circles do not.

**How one circle is computed**, the one at :math:`h` = 3 s. :math:`\sigma`:
how spread the predicted position is, along each axis. :math:`q` = 0.5 ×
0.5 = 0.25 m²/s³: the speed wanders by 0.5 m/s per
:math:`\sqrt{\text{s}}` (chosen).

.. list-table::
   :widths: 40 35 25
   :header-rows: 1
   :class: compact-table

   * - **Step**
     - **Computation**
     - **Value**
   * - 1. Center: CV's position at 3 s
     - from Step 2
     - (156.64, 1.40) m
   * - 2. :math:`\sigma^2` from the wandering speed
     - :math:`q h^3 / 3` = 0.25 × 27 / 3
     - 2.25 m²
   * - 3. :math:`\sigma^2` from the fit's own errors
     - from the 0.05 m track errors
     - 0.0105 m²
   * - 4. :math:`\sigma`
     - :math:`\sqrt{2.25 + 0.0105}`
     - 1.50 m
   * - 5. Radius
     - 2.45 × 1.50
     - 3.68 m

**Why the circles grow.** CV assumes car A keeps its speed, while real
drivers speed up and slow down a little. We let the speed wander at random
(chosen): by about 0.5 m/s after 1 s, and 1.0 m/s after 4 s. The further
ahead, the more it can have wandered, so the wider the circle. (The error in
the fitted velocity adds under 3% of :math:`\sigma^2` from 1 s on.)
:math:`\sigma` is how spread the predicted position is, along each axis; the
circle's radius is 2.45 × :math:`\sigma` (2.45 = :math:`\sqrt{5.99}`,
rounded; the appendix says why).

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

The dotted line is what the region promises. Both lines stay below it:
CV's region holds the truth less often than it says.

- With **no turn** (solid line), the region holds the truth a little less
  than 95% of the time at every horizon. The line mixes two kinds of road:
  on straight roads the region is too wide, and on roads before a turn it is
  too narrow.
- With **a turn** (dashed line), it holds the truth far less often, and less
  the further ahead CV predicts, because CV's region cannot follow a turn.

The numbers, at 1, 3 and 5 s:

- no turn: 81.5, 85.6 and 82.6%. That average mixes two groups:
  straight routes, 100% (too wide); turning routes before the turn, 59 to
  68% (too narrow);
- a turn: 46.5, 20.4 and 7.2%: far too narrow.

Chance alone moves each number by about 2 points (counted by drive). CV's
region has no term for a turn or a speed change.

.. note::

   So CV's region is too sure, most of all near a turn, where a planner that
   trusted it would keep too little distance. Check a region for straight
   driving and for turns, separately.


.. _l8-lec-scoring-summary:

Physics Models, Scored
~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Summary: physics models, scored
   :class: tip

   - **Car A, from t = 0:** CV's FDE 12.35 m, CTRV's 10.00 m, CTRA's
     7.26 m: three misses. Car A had not started its turn.
   - **The test set:** with no turn, CV's mean error stays under 2 m up to
     3.5 s (1.65 m at 3 s), the best of the three. With a turn ahead, CV
     passes 2 m at 1.3 s, and all three miss at 5 s almost every time (98.3
     to 99.5%).
   - **CTRV and CTRA:** better than CV only once a turn or a braking is
     under way, for about a second; with no turn ahead, worse (FDE 10.1 and
     15.2 against 3.6 m).
   - **Uncertainty:** CV's 95% region held the truth 82 to 86% of the time
     with no turn, 7.2% at 5 s with one.
   - **So:** trust CV only for short horizons with no maneuver ahead. Near
     a junction, the AV keeps CV as one mode and as the fallback, never as
     its only prediction: it needs **several futures**.


.. _l8-lec-futures:

Several Futures
---------------

One predicted future is wrong whenever the car turns and the model does
not. So a prediction now gives several futures for each road user, each with
a probability, and we learn to score them. The futures come from the map:
one per lane the road user can take through the junction. The next section,
Using the Map, shows how we build them.

**What it is for:** the planner can then know that car A may turn, before car A
turns.


.. _l8-lec-two-things:

Car A Can Do Two Things
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/two_futures.png
   :alt: The close-up of the junction with car A at x 175 facing west. Two magenta predicted lines leave it, each with a dot every second: a thick solid one curving left into the side road, labeled left turn, p = 0.87, and a dashed one running straight west, labeled straight on, p = 0.13.
   :width: 70%
   :align: center

   Car A's two predicted futures, a dot every second. Thick magenta: the left
   turn, probability 0.87. Dashed magenta: straight on, probability 0.13.

The map shows that car A's lane splits at the junction: **straight on** to the
west, or **left** into the side road. No road leaves the junction to car A's
right. Each predicted future follows one of these lanes.

Each future has a probability, 0.87 or 0.13. The next section
(:ref:`l8-lec-map`) shows how we built the futures and their probabilities
from the map and car A's speed; here, what to do with them.


.. _l8-lec-average:

The Average of Two Futures Is Not a Future
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/mean_of_modes.png
   :alt: The close-up of the junction with car A at x 175. Tag 1: the end of the magenta left-turn line in the side road. Tag 2: the end of the magenta dashed straight line, far west on car A's lane. Tag 3: a red dot at the end of a red dotted line between them; the line starts along car A's lane and bends south-west across the junction toward its south-west corner.
   :width: 70%
   :align: center

   **1:** the left turn. **2:** straight on. **3:** their average, point by
   point: the red dotted line, ending at the red dot.

At 5 s, point **3** is 7.21 m from each future, inside the AV's own lane,
facing against its traffic. No driver in car A's lane ends up there.

Its FDE against the truth is 5.92 m, a miss, while the left-turn future
alone is off by 1.88 m.

.. note::

   If half the drivers in car A's place turn and half go straight on, a
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
truth (hit or miss by its FDE alone, see :ref:`l8-lec-miss`):

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

The section Using the Map computes 0.87 and 0.13 from the map and car A's speed
(:ref:`l8-lec-step4-bayes`).

With several futures, which one do we score? The benchmark scores keep the
best mode; a separate check scores the probabilities. Like ADE and FDE, both
are computed afterwards, from the truth. While it drives, the planner uses
the modes and their probabilities.


.. _l8-lec-minade:

minADE and minFDE
~~~~~~~~~~~~~~~~~

.. admonition:: Definition: minADE and minFDE
   :class: note

   With several modes, Argoverse 2 scores only the best one: the mode that
   ends closest to the truth (Wilson et al., 2021). minFDE is that mode's
   FDE; minADE is the same mode's ADE.

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

minFDE scores only the mode that ends closest to the truth. So a predictor
can lower its minFDE just by giving more modes.

1. An example (made up): car A can take two lanes, left or straight on. A
   predictor gives each lane three speeds, slow, steady and fast: six modes,
   each with probability 1/6. Whatever car A does, one mode ends near the truth,
   so minFDE is small.
2. The planner would gain little. The three left-turn modes would put car A in
   the AV's lane at three different times, so the AV would have to keep the
   crossing clear at all three (next section).
3. A score that uses the probabilities catches this: Waymo's dataset ranks
   the modes by confidence and computes a mean average precision (mAP)
   (Ettinger et al., 2021).
4. Our simpler check: the probability a predictor gives to the true future.
   For car A, ours gives 0.87; the six-mode predictor, 1/6 = 0.17. Whether
   such probabilities come true as often as they say, we check on the test
   set (:ref:`l8-lec-calibration`).


.. _l8-lec-three-left:

More Modes Block the Crossing Longer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The made-up example: three left-turn modes, slow, steady and fast through the
turn. The steady one is the lecture's mode. Turn speeds chosen for this
example: 3.83, 5.42 and 6.06 m/s.

.. figure:: /_static/images/L8/three_left_timeline.png
   :alt: Four gray time lines, one per row, against time from now, 0 to 8 seconds. Row tag 1: a magenta bar from 4.2 to 5.0 seconds. Row tag 2: a magenta bar from 3.2 to 4.0 seconds. Row tag 3: a magenta bar from 3.0 to 3.7 seconds. Row tag 4: a black diamond at 6.08 seconds, with a dotted vertical line up through the rows. Tag 5: a two-headed arrow above the rows from 3.0 to 5.0 seconds, between two dotted lines. Tag 6: a two-headed arrow on row 1 from 5.0 seconds to the dotted line at 6.08 seconds.
   :width: 80%
   :align: center

   Each row is a time line; a bar shows when that mode would put car A in
   the AV's lane. **1:** slow, 4.2 to 5.0 s. **2:** steady, the lecture's
   mode, 3.2 to 4.0 s. **3:** fast, 3.0 to 3.7 s. **4:** the AV, at 8 m/s
   straight on, reaches the crossing at 6.08 s. **5:** the time the
   crossing is blocked by the three modes. **6:** the time from the slow
   mode's exit to the AV's arrival.

1. One left-turn mode keeps the crossing blocked for 4.0 − 3.2 = 0.8 s.
2. Three keep it blocked from the first one in to the last one out (**5**):
   5.0 − 3.0 = 2.0 s, 2.5 times as long (2.0 / 0.8). A plan that reached the
   crossing in that time would have to slow down.
3. Our AV still arrives after car A has left the lane in every mode, but only
   6.08 − 5.0 = 1.08 s after the slow one (**6**), against 2.08 s with one
   mode. More modes cost the planner time, and minFDE never shows that cost.


.. _l8-lec-planner-two:

What the Planner Does with Two Futures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AV's own plan is 8 m/s, straight on.

.. figure:: /_static/images/L8/lane_timeline.png
   :alt: Four gray time lines, one per row, against time from now, 0 to 8 seconds. Row tag 1: a magenta bar from 3.2 to 4.0 seconds. Row tag 2: empty. Row tag 3: a green bar from 3.4 to 4.3 seconds. Row tag 4: a black diamond at 6.08 seconds, with a dotted vertical line up through all rows. Tag 5: a two-headed arrow on row 1 from the end of the magenta bar, 4.0 seconds, to the dotted line.
   :width: 95%
   :align: center

   Each row is a time line, against the time from now. A bar shows when
   car A is in the AV's lane. **1:** the left-turn mode (probability 0.87),
   the magenta bar: 3.2 to 4.0 s. **2:** the straight-on mode (0.13): car A
   stays in its own lane, so the row has no bar. **3:** the truth, what car A
   did, the green bar: 3.4 to 4.3 s. **4:** the AV, at
   8 m/s straight on, reaches the point where car A's turn crosses its lane at
   6.08 s. **5:** the AV arrives 6.08 − 4.0 = 2.08 s after car A leaves its
   lane.

1. For each mode, find when it puts car A in the AV's lane, and note its
   probability: 0.87 for the left turn, the one that crosses.
2. Plan so that the AV is not at the crossing while a likely mode is: it
   arrives 2.08 s after the left-turn mode has car A leave the lane (**5**), so
   it keeps its speed. In the truth, car A leaves at 4.3 s, so the AV gets
   there 6.08 − 4.3 = 1.78 s after car A has gone. A plan that reached the crossing near :math:`t` = 4 s would
   have to slow down.

.. note::

   How far to stay from each mode is the planner's job (L9). The
   prediction's job: every likely future, with its times and its
   probability.


.. _l8-lec-futures-summary:

Several Futures, Scored
~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Summary: several futures, scored
   :class: tip

   - **What we did:** car A can turn left or go straight on, and one future
     cannot cover both: their average is a place no driver goes. So the
     predictor gives several modes, each with a probability: left 0.87,
     straight on 0.13.
   - **How we scored them:** minADE and minFDE keep the mode that ends
     closest to the truth (left, 1.88 m: a hit). They ignore the
     probabilities, and more modes always lower them, so we also check the
     probability given to the true future.
   - **What the planner does:** it keeps the AV off the crossing while a
     likely mode has car A there.
   - **Why it is not enough:** we were handed the two modes and their
     probabilities. A predictor must build them from what the AV sees.
   - **What is missing:** where do the modes, and 0.87 and 0.13, come from?
     Next, :ref:`l8-lec-map`: each lane car A can take becomes a mode, and
     Bayes' rule turns car A's speed into the probabilities.


.. _l8-lec-map:

Using the Map
-------------

A car drives where the map has lanes. So each lane car A can take gives one
future, and Bayes' rule, applied to car A's track, gives each future its
probability.

**What it is for:** the predictor then knows that car A can turn, and how
likely the turn is.

Lefèvre calls this maneuver-based: the driver picks a maneuver (a
lane through the junction), and the motion follows it (Lefèvre et al.,
2014).


.. _l8-lec-candidates:

The Map's Lanes Are the Candidate Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Where a lane splits, each branch is a possible future path: one mode.
- The map lists every way through the junction: six, two from each arm. Car A's arm has two: **straight on** (23.12 m inside the
  junction) and **left** (23.07 m, radius 14.7 m).

.. _l8-lec-plan:

The Plan for Car A, in Four Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/lane_plan.png
   :alt: A flowchart. A gray box, car A's track and the map's lanes, has an arrow into Step 1, put car A on each candidate lane; an arrow to Step 2, the speed each path expects here; an arrow down to Step 3, how well each path explains car A's speed; an arrow left to Step 4, Bayes' rule; a magenta arrow left to a magenta box, one probability for each lane.
   :width: 90%
   :align: center

   From car A's track and the map's lanes to one probability for each lane.
   **Step 1:** put car A on each candidate lane. **Step 2:** the speed each path
   expects here. **Step 3:** how well each path explains car A's speed.
   **Step 4:** Bayes' rule.


.. _l8-lec-step1-lane:

Step 1: Put Car A on Each Candidate Lane
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each candidate lane, we find the lane point nearest car A's fitted
position (**1** in the figure).

.. figure:: /_static/images/L8/step1_lanes.png
   :alt: Top view of the junction to scale, x east from 148 to 184 meters, y north from minus 16 to 7 meters. Car A, green, faces west in the north lane at x 175. One magenta line runs west from a dot at car A's rear axle, tag 1, through a black square at x 168, tag 2, and splits a few meters later: a solid line curves left into the side road, tag 4, and a dashed line continues west, tag 5. Tag 3: a two-headed arrow above the road from the square to the dot. The junction, from x 168 meters west and into the side road, is shaded tan; the rest of the road is gray.
   :width: 80%
   :align: center

   Car A on its candidate lanes, from above, to scale. **1:** the lane
   point nearest car A's fitted position. **2:** the junction's entry. **3:**
   the distance along the lane between them. **4:** the left-turn lane.
   **5:** the straight-on lane. Up to the junction the two lanes share one
   line. The junction is shaded tan.

1. **Distance to the junction** (**2**) along the lane (**3**): **6.51** m,
   the same for the left-turn lane (**4**) and the straight-on lane
   (**5**): they share car A's road up to the junction.
2. **Offset** from the lane's center: 0.07 m.
3. **Heading** against the lane's: 1.86° apart.

Offset and heading are too small to see at this scale.

.. note::

   Before the junction, the two lanes share one line, so car A's offset and
   heading are the same for both. Car A's **speed** can tell them apart: a
   driver who will turn must slow down before the junction, and one going
   straight keeps the street's speed (Step 2). Once car A starts turning, its
   heading leaves the straight lane's too.


.. _l8-lec-step2-speed:

Step 2: The Speed Each of Car A's Paths Expects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At car A's spot, 6.51 m before the junction, how fast would a driver on each of
car A's two paths go?

**Straight on:** the street's speed, 8 m/s (chosen: the speed our cars
cruise at). **Left:** slow enough for the turn.

1. Turn speed. A car at speed :math:`v` in a turn of radius :math:`R` has
   a sideways acceleration :math:`a = v^2/R`, so :math:`v = \sqrt{a \times
   R}`. With :math:`a` = 2.0 m/s² (chosen) and the turn's :math:`R` =
   14.7 m: :math:`v = \sqrt{2.0 \times 14.7} = \sqrt{29.4}` = 5.42 m/s.
2. A driver who brakes at 1.0 m/s² (chosen) and reaches 5.42 m/s at the
   junction, 6.51 m away, drives now at
   :math:`\sqrt{\text{turn speed}^2 + 2 \times \text{braking} \times
   \text{distance}} = \sqrt{5.42^2 + 2 \times 1.0 \times 6.51} =
   \sqrt{42.4}` = 6.51 m/s. The speed has the same digits as the distance,
   by chance.
3. So straight on expects **8.00** m/s here, and left expects **6.51** m/s.
   Car A drives at **5.99** m/s.

.. note::

   The expected speed is only for scoring. Each mode's predicted future
   starts from car A's own 5.99 m/s: straight on keeps it; left brakes evenly to
   5.42 m/s by the junction (at 0.50 m/s²), holds it through the turn, then
   speeds up.


.. _l8-lec-step2-graph:

Step 2, as a Graph: Car A's Speed Against Each Path's
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a graph, not a picture of the road: it plots each path's expected
speed against the distance to the junction. Read it left to right, as car A
drives toward the junction.

.. figure:: /_static/images/L8/speed_expect.png
   :alt: A graph of speed in meters per second, 4.6 to 8.6, against distance to the junction in meters, from 25 on the left down to 0 on the right, so the junction is at the right edge. A gray dashed line at 5.42 meters per second, marked on the speed axis, runs across to where the solid curve ends at the junction. A dashed magenta line at 8 meters per second runs across. A solid magenta curve runs flat at 8 from 25 meters to about 17.3 meters, then falls to 5.42 at 0 meters. A green dot at 6.51 meters and 5.99 meters per second, just below the curve. A short solid segment from the dot up to the curve, tag 1; a dotted segment from the dot level up to the dashed line, tag 2. A gray dotted vertical line at 17.3 meters, tag 3.
   :width: 95%
   :align: center

   The speed each path expects against the distance to the junction. Solid
   magenta: left; dashed magenta: straight on; gray dashed: 5.42 m/s, the
   speed left expects at the junction. Green dot: car A, 5.99 m/s at 6.51 m. **1:** how much slower car A is than left expects. **2:** how much
   slower car A is than straight on expects. **3:** 17.3 m from the junction,
   where left's curve reaches 8 m/s.

**1** Left: car A drives 6.51 − 5.99 = 0.52 m/s slower than this path expects.
**2** Straight on: car A drives 8.00 − 5.99 = 2.01 m/s slower than this path
expects. **3** 17.3 m is the distance a driver needs to slow from 8 to 5.42 m/s at
1.0 m/s²: (8² − 5.42²) / (2 × 1.0) = 17.3 m from the junction. Farther than that,
both paths expect 8 m/s, so speed cannot tell them apart.


.. _l8-lec-step3-likelihood:

Step 3: A Bell Curve Scores Each Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`\Delta v` is car A's speed now, measured from its track (5.99 m/s),
minus the speed a path expects at car A's spot (Step 2). It uses neither the
prediction nor the truth: only what the AV measures at :math:`t` = 0.

.. admonition:: Definition: Likelihood
   :class: note

   A score from 0 to 1 for how well a path explains what the AV measures:
   if car A were taking this path, how believable is its speed? It is not yet
   the probability of the path; Step 4 turns the scores into
   probabilities.

.. figure:: /_static/images/L8/bell_curve.png
   :alt: A bell curve of likelihood, 0 to 1, against delta v, car A's speed minus the path's expected speed, from minus 3.5 to 3.5 meters per second. The curve peaks at 1 at delta v equals 0, marked by a dotted vertical line. Two magenta dots on the curve, each with a magenta dashed line down to the delta v axis, where its value is marked: tag 1 at minus 0.52, likelihood about 0.87; tag 2 at minus 2.01, likelihood about 0.13.
   :width: 80%
   :align: center

   The likelihood against :math:`\Delta v`. **1:** left, a gap of
   −0.52 m/s. **2:** straight on, a gap of −2.01 m/s.

The curve is highest at a gap of 0: a driver going exactly as the path
expects scores 1. The farther the gap from 0, too slow or too fast, the
lower the score. Left (**1**) has a small gap (:math:`\Delta v` = 5.99 − 6.51 = −0.52 m/s),
so it scores high; straight on (**2**) has a large gap (:math:`\Delta v` =
5.99 − 8.00 = −2.01 m/s), so it scores low. These are scores, not
probabilities yet. The numbers:

**1** Left: :math:`\Delta v` = 5.988 − 6.512 = −0.524 m/s, likelihood
0.872. **2** Straight on: :math:`\Delta v` = 5.988 − 8.000 = −2.012 m/s,
likelihood 0.132.


.. _l8-lec-step3-words:

Step 3: The Bell Curve's Formula, in Words
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The curve is :math:`e^{-\frac12 (\Delta v / \sigma)^2}`, with
:math:`\sigma` = 1.0 m/s (chosen: drivers differ by about that much). Read
it from the inside out:

1. :math:`\Delta v / \sigma`: how far car A's speed is from the path's, counted
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

A path's **prior** is its probability before we use any measurement of car
A. We have no data on how often drivers turn left here, so we chose 0.5 for
each of the two paths. Bayes' rule: multiply each prior by the path's
likelihood, then divide by the sum, so the probabilities add up to 1.

1. Left: 0.5 × 0.872 = 0.436. Straight on: 0.5 × 0.132 = 0.066.
2. Sum: 0.436 + 0.066 = 0.502.
3. P(left) = 0.436 / 0.502 = **0.87**; P(straight on) = 0.066 / 0.502 =
   **0.13**: the probabilities we gave the two modes
   (:ref:`l8-lec-two-things`).

.. note::

   The two 0.5 priors cancel: with equal priors, the probabilities are the
   likelihoods divided by their sum, 0.872 / (0.872 + 0.132) = 0.87. That
   sum, 1.004, is close to 1 by chance, so the probabilities show the same
   digits as the likelihoods. A prior from data (how often drivers turn
   left here) would change them.

In papers this is written P(maneuver | track, map): here the maneuver is
the lane path, the track gives car A's speed, and the map gives each path's
expected speed.

.. tip::

   See "All three scores, written out" and "P(left) as car A approaches" in
   :doc:`Going Further <l8_appendix>`.


.. _l8-lec-results:

Results
~~~~~~~

How good is the map-aware predictor?

.. admonition:: Summary: results
   :class: tip

   The predictor's most likely mode usually follows car A's correct lane,
   but often at the wrong speed, so it can still miss. With no turn ahead,
   CV does better, so the AV keeps a CV mode next to the lane modes. Our
   test set is too small to say whether the probabilities are too sure. The
   predictor also fails when a driver does not follow the rule, leaves the
   lanes, or the map is out of date.

The numbers:

- **Car A:** the left mode picks the correct lane and ends 1.88 m from the
  truth, a hit (CV: 12.35 m).
- **Test set, turn ahead:** the true path is the most likely mode 84% of the
  time, but that mode still misses half the time: the correct lane at the
  wrong speed.
- **Test set, no turn ahead:** CV does better, so the AV keeps a CV mode next
  to the lane modes.
- **Probabilities:** modes given 0.81 came true 0.73 of the time; our test
  set is too small to say whether that gap is more than chance.
- It also goes wrong when a driver does not follow the rule, leaves the
  lanes, or the map is out of date.

.. note::

   The details are reading material in :doc:`Going Further <l8_appendix>`:
   :ref:`l8-lec-map-truth`, :ref:`l8-lec-map-test`,
   :ref:`l8-lec-calibration` and :ref:`l8-lec-map-wrong`. Hands-on part 3 is
   there too: :ref:`l8-lec-handson-modes`.


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
   :alt: A block diagram. Three gray input boxes on the left: 1. every road user's last few seconds of track; 2. the map's lanes, as polylines (lists of points); 3. traffic lights, the road user's type (car, cyclist). Each has an arrow into a central box: a neural network, weights set by training. Two magenta arrows lead out to two magenta boxes: K future tracks for each road user, and one probability for each of them.
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
       works like a candidate lane: a probability, a shift, a
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

   CV is the common baseline for learned models and the fallback when
   nothing else fits: with no turn ahead, its mean error stays under 2 m up
   to 3.5 s; with a turn ahead, it passes 2 m at 1.3 s.


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


.. _l8-lec-disc-learned:

Discussion: A Learned Predictor on Our Streets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Discussion
   :class: hint

   A learned predictor beats CV on a benchmark's test scenes. **What could
   still make it worse than CV on our streets? How would you find out before
   it drives?** Three minutes with your neighbors.

.. dropdown:: What to listen for
   :color: success
   :icon: check-circle

   - **Other data.** The benchmark was recorded in other cities, with other
     road layouts and other drivers. A scene that is rare in training is
     predicted badly: Tempe's ADS had no goal for a person crossing away from a
     crosswalk.
   - **Averages hide rare cases.** A better minADE over many test scenes can
     come with worse errors on the few scenes that matter. Score turns,
     pedestrians and cyclists on their own.
   - **minADE keeps only the best of the modes.** The planner uses every mode
     and its probability, so check calibration too.
   - **Wrong inputs give wrong futures:** a broken track, or a map that is out
     of date.
   - **How to find out:** score it on drives recorded on our own streets, scene
     by scene, against CV, and keep CV as the fallback.


.. _l8-lec-drivers:

Other Drivers
-------------

Until now we predicted each road user alone. But drivers react to each
other: car B to car A, and car A to the AV.

**What it is for:** B's prediction then uses car A's, car A's uses the AV's plan,
and the AV knows that its own motion changes what others do.

.. admonition:: Definition: Behavior model
   :class: note

   A model of how a road user decides what to do and reacts to others: what
   it means to do next, how it follows the car ahead, and when it accepts a
   gap. This section is the behavior modeling of the lecture's title;
   Lefèvre calls it interaction-aware (Lefèvre et al., 2014).

At the end, the AV's own behavior layer uses these predictions to choose
what the AV does.


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
       <l8-lec-step4-bayes>` got P(left) = 0.87 from car A's speed alone.
   * - Position in the lane
     - A car drifting toward a lane boundary may change lanes (Autoware
       Foundation, map-based prediction).
   * - Turn signal
     - A camera can read it, but drivers forget it, or leave it on.
   * - Where the lane goes
     - Only some maneuvers are possible: no road leaves the junction to
       car A's right.


.. _l8-lec-idm-summary:

Following: the IDM
~~~~~~~~~~~~~~~~~~

.. admonition:: Summary: following, the IDM
   :class: tip

   Car B drives behind car A, so B's future depends on car A's. The
   Intelligent Driver Model (IDM) is a rule for a driver who follows another
   car: speed up toward the speed you like when the road ahead is clear, and
   slow down when the gap to the car ahead gets smaller than a safe gap. The
   safe gap grows with your speed and with how fast you close in. So to
   predict B, the AV first predicts car A, then lets B follow car A's
   predicted future with the IDM. That is much closer to B's true motion
   than CV, which ignores car A: CV ends 3.55 m off at 5 s, the IDM 0.92 m.

The formula, its parameters and a worked example are reading material in
:doc:`Going Further <l8_appendix>`: :ref:`l8-lec-b-slows`, :ref:`l8-lec-idm`,
:ref:`l8-lec-idm-gap` and :ref:`l8-lec-idm-hand`.


.. _l8-lec-gap:

Car A Waits for a Gap in the AV's Lane
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Car A turns left across oncoming traffic, so it must give way to the AV.

.. admonition:: Definition: Critical headway (gap acceptance)
   :class: note

   The shortest gap, in seconds, that a driver accepts to make a maneuver
   across traffic. The Highway Capacity Manual's base value for a left turn
   from the major street of a two-lane road, at a junction with stop signs
   on the side street: **4.1 s**, as reproduced in the McTrans Center's
   users guide (McTrans Center, HCS Two-Way Stop Controlled Intersections
   Users Guide). We use it for car A (chosen).

**In other words:** car A turns only if the AV is at least 4.1 s away from
the point where car A's turn crosses its lane. At the AV's 8 m/s, that is
4.1 × 8 = 32.8 m. If the AV is closer, car A waits for it to pass.

.. _l8-lec-run1:

Run #1: The AV Is 48 m Away When Car A Decides
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/run1_gap.png
   :alt: Top view of the junction to scale, x east from 100 to 182 meters, at the moment car A decides. The AV, black, on the south lane at x 108, facing east. Car A, green, on the north lane at x 174, facing west. A red cross at x 156 where car A's turn crosses the AV's lane. Tag 1: a two-headed arrow below the road from the AV to the red cross. Tag 2: a two-headed arrow above the road from car A to the junction's entry at x 168. Tag 3: a dashed mark across the AV's lane at x 123.
   :width: 95%
   :align: center

   Run #1 at the moment car A decides, from above, to scale; the junction is
   shaded tan. **1:** the AV
   to the red cross, 48 m. **2:** car A to the junction, 6 m. **3:** 32.8 m
   from the cross, the distance 4.1 s takes at 8 m/s.

1. **2** Car A decides 6 m before the junction (chosen).
2. **1** At that moment the AV is 48 m from the red cross, where car A's
   turn crosses its lane: 48 / 8 = 6.0 s away (we placed it there).
3. **3** 4.1 s at 8 m/s is 4.1 × 8 = 32.8 m. The AV is farther than that,
   6.0 s ≥ 4.1 s, so car A turns without stopping.


.. _l8-lec-run2:

Run #2: The AV Starts 24 m Closer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/run2_gap.png
   :alt: The same top view as run 1, at the moment car A decides, with the junction shaded tan. The AV, black, on the south lane at x 132, facing east. Car A, green, on the north lane at x 174, facing west. A red cross at x 156. Tag 1: a two-headed arrow below the road from the AV to the red cross. Tag 2: a two-headed arrow above the road from car A to the junction's entry at x 168. Tag 3: a dashed mark across the AV's lane at x 123, behind the AV.
   :width: 95%
   :align: center

   Run #2 at the moment car A decides, from above, to scale; the junction is
   shaded tan. **1:** the AV to the red cross, 24 m. **2:** car A to the
   junction, 6 m. **3:** 32.8 m from the cross, the distance 4.1 s takes at
   8 m/s; the AV is inside it.

Run #2 changes one thing: the AV starts 24 m closer to the crossing.

1. **1** When car A decides (**2**), the AV is now 48 − 24 = 24 m from the
   red cross: 24 / 8 = 3.0 s away. **3** That is inside 32.8 m (4.1 s), so
   car A stops and waits.
2. The AV's front reaches the crossing at 6.08 − 3.0 = 3.08 s. Its rear
   clears it 4.5 / 8 = 0.56 s later (4.5 m: a car's length), at 3.64 s.
   Then the gap rule lets car A go; our driver waits 1 s more (chosen).
3. The left mode that ignores the AV ends 18.31 m off. With the gap rule it
   ends 0.86 m off: the extra second our driver waited.

.. note::

   Same track for car A up to :math:`t` = 0, different futures: the **AV's**
   motion is an input to car A's prediction.


.. _l8-lec-pet:

Post-Encroachment Time: What It Measures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Post-encroachment time (PET)
   :class: note

   "Post-encroachment time is the time between when the first vehicle last
   occupied a position and the time when the second vehicle subsequently
   arrived to the same position" (Gettman et al., 2008). A larger PET is a
   wider margin.

.. figure:: /_static/images/L8/pet_side.png
   :alt: A side view of the road, to scale, with the red cross on it at 0 meters. The AV is drawn twice, driving right: faded, tag 1, with its front bumper at the cross; black, tag 2, with its rear bumper at the cross and its front bumper 4.5 meters past it. Above the black AV, a black bar from 0 to 4.5 meters, tag 3. A time axis on top marks 5.63 seconds above 0 meters and 6.19 seconds above 4.5 meters.
   :width: 80%
   :align: center

   The AV in run #1, at 8 m/s, from the side. **1:** its front bumper
   reaches the red cross at 5.63 s. **2:** its rear bumper leaves it at
   6.19 s. **3:** the bar: the time the AV's body covers the cross, its
   length over its speed, 4.5 / 8 = 0.56 s. Car A, turning at 5.0 m/s,
   covers it for 4.5 / 5.0 = 0.9 s.


.. _l8-lec-pet-runs:

Post-Encroachment Time in the Two Runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/pet_timeline.png
   :alt: A timeline from 0 to 8 seconds, time from now, in two parts. Run 1: a green bar for car A from 3.19 to 4.09 seconds and a black bar for the AV from 5.63 to 6.19, with a double arrow between them, tag 1. Run 2: a black bar for the AV from 2.63 to 3.19 seconds, a double arrow from 3.19 to 8, tag 2, and a green arrow for car A pointing right from 8 seconds.
   :width: 95%
   :align: center

   When each car's body is on the red cross, against the time from now:
   run #1 on top, run #2 below. Green: car A; black: the AV. **1:** run #1's
   PET, from car A leaving to the AV arriving. **2:** run #2's PET so far, from
   the AV leaving to the end of the run at 8 s; the green arrow: car A has not
   arrived by then.

The bars are the truth: what each car really did. A bar runs from when a
car's front bumper reaches the red cross to when its rear bumper leaves it. Its length is the car's length, 4.5 m, over its
speed there: car A turns at 5.0 m/s (4.5 / 5.0 = 0.9 s), and the AV drives at
8 m/s (4.5 / 8 = 0.56 s).

- **1** Run #1: car A leaves at 4.09 s, the AV arrives at 5.63 s.
  PET = 5.63 − 4.09 = 1.54 s.
- **2** Run #2: the AV leaves at 3.19 s; car A has not arrived when the run ends,
  at 8.0 s. PET is more than 8.0 − 3.19 = 4.81 s.

.. note::

   ADE and FDE say how good a prediction is; PET says how close two road
   users come. A planner can compute PET before it happens, from the
   predictions. In run #1:

   1. Car A's left-turn mode has car A leave the cross at 3.82 s; the AV's
      plan reaches it at 5.63 s. Predicted PET: 5.63 − 3.82 = 1.81 s.
   2. In truth car A left at 4.09 s, 4.09 − 3.82 = 0.27 s later than
      predicted, so the true PET was smaller: 1.54 s. The prediction was
      optimistic: the AV had 0.27 s less margin than it planned for.


.. _l8-lec-disc-react:

Discussion: Do Other Drivers React to the AV?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Discussion
   :class: hint

   In run #2, our predictor assumed that car A sees the AV and waits for a
   gap. **Should the AV assume that other drivers react to it? What goes
   wrong if one does not?** Three minutes with your neighbors.

.. dropdown:: What to listen for
   :color: success
   :icon: check-circle

   - **A driver who does not react.** If the AV assumes car A waits and car A pulls out
     (car A did not see the AV), the AV keeps its speed toward a car in its lane.
     Run #2 shows how far apart the two futures are: the left mode that ignores
     the AV ends 18.31 m from the truth.
   - **Nobody reacts.** If the AV assumes that, it treats every car as if it
     will pull out, and it may wait a long time at a busy junction.
   - **A middle way:** keep both futures, car A waits and car A goes, each with a
     probability, and plan so the AV can still stop if the less likely one
     happens.
   - The next section takes this up: the AV's plan changes the other drivers'
     futures.


.. _l8-lec-av-plan:

The AV's Plan Changes the Other Drivers' Futures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   "Our key insight is that an autonomous car's actions will actually
   affect what other cars will do in response, whether the car is aware of
   it or not" (Sadigh et al., 2016).

- In run #2, an AV that arrived 1 s later would give car A a 3.0 + 1 = 4.0 s
  gap: still below 4.1 s, so car A would still wait. Arriving 2 s later gives
  5.0 s, and car A would go.
- So predicting car A needs the AV's plan, and choosing the plan needs car A's
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

1. **Current position only:** car A is in the other lane, 4 m from the AV's lane
   center. A check that uses only current positions sees car A in the AV's
   lane at :math:`t` = 3.4 s, when car A is already there.
2. **Predicted positions:** at :math:`t` = 0, the left mode (P(left) =
   0.87) already puts car A in the AV's lane from :math:`t` = 3.2 to 4.0 s.

.. note::

   The prediction warns the AV 3.4 s earlier, at :math:`t` = 0: time to
   ease off gently instead of braking hard. GP4's behavior node reads
   current fused objects; a predicted path is the next input to add.


.. _l8-lec-handson-interact:

Hands-On, Part 4: Drivers Who React
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``interact`` part of the hands-on script shows B, car A and the AV: car A's
meters driven on the left, car B's speed on the right. The commands are on
:doc:`the Code page <l8_code>`.

.. admonition:: What to look at
   :class: hint

   1. Run #1: compare B's speed from CV and from the IDM. At what time do the
      two speed curves start to differ?
   2. Tick **AV 24 m closer** (run #2). Read car A's gap in the title. Which of
      the two "most likely mode" lines matches the truth?
   3. In ``l8sim.py``, set ``GAP = 2.5``. ``GAP`` is the critical headway,
      4.1 s in the lecture. What does car A do in run #2 now? And car B, behind
      it?


.. _l8-lec-next:

Next Class
----------

.. admonition:: Today
   :class: important

   Car A, braking, was 6.5 m before the junction at :math:`t` = 0; the
   physics models said "straight on" (CV's FDE 12.35 m). The map gave two
   futures; car A's speed made the left turn 0.87 likely, and that mode ended
   1.88 m from the truth. Car B needed car A's prediction (FDE: IDM 0.92 m, CV
   3.55 m), and car A's own choice needed the AV's position (run #2).

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
