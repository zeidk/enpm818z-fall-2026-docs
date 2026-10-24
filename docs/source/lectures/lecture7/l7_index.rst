==================
L7: Route Planning
==================

Overview
--------

**L6 finds where the AV is on the map. L7 finds which lanes take it to the
goal.** That answer is the **route**: a sequence of lanes on a map made
before the drive, handed on as waypoints about every 2 m.

The lecture follows one trip through CARLA's Town01, a small town with a grid
of two-lane streets. The start, S, and the goal, G, were chosen for this
lecture. They are 141.9 m apart in a straight line, but no lane runs along
that line: the shortest route the AV can drive turns four times and is
260.6 m long. A planner has to search for it. On that one trip:

- **Map to graph.** What an HD map (high-definition map) holds, then Town01's
  own map file, ``Town01.xodr``, in the OpenDRIVE format CARLA uses. CARLA
  cuts each lane into segments, and a waypoint every 2 m, joined in driving
  order, makes the routing graph: 3107 nodes and 3143 edges.
- **Lane changes.** In Town03, many roads have two lanes the same way, and the
  lane decides the turn. The graph gets a third kind of edge, the lane change.
- **Edge costs.** Distance, travel time, or distance plus a penalty for each
  left turn. Travel time picks a route 6.3 m longer but 3.3 s faster than
  distance does.
- **Search.** Dijkstra and A* from the planning course, recapped in
  :doc:`Going Further <l7_appendix>`. On Town01's full graph, both find the
  same 260.6 m route, but A* takes 196 nodes on the way and Dijkstra 543.
- **Re-planning.** GP4's planner searches again when an object blocks the
  route or the AV ends up too far from it, and must not switch routes back
  and forth.
- **Maneuvers.** The route is handed on as the move at each intersection:
  right at 1, right at 3, left at 5 and right at 6.

Learning Objectives
-------------------

After this lecture, you can:

- Read a **map file** and turn it into a **routing graph**: say what a node
  and an edge are, and where they come from in OpenDRIVE.
- Say how **traffic rules and lanes** enter the graph: missing edges, driving
  directions, lane change edges.
- Choose an **edge cost** (distance, travel time, a left-turn penalty) and
  predict how it changes the route.
- Recall **Dijkstra and A*** from the planning course (recap in
  :doc:`Going Further <l7_appendix>`), and say what GP4's A* heuristic must
  satisfy: it never overestimates, in the units of the edge costs.
- Say when a planner must **plan again** (GP4's two triggers), and why it must
  not switch routes back and forth.
- Turn a route into **maneuvers** for the planners after route planning.

Lecture Materials
-----------------

- :doc:`l7_lecture`: the notes, following the slides shown in class.
- :doc:`Going Further <l7_appendix>`: the deck's appendix (route words in
  other stacks, path and trajectory, the map in the AV's architecture, map
  formats and Lanelet2, lanes and curves in OpenDRIVE, waiting at traffic
  lights, the Dijkstra and A* recap with its heuristics, and the searches on
  Town01's full graph).
- :doc:`l7_search_steps`: every step of both searches on the intersection
  graph.
- :doc:`l7_code`: the hands-on, five parts on the trip (``map``, ``graph``,
  ``costs``, ``search`` and ``replan``).
- :doc:`l7_exercises`, :doc:`l7_quiz` and :doc:`l7_references`.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l7_lecture
   l7_appendix
   l7_code
   l7_exercises
   l7_quiz
   l7_references
   l7_search_steps


Next Steps
----------

- **Next class, L8: Prediction and Behavior Modeling.** The other road users,
  and what they will do next.
- **Before then:** run the five hands-on parts on the
  :doc:`Code page <l7_code>`; then, on :doc:`l7_search_steps`, redo the A*
  steps with A*'s estimate at intersection 4, :math:`h(4)`, set to 120 m
  instead of 105 m, and see whether the route changes.
