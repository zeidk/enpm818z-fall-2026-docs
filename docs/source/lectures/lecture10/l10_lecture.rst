====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L10, the slides shown in class and
   the reading slide that goes with them, in the same order and with the
   same sections. You can read them at home. The deck has no appendix:
   material that was cut from class for time sits in closed **More detail**
   boxes, right after the part they explain. They are not on the quiz.

   The papers and pages behind these notes are listed on :doc:`the
   References page <l10_references>`.


.. _l10-lec-introduction:

Introduction
------------

The local planner's output is a **path**: map points :math:`(x, y)` for the
next 70 m, planned again every 0.5 s. The behavior layer above it decides
which lanes the AV may use, where it must stop, and a speed limit. A path
says only where the AV should go, not when. Today we plan trajectories,
paths with times, around a car that moves, and then turn a trajectory into
steering, throttle and brake.

.. figure:: /_static/images/L10/l10_stack.png
   :alt: A block diagram of four boxes in a row joined by arrows: Route planner (L7), Behavior layer (L9), Local planner (L9) and Controller (L10, today); only the controller box is green. Under the arrows: lanes to follow, a task, a path for the next seconds, and, after the controller, steering, throttle, brake. Above, a box Pose feeds the route planner, a box Pose, objects, predictions feeds the behavior layer and the local planner, and a box Pose, speed feeds the controller.
   :width: 95%
   :align: center

   The four layers, and today's layer: the controller.

.. admonition:: Reading the figure
   :class: tip

   Read the row left to right. Each arrow carries what one layer hands to
   the next. Each box names the lecture that covers its layer.

   - The **route planner** (L7) reads the pose and hands on the lanes to
     follow.
   - The **behavior layer** (L9) reads the pose, the objects and their
     predictions, and hands on a task.
   - The **local planner** (L9) reads the same inputs and hands on a path
     for the next seconds.
   - The **controller** (L10, today, green) reads the pose and the speed,
     and turns the path into steering, throttle and brake.


.. _l10-lec-recap-path:

Recap L9, the Path: Sample 31 Candidates, Keep the Cheapest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Last class, the local planner found a path past a parked car on our Town03
road, with the AV at 10 m/s. It worked in the Frenet frame: :math:`s` is the
distance along the right lane's center, :math:`d` the offset to its left.

.. figure:: /_static/images/L10/candidate_set.png
   :alt: A graph of d against s, s from 57 to 132 meters, the right lane pale yellow and the left lane pale purple. A black car icon, the AV, at s = 60 and d = 0. Thirty thin dark curves leave it, solid, dashed or dotted, and level off at ten values of d from minus 0.5 to 4 meters, every 0.5; a dot marks where each one levels off, at s = 80 for the solid ones, 90 for the dashed ones and 100 for the dotted ones. A thick dark line stays at d = 0 and ends with a bar at s = 110. A blue car icon, the obstacle, at s = 118 just below d = 0. A legend names the line styles 20 m, 30 m and 40 m, and the thick line stop behind.
   :width: 85%
   :align: center

   Last class's 31 candidates, from the AV at s = 60 m.

.. admonition:: Reading the figure
   :class: tip

   - The AV (black car icon) sits at :math:`s` = 60 m, :math:`d` = 0; the
     parked car (blue icon) sits at :math:`s` = 118 m, just below
     :math:`d` = 0.
   - Thirty curves leave the AV and level off at ten offsets from
     :math:`-0.5` to 4 m, every 0.5 m: solid curves level off over 20 m,
     dashed over 30 m, dotted over 40 m.
   - A thick dark line stays at :math:`d` = 0 and ends with a bar at
     :math:`s` = 110 m: the stop-behind candidate.

1. **Sample**: 10 end offsets :math:`d_\text{end}` times 3 maneuver lengths
   (20, 30 and 40 m, chosen: 2, 3 and 4 s at 10 m/s), plus 1 stop behind: 31
   candidates.
2. **Check**: 18 collide, 4 turn too hard (over 3 m/s²).
3. **Score** the 9 left and keep the cheapest: the left lane over 40 m, cost
   5.07.
4. **Repeat** every 0.5 s.

.. important::

   Each candidate is a **path**: a curve :math:`d(s)`, positions with no
   times.


.. _l10-lec-lane-change-numbers:

Describe One Lane Change with Four Numbers: s0, d0, Δd and L
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Candidate A, the cheapest (green), on last class's road; the :math:`d` axis
is stretched.

.. figure:: /_static/images/L10/scurve_setup.png
   :alt: A graph of d against s, s from 50 to 123 meters, the right lane pale yellow from minus 1.75 to 1.75 and the left lane pale purple from 1.75 to 5.25, the right lane's center a thick black line at d = 0 and the left lane's center dotted at 3.5. A black AV icon at s = 60, d = 0; a blue parked car at s = 118, just below d = 0. A thick green S curve leaves the AV, crosses the dashed lane line near s = 80, reaches d = 3.5 at a green dot at s = 100 and runs straight on. Two dotted vertical guides at s = 60 and s = 100, labeled s0 = 60 m and s0 + L = 100 m near the bottom. Above the road, a double arrow between the guides is labeled L = 40 m. Near the AV, the label d0 = 0. A vertical double arrow at s = 107, from d = 0 up to 3.5, is labeled Delta d = 3.5 m. A top axis, u = (s minus s0) / L, reads 0 above s = 60, 0.5 above s = 80 and 1 above s = 100.
   :width: 80%
   :align: center

   Candidate A, the cheapest path, with its four numbers.

.. admonition:: Reading the figure
   :class: tip

   - The AV starts at :math:`s_0` = 60 m, :math:`d_0` = 0; the green curve
     reaches :math:`d` = 3.5 m at :math:`s_0 + L` = 100 m and runs straight
     on from there.
   - The double arrow above the road marks :math:`L` = 40 m, the maneuver
     length; the vertical double arrow marks :math:`\Delta d` = 3.5 m, how
     far the move goes sideways.
   - The top axis reads :math:`u = (s - s_0)/L`: 0 at the start, 0.5 at
     :math:`s` = 80 m, 1 at the end.

- :math:`s_0`: where the move starts.
- :math:`d_0`: the offset where it starts.
- :math:`\Delta d`: how far it moves sideways.
- :math:`s`: a point along the road (the bottom axis).
- :math:`L`: the maneuver length, along :math:`s`.
- :math:`u`: how far through the move :math:`s` is (the top axis).


.. _l10-lec-u:

Read u: How Far Through the Move a Point s Is
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pick a point :math:`s` on the road, in meters along the right lane's
center. For candidate A (:math:`s_0` = 60 m, :math:`L` = 40 m), :math:`u`
says how far through the move that point is:

.. math::
   u = \frac{s - s_0}{L} = \frac{s - 60}{40}

.. list-table::
   :widths: 15 35 50
   :header-rows: 1
   :class: compact-table

   * - :math:`s` (m)
     - :math:`u`
     - What it says
   * - 60
     - (60 − 60) / 40 = 0
     - the move starts: the AV is at :math:`s_0`
   * - 70
     - (70 − 60) / 40 = 0.25
     - a quarter of the way through
   * - 80
     - (80 − 60) / 40 = 0.5
     - halfway through
   * - 100
     - (100 − 60) / 40 = 1
     - the move ends, at :math:`s_0 + L`
   * - 110
     - (110 − 60) / 40 = 1.25
     - past the end: the move is over

- :math:`u` has no unit: meters divided by meters. It is a share of the
  move.
- Only 0 to 1 matters: past the end the AV stays at :math:`d_0 + \Delta d`,
  so the code clips :math:`u` to 1.
- The same :math:`u` works for every :math:`L`: halfway is :math:`u` = 0.5
  for 20, 30 or 40 m.


.. _l10-lec-qu:

Shape the Move with q(u): How Much of Δd Is Done at u
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`u` is the share of the distance :math:`L` covered. :math:`q(u)` is a
**formula**: give it :math:`u`, and it returns the share of the sideways
move :math:`\Delta d` done.

.. figure:: /_static/images/L10/scurve_q.png
   :alt: A graph of q(u), the share of Delta d, from 0 to 1, against u, the share of the distance L, from 0 to 1. A dark S-shaped curve starts flat at (0, 0), rises slowly, climbs fastest in the middle and levels off flat at (1, 1). Dots on the curve at u = 0, 0.25, 0.5, 0.75 and 1, with dotted guides to both axes; the vertical axis is marked 0, 0.10, 0.5, 0.90 and 1.
   :width: 55%
   :align: center

   q(u): the share of Δd done, against u, the share of L covered.

.. admonition:: Reading the figure
   :class: tip

   The curve starts flat at (0, 0), climbs fastest around the middle, and
   levels off flat at (1, 1). Dots mark :math:`u` = 0, 0.25, 0.5, 0.75 and
   1, each with a dotted guide to both axes.

.. math::
   q(u) = 10u^3 - 15u^4 + 6u^5

1. :math:`u = 0`: :math:`q = 0`. None of the move is done.
2. :math:`u = 0.25`: :math:`q = 0.156 - 0.059 + 0.006 = 0.10`. A quarter of
   the distance, a tenth of the move: a slow start.
3. :math:`u = 0.5`: :math:`q = 1.25 - 0.9375 + 0.1875 = 0.5`. Halfway, half
   the move.
4. :math:`u = 0.75`: :math:`q = 4.219 - 4.746 + 1.424 = 0.90`.
5. :math:`u = 1`: :math:`q = 10 - 15 + 6 = 1`. The whole move.

The slope of :math:`q`, :math:`30u^2(1 - u)^2`, is 0 at :math:`u = 0` and
:math:`u = 1`: the curve is flat at both ends. So the AV leaves its lane and
enters the next one parallel to the lane.

.. dropdown:: More detail: find 10, −15 and 6
   :class-container: more-detail
   :icon: info
   :name: l10-more-quintic-numbers

   :math:`q` is a polynomial of degree five, with six numbers to find:
   :math:`q(u) = a_0 + a_1 u + a_2 u^2 + a_3 u^3 + a_4 u^4 + a_5 u^5`. Six
   conditions fix them, three at each end: the value :math:`q`, the slope
   :math:`q'` (how fast :math:`q` grows) and the bend :math:`q''` (how fast
   the slope changes).

   1. At :math:`u = 0`: :math:`q = 0`, :math:`q' = 0`, :math:`q'' = 0`. They
      give :math:`a_0 = 0`, :math:`a_1 = 0`, :math:`a_2 = 0`.
   2. At :math:`u = 1`: :math:`q = 1`, :math:`q' = 0`, :math:`q'' = 0`, with
      :math:`q' = 3a_3u^2 + 4a_4u^3 + 5a_5u^4` and
      :math:`q'' = 6a_3u + 12a_4u^2 + 20a_5u^3`. Every power of 1 is 1, so
      they are three equations:

      .. math::
         a_3 + a_4 + a_5 = 1, \qquad 3a_3 + 4a_4 + 5a_5 = 0, \qquad
         6a_3 + 12a_4 + 20a_5 = 0

   3. Second minus 3 times the first: :math:`a_4 + 2a_5 = -3`. Third minus 6
      times the first: :math:`6a_4 + 14a_5 = -6`.
   4. That minus 6 times :math:`a_4 + 2a_5 = -3`: :math:`2a_5 = 12`, so
      :math:`a_5 = 6`. Then :math:`a_4 = -3 - 2 \times 6 = -15` and
      :math:`a_3 = 1 + 15 - 6 = 10`.

   The six conditions are equations: we solve them for the numbers. The
   result, :math:`q(u) = 10u^3 - 15u^4 + 6u^5`, is a formula: give it
   :math:`u`, and it returns :math:`q`.


.. _l10-lec-candidate-formula:

Write Every Candidate with One Formula: d(s) = d0 + Δd q(u)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here :math:`d(s)` is the path's sideways offset at a point :math:`s` on the
road: how far left of the right lane's center, in meters, the path is
there. It is the start offset plus the share :math:`q(u)` of the sideways
move:

.. important::

   .. math::
      d(s) = d_0 + \Delta d\; q(u), \qquad u = \frac{s - s_0}{L}

   After :math:`s_0 + L`, :math:`d` stays at :math:`d_0 + \Delta d`.

The planner writes all 31 candidates with this formula, then checks and
scores them:

- 30 lane shifts: the same :math:`s_0` = 60 m and :math:`d_0` = 0; only
  :math:`\Delta d` and :math:`L` change.
- 1 stop behind: :math:`\Delta d = 0`, so :math:`d(s) = 0`. It ends 2.0 m
  short of the parked car (:math:`s` = 110.15 m, as in L9).

Candidate A, with :math:`\Delta d` = 3.5 m and :math:`L` = 40 m, at three
points:

1. :math:`s` = 60 m: :math:`u = 0`, :math:`q = 0`, :math:`d = 0`: on the
   right lane's center.
2. :math:`s` = 80 m: :math:`u = 20/40 = 0.5`, :math:`q = 0.5`,
   :math:`d = 3.5 \times 0.5 = 1.75` m: on the lane line.
3. :math:`s` = 100 m: :math:`u = 1`, :math:`q = 1`, :math:`d` = 3.5 m: on
   the left lane's center.

.. important::

   Only :math:`s` appears, never a time: that makes it a path. Later today,
   Trajectory Generation writes :math:`d` as a polynomial in the time
   :math:`t`.


.. _l10-lec-two-candidates:

See Two Candidates on the Road Before Scoring Them: A and B
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two of the 9 candidates that pass the checks, both from :math:`s_0` = 60 m
over :math:`L` = 40 m.

.. figure:: /_static/images/L10/two_candidates.png
   :alt: A graph of d against s, s from 56 to 132 meters, the right lane pale yellow from minus 1.75 to 1.75 and the left lane pale purple from 1.75 to 5.25, the right lane's center a thick black line at d = 0 and the left lane's center dotted at 3.5. A black AV icon at s = 60, d = 0; a blue parked car at s = 118, just below d = 0. Two S curves leave the AV together: a green one, labeled A, levels off at d = 3.5 near s = 100; a gray one, labeled B, levels off just below it at d = 3. Both then run straight to s = 132.
   :width: 90%
   :align: center

   Candidates A and B on the road.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a map: the :math:`d` axis is stretched.

   - **A** (green): :math:`d(s) = 3.5\; q\big((s - 60)/40\big)`, to the
     left lane's center.
   - **B** (gray): :math:`d(s) = 3.0\; q\big((s - 60)/40\big)`, 0.5 m short
     of it: it ends 0.5 m closer to the parked car's lane.


.. _l10-lec-apply-costs:

Apply the Costs: A Is the Cheapest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the planner has all the candidates, it applies the costs to the 9 that
pass the checks. Each term is a number read off the curve times a weight
chosen in L9; lower is better. A and B from the last section, with
:math:`u = (s - 60)/40`:

.. list-table::
   :widths: 15 35 25 25
   :header-rows: 1
   :class: compact-table

   * - **Term**
     - **Read off the curve, times the weight**
     - **A**: :math:`d = 3.5\,q(u)`
     - **B**: :math:`d = 3.0\,q(u)`
   * - Comfort
     - peak sideways acceleration (m/s²), times 2
     - 2 × 1.253 = 2.51
     - 2 × 1.076 = 2.15
   * - Clearance
     - 1.5 m minus the smallest gap, times 4
     - 4 × (1.5 − 1.359) = 0.56
     - 4 × (1.5 − 0.859) = 2.56
   * - Lane
     - lanes off the route, times 2; meters off a lane center, times 2
     - 2 × 1 + 2 × 0 = 2.00
     - 2 × 1 + 2 × 0.5 = 3.00
   * - Progress
     - meters of the 70 m not covered, times 0.5
     - 0
     - 0
   * - **Cost**
     - sum of the four
     - **5.07**
     - **7.71** (7.72 unrounded)

.. important::

   B ends 0.5 m closer to the parked car: it saves 0.36 on comfort but pays
   2.00 more on clearance and 1.00 more on the lane. A also beats the other
   7, the stop behind (11.54) included.


.. _l10-lec-recap-behavior:

Recap L9, the Behavior Layer: It Picks the Task, the Planner Finds the Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Last class split the job in two: the behavior layer says **what** to do;
the local planner works out **how**, as a path.

.. list-table::
   :widths: 36 64
   :header-rows: 1
   :class: compact-table

   * - **The behavior layer decides**
     - **On our road (L9)**
   * - which lanes the AV may use
     - both open: 31 candidates; left lane closed: 10, and the AV stops
       behind the parked car (cost 11.54)
   * - where the AV must stop, and by when
     - nowhere: the paths run the full 70 m
   * - a speed limit
     - 10 m/s: every bend needs a radius of 33.3 m or more

- Its tools: a **finite state machine** (FSM) picks one behavior at a time,
  as for the valet in the garage; a **game** decides the lane change: the AV
  goes first only when prediction says the other car will yield.
- Today: one FSM grows too fast for city streets (Scaling the Behavior
  Layer), and the path gets times (Trajectory Generation).


.. _l10-lec-tracking-compare:

Compare Path Tracking and Trajectory Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Snider: "Path tracking refers to a vehicle executing a globally defined
geometric path by applying appropriate steering motions that guide the
vehicle along the path" (Snider, 2009).

.. list-table::
   :widths: 22 39 39
   :header-rows: 1
   :class: compact-table

   * -
     - **Path tracking**
     - **Trajectory tracking**
   * - Follows
     - points :math:`(x, y)`: where to be
     - points :math:`(x, y)`, each with a time: where to be, and when
   * - Speed comes from
     - a separate speed profile
     - the times in the reference
   * - If the AV is 1 s late
     - no error, as long as it is on the path
     - an error: it is behind where it should be
   * - Used today by
     - Pure Pursuit and Stanley, each with a speed PID
     - MPC can track it: its horizon has times

Our turn uses path tracking: the path, plus a speed profile for the speed
PID.

.. dropdown:: More detail: the same lane change as two references; the Frenet frame to control
   :class-container: more-detail
   :icon: info
   :name: l10-more-tracking

   .. rubric:: The same lane change, two references

   The same lane change, written two ways (numbers chosen for the example).
   As a **trajectory**, where and when:

   .. list-table::
      :widths: 25 25 25 25
      :header-rows: 1
      :class: compact-table

      * - :math:`t` (s)
        - :math:`x` (m)
        - :math:`y` (m)
        - :math:`v` (m/s)
      * - 0.0
        - 0.0
        - 0.0
        - 15.0
      * - 1.0
        - 15.0
        - 0.9
        - 15.0
      * - 2.0
        - 30.0
        - 2.8
        - 15.0
      * - 3.0
        - 45.0
        - 3.5
        - 15.0

   Drop :math:`t` and :math:`v` and a **path** is left, where only:

   .. list-table::
      :widths: 50 50
      :header-rows: 1
      :class: compact-table

      * - :math:`x` (m)
        - :math:`y` (m)
      * - 0.0
        - 0.0
      * - 15.0
        - 0.9
      * - 30.0
        - 2.8
      * - 45.0
        - 3.5

   A trajectory must reach each point at its time: needed when the timing
   matters, as when merging or crossing ahead of another car. Drop the
   path's time and speed, and the speed then comes from a separate profile.

   .. rubric:: From the Frenet frame to control: the offset d is the cross-track error

   The planner works in the Frenet frame :math:`(s, d)`; the controllers
   need map points and errors.

   .. list-table::
      :widths: 28 72
      :header-rows: 1
      :class: compact-table

      * - **Controller**
        - **What it needs**
      * - Pure Pursuit
        - path points :math:`(x_i, y_i)`, plus a speed profile
      * - Stanley
        - path points and the path's heading
      * - PID on steering
        - the cross-track error
      * - LQR, MPC
        - the path, its heading and curvature, the speed: a model's
          reference

   - Back to the map: :math:`x = x_r(s) - d\sin\theta_r(s)`,
     :math:`y = y_r(s) + d\cos\theta_r(s)`: the point on the reference and
     then :math:`d` meters to its left.
   - The AV's own :math:`d` **is** its cross-track error: its signed
     distance from the path, positive to the left.


.. _l10-lec-two-controllers:

Follow the Path at the Right Speed: Two Controllers Side by Side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Feedback controller
   :class: note

   A program that, at every cycle, compares what the AV should be doing with
   what it measures it is doing, and sends a command that shrinks the
   difference.

.. list-table::
   :widths: 22 43 35
   :header-rows: 1
   :class: compact-table

   * -
     - **Lateral (steering)**
     - **Longitudinal (speed)**
   * - Should be
     - on the path
     - at the profile's speed
   * - Measures
     - distance and angle to the path
     - speed
   * - Sends
     - a steering angle
     - throttle or brake
   * - Today
     - Pure Pursuit, Stanley, MPC
     - PID


