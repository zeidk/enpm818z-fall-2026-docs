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

This quiz covers Lecture 6: the AV's pose in the map frame and the accuracy it
needs, GNSS in a city and RTK, dead reckoning and its drift, fusion in the EKF
and the absolute pose error (APE), Monte Carlo localization (MCL), ICP scan
matching, integrity with the NIS gate and the protection level, and SLAM with a
pose graph and a loop closure. Every question can be answered from the slides
shown in class. Nothing on this page needs the appendix.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.
   - The recorded drive is the lecture's running example: 916 m in CARLA's
     Town10HD_Opt, two laps, with no GNSS from 250 m to 650 m along the
     route. Its sensor errors were all chosen for the drive: GNSS noise
     :math:`\sigma = 1.5` m with a bias of 0.5 m east and 0.3 m south,
     wheels 0.5% fast, gyro bias 0.001 rad/s.


----


Multiple Choice (Questions 1 to 22)
===================================

.. admonition:: Question 1
   :class: hint

   The localizer hands the AV's pose :math:`(x, y, \theta)` to the rest of
   the stack. What does :math:`\theta` measure?

   A. The angle from the AV's :math:`x` axis to the nearest wall.

   B. **The angle from the map's** :math:`x` **axis (east) to the AV's**
      :math:`x` **axis (forward), counterclockwise.**

   C. The steering angle of the front wheels.

   D. The angle from north to the AV's :math:`y` axis, clockwise.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The map frame is fixed to the ground: :math:`x` east, :math:`y` north, in
   meters from a chosen origin. The vehicle frame is fixed to the AV:
   :math:`x` forward, :math:`y` left. The pose says where the vehicle frame's
   origin sits in the map frame, and :math:`\theta` is the angle between the
   two :math:`x` axes, counterclockwise. CARLA's :math:`y` points right; the
   recorded drive flips it, so both frames turn counterclockwise. See the
   Introduction in :doc:`l6_lecture`.


.. admonition:: Question 2
   :class: hint

   The lecture quotes Reid and co-authors (2019) for a passenger car on local
   streets: "lateral and longitudinal error bounds of 0.29 m (0.10 m, 95%)".
   What does the 0.29 m bound mean?

   A. The average error of a good localizer.

   B. The error of an RTK receiver near its base station.

   C. **The error the AV must stay inside almost always: the paper derives it
      at a failure rate of** :math:`10^{-8}` **per hour of driving.**

   D. The width of a lane marking.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The bound is the error the car may have, sideways and along the road,
   and still be safe on a local street. The paper sets it so that the error
   goes past it less than once in 100 million hours of driving. On freeways
   the sideways bound is 0.57 m. The lecture compares every method against
   0.29 m. See the Introduction in :doc:`l6_lecture`.


.. admonition:: Question 3
   :class: hint

   In a city, GNSS fails in two ways: a blocked sky and multipath. Which
   statement is right?

   A. Both failures stop the fixes, so the AV always knows.

   B. A blocked sky gives fixes that look normal and are meters off.

   C. **A blocked sky stops the fixes, and the AV knows. Multipath gives a
      fix that looks normal and is meters off, and the AV does not know.**

   D. Multipath is noise, so averaging a few fixes removes it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   With too few satellites in view, the receiver gives a poor fix or none:
   an outage, and the fixes stop. In multipath, the signal bounces off a
   building before it reaches the antenna. The path is longer than the
   straight line, so the receiver computes the wrong position, and the fix
   looks normal. Multipath is a bias that comes and goes as the AV drives,
   and you cannot average a bias away (L3), so **D** is wrong. See GNSS and
   RTK in :doc:`l6_lecture`.


.. admonition:: Question 4
   :class: hint

   Over the drive's 72 GNSS fixes, the measured median error is 1.77 m. How
   does that compare with the local-street bound of 0.29 m?

   A. It is inside the bound.

   B. About 1.5 times too far off.

   C. **About 6 times too far off:** :math:`1.77 / 0.29 = 6.1`.

   D. About 12 times too far off.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`1.77 / 0.29 = 6.1`. Half the fixes are within 1.77 m, 95 percent
   within 3.39 m, and the worst is 5.44 m off. **D** uses the 95 percent
   value: :math:`3.39 / 0.29 = 11.7`. Plain GNSS cannot keep a car in its
   lane. The errors come from the noise and bias chosen for the drive: 1.5 m
   of noise in each direction and a fixed bias of about half a meter. See
   GNSS and RTK in :doc:`l6_lecture`.


