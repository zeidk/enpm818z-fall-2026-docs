====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Seven take-home exercises, built on the Lecture 10 notes,
:doc:`l10_lecture`, and on the lecture's Town03 turn. They test only what
the deck teaches in class, never the lecture's "More detail" boxes.
Exercise 1 counts the states and arrows of the behavior layer, and
Exercise 2 ticks the road behavior tree. Exercise 3 builds a speed profile
for another curve, and Exercise 4 finds the bicycle model's turn rate and
circle. Exercise 5 works the PID by hand, Exercise 6 applies Pure Pursuit's
steering law, and Exercise 7 applies the Stanley law. Exercise 4 ends with a
check in the lecture's hands-on window.

.. note::

   Every exercise can be done with a calculator. The hands-on check needs
   ``l10_handson.py`` from folder ``lecture10`` of the course's Python
   repository (`README
   <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture10>`__),
   with numpy and matplotlib, and no CARLA server.

   **The lecture's values:** wheelbase :math:`L` = 2.875 m (chosen); the
   controller's steering limit, 0.7 rad; the wheel angle at full steering,
   1.222 rad; the cap on the sideways acceleration, 2.0 m/s²; one controller
   step, :math:`\Delta t` = 0.05 s. Steering and the sideways direction are
   positive to the left. Numbers that are not the lecture's are marked
   "chosen for this exercise".


.. dropdown:: Exercise 1. Count the States and the Arrows
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See how a flat FSM and a superstate grow differently when the behavior
   layer gets more concerns.

   .. raw:: html

      <hr>

   **Specification**

   The AV has the lecture's five road behaviors: Lane keep, Follow a slower
   car, Change lane, Stop at the line, Cross the intersection. The safety
   monitor now has four states (chosen for this exercise): Nominal,
   Caution, Degraded, Emergency.

   .. raw:: html

      <hr>

   **Part A. One flat FSM**

   1. How many states does one flat FSM need for the road behaviors and the
      monitor together?
   2. Lane keep to Follow: how many times is that arrow drawn?
   3. The monitor's Nominal to Caution: how many times is that arrow drawn?

   .. raw:: html

      <hr>

   **Part B. A superstate**

   4. The AV gets a sixth behavior, Park at the curb (chosen for this
      exercise). The AV must be able to make an emergency stop from every
      behavior. How many arrows to Emergency stop does a flat FSM of the
      six behaviors need? How many with the superstate Driving around them?

   .. raw:: html

      <hr>

   **Part C. A third concern**

   5. Add a third concern, the lights, with two states (chosen for this
      exercise): Off, On. How many states does one flat FSM need for the
      road behaviors, the monitor and the lights together?
   6. Compare that with question 1's count. By what factor did adding the
      lights multiply the state count, and why that factor?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 6, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: the AV is in one behavior and one monitor state at once,
      so the flat FSM needs a state for every pair: 5 × 4 = 20.

      Question 2: once per monitor state: 4 arrows.

      Question 3: once per behavior: 5 arrows.

      Question 4: a flat FSM needs one arrow from each behavior: 6 arrows.
      With the superstate Driving around all six, one arrow leaves Driving
      and stands for the 6. Adding a behavior inside Driving adds no arrow
      to Emergency stop.

      Question 5: 5 × 4 × 2 = 40 states.

      Question 6: 40 / 20 = 2, the lights' own state count. Each new
      concern multiplies the flat FSM's states by its own count, as in
      Harel's example of two components with 1000 states each:
      1000 × 1000 = 1,000,000 in the product.


