====================================================
Lecture
====================================================


The Navigation Problem
-----------------------

Navigation answers the question: **"Which sequence of roads and lanes
should I take to reach my destination?"** This is fundamentally different
from motion planning (L10), which asks *"How do I move safely along this
road segment?"*

.. list-table:: Navigation vs. Motion Planning
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Property
     - Navigation (Route Planning)
     - Motion Planning (L10)
   * - Scale
     - City-wide (km)
     - Local (10--50 m)
   * - Input
     - Road network graph, current position, goal
     - Reference path, obstacles, vehicle dynamics
   * - Output
     - Sequence of road segments / waypoints
     - Collision-free trajectory
   * - Replanning rate
     - On request or every few minutes
     - 10--50 Hz
   * - Algorithm class
     - Graph search (Dijkstra, A*)
     - Sampling, optimization, lattice search
   * - Obstacle awareness
     - Traffic conditions (aggregate)
     - Individual obstacles (precise geometry)


Position in the AV Stack
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ┌──────────────────────────────────────────────────────────┐
   │  L7: Localization           → Where am I?                │
   ├──────────────────────────────────────────────────────────┤
   │  L8: Navigation (this)      → Which roads do I take?     │
   │      Output: ordered list of road segments / waypoints   │
   ├──────────────────────────────────────────────────────────┤
   │  L9: Prediction & Behavior  → What will others do, and   │
   │                               which maneuver do I pick?  │
   ├──────────────────────────────────────────────────────────┤
   │  L10: Motion Planning       → What collision-free path?  │
   ├──────────────────────────────────────────────────────────┤
   │  L11: Trajectory & Control  → Execute the path smoothly  │
   └──────────────────────────────────────────────────────────┘

The route planner produces a **reference route** (sequence of waypoints
or road segments). The behavior planner decides how to handle each
segment (follow lane, change lane, yield). The motion planner generates
a geometrically feasible, collision-free path within those constraints.


Road Network Representation
-----------------------------

Road networks for AV navigation are significantly more detailed than
consumer GPS maps. They encode **lane-level topology**, not just
road-level connectivity.


Graph Structure
~~~~~~~~~~~~~~~~

A road network is modeled as a **directed graph** :math:`G = (V, E)`:

- **Nodes** :math:`V`: Lane-level waypoints at regular intervals
  (e.g., every 2 m). Each node stores position :math:`(x, y, z)`,
  road ID, lane ID, speed limit, and lane width.
- **Edges** :math:`E`: Connections between consecutive waypoints.
  Edges encode whether a transition is a **lane follow**, **lane
  change**, or **junction maneuver**.

.. list-table:: Edge Types
   :widths: 20 30 50
   :header-rows: 1
   :class: compact-table

   * - Type
     - Connectivity
     - Example
   * - Lane follow
     - Same lane, consecutive waypoints
     - Driving straight along a road
   * - Lane change (left)
     - Adjacent lane, same road section
     - Moving to the left lane for overtaking
   * - Lane change (right)
     - Adjacent lane, same road section
     - Moving to the right lane before an exit
   * - Junction
     - Different roads, connected through intersection
     - Turning left at a traffic light


OpenDRIVE Format
~~~~~~~~~~~~~~~~~

CARLA uses the **OpenDRIVE** standard (ISO, adopted by ASAM) to define
road networks. An OpenDRIVE file (``.xodr``) describes:

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **Roads**
     - Defined by a reference line (geometry: line, arc, spiral, cubic)
       with a unique road ID.
   * - **Lanes**
     - Organized in lane sections along each road. Each lane has an ID,
       type (driving, shoulder, sidewalk), width, and speed limit.
   * - **Junctions**
     - Connect roads at intersections. Define which incoming lanes can
       connect to which outgoing lanes (connection elements).
   * - **Signals**
     - Traffic lights, stop signs, speed limit signs with position and
       orientation relative to the road.
   * - **Objects**
     - Static objects like barriers, poles, and crosswalks.

