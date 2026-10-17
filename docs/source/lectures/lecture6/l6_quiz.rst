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

This quiz covers Lecture 6: the AV's pose in the map frame and the error bound
it must meet, GNSS in a city and RTK, dead reckoning and its drift, fusion in
the EKF and the absolute pose error (APE), Monte Carlo localization (MCL), ICP
scan registration and how a match goes into the filter, and SLAM with a pose
graph and a loop closure. Every question can be answered from the lecture
notes, :doc:`l6_lecture`. Nothing on this page needs
:doc:`Going Further <l6_appendix>`.

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

   B. The angle from the map's :math:`x` axis (east) to the AV's
      :math:`x` axis (forward), counterclockwise.

   C. The steering angle of the front wheels.

   D. The angle from north to the AV's :math:`y` axis, clockwise.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The map frame is fixed to the ground: :math:`x` east, :math:`y` north, in
   meters from a chosen origin. The vehicle frame is fixed to the AV, with
   its origin at the middle of the rear axle: :math:`x` forward, :math:`y`
   left. The pose says where the vehicle frame's origin sits in the map
   frame, and :math:`\theta` is the angle from the map's :math:`x` axis to
   the AV's :math:`x` axis, counterclockwise. See the Introduction in
   :doc:`l6_lecture`.


.. admonition:: Question 2
   :class: hint

   The lecture scores every method against an error bound of 0.29 m for a
   passenger car on a local street (Reid et al., 2019). What does that bound
   mean?

   A. The average error of a good localizer.

   B. The error of an RTK receiver near its base station.

   C. The largest position error that still keeps the AV in its lane. The
      error may pass it at most once in :math:`10^8` hours of driving.

   D. The width of a lane marking.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The paper defines it as "the allowable maximum position error of the
   vehicle to ensure it is within the lane". The lecture builds it in two
   steps. A 3.0 m lane and a 2.1 m wide car leave
   :math:`(3.0 - 2.1)/2 = 0.45` m on each side on a straight road, but only
   0.33 m in a turn of radius 20 m. A heading error of :math:`0.5^\circ`
   uses 0.04 m of that, so :math:`0.33 - 0.04 = 0.29` m is left for the
   position error. It is a limit for every moment, not an average, so
   **A** is wrong. See the Introduction in :doc:`l6_lecture`.


.. admonition:: Question 3
   :class: hint

   In a city, GNSS fails in two ways: a blocked sky and multipath. Which
   statement is right?

   A. Both failures stop the fixes, so the AV always knows.

   B. A blocked sky gives fixes that look normal and are meters off.

   C. A blocked sky stops the fixes, and the AV knows. Multipath gives a
      fix that looks normal and is meters off, and the AV does not know.

   D. Multipath is noise, so averaging a few fixes removes it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   With too few satellites in view, the receiver gives a poor fix or none:
   an outage, and the fixes stop. In multipath, the signal bounces off a
   building before it reaches the antenna. The path is longer, so the
   receiver puts the AV in the wrong place, and the fix looks normal. Noise
   you can average away; a bias you cannot. Multipath is a bias that comes
   and goes as the AV drives, so **D** is wrong. See GNSS and RTK in
   :doc:`l6_lecture`.


.. admonition:: Question 4
   :class: hint

   Over the drive's 72 GNSS fixes, the measured median error is 1.77 m. How
   does that compare with the local-street bound of 0.29 m?

   A. It is inside the bound.

   B. About 1.5 times too far off.

   C. About 6 times too far off: :math:`1.77 / 0.29 = 6.1`.

   D. About 12 times too far off.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`1.77 / 0.29 = 6.1`. Half the fixes are within 1.77 m, 95 percent
   within 3.39 m, and the worst is 5.44 m off. **D** uses the 95 percent
   value: :math:`3.39 / 0.29 = 11.7`. Plain GNSS cannot keep a car in its
   lane. These errors are the noise and bias chosen for the drive: CARLA
   simulates no multipath. See GNSS and RTK in :doc:`l6_lecture`.


