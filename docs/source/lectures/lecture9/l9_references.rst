References
==========


.. dropdown:: Lecture 8
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818Z -- L8: Motion Planning**

        Covers the three-tier motion planning hierarchy (route,
        behavior, motion), bicycle kinematic model and nonholonomic
        constraints, graph-based planners (Dijkstra, A*, Weighted
        A*), sampling-based planners (RRT, RRT*, PRM), lattice-based
        planning in the Frenet frame with pre-computed motion
        primitives, geometric collision detection with safety
        margins (OBB, Minkowski sum), and diffusion-based planners
        (Diffusion Planner ICLR 2025, DiffusionDrive CVPR 2025).


.. dropdown:: Foundational Textbooks
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Choset et al. -- Principles of Robot Motion
            :class-card: sd-border-secondary

            **MIT Press, 2005**

            Comprehensive coverage of configuration spaces,
            potential fields, graph-based planning, and sampling-
            based planners. Chapters 4--7 are directly relevant
            to this lecture.

            +++

            - Configuration space theory
            - PRM and RRT derivations
            - Completeness and optimality proofs

        .. grid-item-card:: LaValle -- Planning Algorithms
            :class-card: sd-border-secondary

            **Cambridge University Press, 2006**
            (freely available at planning.cs.uiuc.edu)

            The definitive reference for motion planning
            algorithms. Covers discrete planning, sampling-based
            methods, and nonholonomic systems.

            +++

            - RRT and PRM foundations
            - Nonholonomic planning
            - Optimality analysis

        .. grid-item-card:: Thrun, Burgard, Fox -- Probabilistic Robotics
            :class-card: sd-border-secondary

            **MIT Press, 2005**

            Probabilistic foundations for robotics including
            localization, mapping, and planning under uncertainty.
            Relevant for understanding safety margins and
            uncertainty-aware planning.

            +++

            - Probabilistic state estimation
            - Occupancy grid maps
            - Planning under uncertainty

        .. grid-item-card:: Paden et al. -- Survey of AV Motion Planning
            :class-card: sd-border-secondary

            **IEEE T-ITS, 2016**

            Comprehensive survey of motion planning techniques
            specifically for autonomous vehicles, covering all
            algorithm families in this lecture.

            +++

            - Route, behavior, motion hierarchy
            - Graph-based and sampling-based planners
            - AV-specific constraints


.. dropdown:: Graph-Based Planning
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Hart, Nilsson, Raphael -- A* (1968)
            :class-card: sd-border-secondary

            **IEEE T-SSC, 1968**

            The original A* paper introducing the heuristic
            search algorithm and proving its optimality under
            admissible heuristics.

            +++

            - Original A* formulation
            - Admissibility proof
            - Heuristic design

        .. grid-item-card:: Likhachev et al. -- Weighted A* (2003)
            :class-card: sd-border-secondary

            **NIPS 2003**

            Introduces the :math:`\varepsilon`-suboptimal
            weighted A* variant with formal bounds on solution
            quality vs. computation time.

            +++

            - Inflation factor analysis
            - Anytime planning extensions
            - Practical implementation


.. dropdown:: Sampling-Based Planning
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: LaValle -- RRT (1998)
            :class-card: sd-border-secondary

            **Technical Report, Iowa State, 1998**

            Original RRT paper introducing rapidly-exploring
            random trees for single-query kinodynamic planning.

            +++

            - RRT algorithm
            - Probabilistic completeness proof
            - Kinodynamic extension

        .. grid-item-card:: Karaman & Frazzoli -- RRT* (2011)
            :class-card: sd-border-secondary

            **IJRR, 2011**

            Introduces RRT* with asymptotic optimality guarantee.
            Also introduces PRM* and formal analysis of
            sampling-based planner convergence rates.

            +++

            - RRT* rewiring algorithm
            - Asymptotic optimality proof
            - Convergence rate analysis

        .. grid-item-card:: Kavraki et al. -- PRM (1996)
            :class-card: sd-border-secondary

            **IEEE T-RA, 1996**

            Original PRM paper introducing probabilistic road
            maps for multi-query planning in high-dimensional
            configuration spaces.

            +++

            - Two-phase construction
            - Probabilistic completeness
            - Multi-query efficiency


