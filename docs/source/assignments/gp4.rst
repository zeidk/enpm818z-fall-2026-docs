====================================================
GP4: Planning & Control
====================================================

.. card::
   :class-card: sd-bg-dark sd-text-white sd-shadow-sm

   **GP4 -- At a Glance**

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 3 weeks (Week 11 -- Week 14)
      * - **Weight**
        - 20 points (20% of final project)
      * - **Lectures**
        - L8--L10
      * - **Team Size**
        - 4 students
      * - **Submission**
        - Canvas + GitHub repository link


Overview
--------

GP4 is the final building block of your Automated Driving System (ADS).
You will close the loop by adding **path planning** and **vehicle
control** to the pipeline built across GP1--GP3. When GP4 is complete,
the vehicle will drive itself: perceiving the world (GP2), knowing where
it is (GP3), deciding where to go (GP4 planner), and turning the wheel
to get there (GP4 controller).

The three new modules introduced in GP4 are:

- **Path Planner** (``planner_node.py``) -- A* search on the CARLA
  waypoint graph, producing a sequence of ``PoseStamped`` waypoints.
- **Controller** (``controller_node.py``) -- Pure Pursuit (lateral)
  combined with PID (longitudinal) to track the planned path.
- **Behavioral State Machine** (``behavior_node.py``) -- An FSM that
  governs high-level driving behavior: lane following, stopping at
  lights and signs, obstacle avoidance, and emergency stop.

By the end of GP4, your team will record a fully autonomous run in at
least two provided CARLA scenarios and evaluate the system using the
provided metrics script.


Learning Objectives
-------------------

After completing GP4, you will be able to:

- Implement A* graph search on a road network (CARLA waypoint graph)
  and produce a drivable path in real time.
- Design a re-planning strategy that reacts to detected obstacles and
  path deviations.
- Implement the Pure Pursuit lateral controller and derive the steering
  angle from the lookahead geometry.
- Implement a PID longitudinal controller with anti-windup for speed
  tracking.
- Design a finite state machine (FSM) for behavioral driving, including
  state definitions, transition conditions, and safety guards.
- Integrate four separate GP modules (GP1--GP4) into a single pipeline
  launched by one launch file.
- Evaluate autonomous driving performance quantitatively: route
  completion, collision rate, average speed, lateral jerk, and traffic
  rule compliance.
- Document system integration challenges and produce a final technical
  report and presentation-quality results.


Provided Resources
------------------

The following files are provided by the instructor on Canvas and the
course GitHub repository. Integrate them into your package as-is.

.. list-table::
   :header-rows: 1
   :widths: 38 62

   * - File
     - Description
   * - ``waypoint_utils.py``
     - Utilities for querying the CARLA waypoint graph:
       ``get_waypoints(world, location, resolution)``,
       ``get_next_waypoint(wp, distance)``,
       ``distance_to_waypoint(pose, wp)``.
       Wraps the CARLA Python API for ROS 2 compatibility.
   * - ``carla_vehicle_control.py``
     - Helper node that subscribes to a custom
       ``VehicleCmd`` message (throttle, brake, steer)
       and converts it to ``carla_msgs/CarlaEgoVehicleControl``
       for the CARLA ROS bridge.
   * - ``traffic_light_detector.py``
     - ROS 2 node that reads the current traffic light state
       directly from the CARLA API (ground truth) and publishes
       it on ``/traffic/light_state`` (``std_msgs/String``):
       values ``"RED"``, ``"YELLOW"``, ``"GREEN"``, ``"UNKNOWN"``.
   * - ``evaluation_metrics.py``
     - Computes route completion %, collision count, average
       speed, lateral jerk (mean absolute lateral acceleration),
       and red-light violation count from a ROS bag file.
       Outputs a JSON metrics file and summary plots.
   * - ``town01_route.yaml``
     - Test scenario: Town01 route with start pose, goal pose,
       and intermediate checkpoints. Approximately 800 m.
   * - ``town03_route.yaml``
     - Test scenario: Town03 route through an urban grid with
       intersections and traffic lights. Approximately 1.2 km.

.. note::

   ``carla_vehicle_control.py`` requires the ``carla_msgs`` ROS 2
   package from the CARLA ROS bridge. Ensure it is installed before
   building. See the CARLA setup guide in the course materials.


Tasks
-----

GP4 is worth **100 internal points** (scaled to 20% of the project
grade). All four tasks are required. There is no bonus task in GP4
-- invest your effort in making the end-to-end integration robust.

