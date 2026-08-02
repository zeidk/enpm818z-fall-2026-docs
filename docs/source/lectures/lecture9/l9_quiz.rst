====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 9: Prediction &
Behavior Modeling, including trajectory prediction approaches
(physics-based, maneuver-based, interaction-aware, Transformer-
based), scene encoding, multi-modal prediction metrics, FSM behavior
planning, rule-based vs. learned decision-making, and practical
decision-making in traffic.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement
     is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   At a busy intersection, an autonomous vehicle must decide
   whether to proceed or yield. The minimum prediction horizon
   it needs to reason about crossing agents is approximately:

   A. 0.5 seconds

   B. 1 second

   C. 5--8 seconds

   D. 30 seconds

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- 5--8 seconds.

   A vehicle crossing at 50 km/h (14 m/s) takes roughly 3--5 s
   to cross a 40--70 m intersection. The ego vehicle also needs
   time to accelerate and clear the intersection. In total,
   5--8 s of prediction is needed to safely evaluate whether
   to proceed. Sub-second prediction is sufficient only for
   emergency braking (collision imminent); it is far too short
   for intersection negotiation.


.. admonition:: Question 2
   :class: hint

   The Constant Turn Rate and Acceleration (CTRA) model predicts
   agent trajectories using which measured quantities?

   A. Position, heading, yaw rate, and longitudinal acceleration

   B. Position, velocity, jerk, and mass

   C. GPS coordinates and map-matched lane ID

   D. Optical flow from a front-facing camera

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- Position, heading, yaw rate, and longitudinal
   acceleration.

   CTRA assumes constant yaw rate :math:`\omega` and constant
   longitudinal acceleration :math:`a`, integrating these over
   time to extrapolate the future position and heading. These
   quantities can be measured directly from the IMU (yaw rate)
   and from differentiated GPS or odometry (acceleration).
   CTRA outperforms CV in curved motion but still fails when
   agents change intent (e.g., braking at a stop sign).


.. admonition:: Question 3
   :class: hint

   In maneuver-based prediction, the intent classification step
   is limited because:

   A. Intent classifiers require GPU hardware not available
      on embedded automotive platforms.

   B. The discrete maneuver set is hand-designed and cannot
      cover all real-world behaviors; transitions between
      maneuvers are abrupt.

   C. Intent classification requires access to the agent's
      internal state (acceleration pedal position).

   D. Classifiers require at least 10 seconds of agent history.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The discrete maneuver set is hand-designed and
   cannot cover all real-world behaviors; transitions are abrupt.

   Any hand-crafted maneuver taxonomy (lane keep, lane change,
   stop, etc.) is an approximation of the continuous space of
   possible agent behaviors. Rare behaviors (abrupt U-turns,
   cyclists entering the road from a sidewalk) fall outside
   the predefined set. Additionally, the boundary between
   maneuver classes produces a step-change in predicted
   trajectory, which is physically implausible.


.. admonition:: Question 4
   :class: hint

   MotionTransformer achieves interaction-aware prediction by:

   A. Simulating all agent interactions using a physics engine
      and sampling trajectories from the simulation.

   B. Using factorized multi-head self-attention over agent
      and map tokens, allowing each agent to attend to all
      other agents and road elements.

   C. Clustering agent histories into discrete motion modes
      using k-means and fitting a linear model per cluster.

   D. Reusing the ego vehicle's MPC prediction model for
      surrounding agents.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Using factorized multi-head self-attention over
   agent and map tokens.

   The Transformer's self-attention mechanism allows every
   agent token to exchange information with every other agent
   token and every map token in each layer. This naturally
   captures social interactions (yielding, gap acceptance,
   following) without explicitly modeling pairwise interactions.
   Factorized attention reduces the :math:`O(N^2)` cost by
   separating agent-to-agent and agent-to-map attention.


