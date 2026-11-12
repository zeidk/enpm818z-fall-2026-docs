====================================================
References
====================================================

These are the sources of the L10 deck, grouped by the lecture's sections, in
the order the lecture first uses each one. A source used in several
sections is listed once, where the lecture first uses it. Several sources
are quoted only in a "More detail" box of the lecture; their cards say so.


.. dropdown:: Introduction
   :class-container: sd-border-secondary
   :open:

   Path tracking against trajectory tracking.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Steering methods compared
         :class-card: sd-border-secondary

         **Snider, J. M. (2009)**

         *Automatic Steering Methods for Autonomous Automobile Path
         Tracking.* Technical report CMU-RI-TR-09-08, Robotics Institute,
         Carnegie Mellon University, Pittsburgh, PA.

         Quoted first in "Compare Path Tracking and Trajectory Tracking":
         "Path tracking refers to a vehicle executing a globally defined
         geometric path by applying appropriate steering motions". Quoted
         again for the bicycle model, the lookahead trade-off, the steering
         controllers' groupings, Pure Pursuit's strengths and limits, and
         (in a "More detail" box) Snider's guidelines for matching a
         controller to the job and his dynamic-model and LQR numbers.


.. dropdown:: Scaling the Behavior Layer
   :class-container: sd-border-secondary
   :open:

   Statecharts, behavior trees, and how real stacks organize their behavior
   layer.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Statecharts: superstates
         :class-card: sd-border-secondary

         **Harel, D. (1987)**

         "Statecharts: A Visual Formalism for Complex Systems". *Science of
         Computer Programming*, 8, 231 to 274.

         Why one flat FSM grows too fast: "two components with one thousand
         states each would result in one million states in the product".
         Superstates, "the main way statecharts economize in the number of
         arrows".

      .. grid-item-card:: Behavior trees
         :link: https://ar5iv.arxiv.org/html/1709.00084
         :class-card: sd-border-secondary

         **Colledanchise, M. and Ögren, P. (2018)**

         *Behavior Trees in Robotics and AI: An Introduction.* Chapman &
         Hall/CRC. arXiv:1709.00084. Accessed 7 November 2026.

         The definition of a behavior tree, quoted in "Define a Behavior
         Tree". Ticks and the three statuses (Running, Success, Failure),
         quoted in "Read a Behavior Tree".

      .. grid-item-card:: Nav2's behavior tree navigator
         :link: https://github.com/ros-navigation/navigation2/tree/main/nav2_bt_navigator
         :class-card: sd-border-secondary

         **Nav2 contributors (2026)**

         *nav2_bt_navigator and nav2_behavior_tree README files, and
         nav2_params.yaml.* Accessed 7 November 2026.

         Nav2, ROS 2's navigation stack, runs a behavior tree (the Scaling
         the Behavior Layer section's opening). Also quoted in the "More
         detail" box "What Real Stacks Use": the navigator "uses the
         Behavior-Tree.CPP library to dynamically create and execute the
         BT".

      .. grid-item-card:: py_trees
         :link: https://github.com/splintered-reality/py_trees
         :class-card: sd-border-secondary

         **Splintered Reality (2026)**

         *py_trees: pythonic implementation of behaviour trees.* PyPI
         package py-trees, version 2.6.0. Accessed 12 November 2026.

         Named in "Code a Behavior Tree" as the Python library.

      .. grid-item-card:: py_trees_ros
         :link: https://github.com/splintered-reality/py_trees_ros
         :class-card: sd-border-secondary

         **Splintered Reality (2026)**

         *py_trees_ros: Behaviours, trees, and utilities that extend PyTrees
         for use with ROS.* Accessed 12 November 2026.

         Named in "Code a Behavior Tree" as the library for ROS 2.

      .. grid-item-card:: BehaviorTree.CPP
         :link: https://github.com/BehaviorTree/BehaviorTree.CPP
         :class-card: sd-border-secondary

         **BehaviorTree.CPP contributors (2026)**

         *BehaviorTree.CPP.* C++17 library; graphical editor Groot2.
         Accessed 12 November 2026.

         Named in "Code a Behavior Tree": Nav2 runs its trees with it.

      .. grid-item-card:: Autoware's behavior path planner, older design
         :link: https://autowarefoundation.github.io/autoware.universe_planning/pr-5562/planning/behavior_path_planner
         :class-card: sd-border-secondary

         **Autoware Foundation (2023)**

         *behavior_path_planner (older documentation build, pull request
         5562).* Documentation build for pull request 5562, opened 13
         November 2023. Accessed 7 November 2026.

         Used only in the "More detail" box "What Real Stacks Use": the
         planner once ran its modules from a behavior tree, chosen for its
         "high scalability compared to the state machine".

      .. grid-item-card:: Autoware's Planner Manager
         :link: https://autowarefoundation.github.io/autoware_universe/main/planning/behavior_path_planner/autoware_behavior_path_planner/
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *autoware_behavior_path_planner: Planner Manager design.* Accessed
         7 November 2026.

         Used only in the "More detail" box "What Real Stacks Use": today a
         Planner Manager runs the modules, candidate modules in parallel
         until approved, approved modules in series.

      .. grid-item-card:: Apollo's scenarios and stages
         :link: https://github.com/ApolloAuto/apollo/blob/master/modules/planning/planning_interface_base/scenario_base/scenario.h
         :class-card: sd-border-secondary

         **Apollo Auto (2026)**

         *Apollo planning: scenario.h and scenario_manager.cc.* Accessed 7
         November 2026.

         Used only in the "More detail" box "What Real Stacks Use": each
         scenario's stage "determines the transition from one stage to
         another".


