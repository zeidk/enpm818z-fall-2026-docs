ENPM818Z — On-Road Automated Vehicles
=====================================

Course Description
------------------

ENPM818Z provides a deep dive into the core technical and technological
components of automated passenger vehicles for on-road applications. Students
explore the essential systems that enable self-driving capabilities, including
perception, sensor fusion, localization, motion planning, and control.

The course emphasizes a hands-on approach using the **CARLA** simulation
environment, where students develop and test advanced driving algorithms in
simulated urban and highway scenarios. Core topics include:

- Multi-sensor perception (LiDAR, RADAR, cameras, IMU, GNSS)
- Real-time data fusion and SLAM-based localization
- Motion planning and trajectory optimization
- AI-driven decision-making for behavior prediction and control
- End-to-end driving and foundation models
- System integration and simulation-based validation

By the end of the semester, students will have designed, implemented, and
tested components of an **automated driving system (ADS)**, gaining the
technical foundation required for careers in robotics, automated vehicle
engineering, and intelligent transportation systems.


Prerequisites
--------------

Students enrolling in ENPM818Z must have:

- **ENPM605** (Python Applications for Robotics) or equivalent -- strong
  Python programming skills and familiarity with ROS 2.
- **ENPM673** (Perception for Autonomous Robotics) or equivalent --
  basic understanding of computer vision and sensor processing.
- Proficiency in **ROS 2** for developing and testing robotic systems.
- Basic understanding of robotics, linear algebra, and probability.
- Familiarity with simulation environments such as CARLA (recommended but
  not required).

.. note::

   ENPM605 covers Python fundamentals, OOP, and ROS 2 development, which
   are essential for all group projects in this course. Students without
   ROS 2 experience should complete the
   `ROS 2 Tutorials <https://docs.ros.org/en/humble/Tutorials.html>`_
   before the semester begins.


Learning Outcomes
-----------------

Upon successful completion of this course, students will be able to:

- **Understand Core AV Technologies:** Explain how perception, localization,
  motion planning, and control interact within an ADS.
- **Implement Multi-Sensor Fusion:** Combine data from LiDAR, RADAR, camera,
  IMU, and GNSS sensors to improve perception accuracy.
- **Train and Deploy AI Models:** Fine-tune CNN-based (YOLO) and
  transformer-based (DETR) object detectors on driving data.
- **Develop Localization and Mapping Systems:** Implement EKF-based
  localization and evaluate accuracy under dynamic conditions.
- **Apply Motion Planning Techniques:** Create safe and efficient motion
  planners and controllers for urban and highway driving.
- **Design AI-Driven Decision Systems:** Apply machine learning or rule-based
  methods for decision-making in traffic scenarios.
- **Integrate and Validate AV Systems:** Use CARLA simulation to integrate
  multiple modules into a working ADS pipeline.
- **Analyze System Performance:** Evaluate robustness and safety using
  simulation metrics and performance indicators.


How to Navigate This Website
-----------------------------

This website contains all course materials for ENPM818Z. Use the **top
navigation bar** to access the main sections:

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Changelog
      :class-card: sd-border-secondary

      Track all updates to the course documentation. Check here after each
      lecture for newly released materials.

   .. grid-item-card:: Syllabus
      :class-card: sd-border-secondary

      Course schedule, grade breakdown, group project timeline, and required
      software. **Start here** to understand the course structure.

   .. grid-item-card:: CARLA Simulator
      :class-card: sd-border-secondary

      Setup guides for CARLA 0.9.16 on Ubuntu 22.04 (native) or Ubuntu
      24.04 (Docker). Includes Python API reference, CLI options, and
      troubleshooting.

   .. grid-item-card:: Lectures
      :class-card: sd-border-secondary

      13 lectures covering the full AV stack. Each lecture includes:

      - **Lecture notes** -- Detailed content with code examples, diagrams,
        and tables.
      - **Quiz** -- Practice questions (multiple choice, true/false, essay)
        with **hidden answers** you can reveal by clicking the dropdown.
      - **References** -- Papers, tools, and further reading.

   .. grid-item-card:: Final Project
      :class-card: sd-border-secondary

      Four cumulative group projects (GP1--GP4) that build a complete ADS
      pipeline in CARLA. Each GP includes detailed instructions, provided
      scripts, grading rubrics, and submission checklists.

   .. grid-item-card:: Glossary
      :class-card: sd-border-secondary

      70+ AV-specific terms organized alphabetically. Use this as a quick
      reference while studying or working on projects.

.. tip::

   **Practice quizzes** are available at the end of each lecture. Click the
   dropdown below each question to reveal the answer and explanation. These
   are not graded -- use them to test your understanding before in-class
   quizzes.


Course Resources
----------------

**Required Software and Tools**

- Ubuntu 22.04 LTS or 24.04 LTS
- CARLA Simulator 0.9.16
- ROS 2 (Humble or Jazzy)
- Python 3.10+ with ``numpy``, ``matplotlib``, ``opencv-python``, and
  ``carla`` packages
- Visual Studio Code or preferred IDE
- Git and GitHub for version control

**Hardware Recommendations**

- GPU: NVIDIA GTX 1060 (1070+ recommended)
- RAM: 8 GB minimum (16 GB+ preferred)
- CPU: Quad-core processor
- 20 GB free storage for CARLA and datasets


Course Structure
----------------

ENPM818Z combines lectures with intensive, hands-on programming sessions in
CARLA. Each week builds on prior material -- progressing from single-sensor
processing to full system integration. Students complete four group projects
(GP1--GP4) that cumulatively build a functional ADS pipeline.


Evaluation
----------

.. list-table::
   :header-rows: 1
   :widths: 60 20
   :class: compact-table

   * - Component
     - Percentage
   * - Final Project (GP1--GP4 + Final Report)
     - 80%
   * - Quizzes (5)
     - 20%
   * - **Total**
     - **100%**

Late submissions incur a 10% deduction per day (maximum 3 days). Beyond
3 days, submissions receive zero credit.


.. toctree::
   :hidden:
   :maxdepth: 3
   :titlesonly:

   changelog/changelog
   syllabus/index
   carla/carla
   lectures/index
   assignments/index
   glossary/glossary
