====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L9, the slides shown in class and
   the reading slide that goes with them, in the same order and with the
   same sections. You can read them at home. The deck keeps more material in
   its appendix, on :doc:`the appendix page <l9_appendix>`, "Going Further":

   - the region the base link must avoid, worked for two boxes;
   - the Frenet formulas: a path's position, heading and curvature from
     :math:`(s, d)`;
   - how hard a candidate turns, by hand, and the S curve's polynomial, with
     where 5.77 comes from;
   - how the circle radius changes with the number of circles;
   - grid search in the garage, and by hand on a small grid;
   - hybrid A*'s six steps, its estimates of cost to go, and its direct try
     at the goal;
   - RRT*, and RRT and RRT* in words.

   The hands-on commands, and the files of the in-class exercises, are on
   :doc:`the Code page <l9_code>`. The papers
   and pages behind these notes are listed on :doc:`the References page
   <l9_references>`.


.. _l9-lec-introduction:

Introduction
------------

The route planner gives the AV a route: the lanes to follow. Today's planner
finds the path for the next few seconds that follows the route and stays
clear of every object, through the next lane if needed.

.. figure:: /_static/images/L9/l7_to_l9.png
   :alt: Two top views of the same two-lane road, one above the other, x and y in meters. In each, the AV, a black car, drives to the right in the lower lane, and the obstacle, a blue parked car, stands about 58 meters ahead in the same lane. Top view, tag 1: a black dotted line along the center of the AV's lane runs straight through the obstacle. Bottom view, tag 2: a green path leaves the AV's lane, moves into the upper lane and passes the obstacle.
   :width: 95%
   :align: center

   The route's lane, and a path that passes the obstacle.

.. admonition:: Reading the figure
   :class: tip

   Both views show the same stretch of road from above, :math:`x` and
   :math:`y` in meters. The AV is the black car on the left; the obstacle,
   a parked car, is about 58 m ahead in the AV's lane.

   - **Top, tag 1:** the reference path from the route, the center of the
     AV's lane (black dots). It runs straight through the obstacle.
   - **Bottom, tag 2:** a path from today's planner (green). It moves into
     the upper lane and passes the obstacle.


.. _l9-lec-route-path:

Route, Path and Trajectory
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 16 46 38
   :header-rows: 1
   :class: compact-table

   * -
     - **What it holds**
     - **Made in**
   * - Route
     - the lanes to drive, from start to goal
     - the route planner (A* on the lane graph)
   * - Path
     - the curve the AV follows: positions and headings along it, no times
     - the local planner, today
   * - Trajectory
     - a path with a speed and a time at each point
     - next class

A route runs from start to goal and changes rarely. A path covers the next
few seconds, and the planner plans it again every 0.5 s, because what is
near the AV keeps changing.


.. _l9-lec-layers:

Four Layers Decide What the AV Does
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/layers.png
   :alt: A block diagram of four boxes in a row joined by arrows: Route planner, Behavior layer (today), Local planner (today) and Controller (next class). The two boxes marked today are green. Under the arrows: lanes to follow, a maneuver, a path for the next seconds, and, after the controller, steering, throttle, brake. Above, a box Pose feeds the route planner, and a box Pose, objects, predictions feeds the behavior layer and the local planner.
   :width: 95%
   :align: center

   The four layers that decide what the AV does.

.. admonition:: Reading the figure
   :class: tip

   Read the row left to right. Each arrow carries what one layer hands to
   the next.

   - The **route planner** reads the pose and hands on the lanes to follow.
   - The **behavior layer** (today, green) reads the pose, the objects and
     their predictions, and hands on a maneuver.
   - The **local planner** (today, green) reads the same inputs and hands on
     a path for the next seconds.
   - The **controller** (next class) turns the path into steering, throttle
     and brake.

Most driving stacks split their decisions into these four layers. Today
covers the two middle layers: the **local planner** first, then the
**behavior layer** that tells it what to do.


.. _l9-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

This is a reading slide in the deck. After this lecture, you can:

1. say what a local planner takes from the route planner and hands to the
   controller;
2. describe the AV by its configuration :math:`(x, y, \theta)`, and grow an
   obstacle into the region the AV's base link must avoid;
3. convert a point between the map and the Frenet frame :math:`(s, d)`, and
   say where the frame fails;
4. generate candidate paths with sideways shifts and score them by hand;
5. check a pose for collision with circles, and say why the check is
   conservative;
6. explain the behavior layer with a finite state machine;
7. explain grid search, hybrid A* and RRT, and say where each one is used.


.. _l9-lec-scene:

The Scene
---------

We take one road from CARLA's Town03 map, with the obstacle, a parked car,
in the AV's lane.

**What it is for:** every road method today runs on this one scene, with
distances read from the map.


.. _l9-lec-town03:

Town03, Road 67, Read from the Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/scene_overview.png
   :alt: A top view of every lane of CARLA's Town03 map as thin gray lines, x and y in meters: a grid of streets, a roundabout near the middle and a ring road around the edge. A thick black line follows the bottom edge of the ring to the right, then curves up the right side. Tag 1 marks the AV, a white dot with a dark edge on the straight part; tag 2 marks the obstacle, a blue square where the curve begins; tag 3 marks the end of the black line.
   :width: 60%
   :align: center

   Our stretch of road on the Town03 map.

.. admonition:: Reading the figure
   :class: tip

   The thin gray lines are every lane of Town03, seen from above. The thick
   black line is our stretch, along the bottom of the ring road and up its
   right side.

   - **Tag 1:** the AV (white dot).
   - **Tag 2:** the obstacle (blue square), where the curve begins.
   - **Tag 3:** the end of the stretch.

**We measured** these from the waypoints in CARLA's map file, with no CARLA
server:

- two lanes in each direction, 3.5 m wide;
- the stretch: 237.9 m of the right lane;
- straight for 116.5 m, then two left curves.

GP4 drives only Town01, which has one lane each way. Its A* tests also plan
two trips on Town03's graph, lane changes included.


.. _l9-lec-av-car:

The AV, the Obstacle and the Two Lanes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/scene_top.png
   :alt: A top view, to scale, of the start of the stretch, x and y in meters: two lanes, the lower one with a dotted center line, the lane line between them dashed. Tag 1 below the AV, a black car in the lower lane at the left. Tag 2 below the obstacle, a blue parked car, about 58 meters ahead in the same lane. Tag 3 in the upper lane. On the right the road starts to curve upward.
   :width: 95%
   :align: center

   The AV, the obstacle and the two lanes, to scale.

.. admonition:: Reading the figure
   :class: tip

   A top view of the start of the stretch, to scale. The dotted line is the
   reference path, the center of the right lane; the dashed line is the
   lane line between the two lanes.

   - **Tag 1:** the AV, black, in the right (lower) lane.
   - **Tag 2:** the obstacle, blue, about 58 m ahead in the same lane.
   - **Tag 3:** the left lane, which goes the same direction.

On the right, the road starts to curve upward.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **1: the AV (chosen)**
     - **2: the obstacle, a parked car (chosen)**
   * - on the right lane's center, at 10 m/s
     - 58 m ahead, 0.3 m right of the lane's center
   * - 4.5 m long, 1.9 m wide
     - 4.5 m long, 1.9 m wide
   * - position: its base link, the middle of its rear axle
     - position: its center

The plan covers 70 m ahead (chosen): 70 / 10 = 7 s at 10 m/s.


.. _l9-lec-gp4:

GP4's Planner and Its Two Triggers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In GP4 Task 2, you write A* on a lane graph with a node every 2 m along
each lane center; the path is a list of those nodes. It plans again in two
cases:

- a standing vehicle's center comes within ``obstacle_clearance`` = 3.0 m of
  a waypoint ahead;
- the AV is more than 2.0 m from the path.

**On our road:** the obstacle's center is 0.3 m from the right lane's
center. The waypoints there are 2 m apart, so the obstacle's center is
within about 1 m of one of them. That is under 3.0 m, so GP4 plans again.

If the route ran down the left lane instead, the obstacle's center would be
3.5 + 0.3 = 3.8 m from that lane's center, so at least 3.8 m from every
waypoint. That is over 3.0 m, so GP4 would not plan again.


.. _l9-lec-adds:

What a Local Planner Adds to GP4's Planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 48 52
   :header-rows: 1
   :class: compact-table

   * - **A path of lane waypoints**
     - **What a local planner adds**
   * - moves sideways only by whole lanes
     - any sideways offset, with a smooth move
   * - checks an object's center against waypoints
     - checks the AV's whole body against the object's
   * - is planned again only when a trigger fires (checked every 0.5 s)
     - is planned again every 0.5 s, from where the AV is

GP4 does not ask for a local planner. One would sit between your A* and your
controller. The course Final Report can discuss where one would help.


.. _l9-lec-cspace:

Configuration Space
-------------------

We describe the AV by three numbers, and turn the obstacle into a region
that the AV's base link must stay out of.

**What it is for:** every planner today searches over these three numbers.


.. _l9-lec-configuration:

Three Numbers Place the Whole AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Configuration
   :class: note

   A **configuration** of the AV, :math:`q = (x, y, \theta)`, fixes where
   every point of its body is: the base link at :math:`(x, y)` in the map frame, and the heading :math:`\theta`,
   counterclockwise from the map's :math:`x` axis.