.. dropdown:: Trajectory Generation
   :class-container: sd-border-secondary
   :open:

   Trajectories in the Frenet frame.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Trajectories in the Frenet frame
         :link: https://doi.org/10.1109/ROBOT.2010.5509799
         :class-card: sd-border-secondary

         **Werling, M., Ziegler, J., Kammel, S. and Thrun, S. (2010)**

         "Optimal Trajectory Generation for Dynamic Street Scenarios in a
         Frenét Frame". *2010 IEEE International Conference on Robotics and
         Automation (ICRA)*, 987 to 993. doi:10.1109/ROBOT.2010.5509799.

         Quoted in "Plan Across the Road: the Offset d(t) as a Quintic" and
         "Score Comfort with Jerk: Werling's Cost": "ease and comfort can be
         best described by the jerk". Also used in the "More detail" box
         "A Quartic to Keep a Speed...": the quartic and quintic conditions.


.. dropdown:: Control-to-Actuator Interface
   :class-container: sd-border-secondary
   :open:

   Drive-by-wire actuators and the steering chain's measured delay.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Steering chain delay, measured on a research car
         :class-card: sd-border-secondary

         **Xu, S., Peng, H. and Tang, Y. (2021)**

         "Preview Path Tracking Control With Delay Compensation for
         Autonomous Vehicles". *IEEE Transactions on Intelligent
         Transportation Systems*, 22(5), 2979 to 2989.
         doi:10.1109/TITS.2020.2978417.

         Quoted in "Measure the Chain's Delay": on a Lincoln MKZ, "the
         steering wheel starts to rotate roughly 0.2 s after the command
         :math:`\delta` is delivered". Also used in the "More detail" box
         "ECUs, CAN...": the command's path from the control app to the
         motor, and (in "The Dynamic Bicycle Model") the MKZ's tire
         stiffness.

      .. grid-item-card:: The CAN bus specification
         :class-card: sd-border-secondary

         **Robert Bosch GmbH (1991)**

         *CAN Specification, Version 2.0.* Robert Bosch GmbH, Stuttgart.

         Used only in the "More detail" box "ECUs, CAN, a Message Layout
         and Fail-Safe Checks": each CAN frame "carries an identifier and
         from 0 to 8 bytes of data", and the bus runs "with bitrates up to
         1 Mbit/s".


