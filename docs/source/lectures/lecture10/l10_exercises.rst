====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 10. Exercises cover trajectory generation, lateral and
longitudinal controllers, and MPC concepts.


.. dropdown:: Exercise 1 -- Quintic Polynomial Trajectory
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Generate a smooth trajectory using quintic polynomials and verify
   that it satisfies comfort constraints.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``quintic_trajectory.py`` that performs the
   following:

   Generate a quintic polynomial
   :math:`s(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5`
   satisfying:

   - :math:`s(0) = 0,\; \dot{s}(0) = 10,\; \ddot{s}(0) = 0`
   - :math:`s(3) = 40,\; \dot{s}(3) = 15,\; \ddot{s}(3) = 0`

   1. Set up the **6 × 6 linear system** and solve for
      :math:`a_0 \ldots a_5` using ``numpy.linalg.solve``.
   2. Plot :math:`s(t)`, :math:`\dot{s}(t)` (velocity), and
      :math:`\ddot{s}(t)` (acceleration) over :math:`t \in [0, 3]` s
      in a 3-subplot figure.
   3. Print the **maximum acceleration** along the trajectory.
   4. If the comfort limit is :math:`|\ddot{s}| \leq 3` m/s², does
      this trajectory satisfy it?

   **Deliverable**

   The script, 3-subplot figure, and written answer about comfort.


.. dropdown:: Exercise 2 -- Pure Pursuit Controller
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Implement Pure Pursuit and observe how the lookahead distance
   affects convergence to a reference path.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``pure_pursuit.py`` that performs the following:

   A vehicle starts at :math:`(x, y) = (0, 1)` with heading
   :math:`\theta = 0`. The reference path is the x-axis
   (:math:`y = 0`). Wheelbase :math:`L = 2.9` m.

   1. With lookahead :math:`L_d = 5` m, find the **lookahead point**
      on the path.
   2. Compute the **curvature**
      :math:`\kappa = 2 \sin(\alpha) / L_d` where :math:`\alpha` is
      the angle from the vehicle heading to the lookahead point.
   3. Compute the **steering angle**
      :math:`\delta = \arctan(\kappa \cdot L)`.
   4. Simulate the vehicle for **10 seconds** at :math:`v = 10` m/s,
      :math:`\Delta t = 0.05` s, with Pure Pursuit updating at each
      step. **Plot the trajectory** showing convergence to the path.
   5. Repeat with :math:`L_d = 10` m and :math:`L_d = 2` m. Plot all
      three on the same figure.

   **Written analysis**

   How does the lookahead distance affect convergence speed and
   oscillation? What is the trade-off?

   **Deliverable**

   The script, trajectory plot, and written analysis (3--5 sentences).


.. dropdown:: Exercise 3 -- Stanley vs. Pure Pursuit
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compare Stanley and Pure Pursuit controllers on a curved path and
   identify which has lower steady-state error.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``controller_comparison.py`` that performs the
   following:

   1. Define a **circular arc** reference path with radius 20 m
      (generate waypoints every 0.5 m over 180°).
   2. Implement the **Stanley controller**:

      .. math::

         \delta = \psi_e + \arctan\!\left(\frac{k \cdot e}{v}\right)

      with :math:`k = 0.5`, :math:`v = 10` m/s.

   3. Implement **Pure Pursuit** with :math:`L_d = k_{pp} \cdot v`,
      :math:`k_{pp} = 0.5`.
   4. Simulate both controllers for **10 seconds** on the arc.
   5. Plot on two subplots:

      - **Cross-track error** over time (both controllers).
      - **Steering angle** over time (both controllers).

   **Written analysis**

   Which controller has lower steady-state error on curves? Why?

   **Deliverable**

   The script, comparison plots, and written analysis.


.. dropdown:: Exercise 4 -- PID Tuning and Anti-Windup
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Implement a PID longitudinal controller, observe integral windup,
   and implement a clamping fix.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``pid_controller.py`` that implements a PID speed
   controller:

   .. math::

      u(t) = K_p \, e(t) + K_i \textstyle\int_0^t e(\tau)\,d\tau
             + K_d \, \dot{e}(t)

   where :math:`e(t) = v_{\text{ref}} - v(t)`.

   Use a simple 1D vehicle model:
   :math:`v(t + \Delta t) = v(t) + u(t) \cdot \Delta t` (clamped to
   :math:`[0, 50]` km/h).

   1. Set :math:`K_p = 1.0,\; K_i = 0,\; K_d = 0`. Reference speed =
      30 km/h. Simulate 10 s. **Plot speed vs. time**.
   2. Add :math:`K_i = 0.1`. What changes?
   3. Add :math:`K_d = 0.5`. What changes?
   4. **Demonstrate windup**: set reference to 30 km/h for 5 s, then
      drop to 10 km/h. Show the overshoot caused by accumulated
      integral.
   5. Implement **anti-windup clamping** (limit integral term to
      :math:`\pm 1.0`) and repeat step 4. Show the improvement.

   All five experiments should be plotted in a single 5-subplot figure.

   **Deliverable**

   The script and 5-subplot figure.


.. dropdown:: Exercise 5 -- MPC Conceptual Analysis
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Understand MPC design choices by reasoning about horizon length,
   cost weights, and real-time constraints.


   .. raw:: html

      <hr>


   **Specification**

   A linear MPC for lateral control uses:

   - State: :math:`\mathbf{x} = [e, \dot{e}, \psi_e, \dot{\psi}_e]^T`
   - Control: :math:`u = \delta` (steering angle)
   - Horizon: :math:`N = 10`, :math:`\Delta t = 0.1` s

   Answer the following:

   1. What is the **prediction horizon** in seconds?
   2. The cost is
      :math:`J = \sum_{k=0}^{N} \mathbf{x}_k^T Q\,\mathbf{x}_k + \sum_{k=0}^{N-1} u_k^T R\,u_k`
      with :math:`Q = \text{diag}(10, 1, 10, 1)` and :math:`R = [1]`.
      Which state components are penalized most heavily?
   3. If :math:`R` is increased to ``[100]``, what happens to steering
      behavior (smoother or more aggressive)?
   4. What is the advantage of MPC over Pure Pursuit for **obstacle
      avoidance**?
   5. A nonlinear MPC solver takes 25 ms per solve. At a 50 Hz control
      rate, is this fast enough? What are two strategies to speed it
      up?

   **Deliverable**

   Written answers (2--4 sentences per question).
