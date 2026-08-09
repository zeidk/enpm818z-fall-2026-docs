====================================================
Lecture
====================================================


What Is a World Model?
-----------------------

A **world model** is a learned model that captures how the world evolves over
time -- how future states follow from past states and the actions of an agent.
In autonomous driving, a world model trained on video data can predict what
the scene ahead will look like after the ego vehicle takes a specific action,
acting as a learned, data-driven simulator.

.. admonition:: Formal Definition
   :class: note

   Given a history of observations :math:`o_{1:t}` and a sequence of future
   actions :math:`a_{t:t+H}`, a world model predicts the distribution over
   future observations:

   .. math::

      p(o_{t+1:t+H} \mid o_{1:t},\, a_{t:t+H})

   A **generative** world model can sample from this distribution to produce
   photorealistic video of what the world would look like if the vehicle
   took those actions.

Why Does Autonomous Driving Need World Models?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Data Scarcity for Rare Events
      :class-card: sd-border-info

      Real-world driving data is abundant for common scenarios but extremely
      sparse for safety-critical edge cases (vehicle running a red light,
      sudden tire blowout, child chasing a ball). World models can synthesize
      these rare events at scale.

   .. grid-item-card:: Offline Policy Evaluation
      :class-card: sd-border-info

      Before deploying a new planner on the road, it can be evaluated against
      the world model: "What would happen if I had used this new planner on
      yesterday's fleet data?" This avoids costly on-road experiments.

   .. grid-item-card:: Model-Based Planning
      :class-card: sd-border-info

      A planner can use a world model as an internal simulator to "imagine"
      the consequences of candidate action sequences and select the one that
      leads to the best predicted outcome.

   .. grid-item-card:: Sim-to-Real Reduction
      :class-card: sd-border-info

      World models trained on real data produce training images that are
      indistinguishable from real sensor data, dramatically reducing the
      distributional gap compared to traditional physics-based simulators.


Architecture: Video Prediction Transformers
--------------------------------------------

Modern driving world models are built on **video generation transformers** --
large autoregressive or diffusion-based models that operate in a compressed
latent space.

Tokenization and Latent Space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raw video frames are too high-dimensional to process directly. World models
use a **visual tokenizer** (typically a VQ-VAE or a video VAE) to compress
each frame into a grid of discrete or continuous tokens:

.. code-block:: text

   Raw frame (1920×1080 RGB)
         |
   Visual Tokenizer (VQ-VAE / Video VAE)
         |
   Latent tokens (32×32 = 1024 tokens per frame)
         |
   Transformer backbone (attention across time and space)
         |
   Predicted latent tokens (future frames)
         |
   Decoder → Synthesized future video frames

Autoregressive vs. Diffusion Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Autoregressive

      Predicts future tokens one at a time, conditioned on all previous tokens.
      Simple to train (next-token prediction), but slow at inference because
      tokens must be generated sequentially.

      .. math::

         p(o_{1:T}) = \prod_{t=1}^{T} p(o_t \mid o_{1:t-1},\, a_{1:t-1})

   .. tab-item:: Diffusion-Based

      Generates future frames by iteratively denoising a random noise tensor.
      Faster than autoregressive at high resolution, and produces sharper,
      more consistent video. Used by NVIDIA Cosmos.

      .. math::

         p_\theta(x_{0}) = \int p_\theta(x_{0:T})\, dx_{1:T}

Action Conditioning
~~~~~~~~~~~~~~~~~~~~

To make predictions useful for planning, the world model must condition on
**ego-vehicle actions** (steering angle, acceleration). This is implemented
via cross-attention between the action embeddings and the latent video tokens:

.. code-block:: text

   [Action sequence a_{t:t+H}] → Action Encoder → Action Embeddings
                                                            ↓
   [Past latent tokens] → Transformer → Cross-Attention ← → Next token prediction


Wayve GAIA
------------

**GAIA** is Wayve's family of generative driving world models, and the
clearest example of the "learned simulator" idea applied at industrial
scale on real fleet data.

