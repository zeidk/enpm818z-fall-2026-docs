====================================================
L10: Trajectory Generation & Control
====================================================

Overview
--------

This lecture turns the planner's path into a steering, throttle and brake
command. It opens with the behavior layer: for an AV that drives city
streets, one flat finite state machine (FSM) grows too fast as behaviors are
added, and a superstate and a behavior tree keep it small. A short Python
script builds and runs a behavior tree for four road behaviors. Trajectory
Generation gives the path a quintic offset in time, checked against a moving
car and scored for jerk. Drive-by-wire actuators carry the command over the
CAN bus and through the electronic control units to the wheel, with a
measured 0.2 s delay and checks that fail safe. The lecture then follows one
right turn in Town03: the kinematic bicycle model, a speed profile, a PID
controller for the speed, Pure Pursuit and Stanley for the
steering, and what Model Predictive Control (MPC) adds. The controller node
it describes reads five ROS topics and sends one command, and a demo shows
those topics live.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Say why one flat FSM grows too fast, and how a **superstate** and a
  **behavior tree** keep the behavior layer small.
- Write the **kinematic bicycle model** and find the steering angle that follows a curvature.
- Give a path a speed profile and a time (a **trajectory**), and say why a
  quintic speed change keeps the **jerk** small.
- Read a **PID** speed response: what P, I and D each do, what **windup** is
  and how clamping stops it.
- Work **Pure Pursuit**'s geometry by hand, from the lookahead circle to the
  steering angle.
- Predict how the **lookahead distance** changes Pure Pursuit, and compare it
  with **Stanley**.
- Say what **MPC** adds: a model, a horizon, limits, and only the first input
  applied.


Lecture Materials
-----------------

- :doc:`l10_lecture`: the notes, following the slides shown in class.
  Material cut from class sits in closed "More detail" boxes, right after
  the part it explains.
- :doc:`l10_exercises`, :doc:`l10_quiz` and :doc:`l10_references`.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l10_lecture
   l10_exercises
   l10_quiz
   l10_references


Next Steps
----------

- In the next lecture, **L11: End-to-End Driving, VLA and Imitation
  Learning**, one network goes from the sensors to a trajectory or to the
  controls, in place of the whole stack.
- Before then, run the four hands-on parts of this lecture,
  ``behavior_tree.py`` (with and without ``--no-pass``), and the topics demo
  if you have CARLA.
