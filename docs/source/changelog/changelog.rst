====================================================
Changelog
====================================================

All notable changes to the ENPM818Z Fall 2026 course documentation are recorded here.


.. dropdown:: v2.0.0 -- Full Curriculum Released: L4--L13 (2026-04-01)
   :icon: tag
   :class-container: sd-border-success

   Complete documentation for all 13 lectures of the ENPM818Z Fall 2026
   curriculum.

   .. rubric:: Lecture 4: Perception II -- BEV Perception & Occupancy Networks

   - BEV motivation, Lift-Splat-Shoot (LSS), BEVFormer (spatial/temporal
     attention), 3D occupancy networks, multi-camera fusion, nuScenes
     benchmarks, Tesla's BEV approach.

   .. rubric:: Lecture 5: Perception III -- Segmentation, Tracking & Temporal Reasoning

   - U-Net, DeepLabv3+/ASPP, instance and panoptic segmentation, SORT,
     DeepSORT, ByteTrack, tracking metrics (MOTA/MOTP/IDF1/HOTA),
     temporal reasoning methods.

   .. rubric:: Lecture 6: Multi-Sensor Fusion

   - Fusion architectures (early/intermediate/late), Kalman Filter
     predict-update cycle with full equations, EKF (Jacobian), UKF (sigma
     points), particle filter, filter comparison, data association
     (NN/GNN/JPDA/MHT), cross-attention fusion (BEVFusion), CARLA code.

   .. rubric:: Lecture 7: Localization & SLAM

   - GNSS/RTK, dead reckoning, visual/LiDAR odometry, EKF and particle
     filter localization, SLAM frontend (ICP, feature extraction,
     keyframes), SLAM backend (pose graph optimization, loop closure),
     LOAM/LeGO-LOAM/LIO-SAM/KISS-ICP, evaluation metrics (APE/RPE).

   .. rubric:: Lecture 8: Motion Planning

   - Planning hierarchy, bicycle model, Dijkstra, A*, RRT/RRT*, PRM,
     lattice planners, collision detection, diffusion-based planning
     (Diffusion Planner, DiffusionDrive), algorithm comparison.

   .. rubric:: Lecture 9: Trajectory Planning & Control

   - Path vs. trajectory, polynomial/spline generation, optimization-based
     planning, MPC (formulation, receding horizon), Pure Pursuit, Stanley
     controller, PID, controller comparison, emergency maneuvers.

   .. rubric:: Lecture 10: Prediction & Decision-Making

   - Trajectory prediction (physics/maneuver/interaction-aware),
     transformer-based prediction, multi-modal futures, behavior planning
     (state machines), imitation learning, DAgger, traffic scenarios.

   .. rubric:: Lecture 11: End-to-End Driving & Foundation Models

   - Modular vs. E2E debate, UniAD, DriveTransformer, VLA models
     (Alpamayo, DriveVLM), chain-of-thought reasoning, Tesla FSD v12,
     NVIDIA RL approach, safety/interpretability concerns.

   .. rubric:: Lecture 12: World Models & Simulation

   - World model definition, video prediction transformers, GAIA-3,
     NVIDIA Cosmos, Vista, generative scenario generation, sim-to-real
     gap, model-based planning (Dreamer), CARLA vs. world models.

   .. rubric:: Lecture 13: System Integration, Safety & Industry Outlook

   - Full AV stack architecture, ROS 2/DDS middleware, real-time
     constraints, ISO 26262 (ASIL, V-model), SOTIF, UNECE GTR on ADS,
     cybersecurity (ISO/SAE 21434), V2X (DSRC/C-V2X), industry outlook
     (US vs. China), robotaxi economics, ethics/liability, career paths,
     course summary.

   .. rubric:: Other Changes

   - Removed all old ENPM605 content from lecture4/ through lecture8/.
   - Created new directories for lecture9/ through lecture13/.
   - Updated lectures/index.rst toctree with all 13 lectures.
   - Each lecture includes: index, lecture notes, quiz (10 MC + 5 T/F +
     3 essay with hidden answers), and categorized references.


