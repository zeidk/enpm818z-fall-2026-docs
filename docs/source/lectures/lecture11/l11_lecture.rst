====================================================
Lecture
====================================================

.. raw:: latex

   \setcounter{figure}{0}


Why Prediction Matters
====================================================

An autonomous vehicle does not exist in isolation. At every moment,
it shares the road with pedestrians, cyclists, motorcycles, and
other vehicles -- all of whose future positions directly affect
which plans are safe.

.. dropdown:: The Prediction Problem

   **Planning needs future states, but only current states are
   observable.**

   Without prediction, a planner can only react to the current
   positions of other agents. By the time the planner computes a
   safe maneuver and the vehicle executes it (200--500 ms latency),
   other agents have moved -- potentially into the path.

   **Prediction horizon requirements:**

   .. list-table::
      :header-rows: 1
      :widths: 30 20 50

      * - Maneuver type
        - Horizon needed
        - Rationale
      * - Emergency braking
        - 1 s
        - Collision imminent
      * - Lane change
        - 3--5 s
        - Must verify clearance ahead
      * - Intersection negotiation
        - 5--8 s
        - Other agents crossing at full speed
      * - Highway merge
        - 5--10 s
        - Speed differential at merge point

   .. admonition:: The Prediction-Planning Loop
      :class: tip

      Prediction feeds planning: the planner uses predicted agent
      trajectories to evaluate which candidate ego-trajectories are
      collision-free. In interaction-aware systems, ego plans and
      agent predictions are solved jointly -- the ego's action
      changes agent behavior, which changes the optimal ego action.


Trajectory Prediction Approaches
====================================================

Prediction methods span a spectrum from physics-based extrapolation
to data-driven interaction modeling.

.. list-table:: Prediction Approach Comparison
   :header-rows: 1
   :widths: 22 22 22 34

   * - Approach
     - Representation
     - Interaction-aware
     - Key limitation
   * - Physics-based
     - Constant velocity / CTRA
     - No
     - Fails at maneuvers, intersections
   * - Maneuver-based
     - Intent + conditional model
     - Partial
     - Discrete maneuver set
   * - Interaction-aware
     - Social force / LSTM
     - Yes
     - Complex to train, slow
   * - Transformer-based
     - Attention over agents
     - Yes
     - Requires large datasets


Physics-Based Prediction
------------------------

.. dropdown:: Constant Velocity and CTRA

   The simplest prediction model assumes the agent continues
   its current motion:

   **Constant Velocity (CV):**

   .. math::

      x(t+\Delta t) &= x(t) + v_x \Delta t \\
      y(t+\Delta t) &= y(t) + v_y \Delta t

   **Constant Turn Rate and Acceleration (CTRA):**

   .. math::

      x(t+\Delta t) &= x + \frac{a}{\omega^2}
        \left[\omega \Delta t \cos(\theta + \omega\Delta t)
        + \sin(\theta+\omega\Delta t) - \sin\theta\right] \\
      y(t+\Delta t) &= y + \frac{a}{\omega^2}
        \left[\omega \Delta t \sin(\theta + \omega\Delta t)
        - \cos(\theta+\omega\Delta t) + \cos\theta\right]

   where :math:`\omega` is the measured yaw rate and :math:`a` is
   longitudinal acceleration.

   Physics-based models are O(1), deterministic, and run in
   microseconds. They are accurate for the first 0.5--1 s but
   diverge rapidly at maneuver boundaries.


Maneuver-Based Prediction
-------------------------

.. dropdown:: Intent Classification + Conditional Model

   Maneuver-based prediction separates the problem into two stages:

   1. **Intent classification:** classify the agent's current
      maneuver intent into a discrete set
      :math:`\mathcal{M} = \{`keep lane, left change, right change,
      accelerate, decelerate, stop:math:`\}`.

   2. **Conditional trajectory model:** given intent :math:`m`,
      predict the trajectory using a physics model or learned
      regressor conditioned on :math:`m`.

   **Intent classification** is typically a binary or multi-class
   classifier taking as input:

   - Relative velocity and acceleration of the agent
   - Distance to lane boundaries
   - Turn signal state (if observable)
   - Historical trajectory over the past 2--3 s

   **Limitation:** the maneuver set is hand-designed and may not
   cover all real-world behaviors. Transitions between maneuvers
   are abrupt.


