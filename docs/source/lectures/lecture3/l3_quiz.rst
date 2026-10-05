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

This quiz covers Lecture 3: the road frame, noise and bias, variance,
standard deviation and covariance, the Kalman gain and the full Kalman filter
cycle in the tunnel, the hands-on sliders, what breaks when the assumptions
fail, the extended Kalman filter, choosing a filter, and checking the
covariance with the NIS and gating. Every question can be answered from the
slides shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 21)
===================================

.. admonition:: Question 1
   :class: hint

   In the road frame, the AV sits at (103.0, 2.5) m. The survey marker that
   defines the origin is moved 50 m up the road, and the AV does not move.
   What is the AV's position now?

   A. (103.0, 2.5) m, because the AV did not move

   B. (153.0, 2.5) m

   C. **(53.0, 2.5) m**

   D. (103.0, 52.5) m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A position is an instruction for finding the AV from the marker: so many
   meters along the road, so many across. Move the marker 50 m up the road
   and the same AV is only 53.0 m from it. The AV did not move, the frame
   did, which is why the lecture says the frame is part of every reading,
   not decoration. **A** is the mistake the slide warns about: treating the
   numbers as a property of the AV.


.. admonition:: Question 2
   :class: hint

   The AV is parked on the surveyed spot and the GNSS reports six positions
   along the road. Their distances from the mean are +2.1, −1.4, +0.9, −0.8,
   +1.4 and −2.2 m. Why does variance square these distances before
   averaging them?

   A. Because squaring makes the arithmetic easier

   B. **Because the six distances add up to 0.0 m: plus and minus cancel, so
      their plain average says nothing about the spread**

   C. Because the result then has the same unit as the readings, meters

   D. Because it guarantees the result is smaller than one

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The distances from the mean always add up to zero, here 0.0 m, so their
   average is zero for any receiver, however scattered. Squared, every term
   is positive: 4.41 + 1.96 + 0.81 + 0.64 + 1.96 + 4.84 = 14.62, and
   14.62 / 6 = 2.437 m². **C is backwards**: squaring leaves the answer in
   square meters, which is why the next step takes the square root.


.. admonition:: Question 3
   :class: hint

   For the same six readings, :math:`\operatorname{Var}(x) = 2.437` m². What
   is the standard deviation :math:`\sigma_x`, and why does the lecture quote
   it instead of the variance?

   A. 2.437 m, because variance and standard deviation are the same number

   B. **1.56 m, because the square root brings the spread back to meters**

   C. 0.41 m, because the variance is divided by the six readings once more

   D. 14.62 m, because it is the total of the squared distances

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`\sigma_x = \sqrt{2.437} = 1.56` m. A variance in square meters is
   hard to picture ("what does a square meter of missing look like?"). The
   standard deviation is in meters: how far a typical reading sits from the
   mean. Across the road, :math:`\sigma_y = \sqrt{1.353} = 1.16` m, about a
   third of a 3.6 m lane, so from one reading the AV cannot tell where in
   its lane it is.


.. admonition:: Question 4
   :class: hint

   Receiver A (chosen with no bias) and a new receiver B sit side by side on
   the AV, parked at :math:`x = 100.0` m. Six readings each give A a mean of
   100.0 m and B a mean of 103.2 m. Both have
   :math:`\sigma_x = 1.561` m. What can you conclude?

   A. A and B are equally good, because their :math:`\sigma` is the same

   B. **B has a bias of about 3.2 m: noise alone moves the average of six
      readings by only about 0.64 m**

   C. B's offset is noise, and averaging more readings will remove it

   D. B is noisier than A, because its readings are larger

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The average of :math:`n` readings wanders by about
   :math:`\sigma/\sqrt{n} = 1.561/2.45 \approx 0.64` m. An offset of 3.2 m
   is five times that, so chance cannot explain it: it is bias. The lesson
   of the slide is that :math:`\sigma` cannot tell a centered receiver from a
   biased one, because :math:`\sigma` needs only the readings. Finding the
   bias needed the truth from outside, the surveyed spot. **C** fails
   because averaging removes noise, never bias.


