====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 13: System Integration, Safety
& Industry Outlook. Topics include AV system architecture and data flow,
ROS 2 middleware and DDS QoS, real-time constraints and latency budgets,
ISO 26262 (ASIL levels, V-model), ISO 21448 (SOTIF), the UNECE Global
Technical Regulation on ADS (January 2026), automotive cybersecurity (ISO/SAE
21434), V2X communication standards (DSRC and C-V2X), cooperative perception,
the 2026+ industry outlook, ethics and liability, and career paths in
autonomous vehicles.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-10)
=================================

.. admonition:: Question 1
   :class: hint

   In a production AV system, what is the **correct order** of the main
   software modules in the data pipeline?

   A. Planning → Perception → Prediction → Control

   B. Perception → Planning → Prediction → Control

   C. Perception → Prediction → Planning → Control

   D. Prediction → Perception → Control → Planning

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Perception → Prediction → Planning → Control

   Sensors provide raw data to the Perception module, which produces a
   structured scene understanding (object lists, occupancy grids). Prediction
   uses the perceived agents to forecast their future trajectories. Planning
   uses those predicted trajectories to generate a safe ego trajectory. Control
   converts the planned trajectory into actuator commands (steer, throttle,
   brake).


.. admonition:: Question 2
   :class: hint

   Which **QoS policy** should be used for a camera sensor topic in ROS 2
   where the most recent frame is always preferred and older frames can
   be safely dropped?

   A. RELIABILITY = RELIABLE, HISTORY = KEEP_ALL

   B. RELIABILITY = BEST_EFFORT, HISTORY = KEEP_LAST(1)

   C. RELIABILITY = RELIABLE, HISTORY = KEEP_LAST(100)

   D. DURABILITY = TRANSIENT_LOCAL, RELIABILITY = RELIABLE

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- RELIABILITY = BEST_EFFORT, HISTORY = KEEP_LAST(1)

   Camera streams require the most recent frame; dropping old frames is
   acceptable and preferable to queuing them (which would introduce latency).
   BEST_EFFORT reliability avoids retransmission overhead for dropped packets.
   KEEP_LAST(1) ensures only the latest image is buffered. RELIABLE is
   appropriate for safety-critical commands, not high-rate sensor streams.


.. admonition:: Question 3
   :class: hint

   What is the **Minimal Risk Condition (MRC)** in the context of ADS
   real-time safety?

   A. The minimum acceptable perception accuracy for highway driving.

   B. The fallback behavior an ADS executes when it cannot safely continue
      the driving task -- typically decelerating smoothly to a stop at the
      side of the road.

   C. The minimum number of sensors required to achieve ASIL D compliance.

   D. A software update process that minimizes the risk of introducing
      new bugs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The fallback behavior an ADS executes when it cannot safely
   continue the driving task -- typically decelerating smoothly to a stop at
   the side of the road.

   The MRC is a key safety concept in SAE J3016 for Level 4 and 5 systems:
   since there is no human fallback driver available, the ADS must itself
   execute a safe stop if it encounters a condition it cannot handle (system
   fault, ODD exit, missed deadline). Watchdog timers trigger MRC automatically
   if safety-critical modules miss their deadlines.


.. admonition:: Question 4
   :class: hint

   Which ASIL level is required for **brake-by-wire** systems in an
   autonomous vehicle?

   A. QM (Quality Management)

   B. ASIL A

   C. ASIL B

   D. ASIL D

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ASIL D

   Brake-by-wire is the highest-criticality function in a vehicle: failure
   or corruption of braking commands can directly cause a fatal accident with
   no human override available. ISO 26262 assigns ASIL D to functions with
   the highest severity (S3), high exposure (E4), and no driver controllability
   (C0), which characterizes brake-by-wire in an ADS.


