====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Seven take-home exercises, then three in-class ones, built on the Lecture 9
notes, :doc:`l9_lecture`, and on the lecture's Town03 road and garage. They use only the lecture,
never :doc:`Going Further <l9_appendix>`. Exercise 1 grows the obstacle
for another AV. Exercise 2 converts points between the map and the Frenet
frame. Exercises 3 and 4 check and score candidate paths, and Exercise 5
checks poses with circles. Exercise 6 runs the valet's state machine, and
Exercise 7 compares the garage planners. Two exercises end with a check in
the lecture's hands-on window. Exercises 8 to 10 are done in class: a
spreadsheet and two games.

.. note::

   Every exercise can be done with a calculator. The hands-on checks need
   ``l9_handson.py`` and ``l9common.py`` from folder ``lecture9`` of the
   course's Python repository, and no CARLA server (see :doc:`l9_code`).

   **The scene:** one road of Town03, with two lanes, 3.5 m wide,
   that run the same way. The
   reference path is the right lane's center; :math:`s` is the distance
   along it and :math:`d` the distance across it, positive to the left. The
   AV drives at 10 m/s on the right lane's center at :math:`s` = 60 m. The
   obstacle, a parked car, is at :math:`s` = 118 m, :math:`d` = −0.3 m. Both
   are 4.5 m long and 1.9 m wide; the AV's base link is 0.9 m in from its
   rear bumper. The
   lecture chose these values. Numbers that are not the lecture's are marked
   "chosen for this exercise".


.. dropdown:: Exercise 1. Grow the Obstacle for Another AV
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Build the region the base link must avoid for a larger AV, place it on
   the road, and work out the AV's two turn limits.

   .. raw:: html

      <hr>

   **Specification**

   The new AV is 5.0 m long and 2.0 m wide, with its base link 1.0 m in from
   its rear bumper (all chosen for this exercise). It heads along the lane,
   the same way as the lecture's obstacle (4.5 m by 1.9 m). Use the three
   overlap conditions of "Step 1: Grow the Obstacle, for One AV Heading"
   in the lecture: from behind, from ahead and across.

   .. raw:: html

      <hr>

   **Part A. The region**

   1. How far ahead of the base link is the new AV's front bumper? How far
      is each side from its center line?
   2. How far behind and how far ahead of the obstacle's center does the
      region reach, and how far to either side? How long and how wide is
      it?

   .. raw:: html

      <hr>

   **Part B. On the road**

   3. Between which values of :math:`s` must the base link stay out? From
      how far right to how far left of the right lane's center?
   4. By how much does the left lane's center clear the region?

   .. raw:: html

      <hr>

   **Part C. Turns**

   5. The new AV's wheelbase is 3.0 m (chosen for this exercise), with GP4's
      steering limit of 0.7 rad (tan 0.7 = 0.842). What is its tightest turn
      radius?
   6. At 8 m/s (chosen for this exercise), with the lecture's comfort limit
      of 3 m/s², what is the smallest comfortable radius? How many times the
      tightest turn is it?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 6, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: 5.0 − 1.0 = 4.0 m ahead; each side 2.0 / 2 = 1.0 m.

      Question 2:

      1. From behind: 4.5 / 2 + 4.0 = 2.25 + 4.0 = 6.25 m behind the center.
      2. From ahead: 2.25 + 1.0 = 3.25 m ahead of the center.
      3. Across: 0.95 + 1.0 = 1.95 m to either side.
      4. The region is 6.25 + 3.25 = 9.5 m long and 1.95 + 1.95 = 3.9 m
         wide, against the lecture's 9.0 m by 3.8 m.

      Question 3: from 118 − 6.25 = 111.75 m to 118 + 3.25 = 121.25 m along
      the stretch; from 0.3 + 1.95 = 2.25 m right to 1.95 − 0.3 = 1.65 m
      left of the right lane's center.

      Question 4: 3.5 − 1.65 = 1.85 m, against the lecture's 1.9 m.

      Question 5: :math:`R` = 3.0 / 0.842 = 3.56 m.

      Question 6: :math:`R` ≥ 8² / 3 = 64 / 3 = 21.3 m, and
      21.3 / 3.56 = 6.0 times the tightest turn. A slower AV can take a
      tighter curve in comfort.


