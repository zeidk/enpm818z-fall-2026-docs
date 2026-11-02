====================================================
Nonlinear Filters: EKF, UKF and Particle Filter
====================================================

.. admonition:: Read this before you start GP3 Task 2
   :class: important

   This page is **reading material** for :doc:`GP3 </assignments/gp3>`.
   Task 2 asks you to build an extended Kalman filter (EKF). This page
   teaches the EKF one step at a time, then two other filters for the cases
   where the EKF fails: the unscented Kalman filter (UKF) and the particle
   filter.

**What you need first.** The linear Kalman filter from
:doc:`Lecture 3 </lectures/lecture3/l3_lecture>`. This page uses its
symbols:

- :math:`\hat{\mathbf{x}}` is the **estimate**: the filter's best guess of
  the state. :math:`P` is its **covariance**: how unsure the filter is.
- **Predict** moves both forward one time step:
  :math:`\hat{\mathbf{x}}^{-} = F\hat{\mathbf{x}} + B\mathbf{u}` and
  :math:`P^{-} = FPF^\top + Q`. :math:`F` is the motion model, :math:`B`
  carries the control input :math:`\mathbf{u}` into the state, and
  :math:`Q` is the noise the motion adds. The minus sign marks a
  **prediction**: the state before the next reading.
- **Update** corrects the prediction with a reading :math:`\mathbf{z}`.
  :math:`H` is the measurement model: the reading the sensor should give
  for a state. The **surprise** (innovation) is
  :math:`\boldsymbol{\nu} = \mathbf{z} - H\hat{\mathbf{x}}^{-}`. :math:`S
  = HP^{-}H^\top + R` is how big the filter expects the surprise to be, with
  :math:`R` the sensor noise. The **gain** :math:`K = P^{-}H^\top S^{-1}`
  says how far to move toward the reading.

Every number on this page comes from that lecture's slides and their
hands-on scripts, or from arithmetic shown next to it. Values chosen for an example say so where they appear.


Where the Kalman Filter Breaks
==============================

The Kalman filter rests on four assumptions. On a real AV all four break.
Two of them have an alternative filter:

.. list-table::
   :widths: 55 45
   :header-rows: 1
   :class: compact-table

   * - What breaks
     - The alternative
   * - The model is not linear.
     - The **EKF**
   * - The uncertainty is wide on a curve, or the model is only code.
     - The **UKF**
   * - The belief has more than one peak.
     - The **particle filter**

The other two have no filter of their own. Bias, an error that stays, is
covered by making :math:`Q` bigger. Knowing :math:`Q` and :math:`R` has a
**test** instead, in `Checking a Filter: NIS`_ near the end of this page.


Matrices can only scale and add
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Kalman filter runs on matrices. A matrix does two things: it **scales**
numbers and **adds** them. That is enough for a straight-line model, and
not for an AV that turns.

.. figure:: /_static/images/L3/ekf_story_1_matrix.png
   :alt: Three plots. Tag 1: three straight lines through the origin, output against input from minus 2 to 2, with slopes 2, 0.5 and minus 1. Tag 2: an arch, x in meters against heading theta from minus 90 to 90 degrees, highest at 20 meters for theta 0 and 0 at both ends. Tag 3: a curve, range r in meters against AV position x from 0 to 30 meters, starting near 22.4 meters, lowest at 10 meters for x 20, and rising again to about 14 meters at x 30.
   :align: center
   :width: 100%
   :class: white-figure

   **1** A matrix: times 2, times 0.5, times minus 1. Every output is a
   straight line. **2** Turning: driving 20 m at heading :math:`\theta`
   moves the AV :math:`x = 20\cos\theta` east, an arch. **3** The range to
   a sign 10 m off the road, beside :math:`x = 20`:
   :math:`r = \sqrt{(20 - x)^2 + 10^2}`, a curve.

No fixed matrix times the state gives a cosine or a square root of the
state. So the plain Kalman filter breaks the moment the AV turns, or a
camera measures a range.


A straight line keeps a bell curve a bell curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AV is on a road that runs at :math:`30^\circ` from east. Its heading is
**known**, :math:`30^\circ`. The distance it drives is not: :math:`d = 20
\pm 1` m. You track :math:`x`, how far east it gets.

.. figure:: /_static/images/L3/bell_1_line.png
   :alt: A bell curve pushed through a straight line. Bottom: the input, distance driven d in meters from 16 to 24, a gray bell curve centered on 20. Top right: a straight line labeled d cos 30 degrees and "A straight line". Top left: the output, distance along x in meters, a blue bell curve centered near 17.3. A dotted guide runs from 20 up to the line and across to the output's peak. Readout: in: bell curve; out: bell curve, 17.32 m plus or minus 0.87 m.
   :align: center
   :width: 60%
   :class: white-figure

   **Bottom:** the input, the distance driven. **Top right:** the function,
   :math:`x = d\cos 30^\circ`, a straight line in :math:`d`. **Top left:**
   the output, still a bell curve.

The numbers, in two steps:

1. The mean: :math:`20 \times \cos 30^\circ = 20 \times 0.866 = 17.32` m.
2. The spread: :math:`1 \times 0.866 = 0.87` m.

Through a straight line, a bell curve stays a bell curve, and
:math:`FPF^\top` gives its width exactly. That is why the Kalman filter
works.


A curve bends a bell curve out of shape
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same road, the other way round. The distance is **known**, 20 m. The
heading is not: :math:`30^\circ \pm 12^\circ`. The :math:`12^\circ` is a
value chosen for this example, large enough to show the effect.

.. figure:: /_static/images/L3/bell_2_curve.png
   :alt: A bell curve pushed through a curve. Bottom: the input, heading theta in degrees from about minus 10 to 70, a gray bell curve centered on 30. Top right: the curve 20 cos theta, highest at 20 meters at 0 degrees and falling to about 7 meters at 70 degrees, labeled "A curve". Top left: the output, a gray histogram that is lopsided: it piles up just under 20 meters and has a long tail down to about 8 meters. A solid line marks its mean, just below a dotted guide at 17.32 meters. Readout: out: lopsided, not a bell; mean 16.95 m; at 30 degrees: 17.32 m.
   :align: center
   :width: 60%
   :class: white-figure

   **Bottom:** the input, the heading. **Top right:** the function,
   :math:`x = 20\cos\theta`, a curve. **Top left:** the output, lopsided.
   Solid line: its mean, 16.95 m. Dotted line: the curve at
   :math:`30^\circ`, 17.32 m.

The output is not a bell curve. It piles up just under 20 m, because no
heading takes the AV farther east than 20 m, and it has a long tail below.
Its mean is **16.95 m**, not 17.32 m. The mean of the output is not the
curve at the mean of the input.

So the problem has two parts:

- Moving the **estimate** through a curve is easy: call the function once.
- Moving the **uncertainty** :math:`P` through a curve has no formula.

The three filters on this page are three ways around the second part.


The Extended Kalman Filter (EKF)
================================

.. admonition:: Definition: extended Kalman filter (EKF)
   :class: note

   A Kalman filter for models that are curves, not straight lines. At every
   step it replaces each curve by its **tangent at the estimate**, then runs
   the ordinary Kalman equations.

A **tangent** is the straight line that touches a curve at one point and
has the same slope there.


The trick: a straight line, one step at a time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the current estimate, draw the tangent. For the next step, use the
tangent in place of the curve. At the next step, draw a new tangent at the
new estimate.

.. figure:: /_static/images/L3/ekf_story_2_steps.png
   :alt: The range to the sign in meters against the AV position x in meters, 0 to 24. Tag 1: the real curve, dark, falling from about 22.4 meters and lowest near 10 meters at x 20. Tag 2: a blue dot on the curve at x 4. Two more blue dots on the curve at x 9 and x 14. Three short thick orange segments lie along the curve, one through each dot; tag 3 points at the one at x 9. Tag 4: a dashed orange line, the tangent from x 4 extended, which falls well below the curve after about x 14 and reaches about 6 meters near x 19.
   :align: center
   :width: 85%
   :class: white-figure

   **1** The real curve, the range to a sign. **2** The estimate at step
   :math:`k`. **3** The tangent there: for one step, the EKF uses this
   short straight line as the curve. Each step draws a new one. **4** Far
   from where it touches, a tangent is wrong.

Near the point where it touches, the tangent and the curve are almost the
same. In the EKF hands-on, the AV drives a bend of 60 m radius at 10 m/s.
It turns :math:`10 / 60 = 0.167` rad/s, so in one 0.1 s step it turns
:math:`0.167 \times 0.1 = 0.0167` rad, or :math:`0.95^\circ`. Over one step
the curve is almost straight.


A worked example: the range to one landmark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example has one number in the state, so you can follow every step by
hand.

.. figure:: /_static/images/L3/range_example.png
   :alt: The road seen from above, with an x axis along the bottom marked 0, 10, 16 and 20 meters. A landmark, a dark square, stands 10 meters off the road beside x 20. The AV drives right; the middle of its rear axle, a white dot, is at x 16. A thick black line from the dot to the landmark is labeled range h of x. Above the road, a green marker at 15.5 is labeled run 1, x hat equals 15.5, and an orange marker at 10 is labeled run 2, x hat equals 10. Below the road, a blue two-headed arrow from 0 to 16 is labeled x, and a gray one from 16 to 20 is labeled 20 minus x.
   :align: center
   :width: 70%
   :class: white-figure

   The road from above. :math:`x` is the AV's position along the road. The
   landmark stands 10 m off the road, beside :math:`x = 20` m.

- :math:`x` is the **AV's position along the road**, in meters. The AV
  drives right, toward the landmark.
- The camera measures the **range**: the straight-line distance from the
  AV to the landmark. The AV, the landmark and the spot on the road beside
  the landmark make a right triangle. Its legs are :math:`20 - x` along the
  road and 10 across. The range is the long side:

  .. math::

     h(x) = \sqrt{(20 - x)^2 + 10^2}

