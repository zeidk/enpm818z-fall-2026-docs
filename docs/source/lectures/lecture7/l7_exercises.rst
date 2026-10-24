====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Eight take-home exercises built on the Lecture 7 notes, :doc:`l7_lecture`, and
on the lecture's trip in Town01. They use only the lecture, never
:doc:`Going Further <l7_appendix>`. Exercises 1 and 2 read the map file:
one road and one junction. Exercise 3 counts Town01's graph. Exercise 4 works
through lane changes in Town03. Exercises 5 and 6 compute edge costs and
compare routes under three costs. Exercise 7 runs GP4's re-planning triggers
and hysteresis by hand, and Exercise 8 follows the route and labels its
maneuvers. Three exercises end with a check in the lecture's hands-on window.

.. note::

   Every exercise can be done with a calculator. The hands-on checks need
   ``l7_handson.py`` from folder ``lecture7`` of the course's Python
   repository, and no CARLA server.

   **The map frame** is L6's: :math:`x` east and :math:`y` north, in meters.
   CARLA's own :math:`y` points south, so the lecture flips its sign.

   **The trip** (start and goal chosen for the lecture): S is 41 m east of
   the center of intersection 1, with the AV driving west; G is 40 m east of
   the center of intersection 6, on the top street, driving east. The
   shortest route is 260.6 m long and turns at intersections 1, 3, 5 and 6,
   which the map file calls junctions 306, 171, 332 and 54. Numbers that are
   not the lecture's are marked "chosen for this exercise".

   None of these exercises asks you to write a search. You write A* in GP4,
   Task 1.


.. dropdown:: Exercise 1. Reading Road 25 in Town01.xodr
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Read one road of the map file, attribute by attribute, and work out where
   it runs, which junctions it joins, and how long the AV needs to drive it.

   .. raw:: html

      <hr>

   **Specification**

   Road 25, shortened from ``Town01.xodr`` as in the lecture (numbers
   rounded, lanes and signals cut):

   .. code-block:: xml

      <road name="Road 25"
        length="35.18" id="25" junction="-1">
       <link>
        <predecessor elementType="junction"
          elementId="54"/>
        <successor elementType="junction"
          elementId="332"/>
       </link>
       <type s="0" type="town">
        <speed max="25" unit="mph"/>
       </type>
       <planView>
        <geometry s="0" x="156.07"
          y="-11.02" hdg="-1.572"
          length="35.18">
         <line/>
        </geometry>
       </planView>
       ...
      </road>

   In ASAM OpenDRIVE, ``s`` is the distance along the reference line, the
   line the file draws the road along. ``x`` and ``y`` are the start of the
   geometry in the map frame, ``hdg`` is its start heading in radians,
   counterclockwise from east, and ``length`` is the length of its reference
   line. The road starts at its predecessor (:math:`s = 0`) and ends at its
   successor. One mile per hour is 0.44704 m/s.

   .. raw:: html

      <hr>

   **Part A. The road**

   1. Is road 25 inside a junction? Which attribute says so?
   2. Which junction is at the road's start, and which is at its end?
   3. Convert the speed limit to meters per second.

   .. raw:: html

      <hr>

   **Part B. The geometry**

   4. Convert ``hdg`` to degrees. Which way does the reference line point?
   5. Compute the end of the geometry, 35.18 m from its start. Which
      junction is there?
   6. The geometry holds ``<line/>``. What shape is the road?

   .. raw:: html

      <hr>

   **Part C. The lanes and the trip**

   Lane 1 lies on the left of the reference line, and lane −1 on its right,
   looking the way the line points. Each lane is 4.0 m wide.

   7. Which lane drives north, and which drives south?
   8. Which junction does an AV in lane −1 reach first? An AV in lane 1?
   9. Our route drives road 25 from intersection 5 to intersection 6. Which
      lane does it use?
   10. At the speed limit, how long does the AV need to drive road 25 from
       end to end?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 10, each with its arithmetic or the
   attribute it comes from.

   .. dropdown:: Guidance
      :color: success

      Question 1: no. ``junction="-1"`` means the road is not inside a
      junction. The roads inside a junction carry that junction's ID: the
      roads inside junction 332 say ``junction="332"``.

      Question 2: the predecessor, junction 54, is at the start
      (:math:`s = 0`). The successor, junction 332, is at the end.

      Question 3: 25 × 0.44704 = 11.18 m/s.

      Question 4:

      1. −1.572 × 180 / π = −90.07°.
      2. A negative heading turns clockwise from east. About a quarter turn
         clockwise from east is south: the line points south.

      Question 5:

      1. :math:`x = 156.07 + 35.18 \cos(-90.07^\circ) = 156.03` m with these
         rounded numbers. The lecture gives 156.02 m: the listing's numbers
         are rounded, so the last digit can differ.
      2. :math:`y = -11.02 + 35.18 \sin(-90.07^\circ) = -46.20` m.

      The line runs 35.18 m south, and its end is at junction 332, the
      successor.

      Question 6: one straight piece. ``<line/>`` is a straight line, so
      the whole 35.18 m of road 25 is straight.

      Question 7: the line points south. Looking south, the left is east, so
      lane 1, on the east side, drives north. Lane −1, on the west side,
      drives south.

      Question 8: lane −1 drives with :math:`s`, from the start to the end,
      so an AV in it reaches junction 332 first. Lane 1 drives against
      :math:`s`, so an AV in it reaches the predecessor first: junction 54.

      Question 9: intersection 5 is junction 332, at the south end, and
      intersection 6 is junction 54, at the north end. The route drives
      north, so it uses lane 1.

      Question 10: the road is straight, so the speed limit sets the speed:
      35.18 / 11.18 = 3.15 s.