.. admonition:: Question 5
   :class: hint

   Two receivers on the parked AV report 120 readings each. Both clouds have
   :math:`\operatorname{Var}(x) = 2.437` m² and
   :math:`\operatorname{Var}(y) = 1.353` m², but one cloud is upright and the
   other leans. Which number tells them apart?

   A. The mean along the road

   B. The standard deviation :math:`\sigma_x`

   C. **The covariance** :math:`\operatorname{Cov}(x, y)`

   D. The number of readings

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Two variances give the width and the height of the cloud, never its
   lean. The covariance measures how much the :math:`x` and :math:`y` errors
   move together: multiply each :math:`x` distance by its :math:`y` distance,
   then average. Positive means "too far ahead usually comes with too far
   left". The covariance matrix :math:`P` holds all of it: the variances on
   the diagonal, :math:`\operatorname{Cov}(x, y)` off it.


.. admonition:: Question 6
   :class: hint

   In the tunnel, the prediction says 50.0 m with :math:`\sigma = 2` m and
   the sign match says 53.0 m with :math:`\sigma = 1` m (numbers we chose).
   What are the Kalman gain and the new estimate?

   A. :math:`K = 0.5`, 51.5 m

   B. :math:`K = 0.2`, 50.6 m

   C. **K = 0.8, 52.4 m**

   D. :math:`K = 1`, 53.0 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`K` is the prediction's share of the total variance:
   :math:`K = 2^2/(2^2 + 1^2) = 4/5 = 0.8`. The surprise is
   :math:`53 - 50 = 3` m, and the estimate moves 0.8 of it:
   :math:`50 + 0.8 \times 3 = 52.4` m. The less certain prediction gets the
   smaller say. **A** would be right only if the two :math:`\sigma` values
   were equal; **D** only if the sign match were perfect.


.. admonition:: Question 7
   :class: hint

   After that update (50.0 m with :math:`\sigma = 2` m, 53.0 m with
   :math:`\sigma = 1` m, :math:`K = 0.8`), what is the new :math:`\sigma`?

   A. 1.5 m, the average of the two

   B. 1.0 m, the better of the two

   C. **0.89 m, smaller than both**

   D. 2.24 m, the square root of 4 + 1

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The new estimate is the weighted average
   :math:`0.2 \times 50 + 0.8 \times 53`, so its error is 20% of the
   prediction's error plus 80% of the sign match's. When the two errors are
   independent, variances add, each times its weight squared:
   :math:`0.2^2 \times 2^2 + 0.8^2 \times 1^2 = 0.16 + 0.64 = 0.8` m², so
   :math:`\sigma = 0.89` m. The shortcut gives the same:
   :math:`(1 - K)\,\sigma_\text{pred}^2 = 0.2 \times 4 = 0.8` m². Combining
   beats either source because their errors partly cancel.


.. admonition:: Question 8
   :class: hint

   Suppose the HD map puts every exit sign 2 m too far along the tunnel.
   The prediction counted from the last sign and the sign match uses the
   same map. What happens?

   A. The filter reports ±0.89 m, and the real error is also 0.89 m

   B. **The filter reports ±0.89 m while the real error is 2 m, and the
      surprise cannot show it**

   C. The surprise grows to 5 m, so the filter detects the map error

   D. The error averages down to :math:`0.2 \times 2 = 0.4` m

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Combining helps only because the two errors are independent. Here both
   answers carry the same 2 m, and
   :math:`0.2 \times 2 + 0.8 \times 2 = 2` m: the shared error stays, yet
   the filter still reports ±0.89 m. The surprise cannot tell, because
   :math:`53 - 50` and :math:`51 - 48` are both 3 m. Anything that trusts
   the reported number plans for a 0.89 m error when the real one is 2 m.
   This is the "no bias" assumption failing.