.. dropdown:: Exercise 2. The Frenet Frame by Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Convert a point from the map to :math:`(s, d)` and another one back, with
   the lecture's three steps.

   .. raw:: html

      <hr>

   **Specification**

   Use the lecture's piece of the reference: :math:`A` = (155.225,
   −207.141), :math:`B` = (155.750, −207.134), 0.525 m long, with :math:`A`
   117.539 m along the reference and the left direction :math:`n` =
   (−0.012, 1.000). At :math:`s` = 118 m, the reference point is :math:`r` =
   (155.686, −207.135) and its left direction (−0.0141, 0.9999). All
   coordinates are in meters.

   .. raw:: html

      <hr>

   **Part A. From the map to (s, d)**

   A point :math:`P` = (155.600, −204.000) (chosen for this exercise) has
   its foot point on the piece :math:`A` to :math:`B`.

   1. Find :math:`t`, how far along the piece the foot point is:
      :math:`t = (P - A) \cdot (B - A) / 0.525^2`.
   2. Find the foot point :math:`F` and :math:`s`.
   3. Find :math:`d`. In which lane is :math:`P`?

   .. raw:: html

      <hr>

   **Part B. From (s, d) to the map**

   4. Find the map point of :math:`(s, d)` = (118, 1.75). What is on the
      road there?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 4, with the arithmetic, and the hands-on
   check below.

   **Check in the hands-on.** Run ``python3 l9_handson.py --part scene``,
   set :math:`s` = 118 and :math:`d` = 1.75, and compare the title with your
   answer to question 4.

   .. dropdown:: Guidance
      :color: success

      Question 1:

      1. :math:`P - A` = (0.375, 3.141) and :math:`B - A` = (0.525, 0.007).
      2. The dot product: 0.375 × 0.525 + 3.141 × 0.007 = 0.1969 + 0.0220 =
         0.2189.
      3. :math:`t` = 0.2189 / 0.2756 = 0.794.

      Question 2: :math:`F` = (155.225 + 0.794 × 0.525, −207.141 + 0.794 ×
      0.007) = (155.642, −207.135), and :math:`s` = 117.539 + 0.794 × 0.525
      = 117.539 + 0.417 = 117.96 m.

      Question 3:

      1. :math:`P - F` = (155.600 − 155.642, −204.000 + 207.135) = (−0.042,
         3.135).
      2. :math:`d` = (−0.012)(−0.042) + (1.000)(3.135) = 0.0005 + 3.135 =
         3.14 m.

      The left lane runs from :math:`d` = 1.75 to 5.25 m, so :math:`P` is
      in the left lane, 3.5 − 3.14 = 0.36 m right of its center. The
      hands-on code's ``to_frenet``, with the unrounded points, gives
      :math:`s` = 117.95 m and :math:`d` = 3.14 m.

      Question 4:

      1. :math:`x` = 155.686 + 1.75 × (−0.0141) = 155.686 − 0.025 = 155.661 m.
      2. :math:`y` = −207.135 + 1.75 × 0.9999 = −207.135 + 1.750 = −205.385 m.

      This is the lane line beside the obstacle. The script gives
      (155.661, −205.385); the title rounds it to (155.66, −205.39).


