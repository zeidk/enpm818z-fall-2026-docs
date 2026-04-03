====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 11: End-to-End Driving &
Foundation Models. Topics include the modular vs. end-to-end debate, UniAD
(CVPR 2023), DriveTransformer (ICLR 2025), Vision-Language-Action (VLA)
models, Tesla's FSD v12 architecture, NVIDIA's end-to-end stack with
reinforcement learning, and the safety and validation challenges of
black-box neural driving systems.

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

   What is the **primary theoretical advantage** of end-to-end driving over
   the modular pipeline?

   A. End-to-end models are always faster to train than modular pipelines.

   B. End-to-end models eliminate information loss at module boundaries and
      allow joint optimization toward a unified driving objective.

   C. End-to-end models do not require any labeled training data.

   D. End-to-end models are more interpretable because their representations
      are learned rather than hand-engineered.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- End-to-end models eliminate information loss at module boundaries
   and allow joint optimization toward a unified driving objective.

   In a modular pipeline, each stage outputs a fixed schema (e.g., object
   lists), discarding information that doesn't fit. E2E models propagate
   gradients from the final planning loss back through all representations,
   ensuring every feature extraction step is optimized for the ultimate goal.


.. admonition:: Question 2
   :class: hint

   UniAD (CVPR 2023) uses a **query-based architecture** built on a shared
   BEV backbone. What are the four task-specific modules it introduces?

   A. TrackFormer, MapFormer, PredictFormer, ControlFormer

   B. TrackFormer, MapFormer, MotionFormer, OccFormer

   C. PerceptionFormer, FusionFormer, PlanFormer, ControlFormer

   D. BEVFormer, OccFormer, MotionFormer, PlanFormer

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- TrackFormer, MapFormer, MotionFormer, OccFormer

   UniAD's architecture flows from a shared BEV encoder into TrackFormer
   (agent tracking), MapFormer (map element detection), MotionFormer
   (multi-modal motion forecasting), and OccFormer (occupancy grid
   prediction), with a final ego-trajectory planner on top.


.. admonition:: Question 3
   :class: hint

   DriveTransformer (ICLR 2025) achieves approximately **3x the throughput**
   of UniAD. What is the key architectural change that enables this?

   A. DriveTransformer removes the planning module entirely.

   B. DriveTransformer uses a single joint attention block shared across
      all tasks, eliminating redundant feature extraction in separate heads.

   C. DriveTransformer operates on LiDAR point clouds instead of cameras.

   D. DriveTransformer uses knowledge distillation to compress UniAD into
      a smaller model.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- DriveTransformer uses a single joint attention block shared across
   all tasks, eliminating redundant feature extraction in separate heads.

   Instead of having each task head independently attend to BEV features,
   DriveTransformer defines three unified token types (agent, map, ego) that
   all attend to each other and to sensor features in a single operation.
   This sharing eliminates the computational duplication that made UniAD slow.


