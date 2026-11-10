====================================================
L10: Trajectory Generation & Control
====================================================

Overview
--------

This lecture takes the path the planners hand over and turns it into
steering and speed commands. It opens with the behavior layer: for an AV that
drives city streets, one flat finite state machine (FSM) grows too fast as
behaviors are added, and superstates, parallel regions and behavior trees keep
that layer small. A short Python script builds and runs a behavior tree for
four road behaviors. Then it follows one right turn in Town03: the kinematic
bicycle model, a trajectory (a path with a speed profile in time), a PID
controller for the speed, Pure Pursuit and Stanley for the steering, and what
Model Predictive Control (MPC) adds. The controller node it describes reads
five ROS topics and sends one command, and a demo shows those topics live.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Say why one flat FSM grows too fast, and how a **superstate**, parallel
  regions and a **behavior tree** keep the behavior layer small.
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

- :doc:`l10_lecture`: the notes, following the slides shown in class, with
  four worked steps cut from class in closed "More detail" boxes.
- :doc:`Going Further <l10_appendix>`: the deck's appendix (the bicycle
  model, the quintic, Pure Pursuit's arc, Stanley, and MPC).
- :doc:`l10_exercises`, :doc:`l10_quiz` and :doc:`l10_references`.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l10_lecture
   l10_appendix
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
