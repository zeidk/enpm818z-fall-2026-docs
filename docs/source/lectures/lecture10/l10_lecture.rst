====================================================
Lecture
====================================================

Motion Planning Hierarchy
====================================================

Autonomous vehicle planning is organized into three tiers, each
operating at a different temporal and spatial resolution.

.. list-table:: Planning Hierarchy
   :header-rows: 1
   :widths: 15 20 20 25 20

   * - Tier
     - Name
     - Horizon
     - Output
     - Replanning Rate
   * - 1
     - Route Planning
     - City-scale (km)
     - Sequence of road segments
     - Minutes / on request
   * - 2
     - Behavior Planning
     - Intersection-scale (100 m)
     - Maneuver selection (follow, change lane, yield)
     - 1–10 Hz
   * - 3
     - Motion Planning
     - Local (10–50 m)
     - Collision-free path or trajectory
     - 10–50 Hz

Tier Interactions
-----------------

Each tier produces constraints that narrow the search space of the
tier below it. The route planner selects which roads to traverse;
the behavior planner decides how to interact with other agents at
each road segment; the motion planner finds a geometrically
feasible, collision-free path within the envelope defined by the
behavior decision.

This hierarchical decomposition keeps each planner computationally
tractable. A flat planner operating at city scale with
millimeter-level resolution is computationally infeasible.

.. admonition:: Key Insight
   :class: tip

   The output of tier *n* is the **input constraint** of tier
   *n+1*. Motion planners do not choose which lane to be in;
   behavior planners do not choose which street to take.

Vehicle Kinematic Models
====================================================

A kinematic model captures geometric relationships between vehicle
configuration and velocity without modeling forces.


Bicycle Model
-------------

The **bicycle model** approximates a four-wheeled vehicle by merging
the two front wheels into one steerable wheel and the two rear
wheels into one driven wheel. This yields a tractable model for
planning at low to moderate speeds.

Bicycle Model Equations
~~~~~~~~~~~~~~~~~~~~~~~

Let :math:`(x, y)` be the rear-axle position, :math:`\theta` the
heading, :math:`v` the speed, :math:`\delta` the front-wheel
steering angle, and :math:`L` the wheelbase.

The kinematic equations are:

.. math::

   \dot{x} &= v \cos\theta \\
   \dot{y} &= v \sin\theta \\
   \dot{\theta} &= \frac{v}{L} \tan\delta

The **turning radius** for steering angle :math:`\delta` is:

.. math::

   R = \frac{L}{\tan\delta}

Maximum curvature is bounded by the physical steering limit
:math:`\delta_{\max}`:

.. math::

   \kappa_{\max} = \frac{\tan\delta_{\max}}{L}

.. admonition:: Nonholonomic Constraint
   :class: warning

   The vehicle cannot move sideways. Formally:

   .. math::

      \dot{x}\sin\theta - \dot{y}\cos\theta = 0

   This constraint eliminates lateral translations and
   fundamentally distinguishes vehicle planning from point-robot
   planning.

Configuration Space
~~~~~~~~~~~~~~~~~~~

The vehicle's **configuration** is the tuple
:math:`q = (x, y, \theta)`. Planning must find a path through
3-D configuration space :math:`\mathcal{C}` that satisfies the
nonholonomic constraints and avoids obstacles.

For parking and low-speed maneuvers, the full nonholonomic
constraint must be respected. For high-speed highway driving,
approximate unicycle models are often sufficient because
lateral slipping is small.

The Frenet Frame
~~~~~~~~~~~~~~~~

Structured-road planning is almost never done in Cartesian
:math:`(x, y)`. Instead the road centerline is used as a curved
axis and every pose is expressed in the **Frenet frame**
:math:`(s, d)`:

- :math:`s` -- arc length **along** the reference centerline.
- :math:`d` -- signed lateral offset **perpendicular** to it
  (positive to the left).

Given a centerline point :math:`\mathbf{r}(s)` with unit tangent
:math:`\mathbf{t}(s)` and unit normal :math:`\mathbf{n}(s)`, the
conversion back to Cartesian is:

.. math::

   \mathbf{p}(s, d) = \mathbf{r}(s) + d \, \mathbf{n}(s)

and the heading and curvature transform as:

.. math::

   \theta = \theta_r(s) + \arctan\!\left(\frac{d'}{1 - \kappa_r d}\right),
   \qquad
   \kappa = \frac{\kappa_r}{1 - \kappa_r d} \;+\; \text{(curvature of } d(s))

where :math:`\kappa_r(s)` is the centerline curvature and
:math:`d' = \mathrm{d}d/\mathrm{d}s`.

.. admonition:: Why this matters
   :class: tip

   In Frenet coordinates "stay in the lane" becomes
   :math:`d \approx 0` and "change lanes" becomes a step in
   :math:`d` -- both trivially expressible. Lattice planners
   (below) and the quintic-polynomial planners of **L11** both
   operate in this frame.

   The transform degenerates when :math:`\kappa_r d \to 1`, i.e.
   when the lateral offset reaches the centerline's radius of
   curvature. On tight turns this bounds how far off-centerline
   the frame remains valid.

Graph-Based Planning
====================================================

Graph-based planners discretize the environment into a graph and
apply shortest-path search.


Dijkstra's Algorithm
--------------------

Algorithm and Complexity
~~~~~~~~~~~~~~~~~~~~~~~~

Dijkstra's algorithm finds the shortest path from a source node
to all reachable nodes in a weighted graph with non-negative edge
weights.

**Core steps:**

1. Initialize distance :math:`d[s] = 0`, :math:`d[v] = \infty`
   for all :math:`v \neq s`.
2. Push :math:`(0, s)` onto a min-priority queue.
3. Pop the minimum-cost node :math:`u`. If already visited, skip.
4. For each neighbor :math:`v` of :math:`u`: if
   :math:`d[u] + w(u,v) < d[v]`, update and push
   :math:`(d[u] + w(u,v), v)`.
5. Repeat until the queue is empty or the goal is popped.

**Time complexity:** :math:`O((V + E)\log V)` with a binary heap.

**Completeness:** Yes (finds a path if one exists).

**Optimality:** Yes (with non-negative edge weights).

**Limitation:** Explores in all directions uniformly; slow on
large road networks.

A* Search
---------

Heuristic and Optimality
~~~~~~~~~~~~~~~~~~~~~~~~

A* augments Dijkstra with a **heuristic** :math:`h(v)` that
estimates the cost-to-go from node :math:`v` to the goal.
Nodes are prioritized by:

.. math::

   f(v) = g(v) + h(v)

where :math:`g(v)` is the true cost-to-come and :math:`h(v)` is
the estimated cost-to-go.

**Admissibility:** A heuristic is admissible if it never
overestimates the true cost:

.. math::

   h(v) \leq h^*(v) \quad \forall v

A common admissible heuristic for road networks is the Euclidean
distance to the goal.

**Optimality:** A* with an admissible heuristic always finds the
optimal path.

**Consistency (monotonicity):** :math:`h(u) \leq w(u,v) + h(v)`
for every edge :math:`(u, v)`. Consistent heuristics guarantee
that each node is expanded at most once.

Weighted A*
~~~~~~~~~~~

**Weighted A*** inflates the heuristic by a factor
:math:`\varepsilon > 1`:

.. math::

   f(v) = g(v) + \varepsilon \cdot h(v)

This biases search toward the goal, dramatically reducing the
number of expanded nodes. The solution cost is bounded:

.. math::

   \text{cost}(path) \leq \varepsilon \cdot \text{cost}^*

Weighted A* is the standard choice for real-time motion planning
where a suboptimal but fast solution is preferable to an optimal
but slow one.

.. list-table:: A* Variant Comparison
   :header-rows: 1
   :widths: 30 20 20 30

   * - Variant
     - Optimal
     - Speed
     - Use case
   * - Dijkstra
     - Yes
     - Slow
     - Offline, small graphs
   * - A* (:math:`\varepsilon=1`)
     - Yes
     - Medium
     - Moderate graphs
   * - Weighted A* (:math:`\varepsilon>1`)
     - :math:`\varepsilon`-suboptimal
     - Fast
     - Real-time planning

Hybrid A*
---------

Plain A* on a grid produces paths a car cannot drive: the path can
turn in place and ignores the minimum turning radius. **Hybrid A***
(Dolgov & Thrun, used on Stanford's *Junior* in the DARPA Urban
Challenge) fixes this by searching over **continuous** poses while
using a grid only for bookkeeping.

How Hybrid A\* Differs from Grid A\*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 37 38

   * - Aspect
     - Grid A\*
     - Hybrid A\*
   * - Node
     - Grid cell centre :math:`(i, j)`
     - Continuous pose :math:`(x, y, \theta)`
   * - Expansion
     - 4- or 8-connected neighbours
     - Steering primitives from the bicycle model
   * - Visited set
     - One flag per cell
     - One flag per :math:`(i, j, \theta_{\text{bin}})` cell
   * - Path feasibility
     - Not guaranteed
     - Kinematically feasible by construction

The key trick: each expansion applies a **constant steering angle**
:math:`\delta \in \{-\delta_{\max}, 0, +\delta_{\max}\}` (plus
optional reverse) for a short arc using the bicycle model from
earlier in this lecture. The resulting pose lands *anywhere* in the
cell, not at its centre -- so the stored continuous pose is exact
while the discrete cell prevents infinite re-expansion.

The Two Heuristics
~~~~~~~~~~~~~~~~~~

Hybrid A\* takes the **maximum** of two complementary admissible
heuristics -- each covers the other's blind spot:

1. **Nonholonomic-without-obstacles.** The Reeds-Shepp (or Dubins,
   if reverse is disallowed) distance from the node to the goal,
   ignoring obstacles. Precomputed into a lookup table. This
   captures the turning-radius constraint and guides the final
   approach heading.

2. **Holonomic-with-obstacles.** A 2-D Dijkstra over the obstacle
   grid, ignoring the vehicle's kinematics. This captures dead ends
   and detours that the first heuristic cannot see.

.. math::

   h(n) = \max\big(h_{\text{RS}}(n),\; h_{\text{2D}}(n)\big)

Taking the max preserves admissibility (both underestimate) while
being far tighter than either alone.

Analytic Expansion
~~~~~~~~~~~~~~~~~~

Near the goal, Hybrid A\* periodically attempts a direct
**Reeds-Shepp shot**: an analytically computed
minimum-length curve from the current node straight to the goal
pose. If that curve is collision-free, the search terminates
immediately with an exactly-feasible tail.

This is what makes Hybrid A\* practical -- without it, hitting an
exact goal *heading* by discrete expansion alone is prohibitively
slow.

.. admonition:: Where It Is Used
   :class: tip

   Hybrid A\* is the standard planner for **unstructured**
   environments: parking lots, valet manoeuvres, construction
   detours, and three-point turns. Apollo, Autoware, and most
   production parking stacks ship a variant of it. On structured
   roads the Frenet lattice (below) is preferred because it
   exploits road geometry that Hybrid A\* would have to rediscover.

Sampling-Based Planning
====================================================

Sampling-based planners avoid explicit discretization by randomly
sampling the configuration space.


Rapidly-Exploring Random Trees (RRT)
-------------------------------------

RRT Algorithm
~~~~~~~~~~~~~

RRT incrementally builds a tree rooted at the start configuration
by randomly extending toward sampled configurations.

**Algorithm:**

.. code-block:: text

   T.init(q_start)
   for i = 1 to N:
       q_rand = SAMPLE()           # random config, or goal with prob p_goal
       q_near = NEAREST(T, q_rand) # nearest node in tree
       q_new  = STEER(q_near, q_rand, step_size)
       if COLLISION_FREE(q_near, q_new):
           T.add_vertex(q_new)
           T.add_edge(q_near, q_new)
           if q_new == q_goal:
               return PATH(T, q_start, q_goal)
   return FAILURE

**Properties:**

- **Probabilistically complete:** As :math:`N \to \infty`, the
  probability of finding a path (if one exists) approaches 1.
- **Not optimal:** RRT returns the first path found, which is
  typically far from optimal.
- **Exploration bias:** The Voronoi bias of RRT causes it to
  preferentially expand toward unexplored regions.

RRT*
----

Asymptotic Optimality
~~~~~~~~~~~~~~~~~~~~~

RRT* extends RRT with two additional steps that guarantee
**asymptotic optimality**: the path cost converges to optimal as
the number of samples :math:`N \to \infty`.

**Added steps after adding** :math:`q_{new}`:

1. **Choose parent:** Among all nodes within radius
   :math:`r_n = \gamma(\log N / N)^{1/d}`, select the parent
   that minimizes the cost-to-come to :math:`q_{new}`.

2. **Rewire:** For each neighbor :math:`q_{near}` within
   :math:`r_n`, check if routing through :math:`q_{new}` reduces
   its cost. If so, reassign its parent.

The radius :math:`r_n` shrinks as :math:`N` grows, so the
computational overhead per iteration remains bounded.

.. admonition:: RRT vs RRT* Summary
   :class: note

   RRT finds a feasible path quickly but never improves it.
   RRT* continually refines the path and converges to optimal
   given enough computation time -- making it suitable for offline
   planning or anytime planners.

Probabilistic Road Map (PRM)
-----------------------------

Two-Phase Construction
~~~~~~~~~~~~~~~~~~~~~~

PRM operates in two phases:

**Construction phase:**

1. Sample :math:`N` random configurations in :math:`\mathcal{C}_{free}`.
2. For each sample, attempt to connect it to its :math:`k` nearest
   neighbors using a local planner (usually straight-line).
3. Accept edges where the local plan is collision-free.

**Query phase:**

1. Connect the start and goal to the roadmap.
2. Run A* or Dijkstra on the roadmap graph.

PRM is a **multi-query** planner: the roadmap is built once and
reused for many start/goal pairs. This is useful for
semi-static environments like parking structures.

Lattice-Based Planning
====================================================

Lattice planners discretize the configuration space using a
structured, pre-computed graph called a **state lattice**.


State Lattice Construction
--------------------------

A state lattice is a graph :math:`\mathcal{L} = (V, E)` where:

- **Vertices** :math:`V` correspond to configurations
  :math:`(x, y, \theta, \kappa)` on a regular grid aligned
  with the road.
- **Edges** :math:`E` are pre-computed **motion primitives** --
  short kinematically feasible maneuvers (e.g., 2-second constant-
  curvature arcs) that connect adjacent lattice states.

Motion primitives are computed offline and stored in a lookup
table. At runtime, planning is pure graph search on
:math:`\mathcal{L}`.

Automotive Lattice Planning
---------------------------

In structured road environments:

- The lattice is aligned with the road centerline (Frenet frame).
- Lateral positions correspond to lane positions.
- Longitudinal positions correspond to distance along the road.
- Motion primitives include lane-following arcs, lane-change
  maneuvers, and deceleration profiles.

**Advantages over RRT for roads:**

- Systematic coverage of the reachable space.
- Consistent, predictable maneuver shapes.
- Easy to encode traffic rules as edge costs.
- Real-time performance (graph is pre-built).

.. admonition:: Industrial Use
   :class: tip

   Lattice planners in the Frenet frame are the dominant approach
   for highway and structured urban driving, and appear in Apollo's
   public planning stack and Autoware. The design traces back to the
   DARPA Urban Challenge era (including the former Uber ATG, whose
   technology was acquired by Aurora in 2021).

Collision Detection
====================================================

Every candidate path must be checked for collisions before execution.

Geometric Methods
-----------------

.. list-table:: Collision Detection Representations
   :header-rows: 1
   :widths: 25 30 25 20

   * - Method
     - Description
     - Accuracy
     - Cost
   * - Bounding circle
     - Single circle per object
     - Low
     - O(1)
   * - Axis-aligned bounding box (AABB)
     - Axis-aligned rectangle
     - Medium
     - O(1)
   * - Oriented bounding box (OBB)
     - Rotated rectangle
     - High
     - O(1)
   * - Convex hull
     - Tight convex polygon
     - Very high
     - O(n)
   * - Swept volume
     - Union along path
     - Exact
     - O(path length)

For real-time AV planning, **OBB** representations are the
standard: they are tight enough to avoid false collisions yet
cheap enough to evaluate at 50 Hz.

Safety Margins
--------------

Collision checks use **inflated** obstacle representations.
A margin :math:`d_{\text{safe}}` is added to all obstacle
boundaries before checking:

.. math::

   \mathcal{O}_{\text{inflated}} = \mathcal{O} \oplus
   \mathcal{B}(d_{\text{safe}})

where :math:`\oplus` is the Minkowski sum and
:math:`\mathcal{B}(r)` is a disk of radius :math:`r`.

Typical safety margins:

- Stationary obstacle: 0.3–0.5 m
- Moving vehicle (same direction): 0.5–1.0 m
- Pedestrian: 1.0–1.5 m

Safety margins encode **uncertainty** (localization error,
prediction error) and **comfort** (passengers should not feel
near-miss events).

Diffusion-Based Planning
====================================================

A new class of motion planners formulates path generation as an
iterative **denoising** process learned from expert driving data.

Diffusion Models for Planning
-----------------------------

**Forward process:** Given a ground-truth trajectory
:math:`\tau_0`, add Gaussian noise over :math:`T` steps:

.. math::

   q(\tau_t | \tau_{t-1}) = \mathcal{N}(\tau_t;\,
   \sqrt{1-\beta_t}\,\tau_{t-1},\, \beta_t I)

**Reverse process (planning):** Starting from pure noise
:math:`\tau_T \sim \mathcal{N}(0, I)`, a learned denoising
network :math:`\epsilon_\theta` iteratively removes noise:

.. math::

   p_\theta(\tau_{t-1}|\tau_t) = \mathcal{N}(\tau_{t-1};\,
   \mu_\theta(\tau_t, t),\, \Sigma_\theta(\tau_t, t))

The network :math:`\epsilon_\theta` is conditioned on the
**scene context** (HD map, agent states, ego history) so that
the denoised trajectory is consistent with the current
traffic situation.

Diffusion Planner (ICLR 2025)
-----------------------------

**Diffusion Planner** (Zheng et al., ICLR 2025) is a
diffusion-based closed-loop planner that:

- Encodes the HD map and surrounding agent trajectories using
  a Transformer encoder.
- Runs a DDPM-style denoising process to generate the ego
  trajectory.
- Achieves state-of-the-art closed-loop scores on the nuPlan
  benchmark, outperforming both rule-based and regression-based
  learned planners.

Key design choices:

- **Joint prediction:** ego trajectory and agent trajectories
  are denoised together, enabling interaction-aware planning.
- **Guidance:** traffic rules and comfort metrics can be
  incorporated as classifier guidance during inference.

DiffusionDrive (CVPR 2025)
--------------------------

**DiffusionDrive** (Liao et al., CVPR 2025) demonstrates
real-time diffusion planning by:

- Using a **truncated diffusion schedule** (starting from
  step :math:`T' < T`) to cut the denoising loop to a handful of
  steps rather than the tens-to-hundreds a standard DDPM needs.
- Employing an **anchored Gaussian diffusion** that initializes
  from clustered prior trajectories rather than pure noise.
- Reporting real-time inference (tens of FPS on a single modern
  GPU) on the **NAVSIM** end-to-end planning benchmark.

.. list-table:: Diffusion Planner Comparison
   :header-rows: 1
   :widths: 26 18 26 30

   * - Method
     - Venue
     - Evaluated on
     - Key Feature
   * - Diffusion Planner
     - ICLR 2025
     - nuPlan (closed-loop)
     - Joint ego + agent denoising
   * - DiffusionDrive
     - CVPR 2025
     - NAVSIM / nuScenes
     - Truncated + anchored diffusion

.. warning::

   The two systems are evaluated on **different benchmarks**
   (nuPlan closed-loop vs. NAVSIM), so their headline scores are
   not directly comparable. Always check which benchmark and which
   protocol (open-loop vs. closed-loop) a planning number comes
   from before quoting it. Verify current step counts and FPS
   figures against the published papers -- both move between the
   arXiv and camera-ready versions.

Algorithm Comparison and Selection
====================================================

.. list-table:: Motion Planning Algorithm Summary
   :header-rows: 1
   :widths: 18 12 12 12 22 24

   * - Algorithm
     - Complete
     - Optimal
     - Real-time
     - Best for
     - Limitation
   * - Dijkstra
     - Yes
     - Yes
     - No
     - Small road graphs
     - Exhaustive, slow
   * - A*
     - Yes
     - Yes
     - Marginal
     - Mid-size graphs with good heuristic
     - Needs admissible heuristic
   * - Weighted A*
     - Yes
     - :math:`\varepsilon`-suboptimal
     - Yes
     - Real-time road graphs
     - Solution quality varies with :math:`\varepsilon`
   * - Hybrid A*
     - Yes (in discretization)
     - Near-optimal
     - Yes
     - Parking, unstructured, 3-point turns
     - Needs Reeds-Shepp tables; slower than lattice on roads
   * - RRT
     - Prob.
     - No
     - Yes
     - Unstructured, high-D spaces
     - Suboptimal paths
   * - RRT*
     - Prob.
     - Asymp.
     - No (slow conv.)
     - Offline planning
     - Slow convergence
   * - PRM
     - Prob.
     - Asymp.
     - Yes (query)
     - Semi-static multi-query
     - Construction offline
   * - Lattice
     - Yes (in lattice)
     - Yes (in lattice)
     - Yes
     - Structured roads
     - Requires pre-built primitives
   * - Diffusion
     - --
     - --
     - Yes (DiffusionDrive)
     - Data-rich, complex interactions
     - Requires large training set

Selection Guidelines
--------------------

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: Structured Road (Highway / Urban)
      :class-card: sd-border-primary

      **Recommended:** Lattice-based planner in Frenet frame

      - Pre-built primitives exploit road structure.
      - Efficient graph search at 20–50 Hz.
      - Easy to add traffic rule costs.

   .. grid-item-card:: Unstructured (Parking / Off-Road)
      :class-card: sd-border-primary

      **Recommended:** Hybrid A\* (primary) or RRT\* (offline)

      - No road structure to exploit.
      - Nonholonomic constraints handled by steering primitives.
      - Hybrid A\*'s dual heuristic plus analytic Reeds-Shepp
        expansion gives feasible paths with exact goal headings.

   .. grid-item-card:: Large Road Network Routing
      :class-card: sd-border-primary

      **Recommended:** Dijkstra or A* on road graph

      - Road graph is sparse and small relative to grid.
      - Euclidean heuristic is admissible and tight.

   .. grid-item-card:: Learning-Based (Complex Interactions)
      :class-card: sd-border-primary

      **Recommended:** Diffusion Planner / DiffusionDrive

      - Captures multi-modal human behavior.
      - Handles unstructured interactions not covered by rules.
      - Requires annotated training data.

CARLA Implementation Exercise
====================================================

.. admonition:: Exercise: A* Planner in CARLA
   :class: note

   **Goal:** Implement a graph-based planner that navigates a
   simulated ego vehicle from a start waypoint to a goal waypoint
   in the CARLA Town03 map.

   **Tasks:**

   1. Extract the CARLA waypoint graph using the
      ``carla.Map.generate_waypoints()`` API and build an adjacency
      list with Euclidean edge weights.

   2. Implement A* search with a Euclidean heuristic to find the
      shortest path on the waypoint graph.

   3. Visualize the planned path using CARLA's debug drawing API
      (``world.debug.draw_point()``).

   4. Drive the ego vehicle along the planned path using a
      waypoint-following controller.

   5. **Extension:** Replace the Euclidean heuristic with a
      weighted A* variant (:math:`\varepsilon = 2`) and compare the
      number of nodes expanded vs. plain A*.

   .. warning::

      **CARLA waypoint identity is the trap in this exercise.**
      ``generate_waypoints()`` and ``wp.next()`` return *different
      Waypoint objects* for the same road position, and their ``.id``
      and ``.s`` values will not match. If you key your graph on raw
      ``.id`` or raw ``.s``, ``wp.next()`` will return neighbours that
      are not nodes in your graph and the search will dead-end
      immediately. The starter code below keys on a **quantized**
      ``(road_id, lane_id, s)`` tuple so both APIs agree.

   **Starter code:**

   .. code-block:: python

      import carla
      import heapq

      S_QUANT = 1.0   # metres; must be <= sampling_resolution

      def wp_key(wp):
          """Stable, hashable identity for a CARLA waypoint.

          Quantizing `s` is what makes generate_waypoints() and
          wp.next() agree on node identity.
          """
          return (wp.road_id, wp.lane_id, round(wp.s / S_QUANT))

      def build_graph(world, sampling_resolution=2.0):
          waypoints = world.get_map().generate_waypoints(sampling_resolution)
          waypoint_map = {wp_key(wp): wp for wp in waypoints}
          graph = {k: [] for k in waypoint_map}

          for key, wp in waypoint_map.items():
              for next_wp in wp.next(sampling_resolution):
                  nkey = wp_key(next_wp)
                  if nkey not in waypoint_map:      # off the sampled set
                      continue
                  dist = wp.transform.location.distance(
                      next_wp.transform.location)
                  graph[key].append((nkey, dist))

          n_edges = sum(len(v) for v in graph.values())
          print(f"Graph: {len(graph)} nodes, {n_edges} edges")
          assert n_edges > 0, "No edges built -- check wp_key quantization"
          return graph, waypoint_map

      def astar(graph, waypoint_map, start_key, goal_loc, epsilon=1.0):
          """A* over the waypoint graph. epsilon>1 gives Weighted A*."""
          def h(key):
              return waypoint_map[key].transform.location.distance(goal_loc)

          open_set = [(epsilon * h(start_key), 0.0, start_key)]
          came_from = {}
          g_score = {start_key: 0.0}
          visited = set()
          expanded = 0                      # for the Task 5 comparison

          while open_set:
              _, g, current = heapq.heappop(open_set)
              if current in visited:
                  continue
              visited.add(current)
              expanded += 1

              if h(current) < 2.0:          # within 2 m of goal
                  path = [current]
                  while path[-1] in came_from:
                      path.append(came_from[path[-1]])
                  return path[::-1], expanded

              for nkey, cost in graph.get(current, []):
                  new_g = g + cost
                  if new_g < g_score.get(nkey, float('inf')):
                      g_score[nkey] = new_g
                      came_from[nkey] = current
                      heapq.heappush(
                          open_set, (new_g + epsilon * h(nkey), new_g, nkey))

          return None, expanded

      # Usage
      graph, wp_map = build_graph(world, sampling_resolution=2.0)
      start_key = wp_key(world.get_map().get_waypoint(start_location))
      path, n = astar(graph, wp_map, start_key, goal_location, epsilon=1.0)
      print(f"A*:          {len(path)} waypoints, {n} nodes expanded")
      path_w, n_w = astar(graph, wp_map, start_key, goal_location, epsilon=2.0)
      print(f"Weighted A*: {len(path_w)} waypoints, {n_w} nodes expanded")


Summary
====================================================

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Models and Frames
      :class-card: sd-border-primary

      - Three-tier hierarchy: route (km) -> behavior (100 m) -> motion (10--50 m)
      - Bicycle model: :math:`\dot\theta = (v/L)\tan\delta`,
        :math:`\kappa_{\max} = \tan\delta_{\max}/L`
      - Nonholonomic constraint is what separates cars from point robots
      - Frenet :math:`(s, d)` frame turns "stay in lane" into :math:`d \approx 0`

   .. grid-item-card:: Algorithms
      :class-card: sd-border-primary

      - Dijkstra / A* / Weighted A*: optimal to
        :math:`\varepsilon`-suboptimal, complete
      - Hybrid A*: continuous poses + steering primitives + dual
        heuristic + Reeds-Shepp shot -- the unstructured-space workhorse
      - RRT (feasible fast) vs RRT* (asymptotically optimal, slow)
      - Frenet lattice: pre-built primitives, the structured-road default
      - Diffusion planners: learned denoising, strong on interaction-heavy
        scenes, benchmark-dependent numbers