- The AV is **really** at :math:`x = 16` m, 4 m before the landmark. So the
  camera reads :math:`\sqrt{4^2 + 10^2} = \sqrt{116} = 10.77` m.
- The filter does not know where the AV really is. It keeps one estimate,
  :math:`\hat{x}`. The example runs twice, as two separate runs: **run 1**
  with :math:`\hat{x} = 15.5` m (a good estimate) and **run 2** with
  :math:`\hat{x} = 10` m (a poor one). Same AV, same reading; only the
  estimate changes.


The range curve has no single slope
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The next figure has two panels. The left one is the road from above. The
right one is **not** the road: it is a graph of the range the camera would
report at each position :math:`x`.

.. figure:: /_static/images/L3/ekf_linearize_0_curve.png
   :alt: Two panels. Left: the road from above, to scale. Tag 6: a black square, the landmark, above the road. Lines of sight run to it from four positions on the road, each labeled with its range: from 4 meters, 18.87 meters, at 32 degrees off the road; from 10 meters, 14.14 meters; from 16 meters, where a faint AV is drawn, 10.77 meters; from 19 meters, 10.05 meters, at 84 degrees off the road. Right: the range to the landmark in meters against the AV's position along the road x, from 4 to 20 meters. Tag 1: the curve, falling and flattening toward 10 meters at x 20. Tags 4, 2, 3 and 5: the four positions on the curve, at 4, 10, 16 and 19 meters, with dotted lines to both axes.
   :align: center
   :width: 100%
   :class: white-figure

   **1** The range :math:`h(x)`. **2** The AV at 10 m: 14.14 m. **3** At
   16 m: 10.77 m. **4** At 4 m: 18.87 m. **5** At 19 m: 10.05 m. **6** The
   landmark.

As the AV drives right, the range shrinks, but not at a steady rate. The
rate depends on where the camera looks:

- At :math:`x = 4`, the landmark is far ahead. The line of sight is
  :math:`32^\circ` off the road. Drive 1 m and the range drops 0.85 m:
  :math:`16 / 18.87 = 0.85`.
- At :math:`x = 19`, the landmark is almost beside the AV. The line of
  sight is :math:`84^\circ` off the road. Drive 1 m and the range drops
  only 0.10 m: :math:`1 / 10.05 = 0.10`.

The rate is how much of the line of sight points along the road,
:math:`(20 - x)/h(x)`. The range **drops** as :math:`x` grows, so the slope
of :math:`h` is that rate with a minus sign:

.. math::

   \frac{dh}{dx} = -\frac{20 - x}{h(x)}

The slope changes as the AV drives. **There is no single slope**, so no
fixed :math:`H` describes this sensor.


The surprise says the AV is farther ahead
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The camera measures from where the AV **really** is. The filter compares
that reading with the reading it **expects** at its estimate. The gap, the
surprise, is its only clue that the estimate is off.

.. figure:: /_static/images/L3/ekf_linearize_1_good.png
   :alt: The range to the landmark in meters against the AV's position along the road, 4 to 20 meters. Tag 1: a dotted horizontal line at 10.77 meters, the camera's reading. Tag 2: a green dot on the curve at x 15.5. Tag 3: a pointer to the short gap between the green dot and the reading line. Tag 4: a dashed purple tangent through the green dot. Tag 5: a green cross where the tangent meets the reading line, just left of 16. Tag 6: a dotted vertical line at 16 meters, where the AV really is.
   :align: center
   :width: 85%
   :class: white-figure

   Run 1. **1** The camera reads 10.77 m. **2** At :math:`\hat{x} = 15.5`
   m the filter expects :math:`h(15.5) = 10.97` m. **3** The surprise.
   **4** The tangent at :math:`\hat{x}`. **5** Where the tangent meets the
   reading. **6** Where the AV really is, 16 m.

The reading came in 0.20 m **less** than expected: :math:`10.77 - 10.97`.
Less range means closer to the landmark, so the AV is **farther ahead**
than :math:`\hat{x}`. How much farther is the next step.


Run 1: a good estimate lands near the truth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The surprise is in meters of **range**. The filter moves the AV in meters of
**position**. The slope of the tangent converts one into the other.

.. figure:: /_static/images/L3/ekf_linearize_1b_zoom.png
   :alt: A close-up of run 1, 14.5 to 17 meters along the road and 10.3 to 11.3 meters of range. The black curve and a dashed purple tangent through a green dot at 15.5 meters nearly overlap. Tag 1: a purple slope triangle from the dot, 1 meter to the right and about 0.41 meters down. Tag 2: a short black arrow down from the dot, near 10.97 meters, to a dotted reading line at 10.77 meters. Tag 3: a green arrow along the reading line from 15.5 to about 16. Tag 4: a green cross where the tangent meets the reading line, at about 15.98. Tag 5: a dotted vertical line at 16 meters, where the AV really is.
   :align: center
   :width: 85%
   :class: white-figure

   **1** The slope at :math:`\hat{x}`: 1 m ahead, 0.41 m less range.
   **2** The surprise: 0.20 m less range. **3** The move. **4** The new
   estimate. **5** Where the AV really is, 16 m.

The arithmetic, in four steps:

1. The slope at :math:`\hat{x} = 15.5`: there are :math:`20 - 15.5 = 4.5`
   m to go and the range is 10.97 m, so the range drops
   :math:`4.5 / 10.97 = 0.41` m per meter.
2. The surprise: the range must come down by 0.20 m (0.196 m before
   rounding).
3. The move: :math:`0.196 / 0.410 = 0.48` m ahead. It is the same
   arithmetic as time equals distance divided by speed.
4. The new estimate: :math:`15.5 + 0.48 = 15.98` m. The AV is really at
   16 m, so the filter is 0.02 m short.

Near the estimate, the tangent and the curve are almost the same line, so
the move is almost right. This example uses a perfect reading and trusts it
fully, to show one idea at a time. A real filter moves only part of the
way, by the gain :math:`K`. That changes how far it moves, not the slope it
uses.


Run 2: a poor estimate falls short
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same AV, same reading, 10.77 m. This time the estimate is
:math:`\hat{x} = 10` m, 6 m behind the AV.

.. figure:: /_static/images/L3/ekf_linearize_2_poor.png
   :alt: The range to the landmark in meters against the AV's position along the road, 4 to 20 meters. Tag 1: a dotted horizontal line at 10.77 meters, the camera's reading. Tag 2: an orange dot on the curve at x 10, near 14.14 meters. Tag 3: a long black arrow down from the orange dot to the reading line. Tag 4: a dashed purple tangent through the orange dot, which runs below the curve to the right of it. Tag 5: an orange cross where the tangent meets the reading line, near 14.8 meters, with a short two-headed arrow to a black dot on the curve at 16. Tag 6: a dotted vertical line at 16 meters, where the AV really is.
   :align: center
   :width: 85%
   :class: white-figure

   Run 2. **1** The camera reads 10.77 m. **2** At :math:`\hat{x} = 10` m
   the filter expects 14.14 m. **3** The surprise. **4** The tangent at
   10 m. **5** Where the tangent meets the reading, 14.77 m, 1.23 m short of
   **6**, the AV at 16 m.

The arithmetic, in four steps:

1. The surprise: :math:`14.14 - 10.77 = 3.37` m less range than expected,
   so the AV is farther ahead.
2. The slope at 10 m: :math:`-(20 - 10)/14.14 = -10 / 14.14 = -0.71`. The
   range drops 0.71 m per meter.
3. The move: :math:`3.37 / 0.71 = 4.77` m ahead, to
   :math:`10 + 4.77 = 14.77` m.
4. The miss: :math:`16 - 14.77 = 1.23` m short.

Why short? Between 10 m and 16 m the real curve drops only 3.37 m over
6 m, :math:`3.37 / 6 = 0.56` m per meter. The tangent at 10 m says 0.71.
The tangent is too steep, so the correction is too small.

That slope, :math:`-0.71`, is what the EKF calls the **Jacobian**
:math:`H` (defined below). A poor estimate gives a wrong :math:`H`, and a
wrong :math:`H` gives a correction of the wrong size. Run 2 still
improved: from 6 m off to 1.23 m off. `The catch: a feedback loop`_ shows
how a larger error can feed on itself.


Two jobs: the estimate uses the curve, P uses the tangent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Go back to the heading example, :math:`x = 20\cos\theta` with
:math:`\theta = 30^\circ \pm 12^\circ`. Replace the curve by its tangent at
the estimate, :math:`30^\circ`. A tangent is a straight line, so a bell
curve comes out again.

.. figure:: /_static/images/L3/bell_3_ekf.png
   :alt: The same three panels as the curve example: the input heading bell curve centered on 30 degrees at the bottom, the curve 20 cos theta at the top right, and the gray lopsided output histogram at the top left. A dashed orange straight line touches the curve at an orange dot at 30 degrees, labeled tangent at 30 degrees and EKF: one tangent. At the top left, a dashed orange bell curve centered on about 17.3 meters is drawn over the gray histogram; its upper half spills above 20 meters, where the histogram is empty. Readout: EKF: 17.32 m plus or minus 2.09 m; true: 16.95 m plus or minus 2.11 m.
   :align: center
   :width: 60%
   :class: white-figure

   Orange: the EKF. It pushes the input bell curve through the tangent at
   :math:`30^\circ` and gets a bell curve back. Gray: the true output.

So the EKF splits the work in two:

- The **estimate** goes through the real function:
  :math:`20\cos 30^\circ = 17.32` m.
- The **uncertainty** goes through the tangent: :math:`\pm 2.09` m.

The truth is :math:`16.95 \pm 2.11` m. The width is close. The mean is
:math:`17.32 - 16.95 = 0.37` m too far, because a straight line cannot see
the bend. The orange bell curve also spills above 20 m, where the AV can
never be.


