====================================================
L8: Navigation & Route Planning
====================================================

Overview
--------

This lecture covers the **navigation layer** of the autonomous driving
stack -- the system that determines *which roads to take* to reach a
destination. Navigation sits between localization (L7: knowing where
you are) and motion planning (L9: finding a collision-free local path).
While motion planning operates at the 10--50 m scale, navigation
operates at the city scale, producing a sequence of road segments and
lane-level waypoints that guide all downstream planning.

Students will learn how road networks are represented as graphs, how
global route planning algorithms work on these graphs, and how to use
CARLA's navigation API to plan and execute multi-kilometer routes.
This lecture directly supports **GP4: Planning & Control**, where
students must achieve route completion on instructor-provided scenarios.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain the role of navigation in the AV planning hierarchy and how
  it constrains behavior and motion planning.
- Describe how road networks are represented as directed graphs with
  lane-level topology (OpenDRIVE, Lanelet2).
- Apply Dijkstra and A* algorithms to road network graphs with
  appropriate cost functions.
- Use CARLA's ``GlobalRoutePlanner`` API to compute and visualize
  global routes.
- Explain how HD maps encode semantic road information (speed limits,
  traffic rules, lane connectivity) for navigation.
- Implement lane-level routing decisions (lane selection, merge
  planning, highway exit timing).
- Discuss dynamic rerouting strategies for handling road closures and
  unexpected obstacles.


.. admonition:: Materials in revision
   :class: note

   The lecture notes, exercises, quiz and references for this lecture are
   being revised against the current slide deck and are not published yet.
   This page will link to them once they are ready.


Next Steps
----------

- The next lecture covers **L9: Prediction & Behavior Modeling**: physics-,
  maneuver- and interaction-based trajectory prediction, Transformer-based
  scene encoding, multi-modal prediction, and finite state machine behavior
  planning. The route this lecture produces is the constraint every
  downstream planner works inside.
- Read the `CARLA map and navigation documentation
  <https://carla.readthedocs.io/en/0.9.16/core_map/>`_, in particular the
  waypoint API and the OpenDRIVE discussion.
- Review the `Lanelet2 <https://github.com/fzi-forschungszentrum-informatik/Lanelet2>`_
  map format to see how lane-level topology is represented in production.
