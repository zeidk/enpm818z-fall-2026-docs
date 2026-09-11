====================================================
Pre-Read: Simulation for Automated Driving
====================================================

.. admonition:: Read this after Lecture 2
   :class: important

   L2 introduces CARLA and spawns your first sensor suite. This page is the
   context around it: **why** the industry simulates at all, what simulation
   can and cannot tell you, how it is done in production, and what exists
   besides CARLA.

   Read it once the lecture has given you something concrete to attach it to,
   and **before you start GP1**. The engineering of scenario-based testing --
   how scenarios are specified, sampled, executed and scored -- is developed
   properly in :doc:`L13 </lectures/lecture13/l13_index>`.


Why Simulation Is Not Optional
------------------------------

Simulation in automated driving is not a cost saving or a convenience for
people without a test track. It is the only way to obtain the evidence a
safety argument needs.

**1. You cannot drive far enough.**
Human drivers in the US average roughly one fatality per 100 million miles.
Demonstrating *statistically* that a vehicle is as safe as a human would take
on the order of 275 million miles; showing it is 20% safer takes around 11
billion. A 100-vehicle fleet driving continuously covers about 22 million
miles a year, so the second claim is roughly 500 fleet-years. And every
software release resets the argument, because the system you measured is no
longer the system you are shipping (`Kalra & Paddock, 2016
<https://doi.org/10.1016/j.tra.2016.09.010>`__).

**2. Rare events do not arrive on schedule.**
The situations that matter most -- a child stepping out from between parked
cars, a stopped fire truck over a crest, a mattress on the highway -- are
exactly the ones you cannot wait for and must not stage on a public road. In
simulation you can run one a thousand times, vary it systematically, and harm
nobody.

**3. Ground truth is free.**
A simulator placed every object in the scene, so it knows precisely where each
one is. That is what makes labelled training data cheap, and it is the only
reason GP2 is possible: you will collect and label a dataset in an afternoon.
On real data, that labelling is the expensive part.

**4. Runs are repeatable.**
A failure you cannot reproduce is a failure you cannot fix. In synchronous
mode a simulated scenario replays identically, so you can change one thing and
attribute the difference to it. Public-road testing gives you the opposite:
every run is a different run.

.. note::

   These four arguments are why *simulation* exists. They do not yet tell you
   **which** situations to simulate, or how to know when you have simulated
   enough. That question -- scenario-based testing -- is L13, and it is the
   harder half.


What Simulation Is Not
----------------------

A simulator is a model, and the useful question is always which parts of it
you are entitled to trust.

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: compact-table

   * - Trust level
     - What falls here in a modern simulator
   * - **Modelled well**
     - Geometry, road networks, traffic rules, actor kinematics, sensor
       placement and extrinsics, timing and message flow, gross weather.
   * - **Modelled roughly**
     - Material appearance and reflectance, LiDAR returns in rain and fog,
       RADAR multipath, camera artifacts such as bloom, rolling shutter and
       lens flare.
   * - **Not modelled**
     - Sensor degradation and dirt, calibration drift, hardware faults, the
       full variety of human behaviour, and the appearance statistics a real
       deployment actually encounters.

The distributional mismatch between simulated and real sensor data is the
**sim-to-real gap**. Two standard mitigations are *domain randomization*
(deliberately varying textures, lighting and noise during training so the
model cannot depend on any of them) and *domain adaptation* (explicitly
mapping between the two distributions, or fine-tuning on real data).

.. warning::

   **The skills transfer completely. The weights do not.** A detector trained
   only on CARLA imagery will not work on real driving footage without
   adaptation. In your final report, "we achieve 0.83 mAP" is a claim about
   CARLA, and writing it as a claim about driving is an error that will be
   marked as one.


How Industry Actually Does It
-----------------------------

Scale
~~~~~

Waymo's simulator began as **Carcraft** and became **Simulation City**
(`announced July 2021 <https://waymo.com/blog/2021/07/simulation-city/>`__).
The published figures give a sense of the ratio the industry works at: around
25,000 virtual vehicles driving roughly 10 million simulated miles per day,
about 10 billion cumulative simulated miles by 2019 and roughly 15 billion by
2020 -- against approximately 20 million real autonomous miles in the same
period. That is on the order of **750 simulated miles for every real one**.

In February 2026 Waymo announced the `Waymo World Model
<https://waymo.com/blog/2026/02/the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation/>`__,
a generative approach to the same problem. Learned simulators are covered in
L13.

Where each test runs
~~~~~~~~~~~~~~~~~~~~

Production programmes run a **test pyramid**. Cost per scenario rises by
orders of magnitude down the levels, and realism rises with it, so millions of
scenarios run at the top and a handful at the bottom.

