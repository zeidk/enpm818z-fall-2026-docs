====================================================
Lecture
====================================================


Automated Vehicles
------------------

Automated vehicles (AVs) are motor vehicles equipped with technology that can
sense their environment and navigate with minimal or no human input.

.. card::
   :class-card: sd-border-primary sd-shadow-sm

   **Why Study Automated Vehicles?**

   - **Safety impact** -- Road traffic accidents cause 1.35 million deaths globally per year (WHO). 94% of serious crashes are due to human error (NHTSA).
   - **Economic significance** -- The AV market is projected to reach $2.1 trillion by 2030 (McKinsey).
   - **Technical challenge** -- Integration of perception, prediction, planning, and control in safety-critical real-time systems.
   - **Societal transformation** -- Potential to reshape transportation, urban planning, and mobility services.

.. admonition:: Core Technologies
   :class: note

   Sensors (cameras, LiDAR, radar), artificial intelligence, and control systems
   work together to **perceive**, **decide**, and **act**.


Key Terminology
~~~~~~~~~~~~~~~

The Dynamic Driving Task (DDT)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **Dynamic Driving Task (DDT)** encompasses all the real-time operational
and tactical functions required to operate a vehicle in on-road traffic
(SAE J3016).

.. list-table::
   :widths: 15 85
   :class: compact-table

   * - **Includes**
     - Steering, acceleration/deceleration, monitoring the driving environment,
       object and event detection and response, maneuver execution.
   * - **Excludes**
     - Strategic functions such as trip scheduling, route selection, or
       destination choice.


ADAS vs. ADS
^^^^^^^^^^^^^

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Aspect
     - ADAS (Advanced Driver Assistance Systems)
     - ADS (Automated Driving Systems)
   * - **Role**
     - Supports the human driver in performing parts of the DDT
     - Performs the **entire** DDT without human intervention (within ODD)
   * - **Responsibility**
     - Human is always in control and responsible for monitoring
     - System is in control and monitors the environment
   * - **SAE Levels**
     - Levels 1--2
     - Levels 3--5
   * - **Examples**
     - Lane Keeping Assist, Adaptive Cruise Control
     - Waymo robotaxi, Tesla FSD (supervised)


Operational Design Domain (ODD)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **Operational Design Domain** describes the specific operating conditions
under which an ADS is designed to function safely. If the vehicle is about to
exit its ODD, it must ensure a safe transition of control.

- **Geographic** -- Limited to certain highways or a geofenced urban area.
- **Environmental** -- May be restricted by weather (e.g., no heavy snow), lighting (daytime only).
- **Traffic** -- Designed for specific speed limits or traffic densities.

.. tip::

   NIST has proposed the **Operating Envelope Specification (OES)** -- a formal,
   machine-readable format to precisely define an ADS's ODD. Think of ODD as the
   *idea* of operating limits and OES as the *document* that writes them down.


SAE Levels of Driving Automation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Society of Automotive Engineers (SAE) defines six levels of automation via
the J3016 standard, which has become the industry classification system.

.. list-table::
   :widths: 10 25 35 30
   :header-rows: 1
   :class: compact-table

   * - Level
     - Name
     - Description
     - Who Drives?
   * - **0**
     - No Automation
     - Human performs all driving tasks
     - Human
   * - **1**
     - Driver Assistance
     - System assists with steering **or** acceleration/braking
     - Human (with assistance)
   * - **2**
     - Partial Automation
     - System controls steering **and** acceleration/braking; human must monitor
     - Human (supervising)
   * - **3**
     - Conditional Automation
     - System performs DDT within ODD; human must be ready to intervene
     - System (human as fallback)
   * - **4**
     - High Automation
     - System performs DDT within ODD; no human fallback needed in ODD
     - System (within ODD)
   * - **5**
     - Full Automation
     - System performs DDT in all conditions; no ODD restriction
     - System (everywhere)

.. important::

   The key distinction is **who is responsible for the DDT**:

   - **Levels 0--2 (ADAS)**: The human driver is ultimately responsible.
   - **Levels 3--5 (ADS)**: The automated system performs the entire DDT within its ODD.