.. figure:: /_static/images/L9/config_pose.png
   :alt: A top view of a black car facing up and to the right, at 30 degrees from a dashed horizontal arrow labeled map x; a dashed vertical arrow labeled map y crosses it at a small white circle near the rear of the car, the base link, with tag 1 beside it. An arc between the map x arrow and the car's dotted center line, ahead of the car, is labeled theta, tag 2. Beside the car's right side, two arrows along its length run from the rear bumper to the base link, 0.9 m, and from the base link to the front bumper, 3.6 m, tag 3. Ahead of the front bumper, a short arrow across the car's direction, labeled 0.95 m, runs from the center line to the side, tag 4.
   :width: 60%
   :align: center

   The three numbers of a configuration, on the AV.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** the base link at :math:`(x, y)`.
   - **Tag 2:** the heading :math:`\theta`, drawn at 30° so it shows.
   - **Tag 3:** the body is rigid, so :math:`q` places all of it: the rear
     bumper 0.9 m behind the base link (chosen), the front bumper
     4.5 − 0.9 = 3.6 m ahead.
   - **Tag 4:** each side 1.9 / 2 = 0.95 m out from the center line.

Our AV at the start: :math:`q` = (97.69 m, −207.29 m, 0.14°).


.. _l9-lec-cspace-def:

Configuration Space and Its Obstacle Region
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Configuration space (C-space)
   :class: note

   The set :math:`\mathcal{C}` of all configurations :math:`q`. Its
   **obstacle region** holds every :math:`q` at which the robot's body
   placed at :math:`q`, :math:`\mathcal{A}(q)`, overlaps an obstacle,
   :math:`\mathcal{O}`. The rest of :math:`\mathcal{C}` is the **free
   space**.

.. figure:: /_static/images/L9/cspace_idea.png
   :alt: A top view of two lanes, gray, with a dashed line between them. In the lower lane, a blue car points right, tag 1. Behind it in the same lane, a black car, tag 2, points right with its front over the blue car's rear; the part where the two bodies overlap is outlined in rust and hatched. In the upper lane, a second black car, tag 3, at the same distance behind, is clear of the blue car. Each black car has a small white circle near its rear, its base link.
   :width: 60%
   :align: center

   The AV's body at two poses behind the obstacle.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** :math:`\mathcal{O}`, the obstacle, a 4.5 m by 1.9 m box.
   - **Tag 2:** :math:`\mathcal{A}(q)` overlaps :math:`\mathcal{O}` (hatched):
     this :math:`q` is in the obstacle region.
   - **Tag 3:** :math:`\mathcal{A}(q)` is clear of :math:`\mathcal{O}`: this
     :math:`q` is free.

A path is collision free when every pose along it is free.


.. _l9-lec-cspace-plan:

Fast Collision Check: Grow the Obstacle, Then Test One Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Goal: the planner checks the AV's future poses, one every 0.5 m along each
path it considers. At each pose :math:`q`, decide quickly whether the AV
would hit the obstacle.

.. figure:: /_static/images/L9/cspace_plan.png
   :alt: Two panels side by side, split by a dashed line. Left: a black car behind a blue car, its front over the blue car's rear. Right: the blue car, faded, inside a rust hatched box much larger than it; a small white circle sits inside the box where the black car's base link was.
   :width: 85%
   :align: center

   Two bodies to compare, or one point and a box.

.. admonition:: Reading the figure
   :class: tip

   - **Left, the direct check**: compare the AV's body with the obstacle at
     every future pose: two shapes to compare each time.
   - **Right, grow, then test a point** (for one AV heading):

     - **Step 1**, once per heading: grow the obstacle by the AV's shape
       (hatched). It holds every position of the AV's base link at which the
       AV's body would touch the obstacle.
     - **Step 2**, at each pose: keep only the AV's base link (white dot). The
       pose collides when that point is inside the grown obstacle, as here.

   Both figures show the same pose. On the left the two bodies overlap: the
   pose collides, and the white dot on the right is inside the grown obstacle.


.. _l9-lec-grow:

Step 1: Grow the Obstacle, for One AV Heading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/cspace_grow.png
   :alt: A top view of a blue car, its center marked with a white cross, and three gray cars heading the same way, each just touching it: tag 1 behind it, tag 2 ahead of it, tag 3 beside it on its left. Each gray car has a white circle at its base link, near its rear. A rust box joins the three circles: its back edge 5.85 m behind the blue car's center, its front edge 3.15 m ahead, its side 1.9 m out from the center line.
   :width: 75%
   :align: center

   The AV at the three poses where it just touches the obstacle.

.. admonition:: Reading the figure
   :class: tip

   Slide the AV, heading along the lane, around the obstacle until it just
   touches; its base link (white circle) marks the edge of the grown
   obstacle.

   - **Tag 1, behind:** 5.85 m behind the obstacle's center.
   - **Tag 2, ahead:** 3.15 m ahead.
   - **Tag 3, beside:** 1.9 m out.

Take the AV heading along the lane, the same way as the obstacle. Measure
from the obstacle's center, along its length and across it. The two bodies
overlap when all three of these hold:

1. **From behind:** the AV's front, 3.6 m ahead of its base link, reaches
   the obstacle's rear, 4.5 / 2 = 2.25 m behind its center. So the base
   link is less than 2.25 + 3.6 = 5.85 m behind the center.
2. **From ahead:** the AV's rear, 0.9 m behind its base link, has not
   cleared the obstacle's front, 2.25 m ahead. So the base link is less
   than 2.25 + 0.9 = 3.15 m ahead of the center.
3. **Across:** the half widths add up. The base link is less than
   0.95 + 0.95 = 1.9 m to either side.

.. important::

   The region the base link must avoid is 5.85 + 3.15 = 9.0 m long and
   1.9 + 1.9 = 3.8 m wide. It reaches farther behind the obstacle than
   ahead, because the base link sits near the AV's rear.

.. tip::

   See "C-Space for Two Boxes" in :doc:`Going Further <l9_appendix>` for
   the region for two boxes, in general.


.. _l9-lec-point:

Step 2: the AV Becomes a Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 2 keeps only the AV's base link: a pose collides when that point is inside
the grown obstacle. This section works out where the grown obstacle is on our
road.

.. figure:: /_static/images/L9/cspace_region.png
   :alt: A top view in the obstacle's own frame, along it to the right and across it upward, in meters. The obstacle, the blue car, sits at the center. A rust hatched box 9.0 meters long and 3.8 meters wide surrounds it, reaching from minus 5.85 to plus 3.15 along and from minus 1.9 to plus 1.9 across. Four white dots mark the AV's base link at four poses: tag 1 inside the box, behind the car and to its left; tag 2 inside the box, beside the car on its right; tag 3 outside the box, behind it; tag 4 outside the box, 3.8 meters to the car's left.
   :width: 70%
   :align: center

   The region the base link must avoid, for the AV heading along the
   obstacle.

.. admonition:: Reading the figure
   :class: tip

   The axes follow the obstacle: along it to the right, across it to the
   obstacle's left upward, both in meters, with the obstacle's center at 0.
   The rust hatched box is the region the AV's base link must avoid: 9.0 m
   long (from −5.85 to +3.15) and 3.8 m wide (from −1.9 to +1.9).

   Each white dot is the AV's base link at one pose; the AV's body is not
   drawn.

   - **Tags 1 and 2:** inside the box, so those poses collide.
   - **Tags 3 and 4:** outside the box, so those poses are free. Tag 4 is on
     the left lane's center, 3.8 m to the obstacle's left.

Where the grown obstacle lies on our road, in meters along the stretch and
across the lane, is worked out in the appendix: :ref:`l9-app-cspace-road`.


.. _l9-lec-heading:

The Region Changes with the Heading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The grown obstacle from Step 1 holds for the AV heading along the obstacle. Turn
the AV by 30° and the grown obstacle changes shape.

.. figure:: /_static/images/L9/cspace_heading.png
   :alt: The same top view, along the obstacle and across it in meters. The solid rust box is the region for the AV heading along the obstacle. A dashed rust outline, wider and slanted, is the region for the AV turned 30 degrees: it reaches lower and farther to the right. Tag 1: the AV turned 30 degrees, above the obstacle, its base link on the dashed outline. Tag 2 sits beside the dashed outline on the right.
   :width: 70%
   :align: center

   The region for two AV headings.

.. admonition:: Reading the figure
   :class: tip

   The same axes as the figure before.

   - **Solid rust box:** the region for the AV heading along the obstacle,
     as before.
   - **Tag 2, dashed rust outline:** the region for the AV turned 30° to its
     left. It reaches lower and farther to the right than the box.
   - **Tag 1:** the turned AV touching the obstacle. Its base link is on the
     dashed outline.

- Each heading gives its own region, so the obstacle region depends on all
  three numbers :math:`(x, y, \theta)`.
- For a turned AV the grown obstacle is no longer a box, and each heading needs
  its own. So the next sections use the direct check, made cheap: three circles
  cover the AV's body at each pose.


.. _l9-lec-heading-grow:

Step 1 Again: Grow the Obstacle for the Turned AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The dashed outline comes from Step 1, done with the AV turned 30° to its left.

