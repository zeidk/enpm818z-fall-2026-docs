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

Every step of the Kalman filter multiplies the state by a fixed matrix. A
matrix does two things: it **scales** each number in the state by a fixed
amount, and it **adds** the results. So each output is a fixed number times
each state value, added up. Plot one output against one state value and you
always get a straight line. Some of an AV's models are straight lines. Many
are curves.

.. figure:: /_static/images/filters/line_or_curve.png
   :alt: Six panels in two rows. The top row shows three scenes from above, east and north in meters. Left, "Drive along a road at 30°": a gray road at 30 degrees from east; a black car at the origin and a faint gray car 20 meters along the road, joined by an arrow labeled "d = 20 m along the road"; a blue dashed line drops from the faint car to a blue two-headed arrow on the east axis labeled "x = 17.32 m east". Middle, "Drive 20 m at heading theta": a black car at the origin, an arrow labeled "20 m at heading theta" to a faint gray car, an angle theta between east and the arrow, a dotted arc labeled "every spot 20 m away", and a blue arrow on the east axis labeled "x = 20 cos theta". Right, "Measure the range to a sign": a gray road running east, a black car facing east at x = 16 meters, a black square labeled "the sign" 10 meters north of the road at x = 20, a line r from the car to the sign, a dotted line labeled 10 m, an arrow labeled "x = 16 m", and the text "the AV at x: r = 10.77 m". The bottom row has one graph under each scene. Left, "A straight line": distance east x against distance driven d, a straight line labeled x = d cos 30° = 0.866 d, with a blue dot labeled "d = 20 m: x = 17.32 m". Middle, "A curve": distance east x against heading theta from minus 90 to 90 degrees, an arch labeled x = 20 cos theta, with a blue dot labeled "theta = 30°: x = 17.32 m". Right, "A curve": range to the sign r against the AV's position along the road x from 0 to 30 meters, a curve lowest at 10 meters at x = 20, labeled r = square root of (20 minus x) squared plus 10 squared, with a blue dot labeled "x = 16 m: r = 10.77 m".
   :align: center
   :width: 100%
   :class: white-figure

   Three AV scenes from above, and the graph each one gives.

.. admonition:: Reading the figure
   :class: tip

   Each column is one scene. The top shows it from above; the bottom is
   its graph. The blue dot on each graph is the example drawn in the scene
   above it.

   - **Left, a straight line.** The road runs at :math:`30^\circ` from
     east, and the AV drives a distance :math:`d` along it. How far east it
     gets is :math:`x = d\cos 30^\circ = 0.866\,d`: a fixed number, 0.866,
     times :math:`d`. For :math:`d = 20` m, :math:`x = 17.32` m. Every
     extra meter driven adds the same 0.866 m east, so the graph is a
     straight line. A matrix can do that, so the Kalman filter can use this
     model.
   - **Middle, a curve.** Now the AV always drives 20 m, at heading
     :math:`\theta`, its angle from east. The end points lie on the dotted
     arc. How far east it gets is :math:`x = 20\cos\theta`: 20 m when it
     heads due east (:math:`0^\circ`), 17.32 m at :math:`30^\circ`, 0 m
     when it heads due north or south (:math:`\pm 90^\circ`).
   - **Right, a curve.** The AV drives east on a straight road. A sign
     stands 10 m off the road, beside the point :math:`x = 20` m. The
     camera measures the range :math:`r` from the AV to the sign:
     :math:`r = \sqrt{(20 - x)^2 + 10^2}`. From :math:`x = 16` m it reads
     10.77 m. The range is smallest, 10 m, when the AV is beside the sign.

No fixed number times :math:`\theta` gives a cosine, and no fixed number
times :math:`x` gives that square root. So the plain Kalman filter breaks
the moment the AV turns, or a camera measures a range. The next two sections
show why: a straight line keeps the filter's uncertainty in the shape the
filter needs, and a curve does not.


A straight line keeps a bell curve a bell curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Kalman filter describes every number it is unsure of with a **bell
curve** (a normal distribution). Two numbers set a bell curve: its
**mean**, the most likely value, under the peak, and its **spread**
:math:`\sigma`, how wide it is. ":math:`20 \pm 1` m" is short for a bell
curve with mean 20 m and :math:`\sigma = 1` m. The real value is within one
:math:`\sigma` of the mean, here between 19 and 21 m, about 68% of the time.
That every uncertainty is a bell curve is the filter's assumption, not a
fact about the AV.

The AV is on a road that runs at :math:`30^\circ` from east. Its heading is
**known**, :math:`30^\circ`. The distance it drives is not: :math:`d = 20
\pm 1` m. You track :math:`x`, how far east it gets.

.. figure:: /_static/images/filters/road_30_top.png
   :alt: A top view, east to the right and north up, both in meters. A gray road runs from the bottom left up to the right at 30 degrees from east. A black car at the origin, labeled "the AV at the start", points along the road; an arc marks the 30 degree angle between east and the road. About 20 meters along the road, a faint gray copy of the car has a dark gray bar under it along the road and a black dot in its middle, labeled "where it ends: 19 to 21 m along the road". Two blue dashed lines drop from the ends of the gray bar to the east axis, where a blue bar is labeled "how far east: 16.45 to 18.19 m". A dotted line drops from the black dot to the east axis at about 17.3 meters.
   :align: center
   :width: 75%
   :class: white-figure

   The road from above: where the AV starts, and where it can end.

.. admonition:: Reading the figure
   :class: tip

   - The black AV starts at the origin and heads along the gray road,
     :math:`30^\circ` from east.
   - It drives :math:`d = 20 \pm 1` m, so it most likely ends on the dark
     gray stretch, 19 to 21 m along the road. The faint AV marks 20 m.
   - The blue dashed lines drop the ends of that stretch onto the east axis.
     How far east the AV ends is :math:`x = d\cos 30^\circ`: the blue
     stretch, from :math:`19 \times 0.866 = 16.45` m to
     :math:`21 \times 0.866 = 18.19` m.

The next figure is not a picture of the road. It is three graphs: the bell
curve for :math:`d`, the function :math:`x = d\cos 30^\circ`, and the bell
curve that comes out for :math:`x`.

