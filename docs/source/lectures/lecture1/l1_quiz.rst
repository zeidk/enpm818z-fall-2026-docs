====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 1: Course Introduction & AV
Landscape. Topics include the Dynamic Driving Task (DDT), SAE J3016 levels
of automation, ADAS vs. ADS, Operational Design Domain (ODD), the current
industry landscape, core technical challenges, safety standards (ISO 26262,
SOTIF), regulatory developments, and the CARLA simulator architecture.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-15)
=================================

.. admonition:: Question 1
   :class: hint

   What does the **Dynamic Driving Task (DDT)** include?

   A. Trip scheduling, destination selection, and route planning.

   B. Steering, acceleration/deceleration, monitoring the environment, and
      object detection and response.

   C. Vehicle manufacturing, maintenance, and insurance.

   D. Only steering and braking.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Steering, acceleration/deceleration, monitoring the environment,
   and object detection and response.

   The DDT encompasses all real-time operational and tactical functions
   required to operate a vehicle in on-road traffic. It explicitly excludes
   strategic functions such as trip scheduling or destination selection.


.. admonition:: Question 2
   :class: hint

   At which SAE level does the **automated system** first become responsible
   for performing the entire Dynamic Driving Task within its ODD?

   A. Level 1

   B. Level 2

   C. Level 3

   D. Level 4

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Level 3

   At Level 3 (Conditional Automation), the system performs the entire DDT
   within its ODD for the first time. However, the human must remain ready
   to intervene when requested. Levels 1--2 only assist the driver; the
   human remains responsible for the DDT.


.. admonition:: Question 3
   :class: hint

   What is the key distinction between **ADAS** and **ADS**?

   A. ADAS uses cameras while ADS uses LiDAR.

   B. ADAS supports the human driver; ADS performs the entire DDT without
      human intervention (within its ODD).

   C. ADAS is cheaper than ADS.

   D. ADAS works only on highways while ADS works in cities.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ADAS supports the human driver; ADS performs the entire DDT
   without human intervention (within its ODD).

   ADAS (Levels 1--2) assists the driver but the human remains ultimately
   responsible. ADS (Levels 3--5) performs the entire DDT within its
   Operational Design Domain, with the system taking full responsibility.


.. admonition:: Question 4
   :class: hint

   A robotaxi operates only in downtown Phoenix during clear weather and
   daytime hours. What does this set of restrictions define?

   A. The vehicle's SAE Level.

   B. The vehicle's Operational Design Domain (ODD).

   C. The vehicle's ISO 26262 ASIL rating.

   D. The vehicle's sensor configuration.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The vehicle's Operational Design Domain (ODD).

   The ODD describes the specific operating conditions under which an ADS
   is designed to function safely, including geographic boundaries (downtown
   Phoenix), environmental conditions (clear weather), and temporal
   restrictions (daytime). If the vehicle is about to exit its ODD, it must
   ensure a safe transition.


.. admonition:: Question 5
   :class: hint

   What is the purpose of the **Operating Envelope Specification (OES)**
   proposed by NIST?

   A. To define the maximum speed of an autonomous vehicle.

   B. To provide a formal, machine-readable format for precisely defining
      an ADS's ODD.

   C. To certify vehicles for sale in the European Union.

   D. To classify the severity of vehicle crashes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To provide a formal, machine-readable format for precisely
   defining an ADS's ODD.

   The OES is a structured language proposed by NIST to clearly and
   unambiguously define an AV's capabilities and operational limits. Think
   of the ODD as the general idea of operating limits and the OES as the
   formal document that writes them down precisely.


.. admonition:: Question 6
   :class: hint

   Which company had **suspended operations** and is effectively out of the
   robotaxi race as of 2026?

   A. Waymo

   B. Baidu Apollo

   C. Cruise

   D. Pony.ai

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Cruise

   Cruise suspended operations in 2024 and is effectively out of the
   robotaxi race. Meanwhile, Waymo leads in the US with 250K+ paid
   rides/week, and Baidu Apollo Go matches that scale in China.


