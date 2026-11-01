====================================================
GP4: Planning & Control
====================================================

.. admonition:: The Situation
   :class: story

   Your robotaxi now knows where it is and where every car and person around
   it is, with their speeds: your GP3 pipeline. It still has a safety driver
   at the wheel.

   The company's first driverless test is a trip across Town01: from a
   pick-up point to a drop-off point, through junctions and traffic lights,
   with cars and people around. The test has three rules:

   1. **Follow the route** the car plans for itself.
   2. **Stop at red lights,** and slow down or stop for cars and people in
      the way.
   3. **Search for a new route** when a parked vehicle blocks it or the car
      leaves it.

   GP4 closes the loop: the car plans its route, decides how fast to go, and
   turns the wheel, with every earlier part of your pipeline running live.

.. card:: GP4: At a Glance
   :class-card: sd-shadow-sm

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 2 weeks of work: posted **Thursday, November 19**, due **Thursday,
          December 10** (the Thanksgiving week, Nov 25 to 29, is not counted)
      * - **Weight**
        - 20% of the group-project grade: 17.0% of the final project grade,
          13.6% of the course grade
      * - **Lectures**
        - L7 (route planning, re-planning), L8 (constant-velocity prediction),
          L10 (Pure Pursuit, PID); L9 for the report's discussion
      * - **Starter code**
        - `gp4_starter <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/tree/main/gp4_starter>`__
          and `ads_msgs <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/tree/main/ads_msgs>`__
          (now with ``VehicleCmd``) in the course repository
      * - **Team Size**
        - 3 students, the GP1 team
      * - **Submission**
        - Canvas + the ``gp4`` branch of your GP1 repository


.. admonition:: AI Disclosure (required)
   :class: warning

   You may use AI tools on GP4. You must say so in your ``README.md``.

   Name the tool and describe how you used it, two or three sentences per
   team member. Disclosure carries no penalty. **Undisclosed use is a
   violation of the Code of Academic Integrity.**

   Your team is responsible for every line you submit. Any member may be
   asked, in class or office hours, to walk through any part of the code:
   why it works, what would break it, what you would change. **Work that
   cannot be explained does not count**, even if it runs.

   Read :ref:`ai-disclosure` for the full rules on what is permitted and
   what is not.


Overview
--------

GP4 drives the car with your whole pipeline, live in CARLA:

.. figure:: /_static/images/GP4/gp4_flow.png
   :alt: A flow diagram of the closed loop. Top row, left to right: GP1's sensor_manager, green, sends the camera to GP2's detector_node, blue; its boxes go to GP3's fusion_node, purple, whose objects go to GP3's tracker_node, purple; sensor_manager also sends LiDAR along the top to fusion_node and on, down the right side of tracker_node, to behavior_node. sensor_manager sends IMU and GNSS down to GP3's localization_node, purple, whose pose goes to planner_node, red. Middle row: planner_node sends the path to behavior_node, red, which also gets tracks from tracker_node and the traffic light from a gray ground truth box on the right; tracker_node also sends standing vehicles to planner_node. Bottom: controller_node, red, gets the path from planner_node, pose and speed from localization_node, and the target speed from behavior_node, and sends /control/vehicle_cmd back to sensor_manager along the bottom and up the left side. A legend: green GP1, blue GP2, purple GP3, red GP4: yours, gray given.
   :align: center
   :width: 100%

   How GP4 closes the loop with GP1, GP2 and GP3. **Green:** GP1's code;
   **blue:** GP2's; **purple:** GP3's; **red:** the GP4 nodes you write;
   **gray:** given. Every arrow carries a ROS 2 topic. The command goes back
   to your GP1 node, which waits for it before the next simulation step.

**Our reference, running.** The video below shows our reference GP4 pipeline
driving rig A's route (535 m) in closed loop, with its EKF pose, 40 other
vehicles and 80 people. It plays at normal speed: 130 s of simulated time.

.. raw:: html

   <video controls preload="metadata" width="100%"
          poster="../_static/images/GP4/gp4_video_poster.png">
     <source src="../_static/videos/gp4_reference.mp4" type="video/mp4">
     Your browser cannot play this video. The description below says what it shows.
   </video>