.. figure:: /_static/images/L9/cspace_heading_grow.png
   :alt: A top view in the obstacle's own frame, along it to the right and across it upward, in meters. The blue car sits at the center. Four gray copies of the AV, each turned 30 degrees to its left, sit around it: behind it, above it, ahead of it and below it, each just touching it. Each copy's base link is a white dot. A dashed rust outline runs through the four dots and around the obstacle: straight pieces along and across, joined by slanted pieces.
   :width: 70%
   :align: center

   Step 1 for the AV turned 30°.

1. Keep the AV turned 30°. Move it around the obstacle and stop each time it
   just touches it (the gray copies show four of these poses).
2. Mark the base link at each touching pose (white dots).
3. Join the marks all the way around: the dashed outline. With its base link
   inside, the turned AV overlaps the obstacle.

Each slanted piece is where an edge of the turned AV slides along a corner of
the obstacle. So the outline is no longer a box.


.. _l9-lec-sideways:

The AV Cannot Move Sideways
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The wheels roll; they do not slide. So the base link always moves along the heading, and the AV turns only by steering. Two
limits follow.

.. figure:: /_static/images/L9/turn_limits.png
   :alt: A top view of the AV, a black car heading right, its base link a white dot near the rear. Tag 1: two dashed arcs start at the base link and curve forward, one to the left and one to the right, each around a center marked with a plus sign beside the AV; an arrow marked 3.41 m runs from the upper center to the end of the left arc. Tag 2: an arrow pointing straight up from the AV's left side.
   :width: 40%
   :align: center

   What the AV can do, and what it cannot.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** the base link's path in the tightest turn, to the left and to
     the right. Each arc turns around a center (plus sign) 3.41 m to the side.
   - **Tag 2:** a sideways move: the AV cannot make it.

- **The tightest turn:** radius :math:`R = L / \tan\delta_\text{max}`,
  with :math:`L` the wheelbase and :math:`\delta_\text{max}` the largest
  steering angle. With :math:`L` = 2.875 m and :math:`\delta_\text{max}` =
  0.7 rad (40.1°):

  1. tan 0.7 = 0.842;
  2. :math:`R` = 2.875 / 0.842 = 3.41 m.

- **A comfortable turn:** at speed :math:`v` on a curve of radius
  :math:`R`, the sideways acceleration is :math:`v^2 / R`. With a limit of
  3 m/s² at 10 m/s: :math:`R` ≥ 10² / 3 = 33.3 m.

The wheelbase and the 3 m/s² limit are chosen; the 0.7 rad steering limit is
GP4's. GP4's vehicles have wheelbases of 2.3 to 3.0 m, and GP4 uses a
stricter 2.0 m/s².


.. _l9-lec-rule-out:

What the Two Limits Rule Out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The planners later in this lecture keep both limits.

.. important::

   A drivable path has no corners (the heading never jumps), and no turn has
   a radius under 3.41 m. At 10 m/s, comfort needs a radius of 33.3 m or
   more: 33.3 / 3.41 = 9.8, about ten times the tightest turn.

1. **Sampling drops every candidate that turns harder than 3 m/s²:** 4 of
   the 31 on our road (:ref:`l9-lec-drop`).
2. **A path with corners cannot be driven as it is.** RRT's garage path has
   them (:ref:`l9-lec-rrt-garage`). Hybrid A* builds its path from arcs no
   tighter than 3.41 m (:ref:`l9-lec-hybrid`).
3. **The AV cannot slide into a parking spot.** Hybrid A*'s path drives
   24.0 m forward, switches once, and backs 6.6 m into the spot
   (:ref:`l9-lec-hybrid-garage`).


.. _l9-lec-cspace-summary:

Where Configuration Space Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where configuration space leaves us
   :class: tip

   - The AV is one point :math:`(x, y, \theta)`; the obstacle is the
     region that point must avoid.
   - For the AV heading along the lane, that region is 9.0 m by 3.8 m. The
     left lane's center is outside it.
   - A path has no corners, and no turn radius under 3.41 m (steering). At
     10 m/s, comfort needs 33.3 m or more.


.. _l9-lec-frenet:

The Frenet Frame
----------------

We keep configuration space: every pose is still :math:`(x, y, \theta)`, and
it is still checked for collisions. We add a second way to write positions:
along the road and across it, instead of the map's :math:`x` and :math:`y`.

**What it is for:** "stay in the lane" and "move one lane left" become
statements about one number, :math:`d`.


.. _l9-lec-frenet-def:

Two Coordinates That Follow the Road
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Frenet frame
   :class: note

   Coordinates attached to a reference path. :math:`s` is the distance along
   the reference from its start; :math:`d` is the distance across it,
   positive to the left of the driving direction.

.. figure:: /_static/images/L9/frenet_def.png
   :alt: A top view of a piece of the stretch where it starts to curve upward, a left turn for the AV, x and y in meters. The reference path, the right lane's center, is a thick black line with small ticks every 5 meters labeled 120 to 155 below the road: the value of s. A dark point P sits in the left lane; a white dot on the reference marks its foot point; a dark dashed arrow from the foot point to P is d. A legend names the reference path (d = 0), the point P, its foot point on the reference, and d from the foot point to P.
   :width: 80%
   :align: center

   A point P and its two Frenet coordinates.

.. admonition:: Reading the figure
   :class: tip

   A top view of the stretch where it starts to curve left, :math:`x` and
   :math:`y` in meters.

   - The thick black line is the reference path, the right lane's center
     (:math:`d` = 0). Its ticks mark :math:`s` every 5 m, from 120 to 155.
   - The dark dot is a point P in the left lane.
   - The white dot is P's **foot point**: the nearest point to P on the
     reference. It gives :math:`s`.
   - The dashed arrow from the foot point to P is :math:`d`.

Our reference comes from the route: the right lane's center. P is at
:math:`s` = 140 m, :math:`d` = 3.0 m.


.. _l9-lec-unrolled:

The Road Becomes Straight in (s, d)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/frenet_unrolled.png
   :alt: Two plots. Top: the whole stretch on the map, x and y in meters, two lanes going right and curving up, with ticks at s = 100, 150 and 200, the AV as a black dot and the obstacle as a blue square. Bottom: the same road in s and d, both in meters: three straight horizontal lines at d = minus 1.75, 1.75 (dashed) and 5.25, the AV at s = 60, d = 0 and the obstacle at s = 118, just below d = 0.
   :width: 75%
   :align: center

   The same road on the map and in :math:`(s, d)`.

.. admonition:: Reading the figure
   :class: tip

   - **Top, a top view:** the whole stretch on the map, with ticks at
     :math:`s` = 100, 150 and 200 m. The black dot is the AV; the blue
     square is the obstacle.
   - **Bottom, a graph, not a picture of the road:** the same road with
     :math:`s` along and :math:`d` across. Its :math:`d` axis is stretched,
     and curves do not show. The lane edges become straight lines. The AV is
     at :math:`s` = 60 m, :math:`d` = 0; the obstacle at :math:`s` = 118
     m, just below :math:`d` = 0.

In :math:`(s, d)`, every lane edge is a line of constant :math:`d`:

- the right lane's right edge, :math:`d` = −1.75 m;
- the lane line, :math:`d` = +1.75 m;
- the left lane's left edge, :math:`d` = +5.25 m.

"Stay in the right lane": keep :math:`d` near 0. "Move to the left lane":
bring :math:`d` to 3.5 m.


.. _l9-lec-frenet-step1:

Step 1: Find the Nearest Point on the Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The obstacle's center in the map frame (chosen for this example) is
:math:`P` = (155.690, −207.435) m. The reference is a chain of points, about
0.5 m apart.

1. Of all the pieces of the chain, the one closest to :math:`P` runs from
   :math:`A` = (155.225, −207.141) to :math:`B` = (155.750, −207.134). It is
   0.525 m long.
2. Draw the line from :math:`P` that meets that piece at a right angle. It
   meets it 0.879 of the way from :math:`A` to :math:`B` (:math:`t` =
   0.879).
3. That point is the **foot point**:
   :math:`F = A + 0.879\,(B - A)` = (155.686, −207.135).


.. _l9-lec-frenet-step23:

Step 2 and Step 3: Read s and d
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Step 2, read** :math:`s`: the distance along the reference up to :math:`F`.

1. :math:`A` is 117.539 m along the reference: the lengths of all the pieces
   before it, added up.
2. :math:`s` = 117.539 + 0.879 × 0.525 = 117.539 + 0.461 = 118.00 m.

**Step 3, read** :math:`d`: the distance from :math:`F` to :math:`P`, with a
sign.

3. :math:`P - F` = (0.004, −0.300) m.
4. The piece from :math:`A` to :math:`B` heads 0.705° left of the map's
   :math:`x` axis, so its left direction is :math:`n` = (−0.012, 1.000).
5. :math:`d = n \cdot (P - F)` = (−0.012)(0.004) + (1.000)(−0.300) =
   −0.300 m.

.. important::

   The obstacle is at :math:`s` = 118.00 m, :math:`d` = −0.30 m: 0.3 m to
   the right of the right lane's center, 58 m ahead of the AV at
   :math:`s` = 60 m.


.. _l9-lec-frenet-back:

