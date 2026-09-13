====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Working
   through this page is good preparation for one. Memorising the answers
   below is not.

This quiz covers Lecture 3: variance and confidence, weighting by certainty,
fusion architectures, the Kalman filter and its relatives, filter
consistency, and data association. Every question can be answered from the
lecture notes.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-19)
================================

.. admonition:: Question 1
   :class: hint

   Why does the definition of variance square the distances from the mean,
   instead of just averaging them?

   A. Because squaring makes the arithmetic easier

   B. **Because it removes the sign, and makes large errors count much more
      than small ones**

   C. Because the result then has the same units as the measurement

   D. Because it guarantees the result is less than one

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Squaring does two jobs. It stops a reading that is 2 m too high from
   cancelling a reading that is 2 m too low, which would wrongly suggest
   there was no spread at all. It also means a reading 10 m off contributes
   one hundred times as much as one 1 m off, not ten times, which is
   deliberate. **C is exactly backwards**: squaring gives you metres
   squared, and that is why we take the square root to get the standard
   deviation.


.. admonition:: Question 2
   :class: hint

   A GNSS receiver is tested against a surveyed point. Every single reading
   is 5.0 m too far north, with almost no scatter. What does this show?

   A. High variance and no bias

   B. **Low variance and large bias**

   C. High variance and large bias

   D. Low variance and no bias

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** low variance, large bias.

   Variance describes **spread**, not correctness. Every reading here is
   close to every other reading, and all of them are wrong by the same 5 m.
   A Kalman filter handles variance through :math:`R`, but it does **not**
   handle bias, because bias breaks the zero mean assumption. You either
   estimate it as part of the state or calibrate it out first.


.. admonition:: Question 3
   :class: hint

   A statistician tells you a 95% confidence interval for a measurement is
   from 4.2 to 4.8. What does the 95% actually mean?

   A. There is a 95% chance the true value lies between 4.2 and 4.8

   B. 95% of future measurements will land between 4.2 and 4.8

   C. **If the whole procedure were repeated many times, about 95% of the
      intervals produced would contain the true value**

   D. The measurement is 95% accurate

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, and **A is the classic mistake**.

   The 95% describes **the method**, not the one interval in front of you.
   Your particular interval either contains the true value or it does not,
   and you have no way to tell which. Because this is so easy to get wrong,
   the measurement standards GUM (JCGM 100:2008) and VIM (JCGM 200:2012)
   avoid the word entirely and use **coverage interval** and **coverage
   probability** instead.


.. admonition:: Question 4
   :class: hint

   What does the covariance reported by a Kalman filter actually claim?

   A. A frequentist confidence interval

   B. **A credible region, valid only if the filter's model is correct**

   C. The true error of the estimate

   D. Nothing; it is only a tuning parameter

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Under a Bayesian reading you may say "given my model, there is about a
   95% probability that the true state lies inside this ellipse." That is a
   stronger and more useful statement than a confidence interval. But the
   first three words carry all the weight: **given my model**. If the motion
   model, the noise sizes or the independence assumption is wrong, the
   ellipse is still drawn, still looks reasonable, and means nothing.


.. admonition:: Question 5
   :class: hint

   Two independent estimates of the same coordinate on a straight road:
   103.0 m with :math:`\sigma = 1.0` m, and 100.0 m with
   :math:`\sigma = 2.0` m. What do you report?

   A. 101.5 m, the average

   B. 103.0 m, just use the better sensor

   C. **102.4 m**

   D. 100.0 m, the more cautious reading

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** 102.4 m.

   Weights go as :math:`1/\sigma^2`, so they are 0.8 and 0.2, giving
   :math:`0.8(103.0) + 0.2(100.0) = 102.4`. Answer **A** assumes the sensors
   are equally trustworthy, which they are not. Answer **B** throws away
   real information from the second sensor.


.. admonition:: Question 6
   :class: hint

   A sensor's :math:`\sigma` is cut in half. What happens to its weight in
   the combined estimate?

   A. It doubles

   B. **It becomes four times larger**

   C. It stays the same

   D. It halves

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** four times larger.

   Weight goes as :math:`1/\sigma^2`, not :math:`1/\sigma`. **A sensor that
   is twice as good is four times as important.** This relationship is worth
   memorising.