.. code-block:: python

   # Access CARLA's OpenDRIVE data
   import carla

   client = carla.Client('localhost', 2000)
   world = client.get_world()
   carla_map = world.get_map()

   # Get the raw OpenDRIVE XML
   opendrive_xml = carla_map.to_opendrive()
   print(f"OpenDRIVE data: {len(opendrive_xml)} characters")

   # Get topology: list of (waypoint, waypoint) pairs
   # representing road segment start-end connections
   topology = carla_map.get_topology()
   print(f"Topology: {len(topology)} road segments")


Lanelet2 Format
~~~~~~~~~~~~~~~~

**Lanelet2** is the map format used by Autoware and many research
platforms. It differs from OpenDRIVE in its representation:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Feature
     - OpenDRIVE
     - Lanelet2
   * - Geometry
     - Parametric curves (arcs, spirals)
     - Polylines (left/right boundary points)
   * - Lane representation
     - Offset from road reference line
     - Bounded region between two linestrings
   * - Traffic rules
     - Signal elements attached to roads
     - Regulatory elements attached to lanelets
   * - Primary users
     - CARLA, SUMO, dSPACE
     - Autoware, many research platforms
   * - File format
     - XML (.xodr)
     - OSM-based XML (.osm)


HD Maps for Navigation
~~~~~~~~~~~~~~~~~~~~~~~

High-Definition maps go beyond basic road geometry to encode rich
semantic information used by the navigation and planning stack:

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Geometry
      :class-card: sd-border-info

      - Lane boundaries with centimeter accuracy
      - Road elevation profile
      - Curvature at every point
      - Intersection geometry

   .. grid-item-card:: Topology
      :class-card: sd-border-info

      - Lane-level connectivity graph
      - Lane change permissions (solid vs. dashed lines)
      - Merge/diverge points
      - Turn restrictions

   .. grid-item-card:: Semantics
      :class-card: sd-border-info

      - Speed limits per lane segment
      - Traffic light positions and associations
      - Stop/yield sign locations
      - Crosswalk boundaries

.. admonition:: HD Map Limitations
   :class: warning

   HD maps are expensive to create ($5K--$50K per km), require
   continuous maintenance, and limit the ODD to mapped areas. The
   industry trend is toward lighter maps supplemented by stronger
   online perception (Tesla, Mobileye REM).


Global Route Planning
----------------------

Given the road network graph, a start position, and a goal position,
the route planner finds the optimal sequence of road segments to
traverse.


Cost Functions for Road Networks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unlike grid-based planning, road network edges carry rich cost
information:

.. math::

   \text{cost}(e) = w_d \cdot d(e) + w_t \cdot t(e) + w_r \cdot r(e)
                    + w_c \cdot c(e) + w_m \cdot m(e)

.. list-table::
   :widths: 15 25 60
   :header-rows: 1
   :class: compact-table

   * - Term
     - Component
     - Description
   * - :math:`d(e)`
     - Distance
     - Physical length of the road segment (meters).
   * - :math:`t(e)`
     - Travel time
     - Segment length / speed limit. Accounts for faster highways vs.
       slower urban roads.
   * - :math:`r(e)`
     - Road class
     - Penalty for road types: prefer highways over residential streets
       for long routes, or vice versa in urban settings.
   * - :math:`c(e)`
     - Comfort
     - Penalty for sharp turns, steep grades, or frequent lane changes.
   * - :math:`m(e)`
     - Maneuver complexity
     - Penalty for unprotected left turns, complex merges, or high-risk
       intersections.

.. tip::

   By adjusting the weights :math:`w_d, w_t, w_r, w_c, w_m`, the same
   algorithm can produce shortest-distance, fastest-time, or
   safest/most-comfortable routes.


Dijkstra's Algorithm on Road Graphs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dijkstra's algorithm finds the shortest path from a start node to all
other nodes in a weighted graph with non-negative edge costs.