.. dropdown:: Exercise 2. Reading a Junction Element
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Read two connections of junction 332, say which graph edges they become,
   and see how the junction keeps a U-turn out of the graph.

   .. raw:: html

      <hr>

   **Specification**

   Junction 332 is intersection 5 on our route, at the south end of road 25.
   Two of its connections, from ``Town01.xodr``:

   .. code-block:: xml

      <junction id="332"
        name="junction332">
       <connection id="0"
         incomingRoad="25"
         connectingRoad="333"
         contactPoint="start">
        <laneLink from="-1" to="-1"/>
       </connection>
       <connection id="3"
         incomingRoad="25"
         connectingRoad="339"
         contactPoint="start">
        <laneLink from="-1" to="-1"/>
       </connection>
        ...

   ASAM OpenDRIVE defines ``incomingRoad`` as the "ID of the incoming road",
   ``connectingRoad`` as the "ID of the connecting road", ``contactPoint`` as
   the "Contact point on the @connectingRoad", and ``laneLink`` ``from`` and
   ``to`` as the "ID of the incoming lane" and the "ID of the connection
   lane".

   .. raw:: html

      <hr>

   **Part A. One connection**

   1. Say in one sentence what connection 0 allows.
   2. What does ``contactPoint="start"`` tell you about road 333?
   3. Road 333 is the right turn and road 339 the left turn. An AV that
      leaves road 25 by road 333 drives south first. In which direction
      does it leave the junction?

   .. raw:: html

      <hr>

   **Part B. The graph**

   4. Connections 0 and 3 start from the same lane. What do they become in
      the waypoint graph? Name the node they leave from, and say how many
      edges leave it.
   5. Does our trip use connection 0 or 3 at intersection 5? Use the route
      of the lecture: it comes east on road 9's lane −1 and turns left,
      through road 334, onto road 25.
   6. The junction lists no connection from road 25's lane −1 into road
      25's lane 1. What does that mean for every search on this graph?

   .. raw:: html

      <hr>

   **Deliverable**

   A sentence for each of questions 1 to 6.

   .. dropdown:: Guidance
      :color: success

      Question 1: from road 25's lane −1, driving south, the AV may drive on
      into lane −1 of road 333, a short road inside the junction.

      Question 2: road 333 begins where road 25 ends, so traffic drives road
      333 from its :math:`s = 0`.

      Question 3: west. An AV driving south that turns right ends up driving
      west, as the lecture's figure of intersection 5 shows.

      Question 4: they become the two edges out of a split. The node is the
      last waypoint of road 25's lane −1, where the lane meets the
      intersection. One edge leads into road 333's lane −1 (the right turn)
      and one into road 339's lane −1 (the left turn). Every node that is
      not a split has one edge out.

      Question 5: neither. Both connections leave road 25's lane −1, which
      drives south, away from intersection 6. Our route enters junction 332
      from road 9 and leaves it on road 25's lane 1, driving north, so it
      uses the connection for road 334.

      Question 6: only the connections the file lists become edges. With no
      connection for the U-turn, there is no edge for it, so no search can
      return it, whatever cost it uses. ``Town01.xodr`` has 0 U-turn
      connections.