.. admonition:: Question 5
   :class: hint

   What does RTK's base station do?

   A. It relays the satellite signals to the car through a cable.

   B. **It sits on a surveyed point, so it knows its own error. It sends that
      error to the car nearby as a correction, and the errors both receivers
      share cancel.**

   C. It measures the car's position with its own LiDAR.

   D. It replaces the satellites in a tunnel.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The base station sees the same satellites through nearly the same atmosphere as
   a car nearby. Errors both share, like the satellite clocks and the
   atmosphere, cancel. RTK also measures the carrier wave, not only the
   timing code. The reference the lecture quotes gives "performances in the
   range of a few centimetres", "in the vicinity of a base station". See
   GNSS and RTK in :doc:`l6_lecture`.


.. admonition:: Question 6
   :class: hint

   An RTK receiver reports a fix 2 cm from the truth in an open parking lot.
   The AV then drives into a street lined with glass towers, and the fixes
   keep coming, each one looking normal. Is the AV still within a few
   centimeters?

   A. Yes: RTK cancels every error.

   B. Yes: the fixes keep coming, so the sky is clear.

   C. **Not necessarily: multipath at the car is not in the base station's
      correction, so a normal-looking fix can be meters off.**

   D. No: RTK stops working as soon as the AV moves.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The base station is in the open. A bounce off the glass next to the car
   happens at the car alone, so the correction does not contain it. Fixes
   that keep coming only say the sky is not fully blocked. To notice a bad
   fix, the AV needs a second, independent source (the Integrity section).
   See GNSS and RTK in :doc:`l6_lecture`.


.. admonition:: Question 7
   :class: hint

   Dead reckoning updates the pose every :math:`\Delta t` with
   :math:`x \mathrel{+}= v\cos\theta\,\Delta t`,
   :math:`y \mathrel{+}= v\sin\theta\,\Delta t` and
   :math:`\theta \mathrel{+}= \omega\,\Delta t`. The AV drives north
   (:math:`\theta = 90^\circ`) at :math:`v = 10` m/s (chosen for this
   question), and :math:`\Delta t = 0.05` s, as on the drive. How far does
   one step move it?

   A. 0.5 m east.

   B. **0.5 m north:** :math:`x` **does not change.**

   C. 10 m north.

   D. 0.35 m east and 0.35 m north.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`\cos 90^\circ = 0` and :math:`\sin 90^\circ = 1`, so :math:`x`
   grows by 0 and :math:`y` by :math:`10 \times 1 \times 0.05 = 0.5` m.
   :math:`y` points north in the map frame. **C** forgets :math:`\Delta t`.
   The wheels give :math:`v` and the gyro gives :math:`\omega`. The same rule
   is the predict step of every filter in the lecture. See Dead Reckoning in
   :doc:`l6_lecture`.


.. admonition:: Question 8
   :class: hint

   The AV believes it faces :math:`2^\circ` off its true heading and drives
   straight. How far sideways is it after 100 m?

   A. 0.35 m

   B. 1.75 m

   C. **3.49 m**

   D. 200 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Sideways error :math:`= d \sin(\text{heading error})`, and
   :math:`\sin 2^\circ = 0.0349`, so :math:`100 \times 0.0349 = 3.49` m.
   **B** is the lecture's :math:`1^\circ` case:
   :math:`100 \times 0.01745 = 1.75` m. To stay under 0.29 m at
   :math:`2^\circ`, the AV can drive :math:`0.29 / 0.0349 = 8.3` m. A fixed
   heading error grows the sideways error by the same amount every meter.
   See Dead Reckoning in :doc:`l6_lecture`.


.. admonition:: Question 9
   :class: hint

   With a gyro bias :math:`b`, the AV driving straight at speed :math:`v`
   drifts sideways by about :math:`v\,b\,t^2/2`. With the lecture's
   :math:`v = 10` m/s and :math:`b = 0.001` rad/s, the drift after 20 s is
   2.0 m. What is it after 40 s?

   A. 4.0 m

   B. **8.0 m**

   C. 2.8 m

   D. 40 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`10 \times 0.001 \times 40^2 / 2 = 8.0` m. Twice the time, four
   times the error, because the heading error itself grows (:math:`b\,t`),
   so the sideways speed grows too. **A** treats the drift as growing in
   step with time, the way a fixed heading error grows with distance. The
   lecture's example gives 4.5 m after 30 s from the formula, and 4.54 m
   from a program that integrates step by step. See Dead Reckoning in
   :doc:`l6_lecture`.


