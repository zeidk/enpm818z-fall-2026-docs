====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 4. Exercises cover BEV representation, the Lift-Splat-Shoot
pipeline, and occupancy networks.


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
