====================================================
Lecture
====================================================

.. note::

   These notes are the primary reference for L3. There is no separate slide
   deck yet. The deck will be built from these notes, so if the two ever
   disagree, use these notes.

.. important::

   **Perception is not covered here.** This lecture assumes measurements
   arrive from somewhere and asks what to do with them. The detector that
   turns pixels into boxes is :doc:`L4 <../lecture4/l4_index>`.

   **Learned fusion is not covered here either.** Cross-attention and
   BEVFusion are :doc:`L6 <../lecture6/l6_index>`. Monte Carlo
   Localization, which applies the particle filter to localization, is
   :doc:`L7 <../lecture7/l7_index>`.

.. admonition:: Class logistics for this week
   :class: warning

   **Quiz 1 is given at the start of class** and covers L1 and L2. Closed
   notes, about 15 minutes. The lecture starts afterwards, so we have less
   time than usual.

   **Teams form this week**, and **GP1 is posted** after class. GP1 builds
   on L2's calibration work. This lecture feeds **GP3**.


Introduction
------------

Closing the Loop
~~~~~~~~~~~~~~~~

L2 finished with sensors that are mounted, calibrated and time stamped, and
with a promise that everything you calibrate is what L3 combines.

Now that those sensors are running, a problem appears that calibration does
not solve. **They disagree with each other.** The GNSS says the car is in
one place, the LiDAR says it is somewhere slightly different, and the wheels
say something different again. None of them is lying and none of them is
exactly right.

Worse, L2 showed that one of them can be wrong in a way you cannot see. In a
street lined with tall buildings, a GNSS fix can arrive on time, look
completely normal, and still be several metres out.

So you have several disagreeing numbers, arriving at different times, one of
which may be quietly wrong, and the planner downstream needs **one** answer.
Producing that one answer is the job of a filter.


What a Filter Is
~~~~~~~~~~~~~~~~

The word **filter** appears constantly from here on, so here is what it
means before it starts turning up in questions.

.. important::

   A **filter** is a piece of software that keeps a running estimate of
   something you cannot measure directly. It updates that estimate every
   time a new measurement arrives, and it reports how uncertain the estimate
   currently is.

   It holds two things at all times: **the estimate**, and **how much to
   trust it**.

Four reasons a car cannot just use the newest reading instead.

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: table-hover

   * - **Problem**
     - **What the filter does about it**
   * - No single sensor is enough
     - GNSS gives absolute position but slowly, and not in tunnels. An IMU
       is fast and always available but drifts. The filter combines them so
       the pair behaves better than either one.
   * - Readings arrive at different times
     - Sensors run at different rates and never line up neatly. The filter
       carries an estimate forward continuously, so there is an answer
       available at every instant.
   * - Every reading is noisy
     - Steering on whatever the last reading said would make the car
       twitch. The filter blends each new reading into what it already
       believed, in the correct proportion.
   * - Some quantities are never measured
     - No sensor reports your velocity directly, but the planner needs it.
       The filter works it out from how the position keeps changing.

.. note::

   The name comes from signal processing, where a filter removes noise from
   a signal and passes the real content through. A state estimation filter
   does the same job: many noisy readings go in, one cleaner estimate comes
   out.

Two questions decide whether that filter is any good.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Question 1. Combining
      :class-header: bg-primary text-white

      Two sensors report different numbers for the same quantity. Neither
      one is right.

      What does the filter report? There is an exact answer, and it is not
      the average.

   .. grid-item-card:: Question 2. Trust
      :class-header: bg-warning

      The filter reports a position **and** an uncertainty.

      How do you check that the uncertainty is correct? A filter that is
      wrong does not crash. It reports a small number and keeps running.

.. admonition:: The main idea of this lecture
   :class: danger

   A filter reports two things: an estimate, and how uncertain that estimate
   is. **The uncertainty is the one that causes trouble**, because when it
   is wrong, nothing in the system detects it.

   L2 made the same point about hardware: a dirty sensor does not report an
   error, it reports data. The same failure happens inside the algorithm. An
   overconfident filter reports plus or minus 0.2 m while being 3 m wrong,
   and no alarm is raised anywhere.


.. _l3-tempe-reminder:

A Reminder. What Happened at Tempe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a third question, and the two above quietly assume it has already
been answered.

A filter combines measurements **of one object**. Before it can do that,
something has to decide which measurements belong to that object in the
first place. With one car on an empty road that decision is trivial. With
traffic it is not, and getting it wrong does not produce a slightly worse
estimate. It produces a confident estimate of something that never happened.

That is not a hypothetical. It is what killed someone in 2018, so it is
worth recalling the details now, before the vocabulary arrives to describe
them. L1 covered this case in full, and here is the short version.

On the night of 18 March 2018, in Tempe, Arizona, a test vehicle driving
itself struck and killed a woman who was walking a bicycle across a wide,
straight road. She was not at a crosswalk. A safety operator was sitting in
the driver's seat but was not watching the road. The car was moving at about
43 mph. It was the first case of a self-driving car killing a pedestrian.

The timings below come from the United States National Transportation Safety
Board investigation, report **NTSB/HAR-19/03**.

.. list-table::
   :widths: 24 76
   :header-rows: 1
   :class: compact-table

   * - **Time before impact**
     - **What the system did**
   * - about 5.6 s
     - The radar and the LiDAR both detected her. She was in the sensor data
       from this point onward.
   * - 5.6 s to 1.3 s
     - The software repeatedly changed its classification of her: first an
       unknown object, then a vehicle, then a bicycle. Each change also
       changed the predicted path.
   * - 1.3 s
     - The software determined that hard braking was required.
   * - 1.3 s to 0.3 s
     - Braking was **held back for one full second by design**, to prevent
       the car braking hard for objects that turn out not to be real. The
       human operator was expected to intervene during this second.
   * - impact
     - The car did not brake. The operator did not intervene.

.. important::

   The second row is the one that matters here.

   She was in the sensor data for more than five seconds, so nothing failed
   to detect her. What the system could not do was recognise that the object
   it saw now was the same object it had seen a moment earlier. Each time
   the classification changed, the software treated her as a new object and
   discarded everything it had learned.

   :ref:`l3-data-association` explains why that is fatal, once the
   vocabulary is available to state it precisely.


.. _l3-roadmap:

The Path Through This Lecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The two questions above split into a chain. Every section answers a question
raised by the one before it.

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: table-hover

   * - **Section**
     - **The question it answers**
   * - Terminology
     - What do the words and the symbols mean?
   * - Fusion Architectures
     - At what point in the system should two sensors meet?
   * - Combining Two Estimates
     - Two estimates of the same thing disagree. What do you report?
   * - The Kalman Filter
     - The same question, except the car keeps moving and there is more
       than one quantity to track.
   * - When the Assumptions Break
     - That filter is only correct under four conditions. Three of them
       fail on a real vehicle. Now what?
   * - Checking That the Filter Is Consistent
     - Every filter reports a confidence. How do you tell whether it is
       honest?
   * - Data Association
     - All of the above assumed you knew which measurement came from which
       object. What if you do not?
   * - CARLA Hands-On
     - Build one, and watch it fail in the way this lecture predicts.

The first half answers Question 1 and the second half answers Question 2.
**The last two sections are where the Tempe crash lives**, so keep the
reminder above in mind as you go.


.. _l3-no-ai:

.. admonition:: There is almost no AI in this lecture, and that is deliberate
   :class: important

   Students often arrive at a self-driving course expecting every part of it
   to be a neural network. This lecture is the part that is not.

   Everything here is classical probability and linear algebra, and most of
   it is old.

   .. list-table::
      :widths: 46 18 36
      :header-rows: 1
      :class: table-striped

      * - **Technique**
        - **Year**
        - **What it is**
      * - Mahalanobis distance
        - 1936
        - A distance measure
      * - Hungarian algorithm, used by GNN
        - 1955
        - An assignment algorithm
      * - Kalman filter
        - 1960
        - Linear algebra, in closed form
      * - MHT
        - 1979
        - A search over hypotheses
      * - JPDA
        - 1983
        - Weighted averaging
      * - Unscented Kalman filter
        - 1997
        - Sampling, then averaging
      * - Particle filter for localization
        - 1999
        - Sampling, then resampling

   None of these is trained. None has weights. Each one does exactly the
   same thing every time you run it on the same input, and you can work out
   by hand what it will do.

   **Why the oldest part of the stack is still the one deciding where the
   car is.** Three reasons, and they are the themes of this lecture.

   - It reports **calibrated uncertainty**. The covariance means something
     specific, and :ref:`l3-consistency` can test whether it is honest.
     Getting a neural network to report a trustworthy confidence is an
     open research problem.
   - It is **inspectable**. When it goes wrong you can find out why, which
     matters enormously for a safety case, as L1 discussed.
   - Under stated conditions it is **provably the best possible** estimator.
     No amount of training data beats it on its own terms.

   **Where the AI actually is.** The filter here assumes measurements simply
   arrive. Producing those measurements is almost entirely learned, and that
   is the rest of the semester: detection in :doc:`L4 <../lecture4/l4_index>`,
   bird's-eye-view and occupancy in :doc:`L5 <../lecture5/l5_index>`,
   learned fusion and tracking in :doc:`L6 <../lecture6/l6_index>`, behaviour
   prediction in :doc:`L9 <../lecture9/l9_index>`, and end-to-end driving in
   :doc:`L12 <../lecture12/l12_index>`.

   **The division of labour is the point.** Learned components turn pixels
   into objects, because no one can write that by hand. Classical estimation
   then decides what to believe about those objects over time, because that
   part has to be verifiable. A modern stack is both, and knowing which half
   you are debugging is a genuinely useful skill.

   .. note::

      The boundary does move. Modern trackers often learn an appearance
      descriptor to help decide which detection belongs to which track, and
      there is active research on learned motion models and on filters you
      can train through. **The structure in this lecture is what those
      systems are still built around**, which is why it is worth knowing
      before you replace any part of it.