.. figure:: /_static/images/filters/bell_line.png
   :alt: Three plots side by side. Left, "Step 1: what the AV knows": probability density per meter against distance driven d from 16 to 24 meters; a gray bell curve peaked at 20 with a height of 0.40, labeled d = 20 plus or minus 1 m, with a shaded stretch from 19 to 21 meters. Middle, "Step 2: the function": distance east x against distance driven d, a straight line labeled "x = d cos 30°: a straight line"; a gray vertical band from d = 19 to 21 and a blue horizontal band from x = 16.45 to 18.19 cross on the line; a dotted guide runs from d = 20 up to the line and across to x = 17.32. Right, "Step 3: what you get": probability density per meter against distance east x from 13.5 to 21 meters; a blue bell curve peaked near 17.3 with a height of about 0.46, labeled "x = 17.32 plus or minus 0.87 m: still a bell curve", with a shaded stretch labeled 16.45 to 18.19 m.
   :align: center
   :width: 100%
   :class: white-figure

   A bell curve through a straight line stays a bell curve.

.. admonition:: Reading the figure
   :class: tip

   Read the three panels left to right.

   - **Step 1, what the AV knows:** the bell curve for the distance driven,
     :math:`d = 20 \pm 1` m. The height is the **probability density**: how
     likely each distance is, per meter. The area under the curve between two
     distances is the chance that :math:`d` falls between them, and the whole
     area is 1. The shaded stretch is 19 to 21 m, one :math:`\sigma` on each
     side of the mean; about 68% of the area lies over it.
   - **Step 2, the function:** :math:`x = d\cos 30^\circ`, a straight line.
     Follow the dotted line: :math:`d = 20` m gives :math:`x = 17.32` m. The
     gray stretch of :math:`d` lands on the blue stretch of :math:`x`, 16.45
     to 18.19 m, as in the top view.
   - **Step 3, what you get:** the curve for :math:`x`. A straight line
     multiplies every possible :math:`d` by the same number, 0.866, so every
     part of the input curve shrinks by the same factor. The shape stays a
     bell curve, 0.866 times as wide. Its area must still be 1, so it is
     :math:`1 / 0.866 = 1.15` times as tall: a peak of 0.46 per meter
     instead of 0.40.

The numbers, in two steps:

1. The mean: :math:`20 \times \cos 30^\circ = 20 \times 0.866 = 17.32` m.
2. The spread: :math:`1 \times 0.866 = 0.87` m.

Through a straight line, a bell curve stays a bell curve, and
:math:`FPF^\top` gives its width exactly. That is why the Kalman filter
works.


A curve bends a bell curve out of shape
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The last section knew the heading and was unsure of the distance. This one
swaps them, on the same road. The AV drives a **known** 20 m, and its
heading is unsure: :math:`\theta = 30^\circ \pm 12^\circ`. The
:math:`12^\circ` is a value chosen for this example, large enough to show
the effect.

The input is again a bell curve. What changes is the function. How far east
the AV gets is now :math:`x = 20\cos\theta`, a curve in :math:`\theta`, not
a straight line.

.. figure:: /_static/images/filters/bell_curve.png
   :alt: Three plots side by side. Left, "Step 1: what the AV knows": probability density per degree against heading theta from minus 10 to 70 degrees; a gray bell curve peaked at 30 with a height of about 0.033, labeled theta = 30° plus or minus 12°, with a shaded stretch labeled 18° to 42°. Middle, "Step 2: the function": distance east x against heading, the curve labeled "x = 20 cos theta: a curve", highest at 20 meters at 0 degrees and falling to about 7 meters at 70 degrees; a gray vertical band from 18 to 42 degrees and a blue horizontal band from about 14.9 to 19.0 meters cross on the curve; a dotted guide runs from 30 degrees up to the curve and across to 17.32 meters. Two black dots mark the ends of the gray band on the curve, labeled "18°: 19.02 m, 1.70 m above" and "42°: 14.86 m, 2.46 m below". Right, "Step 3: what you get": probability density per meter against distance east x; blue histogram bars from about 7.5 to 20 meters, low on the left and highest, about 0.2, between about 17.5 and 19.5 meters, cut off at 20, labeled "lopsided: not a bell curve". A solid vertical line is labeled "its mean, 16.95 m" and a dashed vertical line just to its right is labeled "20 cos 30° = 17.32 m".
   :align: center
   :width: 100%
   :class: white-figure

   A bell curve through a curve comes out lopsided.

.. admonition:: Reading the figure
   :class: tip

   - **Step 1, what the AV knows:** the bell curve for the heading,
     :math:`30^\circ \pm 12^\circ`. Its height is the probability density per
     degree. The shaded stretch is :math:`18^\circ` to :math:`42^\circ`, one
     :math:`\sigma` on each side of the mean.
   - **Step 2, the function:** :math:`x = 20\cos\theta`, a curve. The dotted
     line: :math:`30^\circ` gives 17.32 m. Now follow the two black dots.
     They are the same step in heading, :math:`12^\circ` each way, but not
     the same step east:

     - :math:`12^\circ` less, :math:`18^\circ`, gives
       :math:`20\cos 18^\circ = 19.02` m: only 1.70 m more than 17.32 m.
     - :math:`12^\circ` more, :math:`42^\circ`, gives
       :math:`20\cos 42^\circ = 14.86` m: 2.46 m less.

     The curve is flat near :math:`0^\circ` and never goes above 20 m, so it
     squeezes the small headings together and spreads the large ones apart.
     The blue stretch is not centered on 17.32 m.
   - **Step 3, what you get:** 400,000 random headings from the Step 1 curve,
     each pushed through :math:`20\cos\theta`. The bars count where they
     land, scaled to a probability density per meter so that their total
     area is 1, as for a bell curve. They pile up just under 20 m, where the
     squeezed headings land, and trail off in a long tail below, where the
     spread-out ones land. The solid line is their mean, 16.95 m. The dashed
     line is the curve at the mean heading, :math:`20\cos 30^\circ = 17.32`
     m.

So the output is not a bell curve, and its mean is **16.95 m**, not
17.32 m. The mean of the output is not the curve at the mean of the input.

The two sections side by side:

.. list-table::
   :widths: 24 38 38
   :header-rows: 1
   :class: compact-table

   * -
     - Through a straight line
     - Through a curve
   * - Known
     - the heading, :math:`30^\circ`
     - the distance, 20 m
   * - Unsure
     - the distance, :math:`d = 20 \pm 1` m
     - the heading, :math:`\theta = 30^\circ \pm 12^\circ`
   * - Function
     - :math:`x = d\cos 30^\circ`, a straight line
     - :math:`x = 20\cos\theta`, a curve
   * - Equal steps in
     - give equal steps east: 0.866 m per meter
     - give unequal steps east: 1.70 m up, 2.46 m down
   * - What you get
     - a bell curve, :math:`17.32 \pm 0.87` m
     - lopsided, mean 16.95 m, not 17.32 m

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

.. figure:: /_static/images/filters/ekf_tangent_steps.png
   :alt: A graph of the range to the sign r in meters against the AV's position along the road x in meters, from 0 to 24. A thick black curve, labeled "the real range, r", falls from about 22.4 meters at x = 0, is lowest, 10 meters, at x = 20, and rises after that. Purple dots on the curve at 4, 9 and 14 meters are labeled "step 1: the estimate, 4 m, and the tangent there", and the same for step 2 at 9 m and step 3 at 14 m. Through each dot a short, wide, light purple band lies along the curve. A dashed purple line, labeled "the tangent at 4 m, drawn long", starts at the first dot and runs straight on, falling farther and farther below the curve. At x = 18 it ends at a purple dot, and a two-headed black arrow from that dot up to the curve is labeled "at 18 m it says 7.00 m; the real range is 10.20 m".
   :align: center
   :width: 85%
   :class: white-figure

   The EKF draws a new tangent at each step.

.. admonition:: Reading the figure
   :class: tip

   - The black curve is the range to the sign, :math:`r`, from the right
     panel of the first figure on this page. The three estimates, 4, 9 and
     14 m, are values chosen for this picture.
   - **Step 1:** the estimate is 4 m. The EKF draws the tangent there, the
     short purple band, and uses it in place of the curve for that step.
   - **Steps 2 and 3:** the estimate has moved to 9 m, then to 14 m. Each
     step draws a new tangent at the new estimate. Near its estimate, each
     band lies on the curve.
   - The dashed line is the tangent at 4 m, drawn long. At 18 m it says
     7.00 m, and the real range is 10.20 m. Far from where it touches, a
     tangent is wrong.

Near the point where it touches, the tangent and the curve are almost the
same. In the EKF hands-on, the AV drives a bend of 60 m radius at 10 m/s.
It turns :math:`10 / 60 = 0.167` rad/s, so in one 0.1 s step it turns
:math:`0.167 \times 0.1 = 0.0167` rad, or :math:`0.95^\circ`. Over one step
the curve is almost straight.


A worked example: the range to one landmark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example has one number in the state, so you can follow every step by
hand.

.. figure:: /_static/images/filters/range_road_top.png
   :alt: A top view, to scale: position along the road x in meters to the right, from 0 to 20, and distance across the road up, from 0 to 10 meters. A gray one-lane road, labeled "the road", runs left to right, and an arrow on it says "the AV drives this way", to the right. A black car faces right, with the middle of its rear axle, a white dot, at x = 16. A black square at x = 20, 10 meters above the AV's path, is labeled "the landmark"; a dotted gray line labeled 10 m drops from it to the AV's path. A thick black line from the white dot to the landmark is labeled "the range from the AV at 16 m: 10.77 m". Above the road, a green triangle at 15.5 meters is labeled "run 1: the estimate, 15.5 m", and an orange triangle at 10 meters is labeled "run 2: the estimate, 10 m". Under the road, a black two-headed arrow from 0 to 16 is labeled "x = 16 m", and a gray one from 16 to 20 is labeled "20 − x = 4 m".
   :align: center
   :width: 80%
   :class: white-figure

   The road from above: the AV, the landmark and the two estimates.

.. admonition:: Reading the figure
   :class: tip

   - The AV drives right along the road. Its position :math:`x` is measured
     at the middle of its rear axle, the white dot. It is really at
     :math:`x = 16` m.
   - The landmark stands 10 m off the AV's path, beside :math:`x = 20` m.
   - The thick black line is the range the camera measures: 10.77 m from
     16 m.
   - Under the road: :math:`x = 16` m from the start of the axis, and
     :math:`20 - x = 4` m from the AV to the spot beside the landmark.
   - The triangles above the road are the filter's estimate in the two runs
     below: 15.5 m in run 1 (green) and 10 m in run 2 (orange).

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

.. figure:: /_static/images/filters/range_curve.png
   :alt: Two panels. Left, titled "The road from above", to scale: position along the road x in meters, with ticks at 4, 10, 16 and 19, and distance across the road, up to 10 meters. A gray band is labeled "the road". A black square at x = 20, 10 meters off the AV's path, is labeled "the landmark". Black lines of sight run to it from four dots on the road, each labeled with its length: 18.87 m from 4 m, 14.14 m from 10 m, 10.77 m from 16 m and 10.05 m from 19 m. Arcs mark the line from 4 m at 32° off the road and the line from 19 m at 84°. A faint gray car with its rear axle at 16 m is labeled "the faint AV: where the AV really is". Right, titled "A graph, not the road: range against position": the range to the landmark in meters, from 8.5 to 20.5, against the AV's position along the road x, from 3 to 21 meters. A black curve, labeled "the range, h(x)", falls from about 19.7 meters at x = 3 and flattens toward 10 meters at x = 20. Black dots on it, with dotted lines down to the x axis, are labeled "from 4 m: 18.87 m", "from 10 m: 14.14 m", "from 16 m: 10.77 m" and "from 19 m: 10.05 m".
   :align: center
   :width: 100%
   :class: white-figure

   The range from four positions: from above, and as a graph.

.. admonition:: Reading the figure
   :class: tip

   - **Left, the road from above, to scale.** The camera's line of sight to
     the landmark from four positions on the road: 4, 10, 16 and 19 m. Each
     line is labeled with its length, the range :math:`h(x)`. The faint AV
     marks where the AV really is, 16 m.
   - The arcs show how far each line of sight points away from the road:
     :math:`32^\circ` from 4 m, where the landmark is far ahead, and
     :math:`84^\circ` from 19 m, where it is almost beside the AV.
   - **Right, a graph, not the road.** The vertical axis is the range
     :math:`h(x)`, and the horizontal axis is the position :math:`x`. Each
     dot is one of the four positions on the left, at the height of its
     range.
   - The curve falls steeply near 4 m and flattens near 19 m.

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

