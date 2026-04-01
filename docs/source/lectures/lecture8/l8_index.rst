====================================================
L8: Motion Planning
====================================================

Overview
--------

This lecture covers the full motion planning stack for autonomous
vehicles, from high-level route planning down to collision-aware
path generation. You will learn the mathematical foundations of
vehicle kinematic models, implement classical graph-based and
sampling-based planners, and explore the emerging class of
diffusion-based neural planners that are redefining the state of
the art. The lecture concludes with algorithm selection criteria
and a hands-on CARLA implementation exercise.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Describe the three-tier motion planning hierarchy (route, behavior,
  motion) and explain how each tier constrains the next.
- Derive the bicycle kinematic model and articulate its nonholonomic
  constraints.
- Implement Dijkstra's algorithm and A* search with admissible
  heuristics on a road network graph.
- Explain how RRT and RRT* explore configuration space and why RRT*
  achieves asymptotic optimality.
- Construct a state lattice and perform graph search over it for
  structured road scenarios.
- Apply geometric collision detection methods with appropriate safety
  margins.
- Describe how diffusion-based planners (Diffusion Planner, DiffusionDrive)
  formulate planning as iterative denoising.
- Select an appropriate planning algorithm given task requirements,
  environment structure, and computational constraints.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l8_lecture
   l8_quiz
   l8_references


Next Steps
----------

- In the next lecture, we will cover trajectory planning and control:

  - Adding the time dimension: converting paths into trajectories
  - Polynomial and spline-based trajectory generation
  - Model Predictive Control (MPC) formulation
  - Pure Pursuit, Stanley, and PID lateral/longitudinal controllers

- Complete the CARLA motion planning exercise from this lecture.
- Read Chapter 4 of *Principles of Robot Motion* (Choset et al.)
  for deeper coverage of sampling-based planners.
