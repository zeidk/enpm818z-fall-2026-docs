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

This quiz covers Lecture 7: the terms of route planning (road, carriageway,
lane, route, path, trajectory), the trip in Town01, HD maps and their layers,
reading the map file ``Town01.xodr``, segments and the waypoint graph,
junctions and the traffic rules they put in the graph, the intersection
graph, lane changes in Town03, edge costs and the top speed in a turn, routes
under three costs, GP4's re-planning triggers and hysteresis, and turning the
route into maneuvers. Every question can be answered from the lecture notes,
:doc:`l7_lecture`. Nothing on this page needs
:doc:`Going Further <l7_appendix>`.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.
   - The trip in CARLA's Town01 is the lecture's running example. The start,
     S, is 41 m east of the center of intersection 1, with the AV driving
     west. The goal, G, is 40 m east of the center of intersection 6, on the
     top street, driving east. The start and the goal were chosen for the
     lecture. The shortest route is 9 lanes and 260.6 m long, and it turns
     at intersections 1, 3, 5 and 6 (CARLA's junctions 306, 171, 332 and
     54). The map frame has :math:`x` east and :math:`y` north, in meters.


----


Multiple Choice (Questions 1 to 14)
===================================

.. admonition:: Question 1
   :class: hint

   The lecture uses three words for how the AV gets to its goal: route,
   path and trajectory. Which statement matches the lecture?

   A. A route is a chain of configurations :math:`(x, y, \theta)`, and a
      path is a route with times added.

   B. A route says which lanes to take, in order. A path is a chain of
      configurations :math:`(x, y, \theta)` with no times. A trajectory is
      the path, plus when the AV is at each point.

   C. A route and a trajectory are the same thing, seen at two scales.

   D. A path says which lanes to take, and a route says how fast to drive
      on them.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   A configuration is a position :math:`x`, :math:`y` in meters and a
   heading :math:`\theta`, counterclockwise from east. Route planning, this
   lecture, finds the route. L9 plans the path, and L10 follows the
   trajectory. In the lecture's trajectory, every point of the path gets a
   speed: the speed limit, 11.18 m/s, but slower in a turn. All of those
   settings were chosen for that example. See the Introduction in
   :doc:`l7_lecture`.


.. admonition:: Question 2
   :class: hint

   On road 25, ``Town01.xodr`` gives two sidewalks, 4.0 m wide each, two
   shoulders, 0.3 m wide each, and two driving strips, 4.0 m wide each, one
   going south and one going north. How wide is the carriageway?

   A. 4.0 m

   B. 8.0 m

   C. 8.6 m

   D. 16.6 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The carriageway is the "part of the road intended mainly for the
   movement of road vehicles". Shoulders and parking are not part of it, and
   the sidewalks are part of the road but not of the carriageway. Only the
   two driving strips count: 4.0 + 4.0 = 8.0 m. **C** adds the two
   shoulders (8.0 + 0.3 + 0.3 = 8.6 m). **D** is the whole road:
   4.0 + 0.3 + 4.0 + 4.0 + 0.3 + 4.0 = 16.6 m. **A** is one lane. See the
   Introduction in :doc:`l7_lecture`.


.. admonition:: Question 3
   :class: hint

   GP4's planner node has three inputs, a goal and one output. Which input
   does not reach the node on a ROS topic?

   A. The AV's pose.

   B. The objects on the road.

   C. The map.

   D. None: all three inputs come on topics.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The planner reads the map from the CARLA world through the Python API,
   and CARLA built it from the OpenDRIVE file. The pose comes on
   ``/localization/pose`` from your GP3 localization node (L6), and the
   objects come on ``/perception/fused_objects`` from your GP3 fusion node
   (L5). The goal is two parameters, ``goal_x`` and ``goal_y``: a point with
   no heading. The output is the route as waypoints on ``/planning/path``,
   for GP4 Task 2's controller. See the Introduction in :doc:`l7_lecture`.


.. admonition:: Question 4
   :class: hint

   The lecture compares ``Town01.xodr`` with the six HD map layers of
   Elghazaly et al.: base map, geometric, semantic, road connectivity,
   priors and real-time. Which layers does the file hold?

   A. All six.

   B. The base map and the geometric layer only.

   C. The geometric layer, the road connectivity layer, and part of the
      semantic layer.

   D. Only the road connectivity layer.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The geometric layer is there: the line each road is drawn along, and the
   lane widths. So is road connectivity: the junctions list which lane leads
   to which. The semantic layer is there only in part: 36 traffic lights and
   22 speed signs, but no stop lines and no crossings. The base map is not
   in the file: CARLA ships it as a separate 190 MB point cloud. There are
   no priors, and no real-time layer: "To change the map, the world has to
   change too". So the file is the lane-level part of an HD map. See Map to
   Graph in :doc:`l7_lecture`.


