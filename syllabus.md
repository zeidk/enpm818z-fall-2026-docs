---
title: "On-Road Automated Vehicles"
subtitle: "ENPM818Z | Sections 0101 and AEB1 | Fall 2026"
author: "Zeid Kootbally"
date: "University of Maryland"
geometry: margin=1in
fontsize: 11pt
colorlinks: true
linkcolor: RoyalBlue
urlcolor: RoyalBlue
toc: true
toc-depth: 2
numbersections: false
---

# Course Information

| | |
| --------------------- | ------------------------------------------------ |
| **Term**              | Fall 2026                                        |
| **Instructor**        | Zeid Kootbally (He/Him)                          |
| **Email**             | <zeidk@umd.edu>                                  |
| **Office Hours**      | By appointment                                   |
| **Credits**           | 3                                                |
| **Course Dates**      | September 3, 2026 to December 10, 2026           |
| **Course Times**      | Thursdays, 7:00 PM to 9:40 PM                    |
| **Classroom**         | J.M. Patterson Building (JMP), Room 2121         |

**ELMS-Canvas:** <https://umd.instructure.com/courses/1409148>

**Lecture notes:** <https://enpm818z-fall-2026-docs.readthedocs.io/en/latest/>

**Lecture code:** <https://github.com/rubixcubic/enpm818z-fall-2026-code>

\newpage

## Course Description

ENPM818Z provides a deep technical tour of on-road automated passenger
vehicles, building the full autonomy stack one layer at a time. The course
follows a deliberate pedagogical progression: sensors and calibration first,
then the probabilistic state-estimation backbone (Kalman, Extended Kalman,
Unscented Kalman, and particle filters) that everything else depends on,
then modern perception (object detection, Bird's-Eye-View representations,
3D occupancy networks, segmentation, and multi-object tracking), then
localization and SLAM, then route planning over HD maps, then prediction
of surrounding agents, and finally motion planning, trajectory generation,
and feedback control. Every concept is exercised hands-on in CARLA, where
students grow a single ROS 2 pipeline across the semester from raw sensor
input to closed-loop autonomous driving.

Beyond the classical modular stack, the course covers the algorithms and
architectures driving the state of the art in 2026: transformer-based
detection (DETR, RT-DETR), BEV transformers (BEVFormer, LSS), deep
multi-sensor fusion (BEVFusion, cross-attention), modern multi-object
trackers (SORT, DeepSORT, ByteTrack), transformer-based and multi-modal
trajectory prediction, sampling- and diffusion-based motion planners, and
Model Predictive Control. Students compare these against the rapidly
emerging end-to-end paradigm: UniAD, DriveTransformer, Vision-Language-
Action models such as DriveVLM and NVIDIA Alpamayo, imitation learning,
and DAgger. You will learn when each approach is the right tool for an
automotive-grade system.

The course closes with the engineering reality of shipping an automated
vehicle: world models and generative simulation (GAIA-3, NVIDIA Cosmos,
Vista) for training and long-tail evaluation, system integration over
ROS 2 / DDS middleware, and the safety standards (ISO 26262, ISO 21448 /
SOTIF, UNECE GTR on ADS, ISO/SAE 21434 cybersecurity) that bound what a
deployed AV is allowed to do.

### Key topics covered include:

- AV landscape, SAE J3016 levels, ODD, and the modern AV industry (2026)
- Sensor technologies and calibration: cameras, LiDAR, RADAR, IMU, GNSS
- Probabilistic state estimation: Kalman / EKF / UKF / particle filters
- Multi-sensor fusion: early / intermediate / late architectures, data
  association (Hungarian, JPDA, MHT), weighted averaging
- Object detection: YOLO family, DETR, RT-DETR, transformer attention
- BEV perception: Lift-Splat-Shoot, BEVFormer, 3D occupancy networks
- Semantic / instance / panoptic segmentation (DeepLabv3+, Mask R-CNN)
- Multi-object tracking: SORT, DeepSORT, ByteTrack, transformer MOT
- Deep-learning sensor fusion: cross-attention, BEVFusion
- Localization and SLAM: EKF-based fusion, scan matching (ICP, NDT),
  pose-graph optimization, loop closure