.. list-table:: The GAIA line
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - Model
     - Contribution
   * - **GAIA-1** (2023)
     - ~9B-parameter proof of concept. Established the recipe: tokenize
       driving video, model it autoregressively in latent space, and
       condition generation on **ego actions and text**, so the model can
       be asked "what if I steered left here?"
   * - **GAIA-2** (2025)
     - Latent-diffusion successor. Multi-camera generation with
       cross-view consistency, and richer structured conditioning (ego
       action, other agents, road layout, weather, time of day) aimed
       squarely at controllable safety-critical scenario synthesis.

.. warning::

   Vendor world models are announced frequently and the version numbers
   move quickly. Confirm the **current** generation, its parameter count,
   and its published capabilities from Wayve's own technical report
   before citing specifications -- do not carry forward figures from
   lecture notes, including these.

Key Capabilities
~~~~~~~~~~~~~~~~

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Multi-Camera Consistency
      :class-card: sd-border-primary

      GAIA-2 generates video across multiple cameras simultaneously, maintaining
      geometric consistency between views. This is critical for training BEV
      perception models that require multi-camera input.

   .. grid-item-card:: Long-Horizon Generation
      :class-card: sd-border-primary

      Can synthesize driving video for up to 30+ seconds while maintaining
      scene consistency -- long enough to simulate complete intersection
      negotiations and lane change maneuvers.

   .. grid-item-card:: Controllable Rare Events
      :class-card: sd-border-primary

      Using text conditioning, operators can request specific scenarios: "a
      cyclist merges into the ego lane at an intersection" or "heavy rain
      begins during a highway merge". The model synthesizes plausible video
      matching the description.

   .. grid-item-card:: Action-Conditional Rollouts
      :class-card: sd-border-primary

      Given a sequence of planned waypoints, GAIA renders what the scene
      would look like if the ego vehicle executed those waypoints -- enabling
      closed-loop policy evaluation entirely within the world model.

.. admonition:: The trajectory of the GAIA line
   :class: tip

   The progression is instructive: GAIA-1 proved that action-conditioned
   driving video generation was possible at all; GAIA-2 shifted the
   emphasis from raw generation quality to **controllability** --
   multi-camera consistency and structured conditioning on the things a
   safety engineer actually wants to vary.

   That shift matters more than the parameter count. A world model is
   only useful for validation if you can *ask it for a specific
   scenario*; an uncontrollable model that produces beautiful video is a
   demo, not a tool.


NVIDIA Cosmos
-------------

NVIDIA Cosmos is a family of **world foundation models** for physical AI,
announced at CES 2025 and developed as part of NVIDIA's end-to-end ADS stack.

Design Philosophy
~~~~~~~~~~~~~~~~~

Unlike GAIA, which is specialized for driving video, Cosmos is a general
physical world model trained on diverse real-world video (robotics,
manufacturing, driving, outdoor scenes). It is then fine-tuned for specific
domains such as autonomous driving.

Cosmos Architecture
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Pre-training (diverse physical world video)
         |
   Cosmos Base (general physics world model)
         |
   Fine-tuning (AV driving data, robotics data)
         |
   Cosmos-Drive / Cosmos-Robot (domain-specific models)

Integration with NVIDIA DRIVE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NVIDIA integrates Cosmos directly into its ADS development pipeline:

1. **Synthetic data generation** -- Cosmos generates additional training data
   from existing fleet footage, augmenting with rare weather, unusual agents,
   and edge-case scenarios.
2. **RL environment** -- The planner trained via reinforcement learning
   (L12) uses Cosmos as a differentiable environment, receiving visual
   feedback on the consequences of planned actions.
3. **Test oracle** -- Candidate planners are evaluated in Cosmos rollouts before
   any on-road testing, reducing safety risk.

.. note::

   NVIDIA released Cosmos under an open license for non-commercial research,
   making it accessible for academic study and experimentation. The DRIVE
   production variant is proprietary.


Vista: Generalizable Driving World Models (NeurIPS 2024)
---------------------------------------------------------

Vista (Gao et al., NeurIPS 2024) comes from **OpenDriveLab / Shanghai AI
Laboratory** and, unlike the proprietary models above, is **openly
released**. Its central contribution is **generalizability**: earlier
world models were trained and evaluated largely on a single dataset, with
limited transfer to unseen locations and driving styles.