.. admonition:: Question 5
   :class: hint

   What is the key distinction between **ISO 26262** and **ISO 21448
   (SOTIF)**?

   A. ISO 26262 applies to software; SOTIF applies to hardware.

   B. ISO 26262 addresses safety risks from system malfunctions; SOTIF
      addresses safety risks that occur even when the system functions
      as designed (e.g., sensor performance limitations).

   C. ISO 26262 is for passenger vehicles; SOTIF is for commercial trucks.

   D. ISO 26262 is for European markets; SOTIF is for US markets.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ISO 26262 addresses safety risks from system malfunctions; SOTIF
   addresses safety risks that occur even when the system functions as designed.

   ISO 26262 handles failures (a radar sensor stops working), while SOTIF
   handles limitations (a radar sensor that is working correctly but cannot
   detect a bicycle in heavy rain). Both are required for a comprehensive ADS
   safety argument because they address orthogonal risk classes.


.. admonition:: Question 6
   :class: hint

   The UNECE Global Technical Regulation on ADS (January 2026) uses what
   approach for demonstrating ADS safety?

   A. Mandatory minimum hardware specifications for sensors.

   B. A prescriptive test scenario library that all AVs must pass.

   C. A safety case approach -- a structured argument with evidence that
      the ADS is acceptably safe within its documented ODD.

   D. A type approval process identical to the existing UNECE R157 standard.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- A safety case approach -- a structured argument with evidence
   that the ADS is acceptably safe within its documented ODD.

   The safety case approach is more flexible and technology-neutral than
   prescriptive specifications, which is why regulators chose it for ADS:
   the technology is evolving too rapidly for fixed hardware requirements to
   remain relevant. Manufacturers must construct and maintain a documented
   safety case showing that all identified hazards are adequately mitigated
   within the stated ODD.


.. admonition:: Question 7
   :class: hint

   **LiDAR spoofing** is an example of which category of automotive
   cybersecurity attack?

   A. Backend server compromise.

   B. OTA update hijacking.

   C. Sensor spoofing / physical-layer attack.

   D. CAN bus injection.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Sensor spoofing / physical-layer attack.

   LiDAR spoofing attacks the physical sensing layer by firing laser pulses
   at the AV's LiDAR detector to inject phantom obstacles or blank out real
   ones. This is a physical-layer attack that bypasses the software stack
   entirely and is addressed through sensor diversity, cross-sensor validation,
   and hardware-level countermeasures.


.. admonition:: Question 8
   :class: hint

   What is the **primary advantage of C-V2X over DSRC** for V2X
   communication in autonomous vehicles?

   A. C-V2X has lower latency than DSRC in all conditions.

   B. C-V2X operates in the 5.9 GHz band, which has longer range than DSRC.

   C. C-V2X integrates with cellular networks (LTE/5G), enabling wide-area
      services (HD map updates, traffic optimization) in addition to
      vehicle-to-vehicle direct communication.

   D. C-V2X is backward compatible with DSRC hardware.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- C-V2X integrates with cellular networks (LTE/5G), enabling
   wide-area services (HD map updates, traffic optimization) in addition to
   vehicle-to-vehicle direct communication.

   C-V2X supports two modes: PC5 (direct sidelink, low latency, no network)
   and Uu (via cellular base station, wide area). This dual-mode capability
   enables both immediate safety-critical communication (V2V) and cloud-based
   services that DSRC cannot support. C-V2X is also the preferred standard in
   China and is gaining ground in Europe.


.. admonition:: Question 9
   :class: hint

   **Cooperative perception** using V2X enables which capability that is
   impossible with single-vehicle perception?

   A. Higher-resolution point clouds than any single LiDAR can produce.

   B. Detection of objects that are occluded from the ego vehicle's sensors
      by sharing sensor data from other vehicles and roadside units.

   C. Elimination of the need for onboard perception hardware.

   D. Guaranteed latency below 1 ms for perception updates.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Detection of objects that are occluded from the ego vehicle's
   sensors by sharing sensor data from other vehicles and roadside units.

   This non-line-of-sight (NLOS) awareness is the transformative capability
   of cooperative perception: a vehicle behind a truck can see a pedestrian
   stepping off the curb and share that perception with the vehicle in front,
   which cannot see the pedestrian directly. This dramatically extends
   effective perception range beyond the physical limits of any single sensor.


