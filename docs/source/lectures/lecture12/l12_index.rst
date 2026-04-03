====================================================
L12: End-to-End Driving & Foundation Models
====================================================

Overview
--------

This lecture examines the fundamental architectural shift from modular autonomous
driving pipelines to end-to-end learned systems. We analyze landmark systems
such as UniAD (CVPR 2023) and DriveTransformer (ICLR 2025), explore how
Vision-Language-Action (VLA) models are beginning to encode common-sense
reasoning into driving, and assess the practical trade-offs of black-box neural
approaches versus interpretable, hand-engineered pipelines. The lecture also
covers the industrial deployments of Tesla and NVIDIA and addresses the
outstanding challenges of validation, safety, and interpretability for
data-driven end-to-end systems.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Distinguish the modular ADS pipeline from end-to-end approaches and articulate
  the key trade-offs of each design philosophy.
- Describe the architecture and key contributions of UniAD (CVPR 2023), including
  its unified query-based perception-prediction-planning formulation.
- Explain how DriveTransformer (ICLR 2025) achieves shared attention across all
  driving tasks and why this yields a 3x throughput improvement over UniAD.
- Identify the role of Vision-Language-Action (VLA) models -- including NVIDIA
  Alpamayo and DriveVLM -- in enabling chain-of-thought reasoning for driving.
- Summarize Tesla's and NVIDIA's end-to-end stacks, from sensor input through
  Bird's-Eye-View (BEV) feature extraction to planning and vehicle control.
- Evaluate the advantages (joint optimization, no cross-module information loss)
  and disadvantages (black-box behavior, data hunger, validation difficulty) of
  end-to-end driving.
- Discuss the safety, interpretability, and regulatory challenges that must be
  resolved before end-to-end systems can be deployed at scale.
- Explain the role of simulation in generating the training data and evaluation
  benchmarks required by end-to-end driving models.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l12_lecture
   l12_quiz
   l12_references


Next Steps
----------

- In the next lecture, we will cover **World Models & Simulation**:

  - What is a world model? Learning a simulator from data.
  - Wayve GAIA-3 (15B parameters) and NVIDIA Cosmos.
  - Vista (NeurIPS 2024): generalizable driving world models.
  - Applications in data augmentation, long-tail scenario generation, and
    policy evaluation.

- Review the UniAD paper: *Planning-Oriented Autonomous Driving* (Hu et al.,
  CVPR 2023).
- Skim the DriveTransformer preprint for its attention-sharing mechanism.