.. admonition:: Question 5
   :class: hint

   What does RTK's base station do?

   A. It relays the satellite signals to the AV through a cable.

   B. It sits on a surveyed point, so it can work out its own GNSS error.
      It sends that error to receivers nearby as corrections, and the AV
      subtracts it from its own fix.

   C. It measures the AV's position with its own LiDAR.

   D. It replaces the satellites in a tunnel.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The base computes where it is from the satellites and compares that with
   the surveyed point: the difference is its error. Near the base, the AV's
   signals cross nearly the same air, so they are slowed by nearly the same
   amount, and the AV's fix has nearly the same error. In the lecture's
   example (numbers chosen), the base's error is 1.2 m east and 0.8 m north,
   the AV's raw fix is 1.3 m east and 0.7 m north, and the corrected fix is
   0.1 m east and 0.1 m south: :math:`\sqrt{0.1^2 + 0.1^2} = 0.14` m left
   over. Timing the carrier wave as well brings RTK to "a few centimetres"
   near a base. See GNSS and RTK in :doc:`l6_lecture`.


.. admonition:: Question 6
   :class: hint

   An RTK receiver reports a fix 2 cm from the truth in an open parking lot.
   The AV then drives into a street lined with glass towers, and the fixes
   keep coming, each one looking normal. Is the AV still within a few
   centimeters?

   A. Yes: RTK cancels every error.

   B. Yes: the fixes keep coming, so the sky is clear.

   C. Not necessarily: a bounce at the AV is not in the base station's
      correction, so a normal-looking fix can be meters off.

   D. No: RTK stops working as soon as the AV moves.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The base is in the open and has no bounce, so its correction holds none
   to subtract. Fixes that keep coming only say the sky is not fully
   blocked. That is why the lecture keeps GNSS and adds a second source
   beside it: one that keeps working without satellites and that, compared
   with GNSS, shows when a fix is wrong. See GNSS and RTK in
   :doc:`l6_lecture`.


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

   B. 0.5 m north: :math:`x` does not change.

   C. 10 m north.

   D. 0.35 m east and 0.35 m north.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`\cos 90^\circ = 0` and :math:`\sin 90^\circ = 1`, so :math:`x`
   grows by 0 and :math:`y` by :math:`10 \times 1 \times 0.05 = 0.5` m.
   :math:`y` points north in the map frame. **C** forgets :math:`\Delta t`.
   The wheels give :math:`v` and the gyro gives :math:`\omega`. The same rule
   moves the pose forward between readings in the EKF and in MCL. See Dead
   Reckoning in :doc:`l6_lecture`.


.. admonition:: Question 8
   :class: hint

   The AV believes it faces :math:`2^\circ` off its true heading and drives
   straight. How far sideways is it after 100 m?

   A. 0.35 m

   B. 1.75 m

   C. 3.49 m

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

   B. 8.0 m

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

   B. 2.69 m after 100 m, and a worst of 9.03 m at 329 m.

   C. An error that grows smoothly with the square of the distance.

   D. 0 m, because it starts from the true pose.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The worst error is :math:`9.03 / 0.29 = 31` times the bound. The error
   does not grow smoothly (**C**). CARLA's own gyro reads a little more
   turning than the AV makes in a turn, so most of the :math:`6.0^\circ`
   heading error comes at the corners, and the next straight drifts faster.
   After a corner, the old sideways error points along the new road, so the
   two paths can cross. Even the best start, the true pose, does not stop
   the drift (**D**). Dead reckoning is good for a short gap, never alone for
   long. See Dead Reckoning in :doc:`l6_lecture`.


.. admonition:: Question 11
   :class: hint

   The fused filter keeps a state :math:`(x, y, \theta, v)` and its
   covariance :math:`P`. What happens to :math:`P` in each step?

   A. It grows at an update and shrinks at a predict.

   B. It stays the same; only the state changes.

   C. It grows at every predict step and shrinks at every update.

   D. It shrinks at every step.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Predict, every 0.05 s, moves the state with the dead-reckoning rule. The
   filter cannot check that step, so it is less sure: :math:`P` grows.
   Update, when a reading arrives, compares the reading with what the state
   predicts (the innovation) and moves the state by a fraction :math:`K` of
   it, and :math:`P` shrinks. On the drive, the wheels give a reading of
   :math:`v` every 0.05 s, and GNSS gives :math:`x` and :math:`y` once a
   second. See Fusion in the EKF in :doc:`l6_lecture`.


