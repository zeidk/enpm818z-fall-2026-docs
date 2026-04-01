====================================================
Lecture
====================================================


AV System Architecture: From Components to a Complete Stack
------------------------------------------------------------

A production autonomous vehicle is not a collection of independent algorithms
-- it is a tightly integrated real-time system where every component must
interoperate reliably, safely, and within strict timing constraints.

The Full Stack Overview
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ┌─────────────────── SENSOR LAYER ──────────────────────┐
   │  Cameras · LiDAR · Radar · IMU · GNSS/RTK · Ultrasonic│
   └───────────────────────┬───────────────────────────────┘
                           │ raw data (< 5 ms latency)
   ┌───────────────────────▼───────────────────────────────┐
   │              PERCEPTION MODULE                        │
   │  Object detection · Tracking · Segmentation · BEV     │
   └───────────────────────┬───────────────────────────────┘
                           │ object lists, occupancy grids
   ┌───────────────────────▼───────────────────────────────┐
   │             PREDICTION MODULE                         │
   │  Agent trajectory forecasting · Behavior classification│
   └───────────────────────┬───────────────────────────────┘
                           │ predicted trajectories
   ┌───────────────────────▼───────────────────────────────┐
   │             PLANNING MODULE                           │
   │  Route planning · Behavior planning · Motion planning  │
   └───────────────────────┬───────────────────────────────┘
                           │ planned trajectory
   ┌───────────────────────▼───────────────────────────────┐
   │              CONTROL MODULE                           │
   │  Trajectory tracking (MPC/PurePursuit) · PID control  │
   └───────────────────────┬───────────────────────────────┘
                           │ actuator commands
   ┌───────────────────────▼───────────────────────────────┐
   │          VEHICLE PLATFORM (CAN bus / Ethernet)        │
   │  Steer-by-wire · Throttle-by-wire · Brake-by-wire     │
   └───────────────────────────────────────────────────────┘

Data Flow Rates
~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 25 45
   :header-rows: 1
   :class: compact-table

   * - Module Interface
     - Typical Rate
     - Notes
   * - Camera → Perception
     - 30--60 FPS per camera
     - 6-8 cameras × up to 4 MB/frame
   * - LiDAR → Perception
     - 10--20 Hz
     - 100K--500K points per sweep
   * - Perception → Prediction
     - 10--20 Hz
     - Object lists: hundreds of bytes per object
   * - Prediction → Planning
     - 10 Hz
     - Trajectory samples per agent
   * - Planning → Control
     - 10--50 Hz
     - Waypoint list with velocity profile
   * - Control → Actuators
     - 100--500 Hz
     - Steer, throttle, brake commands via CAN


Middleware: ROS 2 and DDS
--------------------------

ROS 2 (Robot Operating System 2) is the industry-standard middleware framework
for autonomous vehicles in research and increasingly in production.

Why ROS 2 for AVs?
~~~~~~~~~~~~~~~~~~~

ROS 2 was designed specifically to address the limitations of ROS 1 in
real-time, safety-critical applications:

.. list-table:: ROS 1 vs. ROS 2
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - Feature
     - ROS 1
     - ROS 2
   * - **Middleware**
     - Custom TCPROS
     - DDS (industrial standard)
   * - **Real-time support**
     - Limited
     - RTOS support, DDS QoS
   * - **Discovery**
     - Requires rosmaster
     - Distributed, no single point of failure
   * - **Security**
     - None
     - DDS-Security (SROS 2)
   * - **Multi-robot**
     - Complex
     - Native with DDS namespacing

DDS: The Communication Foundation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Data Distribution Service (DDS)** is the OASIS standard for real-time
publish-subscribe communication used by ROS 2. It provides:

- **Publish-subscribe decoupling** -- Publishers and subscribers are unaware
  of each other; they communicate through named topics.
- **Quality of Service (QoS) policies** -- Configurable parameters that
  determine how messages are delivered.
- **Distributed discovery** -- No central broker; nodes discover each other
  automatically on the network.

