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
collision checking with circles and its margin, the Frenet frame, sampling
and scoring candidate paths, the behavior layer (the lane change as a game
and the finite state machine), and the garage planners (grid search, hybrid
A*, RRT and RRT*). Every question can be answered from the lecture notes,
:doc:`l9_lecture`. Nothing on this page needs
:doc:`Going Further <l9_appendix>`.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.
   - The lecture's scene is one road of CARLA's Town03 map, with two
     lanes, 3.5 m wide, that run the same way. The AV drives at 10 m/s on
     the right lane's center, at :math:`s` = 60 m. The obstacle, a parked car, is 58 m ahead, at
     :math:`s` = 118 m, 0.3 m right of the lane's center. Both are 4.5 m
     long and 1.9 m wide.
     :math:`s` is the distance along the right lane's center, :math:`d` the
     distance across it, positive to the left. Numbers that are not the
     lecture's are marked "chosen for this question".


----


Multiple Choice (Questions 1 to 15)
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

   The AV heads along the lane, the same way as the obstacle. Its front
   bumper is 3.6 m ahead of its base link; the obstacle is 4.5 m long. The
   two bodies overlap from behind when the base link is less than how far
   behind the obstacle's center?

   A. 3.15 m

   B. 3.6 m

   C. 5.85 m

   D. 9.0 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The obstacle's rear is 4.5 / 2 = 2.25 m behind its center. The AV's front
   reaches it when the base link is less than 2.25 + 3.6 = 5.85 m behind the
   center. 3.15 m (**A**) is the limit ahead of the obstacle, from the AV's
   rear (2.25 + 0.9). 9.0 m (**D**) is the whole length of the region,
   5.85 + 3.15. See "Step 1: Grow the Obstacle, for One AV Heading" in :doc:`l9_lecture`.


.. admonition:: Question 3
   :class: hint

   The region the AV's base link must avoid reaches 5.85 m behind the
   obstacle's center but only 3.15 m ahead of it. Why?

   A. The obstacle faces the other way.

   B. The base link sits near the AV's rear, 0.9 m from the rear bumper and
      3.6 m from the front bumper.

   C. The 0.3 m margin is added only behind the obstacle.

   D. The AV is wider than the obstacle.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Coming from behind, the AV's front leads by 3.6 m, so the base link must
   stay farther back. Coming from ahead, only the 0.9 m behind the base
   link matters. Both cars face the same way (**A** is wrong), the margin
   is not part of this region (**C** is wrong), and both are 1.9 m wide
   (**D** is wrong). See "Step 1: Grow the Obstacle, for One AV Heading" in :doc:`l9_lecture`.


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
   turn the steering allows, about ten times smaller. See "Comfort Limit:
   Wider Turns at Higher Speed" in :doc:`l9_lecture`.


.. admonition:: Question 5
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
   bodies 0.4 m apart. See "The Margin: How Close Counts as a Collision"
   and "Circles Can Report a Collision That Is Not There" in
   :doc:`l9_lecture`.


.. admonition:: Question 6
   :class: hint

   What does the 0.3 m margin of the collision check cover?

   A. Only the error in the AV's own position.

   B. Only the error in where perception places the obstacle.

   C. Only the error in prediction for a moving car.

   D. All three errors together.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   A published requirement allows at most 0.29 m of error in the AV's own
   position on a local street, rounded to 0.3 m. The obstacle's position
   comes from perception, and a moving car's from prediction, with more
   error; a margin for them would add to the 0.3 m. See "The Margin: How
   Close Counts as a Collision" in :doc:`l9_lecture`.


.. admonition:: Question 7
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


.. admonition:: Question 8
   :class: hint

   At 10 m/s, the candidate that moves 3.5 m sideways over 20 m has a peak
   sideways acceleration of 4.91 m/s², and its smallest gap to the obstacle
   is 1.36 m (both measured by the hands-on script). What does the
   planner do with it?

   A. It keeps it and scores it.

   B. It drops it as too sharp.

   C. It drops it as a collision.

   D. It keeps it, with a clearance cost only.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   4.91 m/s² is over the 3 m/s² limit, so the planner drops the path before
   it scores it (**A** and **D** are wrong). A gap of 1.36 m is well over the
   0.3 m margin, so it does not collide (**C**). It is one of the 4 too-sharp
   candidates of "Step 2: Drop Paths That Collide or Turn Too Hard" in
   :doc:`l9_lecture`.


.. admonition:: Question 9
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


.. admonition:: Question 10
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
   C, Stop Behind" in :doc:`l9_lecture`.


.. admonition:: Question 11
   :class: hint

   The behavior layer closes the left lane, so the sampler keeps
   :math:`d_\text{end}` ≤ 0.5 m. Why does the AV then wait behind the
   obstacle?

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
   0.5 m the AV's circles are 0.5 + 0.3 = 0.8 m across from the obstacle's,
   under 2 × 1.21 = 2.42 m, so they overlap; the smaller offsets are closer
   still. With the left lane open, stop behind ranks 8th at 11.54 (**A** is
   wrong). See "One Decision Changes the Cheapest Path" in
   :doc:`l9_lecture`.