.. dropdown:: Exercise 3. Counting Town01's Graph
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Work out the counts the lecture measured on Town01, from the town's
   layout, and check them in the hands-on window.

   .. raw:: html

      <hr>

   **Specification**

   From the lecture, measured with ``carla.Map`` on ``Town01.xodr``:

   - 26 roads run between intersections, each with one lane each way. There
     are 12 T-intersections, with 3 roads into each.
   - ``get_topology()`` returns a segment as a pair of waypoints, one pair
     per segment and way out: 160 pairs. A segment is one lane of one road,
     in driving order. Through the intersections there are 24 left turns,
     24 right turns and 24 straight on.
   - ``generate_waypoints(2.0)`` returns 3266 waypoints.
   - The waypoint graph has 3107 nodes and 3143 edges. All its edges
     together are 6400.4 m long, and the median edge is 2.00 m (shortest
     1.38 m, longest 4.03 m).

   .. raw:: html

      <hr>

   **Part A. The 160 pairs**

   1. How many lanes run outside the intersections?
   2. How many of those lanes end at a split, where the AV can go two ways?
   3. Each of those lanes is listed once for each lane it leads into. How
      many pairs do the lanes outside the intersections give?
   4. How many segments run through the intersections? Check your answer
      against the 24 + 24 + 24 turns.
   5. Add up the pairs and the segments.

   .. raw:: html

      <hr>

   **Part B. The waypoint graph**

   6. Explain the 3143 edges from the 3107 nodes.
   7. The graph has fewer nodes than ``generate_waypoints`` returns. How many
      fewer, and why?
   8. Compute the mean edge length and compare it with the median.

   .. raw:: html

      <hr>

   **Part C. Hands-on check**

   Run ``python3 l7_handson.py --part graph`` and click node 224 at
   intersection 3 (it is amber).

   9. How many successors does the box list, and how long is each edge?
      Why is the node amber?

   .. raw:: html

      <hr>

   **Deliverable**

   The counts with their arithmetic, a sentence each for questions 6 and 7,
   and the box's numbers for node 224.

   .. dropdown:: Guidance
      :color: success

      Question 1: 26 × 2 = 52 lanes.

      Question 2: 12 × 3 = 36 lanes, one for each road into each
      intersection. These are the 36 splits.

      Question 3: each of the 36 lanes is listed twice, so 36 pairs are
      added to the 52: 52 + 36 = 88 pairs. Road 9's eastbound lane, from
      intersection 3 to intersection 5, is one of them.

      Question 4: each of the 36 splits leads into 2 short roads, so
      36 × 2 = 72 segments. That matches 24 + 24 + 24 = 72.

      Question 5: 88 + 72 = 160 pairs, for 52 + 72 = 124 segments.

      Question 6: every node has one edge out, and each of the 36 splits has
      a second one: 3107 + 36 = 3143.

      Question 7: 3266 − 3107 = 159 fewer. Where a lane ends and a single
      lane continues, the graph keeps one node, not two. At a split, each
      way out starts with its own node.

      Question 8: 6400.4 / 3143 = 2.04 m, close to the 2.00 m median, as you
      expect with a waypoint every 2 m. The edges range from 1.38 m to
      4.03 m.

      Question 9: two successors, node 225 and node 2934, each 2.00 m ahead
      and at one point (ringed in the window): straight on and a right turn,
      which part about 7 m on. The node is amber because it is a split.


