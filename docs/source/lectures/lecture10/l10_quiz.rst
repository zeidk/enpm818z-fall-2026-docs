====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 9: Trajectory
Planning & Control, including path vs. trajectory, quintic
polynomial and spline methods, optimization-based trajectory
planning, MPC formulation and receding-horizon control, Pure
Pursuit, Stanley, and PID controllers, and emergency maneuver
synthesis.

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

   What is the minimum polynomial degree required to match position,
   velocity, **and** acceleration at both the start and end of a
   trajectory segment?

   A. 3rd degree (cubic)

   B. 4th degree (quartic)

   C. 5th degree (quintic)

   D. 6th degree (sextic)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- 5th degree (quintic).

   A degree-:math:`n` polynomial has :math:`n+1` coefficients.
   Matching position, velocity, and acceleration at two endpoints
   gives 6 constraints. The minimum degree satisfying 6 constraints
   is :math:`n = 5` (quintic), yielding exactly 6 coefficients.
   Cubic polynomials (4 coefficients) can match only position and
   velocity at both ends; quartics (5 coefficients) are
   over-constrained by the 6 boundary conditions.


.. admonition:: Question 2
   :class: hint

   In MPC, the **receding horizon** principle means that:

   A. The prediction horizon :math:`N` shrinks as the vehicle
      approaches the goal.

   B. Only the first control action from the optimized sequence is
      applied; the optimization is then re-solved at the next
      time step.

   C. The vehicle predicts the future states of surrounding agents
      over horizon :math:`N`.

   D. The cost function is evaluated backwards from the terminal
      state to the current state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Only the first control action is applied; the
   optimization is re-solved at the next time step.

   The receding horizon principle is what makes MPC a *feedback*
   controller rather than an open-loop trajectory tracker. By
   re-solving at every time step with the current measured state,
   MPC corrects for disturbances, model errors, and state
   estimation noise. The horizon "recedes" because the planning
   window always starts from the current time.


.. admonition:: Question 3
   :class: hint

   In the Pure Pursuit controller, if the lookahead distance
   :math:`L_d` is doubled while speed remains constant, the
   steering response becomes:

   A. More aggressive (tighter turns)

   B. Less aggressive (smoother, cutting corners more)

   C. Identical, because only :math:`\alpha` determines steering

   D. Unstable, because the lookahead point leaves the path

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Less aggressive (smoother, cutting corners more).

   From the steering equation
   :math:`\delta = \arctan(2L\sin\alpha / L_d)`, increasing
   :math:`L_d` (denominator) reduces :math:`\delta` for the same
   angular error :math:`\alpha`. A larger lookahead point is
   further ahead on the path, requiring less steering to reach it.
   The result is smoother tracking but larger corner-cutting at
   high curvature.


.. admonition:: Question 4
   :class: hint

   The Stanley controller steering command
   :math:`\delta = \psi_e + \arctan(ke/v)` divides the cross-track
   correction by speed :math:`v` because:

   A. The steering actuator has a velocity-dependent deadband.

   B. At higher speeds, the same steering angle produces a larger
      lateral displacement per unit time, so less correction is
      needed to achieve the same path convergence rate.

   C. The cross-track error :math:`e` grows proportionally to
      speed.

   D. The heading error :math:`\psi_e` is inversely proportional
      to speed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- At higher speeds, the same steering angle produces
   larger lateral displacement per unit time, requiring less
   proportional correction.

   The :math:`1/v` factor normalizes the cross-track correction
   by time-to-travel: at high speed the vehicle is moving
   quickly toward the path anyway, so a smaller steering angle
   suffices. Without this factor, the controller would oversteer
   at high speed and understeer at low speed.


.. admonition:: Question 5
   :class: hint

   Integrator windup in a PID speed controller occurs when:

   A. The derivative term grows too large due to measurement noise.

   B. The integral accumulates error during actuator saturation,
      causing large overshoot when the saturation constraint
      is released.

   C. The proportional gain is set too high, causing the system
      to become underdamped.

   D. The reference speed changes faster than the vehicle can
      accelerate.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The integral accumulates error during actuator
   saturation.

   When the throttle or brake is saturated (clamped at its
   physical limit), the PID output is clipped but the integrator
   continues to add the current error at every time step. When
   the constraint is eventually released (e.g., vehicle reaches
   the speed range), the large accumulated integral causes the
   output to shoot far beyond the target. Anti-windup strategies
   prevent accumulation during saturation.


.. admonition:: Question 6
   :class: hint

   A natural cubic spline minimizes which quantity over the
   interpolated curve?

   A. Maximum curvature along the curve

   B. Total arc length

   C. Integral of the squared second derivative (bending energy)

   D. Sum of squared interpolation errors at the waypoints

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Integral of the squared second derivative (bending
   energy).

   The natural cubic spline is the unique minimum-bending-energy
   interpolant through the given waypoints:

   .. math::

      \min \int_{t_0}^{t_n} \left[S''(t)\right]^2 dt

   This is why cubic splines produce visually smooth curves --
   they distribute curvature as evenly as possible. This property
   also relates to the physical deflection of a thin elastic beam
   (a "spline" in the engineering sense).


