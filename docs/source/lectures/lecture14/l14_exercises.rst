====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 14. Exercises cover system integration, safety standards,
real-time constraints, and cybersecurity.


.. dropdown:: Exercise 1 -- Latency Budget Analysis
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Reason about end-to-end latency requirements and the consequences
   of budget overruns.


   .. raw:: html

      <hr>


   **Specification**

   The ADS latency budget is **100 ms** end-to-end:

   .. list-table::
      :widths: 40 20 40
      :header-rows: 1
      :class: compact-table

      * - Module
        - Budget (ms)
        - Notes
      * - Sensor capture + preprocessing
        - 15
        -
      * - Perception (detection + tracking)
        - 40
        -
      * - Prediction
        - 15
        -
      * - Planning
        - 20
        -
      * - Control + CAN bus
        - 10
        -

   1. If perception takes **60 ms** instead of 40 ms, which module(s)
      must compensate? Is this feasible without degrading output
      quality?
   2. At **60 km/h**, how far does the vehicle travel during the full
      100 ms latency? During a 200 ms latency?
   3. Why is the control module given the **smallest** budget?
   4. Name **one technique** to reduce perception latency without
      changing the model architecture.

   **Deliverable**

   Written answers with distance calculations shown.


.. dropdown:: Exercise 2 -- ASIL Classification
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice assigning ASIL levels using Hazard Analysis and Risk
   Assessment (HARA).


   .. raw:: html

      <hr>


   **Specification**

   For each failure mode, assign **Severity** (S0--S3), **Exposure**
   (E1--E4), **Controllability** (C0--C3), and the resulting **ASIL**
   (QM, A, B, C, or D).

   .. list-table::
      :widths: 30 12 12 12 12
      :header-rows: 1
      :class: compact-table

      * - Hazard
        - S
        - E
        - C
        - ASIL
      * - Steering locks at 120 km/h on highway
        -
        -
        -
        -
      * - Camera freezes for 500 ms in a parking lot at 5 km/h
        -
        -
        -
        -
      * - False positive pedestrian causes unnecessary stop on road
        -
        -
        -
        -
      * - LiDAR returns no points for 2 s at 80 km/h
        -
        -
        -
        -
      * - Incorrect lane detection on a rural road at 30 km/h
        -
        -
        -
        -

   For each row, write a **one-sentence justification** for your S, E,
   and C ratings.

   **Deliverable**

   Completed table with justifications.


.. dropdown:: Exercise 3 -- ROS 2 QoS Configuration
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Configure ROS 2 Quality of Service policies for safety-critical
   perception data and design a watchdog strategy.


   .. raw:: html

      <hr>


   **Specification**

   A perception node publishes detections at 10 Hz. A planning node
   subscribes.

   1. Should the **reliability** policy be ``RELIABLE`` or
      ``BEST_EFFORT``? Justify for safety-critical data.
   2. What **history depth** is appropriate? What happens if the
      planner is slower than the publisher?
   3. Configure a QoS profile with a **150 ms deadline**:

      .. code-block:: python

         from rclpy.qos import QoSProfile, ReliabilityPolicy
         from rclpy.qos import HistoryPolicy, DurabilityPolicy
         from rclpy.duration import Duration

         perception_qos = QoSProfile(
             reliability=...,
             durability=...,
             history=...,
             depth=...,
             deadline=Duration(seconds=0, nanoseconds=150_000_000),
         )

      Fill in the ``...`` values and explain each choice.

   4. Design a **watchdog strategy**: if the deadline is missed **three
      times consecutively**, what should the system do? Write
      pseudocode for the watchdog callback.

   **Deliverable**

   Completed QoS code, explanation of each setting, and watchdog
   pseudocode.


.. dropdown:: Exercise 4 -- Cybersecurity Threat Analysis
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Perform a simplified TARA (Threat Analysis and Risk Assessment)
   for common ADS attack surfaces.


   .. raw:: html

      <hr>


   **Specification**

   For each attack surface, describe a concrete threat, rate its
   impact, and propose a mitigation.

   .. list-table::
      :widths: 20 25 15 40
      :header-rows: 1
      :class: compact-table

      * - Attack Surface
        - Threat Example
        - Impact
        - Mitigation
      * - Camera input
        -
        -
        -
      * - V2X communication
        -
        -
        -
      * - OTA software update
        -
        -
        -
      * - LiDAR sensor
        -
        -
        -
      * - GNSS signal
        -
        -
        -

   For each row:

   1. Describe a **specific attack** (e.g., adversarial patch on stop
      sign, GPS spoofing).
   2. Rate impact as **Low**, **Medium**, or **High**.
   3. Propose one concrete **mitigation strategy**.

   **Deliverable**

   Completed TARA table with 1--2 sentence descriptions per cell.


.. dropdown:: Exercise 5 -- Integration Pre-Flight Checklist
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Create a systematic verification checklist for running the complete
   GP1--GP4 pipeline in CARLA.


   .. raw:: html

      <hr>


   **Specification**

   You are preparing to run a full ADS demonstration. Create a
   pre-flight checklist covering five subsystems. For each check,
   specify the **ROS 2 command** you would use.

   1. **Sensor verification** (3 checks):

      - All sensors publishing at expected rates?
      - Data formats match subscriber expectations?
      - Calibration parameters loaded?

   2. **Perception verification** (3 checks):

      - Detection node running and publishing?
      - Confidence threshold configured?
      - Inference latency within budget?

   3. **Localization verification** (3 checks):

      - EKF converged before motion?
      - GNSS fix acquired?
      - Odometry drift within limits?

   4. **Planning & control verification** (3 checks):

      - Path planned and published?
      - Controller gains loaded from config?
      - Emergency stop functional?

   5. **Safety verification** (3 checks):

      - FSM starts in safe state?
      - Maximum speed limit enforced?
      - Watchdog monitoring all critical nodes?

   Format as a table:

   .. list-table::
      :widths: 25 40 35
      :header-rows: 1
      :class: compact-table

      * - Subsystem
        - Check
        - ROS 2 Command
      * - Sensors
        - Camera publishing at 10 Hz?
        - ``ros2 topic hz /carla/camera/rgb/image``
      * - ...
        - ...
        - ...

   **Deliverable**

   Completed checklist table with 15 entries (3 per subsystem) and
   the exact ROS 2 command for each.