.. dropdown:: Exercise 4. Lane Changes on Town03's Road 4
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Read road 4's lanes and their ``lane_change`` fields, find the lane change
   edges our graph adds, and list a route's edges before a turn.

   .. raw:: html

      <hr>

   **Specification**

   Town03's road 4 runs south toward junction 238. OpenDRIVE numbers a
   road's lanes outward from its reference line: 1, 2, 3 on its left and
   −1, −2 on its right, looking the way it points (south). Lanes −2 and −1
   drive south, lanes 2 and 3 drive north, and lane 1, in the middle, is a
   center lane that traffic from both directions may use.

   Each CARLA waypoint has a field, ``lane_change``, that says to which side
   an AV on it may change lanes: ``NONE``, ``Left``, ``Right`` or ``Both``,
   seen from the AV facing the way its lane drives. On road 4:

   .. list-table::
      :widths: 30 70
      :header-rows: 1
      :class: compact-table

      * - **Lane**
        - ``lane_change``
      * - −2
        - ``Left``
      * - −1
        - ``Both``
      * - 1
        - no waypoints (``generate_waypoints`` skips it)
      * - 2
        - ``Right``
      * - 3
        - ``Left``

   Our graph adds a lane change edge only between lanes that drive the same
   way. Before junction 238, the left lane goes left or straight on, and the
   right lane goes right or straight on.

   .. raw:: html

      <hr>

   **Part A. The lanes**

   1. An AV drives south on road 4. Which lane, −1 or −2, is its left lane?
   2. For each lane, say which lane an AV there may move into.
   3. Which lane change edges does our graph add on road 4? Which allowed
      move gets no edge, and why?

   .. raw:: html

      <hr>

   **Part B. Routes before junction 238**

   4. The AV drives south in the left lane and must turn right at 238. List
      the kinds of edge its route must hold, in order. Does the map allow
      the lane change it needs?
   5. The AV drives south in the right lane and must go straight on. Does
      its route need a lane change edge?

   .. raw:: html

      <hr>

   **Part C. Town01 against Town03**

   Measured with ``carla.Map``, waypoints every 2 m:

   .. list-table::
      :widths: 56 22 22
      :header-rows: 1
      :class: compact-table

      * - **Measured**
        - **Town01**
        - **Town03**
      * - Road sections outside the intersections with 2 or more lanes the
          same way
        - 0 of 26
        - 37 of 68
      * - Waypoints where the map allows a lane change
        - 0
        - 4241
      * - Approaches to an intersection with 2 or more lanes
        - 0
        - 49 of 89
      * - Of them, approaches whose lanes lead to different turns
        - 0
        - 22

   A road section is a stretch of one road with a fixed set of lanes; an
   approach is one road's lanes entering one intersection.

   6. Why does Town01's graph need no lane change edges?
   7. Of Town03's approaches with 2 or more lanes, what share has lanes that
      lead to different turns?

   .. raw:: html

      <hr>

   **Deliverable**

   The lane change edges of road 4, the two routes as lists of edge kinds,
   and a sentence each for questions 6 and 7.

   .. dropdown:: Guidance
      :color: success

      Question 1: lane −1. Looking south, the AV's left is east. Lanes are
      numbered outward from the reference line, so lane −1 lies next to the
      center lane and lane −2 farther out, to the west. Lane −1 is the left
      lane, and lane −2 the right lane.

      Question 2:

      - Lane −2, ``Left``: only into lane −1.
      - Lane −1, ``Both``: right into lane −2, or left into the center lane.
      - Lane 2, ``Right``: only into lane 3, not into the center lane.
      - Lane 3, ``Left``: only into lane 2.

      Question 3: four kinds: lane −2 to lane −1, lane −1 to lane −2, lane 2
      to lane 3 and lane 3 to lane 2. The move from lane −1 into the center
      lane is allowed but gets no edge: the center lane has no waypoints, so
      the graph has no node there, and it does not drive one way with lane
      −1.

      Question 4:

      1. Lane follow edges in the left lane, lane −1.
      2. One lane change edge, from lane −1 to lane −2.
      3. Lane follow edges in the right lane, lane −2.
      4. The right turn through junction 238.

      The map allows it: lane −1 says ``Both``, so the AV may move right
      into lane −2. The cost of a lane change edge is its length plus a
      penalty, and the search decides where the AV changes lanes.

      Question 5: no. The right lane goes right or straight on, so lane
      follow edges and the straight way through 238 are enough.

      Question 6: every road in Town01 has one lane each way, so no two
      lanes drive the same way side by side, and no waypoint allows a lane
      change. The road the AV takes also fixes its lane.

      Question 7: 22 / 49 = 0.45, so 45%. At those 22 approaches, the turn
      decides which lane the AV must be in before it reaches the
      intersection.


