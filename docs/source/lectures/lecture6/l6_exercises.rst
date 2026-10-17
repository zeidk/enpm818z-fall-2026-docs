====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises built on the Lecture 6 notes, :doc:`l6_lecture`, and
on the same recorded CARLA drive. They use only the lecture, never
:doc:`Going Further <l6_appendix>`. Exercises 1 to 5 are paper and arithmetic:
dead reckoning and its drift, the absolute pose error (APE) and the eight runs,
ICP's step 2 by hand, weighing and resampling in MCL, and a pose graph with one
loop. Exercise 6 runs the hands-on in :doc:`l6_code`.

.. note::

   Exercises 1 to 5 can be done with a calculator, but you will learn more by
   writing ten lines of NumPy and checking your arithmetic against it. They
   need no CARLA.

   **Frames.** As in the lecture, the map frame has :math:`x` east and
   :math:`y` north, in meters. The vehicle frame has :math:`x` forward and
   :math:`y` left. The pose :math:`(x, y, \theta)` puts the vehicle frame in
   the map frame, with :math:`\theta` counterclockwise from east.

   **The drive** (errors chosen for the lecture): GNSS once a second with
   noise :math:`\sigma = 1.5` m and a bias of 0.5 m east and 0.3 m south, no
   fixes for 400 m; wheels 0.5% fast; gyro bias 0.001 rad/s. Numbers that
   are not the lecture's are marked "chosen for this exercise".

   None of these exercises builds the filter itself. How the EKF's matrices
   are built for this car is GP3, Task 2.


.. dropdown:: Exercise 1. Dead Reckoning and Its Drift
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run one dead-reckoning step by hand, then size the two drifts of the
   lecture: a fixed heading error, which grows with distance, and a gyro
   bias, which grows with the square of time.

   .. raw:: html

      <hr>

   **Part A. One step**

   Every :math:`\Delta t`, dead reckoning adds
   :math:`x \mathrel{+}= v\cos\theta\,\Delta t`,
   :math:`y \mathrel{+}= v\sin\theta\,\Delta t` and
   :math:`\theta \mathrel{+}= \omega\,\Delta t`. The AV is at
   :math:`(0, 0)` facing :math:`\theta = 30^\circ`, with :math:`v = 10` m/s
   from the wheels and :math:`\omega = 0.2` rad/s from the gyro (all chosen
   for this exercise). :math:`\Delta t = 0.05` s, as on the drive.

   1. Compute the pose after one step.

   .. raw:: html

      <hr>

   **Part B. A fixed heading error**

   The AV believes it faces :math:`1.5^\circ` off its true heading (chosen
   for this exercise) and drives straight.

   2. Convert :math:`1.5^\circ` to radians, and compute its sine.
   3. How far sideways is the AV after 50 m, 100 m and 200 m?
   4. How far can it drive before it leaves the local-street bound of
      0.29 m?
   5. What is the largest heading error that keeps the AV under 0.29 m after
      100 m?

   .. raw:: html

      <hr>

   **Part C. A gyro bias**

   The AV drives straight at :math:`v = 15` m/s with a gyro bias
   :math:`b = 0.002` rad/s (both chosen for this exercise: twice the
   drive's bias).

   6. Compute the heading error :math:`b\,t` after 10 s, 20 s and 40 s, in
      radians and in degrees.
   7. Compute the sideways error :math:`v\,b\,t^2/2` at the same times. What
      happens when the time doubles?
   8. How long after the last fix does the AV leave the 0.29 m bound?

   .. raw:: html

      <hr>

   **Part D. The drive**

   9. The wheels read 0.5% fast. How far off along the road does that put
      dead reckoning after the 400 m outage?
   10. The outage lasts 54.8 s. How large does the drive's gyro bias,
       0.001 rad/s, make the heading error by its end? Compare it with the
       measured heading error at the end of the outage, :math:`6.0^\circ`.
       Then compute :math:`v\,b\,t^2/2` with the drive's mean speed,
       7.3 m/s, and compare it with the measured worst error, 9.03 m.

   .. raw:: html

      <hr>

   **Deliverable**

   The pose after one step, a table of sideways error against distance for
   Part B and against time for Part C, and two sentences on why a heading
   error matters more than a speed error.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`\cos 30^\circ = 0.866` and
      :math:`\sin 30^\circ = 0.5`.

      1. :math:`x = 0 + 10 \times 0.866 \times 0.05 = 0.433` m.
      2. :math:`y = 0 + 10 \times 0.5 \times 0.05 = 0.250` m.
      3. :math:`\theta = 30^\circ + 0.2 \times 0.05` rad
         :math:`= 30^\circ + 0.01` rad :math:`= 30^\circ + 0.57^\circ =
         30.57^\circ`.

      Question 2: :math:`1.5 \times \pi / 180 = 0.02618` rad, and
      :math:`\sin 1.5^\circ = 0.02618`. For small angles the sine and the
      angle in radians are almost the same.

      Question 3: sideways error :math:`= d \sin(\text{heading error})`.

      .. list-table::
         :widths: 40 60
         :header-rows: 1
         :class: compact-table

         * - **Distance driven**
           - **Sideways error**
         * - 50 m
           - :math:`50 \times 0.02618 = 1.31` m
         * - 100 m
           - :math:`100 \times 0.02618 = 2.62` m
         * - 200 m
           - :math:`200 \times 0.02618 = 5.24` m

      Twice the distance, twice the error: a straight line, as in the
      lecture's graph.

      Question 4: :math:`0.29 / 0.02618 = 11.1` m. The bound is used up in
      less than a block.

      Question 5: :math:`\sin(\text{heading error}) = 0.29 / 100 = 0.0029`,
      so the heading error is 0.0029 rad, :math:`0.17^\circ`.

      Questions 6 and 7:

      .. list-table::
         :widths: 25 40 35
         :header-rows: 1
         :class: compact-table

         * - **Time since the fix**
           - **Heading error** :math:`b\,t`
           - **Sideways error** :math:`v\,b\,t^2/2`
         * - 10 s
           - 0.02 rad, :math:`1.15^\circ`
           - :math:`15 \times 0.002 \times 10^2 / 2 = 1.5` m
         * - 20 s
           - 0.04 rad, :math:`2.29^\circ`
           - :math:`15 \times 0.002 \times 20^2 / 2 = 6.0` m
         * - 40 s
           - 0.08 rad, :math:`4.58^\circ`
           - :math:`15 \times 0.002 \times 40^2 / 2 = 24.0` m

      Twice the time, four times the error. A program that applies the
      lecture's rule to the same straight drive every 0.05 s (move, then
      turn) gives 1.49 m, 5.98 m and 23.96 m: the formula is close.

      Question 8: set :math:`v\,b\,t^2/2 = 0.29`, so
      :math:`t^2 = 2 \times 0.29 / (15 \times 0.002) = 0.58 / 0.03 = 19.3`
      and :math:`t = 4.4` s.

      Question 9: :math:`0.005 \times 400 = 2.0` m, along the road. That
      error does not grow faster than the distance, and it does not push the
      AV out of its lane.

      Question 10: :math:`0.001 \times 54.8 = 0.0548` rad, :math:`3.14^\circ`.
      The measured :math:`6.0^\circ` is about twice that: the lecture says
      CARLA's own gyro reads a little more turning than the AV makes in a
      turn, so most of the heading error comes at the corners. The formula
      gives :math:`7.3 \times 0.001 \times 54.8^2 / 2 = 11.0` m, against
      9.03 m measured. The formula assumes a straight road at a constant
      speed. The route turns, and after a corner the old sideways error
      points along the new road, so the two paths can cross and the measured
      error does not follow the formula. Both say the same thing: meters of
      error, against a bound of 0.29 m.

      For the sentences: a speed error stretches the path along the road,
      and grows only with the distance. A heading error pushes the AV
      sideways, toward the next lane, and a gyro bias makes the heading
      error itself grow, so the sideways error grows with the square of
      time.