.. dropdown:: Exercise 3. Which Candidates Turn Too Hard
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use the measured peak sideways accelerations to find which candidates
   are too sharp, and see why exactly four are.

   .. raw:: html

      <hr>

   **Specification**

   ``candidates.csv``, the file of the lecture's spreadsheet exercise,
   gives each candidate's peak sideways acceleration and its smallest gap
   to the obstacle, as the hands-on script measured them at 10 m/s. A
   candidate over 3 m/s² is dropped as too sharp; one whose gap falls under
   0.3 m is dropped as a collision. The rows used here:

   .. list-table::
      :widths: 40 30 30
      :header-rows: 1
      :class: compact-table

      * - **Candidate**
        - **Peak sideways acceleration**
        - **Smallest gap**
      * - 4.0 m over 20 m
        - 5.562 m/s²
        - 1.858 m
      * - 4.0 m over 30 m
        - 2.521 m/s²
        - 1.858 m
      * - 4.0 m over 40 m
        - 1.428 m/s²
        - 1.858 m
      * - 3.5 m over 20 m
        - 4.907 m/s²
        - 1.359 m
      * - 3.0 m over 20 m
        - 4.236 m/s²
        - 0.859 m
      * - 2.5 m over 20 m
        - 3.551 m/s²
        - 0.360 m
      * - 2.0 m over 20 m
        - 2.855 m/s²
        - −0.139 m

   .. raw:: html

      <hr>

   **Part A. The 4.0 m candidates**

   1. Which of the three 4.0 m candidates is too sharp?
   2. About how many times smaller is the peak over 40 m than over 20 m?
      What does doubling the maneuver length do to the peak?

   .. raw:: html

      <hr>

   **Part B. Why four**

   3. Over 20 m, which end offsets are too sharp? The lecture's Step 2
      counts 4 too sharp.
   4. 2.0 m over 20 m stays under 3 m/s². Why is it still dropped?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 4, with the arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: only the 20 m one, at 5.56 m/s², over 3. The 30 m and
      40 m ones, at 2.52 and 1.43 m/s², are kept.

      Question 2: 5.562 / 1.428 = 3.9, so about 4 times smaller: twice the
      length gives about a quarter of the peak.

      Question 3: 2.5, 3.0, 3.5 and 4.0 m, at 3.55, 4.24, 4.91 and 5.56
      m/s²: 4 candidates, as Step 2 says. Their gaps, from 0.36 m up, are
      all over 0.3 m, so none of them collides.

      Question 4: its smallest gap is −0.139 m, under 0.3 m (negative: the
      circles overlap). It collides, and the lecture counts it among the 18
      that collide.