Back from (s, d) to the Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A planner works in :math:`(s, d)`, but the controller and the collision
check need map coordinates. Example: the left lane's center beside the
obstacle, :math:`(s, d)` = (118, 3.5).

1. The reference at :math:`s` = 118 m: :math:`r` = (155.686, −207.135),
   heading 0.81°. The script averages the heading over nearby points; the
   piece :math:`A` to :math:`B` alone gives 0.705°.
2. Its left direction:
   :math:`n = (-\sin 0.81^\circ,\ \cos 0.81^\circ)` = (−0.0141, 0.9999).
3. Step :math:`d` along it, :math:`p = r + 3.5\,n`:

   - :math:`x` = 155.686 + 3.5 × (−0.0141) = 155.637 m;
   - :math:`y` = −207.135 + 3.5 × 0.9999 = −203.635 m.

.. important::

   :math:`p(s, d) = r(s) + d\,n(s)`: the point on the reference, then
   :math:`d` meters to its left.

.. tip::

   See "The Frenet Formulas" in :doc:`Going Further <l9_appendix>`.


.. _l9-lec-frenet-fails:

Where the Frenet Frame Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On a curve, the lines across the road (constant :math:`s`) all point at the
curve's center.

1. On a left curve of radius :math:`R`, the center is :math:`R` to the left
   of the reference. A point there sits on every line across, so its
   :math:`s` is not defined.
2. The formulas for a path's heading and curvature in :math:`(s, d)` carry
   the factor :math:`1 - d/R`, written :math:`1 - \kappa d` with the
   curvature :math:`\kappa = 1/R` (see "The Frenet Formulas" in
   :doc:`Going Further <l9_appendix>`). It must stay above 0.
3. Our reference: the tightest curve has :math:`R` = 61.9 m. The candidates
   reach :math:`d` = 4.0 m: 1 − 4.0 / 61.9 = 0.935, well above 0.

.. important::

   Check :math:`1 - \kappa d` where :math:`R` is small and :math:`d` is
   large: a tight junction turn.


.. _l9-lec-handson-scene:

Hands-On, Part 1: the Road in Two Frames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The hands-on script is in the course's Python repo, folder ``lecture9``
(`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture9>`__).
Its ``scene`` part shows the road in the map and in the Frenet frame. It
needs numpy and matplotlib only, and no CARLA server: ``export_scene.py``
read the road once from CARLA's Town03 map. The commands are on
:doc:`the Code page <l9_code>`.

.. admonition:: What to look at
   :class: hint

   1. Move the point P with the :math:`s` and :math:`d` sliders. In the map
      it follows the curve; in :math:`(s, d)` it moves on straight lines.
   2. The title converts P to the map and back. Set :math:`s` = 118,
      :math:`d` = 3.5: do you get (155.64, −203.64), the point you worked out
      by hand in "Back from (s, d) to the Map"?
   3. Set :math:`d` = 5.25 and move :math:`s` through the curve: the point
      stays on the left lane's left edge.

.. dropdown:: Answers, from the script
   :class-container: sd-border-success

   2. Yes. With :math:`s` = 118 and :math:`d` = 3.5, the title reads
      P = (155.64, −203.64) m, the hand result rounded to two decimals. Back
      to Frenet, it reads :math:`s` = 117.99 m, :math:`d` = 3.50 m: the round
      trip through the map moves :math:`s` by 0.01 m.


.. _l9-lec-frenet-summary:

Where the Frenet Frame Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where the Frenet frame leaves us
   :class: tip

   - :math:`s` along the route's reference path, :math:`d` across it, left
     positive.
   - The obstacle: :math:`s` = 118.00 m, :math:`d` = −0.30 m (nearest
     point, then distance along, then signed distance across).
   - Lanes are lines of constant :math:`d`: the right lane at 0, the left
     lane at 3.5 m.
   - The frame holds while :math:`1 - \kappa d > 0`: here 0.935 at the
     worst.


.. _l9-lec-sampling:

Sampling Paths
--------------

We draw 31 candidate paths in :math:`(s, d)`, drop the ones that collide,
score the rest and keep the cheapest.

**What it is for:** it gives a path around the obstacle that is
comfortable, keeps its distance and stays on the route.


.. _l9-lec-rollout:

Roll Out Paths with Sideways Shifts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stanford's Junior drove the 2007 DARPA Urban Challenge this way. It rolled
out one path parallel to the lane's center, and more paths shifted sideways
from it.

Our planner does the same, in five steps:

1. **Generate** candidate paths: the reference path, shifted sideways.
2. **Check** each one: drop it if the AV would hit something, or turn too
   hard.
3. **Score** the rest with a cost.
4. **Pick** the cheapest.
5. **Repeat** every 0.5 s, from where the AV is then.


.. _l9-lec-scurve:

Step 1: One Candidate, a Smooth Move Sideways
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/lateral_curve.png
   :alt: A graph of d against s, both in meters, from s = 55 to 120, with the lane edges as horizontal lines at minus 1.75, 1.75 (dashed) and 5.25. Three curves start at the AV, s = 60 and d = 0, flat, rise in an S shape and level off at d = 3.5: a solid one reaches 3.5 at s = 80 (tag 1), a dashed one at s = 90 (tag 2), a dotted one at s = 100 (tag 3). After that each stays at 3.5.
   :width: 80%
   :align: center

   Three moves to the left lane's center, over three lengths.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a picture of the road: :math:`d` against :math:`s`, with the
   :math:`d` axis stretched. The gray lines are the lane edges and, dashed,
   the lane line. All three curves start at the AV (:math:`s` = 60 m,
   :math:`d` = 0) and end at :math:`d_\text{end}` = 3.5 m.

   - **Tag 1, solid:** over 20 m, so it reaches 3.5 m at :math:`s` = 80 m.
   - **Tag 2, dashed:** over 30 m, so at :math:`s` = 90 m.
   - **Tag 3, dotted:** over 40 m, so at :math:`s` = 100 m.

- A candidate has two numbers: where it ends, :math:`d_\text{end}`, and over
  how much road it gets there, the **maneuver length**. After that it keeps
  :math:`d_\text{end}`.
- The S shape starts and ends flat, with no bend.

.. tip::

   See "The S Curve" in :doc:`Going Further <l9_appendix>` for the S
   curve's formula.


.. _l9-lec-candidate-set:

Step 1: the Candidate Set
~~~~~~~~~~~~~~~~~~~~~~~~~

**Chosen for this example:**

- 10 end offsets: :math:`d_\text{end}` from −0.5 m to 4.0 m, every 0.5 m;
- 3 maneuver lengths: 20, 30 and 40 m;
- 1 more: keep the lane and **stop behind** the obstacle, the AV's front
  bumper 2.0 m short of the obstacle's rear.

In all: 10 × 3 + 1 = 31 candidates. The 30 shifts are each 70 m long.

**Why those offsets:** the AV's body reaches 0.95 m to each side, and the
two lanes run from :math:`d` = −1.75 to 5.25 m.

1. Lowest: −0.5 − 0.95 = −1.45, inside −1.75.
2. Highest: 4.0 + 0.95 = 4.95, inside 5.25.


.. _l9-lec-drop:

Step 2: Drop Paths That Collide or Turn Too Hard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/candidates_frenet.png
   :alt: A graph of d against s, both in meters, with all 31 candidates from the AV at s = 60. The obstacle is a blue box at s = 116 to 120, d around 0. Thin rust curves end at d from minus 0.5 to 2.0 and run into or beside the obstacle: they collide. Purple dashed curves rise steeply to 2.5 to 4.0 within 20 meters: too sharp. Gray curves end at 2.5 to 4.0 after 30 or 40 meters. One thick green curve ends at 3.5 after 40 meters. A black dotted line stays at d = 0 and ends with a bar at s = 110: stop behind. A legend names cheapest, kept, stop behind, collides and too sharp.
   :width: 90%
   :align: center

   All 31 candidates, sorted by what happens to them.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a picture of the road: :math:`d` against :math:`s`, with the
   :math:`d` axis stretched. The blue box is the obstacle, at :math:`s` =
   116 to 120 m.

   - **Rust, collides:** the curves that end at :math:`d` from −0.5 to
     2.0 m. They run into the obstacle or too close beside it.
   - **Purple dashed, too sharp:** the 20 m moves to 2.5 to 4.0 m.
   - **Gray, kept:** the 30 m and 40 m moves to 2.5 to 4.0 m.
   - **Green, cheapest:** 3.5 m over 40 m (Step 4).
   - **Black dotted, stop behind:** stays at :math:`d` = 0 and ends with a
     bar at :math:`s` = 110 m.

- **18 collide** (rust): the AV on them comes within 0.3 m of the obstacle
  (see the Collision Checking section).
- **4 are too sharp** (purple): over 3 m/s² sideways.
- **9 are kept**, stop behind included.

.. tip::

   See "How Hard a Candidate Turns, by Hand" in :doc:`Going Further
   <l9_appendix>` for an estimate of the peak by hand.


.. _l9-lec-cost-terms:

Step 3: the Four Cost Terms
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each kept candidate gets a cost; lower is better. All weights are
**chosen** for this example.

