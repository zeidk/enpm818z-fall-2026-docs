====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Working
   through this page is good preparation for one. Memorizing the answers
   below is not.

This quiz covers Lecture 8: what a planner needs from prediction and how far
ahead it must look, the physics models (CV, CTRV, CTRA) and why their error
grows, ADE, FDE and the miss rate, CV's 95% region and its honesty check,
several futures with minADE and minFDE, the map's lanes as candidate paths
with Bayes' rule, intent, the Intelligent Driver Model (IDM), and gap
acceptance. Every question can be answered from the lecture notes,
:doc:`l8_lecture`. Nothing on this page needs
:doc:`Going Further <l8_appendix>`.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.
   - The lecture's scene is a T-junction of CARLA's Town01. The AV drives
     east at 8 m/s, straight on. Car A, on the other lane, drives west and
     brakes for a left turn across the AV's lane. Car B follows car A and
     goes straight on. :math:`t` = 0 is now; the predictions reach 5 s
     ahead. The motion is simulated, and every speed and braking in it was
     chosen for the lecture. The map frame has :math:`x` east and :math:`y`
     north, in meters.


----


Multiple Choice (Questions 1 to 14)
===================================

.. admonition:: Question 1
   :class: hint

   L5's tracker already predicts each road user with constant velocity.
   Why does the planner need more than that?

   A. The tracker's prediction uses the wrong units.

   B. The tracker predicts one step, 0.1 s ahead, and the next detection
      corrects it. The planner needs where the road user will be 1 to 5 s
      ahead, and nothing corrects those predictions until they happen.

   C. The tracker does not know the road user's velocity.

   D. The planner needs the road user's position now, which the tracker
      does not give.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The tracker's state is :math:`[\,p_x,\ p_y,\ v_x,\ v_y\,]`, so it knows
   the velocity (**C** is wrong), and it gives the position now (**D** is
   wrong). Its one constant-velocity step only says where to look among the
   next detections, and a new detection then corrects it. The planner needs
   many steps, and constant velocity has no turn in it. See the
   Introduction in :doc:`l8_lecture`.


.. admonition:: Question 2
   :class: hint

   The AV drives at 8 m/s. Reacting takes 0.5 s, and the AV then brakes at
   3 m/s² (both chosen in the lecture). At least how far ahead in time
   must the prediction reach?

   A. 2.67 s

   B. 3.17 s

   C. 5 s

   D. 14.67 s

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   1. Reacting: 0.5 s.
   2. Braking: 8 / 3 = 2.67 s.
   3. In all: 0.5 + 2.67 = 3.17 s.

   **A** leaves out the reaction time. **C** is the horizon the lecture
   chose, which covers the 3.17 s with room to slow down gently. **D** is
   the distance, 4.0 + 10.67 = 14.67 m, not a time. See the Introduction in
   :doc:`l8_lecture`.


.. admonition:: Question 3
   :class: hint

   From the fit, car A is at :math:`x_0` = 174.59 m, :math:`y_0` = 1.98 m,
   with :math:`v_x` = −5.985 m/s and :math:`v_y` = −0.194 m/s. Where does
   constant velocity (CV) put car A at :math:`h` = 2 s?

   A. (162.62, 1.59) m

   B. (168.60, 1.79) m

   C. (186.56, 2.37) m

   D. (156.64, 1.40) m

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   1. :math:`x` = 174.59 − 2 × 5.985 = 174.59 − 11.97 = 162.62 m.
   2. :math:`y` = 1.98 − 2 × 0.194 = 1.98 − 0.388 = 1.59 m.

   **B** is :math:`h` = 1 s and **D** is :math:`h` = 3 s. **C** adds the
   velocity instead of using its sign: the velocity points west and a little
   south. See Physics Models in :doc:`l8_lecture`.


.. admonition:: Question 4
   :class: hint

   At :math:`t` = 0 the fit gives car A a speed of 5.99 m/s and a turn rate
   of 0.049 rad/s, while A really drives straight. What does the lecture
   say about that turn rate?

   A. It shows that A has started its left turn, on a circle of radius
      14.7 m.

   B. It gives a circle of radius 5.99 / 0.049 = 122 m, nearly straight.
      It comes from the 0.05 m errors in the track: a turn rate read from
      1.5 s of track is noisy.

   C. It is exact, because the fit uses 16 positions.

   D. It makes CTRV divide by zero, so CTRV cannot be used at all.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The truth is 0 rad/s: A drives straight at :math:`t` = 0. The 14.7 m in
   **A** is the radius of the lane's left turn, which A has not started.
   **D** confuses this case with a turn rate near 0, where CTRV's formula
   divides by almost 0 and code switches to CV; 0.049 rad/s gives a large
   radius, not a division by zero. See Physics Models in
   :doc:`l8_lecture`.