.. dropdown:: Exercise 2. Tick the Road Behavior Tree
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run the road behavior tree by hand and see it switch actions with no
   arrows.

   .. raw:: html

      <hr>

   **Specification**

   Use the tree of "Pass a Slow Car or Follow It" in the lecture. Its root
   Fallback tries four branches from the left: a Sequence of condition 1
   and Stop at the line; a Sequence of conditions 2 and 3 and Change lane; a
   Sequence of condition 4 and Follow; and Lane keep. Its four conditions:

   1. A stop line is within 30 m ahead.
   2. The car ahead has driven under 6 m/s for 3 s.
   3. The left lane is free: no car within 30 m behind or 40 m ahead.
   4. A car is ahead in our lane, within 40 m.

   Five ticks, each chosen for this exercise:

   - **Tick A:** the next stop line is 80 m ahead; the nearest car in our
     lane is 60 m ahead, at 8 m/s; the left lane is empty.
   - **Tick B:** no stop line within 30 m; a car 30 m ahead in our lane has
     driven at 5 m/s for 2 s; the left lane is empty.
   - **Tick C:** as tick B, but the car has now driven at 5 m/s for 4 s,
     and the left lane has one car, 35 m behind us.
   - **Tick D:** a stop line is 25 m ahead; the car ahead has driven at
     5 m/s for 4 s; the left lane is empty.
   - **Tick E:** no stop line within 30 m; a car 45 m ahead in our lane
     drives at 7 m/s; the left lane is empty.

   .. raw:: html

      <hr>

   **Questions**

   1. For each tick, which condition nodes are ticked, and what does each
      return?
   2. For each tick, which action runs?
   3. In which ticks is a condition never checked, and why?

   .. raw:: html

      <hr>

   **Deliverable**

   A table with one row per tick: the conditions ticked, their results, and
   the action that runs.

   .. dropdown:: Guidance
      :color: success

      The root Fallback ticks its branches from the left and stops at the
      first one that does not fail. A Sequence stops at its first child
      that does not succeed, so a failed condition ends its branch.

      **Tick A.** Condition 1 fails (80 m is past 30 m). Condition 2 fails:
      the car ahead drives at 8 m/s. Condition 4 fails (60 m is
      past 40 m). Lane keep runs. Checked: 1 no, 2 no, 4 no.

      **Tick B.** Condition 1 fails. Condition 2 fails: 2 s is less than
      3 s. Condition 4 succeeds (30 m is within 40 m). Follow runs.
      Checked: 1 no, 2 no, 4 yes.

      **Tick C.** Condition 1 fails. Condition 2 succeeds (4 s at 5 m/s).
      Condition 3 succeeds: the car behind is 35 m away, past 30 m, and no
      car is ahead in the left lane. Change lane runs. Checked: 1 no,
      2 yes, 3 yes.

      **Tick D.** Condition 1 succeeds (25 m is within 30 m), so the first
      Sequence ticks Stop at the line. Stop at the line runs. Checked:
      1 yes.

      **Tick E.** Condition 1 fails. Condition 2 fails: 7 m/s is not under
      6 m/s. Condition 4 fails (45 m is past 40 m). Lane keep runs.
      Checked: 1 no, 2 no, 4 no.

      Question 3: condition 3 is checked only in tick C. In ticks A, B and
      E, condition 2 fails first, so the second Sequence stops before it.
      In tick D, condition 1 succeeds and the root stops at the first
      branch, so conditions 2 to 4 are never checked, as in the lecture's
      run of ``behavior_tree.py`` at 9.0 s.


.. dropdown:: Exercise 3. A Speed Profile for Another Curve
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Build a speed profile for one curve: the speed cap, where braking starts,
   where the AV is back at speed, and the steering in the curve.

   .. raw:: html

      <hr>

   **Specification**

   A straight road with one arc of radius 20 m (chosen for this exercise),
   from :math:`s` = 50 m to :math:`s` = 60 m. The AV drives at 8 m/s
   elsewhere, the lecture's target speed. As in the lecture: the cap on the
   sideways acceleration, :math:`a_{\mathrm{lat}}` = 2.0 m/s²; braking at
   2.0 m/s²; speeding up at 1.5 m/s² (all chosen in the lecture).

   .. raw:: html

      <hr>

   **Questions**

   1. What is the highest speed in the arc?
   2. How far does the AV brake, and at which :math:`s` does braking start?
   3. How far does the AV take to get back to 8 m/s, and at which :math:`s`
      is it back at 8 m/s?
   4. Which steering angle follows the arc? Is it within the controller's
      0.7 rad limit?
   5. Check: what is the sideways acceleration in the arc at the speed of
      question 1?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 5, with the arithmetic, and a sketch of the
   profile: speed against :math:`s`, with the four points of questions 2
   and 3 marked.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`v = \sqrt{a_{\mathrm{lat}} R} = \sqrt{2.0 \times 20}
      = \sqrt{40}` = 6.32 m/s.

      Question 2: :math:`d = (v_1^2 - v_2^2) / (2a)`:

      1. :math:`8^2 - 40` = 64 − 40 = 24.
      2. :math:`d` = 24 / (2 × 2.0) = 6.0 m.
      3. Braking starts at 50 − 6.0 = 44.0 m.

      Question 3: :math:`d` = 24 / (2 × 1.5) = 8.0 m, so the AV is at 8 m/s
      again at 60 + 8.0 = 68.0 m.

      Question 4: :math:`\delta = \arctan(L\kappa) = \arctan(2.875 / 20) =
      \arctan(0.144)` = 0.143 rad, well under 0.7 rad.

      Question 5: :math:`v^2 / R` = 40 / 20 = 2.0 m/s², the cap, as it must
      be: question 1 came from that cap.


