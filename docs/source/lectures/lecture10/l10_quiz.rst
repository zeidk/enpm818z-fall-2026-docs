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

This quiz covers Lecture 10: the behavior layer beyond one flat FSM (a
superstate and behavior trees), trajectory generation, drive-by-wire, the
test turn and its speed profile, the kinematic bicycle model, PID speed
control and windup, Pure Pursuit and its lookahead distance, the Stanley
law, and what MPC adds. Every question can be answered from the lecture
notes, :doc:`l10_lecture`. This quiz tests only what the deck teaches in
class: nothing on this page needs the lecture's "More detail" boxes.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.
   - The lecture's example is one right turn in Town03, driven in a numpy
     simulation of the bicycle model: wheelbase :math:`L` = 2.875 m, the
     controller's steering limit of 0.7 rad, 20 controller steps a second
     (:math:`\Delta t` = 0.05 s), and a cap of 2.0 m/s² on the sideways
     acceleration. Numbers that are not the lecture's are marked "chosen
     for this question".


----


Multiple Choice (Questions 1 to 15)
===================================

.. admonition:: Question 1
   :class: hint

   The AV has the lecture's five road behaviors. You add a safety monitor
   with 4 states (chosen for this question). How many states does one flat
   FSM need for the behaviors and the monitor together?

   A. 9

   B. 15

   C. 20

   D. 24

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The AV is in one behavior and one monitor state at once, so one flat FSM
   needs a state for every pair: 5 × 4 = 20. The lecture's own monitor has
   3 states, for 5 × 3 = 15 (**B**); 9 (**A**) is 5 + 4, not a flat FSM's
   count. See "Step 1, the Problem: One Flat FSM Multiplies Its States" in
   :doc:`l10_lecture`.


.. admonition:: Question 2
   :class: hint

   The AV must be able to make an emergency stop from each of its five road
   behaviors (Lane keep, Follow, Change lane, Stop at the line, Cross the
   intersection). With the superstate Driving around those five, how many
   arrows go to Emergency stop?

   A. 1

   B. 3

   C. 5

   D. 15

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   An arrow that leaves a superstate stands for that arrow leaving every
   state inside it. So one arrow from Driving replaces the 5 arrows a flat
   FSM needs (**C**). Harel calls this "the main way statecharts economize
   in the number of arrows". See "Step 2, Fewer Arrows: One Superstate Arrow
   Replaces Five" in :doc:`l10_lecture`.


.. admonition:: Question 3
   :class: hint

   In a behavior tree, when does a Fallback node return Failure?

   A. When its first child returns Failure.

   B. When any one of its children returns Failure.

   C. Only when all its children return Failure.

   D. Never: a Fallback always returns Running.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A Fallback tries its children in order and stops at the first that
   succeeds or runs. In Colledanchise and Ögren's words, "It returns Failure
   if and only if all its children return Failure". A Sequence is the node
   that stops at the first child that fails (**A**). See "Read a Behavior
   Tree: Ticks, Three Statuses, Four Node Types" in :doc:`l10_lecture`.


.. admonition:: Question 4
   :class: hint

   The lecture's road tree is ticked. No stop line is within 30 m. A car is
   25 m ahead in our lane, driving at 7 m/s, and the left lane is free
   (chosen for this question). Which action does the tree run?

   A. Stop at the line

   B. Change lane

   C. Follow

   D. Lane keep

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The root Fallback tries its branches from the left. Condition 1 (a stop
   line within 30 m) fails, so the first Sequence fails. Condition 2 (the
   car ahead under 6 m/s for 3 s) fails, because the car drives at 7 m/s, so
   the second Sequence fails at its first child and condition 3 is never
   checked: a free left lane does not start a pass (**B**). Condition 4 (a
   car ahead within 40 m) succeeds at 25 m, so the third Sequence ticks
   Follow. The Fallback stops at this branch, because it did not fail, so
   Lane keep is not ticked. See "Pass a Slow Car or Follow It: Four Road
   Behaviors as a Behavior Tree" in :doc:`l10_lecture`.


.. admonition:: Question 5
   :class: hint

   A curve has radius 12.5 m (chosen for this question). With the lecture's
   cap on the sideways acceleration, 2.0 m/s², what is the highest speed in
   the curve?

   A. 3.54 m/s

   B. 5.0 m/s

   C. 6.25 m/s

   D. 25 m/s

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   On a circle of radius :math:`R` at speed :math:`v`, the sideways
   acceleration is :math:`v^2 / R`. From :math:`v^2 / R \le 2.0`, the
   highest speed is :math:`v = \sqrt{2.0 \times 12.5} = \sqrt{25}` =
   5.0 m/s. 3.54 (**A**) is :math:`\sqrt{12.5}`, without the 2.0; 6.25
   (**C**) is 12.5 / 2.0, and 25 (**D**) is :math:`2.0 \times 12.5` before
   the square root. See "Speed Profile, Step
   1: a Curve Caps the Speed" in :doc:`l10_lecture`.