.. admonition:: Question 10
   :class: hint

   On the drive, dead reckoning starts from the true pose at the last fix and
   runs through the 400 m without GNSS. What does the lecture measure?

   A. Under 0.29 m all the way: wheels and gyro are enough.

   B. **2.69 m after 100 m, a worst of 9.03 m at 329 m, and 7.84 m at the
      end of the outage.**

   C. An error that grows smoothly with the square of the distance.

   D. 0 m, because it starts from the true pose.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The error is 3.56 m after 200 m, and it does not grow smoothly (**C**):
   at some corners the two paths cross again. The trend is clear, though:
   meters of error against a bound of 0.29 m. Even the best start, the true
   pose, does not stop the drift (**D**). Dead reckoning bridges a short
   gap, never a long one. See Dead Reckoning in :doc:`l6_lecture`.


.. admonition:: Question 11
   :class: hint

   The fused filter keeps a state :math:`(x, y, \theta, v)` and its
   covariance :math:`P`. What happens to :math:`P` in each step?

   A. It grows at an update and shrinks at a predict.

   B. It stays the same; only the state changes.

   C. **It grows at every predict step and shrinks at every update.**

   D. It shrinks at every step.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Predict, every 0.05 s, moves the state with the dead-reckoning rule. The
   filter cannot check that step, so it is less sure: :math:`P` grows.
   Update, when a reading arrives, moves the state by a fraction :math:`K`
   of the surprise (L3), and :math:`P` shrinks. On the drive, the wheels
   update about :math:`v` every 0.05 s, and GNSS updates :math:`x` and
   :math:`y` once a second. See Fusion in the EKF in :doc:`l6_lecture`.


.. admonition:: Question 12
   :class: hint

   In the outage, the fused filter (GNSS, wheels and gyro, no map) reaches a
   real error of 9.50 m at its worst moment. Its own :math:`1\sigma` there is
   3.93 m. What does that say?

   A. The filter is honest: the error is inside :math:`3\sigma`.

   B. **The filter is overconfident: the real error is 2.4 times its own**
      :math:`1\sigma` (:math:`9.50 / 3.93`).

   C. The filter is underconfident: it thinks it is worse than it is.

   D. Nothing: :math:`1\sigma` and the error measure different things.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`P` grows in the outage, as it should: the band widens from 0.75 m
   before the outage to 3.93 m. But the error grows faster. The filter is less
   sure, but not unsure enough. One reason the lecture gives: its model has
   no gyro bias, and the drive has one. See Fusion in the EKF in
   :doc:`l6_lecture`.


.. admonition:: Question 13
   :class: hint

   The APE of a run is the RMSE of the distances from the estimated
   position to the true one. A run of four time steps has distances 0.2,
   0.2, 0.2 and 1.0 m (chosen for this question). What is its APE?

   A. 0.40 m

   B. 0.28 m

   C. **0.53 m**

   D. 1.00 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1. Square: 0.04, 0.04, 0.04, 1.00.
   2. Average: :math:`1.12 / 4 = 0.28`.
   3. Root: :math:`\sqrt{0.28} = 0.53` m.

   **A** is the plain average, 0.40 m. **B** forgets the root. The RMSE is
   larger than the average because squaring weighs the one bad step more.
   For a car, one bad moment matters more than many good ones. See Fusion in
   the EKF in :doc:`l6_lecture`.


.. admonition:: Question 14
   :class: hint

   The hands-on compares eight runs of the filter by their APE. Which input
   lowers the APE the most?

   A. GNSS through the outage.

   B. The wheels.

   C. **Map matching: through the outage, 4.99 m becomes 0.52 m.**

   D. None: all eight runs score about the same.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   With wheels and the outage, 4.99 m without the map and 0.52 m with it.
   With GNSS all the way, 1.28 m becomes 0.47 m. The wheels matter less in
   APE here: without them the outage run scores 4.58 m against 4.99 m, but
   its worst moment is worse, 12.4 m against 9.5 m. One run with the map
   fails: outage, no wheels, map, 27.66 m. See Fusion in the EKF in
   :doc:`l6_lecture`.


