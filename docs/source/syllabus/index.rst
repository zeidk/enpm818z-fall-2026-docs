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


.. _peer-evaluation:

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

- Peer evaluations are **emailed to the instructor** within **48 hours** of
  every project deadline. The format is below.
- They are **not optional**. Not submitting yours forfeits your own peer
  review score for that project. Your teammates' scores are unaffected.
- Each member is responsible for understanding the **whole** submission, not
  only the part they wrote. You may be asked to walk through any part of it.
- Ratings are confidential. Teammates see only their final peer score, never
  who rated them what, and never the comments.

.. important::

   Forty percent is a lot, and that is deliberate. In a three-person team
   over a semester, the person who knows who did the work is not the
   instructor. The form rates **contribution**, not whether people liked
   each other.


The form
~~~~~~~~

Rate each teammate, **and yourself**, on five criteria.

Scale: **1** = well below what the team needed, **3** = a fair share,
**5** = carried more than their share, and did it well.

.. list-table::
   :header-rows: 1
   :widths: 5 25 70
   :class: compact-table

   * - #
     - Criterion
     - What it means
   * - 1
     - Technical contribution
     - Wrote, debugged, or tested a meaningful part of the submission.
   * - 2
     - Reliability
     - Did what they said, when they said. Told the team early when they
       could not.
   * - 3
     - Communication
     - Kept the team informed, asked when stuck, answered when asked.
   * - 4
     - Understanding
     - Can explain any part of the submission, including parts they did
       not write.
   * - 5
     - Collaboration
     - Reviewed others' work, helped unblock teammates, handled
       disagreement well.

**One required sentence per teammate** naming the specific thing they
contributed. "Worked hard" and "did their part" do not count. "Wrote the
LiDAR and RADAR attachments and found the queue-offset bug in the projection
driver" does.

**Your self-rating** is not used in your score. It is compared with what your
teammates said, and a large gap is one of the things that triggers a
conversation.

**One optional question:** is there anything the instructor should know
about how this team worked?


How to submit
~~~~~~~~~~~~~

One email per student, from your UMD address, to ``zeidk@umd.edu``.

**Subject line, exactly:**

.. code-block:: text

   [ENPM818Z] GP1 peer evaluation - Team X

**Body**, plain text, no attachments. Copy this template and fill it in.
One block per teammate, then your own block, then the optional question.

.. code-block:: text

   Project: GP1
   Team: X
   From: Alice Nguyen

   --- Bob Ortiz ---
   Technical contribution: 3
   Reliability: 3
   Communication: 3
   Understanding: 3
   Collaboration: 4
   What they contributed: Set up the recording launch file and the rates
   table, and wrote the Task 3 section of the report.

   --- Carol Singh ---
   Technical contribution: 5
   Reliability: 5
   Communication: 4
   Understanding: 5
   Collaboration: 5
   What they contributed: Wrote the LiDAR and RADAR attachments, the
   extrinsic, and found the queue-offset bug in the projection driver.

   --- Alice Nguyen (self) ---
   Technical contribution: 4
   Reliability: 5
   Communication: 4
   Understanding: 4
   Collaboration: 4
   What I contributed: Wrote the three camera attachments and the static
   TF tree, and produced the RViz screenshot.

   Anything the instructor should know: (optional)


How the score is computed
~~~~~~~~~~~~~~~~~~~~~~~~~

For each student, take the mean of the ratings **received** from teammates
across all five criteria. Call it :math:`R`. Take the team's mean of all
:math:`R` values. Call it :math:`T`. The student's peer factor is

.. math::

   F = \frac{R}{T}, \quad \text{clamped to } [0.6,\ 1.1]

Peer score for the project :math:`= 40 \times F`, capped at 40. The team
project grade supplies the other 60.

What this does in practice:

- A team where everyone rates everyone 5 gets :math:`F = 1.0` for everyone.
  So does a team where everyone rates everyone 3. Generous ratings do not
  inflate anyone. Only **relative differences** move the score.
- A member rated a full point below their teammates on a three-person team
  lands near :math:`F = 0.8`, an 8-point loss on a 100-point project.
- The clamp keeps a single project from being decided entirely by peer
  ratings. The floor is 0.6, so the worst case for a member who did
  contribute something is a 16-point loss. Genuine non-contribution is
  handled by the instructor, not by the formula.

**Worked example: Team X on GP1**

Team X's project scored 82 out of 100. Three members: Alice, Bob and Carol.
Each rated the other two on the five criteria. Received ratings, averaged
over the five criteria:

.. list-table::
   :header-rows: 1
   :widths: 16 21 21 21 21
   :class: compact-table

   * - Rated
     - From Alice
     - From Bob
     - From Carol
     - Received mean :math:`R`
   * - Alice
     - (self)
     - 4.6
     - 4.4
     - 4.5
   * - Bob
     - 3.0
     - (self)
     - 3.2
     - 3.1
   * - Carol
     - 4.8
     - 4.6
     - (self)
     - 4.7

Team mean :math:`T = (4.5 + 3.1 + 4.7) / 3 = 4.1`.