Interaction-Aware Prediction
----------------------------

.. dropdown:: Social Force and Graph Models

   Interaction-aware models explicitly model the influence of
   nearby agents on each other.

   **Social Force Model (Helbing & Molnar, 1995):**

   .. math::

      \dot{\mathbf{v}}_i = \frac{\mathbf{v}_i^0 - \mathbf{v}_i}{\tau}
      + \sum_{j \neq i} f_{ij} + f_{i,\text{boundary}}

   where :math:`\mathbf{v}_i^0` is the desired velocity, :math:`\tau`
   is a relaxation time, and :math:`f_{ij}` is a repulsive force
   from agent :math:`j`.

   **Graph Neural Network (GNN) approaches:** agents are nodes
   in a graph; edges encode pairwise interactions. Graph
   convolutions propagate influence across agents at each
   prediction step.

   Interaction-aware models capture behaviors like merging
   courtesy and pedestrian group dynamics that physics-based
   models entirely miss.


Transformer-Based Prediction
====================================================

Modern state-of-the-art prediction systems use Transformer
architectures to encode the full scene context.

.. dropdown:: Scene Encoding

   A Transformer-based predictor encodes:

   - **Agent history:** past trajectory tokens
     :math:`\{(x_t, y_t, \theta_t, v_t)\}_{t=-T}^{0}`
     for each agent, projected to a feature dimension
     :math:`d_{\text{model}}`.
   - **Map context:** road centerlines, lane boundaries,
     stop lines, and crosswalks are encoded as polyline
     tokens using a PointNet-style encoder.
   - **Agent type:** pedestrian, cyclist, vehicle --
     embedded as a learned type token.

   All tokens are concatenated and processed by a Transformer
   encoder with multi-head self-attention, allowing each agent
   to attend to all other agents and map elements.

.. dropdown:: MotionTransformer Architecture

   **MotionTransformer** (Shi et al., NeurIPS 2023) introduces
   a two-stage architecture:

   1. **Global motion transformer:** encodes all agents and map
      elements jointly using factorized attention, producing
      per-agent context embeddings.

   2. **Local motion transformer:** for each agent, decodes
      :math:`K` future trajectory modes using a set of
      learnable **motion query pairs** (one per mode) that
      attend to the agent's context embedding.

   The output is :math:`K` trajectory predictions with
   associated probabilities:

   .. math::

      \{(\hat{\tau}_k, p_k)\}_{k=1}^{K}, \quad \sum_k p_k = 1

   MotionTransformer achieves state-of-the-art performance on
   the Waymo Open Motion Dataset (WOMD) benchmark.

.. dropdown:: Scene Context Encoding Detail

   The map encoding uses a **hierarchical polyline encoder**:

   - Each road element (lane, boundary, stop line) is a polyline
     of ordered points.
   - A PointNet-style MLP encodes each point to a feature vector.
   - Max-pooling over the points gives a fixed-size polyline
     feature.
   - Cross-attention allows each agent query to attend to all
     polyline features, incorporating spatial map context.

   **Positional encoding** uses sinusoidal encodings of
   :math:`(x, y, \theta)` so the attention mechanism is
   geometry-aware.


Multi-Modal Prediction
====================================================

Real agents can take multiple plausible future actions. A single
deterministic prediction is insufficient for safe planning.

.. dropdown:: Why Multi-Modal Matters

   At an intersection, a vehicle approaching from the left
   might go straight, turn right, or turn left. Any single
   predicted trajectory represents only one hypothesis.

   If the ego planner uses a single predicted trajectory and
   the agent takes a different action, the plan may fail.
   With multi-modal predictions, the planner can:

   - Generate candidate ego-trajectories for each agent mode.
   - Compute the worst-case (most dangerous) agent mode.
   - Select the ego trajectory that is safe across all likely
     agent modes weighted by probability.