.. figure:: /_static/images/filters/ekf_run1_whole.png
   :alt: The range to the landmark in meters, from 8.6 to 19.4, against the AV's position along the road x, from 4 to 20 meters. A thick black curve, labeled "the real range, h(x)", falls from about 18.9 meters at x = 4 and flattens near 10 meters at x = 20. A dotted gray horizontal line is labeled "the camera reads 10.77 m". A green dot on the curve at 15.5 meters is labeled "the estimate, 15.5 m: the filter expects 10.97 m". A label, "surprise: 0.20 m less range", points to the small gap between the green dot and the dotted line. A dashed purple line, labeled "the tangent at 15.5 m", runs through the green dot from about 11.5 to 17.5 meters, close to the curve. A green cross where the tangent crosses the dotted line is labeled "where the tangent meets the reading: 15.98 m". A dotted gray vertical line at 16 meters is labeled "the AV really is at 16 m". A thin gray box around x = 14 to 17.2 meters and ranges 10.3 to 11.45 meters is labeled "drawn close up in the next figure".
   :align: center
   :width: 85%
   :class: white-figure

   Run 1: the estimate, the reading and the tangent.

.. admonition:: Reading the figure
   :class: tip

   - The dotted horizontal line is the camera's reading, 10.77 m. The
     camera takes it from where the AV really is, 16 m, the dotted vertical
     line.
   - The green dot is run 1's estimate, :math:`\hat{x} = 15.5` m. On the
     curve, the filter expects a reading of :math:`h(15.5) = 10.97` m.
   - The surprise is the gap between the two: the reading is 0.20 m less
     than expected. At this scale the gap is small. The next figure draws
     the gray box close up.
   - The dashed purple line is the tangent at :math:`\hat{x}`. It meets the
     reading line at the green cross, 15.98 m, almost where the AV really
     is.

The reading came in 0.20 m **less** than expected: :math:`10.77 - 10.97`.
Less range means closer to the landmark, so the AV is **farther ahead**
than :math:`\hat{x}`. How much farther is the next step.


Run 1: a good estimate lands near the truth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The surprise is in meters of **range**. The filter moves the AV in meters of
**position**. The slope of the tangent converts one into the other.

.. figure:: /_static/images/filters/ekf_run1.png
   :alt: A close-up of run 1. The horizontal axis is the AV's position along the road, x, from 14 to 17 meters; the vertical axis is the range to the landmark, from 10.3 to 11.4 meters. A thick black curve, labeled the real range h(x), falls from left to right. A dashed purple line, labeled the tangent at 15.5 m, touches the curve at a green dot labeled "the estimate, 15.5 m: the filter expects 10.97 m"; the two lines almost overlap. A purple right triangle above the dot is 1 m wide and 0.41 m tall. A dotted gray line at 10.77 m is labeled "the camera reads 10.77 m". A black arrow points down from the dot to that line, labeled "surprise: 0.20 m less range". A green arrow points right along it, labeled "move: 0.20 / 0.41 = 0.48 m", and ends at a green cross labeled "new estimate, 15.98 m", where the tangent meets the reading line. The cross sits almost on the black curve at 16 m, labeled "the AV really is at 16 m".
   :align: center
   :width: 85%
   :class: white-figure

   Run 1, close up: a good estimate lands near the AV.

.. admonition:: Reading the figure
   :class: tip

   - Start at the green dot, the estimate: 15.5 m, where the filter expects
     a range of 10.97 m.
   - Go down by the surprise, the black arrow, to the camera's reading, the
     dotted line at 10.77 m: 0.20 m less range.
   - The purple triangle is the slope of the tangent: 1 m ahead, 0.41 m less
     range.
   - Go right by the move, the green arrow: :math:`0.20 / 0.41 = 0.48` m.
     The green cross is the new estimate, 15.98 m. The AV is really at 16 m.

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

.. figure:: /_static/images/filters/ekf_run2.png
   :alt: Run 2. The horizontal axis is the AV's position along the road, x, from 4 to 20 meters; the vertical axis is the range to the landmark, from 10 to 19 meters. A thick black curve, labeled the real range h(x), falls from left to right and flattens near 20 m. An orange dot on the curve at 10 m is labeled "the estimate, 10 m: the filter expects 14.14 m". A dotted gray line at 10.77 m is labeled "the camera reads 10.77 m". A long black arrow points down from the dot to that line, labeled "surprise: 3.37 m less range". A dashed purple line through the dot is labeled "the tangent at 10 m: 0.71 m less range per meter"; it runs below the curve to the right of the dot. An orange dotted line from the dot to a black dot on the curve at 16 m is labeled "the real drop from 10 m to 16 m: 0.56 m per meter". The tangent meets the reading line at an orange cross labeled "new estimate, 14.77 m". A two-headed orange arrow from the cross to the black dot, labeled "the AV really is at 16 m", is labeled "1.23 m short".
   :align: center
   :width: 85%
   :class: white-figure

   Run 2: a poor estimate falls short.

.. admonition:: Reading the figure
   :class: tip

   - The orange dot is the estimate, 10 m, where the filter expects 14.14 m.
     The camera reads 10.77 m, the dotted line: 3.37 m less range, the black
     arrow.
   - The dashed purple line is the tangent at 10 m: 0.71 m less range per
     meter. The dotted orange line is the real drop from 10 m to 16 m: 0.56 m
     per meter.
   - The tangent falls faster than the real curve, so it reaches the reading
     too soon: at the orange cross, 14.77 m, 1.23 m short of the AV at 16 m.

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

.. figure:: /_static/images/filters/bell_ekf.png
   :alt: Three plots side by side. Left, "Step 1: what the AV knows": a gray bell curve over heading theta from minus 10 to 70 degrees, peaked at 30, labeled theta = 30° plus or minus 12°, with a shaded stretch labeled 18° to 42°; the y axis is probability density per degree, 0 to 0.04. Middle, "Step 2: the function": distance east x against heading, the black curve labeled "x = 20 cos theta: the curve" and a dashed orange straight line labeled "the tangent at 30°: a straight line" that touches it at an orange dot at 30 degrees and 17.32 meters; a gray vertical band from 18 to 42 degrees and an orange horizontal band labeled 15.23 to 19.41 m. Right, "Step 3: what you get": blue histogram bars over distance east x, lopsided and cut off at 20 meters, with a dashed orange bell curve over them that runs on past 20 meters, labeled "above 20 m: impossible"; the y axis is probability density per meter. A black vertical line is labeled "true mean, 16.95 m" and an orange one "EKF mean, 17.32 m". Text at the top left reads "the EKF: 17.32 ± 2.09 m" in orange and "the truth: 16.95 ± 2.11 m" in blue.
   :align: center
   :width: 100%
   :class: white-figure

   The EKF pushes the heading bell curve through the tangent at 30°.