*What the video shows* (it has no sound). **Left:** a camera that follows
the car from behind. It is only for the video; the pipeline does not use
it. **Right:** a top view 80 m across, centered on the car: the lane
centers from the map (light gray), the planned path (red) with the goal at
its end (red star), the true car (black triangle), the EKF's pose (orange
dot) and the tracks (purple squares, with speed arrows). The title gives
the behavior state, its target speed and the car's speed.

The car follows its lane at up to 8.1 m/s. At 58 s, a person on the right
is walking toward the road: their track's position 2 s ahead comes within
3 m of our path, so the behavior node stops the car (from 7.4 m/s to 0 at
58.4 s), and it drives on once the person's track no longer counts as
ahead. At 66 s, a car coming the other way and a person on the right stop
it again (from 7.3 m/s to 0 at 67.4 s). From 89 s to 121 s the car waits at a red
light, 11 m before the goal. It then comes within 2 m of the goal at
124.5 s and stops 0.35 m from it. Scored to arrival, the run had no
collision, no pedestrian hit and no red-light violation; the EKF's error was
0.44 m RMSE and the mean cross-track error 0.28 m.

.. list-table::
   :widths: 26 14 60
   :header-rows: 1
   :class: compact-table

   * - **Task**
     - **Lecture**
     - **What it adds**
   * - 1. Close the loop (15 pts)
     - L10
     - Your GP1 node applies the controller's command and waits for it
       before the next simulation step.
   * - 2. Route planner (25 pts)
     - L7
     - A* on the road network, and a new search when a car is parked in the
       way or the car leaves its route.
   * - 3. Controller (25 pts)
     - L10
     - Pure Pursuit for steering, a PID with anti-windup for speed.
   * - 4. Behavior (20 pts)
     - L8
     - Follow, slow down, stop at red lights, stop in an emergency, using
       your GP3 tracks' speeds.
   * - 5. Report (15 pts)
     - all
     - Your runs, what your EKF costs the controller, and one failure.

**What GP4 reuses.** Every task starts from code your team wrote:

.. list-table::
   :widths: 24 40 36
   :header-rows: 1
   :class: compact-table

   * - **Task**
     - **Your code it builds on**
     - **What is new**
   * - 1. Close the loop
     - GP1's ``sensor_manager.py`` and YAML (your vehicle, your sensors);
       GP3's ground truth and traffic
     - Apply the command at each step; wait for it (lock step)
   * - 2. Planner
     - GP3's pose (start, deviation) and tracks (parked cars)
     - A* and the two triggers
   * - 3. Controller
     - GP3's pose and speed (``/localization/odom``)
     - Pure Pursuit and the PID
   * - 4. Behavior
     - GP3's tracks with their speeds
     - The state machine

.. note::

   **If GP3 did not work for your team,** use the GP3 reference
   implementation released on Canvas: GP4 needs GP3's pose and tracks.


Learning Objectives
-------------------

After completing GP4, you will be able to:

- Search a road network with A*, explain why the straight-line heuristic
  never overestimates, and check routes against CARLA's own planner.
- Decide when a route must be searched again, and keep a trigger from
  firing again and again.
- Steer with Pure Pursuit at the rear axle, and control speed with a PID
  that does not wind up.
- Write a state machine where the safer state always wins, and use a
  constant-velocity prediction to see a person about to step into the road.
- Run a closed loop where the simulation waits for the controller, and
  measure a drive: route completion, collisions, red-light violations,
  cross-track error.
- Measure what localization error costs the controller.


Provided Resources
------------------

1. Update the course repository and rebuild ``ads_msgs`` (it now has
   ``VehicleCmd``: throttle, steer, brake):

   .. code-block:: bash

      cd ~/enpm818z_ws/src/enpm818z-fall-2026-carla-ros && git pull
      cd ~/enpm818z_ws && colcon build --packages-select ads_msgs && source install/setup.bash

2. Start the ``gp4`` branch from your GP3 submission:

   .. code-block:: bash

      cd ~/enpm818z_ws/src/GP1_TeamX && git checkout -b gp4 gp3-final