.. admonition:: Question 10
   :class: hint

   As of 2026, why has **Baidu Apollo Go's achievement of per-vehicle
   profitability in Wuhan** been significant for the AV industry?

   A. It proved that LiDAR-based systems are more cost-effective than
      camera-only systems.

   B. It was the first demonstration that robotaxi economics can work at
      city-scale density, providing a proof-of-concept for the commercial
      viability of ADS.

   C. It showed that regulatory approval in China is easier than in the US.

   D. It demonstrated that end-to-end models are more profitable than
      modular stacks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It was the first demonstration that robotaxi economics can work
   at city-scale density, providing a proof-of-concept for the commercial
   viability of ADS.

   Robotaxi profitability requires high utilization rates (many rides per
   vehicle per day), competitive cost per mile, and a geographic density that
   minimizes repositioning costs. Baidu achieving this in Wuhan in 2025
   provided empirical evidence that the robotaxi business model is viable --
   not just a theoretical projection -- and has accelerated investment and
   expansion plans globally.


----


True or False (Questions 11-15)
================================

.. admonition:: Question 11
   :class: hint

   **True or False:** In ROS 2, the DDS middleware requires a central
   rosmaster process to manage communication between nodes, just as ROS 1
   did.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   DDS uses **distributed discovery** -- nodes discover each other
   automatically through multicast without any central broker or master
   process. This is one of the key improvements of ROS 2 over ROS 1: the
   single-point-of-failure rosmaster is eliminated, making the system more
   robust for safety-critical deployments where the master could crash.


.. admonition:: Question 12
   :class: hint

   **True or False:** ISO 26262's V-model development process ensures that
   every design phase has a corresponding verification and testing phase.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The V-model is named for its V-shape when drawn: the left arm descends
   from system requirements through architecture to implementation; the right
   arm ascends from unit testing through integration testing to system
   testing. Each level on the right arm verifies the corresponding level on
   the left arm, ensuring comprehensive traceability from requirements to
   tests.


.. admonition:: Question 13
   :class: hint

   **True or False:** Under a Level 4 ADS operating in its ODD, the human
   passenger is legally liable for any collision that occurs during the
   autonomous operation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   At Level 4, the ADS performs the entire DDT within its ODD and there is
   no human fallback driver role. Liability during autonomous operation
   therefore shifts from the passenger/driver to the ADS operator or
   manufacturer -- a product liability model. Several jurisdictions (Germany,
   UK, Singapore) have codified this in legislation. The passenger is not
   responsible for the ADS's driving decisions.


.. admonition:: Question 14
   :class: hint

   **True or False:** The "unknown unsafe" zone in SOTIF refers to scenarios
   that are known to the manufacturer to cause system failures but have not
   yet been fixed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The "unknown unsafe" zone refers to scenarios that the manufacturer has
   not yet discovered and therefore does not know cause failures. These are
   the scenarios the system will fail in when encountered in the field,
   before the manufacturer can identify and address them. The SOTIF validation
   goal is to reduce this zone through systematic scenario exploration
   (simulation, formal analysis, real-world testing) before deployment.


.. admonition:: Question 15
   :class: hint

   **True or False:** Adversarial stickers placed on stop signs that fool
   camera-based perception systems are an example of a SOTIF hazard rather
   than a cybersecurity attack.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** (or arguably **both** -- accept with explanation)

   Physical adversarial attacks (stickers on stop signs) are technically
   cybersecurity attacks in the sense that they are deliberate adversarial
   manipulations of the system. However, they also fall under SOTIF because
   they exploit a performance limitation of the intended functionality
   (the CNN-based perception cannot handle out-of-distribution patterns).
   In practice, both frameworks are needed: SOTIF to characterize the
   performance limitation, and ISO/SAE 21434 to define countermeasures
   against deliberate adversarial exploitation.


