====================================================
Going Further
====================================================

.. admonition:: Reading material, not covered in class
   :class: note

   This page is the written version of the deck's appendix. It is **reading
   material**: we do not present it in class, and it is **not on the quiz**.

   Each section picks up a topic from the :doc:`lecture <l9_lecture>` and
   adds the math, the worked steps or the sources behind it. The sections
   follow the deck's order. Read the one you need, when you need it. The
   running examples are the lecture's: the AV passing a car parked in its
   lane on Town03's road 67, and the AV parking in a garage.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Section**
     - **What it adds to the lecture**
   * - :ref:`l9-app-cspace`
     - The region the base link must avoid, worked for two boxes.
   * - :ref:`l9-app-frenet`
     - A path's position, heading and curvature from :math:`(s, d)`.
   * - :ref:`l9-app-scurve`
     - The S curve's polynomial, and where 5.77 comes from.
   * - :ref:`l9-app-circles`
     - How the radius changes with the number of circles.
   * - :ref:`l9-app-grid`
     - Grid search on a small grid, step by step.
   * - :ref:`l9-app-hybrid`
     - Hybrid A*'s estimates of cost to go, and the direct try at the goal.
   * - :ref:`l9-app-rrt`
     - RRT's goal test and settings, and why RRT is not optimal.

The sources for these sections are on :doc:`the References page
<l9_references>`.


.. _l9-app-cspace:

C-Space for Two Boxes
---------------------

This section continues "Step 1: Grow the Parked Car, for One AV Heading" in
the Configuration Space section of the :doc:`lecture <l9_lecture>`.

The Region the Base Link Must Avoid, in General
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fix one heading :math:`\theta` and place the AV's base link at a point
:math:`p`. If the AV's body then overlaps the obstacle :math:`\mathcal{O}`,
the base link must avoid :math:`p`. The set of such :math:`p` is
:math:`\mathcal{O}` grown by the AV's shape turned 180° about the base link,
a **Minkowski sum**. LaValle (2006) derives it for a robot that only
translates (Section 4.3.2).

**Two boxes with the same heading.** Measure along the obstacle, positive the
way both face, and across it.

- Obstacle: length :math:`l_o`, width :math:`w_o`, centered at 0.
- AV: front :math:`f` ahead of the base link, rear :math:`b` behind it,
  width :math:`w`.
- Region along: from :math:`-(l_o/2 + f)` to :math:`+(l_o/2 + b)`.
  Across: from :math:`-(w_o + w)/2` to :math:`+(w_o + w)/2`.

Ours: :math:`l_o` = 4.5, :math:`w_o = w` = 1.9, :math:`f` = 3.6,
:math:`b` = 0.9. So the region runs along from −5.85 to +3.15 m, and across
from −1.9 to +1.9 m.

For another heading the region is no longer a box (the dashed outline in
"The Region Changes with the Heading"), so the class sections check circles
instead.


.. _l9-app-frenet:

The Frenet Formulas
-------------------

This section continues "Back from (s, d) to the Map" and "Where the Frenet
Frame Fails" in the Frenet Frame section of the :doc:`lecture <l9_lecture>`.

Position, Heading and Curvature of a Path in (s, d)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The reference has, at each :math:`s`, a point :math:`r(s)`, a heading
:math:`\theta_r(s)`, a curvature :math:`\kappa(s)`, and a left direction
:math:`n(s) = (-\sin\theta_r, \cos\theta_r)`. A path is given by
:math:`d(s)`. :math:`d'` is the change of :math:`d` per meter of :math:`s`,
and :math:`d''` the change of :math:`d'`.

1. Position: :math:`p(s) = r(s) + d(s)\,n(s)`.
2. Heading: :math:`\theta = \theta_r + \operatorname{atan2}(d',\ 1 - \kappa d)`.
3. Curvature, with :math:`\kappa` taken as constant over a short piece (from
   :math:`p'` and :math:`p''`; ``tests/test_l9common.py`` in the hands-on
   folder checks it against the drawn points):

