====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Eight take-home exercises built on the Lecture 8 notes, :doc:`l8_lecture`,
and on the lecture's Town01 junction. They use only the lecture, never
:doc:`Going Further <l8_appendix>`. Exercise 1 works out how far ahead to
predict. Exercises 2 and 3 run the physics models by hand. Exercise 4 checks
CV's 95% region. Exercise 5 scores several futures, and Exercise 6 gives
them probabilities with Bayes' rule. Exercise 7 runs the IDM and gap
acceptance, and Exercise 8 puts the prediction to use in the AV's plan.
Two exercises end with a check in the lecture's hands-on window.

.. note::

   Every exercise can be done with a calculator. The hands-on checks need
   ``l8_handson.py`` and ``l8sim.py`` from folder ``lecture8`` of the
   course's Python repository, and no CARLA server (see :doc:`l8_code`).

   **The scene:** a T-junction of Town01, :math:`x` east and :math:`y`
   north in meters. The AV drives east at 8 m/s, straight on. Car A, on the
   other lane, drives west, brakes for a left turn across the AV's lane and
   turns at 5.0 m/s. Car B follows A and goes straight on. :math:`t` = 0 is
   now. The motion is simulated, and every speed and braking in it was
   chosen for the lecture. Numbers that are not the lecture's are marked
   "chosen for this exercise".


.. dropdown:: Exercise 1. How Far Ahead to Predict
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Work out how far ahead the prediction must reach for other speeds and
   brakings, and compare it with the lecture's 5 s horizon and the
   datasets' windows.

   .. raw:: html

      <hr>

   **Specification**

   The prediction must reach at least as far ahead as the AV needs to react
   and stop. In the lecture: 8 m/s, a reaction time of 0.5 s and braking at
   3 m/s² give 0.5 + 8 / 3 = 3.17 s and 4.0 + 10.67 = 14.67 m. While
   braking, the speed falls evenly to 0, so the average speed is half the
   starting speed, and the braking distance is that average speed × the
   braking time.

   The datasets' windows (observed, then predicted): Argoverse 2 s and 3 s;
   Argoverse 2, 5 s and 6 s; Waymo Open Motion, 1 s and 8 s.

   .. raw:: html

      <hr>

   **Part A. A faster AV**

   The AV drives at 10 m/s (chosen for this exercise), with the lecture's
   reaction time and braking.

   1. How long, and how far, does it take to react?
   2. How long, and how far, does it take to brake to a stop?
   3. How far ahead in time must the prediction reach? Is the lecture's 5 s
      enough?

   .. raw:: html

      <hr>

   **Part B. A wet road**

   The AV drives at 8 m/s on a wet road, where it brakes at only 1.5 m/s²
   (chosen for this exercise).

   4. How far ahead in time must the prediction reach now? Is 5 s enough?
   5. Which of the three datasets predict far enough ahead for this case?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 5, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: 0.5 s, and 10 × 0.5 = 5.0 m.

      Question 2: 10 / 3 = 3.33 s. The average speed is 10 / 2 = 5 m/s, so
      the AV drives 5 × 3.33 = 16.67 m.

      Question 3: 0.5 + 3.33 = 3.83 s (and 5.0 + 16.67 = 21.67 m). Yes:
      5 s covers 3.83 s, with room to slow down gently.

      Question 4:

      1. Reacting: 0.5 s and 4.0 m, as in the lecture.
      2. Braking: 8 / 1.5 = 5.33 s, at an average speed of 8 / 2 = 4 m/s:
         4 × 5.33 = 21.33 m.
      3. In all: 0.5 + 5.33 = 5.83 s and 4.0 + 21.33 = 25.33 m.

      No: 5 s is shorter than 5.83 s. On a wet road, the AV would need to
      predict further ahead, or drive slower.

      Question 5: Argoverse 2 (6 s) and Waymo Open Motion (8 s). Argoverse's
      3 s is too short.


