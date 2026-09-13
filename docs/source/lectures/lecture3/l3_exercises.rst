====================================================
Exercises
====================================================

Six take-home exercises built on the Lecture 3 notes. Exercises 1 to 3 are
paper and arithmetic. Exercises 4 and 5 need CARLA running. Exercise 6 is an
analysis argument.

.. important::

   **Exercise 5 is the one that matters.** It is the debugging skill GP3
   assumes you already have, and it is the only exercise here that teaches
   you to detect a filter whose reported uncertainty is wrong, rather than
   one that fails visibly. Set aside real time for it.

.. note::

   Exercises 1 to 3 can be done with a calculator, but you will learn more
   by writing ten lines of NumPy and checking your arithmetic against it.
   Show both if you do.


.. dropdown:: Exercise 1. Variance, and Weighting by Certainty
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compute a variance from raw readings, then convince yourself that
   inverse-variance weighting follows directly from the uncertainties you
   were given.

   .. raw:: html

      <hr>

   **Part A. Where the numbers come from**

   A car is parked on a straight road, with a survey marker at the
   roadside. Distance along the road from that marker is the coordinate
   :math:`x`, as defined in the lecture. The car has been surveyed at
   exactly :math:`x = 50.0` m. A GNSS receiver reports these five estimates
   of :math:`x`, in metres:

   .. code-block:: text

      51.2   48.7   50.4   49.1   50.6

   1. Compute the **mean** of the five readings.
   2. Compute the **variance**, using the definition from the notes: find
      how far each reading sits from the mean, square those distances, and
      average the squares.
   3. Compute the **standard deviation**, and state its units.
   4. The true coordinate is 50.0 m and your mean is not 50.0 m. Is that
      difference **noise** or **bias**? Explain how five readings are not
      really enough to tell, and say what you would do to find out.

   .. raw:: html

      <hr>

   **Part B. Combining three sources**

   Three independent systems estimate the same coordinate :math:`x` on a
   straight road, measured from the same marker:

   .. list-table::
      :widths: 40 30 30
      :header-rows: 1

      * - **Source**
        - **Estimate of** :math:`x` **(m)**
        - :math:`\sigma` **(m)**
      * - LiDAR map matching
        - 100.0
        - 0.5
      * - Wheel odometry
        - 101.0
        - 1.5
      * - GNSS
        - 106.0
        - 3.0

   5. Compute each source's **precision**, then the **weights**, then the
      **combined estimate** and the **combined** :math:`\sigma`. Show that
      the weights add up to one.
   6. Compare your combined estimate against the plain average of the three.
      Which source moved the answer least, and how many times smaller is its
      influence than the LiDAR's?
   7. The GNSS reading is 6 m away from the LiDAR's. Did the formula treat
      it as an outlier? Explain what the formula actually did with it, and
      why that is **not** the same thing as rejecting it.
   8. Now suppose the wheel odometry estimate is actually derived from the
      same LiDAR scan match as row one, so their errors rise and fall
      together. Without redoing any arithmetic, say whether your combined
      :math:`\sigma` is now too small, too large, or unchanged, and explain
      why that matters more than the error in the estimate itself.

   .. raw:: html

      <hr>

   **Deliverable**

   Your working for Part A, a short table of precisions and weights for
   Part B, and three or four sentences each on questions 4, 7 and 8.

   .. dropdown:: Guidance
      :color: success

      Part A: the mean is 50.0 m. The squared distances are 1.44, 1.69,
      0.16, 0.81 and 0.36, adding to 4.46. Dividing by 5 gives a variance of
      0.892 m squared, so :math:`\sigma` is about 0.944 m. Note the units
      carefully. Variance is in metres squared, which is why we quote
      :math:`\sigma` instead.

      **If you used NumPy you may have got 1.115 instead.** Dividing by
      :math:`n` gives the variance of the numbers you actually have.
      Dividing by :math:`n-1` estimates the variance of the larger
      population those numbers came from, and that is what
      ``numpy.var(x, ddof=1)`` and most calculators do by default. The
      lecture definition divides by :math:`n`, so use ``ddof=0``. With five
      readings the two answers differ by 25%. With five hundred they differ
      by 0.2%, which is why nobody argues about it in practice. Just say
      which one you used.

      Question 4: with only five readings you cannot separate the two. A
      mean that happens to land on 50.0 m does not prove there is no bias,
      and a mean that misses by 0.3 m does not prove there is one. To find
      out, take hundreds of readings and check whether the mean **settles**
      on the truth or settles somewhere else. Noise averages away. Bias does
      not.

      Question 5: precisions are 4.000, 0.444 and 0.111, adding to 4.556.
      Weights are 0.878, 0.098 and 0.024. The combined estimate is
      **100.24 m** with :math:`\sigma` of **0.469 m**. Notice it is smaller
      than the best input.

      Question 6: the plain average is 102.33 m, nearly two metres away,
      dragged there by the worst sensor. The GNSS influence is **36 times**
      smaller than the LiDAR's, which is the square of the 6 to 1 ratio of
      their sigmas.

      Question 7: the formula rejected nothing. It gave the GNSS a weight of
      2.4%, which happens to produce a similar outcome for this one sample
      but is a completely different mechanism. A real outlier test is
      :math:`\chi^2` gating. A sensor that is **biased** rather than
      **noisy** will still poison a weighted average no matter how small its
      weight. Weighting handles noise. Gating handles outliers.

      Question 8: **too small, and dangerously so.** The formula assumes the
      errors are independent, so it counts the same evidence twice and
      reports a confidence it has not earned. The estimate barely moves. The
      confidence is what breaks. A wrong number that admits it is uncertain
      can be handled downstream. A wrong number claiming precision cannot.


