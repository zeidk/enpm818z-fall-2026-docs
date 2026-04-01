====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 8: Motion Planning,
including the planning hierarchy, bicycle kinematic model,
graph-based planners (Dijkstra, A*, Weighted A*), sampling-based
planners (RRT, RRT*, PRM), lattice-based planning, collision
detection, and diffusion-based planning.

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

   In the three-tier autonomous vehicle planning hierarchy, which tier
   is responsible for deciding whether the vehicle should change lanes
   or yield to an oncoming vehicle?

   A. Route planning (Tier 1)

   B. Behavior planning (Tier 2)

   C. Motion planning (Tier 3)

   D. Trajectory planning (a separate fourth tier)

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Behavior planning (Tier 2).

   Behavior planning operates at the intersection scale and decides
   *how* the vehicle interacts with other agents -- lane-keeping,
   lane-change, yield, stop. Route planning selects which roads to
   use. Motion planning finds a collision-free geometric path within
   the maneuver envelope defined by the behavior planner. Trajectory
   planning (covered in L9) adds the time dimension to the path.


.. admonition:: Question 2
   :class: hint

   The bicycle kinematic model describes vehicle heading change as:

   .. math::

      \dot{\theta} = \frac{v}{L} \tan\delta

   If the wheelbase :math:`L = 2.7` m, speed :math:`v = 10` m/s,
   and the steering angle :math:`\delta = 0.15` rad, what is
   :math:`\dot{\theta}` (approximately)?

   A. 0.055 rad/s

   B. 0.55 rad/s

   C. 5.5 rad/s

   D. 0.0055 rad/s

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Approximately 0.55 rad/s.

   .. math::

      \dot{\theta} = \frac{10}{2.7} \tan(0.15) \approx
      3.70 \times 0.1501 \approx 0.556 \text{ rad/s}

   At this heading rate the vehicle completes roughly one full turn
   every 11 seconds, consistent with a gentle highway curve at
   36 km/h.


.. admonition:: Question 3
   :class: hint

   A* search is guaranteed to find the optimal path when:

   A. The heuristic overestimates the true cost-to-go by at most 10%.

   B. The heuristic is admissible (never overestimates the true
      cost-to-go).

   C. The graph has no negative edge weights.

   D. The goal node is expanded before any other node with higher
      :math:`f`-value.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The heuristic is admissible (never overestimates).

   Admissibility ensures that whenever a node is expanded, its
   :math:`g`-value is already optimal. An overestimating heuristic
   can cause A* to expand the goal prematurely with a suboptimal
   cost. Note: non-negative edge weights are required by Dijkstra
   but A* inherits this requirement too; however, the critical
   guarantee for *optimality specifically* is admissibility of
   the heuristic.


.. admonition:: Question 4
   :class: hint

   Weighted A* with inflation factor :math:`\varepsilon = 3` finds a
   path of cost 120. What is the tightest guarantee on the optimal
   path cost?

   A. The optimal cost is at least 40.

   B. The optimal cost is at least 60.

   C. The optimal cost is at least 90.

   D. No guarantee can be made.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- The optimal cost is at least 40.

   Weighted A* guarantees that the returned cost is at most
   :math:`\varepsilon` times the optimal cost:

   .. math::

      \text{cost}_{returned} \leq \varepsilon \cdot \text{cost}^*
      \implies 120 \leq 3 \cdot \text{cost}^*
      \implies \text{cost}^* \geq 40

   The optimal cost is therefore at least 40 (it could be anywhere
   in :math:`[40, 120]`).


.. admonition:: Question 5
   :class: hint

   What is the key property that makes RRT* asymptotically optimal
   but plain RRT is not?

   A. RRT* uses a bidirectional search from both start and goal.

   B. RRT* rewires the tree to reassign parents when a cheaper
      path to a node is found.

   C. RRT* uses a grid-based heuristic instead of random sampling.

   D. RRT* runs Dijkstra on the final tree to extract the path.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- RRT* rewires the tree to reassign parents when a cheaper
   path to a node is found.

   The two extra steps in RRT* (parent selection within a shrinking
   radius and tree rewiring) allow the algorithm to continuously
   improve path cost as more samples are added. Plain RRT only
   adds edges and never removes or reassigns them, so the first
   path found is never improved.


