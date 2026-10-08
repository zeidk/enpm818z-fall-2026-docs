====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

This page contains take-home exercises that reinforce the concepts from
Lecture 5. Exercises cover BEV representation, the Lift-Splat-Shoot
pipeline, occupancy networks, and semantic segmentation.


.. dropdown:: Exercise 1 -- Perspective vs. BEV Representation
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Build geometric intuition for why BEV is preferred for planning
   while perspective views are better for recognition.


   .. raw:: html

      <hr>


   **Specification**

   A vehicle is located **30 m ahead** and **5 m to the left** of the
   ego vehicle. A second vehicle is **60 m ahead** in the same lane.

   1. In a front-facing camera image (640 × 480, 90° FOV), roughly
      where does the first vehicle appear (left/center/right)? Would
      it appear large or small?
   2. In a BEV grid (100 m × 100 m, 0.5 m/cell, ego at center), what
      are the **grid coordinates** (row, col) of the first vehicle?
   3. In the camera image, how does the second vehicle's apparent size
      compare to the first? In BEV?
   4. Write 3--4 sentences explaining why BEV is preferred for
      **planning** while perspective is better for **fine-grained
      recognition** (e.g., reading a traffic sign).

   **Deliverable**

   Written answers with coordinate calculations shown.


.. dropdown:: Exercise 2 -- Multi-Camera Rig Coverage
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Analyze the coverage pattern of a multi-camera rig and identify
   blind spots and overlap regions.


   .. raw:: html

      <hr>


   **Specification**

   A six-camera rig is mounted on a vehicle:

   - Front: ``(2.0, 0, 1.5)`` m, yaw ``0°``, FOV ``110°``
   - Front-Left: ``(1.5, -0.8, 1.5)`` m, yaw ``-55°``, FOV ``110°``
   - Front-Right: ``(1.5, 0.8, 1.5)`` m, yaw ``55°``, FOV ``110°``
   - Rear: ``(-2.0, 0, 1.5)`` m, yaw ``180°``, FOV ``110°``
   - Rear-Left: ``(-1.5, -0.8, 1.5)`` m, yaw ``-125°``, FOV ``110°``
   - Rear-Right: ``(-1.5, 0.8, 1.5)`` m, yaw ``125°``, FOV ``110°``

   1. Sketch a **top-down view** of the camera coverage (show FOV
      cones). Is there any blind spot around the vehicle?
   2. Compute the **angular overlap** between the Front and Front-Left
      cameras. Why is overlap important for BEV construction?
   3. A pedestrian stands at ``(0, -3, 0)`` relative to the vehicle
      (directly to the left, 3 m away). Which camera(s) can see them?

   **Deliverable**

   Top-down coverage sketch and written answers.


.. dropdown:: Exercise 3 -- Lift-Splat-Shoot Pipeline
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Understand the computational structure of the LSS pipeline by
   working through the numbers.


   .. raw:: html

      <hr>


   **Specification**

   In the LSS pipeline, each pixel predicts a **depth distribution**
   over :math:`D` discrete bins.

   1. If the depth range is ``[2 m, 50 m]`` with 1 m bins, how many
      bins :math:`D` are there?
   2. Each pixel generates :math:`D` feature points in 3D. For an
      image of size ``H = 224, W = 400``, how many 3D points does a
      **single camera** produce?
   3. With **6 cameras**, what is the total number of 3D points before
      splatting?
   4. The BEV grid covers ``[-50 m, 50 m]`` in X and Y with 0.5 m
      resolution. How many cells does the grid have?
   5. Why does LSS use **sum pooling** (not max pooling) when
      accumulating features in the BEV grid?

   **Deliverable**

   Numerical answers with calculations shown, plus a written
   explanation for question 5.