.. dropdown:: Exercise 2. Constant Velocity and Its Scores
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict car A with constant velocity by hand, then score the prediction
   with its displacement errors, ADE, FDE and the miss rule.

   .. raw:: html

      <hr>

   **Specification**

   From the fit at :math:`t` = 0 (rounded): :math:`x_0` = 174.59 m,
   :math:`y_0` = 1.98 m, :math:`v_x` = −5.985 m/s, :math:`v_y` =
   −0.194 m/s. CV predicts :math:`x(h) = x_0 + v_x h` and
   :math:`y(h) = y_0 + v_y h`.

   The truth at :math:`h` = 5 s: car A is at (154.08, −6.98) m, in the side
   road. CV's errors at 1 to 5 s: 0.52, 1.50, 2.58, 6.01 and 12.35 m.

   A prediction misses when its FDE is above 2.0 m.

   .. raw:: html

      <hr>

   **Part A. The prediction**

   1. Compute CV's position at :math:`h` = 1, 2, 3, 4 and 5 s.
   2. Which way does CV say car A goes, and at what speed?

   .. raw:: html

      <hr>

   **Part B. The scores**

   3. Compute the FDE yourself from CV's position at 5 s and the truth.
   4. Compute the ADE over the five whole seconds.
   5. Over all 50 predicted times (every 0.1 s from 0.1 to 5.0 s), the
      lecture's ADE is 3.37 m. Why is it smaller than your answer to 4?
   6. Is CV's prediction a miss? Are CTRV's (FDE 10.00 m) and CTRA's (FDE
      7.26 m)?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 6, with the arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1:

      .. list-table::
         :widths: 20 40 40
         :header-rows: 1
         :class: compact-table

         * - :math:`h`
           - :math:`x` (m)
           - :math:`y` (m)
         * - 1 s
           - 174.59 − 5.985 = 168.60
           - 1.98 − 0.194 = 1.79
         * - 2 s
           - 174.59 − 11.97 = 162.62
           - 1.98 − 0.388 = 1.59
         * - 3 s
           - 174.59 − 17.955 = 156.64
           - 1.98 − 0.582 = 1.40
         * - 4 s
           - 174.59 − 23.94 = 150.65
           - 1.98 − 0.776 = 1.20
         * - 5 s
           - 174.59 − 29.925 = 144.67
           - 1.98 − 0.970 = 1.01

      Question 2: west, a little south, past the junction, at
      :math:`\sqrt{5.985^2 + 0.194^2}` = 5.99 m/s. CV has no turn in it.

      Question 3:

      1. Along :math:`x`: 154.08 − 144.67 = 9.41 m apart.
      2. Along :math:`y`: 1.01 − (−6.98) = 7.99 m.
      3. FDE: :math:`\sqrt{9.41^2 + 7.99^2} = \sqrt{88.55 + 63.84} =
         \sqrt{152.39}` = 12.34 m. The lecture's 12.35 m comes from the
         unrounded fit.

      Question 4: (0.52 + 1.50 + 2.58 + 6.01 + 12.35) / 5 = 22.96 / 5 =
      4.59 m.

      Question 5: the five whole seconds leave out the times from 0.1 to
      0.9 s, where the errors are smallest, and two of the five (4 and 5 s)
      are the largest errors. The 50 times start at 0.1 s, so the small
      early errors pull the average down.

      Question 6: all three miss: 12.35, 10.00 and 7.26 m are all above
      2.0 m. At :math:`t` = 0, car A has not started its turn, and none of
      the three physics models has a term for a turn that has not started.