.. dropdown:: Vehicle Modeling
   :class-container: sd-border-secondary
   :open:

   Ackermann steering, the kinematic bicycle model, CARLA's vehicle command,
   and where the kinematic model stops holding.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Ackermann steering geometry
         :class-card: sd-border-secondary

         **Moldovanu, D., Csato, A. and Bagameri, N. (2019)**

         "Study Regarding the Implementation of an Ackerman Steering
         Geometry in MATLAB". *Annals of the Oradea University, Fascicle of
         Management and Technological Engineering*, XXIX (XIX)(3).
         doi:10.15660/auofmte.2019-3.3506.

         Quoted in "Turn Four Wheels About One Point": "the inner wheel has
         a bigger steer angle than the outer wheel, because is closer to
         the centre of rotation". Also used in the "More detail" box
         "Ackermann's Two Wheel Angles" for the Ackermann condition.

      .. grid-item-card:: CARLA's vehicle command
         :link: https://carla.readthedocs.io/en/latest/python_api/
         :class-card: sd-border-secondary

         **CARLA Team (2026)**

         *Python API Reference: carla.VehicleControl and
         carla.VehicleAckermannControl.* Accessed 14 October 2026.

         Quoted in "Collapse Four Wheels into Two": CARLA too takes one
         ``steer`` angle. Also used in the "More detail" boxes "Ackermann's
         Two Wheel Angles" and "CARLA Inputs and Outputs": the command and
         state CARLA takes and gives, and the waypoint it returns at a
         junction.

      .. grid-item-card:: Why no linkage is perfectly Ackermann
         :class-card: sd-border-secondary

         **Peñuñuri, F., Peón-Escalante, R., Villanueva, C. and Pech-Oy, D.
         (2011)**

         "Synthesis of Mechanisms for Single and Hybrid Tasks Using
         Differential Evolution". *Mechanism and Machine Theory*, 46(10),
         1335 to 1349. doi:10.1016/j.mechmachtheory.2011.05.013.

         Used only in the "More detail" box "Ackermann's Two Wheel Angles":
         "there is no four-bar mechanism that can fulfill the Ackerman
         condition perfectly".

      .. grid-item-card:: The kinematic bicycle model's limits
         :link: https://doi.org/10.1109/IVS.2017.7995816
         :class-card: sd-border-secondary

         **Polack, P., Altché, F., d'Andréa-Novel, B. and de La Fortelle, A.
         (2017)**

         "The Kinematic Bicycle Model: A Consistent Model for Planning
         Feasible Trajectories for Autonomous Vehicles?". *2017 IEEE
         Intelligent Vehicles Symposium (IV)*, 812 to 818.
         doi:10.1109/IVS.2017.7995816.

         Quoted in "Know Where the Model Stops": keep the sideways
         acceleration "lower than 0.5 μg". Also used in the "More detail"
         box "The Dynamic Bicycle Model": the combined-slip tire model and
         the friction circle.

      .. grid-item-card:: Kinematic and dynamic vehicle models
         :link: https://doi.org/10.1109/IVS.2015.7225830
         :class-card: sd-border-secondary

         **Kong, J., Pfeiffer, M., Schildbach, G. and Borrelli, F. (2015)**

         "Kinematic and Dynamic Vehicle Models for Autonomous Driving
         Control Design". *2015 IEEE Intelligent Vehicles Symposium (IV)*,
         1094 to 1099. doi:10.1109/IVS.2015.7225830.

         Quoted in "Know Where the Model Stops": an MPC built on this model
         gives "0.41 m mean error" without "consideration slip, such as a
         dynamic bicycle model". Quoted again in "Look Ahead, Then Act: the
         Idea of MPC": MPC "can handle Multi-Input Multi-Output systems".

      .. grid-item-card:: Ackermann and bicycle model figures
         :link: https://thomasfermi.github.io/Algorithms-for-Automated-Driving/Control/BicycleModel.html
         :class-card: sd-border-secondary

         **Theers, M. and Singh, M. (2026)**

         *Algorithms for Automated Driving: Kinematic Bicycle Model.*
         Figures used under the Creative Commons Attribution 4.0
         International License. Accessed 9 November 2026.

         The Ackermann and bicycle model figures in "Turn Four Wheels About
         One Point" and "Collapse Four Wheels into Two". Also listed as a
         resource in the "More detail" box "More Equations, Parameters".


