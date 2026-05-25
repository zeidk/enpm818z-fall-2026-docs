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
   * - Final Project (GP1--GP4 + Final Report)
     - 80%
   * - Quizzes (5)
     - 20%
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


AV Case Studies: Learning from Real-World Incidents
----------------------------------------------------

Understanding real-world failures is critical for building safe autonomous
systems. These case studies illustrate how technical, organizational, and
regulatory factors interact.


Uber ATG Fatality (Tempe, AZ -- March 2018)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In March 2018, an Uber ATG test vehicle operating in autonomous mode struck
and killed a pedestrian crossing the road at night in Tempe, Arizona. The
NTSB investigation revealed multiple contributing factors:

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **Perception failure**
     - The system detected the pedestrian 6 seconds before impact but
       repeatedly reclassified her as "vehicle," "other," and "bicycle,"
       preventing a stable track.
   * - **Planner design flaw**
     - Each reclassification reset the prediction module. The system never
       built enough confidence to initiate emergency braking.
   * - **Safety driver distraction**
     - The backup safety driver was watching a video on a phone and did not
       intervene.
   * - **Disabled emergency braking**
     - Uber had disabled the Volvo XC90's factory AEB system to prevent
       conflicts with the autonomy stack. No fallback existed.

.. admonition:: Key Lesson
   :class: warning

   Redundancy and fail-safe design are non-negotiable. Disabling factory
   safety systems without equivalent replacements creates an unacceptable
   single point of failure. Object classification instability must be handled
   by the planner -- track-level fusion should maintain object persistence
   across classification changes.


Cruise Dragging Incident (San Francisco -- October 2023)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In October 2023, a Cruise robotaxi in San Francisco was involved in an
incident where a pedestrian -- initially struck by a human-driven vehicle --
was knocked into the path of the robotaxi. The Cruise vehicle:

1. Detected the collision and stopped.
2. Incorrectly determined the safest action was to **pull over** to the
   curb (Minimal Risk Condition).
3. Dragged the pedestrian approximately 20 feet while executing the pullover.

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **Perception gap**
     - The system did not detect that the pedestrian was pinned under the
       vehicle after the initial stop.
   * - **MRC design flaw**
     - The pullover maneuver was inappropriate for this scenario. The MRC
       logic did not account for objects trapped beneath the vehicle.
   * - **Organizational response**
     - Cruise initially presented incomplete information to regulators,
       leading to the California DMV revoking their autonomous testing
       permit and eventual shutdown of operations.

.. admonition:: Key Lesson
   :class: warning

   MRC (Minimal Risk Condition) maneuvers must be validated against a broad
   range of edge cases. "Pull over and stop" is not universally safe.
   Transparency with regulators is critical for maintaining public trust and
   operational permits.


CARLA Live Walkthrough
-----------------------

This in-class demonstration introduces the CARLA simulation environment
that you will use throughout the course. The goal is to become comfortable
with the client-server architecture, the Python API, and basic vehicle
and sensor control.


Demo 1: Launch CARLA and Explore the World
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import carla
   import time

   # ── Connect to the CARLA server ───────────────────────────────────
   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   world = client.get_world()

   # ── Explore available maps ────────────────────────────────────────
   available_maps = client.get_available_maps()
   print("Available maps:")
   for m in available_maps:
       print(f"  {m}")

   # ── Load a specific town ──────────────────────────────────────────
   world = client.load_world('Town03')
   print(f"Loaded: {world.get_map().name}")

   # ── Set weather ───────────────────────────────────────────────────
   weather = carla.WeatherParameters.ClearNoon
   world.set_weather(weather)
   print(f"Weather set to ClearNoon")

   # ── Explore the blueprint library ─────────────────────────────────
   bp_lib = world.get_blueprint_library()
   vehicles = bp_lib.filter('vehicle.*')
   print(f"\nAvailable vehicle blueprints: {len(vehicles)}")
   for bp in list(vehicles)[:5]:
       print(f"  {bp.id}")

   sensors = bp_lib.filter('sensor.*')
   print(f"\nAvailable sensor blueprints: {len(sensors)}")
   for bp in sensors:
       print(f"  {bp.id}")