.. dropdown:: Exercise 4 -- BEV Grid Resolution Trade-Off
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Empirically evaluate how BEV grid resolution affects detail and
   computational cost using CARLA.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``bev_resolution.py`` that performs the following:

   1. Spawn an ego vehicle with a depth camera in Town03.
   2. Using the simplified LSS pipeline from the lecture (ground-truth
      depth), generate BEV grids at three resolutions:

      - **0.25 m** per cell
      - **0.5 m** per cell
      - **1.0 m** per cell

   3. For each resolution, measure and report:

      - BEV grid dimensions (rows × cols) for a 100 m × 100 m area.
      - Computation time to generate one BEV frame.
      - Number of occupied cells (cells with ≥ 1 point).

   4. Save the three BEV visualizations as images.

   **Written analysis**

   - Can you distinguish between two vehicles parked side-by-side at
     each resolution?
   - Recommend a resolution that balances detail and compute cost for
     real-time driving at 10 Hz.

   **Deliverable**

   The script, three BEV images, results table, and recommendation.


.. dropdown:: Exercise 5 -- Occupancy vs. Detection
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Reason about when detection-based vs. occupancy-based perception
   is more appropriate for safe navigation.


   .. raw:: html

      <hr>


   **Specification**

   Consider a scene with the following four objects:

   - A **parked car** (standard rectangular shape)
   - A **fallen tree** across the road (irregular shape)
   - A **construction barrier** (thin, elongated)
   - An **overhanging branch** at 2.5 m height

   For each object, fill in the table:

   .. list-table::
      :widths: 25 25 25 25
      :header-rows: 1
      :class: compact-table

      * - Object
        - Well represented by 3D bbox?
        - Well represented by occupancy?
        - More useful for planner?
      * - Parked car
        -
        -
        -
      * - Fallen tree
        -
        -
        -
      * - Construction barrier
        -
        -
        -
      * - Overhanging branch
        -
        -
        -

   Write a concluding paragraph (5--7 sentences) arguing when a
   production ADS should use detection-based vs. occupancy-based
   perception, or both.

   **Deliverable**

   Completed table and written analysis.


.. dropdown:: Exercise 6 -- Segmentation Metrics
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


Python Exercises
----------------

Exercises 7 to 10 use small Python scripts that run on your own machine, with
no CARLA and no downloads beyond two packages:

.. code-block:: bash

   pip3 install numpy matplotlib
   python3 ipm_bev.py              # opens a window with the figure
   python3 ipm_bev.py --save a.png # or writes it to a file
   python3 ipm_bev.py --help       # every option

Every script builds a synthetic scene in CARLA's vehicle frame (x forward,
y right, z up), the frame of Exercise 2, and prints the numbers the questions
ask about. The ROS package ``l5_bev_demo`` uses the ROS frame instead, where
y points left: flip the sign of y to compare the two.
Change the constants at the top of a script to try your own cases.


.. dropdown:: Exercise 7: Inverse Perspective Mapping
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See what a ground-plane homography does to a front camera image, and
   where its flat-ground assumption fails.


   .. raw:: html

      <hr>


   **Specification**

   Download :download:`ipm_bev.py <scripts/ipm_bev.py>`. It renders a front
   camera (1.6 m up, pitched 5° down) looking at three lane lines and a
   parked car, warps the image to BEV with a homography, and shows the true
   top view beside it.

   1. Run it. In the IPM panel the lane lines are parallel, but the car
      becomes a long dark wedge. Which assumption of IPM does the car break,
      and why does that stretch it **away** from the camera?
   2. The car is 1.5 m tall. Use similar triangles to find where IPM puts
      the top of the car's rear face: a point 16 m in front of the camera,
      0.1 m below it. Does your answer agree with the wedge running off the
      top of the plot?
   3. Run ``--pitch-error 1.0`` and ``--pitch-error -1.0``. How do the lane
      lines change in each case? Why does a one-degree calibration error
      matter more at 40 m than at 10 m?
   4. The script prints how many image rows one 5 cm BEV cell spans at
      10 m and at 40 m. What does that tell you about the detail available
      in the far part of an IPM image?

   **Deliverable**

   Written answers, with the similar-triangle calculation for question 2.


