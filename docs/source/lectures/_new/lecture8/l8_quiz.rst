====================================================
Practice Quiz
====================================================


.. admonition:: Instructions
   :class: note

   These practice questions cover the material from L8: Navigation &
   Route Planning. Click the dropdown below each question to reveal the
   answer and explanation.


Question 1
----------

What is the key difference between navigation (route planning) and
motion planning?

A. Navigation uses neural networks; motion planning uses classical algorithms.
B. Navigation operates at the city scale on road graphs; motion planning
   operates at the local scale on continuous space.
C. Navigation considers obstacles; motion planning does not.
D. Navigation runs at 50 Hz; motion planning runs once per trip.

.. dropdown:: Answer

   **B.** Navigation operates at the city scale, finding the optimal
   sequence of road segments on a road network graph (km scale, replanned
   every few minutes). Motion planning operates at the local scale (10--50 m),
   finding collision-free paths in continuous configuration space at 10--50 Hz.
   They address different layers of the planning hierarchy.


Question 2
----------

In a road network graph used for AV navigation, what do nodes and edges
typically represent at the **lane level**?

.. dropdown:: Answer

   **Nodes** represent lane-level waypoints at regular intervals (e.g.,
   every 2 meters), each storing position, road ID, lane ID, speed limit,
   and lane width. **Edges** represent connections between waypoints and
   are typed: lane-follow (same lane, consecutive), lane-change (adjacent
   lane), or junction (connecting different roads through an intersection).


Question 3
----------

Which of the following is **NOT** encoded in an OpenDRIVE map file?

A. Road geometry (reference lines with arcs, spirals)
B. Lane structure (driving, shoulder, sidewalk)
C. Real-time traffic density
D. Traffic signal positions

.. dropdown:: Answer

   **C.** OpenDRIVE is a static map format that describes road geometry,
   lane structure, junctions, signals, and static objects. Real-time
   traffic density is dynamic information obtained from sensors, V2X
   communication, or traffic services -- it is not part of the map file.


Question 4
----------

An AV navigation system uses the cost function:

.. math::

   \text{cost}(e) = w_d \cdot d(e) + w_t \cdot t(e) + w_m \cdot m(e)

where :math:`d` is distance, :math:`t` is travel time, and :math:`m` is
maneuver complexity. How would you adjust the weights to produce a route
that **avoids complex intersections** even if it is longer?

.. dropdown:: Answer

   Increase :math:`w_m` (maneuver complexity weight) relative to
   :math:`w_d` and :math:`w_t`. For example, setting :math:`w_m = 10`,
   :math:`w_d = 1`, :math:`w_t = 1` would heavily penalize complex
   maneuvers (unprotected left turns, multi-lane merges), causing the
   planner to prefer longer but simpler routes that avoid difficult
   intersections.


Question 5
----------

Why is Euclidean distance divided by maximum speed limit an admissible
heuristic for A* route planning optimized for travel time?

.. dropdown:: Answer

   A heuristic is admissible if it never overestimates the true cost to
   the goal. The Euclidean distance is the shortest possible distance
   (straight line) between the current node and the goal. Dividing by
   the maximum speed limit gives the minimum possible travel time to
   reach the goal (driving the shortest distance at the fastest
   allowed speed). Since no real route can be shorter or faster than
   this, the heuristic never overestimates -- it is admissible.


Question 6
----------

**True or False:** CARLA's ``GlobalRoutePlanner.trace_route()`` returns
both waypoints and ``RoadOption`` annotations that indicate the type of
maneuver (lane follow, left turn, right turn, lane change) at each
waypoint.

.. dropdown:: Answer

   **True.** The ``trace_route()`` method returns a list of
   ``(waypoint, RoadOption)`` tuples. The ``RoadOption`` enum includes
   ``LANEFOLLOW``, ``LEFT``, ``RIGHT``, ``STRAIGHT``,
   ``CHANGELANELEFT``, ``CHANGELANERIGHT``, and ``VOID``. These
   annotations are essential for the behavior planner to prepare for
   upcoming maneuvers.


Question 7
----------

A vehicle is traveling on a highway and needs to exit in 800 m. The
navigation system determines it must change from the leftmost lane to
the exit lane (3 lanes to the right). What navigation-level information
is needed to plan this maneuver sequence?

.. dropdown:: Answer

   The navigation layer needs: (1) the distance to the exit diverge
   point (800 m), (2) the number of lane changes required (3), (3) lane
   change permissions (which segments allow lane changes -- solid vs.
   dashed markings), and (4) the minimum comfortable distance per lane
   change (~200 m each for safe execution). Given 3 lane changes
   needing ~600 m total, the first lane change should begin immediately.
   The navigation layer passes this as a sequence of ``CHANGELANERIGHT``
   road options to the behavior planner, which then coordinates with the
   motion planner for each individual lane change.


Question 8
----------

What are two key limitations of HD maps for AV navigation?

.. dropdown:: Answer

   (1) **Cost and maintenance**: HD maps cost $5K--$50K per kilometer
   to create and require continuous updates as road infrastructure
   changes (construction, new lanes, signal changes). (2) **ODD
   limitation**: The AV can only operate in mapped areas, restricting
   the operational design domain. If a road is not in the HD map, the
   vehicle cannot navigate it. This is why Tesla and others are moving
   toward "map-light" approaches that rely more on online perception.


Question 9
----------

Explain why dynamic rerouting must be computed **before** the vehicle
reaches the last decision point where old and new routes diverge.

.. dropdown:: Answer

   If the vehicle passes the diverge point before the new route is
   ready, it is committed to the old (potentially blocked) route with
   no alternative. On a highway, this could mean being forced into a
   traffic jam or a closed exit with no way to recover. The navigation
   system must detect the need for rerouting, compute the alternative
   route, and communicate it to the behavior planner while there is
   still at least one intersection or lane-change opportunity to
   transition to the new route. This imposes a real-time constraint
   on the route planner -- it must complete replanning within the time
   it takes to reach the next decision point.


Question 10
-----------

Describe the three steps needed to convert a global route (sequence of
waypoints) into a **reference path** usable by the motion planner.

.. dropdown:: Answer

   (1) **Waypoint extraction**: Extract the ordered :math:`(x, y, z,
   \text{yaw})` positions from the route waypoints. (2) **Speed profile
   generation**: For each waypoint, compute the target speed as the
   minimum of the posted speed limit, the curvature-constrained speed
   :math:`v = \sqrt{a_{\text{lat,max}} / \kappa}`, and a global comfort
   cap. (3) **Path smoothing** (optional): Apply spline interpolation
   (cubic or quintic) to produce a smooth, continuous path between the
   discrete waypoints, removing sharp transitions at lane changes and
   intersections. The result is a dense reference path with position,
   heading, curvature, and speed at each sample point.