The models f and h for an AV that turns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The EKF replaces the matrices :math:`F` and :math:`H` by **functions**
:math:`f` and :math:`h`. The noise, :math:`\mathbf{w}` for the motion and
:math:`\mathbf{v}` for the sensor, stays as before:

.. math::

   \mathbf{x}_k = f(\mathbf{x}_{k-1}, \mathbf{u}) + \mathbf{w},
   \qquad
   \mathbf{z}_k = h(\mathbf{x}_k) + \mathbf{v}

In the EKF hands-on, the state is :math:`\mathbf{x} = [x,\ y,\ \theta]`:
the position and the heading :math:`\theta`, the direction the AV's nose
points. The control input is :math:`\mathbf{u} = [v,\ \omega]`: the speed
:math:`v` from the wheel encoders and the turn rate :math:`\omega` from the
gyro. Over a time step :math:`\Delta t`:

.. math::

   \begin{bmatrix} x_k \\ y_k \\ \theta_k \end{bmatrix}
   =
   \begin{bmatrix} x_{k-1} + v\,\Delta t\cos\theta_{k-1} \\
                   y_{k-1} + v\,\Delta t\sin\theta_{k-1} \\
                   \theta_{k-1} + \omega\,\Delta t \end{bmatrix}
   + \mathbf{w}

Rows 1 and 2 hold the cosine and the sine of :math:`\theta`, and
:math:`\theta` is a state number. No fixed matrix :math:`F` holds them.

The camera in the hands-on matches an exit sign against the HD map, which
gives the sign's position :math:`(x_s, y_s)`. It reports the **range**
:math:`r`, how far away the sign is, and the **bearing** :math:`\beta`, the
angle from the AV's nose to the sign, positive to the left. With
:math:`\Delta x = x_s - x` and :math:`\Delta y = y_s - y`:

.. math::

   h(\mathbf{x}) = \begin{bmatrix} r \\ \beta \end{bmatrix}
   = \begin{bmatrix} \sqrt{\Delta x^2 + \Delta y^2} \\
     \operatorname{atan2}(\Delta y, \Delta x) - \theta \end{bmatrix}

:math:`\operatorname{atan2}` is the arctangent that keeps track of the
quadrant. A square root and an arctangent of the state: no fixed matrix
:math:`H` holds them either.


The Jacobian: the tangent for several inputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With one input and one output, the tangent is one slope. The motion model
above has three inputs and three outputs, so "the slope" becomes a table of
slopes.

.. admonition:: Definition: Jacobian
   :class: note

   The slopes of every output with respect to every input, for a function
   with several inputs and outputs. A table: entry :math:`(i, j)` says
   *nudge input* :math:`j` *a little, and output* :math:`i` *moves this
   much.*

The EKF needs two of them:

.. math::

   F_k = \left.\frac{\partial f}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}_{k-1}}
   \qquad\qquad
   H_k = \left.\frac{\partial h}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}^{-}_k}

- The curly :math:`\partial` reads "partial": the slope for one input while
  the other inputs stay put.
- The bar with a subscript says **where** the slope is taken.
  :math:`F_k` is taken at the **last estimate**, before predict moves it.
  :math:`H_k` is taken at the **prediction**.
- Both depend on the estimate, so both are **recomputed every step**. The
  plain Kalman filter's :math:`F` was a constant you typed once.

In the one-number range example, :math:`H` was the slope
:math:`-(20 - \hat{x})/h(\hat{x})`: :math:`-0.41` in run 1 and
:math:`-0.71` in run 2.


H_k with real numbers: range and bearing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the range and bearing model, :math:`H_k` has 2 rows (range, bearing) and
3 columns (:math:`x`, :math:`y`, :math:`\theta`). The numbers are chosen for
this example: the sign is 24 m east and 18 m north of the predicted
position, so :math:`r = \sqrt{24^2 + 18^2} = 30` m.

.. math::

   H_k =
   \begin{bmatrix}
     -\Delta x / r   & -\Delta y / r   & 0 \\
     \Delta y / r^2 & -\Delta x / r^2 & -1
   \end{bmatrix}
   =
   \begin{bmatrix}
     -0.80 & -0.60 & 0 \\
     0.020 & -0.027 & -1
   \end{bmatrix}

Read two entries:

- **Row 1, column 1:** move the AV 1 m east, partly toward the sign, and the
  range drops by :math:`24 / 30 = 0.80` m. The minus sign says it drops.
- **Row 2, column 3:** turn the nose 1 rad to the left. The sign has not
  moved, so it now sits 1 rad farther to the right of the nose. The bearing
  drops by exactly 1, wherever the sign is.

The middle entries of row 2 are small, :math:`18 / 900 = 0.020` and
:math:`24 / 900 = 0.027` rad per meter, about one degree per meter, because
the sign is 30 m away. A nearer sign makes them bigger.


P goes through the Jacobian
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The predicted covariance is :math:`P^{-} = F_k P F_k^\top + Q_k`: the same
sandwich as the Kalman filter, with a new :math:`F_k` at every step. The
next figure shows what that does on a real drive.

.. figure:: /_static/images/L3/ekf_story_3_ellipse.png
   :alt: Seen from above, north in meters against east in meters, 0 to 35. Tag 1: a green arc curving left from the origin to about 29 meters east and 7 meters north, with dots every half second. Black arrows show the heading at 0, 1, 2 and 3 seconds; tag 4 points at the one at 3 seconds. Light blue ellipses sit on the arc at 0, 1, 2 and 3 seconds, labeled with their times: tag 3 points at the small round one at 0 seconds. The ellipses grow longer and thinner over time, each lying across the direction of travel; tag 2 points at the longest one, at 3 seconds, about 8 meters long.
   :align: center
   :width: 100%
   :class: white-figure

   Predict only, on the EKF hands-on's bend (10 m/s, 60 m radius), with
   :math:`Q` left out to show :math:`F_k` alone. **1** The estimate follows
   the real :math:`f`, an arc. **2** At 3 s, the :math:`2\sigma` ellipse.
   **3** At 0 s: :math:`\sigma = 0.3` m each way, heading
   :math:`\sigma = 3^\circ`. **4** The heading.

The heading is known only to :math:`3^\circ`. A heading error moves the AV
**sideways**, and :math:`F_k` carries that into :math:`P`. Step after step,
the ellipse stretches across the direction of travel and stays thin along
it, and it turns with the AV. After 3 s, :math:`\sigma` is **1.58 m
across** the direction of travel and still **0.30 m along** it.


Building Q_k from the wheel and gyro noise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The motion noise is in the **inputs**: the wheel speed has an error
:math:`\sigma_v`, and the gyro an error :math:`\sigma_\omega`. :math:`P`
describes the state, so the noise must be carried into the state. One more
Jacobian does that: :math:`G = \partial f / \partial \mathbf{u}`, the slopes
of :math:`f` with respect to the inputs, taken at the last estimate. Then

.. math::

   Q_k = G \begin{bmatrix} \sigma_v^2 & 0 \\ 0 & \sigma_\omega^2 \end{bmatrix} G^\top

It is the same sandwich as :math:`FPF^\top`. :math:`G` depends on the
estimate, so :math:`Q_k` is **rebuilt every step**, next to :math:`F_k`.
The hands-on uses :math:`\sigma_v = 0.2` m/s and
:math:`\sigma_\omega = 2^\circ`/s.


The full EKF cycle
~~~~~~~~~~~~~~~~~~

Here is the EKF next to the Kalman filter, line by line. Each line that
changed is marked with a star.

.. list-table::
   :widths: 14 38 48
   :header-rows: 1
   :class: compact-table

   * - Step
     - Kalman filter
     - EKF
   * - Predict
     - :math:`\hat{\mathbf{x}}^{-} = F\hat{\mathbf{x}} + B\mathbf{u}`
     - :math:`\hat{\mathbf{x}}^{-} = f(\hat{\mathbf{x}}, \mathbf{u})` (*)
   * -
     - :math:`P^{-} = FPF^\top + Q`
     - :math:`P^{-} = F_k P F_k^\top + Q_k` (*)
   * - Update
     - :math:`\boldsymbol{\nu} = \mathbf{z} - H\hat{\mathbf{x}}^{-}`
     - :math:`\boldsymbol{\nu} = \mathbf{z} - h(\hat{\mathbf{x}}^{-})` (*)
   * -
     - :math:`S = HP^{-}H^\top + R`
     - :math:`S = H_k P^{-} H_k^\top + R` (*)
   * -
     - :math:`K = P^{-}H^\top S^{-1}`
     - :math:`K = P^{-}H_k^\top S^{-1}` (*)
   * -
     - :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^{-} + K\boldsymbol{\nu}`
     - :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^{-} + K\boldsymbol{\nu}`
   * -
     - :math:`P = (I - KH)P^{-}`
     - :math:`P = (I - KH_k)P^{-}` (*)

The pattern:

- Two lines use the **real functions**: moving the estimate, and predicting
  the reading.
- Every line with :math:`P`, :math:`S` or :math:`K` uses a **Jacobian**.
- The **order** matters. :math:`F_k` and :math:`Q_k` are computed at the
  last estimate, before the first line moves it. :math:`H_k` is computed at
  the prediction.

In code, from ``run_ekf()`` in the hands-on script
``curved_tunnel/ekf_curve.py``, trimmed:

.. code-block:: python

   # PREDICT: F_k and Q_k at the estimate, before moving it
   F = jacobian_f(x, u)
   Q = process_noise(x, u, SIGMA_V, sigma_w)
   x = f(x, u)                       # the estimate goes through the real f
   P = F @ P @ F.T + Q               # P goes through the tangent

   # UPDATE: one sign match, z = [range, bearing]
   Hk = jacobian_h(x, sign)          # H_k at the prediction
   nu = z - h(x, sign)               # expected reading from the real h
   nu[1] = wrap(nu[1])               # angles wrap
   S = Hk @ P @ Hk.T + R
   K = P @ Hk.T @ np.linalg.inv(S)
   x = x + K @ nu
   x[2] = wrap(x[2])                 # angles wrap
   P = (np.eye(3) - K @ Hk) @ P

