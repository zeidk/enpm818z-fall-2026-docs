====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises built on the Lecture 6 slides shown in class, and on
the same recorded CARLA drive. Exercises 1 to 5 are paper and arithmetic: dead
reckoning and its drift, the absolute pose error (APE) and the eight runs, one
ICP fit by hand, the NIS gate, and a pose graph with one loop. Exercise 6 runs
four of the five parts of the hands-on in :doc:`l6_code`.

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
      0.29 m? And the freeway's sideways bound of 0.57 m?
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
       0.001 rad/s, make the heading error by its end? Compute
       :math:`v\,b\,t^2/2` with the drive's mean speed, 7.3 m/s, and compare
       it with the measured worst error, 9.03 m.

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

      Question 4: :math:`0.29 / 0.02618 = 11.1` m on a local street, and
      :math:`0.57 / 0.02618 = 21.8` m on a freeway. The budget is gone in
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

      Twice the time, four times the error. A program that integrates the
      same straight drive in steps of 0.05 s gives 1.51 m, 6.01 m and
      24.02 m: the formula is close.

      Question 8: set :math:`v\,b\,t^2/2 = 0.29`, so
      :math:`t^2 = 2 \times 0.29 / (15 \times 0.002) = 0.58 / 0.03 = 19.3`
      and :math:`t = 4.4` s.

      Question 9: :math:`0.005 \times 400 = 2.0` m, along the road. That
      error does not grow faster than the distance, and it does not push the
      AV out of its lane.

      Question 10: :math:`0.001 \times 54.8 = 0.0548` rad, :math:`3.14^\circ`.
      The formula gives :math:`7.3 \times 0.001 \times 54.8^2 / 2 = 11.0` m,
      against 9.03 m measured. The formula assumes a straight road at a
      constant speed. The route turns, and the lecture's plot shows the two
      paths crossing again at some corners, so the measured error does not
      follow the formula. Both say the same thing: meters of error, against
      a bound of 0.29 m.

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

   The hands-on ran the fused filter eight times on the drive: with the GNSS
   outage or with GNSS always, with or without the wheels, with or without
   map matching. The table gives each run's APE and its worst error, from
   :doc:`l6_code`.

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
        - 2.62
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
   8. Why can we compute APE on the drive, and why can a real car not?

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

      Question 7: for ten seconds of the outage, 35 s to 44 s, ICP gives one
      pose per second, all accepted. At 45 s the NIS gate rejects one match,
      and at 46 s the next fit fails its quality check and is dropped. With
      no wheels and no GNSS, nothing measures the speed, so at 46.5 s the
      filter's position :math:`\sigma` passes 2 m, the limit chosen for
      starting ICP, and ICP stops. The filter coasts on the gyro alone and
      is 65.6 m off at 79.2 s, until GNSS returns at 89.0 s. ICP keeps the
      AV localized only while it has a good starting guess.

      Question 8: APE needs the true position at every step. CARLA knows it;
      a real car never does. That is the Integrity section's problem: the
      car has to judge its pose without the truth.