.. admonition:: Question 15
   :class: hint

   In Monte Carlo localization (MCL), what happens in the **weigh** step?

   A. Every particle moves with the wheels and the gyro.

   B. **For each particle, the scan is placed where that particle says the
      car is, and each scan point is scored by how close it lands to the
      map.**

   C. Heavy particles are copied and light ones dropped.

   D. The particle with the most weight becomes the only particle.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   MCL is L3's particle filter given a map. Each particle is one guess of the
   pose :math:`(x, y, \theta)`. **A** is predict (plus a little random
   noise), **C** is resample. The scoring uses a likelihood field: a scan
   point on a wall is likely, a point in empty space is not. The estimate is
   the weighted mean of the particles, and their spread is how sure MCL is.
   See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 16
   :class: hint

   In a chosen 20 m by 10 m box, MCL starts with 2000 particles anywhere,
   with any heading. Over 20 runs, 9 end on the mirror pose. With one small
   pillar near a corner, 0 do. Why?

   A. The pillar adds more scan points, so MCL runs faster.

   B. 2000 particles are too few for any box.

   C. **A plain box turned half a turn looks the same, so the scan cannot
      tell the two poses apart. The pillar makes them look different.**

   D. The pillar blocks the LiDAR, so fewer particles survive.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The plain box has two poses that see the same walls: the true one and the
   one opposite it through the box's center. MCL picks one of them. On real
   roads, a long street of identical blocks looks the same in many places.
   MCL needs something distinctive, or a rough GNSS fix to rule out the
   look-alikes. See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 17
   :class: hint

   Why does ICP, iterative closest point, have to iterate?

   A. Because the rotation formula is only approximate, and each round makes
      it more accurate.

   B. **If we knew which map point each scan point hit, the best pose would
      be one formula; if we knew the pose, we would know the pairs. We know
      neither, so ICP guesses the pairs from the nearest points, solves,
      moves the scan, and guesses again.**

   C. Because the map changes between iterations.

   D. Because each iteration adds one more scan.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The first pairs are partly wrong, but the move brings the scan closer, so
   the next pairs are better. ICP stops when the fit stops improving. On one
   scan of the drive, started :math:`5^\circ` off, 1.5 m east and 1.0 m
   south of the truth (chosen), it took 28 iterations. The RMSE of the pairs
   fell from 1.32 m to 0.06 m, and the final pose was 0.02 m from the truth.
   See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 18
   :class: hint

   In 2-D, ICP's rotation has a short form:
   :math:`\alpha = \operatorname{atan2}(H_{12} - H_{21},\ H_{11} + H_{22})`.
   A cross-covariance comes out as
   :math:`H = \begin{pmatrix} -4 & 5 \\ -1 & -2 \end{pmatrix}` (chosen for
   this question). What is :math:`\alpha`?

   A. :math:`-45^\circ`

   B. :math:`45^\circ`

   C. :math:`\mathbf{135^\circ}`

   D. :math:`90^\circ`

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`H_{12} - H_{21} = 5 - (-1) = 6` and
   :math:`H_{11} + H_{22} = -4 + (-2) = -6`. atan2 takes the first number as
   the up part and the second as the right part. The point 6 up and 6 to the
   left lies at :math:`135^\circ`, so
   :math:`\operatorname{atan2}(6, -6) = 135^\circ`. **A** is the plain arc
   tangent of :math:`6 / (-6) = -1`, which loses the quadrant: that is why
   the formula uses atan2. See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 19
   :class: hint

   An ICP fit finds the rotation :math:`R = \begin{pmatrix} 0 & -1 \\ 1 & 0
   \end{pmatrix}` (a quarter turn counterclockwise). The scan's centroid is
   :math:`\bar p = (1, 2)` and the map's is :math:`\bar q = (3, 4)` (both
   chosen for this question). What is the shift :math:`t = \bar q - R\,\bar p`?

   A. (2, 2)

   B. (1, 6)

   C. **(5, 3)**

   D. (3, 4)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`R\,\bar p = (0 \times 1 - 1 \times 2,\ 1 \times 1 + 0 \times 2) =
   (-2, 1)`, so :math:`t = (3 - (-2),\ 4 - 1) = (5, 3)`. **A** forgets to
   rotate :math:`\bar p` first: :math:`\bar q - \bar p`. **D** is right only
   when the scan's centroid is the origin, as in the lecture's example,
   where :math:`t = (2, 1) = \bar q`. See Against a Map in
   :doc:`l6_lecture`.


