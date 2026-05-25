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


.. toctree::
   :hidden:
   :maxdepth: 2

   l8_lecture
   l8_exercises
   l8_quiz
   l8_references