.. dropdown:: Exercise 3. Turn Rates and Circles
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use CTRV's circle, radius = speed / turn rate, to see when a turn rate is
   real, and why CTRV goes wrong after a turn.

   .. raw:: html

      <hr>

   **Specification**

   CTRV keeps the speed :math:`v` and the turn rate :math:`\omega`, so the
   road user drives on a circle of radius :math:`v / \omega`.

   - At :math:`t` = 0, the fit gives car A 5.99 m/s and 0.049 rad/s. A
     drives straight.
   - At :math:`t` = 3 s, in the middle of the turn, it gives 4.98 m/s and
     0.331 rad/s.
   - A's left turn on the map is about a quarter circle, 23.07 m long.

   .. raw:: html

      <hr>

   **Part A. Car A's two fits**

   1. Compute the radius of CTRV's circle at :math:`t` = 0 and at
      :math:`t` = 3 s.
   2. Compute the radius of the lane's turn. Which of the two fits matches
      it?
   3. Where does the 0.049 rad/s at :math:`t` = 0 come from?

   .. raw:: html

      <hr>

   **Part B. A circle that keeps turning**

   A car drives at 10 m/s in a turn of radius 20 m (chosen for this
   exercise), and CTRV reads both exactly.

   4. What is its turn rate?
   5. A turn like A's is a quarter circle, :math:`\pi/2` rad. After how many
      seconds has CTRV turned a quarter circle?
   6. By how many degrees has CTRV's heading turned after 5 s? What does
      that mean when the lane straightens after a quarter turn?

   .. raw:: html

      <hr>

   **Part C. A speed that is a little wrong**

   7. The lecture says 0.1 m/s off is 0.5 m after 5 s. How far off is a CV
      prediction after 3 s if its speed is 0.3 m/s off (chosen for this
      exercise), with no turn?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 7, with the arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: at :math:`t` = 0, 5.99 / 0.049 = 122 m, nearly straight.
      At :math:`t` = 3 s, 4.98 / 0.331 = 15.0 m.

      Question 2: a quarter circle turns π/2 = 1.571 rad, and length =
      radius × angle, so the radius is 23.07 / 1.571 = 14.7 m. The fit at :math:`t` = 3 s (15.0 m) matches
      it.

      Question 3: from the 0.05 m errors in the track. A turn rate read from
      1.5 s of track is noisy; the true turn rate at :math:`t` = 0 is
      0 rad/s.

      Question 4: :math:`\omega = v / r` = 10 / 20 = 0.5 rad/s.

      Question 5: (π/2) / 0.5 = 3.14 s.

      Question 6:

      1. 0.5 × 5 = 2.5 rad.
      2. 2.5 × 180 / π = 143°.

      The lane turns 90° and then runs straight, but CTRV's circle keeps
      turning, 53° more than the lane by 5 s. This is what the lecture's
      figure shows at :math:`t` = 3 s: CTRV follows the curve, then its
      dotted circle swings on.

      Question 7: 0.3 × 3 = 0.9 m. A speed error grows in proportion to the
      time.


.. dropdown:: Exercise 4. Is CV's 95% Region Honest?
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compute CV's 95% region for car A, check the truth against it, and say
   what the test set's counts mean.

   .. raw:: html

      <hr>

   **Specification**

   :math:`\sigma` is the standard deviation of CV's predicted position, per
   axis. The 95% radius is 2.45 × :math:`\sigma`.

   .. list-table::
      :widths: 25 25 50
      :header-rows: 1
      :class: compact-table

      * - :math:`h`
        - :math:`\sigma`
        - **CV's error for car A**
      * - 1 s
        - 0.293 m
        - 0.52 m
      * - 3 s
        - 1.50 m
        - 2.58 m
      * - 5 s
        - 3.23 m
        - 12.35 m

   On the test set, CV's 95% region held the truth 81.5, 85.6 and 82.6% of
   the time at 1, 3 and 5 s with no turn, and 46.5, 20.4 and 7.2% with a
   turn. With no turn, the lecture also splits the predictions by route: on
   straight routes, the region held the truth 100% of the time; on turning
   routes, before the turn, 59 to 68%. Chance alone moves each number by
   about 2 points (counted by drive).

   .. raw:: html

      <hr>

   **Part A. Car A**

   1. Compute the 95% radius at 1, 3 and 5 s.
   2. At each of the three times, is the truth inside the region?
   3. Why does the region grow with the horizon? Of the lecture's two
      causes, which one is almost all of it?

   .. raw:: html

      <hr>

   **Part B. The test set**

   4. Is CV's region honest with no turn? Look at the average, then at the
      two route groups. With a turn? Say "too narrow" (the predictor is too
      sure) or "too wide" (not sure enough).
   5. Why does the region fail so badly with a turn?
   6. Another predictor's region (chosen for this exercise) holds the
      truth 99% of the time at every horizon. Is it honest? What would it
      cost the planner?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 6.

   .. dropdown:: Guidance
      :color: success

      Question 1: 2.45 × 0.293 = 0.72 m, 2.45 × 1.50 = 3.68 m and 2.45 ×
      3.23 = 7.91 m.

      Question 2: at 1 s, 0.52 m is less than 0.72 m: inside. At 3 s,
      2.58 m is less than 3.68 m: inside. At 5 s, 12.35 m is more than
      7.91 m: outside.

      Question 3: two causes. The fitted velocity has an error, carried
      further at each second, and CV lets the speed drift (0.5 m/s per
      :math:`\sqrt{\text{s}}`, chosen in the lecture). The drift is almost
      all of it: the fitted velocity's error adds under 3% of the variance
      from 1 s on.

      Question 4: a 95% region must hold the truth 95% of the time. With no
      turn, the average, 82 to 86%, looks a little too narrow. But it hides
      two groups, and neither is honest: straight routes, 100%, too wide;
      turning routes before the turn, 59 to 68%, too narrow. Chance alone
      moves each number by about 2 points, so these gaps are not chance. With
      a turn, 46.5% down to 7.2%: far too narrow.

      Question 5: CV's region has no term for a turn or a speed change, so a
      car that turns, or brakes for a turn, leaves it.

      Question 6: no. A 95% region that holds the truth 99% of the time is
      larger than it needs to be: too wide, not sure enough. The planner keeps more
      room where the uncertainty is larger, so it would keep more room than
      needed and slow down or wait for nothing.


