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
   running examples are the lecture's: the AV passing the obstacle, a parked
   car, in its lane on Town03's road 67, and the AV parking in a garage.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Section**
     - **What it adds to the lecture**
   * - :ref:`l9-app-cspace`
     - The region the base link must avoid, worked for two boxes, and where
       it lies on our road.
   * - :ref:`l9-app-frenet`
     - A path's position, heading and curvature from :math:`(s, d)`.
   * - :ref:`l9-app-frenet-fails`
     - Tight turns, and what to do there.
   * - :ref:`l9-app-scurve`
     - How hard a candidate turns, by hand; the S curve's polynomial, and
       where 5.77 comes from.
   * - :ref:`l9-app-circles`
     - How the radius changes with the number of circles.
   * - :ref:`l9-app-mdp`
     - The lane change with a chance that the other car yields, and when the
       AV should go.
   * - :ref:`l9-app-hybrid`
     - The two estimates of cost to go, and the direct try at the goal, from
       Dolgov et al.

The sources for these sections are on :doc:`the References page
<l9_references>`.


.. _l9-app-cspace:

C-Space for Two Boxes
---------------------

This section continues "Step 1: Grow the Obstacle, for One AV Heading" and
"Step 2: the AV Becomes a Point" in the Configuration Space section of the
:doc:`lecture <l9_lecture>`.

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

.. _l9-app-cspace-road:

The Grown Obstacle on Our Road
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The obstacle's center is 60 + 58 = 118 m along the stretch and 0.3 m right of
the right lane's center. The region reaches 5.85 m behind it and 3.15 m ahead,
and 1.9 m to each side. So the base link must avoid:

- along the stretch: 118 − 5.85 = 112.15 m to 118 + 3.15 = 121.15 m;
- across: 0.3 + 1.9 = 2.2 m right to 1.9 − 0.3 = 1.6 m left of the right
  lane's center.

The left lane's center is 3.5 m left of the right lane's center: 3.5 − 1.6 =
1.9 m clear of the region. So a pose on the left lane's center, beside the
obstacle, is free.


.. _l9-app-frenet:

The Frenet Formulas
-------------------

This section continues "Back from (s, d) to the Map" in the Frenet Frame
section of the :doc:`lecture <l9_lecture>`. The next section, "Where the
Frenet Frame Fails", uses its formulas.

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

The sign of :math:`d` in Step 3, by hand: :math:`P - F` = (0.004, −0.300) m;
the piece :math:`AB` heads 0.705°, so its left direction is :math:`n` =
(−0.012, 1.000), and :math:`d = n \cdot (P - F)` = (−0.012)(0.004) +
(1.000)(−0.300) = −0.300 m.

In class, Step 3 used the direction of the piece :math:`AB` (0.705°). The
way back used the reference's heading at :math:`s` = 118 m, smoothed over
its neighbors (0.81°). The difference moves the point by
3.5 × sin 0.1° = 0.006 m.


.. _l9-app-frenet-fails:

Where the Frenet Frame Fails
----------------------------

This section continues "Where the Frenet Frame Leaves Us" at the end of the
Frenet Frame section of the :doc:`lecture <l9_lecture>`.

Where the Frenet Frame Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On a curve, the lines across the road (constant :math:`s`) all meet at the
curve's center.

.. figure:: /_static/images/L9/frenet_fails.png
   :alt: A tight left turn drawn to scale: a straight piece of the two lanes, the right lane pale yellow with the reference as a thick black line, the left lane pale purple, then a quarter circle turning left. Dashed lines cross the road every 2 meters of the reference: vertical and parallel on the straight, and on the curve all running to one black dot, the curve's center, tag 1. Three white circles sit on the reference, each on one of those lines, at the same distance from the center; past the road's edge, their labels read F, s = 2 m, F, s = 6 m and F, s = 10 m. An arrow labeled R = 8 m runs from the center down to the reference. An orange box on the inside of the left lane, near its inner edge, holds the part where the dashed lines are closest together; tag 2 points at it.
   :width: 70%
   :align: center

   A tight left turn in the Frenet frame.

.. admonition:: Reading the figure
   :class: tip

   A turn with :math:`R` = 8 m, chosen for the example, drawn to scale. The
   right lane is pale yellow, with the reference as a thick black line; the
   left lane is pale purple.

   - **Dashed lines:** a line across the road every 2 m of :math:`s`,
     counted from the start of the turn. On the straight they are parallel;
     on the curve they all run to one point.
   - **Tag 1:** the curve's center, 8 m from the reference (the arrow
     labeled :math:`R` = 8 m).
   - **White circles,** labeled :math:`F`: three points of the reference, at
     :math:`s` = 2, 6 and 10 m.
   - **Tag 2,** the orange box: the inside of the left lane, near its inner
     edge, where the dashed lines are closest together.

1. Tag 1 is the curve's center. Every point of the curved reference is
   :math:`R` from it, so every one of them is its foot point (its nearest
   point on the reference). The figure marks three of them as :math:`F`, at
   :math:`s` = 2, 6 and 10 m. The center's :math:`s` could be any of them,
   so the frame cannot place it.
2. Tag 2: closer to tag 1, the lines across crowd together. The formulas for
   a path's heading and curvature divide by their spacing, the factor
   :math:`1 - d/R`, written :math:`1 - \kappa d` with :math:`\kappa = 1/R`
   in :ref:`l9-app-frenet`. The factor shrinks to 0 at tag 1, and the
   formulas break.