.. admonition:: Reading the figure
   :class: tip

   Read the three panels left to right. They match the curve example above, panel
   by panel.

   - **Step 1, what the AV knows:** the same bell curve for the heading,
     :math:`30^\circ \pm 12^\circ`. The height of the curve is the probability
     density. The area under the curve between two values is the chance that the
     value falls between them.
   - **Step 2, the function:** the black curve is :math:`x = 20\cos\theta`. The
     dashed orange line is its tangent at :math:`30^\circ`, the line the EKF uses
     in its place. The tangent drops :math:`20 \times \sin 30^\circ \times \pi / 180
     = 0.1745` m per degree. So the gray stretch of headings, 12° on each side,
     lands on the orange stretch, :math:`17.32 \pm 12 \times 0.1745`: from 15.23 m
     to 19.41 m. That stretch is centered on 17.32 m, because a straight line
     treats both sides the same.
   - **Step 3, what you get:** the blue bars are the true output, the same 400,000
     headings as in the curve example, pushed through the real curve. The dashed
     orange bell curve is the EKF's answer, :math:`17.32 \pm 2.09` m. The black
     line is the true mean, 16.95 m, and the orange line is the EKF's mean,
     17.32 m. About 10% of the area under the orange curve lies above 20 m,
     where the AV can never be.

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

.. figure:: /_static/images/filters/ekf_bend_ellipses.png
   :alt: Seen from above, north in meters against east in meters. A black arc curves left from the origin to about 29 meters east and 7 meters north, with dots every half second; it is labeled "the estimate: an arc from the real f". Black arrows show the heading at 0, 1, 2 and 3 seconds; the one at 3 seconds is labeled "the heading". Orange ellipses, labeled "each ellipse: 2σ", sit on the arc at 0, 1, 2 and 3 seconds, each marked with its time. The one at 0 seconds is a small circle labeled "at 0 s: σ = 0.3 m each way, heading σ = 3°". The ellipses grow longer and thinner over time and lie nearly across the direction of travel; the one at 3 seconds, about 6 meters long, is labeled "at 3 s: σ = 1.58 m the long way, 0.30 m the short way".
   :align: center
   :width: 100%
   :class: white-figure

   Predict only on the EKF hands-on's bend: :math:`P` stretches sideways.

.. admonition:: Reading the figure
   :class: tip

   - The AV drives the hands-on's bend: 10 m/s on a 60 m radius, one predict
     step every 0.1 s. :math:`Q` is left out, so only :math:`F_k` changes
     :math:`P`.
   - The black arc is the estimate, moved by the real :math:`f` at each step. The
     dots are 0.5 s apart. The arrows show the heading at 0, 1, 2 and 3 s.
   - Each orange ellipse is the position part of :math:`P`, drawn
     :math:`2\sigma` out from the estimate.
   - At 0 s the ellipse is a circle: :math:`\sigma = 0.3` m east and north, and
     a heading :math:`\sigma` of :math:`3^\circ`. Both are chosen for this
     example.
   - At 3 s, :math:`\sigma` is 1.58 m the long way and still 0.30 m the short
     way. The long way points nearly across the direction of travel. It turns
     with the AV, but more slowly: at 3 s it is :math:`75^\circ` from the
     heading, not :math:`90^\circ`.

The heading is known only to :math:`3^\circ`. A heading error moves the AV
**sideways**, and :math:`F_k` carries that into :math:`P`. Step after step,
the ellipse stretches nearly across the direction of travel and stays thin
the other way, and it turns with the AV. After 3 s, :math:`\sigma` is
**1.58 m the long way**, :math:`75^\circ` from the heading, and still
**0.30 m the short way**.


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

.. figure:: /_static/images/filters/banana_belief.png
   :alt: Seen from above, east and north in meters, a straight two-lane road. A black AV, labeled "the AV, heading east", sits in the lower lane at the origin with an arrow pointing east. Two dashed gray lines fan out from it, labeled "heading spread: ±12° (1σ)". A dotted gray arc about 20 meters ahead is labeled "every spot 20 m from the start". About 500 blue dots, labeled "where the AV could be after 20 m: 500 draws", spread along that arc from about 11 meters north to 11 meters south, forming a curved band whose ends bend back toward the AV. A tall dashed orange ellipse, straight, centered at 20 meters east, is drawn over the dots and labeled "the EKF's 2σ ellipse: straight, from one tangent". An orange dot at its center is labeled "the EKF's mean: 20.00 m ahead", and a black cross just left of it is labeled "the real middle: 19.57 m ahead".
   :align: center
   :width: 90%
   :class: white-figure

   A wide heading spread bends the belief into a banana.

.. admonition:: Reading the figure
   :class: tip

   - The black AV starts at the left, in the right-hand lane, heading east.
   - Its heading is known only to :math:`\pm 12^\circ` (one :math:`\sigma`),
     the gray dashed lines, and the distance it drives to :math:`20 \pm 0.5` m.
     Both values are chosen for this example.
   - The gray dotted arc is every spot 20 m from the start.
   - The 500 blue dots are random draws of the heading and the distance, each
     driven with the real model. They show where the AV could be. They follow
     the arc, so the band bends back toward the AV at both ends: a banana.
   - The dashed orange ellipse is the EKF's :math:`2\sigma` ellipse. It comes
     from one tangent, so it is straight: 1 m ahead and behind
     (:math:`2 \times 0.5` m) and 8.38 m to each side
     (:math:`2 \times 20 \times 0.209`, with :math:`12^\circ = 0.209` rad).
   - The orange dot is the EKF's mean, 20.00 m ahead. The black cross is the
     real middle of the dots, 19.57 m ahead.

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

