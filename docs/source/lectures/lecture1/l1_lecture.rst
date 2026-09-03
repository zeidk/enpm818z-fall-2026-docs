====================================================
Lecture
====================================================

.. note::

   These notes accompany the L1 slide deck (v1.0) and carry more detail than
   the slides do. Where the two disagree, these notes are the authoritative
   version.

.. important::

   Development environment setup (Ubuntu, ROS 2, VS Code, Git, shell basics)
   is **pre-read material** and is not covered in lecture. Work through
   :doc:`Pre-Read: Development Environment </preread/dev-environment>` before
   this class, then install CARLA with the
   :doc:`setup guide </carla/carla>`.


How These Notes Work
--------------------

Four conventions that apply all semester:

- **Every deck has a version number and a changelog.** If you printed an old
  copy, check the version before you rely on it. The same applies to these
  pages -- see the :doc:`course changelog </changelog/changelog>`.
- **Every deck has a matching page here**, and the page carries more detail
  than the slides.
- **Claims that are not obvious are cited.** See :doc:`l1_references`.
- **Never copy-paste code out of a PDF.** PDF copy-paste silently corrupts
  whitespace, quotes and dashes. The code lives in the course repository and
  in this documentation.

.. warning::

   Two practical checks before the semester starts. Can you connect to eduroam
   from Linux? And do you have access to a machine with an NVIDIA GPU? If
   either answer is no, email the instructor in **Week 1** -- not in October.


Automated Vehicles
------------------

There is no standard definition of "automated vehicle". **SAE J3016**, the
taxonomy this field runs on, classifies **driving automation features**, not
vehicles, and it classifies them by **who is responsible for the driving
task** -- not by how capable the technology is.

.. card::
   :class-card: sd-border-primary sd-shadow-sm

   **What follows from that**

   - A single vehicle may offer several features operating at different
     levels. The level that applies at any moment is whichever feature is
     engaged.
   - So "this is a Level 2 car" is a category error. The **feature** is
     Level 2.
   - What J3016 *does* define precisely: driving automation system, ADS, DDT,
     DDT fallback, minimal risk condition, and ODD. Those are the words this
     course will use.
   - J3016 is a **Recommended Practice, not a regulation**. It carries no
     legal force by itself, though regulators reference it.

.. tip::

   NIST's usage is downstream of this: an automated vehicle is a vehicle
   equipped with an **ADS**. Notice what that avoids -- the work is all in
   defining the ADS and its operating limits, not in defining the vehicle.


Why Study Automated Vehicles?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Safety impact** -- Road traffic crashes cause roughly **1.19 million
  deaths per year** worldwide (WHO, *Global Status Report on Road Safety
  2023*).
- **The 94% figure, and why it is misused** -- NHTSA studied crashes and asked
  what the *last* thing to go wrong was. In 94% of cases that last thing was
  something the driver did. **That is not the same as saying drivers cause 94%
  of crashes.** A worn tire, a badly designed intersection and a distracted
  driver can all be part of one crash, and only the last one gets counted
  here. NHTSA says this explicitly. It is quoted the wrong way constantly.
- **Economic significance** -- Market forecasts differ by a **factor of ten**
  depending on what gets counted. Treat any single headline number with
  skepticism.
- **Technical challenge** -- Perception, prediction, planning and control
  integrated in a safety-critical real-time system.
- **Societal transformation** -- Potential to reshape transportation, urban
  planning and mobility services.

.. admonition:: The habit this course asks of you
   :class: important

   Notice what just happened with the 94% figure. **The most-cited number in
   this field is routinely misquoted**, including by people selling things.
   That habit of checking is the first thing this course asks of you, and it
   is why the claims on these pages carry citations.


Key Terminology
---------------

