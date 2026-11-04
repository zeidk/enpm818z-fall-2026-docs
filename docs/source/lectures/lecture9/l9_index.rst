====================================================
L9: Motion Planning
====================================================

Overview
--------

**The route planner gives the AV a route: the lanes to follow. L9 finds the
path for the next few seconds** that follows the route and stays clear of
every object, through the next lane if needed. A path is the curve the AV
follows, with positions and headings and no times; the controller of the
next class drives it.

The lecture follows one road of CARLA's Town03 map, read from the map file.
The AV drives at 10 m/s in the right lane, and a car is parked 58 m ahead in
the same lane. Every road method today runs on this scene:

- **Configuration space.** Three numbers, :math:`(x, y, \theta)`, place the
  whole AV. The parked car becomes a region, 9.0 m by 3.8 m, that the AV's
  base link must avoid. Steering limits the tightest turn to 3.41 m.
- **The Frenet frame.** Positions along the road, :math:`s`, and across it,
  :math:`d`. The lanes become lines of constant :math:`d`, and the parked
  car sits at :math:`s` = 118.00 m, :math:`d` = −0.30 m.
- **Sampling paths.** 31 candidate paths, shifted sideways: 18 collide, 4
  turn too hard, and the cheapest of the other 9 passes in the left lane at
  a cost of 5.07. Planned again every 0.5 s, the AV passes the car and comes
  back to its lane.
- **Collision checking.** Three circles cover the AV. The check never misses
  a real collision, but it can drop a path that was free.
- **Behavior.** The layer that picks the task, as a finite state machine.
  With the left lane closed, the AV stops behind the car.
- **Garage planners.** Where there is no lane to follow: grid search, hybrid
  A* and RRT, in a parking garage.


Learning Objectives
-------------------

After this lecture, you can:

- Say what a **local planner** takes from the route planner and hands to
  the controller.
- Describe the AV by its **configuration** :math:`(x, y, \theta)`, and grow
  an obstacle into the region the AV's base link must avoid.
- Convert a point between the map and the **Frenet frame**
  :math:`(s, d)`, and say where the frame fails.
- Generate **candidate paths** with sideways shifts, score them, and add a
  cost term.
- Check a pose for collision with **circles**, and say why the check is
  conservative.
- Explain the **behavior layer** with a **finite state machine**, and find
  the **Nash equilibria** of a lane change between the AV and another car.
- Explain **hybrid A*** and **RRT**, and say where each planner is used.


Lecture Materials
-----------------

- :doc:`l9_lecture`: the notes, following the slides shown in class.
- :doc:`Going Further <l9_appendix>`: the deck's appendix (the region for
  two boxes, the Frenet formulas, how hard a candidate turns and the S
  curve, more or fewer circles, grid search, hybrid A*'s six steps and its
  estimates of cost to go, and RRT*).
- :doc:`l9_code`: the hands-on, five parts (``scene``, ``sample``,
  ``drive``, ``rrt`` and ``search``), and the files of two in-class
  exercises (a spreadsheet and a fifth cost term; the third, a game, needs
  no code).
- :doc:`l9_exercises`, :doc:`l9_quiz` and :doc:`l9_references`.

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
- **Before then:** finish the two exercises and the three hands-on parts on
  the :doc:`Code page <l9_code>`, and read "The S Curve" and "Hybrid A*" in :doc:`Going Further
  <l9_appendix>`.
