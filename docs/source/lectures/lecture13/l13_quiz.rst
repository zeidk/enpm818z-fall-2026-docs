====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 12: World Models & Simulation.
Topics include the definition and architecture of driving world models, Wayve
GAIA-3, NVIDIA Cosmos, Vista (NeurIPS 2024), applications of world models
(data augmentation, long-tail scenarios, offline policy evaluation),
comparison with physics-based simulators like CARLA, the sim-to-real gap,
and the role of world models as imagination modules in end-to-end driving.

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

   What does a **driving world model** predict, given past observations and
   a sequence of future ego actions?

   A. The optimal waypoints the ego vehicle should follow.

   B. The distribution over future observations (video frames) that would
      result from taking those actions.

   C. The 3-D bounding boxes of surrounding agents in the next frame.

   D. The GPS coordinates the ego vehicle will occupy in the future.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The distribution over future observations (video frames) that
   would result from taking those actions.

   A world model learns to simulate future sensory experience conditioned on
   actions. Formally: :math:`p(o_{t+1:t+H} \mid o_{1:t}, a_{t:t+H})`. This
   makes it a data-driven simulator -- a "neural imagination" of future scenes.


.. admonition:: Question 2
   :class: hint

   Wayve GAIA-3, released in December 2025, has approximately how many
   parameters?

   A. 1.5 billion

   B. 9 billion

   C. 15 billion

   D. 70 billion

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- 15 billion

   GAIA-3 has 15 billion parameters and represents a significant scale-up
   from GAIA-1 (9B, 2023). Its scale enables multi-camera consistency,
   long-horizon generation (30+ seconds), and high-fidelity controllable
   scenario synthesis.


.. admonition:: Question 3
   :class: hint

   What is the role of a **visual tokenizer** (such as a VQ-VAE) in a
   driving world model architecture?

   A. It converts driving actions into natural language descriptions.

   B. It compresses high-dimensional video frames into a compact grid of
      latent tokens, making transformer-based modeling tractable.

   C. It detects and classifies objects in the scene before world model
      generation.

   D. It converts GPS waypoints into vehicle control commands.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It compresses high-dimensional video frames into a compact grid
   of latent tokens, making transformer-based modeling tractable.

   A raw 1080p frame has over 6 million pixels -- far too many for a
   transformer to process directly. A VQ-VAE compresses each frame into
   roughly 1024 discrete tokens. The world model then operates in this
   compact latent space, predicting future latent tokens rather than raw pixels.


.. admonition:: Question 4
   :class: hint

   Which of the following is a **key distinction** between NVIDIA Cosmos
   and Wayve GAIA-3?

   A. Cosmos is camera-only while GAIA-3 uses LiDAR.

   B. Cosmos is a general physical world model pre-trained on diverse video
      then fine-tuned for driving, while GAIA-3 is purpose-built for
      driving video from the start.

   C. GAIA-3 is open-source while Cosmos is fully proprietary.

   D. Cosmos can only generate single-camera video while GAIA-3 generates
      multi-camera video.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Cosmos is a general physical world model pre-trained on diverse
   video then fine-tuned for driving, while GAIA-3 is purpose-built for
   driving video from the start.

   NVIDIA Cosmos follows the large-model paradigm of pre-training on massive
   heterogeneous data (robotics, outdoor scenes, driving, manufacturing) to
   learn general physical priors, then fine-tuning on domain-specific data.
   GAIA-3 is specialized for driving from the ground up.