.. figure:: /_static/images/filters/ekf_feedback_loop.png
   :alt: A loop diagram. A gray box, "The estimate is a little off", points into a loop of four orange boxes joined by arrows, clockwise: "The tangent is drawn in the wrong place"; "The correction is the wrong size"; "If it is far enough off, the next estimate is worse"; "The next tangent is drawn at that estimate"; and back to the first. In the middle of the loop: "each turn starts from a worse place". A shaded orange box on the right reads: "Meanwhile P shrinks at every update, right or wrong. Confident and wrong: divergence".
   :align: center
   :width: 85%
   :class: white-figure

   The EKF's feedback loop.

.. admonition:: Reading the figure
   :class: tip

   - Start at the gray box: the estimate is a little off.
   - Follow the orange arrows clockwise. The tangent is drawn at the wrong
     estimate, so the correction is the wrong size. If the error is large
     enough, the next estimate is worse, and the next tangent is drawn there.
   - The box on the right happens at the same time: every update shrinks
     :math:`P`, whether it helped or not.

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

.. figure:: /_static/images/filters/bell_ukf.png
   :alt: Three plots side by side. Left, "Step 1: place three points": a gray bell curve of probability density per degree over heading theta, from minus 10 to 70 degrees, labeled theta = 30° ± 12°, with three green dots on the curve, labeled 9.2° weight 1/6, 30° weight 2/3, and 50.8° weight 1/6. Middle, "Step 2: push each through the curve": distance east x in meters against heading, the curve labeled "x = 20 cos θ: the real curve", with the three green dots on it and dotted green guides to both axes, labeled 19.74 m, 17.32 m and 12.64 m. Right, "Step 3: average with the weights": blue histogram bars of probability density per meter over distance east x, highest between about 17.5 and 19.5 meters and cut off at 20, with a green bell curve labeled "the UKF's bell curve", peaked near 17 meters. Three green dots on the x axis, at 12.64, 17.32 and 19.74 meters, are labeled "where the three points land". At the top, in blue, "true: 16.95 ± 2.11 m", and in green, "UKF: 16.94 ± 2.12 m".
   :align: center
   :width: 100%
   :class: white-figure

   Three headings through the real curve, rebuilt into one bell curve.

.. admonition:: Reading the figure
   :class: tip

   - **Step 1, place three points:** the same heading bell curve as in the
     curve example, :math:`30^\circ \pm 12^\circ`. The height of a curve is
     the probability density: the area under it between two values is the
     chance that the value falls between them. The UKF picks three headings:
     the mean, :math:`30^\circ`, and one step to each side,
     :math:`9.2^\circ` and :math:`50.8^\circ`. A weight says how much a point
     counts in the average: 2/3 for the middle, 1/6 for each side.
   - **Step 2, push each through the curve:** follow each green dot up to
     the real curve and across to :math:`x`. The three headings give 19.74 m,
     17.32 m and 12.64 m. The UKF calls the real function three times and
     draws no tangent.
   - **Step 3, average with the weights:** the blue bars are the true output
     from the curve example, 400,000 random headings pushed through
     :math:`20\cos\theta`. The green dots on the axis are where the three
     points land. The green curve is the bell curve the UKF rebuilds from
     their weighted mean and weighted spread: :math:`16.94 \pm 2.12` m,
     against a true :math:`16.95 \pm 2.11` m.

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

.. figure:: /_static/images/filters/ukf_sigma_points.png
   :alt: Three panels. Left, "Step 1: place five points": distance driven d in meters, 18.7 to 21.7, against heading theta in degrees, minus 30 to 30. A gray ellipse, labeled "gray, the input (2σ ellipse): d = 20 ± 0.5 m, θ = 0° ± 12°", holds five green dots: chi 0 at the center, 20 meters and 0 degrees, weight 1/3; chi 1 above, at about 20.9 meters, and chi 3 below, at about 19.1 meters; chi 2 to the right, at about 21 degrees, and chi 4 to the left, at about minus 21 degrees; each of the four has weight 1/6. Middle, "Step 2: push each through f": seen from above, north against east in meters, to scale. A black car at the origin faces east, labeled "the AV starts here, facing east". A gray curved cloud between about 17 and 21 meters east, labeled "gray: 4,000 possible AVs". Thin green lines run from the car to five green dots: "chi 2 lands 18.70 m east, 7.1 m north", "chi 4 lands 18.70 m east, 7.1 m south", and three dots on the line straight east, labeled "chi 3, chi 0, chi 1 stay on this line". Right, "Step 3: rebuild a bell curve": the same cloud, closer, with a tall, thin green filled ellipse labeled "UKF ellipse" and a tall, thin dashed orange ellipse just to its right, labeled "EKF ellipse". A green dot is labeled "UKF mean: 19.57 m east" and an orange dot just right of it "EKF mean: 20.00 m east". Text below them: "middle of the gray cloud: 19.57 m east".
   :align: center
   :width: 100%
   :class: white-figure

   The five sigma points of the drive: place, push, rebuild.

.. admonition:: Reading the figure
   :class: tip

   - **Step 1, place five points.** This plot is not a map. It shows the two
     numbers the AV is unsure of: the distance driven :math:`d` and the
     heading :math:`\theta`. The gray ellipse is the input,
     :math:`d = 20 \pm 0.5` m and :math:`\theta = 0^\circ \pm 12^\circ`,
     drawn out to :math:`2\sigma`. :math:`\chi_0` sits at the center, with
     weight 1/3. The other four sit one step out along each axis, with weight
     1/6 each: :math:`\chi_1` 0.87 m farther and :math:`\chi_3` 0.87 m less
     far; :math:`\chi_2` turned :math:`21^\circ` to the left (:math:`+21^\circ`)
     and :math:`\chi_4` turned :math:`21^\circ` to the right
     (:math:`-21^\circ`).
   - **Step 2, push each through** :math:`f`. Now the plot is the road from
     above, to scale. The AV starts at the origin, facing east. The real
     motion model drives each point :math:`d` meters at heading
     :math:`\theta`. The gray cloud is 4,000 possible AVs, each with a random
     distance and heading drawn from the input: the real banana. The three
     points with heading :math:`0^\circ` stay on the line straight east.
     :math:`\chi_2` and :math:`\chi_4` land on the banana's arms, 18.70 m east
     and 7.1 m to each side.
   - **Step 3, rebuild a bell curve.** The same view, closer. The green
     ellipse is the bell curve the UKF rebuilds from the five landing spots,
     drawn out to :math:`2\sigma`. Its center, the green dot, is the weighted
     average, 19.57 m east: the middle of the gray cloud. The dashed orange
     ellipse is the EKF's, from the tangent at the mean heading. Its center,
     the orange dot, sits at the full 20.00 m.

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