.. dropdown:: Exercise 2. One Kalman Cycle, By Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run the five update equations once, with numbers small enough that you
   can see what each one did.

   .. raw:: html

      <hr>

   **Specification**

   A vehicle moves along one axis. The state is :math:`[p, v]` and the
   timestep is :math:`\Delta t = 1` s.

   .. math::

      F = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}, \quad
      Q = \begin{bmatrix} 0.25 & 0 \\ 0 & 0.25 \end{bmatrix}, \quad
      H = \begin{bmatrix} 1 & 0 \end{bmatrix}, \quad R = 4

   The filter starts believing :math:`\hat{\mathbf{x}} = [0,\ 10]^\top` with
   :math:`P = \mathrm{diag}(4,\ 1)`. A position measurement arrives:
   :math:`z = 12.0`.

   1. **Predict.** Compute :math:`\hat{\mathbf{x}}^-` and :math:`P^-`.
      Report :math:`\sigma_p` before and after the prediction and confirm
      that it grew.
   2. :math:`P^-` **has non-zero off-diagonal entries and** :math:`P`
      **did not.** Where did that come from, and what does it mean
      physically?
   3. **Update.** Compute :math:`\boldsymbol{\nu}`, :math:`S`, :math:`K`,
      :math:`\hat{\mathbf{x}}` and :math:`P`.
   4. The measurement said 12.0 and you predicted 10.0. Your updated
      position is **not** 12.0. Use :math:`K` to explain why not, and say
      what value of :math:`R` would have put it exactly at 12.0.
   5. **Velocity was never measured, yet it changed.** Explain how in one
      sentence, and name the matrix entry responsible.
   6. Compute the **NIS** for this update and compare it against the 95%
      range for :math:`m = 1`, which is 0.001 to 5.024. Is this filter
      consistent on this sample?

   .. raw:: html

      <hr>

   **Deliverable**

   All the intermediate matrices, and a sentence each for questions 2, 4, 5
   and 6.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`\hat{\mathbf{x}}^- = [10,\ 10]^\top` and
      :math:`P^- = \begin{bmatrix} 5.25 & 1 \\ 1 & 1.25\end{bmatrix}`.
      :math:`\sigma_p` grows from 2.000 to **2.291**.

      Question 2: it comes from :math:`FPF^\top`. Position was advanced
      **using** velocity, so an error in velocity is now also an error in
      position. They are no longer independent. In plain terms: if you are
      going faster than you think, then you are also further ahead than you
      think.

      Question 3: :math:`\nu = 2.0`, :math:`S = 9.25`,
      :math:`K = [0.568,\ 0.108]^\top`,
      :math:`\hat{\mathbf{x}} = [11.135,\ 10.216]^\top` and
      :math:`P = \begin{bmatrix} 2.270 & 0.432 \\ 0.432 & 1.142\end{bmatrix}`.
      :math:`\sigma_p` falls to **1.507**.

      Question 4: :math:`K = 0.568`, so you travel 56.8% of the way from 10
      to 12 and land at 11.135. Getting to exactly 12.0 needs
      :math:`K = 1`, which needs :math:`R = 0`, meaning a sensor that claims
      zero noise. That should feel wrong, and it is. It throws the prior
      away completely and turns the filter into a passthrough.

      Question 5: through the off-diagonal entry of :math:`P^-` you found in
      question 2. Because position and velocity are linked, a surprise in
      position is evidence about velocity. The entry responsible is
      :math:`P^-_{12} = 1`, which produces :math:`K_v = 1/9.25 = 0.108`.
      **This is the entire reason velocity is in the state.**

      Question 6: NIS :math:`= \nu^2/S = 4/9.25 = 0.432`, comfortably inside
      the range. Consistent on this sample, although one sample proves very
      little, which is what Exercise 5 is about.