.. dropdown:: Exercise 4. Score Two More Candidates, Then Change a Weight
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Score the candidates ranked 2 and 3 in the lecture, and find the
   clearance weight at which the cheapest path changes.

   .. raw:: html

      <hr>

   **Specification**

   The lecture's cost terms and weights: comfort, 2 per m/s² of peak
   sideways acceleration; clearance, 4 per m that the smallest gap falls
   under 1.5 m; lane, 2 per lane away from the route's lane plus 2 per m off
   a lane center; progress, 0.5 per m of the 70 m not covered. The
   hands-on script measured:

   .. list-table::
      :widths: 40 30 30
      :header-rows: 1
      :class: compact-table

      * - **Candidate**
        - **Peak sideways acceleration**
        - **Smallest gap**
      * - A: 3.5 m over 40 m
        - 1.253 m/s²
        - 1.359 m
      * - 4.0 m over 40 m
        - 1.428 m/s²
        - 1.858 m
      * - 3.5 m over 30 m
        - 2.214 m/s²
        - 1.359 m

   All three cover the 70 m.

   .. raw:: html

      <hr>

   **Part A. Score them**

   1. Score 4.0 m over 40 m, term by term.
   2. Score 3.5 m over 30 m, term by term.
   3. Do your totals match the lecture's ranks 2 and 3?

   .. raw:: html

      <hr>

   **Part B. A larger clearance weight**

   4. Raise the clearance weight from 4 to 10. What are the costs of A and
      of 4.0 m over 40 m now? Which one wins?
   5. At about what clearance weight do the two cost the same?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 5, and the hands-on check below.

   **Check in the hands-on.** Run ``python3 l9_handson.py --part sample``,
   set the clearance weight slider to 10 and read the table.

   .. dropdown:: Guidance
      :color: success

      Question 1:

      1. Comfort: 2 × 1.428 = 2.86.
      2. Clearance: the gap, 1.858 m, is over 1.5 m, so 0.
      3. Lane: 4.0 m is one lane from the route's (the left lane's center is
         at 3.5 m) and 0.5 m off that center: 2 × 1 + 2 × 0.5 = 3.00.
      4. Progress: 0.

      Total: 2.86 + 0 + 3.00 + 0 = 5.86.

      Question 2:

      1. Comfort: 2 × 2.214 = 4.43.
      2. Clearance: 4 × (1.5 − 1.359) = 0.56.
      3. Lane: on the left lane's center, 2 × 1 + 2 × 0 = 2.00.
      4. Progress: 0.

      Total: 4.43 + 0.56 + 2.00 + 0 = 6.99.

      Question 3: yes: rank 2 at 5.86 and rank 3 at 6.99.

      Question 4: A's clearance becomes 10 × (1.5 − 1.359) = 1.41, so A
      costs 2.51 + 1.41 + 2.00 = 5.92. 4.0 m over 40 m pays no clearance at
      any weight, so it still costs 5.86, and it wins. The table in the
      hands-on shows the same: 5.86, then 5.92.

      Question 5: A's terms other than clearance add up to 2.51 + 2.00 =
      4.51. It ties with 5.86 when the clearance term is 5.86 − 4.51 = 1.35,
      so at a weight of 1.35 / 0.141 = 9.6. Above about 9.6, the AV moves
      farther from the obstacle and pays for it on the lane.


.. dropdown:: Exercise 5. Circles by Hand
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Place the AV's circles for a turned pose, and use gaps to see which
   candidates beside the obstacle collide.

   .. raw:: html

      <hr>

   **Specification**

   The AV's three circles have radius 1.21 m. For a pose
   :math:`(x, y, \theta)`, circle :math:`k` is centered at
   :math:`(x + o_k \cos\theta,\ y + o_k \sin\theta)`, with :math:`o_k` =
   −0.15, 1.35 and 2.85 m. The obstacle has the same circles around its
   own body. The gap is the distance between two centers minus the two
   radii; a gap under 0.3 m is a collision.

   .. raw:: html

      <hr>

   **Part A. A turned pose**

   1. Find the three circle centers for the pose (10.00 m, 5.00 m, 30°)
      (chosen for this exercise). cos 30° = 0.866 and sin 30° = 0.5.

   .. raw:: html

      <hr>

   **Part B. Beside the obstacle**

   The AV passes the obstacle with its middle circle lined up with the
   obstacle's, as in "Step 2: One Pose, Checked by Hand".

   2. Find the gap between the two middle circles for :math:`d_\text{end}` =
      3.0, 2.5 and 2.0 m.
   3. Which of the three collide? What does the clearance term charge the
      one that is closest but still kept?

   .. raw:: html

      <hr>

   **Part C. Stop behind**

   4. Stop behind leaves 2.0 m between the AV's front bumper and the
      obstacle's rear bumper. The AV's base link stops at :math:`s` =
      110.15 m, at :math:`d` = 0. Where along the road are the AV's front
      circle center and the obstacle's rear circle center? What is their
      gap, taking the
      0.3 m offset across into account?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 4, with the arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1:

      1. :math:`o` = −0.15: (10 − 0.15 × 0.866, 5 − 0.15 × 0.5) = (9.870,
         4.925).
      2. :math:`o` = 1.35: (10 + 1.169, 5 + 0.675) = (11.169, 5.675).
      3. :math:`o` = 2.85: (10 + 2.468, 5 + 1.425) = (12.468, 6.425).

      Question 2: the obstacle's center is 0.3 m right of the reference, so the
      centers are :math:`d_\text{end}` + 0.3 apart across.

      1. 3.0 m: 3.3 − 2.42 = 0.88 m.
      2. 2.5 m: 2.8 − 2.42 = 0.38 m.
      3. 2.0 m: 2.3 − 2.42 = −0.12 m.

      The script's smallest gaps along these paths are 0.86, 0.36 and
      −0.14 m.

      Question 3: 2.0 m collides (its gap is under 0.3 m; it is even under
      0). 2.5 m is kept, just: its gap of 0.36 m is over 0.3 m. Its
      clearance term is 4 × (1.5 − 0.36) = 4.56, which is why it ranks low
      (7th and 9th).

      Question 4:

      1. The AV's front circle center is 2.85 m ahead of the base link:
         110.15 + 2.85 = 113.00 m.
      2. The obstacle's rear circle center is 1.5 m behind its center:
         118 − 1.5 = 116.50 m.
      3. Along: 116.50 − 113.00 = 3.50 m. Across: 0.3 m. The distance is
         :math:`\sqrt{3.50^2 + 0.3^2} = \sqrt{12.25 + 0.09}` = 3.51 m.
      4. Gap: 3.51 − 2.42 = 1.09 m.

      The lecture's script gets 1.10 m. The 2.0 m between the bumpers
      shrinks to about 1.1 m because each circle reaches 0.46 m past its
      bumper.