Key Contributions
~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Web-scale pre-training**
     - Vista pre-trains on **OpenDV-2K**, a large corpus assembled from
       publicly available driving video (thousands of hours spanning many
       countries, vehicles, and cameras), then fine-tunes on curated
       datasets such as nuScenes. The scale and diversity of the
       pre-training corpus is what drives the generalization.
   * - **High fidelity and long horizon**
     - Generates at higher spatial resolution and frame rate than prior
       driving world models, with a latent-replacement scheme to extend
       rollouts beyond a single generation window without collapsing.
   * - **Versatile action conditioning**
     - Accepts control at several levels of abstraction -- steering
       angle, speed, trajectory, or a high-level command -- rather than a
       single fixed action format.
   * - **Evaluation without ground truth**
     - Proposes a reward formulation that scores generated futures
       without requiring matched real-world video, addressing the
       awkward problem of evaluating counterfactual rollouts.
   * - **Open source**
     - Model weights and training code are publicly available, which is
       what makes Vista usable in coursework -- GAIA and Cosmos-Drive are
       not.

Why Vista Matters
~~~~~~~~~~~~~~~~~~

Vista addresses the **generalization problem** that limits real-world
driving world models: a model trained on data from one city may not
simulate driving in another. Training on a geographically diverse,
web-scale corpus is a step toward a universal driving world model -- and
being open, it is the one model in this lecture you can actually run.


Applications of Driving World Models
--------------------------------------

Data Augmentation
~~~~~~~~~~~~~~~~~

Training end-to-end perception and planning models requires diverse, balanced
datasets. World models can augment existing data by:

- **Weather augmentation** -- Converting clear-day sequences to rain, fog, or
  night, producing free labels for all conditions.
- **Camera failure simulation** -- Degrading one camera input to train
  perception redundancy.
- **Novel viewpoint synthesis** -- Generating views from hypothetical sensor
  positions not present in the original vehicle.

.. code-block:: python

   # Conceptual pseudocode: world model augmentation
   from gaia3 import WorldModel

   model = WorldModel.load_pretrained("gaia3-15b")

   for frame_seq in real_driving_data:
       # Generate rain version
       rain_seq = model.generate(
           conditioning_video=frame_seq,
           text_condition="heavy rain",
           ego_actions=frame_seq.actions
       )
       augmented_dataset.add(rain_seq, labels=frame_seq.labels)

Long-Tail Scenario Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **long tail** of rare safety-critical scenarios is the primary unsolved
data challenge in AV development. Traditional simulation can script these
scenarios, but scripted CARLA scenarios lack the visual realism of real data.
World models generate photo-realistic long-tail scenarios:

.. list-table:: Example Long-Tail Scenarios
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - Scenario Type
     - World Model Conditioning
   * - Pedestrian stepping off curb into traffic
     - ``"pedestrian suddenly steps into the road from the right sidewalk"``
   * - Emergency vehicle approaching from behind
     - ``ego_action=pull_right`` + ``text="ambulance with siren behind ego"``
   * - Road debris in travel lane
     - ``"large cardboard box in the center of the left lane ahead"``
   * - Sensor degradation (camera flare)
     - ``"strong sun glare on front-left camera"``
   * - Construction zone with atypical lane markings
     - ``"construction cones redirect traffic, no visible lane lines"``

Policy Evaluation (Offline Closed-Loop)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the most valuable applications of world models is **offline closed-loop
evaluation**: testing a new planner version on historical data without deploying
it on the road.

.. code-block:: text

   Historical fleet log (O_1:T, A_human)
              |
   Replace human actions with new planner: A_planner
              |
   World model generates: O'_2:T = WM(O_1, A_planner_2, ...)
              |
   Evaluate: collision rate, comfort metrics, lane adherence
              |
   If acceptable → promote to shadow mode → on-road test

This **counterfactual evaluation** pipeline dramatically reduces the cost
and risk of iterating on planners.


World Models vs. Traditional Simulation (CARLA)
------------------------------------------------

.. list-table::
   :widths: 25 38 37
   :header-rows: 1
   :class: compact-table

   * - Dimension
     - Physics-Based (CARLA)
     - Generative World Model
   * - **Realism**
     - High geometry; synthetic appearance
     - Photo-realistic (trained on real data)
   * - **Physical accuracy**
     - Exact (rules-based physics engine)
     - Approximate (learned from data)
   * - **Scenario control**
     - Precise API control over all agents
     - Probabilistic; conditioning may not be obeyed exactly
   * - **Scalability**
     - Limited by hand-crafting scenarios
     - Can generate unlimited variations at scale
   * - **Training data quality**
     - Sim-to-real gap in appearance
     - Near-real; minimal appearance gap
   * - **Compute cost**
     - Low (game engine rendering)
     - High (large GPU inference)
   * - **Best use case**
     - Algorithm development, course instruction
     - Large-scale synthetic data, E2E training

