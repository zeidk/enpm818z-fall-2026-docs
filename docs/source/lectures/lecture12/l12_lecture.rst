====================================================
Lecture
====================================================


The Fundamental Debate: Modular vs. End-to-End
-----------------------------------------------

The autonomous driving community has long debated two competing architectural
philosophies for building a complete ADS stack.

.. tab-set::

   .. tab-item:: Modular Pipeline

      The **modular pipeline** decomposes the driving task into a sequence of
      specialized subsystems:

      1. **Perception** -- Detects and classifies objects, estimates 3-D bounding
         boxes, segments the scene.
      2. **Prediction** -- Forecasts future trajectories of agents.
      3. **Planning** -- Generates a safe, comfortable trajectory for the ego
         vehicle.
      4. **Control** -- Converts the planned trajectory into actuator commands
         (steering, throttle, brake).

      Each module is developed and validated independently, with structured
      intermediate representations (object lists, maps, trajectories) passed
      between stages.

   .. tab-item:: End-to-End

      An **end-to-end** (E2E) system replaces the hand-engineered pipeline with
      a single model (or tightly coupled set of models) that maps raw sensor
      inputs directly to driving actions or waypoints.

      - Sensors (cameras, LiDAR, radar) feed directly into a neural network.
      - The network learns all intermediate representations implicitly.
      - The output is typically a set of planned waypoints or direct actuator
        commands.

.. list-table:: Modular vs. End-to-End Trade-offs
   :widths: 25 38 37
   :header-rows: 1
   :class: compact-table

   * - Dimension
     - Modular Pipeline
     - End-to-End
   * - **Interpretability**
     - High -- each module can be inspected
     - Low -- internal representations are opaque
   * - **Debuggability**
     - Failures are localizable to a module
     - Hard to attribute failures to causes
   * - **Joint optimization**
     - Absent -- each module optimized separately
     - Full -- gradients flow across the entire stack
   * - **Information loss**
     - Present at each module boundary
     - Minimal -- raw data preserved throughout
   * - **Data requirements**
     - Moderate per module
     - Massive -- billions of labeled driving miles
   * - **Validation**
     - Module-level + integration testing
     - Requires comprehensive scenario coverage
   * - **Regulatory acceptance**
     - Mature frameworks available
     - Open research question


Information Loss at Module Boundaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A key theoretical argument for end-to-end approaches is the **information loss
problem**: when perception outputs a discretized object list, geometric
uncertainty, rare edge cases, and subtle scene context that did not fit the
output schema are permanently discarded before the planner ever sees them.

.. admonition:: Example
   :class: note

   A modular system that represents a pedestrian as a 3-D bounding box cannot
   convey that the pedestrian is holding a ball that may roll into the road.
   An end-to-end system working on raw images can, in principle, learn to
   condition its plan on such subtle visual cues.


UniAD: Planning-Oriented Autonomous Driving (CVPR 2023)
-------------------------------------------------------

UniAD was a landmark result that demonstrated that **unifying all driving tasks
in a single end-to-end model** outperforms carefully tuned specialized modules
on every sub-task.

Architecture
~~~~~~~~~~~~

UniAD introduces a hierarchical query-based architecture built on a shared BEV
backbone:

.. code-block:: text

   Camera inputs (multi-view)
         |
   BEV Feature Encoder (BEVFormer)
         |
   ┌─────┴──────────────────────────────────────────┐
   │  TrackFormer   → Agent Tracking Queries        │
   │  MapFormer     → Map Element Queries           │
   │  MotionFormer  → Multi-modal Motion Queries    │
   │  OccFormer     → Occupancy Grid Queries        │
   │  Planner       → Ego Trajectory Waypoints      │
   └────────────────────────────────────────────────┘

Each downstream module receives **queries** -- learned embeddings that
accumulate task-specific features from the shared BEV representation via
cross-attention.

Key Contributions
~~~~~~~~~~~~~~~~~

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Unified Query Propagation
      :class-card: sd-border-info

      Agent tracking queries flow downstream to the motion forecasting module,
      which then informs occupancy prediction, which informs the planner. This
      creates an explicit information flow that mimics the intuitive reasoning
      chain a human driver uses.

   .. grid-item-card:: Planning-Centric Loss
      :class-card: sd-border-info

      All sub-task losses are co-optimized with a planning loss, so every
      component is incentivized to produce representations that ultimately
      improve the planned trajectory rather than just maximizing its own
      metric in isolation.

   .. grid-item-card:: CVPR 2023 SOTA
      :class-card: sd-border-info

      UniAD achieved state-of-the-art results on nuScenes across tracking,
      mapping, motion prediction, occupancy, and planning simultaneously --
      the first single model to do so.

   .. grid-item-card:: Influence
      :class-card: sd-border-info

      UniAD became the foundation for a wave of follow-on work (SparseDrive,
      DriveTransformer) and is widely cited as the model that proved the
      end-to-end paradigm works at the systems level.

