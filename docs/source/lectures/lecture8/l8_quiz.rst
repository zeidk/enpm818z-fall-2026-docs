====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 8: Navigation & Route
Planning. Topics include the navigation vs. motion planning distinction,
road network graph representation, OpenDRIVE and Lanelet2 map formats,
HD maps, multi-objective cost functions, Dijkstra and A* on road graphs,
lane-level routing, dynamic rerouting, CARLA's GlobalRoutePlanner, and
route-to-reference-path conversion.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-10)
=================================

.. admonition:: Question 1
   :class: hint

   What is the key difference between navigation (route planning) and
   motion planning?

   A. Navigation uses neural networks; motion planning uses classical algorithms.
   B. Navigation operates at the city scale on road graphs; motion planning
      operates at the local scale on continuous space.
   C. Navigation considers obstacles; motion planning does not.
   D. Navigation runs at 50 Hz; motion planning runs once per trip.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   Navigation operates at the city scale, finding the optimal sequence of
   road segments on a road network graph (km scale, replanned every few
   minutes or on request). Motion planning operates at the local scale
   (10--50 m) in continuous space, producing a collision-free trajectory
   at 10--50 Hz. Option C is backwards: motion planning is precisely the
   layer that reasons about individual obstacle geometry, while navigation
   sees only aggregate traffic conditions.


.. admonition:: Question 2
   :class: hint

   In a lane-level road network graph, which of the following is **not**
   a standard edge type?

   A. Lane follow
   B. Lane change (left/right)
   C. Junction maneuver
   D. Obstacle avoidance

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**

   Edges encode topological connectivity: continuing along a lane,
   transitioning to an adjacent lane, or traversing an intersection.
   Obstacle avoidance is not a topological property of the map -- it is a
   runtime decision made by the motion planner (L10) against perceived
   obstacles, which are not in the map at all.


.. admonition:: Question 3
   :class: hint

   Which statement correctly describes the difference between OpenDRIVE
   and Lanelet2 geometry representation?

   A. OpenDRIVE uses polylines; Lanelet2 uses parametric curves.
   B. OpenDRIVE uses parametric curves (lines, arcs, spirals) with lanes
      defined as offsets from a road reference line; Lanelet2 uses
      polylines defining left and right lane boundaries.
   C. Both use identical geometry; they differ only in file extension.
   D. OpenDRIVE stores geometry as a raster occupancy grid.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   OpenDRIVE (``.xodr``, used by CARLA and SUMO) describes each road by a
   reference line built from analytic primitives -- straight lines, arcs,
   and spirals (clothoids) -- with lanes specified as width offsets from
   that line. Lanelet2 (OSM-based ``.osm``, used by Autoware) instead
   represents a lanelet as the region bounded by two explicit linestrings.
   The practical consequence: OpenDRIVE gives exact curvature analytically,
   while Lanelet2 is simpler to edit and query but must approximate
   curvature from discrete points.


.. admonition:: Question 4
   :class: hint

   A route planner uses the cost function
   :math:`\text{cost}(e) = w_d d(e) + w_t t(e) + w_r r(e) + w_c c(e) + w_m m(e)`.
   To produce the **fastest** route rather than the shortest, you should:

   A. Increase :math:`w_d` and set all other weights to zero.
   B. Increase :math:`w_t` relative to :math:`w_d`, since
      :math:`t(e)` = segment length / speed limit.
   C. Increase :math:`w_m` to penalize complex maneuvers.
   D. Switch from A* to Dijkstra.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   The travel-time term :math:`t(e)` divides segment length by the speed
   limit, so weighting it favors highways over shorter but slower surface
   streets. Option D is a category error: Dijkstra and A* are *search
   algorithms* that both return the optimal path for whatever cost
   function they are given -- changing the algorithm cannot change the
   objective.