.. admonition:: Question 7
   :class: hint

   In linear MPC for vehicle trajectory tracking, the bicycle
   model is **linearized** around the reference trajectory because:

   A. The full nonlinear model cannot represent vehicle dynamics.

   B. Linearization converts the nonlinear optimization problem
      into a quadratic program (QP), which can be solved in
      milliseconds at real-time rates.

   C. The bicycle model is already linear; no approximation is
      needed.

   D. Linearization eliminates the need for a prediction horizon.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Linearization converts the NLP to a QP solvable in
   milliseconds.

   The bicycle model is nonlinear (trigonometric functions of
   heading). Linearizing around the reference trajectory yields
   linear state equations, and if the cost is quadratic the
   resulting optimization is a QP. QPs have polynomial-time
   algorithms (active-set, interior-point) and can be solved
   in under 1 ms with code-generated solvers, enabling
   real-time MPC at 50 Hz.


.. admonition:: Question 8
   :class: hint

   A B-spline trajectory has the **local support** property,
   meaning:

   A. The curve passes through all control points.

   B. Moving one control point affects only a local portion
      of the curve (at most :math:`k+1` spans for degree
      :math:`k`).

   C. The curve is supported (lies above) the convex hull of
      the control points.

   D. The spline can only be evaluated at the knot locations.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Moving one control point affects only the local
   portion of the curve (at most :math:`k+1` spans).

   Local support is a key advantage of B-splines over global
   polynomials. It means that local adjustments to the trajectory
   (e.g., routing around a newly detected obstacle) require
   modifying only a few control points, and the change affects
   only the nearby portion of the path. This is critical for
   efficient online trajectory editing.


.. admonition:: Question 9
   :class: hint

   In Frenet-frame trajectory planning, generating multiple
   candidate quintic polynomials by varying the terminal lateral
   offset :math:`d_f` serves what purpose?

   A. It guarantees that at least one candidate is kinematically
      feasible.

   B. It produces a discrete set of trajectory options that can
      be evaluated for cost and safety, with the best feasible
      candidate selected.

   C. It reduces the computation time by parallelizing the
      coefficient calculation.

   D. It ensures the trajectory converges to the road centerline
      within one planning step.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It produces a discrete set of options evaluated for
   cost and safety.

   By sampling a grid of terminal conditions
   :math:`(d_f, \dot{d}_f, T)`, the planner generates many
   candidate trajectories covering different lateral positions
   and durations. Each is evaluated for collision clearance and
   cost. The lowest-cost collision-free candidate is selected.
   This sampling-then-scoring approach is efficient and handles
   multi-modal situations (e.g., passing on either side of
   an obstacle).


.. admonition:: Question 10
   :class: hint

   Emergency braking distance at :math:`v_0 = 20` m/s with maximum
   deceleration :math:`a_{\max} = 6` m/s² is:

   A. 20 m

   B. 33.3 m

   C. 60 m

   D. 66.7 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Approximately 33.3 m.

   .. math::

      d_{\text{stop}} = \frac{v_0^2}{2 a_{\max}}
      = \frac{20^2}{2 \times 6} = \frac{400}{12} \approx 33.3 \text{ m}

   At 72 km/h, an autonomous vehicle must begin emergency braking
   at least 33 m before an obstacle (plus any perception and
   actuation latency). Typical system latency of 100--200 ms adds
   2--4 m to the required detection range.


----


True / False
============

.. admonition:: Question 11
   :class: hint

   **True or False:** A path and a trajectory contain the same
   information; the terms can be used interchangeably in motion
   planning.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   A path specifies only the geometric shape of the route (as a
   function of arc length or an arbitrary parameter). A trajectory
   adds a time parameterization: it specifies where the vehicle is
   at every point in time, implicitly defining velocity and
   acceleration profiles. Controllers that handle speed regulation
   (throttle, brake) require a trajectory, not just a path.


.. admonition:: Question 12
   :class: hint

   **True or False:** The Stanley controller produces a non-zero
   steady-state lateral error on a straight road at constant speed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   On a straight road at constant speed with zero initial
   cross-track error, the Stanley controller produces zero
   steady-state lateral error. The heading-error term
   :math:`\psi_e` drives the vehicle parallel to the path,
   and the :math:`\arctan(ke/v)` term drives cross-track error
   :math:`e` to zero. Unlike Pure Pursuit, Stanley has no
   geometry-induced steady-state error on straight or
   gently curved roads.


