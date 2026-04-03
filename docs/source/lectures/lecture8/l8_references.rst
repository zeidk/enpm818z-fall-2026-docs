====================================================
References
====================================================


Textbooks and Surveys
---------------------

.. list-table::
   :widths: 100
   :class: compact-table

   * - .. dropdown:: LaValle (2006) -- Planning Algorithms, Ch. 2: Discrete Planning

         | **Planning Algorithms**
         | Steven M. LaValle, Cambridge University Press, 2006
         | `Available free online <http://lavalle.pl/planning/>`_

         Covers graph search algorithms (BFS, DFS, Dijkstra, A*) with
         formal analysis. Chapter 2 provides the theoretical foundation
         for route planning on discrete graphs.

         **Key topics:**

            - Graph representations
            - Dijkstra's algorithm
            - A* search and admissible heuristics
            - Complexity analysis

   * - .. dropdown:: Paden et al. (2016) -- A Survey of Motion Planning and Control Techniques for Self-Driving Vehicles

         | **A Survey of Motion Planning and Control Techniques for Self-Driving Vehicles**
         | Brian Paden, Michal Čáp, Sze Zheng Yong, Dmitry Yershov, Emilio Frazzoli
         | IEEE Transactions on Intelligent Vehicles, 2016

         Covers the full planning hierarchy including route planning,
         behavioral planning, and motion planning. Provides the three-tier
         framework used in this lecture.

         **Key topics:**

            - Route, behavior, motion planning hierarchy
            - Road network representations
            - Decision-making architectures


Map Formats and Standards
-------------------------

.. list-table::
   :widths: 100
   :class: compact-table

   * - .. dropdown:: ASAM OpenDRIVE Standard

         | **ASAM OpenDRIVE -- Open Dynamic Road Information for Vehicle Environment**
         | `ASAM OpenDRIVE <https://www.asam.net/standards/detail/opendrive/>`_

         The industry standard for describing road networks in driving
         simulation. Used by CARLA, dSPACE, IPG CarMaker, and others.

         **Key topics:**

            - Road reference lines (geometry primitives)
            - Lane sections and lane types
            - Junction definitions
            - Signal and object elements

   * - .. dropdown:: Poggenhans et al. (2018) -- Lanelet2: A High-Definition Map Framework

         | **Lanelet2: A High-Definition Map Framework for the Future of Automated Driving**
         | Fabian Poggenhans et al., IEEE ITSC 2018

         Describes the Lanelet2 map framework used by Autoware and many
         research platforms. Boundary-based lane representation with
         regulatory elements.

         **Key topics:**

            - Lanelet representation (left/right linestrings)
            - Regulatory elements (traffic lights, stop lines)
            - Routing graph construction
            - OSM-based file format


Route Planning Algorithms
-------------------------

.. list-table::
   :widths: 100
   :class: compact-table

   * - .. dropdown:: Geisberger et al. (2012) -- Exact Routing in Large Road Networks Using Contraction Hierarchies

         | **Exact Routing in Large Road Networks Using Contraction Hierarchies**
         | Robert Geisberger, Peter Sanders, Dominik Schultes, Christian Vetter
         | Transportation Science, 2012

         Describes Contraction Hierarchies, the algorithm behind many
         production routing engines. Precomputes a hierarchy that enables
         microsecond query times on continental-scale road networks.

         **Key topics:**

            - Node contraction and shortcut edges
            - Bidirectional search on the hierarchy
            - Preprocessing vs. query time trade-off

   * - .. dropdown:: Hart, Nilsson & Raphael (1968) -- A Formal Basis for the Heuristic Determination of Minimum Cost Paths

         | **A Formal Basis for the Heuristic Determination of Minimum Cost Paths**
         | Peter E. Hart, Nils J. Nilsson, Bertram Raphael
         | IEEE Transactions on Systems Science and Cybernetics, 1968

         The original A* paper. Proves optimality and completeness of A*
         with admissible heuristics.

         **Key topics:**

            - A* algorithm formulation
            - Admissibility and consistency of heuristics
            - Optimality proof


CARLA Navigation
----------------

.. list-table::
   :widths: 100
   :class: compact-table

   * - .. dropdown:: CARLA Documentation -- Navigation and Maps

         | **CARLA Documentation: Maps and Navigation**
         | `carla.readthedocs.io <https://carla.readthedocs.io/en/0.9.16/core_map/>`_

         Official documentation for CARLA's map and waypoint system,
         including the GlobalRoutePlanner API.

         **Key topics:**

            - Map and waypoint API
            - GlobalRoutePlanner usage
            - Road topology queries
            - OpenDRIVE integration

   * - .. dropdown:: CARLA Documentation -- Agents Module

         | **CARLA Agents**
         | `carla.readthedocs.io <https://carla.readthedocs.io/en/0.9.16/adv_agents/>`_

         Documentation for CARLA's built-in agent implementations,
         including the BasicAgent and BehaviorAgent that use the
         GlobalRoutePlanner internally.

         **Key topics:**

            - BasicAgent (route following)
            - BehaviorAgent (traffic-aware driving)
            - Local planner integration


Industry and Applications
-------------------------

.. list-table::
   :widths: 100
   :class: compact-table

   * - .. dropdown:: Bast et al. (2016) -- Route Planning in Transportation Networks

         | **Route Planning in Transportation Networks**
         | Hannah Bast, Daniel Delling, Andrew Goldberg, et al.
         | Algorithm Engineering, Springer, 2016

         Comprehensive survey of route planning algorithms used in
         production systems (Google Maps, Bing Maps, OSRM).

         **Key topics:**

            - Dijkstra, A*, bidirectional search
            - Contraction Hierarchies, Transit Node Routing
            - Time-dependent and multi-criteria routing
            - Real-world engineering considerations

   * - .. dropdown:: Autoware Foundation -- Autoware.Universe Routing

         | **Autoware.Universe: Mission Planner and Route Planner**
         | `Autoware Documentation <https://autowarefoundation.github.io/autoware-documentation/main/>`_

         Open-source AV routing implementation built on Lanelet2 maps.
         Demonstrates a production-grade route planner integrated with
         ROS 2.

         **Key topics:**

            - Mission planner architecture
            - Lanelet2 routing graph
            - Lane-level route generation
            - Integration with behavior and motion planners