.. admonition:: Question 5
   :class: hint

   Road 25's ``<geometry>`` element has ``hdg="-1.572"``. The heading
   ``hdg`` is in radians, measured counterclockwise from east. Which way
   does road 25's reference line point?

   A. North.

   B. East.

   C. South.

   D. West.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1. In degrees: −1.572 × 180 / π = −90.07°.
   2. A negative angle turns clockwise from east, and a quarter turn
      clockwise from east points south.

   The geometry starts at (156.07, −11.02) and runs 35.18 m, so it ends at
   :math:`y = -11.02 + 35.18 \sin(-90.07^\circ) = -46.20` m, at junction
   332. Lanes are numbered from the reference line: lane 1 on its left
   drives north, and lane −1 on its right drives south. See Map to Graph in
   :doc:`l7_lecture`.


.. admonition:: Question 6
   :class: hint

   Town01's waypoint graph, with a waypoint every 2 m, has 3107 nodes and
   3143 edges. Where does the difference of 36 come from?

   A. The graph has 36 lane change edges.

   B. The map has 36 traffic lights, and each one adds an edge.

   C. Each node has one edge out, and each of the 36 splits has two:
      3107 + 36 = 3143.

   D. The graph has 36 U-turn edges.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A split is a node where a lane meets an intersection and the AV can go
   two ways, so two edges leave it. Town01 has 36 splits: 12 intersections
   with 3 roads into each. Every other node has one edge out. **A** is
   wrong: no waypoint in Town01 allows a lane change. **D** is wrong:
   ``Town01.xodr`` has 0 U-turn connections. The 36 traffic lights are
   real, but they are in the semantic layer and add no edges. See Map to
   Graph in :doc:`l7_lecture`.


.. admonition:: Question 7
   :class: hint

   Junction 332 in ``Town01.xodr`` holds this connection:

   .. code-block:: xml

      <connection id="0"
        incomingRoad="25"
        connectingRoad="333"
        contactPoint="start">
       <laneLink from="-1" to="-1"/>
      </connection>

   What does it say?

   A. Road 333 leads into road 25.

   B. From road 25's lane −1, the AV may drive on into lane −1 of road 333,
      a short road inside the junction that begins where road 25 ends.

   C. Roads 25 and 333 are two names for the same road.

   D. An AV in road 25's lane −1 must change to lane 1 before the junction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   ``incomingRoad`` is the road that leads into the junction, 25.
   ``connectingRoad`` is the path across the junction, road 333, the right
   turn. ``contactPoint="start"`` says road 333 begins where road 25 ends,
   so traffic drives it from its :math:`s = 0`. ``laneLink`` joins road
   25's lane −1 (driving south) to road 333's lane −1. Connection 3 does the
   same for road 339, the left turn. Together they give the split at the
   end of road 25's lane −1 its two edges. See Map to Graph in
   :doc:`l7_lecture`.


.. admonition:: Question 8
   :class: hint

   On the intersection graph, our route costs
   41 + 75 + 64 + 53 + 40 = 273 m. On the waypoint graph, the same route is
   260.6 m long. Why is the intersection graph 12.4 m longer?

   A. The intersection graph measures straight lines between its nodes.

   B. The intersection graph measures to each intersection's center, and
      the lanes cut through the turns.

   C. The waypoint graph's route skips intersection 3.

   D. The waypoint graph rounds each edge down to 2 m.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Each node of the intersection graph sits at the center of CARLA's
   rectangle around an intersection. An AV that turns does not drive
   through that center: its lane cuts the corner, so the waypoint graph
   gives a shorter length. 273 − 260.6 = 12.4 m. **A** is wrong: the edge
   lengths are whole meters along the lane, even where the figure draws the
   edge straight. One edge stands for a street's two lanes, with their
   average length. See Map to Graph in :doc:`l7_lecture`.


.. admonition:: Question 9
   :class: hint

   In Town03, the AV drives south on road 4 in the right lane, and it must
   turn left at junction 238. Which edges must its route hold, in order?

   A. Lane follow edges in the right lane, then the left turn through 238.

   B. Lane follow edges in the right lane, one lane change edge, lane follow
      edges in the left lane, then the left turn through 238.

   C. Lane follow edges in the right lane, then a lane change edge inside
      junction 238.

   D. Lane follow edges in the right lane, a U-turn, and the left lane back.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   On road 4, the left lane goes left or straight on, and the right lane
   goes right or straight on. From the right lane, the paths through 238 go
   only right or straight on, so a route with no lane change edge cannot
   turn left there. The map allows the lane change on all 92 m of road 4.
   The cost of a lane change edge is its length plus a penalty, and the
   search then decides where the AV changes lanes. See Lane Changes in
   :doc:`l7_lecture`.


