====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 10: Prediction &
Decision-Making, including trajectory prediction approaches
(physics-based, maneuver-based, interaction-aware, Transformer-
based), multi-modal prediction metrics, FSM behavior planning,
rule-based vs. learned decision-making, behavior cloning, and
DAgger.

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


.. admonition:: Question 8
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