.. admonition:: Question 6
   :class: hint

   A Probabilistic Road Map (PRM) is best described as:

   A. A single-query planner that rebuilds the graph for every new
      start/goal pair.

   B. A multi-query planner that constructs a roadmap offline and
      reuses it for many queries.

   C. A planner that samples configurations online during execution
      to react to dynamic obstacles.

   D. An exact planner that guarantees finding the shortest path.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A multi-query planner that constructs a roadmap offline
   and reuses it for many queries.

   PRM's two-phase design (offline construction + online query)
   amortizes the sampling cost over many planning queries. This
   makes it efficient for static or semi-static environments
   where the same roadmap can be queried repeatedly (e.g., a
   warehouse or structured parking garage).


.. admonition:: Question 7
   :class: hint

   In lattice-based planning for autonomous vehicles, motion
   primitives are:

   A. Computed online at every planning cycle using numerical
      integration of the bicycle model.

   B. Pre-computed offline kinematically feasible maneuvers stored
      in a lookup table.

   C. Straight-line segments connecting adjacent grid cells,
      ignoring vehicle kinematics.

   D. Neural network outputs that map sensor data to control actions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Pre-computed offline kinematically feasible maneuvers
   stored in a lookup table.

   The key advantage of lattice planning is that the expensive
   kinematic computation (integrating the bicycle model, checking
   curvature limits) is done once offline. At runtime, planning
   reduces to pure graph search with O(1) edge lookups, enabling
   real-time replanning at 20--50 Hz.


.. admonition:: Question 8
   :class: hint

   The Minkowski sum :math:`\mathcal{O} \oplus \mathcal{B}(d)` used
   in collision detection safety margins:

   A. Shrinks the obstacle by radius :math:`d` to create a
      conservative free space.

   B. Inflates the obstacle boundary outward by radius :math:`d`,
      equivalent to shrinking the robot to a point.

   C. Computes the intersection of the obstacle with a circle of
      radius :math:`d`.

   D. Rotates the obstacle by angle :math:`d` around its centroid.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Inflates the obstacle boundary outward by radius
   :math:`d`.

   The Minkowski sum with a disk inflates every point on the
   obstacle boundary outward by :math:`d`. This is equivalent
   to shrinking the robot to a point and planning in the inflated
   configuration space -- a standard trick that reduces collision
   checking to point-in-polygon tests. The safety margin encodes
   both localization uncertainty and comfort distance.


.. admonition:: Question 9
   :class: hint

   DiffusionDrive (CVPR 2025) achieves real-time performance
   compared to earlier diffusion planners primarily by:

   A. Using a larger neural network with more parameters.

   B. Running a truncated diffusion schedule starting partway
      through the denoising chain, reducing denoising steps from
      ~100 to ~10.

   C. Replacing the Transformer encoder with a simpler CNN.

   D. Only planning for the next 1 second instead of 8 seconds.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Using a truncated diffusion schedule starting partway
   through the denoising chain.

   DiffusionDrive initializes from anchored Gaussian noise
   (clustered around likely trajectory modes) rather than pure
   noise, and runs the reverse diffusion process starting from
   step :math:`T' \ll T`. This dramatically cuts the number of
   network forward passes required at inference while maintaining
   trajectory quality, enabling 45 FPS on a single GPU.


.. admonition:: Question 10
   :class: hint

   Which planning algorithm is most appropriate for real-time motion
   planning on a structured highway road network?

   A. Plain RRT (fast first path)

   B. PRM (multi-query roadmap)

   C. Lattice-based planner in Frenet frame

   D. Full RRT* (asymptotically optimal)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Lattice-based planner in Frenet frame.

   Highway driving is highly structured: lanes are well-defined,
   maneuvers are limited, and replanning must occur at 10--50 Hz.
   Lattice planners exploit this structure through pre-built
   road-aligned motion primitives and fast graph search. RRT/RRT*
   are designed for unstructured spaces and converge slowly. PRM
   is a multi-query planner but its roadmap is not road-aligned.


----


True / False
============

.. admonition:: Question 11
   :class: hint

   **True or False:** The bicycle model imposes a holonomic
   constraint, meaning the vehicle can move freely in any direction
   including sideways.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The bicycle model imposes a **nonholonomic** constraint:
   :math:`\dot{x}\sin\theta - \dot{y}\cos\theta = 0`. This
   prohibits lateral (sideways) motion. A nonholonomic constraint
   restricts the instantaneously achievable velocities but not
   necessarily the reachable configurations over time (the vehicle
   can parallel-park using a sequence of forward/backward arcs).


.. admonition:: Question 12
   :class: hint

   **True or False:** Dijkstra's algorithm expands nodes in
   increasing order of their true cost-to-come :math:`g(v)`.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Dijkstra maintains a min-priority queue keyed on :math:`g(v)`.
   Each extraction yields the node with the smallest known
   cost-to-come among unvisited nodes. This is exactly the
   Bellman optimality condition: once a node is extracted, its
   :math:`g`-value is optimal (assuming non-negative edge weights).