.. admonition:: Question 7
   :class: hint

   What does **ISO 21448 (SOTIF)** address that ISO 26262 does not?

   A. Cybersecurity vulnerabilities in vehicle networks.

   B. Safety hazards that occur *without* a system failure (e.g., a sensor
      blinded by sun glare).

   C. Manufacturing defects in electronic components.

   D. Software licensing compliance.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Safety hazards that occur *without* a system failure (e.g., a
   sensor blinded by sun glare).

   ISO 26262 covers functional safety -- managing risks from hardware and
   software failures. SOTIF (Safety of the Intended Functionality) addresses
   a different class of hazards: situations where the system works as
   designed but still produces unsafe behavior due to limitations in
   perception or decision-making. Both standards are needed together.


.. admonition:: Question 8
   :class: hint

   What was the significance of the **UNECE Global Technical Regulation on
   ADS** approved in January 2026?

   A. It banned all Level 4 vehicles from public roads.

   B. It was the first global safety framework for autonomous driving.

   C. It standardized LiDAR sensor specifications across all manufacturers.

   D. It required all AVs to use CARLA for validation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It was the first global safety framework for autonomous driving.

   The UNECE GTR on ADS uses a "safety case" approach and represents the
   first step toward international harmonization of AV safety regulations.
   Prior to this, regulations were fragmented across countries and regions.


.. admonition:: Question 9
   :class: hint

   In CARLA's architecture, what is the role of the **CARLA Server**?

   A. It runs your Python scripts and processes sensor data.

   B. It manages the 3D world, physics, rendering, and sensor data
      generation.

   C. It publishes ROS 2 topics for visualization.

   D. It connects to GitHub to download map updates.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It manages the 3D world, physics, rendering, and sensor data
   generation.

   CARLA uses a client-server architecture. The server (``CarlaUE4.sh``)
   runs the simulation using Unreal Engine 4, handling all physics,
   rendering, and sensor simulation. The client is your Python script
   that connects to the server via TCP to control vehicles, sensors, and
   the environment.


.. admonition:: Question 10
   :class: hint

   Why does this course use a **custom ROS 2 bridge** instead of CARLA's
   native ROS 2 support?

   A. CARLA does not have any ROS 2 support.

   B. The native ROS 2 implementation has a bug that creates invalid topic
      names with double slashes.

   C. The custom bridge is faster than native ROS 2.

   D. CARLA's native ROS 2 only supports ROS 2 Foxy.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The native ROS 2 implementation has a bug that creates invalid
   topic names with double slashes.

   CARLA 0.9.16's native ROS 2 support generates topic names like
   ``/carla//camera/image`` (double slash), which ROS 2 rejects as invalid.
   The custom bridge bypasses this by using the Python API directly and
   publishing to clean topic names.


.. admonition:: Question 11
   :class: hint

   Which of the following is **NOT** one of the six core technical
   challenges in autonomous driving discussed in this lecture?

   A. Perception

   B. Prediction

   C. Entertainment

   D. Validation & Safety

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Entertainment

   The six core technical challenges are: Perception, Prediction, Planning,
   Control, Validation & Safety, and System Integration. Entertainment is
   not a technical challenge of autonomous driving.


.. admonition:: Question 12
   :class: hint

   What does **ASIL** stand for in the context of ISO 26262?

   A. Automated System Integration Level

   B. Automotive Safety Integrity Level

   C. Advanced Sensor Integration Layer

   D. Autonomous System Intelligence Level

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Automotive Safety Integrity Level

   ASIL is defined by ISO 26262 to classify the severity of safety risks
   in electrical and electronic systems. It ranges from ASIL A (lowest)
   to ASIL D (highest), determining the rigor of development and testing
   required.


.. admonition:: Question 13
   :class: hint

   A Level 2 vehicle with Adaptive Cruise Control and Lane Keeping Assist
   is driving on a highway. Who is responsible for monitoring the driving
   environment?

   A. The automated system.

   B. The human driver.

   C. Both equally share responsibility.

   D. No one -- the vehicle handles everything.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The human driver.

   At Level 2, the system can control both steering and acceleration/braking
   simultaneously, but the human driver must continuously monitor the
   driving environment and be ready to take over at any time. The human
   remains ultimately responsible for the DDT.