.. admonition:: Question 6
   :class: hint

   The AV drives at 8 m/s and must be at 4 m/s (chosen for this question)
   when a curve starts. It brakes at the lecture's constant 2.0 m/s². How far
   before the curve must braking start?

   A. 2.0 m

   B. 8.0 m

   C. 12.0 m

   D. 24.0 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Slowing from :math:`v_1` to :math:`v_2` at a constant deceleration
   :math:`a` takes :math:`d = (v_1^2 - v_2^2) / (2a)`:

   1. :math:`8^2 - 4^2` = 64 − 16 = 48.
   2. :math:`2a` = 2 × 2.0 = 4.0.
   3. :math:`d` = 48 / 4.0 = 12.0 m.

   24.0 m (**D**) forgets the 2 in :math:`2a`. On the lecture's turn, the
   same rule gives 11.0 m for 8 to 4.47 m/s. See "Speed Profile, Step 2:
   Brake Before the Curve, Speed Up After It" in :doc:`l10_lecture`.


.. admonition:: Question 7
   :class: hint

   In the kinematic bicycle model, which equation is where the steering
   angle :math:`\delta` enters?

   A. :math:`\dot x = v\cos\theta`

   B. :math:`\dot y = v\sin\theta`

   C. :math:`\dot\theta = \frac{v}{L}\tan\delta`

   D. :math:`\dot v = a`

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The first two equations move the rear axle along the heading (**A**,
   **B**); the fourth changes the speed (**D**). The turn rate grows with
   speed and with steering: :math:`\dot\theta = v\tan\delta / L`. An EKF
   predicts with the gyro's measured turn rate instead; a controller chooses
   :math:`\delta`, so here the turn rate comes from it. See "Write the
   Model: the State, the Inputs and Four Equations" in :doc:`l10_lecture`.


.. admonition:: Question 8
   :class: hint

   The path has a curvature of 0.15 /m (chosen for this question). With the
   lecture's wheelbase, 2.875 m, which steering angle follows it?

   A. 0.150 rad

   B. 0.408 rad

   C. 0.431 rad

   D. 1.164 rad

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   To follow a curvature :math:`\kappa`, steer
   :math:`\delta = \arctan(L\kappa)`:

   1. :math:`L\kappa` = 2.875 × 0.15 = 0.431.
   2. :math:`\delta` = arctan(0.431) = 0.408 rad.

   0.431 (**C**) forgets the arctan; 0.150 (**A**) is the curvature itself;
   1.164 (**D**) is :math:`\arctan(1 / (L\kappa))`, the angle the wrong way
   up. 0.408 rad is under the 0.7 rad limit, so the AV can follow this
   curve. See "Steer for a Curvature: a Fixed Angle Drives a Circle" in
   :doc:`l10_lecture`.