.. admonition:: Question 5
   :class: hint

   Car A's CV prediction has errors of 0.52, 1.50, 2.58, 6.01 and 12.35 m
   at 1, 2, 3, 4 and 5 s. Using only these five whole seconds, what is the
   ADE?

   A. 2.58 m

   B. 4.59 m

   C. 12.35 m

   D. 22.96 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   1. Sum: 0.52 + 1.50 + 2.58 + 6.01 + 12.35 = 22.96 m.
   2. ADE, the average: 22.96 / 5 = 4.59 m.

   **C** is the FDE, the error at the last time. **D** is the sum, not the
   average. Over all 50 predicted times (every 0.1 s), the lecture's ADE is
   3.37 m. See Scoring in :doc:`l8_lecture`.


.. admonition:: Question 6
   :class: hint

   A predictor gives car A two modes. The left turn ends 1.88 m from the
   truth; straight on ends 13.06 m from it. With Argoverse 2's 2.0 m
   threshold, what are the minFDE and the verdict?

   A. minFDE 7.47 m, a miss.

   B. minFDE 13.06 m, a miss.

   C. minFDE 1.88 m, not a miss.

   D. minFDE 1.88 m, a miss, because one mode ends more than 2 m away.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   minFDE is the smaller of the two endpoint errors, 1.88 m. It is under
   2.0 m, so the prediction is not a miss. With several modes, a miss means
   that **no** mode ends within 2 m (**D** has the rule backward). **A**
   averages the two modes; minFDE takes the best one. See Several Futures in
   :doc:`l8_lecture`.


.. admonition:: Question 7
   :class: hint

   At :math:`h` = 3 s, CV's standard deviation of car A's position is
   :math:`\sigma` = 1.50 m per axis, and CV's error is 2.58 m. Is the truth
   inside CV's 95% region?

   A. Yes: the radius is 2.45 × 1.50 = 3.68 m, and 2.58 m is less.

   B. No: the radius is 1.50 m, and 2.58 m is more.

   C. No: the radius is 1.50 / 2.45 = 0.61 m.

   D. Yes, always: a 95% region holds the truth 95% of the time.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   The 95% radius is 2.45 × :math:`\sigma`. With :math:`\sigma` = 1.50 m,
   that is 3.68 m, and the truth is 2.58 m away, so it is inside. **B**
   uses one :math:`\sigma` as the radius. **D** confuses a promise about
   many predictions with a guarantee for one: at 4 and 5 s, car A's truth
   is outside its region. See Scoring in :doc:`l8_lecture`.


.. admonition:: Question 8
   :class: hint

   On the test set with no turn ahead, CV's 95% region held the truth 81.1,
   85.2 and 81.1% of the time at 1, 3 and 5 s. What does that say?

   A. The region is too large: CV is not sure enough.

   B. The region is honest: 81 to 85% is close enough to 95%.

   C. The region is a little too small: CV is a little too sure.

   D. Nothing: the region can only be checked on turns.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A 95% region must hold the truth 95% of the time. Holding it less often
   means the region is too small for the real errors: the predictor claims
   more certainty than it has. With a turn ahead it is far too sure: 42.8,
   15.3 and 4.8%. The region only covers a slightly wrong speed and knows
   nothing about a turn. See Scoring in :doc:`l8_lecture`.


.. admonition:: Question 9
   :class: hint

   Why do predictors give several futures instead of one?

   A. A single answer trained for the smallest mean squared error tends to
      the average of the futures. Between a left turn and straight on, that
      average leads where no lane goes.

   B. Several futures always have a smaller FDE than one.

   C. The planner cannot read a single trajectory.

   D. Benchmarks forbid a single trajectory.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   For car A, the point-by-point average of the two futures ends at 5 s
   7.21 m from each, toward the junction's corner. No lane leads there, and
   its FDE is 5.92 m, a miss, while the left-turn future alone is off by
   1.88 m. **B** is not a rule: a mode can be far off (straight on ends
   13.06 m away). See Several Futures in :doc:`l8_lecture`.


