====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L11, the slides shown in class,
   in the same order and with the same sections. You can read them at home.
   The deck links some slides to a **"More detail"** box on this page: a
   closed box right after the part it explains. Click its title to open it.
   Nothing in a "More detail" box is on the quiz.

   The hands-on commands are in the section "Hands-on: clone the expert,
   then run DAgger" below. The papers and pages behind these notes are on
   :doc:`the References page <l11_references>`.


.. _l11-lec-introduction:

Introduction
------------

Every earlier lecture built a driver from parts that people design, tune and
test one at a time: the stack of GP1 to GP4. Today builds a driver that
**learns from an expert**, and then asks how to compare the two.

Two ways to build a driver
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/stack_e2e.png
   :class: white-figure
   :alt: Two rows of boxes. Top row, titled Modular: the stack you built in GP1 to GP4: Sensors (L2), Perception (L4, L5), Localization (L6), Planning (L7, L8, L9), Control (L10), then Steering, throttle, brake, joined by arrows numbered 1 to 5. Bottom row, titled End-to-end: one network, learned from driving data: Sensors, one long blue box labeled One neural network, then Trajectory or steering, throttle, with the last arrow numbered 6.
   :width: 100%
   :align: center

   A modular stack and an end-to-end driver.

.. admonition:: Reading the figure
   :class: tip

   The top row is the stack you built, drawn as a chain to keep the picture
   simple. Each arrow carries something a person chose:

   - **Arrow 1:** images and LiDAR points.
   - **Arrow 2:** objects with tracks.
   - **Arrow 3:** the AV's pose and the objects on the map.
   - **Arrow 4:** a trajectory.
   - **Arrow 5:** the commands to the car.

   The bottom row is one network, learned from driving data. **Arrow 6**
   carries a trajectory or the commands, straight from the sensors, with no
   parts you can open one by one. Today is about the bottom row.

End-to-end driving, defined
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: End-to-end driving
   :class: note

   "We define end-to-end autonomous driving systems as fully differentiable
   programs that take raw sensor data as input and produce a plan and/or
   low-level control actions as output" (Chen et al., 2024).

- **Differentiable** means every part can be trained together, from the
  error at the output back to the sensors.