.. figure:: /_static/images/filters/two_peaks.png
   :alt: A graph of probability density per meter, 0 to 0.15, against position along the tunnel in meters, minus 15 to 40. Two tall, narrow blue bell curves peak at about 0.15 per meter over 0 and 25 meters, labeled "the honest belief: two peaks, σ = 1.3 m each, half the weight each". A low, wide dashed orange bell curve peaks at about 0.03 per meter over 12.5 meters, labeled "one bell curve with the same mean and spread: σ = 12.6 m". A dotted orange line at 12.5 meters is labeled "its mean, 12.5 m: between the lights, where the honest belief is near zero". Two yellow squares at the top, over 0 and 25 meters, are labeled "a light at 0 m" and "a light at 25 m". A black cross on the axis at 0 meters is labeled "the AV is really at 0 m".
   :align: center
   :width: 85%
   :class: white-figure

   Two peaks against one bell curve.

.. admonition:: Reading the figure
   :class: tip

   - This is a graph, not a map of the tunnel. The horizontal axis is the
     position along the tunnel. The height of a curve is the probability
     density: the area under it between two positions is the chance that the
     AV is between them.
   - The yellow squares mark the two lights, 25 m apart. The black cross is
     where the AV really is, under the light at 0 m.
   - The blue curve is the honest belief: one peak under each light, each
     with :math:`\sigma = 1.3` m and half the weight.
   - The dashed orange curve is the one bell curve with the same mean and
     spread as the blue curve. Its mean, the dotted line, is 12.5 m: between
     the lights, where the blue curve is near zero. Its :math:`\sigma` is
     :math:`\sqrt{1.3^2 + 12.5^2} = 12.6` m. The 1.3 m is the width of each
     peak, the 12.5 m is how far each peak sits from the middle, and the two
     add as squares.

One mean and one covariance average the peaks. The mean lands at 12.5 m,
**between the lights**, the one place the honest belief says the AV is not.
With :math:`\sigma = 12.6` m, the bell curve also smears the AV across the
whole stretch. Nothing in the equations warns you.

The particle filter keeps no bell curve at all. On the heading example,
:math:`x = 20\cos\theta` with :math:`\theta = 30^\circ \pm 12^\circ`:

.. figure:: /_static/images/filters/bell_pf.png
   :alt: Three plots side by side. Left, "Step 1: what the AV knows": probability density per degree against heading theta, from minus 10 to 70 degrees. A black bell curve over a gray fill peaks at 30 degrees and is labeled theta = 30° ± 12°. Purple dots, labeled "200 random headings", are stacked in columns that roughly follow the curve. Middle, "Step 2: the function": distance east x in meters against heading. The black curve x = 20 cos theta carries the purple dots, from 0 to about 60 degrees. A dotted guide from one dot, labeled "one point: 45.2° gives 14.08 m", runs down to the heading axis and across to the distance axis. Right, "Step 3: what you get": probability density per meter against distance east x, from 6 to 21 meters. A light blue stepped outline, labeled "blue: the true shape (400,000 points)", is low on the left, highest near 18 meters and cut off at 20. Purple dots stacked in columns, labeled "dots: where the 200 points land", roughly fill it. A dashed purple line is labeled "mean of the dots: 16.82 m" and a solid black line just to its right is labeled "true mean: 16.95 m".
   :align: center
   :width: 100%
   :class: white-figure

   200 random points through the same curve: the dots are the belief.

.. admonition:: Reading the figure
   :class: tip

   Read the three panels left to right, as in the curve figure above. The
   height of a curve or a column is a probability density: the higher it is
   above a value, the more likely that value. Each dot adds the same height,
   0.002 per degree on the left and 0.01 per meter on the right.

   - **Step 1, what the AV knows:** the same heading bell curve,
     :math:`30^\circ \pm 12^\circ`. The 200 purple dots are random headings
     drawn from it. Each column holds the dots that fall in one
     :math:`2.5^\circ` stretch, so the columns roughly follow the curve.
   - **Step 2, the function:** each dot goes through the real curve,
     :math:`x = 20\cos\theta`. There is no tangent, and nothing is fitted.
     The dotted line follows one dot: :math:`45.2^\circ` gives 14.08 m.
   - **Step 3, what you get:** each column holds the dots that land in one
     0.5 m stretch. The blue outline is the true shape from 400,000 points,
     as in the curve figure. The dots follow its lopsided shape: many just
     under 20 m, a thin tail below. Their mean, the dashed line, is 16.82 m.
     The true mean, the solid line, is 16.95 m.

Their mean is 16.82 m; the true mean is 16.95 m. Two hundred random points
give a slightly noisy answer. More points, less noise: that is the price of
random points. The gain: the crowd can take any shape, even two separate
clumps.


One cycle: predict, weigh, resample
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is the same loop as the Kalman filter: predict, then update. The figure
shows one cycle along a road, with 40 particles.

.. figure:: /_static/images/filters/pf_cycle_steps.png
   :alt: Three strips, one above the other, sharing one axis: position along the tunnel in meters, 3 to 27. Strip 1, "Step 1: predict": 40 gray dots between about 3.5 and 13 meters, labeled "the 40 particles, last cycle", and 40 purple dots between about 13 and 25 meters, labeled "after predict: more spread out". An arrow between the two groups is labeled "each moves 10 m/s for 1 s, plus its own random kick". Strip 2, "Step 2: weigh": score from 0 to 1 against position. A black bell-shaped curve peaks at 1 over a dotted gray line at 20.5 meters, labeled "the sign match: z = 20.5 m, σ = 1.5 m"; the curve is labeled "the score: how well a particle here explains the reading". The purple dots sit on the axis, large near 20.5 meters and tiny far from it. One large dot is labeled "big dot: heavy, weight 0.093" and the leftmost tiny dot "tiny dot: far from the match, weight close to 0". Strip 3, "Step 3: resample": copies, from 0 to 7, against position. Purple dots stand in columns between about 16.5 and 22 meters; the tallest column, 7 dots, is labeled "7 copies of the particle at 20.36 m". Text on the left reads "40 particles again, but only 16 different ones".
   :align: center
   :width: 100%
   :class: white-figure

   One cycle with 40 particles: predict, weigh, resample.