.. dropdown:: Exercise 5. Scoring Several Futures
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Score multimodal predictions with minADE, minFDE, the miss rule and the
   probability given to the true future, and see why minFDE alone is not
   enough.

   .. raw:: html

      <hr>

   **Specification**

   The lecture's map-aware predictor gives car A two modes at
   :math:`t` = 0:

   .. list-table::
      :widths: 30 25 20 25
      :header-rows: 1
      :class: compact-table

      * - **Mode**
        - **Probability**
        - **ADE**
        - **FDE**
      * - left turn
        - 0.87
        - 0.86 m
        - 1.88 m
      * - straight on
        - 0.13
        - 3.55 m
        - 13.06 m

   A second predictor (chosen for this exercise) gives three modes: the same
   left turn with probability 0.40, the same straight on with probability
   0.35, and a stop before the junction with probability 0.25 and an FDE of
   9.00 m. Car A really turns left.

   .. raw:: html

      <hr>

   **Part A. The lecture's predictor**

   1. Compute minADE and minFDE.
   2. Is the prediction a miss? State the rule for several modes.
   3. What probability does the predictor give to the true future?

   .. raw:: html

      <hr>

   **Part B. The two modes' average**

   4. The point-by-point average of the two modes ends at 5 s 7.21 m from
      each mode, with an FDE of 5.92 m. Is it a miss? Can a driver end up
      there?

   .. raw:: html

      <hr>

   **Part C. The second predictor**

   5. Check that its probabilities add up to 1.
   6. Compute its minFDE. Is it a miss?
   7. Which predictor is better for the planner, and which score shows it?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 7.

   .. dropdown:: Guidance
      :color: success

      Question 1: the best mode is the one that ends closest to the truth:
      the left turn, 1.88 m against 13.06 m. minFDE is its FDE, 1.88 m, and
      minADE is its ADE, 0.86 m.

      Question 2: no. With several modes, a miss means that no mode ends
      within 2.0 m. The left turn ends 1.88 m from the truth.

      Question 3: 0.87, the left turn's probability.

      Question 4: 5.92 m is above 2.0 m: a miss. It ends inside the AV's
      own lane, facing against its traffic, so no driver in A's lane ends up
      there.
      This is why predictors give several futures instead of their average.

      Question 5: 0.40 + 0.35 + 0.25 = 1.00.

      Question 6: the smallest of 1.88, 13.06 and 9.00 is 1.88 m: not a
      miss. Its minFDE is the same as the lecture's predictor's.

      Question 7: the lecture's predictor. minFDE cannot tell them apart,
      because it does not look at the probabilities. The probability given
      to the true future can: 0.87 against 0.40. The second predictor also
      makes the AV keep clear of three modes instead of two. A good
      multimodal prediction has few modes, one of them close to the truth,
      and most of the probability on that one.