.. admonition:: Question 14
   :class: hint

   Which CARLA concept provides **templates for creating actors** with
   configurable attributes like color and sensor parameters?

   A. World

   B. Traffic Manager

   C. Blueprint Library

   D. Waypoints

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Blueprint Library

   The Blueprint Library contains templates for creating actors (vehicles,
   pedestrians, sensors). You can configure attributes like color,
   ``role_name``, and sensor-specific parameters before spawning an actor
   in the simulation.


.. admonition:: Question 15
   :class: hint

   As of 2026, which two regions are **neck-and-neck** in autonomous vehicle
   deployment scale?

   A. Europe and Japan.

   B. United States and China.

   C. South Korea and India.

   D. United Kingdom and Canada.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- United States and China.

   Waymo leads in the US with 250K+ paid rides/week, while Baidu Apollo Go
   matches that scale in China. Pony.ai and Huawei ADS further strengthen
   China's position. The industry is consolidating around well-capitalized
   first movers in both regions.


----


True or False (Questions 16-25)
================================

.. admonition:: Question 16
   :class: hint

   **True or False:** SAE Level 5 autonomous vehicles are commercially
   available and deployed on public roads as of 2026.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Level 5 (full automation in all conditions with no ODD restrictions) is
   not yet commercially available. It remains a long-term research goal.
   Current commercial deployments are at Level 4 (geofenced) or Level 2
   (supervised).


.. admonition:: Question 17
   :class: hint

   **True or False:** The Operational Design Domain (ODD) can include
   restrictions on geography, weather, lighting, and traffic density.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The ODD defines all operating conditions under which an ADS is designed
   to function safely. This includes geographic boundaries, environmental
   conditions (weather, lighting), and traffic parameters (speed limits,
   density).


.. admonition:: Question 18
   :class: hint

   **True or False:** ISO 26262 and ISO 21448 (SOTIF) address the exact
   same types of safety risks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ISO 26262 addresses functional safety -- risks from hardware/software
   malfunctions. SOTIF addresses hazards that arise even when the system
   works as designed, such as a sensor being blinded by sun glare. They are
   complementary standards.


.. admonition:: Question 19
   :class: hint

   **True or False:** At SAE Level 3, the human driver must continuously
   monitor the driving environment at all times.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   At Level 3, the system performs the DDT and monitors the environment.
   The human does not need to continuously monitor but must be ready to
   intervene when the system requests a takeover (DDT fallback). This
   handover challenge is one reason Level 3 deployment has been limited.


.. admonition:: Question 20
   :class: hint

   **True or False:** CARLA uses a client-server architecture where the
   server runs on Unreal Engine 4 and the client is a Python script.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The CARLA server (``CarlaUE4.sh``) runs the simulation using Unreal
   Engine 4, handling physics, rendering, and sensor generation. Your
   Python scripts act as clients, connecting via TCP on port 2000 to
   control the simulation.


.. admonition:: Question 21
   :class: hint

   **True or False:** The United States has comprehensive federal
   legislation governing autonomous vehicle testing and deployment.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   As of 2026, the US still lacks federal autonomous driving legislation.
   Regulation follows a state-by-state approach, with NHTSA providing
   guidance at the federal level. The UNECE GTR approved in January 2026
   represents the first major step toward international harmonization.


.. admonition:: Question 22
   :class: hint

   **True or False:** The prediction challenge in autonomous driving refers
   to forecasting the future actions of other road users such as
   pedestrians and cyclists.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Prediction is one of the six core technical challenges. It involves
   accurately forecasting the intentions and future trajectories of
   unpredictable human drivers, pedestrians, and cyclists -- a critical
   input for safe motion planning.


.. admonition:: Question 23
   :class: hint

   **True or False:** CARLA's Traffic Manager allows you to control the
   behavior of NPC (non-player character) vehicles in the simulation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The Traffic Manager is a CARLA component that controls NPC vehicle
   behavior, including speed, lane changes, and responses to traffic
   signals. It enables realistic traffic scenarios for testing ADS
   algorithms.


.. admonition:: Question 24
   :class: hint

   **True or False:** Mercedes-Benz DRIVE PILOT is an example of a
   Level 4 autonomous driving system.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Mercedes-Benz DRIVE PILOT is a Level 3 system -- the first
   internationally certified L3 system. It operates as a highway traffic
   jam assistant at speeds up to 60 km/h. Level 4 examples include Waymo
   and Baidu Apollo Go robotaxis.