.. admonition:: Question 4
   :class: hint

   In the context of Vision-Language-Action (VLA) models, what is the
   purpose of **chain-of-thought reasoning**?

   A. To increase the size of the training dataset through data augmentation.

   B. To generate an intermediate textual reasoning trace that makes the
      model's driving decisions auditable and interpretable.

   C. To replace the camera sensor with a language description of the scene.

   D. To fine-tune the model on a chain of reinforcement learning rewards.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To generate an intermediate textual reasoning trace that makes
   the model's driving decisions auditable and interpretable.

   Chain-of-thought (CoT) prompting/training encourages the model to produce
   a human-readable reasoning step (e.g., "the pedestrian may cross; I should
   slow down") before outputting a waypoint or action. This dramatically
   improves interpretability compared to direct regression models.


.. admonition:: Question 5
   :class: hint

   Starting with FSD v12, Tesla's end-to-end architecture is:

   A. LiDAR-primary with camera redundancy.

   B. Camera-only, with gradients flowing from control commands back through
      the video encoder.

   C. Radar-primary with camera confirmation.

   D. A hybrid of modular perception and learned planning.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Camera-only, with gradients flowing from control commands back
   through the video encoder.

   Tesla's FSD v12 uses 8 cameras feeding space-time transformers that
   produce BEV features, which feed an occupancy/flow predictor, and then a
   planning transformer. The entire pipeline is differentiable, and Tesla
   trains it using billions of fleet miles of human supervision and shadow
   mode corrections.


.. admonition:: Question 6
   :class: hint

   NVIDIA's end-to-end stack uses reinforcement learning (RL) **after**
   imitation learning (IL). Why?

   A. Imitation learning is too slow, so RL is used to speed up training.

   B. RL allows the model to be deployed without any labeled data.

   C. Imitation learning inherits the distribution of human driving (including
      human mistakes), while RL can optimize explicitly for safety and comfort
      reward functions.

   D. RL generates the camera images used for imitation learning.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Imitation learning inherits the distribution of human driving
   (including human mistakes), while RL can optimize explicitly for safety and
   comfort reward functions.

   IL is a strong initialization because it immediately produces human-like
   behavior. RL fine-tuning then corrects the inherited human errors and
   optimizes for explicit objectives (minimize collision risk, maximize
   comfort, make progress) that are difficult to demonstrate.


.. admonition:: Question 7
   :class: hint

   Which of the following is a **key validation challenge** specific to
   end-to-end driving models compared to modular pipelines?

   A. End-to-end models cannot be evaluated in simulation.

   B. ISO 26262 assumes modular decomposition, making it difficult to apply
      standard safety arguments to a monolithic E2E system.

   C. End-to-end models require more compute than modular pipelines.

   D. End-to-end models cannot process LiDAR data.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ISO 26262 assumes modular decomposition, making it difficult to
   apply standard safety arguments to a monolithic E2E system.

   ISO 26262 functional safety methodology relies on decomposing system
   requirements into subsystem requirements and testing each component
   independently. A monolithic neural network has no such decomposition,
   requiring novel "neural system safety" frameworks that are still being
   developed by standards bodies in 2026.


.. admonition:: Question 8
   :class: hint

   What is **NVIDIA Alpamayo**?

   A. NVIDIA's hardware SoC for autonomous driving compute.

   B. A vision-language-action model for driving released as part of
      NVIDIA's DRIVE platform in 2025.

   C. NVIDIA's simulation environment that replaces CARLA.

   D. A LiDAR sensor used in NVIDIA's reference vehicle.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A vision-language-action model for driving released as part of
   NVIDIA's DRIVE platform in 2025.

   Alpamayo is a VLA model that generates driving decisions conditioned on
   natural language scene descriptions produced by the model itself. It
   supports free-form language commands from passengers and is integrated
   with NVIDIA's broader DRIVE end-to-end stack.


.. admonition:: Question 9
   :class: hint

   What is the primary purpose of **domain randomization** when training
   end-to-end models in simulation?

   A. To speed up CARLA rendering by simplifying scene geometry.

   B. To vary simulation parameters during training so the model learns
      features that are robust to environment variation, reducing the
      sim-to-real gap.

   C. To generate additional training data by randomly cropping camera images.

   D. To test model performance across different geographic locations.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To vary simulation parameters during training so the model learns
   features that are robust to environment variation, reducing the sim-to-real gap.

   Domain randomization intentionally introduces variation in lighting,
   weather, texture, and object properties during simulation-based training.
   If the model is never presented with a consistent simulation "look", it
   cannot overfit to simulation artifacts and must learn more general features
   that transfer to the real world.


.. admonition:: Question 10
   :class: hint

   As of 2026, what describes the **industry consensus** on where end-to-end
   learning fits in production ADS systems?

   A. Major robotaxi operators run fully end-to-end systems from pixels to
      actuators with no engineered safety layers.

   B. End-to-end learning is considered a failed approach and the industry
      has returned to purely modular pipelines.

   C. E2E models excel at perception and scene understanding, but explicit
      safety checks and rule-based overrides remain as engineered layers on top.

   D. End-to-end models are only used for highway driving, not urban
      environments.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- E2E models excel at perception and scene understanding, but
   explicit safety checks and rule-based overrides remain as engineered
   layers on top.

   No major robotaxi operator in 2026 runs a system that is purely neural
   from camera to brake pedal without any engineered safety monitoring. The
   dominant pattern is a hybrid: a powerful E2E neural backbone for perception
   and initial planning, with an explicit safety module (RSS, rule-based
   overrides) that can veto unsafe actions.


----


True or False (Questions 11-15)
================================

.. admonition:: Question 11
   :class: hint

   **True or False:** In a modular ADS pipeline, a detected pedestrian's
   probability of entering the road can be fully preserved and communicated
   to the planner via the standard object-list interface between perception
   and prediction modules.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The object-list interface between perception and prediction modules
   typically encodes discrete detections with fixed attributes (class, 3-D
   box, velocity). Subtle behavioral cues -- such as a pedestrian looking
   toward the road, crouching, or holding a ball -- that are visible in the
   raw image are often discarded because they don't fit the schema. This is
   the information loss problem that motivates end-to-end approaches.


.. admonition:: Question 12
   :class: hint

   **True or False:** DriveTransformer achieves 3x throughput over UniAD
   by using a smaller model with fewer parameters, sacrificing performance
   on individual driving tasks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   DriveTransformer's throughput improvement comes from **sharing** attention
   computations across tasks through unified agent, map, and ego token types --
   not from reducing model size. DriveTransformer matches or exceeds UniAD on
   planning metrics (L2 distance) while running approximately 3x faster.


.. admonition:: Question 13
   :class: hint

   **True or False:** Tesla's FSD v12 uses a LiDAR sensor as its primary
   perception modality.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Tesla's FSD is camera-only. Tesla argues that cameras provide sufficient
   information for driving because humans navigate with vision alone. The
   FSD v12 architecture uses 8 cameras feeding space-time transformers to
   produce BEV features, with no LiDAR or radar primary sensor.


.. admonition:: Question 14
   :class: hint

   **True or False:** Chain-of-thought (CoT) supervision in VLA models
   provides a language-based training signal that can improve generalization
   to novel scenarios compared to direct waypoint regression.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Language descriptions of scenes encode semantic reasoning (e.g., "the
   cyclist may merge left") that transfers across geographic domains and
   lighting conditions far better than pixel-level imitation labels. VLA
   models trained with CoT supervision have demonstrated better zero-shot
   generalization than equivalent direct regression models in several
   benchmarks (DriveVLM, 2024).


.. admonition:: Question 15
   :class: hint

   **True or False:** The sim-to-real gap is fully eliminated by using
   CARLA for end-to-end training because CARLA uses Unreal Engine 4 for
   photorealistic rendering.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Despite CARLA's high-quality rendering, a significant sim-to-real gap
   remains. Sensor noise models, material reflectances, dynamic agent
   behavior distributions, and environmental conditions in CARLA do not
   perfectly match reality. Neural world models (GAIA-3, Cosmos) trained
   on real data are emerging as a complementary approach to reduce this gap,
   but it has not been eliminated.


----


Essay Questions (Questions 16-18)
===================================

.. admonition:: Question 16
   :class: hint

   **Compare and contrast the UniAD and DriveTransformer architectures.**
   What specific problem does DriveTransformer solve, and what is the
   practical significance of the 3x throughput improvement for real-time
   ADS deployment?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - UniAD uses separate decoder heads per task (TrackFormer, MapFormer,
     MotionFormer, OccFormer), each independently attending to BEV features,
     leading to redundant computation and low throughput (~1.8 FPS).
   - DriveTransformer defines unified agent, map, and ego tokens that share
     a single joint attention block across all tasks, eliminating redundant
     feature extraction.
   - The 3x throughput improvement (from ~1.8 to ~5.5 FPS) is practically
     significant because real-time ADS requires inference within a 50-100 ms
     window to maintain safe reaction times. UniAD's throughput is too low
     for production deployment without significant simplification.
   - DriveTransformer achieves this throughput gain while matching or improving
     on UniAD's planning L2 metric, demonstrating that efficiency and
     accuracy are not in conflict.


.. admonition:: Question 17
   :class: hint

   **Explain the safety and validation challenges unique to end-to-end driving
   models** compared to modular systems. What approaches are researchers and
   engineers pursuing to address these challenges?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Modular systems can be validated module-by-module against ISO 26262
     ASIL requirements with component-level fault trees. E2E models have no
     such decomposition -- the entire neural network must be validated as a
     whole, which is computationally intractable for exhaustive testing.
   - Black-box behavior makes it difficult to determine the root cause of
     failures, which is essential for constructing safety cases and for
     regulator approval.
   - Approaches being pursued include: neural network formal verification
     (limited to small networks), comprehensive simulation-based scenario
     testing, runtime safety monitors (Responsibility-Sensitive Safety),
     concept bottleneck models that enforce interpretable intermediate
     representations, and VLA chain-of-thought reasoning for post-hoc
     explainability.
   - The UNECE GTR (Jan 2026) is moving toward a "safety case" approach
     that may be more amenable to E2E systems than component-level ASIL
     certification.


.. admonition:: Question 18
   :class: hint

   **Explain why Tesla's fleet data advantage is often described as a
   structural moat** in the end-to-end driving paradigm. What are the limits
   of this advantage, and what could competitors do to close the gap?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Tesla has millions of vehicles on the road collecting 8 cameras × 36
     FPS of continuous video, with shadow mode capturing human corrections
     to model errors. This self-reinforcing flywheel -- more vehicles →
     more data → better models → more vehicles -- is extremely difficult
     for a competitor starting from zero fleet to replicate.
   - The advantage is structural because edge cases (rare weather, unusual
     road markings, non-standard lane configurations) are encountered at
     frequency proportional to total fleet miles. With 8.3 billion
     supervised FSD miles, Tesla has covered a vast space of long-tail
     events.
   - Limits: geographic coverage is skewed toward North America; data
     requires annotation cost even with shadow mode; regulatory constraints
     prevent data collection in some regions.
   - Competitors can partially close the gap through: generative world
     models that synthesize rare scenarios from limited real data,
     simulation-to-real techniques, and strategic partnership with OEMs
     for data access (as Mobileye and NVIDIA do).