.. dropdown:: Task 1: Path Planner Node (30 pts)
   :icon: gear
   :class-container: sd-border-primary

   Implement ``planner_node.py``, which performs A* search on the CARLA
   waypoint graph and publishes a drivable path to the controller.

   **Subscriptions:**

   - ``/localization/pose`` -- ``geometry_msgs/PoseStamped`` (current position from GP3)
   - ``/perception/fused_objects`` -- ``vision_msgs/Detection3DArray`` (obstacles from GP3)

   **Publications:**

   - ``/planning/path`` -- ``nav_msgs/Path`` (sequence of ``PoseStamped`` waypoints)

   **A* on the CARLA Waypoint Graph:**

   The CARLA world exposes a waypoint graph: each waypoint has
   ``get_next(distance)`` returning successor waypoints. Represent the
   graph as an adjacency list and run A* with Euclidean distance as the
   heuristic.

   .. code-block:: python

      import heapq
      import numpy as np
      from waypoint_utils import get_waypoints, get_next_waypoint, distance_to_waypoint

      def astar_waypoints(start_wp, goal_location, world, resolution=2.0,
                          max_nodes=500):
          """
          A* search on CARLA waypoint graph.

          Parameters
          ----------
          start_wp      : carla.Waypoint  -- starting waypoint
          goal_location : carla.Location  -- goal position
          world         : carla.World
          resolution    : float           -- waypoint step size (metres)
          max_nodes     : int             -- expansion limit (fail-safe)

          Returns
          -------
          list[carla.Waypoint] -- ordered waypoints from start to goal,
                                  or empty list if no path found.
          """
          def heuristic(wp):
              loc = wp.transform.location
              return np.sqrt((loc.x - goal_location.x)**2 +
                             (loc.y - goal_location.y)**2)

          open_set = []
          heapq.heappush(open_set, (heuristic(start_wp), 0, start_wp))
          came_from = {}
          g_score = {start_wp.id: 0.0}
          expanded = 0

          while open_set and expanded < max_nodes:
              _, g, current = heapq.heappop(open_set)
              expanded += 1

              if heuristic(current) < resolution:
                  # Reconstruct path
                  path = []
                  while current.id in came_from:
                      path.append(current)
                      current = came_from[current.id]
                  path.append(start_wp)
                  return list(reversed(path))

              for neighbor in get_next_waypoint(current, resolution):
                  tent_g = g + resolution
                  if neighbor.id not in g_score or tent_g < g_score[neighbor.id]:
                      g_score[neighbor.id] = tent_g
                      f = tent_g + heuristic(neighbor)
                      heapq.heappush(open_set, (f, tent_g, neighbor))
                      came_from[neighbor.id] = current

          return []  # No path found

   **Re-Planning Triggers:**

   The planner must re-plan when either of the following conditions is
   detected (check at ``replan_frequency`` Hz):

   1. **Obstacle on path:** A fused object from ``/perception/fused_objects``
      has its 3D centroid within ``obstacle_clearance`` metres of any
      waypoint on the current planned path.
   2. **Path deviation:** The vehicle's current pose (from
      ``/localization/pose``) is more than ``max_deviation`` metres from
      the nearest waypoint on the current path.

   **Parameters (configurable via** ``planner_config.yaml`` **):**

   .. code-block:: yaml

      planner_node:
        ros__parameters:
          goal_x: 50.0                # Goal position x (metres, map frame)
          goal_y: 120.0               # Goal position y (metres, map frame)
          waypoint_resolution: 2.0    # Metres between waypoints
          replan_frequency: 2.0       # Hz -- how often to check re-plan triggers
          obstacle_clearance: 3.0     # Metres -- min clearance from path to obstacle
          max_deviation: 2.0          # Metres -- max off-path distance before re-plan
          max_astar_nodes: 500        # A* node expansion limit

   .. note::

      The CARLA API is not thread-safe. Make all CARLA API calls from
      the main executor thread. Use a ROS 2 timer callback for the
      re-planning check rather than a separate thread.