.. _l10-lec-map:

From the Inputs to a Steering Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each section today fills in one box of this flowchart. In the deck, each
section's divider shows it again with that box highlighted, and the boxes
link to their sections.

.. figure:: /_static/images/L10/l10_pipeline.png
   :alt: The lecture's flowchart. Top row: the inputs (the path with its points and curvature, the AV's pose and speed, the limits), then the behavior layer (an FSM or a tree picks a target speed), the trajectory (d and s in time) and the speed profile (curves cap the speed). Below, a green dashed frame, the controller node: the bicycle model (how steering turns the AV, dashed), the speed PID (throttle, brake), fed the target speed from the speed profile, and a row of three steering methods, one of which is used (the section also covers PID and LQR): Pure Pursuit, Stanley, MPC, fed the path from the inputs; the bicycle model points down to them. Both loops lead to the output (steer, throttle, brake, every 0.05 s, to the actuators), which goes to the AV in CARLA; a dashed line takes the measured pose and speed back to the inputs. Each box links to its section.
   :width: 100%
   :align: center

   The lecture's flowchart: from the inputs to a steering command.

.. admonition:: Reading the figure
   :class: tip

   Each box is covered in one section of these notes.

   - **Inputs** (gray): the path with its points and curvature, the AV's
     pose and speed, the limits.
   - **Behavior layer** (green, top row): an FSM or a tree picks a target
     speed. See :ref:`l10-lec-behavior`.
   - **Trajectory** and **Speed profile** (top row): :math:`d` and :math:`s`
     in time, then curves that cap the speed. See
     :ref:`l10-lec-trajectory`.
   - **Controller node** (green dashed frame): the bicycle model (how
     steering turns the AV), the speed PID, and a row of three steering
     methods, Pure Pursuit, Stanley and MPC, one of which is used (the
     section also covers PID and LQR on steering). These boxes are covered
     later in the lecture.
   - **Output** (gray): steer, throttle and brake, every 0.05 s, to the
     actuators. See :ref:`l10-lec-control-interface`.
   - A dashed line takes the measured pose and speed from the AV in CARLA
     back to the inputs.


.. _l10-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

This is a reading slide in the deck. After this lecture, you can:

1. say why one flat FSM grows too fast, and how a **superstate** and a
   **behavior tree** keep the behavior layer small;
2. write the **kinematic bicycle model** and find the steering angle that follows a curvature;
3. give a path a speed profile and a time (a **trajectory**), and say why a
   quintic speed change keeps the **jerk** small;
4. read a **PID** speed response: what P, I and D each do, what **windup**
   is and how clamping stops it;
5. work **Pure Pursuit**'s geometry by hand, from the lookahead circle to
   the steering angle;
6. predict how the **lookahead distance** changes Pure Pursuit, and compare
   it with **Stanley**;
7. say what **MPC** adds: a model, a horizon, limits, and only the first
   input applied.


.. _l10-lec-behavior:

Scaling the Behavior Layer
---------------------------

Last class showed one finite state machine (FSM) for a valet that parks
itself in a garage. Here we use the same tools on an AV that drives city
streets.

**In this section:** two parts. Finite State Machines: five road behaviors
and a safety monitor need 5 × 3 = 15 states in one flat FSM, and a
superstate cuts its arrows. Behavior Trees: what a tree is, how it
runs, and our road behaviors as a tree.

**What it is for:** real stacks face the same growth: Nav2, ROS 2's
navigation stack, runs a behavior tree (Nav2 contributors). The behavior
layer's output, such as a target speed, is the input to the rest of today.


.. _l10-lec-fsm:

Finite State Machines
~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Finite state machine (FSM)
   :class: note

   A fixed list of **states**, of which the system is in exactly one at a
   time, and a list of **transitions**: each one moves the system from one
   state to another when its condition becomes true.


.. _l10-lec-flat-fsm:

Step 1, the Problem: One Flat FSM Multiplies Its States
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to see why one flat FSM grows too fast. Our AV drives city
streets with five behaviors: Lane keep, Follow a slower car, Change lane,
Stop at the line and Cross the intersection. A safety monitor adds three
states: Nominal, Caution, Emergency. Both lists are chosen for this example.
The AV is in one behavior and one monitor state at once, so one flat FSM
needs a state for every pair: 5 × 3 = 15.

.. figure:: /_static/images/L10/beh_flat.png
   :alt: A grid of 15 rounded boxes in three rows and five columns. Each box names one road behavior and one monitor state: the columns are Lane keep, Follow, Change lane, Stop at line and Cross, the rows Nominal, Caution and Emergency. Three orange arrows go from Lane keep to Follow, one in each row; dark tag 1 marks the top one. Five blue arrows go down from each Nominal box to the Caution box below it; dark tag 2 marks the leftmost one.
   :width: 85%
   :align: center

   The road behaviors and the monitor as one flat FSM: 15 states.

.. admonition:: Reading the figure
   :class: tip

   Each box is one state of the flat FSM: a road behavior (the column: Lane
   keep, Follow, Change lane, Stop at line, Cross) paired with a monitor
   state (the row: Nominal, Caution, Emergency).

   - **Tag 1:** Lane keep to Follow, drawn once per monitor state: 3 arrows
     (orange).
   - **Tag 2:** the monitor's Nominal to Caution, drawn once per behavior:
     5 arrows (blue).

.. important::

   Harel: "two components with one thousand states each would result in one
   million states in the product" (Harel, 1987). That is
   1000 × 1000 = 1,000,000.


.. _l10-lec-superstate:

Step 2, Fewer Arrows: One Superstate Arrow Replaces Five
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to add an emergency stop without an arrow from every state. The
AV must be able to stop from any of its five behaviors, so one flat FSM
needs 5 arrows to Emergency stop.

.. figure:: /_static/images/L10/beh_hier.png
   :alt: A state diagram. A large green rounded box labeled Driving, dark tag 1 at its top-left corner, holds five states: Lane keep, Follow and Change lane in a top row, Stop at the line and Cross the intersection below. An arrow from the left enters Lane keep. Lane keep and Follow go to each other; Follow goes to Change lane; Change lane goes back to Lane keep by an arc over the top. Lane keep goes down to Stop at the line, which goes to Cross the intersection, which goes back up to Lane keep. One red arrow, dark tag 2, leaves the bottom edge of the Driving box and goes down to Emergency stop.
   :width: 75%
   :align: center

   The road behaviors inside the superstate Driving.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** the **superstate** Driving, a state that holds the five
     behaviors (green box). Their own arrows stay as they were: Lane keep
     and Follow go to each other, Follow goes to Change lane and back to
     Lane keep, and Lane keep goes to Stop at the line, then to Cross the
     intersection, then back to Lane keep.
   - **Tag 2:** one arrow (red) leaves Driving for Emergency stop. It stands
     for 5 arrows, one from each state inside.

.. important::

   Harel lets a transition that leaves a superstate stand for that
   transition leaving every state inside it: "the main way statecharts
   economize in the number of arrows" (Harel, 1987).


.. _l10-lec-bt:

Behavior Trees
~~~~~~~~~~~~~~

A behavior tree has no arrows between behaviors: at every tick it checks its
conditions again and runs the first branch that does not fail. We read its
parts, then write our road behaviors as a tree.


.. _l10-lec-bt-def:

Define a Behavior Tree: a Root, Control Nodes and Leaves
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to name the parts of a behavior tree before we read one.

.. admonition:: Definition: Behavior tree (BT)
   :class: note

   "A directed rooted tree where the internal nodes are called control flow
   nodes and leaf nodes are called execution nodes" (Colledanchise and
   Ögren, 2018).

In plain words, with our road behaviors:

- The **root** is the one node with no parent. Every tick starts there.
- **Control flow nodes**, such as Sequence and Fallback, sit inside the tree
  and decide which child is ticked next.
- A **Condition** leaf checks a fact and returns Success or Failure: a stop
  line within 30 m, a car ahead within 40 m.
- An **Action** leaf runs a behavior: "While the action is ongoing it
  returns Running". Ours: Lane keep, Follow, Change lane, Stop at the line.


.. _l10-lec-bt-read:

Read a Behavior Tree: Ticks, Three Statuses, Four Node Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to learn how a tree runs. A tick goes down from the root: "A
node is executed if and only if it receives ticks". A ticked node returns
Running, Success or Failure (Colledanchise and Ögren, 2018).

.. list-table::
   :widths: 17 83
   :header-rows: 1
   :class: compact-table

   * - **Node**
     - **What it does when ticked**
   * - Sequence (→)
     - Ticks its children one at a time, from the left. A child that
       succeeds: tick the next one. A child that fails or is still running:
       stop there and return that status. So it succeeds only if every
       child succeeds. In our road tree (next slide): the pass branch
       checks that the car ahead is slow, then that the left lane is free,
       then runs Change lane.
   * - Fallback (?)
     - Ticks its children one at a time, from the left. A child that fails:
       try the next one. A child that succeeds or is still running: stop
       there and return that status. So it fails only if every child fails.
       In our road tree: the root, which tries stop, pass, follow and keep
       lane, in that order.
   * - Parallel
     - Ticks all its children at every tick. It succeeds once :math:`M` of
       its :math:`N` children succeed, fails once :math:`N - M + 1` fail
       (then :math:`M` successes can no longer happen), and is running
       otherwise. :math:`M` is set by the designer.
   * - Decorator
     - Has one child. A rule set by the designer changes the status the
       child returns, and decides when the child is ticked at all.


.. _l10-lec-road-bt:

Pass a Slow Car or Follow It: Four Road Behaviors as a Behavior Tree
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to write four of the road behaviors as a tree. The root
Fallback (?) tries its branches from the left: stop for a line, pass a slow
car, follow a car, keep the lane. Ellipses are conditions, gray boxes are
actions; each tag is one condition (thresholds chosen for this example).

.. figure:: /_static/images/L10/beh_road_bt.png
   :alt: A behavior tree. The root, a Fallback box marked with a question mark, has four children from left to right: three Sequence boxes marked with an arrow, and a gray action box, Lane keep. The first Sequence holds condition 1, an ellipse with dark tag 1, and the action Stop at the line. The second holds conditions 2 and 3 and the action Change lane. The third holds condition 4 and the action Follow.
   :width: 90%
   :align: center

   Four road behaviors as a behavior tree.

.. admonition:: Reading the figure
   :class: tip

   The root is a Fallback (box with a question mark). Its children, from
   left to right: a Sequence (box with an arrow) of condition 1 and Stop at
   the line; a Sequence of conditions 2 and 3 and Change lane; a Sequence of
   condition 4 and Follow; and the action Lane keep.

   - **Tag 1:** a stop line is within 30 m ahead.
   - **Tag 2:** the car ahead has driven under 6 m/s for 3 s.
   - **Tag 3:** the left lane is free: no car within 30 m behind or 40 m
     ahead.
   - **Tag 4:** a car is ahead in our lane, within 40 m.

Cross the intersection is left out to keep the tree small.


.. _l10-lec-bt-ticks:

Switch Behaviors with No Arrow: a Car in the Left Lane Stops the Pass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to watch the tree switch behaviors with no arrow, at two ticks
chosen for this example. The root ticks every 0.1 s (chosen); each tick
checks the conditions again from the left, and the first branch that does
not fail picks the action.

.. list-table::
   :widths: 50 25 25
   :header-rows: 1
   :class: compact-table

   * - **Condition**
     - **Tick 1**
     - **Tick 2**
   * - 1: a stop line within 30 m
     - no
     - no
   * - 2: the car ahead under 6 m/s for 3 s
     - yes: 5 m/s
     - yes
   * - 3: the left lane free
     - yes
     - no: a car 20 m behind
   * - 4: a car ahead within 40 m
     - yes: 25 m
     - yes
   * - The tree runs
     - Change lane
     - Follow

No arrow goes from Change lane to Follow: at tick 2, condition 3 fails, so
the second Sequence fails, and the Fallback moves on to the third branch,
Follow. Tick 2 comes before the AV has left its lane.

.. dropdown:: More detail: what real stacks use, and what they hand down
   :class-container: more-detail
   :icon: info
   :name: l10-more-real-stacks

   Real driving and robot stacks use these structures:

   - **Nav2**, ROS 2's navigation stack: its navigator reads a behavior tree
     from an XML file and "uses the Behavior-Tree.CPP library to dynamically
     create and execute the BT" (Nav2 contributors). The default tree for
     driving to a pose is
     ``navigate_to_pose_w_replanning_and_recovery.xml``.
   - **Autoware**'s behavior path planner once ran its modules from a
     behavior tree, chosen for its "high scalability compared to the state
     machine" (Autoware Foundation, older documentation). Today a Planner
     Manager runs them: candidate modules run in parallel until they are
     approved, and approved modules run in series (Autoware Foundation,
     current documentation).
   - **Apollo** plans by scenarios made of stages: each scenario has its own
     transfer condition, and the result of each stage "determines the
     transition from one stage to another" (Apollo Auto, ``scenario.h``).

   Whichever structure picks the behavior, its output is a maneuver, a
   target lane, a speed or a stop point. That output is the input to the
   rest of today.


.. _l10-lec-trajectory:

Trajectory Generation
----------------------

The behavior layer picks the task. Last class, the local planner then found
a path around a parked car; for a fast car coming up in the left lane, the
behavior layer closed that lane, and the AV waited behind the parked car
(cost 11.54). This section builds on that planner: the same road, the same
three circles and the same 0.3 m margin, plus time.

**In this section:** we plan trajectories, not paths: the sideways offset
:math:`d` and the distance :math:`s` as polynomials in time, sampled,
checked against where the other car will be, and scored for comfort.

**What it is for:** the AV passes a moving car when the timing works,
instead of waiting behind the parked car.


.. _l10-lec-traj-scene:

Plan Around a Car That Moves: Last Class Closed the Lane Instead
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/traj_scene.png
   :alt: A top view of the two-lane road, to scale: the right lane light yellow, the left lane light purple, a dashed line between them. In the left lane, at the left, a blue car, dark tag 1. A blue dashed line runs ahead of it along the left lane's center, with a blue dot every second for four seconds, dark tag 2 above the second dot. In the right lane the black AV, tag 3, below the first dots, and far ahead a blue parked car, tag 4.
   :width: 95%
   :align: center

   The scene: car B coming up in the left lane, the AV and the parked car
   ahead.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** car B, last class's fast car, in the left lane.
   - **Tag 2:** where prediction puts car B each second, a dot every second
     for four seconds.
   - **Tag 3:** the AV, in the right lane.
   - **Tag 4:** the parked car, far ahead.

- Car B, last class's fast car: 15 m behind the AV, at 15 m/s (chosen).
- Where prediction puts car B each second: straight on at 15 m/s, a constant
  velocity, the simplest prediction model.
- The AV, at 10 m/s. The parked car, 58 m ahead.

Last class's planner checked **paths**, which have no time. It could not
tell whether the AV would reach the left lane before car B or after it, so
the behavior layer closed the lane. To decide, the check needs where the AV
is at each moment, and where car B will be then.


.. _l10-lec-traj-timings:

Same Path, Two Timings: One Meets Car B, the Other Does Not
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Trajectory
   :class: note

   A path with a time at each point: where the AV should be, and when. A
   **path** says only where.

.. figure:: /_static/images/L10/traj_two_timings.png
   :alt: Two top views of the same stretch of road, to scale, one above the other, dark tags 1 and 2. Both show the same black line: it keeps the right lane, then curves smoothly into the left lane's center. Black dots on the line mark each second. Top, tag 1: the dots are evenly spaced; the black AV is crossing the dashed lane line, and the blue car B is right beside and slightly ahead of it, the two bodies touching. Bottom, tag 2: the dots are closer together at first; the AV is still in the right lane, well behind car B, which is in the left lane. The blue parked car is in the right lane at the right of both views.
   :width: 90%
   :align: center

   Two timings of the same path: one meets car B, the other does not.

.. admonition:: Reading the figure
   :class: tip

   Both views show the same path, with a dot marking each second. Both are
   drawn at :math:`t` = 3.95 s, when car B is at :math:`s` = 104.25 m.

   - **Tag 1:** 10 m/s all the way. The AV is at :math:`s` = 99.5 m, almost
     on the lane line, right beside car B.
   - **Tag 2:** slow to 7 m/s first. The AV is at :math:`s` = 90.65 m, still
     in its own lane, well behind car B.

Both paths keep the lane to :math:`s` = 80 m, then last class's S curve into
the left lane over 40 m. At 10 m/s all the way, the AV's circles overlap car
B's by 0.98 m. Slowed to 7 m/s first, the smallest gap to car B on the whole
run is 1.04 m.


.. _l10-lec-traj-quintic-d:

Plan Across the Road: the Offset d(t) as a Quintic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Werling et al. plan across and along apart (Werling et al., 2010), as last
class did, but in time: :math:`d(t)` across, :math:`s(t)` along.

