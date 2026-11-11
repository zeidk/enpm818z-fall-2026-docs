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
   - where the Frenet frame fails, and what to do on a tight turn;
   - how hard a candidate turns, by hand, and the S curve's polynomial, with
     where 5.77 comes from;
   - how the circle radius changes with the number of circles;
   - the lane change as a Markov decision process (MDP);
   - hybrid A*'s estimates of cost to go, and its direct try at the goal.

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
   :alt: Two top views of the same two-lane road, one above the other. In each, the AV, a black car, drives to the right in the lower lane, and the obstacle, a blue parked car, stands about 58 meters ahead in the same lane. Top view, tag 1: a black dotted line along the center of the AV's lane runs straight through the obstacle. Bottom view, tag 2: a green path leaves the AV's lane, moves into the upper lane and passes the obstacle.
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
   :alt: A block diagram of four boxes in a row joined by arrows: Route planner (L7), Behavior layer (L9, today), Local planner (L9, today) and Controller (L10). The two boxes marked today are green. Under the arrows: lanes to follow, a task, a path for the next seconds, and, after the controller, steering, throttle, brake. Above, a box Pose feeds the route planner, and a box Pose, objects, predictions feeds the behavior layer and the local planner.
   :width: 95%
   :align: center

   The four layers that decide what the AV does.

.. admonition:: Reading the figure
   :class: tip

   Read the row left to right. Each arrow carries what one layer hands to
   the next.

   - The **route planner** reads the pose and hands on the lanes to follow.
   - The **behavior layer** (today, green) reads the pose, the objects and
     their predictions, and hands on a task.
   - The **local planner** (today, green) reads the same inputs and hands on
     a path for the next seconds.
   - The **controller** (next class) turns the path into steering, throttle
     and brake.

Most driving stacks split their decisions into these four layers.

Today covers the two middle layers: the **local planner** first, then the
**behavior layer** that tells it what to do. **Motion planning**, this
lecture's title, is what Paden et al. call the local planner's job: finding a
path the AV can drive, free of collisions (Paden et al., 2016; see :doc:`the
References page <l9_references>`).


.. _l9-lec-map:

Today's Map: From the Inputs to a Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This map opens up the two middle layers of the last figure: the behavior
layer, and the local planner (dashed frame). Each section today fills in one
box. In the deck, each section's divider shows this picture with that box
highlighted.

