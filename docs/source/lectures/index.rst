====================================================
Lectures
====================================================

Overview
--------

The lectures in ENPM818Z follow a progressive structure, starting with the autonomous vehicle landscape and sensor fundamentals, then building through perception, fusion, localization, planning, and control, and culminating with end-to-end driving, world models, and system integration. Each lecture introduces new concepts through explanation, live demonstrations, and hands-on exercises in CARLA. Lecture materials are available on Canvas and GitHub.

.. tip::

   Each assignment builds on the previous one to form a cumulative ADS pipeline. Review the CARLA exercises after each lecture and run them on your own machine.


Schedule
--------

.. list-table::
   :widths: 8 40 52
   :header-rows: 1
   :class: compact-table

   * - Lecture
     - Topic
     - Key Concepts
   * - L1
     - Course Introduction & AV Landscape
     - SAE levels, DDT, ODD, industry status (2026), safety standards (ISO 26262, SOTIF, UNECE GTR), CARLA setup, development environment
   * - L2
     - Sensor Technologies & Calibration
     - Camera, LiDAR, RADAR, IMU, GNSS; intrinsic/extrinsic calibration; sensor placement and complementarity
   * - L3
     - Perception I: Object Detection (YOLO to DETR)
     - CNN fundamentals, YOLO architecture, transformer attention mechanism, DETR (encoder-decoder, object queries, bipartite matching), YOLO vs. DETR comparison
   * - L4
     - Perception II: BEV Perception & Occupancy Networks
     - Bird's-Eye View representation, BEVFormer, camera-to-BEV projection, 3D occupancy grids, modern AV perception paradigm
   * - L5
     - Perception III: Segmentation, Tracking & Temporal Reasoning
     - Semantic segmentation (U-Net, DeepLab), driveable surface and lane detection, multi-object tracking (SORT, DeepSORT), temporal fusion
   * - L6
     - Multi-Sensor Fusion
     - Fusion architectures (early, intermediate, late), Kalman Filter, EKF, UKF, particle filters, cross-attention fusion, data association, uncertainty quantification
   * - L7
     - Localization & SLAM
     - GNSS/RTK, dead reckoning, visual/LiDAR odometry, probabilistic localization, SLAM frontend (ICP, feature extraction), SLAM backend (pose graphs, loop closure)
   * - L8
     - Motion Planning
     - Planning hierarchy, vehicle kinematic models, A*, Dijkstra, RRT, PRM, lattice planners, collision detection, diffusion-based planning
   * - L9
     - Trajectory Planning & Control
     - Path vs. trajectory, polynomial and spline generation, optimization-based planning, MPC, Pure Pursuit, Stanley controller, real-time replanning
   * - L10
     - Prediction & Decision-Making
     - Trajectory prediction (transformer-based), behavior planning, state machines, imitation learning (behavior cloning), practical decision-making in traffic
   * - L11
     - End-to-End Driving & Foundation Models
     - UniAD, DriveTransformer, Vision-Language-Action (VLA) models, DriveVLM, modular vs. end-to-end debate
   * - L12
     - World Models & Simulation
     - Learned simulators, video prediction transformers, GAIA-3, NVIDIA Cosmos, Vista, generative scenario generation, data augmentation
   * - L13
     - System Integration, Safety & Industry Outlook
     - AV system architecture, middleware, ISO 26262, SOTIF, UNECE GTR on ADS, V2X, industry trends, course wrap-up


Contents
--------

.. toctree::
   :maxdepth: 3
   :titlesonly:

   lecture1/l1_index