.. code-block:: python

   import heapq

   def dijkstra(graph, start_id, goal_id):
       """
       Find shortest path on a road network graph.

       Args:
           graph: dict of {node_id: [(neighbor_id, cost), ...]}
           start_id: starting waypoint ID
           goal_id: goal waypoint ID

       Returns:
           path: list of waypoint keys from start to goal
           total_cost: total path cost
           expanded: number of nodes expanded (for comparison with A*)
       """
       dist = {start_id: 0.0}
       prev = {}
       pq = [(0.0, start_id)]
       expanded = 0

       while pq:
           d, u = heapq.heappop(pq)
           if u == goal_id:
               break
           if d > dist.get(u, float('inf')):
               continue
           expanded += 1
           for v, cost in graph.get(u, []):     # .get: u may be a dead end
               new_dist = d + cost
               if new_dist < dist.get(v, float('inf')):
                   dist[v] = new_dist
                   prev[v] = u
                   heapq.heappush(pq, (new_dist, v))

       # Reconstruct path
       path = []
       node = goal_id
       while node in prev:
           path.append(node)
           node = prev[node]
       path.append(start_id)
       return path[::-1], dist.get(goal_id, float('inf')), expanded

**Complexity:** :math:`O((|V| + |E|) \log |V|)` with a binary heap.
Road networks are sparse (:math:`|E| \approx 3|V|`), so this is
efficient even for city-scale graphs.


A* with Road Network Heuristics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A* improves on Dijkstra by using a heuristic to guide the search
toward the goal:

.. math::

   f(n) = g(n) + h(n)

For road networks, the **Euclidean distance** to the goal divided by
the maximum speed limit is an admissible heuristic for travel-time
optimization:

.. math::

   h(n) = \frac{\| \text{pos}(n) - \text{pos}(\text{goal}) \|_2}{v_{\max}}

.. code-block:: python

   import numpy as np

   def astar_road(graph, start_id, goal_id, positions, v_max=None):
       """A* search on a road network graph.

       The heuristic MUST be in the same units as the edge costs, or it
       is not admissible and A* loses its optimality guarantee:

         * edge cost = distance (m)  ->  h = Euclidean distance (m)
         * edge cost = time (s)      ->  h = distance / v_max (s)

       Pass v_max (in m/s) for a time-weighted graph; leave it None for
       a distance-weighted one.
       """

       def heuristic(node_id):
           d = np.linalg.norm(positions[node_id] - positions[goal_id])
           return d / v_max if v_max else d

       dist = {start_id: 0.0}
       prev = {}
       pq = [(heuristic(start_id), 0.0, start_id)]
       expanded = 0

       while pq:
           _, g, u = heapq.heappop(pq)
           if u == goal_id:
               break
           if g > dist.get(u, float('inf')):
               continue
           expanded += 1
           for v, cost in graph.get(u, []):
               new_g = g + cost
               if new_g < dist.get(v, float('inf')):
                   dist[v] = new_g
                   prev[v] = u
                   f = new_g + heuristic(v)
                   heapq.heappush(pq, (f, new_g, v))

       path = []
       node = goal_id
       while node in prev:
           path.append(node)
           node = prev[node]
       path.append(start_id)
       return path[::-1], dist.get(goal_id, float('inf')), expanded

.. note::

   For very large road networks (city/country scale), algorithms like
   **Contraction Hierarchies** and **Hub Labeling** preprocess the graph
   to answer queries in microseconds. These are used by Google Maps and
   OSRM but are beyond the scope of this course.


Lane-Level Routing
-------------------

Global route planning on road segments answers *which roads to take*.
**Lane-level routing** answers *which lane to be in* on each road
segment.