.. dropdown:: Exercise 2. The Absolute Pose Error, and the Eight Runs
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compute the APE of a run by hand, see what the RMSE adds to a plain
   average, and read the lecture's eight runs.

   .. raw:: html

      <hr>

   **Part A. Two runs with the same average**

   The APE of a run is the RMSE of the distances from the estimated
   position to the true one, one per time step: square, average, take the
   root. Two runs of five time steps have these distances (chosen for this
   exercise):

   - Run A: 0.2, 0.5, 0.3, 1.6, 0.4 m.
   - Run B: 0.6, 0.6, 0.6, 0.6, 0.6 m.

   1. Compute the plain average of each run.
   2. Compute the APE of each run, in numbered steps.
   3. Which run would you rather ride in? Which number tells them apart?

   .. raw:: html

      <hr>

   **Part B. The eight runs**

   The lecture ran the fused filter eight times on the drive: with the GNSS
   outage or with GNSS always, with or without the wheel speed, with or
   without map matching. The table gives each run's APE, as on the slides,
   and its worst error, as the title of the hands-on window prints it
   (:doc:`l6_code`).

   .. list-table::
      :widths: 18 18 16 24 24
      :header-rows: 1
      :class: compact-table

      * - **GNSS**
        - **Wheels**
        - **Map**
        - **APE RMSE (m)**
        - **Worst (m)**
      * - outage
        - yes
        - no
        - 4.99
        - 9.50
      * - outage
        - yes
        - yes
        - 0.52
        - 2.49
      * - outage
        - no
        - no
        - 4.58
        - 12.36
      * - outage
        - no
        - yes
        - 27.66
        - 65.62
      * - always
        - yes
        - no
        - 1.28
        - 2.61
      * - always
        - yes
        - yes
        - 0.47
        - 2.38
      * - always
        - no
        - no
        - 1.97
        - 5.93
      * - always
        - no
        - yes
        - 1.38
        - 6.81

   4. Which input lowers the APE the most? Give the two pairs of runs that
      show it, and by what factor each one drops.
   5. Compare the two outage runs with no map. By APE, which is better, the
      one with wheels or the one without? By the worst error? What does one
      number per run hide?
   6. Look at the two runs with GNSS always and no wheels. What does the
      map do to the APE, and to the worst error?
   7. The run "outage, no wheels, map" has the worst APE of the eight.
      Explain why, with the lecture's timeline of that run.
   8. Why can we compute APE on the drive, and why can a real AV not?

   .. raw:: html

      <hr>

   **Deliverable**

   The two APEs with their steps, and a sentence for each of questions 4 to
   8.

   .. dropdown:: Guidance
      :color: success

      Question 1: Run A,
      :math:`(0.2 + 0.5 + 0.3 + 1.6 + 0.4)/5 = 3.0/5 = 0.60` m. Run B,
      0.60 m. The same average.

      Question 2: Run A:

      1. Square: 0.04, 0.25, 0.09, 2.56, 0.16.
      2. Average: :math:`(0.04 + 0.25 + 0.09 + 2.56 + 0.16)/5 = 3.10/5 =
         0.62`.
      3. Root: :math:`\sqrt{0.62} = 0.79` m.

      Run B:

      1. Square: 0.36 each.
      2. Average: :math:`1.80/5 = 0.36`.
      3. Root: :math:`\sqrt{0.36} = 0.60` m.

      Question 3: Run B. Run A has one step 1.6 m off, more than five times
      the 0.29 m bound, and that is the step that puts a car in the next
      lane. The averages are equal; the RMSE, 0.79 m against 0.60 m, tells
      them apart because squaring weighs the bad step more. When every
      distance is the same, as in Run B, the RMSE equals the average.

      Question 4: the map. Through the outage with wheels, 4.99 m becomes
      0.52 m, :math:`4.99/0.52 = 9.6` times lower. With GNSS always and
      wheels, 1.28 m becomes 0.47 m, :math:`1.28/0.47 = 2.7` times lower.

      Question 5: by APE, the run without wheels looks better, 4.58 m
      against 4.99 m. By the worst error it is worse, 12.36 m against 9.50
      m. The RMSE averages over the whole run; a run can score a lower RMSE
      and still have a worse moment. Read both numbers.

      Question 6: the map lowers the APE from 1.97 m to 1.38 m, but the
      worst error rises from 5.93 m to 6.81 m. Again, one number per run
      does not tell the whole story.

      Question 7: from 35 s to 44 s of the outage, ICP matches the scan to
      the map every second, the match passes the checks, and the filter uses
      it. At 45 s a match is thrown out: it puts the AV too far from where
      the filter expected it. At 46 s the next one is thrown out too: the
      scan does not line up well with the map. With no wheel speed and no
      GNSS, nothing tells the filter how far the AV moves, so from 46.5 s it
      is too unsure to give ICP a good start, and ICP is no longer run. The
      filter knows only how the AV turns and is 65.6 m off at 79.2 s, until
      GNSS returns at 89.0 s. ICP keeps the AV located only while it starts
      from a good guess.

      Question 8: APE needs the true position at every step. CARLA knows it;
      a real AV never does. On the road the AV has to judge its pose without
      the truth, for example by comparing GNSS with map matching and by
      checking each match against the filter's prediction.