.. dropdown:: Exercise 4. The Bicycle Model's Turn Rate and Circle
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use the kinematic bicycle model's third equation to find the turn rate,
   find the circle a fixed steering angle drives, and check a steering
   angle in the hands-on window.

   .. raw:: html

      <hr>

   **Specification**

   The AV drives at :math:`v` = 5 m/s, with the front wheel held at
   :math:`\delta` = 0.2 rad (both chosen for this exercise);
   :math:`\tan 0.2` = 0.203.

   .. raw:: html

      <hr>

   **Part A. The turn rate**

   1. Which of the model's four equations gives the turn rate? What is the
      turn rate, in rad/s?

   .. raw:: html

      <hr>

   **Part B. The circle**

   2. Held at 0.2 rad, the AV drives a circle. What is its radius?
   3. Check question 1 with that radius. Since :math:`R = L / \tan\delta`,
      the turn rate :math:`v\tan\delta / L` equals :math:`v / R`.
   4. Could this AV drive a circle of radius 3 m? Use the controller's
      steering limit.

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 4, with the arithmetic, and the hands-on
   check below.

   **Check in the hands-on.** Run ``python3 l10_handson.py --part bicycle``
   and find the steering angle that drives a 10 m circle. Compare it with
   :math:`\delta = \arctan(L/R)`.

   .. dropdown:: Guidance
      :color: success

      Question 1: the third equation,
      :math:`\dot\theta = \frac{v}{L}\tan\delta`, is where the steering
      enters: (5 / 2.875) × 0.203 = 1.739 × 0.203 = 0.353 rad/s.

      Question 2: :math:`R = L / \tan\delta` = 2.875 / 0.203 = 14.2 m.

      Question 3: :math:`v / R` = 5 / 14.2 = 0.352 rad/s, the same as
      question 1 up to rounding.

      Question 4: no. At the 0.7 rad limit, the smallest circle is
      :math:`R = 2.875 / \tan 0.7` = 3.41 m, larger than 3 m.

      Hands-on check: :math:`\delta = \arctan(2.875 / 10) = \arctan(0.2875)`
      = 0.280 rad. Compare it with the angle the window gives for a 10 m
      circle.