Current Industry Landscape (2026)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Level 2 (ADAS)

      Widely deployed and marketed as advanced assistance:

      - **Tesla Autopilot / FSD (Supervised)** -- Available to millions of vehicles; 8.3 billion supervised FSD miles as of early 2026. Launched unsupervised Robotaxi in Austin (Jan 2026).
      - **GM Super Cruise** -- Hands-free highway driving on mapped roads.
      - **Ford BlueCruise** -- Hands-free highway driving.
      - **Mobileye SuperVision** -- Hands-off/eyes-on driving up to 130 km/h.

   .. tab-item:: Level 3 (Conditional)

      Very limited deployment due to liability and handover challenges:

      - **Mercedes-Benz DRIVE PILOT** -- First internationally certified L3 system; highway traffic jam assistant up to 60 km/h.
      - **Huawei ADS 4.0** -- L3 highway capability; 1M+ vehicles equipped; 7.28B km accumulated.

   .. tab-item:: Level 4 (Robotaxis & Trucks)

      Deployed in geofenced commercial services:

      - **Waymo** -- Market leader: 250K+ paid rides/week across Phoenix, LA, SF, Austin. Expanding to Atlanta, Miami, DC.
      - **Baidu Apollo Go** -- 250K+ weekly fully driverless rides (matching Waymo). Per-vehicle profitability achieved in Wuhan.
      - **Pony.ai** -- Fully autonomous robotaxis in all four Chinese tier-1 cities. Expanding to Dubai in 2026.
      - **Aurora** -- Focused on autonomous trucking and freight logistics.
      - **Cruise** -- Suspended operations (2024). Effectively out of the robotaxi race.

   .. tab-item:: Level 5

      True "all conditions" automation **is not yet commercially available** and remains a long-term research goal.

.. admonition:: Key Takeaway
   :class: tip

   The industry is consolidating around well-capitalized first movers. China (Baidu, Pony.ai, Huawei) is now neck-and-neck with the US (Waymo, Tesla) in deployment scale.


Technical Challenges
~~~~~~~~~~~~~~~~~~~~

Achieving robust automation requires solving immense challenges across the
entire AV stack:

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Perception
      :class-card: sd-border-info

      Reliably seeing and understanding the world in all conditions (rain, fog,
      snow, glare) and identifying rare edge-case events.

   .. grid-item-card:: Prediction
      :class-card: sd-border-info

      Accurately forecasting the intentions and future actions of unpredictable
      human drivers, pedestrians, and cyclists.

   .. grid-item-card:: Planning
      :class-card: sd-border-info

      Making safe, efficient, and human-like driving decisions in complex,
      interactive scenarios.

   .. grid-item-card:: Control
      :class-card: sd-border-info

      Precisely controlling vehicle dynamics for a smooth, safe ride across
      varied road surfaces and conditions.

   .. grid-item-card:: Validation & Safety
      :class-card: sd-border-info

      Proving a system is safe requires billions of miles of simulated and
      real-world testing to cover endless scenarios.

   .. grid-item-card:: System Integration
      :class-card: sd-border-info

      Ensuring complex hardware and software subsystems work together
      flawlessly with built-in redundancy and cybersecurity.


Safety and Regulation
~~~~~~~~~~~~~~~~~~~~~

Key Safety Standards
^^^^^^^^^^^^^^^^^^^^

- **ISO 26262 (Functional Safety)** -- Manages safety risks in electrical/electronic systems. Defines Automotive Safety Integrity Levels (ASIL) to classify risk.
- **ISO 21448 (SOTIF)** -- "Safety of the Intended Functionality." Addresses hazards that occur *without* a system failure (e.g., sensor blinded by sun glare). A critical complement to ISO 26262.
- **ISO/SAE 21434** -- Automotive cybersecurity engineering standard.

Regulatory Landscape
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 80
   :class: compact-table

   * - **United States**
     - Guided by NHTSA at the federal level; no federal AV legislation yet.
       State-by-state approach continues.
   * - **European Union**
     - "Type approval" framework. UNECE R157 for L3 highway systems.
   * - **China**
     - Rapidly developing its own regulatory framework enabling Baidu, Pony.ai,
       and others to operate at scale.
   * - **Global (2026)**
     - The **UNECE Global Technical Regulation on ADS** was approved in Jan 2026 --
       the first global safety framework for autonomous driving, using a
       "safety case" approach. Final approval expected mid-2026.

.. warning::

   The regulatory environment is struggling to keep pace with rapid
   technological advancements. The UNECE GTR represents the first major step
   toward international harmonization.


ADS Development Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^

The development, validation, and deployment of an ADS involves a complex
pipeline:

1. **Design & Development** -- Define ODD, develop perception/planning/control modules.
2. **Simulation Testing** -- Validate in simulation (CARLA, internal simulators) across millions of scenarios.
3. **Closed-Course Testing** -- Physical testing on controlled tracks.
4. **Public Road Testing** -- Real-world testing with safety drivers.
5. **Regulatory Approval** -- Comply with ISO 26262, SOTIF, and regional regulations.
6. **Commercial Deployment** -- Launch within approved ODD.