.. admonition:: Question 7
   :class: hint

   You combine two independent estimates with :math:`\sigma_1 = 1.0` m and
   :math:`\sigma_2 = 2.0` m. The combined :math:`\sigma` is:

   A. Between 1.0 and 2.0 m

   B. Exactly 1.5 m

   C. **Less than 1.0 m**

   D. Greater than 2.0 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** 0.894 m, smaller than either input.

   Precisions add: :math:`1/\sigma_f^2 = 1/1 + 1/4 = 1.25`, so
   :math:`\sigma_f = 0.894`. Two independent measurements of the same
   quantity contain more information than either one alone, so the combined
   result is sharper than both. Most students pick **A**, reasoning that a
   worse sensor must dilute a better one. It does not.


.. admonition:: Question 8
   :class: hint

   In inverse-variance weighting, which quantity adds up?

   A. The standard deviations

   B. The variances

   C. **The precisions,** :math:`1/\sigma^2`

   D. The estimates

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** precisions add.

   :math:`1/\sigma_f^2 = 1/\sigma_1^2 + 1/\sigma_2^2`. This is exactly why
   the combined uncertainty is always smaller than either input. You cannot
   add a positive precision and come out less certain than you started.


.. admonition:: Question 9
   :class: hint

   Inverse-variance weighting requires the two error sources to be:

   A. Gaussian

   B. Zero mean

   C. **Independent**

   D. The same size

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** independent.

   If two estimates share a bias, such as the same mounting calibration
   error, the same clock, or the same patch of fog, the formula counts the
   same evidence twice and reports a confidence it has not earned. **Two
   identical forward cameras do not give you** :math:`\sigma/\sqrt{2}`. They
   give you :math:`\sigma` plus false confidence. This is L2's redundancy
   versus complementarity point written as mathematics.


.. admonition:: Question 10
   :class: hint

   Which fusion architecture keeps the most information, and what does it
   demand in return?

   A. Late fusion, and it demands more bandwidth

   B. **Early fusion, and it demands near perfect mounting calibration and
      very tight timing**

   C. Intermediate fusion, and it demands no calibration

   D. Late fusion, and it demands training data

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Early fusion combines raw measurements before anything is discarded, so
   nothing is thrown away. But every raw stream has to be expressed in one
   frame at one instant, which is exactly the calibration and timing problem
   from L2. It also moves enormous amounts of data and lets one bad sensor
   spoil everything.


.. admonition:: Question 11
   :class: hint

   Which Kalman filter step **always increases** the covariance?

   A. The update

   B. **The prediction**

   C. Both of them

   D. Neither; it depends on the gain

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** the prediction.

   :math:`P^- = FPF^\top + Q`, and :math:`Q` is always positive. Time
   passed, you learned nothing, so you are less sure than before. The update
   does the opposite, because evidence arrived.


.. admonition:: Question 12
   :class: hint

   The measurement noise :math:`R` is very large compared with the
   prediction covariance :math:`P`. What does the Kalman gain do?

   A. :math:`K \to 1`, and the filter jumps to the measurement

   B. **:math:`K \to 0`, and the measurement is effectively ignored**

   C. :math:`K = 0.5`, and the filter splits the difference

   D. :math:`K` goes negative

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`K = P/(P+R)`, so a large :math:`R` pushes :math:`K` toward zero.
   The sensor is telling you nothing you did not already know better, and
   the filter correctly declines to act on it.


.. admonition:: Question 13
   :class: hint

   In one dimension the Kalman gain is :math:`K = P/(P+R)`. What earlier
   result is that identical to?

   A. The Mahalanobis distance

   B. **The inverse-variance weight, with the prediction acting as the
      second sensor**

   C. The NIS

   D. Nothing; the gain is a separate idea

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   **The Kalman filter is the weighted average you already did, with a
   prediction step added in front.** The prediction is just another estimate
   with a variance, and the gain is its relative weight. Everything else,
   the matrices and the transposes, is that same idea carried into more
   dimensions.


.. admonition:: Question 14
   :class: hint

   No sensor measures velocity, yet velocity sits in the state and changes
   during the update. How is that possible?

   A. The filter differentiates the position estimates

   B. **Position and velocity are linked inside** :math:`P`, **so a surprise
      in position is evidence about velocity**

   C. The measurement matrix :math:`H` has a velocity row

   D. It is not possible, and would be a bug

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The prediction step advances position **using** velocity, which links
   them together. The off-diagonal entries of :math:`P^-` become non-zero
   even when :math:`P` was diagonal. So the gain has a non-zero velocity
   row, and a position measurement updates velocity. **This is the whole
   reason for putting unmeasured quantities in the state.**


