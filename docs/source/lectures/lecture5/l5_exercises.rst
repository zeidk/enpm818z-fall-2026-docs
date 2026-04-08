====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 5. Exercises cover segmentation metrics, Kalman filter
tracking, and the Hungarian algorithm.


.. dropdown:: Exercise 1 -- Segmentation Metrics
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice computing IoU and mIoU from a confusion matrix.


   .. raw:: html

      <hr>


   **Specification**

   A semantic segmentation model produces the following confusion
   matrix for three classes:

   .. list-table::
      :widths: 25 25 25 25
      :header-rows: 1
      :class: compact-table

      * - Predicted \\ Actual
        - Road
        - Vehicle
        - Pedestrian
      * - Road
        - 8000
        - 200
        - 50
      * - Vehicle
        - 300
        - 1500
        - 100
      * - Pedestrian
        - 100
        - 50
        - 700

   1. Compute the **IoU** for each class using
      :math:`\text{IoU} = \frac{TP}{TP + FP + FN}`.
   2. Compute the **mIoU** across all three classes.
   3. Which class has the worst IoU? Suggest one reason why.
   4. If you could only optimize one class for safety, which would you
      choose and why?

   **Deliverable**

   All IoU calculations shown with final mIoU value, plus written
   answers to questions 3 and 4.


.. dropdown:: Exercise 2 -- Kalman Filter Tracking (Pen and Paper)
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Work through two full Kalman filter predict-update cycles by hand
   to build intuition for state estimation.


   .. raw:: html

      <hr>


   **Specification**

   A tracked vehicle has state
   :math:`\mathbf{x} = [x, v_x]^T` (1D position and velocity).

   - Motion model:
     :math:`F = \begin{bmatrix} 1 & \Delta t \\ 0 & 1 \end{bmatrix}`
   - Measurement model: :math:`H = [1 \;\; 0]` (observe position only)
   - Initial state: :math:`\mathbf{x}_0 = [0, 5]^T`
   - Initial covariance:
     :math:`P_0 = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}`
   - Process noise:
     :math:`Q = \begin{bmatrix} 0.1 & 0 \\ 0 & 0.1 \end{bmatrix}`
   - Measurement noise: :math:`R = [2]`
   - Time step: :math:`\Delta t = 1` s

   Perform **two full predict-update cycles** with measurements
   :math:`z_1 = 4.5` m and :math:`z_2 = 10.2` m.

   For each cycle, show:

   1. **Predicted state** :math:`\hat{\mathbf{x}}^-` and
      **predicted covariance** :math:`P^-`.
   2. **Kalman gain** :math:`K`.
   3. **Updated state** :math:`\hat{\mathbf{x}}^+` and
      **updated covariance** :math:`P^+`.

   **Deliverable**

   Complete hand calculations for both cycles (show all matrix
   operations).


.. dropdown:: Exercise 3 -- Hungarian Algorithm
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice the detection-to-track association step used in SORT.


   .. raw:: html

      <hr>


   **Specification**

   At time :math:`t`, three tracked objects have predicted positions:

   - Track A: (10, 20)
   - Track B: (30, 15)
   - Track C: (50, 40)

   Four new detections arrive:

   - D1: (11, 21)
   - D2: (52, 38)
   - D3: (31, 14)
   - D4: (70, 60)

   1. Compute the **Euclidean distance cost matrix** (3 tracks ×
      4 detections).
   2. Apply a **gating threshold** of 10 m -- mark which assignments
      are impossible.
   3. Find the **optimal assignment** (by inspection or using
      ``scipy.optimize.linear_sum_assignment``).
   4. Which detection is **unmatched**? What should the tracker do
      with it?
   5. If Track C had no valid match (all distances > 10 m), how many
      consecutive frames of no match before the track should be
      **deleted**?

   **Deliverable**

   Cost matrix, gated matrix, optimal assignment, and written answers.


.. dropdown:: Exercise 4 -- SORT vs. ByteTrack
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compare SORT and ByteTrack tracking performance in CARLA and
   understand why the second association pass helps.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``tracker_comparison.py`` that performs the
   following:

   1. Spawn traffic in a busy intersection (Town03 or Town05, 30+
      vehicles).
   2. Implement a **basic SORT tracker** using the lecture code (Kalman
      filter + Hungarian matching at confidence > 0.5).
   3. Run for **200 frames** and count the number of **ID switches**.
   4. Modify the tracker to implement **ByteTrack's two-pass
      association**:

      - First pass: match high-confidence detections (> 0.5).
      - Second pass: match low-confidence detections (0.2--0.5) to
        remaining unmatched tracks.

   5. Run ByteTrack on the same 200 frames and count ID switches.
   6. Print a comparison:

      .. code-block:: text

         SORT:      ID switches = ??
         ByteTrack: ID switches = ??

   **Written analysis**

   Explain in 3--5 sentences **why** the second pass helps during
   occlusions.

   **Deliverable**

   The script, comparison results, and written analysis.


.. dropdown:: Exercise 5 -- Tracking Metrics Computation
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compute MOTA from tracking results and reason about acceptable
   performance thresholds.


   .. raw:: html

      <hr>


   **Specification**

   Given the following tracking results over 5 frames:

   .. list-table::
      :widths: 12 16 16 20 20 16
      :header-rows: 1
      :class: compact-table

      * - Frame
        - GT
        - Matched
        - Missed (FN)
        - False pos (FP)
        - ID switches
      * - 1
        - 4
        - 3
        - 1
        - 1
        - 0
      * - 2
        - 4
        - 4
        - 0
        - 0
        - 0
      * - 3
        - 5
        - 3
        - 2
        - 2
        - 1
      * - 4
        - 5
        - 4
        - 1
        - 1
        - 0
      * - 5
        - 4
        - 4
        - 0
        - 0
        - 1

   1. Compute **MOTA** using:

      .. math::

         \text{MOTA} = 1 - \frac{\sum(\text{FN} + \text{FP} + \text{IDSW})}{\sum \text{GT}}

   2. Is this a good MOTA score? What value is typically considered
      acceptable for autonomous driving?
   3. Which frame has the worst performance? What might have caused
      the spike in errors?
   4. If you could improve only one component (reduce FN, reduce FP,
      or reduce IDSW), which would have the largest impact on MOTA?

   **Deliverable**

   MOTA calculation with all intermediate sums shown, plus written
   answers.