.. dropdown:: Exercise 3. One ICP Fit by Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run Step 2 of the ICP loop, the best rotation and shift for a set of
   pairs, with the five steps of the lecture, on new numbers.

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

   The scan points are centered (their centroid is the origin) and they are
   not on one line, as in the lecture's example. The cross-covariance is
   :math:`H = \sum_i p_i'\,q_i'^{\top}`, so :math:`H_{11} = \sum p_x' q_x'`,
   :math:`H_{12} = \sum p_x' q_y'`, :math:`H_{21} = \sum p_y' q_x'` and
   :math:`H_{22} = \sum p_y' q_y'`.

   .. raw:: html

      <hr>

   **Part A. The five steps**

   1. **Centroids:** compute :math:`\bar p` and :math:`\bar q`.
   2. **Center:** compute :math:`p_i' = p_i - \bar p` and
      :math:`q_i' = q_i - \bar q`.
   3. **Cross-covariance:** compute the four entries of :math:`H`, each as a
      sum over the three pairs.
   4. **Rotation:** compute
      :math:`\alpha = \operatorname{atan2}(H_{12} - H_{21},\ H_{11} + H_{22})`
      and write :math:`R`.
   5. **Shift:** compute :math:`t = \bar q - R\,\bar p`.

   .. raw:: html

      <hr>

   **Part B. Check and read the answer**

   6. Move all three scan points with :math:`R\,p_i + t`. Where do they land?
   7. The scan points are in the vehicle frame. What pose
      :math:`(x, y, \theta)` of the AV puts this scan on top of the map?

   .. raw:: html

      <hr>

   **Part C. Two variations**

   8. Add :math:`(1, 1)` to every scan point, keep the map points, and redo
      the five steps. What changes, and what does not?
   9. Suppose you build :math:`H` the wrong way round,
      :math:`\sum_i q_i'\,p_i'^{\top}`. What angle does the short form give,
      and what does that rotation do?

   .. raw:: html

      <hr>

   **Deliverable**

   The five steps with the arithmetic, the three moved points, the AV's
   pose, and a sentence each for questions 8 and 9.

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
      :math:`\alpha = \operatorname{atan2}(80, 60) = 53.13^\circ`. The two
      numbers are 80 and 60, and :math:`\sqrt{80^2 + 60^2} = 100`, so
      :math:`\cos\alpha = 60/100 = 0.6` and :math:`\sin\alpha = 80/100 = 0.8`:

      .. math::

         R = \begin{pmatrix} 0.6 & -0.8 \\ 0.8 & 0.6 \end{pmatrix}

      Question 5: :math:`t = (3, -1) - R\,(0, 0) = (3, -1)`.

      Question 6:

      - :math:`R\,p_1 = (0.6 \times 5,\ 0.8 \times 5) = (3, 4)`, plus
        :math:`t`: :math:`(6, 3) = q_1`.
      - :math:`R\,p_2 = (-0.8 \times 5,\ 0.6 \times 5) = (-4, 3)`, plus
        :math:`t`: :math:`(-1, 2) = q_2`.
      - :math:`R\,p_3 = (-3 + 4,\ -4 - 3) = (1, -7)`, plus :math:`t`:
        :math:`(4, -8) = q_3`.

      All three land on their map points. The pairs were built from an exact
      rotation and shift, so the fit is perfect. On the car the pairs come
      from nearest neighbors, so they are partly wrong at first, and the loop
      repeats.

      Question 7: :math:`R` and :math:`t` move points from the vehicle frame
      into the map frame, so they are the AV's pose: :math:`x = 3` m,
      :math:`y = -1` m, :math:`\theta = 53.13^\circ`.

      Question 8: :math:`\bar p` becomes :math:`(1, 1)`, but the centered
      points :math:`p_i'` are the same as before, so :math:`H` and
      :math:`\alpha = 53.13^\circ` do not change. The shift does:
      :math:`R\,\bar p = (0.6 - 0.8,\ 0.8 + 0.6) = (-0.2, 1.4)`, so
      :math:`t = (3 - (-0.2),\ -1 - 1.4) = (3.2, -2.4)`. Centering in Step 2
      keeps the rotation separate from the shift; Step 5 then puts the shift
      back.

      Question 9: the swapped matrix is :math:`H` turned over its diagonal,
      so :math:`H_{12}` and :math:`H_{21}` trade places:
      :math:`\operatorname{atan2}(-25 - 55,\ 60) = \operatorname{atan2}(-80,
      60) = -53.13^\circ`. That rotation turns the map onto the scan, the
      opposite of what you want. The order in :math:`p_i'\,q_i'^{\top}`
      matters.


