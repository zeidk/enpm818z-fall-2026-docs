====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 13. Exercises cover world model concepts, scenario design,
domain randomization, and counterfactual evaluation.


.. dropdown:: Exercise 1 -- World Model Concepts
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Solidify the formal definition of a world model and reason about
   its advantages and risks.


   .. raw:: html

      <hr>


   **Specification**

   Answer the following questions:

   1. A world model predicts
      :math:`p(o_{t+1:t+H} \mid o_{1:t}, a_{t:t+H})`. In the context
      of autonomous driving, what are :math:`o` (observations),
      :math:`a` (actions), and :math:`H` (horizon)? Give concrete
      examples.
   2. Why is a world model more useful than a **replay buffer** of
      past driving data for training a planner? (Hint: think about
      counterfactual actions.)
   3. Name **two advantages** of generating training data with a world
      model vs. collecting real-world data.
   4. Name **two risks** of training exclusively on world-model
      generated data.

   **Deliverable**

   Written answers (2--4 sentences per question).


.. dropdown:: Exercise 2 -- Safety-Critical Scenario Design
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Design and implement rare but dangerous scenarios in CARLA that
   would be difficult to encounter in real-world data collection.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``critical_scenarios.py`` that implements **three
   scenarios**:

   1. **Pedestrian dart-out**: A pedestrian suddenly steps off the
      curb into the ego vehicle's lane. Use
      ``walker_controller.go_to_location()`` with a timed trigger
      (activate when ego is 30 m away).

   2. **Stopped vehicle on highway**: Place a stationary vehicle in a
      highway lane in Town04. The ego vehicle approaches at 60 km/h.

   3. **Sensor blackout**: Simulate a 2-second camera failure by
      stopping the camera callback mid-drive.

   For each scenario:

   - Enable CARLA's autopilot on the ego vehicle.
   - Record the ego vehicle's response (speed, steering, braking).
   - Note whether the autopilot handled it correctly.

   **Written analysis**

   For each scenario, explain:

   - Why is this scenario important for **ADS validation**?
   - How would a world model help generate **variations** of this
     scenario at scale?

   **Deliverable**

   The script, recorded responses, and written analysis.


.. dropdown:: Exercise 3 -- Domain Randomization
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Implement domain randomization in CARLA and evaluate its impact on
   detector robustness.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``domain_randomization.py`` that performs the
   following:

   1. For each of **100 frames**, randomize:

      - **Weather**: randomly select from 5+ presets.
      - **Sun altitude**: random value between -20° and 90°.
      - **NPC count**: random vehicles (10--80) and pedestrians
        (5--30).
      - **Camera noise**: add Gaussian noise (:math:`\sigma = 5`) to
        the captured image.

   2. Collect a second set of **100 frames** under fixed
      ``ClearNoon`` conditions (no randomization).
   3. Run YOLOv8s inference on both sets and compute:

      - **Mean confidence** of detections.
      - **Mean detection count** per frame.

   4. Print a comparison table.

   **Written analysis**

   If you trained a detector on the randomized dataset vs. the fixed
   dataset, which would generalize better to the real world? Why?

   **Deliverable**

   The script, comparison table, and written analysis (3--5 sentences).


.. dropdown:: Exercise 4 -- Synthetic Data Quality Assessment
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Assess the quality of CARLA-generated data by comparing its
   characteristics to real-world driving datasets.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``data_quality.py`` that performs the following:

   1. Generate **200 labeled images** from CARLA across 4 weather
      conditions and 2 towns. Use CARLA's ground-truth bounding box
      API.
   2. Compute the **class distribution** across the dataset (vehicles,
      pedestrians, cyclists, traffic lights, stop signs).
   3. Compare to the **nuScenes** dataset class frequencies (look up
      approximate ratios from the nuScenes website or papers).
   4. Identify **three visual differences** between CARLA images and
      real-world driving images (e.g., texture quality, lighting,
      pedestrian appearance).

   **Written analysis**

   - Are the CARLA and nuScenes class distributions similar?
   - Name **two techniques** from the lecture that help bridge the
     sim-to-real gap.

   **Deliverable**

   The script, class distribution bar chart, comparison table, and
   written analysis.


.. dropdown:: Exercise 5 -- Counterfactual Evaluation
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Reason about how world models enable offline evaluation of
   alternative planning decisions.


   .. raw:: html

      <hr>


   **Specification**

   Consider the following logged scenario: the ego vehicle encounters
   a slow truck and decides to **follow it for 30 seconds**.

   1. Define **three alternative actions** the planner could have
      taken (e.g., lane change left, overtake via oncoming lane, slow
      down earlier).
   2. For each alternative, list the information a world model would
      need to **simulate the outcome** (other agents' reactions,
      traffic rules, visibility, road geometry).
   3. Design a **reward function** to score each outcome:

      .. math::

         R = w_s \cdot \text{safety} + w_p \cdot \text{progress}
             + w_c \cdot \text{comfort}

      Define each term concretely (e.g., safety = 0 if collision,
      progress = distance traveled / time, comfort = -RMS jerk).

   4. Why is counterfactual evaluation **difficult without a world
      model**? What assumption does simple log replay make that breaks
      down?

   **Deliverable**

   Written answers with the reward function definition and reasoning.