.. admonition:: Question 12
   :class: hint

   The lane change as a game. Each cell gives the AV's delay, then the other
   car's, in seconds: AV goes and car keeps, a crash, 100 and 100; AV goes
   and car yields, 0 and 2; AV waits and car keeps, 3 and 0; AV waits and car
   yields, 3 and 2. Why is the cell "AV waits, car yields" not a Nash
   equilibrium?

   A. Both drivers wait for each other, so neither one moves.

   B. Each driver can lower its own delay by switching alone: the AV by
      going, the other car by keeping its speed.

   C. Its total delay, 5 s, is the largest of the four cells.

   D. Only the AV can lower its delay by switching; the other car cannot.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   With the car still yielding, the AV that goes gets 0 s instead of 3 s.
   With the AV still waiting, the car that keeps its speed gets 0 s instead
   of 2 s. One such switch is enough to rule the cell out, and here the car
   can switch too (**D** is wrong). The crash cell has the largest total, 200 s (**C** is wrong).
   The game has two equilibria: AV goes and car yields, and AV waits and car
   keeps. See "Two Equilibria: the AV Goes First Only When It Is Sure" in
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

   The lecture's grid search finds a 27.4 m path through the garage. Why
   can the AV not drive that path as it is?

   A. The path runs through a parked car.

   B. The path has corners of 45°, where the heading would jump, and the AV
      cannot turn on the spot.

   C. The path is longer than hybrid A*'s.

   D. The cells, 0.5 m, are smaller than the AV.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The grid search steps from cell to cell, and a cell has no heading. Its
   path has 9 corners of 45°. At a corner the AV would have to turn on the
   spot, and it cannot: a path it can drive has no corners. Each car and
   wall was grown by 1.05 m before the search, so the path does not enter a
   car (**A** is wrong). It is shorter than hybrid A*'s 30.6 m (**C** is
   wrong). The cell size is not the problem (**D**). See "Grid Search on
   the Whole Garage" and "Drivable Paths: No Corners, No Tight Bends" in
   :doc:`l9_lecture`.


.. admonition:: Question 15
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

   Plain A* visits only the cell centers (**A**). Hybrid A* keeps in each
   cell one exact pose, one the AV reaches by driving from the pose before
   it. It does not keep every pose that reaches the cell (**C**): if the
   cell already holds a pose, the new one is dropped. The path is made of
   these exact poses, so it has no jumps. See "Hybrid A*: an Exact Pose in
   Every Cell" and "Hybrid A*, Steps 4 to 6: Cells, Cost and the Goal" in
   :doc:`l9_lecture`.


----


True or False (Questions 16 to 19)
==================================

.. admonition:: Question 16
   :class: hint

   The three-circle collision check can miss a real collision between the
   AV and the obstacle.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   The circles cover the whole body, so the check never misses a real
   collision. It errs the other way: it can drop a path that was free.
   Bodies 0.4 m apart already count as overlapping. See "Circles Can Report
   a Collision That Is Not There" in :doc:`l9_lecture`.


.. admonition:: Question 17
   :class: hint

   With the right lane's center as the reference, the lane line between the
   two lanes is the line :math:`d` = +1.75 m.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**.

   The lanes are 3.5 m wide, so the lane line is 3.5 / 2 = 1.75 m left of
   the right lane's center. In :math:`(s, d)` every lane edge is a line of
   constant :math:`d`: −1.75, +1.75 and +5.25 m. See "The Big Idea: the Road
   Becomes Straight in (s, d)" in :doc:`l9_lecture`.


.. admonition:: Question 18
   :class: hint

   If a path to the goal exists, hybrid A* always finds it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   Every path hybrid A* returns can be driven, but the search is not
   complete: it can miss a path that exists. See "Hybrid A* in the Garage"
   in :doc:`l9_lecture`.


.. admonition:: Question 19
   :class: hint

   As plain RRT keeps adding nodes, the length of its path tends to the
   length of the shortest path.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**.

   As plain RRT adds nodes, its path's length settles on a value above the
   shortest. RRT keeps the first path it finds. RRT*, which chooses each new
   node's parent and rewires the nodes near it, is the one whose path length
   tends to the shortest as the tree grows. See "RRT*: the Path Keeps
   Getting Shorter" in :doc:`l9_lecture`.


----


Short Answer (Questions 20 to 21)
=================================

.. admonition:: Question 20
   :class: hint

   For the AV heading along the lane, the obstacle becomes a 9.0 m by
   3.8 m box that the base link must avoid. Why do the planners not use
   this box for every pose along a path, and what do they do instead?

.. dropdown:: Answer
   :class-container: sd-border-success

   The box holds only for one heading. Each heading gives its own region,
   so the obstacle region depends on all three numbers
   :math:`(x, y, \theta)`; for a turned AV it is not even a box. So the
   planners do not build it. They place the AV's body at each pose along a
   path, covered by three circles, and check it against the obstacle's
   circles:
   4,332 poses for the 31 candidates, every 0.5 s. See "The Region Changes
   with the Heading" and "How Often the Check Runs: 4,332 Poses Every
   0.5 s" in :doc:`l9_lecture`.


.. admonition:: Question 21
   :class: hint

   Set the progress weight to 0 and keep the other weights. Which candidate
   is the cheapest, and why? Use the cost terms of candidates A and C.

.. dropdown:: Answer
   :class-container: sd-border-success

   Stop behind (C) wins. Without the progress term, its cost is
   0 + 1.62 + 0 = 1.62 (1.61 unrounded): it pays only for clearance. A still
   costs 2.51 + 0.56 + 2.00 = 5.07, because it never lost any progress, and
   every other kept candidate ends one lane over, so its lane term alone is
   at least 2.00. The
   weight of 0.5 per meter is what makes the AV pass: it prices the 19.85 m
   that stopping gives up at 9.93. See "Step 3: Score Candidate C, Stop
   Behind" in :doc:`l9_lecture`.