Terminology
-----------

Four things have to be clear before the rest of the lecture makes sense.
The frame the numbers are measured in. The symbols used to write them. What
an uncertainty actually is. And what a statement of confidence actually
claims.

None of this is hard. But all of it is assumed later, and two of the words
mean something narrower here than they do in ordinary speech.

.. _l3-road-frame:

.. admonition:: First, the frame these numbers are measured in
   :class: note

   L2 established that a position means nothing until you say what frame it
   is measured in. Every example in this lecture uses the same frame, so it
   is defined once here.

   Place a survey marker at the roadside and use it as the origin. Measure
   :math:`x` **along** the road from the marker, and :math:`y` **across**
   the road, positive toward the far kerb. A position is then the pair
   :math:`(x, y)`, both in metres.

   So a sensor reporting :math:`(103.0,\ 2.5)` is saying the car is 103.0 m
   past the marker and 2.5 m to the side of it. **Those numbers are
   coordinates, not lengths.**

.. _l3-notation:

Notation
~~~~~~~~

This lecture uses more symbols than the previous two. They are collected
here so you have one place to come back to. Nothing here needs to be read
in order, and every symbol is introduced properly where it is first used.

**Statistics**

.. list-table::
   :widths: 14 30 56
   :header-rows: 1
   :class: table-striped

   * - **Symbol**
     - **Name**
     - **Meaning**
   * - :math:`\mu`
     - mu, the mean
     - The average of a set of readings. Subscripted per axis, so
       :math:`\mu_x` and :math:`\mu_y`.
   * - :math:`\mathbb{E}[\,\cdot\,]`
     - expectation
     - The average of whatever is inside the brackets, taken over all
       possible outcomes rather than a finite sample.
   * - :math:`\operatorname{Var}(X)`
     - variance
     - How spread out the readings are, in squared units.
   * - :math:`\sigma`
     - sigma
     - Standard deviation, the square root of the variance, back in the
       original units. Most uncertainties in this course are quoted this
       way.
   * - :math:`\sigma^2`
     - sigma squared
     - The variance again. The two notations are used interchangeably.
   * - :math:`\operatorname{Cov}(x, y)`
     - covariance
     - How much the errors in :math:`x` and :math:`y` move together. Zero
       when they are independent.
   * - :math:`\mathcal{N}(\mu, \sigma^2)`
     - normal distribution
     - A bell curve with that mean and variance. Reading
       :math:`\mathbf{w} \sim \mathcal{N}(0, Q)` aloud: "the noise
       :math:`\mathbf{w}` is drawn from a bell curve centred on zero with
       covariance :math:`Q`."

**The state and the two models**

.. list-table::
   :widths: 14 30 56
   :header-rows: 1
   :class: table-striped

   * - **Symbol**
     - **Name**
     - **Meaning**
   * - :math:`x, y`
     - coordinates
     - Position along and across the road, as set out in
       :ref:`the road frame <l3-road-frame>`. Plain italics, not bold.
   * - :math:`\mathbf{x}`
     - the state
     - **Bold**, so a whole vector of quantities being estimated, such as
       :math:`[p_x\ p_y\ v_x\ v_y]^\top`. Do not confuse it with the
       coordinate :math:`x`.
   * - :math:`\hat{\mathbf{x}}`
     - x-hat
     - The filter's **estimate** of the state. The hat always means "our
       best guess at", never the true value, and it is used on scalars too,
       as in :math:`\hat{x}`.
   * - :math:`\hat{\mathbf{x}}^-`
     - x-hat-minus
     - The estimate **after predicting but before using the measurement**.
       The minus superscript marks every such prior quantity.
   * - :math:`P`
     - state covariance
     - How uncertain the filter is about the state, and how those
       uncertainties are linked. :math:`P^-` is its predicted version.
   * - :math:`F`
     - transition matrix
     - How the state changes on its own over one timestep.
   * - :math:`Q`
     - process noise covariance
     - How wrong :math:`F` is. Tuned, not measured.
   * - :math:`H`
     - measurement matrix
     - Which parts of the state the sensor observes.
   * - :math:`R`
     - measurement noise covariance
     - How noisy the sensor is. Measured, quoted or set, never guessed.
       See :ref:`where it comes from <l3-where-sigma-comes-from>`.
   * - :math:`\mathbf{z}`
     - measurement
     - What the sensor actually reported.
   * - :math:`\mathbf{u}`
     - control input
     - What you told the vehicle to do, such as a commanded acceleration or
       steering angle. Known, so it helps the prediction.
   * - :math:`\mathbf{w}, \mathbf{v}`
     - process and measurement noise
     - The random parts of the two models, with covariances :math:`Q` and
       :math:`R`.
   * - :math:`\Delta t`
     - delta t
     - The time between one step and the next.
   * - :math:`k`
     - time index
     - Which step you are on, so :math:`\mathbf{x}_k` is the state now and
       :math:`\mathbf{x}_{k-1}` the state one step ago.
   * - :math:`f, h`
     - nonlinear models
     - The nonlinear versions of :math:`F` and :math:`H`, used by the EKF
       and UKF.

**The update, and checking it**

.. list-table::
   :widths: 14 30 56
   :header-rows: 1
   :class: table-striped

   * - **Symbol**
     - **Name**
     - **Meaning**
   * - :math:`\boldsymbol{\nu}`
     - nu, the innovation
     - Measurement minus predicted measurement. The surprise.
   * - :math:`S`
     - innovation covariance
     - How large the filter expected that surprise to be.
   * - :math:`K`
     - Kalman gain
     - What fraction of the surprise the filter acts on.
   * - :math:`I`
     - identity matrix
     - Ones on the diagonal, zeros elsewhere. Multiplying by it changes
       nothing.
   * - :math:`\varepsilon`
     - epsilon, the NIS
     - Normalised innovation squared, the consistency check of
       :ref:`l3-consistency`.
   * - :math:`\chi^2_m`
     - chi-square
     - The distribution :math:`\varepsilon` should follow if the filter is
       honest, with :math:`m` degrees of freedom.
   * - :math:`d^2`
     - Mahalanobis distance squared
     - Disagreement measured in units of expected disagreement, used for
       data association.
   * - :math:`m`
     - degrees of freedom
     - How many numbers the sensor reports at once. Two, for a fix giving
       :math:`x` and :math:`y`.
   * - :math:`\top`
     - transpose
     - Flips a matrix or vector on its diagonal, as in
       :math:`\boldsymbol{\nu}^\top`.

.. warning::

   **Two symbols do double duty, so watch for them.**

   :math:`x` is a road coordinate in plain italics and a whole state vector
   in bold :math:`\mathbf{x}`. The typeface is the only difference.

   :math:`n` counts readings when you see :math:`\sigma/\sqrt{n}`, and
   counts the size of the state when you see :math:`2n+1` sigma points in
   the UKF.

.. note::

   **If you read other textbooks**, be aware that most of them write the
   innovation as :math:`\mathbf{y}` rather than :math:`\boldsymbol{\nu}`.
   This lecture uses :math:`\boldsymbol{\nu}` because :math:`y` is already
   the across-road coordinate here, and the two would collide in exactly the
   formulas where clarity matters most. The tracking literature, including
   Bar-Shalom, uses :math:`\boldsymbol{\nu}` as well.

.. _l3-uncertainty:

Uncertainty, Noise and Bias
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Uncertainty** is a number attached to an estimate that says how far the
truth could plausibly be from it. A GNSS fix of 100.0 m with an uncertainty
of 2 m is a claim that the truth is probably within a couple of metres of
100.0 m. Without that second number, the first number cannot be combined
with anything, which is why this lecture needs it.

.. admonition:: The formal definition
   :class: seealso

   The **VIM** (JCGM 200:2012, clause 2.26) defines *measurement
   uncertainty* as a non-negative parameter that characterises the spread of
   the values that could reasonably be attributed to the quantity being
   measured.

   In practice that parameter is a standard deviation, which is what the
   next subsection builds.

An estimate is wrong for two different reasons, and the difference decides
what you can do about it.

.. list-table::
   :widths: 18 40 42
   :header-rows: 1
   :class: table-striped

   * - **Kind of error**
     - **What it looks like**
     - **What happens if you average many readings**
   * - **Random error**, also called **noise**
     - Readings scatter around some centre. Each one is wrong by a different
       amount, in a different direction.
     - It **averages away**. More readings give a better answer.
   * - **Systematic error**, also called **bias**
     - Every reading is shifted the same way. The scatter can be tiny.
     - It **does not average away**. A thousand readings give you a very
       precise wrong answer.

Here are two GNSS receivers, both reporting the :math:`x` coordinate of the
same car, whose surveyed position is :math:`x = 100.0` m:

.. list-table::
   :widths: 14 50 18 18
   :header-rows: 1

   * - **Receiver**
     - **Six readings (m)**
     - **Their mean**
     - **Their** :math:`\sigma`
   * - A
     - 102.1, 98.6, 100.9, 99.2, 101.4, 97.8
     - 100.0
     - 1.561
   * - B
     - 105.3, 101.8, 104.1, 102.4, 104.6, 101.0
     - 103.2
     - 1.561

.. danger::

   **The two receivers have exactly the same** :math:`\sigma`.

   Their readings scatter by identical amounts. But receiver A is centred on
   the truth, and receiver B is centred 3.2 m away from it. Receiver B has a
   **bias** of +3.2 m.

   So :math:`\sigma` tells you **nothing at all** about whether a sensor is
   centred on the truth. It only describes the scatter. A sensor can have a
   small :math:`\sigma` and be useless.