.. dropdown:: Exercise 4. The NIS Gate
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Decide by hand whether the filter accepts an update, with the 0.99
   bounds of the lecture, and see both kinds of mistake the gate makes.

   .. raw:: html

      <hr>

   **Specification**

   L3's test: :math:`\varepsilon = \boldsymbol{\nu}^\top S^{-1}
   \boldsymbol{\nu}`, where :math:`\boldsymbol{\nu}` is the surprise (the
   reading minus what the state predicts) and :math:`S` is the surprise the
   filter expects. In this exercise :math:`S` is given, and its numbers do
   not affect each other (chosen for this exercise), with a standard
   deviation :math:`\sigma` for each number. Then :math:`\varepsilon` is a
   sum with one term per number, the one-number form of L3,
   :math:`\nu^2/S`, added up:

   .. math::

      \varepsilon = \Big(\frac{\nu_1}{\sigma_1}\Big)^2 +
                    \Big(\frac{\nu_2}{\sigma_2}\Big)^2 + \dots

   Reject the update if :math:`\varepsilon` is above **9.21** for a GNSS fix
   (2 numbers, :math:`x` and :math:`y`) or above **11.34** for a matched
   pose (3 numbers, :math:`x`, :math:`y` and :math:`\theta`): the
   chi-square 0.99 bounds.

   .. raw:: html

      <hr>

   **Part A. One GNSS fix, two moments**

   A fix arrives 2.0 m east and 1.5 m south of the filter's predicted
   position: :math:`\boldsymbol{\nu} = (2.0, -1.5)` m (chosen for this
   exercise).

   1. How far is the fix from the prediction?
   2. Before the outage, the filter expects :math:`\sigma = 0.8` m in
      :math:`x` and in :math:`y`. Compute :math:`\varepsilon`. Accept or
      reject?
   3. Just after the outage, :math:`P` is large and the filter expects
      :math:`\sigma = 3.0` m in each. Same fix: compute :math:`\varepsilon`.
      Accept or reject?
   4. With equal :math:`\sigma` in :math:`x` and :math:`y`, the gate is a
      circle of radius :math:`\sqrt{9.21}\,\sigma = 3.03\,\sigma`. Compute it
      for both moments.
   5. Suppose the fix of question 3 is multipath, 2.5 m off. Which mistake
      has the gate made?

   .. raw:: html

      <hr>

   **Part B. Two matched poses**

   ICP's pose arrives with :math:`\sigma = 0.2` m in :math:`x` and in
   :math:`y`, and :math:`1.0^\circ` in :math:`\theta` (chosen for this
   exercise).

   6. Pose 1: :math:`\boldsymbol{\nu} = (0.4 \text{ m},\ -0.3 \text{ m},\
      2.0^\circ)`. Compute :math:`\varepsilon`. Accept or reject?
   7. A programmer uses 9.21 for every update. What happens to pose 1, and
      which mistake is that?
   8. Pose 2: :math:`\boldsymbol{\nu} = (0.1 \text{ m},\ 0.1 \text{ m},\
      4.0^\circ)`. Compute :math:`\varepsilon`. Accept or reject? Which
      number causes it?

   .. raw:: html

      <hr>

   **Part C. The drive's NIS**

   On the run with the outage, wheels and map, the lecture measured: GNSS,
   mean NIS 2.12 over 68 fixes, 1 above 9.21; map poses, mean NIS 2.50 over
   118 poses, 0 above 11.34.

   9. What mean does an honest filter give for each source?
   10. At 0.99, how many updates of each source do you expect above the
       bound, on average? Compare with what was measured.
   11. Is the filter honest about each source? Which side is the map on, and
       is that the safe side?

   .. raw:: html

      <hr>

   **Deliverable**

   Every :math:`\varepsilon` with its arithmetic and its verdict, the two
   gate radii, and two sentences for Part C.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`\sqrt{2.0^2 + 1.5^2} = \sqrt{6.25} = 2.5` m.

      Question 2: :math:`(2.0/0.8)^2 + (1.5/0.8)^2 = 6.25 + 3.52 = 9.77`.
      Above 9.21: **reject**.

      Question 3: :math:`(2.0/3.0)^2 + (1.5/3.0)^2 = 0.44 + 0.25 = 0.69`.
      Far below 9.21: **accept**. The same 2.5 m is a large surprise for a
      filter that expects 0.8 m, and a small one for a filter that expects
      3.0 m.

      Question 4: :math:`3.03 \times 0.8 = 2.43` m before the outage, and
      :math:`3.03 \times 3.0 = 9.10` m just after it. The fix, 2.5 m off,
      is just outside the first circle and well inside the second.

      Question 5: a **missed fault**: a bad update accepted. After the
      outage :math:`P` is large, so :math:`S` is large, and
      :math:`\varepsilon` stays small. The filter moves toward a fix that is
      2.5 m wrong, as in the lecture's example of a multipath fix 3 m off.

      Question 6: :math:`(0.4/0.2)^2 + (0.3/0.2)^2 + (2.0/1.0)^2 = 4 + 2.25
      + 4 = 10.25`. Below 11.34: **accept**.

      Question 7: 10.25 is above 9.21, so the pose is rejected. If the pose
      was right, that is a **false alarm**: a good update rejected. The cost
      is that the filter coasts on dead reckoning a little longer. A pose
      reports 3 numbers, so its bound is 11.34.

      Question 8: :math:`(0.1/0.2)^2 + (0.1/0.2)^2 + (4.0/1.0)^2 = 0.25 +
      0.25 + 16 = 16.5`. Above 11.34: **reject**. The position fits; the
      heading is 4 standard deviations off and alone gives 16.

      Question 9: about 1 per number: 2 for a GNSS fix, 3 for a pose.

      Question 10: about 1 in 100 honest updates lands above the bound:
      :math:`0.01 \times 68 = 0.68` GNSS fixes and
      :math:`0.01 \times 118 = 1.18` map poses. Measured: 1 and 0, both close
      to what an honest filter gives.

      Question 11: GNSS, 2.12 against 2: honest. The map, 2.50 against 3: a
      little below, so the filter slightly overestimates the map's error. It
      is a little underconfident about the map, which is the safe side. An
      overconfident filter would make false alarms; an underconfident one
      misses faults.


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

   Run the lecture's four hands-on parts and compare what you see with the
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

   1. This part runs dead reckoning over the whole drive, from the true pose
      at the start. Find the stretch where the error grows fastest. Is it on
      a straight or in a turn? Explain it with the heading error, not the
      speed error.

   .. raw:: html

      <hr>

   **Part B. The fused filter:** ``python3 l6_handson.py --part ekf``

   2. Tick and untick **GNSS outage**, **wheels** and **map matching**, and
      write down the APE of each of the eight runs. Compare with Exercise 2.
   3. In the outage, with wheels and no map, does the filter's own
      :math:`1\sigma` (grey) grow as fast as its error (blue)?
   4. Open the run "outage, no wheels, map" and its NIS plot. Where does it
      lose the map?

   .. raw:: html

      <hr>

   **Part C. MCL:** ``python3 l6_handson.py --part mcl``

   5. How long until the particles' spread is under 1 m? Where does the
      error rise again, and what does the LiDAR see there?
   6. Run ``--particles 200`` with ``--seed`` 0 to 4. How many runs find the
      car? Compare the median error after the first 10 s with 2000
      particles on the same seeds.

   .. raw:: html

      <hr>

   **Part D. ICP:** ``python3 l6_handson.py --part icp``

   7. Drag the slider. How many iterations until the RMSE stops falling?
      Which walls pull the scan into place first?
   8. Run ``--icp-start`` with ``3 -2 10``, ``4 -3 15`` and ``6 -4 20`` (east
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

      Question 1: ``--part dr`` starts dead reckoning from the true pose at
      the last fix before the outage, as the lecture does, and runs it to the
      next fix, 401 m on. The error is 2.69 m after 100 m, 3.56 m after 200 m,
      8.24 m after 300 m, at worst 9.03 m (at 329 m), and 7.84 m at the next
      fix. It grows fastest from 250 m to 300 m, from 4.59 m to 8.24 m, on the
      straight middle street: the true heading turns less than one degree
      there, and the estimated heading is about :math:`5^\circ` off. On a
      straight, a heading error pushes the AV sideways by the same amount
      every meter: :math:`50 \times \sin 5^\circ = 4.4` m in 50 m. The
      wheels' 0.5% only stretches the path along the road.

      Question 2: the table of Exercise 2: 4.99, 0.52, 4.58 and 27.66 m with
      the outage; 1.28, 0.47, 1.97 and 1.38 m with GNSS always. The map
      lowers the APE most.

      Question 3: no. With wheels and no map, the filter's :math:`1\sigma`
      is 3.93 m at the outage's worst moment, where the real error is
      9.50 m: the filter is overconfident.

      Question 4: the NIS gate rejects one map match at 45 s, the next fit
      is dropped at 46 s, and from 46.5 s the filter's :math:`\sigma` is
      above the 2 m limit for starting ICP. The run stays lost until GNSS
      returns at 89.0 s (Exercise 2, question 7).

      Question 5: with the default seed, the error is first under 1 m at
      the 5th scan, 2.0 s in. After 10 s the median error is 0.20 m and the
      worst 0.95 m. Where the error rises again, count the walls and poles
      in the scan: MCL can place the car only where the scan has something
      distinctive to match, as the box with and without its pillar showed.

      Question 6: all five runs find the car with 200 particles, and all
      five with 2000. Median error after the first 10 s, seeds 0 to 4: 0.29,
      0.78, 0.29, 0.37 and 0.70 m with 200 particles; 0.28, 0.21, 0.27, 0.20
      and 0.34 m with 2000. Fewer particles cover the start more thinly, so
      the answer is less precise.

      Question 7: the default start is :math:`5^\circ` off, 1.5 m east and
      1.0 m south. ICP takes 28 iterations; the RMSE of the pairs falls from
      1.32 m to 0.06 m, and the final pose is 0.02 m and :math:`0.02^\circ`
      from the truth.

      Question 8: ``3 -2 10`` starts :math:`\sqrt{3^2 + 2^2} = 3.6` m and
      :math:`10^\circ` off; ``4 -3 15`` starts 5 m and :math:`15^\circ` off;
      ``6 -4 20`` starts 7.2 m and :math:`20^\circ` off. The first two land
      within 0.10 m of the truth. The last ends 7.09 m off, on the wrong
      walls. ICP needs a good starting guess, which is why the filter's own
      pose starts it, and why a lost AV needs MCL.