Demo 2: Spawn a Vehicle, Attach a Camera, and Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   import cv2

   # ── Spawn the ego vehicle ─────────────────────────────────────────
   vehicle_bp = bp_lib.find('vehicle.tesla.model3')
   spawn_points = world.get_map().get_spawn_points()
   vehicle = world.spawn_actor(vehicle_bp, spawn_points[0])
   print(f"Spawned: {vehicle.type_id}")

   # ── Attach a front-facing RGB camera ──────────────────────────────
   camera_bp = bp_lib.find('sensor.camera.rgb')
   camera_bp.set_attribute('image_size_x', '1280')
   camera_bp.set_attribute('image_size_y', '720')
   camera_bp.set_attribute('fov', '90')
   camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
   camera = world.spawn_actor(camera_bp, camera_transform,
                              attach_to=vehicle)

   # ── Display camera feed ───────────────────────────────────────────
   def camera_callback(image):
       array = np.frombuffer(image.raw_data, dtype=np.uint8)
       frame = array.reshape((image.height, image.width, 4))[:, :, :3]
       cv2.imshow("CARLA Ego Camera", frame)
       cv2.waitKey(1)

   camera.listen(camera_callback)

   # ── Enable autopilot and observe ──────────────────────────────────
   vehicle.set_autopilot(True)
   print("Autopilot enabled. Watch the camera feed.")

   # ── Spawn NPC traffic ─────────────────────────────────────────────
   traffic_manager = client.get_trafficmanager(8000)
   npc_bps = bp_lib.filter('vehicle.*')

   npcs = []
   for i, sp in enumerate(spawn_points[1:21]):  # spawn 20 NPCs
       npc_bp = np.random.choice(list(npc_bps))
       npc = world.try_spawn_actor(npc_bp, sp)
       if npc is not None:
           npc.set_autopilot(True, traffic_manager.get_port())
           npcs.append(npc)

   print(f"Spawned {len(npcs)} NPC vehicles.")


Demo 3: Weather and Lighting Experiments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ── Cycle through weather conditions ──────────────────────────────
   weather_presets = [
       ("Clear Noon",    carla.WeatherParameters.ClearNoon),
       ("Cloudy Noon",   carla.WeatherParameters.CloudyNoon),
       ("Wet Noon",      carla.WeatherParameters.WetNoon),
       ("Hard Rain",     carla.WeatherParameters.HardRainNoon),
       ("Soft Rain Sunset", carla.WeatherParameters.SoftRainSunset),
       ("Clear Night",   carla.WeatherParameters(
           sun_altitude_angle=-30.0)),
       ("Dense Fog",     carla.WeatherParameters(
           fog_density=80.0, fog_distance=10.0)),
   ]

   for name, preset in weather_presets:
       world.set_weather(preset)
       print(f"Weather: {name} -- observe the camera feed")
       time.sleep(5)  # observe each condition for 5 seconds

.. admonition:: Discussion Points During Demo
   :class: tip

   1. **Sensor visibility**: How does each weather condition affect what the
      camera can see? What about at night?
   2. **Town diversity**: Switch between Town01 (residential), Town03
      (commercial), and Town04 (highway). How do the driving challenges
      differ?
   3. **Traffic complexity**: Observe NPC vehicle behavior at intersections.
      What decisions must the ADS make?
   4. **Connection to the course**: This demo shows the raw inputs. Over the
      next 13 weeks, you will build the full pipeline: sensors (L2) ->
      perception (L3--L5) -> fusion (L6) -> localization (L7) -> planning
      (L8--L9) -> control (L9) -> decision-making (L10).

.. code-block:: python

   # ── Cleanup ───────────────────────────────────────────────────────
   camera.stop()
   camera.destroy()
   for npc in npcs:
       npc.destroy()
   vehicle.destroy()
   print("All actors destroyed.")