The loop is short. Most of the work in an EKF goes into the three functions
around it: :math:`f`, :math:`h` and their Jacobians.


Checking a Jacobian with finite differences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Jacobian worked out by hand with one wrong sign gives a filter that runs,
does not crash, settles down, and is wrong. Nothing tells you. So test
every Jacobian before the filter sees data.

The test is the definition of a slope. Nudge one input by a small amount
:math:`\delta` up and down, call the real function both times, and divide
the change in the output by the change in the input:

.. math::

   \text{slope} \approx \frac{h(x + \delta) - h(x - \delta)}{2\delta}

This is a **finite difference**. For a function with several inputs, nudge
each input in turn. Each nudge gives one column of the Jacobian. Compare
each entry with your formula.

**On the range example**, at :math:`\hat{x} = 15.5` m with
:math:`\delta = 0.001` m (these numbers were computed for this page from
:math:`h(x) = \sqrt{(20 - x)^2 + 10^2}`):

1. :math:`h(15.501) = 10.965446` m.
2. :math:`h(15.499) = 10.966267` m.
3. The change: :math:`10.965446 - 10.966267 = -0.000821` m, over a change
   in :math:`x` of :math:`2 \times 0.001 = 0.002` m.
4. The slope: :math:`-0.000821 / 0.002 = -0.410`.
5. The formula gives :math:`-(20 - 15.5)/h(15.5) = -4.5 / 10.966 = -0.410`.
   They agree to three decimals.

If your formula had the wrong sign, it would give :math:`+0.410`, and the
check would show the mismatch at once. The EKF hands-on script has this check built in:
it nudges every input, measures how every output moves, and compares the
result with the formulas in the file.


Where the straight line stops being good enough
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run 2 was a poor estimate. The tangent also fails with a **good** estimate,
when the uncertainty is wide.

.. figure:: /_static/images/L3/breaks_2_banana.png
   :alt: Seen from above, a straight two-lane road. Tag 1: the AV on the right-hand lane at the left, with an arrow pointing east along the road. Tag 2: two dashed gray lines fanning out from it, one up and one down. Tag 3: a dotted gray arc far to the right, all points the same distance from the start. Tag 4: about 500 blue dots spread along that arc, forming a curved band, a banana, whose ends bend back toward the AV. Tag 5: a tall dashed orange ellipse, straight, drawn over the dots. Tag 6: an orange dot at the ellipse's center. Tag 7: a green cross just left of the orange dot, the real middle of the dots.
   :align: center
   :width: 80%
   :class: white-figure

   **1** The AV and its heading. **2** The heading spread,
   :math:`\sigma = 12^\circ`, chosen for this example. **3** Every spot 20 m
   from the start (the distance is known to :math:`\pm 0.5` m, also
   chosen). **4** Where the AV could be after 20 m: a banana. **5** The
   EKF's :math:`2\sigma` ellipse: straight, from one tangent. **6** The
   EKF's mean: 20.00 m ahead. **7** The real middle: 19.57 m.

The slides show this as an animation of the AV driving away from the start
with the same spreads. Two errors grow together as it drives:

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1
   :class: compact-table

   * - Driven
     - Distance ahead, EKF and real
     - Along-track :math:`\sigma`, EKF
     - Along-track :math:`\sigma`, real
   * - 4 m
     - 4.0 m, 3.93 m
     - 0.50 m
     - 0.52 m
   * - 13 m
     - 13.0 m, 12.73 m
     - 0.50 m
     - 0.62 m
   * - 22 m
     - 22.0 m, 21.54 m
     - 0.50 m
     - 0.79 m

- **The mean.** The EKF puts the AV at the full distance driven. The AV
  lands short, because the forward part of the drive is the distance times
  :math:`\cos\theta`, and the average of :math:`\cos\theta` over a spread of
  headings is less than 1. After 22 m, the real middle is 2 percent short.
- **The spread.** The EKF's along-track :math:`\sigma` stays at 0.50 m, the
  spread of the distance driven, while the real one grows to 0.79 m. The
  EKF is **overconfident**: it reports less uncertainty than it has.

No tuning fixes this. It is a shape problem: no ellipse can draw a banana.
The EKF works well while the uncertainty is small next to how sharply the
function bends. A long stretch with no sign match is exactly when it is
not.


The catch: a feedback loop
~~~~~~~~~~~~~~~~~~~~~~~~~~

A tangent is only right near the point where it touches. The EKF draws it
at its **own estimate**, so a wrong estimate puts it in the wrong place.

.. figure:: /_static/images/L3/ekf_story_4_loop.png
   :alt: A loop diagram. A gray box, "The estimate is a little off", points into a loop of four orange boxes joined by arrows: "The tangent is drawn in the wrong place"; "The correction is the wrong size"; "If it is far enough off, the next estimate is worse"; "The next tangent is drawn at that estimate"; and back to the first. In the middle of the loop: "each turn starts from a worse place". A shaded box on the right reads: "Meanwhile P shrinks at every update, right or wrong. Confident and wrong: divergence."
   :align: center
   :width: 85%
   :class: white-figure

   The EKF's feedback loop. Each turn starts from a worse estimate, while
   :math:`P` keeps shrinking.

Every update shrinks :math:`P`, whether the update was good or not. So the
filter becomes **more confident as it becomes less accurate**. That is
**divergence**. Run 2 still improved; the loop starts only when the error
is large enough to make the next estimate worse.


Three traps when you build an EKF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Wrap angles, in three places:** inside :math:`f`, in the surprise
   :math:`\boldsymbol{\nu}`, and in :math:`\hat{\mathbf{x}}` after the
   update. Headings of :math:`179^\circ` and :math:`-179^\circ` are
   :math:`2^\circ` apart. Subtract them the plain way and you get
   :math:`358^\circ`: the filter sees a huge surprise and swings the AV
   almost all the way round to fix a :math:`2^\circ` error. One line wraps
   an angle ``a`` into :math:`-180^\circ` to :math:`180^\circ`:
   ``np.arctan2(np.sin(a), np.cos(a))``.
2. **Test the Jacobians** with finite differences, as above. A wrong sign
   still runs and converges.
3. **Rebuild** :math:`F_k`, :math:`Q_k` **and** :math:`H_k` **every step,
   at the right point:** :math:`F_k` and :math:`Q_k` before predict moves
   :math:`\hat{\mathbf{x}}`, :math:`H_k` after. Computing :math:`F_k` after
   moving the estimate is a quiet bug.


The EKF hands-on
~~~~~~~~~~~~~~~~

The script ``curved_tunnel/ekf_curve.py`` runs an EKF on a drive of 21 s
through a :math:`120^\circ` bend, one row every 0.1 s. The wheel speed and
gyro give the control input. A sign match gives the range and bearing to a
mapped sign. The true pose is in the file only to score the filter. How to
run it is on the :doc:`hands-on code page </lectures/lecture3/l3_code>`, under
"Interactive: EKF and UKF on a curve".

What the slides measured with it:

- The heading :math:`\sigma` climbs between sign matches, while only the
  gyro drives the prediction. It drops at each match, because the bearing
  to the sign tells the filter which way the AV faces. It settles between
  about :math:`1.0^\circ` and :math:`1.4^\circ`.
- An honest filter keeps its true error inside its own :math:`\pm 1\sigma`
  band about 68 percent of the time. The default run: 65 percent.

What each setting does:

.. list-table::
   :widths: 34 16 16 14 20
   :header-rows: 1
   :class: compact-table

   * - Setting
     - Position error
     - Heading error
     - Inside 1 sigma
     - What it shows
   * - Default: gyro :math:`2^\circ`/s, range 1 m
     - 0.69 m
     - :math:`1.4^\circ`
     - 65%
     - honest
   * - :math:`Q` too small: gyro :math:`0.1^\circ`/s
     - 1.18 m
     - :math:`2.1^\circ`
     - 23%
     - **overconfident**
   * - :math:`Q` too big: gyro :math:`8^\circ`/s
     - 0.75 m
     - :math:`1.8^\circ`
     - 92%
     - underconfident
   * - :math:`R` too small: range 0.1 m
     - 1.42 m
     - :math:`1.8^\circ`
     - 46%
     - trusts every match
   * - Wrong sign in :math:`F_k`
     - 1.23 m
     - :math:`4.0^\circ`
     - 30%
     - **runs, and is wrong**

The last row is the one to remember. One wrong sign in a Jacobian nearly
doubles the position error, from 0.69 m to 1.23 m, and nearly triples the
heading error, from :math:`1.4^\circ` to :math:`4.0^\circ`. The filter never
complains. On a real AV you have no true pose to compare with, so your
defenses are the finite-difference check and the NIS test below.

The default gyro noise, :math:`2^\circ`/s, is bigger than the gyro's real
noise, :math:`1.1^\circ`/s, on purpose: :math:`Q` must also cover a small
gyro bias that the filter does not model.


Check yourself: the EKF
~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Question 1
   :class: hint

   In the EKF, what goes through the real :math:`f`, and what goes through
   the Jacobian?

   .. dropdown:: Answer

      The estimate goes through the real functions: :math:`f` to predict,
      :math:`h` for the expected reading. Everything that touches an
      uncertainty, :math:`P`, :math:`S` and :math:`K`, goes through the
      Jacobians :math:`F_k` and :math:`H_k`.

.. admonition:: Question 2
   :class: hint

   Why is :math:`Q_k` rebuilt every step?

   .. dropdown:: Answer

      The noise is in the wheel speed and the gyro. :math:`G`, the slope of
      :math:`f` for each of those inputs, carries it into the state, and
      :math:`G` depends on the heading estimate. The heading changes, so
      :math:`Q_k` changes.