.. dropdown:: Exercise 3. ICP Step 2 by Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run step 2 of the ICP loop, the best turn and shift for a set of pairs,
   with the six steps of the lecture's slide "ICP step 2 in general", on new
   numbers.

   .. raw:: html

      <hr>

   **Specification**

   Three scan points :math:`p_i`, in the vehicle frame, and three map points
   :math:`q_i`, in the map frame, already paired :math:`p_i \to q_i` (all
   chosen for this exercise):

   .. list-table::
      :widths: 20 40 40
      :header-rows: 1
      :class: compact-table

      * - **Pair**
        - **Scan point** :math:`p_i`
        - **Map point** :math:`q_i`
      * - 1
        - (5, 0)
        - (6, 3)
      * - 2
        - (0, 5)
        - (-1, 2)
      * - 3
        - (-5, -5)
        - (4, -8)

   The scan points are not on one line. Step 3 builds
   :math:`H = \sum_i p_i'\,q_i'^{\top}`, a :math:`2 \times 2` matrix, so
   :math:`H_{11} = \sum p_x' q_x'`, :math:`H_{12} = \sum p_x' q_y'`,
   :math:`H_{21} = \sum p_y' q_x'` and :math:`H_{22} = \sum p_y' q_y'`.

   .. raw:: html

      <hr>

   **Part A. The six steps**

   1. **Centroids:** compute :math:`\bar p` and :math:`\bar q`.
   2. **Center:** compute :math:`p_i' = p_i - \bar p` and
      :math:`q_i' = q_i - \bar q`.
   3. **Compare:** compute the four entries of :math:`H`, each as a sum
      over the three pairs.
   4. **Angle:** compute
      :math:`\alpha = \operatorname{atan2}(H_{12} - H_{21},\ H_{11} + H_{22})`.
   5. **Turn:** write the rotation matrix :math:`R` of that angle.
   6. **Shift:** compute :math:`t = \bar q - R\,\bar p`.

   .. raw:: html

      <hr>

   **Part B. Check and read the answer**

   7. Move all three scan points with :math:`R\,p_i + t`. Where do they land?
   8. The scan points are in the vehicle frame. What pose
      :math:`(x, y, \theta)` of the AV puts this scan on top of the map?

   .. raw:: html

      <hr>

   **Part C. Two variations**

   9. Add :math:`(1, 1)` to every scan point, keep the map points, and redo
      the six steps. What changes, and what does not?
   10. Suppose you build :math:`H` the wrong way round,
       :math:`\sum_i q_i'\,p_i'^{\top}`. What angle does step 4 give, and
       what does that rotation do?

   .. raw:: html

      <hr>

   **Deliverable**

   The six steps with the arithmetic, the three moved points, the AV's
   pose, and a sentence each for questions 9 and 10.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`\bar p = \big((5 + 0 - 5)/3,\ (0 + 5 - 5)/3\big) =
      (0, 0)`, and :math:`\bar q = \big((6 - 1 + 4)/3,\ (3 + 2 - 8)/3\big) =
      (9/3,\ -3/3) = (3, -1)`.

      Question 2: :math:`p_i' = p_i`, unchanged. :math:`q_1' = (6 - 3,\ 3 + 1)
      = (3, 4)`, :math:`q_2' = (-1 - 3,\ 2 + 1) = (-4, 3)` and
      :math:`q_3' = (4 - 3,\ -8 + 1) = (1, -7)`.

      Question 3:

      - :math:`H_{11} = 5 \cdot 3 + 0 \cdot (-4) + (-5) \cdot 1 = 15 + 0 - 5
        = 10`.
      - :math:`H_{12} = 5 \cdot 4 + 0 \cdot 3 + (-5) \cdot (-7) = 20 + 0 + 35
        = 55`.
      - :math:`H_{21} = 0 \cdot 3 + 5 \cdot (-4) + (-5) \cdot 1 = 0 - 20 - 5
        = -25`.
      - :math:`H_{22} = 0 \cdot 4 + 5 \cdot 3 + (-5) \cdot (-7) = 0 + 15 + 35
        = 50`.

      .. math::

         H = \begin{pmatrix} 10 & 55 \\ -25 & 50 \end{pmatrix}

      Question 4: :math:`H_{12} - H_{21} = 55 - (-25) = 80` and
      :math:`H_{11} + H_{22} = 10 + 50 = 60`, so
      :math:`\alpha = \operatorname{atan2}(80, 60) = 53.13^\circ`.

      Question 5: the two numbers are 80 and 60, and
      :math:`\sqrt{80^2 + 60^2} = 100`, so
      :math:`\cos\alpha = 60/100 = 0.6` and :math:`\sin\alpha = 80/100 = 0.8`:

      .. math::

         R = \begin{pmatrix} 0.6 & -0.8 \\ 0.8 & 0.6 \end{pmatrix}

      Question 6: :math:`t = (3, -1) - R\,(0, 0) = (3, -1)`.

      Question 7:

      - :math:`R\,p_1 = (0.6 \times 5,\ 0.8 \times 5) = (3, 4)`, plus
        :math:`t`: :math:`(6, 3) = q_1`.
      - :math:`R\,p_2 = (-0.8 \times 5,\ 0.6 \times 5) = (-4, 3)`, plus
        :math:`t`: :math:`(-1, 2) = q_2`.
      - :math:`R\,p_3 = (-3 + 4,\ -4 - 3) = (1, -7)`, plus :math:`t`:
        :math:`(4, -8) = q_3`.

      All three land on their map points. The pairs were built from an exact
      rotation and shift, so the fit is perfect. On the AV the pairs come
      from nearest neighbors, so they are partly wrong at first, and the loop
      repeats.

      Question 8: :math:`R` and :math:`t` move points from the vehicle frame
      into the map frame, so they are the AV's pose: :math:`x = 3` m,
      :math:`y = -1` m, :math:`\theta = 53.13^\circ`.

      Question 9: :math:`\bar p` becomes :math:`(1, 1)`, but the centered
      points :math:`p_i'` are the same as before, so :math:`H` and
      :math:`\alpha = 53.13^\circ` do not change. The shift does:
      :math:`R\,\bar p = (0.6 - 0.8,\ 0.8 + 0.6) = (-0.2, 1.4)`, so
      :math:`t = (3 - (-0.2),\ -1 - 1.4) = (3.2, -2.4)`. Centering in step 2
      keeps the turn separate from the shift; step 6 then puts the shift
      back.

      Question 10: the swapped matrix is :math:`H` turned over its diagonal,
      so :math:`H_{12}` and :math:`H_{21}` trade places:
      :math:`\operatorname{atan2}(-25 - 55,\ 60) = \operatorname{atan2}(-80,
      60) = -53.13^\circ`. That rotation turns the map onto the scan, the
      opposite of what you want. The order in :math:`p_i'\,q_i'^{\top}`
      matters.