.. admonition:: Key Insight
   :class: important

   CARLA and world models are **complementary**, not competing. CARLA
   excels for controlled algorithm development and testing where precise
   scenario specification matters. World models excel for large-scale data
   augmentation and photo-realistic long-tail generation where visual
   realism is the priority. In production ADS development, both are used.


Generative Scenario Generation for Safety Validation
------------------------------------------------------

Safety validation requires demonstrating that an ADS handles a comprehensive
set of scenarios safely. Traditional testing approaches face the **coverage
problem**: there are infinite possible scenarios, and testing on a finite set
cannot guarantee safety.

Adversarial Scenario Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

World models can be combined with adversarial optimization to systematically
find **failure-inducing scenarios** for a given planner:

.. math::

   \text{scenario}^* = \arg\max_{\text{scenario}} \mathcal{L}_{\text{safety}}(\text{planner}(\text{scenario}))

The optimizer finds the scenario parameters (pedestrian timing, vehicle
speed, weather) that maximize safety-relevant losses (collision probability,
traffic law violations). This is more efficient than random scenario sampling
for finding the planner's failure modes.

Structured Scenario Families
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Regulatory bodies are beginning to specify **scenario families** -- systematic
parameterizations of scenario classes -- as the basis for safety validation.
World models can populate these families with photo-realistic instances:

- **ASAM OpenSCENARIO 2.0** -- A standard format for specifying scenario
  families that world models can instantiate.
- **UNECE GTR safety cases** -- The UNECE GTR (January 2026) encourages
  safety case arguments based on systematic scenario coverage.


Sim-to-Real Gap and Domain Adaptation
--------------------------------------

The sim-to-real gap remains a fundamental challenge for any simulation-based
training approach, including world models.

Sources of the Gap
~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Appearance Gap

      Even photorealistic simulators differ from real cameras in subtle ways:
      lens flare, compression artifacts, sensor noise spectral characteristics,
      and HDR handling. Models that overfit to simulation appearance fail in
      the real world.

   .. tab-item:: Dynamics Gap

      Physics engines make simplifying assumptions (rigid bodies, simplified
      tire models) that differ from real vehicle dynamics. Learned world
      models inherit the biases of their training data distribution.

   .. tab-item:: Agent Behavior Gap

      Simulated pedestrians and vehicles follow programmed behavior models.
      Real agents are unpredictable and culturally diverse. A world model
      trained on London driving data may not model the behavior of drivers
      in Cairo or Mumbai.

Mitigation Strategies
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Domain randomization**
     - Randomly vary simulation parameters (textures, lighting, weather,
       dynamics) during training so the model learns invariant features.
   * - **Domain adaptation**
     - Fine-tune simulation-trained models on a small amount of real data
       using techniques like DANN (Domain Adversarial Neural Networks).
   * - **Real + sim co-training**
     - Mix real and simulated data in fixed ratios during training batches.
   * - **Neural rendering augmentation**
     - Use a style-transfer network to make synthetic images look like
       real camera data before feeding them to the perception model.
   * - **World model as bridge**
     - Generate synthetic training data using a world model trained on
       real data -- the generated data has real-world appearance statistics
       without the annotation cost.


World Models as the "Imagination Module"
-----------------------------------------

The most exciting architectural implication of world models is their role
as an **imagination module** inside an end-to-end driving system.

Model-Based Planning
~~~~~~~~~~~~~~~~~~~~

Classic model-based control uses a physics model to predict the future and
select actions. A world model extends this to high-dimensional sensory
predictions:

.. code-block:: text

   Current observation o_t
         |
   Encoder → Latent state z_t
         |
   For each candidate action sequence A_i:
       z_{t+1:t+H} = WorldModel.rollout(z_t, A_i)     ← "imagine" the future
       reward_i    = Reward(z_{t+1:t+H})
   Select A* = argmax reward_i
         |
   Execute a*_t in the real world, observe o_{t+1}