.. dropdown:: Evaluation Metrics

   .. list-table:: Multi-Modal Prediction Metrics
      :header-rows: 1
      :widths: 25 30 45

      * - Metric
        - Formula
        - Meaning
      * - minADE_K
        - :math:`\min_k \text{ADE}(\hat{\tau}_k, \tau^*)`
        - Best-of-K average displacement error
      * - minFDE_K
        - :math:`\min_k \|\hat{\tau}_k(T) - \tau^*(T)\|`
        - Best-of-K final displacement error
      * - MissRate
        - Fraction of scenarios where :math:`\text{FDE} > 2` m
        - Prediction failure rate
      * - mAP
        - Mean Average Precision over modes
        - Joint quality of positions and probabilities

   .. admonition:: The Oracle Problem
      :class: warning

      MinADE and MinFDE evaluate only the *best* of :math:`K`
      predictions. A system that outputs many diverse trajectories
      will score well on these metrics even if its probability
      estimates are poor. mAP jointly evaluates probability
      calibration and trajectory accuracy.


Behavior Planning
====================================================

Behavior planning is the **strategic layer**: it decides what the
vehicle should *do* (which maneuver to execute) based on the
current traffic situation.

.. dropdown:: Position in the Stack

   .. list-table::
      :header-rows: 1
      :widths: 20 30 50

      * - Layer
        - Input
        - Output
      * - Perception
        - Sensor data
        - Agent detections, HD map
      * - Prediction
        - Agent history + map
        - Agent trajectory distributions
      * - **Behavior planning**
        - Predicted states + rules
        - Maneuver decision (current + next N steps)
      * - Motion planning
        - Maneuver decision + map
        - Collision-free path
      * - Trajectory planning
        - Path + speed profile
        - Time-stamped trajectory
      * - Control
        - Trajectory
        - Steering + throttle/brake


State Machine Behavior Planner
===============================

The finite state machine (FSM) is the classical approach to
behavior planning.

.. dropdown:: States and Transitions

   A highway driving FSM with four states:

   .. list-table::
      :header-rows: 1
      :widths: 20 40 40

      * - State
        - Behavior
        - Exit condition
      * - ``LANE_FOLLOW``
        - Follow lane at reference speed
        - Slow vehicle ahead OR lane change opportunity
      * - ``LANE_CHANGE_LEFT``
        - Execute left lane change maneuver
        - Maneuver complete OR abort (gap closes)
      * - ``LANE_CHANGE_RIGHT``
        - Execute right lane change maneuver
        - Maneuver complete OR abort
      * - ``FOLLOW``
        - Adaptive cruise control behind lead vehicle
        - Lead vehicle clears OR speed returns to reference
      * - ``STOP``
        - Decelerate to zero
        - Stop line reached, signal clears, or obstacle removed
      * - ``YIELD``
        - Decelerate, give right-of-way
        - Intersection clear

   **Transition conditions** use predicted agent states:

   - ``LANE_FOLLOW`` → ``FOLLOW``: predicted collision with lead
     vehicle within :math:`t_{\text{ttc}} < 3` s.
   - ``FOLLOW`` → ``LANE_CHANGE_LEFT``: speed below threshold
     AND left lane gap :math:`> d_{\text{safe}}`.