3. Copy the GP4 files into your package. One file has the same name as a
   GP3 file on purpose: ``ground_truth.py``. The GP4 version adds the
   collision sensor and the traffic light, and keeps everything GP3 used.
   Check for other files with the same name first:

   .. code-block:: bash

      (cd ../enpm818z-fall-2026-carla-ros/gp4_starter/ads_pipeline && find . -type f -printf '%P\n') | while read -r f; do [ -e "ads_pipeline/$f" ] && echo "already exists: ads_pipeline/$f"; done
      cp -r ../enpm818z-fall-2026-carla-ros/gp4_starter/ads_pipeline/. ads_pipeline/

   The only line printed should be ``ads_pipeline/ads_pipeline/ground_truth.py``.

4. Add the GP4 nodes to ``setup.py``, in ``console_scripts``:

   .. code-block:: python

      'planner_node = ads_pipeline.planner_node:main',
      'behavior_node = ads_pipeline.behavior_node:main',
      'controller_node = ads_pipeline.controller_node:main',

5. Check: ``python3 -m pytest test/ -k gp4`` runs. Most GP4 tests fail with
   ``NotImplementedError`` until you write the functions marked YOURS, and
   ``test_gp4_lockstep.py`` fails to import until you finish Task 1.

What the starter contains
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 20 50
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **Status**
     - **What it does**
   * - ``route_graph.py``
     - Given
     - The road network as a graph, read from the map file with no CARLA
       server: a node every 2 m along each lane, and lane changes where the
       road markings allow them.
   * - ``planner_core.py``
     - **Yours:** ``astar_waypoints``, ``obstacle_on_path``, ``off_path``
     - Given: ``Hysteresis``.
   * - ``planner_node.py``
     - Given
     - Plans at the first pose, checks both triggers twice a second,
       publishes ``/planning/path``.
   * - ``controller_core.py``
     - **Yours:** ``pure_pursuit_steer``, ``PIDController.compute``
     - Given: the command conversion and the start-up creep.
   * - ``controller_node.py``
     - Given
     - Answers every target speed with one ``VehicleCmd``, stamped for the
       lock step.
   * - ``bicycle_sim.py``
     - Given
     - Tunes your controller offline, with no CARLA.
   * - ``behavior_core.py``
     - **Yours:** ``BehaviorFSM.update``
     - Given: ``nearest_ahead`` (the constant-velocity look-ahead) and the
       start-up branch.
   * - ``behavior_node.py``
     - Given
     - Answers every tracks message with a target speed; holds the car at
       the goal.
   * - ``ground_truth.py``
     - Given
     - GP3's helper plus collisions and the traffic light (grading and the
       behavior node's light only).
   * - ``tools/evaluate_run.py``
     - Given
     - Scores a run (see Task 5).


Your Team's Values
------------------

Your route starts at a Town01 spawn point and ends at a goal on the road.
Find your rig letter on Canvas (the same rig as in GP1 to GP3). Your route
file is ``routes/<rig>.yaml``.

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Rig
     - spawn_index
     - Goal (x, y) m
     - Length (m)
     - Junctions
     - Lights
   * - A
     - 71
     - (327.72, -330.61)
     - 535.2
     - 2
     - 2
   * - B
     - 114
     - (167.62, -330.6)
     - 577.6
     - 7
     - 7
   * - C
     - 128
     - (-2.05, -71.96)
     - 618.9
     - 5
     - 5
   * - D
     - 109
     - (99.6, -330.46)
     - 619.4
     - 7
     - 7
   * - E
     - 154
     - (158.06, -20.2)
     - 534.9
     - 4
     - 5

Your vehicle is your GP1 rig's. We measured its wheels in CARLA:

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Rig
     - Vehicle
     - Wheelbase (m)
     - Rear axle behind the car's origin (m)
   * - A
     - ``vehicle.toyota.prius``
     - 2.819
     - 1.399
   * - B
     - ``vehicle.chevrolet.impala``
     - 2.982
     - 1.329
   * - C
     - ``vehicle.jeep.wrangler_rubicon``
     - 2.308
     - 1.017
   * - D
     - ``vehicle.audi.a2``
     - 2.506
     - 1.257
   * - E
     - ``vehicle.bmw.grandtourer``
     - 2.935
     - 1.443

