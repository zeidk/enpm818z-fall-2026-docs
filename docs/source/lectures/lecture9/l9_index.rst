====================================================
L9: Prediction & Behavior Modeling
====================================================

Overview
--------

A motion planner that ignores what other agents will do is unsafe;
this lecture supplies the missing piece by covering how to predict
surrounding agents' future trajectories and how to make strategic
behavioral decisions. You will study classical (physics-based,
maneuver-based) and modern (Transformer-based, multi-modal) prediction
models, then move into behavior planning with finite state machines
and learned policies. The lecture deliberately precedes Motion
Planning (L10): everything the planner does in L10-L11 consumes the
prediction outputs developed here.

Imitation learning and DAgger -- mentioned briefly as one form of
learned policy -- are developed in depth in L12 (End-to-End Driving,
VLA & Imitation Learning).


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain why trajectory prediction is necessary and how prediction
  horizon affects downstream planning quality.
- Compare physics-based, maneuver-based, and interaction-aware
  prediction approaches and identify their trade-offs.
- Describe how Transformer architectures encode scene context for
  motion prediction.
- Explain multi-modal prediction and why capturing multiple possible
  futures is essential for safe planning.
- Implement a finite state machine (FSM) behavior planner with
  lane-follow, lane-change, stop, and yield states.
- Contrast rule-based and learned decision-making approaches.
- Analyse common decision-making scenarios in traffic (intersections,
  merges, unprotected turns).


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l9_lecture
   l9_exercises
   l9_quiz
   l9_references


Next Steps
----------

- The next lecture covers **Motion Planning** (L10): planning
  hierarchy, vehicle kinematic models, A* / Dijkstra / RRT / lattice
  planners, collision detection, and diffusion-based planning. The
  planner will consume the predictions you build here.
- Read the MotionTransformer paper (Shi et al., NeurIPS 2022) for
  deeper coverage of Transformer-based prediction.
- The imitation-learning material that used to share this lecture
  has moved to L12, where it sits alongside the rest of the
  end-to-end / foundation-model treatment.