.. list-table::
   :widths: 16 52 32
   :header-rows: 1
   :class: compact-table

   * - **Term**
     - **What it measures**
     - **Weight**
   * - Comfort
     - the peak sideways acceleration along the path
     - 2 per m/s²
   * - Clearance
     - how far the smallest gap to the obstacle falls under 1.5 m
     - 4 per m
   * - Lane
     - lanes away from the route's lane; meters off a lane center
     - 2 per lane; 2 per m
   * - Progress
     - meters of the 70 m ahead the path does not cover
     - 0.5 per m

.. important::

   1 m/s² of extra sideways acceleration costs as much as 4 m of lost
   progress (2 = 0.5 × 4). Change a weight and a different path can win; the
   spreadsheet exercise and the hands-on let you try it.


.. _l9-lec-score-a:

Step 3: Score Candidate A, the Left Lane over 40 m
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Candidate A: :math:`d_\text{end}` = 3.5 m, maneuver 40 m. The numbers in the
steps are the script's, rounded.

1. **Comfort:** peak 1.25 m/s². 2 × 1.253 = 2.51.
2. **Clearance:** smallest gap 1.36 m (the gap is defined in the Collision
   Checking section). 4 × (1.5 − 1.359) = 0.56.
3. **Lane:** one lane from the route's, on the left lane's center.
   2 × 1 + 2 × 0 = 2.00.
4. **Progress:** it covers all 70 m. 0.5 × 0 = 0.

.. important::

   Cost of A: 2.51 + 0.56 + 2.00 + 0 = 5.07.


.. _l9-lec-score-b:

Step 3: Score Candidate B, Closer to the Obstacle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Candidate B: :math:`d_\text{end}` = 3.0 m, maneuver 40 m. It moves 0.5 m
less, so it bends less, but it passes closer.

1. **Comfort:** peak 1.08 m/s². 2 × 1.076 = 2.15.
2. **Clearance:** smallest gap 0.86 m. 4 × (1.5 − 0.859) = 2.56.
3. **Lane:** one lane from the route's, 0.5 m off the left lane's center.
   2 × 1 + 2 × 0.5 = 3.00.
4. **Progress:** 0.

.. important::

   Cost of B: 2.15 + 2.56 + 3.00 + 0 = 7.71 (7.72 unrounded). B saves 0.36 on
   comfort and pays 2.00 more on clearance and 1.00 more on the lane.


.. _l9-lec-score-c:

Step 3: Score Candidate C, Stop Behind
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Candidate C keeps the right lane and stops its front bumper 2.0 m short of
the obstacle's rear. Its base link stops at 118 − 2.25 − 2.0 − 3.6 = 110.15 m:
from the obstacle's center, back by half the obstacle's 4.5 m, by the gap,
and by the distance from the AV's front to its base link.

1. **Comfort:** the path is straight. 2 × 0.000 = 0.00.
2. **Clearance:** 2.0 m lie between the bumpers, but the collision check
   measures from circles that reach past them (see the Collision Checking
   section): smallest gap 1.10 m. 4 × (1.5 − 1.096) = 1.62.
3. **Lane:** the route's lane, centered. 0.
4. **Progress:** it covers 110.15 − 60 = 50.15 m of 70 m.
   0.5 × (70 − 50.15) = 9.93.

.. important::

   Cost of C: 0 + 1.62 + 0 + 9.93 = 11.55 (11.54 unrounded). Stopping costs
   nothing for comfort or the lane, but the 19.85 m of lost progress costs
   9.93.


.. _l9-lec-spreadsheet:

Exercise: Score Every Candidate in a Spreadsheet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In class, in pairs. Open ``candidates.csv``, from folder ``lecture9`` of the
course's Python repository (see :doc:`the Code page <l9_code>`), in Excel,
Google Sheets or LibreOffice Calc. It has one row per candidate: the
numbers each cost term needs, and no costs.

1. Put the five weights of the cost terms in cells of their own.
2. Add one column per cost term and a total. Skip the rows the ``dropped``
   column names: the planner drops them before it scores.
3. Sort by the total. Is A first, at 5.07?
4. Set the clearance weight to 10 and sort again. Which path wins, and
   where does it end?
5. Set the progress weight to 0. What does the AV do now, and why?

The answers are in Exercise 8 of :doc:`l9_exercises`.


.. _l9-lec-cheapest:

Step 4: the Cheapest Path, on the Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/candidates_map.png
   :alt: A top view, to scale, of the 31 candidates on the road from the AV at the left to past the obstacle, x and y in meters. Rust lines run into the obstacle; purple dashed lines bend sharply into the left lane; gray lines move into the left lane more gently; a black dotted line stops behind the obstacle; one thick green line moves into the left lane and passes the obstacle. A legend names cheapest, kept, stop behind, collides and too sharp.
   :width: 95%
   :align: center

   The 31 candidates on the map, to scale.

.. admonition:: Reading the figure
   :class: tip

   The same candidates as in Step 2, now drawn on the road to scale, with
   the same colors. Rust lines run into the obstacle; purple dashed lines
   bend sharply into the left lane; gray lines move into it more gently; the
   black dotted line stops behind the obstacle. The thick green line, the
   cheapest, moves into the left lane and passes the obstacle.

.. list-table::
   :widths: 14 62 24
   :header-rows: 1
   :class: compact-table

   * - **Rank**
     - **Candidate**
     - **Cost**
   * - 1
     - A: 3.5 m over 40 m
     - 5.07
   * - 2
     - 4.0 m over 40 m
     - 5.86
   * - 3
     - 3.5 m over 30 m
     - 6.99
   * - 4
     - B: 3.0 m over 40 m
     - 7.72
   * - 5 to 7
     - 4.0 and 3.0 m over 30 m; 2.5 m over 40 m
     - 8.04 to 10.40
   * - 8
     - C: stop behind
     - 11.54
   * - 9
     - 2.5 m over 30 m
     - 11.74


.. _l9-lec-replan:

Step 5: Plan Again Every 0.5 s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/drive_snapshots.png
   :alt: Three top views of the stretch, one above the other, tagged 1 to 3, x and y in meters. In each, the obstacle is blue in the lower lane and the AV is black; both are drawn about twice their true size so they show. 1: the AV at the start, its green path moving into the upper lane. 2: the AV halfway into the upper lane, a dotted trail behind it, its green path continuing in the upper lane into the curve. 3: the AV beside the obstacle in the upper lane, its green path moving back into the lower lane in the curve.
   :width: 70%
   :align: center

   The AV's plan at 0, 3 and 6 s.

.. admonition:: Reading the figure
   :class: tip

   Three moments of the same drive, from above. The obstacle (blue) and
   the AV (black) are drawn about twice their true size so they show. The
   green line is the cheapest path at that moment; the dotted line is where
   the AV has been.

   - **Tag 1, at 0 s:** the AV at the start. Its path moves into the upper
     (left) lane.
   - **Tag 2, at 3 s:** the AV halfway into the left lane. Its path goes on
     in that lane into the curve.
   - **Tag 3, at 6 s:** the AV beside the obstacle, in the left lane. Its
     path moves back into the right lane, in the curve.

Every 0.5 s the AV drives the first 0.5 s of the cheapest path, then plans
again from where it is.

- The AV is in the left lane (:math:`d` > 1.75 m) from about :math:`s` = 85
  to 135 m.
- From :math:`s` = 115 m, still beside the obstacle, the cheapest path
  already heads back to :math:`d` = 0. The AV crosses the lane line after
  the obstacle is behind it. It is back on its lane's center by
  :math:`s` = 160 m.


.. _l9-lec-demo:

Demo: the Same Planner in CARLA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ROS 2 package ``l9_planning_demo``, in the course's ROS repository
(`its README <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l9_planning_demo/README.md>`__),
runs this planner on the same stretch of Town03, with the obstacle at
:math:`s` = 118 m:

.. code-block:: bash

   ros2 launch l9_planning_demo demo.launch.py
   ros2 param set /planning_demo w_clearance 10.0

- RViz draws every candidate in the colors of these figures, and the AV's
  circles.
- Every 0.5 s the AV moves along the first 0.5 s of the cheapest path, then
  plans again. The demo places the AV on the path; L10 adds the controller
  that drives it.
- A changed weight takes effect at the next plan: the path changes while you
  watch.


.. _l9-lec-handson-sample:

Hands-On, Part 2: Sample, Score, Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``sample`` part draws every candidate with its costs; the ``drive`` part
plans again every 0.5 s. The commands are on :doc:`the Code page
<l9_code>`.

.. admonition:: What to look at
   :class: hint

   1. In ``sample``, read the table: do A, B and C have the costs of the
      last sections?
   2. Move the obstacle to :math:`s` = 90 m. How many candidates survive?
   3. In ``drive``, step through the plans: when does the AV start back?

.. dropdown:: Answers, from the script
   :class-container: sd-border-success

   1. Yes. The table ranks the nine kept candidates: A is rank 1 at 5.07, B
      rank 4 at 7.72 and C (``stop``) rank 8 at 11.54.
   2. 8 of the 31: 7 shifts and stop behind. 19 collide and 4 are too sharp.
      The cheapest is then 4.0 m over 40 m, at 6.80.
   3. At :math:`t` = 5.5 s, with the AV at :math:`s` = 115 m: the plan
      changes from :math:`d_\text{end}` = 3.5 m to :math:`d_\text{end}` = 0.