.. dropdown:: Task 2: Controller Node (30 pts)
   :icon: gear
   :class-container: sd-border-primary

   Implement ``controller_node.py``, which subscribes to the planned
   path and the current pose, and publishes vehicle control commands.

   **Subscriptions:**

   - ``/planning/path`` -- ``nav_msgs/Path``
   - ``/localization/pose`` -- ``geometry_msgs/PoseStamped``
   - ``/behavior/state`` -- ``std_msgs/String`` (from behavior node)

   **Publications:**

   - ``/carla/ego_vehicle/vehicle_control_cmd`` -- ``carla_msgs/CarlaEgoVehicleControl``
     (via ``carla_vehicle_control.py`` helper)

   **Pure Pursuit -- Lateral Control:**

   Pure Pursuit selects a lookahead point on the path at distance ``L_d``
   from the vehicle and computes the required steering angle ``delta``:

   .. math::

      \delta = \arctan\!\left(\frac{2 \, L \, \sin(\alpha)}{L_d}\right)

   where ``L`` is the vehicle wheelbase, ``L_d`` is the lookahead
   distance, and ``alpha`` is the angle between the vehicle heading and
   the direction to the lookahead point.

   .. code-block:: python

      import numpy as np

      def pure_pursuit_steer(vehicle_pose, path_poses, lookahead_dist,
                             wheelbase=2.875):
          """
          Compute steering angle (radians) using Pure Pursuit.

          Parameters
          ----------
          vehicle_pose  : geometry_msgs/Pose  -- current vehicle pose
          path_poses    : list[geometry_msgs/Pose]  -- planned path
          lookahead_dist: float  -- lookahead distance L_d (metres)
          wheelbase     : float  -- vehicle wheelbase L (metres)

          Returns
          -------
          float -- steering angle in radians (positive = left)
          """
          vx = vehicle_pose.position.x
          vy = vehicle_pose.position.y

          # Extract heading from quaternion
          q = vehicle_pose.orientation
          heading = 2.0 * np.arctan2(q.z, q.w)

          # Find lookahead point: first path pose at distance >= L_d
          lookahead_pt = None
          for pose in path_poses:
              dx = pose.position.x - vx
              dy = pose.position.y - vy
              dist = np.sqrt(dx**2 + dy**2)
              if dist >= lookahead_dist:
                  lookahead_pt = (pose.position.x, pose.position.y)
                  break

          if lookahead_pt is None:
              # At or past goal -- use last point
              last = path_poses[-1].position
              lookahead_pt = (last.x, last.y)

          # Angle to lookahead point in vehicle frame
          dx = lookahead_pt[0] - vx
          dy = lookahead_pt[1] - vy
          angle_to_pt = np.arctan2(dy, dx)
          alpha = angle_to_pt - heading

          # Normalize alpha to [-pi, pi]
          alpha = (alpha + np.pi) % (2 * np.pi) - np.pi

          # Pure Pursuit steering formula
          Ld = np.sqrt(dx**2 + dy**2)  # actual distance to lookahead pt
          delta = np.arctan2(2.0 * wheelbase * np.sin(alpha), Ld)
          return delta

   **PID -- Longitudinal Control:**

   A PID controller tracks the target speed set by the behavior node.

   .. code-block:: python

      class PIDController:
          """PID controller with anti-windup for speed (longitudinal) control."""

          def __init__(self, kp, ki, kd, windup_limit=1.0):
              self.kp = kp
              self.ki = ki
              self.kd = kd
              self.windup_limit = windup_limit
              self._integral = 0.0
              self._prev_error = 0.0

          def compute(self, setpoint, measurement, dt):
              """
              Returns throttle in [0, 1] or brake in [0, 1].
              Positive output -> throttle, negative -> brake.
              """
              error = setpoint - measurement
              self._integral += error * dt
              # Anti-windup: clamp integrator
              self._integral = np.clip(
                  self._integral, -self.windup_limit, self.windup_limit)
              derivative = (error - self._prev_error) / max(dt, 1e-6)
              self._prev_error = error
              output = self.kp * error + self.ki * self._integral \
                       + self.kd * derivative
              return output

   **Parameters (configurable via** ``controller_config.yaml`` **):**

   .. code-block:: yaml

      controller_node:
        ros__parameters:
          # Pure Pursuit
          lookahead_distance: 5.0   # metres
          wheelbase: 2.875          # metres (CARLA Lincoln MKZ default)
          max_steer_angle: 0.7      # radians (~40 deg)
          # PID speed control
          target_speed: 8.0         # m/s (default, overridden by behavior node)
          pid_kp: 0.5
          pid_ki: 0.05
          pid_kd: 0.1
          pid_windup_limit: 2.0
          # Control output limits
          max_throttle: 0.75
          max_brake: 1.0

   .. warning::

      CARLA steering is normalized to ``[-1, 1]``. Convert your
      Pure Pursuit ``delta`` (radians) by dividing by
      ``max_steer_angle``. Clamp the result to ``[-1, 1]`` before
      publishing. Sending values outside this range will be silently
      clipped by CARLA, masking bugs.