This matters for the rest of the lecture because the Kalman filter handles
these two cases very differently. Noise is what :math:`R` describes, and the
filter deals with it correctly. Bias violates one of the filter's
assumptions, so the filter does **not** deal with it, and will integrate a
steady offset forever without complaint. That assumption is listed in
:ref:`l3-four-assumptions`, and Exercise 4 has you measure both on a real
CARLA sensor.

.. note::

   The everyday words for this pair are **accuracy** and **precision**.
   Accuracy is how close you are to the truth, so it is about bias.
   Precision is how repeatable you are, so it is about noise. Receiver B
   above is precise but not accurate.

   Be careful, because :ref:`the next section <l3-weighting>` gives
   "precision" a second, narrower meaning: one divided by the variance. Both
   meanings are standard and you will meet both. This lecture always means
   the narrow one when it writes :math:`1/\sigma^2`.

.. _l3-variance:

Variance
~~~~~~~~

Variance measures how spread out a set of measurements is. It is the
standard way of putting a number on the **noise** half of the table above.

Park the car at a surveyed point, so you know its true position is exactly
:math:`(100.0,\ 2.5)`. Ask the GNSS receiver where the car is six times
without moving it. You get six different answers:

.. code-block:: text

   (102.1, 1.4)   (98.6, 4.3)   (100.9, 3.1)
   ( 99.2, 1.2)   (101.4, 3.4)  ( 97.8, 1.6)

The **mean**, written :math:`\mu`, is the average, computed separately for
each axis:

.. math::

   \mu_x = \frac{600.0}{6} = 100.0 \text{ m},
   \qquad
   \mu_y = \frac{15.0}{6} = 2.5 \text{ m}

The **variance** describes how far the readings typically sit from that
mean:

.. math::

   \operatorname{Var}(X) = \mathbb{E}\left[(X - \mu)^2\right],
   \qquad \mu = \mathbb{E}[X]

Worked out on these six readings, one axis at a time:

.. list-table::
   :widths: 24 19 19 19 19
   :header-rows: 1
   :class: table-striped

   * - **Reading** :math:`(x, y)`
     - :math:`x - \mu_x`
     - **squared**
     - :math:`y - \mu_y`
     - **squared**
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

Divide each total of squares by the number of readings:

.. math::

   \operatorname{Var}(x) = \frac{14.62}{6} = 2.437 \text{ m}^2,
   \qquad
   \sigma_x = \sqrt{2.437} = 1.561 \text{ m}

.. math::

   \operatorname{Var}(y) = \frac{8.12}{6} = 1.353 \text{ m}^2,
   \qquad
   \sigma_y = \sqrt{1.353} = 1.163 \text{ m}

.. note::

   **Two numbers are not always enough to describe a two dimensional
   spread.**

   Computing a variance per axis assumes the two axes are independent, so
   that knowing the car read high in :math:`x` tells you nothing about
   :math:`y`. For these six readings that holds: the errors in :math:`x` and
   :math:`y` are essentially uncorrelated.

   When the axes are **not** independent, the errors lean in a preferred
   direction and you need a **covariance matrix** rather than two separate
   variances:

   .. math::

      P = \begin{bmatrix}
            \operatorname{Var}(x) & \operatorname{Cov}(x, y) \\
            \operatorname{Cov}(x, y) & \operatorname{Var}(y)
          \end{bmatrix}

   The off-diagonal entry measures that lean. It is zero here, so
   :math:`P = \mathrm{diag}(2.437,\ 1.353)`. Off-diagonal entries appear on
   their own as soon as a filter predicts forward, which is the subject of
   Exercise 2.

.. admonition:: Why the distances are squared
   :class: note

   Look at the two columns of distances. Each one adds up to **exactly
   0.0**, because the positive and negative values cancel. That is
   not a coincidence and it is not specific to these six numbers. The
   distances from the mean always sum to zero, by definition of the mean.

   So averaging the raw distances would report a spread of zero for a set of
   readings that clearly are spread out. Squaring removes the signs and
   stops the cancellation.

   Squaring also weights large errors more heavily. In the :math:`x`
   column, the 2.2 m miss contributes 4.84 to the total while the 0.8 m
   miss contributes 0.64. That is roughly seven times as much for a miss
   less than three times as large. In a vehicle, one large error matters
   more than several small ones, so this weighting is intentional.

Notice the units. The readings are in metres, so the squared distances and
both variances are in metres squared. That is hard to compare against
anything. Taking the square root gives the **standard deviation**:

.. math::

   \sigma = \sqrt{\operatorname{Var}(X)}

Here :math:`\sigma_x = 1.561` m and :math:`\sigma_y = 1.163` m, both back
in metres, so they can be compared directly against the vehicle or the lane
width. That is why
nearly every number in this course is quoted as a :math:`\sigma` rather than
a variance, even though the formulas are written in terms of variance.

If the readings follow a bell curve, which sensor noise often does, the
standard deviation tells you where readings land. Taking the :math:`x`
axis, with :math:`\mu_x = 100.0` m and :math:`\sigma_x = 1.561` m:

.. list-table::
   :widths: 20 22 28 30
   :header-rows: 1
   :class: table-hover

   * - **Range**
     - **In metres**
     - **Expected share inside**
     - **Of our six** :math:`x` **readings**
   * - :math:`\mu_x \pm 1\sigma_x`
     - 98.44 to 101.56
     - about 68%
     - 4 of 6, which is 67%
   * - :math:`\mu_x \pm 2\sigma_x`
     - 96.88 to 103.12
     - about 95%
     - 6 of 6
   * - :math:`\mu_x \pm 3\sigma_x`
     - 95.32 to 104.68
     - about 99.7%
     - 6 of 6

Six readings is far too few to confirm anything statistically, but the
counts already land close to the expected shares.

.. admonition:: Where the formal definition comes from
   :class: seealso

   - **ISO 3534-1:2006**, *Statistics. Vocabulary and symbols. Part 1:
     General statistical terms and terms used in probability.* The standards
     body definitions of variance and standard deviation.
   - **JCGM 200:2012**, the *International Vocabulary of Metrology (VIM)*,
     which is the same document L2 quoted for the definition of
     calibration. It defines standard measurement uncertainty as an
     uncertainty expressed as a standard deviation.
   - Casella, G. and Berger, R. L. (2002). *Statistical Inference*, 2nd
     edition. Duxbury.

.. warning::

   **Variance describes spread, not correctness.** Receiver B in
   :ref:`l3-uncertainty` had this exact :math:`\sigma` and was still 3.2 m
   off. Variance measures noise, and says nothing about bias.


.. _l3-confidence:

Confidence
~~~~~~~~~~

This word has a loose engineering meaning and a strict statistical meaning,
and they are not the same.

**The loose meaning** is how sure the system is. A small covariance means
sure, a large covariance means unsure. This is how the word gets used in
most engineering conversations and in most code comments, including in this
course. That is acceptable as long as you know it is informal.

**The strict meaning** comes from statistics. A **confidence interval** is a
range built from your data by a stated procedure. The **confidence level**,
such as 95%, describes how often that procedure succeeds.

Take the :math:`x` values from the same six GNSS readings. Their mean is
100.0 m. A confidence
interval is built on the uncertainty of that **mean**, which is
:math:`\sigma/\sqrt{n}` rather than :math:`\sigma`, so it uses
:math:`1.710/\sqrt{6} = 0.698` m rather than the 1.561 m spread of the
readings themselves. The standard 95% procedure then gives:

.. math::

   100.0 \pm 1.79 \text{ m}, \qquad \text{so } 98.21 \text{ to } 101.79
   \text{ m}

.. note::

   The 1.710 is the spread of the readings computed with the :math:`n-1`
   divisor rather than :math:`n`, which is the convention these interval
   procedures assume. With six readings that choice moves the answer by
   about 10%. Exercise 1 covers the difference.

.. danger::

   That interval does **not** mean there is a 95% chance the true
   coordinate lies between 98.21 and 101.79 m.

   Here is what it does mean. Imagine repeating the whole exercise many
   times: park the car, take six readings, build an interval the same way.
   About 95% of the intervals built that way would contain the true
   coordinate.

   The claim is about **the procedure**, not about the one interval you are
   holding. Your interval either contains 100.0 m or it does not. In this
   case we happen to know it does, because the point was surveyed, but on a
   real vehicle you never know. This is the most commonly misread idea in
   applied statistics.

Because that distinction is easy to get wrong, the measurement community
avoids the word. The **GUM** (JCGM 100:2008) and the **VIM** (JCGM 200:2012)
use **coverage interval** and **coverage probability** instead, so that
nobody has to guess which meaning was intended.

**What a Kalman filter reports is neither of those.** Its covariance is a
**Bayesian credible region**, which is a different and more useful
statement.

Suppose your filter reports the vehicle at :math:`(12.4,\ 3.1)` in the road
frame, with covariance

.. math::

   P = \begin{bmatrix} 0.25 & 0 \\ 0 & 0.64 \end{bmatrix},
   \qquad \sigma_x = 0.5 \text{ m}, \quad \sigma_y = 0.8 \text{ m}

.. important::

   The filter is claiming: given the model, there is a 95% probability that
   the vehicle is inside an ellipse centred on (12.4, 3.1) with semi-axes of
   **1.22 m across and 1.96 m along**.

   The first three words carry the weight. **Given the model.**

.. warning::

   **Two sigma is not 95% in two dimensions.**

   In one dimension, 95% of a bell curve lies within :math:`\pm 1.96\sigma`,
   so people round it to two sigma and move on. In two dimensions the
   95% ellipse sits at :math:`\sqrt{\chi^2_{2,\,0.95}} = \sqrt{5.991}
   = 2.45\sigma`, not :math:`2\sigma`.

   With the covariance above, that is the difference between semi-axes of
   1.22 m and 1.96 m (correct) and 1.00 m and 1.60 m (wrong). An ellipse
   drawn at two sigma in two dimensions actually contains about **86.5%** of
   the probability, not 95%.

   This matters whenever you draw an uncertainty ellipse or set a gate
   threshold, which is exactly what :ref:`l3-consistency` does.