.. dropdown:: Exercise 3. Pick the Filter
   :icon: law
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Choose between KF, EKF, UKF and PF using the property that actually
   decides it, rather than using how nonlinear the problem sounds.

   .. raw:: html

      <hr>

   **Specification**

   For each scene, name the filter, give the **one property** that decides
   it, and say what you would lose by choosing the next option up in cost.

   .. list-table::
      :widths: 6 94
      :header-rows: 1

      * -
        - **Scene**
      * - A
        - Tracking a vehicle ahead on a motorway using RADAR range and range
          rate. It stays in its lane, and your uncertainty is a few tens of
          centimetres.
      * - B
        - Estimating your own pose from GNSS, IMU and wheel odometry while
          driving round a roundabout.
      * - C
        - You have just switched on in a multi-storey car park with no GNSS.
          The LiDAR scan matches four different floors equally well.
      * - D
        - Combining a camera bearing measurement with LiDAR range, where the
          measurement function involves a projection and your team cannot
          agree on the sign of one Jacobian term.
      * - E
        - Tracking sixty objects at 20 Hz on an embedded computer with a
          fixed compute budget.

   .. raw:: html

      <hr>

   **Deliverable**

   A five-row table: scene, filter, deciding property, and the cost of going
   one step further.

   .. dropdown:: Guidance
      :color: success

      **A. KF, or an EKF you barely notice.** Nearly straight over a narrow
      uncertainty. The deciding property is that the covariance is small
      compared with how much the model curves.

      **B. EKF.** Nonlinear, but it has clean derivatives, and the belief
      has a single peak. This is the default for vehicle pose and what GP3
      uses. A UKF would work and would buy you very little here.

      **C. Particle filter.** The deciding property is that the belief has
      **four separate peaks**, not that the model is nonlinear. Four
      plausible answers cannot be one blob, and an EKF would place its
      centre somewhere the car definitely is not. This is Monte Carlo
      Localization, and it is L7.

      **D. UKF.** The deciding property here is not accuracy. It is that
      **no Jacobian is needed at all.** A hand-derived Jacobian with a sign
      error is a silent and expensive bug, and the UKF removes the
      opportunity to make it.

      **E. KF or EKF, and the real answer is that the filter is not your
      problem.** Sixty objects at 20 Hz makes **data association** both the
      bottleneck and the risk. Spend the budget on gating and GNN, not on a
      fancier filter for each track.


.. dropdown:: Exercise 4. GNSS and IMU in CARLA
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Get real noisy data out of the simulator, and see what your filter is
   actually being asked to cope with.

   .. raw:: html

      <hr>

   **Setup**

   A CARLA server running in synchronous mode, as in L2.

   .. raw:: html

      <hr>

   **Specification**

   1. Spawn an ego vehicle with a **GNSS** and an **IMU** sensor, put it in
      autopilot, and log for 60 seconds: the GNSS output, the IMU output,
      and the **ground truth** transform from ``vehicle.get_transform()``.
   2. **CARLA's GNSS reports latitude, longitude and altitude, not metres.**
      Convert to a local flat frame before you do anything else. State the
      conversion you used and what it assumes.
   3. Measure the GNSS noise for yourself. Subtract the ground truth and
      report the mean and the standard deviation of the error on each axis.
      Compare against the ``noise_lat_stddev`` and ``noise_lon_stddev``
      values you set on the blueprint.
   4. Do the same for the IMU accelerometer. Report the **mean** separately
      from the **standard deviation**, and say which of the two a Kalman
      filter handles gracefully and which it does not.
   5. Integrate the IMU acceleration twice, with no GNSS at all, and plot
      the position error against time for 60 s. Fit the growth. Does it
      match the :math:`t^2` behaviour L2 predicted?

   .. raw:: html

      <hr>

   **Deliverable**

   Your logging script, the two noise tables, and the dead reckoning error
   plot with a sentence about its shape.

   .. dropdown:: Guidance
      :color: success

      Question 2 is where most of your time will go, and that is
      deliberate. This is L3's version of L2's axis trap. Nothing raises an
      error, the numbers look plausible, and your filter quietly estimates
      position in a unit that is not metres. Check your work by driving in a
      straight line and confirming that a 10 m ground truth displacement
      really does come out as 10 m after conversion.

      Question 4: **standard deviation is noise, and the filter handles it
      through** :math:`R`. A mean that is not zero is **bias**, and the
      filter does **not** handle it. Bias breaks the zero-mean assumption,
      and the filter will happily integrate it forever. You either put it in
      the state and estimate it, or you calibrate it out beforehand.

      Question 5: expect growth close to quadratic, because a constant
      acceleration error gets integrated twice into
      :math:`\tfrac{1}{2}at^2`. Noise on its own grows more slowly. If your
      curve looks close to quadratic, you are looking at bias, which is
      question 4 arriving in a different form.