.. dropdown:: Task 3: Behavioral State Machine (20 pts)
   :icon: gear
   :class-container: sd-border-primary

   Implement ``behavior_node.py``, a finite state machine (FSM) that
   governs high-level driving behavior and adjusts the target speed
   sent to the controller.

   **States:**

   .. list-table::
      :header-rows: 1
      :widths: 25 75

      * - State
        - Description
      * - ``LANE_FOLLOW``
        - Normal driving along the planned path at configured
          ``target_speed``. Default state.
      * - ``STOP``
        - Vehicle decelerates to 0 and remains stationary.
          Triggered by red traffic light or stop sign within
          ``stop_distance`` metres ahead.
      * - ``OBSTACLE_AVOIDANCE``
        - Vehicle decelerates to ``slow_speed`` when a fused
          object is within ``obstacle_distance`` metres of the
          path but not yet requiring emergency stop.
      * - ``EMERGENCY_STOP``
        - Vehicle brakes immediately (throttle = 0, brake = 1).
          Triggered when any fused object is within
          ``emergency_distance`` metres directly ahead.

   **Subscriptions:**

   - ``/perception/fused_objects`` -- ``vision_msgs/Detection3DArray``
   - ``/traffic/light_state`` -- ``std_msgs/String`` (from ``traffic_light_detector.py``)
   - ``/planning/path`` -- ``nav_msgs/Path`` (to check for obstacles on path)

   **Publications:**

   - ``/behavior/state`` -- ``std_msgs/String`` (current FSM state name)
   - ``/behavior/target_speed`` -- ``std_msgs/Float32`` (speed setpoint for controller)

   **State Transition Logic:**

   .. code-block:: python

      from enum import Enum, auto

      class BehaviorState(Enum):
          LANE_FOLLOW = auto()
          STOP = auto()
          OBSTACLE_AVOIDANCE = auto()
          EMERGENCY_STOP = auto()

      class BehaviorFSM:
          """
          Finite state machine for behavioral driving.
          Call update() at the FSM tick rate (e.g. 10 Hz).
          """

          def __init__(self, target_speed=8.0, slow_speed=3.0,
                       emergency_dist=5.0, obstacle_dist=15.0,
                       stop_dist=20.0):
              self.state = BehaviorState.LANE_FOLLOW
              self.target_speed = target_speed
              self.slow_speed = slow_speed
              self.emergency_dist = emergency_dist
              self.obstacle_dist = obstacle_dist
              self.stop_dist = stop_dist

          def update(self, nearest_obstacle_dist, traffic_light_state,
                     stop_sign_dist):
              """
              Determine next state given current perception inputs.

              Parameters
              ----------
              nearest_obstacle_dist : float  -- metres to nearest object on path
                                               (inf if no obstacle)
              traffic_light_state   : str    -- "RED", "YELLOW", "GREEN", "UNKNOWN"
              stop_sign_dist        : float  -- metres to nearest stop sign
                                               (inf if none)
              Returns
              -------
              BehaviorState, float -- new state and target speed
              """
              # Priority 1: Emergency stop
              if nearest_obstacle_dist < self.emergency_dist:
                  self.state = BehaviorState.EMERGENCY_STOP
                  return self.state, 0.0

              # Priority 2: Stop at red light or stop sign
              if (traffic_light_state in ("RED", "YELLOW") and
                      nearest_obstacle_dist > self.emergency_dist):
                  self.state = BehaviorState.STOP
                  return self.state, 0.0

              if stop_sign_dist < self.stop_dist:
                  self.state = BehaviorState.STOP
                  return self.state, 0.0

              # Priority 3: Slow for nearby obstacle
              if nearest_obstacle_dist < self.obstacle_dist:
                  self.state = BehaviorState.OBSTACLE_AVOIDANCE
                  return self.state, self.slow_speed

              # Default: lane following
              self.state = BehaviorState.LANE_FOLLOW
              return self.state, self.target_speed

   **Required in Report:**
   Include a state transition diagram showing all four states, all
   transition conditions (with variable names and thresholds), and
   the speed output associated with each state.

   .. tip::

      Test the FSM in isolation first using a simple Python unit test
      that calls ``update()`` with controlled inputs and asserts the
      correct output state and speed. This avoids needing CARLA running
      to debug FSM logic.