.. dropdown:: Exercise 6. Probabilities from the Map and Bayes' Rule
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Redo the lecture's four steps for car A by hand, then change the spread
   :math:`\sigma` and the prior and see how P(left) moves.

   .. raw:: html

      <hr>

   **Specification**

   From the lecture:

   - Car A is 6.51 m from the junction and drives at 5.988 m/s (5.99 m/s,
     rounded). Its offset and heading are the same for both lanes, so only
     the speed counts.
   - Straight on expects the street's speed, 8 m/s (chosen).
   - The left turn has a radius of 14.7 m. The predictor assumes a sideways
     acceleration of 2.0 m/s² in the turn and a braking of 1.0 m/s² before
     it (both chosen).
   - The speed likelihood is :math:`e^{-\frac12 (\Delta v / \sigma)^2}`,
     where :math:`\Delta v` is A's speed minus the path's, and
     :math:`\sigma` = 1.0 m/s (chosen).
   - Bayes' rule: multiply each prior by its likelihood, then divide by the
     sum.

   .. raw:: html

      <hr>

   **Part A. The expected speeds**

   1. Compute the left turn's speed, :math:`\sqrt{2.0 \times 14.7}`.
   2. Compute the speed a driver who brakes at 1.0 m/s² to that turn speed
      has now, 6.51 m before the junction:
      :math:`\sqrt{\text{turn speed}^2 + 2 \times \text{braking} \times
      \text{distance}}`.

   .. raw:: html

      <hr>

   **Part B. The probabilities**

   3. Compute both likelihoods with :math:`\sigma` = 1.0 m/s.
   4. Compute P(left) with equal priors, 0.5 each.
   5. Redo question 4 with :math:`\sigma` = 0.5 m/s, then with
      :math:`\sigma` = 2.0 m/s. Explain the change.
   6. Back to :math:`\sigma` = 1.0 m/s. Suppose data showed that 30% of
      drivers turn left here (chosen for this exercise): prior 0.3 for left
      and 0.7 for straight on. Compute P(left).

   .. raw:: html

      <hr>

   **Part C. A driver who does not look like the rule**

   7. A different car (chosen for this exercise) cruises at 6.00 m/s,
      6.51 m before the junction, and will go straight on. With
      :math:`\sigma` = 1.0 m/s and equal priors, what P(left) does the
      predictor give it? Which failure from the lecture is this?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 7, with the arithmetic.

   **Check in the hands-on window:** in ``l8sim.py``, set ``SIG_V = 0.5``,
   then ``2.0``, run ``python3 l8_handson.py --part modes`` and read P(left)
   at :math:`t` = 0. Set ``SIG_V`` back to 1.0 after.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`\sqrt{2.0 \times 14.7} = \sqrt{29.4}` = 5.42 m/s.

      Question 2: :math:`\sqrt{5.42^2 + 2 \times 1.0 \times 6.51} =
      \sqrt{29.4 + 13.02} = \sqrt{42.4}` = 6.51 m/s.

      Question 3:

      1. Left: :math:`\Delta v` = 5.988 − 6.512 = −0.524 m/s;
         :math:`e^{-\frac12 (0.524)^2} = e^{-0.137}` = 0.872.
      2. Straight on: :math:`\Delta v` = 5.988 − 8.000 = −2.012 m/s;
         :math:`e^{-\frac12 (2.012)^2} = e^{-2.024}` = 0.132.

      Question 4: 0.5 × 0.872 = 0.436 and 0.5 × 0.132 = 0.066; P(left) =
      0.436 / (0.436 + 0.066) = 0.436 / 0.502 = 0.87.

      Question 5:

      - :math:`\sigma` = 0.5 m/s: left, :math:`e^{-\frac12 (0.524 /
        0.5)^2} = e^{-0.549}` = 0.577; straight on, :math:`e^{-\frac12
        (2.012 / 0.5)^2} = e^{-8.096}` = 0.0003. P(left) = 0.577 / (0.577
        + 0.0003) = 0.9995.
      - :math:`\sigma` = 2.0 m/s: left, :math:`e^{-\frac12 (0.524 /
        2.0)^2} = e^{-0.034}` = 0.966; straight on, :math:`e^{-\frac12
        (2.012 / 2.0)^2} = e^{-0.506}` = 0.603. P(left) = 0.966 / (0.966 +
        0.603) = 0.62.

      :math:`\sigma` says how much drivers' speeds differ. A small
      :math:`\sigma` says that drivers hold the expected speed closely, so
      A's 2.01 m/s gap to the straight-on speed rules that path out. A large
      :math:`\sigma` says that drivers differ a lot, so the same gap is weak
      evidence. The hands-on window shows the same values: about 1.00 and
      0.62.

      Question 6:

      1. Left: 0.3 × 0.872 = 0.2616. Straight on: 0.7 × 0.132 = 0.0924.
      2. Sum: 0.2616 + 0.0924 = 0.3540.
      3. P(left) = 0.2616 / 0.3540 = 0.74.

      Question 7:

      1. Left: :math:`\Delta v` = 6.00 − 6.51 = −0.51 m/s;
         :math:`e^{-\frac12 (0.51)^2} = e^{-0.130}` = 0.878.
      2. Straight on: :math:`\Delta v` = 6.00 − 8.00 = −2.00 m/s;
         :math:`e^{-\frac12 (2.00)^2} = e^{-2.0}` = 0.135.
      3. P(left) = 0.878 / (0.878 + 0.135) = 0.87.

      The predictor is as sure of a left turn as it was for car A, but this
      car goes straight on. This is the lecture's "a driver who does not
      look like the rule": a car cruising at 6 m/s on an 8 m/s street looks
      like a car about to turn.


