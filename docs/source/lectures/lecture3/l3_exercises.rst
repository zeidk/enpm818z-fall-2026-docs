====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises built on the Lecture 3 slides shown in class, and on
the same running examples: the six GNSS readings of the parked AV, the
50 m / 53 m blend in the tunnel, the landmark at :math:`x = 20` m, and the
two hands-on scripts. Exercises 1 to 4 are paper and arithmetic (one predict
step and one update in the tunnel). Exercise 5 mixes paper (the EKF with the
landmark and the Jacobians) with ``ekf_curve.py``. Exercise 6 uses both
scripts, ``kf_tunnel.py`` and ``ekf_curve.py``, to test whether a filter's
reported uncertainty is honest.

.. important::

   **Exercise 6 is the one that matters.** It is the skill GP3 assumes you
   already have: catching a filter whose reported uncertainty is wrong. Such a
   filter does not crash. It reports a small :math:`\sigma` and keeps running,
   and nothing in the system raises an alarm. Turn :math:`Q` down until the
   filter fails, and watch the share of time inside :math:`1\sigma`, and the
   NIS, catch it. Set aside real time for it.

.. note::

   Exercises 1 to 5 can be done with a calculator, but you will learn more by
   writing ten lines of NumPy and checking your arithmetic against it. Show
   both if you do. The hands-on scripts are in the course code repository,
   folder ``lecture3/``: ``tunnel_kf/kf_tunnel.py`` and
   ``curved_tunnel/ekf_curve.py``. They need Python 3 with ``numpy`` and
   ``matplotlib`` (on Ubuntu 24.04:
   ``sudo apt install python3-numpy python3-matplotlib python3-tk``). Each
   script prints its score in the terminal before it opens the live window.