.. dropdown:: Exercise 4. Weigh and Resample in MCL
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run MCL's weigh, normalize and resample steps by hand on four particles,
   with the lecture's score and its rule for when to resample.

   .. raw:: html

      <hr>

   **Specification**

   Each scan point is placed in the map frame with a particle's pose and
   scored by the lecture's likelihood field, with our code's values:

   .. math::

      p(d) = 0.9\, e^{-d^2/2} + 0.1/3

   where :math:`d` is the distance from the scan point to the nearest map
   point. Past :math:`d_\text{max} = 3` m, the first term is 0, so the score
   is only :math:`0.1/3 = 0.033`.

   Four particles A, B, C and D start with equal weights. One scan of three
   points gives these distances (all chosen for this exercise):

   .. list-table::
      :widths: 25 25 25 25
      :header-rows: 1
      :class: compact-table

      * - **Particle**
        - **Point 1 (m)**
        - **Point 2 (m)**
        - **Point 3 (m)**
      * - A
        - 0.2
        - 0.0
        - 0.4
      * - B
        - 0.8
        - 1.1
        - 0.6
      * - C
        - 1.5
        - 2.2
        - 3.4
      * - D
        - 0.5
        - 0.7
        - 0.9

   Our code resamples only when
   :math:`N_\text{eff} = 1 / \sum_i w_i^2` is below :math:`N/2`, and it
   resamples by the lecture's systematic method: :math:`N` pointers at
   :math:`(r + k)/N`, :math:`k = 0, \dots, N-1`, on a bar where the weights
   lie end to end.

   .. raw:: html

      <hr>

   **Part A. The first scan**

   1. Score every point. Which point scores only the floor, and why?
   2. Multiply each particle's three scores.
   3. Normalize: divide each product by their sum.
   4. Compute :math:`N_\text{eff}`. Does MCL resample after this scan?

   .. raw:: html

      <hr>

   **Part B. The second scan**

   The AV drives on, and the next scan gives each particle the same three
   distances as before (chosen for this exercise, to keep the arithmetic
   short).

   5. Multiply each weight from question 3 by the particle's product from
      question 2, and normalize again.
   6. Compute :math:`N_\text{eff}`. Does MCL resample now?
   7. Resample with the random start :math:`r = 0.3` (chosen for this
      exercise). Where are the four pointers, and how many copies does each
      particle get? Compare with :math:`N` times each weight.

   .. raw:: html

      <hr>

   **Part C. Why the floor**

   8. A parked car that the map does not have stands next to the AV. A's
      third point hits it and lands 3.5 m from the nearest map point, so A's
      distances are 0.2, 0.0 and 3.5 m. Compute A's product with the floor,
      and without it (score :math:`0.9\,e^{-d^2/2}` up to 3 m, 0 past it).
      What does one such point do to a good particle without the floor?

   .. raw:: html

      <hr>

   **Deliverable**

   The table of scores, the weights after each scan, both
   :math:`N_\text{eff}` with their verdicts, the copies after resampling,
   and a sentence on what the floor is for.

   .. dropdown:: Guidance
      :color: success

      Question 1: the scores, rounded to 4 decimals:

      .. list-table::
         :widths: 20 20 20 20 20
         :header-rows: 1
         :class: compact-table

         * - **Particle**
           - **Point 1**
           - **Point 2**
           - **Point 3**
           - **Product**
         * - A
           - 0.9155
           - 0.9333
           - 0.8641
           - 0.7384
         * - B
           - 0.6869
           - 0.5248
           - 0.7851
           - 0.2830
         * - C
           - 0.3255
           - 0.1134
           - 0.0333
           - 0.0012
         * - D
           - 0.8276
           - 0.7378
           - 0.6336
           - 0.3869

      For example, A's first point:
      :math:`0.9 \times e^{-0.2^2/2} + 0.0333 = 0.9 \times 0.9802 + 0.0333
      = 0.9155`. C's third point, 3.4 m away, is past 3 m, so it scores only
      the floor, 0.0333.

      Question 2: the last column of the table.

      Question 3: the sum is
      :math:`0.7384 + 0.2830 + 0.0012 + 0.3869 = 1.4095`. Weights:
      A :math:`0.7384 / 1.4095 = 0.524`, B 0.201, C 0.001, D 0.274.

      Question 4:

      1. Square each weight: 0.2744, 0.0403, 0.0000, 0.0753.
      2. Add them: 0.3901.
      3. :math:`N_\text{eff} = 1 / 0.3901 = 2.56`.
      4. The cutoff is :math:`N/2 = 4/2 = 2`. 2.56 is above it: no
         resampling yet. The weights carry over to the next scan.

      Question 5: products of weight and score: A
      :math:`0.524 \times 0.7384 = 0.3868`, B 0.0568, C 0.0000, D 0.1062.
      Their sum is 0.5498, so the weights are A 0.704, B 0.103, C 0.000,
      D 0.193.

      Question 6: :math:`0.704^2 + 0.103^2 + 0.000^2 + 0.193^2 = 0.495 +
      0.011 + 0.000 + 0.037 = 0.543`, so :math:`N_\text{eff} = 1/0.543 =
      1.84`. That is below 2: MCL resamples.

      Question 7: the pointers are at :math:`0.3/4 = 0.075`,
      :math:`1.3/4 = 0.325`, :math:`2.3/4 = 0.575` and
      :math:`3.3/4 = 0.825`. On the bar, A covers 0 to 0.704, B 0.704 to
      0.807, C a sliver at 0.807, and D 0.807 to 1. The first three pointers
      land in A, the last in D: A gets 3 copies, D 1, B and C none. On
      average a particle gets :math:`N` times its weight: A 2.81, B 0.41,
      C 0.00, D 0.77. The random start rounds these to whole copies, and here
      B, with 0.41, gets none. After resampling every weight is
      :math:`1/4` again.

      Question 8: with the floor, A's scores are 0.9155, 0.9333 and 0.0333,
      and the product is 0.0285, about 26 times smaller than its 0.7384
      before. Without the floor the third score is 0, so the product is 0: one
      point that hits something the map lacks wipes out the best particle,
      whatever its other points say. The floor keeps that from happening.


