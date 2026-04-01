====================================================
L12: World Models & Simulation
====================================================

Overview
--------

This lecture introduces **world models** -- neural networks that learn a
compressed, generative model of the physical world from driving data -- and
examines how they are transforming simulation-based ADS development. We survey
the most capable driving world models of 2024--2025, including Wayve GAIA-3
(15B parameters), NVIDIA Cosmos, and Vista (NeurIPS 2024), and explain how
each can be used for data augmentation, long-tail scenario generation, and
policy evaluation. The lecture concludes by comparing world models with
traditional physics-based simulators like CARLA, analyzing the sim-to-real
gap, and positioning world models as the "imagination module" within the
broader end-to-end driving stack.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Define a world model and explain how video prediction transformers and
  action-conditioned generation work at an architectural level.
- Describe the key design choices and capabilities of Wayve GAIA-3 (15B
  parameters, December 2025), NVIDIA Cosmos, and Vista (NeurIPS 2024).
- Identify three distinct applications of driving world models: data
  augmentation, long-tail scenario generation, and offline policy evaluation.
- Compare and contrast world models with traditional physics-based simulators
  like CARLA on dimensions of realism, control, and scalability.
- Explain what the sim-to-real gap is and describe at least two strategies --
  domain randomization and domain adaptation -- that address it.
- Articulate how a world model functions as the "imagination module" inside
  an end-to-end driving system, enabling model-based planning.
- Discuss the limitations of current generative world models, including
  consistency, physical plausibility, and controllability.
- Explain why CARLA remains relevant alongside generative world models for
  ADS education and algorithm development.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l12_lecture
   l12_quiz
   l12_references


Next Steps
----------

- In the next lecture, we will cover **System Integration, Safety & Industry
  Outlook**:

  - Full AV stack architecture: how modules communicate in production.
  - Middleware: ROS 2, DDS, and publish-subscribe at scale.
  - ISO 26262, SOTIF, and the UNECE GTR (January 2026).
  - Cybersecurity, V2X, and the industry outlook for 2026 and beyond.

- Review the GAIA-1 paper (Wayve, 2023) as a predecessor to GAIA-3.
- Explore the NVIDIA Cosmos announcement and technical report.
- Familiarize yourself with CARLA's scenario generation Python API, which
  will be used in the final project.