.. admonition:: Question 13
   :class: hint

   **True or False:** RRT is probabilistically complete, meaning
   that given infinite samples it will always find a path if one
   exists.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   RRT is probabilistically complete. As the number of random
   samples :math:`N \to \infty`, the probability that the tree
   fails to reach any reachable configuration goes to zero. This
   follows from the density of the sampling distribution over
   :math:`\mathcal{C}_{free}`. However, probabilistic completeness
   does not guarantee path quality -- RRT finds *a* path, not
   necessarily a *good* path.


.. admonition:: Question 14
   :class: hint

   **True or False:** In diffusion-based planning, the reverse
   (denoising) process starts from a trajectory drawn from the
   dataset and gradually removes noise.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The reverse process starts from **pure Gaussian noise**
   :math:`\tau_T \sim \mathcal{N}(0, I)` (or, in DiffusionDrive,
   from anchored noise near likely trajectory clusters). It is the
   *forward* process that starts from a real trajectory and adds
   noise. The reverse process is the generative (planning) process
   that denoises from noise to a plausible trajectory.


.. admonition:: Question 15
   :class: hint

   **True or False:** Inflating obstacle representations by a safety
   margin :math:`d_{\text{safe}}` is equivalent to planning with a
   point-mass robot in the inflated configuration space.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   When all obstacles are inflated by the robot's radius (or
   safety margin) via the Minkowski sum, the robot can be treated
   as a point mass for collision checking purposes. Any path that
   is collision-free for the point mass in the inflated space is
   also collision-free for the full-size robot in the original
   space. This simplification is used in virtually all practical
   motion planners.


----


Essay Questions
===============

.. admonition:: Question 16
   :class: hint

   **Compare RRT and A* as motion planners for an autonomous
   vehicle navigating a structured urban environment.** Address
   completeness, optimality, computational efficiency, and
   suitability for real-time replanning.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A* on a pre-built road graph is complete and optimal
     (with an admissible heuristic) and runs in milliseconds
     on sparse road graphs, making it well-suited for real-time
     replanning in structured environments.
   - RRT is probabilistically complete but not optimal; it
     explores uniformly in all directions including off-road
     areas, making it inefficient when the environment has
     exploitable structure (lanes, intersections).
   - For structured urban driving, A* (or lattice search) is
     strongly preferred. RRT is better suited to unstructured
     spaces (parking, off-road) where a road-graph abstraction
     does not exist.
   - Weighted A* with :math:`\varepsilon > 1` reduces the number
     of expanded nodes at the cost of a bounded suboptimality,
     making it the practical choice for real-time urban planning.


.. admonition:: Question 17
   :class: hint

   **Explain the concept of asymptotic optimality in RRT* and
   why it matters for practical motion planning.** What is the
   trade-off between RRT and RRT* in a time-constrained setting?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Asymptotic optimality means that as the number of samples
     :math:`N \to \infty`, the cost of the RRT* path converges
     to the true optimal cost. For any finite :math:`N`, RRT*
     provides a path that is at least as good as RRT's.
   - RRT* achieves this through the parent-selection and rewiring
     steps that continuously improve the tree structure as new
     samples are added.
   - The trade-off: RRT* does more work per sample (neighbor
     search within radius :math:`r_N`), so it runs slower than
     RRT for a fixed time budget. In time-constrained scenarios
     RRT might find a feasible path faster.
   - In practice, RRT* is used for offline planning or as an
     *anytime* algorithm: run it until the time budget expires
     and return the best path found so far.


.. admonition:: Question 18
   :class: hint

   **Describe how diffusion-based planners differ from classical
   optimization-based motion planners.** What advantages do they
   offer for complex multi-agent scenarios, and what are their
   current limitations?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Classical optimization-based planners define an explicit
     cost function (e.g., path length + smoothness + safety
     margin) and solve a constrained optimization problem. They
     are interpretable and can encode hard constraints but
     struggle with multi-modal distributions over possible
     futures.
   - Diffusion planners learn a generative model of plausible
     trajectories from expert data. The denoising process
     implicitly captures the multi-modal distribution of human
     driving behavior and can generate diverse, interaction-
     consistent plans.
   - Advantages: handles complex interactions without hand-crafted
     cost functions; naturally multi-modal (can represent
     uncertainty over which maneuver to take).
   - Limitations: require large, high-quality training datasets;
     inference is more expensive than classical planners;
     safety guarantees are harder to formally prove; behavior
     can be hard to interpret or correct when it fails.