Lane Selection Strategy
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Scenario
     - Lane Selection Rule
   * - Approaching a right turn
     - Transition to rightmost lane at least 200 m before the turn.
   * - Approaching a left turn
     - Transition to leftmost lane at least 200 m before the turn.
   * - Highway cruising
     - Prefer the rightmost non-exit lane. Move left to overtake.
   * - Highway exit
     - Transition to exit lane at least 500 m before the diverge point.
   * - Merge
     - Target the merge lane, matching speed of traffic flow.
   * - Construction zone
     - Follow lane closure signs; merge early (zipper merge).

.. admonition:: Lane Change Planning
   :class: tip

   Lane changes are not instantaneous -- they require gap finding in the
   target lane, a safe trajectory, and coordination with the behavior
   planner. The navigation layer determines *when* a lane change is
   needed; the behavior planner decides *whether it is safe to execute
   now*; the motion planner generates the *trajectory*.


Dynamic Rerouting
~~~~~~~~~~~~~~~~~~

Static routes computed at trip start may become invalid due to:

- **Road closures** -- Construction, accidents, police activity.
- **Traffic congestion** -- Travel time on the current route exceeds
  alternatives.
- **Mission changes** -- New destination or waypoint added.
- **Sensor-detected obstacles** -- Blocked road not in the map.

**Rerouting strategy:**

1. Monitor route cost continuously using real-time traffic data or
   perception-detected blockages.
2. If the estimated remaining cost exceeds a threshold (e.g., 1.5x the
   alternative route cost), trigger replanning.
3. Rerun A* from the current position to the goal on the updated graph.
4. Smoothly transition to the new route at the next intersection.

.. important::

   Rerouting must be seamless -- the vehicle cannot stop in the middle
   of a highway to recompute. The new route must be ready before the
   last decision point where the old and new routes diverge.


CARLA Navigation API
---------------------

CARLA provides a complete navigation stack through its Python API. The
key component is the ``GlobalRoutePlanner``.


GlobalRoutePlanner
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import carla
   from agents.navigation.global_route_planner import GlobalRoutePlanner

   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   world = client.get_world()
   carla_map = world.get_map()

   # ── Initialize the GlobalRoutePlanner ─────────────────────────────
   sampling_resolution = 2.0  # meters between waypoints
   grp = GlobalRoutePlanner(carla_map, sampling_resolution)

   # ── Define start and goal ─────────────────────────────────────────
   spawn_points = carla_map.get_spawn_points()
   start = spawn_points[0].location
   goal = spawn_points[50].location

   # ── Compute the route ─────────────────────────────────────────────
   route = grp.trace_route(start, goal)
   print(f"Route: {len(route)} waypoints")

   # Each element is a (waypoint, road_option) tuple
   for i, (wp, option) in enumerate(route[:10]):
       print(f"  [{i}] pos=({wp.transform.location.x:.1f}, "
             f"{wp.transform.location.y:.1f}) "
             f"road={wp.road_id} lane={wp.lane_id} "
             f"option={option}")


Road Options
~~~~~~~~~~~~~

The ``GlobalRoutePlanner`` annotates each waypoint with a
``RoadOption`` indicating the maneuver type:

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - RoadOption
     - Meaning
   * - ``LANEFOLLOW``
     - Continue in the current lane.
   * - ``LEFT``
     - Turn left at a junction.
   * - ``RIGHT``
     - Turn right at a junction.
   * - ``STRAIGHT``
     - Go straight through a junction.
   * - ``CHANGELANELEFT``
     - Change to the left lane.
   * - ``CHANGELANERIGHT``
     - Change to the right lane.
   * - ``VOID``
     - Unclassified (e.g., roundabout entry).

These annotations are critical for the behavior planner -- they tell
it *what kind of maneuver* is coming up so it can prepare (e.g., slow
down before a turn, check blind spot before a lane change).


