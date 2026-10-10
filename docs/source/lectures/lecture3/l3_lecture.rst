====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L3, the slides shown in class, in
   the same order and with the same sections. They add what the speaker
   notes say aloud, so you can read them at home. Material the deck keeps in
   its appendix (the worked fix for a shared map error, the motion and
   measurement models in detail, the UKF, the particle filter and the
   notation tables) is on :doc:`the appendix page <l3_appendix>`.

.. important::

   **Perception is not covered here.** This lecture assumes measurements
   arrive from somewhere and asks what to do with them. The detector that
   turns pixels into boxes is :doc:`L4 <../lecture4/l4_index>`.

   **Data association**, deciding which measurement belongs to which object,
   is L6. Here there is one AV and every
   measurement is about it.

.. admonition:: Class logistics for this week
   :class: warning

   - **CARLA cluster accounts** are set up this week.
   - **Teams form this week.**
   - **GP1 is posted after class.** It uses L2's calibration work, not
     today's filter.

   **This lecture is for GP3**, whose EKF fuses GNSS fixes with IMU and
   wheel speed data to estimate the AV's pose.


.. _l3-introduction:

Introduction
------------

Every Sensor Reports a Different Number
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every sensor on the AV looks at the same world, and each one reports a
different number for it. None of them is exactly right.

It is tempting to ask which sensor to trust. That is the wrong way to think
about it. **We trust all of them, each by the right amount**, and how much to
trust each one has an exact answer. Not a guess, and not a knob you turn
until the plot looks nice: a formula. You only get it if you know how
uncertain each sensor is, and if their errors have no bias, so the first part
of the lecture puts a number on uncertainty.

- **Where we are:** L2 mounted and calibrated the sensors, so they can be
  combined.
- **In this lecture:** how much to trust each sensor, and how to combine
  them.
- **What it is for:** the AV needs **one** position, and the right weights
  have an **exact answer** once you know how uncertain each sensor is.

.. tip::

   **This lecture is the other half of L2.** L2 made combining possible. L3
   does the combining, with everything you calibrated last week. Why the AV
   cannot simply use its newest reading is worked through in
   :doc:`the appendix <l3_appendix>` ("Why we filter").


.. _l3-what-a-filter-is:

What a Filter Is
~~~~~~~~~~~~~~~~

.. admonition:: Definition: filter
   :class: note

   A **filter** keeps a running **estimate** (best guess) of something **no
   sensor gives you exactly**, updates it whenever a measurement arrives,
   and reports how uncertain that guess is right now.

   It holds two things at all times: **the estimate**, and **how much to
   trust it**.

The name comes from signal processing: noise in, cleaner signal out. A filter
that estimates the AV's position does the same job.

**No sensor gives you exactly what you want**, for three reasons, and a real
AV has all three at once.

- **Nothing reports it directly.** No sensor on our AV reports its velocity,
  meaning its speed *and* its direction (wheel speed gives only how fast).
  The planner, which decides where to drive, needs it. *The filter works it
  out from how the position changes.*
- **No single sensor sees all of it.** A GNSS fix, as we use it, gives
  position only. An IMU measures acceleration, but not where you are.
- **What does arrive is corrupted.** Every reading is the true value *plus
  noise* (random error), so even the parts you do measure come in a little
  wrong.


.. _l3-two-jobs:

A Good Filter Does Two Jobs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The two jobs below are the backbone of the whole lecture.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Job 1. Combining
      :class-header: bg-primary text-white

      Two sensors report different numbers for the same quantity. Neither
      one is right.

      The filter must turn them into one number. By the end of the Kalman
      gain subsection there is a complete answer.

   .. grid-item-card:: Job 2. Trust
      :class-header: bg-warning

      The filter reports a position **and** an uncertainty.

      That uncertainty must be checked. A filter that is wrong does not
      crash. It reports a small number and keeps running.

.. admonition:: The main idea of this lecture
   :class: danger

   Job 2, the uncertainty, is the one that causes trouble: when it is wrong,
   **nothing in the system detects it**.

   L2 said the same about hardware: a dirty camera does not report an error,
   it reports data. The algorithm fails the same way. Imagine an
   **overconfident** filter, one that claims to be more precise than it is.
   It reports :math:`\pm 0.2` m while being 3 m wrong, and no alarm goes off
   anywhere in the AV. The last section of the lecture,
   :ref:`l3-consistency`, is the check that catches it.

The learning objectives for the lecture are listed in
:doc:`the appendix <l3_appendix>`.


.. _l3-terminology:

Terminology
-----------

Three things come first, because the rest of the lecture uses them:

- The **frame**: where zero is, and which way the axes point.
- What an **uncertainty** is, and the two kinds of error.
- How to put a number on it: the spread :math:`\sigma`, and the covariance
  matrix :math:`P`.

None of this is hard, and each one is built step by step. A deeper treatment
(noise and bias, where readings land in 2-D, confidence intervals) is in
:doc:`the appendix <l3_appendix>`.


.. _l3-road-frame:

The Road Frame
~~~~~~~~~~~~~~

From L2: **a position means nothing until you say which frame (which zero and
which axes) it is measured in.** A frame is a set of choices, and every
number in this lecture lives in the one below.

- **Origin**: a survey marker at the roadside. It is :math:`(0, 0)`.
- **Axes**: :math:`x` runs **along** the road, :math:`y` runs **across** it,
  positive toward the far curb.
- **Unit**: the meter, on both axes.
- **Point on the AV**: the middle of its **rear axle**, called the **base
  link**. This is the convention Autoware, the open-source AV software,
  uses. The rear wheels do not steer, so that point always moves straight
  along the heading, never sideways, even in a turn. That keeps the motion
  model simple. (The appendix explains this choice in more detail.)

.. figure:: /_static/images/L3/road_frame.png
   :alt: Plan view of a straight two-lane road. A survey marker on the near curb is the origin; x runs along the road and y across it. The AV's rear axle middle, marked with a dot, is at x = 103.0 m and y = 2.5 m. The x axis carries a break between 7 and 96 m.
   :width: 90%
   :align: center

   The road frame. The survey marker on the near curb is the origin. Solid
   edge lines run at :math:`y = 0.7` m and :math:`y = 7.9` m, and the dashed
   lane line at 4.3 m. The AV, facing along the road and centered in its
   3.6 m lane, has its base link (the dot on the rear axle) at
   :math:`(103.0,\ 2.5)`. The break in the :math:`x` axis between 7 and
   96 m lets the origin and the AV fit at the same scale.

.. tip::

   :math:`(103.0,\ 2.5)` is not a property of the AV. Nothing here is 103 m
   long. It is an **instruction for finding the AV**: from the marker, go
   103.0 m along the road, then 2.5 m across. Like a street address, it only
   makes sense once you know the town.

   Move the marker 50 m up the road, and the same AV becomes
   :math:`(53.0,\ 2.5)`. **The AV did not move. The frame did.** So the frame
   is part of every reading, not decoration.


.. _l3-uncertainty:

Uncertainty, Noise and Bias
~~~~~~~~~~~~~~~~~~~~~~~~~~~

One idea opens this subsection: **an estimate without an uncertainty is
useless to a filter.**

.. admonition:: Definition: uncertainty
   :class: note

   A number attached to an estimate saying how far the truth could plausibly
   be from it.

   **Formally**, the International Vocabulary of Metrology (VIM, JCGM
   200:2012, clause 2.26) defines *measurement uncertainty* as a
   non-negative parameter characterizing the spread of values that could
   reasonably be attributed to the measured quantity. In practice that
   parameter is a standard deviation, which we build in
   :ref:`l3-sigma`. L2 cited the same document for calibration, so this is
   standard vocabulary, not course jargon.

**Example.** A GNSS fix of 100.0 m with an uncertainty of 2 m says the truth
is probably within a couple of meters of 100.0 m.

**The** :math:`\pm 2` **m is not optional.** Say someone tells you the AV is
at 100 m, and nothing else. How much weight should that get? Nobody can say.
Combining two estimates means deciding **how much each one counts**, and that
weight comes from the uncertainties. A bare 100.0 m, with no
:math:`\pm`, gives nothing to weigh, so all you can do is trust every source
equally, which is a guess.

Noise and Bias Are Two Separate Errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Imagine taking one of the AV's sensors to a shooting range. Every reading is
a shot at the target. There are two completely different ways for it to fail.

- **Noise** is random scatter, like shooting with shaky hands. Every reading
  is off by a different, random amount.
- **Bias** is the same error every time. Picture a rifle whose sight has been
  knocked a little out of line: with rock steady hands, every shot still lands
  two inches to the left. On an AV, it is a camera mounted slightly crooked:
  every position it reports is off in the same direction.

.. figure:: /_static/images/L3/noise_vs_bias.png
   :alt: Four shooting targets in a two by two grid. Columns: low noise (tight group) and high noise (wide scatter). Rows: no bias (centered) and bias (shifted). Each target has fourteen blue readings, an orange cross at their average and a dark dot at the truth.
   :width: 75%
   :align: center

   Noise against bias. The **blue dots** are sensor readings, the **orange
   cross** is their average, and the **dark center** is the truth. The
   columns show noise (left tight, right scattered); the rows show bias (top
   centered on the truth, bottom shifted, with a dashed orange line from the
   truth to the average). The four targets are captioned: the good sensor;
   averaging fixes it; looks good, is wrong; and plainly bad.

Two things to read off the grid.

- **Averaging fixes scatter.** The readings stay just as scattered, but their
  *average* wanders less the more readings you take: by about
  :math:`\sigma/\sqrt{n}` for :math:`n` readings. A noisy sensor, averaged,
  gives an answer as steady as a quiet one (right column to left column).
- **Averaging cannot fix a fixed shift.** Taking more readings never moves
  the cross closer to the bullseye. You can average away **noise**, but you
  can never average away **bias**.

The bottom-left target is the one that crashes an AV. The readings agree with
each other beautifully, and the data stream looks clean and reliable, but the
whole cluster is in the wrong place. Average a thousand of its readings and
you get a perfectly confident, perfectly wrong answer.

.. admonition:: Where that leaves us: two kinds of error
   :class: tip

   An estimate is wrong for **two separate reasons**, and which one you have
   decides what you can do about it.

   **Noise** is random scatter about a center. Take more readings and it
   **averages away**. **Bias** is the same shift every time, and it **never
   averages away**, however many readings you take.

   Three careful words: **precision** is the word for noise, **trueness** for
   bias, and **accuracy** means both are small at once. A sensor can be
   precise and still be wrong.


.. _l3-variance:

Variance
~~~~~~~~

**Park the AV** on a surveyed spot 100.0 m down the road, so we know its true
position exactly: :math:`(100.0,\ 2.5)`. Without moving it an inch, ask the
GNSS receiver for the position six times. You get six different answers:

.. code-block:: text

   (102.1, 1.4)   (98.6, 4.3)   (100.9, 3.1)
   ( 99.2, 1.2)   (101.4, 3.4)  ( 97.8, 1.6)

First, the middle. The **mean (average)**: add the six readings on one axis,
then divide by six.

.. math::

   \mu_x = \tfrac{1}{6}\,(102.1 + 98.6 + \dots + 97.8) = 100.0\ \text{m},
   \qquad
   \mu_y = \tfrac{1}{6}\,(1.4 + 4.3 + \dots + 1.6) = 2.5\ \text{m}

The six :math:`x` readings total exactly 600, so the mean lands right on the
truth. That is by design: **we chose a receiver with no bias**. Its readings
average to the truth, so all of their error is noise, and variance has a
clean job: **it measures that noise.**

.. note::

   Could six readings prove there is no bias? No. Their average wobbles by
   about 0.6 m (:math:`\sigma/\sqrt{6}`, with the :math:`\sigma` we compute
   below), so proving it takes many readings. "No bias" here is a premise we
   chose, not something the data shows. Keep one catch in mind as well: a few
   paragraphs on, you meet a second receiver whose readings sit 3.2 m ahead
   every time, and its variance is exactly the same.

.. admonition:: Definition: variance
   :class: note

   How spread out the readings are from their center. To find it, take each
   reading's distance from the mean, **square it**, and average those squared
   distances.

   .. math::

      \operatorname{Var}(x) = \mathbb{E}\!\left[(x - \mu_x)^2\right],
      \qquad \mu_x = \mathbb{E}[x]

   :math:`x`: one reading along the road. :math:`\mu_x`: the mean.
   :math:`\mathbb{E}[\,\cdot\,]`: "the average of", over all readings.

Read the formula like a sentence: take a reading, subtract the mean, square
that distance, and average the squares. Worked out for our six readings:

.. list-table::
   :widths: 24 19 19 19 19
   :header-rows: 1
   :class: compact-table

   * - **Reading**
     - :math:`x-\mu_x`
     - :math:`(x-\mu_x)^2`
     - :math:`y-\mu_y`
     - :math:`(y-\mu_y)^2`
   * - (102.1, 1.4)
     - +2.1
     - 4.41
     - -1.1
     - 1.21
   * - (98.6, 4.3)
     - -1.4
     - 1.96
     - +1.8
     - 3.24
   * - (100.9, 3.1)
     - +0.9
     - 0.81
     - +0.6
     - 0.36
   * - (99.2, 1.2)
     - -0.8
     - 0.64
     - -1.3
     - 1.69
   * - (101.4, 3.4)
     - +1.4
     - 1.96
     - +0.9
     - 0.81
   * - (97.8, 1.6)
     - -2.2
     - 4.84
     - -0.9
     - 0.81
   * - **Total**
     - **0.0**
     - **14.62**
     - **0.0**
     - **8.12**

Walk through the first row: the reading 102.1 misses the mean of 100.0 by
+2.1 m, and :math:`2.1^2 = 4.41`. The total of squares divided by 6 is the
**variance**:

.. math::

   \operatorname{Var}(x) = 14.62 / 6 = \mathbf{2.437}\ \text{m}^2
   \quad\text{(along the road)},
   \qquad
   \operatorname{Var}(y) = 8.12 / 6 = \mathbf{1.353}\ \text{m}^2
   \quad\text{(across)}

The bigger number means more spread: these readings scatter more along the
road than across it.

**Why square?** Look at the totals row. The raw distances add up to exactly
zero: the readings above the mean cancel the ones below, so their average
says nothing. Squaring makes every distance positive. It also punishes one
huge miss much harder than a few tiny ones.

.. note::

   We divide by 6, not 5, because the mean here is the surveyed truth. A mean
   worked out from the readings themselves calls for :math:`n - 1 = 5`.

**Variance is in square meters.** An error of 2.437 m² is hard to picture:
what does a square meter of missing look like? Taking the square root brings
us back to meters.


.. _l3-sigma:

Standard Deviation
~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: standard deviation :math:`\sigma`
   :class: note

   **How far a typical reading sits from the mean**, in meters: the square
   root of the variance.

   .. math::

      \sigma = \sqrt{\operatorname{Var}(x)}, \qquad
      \sigma_x = \sqrt{2.437} = \mathbf{1.56}\ \text{m}, \qquad
      \sigma_y = \sqrt{1.353} = \mathbf{1.16}\ \text{m}

.. figure:: /_static/images/L3/lane_sigma.png
   :alt: Top view, to scale, of a 3.6 m lane split into thirds. The parked AV sits in the middle; a cross on its rear axle marks the truth. A blue band covers plus and minus 1.16 m across the road. Six orange dots are the six readings. A two-headed arrow below spans plus and minus 1.56 m along the road.
   :width: 90%
   :align: center

   The same six readings, drawn to scale on a real lane. The **cross** on the
   AV's rear axle is the truth, where we parked. The **blue band** is
   :math:`\pm\sigma_y = \pm 1.16` m across the road, about a third of the
   lane on each side. The **orange dots** are the six readings: three in the
   right third of the lane, one in the left third, one on the edge of the
   center third, and one, :math:`(98.6,\ 4.3)`, right on the lane line. The
   arrow under the lane is :math:`\pm\sigma_x = \pm 1.56` m along the road,
   centered on the truth.

A typical sideways miss, 1.16 m, is **a third of a 3.6 m lane**: from one
reading, the AV cannot tell where in its lane it is. To keep a lane, the AV
needs its sideways position to a few tens of centimeters, and this receiver
misses by more than a meter. That is the argument for the whole lecture: we
cannot trust this receiver alone, so we filter. Where readings land in 2-D,
and why a 1σ circle holds fewer of them than you might expect, is in
:doc:`the appendix <l3_appendix>`.

.. admonition:: Where that leaves us: putting a number on the scatter
   :class: tip

   Along the road, for our six readings:

   - **Mean** :math:`\mu_x = 100.0` m: *where the readings sit on average.*
     Add the six readings, divide by six.
   - **Variance** :math:`\operatorname{Var}(x) = 14.62/6 = 2.437` m²: *how
     spread out they are.* Square each distance from :math:`\mu_x`, then
     average.
   - **Standard deviation** :math:`\sigma_x = \sqrt{2.437} = 1.56` m: *how
     far a typical reading sits from* :math:`\mu_x`. Back in meters, so it is
     the one you hold against a lane.

   **Why square?** The distances from the mean, +2.1, -1.4, +0.9, -0.8,
   +1.4, -2.2, add up to **0.0**: plus and minus cancel. Squared, every one is
   positive: :math:`4.41 + 1.96 + \dots + 4.84 = 14.62`.

   **None of the three knows where the truth is.** Our mean matches the
   surveyed spot, 100.0 m, only because we chose a receiver with no bias.
   Checking that takes an outside reference.

Two Receivers with the Same Sigma
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Imagine we bolt a second GNSS receiver, B, onto the same AV**, right next
to receiver A. A is the receiver we chose with no bias. **B is new: we do not
know yet whether it has bias.** That is what we want to find out. The AV is
still parked on the surveyed spot, :math:`x = 100.0` m, and we ask both
receivers for the position six times (only :math:`x`, along the road, is
shown).

.. list-table::
   :widths: 14 56 15 15
   :header-rows: 1
   :class: compact-table

   * - **Receiver**
     - **Six readings (m)**
     - :math:`\mu_x`
     - :math:`\sigma_x`
   * - A
     - 102.1, 98.6, 100.9, 99.2, 101.4, 97.8
     - 100.0
     - 1.561
   * - B
     - 105.3, 101.8, 104.1, 102.4, 104.6, 101.0
     - 103.2
     - 1.561

.. admonition:: Before reading on
   :class: hint

   Look at both rows. Does B have bias? Which receiver would you trust? Then
   look at the last column.