.. dropdown:: Task 4: End-to-End Integration Test (20 pts)
   :icon: gear
   :class-container: sd-border-primary

   Run the **complete ADS pipeline** in CARLA and evaluate its
   autonomous driving performance.

   **Pipeline:**

   .. code-block:: text

      GP1: sensor_manager.py  (camera, LiDAR, GNSS, IMU)
           |
      GP2: detector_node.py   (YOLO or DETR -- /perception/detections)
           |
      GP3: fusion_node.py        (/perception/fused_objects)
           localization_node.py  (/localization/pose, /localization/odom)
           |
      GP4: behavior_node.py   (/behavior/state, /behavior/target_speed)
           planner_node.py    (/planning/path)
           controller_node.py (vehicle control commands -> CARLA)

   **Required Scenarios:**

   Run the full pipeline on both provided scenarios:

   .. list-table::
      :header-rows: 1
      :widths: 20 30 50

      * - Scenario
        - Config File
        - Description
      * - Town01
        - ``town01_route.yaml``
        - Straight roads with T-intersections. ~800 m route.
          Primarily tests basic lane following and speed control.
      * - Town03
        - ``town03_route.yaml``
        - Urban grid with traffic lights, roundabouts, and
          pedestrian crossings. ~1.2 km route. Tests FSM and
          re-planning under dynamic obstacles.

   **For each scenario, record:**

   1. A ROS bag of the full autonomous run:

   .. code-block:: bash

      ros2 bag record \
          /localization/pose \
          /planning/path \
          /perception/fused_objects \
          /behavior/state \
          /behavior/target_speed \
          /carla/ego_vehicle/vehicle_control_cmd \
          /carla/ego_vehicle/collision \
          -o evaluation/rosbags/town01_run1

   2. Run the provided evaluation script:

   .. code-block:: bash

      python evaluation_metrics.py \
          --bag  evaluation/rosbags/town01_run1 \
          --route scenarios/town01_route.yaml \
          --output evaluation/metrics/town01_metrics.json \
          --plot  evaluation/plots/

   **Metrics reported by** ``evaluation_metrics.py``:

   .. list-table::
      :header-rows: 1
      :widths: 35 65

      * - Metric
        - Description
      * - Route completion (%)
        - Fraction of route checkpoints reached before timeout.
      * - Collision count
        - Number of collision events recorded by CARLA.
      * - Average speed (m/s)
        - Mean speed over the completed portion of the route.
      * - Lateral jerk (m/s\ :sup:`3`)
        - Mean absolute lateral acceleration rate -- measures
          ride smoothness.
      * - Red light violations
        - Number of times the vehicle crossed a stop line
          while the light was red.

   **Minimum Passing Bar:**

   - Route completion >= 70% on both scenarios
   - Collision count = 0 (any collision loses 5 pts)
   - At least 2 minutes of continuous autonomous driving recorded per scenario

   .. important::

      Record **at least 2 minutes** of autonomous driving per scenario.
      Runs shorter than 2 minutes will not be graded for the integration
      test component. Use CARLA's spectator camera to verify the vehicle
      is actually driving and not stuck before starting the bag recording.


Folder Structure
----------------

Your submission must follow this exact directory layout:

.. code-block:: text

   GP4_Team{X}/
   ├── ads_pipeline/                    # Extended from GP3
   │   ├── ads_pipeline/
   │   │   ├── __init__.py
   │   │   ├── sensor_manager.py        # GP1
   │   │   ├── detector_node.py         # GP2
   │   │   ├── fusion_node.py           # GP3
   │   │   ├── localization_node.py     # GP3
   │   │   ├── planner_node.py          # NEW
   │   │   ├── controller_node.py       # NEW
   │   │   ├── behavior_node.py         # NEW
   │   │   ├── waypoint_utils.py        # Provided (copied here)
   │   │   ├── carla_vehicle_control.py # Provided (copied here)
   │   │   └── traffic_light_detector.py # Provided (copied here)
   │   ├── config/
   │   │   ├── carla_config.yaml        # From GP3
   │   │   ├── detector_config.yaml     # From GP2
   │   │   ├── ekf_config.yaml          # From GP3
   │   │   ├── planner_config.yaml      # NEW
   │   │   └── controller_config.yaml   # NEW
   │   ├── launch/
   │   │   ├── sensors_launch.py        # GP1
   │   │   ├── perception_launch.py     # GP2
   │   │   ├── fusion_launch.py         # GP3
   │   │   ├── planning_launch.py       # NEW
   │   │   └── full_pipeline_launch.py  # NEW -- launches everything
   │   ├── models/                      # GP2 (YOLO/DETR weights)
   │   ├── scenarios/
   │   │   ├── town01_route.yaml        # Provided
   │   │   └── town03_route.yaml        # Provided
   │   ├── package.xml
   │   └── setup.py
   ├── evaluation/
   │   ├── rosbags/                     # ROS bag files (town01, town03)
   │   ├── metrics/                     # JSON metrics output files
   │   └── plots/                       # Generated plots (PNG/PDF)
   └── report.pdf