.. admonition:: Question 5
   :class: hint

   What is the time complexity of Dijkstra's algorithm with a binary heap,
   and why is it tractable on city-scale road networks?

   A. :math:`O(V^2)`; road graphs are small.
   B. :math:`O((V + E)\log V)`; road networks are sparse, with
      :math:`|E| \approx 3|V|`.
   C. :math:`O(V!)`; tractable only with pruning.
   D. :math:`O(E \log E)`; road networks are dense.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   With a binary heap, Dijkstra runs in :math:`O((V + E)\log V)`. Road
   networks are **sparse** -- each intersection connects to only a handful
   of others, giving :math:`|E| \approx 3|V|` -- so the term is effectively
   :math:`O(V \log V)`. This is why city-scale routing is feasible without
   specialized preprocessing.


.. admonition:: Question 6
   :class: hint

   For a road graph whose edge costs are **travel times**, which heuristic
   is admissible for A*?

   A. :math:`h(n) = 0` for all nodes.
   B. :math:`h(n) = \|\text{pos}(n) - \text{pos}(\text{goal})\|_2 / v_{\max}`
   C. :math:`h(n) = \|\text{pos}(n) - \text{pos}(\text{goal})\|_2`
   D. :math:`h(n) = \|\text{pos}(n) - \text{pos}(\text{goal})\|_2 \times v_{\max}`

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   The heuristic must be in the **same units as the edge costs** (seconds)
   and must never overestimate. Dividing straight-line distance by the
   maximum speed limit gives the shortest conceivable travel time, which
   is admissible. Option C returns metres and is dimensionally
   inconsistent with a time-weighted graph. Option A is technically
   admissible but reduces A* to Dijkstra.


.. admonition:: Question 7
   :class: hint

   In CARLA, ``GlobalRoutePlanner.trace_route()`` returns a list of:

   A. ``carla.Location`` objects only.
   B. ``(waypoint, RoadOption)`` tuples, where ``RoadOption`` annotates the
      maneuver type.
   C. Raw OpenDRIVE XML strings.
   D. A single smoothed spline.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   Each element pairs a ``carla.Waypoint`` with a ``RoadOption``
   (``LANEFOLLOW``, ``LEFT``, ``RIGHT``, ``STRAIGHT``, ``CHANGELANELEFT``,
   ``CHANGELANERIGHT``, ``VOID``). The annotation is what lets the behavior
   planner prepare for an upcoming maneuver -- slowing before a turn, or
   checking the blind spot before a lane change.


.. admonition:: Question 8
   :class: hint

   A vehicle must exit the highway in 400 m but is in the leftmost of four
   lanes. Which lane-level routing behavior is correct?

   A. Wait until 50 m before the exit, then change all three lanes at once.
   B. Begin transitioning right immediately, allowing one lane change at a
      time with adequate gaps; if the exit becomes unreachable, reroute.
   C. Stop on the highway and wait for a gap.
   D. Ignore the exit and let the motion planner handle it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   Lane changes take time and require gap acceptance in the target lane,
   so the navigation layer must signal the need for a lane change with
   substantial lead distance -- typically 500 m before a highway diverge.
   Critically, the system must also be willing to **miss the exit and
   reroute**: forcing a late multi-lane change is the unsafe option, and a
   missed exit costs only time.


.. admonition:: Question 9
   :class: hint

   The curvature-constrained speed limit is
   :math:`v_{\max} = \sqrt{a_{\text{lat,max}} / \kappa}`. With
   :math:`a_{\text{lat,max}} = 2.5\ \text{m/s}^2` and a curve of radius
   50 m, the maximum comfortable speed is approximately:

   A. 5.0 m/s
   B. 11.2 m/s
   C. 25.0 m/s
   D. 125.0 m/s

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   Curvature is the reciprocal of radius: :math:`\kappa = 1/50 = 0.02`
   m\ :sup:`-1`. Then

   .. math::

      v_{\max} = \sqrt{2.5 / 0.02} = \sqrt{125} \approx 11.2\ \text{m/s}

   which is about 40 km/h. The common error is to substitute the radius
   directly for :math:`\kappa`, giving :math:`\sqrt{2.5/50} = 0.22` m/s.