.. dropdown:: Exercise 5. The Speed PID by Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict P alone's steady gap, and run one PID step with the clamp.

   .. raw:: html

      <hr>

   **Specification**

   The lecture's speed model: full throttle gives 4 m/s², drag takes
   :math:`0.15 + 0.012\,v^2` m/s². The target is 8 m/s. The three terms of
   "Hold the Target Speed: the Speed Loop" in the lecture,
   :math:`K_p e`, :math:`K_i \sum e\,\Delta t` and
   :math:`K_d (e_k - e_{k-1}) / \Delta t`, add to the command :math:`u`,
   with the sum of :math:`e\,\Delta t` held within the clamp as in
   "Anti-Windup: Clamp the Sum".

   .. raw:: html

      <hr>

   **Part A. P alone**

   1. With :math:`K_p` = 1.0 (chosen for this exercise), where does the AV
      settle? Use the lecture's two steps: the throttle that holds a speed
      against drag, and :math:`K_p e` = that throttle. Start from a guess of
      :math:`e` = 0.21 m/s and repeat the two steps once.
   2. Compare with the lecture's :math:`K_p` = 0.5. Does doubling
      :math:`K_p` close the gap?

   .. raw:: html

      <hr>

   **Part B. One step**

   Gains :math:`K_p` = 0.5, :math:`K_i` = 0.3, :math:`K_d` = 0.1, the sum
   held within ±1 m (the lecture's). The sum before this step is 0.98 m;
   the last error was :math:`e_{k-1}` = 0.7 m/s and this step's error is
   :math:`e_k` = 0.6 m/s (chosen for this exercise).

   3. Add :math:`e_k\,\Delta t` to the sum, then hold the sum within ±1 m.
      What is the sum?
   4. Compute the three terms and :math:`u_k`. Is it throttle or brake, and
      is it under the node's throttle limit of 0.75?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 4, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1:

      1. Guess :math:`e` = 0.21, so :math:`v` = 7.79 m/s. Drag:
         :math:`0.15 + 0.012 \times 7.79^2` = 0.15 + 0.728 = 0.878 m/s².
         Throttle: 0.878 / 4 = 0.220. Then :math:`e` = 0.220 / 1.0 =
         0.22 m/s.
      2. Again with :math:`e` = 0.22, :math:`v` = 7.78 m/s: drag
         0.15 + 0.726 = 0.876 m/s², throttle 0.219, :math:`e` = 0.22 m/s.

      The AV settles about 0.22 m/s short, near 7.78 m/s. This is a
      prediction from the two steps, not a measured run.

      Question 2: the gap about halves, from 0.42 to 0.22 m/s, but it does
      not close. P makes throttle only from an error, so some error always
      stays.

      Question 3: 0.98 + 0.6 × 0.05 = 0.98 + 0.03 = 1.01 m, held to 1.00 m.

      Question 4:

      1. P: 0.5 × 0.6 = 0.30.
      2. I: 0.3 × 1.00 = 0.30.
      3. D: 0.1 × (0.6 − 0.7) / 0.05 = 0.1 × (−2.0) = −0.20. The error
         shrank, so D pulls the command down.
      4. :math:`u_k` = 0.30 + 0.30 − 0.20 = 0.40. Above 0, so throttle,
         0.40, under 0.75.


.. dropdown:: Exercise 6. Pure Pursuit's Steering Law
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Apply Pure Pursuit's formula for the lookahead, the curvature and the
   steering angle, and see how the lookahead changes the curvature.

   .. raw:: html

      <hr>

   **Specification**

   The AV drives at :math:`v` = 7 m/s (chosen for this exercise). The
   lookahead scales with the speed, :math:`L_d = \max(3\ \mathrm{m},\
   0.75\ \mathrm{s} \times v)`, as in the lecture. The angle from the AV's
   heading to the lookahead point is :math:`\alpha` = −18° (chosen for this
   exercise).

   .. raw:: html

      <hr>

   **Questions**

   1. What is :math:`L_d` at this speed?
   2. What is the curvature of the arc, :math:`\kappa = 2\sin\alpha / L_d`?
      Does the AV turn left or right?
   3. With the lecture's wheelbase, :math:`L` = 2.875 m, what is the
      steering angle, :math:`\delta = \arctan(L\kappa)`? Is it within the
      controller's 0.7 rad limit?
   4. If the lookahead were fixed at 3 m instead (same :math:`\alpha`),
      would :math:`|\delta|` be larger or smaller? Compute it to check.
   5. At what speed does the scaled lookahead first exceed the fixed 3 m
      value?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 5, with the arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`0.75 \times 7` = 5.25 m, longer than 3 m, so
      :math:`L_d` = 5.25 m.

      Question 2: :math:`\sin(-18°)` = −0.309, so
      :math:`\kappa = 2 \times (-0.309) / 5.25` = −0.1177 /m. Negative: a
      right turn.

      Question 3: :math:`\delta = \arctan(2.875 \times (-0.1177)) =
      \arctan(-0.3384)` = −0.326 rad (−18.7°), under the 0.7 rad limit.

      Question 4: a shorter lookahead gives a larger magnitude. At
      :math:`L_d` = 3 m: :math:`\kappa = 2 \times (-0.309) / 3` =
      −0.206 /m, and :math:`\delta = \arctan(2.875 \times (-0.206))` =
      −0.535 rad (−30.6°), larger in magnitude than question 3's −0.326 rad.

      Question 5: :math:`0.75 v` = 3 m at :math:`v` = 4 m/s; above that
      speed the scaled lookahead is longer than 3 m.


.. dropdown:: Exercise 7. The Stanley Law by Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Apply the Stanley law with the lecture's signs, and see what :math:`k_s`
   does at a standstill.

   .. raw:: html

      <hr>

   **Specification**

   The law, with steering and :math:`e` positive to the left:

   .. math::

      \delta = \psi_e - \arctan\frac{k\,e}{v + k_s}

   The path points 0.1 rad to the left of the AV's heading:
   :math:`\psi_e` = 0.1 rad. The front axle is 0.5 m to the right of the
   path: :math:`e` = −0.5 m. Gain :math:`k` = 1 (all chosen for this
   exercise); :math:`k_s` = 1 m/s, as in the lecture.

   .. raw:: html

      <hr>

   **Questions**

   1. At :math:`v` = 4 m/s, what is the cross-track term, and what is
      :math:`\delta`? Which way does the AV steer?
   2. The AV stands still, :math:`v` = 0, with the same errors. What is
      :math:`\delta`? What would happen to the fraction without
      :math:`k_s`?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 and 2, with the arithmetic and the sign of
   each term.

   .. dropdown:: Guidance
      :color: success

      Question 1:

      1. The fraction: 1 × (−0.5) / (4 + 1) = −0.1.
      2. The cross-track term: :math:`-\arctan(-0.1)` = +0.100 rad. The AV
         is right of the path, so the term steers left, toward it.
      3. :math:`\delta` = 0.1 + 0.100 = 0.200 rad, to the left. Both terms
         agree: the path points left and the AV is right of it.

      Question 2:

      1. The fraction: 1 × (−0.5) / (0 + 1) = −0.5.
      2. :math:`\delta` = 0.1 − arctan(−0.5) = 0.1 + 0.464 = 0.564 rad, to
         the left, under the 0.7 rad limit.
      3. Without :math:`k_s`, the fraction would divide by :math:`v` = 0:
         it has no finite value. :math:`k_s` keeps it finite when the AV
         stands still.
