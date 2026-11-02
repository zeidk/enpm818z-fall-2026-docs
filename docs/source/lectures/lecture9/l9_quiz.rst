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

This quiz covers Lecture 9: route, path and trajectory, configuration space
and the region an obstacle becomes, the tightest and the comfortable turn,
the Frenet frame and where it fails, sampling and scoring candidate paths,
collision checking with circles and its margin, the behavior layer and its
finite state machine, and the garage planners (grid search, hybrid A* and
RRT). Every question can be answered from the lecture notes,
:doc:`l9_lecture`. Nothing on this page needs
:doc:`Going Further <l9_appendix>`.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.
   - The lecture's scene is one road of CARLA's Town03 map, two lanes each
     way, 3.5 m wide. The AV drives at 10 m/s on the right lane's center,
     at :math:`s` = 60 m. A car is parked 58 m ahead, at :math:`s` = 118 m,
     0.3 m right of the lane's center. Both are 4.5 m long and 1.9 m wide.
     :math:`s` is the distance along the right lane's center, :math:`d` the
     distance across it, positive to the left. Numbers that are not the
     lecture's are marked "chosen for this question".


----


Multiple Choice (Questions 1 to 14)
===================================

.. admonition:: Question 1
   :class: hint

   Which one holds the positions and headings the AV follows over the next
   few seconds, with no times?

   A. The route

   B. The path

   C. The trajectory

   D. The lane graph

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   A route is the lanes to drive, from start to goal (**A** is wrong). A
   trajectory is a path with a speed and a time at each point (**C** is
   wrong). The lane graph is what the route planner searches (**D** is
   wrong). The local planner makes the path, and plans it again every
   0.5 s. See "Route, Path and Trajectory" in :doc:`l9_lecture`.


.. admonition:: Question 2
   :class: hint

   The AV heads along the lane, the same way as the parked car. Its front
   bumper is 3.6 m ahead of its base link; the parked car is 4.5 m long. The
   two bodies overlap from behind when the base link is less than how far
   behind the parked car's center?

   A. 3.15 m

   B. 3.6 m

   C. 5.85 m

   D. 9.0 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The car's rear is 4.5 / 2 = 2.25 m behind its center. The AV's front
   reaches it when the base link is less than 2.25 + 3.6 = 5.85 m behind the
   center. 3.15 m (**A**) is the limit ahead of the car, from the AV's rear
   (2.25 + 0.9). 9.0 m (**D**) is the whole length of the region,
   5.85 + 3.15. See "Step 1: Grow the Parked Car" in :doc:`l9_lecture`.


.. admonition:: Question 3
   :class: hint

   The region the AV's base link must avoid reaches 5.85 m behind the
   parked car's center but only 3.15 m ahead of it. Why?

   A. The parked car faces the other way.

   B. The base link sits near the AV's rear, 0.9 m from the rear bumper and
      3.6 m from the front bumper.

   C. The 0.3 m margin is added only behind the car.

   D. The AV is wider than the parked car.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Coming from behind, the AV's front leads by 3.6 m, so the base link must
   stay farther back. Coming from ahead, only the 0.9 m behind the base
   link matters. Both cars face the same way (**A** is wrong), the margin
   is not part of this region (**C** is wrong), and both are 1.9 m wide
   (**D** is wrong). See "Step 1: Grow the Parked Car" in :doc:`l9_lecture`.


.. admonition:: Question 4
   :class: hint

   At 10 m/s, with a limit of 3 m/s² on the sideways acceleration, what is
   the smallest radius of a comfortable turn?

   A. 3.41 m

   B. 10 m

   C. 33.3 m

   D. 300 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The sideways acceleration on a curve of radius :math:`R` is
   :math:`v^2 / R`. It must stay at or under 3 m/s², so
   :math:`R` ≥ 10² / 3 = 100 / 3 = 33.3 m. 3.41 m (**A**) is the tightest
   turn the steering allows, about ten times smaller. See "The AV Cannot
   Move Sideways" in :doc:`l9_lecture`.


.. admonition:: Question 5
   :class: hint

   With the right lane's center as the reference, where is the point
   :math:`(s, d)` = (140, 3.0)?

   A. In the right lane, 3.0 m right of its center.

   B. In the left lane, 0.5 m right of the left lane's center.

   C. On the left lane's left edge.

   D. On the lane line between the two lanes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`d` is positive to the left, so the point is 3.0 m left of the
   right lane's center (**A** is wrong). The lane line is at
   :math:`d` = 1.75 m (**D**) and the left lane's left edge at 5.25 m
   (**C**), so the point is in the left lane. That lane's center is at
   3.5 m, so the point is 3.5 − 3.0 = 0.5 m right of it. This is the point
   P of "Two Coordinates That Follow the Road" in :doc:`l9_lecture`.