.. dropdown:: Exercise 5. Top Speed and Travel Time
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compute the travel-time cost of edges, straight and in turns, with the
   lecture's top speed in a curve, and run the lecture's cost code by hand
   on one edge.

   .. raw:: html

      <hr>

   **Specification**

   The travel-time cost of an edge :math:`\ell` meters long is
   :math:`\ell / v` seconds. The speed :math:`v` is the lower of the speed
   limit and the curve's top speed :math:`\sqrt{a_{\mathrm{lat}}\, r}`, where
   :math:`r` is the radius of the circle the lane follows and
   :math:`a_{\mathrm{lat}} = 2.0` m/s² (chosen for the lecture). Town01's
   speed limit is 25 mph, 11.18 m/s. The lecture computes the three costs
   for all 3143 edges with this code:

   .. code-block:: python

      turn = np.radians(wrap_deg(yaw[et] - yaw[ef]))  # rad
      kappa = np.abs(turn) / el          # curvature: 1 / radius
      kappa = np.maximum(kappa, 1e-12)   # never exactly 0
      v = np.minimum(v_limit, np.sqrt(a_lat / kappa))  # m/s
      cost_distance = el                           # 1. meters
      cost_time = el / v                           # 2. seconds
      cost_left = el + np.where(is_left, P, 0.0)   # 3. meters

   Edge ``i`` goes from node ``ef[i]`` to node ``et[i]`` and is ``el[i]``
   meters long. ``yaw`` holds each node's heading in degrees, and
   ``wrap_deg`` brings a change of heading into −180 to 180 degrees.
   ``v_limit`` is 11.18 m/s, ``a_lat`` is 2.0 m/s² and ``P`` is 30 m.
   ``is_left`` is true on the first edge of each left turn.

   .. raw:: html

      <hr>

   **Part A. Straight edges**

   1. A 100 m straight edge has a 25 mph limit. Compute its travel time.
      Then compute it with a 15 mph limit (1 mph = 0.44704 m/s). How much
      longer is it?

   .. raw:: html

      <hr>

   **Part B. Turns**

   2. At which radius does :math:`\sqrt{2.0\, r}` reach the speed limit?
   3. Town01's 24 right-turn lanes have a median radius of 7.2 m, and its 24
      left-turn lanes a median of 11.5 m (both from the map). Compute the top
      speed in each.
   4. How many times as long as a straight meter does a meter of each turn
      take?

   .. raw:: html

      <hr>

   **Part C. The code on one edge**

   An edge is 2.00 m long, and the heading turns 15° from its first node to
   its second (chosen for this exercise).

   5. Compute ``turn``, ``kappa``, the radius and ``v``.
   6. Compute the three costs, first for an edge in the middle of a left
      turn, then for the first edge of a left turn.
   7. On a straight edge, ``turn`` is 0. What do ``kappa`` and ``v`` become,
      and why does the code need ``np.maximum``?

   .. raw:: html

      <hr>

   **Part D. Hands-on check**

   Run ``python3 l7_handson.py --part costs`` and click the edge the lecture
   clicks, near :math:`x = 146` m, :math:`y = -59` m.

   8. The box lists edges 0 and 31, which leave node 0. Write down their
      three costs. Check the travel time with the speed limit. Why does edge
      31 cost 32.00 m with the penalty?

   .. raw:: html

      <hr>

   **Deliverable**

   The travel times of Part A, the speeds and ratios of Part B, the values of
   Part C in numbered steps, and the box's numbers for Part D.

   .. dropdown:: Guidance
      :color: success

      Question 1:

      1. 15 mph is 15 × 0.44704 = 6.71 m/s.
      2. At 11.18 m/s: 100 / 11.18 = 8.9 s.
      3. At 6.71 m/s: 100 / 6.71 = 14.9 s.
      4. The slower limit costs 6.0 s more. The speed limit is not a cost by
         itself, but it sets :math:`v` in :math:`\ell / v`.

      Question 2: set :math:`\sqrt{2.0\, r} = 11.18`, so
      :math:`r = 11.18^2 / 2.0 = 62.5` m. In a curve wider than that, the
      speed limit caps the speed.

      Question 3:

      - Right turn: :math:`\sqrt{2.0 \times 7.2} = \sqrt{14.4} = 3.79` m/s.
      - Left turn: :math:`\sqrt{2.0 \times 11.5} = \sqrt{23} = 4.80` m/s.

      Question 4: the median right turn takes 11.18 / 3.79 = 2.9 times as
      long as a straight meter, and the median left turn 11.18 / 4.80 = 2.3
      times.

      Question 5:

      1. ``turn`` = 15 × π / 180 = 0.2618 rad.
      2. ``kappa`` = 0.2618 / 2.00 = 0.1309 per meter.
      3. The radius is 1 / 0.1309 = 7.64 m.
      4. :math:`\sqrt{2.0 / 0.1309} = \sqrt{15.28} = 3.91` m/s, below the
         limit, so ``v`` = 3.91 m/s.

      Question 6: for an edge in the middle of the turn, ``cost_distance``
      is 2.00 m, ``cost_time`` is 2.00 / 3.91 = 0.512 s, and ``cost_left``
      is 2.00 m, because ``is_left`` is false. For the first edge of a left
      turn, ``cost_left`` is 2.00 + 30 = 32.00 m. A left turn adds ``P``
      once.

      Question 7: ``np.abs(turn) / el`` is 0, and ``np.maximum`` raises it
      to 1e-12. Then :math:`\sqrt{2.0 / 10^{-12}} = 1.41 \times 10^6` m/s,
      and ``np.minimum`` picks the limit, 11.18 m/s. Without
      ``np.maximum``, the code would divide by 0.

      Question 8: both edges cost 2.00 m and 0.179 s. They leave node 0
      along the same first 2 m, where the heading does not change yet, so
      the speed limit sets the speed: 2.00 / 11.18 = 0.179 s. Edge 31 starts
      a left turn, so its penalty cost is 2.00 + 30 = 32.00 m.