.. admonition:: Question 15
   :class: hint

   What is the **innovation**, :math:`\boldsymbol{\nu}`?

   A. The difference between the estimate and the ground truth

   B. **The difference between what the sensor reported and what the filter
      expected it to report**

   C. How much the state changed between two steps

   D. The trace of the covariance matrix

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, that is :math:`\boldsymbol{\nu} = \mathbf{z} - H\hat{\mathbf{x}}^-`.

   Notice that **A** needs ground truth, which a real vehicle never has. The
   innovation uses only quantities the filter has already computed, which is
   why it can be watched at run time forever. It is the only genuinely new
   information in each cycle.


.. admonition:: Question 16
   :class: hint

   Of the four assumptions behind Kalman optimality, which one can you
   essentially never satisfy honestly?

   A. Linear models

   B. Gaussian noise

   C. **Knowing** :math:`Q`

   D. Knowing :math:`R`

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** knowing :math:`Q`.

   You can often measure :math:`R` by pointing the sensor at a known target
   and looking at the spread. :math:`Q` describes **how wrong your model of
   the world is**, and if you knew that you would have used a better model.
   You tune it, which means the optimality proof does not apply to any
   filter you have ever shipped. :math:`Q` is the parameter you are most
   likely to get wrong, and getting it wrong is what makes a filter
   overconfident.


.. admonition:: Question 17
   :class: hint

   Why is EKF divergence a **feedback loop** rather than a single mistake?

   A. Measurement noise builds up over time

   B. **A bad estimate gives a bad linearisation, which gives a worse
      estimate, while** :math:`P` **keeps shrinking anyway**

   C. The Jacobian grows without limit

   D. The particles degenerate

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Each step makes the next one worse. Critically, the update equation
   shrinks :math:`P` whether or not the update was any good. So the filter
   becomes **more confident as it becomes more wrong**. A small :math:`P`
   gives a small :math:`K`, a small :math:`K` means new measurements barely
   move anything, so the filter effectively ignores its inputs.


.. admonition:: Question 18
   :class: hint

   Which property decides that you need a **particle filter** instead of a
   UKF?

   A. The model is strongly nonlinear

   B. The state has many dimensions

   C. **The belief has several separate peaks**

   D. The measurement rate is high

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The deciding question is the **shape of the belief**, not how nonlinear
   the model is. A strongly nonlinear system with one peak is a UKF problem.
   Four aisles in a car park that match a LiDAR scan equally well cannot be
   one blob, and a filter forced to try puts its centre somewhere the car
   definitely is not. **B is an argument against** particle filters, since
   the number of particles needed grows brutally with dimension.


.. admonition:: Question 19
   :class: hint

   Why is Mahalanobis distance the right measure for data association rather
   than ordinary straight line distance?

   A. It is cheaper to compute

   B. It is always smaller

   C. **It measures disagreement in units of expected disagreement**

   D. It works in three dimensions

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A detection 2 m away from a track pinned down to 0.1 m is a terrible
   match. The same 2 m from a brand new track with 3 m of uncertainty is an
   excellent one. Ordinary distance reports 2 m in both cases and cannot
   tell them apart. Mahalanobis distance divides by the expected spread, so
   the same gap gets scored against what the track claims to know.


----


True or False (Questions 20-30)
===============================

.. admonition:: Question 20
   :class: hint

   A sensor with very low variance is therefore very accurate.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Variance measures **spread**, not correctness. A sensor whose every
   reading is 5 m too far north has almost zero variance and is useless.
   That steady offset is **bias**, it is a different problem, and the filter
   does not handle it.


.. admonition:: Question 21
   :class: hint

   Combining two estimates always gives a smaller uncertainty than either
   input.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**, and the exception is the dangerous part.

   It holds only when the errors are **independent**. If the two share a
   bias, the formula still reports a smaller :math:`\sigma`, and that number
   is a lie. Averaging two copies of the same mistake does not shrink it.


.. admonition:: Question 22
   :class: hint

   The Kalman update step can increase the covariance if the measurement is
   bad enough.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   :math:`P = (I-KH)P^-` shrinks the covariance regardless of whether the
   measurement was any good. **That is precisely why divergence is
   possible.** A filter fed nonsense still becomes more confident with every
   update.