.. admonition:: Question 5
   :class: hint

   The MinADE_K metric evaluates trajectory prediction by:

   A. Computing the average displacement error of all K
      predicted trajectories and averaging over K.

   B. Selecting the single best prediction (minimum ADE) among
      the K predictions for each scenario.

   C. Computing the maximum displacement error across all K
      predictions.

   D. Evaluating the calibration of predicted probabilities
      across K modes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Selecting the single best prediction (minimum ADE)
   among K predictions for each scenario.

   MinADE_K (also written mADE@K) evaluates the oracle performance:
   given K predicted trajectories, how well does the best one
   match the ground truth? This rewards *diversity* -- a system
   that covers many possible futures will score well even if
   individual trajectories are not highly probable. Critics of
   MinADE argue that it ignores probability calibration, which
   is why mAP is increasingly used alongside it.


.. admonition:: Question 6
   :class: hint

   In a highway driving FSM, the transition
   ``LANE_FOLLOW`` → ``LANE_CHANGE_LEFT`` should be gated on which
   conditions?

   A. Current speed > 100 km/h only.

   B. Lead vehicle speed is below reference speed AND the left
      lane has a safe gap > minimum safe distance ahead and
      behind the ego.

   C. The left turn signal has been on for more than 3 seconds.

   D. The ego vehicle has been in ``LANE_FOLLOW`` for more
      than 10 seconds.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Lead vehicle below reference speed AND safe gap
   in the left lane.

   Both conditions must hold: there must be a reason to change
   lanes (blocked by a slow vehicle) and a safe opportunity
   (gap in the target lane). Gating on speed alone would cause
   unnecessary lane changes; gating on gap alone would change
   lanes without motivation. The gap check uses predicted agent
   positions (from the prediction module) to verify safety
   for the duration of the lane-change maneuver.


.. admonition:: Question 7
   :class: hint

   Modern learned trajectory predictors (e.g., VectorNet) encode
   the map and agent histories as **vectorized polylines** rather
   than rasterized BEV images primarily because:

   A. Rasterized images cannot be processed by neural networks.

   B. Polylines are a sparse, structured representation that
      preserves geometric relationships and is far more compute-
      and memory-efficient than dense image rasters.

   C. Vectorized inputs remove the need for any map data.

   D. Rasterization requires LiDAR, which is often unavailable.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Polylines are a sparse, structured representation that
   preserves geometric relationships and is far more compute- and
   memory-efficient than dense image rasters.

   Early predictors rendered the HD map and agent tracks into a
   multi-channel BEV image processed by a CNN, which is wasteful
   (most pixels are empty) and blurs precise geometry. VectorNet
   instead represents lanes, crosswalks, and agent tracks as sets
   of polylines encoded with a graph/attention network, keeping
   exact coordinates and connectivity at a fraction of the cost.


.. admonition:: Question 8
   :class: hint

   A predictor that outputs an **independent (marginal)** trajectory
   distribution for each agent can be unsafe for planning because:

   A. Marginal predictions are always less accurate than a constant
      velocity baseline.

   B. The per-agent predictions may be mutually inconsistent -- e.g.,
      two agents each predicted to occupy the same space, or both
      predicted to yield to each other.

   C. Marginal predictions cannot be evaluated with MinADE.

   D. Marginal predictions require joint LiDAR-camera fusion.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The per-agent predictions may be mutually inconsistent.

   Marginal prediction estimates each agent's future in isolation,
   so the combination of most-likely modes across agents need not
   form a physically consistent scene: two cars can both be predicted
   into the same gap, or a "both yield" / "both go" deadlock can
   appear. Scene-level (joint) prediction models the agents' futures
   together, producing a self-consistent set of trajectories that a
   planner can reason about safely.


.. admonition:: Question 9
   :class: hint

   The **gap acceptance** problem at an uncontrolled intersection
   requires predicting:

   A. The traffic light phase remaining time.

   B. The time gap available in the crossing traffic stream and
      whether the ego can cross before the next vehicle arrives.

   C. The number of lanes on the cross street.

   D. The ego vehicle's braking distance at current speed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The time gap in the crossing traffic stream and
   whether the ego can complete the crossing within that gap.

   Gap acceptance is the decision of whether to enter a traffic
   stream given a current gap. The ego must predict how long
   the current gap will remain open (based on approaching
   vehicle speed and distance) and compare it to the time
   needed to cross (based on ego speed and intersection width).
   Fixed-threshold rules work poorly because the required gap
   size depends on ego speed, intersection geometry, and
   approaching vehicle speed.