.. dropdown:: Exercise 5. The Divergence Hunt
   :icon: alert
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   **Goal**

   Detect a filter whose reported uncertainty is wrong. **This is the core
   exercise of L3.**

   .. raw:: html

      <hr>

   **Specification**

   Implement the one dimensional constant velocity filter from the lecture,
   and use it to track a CARLA vehicle that **accelerates**. Your motion
   model is therefore deliberately wrong, exactly as every motion model
   always is.

   Use :math:`\Delta t = 0.1` s, one position measurement per step with
   :math:`\sigma = 1.0` m, and run for 30 seconds.

   1. Run it with a **very small** process noise, :math:`q = 10^{-6}`. At
      the end, record three numbers: the :math:`\sigma_p` the filter
      reports, the **actual** absolute error against ground truth, and the
      mean NIS over the last 100 steps.
   2. Run it again with :math:`q = 1.0` and record the same three numbers.
   3. Plot both runs on the same axes, showing the reported
      :math:`\pm\sigma_p` as a band and the true error as a line. Describe
      what the first run's plot shows that its three final numbers do not.
   4. Plot NIS against step for both runs, with the 95% range for
      :math:`m=1` drawn on. At roughly which step does the bad run leave the
      range? Compare that against the step where the **position error**
      first becomes obviously unacceptable.
   5. Add :math:`\chi^2` **gating** at the 99% threshold, which is 6.635 for
      :math:`m=1`, to the bad run. Does gating rescue it? Explain the
      result, because it is not the one most students expect.
   6. In one paragraph: your filter reported a small covariance while being
      badly wrong, and raised nothing. Name the single logged quantity that
      would have caught it, and say what the vehicle should do when that
      quantity leaves its range.

   .. raw:: html

      <hr>

   **Deliverable**

   The two plots, a three-row results table, and the paragraph from
   question 6.

   .. dropdown:: What to expect
      :color: warning

      With a constant acceleration of about 0.4 m/s squared you should see
      something close to this:

      .. list-table::
         :widths: 28 24 24 24
         :header-rows: 1

         * - **Run**
           - **Reported** :math:`\sigma_p`
           - **True error**
           - **Mean NIS**
         * - :math:`q = 10^{-6}`
           - **0.115 m**
           - **29.7 m**
           - **475**
         * - :math:`q = 1.0`
           - 0.363 m
           - 0.044 m
           - 1.04

      Compare the two middle columns of the first row. The filter reports
      about 12 cm of uncertainty while sitting 30 m from the truth, so its
      reported uncertainty is wrong by more than two orders of magnitude.
      No error is raised, and the trajectory looks smooth.

      Question 4 is the useful part. The NIS leaves its range well before the
      position error becomes visibly wrong, and that interval is the warning
      margin you get for one line of logging.

      Question 5 is the one most students get wrong. Gating does not rescue
      the bad run, and it makes the result worse. Once the estimate has
      drifted, the correct measurements are the ones that disagree with it,
      so the gate discards exactly the data that would have corrected it.
      This is the same problem as L2's zero-Doppler filter: a mechanism that
      discards inconvenient returns ends up preserving the error. Gating
      protects an accurate filter from bad measurements, but it cannot
      repair an inaccurate one, which is why rejections have to be counted
      and escalated.


