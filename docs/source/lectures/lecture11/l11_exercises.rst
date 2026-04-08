====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 11. Exercises cover trajectory prediction, behavior
planning, and imitation learning.


.. dropdown:: Exercise 1 -- Constant Velocity Prediction
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Implement the constant velocity (CV) prediction model and
   understand its limitations for turning vehicles.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``cv_prediction.py`` that performs the following:

   A vehicle is observed at position :math:`(20, 10)` m with velocity
   :math:`(12, 3)` m/s.

   1. Using the **CV model**, predict positions at
      :math:`t = 1, 2, 3, 4, 5` s.
   2. Plot the predicted trajectory.
   3. The vehicle is actually turning right. At :math:`t = 3` s, its
      true position is :math:`(52, 5)`. Compute the **prediction
      error** (Euclidean distance).
   4. On the same plot, show the true position at :math:`t = 3` s and
      draw a line between predicted and actual.

   **Written analysis**

   - Why does the CV model fail for turning maneuvers?
   - Write the **CTRA** (Constant Turn Rate and Acceleration) model
     equations and explain how they would improve this prediction.

   **Deliverable**

   The script, trajectory plot, and written analysis.


.. dropdown:: Exercise 2 -- Multi-Modal Prediction
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Reason about why multi-modal prediction is essential and how
   planners should consume probabilistic forecasts.


   .. raw:: html

      <hr>


   **Specification**

   A vehicle is approaching a T-intersection and can either turn left
   or continue straight.

   1. A **unimodal** predictor outputs the mean trajectory. Sketch
      this trajectory and explain in 2--3 sentences why it is
      **dangerous** (hint: the mean of two valid paths may be
      invalid).
   2. A **multi-modal** predictor outputs two trajectories:

      - Left turn: :math:`p = 0.6`
      - Straight: :math:`p = 0.4`

      How should the planner use these? Should it plan for the most
      likely one, or consider both? Why?

   3. Define **minADE₅** and **minFDE₅** in your own words (1--2
      sentences each).
   4. A model predicts 5 trajectories for an agent. The closest to
      ground truth is prediction #3 with ADE = 1.2 m and FDE = 2.5 m.
      What are minADE₅ and minFDE₅?

   **Deliverable**

   Sketch, written answers, and metric values.


.. dropdown:: Exercise 3 -- FSM Behavior Planner Design
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Design a finite state machine for highway driving with clearly
   defined states and transition conditions.


   .. raw:: html

      <hr>


   **Specification**

   Design an FSM with the following states:

   - ``LANE_FOLLOW`` -- maintain lane at reference speed
   - ``FOLLOW`` -- match speed of lead vehicle
   - ``PREPARE_LANE_CHANGE`` -- signal and check adjacent lane
   - ``LANE_CHANGE`` -- execute lane change
   - ``EMERGENCY_STOP`` -- maximum deceleration

   1. Draw the **state transition diagram** with labeled edges.
   2. Define transitions using TTC thresholds:

      - TTC < 2 s → ``EMERGENCY_STOP``
      - TTC < 5 s → ``FOLLOW``
      - In ``FOLLOW`` and speed < 60% of reference →
        ``PREPARE_LANE_CHANGE``
      - Adjacent lane clear for > 3 s →
        ``LANE_CHANGE``

   3. What happens if the adjacent lane is also blocked during
      ``PREPARE_LANE_CHANGE``? Add a transition for this case.
   4. Name **two limitations** of FSM-based behavior planning.
   5. How many states would you need for a busy urban intersection
      (traffic lights, pedestrians, cyclists)? Why do FSMs struggle
      at this scale?

   **Deliverable**

   State transition diagram (hand-drawn or digital) and written
   answers.


.. dropdown:: Exercise 4 -- Time-to-Collision
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compute TTC for various scenarios and reason about its limitations
   as a safety metric.


   .. raw:: html

      <hr>


   **Specification**

   The ego vehicle is at :math:`x = 0` m traveling at
   :math:`v_{\text{ego}} = 20` m/s. A lead vehicle is at
   :math:`x = 50` m traveling at :math:`v_{\text{lead}} = 10` m/s.
   Both are 4.5 m long.

   1. Compute **TTC** assuming constant velocities:

      .. math::

         \text{TTC} = \frac{x_{\text{lead}} - x_{\text{ego}} - L}
                           {v_{\text{ego}} - v_{\text{lead}}}

   2. If the ego brakes at :math:`a = -4` m/s², compute the
      **stopping distance**. Will it stop before hitting the lead
      vehicle?
   3. At what **following distance** is TTC exactly 3 seconds?
   4. A vehicle in the adjacent lane is approaching at 20 m/s on a
      **parallel path** (lateral offset 3.7 m). The TTC is very low,
      but there is **no collision risk**. Why is TTC alone
      insufficient for safe decisions?

   **Deliverable**

   All calculations shown and written answer for question 4.


.. dropdown:: Exercise 5 -- Behavior Cloning Failure Modes
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Understand the distribution shift problem in behavior cloning and
   evaluate mitigation strategies.


   .. raw:: html

      <hr>


   **Specification**

   A behavior cloning model is trained on 10 hours of expert driving
   data.

   1. Explain the **distribution shift** problem with a concrete
      example: the vehicle drifts 10 cm left of center. The training
      data never included this state. What happens next?
   2. Compounding error grows as :math:`O(\varepsilon T^2)`. If the
      per-step error is :math:`\varepsilon = 0.01` rad, compute the
      bound at :math:`T = 50` and :math:`T = 100` steps.
   3. **DAgger** addresses this by querying the expert on the
      learner's visited states. Describe **one practical challenge**
      of using DAgger for autonomous driving.
   4. Name one alternative approach that does not suffer from
      distribution shift. Explain in 2--3 sentences how it avoids
      the problem.

   **Deliverable**

   Written answers (one paragraph per question).