Performance Snapshot
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 35 35 30
   :header-rows: 1
   :class: compact-table

   * - Task
     - Metric
     - UniAD Result
   * - 3-D Object Tracking
     - AMOTA
     - 0.359
   * - Motion Forecasting
     - minADE (5s)
     - 0.607 m
   * - Occupancy Prediction
     - IoU (occluded)
     - 42.5%
   * - Planning (L2, 3s)
     - Average L2 distance
     - 0.25 m


DriveTransformer (ICLR 2025)
-----------------------------

DriveTransformer extended the UniAD paradigm with a key architectural
insight: **a single set of attention operations can simultaneously serve all
driving tasks** rather than using separate specialized decoder heads.

Shared Attention Mechanism
~~~~~~~~~~~~~~~~~~~~~~~~~~

In UniAD, each task head applies cross-attention to the BEV features
independently. DriveTransformer instead defines **three unified token types**:

- **Agent tokens** -- represent moving objects (vehicles, pedestrians).
- **Map tokens** -- represent static scene elements (lanes, crosswalks).
- **Ego token** -- represents the autonomous vehicle itself.

All tokens attend to each other and to raw sensor features in a **single
joint attention block**, repeated across multiple layers.

.. admonition:: Why This Matters
   :class: tip

   By sharing attention computations across tasks, DriveTransformer eliminates
   the redundant feature extraction that each separate head in UniAD performs.
   This leads to a **3x throughput improvement** over UniAD at equivalent
   performance -- a critical difference for real-time deployment where inference
   must complete in under 50 ms.

Throughput Comparison
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 35 30 35
   :header-rows: 1
   :class: compact-table

   * - Model
     - Frames Per Second
     - Planning L2 (3s)
   * - UniAD
     - ~1.8 FPS
     - 0.25 m
   * - DriveTransformer
     - ~5.5 FPS (3x)
     - 0.22 m

.. note::

   DriveTransformer was accepted at ICLR 2025, and subsequent industrial
   implementations have pushed throughput further with quantization and
   hardware-specific optimization.


Vision-Language-Action (VLA) Models
------------------------------------

The emergence of large language models (LLMs) and vision-language models
(VLMs) has opened a new direction in autonomous driving: embedding
**natural language reasoning** directly into the driving loop.

What Is a VLA Model?
~~~~~~~~~~~~~~~~~~~~~

A **Vision-Language-Action (VLA)** model takes visual input (camera images,
BEV features) and conditions its output on language -- either explicit
text commands or implicit chain-of-thought reasoning -- before producing
driving actions or waypoints.

.. code-block:: text

   [Camera images] + [Language context / CoT]
            |
   Vision-Language Model backbone (e.g., LLaVA, InternVL)
            |
   [Action decoder] → Waypoints / control signals

Chain-of-Thought Reasoning for Driving
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rather than directly regressing waypoints, VLA systems can generate an
intermediate **textual reasoning trace** that makes their logic auditable:

.. code-block:: text

   "The pedestrian on the left is looking toward the road and is likely
    to cross. The traffic light ahead is yellow. I should slow down
    and prepare to stop at the crosswalk."
    → [decelerate, target_speed=0, stop_distance=12m]

This chain-of-thought approach offers several benefits:

- The reasoning trace is **human-readable**, dramatically improving
  interpretability over pure neural planners.
- The model can be queried in natural language to **explain a past
  decision** (important for incident investigation).
- Language supervision provides a rich additional training signal beyond
  imitation labels.

NVIDIA Alpamayo
~~~~~~~~~~~~~~~

NVIDIA Alpamayo is a VLA model for driving released in 2025 as part of
NVIDIA's DRIVE platform. Key features:

- Built on a large vision-language backbone fine-tuned on driving data.
- Produces **driving decisions conditioned on natural language scene
  descriptions** generated by the model itself.
- Integrated with NVIDIA's end-to-end DRIVE stack and evaluated in
  CARLA and on-road in partnership with automotive OEMs.
- Supports **free-form language commands** from the passenger or dispatcher
  (e.g., "take the scenic route" or "avoid the highway").

DriveVLM
~~~~~~~~~

DriveVLM (Wayve / academic collaboration, 2024) demonstrated that:

- A VLM backbone can successfully ground visual driving scenes to language.
- Chain-of-thought driving outperforms direct waypoint regression on rare and
  complex scenarios where standard E2E models fail.
- The approach generalizes better across geographic domains because language
  provides a universal, transferable representation.


Tesla's End-to-End Approach
----------------------------

Tesla represents the most large-scale industrial deployment of end-to-end
driving principles.

The FSD v12 Architecture
~~~~~~~~~~~~~~~~~~~~~~~~

Starting with FSD v12 (2024), Tesla replaced its modular pipeline with a
**fully neural, camera-only end-to-end system**:

.. code-block:: text

   8 Cameras (1280×960 @ 36 FPS each)
         |
   Video encoder (space-time transformers per camera)
         |
   BEV feature fusion (cross-camera attention)
         |
   Occupancy & flow prediction
         |
   Planning transformer (waypoint sequence)
         |
   Low-level PID / MPC controller
         |
   Steering, throttle, brake actuators

Key characteristics:

- **Camera-only** -- no LiDAR or radar. Tesla argues cameras suffice because
  humans drive with eyes.
- **End-to-end differentiable** -- gradients flow from control commands back
  through the planner to the video encoder.
- **Fleet learning** -- 8.3 billion supervised FSD miles as of early 2026,
  continuously improving through shadow mode and human correction labels.

.. admonition:: Scale as a Moat
   :class: important

   Tesla's fleet data advantage is structural. With millions of vehicles
   collecting edge cases daily, the system receives training signal that
   no simulation-only approach can easily replicate.


NVIDIA's End-to-End Stack
--------------------------

NVIDIA's approach combines hardware (DRIVE Orin/Thor SoC) with a full
software stack that incorporates end-to-end learning with reinforcement
learning fine-tuning.

Key Layers
~~~~~~~~~~

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Perception (NVIDIA Hydra-MDP)
      :class-card: sd-border-primary

      Multi-task BEV perception trained with a single unified decoder
      for detection, segmentation, and occupancy.

   .. grid-item-card:: World Model
      :class-card: sd-border-primary

      NVIDIA Cosmos generates synthetic training data and serves as a
      differentiable environment for RL fine-tuning of the planner.

   .. grid-item-card:: Planner (E2E + RL)
      :class-card: sd-border-primary

      A learned planner trained with imitation learning then refined
      with reinforcement learning rewards (comfort, safety, progress).

   .. grid-item-card:: DRIVE Thor SoC
      :class-card: sd-border-primary

      Up to 2000 TOPS of compute. Executes all E2E inference at the
      latency required for real-time vehicle control.

Reinforcement Learning Fine-Tuning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Imitation learning alone inherits the distribution of human driving,
including human mistakes and sub-optimal decisions. NVIDIA uses RL
to optimize for **explicit reward functions** that humans cannot
efficiently demonstrate:

.. math::

   \mathcal{R} = w_1 \cdot r_{\text{safety}} + w_2 \cdot r_{\text{comfort}} + w_3 \cdot r_{\text{progress}}

where :math:`r_{\text{safety}}` penalizes proximity to obstacles and traffic
violations, :math:`r_{\text{comfort}}` penalizes high jerk and acceleration,
and :math:`r_{\text{progress}}` rewards making forward progress toward the
destination.


Advantages of End-to-End Driving
----------------------------------

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Joint Optimization
      :class-card: sd-border-success

      All components are optimized for the same ultimate objective (safe,
      comfortable driving), eliminating the proxy-metric misalignment that
      plagues modular pipelines.

   .. grid-item-card:: No Information Loss
      :class-card: sd-border-success

      Raw sensor data flows through the entire computation graph. Features
      relevant to planning that don't fit a predefined schema can still
      influence the output.

   .. grid-item-card:: Emergent Capabilities
      :class-card: sd-border-success

      E2E models trained at scale have demonstrated emergent abilities --
      behaviors that appear without explicit programming, analogous to
      emergent capabilities in large language models.

   .. grid-item-card:: Architectural Simplicity
      :class-card: sd-border-success

      A single model (or small set of coupled models) replaces dozens of
      specialized subsystems, reducing the engineering surface area for
      integration bugs.


Disadvantages and Open Challenges
-----------------------------------

.. admonition:: Black-Box Behavior
   :class: warning

   End-to-end models provide no interpretable intermediate representations.
   When the system makes an error, it is extremely difficult to determine
   whether the failure was due to perception, prediction, or planning -- or
   some emergent interaction between them.