.. dropdown:: Exercise 1. Variance, Standard Deviation and Covariance
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compute the three numbers that describe a cloud of readings, from the
   class's six GNSS readings, and see what each one can and cannot tell you.

   .. raw:: html

      <hr>

   **Part A. The six readings**

   The AV is parked on a surveyed spot, so its true position is known:
   :math:`(100.0,\ 2.5)` m in the road frame (:math:`x` along the road,
   :math:`y` across it, from the survey marker). Without moving, it asks the
   GNSS receiver for its position six times:

   .. code-block:: text

      (102.1, 1.4)   (98.6, 4.3)   (100.9, 3.1)   (99.2, 1.2)   (101.4, 3.4)   (97.8, 1.6)

   We chose a receiver with no bias: its readings average to the truth.

   1. Compute the **mean** on each axis, :math:`\mu_x` and :math:`\mu_y`.
   2. For each reading, compute its distance from the mean on each axis.
      Add the six distances along the road. What do you get, and why does
      that make the plain average of the distances useless as a measure of
      spread?
   3. Compute the **variance** on each axis: square each distance, add the
      squares, divide by 6. State the units.
   4. Compute the **standard deviation** on each axis, and compare the
      sideways one with a 3.6 m lane. What can the AV say about where it is
      in its lane from one reading?
   5. The slide divides by 6, not 5. Explain why, and compute what dividing
      by :math:`n - 1 = 5` would give along the road, and when you would
      use it.

   .. raw:: html

      <hr>

   **Part B. The lean**

   6. Compute the **covariance** :math:`\mathrm{Cov}(x, y)`: multiply each
      reading's :math:`x` distance by its own :math:`y` distance, add the six
      products, divide by 6.
   7. Write the covariance matrix :math:`P`. What does the sign of the
      off-diagonal entry say about the cloud? Can six readings prove the
      receiver has no lean?

   .. raw:: html

      <hr>

   **Part C. Same sigma, not equally good**

   A second receiver, B, is bolted next to A. We do not know yet whether B
   has bias. Its six readings along the road, with the AV still parked at
   :math:`x = 100.0` m, are:

   .. code-block:: text

      105.3   101.8   104.1   102.4   104.6   101.0

   8. Compute B's mean and standard deviation without redoing the full
      table. (Hint: compare each reading with A's.)
   9. B's mean is off by 3.2 m. Could noise alone explain that? Use the fact
      that the average of :math:`n` readings wanders by about
      :math:`\sigma / \sqrt{n}`.
   10. What did you need, besides the readings, to find B's bias? Could
       :math:`\sigma` alone have told you?

   .. raw:: html

      <hr>

   **Deliverable**

   The deviation table with its squared and product columns, :math:`P`, and
   a sentence each for questions 2, 4, 9 and 10.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`\mu_x = 100.0` m and :math:`\mu_y = 2.5` m, the
      surveyed spot, because we chose a receiver with no bias.

      Question 2: the distances along the road are +2.1, -1.4, +0.9, -0.8,
      +1.4 and -2.2. They add to **0.0**: pluses and minuses cancel, and
      they always do around the mean, so their average says nothing about
      the spread. Squaring makes every term positive.

      Question 3: the squares along the road are 4.41, 1.96, 0.81, 0.64, 1.96
      and 4.84, adding to 14.62, so :math:`\mathrm{Var}(x) = 14.62/6 = 2.437`
      **m²**. Across the road: 1.21, 3.24, 0.36, 1.69, 0.81 and 0.81, adding
      to 8.12, so :math:`\mathrm{Var}(y) = 8.12/6 = 1.353` m². Square meters
      are hard to picture, which is why the next step takes the square root.

      Question 4: :math:`\sigma_x = \sqrt{2.437} = 1.56` m and
      :math:`\sigma_y = \sqrt{1.353} = 1.16` m. A typical sideways miss of
      1.16 m is a third of a 3.6 m lane: from one reading, the AV cannot tell
      where in its lane it is.

      Question 5: the mean here is the surveyed truth, known from outside,
      so we divide by 6. A mean worked out from the readings themselves sits
      a little closer to them than the truth does, so you divide by
      :math:`n - 1` to make up for it: :math:`14.62/5 = 2.924` m², and
      :math:`\sigma_x = 1.71` m. NumPy's ``np.var`` divides by :math:`n`
      unless you pass ``ddof=1``. Say which one you used.

      Question 6: the products are -2.31, -2.52, +0.54, +1.04, +1.26 and
      +1.98, adding to **-0.01**, so :math:`\mathrm{Cov}(x, y) = -0.01/6 =
      -0.002` m².

      Question 7:

      .. math::

         P = \begin{bmatrix} 2.437 & -0.002 \\ -0.002 & 1.353 \end{bmatrix}
           \approx \begin{bmatrix} 2.437 & 0 \\ 0 & 1.353 \end{bmatrix} \text{ m}^2

      Positive would mean "too far ahead usually comes with too far left", a
      leaning cloud; negative, "too far ahead usually comes with too far
      right". Near zero, as here, means no lean: an upright cloud. Six
      readings cannot prove it. We chose a receiver with no lean.

      Question 8: every B reading is A's plus 3.2 m, so B's mean is
      **103.2 m** and its :math:`\sigma_x` is **1.561 m**, exactly A's.
      Shifting every reading by the same amount does not change any distance
      from the mean.

      Question 9: no. Noise alone moves the average of six readings by only
      about :math:`1.561/\sqrt{6} = 1.561/2.45 \approx 0.64` m. An offset of
      3.2 m is five times that, so it is **bias**.

      Question 10: the truth from outside, here the surveyed spot.
      :math:`\sigma` needs only the readings, so it cannot tell a centered
      receiver from a biased one: both have :math:`\sigma = 1.561` m.


.. dropdown:: Exercise 2. The Kalman Gain in the Tunnel
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Blend a prediction and a sign match by hand, and see that only the two
   :math:`\sigma` values decide how far the estimate moves.

   .. raw:: html

      <hr>

   **Specification**

   The AV is in the tunnel, GNSS is lost. The wheels and the IMU predict
   that it is at **50.0 m** along the tunnel, with :math:`\sigma = 2` m.
   The camera matches an exit sign against the HD map, which places the AV
   at **53.0 m**, with :math:`\sigma = 1` m. (These are numbers we chose for
   the example.)

   1. Compute the **surprise**, measured minus predicted.
   2. Compute the gain
      :math:`K = \sigma_\text{pred}^2 / (\sigma_\text{pred}^2 + \sigma_\text{meas}^2)`,
      the new estimate :math:`\hat{x} = \hat{x}^- + K (z - \hat{x}^-)`, and
      the new :math:`\sigma` from
      :math:`\sigma^2 = (1 - K)\,\sigma_\text{pred}^2`.
   3. Check the new :math:`\sigma^2` with the long form,
      :math:`(1 - K)^2 \sigma_\text{pred}^2 + K^2 \sigma_\text{meas}^2`.
      Which source contributes more of the remaining uncertainty?
   4. Repeat questions 2 and 3 with a sign match of :math:`\sigma = 2` m,
      then :math:`\sigma = 4` m (same readings). Describe how :math:`K` moves
      and what that does to the estimate.
   5. In all three cases, compare the new :math:`\sigma` with both inputs.
      What do you notice?
   6. Now suppose the HD map puts every exit sign 2 m too far along. The
      prediction counted from the last sign, and the sign match uses the
      same map, so both answers are 2 m too far. How much of that 2 m
      survives the blend with :math:`K = 0.8`? What does the filter report?
      Can the surprise reveal the error?

   .. raw:: html

      <hr>

   **Deliverable**

   A three-row table (sign match :math:`\sigma` of 1, 2 and 4 m) with
   :math:`K`, the new estimate and the new :math:`\sigma`, and three
   sentences on question 6.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`53 - 50 = 3` m.

      Question 2: :math:`K = 4/(4 + 1) = 0.8`, so
      :math:`\hat{x} = 50 + 0.8 \times 3 = 52.4` m, and
      :math:`\sigma^2 = 0.2 \times 4 = 0.8` m², :math:`\sigma = 0.89` m.

      Question 3: :math:`0.2^2 \times 2^2 + 0.8^2 \times 1^2 = 0.16 + 0.64 =
      0.8` m², the same answer. The sign match contributes most (0.64 of
      0.8), because the estimate leans on it with weight 0.8.

      Question 4:

      .. list-table::
         :class: compact-table
         :widths: 28 18 27 27
         :header-rows: 1

         * - **Sign match** :math:`\sigma`
           - :math:`K`
           - **New estimate**
           - **New** :math:`\sigma`
         * - 1 m
           - 0.8
           - 52.4 m
           - 0.89 m
         * - 2 m
           - 0.5
           - 51.5 m
           - 1.41 m
         * - 4 m
           - 0.2
           - 50.6 m
           - 1.79 m

      A worse sign match means a smaller :math:`K`: the estimate stays
      closer to the prediction. Equal :math:`\sigma` values split the
      difference. :math:`K` is computed at every sign match, never picked.

      Question 5: the new :math:`\sigma` is smaller than **both** inputs
      every time (0.89 against 2 and 1; 1.41 against 2 and 2; 1.79 against 2
      and 4). Combining two independent sources beats either one alone.

      Question 6: all of it. The blend is
      :math:`0.2 \times 2 + 0.8 \times 2 = 2` m of error, yet the filter
      still reports :math:`\pm 0.89` m. The surprise cannot tell:
      :math:`53 - 50` and :math:`51 - 48` are both 3 m. Combining helps only
      because the two errors are independent and partly cancel. A shared
      error does not cancel; it needs a source without the map (GNSS at the
      tunnel exit).


.. dropdown:: Exercise 3. One Predict Step, and Twenty-Two
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run predict by hand and find out where the growth of :math:`P` comes
   from: mostly through :math:`F P F^\top`, not through :math:`Q`.

   .. raw:: html

      <hr>

   **Part A. The predicted state**

   The state is :math:`\mathbf{x} = [p_x\ p_y\ v_x\ v_y]^\top`, with
   :math:`\Delta t = 0.1` s and the constant velocity rule. Our example
   (numbers we chose): the last estimate is
   :math:`\hat{\mathbf{x}} = [100,\ 20,\ 10,\ 0]^\top` (m and m/s), and the
   IMU reads a brake of 1 m/s², so :math:`\mathbf{u} = [-1,\ 0]^\top`.

   1. Write :math:`F` (4 by 4) and :math:`B` (4 by 2). Hint: the lecture's
      motion-model table gives each row. Position becomes
      :math:`p + \Delta t\,v` (from :math:`F`) plus
      :math:`\tfrac{1}{2}\Delta t^2 a` (from :math:`B`); speed becomes
      :math:`v + \Delta t\,a`.
   2. Compute :math:`\hat{\mathbf{x}}^- = F \hat{\mathbf{x}} + B \mathbf{u}`.
   3. The true motion has a term :math:`\mathbf{w}` that the prediction
      sets to 0. Why 0, and where does :math:`\mathbf{w}` go instead?

   .. raw:: html

      <hr>

   **Part B. The predicted uncertainty, along the tunnel**

   Keep only the two numbers along the tunnel, position :math:`p_x` and
   speed :math:`v_x`. In the hands-on at :math:`t = 7.1` s, just after a
   sign match, the filter reports :math:`\sigma_p = 0.81` m,
   :math:`\sigma_v = 0.30` m/s, and a correlation of +0.63 between them.

   4. Build the 2 by 2 :math:`P` from those three numbers (the off-diagonal
      entry is correlation times both :math:`\sigma` values).
   5. With :math:`F = \begin{bmatrix} 1 & 0.1 \\ 0 & 1 \end{bmatrix}`,
      compute :math:`F P F^\top` once. What is the new :math:`\sigma_p`?
      Which term of the product added the most?
   6. The filter's :math:`Q` comes from the acceleration the IMU gets
      wrong: we chose :math:`\sigma_a = 0.5` m/s², pushed through the
      position and speed rows of :math:`B`. An acceleration error of
      :math:`\sigma_a` moves the speed by :math:`\Delta t\,\sigma_a` and the
      position by :math:`\tfrac{1}{2}\Delta t^2 \sigma_a`, and each
      diagonal entry of :math:`Q` is that size squared. Compute the position
      and speed entries of :math:`Q` for one step. Which one matters?
   7. In the hands-on, 22 predict steps with no sign match take
      :math:`\sigma_p` from 0.81 to **1.35 m**. Without :math:`Q` it would
      still reach **1.32 m**. Explain, using questions 5 and 6, why
      :math:`Q` matters so little to position directly and yet matters a
      lot over many steps. (Optional: loop 22 times in NumPy and confirm.)

   .. raw:: html

      <hr>

   **Deliverable**

   :math:`\hat{\mathbf{x}}^-`, the 2 by 2 :math:`P` before and after one
   step, the two :math:`Q` entries, and a paragraph for question 7.

   .. dropdown:: Guidance
      :color: success

      Question 1:

      .. math::

         F = \begin{bmatrix} 1 & 0 & 0.1 & 0 \\ 0 & 1 & 0 & 0.1 \\
                             0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}, \quad
         B = \begin{bmatrix} 0.005 & 0 \\ 0 & 0.005 \\ 0.1 & 0 \\ 0 & 0.1 \end{bmatrix}

      :math:`B` adds :math:`\tfrac{1}{2}\Delta t^2 a` to the position and
      :math:`\Delta t\, a` to the speed.

      Question 2: :math:`F \hat{\mathbf{x}} = [101,\ 20,\ 10,\ 0]^\top` and
      :math:`B\mathbf{u} = [-0.005,\ 0,\ -0.1,\ 0]^\top`, so
      :math:`\hat{\mathbf{x}}^- = [100.995,\ 20,\ 9.9,\ 0]^\top`.

      Question 3: :math:`\mathbf{w}` is drawn from a bell curve centered on
      0, as likely to push the AV ahead as back, so the best single guess is
      its center. It is not dropped: its size, :math:`Q`, goes into the
      predicted uncertainty, :math:`P^- = F P F^\top + Q`.

      Question 4: the off-diagonal entry is
      :math:`0.63 \times 0.81 \times 0.30 = 0.153`, so

      .. math::

         P = \begin{bmatrix} 0.656 & 0.153 \\ 0.153 & 0.090 \end{bmatrix}

      Question 5: the new position variance is
      :math:`P_{pp} + 2\,\Delta t\, P_{pv} + \Delta t^2 P_{vv}
      = 0.656 + 0.031 + 0.001 = 0.688` m², so :math:`\sigma_p \approx 0.83`
      m after one step. The largest addition is :math:`2\,\Delta t\,P_{pv}`:
      the speed error, through the tilt, leaks into position. The
      off-diagonal entry grows too (to about 0.162), so position and speed
      become more linked at every step.

      Question 6: :math:`Q_{pp} = \sigma_a^2 (0.005)^2 = 0.25 \times
      0.000025 \approx 0.000006` m², which is nothing. :math:`Q_{vv} =
      \sigma_a^2 (0.1)^2 = 0.0025` (m/s)². :math:`Q` mostly feeds the
      **speed** error.

      Question 7: each step adds only a few millionths of a square meter to
      position directly, so 22 steps of :math:`F P F^\top` alone already take
      :math:`\sigma_p` to 1.32 m. But the 0.0025 added to the speed variance
      each step is leaked into position by :math:`F P F^\top` at the next
      steps, which brings it to 1.35 m. Over a long gap, or with a large
      :math:`\sigma_a`, that leak dominates. In the hands-on the same 22
      steps take :math:`\sigma_v` from 0.30 to 0.38 m/s and the correlation
      from +0.63 to +0.79. With no sign match, :math:`P` only grows.

      The optional NumPy loop, started from the rounded values in Part B,
      gives 1.36 m with :math:`Q` and 1.33 m without. The hands-on starts
      from unrounded values, hence 1.35 and 1.32; the gap between the two
      runs, about 0.03 m, is the same.


