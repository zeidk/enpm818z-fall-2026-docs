====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 9. Exercises cover vehicle kinematics, graph-based planning,
sampling-based planning, and collision detection.


.. dropdown:: Exercise 1 -- Bicycle Model Kinematics
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Simulate vehicle motion using the kinematic bicycle model and
   understand the effect of steering angle on turning radius.


   .. raw:: html

      <hr>


   **Specification**

   The bicycle model equations are:

   .. math::

      \dot{x} = v \cos(\theta), \quad
      \dot{y} = v \sin(\theta), \quad
      \dot{\theta} = \frac{v}{L} \tan(\delta)

   with wheelbase :math:`L = 2.9` m.

   Create the file ``bicycle_model.py`` that performs the following:

   1. With :math:`v = 10` m/s and :math:`\delta = 15°`, compute the
      **turning radius** :math:`R = L / \tan(\delta)`.
   2. Starting from :math:`(x, y, \theta) = (0, 0, 0)`, simulate the
      vehicle for **5 seconds** with :math:`\Delta t = 0.1` s using
      Euler integration. **Plot the resulting path**.
   3. Repeat with :math:`\delta = 0°` and :math:`\delta = 30°`. Plot
      all three paths on the same figure.
   4. The vehicle has a maximum steering angle of **35°**. Compute the
      **minimum turning radius**.

   **Expected output**

   A plot showing three paths (straight, gentle curve, tight curve)
   and printed turning radius values.

   **Deliverable**

   The script and the plot (PNG or PDF).


.. dropdown:: Exercise 2 -- A* on an Occupancy Grid
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Implement A* search on a 2D occupancy grid with obstacles and
   evaluate the effect of obstacle inflation.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``astar_grid.py`` that performs the following:

   1. Create a **50 × 50 occupancy grid** with these obstacles:

      - A wall from (10, 0) to (10, 35)
      - A wall from (30, 15) to (30, 49)
      - A rectangular block at (20, 20) to (25, 25)

   2. Implement **A* search** with 8-connected neighbors and Euclidean
      distance heuristic.
   3. Find the shortest path from **(0, 0)** to **(49, 49)**.
   4. Report **path length** and **nodes expanded**.
   5. **Inflate obstacles** by 2 cells (to account for vehicle width)
      and replan. Report new path length and nodes expanded.
   6. Visualize both paths on the grid (original in blue, inflated in
      red).

   **Written analysis**

   Replace the Euclidean heuristic with **Manhattan distance**. Is it
   still admissible for 8-connected grids? Does the path change?

   **Deliverable**

   The script, grid visualization, results table, and written answer.


.. dropdown:: Exercise 3 -- RRT vs. RRT*
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Implement both RRT and RRT* and compare path quality as a function
   of iteration count.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``rrt_comparison.py`` that performs the following:

   1. Define a **50 × 50 m** workspace with 5 circular obstacles
      (radius 2 m each) at fixed locations.
   2. Implement **RRT** with step size 2.0 m and 2000 iterations.
      Find a path from **(5, 5)** to **(45, 45)**.
   3. Implement **RRT*** with the same parameters, using rewiring
      radius:

      .. math::

         r = \gamma \left(\frac{\log n}{n}\right)^{1/d}, \quad
         \gamma = 50, \; d = 2

   4. Plot both trees and final paths side-by-side.
   5. Run RRT* with **500, 1000, 2000, and 5000 iterations**. Plot
      **path length vs. iterations**.

   **Expected result**

   RRT* should produce progressively shorter paths as iterations
   increase, while RRT's path length does not improve.

   **Deliverable**

   The script, tree visualizations, and path length convergence plot.


.. dropdown:: Exercise 4 -- Lattice-Based Planning
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Design motion primitives for a highway lattice planner and reason
   about the combinatorial structure.


   .. raw:: html

      <hr>


   **Specification**

   A state lattice planner uses pre-computed motion primitives in the
   Frenet frame. Define **5 primitives** for a highway scenario:

   - Stay in lane (straight, 30 m longitudinal)
   - Slight left offset (+0.5 m lateral over 30 m)
   - Slight right offset (-0.5 m lateral over 30 m)
   - Lane change left (+3.7 m lateral over 30 m)
   - Lane change right (-3.7 m lateral over 30 m)

   1. Sketch the resulting **lattice** for 3 steps, showing all
      reachable states from the start position.
   2. How many **total unique paths** exist after 3 steps?
      (Hint: :math:`5^3`, but some may overlap.)
   3. Design a **cost function** that penalizes:

      - Lateral deviation from lane center
      - Lateral acceleration (comfort)
      - Proximity to obstacles

   4. Why are lattice planners preferred on **highways** but not in
      **unstructured parking lots**?

   **Deliverable**

   Lattice sketch, path count, cost function definition, and written
   answer.


.. dropdown:: Exercise 5 -- Collision Checking
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Implement oriented bounding box collision detection using the
   separating axis theorem.


   .. raw:: html

      <hr>


   **Specification**

   A vehicle is represented as an **OBB** with dimensions 4.5 m × 2.0 m,
   centered at (10, 5) with heading 30°. An obstacle is a **circle**
   centered at (13, 7) with radius 1.0 m.

   Create the file ``collision_check.py`` that performs the following:

   1. Compute the **four corners** of the OBB in world coordinates.
   2. Implement the **separating axis theorem (SAT)** to determine if
      the OBB and circle collide.
   3. **Inflate** the vehicle by a **0.5 m safety margin** on all
      sides and check again.
   4. Compute the **minimum center-to-center distance** at which the
      inflated OBB and circle just touch.
   5. Visualize the OBB, inflated OBB, and circle using matplotlib.

   **Deliverable**

   The script, collision results (True/False for each case), minimum
   distance value, and visualization plot.
