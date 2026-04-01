====================================================
References
====================================================


.. dropdown:: World Model Papers
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: GAIA-1 (Wayve, 2023)
         :link: https://arxiv.org/abs/2309.17080
         :class-card: sd-border-secondary

         **GAIA-1: Generative World Model for Autonomous Driving**

         Hu, A. et al. (2023). The first Wayve generative driving world model.
         9B parameters; action-conditioned video generation for driving.

      .. grid-item-card:: Vista (NeurIPS 2024)
         :link: https://arxiv.org/abs/2405.17398
         :class-card: sd-border-secondary

         **Vista: Generalizable Driving World Models**

         Gao, S. et al. (2024). Multi-dataset training for generalizable
         driving world models with standard evaluation protocol.

      .. grid-item-card:: DriveDreamer
         :link: https://arxiv.org/abs/2309.09777
         :class-card: sd-border-secondary

         **DriveDreamer: Towards Real-world-driven World Models**

         Wang, X. et al. (2023). World model conditioned on structured
         driving representations (HD maps, agent boxes).

      .. grid-item-card:: WoVogen
         :link: https://arxiv.org/abs/2312.02934
         :class-card: sd-border-secondary

         **WoVogen: World Volume-aware Driving Video Generation**

         Structured scene representation for temporally consistent
         driving video generation.


.. dropdown:: NVIDIA Cosmos
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: NVIDIA Cosmos Announcement
         :link: https://www.nvidia.com/en-us/ai/cosmos/
         :class-card: sd-border-secondary

         **NVIDIA Cosmos World Foundation Models**

         Official page for NVIDIA Cosmos, including model descriptions,
         licensing, and developer resources.

      .. grid-item-card:: Cosmos Technical Report
         :link: https://arxiv.org/abs/2501.03575
         :class-card: sd-border-secondary

         **Cosmos World Foundation Model Platform for Physical AI**

         NVIDIA (2025). Technical report describing the Cosmos model
         family, training data, and evaluation on robotics and driving.

      .. grid-item-card:: NVIDIA DRIVE
         :link: https://developer.nvidia.com/drive
         :class-card: sd-border-secondary

         **NVIDIA DRIVE Developer Platform**

         End-to-end ADS development platform integrating Cosmos, Hydra-MDP,
         DRIVE Orin/Thor, and DriveTransformer.


.. dropdown:: Foundational World Model Theory
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Dreamer (Hafner et al.)
         :link: https://arxiv.org/abs/1912.01603
         :class-card: sd-border-secondary

         **Dream to Control: Learning Behaviors by Latent Imagination**

         Hafner, D. et al. (2020). Seminal work demonstrating world-model-based
         RL for control from pixels. Conceptual ancestor of driving world models.

      .. grid-item-card:: World Models (Ha & Schmidhuber)
         :link: https://arxiv.org/abs/1803.10122
         :class-card: sd-border-secondary

         **World Models**

         Ha, D. & Schmidhuber, J. (2018). Original world model architecture
         (VAE + RNN + controller) that inspired subsequent large-scale work.

   - LeCun, Y. (2022). *A Path Towards Autonomous Machine Intelligence.*
     OpenReview. Influential whitepaper arguing world models are essential
     for general intelligence and autonomous driving.


.. dropdown:: Simulation Platforms
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: CARLA Simulator
         :link: https://carla.org/
         :class-card: sd-border-secondary

         **Open-Source AV Simulator**

         Physics-based driving simulator used throughout this course.

         +++

         - `Documentation <https://carla.readthedocs.io/en/0.9.16/>`_
         - `Scenario Runner <https://github.com/carla-simulator/scenario_runner>`_

      .. grid-item-card:: ASAM OpenSCENARIO 2.0
         :link: https://www.asam.net/standards/detail/openscenario/
         :class-card: sd-border-secondary

         **Scenario Specification Standard**

         Standard format for parameterized driving scenario families, used
         for safety validation and world model conditioning.

      .. grid-item-card:: Waymo Open Dataset
         :link: https://waymo.com/open/
         :class-card: sd-border-secondary

         **Waymo Open Dataset**

         Large-scale real-world driving dataset used for training and
         evaluating world models, including Vista.

      .. grid-item-card:: nuScenes
         :link: https://www.nuscenes.org/
         :class-card: sd-border-secondary

         **nuScenes Dataset**

         Multi-camera and LiDAR driving dataset, commonly used for
         world model training and evaluation benchmarks.


.. dropdown:: Sim-to-Real and Domain Adaptation
   :class-container: sd-border-secondary

   - Tobin, J. et al. (2017). *Domain Randomization for Transferring Deep
     Neural Networks from Simulation to the Real World.* IROS 2017.
     Foundational paper on domain randomization.
   - Ganin, Y. et al. (2016). *Domain-Adversarial Training of Neural
     Networks.* JMLR 2016. Foundation for domain adaptation methods.
   - Yang, J. et al. (2023). *UniSim: A Neural Closed-Loop Sensor
     Simulator.* CVPR 2023. Sensor-realistic simulation for ADS evaluation.
