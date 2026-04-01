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


Assignments
-----------

Students complete four individual assignments and a final project, each
building on prior material and using the CARLA simulator with ROS 2.

.. list-table::
   :header-rows: 1
   :widths: 35 15 15 15 20
   :class: compact-table

   * - Assignment
     - Posted
     - Due
     - Duration
     - Topic
   * - A1: Sensor Data & Exploration
     - Week 4
     - Week 6
     - 2 weeks
     - L1--L2
   * - A2: Object Detection -- YOLO vs. DETR
     - Week 6
     - Week 8
     - 2 weeks
     - L3--L4
   * - A3: Multi-Sensor Fusion & Localization
     - Week 8
     - Week 10
     - 2 weeks
     - L5--L7
   * - A4: Planning & Control Pipeline
     - Week 11
     - Week 13
     - 2 weeks
     - L8--L10


Final Project
-------------

The final project is the capstone of this course. Students design, implement,
and test components of an **automated driving system (ADS)** pipeline in CARLA,
integrating perception, localization, planning, and control modules developed
throughout the semester.

The project includes:

- A complete ROS 2 ADS implementation in CARLA.
- A written report documenting the system architecture, design decisions, and
  evaluation results.
- A final presentation demonstrating the system.

**End-to-end driving** using transformers or imitation learning is available as
an advanced project option for ambitious students.


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