.. math::

   \kappa_p = \frac{\kappa (1 - \kappa d)^2 + (1 - \kappa d)\, d'' + 2 \kappa\, d'^2}
                   {\big((1 - \kappa d)^2 + d'^2\big)^{3/2}}

Two special cases:

- Constant :math:`d`: :math:`\kappa_p = \kappa / (1 - \kappa d)`, a circle
  of radius :math:`R - d`, with :math:`R = 1/\kappa`.
- Straight reference (:math:`\kappa` = 0):
  :math:`\kappa_p = d'' / (1 + d'^2)^{3/2}`.

In class, Step 3 used the direction of the piece :math:`AB` (0.705°). The
way back used the reference's heading at :math:`s` = 118 m, smoothed over
its neighbors (0.81°). The difference moves the point by
3.5 × sin 0.1° = 0.006 m.


.. _l9-app-scurve:

The S Curve
-----------

This section continues "Step 1: One Candidate, a Smooth Move Sideways" and
"How Hard a Candidate Turns, by Hand" in the Sampling Paths section of the
:doc:`lecture <l9_lecture>`.

The S Curve and Where 5.77 Comes From
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let :math:`u = (s - s_0)/L` run from 0 to 1 over the maneuver, with
:math:`s_0` where it starts and :math:`L` its length. Then
:math:`d(s) = d_0 + \Delta d\, q(u)`, where

.. math::

   q(u) = 10u^3 - 15u^4 + 6u^5

1. :math:`q(0) = 0` and :math:`q(1) = 1`. Its slope
   :math:`q'(u) = 30u^2(1 - u)^2` and its bend
   :math:`q''(u) = 60u - 180u^2 + 120u^3` are 0 at both ends: the curve
   starts and ends flat, with no bend.
2. It is steepest at :math:`u` = 0.5: :math:`q'` = 30 / 16 = 1.875, so
   :math:`d'_\text{max} = 1.875\,\Delta d/L`. For candidate A (3.5 m over
   40 m): 1.875 × 3.5 / 40 = 0.164.
3. It bends most where :math:`q''' = 60 - 360u + 360u^2 = 0`:
   :math:`u = (3 - \sqrt{3})/6` = 0.211, where :math:`q'' = 10/\sqrt{3}` =
   5.77. So :math:`d''_\text{max} = 5.77\,\Delta d / L^2`. On a straight
   road the curvature is about :math:`d''`, and :math:`a = v^2 \times`
   curvature.
4. The exact curvature is :math:`d'' / (1 + d'^2)^{3/2}`. For :math:`L` =
   20 m at 10 m/s, the estimate is
   :math:`a \approx` 10² × 5.77 × 3.5 / 400 = 5.05 m/s². At :math:`u` =
   0.211, :math:`d'` = 30 × 0.211² × 0.789² × 3.5 / 20 = 0.146, so the exact
   value is 5.05 / (1 + 0.146²)^(3/2) = 5.05 / 1.032 = 4.89. The script's
   maximum over the whole curve is 4.91.

When the AV plans again in the middle of a move, it already has a slope and
a bend. The code then fits a fifth-degree polynomial to :math:`d`,
:math:`d'` and :math:`d''` at both ends: six conditions, six coefficients.


.. _l9-app-circles:

More or Fewer Circles
---------------------

This section continues "Step 1: the Radius and the Centers, by Hand" in the
Collision Checking section of the :doc:`lecture <l9_lecture>`.

The Radius for n Circles, and What Each Circle Costs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cut the :math:`l` by :math:`w` body into :math:`n` equal pieces. One circle
per piece reaches its corners:

.. math::

   r(n) = \sqrt{\Big(\frac{l}{2n}\Big)^2 + \Big(\frac{w}{2}\Big)^2}

For our AV, :math:`l` = 4.5 m and :math:`w` = 1.9 m:

.. list-table::
   :widths: 16 22 31 31
   :header-rows: 1
   :class: compact-table

   * - **Circles**
     - **Radius** :math:`r`
     - **Past each side,** :math:`r` **− 0.95**
     - **Distances per pose,** :math:`n \times n`
   * - 1
     - 2.442 m
     - 1.492 m
     - 1
   * - 2
     - 1.472 m
     - 0.522 m
     - 4
   * - 3
     - 1.210 m
     - 0.260 m
     - 9
   * - 4
     - 1.104 m
     - 0.154 m
     - 16

One circle would make the AV 4.9 m wide. Going from 3 to 4 circles saves
0.106 m per side for 7 more distances.


.. _l9-app-grid:

Grid Search by Hand
-------------------

This section continues "Grid Search on the Whole Garage" in the Garage
Planners section of the :doc:`lecture <l9_lecture>`.

Grid Search, Step 1: Count the Steps from the Start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L9/toy_wavefront.png
   :alt: A grid of 5 rows and 7 columns. Blue cells are parked cars: the top two rows except the fourth column, and the bottom row except the third and fourth columns. White cells hold numbers. Tag 1 marks the start cell, row 4 at the left, holding a bold 0. Its row reads 0 to 6 from left to right; the row above reads 1 to 7. The bottom row's free cells read 3 and 4. The fourth column above reads 5, then a bold 6 at the top: the goal, tag 2.
   :width: 55%
   :align: center

   The number of steps from the start, in every free cell.

.. admonition:: Reading the figure
   :class: tip

   A grid of 5 rows and 7 columns. Blue cells are taken by parked cars;
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

4. From the goal (6), step to a neighbor holding 5, then 4, and so on down
   to 0. Where two neighbors tie, either one gives a 6-step path.
5. Read it forward: right 3 cells, then up 3 cells.

.. important::

   The path turns 90° inside one cell. A cell has no heading, so the search
   does not know that the AV cannot turn on the spot.


.. _l9-app-hybrid:

Hybrid A*
---------

This section continues "Hybrid A*, Steps 1 to 3: Expand a Pose and Check It"
in the Garage Planners section of the :doc:`lecture <l9_lecture>`.

The Estimates of Cost to Go, and the Direct Try at the Goal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dolgov et al. (2008): "Our search algorithm is guided by two heuristics".

1. The first "ignores obstacles but takes into account the non-holonomic
   nature of the car": the shortest drive to the goal pose on an empty
   floor, never sideways.
2. The second "ignores the non-holonomic nature of the car, but uses the
   obstacle map to compute the shortest distance to the goal by performing
   dynamic programming in 2D".
3. "Both heuristics are mathematically admissible in the A* sense, so the
   maximum of the two can be used": neither estimate is ever more than the
   true cost.
4. Near the goal: "we augment the search with analytic expansions based on
   the Reed-Shepp model" (Reeds and Shepp, 1990): the shortest curve to the
   goal pose, forward and backward, tried as one piece.

**The course's version** uses the larger of two estimates: the straight-line
distance, and a 2-D grid distance around the cars. It tries a straight
reverse onto the goal instead of Reeds and Shepp's curves. On an 8-neighbor
grid the second estimate can be a little long, so the path found is not
guaranteed shortest.

Settings: 0.75 m arcs, 5 steering angles, cells of 0.5 m and 7.5°; reverse
length counts double, plus 4 per change of direction.


.. _l9-app-rrt:

RRT and RRT*
------------

This section continues "RRT*: the Path Keeps Getting Shorter" in the Garage
Planners section of the :doc:`lecture <l9_lecture>`.

RRT and RRT* in Words
~~~~~~~~~~~~~~~~~~~~~

**RRT**, one try, as in class, with the garage run's settings:

1. The random point is the goal itself 5 times in 100; a step is at most
   1.5 m.
2. A free step's new node keeps the node it grew from as its parent.
3. Once a new node is within 1.5 m of the goal, follow the parents back to
   the start.

**RRT\*** chooses a parent and rewires, as in class, among the nodes within a
"nearby" radius that shrinks as the tree grows (Karaman and Frazzoli, 2011).

.. important::

   "Theorem 33 (Non-optimality of RRT) The RRT algorithm is not
   asymptotically optimal" (Karaman and Frazzoli, 2011).