.. admonition:: Question 10
   :class: hint

   The speed likelihoods of car A's two paths are 0.872 (left) and 0.132
   (straight on), as in the lecture. Suppose the prior for the left turn
   were 0.2 and for straight on 0.8 (chosen for this question: few drivers
   turn here). What is P(left)?

   A. 0.87

   B. 0.62

   C. 0.17

   D. 0.20

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   1. Left: 0.2 × 0.872 = 0.1744. Straight on: 0.8 × 0.132 = 0.1056.
   2. Sum: 0.1744 + 0.1056 = 0.2800.
   3. P(left) = 0.1744 / 0.2800 = 0.62.

   **A** is the lecture's answer with equal priors, where the two 0.5
   priors cancel. **C** forgets to divide by the sum, and **D** ignores the
   evidence. A's slowing down still pulls P(left) from 0.2 up to 0.62. See
   Using the Map in :doc:`l8_lecture`.


.. admonition:: Question 11
   :class: hint

   The lecture's map-aware predictor takes a turn at the speed that gives a
   sideways acceleration of 2.0 m/s² (chosen). For a turn of radius 8.0 m
   (chosen for this question), what turn speed does it expect?

   A. 16.0 m/s

   B. 5.42 m/s

   C. 4.0 m/s

   D. 2.83 m/s

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The turn speed is :math:`v = \sqrt{a \times r}`, with :math:`a` the
   sideways acceleration and :math:`r` the radius:
   :math:`\sqrt{2.0 \times 8.0} = \sqrt{16} = 4.0` m/s. **A** forgets the
   square root. **B** is the lecture's turn speed for A's turn, of radius
   14.7 m. **D** is :math:`\sqrt{8.0}`, without the acceleration. See Using
   the Map in :doc:`l8_lecture`.


.. admonition:: Question 12
   :class: hint

   In the IDM by hand, car B wants a gap :math:`s^*` = 20.64 m, and
   :math:`1 - (v/v_0)^4` = 0.447, with :math:`a_{\max}` = 0.73 m/s².
   Suppose the gap to car A were :math:`s` = 15.0 m instead of 22.25 m
   (chosen for this question), with everything else the same. What is B's
   acceleration?

   A. −0.30 m/s²

   B. +0.33 m/s²

   C. −1.06 m/s²

   D. −1.45 m/s²

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1. :math:`(s^*/s)^2` = (20.64 / 15.0)² = 1.376² = 1.893.
   2. :math:`a` = 0.73 × (0.447 − 1.893) = 0.73 × (−1.446) = −1.06 m/s².

   B brakes harder than in the lecture (−0.30 m/s², **A**), because the gap
   is smaller than the gap it wants. **B** is the free-road term alone,
   0.73 × 0.447. **D** forgets to multiply by :math:`a_{\max}`. See Other
   Drivers in :doc:`l8_lecture`.


.. admonition:: Question 13
   :class: hint

   In run 1, when car A is 6 m before the junction, the AV is 6.0 s from
   the crossing. Suppose the AV started 16 m closer instead (chosen for this
   question), still at 8 m/s. With a critical headway of 4.1 s, what does
   A do?

   A. It turns, because the gap is 6.0 s.

   B. It turns, because the gap is 4.0 s and that is close enough.

   C. It waits, because the gap is 6.0 − 16 / 8 = 4.0 s, below 4.1 s.

   D. It waits, because the gap is 2.0 s.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1. 16 m at 8 m/s is 16 / 8 = 2.0 s less.
   2. Gap: 6.0 − 2.0 = 4.0 s.
   3. 4.0 s is below 4.1 s, so A waits for the AV to pass.

   **D** takes the 2.0 s change for the gap. The lecture makes the same
   point for run 2: an AV that slowed by 1 s would give A a 4.0 s gap, and
   A would still wait. See Other Drivers in :doc:`l8_lecture`.


