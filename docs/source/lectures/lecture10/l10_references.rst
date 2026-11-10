====================================================
References
====================================================

These are the sources of the L10 deck, grouped by the lecture's sections, in
the order the lecture first uses each one. A source used in several
sections is listed once, where the lecture first uses it. Three sources are
quoted only in a "More detail" box of the lecture; their cards say so. One
source is used only in the appendix (:doc:`l10_appendix`); it has its own
group at the end. The deck also lists four background sources that no slide
quotes; each sits in the section its subject belongs to, and its card says
so.


.. dropdown:: Scaling the Behavior Layer
   :class-container: sd-border-secondary
   :open:

   Statecharts, behavior trees, and how real stacks organize their behavior
   layer.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Statecharts: superstates and parallel regions
         :class-card: sd-border-secondary

         **Harel, D. (1987)**

         "Statecharts: A Visual Formalism for Complex Systems". *Science of
         Computer Programming*, 8, 231 to 274.

         Why one flat FSM grows too fast: "two components with one thousand
         states each would result in one million states in the product".
         Superstates, "the main way statecharts economize in the number of
         arrows". Orthogonal (parallel) regions that talk by broadcast.

      .. grid-item-card:: Behavior trees
         :link: https://ar5iv.arxiv.org/html/1709.00084
         :class-card: sd-border-secondary

         **Colledanchise, M. and Ögren, P. (2018)**

         *Behavior Trees in Robotics and AI: An Introduction.* Chapman &
         Hall/CRC. arXiv:1709.00084. Accessed 7 November 2026.

         The definition of a behavior tree, quoted in "Define a Behavior
         Tree". Ticks, the three statuses (Running, Success, Failure), and
         the Sequence, Fallback, Parallel and Decorator nodes, quoted in
         "Read a Behavior Tree". What a tree gains over an FSM (a "two-way
         control transfer", modular, reactive, reusable) and what it costs,
         quoted in "Choose a Tree Over an FSM".

      .. grid-item-card:: Nav2's behavior tree navigator
         :link: https://github.com/ros-navigation/navigation2/tree/main/nav2_bt_navigator
         :class-card: sd-border-secondary

         **Nav2 contributors (2026)**

         *nav2_bt_navigator and nav2_behavior_tree README files, and
         nav2_params.yaml.* Accessed 7 November 2026.

         Nav2, ROS 2's navigation stack, runs a behavior tree (the Scaling
         the Behavior Layer section's opening). In the "More detail" box
         "What real stacks use": the navigator reads a behavior tree from an
         XML file and "uses the Behavior-Tree.CPP library to dynamically
         create and execute the BT". Its default tree for driving to a pose
         is ``navigate_to_pose_w_replanning_and_recovery.xml``.

      .. grid-item-card:: Autoware's behavior path planner, older design
         :link: https://autowarefoundation.github.io/autoware.universe_planning/pr-5562/planning/behavior_path_planner
         :class-card: sd-border-secondary

         **Autoware Foundation (2023)**

         *behavior_path_planner (older documentation build, pull request
         5562).* Documentation build for pull request 5562, opened 13
         November 2023. Accessed 7 November 2026.

         Quoted only in the "More detail" box "What real stacks use". The
         planner once ran its modules from a behavior tree, chosen for its
         "high scalability compared to the state machine".

      .. grid-item-card:: Autoware's Planner Manager
         :link: https://autowarefoundation.github.io/autoware_universe/main/planning/behavior_path_planner/autoware_behavior_path_planner/
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *autoware_behavior_path_planner: Planner Manager design.* Accessed
         7 November 2026.

         Used only in the "More detail" box "What real stacks use". Today a
         Planner Manager runs the modules: candidate modules run in parallel
         until they are approved, and approved modules run in series.

      .. grid-item-card:: Apollo's scenarios and stages
         :link: https://github.com/ApolloAuto/apollo/blob/master/modules/planning/planning_interface_base/scenario_base/scenario.h
         :class-card: sd-border-secondary

         **Apollo Auto (2026)**

         *Apollo planning: scenario.h and scenario_manager.cc.* Accessed 7
         November 2026.

         Quoted only in the "More detail" box "What real stacks use". Apollo
         plans by scenarios made of stages. Each scenario has its own
         transfer condition, and the result of each stage "determines the
         transition from one stage to another".


.. dropdown:: Bicycle Model
   :class-container: sd-border-secondary
   :open:

   Kinematic and dynamic vehicle models.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Kinematic and dynamic vehicle models
         :link: https://doi.org/10.1109/IVS.2015.7225830
         :class-card: sd-border-secondary

         **Kong, J., Pfeiffer, M., Schildbach, G. and Borrelli, F. (2015)**

         "Kinematic and Dynamic Vehicle Models for Autonomous Driving
         Control Design". *2015 IEEE Intelligent Vehicles Symposium (IV)*,
         1094 to 1099. doi:10.1109/IVS.2015.7225830.

         Background reading: the deck lists this paper, and no slide quotes
         it.


.. dropdown:: Trajectories
   :class-container: sd-border-secondary
   :open:

   Trajectory generation.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Trajectories in the Frenet frame
         :link: https://doi.org/10.1109/ROBOT.2010.5509799
         :class-card: sd-border-secondary

         **Werling, M., Ziegler, J., Kammel, S. and Thrun, S. (2010)**

         "Optimal Trajectory Generation for Dynamic Street Scenarios in a
         Frenét Frame". *2010 IEEE International Conference on Robotics and
         Automation (ICRA)*, 987 to 993. doi:10.1109/ROBOT.2010.5509799.

         Background reading: the deck lists this paper, and no slide quotes
         it.


.. dropdown:: Speed Control
   :class-container: sd-border-secondary
   :open:

   Feedback control.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Feedback systems
         :class-card: sd-border-secondary

         **Åström, K. J. and Murray, R. M. (2021)**

         *Feedback Systems: An Introduction for Scientists and Engineers*,
         2nd edition. Princeton University Press. ISBN 978-0-691-19398-4.

         Background reading: the deck lists this book, and no slide quotes
         it.


.. dropdown:: Pure Pursuit
   :class-container: sd-border-secondary
   :open:

   The lookahead trade-off, Autoware's Pure Pursuit controller, and CARLA's
   vehicle command.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Steering methods compared
         :class-card: sd-border-secondary

         **Snider, J. M. (2009)**

         *Automatic Steering Methods for Autonomous Automobile Path
         Tracking.* Technical report CMU-RI-TR-09-08, Robotics Institute,
         Carnegie Mellon University, Pittsburgh, PA.

         The lookahead trade-off, in the lecture's own words: a short
         lookahead tracks the path more closely, a long one drives more
         smoothly.

      .. grid-item-card:: Autoware's Pure Pursuit controller
         :link: https://autowarefoundation.github.io/autoware_universe/main/control/autoware_pure_pursuit/
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *autoware_pure_pursuit.* Accessed 14 October 2026.

         Autoware offers a Pure Pursuit steering controller, beside its MPC
         one (see "Weigh MPC" in the lecture).

      .. grid-item-card:: CARLA's vehicle command
         :link: https://carla.readthedocs.io/en/latest/python_api/
         :class-card: sd-border-secondary

         **CARLA Team (2026)**

         *Python API Reference: carla.VehicleControl.* Accessed 14 October
         2026.

         The command CARLA takes for steering, throttle and brake. In
         "Step 4: Turn the Arc into a Steering Command", CARLA's steer is
         positive to the right, so the node that steps CARLA flips the sign
         of ``VehicleCmd``'s steer.


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

         The steering law of Stanford's DARPA Grand Challenge car. The paper
         writes the cross-track term with a plus sign, with its own signs;
         the lecture subtracts it, with steering and :math:`e` positive to
         the left. Also used in Going Further, "Why the Cross-Track Term
         Pulls e to Zero": the sideways speed
         :math:`\dot e = v\sin\delta`, as Thrun et al. write it.

      .. grid-item-card:: The gain k_s
         :link: https://doi.org/10.1109/ACC.2007.4282788
         :class-card: sd-border-secondary

         **Hoffmann, G. M., Tomlin, C. J., Montemerlo, M. and Thrun, S.
         (2007)**

         "Autonomous Automobile Trajectory Tracking for Off-Road Driving:
         Controller Design, Experimental Validation and Racing". *2007
         American Control Conference*, 2296 to 2301. IEEE.
         doi:10.1109/ACC.2007.4282788.

         :math:`k_s` = 1 m/s: the authors found 1 m/s "appropriate" in
         experiments (p. 2299).


.. dropdown:: MPC
   :class-container: sd-border-secondary
   :open:

   Autoware's MPC steering controller, and a textbook on MPC.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Autoware's MPC lateral controller
         :link: https://autowarefoundation.github.io/autoware_universe/main/control/autoware_mpc_lateral_controller/
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *autoware_mpc_lateral_controller.* Accessed 14 October 2026.

         Autoware's steering controller that tracks the path with a linear
         MPC. Also used in Going Further, "The Problem Written Out": with
         the model linearized around the path and a squared score, each step
         is a quadratic program.

      .. grid-item-card:: Model predictive control
         :class-card: sd-border-secondary

         **Rawlings, J. B., Mayne, D. Q. and Diehl, M. M. (2017)**

         *Model Predictive Control: Theory, Computation, and Design*, 2nd
         edition. Nob Hill Publishing. ISBN 978-0-9759377-3-0.

         Background reading: the deck lists this book, and no slide quotes
         it.


.. dropdown:: Used Only in the Appendix
   :class-container: sd-border-secondary

   Pure Pursuit's original form, from :doc:`l10_appendix`.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Pure Pursuit
         :class-card: sd-border-secondary

         **Coulter, R. C. (1992)**

         *Implementation of the Pure Pursuit Path Tracking Algorithm.*
         Technical report CMU-RI-TR-92-01, Robotics Institute, Carnegie
         Mellon University, Pittsburgh, PA.

         The curvature of the arc through the goal point in Coulter's form,
         :math:`\kappa = 2 g_y / L_d^2`, used in "Pure Pursuit's Arc" on the
         Going Further page.


.. rubric:: Map data and images

The road in every top view is CARLA's ``Town03.xodr``, read offline with the
CARLA Python API (`carla.org <https://carla.org>`_). The vehicle icon in the
figures was created by Stone from the `Noun Project
<https://thenounproject.com>`_.