.. admonition:: Question 3
   :class: hint

   Where is each Jacobian worked out, and why does that matter when the
   estimate is off?

   .. dropdown:: Answer

      :math:`F_k` at the last estimate, :math:`H_k` at the prediction. If
      the estimate is off, the tangent is drawn in the wrong place, the
      correction comes out the wrong size, and the next Jacobian is drawn at
      a worse estimate still. That is the feedback loop, and :math:`P`
      keeps shrinking while it happens.

.. admonition:: Question 4
   :class: hint

   One sign in your Jacobian is wrong, and the filter still runs. How do
   you catch it?

   .. dropdown:: Answer

      Nudge each input a little, see how each output moves, and compare
      with your formula: a finite-difference check, run once in a test
      before the filter ever sees data.


The Unscented Kalman Filter (UKF)
=================================

.. admonition:: Definition: unscented Kalman filter (UKF)
   :class: note

   A Kalman filter for curved models that **needs no tangents**. It pushes
   a few chosen points through the **real** function and rebuilds the mean
   and covariance from where they land.

**The idea.** Skip the slope and try a few what-ifs. Take the AV from the
banana: :math:`20 \pm 0.5` m out, heading :math:`0^\circ \pm 12^\circ`.
What if the heading is :math:`21^\circ` off, to the left or to the right?
What if the AV went 0.9 m farther, or 0.9 m less far? Drive each what-if
with the real model and see where it lands. The spread of the landing spots
is the new uncertainty. (The :math:`21^\circ` and the 0.9 m come from the
step-length rule below.)

**Why not keep the EKF?** A tangent is only good near the point where you
drew it. When :math:`P` is wide, after a long stretch with no sign match or
in a hard turn, the curve bends across the area that matters. Some models
are also only code, such as a search of the HD map for the sign the camera
should see. You can run that code, but it has no formula to take a slope
of.

**The cost.** :math:`2n + 1` calls to the model per step, where :math:`n`
is the number of values in the state. For the hands-on state
:math:`[x, y, \theta]`, :math:`n = 3`, so :math:`2 \times 3 + 1 = 7`
calls. There is no Jacobian of :math:`f` or :math:`h`. Only :math:`Q_k`
still uses :math:`G`, as in the EKF.


Three points through the real curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Back to :math:`x = 20\cos\theta` with :math:`\theta = 30^\circ \pm
12^\circ`. Instead of a tangent, the UKF picks three headings on the input
bell curve and pushes each through the real curve.

.. figure:: /_static/images/L3/bell_4_ukf.png
   :alt: The same three panels as the curve example. Bottom: the input heading bell curve centered on 30 degrees, with three green points on it at about 9, 30 and 51 degrees, labeled with weights 1/6, 2/3 and 1/6. Top right: the curve 20 cos theta, labeled UKF: three points; dotted green lines run from each point up to the curve and across to the output, landing near 19.7, 17.3 and 12.6 meters. Top left: a green bell curve fitted to those three landing spots, drawn over the gray lopsided histogram of the true output; its peak sits near 17 meters. Readout: UKF: 16.94 m plus or minus 2.12 m; true: 16.95 m plus or minus 2.11 m.
   :align: center
   :width: 60%
   :class: white-figure

   Three headings, weighted 1/6, 2/3 and 1/6, go through the real curve.
   Green: the bell curve rebuilt from where they land. Gray: the true
   output.

The arithmetic, in three steps:

1. **Place.** The middle, :math:`30^\circ`, and one step to each side,
   :math:`9.2^\circ` and :math:`50.8^\circ`.
2. **Push** each through the real curve: :math:`20\cos 9.2^\circ =
   19.74` m, :math:`20\cos 30^\circ = 17.32` m,
   :math:`20\cos 50.8^\circ = 12.64` m.
3. **Average** with the weights: :math:`\tfrac{2}{3} \times 17.32 +
   \tfrac{1}{6} \times 19.74 + \tfrac{1}{6} \times 12.64 = 16.94` m. The
   weighted spread gives :math:`\pm 2.12` m.

The truth, from 400,000 samples, is :math:`16.95 \pm 2.11` m. The EKF said
:math:`17.32 \pm 2.09` m. Both filters cheat to get a bell curve back, in
opposite places: **the EKF approximates the curve; the UKF approximates the
bell curve.**


Sigma points
~~~~~~~~~~~~

.. admonition:: Definition: sigma points
   :class: note

   :math:`2n + 1` points whose **weighted average is the mean** and whose
   **weighted spread is the covariance**. :math:`n` is the size of the
   state (Julier and Uhlmann, 1997).

.. list-table::
   :widths: 50 25 25
   :header-rows: 1
   :class: compact-table

   * - Where
     - State
     - Points
   * - The heading example above
     - :math:`\theta`
     - :math:`n = 1`: 3
   * - The drive below
     - :math:`d`, :math:`\theta`
     - :math:`n = 2`: 5
   * - The curved-tunnel hands-on
     - :math:`x`, :math:`y`, :math:`\theta`
     - :math:`n = 3`: 7


Place, push, rebuild
~~~~~~~~~~~~~~~~~~~~

The UKF predict step has three parts:

1. **Place** :math:`2n + 1` sigma points :math:`\chi_i`: the mean, plus one
   step out and one step back along each of :math:`n` directions. Point
   :math:`i` gets a weight :math:`W_i`; the weights add to 1.
2. **Push** each one through the real motion model. :math:`\mathcal{Y}_i`
   is where point :math:`i` lands:

   .. math::

      \mathcal{Y}_i = f(\chi_i, \mathbf{u})

3. **Rebuild** the prediction from where they land:

   .. math::

      \hat{\mathbf{x}}^{-} = \sum_i W_i\,\mathcal{Y}_i
      \qquad
      P^{-} = \sum_i W_i\,(\mathcal{Y}_i - \hat{\mathbf{x}}^{-})
              (\mathcal{Y}_i - \hat{\mathbf{x}}^{-})^\top + Q_k

   For each point, take how far it landed from the new mean, multiply that
   difference by itself (the matrix version of squaring it), weight it, and
   add them up. Then add :math:`Q_k`, because the model still makes its
   usual error each step.

**Step length.** The points sit at

.. math::

   \chi_0 = \hat{\mathbf{x}} \qquad
   \chi_i = \hat{\mathbf{x}} + \sqrt{n + \kappa}\;L_i \qquad
   \chi_{n+i} = \hat{\mathbf{x}} - \sqrt{n + \kappa}\;L_i

:math:`L_i` is column :math:`i` of :math:`L`, the **matrix square root** of
:math:`P`: the matrix with :math:`LL^\top = P`. Each column is one direction
to step in, already :math:`1\sigma` long. Code gets :math:`L` with one call,
named **Cholesky**. When :math:`P` is diagonal, the columns are the axes of
the ellipse. :math:`\kappa` sets how far out the points sit. The usual
choice is :math:`n + \kappa = 3`, so one step is :math:`\sqrt{3} \approx
1.7` :math:`\sigma`. That is where the what-ifs came from:
:math:`\sqrt{3} \times 12^\circ = 20.8^\circ`, about :math:`21^\circ`, and
:math:`\sqrt{3} \times 0.5 = 0.87` m.

**Weights.**

.. math::

   W_0 = \frac{\kappa}{n + \kappa} \qquad\qquad
   W_i = \frac{1}{2(n + \kappa)} \quad \text{for the other } 2n

.. list-table::
   :widths: 34 16 20 30
   :header-rows: 1
   :class: compact-table

   * - Case
     - :math:`\kappa`
     - Center
     - Each other point
   * - Heading example, :math:`n = 1`
     - 2
     - 2/3
     - 1/6 (two)
   * - Drive, :math:`n = 2`
     - 1
     - 1/3
     - 1/6 (four)
   * - Hands-on, :math:`n = 3`
     - 0
     - 0
     - 1/6 (six)

All three keep :math:`n + \kappa = 3`. With :math:`n = 3`, the center point
is still placed, but its weight is 0. Many libraries use a scaled version
with three settings, :math:`\alpha`, :math:`\beta` and :math:`\kappa`: same
idea, different weights, so their numbers will not match this table.


The same drive, done with five points
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AV drives :math:`20 \pm 0.5` m with its heading known to
:math:`0^\circ \pm 12^\circ`. Two numbers in the state, distance and
heading, so :math:`n = 2` and 5 sigma points. One step is
:math:`\sqrt{3} \times 0.5 = 0.87` m in distance, or
:math:`\sqrt{3} \times 12^\circ \approx 21^\circ` in heading.

.. figure:: /_static/images/L3/ukf_story_2_drive.png
   :alt: Three panels. 1, Place: distance driven in meters against heading in degrees, a light blue ellipse with five green points: chi 0 at the center, 20 meters and 0 degrees, weight 1/3; chi 1 above at about 20.9 meters and chi 3 below at about 19.1 meters; chi 2 to the right at about plus 21 degrees and chi 4 to the left at about minus 21 degrees; each of the four weighted 1/6. 2, Push through the real f: north against east in meters, a gray banana-shaped cloud near 20 meters east labeled 4,000 possible AVs, the real banana. Thin green lines run from the origin to the five landed points: three on the center line near 19 to 21 meters east, and two at about 18.7 meters east and plus and minus 7 meters north. 3, Rebuild a bell: the same cloud, with a green UKF ellipse and center cross at about 19.6 meters east, and a dashed orange EKF ellipse and center cross at 20 meters east. Labels: UKF 19.57, EKF 20.00, true 19.57.
   :align: center
   :width: 100%
   :class: white-figure

   **1 Place** the five sigma points. **2 Push** each through the real
   motion model; the gray cloud is 4,000 possible AVs. **3 Rebuild** a bell
   curve: green, the UKF; dashed orange, the EKF.

