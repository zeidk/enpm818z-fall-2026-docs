====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 6: Multi-Sensor Fusion.
Topics include the motivation for sensor fusion, fusion architectures
(early, intermediate, late), Kalman filter predict/update equations, Kalman
gain, EKF, UKF, particle filter, filter comparison, data association,
inverse-variance weighting, and cross-attention deep learning fusion.

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

   A camera detects traffic light color while LiDAR measures precise distance
   to the traffic light pole. This sensor combination exemplifies which type
   of sensor relationship?

   A. Competitive (redundant)

   B. Cooperative

   C. Complementary

   D. Adversarial

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Complementary

   Complementary sensors measure different physical phenomena, and their
   combination provides information that neither can provide alone. Here,
   the camera provides color/semantic information (which light is active)
   while LiDAR provides precise range -- a combination that enables both
   detection and accurate localization of the traffic light.


.. admonition:: Question 2
   :class: hint

   Which fusion architecture processes sensor data from each modality
   independently through its own feature extractor and then combines the
   extracted features in a shared representation space?

   A. Early fusion (raw data level)

   B. Intermediate fusion (feature-level)

   C. Late fusion (decision level)

   D. Cascade fusion

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Intermediate fusion (feature-level)

   In intermediate (feature-level) fusion, each sensor modality processes
   its raw data through its own backbone network to extract features. The
   extracted features are then fused in a shared space (e.g., a BEV grid
   where both camera and LiDAR BEV features are concatenated or combined
   via attention). This balances information richness with computational
   efficiency.


.. admonition:: Question 3
   :class: hint

   In the Kalman Filter **predict** step, what happens to the uncertainty
   (covariance matrix P) when no new measurement is received?

   A. P decreases because the filter becomes more confident about the state.

   B. P stays constant because no new information has been added.

   C. P increases because the process noise (Q) is added, reflecting growing
      uncertainty about the state over time.

   D. P is reset to zero because the previous estimate is discarded.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- P increases because the process noise (Q) is added, reflecting
   growing uncertainty about the state over time.

   The predict step propagates uncertainty: :math:`P_{k|k-1} = F P_{k-1} F^T + Q`.
   The process noise covariance Q is always added, representing uncertainty
   from unmodeled dynamics, actuator noise, and disturbances. Without
   measurements, the filter's state estimate becomes progressively less
   certain.


.. admonition:: Question 4
   :class: hint

   The **Kalman Gain** :math:`K_k` approaches zero when:

   A. The measurement noise covariance R is very small (accurate sensor).

   B. The prior covariance P is very large (uncertain prediction).

   C. The measurement noise covariance R is very large (noisy sensor) OR the
      prior covariance P is very small (confident prediction).

   D. The state transition matrix F is the identity matrix.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The measurement noise covariance R is very large (noisy sensor)
   OR the prior covariance P is very small (confident prediction).

   K ≈ P / (P + R). When R >> P, K → 0: the measurement is too noisy to
   be useful, so the filter trusts the prediction. When P << R, K → 0 for
   the same reason: the prediction is already very accurate. Conversely,
   when R << P (accurate sensor, uncertain prediction), K is large and the
   update aggressively corrects the prediction.


.. admonition:: Question 5
   :class: hint

   What is the key innovation of the **Extended Kalman Filter (EKF)** compared
   to the standard Kalman Filter?

   A. It uses sigma points to propagate uncertainty through nonlinear functions.

   B. It represents the posterior as a set of weighted particles.

   C. It linearizes nonlinear process and measurement functions using their
      Jacobian matrices at the current state estimate.

   D. It eliminates the need for a process model by using only measurements.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It linearizes nonlinear process and measurement functions using
   their Jacobian matrices at the current state estimate.

   The EKF replaces F and H in the standard KF with the Jacobians
   ∂f/∂x and ∂h/∂x evaluated at the current estimate. The state
   propagation itself uses the full nonlinear function f(x), but the
   covariance propagation uses the linearized Jacobian. This is the
   first-order approximation to the true nonlinear transform.


.. admonition:: Question 6
   :class: hint

   The **Unscented Kalman Filter (UKF)** propagates uncertainty through
   nonlinear functions by:

   A. Computing the Jacobian and applying first-order Taylor expansion.

   B. Drawing random Monte Carlo samples from the prior distribution.

   C. Selecting 2n+1 deterministic sigma points that capture the prior mean
      and covariance, propagating them through the nonlinear function, and
      computing the posterior as a weighted mean of the results.

   D. Using a lookup table of precomputed linearizations.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Selecting 2n+1 deterministic sigma points that capture the prior
   mean and covariance, propagating them through the nonlinear function, and
   computing the posterior as a weighted mean of the results.

   The UKF uses the "unscented transform" to exactly compute the mean and
   covariance of a nonlinear function applied to a Gaussian distribution,
   accurate to second-order. Unlike the EKF, no Jacobian is required -- only
   function evaluations at the sigma points.


