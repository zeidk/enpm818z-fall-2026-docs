====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 12: End-to-End Driving,
VLA & Imitation Learning. Topics include the modular vs. end-to-end
debate, UniAD (CVPR 2023), DriveTransformer (ICLR 2025),
Vision-Language-Action (VLA) models, Tesla's FSD v12 architecture,
NVIDIA's end-to-end stack with reinforcement learning, behavior
cloning and the distribution-shift / compounding-error problem,
DAgger, and the safety and validation challenges of black-box neural
driving systems.

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

   The fundamental problem with behavior cloning (BC) that
   DAgger is designed to solve is:

   A. Behavior cloning requires labeled data, which is expensive
      to collect.

   B. Distribution shift: the policy visits states not seen
      during training, where it has no supervision signal,
      causing compounding errors.

   C. Behavior cloning converges to the wrong policy because
      the supervised loss is non-convex.

   D. Behavior cloning cannot learn from continuous action
      spaces.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Distribution shift causing compounding errors.

   When a BC policy makes a small error, it moves to a state
   slightly off the expert's trajectory. The policy was never
   trained on this state, so it may make another error in
   a bad direction. Errors compound quadratically in the time
   horizon (:math:`O(\epsilon T^2)`). DAgger fixes this by
   querying the expert at states the learned policy actually
   visits, so the training distribution converges to the
   deployment distribution.


.. admonition:: Question 9
   :class: hint

   DAgger improves over behavior cloning by:

   A. Using a larger neural network with more capacity.

   B. Iteratively rolling out the learned policy and augmenting
      the training dataset with expert actions at visited states.

   C. Using reinforcement learning with a reward signal instead
      of supervised learning.

   D. Training on randomized simulation environments to cover
      more state diversity.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Iteratively rolling out the learned policy and
   augmenting the dataset with expert labels at visited states.

   DAgger is a supervised learning algorithm (not RL), but it
   uses an online data collection loop. At each iteration the
   current policy generates new states, the expert labels them,
   and these are added to the aggregated dataset. Over iterations
   the training distribution converges to the deployment
   distribution, reducing compounding errors from
   :math:`O(\epsilon T^2)` to :math:`O(\epsilon T)`.


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

   **True or False:** In DAgger, the expert is only queried at
   states that the *expert* would visit, not states that the
   *learned policy* visits.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   DAgger explicitly queries the expert at states that the
   **learned policy** visits during its rollouts. This is the
   key distinction from standard behavior cloning. By labeling
   states on the *policy's* trajectory (not the expert's),
   DAgger provides supervision at the states where the policy
   will actually be deployed, closing the distribution shift gap.


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

   **Explain the distribution shift problem in behavior cloning
   and why it causes compounding errors.** Use a concrete
   autonomous driving example to illustrate the failure mode.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Behavior cloning trains a policy on expert state-action pairs.
     During deployment, the policy's own actions take it to states
     that differ from the expert's trajectory -- these states were
     never seen during training.
   - Concrete example: the expert always stays centered in the lane.
     The BC policy makes a small right-drift error, ending up
     slightly off-center. This state was never in the training set,
     so the policy has no reliable recovery action and may drift
     further right -- eventually leaving the lane.
   - Errors compound because each mistake produces a new out-of-
     distribution state, which produces a larger mistake, which
     produces an even more out-of-distribution state.
   - The compounding grows as :math:`O(\epsilon T^2)` where
     :math:`\epsilon` is the per-step error and :math:`T` is
     the episode length -- making BC fragile for long-horizon tasks.


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

   **Compare rule-based FSM behavior planners with learned
   (imitation learning) behavior planners.** Under what
   operational conditions would you choose each approach, and
   what hybrid strategies exist?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - FSM planners are preferred when: interpretability and
     certifiability are required (regulatory approval), the
     operational design domain (ODD) is well-defined and narrow,
     or real-time guarantees with bounded computation are needed.
   - Learned planners are preferred when: the ODD is broad and
     difficult to enumerate (urban driving), human-like interaction
     is required (gap acceptance, courtesy behaviors), or large
     logged datasets are available to train from.
   - Hybrid strategies: use an FSM for safety-critical decisions
     (emergency stop, right-of-way) with a learned planner for
     non-safety-critical comfort behaviors (smooth merges, yield
     negotiation). The safety layer can override the learned policy
     whenever a formal safety condition is violated.
   - Another hybrid: use a learned policy as a cost function or
     prior within a model-based planner (e.g., RL-guided lattice
     search), combining the interpretability of the lattice with
     the generalization of learned policies.