Visualizing Routes in CARLA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np

   def draw_route(world, route, life_time=60.0):
       """Draw the planned route as colored waypoints in CARLA."""
       color_map = {
           'LANEFOLLOW':      carla.Color(0, 255, 0),     # green
           'LEFT':            carla.Color(255, 0, 0),     # red
           'RIGHT':           carla.Color(0, 0, 255),     # blue
           'STRAIGHT':        carla.Color(255, 255, 0),   # yellow
           'CHANGELANELEFT':  carla.Color(255, 128, 0),   # orange
           'CHANGELANERIGHT': carla.Color(128, 0, 255),   # purple
       }

       for wp, option in route:
           color = color_map.get(option.name, carla.Color(128, 128, 128))
           world.debug.draw_point(
               wp.transform.location + carla.Location(z=0.5),
               size=0.1,
               color=color,
               life_time=life_time)

       # Draw start and goal markers
       start_loc = route[0][0].transform.location + carla.Location(z=1.0)
       goal_loc = route[-1][0].transform.location + carla.Location(z=1.0)
       world.debug.draw_string(start_loc, "START", color=carla.Color(0,255,0))
       world.debug.draw_string(goal_loc, "GOAL", color=carla.Color(255,0,0))

   draw_route(world, route)


Building a Custom Road Graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For custom cost functions or research purposes, you can build your own
graph from CARLA's waypoint API:

.. code-block:: python

   S_QUANT = 1.0    # metres; must be <= resolution

   def wp_key(wp):
       """Stable, hashable identity for a CARLA waypoint.

       CRITICAL: `wp.s` is a float, and generate_waypoints() and
       wp.next() do NOT return bit-identical values for the same road
       position. Keying on the raw float makes every
       `next_key in waypoint_map` test fail, so the graph ends up with
       zero edges -- a silent failure that later looks like
       "no route found".

       Quantizing `s` to a coarse grid makes both APIs agree.
       """
       return (wp.road_id, wp.section_id, wp.lane_id,
               int(round(wp.s / S_QUANT)))

   def build_road_graph(carla_map, resolution=2.0, lane_change_penalty=5.0):
       """
       Build a road network graph from CARLA waypoints.

       Returns:
           graph: dict {wp_key: [(neighbor_key, cost), ...]}
           waypoint_map: dict {wp_key: carla.Waypoint}
       """
       waypoints = carla_map.generate_waypoints(resolution)
       waypoint_map = {wp_key(wp): wp for wp in waypoints}
       graph = {k: [] for k in waypoint_map}

       for key, wp in waypoint_map.items():
           # Lane follow: next waypoints along the lane
           for next_wp in wp.next(resolution):
               nkey = wp_key(next_wp)
               if nkey in waypoint_map:
                   dist = wp.transform.location.distance(
                       next_wp.transform.location)
                   graph[key].append((nkey, dist))

           # Lane changes (if permitted)
           left_wp = wp.get_left_lane()
           if (left_wp is not None and
                   left_wp.lane_type == carla.LaneType.Driving and
                   str(wp.lane_change) in ['Left', 'Both']):
               lkey = wp_key(left_wp)
               if lkey in waypoint_map:
                   # Lane change cost = distance + penalty
                   dist = wp.transform.location.distance(
                       left_wp.transform.location)
                   graph[key].append((lkey, dist + lane_change_penalty))

           right_wp = wp.get_right_lane()
           if (right_wp is not None and
                   right_wp.lane_type == carla.LaneType.Driving and
                   str(wp.lane_change) in ['Right', 'Both']):
               rkey = wp_key(right_wp)
               if rkey in waypoint_map:
                   dist = wp.transform.location.distance(
                       right_wp.transform.location)
                   graph[key].append((rkey, dist + lane_change_penalty))

       return graph, waypoint_map

   graph, wp_map = build_road_graph(carla_map, resolution=2.0)
   n_edges = sum(len(v) for v in graph.values())
   print(f"Graph: {len(graph)} nodes, {n_edges} edges")

   # Fail loudly now rather than "finding no route" ten minutes later
   assert n_edges > 0, (
       "No edges built. Check that S_QUANT <= resolution and that "
       "wp_key() quantizes `s` instead of using the raw float.")