.. dropdown:: Exercise 6. The Valet's State Machine
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run the valet's FSM on a sequence of width readings, with one threshold
   and then with two, and count how often the local planner gets a new task.

   .. raw:: html

      <hr>

   **Specification**

   The lecture's valet FSM has the states Enter, Search the aisle, Approach
   the spot, Reverse in and Parked, and the six transitions of "Each
   Transition Has One Condition". The spot detector measures the free
   spot's width every 0.1 s. The spot is never taken. The FSM is in Search
   before the first reading. The readings, in meters (chosen for this
   exercise):

   2.7, 2.5, 2.7, 2.5, 2.2, 2.5, 2.7

   .. raw:: html

      <hr>

   **Part A. One threshold**

   1. With one threshold, 2.6 m both ways (Approach at 2.6 m or more,
      Search below it), write the state after each reading. How many times
      does the state change?

   .. raw:: html

      <hr>

   **Part B. Two thresholds**

   2. With the lecture's two thresholds (enter Approach at 2.6 m or more; go
      back to Search only below 2.3 m), write the state after each reading.
      How many times does the state change?
   3. Which reading still sends the AV back to Search, and why should it?

   .. raw:: html

      <hr>

   **Part C. Other transitions**

   4. The FSM is in Search, and the AV reaches the end of the aisle with no
      free spot. Which transition fires, and where does it lead?
   5. The FSM is in Reverse in. The base link is 0.15 m and 5° from the goal
      pose. Does transition 5 fire?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 5.

   .. dropdown:: Guidance
      :color: success

      Question 1: Approach, Search, Approach, Search, Search, Search,
      Approach. The state changes 5 times in 7 readings, so the local planner
      gets 5 new tasks in 0.7 s.

      Question 2: Approach, Approach, Approach, Approach, Search, Search,
      Approach. The state changes 3 times. The readings of 2.5 m no longer
      send the AV back, and after the 2.2 m reading a 2.5 m reading does not
      bring it to Approach either: that needs 2.6 m or more.

      Question 3: the 2.2 m reading, the only one under 2.3 m. Transition 3
      exists for this case: a spot that reads under 2.3 m wide no longer
      counts as free (2.3 m was chosen for the lecture), so the AV goes back
      to searching the aisle.

      Question 4: transition 6, from Search back to Search: take the next
      aisle.

      Question 5: no. The base link must be within 0.2 m **and** 3° of the
      goal pose. 0.15 m passes, but 5° does not.