.. list-table::
   :widths: 15 15 35 35
   :header-rows: 1
   :class: compact-table

   * - Point
     - :math:`W_i`
     - Placed at
     - Lands at :math:`x`
   * - :math:`\chi_0`
     - 1/3
     - 20.0 m, :math:`0^\circ`
     - 20.00 m
   * - :math:`\chi_1`
     - 1/6
     - 20.9 m, :math:`0^\circ`
     - 20.87 m
   * - :math:`\chi_3`
     - 1/6
     - 19.1 m, :math:`0^\circ`
     - 19.13 m
   * - :math:`\chi_2`
     - 1/6
     - 20.0 m, :math:`+21^\circ`
     - 18.70 m
   * - :math:`\chi_4`
     - 1/6
     - 20.0 m, :math:`-21^\circ`
     - 18.70 m

The points with heading :math:`0^\circ` land where they were placed: an AV
pointed straight goes straight. The two turned points land short, at
18.70 m and about 7 m to the side, on the banana's arms. The weighted
average:

.. math::

   \tfrac{1}{3} \times 20.00 + \tfrac{1}{6} \times (20.87 + 19.13 + 18.70 + 18.70)
   = 6.667 + 12.900 = 19.57 \text{ m}

The truth is 19.57 m. The EKF says 20.00 m. The along-track spread from the
same five points is 0.79 m, against a true spread of about 0.78 m; the EKF
says 0.5 m, however far the AV drives. Two calls to the function that
landed short are what caught the banana.


The update without a Jacobian
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The update uses the same recipe, through :math:`h`. Place fresh sigma points
around the prediction :math:`\hat{\mathbf{x}}^{-}`, and push each through
:math:`h`: :math:`\mathcal{Z}_i = h(\chi_i)` is the reading that point
expects. Then

.. math::

   \hat{\mathbf{z}} = \sum_i W_i\,\mathcal{Z}_i
   \qquad
   S = \sum_i W_i\,(\mathcal{Z}_i - \hat{\mathbf{z}})(\mathcal{Z}_i - \hat{\mathbf{z}})^\top + R

.. math::

   P_{xz} = \sum_i W_i\,(\chi_i - \hat{\mathbf{x}}^{-})(\mathcal{Z}_i - \hat{\mathbf{z}})^\top
   \qquad
   K = P_{xz}\,S^{-1}

:math:`\hat{\mathbf{z}}` is the expected reading. :math:`P_{xz}` says how
the state and the reading **move together**: if the AV were a bit farther
east, would the range be longer or shorter? In the Kalman filter,
:math:`P^{-}H^\top` did that job. The UKF measures it from the points
instead. The new estimate is :math:`\hat{\mathbf{x}}^{-} + K\boldsymbol{\nu}`,
with :math:`\boldsymbol{\nu} = \mathbf{z} - \hat{\mathbf{z}}`, as always.

.. list-table::
   :widths: 14 38 48
   :header-rows: 1
   :class: compact-table

   * - Step
     - EKF
     - UKF
   * - Predict
     - :math:`\hat{\mathbf{x}}^{-} = f(\hat{\mathbf{x}}, \mathbf{u})`
     - :math:`\hat{\mathbf{x}}^{-} = \sum W_i\,\mathcal{Y}_i`
   * -
     - :math:`P^{-} = F_k P F_k^\top + Q_k`
     - :math:`P^{-} =` spread of :math:`\mathcal{Y}_i` :math:`+\, Q_k`
   * - Update
     - :math:`\hat{\mathbf{z}} = h(\hat{\mathbf{x}}^{-})`
     - :math:`\hat{\mathbf{z}} = \sum W_i\,\mathcal{Z}_i`
   * -
     - :math:`S = H_k P^{-} H_k^\top + R`
     - :math:`S =` spread of :math:`\mathcal{Z}_i` :math:`+\, R`
   * -
     - :math:`K = P^{-}H_k^\top S^{-1}`
     - :math:`K = P_{xz}\,S^{-1}`
   * -
     - :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^{-} + K\boldsymbol{\nu}`
     - :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^{-} + K\boldsymbol{\nu}`
   * -
     - :math:`P = (I - KH_k)P^{-}`
     - :math:`P = P^{-} - KSK^\top`

The last line looks different but means the same thing. In the Kalman
filter, :math:`KS = P^{-}H^\top`, so :math:`P^{-} - KSK^\top = (I -
KH)P^{-}`. The UKF uses the form that needs no :math:`H`. No :math:`F_k`,
no :math:`H_k`: no Jacobian of :math:`f` or :math:`h` to get wrong.


Three traps when you build a UKF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Average angles with care.** :math:`179^\circ` and :math:`-179^\circ`
   both point almost due west, but their plain average is :math:`0^\circ`,
   due east. Measure each angle from one reference point, wrap the
   differences, average those, and add the reference back. The hands-on's
   ``mean_and_cov()`` does this. The EKF never averages angles, so this
   trap is new.
2. **Cholesky needs a healthy** :math:`P`. It raises an error when
   :math:`P` is not symmetric and positive. Treat the error as a bug
   report: :math:`P` went bad upstream, often from rounding or from a
   :math:`Q` or :math:`R` far too small.
3. **Wrap** :math:`\boldsymbol{\nu}` **and** :math:`\hat{\mathbf{x}}`
   after the update, exactly as in the EKF.


The UKF hands-on
~~~~~~~~~~~~~~~~

The script ``curved_tunnel/ukf_curve.py`` runs the UKF next to the EKF on
the same tunnel, with an unlit stretch at the start where the camera
matches no sign. A referee drives 4,000 possible AVs through the same bend,
each with its own random wheel and gyro noise, and weighs them against
every sign match. That cloud is the **exact belief**. How to run it is on
the :doc:`hands-on code page </lectures/lecture3/l3_code>`.

What the slides measured, with the defaults (heading :math:`\sigma =
12^\circ` at the entrance, 5 s unlit):

- In the dark, all three beliefs grow together, to about 14 m of largest
  position :math:`\sigma`. The first sign match, near 6.8 s, shrinks all
  three to about 1 m.
- Just before that match, the EKF's mean is **1.45 m** from the exact
  belief's mean. It keeps the middle of a straight ellipse, not of the
  banana. The UKF's mean is **0.03 m** off.
- After the match, the UKF is the one farther off, about 1.1 m, shrinking
  to 0.1 m by 21 s. A 14 m belief meets a 1 m sign match, and the UKF
  corrects cautiously. Neither filter follows the exact belief at once.

How far each mean is from the exact belief, just before the first sign
match:

.. list-table::
   :widths: 40 30 30
   :header-rows: 1
   :class: compact-table

   * - Heading :math:`\sigma`, unlit time
     - EKF
     - UKF
   * - :math:`3^\circ`, 5 s
     - 0.12 m
     - 0.04 m
   * - :math:`12^\circ`, 5 s (default)
     - 1.45 m
     - 0.03 m
   * - :math:`12^\circ`, 9 s
     - 1.90 m
     - 0.03 m
   * - :math:`25^\circ`, 5 s
     - **6.03 m**
     - 0.01 m

With a small uncertainty the two agree. With a wide uncertainty on a curve,
the EKF's tangent misses and the UKF's points do not. The exact belief is
itself 4,000 samples, so the UKF column means "within a few hundredths, at
most 0.1 m".


The catch: still one bell curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

However cleverly the UKF places its points, it always rebuilds **one** mean
and **one** covariance: one bell curve, one peak. The EKF has the same
limit. When the honest answer is "here **or** there", neither can say it.
That is the particle filter's job.


Check yourself: the UKF
~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Question 1
   :class: hint

   The EKF approximates the curve. What does the UKF approximate instead?

   .. dropdown:: Answer

      The bell curve. The UKF keeps the real function and replaces the bell
      curve with a few points, then pushes each point through the real
      function.

.. admonition:: Question 2
   :class: hint

   With :math:`n = 2` and :math:`\kappa = 1`: how many sigma points, and
   what are their weights?

   .. dropdown:: Answer

      :math:`2n + 1 = 5` points. The center gets
      :math:`\kappa/(n + \kappa) = 1/3`. Each of the other four gets
      :math:`1/(2 \times 3) = 1/6`. They add to 1.

.. admonition:: Question 3
   :class: hint

   What takes the place of :math:`P^{-}H^\top` in the UKF gain, and where
   does it come from?

   .. dropdown:: Answer

      :math:`P_{xz}`, how the state and the reading move together. It comes
      from the sigma points: each point's distance from the prediction,
      times its expected reading's distance from :math:`\hat{\mathbf{z}}`,
      weighted and added up.

.. admonition:: Question 4
   :class: hint

   Can a UKF say "under this light **or** the next one"?

   .. dropdown:: Answer

      No. It still carries one mean and one covariance: one peak.


The Particle Filter
===================

.. admonition:: Definition: particle filter
   :class: note

   A filter that stores the belief as a **crowd of weighted guesses**,
   called particles, instead of one bell curve. So the belief can be in
   several places at once.

A **particle** is one complete guess at the state, with a **weight** that
says how much the filter believes it. The filter carries :math:`N` of them,
hundreds to thousands. The crowd is the belief: dense where the filter
thinks the AV is, empty where it does not.


When the belief has more than one peak
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every Kalman filter, the EKF and the UKF included, keeps the belief as one
bell curve: one best guess, one **peak**. A peak is a place the AV might be.

Picture the AV in a tunnel with no exit sign in view. It falls back on other
landmarks in the HD map, such as the ceiling lights. The lights are
identical, one every 25 m, with nothing on them for a camera to read. So "a
light overhead" fits this light and the next one equally well. The honest
belief has two peaks, with nothing in between.

