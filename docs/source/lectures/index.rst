====================================================
Lectures
====================================================

Overview
--------

The lectures in ENPM818Z follow a progressive structure, starting with the autonomous vehicle landscape and sensor fundamentals, then building through perception, fusion, localization, navigation, planning, and control, and culminating with end-to-end driving, world models, and system integration. Each lecture introduces new concepts through explanation, live demonstrations, and hands-on exercises in CARLA. Lecture materials are available on Canvas and GitHub.

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
     - Probabilistic State Estimation & Fusion
     - Kalman Filter, EKF, UKF, particle filters; fusion architectures (early/intermediate/late); data association; weighted averaging / inverse-variance weighting
   * - L4
     - Perception I: Object Detection (YOLO to DETR)
     - CNN fundamentals, YOLO architecture, transformer attention mechanism, DETR (encoder-decoder, object queries, bipartite matching), YOLO vs. DETR comparison, industrial perception architectures, deployment
   * - L5
     - Perception II: BEV, Occupancy & Segmentation
     - Bird's-Eye View representation, BEVFormer, camera-to-BEV projection (LSS), 3D occupancy networks, semantic / instance / panoptic segmentation (DeepLabv3+, Mask R-CNN, PQ), driveable surface & lane detection
   * - L6
     - Perception III: Tracking, Temporal & Deep Fusion
     - Multi-object tracking (SORT, DeepSORT, ByteTrack), tracking metrics (MOTA, IDF1, HOTA), temporal reasoning, cross-attention / BEVFusion deep-learning fusion
   * - L7
     - Localization & SLAM
     - GNSS/RTK, dead reckoning, visual/LiDAR odometry, probabilistic localization (EKF from L3), SLAM frontend (ICP, feature extraction), SLAM backend (pose graphs, loop closure)
   * - L8
     - Navigation & Route Planning
     - Road network graphs, OpenDRIVE/Lanelet2 maps, HD maps, global route planning (Dijkstra, A*), lane-level routing, dynamic rerouting, CARLA GlobalRoutePlanner
   * - L9
     - Prediction & Behavior Modeling
     - Trajectory prediction (physics-based, maneuver-based, interaction-aware, Transformer-based), multi-modal prediction, behavior planning, FSM, rule-based vs learned decision-making
   * - L10
     - Motion Planning
     - Planning hierarchy, vehicle kinematic models, A*, Dijkstra, RRT, PRM, lattice planners, collision detection, diffusion-based planning (consumes L9 predictions)
   * - L11
     - Trajectory Generation & Control
     - Path vs. trajectory, polynomial and spline generation, optimization-based planning, MPC, Pure Pursuit, Stanley controller, real-time replanning
   * - L12
     - End-to-End Driving, VLA & Imitation Learning
     - UniAD, DriveTransformer, Vision-Language-Action (VLA) models, DriveVLM, modular vs. end-to-end debate, behavior cloning, distribution shift, DAgger
   * - L13
     - World Models & Simulation
     - Learned simulators, video prediction transformers, GAIA-3, NVIDIA Cosmos, Vista, generative scenario generation, data augmentation
   * - L14
     - System Integration, Safety & Industry Outlook
     - AV system architecture, middleware, ISO 26262, SOTIF, UNECE GTR on ADS, V2X, industry trends, course wrap-up

.. toctree::
   :hidden:
   :maxdepth: 3
   :titlesonly:

   lecture1/l1_index
   lecture2/l2_index
   lecture3/l3_index
   lecture4/l4_index
   lecture5/l5_index
   lecture6/l6_index
   lecture7/l7_index
   lecture8/l8_index
   lecture9/l9_index
   lecture10/l10_index
   lecture11/l11_index
   lecture12/l12_index
   lecture13/l13_index
   lecture14/l14_index