Put both into ``config/controller_config.yaml`` (``wheelbase``,
``rear_offset``). Every vehicle's front wheels turn 70 degrees (1.222 rad) at
full steering in CARLA: that is ``max_steer_angle``, and your controller
never asks for more than ``steer_limit``, 0.7 rad.


Tasks
-----

.. dropdown:: Task 1: Close the Loop (15 pts)
   :icon: goal
   :class-container: sd-border-primary

   Your GP1 ``sensor_manager`` ticks the world on a timer. In GP4 the
   controller drives, so each step must wait for its answer.

   **Step 1: Two functions** at module level in ``sensor_manager.py``:

   - ``ready_to_tick(last_tick_stamp, last_cmd_stamp, waited_s, timeout_s)``
     returns ``(tick_now, timed_out)``. Tick when the last command's stamp
     is at or after the last tick's stamp (a 1 ms margin), or when
     ``timeout_s`` seconds of waiting have passed (then ``timed_out`` is
     true). The first tick needs no command.
   - ``to_carla_control(cmd)`` returns the ``carla.VehicleControl``
     arguments as a dict. ``VehicleCmd.steer`` is positive to the LEFT;
     CARLA's ``steer`` is positive to the RIGHT (its y axis points right).

   **Step 2: The lock step.** Add the parameters ``lock_step`` (default
   false, so GP1 to GP3 behave as before) and ``cmd_timeout_s`` (2.0).
   With ``lock_step``: subscribe to ``/control/vehicle_cmd``; poll in the
   timer callback every 5 ms; tick only when ``ready_to_tick`` says so, and
   log every timeout with its count; apply the last command with
   ``vehicle.apply_control(carla.VehicleControl(**to_carla_control(cmd)))``
   before ``world.tick()``.

   **Step 3: Ground truth for GP4.** Create ``GroundTruth(...,
   gp4=self.p('lock_step'))`` and add its ``actors`` to the list your node
   destroys: it attaches a collision sensor.

   **Step 4: Run it.** ``gp4_launch.py`` starts your whole pipeline with
   ``lock_step`` on (Task 5 has the command). On day 1, before Tasks 2 to 4
   work, the given controller already answers every frame: it creeps
   straight at 2 m/s until the first pose and the first path.

   **Evidence:** ``results/gp4/lockstep.txt``: ``ros2 topic hz
   /control/vehicle_cmd`` during a run, and your log's timeout count.

   **Tests:** ``python3 -m pytest test/test_gp4_lockstep.py test/test_gp4_ground_truth.py -v``.

.. dropdown:: Task 2: Route Planner (25 pts)
   :icon: goal
   :class-container: sd-border-primary

   **The graph** (``route_graph.py``, given) has a node every 2 m along
   every lane of the map, an edge to the next node along the lane, and an
   edge to the neighbor lane where the road markings allow a lane change.
   Town01 has 3107 nodes and 3143 edges; it has one lane each way, so no
   lane changes. Town03 has 6647 nodes and 2753 lane-change edges.

   **Yours: astar_waypoints.** A* from the node nearest the car to the node
   nearest your goal, with the straight-line distance to the goal as the
   heuristic. It returns the node list, or ``None`` when no route exists or
   after ``max_astar_nodes`` (10,000) expansions.

   **The tests compare your routes with CARLA's own planner,**
   ``GlobalRoutePlanner``, on three Town01 and two Town03 trips; we
   computed its routes once and stored their lengths. On Town01 both graphs
   are the same, so the lengths must agree within 4 m. On Town03, CARLA
   allows a lane change only once per road segment; your graph allows one
   wherever the markings do, so your route may be shorter than CARLA's,
   never longer by more than a lane width (4 m) per lane change. Do not
   import CARLA's planner in your node.

   **Yours: the two triggers.** ``obstacle_on_path``: an object's center
   within ``obstacle_clearance`` (3.0 m) of a waypoint. ``off_path``: the
   car more than ``max_deviation`` (2.0 m) from the nearest waypoint.

   **What the given node does with them,** twice a second:

   - Trigger 1 counts only standing vehicles (vehicle tracks slower than
     0.5 m/s) on the path ahead of the car, and not those within 30 m of a
     traffic light's stop line, which are most likely queued at the light. It closes the graph's edges
     within 3.0 m of the vehicle and searches again. Town01's lanes are
     one-way: when no route avoids the vehicle, the node reopens the edges
     and keeps the path, and your behavior node stops for it.
   - Trigger 2 searches again from the node nearest the car.
   - A trigger that stays on starts one search, not one per check: the
     given ``Hysteresis`` waits until the trigger has been off for 1 s.

   **Tests:** ``python3 -m pytest test/test_gp4_route_graph.py test/test_gp4_planner.py test/test_gp4_triggers.py -v``.