Replace ``{X}`` with your team number (e.g., ``GP4_Team3``).

.. important::

   ``full_pipeline_launch.py`` must launch **all** nodes (GP1 through GP4)
   with a single command:

   .. code-block:: bash

      ros2 launch ads_pipeline full_pipeline_launch.py \
          scenario:=town01_route.yaml

   The grader will use this single command to launch your system.
   If this launch file is missing or broken, the integration test
   component receives zero points.


Submission
----------

.. important::

   **Submission Instructions**

   Submit a single ``.zip`` archive named ``GP4_TeamX.zip`` (replace ``X``
   with your team number) to **Canvas** by the deadline.

   - **Deadline:** End of Week 13 (see Canvas for exact date/time)
   - **Late policy:** 10% deduction per day, maximum 3 days late
   - **One submission per team** -- designate one member to submit
   - ROS bag files are large -- zip them separately if the total archive
     exceeds 500 MB and upload the bag zip to the shared Google Drive
     folder (link on Canvas). Reference the Drive folder in your README.
   - ``report.pdf`` must be inside the archive
   - ``colcon build --packages-select ads_pipeline`` must succeed

   **This is the last group project.** GP4 will be directly evaluated
   during the final presentation in Weeks 14--15. Ensure your pipeline
   runs reliably before submitting.


Submission Checklist
--------------------

.. admonition:: Before You Submit -- Check Every Item
   :class: tip

   - [ ] ``planner_node.py`` runs, publishes ``/planning/path``, and
         re-plans on obstacle detection and path deviation
   - [ ] ``controller_node.py`` runs and publishes valid vehicle
         control commands (throttle, brake, steer all in expected range)
   - [ ] ``behavior_node.py`` runs, publishes ``/behavior/state`` and
         ``/behavior/target_speed``; all four FSM states are reachable
   - [ ] ``full_pipeline_launch.py`` launches all GP1--GP4 nodes
         with one command and accepts a ``scenario`` argument
   - [ ] ``planner_config.yaml`` and ``controller_config.yaml`` are
         present and loaded by ``planning_launch.py``
   - [ ] Town01 autonomous run recorded: bag >= 2 minutes, metrics JSON present
   - [ ] Town03 autonomous run recorded: bag >= 2 minutes, metrics JSON present
   - [ ] Evaluation plots present in ``evaluation/plots/``
   - [ ] ``report.pdf`` is present: 4--5 pages, includes FSM diagram,
         controller formulation, and quantitative metrics table
   - [ ] ``colcon build`` succeeds with no errors or warnings
   - [ ] Folder is named ``GP4_TeamX/`` (correct team number)
   - [ ] Archive is named ``GP4_TeamX.zip``
   - [ ] Peer evaluation form submitted on Canvas separately
   - [ ] If bags are on Google Drive, Drive link is in README


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Component
     - Points
     - Criteria
   * - Path Planner
     - 30
     - A* correctly implemented on CARLA waypoint graph; path
       published as ``nav_msgs/Path``; re-planning triggers work
       (obstacle on path and deviation > 2 m); goal specified
       via parameter; planner does not crash on no-path scenarios.
   * - Controller
     - 30
     - Pure Pursuit geometry correct (lookahead selection, alpha
       computation, delta formula); PID longitudinal with
       anti-windup; all gains configurable via YAML; steering
       output normalized to ``[-1, 1]``; vehicle tracks straight
       path at target speed without oscillation.
   * - Behavioral FSM
     - 20
     - All four states implemented; transitions correct per spec;
       red light stops demonstrated in Town03; obstacle avoidance
       slows vehicle; emergency stop tested; FSM state diagram
       in report matches implementation.
   * - Integration Test
     - 20
     - Full pipeline launches with one command; Town01 route
       completion >= 70%; Town03 route completion >= 70%;
       zero collisions; ROS bags >= 2 min each; metrics JSON
       present and verifiable; evaluation plots included.