.. admonition:: Question 14
   :class: hint

   The left-turn mode (probability 0.87) puts car A in the AV's lane from
   :math:`t` = 3.2 to 4.0 s. The AV, at 8 m/s, reaches the crossing at
   :math:`t` = 6.08 s. What does the lecture's planner do?

   A. It brakes hard now, because the left turn is likely.

   B. It keeps its speed: it arrives after A has left the lane. A plan that
      reached the crossing near :math:`t` = 4 s would have to slow down.

   C. It ignores the left turn, because A is in the other lane now.

   D. It changes lanes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The planner keeps the AV away from the crossing while a likely mode puts
   A there. 6.08 s is after 4.0 s, so the AV can keep its speed. **C** is
   the check of today's positions only, which finds A in the AV's lane only
   at :math:`t` = 3.4 s. See Several Futures in :doc:`l8_lecture`.


True or False (Questions 15 to 18)
==================================

.. admonition:: Question 15
   :class: hint

   **True or false:** with no turn ahead, CTRA uses more terms than CV, so
   on the lecture's test set its mean error at 5 s is smaller than CV's.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   With no turn, CTRA's mean error at 5 s is 16.13 m and CV's is 4.01 m.
   Each extra term (CTRV's turn rate, CTRA's braking) is read from a noisy
   track, and that noise is carried 5 s ahead. See "Why the error grows, and
   why more terms do not help" in :doc:`l8_lecture`.


.. admonition:: Question 16
   :class: hint

   **True or false:** a predictor that gives six modes spread over every
   lane and speed has a very good minFDE, so it is the best for the planner.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   One of six spread modes lands near the truth whatever the road user
   does, so minFDE looks very good. But the AV must keep clear of every mode
   it takes seriously, and six spread modes leave it little room. A score
   that uses the probabilities catches this: Waymo's mAP, or the lecture's
   check, the probability given to the true future. See Several Futures in
   :doc:`l8_lecture`.


.. admonition:: Question 17
   :class: hint

   **True or false:** at :math:`t` = 0, car A's offset from the lane's
   center and its heading cannot tell the left-turn lane from the
   straight-on lane.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Before the junction, the two lanes are one: A is 0.07 m from the center
   and 1.86° off the heading of both, so the heading and offset likelihoods
   are the same for both (0.973 and 0.995). Only A's speed tells them apart
   so far: 5.99 m/s, against 6.51 m/s expected for the left turn and
   8.00 m/s for straight on. See Using the Map in :doc:`l8_lecture`.


.. admonition:: Question 18
   :class: hint

   **True or false:** in run 2, car A waits because its track up to
   :math:`t` = 0 shows it braking harder than in run 1.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A's track up to :math:`t` = 0 is the same in both runs. Only the AV
   starts 24 m closer, so A's gap is 6.0 − 24 / 8 = 3.0 s, below 4.1 s, and
   A waits. What A does next depends on where the AV is: the AV's motion is
   an input to A's prediction. See Other Drivers in :doc:`l8_lecture`.


Short Answer (Questions 19 to 20)
=================================

.. admonition:: Question 19
   :class: hint

   In the Tempe crash of March 2018, the ADS detected the pedestrian
   5.6 s before impact. Why did it never predict her path?

.. dropdown:: Answer
   :class-container: sd-border-success

   A prediction is built from the track's history. The NTSB report says
   that when perception changed the class of an object, the system "no
   longer considered the tracking history of that object when generating a
   new trajectory". With the history thrown away at every new class, the
   system had no path for her across the road. It saw an emergency only when she was in the vehicle's path, 1.2 s
   before impact. See the Introduction in :doc:`l8_lecture`.


.. admonition:: Question 20
   :class: hint

   Explain why predicting car B needs car A's prediction, and why
   predicting car A needs the AV's plan. Use the lecture's numbers.

.. dropdown:: Answer
   :class-container: sd-border-success

   Car B follows A: A brakes for its turn, so B must slow too, until A
   leaves its lane. CV keeps B at 7.76 m/s and ends 3.55 m off; the IDM,
   following A's most likely future, ends 0.92 m off. Car A turns across
   the AV's lane only with a gap of at least 4.1 s. In run 1 the gap is
   6.0 s and A turns; in run 2, with the AV 24 m closer, it is 3.0 s and A
   waits. Ignoring the AV, the left mode ends 18.31 m off; with the gap
   rule, 0.86 m. So the AV's own plan changes what A does, and planners
   either alternate (predict, plan, predict again) or solve both together.
   See Other Drivers in :doc:`l8_lecture`.
