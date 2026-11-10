====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L10, the slides shown in class and
   the reading slide that goes with them, in the same order and with the
   same sections. You can read them at home. Four worked steps that were cut
   from class for time sit in closed **More detail** boxes, right after the
   part they explain; they are not on the quiz. The deck keeps more material
   in its appendix, on :doc:`the appendix page <l10_appendix>`, "Going
   Further":

   - why :math:`\tan\delta = L/R` in the bicycle model, and where the model
     stops holding;
   - the quintic's six conditions, and its six equations for our slow-down;
   - why Pure Pursuit's arc has curvature :math:`2\sin\alpha / L_d`;
   - one Stanley step by hand, which axle stays on the path, Pure Pursuit
     against Stanley, and why the cross-track term pulls the error to zero;
   - one MPC step on our turn, drawn, and the optimization problem written
     out.

   The papers and pages behind these notes are listed on :doc:`the
   References page <l10_references>`.


.. _l10-lec-introduction:

Introduction
------------

The local planner's output is a **path**: map points :math:`(x, y)` for the
next 70 m, planned again every 0.5 s. The behavior layer above it decides
which lanes the AV may use, where it must stop, and a speed limit. A path
says only where the AV should go, not how fast or when. Today we give the
path a speed and a time, then turn it into steering, throttle and brake.

.. figure:: /_static/images/L10/l10_stack.png
   :alt: A block diagram of four boxes in a row joined by arrows: Route planner (L7), Behavior layer (L9), Local planner (L9) and Controller (L10, today); only the controller box is green. Under the arrows: lanes to follow, a task, a path for the next seconds, and, after the controller, steering, throttle, brake. Above, a box Pose feeds the route planner, a box Pose, objects, predictions feeds the behavior layer and the local planner, and a box Pose, speed feeds the controller.
   :width: 95%
   :align: center

   The four layers, and today's layer: the controller.

.. admonition:: Reading the figure
   :class: tip

   Read the row left to right. Each arrow carries what one layer hands to
   the next. Each box names the lecture that covers its layer.

   - The **route planner** (L7) reads the pose and hands on the lanes to
     follow.
   - The **behavior layer** (L9) reads the pose, the objects and their
     predictions, and hands on a task.
   - The **local planner** (L9) reads the same inputs and hands on a path
     for the next seconds.
   - The **controller** (L10, today, green) reads the pose and the speed,
     and turns the path into steering, throttle and brake.


.. _l10-lec-controller-node:

Today's Two Controllers: One Node, Five Inputs, One Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/controller_io.png
   :alt: A block diagram. A green block labeled controller_node holds two boxes: steering, Pure Pursuit, and speed, PID. Five ROS topics come in on the left, each with what it carries: /planning/path, the route planner's lane path; /localization/odom, the pose, which the node moves 1.4 meters back to the rear axle; /carla/imu/data, the turn rate, for the heading; /carla/speedometer, the speed the PID uses; /behavior/target_speed, the speed to hold. One output on the right: /control/vehicle_cmd, with steer from minus 1 to 1, positive left, throttle and brake, to the node that steps CARLA.
   :width: 95%
   :align: center

   The controller node: its inputs and its command.

.. admonition:: Reading the figure
   :class: tip

   - **Left, five inputs (ROS topics):** ``/planning/path``, the route
     planner's lane path; ``/localization/odom``, the pose, which the node
     moves 1.4 m back to the rear axle; ``/carla/imu/data``, the turn rate,
     for the heading; ``/carla/speedometer``, the speed the PID uses;
     ``/behavior/target_speed``, the speed to hold.
   - **Middle, green:** ``controller_node``, with two parts: the steering
     (Pure Pursuit) and the speed (PID).
   - **Right, one output:** ``/control/vehicle_cmd``, with a steer from −1
     to 1 (positive left), a throttle and a brake. It goes to the node that
     steps CARLA.

- The node holds two parts: **Pure Pursuit** for the steering and a **PID**
  for the speed. Today: how each one works, by hand and in simulation.
- A separate node steps CARLA every 0.05 s and waits for this node's command
  before each step (the lock step). So the controller runs 20 times a
  second; our simulation uses the same rate.


.. _l10-lec-messages:

Know What Each Topic Carries: the Message Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal is to know which fields of each message the controller reads, and
which it writes.

.. list-table::
   :widths: 30 30 40
   :header-rows: 1
   :class: compact-table

   * - **Topic**
     - **Message type**
     - **Main fields used**
   * - ``/planning/path``
     - ``nav_msgs/Path``
     - ``poses[i].pose.position``: the path's points :math:`(x, y)`, in m
   * - ``/localization/odom``
     - ``nav_msgs/Odometry``
     - ``pose.pose``: the position :math:`(x, y)` and the heading
   * - ``/carla/imu/data``
     - ``sensor_msgs/Imu``
     - ``angular_velocity.z``: the turn rate, in rad/s
   * - ``/carla/speedometer``
     - ``geometry_msgs/TwistStamped``
     - ``twist.linear.x``: the speed, in m/s
   * - ``/behavior/target_speed``
     - ``geometry_msgs/TwistStamped``
     - ``twist.linear.x``: the speed to hold, in m/s
   * - ``/control/vehicle_cmd`` (output)
     - ``ads_msgs/VehicleCmd``
     - ``throttle`` 0 to 0.75, ``steer`` −1 to 1 (positive turns left),
       ``brake`` 0 to 1

Each ``/behavior/target_speed`` message starts one control step: the node
answers it with one ``VehicleCmd`` that carries the same time stamp.


.. _l10-lec-topics-demo:

See the Five Inputs Live: CARLA on Autopilot in Town03
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal is to see what each input topic carries while the AV drives. The
package is ``l10_topics_demo`` in the course's ROS repository (`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l10_topics_demo/README.md>`__).

.. code-block:: bash

   ros2 launch l10_topics_demo l10_topics.launch.py
   ros2 topic echo /behavior/target_speed --once     # in a second terminal

One message on each topic, from our run:

.. list-table::
   :widths: 30 52 18
   :header-rows: 1
   :class: compact-table

   * - **Topic**
     - **One message, from our run**
     - **Per second**
   * - ``/planning/path``
     - 51 points: the lane center, 50 m ahead
     - 2
   * - ``/localization/odom``
     - :math:`x` = 22.19 m, :math:`y` = 4.67 m; forward speed 8.04 m/s
     - 20
   * - ``/carla/imu/data``
     - ``angular_velocity.z`` = 0.234 rad/s, in a curve
     - 20
   * - ``/carla/speedometer``
     - ``twist.linear.x`` = 8.05 m/s
     - 20
   * - ``/behavior/target_speed``
     - ``twist.linear.x`` = 8.33 m/s: the road's 30 km/h limit, 30 / 3.6
     - 20

The demo uses stand-ins: the pose is CARLA's truth, the target speed is the
speed limit, and the path is the lane center ahead. Nothing publishes
``/control/vehicle_cmd``: the autopilot drives.


.. _l10-lec-two-controllers:

Follow the Path at the Right Speed: Two Controllers Side by Side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Feedback controller
   :class: note

   A program that, at every cycle, compares what the AV should be doing with
   what it measures it is doing, and sends a command that shrinks the
   difference.

.. list-table::
   :widths: 22 43 35
   :header-rows: 1
   :class: compact-table

   * -
     - **Lateral (steering)**
     - **Longitudinal (speed)**
   * - Should be
     - on the path
     - at the profile's speed
   * - Measures
     - distance and angle to the path
     - speed
   * - Sends
     - a steering angle
     - throttle or brake
   * - Today
     - Pure Pursuit, Stanley, MPC
     - PID


.. _l10-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

This is a reading slide in the deck. After this lecture, you can:

1. say why one flat FSM grows too fast, and how a **superstate**, parallel
   regions and a **behavior tree** keep the behavior layer small;
2. write the **kinematic bicycle model** and find the steering angle that follows a curvature;
3. give a path a speed profile and a time (a **trajectory**), and say why a
   quintic speed change keeps the **jerk** small;
4. read a **PID** speed response: what P, I and D each do, what **windup**
   is and how clamping stops it;
5. work **Pure Pursuit**'s geometry by hand, from the lookahead circle to
   the steering angle;
6. predict how the **lookahead distance** changes Pure Pursuit, and compare
   it with **Stanley**;
7. say what **MPC** adds: a model, a horizon, limits, and only the first
   input applied.


.. _l10-lec-behavior:

Scaling the Behavior Layer
--------------------------

The previous lecture showed one finite state machine (FSM) for a valet that
parks itself in a garage. Here we use the same tools on an AV that drives
city streets.

**In this section:** two parts. Finite State Machines: five road behaviors
and a safety monitor need 5 × 3 = 15 states in one flat FSM; a superstate
and parallel regions bring that down. Behavior Trees: what a tree is, what
it gains over an FSM, our road behaviors as a tree, and a Python script that
builds and runs it.

**What it is for:** real stacks face the same growth: Nav2, ROS 2's
navigation stack, runs a behavior tree (Nav2 contributors). The behavior
layer's output, such as a target speed, is the input to the rest of today.


.. _l10-lec-fsm:

Finite State Machines
~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Finite state machine (FSM)
   :class: note

   A fixed list of **states**, of which the system is in exactly one at a
   time, and a list of **transitions**: each one moves the system from one
   state to another when its condition becomes true.


.. _l10-lec-flat-fsm:

Step 1, the Problem: One Flat FSM Multiplies Its States
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to see why one flat FSM grows too fast. Our AV drives city
streets with five behaviors: Lane keep, Follow a slower car, Change lane,
Stop at the line and Cross the intersection. A safety monitor adds three
states: Nominal, Caution, Emergency. Both lists are chosen for this example.
The AV is in one behavior and one monitor state at once, so one flat FSM
needs a state for every pair: 5 × 3 = 15.

.. figure:: /_static/images/L10/beh_flat.png
   :alt: A grid of 15 rounded boxes in three rows and five columns. Each box names one road behavior and one monitor state: the columns are Lane keep, Follow, Change lane, Stop at line and Cross, the rows Nominal, Caution and Emergency. Three orange arrows go from Lane keep to Follow, one in each row; dark tag 1 marks the top one. Five blue arrows go down from each Nominal box to the Caution box below it; dark tag 2 marks the leftmost one.
   :width: 85%
   :align: center

   The road behaviors and the monitor as one flat FSM: 15 states.

.. admonition:: Reading the figure
   :class: tip

   Each box is one state of the flat FSM: a road behavior (the column: Lane
   keep, Follow, Change lane, Stop at line, Cross) paired with a monitor
   state (the row: Nominal, Caution, Emergency).

   - **Tag 1:** Lane keep to Follow, drawn once per monitor state: 3 arrows
     (orange).
   - **Tag 2:** the monitor's Nominal to Caution, drawn once per behavior:
     5 arrows (blue).

.. important::

   Harel: "two components with one thousand states each would result in one
   million states in the product" (Harel, 1987). That is
   1000 × 1000 = 1,000,000.


.. _l10-lec-superstate:

Step 2, Fewer Arrows: One Superstate Arrow Replaces Five
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to add an emergency stop without an arrow from every state. The
AV must be able to stop from any of its five behaviors, so one flat FSM
needs 5 arrows to Emergency stop.

.. figure:: /_static/images/L10/beh_hier.png
   :alt: A state diagram. A large green rounded box labeled Driving, dark tag 1 at its top-left corner, holds five states: Lane keep, Follow and Change lane in a top row, Stop at the line and Cross the intersection below. An arrow from the left enters Lane keep. Lane keep and Follow go to each other; Follow goes to Change lane; Change lane goes back to Lane keep by an arc over the top. Lane keep goes down to Stop at the line, which goes to Cross the intersection, which goes back up to Lane keep. One red arrow, dark tag 2, leaves the bottom edge of the Driving box and goes down to Emergency stop.
   :width: 75%
   :align: center

   The road behaviors inside the superstate Driving.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** the **superstate** Driving, a state that holds the five
     behaviors (green box). Their own arrows stay as they were: Lane keep
     and Follow go to each other, Follow goes to Change lane and back to
     Lane keep, and Lane keep goes to Stop at the line, then to Cross the
     intersection, then back to Lane keep.
   - **Tag 2:** one arrow (red) leaves Driving for Emergency stop. It stands
     for 5 arrows, one from each state inside.

.. important::

   Harel lets a transition that leaves a superstate stand for that
   transition leaving every state inside it: "the main way statecharts
   economize in the number of arrows" (Harel, 1987).


.. _l10-lec-parallel:

Step 3, Fewer States: Parallel Regions Add Instead of Multiply
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to keep the road behaviors and the monitor as two small
machines. One state holds two **parallel regions**, and the AV is in one
state of each at the same time: 5 + 3 = 8 states drawn, instead of 15.

.. figure:: /_static/images/L10/beh_parallel.png
   :alt: A rounded green box split by a vertical dashed line into two regions. Left, dark tag 1: the five road behaviors with the same arrows as in the Driving box, Lane keep, Follow and Change lane on top, Stop at the line and Cross the intersection below, and an arrow from the left entering Lane keep. Right, dark tag 2: Nominal, entered from above, and Caution go to each other, and Caution goes down to Emergency. A red dashed arrow goes from Emergency left across the dashed line into the road region; dark tag 3 sits above it.
   :width: 95%
   :align: center

   The road behaviors and the monitor as two parallel regions: 8 states.

.. admonition:: Reading the figure
   :class: tip

   One state (the green box) holds two regions, split by the dashed line.

   - **Tag 1:** the road region, with the five behaviors and their arrows.
   - **Tag 2:** the safety monitor region: Nominal, Caution, Emergency.
   - **Tag 3:** Emergency sends an event (red dashed arrow); the road region
     senses it and stops the AV. That reaction is our choice for this
     example.

.. important::

   Harel calls these regions orthogonal and lets them talk by broadcast:
   "One part generates an event ... and all other parts sense it, acting in
   response if so specified" (Harel, 1987).


.. _l10-lec-bt:

Behavior Trees
~~~~~~~~~~~~~~

A behavior tree has no arrows between behaviors: at every tick it checks its
conditions again and runs the first branch that does not fail. We read its
parts, compare it with an FSM, and build our road tree in Python.


.. _l10-lec-bt-def:

Define a Behavior Tree: a Root, Control Nodes and Leaves
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to name the parts of a behavior tree before we read one.

.. admonition:: Definition: Behavior tree (BT)
   :class: note

   "A directed rooted tree where the internal nodes are called control flow
   nodes and leaf nodes are called execution nodes" (Colledanchise and
   Ögren, 2018).

In plain words, with our road behaviors:

- The **root** is the one node with no parent. Every tick starts there.
- **Control flow nodes**, such as Sequence and Fallback, sit inside the tree
  and decide which child is ticked next.
- A **Condition** leaf checks a fact and returns Success or Failure: a stop
  line within 30 m, a car ahead within 40 m.
- An **Action** leaf runs a behavior: "While the action is ongoing it
  returns Running". Ours: Lane keep, Follow, Change lane, Stop at the line.


.. _l10-lec-bt-read:

Read a Behavior Tree: Ticks, Three Statuses, Four Node Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to learn how a tree runs. A **tick** goes down from the root: "A
node is executed if and only if it receives ticks". A ticked node returns
Running, Success or Failure (Colledanchise and Ögren, 2018).

.. list-table::
   :widths: 15 30 55
   :header-rows: 1
   :class: compact-table

   * - **Node**
     - **In plain words**
     - **In Colledanchise and Ögren's words**
   * - Sequence (→)
     - run the children in order; stop at the first that fails or runs
     - "routing the ticks to its children from the left until it finds a
       child that returns either Failure or Running"; "It returns Success if
       and only if all its children return Success".
   * - Fallback (?)
     - try the children in order; stop at the first that succeeds or runs
     - "routing the ticks to its children from the left until it finds a
       child that returns either Success or Running"; "It returns Failure if
       and only if all its children return Failure".
   * - Parallel
     - tick every child; count successes and failures
     - "routing the ticks to all its children": Success when :math:`M` of
       the :math:`N` children succeed, Failure when :math:`N - M + 1` fail
       (:math:`M` set by the user)
   * - Decorator
     - one child, with a rule on top
     - "a control flow node with a single child that manipulates the return
       status of its child according to a user-defined rule"


.. _l10-lec-bt-choose:

Choose a Tree Over an FSM: a Change Stays in One Branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to see what a tree gains over an FSM, and what it costs
(Colledanchise and Ögren, 2018).

- An FSM's arrow hands control to the next state for good: a "one-way
  control transfer". Remove Change lane, and the arrows into and out of it
  must change.
- A tree's parent ticks a child and gets a status back, as from a function
  call: a "two-way control transfer". Remove the pass branch, and nothing
  else changes.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **What a tree gains**
     - **What it costs**
   * - Modular: "each subtree of a BT can be seen as a module"
     - "Checking all the conditions can be expensive": every tick checks
       again from the root
   * - Reactive: a car that enters the left lane changes the behavior at the
       next tick
     - "The BT engine can be complex to implement", but a library does it
       once
   * - Reusable: "any subtree can be reused in multiple places of a BT"
     - It needs "a new mindset": think in conditions, not in states


.. _l10-lec-road-bt:

Pass a Slow Car or Follow It: Four Road Behaviors as a Behavior Tree
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to write four of the road behaviors as a tree. The root
Fallback (?) tries its branches from the left: stop for a line, pass a slow
car, follow a car, keep the lane. Ellipses are conditions, gray boxes are
actions; each tag is one condition, with thresholds chosen for this example.

.. figure:: /_static/images/L10/beh_road_bt.png
   :alt: A behavior tree. The root, a Fallback box marked with a question mark, has four children from left to right: three Sequence boxes marked with an arrow, and a gray action box, Lane keep. The first Sequence holds condition 1, an ellipse with dark tag 1, and the action Stop at the line. The second holds conditions 2 and 3 and the action Change lane. The third holds condition 4 and the action Follow.
   :width: 90%
   :align: center

   Four road behaviors as a behavior tree.

.. admonition:: Reading the figure
   :class: tip

   The root is a Fallback (box with a question mark). Its children, from
   left to right: a Sequence (box with an arrow) of condition 1 and Stop at
   the line; a Sequence of conditions 2 and 3 and Change lane; a Sequence
   of condition 4 and Follow; and the action Lane keep.

   - **Tag 1:** a stop line is within 30 m ahead.
   - **Tag 2:** the car ahead has driven under 6 m/s for 3 s.
   - **Tag 3:** the left lane is free: no car within 30 m behind or 40 m
     ahead.
   - **Tag 4:** a car is ahead in our lane, within 40 m.

Cross the intersection is left out to keep the tree small.


.. _l10-lec-bt-ticks:

Switch Behaviors with No Arrow: a Car in the Left Lane Stops the Pass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to watch the tree switch behaviors with no arrow, at two ticks
chosen for this example. The root ticks every 0.1 s (chosen); each tick
checks the conditions again from the left, and the first branch that does
not fail picks the action.