The Dynamic Driving Task (DDT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **Dynamic Driving Task (DDT)** is all the real-time work of driving.
J3016 splits it into six subtasks. **You will build five of them.**

.. list-table::
   :widths: 20 55 25
   :header-rows: 1
   :class: compact-table

   * - Subtask
     - What it means
     - Course
   * - **Lateral control**
     - Steering. Holding a lane, and turning.
     - L11
   * - **Longitudinal control**
     - Acceleration and braking. Speed and gap keeping.
     - L11
   * - **OEDR: detection**
     - *Object and event detection and response.* Monitoring the environment:
       detecting and classifying objects and events, and deciding what to do.
     - L4--L6
   * - **OEDR: response**
     - Actually carrying that response out.
     - L10, L11
   * - **Maneuver planning**
     - Deciding what to do next: change lane, wait, turn, overtake.
     - L8--L10
   * - **Conspicuity**
     - Making your intent visible: lights, indicators, horn, gestures.
     - *not covered*

**What the DDT excludes is strategic**: trip scheduling, choosing a
destination, picking a route. Those stay with the human -- so a vehicle with a
flawless route planner and nothing else is not automated at all.

This term comes first because everything else in this lecture is defined in
terms of it. Levels, operating limits, fallback and safe states are all
answers to the question *who is doing which part of this*.

.. note::

   Conspicuity is a real gap in the field, not just in this course. A vehicle
   that cannot signal its intent to a human is hard to share a road with, and
   almost nobody works on it.


ADAS vs. ADS
~~~~~~~~~~~~

The same hardware can appear on both sides. What separates them is **who holds
the DDT**.

.. list-table::
   :widths: 18 41 41
   :header-rows: 1
   :class: compact-table

   * - Aspect
     - ADAS: driver support
     - ADS: automated driving
   * - **Scope**
     - **Part** of the DDT
     - **All** of the DDT, within its ODD
   * - **Who monitors**
     - The human, continuously
     - The system
   * - **Examples**
     - Adaptive cruise, lane keeping, hands-off highway
     - Robotaxi, driverless shuttle, traffic-jam pilot
   * - **Who is fallback**
     - The human, always, immediately
     - L3: the human, on request. L4--L5: the system itself
   * - **Role of the ODD**
     - May have limits, but the human covers everything outside them
     - The ODD bounds the system's responsibility
   * - **SAE levels**
     - 1 and 2
     - 3, 4 and 5

.. admonition:: The point to land
   :class: important

   Cameras, radar and a good planner do not decide which column you are in.
   **A very capable system that still requires an attentive driver is an
   ADAS.** Capability does not promote you; responsibility does. Most things
   sold with autonomy language live in the left column -- and you are building
   the right one, which is why your package is called ``ads_pipeline``.


The DDT Fallback
~~~~~~~~~~~~~~~~

The **DDT fallback** is what happens when the system can no longer do the
driving task. Two things trigger it: a **system failure**, or the vehicle
**reaching the edge of its ODD**.

.. list-table::
   :widths: 24 38 38
   :header-rows: 1
   :class: compact-table

   * - Aspect
     - Level 3
     - Levels 4 and 5
   * - **Who performs it**
     - The human, called the *fallback-ready user*
     - The system itself
   * - **How it starts**
     - A request to intervene, with a budget of seconds
     - No request. The system just acts
   * - **The human must be**
     - Receptive to that request, and able to resume driving
     - Nothing is required. There may be nobody aboard
   * - **If nobody responds**
     - The system does what it can, unaided
     - Not applicable

- **Only the first trigger is a fault.** Leaving the ODD is a planned,
  foreseeable event with nothing broken at all, and it still demands a full
  handover. **Most fallbacks in service are of the second kind.**
- **Level 3 is the hard case**, and it is a human-factors problem rather than
  a software one: you get seconds to rebuild situational awareness you stopped
  maintaining minutes ago.

.. warning::

   Keep this in mind for the :ref:`Tempe case study <l1-case-tempe>`. A human
   was the designated fallback and was not watching the road. That is the
   failure mode row three of this table is describing.


The Minimal Risk Condition (MRC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The fallback says *who* takes over. The **MRC** says *where the vehicle ends
up*. When a trip cannot be finished safely, the vehicle has to reach somewhere
safe, and that somewhere is the MRC.

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Candidate MRC
     - What it quietly assumes
   * - Stop where you are
     - Traffic behind can see you and stop in time, and you are not on a
       crossing or in a tunnel
   * - Pull to the shoulder or curb
     - A shoulder is reachable, and nothing is attached to, dragged by, or
       trapped under the vehicle
   * - Carry on to the next exit
     - Whatever failed still leaves you able to drive that far
   * - Park in a mapped safe area
     - Somebody mapped such an area in advance, and you can still reach it

**"Stop" is not automatically safe**, and neither is pulling over. Every row
above is correct in some situations and dangerous in others, so choosing well
means knowing what is around the vehicle.

.. admonition:: An MRC is a designed artifact
   :class: warning

   Somebody decided in advance what *safe* means here, wrote it into the
   software, and validated it against a list of situations they thought of.
   **If the situation is not on the list, the vehicle still does what the list
   says.** The :ref:`second case study <l1-case-mrc>` turns entirely on this.


Operational Design Domain (ODD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **Operational Design Domain** is the specific set of operating conditions
under which an ADS is designed to function safely. If the vehicle is about to
leave its ODD, it must perform the DDT fallback.

- **Geographic** -- Limited to certain highways, or a geofenced urban area.
- **Environmental** -- Restricted by weather (no heavy snow), or lighting
  (daytime only).
- **Traffic** -- Designed for specific speed limits or traffic densities.
- **Infrastructure** -- Mapped roads only, lane markings present, no active
  construction.

.. tip::

   NIST proposed the **Operating Envelope Specification (OES)**: a structured,
   machine-readable description of the driving environment that supports
   calculation-based reasoning about performance, with testing and
   certification applications.

   The easy way to keep them apart: the **ODD is the idea** of the operating
   limits; the **OES is the document** that states them, in machine-readable
   form, together with the criteria for assessing performance inside them.
   People conflate the two constantly.


SAE Levels of Driving Automation
--------------------------------

SAE defines six levels of driving automation in J3016, jointly with
ISO TC204/WG14. The standard splits them in half: **levels 0--2 are driver
support features**, **levels 3--5 are automated driving features**.


Levels 0--2: Driver Support Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In all three, **you are driving**, whatever the system is doing.

.. list-table::
   :widths: 8 20 52 20
   :header-rows: 1
   :class: compact-table

   * - Level
     - Name
     - Description and examples
     - Who drives?
   * - **0**
     - No automation
     - Human does everything. Warnings and brief interventions do not change
       that. *AEB, blind-spot warning, stability control.*
     - Human
   * - **1**
     - Driver assistance
     - Steering **or** speed, never both. *Adaptive cruise control, or
       lane-keeping assist, on most new cars.*
     - Human, assisted
   * - **2**
     - Partial automation
     - Steering **and** speed together; the human keeps watching. *Tesla
       Autopilot and FSD (Supervised), GM Super Cruise, Ford BlueCruise,
       Mercedes Drive Assist Pro.*
     - Human, supervising

- **Level 0 is the surprise.** Automatic emergency braking intervenes, it can
  save your life, and it is still Level 0 -- because you never stopped
  driving.
- **Level 2 is where almost every consumer product sits**, including several
  sold with language that suggests otherwise.

.. important::

   In all three rows the human performs or supervises the DDT. **Capability
   varies enormously across this table and the level does not move.**


Levels 3--5: Automated Driving Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From here the **system** performs the entire DDT within its ODD. What
separates the three rows is **who handles the fallback**.

.. list-table::
   :widths: 8 20 52 20
   :header-rows: 1
   :class: compact-table

   * - Level
     - Name
     - Description and examples
     - Who drives?
   * - **3**
     - Conditional automation
     - The whole driving task inside its ODD; the human takes over when asked.
       *Honda Sensing Elite (Japan). Mercedes Drive Pilot and BMW Personal
       Pilot L3 withdrawn in 2026.*
     - System, human as fallback
   * - **4**
     - High automation
     - The driving task **and** the fallback, inside its ODD. *Waymo, Zoox,
       Baidu Apollo Go, WeRide, Nuro.*
     - System, within ODD
   * - **5**
     - Full automation
     - Anywhere a human could drive, in any conditions. *No production system
       exists.*
     - System, everywhere

- **Level 3 has gone backwards.** Two of the three products named above were
  withdrawn in 2026, and Mercedes moved its effort to Level 4 instead. Asking
  a person to be ready to take over within seconds, while doing something
  else, is expensive to build and hard to rely on.
- **Level 5 is not a product category.** It is a research goal, and nothing on
  sale is close to it.

.. note::

   The examples in both tables are the most perishable content in this
   lecture. They are current as of 2026 and should be re-checked before you
   cite them.


Three Things the Levels Are Not
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 1 1 3
   :gutter: 3

   .. grid-item-card:: Not a quality ranking
      :class-card: sd-border-warning

      A Level 2 feature can be more capable, better engineered and safer than
      a Level 3 feature. The level describes *who is responsible*, not how
      good the engineering is.

      Mercedes withdrew Drive Pilot during 2026, replaced it with a **Level 2**
      system, and put its effort into Level 4 instead. A lower number is not a
      worse company.

   .. grid-item-card:: Not "what can it do"
      :class-card: sd-border-warning

      A shuttle doing one fixed loop at 15 km/h in fair weather is Level 4. So
      is a robotaxi in a large city. Same number, almost nothing in common,
      and the entire difference is in the **ODD**.

      When somebody tells you they are Level 4 and stops there, ask *where*.

   .. grid-item-card:: Not what the badge says
      :class-card: sd-border-warning

      Names are chosen to sell cars, not to describe levels. Autopilot, Full
      Self-Driving and Super Cruise are all **Level 2**.

      What sets the level is what the system actually does, and where it is
      allowed to do it.

.. admonition:: The most consequential jump is 2 to 3
   :class: important

   And it is **legal rather than technical**: responsibility for the driving
   task moves from the person to the manufacturer. That is expensive, which is
   why **Level 3 is the only level that has gone backwards**.


Industry Landscape
------------------

Where Deployment Actually Stands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Level 2

      **Everywhere.** Hands-on and hands-off highway features ship on millions
      of consumer vehicles across many manufacturers -- Tesla Autopilot and
      FSD (Supervised), GM Super Cruise, Ford BlueCruise, Mobileye
      SuperVision, Mercedes Drive Assist Pro.

   .. tab-item:: Level 3

      **Rare, and shrinking.** Certification, handover design and liability
      have kept deployments to narrow highway ODDs at low speeds. UNECE R157
      is the regulation that made the first of them possible.

      Mercedes Drive Pilot and BMW Personal Pilot were both withdrawn during
      2026. Honda Sensing Elite remains on a very small leased fleet in Japan.

   .. tab-item:: Level 4

      **Real but geofenced.** Driverless commercial robotaxi service operates
      in a limited set of metropolitan areas -- Waymo, Baidu Apollo Go, Zoox,
      WeRide, Pony.ai -- alongside low-speed shuttles, yard and port
      automation, and highway freight pilots.

   .. tab-item:: Level 5

      **Does not exist and is not close.** It remains a research goal, not a
      product category.

.. warning::

   Specific ride counts, service areas and company statuses change quarterly.
   A page with last year's figures is worse than a page with none, so any
   figure you quote in a report needs **a date attached to it**.


Structural Features Worth Knowing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Capital concentration.** The cost of validation has consolidated the field
  around a small number of very well funded players, and several
  once-prominent programs have shut down or been absorbed.
- **Two centers of gravity.** The United States and China are both deploying
  at scale, under quite different regulatory regimes.
- **Two architectural bets.** Modular pipelines with interpretable interfaces,
  versus increasingly end-to-end learned systems. **This course builds the
  former and studies the latter in L12 and L13.**


Why It Is Taking So Long: The Long Tail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The first 90% of driving is close to solved. The hard part is **rare
  events**, which are individually rare but collectively constant. You meet
  one every drive; you just never meet the same one twice.
- A system can be excellent on average and still fail on a mattress in the
  road, a police officer waving traffic through a red light, or a pedestrian
  in an unusual posture.
- **Proving safety statistically would take hundreds of millions of miles**,
  in some cases billions (Kalra & Paddock, 2016). You cannot drive that before
  deploying.

.. admonition:: Why this course lives in CARLA
   :class: important

   That last point is **arithmetic, not an engineering gap**. It is why
   simulation is a necessity here rather than a convenience.


On Disengagement Rates
~~~~~~~~~~~~~~~~~~~~~~

A **disengagement** is any moment in testing when the system stops driving and
a human takes over -- either because the system asked, or because the safety
driver decided to. **Miles per disengagement** is test miles divided by how
many times that happened.

- It is the most quoted way to compare one company against another, and close
  to useless for it.
- **The definition is subjective.** California counts a takeover when safe
  operation *requires* it, and the operator decides what that means. Two
  fleets can drive identically and report very different numbers.
- **Self-reported, and not normalized for difficulty.** Quiet suburban roads
  in fair weather beat dense city traffic, while being far less capable.
  Companies also stop reporting once the safety driver goes, **so the best
  systems leave the table.**

.. tip::

   The habit to take away: **when somebody hands you a safety number, ask what
   the denominator was.** You will need this in your final report, where you
   argue that your own scenarios were hard enough to mean anything.


Technical Challenges
--------------------

.. list-table::
   :widths: 18 62 20
   :header-rows: 1
   :class: compact-table

   * - Challenge
     - The difficulty
     - Course
   * - **Perception**
     - Seeing reliably in rain, fog, snow and glare, and recognizing events
       that appear a handful of times in a dataset
     - L2, L4--L6
   * - **Prediction**
     - Forecasting what unpredictable humans will do, when their behavior
       depends on what your vehicle does
     - L9
   * - **Planning**
     - Safe, efficient and human-legible decisions in interactive scenarios
       where hesitation is itself a hazard
     - L8, L10
   * - **Control**
     - Tracking a trajectory smoothly across varied surfaces and vehicle
       dynamics
     - L11
   * - **Validation**
     - Proving safety when the events you care about are the ones you have
       never observed
     - L13, L14
   * - **Integration**
     - Making the subsystems above work together with redundancy, timing
       guarantees and cybersecurity
     - L14

.. admonition:: What this table really is
   :class: note

   Every row is a lecture *and* a piece of your project. By December you will
   have built something that fails at each of them, and the interesting part
   of your final report is explaining **how** it failed.


Safety and Regulation
---------------------

Key Safety Standards
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Standard
     - Scope
   * - **ISO 26262**
     - **Things that break.** A sensor fails, a chip flips a bit, code
       crashes. Called *functional safety*. It ranks each hazard with an
       Automotive Safety Integrity Level (**ASIL**) so the riskiest ones get
       the most engineering.
   * - **ISO 21448**
     - **Things that work exactly as designed and still cause a crash.** The
       camera is not broken; the sun is just directly behind the traffic
       light. Called **SOTIF**.
   * - **ISO/SAE 21434**
     - **Things an attacker does on purpose.** Automotive cybersecurity, and
       the subject of the
       :doc:`cybersecurity pre-read </preread/cybersecurity>` before L14.

Both kinds of hazard are real, and **finding them takes completely different
work**.

.. admonition:: SOTIF is the one to remember
   :class: important

   Your detector will not crash. It will confidently return the **wrong
   answer**, and everything downstream will believe it. That is a SOTIF
   hazard, and it is what the case studies below are about.


Regulatory Landscape
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 80
   :class: compact-table

   * - **United States**
     - No comprehensive federal AV legislation; NHTSA guidance plus a
       state-by-state patchwork.
   * - **European Union**
     - Type approval, with UNECE R157 covering Level 3 highway systems.
   * - **China**
     - Its own rapidly developing framework, enabling deployment at scale.
   * - **International**
     - Work toward a harmonized, **safety-case-based** framework for ADS is
       underway at UNECE. Check the current status before citing it.

A survey of which standards apply where, and which performance metrics go with
them, is in **NIST IR 8527** (free to download -- see :doc:`l1_references`).


.. _l1-concept-to-road:

From Concept to Public Roads
----------------------------

Getting an ADS onto a public road is **not a release**. It is a negotiation
between a developer, a set of standards bodies, and a regulator. Seven stages:

1. **Framework** -- standards bodies publish; regulators adopt or reference
   them.
2. **Specify** -- define the ODD, formalize it as an OES, then run HARA, SOTIF
   analysis and TARA.
3. **Build** -- architecture, data collection, model training, unit and module
   verification.
4. **Validate** -- scenario-based simulation, then closed course, then
   supervised on-road testing with a safety driver.
5. **Argue** -- assemble a safety case (claims, arguments, evidence) and
   submit it, often via an independent assessor.
6. **Approve** -- the regulator reviews against the *claimed ODD* and grants,
   conditions or denies.
7. **Operate and monitor** -- field data, mandatory incident reporting, OTA
   updates, and investigation when something goes wrong.

.. admonition:: Two things to watch for
   :class: important

   **Stage 4 is where almost all the calendar time goes**, and the vehicle is
   still operating at **Level 2** the whole way through it. And **every
   software update in Stage 7 changes the system that the approval in Stage 6
   was granted for.**


Stage 1 of 7 -- Framework
~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L1/concept_road1.png
   :alt: Sequence diagram. Standards bodies send the J3016 taxonomy and the ISO safety and cybersecurity standards to the developer, and harmonized regulations to the regulator, which then adopts, references or ignores them.
   :align: center
   :width: 95%
   :class: white-figure

   Standards bodies publish, and nothing binds until a regulator adopts.

- Standards bodies write the rulebooks. **Nobody has to follow them.**
- A rulebook only becomes law when a government adopts it. Until then,
  following it is a business decision, not a legal one.
- That is why the same vehicle can be legal in one country and illegal in
  another, with no change to the software.

J3016 gives everyone the same **words**. ISO 26262, ISO 21448 and
ISO/SAE 21434 give everyone the same **process**. None of them is a law.


Stage 2 of 7 -- Specify
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L1/concept_road2.png
   :alt: Sequence diagram with six participants, of which only the developer sends or receives anything. The developer defines the ODD, formalizes it as an OES, then performs hazard analysis and risk assessment, SOTIF analysis, and threat analysis and risk assessment.
   :align: center
   :width: 85%
   :class: white-figure

   The ODD and the hazard analyses, written with nobody outside the room.

**Three analyses, and each one produces something the next stages have to
build:**

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - Analysis
     - What it asks, and what it produces
   * - **HARA** (ISO 26262)
     - What happens if a part **breaks**? Produces safety goals carrying an
       **ASIL** rating that decides how much redundancy and testing each
       function gets.
   * - **SOTIF** (ISO 21448)
     - What happens when **nothing breaks**? Produces the list of
       **triggering conditions** that becomes the test library in Stage 4.
   * - **TARA** (ISO/SAE 21434)
     - What could an **attacker** do? Produces security goals.

So this is not paperwork. **Stage 3 builds to these requirements and Stage 4
tests against these scenarios.** The ODD is written here too, and turned into
an OES.

.. warning::

   **Notice that five of the six lifelines are empty.** All of it happens
   inside one company. If the ODD is too optimistic, nobody outside says so
   until Stage 5 -- and by then it is expensive.


Stage 3 of 7 -- Build
~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L1/concept_road3.png
   :alt: Sequence diagram. The developer designs the architecture, requests scenarios and synthetic data from simulation, receives labeled data, trains models, and performs unit and module verification.
   :align: center
   :width: 90%
   :class: white-figure

   Building the system, with simulation as a data source rather than a test rig.

- Simulation shows up here, and **not just as a place to run tests**. It is
  where the **training data** comes from. Labels are free in simulation and
  expensive everywhere else.
- **This is the only stage your projects live in.** GP1--GP4 are architecture,
  data, training and testing your own modules.
- **Verification** asks whether you built the thing correctly.
  **Validation** -- next stage -- asks whether it was the right thing to
  build. You can pass one and fail the other.


Stage 4 of 7 -- Validate
~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L1/concept_road4.png
   :alt: Sequence diagram. The developer sends a scenario library to simulation, which runs model, software and hardware in the loop testing with fault injection and returns coverage and failure reports, then closed course testing, then a supervised on-road testing loop with a safety driver, disengagement data and periodic reports to the regulator.
   :align: center
   :width: 95%
   :class: white-figure

   Simulation, then closed course, then years of supervised road testing at Level 2.

- The test scenarios come **from the ODD**. So a vague ODD in Stage 2 gives
  you a weak test set here, **and nobody notices**.
- **Most of the years spent building one of these are spent in that box**, and
  the whole time the vehicle is running at Level 2 with a person watching the
  road.
- You cannot prove safety by driving alone. So the simulation half is not a
  shortcut -- it is the only half that can reach the numbers.
- **Your final report is a small version of this stage**: scenarios you have
  not seen, real numbers, and an honest account of what broke.


Stage 5 of 7 -- Argue
~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L1/concept_road5.png
   :alt: Sequence diagram. The developer assembles a safety case of claims, arguments and evidence, submits it to an independent assessor, receives findings and required remediation, remediates, and then submits a petition, permit application or type approval to the regulator.
   :align: center
   :width: 90%
   :class: white-figure

   Assembling the safety case, and the first time anyone outside the company reads it.

- A **safety case** is an argument, written down. Three parts: what you
  promise the vehicle will not do, why you believe that, and the test results
  that back up each reason.
- **A folder full of test results is not a safety case.** It never says what
  the results were supposed to prove.
- The independent assessor is here **because Stage 2 happened behind closed
  doors**. This is the first time anyone outside the company reads the ODD and
  asks whether the argument holds up.

.. note::

   Keep this vocabulary. Both case studies below are best described as
   failures of the **argument** rather than failures of the code. In neither
   case did anything malfunction.


Stage 6 of 7 -- Approve
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L1/concept_road6.png
   :alt: Sequence diagram with an alternative block. The regulator reviews against the claimed ODD; if approved it issues a driverless testing permit and then a deployment permit and the vehicle operates on public roads, otherwise it issues a denial or conditions and the developer remediates and resubmits.
   :align: center
   :width: 95%
   :class: white-figure

   The regulator reviews against the ODD the developer claimed, and approves, conditions, or denies.

- **The regulator checks the vehicle against the ODD the company claimed**,
  not against driving in general. Claim a small ODD and approval is easy but
  the product is nearly useless. Claim a big one and you have to prove much
  more. **That trade-off drives a lot of behavior in this industry.**
- Approval comes in steps: first a permit to drive with nobody in the vehicle,
  then a separate permit to charge passengers.
- In the US there is no single national law, just federal guidance plus fifty
  state rules. The EU uses type approval, with UNECE R157 for Level 3 on
  highways.


Stage 7 of 7 -- Operate and Monitor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L1/concept_road7.png
   :alt: Sequence diagram. Public roads return field data and incident reports to the developer, which files mandatory incident reports with the regulator and pushes over-the-air updates; on a serious incident the regulator investigates, issues findings, and may order a recall or suspend a permit, sending the developer back to the specification stage.
   :align: center
   :width: 95%
   :class: white-figure

   Operating, reporting, updating, and the loop back to the ODD when something goes wrong.

- **Every software update changes the vehicle that was approved.** The permit
  was granted for one version, running in one ODD. Nobody has a good answer
  for this yet -- it is a live argument in the field, not a settled one.
- Reporting crashes is required by law, and **how you report is part of the
  law too**. One of the two crashes below ended with a company losing its
  permits over what it left out of the report, **not over the crash**.
- Look at the arrow at the bottom. A serious crash does not send you back to
  fix a bug. **It sends you back to the ODD and the hazard list.**


AV Case Studies: Learning from Real-World Incidents
---------------------------------------------------

Two incidents, both thoroughly investigated in public. In class you were given
what the vehicle perceived and did, and asked to diagnose it *before* the
investigators' conclusions were revealed.

.. admonition:: The two questions, every time
   :class: important

   1. Which module failed: perception, tracking, prediction, planning,
      control, or the system-level safety layer?
   2. **Would fixing that module alone have prevented the outcome?**

   Question 2 is the one that matters, and **the answer is almost never yes**.


.. _l1-case-tempe:

Uber ATG Fatality (Tempe, AZ -- March 2018)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What happened, without the conclusions.** A developmental test vehicle in
automated mode, at night, on a straight multi-lane road, traveling at about
43 mph. A pedestrian is walking a bicycle across the road, outside a
crosswalk. A vehicle operator occupies the driver's seat. Timings are from the
NTSB investigation (NTSB/HAR-19/03).

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Time to impact
     - What the system did
   * - **~5.6 to 6 s**
     - Radar and LiDAR first register the pedestrian.
   * - **6 to 1.3 s**
     - The object is classified, then reclassified, several times: as an
       unknown object, as a vehicle, then as a bicycle. The expected future
       travel path changes with each reclassification.
   * - **1.3 s**
     - The system determines that an emergency braking maneuver is needed.
   * - **1.3 to 0.3 s**
     - Braking is **suppressed for one second by design**, to avoid erratic
       behavior from false positives. The operator is expected to intervene.
   * - **Impact**
     - The vehicle has not braked. The operator has not intervened.

.. admonition:: Before you read on
   :class: tip

   Which module(s) failed? What is the single change you would make? Would
   that change alone have been enough?

.. dropdown:: What the investigation found
   :icon: search
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. list-table::
      :widths: 25 75
      :header-rows: 1
      :class: compact-table

      * - Layer
        - Finding
      * - **Perception**
        - The pedestrian was detected early but never stably classified.
      * - **Tracking**
        - Each reclassification reset the object's history, so no consistent
          track and no stable predicted path was ever established. **This is
          the technical heart of it.**
      * - **Planning**
        - One second of action suppression delayed braking past the point
          where it could help.
      * - **Human factors**
        - The operator was not monitoring the road.
      * - **System design**
        - The vehicle's factory automatic emergency braking was disabled while
          under computer control, and nothing replaced it.
      * - **Organizational**
        - Inadequate safety risk assessment procedures, ineffective oversight
          of vehicle operators, and no adequate mechanism for addressing
          automation complacency -- all consequences of an inadequate safety
          culture.
      * - **Road user**
        - The NTSB also found that the pedestrian's drug impairment and her
          crossing outside a crosswalk contributed.

   **Answer to question 2: no.** Fix the classifier and action suppression
   still delays the brake. Fix suppression and an unstable track still gives
   the planner nothing to act on.

   Note the last row: **the investigators did not assign this to the machine
   alone**, which is what a genuinely multi-causal finding looks like.

.. admonition:: You will build this exact failure
   :class: warning

   Track-level fusion in **GP3** must keep an object's identity *across*
   changes of class label. If your tracker throws away an object's history
   whenever the classifier changes its mind, **you have reproduced Tempe**.


.. _l1-case-mrc:

The Minimal Risk Condition (San Francisco -- October 2023)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Set-up.** A driverless robotaxi in a dense city at night. A pedestrian is
struck by a *different*, human-driven vehicle and is thrown into the
robotaxi's path. The robotaxi cannot avoid contact. It detects the collision
and comes to a stop.

**The question, before you hear what happened.** The vehicle has stopped in a
live traffic lane after a collision. It must now reach a minimal risk
condition.

- What should the MRC be here? **Write your answer down before opening the box
  below.**
- What does your answer assume about the state of the world around the
  vehicle?
- What sensing would you need to verify that assumption?

.. dropdown:: What happened
   :icon: search
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The vehicle executed a **pullover maneuver** and dragged the pedestrian,
   who was pinned underneath it, roughly twenty feet.

   **Your three answers:**

   - **What should the MRC be?** You may well have written "pull over". So did
     the engineers -- and it was correct for every scenario anyone had
     enumerated.
   - **What did that assume?** That nothing was attached to, dragged by, or
     trapped under the vehicle. *That assumption is literally a row in the
     minimal risk condition table above.*
   - **What sensing would verify it?** The deployed fix added **no sensor**:
     the recall changed the minimal risk condition so the vehicle now stays
     put after a collision instead of pulling over. **When you cannot sense an
     assumption, delete the assumption.**
   - **And afterwards.** The reports filed with regulators described the
     collision but left out the pullover and the drag. The one-day and ten-day
     filings both omitted it; it appeared a month later. State regulators
     suspended the company's testing and deployment permits, the company later
     resolved a federal charge of submitting a false report, and it ultimately
     lost its robotaxi business. **The collision was survivable as a company.
     The reporting was not.**

.. admonition:: The lesson is not "do not pull over"
   :class: important

   It is that **the minimal risk condition is a design artifact**, validated
   against a list of situations somebody thought of -- and this one was not on
   the list. **Nothing failed**: every component did exactly what it was
   designed to do. That is a **SOTIF** hazard.

Both incidents were **system** failures rather than **algorithm** failures.
That distinction is the sixth learning outcome of this course, and it is what
the final report is graded against.


The Semester Ahead
------------------

.. figure:: /_static/images/L1/pipeline.png
   :alt: Block diagram of the ADS pipeline. Sensing (L2, GP1) feeds Perception (L4 to L6, GP2), which feeds Fusion and Localization (L3, L7, GP3), which feeds Prediction (L9), then Planning (L8, L10, GP4), then Control (L11, GP4), then Integration and Safety (L14, final report).
   :align: center
   :width: 100%
   :class: white-figure

   The ADS pipeline you will build, with the lecture that teaches each stage
   and the project that implements it.

**The pipeline you will build**

- **Sensing** (L2) -- cameras, LiDAR, RADAR, IMU, GNSS, and the calibration
  that makes them agree with each other.
- **Perception** (L4--L6) -- detection, bird's-eye-view representations,
  segmentation, multi-object tracking.
- **State estimation** (L3, L7) -- Kalman filtering, sensor fusion,
  localization and SLAM.
- **Decision** (L8--L10) -- route planning, behavior prediction, motion
  planning.
- **Action** (L11) -- trajectory generation and control.
- **Frontier and safety** (L12--L14) -- end-to-end driving, world models,
  system integration and safety cases.

**L12 and L13 sit alongside this rather than inside it**: end-to-end driving
and world models are the alternative to the modular pipeline you are building,
and you should be able to argue about the trade-off by December.

.. note::

   **One package, extended four times.** By the last week you will run it on
   scenarios you have never seen, and write down honestly where it broke. See
   the :doc:`syllabus </syllabus/index>` for the full grade breakdown, the
   project schedule and the policies.


Next: The Simulator
-------------------

.. note::

   **CARLA is introduced in L2, not here.** The simulator's client-server
   architecture, the course ROS 2 bridge, the limits of its fidelity, and your
   first sensor suite in simulation are all covered next week alongside sensor
   technologies and calibration.

   What you need to do *this* week is get it installed: follow the
   :doc:`setup guide </carla/carla>` for your Ubuntu version. **The download
   alone is substantial, so start now** -- the Week 3 setup milestone requires
   CARLA running, a ROS 2 workspace built, and sensors publishing.