.. dropdown:: Lattice-Based Planning
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Pivtoraiko et al. -- State Lattice (2009)
            :class-card: sd-border-secondary

            **JFR, 2009**

            Introduces the state lattice framework with
            pre-computed motion primitives for kinematically
            feasible robot motion planning.

            +++

            - Lattice construction methodology
            - Motion primitive generation
            - Search algorithms

        .. grid-item-card:: McNaughton et al. -- Frenet Lattice (2011)
            :class-card: sd-border-secondary

            **ICRA 2011 (Uber ATG)**

            Describes the Frenet-frame lattice planner used
            in structured autonomous driving, including
            lane-change and yield maneuver encoding.

            +++

            - Road-aligned lattice design
            - Lane change primitives
            - Real-time performance


.. dropdown:: Diffusion-Based Planning
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Zheng et al. -- Diffusion Planner (ICLR 2025)
            :class-card: sd-border-secondary

            **ICLR 2025**

            Joint ego-agent diffusion planner achieving
            state-of-the-art closed-loop performance on the
            nuPlan benchmark through interaction-aware trajectory
            denoising.

            +++

            - Joint prediction and planning
            - Scene context encoding
            - nuPlan benchmark results

        .. grid-item-card:: Liao et al. -- DiffusionDrive (CVPR 2025)
            :class-card: sd-border-secondary

            **CVPR 2025**

            Real-time diffusion planner using truncated schedule
            and anchored Gaussian initialization achieving 45 FPS
            while maintaining competitive nuPlan performance.

            +++

            - Truncated diffusion schedule
            - Anchored Gaussian initialization
            - Real-time inference analysis

        .. grid-item-card:: Ho et al. -- DDPM (NeurIPS 2020)
            :class-card: sd-border-secondary

            **NeurIPS 2020**

            Foundational paper establishing denoising diffusion
            probabilistic models, the framework underlying
            all diffusion-based planners.

            +++

            - Forward/reverse process formulation
            - Denoising score matching
            - Image generation results


.. dropdown:: Collision Detection
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Ericson -- Real-Time Collision Detection
            :class-card: sd-border-secondary

            **Morgan Kaufmann, 2004**

            Comprehensive reference for geometric collision
            detection algorithms including AABB, OBB, GJK,
            and sweep-based methods.

            +++

            - Bounding volume hierarchies
            - OBB intersection tests
            - Minkowski sum computation

        .. grid-item-card:: Berg et al. -- Reciprocal Velocity Obstacles
            :class-card: sd-border-secondary

            **IJRR, 2011**

            Velocity-obstacle-based collision avoidance for
            multi-agent scenarios, relevant to dynamic obstacle
            handling in AV planning.

            +++

            - Velocity obstacles
            - Multi-agent collision avoidance
            - Real-time performance


.. dropdown:: Benchmarks and Datasets
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: nuPlan Benchmark
            :link: https://nuplan.org/
            :class-card: sd-border-secondary

            **Motional / nuPlan**

            Closed-loop planning benchmark used to evaluate
            Diffusion Planner and DiffusionDrive, based on
            real-world driving logs.

            +++

            - Closed-loop reactive simulation
            - 1300+ hours of driving data
            - Standardized metrics

        .. grid-item-card:: CARLA Simulator
            :link: https://carla.org/
            :class-card: sd-border-secondary

            **CARLA Open-Source Simulator**

            High-fidelity autonomous driving simulator used
            for the lecture's implementation exercise. Provides
            waypoint graphs, sensor simulation, and traffic
            scenarios.

            +++

            - Python API documentation
            - Waypoint graph API
            - Traffic scenario library