From Route to Reference Path
------------------------------

The global route is a sequence of discrete waypoints. Before the motion
planner (L10) can use it, the route must be converted into a smooth
**reference path** with associated metadata.


Waypoint-to-Path Conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   DEFAULT_SPEED_KMH = 30.0

   def route_to_reference_path(route):
       """
       Convert a CARLA route to a reference path for the motion planner.

       Returns:
           path: np.array of shape (N, 6) -- [x, y, z, yaw, speed_limit, curvature]
       """
       path = []
       for i, (wp, option) in enumerate(route):
           loc = wp.transform.location
           rot = wp.transform.rotation
           yaw = np.radians(rot.yaw)

           # Speed limit, in m/s. CARLA exposes posted limits as
           # landmarks attached to the road; fall back to a default when
           # a segment has no sign.
           speed_limit = DEFAULT_SPEED_KMH / 3.6
           landmarks = wp.get_landmarks_of_type(
               50.0, '274')          # OpenDRIVE type 274 = speed limit
           if landmarks:
               speed_limit = landmarks[0].value / 3.6

           # Estimate curvature from consecutive waypoints
           if 0 < i < len(route) - 1:
               p0 = np.array([route[i-1][0].transform.location.x,
                              route[i-1][0].transform.location.y])
               p1 = np.array([loc.x, loc.y])
               p2 = np.array([route[i+1][0].transform.location.x,
                              route[i+1][0].transform.location.y])
               # Menger curvature from three points.
               # NOTE: np.cross on 2-D vectors is REMOVED in NumPy 2.0 --
               # compute the scalar cross product explicitly.
               v1, v2 = p1 - p0, p2 - p0
               cross_z = v1[0] * v2[1] - v1[1] * v2[0]
               a = np.linalg.norm(p1 - p0)
               b = np.linalg.norm(p2 - p1)
               c = np.linalg.norm(p2 - p0)
               area = abs(cross_z) / 2.0
               curvature = 4.0 * area / max(a * b * c, 1e-6)
           else:
               curvature = 0.0

           path.append([loc.x, loc.y, loc.z, yaw, speed_limit, curvature])

       return np.array(path)


Speed Profile Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~

The reference path needs a **speed profile** that respects speed limits,
curvature constraints, and comfort requirements:

.. math::

   v_{\max}(s) = \min\left(
       v_{\text{limit}}(s), \;
       \sqrt{\frac{a_{\text{lat,max}}}{\kappa(s)}}, \;
       v_{\text{comfort}}
   \right)

where:

- :math:`v_{\text{limit}}(s)` is the posted speed limit at arc-length
  :math:`s`.
- :math:`\kappa(s)` is the curvature, and :math:`a_{\text{lat,max}}` is
  the maximum comfortable lateral acceleration (typically 2--3 m/s²).
- :math:`v_{\text{comfort}}` is a global comfort cap.

.. code-block:: python

   def generate_speed_profile(path, a_lat_max=2.5, v_comfort=15.0):
       """Generate a speed profile respecting curvature and speed limits."""
       speeds = np.zeros(len(path))
       for i in range(len(path)):
           v_limit = path[i, 4]
           kappa = abs(path[i, 5])
           v_curvature = np.sqrt(a_lat_max / max(kappa, 1e-4))
           speeds[i] = min(v_limit, v_curvature, v_comfort)
       return speeds


CARLA Hands-On: Plan and Execute a Multi-Kilometer Route
----------------------------------------------------------