.. admonition:: Question 12
   :class: hint

   In the outage, the fused filter (GNSS, wheels and gyro, no map) reaches a
   real error of 9.50 m at its worst moment. Its own :math:`1\sigma` there is
   3.93 m. What does that say?

   A. The filter knows its error well: the error stays inside its own
      :math:`1\sigma` band.

   B. The filter is overconfident: the real error is 2.4 times its own
      :math:`1\sigma` (:math:`9.50 / 3.93`).

   C. The filter is underconfident: it thinks it is worse than it is.

   D. Nothing: :math:`1\sigma` and the error measure different things.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`1\sigma` is the error the filter expects. Its band grows in the
   outage, as it should, because only predict steps run. But the real error
   is 2.4 times larger and stays above the band the whole outage: the filter
   believes it is closer to the truth than it is. See Fusion in the EKF in
   :doc:`l6_lecture`.


.. admonition:: Question 13
   :class: hint

   The APE of a run is the RMSE of the distances from the estimated
   position to the true one. A run of four time steps has distances 0.2,
   0.2, 0.2 and 1.0 m (chosen for this question). What is its APE?

   A. 0.40 m

   B. 0.28 m

   C. 0.53 m

   D. 1.00 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1. Square: 0.04, 0.04, 0.04, 1.00.
   2. Add: 1.12. Divide by 4: :math:`1.12 / 4 = 0.28`.
   3. Root: :math:`\sqrt{0.28} = 0.53` m.

   **A** is the plain average, 0.40 m. **B** forgets the root. The RMSE is
   larger than the average because squaring makes the one bad step count
   more. See Fusion in the EKF in :doc:`l6_lecture`.


.. admonition:: Question 14
   :class: hint

   The lecture compares eight runs of the filter by their APE. Which input
   lowers the APE the most?

   A. GNSS through the outage.

   B. The wheels.

   C. Map matching: through the outage, with wheel speed read, 4.99 m
      becomes 0.52 m.

   D. None: all eight runs score about the same.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   With wheel speed read and the outage, 4.99 m without the map and 0.52 m
   with it. With GNSS always, 1.28 m becomes 0.47 m. The wheels matter less
   here: in the outage without the map, the run without wheel speed scores
   4.58 m, only :math:`4.99 - 4.58 = 0.41` m from the run with it, because
   without GNSS or a map neither run can correct its drift. One run with the
   map gets lost: outage, no wheel speed, map, 27.66 m. See Fusion in the
   EKF in :doc:`l6_lecture`.


.. admonition:: Question 15
   :class: hint

   In Monte Carlo localization (MCL), what happens in the **weigh** step?

   A. Every particle moves with the wheels and the gyro.

   B. For each particle, the scan is placed as if the AV stood at that
      particle's pose, and each scan point is scored by how close it lands
      to the map.

   C. Heavy particles are copied and light ones dropped.

   D. The particle with the most weight becomes the only particle.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Each particle is one guess of the pose :math:`(x, y, \theta)`. MCL takes
   no new scan for a particle: it turns and shifts the one real scan with
   that particle's pose. A point that lands on a map point (:math:`d = 0`)
   scores 0.93, the highest; past 3 m it scores 0.033. **A** is predict
   (plus a little random noise), **C** is resample. See Against a Map in
   :doc:`l6_lecture`.


.. admonition:: Question 16
   :class: hint

   In a chosen 20 m by 10 m room, MCL starts with 2000 particles anywhere,
   with any heading. Over 20 runs, 9 end on the mirror pose. With one small
   pillar in the room, 0 do. Why?

   A. The pillar adds more scan points, so MCL runs faster.

   B. 2000 particles are too few for any room.

   C. A plain room turned half a turn looks the same, so the scan fits the
      mirror pose as well as the true one. The pillar makes the two poses
      look different.

   D. The pillar blocks the LiDAR, so fewer particles survive.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   In the plain room, more scans or random particles cannot undo a wrong
   choice, because every scan fits the mirror pose too. Only the true pose
   sees the pillar where the map has it. Without a pillar, MCL needs
   information from outside the map: with the particles placed around a
   GNSS fix, 0 of 20 runs end on the mirror. See Against a Map in
   :doc:`l6_lecture`.


.. admonition:: Question 17
   :class: hint

   Why does ICP, iterative closest point, have to iterate?

   A. Because the rotation formula is only approximate, and each round makes
      it more accurate.

   B. If we knew which map point each scan point hit, the best pose would
      be one formula; if we knew the pose, we would know the pairs. We know
      neither, so ICP guesses the pairs from the nearest points, solves,
      moves the scan, and guesses again.

   C. Because the map changes between iterations.

   D. Because each iteration adds one more scan.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The first pairs are partly wrong, so one move goes only part of the way,
   but the next pairs are better. On one scan of the drive, started
   :math:`5^\circ`, 1.5 m east and 1.0 m south off the truth (chosen), ICP
   took 28 rounds. The RMSE of the pairs fell from 1.32 m to 0.06 m, and the
   final pose was 0.02 m from the truth. See Against a Map in
   :doc:`l6_lecture`.