.. admonition:: Question 9
   :class: hint

   The tunnel filter's state is
   :math:`\mathbf{x} = [p_x \; p_y \; v_x \; v_y]^\top`, yet no sensor in
   it reports velocity. Why is velocity in the state?

   A. Because the sign match measures it indirectly

   B. **Because the motion model needs it to predict the next position**

   C. Because the planner ignores position

   D. It should not be: a state may only hold measured numbers

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The state must hold everything the motion model needs to predict the
   next moment, even numbers no sensor measures. Constant velocity moves
   the position by :math:`\Delta t \, v_x` each step, so :math:`v_x` must be
   in the state. The filter works velocity out from how the position
   changes, which is the first of the three reasons a filter is needed: no
   sensor reports it directly. **D** is the opposite of the definition.


.. admonition:: Question 10
   :class: hint

   The true motion is
   :math:`\mathbf{x}_k = F\mathbf{x}_{k-1} + B\mathbf{u}_k + \mathbf{w}`.
   The predicted state is
   :math:`\hat{\mathbf{x}}^-_k = F\hat{\mathbf{x}}_{k-1} + B\mathbf{u}_k + 0`.
   Why does :math:`\mathbf{w}` become 0?

   A. Because :math:`\mathbf{w}` is too small to matter

   B. **Because** :math:`\mathbf{w}` **is drawn from a bell curve centered
      on 0, so its best single guess is 0; its size still enters the
      uncertainty as + Q**

   C. Because the IMU removes all motion error

   D. Because :math:`\mathbf{w}` is measured by the sign match

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The filter never knows this step's :math:`\mathbf{w}`. It is as likely
   to push the AV ahead as back, so the best single guess is its center,
   zero. It is not dropped: its size, :math:`Q`, goes into the predicted
   uncertainty, :math:`P^-_k = F P_{k-1} F^\top + Q`. The same move is made
   for :math:`\mathbf{x}_{k-1}`, replaced by the last estimate
   :math:`\hat{\mathbf{x}}_{k-1}`.


.. admonition:: Question 11
   :class: hint

   In the hands-on, 22 predict steps with no sign match take the position
   :math:`\sigma` along the tunnel from 0.81 m to 1.35 m. Without :math:`Q`
   it would still reach 1.32 m. Which part of
   :math:`P^- = FPF^\top + Q` does most of that growth?

   A. :math:`Q` alone

   B. **FPFᵀ: each step leaks the speed error into the position**

   C. :math:`R`, the sign match's noise

   D. Neither: :math:`P` shrinks during predict

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The new position error is the old one plus :math:`\Delta t` times the
   velocity error, so :math:`FPF^\top` turns a speed error into a position
   error at every step, and links the two (the tilt of the ellipse grows
   from a correlation of +0.63 to +0.79). :math:`Q` mostly feeds the speed
   error, which :math:`FPF^\top` then leaks into position. :math:`R` plays no
   part in predict, and **D** is wrong: with no sign match, :math:`P` only
   grows.


.. admonition:: Question 12
   :class: hint

   The state has four numbers :math:`[p_x, p_y, v_x, v_y]` and the sign
   match reports two (east, north). What is the measurement matrix
   :math:`H`?

   A. A 4 by 4 identity, because every state number is measured

   B. **A 2 by 4 matrix that keeps** :math:`p_x` **and** :math:`p_y` **and
      drops the velocity**

   C. A 4 by 2 matrix that turns the reading into a state

   D. A 2 by 2 matrix holding :math:`R`

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The measurement model :math:`\mathbf{z}_k = H\mathbf{x}_k + \mathbf{v}`
   says the reading is the part of the state the sensor sees, plus its
   error. A sign match sees position only, so :math:`H` keeps
   :math:`p_x, p_y` and drops the velocity it cannot see: two rows, one per
   reading, and four columns, one per state number. With the prediction
   (100.995, 20, 9.9, 0), the expected reading :math:`H\hat{\mathbf{x}}^-`
   is (100.995, 20) m. **D** confuses :math:`H` with the sensor's noise,
   :math:`R`.


