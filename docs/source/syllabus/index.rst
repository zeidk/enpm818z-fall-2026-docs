Syllabus
========

.. note::

   The authoritative, printable syllabus is the PDF distributed on
   ELMS-Canvas. This page mirrors it. If the two ever disagree, the
   Canvas PDF governs -- please report the discrepancy.

Prerequisites
-------------

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **ENPM605** (or equivalent)
     - *Python Applications for Robotics.* Strong Python, object-oriented
       design, and ROS 2 development. Every group project depends on this.
   * - **ENPM673** (or equivalent)
     - *Perception for Autonomous Robotics.* Camera models, image
       processing, CNN fundamentals, and an introduction to state
       estimation.
   * - **Robotics fundamentals**
     - Kinematics (differential drive, Ackermann steering), basic control
       theory (PID, feedback), odometry and SLAM concepts.
   * - **Mathematics**
     - Linear algebra (matrix operations, eigendecomposition), probability
       (Gaussians, Bayes' rule), and calculus.

.. admonition:: If you are satisfying ENPM673 by "or equivalent"
   :class: tip

   Several lectures open with a "recap from ENPM673" note. The material
   these notes refer to is developed from first principles anyway where
   the course depends on it -- most importantly the Kalman filter, which
   is built up in full in :doc:`L3 </lectures/lecture3/l3_index>`. You
   will not be left without it. Do, however, review CNN fundamentals
   before L4 and camera calibration before L2.


Course and Instructor
---------------------

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Credits**
     - 3
   * - **Dates**
     - Sep 3 to Dec 10, 2026
   * - **Time**
     - Thursdays, 7:00 to 9:40 pm
   * - **Room**
     - JMP 2121
   * - **Instructor**
     - Zeid Kootbally, ``zeidk@umd.edu``
   * - **Office hours**
     - By appointment
   * - **TA**
     - None this semester

.. warning::

   **There is no TA this semester.** Everything routes to the instructor, so
   give setup problems a head start rather than a deadline. Post environment
   problems where classmates can see them -- someone else has almost certainly
   hit the same thing. Email replies within 24 hours where possible; use email
   for academic and personal concerns, not for due dates and point values
   already in this syllabus.


Grade Breakdown
---------------

These six numbers add up to your grade. There is nothing else.

.. list-table::
   :header-rows: 1
   :widths: 46 27 27
   :class: compact-table

   * - Component
     - % of course grade
     - % of project
   * - GP1: Sensor Suite & Data Pipeline
     - 10.2%
     - 12.75%
   * - GP2: Perception (YOLO vs. RT-DETR)
     - 27.2%
     - 34.0%
   * - GP3: Fusion & Localization
     - 17.0%
     - 21.25%
   * - GP4: Planning & Control
     - 13.6%
     - 17.0%
   * - Final Report
     - 12.0%
     - 15.0%
   * - Quizzes (5, equally weighted)
     - 20.0%
     - --
   * - **Total**
     - **100%**
     - **100%**

- The four group projects plus the final report make up **80%** of the course.
  The right-hand column expresses the same weights as shares of that 80%,
  which is where the odd decimals come from.
- **GP2 alone is more than a quarter of your grade.** It is the project that
  trains models -- start it early.
- **There is no final exam.** The final report is the capstone assessment, and
  there is no presentation.


Letter Grades
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25
   :class: compact-table

   * - Grade
     - Cutoff
     - Grade
     - Cutoff
   * - A+
     - 97.00%
     - C+
     - 77.00%
   * - A
     - 94.00%
     - C
     - 74.00%
   * - A-
     - 90.00%
     - C-
     - 70.00%
   * - B+
     - 87.00%
     - D+
     - 67.00%
   * - B
     - 84.00%
     - D
     - 64.00%
   * - B-
     - 80.00%
     - D-
     - 60.00%

F is anything below 60.00%.

.. warning::

   Cutoffs are applied consistently to every student: **89.99 is not 90.00.**
   Exceptions are not made for some and not others.


Late Work and Regrades
~~~~~~~~~~~~~~~~~~~~~~

**Late work**

- Group projects: **10% deduction per day, maximum 3 days**, zero thereafter.
- **The projects are cumulative**, so three late days on GP2 are three days
  taken out of GP3. The penalty is the smaller cost.
- Peer evaluations and quizzes cannot be made up outside the
  documented-absence process.
- Contact the instructor **before** a deadline, not after.

**Regrades**

- Submit in writing within **one week** of receiving the grade.
- Arithmetic and rubric-application errors are corrected immediately.
- Questions about how something was scored go to the instructor by email.


Quizzes
-------

Five quizzes, each worth **4%** of the course grade.

.. list-table::
   :header-rows: 1
   :widths: 25 20 55
   :class: compact-table

   * - Quiz
     - Week
     - Date
   * - Quiz 1
     - 4
     - 09/24
   * - Quiz 2
     - 6
     - 10/08
   * - Quiz 3
     - 9
     - 10/29
   * - Quiz 4
     - 12
     - 11/19
   * - Quiz 5
     - 14
     - 12/10

- They check that concepts are absorbed **before** the project that depends on
  them.
- Short, and not designed to be tricky.
- **Closed everything**: no notes, no internet, no AI, no collaboration.
- **Missed quizzes**: a makeup is possible with a documented excused absence
  under University policy.

.. note::

   The self-check quizzes on each lecture page are a different thing entirely.
   Those are **not submitted and not graded**.


Peer Review
-----------

Your project grade is not purely a team grade.

.. list-table::
   :header-rows: 1
   :widths: 70 30
   :class: compact-table

   * - Component
     - Share
   * - Team project grade
     - 60%
   * - Peer review score
     - 40%

- Peer evaluations are submitted on ELMS within **48 hours** of every project
  deadline.
- They are **not optional**. Not submitting them forfeits your own peer review
  score for that project.
- Each member is responsible for understanding the **whole** submission, not
  only the part they wrote. You may be asked to walk through any part of it.

.. important::

   Forty percent is a lot, and that is deliberate. In a four-person team over
   a semester, the person who knows who did the work is not the instructor.
   The rubric rates **contribution**, not whether people liked each other, and
   it ships with GP1.


The Team Charter
~~~~~~~~~~~~~~~~

When teams form in Week 3, the first deliverable is not code. Each team writes
one page and posts it to ELMS:

- **Who owns what.** Name a primary and a backup for each module. Ownership is
  not exclusivity, it is accountability.
- **When you meet.** A recurring slot, agreed now, not renegotiated weekly.
- **How you use git.** Branch naming, who reviews, what must pass before a
  merge. Decide before the first merge conflict, not during it.
- **What happens when someone goes quiet.** How long before the team raises
  it, and with whom.
- **How you will disclose AI use.** One convention for the whole team.

.. tip::

   This takes ten minutes and it is the highest-return ten minutes of the
   semester. Nearly every team conflict traces back to something on this list
   that nobody wrote down in September.


Academic Integrity and Generative AI
------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 13 15 18 16 16
   :class: compact-table

   * - Assessment
     - Open notes
     - Learn online
     - Use AI
     - Ask classmates
     - Work in teams
   * - Group projects
     - Yes
     - Yes
     - Yes, disclosed\*
     - Yes
     - Yes
   * - Final report
     - Yes
     - Yes
     - Yes, disclosed\*
     - Within team
     - Within team
   * - Quizzes
     - No
     - No
     - No
     - No
     - No

- Every assignment carries the signed honor pledge.
- Submitting another team's code, or code from a previous offering of this
  course, is a violation.
- If you are ever unclear about the acceptable level of collaboration, **ask
  before submitting**.

.. warning::

   \*Disclosure carries no penalty. **Undisclosed use is a violation of the
   Code of Academic Integrity.**

**Permitted, with disclosure** -- on group projects and the final report:
explaining concepts and papers; interpreting error messages and stack traces;
reviewing code you have **already written**; suggesting debugging strategies;
generating small illustrative examples.

Disclose in the project README: name the tool, describe how it was used. Two
or three sentences per team member.

**Not permitted:** AI tools during quizzes; submitting AI-generated code that
no member of the team can read, explain and modify; using AI to write your
peer evaluations.

**The standard applied:** your team is responsible for every line submitted.
Any member may be asked, in class or office hours, to walk through any part:
why it works, what would break it, what you would change. **Work that cannot
be explained does not count**, regardless of whether it runs. This is the same
standard a future employer will apply.


.. _course-schedule:

Course Schedule
---------------

Lectures meet on **Thursdays**. The first lecture is **September 3, 2026**
and the last lecture is **December 10, 2026**. The Thanksgiving recess
(**Nov 25 to 29**) includes Thursday Nov 26, so there is no class that week;
all other Thursdays meet as scheduled. Dates below are given as MM/DD.

.. list-table::
   :header-rows: 1
   :widths: 10 8 34 20 28
   :class: compact-table

   * - Date
     - Week
     - Topic
     - Lecture
     - Deliverable
   * - 09/03
     - 1
     - Course Introduction & AV Landscape
     - L1
     - Setup milestone posted
   * - 09/10
     - 2
     - Sensor Technologies & Calibration
     - L2
     -
   * - 09/17
     - 3
     - Probabilistic State Estimation & Fusion
     - L3
     - Setup due, teams formed, GP1 posted
   * - 09/24
     - 4
     - Perception I: Object Detection (YOLO to DETR)
     - L4
     - Quiz 1
   * - 10/01
     - 5
     - Perception II: BEV, Occupancy & Segmentation
     - L5
     -
   * - 10/08
     - 6
     - Perception III: Tracking, Temporal & Deep Fusion
     - L6
     - Quiz 2, GP1 due, GP2 posted
   * - 10/15
     - 7
     - Localization & SLAM
     - L7
     -
   * - 10/22
     - 8
     - Navigation & Route Planning
     - L8
     -
   * - 10/29
     - 9
     - Prediction & Behavior Modeling
     - L9
     - Quiz 3, GP2 due, GP3 posted
   * - 11/05
     - 10
     - Motion Planning
     - L10
     -
   * - 11/12
     - 11
     - Trajectory Generation & Control
     - L11
     -
   * - 11/19
     - 12
     - End-to-End Driving, VLA & Imitation Learning
     - L12
     - Quiz 4, GP3 due, GP4 and report posted
   * - 11/26
     - --
     - **Thanksgiving recess -- no class**
     -
     -
   * - 12/03
     - 13
     - World Models & Simulation
     - L13
     -
   * - 12/10
     - 14
     - System Integration, Safety & Industry Outlook
     - L14
     - Quiz 5, GP4 due
   * - 12/17
     - 15
     - No class -- Final report submission window
     -
     - Final Report Due

.. note::

   This is a tentative schedule, subject to change as necessary.
   Monitor ELMS-Canvas for current deadlines.


Final Project: Building an ADS Pipeline
----------------------------------------

The course grade is built around a single **final project** consisting of
four cumulative group projects (GP1--GP4) plus a final report. Each GP
extends the ROS 2 package from the previous one, so that by GP4 your team
has a working ADS pipeline. **One package, extended four times.**

Teams consist of **4 students**, formed in **Week 3** after the schedule
adjustment period closes. The setup milestone before it is individual.

.. important::

   Starting from GP2, every project builds on your previous submission.
   You will extend -- not replace -- the ``ads_pipeline`` ROS 2 package
   your team created in GP1.

.. list-table::
   :header-rows: 1
   :widths: 26 12 12 12 38
   :class: compact-table

   * - Component
     - Posted
     - Due
     - Weight
     - Cumulative Output
   * - Setup milestone
     - Week 1
     - Week 3
     - pass/fail
     - CARLA running, ROS 2 workspace built, sensors publishing.
       **Individual.**
   * - GP1: Sensor Suite & Data Pipeline
     - Week 3
     - Week 6
     - 10.2%
     - CARLA sensor suite + ROS 2 package foundation.
   * - GP2: Perception (YOLO vs. RT-DETR)
     - Week 6
     - Week 9
     - 27.2%
     - Trained YOLO + RT-DETR models, deployed as a ROS 2 node.
   * - GP3: Fusion & Localization
     - Week 9
     - Week 12
     - 17.0%
     - Camera-LiDAR fusion + EKF localization.
   * - GP4: Planning & Control
     - Week 12
     - Week 14
     - 13.6%
     - Path planner + controller + behavioral logic.
   * - **Final Report**
     - Week 12
     - Week 15
     - 12.0%
     - Integration of GP1--GP4 + evaluation on unseen scenarios + report.

- The final report spec is published in **Week 12**, at the same time as GP4,
  so you can write it as you go instead of starting it in Week 14.
- Weights above are shares of the **course** grade. The Grade Breakdown table
  at the top of this page gives the same figures expressed as shares of the
  project.

.. tip::

   **If a project goes badly, you are not stuck with it.** A reference
   implementation is released after each due date, and your team may adopt it
   as the baseline for the next project.

.. note::

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
   * - Bridge
     - Course-provided ROS 2 bridge package
   * - Python
     - 3.10 to 3.12
   * - Machine learning
     - PyTorch, Ultralytics
   * - Libraries
     - ``numpy``, ``matplotlib``, ``opencv-python``, ``carla``
   * - IDE
     - Visual Studio Code (recommended)
   * - Version Control
     - Git + GitHub


Hardware Requirements
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - Component
     - Requirement
   * - GPU
     - **NVIDIA, 8 GB VRAM recommended.** 6 GB is workable with mixed
       precision and a reduced batch size.
   * - RAM
     - 16 GB minimum, 32 GB preferred
   * - CPU
     - Quad-core minimum
   * - Storage
     - 150 GB free

- CARLA runs a game engine, and your training runs on the same machine.
- **A virtual machine will not be adequate.**
- CARLA 0.9.16 is native on Ubuntu 22.04 only; on 24.04 the server runs in
  Docker.

.. warning::

   **If your GPU is marginal, the instructor needs to know in Week 1, not in
   October.** GP2 trains two detectors. A reference training recipe with
   expected wall-clock time on the minimum spec is published with the
   assignment, so you can tell within a day whether your hardware is the
   problem.
