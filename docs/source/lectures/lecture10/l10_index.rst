====================================================
L10: Prediction & Decision-Making
====================================================

Overview
--------

This lecture addresses the two cognitive layers that separate a
reactive path-follower from a genuinely intelligent autonomous
vehicle: predicting the future behavior of surrounding agents
and making strategic decisions about how to interact with them.
You will learn classical and learned trajectory prediction models,
Transformer-based multi-modal prediction architectures, and
behavior planning approaches ranging from finite state machines
to imitation learning with DAgger. The lecture concludes with a
CARLA exercise integrating prediction and a behavioral planner.


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
- Formulate behavior cloning as supervised learning and identify
  its key failure mode (distribution shift).
- Explain how DAgger addresses distribution shift and when it
  converges to an optimal policy.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l10_lecture
   l10_quiz
   l10_references


Next Steps
----------

- In the next lecture, we will cover end-to-end driving and
  foundation models:

  - End-to-end sensor-to-control neural networks
  - Vision transformers and multi-modal representations
  - Large language models as driving planners
  - Foundation models and generalist AV agents

- Complete the CARLA behavioral planner exercise from this lecture.
- Read the MotionTransformer paper (Shi et al., NeurIPS 2023) for
  deeper coverage of Transformer-based prediction.
