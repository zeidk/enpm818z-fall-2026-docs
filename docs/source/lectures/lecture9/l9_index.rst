====================================================
L9: Motion Planning
====================================================

Overview
--------

**The route planner gives the AV a route: the lanes to follow. This lecture's
planner finds the path for the next few seconds** that follows the route and
stays clear of every object, through the next lane if needed. A path is the
curve the AV follows, with positions and headings and no times; the
controller of the next class drives it.

The lecture follows one road of CARLA's Town03 map, read from the map file.
The AV drives at 10 m/s in the right lane, and the obstacle, a parked car,
is 58 m ahead in the same lane. Every road method today runs on this scene:

- **Configuration space.** Three numbers, :math:`(x, y, \theta)`, place the
  whole AV. For the AV heading along the lane, the obstacle becomes a
  region, 9.0 m by 3.8 m, that the AV's base link must avoid. Steering
  limits the tightest turn to 3.41 m, and comfort at 10 m/s to 33.3 m.
- **Collision checking.** Three circles of radius 1.21 m cover the AV, and a
  gap under 0.3 m counts as a collision. The check never misses a real
  collision, but it can drop a path that was free.
- **The Frenet frame.** Positions along the road, :math:`s`, and across it,
  :math:`d`. The lanes become lines of constant :math:`d`, and the obstacle
  sits at :math:`s` = 118.00 m, :math:`d` = −0.30 m.
- **Sampling paths.** 31 candidate paths, shifted sideways: 18 collide, 4
  turn too hard, and the cheapest of the other 9 passes in the left lane at
  a cost of 5.07. Planned again every 0.5 s, the AV passes the obstacle and
  comes back to its lane.
- **Behavior.** The layer that picks the task. With the left lane closed,
  the AV stops behind the obstacle. The lane change, played as a game
  against another car, has two Nash equilibria, and a finite state machine
  picks one behavior at a time.
- **Garage planners.** Where there is no lane to follow: grid search,
  hybrid A*, RRT and RRT*, in a parking garage. Hybrid A*'s path, 30.6 m
  with one switch to reverse, is one the AV can drive.


Learning Objectives
-------------------

After this lecture, you can:

- Say what a **local planner** takes from the route planner and hands to
  the controller.
- Describe the AV by its **configuration** :math:`(x, y, \theta)`, and
  **grow an obstacle** into the region the AV's base link must avoid.
- Check a pose for **collision with circles**, and say why the check is
  **conservative**.
- Convert a point between the map and the **Frenet frame** :math:`(s, d)`.
- Generate **candidate paths** with sideways shifts, **score** them, and say
  how the weights pick the path.
- Explain the **behavior layer** with a finite state machine, and find the
  **Nash equilibria** of a lane change between the AV and another car.
- Explain **grid search**, **hybrid A*** and **RRT**, and say where each
  planner is used.


Lecture Materials
-----------------

- :doc:`l9_lecture`: the notes, following the slides shown in class.
- :doc:`Going Further <l9_appendix>`: the deck's appendix (C-space for two
  boxes, the Frenet formulas, where the Frenet frame fails, the S curve,
  more or fewer circles, behavior as an MDP, and hybrid A*'s estimates of
  cost to go).
- :doc:`l9_code`: the hands-on, five parts (``scene``, ``sample``,
  ``drive``, ``rrt`` and ``search``), the file of the spreadsheet exercise,
  and the demo of the same planner in CARLA, a ROS 2 package.
- :doc:`l9_exercises` (with the answers to the three in-class exercises),
  :doc:`l9_quiz` and :doc:`l9_references`.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l9_lecture
   l9_appendix
   l9_code
   l9_exercises
   l9_quiz
   l9_references


Next Steps
----------

- **Next class, L10: Trajectory Generation and Control.** Put a speed and a
  time on the path, then steer and drive along it.
- **Before then:** finish the three in-class exercises (the spreadsheet, Nash
  and the Prisoner's Dilemma) on the :doc:`Exercises page <l9_exercises>`
  and the three hands-on parts on the :doc:`Code page <l9_code>`, and read
  "The S Curve" in :doc:`Going Further <l9_appendix>`.