.. admonition:: Definition: Quintic
   :class: note

   A polynomial of degree five:

   .. math::
      d(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5

Six numbers meet six conditions:

- at :math:`t = 0`: the AV's own :math:`d`, :math:`\dot d` and
  :math:`\ddot d`;
- at :math:`t = T`: the end offset :math:`d_1`, with
  :math:`\dot d = \ddot d = 0`, parallel to the lane.

Samples (chosen): :math:`d_1` at each lane's center and 0.5 m to each side;
:math:`T` = 3, 4 or 5 s: 6 × 3 = 18. Last class's S curve was this quintic,
in :math:`s`.

.. figure:: /_static/images/L10/traj_lat_set.png
   :alt: A graph of the sideways offset d, in meters, against time t from 0 to 7 seconds, over two horizontal bands: the right lane in yellow from minus 1.75 to 1.75, the left lane in purple from 1.75 to 5.25, a dashed line between them. Eighteen black S-shaped curves start at d = 0 at time 0 and level off at minus 0.5, 0, 0.5, 3, 3.5 or 4 meters; solid curves level off at 3 seconds, dashed at 4, dotted at 5.
   :width: 80%
   :align: center

   Eighteen quintic candidates for the sideways offset d(t).

.. admonition:: Reading the figure
   :class: tip

   Every curve starts at :math:`d` = 0 at :math:`t` = 0 and levels off at
   one of six end offsets: :math:`-0.5`, 0, 0.5, 3, 3.5 or 4 m. Solid curves
   level off at 3 s, dashed at 4 s, dotted at 5 s.

.. dropdown:: More detail: a quartic to keep a speed, the quintic's six conditions, and the equations for a slow-down
   :class-container: more-detail
   :icon: info
   :name: l10-more-quintic

   .. rubric:: Plan along the road: keep a speed with a quartic, stop with a quintic

   **Keep a speed.** No end position is asked, so five conditions:
   :math:`s`, :math:`\dot s`, :math:`\ddot s` at :math:`t = 0`, and the end
   speed :math:`\dot s_1` with :math:`\ddot s = 0` at :math:`T`. A
   **quartic** (degree four, five numbers) meets them (Werling et al.,
   2010).

   - Samples: :math:`\dot s_1` = 4, 6, 8, 10 or 12 m/s; :math:`T` = 3, 4 or
     5 s: 15.

   **Stop at a point.** The end position counts too: :math:`s =
   s_\text{stop}`, :math:`\dot s = 0`, :math:`\ddot s = 0`. Six conditions,
   a quintic.

   - :math:`s_\text{stop}` = 110.15 m, last class's stop behind the parked
     car; :math:`T` = 8, 10 or 12 s: 3.

   In all 15 + 3 = 18 along, so 18 × 18 = 324 candidates: every pair
   (Werling et al. combine the two sets the same way).

   .. figure:: /_static/images/L10/traj_lon_set.png
      :alt: A graph of the speed along the road, in meters per second, against time from 0 to 7 seconds. All curves start at 10. Thin curves change smoothly to 4, 6, 8, 10 or 12 and stay there; solid ones arrive at 3 seconds, dashed at 4, dotted at 5. Thick curves, the stops, fall slowly and are still between 1 and 2.5 meters per second at 7 seconds.
      :width: 65%
      :align: center

      The 18 speed-along-the-road candidates: 15 that keep a speed, 3 that
      stop.

   .. rubric:: The quintic: six conditions fix six numbers

   Distance along the path as a polynomial of degree five in time:

   .. math::
      s(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5

   Six unknowns, so six conditions: distance, speed and acceleration at the
   start and at the end. The planner's S curve is the same idea: a quintic
   whose slope and bend are zero at both ends, there along the road, here in
   time.

   1. Start: :math:`s = 0`, :math:`v = 8` m/s, :math:`a = 0`. End:
      :math:`s = D`, :math:`v = 3.46` m/s, :math:`a = 0`.
   2. Pick :math:`T`. Its largest deceleration is
      :math:`1.5\,\Delta v / T`; set that to 2.0 m/s²:
      :math:`T = 1.5 \times 4.54 / 2.0 = 3.41` s, and
      :math:`D = \frac{8 + 3.46}{2} \times 3.41 = 19.5` m.
   3. Solve the six equations: :math:`s(t) = 8t - 0.391\,t^3 +
      0.0573\,t^4` (the other three coefficients come out 0).

   Zero acceleration at both ends means no jump where the braking starts and
   ends. A **cubic** has four unknowns: it matches distance and speed, not
   acceleration. With :math:`T = 2.27` s and :math:`D = 13.0` m it gives
   :math:`s(t) = 8t - 1.0\,t^2`, the constant 2.0 m/s² again.

   .. rubric:: The six equations, for our slow-down

   :math:`s(t) = a_0 + a_1 t + \dots + a_5 t^5`, so :math:`v = \dot s` and
   :math:`a = \ddot s`. With :math:`T = 3.41` s and :math:`D = 19.5` m, the
   six conditions, in matrix form:

   .. math::
      \begin{bmatrix}
      1 & 0 & 0 & 0 & 0 & 0 \\
      0 & 1 & 0 & 0 & 0 & 0 \\
      0 & 0 & 2 & 0 & 0 & 0 \\
      1 & T & T^2 & T^3 & T^4 & T^5 \\
      0 & 1 & 2T & 3T^2 & 4T^3 & 5T^4 \\
      0 & 0 & 2 & 6T & 12T^2 & 20T^3
      \end{bmatrix}
      \begin{bmatrix} a_0 \\ a_1 \\ a_2 \\ a_3 \\ a_4 \\ a_5 \end{bmatrix}
      =
      \begin{bmatrix} s(0) = 0 \\ v(0) = 8 \\ a(0) = 0 \\ s(T) = 19.5 \\
      v(T) = 3.46 \\ a(T) = 0 \end{bmatrix}

   1. The first three rows give :math:`a_0 = 0`, :math:`a_1 = 8`,
      :math:`a_2 = 0` at once.
   2. The last three, solved: :math:`a_5 = 0`, because :math:`D` is the
      average of the two speeds times :math:`T`. Then :math:`a(T) = 0`
      gives :math:`a_3 = -2a_4T`, and :math:`v(T) = 3.46` gives
      :math:`a_4 = 4.54 / (2 \times 3.41^3) = 0.0573`, so
      :math:`a_3 = -2 \times 0.0573 \times 3.41 = -0.391`.
   3. Then :math:`a(t) = 6a_3 t + 12 a_4 t^2` is largest in size at
      :math:`t = T/2`: :math:`1.5\,\Delta v / T = 1.5 \times 4.54 / 3.41 =
      2.0` m/s².


.. _l10-lec-traj-jerk:

Score Comfort with Jerk: Werling's Cost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Jerk
   :class: note

   The rate of change of acceleration, in m/s³. Passengers feel a jump in
   acceleration as a jolt; a small jerk feels smooth.

Werling et al.: "ease and comfort can be best described by the jerk". Each
direction gets three terms (Werling et al., 2010), each weighted by a
number :math:`k` (all 1 here, chosen):

.. math::
   C_d = k_j \!\int_0^{T}\! \dddot d^{\,2}\,dt \;+\; k_t\,T \;+\;
   k_d\,(d_1 - d_\text{lane})^2
   \qquad
   C_s = k_j \!\int_0^{T}\! \dddot s^{\,2}\,dt \;+\; k_t\,T \;+\;
   k_{\dot s}\,(\dot s_1 - \dot s_\text{d})^2

- The squared jerk, added up over the maneuver: comfort. A quintic gives the
  least for given end states, which is why the polynomials are quintics
  (their Proposition 1).
- :math:`T`: a slow maneuver costs more.
- The end: :math:`d_\text{lane}` is the center of the lane the behavior
  layer picks (3.5 m, the left lane, to pass); :math:`\dot s_\text{d}` is
  the speed it asks for, 10 m/s. A stop is scored with end speed 0.

The total is :math:`C_d + C_s`; the cheapest candidate that passes the
checks wins.


.. _l10-lec-traj-check:

Check Each Candidate at Its Own Time: 45 of 324 Are Kept
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/traj_first_plan.png
   :alt: A graph, d against s, with the right lane yellow and the left lane purple. The black AV at s = 60 meters, the blue parked car in the right lane at 118 meters, car B's blue icon at the left edge of the left lane. A fan of 324 lines leaves the AV. Every line that reaches the left lane is orange-red or dashed purple. In the right lane, gray lines end between about 105 and 110 meters, and one thick green line rises slightly to d = 0.5 and runs to about 110 meters. Orange-red lines in the right lane run on past 120 meters.
   :width: 85%
   :align: center

   The first plan: 45 of 324 candidates kept after the checks.

.. admonition:: Reading the figure
   :class: tip

   - Every candidate line that reaches the left lane (orange-red solid, or
     purple dashed) is dropped: it collides or turns too hard.
   - Gray lines stay in the right lane and are kept; the thick green line is
     the cheapest of them.

Checks, at a point every 0.1 s for 7 s: the acceleration along the road
within ±2.0 m/s² (chosen) and across within 3 m/s² (last class's comfort
limit); the circle gap at least 0.3 m, to the parked car and to **car B
where prediction puts it at that same moment**.

- 54 too hard; 90 hit the parked car; 135 hit car B: every one that ends in
  the left lane.
- A graph with no time: a line into car B's lane is dropped only if the AV
  is there when car B is.

.. dropdown:: More detail: score the cheapest by hand, stay and slow to 6 m/s
   :class-container: more-detail
   :icon: info
   :name: l10-more-score-by-hand

   The cheapest kept candidate: :math:`d_1 = 0.5` m in :math:`T = 3` s; slow
   to :math:`\dot s_1 = 6` m/s in :math:`T = 4` s. Both start at rest across
   the road and at 10 m/s along it, with no acceleration.

   .. rubric:: Across the road, Cd

   1. Jerk: from rest to rest, the integral is :math:`720\,d_1^2/T^5`:
      720 × 0.25 / 243 = 0.74.
   2. Time: 3.
   3. End: :math:`(0.5 - 3.5)^2 = 9`.
   4. :math:`C_d` = 0.74 + 3 + 9 = 12.74.

   .. rubric:: Along the road, Cs

   1. Jerk: for a speed change :math:`\Delta v` with no acceleration at
      either end, the integral is :math:`12\,\Delta v^2/T^3`:
      12 × 16 / 64 = 3.00.
   2. Time: 4.
   3. End: :math:`(6 - 10)^2 = 16`.
   4. :math:`C_s` = 3 + 4 + 16 = 23.00.

   Total 12.74 + 23.00 = 35.74. The behavior layer asks for the left lane,
   and the cost would pay for it, but every candidate into the left lane
   hits car B: the cheapest left now is to slow down and wait in the lane,
   edging 0.5 m toward the lane line.


.. _l10-lec-traj-replan:

Plan Again Every 0.5 s: Wait for Car B, Then Pass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/traj_drive.png
   :alt: Three top views of the road, to scale, dark tags 1 to 3, each with the AV in black, car B and the parked car in blue, a dotted line where the AV has been and a thick green line for its plan. 1: car B beside the AV in the left lane; the green plan stays in the right lane and ends with a short bar well before the parked car. 2: car B level with the AV; the green plan curves into the left lane. 3: the AV in the left lane beside the parked car; car B far ahead; the green plan goes on along the left lane.
   :width: 70%
   :align: center

   Three moments of the drive: wait behind car B, then pass.

.. admonition:: Reading the figure
   :class: tip

   - **1:** car B is beside the AV; the plan (green) stays in the lane and
     stops short of the parked car.
   - **2:** car B is level with the AV; the plan curves into the left lane.
   - **3:** the AV is beside the parked car, in the left lane; car B is far
     ahead.

The AV drives the first 0.5 s of the cheapest candidate, then plans again
from where it is.

- :math:`t` = 2.0 s: car B beside the AV. All 27 kept stay in the lane; the
  cheapest stops at 110.15 m (cost 121.43).
- :math:`t` = 2.5 s: car B level with the AV and 5 m/s faster. The cheapest
  goes left behind it, back to 10 m/s (cost 14.78). The AV crosses the lane
  line at 5.1 s, 20 m behind car B.
- :math:`t` = 7.0 s: beside the parked car, 3.12 m left of the right lane's
  center.

Lowest speed 7.00 m/s; smallest gaps 0.93 m to the parked car, 0.48 m to car
B. Back on the right lane's center at :math:`s` = 181 m, once the behavior
layer picks it again (5 m past the parked car, chosen).


.. _l10-lec-traj-summary:

Where Trajectory Generation Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where trajectory generation leaves us
   :class: tip

   - **A trajectory is a path with times.** The same path at 10 m/s meets
     car B; slowed to 7 m/s first, it passes 1.04 m behind it.
   - **Two one-dimensional plans:** a quintic :math:`d(t)` across; a
     quartic :math:`s(t)` to keep a speed, a quintic to stop at a point.
     18 × 18 = 324 pairs.
   - **Checked in time:** each candidate against car B where prediction puts
     it at the same moment. At the start, all 135 into the left lane hit
     car B.
   - **Scored for comfort:** squared jerk, time and the end state (Werling
     et al.). Planned again every 0.5 s, the AV slows to 7.00 m/s, lets car
     B pass and goes around the parked car; last class's planner waited.


.. _l10-lec-control-interface:

Control-to-Actuator Interface
-------------------------------

The trajectory planner hands the controller where to be and when. Before we
build controllers, we follow one of their commands to the wheels: the
planner is set aside, and the next sections use what this one finds.

**In this section:** drive-by-wire, and how long the chain takes from the
command to the wheel.

**What it is for:** our simulation delays the steering by 0.1 s and lags it
by 0.2 s; this section shows where such numbers come from, and why every
controller today must live with them.


.. _l10-lec-actuators:

Let a Computer Drive: Drive-by-Wire Actuators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Drive-by-wire
   :class: note

   Electronic signals replace the mechanical links between the driver's
   controls and the actuators: a computer can then steer, accelerate and
   brake.

.. list-table::
   :widths: 34 33 33
   :header-rows: 1
   :class: compact-table

   * - **Electronic power steering**
     - **Electronic throttle**
     - **Brake-by-wire**
   * - an electric motor on the steering column or rack
     - a motor sets the throttle plate (or the electric motor's torque)
     - electro-hydraulic valves; an EV also brakes with its motor
   * - takes an angle or a torque
     - takes a torque or a pedal position
     - takes a pressure or a deceleration

- The motors have limits. Apollo's Lincoln MKZ file allows the steering
  wheel 6.98 rad/s, 6.98 × 180 / :math:`\pi` = 400 °/s; with a steering
  ratio of 16, 400 / 16 = 25 °/s at the road wheels (a configuration value,
  not a measurement).

.. _l10-lec-command-chain:

Follow One Steering Command: from the Program to the Motor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On a Lincoln MKZ research car, Xu et al. trace the steering command:
"generated by the control app, checked by the Mcity safeguard module,
sent to the by-wire control ROS driver, USB-CAN ROS driver, USB-CAN tool,
Dataspeed steering module, the onboard CAN network, steering system and
finally the power steering motor actuates the front tires" (Xu et al.,
2021).

.. admonition:: Definition: Controller Area Network (CAN)
   :class: note

   The serial bus a car's control units share. Each message, a frame,
   carries an identifier and from 0 to 8 bytes of data (Bosch, 1991).

- Identifier: 11 bits (29 in the extended format). It sets the message's
  priority.
- Two units send at once: bit by bit, a 0 overrides a 1, and the unit
  that sent the 1 stops. So the lower identifier wins.
- A 15-bit check code (CRC) lets the receiver catch a corrupted frame.
- Bosch: CAN runs "with bitrates up to 1 Mbit/s" in automotive
  electronics.

.. _l10-lec-ecus:

Execute a Command: the Electronic Control Units
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An ECU (electronic control unit) is an embedded computer that runs one
subsystem. It takes commands from the CAN bus and turns them into
actuator signals (solid arrows: commands; dashed: feedback).

What it does with each command:

1. receive it from the CAN bus;
2. check it (range, rate, safety);
3. drive the actuator;
4. read its own sensors;
5. send feedback back on the CAN bus.

The ones a controller talks to: the steering ECU (power steering motor),
the engine or motor ECU (throttle) and the brake ECU (valves, ABS,
stability control).

.. figure:: /_static/images/L10/ecu_chain.png
   :alt: A block diagram from top to bottom. A gray box, Driving computer, planning and control. Below it a box, CAN bus: a solid arrow labeled command goes down to it and a dashed arrow labeled feedback goes up from it. Below that a green box, Electronic control units (ECUs), with the same pair of arrows from the CAN bus. At the bottom left a box, Actuator, reached by a solid arrow labeled drive from the ECUs; at the bottom right a box, Sensor, with a dashed arrow labeled reading up into the ECUs.
   :width: 45%
   :align: center

   One command's path through the car.

.. admonition:: Reading the figure
   :class: tip

   Solid arrows carry commands down; dashed arrows carry feedback up. The
   driving computer sends a command over the CAN bus to the ECUs; an ECU
   drives its actuator and reads its sensor, then sends feedback back up
   the same bus.

.. _l10-lec-can:

Share One Bus: Commands and Feedback on CAN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/can_bus.png
   :alt: A diagram. A thick horizontal line, the CAN bus (example: 500 kbit/s). Above it a gray box, Driving computer, planning and control, sends a solid arrow labeled command down to the bus and gets a dashed arrow labeled feedback back up. Below the bus three green boxes, each with a solid arrow down from the bus and a dashed arrow up to it: Steering ECU (command: angle or torque; feedback: angle, torque, status), Throttle ECU (command: pedal percent; feedback: position, engine speed) and Brake ECU (command: pressure or deceleration; feedback: pressure, wheel speed, ABS). Under each ECU a white box, joined the same way: EPS motor and its angle sensor, Throttle body and its position sensor, Brake actuator and its pressure sensor.
   :width: 80%
   :align: center

   Three ECUs on one CAN bus.

.. admonition:: Reading the figure
   :class: tip

   The thick line is the bus. Each ECU takes its command from the bus
   (solid arrow down) and puts its feedback on it (dashed arrow up). Under
   each ECU, its actuator with the sensor that reports back: the electric
   power steering (EPS) motor, the throttle body and the brake actuator.

One bus carries the commands down (solid arrows) and the feedback up
(dashed). The 500 kbit/s is
an example rate; the Bosch specification allows "bitrates up to 1
Mbit/s" (Bosch, 1991).

.. _l10-lec-can-layout:

Pack a Steering Command into 8 Bytes: an Example Layout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An example layout of one steering command in the 8 data bytes (chosen for
the example; each car maker defines its own):

.. list-table::
   :widths: 10 10 22 30 28
   :header-rows: 1
   :class: compact-table

   * - **Byte**
     - **Bits**
     - **Signal**
     - **Scale, offset**
     - **Range**
   * - 0 to 1
     - 0 to 15
     - steering angle
     - 0.01°, -327.68°
     - ±327.67°
   * - 2 to 3
     - 0 to 15
     - steering rate
     - 0.1 °/s, 0
     - 0 to 6553.5 °/s
   * - 4
     - 0 to 1
     - enable flag
     - on or off
     - 0 or 1
   * - 4
     - 2 to 3
     - control mode
     - angle or torque
     - 0 or 1
   * - 5 to 6
     - 0 to 15
     - torque command
     - 0.01 N m, -327.68
     - ±327.67 N m
   * - 7
     - 0 to 3
     - rolling counter
     - +1 per message
     - 0 to 15

1. A 16-bit field holds 0 to 65535. Angle = raw × 0.01 - 327.68: raw 0
   gives -327.68°, raw 65535 gives 327.67°.
2. The rolling counter goes up by one with every message, so the
   receiver can tell a message was missed.

.. _l10-lec-delay:

Measure the Chain's Delay: the Wheel Turns 0.2 s after the Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Xu et al. sent the MKZ a step in the steering command and watched the wheel
(Xu et al., 2021):

1. "The steering wheel starts to rotate roughly 0.2 s after the command
   :math:`\delta` is delivered": a **delay** of 0.2 s.
2. Then the angle catches up gradually, as a first-order **lag**; a time
   constant of 0.2 s fits the measured angle.

.. list-table::
   :widths: 46 18 36
   :header-rows: 1
   :class: compact-table

   * - **Steering model**
     - **Delay**
     - **Lag (time constant)**
   * - MKZ research car, measured
     - 0.2 s
     - 0.2 s
   * - Autoware's MPC, default values (no vehicle named)
     - 0.24 s
     - 0.27 s
   * - Our simulation (chosen)
     - 0.1 s
     - 0.2 s

.. important::

   During a 0.2 s delay at 8 m/s the AV drives 8 × 0.2 = 1.6 m on its old
   steering. A controller that ignores this steers late; in the Lateral
   section, the delay and the lag make the AV weave when the lookahead is
   short.


.. _l10-lec-fail-safe:

Fail Safe: What the Chain Checks Before It Moves the Car
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Message integrity**

- the 15-bit CRC of every CAN frame (Bosch, 1991);
- a rolling counter catches missed messages.

**Command checks**

- against physical limits (angle, rate);
- reject sequences that make no sense.

**Watchdog (heartbeat)**

- no valid command in time: fail safe;
- give control back to the driver, or stop safely.

**Enable protocol**

- a valid heartbeat first;
- the vehicle in a fitting state, with no active fault.

Our lock step is a watchdog of its own: the node that steps CARLA waits
for each command; if the controller does not answer, the simulation does
not advance.

.. _l10-lec-turn:

The Turn
--------

The behavior layer picks a behavior and a target speed for it, for example
8 m/s to keep the lane and 0 to stop at the line (chosen). This section sets
that choice aside and builds the one example that every controller, steering
and speed, runs on.

**In this section:** we take one right turn in Town03, find its curvature,
and give it a speed profile.

**What it is for:** every controller today drives this same path, at the
same speeds, from the same start, so their results can be compared.


.. _l10-lec-test-path:

One Test Path for Every Controller: a Right Turn in Town03
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/turn_map.png
   :alt: A top view, x along the approach to the right and y to the left, in meters. A single lane 3.5 meters wide, drawn by two black edges with a gray dashed center line, runs 80 meters to the right, turns right through a quarter circle near x = 80 to 92, and runs 40 meters down. The AV is drawn at the start, at the left end, facing right. An arrow under the lane says driving direction. Dark round tags: tag 1 above the straight approach, tag 2 at the corner, which is shaded orange along the center line, tag 3 beside the exit going down.
   :width: 90%
   :align: center

   The test path: a right turn in Town03.

.. admonition:: Reading the figure
   :class: tip

   A top view in meters, drawn turned so the approach points along
   :math:`x`; :math:`y` points to the left. The lane is 3.5 m wide; the
   dashed line is its center. The AV starts at the left end, facing right.

   - **Tag 1:** road 3, the 80 m approach.
   - **Tag 2:** road 817, the junction lane: 17.5 m, turning right by 91°
     (shaded orange).
   - **Tag 3:** road 19, the 40 m exit.

The lane was read from ``Town03.xodr`` with ``carla.Map``, with no CARLA
server running.

Our path is the lane center, as the route planner gives it. Our controller
follows that path, with no local planner in between.


.. _l10-lec-curvature:

Measure How the Turn Bends: Its Curvature Jumps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Curvature
   :class: note

   How sharply a path bends at a point: :math:`\kappa = 1/R`, where
   :math:`R` is the radius of the circle that fits the path there. A
   straight road has :math:`\kappa = 0`.

.. figure:: /_static/images/L10/turn_curvature.png
   :alt: A graph, not a map: curvature in 1 per meter against the distance along the path from 0 to 137.5 meters. The curve is zero up to about 83 meters, jumps to 0.100 (dark tag 1), jumps again near 89.5 meters to 0.167 (dark tag 2), and drops back to zero near 95 meters. The junction lane, from 80 to 97.5 meters, is shaded orange.
   :width: 80%
   :align: center

   The curvature of the test path.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a map: the curvature against the distance :math:`s` along
   the path. The junction lane is shaded orange.

   - **Tag 1:** the first arc, :math:`\kappa` = 0.1000 /m, so
     :math:`R` = 1 / 0.1000 = 10.00 m.
   - **Tag 2:** the second arc, :math:`\kappa` = 0.1673 /m, so
     :math:`R` = 1 / 0.1673 = 5.98 m.

   Each change is a step, with no gradual part between.


.. _l10-lec-profile-1:

Speed Profile, Step 1: a Curve Caps the Speed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Lateral acceleration
   :class: note

   On a circle of radius :math:`R` at speed :math:`v`, the AV accelerates
   toward the circle's center by :math:`v^2 / R` (m/s²). The tires must push
   the AV sideways that hard; the faster or the tighter the curve, the
   harder.

We cap it at :math:`a_{\mathrm{lat}}` = 2.0 m/s² (chosen; the controller
node's ``a_lat``, a cap the node applies itself). From
:math:`v^2 / R \le a_{\mathrm{lat}}`, the highest speed in a curve is
:math:`v = \sqrt{a_{\mathrm{lat}} R}`:

1. First arc, :math:`R` = 10.00 m: :math:`\sqrt{2.0 \times 10.00}` =
   4.47 m/s.
2. Second arc, :math:`R` = 5.98 m: :math:`\sqrt{2.0 \times 5.98}` =
   3.46 m/s.
3. Everywhere else: 8 m/s, the target speed (chosen).

These caps are the speed limit at each point, the dotted line in the next
figure.


.. _l10-lec-profile-2:

Speed Profile, Step 2: Brake Before the Curve, Speed Up After It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/speed_profile.png
   :alt: A graph of speed in meters per second against the distance along the path. A dotted gray limit line sits at 8, drops to about 4.5 on the first arc and 3.46 on the second, and returns to 8. The blue profile holds 8, falls along a curve from about 72 meters (dark tag 1), holds 4.47 on the first arc (tag 2) and 3.46 on the second (tag 3), then rises back to 8 by about 112 meters (tag 4). The junction lane is shaded orange.
   :width: 85%
   :align: center

   The speed profile on the test path.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a map: the speed against the distance :math:`s` along the
   path. The dotted gray line is the limit from Step 1; the blue line is the
   profile. The junction lane is shaded orange.

   - **Tag 1:** braking, before the first arc.
   - **Tag 2:** the first arc's cap, 4.47 m/s.
   - **Tag 3:** the second arc's cap, 3.46 m/s.
   - **Tag 4:** speeding up again, after the second arc.

The AV cannot drop to 4.47 m/s at once: slowing from :math:`v_1` to
:math:`v_2` at a constant deceleration :math:`a` takes the distance
:math:`d = (v_1^2 - v_2^2) / (2a)`.

1. Braking (tag 1), at 2.0 m/s² (chosen; the node's ``a_brake``):
   :math:`d = (8^2 - 4.47^2) / (2 \times 2.0)` = 11.0 m. The first arc
   starts at :math:`s` = 83.2 m, so braking starts at 83.2 minus 11.0,
   which is 72.2 m.
2. Speeding up (tag 4), at 1.5 m/s² (chosen), from 3.46 m/s after the
   second arc ends at :math:`s` = 94.8 m:
   :math:`(8^2 - 3.46^2) / (2 \times 1.5)` = 17.3 m, so the AV is at 8 m/s
   again at 94.8 plus 17.3, which is 112.1 m.


.. _l10-lec-simulation:

Test Controllers Without CARLA: Our Simulation and Its Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every controller today drives this path in a numpy simulation of the
bicycle model (next section). The values:

.. list-table::
   :widths: 28 24 48
   :header-rows: 1
   :class: compact-table

   * - **Value**
     - **Number**
     - **From**
   * - Wheelbase :math:`L`
     - 2.875 m
     - chosen; a real vehicle has its own (2.3 to 3.0 m)
   * - Largest steering angle
     - 0.7 rad
     - chosen: the most the controller commands (``steer_limit``; the
       wheels can turn 1.222 rad)
   * - Steering: delay, then lag
     - 0.1 s, then 0.2 s
     - chosen: real steering is not instant
   * - Controller rate
     - 20 per second
     - set by the lock step
   * - Start
     - 1 m left of center, 8 m/s
     - chosen, to see the AV correct
   * - Speed model
     - see :ref:`Longitudinal Control <l10-lec-speed>`
     - chosen

.. important::

   These are not CARLA's dynamics. The numbers show how each controller
   behaves; tune the gains on CARLA itself.


.. _l10-lec-vehicle-modeling:

Vehicle Modeling
----------------

The last section gave a path, its speed profile and a simulation to drive
them. This section keeps all three and opens up the simulation's model.

**In this section:** the kinematic bicycle model says where a steering angle
and a speed take the AV.

**What it is for:** every controller today predicts with this model, and our
simulation runs it.


.. _l10-lec-ackermann:

Turn Four Wheels About One Point: Ackermann Steering Geometry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a four-wheeled vehicle turns, every wheel should roll around one common
point, the instantaneous center of rotation (ICR). A wheel that does not
point square to the line to the ICR slides sideways: a tire scrub.

.. figure:: /_static/images/L10/l7_ackermann.png
   :alt: A top view of a car turning left, drawn in light gray with its four wheels in blue, in an X Y frame. Dashed lines run from each front wheel to a red point labeled ICR at the top left; the angles between the lines at the ICR are labeled delta o and delta i. The front wheels are turned by delta i and delta o. A line from the ICR to the rear axle's middle is labeled R; the wheelbase is labeled L and the track W; the center of gravity is marked CG.
   :width: 55%
   :align: center

   Ackermann steering geometry.

*Figure: Theers and Singh (2026), CC BY 4.0.*

.. admonition:: Reading the figure
   :class: tip

   A top view of a car turning left, with its four wheels in blue. Dashed
   lines run from each front wheel to the ICR (red), at the top left.

   - The angle at the ICR between the two dashed lines, split into
     :math:`\delta_o` (to the outer front wheel) and :math:`\delta_i` (to
     the inner front wheel); the front wheels are turned by these angles.
   - :math:`R`: the line from the ICR to the rear axle's middle.
   - :math:`L`: the wheelbase. :math:`W`: the track (left wheel to right
     wheel). CG: the center of gravity.

- **Inner wheel:** the one on the inside of the turn, closer to the ICR (the
  left front wheel in a left turn).
- It rolls on a smaller circle, so it steers more: "the inner wheel has a
  bigger steer angle than the outer wheel, because is closer to the centre
  of rotation" (Moldovanu et al., 2019).
- :math:`L`: wheelbase. :math:`W`: track. :math:`R`: turn radius, to the
  rear axle's middle.


.. _l10-lec-bicycle-collapse:

Collapse Four Wheels into Two: the Bicycle Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A controller sends **one** angle; the linkage turns the inner and outer
wheels to about :math:`\delta_i` and :math:`\delta_o`. CARLA too takes one
``steer`` angle (CARLA Team, 2026).

The bicycle model "simplifies the four wheel car by combining the two front
wheels together and the two rear wheels together to form a two wheeled
model, like a bicycle" (Snider, 2009).

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Kept**
     - **Dropped**
   * - the ICR
     - each wheel's own angle
   * - the turn radius :math:`R`
     - the track :math:`W`
   * - the path's shape
     - inner and outer

.. figure:: /_static/images/L10/l7_bicycle.png
   :alt: The same turning car as on the Ackermann slide, drawn in light gray in an X Y frame, now with one blue front wheel and one blue rear wheel on the car's center line. A dashed line from the front wheel and one from the rear wheel meet at a red point labeled ICR; the angle between them is delta. R runs from the ICR to the rear wheel; the wheelbase is L; the heading theta is drawn at the rear wheel, and the direction (cos theta, sin theta) is labeled in pink.
   :width: 55%
   :align: center

   The same car, collapsed to the bicycle model.

*Figure: Theers and Singh (2026), CC BY 4.0.*

.. admonition:: Reading the figure
   :class: tip

   The same car as the Ackermann figure, now with one front wheel and one
   rear wheel on the car's center line (blue). Dashed lines from each wheel
   meet at the ICR (red); the angle between them is :math:`\delta`.

   - :math:`R`: from the ICR to the rear wheel. :math:`L`: the wheelbase.
   - :math:`\theta`: the heading, drawn at the rear wheel; the direction
     :math:`(\cos\theta, \sin\theta)` is labeled in pink.

The one angle that gives the same :math:`R`:
:math:`\delta = \arctan(L/R)`; for our first arc, 0.280 rad, between the
Ackermann angles :math:`\delta_o` = 0.260 and :math:`\delta_i` = 0.303 rad.

.. dropdown:: More detail: Ackermann's two wheel angles, and why the controller skips them
   :class-container: more-detail
   :icon: info
   :name: l10-more-ackermann

   .. rubric:: Compute the Two Wheel Angles: the Ackermann Condition

   On a turn, the inner front wheel is closer to the turning center, so it
   must steer more. The **Ackermann condition** ties the two angles, with
   :math:`w` the track (from left wheel to right wheel) and :math:`l` the
   wheelbase (Moldovanu et al., 2019):

   .. math::

      \cot\delta_o - \cot\delta_i = \frac{w}{l}

   Our turn's first arc, :math:`R` = 10.00 m to the rear axle's middle,
   :math:`l` = 2.875 m, :math:`w` = 1.6 m (chosen):

   1. Inner wheel, :math:`R - w/2` = 9.2 m from the center:
      :math:`\delta_i = \arctan(2.875 / 9.2)` = 0.303 rad.
   2. Outer wheel, :math:`R + w/2` = 10.8 m:
      :math:`\delta_o = \arctan(2.875 / 10.8)` = 0.260 rad.
   3. Check: :math:`10.8/2.875 - 9.2/2.875 = 1.6/2.875 = w/l`.

   .. important::

      The controller sends one angle; the steering linkage turns the two
      wheels. The bicycle model simplifies the four wheel car into two
      wheels: one wheel at :math:`\arctan(2.875/10)` = 0.280 rad, between
      the two.

   .. rubric:: Send One Angle, Not Two: Why the Controller Does Not Use Ackermann

   A controller outputs **one** steering command; Ackermann geometry has
   **two** angles, :math:`\delta_i \ne \delta_o`, and which wheel is inner
   changes with the turn's direction.

   .. list-table::
      :widths: 30 70
      :header-rows: 1
      :class: compact-table

      * - **Layer**
        - **What it does**
      * - Controller
        - outputs one angle :math:`\delta`
      * - Steering ECU
        - turns :math:`\delta` into a motor command
      * - Steering linkage
        - turns the two wheels to about :math:`\delta_i` and :math:`\delta_o`

   - The linkage does it only approximately: "there is no four-bar mechanism
     that can fulfill the Ackerman condition perfectly" (Peñuñuri et al.,
     2011).
   - CARLA does the same: ``VehicleAckermannControl`` takes one ``steer``
     angle, in rad (CARLA Team, 2026).

   So the controller uses the bicycle model: both front wheels collapse
   into one, with one angle.


.. _l10-lec-bicycle-def:

Predict the AV's Motion: the Bicycle Model, One Wheel per Axle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Kinematic bicycle model
   :class: note

   The AV's two front wheels merged into one, and its two rear wheels into
   one. The wheels roll without sliding sideways, so the AV turns about one
   point.

.. figure:: /_static/images/L10/bicycle_geom.png
   :alt: A drawing of the bicycle model. The rear wheel at dark tag 1 and the front wheel at dark tag 2 are short thick bars joined by a line of length L, tilted up to the right at angle theta from a dashed horizontal line. The front wheel is turned further left by the angle delta from the body line. Thin gray lines from both wheels, square to each wheel, meet far up and to the left at a green point, dark tag 3; a green double arrow labeled R runs from the rear wheel to that point. A dashed green arc leaves the rear wheel toward the front. A faint gray top view of the AV lies under the model, facing along the body line, with its rear axle on the rear wheel. Small x and y axes sit at the bottom left, off the car.
   :width: 55%
   :align: center

   The kinematic bicycle model, drawn over the AV.

.. admonition:: Reading the figure
   :class: tip

   The faint gray AV lies under the model, facing along the body line. The
   body line, of length :math:`L`, is turned by the heading :math:`\theta`
   from the :math:`x` axis (the dashed horizontal line). The thin gray lines
   are square to each wheel.

   - **Tag 1:** the rear axle: the AV's position (the base link).
   - **Tag 2:** the front axle, :math:`L` = 2.875 m (chosen) ahead, turned
     by :math:`\delta` from the body line.
   - **Tag 3:** the point the AV turns about, where the two gray lines meet.
     The rear axle drives a circle of radius :math:`R` around it (the green
     dashed arc).


.. _l10-lec-bicycle-eq:

Write the Model: the State, the Inputs and Four Equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**State**, at the rear axle: the configuration, position :math:`x, y` (m)
and heading :math:`\theta` (rad, counterclockwise from :math:`x`), plus the
speed :math:`v` (m/s). **Inputs:** the front wheel angle :math:`\delta`
(rad, positive turns left) and the acceleration :math:`a` (m/s²).

.. math::

   \dot x = v\cos\theta, \qquad \dot y = v \sin\theta, \qquad
   \dot\theta = \frac{v}{L}\tan\delta, \qquad \dot v = a

- The first two: the rear axle moves along the heading.
- The third: the turn rate grows with speed and with steering. This is where
  the steering enters.
- An EKF predicts with the gyro's measured turn rate instead; here the turn
  rate comes from :math:`\delta`, because a controller chooses
  :math:`\delta`.

.. dropdown:: More detail: why tan δ = L/R
   :class-container: more-detail
   :icon: info
   :name: l10-more-bicycle-tan

   .. figure:: /_static/images/L10/bicycle_geom.png
      :alt: The bicycle model drawing again, with dark round tags: rear wheel at tag 1, front wheel at tag 2 turned by delta, the point the AV turns about at tag 3, the radius R from the rear wheel to that point, and the wheelbase L between the wheels.
      :width: 45%
      :align: center

      The bicycle model, from the lecture above.

   .. admonition:: Reading the figure
      :class: tip

      The same drawing as above. The thin gray lines are square to each
      wheel.

      - **Tag 1:** the rear wheel.
      - **Tag 2:** the front wheel, turned by :math:`\delta`; the body line
        between the wheels has length :math:`L`.
      - **Tag 3:** the point the AV turns about; the green double arrow from
        the rear wheel to it is :math:`R`.

   1. No wheel slides sideways, so each wheel moves along its own direction.
      Its turning center lies on the line through it, square to the wheel.
   2. The rear wheel points along the body: its line is square to the body,
      through tag 1.
   3. The front wheel is turned by :math:`\delta`: its line is turned by
      :math:`\delta` too. The two lines meet at tag 3.
   4. The triangle (tag 1, tag 2, tag 3) has a right angle at tag 1, the
      side :math:`L` along the body and the side :math:`R` to tag 3. Its
      angle at tag 3 is :math:`\delta`, so :math:`\tan\delta = L/R`.
   5. The rear axle moves at :math:`v` on a circle of radius :math:`R`: it
      turns at :math:`v/R = v\tan\delta / L`, the model's third equation.


.. _l10-lec-steer-curvature:

Steer for a Curvature: a Fixed Angle Drives a Circle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hold :math:`\delta` and the AV drives a circle of radius
:math:`R = L / \tan\delta`. So, to follow a curvature :math:`\kappa = 1/R`,
steer :math:`\delta = \arctan(L\kappa)`.

1. First arc: :math:`\delta = \arctan(2.875 \times 0.1000) = \arctan(0.288)`
   = 0.280 rad (16.0°).
2. Second arc:
   :math:`\delta = \arctan(2.875 \times 0.1673) = \arctan(0.481)` =
   0.448 rad (25.7°).
3. The controller's steering limit, 0.7 rad (``steer_limit``): the smallest
   circle is :math:`R = 2.875 / \tan 0.7` = 3.41 m.

.. important::

   Both arcs are within reach: 0.448 rad is under the 0.7 rad limit. A
   corner tighter than :math:`R` = 3.41 m would not be.

.. dropdown:: More detail: where the model stops holding
   :class-container: more-detail
   :icon: info
   :name: l10-more-model-limits

   - The model assumes the tires roll where they point. A real tire slides
     a little sideways when it carries a sideways force, and more as the
     force grows.
   - So the model holds while the sideways acceleration :math:`v^2\kappa`
     stays small. Here we take the limit as half of gravity's pull, 0.5 g
     (chosen for this example): 0.5 × 9.81 = 4.9 m/s².
   - Our profile caps it at 2.0 m/s²: on the second arc,
     :math:`3.46^2 \times 0.1673` = 2.0 m/s².
   - Beyond that, the **dynamic** bicycle model adds the tire forces, below.

.. dropdown:: More detail: check the model by hand, one step on the second arc
   :class-container: more-detail
   :icon: info
   :name: l10-more-bike-step

   The AV on the second arc: :math:`v` = 3.458 m/s, :math:`\delta` =
   0.448 rad (the angle this arc needs, from the steps above), one
   controller step :math:`\Delta t` = 0.05 s. We measure from the AV
   itself: :math:`x = y = 0`, :math:`\theta = 0`.

   1. Forward:
      :math:`\Delta x = v\cos\theta\,\Delta t = 3.458 \times 1 \times 0.05`
      = 0.173 m.
   2. Sideways:
      :math:`\Delta y = v\sin\theta\,\Delta t = 3.458 \times 0 \times 0.05`
      = 0 m.
   3. Turn: :math:`\Delta\theta = \frac{v}{L}\tan\delta\,\Delta t =
      \frac{3.458}{2.875} \times 0.481 \times 0.05` = 0.0289 rad.

   Twenty such steps (1 s) turn the AV by 20 × 0.0289 = 0.578 rad, about
   33°. The next step starts from the new heading, so the AV moves sideways
   from step 2 on.


.. _l10-lec-model-stops:

Know Where the Model Stops: Tires Slide at High Sideways Acceleration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The model assumes each wheel rolls where it points. A real tire slides a
little sideways when it carries a sideways force, and more as the force
grows.

- Polack et al. compared the model with a 9-degree-of-freedom vehicle in
  simulation: keep the sideways acceleration "lower than 0.5 μg" (Polack et
  al., 2017). On a dry road (:math:`\mu` = 1): 0.5 × 9.81 = 4.9 m/s².
- Our profile caps it at 2.0 m/s²: on the second arc,
  :math:`3.46^2 \times 0.1673 = 2.0` m/s², well inside.
- Kong et al. drove a car with an MPC built on this model: 0.41 m mean error
  on a test path at 10 m/s, 1.08 m at 15 m/s. "When the lateral acceleration
  grows larger, it becomes more critical to use a model which takes into
  consideration slip, such as a dynamic bicycle model" (Kong et al., 2015).

.. important::

   A speed alone does not set the limit: the sideways acceleration is
   :math:`v^2/R`, so a gentle curve allows more speed than a tight one.

.. dropdown:: More detail: the dynamic bicycle model, when tires slide
   :class-container: more-detail
   :icon: info
   :name: l10-more-dynamic

   .. rubric:: Let the Tires Slide: the Dynamic Bicycle Model

   At speed, a tire slides: its **slip angle** :math:`\alpha` is between
   where it points and where it moves. Snider's model (Snider, 2009), at
   the center of gravity (CG); :math:`v_x, v_y`: speed along and across the
   car; :math:`r`: yaw rate:

   .. math::

      \alpha_f = \tan^{-1}\frac{v_y + \ell_f r}{v_x} - \delta, \qquad
      \alpha_r = \tan^{-1}\frac{v_y - \ell_r r}{v_x}

   .. math::

      F_{yf} = -c_f\,\alpha_f, \qquad F_{yr} = -c_r\,\alpha_r

   .. figure:: /_static/images/L10/l7_dynamic.png
      :alt: A dynamic bicycle model drawn vertically: a front wheel at the top and a rear wheel at the bottom on a dotted center line, the CG between them, Lf above it and Lr below. At each wheel a blue arrow, Tire Heading, along the wheel and a green arrow v for the wheel's velocity, the angle between them alpha f at the front and alpha r at the rear; red arrows Fyf and Fyr point sideways. At the CG the velocity v splits into vx along and vy across, with the angle beta.
      :width: 28%
      :align: center

      The dynamic bicycle model, with slip angles and tire forces.

   .. admonition:: Reading the figure
      :class: tip

      Drawn vertically: the front wheel at the top, the rear wheel at the
      bottom, the CG between them, at distances :math:`\ell_f` and
      :math:`\ell_r`.

      - At each wheel, a blue arrow (tire heading) along the wheel and a
        green arrow :math:`v` for the wheel's velocity; the angle between
        them is :math:`\alpha_f` at the front and :math:`\alpha_r` at the
        rear. Red arrows :math:`F_{yf}` and :math:`F_{yr}` point sideways.
      - At the CG, the velocity :math:`v` splits into :math:`v_x` along the
        car and :math:`v_y` across it, with the angle :math:`\beta`.

   - Force proportional to slip; :math:`c_f, c_r`: each axle's cornering
     stiffness. Snider's car: 155,495 N/rad per axle (Snider, 2009); a
     Lincoln MKZ: 140,000 front, 120,000 N/rad rear (Xu et al., 2021).
   - :math:`v_x` is in a denominator: the model breaks at very low speed.

   .. rubric:: Write the Dynamic Model: One Force Balance and One Moment Balance

   Snider's force and moment balance (Snider, 2009), with no driving force
   on the front wheels:

   **Sideways:** what moves the car sideways

   .. math::

      m\,(\dot v_y + v_x r) = F_{yf}\cos\delta + F_{yr}

   - :math:`m\dot v_y`: mass times sideways acceleration.
   - :math:`m v_x r`: the term from the car's own rotation.
   - the two tire forces, the front one turned by :math:`\delta`.

   **Yaw:** what turns the car

   .. math::

      I_z\,\dot r = \ell_f F_{yf}\cos\delta - \ell_r F_{yr}

   - :math:`I_z\dot r`: yaw inertia times yaw acceleration.
   - the front force pushes the nose one way, the rear force the other.

   For design, these equations are linearized around the path and written
   in the errors: that is the model LQR uses (see "Sort the Steering
   Controllers", above).

   .. rubric:: Model the Tire Force: Linear, Pacejka, Friction Circle

   .. list-table::
      :widths: 24 38 38
      :header-rows: 1
      :class: compact-table

      * - **Model**
        - **In words**
        - **Where we met it**
      * - Linear
        - the sideways force is the cornering stiffness times the slip
          angle
        - Snider's dynamic model, LQR
      * - Pacejka's
        - the force rises with slip, peaks, then falls; it also couples
          braking and turning
        - Polack et al.'s 9-degree-of-freedom reference vehicle
      * - Friction circle
        - the total tire force cannot pass :math:`\mu` times the load:
          :math:`\lVert \vec F_x + \vec F_y\rVert \le \mu \lVert \vec
          F_z\rVert`
        - the same

   - Polack et al. model the tires with "the combined slip tire model
     presented by Pacejka", so "the friction circle due to the laws of
     friction" is respected (Polack et al., 2017).
   - The friction circle in words: a tire cannot brake hard and turn hard at
     the same time.

   .. rubric:: Choose the Model for the Conditions: Sideways Acceleration Decides

   .. list-table::
      :widths: 42 26 32
      :header-rows: 1
      :class: compact-table

      * - **Situation**
        - **Model**
        - **Source**
      * - slow driving, parking
        - kinematic
        - Snider, p. 65
      * - sideways acceleration under 0.5 μg
        - kinematic
        - Polack et al.
      * - highway, moderate speed on smooth roads
        - dynamic, linear tires
        - Snider, p. 65
      * - near the grip limit: hard braking while turning
        - combined-slip tires (Pacejka)
        - Polack et al.

   - Snider: "A simple kinematic model can suffice when a vehicle closely
     exhibits kinematic motion, such as driving slowly or performing
     parking maneuvers" (Snider, 2009).
   - The dynamic model "starts to break down at very slow speeds and/or
     tight steering angles": the speed sits in a denominator.
   - Our turn stays at 2.0 m/s² or less: the kinematic model fits.


.. admonition:: Where the bicycle model leaves us
   :class: tip

   - **State at the rear axle:** :math:`x, y, \theta, v`. **Inputs:**
     :math:`\delta`, :math:`a`. The turn rate is :math:`v\tan\delta / L`.
   - **Steering for a curvature:** :math:`\delta = \arctan(L\kappa)`:
     0.280 rad and 0.448 rad for our two arcs, under the 0.7 rad limit.
   - **Sideways acceleration** on our turn: at most 2.0 m/s², the profile's
     cap. Polack et al.: keep it under 0.5 μg, 4.9 m/s² on a dry road.

A 10-minute break follows in class.


.. _l10-lec-lateral:

Lateral Control
----------------

The vehicle model says how a steering angle moves the AV. This section
builds on it: the controllers that choose the angle. In every run a speed
PID (Longitudinal Control, next) holds the turn's speed profile.

**In this section:** two geometric controllers, Pure Pursuit and Stanley,
and a model-based one, MPC. PID on steering and LQR are covered only in the
"More detail" box below; we do not run them on our turn.

**What it is for:** the controller node steers with Pure Pursuit; Stanley
and MPC show what other choices gain and cost.


.. _l10-lec-lateral-overview:

Sort the Steering Controllers: Geometric, Feedback, Model-Based
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lateral control answers: how do I steer to stay on this path?

.. list-table::
   :widths: 33 33 34
   :header-rows: 1
   :class: compact-table

   * - **Geometric**
     - **Feedback**
     - **Model-based**
   * - steer from the path's shape
     - steer from the measured error
     - steer from a predicted response
   * - Pure Pursuit, Stanley
     - PID
     - LQR, MPC
   * - wheelbase only
     - no vehicle model
     - a dynamic (LQR) or kinematic (MPC) model

- Snider groups path trackers the same way: geometric, then model-based
  with a kinematic or a dynamic model (Snider, 2009); MPC on the kinematic
  model runs on a real car in Kong et al. (2015).
- Snider's verdict: "no method is perfect and all of the methods can work
  well in some applications" (Snider, 2009).

.. dropdown:: More detail: PID on steering, and LQR
   :class-container: more-detail
   :icon: info
   :name: l10-more-pid-lqr

   .. rubric:: PID on Steering

   A PID needs no model of the car: it steers from the cross-track error
   alone.

   .. rubric:: Steer from the Error Alone: PID on the Cross-Track Error

   .. math::

      \delta = K_p\, e + K_i \sum e\,\Delta t + K_d\, \frac{e_k - e_{k-1}}{\Delta t}

   - **P:** steer harder the farther from the path.
   - **I:** remove an offset that stays, such as in a long curve.
   - **D:** ease off as the error shrinks; damps the swing.

   **Strengths:** no vehicle model; the same three gains as the speed PID
   (Longitudinal Control).

   **Limits:** no look-ahead, so it reacts to the error now, not to the
   curve coming; the I term winds up while the steering sits at its limit,
   as the speed PID's did.

   We do not run it on our turn: the geometric controllers above already
   use the path ahead.

   .. rubric:: LQR

   Stanley adds two error terms with one gain. LQR weighs four error states
   at once, with gains computed from a dynamic model of the car.

   .. rubric:: Balance Error Against Effort: the Idea of LQR

   LQR finds the steering that balances two goals: small tracking errors
   and small steering. You say how much each matters; LQR computes the
   gains.

   1. Write a cost that penalizes the errors and the steering effort.
   2. Solve the Riccati equation for the gains :math:`K` (offline, once per
      speed).
   3. Steer with state feedback: a weighted sum of all four error states.

   A PID on steering uses only the cross-track error; LQR uses four states
   at once: the cross-track error and its rate, the heading error and its
   rate. "Linear quadratic": a linear model and a quadratic cost.

   .. rubric:: Weigh Four Errors with LQR: Steering is −K Times the Error

   Snider's linear quadratic regulator (LQR) (Snider, 2009):

   - The error state, at the center of gravity:
     :math:`x = [\,e,\ \dot e,\ \theta_e,\ \dot\theta_e\,]`, the cross-track
     error, its rate, the heading error and its rate.
   - The law:
     :math:`\delta = -Kx = -k_1 e - k_2 \dot e - k_3 \theta_e - k_4 \dot\theta_e`.
   - The gains :math:`K` minimize, over all future steps, the errors
     weighted by :math:`Q` plus the steering weighted by :math:`R`:
     :math:`J = \sum_k x_k^{\top} Q\, x_k + R\,\delta_k^2`. A larger
     :math:`Q` tracks tighter; a larger :math:`R` steers gentler. :math:`K`
     is computed once, offline.

   It needs a dynamic model: mass, yaw inertia, axle positions and the
   tires' cornering stiffness, "not as convenient to directly measure".
   Snider's car: 1140 kg, 155,495 N/rad per axle. His results: plain LQR
   keeps an error in long curves; a feed-forward term
   :math:`\delta_{\text{ff}}`, the steering a steady curve needs, removes
   it. And "the LQR tracker does not considerably outperform the Stanley or
   kinematic methods in many scenarios" (Snider, 2009).

   We do not run LQR on our turn: our simulation has no tire model to
   design it from.


.. _l10-lec-errors:

Measure How Far Off the Path: Two Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Cross-track error
   :class: note

   The AV's distance from the path, measured square to the path at the
   nearest path point. We measure it at the rear axle, positive to the left:
   the rear axle's :math:`d` in the Frenet frame.

- **Heading error:** the angle between the AV's heading and the path's
  direction at that nearest point.
- Our runs start with a cross-track error of 1.0 m and a heading error of 0:
  the AV parallel to the lane, 1 m left of its center.
- A steering controller turns these two into a steering angle. Pure Pursuit
  does it by looking ahead along the path; Stanley (below) uses both errors
  directly.


.. dropdown:: More detail: steer into the turn, the steering must jump too
   :class-container: more-detail
   :icon: info
   :name: l10-more-steer-jump

   Entering the first arc at 4.47 m/s, the AV goes from a straight line to
   :math:`\kappa` = 0.1000 /m in one point of the path:

   1. Steering needed: from 0 to 0.280 rad (the Vehicle Modeling section,
      above), at once.
   2. Sideways acceleration :math:`v^2\kappa`: from 0 to
      :math:`4.47^2 \times 0.1000` = 2.0 m/s², at once.
   3. No steering can turn in zero time: ours takes 0.1 s to start and about
      0.2 s to get most of the way. The AV leaves the path for a moment,
      whatever the controller.

   .. important::

      The curvature graph shows that this Town03 junction has no gradual part:
      the curvature steps from 0 to 0.100 /m. A planner can smooth the path
      first.


.. _l10-lec-pp:

Pure Pursuit
~~~~~~~~~~~~

Pure Pursuit finds a steering angle from the geometry of a point ahead on
the path. The controller node steers with it; its one parameter, the
lookahead, changes how the AV drives.


.. _l10-lec-pp-idea:

Chase a Point Ahead: the Idea of Pure Pursuit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pure Pursuit comes from pursuit guidance: steer so that you reach a point
that runs ahead of you. Coulter's implementation (Coulter, 1992), for a
vehicle:

1. Pick a lookahead point on the path, a distance :math:`L_d` ahead.
2. Find the circle arc from the rear axle, along the heading, through that
   point.
3. Steer to follow that arc.

.. important::

   The lookahead sets the trade-off: short, and the AV tracks tightly but
   can weave; long, and it steers smoothly but cuts corners. Snider: Pure
   Pursuit is "quite robust to large errors and discontinuous paths.
   However, it is not clear how to pick the best look-ahead distance"
   (Snider, 2009).


.. _l10-lec-pp-law:

Steer for the Arc: Pure Pursuit's Steering Law
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

   \delta = \arctan\!\left(\frac{2L\sin\alpha}{L_d}\right), \qquad
   L_d = \max(L_{d,\min},\; k_v\, v)

- :math:`\delta`: steering angle; :math:`L`: wheelbase; :math:`\alpha`: the
  angle from the heading to the lookahead point; :math:`L_d`: lookahead
  distance.
- "Look farther ahead when going faster": :math:`k_v` in seconds.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Strengths**
     - **Limits**
   * - simple: one formula, the wheelbase only; robust to large errors and
       jumps in the path (Snider, 2009)
     - no slip in the model; cuts corners, more as speed grows (Snider,
       2009); ignores the heading error

On our turn (below): 5 m fixed, or :math:`\max(3\ \mathrm{m}, 0.75\ \mathrm{s}\times v)`.

.. dropdown:: More detail: why κ = 2 sin α / L_d
   :class-container: more-detail
   :icon: info
   :name: l10-more-pp-arc

   .. figure:: /_static/images/L10/pp_arc.png
      :alt: A geometry drawing with dark round tags. The rear axle at tag 1 with an arrow pointing right along the heading. A green arc leaves it tangent to the arrow and curves up to the goal point at tag 2. The arc's center, a green cross at tag 3, sits straight above the rear axle; gray lines of length R join it to the rear axle and to the goal. A blue chord of length L_d joins the rear axle to the goal. A red arc marks the angle alpha between the heading and the chord; a green arc at the center marks the angle 2 alpha. A dashed line from the center meets the chord at its middle.
      :width: 45%
      :align: center

      The arc from the rear axle through the goal point.

   .. admonition:: Reading the figure
      :class: tip

      The drawing uses :math:`\alpha` = 35°, chosen for the drawing. The
      arrow from tag 1 is the AV's heading; the green curve is the arc.

      - **Tag 1:** the rear axle.
      - **Tag 2:** the goal point. The blue chord from tag 1 to tag 2 has
        length :math:`L_d`; it makes the angle :math:`\alpha` (red) with
        the heading.
      - **Tag 3:** the arc's center. The gray lines from it to tag 1 and to
        tag 2 both have length :math:`R`; the angle between them is
        :math:`2\alpha` (green). The dashed line from it meets the chord at
        its middle.

   1. The arc starts along the heading, so its center (tag 3) is square to
      the heading from the rear axle (tag 1), at distance :math:`R`.
   2. The goal (tag 2) is on the arc: the center is :math:`R` from it too.
      The triangle (tag 1, tag 2, tag 3) has two sides :math:`R`.
   3. The angle between the heading and the chord is :math:`\alpha`, so the
      chord makes :math:`90^\circ - \alpha` with the side from tag 1 to
      tag 3. The triangle's angle at tag 3 is then
      :math:`180^\circ - 2(90^\circ - \alpha) = 2\alpha`.
   4. The dashed line splits it into two right triangles with half the
      chord: :math:`L_d / 2 = R \sin\alpha`. So
      :math:`R = L_d / (2\sin\alpha)` and :math:`\kappa = 2\sin\alpha/L_d`.
   5. With :math:`\sin\alpha = g_y / L_d`: :math:`\kappa = 2 g_y / L_d^2`,
      Coulter's form (Coulter, 1992). Our example:
      2 × (−0.933) / 25 = −0.0746 /m, as below.


.. _l10-lec-pp-steps:

Steer with Pure Pursuit: Aim at a Point Ahead, Drive the Arc to It
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pure Pursuit chases a point that keeps moving ahead along the path. At every
cycle:

1. Draw a circle of radius :math:`L_d`, the **lookahead distance**, around
   the rear axle. Where the path leaves it, ahead of the AV: the **goal
   point**.
2. Write the goal point in the AV's own frame: how far forward, how far
   left.
3. Find the circle arc that starts at the rear axle along the AV's heading
   and passes through the goal point. Its curvature:
   :math:`\kappa = 2\sin\alpha / L_d`.
4. Steer for that curvature: :math:`\delta = \arctan(L\kappa)`, the bicycle
   model's rule.

.. important::

   The controller node gets the pose of the car's origin and moves it back
   to the rear axle with ``rear_offset``. The four steps by hand, on one
   moment of our run with :math:`L_d` = 5 m (the node's
   ``lookahead_distance``), are in the "More detail" box below.

.. dropdown:: More detail: the four steps by hand, on one moment of our run
   :class-container: more-detail
   :icon: info
   :name: l10-more-pp-steps

   .. rubric:: Step 1: Find the Goal Point on the Lookahead Circle

   The moment: :math:`t` = 10.65 s, at :math:`s` = 82.7 m, just before the
   first arc begins (:math:`s` = 83.2 m).

   .. figure:: /_static/images/L10/pp_geom_1.png
      :alt: A close top view of the corner, in meters: the lane edges in black, the lane center dashed gray, bending right after x = 83. The AV is drawn faintly, facing right and slightly down, with its rear axle as a dark dot (dark tag 2) near x = 82.7, y = 0. A blue dashed circle of radius 5 meters is centered on the rear axle (dark tag 1). A blue dot (dark tag 3) sits where the lane center leaves the circle ahead of the AV, near x = 87.6, y = minus 1.2.
      :width: 60%
      :align: center

      Step 1: the lookahead circle and the goal point.

   .. admonition:: Reading the figure
      :class: tip

      A close top view of the corner, in meters. The lane center is the
      dashed gray line; the AV is drawn faintly.

      - **Tag 1:** the lookahead circle, :math:`L_d` = 5 m (blue dashed).
      - **Tag 2:** the rear axle: :math:`x` = 82.69, :math:`y` = −0.03 m;
        heading :math:`\theta` = −0.0443 rad (−2.5°); speed 5.22 m/s.
      - **Tag 3:** the goal point: (87.56, −1.18) m, where the path leaves
        the circle ahead.

   .. rubric:: Step 2: Write the Goal Point in the AV's Frame

   .. figure:: /_static/images/L10/pp_geom_2.png
      :alt: The same close top view. Two black arrows leave the rear axle: one forward along the AV's heading, labeled forward, one to its left, labeled left. An orange double arrow below and parallel to the forward arrow spans from the rear axle to the goal point's forward distance (tag 4). A short orange double arrow beside the goal spans its sideways distance to the right of the forward line (tag 5). The lookahead circle and the goal point are as before, tags 1 to 3. All tags are dark circles.
      :width: 60%
      :align: center

      Step 2: the goal point's forward and sideways distances.

   .. admonition:: Reading the figure
      :class: tip

      The same view, with the AV's own frame: two black arrows from the
      rear axle, forward and left. Tags 1 to 3 are as in Step 1.

      - **Tag 4:** how far forward the goal point is, :math:`g_x` (orange).
      - **Tag 5:** how far to the side it is, :math:`g_y`, here to the
        right of the forward line (orange).

   1. From the rear axle to the goal, in the map: :math:`\Delta x` =
      4.866 m, :math:`\Delta y` = −1.150 m.
   2. Turn by :math:`-\theta` (:math:`\cos\theta` = 0.9990,
      :math:`\sin\theta` = −0.0443). Forward, tag 4:
      :math:`g_x = \cos\theta\,\Delta x + \sin\theta\,\Delta y`
      = 0.9990 × 4.866 + (−0.0443) × (−1.150) = 4.912 m.
   3. Left, tag 5: :math:`g_y = -\sin\theta\,\Delta x + \cos\theta\,\Delta y`
      = 0.0443 × 4.866 + 0.9990 × (−1.150) = −0.933 m: 0.933 m to the right.

   .. rubric:: Step 3: Find the Angle α and the Arc Through the Goal

   .. figure:: /_static/images/L10/pp_geom_3.png
      :alt: The same close top view, zoomed out downward. A black line joins the rear axle to the goal point; a red arc at the rear axle (tag 4) marks the small angle between the forward arrow and that line. A green arc starts at the rear axle along the heading and curves right into the goal point. A green cross far below, near x = 82.1, y = minus 13.4 (tag 5), is the arc's center; green dotted lines join it to the rear axle and to the goal. All tags are dark circles.
      :width: 55%
      :align: center

      Step 3: the angle to the goal and the arc through it.

   .. admonition:: Reading the figure
      :class: tip

      The same view, zoomed out downward. Tags 1 to 3 are as in Step 1. The
      black line joins the rear axle to the goal point; the green arc is
      the arc through the goal.

      - **Tag 4:** the angle :math:`\alpha` between the forward arrow and
        the line to the goal (red).
      - **Tag 5:** the arc's center (green cross), joined to the rear axle
        and to the goal by green dotted lines.

   1. The angle to the goal (tag 4):
      :math:`\alpha = \arctan(g_y / g_x) = \arctan(-0.933 / 4.912)` =
      −0.188 rad (−10.8°).
   2. The arc's curvature: :math:`\kappa = 2\sin\alpha / L_d`
      = 2 × (−0.1866) / 5 = −0.0746 /m.
   3. Its radius: :math:`R` = 1 / 0.0746 = 13.4 m, centered at tag 5.
      Negative: a right turn.

   .. rubric:: Step 4: Turn the Arc into a Steering Command

   1. The bicycle model: :math:`\delta = \arctan(L\kappa) =
      \arctan(2.875 \times (-0.0746)) = \arctan(-0.214)` = −0.211 rad
      (−12.1°), to the right.
   2. The controller node turns :math:`\delta` into a ``VehicleCmd`` steer
      from −1 to 1: it divides by 1.222 rad, the wheel angle at full
      steering (measured in CARLA), then clamps: −0.211 / 1.222 = −0.173.
   3. Next cycle, 0.05 s later, the AV has moved: a new goal point, a new
      arc.

   .. important::

      Two common mistakes: dividing by 0.7, the most the controller asks
      for, instead of 1.222, which turns the wheels 1.75 times too far; and
      the sign: ``VehicleCmd`` steer is positive to the left, CARLA's steer
      positive to the right, so the node that steps CARLA flips it.

   Steps 3 and 4 in one line:
   :math:`\delta = \arctan\big(2L\sin\alpha / L_d\big)`.


.. _l10-lec-ld-tradeoff:

Choose the Lookahead: Too Short Weaves, Too Long Cuts the Corner
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L10/pp_tradeoff.png
   :alt: A graph of distance from the lane center in meters against the lookahead distance from 4 to 12 meters. The orange line with round markers, dark tag 1, falls from 0.50 at 4 meters to 0.05 at 12. The dark line with square markers, tag 2, is 0.40 at 4 meters, lowest at 5 meters with 0.25, then rises to 0.39, 0.67, 0.98 and 1.53 at 6, 8, 10 and 12 meters.
   :width: 70%
   :align: center

   Two errors against the lookahead distance.

.. admonition:: Reading the figure
   :class: tip

   The distance from the lane center against the lookahead distance
   :math:`L_d`, from 4 to 12 m.

   - **Tag 1 (orange, round markers):** how far the AV crosses after the
     1 m start. It falls as :math:`L_d` grows.
   - **Tag 2 (dark, square markers):** the largest distance from the center
     in the turn. It is lowest at :math:`L_d` = 5 m (0.25 m), then grows.

At 4 m and below the AV weaves (4 m: about 0.4 m each way, and it does not
stop; 3 m: the swings grow to 3.07 m, out of the 3.5 m lane). At 10 m it
turns early and cuts 0.98 m inside the corner.

.. important::

   Snider found the same trade-off: a short lookahead tracks the path more
   closely, a long one drives more smoothly. On our turn, with our model,
   5 m is the best of the eight we tried.

.. dropdown:: More detail: the 3 m and 10 m runs
   :class-container: more-detail
   :icon: info
   :name: l10-more-lookahead

   .. rubric:: Choose the Lookahead: Too Short, and the AV Weaves

   .. figure:: /_static/images/L10/pp_straight.png
      :alt: A graph, not a map: the rear axle's distance from the lane center, positive left, against the distance along the path from 0 to 72 meters. All three runs start at plus 1. The red curve, dark tag 1, swings across the center with growing swings, reaching about plus and minus 3 meters by 70 meters. The blue curve, tag 2, crosses once to about minus 0.3 and settles near zero by about 36 meters. The green dashed curve, tag 3, slides down to zero without crossing much and settles by about 16 meters.
      :width: 85%
      :align: center

      Three lookahead distances on the straight approach.

   .. admonition:: Reading the figure
      :class: tip

      A graph, not a map: the rear axle's distance from the lane center
      (positive left) against the distance :math:`s` along the path.
      Start: 1 m left, 8 m/s, on the straight approach.

      - **Tag 1 (red):** :math:`L_d` = 3 m: the swings grow to 3.07 m, out
        of the 3.5 m lane.
      - **Tag 2 (blue):** :math:`L_d` = 5 m: crosses by 0.32 m, within
        0.1 m from :math:`s` = 35.9 m.
      - **Tag 3 (green, dashed):** :math:`L_d` = 10 m: crosses by 0.07 m,
        within 0.1 m from :math:`s` = 15.8 m.

   .. important::

      The weave needs both the steering's delay and its lag. The same 3 m
      run crosses by only 0.05 m with instant steering, and by 0.32 m with
      the lag alone, then settles.

   .. rubric:: Choose the Lookahead: Too Long, and the AV Cuts the Corner

   .. figure:: /_static/images/L10/pp_turn.png
      :alt: A top view of the corner from x = 68 to 98 and y = minus 26 to 4. The blue solid run with a 5 meter lookahead stays on the dashed lane center through the corner, swinging slightly outside after it. The green dashed run with a 10 meter lookahead leaves the center early, cuts inside the corner, where a green dot marks its farthest point inside (dark tag 1), then swings outside on the exit, where a second green dot marks its farthest point outside (dark tag 2), before returning to the center.
      :width: 60%
      :align: center

      A 5 m and a 10 m lookahead through the corner.

   .. admonition:: Reading the figure
      :class: tip

      A top view of the corner, in meters. The blue line is the 5 m run;
      the green dashed line is the 10 m run.

      - **Tag 1:** with :math:`L_d` = 10 m, the goal point is already
        around the corner, so the AV turns early: 0.98 m inside the center
        at :math:`s` = 90.6 m.
      - **Tag 2:** then it turns too late on the exit: 0.95 m outside at
        :math:`s` = 102.2 m.

   :math:`L_d` = 5 m stays within 0.25 m of the center through the corner.


.. _l10-lec-ld-speed:

A Lookahead for Every Speed: Scale It with the Speed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At 8 m/s the AV covers 5 m in 5 / 8 = 0.6 s; at 3.46 m/s, in
5 / 3.46 = 1.4 s. To look the same **time** ahead at every speed, scale
:math:`L_d` with the speed: :math:`L_d = \max(3\ \mathrm{m},\ k_v v)`, with
:math:`k_v` in seconds. With :math:`k_v` = 0.75 s: on the approach,
0.75 × 8 = 6 m; in the second arc, 0.75 × 3.46 = 2.6 m, raised to 3 m.

Mean \|jerk\|: how fast the sideways acceleration :math:`v\dot\theta`
changes, averaged over the run.

.. list-table::
   :widths: 28 25 27 20
   :header-rows: 1
   :class: compact-table

   * - **Lookahead**
     - **Crosses after start**
     - **Largest in the turn**
     - **Mean \|jerk\|**
   * - 5 m fixed
     - 0.32 m
     - 0.25 m
     - 1.79 m/s³
   * - 10 m fixed
     - 0.07 m
     - 0.98 m
     - 0.42 m/s³
   * - 0.5 s × :math:`v`
     - 0.54 m (weaves)
     - 0.46 m
     - 8.88 m/s³
   * - 0.75 s × :math:`v`
     - 0.23 m
     - 0.07 m
     - 1.11 m/s³
   * - 1.0 s × :math:`v`
     - 0.12 m
     - 0.18 m
     - 0.59 m/s³

Long at speed, short in the corner: 0.75 s gives the smallest corner error.
The controller node sets the lookahead to 5 m or 1 s × :math:`v`,
whichever is longer, because the EKF's pose jumps a little at each GNSS fix
and a short lookahead turns each jump into a swerve.


.. _l10-lec-handson-4:

Hands-On, Part 4: Compare the Steering Runs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python3 l10_handson.py --part track     # steering runs

.. figure:: /_static/images/L10/handson_track.png
   :alt: Part of the hands-on window. Left, the corner from above with the lane edges, the lane center and the rear axle's path of the chosen run, here Pure Pursuit with 5 meters, and the AV. Right, two graphs against the distance along the path: the rear axle's distance off the center, and the steering angle.
   :width: 80%
   :align: center

   Part of the hands-on window, for Pure Pursuit with 5 m.

.. admonition:: Reading the figure
   :class: tip

   - **Left:** the corner from above, with the lane edges, the lane center
     (gray dashed) and the rear axle's path of the chosen run (blue), here
     Pure Pursuit with 5 m, and the AV.
   - **Right, top:** the rear axle's distance off the center (positive
     left) against the distance :math:`s` along the path.
   - **Right, bottom:** the steering angle against :math:`s`.
   - The orange band on both graphs marks the junction lane.

A list at the window's left (not shown) picks the run: Pure Pursuit with 2
to 12 m, or 0.5, 0.75 or 1 s × :math:`v`; Stanley with a gain from 0.5 to 8.

.. admonition:: What to look at
   :class: hint

   1. Pick 2, 3 and 4 m: from which lookahead does the AV stop weaving?
   2. Pick 12 m: how far inside the corner does the rear axle get?


.. _l10-lec-pp-summary:

Where Pure Pursuit Leaves Us
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Where Pure Pursuit leaves us
   :class: tip

   - **Four steps:** goal point on the lookahead circle; goal in the AV's
     frame; :math:`\kappa = 2\sin\alpha / L_d`;
     :math:`\delta = \arctan(L\kappa)`. On our turn: −0.211 rad, command
     −0.173.
   - **Short lookahead** (3 m at 8 m/s): the AV weaves, 3.07 m, because the
     steering is delayed and lags.
   - **Long lookahead** (10 m): 0.98 m inside the corner, then 0.95 m
     outside.
   - **Scaled with speed** (0.75 s): 0.07 m at most in the corner.


.. _l10-lec-stanley:

Stanley
~~~~~~~

Pure Pursuit steers the rear axle toward a point ahead. Stanley keeps the
same turn, start and PID, and steers from the two errors, measured at the
front axle.


.. _l10-lec-stanley-idea:

Correct Heading and Offset Together: the Idea of Stanley
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stanley steered Stanford's car to win the 2005 DARPA Grand Challenge (Thrun
et al., 2006). Pure Pursuit chases a point; Stanley asks: how misaligned am
I with the path, and how do I fix it?

1. Measure the **heading error**: the angle between the car's heading and
   the path's.
2. Measure the **cross-track error** at the **front axle**.
3. Steer to correct both at once.

- Steering commands "at a rate of 20 Hz"; in the race Stanley reached "its
  top speed of 38.0 mph" (Thrun et al., 2006).
- Snider: "this method outperforms Pure Pursuit in most scenarios. However,
  the Stanley method is not as robust to large errors and non-smooth
  paths" (Snider, 2009).


.. _l10-lec-stanley-law:

Steer from the Front Axle: Stanley's Heading and Cross-Track Terms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The steering law of Stanford's DARPA Grand Challenge car, with our signs
(steering and :math:`e` positive to the left):

.. math::

   \delta = \psi_e - \arctan\frac{k\,e}{v + k_s}

- :math:`\psi_e`: the heading error.
- :math:`e`: the cross-track error of the **front** axle.
- :math:`k`: a gain.
- :math:`k_s` = 1 m/s keeps the fraction finite when the AV stands still.
  Hoffmann et al. found 1 m/s "appropriate" in experiments (Hoffmann et al.,
  2007, p. 2299).

The team's paper writes a plus sign with its own signs. With ours, an AV
left of the path (:math:`e > 0`) must steer right, so the term is
subtracted.

.. figure:: /_static/images/L10/stanley_geom.png
   :alt: A close top view of the corner with the AV drawn faintly. A dark dot at the rear axle (tag 1) and a purple dot at the front axle (tag 2), joined by a line. Just below the front axle, a gray dot on the lane center (tag 3), the nearest path point, with a short purple double arrow between them. A gray line from that point along the path's direction (tag 4) and a dark line from the front axle along the AV's heading; a red arc (tag 5) marks the angle between them. All tags are dark circles.
   :width: 75%
   :align: center

   Stanley's two errors, at the front axle.

.. admonition:: Reading the figure
   :class: tip

   A close top view of the corner, at the same moment as Pure Pursuit's
   worked example. The AV is drawn faintly.

   - **Tag 1:** the rear axle.
   - **Tag 2:** the front axle (purple).
   - **Tag 3:** the path point nearest the front axle; the short purple
     double arrow between them is :math:`e`.
   - **Tag 4:** the path's direction there (gray line).
   - **Tag 5:** the heading error :math:`\psi_e`, the angle (red arc)
     between the path's direction and the AV's heading (dark line).

.. dropdown:: More detail: one Stanley step by hand, and why it converges
   :class-container: more-detail
   :icon: info
   :name: l10-more-stanley

   .. rubric:: One Stanley Step by Hand, at the Same Moment

   The AV as in Pure Pursuit's example: rear axle (82.69, −0.03) m,
   :math:`\theta` = −2.54°, :math:`v` = 5.22 m/s. Gain :math:`k` = 1
   (chosen).

   1. Front axle: :math:`L` = 2.875 m ahead along the heading:
      (85.56, −0.15) m.
   2. Nearest path point: the path there points at −15.97°. Heading error:
      :math:`\psi_e` = −15.97° minus (−2.54°), which is −13.43° = −0.234 rad.
   3. Cross-track error: the front axle is 0.212 m **left** of the path, so
      :math:`e` = +0.212 m.
   4. Cross-track term:
      :math:`-\arctan\frac{1 \times 0.212}{5.22 + 1} = -\arctan(0.034)` =
      −0.034 rad (−2.0°), toward the path, to the right.
   5. :math:`\delta` = −0.234 minus 0.034 = −0.268 rad (−15.4°), to the
      right.

   .. important::

      Pure Pursuit at the same moment: −0.211 rad. Stanley steers harder
      here: it measures the heading error at the front axle, where the
      path has already turned.

   .. rubric:: Which Point of the AV Stays on the Path

   .. figure:: /_static/images/L10/axle_paths.png
      :alt: Two top views of the corner side by side, the AV drawn faintly in the second arc in each. Left, dark tag 1, Pure Pursuit with a 5 meter lookahead in blue: the solid line, the rear axle, follows the dashed lane center; the dotted line, the front axle, swings outside it through the corner. Right, tag 2, Stanley with gain 1 in purple: the dotted front axle line follows the lane center; the solid rear axle line runs inside the corner.
      :width: 90%
      :align: center

      The rear and front axles' paths, for Pure Pursuit and for Stanley.

   .. admonition:: Reading the figure
      :class: tip

      Two top views of the corner, in meters, with the AV drawn faintly in
      the second arc. Solid lines are the rear axle, dotted lines the
      front axle; the gray dashed line is the lane center.

      - **Tag 1 (blue):** Pure Pursuit, :math:`L_d` = 5 m.
      - **Tag 2 (purple):** Stanley, :math:`k` = 1.

   Pure Pursuit holds the **rear** axle on the path; the front swings out
   by up to 0.67 m. Stanley holds the **front** axle (within 0.38 m); the
   rear cuts in by up to 0.45 m. On the 5.98 m arc, with the rear axle on
   it, the front axle is :math:`\sqrt{5.98^2 + 2.875^2} - 5.98` = 0.66 m
   outside: the axles, 2.875 m apart, cannot both be on the path.

   .. rubric:: Pure Pursuit Against Stanley on Our Turn

   Same start (1 m left, 8 m/s), same speed PID, same steering lag:

   .. list-table::
      :widths: 29 19 19 19 14
      :header-rows: 1
      :class: compact-table

      * - **Controller**
        - **Crosses after start**
        - **Rear axle, turn**
        - **Front axle, turn**
        - **Mean \|jerk\|**
      * - Pure Pursuit, 5 m
        - 0.32 m
        - 0.25 m
        - 0.67 m
        - 1.79
      * - Pure Pursuit, 0.75 s × :math:`v`
        - 0.23 m
        - 0.07 m
        - 0.68 m
        - 1.11
      * - Stanley, :math:`k` = 0.5
        - 0
        - 0.27 m
        - 0.43 m
        - 0.38
      * - Stanley, :math:`k` = 1
        - 0
        - 0.45 m
        - 0.38 m
        - 0.62
      * - Stanley, :math:`k` = 4
        - 0.79 m (weaves)
        - 0.79 m
        - 1.42 m
        - 22.37

   - Distances: the largest from the lane center. Jerk in m/s³, as in "A
     Lookahead for Every Speed", above.
   - Stanley's gain plays the role of a short lookahead: too high, and with
     our steering lag the AV weaves.

   .. rubric:: Why the Cross-Track Term Pulls e to Zero

   Take a straight path and an AV already parallel to it
   (:math:`\psi_e` = 0), its front axle :math:`e > 0` to the left (leave
   out :math:`k_s`). Stanley steers by :math:`\delta = -\arctan(k e / v)`,
   to the right, so the front axle moves at speed :math:`v` at the angle
   :math:`\delta` toward the path:

   1. Sideways speed:
      :math:`\dot e = v\sin\delta = -v \sin\big(\arctan(k e / v)\big)`, as
      Thrun et al. write it (Thrun et al., 2006).
   2. Small :math:`e`: :math:`\sin(\arctan z) \approx z`, so
      :math:`\dot e \approx -k\,e`. The error shrinks by the same fraction
      every second: :math:`e(t) = e(0)\,e^{-kt}`.
   3. With :math:`k` = 1 /s: after 1 s, :math:`e^{-1}` = 0.37 of the error
      is left; after 3 s, 0.05.
   4. Large :math:`e`: :math:`\arctan` stays below 90°, so the AV turns
      toward the path at most square to it, then the term shrinks as
      :math:`e` does.

   .. important::

      The real AV adds what this leaves out: the steering's delay and lag,
      and its 0.7 rad limit. That is why :math:`k` = 4 weaves in our runs.


.. _l10-lec-mpc:

MPC
~~~

Pure Pursuit and Stanley look at the path now, with one formula. MPC builds
on the bicycle model instead: it predicts the next seconds with it. It does
what the local planner did: it rolls out candidates, scores them and keeps
the best. Here the candidates are steering sequences, the plan is made
again every 0.05 s, and only its first input is applied.


.. _l10-lec-mpc-idea:

Look Ahead, Then Act: the Idea of MPC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

MPC looks ahead: "if I simulate the car for the next seconds, which
steering sequence tracks the path best, within my limits?"

1. **Predict:** run a vehicle model forward over a horizon.
2. **Optimize:** find the input sequence that minimizes the tracking error.
3. **Apply:** only the first input.
4. **Repeat:** at the next step, from the new measurement.

- Re-solving from each measurement is the feedback; looking ahead handles
  the curve coming.
- Kong et al.: MPC "can handle Multi-Input Multi-Output systems with input
  and state constraints while taking into account the nonlinear dynamics of
  the vehicle" (Kong et al., 2015).


.. _l10-lec-mpc-def:

Plan Ahead with MPC: Predict, Score, Apply the First Input, Repeat
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Model predictive control (MPC)
   :class: note

   At every step, choose the sequence of inputs over a fixed horizon that a
   model predicts will score best, within the limits; apply only the first
   input; repeat from the newly measured state.

.. figure:: /_static/images/L10/mpc_loop.png
   :alt: Three rows of eight cells, one row per control step k, k plus 1 and k plus 2, each row shifted one cell to the right. A brace over the first row says the horizon, N = 8 steps, predicted with the bicycle model. In each row only the first cell is green. A time arrow runs along the bottom.
   :width: 80%
   :align: center

   The horizon slides forward one step at a time.

.. admonition:: Reading the figure
   :class: tip

   Each row is the plan made at one control step: :math:`k`,
   :math:`k + 1`, :math:`k + 2`. Each plan covers the horizon, :math:`N` = 8
   steps here, predicted with the bicycle model. Each row starts one step
   later than the one above; time runs to the right.

   - **Green cell:** the one input applied before the next plan.
   - **Gray cells:** the rest of the plan, predicted but not applied.

The figure is drawn with 8 steps; our example uses 60. The horizon slides
forward with the AV, so MPC is a feedback controller: each plan starts from
the measured pose.

.. dropdown:: More detail: one MPC step on our turn, drawn, and the problem written out
   :class-container: more-detail
   :icon: info
   :name: l10-more-mpc

   .. rubric:: One MPC Step on Our Turn, Drawn

   .. figure:: /_static/images/L10/mpc_candidates.png
      :alt: A top view of a right turn, x from 68 to 100 meters and y from minus 26 to 6. The lane comes in from the left along y = 0 and turns down; solid lines mark its edges and a dashed gray line its center. The AV is drawn faintly at about x = 78, with a dark dot at its rear axle. A fan of hundreds of thin gray curves leaves the rear axle: a few bend left, up to y = 6.6, and most bend right, down to y = minus 12.7; tag 4 sits at the fan's lower-left end. One thick green curve runs along the lane center past a green dot (tag 1, joined by a thin line from above the lane), bends right past a second green dot (tag 2) and ends inside the turn, at about x = 90.6 and y = minus 3.5, joined by a thin line to tag 3 to the right of the lane. All tags are dark circles.
      :width: 70%
      :align: center

      The candidate steering sequences and the best one.

   .. admonition:: Reading the figure
      :class: tip

      A top view of the corner, in meters, 2 m before the turn, at
      7.09 m/s. The AV is drawn faintly; the dark dot is its rear axle.

      - **Tag 4 (gray):** every sequence of three steering angles, each
        from −0.6 to 0.2 rad in steps of 0.1 and held 1 s: :math:`9^3` =
        729 sequences, each predicted 3 s (60 steps) with the bicycle
        model.
      - **Tags 1 to 3 (green):** the best sequence, at 1, 2 and 3 s: 0,
        then −0.4, then 0 rad.

   - Score: the squared distance from the path, added over the 60 steps,
     plus the squared steering angles.
   - Apply only 0 rad for 0.05 s, then plan again.

   A simplification for the picture: a real MPC finds the sequence with an
   optimizer, not by trying a list.

   .. rubric:: The Problem Written Out

   At step :math:`k`, with the measured state :math:`\mathbf{x}_0` (the
   AV's :math:`x, y, \theta, v`) and horizon :math:`N`:

   .. math::

      \min_{\delta_0, \dots, \delta_{N-1}} \; \sum_{i=1}^{N} e_i^2\,\Delta t
      \;+\; w \sum_{i=0}^{N-1} \delta_i^2
      \quad \text{subject to} \quad
      \mathbf{x}_{i+1} = f(\mathbf{x}_i, \delta_i), \quad |\delta_i| \le 0.7

   - :math:`f`: one step of the bicycle model; :math:`e_i`: the predicted
     cross-track error after step :math:`i`; :math:`w`: a weight (chosen)
     that trades steering effort against error.
   - The solution is a whole sequence; only :math:`\delta_0` is applied.
   - Our picture: :math:`N` = 60 steps of 0.05 s, :math:`w` = 1, and
     :math:`\delta_i` held for 20 steps at a time, from 9 values, so the
     729 sequences could simply be tried. In the steering term each held
     angle counts once: :math:`0^2 + 0.4^2 + 0^2` = 0.16. The best scored
     0.186: 0.026 from the error, 0.16 from the steering.
   - Autoware's MPC is linear (Autoware Foundation, MPC lateral
     controller): with :math:`f` linearized around the path and this
     squared score, each step is a quadratic program, which solvers handle
     fast.


.. _l10-lec-mpc-weigh:

Weigh MPC: What It Adds and What It Costs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Adds**
     - **Costs**
   * - Sees the curvature jump coming: the horizon covers the next seconds
       of the path
     - An optimization at every step, in time for the next one
   * - Limits inside the problem: the 0.7 rad steering, the steering rate
     - A model good enough to predict with; a wrong model gives wrong plans
   * - Delays in the model: the 0.1 s steering delay can be predicted
     - Weights to tune instead of one lookahead

Autoware, an open-source driving stack, offers both: a steering controller
that tracks the path with a linear MPC, and a Pure Pursuit one.


.. _l10-lec-choosing:

Choosing a Controller
~~~~~~~~~~~~~~~~~~~~~

.. _l10-lec-ctrl-compare:

Compare the Steering Controllers on Our Turn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Same start (1 m left, 8 m/s), same speed PID, same steering delay and lag:

.. list-table::
   :widths: 29 19 19 19 14
   :header-rows: 1
   :class: compact-table

   * - **Controller**
     - **Crosses after start**
     - **Rear axle, turn**
     - **Front axle, turn**
     - **Mean \|jerk\|**
   * - Pure Pursuit, 5 m
     - 0.32 m
     - 0.25 m
     - 0.67 m
     - 1.79
   * - Pure Pursuit, 0.75 s × :math:`v`
     - 0.23 m
     - 0.07 m
     - 0.68 m
     - 1.11
   * - Stanley, :math:`k` = 0.5
     - 0
     - 0.27 m
     - 0.43 m
     - 0.38
   * - Stanley, :math:`k` = 1
     - 0
     - 0.45 m
     - 0.38 m
     - 0.62
   * - Stanley, :math:`k` = 4
     - 0.79 m (weaves)
     - 0.79 m
     - 1.42 m
     - 22.37

- Distances: the largest from the lane center; jerk in m/s³. Pure Pursuit
  holds the rear axle on the path, Stanley the front: the axles, 2.875 m
  apart, cannot both be on it.
- Not run here: LQR and MPC. Snider found geometric trackers "achieve the
  majority of the path tracking performance demonstrated by the other
  trackers until speeds are significantly increased" (Snider, 2009).

.. dropdown:: More detail: Snider's guidelines for matching a controller to the job
   :class-container: more-detail
   :icon: info
   :name: l10-more-snider

   Snider's comparison table, "Good Applications" column (Snider, 2009):

   .. list-table::
      :widths: 24 46 30
      :header-rows: 1
      :class: compact-table

      * - **Tracker**
        - **Good applications**
        - **Cutting corners**
      * - Pure Pursuit
        - slow driving and/or on discontinuous paths
        - significant as speed increases
      * - Stanley
        - smooth highway driving and parking maneuvers
        - no
      * - LQR with feed forward
        - smooth high speed driving, urban driving at speed
        - no

   - Our turn agrees: Pure Pursuit with a long lookahead cut the corner by
     0.98 m; Stanley's front axle stayed within 0.38 m.
   - MPC is the choice when limits must hold inside the plan: the steering
     angle and rate, the delay.


.. _l10-lec-speed:

Longitudinal Control
--------------------

The bicycle model takes two inputs: the steering angle, which the
controllers of the last section set, and the acceleration. This section
covers the acceleration: the PID that holds the AV at the turn's speed
profile, the same speed controller every steering run in the last section
used.

**In this section:** a PID that turns the speed error into throttle and
brake.

**What it is for:** the controller node's speed control is a PID with
anti-windup; this section shows why it needs the anti-windup.


.. _l10-lec-longitudinal-problem:

Hold the Speed with Two Pedals: the Longitudinal Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Longitudinal control answers one question: how does the AV hold its speed
with the throttle and the brake?

- Speeding up and slowing down are not mirror images: the engine limits one,
  the brakes and the tires the other. Our speed model (chosen): full
  throttle gives 4 m/s², full brake gives 8 m/s².
- Throttle and brake are two actuators, so the controller switches between
  them.
- The pedals answer late. Our model's engine lags by 0.3 s. Autoware's gas
  pedal and brake "typically has a delay of about a hundred millisecond"
  (Autoware Foundation).

.. dropdown:: More detail: the profile in time, and its jerk
   :class-container: more-detail
   :icon: info
   :name: l10-more-profile-jerk

   .. rubric:: Turn the Speed Profile into a Trajectory: Add Up the Times

   .. figure:: /_static/images/L10/trajectory_dots.png
      :alt: The same top view of the turn as before, with blue dots on the lane center, one for every second of the speed profile. On the approach the dots are evenly spaced, 8 meters apart; in the corner they bunch up, about 3.5 meters apart, and spread out again on the exit. Gray leader lines label four dots: t = 0 s at the start, t = 5 s on the approach, t = 10 s just before the corner, t = 15 s on the exit.
      :width: 90%
      :align: center

      One dot per second of the speed profile.

   .. admonition:: Reading the figure
      :class: tip

      The same top view of the turn, with a dot on the lane center for every
      second of the profile. On the approach the dots sit 8 m apart; in the
      corner they bunch up to about 3.5 m apart, then spread out again on
      the exit. Labels mark :math:`t` = 0, 5, 10 and 15 s.

   - Each 0.25 m step takes :math:`\Delta s / v`; adding the steps up gives
     :math:`t(s)`.
   - At 8 m/s the dots are 8 × 1 = 8.0 m apart; in the turn, 3.46 × 1 =
     3.5 m (3.45 m measured between two dots).
   - The whole path takes 20.0 s.

   .. rubric:: Slow Down for the Turn: Two Ways Between the Same Speeds

   .. figure:: /_static/images/L10/slow_speed_accel.png
      :alt: Two graphs against the time from the start of braking. Left, speed: the red line, dark tag 1, drops in a straight line from 8 to 3.46 meters per second in 2.3 seconds; the green curve, tag 2, leaves 8 gently, falls along an S shape and reaches 3.46 at about 3.4 seconds. Right, acceleration: the red line jumps from 0 to minus 2 at once, stays there for 2.3 seconds and jumps back to 0; the green curve dips smoothly from 0 to minus 2 at its middle and comes back to 0. A dotted line marks minus 2.
      :width: 90%
      :align: center

      Two ways to slow from 8 to 3.46 m/s.

   .. admonition:: Reading the figure
      :class: tip

      Left, speed against time from the start of braking. Right,
      acceleration against the same time.

      - **Tag 1 (red):** constant deceleration, a straight drop in speed and
        a jump in acceleration.
      - **Tag 2 (green):** the quintic, an S-shaped drop in speed and a
        smooth dip in acceleration.

   - Constant deceleration, 2.0 m/s² (our speed profile's): :math:`T =
     (8 - 3.46)/2.0` = 2.27 s, over :math:`D = \frac{8 + 3.46}{2} \times
     2.27` = 13.0 m.
   - A quintic that never passes 2.0 m/s²: 3.41 s, over 19.5 m. It starts
     braking 19.5 − 13.0 = 6.5 m earlier.

   .. rubric:: Compare the Jerk: a Jump Against a Quintic

   .. figure:: /_static/images/L10/slow_jerk.png
      :alt: A graph of jerk in meters per second cubed, sampled at 20 per second, against the time from the start of braking. The red line, dark tag 1, is zero except for a spike down to minus 40 at time 0 and a spike up to plus 40 at about 2.3 seconds. The green line, tag 2, stays close to zero, rising slowly from about minus 2.3 to plus 2.3.
      :width: 85%
      :align: center

      Jerk: a jump compared with a quintic.

   .. admonition:: Reading the figure
      :class: tip

      Jerk, sampled at 20 per second, against the time from the start of
      braking.

      - **Tag 1 (red):** constant deceleration: a spike to minus 40 at the
        start and a spike to plus 40 at the end.
      - **Tag 2 (green):** the quintic: stays close to zero throughout.

   - **Tag 1:** constant deceleration: the acceleration jumps by 2.0 m/s²
     within one 0.05 s step, so the jerk is 2.0 / 0.05 = 40 m/s³, twice. A
     true jump has no finite jerk: the number grows the faster the profile
     is sampled (100 samples a second give 2.0 / 0.01 = 200).
   - **Tag 2:** the quintic: at most 2.3 m/s³.


.. _l10-lec-speed-loop:

Hold the Target Speed: the Speed Loop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pid_block.png
   :alt: A block diagram. The target speed v_ref enters a summing circle with a plus sign; the measured speed v comes back into it with a minus sign. The difference e splits into three gray boxes: K_p times e, K_i times the sum of e times delta t, K_d times the change of e over delta t. Their outputs add in a second circle to u. A box clips u to minus 1 to 1; u above 0 is throttle, u below 0 is brake. Then the AV, whose measured speed v returns to the first circle.
   :width: 95%
   :align: center

   The speed loop with a PID controller.

.. admonition:: Reading the figure
   :class: tip

   Read left to right. The target speed :math:`v_{\mathrm{ref}}` minus the
   measured speed :math:`v` gives the error :math:`e`. Three terms act on
   it: :math:`K_p e`; :math:`K_i \sum e\,\Delta t`; and
   :math:`K_d (e_k - e_{k-1}) / \Delta t`. They add to the command
   :math:`u`, which is clipped to −1 to 1: above 0 it is throttle, below 0
   brake. The AV's measured speed returns to the start of the loop.

- The error :math:`e = v_{\mathrm{ref}} - v`. Three terms add to the
  command :math:`u`: P, the **proportional** term; I, the **integral** term;
  D, the **derivative** term. Together they make a **PID** controller.
- Our speed model (chosen): full throttle gives 4 m/s², full brake 8 m/s²,
  drag takes :math:`0.15 + 0.012\,v^2` m/s², and the engine lags by 0.3 s.
  Throttle stops at 0.75, the node's ``max_throttle``.
- The test: the AV at rest; the target jumps to 8 m/s, as when a red light
  turns green.


.. _l10-lec-pid-split:

Drive Two Pedals from One PID: Split the Output, Stop the Windup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   u = K_p\, e + K_i \sum e\,\Delta t + K_d\,\frac{e_k - e_{k-1}}{\Delta t},
   \qquad e = v_{\text{ref}} - v

**Split the one output into two pedals**

- :math:`u > 0`: throttle :math:`u` (ours stops at 0.75); :math:`u < 0`:
  brake :math:`-u`.
- Around :math:`u = 0` a small dead zone, or two thresholds, keeps the car
  from switching pedals on every cycle (hysteresis).

**Anti-windup**: keep the integral in check while a pedal sits at its limit

- clamp the sum (ours: ±1 m, chosen; the controller node's
  ``pid_windup_limit`` is 2.0);
- or stop adding while the output is saturated.

The next sections run it: P alone, then I, the windup, and the clamp.


.. _l10-lec-p:

Try P Alone: the AV Settles 0.42 m/s Short
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pid_p.png
   :alt: Two graphs of speed against time after the target steps to 8 meters per second. Left, 0 to 20 seconds: the orange curve rises from 0, levels off just under the dashed target line at 8 after about 4 seconds and stays there; a dotted box marks the part from 10 to 20 seconds. Right, that box enlarged, speed 7.0 to 8.5: the orange line sits flat at 7.58, the dashed target at 8.0, and a double arrow between them carries dark tag 1.
   :width: 95%
   :align: center

   P alone: the speed settles under the target.

.. admonition:: Reading the figure
   :class: tip

   Left: the speed for 20 s after the target steps to 8 m/s (dashed line).
   Right: the dotted box, enlarged.

   - **Tag 1:** the gap between the target, 8.0 m/s, and where the AV
     settles, 7.58 m/s.

:math:`u = K_p e` with :math:`K_p` = 0.5 (chosen). Why the gap stays:

1. At 7.58 m/s the drag is :math:`0.15 + 0.012 \times 7.58^2` = 0.84 m/s²;
   holding the speed needs throttle 0.84 / 4 = 0.21.
2. P makes throttle only from an error: 0.5 × :math:`e` = 0.21 gives
   :math:`e` = 0.42 m/s.


.. _l10-lec-pi:

Close the Gap with I: the AV Overshoots by 4 m/s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The I term adds up the error over time, :math:`K_i \sum e\,\Delta t`. While
any gap remains, the sum grows and pushes more throttle, so the gap closes.
With :math:`K_i` = 0.3 (chosen):

.. figure:: /_static/images/L10/pid_pi.png
   :alt: A graph of speed against time after the target steps to 8 meters per second. The red curve rises past the dashed target line at 8, keeps rising to a peak just above 12 at about 6 seconds (dark tag 1), then falls back and settles on 8 after about 11 seconds.
   :width: 90%
   :align: center

   PI: the gap closes, after a large overshoot.

.. admonition:: Reading the figure
   :class: tip

   The speed against the time after the target steps to 8 m/s (dashed
   line).

   - **Tag 1:** the peak: 12.18 m/s, 4.18 m/s over the target. The speed
     settles within 0.2 m/s of 8 only after 10.6 s.


.. _l10-lec-windup:

Explain the Overshoot: Windup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Integrator windup
   :class: note

   The I term keeps growing while the actuator is at its limit and cannot
   act on it; the stored sum then drives the output past the target once
   the limit is released. Here the sum shrinks only while the AV is too
   fast.

.. figure:: /_static/images/L10/pid_windup.png
   :alt: A graph of the command against time. A pink band covers the first 5.85 seconds, while the throttle sits at its limit. A dotted line marks the throttle limit 0.75. The red curve, the I term, dark tag 1, rises from 0 to a peak of about 4.3 at 3.4 seconds and falls back to about 0.23 by 12 seconds. The dark curve, dark tag 2, is the throttle actually used: flat at 0.75 for the first 5.85 seconds, then a short dip below 0, then about 0.23.
   :width: 80%
   :align: center

   The I term and the throttle during the PI run.

.. admonition:: Reading the figure
   :class: tip

   The command against the time after the target steps to 8 m/s; 0 to 1 is
   throttle. The dotted line is the throttle limit, 0.75. The pink band
   covers the first 5.85 s, while the throttle sits at that limit.

   - **Tag 1 (red):** the I term. It rises to about 4.3, then falls back to
     about 0.23.
   - **Tag 2 (dark):** the throttle actually used: flat at 0.75, then a
     short dip below 0 (brake), then about 0.23.

1. The throttle (tag 2) is at its 0.75 limit from the start; a larger
   command cannot open the throttle further.
2. The I term keeps adding the large early errors: by the time the AV
   reaches 8 m/s (3.45 s), the sum is 14.29 m and the I term
   0.3 × 14.29 = 4.29 (tag 1).


.. _l10-lec-clamp:

Anti-Windup: Clamp the Sum
~~~~~~~~~~~~~~~~~~~~~~~~~~

At every step:

1. add :math:`e\,\Delta t` to the sum;
2. hold the sum within ±1 m (chosen; the controller node's
   ``pid_windup_limit`` is 2.0);
3. compute :math:`u` from the three terms.

.. figure:: /_static/images/L10/pid_clamp.png
   :alt: A graph of speed against time after the target steps to 8 meters per second. The red curve without the clamp rises to a peak above 12 (dark tag 1). The green curve with the clamp rises like it but stops at about 8.25 and settles on 8 within a few seconds (dark tag 2).
   :width: 90%
   :align: center

   The same PI run, without and with the clamp.

.. admonition:: Reading the figure
   :class: tip

   The speed against the time after the target steps to 8 m/s (dashed
   line).

   - **Tag 1 (red):** without the clamp: peak 12.18 m/s.
   - **Tag 2 (green):** with it: peak 8.25 m/s, within 0.2 m/s of 8 after
     4.4 s.

.. dropdown:: More detail: size the clamp, since too tight brings the gap back
   :class-container: more-detail
   :icon: info
   :name: l10-more-clamp

   The sum must still be able to hold the throttle the AV needs at the
   target speed:

   1. At 8 m/s the drag is :math:`0.15 + 0.012 \times 8^2` = 0.92 m/s², so
      the AV needs throttle 0.92 / 4 = 0.23 with no error left.
   2. With :math:`K_i` = 0.3 and the sum held within 1 m, the I term can
      reach 0.3 × 1 = 0.3. Enough.
   3. With :math:`K_i` = 0.1 and the same clamp, it can reach only 0.1.
      Measured: the AV settles at 7.76 m/s, 0.24 m/s short: better than P
      alone (0.42), but the gap does not close.

   So the clamp and :math:`K_i` go together: :math:`K_i` × clamp must
   exceed the throttle the steady speed needs.

.. dropdown:: More detail: trim the peak with D, a little less overshoot
   :class-container: more-detail
   :icon: info
   :name: l10-more-pid-d

   .. figure:: /_static/images/L10/pid_compare.png
      :alt: Two graphs of speed against time. Left, 0 to 20 seconds: three curves rise together from 0; the orange one levels off just under 8, the green and the blue dashed ones reach 8. A dotted box marks 2 to 10 seconds, 7 to 8.5. Right, that box enlarged, with dark tags: the orange curve, tag 1, flattens at 7.58; the green curve, tag 2, peaks at about 8.25 near 4 seconds and settles on 8; the blue dashed curve, tag 3, peaks lower, about 8.12, and settles on 8.
      :width: 95%
      :align: center

      P, PI and PID, all with the clamp.

   .. admonition:: Reading the figure
      :class: tip

      Left: the three runs for 20 s. Right: the dotted box, enlarged. The
      tags match the rows of the table below.

      - **Tag 1 (orange):** P alone.
      - **Tag 2 (green):** PI.
      - **Tag 3 (blue, dashed):** PID.

   .. list-table::
      :widths: 35 20 20 25
      :header-rows: 1
      :class: compact-table

      * - **Gains (chosen), clamp 1 m**
        - **Peak**
        - **After 30 s**
        - **Within 0.2 m/s**
      * - 1: P, :math:`K_p` = 0.5
        - 7.72 m/s
        - 7.58 m/s
        - never
      * - 2: PI, :math:`K_i` = 0.3
        - 8.25 m/s
        - 8.00 m/s
        - after 4.4 s
      * - 3: PID, :math:`K_d` = 0.1
        - 8.12 m/s
        - 8.00 m/s
        - after 3.5 s

.. dropdown:: More detail: run the PID every 0.05 s, the formula the controller uses
   :class-container: more-detail
   :icon: info
   :name: l10-more-pid-formula

   At step :math:`k`, with :math:`\Delta t` = 0.05 s and
   :math:`e_k = v_{\mathrm{ref}} - v_k`:

   .. math::

      u_k = K_p\, e_k \;+\; K_i \sum_{j \le k} e_j\,\Delta t \;+\;
      K_d\,\frac{e_k - e_{k-1}}{\Delta t}

   - :math:`u_k` is clipped to −1 to 1: above 0 it is throttle (at most
     0.75 in the node), below 0 it is brake.
   - D reacts to how fast the error changes. A sudden target jump makes
     that change large for one step. Here :math:`K_d` = 0.1 trimmed the
     peak from 8.25 to 8.12 m/s.
   - Our gains suit our speed model. The node's ``controller_config.yaml``
     starts at :math:`K_p` = 0.5, :math:`K_i` = 0.05, :math:`K_d` = 0.1,
     with the sum held within 2.0. By the clamp rule above,
     0.05 × 2.0 = 0.1, under the 0.23 our model needs at 8 m/s. CARLA's car
     may need another throttle, so tune :math:`K_i` on it and check for a
     gap.


.. _l10-lec-handson-1:

Hands-On, Parts 1 to 3: Try the Model, the Profile and the PID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The hands-on script is in the course's Python repo, folder ``lecture10``
(`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture10>`__):

.. code-block:: bash

   python3 l10_handson.py --part bicycle   # steering and circle
   python3 l10_handson.py --part profile   # slowing down
   python3 l10_handson.py --part pid       # P, PI, PID, clamp

.. admonition:: What to look at
   :class: hint

   1. ``bicycle``: which steering angle drives a 10 m circle? Check it
      against :math:`\delta = \arctan(L/R)`.
   2. ``pid``: set :math:`K_i` = 0.6 with no clamp, then with the clamp. How
      much does the clamp cut the peak?
   3. ``pid``: find gains with a peak under 8.2 m/s that reach 8 m/s within
      0.2 m/s in under 4 s.

We computed the ``pid`` runs in advance; the folder has no controller code.


.. _l10-lec-split-layers:

Split Speed Control in Two Layers: What Production Stacks Do
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Production stacks split speed control into two layers:

1. **Upper level:** a planner or controller picks the target speed or
   acceleration. For factory adaptive cruise control, "the planner model is
   usually a linear controller or an MPC more recently" (Zhou et al.,
   2021).
2. **Lower level:** turns the target acceleration into gas and brake, often
   a PI loop and a lookup table of pedal against acceleration at each
   speed.

- Autoware's longitudinal controller "computes the target acceleration to
  achieve the target velocity" with feed-forward and PID, chosen "from the
  viewpoint of trade-off between development/maintenance cost and
  performance" (Autoware Foundation).
- CARLA's ``VehicleAckermannControl`` works the same way: the caller gives
  a speed and an acceleration, and CARLA's own speed and acceleration PID
  loops set the pedals.

.. important::

   The course uses a PID in CARLA to build intuition (our gains, chosen
   from the runs: :math:`K_p` = 0.5, :math:`K_i` = 0.3, :math:`K_d` = 0.1,
   clamp 1 m); the layer above it may be an MPC.

.. dropdown:: More detail: PID in labs, MPC above
   :class-container: more-detail
   :icon: info
   :name: l10-more-pid-mpc

   **PID: in Our Labs**

   - simple to write and to read;
   - a baseline to compare against;
   - enough for CARLA's scenes;
   - builds intuition for feedback.

   Our gains (chosen, from the runs): :math:`K_p` = 0.5, :math:`K_i` = 0.3,
   :math:`K_d` = 0.1, clamp 1 m.

   **MPC: at the Planner Level**

   - puts acceleration and jerk limits inside the plan;
   - keeps a safe gap to the car ahead;
   - needs an optimization solver: CasADi, acados, OSQP or CVXPY, for
     example.

   .. important::

      The course uses a PID in CARLA to build intuition; know that the
      layer above it may be an MPC.


.. _l10-lec-speed-summary:

Where Speed Control Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where speed control leaves us
   :class: tip

   - **P** needs an error to make throttle: 0.42 m/s short at
     :math:`K_p` = 0.5.
   - **I** removes the gap, but winds up while the throttle sits at its
     limit: 12.18 m/s for an 8 m/s target.
   - **Clamping the sum** stops it: peak 8.25 m/s.
   - **D** trimmed the peak to 8.12 m/s here.


.. _l10-lec-carla:

CARLA Implementation
--------------------

Every run so far was a numpy simulation of the bicycle model. This section
moves the same two controllers, Pure Pursuit and the speed PID, into the
course's ROS 2 node, which drives CARLA.

**In this section:** one control step, the node's five inputs and one
command, a live look at the topics, and tuning by symptom.

**What it is for:** reading each topic while CARLA drives shows the numbers
the node works with.


.. _l10-lec-control-loop:

Run One Control Step: the Loop, Step by Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Each control step, kinematic controllers**

1. The node that steps CARLA advances it 0.05 s (lock step).
2. Read the state: position, heading, speed.
3. Find the nearest path point and the path's heading.
4. Compute the cross-track error or the lookahead point.
5. Compute :math:`\delta` (Pure Pursuit or Stanley).
6. Compute throttle or brake (speed PID).
7. Scale the steering to −1 to 1.
8. Send the command; repeat, 20 times a second.

**Added for LQR or MPC**

- 2b. Turn the velocity into the car's frame: :math:`v_x, v_y`.
- 2c. Read the yaw rate.
- 4b. Build the full error state :math:`[e, \dot e, \theta_e,
  \dot\theta_e]`.
- 4c. Pick the gains for this speed.

A dynamic model needs more measurements and gains that change with speed.

.. dropdown:: More detail: CARLA inputs and outputs
   :class-container: more-detail
   :icon: info
   :name: l10-more-carla-io

   .. rubric:: Command CARLA Two Ways: Normalized Pedals or Physical Targets

   .. list-table::
      :widths: 50 50
      :header-rows: 1
      :class: compact-table

      * - ``carla.VehicleControl``
        - ``carla.VehicleAckermannControl``
      * - ``throttle`` 0 to 1, ``brake`` 0 to 1
        - ``speed`` (m/s), ``acceleration`` (m/s²), ``jerk`` (m/s³)
      * - ``steer`` −1 to 1
        - ``steer`` in rad, "Positive value is to the right"
      * - the caller splits throttle and brake
        - CARLA's speed and acceleration PIDs set the pedals

   - Both send **one** steering angle; CARLA turns it into the two wheels'
     angles.
   - Our node sends ``VehicleControl``: steer = :math:`\delta` / 1.222 (the
     wheel angle at full steering, measured), with the sign flipped, since
     CARLA's steer is positive to the right.
   - The docs slip once: ``__init__``'s list gives ``steer`` as 0 to 1, the
     attribute −1 to 1, which is what CARLA takes (CARLA's API docs).

   .. rubric:: Read the State from CARLA: Mind the Degrees and the Frame

   .. list-table::
      :widths: 18 44 38
      :header-rows: 1
      :class: compact-table

      * - **Quantity**
        - **CARLA call**
        - **Unit, as CARLA gives it**
      * - :math:`x, y`
        - ``get_transform().location``
        - m
      * - :math:`\theta`
        - ``get_transform().rotation.yaw``
        - **degrees**
      * - :math:`v_x, v_y`
        - ``get_velocity()``
        - m/s, in the **world** frame
      * - :math:`\dot\theta`
        - ``get_angular_velocity().z``
        - **deg/s**

   - Kinematic controllers (Pure Pursuit, Stanley) need
     :math:`[x, y, \theta, v]`, with :math:`v = \sqrt{v_x^2 + v_y^2}`.
   - A dynamic model (LQR) also needs the speeds along and across the car:
     turn the world velocity by :math:`-\theta`, as Pure Pursuit's Step 2
     turned the goal point.
   - CARLA's frame is left-handed (Unreal Engine): flip :math:`y` and the
     yaw's sign for a right-handed map, as our road export does.

   .. rubric:: Read the Car's Parameters: What CARLA Gives a Kinematic and a Dynamic Model

   .. list-table::
      :widths: 28 16 16 40
      :header-rows: 1
      :class: compact-table

      * - **Parameter**
        - **Kinematic**
        - **Dynamic**
        - **From CARLA**
      * - wheelbase :math:`L`
        - yes
        - yes
        - from the wheels' positions
      * - largest steer :math:`\delta_{\max}`
        - yes
        - yes
        - ``wheels[0].max_steer_angle``, in degrees
      * - mass :math:`m`
        -
        - yes
        - ``get_physics_control().mass``, kg
      * - yaw inertia :math:`I_z`
        -
        - yes
        - not given: estimate it
      * - CG position :math:`\ell_f, \ell_r`
        -
        - yes
        - not given: estimate it
      * - tire stiffness
        -
        - yes
        - ``lat_stiff_value``, "per unit of lateral slip", not in N/rad

   - The API gives no unit for a wheel's ``position``: check the wheelbase
     it gives against the car's length before using it.
   - A kinematic controller needs only the first two rows.

   .. rubric:: Build the Path from CARLA's Waypoints

   1. Get the map from the world.
   2. ``map.get_waypoint(location)``: the waypoint on the lane at the AV's
      position.
   3. ``waypoint.next(d)``: the waypoints about :math:`d` meters ahead,
      "one waypoint per option" at a junction (CARLA's API docs).
   4. Keep the :math:`(x, y)` of each as the path.

   .. list-table::
      :widths: 40 60
      :header-rows: 1
      :class: compact-table

      * - **Path**
        - **Spacing, length**
      * - our turn
        - every 0.25 m, 137.5 m
      * - the topics demo's ``/planning/path``
        - 51 points over 50 m, sent twice a second

   At a junction, ``next`` returns one waypoint per branch: the route
   decides which one to keep.

   .. rubric:: Know What Each Topic Carries: the Message Types

   .. _l10-lec-messages:

   The goal is to know which fields of each message the controller reads,
   and which it writes.

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - **Topic**
        - **Message type**
        - **Main fields used**
      * - ``/planning/path``
        - ``nav_msgs/Path``
        - ``poses[i].pose.position``: the path's points :math:`(x, y)`, in m
      * - ``/localization/odom``
        - ``nav_msgs/Odometry``
        - ``pose.pose``: the position :math:`(x, y)` and the heading
      * - ``/carla/imu/data``
        - ``sensor_msgs/Imu``
        - ``angular_velocity.z``: the turn rate, in rad/s
      * - ``/carla/speedometer``
        - ``geometry_msgs/TwistStamped``
        - ``twist.linear.x``: the speed, in m/s
      * - ``/behavior/target_speed``
        - ``geometry_msgs/TwistStamped``
        - ``twist.linear.x``: the speed to hold, in m/s
      * - ``/control/vehicle_cmd`` (output)
        - ``ads_msgs/VehicleCmd``
        - ``throttle`` 0 to 0.75, ``steer`` −1 to 1 (positive turns left),
          ``brake`` 0 to 1

   The node runs no timer. Each ``/behavior/target_speed`` message makes it
   compute one ``VehicleCmd``, which copies that message's time stamp. The
   node that steps CARLA waits for this command before its next tick.


.. _l10-lec-controller-node:

Today's Two Controllers: One Node, Five Inputs, One Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/controller_io.png
   :alt: A block diagram. A green block labeled controller_node holds two boxes: steering, Pure Pursuit, and speed, PID. Five ROS topics come in on the left, each with what it carries: /planning/path, the route planner's lane path; /localization/odom, the pose, which the node moves 1.4 meters back to the rear axle; /carla/imu/data, the turn rate, for the heading; /carla/speedometer, the speed the PID uses; /behavior/target_speed, the speed to hold. One output on the right: /control/vehicle_cmd, with steer from minus 1 to 1, positive left, throttle and brake, to the node that steps CARLA.
   :width: 95%
   :align: center

   The controller node: its inputs and its command.

.. admonition:: Reading the figure
   :class: tip

   - **Left, five inputs (ROS topics):** ``/planning/path``, the route
     planner's lane path; ``/localization/odom``, the pose, which the node
     moves 1.4 m back to the rear axle; ``/carla/imu/data``, the turn rate,
     for the heading; ``/carla/speedometer``, the speed the PID uses;
     ``/behavior/target_speed``, the speed to hold.
   - **Middle, green:** ``controller_node``, with two parts: the steering
     (Pure Pursuit) and the speed (PID).
   - **Right, one output:** ``/control/vehicle_cmd``, with a steer from −1
     to 1 (positive left), a throttle and a brake. It goes to the node that
     steps CARLA.

- The node holds two parts: **Pure Pursuit** for the steering and a **PID**
  for the speed. Today: how each one works, by hand and in simulation.
- A separate node steps CARLA every 0.05 s and waits for this node's command
  before each step (the lock step). So the controller runs 20 times a
  second; our simulation uses the same rate.


.. _l10-lec-topics-demo:

See the Five Inputs Live: CARLA on Autopilot in Town03
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal is to see what each input topic carries while the AV drives. The
package is ``l10_topics_demo`` in the course's ROS repository (`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l10_topics_demo/README.md>`__).

.. code-block:: bash

   ros2 launch l10_topics_demo l10_topics.launch.py
   ros2 topic echo /behavior/target_speed --once     # in a second terminal

One message on each topic, from our run:

.. list-table::
   :widths: 30 52 18
   :header-rows: 1
   :class: compact-table

   * - **Topic**
     - **One message, from our run**
     - **Per second**
   * - ``/planning/path``
     - 51 points: the lane center, 50 m ahead
     - 2
   * - ``/localization/odom``
     - :math:`x` = 22.19 m, :math:`y` = 4.67 m; forward speed 8.04 m/s
     - 20
   * - ``/carla/imu/data``
     - ``angular_velocity.z`` = 0.234 rad/s, in a curve
     - 20
   * - ``/carla/speedometer``
     - ``twist.linear.x`` = 8.05 m/s
     - 20
   * - ``/behavior/target_speed``
     - ``twist.linear.x`` = 8.33 m/s: the road's 30 km/h limit, 30 / 3.6
     - 20

The demo uses stand-ins: the pose is CARLA's truth, the target speed is the
speed limit, and the path is the lane center ahead. Nothing publishes
``/control/vehicle_cmd``: the autopilot drives.


.. _l10-lec-tune-symptom:

Tune by Symptom: What Each Fix Did on Our Turn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From our runs on the turn (the Lateral and Longitudinal sections):

.. list-table::
   :widths: 20 36 44
   :header-rows: 1
   :class: compact-table

   * - **Controller**
     - **Symptom**
     - **Fix, and what it did on our turn**
   * - Pure Pursuit
     - weaves
     - longer lookahead: 3 m swung to 3.07 m; 5 m crossed by 0.32 m
   * - Pure Pursuit
     - cuts the corner
     - shorter lookahead: 10 m cut by 0.98 m; 5 m stayed within 0.25 m
   * - Pure Pursuit
     - both
     - scale with speed: 0.75 s × :math:`v` stayed within 0.07 m
   * - Stanley
     - weaves
     - lower :math:`k`: :math:`k` = 4 weaved by 0.79 m; :math:`k` = 0.5 did
       not
   * - Speed PID
     - settles short
     - add I: P alone stopped 0.42 m/s short
   * - Speed PID
     - overshoots
     - clamp the sum: 12.18 to 8.25 m/s peak
   * - Speed PID
     - a little overshoot left
     - add D: 8.25 to 8.12 m/s peak


.. _l10-lec-summary:

Summary
-------

This closes the lecture: the six parts that turned a path into a steering,
throttle and brake command.

- **Trajectories**: sampled in time and checked against where a moving car
  will be; the AV waited for car B, then passed.
- **Actuators**: by wire; the wheel turns about 0.2 s after the command on a
  measured car.
- **Vehicle models**: Ackermann for the wheels, the kinematic bicycle while
  the sideways acceleration stays under :math:`0.5\mu g`, the dynamic one
  beyond.
- **Lateral**: Pure Pursuit chases a point, Stanley fixes heading and offset
  at the front axle, MPC plans the next seconds.
- **Longitudinal**: a PID with split pedals and anti-windup; production
  adds a layer above it.
- **CARLA**: one node, five inputs, one command, 20 times a second.


.. _l10-lec-equations:

Key Equations
~~~~~~~~~~~~~

The lecture's models and controllers condense to five equations:

.. list-table::
   :widths: 28 72
   :header-rows: 1
   :class: compact-table

   * - **Model**
     - **Equation**
   * - Kinematic bicycle
     - :math:`\dot x = v\cos\theta,\ \dot y = v\sin\theta,\ \dot\theta =
       \dfrac{v}{L}\tan\delta,\ \dot v = a`
   * - Steer for a curvature
     - :math:`\delta = \arctan(L\kappa)`
   * - Pure Pursuit
     - :math:`\delta = \arctan\!\left(\dfrac{2L\sin\alpha}{L_d}\right)`
   * - Stanley
     - :math:`\delta = \psi_e - \arctan\dfrac{k e}{v + k_s}` (our signs)
   * - PID
     - :math:`u = K_p e + K_i \sum e\,\Delta t + K_d
       \dfrac{e_k - e_{k-1}}{\Delta t}`

.. dropdown:: More detail: more equations, parameters
   :class-container: more-detail
   :icon: info
   :name: l10-more-parameters

   .. rubric:: More Equations: LQR, Ackermann and the Friction Circle

   .. list-table::
      :widths: 28 72
      :header-rows: 1
      :class: compact-table

      * - **Model**
        - **Equation**
      * - LQR
        - :math:`\delta = -Kx`, :math:`x = [e, \dot e, \theta_e,
          \dot\theta_e]`
      * - Ackermann
        - :math:`\cot\delta_o - \cot\delta_i = W/L`
      * - Friction circle
        - :math:`\lVert \vec F_x + \vec F_y \rVert \le \mu \lVert \vec F_z
          \rVert`

   .. rubric:: Typical Parameters: Ours, and Where Each Comes From

   .. list-table::
      :widths: 46 24 30
      :header-rows: 1
      :class: compact-table

      * - **Parameter**
        - **Value**
        - **From**
      * - control rate
        - 20 per second
        - our lock step
      * - Pure Pursuit lookahead
        - 5 m, or 1 s × :math:`v`
        - the controller node
      * - Stanley gain, softening
        - :math:`k` = 0.5 to 1, :math:`k_s` = 1 m/s
        - our runs; Hoffmann et al.
      * - steering limit
        - 0.7 rad
        - the controller node
      * - sideways acceleration cap
        - 2.0 m/s²
        - our profile (chosen)
      * - kinematic model valid below
        - :math:`0.5\mu g`, 4.9 m/s²
        - Polack et al.
      * - steering delay, lag
        - 0.2 s, 0.2 s
        - MKZ, measured
      * - speed PID
        - 0.5, 0.3, 0.1; clamp 1 m
        - our runs (chosen)

   .. rubric:: Resources

   .. list-table::
      :widths: 30 70
      :header-rows: 1
      :class: compact-table

      * - **Resource**
        - **Link**
      * - CARLA simulator
        - `github.com/carla-simulator/carla
          <https://github.com/carla-simulator/carla>`__
      * - PythonRobotics
        - `github.com/AtsushiSakai/PythonRobotics
          <https://github.com/AtsushiSakai/PythonRobotics>`__
      * - Autoware
        - `github.com/autowarefoundation/autoware
          <https://github.com/autowarefoundation/autoware>`__
      * - Apollo
        - `github.com/ApolloAuto/apollo
          <https://github.com/ApolloAuto/apollo>`__
      * - Algorithms for Automated Driving
        - `Theers and Singh's open book
          <https://thomasfermi.github.io/Algorithms-for-Automated-Driving/>`__

   Key papers: Coulter 1992 (Pure Pursuit); Thrun et al. 2006 (Stanley);
   Snider 2009 (comparison); Kong et al. 2015 (vehicle models); Werling
   et al. 2010 (trajectories).


.. _l10-lec-next:

Next Class
----------

.. admonition:: Today
   :class: important

   The planners hand over a path; **today we planned trajectories, paths
   with times, and turned one into steering, throttle and brake.** A
   superstate or a behavior tree keeps the behavior layer small. Sampled in
   time and checked against a moving car, the AV waited for car B and
   passed the parked car. The bicycle model predicts; a quintic changes
   speed with small jerk; a PID holds the speed, with a clamp against
   windup; Pure Pursuit steers toward a point 5 m ahead (short weaves, long
   cuts corners); Stanley steers from the front axle; MPC plans the next
   seconds and applies only the first input.

- **L11, End-to-End Driving, VLA and Imitation Learning:** one network from
  the sensors to a trajectory or to the controls, in place of the whole
  stack.
- **Before then:** run the four hands-on parts, ``behavior_tree.py`` (with
  and without ``--no-pass``), and the topics demo if you have CARLA.


.. rubric:: Image credits

The vehicle icon in the figures on this page was created by Stone from the
`Noun Project <https://thenounproject.com>`_. The map is CARLA's Town03
(`carla.org <https://carla.org>`_).