.. list-table::
   :widths: 18 40 42
   :header-rows: 1
   :class: compact-table

   * - Level
     - What is real
     - What it catches
   * - **MIL**
     - The model only, no production code.
     - Algorithm logic.
   * - **SIL**
     - The real software, simulated sensors and vehicle.
     - **This is CARLA, and this is where every project in this course
       lives.** Misses timing and hardware faults.
   * - **HIL**
     - Real ECUs and real timing; simulated world.
     - Latency, scheduling, resource limits.
   * - **VIL**
     - A real vehicle on a rig or pad, fed synthetic objects.
     - Real dynamics and actuation, safely.
   * - **Proving ground**
     - Everything, in a controlled place.
     - Real physics. Slow and expensive.
   * - **Public road**
     - Everything, uncontrolled.
     - The long tail, at the cost of exposing the public to it.

Two ways of using recorded data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Re-simulation** (log replay) plays a recorded drive back against a new
software build. It is the regression test of AV development: it proves you
have not broken what previously worked. It is *open loop* -- the recording
does not react to your decisions -- so it cannot tell you whether the system
can drive, only whether it still perceives.

**Closed-loop simulation** lets the system's decisions change what happens
next, so errors compound as they do on a road. It is the only way to observe
recovery, and the only setting in which a driving score means anything.

Where the scenarios come from
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not from imagination. From the **ODD** (every condition you claimed to handle
is a condition you must test), from **SOTIF triggering conditions**, from
**field data** (crash databases, disengagement reports, near-miss mining), and
from **re-simulation** of drives already recorded.


The Open-Source Landscape
-------------------------

.. list-table::
   :widths: 16 12 30 42
   :header-rows: 1
   :class: compact-table

   * - Tool
     - Status
     - Built for
     - Notes
   * - `CARLA <https://carla.org/>`__
     - Active
     - Full-stack AV research: sensors, traffic, maps, scenarios.
     - Unreal Engine; the course simulator. Python API, ROS 2, OpenDRIVE
       maps. `CoRL 2017 paper
       <https://proceedings.mlr.press/v78/dosovitskiy17a.html>`__.
   * - `AWSIM <https://github.com/autowarefoundation/AWSIM>`__
     - Active
     - Autoware development specifically.
     - Unity-based, from TIER IV. Needs no extra middleware layer to talk to
       Autoware. The natural pairing if you work with Autoware rather than a
       stack of your own.
   * - `SUMO <https://eclipse.dev/sumo/>`__
     - Active
     - Microscopic **traffic flow**, city scale.
     - Not a sensor simulator. Models thousands of vehicles as a traffic
       system, and co-simulates with CARLA to give it realistic surrounding
       traffic.
   * - `esmini <https://github.com/esmini/esmini>`__
     - Active
     - Playing and debugging **OpenSCENARIO** files.
     - Lightweight. The quickest way to see what a scenario file actually
       describes, without a full game engine.
   * - `MetaDrive <https://github.com/metadriverse/metadrive>`__
     - Active
     - Reinforcement learning and generalization research.
     - Procedurally generates unlimited driving scenes; very fast, visually
       simple. Built for training thousands of episodes, not for photorealism.
   * - `highway-env <https://github.com/Farama-Foundation/HighwayEnv>`__
     - Active
     - Behavioural decision-making, 2-D.
     - Minimal and abstract: merges, roundabouts, intersections. Good for
       studying *policy* without any perception at all.
   * - `Waymax <https://github.com/waymo-research/waymax>`__
     - Active
     - Large-scale closed-loop **planning** research.
     - JAX-based and very fast; data-driven, built on the Waymo Open Motion
       Dataset. Non-commercial licence. `Project page
       <https://waymo.com/research/waymax/>`__.
   * - `nuPlan <https://github.com/motional/nuplan-devkit>`__
     - Active
     - Closed-loop **planning benchmark**.
     - From Motional. Scenario-based planning metrics with reactive agents.
   * - `AlpaSim <https://github.com/NVlabs/alpasim>`__
     - Active
     - Closed-loop testing of **end-to-end** driving policies.
     - From NVIDIA, part of the Alpamayo initiative. Built as networked
       microservices (renderer, physics, traffic, controller, driver), so the
       policy under test closes the loop against generated sensor data.
   * - `SVL / LGSVL <https://github.com/lgsvl/simulator>`__
     - **Discontinued**
     - (was) High-fidelity AV simulation, Unity-based.
     - Archived in 2022. Still cited constantly in papers; do not start
       anything new on it.
   * - `AirSim <https://github.com/microsoft/AirSim>`__
     - **Discontinued**
     - (was) Drones and ground vehicles, Unreal-based.
     - Archived by Microsoft. Same caution as SVL.

.. warning::

   **Two of the most-cited simulators in the literature are dead.** SVL/LGSVL
   and AirSim appear throughout papers from 2019--2022 and are no longer
   maintained. If you are reading a paper that builds on either, treat its
   tooling as unavailable. CARLA and AWSIM are the actively developed
   open-source options.

.. note::

   **A name clash worth knowing.** MIT's **VISTA** is a data-driven
   photorealistic simulator built from recorded driving. **Vista** (Gao et
   al., NeurIPS 2024) is a generative driving *world model*. Different things,
   same name, both discussed in the literature you will meet in L13.


Commercial Tooling
------------------

Open source is not the whole industry. Most production programmes buy at least
part of their simulation stack, and these are names you will meet in job
descriptions.