.. dropdown:: Exercise 8: Lift-Splat with Depth Uncertainty
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See how the depth distribution each pixel predicts shapes the BEV
   features in Lift-Splat-Shoot, and why LSS pools with a sum.


   .. raw:: html

      <hr>


   **Specification**

   Download :download:`lift_splat_toy.py <scripts/lift_splat_toy.py>`. Only
   pixels that see a car carry a feature. Each pixel lifts it to one point
   per depth bin, weighted by the bin's probability, and the points are
   splatted into a BEV grid. ``--depth`` sets how sure the "network" is
   about depth.

   1. Check the printed number of lifted points against your formula from
      Exercise 3.
   2. Run ``--depth sharp``. The nearest car's feature lands along one edge
      of its footprint, not over the whole footprint. Which edge, and why?
   3. Run ``--depth blurred`` and ``--depth uniform``. Describe the shape
      each car takes in BEV. With uniform depth the brightest cells are near
      the camera, where there is no car at all. Why?
   4. Compare the printed ``grid.sum()`` for ``--pool sum`` and
      ``--pool max``. Which one equals the number of car pixels? Use this to
      answer question 5 of Exercise 3 again.
   5. Change ``DEPTH_STEP`` to 0.5 m. How many depth bins and lifted points
      are there now? What does that cost a real network with six cameras?

   **Deliverable**

   Written answers, with one screenshot for each depth mode.


.. dropdown:: Exercise 9: Checking Multi-Camera Coverage
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Check your answers to Exercise 2, and find the blind spots that a
   top-down sketch of the field-of-view cones misses.


   .. raw:: html

      <hr>


   **Specification**

   Do Exercise 2 by hand first. Then download
   :download:`multicam_coverage.py <scripts/multicam_coverage.py>`. It counts,
   for every ground cell around the car, how many cameras of the Exercise 2
   rig see it.

   1. Compare the printed overlap of the Front and Front-Left cameras with
      your answer to question 2 of Exercise 2.
   2. Which cameras see the pedestrian of question 3? If the script
      disagrees with your answer, compute the bearing of the pedestrian
      from the Front-Left and Rear-Left cameras (not from the car's center)
      and explain the difference.
   3. The script assumes a 1600 × 900 image to get the vertical FOV. Run
      ``--image 1600 1200``. How does the blind area within 5 m change, and
      why does the vertical FOV matter for the ground near the car?
   4. Move the pedestrian to ``(0.0, -6.0)`` by editing ``PEDESTRIAN``.
      Which cameras see them now?

   **Deliverable**

   Written answers, with the bearing calculation for question 2.


.. dropdown:: Exercise 10: Occupancy Grid vs. Detection Boxes
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Build intuition for Exercise 5 by comparing an occupancy grid with a
   detector's boxes on the same scene.


   .. raw:: html

      <hr>


   **Specification**

   Download :download:`occupancy_vs_boxes.py <scripts/occupancy_vs_boxes.py>`.
   A 2D scanner at the origin builds a log-odds occupancy grid; a detector
   that knows only cars and pedestrians reports boxes. Both answer the same
   question: is the lane ahead clear?

   1. Run it. What does each view say about the corridor, and which object
      makes them disagree?
   2. What are the gray regions in the occupancy view? Should a planner
      treat "unknown" as free?
   3. Far from the scanner, free cells look striped. Why? Run
      ``--beam-step 0.25`` and ``--beam-step 2.0`` and compare.
   4. Run ``--scans 1 --noise 0.10``. How many occupied corridor cells are
      left, compared with the default run?
   5. With ``L_OCC = 0.85``, how many hits does a cell need to pass
      :math:`p > 0.7`? Use :math:`l = \log\frac{p}{1 - p}`. How many if
      ``L_OCC`` were 0.4?

   **Deliverable**

   Written answers, and the calculation for question 5.