.. dropdown:: Exercise 7. Comparing the Garage Planners
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Read the lecture's garage results as numbers: how much of hybrid A*'s
   path is in reverse, the work each planner did, and why one path can be
   driven and the other cannot.

   .. raw:: html

      <hr>

   **Specification**

   From the lecture:

   - Hybrid A*: 8,478 poses expanded; 24.0 m forward, one switch to
     reverse, 6.6 m in reverse, 30.6 m in all. From each expanded pose, the
     AV drives a short arc at one of 5 steering angles, forward or in
     reverse: 10 arcs.
   - RRT (seed 4): the tree reaches the goal after 34 tries and has 23
     nodes; the path is 16 straight steps, and the heading jumps by up to
     78° where two steps meet.

   .. raw:: html

      <hr>

   **Part A. The two paths**

   1. What share of hybrid A*'s path does the AV drive in reverse?
   2. Why can the AV drive hybrid A*'s path but not RRT's, as it is?

   .. raw:: html

      <hr>

   **Part B. The work done**

   3. How many new poses does hybrid A* check with the circles, if every
      expanded pose drives its 10 arcs?
   4. The RRT tree starts with one node, the AV. How many of its 34 tries
      hit something?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 4, with the arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: 6.6 / 30.6 = 0.22: about 22 % of the path is in reverse.

      Question 2: every pose of hybrid A*'s path is one the AV reaches by
      driving an arc from the pose before it, so the heading never jumps.
      RRT's path is straight steps that meet at angles of up to 78°: the AV
      would have to turn on the spot, which it cannot do.

      Question 3: 8,478 × 10 = 84,780 new poses, each checked with the
      three circles.

      Question 4: 23 nodes means 23 − 1 = 22 steps were added. The other
      34 − 22 = 12 tries hit something, as the lecture says.


In-Class Exercises
==================

The three exercises below are done in class, at the slides that name them.
Their answers are here for after class.