.. admonition:: Question 10
   :class: hint

   When building a road graph from CARLA waypoints, keying nodes on the
   raw tuple ``(road_id, section_id, lane_id, wp.s)`` produces a graph
   with almost no edges. Why?

   A. ``wp.next()`` returns waypoints on different roads only.
   B. ``wp.s`` is a float, and ``generate_waypoints()`` and ``wp.next()``
      do not return bit-identical values for the same road position, so
      dictionary lookups fail.
   C. CARLA waypoints are immutable and cannot be dictionary keys.
   D. ``section_id`` is always zero, causing hash collisions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   The two APIs compute ``s`` independently, so tiny floating-point
   differences make ``next_key in waypoint_map`` fail for essentially
   every neighbour. The graph builds with the right number of *nodes* and
   almost zero *edges* -- and because the failure is silent, it surfaces
   later as "no route found." Quantizing ``s`` (e.g.
   ``int(round(wp.s / 1.0))``) makes both APIs agree. Asserting that the
   edge count is non-zero immediately after construction turns a
   mysterious failure into an obvious one.


----


True or False (Questions 11-15)
================================

.. admonition:: Question 11
   :class: hint

   **True or False:** CARLA's ``GlobalRoutePlanner.trace_route()`` returns
   a collision-free trajectory that accounts for other vehicles on the road.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``trace_route()`` is a **global route planner**: it searches the static
   road network topology and returns an ordered sequence of waypoints. It
   has no knowledge of dynamic obstacles, and it produces a path rather
   than a timed trajectory. Collision avoidance against other agents is
   the responsibility of the behavior planner (L9) and motion planner
   (L10).


.. admonition:: Question 12
   :class: hint

   **True or False:** A* with an admissible heuristic will always expand
   fewer nodes than Dijkstra on the same graph.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   A* never expands *more* nodes than Dijkstra given the same admissible
   heuristic, but it does not always expand strictly fewer. With
   :math:`h(n) = 0` the two are identical. More practically, a very weak
   heuristic -- such as Euclidean distance divided by a large
   :math:`v_{\max}` on a distance-weighted graph -- provides almost no
   guidance, and A* degenerates toward Dijkstra's behavior. The strength
   of the heuristic, not the choice of algorithm, determines the saving.


.. admonition:: Question 13
   :class: hint

   **True or False:** HD maps eliminate the need for online perception,
   since all road geometry and traffic control devices are already
   encoded.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   HD maps provide static **priors** -- lane geometry, speed limits,
   traffic light positions -- but they cannot represent anything dynamic
   or anything that has changed since the survey. The vehicle still needs
   perception for other agents, for the current *state* of a traffic light
   (the map gives its position, not whether it is red), and for
   construction zones or closures. Maps also go stale, which is why the
   industry trend is toward lighter maps with stronger online perception.


.. admonition:: Question 14
   :class: hint

   **True or False:** Dynamic rerouting should be triggered as soon as the
   vehicle detects any blockage on the planned route, and the new route
   may be adopted at any point.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Two problems. First, rerouting is normally triggered by a **threshold**
   (for instance when the remaining cost exceeds 1.5x an alternative)
   rather than by any blockage, to avoid oscillating between routes on
   minor fluctuations. Second, and more importantly, the new route must be
   ready **before the last decision point where the routes diverge** -- a
   vehicle cannot stop on a highway to recompute, and a route adopted
   after the exit has passed is useless.


.. admonition:: Question 15
   :class: hint

   **True or False:** Contraction Hierarchies and Hub Labeling are
   preprocessing techniques that let continental-scale routing queries be
   answered in microseconds.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Both precompute auxiliary structures over the road graph -- shortcut
   edges for Contraction Hierarchies, distance labels for Hub Labeling --
   trading offline computation and memory for extremely fast online
   queries. They are what makes Google Maps and OSRM feel instantaneous
   at continental scale. They are also why plain Dijkstra is adequate for
   this course: our graphs are a single CARLA town.


----


Essay Questions (Questions 16-18)
==================================

.. admonition:: Question 16
   :class: hint

   Explain the three-layer separation between the navigation layer, the
   behavior planner, and the motion planner when executing a lane change.
   State specifically what each layer decides.