.. admonition:: Question 6
   :class: hint

   A path runs at :math:`d` = 4.0 m beside a left curve of radius 20 m
   (chosen for this question). What is the factor :math:`1 - \kappa d`, and
   does the Frenet frame hold there?

   A. 0.2; it fails.

   B. 0.8; it holds.

   C. 0.935; it holds.

   D. 1.2; it holds.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`\kappa = 1 / R` = 1 / 20, so :math:`1 - \kappa d` = 1 − 4.0 / 20 =
   0.8. It is above 0, so the frame holds. It would fail at :math:`d` =
   20 m, the curve's center. 0.935 (**C**) is the lecture's value on its
   tightest curve, :math:`R` = 61.9 m. See "Where the Frenet Frame Fails" in
   :doc:`l9_lecture`.


.. admonition:: Question 7
   :class: hint

   At 10 m/s, a candidate moves 3.5 m sideways over a maneuver length of
   25 m (chosen for this question). Using the lecture's estimate of the
   peak sideways acceleration, is it kept?

   A. 1.62 m/s²; kept.

   B. 2.24 m/s²; kept.

   C. 3.23 m/s²; dropped as too sharp.

   D. 5.05 m/s²; dropped as too sharp.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`a \approx v^2 \times 5.77 \times \Delta d / L^2` =
   100 × 5.77 × 3.5 / 625 = 3.23 m/s², over the 3 m/s² limit. 2.24 (**B**)
   is the 30 m candidate and 5.05 (**D**) the 20 m one. The estimate leaves
   out the path's slope; the hands-on script's exact value for this path is
   3.17 m/s², still over 3. See "How Hard a Candidate Turns, by Hand" in
   :doc:`l9_lecture`.


.. admonition:: Question 8
   :class: hint

   With the lecture's weights (comfort 2 per m/s², progress 0.5 per m),
   how much lost progress costs as much as 1 m/s² more of peak sideways
   acceleration?

   A. 0.5 m

   B. 2 m

   C. 4 m

   D. 8 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1 m/s² costs 2 × 1 = 2. Lost progress costs 0.5 per meter, so 2 / 0.5 =
   4 m costs the same 2. See "Step 3: the Four Cost Terms" in
   :doc:`l9_lecture`.


.. admonition:: Question 9
   :class: hint

   Candidate C keeps the lane and stops; its path covers 50.15 m of the
   70 m ahead. What is its progress term?

   A. 0

   B. 9.93

   C. 19.85

   D. 25.08

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   It leaves 70 − 50.15 = 19.85 m uncovered, and progress costs 0.5 per
   meter: 0.5 × 19.85 = 9.93. 19.85 (**C**) forgets the weight; 25.08
   (**D**) is 0.5 × 50.15, the meters covered. See "Step 3: Score Candidate
   C" in :doc:`l9_lecture`.


.. admonition:: Question 10
   :class: hint

   Two cars stand side by side, their centers 2.6 m apart across (chosen
   for this question). Each is covered by the lecture's circles of radius
   1.21 m. What does the check report, with the 0.3 m margin?

   A. Gap 0.18 m: under 0.3 m, a collision.

   B. Gap 0.18 m: over 0, so the pose is free.

   C. Gap 0.70 m: free.

   D. Gap −0.12 m: a collision.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   The gap is the distance between the centers minus the two radii:
   2.6 − 2 × 1.21 = 2.6 − 2.42 = 0.18 m. The check calls a pose a collision
   when the gap is under 0.3 m, not only under 0 (**B** is wrong). 0.70 m
   (**C**) is the gap between the bodies, 2.6 − 1.9; the circles reach
   0.26 m past each side. −0.12 m (**D**) is the lecture's case with the
   bodies 0.4 m apart. See "The Margin" and "Circles Can Report a Collision
   That Is Not There" in :doc:`l9_lecture`.


.. admonition:: Question 11
   :class: hint

   What does the 0.3 m margin of the collision check cover?

   A. Only the error in the AV's own position.

   B. Only the error in where perception places the parked car.

   C. Only the error in prediction for a moving car.

   D. All three errors together.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   A published requirement allows at most 0.29 m of error in the AV's own
   position on a local street, rounded to 0.3 m. The parked car's position
   comes from perception, and a moving car's from prediction, with more
   error; a margin for them would add to the 0.3 m. See "The Margin: How
   Close Counts as a Collision" in :doc:`l9_lecture`.


.. admonition:: Question 12
   :class: hint

   The behavior layer closes the left lane, so the sampler keeps
   :math:`d_\text{end}` ≤ 0.5 m. Why does the AV then wait behind the
   parked car?

   A. Stop behind is always the cheapest candidate.

   B. The 9 candidates other than stop behind all collide:
      at :math:`d_\text{end}` = 0.5 m the centers are only 0.8 m apart
      across, under 2.42 m. Stop behind is the only one left.

   C. The candidates in the right lane are all too sharp.

   D. The behavior layer sets the speed to 0.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   3 end offsets × 3 lengths + 1 = 10 candidates. At :math:`d_\text{end}` =
   0.5 m the AV's circles are 0.5 + 0.3 = 0.8 m across from the car's,
   under 2 × 1.21 = 2.42 m, so they overlap; the smaller offsets are closer
   still. With the left lane open, stop behind ranks 8th at 11.54 (**A** is
   wrong). See "One Decision Changes the Cheapest Path" in
   :doc:`l9_lecture`.


