====================================================
L10: Trajectory Planning & Control
====================================================

Overview
--------

This lecture bridges motion planning and vehicle execution by adding
the time dimension to geometric paths and designing feedback
controllers that follow the resulting trajectories. You will learn
how polynomial and spline methods generate smooth, feasible
trajectories, how Model Predictive Control (MPC) optimizes a
receding-horizon plan in real time, and how Pure Pursuit, Stanley,
and PID controllers translate trajectory references into steering
and throttle commands. The lecture concludes with a CARLA exercise
implementing lane-following and obstacle avoidance.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Distinguish between a path (geometry only) and a trajectory
  (geometry plus time / velocity profile).
- Generate smooth trajectories using quintic polynomial and cubic
  spline methods.
- Formulate an MPC problem with prediction horizon, cost function,
  and constraints, and explain the receding-horizon principle.
- Implement the Pure Pursuit controller and derive the relationship
  between lookahead distance and lateral error.
- Implement the Stanley controller combining cross-track error and
  heading error for path following.
- Design a PID controller for longitudinal speed control.
- Select among Pure Pursuit, Stanley, MPC, and PID given task
  requirements, speed regime, and computational constraints.
- Implement lane-following and obstacle avoidance in CARLA using
  a trajectory planner and feedback controller.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l10_lecture
   l10_quiz
   l10_references


Next Steps
----------

- In the next lecture, we will cover prediction and decision-making:

  - Trajectory prediction for surrounding agents (physics-based,
    maneuver-based, interaction-aware)
  - Transformer-based multi-modal prediction
  - Behavior planning with state machines and learned policies
  - Imitation learning and DAgger for behavioral cloning

- Complete the CARLA trajectory following exercise from this lecture.
- Review the MPC tutorial in *Model Predictive Control: Theory and
  Design* (Rawlings & Mayne) Chapter 1.