.. admonition:: Question 20
   :class: hint

   The run "outage, no wheels, map matching" scores 27.66 m APE. For ten
   seconds every ICP pose is accepted. What goes wrong after that?

   A. The map is wrong in that part of the town.

   B. **One match is rejected and the next is dropped. With no wheels and
      no GNSS, nothing measures the speed, so the filter's position**
      :math:`\sigma` **passes 2 m, the limit chosen for starting ICP, and ICP
      stops. The filter coasts on the gyro alone, 65.6 m off at its worst.**

   C. ICP needs more than one scan per second.

   D. The NIS gate rejects every GNSS fix.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   At 45 s the NIS gate rejects one match. At 46 s the fit fails its quality
   check and is dropped. At 46.5 s :math:`\sigma` passes 2 m, and ICP stops.
   GNSS returns at 89.0 s and pulls the filter back. ICP keeps the AV
   localized only while it has a good starting guess. Once lost, the AV needs
   a method that searches widely: MCL, as Autoware does to "estimate initial
   position". See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 21
   :class: hint

   A filter accepts an update only if its NIS :math:`\varepsilon` is under
   the 0.99 bound for the number of values the update reports. Which bound
   applies to a matched pose from ICP?

   A. 9.21, because a pose is a position.

   B. **11.34, because a pose reports three numbers:** :math:`x`, :math:`y`
      **and** :math:`\theta`.

   C. 3, the NIS an honest filter averages for a pose.

   D. 0.99.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Both bounds come from the chi-square distribution at 0.99: 9.21 for 2
   numbers (a GNSS fix, :math:`x` and :math:`y`) and 11.34 for 3 numbers.
   **C** is the expected average, about 1 per number, not the gate. On the
   drive, with the outage, wheels and map: GNSS averages 2.12 over 68 fixes
   with 1 above 9.21, and the map averages 2.50 over 118 poses with 0 above
   11.34. See Integrity in :doc:`l6_lecture`.


.. admonition:: Question 22
   :class: hint

   The lecture defines an alert limit and a protection level. When must the
   localizer warn that its pose cannot be used for lane-level driving?

   A. When the protection level is below the alert limit.

   B. **When the protection level is above the alert limit.**

   C. When the APE is above 0.29 m.

   D. When one GNSS fix is above the NIS gate.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The alert limit is "the largest position error allowable for safe
   operation"; for a car on a local street, Reid's 0.29 m. The protection
   level is a bound the localizer computes from its own covariance and error
   models, so that the true error goes past it only with a tiny, chosen
   probability. If that bound is above the alert limit, the pose may be too
   far off, so the localizer warns. **C** needs the truth, which a real car
   never has. See Integrity in :doc:`l6_lecture`.


----


True or False (Questions 23 to 33)
==================================

.. admonition:: Question 23
   :class: hint

   Of all the sensors in the lecture, GNSS is the only one that says where
   the AV is on Earth with no map and no starting point.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   A receiver times the signals from several satellites and solves for its
   position. Dead reckoning needs a starting pose, and MCL and ICP need a
   map. See GNSS and RTK in :doc:`l6_lecture`.


.. admonition:: Question 24
   :class: hint

   RTK cancels multipath at the car, because the base station sees the same
   satellites.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   RTK cancels errors the base station and the car share. A bounce off the
   building next to the car happens at the car alone, so the correction does
   not contain it. RTK also stops when the sky is blocked, and it works only
   near a base station. See GNSS and RTK in :doc:`l6_lecture`.


.. admonition:: Question 25
   :class: hint

   A fixed heading error makes the sideways error grow with the square of
   the distance driven.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A fixed heading error grows the sideways error by the same amount every
   meter: :math:`d \sin(\text{heading error})`, a straight line on the
   lecture's graph. A gyro **bias** makes the heading error itself grow, and
   then the sideways error grows with the square of **time**:
   :math:`v\,b\,t^2/2`. See Dead Reckoning in :doc:`l6_lecture`.