Task 1: Compute and Visualize a Global Route
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import carla
   import numpy as np
   from agents.navigation.global_route_planner import GlobalRoutePlanner

   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)

   # Load Town03 (urban grid with intersections)
   world = client.load_world('Town03')
   carla_map = world.get_map()

   # Set up route planner
   grp = GlobalRoutePlanner(carla_map, sampling_resolution=2.0)

   # Plan a long route across the town
   spawn_points = carla_map.get_spawn_points()
   start = spawn_points[0].location
   goal = spawn_points[100].location

   route = grp.trace_route(start, goal)
   print(f"Planned route: {len(route)} waypoints")

   # Count maneuver types
   from collections import Counter
   maneuvers = Counter(option.name for _, option in route)
   print(f"Maneuvers: {dict(maneuvers)}")

   # Visualize
   draw_route(world, route, life_time=120.0)


Task 2: Build a Road Graph and Compare Routes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Build the road graph
   graph, wp_map = build_road_graph(carla_map, resolution=2.0)
   print(f"Road graph: {len(graph)} nodes")

   # Find nearest waypoints to start and goal
   def find_nearest_wp(wp_map, location):
       min_dist = float('inf')
       nearest_id = None
       for wp_id, wp in wp_map.items():
           dist = wp.transform.location.distance(location)
           if dist < min_dist:
               min_dist = dist
               nearest_id = wp_id
       return nearest_id

   start_id = find_nearest_wp(wp_map, start)
   goal_id = find_nearest_wp(wp_map, goal)

   # --- Dijkstra vs A* on the SAME distance-weighted graph ---
   # Both are optimal, so they return the same-cost path. What differs
   # is HOW MUCH OF THE GRAPH each had to explore. That is the point of
   # the comparison -- not the route.
   path_d, cost_d, expanded_d = dijkstra(graph, start_id, goal_id)
   print(f"Dijkstra: {len(path_d)} wp, cost={cost_d:.1f}, "
         f"expanded={expanded_d}")

   positions = {k: np.array([wp.transform.location.x,
                             wp.transform.location.y])
                for k, wp in wp_map.items()}

   path_a, cost_a, expanded_a = astar_road(graph, start_id, goal_id,
                                           positions)
   print(f"A*:       {len(path_a)} wp, cost={cost_a:.1f}, "
         f"expanded={expanded_a}")
   print(f"A* explored {100 * expanded_a / expanded_d:.0f}% "
         f"as many nodes as Dijkstra")

   # --- Now a genuinely different objective: fastest TIME ---
   # To compare shortest-distance against fastest-time you must change
   # the EDGE COSTS, not just the search algorithm. Rebuild the graph
   # with cost = length / speed_limit and re-run.
   def to_time_graph(graph, wp_map, default_kmh=30.0):
       tgraph = {}
       for key, edges in graph.items():
           tgraph[key] = []
           for nkey, dist in edges:
               v = default_kmh / 3.6            # m/s; use posted limit
               tgraph[key].append((nkey, dist / v))
       return tgraph

   time_graph = to_time_graph(graph, wp_map)
   path_t, cost_t, _ = astar_road(time_graph, start_id, goal_id,
                                  positions, v_max=50.0 / 3.6)
   print(f"Fastest-time route: {len(path_t)} wp, {cost_t:.1f} s")