.. list-table::
   :widths: 50 25 25
   :header-rows: 1
   :class: compact-table

   * - **Condition**
     - **Tick 1**
     - **Tick 2**
   * - 1: a stop line within 30 m
     - no
     - no
   * - 2: the car ahead under 6 m/s for 3 s
     - yes: 5 m/s
     - yes
   * - 3: the left lane free
     - yes
     - no: a car 20 m behind
   * - 4: a car ahead within 40 m
     - yes: 25 m
     - yes
   * - The tree runs
     - Change lane
     - Follow

No arrow goes from Change lane to Follow: at tick 2, condition 3 fails, so
the second Sequence fails, and the Fallback moves on to the third branch,
Follow. Tick 2 comes before the AV has left its lane.


.. _l10-lec-bt-python-1:

Build a Tree in Python, Step 1: a Node Is a Class with tick()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to write the control nodes in plain Python, with no CARLA and no
ROS. The script is ``behavior_tree.py`` in folder ``lecture10`` of the
course's Python repository (`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture10>`__).

.. code-block:: python
   :linenos:
   :lineno-start: 44
   :emphasize-lines: 10,12

   class Sequence:
       """Stops at the first child that does not succeed."""

       def __init__(self, *children):
           self.children = children

       def tick(self, world):
           for child in self.children:
               status = child.tick(world)
               if status != SUCCESS:
                   return status
           return SUCCESS

Lines 53 and 55: a Sequence passes on the first status that is not Success,
and succeeds only if every child does. ``Fallback`` is the same class with
Success and Failure swapped in those two lines.


.. _l10-lec-bt-python-2:

Build a Tree in Python, Step 2: the Pass Branch, Then a Run
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to build our road tree from those nodes and tick it at five
moments of a drive (times and readings chosen). Tags 2 and 3 are the
conditions of the tree above.

.. code-block:: python
   :linenos:
   :lineno-start: 78

       pass_car = Sequence(
           Condition(2, "car ahead under 6 m/s for 3 s",
                     lambda w: w["slow_for_s"] >= 3),
           Condition(3, "left lane free",
                     lambda w: w["left_free"]),
           Action("Change lane"))

.. code-block:: console

   $ python3 behavior_tree.py
   t = 0.0 s  Lane keep         checked: 1 no, 2 no, 4 no
   t = 2.0 s  Follow            checked: 1 no, 2 no, 4 yes
   t = 4.0 s  Change lane       checked: 1 no, 2 yes, 3 yes
   t = 4.1 s  Follow            checked: 1 no, 2 yes, 3 no, 4 yes
   t = 9.0 s  Stop at the line  checked: 1 yes

A tick lists only the conditions it reached: at 9.0 s the stop line wins and
nothing else is checked. With ``--no-pass``, the 4.0 s tick stays on
Follow.

.. dropdown:: More detail: what real stacks use, and what they hand down
   :class-container: more-detail
   :icon: info

   Real driving and robot stacks use these structures:

   - **Nav2**, ROS 2's navigation stack: its navigator reads a behavior tree
     from an XML file and "uses the Behavior-Tree.CPP library to dynamically
     create and execute the BT" (Nav2 contributors). The default tree for
     driving to a pose is
     ``navigate_to_pose_w_replanning_and_recovery.xml``.
   - **Autoware**'s behavior path planner once ran its modules from a
     behavior tree, chosen for its "high scalability compared to the state
     machine" (Autoware Foundation, older documentation). Today a Planner
     Manager runs them: candidate modules run in parallel until they are
     approved, and approved modules run in series (Autoware Foundation,
     current documentation).
   - **Apollo** plans by scenarios made of stages: each scenario has its own
     transfer condition, and the result of each stage "determines the
     transition from one stage to another" (Apollo Auto, ``scenario.h``).

   Whichever structure picks the behavior, its output is a maneuver, a
   target lane, a speed or a stop point. That output is the input to the
   rest of today.


.. _l10-lec-turn:

The Turn
--------

The behavior layer picks a behavior and a target speed for it, for example
8 m/s to keep the lane and 0 to stop at the line (chosen). This section sets
that choice aside and builds the one example that both controllers,
steering and speed, run on.

**In this section:** we take one right turn in Town03, find its curvature,
and give it a speed profile.

**What it is for:** every controller today drives this same path, at the
same speeds, from the same start, so their results can be compared.


.. _l10-lec-test-path:

One Test Path for Every Controller: a Right Turn in Town03
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/turn_map.png
   :alt: A top view, x along the approach to the right and y to the left, in meters. A single lane 3.5 meters wide, drawn by two black edges with a gray dashed center line, runs 80 meters to the right, turns right through a quarter circle near x = 80 to 92, and runs 40 meters down. The AV is drawn at the start, at the left end, facing right. An arrow under the lane says driving direction. Dark round tags: tag 1 above the straight approach, tag 2 at the corner, which is shaded orange along the center line, tag 3 beside the exit going down.
   :width: 90%
   :align: center

   The test path: a right turn in Town03.

.. admonition:: Reading the figure
   :class: tip

   A top view in meters, drawn turned so the approach points along
   :math:`x`; :math:`y` points to the left. The lane is 3.5 m wide; the
   dashed line is its center. The AV starts at the left end, facing right.

   - **Tag 1:** road 3, the 80 m approach.
   - **Tag 2:** road 817, the junction lane: 17.5 m, turning right by 91°
     (shaded orange).
   - **Tag 3:** road 19, the 40 m exit.

The lane was read from ``Town03.xodr`` with ``carla.Map``, with no CARLA
server running.

Our path is the lane center, as the route planner gives it. Our controller
follows that path, with no local planner in between.


.. _l10-lec-curvature:

Measure How the Turn Bends: Its Curvature Jumps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Curvature
   :class: note

   How sharply a path bends at a point: :math:`\kappa = 1/R`, where
   :math:`R` is the radius of the circle that fits the path there. A
   straight road has :math:`\kappa = 0`.

.. figure:: /_static/images/L10/turn_curvature.png
   :alt: A graph, not a map: curvature in 1 per meter against the distance along the path from 0 to 137.5 meters. The curve is zero up to about 83 meters, jumps to 0.100 (dark tag 1), jumps again near 89.5 meters to 0.167 (dark tag 2), and drops back to zero near 95 meters. The junction lane, from 80 to 97.5 meters, is shaded orange.
   :width: 90%
   :align: center

   The curvature of the test path.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a map: the curvature against the distance :math:`s` along
   the path. The junction lane is shaded orange.

   - **Tag 1:** the first arc, :math:`\kappa` = 0.1000 /m, so
     :math:`R` = 1 / 0.1000 = 10.00 m.
   - **Tag 2:** the second arc, :math:`\kappa` = 0.1673 /m, so
     :math:`R` = 1 / 0.1673 = 5.98 m.

   Each change is a step, with no gradual part between.


.. _l10-lec-profile-1:

Speed Profile, Step 1: a Curve Caps the Speed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Lateral acceleration
   :class: note

   On a circle of radius :math:`R` at speed :math:`v`, the AV accelerates
   toward the circle's center by :math:`v^2 / R` (m/s²). The tires must push
   the AV sideways that hard; the faster or the tighter the curve, the
   harder.

