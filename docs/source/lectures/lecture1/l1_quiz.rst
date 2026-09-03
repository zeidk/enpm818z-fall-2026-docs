====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 1: the Dynamic Driving Task
(DDT), the DDT fallback and the Minimal Risk Condition (MRC), the Operational
Design Domain (ODD) and the OES, ADAS vs. ADS, the SAE J3016 levels, the
industry landscape, the core technical challenges, safety standards
(ISO 26262, ISO 21448/SOTIF, ISO/SAE 21434), the seven-stage path from concept
to public roads, the two case studies, and the CARLA simulator architecture.

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check.
   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`, starting with **Quiz 1 in Week 4**.

.. note::

   **Instructions:**

   - Answer each question before opening its answer box.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2--4 sentences).


----


Multiple Choice (Questions 1-15)
=================================

.. admonition:: Question 1
   :class: hint

   What does the **Dynamic Driving Task (DDT)** include?

   A. Trip scheduling, destination selection, and route planning.

   B. Lateral and longitudinal control, object and event detection and
      response, maneuver planning, and conspicuity.

   C. Vehicle manufacturing, maintenance, and insurance.

   D. Only steering and braking.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Lateral and longitudinal control, OEDR, maneuver planning, and
   conspicuity.

   J3016 splits the DDT into six subtasks: lateral control, longitudinal
   control, OEDR detection, OEDR response, maneuver planning, and conspicuity
   (making your intent visible). It explicitly **excludes** strategic
   functions such as trip scheduling, destination choice or route selection.

   A vehicle with a flawless route planner and nothing else is not automated
   at all.


.. admonition:: Question 2
   :class: hint

   Which DDT subtask is **not covered** in this course, and is a genuine gap
   in the field generally?

   A. Longitudinal control

   B. OEDR detection

   C. Conspicuity

   D. Maneuver planning

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Conspicuity.

   Conspicuity is the subtask of making the vehicle's intent visible to other
   road users: lights, indicators, horn, gestures. A vehicle that cannot
   signal its intent to a human is hard to share a road with, and almost
   nobody works on it. You will build the other five subtasks.


.. admonition:: Question 3
   :class: hint

   A car offers adaptive cruise control, lane-keeping assist, **and** a
   hands-off highway feature. What is "the SAE level of this car"?

   A. Level 1, because ACC alone is Level 1.

   B. Level 2, because that is the highest feature it offers.

   C. The question is malformed -- J3016 classifies features, not vehicles.

   D. Level 3, because hands-off implies the system is driving.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The question is malformed.

   J3016 classifies **driving automation features**, not vehicles. A single
   vehicle may offer several features at different levels, and the level that
   applies at any moment is whichever feature is engaged. "This is a Level 2
   car" is a category error -- the *feature* is Level 2.


.. admonition:: Question 4
   :class: hint

   Automatic emergency braking takes over the brakes and stops the car. What
   SAE level is it?

   A. Level 0

   B. Level 1

   C. Level 2

   D. Level 3

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- Level 0.

   AEB intervenes, it can save your life, and it is still Level 0, because
   **you never stopped driving**. Momentary interventions and warnings do not
   constitute driving automation under J3016. This is the row of the table
   that surprises people most.


.. admonition:: Question 5
   :class: hint

   What is the key distinction between **ADAS** and **ADS**?

   A. ADAS uses cameras while ADS uses LiDAR.

   B. ADAS performs part of the DDT with the human monitoring; ADS performs
      the entire DDT within its ODD.

   C. ADAS is cheaper than ADS.

   D. ADAS works only on highways while ADS works in cities.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ADAS performs part of the DDT with the human monitoring; ADS
   performs the entire DDT within its ODD.

   The same hardware can appear on both sides. **Capability does not promote
   you; responsibility does.** A very capable system that still requires an
   attentive driver is an ADAS.


.. admonition:: Question 6
   :class: hint

   Which of the following triggers a **DDT fallback**, and is **not** a fault?

   A. A LiDAR unit stops returning data.

   B. The compute stack reboots.

   C. The vehicle reaches the edge of its ODD.

   D. A wheel speed sensor fails.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The vehicle reaches the edge of its ODD.

   Two things trigger a fallback: a **system failure**, or **leaving the
   ODD**. Only the first is a fault. Leaving the ODD is a planned, foreseeable
   event with nothing broken at all -- and it still demands a complete
   handover. **Most fallbacks in service are of this second kind.**


.. admonition:: Question 7
   :class: hint

   A robotaxi operates only in downtown Phoenix during clear weather and
   daytime hours. What does this set of restrictions define?

   A. The vehicle's SAE Level.

   B. The vehicle's Operational Design Domain (ODD).

   C. The vehicle's ISO 26262 ASIL rating.

   D. The vehicle's sensor configuration.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The Operational Design Domain (ODD).

   The ODD covers geographic, environmental, traffic and infrastructure
   conditions. It is also what the regulator approves the system against in
   Stage 6, and what the scenario library in Stage 4 is derived from.


.. admonition:: Question 8
   :class: hint

   What is the difference between an **ODD** and an **OES**?

   A. They are two names for the same thing.

   B. The ODD is the idea of the operating limits; the OES is the structured,
      machine-readable document that states them.

   C. The ODD is a US concept; the OES is a European one.

   D. The OES defines the maximum speed of an automated vehicle.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The ODD is the *idea*; the OES is the *document*.

   NIST proposed the **Operating Envelope Specification** as a structured,
   machine-readable description of the driving environment that supports
   calculation-based reasoning about performance, with testing and
   certification applications, together with the criteria for assessing
   performance inside those limits. People conflate the two constantly.


.. admonition:: Question 9
   :class: hint

   A shuttle drives one fixed loop at 15 km/h in fair weather with nobody
   aboard responsible for driving. A robotaxi drives anywhere in a large city
   with nobody aboard responsible for driving. **Both are Level 4.** What
   should you ask next?

   A. Which one has more sensors?

   B. What is the ODD?

   C. Which one is certified to ISO 26262?

   D. Which one uses an end-to-end architecture?

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- What is the ODD?

   The level tells you **who is responsible for the DDT and its fallback** --
   the system, in both cases. It tells you nothing about capability. The
   entire difference between those two products lives in the ODD. When
   somebody tells you they are Level 4 and stops there, ask *where*.


.. admonition:: Question 10
   :class: hint

   Someone quotes: *"94% of crashes are caused by driver error."* What is
   wrong with that sentence?

   A. Nothing -- it is the correct reading of the NHTSA study.

   B. The real figure is 76%.

   C. NHTSA identified the *last event in the causal chain*, not the cause of
      the crash.

   D. The study only looked at highway crashes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- NHTSA identified the **critical reason**, the last event in the
   causal chain.

   A worn tire, a poorly designed intersection and a distracted driver can all
   contribute to one crash, and only the last one is counted in that
   statistic. NHTSA says so explicitly, and the number is still quoted the
   wrong way constantly -- usually by someone selling something.

   The correct phrasing: *"in 94% of crashes, the critical reason was assigned
   to the driver."*


.. admonition:: Question 11
   :class: hint

   Why is **miles per disengagement** a poor way to compare two companies?

   A. The data is classified.

   B. The definition is subjective, the data is self-reported and not
      normalized for difficulty, and companies stop reporting once the safety
      driver is removed.

   C. It is measured in kilometres in some countries.

   D. Only Level 4 systems report it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- All three problems at once.

   California counts a takeover when safe operation *requires* it, and the
   party being measured decides what "requires" means. Nobody normalizes for
   how hard the driving was -- quiet suburban roads in fair weather beat dense
   city traffic while being far less capable. And **the moment a company
   removes its safety driver it stops reporting, so the best systems leave the
   table.**

   The habit to take away: when somebody hands you a safety number, **ask what
   the denominator was.**


.. admonition:: Question 12
   :class: hint

   What does **ISO 21448 (SOTIF)** address that ISO 26262 does not?

   A. Cybersecurity vulnerabilities in vehicle networks.

   B. Safety hazards that occur *without* any system failure.

   C. Manufacturing defects in electronic components.

   D. Software licensing compliance.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Hazards that occur without any system failure.

   ISO 26262 is about **things that break**: a sensor fails, a chip flips a
   bit, code crashes. SOTIF is about **things that work exactly as designed
   and still cause a crash**: the camera is not broken, the sun is just
   directly behind the traffic light. Both are real hazards, and finding them
   takes completely different work.

   Your detector will not crash. It will confidently return the wrong answer,
   and everything downstream will believe it. **That is SOTIF.**


.. admonition:: Question 13
   :class: hint

   What does **ASIL** stand for, and what is it for?

   A. Automated System Integration Level -- it rates module coupling.

   B. Automotive Safety Integrity Level -- it classifies hazard risk and sets
      how much rigor a function gets.

   C. Advanced Sensor Integration Layer -- it defines the fusion stack.

   D. Autonomous System Intelligence Level -- it rates system capability.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Automotive Safety Integrity Level.

   Defined by ISO 26262 and assigned by the **HARA** in Stage 2, it ranges
   from ASIL A (lowest) to ASIL D (highest), plus QM. It determines how much
   redundancy, rigor and testing each function receives.


.. admonition:: Question 14
   :class: hint

   Through which stage of the seven-stage concept-to-road pipeline does the
   vehicle **still operate at Level 2 with a safety driver**?

   A. Stage 2 (Specify)

   B. Stage 4 (Validate)

   C. Stage 6 (Approve)

   D. Stage 7 (Operate and monitor)

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Stage 4, and it is where most of the calendar time goes.

   Supervised on-road testing runs with a safety driver holding the driving
   task, which makes it **Level 2 operation**, often for years. The vehicle
   does not stop being Level 2 until a regulator grants a driverless permit in
   **Stage 6**.


.. admonition:: Question 15
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

   The server (``CarlaUE4.sh``) runs the simulation on Unreal Engine. Your
   Python script is the client, connecting over TCP on port 2000. The server
   is a game engine, and it will compete with your training job for the same
   GPU.


----


True or False (Questions 16-25)
================================

.. admonition:: Question 16
   :class: hint

   **True or False:** SAE Level 5 vehicles are commercially available and
   deployed on public roads as of 2026.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Level 5 -- driving anywhere a human could drive, in any conditions -- is
   not a product category. It remains a research goal, and nothing on sale is
   close to it. Current commercial deployments are Level 4 (geofenced) or
   Level 2 (supervised).


.. admonition:: Question 17
   :class: hint

   **True or False:** A higher SAE level always means a more capable, better
   engineered system.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The level describes **who is responsible**, not how good the engineering
   is. A Level 2 feature can be more capable and safer than a Level 3 feature.
   Mercedes withdrew Drive Pilot during 2026, replaced it with a *Level 2*
   system, and put its effort into Level 4 instead -- a lower number on that
   row, and not a worse company.


.. admonition:: Question 18
   :class: hint

   **True or False:** ISO 26262 and ISO 21448 (SOTIF) address the same types
   of safety risk.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ISO 26262 covers malfunctions. SOTIF covers hazards that arise when nothing
   malfunctions. They are complementary, and finding each kind takes
   completely different work. ISO/SAE 21434 covers a third kind: what an
   attacker does on purpose.


.. admonition:: Question 19
   :class: hint

   **True or False:** At SAE Level 3, the human driver must continuously
   monitor the driving environment at all times.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   At Level 3 the system performs the DDT and monitors the environment. The
   human is the **fallback-ready user**: not required to monitor, but required
   to be receptive to a request to intervene and able to resume driving within
   seconds.

   That is a human-factors problem rather than a software one -- you get
   seconds to rebuild situational awareness you stopped maintaining minutes
   ago -- and it is a large part of why Level 3 has gone backwards.


.. admonition:: Question 20
   :class: hint

   **True or False:** "Pull over and stop" is a safe minimal risk condition in
   essentially all situations.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Pulling over assumes a shoulder is reachable **and that nothing is attached
   to, dragged by, or trapped under the vehicle.** Stopping in place assumes
   traffic behind can see you and stop, and that you are not on a crossing or
   in a tunnel.

   **An MRC is a design artifact**, validated against a list of situations
   somebody thought of. If the situation is not on the list, the vehicle still
   does what the list says.


.. admonition:: Question 21
   :class: hint

   **True or False:** A standard such as ISO 26262 or SAE J3016 is legally
   binding on manufacturers by virtue of being published.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Standards bodies write the rulebooks; nobody has to follow them. **A
   rulebook only becomes law when a government adopts or references it.** That
   is why the same vehicle can be legal in one country and illegal in another
   with no change to the software. J3016 in particular is a Recommended
   Practice, not a regulation.


.. admonition:: Question 22
   :class: hint

   **True or False:** The United States has comprehensive federal legislation
   governing autonomous vehicle testing and deployment.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   There is no comprehensive federal AV legislation: NHTSA guidance plus a
   state-by-state patchwork. The EU uses type approval, with UNECE R157 for
   Level 3 highway systems. Work toward a harmonized, safety-case-based
   international framework is underway at UNECE -- **check its current status
   before citing it.**


.. admonition:: Question 23
   :class: hint

   **True or False:** A folder containing all of a company's test results
   constitutes a safety case.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   A safety case has three parts: **claims** (what you promise the vehicle
   will not do), **arguments** (why you believe that) and **evidence** (the
   results backing each argument). A folder of results is only the third part
   -- it never says what the results were supposed to prove, so no reader can
   judge whether the evidence is sufficient or even relevant.


.. admonition:: Question 24
   :class: hint

   **True or False:** In the Tempe 2018 collision, fixing the object
   classifier alone would have prevented the crash.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The deeper finding was at the **tracking** layer: each reclassification
   reset the object's history, so no consistent track and no stable predicted
   path was ever established. Even with a perfect classifier, one second of
   action suppression still delayed the brake, the factory AEB was still
   disabled, and the operator still was not watching the road.

   **Would fixing that module alone have prevented the outcome? The answer is
   almost never yes.**


.. admonition:: Question 25
   :class: hint

   **True or False:** A detector trained only on CARLA images can be deployed
   on real driving footage without adaptation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   CARLA models geometry, road networks, traffic rules, sensor placement and
   timing well; material appearance, LiDAR in fog and RADAR multipath roughly;
   and sensor dirt, calibration drift and hardware faults not at all.

   **The skills transfer completely. The weights do not.** Your GP2 numbers
   are a claim about CARLA, and your report must say so.


----


Essay Questions (Questions 26-30)
==================================

.. admonition:: Question 26
   :class: hint

   **Explain why "capability does not promote you, responsibility does."**
   Give one example of a highly capable Level 2 system and one example of a
   less capable Level 4 system.

   *(2--4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - J3016 classifies by **who is responsible for the DDT and its fallback**,
     not by how much the system can do.
   - A Class 8 truck that steers, sets speed and changes lanes for an entire
     highway route is **Level 2** if a safety driver must monitor and
     intervene -- the human still holds the driving task.
   - A campus shuttle doing one loop at 15 km/h with no one aboard responsible
     for driving is **Level 4** -- the system holds the task and its own
     fallback within a very small ODD.
   - Same software can sit at two different levels depending only on what is
     asked of the person in the seat.


.. admonition:: Question 27
   :class: hint

   **Describe the difference between the DDT fallback and the minimal risk
   condition**, and explain why the MRC is best understood as a design
   artifact rather than an obviously safe default.

   *(2--4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The **fallback** answers *who takes over* when the system can no longer
     drive; the **MRC** answers *where the vehicle ends up*.
   - Two triggers for the fallback: a system failure, or leaving the ODD --
     and only the first is a fault.
   - Every candidate MRC hides an assumption: stopping in place assumes
     traffic behind can react; pulling over assumes a shoulder exists and that
     nothing is trapped underneath.
   - Somebody wrote that logic in advance and validated it against situations
     they could imagine. If reality is not on the list, the vehicle still
     follows the list -- which is exactly what happened in the October 2023
     pullover-and-drag incident.


.. admonition:: Question 28
   :class: hint

   **Explain why both ISO 26262 and ISO 21448 (SOTIF) are needed.** Give an
   example scenario for each, and say what testing each one implies.

   *(2--4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - **ISO 26262** covers malfunctions. Example: a radar that stops reporting
     obstacles. Addressed with redundancy, fault detection, and ASIL-driven
     development rigor.
   - **SOTIF** covers insufficiency with no malfunction. Example: a camera
     that misses a pedestrian because of sun glare -- the camera is working
     correctly, the intended functionality is insufficient.
   - Redundancy does **not** address a SOTIF hazard. What does is enumerating
     **triggering conditions** in Stage 2 and testing against a scenario
     library derived from the ODD in Stage 4.
   - Both were present in the two case studies, and in neither case did a
     component actually malfunction.


.. admonition:: Question 29
   :class: hint

   **Walk through the seven stages from concept to public roads.** Identify
   which stage consumes the most calendar time and which stage your group
   projects occupy, and explain why an under-specified ODD in Stage 2 is
   expensive.

   *(2--4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Framework → Specify → Build → Validate → Argue → Approve → Operate and
     monitor.
   - **Stage 4 (Validate)** consumes most of the calendar time, and the
     vehicle runs at Level 2 with a safety driver throughout it.
   - **Stage 3 (Build)** is the only stage GP1--GP4 occupy: architecture,
     data, training, and module verification.
   - Stage 2 happens entirely inside one company -- five of six lifelines in
     the diagram are empty. The scenario library in Stage 4 is derived from
     the ODD written in Stage 2, so a vague ODD produces a weak test set and
     nobody outside says so until the independent assessor reads it in
     Stage 5.


.. admonition:: Question 30
   :class: hint

   **Describe CARLA's client-server architecture** and explain what simulation
   does and does not model well. Why is simulation a necessity in this field
   rather than a convenience?

   *(2--4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The **server** runs the simulation on Unreal Engine -- world, physics,
     rendering, sensor generation -- and the **client** is a Python script
     connecting over TCP. A **ROS 2 bridge** publishes sensor data onto topics
     and turns control messages back into actor commands.
   - Modeled well: geometry, road networks, traffic rules, sensor placement
     and extrinsics, timing. Modeled roughly: material appearance, LiDAR in
     rain and fog, RADAR multipath, lens artifacts. Not modeled: sensor dirt,
     calibration drift, hardware faults, the full range of human behavior.
   - Demonstrating safety statistically would take hundreds of millions of
     miles (Kalra & Paddock). **That is arithmetic, not an engineering gap** —
     you cannot drive it before deploying, so simulation is the only half that
     can reach the numbers.
   - Simulation also supplies free ground-truth labels, which is what makes
     GP2 possible at all.