Course Focus Areas
^^^^^^^^^^^^^^^^^^

.. card::
   :class-card: sd-border-success sd-shadow-sm

   **Technologies We Will Explore**

   - **Sensor Technologies** -- Cameras, LiDAR, RADAR, IMU, GNSS; calibration.
   - **Perception** -- Object detection (YOLO, DETR), BEV perception, segmentation, tracking.
   - **Multi-Sensor Fusion** -- Kalman filters, cross-attention fusion.
   - **Localization & SLAM** -- GNSS/RTK, odometry, scan matching, pose graphs.
   - **Motion Planning** -- A*, RRT, lattice planners, diffusion-based planning.
   - **Trajectory Planning & Control** -- MPC, Pure Pursuit, polynomial trajectories.
   - **Prediction & Decision-Making** -- Trajectory prediction, behavior planning, imitation learning.
   - **End-to-End Driving & Foundation Models** -- UniAD, DriveTransformer, VLA models.
   - **World Models & Simulation** -- GAIA-3, Cosmos, generative scenarios.
   - **System Integration & Safety** -- ISO 26262, SOTIF, UNECE GTR.


Course Overview
---------------

Course Structure
~~~~~~~~~~~~~~~~

ENPM818Z combines lectures with intensive, hands-on programming sessions in
CARLA. Each week builds on prior material -- progressing from single-sensor
processing to full system integration. Students complete a sequence of
assignments leading to a **final project** implementing a functional ADS
pipeline.


Assessment
~~~~~~~~~~

.. list-table::
   :widths: 60 20
   :header-rows: 1
   :class: compact-table

   * - Component
     - Weight
   * - Assignments (4)
     - 30%
   * - Quizzes (5)
     - 20%
   * - Final Project
     - 50%
   * - **Total**
     - **100%**

.. warning::

   Late submissions incur a 10% deduction per day (maximum 3 days). Beyond
   3 days, submissions receive zero credit.


Operating System & Software
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Component
     - Details
   * - **OS**
     - Ubuntu 22.04 LTS (Jammy) or Ubuntu 24.04 LTS (Noble)
   * - **ROS 2**
     - Humble Hawksbill (22.04) or Jazzy Jalisco (24.04)
   * - **CARLA**
     - 0.9.16 (native on 22.04; Docker on 24.04)
   * - **IDE**
     - Visual Studio Code
   * - **Python**
     - 3.10+ with ``numpy``, ``matplotlib``, ``opencv-python``, ``carla``
   * - **Version Control**
     - Git + GitHub


Development Environment Setup
------------------------------

Version Control (Git & GitHub)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Git is a version control system that tracks changes in your files over time.

.. code-block:: bash

   # Install Git
   sudo apt update && sudo apt install git

   # Configure
   git config --global user.name "Your Full Name"
   git config --global user.email "your.email@umd.edu"

   # Verify
   git config --list

**Essential Git commands:**

.. grid:: 1 2 2 2
   :gutter: 2

   .. grid-item-card:: Daily Commands

      .. code-block:: bash

         git status          # Check status
         git add .           # Stage changes
         git commit -m "msg" # Commit
         git push            # Upload to GitHub
         git pull            # Download updates

   .. grid-item-card:: Branching Commands

      .. code-block:: bash

         git branch          # List branches
         git checkout -b new # Create & switch
         git merge branch    # Merge branch
         git branch -d old   # Delete branch

**GitHub** is a cloud-based platform that hosts Git repositories. Course
materials are available at the course GitHub repository.


Visual Studio Code
~~~~~~~~~~~~~~~~~~

VS Code is a free, open-source code editor available on all platforms. It is
consistently ranked as the most popular code editor in developer surveys.

**Installation:**

.. code-block:: bash

   # Download .deb from https://code.visualstudio.com/download
   cd ~/Downloads
   sudo apt install ./code_<version>_amd64.deb

**Key features:**

- Activity Bar (left side): File explorer, search, source control, extensions.
- Editor: Where you write code.
- Integrated Terminal: For running commands.
- Command Palette: ``Ctrl+Shift+P`` for all VS Code actions.

**Recommended extensions** for this course: Python, Pylance, ROS, YAML,
GitLens, Docker (if using Jazzy setup).

.. tip::

   The ``.vscode`` folder in your project root stores workspace-specific
   settings (``settings.json``, ``launch.json``, ``extensions.json``). These
   override your global VS Code settings.