.. admonition:: Question 18
   :class: hint

   In 2-D, step 4 of ICP's step 2 gives the angle as
   :math:`\alpha = \operatorname{atan2}(H_{12} - H_{21},\ H_{11} + H_{22})`.
   A matrix comes out as
   :math:`H = \begin{pmatrix} -4 & 5 \\ -1 & -2 \end{pmatrix}` (chosen for
   this question). What is :math:`\alpha`?

   A. :math:`-45^\circ`

   B. :math:`45^\circ`

   C. :math:`135^\circ`

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
   the formula uses atan2. See "ICP step 2 in general" in
   :doc:`l6_lecture`.


.. admonition:: Question 19
   :class: hint

   An ICP fit finds the rotation :math:`R = \begin{pmatrix} 0 & -1 \\ 1 & 0
   \end{pmatrix}` (a quarter turn counterclockwise). The scan's centroid is
   :math:`\bar p = (1, 2)` and the map's is :math:`\bar q = (3, 4)` (both
   chosen for this question). What is the shift :math:`t = \bar q - R\,\bar p`?

   A. (2, 2)

   B. (1, 6)

   C. (5, 3)

   D. (3, 4)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`R\,\bar p = (0 \times 1 - 1 \times 2,\ 1 \times 1 + 0 \times 2) =
   (-2, 1)`, so :math:`t = (3 - (-2),\ 4 - 1) = (5, 3)`. **A** forgets to
   turn :math:`\bar p` first: :math:`\bar q - \bar p`. **D** would be right
   only if the scan's centroid were the origin, so that
   :math:`R\,\bar p = (0, 0)`. Step 6 puts the turned scan centroid on the
   map centroid. See "ICP step 2 in general" in :doc:`l6_lecture`.


.. admonition:: Question 20
   :class: hint

   The run "GNSS outage, no wheel speed, map matching" scores 27.66 m APE.
   From 35 s to 44 s every ICP match is used. What goes wrong after that?

   A. The map is wrong in that part of the town.

   B. Two matches in a row are thrown out. With no wheel speed and no GNSS,
      nothing tells the filter how far the AV moves, so it grows too unsure
      to give ICP a good start, and ICP is no longer run. The filter knows
      only how the AV turns, and it ends up 65.6 m off.

   C. ICP needs more than one scan per second.

   D. The filter throws out every GNSS fix.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   At 45 s a match is thrown out because it puts the AV too far from where
   the filter expected it. At 46 s the next one is thrown out because the
   scan does not line up well with the map. From 46.5 s the filter is too
   unsure to start ICP. It is 65.6 m off at 79.2 s, and GNSS brings it back
   at 89.0 s. ICP keeps the AV located only while it starts from a good
   guess. To find itself again, the AV needs a method that searches widely:
   MCL. See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 21
   :class: hint

   MCL has :math:`N = 4` particles with weights 0.4, 0.3, 0.2 and 0.1
   (chosen for this question). Our code resamples only when
   :math:`N_\text{eff} = 1 / \sum_i w_i^2` is below :math:`N/2`. What is
   :math:`N_\text{eff}`, and does MCL resample?

   A. :math:`N_\text{eff} = 1.0`: resample.

   B. :math:`N_\text{eff} = 3.33`: do not resample.

   C. :math:`N_\text{eff} = 0.30`: resample.

   D. :math:`N_\text{eff} = 4`: do not resample.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   1. Square each weight: 0.16, 0.09, 0.04, 0.01.
   2. Add them: 0.30.
   3. :math:`N_\text{eff} = 1 / 0.30 = 3.33`.
   4. The cutoff is :math:`N/2 = 4/2 = 2`. 3.33 is above it, so MCL does not
      resample.

   **C** forgets to take 1 over the sum. **D** would need four equal
   weights. When the weights are this even, resampling would drop guesses
   almost at random. See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 22
   :class: hint

   ICP runs in a long tunnel with straight walls on both sides. Which part
   of the pose can the scan not pin down?

   A. The heading.

   B. The distance to the walls.

   C. The position along the tunnel.

   D. None: ICP always fixes all three.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   One meter further along the tunnel, the AV sees the same walls at the
   same distance, so the scan cannot tell how far along it is. The lecture's
   number for this scene, a corridor, is 0.000: one direction where moving
   the AV does not change the scan at all. ICP still gives a position along
   the road, and nothing warns that this part is a guess. The fix: keep
   ICP's distance to the walls and its heading, and take the position along
   the road from the EKF's prediction. A corner (0.297) has no such problem.
   See Against a Map in :doc:`l6_lecture`.


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

   RTK cancels multipath at the AV, because the base station sees the same
   satellites.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The base, in the open, has no bounce, so its correction holds none to
   subtract. RTK also stops when the sky is blocked, and it is used only up
   to 10 or 20 km from the base: farther away, the two atmospheric delays
   differ. See GNSS and RTK in :doc:`l6_lecture`.


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
   :math:`P` is large next to the fix's noise and :math:`K` is near 1: the
   filter moves most of the way to the fix, and :math:`P` shrinks. On the
   drive, the error is 0.60 m one second after the first fix. See Fusion in
   the EKF in :doc:`l6_lecture`.


