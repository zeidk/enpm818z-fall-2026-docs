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
     - minADE
     - ~0.7 m
   * - Occupancy Prediction
     - IoU
     - ~63% (near) / ~40% (far)
   * - Planning
     - Average L2 over 1/2/3 s
     - ~1.0 m (rising to ~1.65 m at 3 s)

.. warning::

   **Check these against the paper before quoting them.** Reported
   numbers for UniAD vary considerably between the original paper,
   subsequent reproductions, and re-evaluations under corrected
   protocols -- especially the planning L2 figures, which depend heavily
   on whether ego status is fed to the model. Treat the table above as
   indicative of magnitude, not as citable values.

.. admonition:: Open-loop planning metrics are weaker evidence than they look
   :class: important

   Before accepting "UniAD achieves 1.0 m L2, therefore end-to-end
   works," note the critique that followed. **AD-MLP** (Zhai et al.,
   2023) and the paper *"Is Ego Status All You Need for Open-Loop
   End-to-End Autonomous Driving?"* (Li et al., CVPR 2024) showed that a
   trivial MLP fed **only the ego vehicle's own state** -- no camera
   input at all -- matches or beats sophisticated E2E models on the
   nuScenes open-loop L2 metric.

   The reason is that nuScenes driving is overwhelmingly "continue doing
   what you were just doing." Extrapolating your own recent motion is
   therefore a very strong baseline, and the metric rewards it. The
   models may still be learning something real, but **this benchmark
   cannot demonstrate it**.

   The field's response has been to move toward closed-loop evaluation
   (nuPlan, CARLA leaderboards, NAVSIM), where the policy's own actions
   determine the states it subsequently sees, and compounding error --
   the failure mode from behavior cloning later in this lecture --
   actually shows up. When you read any planning result, the first
   question is: **open-loop or closed-loop?**


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
     - Relative throughput
     - Planning quality
   * - UniAD
     - 1x (baseline)
     - baseline
   * - DriveTransformer
     - ~3x
     - comparable or slightly better

.. note::

   The throughput ratio is the meaningful claim here and is what the
   paper argues for. Absolute FPS depends entirely on GPU, batch size,
   resolution, and precision, so it is not quoted. Apply the open-loop
   caveat above to the planning column as well.

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

DriveVLM (Tsinghua University with Li Auto, 2024) demonstrated that:

- A VLM backbone can successfully ground visual driving scenes to language.
- Chain-of-thought driving -- scene description, then analysis, then
  hierarchical planning -- outperforms direct waypoint regression on rare
  and complex scenarios where standard E2E models fail.
- A **dual-system** design is what makes it practical: the slow VLM
  reasons about the scene while a fast conventional planner runs at
  control rate, because a large VLM cannot itself meet a 10 Hz deadline.

.. note::

   **Wayve** pursues a related but distinct line of work: LINGO-1 and
   LINGO-2 add natural-language commentary and instruction-following to
   their driving models. Do not conflate the two -- they are different
   groups with different architectures.


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
- **Generative world models** (L13) -- Using neural world models
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


Imitation Learning
------------------

Imitation learning trains a policy to mimic expert (human driver)
behavior from logged demonstrations. It is the most direct way to
distil human driving skill into the kinds of end-to-end networks
covered earlier in this lecture.

Behavior Cloning
~~~~~~~~~~~~~~~~

**Behavior cloning (BC)** is the simplest imitation learning
algorithm: treat demonstrations as a supervised learning dataset.

Given a dataset of expert state-action pairs
:math:`\mathcal{D} = \{(s_i, a_i^*)\}_{i=1}^{N}` collected
from human drivers:

.. math::

   \min_\theta \; \mathbb{E}_{(s,a^*) \sim \mathcal{D}}
   \left[ \mathcal{L}(\pi_\theta(s), a^*) \right]

where :math:`\mathcal{L}` is a regression loss (e.g., MSE for
continuous actions) or cross-entropy for discrete maneuver
classification.

**BC pipeline:**

.. code-block:: text

   1. Collect expert demonstrations: (obs_t, action_t) pairs
   2. Train policy network: obs -> action
   3. Deploy: at each step, feed current obs and execute action

Distribution Shift: The Key Failure Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The fundamental problem with behavior cloning is
**distribution shift** (also called covariate shift).

During training, the policy sees states from the expert's
distribution :math:`d_{\pi^*}`. During deployment, the policy's
own actions cause it to visit states in :math:`d_{\pi_\theta}`,
which may be far from :math:`d_{\pi^*}`.

