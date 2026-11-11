====================================================
References
====================================================

These are the sources of the L9 deck, grouped by the lecture's sections, in
the order the lecture first uses each one. A source used in several
sections is listed once, where the lecture first uses it. Two sources are
used only in the appendix (:doc:`l9_appendix`); they have their own group at
the end.

.. dropdown:: Introduction
   :class-container: sd-border-secondary
   :open:

   Route, path and trajectory, and the A* search the route planner runs.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Configuration, route planning, path, trajectory
         :link: https://doi.org/10.1109/TIV.2016.2578706
         :class-card: sd-border-secondary

         **Paden, B., Čáp, M., Yong, S. Z., Yershov, D. and Frazzoli, E.
         (2016)**

         "A Survey of Motion Planning and Control Techniques for Self-Driving
         Urban Vehicles". *IEEE Transactions on Intelligent Vehicles*, 1(1),
         33 to 55. doi:10.1109/TIV.2016.2578706. arXiv:1604.07446.

         A car's configuration, "the planar coordinate of a point on the car
         together with the car's heading". Route planning: the AV "must
         select a route through the road network from its current position
         to the requested destination". The survey separates a path from a
         trajectory, which adds times. The lecture's title, motion planning,
         is what the survey calls the local planner's job: finding a path
         the AV can drive, free of collisions.

      .. grid-item-card:: A*
         :link: https://doi.org/10.1109/TSSC.1968.300136
         :class-card: sd-border-secondary

         **Hart, P. E., Nilsson, N. J. and Raphael, B. (1968)**

         "A Formal Basis for the Heuristic Determination of Minimum Cost
         Paths". *IEEE Transactions on Systems Science and Cybernetics*,
         4(2), 100 to 107. doi:10.1109/TSSC.1968.300136.

         A*, which adds a heuristic, an estimate of the cost to the goal.
         The route planner runs A* on the lane graph, and so does GP4's
         planner. Also used in Garage Planners: grid search and hybrid A*
         are both A* searches.


.. dropdown:: The Scene
   :class-container: sd-border-secondary
   :open:

   How the road was read from CARLA's map file, with no CARLA server.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: CARLA's map and waypoints
         :link: https://carla.readthedocs.io/en/0.9.16/python_api/
         :class-card: sd-border-secondary

         **CARLA Team**

         *Python API Reference: carla.Map and carla.Waypoint.* CARLA
         Simulator, version 0.9.16. Accessed 14 October 2026.

         ``export_scene.py`` reads ``Town03.xodr`` with ``carla.Map`` and
         writes the lane centers every 0.5 m. Every distance on the road
         comes from these waypoints.


.. dropdown:: Configuration Space
   :class-container: sd-border-secondary
   :open:

   The configuration, configuration space and its obstacle region.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Configuration space
         :link: http://lavalle.pl/planning/
         :class-card: sd-border-secondary

         **LaValle, S. M. (2006)**

         *Planning Algorithms.* Cambridge University Press, Cambridge.
         Online at http://lavalle.pl/planning/.

         "The state space for motion planning is a set of possible
         transformations that could be applied to the robot. This will be
         referred to as the configuration space". Also used in the appendix:
         Section 4.3.2 derives the region an obstacle becomes for a robot
         that only translates.

      .. grid-item-card:: The configuration space approach
         :link: https://doi.org/10.1109/TC.1983.1676196
         :class-card: sd-border-secondary

         **Lozano-Pérez, T. (1983)**

         "Spatial Planning: A Configuration Space Approach". *IEEE
         Transactions on Computers*, C-32(2), 108 to 120.
         doi:10.1109/TC.1983.1676196.

         The deck lists it with LaValle for configuration space and its
         obstacle region.