.. admonition:: Question 27
   :class: hint

   The APE of a run, the RMSE of its distances, is never smaller than the
   plain average of those distances.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Squaring makes large distances count more, so the RMSE is at least the
   average. The two are equal only when every distance is the same. In the
   lecture's example, 0.3, 0.4, 1.2 and 0.5 m give an RMSE of 0.70 m
   against an average of 0.60 m. See Fusion in the EKF in
   :doc:`l6_lecture`.


.. admonition:: Question 28
   :class: hint

   MCL's estimate is the single particle with the highest weight.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The estimate is the **weighted mean** of the particles,
   :math:`\hat{\mathbf{x}} = \sum_i w^{(i)}\,\mathbf{x}^{(i)}`, with the
   heading averaged as an angle. On the drive, 2000 particles start within
   20 m of the first GNSS fix (2.05 m from the AV), with any heading. The
   estimate is 3.06 m off at scan 1, 1.66 m at scan 4 (1.5 s) and 0.02 m at
   scan 16 (7.5 s). See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 29
   :class: hint

   In the lecture's made-up scene, ICP started 4 m from the AV and not
   turned always ends on the AV, whichever way the start is off.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Started 4 m ahead of the AV, ICP ends 0.10 m off after 18 rounds.
   Started 4 m to the AV's right, the same distance, it stops after 13
   rounds 7.55 m off and turned :math:`18^\circ`, on the wrong walls, with
   only 90 of its 126 points paired. ICP starts from the filter's pose, so
   the filter must keep it close. See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 30
   :class: hint

   Once MCL has found the AV on the drive (after 70 s), 2000 particles keep
   the error much lower than 200 particles do.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   After 70 s, all ten runs (five with 200, five with 2000) rise and fall at
   the same moments of the drive, to 0.80 to 1.11 m at worst. The peaks come
   from the drive, not from the number of particles. More particles help
   while the AV could be anywhere: with 2000, every run is within 2 m of the
   AV by 33.5 s; with 200, two runs stay 5 to 10 m off until 60.5 and
   64.0 s. See Against a Map in :doc:`l6_lecture`.


.. admonition:: Question 31
   :class: hint

   A k-d tree search finds the same nearest map point as checking every map
   point, but measures fewer distances.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The search skips a side of a line only when the line is farther from the
   query than the best distance found so far, so no closer point can sit
   there. In the lecture's example, the query :math:`(7.5, 5)` finds
   :math:`(9, 6)`, 1.80 m away, after 5 of the 8 distances. Checking every
   point finds the same :math:`(9, 6)`. See Against a Map in
   :doc:`l6_lecture`.


.. admonition:: Question 32
   :class: hint

   In a pose graph with one loop, the loop closure edge, measured by ICP and
   sure, takes most of the correction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Each edge takes a share of the gap in proportion to its variance
   :math:`\sigma^2`. In the lecture's example (chosen), the edges have
   :math:`\sigma` = 0.5 m (:math:`p_1` to :math:`p_2`), 0.3 m (:math:`p_2`
   to :math:`p_3`) and 0.1 m (the loop closure):

   1. Variances: 0.25, 0.09 and 0.01, together 0.35.
   2. Shares of the 0.71 m gap: :math:`0.25/0.35 = 71\%`, 0.51 m;
      :math:`0.09/0.35 = 26\%`, 0.18 m; :math:`0.01/0.35 = 3\%`, 0.02 m for
      the loop closure.

   The sure edge barely bends. See SLAM in :doc:`l6_lecture`.


