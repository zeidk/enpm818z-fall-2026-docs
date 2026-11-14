====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Four take-home exercises, built on the Lecture 10 notes, :doc:`l10_lecture`.
They use only the lecture, with new numbers. Exercise 1 builds a speed
profile for another curve. Exercise 2 works one Pure Pursuit step by hand.
Exercise 3 checks the speed PID at a higher target speed. Exercise 4 plans
another lane change with a quintic.

.. note::

   Every exercise can be done with a calculator.

   **The lecture's values:** wheelbase :math:`L` = 2.875 m; steering limit
   0.7 rad (``steer_limit``); a full steering command turns the wheels
   1.222 rad; lookahead :math:`L_d` = 5 m; target speed 8 m/s; sideways
   acceleration at most :math:`a_{\mathrm{lat}}` = 2.0 m/s²; braking before
   a curve at 2.0 m/s² and speeding up after it at 1.5 m/s². The speed
   model: the most push is 0.75 × 4 = 3 m/s², and drag is
   :math:`0.15 + 0.012\,v^2` m/s². The PID gains: :math:`K_p` = 0.5,
   :math:`K_i` = 0.3, the I sum held within ±1 m. The lecture chose these
   values. Numbers that are not the lecture's are marked "chosen for this
   exercise".


.. dropdown:: Exercise 1. A Speed Profile for Another Curve
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Build the speed profile for a curve that is not the lecture's: the speed
   cap on the curve, where braking starts, and where the AV is back at the
   target speed.

   .. raw:: html

      <hr>

   **Specification**

   The path has one arc of radius :math:`R` = 15 m, from :math:`s` = 120 m
   to :math:`s` = 140 m, and is straight before and after it (all chosen for
   this exercise). The AV drives at the target, 8 m/s, until the profile
   says to slow down. Use "Speed Profile, Step 1" and "Speed Profile, Step 2"
   in the lecture.

   .. raw:: html

      <hr>

   **Part A. The cap**

   1. What is the arc's curvature :math:`\kappa`?
   2. At 8 m/s, how hard would the AV accelerate sideways on this arc? Is it
      under :math:`a_{\mathrm{lat}}`?
   3. What is the highest speed on the arc?

   .. raw:: html

      <hr>

   **Part B. Brake before, speed up after**

   4. Braking at 2.0 m/s², how many meters does the AV need to slow from
      8 m/s to the cap? At which :math:`s` must it start braking?
   5. Speeding up at 1.5 m/s² after the arc ends, at which :math:`s` is it
      back at 8 m/s?
   6. The lecture's tighter arc has :math:`R` = 5.98 m. Is its cap higher or
      lower than this arc's? Why?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 6, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`\kappa = 1/R` = 1/15 = 0.0667 per meter.

      Question 2: :math:`v^2/R` = 8² / 15 = 64 / 15 = 4.27 m/s², more than
      twice the 2.0 m/s² cap. The AV must slow down.

      Question 3: :math:`v = \sqrt{a_{\mathrm{lat}} R} = \sqrt{2.0 \times 15}
      = \sqrt{30}` = 5.48 m/s.

      Question 4: :math:`d = (v_1^2 - v_2^2)/(2a)` = (64 − 30) / (2 × 2.0)
      = 34 / 4 = 8.5 m. Braking starts at 120 − 8.5 = 111.5 m, so the AV is
      at 5.48 m/s where the arc begins.

      Question 5: (64 − 30) / (2 × 1.5) = 34 / 3 = 11.3 m, so the AV is back
      at 8 m/s at 140 + 11.3 = 151.3 m.

      Question 6: lower: :math:`\sqrt{2.0 \times 5.98}` = 3.46 m/s. A smaller
      radius is a tighter arc, and the cap :math:`\sqrt{a_{\mathrm{lat}} R}`
      shrinks with :math:`R`.