.. admonition:: Massive Data Requirements
   :class: warning

   Training competitive E2E models requires hundreds of millions of labeled
   driving frames. Labeling cost, data diversity (geography, weather, culture),
   and long-tail coverage all remain significant challenges.

.. admonition:: Validation Difficulty
   :class: warning

   ISO 26262 and SOTIF assume a modular decomposition where each component
   can be tested in isolation. Validating a monolithic E2E system against
   an ASIL-D safety argument is an open research problem with no settled
   industry-wide methodology.

.. admonition:: Distribution Shift
   :class: warning

   E2E systems trained on one geographic region or driving culture may
   fail silently when deployed in a different environment, with no explicit
   module to flag the out-of-distribution condition.

Interpretability Research
~~~~~~~~~~~~~~~~~~~~~~~~~~

Researchers are actively developing methods to add interpretability to E2E
systems without sacrificing performance:

- **Attention visualization** -- Identifying which image regions most
  influenced a particular action.
- **Concept bottleneck models** -- Forcing the network to predict human-
  interpretable concepts (e.g., "pedestrian present", "rain") as an
  intermediate representation.
- **Chain-of-thought supervision** (VLA models) -- Training the model to
  produce textual reasoning before acting.


The Role of Simulation in Training E2E Models
----------------------------------------------

End-to-end models are data-hungry, and real-world data collection is slow
and expensive. Simulation plays a critical role in closing this gap.

Data Generation at Scale
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Scenario diversity**
     - Simulators (CARLA, Waymo Sim, NVIDIA Cosmos) can generate rare
       events (jaywalking, debris on road, sensor degradation) that are
       almost impossible to encounter at sufficient frequency in the real world.
   * - **Automatic labeling**
     - Ground-truth labels (depth, optical flow, 3-D boxes) are free in
       simulation, eliminating human annotation cost.
   * - **Perturbation testing**
     - Systematic parameter sweeps (weather, traffic density, lighting) can
       evaluate robustness.

Sim-to-Real Gap
~~~~~~~~~~~~~~~

The fundamental limitation of simulation-based training is the **sim-to-real
gap**: models trained in simulation may fail in the real world because the
simulated sensor outputs, scene textures, and agent behavior distributions
differ from reality.

Mitigation strategies include:

- **Domain randomization** -- Randomly varying simulation parameters during
  training so the model learns features robust to environment variation.
- **Generative world models** (Lecture 12) -- Using neural world models
  trained on real data to generate photo-realistic synthetic data.
- **Real + sim co-training** -- Mixing real and simulated data during training.

.. code-block:: python

   # Example: CARLA batch data collection for E2E training
   import carla

   client = carla.Client("localhost", 2000)
   world = client.get_world()

   # Randomize weather for domain randomization
   weathers = [
       carla.WeatherParameters.ClearNoon,
       carla.WeatherParameters.HardRainNoon,
       carla.WeatherParameters.WetCloudySunset,
   ]
   for weather in weathers:
       world.set_weather(weather)
       # collect_episode(world, duration_seconds=60)


Where the Industry Is Heading
------------------------------

The tension between modular and end-to-end is resolving into a **spectrum**
rather than a binary choice:

.. grid:: 1 1 3 3
   :gutter: 3

   .. grid-item-card:: Fully Modular
      :class-card: sd-border-secondary

      Traditional approach. Each module developed independently. Mature
      validation tooling. Used by Mobileye (RSS + modular stack).

   .. grid-item-card:: Hybrid (Dominant 2025-2026)
      :class-card: sd-border-warning

      E2E perception + learned planner, but with explicit safety monitors,
      interpretable occupancy maps, and override logic. Used by Waymo Gen 6,
      Baidu Apollo 6.0.

   .. grid-item-card:: Fully E2E
      :class-card: sd-border-success

      Single neural model from pixels to actuators. Used by Tesla FSD v12,
      Wayve. Requires massive fleet data and novel validation frameworks.

.. note::

   No major robotaxi operator runs a fully end-to-end system without any
   engineered safety layer. The industry consensus in 2026 is that E2E
   models excel at perception and scene understanding, while explicit safety
   checks (collision avoidance, traffic law compliance) remain engineered
   components layered on top.

.. admonition:: Bonus Assignment Unlocked -- GP5: Vision-Language-Action Driving (Optional)
   :class: important

   You now have the foundational knowledge from **L10--L12** to begin
   **GP5: Vision-Language-Action Driving**. In this optional bonus project
   you will build a simplified VLA model that maps camera images and
   natural language commands directly to driving actions, bypassing the
   modular pipeline -- and compare it against your GP4 system.

   :doc:`Go to GP5 </assignments/gp5>`