.. dropdown:: Answer
   :color: success
   :icon: check-circle

   The sigmas are identical, 1.561 m. Every B reading is an A reading plus
   3.2 m, so the two scatter by exactly the same amount.

   .. figure:: /_static/images/L3/two_receivers.png
      :alt: Two rows on the same axis, 96 to 106 m along the road, with a dashed green line at the surveyed truth, 100 m. Receiver A: six dots between 97.8 and 102.1 m, mean 100.0 m on the truth line, band plus or minus 1.561 m. Receiver B: the same dots shifted 3.2 m right, mean 103.2 m, a band of the same width. An arrow from the truth to B's mean is labeled bias plus 3.2 m.
      :width: 90%
      :align: center

      Both receivers on the same road. The **dashed green line** is the
      truth, the surveyed 100 m. Each row shows six **orange dots**, a **red
      bar** at the mean, and a **blue band** of :math:`\pm\sigma =
      \pm 1.561` m. The bands are exactly the same width. A centers on the
      truth; B centers 3.2 m ahead, and the black arrow between the rows marks
      that offset, the bias, +3.2 m.

   **Same** :math:`\sigma`, **not equally good.** Judged by :math:`\sigma`
   alone, A and B are equally good. The difference is where they center.

   Could B just be unlucky? Noise alone moves the average of six readings by
   only about :math:`\sigma/\sqrt{6} = 1.561/2.45 \approx 0.64` m. B is off
   by five times that, so **3.2 m is bias**, not luck. (That 0.64 m assumes
   the six errors are independent. Real GNSS readings taken one after another
   are correlated in time, so their average wanders more. Even if it wandered
   twice as much, 3.2 m would still be well beyond it.)

   :math:`\sigma` **cannot tell a centered receiver from a biased one.**
   Finding bias needs **the truth from outside**: here, the surveyed spot.
   :math:`\sigma` needs only the readings.

   This matters for the rest of the lecture. The Kalman filter handles noise
   correctly. Bias breaks one of its assumptions, so the filter carries a
   steady offset forever and never complains. Confidence intervals, the other
   classic way to quote an uncertainty, are covered in
   :doc:`the appendix <l3_appendix>`.


.. _l3-covariance:

Covariance
~~~~~~~~~~

Two Numbers Are Not Always Enough
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Imagine two receivers on the parked AV. Each reports its position **120
times**, one reading after another, the same way we took our six. **We chose
their errors**, so here we know everything: both center on the truth, and both
have exactly our variances, 2.437 m² along the road and 1.353 m² across.

.. figure:: /_static/images/L3/cov_tilt.png
   :alt: Two panels to scale, each with 120 orange readings around a black cross at the truth and a blue 2-sigma ellipse. Left: errors independent, upright ellipse, Cov x y 0.000. Right: errors move together, the cloud leans up to the right, Cov x y 1.271. Both have Var x 2.437 and Var y 1.353 square meters.
   :width: 85%
   :align: center

   Same variances, different clouds. Each panel shows 120 readings (orange
   dots) around the truth (black cross), with a blue :math:`2\sigma` ellipse
   labeled "most readings". **Left, errors independent:** the ellipse is
   upright, wider along the road than across, with no lean;
   :math:`\operatorname{Cov}(x,y) = 0.000` m². **Right, errors move
   together:** the cloud leans up to the right, so too far ahead usually goes
   with too far left; :math:`\operatorname{Cov}(x,y) = 1.271` m². The
   two-headed arrows, :math:`\pm\sigma` along :math:`= \pm 1.56` m and
   :math:`\pm\sigma` across :math:`= \pm 1.16` m, are the same in both panels.

So far we have used one variance per axis. That quietly assumes the two
errors are **independent**: a reading too far ahead tells you nothing about
left or right. That is the left cloud: of its 62 readings ahead of the truth,
32 are also to the left, about half. The right cloud leans. Of its 62 readings
ahead of the truth, 48 are also to the left. Too far ahead usually comes with
too far left, and we call those errors **correlated**.

**Same** :math:`\operatorname{Var}(x)` **and** :math:`\operatorname{Var}(y)`,
**different clouds.** Two variances give the width and height of the cloud,
never its lean. We need a third number.

Covariance Measures the Lean
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: covariance :math:`\operatorname{Cov}(x,y)`
   :class: note

   **How much the** :math:`x` **and** :math:`y` **errors move together.**
   Same recipe as variance, but instead of squaring the :math:`x` distance
   from its mean, multiply it by the :math:`y` distance, then average.

   .. math::

      \operatorname{Cov}(x,y) = \mathbb{E}\!\left[(x-\mu_x)(y-\mu_y)\right]

Put the numbers in one matrix, the **covariance matrix** :math:`P`. The entry
in row :math:`a`, column :math:`b` is :math:`\operatorname{Cov}(a,b)`:

.. math::

   P \;=\; \begin{bmatrix}
      \operatorname{Cov}(x, x) & \operatorname{Cov}(x, y) \\
      \operatorname{Cov}(y, x) & \operatorname{Cov}(y, y)
   \end{bmatrix}
   \;=\; \begin{bmatrix}
      \operatorname{Var}(x) & \operatorname{Cov}(x, y) \\
      \operatorname{Cov}(x, y) & \operatorname{Var}(y)
   \end{bmatrix}

- **On the diagonal**, each axis with itself. :math:`\operatorname{Cov}(x,x)`
  multiplies the :math:`x` distance by itself, which is squaring it, so it
  *is* :math:`\operatorname{Var}(x)`. The diagonal is the two variances you
  already have.
- **Off the diagonal**, the lean. :math:`\operatorname{Cov}(y,x) =
  \operatorname{Cov}(x,y)`, the same product in the other order, so the two
  corners are equal. One idea, applied four times.

Covariance, Worked Out
^^^^^^^^^^^^^^^^^^^^^^

One more column on the table you already filled in: multiply each :math:`x`
deviation by its own :math:`y` deviation, then average.

The products, row by row: :math:`(+2.1)(-1.1) = -2.31`, then -2.52, +0.54,
+1.04, +1.26 and +1.98. They total **-0.01**.

Row one is plus times minus, so the product is negative. Row four is minus
times minus, so it is positive. That is the whole idea: distances on the same
side of the mean give a positive product, opposite sides a negative one. Here
they nearly cancel:

.. math::

   \operatorname{Cov}(x,y) = \tfrac{-0.01}{6} = -0.002,
   \qquad
   P = \begin{bmatrix} 2.437 & -0.002 \\ -0.002 & 1.353 \end{bmatrix}
   \approx \begin{bmatrix} 2.437 & 0 \\ 0 & 1.353 \end{bmatrix}

**Read the sign off the diagonal.** Positive: too far ahead usually comes with
too far left, the leaning cloud. Negative: too far ahead usually comes with
too far right. **Near zero, like our -0.002: no lean**, the upright cloud on
the left of the figure above. Knowing a reading is too far ahead does not help
you guess left or right.

.. note::

   Six readings cannot prove there is no lean. A covariance from six readings
   wanders by about 0.74 m² from sample to sample even when the true value is
   zero, so -0.002 is near zero partly by luck. Our readings fit a receiver
   with no lean, and that is how we chose it, as with no bias.

.. admonition:: Where that leaves us: when one number per axis is not enough
   :class: tip

   - **Two variances give the width and height of the cloud, never its
     lean.** The two clouds share :math:`\operatorname{Var}(x) = 2.437` and
     :math:`\operatorname{Var}(y) = 1.353` m²; one is upright, one leans.
   - **Covariance** :math:`\operatorname{Cov}(x,y)` *measures the lean.*
     Multiply each :math:`x` distance by its :math:`y` distance, then
     average. Ours: :math:`-0.01/6 = -0.002`, no lean, as we chose the
     receiver.
   - **The covariance matrix** :math:`P` *holds all four numbers*: variances
     on the diagonal, :math:`\operatorname{Cov}(x,y)` off it. For our six
     readings, :math:`P \approx \begin{bmatrix} 2.437 & 0 \\ 0 & 1.353
     \end{bmatrix}`.

   **In a filter that tracks position and velocity, the position-velocity
   terms appear on their own** as soon as it predicts forward, because a
   position predicted from a velocity depends on that velocity. You do not
   put them in yourself. You will see it in the tunnel filter's predict step,
   where the ellipse of position against speed tilts more.



.. _l3-kalman:

The Kalman Filter
-----------------

.. admonition:: Definition: Kalman filter (Kalman, 1960)
   :class: note

   A **recursive estimator**: it keeps only an **estimate**
   :math:`\hat{\mathbf{x}}` and its **covariance** :math:`P`, and repeats two
   steps. **Predict** with a motion model (:math:`P` grows), then **update**
   with a measurement (:math:`P` shrinks). When the models are **linear**
   (matrices) and the noise is **Gaussian** (a bell curve), no other
   estimator has a smaller expected squared error.

*Recursive* means the filter never keeps the history of readings, only the
current estimate and its :math:`P`. Large :math:`P` means uncertain, small
:math:`P` means confident. The two conditions, linear models and Gaussian
noise, are why this filter and not another; the section
:ref:`l3-assumptions-break` shows what happens when they fail.

.. figure:: /_static/images/L3/kf_generic.png
   :alt: Textbook block diagram of the Kalman filter. The initial guess x-hat zero and P zero enter a green Predict box (time update) that computes the predicted state and P minus. That feeds a blue Update box (measurement update) that computes K, the new estimate and the new P. A control input u k feeds Predict and a measurement z k feeds Update. A loop labeled next step returns to Predict.
   :width: 80%
   :align: center

   The Kalman filter as every textbook draws it. **Predict** (green, the
   time update) moves the estimate one time step forward, using the motion
   model and the control input :math:`\mathbf{u}_k`, what the AV did. The
   model is never perfect, so the uncertainty grows. **Update** (blue, the
   measurement update) corrects the prediction with a measurement
   :math:`\mathbf{z}_k`, and the uncertainty shrinks. Out come
   :math:`\hat{\mathbf{x}}_k` and :math:`P_k`, which loop back into Predict
   for the next step. The loop is started once, from a first estimate
   :math:`\hat{\mathbf{x}}_0` and a first :math:`P_0`. Do not read the
   equations in the boxes yet: by the end of this section each one has been
   built, and you can come back and read the figure line by line.

.. note::

   "Measurement" and "observation" mean the same thing. These notes say
   measurement; many books say observation. A deeper look at the Kalman
   filter, including the worked fix for a shared map error, is in
   :doc:`the appendix <l3_appendix>`.


.. _l3-tunnel:

An Example: an AV in a Tunnel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here are the two boxes on a real vehicle. The AV drives into a tunnel and
loses GNSS. It does not stop. It keeps estimating where it is from the wheel
encoders and the IMU: "I was going this fast, sped up or slowed down this
much, for this long, so I must be about here." That is the **prediction**.
Every second it gets a little more uncertain, because wheels slip and the IMU
drifts.

Then the camera spots an emergency exit sign, and the AV matches it against
its HD map: "that sign is at this spot, so I must be about here." That is the
**measurement**, and the AV corrects its estimate. But not completely,
because the match is not perfect either.

.. figure:: /_static/images/L3/lost_gnss_tunnel.jpeg
   :alt: Pencil sketch of an AV driving through a tunnel, headed GNSS lost. Labels: camera array on the roof; IMU and wheel encoders as the prediction; a green Emergency Exit sign as the visual sign match, the measurement; insets for HD map verification and pose estimation from the sign; state estimation as weighted fusion of prediction and measurement.
   :width: 80%
   :align: center

   **GNSS is lost.** The wheel encoders and IMU give the **prediction**. The
   camera's match of an exit sign against the HD map is the **measurement**:
   object detection and character recognition find the sign, its known size
   gives the distance, and the stored HD map gives its position. **Use both,
   and trust each in proportion to how good it is.**

In the Tunnel: Predict from the IMU, Update from a Sign Match
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/tunnel_flow.png
   :alt: Flowchart. Wheel encoders plus IMU feed a green Predict box (P grows), labeled what the AV did. A camera image and a top-view HD map of the tunnel, with exit signs every 25 m and the matched sign 12 m ahead circled, feed a feature match box, which feeds a blue Update box (P shrinks), labeled what a sensor saw. A zoomed panel shows the AV with a 1-sigma ellipse 1.35 m along by 0.44 m across. A start box feeds the belief at step k minus 1, then Predict, Update and the belief at step k, which loops back.
   :width: 90%
   :align: center

   What the AV runs in the tunnel. **Left**, the wheel encoders and the IMU
   say how fast the AV is going and how much it sped up or slowed down; that
   feeds **Predict** ten times a second, and every time :math:`P` grows.
   **Middle**, the camera image (walls, lights, a green exit sign). On its
   own, "I see an exit sign" does not say where we are. **Top right**, the
   HD map, a detailed map built in advance, down to the lane lines, knows
   where every exit sign is. Matching the sign in the image to the circled
   sign in the map, 12 m ahead, gives a position: the measurement. It feeds
   **Update**, and :math:`P` shrinks. In the zoomed map the AV's 1σ ellipse
   is long along the tunnel (1.35 m) and thin across it (0.44 m): the walls
   limit the sideways error, and only the signs say how far along it is.

The **HD map** is what turns "I see an exit sign" into "I am *here*". One
detail: the drawing shows wheel encoders, but our filter uses only the IMU as
the control input. Wheel speed could enter as a second measurement.


.. _l3-belief:

Between Sign Matches, the Filter Keeps a Belief
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the tunnel, a sign match is the only thing that tells the AV where it is,
and one comes along only every few seconds. In between, the filter has to
carry something forward. Not one number: a belief.

.. admonition:: Definition: belief
   :class: note

   **The probability of every possible state**, given everything measured so
   far. In plain words: for every position the AV **could** be at, how
   likely it is to really be there.

   *Example* (big :math:`P`, left figure below): estimate 100 m into the
   tunnel. 99 to 101 m: **likely**; 97 m: **possible**; 120 m: **almost
   impossible**.

.. list-table::
   :widths: 50 50
   :class: compact-table

   * - .. figure:: /_static/images/L3/belief_big_P.png
          :alt: Big P: a low, wide bell curve over position 92 to 108 m, peaking at the estimate, 100 m, with plus or minus sigma of 2.5 m. A gray dot at 97 m, still well up the curve, is labeled possible.
          :width: 100%
          :align: center

          **Big** :math:`P`: a wide, low curve, :math:`\pm\sigma =
          \pm 2.5` m. The AV could be **meters** from the estimate, and
          97 m is still possible.
     - .. figure:: /_static/images/L3/belief_small_P.png
          :alt: Small P: a tall, narrow bell curve on the same axes, peaking at 100 m, with plus or minus sigma of 0.7 m. A gray dot at 97 m sits on the flat baseline, labeled almost impossible.
          :width: 100%
          :align: center

          **Small** :math:`P`: a tall, narrow curve, :math:`\pm\sigma =
          \pm 0.7` m. The AV is **close** to the estimate, and 97 m is almost
          impossible.

A belief can have any shape (later in the tunnel, two identical lights give it
two peaks). **A Kalman filter keeps it as a bell curve, a Gaussian**, and a
bell curve needs only two things: the estimate sets where it peaks, and the
covariance :math:`P` sets how wide it is. :math:`P` is the covariance of the
**error**, the gap between the estimate and where the AV truly is. The area
under each curve is the same, so narrower means taller. That is all
:math:`P` ever means.


The Belief Changes in a Loop: Predict, Then Update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L3/kf_cycle.png
   :alt: Loop diagram. A Start box (first guess, big P) points once to the belief at step k minus 1 (last step). That enters a green Predict box, P grows, fed by a control input box (IMU and wheel encoders, what the AV did). Then a blue Update box, P shrinks, fed by a measurement box (camera sign match, what a sensor saw). Out comes the belief at step k (now), which loops back: next step, this k becomes the new k minus 1.
   :width: 90%
   :align: center

   How the belief changes from one step to the next in the tunnel. **Start**
   is the first estimate, used once: here, the last GNSS fix before the
   tunnel (with no fix at all, a rough guess with a big :math:`P`). The
   **belief** is the estimate and its :math:`P`. The green arrow is what the
   AV did, from the wheel encoders and the IMU; Predict uses it and
   :math:`P` grows, because nothing outside the AV measured anything. The
   blue arrow is what a sensor saw, the camera matching the exit sign to the
   map; Update corrects the estimate and :math:`P` shrinks.

The row begins at :math:`k-1`, not :math:`k`, because :math:`k` means *now*,
and the loop is how we get to now: we always begin from what we knew one step
ago. On the next step, this :math:`k` becomes the new :math:`k-1`, the arrow
along the bottom.

In the tunnel: **predict every 0.1 s, update only when a sign is matched.**
Between matches, the loop skips Update, so :math:`P` keeps growing until the
next match pulls it back down. Grow, shrink, forever. If you remember one
picture from the lecture, make it this loop.


.. _l3-gain:

Kalman Gain
~~~~~~~~~~~

- **Where we are:** the filter keeps a belief, an estimate and its
  :math:`P`, and loops predict, update.
- **In this subsection:** the **Kalman gain** :math:`K`, how to blend the
  prediction and the measurement.
- **What it is for:** letting the two uncertainties, not us, decide which
  source to trust.

Blend Two Answers: Act on a Fraction of the Surprise
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Still in the tunnel, no GNSS. Two sources give two answers, 3 m apart along
the tunnel (numbers we chose for the example):

- **Prediction: 50.0 m,** :math:`\sigma = 2` m. This is dead reckoning: the
  last matched sign, plus speed times the time since.
- **Sign match: 53.0 m,** :math:`\sigma = 1` m. The camera matches the next
  exit sign to the HD map.

Trust neither fully. The estimate :math:`\hat{x}` should land between 50 and
53, and any number there can be written one way: start at the prediction
:math:`\hat{x}^-` and move **some fraction** :math:`K` of the gap toward the
measurement :math:`z`. That gap, **measured minus predicted**, is the
**surprise**: how far the measurement landed from what we predicted. Here it
is :math:`z - \hat{x}^- = 53 - 50 = 3` m.

.. math::

   \hat{x} \;=\; \hat{x}^- \;+\; K \times \underbrace{(z - \hat{x}^-)}_{\text{the surprise}}
   \qquad\Longrightarrow\qquad
   \hat{x} \;=\; 50 \;+\; \underbrace{K}_{\text{what fraction?}}
   \times \underbrace{(53 - 50)}_{\text{the 3 m surprise}}

- :math:`K = 0`: :math:`\hat{x} = 50.0` m, believe the prediction and ignore
  the sign match.
- :math:`K = 0.5`: :math:`\hat{x} = 51.5` m, split the difference.
- :math:`K = 1`: :math:`\hat{x} = 53.0` m, believe the sign match and throw
  the prediction away.

.. admonition:: Definition: Kalman gain :math:`K`
   :class: note

   **The fraction of the surprise we act on.** The update moves the estimate
   by :math:`K` times the surprise. In reality, :math:`K` is **computed**
   from the two :math:`\sigma` values, not chosen as we did in the table.

:math:`K` is always between 0 and 1, so the estimate never lands below 50 or
above 53. The AV's true position can, if both sources are wrong the same way.
Every update of every Kalman filter has this form: the estimate moves by
:math:`K` times the surprise.

Computing the Gain K
^^^^^^^^^^^^^^^^^^^^

The filter computes :math:`K` from the :math:`\sigma` it already carries for
each source. **The less certain the prediction, the more we act on the
measurement.** :math:`K` is the prediction's share of the total variance:

.. math::

   K \;=\; \frac{\sigma_{\text{pred}}^2}{\sigma_{\text{pred}}^2 + \sigma_{\text{meas}}^2}

In the tunnel, :math:`\sigma_{\text{pred}} = 2` m, so its variance is 4, and
the sign match has :math:`\sigma_{\text{meas}} = 1` m, variance 1. The total
is 5, and the prediction owns four fifths of it:

.. math::

   K \;=\; \frac{2^2}{2^2 + 1^2} \;=\; \frac{4}{5} \;=\; \mathbf{0.8}
   \qquad\Longrightarrow\qquad
   \hat{x} \;=\; 50 + 0.8 \times 3 \;=\; \mathbf{52.4}\ \text{m}

We act on 80 percent of the 3 m surprise. A quick check that the rule makes
sense:

- **Big** :math:`\sigma_{\text{pred}}`: the prediction owns almost all the
  variance, :math:`K` is near 1, and we follow the sign match.
- **Equal** :math:`\sigma` **values**: :math:`K = 0.5`, split the difference.
- **Big** :math:`\sigma_{\text{meas}}`: :math:`K` is near 0, and we stay
  with the prediction.

Nobody decides which sensor to believe. The sigmas decide.

The New Sigma Mixes the Two Errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The new estimate is 52.4 m. Next question: **how sure are we of it?** Rewrite
the update as a **weighted average**:

.. math::

   \hat{x} \;=\; (1-K)\,\hat{x}^- + K z \;=\; 0.2 \times 50 + 0.8 \times 53 \;=\; 52.4\ \text{m}

Its error is the same mix: 20 percent of the prediction's error plus 80
percent of the sign match's. When the two errors are **independent**,
variances add, each times its weight squared:

.. math::

   \sigma^2 \;=\; (1-K)^2\,\sigma_{\text{pred}}^2 + K^2\,\sigma_{\text{meas}}^2
   \;=\; 0.2^2 \times 2^2 + 0.8^2 \times 1^2 \;=\; 0.16 + 0.64 \;=\; 0.8\ \text{m}^2,
   \qquad \sigma = \mathbf{0.89}\ \text{m}

.. note::

   **Shortcut:** with the Kalman :math:`K`, that sum always shortens to
   :math:`(1-K)\,\sigma_{\text{pred}}^2`. Here :math:`0.2 \times 4 = 0.8`
   m², the same answer. The matrix version later in the lecture uses this
   form: :math:`P = (I - KH)\,P^-`.

.. admonition:: Where that leaves us: one update, start to finish
   :class: tip

   .. list-table::
      :widths: 30 38 32
      :header-rows: 1
      :class: compact-table

      * - **Step**
        - **Rule**
        - **In the tunnel**
      * - 1. Prediction (wheels + IMU)
        - :math:`\hat{x}^-`, :math:`\sigma_{\text{pred}}`
        - 50.0 m, :math:`\sigma = 2` m
      * - 2. Sign match (camera + map)
        - :math:`z`, :math:`\sigma_{\text{meas}}`
        - 53.0 m, :math:`\sigma = 1` m
      * - 3. Surprise
        - :math:`z - \hat{x}^-`
        - :math:`53 - 50 = 3` m
      * - 4. Gain
        - :math:`K = \sigma_{\text{pred}}^2 / (\sigma_{\text{pred}}^2 + \sigma_{\text{meas}}^2)`
        - :math:`4/(4+1) = 0.8`
      * - 5. New estimate
        - :math:`\hat{x} = \hat{x}^- + K\,(z - \hat{x}^-)`
        - :math:`50 + 0.8 \times 3 =` **52.4 m**
      * - 6. New :math:`\sigma`
        - :math:`\sigma^2 = (1-K)\,\sigma_{\text{pred}}^2`
        - :math:`0.2 \times 4 = 0.8` m², :math:`\sigma =` **0.89 m**

   **Only the two** :math:`\sigma` **values decided:** they set :math:`K`,
   :math:`K` set how far we moved, and the new :math:`\sigma` is smaller than
   both inputs.

   **Then the loop goes on.** 52.4 m with :math:`\sigma = 0.89` m becomes the
   belief that predict starts from. Every 0.1 s predict moves it and
   :math:`\sigma` grows; at the **next** sign match, steps 2 to 6 run again
   with the new numbers.

After the Update, Sigma Is Smaller Than Either Source's
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/fusion_1d.png
   :alt: Three bell curves over distance into the tunnel. Green: prediction, 50.0 m, sigma 2.0 m, low and wide. Blue: sign match, 53.0 m, sigma 1.0 m. Orange, filled: combined, 52.4 m, sigma 0.89 m, the tallest and narrowest. A dotted gray line at 51.5 m is the plain average. Below, plus or minus sigma of each as two-headed bars to scale.
   :width: 85%
   :align: center

   The update as bell curves, in the loop's colors. **Green** is the
   prediction (50.0 m, :math:`\sigma = 2.0` m), wide. **Blue** is the sign
   match (53.0 m, :math:`\sigma = 1.0` m). **Orange** is the combined
   estimate, 52.4 m with :math:`\sigma = 0.89` m: closer to the sign match
   because the sign match is more certain, and the narrowest of the three
   (taller because it is narrower). The **dotted line** at 51.5 m is the
   plain average, which counts both sources equally even though the sign
   match's variance is a quarter of the prediction's. The bars at the bottom
   are :math:`\pm\sigma` of each, to scale; orange is the shortest.

Why is the result narrower than even the better source? One over
:math:`\sigma^2` measures how certain a source is. When the two errors are
independent, combining them **adds those certainties**: a quarter plus one is
1.25, and one over that is 0.8 m², the same variance as before. Keep the
direction straight: combining estimates adds certainties, and the answer gets
sharper. Waiting adds variances, and that is the :math:`+Q` in predict.

A Worse Sign Match Means a Smaller K
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the tunnel the quality of a sign match changes all the time: a sign close
up and well lit gives a sharp match; a sign far away, dirty or half hidden
behind a truck gives a vague one.

.. figure:: /_static/images/L3/kf_gain_sweep.gif
   :alt: Animation of the three bell curves as the sign match's sigma sweeps from 0.4 to 5.0 m and back, with the prediction fixed at 50 m, sigma 2 m. The orange combined curve slides from the sign match toward the prediction as K falls.
   :width: 70%
   :align: center

   Only the **sign match's** :math:`\sigma` changes, from 0.4 to 5.0 m and
   back; the prediction stays at 50 m with :math:`\sigma = 2` m. When the
   match is much sharper than the prediction, :math:`K` runs up near 1 and the
   orange curve sits right on top of the sign match. As the match gets
   vaguer, :math:`K` falls and the orange curve slides back toward 50. Pause
   it where the sign match's :math:`\sigma` is 1 and you get the numbers
   above: :math:`K = 0.8`, estimate 52.4 m.

**K is recomputed at every sign match: nobody picks it.** There is no if
statement; :math:`K` is a ratio of variances, and it slides smoothly from one
behavior to the other.

One Map Error in Both Answers Does Not Cancel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Combining helps because the prediction's error and the sign match's error are
**unrelated** (independent), so they partly cancel. Now break that, in our
tunnel. Suppose the HD map puts every exit sign **2 m too far along**. The
prediction counted from the last sign, and the sign match uses the same map,
so **both answers are 2 m too far**. Same error, twice.

.. figure:: /_static/images/L3/shared_error.png
   :alt: Three rows on a scale of 46 to 54 m into the tunnel. Each row has a hollow dot (correct map) and an arrow labeled plus 2 m to a filled dot (map 2 m off). Prediction, green: 48.0 to 50.0. Sign match, blue: 51.0 to 53.0. Combined, orange: 50.4 to 52.4, with a plus or minus 0.89 m bar around 52.4 that does not reach 50.4.
   :width: 60%
   :align: center

   A shared error. **Hollow dots** are the answers with a correct map;
   **filled dots** are the same answers with the map 2 m off. Prediction
   (green) moves from 48.0 to 50.0 m, the sign match (blue) from 51.0 to
   53.0 m, and the combined estimate (orange) from 50.4 to 52.4 m. Its
   :math:`\pm 0.89` m bar does not reach the correct 50.4 m.

Mixing cannot remove a shared error: :math:`0.2 \times 2 + 0.8 \times 2 = 2`
m stays. Yet the filter still reports :math:`\pm 0.89` m. Confident and
wrong. That hurts because :math:`\pm 0.89` m is a promise: anything that sizes
a margin from it plans for under a meter of error when the real error is 2 m.
And at the tunnel exit, GNSS, which does not use the map, could fix it, but a
small :math:`\sigma` means a small :math:`K`, so the filter acts on little of
that fix.

**The surprise cannot tell:** :math:`53 - 50` and :math:`51 - 48` are both
3 m. Like bias, only an outside check reveals it. Ask what two sources share:
a map, a clock, a calibration, fog. Today's filter assumes they share nothing.

**To fix it, we need** a source that does not use the map (GNSS at the exit),
and the map's error kept in the **state**, the idea of the next subsection.
Then one good fix corrects every answer that uses the map. The fix, worked
out, is in :doc:`the appendix <l3_appendix>`.


.. _l3-state:

The State
~~~~~~~~~

So far the filter tracked **one number**: the position along the tunnel. A
real filter tracks several at once, kept together as one list.

.. admonition:: Definition: state :math:`\mathbf{x}`
   :class: note

   **The list of numbers that describes the AV at one moment**, such as its
   position and velocity. It must hold everything the motion model needs to
   predict the next moment, **even numbers no sensor measures**.

.. math::

   \mathbf{x} = \begin{bmatrix} p_x & p_y & v_x & v_y \end{bmatrix}^\top

:math:`p_x`: position along the tunnel (east); :math:`p_y`: across it
(north); :math:`v_x`, :math:`v_y`: velocity in the same two directions.

**Velocity is in the state** because the motion model needs it, though no
sensor reports it: the wheel encoders give only speed, not direction (and our
filter does not use them), the IMU gives acceleration, and the sign match
gives position. The filter works velocity out from all of those together.

**The map's 2 m error could be in the state too**: one more number. Sign
matches alone cannot pin it down, since they share it; once a source without
the map arrives, GNSS at the exit, the filter learns it and corrects every
answer that uses the map.

The rule cuts both ways. Anything the filter must reason about over time
belongs in the state; anything else makes it slower and its covariance harder
to keep accurate. Choosing the state is a design decision, and the first
thing people get wrong.

.. note::

   **Notation.** :math:`\hat{\mathbf{x}}` (with a hat) is the filter's
   estimate, never the true value. Bold :math:`\mathbf{x}` is the whole
   state; plain :math:`x` is the along-road coordinate. Only the typeface
   tells them apart.


.. _l3-motion-model:

The Motion Model
~~~~~~~~~~~~~~~~

- **Where we are:** the state, the list of numbers the filter tracks.
- **In this subsection:** the **motion model**, how the filter moves the
  state forward in time.
- **What it is for:** predict, where the AV is now, before the next sign
  match.

.. admonition:: Definition: motion model
   :class: note

   **The rule that predicts the next state from the current one**, using only
   how the AV moves: it does not look at the world (no camera, no sign
   match). No rule is perfect, so it comes with an **error**.