.. dropdown:: Exercise 4. One Update, and the Tilt That Corrects Speed
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run the update by hand at the hands-on's :math:`t = 9.3` s sign match,
   and see a position-only reading correct the speed.

   .. raw:: html

      <hr>

   **Specification**

   Along the tunnel only. After the 22 predict steps of Exercise 3 the
   prediction is :math:`p_x = 110.41` m, :math:`v_x = 10.90` m/s, with

   .. math::

      P^- = \begin{bmatrix} 1.84 & 0.40 \\ 0.40 & 0.142 \end{bmatrix},
      \quad H = \begin{bmatrix} 1 & 0 \end{bmatrix}, \quad R = 1 \text{ m}^2

   (:math:`0.40 = 0.79 \times 1.35 \times 0.38`, the tilt.) The sign match
   reads **111.15 m**; :math:`R` is :math:`\sigma = 1` m squared, which we
   chose.

   1. Compute the surprise :math:`\nu = z - H\hat{\mathbf{x}}^-` and its
      expected size :math:`S = H P^- H^\top + R`.
   2. Compute :math:`K = P^- H^\top S^{-1}`. You get two numbers. Which one
      matches the one-number rule :math:`P^-/(P^- + R)`?
   3. Compute the new estimate :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^-
      + K\nu`. By how much did the position move, as a share of the
      surprise? By how much did the speed move?
   4. The sign match never measures speed. Name the entry of :math:`P^-`
      that made the speed move, and say what would happen if it were 0.
   5. Compute :math:`P = (I - KH) P^-`. Report the new :math:`\sigma_p`,
      :math:`\sigma_v` and their correlation.
   6. Look for :math:`\nu` in the line of question 5. What does its absence
      mean if the sign match had been 25 m wrong?

   .. raw:: html

      <hr>

   **Deliverable**

   :math:`\nu`, :math:`S`, :math:`K`, the new estimate and the new
   :math:`P`, with a sentence each for questions 4 and 6.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`\nu = 111.15 - 110.41 = 0.74` m, and
      :math:`S = 1.84 + 1 = 2.84` m².

      Question 2: :math:`K = [1.84,\ 0.40]^\top / 2.84 = [0.65,\ 0.14]^\top`.
      The top entry is the one-number rule, :math:`1.84/(1.84 + 1) = 0.65`:
      the prediction (:math:`\sigma \approx 1.35` m) is less certain than
      the sign match (1 m), so the estimate acts on 65% of the surprise.

      Question 3: the position moves :math:`0.65 \times 0.74 = 0.48` m, to
      **110.89 m**. The speed moves :math:`0.14 \times 0.74 = 0.10` m/s, to
      **11.01 m/s** (the script, unrounded: 10.901 + 0.104).

      Question 4: the off-diagonal entry, 0.40, the tilt. Predict tied speed
      to position (correlation +0.79): "too far along" usually comes with
      "too fast". With that entry at 0, the speed row of :math:`K` would be 0
      and the speed would not move.

      Question 5: :math:`P_{pp} = 0.35 \times 1.84 = 0.65` m², so
      :math:`\sigma_p` goes from 1.35 to **0.80 m**.
      :math:`P_{vv} = 0.142 - 0.14 \times 0.40 \approx 0.086`, so
      :math:`\sigma_v \approx 0.29` m/s. :math:`P_{pv} = 0.35 \times 0.40 =
      0.14`, so the correlation drops from +0.79 to about **+0.60**.

      Question 6: :math:`\nu` is not in it. :math:`P` shrinks by the same
      amount whether the reading was good or bad. The filter does not check:
      a 25 m wrong sign match would still shrink :math:`P` and pull the
      estimate. That is what the NIS test and gating in Exercise 6 are for.
      (Across the tunnel, the same update uses :math:`R = 0.2^2 = 0.04` m²,
      which we chose because the sign is on the wall right beside the AV,
      and gives :math:`K = 0.83` and 0.29.)


.. dropdown:: Exercise 5. The EKF: a Tangent, and Its Jacobians
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Linearize a range measurement by hand at a good and a poor estimate,
   compute the EKF's Jacobians with real numbers, check them numerically,
   and then let the hands-on script do the same check.

   .. raw:: html

      <hr>

   **Part A. The range to one landmark**

   The AV drives along a straight road toward a landmark 10 m off the road,
   beside :math:`x = 20` m. The camera reports the range,
   :math:`h(x) = \sqrt{(20 - x)^2 + 10^2}`. The AV is really at
   :math:`x = 16` m. Treat the reading as perfect and fully trusted (one
   idea at a time).

   1. What does the camera read?
   2. **Run 1, a good estimate**, :math:`\hat{x} = 15.5` m. Compute the
      expected reading :math:`h(\hat{x})`, the surprise, the slope of the
      tangent :math:`-(20 - \hat{x})/h(\hat{x})`, and the move (surprise
      divided by slope). Where does the new estimate land?
   3. **Run 2, a poor estimate**, :math:`\hat{x} = 10` m. Same four steps.
      How far short of 16 m does it land?
   4. Between 10 and 16 m the real curve drops by how much per meter? Compare
      with the slope at 10 m and explain why the correction fell short.
   5. **Run 3** (extension), :math:`\hat{x} = 4` m. Where does it land? What
      happens to the shortfall as the estimate gets worse, and why is that
      the start of the EKF's feedback loop?

   .. raw:: html

      <hr>

   **Part B. The Jacobians with real numbers**

   The EKF's motion model for an AV that turns, with state
   :math:`\mathbf{x} = [x,\ y,\ \theta]` and control
   :math:`\mathbf{u} = [v,\ \omega]`, is

   .. math::

      f(\mathbf{x}, \mathbf{u}) =
      \begin{bmatrix} x + v\,\Delta t \cos\theta \\ y + v\,\Delta t \sin\theta \\
                      \theta + \omega\,\Delta t \end{bmatrix}

   6. Derive :math:`F_k = \partial f / \partial \mathbf{x}` and evaluate it
      at :math:`v = 10` m/s, :math:`\Delta t = 0.1` s,
      :math:`\hat{\theta} = 30^\circ`. What does row 1, column 3 mean in
      words?
   7. **Check it numerically.** Nudge :math:`\theta` by
      :math:`\pm 0.01` rad, compute how much :math:`x + v\,\Delta t \cos\theta`
      changes, and divide by 0.02. Does it match row 1, column 3? What
      would you see if that entry had the wrong sign?
   8. The camera reports range and bearing to a sign. The sign is 24 m east
      and 18 m north of the predicted position (we chose it). Evaluate

      .. math::

         H_k = \begin{bmatrix} -\Delta x / r & -\Delta y / r & 0 \\
                               \Delta y / r^2 & -\Delta x / r^2 & -1 \end{bmatrix}

      and check row 1, column 1 by moving the AV 0.1 m east and recomputing
      the range.

   .. raw:: html

      <hr>

   **Part C. The script does the check**

   .. code-block:: bash

      cd enpm818z-fall-2026-carla-python/lecture3/curved_tunnel
      python3 ekf_curve.py --make-csv        # the data: 21 s through a 120 degree bend
      python3 ekf_curve.py --check-jacobian  # test F_k and H_k first
      python3 ekf_curve.py                   # the live window

   9. Run ``--check-jacobian`` and report the largest difference it prints.
      Then open ``check_jacobian()`` and say which of your by-hand checks it
      repeats, and how many random points it tries.
   10. Open ``run_ekf()`` and find the three places where angles are wrapped,
       and the line where :math:`F_k` and :math:`Q_k` are built before the
       estimate moves. Why must they be built there?
   11. In the live window, tick **wrong sign in the Jacobian** (or run
       ``python3 ekf_curve.py --wrong-sign``). Does the filter crash? What
       happens to the heading error against its :math:`\pm 1\sigma` band?

   .. raw:: html

      <hr>

   **Deliverable**

   The three runs of Part A in a table, :math:`F_k` and :math:`H_k` with
   your numerical checks, and the output of the two script runs with a
   sentence each for questions 10 and 11.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`\sqrt{4^2 + 10^2} = 10.77` m.

      Questions 2, 3 and 5:

      .. list-table::
         :class: compact-table
         :widths: 16 16 16 16 16 20
         :header-rows: 1

         * - :math:`\hat{x}`
           - **Expected**
           - **Surprise**
           - **Slope**
           - **Move**
           - **New estimate**
         * - 15.5 m
           - 10.97 m
           - -0.20 m
           - -0.41
           - +0.48 m
           - 15.98 m, almost 16
         * - 10 m
           - 14.14 m
           - -3.37 m
           - -0.71
           - +4.77 m
           - 14.77 m, 1.23 m short
         * - 4 m
           - 18.87 m
           - -8.10 m
           - -0.85
           - +9.55 m
           - 13.55 m, 2.45 m short

      A negative surprise means less range than expected, so the AV is closer
      to the landmark: farther ahead than :math:`\hat{x}`.

      Question 4: :math:`(14.14 - 10.77)/6 = 0.56` m of range per meter,
      but the tangent at 10 m says 0.71. The tangent is too steep, so the
      correction is too small. That slope is what the EKF calls the Jacobian
      :math:`H`: a poor estimate gives a wrong :math:`H`.

      Question 5: the worse the estimate, the larger the shortfall (0.02,
      1.23, 2.45 m). The EKF draws the tangent at its own estimate, so a
      wrong estimate puts it in the wrong place, and once the error is large
      enough the next estimate gets worse while :math:`P` still shrinks.
      Run 2 and run 3 still improved; that loop (divergence) starts only when
      the error is large enough to make the next estimate worse.

      Question 6:

      .. math::

         F_k = \begin{bmatrix} 1 & 0 & -v\,\Delta t \sin\hat{\theta} \\
                               0 & 1 & v\,\Delta t \cos\hat{\theta} \\
                               0 & 0 & 1 \end{bmatrix}
             = \begin{bmatrix} 1 & 0 & -0.500 \\ 0 & 1 & 0.866 \\ 0 & 0 & 1 \end{bmatrix}

      Row 1, column 3: nudge the heading, and :math:`x` moves by -0.5 m per
      radian of nudge. :math:`F_k` depends on :math:`\hat{\theta}`, so it is
      recomputed every step.

      Question 7: :math:`\cos(0.5336) - \cos(0.5136) = -0.0100`, divided by
      0.02 gives **-0.500**, a match. With the wrong sign you would compute
      +0.500 and the check would differ by 1.0. The filter would still run.

      Question 8: :math:`r = \sqrt{24^2 + 18^2} = 30` m, so

      .. math::

         H_k = \begin{bmatrix} -0.80 & -0.60 & 0 \\ 0.020 & -0.027 & -1 \end{bmatrix}

      Moving 0.1 m east gives :math:`\Delta x = 23.9` and
      :math:`r = 29.920` m: the range drops 0.080 m per 0.1 m, which is
      -0.80. Row 2, column 3 says: turn the nose 1 rad left, and the sign
      moves 1 rad right of it.

      Question 9: it prints
      ``Jacobian check (F_k and H_k): largest difference 2.64e-09  ->  OK``.
      ``check_jacobian()`` does your questions 7 and 8 for every entry at
      once: it nudges each input by :math:`\pm 10^{-6}`, at 20 random states,
      controls and sign positions, and compares with ``jacobian_f`` and
      ``jacobian_h``.

      Question 10: wrapped inside :math:`f` (the heading), in the surprise
      :math:`\nu` (the bearing), and in :math:`\hat{\mathbf{x}}` after the
      update. :math:`F_k` and :math:`Q_k` are built at the last estimate,
      before ``x = f(x, u)`` moves it, because that is where the tangent is
      drawn. :math:`H_k` is built after, at the prediction.

      Question 11: it does not crash, and it raises no error. The printed
      line reads
      ``position RMSE 1.23 m, heading RMSE 4.0 deg, heading inside 1-sigma 30%``,
      against 0.69 m, 1.4 degrees and 65% with the right sign. The heading
      error leaves the band. A wrong sign still runs and converges, which is
      why you test the Jacobians before you trust the filter.


.. dropdown:: Exercise 6. Is the Filter Honest? Sliders and the NIS
   :icon: number
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   **Goal**

   Detect a filter whose reported uncertainty is wrong, twice: with the
   share of time the truth falls inside :math:`\pm 1\sigma` (needs ground
   truth), and with the NIS (needs none). **This is the core exercise of
   L3.**

   .. raw:: html

      <hr>

   **Part A. The NIS by hand**

   The normalized innovation squared compares the actual surprise with the
   expected one:

   .. math::

      \varepsilon = \frac{\nu^2}{S} \quad\text{(one number)}, \qquad
      \varepsilon = \boldsymbol{\nu}^\top S^{-1} \boldsymbol{\nu}
      \quad\text{(}x\text{ and }y\text{ together)}

   If the filter is honest, :math:`\varepsilon` averages about 1 per number
   the sensor reports.

   1. Compute :math:`\varepsilon` along the tunnel for the :math:`t = 9.3` s
      sign match of Exercise 4. Is one value enough to judge the filter?
   2. Over all 19 sign matches in the hands-on, with :math:`x` and :math:`y`
      together, the average is **1.39 per match**. What is the expected
      average? By chance alone the average of 19 matches lands anywhere from
      **1.2 to 3.0**. Is the filter honest?
   3. For a single match giving :math:`x` and :math:`y`, an honest filter
      keeps :math:`\varepsilon` between about **0.05 and 7.4**, 95% of the
      time. What does it mean if :math:`\varepsilon` keeps landing above the
      band? Below it? Which of the two is dangerous?
   4. **Gating** throws a reading away when :math:`\varepsilon > 9.21`, the
      99% line for a sign match reporting :math:`x` and :math:`y`. Name a
      reading it catches, and explain what goes wrong if the filter is
      already wrong when it gates.

   .. raw:: html

      <hr>

   **Part B. The Kalman filter's sliders**

   .. code-block:: bash

      cd enpm818z-fall-2026-carla-python/lecture3/tunnel_kf
      python3 kf_tunnel.py --make-csv                       # the data: 45 s, 451 rows, 19 sign matches
      python3 kf_tunnel.py tunnel_drive.csv                 # the live window
      python3 kf_tunnel.py tunnel_drive.csv --html kf.html  # no desktop? a web page

   The window has two sliders, **Q: sigma_a (m/s^2)** (0.01 to 3) and
   **R: sigma_sign (m)** (0.1 to 6). The same settings run without a window
   from the command line, ``--sigma-a`` and ``--sigma-sign``, and the
   terminal prints the error and the share inside :math:`1\sigma`.

   5. **Guess first, then move the slider.** For each row below, predict
      whether the error goes up or down and whether the share inside
      :math:`1\sigma` goes above or below 68%. Then run it and fill in the
      table.

      .. list-table::
         :class: compact-table
         :widths: 40 20 20 20
         :header-rows: 1

         * - **Setting**
           - **RMS error**
           - **Inside** :math:`1\sigma`
           - **What it shows**
         * - default: :math:`\sigma_a = 0.5`, :math:`\sigma_\text{sign} = 1`
           -
           -
           -
         * - :math:`Q` too small: :math:`\sigma_a = 0.01`
           -
           -
           -
         * - :math:`Q` too big: :math:`\sigma_a = 3`
           -
           -
           -
         * - :math:`R` too small: :math:`\sigma_\text{sign} = 0.1`
           -
           -
           -
         * - :math:`R` too big: :math:`\sigma_\text{sign} = 6`
           -
           -
           -

   6. With :math:`Q` too small, watch the sawtooth and the error panel. What
      does the filter report about itself, and what does the true error do?
      Why is this the dangerous row?
   7. (Extension) Add a few lines to ``run_kf()`` that compute
      :math:`\varepsilon` at every sign match (from the prediction, before
      the update) and print the average. Compare the default against
      :math:`Q` too small and :math:`Q` too big, against the 1.2 to 3.0
      band. Which of the two checks, inside :math:`1\sigma` or NIS, could
      the AV run on the road?

   .. raw:: html

      <hr>

   **Part C. The EKF's sliders**

   In ``ekf_curve.py`` the sliders are **Q: gyro noise (deg/s)** and
   **R: sign range noise (m)** (command line: ``--gyro-noise``,
   ``--range-noise``). The honesty check is on the heading.

   8. Run the default (gyro 2 deg/s, range 1 m), then :math:`Q` too small
      (gyro 0.1 deg/s), then :math:`Q` too big (gyro 8 deg/s). Report the
      position error, the heading error and the share inside :math:`1\sigma`
      for each.
   9. The real gyro noise in the data is 1.1 deg/s, yet the default assumes
      2 deg/s. Why is it right to set :math:`Q` larger than the sensor's
      noise?

   .. raw:: html

      <hr>

   **Deliverable**

   The two NIS answers, the filled table of question 5, the three EKF rows,
   and one paragraph: your filter reported a small :math:`\sigma` while
   being badly wrong, and raised nothing. Which logged quantity would have
   caught it, and what should the AV do when it leaves its band?

   .. dropdown:: What to expect
      :color: warning

      Question 1: :math:`\varepsilon = 0.74^2/2.84 = 0.19`. One reading
      tells you little: an honest filter produces values from about 0 to
      several.

      Question 2: expected 2, one per number reported. 1.39 lies inside the
      1.2 to 3.0 band, so the filter is **honest**: its :math:`\sigma` means
      something.

      Question 3: above the band, the filter is **overconfident**:
      :math:`Q` or :math:`R` is too small. That is the dangerous case. Below
      it, the filter is underconfident: wasteful, but safe.

      Question 4: a wrong sign match, when the camera misreads a sign's
      number: on time, normal-looking, and 25 m wrong. The trap: a filter
      that has already drifted finds the **good** readings far from its
      estimate and rejects them, so the gate keeps it wrong. Count
      rejections in a row, and raise an alarm past a limit.

      Question 5, from the shipped CSV:

      .. list-table::
         :class: compact-table
         :widths: 40 20 20 20
         :header-rows: 1

         * - **Setting**
           - **RMS error**
           - **Inside** :math:`1\sigma`
           - **What it shows**
         * - default: :math:`\sigma_a = 0.5`, :math:`\sigma_\text{sign} = 1`
           - 1.06 m
           - 65%
           - honest
         * - :math:`Q` too small: :math:`\sigma_a = 0.01`
           - **5.46 m**
           - **25%**
           - overconfident
         * - :math:`Q` too big: :math:`\sigma_a = 3`
           - 1.28 m
           - 84%
           - underconfident
         * - :math:`R` too small: :math:`\sigma_\text{sign} = 0.1`
           - 1.46 m
           - 21%
           - trusts every sign, overconfident
         * - :math:`R` too big: :math:`\sigma_\text{sign} = 6`
           - 2.95 m
           - 77%
           - ignores the signs, drifts

      Question 6: with :math:`Q` too small the sawtooth flattens: the filter
      reports a thin band (its final :math:`\sigma` is 0.45 m, against 1.21
      m at the default) while the error is five times larger than the
      default's. The band is thin, the filter sounds confident, and nothing
      raises an alarm. The share inside :math:`1\sigma` catches it: 25%
      instead of about 68%.

      Question 7: computed from ``run_kf()`` with the shipped CSV, the
      average :math:`\varepsilon` per match is about **1.39** at the
      default (honest), about **35** with :math:`Q` too small (11 of the 19
      matches are above 7.4: overconfident), and about **0.84** with
      :math:`Q` too big (below 1.2: underconfident). The share inside
      :math:`1\sigma` needs the true position, which the AV never has on
      the road. The NIS needs only the surprise and :math:`S`, which the
      filter computes anyway, so it is the check the AV can log and act on.

      Question 8:

      .. list-table::
         :class: compact-table
         :widths: 34 18 18 15 15
         :header-rows: 1

         * - **Setting**
           - **Position error**
           - **Heading error**
           - **Inside** :math:`1\sigma`
           - **What it shows**
         * - default: gyro 2 deg/s, range 1 m
           - 0.69 m
           - 1.4 deg
           - 65%
           - honest
         * - :math:`Q` too small: gyro 0.1 deg/s
           - 1.18 m
           - 2.1 deg
           - 23%
           - overconfident
         * - :math:`Q` too big: gyro 8 deg/s
           - 0.75 m
           - 1.8 deg
           - 92%
           - underconfident

      Question 9: :math:`Q` must cover everything the motion model gets
      wrong, not only the gyro's random noise. Here that includes the gyro's
      bias, which no filter averages away, so we widen :math:`Q` to cover it.

      The paragraph: the NIS, logged at every sign match. When its running
      average stays above the band, the filter's :math:`\sigma` can no longer
      be trusted: raise an alarm, so that nothing downstream plans with a
      :math:`\sigma` the filter has not earned.
