====================================================
Lecture
====================================================

.. raw:: latex

   \setcounter{figure}{0}


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

.. dropdown:: Tier Interactions

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

.. dropdown:: Bicycle Model Equations

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

.. dropdown:: Configuration Space

   The vehicle's **configuration** is the tuple
   :math:`q = (x, y, \theta)`. Planning must find a path through
   3-D configuration space :math:`\mathcal{C}` that satisfies the
   nonholonomic constraints and avoids obstacles.

   For parking and low-speed maneuvers, the full nonholonomic
   constraint must be respected. For high-speed highway driving,
   approximate unicycle models are often sufficient because
   lateral slipping is small.


Graph-Based Planning
====================================================

Graph-based planners discretize the environment into a graph and
apply shortest-path search.


Dijkstra's Algorithm
--------------------

.. dropdown:: Algorithm and Complexity

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

.. dropdown:: Heuristic and Optimality

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

.. dropdown:: Weighted A*

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


Sampling-Based Planning
====================================================

Sampling-based planners avoid explicit discretization by randomly
sampling the configuration space.


Rapidly-Exploring Random Trees (RRT)
-------------------------------------

.. dropdown:: RRT Algorithm

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

.. dropdown:: Asymptotic Optimality

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

.. dropdown:: Two-Phase Construction

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


.. dropdown:: State Lattice Construction

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

.. dropdown:: Automotive Lattice Planning

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

      Lattice-based planners are used in production AV systems at
      Waymo and Uber ATG. The Frenet-frame lattice is the dominant
      approach for highway and structured urban driving.


Collision Detection
====================================================

Every candidate path must be checked for collisions before execution.

.. dropdown:: Geometric Methods

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

.. dropdown:: Safety Margins

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

.. dropdown:: Diffusion Models for Planning

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

.. dropdown:: Diffusion Planner (ICLR 2025)

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

.. dropdown:: DiffusionDrive (CVPR 2025)

   **DiffusionDrive** (Liao et al., CVPR 2025) demonstrates
   real-time diffusion planning by:

   - Using a **truncated diffusion schedule** (starting from
     step :math:`T' < T`) to cut denoising steps from 100 to 10.
   - Employing an **anchored Gaussian diffusion** that initializes
     from clustered prior trajectories rather than pure noise.
   - Achieving 45 FPS inference on a single GPU while maintaining
     competitive nuPlan performance.

   .. list-table:: Diffusion Planner Comparison
      :header-rows: 1
      :widths: 30 20 20 30

      * - Method
        - Venue
        - Inference Steps
        - Key Feature
      * - Diffusion Planner
        - ICLR 2025
        - 50
        - Joint ego + agent denoising
      * - DiffusionDrive
        - CVPR 2025
        - 10
        - Truncated + anchored diffusion


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

.. dropdown:: Selection Guidelines

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

         **Recommended:** RRT* (offline) or Hybrid A*

         - No road structure to exploit.
         - Nonholonomic constraints handled by steering primitives.
         - Hybrid A* adds a kinematic-feasible heuristic.

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

   **Starter code:**

   .. code-block:: python

      import carla
      import heapq

      def build_graph(world, sampling_resolution=2.0):
          waypoints = world.get_map().generate_waypoints(sampling_resolution)
          graph = {}
          for wp in waypoints:
              graph[wp.id] = []
              for next_wp in wp.next(sampling_resolution):
                  dist = wp.transform.location.distance(
                      next_wp.transform.location)
                  graph[wp.id].append((next_wp.id, dist, next_wp))
          return graph

      def astar(graph, start_id, goal_loc, waypoint_map):
          def h(wp_id):
              loc = waypoint_map[wp_id].transform.location
              return loc.distance(goal_loc)

          open_set = [(h(start_id), 0.0, start_id, [start_id])]
          visited = set()
          while open_set:
              f, g, current, path = heapq.heappop(open_set)
              if current in visited:
                  continue
              visited.add(current)
              if h(current) < 2.0:   # within 2 m of goal
                  return path
              for neighbor_id, cost, _ in graph.get(current, []):
                  if neighbor_id not in visited:
                      new_g = g + cost
                      heapq.heappush(open_set,
                          (new_g + h(neighbor_id), new_g,
                           neighbor_id, path + [neighbor_id]))
          return None