**NVIDIA** is the one worth understanding in detail, because its stack shows
where the field is going. `DRIVE Sim
<https://developer.nvidia.com/drive/simulation>`__ is the proprietary
simulation platform, built on Omniverse -- a deliberate move from a *game*
engine to a *simulation* engine. Around it sits a pipeline that no longer
looks like classical simulation at all:

- **NuRec** reconstructs real multi-sensor drives into 3-D scenes by neural
  reconstruction, rather than having an artist build them.
- **Cosmos** world foundation models then generate variations of those
  scenes -- new weather, new agents, new outcomes.
- **AlpaSim** closes the loop, running the policy under test against the
  result. This part is open source, and is in the table above.

That chain -- *record, reconstruct, vary, re-run closed-loop* -- is the same
argument L13 makes about world models, implemented as a product.

Others you will encounter:

.. list-table::
   :widths: 24 76
   :header-rows: 1
   :class: compact-table

   * - Tool
     - What it is for
   * - `Applied Intuition <https://www.appliedintuition.com/>`__
     - Toolchain for scenario libraries, triage and large-scale re-simulation.
       Widely used by OEMs building their own stacks.
   * - `Foretellix <https://www.foretellix.com/>`__
     - Coverage-driven verification: describe scenarios abstractly, generate
       many concrete variants, and measure coverage rather than count runs.
       Closely tied to OpenSCENARIO 2.0.
   * - `IPG CarMaker <https://www.ipg-automotive.com/en/products-solutions/software/carmaker>`__
     - Vehicle dynamics and HIL, long established in automotive engineering.
   * - `dSPACE <https://www.dspace.com/en/pub/home.cfm>`__
     - HIL rigs and simulation models; the classic supplier for testing real
       ECUs against a simulated vehicle.
   * - `rFpro <https://rfpro.com/>`__
     - Physically accurate rendering for sensor simulation, from a motorsport
       simulation background.
   * - `Cognata <https://www.cognata.com/>`__
     - Synthetic data generation and sensor simulation for ADAS/AV validation.

.. note::

   You do not need any of these for this course. They are here so the names
   are familiar, and so the open-source table is not mistaken for a survey of
   the whole field.


Formats and Standards
---------------------

A scenario is only useful if another organisation can run it and get the same
thing. Two ASAM formats do that work:

- **OpenDRIVE** describes the *road*: geometry, lanes, signals. CARLA maps are
  built from it, and L8 routing consumes it.
- **OpenSCENARIO** describes *what happens on the road*: actors, manoeuvres,
  triggers. See `ASAM
  <https://www.asam.net/standards/detail/openscenario/>`__.

The **ISO 34500 series** now governs scenario-based evaluation: 34501
(vocabulary), **34502** (the safety evaluation framework), 34503 (how to write
an ODD as a taxonomy), 34504 (scenario categorization) and 34505 (test case
generation). The existence of an international standard for *how to write down
your ODD* is itself the point: scenario-based validation is now the expected
method, not a good idea.


Reading
-------

Essential
~~~~~~~~~

- Kalra & Paddock (2016), *Driving to Safety: How Many Miles of Driving Would
  It Take to Demonstrate Autonomous Vehicle Reliability?*
  `DOI <https://doi.org/10.1016/j.tra.2016.09.010>`__ -- the mileage argument
  that motivates everything on this page.
- Dosovitskiy et al. (2017), *CARLA: An Open Urban Driving Simulator*,
  `CoRL <https://proceedings.mlr.press/v78/dosovitskiy17a.html>`__ -- the
  simulator you will use all semester.

If you want more
~~~~~~~~~~~~~~~~

- `CARLA Foundations <https://carla.readthedocs.io/en/0.9.16/foundations/>`__
  and the `Sensor reference
  <https://carla.readthedocs.io/en/0.9.16/ref_sensors/>`__ -- the two pages to
  bookmark before L2.
- `Synchrony and time-step
  <https://carla.readthedocs.io/en/0.9.16/adv_synchrony_timestep/>`__ -- short,
  and it will save you a week of GP1 debugging.
- `CARLA Leaderboard evaluation rules
  <https://leaderboard.carla.org/evaluation_v2_1/>`__ -- the metrics GP4 is
  graded with.
- Gao et al. (2024), *Vista: A Generalizable Driving World Model*,
  `arXiv <https://arxiv.org/abs/2405.17398>`__.
- NVIDIA (2025), *Cosmos World Foundation Model Platform for Physical AI*,
  `arXiv <https://arxiv.org/abs/2501.03575>`__.


Where This Appears in the Course
--------------------------------

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - Where
     - What it is used for
   * - :doc:`L2 </lectures/lecture2/l2_index>`
     - CARLA's architecture, synchronous mode, spawning a sensor suite, and
       the limits of what it models.
   * - :doc:`L13 </lectures/lecture13/l13_index>`
     - Scenario-based testing in full: scenario layers, sampling, the test
       pyramid, driving scores, and world models.
   * - GP1--GP4
     - Every project runs in CARLA. GP4 is scored with route completion,
       collisions and infractions on provided scenarios.
   * - Final report
     - You must state which level of the test pyramid your numbers come from,
       and report where the system broke rather than a pass rate.