.. dropdown:: v1.2.0 -- L2 and L3 Documentation Released (2026-04-01)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Lecture 2: Sensor Technologies & Calibration

   - Lecture notes covering: complementarity principle (Luo 1989), camera
     systems (telephoto, fisheye, stereo, monocular depth), LiDAR (ToF,
     mechanical vs. solid-state), RADAR (Doppler effect, imaging radar,
     stationary object filtering risk), IMU (drift) and GNSS (signal
     blockage), IMU+GNSS fusion, intrinsic calibration (camera matrix K,
     distortion coefficients), extrinsic calibration (6-DOF transformation),
     sensor placement and coverage patterns, failure mode analysis (single
     point of failure, degraded mode, MRC), design trade-offs ($5K budget
     for highway vs. urban), industry sensor configurations (Waymo, Tesla,
     Cruise, Aurora, Mobileye).
   - Quiz: 15 multiple choice, 10 true/false, 5 essay questions with
     hidden answers.
   - References: sensor technologies, calibration tools, depth estimation,
     industry reports, textbooks.

   .. rubric:: Lecture 3: Perception I -- Object Detection (YOLO to DETR)

   - Lecture notes covering: perception in the AV stack (sensing ->
     perception -> planning -> control), perception inputs/outputs,
     taxonomy of perception tasks (low/mid/high-level), deep learning
     revolution (AlexNet to ResNet), YOLO evolution (v1 to v11 with
     COCO mAP), backbone-neck-head architecture, anchor-based vs.
     anchor-free detection, CIoU loss, training on custom data (with
     Python code), DETR architecture (encoder-decoder, object queries,
     bipartite matching via Hungarian algorithm), Deformable DETR, DINO,
     RT-DETR, YOLO vs. DETR comparison table, ROS 2 perception node
     deployment (with code), preview of BEV/occupancy/E2E.
   - Quiz: 15 multiple choice, 10 true/false, 5 essay questions with
     hidden answers.
   - References: detection papers, DL foundations, segmentation/tracking,
     datasets and benchmarks, tools and frameworks, textbooks.

   .. rubric:: Other Changes

   - Removed old ENPM605 exercise files from lecture2/ and lecture3/.
   - Updated lectures index with 13-lecture v2 curriculum schedule table.
   - Added L2 and L3 to the lectures toctree.


.. dropdown:: v1.1.0 -- Syllabus and Glossary Added (2026-04-01)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Syllabus (new)

   - Grade breakdown (30% assignments, 20% quizzes, 50% final project).
   - 15-week course schedule mapped to 13-lecture curriculum.
   - Cumulative assignment pipeline: A1 (sensors) -> A2 (perception) ->
     A3 (fusion/localization) -> A4 (planning/control) -> Final Project.
   - Final project with standard track (modular ADS) and advanced track
     (end-to-end driving).
   - Required software/tools and hardware recommendations.

   .. rubric:: Glossary (rewritten)

   - Replaced ENPM605 Python glossary with AV-focused terminology from
     L1--L3: 70+ terms across 22 letter sections covering sensors,
     perception, detection architectures, safety standards, CARLA
     concepts, and evaluation metrics.

   .. rubric:: Configuration

   - Set ``header_links_before_dropdown: 7`` to display all navbar items
     without overflow to "More" dropdown.
   - Set ``show_toc_level: 1`` for collapsed right-side TOC with scroll-
     based expansion.


.. dropdown:: v1.0.0 -- Initial Release (2026-04-01)
   :icon: tag
   :class-container: sd-border-success

   Initial release of the ENPM818Z Fall 2026 course documentation.

   .. rubric:: Course Structure

   - Course description and landing page (``index.rst``) with prerequisites,
     learning outcomes, grading, and required software.
   - CARLA Simulator section with overview, Python API reference, CLI options,
     troubleshooting, and performance tips.
   - CARLA setup guide for ROS 2 Humble (native Ubuntu 22.04).
   - CARLA setup guide for ROS 2 Jazzy (Docker on Ubuntu 24.04).

   .. rubric:: Lecture 1: Course Introduction & AV Landscape

   - Lecture notes covering: automated vehicles overview, key terminology
     (DDT, ODD, OES, ADAS vs. ADS), SAE J3016 levels, current industry
     landscape (2026), technical challenges, safety standards (ISO 26262,
     SOTIF, UNECE GTR), ADS development pipeline, course focus areas,
     course overview and assessment, development environment setup
     (Git, VS Code, Linux shell), and CARLA simulator introduction.
   - Quiz with 10 sample review questions.
   - References page with standards, government/policy, simulation tools,
     industry reports, textbooks, and coding standards.