.. dropdown:: Exercise 8. In Class: Score Every Candidate in a Spreadsheet
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compute the cost of each candidate yourself, then see how the weights
   decide which path the AV drives. Work in pairs.

   .. raw:: html

      <hr>

   **Specification**

   Open ``candidates.csv`` (folder ``lecture9`` of the course's Python
   repository, see :doc:`l9_code`) in Excel, Google Sheets or LibreOffice
   Calc. It has 31 rows, one per candidate from the AV at :math:`s` = 60 m,
   with the numbers the cost needs and no costs. Candidate A is the row named
   ``d_end 3.5 m, 40 m``. Know each column before you score with it:

   .. list-table::
      :widths: 26 44 14 16
      :header-rows: 1
      :class: compact-table

      * - **Column**
        - **What it holds**
        - **Cost term**
        - **Row of A**
      * - ``name``
        - the end offset and length, or ``stop behind``
        -
        - ``d_end 3.5 m, 40 m``
      * - ``d_end_m``
        - where the path ends across the road (m)
        -
        - 3.5
      * - ``maneuver_m``
        - the maneuver length (m); empty for stop behind
        -
        - 40.0
      * - ``peak_lat_accel_mps2``
        - the largest sideways acceleration (m/s²)
        - comfort
        - 1.253
      * - ``smallest_gap_m``
        - the smallest circle-to-circle gap (m); under 0: overlap
        - clearance
        - 1.359
      * - ``lanes_away``
        - 0 if the path ends in the route's lane, 1 if one lane over
        - lane
        - 1
      * - ``off_center_m``
        - meters from the nearest lane center, at the end
        - lane
        - 0.0
      * - ``not_covered_m``
        - meters of the 70 m ahead not covered
        - progress
        - 0.0
      * - ``dropped``
        - ``collision``, ``too sharp``, or empty (kept)
        -
        - empty

   .. raw:: html

      <hr>

   **Part 1. Score every candidate**

   1. Delete the 22 rows whose ``dropped`` column is not empty
      (``collision`` or ``too sharp``): the planner never scores them. 9 rows
      remain.
   2. Type the five weights in cells of their own, outside the 9 rows:
      comfort 2, clearance 4, lane 2, center 2, progress 0.5. In formulas,
      refer to them with ``$`` (``$L$2``, not ``L2``), so sorting the rows
      does not break the totals.
   3. Add five columns; each formula uses the weight cells and the row's
      columns:

   .. list-table::
      :widths: 20 80
      :header-rows: 1
      :class: compact-table

      * - **Column**
        - **Formula**
      * - comfort
        - comfort weight × ``peak_lat_accel_mps2``
      * - clearance
        - clearance weight × the larger of 0 and (1.5 − ``smallest_gap_m``)
      * - lane
        - lane weight × ``lanes_away`` + center weight × ``off_center_m``
      * - progress
        - progress weight × ``not_covered_m``
      * - total
        - comfort + clearance + lane + progress

   .. raw:: html

      <hr>

   **Part 2. Change the weights, see who wins**

   4. Sort the rows by total, smallest first (LibreOffice Calc: click a cell
      of the total column, then Data, Sort Ascending). Is the row
      ``d_end 3.5 m, 40 m`` (candidate A) first, at 5.07?
   5. Change the clearance weight from 4 to 10 and sort again. Which row is
      first now? At what :math:`d_\text{end}` does that path end, and why
      does a larger clearance weight favor it?
   6. Put the clearance weight back to 4. Change the progress weight from
      0.5 to 0 and sort again. Which row is first now? What would the AV do,
      and why?

   .. dropdown:: Answer
      :color: success

      Question 4: yes. A costs 2 × 1.253 + 4 × (1.5 − 1.359) + 2 × 1 +
      2 × 0 + 0.5 × 0 = 2.51 + 0.56 + 2.00 + 0 = 5.07. The sorted totals are
      the lecture's ranking: 5.07, 5.86, 6.99, 7.72, 8.04, 9.37, 10.40,
      11.54 (stop behind) and 11.74.

      Question 5: the row ``d_end 4.0 m, 40 m`` is first, at 5.86; A is
      second, at 5.92. That path ends at :math:`d_\text{end}` = 4.0 m, 0.5 m
      left of the left lane's center.

      1. Its smallest gap is 1.858 m, over 1.5 m, so it pays no clearance at
         any weight: 2 × 1.428 + 0 + (2 × 1 + 2 × 0.5) = 2.86 + 3.00 = 5.86.
      2. A's smallest gap, 1.359 m, is 0.141 m short of 1.5 m, so its
         clearance term grows with the weight: 10 × 0.141 = 1.41, and A costs
         2.51 + 1.41 + 2.00 = 5.92.

      A larger clearance weight makes a small gap more expensive, so it
      favors the path that passes farther from the obstacle, even though that
      path ends 0.5 m off a lane center and bends a little harder.

      Question 6: ``stop behind`` is first, at 1.62. With a progress weight of
      0, its 19.85 m of lost progress costs nothing, and its only term is
      clearance: 4 × (1.5 − 1.096) = 1.62. Every other kept row ends one lane
      over, so its lane term alone is 2 × 1 = 2.00. The AV would stop behind
      the obstacle and wait. The progress weight is what makes it pass: at
      0.5 per meter, stopping costs 0.5 × 19.85 = 9.93.

      All the numbers above come from ``candidates.csv``, scored with the
      formulas of Part 1.