.. dropdown:: Exercise 6. Association, and What Went Wrong at Tempe
   :icon: eye
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Work through the yes-or-no decision that sits inside the smooth
   estimator, then use it to explain a real crash precisely.

   .. raw:: html

      <hr>

   **Part A. By hand**

   Two confirmed tracks, predicted to:

   .. list-table::
      :widths: 20 30 50
      :header-rows: 1

      * - **Track**
        - **Predicted position**
        - **Innovation covariance** :math:`S`
      * - T1
        - (10.0, 2.0)
        - :math:`\mathrm{diag}(1.0,\ 1.0)`, a well pinned track
      * - T2
        - (11.0, 2.0)
        - :math:`\mathrm{diag}(4.0,\ 4.0)`, a looser track

   Three detections arrive: :math:`D_1` at (10.6, 2.0), :math:`D_2` at
   (9.2, 2.0) and :math:`D_3` at (13.5, 2.0).

   1. Compute the **squared Mahalanobis distance** from every track to every
      detection. Present the result as a 2 by 3 cost matrix.
   2. Apply a 99% gate, which is :math:`\chi^2_{2} = 9.21`. **One track and
      detection pairing gets rejected, and the other track accepts that same
      detection.** Find it, and explain how one detection can be
      implausible for one track and completely unremarkable for another.
   3. Run **nearest neighbour**, taking T1 first, then run it again taking
      T2 first. Report both assignments and both total costs. Do you get the
      same answer?
   4. Run **GNN**, meaning find the assignment with the lowest total cost.
      Which nearest neighbour result does it match, and what happens to the
      leftover detection?
   5. A fourth detection :math:`D_4` arrives at (10.5, 2.0), which is
      **exactly 0.5 m from each track** in ordinary distance. Which track
      does it prefer, by what factor, and why? This is the point of the
      whole exercise.

   .. raw:: html

      <hr>

   **Part B. The analysis**

   In no more than one page, explain the Tempe collision as a data
   association failure. You must:

   6. State why "the object was detected" and "the object was tracked" are
      two different claims, and say which one failed.
   7. Explain how an unstable **label** destroyed **track** continuity, and
      why that removed the ability to brake.
   8. Propose **one** change to the architecture, in a single sentence, that
      would have prevented this specific failure. Then name something your
      change would make worse.

   .. raw:: html

      <hr>

   **Deliverable**

   The cost matrix and assignments for Part A, and at most one page for
   Part B.

   .. dropdown:: Guidance
      :color: success

      Question 1: with a diagonal :math:`S`,
      :math:`d^2 = \frac{\Delta x^2}{S_{xx}} + \frac{\Delta y^2}{S_{yy}}`.

      .. list-table::
         :widths: 25 25 25 25
         :header-rows: 1

         * -
           - :math:`D_1`
           - :math:`D_2`
           - :math:`D_3`
         * - **T1**
           - 0.36
           - 0.64
           - **12.25**, rejected
         * - **T2**
           - 0.04
           - 0.81
           - 1.5625

      Question 2: :math:`D_3` fails the gate for **T1**, since 12.25 is
      above 9.21, but sits comfortably inside it for **T2** at 1.56. The
      detection did not change. The **expectation** changed. T1 claims to
      know where its object is to within a metre, so a 3.5 m disagreement is
      extraordinary. T2 only claims two metres, so the same detection is
      1.25 sigma away and completely ordinary. **A gate tests agreement
      relative to claimed certainty**, which is also exactly why an
      overconfident filter gates away good data.

      Question 3: **no, and that is the objection to nearest neighbour.**
      Taking T1 first gives T1 to :math:`D_1` and T2 to :math:`D_2`, with a
      total of **1.17**. Taking T2 first gives T2 to :math:`D_1` and T1 to
      :math:`D_2`, with a total of **0.68**. Same code, same data, different
      answer, decided purely by the order of the track list.

      Question 4: GNN finds T1 to :math:`D_2` and T2 to :math:`D_1`, total
      **0.68**. That matches the second ordering, but it found it
      deterministically rather than by luck. :math:`D_3` is left over, so it
      becomes a **tentative track**, and the M of N test decides over the
      next few frames whether it was a new object or junk.

      Question 5: :math:`D_4` is 0.5 m from each track, but :math:`d^2` is
      0.25 for T1 and 0.0625 for T2. It prefers **T2 by a factor of four**,
      meaning it prefers the **less** certain track. Mahalanobis distance
      measures disagreement in units of expected disagreement, so the same
      half metre is half a sigma for T1 and a quarter of a sigma for T2.
      Ordinary distance cannot express this, which is why it is the wrong
      tool for association.

      Question 7: a track that gets destroyed and recreated has **no
      history**, so it has no velocity estimate. With no velocity there is
      no time to collision, and with no time to collision nothing ever
      triggers braking. The filter was working correctly the whole time, on
      a track that was one frame old.

      Question 8: the change most people propose is **separating track
      identity from the label**. Track the object, label it separately, and
      never reset a track just because the label changed. What it makes
      worse: you now keep tracks for things that may turn out to be junk, so
      your false track rate goes up and something downstream has to cope
      with that. A good answer names the cost honestly instead of claiming a
      free win.