.. dropdown:: Implementation

   .. code-block:: python

      from enum import Enum

      class State(Enum):
          LANE_FOLLOW = 0
          FOLLOW      = 1
          LANE_CHANGE_LEFT  = 2
          LANE_CHANGE_RIGHT = 3
          STOP        = 4
          YIELD       = 5

      class BehaviorPlanner:
          def __init__(self):
              self.state = State.LANE_FOLLOW

          def update(self, ego, predictions, map_info):
              lead = self._find_lead(ego, predictions)
              ttc  = self._time_to_collision(ego, lead)

              if self.state == State.LANE_FOLLOW:
                  if ttc < 3.0:
                      self.state = State.FOLLOW
                  elif map_info.stop_line_ahead and ego.speed > 0.1:
                      self.state = State.STOP

              elif self.state == State.FOLLOW:
                  if ttc > 6.0:
                      self.state = State.LANE_FOLLOW
                  elif self._left_gap_safe(ego, predictions):
                      self.state = State.LANE_CHANGE_LEFT

              # ... additional transitions ...
              return self.state

.. dropdown:: Limitations of FSMs

   FSMs are **brittle** at the boundary conditions between states
   and in novel scenarios not covered by hand-designed transitions.

   - **State explosion:** a complete real-world driving FSM
     requires hundreds of states and thousands of transition
     conditions.
   - **No uncertainty handling:** FSM transitions are crisp;
     they do not naturally incorporate prediction uncertainty.
   - **Manual engineering:** every new scenario requires a
     new transition to be hand-coded and tested.

   These limitations motivate learned decision-making approaches.


Rule-Based vs. Learned Decision-Making
====================================================

.. dropdown:: Rule-Based Systems

   Rule-based behavior planners (including FSMs and decision trees)
   encode expert knowledge as explicit logical conditions.

   **Advantages:**

   - Interpretable: every decision can be traced to a rule.
   - Predictable: behavior is deterministic given the same input.
   - Certifiable: rules can be formally verified for safety.

   **Disadvantages:**

   - Incomplete: rare scenarios not covered by rules cause failures.
   - Brittle: edge cases and ambiguous situations require complex
     rule interactions.
   - High engineering cost: thousands of rules must be maintained.

.. dropdown:: Learned Decision-Making

   Learned approaches replace hand-crafted rules with a policy
   :math:`\pi(a | s)` trained from data.

   **Advantages:**

   - Generalizes to unseen scenarios not covered by rules.
   - Can capture complex multi-agent interactions implicitly.
   - Lower engineering effort once training infrastructure exists.

   **Disadvantages:**

   - Interpretability: the policy is a black box.
   - Safety guarantees are hard to prove formally.
   - Requires large, diverse training data.
   - Distribution shift: policy fails on inputs far from training
     distribution.


Imitation Learning
====================================================

Imitation learning trains a policy to mimic expert (human driver)
behavior from logged demonstrations.

.. dropdown:: Behavior Cloning

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

.. dropdown:: Distribution Shift: The Key Failure Mode

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
====================================================

DAgger (Ross et al., ICML 2011) addresses distribution shift
by iteratively augmenting the training dataset with states
visited by the learned policy.

.. dropdown:: Algorithm

   .. code-block:: text

      Initialize: D = {} (empty dataset), pi_1 = any policy
      For iteration i = 1, 2, ..., N:
          1. Roll out policy pi_i in the environment
             (or simulator) to collect trajectory states {s_t}
          2. Query the expert at each visited state: a*_t = pi*(s_t)
          3. Add {(s_t, a*_t)} to D
          4. Train policy pi_{i+1} on the full aggregated D
      Return: best pi_i on validation

.. dropdown:: Why DAgger Works

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

.. dropdown:: Practical Considerations

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


Practical Decision-Making in Traffic
====================================================

.. dropdown:: Intersection Negotiation

   Intersections require reasoning about right-of-way, crossing
   trajectories, and agent intent simultaneously.

   A behavior planner for intersections must:

   1. **Detect the intersection** and classify the control type
      (traffic signal, stop sign, uncontrolled, roundabout).
   2. **Determine right-of-way** from signal state or traffic rules.
   3. **Predict crossing agents** and compute time-to-conflict (TTC)
      for each crossing trajectory pair.
   4. **Decide:** proceed, yield, or stop based on TTC and
      predicted agent gaps.

   .. admonition:: Gap Acceptance
      :class: note

      The fundamental decision at an uncontrolled intersection is
      **gap acceptance**: is the time gap in the crossing stream
      large enough to enter safely? Gap acceptance models learned
      from human data outperform fixed-threshold rules because
      they incorporate speed, visibility, and vehicle type.

