====================================================
Final Project
====================================================

Overview
--------

The final project is the capstone experience of ENPM818Z, where you will
design, implement, and deploy a complete **automated driving system (ADS)**
pipeline in the CARLA simulator. Working in teams of 4 students, you will
build a system that perceives its environment, localizes itself, plans a
path, and controls a vehicle -- progressing from raw sensor data to
autonomous driving.

The project spans **12 weeks** through four progressive group projects
(GP1 through GP4), each building on the previous one. By GP4, your team
will have a working ADS. The final deliverable integrates and evaluates
the complete system on challenging, unseen scenarios.


Project Weight
--------------

The final project accounts for **80% of your overall course grade**:

.. list-table::
   :header-rows: 1
   :widths: 40 12 13 12 23
   :class: compact-table

   * - Component
     - Points
     - % of Project
     - Duration
     - Lectures
   * - GP1: Sensor Suite & Data Pipeline
     - 15
     - 15%
     - 3 weeks
     - L1--L2
   * - GP2: Perception (YOLO vs DETR)
     - 40
     - 40%
     - 3 weeks
     - L3--L5
   * - GP3: Fusion & Localization
     - 25
     - 25%
     - 3 weeks
     - L6--L8
   * - GP4: Planning & Control
     - 20
     - 20%
     - 3 weeks
     - L9--L11
   * - **Total**
     - **100**
     - **100%**
     - **12 weeks**
     -

.. note::

   GP2 carries the highest weight (40%) because it is the **AI-focused
   project** requiring deep learning model training, evaluation, and
   comparison.


Pipeline Progression
--------------------

Each group project extends the ROS 2 package from the previous one:

.. code-block:: text

   GP1: Sensors & Data         ->  CARLA sensor suite + ROS 2 package foundation
       |
   GP2: Perception (AI)        ->  YOLO + DETR detection nodes + evaluation
       |
   GP3: Fusion & Localization  ->  Multi-sensor fusion + EKF vehicle pose
       |
   GP4: Planning & Control     ->  Path planner + controller + behavior FSM
       |
   Final Report                ->  Evaluate on unseen scenarios + written report

.. important::

   Starting from GP2, every project builds on your previous submission.
   You will extend -- not replace -- the ``ads_pipeline`` ROS 2 package
   your team created in GP1.


Learning Objectives
-------------------

By completing the final project, you will be able to:

- Build a complete ROS 2 package for autonomous driving with sensors,
  perception, fusion, localization, planning, and control.
- Collect and label driving data from the CARLA simulator.
- Train and compare CNN-based (YOLO) and transformer-based (DETR) object
  detectors on custom data.
- Implement multi-sensor fusion combining camera, LiDAR, and RADAR data.
- Implement EKF-based localization fusing GNSS and IMU measurements.
- Design and implement motion planning (A*/RRT) and control (Pure
  Pursuit/PID) algorithms.
- Build a behavioral state machine for traffic rule compliance.
- Evaluate an ADS pipeline quantitatively (mAP, APE, route completion,
  collisions) and qualitatively (failure analysis).
- Document technical architecture and justify design decisions.


Team Formation
--------------

**Timeline**: Form teams by end of **Week 2**.

**Team Size**: 4 students per team.

**Process**:

1. Review the GP specifications below.
2. Form teams with complementary skills (perception/ML, controls,
   systems/ROS 2, documentation).
3. Submit team roster via Canvas.
4. Set up a shared Git repository for ``ads_pipeline``.

.. tip::

   Schedule a recurring weekly team meeting from Week 2 onward. Establish
   a communication channel (Slack, Discord, etc.) and divide responsibilities
   early.


Final Report (Weeks 14--15)
---------------------------

After GP4 is complete, your team will evaluate the full pipeline on
**instructor-provided scenarios** not seen during development and submit
a final report. There are no classes during Weeks 14--15.

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Scenario
     - Description
   * - Urban intersection
     - Navigate a 4-way intersection with cross traffic and pedestrians.
   * - Highway merging
     - Merge onto a highway (Town04) with flowing traffic.
   * - Pedestrian crossing
     - Detect and stop for a pedestrian crossing mid-block.
   * - Adverse weather
     - Complete a route under heavy rain and reduced visibility.
   * - Construction zone
     - Navigate around a lane closure with static obstacles.

**Final Deliverables:**

1. **Integrated ADS pipeline** -- All GP1--GP4 nodes running end-to-end.
2. **Evaluation results** -- Quantitative metrics on all 5 scenarios.
3. **Written report (8--10 pages)** -- Architecture, design decisions,
   results, failure analysis, lessons learned.
4. **Peer evaluation** -- Individual contribution assessment.

.. tab-set::

   .. tab-item:: Standard Track

      Integrate and refine the modular pipeline from GP1--GP4. Add
      improvements: enhanced behavioral planner (intersections, yielding),
      robustness across 3+ towns and weather conditions, performance
      optimization.

   .. tab-item:: Advanced Track (Optional -- GP5)

      Build a **Vision-Language-Action (VLA) model** that maps camera
      images and natural language commands directly to driving actions.
      Collect expert data from CARLA's autopilot, train a simplified VLA
      using frozen CLIP encoders, deploy as a ROS 2 node, and compare
      against the modular GP1--GP4 pipeline. See :doc:`GP5 </assignments/gp5>`
      for full specifications. Worth up to **10 bonus points**.


Academic Integrity
------------------

.. warning::

   **AI Usage Policy**

   AI tools (Copilot, ChatGPT, Claude, etc.) are **permitted** for coding
   assistance but must be documented. You must be able to explain any code
   you submit.

   **Permitted**:

   - Code assistance and debugging
   - Understanding concepts and algorithms
   - Generating boilerplate (launch files, package setup)

   **Prohibited**:

   - Using AI to write reports or answer quiz questions
   - Submitting AI-generated code you cannot explain
   - Sharing code between teams

   Violations will be treated as academic dishonesty.

**Peer Reviews**: Required for every GP. Your individual grade is
**60% project grade + 40% peer review score**.


Support Resources
-----------------

- **Instructor office hours**: By appointment (email zeidk@umd.edu)
- **CARLA documentation**: https://carla.readthedocs.io/en/0.9.16/
- **ROS 2 documentation**: https://docs.ros.org/en/humble/ (or Jazzy)
- **Ultralytics YOLOv8**: https://docs.ultralytics.com/
- **Course GitHub**: Materials, starter code, and example scripts
- **Canvas discussions**: For clarification and troubleshooting


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   gp1
   gp2
   gp3
   gp4
   gp5