.. admonition:: Question 13
   :class: hint

   **True or False:** In MPC, increasing the prediction horizon
   :math:`N` always improves closed-loop performance.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Increasing :math:`N` provides better foresight (the optimizer
   can plan further ahead, avoiding locally greedy actions), but
   it also increases the size of the QP or NLP, requiring more
   computation time per solve. If the solve time exceeds the
   control period, the controller misses its real-time deadline
   and performance degrades. There is an optimal :math:`N` that
   balances foresight and computational feasibility.


.. admonition:: Question 14
   :class: hint

   **True or False:** The convex hull property of B-splines
   guarantees that the trajectory lies within the convex hull of
   its control points, which is useful for conservative collision
   checking.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The B-spline convex hull property states that every point on
   the curve lies within the convex hull of its local control
   points. For collision checking, this means: if the convex hull
   of the control polygon is collision-free, the curve itself is
   guaranteed to be collision-free -- a fast and conservative
   check without evaluating the curve densely.


.. admonition:: Question 15
   :class: hint

   **True or False:** The Ziegler-Nichols tuning method for PID
   controllers produces gains that are optimal in the
   :math:`H_\infty` sense.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Ziegler-Nichols is a heuristic tuning method based on
   observing the system's response at the stability boundary
   (ultimate gain and period). It provides a practical starting
   point for tuning but does not produce :math:`H_\infty`-optimal
   or even :math:`H_2`-optimal gains. The resulting controller
   typically has approximately 25% overshoot and adequate
   disturbance rejection, which is acceptable for many applications
   but suboptimal for comfort-critical AV control.


----


Essay Questions
===============

.. admonition:: Question 16
   :class: hint

   **Compare Model Predictive Control with the Stanley controller
   for autonomous vehicle lateral control.** What are the
   key advantages of MPC over Stanley, and in what scenarios
   would Stanley be preferred?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - MPC optimizes a multi-step cost function that incorporates
     future predictions, allowing it to anticipate upcoming curves
     and constraints, respect actuator limits explicitly, and
     trade off multiple objectives (comfort, tracking, safety)
     simultaneously.
   - Stanley is a reactive, single-step controller: it responds
     to current cross-track and heading error without planning
     ahead. This makes it simpler but unable to proactively
     adjust for upcoming trajectory features.
   - MPC advantages: constraint handling (curvature limits,
     speed bounds), look-ahead, comfort optimization, and the
     ability to incorporate obstacle avoidance directly.
   - Stanley is preferred in resource-constrained systems
     (embedded microcontrollers), low-speed applications, or
     as a baseline where MPC's computational cost is unjustified.
     Stanley's O(1) compute cost makes it deterministic and
     latency-free.


.. admonition:: Question 17
   :class: hint

   **Explain why quintic polynomials are preferred over cubic
   polynomials for trajectory segment generation.** What
   additional property does the quintic provide, and why does it
   matter for passenger comfort?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A cubic polynomial has 4 coefficients, which can be uniquely
     determined by 4 boundary conditions: position and velocity at
     both endpoints. It cannot simultaneously match acceleration at
     both endpoints.
   - A quintic polynomial has 6 coefficients, allowing it to match
     position, velocity, **and** acceleration at both endpoints.
     This ensures :math:`C^2` continuity across trajectory
     segments.
   - Continuity of acceleration means there are no impulsive
     changes in acceleration when the vehicle transitions between
     trajectory segments. Without this, passengers experience a
     jerk spike at every segment boundary.
   - Jerk (rate of change of acceleration) is the primary
     perceptual discomfort metric; bounding it through :math:`C^2`
     continuity is essential for a smooth passenger experience.


.. admonition:: Question 18
   :class: hint

   **Describe the Frenet-frame approach to trajectory planning.**
   Why is the Frenet frame more convenient than Cartesian
   coordinates for road-following trajectories, and how is a
   Frenet trajectory converted back to a Cartesian plan for
   execution?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The Frenet frame decomposes vehicle motion into longitudinal
     (:math:`s`, along the road centerline) and lateral
     (:math:`d`, perpendicular to it) components. This decouples
     the planning problem: longitudinal and lateral trajectories
     can be planned independently as 1-D polynomial problems.
   - In Cartesian coordinates, a lane-following trajectory on a
     curved road is a complex 2-D curve; in Frenet coordinates,
     it is simply :math:`d(t) \approx 0` -- a nearly trivial
     1-D problem.
   - Conversion back to Cartesian: for each time sample, evaluate
     :math:`s(t)` and :math:`d(t)`, look up the Cartesian position
     of the road centerline at arc length :math:`s(t)`, and offset
     perpendicular to the centerline by :math:`d(t)`.
   - The Frenet frame is only valid where the road centerline
     curvature is non-singular. At very sharp turns or
     intersections, the frame may become ill-conditioned and
     Cartesian planning must be used instead.