.. dropdown:: Collision Checking
   :class-container: sd-border-secondary
   :open:

   The localization error bound behind the 0.3 m margin.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Localization requirements
         :link: https://doi.org/10.4271/12-02-03-0012
         :class-card: sd-border-secondary

         **Reid, T. G. R., Houts, S. E., Cammarata, R., Mills, G., Agarwal,
         S., Vora, A. and Pandey, G. (2019)**

         "Localization Requirements for Autonomous Vehicles". *SAE
         International Journal of Connected and Automated Vehicles*, 2(3),
         173 to 190. doi:10.4271/12-02-03-0012. arXiv:1906.01061.

         The error bound, "the allowable maximum position error of the
         vehicle to ensure it is within the lane": 0.29 m on a local street.
         The lecture rounds it to 0.3 m, the margin of the collision check.


.. dropdown:: The Frenet Frame
   :class-container: sd-border-secondary
   :open:

   Planning in coordinates along the road and across it.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Planning in a Frenet frame
         :link: https://doi.org/10.1109/ROBOT.2010.5509799
         :class-card: sd-border-secondary

         **Werling, M., Ziegler, J., Kammel, S. and Thrun, S. (2010)**

         "Optimal Trajectory Generation for Dynamic Street Scenarios in a
         Frenét Frame". *2010 IEEE International Conference on Robotics and
         Automation (ICRA)*, 987 to 993. IEEE.
         doi:10.1109/ROBOT.2010.5509799.

         Trajectories for street driving, planned in a Frenet frame along
         the road: the frame of the Frenet Frame and Sampling Paths
         sections. The authors "generate a one-dimensional trajectory for
         both the root point :math:`\vec{r}` along the center line and the
         perpendicular offset :math:`d`"; their root point is the lecture's
         foot point.


.. dropdown:: Sampling Paths
   :class-container: sd-border-secondary
   :open:

   Stanford's Junior, whose planner rolled out paths shifted sideways.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Junior
         :link: https://doi.org/10.1002/rob.20258
         :class-card: sd-border-secondary

         **Montemerlo, M., Becker, J., Bhat, S., Dahlkamp, H., Dolgov, D.,
         Ettinger, S., Haehnel, D., Hilden, T., Hoffmann, G., Huhnke, B.,
         Johnston, D., Klumpp, S., Langer, D., Levandowski, A., Levinson, J.,
         Marcil, J., Orenstein, D., Paefgen, J., Penny, I., Petrovskaya, A.,
         Pflueger, M., Stanek, G., Stavens, D., Vogt, A. and Thrun, S.
         (2008)**

         "Junior: The Stanford Entry in the Urban Challenge". *Journal of
         Field Robotics*, 25(9), 569 to 597. doi:10.1002/rob.20258.

         Junior drove the 2007 DARPA Urban Challenge. The lecture takes three
         facts from it: on roads it rolled out paths parallel to the lane's
         center and shifted sideways; its behavior layer was a finite state
         machine with 13 states (Behavior); and it used hybrid A* in parking
         lots (Garage Planners).


.. dropdown:: Behavior
   :class-container: sd-border-secondary
   :open:

   The Nash equilibrium of the lane change game.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Nash equilibrium
         :link: https://doi.org/10.1073/pnas.36.1.48
         :class-card: sd-border-secondary

         **Nash, Jr., J. F. (1950)**

         "Equilibrium Points in n-Person Games". *Proceedings of the
         National Academy of Sciences*, 36(1), 48 to 49.
         doi:10.1073/pnas.36.1.48.

         The paper that introduced the equilibrium named after Nash, used in
         "The Lane Change as a Game".