.. dropdown:: Task 3: Controller (25 pts)
   :icon: goal
   :class-container: sd-border-primary

   **Yours: pure_pursuit_steer.** From the middle of the rear axle (the
   given node moves your EKF's pose back by your ``rear_offset``), find the
   goal point where the path leaves the circle of radius :math:`L_d` (the
   lookahead), put it in the car's frame, and return the wheel angle
   :math:`\delta = \arctan(2 L \sin\alpha / L_d)`, where :math:`L` is the
   wheelbase and :math:`\alpha` the angle from the car's heading to the
   goal point. The test is the
   worked example: rear axle at (82.50, -0.07) m, heading -0.0796 rad,
   goal point (87.22, -1.72) m, wheelbase 2.875 m: -0.285 rad.

   **The lookahead (given).** The node sets :math:`L_d` to
   ``lookahead_distance`` (5 m) or to ``lookahead_time`` (1 s) times the
   car's speed, whichever is longer. Your EKF's pose jumps a little at each
   GNSS fix (0.24 m within 0.05 s, at the 99th percentile, in our run), and
   a 5 m lookahead turns each jump into a swerve. In our offline test with
   our EKF's measured error, the longer lookahead at speed cut the
   step-to-step change of the steering command by almost half (its standard
   deviation went from 0.021 to 0.011).

   **Yours: PIDController.compute.** Kp, Ki and Kd on the speed error, with
   the integral of the error held within ``pid_windup_limit`` (2.0), and
   the output clamped to [-1, 1]: positive is throttle, negative brake.

   **Speed in curves and at the goal (given).** The controller node caps
   the behavior node's target so the car can slow, at 2.0 m/s², to
   :math:`\sqrt{a_{lat} / \kappa}` (``a_lat`` 2.0 m/s²) on every curve in
   the next 40 m of path, where :math:`\kappa` is the path's curvature.
   Once the goal is within those 40 m, the cap also lets the car stop at
   the goal. Without the curve cap, our car took junction turns at 7 m/s
   and left its lane. Without the goal cap, it drove past its goal at
   5.1 m/s.

   **Tune offline first.** ``bicycle_sim.track`` drives a path with your
   two functions, with steering and engine lags. On the test curve, our
   reference's largest cross-track error is 0.458 m with a 5 m lookahead
   (0.195 m with 3 m, 0.821 m with 8 m: a longer lookahead cuts the
   corners). The test allows 0.69 m.

   **Tests:** ``python3 -m pytest test/test_gp4_controller.py -v``.

.. dropdown:: Task 4: Behavior (20 pts)
   :icon: goal
   :class-container: sd-border-primary

   **Yours: BehaviorFSM.update.** Four states; when more than one holds,
   the safer state wins:

   1. ``EMERGENCY_STOP`` (0 m/s): no route, or an object within
      ``emergency_distance`` (8.0 m) ahead.
   2. ``STOP`` (0 m/s): a red or yellow light whose stop line is ahead of
      the car and within ``stop_distance`` (20 m). A light that turns red
      after the car has passed its stop line does not stop it in the
      junction.
   3. ``OBSTACLE_AVOIDANCE`` (``slow_speed``, 3 m/s): an object within
      ``obstacle_distance`` (15 m) ahead.
   4. ``LANE_FOLLOW`` (``target_speed``, 8 m/s).

   **What counts as ahead** (given, ``nearest_ahead``): an object whose
   constant-velocity position over the next ``lookahead_s`` (2.0 s) comes
   within 3.0 m of the path ahead of the car. A person 6 m from the path,
   walking toward it at 1.5 m/s, counts: in 2 s they are 3 m from it.

   **Given:** before the first path the car creeps at 2 m/s (the EKF needs
   the car to move 3 m before it publishes a pose), and at the goal the
   node holds the car.

   **Given: the LiDAR stop check.** The camera misses a vehicle close ahead:
   at 4.8 m, the back of a box truck fills the whole image, and the
   detector calls it a stop sign. With no box there is no fused object and
   no track, so ``BehaviorFSM.update`` sees an empty road. The node also
   reads the LiDAR. It keeps the points 0.3 m to 2.5 m above the road and
   in front of the car, and when at least 5 of them lie within 1.1 m of
   the path, closer than the car can stop, the state is ``EMERGENCY_STOP``
   whatever the tracks say. "Closer than the car can stop" is 2.5 m (the
   car's front), plus :math:`v^2 / (2 \cdot 4.0)` m (braking at
   4.0 m/s² from the car's speed :math:`v`), plus 2 m of margin. Without it, our car drove
   into a truck twice in each of four runs of one route.

   **Tests:** ``python3 -m pytest test/test_gp4_behavior.py -v``.

.. dropdown:: Task 5: Runs and Report (15 pts)
   :icon: goal
   :class-container: sd-border-primary

   **Run your route** twice: with your EKF, and with the true pose (for the
   comparison):

   .. code-block:: bash

      ros2 launch ads_pipeline gp4_launch.py config:=$PWD/config/carla_config.yaml \
          route_file:=$PWD/routes/<rig>.yaml spawn_index:=<from the table> \
          map_file:=$PWD/ads_pipeline/maps/Town01.xodr \
          weights:=yolov8s.pt out:=$HOME/gp4_data/run_ekf
      ros2 launch ... pose_topic:=/ground_truth/ego out:=$HOME/gp4_data/run_truth
      python3 -m tools.evaluate_run --bag $HOME/gp4_data/run_ekf --out ../results/gp4/metrics_ekf.json

   Set ``traffic.vehicles: 40`` and ``traffic.walkers: 80`` in your YAML.
   ``evaluate_run.py`` scores the drive until the car first comes within
   2 m of the goal: route completion (1 at arrival; otherwise 1 minus the
   road distance still left to the goal over the route's length, so a
   detour counts as progress), collisions, pedestrian hits, red-light
   violations (leaving a light's area on red faster than 1 m/s),
   cross-track error and mean speed. CARLA's collision sensor misses
   people, so a pedestrian hit is a person whose center enters the car's
   outline (2.5 m ahead and behind, 1.1 m to each side) while the car moves
   faster than 0.5 m/s.

   **Our reference** on rig A's route (535 m, 40 vehicles and 80 people):
   with the true pose, the car arrived in 160.3 s of simulated time, with a
   mean cross-track error of 0.018 m; with the EKF, in 124.4 s, with
   0.291 m. Neither run had a collision, a pedestrian hit or a red-light
   violation. Each run took about 5 minutes of wall time on an RTX 4060
   laptop GPU. The traffic differs from run to run, even with the same
   seed, so one route gives different numbers: in two of our earlier runs
   of this route with the same code and the EKF, the car arrived in 89.6 s
   and in 124.1 s. With a 1600 x 900 or 1920 x 1080
   camera the detector is slower and the lock step times out more often
   (301 to 407 times in our runs); the run still works, it takes 19 to 25
   minutes.

   **The report,** ``gp4_report.pdf``, at most 5 pages:

   1. Both runs' metrics, from the JSON files.
   2. What your EKF costs: cross-track error and speed with your EKF
      against the true pose, and whether trigger 2 fired because of it.
   3. One failure, with its time: what each node published then, and the
      cause. Our first run had one: a vehicle about 5 m away that the
      tracker did not report.
   4. Re-planning: when your two triggers fired in your runs, and what the
      planner did. In our tests with a car parked just past a junction,
      the tracker first reported it 14.5 to 23.2 m ahead on three routes
      out of five and never on the other two: after the junction where the
      car could have turned off, so on Town01's one-way roads the planner
      kept the route.
   5. Your tuning: lookahead, PID gains, ``lookahead_s``, and why.
   6. AI disclosure in ``README.md``, per member.


Suggested Schedule
------------------

.. list-table::
   :widths: 18 40 42
   :header-rows: 1
   :class: compact-table

   * - Days
     - Milestone
     - Done when
   * - Nov 19 to 21
     - Starter copied; Task 1 (lock step)
     - The car creeps under the given controller, 0 timeouts
   * - Nov 22 to 24
     - Tasks 2, 3 and 4 offline: one person per task
     - Each task's tests pass
   * - Nov 25 to 29
     - Thanksgiving: nothing scheduled
     -
   * - Nov 30 to Dec 4
     - Closed loop on your route, tuning
     - The route completes with your EKF
   * - Dec 5 to 8
     - Both runs, the report
     - Checklist below fully ticked
   * - Dec 9 to 10
     - **Slack**
     - Nothing scheduled


Submission
----------

.. important::

   **Submission Instructions**

   1. Push the ``gp4`` branch to your team's private repository.
   2. Keep the instructor, GitHub user ``rubixcubic``, as a collaborator.
   3. Tag the submission commit: ``git tag gp4-final && git push --tags``.
   4. Submit the repository link and ``gp4_report.pdf`` on Canvas by the
      deadline.
   5. Email your peer evaluation within 48 hours (see
      :ref:`peer-evaluation`).


Submission Checklist
--------------------

.. admonition:: Before Submitting: Check Every Item
   :class: tip

   - [ ] ``colcon build --packages-up-to ads_pipeline`` succeeds.
   - [ ] ``python3 -m pytest test/ -k gp4`` passes, with nothing skipped.
   - [ ] ``controller_config.yaml`` holds your wheelbase and rear offset.
   - [ ] ``results/gp4/lockstep.txt``, ``metrics_ekf.json``,
         ``metrics_truth.json`` saved.
   - [ ] No bags committed.
   - [ ] AI use disclosed in ``README.md``, per member.
   - [ ] Commit tagged ``gp4-final`` and pushed; ``gp4_report.pdf`` on Canvas.
   - [ ] Peer evaluation emailed within 48 hours (see :ref:`peer-evaluation`).


Grading Rubric
--------------

Total: **100 points**, scaled to 20% of the group-project grade (17.0% of
the final project grade).

The grader also runs your pipeline on a **held-out route**: another
Town01 route for your rig, with the true pose (``pose_topic:=/ground_truth/ego``),
so it measures your GP4 code and not your GP3 EKF. "Reference" means our
reference solution on the same route, with your vehicle. The factors are
the margins chosen for GP4.

.. list-table::
   :widths: 26 10 64
   :header-rows: 1
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - Task 1: Close the loop
     - 15
     - **8** the lock-step tests pass. **4** no timeouts in a normal run
       (``lockstep.txt``). **3** the ground-truth tests pass.
   * - Task 2: Planner
     - 25
     - **12** the planner and trigger tests pass. **13** held-out route:
       route completion at least 0.8 times the reference's.
   * - Task 3: Controller
     - 25
     - **12** the controller tests pass. **13** held-out route: mean
       cross-track error at most 1.5 times the reference's.
   * - Task 4: Behavior
     - 20
     - **10** the behavior tests pass. **10** held-out route: no more
       red-light violations and no more pedestrian hits than the reference,
       and collisions at most the reference's plus one.
   * - Task 5: Report
     - 15
     - **4** both runs' metrics. **4** what the EKF costs. **3** one failure,
       with its time. **2** re-planning. **2** the tuning.

.. note::

   **Individual grade** = 60% team grade for GP4 + 40% peer review score, as
   for every project (:ref:`peer-evaluation`).


Common Mistakes
---------------

.. danger::

   - **The steering sign.** ``VehicleCmd.steer`` turns left when positive;
     CARLA's ``steer`` turns right. A wrong sign drives the car off the
     road at the first bend.
   - **Dividing by 0.7.** The wheel turns 1.222 rad at full steering, so
     ``steer = delta / 1.222``. Dividing by 0.7 turns the wheels 1.75 times
     too far.
   - **Steering from the car's center.** Pure Pursuit works at the rear
     axle. The given node moves the pose there with your ``rear_offset``:
     set it.
   - **An integral that winds up.** At a red light the speed error stays at
     8 m/s for 30 s. Without the clamp, the car lurches when the light
     turns green.
   - **Waiting forever.** If a node stops publishing, the lock step ticks
     after ``cmd_timeout_s`` and logs it: read your timeout count.
   - **Committing a bag.**