.. admonition:: Question 10
   :class: hint

   Multi-modal trajectory prediction outputs
   :math:`K` trajectories with probabilities
   :math:`\{(\hat{\tau}_k, p_k)\}_{k=1}^K`. A planner uses
   these to:

   A. Execute the trajectory with the highest probability
      :math:`k^* = \arg\max_k p_k` and ignore all others.

   B. Generate ego-trajectory candidates evaluated for safety
      against all predicted agent modes, weighting risk by
      mode probability.

   C. Compute the average predicted trajectory weighted by
      probabilities and plan against this mean trajectory.

   D. Request more sensor data until prediction uncertainty
      falls below a threshold.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Generate ego-trajectory candidates evaluated for
   safety against all predicted agent modes, weighted by
   probability.

   Taking only the mode with highest probability ignores the
   tail risk of other plausible behaviors. The correct approach
   is to evaluate candidate ego-trajectories against all :math:`K`
   agent modes and select the ego trajectory that minimizes
   expected collision risk:

   .. math::

      \hat{\tau}_{\text{ego}} = \arg\min_\tau
      \sum_k p_k \cdot \mathcal{R}(\tau, \hat{\tau}_k^{\text{agent}})

   This ensures the ego plan is robust to the full distribution
   of agent futures.


----


True / False
============

.. admonition:: Question 11
   :class: hint

   **True or False:** Physics-based trajectory prediction models
   such as the Constant Velocity (CV) model are accurate for
   prediction horizons of 5--8 seconds on highway roads.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   CV and CTRA models are accurate for approximately 0.5--1 s
   on straight roads, where the constant-motion assumption holds.
   Over 5--8 s, agents frequently change speed, turn, or make
   lane changes -- all of which violate the CV assumption.
   Prediction error grows approximately linearly with horizon
   for CV. At 5 s, CV errors of 10--20 m are common in
   real traffic, making it unsuitable for intersection
   negotiation or merge planning.


.. admonition:: Question 12
   :class: hint

   **True or False:** The mAP (mean Average Precision) metric
   for multi-modal prediction rewards both accurate trajectory
   positions and well-calibrated probabilities.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   mAP treats each predicted mode as a detection: a mode is a
   true positive if its endpoint is within a distance threshold
   of the ground truth AND its probability rank is consistent
   with its precision-recall curve. Unlike MinADE, mAP jointly
   penalizes both inaccurate trajectories and poor probability
   estimates, making it a more complete evaluation metric for
   probabilistic prediction.


.. admonition:: Question 13
   :class: hint

   **True or False:** A finite state machine behavior planner
   can, in principle, handle every possible traffic scenario
   given a sufficiently large number of states and transitions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   While an FSM can be made arbitrarily complex, the number of
   distinct traffic situations grows combinatorially with the
   number of agents, their states, and environmental conditions.
   In practice, FSMs are designed for the most common scenarios
   and fail gracefully in edge cases that were not anticipated
   during design. The fundamental issue is that traffic scenarios
   exist on a continuous manifold, not a discrete state space
   that FSMs naturally represent.


.. admonition:: Question 14
   :class: hint

   **True or False:** A unimodal predictor trained to regress a
   single trajectory with mean-squared-error loss tends to output
   the *average* of several distinct possible futures, which can be
   a trajectory no real agent would take.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   MSE regression to a single output is minimized by the conditional
   mean. When the true future is multi-modal (e.g., an agent will
   either turn left or go straight), the mean of those modes points
   "up the middle" -- straight into the median island or oncoming
   lane. This mode-averaging pathology is the core motivation for
   multi-modal prediction, which outputs several distinct trajectories
   with probabilities instead of one averaged path.