.. dropdown:: Exercise 5. A Pose Graph with One Loop
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Find the gap a loop closure reveals, and share it out over the edges by
   the lecture's rule for one loop.

   .. raw:: html

      <hr>

   **Specification**

   Three positions :math:`p_1`, :math:`p_2`, :math:`p_3`, with
   :math:`p_1 = (0, 0)`. Two odometry edges and one loop closure, measured
   as moves in the map frame (all chosen for this exercise):

   .. list-table::
      :widths: 30 35 35
      :header-rows: 1
      :class: compact-table

      * - **Edge**
        - **Measured move (m)**
        - :math:`\sigma` **(m)**
      * - odometry :math:`p_1 \to p_2`
        - (15.0, 0.2)
        - 0.2
      * - odometry :math:`p_2 \to p_3`
        - (-4.0, 10.0)
        - 0.2
      * - loop closure :math:`p_3 \to p_1`
        - (-10.1, -9.75)
        - 0.1

   The lecture's rule for one loop: **each edge takes a share of the gap in
   proportion to its variance** :math:`\sigma^2`.

   .. raw:: html

      <hr>

   **Part A. The gap and its shares**

   1. Place :math:`p_2` and :math:`p_3` from odometry alone.
   2. Add the three edges around the loop. What is the gap, and how long is
      it?
   3. Compute each edge's variance, the total, and each edge's share.
   4. Move :math:`p_2` back by its edge's share of the gap. Then compute
      :math:`p_3`: it moves once for each odometry edge.
   5. Check: how far does the corrected :math:`p_3` miss the loop closure?
      Compare with the loop's share of the gap.

   .. raw:: html

      <hr>

   **Part B. A poor loop closure**

   6. The scan match behind the loop closure was poor, and its
      :math:`\sigma` is 0.4 m instead (chosen for this exercise). Redo
      questions 3 and 4. Which edge bends most now?

   .. raw:: html

      <hr>

   **Deliverable**

   The gap, the shares, the corrected positions in both parts, and one
   sentence on which edge takes the correction, and why.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`p_2 = (15.0, 0.2)` and
      :math:`p_3 = (15.0 - 4.0,\ 0.2 + 10.0) = (11.0, 10.2)`.

      Question 2: in :math:`x`, :math:`15.0 - 4.0 - 10.1 = 0.9`; in
      :math:`y`, :math:`0.2 + 10.0 - 9.75 = 0.45`. A perfect loop would add
      up to :math:`(0, 0)`, so the gap is :math:`(0.9, 0.45)`, and its length
      is :math:`\sqrt{0.9^2 + 0.45^2} = 1.01` m.

      Question 3:

      1. Variances: :math:`0.2^2 = 0.04` for each odometry edge,
         :math:`0.1^2 = 0.01` for the loop. Total:
         :math:`0.04 + 0.04 + 0.01 = 0.09`.
      2. Shares: :math:`0.04/0.09 = 0.44` for each odometry edge,
         :math:`0.01/0.09 = 0.11` for the loop. The three shares add up to 1.

      Question 4: each odometry edge gives up
      :math:`0.44 \times (0.9, 0.45) = (0.40, 0.20)`.

      1. :math:`p_2 = (15.0, 0.2) - (0.40, 0.20) = (14.60, 0.00)`.
      2. :math:`p_3 = p_2 + (-4.0, 10.0) - (0.40, 0.20) = (10.20, 9.80)`.

      :math:`p_3` moved :math:`(0.80, 0.40)` from its odometry place, twice
      the share of one edge.

      Question 5: :math:`p_1 - p_3 = (-10.20, -9.80)`; the loop closure
      measured :math:`(-10.1, -9.75)`. The miss is :math:`(0.10, 0.05)`, the
      loop's share: :math:`0.11 \times (0.9, 0.45) = (0.10, 0.05)`. A
      least-squares solve of the same graph gives the same positions.

      Question 6:

      1. Variances: 0.04, 0.04 and :math:`0.4^2 = 0.16`. Total 0.24.
      2. Shares: :math:`0.04/0.24 = 0.17` for each odometry edge and
         :math:`0.16/0.24 = 0.67` for the loop.
      3. Each odometry edge gives up :math:`(0.9, 0.45)/6 = (0.15, 0.075)`.
         :math:`p_2 = (15.0 - 0.15,\ 0.2 - 0.075) = (14.85, 0.125)` and
         :math:`p_3 = (14.85 - 4.0 - 0.15,\ 0.125 + 10.0 - 0.075) =
         (10.70, 10.05)`.

      Now the loop closure bends most: it takes two thirds of the gap. In
      Part A the sure loop closure barely bent and the unsure odometry took
      the correction. The rule always gives the most to the least sure
      edge.


