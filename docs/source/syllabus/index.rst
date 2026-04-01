Syllabus
========

Grade Breakdown
---------------

.. list-table::
   :header-rows: 1
   :widths: 60 20
   :class: compact-table

   * - Component
     - Percentage
   * - Individual Assignments (A1--A4)
     - 30%
   * - Quizzes (5)
     - 20%
   * - Final Project
     - 50%
   * - **Total**
     - **100%**

.. warning::

   Late submissions incur a 10% deduction per day (maximum 3 days).
   Beyond 3 days, submissions receive zero credit.


.. _course-schedule:

Course Schedule
---------------

.. list-table::
   :header-rows: 1
   :widths: 10 40 25 25
   :class: compact-table

   * - Week
     - Topic
     - Lecture
     - Deliverable
   * - 1
     - Course Introduction & AV Landscape
     - L1
     -
   * - 2
     - Sensor Technologies & Calibration
     - L2
     -
   * - 3
     - Perception I: Object Detection (YOLO to DETR)
     - L3
     - Quiz 1
   * - 4
     - Perception II: BEV Perception & Occupancy Networks
     - L4
     - A1 Posted
   * - 5
     - Perception III: Segmentation, Tracking & Temporal Reasoning
     - L5
     -
   * - 6
     - Multi-Sensor Fusion
     - L6
     - Quiz 2, A1 Due, A2 Posted
   * - 7
     - Localization & SLAM
     - L7
     -
   * - 8
     - Motion Planning
     - L8
     - Quiz 3, A2 Due, A3 Posted
   * - 9
     - Trajectory Planning & Control
     - L9
     -
   * - 10
     - Prediction & Decision-Making
     - L10
     - Quiz 4, A3 Due
   * - 11
     - End-to-End Driving & Foundation Models
     - L11
     - A4 Posted
   * - 12
     - World Models & Simulation
     - L12
     -
   * - 13
     - System Integration, Safety & Industry Outlook
     - L13
     - Quiz 5, A4 Due
   * - 14--15
     - Final Project Development & Presentations
     -
     - Final Project Due

.. note::

   This is a tentative schedule, subject to change as necessary.
   Monitor ELMS-Canvas for current deadlines.


Assignments: Building an ADS Pipeline
--------------------------------------

The four assignments form a **cumulative pipeline**. Each assignment extends
the ROS 2 package created in the previous one, so that by A4 you have a
working (if basic) automated driving system. The final project elevates this
pipeline into a complete, evaluated ADS.

.. important::

   Starting from A2, every assignment builds on your previous submission.
   You will extend -- not replace -- the ROS 2 package you created in the
   prior assignment.

.. list-table::
   :header-rows: 1
   :widths: 30 12 12 12 34
   :class: compact-table

   * - Assignment
     - Posted
     - Due
     - Lectures
     - Cumulative Output
   * - A1: Sensor Data & Exploration
     - Week 4
     - Week 6
     - L1--L2
     - ROS 2 package that connects to CARLA, spawns a vehicle with
       sensors (camera, LiDAR, odometry), and records data.
   * - A2: Perception (YOLO vs. DETR)
     - Week 6
     - Week 8
     - L3--L5
     - Adds a perception node that subscribes to camera images and
       publishes detected objects (bounding boxes, classes, confidence).
       Comparison of CNN vs. transformer-based detection.
   * - A3: Fusion & Localization
     - Week 8
     - Week 10
     - L6--L7
     - Adds a fusion/localization node that combines camera detections
       (from A2) with LiDAR and odometry to produce a fused world
       representation and vehicle pose estimate.
   * - A4: Planning & Control
     - Week 11
     - Week 13
     - L8--L10
     - Adds planning and control nodes that consume fused perception
       (from A3) and the localized pose to drive the vehicle through
       a CARLA scenario (lane following, obstacle avoidance).

The pipeline progression:

.. code-block:: text

   A1: Sensors & Data        ──►  Record CARLA sensor streams
       │
   A2: Perception            ──►  Detect objects from camera feed
       │
   A3: Fusion & Localization ──►  Fuse sensors + estimate vehicle pose
       │
   A4: Planning & Control    ──►  Drive the vehicle autonomously
       │
   Final Project             ──►  Complete ADS in complex scenarios


Final Project
-------------

The final project is the capstone of this course. Students integrate and
improve their A1--A4 pipeline into a **complete automated driving system**,
then evaluate it on challenging CARLA scenarios.

.. card::
   :class-card: sd-border-primary sd-shadow-sm

   **What You Will Deliver**

   1. **Integrated ADS pipeline** -- A single ROS 2 system combining
      perception, fusion, localization, planning, and control, running
      end-to-end in CARLA.
   2. **Complex scenario evaluation** -- Your system will be tested on
      scenarios beyond what was seen in assignments: urban intersections,
      highway merging, pedestrian crossings, and adverse weather.
   3. **Written report** -- Documents the system architecture, design
      decisions, failure analysis, and quantitative evaluation results.
   4. **Final presentation** -- Live demonstration of the system with Q&A.

.. tab-set::

   .. tab-item:: Standard Track

      Integrate and refine the modular pipeline from A1--A4. Add prediction
      or decision-making logic (e.g., behavioral state machine, rule-based
      planner) to handle complex traffic scenarios.

   .. tab-item:: Advanced Track (Optional)

      Replace part or all of the modular pipeline with an **end-to-end
      driving** approach using transformers or imitation learning. Compare
      performance against the modular baseline from the standard track.

.. note::

   The advanced track is optional and intended for ambitious students. Both
   tracks are graded on the same rubric -- the advanced track does not
   receive bonus points but provides deeper exposure to modern AV techniques.


Required Software and Tools
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - Component
     - Details
   * - Operating System
     - Ubuntu 22.04 LTS or 24.04 LTS
   * - CARLA Simulator
     - 0.9.16 (native on 22.04; Docker on 24.04)
   * - ROS 2
     - Humble Hawksbill (22.04) or Jazzy Jalisco (24.04)
   * - Python
     - 3.10+ with ``numpy``, ``matplotlib``, ``opencv-python``, ``carla``
   * - IDE
     - Visual Studio Code (recommended)
   * - Version Control
     - Git + GitHub


Hardware Recommendations
------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - Component
     - Recommendation
   * - GPU
     - NVIDIA GTX 1060 minimum (GTX 1070+ recommended)
   * - RAM
     - 8 GB minimum (16 GB+ preferred)
   * - CPU
     - Quad-core processor
   * - Storage
     - 20 GB free for CARLA and datasets