.. list-table::
   :header-rows: 1
   :widths: 12 18 14 22 16 18
   :class: compact-table

   * - Student
     - :math:`R / T`
     - :math:`F` after clamp
     - Peer score (40 × :math:`F`, cap 40)
     - Team part (60% of 82)
     - Individual grade
   * - Alice
     - 4.5 / 4.1 = 1.10
     - 1.10
     - 40.0 (capped from 44)
     - 49.2
     - **89.2**
   * - Bob
     - 3.1 / 4.1 = 0.76
     - 0.76
     - 30.4
     - 49.2
     - **79.6**
   * - Carol
     - 4.7 / 4.1 = 1.15
     - 1.10
     - 40.0 (capped from 44)
     - 49.2
     - **89.2**

Read across a row. The team part is the same 49.2 for everyone, since it is
60% of the shared project grade. The peer part is where the rows differ.
Bob's teammates rated him about a point and a half below the others, and
that costs him roughly 10 points against them on a 100-point project. Alice
and Carol both hit the cap, so the small difference between them disappears.
The peer score rewards pulling your weight, not out-rating a teammate who
also pulled theirs.

**The same team, rating everyone 5.** Every :math:`R` would be 5.0,
:math:`T` would be 5.0, every :math:`F` would be 1.0, and every member would
receive 40 + 49.2 = 89.2. Generosity changes nothing.

**Then scaled.** GP1 is worth 15 points of the group-project grade, so each
individual grade above is multiplied by 0.15. Bob's 79.6 becomes 11.9, and
Alice's and Carol's 89.2 becomes 13.4.

**With three members, one opinion carries a lot.** Each :math:`R` is the
mean of only two ratings. Bob's 3.1 came from a 3.0 and a 3.2, which agree,
so the score stands. If it had come from a 2.0 and a 4.2, the mean would be
the same 3.1 but the divergence rule below fires and the instructor reads
the comments before applying it.


Rules
~~~~~

- **Not submitting the evaluation forfeits your own peer score** for that
  project. Late evaluations are not accepted outside the documented-absence
  process.
- **No AI.** The sentences are yours.
- **Ratings that diverge sharply are read, not just averaged.** If one
  member rates a teammate two or more points below the others, or a
  self-rating differs from the received ratings by two or more points, the
  instructor reads the comments and may talk to the team before applying
  the score.
- **Reported non-contribution is a separate process.** If a teammate did
  not contribute to a project, say so in the optional question. The
  instructor follows up with the whole team, and the outcome may be a zero
  on the project for that member rather than a clamped factor.
- **Retaliation** for an honest evaluation is an academic integrity matter.


Where the formula comes from
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dividing a student's mean received rating by the team mean is the standard
way of turning peer ratings into an individual weighting, in use since the
early 1990s. Goldfinch and Raeside [1]_ introduced it, and Conway, Kember,
Sivan and Wu [2]_ reduced it to the single multiplicative factor used here.
Kaufman, Felder and Fuller [3]_ applied it in engineering courses with
self-ratings excluded and a maximum factor of 1.10, which is the ceiling
used here. It is also the "adjustment factor" computed by CATME [4]_, the
most widely used peer evaluation instrument in engineering education,
whose five rating dimensions the criteria above condense, and the factor
computed by SPARK [5]_. The five sources apply the factor to the whole
team grade; this course applies it to the 40% peer share only, and adds a
floor of 0.6, so that a single project cannot be decided entirely by peer
ratings.

.. [1] Goldfinch, J. and Raeside, R. (1990). Development of a peer
   assessment technique for obtaining individual marks on a group project.
   *Assessment & Evaluation in Higher Education*, 15(3), 210--231.
.. [2] Conway, R., Kember, D., Sivan, A. and Wu, M. (1993). Peer assessment
   of an individual's contribution to a group project. *Assessment &
   Evaluation in Higher Education*, 18(1), 45--56.
   https://doi.org/10.1080/0260293930180104
.. [3] Kaufman, D. B., Felder, R. M. and Fuller, H. (2000). Accounting for
   individual effort in cooperative learning teams. *Journal of Engineering
   Education*, 89(2), 133--140.
   https://doi.org/10.1002/j.2168-9830.2000.tb00507.x
.. [4] Ohland, M. W., Loughry, M. L., Woehr, D. J., Bullard, L. G., Felder,
   R. M., Finelli, C. J., Layton, R. A., Pomeranz, H. R. and Schmucker,
   D. G. (2012). The Comprehensive Assessment of Team Member Effectiveness:
   development of a behaviorally anchored rating scale for self and peer
   evaluation. *Academy of Management Learning & Education*, 11(4),
   609--630. See also https://info.catme.org/instructor-faq/what-is-the-adjustment-factor/
.. [5] Freeman, M. and McKenzie, J. (2002). SPARK, a confidential web-based
   template for self and peer assessment of student teamwork: benefits of
   evaluating across different subjects. *British Journal of Educational
   Technology*, 33(5), 551--569. https://doi.org/10.1111/1467-8535.00291


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


.. _ai-disclosure:

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
     - Simulation, Scenario-Based Testing & World Models
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