.. admonition:: Question 26
   :class: hint

   At the first GNSS fix after the 400 m outage, the filter's gain
   :math:`K` is small, so the filter moves only a little toward the fix.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   :math:`P` grew at every predict step of the outage, so at the first fix
   :math:`K` is **large**: the filter trusts its own position little and
   moves most of the way to the fix. :math:`P` drops in one step. On the
   drive, the error is back to 0.60 m one second after the first fix: L3's
   sawtooth, with one long tooth. See Fusion in the EKF in
   :doc:`l6_lecture`.


.. admonition:: Question 27
   :class: hint

   The APE of a run, the RMSE of its distances, is never smaller than the
   plain average of those distances.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Squaring weighs large distances more, so the RMSE is at least the average.
   The two are equal only when every distance is the same. In the lecture's
   example, 0.3, 0.4, 1.2 and 0.5 m give an RMSE of 0.70 m against an
   average of 0.60 m. See Fusion in the EKF in :doc:`l6_lecture`.


.. admonition:: Question 28
   :class: hint

   MCL's estimate is the single particle with the highest weight.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The estimate is the **weighted mean** of the particles, and their spread
   is how sure MCL is. On the drive, 2000 particles start within 20 m of the
   first GNSS fix with any heading. The error is first under 1 m at the 5th
   scan, 2.0 s in; after 10 s the median error is 0.20 m and the worst
   0.95 m. See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 29
   :class: hint

   In the hands-on, ICP started 7.2 m and :math:`20^\circ` off the truth
   still lands on the right walls.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Started 5 m and :math:`15^\circ` off, ICP lands within 0.10 m of the
   truth. Started 7.2 m and :math:`20^\circ` off, it ends 7 m off, on the
   wrong walls. ICP needs a starting guess close to the truth, and the
   filter's own pose is that guess. See Against a Map in :doc:`l6_lecture`
   and :doc:`l6_code`.


.. admonition:: Question 30
   :class: hint

   An NIS that averages well below the expected value (below 2 for a GNSS
   fix) means the filter is overconfident.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   NIS below what is expected means the surprises are smaller than the filter
   predicted: it overestimates its error, so it is **underconfident**. That
   is the safe side. On the drive the map poses average 2.50 against 3
   expected: the filter slightly overestimates the map's error. An
   overconfident filter has an NIS that is too large. See Integrity in
   :doc:`l6_lecture` and :doc:`/lectures/lecture3/l3_lecture`.


.. admonition:: Question 31
   :class: hint

   On the drive, 1 GNSS fix out of 68 is above the 9.21 bound. That alone
   shows the filter is broken.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   At 0.99, an honest filter puts about 1 update in 100 above the line. Over
   68 fixes that is :math:`0.01 \times 68 = 0.68` expected, so one is
   normal. The GNSS average, 2.12 against an expected 2, also says the filter
   is honest about GNSS. See Integrity in :doc:`l6_lecture`.


.. admonition:: Question 32
   :class: hint

   In a pose graph with one loop, the loop closure edge, measured by ICP and
   sure, takes most of the correction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Each edge takes a share of the gap in proportion to its variance
   :math:`\sigma^2`. In the lecture's example, each odometry edge
   (:math:`\sigma = 0.5` m) takes :math:`0.25 / 0.51 = 0.49` of the gap and
   the loop (:math:`\sigma = 0.1` m) only :math:`0.01 / 0.51 = 0.02`. The
   sure edge barely bends. See SLAM in :doc:`l6_lecture`.


.. admonition:: Question 33
   :class: hint

   Autoware's localizer uses NDT scan matching, and starts with the Monte
   Carlo method to estimate the initial position.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The lecture quotes Autoware: "a package for position estimation using the
   NDT scan matching method", and it uses "the Monte Carlo method" to
   "estimate initial position". MCL finds the car once, scan matching
   follows it. See Against a Map in :doc:`l6_lecture`.


----


Short Answer (Questions 34 to 39)
=================================

.. admonition:: Question 34
   :class: hint

   Dead reckoning drifts. Explain, with the lecture's numbers, why a heading
   error matters more than a speed error, and why a gyro bias is worse than a
   fixed heading error.