.. dropdown:: Merging onto a Highway

   Merging requires the ego vehicle to find a gap in the highway
   traffic stream and adjust speed to reach the merge point
   simultaneously with the gap.

   Key considerations:

   - Predict lead and following highway vehicles for 8--10 s.
   - Compute the gap size at the merge point as a function of
     ego speed.
   - Select the target gap and compute the acceleration profile
     (quintic polynomial) to arrive at the merge point
     within the gap.
   - Monitor the gap in real time; abort and re-plan if the
     gap closes.

.. dropdown:: Pedestrian Interactions

   Pedestrians are the most challenging agents for prediction
   because:

   - They can change direction instantly (no kinematic constraints).
   - Their intent is often unobservable (phone in hand, not looking).
   - Social norms (yielding, eye contact) are implicit.

   Best practices:

   - Use multi-modal prediction with high-uncertainty modes.
   - Apply conservative safety margins (1.5--2.0 m clearance).
   - Prefer slow-speed trajectories when pedestrian uncertainty
     is high (reduces collision energy).
   - Never assume a pedestrian will stop or yield.


CARLA Exercise
====================================================

.. admonition:: Exercise: Trajectory Prediction and Behavioral Planner
   :class: note

   **Goal:** Integrate a simple prediction module and FSM behavior
   planner into a CARLA agent that navigates a multi-lane road
   with traffic.

   **Tasks:**

   1. **Perception:** Use CARLA's ground-truth bounding boxes to
      obtain the positions, velocities, and headings of all
      nearby vehicles within 50 m.

   2. **Constant-velocity prediction:** For each nearby vehicle,
      predict its trajectory over 5 s at 0.1 s intervals using
      the CV model. Visualize predicted positions with
      ``world.debug.draw_point()``.

   3. **FSM behavior planner:** Implement a four-state FSM
      (``LANE_FOLLOW``, ``FOLLOW``, ``LANE_CHANGE_LEFT``,
      ``STOP``) with transitions based on:

      - TTC to lead vehicle (< 3 s → ``FOLLOW``)
      - Speed below reference (→ attempt ``LANE_CHANGE_LEFT``)
      - Stop sign detected ahead (→ ``STOP``)

   4. **Integration:** Connect the FSM output to the Stanley
      lateral controller and PID longitudinal controller from L9.
      Run the agent on a multi-vehicle Town04 scenario for 120 s.

   5. **Evaluation:** Log the FSM state sequence, speed profile,
      and collision events. Report: time in each state, max speed
      deviation, number of hard braking events (deceleration
      > 4 m/s²).

   **Starter code:**

   .. code-block:: python

      import carla
      import numpy as np

      def cv_predict(vehicle, horizon=5.0, dt=0.1):
          """Constant-velocity trajectory prediction."""
          t = vehicle.get_transform()
          v = vehicle.get_velocity()
          vx, vy = v.x, v.y
          x0, y0 = t.location.x, t.location.y
          steps = int(horizon / dt)
          trajectory = []
          for i in range(steps):
              t_i = (i + 1) * dt
              trajectory.append(
                  carla.Location(x=x0 + vx * t_i,
                                 y=y0 + vy * t_i,
                                 z=t.location.z))
          return trajectory

      def time_to_collision(ego, lead, predictions):
          """Estimate TTC using predicted lead position."""
          ego_loc = ego.get_transform().location
          lead_traj = predictions[lead.id]
          ego_v = ego.get_velocity()
          ego_speed = (ego_v.x**2 + ego_v.y**2)**0.5
          for i, loc in enumerate(lead_traj):
              dist = ego_loc.distance(loc)
              if dist < 3.0:  # collision threshold (m)
                  return (i + 1) * 0.1  # time in seconds
          return float('inf')