- **In your stack,** people chose what flows between the parts (boxes, a
  pose, a route) and tuned each part on its own score: detection on mAP
  (mean average precision), and the EKF (the Kalman filter that estimates
  the AV's pose) on its error.
- **In an end-to-end driver,** the network chooses what flows inside it, and
  one score at the output trains it all.

One lap, one expert, one clone: today's running example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The example is small on purpose, so that everything in it can be measured.

1. **The road:** one lap of CARLA's Town01, read from its map. GP4 drives
   Town01 too.
2. **The expert:** keeps the AV in its lane. It sees where the AV really is.
3. **The clone:** learns from a recording of the expert, then drives alone.
   It sees only what a noisy lane detector reports. That difference matters
   later.
4. **We measure:** how often each one finishes the lap on 20 test laps, and
   why the clone does not. A **training run** is one recording of the expert
   and the clone trained on it. We follow run 6, and compare it with nine
   other runs near the end of the DAgger section.

Everything runs in numpy on a laptop, with no CARLA server: the hands-on
script ``l11_handson.py`` reproduces the lap, fit, error and DAgger figures
on this page.

Learning objectives
~~~~~~~~~~~~~~~~~~~

After this lecture, you can:

- write **behavior cloning** as supervised learning and fit a small policy;
- explain, with measured numbers, why a clone with a small error on the
  expert's data leaves its lane: **compounding error**;
- run **DAgger**'s loop and say what it costs;
- say why a learned driver needs the route's **command** at a junction;
- place **TransFuser**, **UniAD** and driving **VLA models**: inputs,
  outputs, what is learned;
- tell an **open-loop** result from a **closed-loop** one;
- compare a **modular** stack with an **end-to-end** driver fairly.


.. _l11-lec-behavior-cloning:

Behavior Cloning
----------------

The Introduction gave two ways to build a driver, and today's lap, expert and
clone. This section builds on them: it trains the clone. Behavior cloning is
the simplest way to train an end-to-end driver, and every later method today
starts from it.

Behavior cloning, defined
~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Behavior cloning
   :class: note

   Learning a driving policy from an expert's recorded examples by supervised
   learning: each example pairs what the expert saw with what the expert did,
   and the policy is trained to give the expert's action for the expert's
   input. A **policy** is a rule from what the AV sees to what it does.

The idea is old:

- **1988, ALVINN:** a network that "takes images from a camera and a laser
  range finder as input and produces as output the direction the vehicle
  should travel". It was trained on simulated road images (Pomerleau, 1988).
- **2016, NVIDIA:** "We trained a convolutional neural network (CNN) to map
  raw pixels from a single front-facing camera directly to steering
  commands", from about 72 hours of driving (Bojarski et al., 2016).

Behavior cloning in four steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/bc_steps.png
   :class: white-figure
   :alt: Four boxes in a row joined by arrows. Step 1, outlined dark: the expert drives; we record. Step 2: pairs: what the AV saw, steering. Step 3: fit a policy: supervised learning. Step 4, outlined rust: the clone drives alone.
   :width: 100%
   :align: center

   Behavior cloning, from recording to driving.

.. admonition:: Reading the figure
   :class: tip

   - **Step 1:** the expert drives and we record.
   - **Step 2:** we build pairs: what the AV saw, and the steering the expert
     gave.
   - **Step 3:** we fit a policy to those pairs, by supervised learning.
   - **Step 4:** the clone drives alone.

Steps 1 to 3 are the same as training a detector: inputs, labels, a loss.

Step 4 is new. The trained policy's outputs move the AV, and the AV's new
position decides the next input. A detector's outputs never change its next
image. The whole lecture comes from this one difference.

The road: one lap of Town01
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/l11_lap.png
   :class: white-figure
   :alt: A top view of CARLA Town01's lanes as light gray dots, with the outer loop drawn as a thick dark line, a rounded rectangle about 395 m wide and 330 m tall. A dot on the top side tagged S marks the start, with an arrow pointing left: the lap runs counterclockwise. The four corners are tagged 1 to 4, starting top left. A small square on the bottom side near x 325 m is tagged J.
   :width: 70%
   :align: center

   One lap of Town01's outer loop.

.. admonition:: Reading the figure
   :class: tip

   The axes are the map's x (east) and y (north), in meters.

   - **The thick dark line** is the lap. **S** is the start, and the arrow
     shows the direction: counterclockwise.
   - **Tags 1 to 4** are the four left turns, starting at the top left.
   - **J** is a junction on the lap that the Commands section uses.
   - **The light gray dots** are the other lanes of the town.

The lap is read from ``Town01.xodr``, the town's map, every 0.5 m:

- one lap, counterclockwise from S: **1442.6 m**;
- four left turns; the sharpest has a radius of 9.8 m;
- the lane is 4.0 m wide.

**Chosen for this example:** 8 m/s (about 29 km/h), 20 steps per second, an
AV 2.0 m wide with a 2.9 m wheelbase. Nothing here is measured from a real
car.

A wheel leaves the lane when the AV's center is more than
(4.0 − 2.0) / 2 = 1.0 m from the lane center.

The expert steers for the curve, then back to the center
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two terms first. The **offset** is how far the AV's center is from the lane
center, with left positive. The **heading error** is the angle between the
AV and the lane. The expert's rule has three numbers, all chosen for this
example:

1. steer for the curve 2.4 m ahead (0.3 s at 8 m/s), as the road's curvature
   asks;
2. steer back 3.44° for every meter of offset;
3. steer back 0.8° for every degree of heading error.

.. figure:: /_static/images/L11/expert_drive.png
   :class: white-figure
   :alt: The expert's offset in meters against the distance along the lap, 0 to 1443 m. Dashed gray lines at plus and minus 1.0 m mark where a wheel leaves the lane. The dark line stays between about minus 0.5 and plus 0.5 m, with a short swing at each of the four turns, tagged 1 to 4 above the plot.
   :width: 95%
   :align: center

   The expert's offset along the lap.

.. admonition:: Reading the figure
   :class: tip

   The horizontal axis is the distance driven along the lap. The vertical
   axis is the offset, left positive.

   - **The dark line** is the expert. It stays within about half a meter and
     swings a little at each turn, tagged **1** to **4** above the plot.
   - **The dashed gray lines** at plus and minus 1.0 m are where a wheel
     leaves the lane.

Every driver also gets a random push on the steering, like wind gusts or the
slope of the road (chosen: 0.4°). Measured on 20 test laps, the expert
finishes **all 20**, and its largest offset is 0.75 m.

.. dropdown:: More detail: the AV's motion and the expert, as equations
   :class-container: more-detail
   :icon: info
   :name: l11-more-av-model

   **The state.** Three numbers describe the AV on the road: the distance
   along the lane :math:`s`, the offset :math:`e` (left positive) and the
   heading error :math:`\psi`. The other symbols are speed
   :math:`v` = 8 m/s, wheelbase :math:`L` = 2.9 m, the steering angle
   :math:`\delta`, the lane's curvature :math:`\kappa(s)` read from the map,
   and the time step :math:`\Delta t` = 0.05 s. Everything but
   :math:`\kappa` is chosen for this example.

   **The motion.** A kinematic bicycle model, written in lane coordinates:

   .. math::

      \dot s = \frac{v\cos\psi}{1 - \kappa e}, \qquad
      \dot e = v \sin\psi, \qquad
      \dot\psi = \frac{v}{L}\tan(\delta + g) - \kappa \dot s

   The term :math:`g` is the random push on the steering. It changes at
   every step: :math:`g \leftarrow a g + \sqrt{1 - a^2}\,\sigma_g\,\xi`, with
   :math:`a = e^{-\Delta t / 2\,\mathrm{s}}`, :math:`\sigma_g` = 0.4° and
   :math:`\xi` a new draw from a standard normal distribution (mean 0,
   spread 1).

   **The two drivers.**

   - The expert steers
     :math:`\delta^* = \arctan\!\big(L\,\kappa(s + 0.3\,v)\big) - 0.06\,e - 0.8\,\psi`.
     The first term steers for the curve 0.3 s ahead. The 0.06 rad per
     meter of offset is the 3.44° per meter on the slide
     (0.06 × 180 / π = 3.44).
   - The clone steers
     :math:`\delta = w_1 \hat e + w_2 \hat\psi + w_3 \kappa(s + 0.3\,v) + w_4`.
     It reads the lane detector's numbers, not the truth:
     :math:`\hat e = e + 0.35\,\xi_1` m and
     :math:`\hat\psi = \psi + 0.3^\circ\,\xi_2`, each with a new draw at every
     step. The weights :math:`w_1` to :math:`w_4` are set by training.

   **Two limits.** Steering is limited to ±30°, and a drive stops if the
   offset passes 1.6 m in either direction.

What the clone sees: a noisy lane detector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The expert reads the true offset and heading, as a simulator's autopilot can.
This is **privileged information**: a state only the simulator knows. The
clone gets what a camera's lane detector reports, with noise (chosen):

.. list-table::
   :header-rows: 1
   :widths: 32 32 36
   :class: compact-table

   * - Input
     - The expert reads
     - The clone reads
   * - Offset
     - the truth
     - the truth ± 0.35 m
   * - Heading error
     - the truth
     - the truth ± 0.3°
   * - Curvature ahead
     - the map
     - the map

The sign ± is the noise's standard deviation, drawn again at every step.

.. admonition:: The clone's policy
   :class: note

   Steering = :math:`w_1` × offset seen + :math:`w_2` × heading seen +
   :math:`w_3` × curvature + :math:`w_4`. Four weights, set by training.

Training: least squares on one recorded lap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Record:** the expert drives one lap: 1442.6 / 8 = 180.33 s. At 20 steps
   per second, 180.33 × 20 = 3606.6, so the recording holds 3607 pairs.
2. **Each pair:** the three numbers the detector reported, and the steering
   the expert gave.
3. **Fit:** choose :math:`w_1` to :math:`w_4` so that the policy's steering is
   as close as possible to the expert's, summed over the 3607 pairs: the
   smallest sum of squared differences (least squares).

This is supervised learning with a squared loss, the same kind of training as
a detector's box regression. Here the solution has a closed form, so there is
no gradient descent.

.. dropdown:: More detail: the least-squares solution
   :class-container: more-detail
   :icon: info
   :name: l11-more-least-squares

   Stack the :math:`N` = 3607 pairs in a table :math:`X`. Row :math:`k` of
   :math:`X` holds the numbers the clone read at step :math:`k`,
   :math:`[\hat e_k,\ \hat\psi_k,\ \kappa_k,\ 1]`, and :math:`y_k` is the
   expert's steering at that step. The last number, 1, is the input of the
   constant weight :math:`w_4`. Behavior cloning chooses the weights
   :math:`w = (w_1, w_2, w_3, w_4)` with the smallest sum of squared
   differences:

   .. math::

      w = \arg\min_{w} \sum_{k=1}^{N} \big(x_k^\top w - y_k\big)^2
      \quad\Longrightarrow\quad
      X^\top X\, w = X^\top y .

   - **Four unknowns, four equations.** The call ``numpy.linalg.lstsq(X, y)``
     solves them.
   - **DAgger solves the same equations.** Only :math:`X` and :math:`y` grow:
     they gain the states the clone reached, with the expert's labels for
     them.
   - **A neural network** replaces :math:`x^\top w` with a deeper function,
     and the closed form with gradient descent. The loss is the same.

The clone's weights, next to the expert's
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 52 16 16 16
   :class: compact-table

   * - Weight on
     - Expert
     - Clone
     - Ratio
   * - offset (deg of steering per m)
     - 3.44
     - 0.38
     - 0.11
   * - heading error (deg per deg)
     - 0.80
     - 0.74
     - 0.93
   * - curvature ahead (m; the expert's is the 2.9 m wheelbase)
     - 2.9
     - 2.58
     - 0.89

The ratio is the clone's weight divided by the expert's. For the offset,
0.38 / 3.44 = 0.11. The weights are those of training run 6.

The clone learned the curve and the heading nearly right, and the offset
about **9 times too weak** (3.44 / 0.38 = 9.05): it barely steers back toward
the center. The next section says why.

Scored on the expert's data, the clone looks good
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Open-loop error
   :class: note

   The policy's error on recorded inputs: it reads each recorded input and its
   output is compared with the expert's. Its outputs never move the AV.

On a second recorded expert lap, not used for training:

- the clone's steering differs from the expert's by **0.37°** on average;
- the steering the AV needs in a turn of radius 9.8 m is about
  arctan(2.9 / 9.8) = 16.5°, and 0.37° is 2% of that (0.37 / 16.5 = 0.022).

That looks like a very good clone.

The clone drives: a wheel leaves the lane after 649 m
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/bc_drive.png
   :class: white-figure
   :alt: Offset from lane center against distance along the lap, 0 to 1443 m. Dashed gray lines at plus and minus 1.0 m, tagged 1. A thin gray line, tagged 2, is the expert on the same test lap and stays within about 0.5 m. A rust line, tagged 3 beside its highest point near 1170 m, is the clone: it swings wider at each turn, drifts down to minus 1.0 m near 649 m, where a dark circle tagged 4 marks the first time a wheel leaves the lane, comes back, then drifts up to about plus 1.0 m near 1100 m and reaches plus 1.3 m at 1170 m.
   :width: 95%
   :align: center

   The clone's offset on one test lap.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** the dashed gray lines at plus and minus 1.0 m, where a wheel
     leaves the lane.
   - **Tag 2:** the expert on the same test lap, with the same gusts. It stays
     within about half a meter.
   - **Tag 3:** the clone, in rust. It swings wider than the expert at each
     turn and drifts. Its highest point, near 1170 m, reaches plus 1.3 m.
   - **Tag 4:** the dark circle near 649 m, the first time a wheel leaves the
     lane (the offset reaches minus 1.0 m).

**Measured on 20 test laps** (new gusts and new detector noise on each), the
clone finishes **5**. On average it drives 56% of the lap before a wheel
leaves (a lap that finishes counts as 100%). The lap in the figure is the
median of the 15 failures.

This is one training run, one recorded lap. Another recording gives another
count, and the DAgger section shows ten of them: they finish 2 to 9 laps of
20. A clone that was within 0.37° of the expert on recorded data finishes 5
laps of 20. That gap is what the next section explains.


.. _l11-lec-compounding-error:

Compounding Error
-----------------

Behavior Cloning gave a clone that copies the expert within 0.37° and
finishes 5 of 20 laps. This section builds on that clone and the same 20 test
laps. It measures why small errors grow once the clone drives. What it shows
is what a good score on recorded data does not show.

Where the error grows
~~~~~~~~~~~~~~~~~~~~~

The clone's steering error is not the same everywhere: it depends on how far
the AV is from the lane center. This part measures that, and shows where the
clone drives.

The clone's error grows with the offset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L11/error_vs_offset.png
   :class: white-figure
   :alt: Bar chart. The average size of the clone's steering error, in degrees, for four ranges of how far the AV really is from the lane center: 0.00 to 0.25 m, 0.44; 0.25 to 0.50 m, 1.09; 0.50 to 0.75 m, 1.78; 0.75 to 1.00 m, 2.41.
   :width: 75%
   :align: center

   The clone's steering error against the AV's true offset.

.. admonition:: Reading the figure
   :class: tip

   Each bar groups the steps of the clone's 20 test laps by how far the AV
   really was from the lane center. Its height is the average size of the
   clone's steering error in those steps, in degrees.

   - **0.00 to 0.25 m:** 0.44°.
   - **0.25 to 0.50 m:** 1.09°.
   - **0.50 to 0.75 m:** 1.78°.
   - **0.75 to 1.00 m:** 2.41°.

We took the clone's 20 test laps and, at every step, compared the
clone's steering with what the expert would have steered in that same state. Near the
center the clone is off by 0.44°. At 0.75 m to 1.00 m, it is off by 2.41°,
5.5 times more (2.41 / 0.44 = 5.48). The clone is worst exactly where it
needs to be best.

Step by step: how a small error compounds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Near the center the clone is off by 0.44°: it steers back too little, so a
   gust or a turn pushes it a little farther out than the expert.
2. Farther out, the expert would steer back harder (3.44° per meter). The
   clone adds only 0.38° per meter. Its error grows: 1.09° between 0.25 and
   0.50 m.
3. A larger error pushes it farther out, where the error is larger again:
   1.78°, then 2.41°.
4. Each step starts from where the last one left the AV, so the errors add up
   instead of averaging out. A wheel leaves the lane.

.. admonition:: Definition: Compounding error
   :class: note

   The policy's own mistakes take it to states its training data did not
   cover, where it makes larger mistakes. In open loop this cannot happen: the
   next input is the recorded one, whatever the policy said.

The clone drives where the expert never was
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L11/coverage.png
   :class: white-figure
   :alt: Two histograms of the true offset from the lane center, from minus 1.6 to plus 1.6 m. Tagged 1, dark: the expert's recorded lap, a narrow peak around zero, almost all within plus or minus 0.3 m. Tagged 2, rust: the clone's 20 test laps, wide and flat, spread from about minus 1.4 to plus 1.4 m.
   :width: 75%
   :align: center

   Where the expert and the clone spend their time.

.. admonition:: Reading the figure
   :class: tip

   The horizontal axis is the true offset from the lane center (left
   positive). The vertical axis is the share of time steps, as a density.

   - **Tag 1, dark:** the expert's recorded lap, which is the training data.
     It is a narrow peak around zero.
   - **Tag 2, rust:** the clone on its 20 test laps. It is wide and flat.

In the training data the true offset has a standard deviation of 0.15 m and
never passes 0.61 m. The clone spends **20%** of its time beyond 0.61 m. For
those states the clone has no example at all.

Why the weight is small
~~~~~~~~~~~~~~~~~~~~~~~

The clone's weight on the offset is 9 times too weak. This part finds the
cause, tests whether more data fixes it, and states the general result.

Why the offset weight is too small: the noise hides the offset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L11/bc_fit.png
   :class: white-figure
   :alt: Scatter plot of steering in degrees against the offset the detector reports, in meters, for the expert's lap on straight road. The gray points, tagged 3, form a flat cloud from about minus 1.2 to plus 1.3 m wide and about 2 degrees tall, with a few points higher up. A dark line, tagged 1, falls steeply from plus 4.5 degrees at minus 1.3 m to minus 4.5 at plus 1.3 m. A rust line, tagged 2, through the middle of the cloud is almost flat.
   :width: 75%
   :align: center

   The recorded pairs, the expert's rule and the clone's fit.

.. admonition:: Reading the figure
   :class: tip

   Each gray dot is one recorded pair on straight road: the offset the
   detector reported (horizontal) and the steering the expert gave (vertical).

   - **Tag 1, dark:** the expert's rule, 3.44° per meter. It falls steeply.
   - **Tag 2, rust:** the clone's fit, 0.38° per meter. It is almost flat.
   - **Tag 3:** the recorded pairs. They form a flat cloud.

Why is the fit flat?

1. The expert stays near the center: its true offset varies by 0.15 m.
2. The detector adds noise of 0.35 m, more than twice that
   (0.35 / 0.15 = 2.3).
3. So most of the spread in "offset seen" is noise, and the expert's steering
   does not follow noise. The cloud is flat, and a line fit to a flat cloud
   is flat.

The clone is not at fault. Given these pairs, a flat line is the best fit.

.. dropdown:: More detail: how much the noise shrinks the weight, by hand
   :class-container: more-detail
   :icon: info
   :name: l11-more-noise-shrinks-weight

   Take one input :math:`x`, seen through noise :math:`n` that is
   independent of :math:`x`. Least squares on the noisy reading
   :math:`\hat x = x + n` shrinks the true slope by the share of the spread
   that is real:

   .. math::

      \text{factor} = \frac{\sigma_x^2}{\sigma_x^2 + \sigma_n^2}.

   **On the expert's lap (training run 6):**

   1. The true offset's spread is :math:`\sigma_x` = 0.154 m, measured on the
      recorded lap. The detector's noise is :math:`\sigma_n` = 0.35 m, chosen
      for this example.
   2. Factor: :math:`0.154^2 / (0.154^2 + 0.35^2) = 0.0237 / (0.0237 + 0.1225)
      = 0.162`.
   3. Predicted weight: 3.44 × 0.162 = 0.56° per meter.
   4. Fitted weight: 0.38° per meter. The one-input formula is a rough guide:
      the fit has four inputs, and on curves the heading and the curvature
      take part of the offset's share.

   **With a quieter detector of 0.117 m** (0.35 / 3, chosen for this
   example): :math:`0.0237 / (0.0237 + 0.0137) = 0.63`. Predicted weight:
   3.44 × 0.63 = 2.2° per meter. Fitted weight: 1.85°.

More of the same data does not fix it; a quieter detector does
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each clone is trained on the same recorded lap (training run 6) and tested on
the same 20 laps:

.. list-table::
   :header-rows: 1
   :widths: 40 15 25 20
   :class: compact-table

   * - Training data
     - Pairs
     - Offset weight (deg/m)
     - Laps finished
   * - 1 expert lap, detector 0.35 m
     - 3607
     - 0.38
     - 5 of 20
   * - 5 expert laps, detector 0.35 m
     - 18,035
     - 0.42
     - 6 of 20
   * - 1 expert lap, detector 0.117 m
     - 3607
     - 1.85
     - 20 of 20

- Five times the data moves the weight from 0.38 to 0.42, and the laps from 5
  to 6. The ten runs in the DAgger section show that a new recording alone
  moves the count by several laps (2 to 9), so 5 to 6 is not a change we can
  read. The extra laps stay near the center too, so they add more of the same
  states.
- A detector three times quieter (0.35 / 3 = 0.117) lets the fit see the
  offset.

.. dropdown:: More detail: an early fix, add recoveries to the data
   :class-container: more-detail
   :icon: info
   :name: l11-more-early-fix

   If the expert never drifts, the data has no example of a recovery. Early
   work made the examples up: it showed the network drifted views, with the
   steering that corrects them.

   - **1990, Pomerleau:** "each original image is shifted and rotated in
     software to create 14 additional images". He wrote that "Using
     transformed training patterns allows the network to learn how to recover
     from driving errors" (Pomerleau, 1990).
   - **2016, NVIDIA:** "The network must learn how to recover from mistakes.
     Otherwise the car will slowly drift off the road." "Images for two
     specific off-center shifts can be obtained from the left and the right
     camera" (Bojarski et al., 2016).

   Both make up off-center states from the expert's own drive. The label for
   a shifted view must be made up too (how hard to steer back): the expert
   never gave it. DAgger, below, takes another way: it records the states the
   clone really reaches, and asks the expert for the label.

The general result: mistakes can grow with the square of the time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ross and Bagnell (2010) bound behavior cloning's total cost over a drive of
:math:`T` steps:

- :math:`\varepsilon` is how often the policy makes a mistake on states the
  **expert** visits (the open-loop error rate).
- The bound is a cost that "grows quadratically :math:`O(T^2)` in the task
  horizon :math:`T` rather than as :math:`O(T)`".
- In words: one mistake can take the policy off the expert's states, and from
  there it may keep making mistakes for the rest of the drive.

.. admonition:: A worst case
   :class: note

   **The bound is a worst case,** not a curve our lap must follow. What our
   lap shows is the mechanism: a 0.37° open-loop error, and 15 of 20 test
   laps lost.

.. dropdown:: More detail: behavior cloning's bound, as the paper states it
   :class-container: more-detail
   :icon: info
   :name: l11-more-bc-bound

   **The symbols.** :math:`T` is the number of steps. :math:`J(\pi)` is a
   policy's total cost over :math:`T` steps, with a cost of at most 1 per
   step. :math:`\pi^*` is the expert and :math:`\hat\pi` is the clone.
   :math:`e_{\hat\pi}(s)` is the clone's 0-1 loss in state :math:`s`: 1 if it
   does not act as the expert would, 0 if it does. :math:`d_{\pi^*}` is the
   distribution of states the expert visits.

   **The theorem** (Theorem 2.1 in Ross and Bagnell, 2010): "Let
   :math:`\hat\pi` be such that :math:`E_{s\sim d_{\pi^*}}[e_{\hat\pi}(s)] \le
   \varepsilon`. Then :math:`J(\hat\pi) \le J(\pi^*) + T^2\varepsilon`."

   In plain words: if the clone's average mistake rate on the expert's own
   states is at most :math:`\varepsilon`, its total cost is at most the
   expert's plus :math:`T^2\varepsilon`.

   **Why** :math:`T^2`. The authors write: "as soon as :math:`\hat\pi` makes a
   mistake, it could end up in new states that were not visited by
   :math:`\pi^*`, and always incur maximal cost of 1 at each step from then
   on". They also write that "this bound is tight".

   **In mistakes, not cost.** The DAgger paper puts the same result as "as
   many as :math:`T^2\varepsilon` mistakes in expectation" (Ross, Gordon and
   Bagnell, 2011).

Check: compounding error
^^^^^^^^^^^^^^^^^^^^^^^^

**Question.** A team trains a lane-keeping clone. On a held-out recorded lap
its steering is within 0.2° of the human driver's. They propose to skip
closed-loop testing. What do you tell them?

.. dropdown:: Answer
   :class-container: sd-border-success

   The 0.2° is measured on the human's states only. Once the clone drives, it
   reaches states the recording does not have, where its error is unknown.
   Our clone had 0.37° open loop and finished 5 laps of 20. Only a
   closed-loop test measures that.


.. _l11-lec-dagger:

DAgger
------

Compounding Error gave the cause: the clone fails in states the expert's
recording never shows. This section uses that cause: it adds those states to
the data. DAgger records the states the clone reaches, and asks the expert
what to do there. The result is a training loop whose data covers the states
the clone will drive in.

DAgger: let the clone drive, ask the expert
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/dagger_loop.png
   :class: white-figure
   :alt: A loop of four boxes. A box on the left, Start: behavior cloning, points to Step 1, outlined rust: the newest clone drives one lap. Step 1 points right to Step 2, outlined dark: the expert labels every state it reached. Step 2 points down to Step 3: add the pairs to all the data so far. Step 3 points left to Step 4, outlined green: refit the clone on all the data. Step 4 points up to Step 1.
   :width: 86%
   :align: center

   The DAgger loop.

.. admonition:: Reading the figure
   :class: tip

   DAgger starts from behavior cloning, then loops.

   - **Step 1, rust:** the newest clone drives one lap.
   - **Step 2, dark:** the expert labels every state the clone reached.
   - **Step 3:** we add those pairs to all the data so far.
   - **Step 4, green:** we refit the clone on all of it, and go back to
     step 1.

DAgger ("dataset aggregation") is from Ross, Gordon and Bagnell (2011). The
paper's algorithm has two key lines: "Aggregate datasets: :math:`D \leftarrow
D \cup D_i`" and "Train classifier :math:`\hat\pi_{i+1}` on :math:`D`".
:math:`D` is all the labeled pairs so far, and :math:`D_i` the pairs from
iteration :math:`i`.

Who drives and who labels, in each iteration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In iteration :math:`i` the paper drives with a mix: "Let :math:`\pi_i =
\beta_i \pi^* + (1 - \beta_i)\hat\pi_i`" (Ross, Gordon and Bagnell, 2011).

- :math:`\pi_i` is the driver in iteration :math:`i`, :math:`\pi^*` is the
  expert, :math:`\hat\pi_i` is the clone after :math:`i - 1` refits, and
  :math:`\beta_i` is the share of steps the expert drives.
- **Our choice:** :math:`\beta_1 = 1` (iteration 1 is the expert's lap:
  behavior cloning), then :math:`\beta_i = 0` (the clone drives alone).
- **Labels:** always the expert's, whoever drove. The AV executes the clone's
  steering, and the data stores the expert's.

So the data now holds the states the clone itself reaches. The next fit is
judged on the states where the last clone made its mistakes.

After five DAgger laps, the data covers the drift
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/dagger_coverage.png
   :class: white-figure
   :alt: Two histograms of the true offset in the labeled data. Tagged 1, dark, small: the expert's lap alone, 3607 steps, narrow around zero. Tagged 2, green, tall: all data after iteration 6, 21642 steps, wider, from about minus 1.1 to plus 1.3 m.
   :width: 66%
   :align: center

   The labeled data before and after five DAgger laps.

.. admonition:: Reading the figure
   :class: tip

   The horizontal axis is the true offset (left positive). The vertical axis
   is the number of labeled time steps.

   - **Tag 1, dark:** the expert's lap alone (iteration 1). It is small and
     narrow around zero.
   - **Tag 2, green:** all the data after iteration 6, which is the expert's
     lap and five DAgger laps. It is taller and wider.

- Labeled states: 3607 × 6 = 21,642 (each lap is 3607 steps; the clone did not
  run off the road in the five DAgger laps).
- True offset beyond 0.5 m: 2.0% of the expert's lap, 10.8% of all the data.
  The spread grows from 0.15 m to 0.29 m.

Now the training data contains the drift.

Iteration by iteration: laps finished and the offset weight
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/dagger_iters.png
   :class: white-figure
   :alt: Two line plots against DAgger iteration 1 to 6, iteration 1 being behavior cloning, drawn as a rust dot. Left: test laps finished, of 20: 5 at iteration 1 (tagged 1), 16 at iteration 2, then 19 at iterations 3 to 6; a dashed dark line at 20 is the expert, tagged 2. Right: steer back per meter of offset, in degrees: 0.38 at iteration 1, 1.44 at iteration 2, 1.54 at iteration 3, then slowly down to 1.32 at iteration 6; a dashed dark line at 3.44 is the expert, tagged 2.
   :width: 100%
   :align: center

   Test laps finished and the offset weight, by DAgger iteration.

.. admonition:: Reading the figure
   :class: tip

   Both plots have the DAgger iteration on the horizontal axis. Iteration 1
   is behavior cloning (the rust dot).

   - **Left plot:** test laps finished, out of 20. Tag **1** marks the first
     rise, from behavior cloning to the first DAgger lap. Tag **2** is the
     expert, at 20.
   - **Right plot:** the weight on the offset, in degrees of steering back
     per meter. Tag **2** is the expert, at 3.44.

One DAgger lap lifts the clone from 5 to 16 finished laps, and the second to
19, where it stays. The offset weight goes from 0.38° per meter to 1.44 after
one lap, peaks at 1.54, and ends at 1.32. It stays well below the expert's
3.44: the detector's noise still hides part of the offset. But the weight is
now strong enough to keep the lane.

Ten training runs: the result is not luck
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/seeds.png
   :class: white-figure
   :alt: Dot plot of test laps finished, of 20, for ten training runs numbered 1 to 10. Rust circles, tagged 1, for behavior cloning: 5, 8, 4, 9, 4, 5, 6, 7, 3 and 2. Green squares, tagged 2, for DAgger after iteration 6: 19 in every run.
   :width: 75%
   :align: center

   Laps finished in ten training runs.

.. admonition:: Reading the figure
   :class: tip

   Each run records a new expert lap and new DAgger laps. All clones are
   tested on the same 20 laps.

   - **Tag 1, rust circles:** behavior cloning, from 2 to 9 laps of 20.
   - **Tag 2, green squares:** DAgger after iteration 6, 19 laps in every run.

Run 6, the one we followed, finished 5 with behavior cloning and 19 with
DAgger.

- Behavior cloning finishes 2 to 9 laps of 20 over the ten runs (the median
  is 5). DAgger finishes 19 in every run.
- DAgger always misses test lap 8. The expert's own largest offset, 0.75 m
  (the limit is 1.0 m), is on that lap, so it is the hardest lap.

So the gap between behavior cloning and DAgger is not luck. The spread among
behavior cloning runs is large, which is why one run alone says little.

What DAgger costs
~~~~~~~~~~~~~~~~~

1. **An expert who can label any state.** A program that reads the
   simulator's state can. A human must say what they would steer in a state
   they did not drive, often from a recording, after the fact.
2. **A place for a bad clone to drive.** The first DAgger lap is driven by the
   behavior-cloned clone, which left its lane on 15 of 20 test laps. Such laps
   belong in a simulator, or with a safety driver.
3. **A guarantee with conditions.** The paper's bound is linear in :math:`T`,
   where behavior cloning's was quadratic, under conditions on the expert's
   ability to recover and on the class of policies.

.. dropdown:: More detail: DAgger's guarantee and its conditions
   :class-container: more-detail
   :icon: info
   :name: l11-more-dagger-guarantee

   **The theorem** (Theorem 3.2 in Ross, Gordon and Bagnell, 2011): "if
   :math:`N` is :math:`\tilde O(uT)` there exists a policy
   :math:`\hat\pi \in \hat\pi_{1:N}` s.t. :math:`J(\hat\pi) \le J(\pi^*) +
   uT\varepsilon_N + O(1)`."

   **The symbols:**

   - :math:`N` is the number of DAgger iterations, and
     :math:`\hat\pi_{1:N}` is the set of clones they produce.
   - :math:`u` is how much one wrong action can cost the expert afterward,
     when the expert takes over. An expert that recovers quickly has a small
     :math:`u`.
   - :math:`\varepsilon_N` is the error of the best policy in the class, on
     all the states the clones visited.
   - :math:`T` and :math:`J` are as in the bound for behavior cloning.

   **What it says.** The extra cost grows linearly in :math:`T`, against
   :math:`T^2` for behavior cloning, when :math:`u` and :math:`\varepsilon_N`
   are small. Both are conditions, and our example meets them only in part.
   The clone is a linear policy, and it cannot copy the expert exactly through
   the detector's noise, so :math:`\varepsilon_N` is not zero. That shows in
   the offset weight, which stopped at 1.32° per meter against the expert's
   3.44°.

Hands-on: clone the expert, then run DAgger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the course's Python repo, folder ``lecture11``
(`README <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture11>`__),
five parts. Everything runs on a laptop with numpy and matplotlib, without
CARLA:

.. code-block:: bash

   python3 l11_handson.py --part road     # the lap and the expert
   python3 l11_handson.py --part bc       # fit, then drive
   python3 l11_handson.py --part shift    # error by offset
   python3 l11_handson.py --part dagger   # DAgger, slider
   python3 l11_handson.py --part eval     # open vs closed loop

The options ``--detector-noise`` (meters, default 0.35), ``--gust``
(degrees, default 0.4), ``--seed`` (the expert's recorded lap and DAgger's
laps, default 6, the run in these notes) and ``--iterations`` (default 6)
change the example. The ``bc`` part prints the offset weight, in degrees of
steering back per meter of offset, for the expert and the clone.

Try three things:

1. Run ``--part bc`` with ``--detector-noise 0.1``. Does the clone keep the
   lane? What happened to the offset weight?
2. Run ``--part dagger`` with ``--gust 0.6``. How many laps does the expert
   finish? And DAgger?
3. Change ``--seed`` (the default is 6). Which numbers move, and by how much?
   This is how you see the spread for yourself.


.. _l11-lec-commands:

Commands
--------

DAgger gave a lane keeper that finishes 19 of 20 laps. This section keeps the
same road and sets the four weights aside: they see only the offset and the
curve, and at a junction the image cannot say which way to turn. So it adds an
input the clone lacks. The question is what a learned driver needs at a
junction, so that it follows the route your planner chose.

At junction J, the image does not say which way to go
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Junction J is on our lap, but our lap only goes straight through it. So
suppose the recording held expert drives both ways through J, half going
straight and half turning left. The camera sees the same junction each time.

.. figure:: /_static/images/L11/junction.png
   :class: white-figure
   :alt: Top view of junction J in Town01, about 60 m across. The AV, drawn as a car facing right, sits in a gray lane coming from the left. The lane goes straight on to the right, its centerline a solid dark line tagged 1, and also turns left and up, its centerline a dashed dark line tagged 2. A rust arc, tagged 3, starts where the lanes split and curves up between them, through the corner, missing both lanes.
   :width: 60%
   :align: center

   Junction J: straight on, left, and the average of the two.

.. admonition:: Reading the figure
   :class: tip

   The axes are the map's x (east) and y (north), in meters. The AV comes
   from the left.

   - **Tag 1, solid dark line:** the center line of the lane that goes
     straight on.
   - **Tag 2, dashed dark line:** the center line of the lane that turns left.
   - **Tag 3, rust arc:** the path of a clone fit to both drives. It starts
     where the lanes split and curves up between them, through the corner,
     and misses both lanes.

1. **Straight:** the expert steers 0°.
2. **Left:** the turn's radius is 10.9 m (17.1 m of arc for 90°), so the
   expert steers arctan(2.9 / 10.9) = 14.9°.
3. **A clone fit to both** by least squares gives about the average:
   14.9 / 2 = 7.45°, a circle of radius 2.9 / tan(7.45°) = 22.2 m. After 34 m
   (a length chosen for this example) it is 9.1 m from the nearest point of
   the left lane's center line, measured on the map.

Codevilla et al. (2018) say it the same way: "when a car approaches an
intersection, the camera input is not sufficient to predict whether the car
should turn left, right, or go straight".

Conditional imitation: the route's command picks the head
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The fix is to tell the network which way to go.

.. figure:: /_static/images/L11/cil_branches.png
   :class: white-figure
   :alt: A diagram. Camera image and Speed feed a blue box, Shared layers. From it, four blue boxes: Follow lane head, Left head, Straight head, Right head. Only the Straight head connects to the output box, Steering, throttle, brake. A dashed arrow from a box below, Command from the route: Straight, points up to that connection, labeled picks the Straight head.
   :width: 84%
   :align: center

   A conditional imitation network with one head for each command.

.. admonition:: Reading the figure
   :class: tip

   - **Shared layers:** the camera image and the speed go in. These first
     layers are used for every command.
   - **Four heads:** follow lane, left, straight and right. Each head is a
     small part of the network that produces the steering, throttle and brake
     for one command.
   - **The dashed arrow:** the command from the route, here "Straight", picks
     which head connects to the output. The other three heads are not used at
     that moment.

Codevilla et al. (2018) use "a set of four commands: continue (follow the
road), left (turn left at the next intersection), straight (go straight at the
next intersection), and right". The command "acts as a switch that selects
between specialized sub-modules". The route planner supplies the command, and
that is how a learned driver follows the route your planner chose.

CARLA's Leaderboard, which has since closed (CARLA Team, 2026), gave every
agent its route with these commands. For example, ``RoadOption.LEFT`` means
"Turn left at the intersection" (CARLA Team, 2026).

.. dropdown:: More detail: other shortcuts a clone can learn
   :class-container: more-detail
   :icon: info
   :name: l11-more-shortcuts

   A clone can learn a shortcut that works on the recording and fails on the
   road. Two published cases:

   - **Causal confusion** (de Haan, Jayaraman and Levine, 2019). With more
     inputs, the clone can learn the wrong cause. Their example: the
     dashboard has a light that comes on as soon as the brake is pressed. A
     model that sees the light learns to brake only when the light is on,
     which gets the cause backward. The light follows the braking and does not
     cause it. They found that "access to more information can yield worse
     performance".
   - **Behavior cloning in CARLA** (Codevilla et al., 2019). The authors
     confirm known limits of behavior cloning (the data is biased, and the
     network fits it too closely), new problems that come from moving objects
     and from having no model of cause and effect, and training that is
     unstable. One failure is "the inertia problem": cars that are stopped in
     the data stay stopped, so the clone stops too often and has trouble
     starting again.

   Our clone's weakness was in what it could see (the detector's noise).
   These two are in what it chose to look at. Both pass an open-loop test.


.. _l11-lec-architectures:

Architectures
-------------

Commands gave a learned driver that follows the route. This section keeps the
idea, imitation with a command, and sets aside the four-weight clone and the
lap. Two published drivers are far bigger than that. We look at TransFuser and
UniAD at the level of their blocks, to see which parts of your stack such a
network replaces, and which it keeps.

TransFuser: camera and LiDAR fused by attention, then waypoints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/transfuser.png
   :class: white-figure
   :alt: A diagram. Camera image feeds a row of four blue conv boxes; LiDAR, seen from above, feeds a second row of four conv boxes. Between each pair, a blue attn box exchanges with both rows. Both rows end in a blue Waypoint predictor box, which sends waypoints to a gray box, Two PID controllers, which outputs steering, throttle, brake. A note says learned (blue): trained by imitation.
   :width: 100%
   :align: center

   TransFuser, at the level of its blocks.

.. admonition:: Reading the figure
   :class: tip

   - **conv:** convolution layers. The top row reads the camera image, and
     the bottom row reads the LiDAR points seen from above.
   - **attn:** attention, the building block of transformers. Between each
     pair of conv boxes it lets the two branches exchange features. The
     figure shows four pairs, at four resolutions.
   - **Waypoint predictor:** both branches end in it. Everything in blue is
     trained by imitation.
   - **Two PID controllers (gray):** they turn the waypoints into steering,
     throttle and brake. This last step is not learned.

The authors' aim is "to integrate image and LiDAR representations using
attention", in "an auto-regressive waypoint prediction framework" (Prakash
et al., 2021). They also write: "We use two PID controllers for lateral and
longitudinal control". A PID controller turns a target into steering or
throttle by feedback on its error. They are the same kind of controllers you
built.

TransFuser was tested closed loop in CARLA, on the CARLA Leaderboard, which
has since closed (Chitta et al., 2023).

UniAD: the stack's modules, inside one network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/uniad.png
   :class: white-figure
   :alt: A diagram. Several cameras feed a blue box, Bird's-eye features, then a row of blue boxes joined by blue arrows: Track (L5), Map, Motion (L8), Occupancy (L5), Planner (L9), then the output AV's future waypoints. A brace above the five modules reads one network: every part trained together, toward planning.
   :width: 100%
   :align: center

   UniAD, at the level of its blocks.

.. admonition:: Reading the figure
   :class: tip

   - **Several cameras** give bird's-eye features: a top-down grid of what the
     cameras saw.
   - **The five blue modules** do the jobs of your stack: tracking, mapping,
     motion forecasting, occupancy and planning. The labels under four of
     them name the lecture that covered the same job in your stack.
   - **The brace** says all five are one network, trained together, toward
     planning.
   - **The output** is the AV's future waypoints.

UniAD "incorporates full-stack driving tasks in one network". "Tasks are
communicated with unified query interfaces to facilitate each other toward
planning" (Hu et al., 2023). A **query** is a learned vector that collects
what one module needs from the bird's-eye features. It replaces the
hand-designed message between two parts.

UniAD won Best Paper at CVPR 2023 (CVPR 2023). Its planning is scored open
loop, on recorded nuScenes drives (Zhai et al., 2023). The Evaluation section
comes back to this.

Your stack and UniAD, part by part
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 40 40
   :class: compact-table

   * -
     - Your stack (GP1 to GP4)
     - UniAD
   * - Between parts
     - ROS topics you defined: boxes, a pose, a path
     - learned queries
   * - Trained or tuned
     - each part on its own score
     - all parts together, with the planning loss
   * - When it fails
     - read each topic to find the part
     - each module's output can be read out; the queries are vectors, not
       messages a person reads
   * - Data it needs
     - labels for each part
     - labels for every module, and driving

UniAD keeps your stack's tasks and their names. What it removes is the
hand-designed message between them.


.. _l11-lec-vla:

VLA
---

Architectures gave end-to-end networks that output waypoints. This section
builds on them: it adds language, in and out. These are models that also read
and write text: vision-language-action (VLA) models. We see what they add, and
what they cost in time.

Vision-language-action models, defined
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Vision-language-action model (VLA)
   :class: note

   A vision-language model (one that reads images and text and writes text)
   trained to output actions too: "we express the actions as text tokens and
   incorporate them directly into the training set of the model in the same
   way as natural language tokens. We refer to such category of models as
   vision-language-action models (VLA)" (Brohan et al., 2023).

- The term comes from RT-2, a robot manipulation model (2023).
- For driving, the action is a trajectory, written as numbers in text, and the
  model can also write why.

Four driving VLAs, from their papers and pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are claims by the makers, so the table quotes their words instead of
describing the models.

.. list-table::
   :header-rows: 1
   :widths: 18 82
   :class: compact-table

   * - Model
     - What its authors report
   * - DriveVLM
     - "reasoning modules for scene description, scene analysis, and
       hierarchical planning"; a dual version deployed "on a production
       vehicle" (Tian et al., 2025)
   * - EMMA (Waymo)
     - built on "a multi-modal large language model foundation like Gemini";
       outputs "trajectories and 3D locations" "as natural language text".
       Limits it lists: "up to 4" frames, no LiDAR or radar, more compute
       (Hwang et al., 2025)
   * - LINGO-2 (Wayve)
     - "the first closed-loop vision-language-action driving model (VLAM)
       tested on public roads", driving in Central London (Wayve, 2024)
   * - Alpamayo 1 (NVIDIA)
     - named Alpamayo-R1 in its paper: "integrates Chain of Causation
       reasoning with trajectory planning" (NVIDIA, 2025); open weights,
       "ready for non-commercial use" (NVIDIA, model card). NVIDIA's newer
       Alpamayo 2 Super has its own model card.

A slow model needs a fast partner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L11/vla.png
   :class: white-figure
   :alt: A diagram. Camera images and Text: route, question feed a blue box, Vision-language model, marked slow: about 0.4 s per answer. It writes two outputs: Text out: what it sees and plans; and Coarse trajectory, written as numbers, which goes to a box Fast planner refines it, marked fast: every control step.
   :width: 90%
   :align: center

   A vision-language model and a fast planner.

.. admonition:: Reading the figure
   :class: tip

   - **Inputs (left, gray):** camera images, and text with the route and a
     question.
   - **Vision-language model (blue):** slow, about 0.4 s per answer. It writes
     two outputs.
   - **Text out:** what it sees and plans, in words.
   - **Coarse trajectory:** a rough path, written as numbers. A **fast
     planner** refines it at every control step.

A VLA writes text, and writing is slow. Three numbers show what that costs at
our 8 m/s:

1. DriveVLM's vision-language model, on an NVIDIA OrinX chip in the car, has
   "an average inference speed of 410 ms" (Tian et al., 2025). The AV drives
   0.41 × 8 = 3.3 m per answer.
2. Alpamayo 1 reports 99 ms on an NVIDIA RTX 6000 Pro Blackwell (NVIDIA,
   2025): 0.099 × 8 = 0.8 m.
3. Our lane keeper steers every 0.05 s: 0.05 × 8 = 0.4 m.

These times are the authors' reports, on different chips, not a comparison of
the two models. DriveVLM-Dual hands its trajectory to "a classical planner for
high-frequency trajectory refinement" (Tian et al., 2025).


.. _l11-lec-evaluation:

Evaluation
----------

VLA gave the newest models. This section uses our lap's numbers again, and
applies what they show to published results. It covers how learned drivers are
scored: open loop against closed loop, and two benchmarks. That is what you
need to read any result, and to score your own GP4 drives.

Open loop and closed loop
~~~~~~~~~~~~~~~~~~~~~~~~~

The same driver can score well in one and badly in the other. This part
defines both, shows it on our lap, and shows it on a published benchmark.

Closed-loop evaluation, defined
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Closed-loop evaluation
   :class: note

   The policy drives: its outputs move the AV, and the AV's new state gives the
   next input. It is scored on what happens: route completed, collisions,
   rules broken.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40
   :class: compact-table

   * -
     - Open loop
     - Closed loop
   * - Next input
     - the recorded one
     - the result of the policy's own action
   * - Score
     - average error against the expert's output (steering in degrees, or
       distance in meters)
     - share of the route completed, infractions
   * - Needs
     - a dataset
     - a simulator, or a car
   * - Our clone
     - 0.37°
     - 5 laps of 20

Our lap: the better open-loop score loses in closed loop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L11/open_closed.png
   :class: white-figure
   :alt: Two bar charts. Left, open loop on the expert's recorded lap, mean clone minus expert steering in degrees: bar 1, rust, 0.37; bar 2, green, 0.47. Right, closed loop, test laps finished of 20: bar 1, rust, 5; bar 2, green, 19; bar 3, dark, 20.
   :width: 100%
   :align: center

   The same drivers, scored open loop and closed loop.

.. admonition:: Reading the figure
   :class: tip

   Bar **1** is behavior cloning, bar **2** is DAgger after iteration 6, and
   bar **3** is the expert.

   - **Left, open loop:** the error on a second recorded lap of the expert,
     not used for training: behavior cloning 0.37°, DAgger 0.47°. Behavior
     cloning looks better.
   - **Right, closed loop:** test laps finished, out of 20: behavior cloning
     5, DAgger 19, the expert 20. Behavior cloning is much worse.

Behavior cloning has the **lower** open-loop error in all 10 training runs,
and the fewer finished laps in all 10. It fits the expert's own states best.
DAgger's fit also covers the states where the AV drifts, so on the expert's
states alone it fits slightly worse.

nuScenes: a model without cameras scores as well
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The same effect appears in a published benchmark. AD-MLP (Zhai et al., 2023)
plans from the AV's own past motion and the route command, "without using any
perception or prediction information such as camera images or LiDAR". Their
Table 1, nuScenes, open loop, averaged over 1, 2 and 3 s:

.. list-table::
   :header-rows: 1
   :widths: 36 19 23 22
   :class: compact-table

   * - Planner
     - Cameras
     - Average distance error (m)
     - Collision (%)
   * - UniAD
     - yes
     - 1.03
     - 0.31
   * - VAD-Base
     - yes
     - 0.37
     - 0.14
   * - AD-MLP
     - no
     - 0.29
     - 0.19

AD-MLP, with no cameras at all, has the lowest distance error. Its collision
rate is between the two. So an open-loop score on nuScenes does not show that
a model sees the road. Li et al. (2024) give a reason: "73.9% of the nuScenes
data involve scenarios of driving straightforwardly", and models given the
AV's speed "tend to rely predominantly on the ego vehicle's status". Nothing
here is closed loop. It tells us how little this open-loop score measures.

Benchmarks and GP4
~~~~~~~~~~~~~~~~~~

Two benchmarks try to score a plan better than an open-loop error does. Then
we see how GP4 scores your own stack, in closed loop.

Two benchmarks that score a plan
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **NAVSIM** (2024) uses real recorded drives. Its authors say: "Our
  simulation is non-reactive, i.e., the evaluated policy and environment do
  not influence each other." The planner is "only queried in the initial
  frame of each scene", and its 4 s plan gets the PDM Score: collisions and
  leaving the drivable area cancel the score, and progress, time to collision
  and comfort are averaged (Dauner et al., 2024).
- **Bench2Drive** (2024) runs in CARLA: "the first benchmark for evaluating
  E2E-AD systems' multiple abilities in a closed-loop manner", with "44
  interactive scenarios" over "220 routes" (Jia et al., 2024).

NAVSIM is a middle ground: real sensor data and a score that checks the plan,
but the plan never moves the AV. Only a closed loop shows compounding error.

GP4 scores your stack in closed loop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

GP4 scores your stack by running it: your commands decide where the AV goes
next. You run your route twice, once with your EKF pose and once with the true
pose, with 40 vehicles and 80 walkers. The script ``tools/evaluate_run.py``
scores each drive until the AV first comes within 2 m of the goal, and
reports:

- route completion: 1 at arrival; otherwise 1 minus the road distance still
  left to the goal over the route's length;
- collisions and pedestrian hits;
- red-light violations: crossing a stop line on red faster than 1 m/s;
- cross-track error and mean speed.

For grading, the grader runs your code on a held-out route and compares with
the reference solution: route completion at least 0.8 times the reference's,
and no more red-light violations or pedestrian hits than the reference. The
:doc:`GP4 page </assignments/gp4>` has the full rubric.


.. _l11-lec-modular-or-e2e:

Modular or End-to-End
---------------------

Evaluation gave closed-loop scores and showed why open-loop ones mislead. This
section uses them to compare the two designs: the designs side by side, how to
compare them fairly, and GP5. Your final report evaluates your modular
pipeline. End-to-end driving is the optional GP5.

The two designs, side by side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 40 40
   :class: compact-table

   * -
     - Modular (your stack)
     - End-to-end
   * - Built from
     - parts people design, each with its own test
     - one network trained on driving data
   * - Between parts
     - messages people chose: boxes, a pose, a path
     - whatever the network learned
   * - Trained for
     - each part's own score
     - the driving output
   * - Debugging
     - read each topic, find the part
     - look at outputs and any readable parts inside (UniAD)
   * - Data it needs
     - labels for each part, such as boxes for a detector
     - driving data; for DAgger, an expert that can label any state

Both are tested the same way at the end: closed loop, on the routes and
scenarios that matter.

.. dropdown:: More detail: what two companies say about their own systems
   :class-container: more-detail
   :icon: info
   :name: l11-more-company-claims

   Companies have said where they sit between the two designs. These are
   company statements, quoted with their dates. No outside test has checked
   them.

   - **Tesla, Q4 and FY 2023 Update (an investor update published in 2024):**
     "V12 utilizes end-to-end training". In words: Tesla says its V12 software
     is trained end to end (Tesla, 2024).
   - **Tesla, Q1 2024 Update (published in 2024):** "We believe a scalable and
     profitable autonomy business can be realized through a vision-only
     architecture with end-to-end neural networks, trained on billions of
     miles of real-world data". In words: Tesla says it believes cameras
     alone and end-to-end networks can support a profitable autonomy business
     (Tesla, 2024).
   - **Waymo, blog post of December 9, 2025:** "Its innovative architecture
     provides significant benefits over the pure end-to-end or modular
     approaches." In words: Waymo says its design is better than either pure
     design. It "supports full end-to-end signal backpropagation during
     training", so the error at the output trains all the parts together. It
     also keeps "compact, materialized structured representations like
     objects, semantic attributes, and roadgraph elements", which are readable
     objects and roads inside the network (Waymo, 2025).

   Waymo's description sits between the two rows of the first figure on this
   page: trained end to end, with readable objects and roads inside.

A fair comparison, in four steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Same routes and scenarios,** none used in training or tuning. Your final
   report does this for your modular pipeline: three scenarios the instructor
   provides, unseen during development.
2. **Closed loop,** with the same metrics: route completion, collisions, red
   lights, as GP4's script reports them.
3. **Several runs,** and report the spread: our clone finished 2 to 9 laps of
   20 depending only on the training run.
4. **Say what each one was given:** sensors, the map, the route, privileged
   information (a state only the simulator knows, like the expert's true
   offset). CARLA's Leaderboard banned "any privilege information offered by
   the CARLA simulator" (CARLA Team, 2026).

GP5: an optional end-to-end project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**GP5 is optional and not graded:** no points, no bonus, nothing due and
nothing submitted. It does not count toward the group-project grade or the
final report. The full description is on :doc:`the GP5 page </assignments/gp5>`.

- **What you do:** keep your GP1 to GP3 nodes and GP4's planner, remove GP4's
  behavior and controller nodes, and add one learned model in their place. It
  reads the front camera image and a short text command, and outputs steering,
  throttle and brake.
- **What you get:** no starter code and no reference solution. The GP5 page
  lists the files you create and the GP4 files you reuse.
- **Your team:** your GP4 team. You can show the drive and a comparison table
  to the instructor, by email or in office hours.

Today's lecture gives the ideas behind GP5, and GP4's closed loop and scoring
script test your model.

GP5's model: three parts, six commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Two frozen CLIP encoders** (CLIP is a pre-trained image and text model),
  one for the image and one for the text command, each giving 512 numbers.
  You do not train them.
- **One input:** the two vectors and the speed, 512 + 512 + 1 = 1,025 numbers.
- **A small decoder** that you train, a multi-layer perceptron (a few fully
  connected layers). It gives three numbers, kept in the ranges of the
  vehicle command.
- **Six fixed commands,** such as "follow the road" and "turn left at the
  intersection". With six phrases, the text input is a choice among six
  constant vectors.

So GP5's model is close to conditional imitation: a camera-driven policy with
a six-way command. It is much smaller than DriveVLM or Alpamayo, and it does
not write text.

.. admonition:: Where that leaves us
   :class: tip

   - Behavior cloning is supervised learning on an expert's drive. Our clone
     (run 6) copied the expert within 0.37° and finished 5 test laps of 20;
     ten runs finish 2 to 9.
   - Its error grew from 0.44° near the center to 2.41° near the lane's edge:
     compounding error, in states the recording never showed.
   - DAgger adds those states, labeled by the expert: 19 of 20 laps, in 10 of
     10 training runs.
   - Junctions need the route's command. End-to-end networks range from
     TransFuser to UniAD to VLAs; their authors report 0.41 s (DriveVLM) and
     0.099 s (Alpamayo 1), on different chips.
   - Judge any driver in closed loop: open-loop scores favored the clone that
     failed.