.. _l9-lec-fifth-term:

Exercise: a Fifth Cost Term
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In class, in pairs. The road has two lanes each way. The left lane's left
edge, at :math:`d` = 3.5 + 1.75 = 5.25 m, is the road's center line: past
it, traffic comes the other way. No cost term sees it. With the clearance
weight at 10, the cheapest path ends at :math:`d` = 4.0 m: its left side,
half the AV's 1.9 m width to the left, is 5.25 − (4.0 + 0.95) = 0.30 m from
the line. The commands are on :doc:`the Code page <l9_code>`.

1. In ``l9_exercise.py``, write ``edge_cost(path)``: like clearance, 4 per
   meter that the gap to the center line falls under 1.5 m, at the path's
   worst point.
2. Run ``l9_check.py`` until its five checks pass.
3. Run the sample part with ``--extra``: which path wins, and at what cost?
4. Set ``W_EDGE`` to 10. Which path wins now, and what does the AV give up?

The answers are in Exercise 9 of :doc:`l9_exercises`.


.. _l9-lec-sampling-summary:

Where Sampling Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where sampling leaves us
   :class: tip

   - 31 candidates: 18 collide, 4 turn too hard (over 3 m/s²), 9 are
     scored.
   - Cheapest: A, the left lane over 40 m, cost 5.07. B (closer to the
     obstacle) 7.72; C (stop behind) 11.54.
   - Planned again every 0.5 s, the AV passes in the left lane from about
     85 m to 135 m and is back on its lane's center by 160 m.


.. _l9-lec-collision:

Collision Checking
------------------

We build a quick test of whether the AV's body overlaps the obstacle at
one pose.

**What it is for:** the sampling planner's Step 2 runs this test at every
point of every candidate: 4,332 poses, every 0.5 s.

Each candidate has a point every 0.5 m: 70 / 0.5 = 140 steps, so 141 points.
Stop behind ends 50.15 m ahead: 101 points, plus its end point, 102. In all,
30 × 141 + 102 = 4,332.


.. _l9-lec-circles:

Cover the AV with Three Circles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/circles_cover.png
   :alt: The AV from above, 4.5 meters long and 1.9 meters wide, facing right, split into three 1.5 meter pieces marked along the top. Three equal black circles, one per piece, cover the body; each center is a dark plus sign. Tag 1 below the rear circle, joined by a thin line, marks the base link, a white dot next to the rear circle's center. Tag 2, above the body, marks a dark arrow from the middle circle's center to the corner of its piece: the radius. Tag 3 below the front circle, joined by a thin line, marks its center.
   :width: 60%
   :align: center

   Three circles that cover the AV's body.

.. admonition:: Reading the figure
   :class: tip

   The AV from above, facing right, 4.5 m long and 1.9 m wide, cut into
   three pieces of 1.5 m. One circle per piece covers the body; each circle's
   center is a plus sign.

   - **Tag 1:** the base link (white dot), next to the rear circle's center.
   - **Tag 2:** a circle's radius, from the middle circle's center to the
     corner of its piece.
   - **Tag 3:** a circle's center, the front one.

**Why circles:** two circles overlap exactly when their centers are closer
than the sum of their radii. The **gap** is the distance between the centers
minus the two radii; under 0, the circles overlap. Each pair needs one
distance, whatever the headings.

Three circles on the AV and three on the obstacle give 3 × 3 = 9 distances
per pose.


.. _l9-lec-radius:

Step 1: the Radius and the Centers, by Hand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cut the 4.5 m by 1.9 m body into three pieces, each 4.5 / 3 = 1.5 m long.
One circle per piece, centered on it, must reach the piece's corners.

1. A corner is 1.5 / 2 = 0.75 m along and 1.9 / 2 = 0.95 m across from the
   piece's center.
2. Radius: :math:`r = \sqrt{0.75^2 + 0.95^2} = \sqrt{0.5625 + 0.9025} =
   \sqrt{1.465}` = 1.21 m.
3. Centers: 0.75, 2.25 and 3.75 m from the rear bumper. The base link is
   0.9 m from it, so the rear center is 0.9 − 0.75 = 0.15 m behind the base
   link, and the others 2.25 − 0.9 = 1.35 and 3.75 − 0.9 = 2.85 m ahead of
   it.

.. important::

   For a pose :math:`(x, y, \theta)`, circle :math:`k` is centered at
   :math:`(x + o_k \cos\theta,\ y + o_k \sin\theta)`, with :math:`o_k` =
   −0.15 (behind), 1.35 or 2.85 m.

.. tip::

   See "More or Fewer Circles" in :doc:`Going Further <l9_appendix>`.


.. _l9-lec-margin:

The Margin: How Close Counts as a Collision
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our check calls a pose a collision when the gap is under 0.3 m.

The AV does not know its own pose exactly. A published requirement allows at
most 0.29 m of error on a local street (Reid et al., 2019, on :doc:`the
References page <l9_references>`). We round it to 0.3 m.

.. important::

   The 0.3 m covers only the AV's own position. The obstacle's position
   comes from perception, and a moving car's from prediction, with more
   error. A margin for them would add to it.


.. _l9-lec-one-pose:

Step 2: One Pose, Checked by Hand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/circle_check.png
   :alt: A close top view beside the obstacle, x and y in meters. The AV, black with three black circles, is in the upper lane; the obstacle, blue with three blue circles, is in the lower lane right below it, the circles side by side. A dark double arrow spans the gap between the two middle circles, across the dashed lane line. Tag 1 sits just right of the arrow, below the dashed lane line.
   :width: 70%
   :align: center

   The AV on candidate A, beside the obstacle.

.. admonition:: Reading the figure
   :class: tip

   A close top view, :math:`x` and :math:`y` in meters. The AV (black, with
   its three black circles) is in the upper lane; the obstacle (blue, with
   its three blue circles) is right below it in the lower lane. Their
   circles line up in pairs.

   - **Tag 1:** the gap between the two middle circles (the double arrow),
     across the dashed lane line.

The AV on candidate A, beside the obstacle: base link at :math:`s` = 116.65 m,
:math:`d` = 3.5 m. Its middle circle is at 116.65 + 1.35 = 118 m, the
obstacle's center, so the circles line up.

1. Centers across: the AV is 3.5 m left of the reference and the obstacle
   0.3 m right of it, so they are 3.5 + 0.3 = 3.8 m apart.
2. Gap (tag 1): 3.8 − 2 × 1.21 = 1.38 m.
3. The gap is over the 0.3 m margin, so this pose is free.

The script gets 1.37 m between the two middle circles at this pose (the lane
curves slightly here), and 1.36 m as the smallest gap along all of A.


.. _l9-lec-conservative:

Circles Can Report a Collision That Is Not There
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/circles_conservative.png
   :alt: Two cars side by side from above, the AV black on top and the obstacle, a blue car, below, each with its three circles. Tag 1 marks the gap between the two bodies on the right: 0.4 meters, the bodies do not touch. Small rust lens shapes show where each black circle overlaps the blue circle below it; tag 2, left of the cars at the height of the lenses, marks them.
   :width: 60%
   :align: center

   Two bodies that do not touch, with circles that overlap.

.. admonition:: Reading the figure
   :class: tip

   Two cars side by side from above: the AV (black) on top and the
   obstacle, a blue car, below, each with its three circles.

   - **Tag 1:** the gap between the two bodies, 0.4 m. The bodies do not
     touch.
   - **Tag 2:** the small rust lens shapes, where each black circle overlaps
     the blue circle below it.

Two cars side by side; the gap between their bodies (tag 1) is 0.4 m
(chosen).

1. Centers: 1.9 + 0.4 = 2.3 m apart.
2. Gap: 2.3 − 2 × 1.21 = −0.12 m, so the circles overlap (tag 2).

The circles bulge past the body: 1.21 − 0.95 = 0.26 m at the sides, and
1.21 − 0.75 = 0.46 m past each bumper.

.. important::

   The circles cover the whole body, so the check never misses a real
   collision. It can drop a path that was free, so the check is
   **conservative**.


.. _l9-lec-collision-summary:

Where Collision Checking Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where collision checking leaves us
   :class: tip

   - Three circles of radius 1.21 m, at −0.15, 1.35 and 2.85 m from the base
     link, cover the AV; 9 distances per pose.
   - Beside the obstacle on A: centers 3.8 m apart, gap 1.38 m by hand
     (1.36 m smallest along A).
   - Conservative: bodies 0.4 m apart already count as overlapping.
   - On the road, a gap under 0.3 m is a collision: a 0.29 m bound on the
     AV's position error, rounded.


.. _l9-lec-behavior:

Behavior
--------

We add the layer that picks the task the local planner carries out.

**What it is for:** the local planner finds the best path for a task; it
does not choose the task (pass or wait, park or keep searching).


.. _l9-lec-decides:

What the Behavior Layer Decides
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 46 54
   :header-rows: 1
   :class: compact-table

   * - **The behavior layer decides**
     - **The local planner then**
   * - which lanes the AV may use
     - samples :math:`d_\text{end}` only inside them
   * - where the AV must stop, and by when
     - keeps every path short of that :math:`s`
   * - a speed limit for this stretch
     - scores comfort at that speed