- HD maps and route planning: OpenDRIVE, Lanelet2, A\*, Dijkstra
- Trajectory prediction and behavior modeling: physics-based,
  transformer-based, multi-modal
- Motion planning: graph-based, sampling-based (RRT, RRT\*, PRM),
  lattice planners, diffusion-based planning
- Trajectory generation and control: quintic polynomials, B-splines,
  MPC, Pure Pursuit, Stanley, PID
- End-to-end driving: UniAD, DriveTransformer, behavior cloning, DAgger
- Vision-Language-Action (VLA) models: DriveVLM, NVIDIA Alpamayo
- World models and generative simulation: GAIA-3, NVIDIA Cosmos, Vista
- System integration over ROS 2 / DDS, safety standards (ISO 26262,
  SOTIF, UNECE GTR), V2X / C-V2X, cybersecurity (ISO/SAE 21434)

---

## Prerequisites

- **Prior Coursework**
    - *ENPM605: Python Applications for Robotics* (or equivalent).
      Strong Python programming skills, object-oriented design, and
      familiarity with ROS 2 development.
    - *ENPM673: Perception for Autonomous Robotics* (or equivalent).
      Sensors, vision, and perception pipelines, necessary for
      understanding CARLA sensor data and multi-sensor fusion.
- **Robotics Fundamentals**
    - Robot kinematics (differential drive, Ackermann steering).
    - Basic control theory (PID, feedback loops).
    - Localization and mapping concepts (odometry, SLAM, Kalman filters).
- **Mathematical Background**
    - Linear algebra (for transformations and state estimation).
    - Probability and statistics (sensor uncertainty, noise models).
    - Calculus and optimization (trajectory generation, control).
- **ROS 2**
    - Ability to create nodes, topics, services, and actions in ROS 2.
    - Experience with parameter servers and launch files.
    - Familiarity with rosbag recording and visualization in RViz.
- **Simulation & Tools**
    - Familiarity with simulation environments such as CARLA or Gazebo.
    - Experience with Git / GitHub for version control.
    - Ability to configure development environments in Ubuntu
      (20.04 / 22.04 / 24.04) with Python virtual environments or
      Docker.

---

## Learning Outcomes

After successfully completing this course, students will be able to:

1. **Understand the Core AV Stack.** Explain how an on-road automated
   vehicle is built up from sensing, probabilistic state estimation,
   perception, localization, route planning, prediction, motion
   planning, trajectory generation, control, and end-to-end approaches,
   and articulate the data dependencies between these layers.
2. **Apply Probabilistic State Estimation and Multi-Sensor Fusion.**
   Derive and implement the Kalman, Extended Kalman, Unscented Kalman,
   and particle filters; design early, intermediate, and late fusion
   architectures; and apply data association (Hungarian, JPDA, MHT) to
   combine LiDAR, RADAR, camera, IMU, and GNSS data.
3. **Implement Modern Perception Pipelines.** Build and evaluate CNN- and
   transformer-based object detectors (YOLO, DETR), BEV constructions
   (LSS, BEVFormer), 3D occupancy networks, semantic / instance /
   panoptic segmentation, and multi-object trackers (SORT, DeepSORT,
   ByteTrack) on CARLA data.
4. **Develop Localization and Mapping Systems.** Create and test
   localization and SLAM algorithms for real-time vehicle positioning in
   dynamic environments using EKF-based fusion, scan matching (ICP,
   NDT), HD maps, and pose-graph optimization with loop closure.
5. **Model Prediction, Behavior, and Plan Through to Control.** Forecast
   surrounding-agent trajectories with physics-based and transformer-
   based predictors, design FSM and learned behavior planners, run
   graph- / sampling- / lattice-based motion planners, generate smooth
   trajectories (quintic polynomials, B-splines), and implement Pure
   Pursuit, Stanley, MPC, and PID controllers.
6. **Evaluate End-to-End, VLA, and World-Model Approaches.** Compare
   modular vs. end-to-end stacks (UniAD, DriveTransformer), reason about
   imitation learning and distribution shift (behavior cloning, DAgger),
   and explain how Vision-Language-Action models (DriveVLM) and
   generative world models (GAIA-3, NVIDIA Cosmos, Vista) are reshaping
   training and validation.