.. admonition:: Question 23
   :class: hint

   :math:`Q` can be measured experimentally in the same way :math:`R` can.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   :math:`R` is a property of the sensor, so you can measure it against a
   known target. :math:`Q` describes how wrong your motion model is, and if
   you could measure that you would fix the model instead. :math:`Q` gets
   tuned, and it is the usual culprit when a filter is overconfident.


.. admonition:: Question 24
   :class: hint

   A Kalman filter that is provably optimal is therefore producing correct
   estimates.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Optimality is a claim **about the model you supplied**, not about the
   road. A filter can be provably optimal with respect to assumptions that
   are all wrong, and it will report a small covariance the entire time.


.. admonition:: Question 25
   :class: hint

   Chi-square gating can cause a filter to reject exactly the measurements
   that would have corrected it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**, and it is the same problem as L2's zero-Doppler filter.

   A gate rejects whatever disagrees with the current estimate. Once the
   estimate has drifted, the **good** measurements are the ones that
   disagree, so the gate defends the error. Gating protects a **healthy**
   filter from bad data. It cannot repair a sick one, which is why
   rejections must be counted and escalated instead of quietly piling up.


.. admonition:: Question 26
   :class: hint

   A tracked object's identity should be reset whenever its label changes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**, and this is the Tempe lesson.

   Killing the track every time the label changes means the track never
   builds up history, so it never has a velocity estimate, so there is no
   time to collision and nothing ever triggers braking. **Track the object,
   and label it separately.** A thing moving toward you matters whether or
   not you know what to call it.


.. admonition:: Question 27
   :class: hint

   Nearest neighbour association can give different answers depending on the
   order in which tracks are processed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Nearest neighbour is greedy. Whichever track is processed first claims
   its best detection, and later tracks take what is left. The same code on
   the same data gives different answers depending on track order, which
   also makes the resulting bug very hard to reproduce. GNN removes this by
   solving the whole frame at once.


.. admonition:: Question 28
   :class: hint

   Particle filters are a sensible default for high dimensional state
   estimation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The number of particles you need grows brutally with dimension. A
   particle filter with too few particles collapses onto one peak and
   quietly stops representing the others, which destroys the exact property
   you chose it for. Use it when the belief has several peaks **and** the
   state is small.


.. admonition:: Question 29
   :class: hint

   Running your filter under CARLA's rain and fog presets produces a valid
   degraded weather result.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**, and L2 measured this directly.

   LiDAR returns hold near 11,500 per sweep across all six weather presets,
   because CARLA's ray casting does not model attenuation at all. Inflating
   :math:`R` by hand to represent a degraded sensor is a perfectly good
   exercise, but **you** produced the degradation, in a constant. The
   simulator did not, and your write up has to say so.


.. admonition:: Question 30
   :class: hint

   A filter that detects its own inconsistency should automatically increase
   :math:`Q` until the NIS returns to its range.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   That hides the fault. Quietly retuning until the diagnostic looks healthy
   turns a problem you could have detected into one you cannot, which is the
   same argument L2 made about auto-correcting a large calibration
   deviation. A filter that has lost confidence in itself should say so, and
   the vehicle should slow down or stop.


----


Short Answer (Questions 31-36)
==============================

.. admonition:: Question 31
   :class: hint

   Define variance in your own words, explain why the distances are squared,
   and say why we usually quote a standard deviation instead.

.. dropdown:: Answer
   :class-container: sd-border-success

   Variance measures how spread out a set of readings is. Take each reading,
   find how far it sits from the average, square that distance, then average
   the squares. Formally,
   :math:`\operatorname{Var}(X) = \mathbb{E}[(X-\mu)^2]`.

   Squaring does two jobs. It removes the sign, so a reading 2 m too high
   and one 2 m too low do not cancel out and wrongly suggest zero spread. It
   also makes large misses count far more than small ones, which is
   deliberate, because in a vehicle one big error matters more than many
   tiny ones.

   Squaring leaves the answer in squared units, such as metres squared,
   which is hard to picture. Taking the square root gives the standard
   deviation :math:`\sigma`, back in metres, so it can be compared directly
   against the quantity being measured.


.. admonition:: Question 32
   :class: hint

   Explain why combining two independent estimates gives an uncertainty
   smaller than either one, and state exactly what that result depends on.