.. admonition:: Question 9
   :class: hint

   Recall last class's candidate A: :math:`s_0` = 60 m, :math:`L` = 40 m,
   :math:`\Delta d` = 3.5 m. At :math:`s` = 90 m (chosen for this
   question), what is :math:`u`, and how far sideways, :math:`d`, has
   candidate A moved?

   A. :math:`u` = 0.75, :math:`d` = 3.15 m

   B. :math:`u` = 0.75, :math:`d` = 2.63 m

   C. :math:`u` = 0.60, :math:`d` = 2.10 m

   D. :math:`u` = 1.00, :math:`d` = 3.50 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   1. :math:`u = (s - s_0)/L = (90 - 60)/40` = 0.75.
   2. :math:`q(0.75)` = 0.90 (the lecture's own value at :math:`u` = 0.75).
   3. :math:`d = \Delta d\, q(u) = 3.5 \times 0.90` = 3.15 m.

   2.63 m (**B**) comes from :math:`d = \Delta d \times u` (skipping
   :math:`q`); 1.00 (**D**) is :math:`u` past the move's end. See "Read u:
   How Far Through the Move a Point s Is" and "Shape the Move with q(u)" in
   :doc:`l10_lecture`.


.. admonition:: Question 10
   :class: hint

   In the lecture's speed test, a P controller alone with
   :math:`K_p` = 0.5 settles at 7.58 m/s for an 8 m/s target. Why does a
   gap stay?

   A. The throttle sits at its 0.75 limit the whole time.

   B. P makes throttle only from an error, and holding the speed against
      drag needs some throttle.

   C. The engine lag of 0.3 s never ends.

   D. The I term winds up.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   1. At 7.58 m/s the drag is :math:`0.15 + 0.012 \times 7.58^2` =
      0.84 m/s², so holding the speed needs throttle 0.84 / 4 = 0.21.
   2. P gives :math:`u = 0.5\,e`, so 0.5 × :math:`e` = 0.21 needs
      :math:`e` = 0.42 m/s.

   With no error, P gives no throttle, and drag slows the AV. A P
   controller alone has no I term to wind up (**D**). See "Try P Alone: the
   AV Settles 0.42 m/s Short" in :doc:`l10_lecture`.


.. admonition:: Question 11
   :class: hint

   With :math:`K_i` = 0.3 and no clamp, the PI run peaks at 12.18 m/s for
   an 8 m/s target. What causes the overshoot?

   A. The D term reacts to the target jump.

   B. The I term keeps adding the large early errors while the throttle sits
      at its limit, and the stored sum then pushes the AV past the target.

   C. :math:`K_p` is too small.

   D. The drag is larger at high speed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   This is integrator windup. The throttle is at its 0.75 limit from the
   start, so a larger command cannot open it further, but the sum keeps
   growing: by the time the AV reaches 8 m/s (3.45 s), the sum is 14.29 m
   and the I term 0.3 × 14.29 = 4.29. The sum shrinks only while the AV is
   too fast. This run has no D term (**A**). See "Explain the Overshoot:
   Windup" in :doc:`l10_lecture`.


.. admonition:: Question 12
   :class: hint

   Last class scored two of the nine kept candidates: A (:math:`d` =
   3.5 m) costs 5.07; B (:math:`d` = 3.0 m) costs 7.71. B saves 0.36 on
   comfort but costs more on the other terms and still loses. Which term
   adds B's largest extra cost over A?

   A. Progress

   B. Lane

   C. Clearance

   D. Comfort

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Clearance: B pays 4 × (1.5 − 0.859) = 2.56 against A's
   4 × (1.5 − 1.359) = 0.56, 2.00 more. Lane costs B 1.00 more
   (3.00 against 2.00) (**B**); Progress costs both 0 (**A**); Comfort is
   where B is cheaper, by 0.36, not more expensive (**D**). See "Apply the
   Costs: A Is the Cheapest" in :doc:`l10_lecture`.


.. admonition:: Question 13
   :class: hint

   Pure Pursuit, :math:`L_d` = 5 m. In the AV's own frame, the goal point
   is 4.0 m forward and 3.0 m to the right (chosen for this question):
   :math:`g_x` = 4.0 m, :math:`g_y` = −3.0 m. What is the curvature of the
   arc through the goal?

   A. −0.12 /m

   B. −0.24 /m

   C. −0.375 /m

   D. −0.6 /m

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   1. :math:`\alpha = \arctan(g_y / g_x) = \arctan(-3.0 / 4.0)` =
      −0.644 rad.
   2. :math:`\sin\alpha` = −0.6.
   3. :math:`\kappa = 2\sin\alpha / L_d` = 2 × (−0.6) / 5 = −0.24 /m.
      Negative: a right turn.

   −0.12 (**A**) forgets the 2; −0.6 (**D**) is :math:`\sin\alpha` alone.
   The steering is then :math:`\arctan(2.875 \times (-0.24))` = −0.604 rad,
   under the 0.7 rad limit. See "Steer for the Arc: Pure Pursuit's Steering
   Law" in :doc:`l10_lecture`.


.. admonition:: Question 14
   :class: hint

   The trajectory planner checks all 324 candidates (18 across the road
   times 18 along it) against the checks and against car B. 54 are too
   hard, 90 hit the parked car, and 135 hit car B (every one that ends in
   the left lane). How many are kept?

   A. 27

   B. 45

   C. 90

   D. 135

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   324 − (54 + 90 + 135) = 324 − 279 = 45. See "Check Each Candidate at Its
   Own Time: 45 of 324 Are Kept" in :doc:`l10_lecture`.


.. admonition:: Question 15
   :class: hint

   The lookahead scales with the speed: :math:`L_d = \max(3\ \mathrm{m},\
   k_v v)` with :math:`k_v` = 0.75 s. What is :math:`L_d` at 6 m/s and at
   2 m/s (speeds chosen for this question)?

   A. 4.5 m and 1.5 m

   B. 4.5 m and 3 m

   C. 6 m and 3 m

   D. 3 m and 3 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   At 6 m/s: 0.75 × 6 = 4.5 m, longer than 3 m. At 2 m/s: 0.75 × 2 = 1.5 m,
   raised to 3 m. On the lecture's turn, this rule gave the smallest corner
   error of the runs tried: 0.07 m. See "A Lookahead for Every Speed: Scale
   It with the Speed" in :doc:`l10_lecture`.


True or False (Questions 16 to 19)
==================================

.. admonition:: Question 16
   :class: hint

   True or false: in the lecture's runs, a 3 m lookahead makes the AV weave
   on the straight approach, and the weave needs both the steering's delay
   and its lag.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   At 3 m, 8 m/s, the AV weaves because the steering is both delayed and
   lags: its swings grow to 3.07 m, out of the 3.5 m lane. See "Choose the
   Lookahead: Too Short Weaves, Too Long Cuts the Corner" in
   :doc:`l10_lecture`.


.. admonition:: Question 17
   :class: hint

   True or false: during the measured 0.2 s steering delay, at the test
   path's 8 m/s starting speed, the AV drives 2.0 m on its old steering
   before the wheel begins to turn.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The AV drives :math:`8 \times 0.2` = 1.6 m on its old steering during
   the 0.2 s delay, not 2.0 m. See "Measure the Chain's Delay: the Wheel
   Turns 0.2 s after the Command" in :doc:`l10_lecture`.


.. admonition:: Question 18
   :class: hint

   True or false: in Stanley's law, :math:`e` is the cross-track error of
   the rear axle, as in Pure Pursuit.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Stanley measures :math:`e` at the **front** axle:
   :math:`\delta = \psi_e - \arctan\big(k e / (v + k_s)\big)`. Pure Pursuit
   works from the rear axle. With the lecture's signs, an AV left of the
   path (:math:`e > 0`) must steer right, so the term is subtracted. See
   "Steer from the Front Axle: Stanley's Heading and Cross-Track Terms" in
   :doc:`l10_lecture`.


.. admonition:: Question 19
   :class: hint

   True or false: at each step, MPC applies the whole sequence of inputs it
   found over the horizon, then plans again at the end of the horizon.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   MPC applies only the first input, then plans again from the newly
   measured state at the next step (every 0.05 s here). The horizon slides
   forward with the AV, so MPC is a feedback controller: each plan starts
   from the measured pose. See "Plan Ahead with MPC: Predict, Score, Apply
   the First Input, Repeat" in :doc:`l10_lecture`.


Short Answer (Questions 20 to 21)
=================================

.. admonition:: Question 20
   :class: hint

   On the lecture's turn, a 10 m lookahead crosses the center by only
   0.07 m after the 1 m start, but a 5 m lookahead is the best of the eight
   tried. Explain the trade-off with the two errors the lecture measures.

.. dropdown:: Answer
   :class-container: sd-border-success

   A long lookahead aims at a point far ahead, so after the 1 m start it
   steers gently and barely crosses the center (0.07 m at 10 m). In the
   corner, the same far point is already around the bend, so the AV turns
   early: 0.98 m inside the center, then 0.95 m outside on the exit. A
   short lookahead tracks the corner more closely, but at 4 m and below the
   AV weaves. 5 m balances the two: it crosses by 0.32 m after the start and
   stays within 0.25 m of the center in the turn. See
   "Choose the Lookahead: Too Short Weaves, Too Long Cuts the Corner" in
   :doc:`l10_lecture`.


.. admonition:: Question 21
   :class: hint

   In the lecture's road tree, tick 1 runs Change lane. At tick 2, 0.1 s
   later, a car is 20 m behind in the left lane, and the tree runs Follow.
   Explain how the tree switches with no arrow from Change lane to Follow,
   and what a flat FSM would need for the same switch.

.. dropdown:: Answer
   :class-container: sd-border-success

   At every tick the root Fallback checks the conditions again from the
   left, and the first branch that does not fail picks the action. At tick
   2, condition 1 (a stop line within 30 m) still fails. Condition 2 (the
   car ahead under 6 m/s for 3 s) still holds, but condition 3 (the left
   lane free) fails, because a car is within 30 m behind, so the second
   Sequence fails. The Fallback moves on to the third branch: condition 4 (a
   car ahead within 40 m) holds at 25 m, so Follow runs. A flat FSM would
   need an explicit arrow from Change lane to Follow, with the left lane's
   state as its condition. See "Switch Behaviors with No Arrow: a Car in
   the Left Lane Stops the Pass" in :doc:`l10_lecture`.