.. dropdown:: Exercise 6. Routes Under Three Costs
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   List the routes of the intersection graph by hand, compare the two
   routes the lecture found under three costs, and find the penalty that
   switches the route.

   .. raw:: html

      <hr>

   **Specification**

   The intersection graph has the nodes S, G and intersections 1 to 7. Its
   edges, with their lengths in whole meters along the lane: S to 1, 41
   (one way, from S); 1 to 2, 67; 1 to 3, 75; 3 to 4, 55; 3 to 5, 64; 4 to
   6, 66; 5 to 6, 53; 5 to 7, 179; 6 to G, 40 (one way, into G). The other
   edges each stand for a street's two lanes, one each way.

   On the waypoint graph, the lecture searched the trip once with each cost:

   .. list-table::
      :widths: 34 22 22 22
      :header-rows: 1
      :class: compact-table

      * - **Cost**
        - **Through**
        - **Length (m)**
        - **Time (s)**
      * - distance
        - 1, 3, 5, 6
        - 260.6
        - 31.0
      * - travel time
        - 1, 3, 4, 6
        - 266.9
        - 27.7
      * - left-turn penalty
        - 1, 3, 4, 6
        - 266.9
        - 27.7

   The left-turn penalty cost is each edge's length in meters, plus
   :math:`P` on the edge that starts a left turn. The route through 5 turns
   left at 5; the route through 4 makes no left turn.

   .. raw:: html

      <hr>

   **Part A. The intersection graph by hand**

   1. List every route from S to G that visits no node twice. Why can a
      route not go through 2 or 7?
   2. Add up the length of each route. Which is shorter?

   .. raw:: html

      <hr>

   **Part B. The waypoint graph**

   3. How much longer is the travel-time route, and how much faster?
   4. Compute the mean speed of each route.
   5. Explain why the longer route is faster.

   .. raw:: html

      <hr>

   **Part C. The penalty that switches the route**

   6. With :math:`P = 30` m, compute the penalty cost of both routes. Which
      does the search pick?
   7. Above which :math:`P` does the search pick the route through 4? Check
      your answer with :math:`P = 5` m (chosen for this exercise).
   8. On the intersection graph, above which :math:`P` would the route
      through 4 win? Why does it differ from question 7?

   .. raw:: html

      <hr>

   **Deliverable**

   The routes and their sums, the differences and mean speeds, the penalty
   costs, and the two values of :math:`P` that switch the route.

   .. dropdown:: Guidance
      :color: success

      Question 1: from S, the only edge goes to 1. From 1, the edge to 2
      ends there: 2 has no other edge, so a route into 2 must come back
      through 1. The same holds for 7, reached only from 5. From 3 a route
      goes on to 4 or to 5, and both lead to 6, the only node joined to G.
      So there are two routes: S, 1, 3, 5, 6, G and S, 1, 3, 4, 6, G.

      Question 2:

      - Through 5: 41 + 75 + 64 + 53 + 40 = 273 m.
      - Through 4: 41 + 75 + 55 + 66 + 40 = 277 m.

      The route through 5 is shorter by 277 − 273 = 4 m. It is our route.

      Question 3: 266.9 − 260.6 = 6.3 m longer, and 31.0 − 27.7 = 3.3 s
      faster.

      Question 4: through 5, 260.6 / 31.0 = 8.4 m/s. Through 4,
      266.9 / 27.7 = 9.6 m/s.

      Question 5: the route through 4 makes two turns, against four for the
      route through 5, and each turn caps the speed (Exercise 5: a meter of
      the median right turn takes 2.9 times as long as a straight meter). So
      more of its length is driven at the speed limit.

      Question 6: through 5, 260.6 + 30 = 290.6 m. Through 4, 266.9 m, with
      no penalty. The search picks the route through 4.

      Question 7: the route through 5 costs 260.6 + :math:`P`, and the route
      through 4 costs 266.9. The route through 4 wins when :math:`P` is
      above 266.9 − 260.6 = 6.3 m. With :math:`P = 5` m, the route through 5
      costs 260.6 + 5 = 265.6 m, less than 266.9 m, so the search keeps it.

      Question 8: 273 + :math:`P` against 277, so above 4 m. The value of
      :math:`P` that switches the route is the difference in length between
      the two routes on the graph that is searched. The intersection graph
      measures to each intersection's center, and the lanes cut through the
      turns, so its lengths differ from the waypoint graph's. A search uses
      one cost on one graph; in GP4 you choose the cost.