.. dropdown:: Answer
   :class-container: sd-border-success

   Two independent measurements of the same quantity contain more
   information than either one alone.
   Formally, precisions add:
   :math:`1/\sigma_f^2 = 1/\sigma_1^2 + 1/\sigma_2^2`, so the combined
   precision is larger than either one and the combined variance is smaller
   than both. Any other answer would mean you had thrown information away.

   It depends entirely on **independence**. If the two errors are linked, by
   a shared calibration, a shared clock or a shared mounting bracket, then
   the same evidence gets counted twice and the reported :math:`\sigma` is
   unearned. The estimate barely moves. The confidence is what breaks, and
   a wrong number claiming precision is far worse downstream than a wrong
   number that admits it is uncertain.


.. admonition:: Question 33
   :class: hint

   Describe the Kalman gain as a trust dial. Give its behaviour in both
   extremes and say what each one means physically.

.. dropdown:: Answer
   :class-container: sd-border-success

   :math:`K = P/(P+R)` is the fraction of the surprise the filter acts on.

   When :math:`R \ll P` the sensor is far better than the prediction, so
   :math:`K` goes to 1 and the filter jumps essentially to the measurement,
   dropping what it believed before. When :math:`R \gg P` the sensor adds
   nothing, so :math:`K` goes to 0 and the measurement is ignored. At
   :math:`R = P` the gain is 0.5 and the plain average is finally right.

   Physically, the gain is the filter continuously re-deciding which of its
   two information sources is currently more reliable: its own model of the
   world, or this sensor. It is the same inverse-variance weight from the
   one dimensional case, with the prediction acting as the second estimate.


.. admonition:: Question 34
   :class: hint

   Explain filter divergence as a sequence of steps, and say why it is an
   example of the kind of failure this course keeps returning to.

.. dropdown:: Answer
   :class-container: sd-border-success

   1. The update shrinks :math:`P`, because that is what
      :math:`(I-KH)P^-` does, whether or not the update was any good.
   2. A small :math:`P` produces a small :math:`K`.
   3. A small :math:`K` means incoming measurements barely move the
      estimate.
   4. The filter effectively ignores its inputs. The true error grows
      without limit while
      the reported covariance keeps getting smaller.

   The output is a confident, precise, completely wrong position, and
   **nothing raises an alarm**. L2 made the same point about hardware: a
   dirty sensor does not report an error, it reports data. Nothing
   downstream can detect the problem, which is why the covariance has to be
   tested rather than trusted.


.. admonition:: Question 35
   :class: hint

   You cannot use ground truth on a real vehicle. Explain how NIS lets you
   check a running filter anyway, and what the two out of range cases mean.

.. dropdown:: Answer
   :class-container: sd-border-success

   The filter computes the innovation :math:`\boldsymbol{\nu}` and its expected
   covariance :math:`S` every cycle, so it has already **predicted how big
   its own surprises should be**. The NIS
   :math:`\varepsilon = \boldsymbol{\nu}^\top S^{-1}\boldsymbol{\nu}` compares the
   surprises it actually got against that prediction, and should follow a
   chi-square distribution if the filter is honest. No outside reference is
   needed, so it runs on the vehicle forever.

   Landing repeatedly **above** the range means overconfidence. The real
   surprises are bigger than predicted, so :math:`P` or :math:`R` is too
   small, and usually it is :math:`Q`. Landing repeatedly **below** means
   underconfidence: the filter is wasting good information and converging
   slowly, which is inefficient but safe. Only inside the range does the
   reported uncertainty mean anything at all.


.. admonition:: Question 36
   :class: hint

   A tracker swaps the identities of two vehicles that cross. Explain why
   that is worse than losing both tracks completely.

.. dropdown:: Answer
   :class-container: sd-border-success

   If both tracks are **lost**, the system knows it. The objects drop back
   to tentative, the planner is told that nothing is confirmed, and a
   sensible stack becomes cautious. The failure announces itself.

   If the identities are **swapped**, every track stays confirmed and
   confident, but each one now carries the other one's history. The system
   reports two vehicles travelling in directions neither of them is going,
   with full confidence and no fault raised. The planner then avoids
   collisions that will never happen and ignores one that will.

   The general rule applies here as elsewhere in this course: a failure that
   reports confidence is worse than a failure that reports nothing. The same
   pattern appears in a blocked lens, a zero-Doppler discard, a multipath
   GNSS fix, and a diverging filter.