Programming Guidelines
~~~~~~~~~~~~~~~~~~~~~~

In this course we follow:

- `PEP 8 <https://peps.python.org/pep-0008/>`_ -- Python style guide.
- `C++ Core Guidelines <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>`_ -- For any C++ code.

.. warning::

   One way to lose points on assignments is by failing to follow coding guidelines.


Linux Shell Essentials
~~~~~~~~~~~~~~~~~~~~~~

A shell is a program that provides a command-line interface for interacting
with the operating system.

**Common shells:**

- **Bash** (``~/.bashrc``) -- Default for most Linux distributions.
- **Zsh** (``~/.zshrc``) -- Enhanced autocompletion and customization.

**Useful concepts:**

.. tab-set::

   .. tab-item:: Aliases

      Shortcuts that save you from typing long commands:

      .. code-block:: bash

         alias cdd='cd ~/Documents'
         alias sr='source ~/.bashrc'   # or source ~/.zshrc

   .. tab-item:: File Sourcing

      Apply changes to your shell configuration without opening a new terminal:

      .. code-block:: bash

         source ~/.bashrc

   .. tab-item:: Functions

      Reusable blocks of commands:

      .. code-block:: bash

         my_function() {
             echo "Hello from my_function"
             cd ~/catkin_ws && colcon build
         }

.. tip::

   Check your current shell with ``ps -p $$``.


CARLA Simulator
---------------

CARLA (Car Learning to Act) is an open-source autonomous driving simulator
built on Unreal Engine 4, designed for ADS development, training, and
validation.

- Developed by the Computer Vision Center (CVC), Autonomous University of Barcelona.
- Provides realistic urban and highway environments.
- Supports multi-agent simulation with pedestrians, cyclists, and vehicles.
- Includes weather conditions, day/night cycles, and various lighting scenarios.
- Active open-source community.

.. seealso::

   See the :doc:`CARLA setup guides </carla/carla>` for installation
   instructions (native or Docker).


Key Features
~~~~~~~~~~~~

.. grid:: 1 2 2 3
   :gutter: 2

   .. grid-item-card:: Sensor Simulation

      - RGB, depth, semantic segmentation cameras
      - LiDAR point clouds (configurable)
      - RADAR range/velocity detection
      - IMU (accelerometer + gyroscope)
      - GNSS with realistic noise
      - Collision and lane invasion detection

   .. grid-item-card:: Environment Diversity

      - Multiple towns (urban, rural, highway)
      - Dynamic weather (rain, fog, sun position)
      - Traffic scenarios (intersections, roundabouts, merging)
      - Pedestrians and cyclists with behavior models

   .. grid-item-card:: APIs & Integration

      - Python API for scenario control and data collection
      - Custom ROS 2 bridge (course-provided)
      - Co-simulation with SUMO for large-scale traffic


Client-Server Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 80
   :class: compact-table

   * - **CARLA Server**
     - Runs the simulation (``CarlaUE4.sh``). Manages the 3D world, physics,
       rendering, and sensor data generation. Default port: 2000.
   * - **CARLA Client**
     - Your Python scripts. Connects to the server via TCP. Controls vehicles,
       sensors, and the environment.
   * - **ROS 2 Bridge**
     - Course-provided middleware that publishes CARLA sensor data to ROS 2
       topics and subscribes to control commands.

**Key CARLA concepts:**

- `World <https://carla.readthedocs.io/en/latest/core_world/>`_ -- The simulated environment (towns, weather, actors).
- `Actors <https://carla.readthedocs.io/en/latest/core_actors/>`_ -- Dynamic objects (vehicles, pedestrians, sensors).
- `Blueprint Library <https://carla.readthedocs.io/en/latest/bp_library/>`_ -- Templates for creating actors with configurable attributes.
- `Waypoints <https://carla.readthedocs.io/en/0.9.16/core_map/#waypoints>`_ -- Points on the road network for navigation.
- `Traffic Manager <https://carla.readthedocs.io/en/0.9.16/adv_traffic_manager/>`_ -- Controls NPC vehicle behavior.


CARLA in This Course
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Week
     - CARLA Usage
   * - Week 2
     - Sensor data collection and visualization
   * - Week 4
     - Multi-sensor fusion with LiDAR and camera data
   * - Week 6--7
     - Localization and SLAM testing in different towns
   * - Week 8--9
     - Motion planning with dynamic obstacles
   * - Weeks 11--13
     - Full ADS pipeline development and testing

.. note::

   Pre-configured CARLA scenarios will be provided for each assignment to
   ensure consistent learning experiences across different hardware
   configurations.