.. dropdown:: Exercise 7. Re-planning Triggers and Hysteresis
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run GP4's two triggers by hand, size the time between checks, read the
   lecture's detour, and apply a hysteresis rule to a detector that comes
   and goes.

   .. raw:: html

      <hr>

   **Specification**

   GP4's settings, in ``planner_config.yaml``: ``obstacle_clearance``
   3.0 m, ``max_deviation`` 2.0 m and ``replan_frequency`` 2.0 Hz.
   Trigger 1 fires when perception reports an object whose center is within
   3.0 m of a waypoint of the path. Trigger 2 fires when the AV's base link
   is more than 2.0 m from the nearest waypoint.

   For Part A, the path runs along the :math:`x` axis from 0 to 30 m, with a
   waypoint every 2 m at :math:`y = 0`, as in the lecture's panel 1.

   .. raw:: html

      <hr>

   **Part A. The two triggers**

   1. The lecture's object is at (20, 2.0). Which waypoints are within
      3.0 m of it?
   2. Redo question 1 for objects at (20, 2.5), (21, 2.5) and (20, 3.5)
      (chosen for this exercise). Which of them fire trigger 1?
   3. The AV's base link is 1.8 m from the nearest waypoint, then 2.5 m
      (1.8 m chosen for this exercise, 2.5 m the lecture's). Does trigger 2
      fire each time?

   .. raw:: html

      <hr>

   **Part B. How often to check**

   4. At 2.0 Hz, how long can a new obstacle wait for the next check? How
      far does the AV drive in that time at 8.0 m/s (the controller's
      default ``target_speed``)? At 11.18 m/s, the speed limit?

   .. raw:: html

      <hr>

   **Part C. The detour**

   In the lecture, the AV drives north before intersection 3, and an
   obstacle is reported on the road from 5 to 6. The planner deletes the 4
   edges that start or end within 3.0 m of it and searches again from the
   waypoint nearest the AV. The new route, straight on at 3 and right at 4,
   is 178.9 m long. The old route had 172.6 m left.

   5. How long is the detour? How far along the old 260.6 m route is the AV?
   6. The travel-time route of Exercise 6 also goes through 1, 3, 4 and 6,
      and is 266.9 m long. Compare its length after the AV's position with
      the new route. Why is the detour also 6.3 m?

   .. raw:: html

      <hr>

   **Part D. Hysteresis**

   The planner checks every 0.5 s, from 0 to 4.5 s: ten checks. Without a
   rule, it picks route B (around the obstacle) at every check where the
   detector reports the obstacle, and route A (the original route)
   otherwise. With the lecture's rule, it switches to B at a check where
   the detector reports the obstacle, and back to A only at the third check
   in a row where it does not. A change is a check whose route differs
   from the one before.

   7. The lecture's detector reports the obstacle at 0, 1.0, 1.5 and 2.5 s.
      Write the route at each check without the rule and with it, and count
      the changes.
   8. Redo question 7 with "back to A at the second check in a row" (chosen
      for this exercise). When does the route change back?
   9. A second detector reports the obstacle at 0.5, 1.0, 2.0 and 3.5 s
      (chosen for this exercise), and the planner starts on A at 0 s. Count
      the changes without a rule, with the third-check rule and with the
      second-check rule.

   .. raw:: html

      <hr>

   **Deliverable**

   The waypoints within 3.0 m for each object, the verdicts of Part A, the
   wait and distance of Part B, the detour, and the three rows of routes in
   Part D with their changes.

   .. dropdown:: Guidance
      :color: success

      Question 1: the distance from (20, 2.0) to a waypoint at
      :math:`(x, 0)` is :math:`\sqrt{(x - 20)^2 + 2.0^2}`.

      - :math:`x = 20`: 2.0 m.
      - :math:`x = 18` and :math:`x = 22`: :math:`\sqrt{4 + 4} = 2.83` m.
      - :math:`x = 16` and :math:`x = 24`: :math:`\sqrt{16 + 4} = 4.47` m.

      Three waypoints, at 18, 20 and 22 m, are within 3.0 m: the three red
      points of the lecture's panel 1.

      Question 2:

      - (20, 2.5): only :math:`x = 20`, 2.5 m. The next ones are
        :math:`\sqrt{4 + 6.25} = 3.20` m away. Trigger 1 fires.
      - (21, 2.5): :math:`x = 20` and :math:`x = 22`, each
        :math:`\sqrt{1 + 6.25} = 2.69` m away. Trigger 1 fires.
      - (20, 3.5): the nearest waypoint is 3.5 m away. Trigger 1 does not
        fire.

      Question 3: at 1.8 m, no: the trigger needs more than 2.0 m. At 2.5 m,
      yes.

      Question 4: 1 / 2.0 = 0.5 s. At 8.0 m/s, 8.0 × 0.5 = 4.0 m. At
      11.18 m/s, 11.18 × 0.5 = 5.59 m. A check only measures distances to
      the route's waypoints, which is fast; a search runs only when a
      trigger fires.

      Question 5: 178.9 − 172.6 = 6.3 m. The AV has driven
      260.6 − 172.6 = 88.0 m of the old route.

      Question 6: the travel-time route shares the old route as far as
      intersection 3, so the AV is 88.0 m along it too. It has
      266.9 − 88.0 = 178.9 m left, the length of the new route: the new
      route is the rest of the travel-time route. Its detour is the same
      6.3 m by which the travel-time route was longer.

      Question 7:

      .. list-table::
         :widths: 34 66
         :header-rows: 1
         :class: compact-table

         * - **Checks, 0 to 4.5 s**
           - **Route at each check**
         * - No rule
           - B, A, B, B, A, B, A, A, A, A: 5 changes
         * - Third check in a row
           - B, B, B, B, B, B, B, B, A, A: 1 change, at 4.0 s

      These are the lecture's rows 2 and 3.

      Question 8: B, B, B, B, B, B, B, A, A, A. The checks at 3.0 and 3.5 s
      are the first two in a row without the obstacle, so the route changes
      back at 3.5 s: still one change.

      Question 9:

      - No rule: A, B, B, A, B, A, A, B, A, A: 6 changes.
      - Third check in a row: A, B, B, B, B, B, B, B, B, B: 1 change, at
        0.5 s. After 3.5 s only two checks without the obstacle are left, so
        the route stays B.
      - Second check in a row: A, B, B, B, B, B, A, B, B, A: 4 changes, at
        0.5, 3.0, 3.5 and 4.5 s.

      The longer the rule waits, the fewer the changes. Without hysteresis,
      L9's motion planner could get a new route to follow as often as every
      half second.


.. dropdown:: Exercise 8. Following the Route, and Its Maneuvers
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Label intersections by their maneuvers, compute what the AV reports
   while it follows the route, and compare CARLA's ``GlobalRoutePlanner``
   costs with distance costs.

   .. raw:: html

      <hr>

   **Specification**

   The lecture labels each intersection on the route by how much the
   heading turns in it: more than 30° left is a left turn, more than 30°
   right a right turn, and less is straight on (30° chosen for the
   lecture). Between re-plans, the AV's pose and the route give where the
   AV is on the route (the route waypoint nearest its pose), the distance
   left, and the next maneuver. On our trip, the route is 260.6 m long and
   enters intersection 3 at 99.7 m.

   CARLA's ``GlobalRoutePlanner`` returns each waypoint of a route with a
   ``RoadOption``: ``LANEFOLLOW``, ``LEFT``, ``RIGHT``, ``STRAIGHT``,
   ``CHANGELANELEFT``, ``CHANGELANERIGHT``, or ``VOID`` for none. An edge of
   its graph costs the number of waypoints it samples along the road, one
   every ``sampling_resolution`` meters, so about its length divided by that
   spacing; a lane change costs 0.

   .. raw:: html

      <hr>

   **Part A. Maneuvers**

   1. Label four intersections whose heading turns 88° right, 12° left, 92°
      left and 35° right (all chosen for this exercise).
   2. Write our route's four maneuvers, and what the AV does between them,
      with the ``RoadOption`` names.

   .. raw:: html

      <hr>

   **Part B. Following the route**

   3. The AV is 50.0 m along the route (the lecture's example). Give the
      distance left and the distance to the next maneuver.
   4. Redo question 3 with the AV 80.0 m along the route (chosen for this
      exercise).
   5. Which part of GP4's planner does the same nearest-waypoint lookup?

   .. raw:: html

      <hr>

   **Part C. GlobalRoutePlanner's costs**

   6. Road 9's eastbound lane, from intersection 3 to intersection 5, is a
      43.6 m segment. About what does its edge cost with
      ``sampling_resolution`` 2.0 m, and with 1.0 m (both chosen for this
      exercise)?
   7. On Town01, would ``GlobalRoutePlanner`` and a distance-cost search
      rank routes about the same way? Where would the two differ on Town03?

   .. raw:: html

      <hr>

   **Deliverable**

   The four labels, the route's maneuvers, the distances of Part B with
   their arithmetic, and a sentence each for questions 5 to 7.

   .. dropdown:: Guidance
      :color: success

      Question 1: 88° right is more than 30°, so a right turn. 12° left is
      less than 30°, so straight on. 92° left is a left turn. 35° right is a
      right turn.

      Question 2: ``RIGHT`` at 1, ``RIGHT`` at 3, ``LEFT`` at 5 and
      ``RIGHT`` at 6, with ``LANEFOLLOW`` between the intersections: the
      lecture's table says turn right, turn right, turn left and turn right,
      and between intersections the AV follows its lane.

      Question 3:

      1. Distance left: 260.6 − 50.0 = 210.6 m.
      2. Next maneuver: turn right at 3, which the route enters at 99.7 m,
         so 99.7 − 50.0 = 49.7 m ahead.

      Question 4:

      1. Distance left: 260.6 − 80.0 = 180.6 m.
      2. The AV has not reached intersection 3 yet, so the next maneuver is
         still turn right at 3, 99.7 − 80.0 = 19.7 m ahead.

      Question 5: trigger 2, which measures the AV's base link to the
      nearest waypoint of the path. A navigation app shows the same three
      things: where you are, how far is left, and the next turn.

      Question 6: about 43.6 / 2.0 = 21.8, so about 22 waypoints, at 2.0 m,
      and about 43.6 / 1.0 = 43.6, so about 44, at 1.0 m. Either way, the
      cost is about the length divided by the spacing.

      Question 7: on Town01, about the same. Every edge costs about its
      length divided by the same spacing, and Town01 has no lane change
      edges. On Town03, a lane change costs 0 in ``GlobalRoutePlanner`` but
      its length plus a penalty in our graph, so on a route with a lane
      change the two costs differ, and the two searches need not agree.
      That is why the lecture says to
      compare it with your distance costs at the same 2 m spacing, and to
      use it only in your tests.
