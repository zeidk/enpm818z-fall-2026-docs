====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 7. Exercises cover coordinate transforms, odometry drift,
ICP registration, and SLAM evaluation.


.. dropdown:: Exercise 1 -- Coordinate Frame Transforms
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice converting between GNSS (geodetic) coordinates and local
   ENU coordinates, and constructing SE(2) transformation matrices.


   .. raw:: html

      <hr>


   **Specification**

   A vehicle is at GNSS coordinates **(lat 38.9897, lon -76.9378,
   alt 50 m)**. The local ENU origin is at **(lat 38.9900, lon
   -76.9380, alt 50 m)**.

   1. Convert the vehicle's position to **ENU coordinates** using:

      - :math:`\Delta E \approx \Delta\text{lon} \times \cos(\text{lat}) \times 111{,}320` m
      - :math:`\Delta N \approx \Delta\text{lat} \times 110{,}540` m

   2. The vehicle's heading is **45° from North** (clockwise). Write
      the **3 × 3 SE(2) homogeneous transformation matrix**
      :math:`T_{\text{vehicle}}^{\text{ENU}}`.

   3. A LiDAR point at ``(5, 2, 0)`` in the vehicle frame -- what are
      its **ENU coordinates**?

   **Deliverable**

   All conversions and matrix operations shown with numerical results.


.. dropdown:: Exercise 2 -- Odometry Drift Analysis
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Quantify odometry drift rates and reason about their impact on
   long-range navigation without GNSS.


   .. raw:: html

      <hr>


   **Specification**

   A vehicle drives a 500 m loop and returns to the start. Three
   odometry sources report the following final position errors:

   - **Wheel odometry**: 12.5 m error
   - **Visual odometry (stereo)**: 3.2 m error
   - **LiDAR odometry**: 0.8 m error

   1. Compute the **drift rate** (% of distance traveled) for each.
   2. If the vehicle must drive **10 km** without GNSS (tunnel + urban
      canyon), what is the expected error from each source?
   3. Name **two physical causes** of wheel odometry drift.
   4. Would fusing wheel + LiDAR odometry help? Explain using the
      concept of complementary information.
   5. At what drift rate does localization become **unsafe for lane
      keeping** (assume lane width = 3.7 m)?

   **Deliverable**

   Drift rate table, projected 10 km errors, and written answers.


.. dropdown:: Exercise 3 -- ICP Registration
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Understand and implement the ICP algorithm using Open3D.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``icp_exercise.py`` that performs the following:

   1. Generate a synthetic **source point cloud**: a 10 m × 10 m
      plane with 1000 random points and Gaussian noise
      (:math:`\sigma = 0.02` m).
   2. Create a **target point cloud** by applying a known
      transformation to the source: translation ``(1.0, 0.5, 0.0)``
      and rotation of ``5°`` about the z-axis.
   3. Run ``o3d.pipelines.registration.registration_icp`` with
      ``TransformationEstimationPointToPlane`` (estimate normals
      first).
   4. Print the **recovered transformation** and compare it to the
      ground-truth transform.
   5. Report the **fitness score** and **inlier RMSE**.

   **Written analysis**

   - What happens if you increase the rotation to 45°? Does ICP still
     converge?
   - Name two strategies to improve convergence for large initial
     displacements.

   **Deliverable**

   The script, printed results, and written analysis.


.. dropdown:: Exercise 4 -- SLAM Evaluation with EVO
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run a SLAM frontend in CARLA and evaluate trajectory accuracy
   using standard metrics.


   .. raw:: html

      <hr>


   **Specification**

   1. Run the SLAM frontend from the lecture on a **60-second drive**
      in Town03 (ICP-based scan matching).
   2. Record the **ground-truth trajectory** from CARLA at each
      timestep.
   3. Save both trajectories in **TUM format**:
      ``timestamp tx ty tz qx qy qz qw``.
   4. Use the ``evo`` tool to compute:

      .. code-block:: console

         evo_ape tum gt.txt est.txt -p --save_results ape.zip
         evo_rpe tum gt.txt est.txt -p --save_results rpe.zip

   5. Report: **mean APE**, **max APE**, **mean RPE**.

   **Written analysis**

   Is the drift accumulating **linearly** or **accelerating**? What
   would a loop closure add to this pipeline?

   **Deliverable**

   Both trajectory files, EVO output plots, metrics, and analysis.


.. dropdown:: Exercise 5 -- Loop Closure Impact
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Reason about the role of loop closure in SLAM and the dangers of
   false loop closures.


   .. raw:: html

      <hr>


   **Specification**

   Consider a pose graph with 100 nodes (poses) connected by 99
   sequential odometry edges.

   1. Draw a simple **pose graph** with 5 nodes and 4 sequential
      edges. Add a **loop closure edge** from node 5 back to node 1.
   2. Before optimization, node 5 has drifted **2 m** from its true
      position. After pose graph optimization, the correction is
      distributed across all nodes. What is the **approximate
      per-node correction** (assume uniform distribution)?
   3. In the 100-node graph, if the accumulated drift at node 100 is
      **5 m**, what is the per-node correction after a loop closure
      from node 100 to node 1?
   4. Why can a **single false loop closure** be catastrophic for the
      entire map?
   5. Name **two methods** used to verify loop closure candidates
      before adding them to the pose graph.

   **Deliverable**

   Pose graph sketch, calculations, and written answers.