Key QoS Policies for AV Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 30 50
   :header-rows: 1
   :class: compact-table

   * - QoS Policy
     - Options
     - AV Application
   * - **Reliability**
     - BEST_EFFORT, RELIABLE
     - Sensor streams: BEST_EFFORT (drop old frames). Commands: RELIABLE.
   * - **Durability**
     - VOLATILE, TRANSIENT_LOCAL
     - Static maps: TRANSIENT_LOCAL (new subscribers get last map).
   * - **Deadline**
     - Duration
     - Perception output: 100 ms deadline. Control: 10 ms deadline.
   * - **History**
     - KEEP_LAST(N), KEEP_ALL
     - Camera: KEEP_LAST(1). Diagnostics: KEEP_LAST(100).

.. code-block:: python

   # ROS 2: publishing perception output with strict QoS
   import rclpy
   from rclpy.node import Node
   from rclpy.qos import QoSProfile, ReliabilityPolicy, DeadlinePolicy
   from vision_msgs.msg import Detection3DArray
   from rclpy.duration import Duration

   class PerceptionNode(Node):
       def __init__(self):
           super().__init__("perception_node")
           qos = QoSProfile(
               reliability=ReliabilityPolicy.RELIABLE,
               depth=10,
               deadline=Duration(nanoseconds=100_000_000),  # 100 ms
           )
           self.pub = self.create_publisher(Detection3DArray,
                                            "/perception/detections", qos)


Real-Time Constraints
----------------------

Autonomous driving is a **hard real-time** application: missing a deadline
can cause a safety failure (collision). Understanding timing budgets is
essential for system integration.

Latency Budget
~~~~~~~~~~~~~~

The latency budget defines how much time each module has to process its
inputs and produce outputs. A typical 100 ms end-to-end budget (supporting
10 Hz planning) is allocated as follows:

.. list-table::
   :widths: 35 20 45
   :header-rows: 1
   :class: compact-table

   * - Module
     - Budget
     - Notes
   * - Sensor data acquisition + DMA
     - 5 ms
     - Hardware-level
   * - Sensor preprocessing (undistortion, sync)
     - 10 ms
     - GPU kernel
   * - Perception (detection + tracking)
     - 40 ms
     - Dominant consumer
   * - Prediction
     - 15 ms
     - Transformer inference
   * - Motion planning
     - 20 ms
     - Lattice or optimization-based
   * - Control computation
     - 5 ms
     - MPC or PID
   * - CAN bus command transmission
     - 5 ms
     - Hardware fixed
   * - **Total**
     - **100 ms**
     -

Scheduling and Priorities
~~~~~~~~~~~~~~~~~~~~~~~~~~

Real-time scheduling on Linux is managed via the ``SCHED_FIFO`` or
``SCHED_RR`` policies with priority levels:

.. code-block:: bash

   # Run a ROS 2 node with real-time scheduling priority
   sudo chrt -f 90 ros2 run control control_node

   # Or configure in the node's launch file using executor priority

- **Priority 99 (highest)**: Hardware interrupt handlers (CAN, IMU).
- **Priority 90**: Control module (must respond within 5 ms).
- **Priority 80**: Perception module GPU kernels.
- **Priority 70**: Planning.
- **Priority 50**: Prediction, localization.
- **Priority 10 (lowest)**: Logging, visualization, diagnostics.

Deadline Monitoring and Watchdogs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every safety-critical module must be monitored by a **watchdog** that
declares a system fault if a deadline is missed:

.. admonition:: Safety Requirement
   :class: warning

   If the control module does not receive a valid planned trajectory within
   its deadline, the watchdog must trigger a **Minimal Risk Condition (MRC)**:
   the vehicle decelerates smoothly to a stop at the side of the road.


ISO 26262: Functional Safety
-----------------------------

ISO 26262 is the automotive functional safety standard for electrical and
electronic systems. It applies to all AV components that can contribute to
safety hazards if they fail.