.. math::

   \underbrace{\mathbf{x}_k}_{\text{the state now}}
   \;=\; \underbrace{F\,\mathbf{x}_{k-1}}_{\text{where the motion rule puts us}}
   \;+\; \underbrace{\mathbf{w}}_{\text{the rule's error, this step}}

**k is the step count.** The filter takes one step every
:math:`\Delta t = 0.1` s: :math:`\mathbf{x}_k` is the state now,
:math:`\mathbf{x}_{k-1}` the state one step earlier. In plain words: where you
are now is where the rule says, plus however wrong the rule was this time.
:math:`F` is the motion rule. At constant speed the new position is the old
position plus speed times :math:`\Delta t`: 10 m/s for a tenth of a second is
1 m further. :math:`\mathbf{w}` is how wrong that rule is each step. The AV
speeds up, brakes and turns, and the rule knows nothing about that. The AV
never sees :math:`\mathbf{w}`.

The Motion Model: All the Pieces in One Equation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add one term to the rule: :math:`B\,\mathbf{u}_k`, what the AV **knows** it
did this step, such as speeding up or braking, read from the IMU. (Turning
needs the EKF, later.)

.. math::

   \mathbf{x}_k \;=\; F\,\mathbf{x}_{k-1} \;+\; B\,\mathbf{u}_k \;+\; \mathbf{w},
   \qquad \mathbf{w} \sim \mathcal{N}(0,\,Q)

:math:`\sim \mathcal{N}(0, Q)` reads "drawn from a bell curve (Gaussian)
**centered on 0**, with **covariance** :math:`Q`". Our example, with numbers
we chose, for one step of 0.1 s: the AV is 100 m east and 20 m north, driving
east at 10 m/s, and the IMU reads a brake of 1 m/s².

.. list-table::
   :widths: 10 40 50
   :header-rows: 1
   :class: compact-table

   * -
     - **What it is**
     - **In our example**
   * - :math:`\mathbf{x}_{k-1}`
     - the state one step ago
     - :math:`p_x = 100` m, :math:`p_y = 20` m, :math:`v_x = 10` m/s,
       :math:`v_y = 0`
   * - :math:`F`
     - the motion rule
     - constant velocity: :math:`p_x + 0.1\,v_x`, and so on
   * - :math:`\mathbf{u}_k`
     - what the AV knows it did (control input)
     - IMU: braking, :math:`[-1,\ 0]` m/s²
   * - :math:`B`
     - turns :math:`\mathbf{u}` into state changes
     - position :math:`+\tfrac{1}{2}\Delta t^2 a`, velocity
       :math:`+\Delta t\,a`
   * - :math:`\mathbf{w}`
     - what is left over, **unknown**
     - IMU noise, tire slip
   * - :math:`Q`
     - how big :math:`\mathbf{w}` usually is
     - what the IMU misses: we chose :math:`\sigma_a = 0.5` m/s²

The brake is no longer in :math:`\mathbf{w}`; it went into
:math:`B\mathbf{u}`, so :math:`Q` only covers what the IMU misses: in the
hands-on, :math:`\sigma_a = 0.5` m/s², chosen and then tuned. Without
:math:`B\mathbf{u}`, :math:`Q` would have to cover the brake too, 1 m/s²
(the appendix works out both, and the brake step in detail). Its usual name,
**process noise**, sounds physical, but it is model error: how inaccurate
:math:`F` is. Nobody measures it. We choose it, and then we tune it.

The filter never knows this step's :math:`\mathbf{w}`. So how can it predict
with this equation?

The Predicted State
^^^^^^^^^^^^^^^^^^^

The motion model gives the **true** state, but it needs two things the filter
never has: the true :math:`\mathbf{x}_{k-1}` and this step's
:math:`\mathbf{w}`. So the filter puts in its best guess for each:

.. math::

   \text{true:}\quad \mathbf{x}_k \;=\; F\,\mathbf{x}_{k-1} + B\,\mathbf{u}_k + \mathbf{w}

.. math::

   \text{predicted:}\quad
   \hat{\mathbf{x}}^-_k \;=\; F\,\underbrace{\hat{\mathbf{x}}_{k-1}}_{\text{last estimate}} \;+\; B\,\mathbf{u}_k
   \;+\; \underbrace{0}_{\mathbf{w}\text{'s average}}

- :math:`\mathbf{x}_{k-1}` **becomes** :math:`\hat{\mathbf{x}}_{k-1}`: the
  true state is unknown, so we use our last **estimate** (the hat).
- :math:`\mathbf{w}` **becomes 0.** :math:`\mathbf{w}` is not really zero: in
  the hands-on it is a few centimeters per second on almost every step,
  +0.027, then -0.046. But it comes from a bell curve **centered on 0**, as
  likely to push the AV ahead as back. If we must pick one number, the best is
  the center. Any other number would bet on a direction we have no reason to
  pick. **It is not dropped:** its size enters the uncertainty, as
  :math:`+Q`, next.
- **The minus on** :math:`\hat{\mathbf{x}}^-` means **predicted**: before the
  next sign match corrects it.

**Our step:** last estimate :math:`[100,\ 20,\ 10,\ 0]`, braking at
:math:`a = -1` m/s². :math:`B\mathbf{u}_k` adds
:math:`\tfrac12\Delta t^2 a = \tfrac12 \times 0.1^2 \times (-1) = -0.005` m to
the position and :math:`\Delta t\,a = -0.1` m/s to the velocity:

.. math::

   F\hat{\mathbf{x}}_{k-1} + B\mathbf{u}_k = [101,\ 20,\ 10,\ 0] + [-0.005,\ 0,\ -0.1,\ 0]
   = [\mathbf{100.995},\ 20,\ \mathbf{9.9},\ 0]

.. _l3-predicted-uncertainty:

The Predicted Uncertainty
^^^^^^^^^^^^^^^^^^^^^^^^^

:math:`\mathbf{w}` added 0 to the predicted state. Its **size**, :math:`Q`,
goes into the uncertainty here:

.. math::

   \underbrace{P^-_k}_{\text{predicted uncertainty}}
   \;=\; \underbrace{F P_{k-1} F^\top}_{\text{old uncertainty, moved by the rule}}
   \;+\; \underbrace{Q}_{\text{size of } \mathbf{w}}

- **Why** :math:`F` **twice.** It is the rule from the new-sigma step above:
  scale an error by :math:`f` and its variance scales by :math:`f^2`, as each
  weight was squared there. With a matrix, "squared" is :math:`F` on the left
  and :math:`F^\top` on the right.
- **What** :math:`FPF^\top` **does.** The new position error is the old one
  plus :math:`\Delta t` times the velocity error. A velocity error leaks into
  position, and the two become linked: the off-diagonal terms the covariance
  summary promised would appear on their own. In the hands-on, 22 predict
  steps with no sign match take the position :math:`\sigma` along the tunnel
  from 0.81 to **1.35 m**, mostly through :math:`FPF^\top`: without
  :math:`Q` it would still reach 1.32 m.
- **Why** :math:`+Q` **always adds.** :math:`\mathbf{w}` is a brand new
  error, independent of the old one, so variances add. :math:`Q` mostly feeds
  the **speed** error, which :math:`FPF^\top` then leaks into position at the
  next step. With no sign match, :math:`P` only grows. This is the rising edge
  of the sawtooth you meet below. Predict in code is in
  :doc:`the appendix <l3_appendix>`.


.. _l3-measurement-model:

The Measurement Model
~~~~~~~~~~~~~~~~~~~~~

- **Where we are:** the motion model predicts where the AV is now.
- **In this subsection:** the **measurement model**, what a sensor should
  read if the state is right.
- **What it is for:** comparing that expected reading with the real one gives
  the surprise.

.. admonition:: Definition: measurement model
   :class: note

   **The rule that predicts what a sensor should read**, given the state at
   the same instant. No sensor is exact, so it comes with an **error**.

.. math::

   \underbrace{\mathbf{z}_k}_{\text{the reading}}
   \;=\; \underbrace{H\,\mathbf{x}_k}_{\text{the part of the state it sees}}
   \;+\; \underbrace{\mathbf{v}}_{\text{its error}}

Many books call it the observation model. People often read it backwards, so
go slowly. It answers one thing: if the state really were
:math:`\mathbf{x}_k`, what should the sensor read right now?

- **Same** :math:`k` **on both sides:** no time passes. Moving through time is
  the motion model's job, which is why the motion model always runs first.
  Put in its prediction :math:`\hat{\mathbf{x}}^-`, and
  :math:`H\hat{\mathbf{x}}^-` is the reading we **expect**.
- **It runs one way only:** state to expected reading, never a reading into a
  position. The gap between the reading we expected and the one we got is the
  surprise from the Kalman gain example.

How H, v and R Fit Together
^^^^^^^^^^^^^^^^^^^^^^^^^^^

One equation for any sensor: the reading is the part of the state the sensor
sees, plus the sensor's error this time.

.. math::

   \mathbf{z}_k \;=\; H\,\mathbf{x}_k \;+\; \mathbf{v},
   \qquad \mathbf{v} \sim \mathcal{N}(0,\,R)

.. list-table::
   :widths: 10 40 50
   :header-rows: 1
   :class: compact-table

   * -
     - **What it is**
     - **In our example**
   * - :math:`\mathbf{z}_k`
     - what the sensor reports
     - sign match: the AV at :math:`(102.4,\ 19.1)` m
   * - :math:`\mathbf{x}_k`
     - the **true** state, same instant
     - :math:`[100.995,\ 20,\ 9.9,\ 0]`, after the braking step
   * - :math:`H`
     - keeps what the sensor sees, 2 by 4
     - keeps :math:`p_x`, :math:`p_y`; drops velocity, which it cannot see
   * - :math:`\mathbf{v}`
     - this reading's error, **unknown**
     - :math:`102.4 - 100.995 = 1.405` and :math:`19.1 - 20 = -0.9` m
   * - :math:`R`
     - how big :math:`\mathbf{v}` usually is
     - :math:`\sigma = 1` m per axis, so 1 m² (we chose it)

:math:`\mathbf{x}_k` is where the AV **really** is, not where the filter
thinks it is: the model describes reality. :math:`H` is 2 by 4 because two
readings come out and four state numbers go in. :math:`\mathbf{v}`, measured
minus true, can be computed here only because the example gives us the true
state; on the road the AV never can.

**The filter has neither** :math:`\mathbf{x}_k` **nor** :math:`\mathbf{v}`,
so, as for the predicted state, it puts in its best guess for each: its
prediction :math:`\hat{\mathbf{x}}^-` and :math:`\mathbf{v}`'s average, 0.
That gives the **expected reading**:
:math:`H\hat{\mathbf{x}}^- + 0 = (100.995,\ 20)` m.

.. note::

   Here :math:`\hat{\mathbf{x}}^-` equals the true state only because we chose
   an exact last estimate and an exact IMU (:math:`\mathbf{w} = 0` this
   step). In the hands-on they differ by 0.34 m along and 0.32 m across. Also
   in the hands-on, the sign match is sharper across the tunnel, 20 cm, so
   :math:`R` is 1 along and 0.04 across.

The Measurement Model, Seen from Above
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/meas_model.png
   :alt: Top view to scale, east 98 to 106 m, north 18 to 22 m, with six numbered tags. A faded AV faces east with its base link on a green dot at (100.995, 20), tag 1. A blue cross at (102.4, 19.1), tag 2. An arrow between them, tag 3. Arrows of 1 m each way and a dashed 1 m circle, tag 4. A dashed velocity arrow ahead of the AV, tag 5. A dashed 2 m circle, tag 6. Sixty faint blue dots scatter around the green dot.
   :width: 60%
   :align: center

   The same step from above, to scale.
   **1. Expected**, :math:`H\hat{\mathbf{x}}^- = (100.995,\ 20)` m: where
   the sign match *should* place the AV (the green dot, with the AV drawn
   there).
   **2. Measured**, :math:`\mathbf{z} = (102.4,\ 19.1)` m: where it *did*
   (the blue cross).
   **3. The surprise**, :math:`\mathbf{z} - H\hat{\mathbf{x}}^- = (1.405,\
   -0.9)` m (the arrow).
   **4.** :math:`R`: :math:`\pm\sigma = 1` m each way, a *typical* error, not
   a limit. The faint dots are where sign matches would place the AV if the
   prediction were right; about 4 in 10 land inside :math:`1\sigma` (here 27
   of 60).
   **5. Velocity**, 9.9 m/s: in the state, but :math:`H` drops it; a sign
   match cannot see speed.
   **6. The** :math:`2\sigma` **circle** (2 m): outside it is *unusual*,
   about 1 in 7 (here 10 of 60). The measurement is
   :math:`\sqrt{1.405^2 + 0.9^2} = 1.67` m out, inside it: **ordinary**.

Why only 4 in 10 inside one sigma? In two dimensions a circle of radius
:math:`r` holds :math:`1 - e^{-r^2/2\sigma^2}` of the readings: 39 percent at
:math:`1\sigma`, 86 percent at :math:`2\sigma`. That is less than the 68 and
95 percent of one dimension, because a reading can miss two ways at once (see
"How far out is unusual" in :doc:`the appendix <l3_appendix>`).

.. important::

   **The filter cannot know** :math:`\mathbf{v}`: :math:`\mathbf{v} =
   \mathbf{z} - H\mathbf{x}` needs the true state, the very thing it is
   looking for. If it knew :math:`\mathbf{v}`, it would already know where the
   AV is. So it uses :math:`\mathbf{v}`'s average, zero (the expected reading
   :math:`H\hat{\mathbf{x}}^-`), and its size, :math:`R` (how big a surprise
   to expect). Here the surprise equals :math:`\mathbf{v}` only because the
   prediction is the true state; in general it mixes both errors, which the
   gain untangles. The measurement model in detail is in
   :doc:`the appendix <l3_appendix>`.


.. _l3-predict:

Predict
~~~~~~~

- **Where we are:** the two models, motion and measurement.
- **In this subsection:** **predict**, the two lines that carry the estimate
  and its uncertainty forward.
- **What it is for:** between sensor readings, this is all the filter can do.

.. admonition:: Definition: predict
   :class: note

   **The first half of every cycle**: move the estimate forward one time step
   with the motion model, before any measurement arrives.

.. math::

   \underbrace{\hat{\mathbf{x}}^- = F\hat{\mathbf{x}} + B\mathbf{u}}_{\text{predict the state}}
   \qquad\qquad
   \underbrace{P^- = F P F^\top + Q}_{\text{grow the uncertainty}}

The filter runs in two steps, one subsection each, so nobody reads ten
equations at once. Predict carries the estimate forward in time, and that is
all. Nothing that sees the world is involved: only the motion model and what
the AV knows it did. The left line predicts the state. The right line moves
the uncertainty: :math:`FPF^\top` is the old uncertainty carried forward
(move an uncertain thing, and its uncertainty moves too), and :math:`+Q` adds
the model's usual error for this step.

.. important::

   :math:`P` **always grows here:** time passed and nothing outside the AV was
   measured. No version of predict makes you more precise. In the tunnel this
   runs every 0.1 s, about 22 times between two sign matches. The minus means
   *predicted, not yet corrected*; once the measurement is folded in, the minus
   drops off.

Before Predict: the Belief after a Sign Match
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These numbers come from the hands-on (:ref:`l3-kf-hands-on`) at
:math:`t = 7.1` s, just after a sign match. In both panels, the shaded ellipse
is the filter's uncertainty :math:`P` (:math:`1\sigma`) around its estimate,
the dot.

.. list-table::
   :widths: 50 50
   :class: compact-table

   * - .. figure:: /_static/images/L3/belief_top.png
          :alt: Top view measured from the estimate, along minus 1.3 to 1.3 m, across minus 0.5 to 0.5 m. An orange ellipse 0.81 m to each side along and 0.18 m across. Tag 1: the dot at the center. Tag 2: the arrow along. Tag 3: the arrow across. Tag 4: a black plus 0.63 m ahead, inside the ellipse.
          :width: 100%
          :align: center

          **From above** (along against across, m).
          **1** The estimate: where the filter thinks the AV is.
          **2** :math:`\pm\sigma` along: **0.81 m**.
          **3** :math:`\pm\sigma` across: only **0.18 m**; a sign on the wall
          fixes the distance to the wall best.
          **4** Where the AV really is: 0.63 m ahead, **inside** the ellipse
          (0.79σ out). The filter never sees it.
     - .. figure:: /_static/images/L3/belief_tilt.png
          :alt: Position along the tunnel, minus 1.3 to 1.3 m, against speed, minus 0.5 to 0.5 m/s, measured from the estimate. An orange ellipse tilted up to the right with a dashed line along the tilt. Tag 1: the dot. Tag 5: the dashed line. Tag 4: a black plus 0.63 m ahead and 0.02 m/s slower, just outside.
          :width: 100%
          :align: center

          **Position against speed** (along in m, speed in m/s).
          **1** The same estimate; :math:`\sigma` of speed: **0.30 m/s**.
          **4** The same AV: ahead but 0.02 m/s slower, against the tilt: just
          **outside** (1.06σ), which is normal.
          **5** The **tilt**, correlation +0.63: each predict adds speed
          :math:`\times\,\Delta t` to the position.

In words: "I know how far I am from the wall, not how far along." And: "if I
am further along than I think, I am probably faster too." That link lets one
sign match correct the speed, which no sign can measure. An AV just outside a
1σ ellipse is ordinary: in two dimensions a 1σ ellipse holds only 39 percent.

After Predict: 22 Steps, No Sign Match
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now 22 predict steps (2.2 s) run with no sign match, giving the prediction for
:math:`t = 9.3` s. The estimate moved 25.8 m along the tunnel:
:math:`F\hat{\mathbf{x}} + B\mathbf{u}`, 22 times over. Shaded green is its
uncertainty :math:`P^-` (:math:`1\sigma`); dotted orange is the belief from
before predict.

.. list-table::
   :widths: 50 50
   :class: compact-table

   * - .. figure:: /_static/images/L3/predict_top.png
          :alt: Top view from the estimate, along minus 2 to 2 m, across minus 0.75 to 0.75 m. A green ellipse 1.35 m along and 0.44 m across around a dotted orange 0.81 by 0.18 m ellipse. Tag 1: the dot. Tag 2: the arrow along. Tag 3: the arrow across. Tag 4: a black plus 0.34 m ahead and 0.32 m left, inside the green ellipse. Tag 6: the dotted ellipse.
          :width: 100%
          :align: center

          **From above.**
          **1** The prediction: :math:`F\hat{\mathbf{x}} + B\mathbf{u}`, 22
          times.
          **2** :math:`\pm\sigma` along: 0.81 to **1.35 m**.
          **3** :math:`\pm\sigma` across: 0.18 to **0.44 m**.
          **4** The AV: inside; the ellipse grew to cover it.
          **6** The belief before predict, for comparison.
          *"With no sign, I am less sure where I am: by about half a meter
          along, a quarter meter across."*
     - .. figure:: /_static/images/L3/predict_tilt.png
          :alt: Position along the tunnel against speed, from the estimate. A green ellipse, longer and more tilted than a dotted orange one inside it, with a dashed line along the tilt. Tag 1: the dot. Tag 5: the dashed line. Tag 4: a black plus 0.34 m ahead and 0.20 m/s slower, just outside the green ellipse. Tag 6: the dotted ellipse.
          :width: 100%
          :align: center

          **Position against speed.**
          **1** The same prediction; :math:`\sigma` of speed 0.30 to 0.38 m/s.
          **4** The AV: ahead but slower, against the tilt: just outside,
          normal.
          **5** **More tilted:** correlation +0.63 to +0.79.
          *"Each step turns a speed error into a position error, so the two
          are more linked."*

The uncertainty grew most along the tunnel. Along it, :math:`Q` must cover the
IMU's bias as well as its noise, and an AV in its lane barely moves sideways.
The tilt grew because every step adds speed times :math:`\Delta t` to the
position, so a speed error becomes a position error. Nobody typed that
correlation in; predict put it there.


.. _l3-update:

Update
~~~~~~

- **Where we are:** predict moved the estimate forward and grew :math:`P`.
- **In this subsection:** the **update**: the surprise, the gain, the new
  estimate and the new :math:`P`.
- **What it is for:** the surprise :math:`\boldsymbol{\nu}` is **the only new
  information in the whole cycle**.

.. admonition:: Definition: update
   :class: note

   **The second half of every cycle**: correct the prediction with a
   measurement, by acting on part of the surprise.

.. math::

   \underbrace{\boldsymbol{\nu}}_{\text{the surprise}}
   \;=\; \underbrace{\mathbf{z}}_{\text{what we got}}
   \;-\; \underbrace{H\hat{\mathbf{x}}^-}_{\text{what we expected}}
   \qquad\qquad
   \underbrace{S}_{\text{how big we expected the surprise to be}}
   \;=\; H P^- H^\top + R

The surprise :math:`\boldsymbol{\nu}`, the **innovation**, is what we got minus
what we expected. What we expected is the measurement model run on our
prediction. It is the same surprise as in the Kalman gain example,
:math:`z - \hat{x}^-`, now with :math:`H`. Everything else in the update is
built from numbers we already had. If :math:`\boldsymbol{\nu}` is zero, the
sensor told us nothing new, and the estimate will not move.

:math:`S` is how big we expected the surprise to be, before we saw it. Two
things feed it: how uncertain we were about the reading (our covariance pushed
through :math:`H`) and how noisy the sensor is (:math:`R`). It is the bottom
of :math:`K` in the one-number gain,
:math:`\sigma_{\text{pred}}^2 + \sigma_{\text{meas}}^2`, written with
matrices. In the gain, it turns a raw disagreement in meters into a fraction.

The Gain K with One Number: Act on 65 Percent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The sign match arrives at :math:`t = 9.3` s. Take one number, the position
along the tunnel. Every number here is one we already have. From the
after-predict panels, the prediction is 110.41 m with :math:`\sigma = 1.35`
m, so :math:`P^- = 1.35^2 = 1.84` m². The sign match reads 111.15 m with
:math:`\sigma = 1` m, so :math:`R = 1` m². The surprise is
:math:`111.15 - 110.41 = 0.74` m.

.. math::

   K \;=\; \frac{P^-}{P^- + R} \;=\; \frac{1.84}{1.84 + 1} \;=\; \mathbf{0.65}

:math:`K` is the prediction's share of the total variance. The prediction
(:math:`\sigma \approx 1.35` m) is less certain than the sign match (1 m), so
the estimate moves **65 percent of the surprise**, 0.48 of 0.74 m.

.. figure:: /_static/images/L3/gain_one.png
   :alt: Three bell curves along the tunnel, 106 to 115 m. Green: prediction, 110.41 m, sigma 1.35 m. Blue: sign match, 111.15 m, sigma 1 m. Orange: new estimate, 110.89 m, sigma 0.80 m, the tallest. Below, a black arrow from the prediction to the sign match, surprise 0.74 m, and a shorter orange arrow to the new estimate, moved 0.48 m: K equals 0.65 of it.
   :width: 75%
   :align: center

   The update at 9.3 s along the tunnel. **Green**: the prediction, 110.41 m,
   :math:`\sigma = 1.35` m. **Blue**: the sign match, 111.15 m,
   :math:`\sigma = 1` m. **Orange**: the new estimate, 110.89 m,
   :math:`\sigma = 0.80` m. The **black arrow** is the surprise, 0.74 m; the
   shorter **orange arrow** is the move, 0.48 m, which is :math:`K = 0.65` of
   it.

**K is recomputed at every sign match**, from that moment's :math:`P^-`. The
longer the AV drives without a sign match, the more :math:`P^-` grows, so the
next sign match gets a bigger :math:`K` and moves the estimate further. At the
extremes, :math:`R = 0` gives :math:`K = 1`, and a huge :math:`R` gives
:math:`K = 0`.

The Gain K with Matrices: the Same Fraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now the state has four numbers (:math:`p_x, p_y, v_x, v_y`) and the sign
match gives two (east, north). Each piece of :math:`K = P^- / (P^- + R)` grows
into a matrix:

.. math::

   K \;=\; P^- H^\top \, S^{-1}, \qquad S \;=\; H P^- H^\top + R

- **The bottom,** :math:`P^- + R`, **becomes** :math:`S = HP^-H^\top + R`.
  The sensor sees only :math:`H\mathbf{x}`, so what matters is the
  prediction's uncertainty *about the reading*: :math:`P^-` seen through
  :math:`H`, which puts :math:`H` on both sides, as the squared-size rule put
  :math:`F` on both sides of :math:`FPF^\top`. Then add the sensor's own
  :math:`R`.
- **Dividing becomes** :math:`S^{-1}`. You cannot divide by a matrix;
  multiplying by its inverse does it.
- **The top,** :math:`P^-`, **becomes** :math:`P^-H^\top`: how *every* state
  number goes with what the sensor sees, including the ones it never
  measures, like speed. That is why :math:`K` has speed rows that are not
  zero.

With one number and :math:`H = 1`, the matrix form gives back
:math:`P^- / (P^- + R)` exactly.

The Gain K at 9.3 s: One Row per State Number
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:math:`K` is computed **once** per sign match, as one matrix: one **row** per
state number, one **column** per reading. Each entry says how much of that
reading's surprise moves that state number. East and north are not linked in
:math:`P^-`, so each entry reduces to a simple fraction.

- :math:`p_x`, **east**: **0.65** of the east surprise,
  :math:`1.84 / (1.84 + 1)`, the one-number gain.
- :math:`p_y`, **north**: **0.83** of the north surprise,
  :math:`0.19 / (0.19 + 0.04)`. Across the tunnel the sign match is sharp,
  so we trust it more.
- :math:`v_x`, **east speed**: **0.14** of the east surprise,
  :math:`0.40 / 2.84`, the tilt over :math:`S`.
- :math:`v_y`, **north speed**: 0.29 of the north surprise,
  :math:`0.068 / 0.23`, the same link, across.

The tilt is the position-speed covariance predict built:
:math:`0.79 \times 1.35 \times 0.38 = 0.40`. We chose
:math:`R = \operatorname{diag}(1,\ 0.2^2) = \operatorname{diag}(1,\ 0.04)` m²,
0.2 m across, because the sign is on the wall right beside the AV. As one
matrix:

.. math::

   K = \begin{bmatrix} 0.65 & 0 \\ 0 & 0.83 \\ 0.14 & 0 \\ 0 & 0.29 \end{bmatrix}

**The speed rows are not zero**, although a sign match never measures speed.
Predict tied speed to position (correlation +0.79): further along goes with
faster, so a position surprise also corrects speed. The zeros say east and
north are not linked, so an east surprise changes nothing north.

The New Estimate: Prediction plus K Times the Surprise
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We now have the prediction :math:`\hat{\mathbf{x}}^-`, the surprise
:math:`\boldsymbol{\nu}` and the gain :math:`K`. One line combines them:

.. math::

   \underbrace{\hat{\mathbf{x}}}_{\text{new estimate}} \;=\;
   \underbrace{\hat{\mathbf{x}}^-}_{\text{prediction}} \;+\;
   \underbrace{K}_{\text{gain}}\ \underbrace{\boldsymbol{\nu}}_{\text{surprise}}

Row by row (prediction + gain :math:`\times` surprise = new estimate):

- :math:`p_x`, east: :math:`110.41 + 0.65 \times 0.74 = 110.41 + 0.48 =`
  **110.89 m**
- :math:`p_y`, north: :math:`-2.09 + 0.83 \times 0.14 = -2.09 + 0.11 =`
  **-1.98 m**
- :math:`v_x`, speed: :math:`10.90 + 0.14 \times 0.74 = 10.90 + 0.10 =`
  **11.01 m/s**
- :math:`v_y`, speed: :math:`-0.37 + 0.29 \times 0.14 = -0.37 + 0.04 =`
  **-0.33 m/s**

The surprise in each row is the one from
the reading whose :math:`K` entry is not zero: east for :math:`p_x` and
:math:`v_x`, north for :math:`p_y` and :math:`v_y`. The position moves
**part of the way**, 0.48 of 0.74 m, because the sign match is noisy too. The
speed has no surprise of its own: it uses the **east position** surprise,
through the tilt, :math:`0.14 \times 0.74 = 0.10` m/s.

The New Uncertainty: P Shrinks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

   \underbrace{P}_{\text{new uncertainty}} \;=\; (I - KH)\,\underbrace{P^-}_{\text{prediction's}}
   \qquad \text{one number:}\quad P = (1 - K)\,P^-

The one-number form is the shortcut from the new-sigma step.

- **Along** (:math:`p_x`): :math:`K = 0.65`, so
  :math:`P = 0.35 \times 1.84 = 0.65` m², and :math:`\sigma` goes from 1.35
  to **0.80 m**.
- **Across** (:math:`p_y`): :math:`K = 0.83`, so
  :math:`P = 0.17 \times 0.19 = 0.033` m², and :math:`\sigma` goes from 0.44
  to **0.18 m**.

:math:`KH` is the share of the uncertainty the sign match removed, so
:math:`I - KH` is the share that survives (:math:`I`, the identity, means
"keep everything"). Across the tunnel the gain was bigger, so much less
survives.

.. danger::

   **Look for the surprise** :math:`\boldsymbol{\nu}` **in this line: it is
   not there.** The new :math:`P` depends only on :math:`K` and :math:`P^-`,
   and neither looks at what the sensor actually said. So :math:`P` shrinks by
   exactly the same amount whether the reading was good or wildly wrong. The
   filter does not check. That one fact is what divergence is made of, and it
   comes back in the EKF section.

With more than one sensor, run the update once per sensor, each with its own
:math:`H` and :math:`R`.

After Update: the Sign Match Pulls It In
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:math:`t = 9.3` s, right after the sign match. Axes are measured from the
prediction. Dotted green is the prediction :math:`P^-` from the after-predict
panels; shaded orange is the new belief :math:`P` (:math:`1\sigma`) around the
new estimate.

.. list-table::
   :widths: 50 50
   :class: compact-table

   * - .. figure:: /_static/images/L3/update_top.png
          :alt: Top view from the prediction, along minus 2 to 2 m, across minus 0.75 to 0.75 m. A dotted green ellipse around the prediction, tag 6. A blue cross 0.74 m ahead, tag 7. A smaller shaded orange ellipse around a dot 0.48 m ahead, tag 1, with arrows along, tag 2, and across, tag 3. A black plus 0.34 m ahead and 0.32 m left, just above the orange ellipse, tag 4.
          :width: 100%
          :align: center

          **From above.**
          **7** The sign match: 0.74 m ahead.
          **1** New estimate: moved **0.48 m**, :math:`K = 0.65` of it.
          **2** :math:`\pm\sigma` along: 1.35 to **0.80 m**.
          **3** :math:`\pm\sigma` across: 0.44 to **0.18 m**, the sharpest.
          **4** The AV: just outside, 1.1σ; normal.
          **6** The prediction, for comparison.
          *"I moved toward the sign, part of the way, and I am surer now."*
     - .. figure:: /_static/images/L3/update_tilt.png
          :alt: Position along the tunnel against speed, from the prediction. A dotted green tilted ellipse, tag 6. A dashed blue vertical line 0.74 m ahead, the sign match, tag 7. A smaller shaded orange tilted ellipse around a dot 0.48 m ahead and 0.10 m/s faster, tag 1, with a dashed line along its tilt, tag 5. A black plus 0.34 m ahead and 0.20 m/s slower, just outside, tag 4.
          :width: 100%
          :align: center

          **Position against speed.**
          **7** The sign match: a **line**, position only, any speed.
          **1** Yet the speed moved too: **+0.10 m/s**.
          **5** Through the tilt: further along goes with faster. Correlation
          +0.79 to +0.60.
          **4** The AV: just outside, 1.2σ; normal.
          *"A sign cannot see speed, but the link corrected it anyway."*

The update used up part of the tilt: the correlation fell from 0.79 to 0.60.
The AV sits just outside both ellipses, about 1.2σ, which is normal for a 1σ
ellipse that holds only about 39 percent.


.. _l3-whole-cycle:

The Whole Cycle
~~~~~~~~~~~~~~~

.. admonition:: Where that leaves us: the Kalman filter, one cycle
   :class: tip

   .. list-table::
      :widths: 12 34 28 26
      :header-rows: 1
      :class: compact-table

      * -
        - **What we did**
        - **Computed**
        - **What it is**
      * - **Predict**
        - Moved the estimate one step with the motion model.
        - :math:`\hat{\mathbf{x}}^- = F\hat{\mathbf{x}} + B\mathbf{u}`
        - predicted state, :math:`\mathbf{w} = 0`
      * -
        -
        - :math:`P^- = FPF^\top + Q`
        - **grows** by :math:`Q`
      * - **Update**
        - A sign match arrived. Compared it with what we expected, then acted
          on part of the difference.
        - :math:`\boldsymbol{\nu} = \mathbf{z} - H\hat{\mathbf{x}}^-`
        - the surprise
      * -
        -
        - :math:`S = HP^-H^\top + R`
        - its expected size
      * -
        -
        - :math:`K = P^-H^\top S^{-1}`
        - how much to act on
      * -
        -
        - :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^- + K\boldsymbol{\nu}`
        - new estimate
      * -
        -
        - :math:`P = (I - KH)\,P^-`
        - **shrinks**

   Then this step's :math:`\hat{\mathbf{x}}` and :math:`P` become the next
   step's starting point. Grow, shrink, grow, shrink, for as long as the AV
   drives. Now go back to the textbook diagram at the top of this section:
   you can read every line of it.

Over Many Cycles, the Uncertainty Settles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One picture for the whole section: what happens to the uncertainty over many
cycles, in a simplified tunnel (position only, predict at 10 Hz, a sign match
every 2.5 s). The hands-on numbers differ a little, but the shape is the same.

.. figure:: /_static/images/L3/kf_sawtooth.png
   :alt: Sigma on position, 0 to 3.6 m, against time, 0 to 12.5 s. Tag 1: a solid sawtooth climbing from 1.000 to 1.756 m over 2.5 s. Tag 2: the drop at 2.5 s to 0.869 m. Tag 3: later teeth settling between about 0.9 and 2.0 m. Tag 4: a dashed curve that keeps rising and leaves the chart at about 5.4 s. Tag 5: a dotted horizontal line at 1 m.
   :width: 75%
   :align: center

   The sawtooth.
   **1. Predict** runs every 0.1 s, so 25 times before the first sign:
   :math:`\sigma` climbs from 1.000 to 1.756 m. Nothing measured position.
   **2. Update**, a sign match: 1.756 to 0.869 m, with :math:`K = 0.755`.
   **3. Settles** between about 0.9 and 2.0 m: the growth and the shrink
   cancel.
   **4. The IMU alone**, no sign matches: it passes 2 m at 3 s and grows
   without limit. That is IMU drift.
   **5. The latest sign alone**, ignoring the prediction:
   :math:`\sigma = 1` m. Right after each match the filter is *below* it,
   about 0.89 m, because combining beats either source.

   Climb, drop, climb, drop: that sawtooth is the Kalman filter.



.. _l3-four-assumptions:

What We Assumed
~~~~~~~~~~~~~~~

- **Where we are:** the Kalman filter, one full cycle.
- **In this subsection:** the four assumptions the filter made, without
  saying so.
- **What it is for:** under all four, the filter is **provably the best
  possible**: no method has a smaller average squared error.

.. list-table::
   :widths: 22 34 44
   :header-rows: 1
   :class: compact-table

   * - **Assumption**
     - **In plain words**
     - **Breaks in the tunnel when**
   * - **Linear** (:math:`F`, :math:`H` matrices)
     - new numbers are old ones scaled and added
     - the state uses heading and speed (an AV that turns): position then
       needs :math:`\cos` and :math:`\sin` of the heading (EKF, next)
   * - **Bell curve** (:math:`\mathcal{N}`)
     - one peak; errors usually small, rarely large
     - two identical lights: two places the AV could be (particle filter)
   * - **No bias, no memory** (the 0; a fresh :math:`\mathbf{w}`,
       :math:`\mathbf{v}` each step)
     - errors as often high as low, unrelated from step to step and to each
       other
     - the HD map is 2 m off: every sign match shares it
   * - :math:`Q`, :math:`R` **known**
     - we know how big the errors are
     - always partly: :math:`Q` is chosen, then tuned

Our tunnel state, positions and velocities in :math:`x` and :math:`y`, stays
linear even in a turn. But once the state carries heading and speed, as on a
curve, position needs the cosine and sine of the heading, and no fixed matrix
times the state gives a cosine. Textbooks call the third assumption
**zero-mean white noise**. :math:`R` can be measured; :math:`Q` is chosen and
tuned.

If only the bell curve fails, the filter is still the best *linear*
estimator; it is no longer the best of all. The appendix checks each
assumption on a real AV (:doc:`l3_appendix`).


.. _l3-kf-check:

Check: the Kalman Filter
~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Answer each one before you open the answers
   :class: hint

   1. The AV drives 3 s with no sign match. What happens to :math:`P` (the
      uncertainty of the estimate), and which term does it?
   2. The sign match is much more precise than the prediction. Is :math:`K`
      near 0 or near 1?
   3. The sign match reads position only. How can the update change the
      **speed**?
   4. You set :math:`Q` far too small. What does the filter report, and what
      does the error do?

.. dropdown:: Check: the Kalman filter. Answers
   :color: success
   :icon: check-circle

   1. :math:`P` **grows at every predict step**, mostly through
      :math:`FPF^\top`: the speed uncertainty leaks into position every step,
      and :math:`+Q` keeps feeding the speed uncertainty. With no sign match
      there is no update to shrink it again. That is the rising edge of the
      sawtooth.
   2. **Near 1.** :math:`K` compares the two uncertainties. If the sign match
      is much more precise than the prediction, trust the match: the estimate
      jumps most of the way to the reading.
   3. **Through** :math:`P`. Predict builds a link between position and
      speed, because position is where speed took you. :math:`K` has a speed
      row, so a position surprise corrects speed too. The measurement never
      saw speed; the covariance carried the correction there.
   4. :math:`Q` is how wrong the filter expects its own prediction to be at
      each step. :math:`Q` too small tells the filter its motion model is
      almost perfect. Its uncertainty hardly grows, it reports a thin band,
      and it trusts its prediction over the sign matches. But the real IMU
      still has noise and a bias, so the true error keeps growing and walks
      right out of the band. That is **overconfidence**: the filter is most
      confident exactly when it is wrong. It is the dangerous failure, because
      everything downstream trusts that small :math:`\sigma`. Step 4 of the
      hands-on makes it happen.


.. _l3-kf-hands-on:

Hands-On: the Tunnel Kalman Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now watch the filter run on a simulated tunnel drive. Everything is in the
course repository,
`github.com/rubixcubic/enpm818z-fall-2026-carla-python
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python>`_, folder
``lecture3/tunnel_kf/``. (Every L3 script and the ROS 2 package are listed on
the :doc:`l3_code` page.) It holds three files:

- ``kf_tunnel.py``: **the one script**. It makes the data, runs the Kalman
  filter, and draws the live window.
- ``tunnel_drive.csv``: **the drive**, 45 s in the tunnel, one row every
  0.1 s, 451 rows.
- ``README.md``: the commands, the columns, and four exercises.

.. admonition:: Requirements
   :class: note

   Python 3 with ``numpy`` and ``matplotlib`` (tested: Python 3.12, numpy
   1.26, matplotlib 3.6 and 3.10). On Ubuntu 24.04:

   .. code-block:: bash

      sudo apt install python3-numpy python3-matplotlib python3-tk

   ``python3-tk`` is what lets matplotlib open the live window. The appendix
   opens each file, so you know exactly what you are looking at before you run
   anything (:doc:`l3_appendix`).

Step 1: Run the Script
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   cd enpm818z-fall-2026-carla-python/lecture3/tunnel_kf
   python3 kf_tunnel.py --make-csv          # the data
   python3 kf_tunnel.py tunnel_drive.csv    # the live window
   python3 kf_tunnel.py tunnel_drive.csv --html kf.html # web page

The first command writes the CSV, so everyone has the same data. The second
opens the live window. The third is for anyone without a desktop: it writes
the same animation as a web page you open in a browser.

- **Watch:** the blue ellipse grows between signs and shrinks at each orange
  cross, a sign match.
- **Raise** :math:`Q` (motion noise, :math:`\sigma_a`): the ellipse gets
  fatter, and the estimate jumps further toward each sign.
- **Raise** :math:`R` (sign-match noise, :math:`\sigma_{\text{sign}}`): the
  jumps get smaller, and the estimate drifts with the IMU.

One difference from the measurement-model example. There, the sign match was
1 m off in both directions. Here, as in the update at 9.3 s, it is 1 m along
the tunnel but only 20 cm across it. The camera sees the sign on the wall
right next to the AV, so the distance to the wall is easy; the distance along
the tunnel is the hard part. That is why the ellipse is long and thin.

Step 2: Watch the Sawtooth
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/tunnel_kf_sigma.png
   :alt: Sigma of the position along the tunnel over 45 s. A blue sawtooth climbs between sign matches and drops at each, marked by thin orange vertical lines. It starts at 1 m and settles between about 0.8 m after a match and 1.3 to 1.7 m before the next. The brake from 8 to 12 s is shaded red, the speed-up from 20 to 24 s green, and a black line marks 11 s.
   :width: 75%
   :align: center

   The bottom-left plot of the hands-on window: the sawtooth, now on the
   simulated drive. Red shading marks the brake, green the speed-up, and the
   black line is the moment of this snapshot, :math:`t = 11` s, in the middle
   of the brake.

The curve is :math:`\sigma`: how uncertain the filter is about its position
along the tunnel, second by second. It **climbs** while only the IMU drives
the prediction, because every predict step leaks the speed error into position
(:math:`FPF^\top`) and adds :math:`Q` (see :ref:`l3-predicted-uncertainty`).
It **drops** at each sign match, the thin orange lines, because the update
removes part of the uncertainty. After a few matches it settles between about
**0.8 m** just after a match and **1.3 to 1.7 m** just before the next. The
growth from predicting and the shrink from each match balance out.

Step 3: Check That the Filter Is Honest
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the most important picture in the hands-on: it checks whether the
filter tells the truth about itself.

.. figure:: /_static/images/L3/tunnel_kf_error.png
   :alt: The true error along the tunnel over 45 s, an orange line, against a light blue band of plus and minus sigma. The line stays inside most of the time, leaves upward from about 15 to 24 s, peaking near 3 m at 18 s, dips below from about 3 to 5 s, and leaves downward after about 37 s. Brake and speed-up shaded; a black line at 11 s.
   :width: 75%
   :align: center

   The bottom-right plot of the hands-on window. The **orange line** is the
   true error along the tunnel; the **blue band** is the filter's own claim,
   :math:`\pm 1\sigma`. The line leaves the band upward from about 15 to 24 s
   (peaking near 3 m at 18 s), briefly near 3 to 5 s, and again after about
   37 s.

The orange line is the **true error along the tunnel**: the estimate minus
where the AV really is. **+2 m** means the estimate is 2 m ahead of the AV,
**-2 m** means 2 m behind; it says nothing about the lane. We can only draw it
because the CSV has the ground truth; a real AV never has it. The blue band is
the filter's own claim about that error: :math:`\pm 1\sigma`.

A bell curve holds **68 percent** of its values within :math:`1\sigma`, so an
honest filter keeps the line inside the band about 68 percent of the time.
Leaving the band is allowed: an honest filter is outside about a third of the
time.

- **Much less** than 68 percent: the band is too thin, **overconfident**.
- **Much more**: the band is too wide, **underconfident**.
- **Here: 65 percent**, close to 68, so this filter is honest.

Step 4: Move the Sliders
^^^^^^^^^^^^^^^^^^^^^^^^

Guess the result first, then move the slider and check. (Without a desktop,
the same settings are command-line options: ``--sigma-a`` for :math:`Q` and
``--sigma-sign`` for :math:`R`.)

.. list-table::
   :widths: 36 16 16 32
   :header-rows: 1
   :class: compact-table

   * - **Setting**
     - **RMS error**
     - **Inside 1σ**
     - **What it shows**
   * - default: :math:`\sigma_a = 0.5`, :math:`\sigma_{\text{sign}} = 1`
     - 1.06 m
     - 65%
     - honest
   * - :math:`Q` too small: :math:`\sigma_a = 0.01`
     - 5.46 m
     - 25%
     - **overconfident**
   * - :math:`Q` too big: :math:`\sigma_a = 3`
     - 1.28 m
     - 84%
     - underconfident
   * - :math:`R` too small: :math:`\sigma_{\text{sign}} = 0.1`
     - 1.46 m
     - 21%
     - trusts every sign, **overconfident**
   * - :math:`R` too big: :math:`\sigma_{\text{sign}} = 6`
     - 2.95 m
     - 77%
     - ignores the signs, drifts

.. danger::

   **The dangerous row is the second.** Shrink :math:`Q` to
   :math:`\sigma_a = 0.01` and the filter believes its motion rule is almost
   perfect. The band gets thin, the filter sounds confident, and the orange
   error line walks right out of it: inside only a quarter of the time, with
   an error five times larger. The filter sounds most confident exactly when
   it is most wrong.

Make :math:`Q` huge instead and the band gets fat: safe, but too cautious.
Make :math:`R` tiny and the filter jumps to every sign match, noise and all.
Make :math:`R` huge and it stops listening to the signs, and the IMU's small
bias makes it drift. The default is the only row where the band tells the
truth.



.. _l3-assumptions-break:

When the Assumptions Break
--------------------------

- **Where we are:** the Kalman filter rests on four assumptions.
- **In this section:** all four assumptions break on a real AV; alternative
  filters answer two of them.
- **What it is for:** picking an alternative filter: the EKF and UKF when the
  model is not linear, the particle filter when the belief is not one bell
  curve.

.. list-table::
   :widths: 60 40
   :header-rows: 1
   :class: compact-table

   * - **What breaks**
     - **The alternative**
   * - the model is not linear
     - **EKF** (this lecture)
   * - a wide uncertainty on a curve, or a model that is only code
     - **UKF** (:doc:`l3_appendix`)
   * - the belief has more than one peak
     - **particle filter** (:doc:`l3_appendix`)

The other two assumptions have no filter of their own. Bias, an error that
stays, we cover by making :math:`Q` bigger. Knowing :math:`Q` and :math:`R`,
how far off the motion rule and the sensor can be, has no alternative either.
It has a **test**, which gets its own section: :ref:`l3-consistency`. Each
failure below is described the same way: what the Kalman filter assumes, what
breaks, what goes wrong if you ignore it, and what the alternative costs.


What Breaks: the Model Is Not Linear
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The Kalman filter assumes** the motion and the sensor are straight-line
rules: :math:`\mathbf{x}_k = F\,\mathbf{x}_{k-1}` and
:math:`\mathbf{z} = H\mathbf{x}`. A matrix can only scale its inputs and add
them up.

.. figure:: /_static/images/L3/breaks_1_linear.png
   :alt: A curved road from above, bending left and up. Tag 1: the AV at four moments, following the bend. Tag 2: three faint orange copies of the AV continuing straight from where the bend starts, off the road. Tag 3: a blue dashed line from the AV's rear axle to a square landmark inside the bend, with dotted legs delta x and delta y closing a right triangle.
   :width: 55%
   :align: center

   **1** The AV follows the bend. **2** A straight-line rule keeps going
   straight, off the road. **3** The range to a landmark,
   :math:`\sqrt{\Delta x^2+\Delta y^2}`, from its offsets :math:`\Delta x`
   and :math:`\Delta y` (dotted).

**What breaks:** an AV that steers. One step moves it
:math:`x_k = x_{k-1} + v\,\Delta t\,\cos\theta`, where the heading
:math:`\theta` is itself a state number: no **fixed** :math:`F` times the
state gives :math:`\cos\theta` (the appendix shows why). A range sensor
reports :math:`\sqrt{\Delta x^2 + \Delta y^2}` (tag 3): no fixed :math:`H`
gives that either.

**What goes wrong:** you cannot even write :math:`F` or :math:`H`. Force a
straight line anyway, say by freezing the heading, and the prediction runs
straight on while the AV turns. It leaves the road on the first bend.

**The alternative: the EKF**, the extended Kalman filter. At every step,
replace each curve by its **tangent**, the line touching it at the current
estimate. **Cost:** the tangents, called **Jacobians**, are derived by hand,
you must get them right, and they are only good near the estimate.


What Breaks: the Model Curves Too Much, or Is Only Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The EKF swaps the curve for its tangent** at the best guess. That works only
if the curve is almost straight across **every** heading the AV might have.
It breaks in two ways.

.. figure:: /_static/images/L3/breaks_2_banana.png
   :alt: From above, the AV starts on a straight road heading east, tag 1. Two dashed lines fan out at plus and minus 12 degrees, tag 2. A dotted arc 20 m from the start, tag 3. About 500 blue dots along the arc, curving like a banana, tag 4. A tall dashed orange ellipse, tag 5, centered on an orange dot at 20 m, tag 6. A green cross at 19.57 m, tag 7.
   :width: 75%
   :align: center

   The banana.
   **1** The AV and its heading, on the road.
   **2** Heading spread :math:`\sigma = 12^\circ`: a value we chose, large
   enough to show the bend.
   **3** Every spot 20 m from the start (distance known to :math:`\pm 0.5`
   m, which we chose).
   **4** Where the AV could be after 20 m: a **banana**.
   **5** The EKF's :math:`2\sigma` ellipse: straight, from one tangent.
   **6** The EKF's mean: 20.00 m ahead.
   **7** The real middle of the dots: **19.57 m**.

- **Too curved.** With the heading known only to 12°, each possible heading
  lands the AV somewhere different after 20 m, and the spots form a banana.
  The EKF's straight line says 20 m ahead; the real middle is 19.57 m. Know
  the heading to 1° and the EKF is fine: same model, less uncertainty.
- **Only code.** Sometimes the model is a program, not an equation: searching
  the HD map for the sign the camera should see, or a physics engine. You can
  run it, but there is no formula to take the slope of.

**What goes wrong:** the EKF's answer is too far ahead, and less uncertain
than it really is: **overconfident**, the dangerous direction.

**The alternative: the UKF**, the unscented Kalman filter. Take a few chosen
possible positions, move each with the **real** model, and rebuild the mean
and covariance from where they land. **Cost:** :math:`2n+1 = 7` runs of the
model per step (:math:`n = 3`: :math:`x`, :math:`y`, :math:`\theta`), but no
slopes. The UKF in detail is in :doc:`the appendix <l3_appendix>`.


What Breaks: the Belief Has More Than One Peak
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This failure is a different assumption altogether: sometimes the honest
answer is one of two places. **Every Kalman filter**, the EKF and UKF
included, **assumes the belief is one bell curve**: one best guess, with
confidence fading away from it in every direction. A bell curve has exactly
**one peak**, and a peak is just a place the AV might be.

.. figure:: /_static/images/L3/breaks_3_peaks.png
   :alt: A straight two-lane tunnel from above. Two identical yellow ceiling lights 25 m apart, tags 1 and 2. Tag 3: the AV under the first light, with a cluster of blue dots under each light. Tag 4: a long dashed orange ellipse spanning both clusters, with a faint AV at its center halfway between the lights. Tag 5: two exit signs on the lower wall, one behind and one far ahead.
   :width: 85%
   :align: center

   **1, 2** Two identical lights, 25 m apart. **3** The AV, and the two
   clusters of blue dots where it could be. **4** One bell curve, drawn as
   its :math:`1\sigma` ellipse, spanning both clusters. **5** Exit signs,
   too far away to match.

**What breaks:** until now the camera matched exit signs, and in our tunnel
each exit sign carries its own number (the sign ID in the hands-on file), so a
match says *which* sign it was. Now picture a stretch with **no exit sign in
view** (tag 5), and say the AV falls back on other landmarks in the HD map,
such as the ceiling **lights**. The lights are identical fixtures, with
nothing for a camera to read, one every 25 m. The camera is right that there
is a light overhead, but "a light overhead" fits **this light or the next
one** equally well. The honest belief has two peaks, with nothing in between.

What Goes Wrong: One Bell Curve over Two Peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The same belief along the tunnel, drawn as curves. The AV is under the first
light.

.. figure:: /_static/images/L3/breaks_3b_bells.png
   :alt: Belief per meter against position along the tunnel, minus 15 to 40 m. Tag 1: two tall narrow blue bell curves peaking at about 0.15 per meter over 0 and 25 m. Tag 2: one low wide dashed orange bell curve spread across both. Tag 3: a dotted line at its mean, 12.5 m, where the blue curves are zero. Tag 4: two yellow squares, the lights. Tag 5: a black cross at 0 m, where the AV really is.
   :width: 80%
   :align: center

   **1** The honest belief: two peaks, :math:`\sigma = 1.3` m each, half the
   weight each. **2** The one bell curve with the same mean and spread.
   **3** Its mean: **12.5 m**, with :math:`\sigma = 12.6` m. **4** The two
   lights. **5** The AV, really at 0 m.

**What goes wrong:** one mean and one covariance average the peaks. The AV
lands **between the lights**, exactly where the honest belief is zero, and its
:math:`\sigma` of 12.6 m smears the AV across the whole stretch. The ellipse
looks reasonable, and nothing in the equations warns you.

**The alternative: the particle filter.** Carry thousands of candidate
states, called particles, at once, so the belief can sit in several places
until something settles it. **Cost:** it scales badly; the number of
particles you need grows very fast with the size of the state. The particle
filter in detail is in :doc:`the appendix <l3_appendix>`.


.. _l3-ekf:

The Extended Kalman Filter
--------------------------

**Alternative 1 of 3.**

- **Where we are:** the Kalman filter, which handles only straight-line
  models.
- **In this section:** the **EKF**, a clever, necessary hack that fakes a
  straight line, one small step at a time.
- **What it is for:** a turn needs a cosine and a range needs a square root,
  and no fixed matrix computes either. **GP3 uses the EKF.**

.. admonition:: Definition: extended Kalman filter (EKF)
   :class: note

   A Kalman filter for models that are **curves, not straight lines**. At
   every step it replaces each curve by its **tangent at the estimate**, then
   runs the ordinary Kalman equations.

The story has four parts. The plain Kalman filter breaks on a curve. The EKF
fakes a straight line, one step at a time. It splits the work in two. And it
has a catch.


Matrices Can Only Scale and Add
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Kalman filter's engine is matrices, and a matrix does only two things: it
**scales** numbers and **adds** them.

.. figure:: /_static/images/L3/ekf_story_1_matrix.png
   :alt: Three plots. Tag 1: three straight lines through the origin, output against input, with slopes 2, 0.5 and minus 1. Tag 2: an arch, x in meters against heading theta from minus 90 to 90 degrees, x equals 20 cos theta, highest at 20 meters for theta 0. Tag 3: a curve, range r in meters against AV position x from 0 to 30 meters, r equals the square root of 20 minus x squared plus 10 squared, lowest at 10 meters for x 20.
   :width: 100%
   :align: center

   **1** A matrix: scale and add. Times 2, times 0.5, times :math:`-1`: every
   output is a **straight line**. **2** Turning: driving 20 m at heading
   :math:`\theta` moves :math:`x = 20\cos\theta` east, an **arch**. **3** The
   range to a sign 10 m off the road, beside :math:`x = 20`:
   :math:`r = \sqrt{(20 - x)^2 + 10^2}`, a **curve**.

The Kalman filter is the best filter there is, but only when every model is a
straight line and the noise is a bell curve. Whatever a matrix scales by, the
result is a straight line through the origin. An AV that turns moves
:math:`20\cos\theta` east, and the range from the camera to an exit sign is a
square root: both curve.

.. important::

   **No fixed matrix times the state gives a cosine or a square root of the
   state**, so the plain Kalman filter breaks the moment the AV turns or a
   camera measures a range.


Bell Curves on the Road
~~~~~~~~~~~~~~~~~~~~~~~

Two examples show what happens to a bell curve when we push it through a
function: first a straight line, then a curve. The AV is on a road that runs at
30° from east and drives about 20 m. We look at :math:`x`, how far east it
gets.

A Straight Line Keeps a Bell Curve a Bell Curve
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here the heading is **known** (30°) and the distance is not
(:math:`20 \pm 1` m).

.. list-table::
   :widths: 55 45
   :class: compact-table

   * - .. figure:: /_static/images/L3/bell_road_1_line.png
          :alt: From above, a road running up to the right at 30 degrees. Tag 1: the AV at the origin with its heading arrow, 30 degrees from east, and distance d along it. Tag 2: blue dots in a short line along the heading about 20 m ahead. Tag 3: dotted lines dropping from the dots to the x axis. Below, a plot of belief against x. Tag 4: a narrow blue bell curve. Tag 5: a line at its mean, 17.32 m.
          :width: 100%
          :align: center

          **1** The AV; its heading, from east, is known: 30°.
          **2** Where it could be after :math:`d = 20 \pm 1` m: a short line.
          **3** Straight down to :math:`x`: :math:`x = d\cos 30^\circ`, a
          straight line in :math:`d`.
          **4** The belief about :math:`x`: still a **bell curve**,
          :math:`17.32 \pm 0.87` m.
          **5** Its mean: 17.32 m.
     - .. figure:: /_static/images/L3/bell_1_line.png
          :alt: A bell curve pushed through a straight line. Input: distance driven, a bell curve centered on 20 m with a spread of 1 m. The line d times cosine 30 degrees. Output: a blue bell curve centered on 17.32 m. Readout: in, bell curve; out, bell curve, 17.32 plus or minus 0.87 m.
          :width: 100%
          :align: center

          The same story as input, function and output: a bell curve of
          distance, :math:`20 \pm 1` m, goes in; the straight line
          :math:`d\cos 30^\circ` maps it; a bell curve,
          :math:`17.32 \pm 0.87` m, comes out.

**Straight line:** bell curve in, bell curve out, and :math:`FPF^\top` gives
its width exactly. That is why the Kalman filter works.

A Curve Bends a Bell Curve out of Shape
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Same road, the other way round. The distance is **known** (20 m), and the
heading is not: :math:`30^\circ \pm 12^\circ`, the same 12° as the banana, a
value we chose.

.. list-table::
   :widths: 55 45
   :class: compact-table

   * - .. figure:: /_static/images/L3/bell_road_2_curve.png
          :alt: The same road at 30 degrees. Tag 1: the AV with its heading theta and d equals 20 m. Tag 7: dashed lines fanning out at 18 and 42 degrees. Tag 2: blue dots on an arc 20 m from the AV. Tag 3: dotted lines dropping to the x axis. Below, tag 4: a gray lopsided histogram piled up just under 20 m with a long tail toward 9 m. Tag 5: a line at its mean, 16.95 m. Tag 6: a dotted line at 17.32 m.
          :width: 100%
          :align: center

          **1** The AV; heading :math:`\theta = 30^\circ`, spread 12° (**7**).
          **2** Where it could be after exactly :math:`d = 20` m: an
          **arc**.
          **3** Straight down to :math:`x`: :math:`x = 20\cos\theta`, a
          curve in :math:`\theta`.
          **4** The belief about :math:`x`: **lopsided**; no heading gets it
          past 20 m.
          **5** Its mean: **16.95 m**.
          **6** The curve at 30°: 17.32 m.
     - .. figure:: /_static/images/L3/bell_2_curve.png
          :alt: A bell curve pushed through a curve. Input: heading, a bell curve centered on 30 degrees with a spread of 12 degrees. The curve 20 cosine theta. Output: a gray lopsided histogram piled up just under 20 m with a long tail toward 8 m; its mean, 16.95 m, sits below the dotted guide at 17.32 m.
          :width: 100%
          :align: center

          Input, function and output: a bell curve of heading goes in; the
          curve :math:`20\cos\theta` maps it; a lopsided shape comes out,
          with mean 16.95 m, not 17.32 m.

**Curve:** bell curve in, **lopsided** shape out, and its mean is not the
curve at the mean. So the problem, in two lines: moving the estimate through
:math:`f` is easy (call :math:`f` once), but moving the uncertainty :math:`P`
through :math:`f` has no formula. The EKF works around it.


The Trick: a Straight Line, One Step at a Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the whole idea of the EKF. At the current estimate, draw the
**tangent**. For the next step, **pretend the tangent is the curve**. Next
step, draw a new one.

.. figure:: /_static/images/L3/ekf_story_2_steps.png
   :alt: The range to a sign against the AV's position x, 0 to 24 m. Tag 1: the real curve, lowest at x = 20. Tag 2: a blue dot on the curve at x = 4, the estimate at step k. Short orange tangent segments at x = 4, 9 and 14, one per step; tag 3 points at the one at 9. Tag 4: the tangent from x = 4 extended as a dashed line, which falls well below the curve by x = 18.
   :width: 75%
   :align: center

   **1** The real curve, the range to the sign as the AV drives. **2** The
   estimate at step :math:`k`. **3** The **tangent** there: for one step, the
   EKF pretends this short straight line is the curve; each step draws a new
   one. **4** Far from where it touches, a tangent is **wrong**.

Why does this work? Close to where it touches, the tangent and the curve are
almost the same. On the hands-on's bend (10 m/s, 60 m radius) the AV turns
only 0.95° per 0.1 s step: over one step, the curve **is** almost straight.
The dashed line is the catch, and it comes back at the end of the section.


A Simple Example: the Range to One Landmark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The next few steps all use one example.

.. figure:: /_static/images/L3/range_example.png
   :alt: The road from above, x along the bottom from 0 to 20 m. A landmark stands 10 m off the road beside x = 20. The AV's rear axle middle is at x = 16, driving right; a thick line from it to the landmark is the range h of x. Markers above the road: run 1, x-hat = 15.5, and run 2, x-hat = 10. Below, arrows for x, 0 to 16, and 20 minus x.
   :width: 80%
   :align: center

   The range example from above: the thick line is the range :math:`h(x)`;
   under the road, the blue arrow is :math:`x` and the gray one
   :math:`20 - x`; above it, the green marker is run 1's estimate and the
   orange marker run 2's.

- :math:`x` is the **AV's position along the road**. The AV drives right,
  toward a landmark 10 m off the road, beside :math:`x = 20` m.
- The camera measures the **range**: the straight-line distance to the
  landmark. The AV, the landmark and the spot beside it make a right triangle
  with legs :math:`20 - x` and 10, so
  :math:`h(x) = \sqrt{(20 - x)^2 + 10^2}`.
- The AV is really at :math:`x = 16` m, 4 m before the landmark, so the camera
  reads :math:`\sqrt{4^2 + 10^2} = \sqrt{116} =` **10.77 m**.
- The filter does not know where the AV really is. It keeps **one** estimate,
  :math:`\hat{x}`. We run the example twice: **run 1**, :math:`\hat{x} = 15.5`
  m (good, half a meter behind); **run 2**, :math:`\hat{x} = 10` m (poor, 6 m
  behind). They are two separate runs, not two answers at once. Same AV, same
  reading; only the estimate changes.

The Range Curve Has No Single Slope
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/ekf_linearize_0_curve.png
   :alt: Left: the road from above with a landmark, tag 6, 10 m off the road beside x = 20, and lines of sight from 4 m (18.87 m, 32 degrees off the road), 10 m (14.14 m), 16 m (10.77 m) and 19 m (10.05 m, 84 degrees off). Right: the range against the AV's position, tag 1, falling and flattening toward 10 m at x = 20, with tags 4, 2, 3 and 5 at 4, 10, 16 and 19 m.
   :width: 90%
   :align: center

   **Left:** the road from above. **Right:** not the road, a graph of the
   range the camera would report at each :math:`x`. **1** The range
   :math:`h(x) = \sqrt{(20 - x)^2 + 10^2}`. **2** The AV at 10 m (run 2's
   estimate): 14.14 m. **3** At 16 m, where the AV really is: 10.77 m.
   **4** At 4 m: 18.87 m. **5** At 19 m: 10.05 m. **6** The landmark.

As the AV drives right the range shrinks, but not at a steady rate. Think
about where the camera looks. The slope is how much of the camera's line of
sight points along the road, :math:`(20 - x)/h(x)`, the cosine of the angle
between the line of sight and the road.

- At :math:`x = 4` the landmark is far ahead; the line of sight is 32° off
  the road. Drive 1 m and the range drops 0.85 m: slope 0.85.
- At :math:`x = 19` the landmark is almost beside the AV; the line of sight is
  84° off the road. Drive 1 m and the range drops only 0.10 m: slope 0.10.
- Right beside it, square to the road, the range stops changing: the curve is
  flat, at 10 m.

The angle changes as the AV drives, so **there is no single slope**.

The Surprise Says the AV Is Farther Ahead
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The camera measures from where the AV **really** is, which the filter does
not know; to the filter, 10.77 is just a number the camera sent. The filter
compares that reading with the one it **expects** at its estimate. The gap,
the **surprise**, is its only clue that the estimate is off. Run 1:
:math:`\hat{x} = 15.5` m.

.. figure:: /_static/images/L3/ekf_linearize_1_good.png
   :alt: The range curve, 4 to 20 m. Tag 1: a dotted horizontal line at 10.77 m. Tag 2: a green dot on the curve at x = 15.5, 10.97 m. Tag 3: a short arrow down from the dot to the reading line. Tag 4: a dashed tangent through the green dot. Tag 5: a green cross where the tangent meets the reading line, 15.98 m. Tag 6: a dotted vertical line at 16 m.
   :width: 70%
   :align: center

   **1** The camera reads **10.77 m**. **2** At :math:`\hat{x} = 15.5` m the
   filter expects :math:`h(15.5) =` **10.97 m**. **3** The surprise: 0.20 m
   **less** than expected. **4** The tangent at :math:`\hat{x}`. **5** Where
   the tangent meets the reading. **6** Where the AV really is, 16 m.

Two readings, from two positions. They differ only because the estimate is
wrong; if it were exactly right, they would match. The reading came in 0.20 m
less than expected. Less range means closer to the landmark, so the AV is
**farther ahead** than :math:`\hat{x}`. How much farther is the next step.

A Good Estimate: the Tangent Lands Near the Truth
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The surprise is in meters of **range**; the filter moves the AV in meters of
**position**. The tangent at :math:`\hat{x}` converts one into the other.

.. figure:: /_static/images/L3/ekf_linearize_1b_zoom.png
   :alt: Close-up of run 1, 14.4 to 17 m along the road, 10.3 to 11.35 m of range. The curve and a dashed tangent at 15.5 m nearly overlap. Tag 1: a slope triangle, 1 m ahead and 0.41 m down. Tag 2: an arrow from 10.97 m down to the reading, 10.77 m. Tag 3: an arrow along the reading line from 15.5 to 15.98 m. Tag 4: a green cross at 15.98 m. Tag 5: a dotted line at 16 m.
   :width: 70%
   :align: center

   **1** The slope at :math:`\hat{x}`, **0.41**: 1 m ahead, 0.41 m less
   range. From the curve rule: :math:`(20 - \hat{x}) / h(\hat{x}) = 4.5 /
   10.97`. **2** The surprise: 0.20 m less range. **3** The move:
   :math:`0.196 / 0.410 =` **0.48 m** ahead. **4** The new estimate:
   :math:`15.5 + 0.48 =` **15.98 m**. **5** Where the AV really is: 16 m.

The range has to come down by 0.20, and it comes down 0.41 for each meter the
AV moves ahead. So the AV has to move 0.20 divided by 0.41, which is 0.48 m:
the same arithmetic as time equals distance divided by speed. The new
estimate, 15.98 m, is 2 cm off, because near the estimate the tangent and the
curve are almost the same line.

.. note::

   One simplification, so there is one idea at a time: here the reading is
   perfect and fully trusted. A real filter moves only part of the way, by the
   gain :math:`K`. That changes how far it moves, not the slope it uses.

A Poor Estimate: the Tangent Falls Short
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run 2: same AV, same landmark, same reading, 10.77 m. Only the estimate
changes: :math:`\hat{x} = 10` m, 6 m behind.

.. figure:: /_static/images/L3/ekf_linearize_2_poor.png
   :alt: The range curve, 4 to 20 m. Tag 1: a dotted line at 10.77 m. Tag 2: an orange dot on the curve at x = 10, 14.14 m. Tag 3: a long arrow down to the reading line. Tag 4: a dashed tangent at x = 10, steeper than the curve near 16. Tag 5: an orange cross where the tangent meets the reading line, 14.77 m, with a short double arrow to the true position. Tag 6: a dotted line at 16 m.
   :width: 70%
   :align: center

   **1** The camera reads **10.77 m**. **2** At :math:`\hat{x} = 10` m the
   filter expects **14.14 m**. **3** The surprise: 3.37 m **less**, so the AV
   is farther ahead. **4** The tangent: slope :math:`-10 / 14.14 = -0.71`,
   the range drops 0.71 per meter. Between 10 and 16 m the curve drops only
   0.56 per meter. **5** Move :math:`3.37 / 0.71 = 4.77` m: to **14.77 m**,
   **1.23 m short** of **6**, the AV at 16 m.

Back at 10 m the curve is steeper, so the tangent drawn there says 0.71 per
meter. Between 10 and 16 m the real curve drops only 3.37 over 6 m, about 0.56
per meter. **The tangent is too steep, so the correction is too small.** That
slope, -0.71, is what the EKF calls the **Jacobian** :math:`H` (defined
below): a poor estimate gives a wrong :math:`H`, and a wrong :math:`H` gives a
correction of the wrong size. Run 2 still improved, from 6 m off to 1.23 m.
The catch, later in this section, is how this can feed on itself when the
error is large enough.


Two Jobs: the Estimate Rides the Curve, P Rides the Tangent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now the trick on the bell curve, and the way the EKF splits the work.

.. figure:: /_static/images/L3/bell_3_ekf.png
   :alt: The curve 20 cosine theta with its tangent at 30 degrees as a dashed straight line. The same input bell curve, 30 plus or minus 12 degrees, goes through the tangent. On the left, a dashed orange bell curve centered on 17.32 m over the gray lopsided histogram of the true output; the orange bell spills above 20 m. Readout: EKF 17.32 plus or minus 2.09 m, true 16.95 plus or minus 2.11 m.
   :width: 70%
   :align: center

   Replace the curve by its **tangent** at the estimate, 30° (the dashed
   orange line). A tangent is a straight line, so a bell curve comes out again:
   the dashed orange bell on the left, drawn over the gray lopsided shape of
   the true output. The orange bell also spills above 20 m, where the AV can
   never be.

- **The estimate goes through the real curve**, :math:`20\cos\theta` (later:
  :math:`f`): :math:`20\cos 30^\circ = 17.32` m.
- :math:`P` **goes through the tangent**, which gives :math:`\pm 2.09` m.

EKF: :math:`17.32 \pm 2.09` m. True: :math:`16.95 \pm 2.11` m. The width is
close; the mean is **0.37 m too far**, because a straight line cannot see the
bend. The UKF, in :doc:`the appendix <l3_appendix>`, starts from this picture.


The Models f and h for an AV That Turns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replace the matrices by **functions**. Where the Kalman filter had a matrix
:math:`F`, we now have a function :math:`f`; where it had :math:`H`, a
function :math:`h`. The noise stays exactly as before:

.. math::

   \mathbf{x}_k = f(\mathbf{x}_{k-1}, \mathbf{u}) + \mathbf{w},
   \qquad
   \mathbf{z}_k = h(\mathbf{x}_k) + \mathbf{v}

The motion model :math:`f`, all three rows:

.. math::

   \underbrace{\begin{bmatrix} x_k \\ y_k \\ \theta_k \end{bmatrix}}_{\mathbf{x}_k}
   \;=\;
   \underbrace{\begin{bmatrix} x_{k-1} + v\,\Delta t\cos\theta_{k-1} \\
                               y_{k-1} + v\,\Delta t\sin\theta_{k-1} \\
                               \theta_{k-1} + \omega\,\Delta t \end{bmatrix}}_{f(\mathbf{x}_{k-1},\,\mathbf{u})}
   \;+\; \mathbf{w}

State :math:`\mathbf{x} = [x,\ y,\ \theta]`: position and heading, the
direction the AV is pointing. Control :math:`\mathbf{u} = [v,\ \omega]`: speed
from the wheel encoders, turn rate from the gyro, what the AV did during the
step. Read the rows: the new :math:`x` is the old :math:`x` plus speed times
time times the cosine of the heading; the new :math:`y` is the same with sine;
the new heading is the old one plus turn rate times time.

Rows 1 and 2 hold :math:`\cos\theta` and :math:`\sin\theta` of the state's
own :math:`\theta`: **no fixed matrix** :math:`F` **holds them**. That is the
whole reason for the EKF. This is exactly the :math:`f` in the hands-on
script, :ref:`l3-ekf-hands-on`.


.. _l3-jacobian:

The Jacobian: the Tangent for Several Inputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With one input and one output, the tangent is just the slope: nudge the input,
and see how much the output moves. Our :math:`f` has three inputs and three
outputs, so "the slope" becomes a table of slopes.

.. admonition:: Definition: Jacobian
   :class: note

   The slopes of every output with respect to every input, for a function with
   several inputs and outputs. A table: *nudge input j a little, and output i
   moves this much.*

.. math::

   F_k = \frac{\partial f}{\partial \mathbf{x}}\bigg|_{\hat{\mathbf{x}}_{k-1}}
   \qquad\qquad
   H_k = \frac{\partial h}{\partial \mathbf{x}}\bigg|_{\hat{\mathbf{x}}^-_k}

The curly :math:`\partial` is read "partial": the slope for one input while the
others stay put. The bar with a subscript says where the slope is taken, and
where matters. :math:`F_k` is taken at the **last estimate**, before predict
moves it. :math:`H_k` is taken at the **prediction**. Both change every step,
because the estimate moves every step.

The Jacobian F_k with Real Numbers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take :math:`v = 10` m/s, :math:`\Delta t = 0.1` s, heading
:math:`\hat\theta = 30^\circ`:

.. math::

   F_k =
   \begin{bmatrix}
     1 & 0 & -v\,\Delta t\,\sin\hat\theta \\
     0 & 1 & \phantom{-}v\,\Delta t\,\cos\hat\theta \\
     0 & 0 & 1
   \end{bmatrix}
   =
   \begin{bmatrix}
     1 & 0 & \mathbf{-0.500} \\
     0 & 1 & \phantom{-}0.866 \\
     0 & 0 & 1
   \end{bmatrix}

Most of it is easy. The new :math:`x` moves one for one with the old :math:`x`
and ignores the old :math:`y`, so the top-left block is the identity. The
bottom row is the heading, which depends only on itself: slope 1. The
interesting column is the third, the heading.

**Row 1, column 3:** nudge the heading, and :math:`x` moves by -0.5 m per
radian of nudge. The slope of :math:`x + v\,\Delta t\cos\theta` as
:math:`\theta` changes is :math:`-v\,\Delta t\sin\theta`, and with our numbers
that is -0.5. Same for :math:`y` with the cosine: 0.866. On the road: if the
heading guess is a tenth of a radian too small (about 6°), this step puts
:math:`x` about 5 cm too far east and :math:`y` about 9 cm too short. That is
the link between heading and position, as numbers, and :math:`P` needs it to
tilt its ellipse correctly.

:math:`F_k` depends on :math:`\hat\theta`, so it is **recomputed every step**.
That is what makes it an EKF and not a KF: the plain filter's :math:`F` was a
constant you typed once.

The Jacobian Stretches and Squeezes the Ellipse
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Predict only, on the hands-on's bend (10 m/s, 60 m radius), heading known to
:math:`\pm 3^\circ`, with :math:`Q` left out to show :math:`F_k` alone.

.. figure:: /_static/images/L3/ekf_story_3_ellipse.png
   :alt: From above, east 0 to 35 m, north minus 4 to 10 m. Tag 1: a green arc curving left from the origin, with dots every half second. Black heading arrows at 0, 1, 2 and 3 s; tag 4 points at the one at 3 s. Blue shaded 2-sigma ellipses on the arc at 0, 1, 2 and 3 s: tag 3 at the small round one at 0 s, tag 2 at the long thin one at 3 s, lying across the direction of travel.
   :width: 80%
   :align: center

   **1** The estimate rides the **real** :math:`f`: an arc, cosines and
   sines. **2** At 3 s (:math:`2\sigma` shown): :math:`\sigma` is **1.58 m
   across** the direction of travel, still 0.30 m along. **3** At 0 s:
   :math:`\sigma = 0.3` m each way, heading :math:`\sigma = 3^\circ`.
   **4** The heading: column 3 of :math:`F_k` turns heading doubt into
   **sideways** doubt.

:math:`P` goes through :math:`F_k P F_k^\top`, one tangent per step. Step
after step, the ellipse stretches across the road, stays thin along it, and
turns with the AV: stretching and squeezing, done by a table of slopes.

Building Q_k from the Wheel and Gyro Noise
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Think about where the noise really is. The wheel encoders report the speed
with some error (:math:`\sigma_v`), and the gyro reports the turn rate with
some error (:math:`\sigma_\omega`). The noise is in the **inputs**, not in
:math:`x`, :math:`y` and :math:`\theta` directly. But :math:`P` describes the
state, so one more Jacobian, :math:`G = \partial f / \partial \mathbf{u}`,
carries the input noise into the state:

.. math::

   Q_k \;=\; G \begin{bmatrix} \sigma_v^2 & 0 \\ 0 & \sigma_\omega^2 \end{bmatrix} G^\top
   \qquad\qquad
   G \;=\; \begin{bmatrix} \Delta t\cos\hat\theta & 0 \\
                           \Delta t\sin\hat\theta & 0 \\
                           0 & \Delta t \end{bmatrix}

Column one: a small speed error moves the AV along its heading. Column two: a
small turn-rate error changes the heading by :math:`\Delta t`. Then
:math:`Q_k` is the same sandwich as :math:`FPF^\top`.

**In the hands-on:** :math:`\sigma_v = 0.2` m/s and
:math:`\sigma_\omega = 2^\circ`/s, so each 0.1 s step adds 0.02 m along the
heading and 0.2° of heading. :math:`G` holds :math:`\hat\theta`, so
:math:`Q_k` is **rebuilt every step**, right next to :math:`F_k`. It is the
same idea as the Kalman filter's :math:`Q` from :math:`\sigma_a`: the noise
enters through an input, and a matrix spreads it into the state.

The Camera Reports Range and Bearing to a Sign
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/range_bearing.png
   :alt: From above, with east and north axes. The AV's rear axle middle, a white dot labeled AV x, y, at the origin. A blue arrow labeled nose points 20 degrees above east: the heading theta. A green square, the sign at x s, y s. An orange line from the AV to the sign is labeled r, the range, and an orange arc from the nose to that line is labeled beta, the bearing.
   :width: 60%
   :align: center

   The AV at :math:`(x, y)`, its nose pointing at angle :math:`\theta` from
   east. The sign is at :math:`(x_s, y_s)`, known from the HD map. The camera
   reports the **range** :math:`r` (how far away the sign is) and the
   **bearing** :math:`\beta` (the angle between the AV's nose and the sign).

.. math::

   h(\mathbf{x}) = \begin{bmatrix} r \\ \beta \end{bmatrix}
   = \begin{bmatrix} \sqrt{\Delta x^2 + \Delta y^2} \\
                     \operatorname{atan2}(\Delta y, \Delta x) - \theta \end{bmatrix}

:math:`\Delta x = x_s - x` and :math:`\Delta y = y_s - y`: how far the sign is
from the AV, east and north. The range is Pythagoras. The bearing is the
direction to the sign, measured from east, minus the direction of the nose,
positive to the left. :math:`\operatorname{atan2}` is the arctangent that
keeps track of the quadrant; every language has it. A square root and an
arctangent of the state: **no fixed matrix** :math:`H` **holds them**, so
:math:`h` needs a tangent too.

The Jacobian H_k with Real Numbers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Chosen for this example: the sign is 24 m east and 18 m north of the predicted
position, so :math:`r = \sqrt{24^2 + 18^2} = 30` m. Columns are :math:`x`,
:math:`y`, :math:`\theta`; rows are range and bearing.

.. math::

   H_k =
   \begin{bmatrix}
     -\Delta x / r   & -\Delta y / r   & \phantom{-}0 \\
     \phantom{-}\Delta y / r^2 & -\Delta x / r^2 & -1
   \end{bmatrix}
   =
   \begin{bmatrix}
     \mathbf{-0.80} & -0.60 & \phantom{-}0 \\
     \phantom{-}0.020 & -0.027 & \mathbf{-1}
   \end{bmatrix}

- **Row 1, column 1:** move 1 m east (partly toward the sign), and the range
  drops by 24/30, 0.8 m. The minus sign says it drops.
- **Row 2, column 3:** turn the nose 1 rad left, and the sign, which has not
  moved, now sits 1 rad further right of the nose: -1. That entry does not
  depend on where the sign is.
- The middle entries of row 2 are small, 0.02 rad per meter, about 1° per
  meter, because the sign is 30 m away. A nearer sign makes them bigger.

Like :math:`F_k`, :math:`H_k` depends on the estimate, so it is recomputed at
every sign match, at the prediction.


The EKF next to the Kalman Filter, Line by Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the table to copy for GP3. The left column is the Kalman filter, the
same seven lines as the whole-cycle summary. The right column is the EKF; the
changed parts are marked with a box.

.. list-table::
   :widths: 16 38 46
   :header-rows: 1
   :class: compact-table

   * -
     - **Kalman filter**
     - **EKF**
   * - **Predict**
     - :math:`\hat{\mathbf{x}}^- = F\hat{\mathbf{x}} + B\mathbf{u}`
     - :math:`\hat{\mathbf{x}}^- = \boxed{f(\hat{\mathbf{x}}, \mathbf{u})}`
   * -
     - :math:`P^- = FPF^\top + Q`
     - :math:`P^- = \boxed{F_k} P \boxed{F_k}^\top + \boxed{Q_k}`
   * - **Update**
     - :math:`\boldsymbol{\nu} = \mathbf{z} - H\hat{\mathbf{x}}^-`
     - :math:`\boldsymbol{\nu} = \mathbf{z} - \boxed{h(\hat{\mathbf{x}}^-)}`
   * -
     - :math:`S = HP^-H^\top + R`
     - :math:`S = \boxed{H_k}P^-\boxed{H_k}^\top + R`
   * -
     - :math:`K = P^-H^\top S^{-1}`
     - :math:`K = P^-\boxed{H_k}^\top S^{-1}`
   * -
     - :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^- + K\boldsymbol{\nu}`
     - :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^- + K\boldsymbol{\nu}`
   * -
     - :math:`P = (I - KH)\,P^-`
     - :math:`P = (I - K\boxed{H_k})\,P^-`

The pattern: two lines use the real functions, moving the estimate and
predicting the reading. Every line with :math:`P`, :math:`S` or :math:`K` uses
a Jacobian. **The real** :math:`f` **and** :math:`h` **move the estimate; the
Jacobians move** :math:`P`, the same as the orange bell curve picture. And
the order matters: :math:`F_k` and :math:`Q_k` are computed at
:math:`\hat{\mathbf{x}}_{k-1}`, **before** predict moves it; :math:`H_k` at
:math:`\hat{\mathbf{x}}^-`.

The EKF Lines in Code
^^^^^^^^^^^^^^^^^^^^^

From ``run_ekf()`` in ``curved_tunnel/ekf_curve.py``, trimmed. Each line of
the table is one line here; the rest computes the Jacobians and wraps angles.

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

Predict is four lines: compute :math:`F_k` and :math:`Q_k` first, while ``x``
is still the last estimate, then move ``x`` through the real :math:`f` and
``P`` through the tangent. Update is eight lines: :math:`H_k` at the
prediction, the surprise through the real :math:`h`, then two lines that are
not in the table. The bearing is an angle, so the surprise is wrapped, and
after the update the heading is wrapped again (the traps below explain why).
The rest is the Kalman filter you already know. The whole EKF is these twelve
lines plus the functions :math:`f`, :math:`h` and their Jacobians; in GP3
most of your time goes into those functions, not this loop.


Where the Straight Line Stops Being Good Enough
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run 2 was a poor estimate. This one is a good estimate with a wide
uncertainty, and it fails too.

.. figure:: /_static/images/L3/ekf_drive_sweep.gif
   :alt: Animation. The AV drives away from the start with its heading known only to plus or minus 12 degrees. Dots show where it can really be; a dashed ellipse shows what the EKF believes. Near the start the ellipse hugs the cloud; farther along the dots curve into a banana while the ellipse stays a straight lens.
   :width: 90%
   :align: center

   The AV **drives away from the start** with its heading known only to
   :math:`\pm 12^\circ`. The dots are where it can **really** be; the dashed
   ellipse is what the **EKF believes**. Near the start the ellipse **hugs**
   the cloud. The farther the AV drives, the more the dots **curve into a
   banana** that no ellipse can represent; by 22 m the ellipse is still a
   straight vertical lens.

No tuning fixes that: it is a shape problem. Two errors appear together:

- **The mean.** The EKF puts the mean at the **full distance driven**, but the
  AV lands **short** of it. The forward part of the drive is
  :math:`\cos\theta` times the distance, and the average of :math:`\cos\theta`
  over a spread of headings is less than 1. The tangent at :math:`\theta = 0`
  cannot see that, because at zero the cosine is flat.
- **The spread.** The EKF's along-track :math:`\sigma` **never moves off
  0.50 m** (the distance driven, :math:`\pm 0.5` m, a value we chose), while
  the truth grows from 0.52 m to 0.79 m. It is **overconfident**.

That is the failure that hurts: an overconfident filter rejects good
measurements. The EKF is fine while the uncertainty is small next to how
sharply the function bends, and a long stretch with no sign match is exactly
when it is not. The UKF, in :doc:`the appendix <l3_appendix>`, is built for
this case.


.. _l3-divergence:

The Catch: a Feedback Loop
~~~~~~~~~~~~~~~~~~~~~~~~~~

A tangent is only right **near where it touches**. The EKF draws it at its
**own estimate**, so a wrong estimate puts it in the wrong place.

.. figure:: /_static/images/L3/ekf_story_4_loop.png
   :alt: Loop diagram. A gray box, the estimate is a little off, points into an orange loop of four boxes: the tangent is drawn in the wrong place; the correction is the wrong size; if it is far enough off, the next estimate is worse; the next tangent is drawn at that estimate; and back. In the middle: each turn starts from a worse place. A shaded box: meanwhile P shrinks at every update, right or wrong. Confident and wrong: divergence.
   :width: 80%
   :align: center

   The feedback loop. The estimate is a little off, so the tangent is drawn in
   the wrong place, so the correction is the wrong size. If the estimate is far
   enough off, the next estimate is worse, and the next tangent is drawn at
   that worse estimate. Each turn starts from a worse place. Meanwhile
   :math:`P` shrinks at every update, right or wrong.

This is what the update subsection asked you to hold on to: the surprise is
not in the :math:`P` line, so every update shrinks :math:`P`, whether the
update was good or not. The filter does not check. **The filter becomes more
confident as it becomes less accurate.** That is **divergence**. Run 2 still
improved; the loop starts only when the error is large enough to make the next
estimate worse.


Three Traps When You Build an EKF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each one costs somebody an evening in GP3.

1. **Wrap angles, in three places:** inside :math:`f`, in the surprise
   :math:`\boldsymbol{\nu}`, and in :math:`\hat{\mathbf{x}}` after the update.
   179° and -179° are 2° apart, not 358°. Subtract them the naive way and the
   filter sees a huge surprise and swings the AV almost all the way around to
   fix a 2° error. Wrap every angle into -180° to 180°:
   ``np.arctan2(np.sin(a), np.cos(a))``.
2. **Test the Jacobians.** A Jacobian worked out by hand with one sign wrong
   gives a filter that runs, does not crash, converges, and is wrong. Nothing
   tells you. The test is one loop: nudge each input a little, see how each
   output moves, and compare that measured slope with :math:`F_k` and
   :math:`H_k`. The hands-on checks it with
   ``python3 ekf_curve.py --check-jacobian``. Do it once, in a test, before
   the filter ever sees data.
3. **Rebuild** :math:`F_k`, :math:`Q_k` **and** :math:`H_k` **every step**,
   at the right point: :math:`F_k` and :math:`Q_k` before predict moves
   :math:`\hat{\mathbf{x}}`, :math:`H_k` after. Computing :math:`F_k` after
   moving ``x`` is a quiet bug.

.. admonition:: Where that leaves us: the EKF
   :class: tip

   **The problem:** a turn needs a cosine and a range a square root; a matrix
   only scales and adds.

   **The hack:** at each step, draw the tangent at the estimate and pretend it
   is the curve.

   **Two jobs:** the **estimate** goes through the real :math:`f` and
   :math:`h`; :math:`P` goes through the Jacobians :math:`F_k`, :math:`H_k`
   (and :math:`Q_k`), rebuilt every step.

   **The catch:** a tangent in the **wrong place** (:math:`P` shrinks anyway:
   **divergence**), or a curve that bends across the uncertainty (:math:`P`
   too small: **overconfident**). That second failure is what the UKF is
   for: see the appendix, :doc:`l3_appendix`.


.. _l3-ekf-check:

Check: the EKF
~~~~~~~~~~~~~~

.. admonition:: Answer each one before you open the answers
   :class: hint

   1. In the EKF, what goes through the real :math:`f`, and what goes through
      the Jacobian?
   2. Why is :math:`Q_k` rebuilt every step?
   3. Where is each Jacobian worked out, and why does that matter when the
      estimate is off?
   4. One sign in your Jacobian is wrong, and the filter still runs. How do you
      catch it?

.. dropdown:: Check: the EKF. Answers
   :color: success
   :icon: check-circle

   1. The **estimate** goes through the real functions: :math:`f` to predict,
      :math:`h` for the expected reading. Everything that touches an
      uncertainty, :math:`P`, :math:`S` and :math:`K`, goes through the
      tangents, the Jacobians :math:`F_k` and :math:`H_k`.
   2. The noise is in the wheel speed and the gyro. :math:`G`, the slope of
      :math:`f` for each of those inputs, carries it into :math:`x`,
      :math:`y` and :math:`\theta`, and :math:`G` holds the cosine and sine of
      the heading. The heading changes, so :math:`Q_k` changes.
   3. :math:`F_k` at the last estimate, :math:`H_k` at the prediction. If the
      estimate is off, the tangent is drawn in the wrong place, the correction
      comes out the wrong size, and the next Jacobian is drawn at a worse
      estimate still. That is the feedback loop, and :math:`P` keeps shrinking
      while it happens.
   4. Nudge each input a little, see how each output moves, and compare with
      your formula: a numerical check, about ten lines, before the filter ever
      sees data. The hands-on script does exactly that with
      ``--check-jacobian``.


.. _l3-ekf-hands-on:

Hands-On: the Curved Tunnel EKF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same idea as the Kalman filter hands-on, one step harder. The tunnel now
bends 120° to the left. The data is ``curve_drive.csv``: 21 s through the
bend, one row every 0.1 s, in the folder ``lecture3/curved_tunnel/`` of the
course repository.

- ``wheel_v``, ``gyro_w``: speed and turn rate, the **control input**
  :math:`\mathbf{u}`.
- ``sign_id``, ``sign_range``, ``sign_bearing``: a sign match, the **range
  and bearing** to a mapped sign, :math:`\mathbf{z}`.
- ``true_x``, ``true_y``, ``true_theta``: the truth, **never used by the
  filter**, only to score it.

The range and bearing are a square root and an arctangent, so neither model
is a matrix: a job for the EKF.

- **Watch:** the heading :math:`\sigma` climbs between signs and drops at each
  match.
- **Raise** :math:`Q` (gyro noise): :math:`\sigma` climbs faster and the band
  gets fatter.
- **Tick "wrong sign":** the filter still runs, and the heading error leaves
  the band. That is exactly the problem.

Step 1: Run the Script
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   cd enpm818z-fall-2026-carla-python/lecture3/curved_tunnel
   python3 ekf_curve.py --make-csv        # the data
   python3 ekf_curve.py --check-jacobian  # test F_k and H_k first
   python3 ekf_curve.py                   # the live window

Run the Jacobian check before anything else. It nudges every input, measures
how every output moves, and compares that with the formulas in the file. It
should say OK. That is the habit to build for GP3. Then open ``run_ekf()``,
next to the plain filter from the tunnel hands-on: it is the loop from
"The EKF Lines in Code", with :math:`f`, :math:`h` and the Jacobians around
it. Without a desktop, ``--html ekf.html`` writes the animation as a web page.

Step 2: Watch the Heading Sawtooth
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/tunnel_ekf_sigma.png
   :alt: Sigma of the heading in degrees over 21 s. A blue sawtooth starts near 2.6 degrees, climbs slowly between sign matches and drops at each one, marked by thin orange lines every 2.5 s, settling between about 1.0 and 1.4 degrees. The bend, 2 to 14.6 s, is shaded yellow. A black line marks 10 s.
   :width: 75%
   :align: center

   The top-right plot of the EKF window. Yellow marks the bend; the black line
   is this snapshot, :math:`t = 10` s.

The curve is :math:`\sigma` of the **heading**: how uncertain the filter is
about which way the nose points. It **climbs** while only the gyro drives the
prediction, and **drops** at each sign match, the thin orange lines, because
the **bearing** to the sign tells the filter which way the AV faces. It
settles between about **1.0 and 1.4°**. It barely changes in the bend: the
EKF handles the curve as long as its straight-line pieces are short.

Step 3: Check That the Filter Is Honest
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/tunnel_ekf_error.png
   :alt: The true heading error in degrees over 21 s, an orange line, against a light blue band of plus and minus sigma. The line starts near 2.5 degrees, above the band, drops inside it at the second sign match, and stays mostly inside or near the band, ending near 1 degree. The bend is shaded yellow; a black line marks 10 s.
   :width: 75%
   :align: center

   The bottom-right plot of the EKF window. The line starts near 2.5°, above
   the band, and drops inside it at the second sign match.

The orange line is the **true heading error**: the estimated heading minus the
real one. **Positive** means the estimate points too far left. You can draw it
only because the CSV has the ground truth. The blue band is the filter's own
claim, :math:`\pm 1\sigma`. An honest filter keeps the line inside about
**68 percent** of the time. Here: **65 percent**, close enough.

Now tick the check box *wrong sign in the Jacobian* (or pass
``--wrong-sign``). The filter still runs, with no error message, but the line
leaves the band and only **30 percent** stays inside. That is how a Jacobian
bug shows up in real life: not a crash, a filter that is quietly wrong.

Step 4: Move the Sliders
^^^^^^^^^^^^^^^^^^^^^^^^

Predict first, then move the slider and check. (On the command line:
``--gyro-noise`` in °/s and ``--range-noise`` in m.)

.. list-table::
   :widths: 30 15 15 14 26
   :header-rows: 1
   :class: compact-table

   * - **Setting**
     - **Position error**
     - **Heading error**
     - **Inside 1σ**
     - **What it shows**
   * - default: gyro 2°/s, range 1 m
     - 0.69 m
     - 1.4°
     - 65%
     - honest
   * - :math:`Q` too small: gyro 0.1°/s
     - 1.18 m
     - 2.1°
     - 23%
     - **overconfident**
   * - :math:`Q` too big: gyro 8°/s
     - 0.75 m
     - 1.8°
     - 92%
     - underconfident
   * - :math:`R` too small: range 0.1 m
     - 1.42 m
     - 1.8°
     - 46%
     - trusts every match
   * - wrong sign in :math:`F_k`
     - 1.23 m
     - 4.0°
     - 30%
     - **runs, and is wrong**

Shrink :math:`Q` and the filter trusts its gyro far too much: only a quarter
of the time inside the band, overconfident again. Make :math:`Q` huge: honest
but pessimistic. Make :math:`R` tiny: it chases every match. In the last row,
one wrong sign in the Jacobian almost doubles the position error and almost
triples the heading error, and the filter never complains. On a real AV you
have no truth column, so the only defenses are the numerical Jacobian check
and the consistency test in the next section.

.. note::

   **The default gyro noise is 2°/s**, bigger than the real 1.1°/s, on
   purpose: the gyro also has a small bias the filter does not model, and
   :math:`Q` must cover it. Same lesson as the tunnel hands-on.


.. _l3-choosing:

Choosing a Filter
~~~~~~~~~~~~~~~~~

.. admonition:: Where that leaves us: choosing a filter
   :class: tip

   .. list-table::
      :widths: 15 85
      :header-rows: 1
      :class: compact-table

      * - **Filter**
        - **Use it when**
      * - **KF**
        - the model really is **linear**: rare, but exact when true
      * - **EKF**
        - the model **curves gently**. The default for estimating a vehicle's
          state, and **GP3 uses it**
      * - **UKF**
        - the model **curves hard** (a wide covariance on a curve), or you
          have no Jacobian (:doc:`l3_appendix`)
      * - **PF**
        - the belief has **several peaks** and the state is small
          (:doc:`l3_appendix`)

   **None of them checks whether its confidence is deserved.** Every one
   shrinks its covariance, or tightens its crowd of particles, on every
   update, whether or not the update was any good. That is not a mistake in
   the algorithms; it is built in. The next section finally takes up Job 2
   from the introduction, trust: telling an honest covariance from a made-up
   one.


.. _l3-consistency:

Checking the Covariance
-----------------------

- **Where we are:** four filters, and when to choose each; none checks its own
  confidence.
- **In this section:** a test of the filter's uncertainty: compare each
  surprise with :math:`S`, the size the filter predicted for it.
- **What it is for:** knowing whether to trust the :math:`\sigma` the filter
  reports. No ground truth needed.

This section is short, but it is the half of the lecture to keep if you keep
only half. Say the filter tells you :math:`\sigma` is 20 cm. This is how you
find out whether to believe it.

Every filter gives you two things: an estimate and a covariance. Most people
use the estimate and ignore the covariance. That is backwards. The covariance
is the filter's claim about its own accuracy, and that claim can be tested
**without ground truth**. Remember :math:`S`: before the filter sees a
reading, :math:`S` says how big the surprise should be. So we compare the
surprises we actually get with the ones it predicted. No survey, no better
sensor, no right answer: only numbers the filter already has. It can run on
the AV all the time, for about one line of code.


.. _l3-nis:

The Test: Actual Surprise over Expected Surprise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \varepsilon \;=\; \frac{\text{surprise}^2}{\text{expected surprise}}
   \;=\; \frac{\nu^2}{S}

That is one number, along the tunnel. With :math:`x` and :math:`y` together:
:math:`\varepsilon = \boldsymbol{\nu}^\top S^{-1}\boldsymbol{\nu}`, the same
thing, because dividing by a matrix means multiplying by its inverse.

.. admonition:: Definition: normalized innovation squared (NIS)
   :class: note

   :math:`\varepsilon` above (innovation = the surprise
   :math:`\boldsymbol{\nu}`). If the filter is honest, it averages **about 1**
   per number the sensor reports: 1 for a range, 2 for a sign match giving
   :math:`x` and :math:`y`.

In words: how surprised the filter was, divided by how surprised it said it
would be. The ratio has no units.

- **Why divide?** A surprise of 3 m means nothing on its own. If the filter
  expected 10 m, 3 is excellent. If it expected 10 cm, 3 is a crisis.
  Dividing by what it expected makes the number mean something, and lets us
  compare sensors and moments in time.
- **Why** :math:`\boldsymbol{\nu}` **twice?** For the same reason :math:`F`
  appears twice in :math:`FPF^\top`: it squares the surprise, so being wrong
  high and wrong low count the same.

**The hands-on at 9.3 s, along the tunnel:** :math:`\nu = 0.74`,
:math:`S = 2.84`, so :math:`\varepsilon = 0.74^2 / 2.84 = 0.19`. One reading
tells us little; it can land anywhere. The average is what counts. Over all 19
sign matches, :math:`x` and :math:`y` together, the average is **1.39** per
match (expected: 2, one per number). Is that low? With only 19 matches, chance
alone puts the average anywhere from **1.2 to 3.0**, 95 percent of the time.
So 1.39 is **honest**; nineteen matches cannot call it cautious.


Reading Epsilon over Time: Above, Below or Inside the Band
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For an honest filter, :math:`\varepsilon` follows a **chi-square**
distribution. All you need from that name is the band it gives: for a sign
match giving :math:`x` and :math:`y`, an honest filter keeps
:math:`\varepsilon` between about **0.05 and 7.4**, 95 percent of the time
(the chi-square band for 2 numbers).

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - :math:`\varepsilon` **keeps landing**
     - **The filter is**
   * - **above** the band
     - **overconfident**: the surprises are bigger than it predicted.
       :math:`Q` or :math:`R` is too small. **Dangerous.**
   * - **below** the band
     - **underconfident**: it throws information away. Wasteful, but safe.
   * - **inside** the band
     - **honest**. Its :math:`\sigma` means something.

Above, dangerous. Below, wasteful. Inside, trustworthy. Log
:math:`\varepsilon` from the first day you write a filter. It costs one line.


.. _l3-gating:

Gating: Throw Away a Reading That Is Wildly Off
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same number has a second job, one reading at a time: throwing away a
reading that is wildly off. This is called **gating**.

.. math::

   \varepsilon > 9.21 \quad\Longrightarrow\quad \text{throw the reading away}

9.21 is the 99 percent line for a sign match reporting :math:`x` and
:math:`y`. It is the number you will hard-code. When a reading is gated, skip
it and run on prediction alone for that cycle.

This catches a **wrong sign match**: the camera misreads a sign's number, so
the match arrives on time, looks normal, and is 25 m wrong. The filter
expected a surprise under 2 m, so :math:`\varepsilon` comes out huge. Over the
gate, gone.

.. warning::

   **The trap:** a filter that is *already* wrong rejects the good readings. A
   gate throws out whatever disagrees with the current estimate. If the
   estimate is already wrong, the correct readings are the ones that disagree,
   so the gate throws them out and keeps the error. **Count rejections in a
   row**, and past a limit, raise an alarm: declare the filter unhealthy.


Next Class
----------

**L4: Perception I, Detecting Objects**

- From pixels to features: what a CNN computes.
- Grading a detector: IoU, precision, recall, mAP.
- One-stage detectors (YOLO) and transformers (DETR, RT-DETR).
- Two detectors side by side on a CARLA frame.

**Before next class**

- Run the four hands-on scripts (KF, EKF, UKF, PF) and move every slider.
  **Most important: turn** :math:`Q` **down in** ``kf_tunnel.py`` **until the
  filter fails, and watch the share of time inside** :math:`1\sigma` **catch
  it.** Spotting a filter that has stopped listening is a skill you will need
  in every project, and nobody learns it by reading.
- **Read the appendix** (:doc:`l3_appendix`): the worked numbers, the UKF and
  particle filter details, and each filter's code. Read it before GP3.
- **GP1 is posted.** It builds on L2's calibration work rather than on this
  lecture's filter.

**How the lectures connect**

- L1 gave the vocabulary and the failure cases. L2 gave the sensors and the
  geometry connecting them.
- **L3 gave the filter that combines them, and the test that shows whether to
  trust it.**
- L4 gives the detector that produces the measurements this filter has been
  assuming.

.. admonition:: Summary
   :class: important

   Report the covariance, and then test it. An uncertainty you have not
   checked tells you nothing useful.


.. rubric:: Image credits

The vehicle icons in the figures on this page were created by Stone from the
`Noun Project <https://thenounproject.com>`_.
