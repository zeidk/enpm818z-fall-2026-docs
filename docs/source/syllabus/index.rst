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
   * - Final Project (GP1--GP4 + Final Evaluation)
     - 80%
   * - Quizzes (5)
     - 20%
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
     - Team Formation, GP1 Posted
   * - 3
     - Perception I: Object Detection (YOLO to DETR)
     - L3
     - Quiz 1
   * - 4
     - Perception II: BEV Perception & Occupancy Networks
     - L4
     -
   * - 5
     - Perception III: Segmentation, Tracking & Temporal Reasoning
     - L5
     - GP1 Due, GP2 Posted
   * - 6
     - Multi-Sensor Fusion
     - L6
     - Quiz 2
   * - 7
     - Localization & SLAM
     - L7
     -
   * - 8
     - Navigation & Route Planning
     - L8
     - GP2 Due, GP3 Posted
   * - 9
     - Motion Planning
     - L9
     - Quiz 3
   * - 10
     - Trajectory Planning & Control
     - L10
     -
   * - 11
     - Prediction & Decision-Making
     - L11
     - Quiz 4, GP3 Due, GP4 Posted
   * - 12
     - End-to-End Driving & Foundation Models
     - L12
     -
   * - 13
     - World Models & Simulation
     - L13
     -
   * - 14
     - System Integration, Safety & Industry Outlook
     - L14
     - Quiz 5, GP4 Due
   * - 15
     - No class -- Final report submission window
     -
     - Final Report Due

.. note::

   This is a tentative schedule, subject to change as necessary.
   Monitor ELMS-Canvas for current deadlines.


Final Project: Building an ADS Pipeline
----------------------------------------

The course grade is built around a single **final project** consisting of
four cumulative group projects (GP1--GP4) plus a final evaluation. Each GP
extends the ROS 2 package from the previous one, so that by GP4 your team
has a working ADS pipeline. Weeks 14--15 are dedicated to integrating,
evaluating, and presenting the complete system.

Teams consist of **4 students** (formed in Week 2).

.. important::

   Starting from GP2, every project builds on your previous submission.
   You will extend -- not replace -- the ``ads_pipeline`` ROS 2 package
   your team created in GP1.

.. list-table::
   :header-rows: 1
   :widths: 30 10 10 10 12 28
   :class: compact-table

   * - Component
     - Posted
     - Due
     - Duration
     - Weight
     - Cumulative Output
   * - GP1: Sensor Suite & Data Pipeline
     - Week 2
     - Week 5
     - 3 weeks
     - 15%
     - CARLA sensor suite + ROS 2 package foundation.
   * - GP2: Perception (YOLO vs. DETR)
     - Week 5
     - Week 8
     - 3 weeks
     - 40%
     - Trained YOLO + DETR models, deployed as ROS 2 node.
   * - GP3: Fusion & Localization
     - Week 8
     - Week 11
     - 3 weeks
     - 25%
     - Camera-LiDAR fusion + EKF localization.
   * - GP4: Planning & Control
     - Week 11
     - Week 14
     - 3 weeks
     - 20%
     - Path planner + controller + behavioral logic.
   * - **Final Report**
     - Week 14
     - Week 15
     - 1 week
     - (included above)
     - Integration of GP1--GP4 + evaluation on unseen scenarios + report.

.. note::

   GP2 carries the highest weight (40%) because it is the AI-focused
   project requiring deep learning model training, evaluation, and
   comparison. The final evaluation is not separately weighted -- it
   assesses the integration quality of GP1--GP4.

   See the :doc:`Final Project </assignments/index>` page for full
   specifications, rubrics, evaluation scenarios, and suggested team roles.


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