.. admonition:: Question 15
   :class: hint

   **True or False:** The Social Force Model (Helbing & Molnar)
   is a learning-based prediction approach that uses neural
   networks to model pedestrian interactions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The Social Force Model is a **physics-based** approach that
   uses hand-crafted attractive and repulsive force functions to
   model pedestrian motion. It does not use neural networks.
   Forces are computed analytically from relative positions and
   velocities. While the model can be parameterized and fitted to
   data, it is not a learning-based approach in the neural network
   sense. Learning-based social interaction models (e.g.,
   Social GAN, MotionTransformer) emerged much later.


----


Essay Questions
===============

.. admonition:: Question 16
   :class: hint

   **Compare physics-based, maneuver-based, and learned (Transformer)
   trajectory prediction.** Describe the strengths and weaknesses of
   each and the prediction horizon and scenario where each is most
   appropriate.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Physics-based (CV, CTRA): no training data, interpretable, and
     accurate for very short horizons (0.5--1 s) and simple motion.
     Weakness: assumes constant motion, so it fails during turns,
     stops, and any intent change; unusable beyond ~2 s.
   - Maneuver-based: classifies a discrete intent (lane keep, turn,
     stop) then predicts a trajectory per maneuver. Strength: adds
     semantic structure and multi-modality. Weakness: the hand-designed
     maneuver set cannot cover all behaviors and produces abrupt
     class-boundary transitions.
   - Learned/Transformer (MotionTransformer, VectorNet): jointly
     encodes agents and map with attention, producing interaction-aware,
     multi-modal predictions accurate to 5--8 s. Strength: state of the
     art in complex urban interaction. Weakness: needs large datasets,
     is less interpretable, and can fail out of distribution.
   - Practical takeaway: short-horizon safety fallbacks often use a
     physics model, while the primary predictor for planning in urban
     ODDs is a learned interaction-aware model.


.. admonition:: Question 17
   :class: hint

   **Explain why single-trajectory prediction is insufficient for
   autonomous driving and what multi-modal prediction provides.**
   Contrast how MinADE_K and mAP evaluate a multi-modal predictor.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A single predicted trajectory collapses genuinely ambiguous
     futures (turn vs. straight, yield vs. go) into one path, and an
     MSE-trained regressor averages those modes into an implausible
     "middle" trajectory. Planning against a single wrong future is
     unsafe.
   - Multi-modal prediction outputs K trajectories with probabilities
     :math:`\{(\hat{\tau}_k, p_k)\}`, each representing a distinct
     behavioral hypothesis, so the planner can hedge against all
     plausible agent intents.
   - MinADE_K is an oracle metric: it scores only the best-matching of
     the K modes, rewarding coverage/diversity but ignoring whether the
     probabilities are calibrated.
   - mAP treats each mode as a detection and jointly rewards accurate
     endpoints and well-ranked probabilities, so it penalizes an
     overconfident wrong mode. Reporting both gives a fuller picture:
     MinADE for coverage, mAP for calibration.


.. admonition:: Question 18
   :class: hint

   **Describe the MotionTransformer architecture for trajectory
   prediction.** Explain how the attention mechanism enables
   interaction-aware prediction and what the multi-modal output
   represents.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - MotionTransformer uses a two-stage Transformer architecture:
     a global motion Transformer encodes all agents and map
     polylines jointly using factorized self-attention; a local
     motion Transformer decodes :math:`K` trajectory modes per
     agent using a set of learnable motion query pairs.
   - The self-attention mechanism allows every agent token to
     attend to every other agent and every map element in each
     layer. Attention weights implicitly represent how much
     each agent's future depends on neighboring agents and road
     geometry -- capturing merging, following, and yielding
     interactions without explicit pairwise modeling.
   - The multi-modal output :math:`\{(\hat{\tau}_k, p_k)\}` represents
     :math:`K` plausible future trajectories and their probabilities.
     Each mode corresponds to a different behavioral hypothesis
     (e.g., turn left vs. go straight vs. stop), allowing the
     planner to reason about the full distribution of possible
     agent behaviors.
   - MotionTransformer achieves state-of-the-art performance on
     the Waymo Open Motion Dataset benchmark, demonstrating that
     joint attention over all scene elements is a powerful
     inductive bias for trajectory prediction.