.. admonition:: Question 10
   :class: hint

   The top speed in a curve of radius :math:`r` is
   :math:`\sqrt{a_{\mathrm{lat}}\, r}`, with
   :math:`a_{\mathrm{lat}} = 2.0` m/s² (chosen for the lecture). Town01's
   24 right-turn lanes have a median radius of 7.2 m, from the map. What is
   the AV's top speed in that turn?

   A. 3.79 m/s

   B. 14.4 m/s

   C. 11.18 m/s

   D. 2.68 m/s

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   :math:`\sqrt{2.0 \times 7.2} = \sqrt{14.4} = 3.79` m/s. **B** forgets
   the square root. **C** is the speed limit, which caps the speed only
   where the curve is wider than :math:`11.18^2 / 2.0 = 62.5` m. **D** drops
   :math:`a_{\mathrm{lat}}`: :math:`\sqrt{7.2} = 2.68`. A meter of this turn
   takes 11.18 / 3.79 = 2.9 times as long as a straight meter at the limit.
   See Edge Costs in :doc:`l7_lecture`.


.. admonition:: Question 11
   :class: hint

   Searched by distance, the route through intersections 1, 3, 5 and 6 is
   260.6 m long, and it has one left turn, at 5. The route through 1, 3, 4
   and 6 is 266.9 m long, and the left-turn penalty adds nothing to it. With
   a left-turn penalty of :math:`P = 5` m (chosen for this question), which
   route does the search pick?

   A. The route through 5.

   B. The route through 4.

   C. Neither: the two routes cost the same.

   D. Neither: the penalty blocks every route with a turn.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   1. The route through 5 costs 260.6 + 5 = 265.6 m.
   2. The route through 4 costs 266.9 m.
   3. 265.6 m is less, so the search keeps the route through 5.

   The route through 4 is 266.9 − 260.6 = 6.3 m longer, so a penalty
   switches the route only when it is above 6.3 m. With the lecture's
   :math:`P = 30` m, the route through 5 costs 260.6 + 30 = 290.6 m, and the
   route through 4 wins. See Edge Costs in :doc:`l7_lecture`.


.. admonition:: Question 12
   :class: hint

   GP4's settings are ``obstacle_clearance`` 3.0 m and ``max_deviation``
   2.0 m. Which situation fires one of GP4's two re-planning triggers?

   A. An object whose center is 3.4 m from the nearest waypoint of the path.

   B. The AV's base link is 1.6 m from the nearest waypoint of the path.

   C. An object whose center is 2.0 m beside the path, with waypoints every
      2 m.

   D. An object whose center is 2.5 m from the AV's base link, on the far
      side of the AV from the path, and 4.0 m from every waypoint.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Trigger 1 fires when an object's center is within 3.0 m of a waypoint.
   An object 2.0 m beside the path is within 3.0 m of three waypoints, as in
   the lecture's panel 1. **A** is farther than 3.0 m. **B** does not fire
   trigger 2, which needs more than 2.0 m. **D** does not fire trigger 1:
   the trigger measures from the object to the path's waypoints, not to the
   AV. See Re-planning in :doc:`l7_lecture`.


.. admonition:: Question 13
   :class: hint

   At one check, the localizer's pose is 2.3 m toward the other lane (chosen
   for this question). At the next check it is back, as after a bad scan
   match in L6. The AV itself never leaves its lane. What does the lecture
   say?

   A. Trigger 2 does not fire, because the AV did not move.

   B. Trigger 2 fires, and the planner throws away a good route. The planner
      should re-plan only when the deviation shows on 2 checks in a row.

   C. Trigger 1 fires, because the AV is now an obstacle on its own path.

   D. The planner should lower ``max_deviation`` to 1.0 m.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Trigger 2 compares the pose the localizer reports with the path, and
   2.3 m is more than 2.0 m, so it fires. The new start still lands on the
   AV's own lane, because it must face the way the AV drives, but the
   search is wasted. Waiting for 2 checks in a row (2 is chosen) is
   hysteresis again: a rule that waits before it acts. **D** makes the
   trigger fire even more often. See Re-planning in :doc:`l7_lecture`.