.. admonition:: Question 33
   :class: hint

   Autoware uses MCL to estimate the AV's initial position, and NDT scan
   matching to keep estimating the position after that.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The lecture quotes Autoware: MCL to "estimate initial position", then
   NDT "for position estimation". MCL finds the AV from a wide search; scan
   matching follows it from a good start. See Against a Map in
   :doc:`l6_lecture`.


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

   A speed error stretches the path along the road: the wheels read 0.5%
   fast, so after 400 m the AV is :math:`0.005 \times 400 = 2.0` m off along
   the road, still in its lane. A heading error pushes it sideways:
   :math:`1^\circ` gives :math:`100 \times 0.01745 = 1.75` m after 100 m,
   and the 0.29 m bound is used up after 16.6 m.

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

   With no fix, the filter has only the wheels and the gyro: it predicts
   with the dead-reckoning rule, and :math:`P` grows at every step, so its
   :math:`1\sigma` grows. The real error grows faster, 2.4 times its
   :math:`1\sigma` at the worst moment, and stays above the band the whole
   outage: the filter is overconfident.

   At the first fix, :math:`P` is large next to the fix's noise, so
   :math:`K` is near 1: the filter moves most of the way to the fix, and
   :math:`P` shrinks. One second later the error is 0.60 m.


.. admonition:: Question 36
   :class: hint

   MCL and ICP both match a scan to the map. Say what each one is good at,
   and how a real stack such as Autoware uses the two together.

.. dropdown:: Answer
   :class-container: sd-border-success

   MCL weighs thousands of guesses spread over a wide area, so it can find
   the AV from a rough start: on the drive, from a 20 m circle around a GNSS
   fix with any heading, it is 0.02 m off by scan 16, 7.5 s in. It can pick
   a look-alike place when the map looks the same in two places.

   ICP takes one guess and moves it until the scan lies on the map, and it
   is precise: 0.02 m from the truth on one scan. But it needs a start close
   to the truth: from 4 m to the side, it stopped 7.55 m off. So MCL finds
   the AV, and scan matching follows it, its pose sent to the filter as one
   more update. Autoware uses MCL to "estimate initial position" and NDT
   after that.


.. admonition:: Question 37
   :class: hint

   The lecture's best run (GNSS always, wheel speed read, map matching)
   scores 0.47 m APE. Give the lecture's two reasons it misses the 0.29 m
   bound, with its numbers.

.. dropdown:: Answer
   :class-container: sd-border-success

   It starts meters off: the filter starts at 4.05 s from a GNSS fix, and
   map matching needs a good first guess, so the first match comes only at
   8.0 s. Until then the error is 0.6 to 2.4 m. Scored only from 8.0 s on,
   the run gets 0.38 m, still above the bound.

   It drifts between map matches: a match comes about once a second and
   brings the pose to about 0.2 m from the truth, and in the second until
   the next one the pose drifts again, most in turns. The bound is a limit
   for every step, not an average: about one step in three is above
   0.29 m.


.. admonition:: Question 38
   :class: hint

   Why does the lecture keep GNSS and add a second source of position, such
   as map matching, beside it?

.. dropdown:: Answer
   :class-container: sd-border-success

   GNSS stops when the sky is blocked, and with multipath it gives a fix
   that looks normal and is meters off, which RTK cannot correct. So the
   AV needs a source that keeps working without satellites and that,
   compared with GNSS, shows when a fix is wrong.

   Map matching fails for other reasons: a look-alike place, a scene that
   is blind along the road, or a start too far off. Before a match is used,
   the filter checks it against its own prediction, and if the check fails,
   the AV searches wider with MCL.


.. admonition:: Question 39
   :class: hint

   Explain how a loop closure corrects a drifted trajectory in a pose graph,
   and why fleets build their maps offline.

.. dropdown:: Answer
   :class-container: sd-border-success

   The AV comes back to a place it has seen, and ICP between the new scan and
   the old one measures where the new pose sits from the old one. Following
   the measured motions around the loop should lead back to the start; the
   drift leaves a gap, 0.71 m in the lecture's example. Solving the graph
   spreads that gap over the edges in proportion to their variances, so the
   unsure odometry edges take most of it and the sure loop closure barely
   bends. The whole path is corrected, not only the last pose.

   A fleet solves this once, offline, over its mapping drives, with time to
   check the result. The AV on the road then localizes against a fixed map,
   which keeps the online problem small and checkable.