.. admonition:: Question 7
   :class: hint

   A **Particle Filter** is most appropriate when:

   A. The system has linear dynamics and Gaussian noise.

   B. The posterior distribution is multi-modal (e.g., multiple possible
      positions) and/or the noise is non-Gaussian.

   C. Low compute budget requires a fast, closed-form filter.

   D. The state dimension is very high (hundreds of variables).

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The posterior distribution is multi-modal (e.g., multiple possible
   positions) and/or the noise is non-Gaussian.

   Particle filters approximate the posterior as a weighted set of samples,
   which can represent any distribution including multi-modal ones. Classic
   use case: robot localization when the robot is initially uncertain about
   which room it is in -- the particle filter maintains hypotheses across
   multiple rooms until sensor evidence resolves the ambiguity.


.. admonition:: Question 8
   :class: hint

   In the **data association problem**, the **Mahalanobis distance** is
   preferred over Euclidean distance because it:

   A. Is faster to compute than Euclidean distance.

   B. Accounts for the uncertainty (covariance) of the predicted track
      position, so that a measurement far in a poorly-constrained direction
      is not over-penalized.

   C. Is always smaller than the Euclidean distance.

   D. Does not require knowledge of the measurement noise covariance R.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Accounts for the uncertainty (covariance) of the predicted track
   position, so that a measurement far in a poorly-constrained direction
   is not over-penalized.

   Mahalanobis distance: d_M = sqrt((z - z_pred)^T S^-1 (z - z_pred))
   where S is the innovation covariance (= HPH^T + R). It scales the
   distance by the inverse of the prediction uncertainty -- a measurement
   that is 3 m away in a direction where the prediction variance is 9 m^2
   is treated very differently from one that is 3 m away in a direction
   with variance 0.01 m^2.


.. admonition:: Question 9
   :class: hint

   Two independent range sensors measure the distance to an obstacle:
   Sensor A gives 10.0 m with variance 0.25 m², Sensor B gives 10.4 m with
   variance 1.0 m². What is the **inverse-variance weighted** fused estimate?

   A. 10.20 m (simple average)

   B. 10.10 m

   C. 10.32 m

   D. 10.08 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- 10.10 m

   Weights: w_A = 1/0.25 = 4, w_B = 1/1.0 = 1.
   Fused = (4 * 10.0 + 1 * 10.4) / (4 + 1) = (40.0 + 10.4) / 5 = 50.4 / 5
   = **10.08 m** (closest to B among given choices; exact answer 10.08 m).

   Note: The exact answer is 10.08 m. The fused estimate is pulled strongly
   toward Sensor A (lower variance = higher weight = 80% contribution).


.. admonition:: Question 10
   :class: hint

   In **BEVFusion**'s cross-attention fusion, what role do the LiDAR BEV
   features play in the attention mechanism?

   A. They serve as Values (V) -- providing the content that is read out.

   B. They serve as Queries (Q) -- asking "what camera features are relevant
      to this spatial location?"

   C. They serve as Keys (K) -- indexing which camera features to attend to.

   D. They are not used in the attention; only camera features are fused.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- They serve as Queries (Q) -- asking "what camera features are
   relevant to this spatial location?"

   In cross-attention fusion: LiDAR BEV features → Q (queries); Camera BEV
   features → K (keys) and V (values). The LiDAR features "query" the
   camera features: for each LiDAR BEV cell (which knows geometry), the
   attention mechanism selectively retrieves relevant semantic information
   from the camera BEV. This is directional fusion where geometry guides
   semantic information retrieval.


----


True or False (Questions 11-15)
================================

.. admonition:: Question 11
   :class: hint

   **True or False:** RADAR is robust to rain and fog conditions that
   significantly degrade camera and LiDAR performance, making it an
   essential complementary sensor for adverse weather driving.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   RADAR operates at millimeter wavelengths (~77 GHz) that pass through rain,
   fog, and snow with minimal attenuation. Camera performance degrades sharply
   in heavy rain (water droplets on lens, reduced visibility) and LiDAR
   degrades due to laser backscatter from water droplets. RADAR also provides
   direct Doppler velocity measurements unavailable from LiDAR or cameras.


.. admonition:: Question 12
   :class: hint

   **True or False:** The Extended Kalman Filter (EKF) provides an exact
   (optimal) solution for nonlinear state estimation under Gaussian noise.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The EKF is only a first-order approximation. It linearizes the nonlinear
   functions at the current state estimate via Jacobians, which introduces
   linearization error. For highly nonlinear functions or far from the
   operating point, this approximation can be poor, causing the EKF to be
   overconfident (underestimate covariance) or even diverge. The Unscented
   KF provides a second-order accurate approximation without linearization.


.. admonition:: Question 13
   :class: hint

   **True or False:** A Particle Filter with a very small number of particles
   (e.g., N=10) will always converge to the true state given enough time.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   With too few particles, particle filters suffer from "particle collapse"
   (degeneracy) -- over time, after repeated resampling, all weight
   concentrates on just one or a few particles, losing diversity. The filter
   then cannot recover if the true state is far from that particle's location.
   Practical particle filters for AV localization (like Monte Carlo
   Localization / AMCL) typically use 1,000-10,000+ particles for reliability.


