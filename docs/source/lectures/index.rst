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

L1 to L5 are open. The later lectures open here one at a time, as their
slides are finished; the table shows the plan.

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
     - Two weeks. Uncertainty, variance and covariance; the Kalman filter (predict, update, gain); EKF, UKF and particle filters; covariance consistency (NIS, gating)
   * - L4
     - Perception I: Detecting Objects
     - IoU, NMS, precision, recall and mAP; one-stage detectors (YOLO); attention and transformers (query, key, value, ViT); DETR and RT-DETR (object queries, bipartite matching); confidence cut, domain gap and latency budget
   * - L5
     - Perception II: 3D Detection, BEV, Fusion & Tracking
     - Situational awareness (Endsley's three levels); 3D detection (PointPillars, CenterPoint, nuScenes NDS); semantic segmentation of the road; Bird's-Eye View (IPM, Lift-Splat-Shoot, BEVFormer, temporal BEV); 3D occupancy; fusion architectures, camera-LiDAR frustum association and BEVFusion; cooperative situational awareness and V2X; multi-object tracking with the L3 Kalman filter, data association, track lifecycle and the Tempe case; how each is used in industry
   * - L6
     - Localization & SLAM
     - GNSS/RTK, dead reckoning, visual/LiDAR odometry, probabilistic localization (EKF from L3), SLAM frontend (ICP, feature extraction), SLAM backend (pose graphs, loop closure)
   * - L7
     - Navigation & Route Planning
     - Road network graphs, OpenDRIVE/Lanelet2 maps, HD maps, global route planning (Dijkstra, A*), lane-level routing, dynamic rerouting, CARLA GlobalRoutePlanner
   * - L8
     - Prediction & Behavior Modeling
     - Trajectory prediction (physics-based, maneuver-based, interaction-aware, Transformer-based), multi-modal prediction, behavior planning, FSM, rule-based vs learned decision-making
   * - L9
     - Motion Planning
     - Planning hierarchy, vehicle kinematic models, A*, Dijkstra, RRT, PRM, lattice planners, collision detection, diffusion-based planning (consumes L8 predictions)
   * - L10
     - Trajectory Generation & Control
     - Path vs. trajectory, polynomial and spline generation, optimization-based planning, MPC, Pure Pursuit, Stanley controller, real-time replanning
   * - L11
     - End-to-End Driving, VLA & Imitation Learning
     - UniAD, DriveTransformer, Vision-Language-Action (VLA) models, DriveVLM, modular vs. end-to-end debate, behavior cloning, distribution shift, DAgger
   * - L12
     - Simulation, Scenario-Based Testing & World Models
     - Scenario-based testing, functional/logical/concrete scenarios, OpenSCENARIO, ISO 34500 series, test pyramid (MIL/SIL/HIL/VIL), open vs. closed loop, re-simulation, CARLA driving score, world models (GAIA-1 to GAIA-4, Cosmos, Vista)
   * - L13
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

..
   Hidden until each deck is finished (see HIDDEN_LECTURES in conf.py).
   To reopen a lecture, move its line back into the toctree above.
   lecture6/l6_index
   lecture7/l7_index
   lecture8/l8_index
   lecture9/l9_index
   lecture10/l10_index
   lecture11/l11_index
   lecture12/l12_index
   lecture13/l13_index