.. admonition:: Reading the figure
   :class: tip

   - **Step 1, predict:** the gray dots are the 40 particles from the last
     cycle. Each one moves by the motion model, 10 m/s for 1 s, so 10 m.
     Each one also gets its own random kick, so the purple crowd after
     predict is more spread out.
   - **Step 2, weigh:** a sign match reads :math:`z = 20.5` m, with
     :math:`\sigma = 1.5` m. The black curve is the score a particle gets at
     each position: 1 right at the reading, close to 0 a few meters away.
     Nothing moves. Each particle's weight is its score divided by the sum of
     all 40 scores, and the size of its dot shows that weight. The heaviest
     particle holds 0.093 of the weight.
   - **Step 3, resample:** 40 new particles are drawn from the old ones, each
     picked with probability equal to its weight. The height of a column
     counts the copies of one particle. The particle at 20.36 m was copied 7
     times, and the light particles far from the reading are gone. The 40
     particles are now only 16 different ones.

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

.. figure:: /_static/images/filters/tunnel_belief.png
   :alt: A bar chart of the weight per 2 m bin, from 0 to 0.6, against position along the tunnel, 0 to 700 meters. A tall purple bar of about 0.55 at 193 meters is labeled "193 m: 57% of the weight", and a dashed black line through it is labeled "where the AV really is, 193 m". A dashed orange line at 341 meters, where there is almost no weight, is labeled "weighted average of the whole crowd, 341 m". A short purple bar of about 0.08 at 417 meters is labeled "417 m: 8% of the weight", and a bar of about 0.29 at 568 meters is labeled "568 m: 35% of the weight". Everywhere else the bars are close to zero.
   :align: center
   :width: 100%
   :class: white-figure

   The belief 12 s in, along the 700 m tunnel.

.. admonition:: Reading the figure
   :class: tip

   - The horizontal axis is the tunnel, 0 to 700 m. The height of a bar is
     the share of the particles' weight that sits in that 2 m stretch. All
     the bars add up to 1.
   - At 12 s the weight sits in three places: 57% near 193 m, 35% near
     568 m and 8% near 417 m. Each place is a **cluster**, a group of
     particles close together.
   - The dashed black line is where the AV really is, 193 m, under the
     tallest bar.
   - The dashed orange line is the weighted average of all the particles,
     341 m. Almost no weight sits there.

At 12 s the belief is in **three places at once**, near 193 m, 417 m and
568 m. The AV's true position is under the tallest spike. A bell curve
would put one peak at the weighted average, 341 m, where almost no weight
sits.

.. figure:: /_static/images/filters/tunnel_clusters.png
   :alt: A step plot of the number of places (clusters), 0 to 25, against time in seconds, 0 to 45. The purple line starts at 23, labeled "23 at the start: one per light", flickers to 22, drops to 18 at half a second, labeled 18, then to 4 at 2.1 seconds, labeled "4 after the first niche", to 3 at about 8 seconds, to 2 at 14.1 seconds, and to 1 at 20.9 seconds, labeled "1 from 20.9 s on". Gray vertical lines labeled niche mark 2.1, 14.1, 20.9, 32.7 and 44.7 seconds. A dotted black line marks 12 s.
   :align: center
   :width: 70%
   :class: white-figure

   How many places the crowd is in, over time.

.. admonition:: Reading the figure
   :class: tip

   - The purple line counts the clusters that hold more than 2% of the
     weight: the places the AV might still be.
   - Each gray line is an SOS niche match. A light match fits 23 places; a
     niche match fits only five, so the big drops come at a niche.
   - At the start: 23 places, one per light. After the first niche, at
     2.1 s: 4. After the second, at 14.1 s: 2. After the third, at 20.9 s:
     1, and it stays at 1.
   - The two small drops, at 0.5 s and 8.1 s, come at light matches. The
     map has no light within 5 m of a niche, so a place that expects a light
     in one of those gaps loses its weight.
   - The dotted line marks 12 s, the moment in the belief figure: 3 places.

.. figure:: /_static/images/filters/tunnel_error.png
   :alt: Error in meters against time in seconds, 0 to 45. The y axis is linear from 0 to 1 meter and logarithmic above, up to 1000. A thick orange line, labeled "weighted average", sits near 300 meters until 2.1 seconds, between about 120 and 170 meters until 14.1 seconds, and between about 12 and 21 meters until 20.9 seconds, then drops below 1 meter. A thin purple line, labeled "heaviest cluster", starts near 70 meters, jumps to about 300 meters, drops close to 0 at 2.1 seconds and stays under 1 meter, mostly between 0 and 0.6. After 20.9 seconds the two lines lie on top of each other, labeled "the two answers agree: the crowd is in one place". A dashed line marks 1 meter, gray vertical lines labeled niche mark the five niche matches, and a dotted line marks 12 s.
   :align: center
   :width: 70%
   :class: white-figure

   The error of two answers from the same crowd.

.. admonition:: Reading the figure
   :class: tip

   - Both lines come from the same crowd at each moment. The purple line is
     the error of the heaviest cluster. The orange line is the error of the
     weighted average of all the particles. The error is how far the answer
     is from where the AV really is.
   - The vertical axis is linear from 0 to 1 m, then logarithmic: above
     1 m, each grid line is ten times the one below it.
   - The heaviest cluster is within 1 m from the first niche match, at
     2.1 s, to the end of the drive. Before that it sits under the wrong
     light, about 300 m off.
   - The weighted average lands between the clusters: 120 to 170 m off
     until the second niche, at 14.1 s, then 12 to 21 m off while two places
     remain. It comes within 1 m only at 20.9 s, when the crowd is in one
     place. From then on the two lines overlap.

- **The crowd settles.** 23 clusters at the start, one per light. 4 after
  the first niche. The gaps between niches all differ, so each niche rules
  places out, and the crowd is in one place by 21 s.
- **How you read the answer matters.** The heaviest cluster is within a
  meter from about 2 s on. The weighted average stays 100 m or more off
  until the second niche, at 14.1 s, and over 10 m off until the crowd is
  in one place, at 20.9 s. While the belief has several peaks,
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