.. figure:: /_static/images/L3/breaks_3b_bells.png
   :alt: A plot of belief per meter against position along the tunnel in meters, with 0, 12.5 and 25 marked. Tag 1: two tall, narrow solid blue bell curves, peaking at about 0.15 per meter over 0 and 25 meters. Tag 2: one low, wide dashed orange bell curve, peaking at about 0.03 per meter, spread across both. Tag 3: a dotted orange line at its mean, 12.5 meters, where the blue curves are zero. Tag 4: two yellow squares at the top, over 0 and 25 meters, the lights. Tag 5: a black cross on the axis at 0 meters.
   :align: center
   :width: 85%
   :class: white-figure

   **1** The honest belief: two peaks, :math:`\sigma = 1.3` m each, half
   the weight each. **2** The one bell curve with the same mean and spread.
   **3** Its mean: 12.5 m, with :math:`\sigma = 12.6` m. **4** The two
   lights, 25 m apart. **5** The AV, really at 0 m.

One mean and one covariance average the peaks. The mean lands at 12.5 m,
**between the lights**, the one place the honest belief says the AV is not.
With :math:`\sigma = 12.6` m, the bell curve also smears the AV across the
whole stretch. Nothing in the equations warns you.

The particle filter keeps no bell curve at all. On the heading example,
:math:`x = 20\cos\theta` with :math:`\theta = 30^\circ \pm 12^\circ`:

.. figure:: /_static/images/L3/bell_5_pf.png
   :alt: The same three panels as the curve example. Bottom: the input heading bell curve centered on 30 degrees, with about 200 blue dots scattered under it. Top right: the curve 20 cos theta, labeled PF: 200 points, with the blue dots placed along it and a few dotted guide lines to both sides. Top left: the dots shown again where they land, filling the gray lopsided histogram of the true output, dense just under 20 meters and thinning toward 10 meters. No bell curve is drawn. Readout: no bell: the dots are the belief; mean 16.82 m; true: 16.95 m.
   :align: center
   :width: 60%
   :class: white-figure

   200 random points from the input go through the real curve. Where they
   land fills the lopsided shape. No bell curve is fitted: the dots are the
   belief.

Their mean is 16.82 m; the true mean is 16.95 m. Two hundred random points
give a slightly noisy answer. More points, less noise: that is the price of
random points. The gain: the crowd can take any shape, even two separate
clumps.


One cycle: predict, weigh, resample
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is the same loop as the Kalman filter: predict, then update. The figure
shows one cycle along a road, with 40 particles.

.. figure:: /_static/images/L3/pf_cycle.png
   :alt: Three horizontal strips sharing an axis of position along the tunnel in meters, 3 to 27. Strip 1, Predict: move every particle, then give each its own random kick. 40 gray dots labeled last cycle, between about 3 and 11 meters, and 40 blue dots labeled after predict, between about 13 and 25 meters, more spread out, with an arrow labeled 10 m/s for 1 s. Strip 2, Weigh: score each particle against the measurement. An orange bell curve centered on a dashed line at 20.5 meters, labeled sign match, z equals 20.5 m, sigma equals 1.5 m. The blue dots are drawn with sizes that show their weight, labeled dot size equals weight: large near 20.5 meters, tiny far from it. Strip 3, Resample: copy the heavy ones, drop the light ones. Green dots, all the same size, between about 16.5 and 22 meters, stacked in columns, labeled stacked dots are copies of the same particle; the tallest stack is near 20.4 meters.
   :align: center
   :width: 100%
   :class: white-figure

   **1 Predict:** every particle moves, 10 m/s for 1 s, plus its own random
   kick. **2 Weigh:** a sign match at :math:`z = 20.5` m with
   :math:`\sigma = 1.5` m scores each particle; dot size shows the weight.
   **3 Resample:** heavy particles are copied, light ones dropped.

1. **Predict.** Move every particle with the motion model. Each particle
   also gets its own random kick, so the crowd spreads. The kick plays the
   role of :math:`Q`: where the Kalman ellipse grew, the crowd spreads.
2. **Weigh.** Score each particle: if the AV were really there, how likely
   is this reading? Nothing moves; the crowd gets weighed. This is the
   whole update.
3. **Resample.** Draw :math:`N` new particles from the old ones, each picked
   with probability equal to its weight. A heavy particle gets copied
   several times; a light one vanishes. Every weight goes back to
   :math:`1/N`. In this figure, the 40 particles came back as 16 different
   ones after one resample.

As equations, first one new word:

.. admonition:: Definition: likelihood
   :class: note

   :math:`p(\mathbf{z} \mid \mathbf{x})`: how likely the reading
   :math:`\mathbf{z}` is, **if** the AV were at :math:`\mathbf{x}`. For one
   sign match with noise :math:`\sigma`, it is the sensor's bell curve read
   at the gap between the reading and what :math:`h` says the AV would see
   from :math:`\mathbf{x}`:
   :math:`\exp\big(-(\mathbf{z} - h(\mathbf{x}))^2 / 2\sigma^2\big)`, up to a
   constant.

With :math:`\mathbf{x}^{(i)}` particle :math:`i` and :math:`w^{(i)}` its
weight:

1. **Predict:** :math:`\mathbf{x}^{(i)} \leftarrow f\big(\mathbf{x}^{(i)},
   \mathbf{u} + \text{noise}^{(i)}\big)`, a new draw of the noise for each
   particle.
2. **Weigh:** :math:`w^{(i)} \leftarrow w^{(i)}\, p(\mathbf{z} \mid
   \mathbf{x}^{(i)})`, then divide every weight by the sum so the weights
   add to 1.
3. **Resample:** draw :math:`N` particles, particle :math:`i` with
   probability :math:`w^{(i)}`. Reset every weight to :math:`1/N`.

No mean, no covariance, no gain and no Jacobian anywhere.


The recipe with numbers: five particles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Five particles, so you can check every number by hand. After predict they
sit at 8, 9, 10, 11 and 13 m. A sign match arrives: :math:`z = 10.5` m,
with :math:`\sigma = 1` m. Each particle's score is
:math:`\exp\big(-(z - x)^2 / 2\sigma^2\big)`.

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1
   :class: compact-table

   * - Particle
     - Score
     - Weight
     - Copies kept
   * - 8 m
     - 0.04
     - 0.02
     - 0
   * - 9 m
     - 0.32
     - 0.15
     - 1
   * - 10 m
     - 0.88
     - **0.40**
     - 2
   * - 11 m
     - 0.88
     - **0.40**
     - 2
   * - 13 m
     - 0.04
     - 0.02
     - 0

1. **Score.** The particle at 10 m is 0.5 m from the match:
   :math:`\exp(-0.5^2/2) = 0.88`. The one at 8 m is 2.5 m off:
   :math:`\exp(-2.5^2/2) = 0.04`.
2. **Weight.** The five scores add up to about 2.18. Divide each by that:
   the two near the match hold 40 percent each, the two far away 2 percent
   each.
3. **Resample.** Draw five new particles with those probabilities. The
   expected number of copies is five times the weight: about two for each
   particle near the match, almost none for the far ones. The right column
   is one draw.

Here the crowd has one peak, so the weighted average, 10.28 m, is a fine
estimate. With two peaks it would not be. Nothing was averaged into a place
the AV is not: every survivor was already on the list. That is why the
crowd can sit under two lights at once and an ellipse cannot.


The particle filter next to the UKF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 18 37 45
   :header-rows: 1
   :class: compact-table

   * -
     - UKF
     - Particle filter
   * - Belief
     - :math:`\hat{\mathbf{x}}` and :math:`P`
     - :math:`N` particles :math:`\mathbf{x}^{(i)}`, weights :math:`w^{(i)}`
   * - Points
     - :math:`2n + 1`, chosen
     - :math:`N`, random, thousands
   * - Predict
     - push through :math:`f`, rebuild, add :math:`Q_k`
     - push each through :math:`f` with its own noise
   * - Update
     - gain :math:`K` moves :math:`\hat{\mathbf{x}}`
     - weigh by :math:`p(\mathbf{z} \mid \mathbf{x}^{(i)})`, resample after
   * - Answer
     - :math:`\hat{\mathbf{x}}`
     - the heaviest cluster
   * - Shape
     - one peak
     - any shape

Both push points through the real :math:`f`. Only the UKF squeezes them back
into a bell curve.


Traps and costs
~~~~~~~~~~~~~~~

Three traps when you build one:

1. **Put a floor under the likelihood.** One bad reading can score every
   particle near zero, and the next line divides by the sum. The hands-on
   script adds :math:`10^{-3}`, so one bad reading can only nudge the
   weights.
2. **Resample only when needed.** Each resample copies some particles and
   drops others, so the crowd gets less varied every time. The **effective
   number of particles**, :math:`N_\text{eff} = 1 / \sum_i (w^{(i)})^2`,
   counts the particles that still matter: :math:`N` when all weigh the
   same, 1 when one particle holds all the weight. The script resamples
   when :math:`N_\text{eff} < N/2`.
3. **Run it more than once.** It is random, so one run proves nothing. The
   hands-on script can run the same drive 40 times and count how often it
   settles on the right place.

Three costs:

1. **It gets expensive fast.** You need about a fixed number of particles
   per quantity in the state, multiplied together. At ten per quantity:
   :math:`10^2 = 100` for :math:`[x, y]`, :math:`10^3 = 1{,}000` for
   :math:`[x, y, \theta]`, and :math:`10^6`, a million, for six. A Kalman
   filter costs about :math:`n^3` operations: for :math:`n = 6`,
   :math:`6^3 = 216`.
2. **It collapses quietly.** With too few particles, the crowd ends up on
   one peak and drops the others. No error is raised. It is the same failure
   as a diverging EKF: a confident number with nothing behind it.
3. **Do not average two peaks.** The weighted average of a cluster under one
   light and a cluster under the next is halfway between them. Report the
   heaviest cluster, or both, or "not yet resolved".


The particle filter hands-on: finding a lost AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The script ``pf_tunnel/pf_tunnel.py`` restarts the AV in a 700 m tunnel.
The AV knows its speed from the wheel encoders and nothing else. The camera
matches two kinds of landmark against the HD map: 23 identical lights, 25 m
apart, and five SOS niches spaced irregularly on purpose. A light match fits
23 places at once; a niche match fits five. The state is one number, the
distance along the tunnel. How to run it is on the
:doc:`hands-on code page </lectures/lecture3/l3_code>`.

