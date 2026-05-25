====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 8. Exercises cover road graph construction, route planning
algorithms, and dynamic rerouting.


.. dropdown:: Exercise 1 -- Road Graph Construction
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Build a directed road graph from CARLA waypoints and analyze its
   structure.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``road_graph.py`` that performs the following:

   1. Load **Town01** and generate waypoints at **5.0 m** spacing.
   2. Build a **directed graph** where:

      - Each waypoint is a node (keyed by its ``id``).
      - Lane-follow edges connect to ``waypoint.next(5.0)``.
      - Lane-change edges connect to ``get_left_lane()`` /
        ``get_right_lane()`` (if they exist and are drivable).

   3. Report the following statistics:

      - Total number of **nodes** and **edges**.
      - Number of **junction waypoints** (``is_junction == True``).
      - Number of **lane-change edges** vs. **lane-follow edges**.

   4. Repeat for **Town03** and compare.

   **Expected output**

   .. code-block:: text

      Town01: nodes=1234, edges=2345, junctions=189, lane_follow=2100, lane_change=245
      Town03: nodes=3456, edges=6789, junctions=412, lane_follow=5800, lane_change=989

   (Exact numbers will vary.)

   **Deliverable**

   The script and a comparison table for both towns.


.. dropdown:: Exercise 2 -- Dijkstra vs. A* Comparison
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Implement and compare Dijkstra and A* on a CARLA road graph,
   measuring optimality and efficiency.


   .. raw:: html

      <hr>


   **Specification**

   Using the road graph from Exercise 1 (Town01):

   1. Implement **Dijkstra's algorithm** with edge weight = Euclidean
      distance between waypoints.
   2. Implement **A* search** with heuristic = Euclidean distance to
      goal.
   3. Plan a route between two distant spawn points and record:

      - **Nodes expanded** by each algorithm.
      - **Total path distance** (should be identical -- explain why).
      - **Computation time**.

   4. Implement **Weighted A*** with :math:`\epsilon = 2.0`. Record
      nodes expanded and path distance.

   Print a comparison table:

   .. code-block:: text

      Algorithm      | Nodes expanded | Path dist (m) | Time (ms)
      Dijkstra       |           1842 |         623.5 |      45.2
      A*             |            534 |         623.5 |      12.1
      Weighted A*    |            287 |         641.2 |       6.8

   **Written analysis**

   Why does Dijkstra and A* produce the same path distance? Why might
   Weighted A* produce a longer path?

   **Deliverable**

   The script, comparison table, and written analysis.


.. dropdown:: Exercise 3 -- Cost Function Design
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Design multi-objective cost functions for route planning and
   observe how they change the selected route.


   .. raw:: html

      <hr>


   **Specification**

   The route planner evaluates edges using:

   .. math::

      c(e) = w_d \cdot d(e) + w_t \cdot t(e) + w_m \cdot m(e)
             + w_r \cdot r(e)

   where:

   - :math:`d(e)` = edge distance (m)
   - :math:`t(e)` = estimated travel time (s), assuming speed limit
   - :math:`m(e)` = maneuver complexity (0 = straight, 0.5 = lane
     change, 1.0 = turn)
   - :math:`r(e)` = road class penalty (0 = highway, 0.5 = arterial,
     1.0 = residential)

   1. Choose weights for the **fastest route** (minimize travel time).
   2. Choose weights for the **most comfortable route** (fewest
      maneuvers, avoid small roads).
   3. Plan the same origin-destination pair with both weight sets in
      CARLA.
   4. Visualize both routes using ``world.debug.draw_string()`` (red
      for fastest, blue for most comfortable).
   5. Report the total distance, estimated time, and maneuver count
      for each route.

   **Deliverable**

   The script, screenshots of both routes, and a comparison table.


.. dropdown:: Exercise 4 -- Dynamic Rerouting
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Implement a dynamic rerouting trigger when an obstacle blocks the
   planned path.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``dynamic_reroute.py`` that performs the following:

   1. Plan a route from point A to point B in Town03 using
      ``GlobalRoutePlanner``.
   2. Spawn the ego vehicle and begin following the route.
   3. After the vehicle has traveled **30%** of the route, spawn a
      **static obstacle** (parked vehicle) blocking the planned path.
   4. Implement a rerouting trigger: when the planner detects the
      obstacle is within **20 m** of the planned path, replan from
      the current position to the original destination.
   5. Visualize both routes:

      - Original route: **red** waypoints.
      - New route: **green** waypoints.

   6. Print the **additional distance** caused by the reroute.

   **Deliverable**

   The script and a screenshot showing both routes with the obstacle.


.. dropdown:: Exercise 5 -- RoadOption Sequence Analysis
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Analyze the maneuver complexity of different routes and reason
   about execution difficulty.


   .. raw:: html

      <hr>


   **Specification**

   Use CARLA's ``GlobalRoutePlanner`` to plan **three different routes**
   in Town03 (choose different origin-destination pairs).

   For each route:

   1. Extract the sequence of ``RoadOption`` values.
   2. Count occurrences of each type (``LANEFOLLOW``, ``LEFT``,
      ``RIGHT``, ``STRAIGHT``, ``CHANGELANELEFT``,
      ``CHANGELANERIGHT``).
   3. Compute the **maneuver density**:

      .. math::

         \rho = \frac{\text{non-LANEFOLLOW maneuvers}}
                     {\text{route length (m)}}

   4. If a behavioral planner has a **5% failure rate** per maneuver,
      compute the **probability of completing** each route without a
      failure:

      .. math::

         P_{\text{success}} = (1 - 0.05)^{n_{\text{maneuvers}}}

   5. Which route is simplest? Which is most risky?

   **Deliverable**

   Maneuver count tables, density values, success probabilities, and
   a brief comparison (3--5 sentences).