.. admonition:: Question 5
   :class: hint

   Vista (NeurIPS 2024) made what specific contribution that distinguishes
   it from earlier driving world models?

   A. Vista was the first driving world model to use diffusion-based
      video generation.

   B. Vista is the first driving world model to achieve real-time inference
      on consumer hardware.

   C. Vista demonstrated generalizability by training jointly on multiple
      driving datasets from different geographic regions and sensor configurations.

   D. Vista introduced action-conditioned video generation to the field.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Vista demonstrated generalizability by training jointly on
   multiple driving datasets from different geographic regions and sensor
   configurations.

   Earlier models like GAIA-1/2 were trained on a single proprietary dataset
   (Wayve's London fleet) and generalized poorly to other regions. Vista's
   multi-dataset training (nuScenes, Waymo, and others) produces a model that
   transfers to unseen geographic regions and driving styles.


.. admonition:: Question 6
   :class: hint

   **Offline closed-loop policy evaluation** using a world model involves:

   A. Testing a new planner by running it in CARLA with real-time physics
      simulation.

   B. Using the world model to render what would have happened if a new
      planner had been used on historical fleet data, without on-road
      deployment.

   C. Training a new planner on simulated data and then evaluating it on
      real roads.

   D. Recording a human driver and comparing the planner's actions against
      the human baseline.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Using the world model to render what would have happened if a
   new planner had been used on historical fleet data, without on-road
   deployment.

   The key feature of world-model-based offline evaluation is its
   **counterfactual** nature: given historical observations O_{1:T} with
   human actions A_human, we substitute the new planner's actions A_planner
   and ask the world model to render the resulting future. This is called
   "offline closed-loop" because the planner and world model interact in a
   loop, but no real vehicle is involved.


.. admonition:: Question 7
   :class: hint

   Which application of world models **directly addresses** the long-tail
   data problem in ADS development?

   A. Offline policy evaluation using historical fleet logs.

   B. Model-based planning for real-time decision making.

   C. Using text conditioning to generate photo-realistic video of rare
      safety-critical scenarios that are rarely encountered in real data.

   D. Fine-tuning the world model on a small amount of real-world data.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Using text conditioning to generate photo-realistic video of rare
   safety-critical scenarios that are rarely encountered in real data.

   The long tail refers to the vast space of safety-critical edge cases
   (pedestrian darting into road, debris on highway) that are encountered
   too rarely in real data to adequately train or evaluate an ADS. World
   models can synthesize these scenarios on demand using text or structured
   conditioning, providing the training and test coverage that real data alone
   cannot.


.. admonition:: Question 8
   :class: hint

   What is the **sim-to-real gap**, and which of the following is an example
   of it?

   A. The difference in compute cost between running simulation on a laptop
      vs. a GPU cluster.

   B. A model trained exclusively in CARLA that achieves high simulation
      accuracy but fails to detect real-world pedestrians because simulation
      textures differ from real camera images.

   C. The time delay between when CARLA renders a frame and when the Python
      client receives it.

   D. The mismatch between simulated GPS coordinates and real-world GPS
      coordinates.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A model trained exclusively in CARLA that achieves high simulation
   accuracy but fails to detect real-world pedestrians because simulation
   textures differ from real camera images.

   The sim-to-real gap encompasses differences in visual appearance, sensor
   noise characteristics, agent behavior distributions, and dynamics between
   simulation and the real world. Models that overfit to simulation-specific
   patterns often fail at deployment. This is the primary motivation for
   domain randomization and world-model-based data augmentation.


.. admonition:: Question 9
   :class: hint

   In **model-based planning** using a world model, what is the purpose of
   the "imagination rollout"?

   A. To generate training data for the world model itself.

   B. To predict what future observations would result from each candidate
      action sequence, enabling the planner to select the best action without
      executing it in the real world first.

   C. To visualize the ego vehicle's past trajectory for the operator.

   D. To compress the current observation into a latent state for the
      world model encoder.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To predict what future observations would result from each
   candidate action sequence, enabling the planner to select the best action
   without executing it in the real world first.

   Model-based planning uses the world model as an internal simulator: for
   each candidate action sequence, the world model "imagines" the future
   scene, and a reward function evaluates each imagined future. The planner
   selects the action sequence leading to the highest-reward imagined future
   and executes only the first action before re-planning.


.. admonition:: Question 10
   :class: hint

   Why does CARLA remain a valuable tool in ADS development and education
   **alongside** neural world models?

   A. CARLA produces more photo-realistic images than world models.

   B. CARLA provides precise API-level scenario control, perfect ground-truth
      labels, real-time closed-loop physics, and is computationally accessible
      for students and researchers without large GPU clusters.

   C. CARLA can generate more long-tail scenarios than world models.

   D. CARLA is more widely used in industry than world models.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- CARLA provides precise API-level scenario control, perfect
   ground-truth labels, real-time closed-loop physics, and is computationally
   accessible for students and researchers without large GPU clusters.

   The two simulation paradigms are complementary: CARLA is ideal for
   controlled algorithm development, debugging, and education because of its
   precise controllability and structured labels. World models are ideal for
   large-scale synthetic data generation and photo-realistic evaluation, but
   require expensive GPU infrastructure and do not provide structured labels.


----


True or False (Questions 11-15)
================================

.. admonition:: Question 11
   :class: hint

   **True or False:** A driving world model trained on real data produces
   training images that are visually indistinguishable from real camera
   images, completely eliminating the sim-to-real gap.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   While world models trained on real data dramatically reduce the visual
   appearance gap compared to physics-based simulators, they do not
   completely eliminate the sim-to-real gap. Generated images may contain
   artifacts, agent behavior distributions may not perfectly match the real
   world, and physical dynamics remain approximate. The gap is reduced, not
   eliminated.


.. admonition:: Question 12
   :class: hint

   **True or False:** Autoregressive world models generate all future frames
   simultaneously in a single forward pass, making them faster than diffusion
   models at inference time.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Autoregressive models generate tokens **sequentially** -- each token is
   predicted after all previous tokens -- making them slow at inference,
   particularly for long video sequences. Diffusion models generate all tokens
   through an iterative denoising process that can be parallelized, typically
   making them faster than autoregressive models at high resolutions.


.. admonition:: Question 13
   :class: hint

   **True or False:** Vista (NeurIPS 2024) introduced a standard evaluation
   protocol for driving world models that includes measuring action
   controllability error.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   One of Vista's key contributions was proposing and adopting a standard
   evaluation protocol for driving world models. Prior to Vista, different
   papers used different metrics, making comparison difficult. Vista's
   protocol includes FID, FVD (video-level quality), and action controllability
   error -- a metric measuring how accurately the generated video reflects the
   input ego action sequence.


.. admonition:: Question 14
   :class: hint

   **True or False:** NVIDIA Cosmos is released exclusively under a
   proprietary license and is not available for academic research.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   NVIDIA released Cosmos under an open license for non-commercial research,
   making it accessible to academic researchers and students. The production
   DRIVE variant integrated into NVIDIA's commercial ADS stack is proprietary,
   but the base Cosmos model weights and code are publicly available.


.. admonition:: Question 15
   :class: hint

   **True or False:** Domain randomization reduces the sim-to-real gap by
   training the model on a fixed, carefully crafted simulation environment
   that closely resembles the real world.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Domain randomization works by **randomly varying** simulation parameters
   (textures, lighting, weather, object colors, dynamics) during training --
   the opposite of creating a fixed, carefully crafted environment. The
   rationale is that if the model is trained across a wide range of simulation
   variations, it cannot overfit to simulation-specific artifacts and must
   learn features that are present across all variations, including in the
   real world.


----


Essay Questions (Questions 16-18)
===================================

.. admonition:: Question 16
   :class: hint

   **Explain how a world model can be used for offline closed-loop policy
   evaluation.** Why is this valuable, and what are the limitations of
   this evaluation approach?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Offline closed-loop evaluation replaces human actions in historical fleet
     logs with the new planner's actions and uses the world model to render
     what would have happened, enabling counterfactual assessment without
     on-road deployment.
   - This is valuable because it dramatically reduces the cost and safety
     risk of evaluating new planners: instead of deploying on the road and
     hoping nothing goes wrong, engineers can evaluate millions of
     counterfactual scenarios on a GPU cluster in hours.
   - Limitations: the evaluation is only as good as the world model's
     accuracy. If the world model fails to realistically simulate how other
     agents would respond to the new planner's different actions (reaction
     modeling), the counterfactual is inaccurate. This is the **agent
     reaction problem** in offline evaluation.
   - A second limitation is distribution shift: if the new planner takes
     actions far outside the historical data distribution, the world model
     may generate unrealistic futures (hallucinations).