.. figure:: /_static/images/L3/tunnel_pf_belief.png
   :alt: A plot titled the belief now: how much weight sits at each place, weight from 0 to 0.6 against position along the tunnel in meters, 0 to 700. A dashed black vertical line near 193 meters is labeled the AV's true position, with a tall blue spike along it. A medium spike, about 0.3, near 567 meters, and a small one, under 0.1, near 417 meters. Everywhere else the weight is near zero.
   :align: center
   :width: 100%
   :class: white-figure

   The belief 12 s in: how much weight sits at each place along the
   700 m tunnel. The dashed line is the AV's true position.

At 12 s the belief is in **three places at once**, near 193 m, 417 m and
567 m. The AV's true position is under the tallest spike. A bell curve
would put one peak at the weighted average, about 340 m, in empty tunnel.

.. figure:: /_static/images/L3/tunnel_pf_clusters.png
   :alt: A plot titled how many places the crowd is in (clusters), on a log scale from 1 to 30, against time in seconds, 0 to 45. The line starts near 23, drops to 18 within the first second, to 4 at about 2 seconds, to 3 at about 8 seconds, to 2 at about 14 seconds and to 1 at about 21 seconds, and stays at 1. Green vertical lines mark the niche matches at about 2, 14, 21, 33 and 45 seconds. A black vertical line marks 12 seconds.
   :align: center
   :width: 70%
   :class: white-figure

   How many places the crowd is in, over time. Green lines: SOS niche
   matches. Black line: 12 s.

.. figure:: /_static/images/L3/tunnel_pf_error.png
   :alt: A plot titled error in meters: heaviest cluster versus weighted average, on a scale that is logarithmic above 1 meter, against time in seconds, 0 to 45. The weighted average, orange, is 100 to 250 meters off until about 14 seconds, then between about 12 and 20 meters, and drops below 1 meter at about 21 seconds. The heaviest cluster, blue, drops below 1 meter at about 2 seconds and stays there; after 21 seconds the two lines overlap. Green vertical lines mark the niche matches, a black line marks 12 seconds.
   :align: center
   :width: 70%
   :class: white-figure

   The error of two answers. Blue: the heaviest cluster. Orange: the
   weighted average.

- **The crowd settles.** 23 clusters at the start, one per light. 4 after
  the first niche. The gaps between niches all differ, so each niche rules
  places out, and the crowd is in one place by 21 s.
- **How you read the answer matters.** The heaviest cluster is within a
  meter from about 2 s on. The weighted average stays 100 m or more off
  until the crowd is in one place. While the belief has several peaks,
  report the heaviest one, never the average.

Forty runs each, same drive, fresh random numbers:

.. list-table::
   :widths: 60 40
   :header-rows: 1
   :class: compact-table

   * - Setting
     - Right place
   * - 5,000 particles
     - 40 of 40
   * - 2,000 particles (default)
     - 40 of 40, by 21 s
   * - 500 particles
     - 33 of 40
   * - 100 particles
     - 11 of 40
   * - 30 particles
     - **1 of 40**
   * - Camera :math:`\sigma = 0.2` m (:math:`R` too small)
     - 31 of 40

When it fails, it does not look like a failure: you get one tight cluster,
a confident answer, in the wrong place. The crowd collapsed onto one peak
before the niches could rule it out. In the last row the filter is told the
camera is five times better than it is (0.2 m against the default 1.0 m),
so good particles are thrown away over small disagreements.


When to use a particle filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Use it when** the belief has several peaks: "where on this map am I?",
  a robot moved somewhere unknown, or a map match that fits several places.
- **Avoid it when** the state is big, or the belief has one peak. Then a
  Kalman filter does the same job for far less work.

Ask about the **shape of the belief**, not how curved the model is. A
strongly curved model with one peak is a UKF problem. A gently curved model
with three possible answers is a particle filter problem. Monte Carlo
Localization (Dellaert, Fox, Burgard and Thrun, 1999) is this filter used
on a real map.


Check yourself: the particle filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Question 1
   :class: hint

   What does the likelihood :math:`p(\mathbf{z} \mid \mathbf{x}^{(i)})`
   measure, and what does it do to a weight?

   .. dropdown:: Answer

      How likely the reading is if the AV were at that particle. The weight
      is multiplied by it, so particles that explain the reading get
      heavier, and resampling then copies them.

.. admonition:: Question 2
   :class: hint

   The crowd is under two lights. Why is the weighted average the worst
   answer to report?

   .. dropdown:: Answer

      The average of two clusters sits halfway between them, between the
      lights: the one place the camera says the AV is not. Report the
      heaviest cluster, or both.

.. admonition:: Question 3
   :class: hint

   You use too few particles. How does the filter fail, and does it warn
   you?

   .. dropdown:: Answer

      It collapses quietly. The crowd ends up in one place, sometimes the
      wrong one, and nothing raises an error. It looks just as confident as
      when it is right: with 30 particles, 1 run of 40 found the right
      place.


Choosing a Filter
=================

.. list-table::
   :widths: 15 85
   :header-rows: 1
   :class: compact-table

   * - Filter
     - Use it when
   * - **KF**
     - the model really is **linear**.
   * - **EKF**
     - the model **curves gently**. The default, and **GP3 uses it**.
   * - **UKF**
     - the model **curves hard**, the uncertainty is wide, or you have no
       Jacobian.
   * - **PF**
     - the belief has **several peaks** and the state is small.

None of the four checks whether its own confidence is deserved. Every one
shrinks its covariance, or tightens its crowd, at every update, whether or
not the update was any good. The next section is the check.


Checking a Filter: NIS
======================

Every filter reports two things: an estimate and a covariance. The
covariance is the filter's claim about its own accuracy, and you can test
that claim **without ground truth**. Before it sees a reading, the filter
says how big the surprise should be: that is :math:`S`. So compare the
surprises you get with the ones it predicted.

.. admonition:: Definition: normalized innovation squared (NIS)
   :class: note

   .. math::

      \varepsilon = \frac{\nu^2}{S}
      \qquad\text{or, for several numbers,}\qquad
      \varepsilon = \boldsymbol{\nu}^\top S^{-1}\boldsymbol{\nu}

   The surprise squared, divided by the surprise the filter expected. If
   the filter is honest, :math:`\varepsilon` averages **about 1 per number
   the sensor reports**.

Why divide? A surprise of 3 m means nothing on its own. If the filter
expected 10 m, 3 m is excellent. If it expected 0.1 m, 3 m is a crisis.
Squaring makes being wrong high and being wrong low count the same.

**An example**, from the tunnel Kalman filter hands-on at 9.3 s, along the
tunnel: :math:`\nu = 0.74`, :math:`S = 2.84`, so
:math:`\varepsilon = 0.74^2 / 2.84 = 0.19`. One reading tells you little.
Over all 19 sign matches, :math:`x` and :math:`y` together, the average is
**1.39** per match, against an expected 2 (one per number). With only 19
matches, chance alone puts the average anywhere from 1.2 to 3.0, 95 percent
of the time. So 1.39 is honest.

**Reading** :math:`\varepsilon` **over time.** For a sign match giving
:math:`x` and :math:`y`, an honest filter keeps :math:`\varepsilon`
between about **0.05 and 7.4**, 95 percent of the time. That band comes
from the chi-square distribution for 2 numbers.

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - :math:`\varepsilon` keeps landing
     - The filter is
   * - **above** the band
     - **overconfident**: :math:`Q` or :math:`R` is too small. Dangerous.
   * - **below** the band
     - **underconfident**. Wasteful, but safe.
   * - **inside** the band
     - **honest**. Its :math:`\sigma` means something.

**Gating.** The same number can throw away one reading that is wildly off.
For a sign match reporting :math:`x` and :math:`y`, the 99 percent line is
**9.21**: if :math:`\varepsilon > 9.21`, skip the reading and run on
prediction for one cycle. This catches a **wrong sign match**: the camera
misreads a sign's number, and the match arrives on time, looks normal, and
is 25 m wrong.

The trap: a gate throws out whatever disagrees with the current estimate.
If the estimate is already wrong, the good readings are the ones that
disagree, so the gate keeps the error. **Count rejections in a row**, and
raise an alarm past a limit.


Where This Is Used
==================

:doc:`GP3 </assignments/gp3>` Task 2 runs an EKF. You write its models and
their Jacobians, and the tests compare your Jacobians with finite
differences. Its state, its models and its rules are on the GP3 page.


References
==========

- Kalman, R. E. (1960). "A New Approach to Linear Filtering and Prediction
  Problems." *Journal of Basic Engineering*, 82(1), 35 to 45.
  `doi:10.1115/1.3662552 <https://doi.org/10.1115/1.3662552>`__
- Julier, S. J. and Uhlmann, J. K. (1997). "A New Extension of the Kalman
  Filter to Nonlinear Systems." *Proceedings of SPIE 3068, Signal
  Processing, Sensor Fusion, and Target Recognition VI*, 182 to 193.
  `doi:10.1117/12.280797 <https://doi.org/10.1117/12.280797>`__. The source
  of the sigma points.
- Dellaert, F., Fox, D., Burgard, W. and Thrun, S. (1999). "Monte Carlo
  Localization for Mobile Robots." *Proceedings of the IEEE International
  Conference on Robotics and Automation (ICRA)*, 1322 to 1328.
  `doi:10.1109/ROBOT.1999.772544 <https://doi.org/10.1109/ROBOT.1999.772544>`__
- Bar-Shalom, Y., Li, X.-R. and Kirubarajan, T. (2001). *Estimation with
  Applications to Tracking and Navigation: Theory, Algorithms and
  Software.* Wiley, New York. The source of the NIS test and the chi-square
  band.
- Thrun, S., Burgard, W. and Fox, D. (2005). *Probabilistic Robotics.* MIT
  Press, Cambridge, MA. Further reading on all four filters.