.. admonition:: Question 14
   :class: hint

   **True or False:** In late (decision-level) fusion, if the camera detector
   misses an object but the LiDAR detector correctly detects it, the fused
   output will still include that object.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Late fusion combines independent detection outputs from each sensor.
   If LiDAR detects an object with sufficient confidence, it will appear
   in the LiDAR detection list. The late fusion module (e.g., via NMS or
   track-level fusion) will include it even if the camera missed it. This
   is one of the key reliability benefits of multi-sensor fusion.


.. admonition:: Question 15
   :class: hint

   **True or False:** In the Kalman Filter update step, the posterior
   covariance P_{k|k} is always smaller than or equal to the prior
   covariance P_{k|k-1}.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The update equation P_{k|k} = (I - K H) P_{k|k-1} always reduces
   uncertainty. The measurement provides new information, and the Kalman
   filter is the optimal linear estimator that minimally reduces uncertainty
   consistent with that information. Mathematically, K is chosen to minimize
   the trace of P_{k|k}, guaranteeing it is less than or equal to P_{k|k-1}.


----


Essay Questions (Questions 16-18)
===================================

.. admonition:: Question 16
   :class: hint

   **Describe the Kalman Filter predict and update cycle** using an example
   from autonomous driving (e.g., tracking a vehicle). Explain what the
   Kalman Gain represents and how its value changes based on sensor noise
   vs. prediction uncertainty.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Example: tracking a vehicle's position and velocity. State x = [px, py,
     vx, vy]. Predict step: use constant-velocity model to propagate x and
     increase P (uncertainty grows). Update step: receive a LiDAR measurement
     z = [px_lidar, py_lidar] and correct the estimate.
   - Innovation = z - H*x_pred: the discrepancy between predicted and actual
     measurement. The posterior estimate = prior + K * innovation.
   - Kalman Gain K = P_prior * H^T * (H*P_prior*H^T + R)^-1. When R is small
     (accurate LiDAR), K is large and the correction is aggressive. When R
     is large (noisy sensor) or P_prior is small (confident prediction), K
     is small and the prediction changes little.
   - Physical interpretation: K is a "trust dial" between prediction and
     measurement. At startup (high P), trust the measurement heavily. After
     converging (low P), trust the model more.


.. admonition:: Question 17
   :class: hint

   **Compare the EKF and UKF** for tracking a vehicle with nonlinear motion
   (e.g., turning with constant angular rate -- the CTRV model). When would
   you prefer the UKF over the EKF?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The CTRV (Constant Turn Rate and Velocity) model has process function
     f(x) involving sin/cos of the heading angle -- a nonlinear function.
     EKF computes the Jacobian of f(x), which involves partial derivatives
     of sin(psi) -- analytically complex and prone to numerical errors.
   - UKF selects 2n+1 sigma points around the current state, propagates
     each through f(x) directly (evaluating sin/cos at specific angles), and
     recovers the posterior mean and covariance. No Jacobian required.
   - Prefer UKF when: (1) the Jacobian is difficult to derive analytically
     (complex models), (2) the motion is highly nonlinear (sharp turns,
     large timesteps), (3) higher accuracy is needed (UKF is second-order
     accurate vs. EKF's first-order). EKF may be preferred when compute
     budget is very tight and the model is mildly nonlinear.
   - In practice, UKF is the standard for IMU + GPS fusion in AV systems
     (PointOne Nav, SBG Systems) due to its superior accuracy in nonlinear
     attitude estimation.


.. admonition:: Question 18
   :class: hint

   **Explain the data association problem** in multi-sensor, multi-object
   tracking. Describe two approaches to solving it and the trade-offs of each.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The data association problem: given a set of measurements z_1,...,z_m
     and a set of tracks T_1,...,T_n at each timestep, determine which
     measurement was produced by which track (or background clutter).
     Incorrect association causes Kalman filter divergence and track confusion.
   - Approach 1 -- Global Nearest Neighbor (GNN) / Hungarian algorithm:
     compute a cost matrix (e.g., Mahalanobis distance for each
     measurement-track pair), solve for optimal global assignment. Pros:
     optimal for a single timestep, O(n^3) compute. Cons: makes hard
     assignments that cannot be undone; fails in high clutter.
   - Approach 2 -- Joint Probabilistic Data Association (JPDA): instead of
     hard assignment, computes probabilities over all possible assignments
     and updates each track as a weighted mixture. Pros: robust in cluttered
     environments (multiple nearby objects). Cons: higher compute, tracks
     can "merge" in high-density scenes.
   - For AV systems at moderate object densities: GNN (via Hungarian) is
     standard. JPDA is used when clutter is high (dense urban intersections,
     parking lots with many closely-spaced vehicles).