.. admonition:: Question 17
   :class: hint

   **Compare and contrast CARLA and a generative world model like GAIA-3**
   as simulation environments for ADS development. For each, name two
   use cases where it is clearly the better choice, and explain why.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - CARLA is better for: (1) debugging perception and planning algorithms,
     because it provides exact ground-truth labels and API-level scenario
     control; (2) real-time closed-loop testing of a specific scenario, because
     CARLA's physics engine responds instantly to the ego vehicle's actions
     without approximation.
   - GAIA-3 / world models are better for: (1) large-scale synthetic training
     data generation, because world models produce photo-realistic images with
     real-world appearance statistics at scale; (2) rare scenario simulation
     where the visual appearance matters for perception, because CARLA's
     appearance gap would cause a perception model to behave differently on
     real data.
   - The practical difference is cost and control: CARLA is cheap and precise;
     world models are expensive and probabilistic but produce photo-realistic
     output.


.. admonition:: Question 18
   :class: hint

   **What is the "long-tail problem" in ADS development, and how do
   driving world models address it?** Describe a concrete example of
   a long-tail scenario and explain how a world model would be used to
   generate training data for it.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The long-tail problem refers to the fact that safety-critical driving
     scenarios (e.g., child running into road, tire blowout, wrong-way driver)
     are extremely rare in real data. Even with billions of driving miles,
     these events may appear only dozens or hundreds of times -- insufficient
     to train or evaluate a robust system.
   - Example: a child chasing a ball into a crosswalk while the ego vehicle
     is approaching at 40 km/h with obstructed sightlines (parked trucks on
     both sides). This scenario requires a sub-second brake response and is
     nearly impossible to collect real data for safely.
   - Using a world model: an engineer provides text conditioning
     ("child suddenly runs from behind a parked truck into the crosswalk ahead")
     along with an ego action sequence (constant speed) to GAIA-3. The model
     generates photo-realistic video of the scenario across different lighting,
     weather, and child trajectory variations. These images are used to train
     and evaluate the perception system's response time.
   - The world model addresses both the data scarcity (unlimited generation)
     and the safety concern (no real child is placed at risk).
