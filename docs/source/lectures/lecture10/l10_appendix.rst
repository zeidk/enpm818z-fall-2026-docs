====================================================
Going Further
====================================================

.. admonition:: Reading material, not covered in class
   :class: note

   This page is the written version of the deck's appendix. It is **reading
   material**: we do not present it in class, and it is **not on the quiz**.

   Each section picks up a topic from the :doc:`lecture <l10_lecture>` and
   adds the math, the worked steps or the sources behind it. The sections
   follow the deck's order. Read the one you need, when you need it. The
   running example is the lecture's: one right turn in Town03, driven in a
   numpy simulation of the bicycle model.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Section**
     - **What it adds to the lecture**
   * - :ref:`l10-app-bicycle`
     - Why :math:`\tan\delta = L/R`, from the turning point's triangle, and
       where the model stops holding.
   * - :ref:`l10-app-quintic`
     - The quintic's six conditions, and the six equations for our
       slow-down, written out and solved.
   * - :ref:`l10-app-pp`
     - Why the arc through the goal point has curvature
       :math:`2\sin\alpha / L_d`.
   * - :ref:`l10-app-stanley`
     - One Stanley step by hand, which axle stays on the path, Pure Pursuit
       against Stanley, and why the cross-track term pulls the error to
       zero.
   * - :ref:`l10-app-mpc`
     - One MPC step on our turn, drawn, and the optimization problem written
       out.

The sources for these sections are on :doc:`the References page
<l10_references>`.


.. _l10-app-bicycle:

The Bicycle Model
-----------------

This section continues "Write the Model: the State, the Inputs and Four
Equations" and "Steer for a Curvature: a Fixed Angle Drives a Circle" in the
Bicycle Model section of the :doc:`lecture <l10_lecture>`.


.. _l10-app-bike:

Why tan δ = L/R
~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/bicycle_geom.png
   :alt: The bicycle model drawing again, with dark round tags: rear wheel at tag 1, front wheel at tag 2 turned by delta, the point the AV turns about at tag 3, the radius R from the rear wheel to that point, and the wheelbase L between the wheels.
   :width: 50%
   :align: center

   The bicycle model, from the lecture.

.. admonition:: Reading the figure
   :class: tip

   The same drawing as in the lecture. The thin gray lines are square to
   each wheel.

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
4. The triangle (tag 1, tag 2, tag 3) has a right angle at tag 1, the side
   :math:`L` along the body and the side :math:`R` to tag 3. Its angle at
   tag 3 is :math:`\delta`, so :math:`\tan\delta = L/R`.
5. The rear axle moves at :math:`v` on a circle of radius :math:`R`: it
   turns at :math:`v/R = v\tan\delta / L`, the model's third equation.


.. _l10-app-limits:

Where the Model Stops Holding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The model assumes the tires roll where they point. A real tire slides a
  little sideways when it carries a sideways force, and more as the force
  grows.
- So the model holds while the sideways acceleration :math:`v^2\kappa`
  stays small. Here we take the limit as half of gravity's pull, 0.5 g
  (chosen for this example): 0.5 × 9.81 = 4.9 m/s².
- Our profile caps it at 2.0 m/s²: on the second arc,
  :math:`3.46^2 \times 0.1673` = 2.0 m/s².
- Beyond that, the **dynamic** bicycle model adds the tire forces.


.. _l10-app-quintic:

The Quintic
-----------

This section continues "Change Speed With No Jump in Acceleration: a
Quintic" in the Trajectories section of the :doc:`lecture <l10_lecture>`.


.. _l10-app-quintic-six:

The Quintic: Six Conditions Fix Six Numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The distance along the path, written as a polynomial of degree five in time:

.. math::

   s(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5

Six unknowns, so six conditions: distance, speed and acceleration at the
start and at the end. The sampling planner's S curve is the same idea: a
quintic whose slope and bend are zero at both ends, there along the road,
here in time.

1. Start: :math:`s` = 0, :math:`v` = 8 m/s, :math:`a` = 0. End:
   :math:`s = D`, :math:`v` = 3.46 m/s, :math:`a` = 0.
2. Pick :math:`T`. Its largest deceleration is :math:`1.5\,\Delta v / T`;
   set that to 2.0: :math:`T = 1.5 \times 4.54 / 2.0` = 3.41 s, and
   :math:`D = \frac{8 + 3.46}{2} \times 3.41` = 19.5 m.
3. Solve the six equations: :math:`s(t) = 8t - 0.391\,t^3 + 0.0573\,t^4`
   (the other three coefficients come out 0).

.. important::

   Zero acceleration at both ends means no jump where the braking starts
   and ends. A **cubic** has four unknowns: it matches distance and speed,
   not acceleration. With :math:`T` = 2.27 s and :math:`D` = 13.0 m it
   gives :math:`s(t) = 8t - 1.0\,t^2`, the constant 2.0 m/s² again.


.. _l10-app-quintic-eq:

The Six Equations, for Our Slow-Down
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`s(t) = a_0 + a_1 t + \dots + a_5 t^5`, so :math:`v = \dot s` and
:math:`a = \ddot s`. With :math:`T` = 3.41 s and :math:`D` = 19.5 m:

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

1. The first three rows give :math:`a_0` = 0, :math:`a_1` = 8,
   :math:`a_2` = 0 at once.
2. The last three, solved: :math:`a_5` = 0, because :math:`D` is the
   average of the two speeds times :math:`T`. Then :math:`a(T) = 0` gives
   :math:`a_3 = -2a_4T`, and :math:`v(T) = 3.46` gives
   :math:`a_4 = 4.54 / (2 \times 3.41^3)` = 0.0573, so
   :math:`a_3 = -2 \times 0.0573 \times 3.41` = −0.391.
3. Then :math:`a(t) = 6a_3 t + 12 a_4 t^2` is largest in size at
   :math:`t = T/2`: :math:`1.5\,\Delta v / T = 1.5 \times 4.54 / 3.41` =
   2.0 m/s².


.. _l10-app-pp:

Pure Pursuit's Arc
------------------

This section continues "Step 3: Find the Angle α and the Arc Through the
Goal" in the Pure Pursuit section of the :doc:`lecture <l10_lecture>`.


.. _l10-app-pp-why:

Why κ = 2 sin α / L_d
~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pp_arc.png
   :alt: A geometry drawing with dark round tags. The rear axle at tag 1 with an arrow pointing right along the heading. A green arc leaves it tangent to the arrow and curves up to the goal point at tag 2. The arc's center, a green cross at tag 3, sits straight above the rear axle; gray lines of length R join it to the rear axle and to the goal. A blue chord of length L_d joins the rear axle to the goal. A red arc marks the angle alpha between the heading and the chord; a green arc at the center marks the angle 2 alpha. A dashed line from the center meets the chord at its middle.
   :width: 45%
   :align: center

   The arc from the rear axle through the goal point.

.. admonition:: Reading the figure
   :class: tip

   The drawing uses :math:`\alpha` = 35°, chosen for the drawing. The arrow
   from tag 1 is the AV's heading; the green curve is the arc.

   - **Tag 1:** the rear axle.
   - **Tag 2:** the goal point. The blue chord from tag 1 to tag 2 has
     length :math:`L_d`; it makes the angle :math:`\alpha` (red) with the
     heading.
   - **Tag 3:** the arc's center. The gray lines from it to tag 1 and to
     tag 2 both have length :math:`R`; the angle between them is
     :math:`2\alpha` (green). The dashed line from it meets the chord at its
     middle.

1. The arc starts along the heading, so its center (tag 3) is square to the
   heading from the rear axle (tag 1), at distance :math:`R`.
2. The goal (tag 2) is on the arc: the center is :math:`R` from it too. The
   triangle (tag 1, tag 2, tag 3) has two sides :math:`R`.
3. The angle between the heading and the chord is :math:`\alpha`, so the
   chord makes :math:`90^\circ - \alpha` with the side from tag 1 to tag 3.
   The triangle's angle at tag 3 is then
   :math:`180^\circ - 2(90^\circ - \alpha) = 2\alpha`.
4. The dashed line splits it into two right triangles with half the chord:
   :math:`L_d / 2 = R \sin\alpha`. So :math:`R = L_d / (2\sin\alpha)` and
   :math:`\kappa = 2\sin\alpha/L_d`.
5. With :math:`\sin\alpha = g_y / L_d`: :math:`\kappa = 2 g_y / L_d^2`,
   Coulter's form (Coulter, 1992). Our example:
   2 × (−0.933) / 25 = −0.0746 /m, as before.


.. _l10-app-stanley:

Stanley
-------

This section continues "Steer from the Front Axle: Stanley's Heading and
Cross-Track Terms" in the Stanley section of the :doc:`lecture
<l10_lecture>`.


.. _l10-app-stanley-step:

One Stanley Step by Hand, at the Same Moment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AV as in Pure Pursuit's example: rear axle (82.69, −0.03) m,
:math:`\theta` = −2.54°, :math:`v` = 5.22 m/s. Gain :math:`k` = 1
(chosen).

1. Front axle: :math:`L` = 2.875 m ahead along the heading:
   (85.56, −0.15) m.
2. Nearest path point: the path there points at −15.97°. Heading error:
   :math:`\psi_e` = −15.97° − (−2.54°) = −13.43° = −0.234 rad.
3. Cross-track error: the front axle is 0.212 m **left** of the path, so
   :math:`e` = +0.212 m.
4. Cross-track term:
   :math:`-\arctan\frac{1 \times 0.212}{5.22 + 1} = -\arctan(0.034)` =
   −0.034 rad (−2.0°), toward the path, to the right.
5. :math:`\delta` = −0.234 − 0.034 = −0.268 rad (−15.4°), to the right.

.. important::

   Pure Pursuit at the same moment: −0.211 rad. Stanley steers harder here:
   it measures the heading error at the front axle, where the path has
   already turned.


.. _l10-app-axles:

Which Point of the AV Stays on the Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/axle_paths.png
   :alt: Two top views of the corner side by side, the AV drawn faintly in the second arc in each. Left, dark tag 1, Pure Pursuit with a 5 meter lookahead in blue: the solid line, the rear axle, follows the dashed lane center; the dotted line, the front axle, swings outside it through the corner. Right, tag 2, Stanley with gain 1 in purple: the dotted front axle line follows the lane center; the solid rear axle line runs inside the corner.
   :width: 90%
   :align: center

   The rear and front axles' paths, for Pure Pursuit and for Stanley.

.. admonition:: Reading the figure
   :class: tip

   Two top views of the corner, in meters, with the AV drawn faintly in the
   second arc. Solid lines are the rear axle, dotted lines the front axle;
   the gray dashed line is the lane center.

   - **Tag 1 (blue):** Pure Pursuit, :math:`L_d` = 5 m.
   - **Tag 2 (purple):** Stanley, :math:`k` = 1.

Pure Pursuit holds the **rear** axle on the path; the front swings out by up
to 0.67 m. Stanley holds the **front** axle (within 0.38 m); the rear cuts
in by up to 0.45 m. On the 5.98 m arc, with the rear axle on it, the front
axle is :math:`\sqrt{5.98^2 + 2.875^2} - 5.98` = 0.66 m outside: the axles,
2.875 m apart, cannot both be on the path.


.. _l10-app-pp-vs-stanley:

Pure Pursuit Against Stanley on Our Turn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
  Lookahead for Every Speed" in the lecture.
- Stanley's gain plays the role of a short lookahead: too high, and with our
  steering lag the AV weaves.


.. _l10-app-stanley-converge:

Why the Cross-Track Term Pulls e to Zero
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Take a straight path and an AV already parallel to it
(:math:`\psi_e` = 0), its front axle :math:`e > 0` to the left (leave out
:math:`k_s`). Stanley steers by :math:`\delta = -\arctan(k e / v)`, to the
right, so the front axle moves at speed :math:`v` at the angle
:math:`\delta` toward the path:

1. Sideways speed:
   :math:`\dot e = v\sin\delta = -v \sin\big(\arctan(k e / v)\big)`, as
   Thrun et al. write it (Thrun et al., 2006).
2. Small :math:`e`: :math:`\sin(\arctan z) \approx z`, so
   :math:`\dot e \approx -k\,e`. The error shrinks by the same fraction
   every second: :math:`e(t) = e(0)\,e^{-kt}`.
3. With :math:`k` = 1 /s: after 1 s, :math:`e^{-1}` = 0.37 of the error is
   left; after 3 s, 0.05.
4. Large :math:`e`: :math:`\arctan` stays below 90°, so the AV turns toward
   the path at most square to it, then the term shrinks as :math:`e` does.

.. important::

   The real AV adds what this leaves out: the steering's delay and lag, and
   its 0.7 rad limit. That is why :math:`k` = 4 weaves in our runs.


.. _l10-app-mpc:

MPC
---

This section continues "Plan Ahead with MPC: Predict, Score, Apply the First
Input, Repeat" in the MPC section of the :doc:`lecture <l10_lecture>`.


.. _l10-app-mpc-step:

One MPC Step on Our Turn, Drawn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/mpc_candidates.png
   :alt: A top view of a right turn, x from 68 to 100 meters and y from minus 26 to 6. The lane comes in from the left along y = 0 and turns down; solid lines mark its edges and a dashed gray line its center. The AV is drawn faintly at about x = 78, with a dark dot at its rear axle. A fan of hundreds of thin gray curves leaves the rear axle: a few bend left, up to y = 6.6, and most bend right, down to y = minus 12.7; tag 4 sits at the fan's lower-left end. One thick green curve runs along the lane center past a green dot (tag 1, joined by a thin line from above the lane), bends right past a second green dot (tag 2) and ends inside the turn, at about x = 90.6 and y = minus 3.5, joined by a thin line to tag 3 to the right of the lane. All tags are dark circles.
   :width: 70%
   :align: center

   The candidate steering sequences and the best one.

.. admonition:: Reading the figure
   :class: tip

   A top view of the corner, in meters, 2 m before the turn, at 7.09 m/s.
   The AV is drawn faintly; the dark dot is its rear axle.

   - **Tag 4 (gray):** every sequence of three steering angles, each from
     −0.6 to 0.2 rad in steps of 0.1 and held 1 s: :math:`9^3` = 729
     sequences, each predicted 3 s (60 steps) with the bicycle model.
   - **Tags 1 to 3 (green):** the best sequence, at 1, 2 and 3 s: 0, then
     −0.4, then 0 rad.

- Score: the squared distance from the path, added over the 60 steps, plus
  the squared steering angles.
- Apply only 0 rad for 0.05 s, then plan again.

A simplification for the picture: a real MPC finds the sequence with an
optimizer, not by trying a list.


.. _l10-app-mpc-problem:

The Problem Written Out
~~~~~~~~~~~~~~~~~~~~~~~

At step :math:`k`, with the measured state :math:`\mathbf{x}_0` (the AV's
:math:`x, y, \theta, v`) and horizon :math:`N`:

.. math::

   \min_{\delta_0, \dots, \delta_{N-1}} \; \sum_{i=1}^{N} e_i^2\,\Delta t
   \;+\; w \sum_{i=0}^{N-1} \delta_i^2
   \quad \text{subject to} \quad
   \mathbf{x}_{i+1} = f(\mathbf{x}_i, \delta_i), \quad |\delta_i| \le 0.7

- :math:`f`: one step of the bicycle model; :math:`e_i`: the predicted
  cross-track error after step :math:`i`; :math:`w`: a weight (chosen) that
  trades steering effort against error.
- The solution is a whole sequence; only :math:`\delta_0` is applied.
- Our picture: :math:`N` = 60 steps of 0.05 s, :math:`w` = 1, and
  :math:`\delta_i` held for 20 steps at a time, from 9 values, so the 729
  sequences could simply be tried. In the steering term each held angle
  counts once: :math:`0^2 + 0.4^2 + 0^2` = 0.16. The best scored 0.186:
  0.026 from the error, 0.16 from the steering.
- Autoware's MPC is linear (Autoware Foundation, MPC lateral controller):
  with :math:`f` linearized around the path and this squared score, each
  step is a quadratic program, which solvers handle fast.


.. rubric:: Image credits

The vehicle icon in the figures on this page was created by Stone from the
`Noun Project <https://thenounproject.com>`_. The map is CARLA's Town03
(`carla.org <https://carla.org>`_).