.. admonition:: Question 25
   :class: hint

   **True or False:** In CARLA, Waypoints are points on the road network
   that can be used for navigation and route planning.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Waypoints in CARLA represent discrete points on the road network,
   including lane information, speed limits, and connectivity to other
   waypoints. They are essential for implementing path planning and
   navigation algorithms.


----


Essay Questions (Questions 26-30)
==================================

.. admonition:: Question 26
   :class: hint

   **Explain the difference between the modular ADS pipeline and the
   end-to-end approach to autonomous driving.** What are the advantages
   and disadvantages of each?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The modular pipeline breaks the driving task into separate components
     (perception, prediction, planning, control), each developed and tested
     independently.
   - The end-to-end approach uses a single neural network (or integrated
     model) that maps raw sensor input directly to driving actions.
   - Modular advantages: interpretable, debuggable, each component can be
     validated independently. Disadvantages: information loss at module
     boundaries, complex integration.
   - End-to-end advantages: can learn representations the modular pipeline
     misses, simpler architecture. Disadvantages: harder to debug,
     requires massive training data, less interpretable.


.. admonition:: Question 27
   :class: hint

   **Describe three different types of ODD restrictions** and give a
   concrete example for each. Explain why defining the ODD precisely
   matters for ADS deployment.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Geographic: limited to specific roads or a geofenced area (e.g., only
     downtown Phoenix).
   - Environmental: restricted by weather or lighting (e.g., no operation
     during heavy rain or at night).
   - Traffic: designed for specific speeds or densities (e.g., highway
     only at speeds below 60 km/h).
   - Precise ODD definition matters because the ADS is only validated for
     safety within its ODD. Operating outside the ODD is untested and
     potentially dangerous. Regulators and consumers need clear
     documentation of system limitations.


.. admonition:: Question 28
   :class: hint

   **Explain why both ISO 26262 and ISO 21448 (SOTIF) are needed** for
   autonomous vehicle safety. Provide an example scenario that each
   standard would address.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ISO 26262 addresses risks from system malfunctions (hardware/software
     failures). Example: a faulty radar sensor that stops reporting
     obstacles.
   - SOTIF addresses risks when the system works as designed but still
     produces unsafe behavior. Example: a camera-based perception system
     that fails to detect a pedestrian because of sun glare -- the camera
     is functioning correctly, but the intended functionality is
     insufficient.
   - Together, they cover both failure modes (26262) and insufficiency
     modes (SOTIF), providing comprehensive safety coverage.


.. admonition:: Question 29
   :class: hint

   **Compare the deployment status of Waymo and Baidu Apollo Go** as of
   2026. What does their parallel growth suggest about the future of the
   AV industry?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Waymo leads in the US with 250K+ paid rides/week across multiple
     cities (Phoenix, LA, SF, Austin), expanding to Atlanta, Miami, DC.
   - Baidu Apollo Go matches that scale in China with 250K+ weekly fully
     driverless rides and has achieved per-vehicle profitability in Wuhan.
   - Their parallel growth suggests the AV industry is consolidating
     around well-capitalized first movers, with the US and China emerging
     as the two dominant markets.
   - The regulatory environments in both countries have been enabling
     factors, while Europe lags in deployment despite leading in
     regulation.


.. admonition:: Question 30
   :class: hint

   **Describe CARLA's client-server architecture** and explain the role of
   the custom ROS 2 bridge used in this course. Why don't we use CARLA's
   native ROS 2 support?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The CARLA server runs the 3D simulation (world, physics, rendering,
     sensors) on Unreal Engine 4. The client is a Python script that
     connects via TCP to control vehicles, sensors, and the environment.
   - The ROS 2 bridge is a middleware layer that publishes CARLA sensor
     data to ROS 2 topics and subscribes to control commands, enabling
     integration with the ROS 2 ecosystem (rviz2, rosbag2, custom nodes).
   - We use a custom bridge because CARLA 0.9.16's native ROS 2 support
     has a bug that generates invalid topic names with double slashes
     (e.g., ``/carla//camera/image``), which ROS 2 rejects.
   - The custom bridge bypasses this by using the Python API directly and
     publishing to properly formatted topic names.