.. dropdown:: Exercise 7. The IDM and Gap Acceptance
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run the Intelligent Driver Model for car B by hand in a second case, and
   decide when car A turns across the AV's lane.

   .. raw:: html

      <hr>

   **Specification**

   The IDM:

   .. math::

      a = a_{\max}\Big[\,1 - \Big(\frac{v}{v_0}\Big)^{4} - \Big(\frac{s^*}{s}\Big)^2\,\Big],
      \qquad s^* = s_0 + v\,T + \frac{v\,\Delta v}{2\sqrt{a_{\max}\,b}}

   :math:`v` is B's speed, :math:`s` the gap to A, :math:`\Delta v` how fast
   B closes in, :math:`s^*` the gap B wants. The paper's values:
   :math:`T` = 1.6 s, :math:`a_{\max}` = 0.73 m/s², :math:`b` =
   1.67 m/s², :math:`s_0` = 2 m; :math:`v_0` = 9 m/s (chosen). In the
   lecture, :math:`v` = 7.76 m/s, :math:`s` = 22.25 m, A drives at
   5.99 m/s, and B's acceleration comes out at −0.30 m/s².

   Gap acceptance: car A decides 6 m before the junction (chosen). It turns
   only if the AV is at least 4.1 s (the critical headway) from the
   crossing at that moment. The AV drives at 8 m/s. In run 1, it is 48 m
   from the crossing at that moment: 48 / 8 = 6.0 s.

   .. raw:: html

      <hr>

   **Part A. The IDM**

   1. Suppose A drove at 7.76 m/s too, the same as B (chosen for this
      exercise), with the same gap of 22.25 m. Compute :math:`\Delta v` and
      :math:`s^*`.
   2. Compute B's acceleration. Compare it with the lecture's −0.30 m/s²
      and explain the difference.

   .. raw:: html

      <hr>

   **Part B. Gap acceptance**

   3. The AV starts 8 m closer than in run 1 (chosen for this exercise).
      What is A's gap, and does A turn?
   4. In run 2, the AV starts 24 m closer. How much later must the AV
      arrive at the crossing for A to turn without waiting?
   5. Suppose the critical headway were 2.5 s instead of 4.1 s (chosen for
      this exercise). What does A do in run 2? What about car B, behind it?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 5, with the arithmetic.

   **Check in the hands-on window:** in ``l8sim.py``, set ``GAP = 2.5``, run
   ``python3 l8_handson.py --part interact``, tick **AV 24 m closer** and
   compare with question 5. Set ``GAP`` back to 4.1 after.

   .. dropdown:: Guidance
      :color: success

      Question 1:

      1. :math:`\Delta v` = 7.76 − 7.76 = 0 m/s, so the last term of
         :math:`s^*` is 0.
      2. :math:`s^*` = 2 + 7.76 × 1.6 = 2 + 12.42 = 14.42 m.

      Question 2:

      1. :math:`1 - (7.76/9)^4` = 1 − 0.553 = 0.447, as in the lecture.
      2. :math:`(s^*/s)^2` = (14.42 / 22.25)² = 0.648² = 0.420.
      3. :math:`a` = 0.73 × (0.447 − 0.420) = 0.73 × 0.027 = +0.02 m/s².

      B holds its speed. In the lecture, B closes in on A at 1.77 m/s, which
      adds 7.76 × 1.77 / (2 × 1.104) = 6.22 m to the gap it wants (20.64 m
      instead of 14.42 m), so B brakes at −0.30 m/s².

      Question 3: 8 m at 8 m/s is 1.0 s less, so the gap is 6.0 − 1.0 =
      5.0 s. 5.0 s ≥ 4.1 s: A turns without stopping.

      Question 4: in run 2 the gap is 6.0 − 24 / 8 = 3.0 s. A turns when the
      gap is at least 4.1 s, so the AV must arrive 4.1 − 3.0 = 1.1 s later,
      or more. The lecture's two cases agree: 1 s later gives 4.0 s, and A
      still waits; 2 s later gives 5.0 s, and A goes.

      Question 5: 3.0 s ≥ 2.5 s, so A turns without stopping, as in run 1.
      Car A then does what it did in run 1, so car B, behind it, slows as in
      run 1 too.


