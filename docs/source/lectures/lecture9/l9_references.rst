References
==========


.. dropdown:: Lecture 9
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818Z -- L9: Trajectory Planning & Control**

        Covers path vs. trajectory (time parameterization),
        trajectory requirements (continuity, feasibility, comfort,
        safety), quintic polynomial trajectory generation in the
        Frenet frame, natural cubic splines and B-splines, optimization-
        based trajectory planning with QP/NLP cost functions,
        Model Predictive Control (MPC formulation, receding horizon,
        prediction horizon tuning, real-time QP solving), Pure
        Pursuit controller (lookahead distance, adaptive gain),
        Stanley controller (cross-track + heading error), PID
        longitudinal speed control with anti-windup, and CARLA
        lane-following implementation.


.. dropdown:: Trajectory Planning
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Werling et al. -- Frenet-Frame Planner (ICRA 2010)
            :class-card: sd-border-secondary

            **ICRA 2010**

            Seminal paper on Frenet-frame quintic polynomial
            trajectory generation for highway driving, including
            candidate sampling and cost-function-based selection.

            +++

            - Frenet frame formulation
            - Quintic polynomial candidates
            - Cost function design

        .. grid-item-card:: Ziegler et al. -- AV Berlin (2014)
            :class-card: sd-border-secondary

            **IEEE Intelligent Transportation Systems, 2014**

            Describes the full trajectory planning and control
            stack of the Bertha-Benz Memorial Route autonomous
            vehicle (Mercedes-Benz research).

            +++

            - End-to-end AV trajectory system
            - Spline-based path representation
            - Emergency maneuver handling

        .. grid-item-card:: Brezak & Petrovic -- Spline Path Planning
            :class-card: sd-border-secondary

            **IEEE T-ITS, 2014**

            Comparison of cubic and quintic spline methods for
            smooth path planning under kinematic constraints.

            +++

            - Curvature continuity analysis
            - Spline vs. polynomial trade-offs
            - Constraint satisfaction

        .. grid-item-card:: Farin -- NURBS and B-Splines
            :class-card: sd-border-secondary

            **A K Peters / CRC Press, 5th Ed.**

            Comprehensive reference for B-spline and NURBS
            theory, including knot insertion, degree elevation,
            and the convex hull and local support properties.

            +++

            - B-spline basis functions
            - Convex hull property
            - Knot vector design


.. dropdown:: Model Predictive Control
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Rawlings & Mayne -- MPC: Theory and Design
            :class-card: sd-border-secondary

            **Nob Hill Publishing, 2nd Ed.**

            The definitive graduate-level MPC textbook covering
            stability theory, constraint handling, and real-time
            implementation.

            +++

            - Receding horizon optimality
            - Terminal cost and constraint design
            - Stability guarantees

        .. grid-item-card:: Kong et al. -- Kinematic and Dynamic MPC (2015)
            :class-card: sd-border-secondary

            **IV 2015**

            Comparison of kinematic and dynamic bicycle model
            MPC for vehicle trajectory tracking across speed
            regimes.

            +++

            - Kinematic vs. dynamic MPC
            - Speed-regime suitability
            - Experimental validation

        .. grid-item-card:: OSQP Solver
            :link: https://osqp.org/
            :class-card: sd-border-secondary

            **OSQP (Operator Splitting QP)**

            Open-source QP solver well-suited to MPC due to
            its warm-starting capability and predictable
            real-time performance.

            +++

            - Warm-starting for MPC
            - Embedded C code generation
            - Real-time performance

        .. grid-item-card:: acados -- Real-Time NMPC
            :link: https://docs.acados.org/
            :class-card: sd-border-secondary

            **acados**

            Fast C library for nonlinear MPC with code
            generation for embedded automotive controllers.
            Supports SQP with Gauss-Newton Hessian approximation.

            +++

            - Nonlinear MPC formulation
            - Code generation
            - ROS 2 integration examples