.. admonition:: Question 13
   :class: hint

   At :math:`t = 9.3` s the prediction along the tunnel is 110.41 m with
   :math:`P^- = 1.35^2 = 1.84` m². The sign match reads 111.15 m with
   :math:`R = 1` m². How far does the estimate move?

   A. 0.74 m, the whole surprise

   B. 0.26 m

   C. **0.48 m, 65% of the 0.74 m surprise**

   D. 0 m, because the reading lies inside the 2σ circle

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`K = P^-/(P^- + R) = 1.84/(1.84 + 1) = 0.65`, and
   :math:`0.65 \times 0.74 = 0.48` m, so the new estimate is 110.89 m. The
   prediction (:math:`\sigma \approx 1.35` m) is less certain than the sign
   match (1 m), so the gain leans toward the sign match. The longer the AV
   drives without a sign, the larger :math:`P^-` grows and the larger the
   next :math:`K`.


.. admonition:: Question 14
   :class: hint

   In the 4 by 2 gain at :math:`t = 9.3` s, the row for the east speed
   :math:`v_x` holds 0.14, although a sign match never measures speed. Why
   is it not zero?

   A. Because the sign match also reports speed

   B. **Because predict tied speed to position (correlation +0.79), so a
      position surprise also corrects the speed**

   C. Because of a rounding error

   D. Because :math:`R` has a speed entry

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Each predict step adds speed times :math:`\Delta t` to the position, so
   the errors become linked: too far along, likely too fast. The
   :math:`P^- H^\top` part of :math:`K = P^- H^\top S^{-1}` carries that link
   to every state number, including the ones never measured. Here the speed
   moves by :math:`0.14 \times 0.74 = 0.10` m/s, from 10.90 to 11.01 m/s. In
   the lecture's words: "A sign cannot see speed, but the link corrected it
   anyway."


.. admonition:: Question 15
   :class: hint

   In the tunnel hands-on, you set the motion noise to
   :math:`\sigma_a = 0.01` (the default is 0.5). The RMS error goes from
   1.06 m to 5.46 m, and the true error is inside the ±1σ band only 25% of
   the time (an honest filter: about 68%). What does this show?

   A. The filter is honest, only less accurate

   B. The filter is underconfident: its band is too wide

   C. **The filter is overconfident: its band is thin while the error is
      five times larger**

   D. The filter ignores the signs and drifts with the IMU

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   With :math:`Q` far too small, :math:`P` stays small, so :math:`K` stays
   small and the filter barely listens to the signs. It sounds confident
   (a thin band) while its error grows. The slide calls this the dangerous
   row: the reported :math:`\sigma` looks good and nothing else in the
   system notices. **B** is the opposite case, :math:`\sigma_a = 3`, with
   84% inside.