.. dropdown:: Exercise 6. The Hands-on on the Recorded Drive
   :icon: number
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   **Goal**

   Run the lecture's hands-on parts and compare what you see with the
   slides: dead reckoning, the fused filter's eight runs, MCL and ICP.

   .. raw:: html

      <hr>

   **Specification**

   The code is in the course's Python repository, folder ``lecture6``. It
   needs ``numpy``, ``scipy`` and ``matplotlib``, and no CARLA. The commands
   and the options are on :doc:`l6_code`. Add ``--snapshot out.png`` to save
   a still instead of opening a window.

   .. raw:: html

      <hr>

   **Part A. Dead reckoning:** ``python3 l6_handson.py --part dr``

   This part runs dead reckoning through the outage, from the true pose at
   the last fix. Two check boxes hold the errors we chose: **gyro bias** and
   **wheels 0.5 % fast**.

   1. With both ticked, watch the heading error (bottom right). Where does
      it step up: on the straights or at the corners?
   2. Untick **gyro bias**. How much smaller is the worst position error?
      Tick it again and untick **wheels 0.5 % fast**. Which error matters
      more?
   3. Untick both. The heading still ends off. What is left in the signals?

   .. raw:: html

      <hr>

   **Part B. The fused filter:** ``python3 l6_handson.py --part ekf``

   4. Tick and untick **GNSS outage**, **wheels** and **map matching**, and
      write down the APE of each of the eight runs. Compare with Exercise 2.
   5. In the outage, with wheels and no map, does the filter's own
      :math:`1\sigma` (the shaded band) grow as fast as its error (the blue
      line)?
   6. Open the run "outage, no wheels, map". When does its error start to
      grow, how large does it get, and when does it come back?

   .. raw:: html

      <hr>

   **Part C. MCL:** ``python3 l6_handson.py --part mcl``

   MCL computes for about 12 s before its window opens, and prints a line to
   say so.

   7. How long until the error is under 1 m? Watch the spread too: is a
      small spread the same as a small error?
   8. Run ``--particles 200`` with ``--seed`` 0 to 4, then 2000 particles
      with the same seeds. Does every run find the AV? How fast?
   9. Run ``--kidnap 40 0 10`` with seeds 0 to 4: at 40 s every particle
      jumps 10 m north. Does MCL find the AV again? Then ``--kidnap 40 0 30``.
      Then add ``--random 20`` and ``--random 100`` to the first: do random
      particles help?

   .. raw:: html

      <hr>

   **Part D. ICP:** ``python3 l6_handson.py --part icp``

   10. Drag the slider. How many iterations until the RMSE stops falling?
   11. Run ``--icp-start`` with ``3 -2 10``, ``4 -3 15`` and ``6 -4 20`` (east
       and north offsets in meters, then degrees). How far off is each start?
       Which ones still land on the walls?

   .. raw:: html

      <hr>

   **Deliverable**

   One snapshot per part, your numbers next to the reference numbers below,
   and a sentence for each question.

   .. dropdown:: What to expect
      :color: warning

      The reference numbers come from the shipped drive and the default
      seed, 818, unless a seed is named (see :doc:`l6_code`).

      Question 1: at the corners. The heading error ends at
      :math:`+6.0^\circ`; while the gyro reads a turn (faster than 0.1 rad/s,
      about a third of the outage), it grows by :math:`5.8^\circ`, and on the
      straights by :math:`0.15^\circ`. The position error is 2.69 m after
      100 m, at worst 9.03 m (at 329 m), and 7.84 m at the next fix, 401 m
      on.

      Question 2: without the gyro bias, the worst error is 4.33 m instead
      of 9.03 m, and the heading ends :math:`+2.8^\circ` off. Without the
      wheel error (gyro bias back on), the worst error is 9.24 m, a little
      larger than with it. The gyro bias matters far more: the wheel error
      only stretches the path along the road.

      Question 3: with neither error, the worst error is 4.49 m, and the
      heading still ends :math:`+2.8^\circ` off. What is left is the
      sensors' noise and CARLA's own gyro, which reports a little more
      turning than the AV makes in a corner.

      Question 4: the table of Exercise 2: 4.99, 0.52, 4.58 and 27.66 m with
      the outage; 1.28, 0.47, 1.97 and 1.38 m with GNSS always. The map
      lowers the APE most. The window's title rounds two of them the other
      way, 0.51 and 27.67 m: the stored values are 0.515 and 27.665 m.

      Question 5: no. With wheels and no map, the filter's :math:`1\sigma`
      is 3.93 m at the outage's worst moment, where the real error is
      9.50 m, and the error stays above the band the whole outage: the
      filter is overconfident.

      Question 6: ICP is used from 35 s to 44 s. Two matches are thrown out at 45 s and 46 s, and from 46.5 s ICP
      is no longer run. The error grows to 65.6 m at about 79.2 s, the worst
      of all eight runs, and GNSS brings it back at 89.0 s (Exercise 2,
      question 7).

      Question 7: the error is first under 1 m at the 5th scan, 2.0 s after
      the first scan. After the first 10 s its median is 0.20 m and its worst
      0.95 m. The spread is under 0.31 m from the first scan on, even while
      the error is 3.06 m: the first scan already puts almost all the weight on
      very few particles. A small spread says the particles agree, not that
      they are on the AV.

      Question 8: every run finds the AV in the end, but not equally fast.
      With 200 particles, seeds 1 and 4 stay 5 to 10 m off until 64.0 s and
      60.5 s. With 2000, every run is within 2 m of the AV by 33.5 s. After
      70 s, all ten runs reach 0.80 to 1.11 m at worst, with 200 or 2000:
      more particles help to find the AV, not once it is found.

      Question 9: seconds after the jump until the error is first under 1 m,
      seeds 0 to 4:

      .. list-table::
         :widths: 45 55
         :header-rows: 1
         :class: compact-table

         * - **Run**
           - **Seeds 0 to 4**
         * - ``--kidnap 40 0 10``
           - 21.6, 16.6, 16.6, 45.1, 10.6
         * - ``--kidnap 40 0 30``
           - never, 72.1, never, never, never
         * - ``--kidnap 40 0 10 --random 20``
           - 4.6, never, 21.1, 6.1, never
         * - ``--kidnap 40 0 10 --random 100``
           - 3.6, 11.1, 2.6, 1.6, 10.1

      A 10 m jump heals by itself on this drive; a 30 m jump mostly does
      not. Random particles can speed the return, but with 20 per scan two
      runs never come back: seed 1 ends 29.8 m off and seed 4 73.4 m off.
      From 50 s of the drive on, their median error is 101 m and 64 m while
      their median spread is 0.38 m and 0.28 m, as the lecture says.

      Question 10: the default start is :math:`5^\circ` off, 1.5 m east and
      1.0 m south. ICP takes 28 iterations; the RMSE of the pairs falls from
      1.32 m to 0.06 m, and the final pose is 0.02 m and :math:`0.02^\circ`
      from the truth.

      Question 11: ``3 -2 10`` starts :math:`\sqrt{3^2 + 2^2} = 3.6` m and
      :math:`10^\circ` off; ``4 -3 15`` starts 5 m and :math:`15^\circ` off;
      ``6 -4 20`` starts 7.2 m and :math:`20^\circ` off. All three stop at
      the 30-round limit. The first ends 0.02 m off and the second 0.10 m
      off. The last ends 7.09 m and :math:`16.6^\circ` off, on the wrong
      walls, with an RMSE still at 1.53 m. ICP needs a good starting guess,
      which is why the filter's own pose starts it, and why a lost AV needs
      MCL.