.. dropdown:: Answer
   :class-container: sd-border-success

   A speed error stretches the path along the road: the wheels read 0.5% fast,
   so after 400 m the AV is :math:`0.005 \times 400 = 2.0` m off along the
   road. A heading error pushes it sideways: :math:`1^\circ` gives
   :math:`100 \times 0.01745 = 1.75` m after 100 m, and the 0.29 m bound is
   gone after 16.6 m.

   A gyro bias makes the heading error itself grow, :math:`b\,t`, so the
   sideways error grows with the square of time: :math:`v\,b\,t^2/2`, 4.5 m
   after 30 s at 10 m/s with :math:`b = 0.001` rad/s. Twice the time, four
   times the error. Dead reckoning bridges only short gaps.


.. admonition:: Question 35
   :class: hint

   During the outage, the fused filter's error reaches 9.50 m while its own
   :math:`1\sigma` is 3.93 m. Explain what goes on in the filter, and what
   happens at the first fix after the outage.

.. dropdown:: Answer
   :class-container: sd-border-success

   With no position update, the filter only predicts, so :math:`P` grows and
   the band widens from 0.75 m to 3.93 m. The real error grows faster, 2.4
   times the band: the filter is overconfident. One reason is that its model
   has no gyro bias, and the drive has one.

   At the first fix, :math:`P` is large, so :math:`K` is large: the filter
   moves most of the way to the fix, and :math:`P` drops in one step. One
   second later the error is 0.60 m.


.. admonition:: Question 36
   :class: hint

   MCL and ICP both match a scan to the map. Say what each one is good at,
   and how a real stack such as Autoware uses the two together.

.. dropdown:: Answer
   :class-container: sd-border-success

   MCL tries thousands of guesses spread over a wide area, so it can find the
   car from a poor start: on the drive, from a 20 m circle with any heading,
   it is under 1 m after 2.0 s. It can pick a look-alike place when the map
   is symmetric.

   ICP takes one guess and improves it, and it is precise: 0.02 m from the
   truth on one scan. But it needs a starting guess close to the truth, or it
   slides into the wrong fit. So MCL finds the car once, and scan matching
   follows it, its pose sent to the filter as one more update. Autoware
   follows this pattern, with NDT as its scan matcher.


.. admonition:: Question 37
   :class: hint

   A filter's NIS gate makes two kinds of mistake. Name them, give the
   lecture's example of each, and say which kind of filter makes each one.

.. dropdown:: Answer
   :class-container: sd-border-success

   A false alarm rejects a good update: a scan full of parked trucks the map
   does not have matches badly, and the filter drops a pose that was right.
   The cost is a little more dead reckoning. A missed fault accepts a bad
   update: a multipath fix 3 m off (chosen) arrives after the outage, when
   :math:`P`, and so :math:`S`, is large, so :math:`\varepsilon` stays small
   and the filter moves 3 m the wrong way.

   An overconfident filter makes false alarms; an underconfident one misses
   faults. That is why the filter must be honest.


.. admonition:: Question 38
   :class: hint

   Why does the lecture want two independent sources of position, such as
   GNSS and map matching, for integrity?

.. dropdown:: Answer
   :class-container: sd-border-success

   A real car never knows the truth, so it cannot compute its own error. GNSS
   and map matching fail for different reasons: GNSS under a blocked sky or
   with multipath, map matching where the map is wrong or one place looks
   like another.

   If they agree, both are likely right. If they disagree, the AV at least
   knows that one is wrong and can warn. What the car does then is L13.


.. admonition:: Question 39
   :class: hint

   Explain how a loop closure corrects a drifted trajectory in a pose graph,
   and why fleets build their maps offline.

.. dropdown:: Answer
   :class-container: sd-border-success

   The AV comes back to a place it has seen, and ICP between the new scan and
   the old one measures the motion between two poses far apart in time. Added
   around the loop, the edges should sum to zero; the drift leaves a gap,
   0.71 m in the lecture's example. Solving the graph spreads that gap over
   the edges in proportion to their variances, so the unsure odometry edges
   take most of it and the sure loop closure barely bends.

   A fleet solves this once, offline, over many mapping drives, with time and
   people to check the result. The AV on the road then localizes against a
   fixed map, a smaller problem that is easier to check.