Task 3: Route-Following Autonomous Agent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time

   # Spawn ego vehicle at the route start
   vehicle_bp = world.get_blueprint_library().find('vehicle.tesla.model3')
   vehicle = world.spawn_actor(vehicle_bp, spawn_points[0])

   # Simple waypoint-following controller
   def follow_route(vehicle, route, target_speed_kmh=30,
                    reach_radius=3.0, timeout_per_wp=15.0, dt=0.05):
       """Follow a route using basic waypoint steering.

       Control is recomputed EVERY tick, not once per waypoint. The
       naive version -- apply a control, then busy-wait until the
       waypoint is reached -- drives open-loop with a frozen steering
       angle, and hangs forever if the vehicle never arrives.
       """
       for i, (wp, option) in enumerate(route):
           target = wp.transform.location
           elapsed = 0.0

           while True:
               tf = vehicle.get_transform()
               v_loc = tf.location

               if v_loc.distance(target) <= reach_radius:
                   break                       # waypoint reached

               if elapsed > timeout_per_wp:
                   print(f"  [WARN] Waypoint {i} unreachable after "
                         f"{timeout_per_wp:.0f}s -- skipping. The vehicle "
                         f"is likely stuck or the route is infeasible.")
                   break                       # give up, do not hang

               # --- Recompute steering toward the target every tick ---
               v_fwd = tf.get_forward_vector()
               dx = target.x - v_loc.x
               dy = target.y - v_loc.y
               dot = v_fwd.x * dx + v_fwd.y * dy
               cross = v_fwd.x * dy - v_fwd.y * dx

               # Angle to target is better behaved than cross/dot, which
               # blows up when the target is beside or behind the car.
               angle = np.arctan2(cross, dot)
               steer = float(np.clip(angle / np.radians(45.0), -1.0, 1.0))

               # --- Speed control ---
               velocity = vehicle.get_velocity()
               speed = 3.6 * np.sqrt(velocity.x**2 + velocity.y**2)
               throttle = 0.5 if speed < target_speed_kmh else 0.0
               brake = 0.3 if speed > target_speed_kmh + 10 else 0.0

               vehicle.apply_control(carla.VehicleControl(
                   throttle=throttle, steer=steer, brake=brake))

               time.sleep(dt)
               elapsed += dt

           if i % 20 == 0:
               print(f"  Waypoint {i}/{len(route)}: option={option.name}")

       vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))

   print("Following route...")
   follow_route(vehicle, route, target_speed_kmh=30)
   print("Route complete!")

.. admonition:: Exercise Tasks
   :class: tip

   1. **Plan and visualize** a route through Town03 using the
      ``GlobalRoutePlanner``. Count the number of left turns, right turns,
      lane follows, and lane changes.
   2. **Build a custom road graph** and run Dijkstra and A* on the
      *same* distance-weighted graph. Both are optimal, so they return
      the same-cost route -- compare the **number of nodes expanded**
      instead. Then rebuild the graph with time-based edge costs and
      confirm that the fastest-time route can differ from the
      shortest-distance one.
   3. **Modify the cost function** to penalize left turns (add +10 to
      junction edges that involve left turns). How does the route change?
   4. **Implement the route-following controller** and drive the full route
      autonomously. Measure route completion percentage and average speed.
   5. **Dynamic rerouting**: Place a static obstacle (``world.spawn_actor``
      with a barrier blueprint) on the planned route. Detect when the
      vehicle cannot proceed and replan from the current position.
   6. **Multi-town comparison**: Plan routes in Town01, Town03, and Town04.
      Compare graph sizes, route lengths, and maneuver distributions.

.. note::

   The waypoint-following controller in Task 3 is intentionally simple.
   In **L10: Motion Planning** and **L11: Trajectory Generation &
   Control**, you will replace it with proper path planners and
   controllers (A*, Hybrid A*, Pure Pursuit, Stanley, MPC) that handle
   obstacles and dynamics.


Summary
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Road Network
      :class-card: sd-border-primary

      - Lane-level directed graph with typed edges (follow, change, junction)
      - OpenDRIVE (CARLA) and Lanelet2 (Autoware) map formats
      - HD maps encode geometry, topology, and semantics

   .. grid-item-card:: Route Planning
      :class-card: sd-border-primary

      - Dijkstra / A* on road graphs with multi-objective cost functions
      - Lane-level routing for turn preparation and highway exits
      - Dynamic rerouting for closures and congestion

   .. grid-item-card:: CARLA Navigation
      :class-card: sd-border-primary

      - GlobalRoutePlanner: trace_route() with RoadOption annotations
      - Custom graph building from waypoint API
      - Route-to-reference-path conversion for downstream planners

.. note::

   Navigation is the *strategic* layer of the planning stack. It tells
   the vehicle where to go. The *tactical* (behavior, L9) and
   *operational* (motion planning L10, trajectory and control L11)
   layers determine how to get there safely and smoothly.