We cap it at :math:`a_{\mathrm{lat}}` = 2.0 m/s² (chosen; the controller
node's ``a_lat``, a cap the node applies itself). From
:math:`v^2 / R \le a_{\mathrm{lat}}`, the highest speed in a curve is
:math:`v = \sqrt{a_{\mathrm{lat}} R}`:

1. First arc, :math:`R` = 10.00 m: :math:`\sqrt{2.0 \times 10.00}` =
   4.47 m/s.
2. Second arc, :math:`R` = 5.98 m: :math:`\sqrt{2.0 \times 5.98}` =
   3.46 m/s.
3. Everywhere else: 8 m/s, the target speed (chosen).

These caps are the speed limit at each point, the dotted line in the next
figure.


.. _l10-lec-profile-2:

Speed Profile, Step 2: Brake Before the Curve, Speed Up After It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/speed_profile.png
   :alt: A graph of speed in meters per second against the distance along the path. A dotted gray limit line sits at 8, drops to about 4.5 on the first arc and 3.46 on the second, and returns to 8. The blue profile holds 8, falls along a curve from about 72 meters (dark tag 1), holds 4.47 on the first arc (tag 2) and 3.46 on the second (tag 3), then rises back to 8 by about 112 meters (tag 4). The junction lane is shaded orange.
   :width: 85%
   :align: center

   The speed profile on the test path.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a map: the speed against the distance :math:`s` along the
   path. The dotted gray line is the limit from Step 1; the blue line is the
   profile. The junction lane is shaded orange.

   - **Tag 1:** braking, before the first arc.
   - **Tag 2:** the first arc's cap, 4.47 m/s.
   - **Tag 3:** the second arc's cap, 3.46 m/s.
   - **Tag 4:** speeding up again, after the second arc.

The AV cannot drop to 4.47 m/s at once: slowing from :math:`v_1` to
:math:`v_2` at a constant deceleration :math:`a` takes the distance
:math:`d = (v_1^2 - v_2^2) / (2a)`.

1. Braking (tag 1), at 2.0 m/s² (chosen; the node's ``a_brake``):
   :math:`d = (8^2 - 4.47^2) / (2 \times 2.0)` = 11.0 m. The first arc
   starts at :math:`s` = 83.2 m, so braking starts at 83.2 − 11.0 = 72.2 m.
2. Speeding up (tag 4), at 1.5 m/s² (chosen), from 3.46 m/s after the
   second arc ends at :math:`s` = 94.8 m:
   :math:`(8^2 - 3.46^2) / (2 \times 1.5)` = 17.3 m, so the AV is at 8 m/s
   again at 94.8 + 17.3 = 112.1 m.


.. _l10-lec-simulation:

Test Controllers Without CARLA: Our Simulation and Its Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every controller today drives this path in a numpy simulation of the
bicycle model (next section). The values:

.. list-table::
   :widths: 28 24 48
   :header-rows: 1
   :class: compact-table

   * - **Value**
     - **Number**
     - **From**
   * - Wheelbase :math:`L`
     - 2.875 m
     - chosen; a real vehicle has its own (2.3 to 3.0 m)
   * - Largest steering angle
     - 0.7 rad
     - chosen: the most the controller commands (``steer_limit``; the
       wheels can turn 1.222 rad)
   * - Steering: delay, then lag
     - 0.1 s, then 0.2 s
     - chosen: real steering is not instant
   * - Controller rate
     - 20 per second
     - set by the lock step
   * - Start
     - 1 m left of center, 8 m/s
     - chosen, to see the AV correct
   * - Speed model
     - see :ref:`Speed Control <l10-lec-speed>`
     - chosen

.. important::

   These are not CARLA's dynamics. The numbers show how each controller
   behaves; tune the gains on CARLA itself.


.. _l10-lec-bicycle:

Bicycle Model
-------------

The last section gave a path, its speed profile and a simulation to drive
them. This section keeps all three and opens up the simulation's model.

**In this section:** the kinematic bicycle model says where a steering angle
and a speed take the AV.

**What it is for:** every controller today predicts with this model, and our
simulation runs it.


.. _l10-lec-bicycle-def:

Predict the AV's Motion: the Bicycle Model, One Wheel per Axle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Kinematic bicycle model
   :class: note

   The AV's two front wheels merged into one, and its two rear wheels into
   one. The wheels roll without sliding sideways, so the AV turns about one
   point.

.. figure:: /_static/images/L10/bicycle_geom.png
   :alt: A drawing of the bicycle model. The rear wheel at dark tag 1 and the front wheel at dark tag 2 are short thick bars joined by a line of length L, tilted up to the right at angle theta from a dashed horizontal line. The front wheel is turned further left by the angle delta from the body line. Thin gray lines from both wheels, square to each wheel, meet far up and to the left at a green point, dark tag 3; a green double arrow labeled R runs from the rear wheel to that point. A dashed green arc leaves the rear wheel toward the front. A faint gray top view of the AV lies under the model, facing along the body line, with its rear axle on the rear wheel. Small x and y axes sit at the bottom left, off the car.
   :width: 55%
   :align: center

   The kinematic bicycle model, drawn over the AV.

.. admonition:: Reading the figure
   :class: tip

   The faint gray AV lies under the model, facing along the body line. The
   body line, of length :math:`L`, is turned by the heading :math:`\theta`
   from the :math:`x` axis (the dashed horizontal line). The thin gray lines
   are square to each wheel.

   - **Tag 1:** the rear axle: the AV's position (the base link).
   - **Tag 2:** the front axle, :math:`L` = 2.875 m (chosen) ahead, turned
     by :math:`\delta` from the body line.
   - **Tag 3:** the point the AV turns about, where the two gray lines meet.
     The rear axle drives a circle of radius :math:`R` around it (the green
     dashed arc).


.. _l10-lec-bicycle-eq:

Write the Model: the State, the Inputs and Four Equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**State**, at the rear axle: the configuration, position :math:`x, y` (m)
and heading :math:`\theta` (rad, counterclockwise from :math:`x`), plus the
speed :math:`v` (m/s). **Inputs:** the front wheel angle :math:`\delta`
(rad, positive turns left) and the acceleration :math:`a` (m/s²).

.. math::

   \dot x = v\cos\theta, \qquad \dot y = v \sin\theta, \qquad
   \dot\theta = \frac{v}{L}\tan\delta, \qquad \dot v = a

- The first two: the rear axle moves along the heading.
- The third: the turn rate grows with speed and with steering. This is where
  the steering enters.
- An EKF predicts with the gyro's measured turn rate instead; here the turn
  rate comes from :math:`\delta`, because a controller chooses
  :math:`\delta`.

.. tip::

   See "Why tan δ = L/R" in :doc:`Going Further <l10_appendix>` for where
   the third equation comes from.


.. _l10-lec-steer-curvature:

Steer for a Curvature: a Fixed Angle Drives a Circle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hold :math:`\delta` and the AV drives a circle of radius
:math:`R = L / \tan\delta`. So, to follow a curvature :math:`\kappa = 1/R`,
steer :math:`\delta = \arctan(L\kappa)`.

1. First arc: :math:`\delta = \arctan(2.875 \times 0.1000) = \arctan(0.288)`
   = 0.280 rad (16.0°).
2. Second arc:
   :math:`\delta = \arctan(2.875 \times 0.1673) = \arctan(0.481)` =
   0.448 rad (25.7°).
3. The controller's steering limit, 0.7 rad (``steer_limit``): the smallest
   circle is :math:`R = 2.875 / \tan 0.7` = 3.41 m.

.. important::

   Both arcs are within reach: 0.448 rad is under the 0.7 rad limit. A
   corner tighter than :math:`R` = 3.41 m would not be.

.. tip::

   See "Where the Model Stops Holding" in :doc:`Going Further
   <l10_appendix>` for the sideways acceleration up to which the model
   holds.

.. dropdown:: More detail: check the model by hand, one step on the second arc
   :class-container: more-detail
   :icon: info

   The AV on the second arc: :math:`v` = 3.458 m/s, :math:`\delta` =
   0.448 rad (the angle this arc needs, from the steps above), one
   controller step :math:`\Delta t` = 0.05 s. We measure from the AV
   itself: :math:`x = y = 0`, :math:`\theta = 0`.

   1. Forward:
      :math:`\Delta x = v\cos\theta\,\Delta t = 3.458 \times 1 \times 0.05`
      = 0.173 m.
   2. Sideways:
      :math:`\Delta y = v\sin\theta\,\Delta t = 3.458 \times 0 \times 0.05`
      = 0 m.
   3. Turn: :math:`\Delta\theta = \frac{v}{L}\tan\delta\,\Delta t =
      \frac{3.458}{2.875} \times 0.481 \times 0.05` = 0.0289 rad.

   Twenty such steps (1 s) turn the AV by 20 × 0.0289 = 0.578 rad, about
   33°. The next step starts from the new heading, so the AV moves sideways
   from step 2 on.


.. _l10-lec-bicycle-summary:

Where the Bicycle Model Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where the bicycle model leaves us
   :class: tip

   - **State at the rear axle:** :math:`x, y, \theta, v`. **Inputs:**
     :math:`\delta`, :math:`a`. The turn rate is :math:`v\tan\delta / L`.
   - **Steering for a curvature:** :math:`\delta = \arctan(L\kappa)`:
     0.280 rad and 0.448 rad for our two arcs, under the 0.7 rad limit.
   - **Sideways acceleration** on our turn: at most 2.0 m/s², the profile's
     cap. Where the model stops holding: :ref:`in Going Further
     <l10-app-limits>`.


.. _l10-lec-trajectories:

Trajectories
------------

The bicycle model says where a steering angle and a speed take the AV. This
section builds on the speed profile from The Turn, and uses the model's
steering rule in its last part.

**In this section:** we add time to the path, and change speed without a
jump in acceleration.

**What it is for:** the controllers get a target that says where to be and
when, with no jolt the passengers feel.


.. _l10-lec-trajectory:

Add Time to the Path: a Trajectory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Trajectory
   :class: note

   A path with a speed and a time at each point: where the AV should be, how
   fast, and when. A **path** says only where.

.. figure:: /_static/images/L10/trajectory_dots.png
   :alt: The same top view of the turn as before, with blue dots on the lane center, one for every second of the speed profile. On the approach the dots are evenly spaced, 8 meters apart; in the corner they bunch up, about 3.5 meters apart, and spread out again on the exit. Gray leader lines label four dots: t = 0 s at the start, t = 5 s on the approach, t = 10 s just before the corner, t = 15 s on the exit.
   :width: 85%
   :align: center

   The speed profile as a trajectory: one dot per second.

.. admonition:: Reading the figure
   :class: tip

   The same top view of the turn as before. Each blue dot marks one second
   of the profile; four of them are labeled with their time: 0 s at the
   start, 5 s on the approach, 10 s just before the corner, 15 s on the
   exit. Where the AV is slow, the dots bunch up.

- Each 0.25 m step of the path takes :math:`\Delta s / v`; adding them up
  gives :math:`t(s)`.
- At 8 m/s the dots are 8 × 1 = 8.0 m apart; in the turn,
  3.46 × 1 = 3.5 m (3.45 m measured between two dots).
- The whole path takes 20.0 s.


.. _l10-lec-quintic:

Change Speed With No Jump in Acceleration: a Quintic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal is to slow from 8 to 3.46 m/s for the turn, with the acceleration
at zero where the braking starts and where it ends.

.. admonition:: Definition: Quintic
   :class: note

   A polynomial of degree five. Here it gives :math:`s`, the distance along
   the path, at time :math:`t`:

   .. math::

      s(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5

Its six numbers, :math:`a_0` to :math:`a_5`, let it meet six conditions,
three at each end. :math:`T` is how long the slow-down lasts, and :math:`D`
is how far the AV travels in that time.

- Start, :math:`t = 0`: :math:`s = 0`, speed 8 m/s, acceleration 0.
- End, :math:`t = T`: :math:`s = D`, speed 3.46 m/s, acceleration 0.

A cubic (degree three) has four numbers: it can match the distance and the
speed at both ends, not the acceleration. The sampling planner's S curve was
a quintic too: the sideways offset from the lane center against the distance
along the road, flat at both ends.

.. tip::

   See "The Quintic" in :doc:`Going Further <l10_appendix>` for how
   :math:`T` and :math:`D` are chosen, and the six equations solved.


.. _l10-lec-slow-down:

Slow Down for the Turn: Two Ways Between the Same Speeds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/slow_speed_accel.png
   :alt: Two graphs against the time from the start of braking. Left, speed: the red line, dark tag 1, drops in a straight line from 8 to 3.46 meters per second in 2.3 seconds; the green curve, tag 2, leaves 8 gently, falls along an S shape and reaches 3.46 at about 3.4 seconds. Right, acceleration: the red line jumps from 0 to minus 2 at once, stays there for 2.3 seconds and jumps back to 0; the green curve dips smoothly from 0 to minus 2 at its middle and comes back to 0. A dotted line marks minus 2.
   :width: 95%
   :align: center

   Two ways to slow from 8 to 3.46 m/s.

.. admonition:: Reading the figure
   :class: tip

   Both graphs are against the time from the start of braking. Left: the
   speed. Right: the acceleration; the dotted line marks −2 m/s².

   - **Tag 1 (red):** constant deceleration, 2.0 m/s² (our speed profile's):
     :math:`T = (8 - 3.46)/2.0` = 2.27 s, over
     :math:`D = \frac{8 + 3.46}{2} \times 2.27` = 13.0 m. Its acceleration
     jumps from 0 to −2 and back.
   - **Tag 2 (green):** a quintic that never passes 2.0 m/s²: 3.41 s, over
     19.5 m. Its acceleration changes smoothly. It starts braking
     19.5 − 13.0 = 6.5 m earlier.


.. _l10-lec-jerk:

Measure Comfort: Jerk, How Fast the Acceleration Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Jerk
   :class: note

   The rate of change of acceleration, in m/s³. Passengers feel a jump in
   acceleration as a jolt; a small jerk feels smooth.

.. figure:: /_static/images/L10/slow_jerk.png
   :alt: A graph of jerk in meters per second cubed, sampled at 20 per second, against the time from the start of braking. The red line, dark tag 1, is zero except for a spike down to minus 40 at time 0 and a spike up to plus 40 at about 2.3 seconds. The green line, tag 2, stays close to zero, rising slowly from about minus 2.3 to plus 2.3.
   :width: 85%
   :align: center

   The jerk of the two slow-downs, sampled 20 times a second.

.. admonition:: Reading the figure
   :class: tip

   The jerk against the time from the start of braking, sampled 20 times a
   second.

   - **Tag 1 (red):** constant deceleration. The acceleration jumps by
     2.0 m/s² within one 0.05 s step, so the jerk is 2.0 / 0.05 = 40 m/s³,
     twice: once when braking starts, once when it ends. A true jump has no
     finite jerk: the number grows the faster we sample (100 samples a
     second give 2.0 / 0.01 = 200).
   - **Tag 2 (green):** the quintic: at most 2.3 m/s³.


.. _l10-lec-steer-jump:

Steer Into the Turn: the Steering Must Jump Too
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Entering the first arc at 4.47 m/s, the AV goes from a straight line to
:math:`\kappa` = 0.1000 /m in one point of the path:

1. Steering needed: from 0 to 0.280 rad (the bicycle model section), at
   once.
2. Sideways acceleration :math:`v^2\kappa`: from 0 to
   :math:`4.47^2 \times 0.1000` = 2.0 m/s², at once.
3. No steering can turn in zero time: ours takes 0.1 s to start and about
   0.2 s to get most of the way. The AV leaves the path for a moment,
   whatever the controller.

.. important::

   The curvature graph shows that this Town03 junction has no gradual part:
   the curvature steps from 0 to 0.100 /m. A planner can smooth the path
   first.


.. _l10-lec-trajectories-summary:

Where Trajectories Leave Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where trajectories leave us
   :class: tip

   - **Trajectory = path + time.** Our profile drives the 137.5 m in 20.0 s;
     the points are 8.0 m apart per second on the approach, 3.45 m in the
     turn.
   - **Jerk** is what passengers feel. A constant 2.0 m/s² braking jumps:
     40 m/s³ at 20 per second. A quintic: 2.3 m/s³, for 6.5 m more braking
     distance.
   - **Quintic:** zero acceleration at both ends, so no jolt where braking
     starts or ends; the six equations solved: :ref:`in Going Further
     <l10-app-quintic>`.
   - **The path's curvature jumps too**, so the steering would have to jump.


.. _l10-lec-speed:

Speed Control
-------------

The trajectory gives a target speed at every point. This section builds on
it: the controller that holds the AV at that speed. The steering waits until
after the break.

**In this section:** a PID controller turns the speed error into throttle
and brake.

**What it is for:** the controller node's speed control is a PID with
anti-windup; this section shows why it needs the anti-windup.


.. _l10-lec-speed-loop:

Hold the Target Speed: the Speed Loop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pid_block.png
   :alt: A block diagram. The target speed v_ref enters a summing circle with a plus sign; the measured speed v comes back into it with a minus sign. The difference e splits into three gray boxes: K_p times e, K_i times the sum of e times delta t, K_d times the change of e over delta t. Their outputs add in a second circle to u. A box clips u to minus 1 to 1; u above 0 is throttle, u below 0 is brake. Then the AV, whose measured speed v returns to the first circle.
   :width: 95%
   :align: center

   The speed loop with a PID controller.

.. admonition:: Reading the figure
   :class: tip

   Read left to right. The target speed :math:`v_{\mathrm{ref}}` minus the
   measured speed :math:`v` gives the error :math:`e`. Three terms act on
   it: :math:`K_p e`; :math:`K_i \sum e\,\Delta t`; and
   :math:`K_d (e_k - e_{k-1}) / \Delta t`. They add to the command
   :math:`u`, which is clipped to −1 to 1: above 0 it is throttle, below 0
   brake. The AV's measured speed returns to the start of the loop.

- The error :math:`e = v_{\mathrm{ref}} - v`. Three terms add to the
  command :math:`u`: P, the **proportional** term; I, the **integral** term;
  D, the **derivative** term. Together they make a **PID** controller.
- Our speed model (chosen): full throttle gives 4 m/s², full brake 8 m/s²,
  drag takes :math:`0.15 + 0.012\,v^2` m/s², and the engine lags by 0.3 s.
  Throttle stops at 0.75, the node's ``max_throttle``.
- The test: the AV at rest; the target jumps to 8 m/s, as when a red light
  turns green.


.. _l10-lec-p:

Try P Alone: the AV Settles 0.42 m/s Short
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pid_p.png
   :alt: Two graphs of speed against time after the target steps to 8 meters per second. Left, 0 to 20 seconds: the orange curve rises from 0, levels off just under the dashed target line at 8 after about 4 seconds and stays there; a dotted box marks the part from 10 to 20 seconds. Right, that box enlarged, speed 7.0 to 8.5: the orange line sits flat at 7.58, the dashed target at 8.0, and a double arrow between them carries dark tag 1.
   :width: 95%
   :align: center

   P alone: the speed settles under the target.

.. admonition:: Reading the figure
   :class: tip

   Left: the speed for 20 s after the target steps to 8 m/s (dashed line).
   Right: the dotted box, enlarged.

   - **Tag 1:** the gap between the target, 8.0 m/s, and where the AV
     settles, 7.58 m/s.

:math:`u = K_p e` with :math:`K_p` = 0.5 (chosen). Why the gap stays:

1. At 7.58 m/s the drag is :math:`0.15 + 0.012 \times 7.58^2` = 0.84 m/s²;
   holding the speed needs throttle 0.84 / 4 = 0.21.
2. P makes throttle only from an error: 0.5 × :math:`e` = 0.21 gives
   :math:`e` = 0.42 m/s.


.. _l10-lec-pi:

Close the Gap with I: the AV Overshoots by 4 m/s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The I term adds up the error over time, :math:`K_i \sum e\,\Delta t`. While
any gap remains, the sum grows and pushes more throttle, so the gap closes.
With :math:`K_i` = 0.3 (chosen):

.. figure:: /_static/images/L10/pid_pi.png
   :alt: A graph of speed against time after the target steps to 8 meters per second. The red curve rises past the dashed target line at 8, keeps rising to a peak just above 12 at about 6 seconds (dark tag 1), then falls back and settles on 8 after about 11 seconds.
   :width: 90%
   :align: center

   PI: the gap closes, after a large overshoot.

.. admonition:: Reading the figure
   :class: tip

   The speed against the time after the target steps to 8 m/s (dashed
   line).

   - **Tag 1:** the peak: 12.18 m/s, 4.18 m/s over the target. The speed
     settles within 0.2 m/s of 8 only after 10.6 s.


.. _l10-lec-windup:

Explain the Overshoot: Windup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Integrator windup
   :class: note

   The I term keeps growing while the actuator is at its limit and cannot
   act on it; the stored sum then drives the output past the target once
   the limit is released. Here the sum shrinks only while the AV is too
   fast.

.. figure:: /_static/images/L10/pid_windup.png
   :alt: A graph of the command against time. A pink band covers the first 5.85 seconds, while the throttle sits at its limit. A dotted line marks the throttle limit 0.75. The red curve, the I term, dark tag 1, rises from 0 to a peak of about 4.3 at 3.4 seconds and falls back to about 0.23 by 12 seconds. The dark curve, dark tag 2, is the throttle actually used: flat at 0.75 for the first 5.85 seconds, then a short dip below 0, then about 0.23.
   :width: 80%
   :align: center

   The I term and the throttle during the PI run.

.. admonition:: Reading the figure
   :class: tip

   The command against the time after the target steps to 8 m/s; 0 to 1 is
   throttle. The dotted line is the throttle limit, 0.75. The pink band
   covers the first 5.85 s, while the throttle sits at that limit.

   - **Tag 1 (red):** the I term. It rises to about 4.3, then falls back to
     about 0.23.
   - **Tag 2 (dark):** the throttle actually used: flat at 0.75, then a
     short dip below 0 (brake), then about 0.23.

1. The throttle (tag 2) is at its 0.75 limit from the start; a larger
   command cannot open the throttle further.
2. The I term keeps adding the large early errors: by the time the AV
   reaches 8 m/s (3.45 s), the sum is 14.29 m and the I term
   0.3 × 14.29 = 4.29 (tag 1).


.. _l10-lec-clamp:

Anti-Windup: Clamp the Sum
~~~~~~~~~~~~~~~~~~~~~~~~~~

At every step:

1. add :math:`e\,\Delta t` to the sum;
2. hold the sum within ±1 m (chosen; the controller node's
   ``pid_windup_limit`` is 2.0);
3. compute :math:`u` from the three terms.

.. figure:: /_static/images/L10/pid_clamp.png
   :alt: A graph of speed against time after the target steps to 8 meters per second. The red curve without the clamp rises to a peak above 12 (dark tag 1). The green curve with the clamp rises like it but stops at about 8.25 and settles on 8 within a few seconds (dark tag 2).
   :width: 90%
   :align: center

   The same PI run, without and with the clamp.

.. admonition:: Reading the figure
   :class: tip

   The speed against the time after the target steps to 8 m/s (dashed
   line).

   - **Tag 1 (red):** without the clamp: peak 12.18 m/s.
   - **Tag 2 (green):** with it: peak 8.25 m/s, within 0.2 m/s of 8 after
     4.4 s.

.. dropdown:: More detail: size the clamp, since too tight brings the gap back
   :class-container: more-detail
   :icon: info

   The sum must still be able to hold the throttle the AV needs at the
   target speed:

   1. At 8 m/s the drag is :math:`0.15 + 0.012 \times 8^2` = 0.92 m/s², so
      the AV needs throttle 0.92 / 4 = 0.23 with no error left.
   2. With :math:`K_i` = 0.3 and the sum held within 1 m, the I term can
      reach 0.3 × 1 = 0.3. Enough.
   3. With :math:`K_i` = 0.1 and the same clamp, it can reach only 0.1.
      Measured: the AV settles at 7.76 m/s, 0.24 m/s short: better than P
      alone (0.42), but the gap does not close.

   So the clamp and :math:`K_i` go together: :math:`K_i` × clamp must
   exceed the throttle the steady speed needs.


.. _l10-lec-d:

Trim the Peak with D: a Little Less Overshoot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pid_compare.png
   :alt: Two graphs of speed against time. Left, 0 to 20 seconds: three curves rise together from 0; the orange one levels off just under 8, the green and the blue dashed ones reach 8. A dotted box marks 2 to 10 seconds, 7 to 8.5. Right, that box enlarged, with dark tags: the orange curve, tag 1, flattens at 7.58; the green curve, tag 2, peaks at about 8.25 near 4 seconds and settles on 8; the blue dashed curve, tag 3, peaks lower, about 8.12, and settles on 8.
   :width: 95%
   :align: center

   P, PI and PID, all with the clamp.

.. admonition:: Reading the figure
   :class: tip

   Left: the three runs for 20 s. Right: the dotted box, enlarged. The tags
   match the rows of the table below.

   - **Tag 1 (orange):** P alone.
   - **Tag 2 (green):** PI.
   - **Tag 3 (blue, dashed):** PID.

.. list-table::
   :widths: 35 20 20 25
   :header-rows: 1
   :class: compact-table

   * - **Gains (chosen), clamp 1 m**
     - **Peak**
     - **After 30 s**
     - **Within 0.2 m/s**
   * - 1: P, :math:`K_p` = 0.5
     - 7.72 m/s
     - 7.58 m/s
     - never
   * - 2: PI, :math:`K_i` = 0.3
     - 8.25 m/s
     - 8.00 m/s
     - after 4.4 s
   * - 3: PID, :math:`K_d` = 0.1
     - 8.12 m/s
     - 8.00 m/s
     - after 3.5 s

.. dropdown:: More detail: run the PID every 0.05 s, the formula the controller uses
   :class-container: more-detail
   :icon: info

   At step :math:`k`, with :math:`\Delta t` = 0.05 s and
   :math:`e_k = v_{\mathrm{ref}} - v_k`:

   .. math::

      u_k = K_p\, e_k \;+\; K_i \sum_{j \le k} e_j\,\Delta t \;+\;
      K_d\,\frac{e_k - e_{k-1}}{\Delta t}

   - :math:`u_k` is clipped to −1 to 1: above 0 it is throttle (at most
     0.75 in the node), below 0 it is brake.
   - D reacts to how fast the error changes. A sudden target jump makes
     that change large for one step. Here :math:`K_d` = 0.1 trimmed the
     peak from 8.25 to 8.12 m/s.
   - Our gains suit our speed model. The node's ``controller_config.yaml``
     starts at :math:`K_p` = 0.5, :math:`K_i` = 0.05, :math:`K_d` = 0.1,
     with the sum held within 2.0. By the clamp rule above,
     0.05 × 2.0 = 0.1, under the 0.23 our model needs at 8 m/s. CARLA's car
     may need another throttle, so tune :math:`K_i` on it and check for a
     gap.


.. _l10-lec-handson-1:

Hands-On, Parts 1 to 3: Try the Model, the Profile and the PID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The hands-on script is in the course's Python repo, folder ``lecture10``
(`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture10>`__):

.. code-block:: bash

   python3 l10_handson.py --part bicycle   # steering and circle
   python3 l10_handson.py --part profile   # slowing down
   python3 l10_handson.py --part pid       # P, PI, PID, clamp

.. admonition:: What to look at
   :class: hint

   1. ``bicycle``: which steering angle drives a 10 m circle? Check it
      against :math:`\delta = \arctan(L/R)`.
   2. ``pid``: set :math:`K_i` = 0.6 with no clamp, then with the clamp. How
      much does the clamp cut the peak?
   3. ``pid``: find gains with a peak under 8.2 m/s that reach 8 m/s within
      0.2 m/s in under 4 s.

We computed the ``pid`` runs in advance; the folder has no controller code.


.. _l10-lec-speed-summary:

Where Speed Control Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where speed control leaves us
   :class: tip

   - **P** needs an error to make throttle: 0.42 m/s short at
     :math:`K_p` = 0.5.
   - **I** removes the gap, but winds up while the throttle sits at its
     limit: 12.18 m/s for an 8 m/s target.
   - **Clamping the sum** stops it: peak 8.25 m/s.
   - **D** trimmed the peak to 8.12 m/s here.

A 10-minute break follows in class.


.. _l10-lec-pp:

Pure Pursuit
------------

The PID holds the AV at the profile's speed. This section keeps that PID
running in every run and adds the steering.

**In this section:** Pure Pursuit finds a steering angle from the geometry
of a point ahead on the path.

**What it is for:** the controller node steers with Pure Pursuit; its one
parameter, the lookahead, changes how the AV drives.


.. _l10-lec-errors:

Measure How Far Off the Path: Two Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Cross-track error
   :class: note

   The AV's distance from the path, measured square to the path at the
   nearest path point. We measure it at the rear axle, positive to the left:
   the rear axle's :math:`d` in the Frenet frame.

- **Heading error:** the angle between the AV's heading and the path's
  direction at that nearest point.
- Our runs start with a cross-track error of 1.0 m and a heading error of 0:
  the AV parallel to the lane, 1 m left of its center.
- A steering controller turns these two into a steering angle. Pure Pursuit
  does it by looking ahead along the path; Stanley (next section) uses both
  errors directly.


.. _l10-lec-pp-steps:

Steer with Pure Pursuit: Aim at a Point Ahead, Drive the Arc to It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pure Pursuit chases a point that keeps moving ahead along the path. At every
cycle:

1. Draw a circle of radius :math:`L_d`, the **lookahead distance**, around
   the rear axle. Where the path leaves it, ahead of the AV: the **goal
   point**.
2. Write the goal point in the AV's own frame: how far forward, how far
   left.
3. Find the circle arc that starts at the rear axle along the AV's heading
   and passes through the goal point. Its curvature:
   :math:`\kappa = 2\sin\alpha / L_d`.
4. Steer for that curvature: :math:`\delta = \arctan(L\kappa)`, the bicycle
   model's rule.

.. important::

   The controller node gets the pose of the car's origin and moves it back
   to the rear axle with ``rear_offset``. Next: the four steps by hand, on
   one moment of our run with :math:`L_d` = 5 m (the node's
   ``lookahead_distance``).


.. _l10-lec-pp-step1:

Step 1: Find the Goal Point on the Lookahead Circle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The moment: :math:`t` = 10.65 s, at :math:`s` = 82.7 m, just before the
first arc begins (:math:`s` = 83.2 m).

.. figure:: /_static/images/L10/pp_geom_1.png
   :alt: A close top view of the corner, in meters: the lane edges in black, the lane center dashed gray, bending right after x = 83. The AV is drawn faintly, facing right and slightly down, with its rear axle as a dark dot (dark tag 2) near x = 82.7, y = 0. A blue dashed circle of radius 5 meters is centered on the rear axle (dark tag 1). A blue dot (dark tag 3) sits where the lane center leaves the circle ahead of the AV, near x = 87.6, y = minus 1.2.
   :width: 70%
   :align: center

   Step 1: the lookahead circle and the goal point.

.. admonition:: Reading the figure
   :class: tip

   A close top view of the corner, in meters. The lane center is the dashed
   gray line; the AV is drawn faintly.

   - **Tag 1:** the lookahead circle, :math:`L_d` = 5 m (blue dashed).
   - **Tag 2:** the rear axle: :math:`x` = 82.69, :math:`y` = −0.03 m;
     heading :math:`\theta` = −0.0443 rad (−2.5°); speed 5.22 m/s.
   - **Tag 3:** the goal point: (87.56, −1.18) m, where the path leaves the
     circle ahead.


.. _l10-lec-pp-step2:

Step 2: Write the Goal Point in the AV's Frame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pp_geom_2.png
   :alt: The same close top view. Two black arrows leave the rear axle: one forward along the AV's heading, labeled forward, one to its left, labeled left. An orange double arrow below and parallel to the forward arrow spans from the rear axle to the goal point's forward distance (tag 4). A short orange double arrow beside the goal spans its sideways distance to the right of the forward line (tag 5). The lookahead circle and the goal point are as before, tags 1 to 3. All tags are dark circles.
   :width: 70%
   :align: center

   Step 2: the goal point's forward and sideways distances.

.. admonition:: Reading the figure
   :class: tip

   The same view, with the AV's own frame: two black arrows from the rear
   axle, forward and left. Tags 1 to 3 are as in Step 1.

   - **Tag 4:** how far forward the goal point is, :math:`g_x` (orange).
   - **Tag 5:** how far to the side it is, :math:`g_y`, here to the right
     of the forward line (orange).

1. From the rear axle to the goal, in the map: :math:`\Delta x` = 4.866 m,
   :math:`\Delta y` = −1.150 m.
2. Turn by :math:`-\theta` (:math:`\cos\theta` = 0.9990,
   :math:`\sin\theta` = −0.0443). Forward, tag 4:
   :math:`g_x = \cos\theta\,\Delta x + \sin\theta\,\Delta y`
   = 0.9990 × 4.866 + (−0.0443) × (−1.150) = 4.912 m.
3. Left, tag 5: :math:`g_y = -\sin\theta\,\Delta x + \cos\theta\,\Delta y`
   = 0.0443 × 4.866 + 0.9990 × (−1.150) = −0.933 m: 0.933 m to the right.


.. _l10-lec-pp-step3:

Step 3: Find the Angle α and the Arc Through the Goal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pp_geom_3.png
   :alt: The same close top view, zoomed out downward. A black line joins the rear axle to the goal point; a red arc at the rear axle (tag 4) marks the small angle between the forward arrow and that line. A green arc starts at the rear axle along the heading and curves right into the goal point. A green cross far below, near x = 82.1, y = minus 13.4 (tag 5), is the arc's center; green dotted lines join it to the rear axle and to the goal. All tags are dark circles.
   :width: 60%
   :align: center

   Step 3: the angle to the goal and the arc through it.

.. admonition:: Reading the figure
   :class: tip

   The same view, zoomed out downward. Tags 1 to 3 are as in Step 1. The
   black line joins the rear axle to the goal point; the green arc is the
   arc through the goal.

   - **Tag 4:** the angle :math:`\alpha` between the forward arrow and the
     line to the goal (red).
   - **Tag 5:** the arc's center (green cross), joined to the rear axle and
     to the goal by green dotted lines.

1. The angle to the goal (tag 4):
   :math:`\alpha = \arctan(g_y / g_x) = \arctan(-0.933 / 4.912)` =
   −0.188 rad (−10.8°).
2. The arc's curvature: :math:`\kappa = 2\sin\alpha / L_d`
   = 2 × (−0.1866) / 5 = −0.0746 /m.
3. Its radius: :math:`R` = 1 / 0.0746 = 13.4 m, centered at tag 5.
   Negative: a right turn.

.. tip::

   See "Pure Pursuit's Arc" in :doc:`Going Further <l10_appendix>` for why
   :math:`\kappa = 2\sin\alpha / L_d`.


.. _l10-lec-pp-step4:

Step 4: Turn the Arc into a Steering Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. The bicycle model: :math:`\delta = \arctan(L\kappa) =
   \arctan(2.875 \times (-0.0746)) = \arctan(-0.214)` = −0.211 rad
   (−12.1°), to the right.
2. The controller node turns :math:`\delta` into a ``VehicleCmd`` steer
   from −1 to 1: it divides by 1.222 rad, the wheel angle at full steering
   (measured in CARLA), then clamps: −0.211 / 1.222 = −0.173.
3. Next cycle, 0.05 s later, the AV has moved: a new goal point, a new arc.

.. important::

   Two common mistakes: dividing by 0.7, the most the controller asks for,
   instead of 1.222, which turns the wheels 1.75 times too far; and the
   sign: ``VehicleCmd`` steer is positive to the left, CARLA's steer
   positive to the right, so the node that steps CARLA flips it.

Steps 3 and 4 in one line:
:math:`\delta = \arctan\big(2L\sin\alpha / L_d\big)`.


.. _l10-lec-ld-short:

Choose the Lookahead: Too Short, and the AV Weaves
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pp_straight.png
   :alt: A graph, not a map: the rear axle's distance from the lane center, positive left, against the distance along the path from 0 to 72 meters. All three runs start at plus 1. The red curve, dark tag 1, swings across the center with growing swings, reaching about plus and minus 3 meters by 70 meters. The blue curve, tag 2, crosses once to about minus 0.3 and settles near zero by about 36 meters. The green dashed curve, tag 3, slides down to zero without crossing much and settles by about 16 meters.
   :width: 90%
   :align: center

   Three lookahead distances on the straight approach.

.. admonition:: Reading the figure
   :class: tip

   A graph, not a map: the rear axle's distance from the lane center
   (positive left) against the distance :math:`s` along the path. Start:
   1 m left, 8 m/s, on the straight approach.

   - **Tag 1 (red):** :math:`L_d` = 3 m: the swings grow to 3.07 m, out of
     the 3.5 m lane.
   - **Tag 2 (blue):** :math:`L_d` = 5 m: crosses by 0.32 m, within 0.1 m
     from :math:`s` = 35.9 m.
   - **Tag 3 (green, dashed):** :math:`L_d` = 10 m: crosses by 0.07 m,
     within 0.1 m from :math:`s` = 15.8 m.

.. important::

   The weave needs both the steering's delay and its lag. The same 3 m run
   crosses by only 0.05 m with instant steering, and by 0.32 m with the lag
   alone, then settles.


.. _l10-lec-ld-long:

Choose the Lookahead: Too Long, and the AV Cuts the Corner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pp_turn.png
   :alt: A top view of the corner from x = 68 to 98 and y = minus 26 to 4. The blue solid run with a 5 meter lookahead stays on the dashed lane center through the corner, swinging slightly outside after it. The green dashed run with a 10 meter lookahead leaves the center early, cuts inside the corner, where a green dot marks its farthest point inside (dark tag 1), then swings outside on the exit, where a second green dot marks its farthest point outside (dark tag 2), before returning to the center.
   :width: 65%
   :align: center

   A 5 m and a 10 m lookahead through the corner.

.. admonition:: Reading the figure
   :class: tip

   A top view of the corner, in meters. The blue line is the 5 m run; the
   green dashed line is the 10 m run.

   - **Tag 1:** with :math:`L_d` = 10 m, the goal point is already around
     the corner, so the AV turns early: 0.98 m inside the center at
     :math:`s` = 90.6 m.
   - **Tag 2:** then it turns too late on the exit: 0.95 m outside at
     :math:`s` = 102.2 m.

:math:`L_d` = 5 m stays within 0.25 m of the center through the corner.


.. _l10-lec-ld-tradeoff:

Choose the Lookahead: a Trade-Off Between the Two
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L10/pp_tradeoff.png
   :alt: A graph of distance from the lane center in meters against the lookahead distance from 4 to 12 meters. The orange line with round markers, dark tag 1, falls from 0.50 at 4 meters to 0.05 at 12. The dark line with square markers, tag 2, is 0.40 at 4 meters, lowest at 5 meters with 0.25, then rises to 0.39, 0.67, 0.98 and 1.53 at 6, 8, 10 and 12 meters.
   :width: 90%
   :align: center

   Two errors against the lookahead distance.

.. admonition:: Reading the figure
   :class: tip

   The distance from the lane center against the lookahead distance
   :math:`L_d`, from 4 to 12 m.

   - **Tag 1 (orange, round markers):** how far the AV crosses after the
     1 m start. It falls as :math:`L_d` grows.
   - **Tag 2 (dark, square markers):** the largest distance from the center
     in the turn. It is lowest at :math:`L_d` = 5 m (0.25 m), then grows.

At 4 m and below the AV weaves (4 m: about 0.4 m each way, and it does not
stop).

.. important::

   Snider found the same trade-off: a short lookahead tracks the path more
   closely, a long one drives more smoothly. On our turn, with our model,
   5 m is the best of the eight we tried.


.. _l10-lec-ld-speed:

A Lookahead for Every Speed: Scale It with the Speed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At 8 m/s the AV covers 5 m in 5 / 8 = 0.6 s; at 3.46 m/s, in
5 / 3.46 = 1.4 s. To look the same **time** ahead at every speed, scale
:math:`L_d` with the speed: :math:`L_d = \max(3\ \mathrm{m},\ k_v v)`, with
:math:`k_v` in seconds. With :math:`k_v` = 0.75 s: on the approach,
0.75 × 8 = 6 m; in the second arc, 0.75 × 3.46 = 2.6 m, raised to 3 m.

Mean \|jerk\|: how fast the sideways acceleration :math:`v\dot\theta`
changes, averaged over the run.

.. list-table::
   :widths: 28 25 27 20
   :header-rows: 1
   :class: compact-table

   * - **Lookahead**
     - **Crosses after start**
     - **Largest in the turn**
     - **Mean \|jerk\|**
   * - 5 m fixed
     - 0.32 m
     - 0.25 m
     - 1.79 m/s³
   * - 10 m fixed
     - 0.07 m
     - 0.98 m
     - 0.42 m/s³
   * - 0.5 s × :math:`v`
     - 0.54 m (weaves)
     - 0.46 m
     - 8.88 m/s³
   * - 0.75 s × :math:`v`
     - 0.23 m
     - 0.07 m
     - 1.11 m/s³
   * - 1.0 s × :math:`v`
     - 0.12 m
     - 0.18 m
     - 0.59 m/s³

Long at speed, short in the corner: 0.75 s gives the smallest corner error.
The controller node sets the lookahead to 5 m or 1 s × :math:`v`,
whichever is longer, because the EKF's pose jumps a little at each GNSS fix
and a short lookahead turns each jump into a swerve.


.. _l10-lec-handson-4:

Hands-On, Part 4: Compare the Steering Runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python3 l10_handson.py --part track     # steering runs

.. figure:: /_static/images/L10/handson_track.png
   :alt: Part of the hands-on window. Left, the corner from above with the lane edges, the lane center and the rear axle's path of the chosen run, here Pure Pursuit with 5 meters, and the AV. Right, two graphs against the distance along the path: the rear axle's distance off the center, and the steering angle.
   :width: 80%
   :align: center

   Part of the hands-on window, for Pure Pursuit with 5 m.

.. admonition:: Reading the figure
   :class: tip

   - **Left:** the corner from above, with the lane edges, the lane center
     (gray dashed) and the rear axle's path of the chosen run (blue), here
     Pure Pursuit with 5 m, and the AV.
   - **Right, top:** the rear axle's distance off the center (positive
     left) against the distance :math:`s` along the path.
   - **Right, bottom:** the steering angle against :math:`s`.
   - The orange band on both graphs marks the junction lane.

A list at the window's left (not shown) picks the run: Pure Pursuit with 2
to 12 m, or 0.5, 0.75 or 1 s × :math:`v`; Stanley with a gain from 0.5 to 8.

.. admonition:: What to look at
   :class: hint

   1. Pick 2, 3 and 4 m: from which lookahead does the AV stop weaving?
   2. Pick 12 m: how far inside the corner does the rear axle get?


.. _l10-lec-pp-summary:

Where Pure Pursuit Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Where Pure Pursuit leaves us
   :class: tip

   - **Four steps:** goal point on the lookahead circle; goal in the AV's
     frame; :math:`\kappa = 2\sin\alpha / L_d`;
     :math:`\delta = \arctan(L\kappa)`. On our turn: −0.211 rad, command
     −0.173.
   - **Short lookahead** (3 m at 8 m/s): the AV weaves, 3.07 m, because the
     steering is delayed and lags.
   - **Long lookahead** (10 m): 0.98 m inside the corner, then 0.95 m
     outside.
   - **Scaled with speed** (0.75 s): 0.07 m at most in the corner.


.. _l10-lec-stanley:

Stanley
-------

Pure Pursuit steers the rear axle toward a point ahead. This section keeps
the same turn, start and PID, and puts a second steering law in its place.

**In this section:** Stanley steers from the two errors, measured at the
front axle.

**What it is for:** it is a second steering controller to compare with Pure
Pursuit.


.. _l10-lec-stanley-law:

Steer from the Front Axle: Stanley's Heading and Cross-Track Terms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The steering law of Stanford's DARPA Grand Challenge car, with our signs
(steering and :math:`e` positive to the left):

.. math::

   \delta = \psi_e - \arctan\frac{k\,e}{v + k_s}

- :math:`\psi_e`: the heading error.
- :math:`e`: the cross-track error of the **front** axle.
- :math:`k`: a gain.
- :math:`k_s` = 1 m/s keeps the fraction finite when the AV stands still.
  Hoffmann et al. found 1 m/s "appropriate" in experiments (Hoffmann et al.,
  2007, p. 2299).

The team's paper writes a plus sign with its own signs. With ours, an AV
left of the path (:math:`e > 0`) must steer right, so the term is
subtracted.

.. figure:: /_static/images/L10/stanley_geom.png
   :alt: A close top view of the corner with the AV drawn faintly. A dark dot at the rear axle (tag 1) and a purple dot at the front axle (tag 2), joined by a line. Just below the front axle, a gray dot on the lane center (tag 3), the nearest path point, with a short purple double arrow between them. A gray line from that point along the path's direction (tag 4) and a dark line from the front axle along the AV's heading; a red arc (tag 5) marks the angle between them. All tags are dark circles.
   :width: 75%
   :align: center

   Stanley's two errors, at the front axle.

.. admonition:: Reading the figure
   :class: tip

   A close top view of the corner, at the same moment as Pure Pursuit's
   worked example. The AV is drawn faintly.

   - **Tag 1:** the rear axle.
   - **Tag 2:** the front axle (purple).
   - **Tag 3:** the path point nearest the front axle; the short purple
     double arrow between them is :math:`e`.
   - **Tag 4:** the path's direction there (gray line).
   - **Tag 5:** the heading error :math:`\psi_e`, the angle (red arc)
     between the path's direction and the AV's heading (dark line).

.. tip::

   See "Stanley" in :doc:`Going Further <l10_appendix>` for one Stanley
   step by hand, which axle stays on the path, Pure Pursuit against Stanley
   on our turn, and why the cross-track term pulls :math:`e` to zero.


.. _l10-lec-mpc:

MPC
---

Pure Pursuit and Stanley look at the path now, with one formula. This
section sets both aside and builds on the bicycle model: it predicts the
next seconds with it.

**In this section:** model predictive control does what the local planner
did: it rolls out candidates, scores them and keeps the best. Here the
candidates are steering sequences, the plan is made again every 0.05 s, and
only its first input is applied.

**What it is for:** production stacks such as Autoware offer MPC; this
section shows what it adds and what it costs.


.. _l10-lec-mpc-def:

Plan Ahead with MPC: Predict, Score, Apply the First Input, Repeat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Model predictive control (MPC)
   :class: note

   At every step, choose the sequence of inputs over a fixed horizon that a
   model predicts will score best, within the limits; apply only the first
   input; repeat from the newly measured state.

.. figure:: /_static/images/L10/mpc_loop.png
   :alt: Three rows of eight cells, one row per control step k, k plus 1 and k plus 2, each row shifted one cell to the right. A brace over the first row says the horizon, N = 8 steps, predicted with the bicycle model. In each row only the first cell is green. A time arrow runs along the bottom.
   :width: 80%
   :align: center

   The horizon slides forward one step at a time.

.. admonition:: Reading the figure
   :class: tip

   Each row is the plan made at one control step: :math:`k`,
   :math:`k + 1`, :math:`k + 2`. Each plan covers the horizon, :math:`N` = 8
   steps here, predicted with the bicycle model. Each row starts one step
   later than the one above; time runs to the right.

   - **Green cell:** the one input applied before the next plan.
   - **Gray cells:** the rest of the plan, predicted but not applied.

The figure is drawn with 8 steps; our example uses 60. The horizon slides
forward with the AV, so MPC is a feedback controller: each plan starts from
the measured pose.

.. tip::

   See "MPC" in :doc:`Going Further <l10_appendix>` for one MPC step on our
   turn, drawn, and the problem written out.


.. _l10-lec-mpc-weigh:

Weigh MPC: What It Adds and What It Costs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Adds**
     - **Costs**
   * - Sees the curvature jump coming: the horizon covers the next seconds
       of the path
     - An optimization at every step, in time for the next one
   * - Limits inside the problem: the 0.7 rad steering, the steering rate
     - A model good enough to predict with; a wrong model gives wrong plans
   * - Delays in the model: the 0.1 s steering delay can be predicted
     - Weights to tune instead of one lookahead

Autoware, an open-source driving stack, offers both: a steering controller
that tracks the path with a linear MPC, and a Pure Pursuit one.


.. _l10-lec-next:

Next Class
----------

.. admonition:: Today
   :class: important

   The planners hand over a path; **today we gave it a speed profile and
   turned it into steering, throttle and brake.** A superstate, parallel
   regions or a behavior tree keep the behavior layer small. The bicycle
   model predicts; a quintic changes speed with small jerk; a PID holds the
   speed, with a clamp against windup; Pure Pursuit steers toward a point
   5 m ahead (short weaves, long cuts corners); Stanley steers from the
   front axle; MPC plans the next seconds and applies only the first input.

- **L11, End-to-End Driving, VLA and Imitation Learning:** one network from
  the sensors to a trajectory or to the controls, in place of the whole
  stack.
- **Before then:** run the four hands-on parts, ``behavior_tree.py`` (with
  and without ``--no-pass``), and the topics demo if you have CARLA.


.. rubric:: Image credits

The vehicle icon in the figures on this page was created by Stone from the
`Noun Project <https://thenounproject.com>`_. The map is CARLA's Town03
(`carla.org <https://carla.org>`_).
