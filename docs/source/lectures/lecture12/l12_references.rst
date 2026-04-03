====================================================
References
====================================================


.. dropdown:: Foundational Papers
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: UniAD (CVPR 2023)
         :link: https://arxiv.org/abs/2212.10156
         :class-card: sd-border-secondary

         **Planning-Oriented Autonomous Driving**

         Hu, Y. et al. (2023). Unified end-to-end model for tracking, mapping,
         motion forecasting, occupancy prediction, and planning.

      .. grid-item-card:: DriveTransformer (ICLR 2025)
         :link: https://arxiv.org/abs/2408.13630
         :class-card: sd-border-secondary

         **DriveTransformer: Unified Transformer for Scalable E2E AD**

         Shared attention across agent, map, and ego tokens. 3x throughput
         improvement over UniAD at equivalent or better performance.

      .. grid-item-card:: DriveVLM
         :link: https://arxiv.org/abs/2402.12289
         :class-card: sd-border-secondary

         **DriveVLM: Chain-of-Thought Empowered Large Vision Language Model**

         Tian, X. et al. (2024). VLM backbone with CoT reasoning for complex
         autonomous driving scenarios.

      .. grid-item-card:: BEVFormer
         :link: https://arxiv.org/abs/2203.17270
         :class-card: sd-border-secondary

         **BEVFormer: Learning BEV Representation from Multi-Camera Images**

         Li, Z. et al. (2022). The BEV encoder backbone used by UniAD and
         many subsequent end-to-end driving models.


.. dropdown:: Industry Systems and Blogs
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Tesla FSD Technical Blog
         :link: https://www.tesla.com/AI
         :class-card: sd-border-secondary

         **Tesla AI & Autopilot**

         Tesla's official AI page with technical details on FSD v12 and the
         HydraNet / end-to-end transition.

      .. grid-item-card:: NVIDIA DRIVE Platform
         :link: https://developer.nvidia.com/drive
         :class-card: sd-border-secondary

         **NVIDIA DRIVE Developer Resources**

         Documentation for DRIVE Orin/Thor SoCs, Hydra-MDP perception, and
         the NVIDIA end-to-end ADS stack.

      .. grid-item-card:: NVIDIA Alpamayo
         :link: https://developer.nvidia.com/blog/alpamayo
         :class-card: sd-border-secondary

         **Alpamayo VLA Model for Driving**

         NVIDIA's vision-language-action model for autonomous vehicles,
         supporting natural language commands and chain-of-thought reasoning.

      .. grid-item-card:: Wayve Blog
         :link: https://wayve.ai/thinking/
         :class-card: sd-border-secondary

         **Wayve Research Blog**

         End-to-end and world model research from the team behind LINGO and
         GAIA-3.


.. dropdown:: Survey Papers and Reviews
   :class-container: sd-border-secondary

   - Chen, L. et al. (2024). *End-to-End Autonomous Driving: Challenges and
     Frontiers.* arXiv:2306.16927. Comprehensive survey of E2E methods.
   - Renz, K. et al. (2022). *Plant: Explainable Planning Transformers via
     Object-Level Representations.* CoRL 2022. Interpretability for
     transformer-based planners.
   - Shao, H. et al. (2023). *ReasonNet: End-to-End Driving with Temporal and
     Global Reasoning.* CVPR 2023.


.. dropdown:: Safety and Validation
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ISO 26262
         :link: https://www.iso.org/standard/68383.html
         :class-card: sd-border-secondary

         **Functional Safety for Road Vehicles**

         The primary standard for hardware and software safety in automotive
         electrical and electronic systems.

      .. grid-item-card:: Responsibility-Sensitive Safety (RSS)
         :link: https://www.mobileye.com/technology/rss/
         :class-card: sd-border-secondary

         **Mobileye RSS Framework**

         Formal safety model providing mathematical guarantees on collision
         avoidance that can be layered on top of E2E planners.

   - Seshia, S. A. et al. (2018). *Formal Specification for Deep Neural
     Networks.* ATVA 2018.
   - Corso, A. et al. (2021). *Interpretable Safety Validation for Autonomous
     Vehicles.* ICRA 2021.


.. dropdown:: Simulation and Data
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: CARLA Simulator
         :link: https://carla.org/
         :class-card: sd-border-secondary

         **Open-Source AV Simulator**

         Primary simulation platform for this course. Used for scenario
         generation, sensor data collection, and E2E model evaluation.

         +++

         - `CARLA Documentation <https://carla.readthedocs.io/en/0.9.16/>`_
         - `CARLA GitHub <https://github.com/carla-simulator/carla>`_

      .. grid-item-card:: nuScenes Dataset
         :link: https://www.nuscenes.org/
         :class-card: sd-border-secondary

         **nuScenes Benchmark**

         The standard benchmark dataset used to evaluate UniAD,
         DriveTransformer, and other E2E models. Includes 1000 driving
         scenes with full sensor suite annotations.