.. dropdown:: Pure Pursuit
   :class-container: sd-border-secondary
   :open:

   Pure Pursuit's steering law.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Pure Pursuit
         :class-card: sd-border-secondary

         **Coulter, R. C. (1992)**

         *Implementation of the Pure Pursuit Path Tracking Algorithm.*
         Technical report CMU-RI-TR-92-01, Robotics Institute, Carnegie
         Mellon University, Pittsburgh, PA.

         Quoted in "Chase a Point Ahead": Coulter's implementation of
         pursuit guidance. Also used in the "More detail" box "Why
         κ = 2 sin α / L_d": the curvature of the arc through the goal
         point in Coulter's form, :math:`\kappa = 2 g_y / L_d^2`.


.. dropdown:: Stanley
   :class-container: sd-border-secondary
   :open:

   The Stanford team's steering law and its gain :math:`k_s`.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Stanley, the robot
         :link: https://doi.org/10.1002/rob.20147
         :class-card: sd-border-secondary

         **Thrun, S. et al. (2006)**

         "Stanley: The Robot that Won the DARPA Grand Challenge". *Journal
         of Field Robotics*, 23(9), 661 to 692. doi:10.1002/rob.20147.

         Quoted in "Correct Heading and Offset Together": Stanley's top
         speed in the race, "38.0 mph", at "a rate of 20 Hz". The steering
         law of Stanford's car, with the lecture's own signs. Also used in
         the "More detail" box "One Stanley Step by Hand": the sideways
         speed :math:`\dot e = v\sin\delta`, as Thrun et al. write it.

      .. grid-item-card:: The gain k_s
         :link: https://doi.org/10.1109/ACC.2007.4282788
         :class-card: sd-border-secondary

         **Hoffmann, G. M., Tomlin, C. J., Montemerlo, M. and Thrun, S.
         (2007)**

         "Autonomous Automobile Trajectory Tracking for Off-Road Driving:
         Controller Design, Experimental Validation and Racing". *2007
         American Control Conference*, 2296 to 2301. IEEE.
         doi:10.1109/ACC.2007.4282788.

         Quoted in "Steer from the Front Axle": :math:`k_s` = 1 m/s, which
         the authors found "appropriate" in experiments (p. 2299).


.. dropdown:: MPC
   :class-container: sd-border-secondary
   :open:

   Autoware's MPC steering controller.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Autoware's MPC lateral controller
         :link: https://autowarefoundation.github.io/autoware_universe/main/control/autoware_mpc_lateral_controller/
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *autoware_mpc_lateral_controller.* Accessed 14 October 2026.

         Used only in the "More detail" box "One MPC Step on Our Turn,
         Drawn...": Autoware's steering controller tracks the path with a
         linear MPC, built by linearizing the model around the path.


.. dropdown:: Longitudinal Control
   :class-container: sd-border-secondary
   :open:

   Autoware's longitudinal PID, and a factory ACC's two-layer split.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: A factory ACC's two-layer split
         :class-card: sd-border-secondary

         **Zhou, H., Zhou, A., Li, T., Chen, D., Peeta, S. and Laval, J.
         (2021)**

         "Significance of Low-level Controller for String Stability under
         Adaptive Cruise Control". arXiv:2104.07726.

         Quoted in "Split Speed Control in Two Layers": a factory ACC's
         "planner model is usually a linear controller or an MPC more
         recently".

      .. grid-item-card:: Autoware's longitudinal PID
         :link: https://github.com/autowarefoundation/autoware_universe/tree/main/control/autoware_pid_longitudinal_controller
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *autoware_pid_longitudinal_controller.* Accessed 9 November 2026.

         Quoted in "Hold the Speed with Two Pedals": the gas pedal and
         brake "typically has a delay of about a hundred millisecond".
         Quoted again in "Split Speed Control in Two Layers": PID was
         chosen "from the viewpoint of trade-off between
         development/maintenance cost and performance".


.. rubric:: Map data and images

The road in every top view is CARLA's ``Town03.xodr``, read offline with the
CARLA Python API (`carla.org <https://carla.org>`_). The vehicle icon in the
figures was created by Stone from the `Noun Project
<https://thenounproject.com>`_. The Ackermann and bicycle model figures are
from Theers and Singh (2026), CC BY 4.0.