Common Mistakes
---------------

.. danger::

   **Avoid These Common Errors**

   - **Calling CARLA API from a ROS callback thread.** The CARLA Python
     client is not thread-safe. All ``world.get_actors()``,
     ``waypoint.get_next()``, and similar calls must happen in the
     main thread (timer callbacks), not inside subscriber callbacks.
     Use a shared-memory queue to pass data between callbacks and
     the planner timer.

   - **Not normalizing the Pure Pursuit angle** ``alpha``. If you do not
     wrap ``alpha`` to ``[-pi, pi]``, the steering will reverse direction
     when the lookahead point crosses behind the vehicle. Always apply
     ``alpha = (alpha + pi) % (2*pi) - pi``.

   - **Forgetting anti-windup in PID.** Without clamping the integrator,
     the vehicle will oscillate around stop-and-go scenarios because
     accumulated error causes large overshoot when the vehicle starts
     moving again.

   - **Publishing raw CARLA steering without normalization.** CARLA
     expects steering in ``[-1, 1]``. Raw Pure Pursuit output is in
     radians (typically ``[-0.7, 0.7]`` for a car). Divide by
     ``max_steer_angle`` before publishing.

   - **Missing** ``full_pipeline_launch.py``. This is the single most
     common reason for zero points on the integration test. Verify it
     works with a fresh ``colcon build`` in a clean workspace before
     submitting.

   - **Hardcoding the goal position.** The grader may test with a
     different goal. The goal must be a ROS 2 parameter loadable from
     ``planner_config.yaml``.

   - **Not testing in Town03.** Town03 has traffic lights and
     intersections that exercise the FSM. If you only test in Town01
     (no traffic lights), your FSM ``STOP`` state will be untested and
     the grader will deduct points.

   - **ROS bag too short.** Bags under 2 minutes will not be graded for
     the integration component. Verify bag duration with
     ``ros2 bag info <bag_folder>`` before submitting.


Tips for Success
----------------

.. tip::

   **Build and test incrementally.** Test the planner in isolation by
   publishing a fake ``/localization/pose`` with a static publisher
   and visualizing ``/planning/path`` in RViz before connecting it to
   the controller. Add one node at a time.

.. tip::

   **Use RViz throughout.** Add these displays to your RViz config:

   - ``nav_msgs/Path`` on ``/planning/path`` -- visualize the planned path as a line
   - ``geometry_msgs/PoseStamped`` on ``/localization/pose`` -- vehicle position arrow
   - ``vision_msgs/Detection3DArray`` on ``/perception/fused_objects`` -- 3D boxes
   - ``std_msgs/String`` on ``/behavior/state`` -- current FSM state (text display)

   Seeing all four in one RViz window catches integration bugs in seconds.

.. tip::

   **Tune Pure Pursuit lookahead for your test scenario.** A lookahead
   of 5--8 m works well for Town01 straight roads. For Town03
   intersections, reduce to 3--5 m so the vehicle starts turning
   earlier. Make ``lookahead_distance`` a parameter so you can tune
   without recompiling.

.. tip::

   **Record bags early and often.** Start recording before the run,
   not after. A 5-minute bag of a failed run is more useful for
   debugging than no bag at all. Name bags descriptively:
   ``town01_run1``, ``town03_after_tuning``, etc.

.. tip::

   **Divide the work clearly.** A natural GP4 split:
   one member on ``planner_node.py`` (A* + re-planning),
   one on ``controller_node.py`` (Pure Pursuit + PID),
   one on ``behavior_node.py`` (FSM + integration),
   one on ``full_pipeline_launch.py`` + evaluation + report.
   All members should run the full pipeline together at least once
   before the final submission.

.. tip::

   **GP4 is demonstrated live.** During the final presentation
   (Weeks 14--15), the grader will launch your pipeline on an
   unseen scenario. Practice the full-pipeline launch command
   until it works reliably from a clean terminal. Know how to
   restart CARLA and your pipeline quickly if something goes wrong.