.. dropdown:: Exercise 8. Using the Prediction in the AV's Plan
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compare when the AV reaches the crossing with when car A is in the AV's
   lane, for several plans, and see what the prediction's own error means
   for the planner.

   .. raw:: html

      <hr>

   **Specification**

   From the lecture:

   - At 8 m/s, the AV reaches the point where A's left turn crosses its lane
     at :math:`t` = 6.08 s.
   - The left-turn mode (probability 0.87) puts A in the AV's lane from
     :math:`t` = 3.2 to 4.0 s. In truth, A is there from :math:`t` = 3.4 to
     4.3 s.
   - The left mode turns at 5.42 m/s; A really turns at 5.0 m/s.
   - A check of current positions only first finds A in the AV's lane at
     :math:`t` = 3.4 s.

   .. raw:: html

      <hr>

   **Part A. The distance**

   1. How far is the AV from the crossing at :math:`t` = 0?

   .. raw:: html

      <hr>

   **Part B. Three plans**

   The AV keeps a constant speed of 10, 11 or 12 m/s (three separate plans,
   chosen for this exercise).

   2. For each plan, when does the AV reach the crossing?
   3. For each plan, is A in the AV's lane at that time, by the left mode?
      By the truth?
   4. Why do the left mode and the truth disagree about the 12 m/s plan?
      What should the planner do about it?

   .. raw:: html

      <hr>

   **Part C. Time to react**

   5. With current positions only, how much time does the AV have between
      :math:`t` = 0 and the moment it first finds A in its lane? With the
      prediction?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 5.

   .. dropdown:: Guidance
      :color: success

      Question 1: 8 × 6.08 = 48.64 m.

      Question 2: 48.64 / 10 = 4.86 s; 48.64 / 11 = 4.42 s; 48.64 / 12 =
      4.05 s.

      Question 3:

      - 10 m/s, 4.86 s: after 4.0 s and after 4.3 s. A has left the lane, by
        the mode and by the truth.
      - 11 m/s, 4.42 s: after 4.0 s and after 4.3 s. A has left, by both.
      - 12 m/s, 4.05 s: after the mode's 4.0 s, so the mode says A has left.
        But it is before the truth's 4.3 s: A is still in the AV's lane.

      Question 4: the left mode picks the right lane but drives it a little
      too fast (5.42 m/s against A's 5.0 m/s), so it has A leave the AV's
      lane 0.3 s too early. A plan that arrives 0.05 s after the mode's
      window has no room for that error. The planner must keep a margin in
      time around each likely mode, not only avoid the mode's exact times.
      Which modes count, and how much room to keep, is the planner's job
      (L9).

      Question 5: with current positions only, the AV first finds A in its
      lane at :math:`t` = 3.4 s, when A is already there: no warning. With
      the prediction, the AV knows at :math:`t` = 0, 3.4 s earlier, which
      gives it time to ease off gently instead of braking hard.