Automotive Safety Integrity Levels (ASIL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ASIL classifies the severity of safety risks on a scale from A (lowest) to D
(highest) based on three factors:

.. math::

   \text{ASIL} = f(\text{Severity} \times \text{Exposure} \times \text{Controllability})

.. list-table::
   :widths: 15 25 20 40
   :header-rows: 1
   :class: compact-table

   * - ASIL
     - Example AV System
     - Max PFH
     - Development Requirements
   * - **QM**
     - Cabin lighting
     - None
     - Standard quality management
   * - **ASIL A**
     - Windshield wiper
     - 10\ :sup:`-6` /h
     - Basic safety measures
   * - **ASIL B**
     - Electric power steering assist
     - 10\ :sup:`-7` /h
     - Moderate testing and analysis
   * - **ASIL C**
     - Automatic emergency braking
     - 10\ :sup:`-8` /h
     - Formal verification required
   * - **ASIL D**
     - Brake-by-wire, steer-by-wire
     - 10\ :sup:`-9` /h
     - Highest rigor; independent review

The V-Model Development Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ISO 26262 mandates the **V-model** development process, ensuring that each
design stage has a corresponding testing stage:

.. code-block:: text

   System Requirements ─────────────────────── System Testing
         │                                         ▲
   Hardware / Software Arch. ────────── Integration Testing
         │                                    ▲
   Software Design ──────────── Module Testing
         │                           ▲
   Implementation ──── Unit Testing

Functional Safety Concept
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The safety lifecycle begins with a **Hazard Analysis and Risk Assessment
(HARA)**, which identifies all foreseeable hazardous events and assigns an
ASIL to each. For example:

.. list-table::
   :widths: 40 15 15 15 15
   :header-rows: 1
   :class: compact-table

   * - Hazardous Event
     - Severity
     - Exposure
     - Controllability
     - ASIL
   * - Unintended steering while driving at highway speed
     - S3 (fatal)
     - E4 (frequent)
     - C0 (uncontrollable)
     - D
   * - Incorrect speed displayed on HMI
     - S1 (minor)
     - E4
     - C3 (easily controllable)
     - QM
   * - Incorrect object detection causing emergency brake
     - S2 (serious)
     - E3
     - C2 (normally controllable)
     - B


ISO 21448: Safety of the Intended Functionality (SOTIF)
---------------------------------------------------------

ISO 21448 (SOTIF) addresses a class of hazards that ISO 26262 does not cover:
situations where the system operates **as designed** but still produces an
unsafe outcome.

The SOTIF Space
~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * - Zone
     - Description
     - Example
   * - **Known safe**
     - Known scenarios, system performs safely
     - Highway driving in clear weather
   * - **Known unsafe**
     - Known scenarios where system fails
     - Heavy snow occludes LiDAR
   * - **Unknown safe**
     - Unknown scenarios, system performs safely
     - Rare but benign edge cases
   * - **Unknown unsafe**
     - Unknown scenarios where system fails
     - Edge cases not yet discovered

The goal of SOTIF validation is to reduce the "unknown unsafe" zone through
systematic exploration (simulation, real-world testing, formal analysis).

SOTIF in Practice
~~~~~~~~~~~~~~~~~~

- **Sensor limitation analysis** -- Characterize sensor performance bounds
  (minimum detection distance in fog, false positive rate from sun glare).
- **Trigger condition enumeration** -- Systematically identify scenarios that
  can trigger performance limitations.
- **Coverage metric** -- Define a quantitative metric for scenario coverage
  and demonstrate that the unknown unsafe space has been sufficiently reduced.

.. admonition:: SOTIF and End-to-End Models
   :class: note

   Applying SOTIF to end-to-end models is particularly challenging because
   the trigger conditions for neural network failures are not easily enumerable
   from the model's architecture. This is an active research area in 2026.


UNECE Global Technical Regulation on ADS (January 2026)
---------------------------------------------------------

The **UNECE Global Technical Regulation (GTR) on Automated Driving Systems**,
approved in January 2026, is the first international safety framework for
autonomous driving.

Key Features
~~~~~~~~~~~~

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Safety Case Approach
      :class-card: sd-border-primary

      Rather than prescribing specific technical requirements, the GTR requires
      manufacturers to construct and maintain a **safety case** -- a structured
      argument with evidence that the ADS is acceptably safe for its ODD.

   .. grid-item-card:: ODD Documentation
      :class-card: sd-border-primary

      Manufacturers must formally document the ADS's Operational Design Domain
      and demonstrate that all safety requirements are met within that ODD.

   .. grid-item-card:: Performance Monitoring
      :class-card: sd-border-primary

      The GTR requires ongoing post-deployment performance monitoring and
      safety case updates as the system accumulates operational experience.

   .. grid-item-card:: Global Harmonization
      :class-card: sd-border-primary

      The GTR is adopted by UNECE member states (including EU, Japan, South
      Korea), representing the first step toward international consistency in
      AV regulation. Final adoption is expected mid-2026.

.. note::

   The US (NHTSA) and China are not UNECE member states but are closely
   monitoring the GTR as they develop their own national frameworks. The US
   still lacks federal AV legislation as of March 2026.


Cybersecurity: ISO/SAE 21434
-----------------------------

Autonomous vehicles are networked computers on wheels -- and therefore
significant cybersecurity targets.

Attack Surfaces
~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Sensor Spoofing

      - **LiDAR spoofing** -- Firing laser pulses at an AV's LiDAR sensor to
        inject phantom objects or remove real obstacles from the point cloud.
      - **GPS spoofing** -- Broadcasting false GPS signals to mislocalize the
        vehicle.
      - **Camera adversarial attacks** -- Applying specially crafted stickers to
        stop signs or lane markings that fool CNN-based perception.

   .. tab-item:: Communication Attacks

      - **V2X man-in-the-middle** -- Intercepting and modifying V2X messages
        to provide false traffic or hazard information.
      - **CAN bus injection** -- If physical access is obtained, injecting
        malicious CAN messages to override vehicle actuators.
      - **OTA update hijacking** -- Compromising the over-the-air update
        channel to install malicious software.

   .. tab-item:: Backend Attacks

      - **Fleet management server compromise** -- Attacking the cloud servers
        that push map updates or planner versions to the vehicle fleet.
      - **Data poisoning** -- Injecting adversarial data into the fleet's
        training pipeline to degrade the next model version.

ISO/SAE 21434 Framework
~~~~~~~~~~~~~~~~~~~~~~~~

ISO/SAE 21434 (Road Vehicles -- Cybersecurity Engineering) defines the
processes and requirements for managing cybersecurity throughout the vehicle
lifecycle:

1. **Threat Analysis and Risk Assessment (TARA)** -- Enumerate threat actors,
   attack vectors, and potential impacts. Assign a **CSMS attack feasibility**
   rating and risk level.
2. **Cybersecurity Goals** -- Define cybersecurity requirements for each
   identified risk.
3. **Implementation** -- Apply controls: encryption (TLS 1.3 for V2X),
   code signing (OTA updates), hardware security modules (HSM) for key storage.
4. **Post-deployment monitoring** -- Continuous vulnerability monitoring and
   incident response.

Secure Communication
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   V2X Message                     Authenticated with:
   ─────────────────────────────────────────────────
   Basic Safety Message (BSM)  → IEEE 1609.2 certificates + ECDSA
   Service Advertisement       → ETSI ITS Security
   OTA Update Payload          → Code signing (RSA-4096 or ECDSA P-384)
   Sensor data (internal LAN)  → TLS 1.3 or DDS-Security


V2X and Connected Vehicles
---------------------------

Vehicle-to-Everything (V2X) communication extends AV perception beyond the
vehicle's own sensors by sharing information with other vehicles, infrastructure,
and cloud services.

V2X Communication Standards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: DSRC (802.11p)

      - **Technology**: IEEE 802.11p (Wi-Fi variant) in the 5.9 GHz band.
      - **Latency**: 2--20 ms (very low).
      - **Range**: 300--1000 m.
      - **Status**: Deployed in some EU infrastructure; being phased out in
        the US in favor of C-V2X.
      - **Weakness**: Requires dedicated DSRC hardware; limited cellular
        network integration.

   .. tab-item:: C-V2X (Cellular V2X)

      - **Technology**: 3GPP LTE-V2X (Release 14) and NR-V2X (5G, Release 16).
      - **Latency**: 3--20 ms (PC5 direct) or 10--50 ms (Uu cellular).
      - **Range**: 500--2000 m.
      - **Status**: Dominant standard in China; mandated in Europe (ITS-G5
        and C-V2X coexistence); growing in US.
      - **Advantage**: Integrates with cellular network for wide-area
        services (HD map updates, traffic optimization).

Cooperative Perception
~~~~~~~~~~~~~~~~~~~~~~~

The most transformative V2X application for ADS is **cooperative perception**:
multiple vehicles and roadside units share sensor data to create a collective
perception of the environment that exceeds what any single vehicle can see.

.. code-block:: text

   Vehicle A (BEV features) ─┐
   Vehicle B (BEV features) ─┼─ V2X → Fusion Server / Edge Node
   RSU Camera (BEV features) ─┘                 │
                                        Fused BEV Grid
                                                 │
                                      All vehicles receive enhanced
                                      perception beyond line-of-sight

Benefits of cooperative perception:

- **Non-line-of-sight (NLOS) awareness** -- Vehicle B can see around a corner
  that Vehicle A cannot, and share that information.
- **Occlusion resolution** -- A truck blocking a pedestrian is visible to
  a vehicle behind the truck, which can warn the vehicle in front.
- **Redundancy** -- Multiple sensor views reduce the impact of individual
  sensor failures.


Industry Outlook 2026+
-----------------------

The autonomous vehicle industry in 2026 is at an inflection point:
early-mover advantages are crystallizing, and the industry is beginning to
consolidate.

Consolidation Trends
~~~~~~~~~~~~~~~~~~~~~

.. admonition:: The Consolidation Thesis
   :class: important

   AV development requires massive, sustained capital investment across
   hardware, software, fleet operations, and safety validation. Only a handful
   of companies globally have the resources and data scale to compete long-term.
   The exit of Cruise (2024) and the absorption of smaller players into larger
   ecosystems (Aurora → FedEx partnership, Motional restructuring) illustrate
   this dynamic.

US vs. China Dynamics
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 38 37
   :header-rows: 1
   :class: compact-table

   * - Dimension
     - United States
     - China
   * - **Leading companies**
     - Waymo, Tesla (FSD), Aurora, Mobileye
     - Baidu Apollo Go, Pony.ai, Huawei ADS, DiDi
   * - **Deployment scale**
     - Waymo: 250K+ rides/week (Phoenix, LA, SF, Austin)
     - Apollo Go: 250K+ rides/week; Pony.ai: all tier-1 cities
   * - **Regulatory environment**
     - State-by-state; no federal legislation
     - Unified national framework; aggressive city-level permitting
   * - **Technology approach**
     - Mixed (camera-centric Tesla; LiDAR-centric Waymo)
     - Predominantly LiDAR + camera + radar (redundant stacks)
   * - **Government support**
     - Moderate (NHTSA guidance, DOT funding)
     - Heavy (national strategic priority, state subsidies)

Robotaxi Economics
~~~~~~~~~~~~~~~~~~~

The path to profitability for robotaxi services requires achieving a
**cost per mile** below that of ride-sharing with human drivers:

.. math::

   \text{Cost per mile} = \frac{\text{Vehicle depreciation} + \text{AV stack cost} + \text{Operations} + \text{Insurance}}{\text{Miles driven per year}}

Baidu Apollo Go achieved per-vehicle profitability in Wuhan in 2025,
demonstrating that the economics are achievable at sufficient density.
Waymo's path to profitability hinges on scaling to the fleet sizes where
fixed AV development costs are amortized over millions of rides.

Modular vs. E2E: Where the Industry Is Heading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The debate between modular and end-to-end architectures is resolving into
a **pragmatic hybrid**:

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: 2020-2023
      :class-card: sd-border-secondary

      Modular dominates production. Mobileye RSS, Waymo Gen 5, Apollo 5.0
      all use explicit intermediate representations.

   .. grid-item-card:: 2024-2026
      :class-card: sd-border-warning

      Hybrid era. E2E neural backbones for perception + learned planners,
      with explicit safety monitors layered on top. Waymo Gen 6, Apollo 6,
      Tesla FSD v12.

   .. grid-item-card:: 2027+
      :class-card: sd-border-success

      Convergence on VLA-style systems with built-in interpretability,
      validated via novel safety case frameworks aligned with UNECE GTR.


Ethics and Liability
--------------------

Autonomous vehicles raise profound ethical questions that engineers, lawyers,
and policymakers are actively working to resolve.

The Trolley Problem in AV Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The philosophical trolley problem asks whether it is acceptable to take an
active harmful action to prevent greater harm. In AV terms:

.. admonition:: Scenario
   :class: note

   An AV's brakes fail. It can either continue straight (hitting 3 pedestrians)
   or swerve left (hitting 1 pedestrian). What should the AV do?

The Moral Machine experiment (MIT Media Lab) surveyed 2.3 million people in
233 countries and found significant cultural variation in preferences --
suggesting that no single ethical framework can satisfy global users.

Current industry position: AVs are programmed to **minimize total risk
in compliance with traffic laws** rather than to make trolley-problem-style
tradeoffs. The scenario is considered a failure of the safety system rather
than an ethical choice.

Liability Frameworks
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **Level 2 (ADAS)**
     - Driver is fully liable. Manufacturer may share liability if system
       fails to perform as advertised.
   * - **Level 3 (Conditional)**
     - Complex. Driver is liable when in control; system is liable when
       conducting DDT. This handover ambiguity is a major deployment barrier.
   * - **Level 4 (ADS)**
     - The ADS operator (e.g., Waymo) is liable for incidents during
       autonomous operation. Shifting from driver liability to product
       liability model.
   * - **Emerging (2026)**
     - Several jurisdictions (Germany, UK, Singapore) have enacted legislation
       placing liability on the ADS operator/manufacturer, not the passenger.

.. admonition:: Insurance Implications
   :class: tip

   The shift to ADS operator liability transforms car insurance from a
   consumer product to a B2B product liability framework. Lloyd's of London
   and major insurers are developing new actuarial models for AV fleets.


Career Paths in Autonomous Vehicles
-------------------------------------

The AV industry employs engineers across a uniquely broad range of disciplines.

.. tab-set::

   .. tab-item:: Perception Engineer

      - Computer vision, deep learning (CNN, transformer architectures).
      - Object detection, tracking, segmentation, BEV perception.
      - Tools: PyTorch/JAX, CUDA, nuScenes/Waymo Open datasets.
      - Companies: Mobileye, Waymo, Tesla, Zoox.

   .. tab-item:: Planning & Prediction Engineer

      - Motion planning (lattice, optimization), trajectory forecasting.
      - Tools: C++, Python, CARLA, nuPlan benchmark.
      - Companies: Waymo, Motional, Aurora, Cruise (legacy).

   .. tab-item:: Systems Integration Engineer

      - ROS 2, DDS, real-time Linux, CAN/Ethernet automotive networking.
      - Integration of hardware and software subsystems.
      - Companies: All AV companies + Tier 1 suppliers (Bosch, Continental).

   .. tab-item:: Safety & Verification Engineer

      - ISO 26262, SOTIF, formal verification, simulation-based testing.
      - Tools: ASAM OpenSCENARIO, model checkers, fault tree analysis.
      - Companies: All AV companies; specialized firms (ANSYS, dSPACE).

   .. tab-item:: Machine Learning Infrastructure

      - Large-scale training pipelines, data management, fleet learning loops.
      - Tools: Kubernetes, Ray, PyTorch Distributed, data lakes.
      - Companies: Tesla, Waymo, NVIDIA.

   .. tab-item:: V2X / Connectivity Engineer

      - C-V2X, DSRC, 5G, network security, cooperative perception.
      - Tools: ETSI ITS stack, ns-3, Cohda Wireless SDK.
      - Companies: Qualcomm, Continental, HARMAN, OEM connectivity teams.

.. admonition:: ENPM818Z and Your Career
   :class: tip

   This course has equipped you with hands-on experience across the entire
   AV stack in CARLA, exposure to the latest research (UniAD, DriveTransformer,
   GAIA-3), and familiarity with the safety and regulatory landscape. These
   are directly marketable skills in the AV industry.


Course Summary and Final Project Guidance
------------------------------------------

ENPM818Z Course Summary
~~~~~~~~~~~~~~~~~~~~~~~~~

Over the past 13 lectures, we have covered the complete autonomous driving
stack:

.. list-table::
   :widths: 10 30 60
   :header-rows: 1
   :class: compact-table

   * - Lecture
     - Topic
     - Key Concepts
   * - 1
     - Introduction & AV Landscape
     - SAE levels, DDT, ODD, industry players, CARLA setup
   * - 2
     - Sensor Technologies
     - Camera, LiDAR, RADAR, IMU, GNSS, calibration
   * - 3
     - Perception I: Detection & Segmentation
     - YOLO, DETR, BEV perception, semantic segmentation
   * - 4
     - Perception II: Tracking & Fusion
     - Kalman filters, multi-sensor fusion, cross-attention
   * - 5
     - Localization & Mapping
     - GNSS/RTK, SLAM, scan matching, pose graphs
   * - 6
     - Motion Planning I
     - A*, RRT, lattice planners, cost functions
   * - 7
     - Motion Planning II
     - Diffusion planning, learned cost functions, nuPlan
   * - 8
     - Trajectory Planning & Control
     - MPC, Pure Pursuit, polynomial trajectories
   * - 9
     - Prediction & Behavior
     - Trajectory forecasting, behavior planning, TNT, MTR
   * - 10
     - Imitation & Reinforcement Learning
     - BC, DAGGER, PPO, reward shaping for driving
   * - 11
     - End-to-End & Foundation Models
     - UniAD, DriveTransformer, VLA, Tesla FSD v12, NVIDIA
   * - 12
     - World Models & Simulation
     - GAIA-3, Cosmos, Vista, scenario generation, sim-to-real
   * - 13
     - System Integration & Safety
     - ROS 2, DDS, ISO 26262, SOTIF, UNECE GTR, V2X, outlook

Final Project Guidance
~~~~~~~~~~~~~~~~~~~~~~~~

The final project integrates all course modules into a functional ADS pipeline
in CARLA:

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Required Components
      :class-card: sd-border-success

      - Multi-camera + LiDAR perception (3-D detection + tracking)
      - Localization using GNSS + IMU fusion
      - Occupancy grid and BEV map construction
      - Behavior planning + motion planning (lattice or optimization)
      - MPC trajectory controller
      - ROS 2 integration with visualization in rviz2

   .. grid-item-card:: Evaluation Criteria
      :class-card: sd-border-success

      - Route completion rate (%)
      - Collision rate (per km)
      - Traffic law compliance (% violations)
      - Passenger comfort (RMS jerk)
      - Code quality and ROS 2 architecture
      - Written report and demonstration

   .. grid-item-card:: Optional Extensions
      :class-card: sd-border-warning

      - End-to-end imitation learning component (replace planner)
      - Trajectory prediction for NPC agents
      - V2X simulation using CARLA's co-simulation API
      - World model integration for data augmentation

   .. grid-item-card:: Key Deadlines
      :class-card: sd-border-warning

      See the course syllabus for exact dates. Contact the course
      instructors via Piazza for technical questions. CARLA scenarios
      for evaluation will be released two weeks before submission.

.. admonition:: Final Advice
   :class: important

   The autonomous vehicle industry rewards engineers who can reason clearly
   about **safety first, then performance**. Whatever system you build, ask
   yourself: "How does this fail? How does it fail safely?" The best AV
   engineers are those who design for failure modes as carefully as they
   design for the happy path.