.. dropdown:: Path-Following Controllers
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Coulter -- Pure Pursuit (1992)
            :class-card: sd-border-secondary

            **CMU Technical Report, 1992**

            Original Pure Pursuit algorithm from the CMU
            Navlab project. Includes derivation of the
            lookahead-to-curvature relationship and
            experimental results.

            +++

            - Geometric derivation
            - Lookahead distance analysis
            - Experimental validation

        .. grid-item-card:: Thrun et al. -- Stanley Controller (2006)
            :class-card: sd-border-secondary

            **JAIR, 2006 (DARPA Grand Challenge)**

            Describes the Stanley controller used on the
            Stanford entry in the DARPA Urban Challenge, with
            analysis of heading and cross-track error behavior.

            +++

            - Stanley derivation
            - Heading + cross-track error
            - Urban challenge results

        .. grid-item-card:: Snider -- Path Tracking Survey (2009)
            :class-card: sd-border-secondary

            **CMU Technical Report, 2009**

            Comprehensive comparison of path-tracking controllers
            (Pure Pursuit, Stanley, and variants) on the same
            test tracks and conditions.

            +++

            - Side-by-side comparison
            - Speed-regime analysis
            - Implementation details


.. dropdown:: PID Control
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Astrom & Hagglund -- PID Controllers
            :class-card: sd-border-secondary

            **ISA, 2nd Ed.**

            Standard reference for PID control covering
            Ziegler-Nichols tuning, anti-windup, derivative
            filtering, and practical implementation.

            +++

            - Ziegler-Nichols tuning
            - Anti-windup strategies
            - Bumpless transfer

        .. grid-item-card:: Franklin, Powell, Emami-Naeini
            :class-card: sd-border-secondary

            **Feedback Control of Dynamic Systems (8th Ed.)**

            Undergraduate-level control systems textbook with
            in-depth coverage of PID design, root locus, and
            frequency-domain stability analysis.

            +++

            - PID design methodology
            - Stability margins
            - Digital implementation


.. dropdown:: CARLA Simulator
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: CARLA Documentation
            :link: https://carla.readthedocs.io/
            :class-card: sd-border-secondary

            **carla.readthedocs.io**

            Official CARLA Python API documentation including
            vehicle control interfaces, waypoint API, sensor
            mounting, and traffic management.

            +++

            - VehicleControl API
            - Map and waypoint access
            - Sensor blueprint library

        .. grid-item-card:: Dosovitskiy et al. -- CARLA (CoRL 2017)
            :class-card: sd-border-secondary

            **CoRL 2017**

            Original CARLA paper describing the simulator
            architecture, sensor models, and evaluation metrics.

            +++

            - Simulator design
            - Benchmark scenarios
            - Sensor simulation fidelity

        .. grid-item-card:: Leaderboard 2.0
            :link: https://leaderboard.carla.org/
            :class-card: sd-border-secondary

            **CARLA Autonomous Driving Leaderboard**

            Official benchmark for evaluating autonomous driving
            agents in CARLA, including town routes, traffic
            scenarios, and scoring methodology.

            +++

            - Route completion metric
            - Infraction taxonomy
            - Submission guidelines


.. dropdown:: Benchmarks
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: nuPlan
            :link: https://nuplan.org/
            :class-card: sd-border-secondary

            **nuPlan Planning Benchmark**

            Closed-loop planning benchmark with 1300+ hours
            of real-world data. Used to evaluate MPC and
            learning-based trajectory planners.

            +++

            - Closed-loop reactive simulation
            - Standardized metrics (PDMs score)
            - Real-world driving scenarios

        .. grid-item-card:: CommonRoad
            :link: https://commonroad.in.tum.de/
            :class-card: sd-border-secondary

            **CommonRoad (TU Munich)**

            Benchmark and scenario format for trajectory
            planning evaluation with standardized kinematic
            feasibility checks.

            +++

            - Standardized scenario format
            - Feasibility checkers
            - Planning solution library