The filter's uncertainty is only as good as the assumptions you supplied:
the motion model, the noise sizes, and the claim that the inputs are
independent. If any of those is wrong, the ellipse is still drawn, still
looks reasonable, and still means nothing.

Checking whether those assumptions hold is covered in
:ref:`l3-consistency`.

.. admonition:: Where the formal definitions come from
   :class: seealso

   - **ISO 3534-1:2006** defines confidence interval and confidence level.
   - **JCGM 100:2008** (GUM) and **JCGM 200:2012** (VIM) define coverage
     interval and coverage probability.
   - Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd edition. CRC
     Press, for credible intervals.


.. admonition:: Where this leads
   :class: tip

   You can now say exactly what an uncertainty is, how to measure it, and
   what a statement of confidence does and does not claim.

   The next question is a design one rather than a mathematical one. Before
   you can combine two sensors, you have to decide **at what point in the
   system they should meet**.

Fusion Architectures
--------------------

Before building the filter, one structural question: at what point in the
pipeline do the sensors meet? There are three answers, and your constraints
usually decide which one you get.

.. list-table::
   :widths: 16 28 28 28
   :header-rows: 1
   :class: table-striped

   * - **Level**
     - **What gets combined**
     - **Advantage**
     - **Cost**
   * - **Early**
     - Raw measurements: point clouds and pixels, before interpretation.
     - The most information available, since nothing is discarded before the
       combination.
     - Requires very accurate mounting calibration and very tight timing.
       Large amounts of data to move. One bad sensor affects everything.
   * - **Intermediate**
     - Learned features from each sensor.
     - The network decides what to combine, and can learn which sensor to
       trust in which conditions.
     - Requires training data with every sensor present. Hard to interpret
       and harder to certify. Covered in **L6**.
   * - **Late**
     - Finished per-sensor results: tracks, object lists, pose estimates.
     - Modular, with clean failure handling. Each sensor path can be built
       and tested separately, and a failed sensor drops out.
     - Information is discarded before fusion. Two sensors that each
       partially detect an object may both report nothing.

.. important::

   Your architecture is partly chosen for you. L2's data rate table showed
   eight 1080p cameras producing 1.5 GB/s, which is why RADAR ships a
   finished object list rather than raw returns. The sensor has already made
   a late fusion decision on your behalf, and you cannot reverse it.

   Early fusion is only available when you own the raw stream and can afford
   to move it.

.. note::

   **What this course uses.** GP3 combines GNSS, IMU and LiDAR pose
   estimates, which is late fusion. That choice is not based on accuracy. It
   is based on the fact that each source can be built and tested
   separately, which matters more for a semester project.

   The filters in this lecture are how late fusion is actually done. The same
   update also appears inside early fusion systems, with different inputs.


.. admonition:: Where this leads
   :class: tip

   This course uses late fusion, so the things being combined are finished
   estimates, one from each sensor.

   That reduces the whole problem to a single question, and it is the one
   the introduction opened with. **Two estimates of the same quantity
   disagree. What do you report?**

Combining Two Estimates
-----------------------

We start in one dimension, with no matrices and no filter. The rest of the
lecture generalises this one section.

The Setup
~~~~~~~~~

Your vehicle is somewhere on the road defined in
:ref:`the road frame <l3-road-frame>`. Two independent systems estimate its
position, and they disagree.

To keep the arithmetic visible, the rest of this section works with the
:math:`x` coordinate alone. The :math:`y` coordinate behaves in exactly the
same way, with its own :math:`\sigma_y`, and the matrix form in
:ref:`l3-kalman` handles both axes at once.

.. list-table::
   :widths: 34 22 22 22
   :header-rows: 1
   :class: table-striped

   * - **Source**
     - **Estimate of** :math:`x`
     - **Its** :math:`\sigma`
     - **Its variance**
   * - LiDAR map matching
     - 103.0 m
     - 1.0 m
     - 1.0
   * - GNSS
     - 100.0 m
     - 2.0 m
     - 4.0

.. admonition:: What the sigma column means
   :class: note

   :math:`\sigma` here is the **uncertainty on that one estimate**, meaning
   how far that estimate is likely to sit from the truth.

   Whenever you see a :math:`\sigma`, ask what it is the sigma **of**. The
   same sensor produces different answers depending on what you report, and
   the six GNSS readings from :ref:`l3-variance` show it directly. Those
   readings scattered with :math:`\sigma_x = 1.561` m.

   .. list-table::
      :widths: 44 20 36
      :header-rows: 1

      * - **What you report**
        - **Its value**
        - **Its uncertainty**
      * - A single reading, say the first one
        - 102.1 m
        - 1.561 m
      * - The average of all six readings
        - 100.0 m
        - :math:`1.561/\sqrt{6}` = **0.637 m**
      * - The average of a hundred readings
        - not shown
        - :math:`1.561/\sqrt{100}` = **0.156 m**

   All three rows come from the same sensor with the same noise. Only the
   third column changes, because averaging more readings gives a better
   estimate of where the car actually is.

   The rule behind the second and third rows is

   .. math::

      \frac{\sigma}{\sqrt{n}}

   so averaging four readings halves your uncertainty and averaging a
   hundred divides it by ten.

   **The table above this note is the first row of that table.** Each
   estimate in it is a single reading, so its :math:`\sigma` is the sensor's
   own noise. If the LiDAR row had been an average of nine scans instead,
   its 1.0 m would have become :math:`1.0/3 = 0.33` m.

   That rule is not a separate thing to memorise. It is what the formula in
   the next section produces when every estimate you feed it is equally
   trustworthy, and you will derive it that way shortly.

.. _l3-where-sigma-comes-from:

.. admonition:: Do you compute the uncertainty, or is it given to you?
   :class: important

   Reasonable question, and the answer is different for the two uncertainty
   numbers in this lecture.

   **The sensor's uncertainty**, which becomes :math:`R`, comes from one of
   four places.

   .. list-table::
      :widths: 30 70
      :header-rows: 1

      * - **Source**
        - **What it means in practice**
      * - The sensor reports it
        - Many GNSS receivers publish an accuracy estimate **with every
          fix**, because the receiver knows how many satellites it has and
          how they are spread across the sky. This is the best case, since
          the number rises on its own when you enter an urban canyon.
      * - You measure it
        - Exactly the procedure in :ref:`l3-variance`. Put the sensor
          somewhere you have surveyed, take many readings, compute
          :math:`\sigma`. This is part of what a calibration session is
          for.
      * - The datasheet
        - The manufacturer quotes a figure. Treat it as optimistic, since
          it was measured in favourable conditions and not on your vehicle.
      * - You set it
        - In simulation you choose the noise yourself, so you know it
          exactly.

   **In this lecture the numbers are simply given to you**, as 1.0 m and
   2.0 m in the table above. That is a teaching simplification, so the
   arithmetic stays visible. In Exercise 4 you do it properly: you set
   CARLA's ``noise_lat_stddev`` yourself, then measure the noise from the
   logged data and check whether the two agree.

   .. warning::

      **Knowing** :math:`R` **exactly is a luxury of simulation**, in the
      same way that L2's exact extrinsics were. On a real vehicle the
      number is always an estimate, it changes with conditions, and a
      value that was right in an open car park is wrong between tall
      buildings.

   **The model's uncertainty**, which becomes :math:`Q`, is a different
   story entirely. **It is never given and it cannot be measured**, because
   it describes how wrong your own motion model is. If you could measure
   that, you would fix the model instead. :math:`Q` is always tuned by hand,
   and :ref:`l3-consistency` is how you tell whether you tuned it well.

.. admonition:: Discussion 1. Which number do you report?
   :class: hint

   Decide on an answer before reading further.

   1. What value of :math:`x` do you report?
   2. What uncertainty do you attach to it?
   3. Is that uncertainty larger or smaller than 1.0 m?

   Most people answer 101.5 m. Consider what that answer assumes about the
   two sensors.

.. dropdown:: Discussion 1. Answer
   :color: success
   :icon: check-circle

   **101.5 m is wrong.** You get it by assuming the two sensors are equally
   trustworthy, and they are not. One has half the standard deviation of the
   other.

   The correct answer is **102.4 m**, which is much closer to the LiDAR
   reading. The uncertainty attached to it is :math:`\sigma = 0.894` m,
   which is smaller than either input.

   Part 3 is where most people go wrong. They expect that mixing a good
   estimate with a worse one must produce something worse than the good one.
   It does not, and the next section explains why.


.. _l3-weighting:

Weighting by Certainty
~~~~~~~~~~~~~~~~~~~~~~

Weight each estimate by how certain it is. Certainty is one divided by
variance, and it is called **precision**.

.. math::

   \hat{x} = \frac{\dfrac{x_1}{\sigma_1^2} + \dfrac{x_2}{\sigma_2^2}}
                  {\dfrac{1}{\sigma_1^2} + \dfrac{1}{\sigma_2^2}}
   \qquad\qquad
   \frac{1}{\sigma_f^2} = \frac{1}{\sigma_1^2} + \frac{1}{\sigma_2^2}

.. admonition:: In plain English
   :class: plain-english

   **The top line is a weighted average. The bottom line makes the weights
   add up to one.**

   Any weighted average looks like this: multiply each value by how much it
   counts, add those up, then divide by the total amount of counting. The
   only real decision is what to use for "how much it counts".

   The answer here is **certainty**, and certainty is one divided by
   variance. A sensor with a small variance is very certain, so
   :math:`1/\sigma^2` is large and that sensor pulls the answer toward
   itself.

   The second formula says the same thing about the result. Add up how
   certain each source is, and that is how certain you now are. Certainty
   accumulates, which is why the answer ends up sharper than either input.