.. admonition:: Question 14
   :class: hint

   The lecture labels each intersection on the route by how much the
   heading turns in it: more than 30° left is a left turn, more than 30°
   right is a right turn, and less is straight on (the lecture chose 30°).
   In one intersection, the heading turns 20° to the left (chosen for this
   question). What is the maneuver?

   A. Turn left.

   B. Turn right.

   C. Straight on.

   D. Lane change.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   20° is less than 30°, so the intersection is labeled straight on. Our
   route has four maneuvers: turn right at 1, turn right at 3, turn left at
   5 and turn right at 6. Between intersections, the AV follows its lane.
   The next lectures' planners (L8, L9) need these maneuvers besides the
   waypoints. See Maneuvers in :doc:`l7_lecture`.


----


True or False (Questions 15 to 18)
==================================

.. admonition:: Question 15
   :class: hint

   The straight line from S to G is 141.9 m long, so the shortest drivable
   route from S to G is close to 141.9 m.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   No lane runs along the straight line: it crosses blocks with no lanes.
   The shortest drivable route turns four times and is 260.6 m long,
   260.6 − 141.9 = 118.7 m more than the line. The map gives only which lane
   leads to which, so a planner has to search for the route. See The Trip in
   :doc:`l7_lecture`.


.. admonition:: Question 16
   :class: hint

   At intersection 1 (junction 306), a search with the distance cost returns
   a U-turn whenever the U-turn is the shortest way to the goal.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Only the connections the file lists become edges. A U-turn has no
   connection, so it has no edge, and no search can return it.
   ``Town01.xodr`` has 0 U-turn connections. The traffic rules are in the
   graph's shape: the missing edges and the directions of the edges. See
   Map to Graph in :doc:`l7_lecture`.


.. admonition:: Question 17
   :class: hint

   On Town03's road 4, lane −1 says ``Both``, so our graph adds a lane change
   edge from lane −1 into the center lane, lane 1.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ``Both`` says an AV in lane −1 may move right, into lane −2, or left,
   into the center lane. But the center lane, lane 1, has no waypoints
   (``generate_waypoints`` skips it), so our graph has no node there. Our
   graph adds a lane change edge only between lanes that drive the same
   way, so the move into the center lane gets no edge. See Lane Changes in
   :doc:`l7_lecture`.


.. admonition:: Question 18
   :class: hint

   CARLA's ``GlobalRoutePlanner`` also runs A* on ``get_topology()``, so GP4
   Task 1 lets you call it inside your planner node.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   GP4 Task 1 asks you to write A* yourself, in ``astar_waypoints``. You may
   use ``GlobalRoutePlanner`` only in your tests, to check your routes. Its
   costs also differ from length: an edge costs the number of waypoints it
   samples along the road, one every ``sampling_resolution`` meters, and a
   lane change costs 0. See Maneuvers in :doc:`l7_lecture`.


----


Short Answer (Questions 19 to 20)
=================================

.. admonition:: Question 19
   :class: hint

   The street between S and intersection 1 has two lanes, one each way. Why
   does the intersection graph give S only one edge, S to 1, and no edge
   from 1 back to S?

.. dropdown:: Answer
   :class-container: sd-border-success

   S is a point in the westbound lane. The AV starts there facing west, so
   it can only drive toward 1. A route back to S would have to arrive in
   the westbound lane from the east, through the intersection at the
   street's other end, and that intersection is not in the intersection
   graph.

   In the waypoint graph, the two lanes are separate chains of nodes, and
   every edge points the way its lane drives. So the one-way start comes
   from the graph itself.


.. admonition:: Question 20
   :class: hint

   Searched by travel time, the trip's route is 6.3 m longer than the
   distance route but 3.3 s faster. Explain why, with the lecture's numbers.

.. dropdown:: Answer
   :class-container: sd-border-success

   The travel-time cost of an edge is its length divided by the AV's speed
   on it, worked out from the map before the drive. On a straight lane, the
   speed is the limit, 11.18 m/s. In a turn, it is at most
   :math:`\sqrt{2.0\, r}`: 3.79 m/s in the median right turn and 4.80 m/s in
   the median left turn. So a meter of the median right turn takes 2.9
   times as long as a straight meter, and a meter of the median left turn
   2.3 times.

   The distance route, through 1, 3, 5 and 6, is 260.6 m and takes 31.0 s.
   The travel-time route, through 1, 3, 4 and 6, is 266.9 m and takes
   27.7 s. It makes two turns against the distance route's four, and each
   turn caps the speed. So it is 266.9 − 260.6 = 6.3 m longer and
   31.0 − 27.7 = 3.3 s faster.