This **imagination-based planning** allows the system to evaluate many action
sequences before committing, improving decision quality in complex situations
like multi-agent negotiation at intersections.

Dreamer Architecture Analogy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Dreamer algorithm (Hafner et al., 2020) demonstrated world-model-based
planning in video games. The driving world models described in this lecture
can be seen as domain-specific, large-scale instantiations of the same
principle:

.. math::

   \underbrace{z_{t+1} = f_\theta(z_t, a_t)}_{\text{world model}} \quad
   \underbrace{a_t = \pi_\phi(z_t)}_{\text{policy}} \quad
   \underbrace{r_t = r_\psi(z_t)}_{\text{reward model}}

Training the policy :math:`\pi_\phi` entirely within the world model
(without real-world rollouts) is called **in-model RL** and is an active
research frontier for autonomous driving.


CARLA's Role Alongside World Models
-------------------------------------

Despite the rise of neural world models, CARLA retains an important role
in ADS education and research for several reasons:

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Precise Scenario Control
      :class-card: sd-border-secondary

      CARLA's Python API allows exact specification of actor positions,
      velocities, traffic light states, and weather -- essential for
      debugging specific edge cases in perception and planning.

   .. grid-item-card:: Ground-Truth Labels
      :class-card: sd-border-secondary

      CARLA provides perfect ground-truth bounding boxes, semantic
      segmentation, depth maps, and ego state. Neural world models do
      not provide these structured labels.

   .. grid-item-card:: Real-Time Closed-Loop
      :class-card: sd-border-secondary

      CARLA supports genuine closed-loop interaction where the ego
      vehicle's actions affect the scene physics in real time. World
      model rollouts are typically open-loop or slow.

   .. grid-item-card:: Compute Accessibility
      :class-card: sd-border-secondary

      Running CARLA requires a consumer-grade GPU. Running a
      large driving world model at full resolution requires a
      multi-GPU datacenter node. CARLA is realistic for coursework
      and academic research; these models are not.

   .. grid-item-card:: Education
      :class-card: sd-border-secondary

      CARLA is the pedagogical platform for this course. Students learn
      sensor physics, ROS 2 integration, and pipeline development through
      hands-on CARLA assignments before encountering world models.

   .. grid-item-card:: Algorithmic Validation
      :class-card: sd-border-secondary

      Localization, SLAM, motion planning, and MPC algorithms can be
      tested and visualized in CARLA without the complexity of real
      data management.

.. tip::

   In production AV companies (Waymo, Zoox, Mobileye), CARLA-like
   physics simulators and neural world models operate in parallel. Physics
   simulation handles algorithm development and unit testing; world models
   handle large-scale synthetic data generation and system-level evaluation.


Summary
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: World Models
      :class-card: sd-border-primary

      - A world model learns :math:`p(o_{t+1:t+H} \mid o_{1:t}, a_{t:t+H})`
        -- a **learned simulator** conditioned on the ego's own actions
      - Built as video generation transformers over a compressed latent
        space, either autoregressive or diffusion-based
      - **GAIA** (Wayve): fleet-data driving models; the arc runs from
        raw generation quality toward *controllability*
      - **Cosmos** (NVIDIA): general physical-world foundation models,
        fine-tuned per domain
      - **Vista** (OpenDriveLab): web-scale pre-training for
        generalization, and the one that is openly available

   .. grid-item-card:: Why They Matter
      :class-card: sd-border-primary

      - **Long-tail generation**: synthesize rare safety-critical events
        that are too infrequent to collect
      - **Offline closed-loop evaluation**: replay fleet logs with a new
        planner's actions substituted, before any on-road testing
      - **Imagination-based planning**: roll out candidate action
        sequences internally and pick the best (the Dreamer idea, scaled)
      - Complementary to CARLA, not a replacement: CARLA gives exact
        control and free ground-truth labels; world models give
        photorealism and scale

.. admonition:: The honest caveat
   :class: warning

   World models are **approximate**. They learn physics from data rather
   than enforcing it, they can be asked for a scenario and quietly
   deliver something slightly different, and they inherit every bias in
   their training distribution. A model trained on one region's driving
   culture does not faithfully simulate another's. Treat generated video
   as a rich data source, not as ground truth about the world.