.. dropdown:: Answer
   :class-container: sd-border-success

   The layers answer three different questions about the same maneuver:

   - **Navigation** decides *whether a lane change is needed at all*, and
     roughly where. It knows the route requires an exit in 500 m and the
     vehicle is in the wrong lane. It works on the static map, at km
     scale, and replans on the order of minutes.
   - **Behavior planning** (L9) decides *whether it is safe to execute
     now*. It consumes predicted trajectories of surrounding agents,
     evaluates gap acceptance in the target lane, and either commits to
     the maneuver, waits, or aborts one already in progress. It runs at
     1--10 Hz.
   - **Motion planning** (L10) decides *what the geometry is*. Given the
     committed decision, it generates a kinematically feasible,
     collision-free path into the target lane, respecting curvature and
     comfort limits, at 10--50 Hz.

   The value of the separation is that each layer's output constrains the
   layer below, keeping each search tractable. It also localizes failures:
   an unnecessary lane change is a navigation bug, an unsafe one is a
   behavior bug, and an uncomfortable one is a motion planning bug.


.. admonition:: Question 17
   :class: hint

   You are given a road graph whose edge costs are distances in metres.
   A colleague runs Dijkstra and A* on it, observes that both return the
   same route, and concludes that A* is broken. Explain what is actually
   happening and describe how to set up a meaningful comparison of the two,
   and separately a meaningful comparison of shortest-distance against
   fastest-time routing.

.. dropdown:: Answer
   :class-container: sd-border-success

   Nothing is broken. Dijkstra and A* with an admissible heuristic are
   **both optimal**, so on the same graph with the same cost function they
   must return paths of the same cost. Returning the same route is
   evidence that the implementation is correct, not that it is faulty.

   The two comparisons are different experiments:

   - **Dijkstra vs A\*** is a comparison of *search efficiency*, not
     route quality. Instrument both to count the number of nodes expanded
     (or popped from the priority queue) and compare those counts. A*
     should expand fewer, and the margin grows with the quality of the
     heuristic. Weighted A* with :math:`\varepsilon > 1` will expand fewer
     still, at the cost of an :math:`\varepsilon`-suboptimal route.
   - **Shortest-distance vs fastest-time** is a comparison of
     *objectives*, which lives in the **edge costs**, not the algorithm.
     Rebuild the graph with :math:`\text{cost}(e) = \text{length}(e) /
     v_{\text{limit}}(e)` and rerun. Only then can the routes legitimately
     differ -- and the fastest-time route will typically be longer in
     distance while favoring high-speed roads. Remember to change the
     heuristic to match the new units, or A* loses admissibility.


.. admonition:: Question 18
   :class: hint

   Describe the steps needed to convert a global route (a sequence of
   discrete waypoints) into a **reference path** usable by the motion
   planner, and explain why a raw waypoint list is insufficient.

.. dropdown:: Answer
   :class-container: sd-border-success

   A raw waypoint list gives position only, at a fixed spacing, with no
   indication of how fast to travel or how sharply the path bends. The
   motion planner and controller need both. Conversion involves:

   1. **Pose extraction.** Pull the ordered :math:`(x, y, z,
      \text{yaw})` from each waypoint to form the geometric path.
   2. **Curvature estimation.** Compute curvature at each point, for
      example via the Menger curvature of three consecutive points,
      :math:`\kappa = 4A / (abc)`. Curvature is what couples geometry to
      the speed profile.
   3. **Speed profile generation.** Set the target speed at each point to

      .. math::

         v_{\max}(s) = \min\left(v_{\text{limit}}(s),\;
           \sqrt{a_{\text{lat,max}} / \kappa(s)},\; v_{\text{comfort}}\right)

      so the vehicle slows for curves before reaching them rather than
      discovering the constraint mid-corner.
   4. **Smoothing (optional but usual).** Fit splines through the
      waypoints to remove the heading discontinuities that appear at lane
      changes and junction boundaries, where consecutive waypoints can
      jump laterally.

   The result is a dense reference with position, heading, curvature, and
   target speed at every sample -- which is exactly the input the Stanley
   and Pure Pursuit controllers of L11 expect.