.. figure:: /_static/images/L9/l9_pipeline.png
   :alt: A flowchart in three rows. Top row: a box of inputs (the route, from the route planner, L7; the AV's pose and speed; other cars and obstacles, as boxes; their predicted paths; the map), an arrow to the behavior layer, which picks the task, and further right the output: a path for the next 70 meters, every 0.5 seconds, with an arrow up to a box, controller (L10): steering, throttle, brake. A green dashed frame labeled local planner surrounds the two rows below; the behavior layer box is green too, as on the layers slide, and the inputs and output boxes are gray. Middle row, reached from the behavior layer on the road: Frenet frame (map to s and d), then sample 31 paths, then check (circles, turn limits), then score (keep the cheapest). Bottom row, reached from the behavior layer in the garage: search (hybrid A star, grid, RRT), and a dashed box, configuration space: the AV as a point x, y, theta, with dashed arrows to the check and to the search. Lines from the score and from the search join at the right and lead to the output.
   :width: 95%
   :align: center

   Today's map, from the inputs to a path.

.. admonition:: Reading the figure
   :class: tip

   Each box is covered in one section of these notes.

   - **Inputs** (gray): the route, from the route planner; the AV's pose and
     speed; other cars and obstacles, as boxes; their predicted paths; the
     map. See :ref:`l9-lec-scene`.
   - **Behavior layer** (green): picks the task. See :ref:`l9-lec-behavior`.
   - **Local planner** (green dashed frame), on the road: the **Frenet
     frame** turns the map into :math:`(s, d)` (:ref:`l9-lec-frenet`);
     **sample** makes 31 paths (:ref:`l9-lec-sampling`); **check** tests
     them with circles and turn limits (:ref:`l9-lec-collision`); **score**
     keeps the cheapest (:ref:`l9-lec-sampling`).
   - **Local planner**, in the garage: **search** with hybrid A*, a grid or
     RRT (:ref:`l9-lec-garage`).
   - **Configuration space** (dashed box): the AV as a point
     :math:`(x, y, \theta)`. Dashed arrows lead from it to the check and to
     the search (:ref:`l9-lec-cspace`).
   - **Output** (gray): a path for the next 70 m, planned every 0.5 s. It
     goes to the **controller** (next class), which turns it into steering,
     throttle and brake (:ref:`l9-lec-next`).


.. _l9-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

This is a reading slide in the deck. After this lecture, you can:

1. say what a **local planner** takes from the route planner and hands to
   the controller;
2. describe the AV by its **configuration** :math:`(x, y, \theta)`, and
   **grow an obstacle** into the region the AV's base link must avoid;
3. check a pose for **collision with circles**, and say why the check is
   **conservative**;
4. convert a point between the map and the **Frenet frame** :math:`(s, d)`;
5. generate **candidate paths** with sideways shifts, **score** them, and
   say how the weights pick the path;
6. explain the **behavior layer** with a finite state machine, and find the
   **Nash equilibria** of a lane change between the AV and another car;
7. explain **grid search**, **hybrid A*** and **RRT**, and say where each
   planner is used.


.. _l9-lec-scene:

The Scene
---------

We take one road from CARLA's Town03 map, with a car parked in the AV's
lane.

**What it is for:** every road method today runs on this one scene, with
distances read from the map.


.. _l9-lec-town03:

Town03, Road 67
~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/scene_overview.png
   :alt: A top view of every lane of CARLA's Town03 map as thin gray lines: a grid of streets, a roundabout near the middle and a ring road around the edge. A thick gray line, the stretch, follows the bottom edge of the ring to the right, then curves up the right side. On its straight part sit two car icons, drawn much larger than to scale: tag 1, the AV, black; tag 2, the obstacle, blue, where the curve begins.
   :width: 60%
   :align: center

   Our stretch of road on the Town03 map.

.. admonition:: Reading the figure
   :class: tip

   The thin gray lines are every lane of Town03, seen from above, :math:`x`
   and :math:`y` in meters. The thick gray line is the stretch of road we
   plan on, along the bottom of the ring road and up its right side.

   - **Tag 1:** the AV (black).
   - **Tag 2:** the obstacle, a parked car (blue), where the curve begins.

   The car icons are drawn about 8 times too large, so they show at this
   scale.


.. _l9-lec-av-car:

The AV, the Obstacle and the Two Lanes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/scene_top.png
   :alt: A top view, to scale, of the start of the stretch: two lanes, the lower one pale yellow with a dotted center line, the upper one pale purple, the lane line between them dashed. Gray arrows in both lanes point right: both lanes run the same way. Tag 1 below the AV, a black car in the lower lane at the left. Tag 2 below the obstacle, a blue parked car, about 58 meters ahead in the same lane. Tag 3 in the upper lane. On the right the road starts to curve upward.
   :width: 95%
   :align: center

   The AV, the obstacle and the two lanes, to scale.

.. admonition:: Reading the figure
   :class: tip

   A top view of the start of the stretch, to scale, :math:`x` and :math:`y`
   in meters. The dotted line is the reference path, the center of the right
   lane; the dashed line is the lane line between the two lanes. The gray
   arrows show that both lanes run the same way, left to right. On the
   right, the road starts to curve upward.

   - **Tag 1:** the AV, black, in the right (lower, yellow) lane.
   - **Tag 2:** the obstacle, blue, about 58 m ahead in the same lane.
   - **Tag 3:** the left (upper, purple) lane.

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
   * - position: its base link, the middle of its rear axle (it turns about
       this axle)
     - position: its center (perception reports a box by its center)

The plan covers 70 m ahead (chosen): 70 / 10 = 7 s at 10 m/s. The reference
path is the center line of the lane the route picks, read from the map: a
point every 0.5 m along the right lane.


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
   every point of its body is: the base link at :math:`(x, y)` in the map
   frame, and the heading :math:`\theta`, counterclockwise from the map's
   :math:`x` axis.

.. figure:: /_static/images/L9/config_pose.png
   :alt: A top view of a black car facing up and to the right, at 30 degrees from a dashed horizontal arrow labeled map x; a dashed vertical arrow labeled map y crosses it at a small white circle near the rear of the car, the base link, with tag 1 beside it. An arc between the map x arrow and the car's dotted center line, ahead of the car, is labeled theta, tag 2. Beside the car's right side, two arrows along its length run from the rear bumper to the base link, 0.9 m, and from the base link to the front bumper, 3.6 m, tag 3. Ahead of the front bumper, a short arrow across the car's direction, labeled 0.95 m, runs from the center line to the side, tag 4.
   :width: 60%
   :align: center

   The three numbers of a configuration, on the AV.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** the base link at :math:`(x, y)`.
   - **Tag 2:** the heading :math:`\theta`. The figure draws :math:`\theta`
     at 30° so it shows.
   - **Tag 3:** the body does not bend, so knowing :math:`q` gives every
     point of it: the rear bumper is 0.9 m behind the base link (chosen), the
     front bumper 4.5 − 0.9 = 3.6 m ahead of it.
   - **Tag 4:** each side 1.9 / 2 = 0.95 m out.

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
   :alt: A top view of two lanes, the lower one pale yellow and the upper one pale purple, with a dashed line between them. In the lower lane, a blue car points right, tag 1. Behind it in the same lane, a light gray car, tag 2, points right with its front over the blue car's rear; the part where the two bodies overlap is outlined in rust and hatched. In the upper lane, a second light gray car, tag 3, at the same distance behind, is clear of the blue car. Each gray car has a small white circle near its rear, its base link.
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

In this figure and every later one, a light gray AV is a pose the AV is not
at now (one it might reach, or a goal); a black AV is where it is.


.. _l9-lec-cspace-plan:

Fast Collision Check, Two Ways: Compare Bodies, or Test One Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** at each future pose :math:`q` (one every 0.5 m on each path it
considers), the planner decides quickly if the AV would hit the obstacle.
There are two ways, shown here on the same three poses.

.. figure:: /_static/images/L9/cspace_plan.png
   :alt: Two panels side by side, split by a dashed line. Left: three light gray cars in a row along the lane, behind a blue car; the last gray car's front is over the blue car's rear. Right: the blue car, faded, inside a rust hatched box much larger than it, and three small white circles where the three gray cars' base links were: the first two outside the box, the last inside it.
   :width: 85%
   :align: center

   Three bodies to compare, or three points and a box.

.. admonition:: Reading the figure
   :class: tip

   - **Left, the direct check:** three future poses of the AV (light gray)
     behind the obstacle (blue). Only the last body overlaps the obstacle.
   - **Right, grow, then test a point:** the obstacle (faded) inside the grown
     obstacle (rust, hatched), and the AV's base link at the same three poses
     (white dots). Only the last dot is inside.

**Direct check:** compare the AV's body with the obstacle at every future
pose. Here, only the last of the three bodies overlaps, so only that pose
collides.

**Expensive as is:** two full shapes compared at every pose of every path,
every 0.5 s. Circles make it cheap (:ref:`l9-lec-collision`).

**Grow, then test a point** (for one AV heading):

- **Step 1**, once per heading: grow the obstacle by the AV's shape
  (hatched): every base-link position where the body would touch it.
- **Step 2**, at each pose: keep only the AV's base link (white dot). A pose
  collides when that point is inside the grown obstacle: here, only the last
  of the three dots.

Both figures show the same three poses, and both checks give the same answer.


.. _l9-lec-grow:

Step 1: Grow the Obstacle, for One AV Heading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/cspace_grow.png
   :alt: A top view of a blue car, its center marked with a white cross, and eight gray cars heading the same way, each just touching it. Four darker ones on its sides: tag 1 behind it, tag 2 ahead of it, tag 3 beside it on its left, tag 4 beside it on its right. Four lighter ones at its corners, each with a dashed rectangle around its body; each dashed rectangle touches the blue car's outlined rectangle at one corner, marked by a black dot. Each gray car has a white circle at its base link, near its rear, and all eight circles lie on a rust box: its back edge 5.85 m behind the blue car's center, its front edge 3.15 m ahead, each side 1.9 m out from the center line.
   :width: 75%
   :align: center

   The AV at the poses where it just touches the obstacle.

.. admonition:: Reading the figure
   :class: tip

   Slide the AV, heading along the obstacle, around it until it just
   touches; its base link (white circle) marks the edge of the grown obstacle
   (rust box). The white cross is the obstacle's center.

   - **Tag 1, behind:** 2.25 + 3.6 = 5.85 m behind the obstacle's center:
     half the obstacle (4.5 / 2 = 2.25 m), then the AV's front, 3.6 m ahead of
     its base link.
   - **Tag 2, ahead:** 2.25 + 0.9 = 3.15 m ahead: half the obstacle, then the
     AV's rear, 0.9 m behind its base link.
   - **Tag 3, beside on the left** (and **tag 4**, on the right):
     0.95 + 0.95 = 1.9 m out, two half widths.
   - **Light gray AVs:** the body's corner touches the obstacle's corner
     (dashed outlines, black dots), and the base link lands on a corner of
     the box.

.. important::

   The grown obstacle is 5.85 + 3.15 = 9.0 m long and 1.9 + 1.9 = 3.8 m
   wide. It reaches farther behind than ahead, because the base link sits
   near the AV's rear.

.. tip::

   See "C-Space for Two Boxes" in :doc:`Going Further <l9_appendix>` for
   the region for two boxes, in general.


.. _l9-lec-point:

Step 2: the AV Becomes a Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 2 keeps only the AV's base link: a pose collides when that point is
inside the grown obstacle.

.. figure:: /_static/images/L9/cspace_region.png
   :alt: A top view in the obstacle's own frame, along it to the right and across it upward, in meters. The obstacle, the blue car, sits at the center. A rust hatched box 9.0 meters long and 3.8 meters wide surrounds it, reaching from minus 5.85 to plus 3.15 along and from minus 1.9 to plus 1.9 across. Four white dots mark the AV's base link at four poses: tag 1 inside the box, behind the car and to its left; tag 2 inside the box, beside the car on its right; tag 3 outside the box, behind it; tag 4 outside the box, 3.8 meters to the car's left. The vertical axis reads across, to the obstacle's left.
   :width: 70%
   :align: center

   The region the base link must avoid, for the AV heading along the
   obstacle.

.. admonition:: Reading the figure
   :class: tip

   The axes follow the obstacle: along it to the right, across it to the
   obstacle's left upward, both in meters, with the obstacle's center at 0.
   The rust hatched box is the grown obstacle: 9.0 m long (from −5.85 to
   +3.15) and 3.8 m wide (from −1.9 to +1.9).

   Each white dot is the AV's base link at one pose; the AV's body is not
   drawn.

   - **Tags 1 and 2:** inside the grown obstacle, so those poses collide.
   - **Tags 3 and 4:** outside, so they are free.

Tag 4 is on the left lane's center: a pose there is free beside the obstacle.

.. tip::

   See "C-Space for Two Boxes" in :doc:`Going Further <l9_appendix>` for
   the grown obstacle on our road.


.. _l9-lec-turned-candidate:

Catch Every Candidate: Some Come In Turned
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The grown obstacle so far assumes the AV heads along the obstacle. But a
planner tries many paths, the **candidates**, and keeps one; the check must
be right for every candidate, every time it plans again (every 0.5 s). The
figure shows one such moment.

.. figure:: /_static/images/L9/turned_candidate.png
   :alt: A top view of the road around the obstacle, x and y in meters: the left lane pale purple, the right lane pale yellow, a dashed lane line between them. Tag 1: the AV, black, in the left lane, behind the blue obstacle. From the AV, a green path, tag 2, runs straight on along the left lane. A rust path leaves the AV, crosses the lane line and comes back into the right lane past the obstacle. On it, tag 3, a light gray copy of the AV turned to its right, its body drawn as a dashed rectangle; it overlaps the obstacle's dashed rectangle at one corner, shaded rust.
   :width: 85%
   :align: center

   A candidate that comes in turned.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** the AV, in the left lane, its base link 8 m behind the
     obstacle's center.
   - **Tag 2:** the path the planner keeps (green): almost parallel to the
     obstacle (over the whole drive, 3.7° at most from the road's direction
     beside it).
   - **Tag 3:** a candidate (rust) that heads back to the right lane within
     20 m. Beside the obstacle it is turned 21° to its right, and its body
     overlaps the obstacle's corner (shaded rust).

The check must catch that candidate, so Step 1 must work for a turned AV
too. The next section redoes it at 21°.


.. _l9-lec-heading-grow:

Step 1 Again: Grow the Obstacle for the Turned AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Turn the AV 21° to its right, as that candidate, and do Step 1 again.

.. figure:: /_static/images/L9/cspace_heading_grow.png
   :alt: A top view in the obstacle's own frame, along it to the right and across it upward, in meters. The road: the right lane, pale yellow, with the blue car at the center, and the left lane, pale purple, above a dashed lane line. Four gray copies of the AV, each turned 21 degrees to its right, sit around the car: behind it, above it, ahead of it and below it, each just touching it; the one below sits off the road's right edge. Each copy's base link is a white dot. A dashed rust outline runs through the four dots and around the obstacle: straight pieces along and across, joined by slanted pieces.
   :width: 70%
   :align: center

   Step 1 for the AV turned 21° to its right.

.. admonition:: Reading the figure
   :class: tip

   The same axes as the figure in Step 2. Yellow: the obstacle's lane;
   purple: the left lane; dashed gray: the lane line. The gray copies are
   the turned AV at four of its touching poses, and the dashed rust outline
   joins the base links of all of them.

1. Keep the AV turned 21° to its right. Move it around the obstacle and stop
   each time it just touches it (gray copies: four of these poses).
2. Mark the base link at each touching pose (white dots).
3. Join the marks all the way around: the dashed outline. With its base link
   inside, the turned AV overlaps the obstacle.

Each slanted piece is where an edge of the turned AV slides along a corner of
the obstacle. So the outline is no longer a box.


.. _l9-lec-heading:

The Region Changes with the Heading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The grown obstacle from Step 1 holds only for the AV heading along the
obstacle. Turned 21° to its right, the AV gets a different shape.

.. figure:: /_static/images/L9/cspace_heading.png
   :alt: The same top view, with the road: the right lane holds the blue car, the left lane is above the dashed lane line. The solid rust box is the region for the AV heading along the obstacle. A dashed rust outline, slanted at its corners, is the region for the AV turned 21 degrees to its right: it reaches higher than the box toward the obstacle's rear and lower toward its front. Tag 1: a light gray AV in the left lane, turned 21 degrees to its right, its nose across the lane line toward the car, its base link on the dashed outline. Tag 2 sits beside the dashed outline on the right.
   :width: 70%
   :align: center

   The region for two AV headings.

.. admonition:: Reading the figure
   :class: tip

   The same axes as the figure before.

   - **Solid rust box:** the region for the AV heading along the obstacle.
   - **Tag 2, dashed rust outline:** the region for the AV turned 21° to its
     right. It reaches higher than the box toward the obstacle's rear and
     lower toward its front.
   - **Tag 1:** the turned AV touching the obstacle, from the left lane. Its
     base link is on the dashed outline.

- Each heading gives its own region, so the obstacle region depends on all
  three numbers :math:`(x, y, \theta)`.
- For a turned AV the grown obstacle is no longer a box, and each heading
  needs its own. So the next section, :ref:`l9-lec-collision`, uses the
  direct check, made cheap: three circles cover the AV's body at each pose.


.. _l9-lec-sideways:

Limits on How the AV Moves
~~~~~~~~~~~~~~~~~~~~~~~~~~

The wheels roll; they do not slide. So the base link always moves along the
heading, and the AV turns only by steering. This gives every path two limits.

.. figure:: /_static/images/L9/turn_limits.png
   :alt: A top view of the AV, a light gray car heading right, its base link a white dot near the rear and the center of its front axle a black dot. Tag 1: two dashed arcs start at the base link and curve forward, one to the left and one to the right, each around a center marked with a plus sign beside the AV; an arrow marked R = 3.41 m runs from the upper center to the end of the left arc. Tag 2: an arrow pointing straight up from the AV's left side. At the front axle, a dotted line continues the AV's axis and a solid line leaves it, turned to the left; the angle between them is marked delta max. Below the car, a double arrow marked L = 2.875 m spans from the base link to the front axle.
   :width: 40%
   :align: center

   What the AV can do, and what it cannot.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1, steering limit:** the tightest turn, to the left or to the
     right. The base link follows a circle of radius :math:`R` around a
     center (plus sign) beside the AV. No turn can be tighter.
   - **Tag 2, sideways limit:** a sideways move. The AV cannot make it.

The radius of the tightest turn, step by step:

1. :math:`R = L / \tan\delta_\text{max}`, with :math:`L` the wheelbase, from
   the base link on the rear axle to the center of the front axle (black dot),
   and :math:`\delta_\text{max}` the largest steering angle, from the AV's axis
   (dotted) to the steered front wheels.
2. :math:`L` = 2.875 m (chosen; GP4's vehicles have 2.3 to 3.0 m) and
   :math:`\delta_\text{max}` = 0.7 rad, or 40.1° (GP4's limit).
3. tan 0.7 = 0.842, so :math:`R` = 2.875 / 0.842 = 3.41 m.


.. _l9-lec-comfort:

Comfort Limit: Wider Turns at Higher Speed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The steering limit says how tight the AV can turn. At speed, a turn that
tight would push the passengers hard to the side, so the planner adds a third
limit, for comfort.

On a curve of radius :math:`R` at speed :math:`v`, the passengers feel a
sideways acceleration of :math:`v^2 / R`. We chose a limit of 3 m/s² (GP4
uses a stricter 2.0 m/s²). At 10 m/s, our road's speed:

1. :math:`v^2 / R` ≤ 3, so :math:`R` ≥ :math:`v^2` / 3.
2. :math:`R` ≥ 10² / 3 = 100 / 3 = 33.3 m.
3. 33.3 / 3.41 = 9.8: about ten times the tightest turn.

.. important::

   33.3 m is a lower limit, not a target: at 10 m/s every bend needs a radius
   of 33.3 m or more. Wider bends are fine; tighter ones are too sharp. To
   turn tighter, slow down: at 5 m/s, 5 × 5 / 3 = 8.3 m.

.. figure:: /_static/images/L9/turn_radius_speed.png
   :alt: A graph of the smallest turn radius in meters, from 0 to 42, against speed in meters per second, from 0 to 12. A flat black line at 3.41 meters across all speeds. A purple curve that starts at zero and rises ever more steeply. A white dot where the curve crosses the flat line, at about 3.2 meters per second. A white dot on the curve at 10 meters per second and 33.3 meters, with dashed gray guide lines down to the speed axis and across to the radius axis.
   :width: 60%
   :align: center

   Tightest turn at each speed: steering or comfort.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a map: the lines are not paths. The black line is the
   steering limit: 3.41 m at any speed. The purple curve is the comfort
   limit, :math:`v^2` / 3. The AV must obey both, so its tightest turn is
   whichever line is higher. The lines cross at 3.2 m/s
   (3.2 × 3.2 / 3 = 3.41 m). Below that speed, steering sets the limit;
   above it, comfort does: 33.3 m at 10 m/s.


.. _l9-lec-drivable:

Drivable Paths: No Corners, No Tight Bends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Goal: a test for every path a planner returns: can the AV drive it as it is?

.. important::

   **What makes a path drivable.** The AV turns by steering while it rolls,
   so its heading changes a little with each meter it drives. A corner, where
   the path's direction jumps at one point, would need the AV to turn on the
   spot, and it cannot. So a path the AV can drive has no corners, and every
   bend has a radius of at least the larger turn limit: 3.41 m from
   steering, or the comfort radius at the AV's speed (33.3 m at 10 m/s).

.. figure:: /_static/images/L9/drivable_path.png
   :alt: Two top views of the AV, a light gray car heading right, its base link a white dot. Left, tag 1: a purple path leaves the base link straight to the right, then turns up at a sharp right-angle corner and ends in an arrow. Right, tag 2: a green path leaves the base link straight to the right, then curves up along a quarter circle and ends in an arrow; a plus sign marks the circle's center, and an arrow marked R runs from the center to the curve.
   :width: 80%
   :align: center

   The same turn, with a corner and as an arc.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** a path with a corner: the AV cannot drive it. Two planners of
     the :ref:`l9-lec-garage` section return such paths.
   - **Tag 2:** the same turn as an arc of radius :math:`R` (center: plus
     sign): drivable when :math:`R` is at least the larger turn limit.


.. _l9-lec-rule-out:

What the Limits Rule Out
~~~~~~~~~~~~~~~~~~~~~~~~

The AV cannot drive a path that breaks the steering or sideways limit, and
should not drive one that breaks comfort. The limits change what a planner
returns in three places:

- **Comfort limit:** sampling drops every candidate that turns harder than
  3 m/s², 4 of the 31 on our road (:ref:`l9-lec-drop`).
- **Steering limit:** a sharp corner is a turn of radius 0, tighter than
  3.41 m, so a path with corners cannot be driven as it is. RRT's garage path
  has them (:ref:`l9-lec-rrt-garage`); hybrid A* uses only arcs of 3.41 m or
  wider (:ref:`l9-lec-hybrid`).
- **Sideways limit:** the AV cannot slide sideways into a parking spot.
  Hybrid A*'s path drives 24.0 m forward, switches once, and backs 6.6 m in
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

.. figure:: /_static/images/L9/cspace_region.png
   :alt: The figure from Step 2: a top view in the obstacle's own frame, in meters. The blue car at the center inside a rust hatched box 9.0 meters long and 3.8 meters wide. Four white dots mark the AV's base link: tags 1 and 2 inside the box, tags 3 and 4 outside it, tag 4 on the left lane's center.
   :width: 60%
   :align: center

   The grown obstacle, from Step 2.

.. admonition:: Reading the figure
   :class: tip

   The same figure as in Step 2. Tags 1 and 2 (inside the rust box) are
   poses that collide; tags 3 and 4 (outside) are free, and tag 4 is on the
   left lane's center.


.. _l9-lec-collision:

Collision Checking
------------------

Configuration space asked for a direct check of the AV's body at each pose.
We make that check quick with circles.

**What it is for:** every planner today runs this test at every pose of every
candidate it tries: on our road, 4,332 poses every 0.5 s
(:ref:`l9-lec-check-rate`).


.. _l9-lec-check-rate:

How Often the Check Runs: 4,332 Poses Every 0.5 s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every 0.5 s the planner tries 31 candidate paths (:ref:`l9-lec-sampling`
builds them) and checks the AV at each pose along each one, a pose every
0.5 m.

.. list-table::
   :widths: 28 14 16 24 18
   :header-rows: 1
   :class: compact-table

   * - **Candidates**
     - **How many**
     - **Length**
     - **Poses on each**
     - **Poses in all**
   * - Shift across the road to one of 10 positions, over 20, 30 or 40 m
     - 10 × 3 = 30
     - 70 m, the whole plan
     - 70 / 0.5 + 1 = 141 (both ends)
     - 30 × 141 = 4,230
   * - Stop behind the obstacle
     - 1
     - 50.15 m (steps below)
     - 50.0 / 0.5 + 1 = 101, plus the stop point: 102
     - 102
   * - **All**
     - **31**
     -
     -
     - **4,332**

The stop candidate ends where the AV's front bumper is 2.0 m short of the
obstacle's rear (chosen):

1. The obstacle's center is 58 m ahead; its rear is 4.5 / 2 = 2.25 m closer:
   55.75 m.
2. The front bumper stops 2.0 m short of it: 53.75 m.
3. The base link is 3.6 m behind the front bumper: 53.75 − 3.6 = 50.15 m.


.. _l9-lec-circles:

Cover the AV with Three Circles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/circles_cover.png
   :alt: The AV from above, light gray, 4.5 meters long and 1.9 meters wide, facing right, split into three 1.5 meter pieces marked along the top. Three equal dark circles, one per piece, cover the body; each circle and each center, a dark plus sign, has a thin white outline so it shows on the light gray car. Tag 1 below the rear circle, joined by a thin line, marks the base link, a white dot next to the rear circle's center. Tag 2, above the body, marks a dark arrow from the middle circle's center to the corner of its piece: the radius. Tag 3 below the front circle, joined by a thin line, marks its center.
   :width: 60%
   :align: center

   Three circles that cover the AV's body.

.. admonition:: Reading the figure
   :class: tip

   The AV from above, facing right. Its body is 4.5 m long and 1.9 m wide
   (chosen), cut into three pieces of 1.5 m. One circle per piece covers the
   body; each circle's center is a plus sign.

   - **Tag 1:** the base link (white dot), next to the rear circle's center.
   - **Tag 2:** a circle's radius, from the middle circle's center to the
     corner of its piece.
   - **Tag 3:** a circle's center, the front one.

**Why circles:** each test is one distance.

1. A circle looks the same at every heading, so a turned AV needs no new
   shape.
2. Two circles overlap when their centers are closer than their two radii
   added.
3. The **gap** is the distance between the centers, minus both radii. Under
   0, the circles overlap.

The obstacle, the same size, gets three circles too: 3 × 3 = 9 gaps per pose.
Three is our choice, not a rule: 4 per car hug the body closer but need
4 × 4 = 16 gaps.

.. tip::

   See "More or Fewer Circles" in :doc:`Going Further <l9_appendix>` for how
   the radius changes with the number of circles.


.. _l9-lec-radius:

Step 1: the Radius and the Centers, by Hand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/circles_hand.png
   :alt: The AV from above, light gray, inside a dashed 4.5 by 1.9 meter box cut by two dashed lines into three pieces. A plus sign marks each piece's center; a white dot just right of the rear plus is the base link. The middle piece holds a right triangle: from its center, a line 0.75 meters along the AV, then a line 0.95 meters across it to the piece's corner, a black dot; an arrow marked r runs from the center to that corner. A circle around the middle center passes through the corner. Below the AV, dimension lines: 0.9 meters from the rear bumper to the base link, 0.15 meters from the rear center to the base link, and 1.35 and 2.85 meters from the base link to the middle and front centers.
   :width: 60%
   :align: center

   The radius and the circle centers, worked out on the AV's body.

.. admonition:: Reading the figure
   :class: tip

   The AV from above, facing right, inside a dashed box 4.5 m by 1.9 m that
   two dashed lines cut into three pieces.

   - **Plus signs:** the center of each piece. The white dot just right of
     the rear plus sign is the base link.
   - **Triangle in the middle piece:** 0.75 m along the AV, then 0.95 m
     across it, to the piece's corner (black dot). The arrow :math:`r` from
     the center to that corner is the radius.
   - **Circle:** the middle circle, around the middle center, passing
     through the corner.
   - **Dimension lines below:** 0.9 m from the rear bumper to the base link;
     0.15 m from the rear center to the base link; 1.35 m and 2.85 m from
     the base link to the middle and front centers.

Cut the 4.5 m by 1.9 m body into three pieces, each 4.5 / 3 = 1.5 m long.
Each circle must reach its piece's corners.

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
   :math:`(x + o_k \cos\theta,\ y + o_k \sin\theta)`, with :math:`o_k` the
   step 3 offset: −0.15, 1.35 or 2.85 m.

.. tip::

   See "More or Fewer Circles" in :doc:`Going Further <l9_appendix>` for how
   the radius changes with the number of circles.


.. _l9-lec-margin:

The Margin: How Close Counts as a Collision
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our check calls a pose a collision when the gap is under 0.3 m. A published
requirement allows the AV's own position at most 0.29 m of error on a local
street (Reid et al., 2019, on :doc:`the References page <l9_references>`). We
round it to 0.3 m.

.. figure:: /_static/images/L9/margin_gap.png
   :alt: Two separate drawings side by side, tags 1 and 2. In each, a black circle (the AV's) on the left and a blue circle (the obstacle's) on the right, each with a plus sign at its center, and a short bar spanning the gap between them along the line through the centers. A dashed black circle is the AV's circle moved 0.3 meters to the right, shown by a small arrow marked 0.3 m. In drawing 1, the gap is wider and the dashed circle stays clear of the blue one. In drawing 2, the gap is narrower and the dashed circle crosses into the blue one; the overlap is shaded rust.
   :width: 85%
   :align: center

   Two gaps, one over the margin and one under it.

.. admonition:: Reading the figure
   :class: tip

   Two different poses side by side, not one after the other; the gaps are
   chosen for the example. The black circle is the AV's circle where the AV
   thinks it is. The dashed circle is where it would be 0.3 m off toward the
   obstacle (blue). The short bar between the circles is the gap.

   - **Tag 1:** gap 0.5 m, over 0.3 m: **no collision**. Even 0.3 m off,
     the circles stay 0.2 m apart.
   - **Tag 2:** gap 0.2 m, under 0.3 m: **counted as a collision**. 0.3 m
     off, the circles would overlap by 0.1 m (rust); the check cannot rule
     that out.

.. important::

   The 0.3 m covers only the AV's own position. Perception's error on the
   obstacle and prediction's on a moving car are larger; a margin for them
   would add to the 0.3 m.


.. _l9-lec-one-pose:

Step 2: One Pose, Checked by Hand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/circle_check.png
   :alt: A close top view beside the obstacle, x and y in meters. The AV, light gray with three dark circles, is in the upper, purple lane, on its center, a dotted line; a white dot near its rear circle's center is its base link. The obstacle, blue with three blue circles, is in the lower, yellow lane right below it, its center a little below the right lane's center, a thick black line; a blue dashed line carries the obstacle's center to the right. Each circle and its center, a plus sign, has a thin white outline so it shows on its car. A dark double arrow spans the gap between the two middle circles, across the dashed lane line, with tag 1 just right of it. Above the AV, a double arrow marked 1.35 m runs from the base link to the middle circle's center. On the right, a double arrow marked 3.5 m runs from the right lane's center up to the left lane's center, and a short bar marked 0.3 m from the right lane's center down to the obstacle's center. On the left, a stack from the obstacle's center up to the AV's: 1.21 m, 1.38 m, 1.21 m.
   :width: 70%
   :align: center

   The AV beside the obstacle, on the left lane's center.

.. admonition:: Reading the figure
   :class: tip

   A close top view, :math:`x` and :math:`y` in meters. The AV (light gray,
   with its three dark circles) is in the left lane (purple, upper); the
   obstacle (blue, with its three blue circles) is right below it in the
   right lane (yellow, lower).

   - **Thick line:** the right lane's center. **Dotted line:** the left
     lane's center. **White dot:** the AV's base link.
   - **Tag 1:** the gap between the two middle circles (the double arrow),
     across the dashed lane line.
   - **1.35 m:** from the AV's base link to its middle circle's center.
   - **3.5 m and 0.3 m (right):** from the right lane's center up to the left
     lane's center, and from the right lane's center down to the obstacle's
     center.
   - **Stack on the left:** from the obstacle's center up to the AV's,
     1.21 m, 1.38 m, 1.21 m.

One pose beside the obstacle: the AV on the left lane's center, its base link
1.35 m behind the obstacle's center, so its middle circle (1.35 m ahead of the
base link) lines up with it.

1. Centers across: lanes are 3.5 m wide (CARLA's map file). The AV is 3.5 m
   left of the right lane's center, the obstacle 0.3 m right: 3.5 + 0.3 =
   3.8 m apart.
2. Gap (tag 1): 3.8 − 2 × 1.21 = 1.38 m.
3. The gap is over the 0.3 m margin, so this pose is free.

The code measures 1.37 m (the lane curves slightly); along the kept path, the
smallest gap is 1.36 m.


.. _l9-lec-conservative:

Circles Can Report a Collision That Is Not There
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/circles_conservative.png
   :alt: The AV and the obstacle side by side from above, the AV light gray on top and the obstacle, a blue car, below, each inside a dashed rectangle, its body's outline, and each with its three circles and their centers, plus signs, outlined in white so they show on the cars. Tag 1 on the right marks the gap between the two dashed outlines, labeled 0.4 m: the bodies do not touch. Further right, a double arrow labeled 2.3 m spans from the AV's centers down to the obstacle's. Small rust lens shapes show where each dark circle overlaps the blue circle below it; tag 2, on the left, points at the rear lens with a line. Above the AV, a short bar labeled 0.26 m spans from the body's side to the top of the middle circle; at the AV's rear, a bar labeled 0.46 m spans from the rear bumper to the edge of the rear circle.
   :width: 60%
   :align: center

   Two bodies that do not touch, with circles that overlap.

.. admonition:: Reading the figure
   :class: tip

   The AV (light gray) on top and the obstacle (blue) below, side by side
   from above. Each body's outline is a dashed rectangle, covered by its
   three circles.

   - **Tag 1:** the gap between the two bodies, 0.4 m. The bodies do not
     touch.
   - **2.3 m:** the distance from the AV's centers down to the other car's.
   - **Tag 2:** the small rust lens shapes, where each dark circle overlaps
     the blue circle below it.
   - **0.26 m and 0.46 m:** how far the circles reach past the AV's body, at
     the side and past the rear bumper.

The AV and the obstacle side by side; the gap between their bodies (dashed),
tag 1, is 0.4 m (chosen).

1. Centers: 0.95 + 0.4 + 0.95 = 2.3 m apart (half a width each).
2. Gap: 2.3 − 2 × 1.21 = −0.12 m: the circles overlap (tag 2).

The circles bulge past the body: 1.21 − 0.95 = 0.26 m at the sides, and
1.21 − 0.75 = 0.46 m past each bumper.

.. important::

   **The circle check is conservative.** The circles cover the whole body,
   so the check never misses a real collision. It can drop a free path, as
   here.


.. _l9-lec-collision-summary:

Where Collision Checking Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where collision checking leaves us
   :class: tip

   - Three circles of radius 1.21 m, at −0.15, 1.35 and 2.85 m from the base
     link, cover the AV; 9 distances per pose.
   - Beside the obstacle, on the left lane's center: centers 3.8 m apart,
     gap 1.38 m by hand (1.36 m smallest along the path the planner keeps).
   - Conservative: bodies 0.4 m apart already count as overlapping.
   - On the road, a gap under 0.3 m is a collision: a 0.29 m bound on the
     AV's position error, rounded.

.. figure:: /_static/images/L9/check_summary.png
   :alt: A flowchart of the collision check, top to bottom. A pose (x, y, theta) on a candidate path. Then: 3 circles of radius 1.21 m on the AV, centers 0.15 m behind, 1.35 m and 2.85 m ahead of the base link. Then: 9 gaps to the obstacle's 3 circles, each the distance between centers minus 1.21 minus 1.21. Then the question: is the smallest gap under 0.3 m? Yes leads to a rust box, collision: drop the candidate. No leads to a green box, free: check the next pose; all free: keep the candidate.
   :width: 60%
   :align: center

   The collision check, one pose at a time.

.. admonition:: Reading the figure
   :class: tip

   The check runs top to bottom, for one pose :math:`(x, y, \theta)` on a
   candidate path.

   - **Second box:** 3 circles of radius 1.21 m on the AV, centered 0.15 m
     behind, 1.35 m and 2.85 m ahead of the base link.
   - **Third box:** 9 gaps to the obstacle's 3 circles; each gap is the
     distance between centers minus 1.21 minus 1.21.
   - **Question:** is the smallest gap under 0.3 m?
   - **Yes (rust box):** collision, drop the candidate.
   - **No (green box):** free, check the next pose. If every pose is free,
     keep the candidate.


.. _l9-lec-frenet:

The Frenet Frame
----------------

We keep configuration space and the circle check: every pose is still
:math:`(x, y, \theta)`, and it is still checked with the circles. We add a
second way to write positions: along the road and across it, instead of the
map's :math:`x` and :math:`y`.

**What it is for:** "stay in the lane" and "move one lane left" become
statements about one number, :math:`d`.


.. _l9-lec-frenet-def:

Two Coordinates That Follow the Road
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Frenet frame
   :class: note

   Coordinates attached to a **reference path**, the curve the AV should
   follow. For a point :math:`P`, its **foot point** :math:`F` is the point of
   the reference closest to :math:`P`: the line from :math:`F` to :math:`P`
   meets the reference at a right angle. Then :math:`s` is the distance along
   the reference from its start to :math:`F`, and :math:`d` is the distance
   from :math:`F` to :math:`P`, positive to the left of the driving direction
   (Werling et al., 2010; see :doc:`the References page <l9_references>`).

.. figure:: /_static/images/L9/frenet_def.png
   :alt: A top view of a piece of the road where it starts to curve upward, a left turn for the AV, x and y in meters. The reference path, the right lane's center, is a thick black line with small ticks every 5 meters labeled 130 to 150 below the road: the value of s. A dark point labeled P sits in the left lane. A white dot labeled F on the reference, at the 140 tick, is its foot point; a small square at F marks the right angle between the reference and the line to P. A solid arrow labeled d runs from F to P. Just outside the road's right edge, an arrow runs along the reference from the left edge of the view to the 140 tick, labeled s = 140 m, from the start; a dotted line drops from F to its end.
   :width: 80%
   :align: center

   A point P, its foot point F, and its two Frenet coordinates.

.. admonition:: Reading the figure
   :class: tip

   A top view of the road where it starts to curve left, :math:`x` and
   :math:`y` in meters.

   - The thick black line is the reference path, the right lane's center
     (:math:`d` = 0). Its ticks mark :math:`s` every 5 m, from 130 to 150.
   - :math:`P` is a point in the left lane.
   - :math:`F` is its foot point. The small square marks the right angle
     between the reference and the line from :math:`F` to :math:`P`.
   - The arrow from :math:`F` to :math:`P` is :math:`d`.
   - The arrow below the road runs along the reference from the left edge of
     the view to the 140 tick: :math:`s` = 140 m, from the start. A dotted
     line joins :math:`F` to its end.

Our reference is the center line of the lane the route picks, read from the
map; here, the right lane's center. :math:`s` = 0 at the start of the scene's
gray stretch: the AV starts at :math:`s` = 60 m, the obstacle at 118 m.

Here :math:`P` is in the left lane. Its foot point :math:`F` is at the 140
tick, so :math:`s` = 140 m. :math:`d` is the arrow from :math:`F` up to
:math:`P`: :math:`d` = 3.0 m, positive because :math:`P` is to the left.


.. _l9-lec-map-d:

On the Map: d Is Measured Across the Road
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/frenet_map.png
   :alt: A top view, to scale, of a piece of our road where it curves left, x and y in meters. The reference, the right lane's center, is a thick black line; the left lane's center is dotted; the lane line is dashed. At three white dots on the reference, at s = 145, 165 and 185, an arrow labeled d = 3.5 m goes from the reference to the left lane's center, at a right angle to the reference; the arrows turn with the road. Tag 3, joined by a thin line, points into the right lane; tag 4 into the left lane.
   :width: 75%
   :align: center

   d on the map, where the road curves.

.. admonition:: Reading the figure
   :class: tip

   A piece of our road where it curves left, to scale. The thick line is the
   reference, the right lane's center; the dotted line is the left lane's
   center. Each lane is 3.5 m wide (measured from CARLA's map file).

   - At each white dot, the arrow goes from the reference to the left lane's
     center, at a right angle to the reference: :math:`d` = 3.5 m.
   - The arrows turn with the road, but :math:`d` stays 3.5 m.
   - **Tag 3:** the right lane. **Tag 4:** the left lane.

.. important::

   The planner builds its candidate paths in :math:`(s, d)`, not on the map.
   It then turns each one back into map points :math:`(x, y)` to check it and
   to hand it to the controller.


.. _l9-lec-unrolled:

The Big Idea: the Road Becomes Straight in (s, d)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now plot the whole road as a graph: :math:`s` along the bottom, :math:`d` up
the side. It is not a picture of the road: the :math:`d` axis is stretched, and
curves do not show.

.. figure:: /_static/images/L9/frenet_sd.png
   :alt: A graph of the road in s and d, both in meters, s from 40 to 236. The right lane, pale yellow, between d = minus 1.75 and 1.75, and the left lane, pale purple, between 1.75 and 5.25, with straight lines at minus 1.75, 1.75 (dashed) and 5.25; the reference as a thick line at d = 0 and the left lane's center dotted at d = 3.5. A black car icon, the AV, sits on the reference with its base link, a white dot, at s = 60; the label d = 0 is just ahead of it on the reference. A blue car icon, the obstacle, is centered at s = 118, just below the reference. Both icons are drawn several times too large. At s = 145, 165 and 185, three equal vertical arrows labeled d = 3.5 m rise from white dots on the reference to the left lane's center. Tags 3 and 4 at s = 215, joined by thin lines, point into the right and left lane bands.
   :width: 80%
   :align: center

   The same road in :math:`(s, d)`.

.. admonition:: Reading the figure
   :class: tip

   - The black car is the AV, its base link (white dot) at :math:`s` = 60 m
     on the reference. The blue car is the obstacle, at :math:`s` = 118 m.
     Both are drawn larger than to scale.
   - **Tag 3:** the right lane. **Tag 4:** the left lane.
   - The thick line is the reference (:math:`d` = 0); the dotted line is the
     left lane's center (:math:`d` = 3.5 m).
   - The three arrows at :math:`s` = 145, 165 and 185 are the three
     :math:`d` arrows of the map figure.

Each lane is a straight band:

- the right lane (tag 3): :math:`d` from −1.75 to +1.75 m; its center is the
  reference, :math:`d` = 0;
- the left lane (tag 4): :math:`d` from +1.75 to +5.25 m.

The three :math:`d` arrows on the map turned with the road; here they stand
straight, all 3.5 m. So "stay in the right lane" is "keep :math:`d` near 0",
"move to the left lane" is "bring :math:`d` to 3.5 m", and progress is
:math:`s` growing.

Werling et al. plan this way: they "generate a one-dimensional trajectory for
both the root point :math:`\vec{r}` along the center line and the
perpendicular offset :math:`d`" (see :doc:`the References page
<l9_references>`). Their root point is our foot point.


.. _l9-lec-frenet-step1:

Step 1: Find the Foot Point F of the Obstacle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To place the obstacle's center :math:`P` (blue) in :math:`(s, d)`, first find
its foot point. The reference is a chain of points (gray dots): CARLA's map
gives one every 0.5 m of its own road length, which on the map comes out 0.50
to 0.55 m apart. The drawing is to scale.

.. figure:: /_static/images/L9/frenet_step1.png
   :alt: A close-up, to scale, of the reference: gray dots about half a meter apart joined by a gray line, running left to right. The piece between dots A and B is drawn thick and black. A blue square P sits below that piece. A dashed line rises from P and meets the piece at a right angle, marked by a small square, at a white dot labeled F, close to B. Above the chain, a dimension shows 0.461 m from A to F and 0.063 m from F to B.
   :width: 85%
   :align: center

   Finding the foot point F of the obstacle's center P.

1. Find the piece of the chain closest to :math:`P`: from :math:`A` to
   :math:`B`, 0.525 m long (measured).
2. Draw the line from :math:`P` that meets that piece at a right angle
   (dashed). It lands 0.879 of the way from :math:`A` to :math:`B`:
   0.879 × 0.525 = 0.461 m past :math:`A`. That point is the foot point
   :math:`F`.

In the map frame: :math:`P` = (155.690, −207.435) m (the obstacle's center,
from the scene), :math:`A` = (155.225, −207.141), :math:`B` = (155.750,
−207.134), :math:`F` = (155.686, −207.135).


.. _l9-lec-frenet-step23:

Step 2 and Step 3: Read s and d
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/frenet_step23.png
   :alt: The same close-up of the reference chain. Above it, an arrow runs from the left edge to A, labeled from the start: 117.539 m, then a dimension from A to F labeled 0.461 m. At F, a short gray arrow labeled n points up, to the left of the reference. A dark arrow labeled d runs from F down to the blue square P.
   :width: 85%
   :align: center

   Reading s along the chain and d across it.

**Step 2,** :math:`s`: the distance along the chain up to :math:`F`. The
pieces before :math:`A` add up to 117.539 m; then 0.461 m more to :math:`F`.
So :math:`s` = 117.539 + 0.461 = 118.00 m.

**Step 3,** :math:`d`: the length of the arrow from :math:`F` to :math:`P`,
0.300 m, with a sign. The arrow :math:`n` points to the reference's left;
:math:`P` is on the other side, so :math:`d` = −0.30 m.

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

.. figure:: /_static/images/L9/frenet_back.png
   :alt: A top view of the road beside the obstacle, x and y in meters. The blue obstacle sits on the thick black reference, the right lane's center. A white dot labeled r on the reference at the obstacle's center; a short gray arrow labeled n points up from it, to the reference's left. A black dot labeled p sits on the dotted center line of the left lane, above r. A double arrow labeled 3.5 m, behind the obstacle, spans from the reference to the left lane's center.
   :width: 70%
   :align: center

   From (s, d) = (118, 3.5) back to the map.

1. :math:`r`: the reference point at :math:`s` = 118 m, (155.686, −207.135).
2. :math:`n`: the arrow of length 1 that points to the reference's left. The
   reference heads 0.81° there (measured from the road's points), so
   :math:`n = (-\sin 0.81^\circ,\ \cos 0.81^\circ)` = (−0.0141, 0.9999).
3. :math:`p`: from :math:`r`, go 3.5 m along :math:`n`.

   - :math:`x` = 155.686 + 3.5 × (−0.0141) = 155.637 m;
   - :math:`y` = −207.135 + 3.5 × 0.9999 = −203.635 m.

.. important::

   :math:`p(s, d) = r(s) + d\,n(s)`: the point on the reference, then
   :math:`d` meters to its left.

.. tip::

   See "The Frenet Formulas" in :doc:`Going Further <l9_appendix>` for a
   path's position, heading and curvature from :math:`(s, d)`.


.. _l9-lec-two-frames:

Why Two Frames: Build in (s, d), Check and Drive in (x, y)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Goal: each step of the planner runs in the frame where it is simplest.

.. figure:: /_static/images/L9/frames_flow.png
   :alt: A flowchart in two bands: the map frame (x, y) on top, gray, and the Frenet frame (s, d) below, dashed. Box 1, in the map frame: the lane points, the AV's pose, the obstacle's box. An arrow labeled to (s, d): foot point goes down to box 2, in the Frenet frame: where each one is, AV s = 60, d = 0, obstacle s = 118, d = minus 0.3. An arrow goes right to box 3: build 31 candidates, d as a curve of s, a lane is a band of d. An arrow labeled back to (x, y) goes up to box 4, in the map frame: check, every gap 0.3 m or more, at most 3 m/s squared sideways. An arrow goes right to box 5: the path as map points, to the controller.
   :width: 90%
   :align: center

   Which step of the planner runs in which frame.

.. admonition:: Reading the figure
   :class: tip

   The top band is the map frame :math:`(x, y)`; the dashed band below is the
   Frenet frame :math:`(s, d)`.

   - **Tag 1** (map frame): the lane points, the AV's pose and the obstacle's
     box. The foot point takes them to :math:`(s, d)`.
   - **Tag 2** (Frenet frame): where each one is. The AV at :math:`s` = 60,
     :math:`d` = 0; the obstacle at :math:`s` = 118, :math:`d` = −0.3.
   - **Tag 3** (Frenet frame): build 31 candidates, each one :math:`d` as a
     curve of :math:`s`; a lane is a band of :math:`d`. Then back to
     :math:`(x, y)`.
   - **Tag 4** (map frame): the check. Every gap is 0.3 m or more, and at
     most 3 m/s² sideways.
   - **Tag 5** (map frame): the path as map points, to the controller.

- **Build in** :math:`(s, d)` (tags 2 and 3): a lane is a band of :math:`d`,
  so "move to the left lane" is :math:`d` going from 0 to 3.5 m as :math:`s`
  grows: one formula, on a straight road or a curve.
- **Check and drive in** :math:`(x, y)` (tags 4 and 5): the circles, the
  obstacle's box and the curve's sharpness are lengths on the real road, and
  the controller steers the AV on the map.


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
   - The frame works on our road; it fails only on tight turns, with a path
     far to their inside.

.. tip::

   See "Where the Frenet Frame Fails" in :doc:`Going Further <l9_appendix>`
   for where the Frenet frame fails, and what to do on a tight turn.


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
2. **Check** each one: drop it if a gap falls under 0.3 m (the circle check)
   or if it pushes the passengers over 3 m/s² (the comfort limit). The other
   two limits need no check here. At 10 m/s, comfort already needs a
   turning radius of 33.3 m, wider than the 3.41 m that steering allows. And
   each candidate is a smooth curve that the AV follows nose first, never
   sideways.
3. **Score** the rest with a cost.
4. **Pick** the cheapest.
5. **Repeat** every 0.5 s, from where the AV is then.


.. _l9-lec-scurve:

Step 1: One Candidate, a Smooth Move Sideways
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/lateral_curve.png
   :alt: A graph of d against s, from s = 55 to 120 meters: the two lanes as bands, the right one pale yellow and the left one pale purple, with the lane edges as horizontal lines at minus 1.75, 1.75 (dashed) and 5.25, the right lane's center as a thick line at d = 0 and the left lane's center dotted at 3.5. Three curves start at the AV, s = 60 and d = 0, flat, rise in an S shape and level off at d = 3.5: a solid one reaches 3.5 at s = 80, a dashed one at s = 90, a dotted one at s = 100; a dot marks each arrival, labeled 20 m, 30 m and 40 m. After that each stays at 3.5. Near the right edge, an arrow rises from the reference to 3.5, labeled d end = 3.5 m.
   :width: 80%
   :align: center

   Three moves to the left lane's center, over three lengths.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a picture of the road: :math:`d` against :math:`s`, with the
   :math:`d` axis stretched.

   - **Yellow band:** the right lane, centered on the reference path
     (:math:`d` = 0, the thick line).
   - **Purple band:** the left lane, centered at :math:`d` = 3.5 m (the
     dotted line).
   - **Dashed line:** the lane line, at :math:`d` = 1.75 m.
   - **Solid, dashed and dotted curves:** three candidates from the AV at
     :math:`s` = 60 m. Each dot marks where a curve reaches 3.5 m: after
     20 m (solid), 30 m (dashed) and 40 m (dotted).
   - **Arrow:** :math:`d_\text{end}` = 3.5 m, measured from the reference.

- Two numbers set a candidate: :math:`d_\text{end}`, the :math:`d` it ends
  at, and the **maneuver length**, how far along :math:`s` it travels to get
  there.
- Here :math:`d_\text{end}` = 3.5 m for all three, with maneuver lengths of
  20, 30 and 40 m from the AV at :math:`s` = 60 m (the numbers on the
  figure). After that, each candidate keeps :math:`d_\text{end}`.

.. tip::

   See "The S Curve" in :doc:`Going Further <l9_appendix>` for the S
   curve's formula.


.. _l9-lec-candidate-set:

Step 1: the Candidate Set, 30 Shifts and One Stop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal is a fixed set of candidates, built the same way every 0.5 s.

.. figure:: /_static/images/L9/candidate_set.png
   :alt: A graph of d against s, s from 57 to 132 meters, the right lane pale yellow and the left lane pale purple. A black car icon, the AV, at s = 60 and d = 0. Thirty thin dark curves leave it, solid, dashed or dotted, and level off at ten values of d from minus 0.5 to 4 meters, every 0.5; a dot marks where each one levels off, at s = 80 for the solid ones, 90 for the dashed ones and 100 for the dotted ones. A thick dark line stays at d = 0 and ends with a bar at s = 110. A blue car icon, the obstacle, at s = 118 just below d = 0. A legend names the line styles 20 m, 30 m and 40 m, and the thick line stop behind.
   :width: 85%
   :align: center

   The 31 candidates from the AV at :math:`s` = 60 m.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a picture of the road: the :math:`d` axis is stretched.

   - **Black car:** the AV, at :math:`s` = 60 m. **Blue car:** the obstacle,
     at :math:`s` = 118 m. Each icon is as long as the car; its width is not
     to scale.
   - **Solid, dashed and dotted curves:** the 20 m, 30 m and 40 m maneuvers.
     The dots mark where each one levels off at its :math:`d_\text{end}`.
   - **Thick line:** stop behind, at :math:`d` = 0, ending with a bar at
     :math:`s` = 110 m.

**Chosen for this example:**

- **10 end offsets:** :math:`d_\text{end}` from −0.5 to 4.0 m, every 0.5 m
  (the dots). The 0.5 m step is chosen because it lands on both lane
  centers, 0 and 3.5 m.
- **3 maneuver lengths:** 20, 30 and 40 m (solid, dashed, dotted). They are
  2, 3 and 4 s at 10 m/s, from a sharp move to a gentle one.
- **1 stop behind** the obstacle: keep the lane, with the AV's front bumper
  2.0 m short of the obstacle's rear (the thick line).

In all: 10 × 3 + 1 = 31 candidates. The 30 shifts are each 70 m long.


.. _l9-lec-offset-limits:

Why Those End Offsets: the AV Stays on the Two Lanes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every end offset keeps the AV's whole body on the two lanes, which run from
:math:`d` = −1.75 to 5.25 m.

.. figure:: /_static/images/L9/offset_limits.png
   :alt: A straight piece of the two lanes, to scale, d in meters up the side: the right lane pale yellow from minus 1.75 to 1.75, the left lane pale purple from 1.75 to 5.25, a dashed lane line between them. Two light gray AVs heading right, each in a dashed 4.5 by 1.9 meter outline with a dotted center line. The lower one, at d = minus 0.5: a bar of 0.95 m from its center line down to its body's side, and a bar of 0.30 m from there to the road's lower edge. The upper one, at d = 4: a bar of 0.95 m up to its body's side, and a bar of 0.30 m from there to the road's upper edge.
   :width: 85%
   :align: center

   The AV at the lowest and the highest end offset.

.. admonition:: Reading the figure
   :class: tip

   A piece of the two lanes, drawn to scale.

   - **Lower AV:** at :math:`d` = −0.5 m, the lowest end offset. Its dotted
     center line, then 0.95 m down to the side of its body, then 0.30 m to
     the road's lower edge.
   - **Upper AV:** at :math:`d` = 4.0 m, the highest end offset. 0.95 m up to
     the side of its body, then 0.30 m to the road's upper edge.
   - **Dashed boxes:** the AV's body, 4.5 m long and 1.9 m wide.

The body reaches 0.95 m to each side of its center (half of 1.9 m).

1. Lowest: −0.5 − 0.95 = −1.45, so 0.30 m inside the edge at −1.75.
2. Highest: 4.0 + 0.95 = 4.95, so 0.30 m inside the edge at 5.25.


.. _l9-lec-drop:

Step 2: Drop Paths That Collide or Turn Too Hard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/candidates_frenet.png
   :alt: A graph of d against s with all 31 candidates from the AV at s = 60. A black car icon, the AV, sits at s = 60. The obstacle is a blue car icon at s = 118, d around 0. Thin rust curves end at d from minus 0.5 to 2.0 and run into or beside the obstacle: they collide. Purple dashed curves rise steeply to 2.5 to 4.0 within 20 meters: too sharp. Gray curves end at 2.5 to 4.0 after 30 or 40 meters. One thick green curve ends at 3.5 after 40 meters. A black dotted line stays at d = 0 and ends with a bar at s = 110: stop behind. A legend names cheapest, kept, stop behind, collides and too sharp.
   :width: 90%
   :align: center

   All 31 candidates, sorted by what happens to them.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a picture of the road: :math:`d` against :math:`s`, with the
   :math:`d` axis stretched. The black car is the AV, at :math:`s` = 60 m;
   the blue car is the obstacle, at :math:`s` = 118 m.

   - **Rust, collides:** the curves that end at :math:`d` from −0.5 to
     2.0 m. They run into the obstacle or too close beside it.
   - **Purple dashed, too sharp:** the 20 m moves to 2.5 to 4.0 m.
   - **Gray, kept:** the 30 m and 40 m moves to 2.5 to 4.0 m.
   - **Green, cheapest:** 3.5 m over 40 m (Step 4).
   - **Black dotted, stop behind:** stays at :math:`d` = 0 and ends with a
     bar at :math:`s` = 110 m.

- **18 collide** (rust): the circle check finds the AV on them within 0.3 m
  of the obstacle.
- **4 are too sharp** (purple): over 3 m/s² sideways.
- **9 are kept**, stop behind included.

.. tip::

   See "The S Curve" in :doc:`Going Further <l9_appendix>` for how hard a
   candidate turns, by hand.


.. _l9-lec-cost-terms:

Step 3: the Four Cost Terms
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each kept candidate gets a cost: the sum of four terms, each a number times
its weight. Lower is better. All weights are **chosen** for this example.

.. list-table::
   :widths: 12 22 44 22
   :header-rows: 1
   :class: compact-table

   * - **Term**
     - **What raises it**
     - **The number**
     - **Weight**
   * - Comfort
     - a hard push sideways
     - the largest sideways acceleration along the path, in m/s²
     - 2 per m/s²
   * - Clearance
     - passing close to the obstacle
     - how much the smallest gap is short of 1.5 m (0 for a gap of 1.5 m or
       more)
     - 4 per m short
   * - Lane
     - ending in another lane than the route's, or away from a lane's center
     - where the path ends: 0 if in the route's lane, 1 if one lane over; and
       meters from the nearest lane center
     - 2 per lane, 2 per m
   * - Progress
     - covering less road
     - meters of the 70 m ahead that the path does not cover
     - 0.5 per m

.. important::

   1 m/s² of extra sideways acceleration costs as much as 4 m of lost
   progress (2 = 0.5 × 4). Change a weight and a different path can win: the
   spreadsheet exercise and the hands-on let you try it.


.. _l9-lec-score-a:

Step 3: Score Candidate A, the Left Lane over 40 m
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Candidate A: :math:`d_\text{end}` = 3.5 m, maneuver 40 m. The numbers in the
steps are the script's, rounded.

.. figure:: /_static/images/L9/score_A.png
   :alt: A graph of d against s, s from 57 to 132 meters, the right lane pale yellow, the left lane pale purple, the right lane's center a thin black line and the left lane's center dotted at 3.5. A black car icon, the AV, at s = 60, d = 0; a blue car icon, the obstacle, at s = 118 just below d = 0. A thick green curve leaves the AV and rises to d = 3.5, reached at s = 100, then runs straight to s = 130. Tag 1 points at a ring on the curve near s = 68, where it bends hardest. Tag 2 points at a ring on the curve at s = 116.5, beside the obstacle. Tag 3 points at a dot where the curve ends, at s = 130 on the left lane's center. Tag 4 sits above a double arrow from s = 60 to 130 near the bottom.
   :width: 70%
   :align: center

   Candidate A and the four places its cost comes from.

.. admonition:: Reading the figure
   :class: tip

   A graph: the :math:`d` axis is stretched. The black car is the AV, the
   blue car the obstacle, and the green curve candidate A. The tags match
   the steps below.

   - **Tag 1:** the ring near :math:`s` = 68 m, where the curve bends
     hardest (comfort).
   - **Tag 2:** the ring at :math:`s` = 116.5 m, beside the obstacle
     (clearance).
   - **Tag 3:** the dot where the path ends, at :math:`s` = 130 m on the left
     lane's center (lane).
   - **Tag 4:** the double arrow from :math:`s` = 60 to 130 m, the road the
     path covers (progress).

1. **Comfort** (tag 1): peak 1.25 m/s². 2 × 1.253 = 2.51.
2. **Clearance** (tag 2): smallest gap 1.36 m (the circle check).
   4 × (1.5 − 1.359) = 0.56.
3. **Lane** (tag 3): one lane from the route's, on the left lane's center.
   2 × 1 + 2 × 0 = 2.00.
4. **Progress** (tag 4): it covers all 70 m. 0.5 × 0 = 0.

.. important::

   Cost of A: 2.51 + 0.56 + 2.00 + 0 = 5.07.


.. _l9-lec-score-b:

Step 3: Score Candidate B, Closer to the Obstacle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Candidate B: :math:`d_\text{end}` = 3.0 m, maneuver 40 m. It moves 0.5 m
less, so it bends less, but it passes closer.

.. figure:: /_static/images/L9/score_B.png
   :alt: A graph of d against s, s from 57 to 132 meters, the right lane pale yellow, the left lane pale purple, the right lane's center a thin black line and the left lane's center dotted at 3.5. A black car icon, the AV, at s = 60, d = 0; a blue car icon, the obstacle, at s = 118 just below d = 0. A thick gray curve leaves the AV and rises to d = 3.0, reached at s = 100, then runs straight to s = 130, 0.5 m below the left lane's center. Tag 1 points at a ring near s = 68, where it bends hardest. Tag 2 points at a ring at s = 116.5, beside the obstacle. Tag 3 points at a dot where the curve ends at s = 130, with a short bar from it up to the left lane's center. Tag 4 sits above a double arrow from s = 60 to 130 near the bottom.
   :width: 70%
   :align: center

   Candidate B and the four places its cost comes from.

.. admonition:: Reading the figure
   :class: tip

   A graph: the :math:`d` axis is stretched. The gray curve is candidate B.
   The tags match the steps below.

   - **Tag 1:** the ring near :math:`s` = 68 m, where the curve bends
     hardest (comfort).
   - **Tag 2:** the ring at :math:`s` = 116.5 m, beside the obstacle
     (clearance).
   - **Tag 3:** the dot where the path ends, at :math:`s` = 130 m. The short
     bar above it is the 0.5 m to the left lane's center (lane).
   - **Tag 4:** the double arrow from :math:`s` = 60 to 130 m, the road the
     path covers (progress).

1. **Comfort** (tag 1): peak 1.08 m/s². 2 × 1.076 = 2.15.
2. **Clearance** (tag 2): smallest gap 0.86 m. 4 × (1.5 − 0.859) = 2.56.
3. **Lane** (tag 3): one lane from the route's, 0.5 m off the left lane's
   center. 2 × 1 + 2 × 0.5 = 3.00.
4. **Progress** (tag 4): it covers all 70 m. 0.

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

.. figure:: /_static/images/L9/score_C.png
   :alt: A graph of d against s, s from 57 to 132 meters, the right lane pale yellow, the left lane pale purple, the right lane's center a thin black line and the left lane's center dotted at 3.5. A black car icon, the AV, at s = 60, d = 0; a blue car icon, the obstacle, at s = 118 just below d = 0. A thick dotted black line stays at d = 0 from the AV to s = 110.15, where a bar marks the stop, 2 meters short of the obstacle. Tag 1 points at the straight line. Tags 2 and 3 point at a ring at the stop. Tag 4 sits above a double arrow from s = 60 to 110.15 near the bottom; from there to s = 130, a gray hatched strip marks the road it does not cover.
   :width: 70%
   :align: center

   Candidate C and the four places its cost comes from.

.. admonition:: Reading the figure
   :class: tip

   A graph: the :math:`d` axis is stretched. The thick dotted line is
   candidate C. The tags match the steps below.

   - **Tag 1:** the straight line at :math:`d` = 0 (comfort).
   - **Tags 2 and 3:** the ring at the stop, :math:`s` = 110.15 m, where the
     bar marks the end of the path (clearance and lane).
   - **Tag 4:** the double arrow from :math:`s` = 60 to 110.15 m, the road
     the path covers. The hatched strip from 110.15 to 130 m is the road it
     does not cover (progress).

1. **Comfort** (tag 1): the path is straight. 2 × 0.000 = 0.00.
2. **Clearance** (tag 2): 2.0 m lie between the bumpers, but the circles of
   the circle check reach past them: smallest gap 1.10 m.
   4 × (1.5 − 1.096) = 1.62.
3. **Lane** (tag 3): the route's lane, centered. 0.
4. **Progress** (tag 4): it covers 110.15 − 60 = 50.15 m of 70 m.
   0.5 × (70 − 50.15) = 9.93.

.. important::

   Cost of C: 0 + 1.62 + 0 + 9.93 = 11.55 (11.54 unrounded). Stopping costs
   nothing for comfort or the lane, but the 19.85 m of lost progress costs
   9.93.


.. _l9-lec-csv-columns:

Exercise: What Each Column of candidates.csv Holds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal is to know each number before you score with it. The file
``candidates.csv`` has 31 rows, one per candidate. Candidate A is the row
named ``d_end 3.5 m, 40 m``.

.. list-table::
   :widths: 30 44 13 13
   :header-rows: 1
   :class: compact-table

   * - **Column**
     - **What it holds**
     - **Cost term**
     - **Row of A**
   * - ``name``
     - the end offset and length, or ``stop behind``
     -
     - see above
   * - ``d_end_m``
     - where the path ends across the road (m)
     -
     - 3.5
   * - ``maneuver_m``
     - the maneuver length (m); empty for stop behind
     -
     - 40.0
   * - ``peak_lat_accel_mps2``
     - the largest sideways acceleration (m/s²)
     - comfort
     - 1.253
   * - ``smallest_gap_m``
     - the smallest circle-to-circle gap (m); under 0 means overlap
     - clearance
     - 1.359
   * - ``lanes_away``
     - 0 if the path ends in the route's lane, 1 if one lane over
     - lane
     - 1
   * - ``off_center_m``
     - meters from the nearest lane center, at the end
     - lane
     - 0.0
   * - ``not_covered_m``
     - meters of the 70 m ahead not covered
     - progress
     - 0.0
   * - ``dropped``
     - ``collision``, ``too sharp``, or empty (kept)
     -
     - empty


.. _l9-lec-spreadsheet:

Exercise, Part 1: Score Every Candidate in a Spreadsheet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal is to compute the cost of each candidate yourself. Work in pairs.

Open ``candidates.csv``, from folder ``lecture9`` of the course's Python
repository (see :doc:`the Code page <l9_code>`), in Excel, Google Sheets or
LibreOffice Calc. It has 31 rows, one per candidate, with the numbers the
cost needs and no costs.

1. Delete the 22 rows whose ``dropped`` column is not empty (``collision``
   or ``too sharp``): the planner never scores them. 9 rows remain.
2. Type the five weights in cells of their own, outside the 9 rows: comfort
   2, clearance 4, lane 2, center 2, progress 0.5. In formulas, refer to
   them with ``$`` (``$L$2``, not ``L2``), so sorting the rows does not
   break the totals.
3. Add five columns. Each formula uses the weight cells and the row's
   columns:

.. list-table::
   :widths: 18 82
   :header-rows: 1
   :class: compact-table

   * - **Column**
     - **Formula**
   * - comfort
     - comfort weight × ``peak_lat_accel_mps2``
   * - clearance
     - clearance weight × the larger of 0 and (1.5 − ``smallest_gap_m``)
   * - lane
     - lane weight × ``lanes_away`` + center weight × ``off_center_m``
   * - progress
     - progress weight × ``not_covered_m``
   * - total
     - comfort + clearance + lane + progress


.. _l9-lec-spreadsheet-weights:

Exercise, Part 2: Change the Weights, See Who Wins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal is to see how the weights decide which path the AV drives.

1. Sort the rows by **total**, smallest first (LibreOffice Calc: click a
   cell of the total column, then Data, Sort Ascending). Check: the row
   ``d_end 3.5 m, 40 m`` (candidate A) is first, at 5.07.
2. Change the clearance weight from 4 to **10** and sort again. Which row is
   first now? At what :math:`d_\text{end}` does that path end, and why does
   a larger clearance weight favor it?
3. Put the clearance weight back to 4. Change the progress weight from 0.5
   to **0** and sort again. Which row is first now? What would the AV do,
   and why?

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

The 9 candidates that pass the check, cheapest first:

.. list-table::
   :widths: 10 22 20 32 16
   :header-rows: 1
   :class: compact-table

   * - **Rank**
     - **Candidate**
     - **Ends at** :math:`d_\text{end}`
     - **Maneuver length**
     - **Cost**
   * - 1
     - A
     - 3.5 m
     - 40 m
     - 5.07
   * - 2
     -
     - 4.0 m
     - 40 m
     - 5.86
   * - 3
     -
     - 3.5 m
     - 30 m
     - 6.99
   * - 4
     - B
     - 3.0 m
     - 40 m
     - 7.72
   * - 5
     -
     - 4.0 m
     - 30 m
     - 8.04
   * - 6
     -
     - 3.0 m
     - 30 m
     - 9.37
   * - 7
     -
     - 2.5 m
     - 40 m
     - 10.40
   * - 8
     - C, stop behind
     - 0 m
     - none (stops at 110.15 m)
     - 11.54
   * - 9
     -
     - 2.5 m
     - 30 m
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
:math:`s` = 118 m. You start CARLA first, then build the package and launch
it (README, "Run it"). A second launch file, ``demo_obstacles.launch.py``,
adds three parked cars. In a second terminal, ``ros2 param set`` changes a
weight while the demo runs. The commands are on :doc:`the Code page
<l9_code>`.

- RViz draws every candidate in the colors of these figures, and the AV's
  circles. Its Camera panel shows CARLA's view from behind the AV.
- Every 0.5 s the AV moves along the first 0.5 s of the cheapest path, then
  plans again. The demo places the AV on the path; the controller that
  drives it comes in the next lecture.
- A changed weight takes effect at the next plan: the path changes while you
  watch.


.. _l9-lec-handson-sample:

Hands-On, Part 2: Sample, Score, Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``sample`` part draws every candidate with its costs; the ``drive`` part
plans again every 0.5 s. Both are in folder ``lecture9`` of the course's
Python repository, and the commands are on :doc:`the Code page <l9_code>`.
You start no CARLA server: the scripts need numpy and matplotlib only, and
read the road saved from CARLA's map.

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


.. _l9-lec-behavior:

Behavior
--------

We add the layer that picks the task the local planner carries out.

**What it is for:** the local planner finds the best path for a task; it
does not choose the task (pass or wait, park or keep searching).


.. _l9-lec-decides:

What the Behavior Layer Decides
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Goal: split the job in two. The behavior layer says **what** to do; the local
planner works out **how**, as a path.

.. list-table::
   :widths: 28 30 42
   :header-rows: 1
   :class: compact-table

   * - **The behavior layer decides**
     - **The local planner then**
     - **On our road**
   * - which lanes the AV may use
     - samples :math:`d_\text{end}` only inside them
     - both lanes open: :math:`d_\text{end}` from −0.5 to 4.0 m, 31
       candidates; left lane closed: −0.5 to 0.5 m, 10 candidates (next
       part)
   * - where the AV must stop, and by when
     - keeps every path short of that :math:`s`
     - none in our example: the paths run the full 70 m
   * - a speed limit for this stretch
     - scores comfort at that speed
     - 10 m/s: every bend needs a radius of 33.3 m or more

- The behavior layer decides from facts that change slowly: a lane is open
  or closed, a spot is free or taken.
- The local planner works from exact positions, and plans again every 0.5 s.
- In the rest of this section, a game decides a choice that depends on
  another driver, and a finite state machine picks the behavior. A game can
  be one of the machine's conditions.


.. _l9-lec-one-decision:

One Decision Changes the Cheapest Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/behavior_restricted.png
   :alt: A top view of the road with the AV at the left and the obstacle ahead in the lower lane, x and y in meters. The upper lane is cross-hatched in gray: not allowed. In it, behind the AV, a blue car, tag 1, with a dashed arrow running ahead of it along the upper lane past the AV, tag 2. Thin rust candidate lines stay in the lower lane and run into the obstacle. A thick green line stays in the lower lane and ends with a bar behind the obstacle. A legend names cheapest: stop behind, and collides.
   :width: 95%
   :align: center

   The candidates when the left lane is closed.

.. admonition:: Reading the figure
   :class: tip

   The road from above, the AV at the left and the obstacle ahead in the
   lower (right) lane.

   - **Tag 1:** a fast blue car in the upper (left) lane, behind the AV.
   - **Tag 2:** the dashed arrow: prediction says that car keeps going, past
     the AV.
   - **Hatched lane:** the behavior layer has closed the left lane.
   - **Thin rust lines:** candidates that stay in the right lane and collide
     with the obstacle.
   - **Thick green line:** the cheapest, stop behind. It stays in the lane
     and ends with a bar behind the obstacle.

Suppose a fast car (tag 1) is coming up in the left lane, prediction says it
keeps going (tag 2), and the behavior layer closes that lane (hatched). The
sampler keeps :math:`d_\text{end}` ≤ 0.5 m, so the AV's body stays in the
right lane: 0.5 + 0.95 = 1.45 m, inside the lane line at 1.75 m.

1. 3 end offsets (−0.5, 0 and 0.5 m) × 3 lengths + 1 = 10 candidates.
2. The 9 that are not stop behind all collide: at :math:`d_\text{end}` =
   0.5 m, the centers are 0.5 + 0.3 = 0.8 m apart across, under
   2 × 1.21 = 2.42 m.
3. Stop behind is the only one left, at cost 11.54: the AV waits.


.. _l9-lec-game:

The Lane Change as a Game
~~~~~~~~~~~~~~~~~~~~~~~~~

The last part closed the left lane because another car was coming up in it.
That car has a driver who chooses too, and each choice changes what is best
for the other.

- The AV chooses: **go** (move into the left lane now) or **wait** (stop
  behind the obstacle).
- The other car chooses: **keep** its speed, or **yield** (slow down and let
  the AV in).
- Each pair of choices costs each of them seconds of delay; a crash costs
  100. All numbers are chosen for this example.

.. admonition:: Definition: Nash equilibrium
   :class: note

   A **Nash equilibrium** is a strategy pair in which no player can achieve
   a better outcome by changing their strategy while the other player keeps
   theirs unchanged. If even one player can improve their payoff by
   deviating, then the outcome is **not** a Nash equilibrium. Named after
   John Nash, who introduced it in 1950 (see :doc:`the References page
   <l9_references>`).

Here a strategy is a choice (go or wait, keep or yield), and the outcome is
the delay: lower is better.


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

Instructions:

1. Keep the other car's choice as it is. If the AV made its other choice
   (wait instead of go, or go instead of wait), would its delay be lower?
2. Keep the AV's choice as it is. If the other car made its other choice
   (yield instead of keep, or keep instead of yield), would its delay be
   lower?

A cell where both answers are no is a Nash equilibrium. How many does this
game have?


.. _l9-lec-two-equilibria:

Two Equilibria: the AV Goes First Only When It Is Sure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each cell gives the AV's delay, then the other car's, in seconds. An arrow
means one driver gets a lower delay by switching while the other keeps its
choice (solid: the AV; dashed: the other car).

.. figure:: /_static/images/L9/nash_arrows.png
   :alt: A two by two grid. Columns: other car keeps, other car yields. Rows: AV goes, AV waits. Cells: AV goes and car keeps, AV 100, car 100, a crash; AV goes and car yields, AV 0, car 2; AV waits and car keeps, AV 3, car 0; AV waits and car yields, AV 3, car 2. A solid arrow from the crash cell down to the AV waits and car keeps cell, labeled AV: 100 to 3. A dashed arrow from the crash cell right to the AV goes and car yields cell, labeled car: 100 to 2. A solid arrow from the bottom right cell up to the AV goes and car yields cell, labeled AV: 3 to 0. A dashed arrow from the bottom right cell left to the AV waits and car keeps cell, labeled car: 2 to 0. The two cells with arrows coming in and none going out, AV goes and car yields, and AV waits and car keeps, have a double border, tag 1 and the words: No arrow leaves the cell: Equilibrium.
   :width: 65%
   :align: center

   The lane change game, with the switches that lower a delay.

.. admonition:: Reading the figure
   :class: tip

   The rows are the AV's choices (go, wait); the columns are the other car's
   (keep, yield). Each cell gives the AV's delay, then the car's.

   - **Solid arrows:** the AV switches its choice and lowers its delay, for
     example from the crash (100) to waiting (3).
   - **Dashed arrows:** the other car switches its choice and lowers its
     delay, for example from the crash (100) to yielding (2).
   - **Tag 1:** the two cells with a double border. Arrows come in, and no
     arrow leaves them: they are the equilibria.

Tag 1: these two cells are Nash equilibria. In each, "no player can achieve
a better outcome by changing their strategy while the other player keeps
theirs unchanged".

- **AV goes, car yields:** if the AV waits instead, its delay goes from 0 to
  3 s; if the car keeps its speed instead, they crash.
- **AV waits, car keeps:** if the AV goes instead, they crash; if the car
  yields instead, its delay goes from 0 to 2 s.

.. important::

   Going first is a bet: 0 s if the other car yields, but a crash if it
   keeps its speed. So the AV goes first only when prediction says the car
   will yield; otherwise it waits, 3 s.

.. tip::

   See "Behavior as an MDP" in :doc:`Going Further <l9_appendix>` for the
   lane change as an MDP (Markov decision process): how sure is sure.


.. _l9-lec-prisoner:

Exercise: Find the Nash Equilibrium of the Prisoner's Dilemma
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same check works on any game of two players. The classic one: two
suspects, A and B, are questioned in separate rooms. Each one either stays
**silent** or **confesses**. Each cell of the table gives their sentences:
A's years, then B's (fewer is better).

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * -
     - **B stays silent**
     - **B confesses**
   * - **A stays silent**
     - A 1, B 1
     - A 10, B 0
   * - **A confesses**
     - A 0, B 10
     - A 5, B 5

With your neighbor:

1. For each cell: keep B's choice as it is; would A get fewer years with its
   other choice? Then keep A's choice as it is; would B? A cell where both
   answers are no is a Nash equilibrium.
2. Which cell is the equilibrium? Is it the best cell for the two of them
   together?


.. _l9-lec-prisoner-answer:

Prisoner's Dilemma Answer: Both Confess, the Only Equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each cell gives A's years, then B's. An arrow means one suspect gets fewer
years by switching while the other keeps its choice (solid: A; dashed: B).

.. figure:: /_static/images/L9/nash_pd.png
   :alt: A two by two grid. Columns: B stays silent, B confesses. Rows: A stays silent, A confesses. Cells: both silent, A 1, B 1, with tag 2; A silent and B confesses, A 10, B 0; A confesses and B silent, A 0, B 10; both confess, A 5, B 5. Solid arrows go down: from A 1, B 1 to A 0, B 10, labeled A: 1 to 0, and from A 10, B 0 to A 5, B 5, labeled A: 10 to 5. Dashed arrows go right: from A 1, B 1 to A 10, B 0, labeled B: 1 to 0, and from A 0, B 10 to A 5, B 5, labeled B: 10 to 5. The both confess cell has arrows coming in and none going out; it has a double border, tag 1 and the words: No arrow leaves the cell: Equilibrium.
   :width: 65%
   :align: center

   The Prisoner's Dilemma, with the switches that lower a sentence.

.. admonition:: Reading the figure
   :class: tip

   The rows are A's choices (stay silent, confess); the columns are B's.
   Each cell gives A's years, then B's.

   - **Solid arrows** go down: A confesses instead of staying silent and
     gets fewer years (1 to 0, and 10 to 5).
   - **Dashed arrows** go right: B confesses instead of staying silent and
     gets fewer years (1 to 0, and 10 to 5).
   - **Tag 1:** the both confess cell, with a double border. Arrows come in,
     and no arrow leaves it: it is the equilibrium.
   - **Tag 2:** the both silent cell. Two arrows leave it.

- **Tag 1:** the only Nash equilibrium (arrows leave every other cell): "no
  player can achieve a better outcome by changing their strategy while the
  other player keeps theirs unchanged". If A stays silent instead, A gets 10,
  not 5; if B does, B gets 10, not 5.
- **Tag 2:** not an equilibrium: each suspect gets 0 years instead of 1 by
  confessing.

.. important::

   At the equilibrium each suspect gets 5 years. Both would get 1 if both
   stayed silent, but neither gets there alone: the one who switches to
   silent alone gets 10.


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
- Our example is parking in a garage, where the next section plans the
  paths.


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
**chose** the states and conditions for this lecture; the double border
marks the final state.


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


.. _l9-lec-three-tools:

FSM, Game and MDP: Three Tools That Work Together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Goal: see where each tool of this section fits; each answers a different
question.

.. list-table::
   :widths: 17 43 40
   :header-rows: 1
   :class: compact-table

   * - **Tool**
     - **The question it answers**
     - **In this lecture**
   * - FSM
     - Which behavior is the AV in, and when does it switch?
     - Enter, Search, Approach, Reverse in, Parked; one condition per
       transition
   * - Game (Nash)
     - When another driver's choice changes the outcome, what should the AV
       choose?
     - the lane change: go or wait, against keep or yield
   * - MDP (:doc:`appendix <l9_appendix>`)
     - The same choice, when the AV knows only how likely the other driver's
       choice is
     - go only if the chance that the other car yields is above 97 %

.. important::

   The FSM is the structure; a game or an MDP can decide one of its
   conditions: "Follow lane" to "Change lane" can wait for the lane change
   game to say go. Most conditions are plain checks, such as "the AV has
   passed the entry gate".


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
     flicker. The two work together: a game can decide one of the FSM's
     conditions.


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
obstacles (all chosen).

The goal is given, not found: picking a spot is the behavior layer's job,
and its FSM would take the nearer of the two tag 3 spots, the first free spot
it passes. We chose tag 2
for a longer drive that ends in reverse. Each planner below plans that
drive, from tag 1.


.. _l9-lec-grid-garage:

Grid Search on the Whole Garage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/garage_grid.png
   :alt: The garage top view, x and y in meters, covered by a fine grid of light gray lines, one every 0.5 meters, with a light rust band around every obstacle, the parked cars and the walls: cells the AV's base link may not enter. A green line of small squares leaves the AV at the left along the aisle, steps up in short diagonal pieces, then turns straight up into the free spot of the top row and ends where the goal is.
   :width: 70%
   :align: center

   Grid search's path through the garage.

.. admonition:: Reading the figure
   :class: tip

   - **Light gray lines:** the grid, one line every 0.5 m.
   - **Light rust band,** around every obstacle, the parked cars and the
     walls: the cells the AV's base link may not enter.
   - **Green line of small squares:** the path, one square per cell. It
     leaves the AV along the aisle, steps up in short diagonal pieces, then
     turns straight up into the free spot and ends at the goal.

Grid search moves from cell to cell. The settings:

- cells of 0.5 m;
- each car and wall grown by 1.05 m (rust): half the AV's width plus a
  0.1 m margin, 1.9 / 2 + 0.1 = 1.05 m, chosen for the garage;
- eight neighbors per cell;
- A* with the straight-line distance to the goal as its estimate.

Result: 514 cells expanded, a 27.4 m path.

- The path has 9 corners of 45°: the heading would jump at each one.
- The search knows no heading, so it cannot place the 4.5 m body. The cars
  grow only by half the AV's width, and the path ends nose first, not
  backed in.


.. _l9-lec-grid-step1:

Grid Search, Step 1: Count the Steps from the Start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/toy_wavefront.png
   :alt: A grid of 5 rows and 7 columns. Blue cells are obstacles (parked cars): the top two rows except the fourth column, and the bottom row except the third and fourth columns. White cells hold numbers. Tag 1 marks the start cell, row 4 at the left, holding a bold 0. Its row reads 0 to 6 from left to right; the row above reads 1 to 7. The bottom row's free cells read 3 and 4. The fourth column above reads 5, then a bold 6 at the top: the goal, tag 2.
   :width: 55%
   :align: center

   The number of steps from the start, in every free cell.

.. admonition:: Reading the figure
   :class: tip

   A grid of 5 rows and 7 columns. Blue cells are obstacles (parked cars);
   each white cell holds its number of steps from the start.

   - **Tag 1:** the start cell, holding a bold 0. Its row reads 0 to 6 from
     left to right, and the row above reads 1 to 7.
   - **Tag 2:** the goal, at the top of the fourth column, holding a bold 6.

A piece of the garage as a grid, chosen for this example. Blue cells are
taken. The AV may step to one of the four neighbors of its cell.

1. Write 0 in the start cell (tag 1).
2. Write 1 in each free neighbor of a 0, then 2 in each empty free neighbor
   of a 1, and so on.
3. Stop when the goal cell (tag 2) gets a number: 6.

This is Dijkstra's algorithm with every step costing 1.


.. _l9-lec-grid-step2:

Grid Search, Step 2: Walk Back from the Goal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/toy_path.png
   :alt: The same grid with the path shaded green: from the start cell 0 right through 1, 2 and 3 along the row, then up through 4, 5 and 6 to the goal in the top row.
   :width: 55%
   :align: center

   The path, read back from the goal.

.. admonition:: Reading the figure
   :class: tip

   The same grid. The green cells are the path: from the start (0) right
   through 1, 2 and 3 along the row, then up through 4, 5 and 6 to the goal.

Step 1 says the goal is 6 steps away, not which way. Each number counts
steps from the start, so from the goal a neighbor one lower is always one
step nearer the start. From the start, the numbers cannot tell which 1
leads to the goal.

4. From the goal (6), step to a neighbor holding 5, then 4, and so on down
   to 0. Where two neighbors tie, either one gives a 6-step path.
5. Read it forward: right 3 cells, then up 3 cells.

.. important::

   The path turns 90° inside one cell. A cell has no heading, so the search
   does not know that the AV cannot turn on the spot.


.. _l9-lec-hybrid:

Hybrid A*: an Exact Pose in Every Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Hybrid A*
   :class: note

   A* over a grid of :math:`(x, y, \theta)` cells. Plain A* visits only the
   cell centers; hybrid A* keeps in each cell an exact pose, one the AV
   reaches by driving from the pose before it.

.. figure:: /_static/images/L9/hybrid_primitives.png
   :alt: A light gray AV facing right with its base link at the origin, x and y in meters. Five solid black arcs leave the base link forward, curving from hard left to hard right, tag 1. Five dashed arcs leave it backward, tag 2. Each arc is 3 meters long and ends in a dot.
   :width: 55%
   :align: center

   The ten arcs the AV can drive from one pose.

.. admonition:: Reading the figure
   :class: tip

   A light gray AV facing right, its base link (white dot) at the origin,
   :math:`x` and :math:`y` in meters.

   - **Tag 1, solid:** five arcs forward, one per steering angle, from hard
     left to hard right.
   - **Tag 2, dashed:** the same five arcs in reverse.

   Each arc is drawn 3 m long and ends in a dot.

From a pose, the AV drives a short arc at one of 5 steering angles, forward
(tag 1) or in reverse (tag 2). The tightest arcs have the 3.41 m radius of
the Configuration Space section. The arcs are drawn 3 m long; the search
used 0.75 m.


.. _l9-lec-hybrid-steps13:

Hybrid A*, Steps 1 to 3: Expand a Pose and Check It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/hybrid_expand.png
   :alt: A zoomed top view of the garage near the top row of parked blue cars, x and y in meters. A pose in the aisle, tag 1 just below it with a short line up to it: a white dot with a dashed outline of the AV's body, heading up and to the right. Ten arcs leave it: five solid ones forward, five dashed ones in reverse, each ending in a point. Eight ends are gray dots. The two forward arcs that turn left end in rust crosses, tag 2; for the sharpest one, a rust dashed body outline and three rust circles reach into a parked car.
   :width: 55%
   :align: center

   One pose expanded: ten arcs, two of them dropped.

.. admonition:: Reading the figure
   :class: tip

   A part of the garage near the top row of parked cars, :math:`x` and
   :math:`y` in meters.

   - **Tag 1:** the pose being expanded, a white dot with a dashed outline
     of the AV's body, heading up and to the right. Five solid arcs leave it
     forward and five dashed arcs in reverse; eight of them end in gray
     dots.
   - **Tag 2:** the two forward arcs that turn left end in rust crosses. For
     the sharpest one, the rust dashed body outline and its three rust
     circles reach into a parked car.

1. Take the pose with the lowest cost so far plus estimated cost to go, as
   in A* (tag 1).
2. Drive the 10 arcs from it (5 steering angles, forward solid, reverse
   dashed), 0.75 m each.
3. Check each new pose with the three circles; drop the ones that hit an
   obstacle (a car or a wall), tag 2: two of the ten here.

The arcs are drawn 3 m long so they show. The pose is chosen for the
example.

.. tip::

   See "Hybrid A*'s Estimates" in :doc:`Going Further <l9_appendix>` for
   hybrid A*'s estimates of cost to go.


.. _l9-lec-hybrid-steps46:

Hybrid A*, Steps 4 to 6: Cells, Cost and the Goal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/hybrid_cells.png
   :alt: Two panels. Left, an example: a grid of 0.5 meter cells, two short arcs from two parent poses. The first ends in a white dot with a short heading arrow, tag 1, off the gray plus sign at its cell's center. The second ends in the same cell in a rust cross, tag 2. Right: the garage near the goal spot; the search's green path comes along the aisle, turns down, and a dashed green line runs straight from there up into the free spot, where a light gray AV stands backed in; a second light gray AV marks where the reverse starts, tag 3.
   :width: 90%
   :align: center

   One pose per cell, and the last move onto the goal.

.. admonition:: Reading the figure
   :class: tip

   **Left, an example:** a grid of 0.5 m cells, :math:`x` and :math:`y` in
   meters. Two short arcs leave two parent poses (black dots) and end in
   the same cell.

   - **Tag 1:** the first arc's end, a white dot with a short heading arrow.
     It is not at the cell's center, the gray plus sign.
   - **Tag 2:** the second arc's end, a rust cross, in the same cell.

   **Right, the garage near the goal spot:** the search's green path comes
   along the aisle and turns down.

   - **Tag 3:** a light gray AV where the reverse starts. A dashed green
     line runs from it straight up into the free spot, where a second light
     gray AV stands backed in.

4. Find the new pose's cell: 0.5 m by 0.5 m by 7.5° of heading. If the cell
   already holds a pose, drop the new one (tag 2); if not, store the
   **exact** pose (tag 1), not the cell's center.
5. Its cost: the length driven, doubled in reverse, plus 4 (as much as 4 m
   driven) for each change of direction (all chosen).
6. Near the goal, try to reverse straight onto the goal pose; if the circles
   say it is free, stop (tag 3).

.. important::

   The cells only keep the search from expanding the same place again. The
   path is made of the stored exact poses, so it has no jumps.


.. _l9-lec-hybrid-garage:

Hybrid A* in the Garage
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/garage_hybrid.png
   :alt: The garage top view, x and y in meters. Light gray dots fill most of the aisle: the poses the search expanded. A green line, tag 1 above it, leaves the AV at the left, rises gently, runs along the aisle and curves down to the right past the free spot. There a gray copy of the AV stands angled down to the right, tag 2: the switch to reverse. A dashed green line runs from it straight up into the free spot, where a gray copy of the AV stands backed in, tag 3.
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
     where a gray copy of the AV stands backed in.

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


.. _l9-lec-rrt-star:

RRT*: the Path Keeps Getting Shorter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two proved results (Karaman and Frazzoli, 2011; see :doc:`the References
page <l9_references>`):

- As plain RRT adds nodes, its path's length settles on a value above the
  shortest.
- With RRT*, the path's length tends to the shortest as the tree grows.

What RRT* adds to each new node:

1. **Choose a parent:** among the tree's nodes near it, connect it to the
   one that gives it the shortest path from the start, not just the nearest.
2. **Rewire:** for each nearby node, if going through the new node is
   shorter, change that node's parent.

.. important::

   RRT keeps the first path it finds. RRT* pays for a shorter path with more
   distance checks per node.


.. _l9-lec-rrt-words:

RRT and RRT* in Words
~~~~~~~~~~~~~~~~~~~~~

**RRT**, one try, as above, with the garage run's settings:

1. The random point is the goal itself 5 times in 100; a step is at most
   1.5 m.
2. A free step's new node keeps the node it grew from as its parent.
3. Once a new node is within 1.5 m of the goal, follow the parents back to
   the start.

**RRT\*** chooses a parent and rewires, as above, among the nodes within a
"nearby" radius that shrinks as the tree grows (Karaman and Frazzoli,
2011).

.. important::

   "Theorem 33 (Non-optimality of RRT) The RRT algorithm is not
   asymptotically optimal" (Karaman and Frazzoli, 2011).


.. _l9-lec-which:

Which Planner Where
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 26 30 44
   :header-rows: 1
   :class: compact-table

   * - **Where**
     - **Planner**
     - **Why**
   * - A route over the town (the route planner)
     - A* on the lane graph (GP4)
     - each node is a stretch of one lane; an edge joins two you can drive
       between (straight on, a turn, a lane change)
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

The script is in the course's Python repo, folder ``lecture9``. The ``rrt``
part grows the tree; ``--seed`` picks another random seed, and
``--goal-spot bottom2`` sends the tree to a free spot near the AV. The
``search`` part shows results only. We computed the grid search and hybrid
A* results in advance. GP4 asks you to write A* on the lane graph, not these
garage searches. No CARLA server to start: the script needs numpy and
matplotlib only. The commands are on :doc:`the Code page <l9_code>`.

.. admonition:: What to look at
   :class: hint

   1. In ``rrt``, drag the slider: where does the tree grow first?
   2. Try three seeds. Does the path change? Does it get any smoother?
   3. With ``--goal-spot bottom2``, a free spot near the AV, how many nodes
      does the tree need now?
   4. In ``search``, follow hybrid A*'s path: where does it switch to
      reverse?

.. dropdown:: Answers, from the script
   :class-container: sd-border-success

   2. The path changes with the seed, and no seed makes it smooth: every
      step is straight, so the heading jumps where two steps meet. Seed 4:
      16 steps, jumps up to 78.2°. Seed 7: 15 steps, up to 52.7°. Seed 1:
      16 steps, up to 72.3°.
   3. With seed 4, the tree reaches the goal after 8 tries, with 8 nodes,
      against 23 nodes for the free spot of the top row.
   4. At (25.9, 9.7) m, after 24.0 m forward: the AV stops once and backs
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

- Finish the three exercises (the spreadsheet, Nash and the Prisoner's
  Dilemma) and the three hands-on parts on :doc:`the Code page <l9_code>`.
- Read "The S Curve" in :doc:`Going Further <l9_appendix>`.


.. _l9-lec-picture:

Today in One Picture: from the Inputs to a Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The inputs are at the top left, the output at the top. The middle row is
the road planner (:ref:`Frenet Frame <l9-lec-frenet>`, :ref:`Sampling Paths
<l9-lec-sampling>`, :ref:`Collision Checking <l9-lec-collision>`); the
bottom row, the garage (:ref:`Garage Planners <l9-lec-garage>`) and the
idea every check uses (:ref:`Configuration Space <l9-lec-cspace>`).

.. figure:: /_static/images/L9/l9_pipeline.png
   :alt: A flowchart in three rows. Top row: a box of inputs (the route, from the route planner, L7; the AV's pose and speed; other cars and obstacles, as boxes; their predicted paths; the map), an arrow to the behavior layer, which picks the task, and further right the output: a path for the next 70 meters, every 0.5 seconds, with an arrow up to a box, controller (L10): steering, throttle, brake. A green dashed frame labeled local planner surrounds the two rows below; the behavior layer box is green too, and the inputs and output boxes are gray. Middle row, reached from the behavior layer on the road: Frenet frame (map to s and d), then sample 31 paths, then check (circles, turn limits), then score (keep the cheapest). Bottom row, reached from the behavior layer in the garage: search (hybrid A star, grid, RRT), and a dashed box, configuration space: the AV as a point x, y, theta, with dashed arrows to the check and to the search. Lines from the score and from the search join at the right and lead to the output.
   :width: 90%
   :align: center

   Today's planner, from the inputs to a path.

.. admonition:: Reading the figure
   :class: tip

   - **Top row:** the inputs (gray: the route, the AV's pose and speed,
     other cars and obstacles as boxes, their predicted paths, the map), an
     arrow to the behavior layer (green), which picks the task, and the
     output (gray): a path for the next 70 m, every 0.5 s. An arrow goes up
     from the output to the controller: steering, throttle, brake.
   - **Green dashed frame:** the local planner, around the two rows below.
   - **Middle row, on the road:** Frenet frame (map to :math:`(s, d)`),
     sample 31 paths, check (circles, turn limits), score (keep the
     cheapest).
   - **Bottom row, in the garage:** search (hybrid A*, grid, RRT), and the
     dashed configuration space box, the AV as a point
     :math:`(x, y, \theta)`, with dashed arrows to the check and to the
     search.
   - The lines from the score and from the search join at the right and
     lead to the output.


.. _l9-lec-learning:

Where Learning Fits in Today's Picture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every box in the picture above is designed by hand: we chose the
candidates, the weights, the circles and the state machine. Learning, a
model trained on data, enters in two places.

1. **The inputs.** The objects come from a detector, a neural network
   trained on labeled images, and the other cars' futures from a predictor
   that can be learned too.
2. **In place of the whole picture.** An end-to-end driver is one network
   from the sensors to the plan.

.. admonition:: Definition: End-to-end driving
   :class: note

   "We define end-to-end autonomous driving systems as fully differentiable
   programs that take raw sensor data as input and produce a plan and/or
   low-level control actions as output" (Chen et al., 2024; see :doc:`the
   References page <l9_references>`).

In 2024, Tesla said its FSD runs on end-to-end neural networks (Tesla,
2024). How such a driver is trained, and where it fails, comes in a later
lecture.


.. rubric:: Image credits

The vehicle icons in the figures on this page were created by Stone from the
`Noun Project <https://thenounproject.com>`_. The road is CARLA's Town03 map.