The first formula is an ordinary weighted average with weights
:math:`1/\sigma_i^2`. The second formula says that **precisions add**, which
is the part worth remembering. Standard deviations do not add, and variances
do not add. Precisions do.

Using the numbers above:

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - **Quantity**
     - **Value**
   * - LiDAR weight
     - :math:`\frac{1/1}{1/1 + 1/4} = 0.8`, so 80%
   * - GNSS weight
     - :math:`\frac{1/4}{1/1 + 1/4} = 0.2`, so 20%
   * - Combined estimate
     - :math:`0.8 \times 103.0 + 0.2 \times 100.0 = \mathbf{102.4}` m
   * - Combined variance
     - :math:`(1/1 + 1/4)^{-1} = 0.8`
   * - Combined :math:`\sigma`
     - :math:`\sqrt{0.8} = \mathbf{0.894}` m

.. admonition:: The result to remember
   :class: important

   **Halving a sensor's sigma multiplies its weight by four.**

   Weight goes as :math:`1/\sigma^2`, so a sensor that is twice as good is
   not twice as important. It is four times as important.

.. figure:: /_static/images/L3/fusion_1d.png
   :alt: Three probability density curves on a position axis. A wide orange GNSS curve centred at 100 metres with sigma 2 metres, a narrower blue LiDAR curve centred at 103 metres with sigma 1 metre, and a green combined curve centred at 102.4 metres with sigma 0.894 metres that is taller and narrower than both inputs. A dotted vertical line marks the plain average at 101.5 metres, labelled as wrong.
   :align: center
   :width: 92%
   :class: white-figure

   The combined estimate sits closer to the more certain sensor, and is
   sharper than either input.

The combined curve is narrower than both inputs because two independent
measurements of the same quantity contain more information than either one
alone. If the result were not sharper, information would have been lost.

.. note::

   **This is where the** :math:`\sigma/\sqrt{n}` **rule comes from.**

   Feed the formula :math:`n` estimates that all have the same
   :math:`\sigma`. Each one contributes a precision of
   :math:`1/\sigma^2`, so the precisions add to :math:`n/\sigma^2`, and the
   combined uncertainty is

   .. math::

      \sigma_f = \sqrt{\frac{\sigma^2}{n}} = \frac{\sigma}{\sqrt{n}}

   Taking an average is just inverse-variance weighting with every source
   trusted equally. The familiar averaging rule is the special case, not a
   separate result.


The Limits
~~~~~~~~~~

Checking a formula at its extremes is a good way to confirm you understand
it.

.. list-table::
   :widths: 26 74
   :header-rows: 1
   :class: table-hover

   * - **If**
     - **Then**
   * - :math:`\sigma_2 \to \infty`
     - The second sensor's weight goes to zero and the answer is the first
       sensor, unchanged. A useless sensor is ignored rather than averaged
       in, so it does no harm.
   * - :math:`\sigma_2 \to 0`
     - The second sensor's weight goes to one and overrides everything else.
       A sensor claiming perfect certainty is believed absolutely, which is
       why setting :math:`R = 0` is never safe.
   * - :math:`\sigma_1 = \sigma_2`
     - Equal weights, and the plain average is correct. This is the only
       case where it is.


.. _l3-independence:

Why Independence Matters
~~~~~~~~~~~~~~~~~~~~~~~~

Everything above requires the two errors to be **independent**, meaning that
knowing one error tells you nothing about the other. When they are not
independent, the formula does not just give a slightly wrong answer. It
gives a wrong answer with high confidence, which is worse.

.. danger::

   Suppose both estimates come from the same slightly wrong mounting
   calibration, such as the one degree error from L2. Then both are wrong in
   the same direction by the same amount. The formula still returns a
   combined :math:`\sigma` smaller than either input, and that number is
   incorrect. Averaging two copies of the same error does not reduce it.

   This is L2's distinction between redundancy and complementarity, stated
   as mathematics. **Two identical forward cameras do not give you**
   :math:`\sigma/\sqrt{2}`. They give you :math:`\sigma` and an
   overconfident uncertainty.

The practical lesson is that the difficult part of fusion is usually not the
algebra. It is establishing whether your inputs are genuinely independent.
A shared clock, a shared calibration, a shared mounting bracket or a shared
patch of fog all break independence.


.. admonition:: Where this leads
   :class: tip

   Weighting by certainty answers the question for two estimates taken at
   the same moment.

   A vehicle needs two things that formula does not provide. The car **keeps
   moving** between measurements, so an old estimate is worth less than a
   fresh one. And there is **more than one quantity** to track, because
   position, velocity and heading all matter at once. Adding those two
   things gives the Kalman filter.

.. _l3-kalman:

The Kalman Filter
-----------------

Now add two things to the one dimensional case: time, and more than one
number. The result is the Kalman filter.

What You Are Estimating
~~~~~~~~~~~~~~~~~~~~~~~

The **state**, written :math:`\mathbf{x}`, is the list of quantities you
want to know but cannot read directly off a sensor. For a vehicle moving in
a plane:

.. math::

   \mathbf{x} = \begin{bmatrix} p_x & p_y & v_x & v_y \end{bmatrix}^\top

.. important::

   Choosing what goes in the state is a design decision, and it determines
   whether the filter can work at all.

   Velocity is included even though no sensor reports it, because the motion
   model needs it and the filter can infer it. Anything the filter must
   reason about over time belongs in the state. Anything else makes the
   filter slower and its covariance harder to keep correct.

Two models describe the world:

.. math::

   \mathbf{x}_k = F\,\mathbf{x}_{k-1} + \mathbf{w}, \qquad
   \mathbf{w} \sim \mathcal{N}(0, Q)

.. math::

   \mathbf{z}_k = H\,\mathbf{x}_k + \mathbf{v}, \qquad
   \mathbf{v} \sim \mathcal{N}(0, R)

Taking the symbols one at a time:

.. list-table::
   :widths: 14 86
   :header-rows: 1

   * - **Symbol**
     - **Meaning**
   * - :math:`F`
     - How the world changes on its own. Under constant velocity, position
       gains :math:`v\,\Delta t` and velocity is unchanged.
   * - :math:`Q`
     - How inaccurate :math:`F` is. The real world does not follow your
       model exactly, and :math:`Q` states by how much.
   * - :math:`H`
     - What the sensor observes. A GNSS receiver reports position but not
       velocity, so :math:`H` selects the position rows.
   * - :math:`R`
     - How noisy the sensor is. This is a variance in the sense of
       :ref:`l3-variance`. Where it comes from in practice is
       covered :ref:`here <l3-where-sigma-comes-from>`.