7. **Integrate, Validate, and Analyze AV Systems.** Integrate perception,
   localization, prediction, planning, and control modules into a single
   CARLA + ROS 2 pipeline; apply automotive safety standards (ISO 26262,
   ISO 21448 / SOTIF, UNECE GTR, ISO/SAE 21434); and evaluate system
   reliability, robustness, and safety with simulation-based testing.

---

## Course Materials

### Required Resources

- **Book:** None.
- **Application / Software:**
    - Ubuntu 22.04 LTS or 24.04 LTS
    - Python 3.10+
    - CARLA 0.9.16 (primary simulator)
    - ROS 2 Humble or Jazzy
    - Visual Studio Code (recommended IDE)
    - Git + GitHub account
    - Docker (recommended for reproducible builds)
- **Total estimated cost of required course materials:** $0.00

### Supplemental Resources (no purchase required)

- **Readings / Documentation:**
    - [CARLA Documentation](https://carla.readthedocs.io/en/0.9.16/)
    - [ROS 2 Documentation](https://docs.ros.org/en/jazzy/)
    - [Autoware Documentation](https://autowarefoundation.github.io/autoware-documentation/)
    - [nuScenes Dataset](https://www.nuscenes.org/)
    - [Argoverse 2 Dataset](https://www.argoverse.org/av2.html)
- **Reference papers (representative):**
    - Bochkovskiy et al., *YOLOv4*; Carion et al., *DETR* (ECCV 2020);
      Zhao et al., *RT-DETR* (2024)
    - Philion & Fidler, *Lift-Splat-Shoot* (NeurIPS 2020); Li et al.,
      *BEVFormer* (ECCV 2022)
    - Bewley et al., *SORT* (2016); Wojke et al., *DeepSORT* (2017);
      Zhang et al., *ByteTrack* (2022)
    - Hu et al., *UniAD* (CVPR 2023, Best Paper); *DriveTransformer*
      (ICLR 2025)
    - Ross et al., *DAgger* (ICML 2011)
- **Course documentation:** Lecture notes are hosted on Read the Docs
  (link above) and the lecture code repository is on GitHub (link
  above). All slides are posted on ELMS-Canvas.

### Course Structure

This course includes both on-campus and online sections. To attend
synchronously online, log into ELMS-Canvas at the time of the Section
0101 class (Thursdays @ 7:00 PM) and select **Video Conference** from
the left side menu. This will open a Zoom link to the live classroom.

For asynchronous online students, all lectures will be recorded and
made available on ELMS-Canvas under **Panopto Recordings / Video
Lectures** within 24 hours of the class time. Be sure to review the
recorded lecture in a timely manner.

On-campus students come to class prepared to engage with the lecture
and materials. Online students, be sure to log into Canvas regularly
and participate in discussions and activities. Regardless of the
section you are enrolled in, participation is expected.

**Please note** that F1 students enrolled in the on-campus section
are required to attend in person. If you have a conflict on a
particular day, please reach out to me in advance to discuss.

---

## Communication Guidelines

### Communicating with the Instructor

My goal is to be readily available to you throughout the semester. I
can be reached by email at zeidk@umd.edu. Please **DO NOT** email me
with questions that are easily found in the syllabus or on ELMS-Canvas
(e.g., *When is this assignment due? How much is it worth?*), but
please **DO** reach out about personal, academic, and intellectual
concerns / questions.

While I will do my best to respond to emails within 24 hours, you
will more likely receive email responses from me on weekdays from
11:00 AM to 7:00 PM EST.

When constructing an email to me please put **"ENPM 818Z (Section
0101): Your Topic"** in the subject line. This will draw my attention
to your email and enable me to respond to you more quickly.

Additionally, please review *These tips for "How to email a
professor"*. By following these guidelines, you will be ensured to
receive a timely and courteous response.

Finally, if you need to discuss issues not appropriate for the
classroom and / or an email, we can arrange to talk by phone, over
Zoom, or in person. Send me an email asking for a meeting and we can
set something up.

### Announcements

I will send IMPORTANT messages, announcements, and updates through
ELMS-Canvas. To ensure you receive this information in a timely
fashion, make sure your email and announcement notifications
(including changes in assignments and / or due dates) are enabled in
ELMS-Canvas. Log into our ELMS-Canvas course site at least once every
24-hour period to check your inbox and the Announcements page.

### Names / Pronouns and Self-Identifications

The University of Maryland recognizes the importance of a diverse
student body, and we are committed to fostering inclusive and
equitable classroom environments. I invite you, if you wish, to tell
us how you want to be referred to in this class, both in terms of
your name and your pronouns (he/him, she/her, they/them, etc.). Keep
in mind that the pronouns someone uses are not necessarily indicative
of their gender identity. Visit <https://trans.umd.edu> to learn more.

Additionally, it is your choice whether to disclose how you identify
in terms of your gender, race, class, sexuality, religion, and
dis/ability, among all aspects of your identity (e.g., should it come
up in classroom conversation about our experiences and perspectives)
and should be self-identified, not presumed or imposed. I will do my
best to address and refer to all students accordingly, and I ask you
to do the same for all of your fellow Terps.

### Communicating with your Peers

With a diversity of perspectives and experience, we may find
ourselves in disagreement and / or debate with one another. As such,
it is important that we agree to conduct ourselves in a professional
manner and that we work together to foster and preserve a virtual
classroom environment in which we can respectfully discuss and
deliberate controversial questions. I encourage you to confidently
exercise your right to free speech, bearing in mind, of course, that
you will be expected to craft and defend arguments that support your
position. Keep in mind that free speech has its limit and this course
is **NOT** the space for hate speech, harassment, and derogatory
language. I will make every reasonable attempt to create an
atmosphere in which each student feels comfortable voicing their
argument without fear of being personally attacked, mocked, demeaned,
or devalued.

Any behavior (including harassment, sexual harassment, and racially
and / or culturally derogatory language) that threatens this
atmosphere will not be tolerated. Please alert me immediately if you
feel threatened, dismissed, or silenced at any point during our
semester together and / or if your engagement in discussion has been
in some way hindered by the learning environment.

### Netiquette Policy

Netiquette is the social code of online classes. Students share a
responsibility for the course's learning environment. Creating a
cohesive online learning community requires learners to support and
assist each other. To craft an open and interactive online learning
environment, communication has to be conducted in a professional and
courteous manner at all times, guided by common sense, collegiality
and basic rules of etiquette.

---

## Grading

### Grade Breakdown

| Assignment                                       | Percentage % |
| ------------------------------------------------ | ------------ |
| Final Project (GP1-GP4: 85% + Final Report: 15%)  | 80%          |
| Quizzes (5 quizzes)                               | 20%          |
| **Total**                                         | **100%**     |

### Course Assignments

#### Group Projects

The group projects are the core of this course, designed to foster
collaboration and apply course concepts to real-world scenarios.
Students work in teams of 4 to build a single, cumulative Automated
Driving System (ADS) pipeline across the semester. The project
integrates CARLA, ROS 2, and modern AV algorithms into a unified
package called `ads_pipeline`. Each team member is expected to
contribute actively to the project, ensuring equitable participation
and shared responsibility.

The Final Project grade is composed of the four group projects
(**85%**) and the Final Report (**15%**). The group projects are
cumulative — GP1 through GP4 each build on the previous, and their
percentages below are shares of the group-project portion:

1. **GP1: Sensor Suite & Data Pipeline** (3 weeks, 15% of GP grade): Spawn a multi-sensor rig in CARLA (camera + LiDAR + GNSS + IMU),
   stream all data through a ROS 2 `sensor_manager` node, and record
   synchronized rosbags. Lectures L1-L2.
2. **GP2: Perception (YOLO vs DETR)** (3 weeks, 40% of GP grade): Build a `detector_node` running YOLO and DETR on CARLA camera
   frames, compare them, and integrate BEV construction and
   segmentation into the perception package. Lectures L4-L6.
3. **GP3: Fusion & Localization** (3 weeks, 25% of GP grade): Add a
   `fusion_node` (Kalman / EKF tracker over multi-sensor inputs) and a
   `localization_node` (EKF-based pose estimate using GNSS + IMU +
   wheel odometry, with map-based correction). Lectures L3, L7.
4. **GP4: Planning & Control** (3 weeks, 20% of GP grade): Add a
   `planner_node` (A\* on the CARLA waypoint graph + re-planning), a
   `controller_node` (Pure Pursuit + PID), and a behavioral FSM. Run
   the full `ads_pipeline` end-to-end on two CARLA scenarios and
   evaluate using the provided metrics script. Lectures L8-L11.

**Final Report: Integrated ADS Pipeline** (1 week, **15% of the Final
Project grade**): After GP4 is complete, teams evaluate the full
`ads_pipeline` on instructor-provided scenarios not seen during
development (urban intersection, highway merging, pedestrian crossing,
adverse weather, construction zone) and submit a written report
documenting the system architecture, design decisions, quantitative
results (mAP, APE, route completion, collisions), and failure analysis.
Because it assesses the integrated system, it draws on Lectures L1-L14.
Due December 17.

#### Quizzes

- Quizzes provide an effective means to assess your understanding of
  the course material. They are administered at the beginning of
  class, either on Canvas or on paper, and typically last between 10
  and 20 minutes. All quizzes are conducted under closed-notes
  conditions.
- **5 quizzes** throughout the semester.
- Students registered for in-person learning must take the quizzes in
  class. Any quiz taken outside of class will not be counted, and a
  different quiz will need to be taken.

#### Participation & Engagement

Active participation and engagement are essential components of this
course. You are expected to contribute to class discussions, ask
questions, and collaborate with peers during activities. Your
involvement will not only enhance your understanding of the material
but also create a dynamic and interactive learning environment.

### Grading Assignments

All assignments will be graded according to a predetermined set of
criteria (i.e., rubric) which will be communicated to students before
the assignment is submitted.

To progress satisfactorily in this class, students need to receive
timely feedback. To that end, it is my intention to grade all
assignments within **8 days** of their due date. If an assignment is
taking longer than expected to grade, students will be informed of
when they can expect to see their grade.

### Grade Computation

All assessment scores will be posted on ELMS / Canvas. If you would
like to review any of your grades (including the exams), or have
questions about how something was scored, please email me to schedule
a time for us to meet and discuss.

It is expected that you will submit work by the deadline listed in
the syllabus and / or on ELMS-Canvas. Late work will be penalized
according to the late work policy described in the **Course Policies
and Procedures** section below.

**Grade Disputes:** I am happy to discuss any of your grades with
you, and if I have made a mistake, I will immediately correct it. Any
formal grade disputes must be submitted in writing within one week of
receiving the grade.

Final letter grades are assigned based on the percentage of total
assessment points earned. To be fair to everyone I have to establish
clear standards and apply them consistently, so please understand
that being close to a cutoff is not the same as making the cut (89.99
≠ 90.00). It would be unethical to make exceptions for some and not
others.

### Final Grade Cutoffs

| Letter Grade | Cutoff |
| ------------ | ------ |
| A+           | 97%    |
| A            | 94%    |
| A-           | 90%    |
| B+           | 87%    |
| B            | 84%    |
| B-           | 80%    |
| C+           | 77%    |
| C            | 74%    |
| C-           | 70%    |
| D+           | 67%    |
| D            | 64%    |
| D-           | 60%    |
| F            | <60%   |

---

## Course Schedule

| Week #     | Date  | Topic                                                 | Deliverable                     |
| ---------- | ----- | ----------------------------------------------------- | ------------------------------- |
| 1          | 09/03 | L1 - Course Intro, AV Landscape, Safety, CARLA        | Team Formation                  |
| 2          | 09/10 | L2 - Sensor Technologies & Calibration                | GP1 Posted                      |
| 3          | 09/17 | L3 - Probabilistic State Estimation & Fusion          | Quiz 1                          |
| 4          | 09/24 | L4 - Perception I: Object Detection (YOLO to DETR)    |                                 |
| 5          | 10/01 | L5 - Perception II: BEV, Occupancy & Segmentation     | GP1 Due, GP2 Posted             |
| 6          | 10/08 | L6 - Perception III: Tracking, Temporal & Deep Fusion | Quiz 2                          |
| 7          | 10/15 | L7 - Localization & SLAM                              |                                 |
| 8          | 10/22 | L8 - Navigation & Route Planning                      | GP2 Due, GP3 Posted             |
| 9          | 10/29 | L9 - Prediction & Behavior Modeling                   | Quiz 3                          |
| 10         | 11/05 | L10 - Motion Planning                                 |                                 |
| 11         | 11/12 | L11 - Trajectory Generation & Control                 | Quiz 4, GP3 Due, GP4 Posted     |
| 12         | 11/19 | L12 - End-to-End Driving, VLA & Imitation Learning    |                                 |
| (no class) | 11/26 | **THANKSGIVING RECESS - no class**                    |                                 |
| 13         | 12/03 | L13 - World Models & Simulation                       |                                 |
| 14         | 12/10 | L14 - System Integration, Safety & Industry Outlook   | Quiz 5, GP4 Due                 |
| 15         | 12/17 | No class - final report submission window             | Final Report Due                |

Lectures meet on **Thursdays**, 7:00 PM - 9:40 PM. The only cancelled
meeting is Thursday, November 26, which falls within the Thanksgiving
recess (Nov 25 to 29). All 14 lectures fit the remaining Thursdays, with
the final report due during the December 17 exam-period window.

**Note:** This is a tentative schedule, and subject to change as
necessary; monitor ELMS-Canvas for current deadlines. In the
unlikely event of a prolonged university closing, or an extended
absence from the university, adjustments to the course schedule,
deadlines, and assignments will be made based on the duration of the
closing and the specific dates missed.

---

## Course Policies and Procedures

The University of Maryland's conduct policy indicates that course
syllabi should refer to a webpage of course-related policies and
procedures. For a complete list of graduate course related policies,
visit the [Graduate School website](https://gradschool.umd.edu/).
Below are course-specific policies and procedures which explain how
these Graduate School policies will be implemented in this class.

### Satisfactory Performance

The Graduate School expects students to take full responsibility for
their academic work and academic progress. The student, to progress
satisfactorily, must meet all the academic requirements of this
course. Additionally, each student is expected to complete all
readings and any preparatory work before each class session, come to
class prepared to make substantive contributions to the learning
experience, and to proactively communicate with the instructor when
challenges or issues arise.

### Questions about Assignments

Please ask all questions you may have about an assignment **by 10 PM
the day before the assignment is due**. Any questions asked after
that time may not be answered in time for you to make changes to
your work.

### Late Work Policy

Assignments should be completed by the due date and time listed with
the assignment, on the syllabus, and / or in the course calendar. If
you are unable to complete an assignment by the stated due date, it
is your responsibility to contact your instructor to discuss an
extension, **at least 24 hours BEFORE the assignment is due**.
Extensions are not guaranteed, but may be granted at the
instructor's discretion.

**Assignments submitted late will receive a 10% deduction in total
grade per each calendar day late up to a maximum of three days late
(i.e., there is a maximum of a 30% grade reduction for assignments
submitted late). Work submitted more than three days late will not
receive feedback and will automatically earn a grade of zero.** If
your failure to turn your work in on time was due to a University
excused absence, please contact your instructor and make-up work
can be arranged.

### Responsible Use of Generative AI

Generative AI tools (e.g., ChatGPT, GitHub Copilot, Claude, etc.) are
becoming increasingly common in engineering education and in the
workplace. In this course, students are expected to use AI
technologies ethically and in ways that support learning, uphold
academic integrity, and align with course objectives.

#### Permitted Uses of AI Tools in This Course

Students may use generative AI tools for the following purposes:

- Brainstorming initial ideas or outlining for assignments
- Getting help understanding difficult engineering concepts (e.g.,
  asking for explanations or examples)
- Writing assistance at the sentence level (e.g., grammar or clarity
  improvements)
- Debugging support in coding assignments, provided students still
  understand and can explain their code

#### Prohibited Uses of AI Tools in This Course

Students may not use generative AI tools for:

- Completing graded assignments, problem sets, or projects unless
  explicitly permitted
- Generating solutions to coding or engineering problems without
  understanding and verifying the output
- Writing full sections of reports, papers, or lab assignments
- Submitting AI-generated work as their own without proper citation
  or instructor approval

It is the student's responsibility to make sure any use of AI aligns
with the expectations outlined above. Misuse of AI tools may
constitute academic dishonesty and will be addressed accordingly
(see section on academic integrity, below). Lastly, please become
familiar with the University-approved AI tools and university
guidelines on responsible AI use. If you are unsure whether a
particular use of AI is appropriate, please ask before proceeding.

### Academic Integrity

For this course, some of your assignments will be collected via
Turnitin on ELMS / Canvas. I have chosen to use this tool because it
can help you improve your scholarly writing and help me verify the
integrity of student work. For information about Turnitin, how it
works, and the feedback reports you may have access to, visit the
Turnitin Originality Checker for Students documentation on the
Office of Graduate Studies site.

The University's Code of Academic Integrity is designed to ensure
that the principles of academic honesty and integrity are upheld.
In accordance with this code, the University of Maryland does not
tolerate academic dishonesty. Please ensure that you fully
understand this code and its implications because all acts of
academic dishonesty will be dealt with in accordance with the
provisions of this code. All students are expected to adhere to
this Code. It is your responsibility to read it and know what it
says, so you can start your professional life on the right path.
**As future professionals, your commitment to high ethical
standards and honesty begins with your time at the University of
Maryland.**

It is important to note that course assistance websites, such as
CourseHero, or AI generated content are not permitted sources,
unless the instructor explicitly gives permission. Material taken
or copied from these sites can be deemed unauthorized material and
a violation of academic integrity. These sites offer information
that might be inaccurate or biased and most importantly, relying on
restricted sources will hamper your learning process, particularly
the critical thinking steps necessary for college-level
assignments.

Additionally, students may naturally choose to use online forums
for course-wide discussions (e.g., Group lists or chats) to discuss
concepts in the course. However, **collaboration on graded
assignments is strictly prohibited unless otherwise stated**.
Examples of prohibited collaboration include: asking classmates for
answers on quizzes or exams, asking for access codes to clicker
polls, etc. Please visit the Office of Graduate Studies' full list
of campus-wide policies and reach out if you have questions.

Finally, on each exam or assignment you must write out and sign
the following pledge:

> **"I pledge on my honor that I have not given or received any
> unauthorized assistance on this exam/assignment."**

If you ever feel pressured to comply with someone else's academic
integrity violation, please reach out to me straight away. Also,
**if you are ever unclear about acceptable levels of collaboration,
please ask!**

To help you avoid unintentional violations, the following table
lists levels of collaboration that are acceptable for each graded
exercise. Each assignment will contain more specific information
regarding acceptable levels of collaboration.

| Assignment Type | Open Notes | Read Book | Learn Online | Gather Content with AI | Ask Friends | Work in Groups |
| --------------- | :--------: | :-------: | :----------: | :--------------------: | :---------: | :------------: |
| Quizzes         | No         | Yes       | Yes          | No                     | No          | No             |
| Group Projects  | Yes        | Yes       | Yes          | Yes                    | Yes         | Yes            |

### Course Evaluation

Please submit a course evaluation through Student Feedback on Course
Experiences in order to help faculty and administrators improve
teaching and learning at Maryland. All information submitted to
Course Experiences is confidential. Campus will notify you when
Student Feedback on Course Experiences is open for you to complete
your evaluations at the end of the semester. By completing all of
your evaluations each semester, you will have the privilege of
accessing through Testudo the evaluation reports for the thousands
of courses for which 70% or more students submitted their
evaluations.

### Religious Observance

It is the student's responsibility to inform the instructor of any
intended absences for religious observances in advance. Notice
should be provided as soon as possible but no later than the end
of the schedule adjustment period.

### Copyright Notice

Course materials are copyrighted and may not be reproduced for
anything other than personal use without written permission.

---

## Tips for Succeeding in this Course

1. **Participate.** I invite you to engage deeply, ask questions, and
   talk about the course content with your classmates. You can learn
   a great deal from discussing ideas and perspectives with your
   peers and professor. Participation can also help you articulate
   your thoughts and develop critical thinking skills.
2. **Manage your time.** Students are often very busy, and I
   understand that you have obligations outside of this class.
   However, students do best when they plan adequate time that is
   devoted to course work. Block your schedule and set aside plenty
   of time to complete assignments including extra time to handle
   any technology-related problems. **CARLA in particular can be
   resource-intensive; budget time for setup and rendering.**
3. **Login regularly.** I recommend that you log in to ELMS-Canvas
   several times a week to view announcements, discussion posts,
   and replies to your posts. You may need to log in multiple times
   a day when group submissions are due.
4. **Do not fall behind.** This class moves at a quick pace and each
   week builds on the previous content (the GPs are cumulative:
   GP2 depends on GP1, GP3 depends on GP2, GP4 depends on GP3). If
   you feel you are starting to fall behind, check in with the
   instructor as soon as possible so we can troubleshoot together.
5. **Use ELMS-Canvas notification settings.** Pro tip! Canvas
   ELMS-Canvas can ensure you receive timely notifications in your
   email or via text. Be sure to enable announcements to be sent
   instantly or daily.
6. **Ask for help if needed.** If you need help with ELMS-Canvas or
   other technology, contact IT Support. If you are struggling with
   a course concept, reach out to me and your classmates for
   support.

---

## Student Resources and Services

Taking personal responsibility for your learning means acknowledging
when your performance does not match your goals and doing something
about it. I hope you will come talk to me so that I can help you find
the right approach to success in this course, and I encourage you to
visit the Counseling Center's Academic Resources to learn more about
the wide range of resources available to you. Below are some
additional resources and services commonly used by graduate students.
For a more comprehensive list, please visit the Graduate School's
Campus Resources Page.

### Accessibility and Disability Services

The University of Maryland is committed to creating and maintaining a
welcoming and inclusive educational, working, and living environment
for people of all abilities. The University of Maryland is also
committed to the principle that no qualified individual with a
disability shall, on the basis of disability, be excluded from
participation in or be denied the benefits of the services, programs,
or activities of the University, or be subjected to discrimination.
The Accessibility & Disability Service (ADS) provides reasonable
accommodations to qualified individuals to provide equal access to
services, programs and activities. ADS cannot assist retroactively,
so it is generally best to request accommodations several weeks
before the semester begins or as soon as a disability becomes known.
Any student who needs accommodations should contact me as soon as
possible so that I have sufficient time to make arrangements.

For assistance in obtaining an accommodation, contact Accessibility
and Disability Service at 301-314-7682, or email them at
adsfrontdesk@umd.edu. Information about sharing your accommodations
with instructors, note-taking assistance and more is available from
the Counseling Center.

### Writing Center

Everyone can use some help sharpening their communication skills
(and improving their grade) by visiting The Graduate School's Writing
Center and schedule an appointment with them. Additionally,
international graduate students may want to take advantage of the
Graduate School's free English Editing for International Graduate
Students (EEIGS) program.

### Health Services

The University offers a variety of physical and mental health
services to students. If you are feeling ill or need non-emergency
medical attention, please visit the University Health Center.

If you feel it would be helpful to have someone to talk to, visit
UMD's Counseling Center or one of the many other mental health
resources on campus.

### Notice of Mandatory Reporting

Notice of mandatory reporting of sexual assault, sexual harassment,
interpersonal violence, and stalking: As a faculty member, I am
designated as a "Responsible University Employee," and I must report
all disclosures of sexual assault, sexual harassment, interpersonal
violence, and stalking to UMD's Title IX Coordinator per University
Policy on Sexual Harassment and Other Sexual Misconduct.

If you wish to speak with someone confidentially, please contact one
of UMD's confidential resources, such as CARE to Stop Violence
(located on the Ground Floor of the Health Center) at 301-741-3442
or the Counseling Center (located at the Shoemaker Building) at
301-314-7651.

You may also seek assistance or supportive measures from UMD's Title
IX Coordinator, Angela Nastase, by calling 301-405-1142, or emailing
titleIXcoordinator@umd.edu. To view further information on the
above, please visit the Office of Civil Rights and Sexual Misconduct.

### Basic Needs Security

If you have difficulty affording groceries or accessing sufficient
food to eat every day, or lack a safe and stable place to live,
please visit UMD's Division of Student Affairs website for
information about resources the campus offers you and let me know if
I can help in any way.

### Veteran Resources

UMD provides some additional supports to our student veterans. You
can access those resources at the office of Veteran Student Life and
the Counseling Center. Veterans and active-duty military personnel
with special circumstances (e.g., upcoming deployments, drill
requirements, disabilities) are welcome and encouraged to
communicate these, in advance if possible, to the instructor.

---

*Last updated: 2026-05-25*