It decides from facts that change slowly: a lane is open or closed, a spot is
free or taken.


.. _l9-lec-one-decision:

One Decision Changes the Cheapest Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/behavior_restricted.png
   :alt: A top view of the road with the AV at the left and the obstacle ahead in the lower lane, x and y in meters. The upper lane is cross-hatched in gray: not allowed. Thin rust candidate lines stay in the lower lane and run into the obstacle. A thick green line stays in the lower lane and ends with a bar behind the obstacle. A legend names cheapest: stop behind, and collides.
   :width: 95%
   :align: center

   The candidates when the left lane is closed.

.. admonition:: Reading the figure
   :class: tip

   The road from above, the AV at the left and the obstacle ahead in the
   lower (right) lane. The upper (left) lane is cross-hatched: the behavior
   layer has closed it. The thin rust lines are candidates that stay in the
   right lane and collide with the obstacle. The thick green line, the
   cheapest, is stop behind: it stays in the lane and ends with a bar behind
   the obstacle.

Suppose prediction says a fast car is coming up in the left lane, and the
behavior layer closes that lane (hatched). The sampler keeps
:math:`d_\text{end}` ≤ 0.5 m, so the AV's body stays in the right lane:
0.5 + 0.95 = 1.45 m, inside the lane line at 1.75 m.

1. 3 end offsets (−0.5, 0 and 0.5 m) × 3 lengths + 1 = 10 candidates.
2. The 9 that are not stop behind all collide: at :math:`d_\text{end}` =
   0.5 m, the centers are 0.5 + 0.3 = 0.8 m apart across, under
   2 × 1.21 = 2.42 m.
3. Stop behind is the only one left, at cost 11.54: the AV waits.


.. _l9-lec-game:

The Lane Change as a Game
~~~~~~~~~~~~~~~~~~~~~~~~~

The last section closed the left lane because another car was coming up in
it. That car has a driver who chooses too, and each choice changes what is
best for the other.

- The AV chooses: **go** (move into the left lane now) or **wait** (stop
  behind the obstacle).
- The other car chooses: **keep** its speed, or **yield** (slow down and let
  the AV in).
- Each pair of choices costs each of them seconds of delay; a crash costs
  100. All numbers are chosen for this example.

.. admonition:: Definition: Nash equilibrium
   :class: note

   A choice for each player such that no player can lower its own cost by
   changing only its own choice. Named after John Nash, who introduced it in
   1950 (see :doc:`the References page <l9_references>`).


.. _l9-lec-nash-exercise:

Exercise: Find the Nash Equilibria
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each cell gives the AV's delay, then the other car's, in seconds (chosen).

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * -
     - **The other car keeps**
     - **The other car yields**
   * - **The AV goes**
     - crash: 100, 100
     - 0, 2
   * - **The AV waits**
     - 3, 0
     - 3, 2

With your neighbor, for each of the four cells:

1. Can the AV lower its delay by switching its row, the other car's choice
   fixed?
2. Can the other car lower its delay by switching its column, the AV's
   choice fixed?

A cell where both answers are no is a Nash equilibrium. How many does this
game have?


.. _l9-lec-two-equilibria:

Two Equilibria: the AV Goes First Only When It Is Sure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * -
     - **The other car keeps**
     - **The other car yields**
   * - **The AV goes**
     - crash: 100, 100
     - **0, 2** (equilibrium)
   * - **The AV waits**
     - **3, 0** (equilibrium)
     - 3, 2

- In (goes, yields), a switch costs the AV 3 instead of 0 and the other car
  100 instead of 2. In (waits, keeps), it costs the AV 100 instead of 3 and
  the car 2 instead of 0. Each of the other two cells has a player who gains
  by switching.
- Two equilibria: the game alone does not say which one happens.
- If the AV moves first and the other car sees it, the car's best answer is
  to yield (2 instead of 100): the AV gets 0. If the car keeps its speed
  anyway, they crash.

.. important::

   So the behavior layer goes first only when prediction says the other car
   will yield; otherwise it waits, at a cost of 3.


.. _l9-lec-fsm:

A Finite State Machine Picks One Behavior at a Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Finite state machine (FSM)
   :class: note

   A fixed list of **states**, of which the system is in exactly one at a
   time, and a list of **transitions**: each one moves the system from one
   state to another when its condition becomes true.

- Each state names a behavior and sets what the planner below receives:
  allowed lanes, a stop point, a speed limit, a goal pose.
- Junior used one, with 13 states.
- Every behavior and every way from one to another is on one diagram, and
  each transition has its own condition, so you can test each one by itself.


.. _l9-lec-valet:

An FSM for a Valet in a Parking Garage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/fsm_garage.png
   :alt: A state diagram with five rounded boxes. An arrow from the left enters Enter. Enter goes to Search the aisle, tag 1. Search the aisle goes to Approach the spot, tag 2, and Approach the spot goes back to Search the aisle, tag 3. Search the aisle has a loop back to itself, tag 6. Approach the spot goes down to Reverse in, tag 4, and Reverse in goes left to Parked, tag 5. Parked has a double border: the final state.
   :width: 75%
   :align: center

   The valet's states and transitions.