.. admonition:: Question 16
   :class: hint

   An AV that steers moves by :math:`x_k = x_{k-1} + v\,\Delta t \cos\theta`,
   where the heading :math:`\theta` is itself in the state. Which Kalman
   filter assumption breaks, and which alternative does the lecture use?

   A. The bell curve; the particle filter

   B. **Linear models; the EKF**

   C. No bias; a larger :math:`Q`

   D. Known :math:`Q` and :math:`R`; the NIS test

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   A matrix can only scale and add. No fixed :math:`F` times the state gives
   :math:`\cos\theta`, and a range sensor's :math:`\sqrt{\Delta x^2 +
   \Delta y^2}` has no fixed :math:`H` either, so you cannot even write the
   matrices. Freeze the heading to force a straight line and the prediction
   leaves the road on the first bend. The EKF replaces each curve by its
   tangent at the current estimate, at every step. Its cost: the
   Jacobians are derived by hand and are only good near the estimate.


.. admonition:: Question 17
   :class: hint

   With no exit sign in view, the AV under the first of two identical
   ceiling lights 25 m apart has two places it could be. A single bell
   curve with the same mean and spread has its mean at 12.5 m with
   :math:`\sigma = 12.6` m. What goes wrong, and what is the alternative?

   A. Nothing: the mean is the best guess

   B. The spread is too small; raise :math:`Q`

   C. **The mean lands between the lights, where the honest belief is
      zero; the particle filter carries many candidate states at once**

   D. The lights make the model nonlinear; use the EKF

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Every Kalman filter, including the EKF, keeps the belief as one bell
   curve: one peak. The honest belief here has two peaks, each with
   :math:`\sigma = 1.3` m and half the weight. One mean and one covariance
   average them and put the AV at 12.5 m, a place it cannot be, with no
   warning. The particle filter carries thousands of candidate states so
   the belief can sit in several places. Its cost: it scales badly as the
   state gets bigger.


.. admonition:: Question 18
   :class: hint

   The EKF does two jobs at every step. Which statement describes them?

   A. Both the estimate and :math:`P` go through the Jacobians

   B. Both the estimate and :math:`P` go through the real :math:`f` and
      :math:`h`

   C. **The estimate goes through the real** :math:`f` **and** :math:`h`;
      :math:`P` **goes through the Jacobians** :math:`F_k`, :math:`H_k`
      **(and** :math:`Q_k` **)**

   D. :math:`P` goes through :math:`f` and the estimate through
      :math:`F_k`

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The estimate rides the curve: :math:`\hat{\mathbf{x}}^- = f(\hat{\mathbf{x}},
   \mathbf{u})` and the expected reading is :math:`h(\hat{\mathbf{x}}^-)`.
   :math:`P` rides the tangent, :math:`P^- = F_k P F_k^\top + Q_k`, because
   a straight line keeps a bell curve a bell curve. In the 30° heading
   example, the EKF gives 17.32 ± 2.09 m against the true 16.95 ± 2.11 m:
   the width is close, but the mean is 0.37 m too far, because a straight
   line cannot see the bend.


.. admonition:: Question 19
   :class: hint

   A landmark stands 10 m off the road beside :math:`x = 20` m. The AV is
   really at 16 m, so the camera reads 10.77 m. In run 2 the estimate is
   :math:`\hat{x} = 10` m: the filter expects 14.14 m, a surprise of 3.37 m,
   and the tangent there has slope −0.71. Where does the update put the AV?

   A. 16.00 m, exactly on the truth

   B. **14.77 m, 1.23 m short of the truth**

   C. 15.98 m, almost on the truth

   D. 4.77 m, because the slope is negative

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The move is :math:`3.37/0.71 = 4.77` m, so :math:`10 + 4.77 = 14.77` m.
   Between 10 and 16 m the curve drops only 0.56 m of range per meter, so
   the tangent at 10 m is too steep and the correction too small. That
   slope is the Jacobian :math:`H`: a poor estimate gives a wrong :math:`H`.
   **C** is run 1, from a good estimate of 15.5 m, where the tangent lands
   near the truth.


.. admonition:: Question 20
   :class: hint

   Your motion model curves hard across its uncertainty, or it is only code
   (an HD-map search) with no slope to take. According to the lecture's
   "choosing a filter" summary, which filter fits, and at what cost?

   A. The KF, at no extra cost

   B. The EKF, with Jacobians derived by hand

   C. **The UKF: it moves a few chosen possible states through the real
      model, 2n + 1 = 7 runs per step for x, y, θ, and needs no slopes**

   D. The particle filter, because it is the cheapest

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The EKF's tangent works only if the curve is almost straight across
   every heading the AV might have. With a heading spread of 12°, the
   possible positions after 20 m form a banana, and the EKF's straight
   ellipse puts the mean at 20.00 m against a real 19.57 m, and claims too
   little uncertainty. The UKF takes a few chosen possible positions, moves
   each with the real model, and rebuilds the belief from where they land:
   :math:`2n + 1 = 7` runs for :math:`n = 3`, no slopes. **D** is wrong on
   both counts: the particle filter is for several peaks, and it scales
   badly with the state size.


.. admonition:: Question 21
   :class: hint

   Over all 19 sign matches of the tunnel hands-on, the NIS averages 1.39
   per match. A sign match reports two numbers, so the expected value is 2,
   and by chance alone the average of 19 lands anywhere from 1.2 to 3.0.
   What does this say about the filter?

   A. It is overconfident, because 1.39 is not 2

   B. It is underconfident, because 1.39 is below 2

   C. **It is honest: 1.39 lies inside the band chance allows**

   D. Nothing, because the NIS needs ground truth

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The NIS, :math:`\varepsilon = \boldsymbol{\nu}^\top S^{-1}\boldsymbol{\nu}`,
   compares each actual surprise with the size :math:`S` the filter
   predicted for it. An honest filter averages about 1 per number the
   sensor reports. An average of 19 values is not exactly 2: chance alone
   spreads it from 1.2 to 3.0, and 1.39 is inside. **A** and **B** read a
   gap that chance explains as a fault. **D** is wrong: the test uses only
   the surprises and :math:`S`, which the filter already has.


----


True or False (Questions 22 to 31)
==================================

.. admonition:: Question 22
   :class: hint

   Taking more readings from a receiver with a fixed offset brings their
   average closer to the truth.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   More readings shrink the wander of the average from noise (by
   :math:`\sigma/\sqrt{n}`), but a fixed shift is the same in every reading,
   so the average keeps it. Receiver B's 3.2 m offset stays 3.2 m however
   many readings you take. You can average away noise, but you can never
   average away bias.


.. admonition:: Question 23
   :class: hint

   For the six parked readings, the variance divides by 6 and not 5 because
   the mean used is the surveyed truth, not one worked out from the
   readings.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The slide says so: the mean here is the surveyed truth, 100.0 m, so the
   squared distances are averaged over all six readings. A mean worked out
   from the readings themselves calls for :math:`n - 1 = 5`.


.. admonition:: Question 24
   :class: hint

   During predict, :math:`P` can shrink if the motion model is good enough.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Predict computes :math:`P^- = FPF^\top + Q`: time passed and nothing
   outside the AV was measured. :math:`FPF^\top` leaks the speed error into
   position, and :math:`Q` adds a new, independent error, so variances add.
   With no sign match, :math:`P` only grows, which is the climbing half of
   the sawtooth.


.. admonition:: Question 25
   :class: hint

   If a sign match is badly wrong, the update :math:`P = (I - KH)P^-`
   shrinks :math:`P` less than for a good one.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The surprise :math:`\nu` does not appear in that line. :math:`P` shrinks
   by the same amount whether the reading was good or bad: the filter does
   not check. That is why the lecture later needs a separate test (the NIS)
   and gating, and why an EKF can become confident while it is wrong.


.. admonition:: Question 26
   :class: hint

   Because a sign match measures position only, the update cannot change
   the filter's speed estimate.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Predict tied speed to position (correlation +0.79 at :math:`t = 9.3`
   s), so the gain has a nonzero speed row, 0.14. The east position surprise
   of 0.74 m moved the speed by :math:`0.14 \times 0.74 = 0.10` m/s.


.. admonition:: Question 27
   :class: hint

   The Kalman gain :math:`K` is a tuning value the engineer picks once,
   like :math:`\sigma_a`.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   :math:`K` is recomputed at every sign match from :math:`P^-` and
   :math:`R`: nobody picks it. In the tunnel it was 0.8 for the 50 m / 53 m
   example and 0.65 at :math:`t = 9.3` s. What we choose are :math:`Q`
   (through :math:`\sigma_a`) and :math:`R`; the gain follows from them.


.. admonition:: Question 28
   :class: hint

   The AV drives exactly 20 m with a heading of 30° ± 12°. The average of
   how far east it gets, :math:`x = 20\cos\theta`, is
   :math:`20\cos 30^\circ = 17.32` m.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   :math:`x = 20\cos\theta` is a curve in :math:`\theta`: a bell curve goes
   in and a lopsided shape comes out, because no heading gets the AV past
   20 m. Its mean is 16.95 m. The curve at the mean, 17.32 m, is not the
   mean of the curve. That 0.37 m gap is exactly the error the EKF makes by
   pushing the estimate through one tangent.


.. admonition:: Question 29
   :class: hint

   If one sign in an EKF Jacobian is wrong, the filter stops with an error,
   so the mistake is easy to find.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A wrong sign still runs and even converges. In the EKF hands-on, ticking
   "wrong sign" in :math:`F_k` raises the heading error to 4.0° and drops the
   share of time inside 1σ to 30%, with no crash. That is why the lecture's
   second trap is to test the Jacobians: nudge each input, see how each
   output moves, and compare (``python3 ekf_curve.py --check-jacobian``).


.. admonition:: Question 30
   :class: hint

   Checking the covariance with the NIS requires knowing where the AV really
   is.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The NIS compares each surprise :math:`\nu` with :math:`S`, the size the
   filter predicted for it. Both come from the filter's own update, so no
   ground truth is needed and the test can run on the AV all the time. The
   "inside 1σ" check of the hands-on, by contrast, needs the true position,
   which the AV does not have on the road.


.. admonition:: Question 31
   :class: hint

   Gating (throw away a sign match with :math:`\varepsilon > 9.21`) only
   ever removes bad readings, so it is always safe.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Gating catches a wrong sign match, such as a misread sign number that is
   on time, normal-looking and 25 m wrong. The trap is a filter that is
   already wrong: every good reading then looks wildly off, and the filter
   rejects exactly the readings that would fix it. The lecture's remedy is to
   count rejections in a row and raise an alarm past a limit.


----


Short Answer (Questions 32 to 37)
=================================

.. admonition:: Question 32
   :class: hint

   Explain the difference between noise and bias, and use receivers A and B
   (both :math:`\sigma_x = 1.561` m, means 100.0 m and 103.2 m, AV parked at
   100.0 m) to show how you can tell that B's offset is bias.

.. dropdown:: Answer
   :class-container: sd-border-success

   Noise is random scatter about a center, and it averages away as you take
   more readings. Bias is the same shift every time, and no number of
   readings removes it. Precision is the word for noise, trueness for bias,
   and accuracy means both are small.

   A and B scatter by exactly the same :math:`\sigma`, so :math:`\sigma`
   cannot separate them. The check is the size of the offset: noise moves
   the average of six readings by only about
   :math:`\sigma/\sqrt{6} = 1.561/2.45 \approx 0.64` m, and B is 3.2 m off,
   five times that, so chance cannot explain it. The check needed an
   outside truth, the surveyed spot; :math:`\sigma` needs only the readings.


.. admonition:: Question 33
   :class: hint

   In plain words, what does the Kalman gain do? Use the tunnel example
   (prediction 50.0 m, :math:`\sigma = 2` m; sign match 53.0 m,
   :math:`\sigma = 1` m) and say what happens as the sign match gets worse.

.. dropdown:: Answer
   :class-container: sd-border-success

   The gain is the fraction of the surprise the filter acts on. The surprise
   is measured minus predicted, :math:`53 - 50 = 3` m, and the estimate
   moves :math:`K` times it. :math:`K` is the prediction's share of the
   total variance, :math:`4/(4 + 1) = 0.8`, so the estimate becomes
   :math:`50 + 0.8 \times 3 = 52.4` m with :math:`\sigma = 0.89` m, smaller
   than either source.

   Only the two :math:`\sigma` values decide. As the sign match's
   :math:`\sigma` grows, :math:`K` falls toward 0 and the filter stays with
   its prediction; a precise match drives :math:`K` toward 1. :math:`K` is
   recomputed at every sign match, never picked by hand.


.. admonition:: Question 34
   :class: hint

   In the tunnel hands-on, the filter's :math:`\sigma` along the tunnel
   forms a sawtooth. Explain why it climbs, why it drops, and why it
   settles (about 0.8 m just after a match, 1.3 to 1.7 m just before the
   next).

.. dropdown:: Answer
   :class-container: sd-border-success

   Between sign matches only the IMU drives the prediction. Every 0.1 s
   predict step leaks the speed error into position through
   :math:`FPF^\top` and adds :math:`Q`, and nothing outside the AV is
   measured, so :math:`\sigma` climbs (for example 0.81 to 1.35 m over 22
   steps).

   At each sign match the update removes part of the uncertainty,
   :math:`P = (I - KH)P^-`, so :math:`\sigma` drops (1.35 to 0.80 m with
   :math:`K = 0.65`). The longer the gap, the larger :math:`P^-` and the
   larger the next :math:`K`, and the further the estimate moves. After a few matches
   the growth between signs and the shrink at each sign cancel, and the
   curve repeats between the same two levels.


.. admonition:: Question 35
   :class: hint

   Explain the EKF's catch: why can it become more confident while it
   becomes less accurate?

.. dropdown:: Answer
   :class-container: sd-border-success

   A tangent is right only near where it touches, and the EKF draws it at
   its own estimate. If the estimate is off, the tangent is in the wrong
   place and the correction is the wrong size (run 2 of the landmark
   example ended at 14.77 m, 1.23 m short). If the error is large enough,
   the next estimate is worse, and the next Jacobian is drawn there: a
   feedback loop.

   Meanwhile :math:`P` shrinks at every update, right or wrong, because the
   surprise does not appear in :math:`P = (I - KH_k)P^-`. So the filter
   reports a smaller and smaller uncertainty around a worse and worse
   estimate. That is divergence.


.. admonition:: Question 36
   :class: hint

   Why is an overconfident filter more dangerous than an underconfident one,
   and how can the AV find out which it has without ground truth?

.. dropdown:: Answer
   :class-container: sd-border-success

   An underconfident filter reports a :math:`\sigma` that is too large: it
   wastes good information, but nothing downstream is misled. An
   overconfident filter reports a small :math:`\sigma` while its error is
   large, and a wrong filter does not crash, it keeps running. In the
   hands-on, :math:`Q` too small gave a thin band and an error five times
   larger (5.46 m against 1.06 m), and nothing else in the system noticed.

   The NIS checks it on the road: compare each surprise with :math:`S`, the
   size the filter predicted for it. If :math:`\varepsilon` keeps landing
   above the band (about 0.05 to 7.4 for a sign match giving :math:`x` and
   :math:`y`), :math:`Q` or :math:`R` is too small: overconfident. Below
   the band means underconfident; inside means its :math:`\sigma` can be
   trusted.


.. admonition:: Question 37
   :class: hint

   The Kalman filter assumes linear models and a one-peak bell curve. For
   each of the three "What breaks" cases in the lecture, name the
   alternative filter, what it does, and its cost.

.. dropdown:: Answer
   :class-container: sd-border-success

   **The model is not linear** (an AV that turns needs :math:`\cos\theta`, a
   range needs a square root): the **EKF** replaces each curve by its
   tangent at the current estimate, at every step. Cost: Jacobians derived
   by hand, good only near the estimate. It is the default, the one to use
   when the model curves gently.

   **The model curves too much across the uncertainty, or is only code**:
   the **UKF** moves a few chosen possible states through the real model
   and rebuilds the belief from where they land. Cost: :math:`2n + 1 = 7`
   runs of the model per step for :math:`x, y, \theta`, but no slopes.

   **The belief has more than one peak** (two identical lights): the
   **particle filter** carries thousands of candidate states at once.
   Cost: it scales badly as the state gets bigger, so it suits a small
   state. None of the three checks whether its confidence is deserved;
   that is the job of the NIS.