.. admonition:: Question 13
   :class: hint

   The valet FSM is in Approach. The spot is still free, and its width
   now reads 2.5 m. With the lecture's two thresholds (enter Approach at
   2.6 m or more, go back to Search below 2.3 m), what happens?

   A. The FSM goes back to Search.

   B. The FSM stays in Approach.

   C. The FSM goes to Reverse in.

   D. The FSM goes to Parked.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   2.5 m is not under 2.3 m, and the spot is not taken, so transition 3
   does not fire. With one threshold of 2.6 m both ways, the same reading
   would send the AV back to Search (**A**). Reverse in needs the AV
   stopped where the reverse maneuver starts (**C** is wrong). See "Two
   Thresholds Keep a State from Flickering" in :doc:`l9_lecture`.


.. admonition:: Question 14
   :class: hint

   What does hybrid A* keep in each :math:`(x, y, \theta)` cell?

   A. The cell's center, as plain A* does.

   B. An exact pose, one the AV reaches by driving an arc from the pose
      before it.

   C. Every pose that has reached the cell.

   D. Only the heading.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   If the cell already holds an expanded pose, the new one is dropped
   (**C** is wrong); if not, the exact pose is stored. The path is made of
   these exact poses, so it has no jumps, unlike a path through cell
   centers (**A**). See "Hybrid A*, Steps 4 to 6" in :doc:`l9_lecture`.


----


True or False (Questions 15 to 18)
==================================

.. admonition:: Question 15
   :class: hint

   The three-circle collision check can miss a real collision between the
   AV and the parked car.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The circles cover the whole body, so the check never misses a real
   collision. It errs the other way: it can drop a path that was free.
   Bodies 0.4 m apart already count as overlapping. See "Circles Can Report
   a Collision That Is Not There" in :doc:`l9_lecture`.


.. admonition:: Question 16
   :class: hint

   If a path to the goal exists, hybrid A* always finds it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   Every path hybrid A* returns can be driven, but the search is not
   complete: it can miss a path that exists. See "Hybrid A* in the Garage"
   in :doc:`l9_lecture`.


.. admonition:: Question 17
   :class: hint

   GP4 asks you to write a local planner that samples candidate paths in
   :math:`(s, d)`.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   GP4 asks for A* on a lane graph with a node every 2 m, which plans again
   when one of two triggers fires. It does not ask for a local planner; one
   would sit between your A* and your controller. See "What a Local Planner
   Adds to GP4's Planner" in :doc:`l9_lecture`.


.. admonition:: Question 18
   :class: hint

   With the right lane's center as the reference, the lane line between the
   two lanes is the line :math:`d` = +1.75 m.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**.

   The lanes are 3.5 m wide, so the lane line is 3.5 / 2 = 1.75 m left of
   the right lane's center. In :math:`(s, d)` every lane edge is a line of
   constant :math:`d`: −1.75, +1.75 and +5.25 m. See "The Road Becomes
   Straight in (s, d)" in :doc:`l9_lecture`.


----


Short Answer (Questions 19 to 20)
=================================

.. admonition:: Question 19
   :class: hint

   For the AV heading along the lane, the parked car becomes a 9.0 m by
   3.8 m box that the base link must avoid. Why do the planners not use
   this box for every pose along a path, and what do they do instead?

.. dropdown:: Answer
   :class-container: sd-border-success

   The box holds only for one heading. Each heading gives its own region,
   so the obstacle region depends on all three numbers
   :math:`(x, y, \theta)`; for a turned AV it is not even a box. So the
   planners do not build it. They place the AV's body at each pose along a
   path, covered by three circles, and check it against the car's circles:
   4,332 poses for the 31 candidates. See "The Region Changes with the
   Heading" and the Collision Checking section in :doc:`l9_lecture`.


.. admonition:: Question 20
   :class: hint

   Set the progress weight to 0 and keep the other weights. Which candidate
   is the cheapest, and why? Use the cost terms of candidates A and C.

.. dropdown:: Answer
   :class-container: sd-border-success

   Stop behind (C) wins. Without the progress term, its cost is
   0 + 1.62 + 0 = 1.62 (1.61 unrounded): it pays only for clearance. A still
   costs 2.51 + 0.56 + 2.00 = 5.07, because it never lost any progress. The
   weight of 0.5 per meter is what makes the AV pass: it prices the 19.85 m
   that stopping gives up at 9.93. See "Step 3: Score Candidate C" in
   :doc:`l9_lecture`.