3. On our road the paths stay far from the curves' centers, so the frame
   works everywhere.

.. admonition:: When the Frenet frame fails
   :class: important

   A tight turn with a path far to its inside, as at a junction.

.. _l9-app-frenet-fix:

On a Tight Turn: Change the Reference, or Drop It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Goal: keep :math:`1 - d/R` well above 0 where the road turns tightly.

.. figure:: /_static/images/L9/frenet_fix.png
   :alt: The tight left turn of the last figure, drawn twice side by side, to scale, with the curve's center as a black dot. Panel 1: the reference is a thick black line on the right lane's center; the AV's path, green, runs on the left lane's center; an arrow labeled d = 3.5 m goes across from the reference to the path in the middle of the turn. Panel 2: the reference, thick black, now runs on the left lane's center, and the green path lies on it, dashed over it; label d = 0.
   :width: 90%
   :align: center

   The same path with two references.

.. admonition:: Reading the figure
   :class: tip

   The turn of the last figure, :math:`R` = 8 m (chosen). The thick black
   line is the reference, the green line is the AV's path, and the dot is
   the curve's center.

   - **Tag 1:** the reference on the right lane's center; the path on the
     left lane's center, :math:`d` = 3.5 m from it.
   - **Tag 2:** the reference on the left lane's center; the path lies on
     it, :math:`d` = 0.

1. **Change the reference.** In tag 1, the reference is the right lane's
   center and the AV turns in the left lane, 3.5 m to the side:
   1 − 3.5 / 8 = 0.56, and it falls toward 0 as :math:`d` nears 8 m. In
   tag 2, the reference is the left lane's own center line (the map stores
   one for every lane), with radius 8 − 3.5 = 4.5 m. The same path is now at
   :math:`d` = 0: 1 − 0 / 4.5 = 1.
2. **Drop the reference.** Plan in :math:`(x, y, \theta)` directly, as the
   :ref:`garage planners <l9-lec-garage>` do. It works anywhere, but a lane
   is no longer a band of :math:`d`: the search must follow the road's shape
   itself.


.. _l9-app-scurve:

The S Curve
-----------

This section continues "Step 1: One Candidate, a Smooth Move Sideways" and
"Step 2: Drop Paths That Collide or Turn Too Hard" in the Sampling Paths
section of the :doc:`lecture <l9_lecture>`. The Next Class section asks you
to read it before the next lecture.

.. _l9-app-how-hard:

How Hard a Candidate Turns, by Hand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On a straight road, the sharpest bend of the S curve gives a sideways
acceleration of about

.. math::

   a \approx v^2 \times 5.77 \times \frac{\Delta d}{L^2}

with :math:`v` the speed, :math:`\Delta d` the sideways move and :math:`L`
the maneuver length. The 5.77 comes from the S curve's shape (next subsection).

With :math:`v` = 10 m/s and :math:`\Delta d` = 3.5 m:

1. :math:`L` = 20 m: 100 × 5.77 × 3.5 / 400 = 5.05 m/s². Over 3, so
   dropped.
2. :math:`L` = 30 m: 100 × 5.77 × 3.5 / 900 = 2.24 m/s².
3. :math:`L` = 40 m: 100 × 5.77 × 3.5 / 1600 = 1.26 m/s².

.. important::

   Twice the length, a quarter of the acceleration. The script measures the
   bend of each drawn path exactly and gets 4.91, 2.21 and 1.25 m/s². The
   formula leaves out the path's slope, which matters most for the steepest
   one.


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

This section continues "Cover the AV with Three Circles" and "Step 1: the
Radius and the Centers, by Hand" in the Collision Checking section of the
:doc:`lecture <l9_lecture>`.

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


.. _l9-app-mdp:

Behavior as an MDP
------------------

This section continues "Two Equilibria: the AV Goes First Only When It Is
Sure" and "FSM, Game and MDP: Three Tools That Work Together" in the Behavior
section of the :doc:`lecture <l9_lecture>`.

The Lane Change as a Markov Decision Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Markov decision process (MDP)
   :class: note

   States, actions, and, for each state and action, the chances of each next
   state and its reward. The next state depends only on the current state and
   action. "MDPs are a classical formalization of sequential decision making,
   where actions influence not just immediate rewards, but also subsequent
   situations, or states, and through those future rewards" (Sutton and
   Barto, 2018, p. 47; see :doc:`the References page <l9_references>`).

The game assumed the AV knows nothing about the other car. In an MDP,
prediction gives the chance :math:`p` that the other car yields. Costs are the
game's delays, in seconds (chosen).

1. Wait: 3, whatever the other car does.
2. Go: 0 if the car yields (chance :math:`p`), 100 if it keeps its speed
   (chance :math:`1 - p`). On average: 100 × (1 − :math:`p`).
3. Go costs less on average when 100 × (1 − :math:`p`) < 3, so when
   :math:`p` > 1 − 3 / 100 = 0.97.

So "go first only when sure" means: go only when prediction gives the yield
more than a 97 % chance. This counts one decision; a longer MDP also weighs
waiting a second to see.

The other driver's intent is a state the AV never sees, only its effects. An
MDP with such a state is a partially observable MDP (POMDP): the true state
"underlies and produces the environment's observations, but is never
available to the agent" (Sutton and Barto, 2018, p. 467).


.. _l9-app-hybrid:

Hybrid A*'s Estimates
---------------------

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