.. admonition:: Reading the figure
   :class: tip

   Each rounded box is a state; each arrow is a transition, numbered 1 to 6
   (the next table gives each one's condition). The arrow from the left
   enters the first state, Enter.

   - **1:** Enter to Search the aisle.
   - **2 and 3:** Search the aisle to Approach the spot, and back.
   - **6:** Search the aisle back to itself.
   - **4:** Approach the spot to Reverse in.
   - **5:** Reverse in to Parked. Parked has a double border: the final
     state.

The AV drops off its passengers at the entrance and parks itself. We
**chose** the states and conditions for this lecture.

GP4's behavior node has four fixed states, and you write the rule that picks
one. Each time it runs, that rule picks the safest state whose condition
holds; there are no arrows between states.


.. _l9-lec-transitions:

Each Transition Has One Condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 6 30 64
   :header-rows: 1
   :class: compact-table

   * -
     - **From, to**
     - **Condition (thresholds chosen)**
   * - 1
     - Enter, Search
     - the AV has passed the entry gate
   * - 2
     - Search, Approach
     - a free spot at least 2.6 m wide is seen within 15 m ahead
   * - 3
     - Approach, Search
     - the spot is taken before the AV reaches it, or reads under 2.3 m wide
   * - 4
     - Approach, Reverse in
     - the AV has stopped where the reverse maneuver starts
   * - 5
     - Reverse in, Parked
     - base link within 0.2 m and 3° of the goal pose
   * - 6
     - Search, Search
     - end of the aisle, no free spot: take the next aisle

- **Search** and **Approach** follow the aisle's center: the sampling planner
  of this lecture, with the aisle as the reference.
- **Reverse in** has no lane to follow: it needs the planners of the next
  section.


.. _l9-lec-flicker:

Two Thresholds Keep a State from Flickering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Imagine the spot detector measures the free spot's width again every 0.1 s,
and the readings jump between 2.5 m and 2.7 m (chosen for this example).

1. **One threshold, 2.6 m, both ways:** the FSM goes from Search to Approach
   and back on almost every reading, so the local planner gets a new task up
   to ten times a second.
2. **Two thresholds (hysteresis):** enter Approach at 2.6 m or more; go back
   to Search only below 2.3 m, or when the spot is taken. A reading of 2.5 m
   no longer sends the AV back.


.. _l9-lec-behavior-summary:

Where Behavior Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where behavior leaves us
   :class: tip

   - The behavior layer picks the task; the local planner finds the path for
     it.
   - On our road, closing the left lane leaves 10 candidates; 9 collide, and
     the AV stops behind the obstacle (cost 11.54).
   - The lane change is a game with two Nash equilibria: the AV goes first
     only when prediction says the other car will yield.
   - An FSM: states, transitions, one condition each; two thresholds against
     flicker.


.. _l9-lec-garage:

Garage Planners
---------------

We plan where there is no lane to follow, with grid search, hybrid A* and
RRT, in a parking garage.

**What it is for:** these planners are for parking, and for any place where
:math:`(s, d)` has no meaning.


.. _l9-lec-garage-scene:

The Garage: No Lane to Follow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/garage_scene.png
   :alt: A top view of a garage 36 by 18 meters, x and y in meters: a row of parking spots along the top wall and one along the bottom wall, with an aisle between them. Blue parked cars, the obstacles, fill most spots. Tag 1: the AV, black, at the left end of the aisle facing right. Tag 2 below a light gray car drawn in the free spot of the top row, facing down: the goal pose. Tag 3 in the aisle, above two empty spots in the bottom row.
   :width: 75%
   :align: center

   The garage, the AV and the goal pose.

.. admonition:: Reading the figure
   :class: tip

   The garage from above, :math:`x` and :math:`y` in meters: a row of spots
   along the top wall, a row along the bottom wall, and the aisle between
   them. Blue cars, the obstacles, fill most spots.

   - **Tag 1:** the AV (black), at the left end of the aisle, facing right.
   - **Tag 2:** the goal pose (light gray car), backed into the free spot of
     the top row.
   - **Tag 3:** two more free spots, in the bottom row.

Garage 36 m by 18 m, aisle 7 m, spots 2.6 m by 5.5 m, 19 parked cars, the
obstacles (all chosen). To compare them, each planner below plans the drive from tag 1
along the aisle.

.. tip::

   See "Grid Search" in :doc:`Going Further <l9_appendix>`: grid search
   in this garage, with no heading, and on a small grid, step by step.


.. _l9-lec-hybrid:

Hybrid A*: an Exact Pose in Every Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Hybrid A*
   :class: note

   A* over a grid of :math:`(x, y, \theta)` cells. Plain A* visits only the
   cell centers; hybrid A* keeps in each cell an exact pose, one the AV
   reaches by driving from the pose before it.

.. figure:: /_static/images/L9/hybrid_primitives.png
   :alt: A faint AV facing right with its base link at the origin, x and y in meters. Five solid black arcs leave the base link forward, curving from hard left to hard right, tag 1. Five dashed arcs leave it backward, tag 2. Each arc is 3 meters long and ends in a dot.
   :width: 55%
   :align: center

   The ten arcs the AV can drive from one pose.

.. admonition:: Reading the figure
   :class: tip

   A faint AV facing right, its base link (white dot) at the origin,
   :math:`x` and :math:`y` in meters.

   - **Tag 1, solid:** five arcs forward, one per steering angle, from hard
     left to hard right.
   - **Tag 2, dashed:** the same five arcs in reverse.

   Each arc is drawn 3 m long and ends in a dot.

From a pose, the AV drives a short arc at one of 5 steering angles, forward
(tag 1) or in reverse (tag 2). The tightest arcs have the 3.41 m radius of
the Configuration Space section. The arcs are drawn 3 m long; the search
used 0.75 m.

.. tip::

   See "Hybrid A*" in :doc:`Going Further <l9_appendix>`: its six
   steps, its estimates of cost to go, and the direct try at the goal.


.. _l9-lec-hybrid-garage:

Hybrid A* in the Garage
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/garage_hybrid.png
   :alt: The garage top view, x and y in meters. Light gray dots fill most of the aisle: the poses the search expanded. A green line, tag 1 above it, leaves the AV at the left, rises gently, runs along the aisle and curves down to the right past the free spot. There a gray copy of the AV stands angled down to the right, tag 2: the switch to reverse. A dashed green line runs from it straight up into the free spot, where the AV stands backed in, tag 3.
   :width: 80%
   :align: center

   Hybrid A*'s path: forward, one switch, then reverse into the spot.

.. admonition:: Reading the figure
   :class: tip

   The light gray dots fill most of the aisle: the poses the search
   expanded.

   - **Tag 1, solid green:** the forward part. It leaves the AV, runs along
     the aisle and curves down to the right past the free spot.
   - **Tag 2, gray AV:** the switch to reverse, the AV angled down to the
     right.
   - **Tag 3, dashed green:** the reverse part, straight up into the spot,
     where the AV stands backed in.

- Tag 1: forward, 24.0 m.
- Tag 2: one switch to reverse, at (25.9, 9.7) m, the nose 66.7° below the
  :math:`x` axis.
- Tag 3: reverse, 6.6 m, into the spot.

The path is 30.6 m in all; the search expanded 8,478 poses (gray dots).
Every path hybrid A* returns can be driven, but the search is not
**complete**: it can miss a path that exists.


.. _l9-lec-rrt:

RRT: Grow a Tree Toward Random Points
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Rapidly exploring random tree (RRT)
   :class: note

   A tree of points, grown from the start. Each step picks a random point,
   finds the tree's nearest node and takes a short step from it toward the
   point; the step's end is a new node.

.. figure:: /_static/images/L9/rrt_step.png
   :alt: A small gray tree of five nodes joined by lines, rooted at the bottom left, tag 1, x and y in meters. A rust star at the top right is a random point, tag 2. The tree node nearest to the star is black, tag 3. A green step 1.5 meters long goes from it toward the star and ends in a green node, tag 4. A thin dotted line continues to the star.
   :width: 55%
   :align: center

   One step of RRT.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** the tree's root, the start, at the bottom left. The gray
     lines and dots are the tree so far.
   - **Tag 2:** a random point (rust star).
   - **Tag 3:** the tree node nearest to it (black).
   - **Tag 4:** the new node (green), at the end of a 1.5 m step from the
     nearest node toward the random point. The dotted line goes on to the
     star.

1. The tree starts as one node: the AV (tag 1).
2. Pick a random point (tag 2), sometimes the goal itself.
3. Find the tree node nearest to it (tag 3).
4. Step from it toward the point, 1.5 m (tag 4). Check the step with the
   circles; if it is free, add it.
5. Repeat until a node is within 1.5 m of the goal.


.. _l9-lec-rrt-garage:

RRT in the Garage
~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/rrt_garage.png
   :alt: The garage top view, x and y in meters. A small gray tree grows from the AV at the left end of the aisle to the right. A green path through the tree zigzags along the aisle to a dark cross in front of the free spot, tag 1.
   :width: 70%
   :align: center

   RRT's tree and path in the garage.

.. admonition:: Reading the figure
   :class: tip

   The gray lines are the tree, grown from the AV at the left end of the
   aisle. The green line is the path through the tree: it zigzags along the
   aisle.

   - **Tag 1:** the goal (dark cross), in front of the free spot.

The goal (tag 1) is in front of the free spot. Seed 4; a random point is the
goal with a chance of 5 in 100.

- The tree reaches the goal after 34 tries. 12 steps hit something, so it
  has 23 nodes.
- The path is 16 straight steps, and the heading jumps by up to 78° where two
  steps meet: fast to find, not drivable as it is.

The original RRT makes each step by steering the AV's model, as hybrid A*
does, so its path can be driven.

.. tip::

   See "RRT and RRT*" in :doc:`Going Further <l9_appendix>`: how RRT*
   keeps shortening the path.


.. _l9-lec-which-discussion:

Discussion: Which Planner Where
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two minutes with your neighbor, before the next section:

1. Why does sampling in :math:`(s, d)` not work in the garage?
2. Why not run hybrid A* on the road too?
3. The AV leaves the road and enters the garage. What decides that it
   switches planners?

The next section answers them.


.. _l9-lec-which:

Which Planner Where
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 26 32 42
   :header-rows: 1
   :class: compact-table

   * - **Where**
     - **Planner**
     - **Why**
   * - A route over the town
     - A* on the lane graph (GP4)
     - the roads are a graph of lanes
   * - A road with lanes
     - sampling in :math:`(s, d)` (today)
     - the lanes give the reference
   * - A garage, parking
     - hybrid A*
     - reversing, tight turns, a goal heading
   * - Open space, no lanes
     - RRT, RRT*
     - a tree finds a path fast, with no grid

.. important::

   Junior used two of these: sideways roll-outs on roads, and hybrid A* in
   parking lots. The behavior layer decides which one runs.


.. _l9-lec-handson-garage:

Hands-On, Part 3: the Garage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``rrt`` part grows the tree; the ``search`` part shows the hybrid A*
result (and the grid search's, from Going Further). We computed those two results in advance. GP4 asks
you to write A* on the lane graph, not these garage searches. The commands
are on :doc:`the Code page <l9_code>`.

.. admonition:: What to look at
   :class: hint

   1. In ``rrt``, drag the slider: where does the tree grow first?
   2. Try three seeds. Does the path change? Does it get any smoother?
   3. In ``search``, follow hybrid A*'s path: where does it switch to
      reverse?

.. dropdown:: Answers, from the script
   :class-container: sd-border-success

   2. The path changes with the seed, and no seed makes it smooth: every
      step is straight, so the heading jumps where two steps meet. Seed 4:
      16 steps, jumps up to 78.2°. Seed 7: 15 steps, up to 52.7°. Seed 1:
      16 steps, up to 72.3°.
   3. At (25.9, 9.7) m, after 24.0 m forward: the AV stops once and backs
      6.6 m into the spot.


.. _l9-lec-garage-summary:

Where Garage Planning Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where garage planning leaves us
   :class: tip

   - Hybrid A*: exact poses in cells; 24.0 m forward, one switch, 6.6 m in
     reverse into the spot.
   - RRT: 34 tries, a jagged path the AV cannot drive as it is.


.. _l9-lec-next:

Next Class
----------

.. admonition:: Today
   :class: important

   The route planner gave a route; **today we found the path for the next
   70 m.** The AV is a point in :math:`(x, y, \theta)`; the Frenet frame
   turns the lanes into lines of constant :math:`d`; 31 sampled candidates,
   checked with circles and scored, give a pass in the left lane at cost
   5.07; the behavior layer chooses the task; in the garage, hybrid A* found
   a path the AV can drive, 30.6 m with one switch to reverse.

- **L10, Trajectory Generation and Control:** put a speed and a time on the
  path, then steer and drive along it.

**Before next class**

- Finish the two exercises and the three hands-on parts on :doc:`the Code
  page <l9_code>`.
- Read "The S Curve" and "Hybrid A*" in :doc:`Going Further <l9_appendix>`.


.. rubric:: Image credits

The vehicle icons in the figures on this page were created by Stone from the
`Noun Project <https://thenounproject.com>`_. The road is CARLA's Town03 map.