----


Essay Questions (Questions 16-18)
===================================

.. admonition:: Question 16
   :class: hint

   **Explain the ASIL classification process under ISO 26262.** Choose one
   AV safety function, perform a simplified HARA (Hazard Analysis and Risk
   Assessment), and justify the ASIL level you assign.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ASIL is determined by three parameters: Severity (S0-S3), Exposure
     (E0-E4), and Controllability (C0-C3). The combination maps to ASIL A-D
     or QM.
   - Example: Automatic Emergency Braking (AEB). Hazardous event: AEB fails
     to activate when a pedestrian is in the path. Severity = S3 (potentially
     fatal). Exposure = E3 (common urban driving). Controllability = C2 (driver
     may be able to brake manually if reaction time allows). ASIL = C.
   - Alternatively: AEB activates falsely at highway speed with following
     traffic. Severity = S3 (rear-end collision possible). Exposure = E4
     (highway driving is frequent). Controllability = C1 (limited -- sudden
     braking at 120 km/h is hard to avoid). ASIL = D.
   - The HARA is documented and the ASIL drives development rigor: ASIL D
     requires formal verification, independent review, and the most stringent
     testing requirements.


.. admonition:: Question 17
   :class: hint

   **Describe how ISO/SAE 21434 addresses the cybersecurity of an OTA
   (over-the-air) software update system for an autonomous vehicle.** What
   threats must be addressed, and what technical countermeasures are used?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The OTA update channel is a high-value attack target: if an attacker
     can push a malicious software update to an AV fleet, they gain control
     of millions of vehicles. ISO/SAE 21434 requires a TARA (Threat Analysis
     and Risk Assessment) that identifies this attack vector and assigns a
     risk level.
   - Primary threats: man-in-the-middle (attacker intercepts and modifies
     the update), replay (attacker re-sends an old, vulnerable update),
     and backend server compromise (attacker breaks into the update server).
   - Countermeasures: code signing (every update package is signed with an
     asymmetric key pair; the vehicle verifies the signature before installation),
     TLS 1.3 for the transport channel, version pinning (vehicle rejects
     updates with lower version numbers to prevent replay), and hardware
     security modules (HSM) to protect the private signing key.
   - Post-deployment monitoring is also required: the manufacturer must
     maintain vulnerability disclosure processes and be able to push urgent
     security patches within a defined time window.


.. admonition:: Question 18
   :class: hint

   **Reflect on the ethical and liability challenges of autonomous vehicles**
   at Level 4. How do current industry and regulatory frameworks address
   these challenges, and what open questions remain?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - At Level 4, the ADS is the sole decision-maker during autonomous
     operation. This raises both ethical questions (how should the system
     prioritize competing harms?) and legal questions (who is responsible
     when an ADS causes injury?).
   - Industry approach to ethics: AVs are not programmed to make trolley-problem
     tradeoffs; instead they are designed to minimize total risk while complying
     with traffic laws. The MIT Moral Machine experiment showed no global
     consensus on ethical priorities, making any specific ethical programming
     controversial.
   - Liability frameworks: Germany, UK, and Singapore have enacted laws
     placing liability on the ADS operator/manufacturer during autonomous
     operation -- a product liability model. This is a pragmatic solution
     that enables deployment but shifts insurance burden to operators.
   - Open questions: (1) How should liability be divided when a failure
     involves both a hardware defect (OEM responsibility) and a software
     limitation (ADS developer responsibility)? (2) Who is liable when a
     third-party software component (e.g., a perception library) causes a
     failure? (3) How are international incidents handled when an AV built
     and regulated in one country causes harm in another?