.. dropdown:: Exercise 2. One Pure Pursuit Step by Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run the four steps of "Code Pure Pursuit: Four Steps, Every 0.05 s" on one
   lookahead point, and find where the steering limit starts to cut the
   angle.

   .. raw:: html

      <hr>

   **Specification**

   The lookahead point is :math:`L_d` = 5 m from the rear axle: 4.77 m
   forward and 1.50 m to the left, in the AV's own frame (chosen for this
   exercise). Step 1 (find the point) and step 2 (write it in the AV's frame)
   are done; you do steps 3 and 4.

   .. raw:: html

      <hr>

   **Part A. The arc and the angle**

   1. Find the angle :math:`\alpha` from the heading to the lookahead point,
      in rad and degrees.
   2. Find the arc's curvature :math:`\kappa = 2\sin\alpha / L_d` and its
      radius :math:`R`. (Hint: :math:`\sin\alpha` is the sideways distance
      over :math:`L_d`.)
   3. Find the steering angle :math:`\delta = \arctan(L\kappa)`. Is it within
      the 0.7 rad limit? To which side does the AV steer?
   4. What steer value does the node send, from −1 to 1?

   .. raw:: html

      <hr>

   **Part B. The limit**

   5. Keep :math:`L_d` = 5 m, and move the lookahead point farther left: 3.0 m
      to the left, then 4.0 m. Find :math:`\delta` for each. Which one does
      the controller have to cut to 0.7 rad?
   6. How far to the left can the point be before the limit cuts the angle?
      (tan 0.7 = 0.842.)

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 6, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`\alpha = \operatorname{atan2}(1.50, 4.77)` =
      0.305 rad, 17.5°, to the left.

      Question 2: :math:`\sin\alpha` = 1.50 / 5 = 0.300, so
      :math:`\kappa` = 2 × 0.300 / 5 = 0.120 per meter, and
      :math:`R` = 1 / 0.120 = 8.33 m.

      Question 3: :math:`\delta = \arctan(2.875 \times 0.120) =
      \arctan(0.345)` = 0.332 rad, 19.0°. It is under 0.7 rad, and positive:
      the AV steers left, toward the point.

      Question 4: 0.332 / 1.222 = 0.272. The node divides by 1.222 rad, the
      wheel angle at a full steering command, not by 0.7.

      Question 5:

      1. 3.0 m left: :math:`\kappa` = 2 × (3.0 / 5) / 5 = 0.240 per meter,
         :math:`\delta = \arctan(2.875 \times 0.240) = \arctan(0.690)` =
         0.604 rad: within the limit.
      2. 4.0 m left: :math:`\kappa` = 2 × (4.0 / 5) / 5 = 0.320 per meter,
         :math:`\delta = \arctan(2.875 \times 0.320) = \arctan(0.920)` =
         0.744 rad: over 0.7, so the controller cuts it to 0.7 rad.

      Question 6: the limit is :math:`\tan\delta = L\kappa` = 0.842, so
      :math:`\kappa` = 0.842 / 2.875 = 0.293 per meter. Then
      :math:`\sin\alpha = \kappa L_d / 2` = 0.293 × 5 / 2 = 0.732, and the
      point is 0.732 × 5 = 3.66 m to the left.


.. dropdown:: Exercise 3. The Speed PID at 12 m/s
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Check what each part of the speed PID needs at a higher target speed: the
   throttle drag asks for, the gap P alone leaves, and whether the clamp
   still lets I hold the speed.

   .. raw:: html

      <hr>

   **Specification**

   The target speed is 12 m/s (chosen for this exercise); everything else is
   the lecture's. The settled speeds below come from the lecture's speed
   model at a steady speed, where the throttle × 4 must equal the drag; they
   are not measured runs. Use "Hold a Speed Against Drag", "Try P Alone" and
   "Size the Clamp" in the lecture.

   .. raw:: html

      <hr>

   **Part A. What 12 m/s needs**

   1. What is the drag at 12 m/s? What throttle holds that speed?
   2. Is 12 m/s under the AV's top speed?

   .. raw:: html

      <hr>

   **Part B. P alone**

   3. With P alone, the AV settles at 11.18 m/s. Check it: the throttle the
      drag needs at 11.18 m/s, and the throttle P makes from the gap.
   4. The gap at 8 m/s was 0.42 m/s. Why is it larger at 12 m/s?

   .. raw:: html

      <hr>

   **Part C. The clamp**

   5. With :math:`K_i` = 0.3 and the sum held within 1 m, how much throttle
      can the I term give at most? Is that enough to hold 12 m/s with no gap?
   6. With that clamp, the AV settles at 11.70 m/s. Check it: here P and the
      clamped I push together.
   7. What is the smallest clamp that lets I hold 12 m/s alone? Is the
      controller node's ``pid_windup_limit`` of 2.0 enough with
      :math:`K_i` = 0.3?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 7, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: drag = 0.15 + 0.012 × 12² = 0.15 + 1.728 = 1.88 m/s².
      Holding 12 m/s needs throttle 1.88 / 4 = 0.47.

      Question 2: yes: the top speed is 15.4 m/s, where the most push,
      3 m/s², meets drag.

      Question 3:

      1. Drag at 11.18 m/s: 0.15 + 0.012 × 11.18² = 0.15 + 1.50 = 1.65 m/s²,
         so the throttle needed is 1.65 / 4 = 0.41.
      2. P makes 0.5 × (12 − 11.18) = 0.5 × 0.82 = 0.41. The two match: the
         AV holds 11.18 m/s, 0.82 m/s short.

      Question 4: drag grows with the square of the speed, so 12 m/s needs
      more throttle (0.47 against 0.23 at 8 m/s). P makes throttle only from
      a gap, so it needs a larger gap.

      Question 5: :math:`K_i` × clamp = 0.3 × 1 = 0.3, under the 0.47 needed.
      Not enough: once the sum reaches the clamp, P must make the rest from a
      gap, so a gap stays.

      Question 6: drag at 11.70 m/s: 0.15 + 0.012 × 11.70² = 1.79 m/s², so
      the throttle needed is 1.79 / 4 = 0.45. P and I give
      0.5 × (12 − 11.70) + 0.3 = 0.15 + 0.3 = 0.45. They match: 0.30 m/s
      short, better than P alone.

      Question 7: the clamp must be larger than 0.47 / 0.3 = 1.57 m. The
      node's 2.0 is enough: 0.3 × 2.0 = 0.6, larger than 0.47.


.. dropdown:: Exercise 4. Another Lane Change with a Quintic
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Plan the move across the road for a slower lane change: its six
   conditions, its six numbers, and how fast the AV moves sideways.

   .. raw:: html

      <hr>

   **Specification**

   The AV starts on the right lane's center, not drifting (:math:`d = 0`,
   :math:`\dot d = 0`, :math:`\ddot d = 0`). It must end on the left lane's
   center, :math:`d_1` = 3.5 m, parallel to it, :math:`T` = 5 s from now
   (:math:`T` chosen for this exercise; the lecture worked :math:`T` = 4 s).
   Use "Work One d(t): Find Its Six Numbers" in the lecture.

   .. raw:: html

      <hr>

   **Part A. The six numbers**

   1. Write the six conditions, three at :math:`t = 0` and three at
      :math:`t = T`.
   2. Which three numbers do the start conditions fix, and to what?
   3. Find :math:`a_3`, :math:`a_4` and :math:`a_5`.
   4. Check them in the three end equations.

   .. raw:: html

      <hr>

   **Part B. Reading d(t)**

   5. Where is the AV at :math:`t` = 2.5 s, halfway through? What is on the
      road there?
   6. The sideways speed is largest halfway. Find it, and compare it with
      the lecture's 1.64 m/s for :math:`T` = 4 s.

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 6, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: at :math:`t = 0`: :math:`d = 0`, :math:`\dot d = 0`,
      :math:`\ddot d = 0`. At :math:`t = 5`: :math:`d = 3.5`,
      :math:`\dot d = 0`, :math:`\ddot d = 0`.

      Question 2: :math:`a_0 = d(0) = 0`, :math:`a_1 = \dot d(0) = 0`,
      :math:`a_2 = \ddot d(0)/2 = 0`.

      Question 3: with a straight start and end, the lecture's rule:

      1. :math:`a_3 = 10\,d_1/T^3` = 10 × 3.5 / 125 = 0.28
      2. :math:`a_4 = -15\,d_1/T^4` = −15 × 3.5 / 625 = −0.084
      3. :math:`a_5 = 6\,d_1/T^5` = 6 × 3.5 / 3125 = 0.00672

      Question 4:

      1. :math:`d(5)`: 0.28 × 125 − 0.084 × 625 + 0.00672 × 3125 =
         35 − 52.5 + 21 = 3.5 m.
      2. :math:`\dot d(5)`: 3 × 0.28 × 25 − 4 × 0.084 × 125 + 5 × 0.00672 ×
         625 = 21 − 42 + 21 = 0.
      3. :math:`\ddot d(5)`: 6 × 0.28 × 5 − 12 × 0.084 × 25 + 20 × 0.00672 ×
         125 = 8.4 − 25.2 + 16.8 = 0.

      Question 5: :math:`d(2.5)` = 0.28 × 15.625 − 0.084 × 39.0625 +
      0.00672 × 97.65625 = 4.375 − 3.281 + 0.656 = 1.75 m: on the dashed
      line between the two lanes.

      Question 6: :math:`\dot d(2.5)` = 3 × 0.28 × 6.25 − 4 × 0.084 × 15.625
      + 5 × 0.00672 × 39.0625 = 5.25 − 5.25 + 1.3125 = 1.31 m/s. Slower than
      the lecture's 1.64 m/s: the same 3.5 m over 5 s instead of 4 s.