.. dropdown:: Exercise 9. In Class: Find the Nash Equilibria of the Lane Change
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Find the Nash equilibria of the lane change between the AV and another
   car, and say what they mean for the AV.

   .. raw:: html

      <hr>

   **Specification**

   The AV chooses to **go** (move into the left lane now) or **wait** (stop
   behind the obstacle). The other car, coming up in the left lane, chooses
   to **keep** its speed or **yield** (slow down and let the AV in). Each
   cell gives the AV's delay, then the other car's, in seconds; a crash
   costs 100. All numbers are chosen for the lecture.

   .. list-table::
      :widths: 30 35 35
      :header-rows: 1
      :class: compact-table

      * -
        - **The other car keeps**
        - **The other car yields**
      * - **The AV goes**
        - crash: 100, 100
        - 0, 2
      * - **The AV waits**
        - 3, 0
        - 3, 2

   A **Nash equilibrium** is "a strategy pair in which no player can
   achieve a better outcome by changing their strategy while the other
   player keeps theirs unchanged". Here a strategy is a choice, and the
   outcome is the delay: lower is better.

   .. raw:: html

      <hr>

   **Instructions**

   For each cell:

   1. Keep the other car's choice as it is. If the AV made its other choice
      (wait instead of go, or go instead of wait), would its delay be lower?
   2. Keep the AV's choice as it is. If the other car made its other choice
      (yield instead of keep, or keep instead of yield), would its delay be
      lower?

   A cell where both answers are no is a Nash equilibrium. How many does
   this game have?

   .. dropdown:: Answer
      :color: success

      Two: **AV goes, car yields** and **AV waits, car keeps**.

      - AV goes, car keeps (a crash): the AV gets 3 instead of 100 by
        waiting, and the car 2 instead of 100 by yielding. Not an
        equilibrium.
      - **AV goes, car yields:** if the AV waits instead, its delay goes from
        0 to 3 s; if the car keeps its speed instead, they crash. Both
        answers are no: an equilibrium.
      - **AV waits, car keeps:** if the AV goes instead, they crash; if the
        car yields instead, its delay goes from 0 to 2 s. Both answers are
        no: an equilibrium.
      - AV waits, car yields: the AV gets 0 instead of 3 by going, and the
        car 0 instead of 2 by keeping its speed. Not an equilibrium.

      Going first is a bet: 0 s if the car yields, but a crash if it keeps
      its speed. So the AV goes first only when prediction says the car will
      yield; otherwise it waits, 3 s.


.. dropdown:: Exercise 10. In Class: The Prisoner's Dilemma
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Find the Nash equilibrium of the Prisoner's Dilemma, and compare it with
   the best outcome for the two players together. The same check as in
   Exercise 9 works on any game of two players.

   .. raw:: html

      <hr>

   **Specification**

   Two suspects, A and B, are questioned in separate rooms. Each one either
   stays **silent** or **confesses**. Each cell gives their sentences: A's
   years, then B's (fewer is better).

   .. list-table::
      :widths: 30 35 35
      :header-rows: 1
      :class: compact-table

      * -
        - **B stays silent**
        - **B confesses**
      * - **A stays silent**
        - A 1, B 1
        - A 10, B 0
      * - **A confesses**
        - A 0, B 10
        - A 5, B 5

   .. raw:: html

      <hr>

   **Instructions**

   With your neighbor:

   1. For each cell: keep B's choice as it is; would A get fewer years with
      its other choice? Then keep A's choice as it is; would B? A cell where
      both answers are no is a Nash equilibrium.
   2. Which cell is the equilibrium? Is it the best cell for the two of them
      together?

   .. dropdown:: Answer
      :color: success

      Both confess, A 5 and B 5: the only Nash equilibrium.

      - Both silent: not an equilibrium. Each suspect gets 0 years instead
        of 1 by confessing.
      - A silent, B confesses: A gets 5 years instead of 10 by confessing.
        Not an equilibrium.
      - A confesses, B silent: B gets 5 years instead of 10 by confessing.
        Not an equilibrium.
      - **Both confess:** if A stays silent instead, A gets 10, not 5; if B
        does, B gets 10, not 5. Neither gains: an equilibrium.

      It is not the best cell for the two together. Both would get 1 year if
      both stayed silent, but neither gets there alone: the one who switches
      to silent alone gets 10.