Predict, Then Update
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 16 44 40
   :header-rows: 1

   * - **Step**
     - **Equations**
     - **Effect on the covariance**
   * - **Predict**
     - :math:`\hat{\mathbf{x}}^- = F\hat{\mathbf{x}}`

       :math:`P^- = F P F^\top + Q`
     - It always grows. Time passed and no new information arrived, so the
       estimate is less certain than before.
   * - **Update**
     - :math:`\boldsymbol{\nu} = \mathbf{z} - H\hat{\mathbf{x}}^-`

       :math:`S = H P^- H^\top + R`

       :math:`K = P^- H^\top S^{-1}`

       :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^- + K\boldsymbol{\nu}`

       :math:`P = (I - KH)P^-`
     - It always shrinks, because new information arrived.

.. admonition:: In plain English
   :class: plain-english

   **Two of these lines look stranger than they are.**

   :math:`P^- = F P F^\top + Q` is two separate ideas stuck together.

   :math:`F P F^\top` is your old uncertainty, carried forward through the
   motion. When you move an uncertain quantity, its uncertainty moves too.
   :math:`F` appears **twice**, once on each side, because variance is built
   out of squared quantities. In one dimension the whole term is just
   :math:`f^2 \sigma^2`, and the two copies of :math:`F` are where that
   square comes from. The transpose is what "squaring" looks like once you
   are working with matrices.

   :math:`+\,Q` then adds new uncertainty, because the motion model is not
   perfect and time has passed.

   So the line reads: **take what you knew, move it forward, then admit you
   are now a little less sure.**

   :math:`P = (I - KH)P^-` is easier than it looks. :math:`KH` is the
   fraction of your uncertainty that the measurement just removed, so
   :math:`I - KH` is the fraction that survives, and multiplying by
   :math:`P^-` keeps that fraction. A useless sensor gives :math:`K = 0`,
   so you keep all of it. A perfect one removes all of it.

.. figure:: /_static/images/L3/covariance_1_belief.png
   :alt: A small, almost round green ellipse centred on the origin, on axes marked x and y in metres, with a dot at its centre labelled the estimate and the outline labelled the 1-sigma ellipse.
   :align: center
   :width: 88%
   :class: white-figure

   **Step 1.** The belief at the end of the previous cycle. The dot is the
   estimate. The single outline around it is the **1-sigma ellipse**, which
   is the standard way of drawing a two dimensional uncertainty.

.. warning::

   **A 1-sigma ellipse does not contain 68% of the probability.** That
   figure is the one dimensional one, quoted in :ref:`l3-variance`. Spread
   over two dimensions the same contour contains only about **39%**, and the
   2-sigma ellipse contains about **86.5%** rather than 95%.

   Every ellipse drawn in this lecture is the 1-sigma contour, so treat it
   as a rough indication of scale rather than as a region the vehicle is
   probably inside. :ref:`l3-confidence` gives the multiplier to use when
   you need a stated probability.

.. figure:: /_static/images/L3/covariance_2_predict.png
   :alt: The small ellipse from step one is now shown as a dotted grey outline at the origin. A much larger blue ellipse sits further along the x axis, tilted so its long axis points up and to the right, along the direction of travel.
   :align: center
   :width: 88%
   :class: white-figure

   **Step 2.** After predicting forward. The ellipse has moved along the
   motion model and grown, stretching most along the direction of travel,
   because that is where the model is least certain.

.. figure:: /_static/images/L3/covariance_3_update.png
   :alt: The large ellipse from step two is now a dashed grey outline. A smaller green ellipse sits inside it, shifted toward an orange cross marking the measurement.
   :align: center
   :width: 88%
   :class: white-figure

   **Step 3.** After using the measurement. The ellipse has shrunk, and its
   centre has moved toward the orange cross. It did not move all the way,
   and how far it moved is what the Kalman gain decides.

The ellipse shows the set of positions the filter currently considers
plausible, in the sense of :ref:`l3-confidence`. Prediction stretches it,
mostly along the direction of travel, because that is where the model is
least certain. The update contracts it, most strongly along whichever
direction the sensor measures.

Three of the five update lines are bookkeeping. Two matter:

- :math:`\boldsymbol{\nu}`, the **innovation**, is the measurement minus what the
  filter expected the measurement to be. It is the only new information in
  the cycle, and :ref:`l3-consistency` is about monitoring it.
- :math:`K`, the **Kalman gain**, is how much of that difference the filter
  acts on.


What the Kalman Gain Does
~~~~~~~~~~~~~~~~~~~~~~~~~

In one dimension the gain reduces to something already derived:

.. math::

   K = \frac{P}{P + R}

.. figure:: /_static/images/L3/kalman_gain.png
   :alt: A curve of Kalman gain K against the ratio of measurement noise R to prediction uncertainty P on a logarithmic x axis. K approaches 1 when R is much less than P, passes through 0.5 when R equals P, and approaches 0 when R is much greater than P. Three labelled points mark those regimes.
   :align: center
   :width: 92%
   :class: white-figure

   The gain is the fraction of the measurement difference that the filter
   acts on.

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: table-hover

   * - **Situation**
     - **Behaviour**
   * - :math:`R \ll P`
     - :math:`K \to 1`. The sensor is much better than the prediction, so
       the filter moves almost entirely to the measurement.
   * - :math:`R = P`
     - :math:`K = 0.5`. The filter splits the difference. This is the one
       case where the plain average is correct.
   * - :math:`R \gg P`
     - :math:`K \to 0`. The sensor adds nothing the filter did not already
       know more accurately, so the measurement has little effect.

.. important::

   The Kalman filter is the weighted average from
   :ref:`l3-independence` with a prediction step added in front.
   :math:`K = P/(P+R)` is the same weight computed earlier. The only new
   idea is that one of the two estimates being combined is the filter's own
   prediction.

   The matrices, transposes and :math:`S^{-1}` are that same idea carried
   into more dimensions.

.. admonition:: In plain English
   :class: plain-english

   **The matrix gain has the same shape as the scalar one.**

   Put them side by side:

   .. math::

      K = \frac{P}{P + R}
      \qquad\text{becomes}\qquad
      K = P^- H^\top S^{-1}

   :math:`S` is the matrix version of :math:`P + R`, meaning "how uncertain
   is the comparison I am about to make". Matrices cannot be divided, so
   multiplying by :math:`S^{-1}` is how you divide by it.

   :math:`H^\top` is a unit converter. :math:`P` describes uncertainty
   about **the state**, while :math:`S` describes uncertainty about **the
   measurement**, and those are not the same thing. :math:`H` translates
   state into measurement, so :math:`H^\top` translates back the other way.

   Read the whole thing as: **how unsure I am, divided by how unsure the
   comparison is, converted into the right units.**


A Worked Cycle. GNSS and IMU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L2 described this pairing as the clearest example of complementarity. Here
it is with numbers.

A vehicle drives along a straight road. The IMU drives the prediction at
10 Hz, and GNSS supplies a position fix once per second with
:math:`\sigma = 2` m. The state is :math:`[p, v]`. The filter starts with
:math:`\sigma_p = 1.0` m and :math:`\sigma_v = 0.5` m/s.

Between fixes only prediction runs, and the uncertainty grows:

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: table-striped

   * - **Time since last fix**
     - :math:`\sigma_p` **(m)**
     - :math:`\sigma_v` **(m/s)**
   * - 0.0 s
     - 1.000
     - 0.500
   * - 0.1 s
     - 1.001
     - 0.510
   * - 0.5 s
     - 1.033
     - 0.548
   * - 1.0 s
     - **1.133**
     - 0.592

When the fix arrives:

.. list-table::
   :widths: 44 56
   :header-rows: 1

   * - **Quantity**
     - **Value**
   * - :math:`P^-` for position, just before the fix
     - 1.283, so :math:`\sigma_p = 1.133` m
   * - :math:`R` for GNSS
     - 4.0, so :math:`\sigma = 2.0` m
   * - :math:`S = P^- + R`
     - 5.283
   * - :math:`K`, position row
     - :math:`1.283/5.283 = \mathbf{0.243}`
   * - :math:`\sigma_p` after the fix
     - **0.986 m**

A gain of 0.243 means the filter moves less than a quarter of the way toward
the GNSS reading. That is correct. At this moment dead reckoning is more
accurate (:math:`\sigma_p = 1.13` m) than the fix (:math:`\sigma = 2.0` m),
so the fix acts as a small correction rather than a replacement.

.. note::

   **Why a 2 m sensor still helps a 1.13 m estimate.**

   The prediction's error grows without limit, and the GNSS error does not.
   Without corrections, :math:`\sigma_p` increases at every step forever.
   That is L2's IMU drift expressed as a number. The fix does not have to be
   more accurate than the current estimate to be useful. It only has to stay
   bounded.

   Running this filter for a few minutes brings it to a steady state, with
   :math:`\sigma_p` near 1.3 m just after each fix and :math:`K` near 0.43.
   The initial value of 1.0 m was optimistic, and the filter corrects that
   over the first few cycles.

The IMU is fast but drifts. GNSS is slow but does not drift. Each one covers
the other's weakness, and the filter is what combines them into a single
estimate.


.. _l3-four-assumptions:

The Four Assumptions
~~~~~~~~~~~~~~~~~~~~

Under four conditions, the Kalman filter is provably the best possible
linear estimator. No other algorithm achieves a lower mean squared error.

.. list-table::
   :widths: 28 72
   :header-rows: 1
   :class: table-striped

   * - **Assumption**
     - **What breaks it in a real vehicle**
   * - The models are **linear**
     - Steering. A turning vehicle's motion is not a matrix multiplication,
       and range and bearing measurements are not linear in position.
   * - The noise is **Gaussian**
     - Multipath, which is a steady offset rather than noise. Association
       mistakes, which are large and sudden rather than noisy.
   * - The noise is **zero mean and white**
     - *Zero mean* means no bias, so the errors average to nothing over
       time. *White* means each error is unrelated to the one before it,
       with no drift or slow wander. Uncorrected IMU bias breaks the first,
       and a sensor whose errors persist from moment to moment breaks the
       second. Either way the filter treats repeated readings as fresh
       evidence when they are not, and trusts the sensor too much. See
       :ref:`l3-uncertainty`.
   * - :math:`Q` **and** :math:`R` **are known**
     - :math:`Q` is never known. It is tuned, which means the optimality
       proof does not apply to any filter that has actually been deployed.

.. danger::

   Optimality is a claim about the model you supplied, not about the road. A
   filter can be provably optimal with respect to assumptions that are all
   wrong, and it will report a small covariance throughout.

   :math:`R` can usually be measured by pointing the sensor at a known
   target and examining the spread, as in :ref:`l3-variance`. :math:`Q`
   cannot be measured, because it describes how wrong your model of the
   world is, and if you knew that you would have used a better model.
   **:math:`Q` is the parameter you are most likely to get wrong, and
   getting it wrong is what makes a filter overconfident.**


.. admonition:: Where this leads
   :class: tip

   The Kalman filter is the best estimator available, but only while its
   four assumptions hold.

   Three of them fail on a real vehicle. The next section takes those three
   failures one at a time and gives the standard repair for each.

When the Assumptions Break
--------------------------

Three of the four assumptions fail on a real vehicle. Each failure has a
standard solution.

Nonlinear Models. The EKF
~~~~~~~~~~~~~~~~~~~~~~~~~

A vehicle that steers does not obey
:math:`\mathbf{x}_k = F\mathbf{x}_{k-1}`. Replace the matrices with
functions:

.. math::

   \mathbf{x}_k = f(\mathbf{x}_{k-1}, \mathbf{u}) + \mathbf{w}, \qquad
   \mathbf{z}_k = h(\mathbf{x}_k) + \mathbf{v}

The **Extended Kalman Filter** keeps every Kalman equation unchanged and
approximates :math:`f` and :math:`h` with straight lines near the current
estimate, using their Jacobians:

.. math::

   F \approx \left.\frac{\partial f}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}}
   \qquad
   H \approx \left.\frac{\partial h}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}}

Everything else is unchanged. The EKF is the standard choice for vehicle
state estimation and is what GP3 uses.

.. danger::

   **The EKF's failure mode is a feedback loop.**

   The Jacobian is worked out at the current estimate. If that estimate is
   already off, the straight-line approximation gets built in the wrong
   place. The correction it produces is then wrong, so the next estimate is
   worse than this one. And the next Jacobian is worked out at that worse
   estimate. Each turn of the loop makes the following turn worse.

   Meanwhile :math:`P` continues to shrink, because the update equation
   shrinks it regardless of whether the update was correct. The filter
   becomes more confident as it becomes less accurate. This is divergence,
   covered in :ref:`l3-consistency`.

Avoiding Jacobians. The UKF
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **Unscented Kalman Filter** takes a different approach. Instead of
approximating the function, it samples the distribution.

1. Choose :math:`2n+1` **sigma points** that reproduce the current mean and
   covariance exactly.
2. Pass each one through the true nonlinear function. No derivatives are
   required.
3. Compute a new mean and covariance from the transformed points.

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: table-hover

   * - **Property**
     - **Why it matters**
   * - No Jacobians
     - Works when :math:`f` is complicated, comes from a lookup table, or
       has no clean derivative. It also eliminates a class of bugs. A
       Jacobian derived by hand with one sign wrong produces a filter that
       runs, converges, and gives wrong answers.
   * - Higher accuracy
     - Better than the EKF when the function curves significantly across the
       width of the uncertainty.
   * - Comparable cost
     - :math:`2n+1` function evaluations per step. For small states this is
       similar to the EKF, and sometimes cheaper once the cost of computing
       the Jacobian is included.

.. note::

   If the uncertainty is small compared with how much the function curves,
   the function is nearly straight across the region that matters and the
   EKF is adequate. The UKF is worth using when the covariance is wide, such
   as at start up, after a long GNSS outage, or during a hard turn.

Non-Gaussian Belief. The Particle Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Up to here, everything the filter knows about where the car is has been one
mean and one covariance. That package is called the filter's **belief**: the
range of states it currently considers possible, and how likely each is.

The EKF and UKF both assume that belief has a single peak. Sometimes it does
not.

Consider a vehicle that has just lost GNSS in a car park, whose LiDAR scan
matches three different aisles equally well. The correct belief has three
peaks. A single peak cannot represent that, and a filter forced to try
places its centre between them, at a location the vehicle is definitely not.

A **particle filter** represents the belief as a set of weighted samples.
Prediction moves every particle through the motion model, each particle is
scored by how well it explains the measurement, and then the set is
resampled.

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - **Use it when**
     - The belief has several separate peaks: global localization, the
       kidnapped robot problem, or ambiguous map matching.
   * - **Avoid it when**
     - The state has many dimensions. The number of particles required grows
       very quickly with dimension, and a filter with too few particles
       collapses onto one peak and stops representing the others.

.. note::

   The deciding question is the shape of the belief, not how nonlinear the
   model is. A strongly nonlinear system with one peak is a UKF problem. A
   mildly nonlinear system with three plausible answers is a particle filter
   problem.

   Monte Carlo Localization, which applies the particle filter to a real
   map, is :doc:`L7 <../lecture7/l7_index>`.

Choosing a Filter
~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 12 22 22 22 22
   :header-rows: 1
   :class: table-striped

   * - **Filter**
     - **Model**
     - **Belief**
     - **Cost**
     - **Use it when**
   * - **KF**
     - Linear
     - Single peak
     - Lowest
     - The model really is linear. Uncommon, but exact when true.
   * - **EKF**
     - Nonlinear, differentiable
     - Single peak
     - Low
     - The default for vehicle state estimation. **GP3 uses this.**
   * - **UKF**
     - Nonlinear, any form
     - Single peak
     - Low to moderate
     - Strong curvature, wide covariance, or no clean Jacobian.
   * - **PF**
     - Any
     - Any
     - High
     - The belief has several peaks and the state is small.


.. admonition:: Where this leads
   :class: tip

   You now have four filters, and each one returns an estimate together
   with a covariance saying how confident it is.

   **Not one of them checks whether that confidence is deserved.** They all
   shrink their covariance on every update, whether or not the update was
   any good. So the next section is Question 2 from the introduction: how do
   you tell an honest covariance from a fictional one?

.. _l3-consistency:

Checking That the Filter Is Consistent
--------------------------------------

Every filter above returns an estimate and a covariance. Students usually
use the first and ignore the second. The covariance is the more important
output, because it is the filter's claim about its own accuracy, and that
claim can be tested.

.. important::

   Testing it does not require ground truth. The test uses only quantities
   the filter already computes, so it can run on the vehicle continuously.

The Innovation
~~~~~~~~~~~~~~

.. math::

   \boldsymbol{\nu} = \mathbf{z} - H\hat{\mathbf{x}}^-, \qquad
   S = H P^- H^\top + R

The innovation is the measurement minus the prediction of that measurement.
If the filter's model of the world is correct, :math:`\boldsymbol{\nu}` should
average to zero and have covariance :math:`S`. The filter computes :math:`S`
itself, which means it has already predicted how large its own measurement
differences ought to be. You can check whether they come out that size.

Normalised Innovation Squared
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \varepsilon = \boldsymbol{\nu}^\top S^{-1} \boldsymbol{\nu}

.. admonition:: In plain English
   :class: plain-english

   **This is surprise, measured in units of expected surprise.**

   :math:`\boldsymbol{\nu}` is how surprised the filter actually was.
   :math:`S` is how surprised it predicted it would be. Dividing the first
   by the second, which for matrices means multiplying by :math:`S^{-1}`,
   gives a number with no units at all.

   That is the whole trick. A raw innovation of 3 m means nothing on its
   own, because it is excellent for a sensor expecting 10 m of disagreement
   and alarming for one expecting 0.1 m. Dividing by what you expected makes
   the number comparable **across sensors and across time**.

   :math:`\boldsymbol{\nu}` appears twice for the same reason :math:`F`
   did earlier: it squares the surprise, so that being wrong in either
   direction counts the same.

   A value near 1 for each quantity measured means the surprises are coming
   out about the size the filter predicted, which is exactly what you want.

If the filter is consistent, :math:`\varepsilon` follows a chi-square
distribution with :math:`m` **degrees of freedom**, where :math:`m` is
simply how many numbers the sensor reports at once. A GNSS fix giving
:math:`x` and :math:`y` has :math:`m = 2`. The chi-square distribution
describes how big a sum of :math:`m` squared, normalised errors should be,
so the tables below say what counts as a normal amount of surprise.

.. list-table::
   :widths: 16 42 42
   :header-rows: 1
   :class: table-striped

   * - :math:`m`
     - **95% range for a single sample**
     - **99% gate threshold**
   * - 1
     - 0.001 to 5.024
     - 6.635
   * - 2
     - 0.051 to 7.378
     - 9.210
   * - 3
     - 0.216 to 9.348
     - 11.345

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: table-hover

   * - **Observation**
     - **Interpretation**
   * - :math:`\varepsilon` repeatedly above the range
     - The filter is **overconfident**. Its measurement differences are
       larger than it predicted, so :math:`P` or :math:`R` is too small,
       usually :math:`Q`. This is the dangerous case.
   * - :math:`\varepsilon` repeatedly below the range
     - The filter is **underconfident**. It is discarding useful information
       and converging slowly. Inefficient, but safe.
   * - :math:`\varepsilon` inside the range
     - The covariance is accurate. This is the only case in which the
       reported uncertainty means anything.

.. tip::

   Log the NIS from the first day you write a filter. It costs one line of
   code. Without it you notice that an estimate looks slightly off. With it
   you know the filter has been overconfident by a factor of four since
   Tuesday.

Divergence
~~~~~~~~~~

.. danger::

   The update equation shrinks :math:`P` whether or not the update was
   correct. A filter receiving bad data, or one that built its
   approximation in the wrong place, therefore does the following:

   1. :math:`P` shrinks, because that is what the update step does.
   2. A small :math:`P` produces a small :math:`K`.
   3. A small :math:`K` means new measurements barely change the estimate.
   4. The filter effectively ignores its inputs. The true error grows
      without limit while the reported covariance keeps shrinking.

   The output is a precise, confident, incorrect position. No alarm is
   raised, and nothing downstream can detect the problem.

Gating
~~~~~~

L2 left the multipath problem open: a GNSS fix in a street of tall buildings
that arrives on time, looks normal, and is several metres wrong. Gating is
the answer.

Test the measurement before using it. Compute :math:`\varepsilon` for the
incoming measurement and discard it if the value is too large:

.. math::

   \boldsymbol{\nu}^\top S^{-1}\boldsymbol{\nu} > \chi^2_{m,\,0.99}
   \quad\Rightarrow\quad \text{discard}

For a two dimensional position fix that threshold is **9.21**. A multipath
fix that is 5 m off, when the filter expected about 1 m of disagreement,
produces a large :math:`\varepsilon` and is discarded. The filter runs on
prediction alone for that cycle. Skipping one update is better than
accepting a bad measurement.

.. warning::

   **Gating has its own failure mode, and it matches L2's zero-Doppler
   filter.**

   A gate rejects anything that disagrees with the current estimate. If the
   estimate is already wrong, the correct measurements are the ones that
   disagree, so the gate rejects them and preserves the error.

   The pattern is the same one L2 described: a system discards inconvenient
   returns to avoid nuisance behaviour and becomes blind to the case that
   matters. The fix is also the same. Count how many measurements are
   rejected consecutively, and once the count is too high, declare the
   filter unhealthy rather than continuing to trust it.

.. admonition:: Discussion 2. It reports 0.2 m and it is 3 m wrong
   :class: hint

   Your EKF reports a position with :math:`\sigma = 0.2` m. Ground truth
   shows the estimate is 3 m off. No fault has been raised.

   1. Name three different mechanisms that could produce this.
   2. Which single logged quantity would distinguish between them?
   3. What should the vehicle do, and who decides?

.. dropdown:: Discussion 2. Answer
   :color: success
   :icon: check-circle

   **Three possible mechanisms.**

   - :math:`Q` **is too small.** The filter treats its motion model as more
     accurate than it is, so :math:`P` collapses, :math:`K` approaches zero,
     and new measurements stop affecting the estimate. This is the most
     common cause and the easiest to create accidentally while tuning for a
     smooth output.
   - **Inputs that are not independent are being treated as independent.**
     Two sources share a bias, as in :ref:`l3-independence`, so the filter
     counts the same evidence twice.
   - **An association error.** The filter is tracking accurately, but it is
     tracking the wrong object. The covariance is correct for a question you
     did not intend to ask. See :ref:`l3-data-association`.

   A fourth mechanism is specific to the EKF: the approximation was built at
   the wrong point, which is a variation on the first.

   **Question 2. Log the NIS.** All three push :math:`\varepsilon` above its
   range, so NIS detects the condition. Distinguishing the causes takes a
   little more: a steadily high NIS with a smooth path suggests :math:`Q`, a
   NIS that jumps when tracks change over suggests association, and a NIS
   that is fine until one input degrades suggests correlation.

   **Question 3. The filter does not decide.** A filter that detects its own
   inconsistency should report it rather than retune itself. Increasing
   :math:`Q` at run time until the NIS looks acceptable hides the fault and
   converts a detectable problem into an undetectable one.

   This is L2's escalation rule applied to software. A vehicle that has lost
   confidence in its own position estimate should slow down or stop rather
   than continue on numbers it cannot justify.


.. admonition:: Where this leads
   :class: tip

   The consistency check tells you whether a filter is tracking its object
   accurately.

   Every word of that assumed the measurements arriving actually belong to
   the object being tracked. With more than one object in the scene that has
   to be earned rather than assumed, **and it is where the Tempe crash
   happened.**

.. _l3-data-association:

Data Association
----------------

Everything so far assumed you already knew which measurement belonged to
which track. In any scene with more than one object, that assumption has to
be earned. It is also where the Tempe crash went wrong.

The Problem
~~~~~~~~~~~

You are maintaining :math:`N` tracks. A new frame delivers :math:`M`
detections. Before any filter can update anything, something must decide:

- which detection belongs to which track,
- which detections are new objects that need a track of their own,
- which detections are clutter and should be discarded,
- which tracks received nothing this frame, and whether they still exist.

.. important::

   Association is a discrete decision inside a continuous estimator, and
   that is what makes it dangerous.

   A filter degrades gradually when its measurements are noisy. It does not
   degrade gradually when its measurements belong to a different object.
   Instead it converges accurately onto a trajectory that never happened.

Measuring Distance Correctly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Straight line distance is the wrong measure. Use **Mahalanobis distance**,
which is the same quantity as the NIS:

.. math::

   d^2 = (\mathbf{z} - H\hat{\mathbf{x}}^-)^\top S^{-1}
         (\mathbf{z} - H\hat{\mathbf{x}}^-)

This measures disagreement in units of expected disagreement. A detection
2 m away from a track the filter has located to within 0.1 m is a poor
match. The same 2 m from a new track with 3 m of uncertainty is a good one.
Straight line distance reports 2 m in both cases and cannot separate them.

The Four Methods
~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 12 40 48
   :header-rows: 1
   :class: table-striped

   * - **Method**
     - **How it works**
     - **Trade-off**
   * - **NN**
     - Each track takes its nearest detection that passes the gate.
     - Simple and fast, but the answer depends on the order in which tracks
       are processed. An early track can take a detection that belonged to a
       later one, and two objects that cross can exchange identities
       permanently.
   * - **GNN**
     - Solves the whole frame at once, finding the set of pairings with the
       lowest total cost, using the Hungarian algorithm.
     - Removes the ordering problem for the cost of one small optimisation
       per frame. This is the right default.
   * - **JPDA**
     - Does not commit. Updates each track with a probability weighted blend
       of all the detections that could plausibly belong to it.
     - Effective in heavy clutter, but cannot easily start new tracks and
       blends genuinely different objects together.
   * - **MHT**
     - Maintains several competing interpretations across frames and lets
       later evidence resolve earlier ambiguity.
     - The most capable and the most expensive. Old hypotheses have to be
       discarded steadily, or the list of them grows without limit.
       Used where an identity swap would be very costly.

.. note::

   Apply the :math:`\chi^2` gate before any of these. It reduces the
   candidate set substantially and removes most clutter at no cost. Every
   method above runs faster and more accurately with a gate in front of it.

The Track Lifecycle
~~~~~~~~~~~~~~~~~~~

A track is not created the moment something is detected, and not deleted the
moment a detection is missed. Both would cause problems.

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: table-hover

   * - **State**
     - **What it means, and the rule for leaving it**
   * - **Tentative**
     - A detection matched no existing track, so a provisional track is
       created. Nothing downstream is told about it yet.
   * - **Confirmed**
     - It passed an **M of N** test, for example 3 detections in 5 frames.
       It now counts as a real object and the planner is informed.
   * - **Coasting**
     - Detections have stopped, but the track is retained and predicted
       forward. This covers occlusion. A pedestrian who walked behind a van
       still exists.
   * - **Deleted**
     - It coasted too long without support and is removed.

.. danger::

   **Tempe.**

   Return to :ref:`l3-tempe-reminder`. She was in the sensor data for more
   than five seconds, but the classification kept changing, and the system
   treated a change of classification as a change of object. Each change
   deleted the track and created a new tentative one.

   A track that is repeatedly recreated is never confirmed, so it never
   accumulates history. Without history there is no velocity estimate.
   Without a velocity estimate there is no time to collision, and without a
   time to collision nothing triggers braking. The filter itself worked
   correctly throughout, on a track that was one frame old.

   The fix is architectural rather than algorithmic: **track identity must
   not depend on classification.** Track the object, and classify it
   separately.

.. admonition:: Discussion 3. Two tracks, three detections
   :class: hint

   Two vehicles are being tracked side by side and are about to cross. This
   frame delivers three detections: one close to each track, and a third
   between them.

   1. Run NN by hand, taking track A first, then again taking track B first.
      Do you get the same answer?
   2. What does GNN do differently, and why does that matter here?
   3. The third detection matches nothing well. Name two things it could be,
      and say how the track lifecycle distinguishes them.
   4. If the tracker exchanges the identities of the two vehicles, what does
      the planner believe, and why is that worse than losing both tracks?

.. dropdown:: Discussion 3. Answer
   :color: success
   :icon: check-circle

   **1. The order changes the answer, which is the objection to NN.**
   Whichever track is processed first takes the ambiguous middle detection,
   leaving the other with a worse match or none. Two runs of the same code
   on the same data produce different results depending on the order of the
   track list, which also makes the resulting bug hard to reproduce.

   **2. GNN optimises the frame rather than the track.** It finds the lowest
   total cost across both tracks at once, so it will accept a slightly worse
   match for A if that allows B a much better one. The result does not
   depend on ordering. When two objects cross, this is often the difference
   between preserving identities and exchanging them.

   **3. The third detection is either a new object or clutter.** The
   lifecycle separates them over several frames rather than in this one. It
   becomes a tentative track, and the M of N test decides. A real object
   continues to produce detections and is confirmed. Clutter does not and is
   deleted. The system does not have to be correct immediately, only within
   a few frames.

   **4. An identity exchange is worse than a loss.** If both tracks are
   lost, the system knows it. The objects return to tentative, the planner
   is told nothing is confirmed, and a well designed stack becomes cautious.
   If the identities are exchanged, every track stays confirmed and
   confident, but each one carries the other's history, so the filter
   reports two vehicles moving in directions neither is travelling.

   The planner then avoids collisions that will not occur and ignores one
   that will. The general rule applies here as elsewhere in this course: a
   failure that reports confidence is worse than a failure that reports
   nothing.


.. admonition:: Where this leads
   :class: tip

   That completes the chain from the introduction. You can combine
   estimates, carry them forward through time, handle models that are not
   linear, check whether the result is honest, and decide which measurement
   belongs to which object.

   What is left is to build one and watch it behave.

CARLA Hands-On
--------------

This lecture's filter, on the simulator you set up in L2.

.. list-table::
   :widths: 6 36 58
   :header-rows: 1
   :class: table-hover

   * -
     - **Task**
     - **What it demonstrates**
   * - 1
     - Log CARLA's GNSS and IMU alongside the ground truth pose.
     - What the noise actually looks like, and that CARLA's GNSS reports
       latitude and longitude, so you must convert to local metres first.
   * - 2
     - Implement the predict and update cycle from this lecture.
     - That the filter itself is about twenty lines of code, and that the
       difficulty is in choosing :math:`Q`.
   * - 3
     - Log the NIS at every step and plot it against its range.
     - Whether your covariance is accurate. This is the task that matters.

.. important::

   CARLA provides ground truth, which a real vehicle does not have. Use it
   to compute the error the filter is actually making, and compare that
   against the uncertainty the filter reports. A filter whose reported
   :math:`\sigma` and true error differ by a factor of three is
   overconfident, and simulation is the only place you can establish that
   directly.

.. warning::

   **About weather, and a correction to earlier versions of this material.**

   Running this under CARLA's rain and fog presets does not produce a valid
   degraded weather result. L2 measured it: LiDAR returns hold near 11,500
   per sweep across all six presets, because CARLA's ray casting does not
   model attenuation.

   Increasing :math:`R` by hand to represent a degraded sensor is a
   reasonable exercise, and it demonstrates the gain shifting trust between
   sensors. But state clearly in the write up that you introduced the
   degradation as a constant, and that the simulator did not produce it.


Next Class
----------

**L4: Perception I. Object Detection, from YOLO to DETR**

- CNN fundamentals and the YOLO family.
- DETR, and detection treated as set prediction.
- The costs of convolutional and transformer detectors.
- Running a detector as a ROS 2 node.

**Before next class**

- Complete the L3 exercises. Exercise 5, the divergence hunt, is the most
  important one, and it is the debugging skill GP3 assumes you have.
- GP1 is posted. It builds on L2's calibration work rather than on this
  lecture's filter.

L1 provided the vocabulary and the failure cases. L2 provided the sensors
and the geometry connecting them. L3 provided the filter that combines them
and the test that shows whether to trust it. L4 provides the detector that
produces the measurements this filter has been assuming.

.. admonition:: Summary
   :class: important

   Report the covariance, and then test it. An uncertainty you have not
   checked is not useful information.
