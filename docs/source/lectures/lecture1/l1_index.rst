====================================================
L1: Course Introduction & AV Landscape
====================================================

Overview
--------

This lecture introduces ENPM818Z and the automated vehicle landscape. It
covers the vocabulary the rest of the course is built on -- the dynamic
driving task, the DDT fallback, the minimal risk condition and the operational
design domain -- and the SAE J3016 levels, which classify **features by who is
responsible**, not vehicles by capability.

It then walks the seven-stage path an automated driving system takes from
hazard analysis, through a safety case, to a deployment permit, and closes
with two real-world incidents that you diagnose *before* the investigators'
findings are revealed. The course structure is covered alongside.

**CARLA itself is introduced in L2**, not here -- but you must have it
installed before that lecture, so start the download this week.

.. important::

   Development environment setup (Ubuntu, ROS 2, VS Code, Git, shell
   basics) is **pre-read material** and is not covered in lecture. Work
   through
   :doc:`Pre-Read: Development Environment </preread/dev-environment>`
   before this class, then install CARLA with the
   :doc:`setup guide </carla/carla>`.

.. admonition:: Deck version
   :class: note

   These pages accompany the **L1 slide deck v1.0**. Where the slides and
   these pages disagree, these pages are authoritative. See the
   :doc:`course changelog </changelog/changelog>` for what changed and when.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Describe the course structure, the cumulative project sequence, and the
  grading policies.
- Define the **Dynamic Driving Task (DDT)**, the **DDT fallback**, the
  **Minimal Risk Condition (MRC)** and the **Operational Design Domain
  (ODD)**, and distinguish an **ADAS** from an **ADS**.
- Classify a driving automation feature by its SAE J3016 level from a
  description of its behavior and its operating limits.
- Describe the current state of commercial deployment and the technical
  challenges that remain unsolved.
- Outline the path an ADS takes from hazard analysis, through a safety case,
  to a deployment permit.
- Distinguish a malfunction hazard (ISO 26262) from a hazard that occurs with
  no malfunction (ISO 21448 / SOTIF), and say what follows for how each must
  be tested.
- Diagnose which module of an ADS pipeline failed in a real-world incident,
  and argue whether fixing that module alone would have been sufficient.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l1_lecture
   l1_exercises
   l1_quiz
   l1_references


Next Steps
----------

.. important::

   The :doc:`exercises <l1_exercises>` and the :doc:`quiz <l1_quiz>` for this
   lecture are **not submitted and not graded**. They are there so you can
   check your own understanding before the first graded quiz.

- In the next lecture, we will cover **Sensor Technologies & Calibration**:

  - Camera, LiDAR, RADAR, IMU, and GNSS systems -- what each one measures and
    how each one lies.
  - Intrinsic and extrinsic calibration.
  - Sensor placement, coverage, and complementarity.
  - **Introduction to CARLA**: client-server architecture, the course ROS 2
    bridge, the limits of simulation fidelity, and your first sensor suite in
    simulation.

- **Install CARLA 0.9.16** following the :doc:`setup guide </carla/carla>`.
  **You will need it running next week**, so start now -- the download alone
  is substantial.
- Review camera calibration and the pinhole model.
- Complete the :doc:`L1 exercises <l1_exercises>` and the
  :doc:`self-check quiz <l1_quiz>`.
- **Due in Week 3**: the **setup milestone** -- CARLA running, ROS 2 workspace
  built, sensors publishing. Individual, pass/fail. Teams are formed the same
  evening, GP1 is posted, and each team writes its charter.
- **Reading**: `SAE J3016 <https://www.sae.org/standards/j3016_202104-taxonomy-definitions-terms-related-driving-automation-systems-road-motor-vehicles/>`_
  (at least the level definitions and the ODD discussion) and
  `NIST IR 8527 <https://doi.org/10.6028/NIST.IR.8527>`_ as a map of the
  standards landscape -- free to download.

.. warning::

   **There is no TA this semester.** If your environment is not working, email
   the instructor **this week** -- not the week it is due.