.. dropdown:: Garage Planners
   :class-container: sd-border-secondary
   :open:

   Hybrid A*, RRT and RRT*.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Hybrid A*
         :link: https://cdn.aaai.org/Workshops/2008/WS-08-10/WS08-10-006.pdf
         :class-card: sd-border-secondary

         **Dolgov, D., Thrun, S., Montemerlo, M. and Diebel, J. (2008)**

         "Practical Search Techniques in Path Planning for Autonomous
         Driving". *Proceedings of the First International Symposium on
         Search Techniques in Artificial Intelligence and Robotics
         (STAIR-08)*. AAAI, Chicago, USA.

         Hybrid A*, which keeps an exact pose in each cell. Also used in the
         appendix: "Our search algorithm is guided by two heuristics", and
         near the goal, "analytic expansions based on the Reed-Shepp model".

      .. grid-item-card:: RRT
         :link: http://lavalle.pl/papers/Lav98c.pdf
         :class-card: sd-border-secondary

         **LaValle, S. M. (1998)**

         *Rapidly-Exploring Random Trees: A New Tool for Path Planning.*
         Technical Report TR 98-11, Computer Science Department, Iowa State
         University.

         The original RRT. As the lecture says, it makes each step by
         steering the robot's model, as hybrid A* does, so its path can be
         driven; the lecture's garage RRT takes straight steps instead.

      .. grid-item-card:: RRT*
         :link: https://doi.org/10.1177/0278364911406761
         :class-card: sd-border-secondary

         **Karaman, S. and Frazzoli, E. (2011)**

         "Sampling-Based Algorithms for Optimal Motion Planning". *The
         International Journal of Robotics Research*, 30(7), 846 to 894.
         doi:10.1177/0278364911406761. arXiv:1105.1186.

         The two proved results of "RRT*: the Path Keeps Getting Shorter",
         and, in "RRT and RRT* in Words", the "nearby" radius that shrinks as
         the tree grows and "Theorem 33 (Non-optimality of RRT) The RRT
         algorithm is not asymptotically optimal".


.. dropdown:: Next Class
   :class-container: sd-border-secondary
   :open:

   Where learning fits in the lecture's picture.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: End-to-end driving
         :link: https://doi.org/10.1109/TPAMI.2024.3435937
         :class-card: sd-border-secondary

         **Chen, L., Wu, P., Chitta, K., Jaeger, B., Geiger, A. and Li, H.
         (2024)**

         "End-to-End Autonomous Driving: Challenges and Frontiers". *IEEE
         Transactions on Pattern Analysis and Machine Intelligence*, 46(12),
         10164 to 10183. doi:10.1109/TPAMI.2024.3435937. arXiv:2306.16927.

         The definition of end-to-end driving: "We define end-to-end
         autonomous driving systems as fully differentiable programs that
         take raw sensor data as input and produce a plan and/or low-level
         control actions as output".

      .. grid-item-card:: Tesla's end-to-end FSD
         :link: https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q1-2024-Update.pdf
         :class-card: sd-border-secondary

         **Tesla (2024)**

         *Q1 2024 Update.* Shareholder update, 23 April 2024. Accessed 24
         October 2026.

         The source for "In 2024, Tesla said its FSD runs on end-to-end
         neural networks".


.. dropdown:: Used Only in the Appendix
   :class-container: sd-border-secondary

   Markov decision processes and the curves hybrid A* tries at the goal,
   from :doc:`l9_appendix`.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Reeds and Shepp curves
         :link: https://doi.org/10.2140/pjm.1990.145.367
         :class-card: sd-border-secondary

         **Reeds, J. and Shepp, L. (1990)**

         "Optimal Paths for a Car That Goes Both Forwards and Backwards".
         *Pacific Journal of Mathematics*, 145(2), 367 to 393.
         doi:10.2140/pjm.1990.145.367.

         The shortest curve to a goal pose for a car that drives forward
         and backward. Hybrid A* tries one as a single piece near the goal;
         the course's version tries a straight reverse instead.

      .. grid-item-card:: Markov decision processes
         :link: http://incompleteideas.net/book/the-book-2nd.html
         :class-card: sd-border-secondary

         **Sutton, R. S. and Barto, A. G. (2018)**

         *Reinforcement Learning: An Introduction*, 2nd edition. The MIT
         Press, Cambridge, Massachusetts.

         The definition of a Markov decision process (p. 47) and of a
         partially observable one (p. 467), used in "Behavior as an MDP" on
         the Going Further page.



.. rubric:: Map data and images

The road in every top view is CARLA's ``Town03.xodr``, read offline with the
CARLA Python API. The vehicle icons in the figures were created by Stone
from the `Noun Project <https://thenounproject.com>`_.