**Compounding error:** Small deviations from the expert
trajectory accumulate over time, driving the policy into
states never seen during training. The policy has no
supervision signal for recovery from these states.

.. admonition:: Compounding Error Formula
   :class: warning

   For a policy with per-step error :math:`\epsilon`:

   .. math::

      \text{Total error after } T \text{ steps} = O(\epsilon T^2)

   Errors compound **quadratically** in time horizon --
   a fundamental limitation of open-loop behavior cloning.

DAgger: Dataset Aggregation
----------------------------

DAgger (Ross et al., ICML 2011) addresses distribution shift
by iteratively augmenting the training dataset with states
visited by the learned policy.

Algorithm
~~~~~~~~~

.. code-block:: text

   Initialize: D = {} (empty dataset), pi_1 = any policy
   For iteration i = 1, 2, ..., N:
       1. Roll out policy pi_i in the environment
          (or simulator) to collect trajectory states {s_t}
       2. Query the expert at each visited state: a*_t = pi*(s_t)
       3. Add {(s_t, a*_t)} to D
       4. Train policy pi_{i+1} on the full aggregated D
   Return: best pi_i on validation

Why DAgger Works
~~~~~~~~~~~~~~~~

DAgger ensures the training distribution converges to the
deployment distribution.

- After :math:`n` iterations, the training dataset contains
  states sampled from the policies
  :math:`\pi_1, \pi_2, \ldots, \pi_n`.
- As the policy improves, the states it visits converge toward
  the expert's states.
- In the limit, the training distribution matches the
  deployment distribution and compounding errors vanish.

**DAgger guarantees** (Ross et al., 2011): Under mild
conditions, DAgger reduces the per-step regret to
:math:`O(\epsilon)` (linear) compared to BC's
:math:`O(\epsilon T^2)` (quadratic).

Practical Considerations
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Challenge
     - Solution
   * - Expert query cost
     - Use simulator with scripted expert; reserve human feedback for hard cases
   * - Safety during rollout
     - Run in simulation (CARLA); use safety fallback controller
   * - Dataset size
     - Prioritize states with high policy uncertainty (active DAgger)
   * - Convergence
     - Monitor validation loss across iterations; stop when plateaued

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

   .. grid-item-card:: Hybrid (Dominant today)
      :class-card: sd-border-warning

      E2E perception + learned planner, but with explicit safety monitors,
      interpretable occupancy maps, and override logic. Used by Waymo's
      current-generation stack and recent Baidu Apollo releases.

   .. grid-item-card:: Fully E2E
      :class-card: sd-border-success

      Single neural model from pixels to actuators. Tesla FSD has been
      end-to-end since v12 (and has iterated well past it); Wayve builds
      on the same principle. Requires massive fleet data and novel
      validation frameworks.

.. note::

   No major robotaxi operator runs a fully end-to-end system without any
   engineered safety layer. The industry consensus in 2026 is that E2E
   models excel at perception and scene understanding, while explicit safety
   checks (collision avoidance, traffic law compliance) remain engineered
   components layered on top.

Summary
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: End-to-End Architectures
      :class-card: sd-border-primary

      - Modular vs E2E: interpretability and validation traded against
        joint optimization and no information loss at boundaries
      - UniAD: query propagation through tracking -> motion -> occupancy
        -> planning, all co-optimized with a planning loss
      - DriveTransformer: one shared attention block over agent, map and
        ego tokens; ~3x throughput at comparable quality
      - VLA: language as an intermediate representation, giving auditable
        chain-of-thought reasoning (DriveVLM, and Wayve's LINGO line)

   .. grid-item-card:: Imitation Learning
      :class-card: sd-border-primary

      - Behavior cloning is supervised learning on expert demonstrations
      - Its failure mode is distribution shift: error compounds as
        :math:`O(\epsilon T^2)` because the policy visits states the
        expert never did
      - DAgger fixes this by querying the expert **on states the learner
        actually visits**, reducing the bound to linear
      - Open-loop benchmarks flatter these methods; insist on closed-loop
        evaluation before believing a planning result

.. note::

   **On the numbers in this lecture.** Nearly every quantitative claim
   here comes from a fast-moving literature with inconsistent evaluation
   protocols. The architectural ideas are durable; the leaderboard
   positions are not. Cite the paper, state the benchmark, and say
   whether it was open-loop.
