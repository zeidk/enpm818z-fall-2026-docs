====================================================
GP1: Sensor Suite & Data Pipeline
====================================================

.. card::
   :class-card: sd-bg-dark sd-text-white sd-shadow-sm

   **GP1 -- At a Glance**

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 3 weeks (Week 3 -- Week 6)
      * - **Weight**
        - 15 points (15% of final project)
      * - **Lectures**
        - L1--L2
      * - **Team Size**
        - 4 students
      * - **Submission**
        - Canvas + GitHub repository link


Overview
--------

GP1 builds the ``ads_pipeline`` ROS 2 package that GP2, GP3 and GP4 all
extend. Everything you write here you will still be using in December, so
the structure matters as much as the behaviour.

But the package is the vehicle, not the destination. The point of GP1 is one
specific capability, and the other four tasks exist to make it possible.

Why the Projection Is the Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L2 put it like this. **A LiDAR reports metres from itself. A camera reports
rows and columns of pixels. Nothing in either measurement says whether the
two are looking at the same object.**

Picture what each sensor actually gives you.

.. list-table::
   :widths: 20 44 36
   :header-rows: 1
   :class: table-hover

   * - **Sensor**
     - **What it knows**
     - **What it cannot tell you**
   * - LiDAR
     - Something is 23 m ahead and 1.8 m wide, measured to the centimetre.
     - What that something is. A pedestrian and a bollard are both just
       returns.
   * - Camera
     - That is a pedestrian, and they are facing away from you.
     - How far away they are, to any useful accuracy.

Each one holds exactly the half the other is missing, and a planner needs
both halves at once. It cannot brake for "an object at 23 m" without knowing
whether it is a person or a postbox, and it cannot brake for "a pedestrian"
without knowing where they are.

The trouble is that those two statements live in **different coordinate
systems**, so there is no way even to ask whether they describe the same
thing. Projecting the LiDAR points into the camera image is what makes that
question askable. Once every LiDAR return has a pixel, a detection box can
acquire a distance and a distance can acquire a label.

.. important::

   **This is the step every later project is built on.**

   - **GP2** produces detections as boxes in the image. A box on its own is
     not a thing in the world. The projection is what turns it into one.
   - **GP3** fuses and tracks those objects over time, which requires them
     to be in one frame to begin with.
   - **GP4** plans around them, which requires knowing both where they are
     and what they are.

   If the projection is wrong in GP1, everything downstream inherits the
   error, and nothing downstream will tell you.

.. warning::

   **The failure mode is quiet, which is why this is worth doing carefully
   now.**

   Get the extrinsic wrong and the points still land somewhere. They look
   plausible. What actually happens is that a label attaches to the wrong
   object, so a pedestrian's identity ends up on the parked car beside them,
   or one real object becomes two tracked objects.

   Nothing raises an error, and the error grows with range. L2 measured it:
   one degree of rotation error is 1.75 m of lateral error at 100 m, about
   the width of a car. On a bench at 5 m the same error is 9 cm and looks
   like noise.

.. note::

   **Projection is not fusion, and GP1 does not ask for fusion.**

   The projection tells you which pixel a LiDAR point lands on. It does not
   tell you whether the thing at that pixel and the thing the laser hit are
   the same object. Deciding that is **data association**, and combining the
   two into one estimate is **fusion**. Both are L3, and both are GP3.

What the Other Four Tasks Are For
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Read in that light, GP1 stops being five unrelated chores.

.. list-table::
   :widths: 26 74
   :header-rows: 1
   :class: compact-table

   * - **Task**
     - **Why the projection needs it**
   * - 1. Package setup
     - Somewhere for all of it to live, structured so GP2 to GP4 can extend
       it rather than rewrite it.
   * - 2. Sensor suite
     - You cannot project one sensor into another until both are running,
       mounted at known positions, and publishing.
   * - 3. Recording
     - The projection needs a camera frame and a LiDAR sweep **from the same
       instant**. Getting that is a timing problem, which is what Task 3
       makes you look at directly.
   * - 4. RViz2
     - The fastest way to see that your frames and transforms are right
       before you start debugging arithmetic.
   * - 5. Projection
     - The capability itself.

By the end of GP1 your team will have a ROS 2 package connected to CARLA, an
ego vehicle carrying the full sensor suite with every parameter in YAML, the
streams recorded to a rosbag and verified on playback, an RViz2 view of all
of them at once, and LiDAR points landing where they belong in the camera
image.

.. important::

   This package is the ``ads_pipeline`` skeleton. Every file you create here
   is inherited by GP2, GP3 and GP4. Follow the required folder structure
   exactly, because the later projects assume it.


Learning Objectives
-------------------

After completing GP1, you will be able to:

- Create a ROS 2 Python package with correct ``package.xml``, ``setup.py``,
  and launch file structure.
- Connect to CARLA from a ROS 2 node and spawn a vehicle with multiple sensors
  using the Blueprint Library.
- Publish sensor data on standard ROS 2 message types (``sensor_msgs``,
  ``nav_msgs``).
- Record and replay sensor streams using ``ros2 bag``.
- Visualize heterogeneous sensor modalities in RViz2.
- Apply extrinsic calibration to project LiDAR points onto a camera image,
  and explain what that makes possible that neither sensor could do alone.


.. _gp1-provided-resources:

Provided Resources
------------------

Everything you need is in one repository:

.. code-block:: bash

   cd ~/enpm818z_ws/src
   git clone https://github.com/zeidk/enpm818z-fall-2026-gp1-starter.git GP1_TeamX
   cd GP1_TeamX

Rename the directory to your own team letter as you clone it, as above. That
name is what the folder structure and the submission checklist expect.

.. important::

   **Do not fork into a public repository.** Your work is coursework, and a
   public fork is visible to every other team. Either clone and push to a
   private team repository, or use the private fork GitHub Classroom hands
   you if your section is using it.

What the starter contains
~~~~~~~~~~~~~~~~~~~~~~~~~

The message-format plumbing is done for you. Everything GP1 actually grades
is not.

.. list-table::
   :widths: 34 20 46
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **State**
     - **What you do with it**
   * - ``ads_pipeline/carla_conversions.py``
     - Complete
     - Every CARLA measurement to its ROS 2 message, including the
       PointCloud2 packing, the RADAR MarkerArray and the static TF helper.
       Import it rather than rewriting it.
   * - ``ads_pipeline/sensor_manager.py``
     - Skeleton, 9 TODOs
     - **Task 2.** Spawning, YAML parameters, TF, clean shutdown. The RGB
       camera is wired as a worked example; the other six sensors follow the
       same shape.
   * - ``ads_pipeline/lidar_projection.py``
     - One function missing
     - **Task 5.** The intrinsics, the projection maths, the depth colouring
       and the overlay are all given. ``build_extrinsic()`` is yours, and it
       is about six lines.
   * - ``launch/sensors_launch.py``
     - Complete
     - Loads the YAML and starts the node. Copy its shape for Task 3.
   * - ``launch/record_launch.py``
     - Stub
     - **Task 3.** Record every topic to a bag.
   * - ``config/carla_config.yaml``
     - Placeholders
     - Replace with **your team's rig** from :ref:`gp1-team-config` before
       you run anything.
   * - ``rviz/ads_pipeline.rviz``
     - Displays laid out
     - **Task 4.** Connect the topics; the display types are already there.
   * - ``package.xml``, ``setup.py``
     - Dependencies declared
     - **Task 1.** Add your entry points and team details.

.. tip::

   ``lidar_projection.run_three_cases()`` produces all three overlays Task 5
   asks for and prints the point counts, as soon as ``build_extrinsic``
   works. It derives the two broken variants from your own transform, so the
   comparison is honest: same scene, one thing changed at a time.

.. note::

   **Nothing in the starter is a solution.** Every function that raises
   ``NotImplementedError`` is deliberate, and a submission that still raises
   one has not completed that task. Submitting the skeleton unchanged
   receives no credit.


.. _gp1-team-config:

Your Team's Sensor Configuration
--------------------------------

.. danger::

   **Every team has a different sensor rig.** Find your team letter below
   and use those values in ``carla_config.yaml``. They are not suggestions.

   The extrinsic transform in Task 5 is determined entirely by this
   geometry, so **each team's answer is a different matrix**, and the number
   of points landing on the image differs too. A transform computed for
   another team's rig produces a visibly and measurably wrong overlay on
   yours.

   Graders recompute the expected matrix from your assigned row. If your
   reported matrix does not match your row, the work is not yours, whatever
   the image looks like.

.. admonition:: What the "Spawn" column means, and which map to load
   :class: note

   CARLA ships every map with a fixed list of valid starting positions,
   already on the road and correctly oriented. ``get_spawn_points()``
   returns that list, and the number in the table is an index into it.
   **Spawn 58 means** ``get_spawn_points()[58]``.

   .. code-block:: python

      world = client.load_world('Town01')          # always, for GP1
      spawn = world.get_map().get_spawn_points()[58]
      vehicle = world.try_spawn_actor(blueprint, spawn)

   **All of GP1 uses Town01.** That matters, because the list is different
   on every map: Town01 has 255 spawn points, Town02 has 101, Town03 has
   265. The same index is a different street on a different map, so a spawn
   index means nothing until the map is pinned.

   Load the map explicitly rather than using whatever the server happens to
   have loaded. Another team's session, or your own earlier run, would
   otherwise decide where your vehicle starts.

.. GP1-TEAM-CONFIG-BEGIN (generated by tools/make_team_configs.py)

.. list-table::
   :widths: 8 26 8 22 20 16
   :header-rows: 1
   :class: compact-table

   * - **Team**
     - **Vehicle blueprint**
     - **Spawn**
     - **LiDAR (x, y, z) / channels**
     - **Camera (x, y, z) / pitch**
     - **Image / FOV**
   * - A
     - ``vehicle.toyota.prius``
     - 58
     - (0.34, 0.0, 2.78) / 64
     - (1.62, 0.26, 1.57) / -6.6 deg
     - 1280x720 / 110 deg
   * - B
     - ``vehicle.chevrolet.impala``
     - 9
     - (-0.22, 0.0, 2.72) / 32
     - (1.52, 0.13, 1.31) / -4.8 deg
     - 1600x900 / 110 deg
   * - C
     - ``vehicle.jeep.wrangler_rubicon``
     - 21
     - (-0.24, 0.0, 2.76) / 32
     - (1.36, -0.23, 1.82) / 0.8 deg
     - 1920x1080 / 90 deg
   * - D
     - ``vehicle.audi.a2``
     - 31
     - (-0.12, 0.0, 2.97) / 64
     - (1.68, -0.05, 1.84) / -6.9 deg
     - 1024x576 / 90 deg
   * - E
     - ``vehicle.bmw.grandtourer``
     - 41
     - (-0.15, 0.0, 2.56) / 32
     - (1.27, -0.01, 1.65) / -9.0 deg
     - 1280x720 / 100 deg
   * - F
     - ``vehicle.tesla.model3``
     - 9
     - (0.04, 0.0, 2.77) / 64
     - (1.45, -0.06, 1.6) / -4.5 deg
     - 1600x900 / 72 deg
   * - G
     - ``vehicle.nissan.patrol_2021``
     - 40
     - (0.06, 0.0, 2.65) / 64
     - (1.95, 0.02, 1.5) / -4.0 deg
     - 1920x1080 / 72 deg
   * - H
     - ``vehicle.nissan.micra``
     - 18
     - (0.32, 0.0, 2.99) / 32
     - (1.07, -0.11, 1.74) / -7.0 deg
     - 1024x576 / 90 deg
   * - I
     - ``vehicle.mercedes.coupe_2020``
     - 34
     - (-0.07, 0.0, 2.86) / 64
     - (2.07, 0.1, 1.4) / 3.2 deg
     - 1280x720 / 110 deg
   * - J
     - ``vehicle.mini.cooper_s``
     - 16
     - (-0.16, 0.0, 2.57) / 32
     - (1.81, -0.01, 1.36) / -11.8 deg
     - 1600x900 / 110 deg

.. GP1-TEAM-CONFIG-END

.. important::

   **The camera pitch is the part that matters.** Most teams have a camera
   that is not level with the vehicle, so relabelling the axes is no longer
   enough on its own. Your extrinsic has to compose the axis convention
   change **and** the mount rotation, in the right order. Getting the order
   backwards produces an overlay that looks almost right and is wrong by a
   few degrees, which is L2's one-degree error made visible.


Tasks
-----

.. dropdown:: Task 1 -- Package Setup (10 pts)
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** Create a properly structured ROS 2 Python package that builds
   cleanly with ``colcon build``.

   **Requirements:**

   - Package name: ``ads_pipeline``
   - ``package.xml`` must declare all dependencies:
     ``sensor_msgs``, ``nav_msgs``, ``cv_bridge``, ``std_msgs``,
     ``visualization_msgs``, and the ``carla`` Python client.
   - ``setup.py`` must include ``console_scripts`` entry points for every node
     your team creates.
   - A top-level launch file (``sensors_launch.py``) that starts all nodes
     and loads ``carla_config.yaml`` as parameters.
   - The package must install cleanly: ``colcon build --symlink-install``
     followed by ``source install/setup.bash`` must produce no errors.

   **Steps:**

   The starter already has this structure, so most of Task 1 is
   understanding it rather than typing it. Do not run ``ros2 pkg create``.

   1. Clone the starter as your team directory, as in
      :ref:`gp1-provided-resources`, and look at what is there. You should
      be able to say what each of ``package.xml``, ``setup.py``,
      ``resource/ads_pipeline`` and the ``share/`` entries in ``data_files``
      is for before you change anything.

   2. Fill in your team's details in both ``package.xml`` (the
      ``<maintainer>`` tag) and ``setup.py`` (``maintainer`` and
      ``maintainer_email``).

   3. Add a ``console_scripts`` entry point for every node your team
      creates. ``sensor_manager`` is already listed as the pattern:

      .. code-block:: python

         entry_points={
             'console_scripts': [
                 'sensor_manager = ads_pipeline.sensor_manager:main',
                 # one line per additional node
             ],
         }

      A node with no entry point cannot be launched by ``ros2 run`` or by a
      launch file, and this is the most common reason a grader cannot start
      your code.

   4. Note how the non-Python files reach the install space:

      .. code-block:: python

         data_files=[
             ('share/ament_index/resource_index/packages',
                 ['resource/' + package_name]),
             ('share/' + package_name, ['package.xml']),
             (os.path.join('share', package_name, 'config'),
                 glob('config/*.yaml')),
             (os.path.join('share', package_name, 'launch'),
                 glob('launch/*.py')),
             (os.path.join('share', package_name, 'rviz'),
                 glob('rviz/*.rviz')),
         ],

      Anything not listed here is not installed, so your launch file will
      not find it. If you add a new config or rviz file, it is covered by
      the existing globs; if you add a new *directory*, it is not.

   5. Replace the placeholder rig in ``config/carla_config.yaml`` with your
      team's row from :ref:`gp1-team-config`. Do this before you run
      anything, because every later task depends on it.

   6. Build and source:

      .. code-block:: bash

         cd ~/ros2_ws
         colcon build --symlink-install --packages-select ads_pipeline
         source install/setup.bash

   **Deliverables:** The complete package directory committed to your team's
   GitHub repository, buildable from a fresh clone.


.. dropdown:: Task 2 -- Sensor Spawning Node (30 pts)
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** Implement ``sensor_manager.py`` -- the node that connects to
   CARLA, spawns the ego vehicle, attaches all sensors, and publishes their
   data to ROS 2 topics.

   **Sensors to attach:**

   .. list-table::
      :widths: 35 35 30
      :header-rows: 1
      :class: compact-table

      * - Sensor
        - Blueprint ID
        - ROS 2 Topic
      * - RGB Camera (front)
        - ``sensor.camera.rgb``
        - ``/carla/camera/rgb/image``
      * - Depth Camera (front)
        - ``sensor.camera.depth``
        - ``/carla/camera/depth/image``
      * - Semantic Segmentation (front)
        - ``sensor.camera.semantic_segmentation``
        - ``/carla/camera/semseg/image``
      * - LiDAR (roof center)
        - ``sensor.lidar.ray_cast``
        - ``/carla/lidar/points``
      * - RADAR (front)
        - ``sensor.other.radar``
        - ``/carla/radar/tracks``
      * - GNSS
        - ``sensor.other.gnss``
        - ``/carla/gnss/fix``
      * - IMU
        - ``sensor.other.imu``
        - ``/carla/imu/data``

   **All sensor parameters** (resolution, FOV, channels, frequency, range)
   must be read from ``carla_config.yaml`` via ROS 2 parameters -- no
   hard-coded values. That includes the **mount transforms**: derive them
   from ``vehicle.bounding_box.extent`` rather than copying the numbers in
   the example below, because blueprints differ in size.

   .. danger::

      **Put the server in synchronous mode before you write any callback.**

      Left to itself the server ticks as fast as the hardware allows and
      hands you whatever happened to be ready. Sensor streams then arrive at
      irregular, unrepeatable times, two runs of the same script disagree,
      and Task 5 has no way to pair a camera frame with a LiDAR sweep from
      the same instant.

      .. code-block:: python

         settings = self.world.get_settings()
         settings.synchronous_mode = True
         settings.fixed_delta_seconds = 0.05      # 20 Hz
         self.world.apply_settings(settings)
         # then drive the clock yourself, once per loop:
         #     self.world.tick()

      Retrofitting this into a working asynchronous pipeline means
      re-checking every callback you have already written, which is why L2
      says to do it first. Remember to restore
      ``settings.synchronous_mode = False`` on shutdown, or the next person
      to connect inherits a server that will not advance on its own.

   **Node requirements:**

   - Declare a ROS 2 parameter ``vehicle_blueprint`` (default:
     ``vehicle.tesla.model3``) so graders can test different vehicles without
     editing source code.
   - Spawn the ego vehicle at CARLA's recommended spawn point (index 0) or a
     configurable spawn index parameter.
   - Register a ``destroy_callback`` that cleanly removes all actors when the
     node shuts down (``Ctrl+C``).
   - The node must handle CARLA connection failures gracefully with a
     meaningful error message.

   **Sensor spawning pattern** (adapt this for each sensor type):

   .. code-block:: python

      import carla
      import rclpy
      from rclpy.node import Node
      from sensor_msgs.msg import Image, PointCloud2, NavSatFix, Imu
      import numpy as np

      from ads_pipeline.carla_conversions import (
          carla_image_to_ros, carla_lidar_to_pointcloud2,
          carla_radar_to_markerarray, carla_gnss_to_navsatfix,
          carla_imu_to_imu, static_transforms_from_config,
      )


      class SensorManager(Node):
          def __init__(self):
              super().__init__('sensor_manager')

              # --- Parameters ---
              self.declare_parameter('host', 'localhost')
              self.declare_parameter('port', 2000)
              self.declare_parameter('vehicle_blueprint',
                                     'vehicle.tesla.model3')
              self.declare_parameter('spawn_index', 0)

              host = self.get_parameter('host').value
              port = self.get_parameter('port').value

              # --- CARLA connection ---
              self.client = carla.Client(host, port)
              self.client.set_timeout(10.0)
              self.world = self.client.get_world()
              self.blueprint_lib = self.world.get_blueprint_library()
              self.actors = []
              self.bridge = CvBridge()

              # --- Publishers ---
              self.rgb_pub = self.create_publisher(
                  Image, '/carla/camera/rgb/image', 10)
              self.lidar_pub = self.create_publisher(
                  PointCloud2, '/carla/lidar/points', 10)
              self.gnss_pub = self.create_publisher(
                  NavSatFix, '/carla/gnss/fix', 10)
              self.imu_pub = self.create_publisher(
                  Imu, '/carla/imu/data', 10)

              self._spawn_vehicle()
              self._attach_sensors()
              self.get_logger().info('SensorManager initialized.')

          def _spawn_vehicle(self):
              bp_name = self.get_parameter('vehicle_blueprint').value
              bp = self.blueprint_lib.find(bp_name)
              spawn_idx = self.get_parameter('spawn_index').value
              spawn_point = (self.world
                             .get_map()
                             .get_spawn_points()[spawn_idx])
              self.vehicle = self.world.spawn_actor(bp, spawn_point)
              self.actors.append(self.vehicle)
              self.get_logger().info(
                  f'Spawned {bp_name} at spawn point {spawn_idx}.')

          def _attach_sensors(self):
              """Attach all sensors relative to the vehicle transform."""
              self._attach_rgb_camera()
              self._attach_lidar()
              self._attach_gnss()
              self._attach_imu()
              # TODO: add depth, semseg, radar

          def _attach_rgb_camera(self):
              bp = self.blueprint_lib.find('sensor.camera.rgb')
              # Set attributes from ROS 2 parameters
              bp.set_attribute('image_size_x',
                  str(self.get_parameter('camera.width').value))
              bp.set_attribute('image_size_y',
                  str(self.get_parameter('camera.height').value))
              bp.set_attribute('fov',
                  str(self.get_parameter('camera.fov').value))
              transform = carla.Transform(
                  carla.Location(x=1.5, z=2.4))
              sensor = self.world.spawn_actor(
                  bp, transform, attach_to=self.vehicle)
              sensor.listen(self._rgb_callback)
              self.actors.append(sensor)

          def _rgb_callback(self, carla_image):
              # carla_conversions handles the buffer layout, the encoding
              # and the header, including taking the timestamp from the
              # measurement rather than from the clock.
              msg = carla_image_to_ros(
                  carla_image, 'camera_rgb_front', kind='rgb')
              self.rgb_pub.publish(msg)

          def destroy(self):
              self.get_logger().info('Destroying actors...')
              for actor in reversed(self.actors):
                  if actor.is_alive:
                      actor.destroy()


      def main(args=None):
          rclpy.init(args=args)
          node = SensorManager()
          try:
              rclpy.spin(node)
          except KeyboardInterrupt:
              pass
          finally:
              node.destroy()
              rclpy.shutdown()

   .. admonition:: What you should see
      :class: note

      With the camera and LiDAR publishing, the two streams look like this.
      Both were captured from a single CARLA tick, which is what synchronous
      mode buys you.

   .. figure:: /_static/images/GP1/gp1_rgb_camera.png
      :alt: A CARLA street scene from the ego vehicle's forward camera, showing a road, a kerb with planters, a lamp post, a wall on the left and a glass building on the right.
      :align: center
      :width: 92%

      The RGB camera, 1280x720 at 90 degrees FOV.

   .. figure:: /_static/images/GP1/gp1_lidar_topdown.png
      :alt: A top-down scatter plot of the same LiDAR sweep, coloured by height, showing the road surface, the kerb line and the building walls either side.
      :align: center
      :width: 78%

      The same sweep from above, coloured by height. The two walls and the
      kerb line are clearly separable, and the empty wedge behind the
      vehicle is the sensor's own blind spot.

   .. tip::

      Attach sensors in dependency order: vehicle first, then sensors that
      attach ``to=self.vehicle``. Use ``carla.Transform`` with appropriate
      ``carla.Location`` offsets so sensors do not overlap with the vehicle
      geometry.


.. dropdown:: Task 3 -- Data Recording & Playback (25 pts)
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** Record a minimum 2-minute drive in Town01 (autopilot mode) to a
   ``ros2 bag`` file, verify the recording, and demonstrate playback.

   **Requirements:**

   - Create ``record_launch.py`` that launches both ``sensor_manager`` and a
     ``ros2 bag record`` process for all sensor topics.
   - The recorded bag must contain **all seven sensor topics** listed in
     Task 2.
   - Record at least **2 minutes** of driving in Town01 with CARLA autopilot
     enabled.
   - Demonstrate playback: ``ros2 bag play`` must show data on all topics
     (verify with ``ros2 topic echo --once``).
   - Include a timestamp synchronization check: compute and report the maximum
     time offset between GNSS and IMU messages in the bag.

   **Enabling autopilot in your node** (add this after ``_attach_sensors``):

   .. code-block:: python

      # Enable CARLA autopilot so the vehicle drives itself during recording
      self.vehicle.set_autopilot(True)
      self.get_logger().info('Autopilot enabled.')

   **Recording launch file pattern:**

   .. code-block:: python

      # launch/record_launch.py
      import os
      from datetime import datetime
      from launch import LaunchDescription
      from launch.actions import ExecuteProcess, IncludeLaunchDescription
      from launch.launch_description_sources import (
          PythonLaunchDescriptionSource)
      from ament_index_python.packages import get_package_share_directory


      def generate_launch_description():
          pkg_share = get_package_share_directory('ads_pipeline')
          sensors_launch = IncludeLaunchDescription(
              PythonLaunchDescriptionSource(
                  os.path.join(pkg_share, 'launch', 'sensors_launch.py')))

          timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
          bag_path = os.path.join(
              os.path.expanduser('~'), 'gp1_data',
              f'sensor_bag_{timestamp}')

          bag_record = ExecuteProcess(
              cmd=[
                  'ros2', 'bag', 'record',
                  '/carla/camera/rgb/image',
                  '/carla/camera/depth/image',
                  '/carla/camera/semseg/image',
                  '/carla/lidar/points',
                  '/carla/radar/tracks',
                  '/carla/gnss/fix',
                  '/carla/imu/data',
                  '-o', bag_path,
              ],
              output='screen')

          return LaunchDescription([sensors_launch, bag_record])

   **Verifying the recording:**

   .. code-block:: bash

      # Check bag metadata
      ros2 bag info ~/gp1_data/sensor_bag_<timestamp>/

      # Verify each topic has messages
      ros2 bag play ~/gp1_data/sensor_bag_<timestamp>/ &
      ros2 topic echo --once /carla/gnss/fix
      ros2 topic echo --once /carla/lidar/points

   **Deliverable:** The bag file (or a public Google Drive / OneDrive link
   if >500 MB), the output of ``ros2 bag info``, and a short paragraph in
   ``report.pdf`` describing the timestamp synchronization check result.

   .. admonition:: What "timestamp analysis" means here, concretely
      :class: important

      Not an open-ended investigation. Produce one table,
      ``results/rates.md``, with a row per topic:

      .. list-table::
         :widths: 34 22 22 22
         :header-rows: 1
         :class: compact-table

         * - Topic
           - Configured rate
           - Measured rate
           - Mean gap between stamps
         * - ``/carla/camera/rgb/image``
           - 20 Hz
           - from ``ros2 topic hz``
           - from the bag

      Then two sentences: **which topics delivered slower than configured,
      and why.** Use the timestamps carried on the messages, which come from
      the sensor. If you stamped with the ROS clock instead, you measured
      when your callbacks ran, not when the data was captured, and the
      answer is meaningless.


.. dropdown:: Task 4 -- RViz2 Visualization (20 pts)
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** Configure RViz2 to display all sensor streams simultaneously
   and capture a screenshot proving they are working.

   **Required displays:**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Display Type
        - Topic
        - Notes
      * - Image
        - ``/carla/camera/rgb/image``
        - RGB camera feed
      * - Image
        - ``/carla/camera/depth/image``
        - Depth camera feed
      * - PointCloud2
        - ``/carla/lidar/points``
        - Color by intensity or height
      * - Odometry (Arrow)
        - ``/carla/gnss/fix`` (converted)
        - Vehicle position marker
      * - MarkerArray
        - ``/carla/radar/tracks``
        - RADAR return visualization

   **Steps:**

   1. Launch your nodes: ``ros2 launch ads_pipeline sensors_launch.py``
   2. Open RViz2 with the provided config:
      ``rviz2 -d $(ros2 pkg prefix ads_pipeline)/share/ads_pipeline/rviz/ads_pipeline.rviz``
   3. Set the **Fixed Frame** to ``ego_vehicle``.

      .. important::

         **RViz2 shows nothing until a TF tree exists.** It cannot place a
         point cloud and a camera image in the same scene until it knows
         where those sensors sit relative to one another. Without it you
         get "Fixed Frame [ego_vehicle] does not exist" and empty displays.

         Publish the tree once at startup, using the mount transforms
         already in your YAML:

         .. code-block:: python

            from tf2_ros import StaticTransformBroadcaster
            from ads_pipeline.carla_conversions import (
                static_transforms_from_config)

            self.tf_static = StaticTransformBroadcaster(self)
            mounts = self.get_parameter('mounts').value   # from YAML
            self.tf_static.sendTransform(
                static_transforms_from_config(mounts))

         Check it with ``ros2 run tf2_tools view_frames`` before you start
         debugging the displays themselves.
   4. Connect each display to its topic and adjust ``Queue Size`` to 5.
   5. For the LiDAR PointCloud2, set **Color Transformer** to ``AxisColor``
      (Z-axis) to visualize height clearly.
   6. Save the RViz2 config: ``File > Save Config``.

   **Deliverable:** ``results/rviz_screenshot.png`` showing all displays
   active simultaneously (no grey "No data" panels).

   .. tip::

      If RViz2 shows ``No transform from [camera_rgb_front] to [map]``,
      you need to publish a static TF. Add this to your launch file:

      .. code-block:: python

         from launch_ros.actions import Node as LaunchNode

         static_tf = LaunchNode(
             package='tf2_ros',
             executable='static_transform_publisher',
             arguments=['1.5', '0', '2.4', '0', '0', '0',
                        'base_link', 'camera_rgb_front'])


.. dropdown:: Task 5 -- LiDAR-to-Camera Projection (15 pts)
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** Project 3D LiDAR points onto the 2D RGB image plane using the
   known extrinsic calibration between the LiDAR and camera. Save the overlay
   as three overlays, one correct and two deliberately broken.

   **Background:**

   The projection from a 3D LiDAR point :math:`P = (X, Y, Z)` in the LiDAR
   frame to a pixel :math:`(u, v)` in the camera image uses the standard
   pinhole model combined with the rigid-body extrinsic transform
   :math:`T_{cam \leftarrow lidar}`:

   .. math::

      \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}
      = K \cdot T_{cam \leftarrow lidar} \cdot
      \begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix}

   where :math:`K` is the :math:`3 \times 3` camera intrinsic matrix.

   **What you actually write**

   The projection maths, the depth colouring and the overlay are given. Two
   things are not, and the second is the larger job.

   .. list-table::
      :widths: 30 18 52
      :header-rows: 1
      :class: compact-table

      * - **Piece**
        - **Rough size**
        - **What makes it work**
      * - ``build_extrinsic()``
        - About 8 lines
        - The axis relabelling, your rig's camera pitch, and the
          translation direction, composed in the right order. Short, and
          the entire concept.
      * - A driver script
        - 40 to 60 lines
        - Connect, spawn, capture **one camera frame and one LiDAR sweep
          from the same tick**, build :math:`K` from your own config, then
          call ``run_three_cases``.

   .. important::

      **Getting a matched pair is the part people underestimate.**

      ``run_three_cases(points_xyz, image_bgr, K, T_correct)`` needs a
      camera frame and a LiDAR sweep that describe the same instant. In
      synchronous mode each sensor produces exactly one measurement per
      tick, so the standard approach is a ``queue.Queue`` per sensor and one
      ``get()`` per ``world.tick()``. Free-running callbacks let a loaded
      machine hand you a frame from one tick and a sweep from another, and
      the overlay will then be wrong in a way that looks like a calibration
      error.

   .. danger::

      **Do not feed the ROS PointCloud2 into the projection.**

      ``l2_carla_demo.conversions.lidar_to_msg`` negates the y axis, because
      ROS is right-handed and CARLA is not:

      .. code-block:: python

         points[:, 1] *= -1.0      # CARLA y is right, ROS y is left

      That flip is correct for RViz2 and wrong for Task 5, because your
      extrinsic converts from the **raw CARLA sensor frame**. Take the
      points straight off the measurement:

      .. code-block:: python

         raw = np.frombuffer(sweep.raw_data, dtype=np.float32)
         points_xyz = raw.reshape(-1, 4)[:, :3].copy()   # no flip

      Apply the flip twice and your points land somewhere plausible and
      wrong, which is the failure this whole task is about.

   **Implementation:**

   .. code-block:: python

      # ads_pipeline/lidar_projection.py
      import numpy as np
      import cv2


      def build_intrinsic_matrix(image_w: int, image_h: int,
                                  fov_deg: float) -> np.ndarray:
          """Compute the 3x3 pinhole intrinsic matrix K from image dimensions
          and horizontal field of view."""
          focal_length = image_w / (2.0 * np.tan(np.radians(fov_deg) / 2.0))
          cx = image_w / 2.0
          cy = image_h / 2.0
          K = np.array([
              [focal_length, 0.0,          cx],
              [0.0,          focal_length, cy],
              [0.0,          0.0,          1.0],
          ], dtype=np.float64)
          return K


      def build_extrinsic(lidar_loc: tuple, camera_loc: tuple) -> np.ndarray:
          """Build the 4x4 transform T_cam_lidar, taking a point from the
          LiDAR frame into the camera's OPTICAL frame.

          YOU WRITE THIS FUNCTION. It is about six lines, and it is the
          only part of Task 5 that is not plumbing.

          Two things decide it, and both are covered in L2:

          1. ROTATION. K assumes the optical convention: x right, y down,
             z forward along the optical axis. CARLA uses x forward,
             y right, z up. Same three physical directions, different
             names, so the axes must be relabelled before K ever sees
             them. Derive the matrix from your own convention rather than
             copying one; the signs follow from which way each axis points.

          2. TRANSLATION. Both locations are given in CARLA vehicle
             coordinates. Work out where the LiDAR origin sits AS SEEN
             FROM the camera, then express that in the optical frame.
             Check the sign with one number you can do in your head: if
             the camera is 1.5 m ahead of the LiDAR, a point 10 m ahead of
             the LiDAR must come out at a depth of 8.5 m, not 11.5 m.

          Returns:
              (4, 4) float64 array.
          """
          raise NotImplementedError("Task 5: implement the extrinsic.")


      def project_lidar_to_image(
              points_xyz: np.ndarray,   # (N, 3) in LiDAR frame
              K: np.ndarray,            # (3, 3) intrinsic
              T_cam_lidar: np.ndarray,  # (4, 4) extrinsic
              image_w: int,
              image_h: int,
      ) -> tuple:
          """
          Returns:
              pixels  -- (M, 2) array of (u, v) coordinates
              depths  -- (M,)   array of depth values for coloring
          """
          N = points_xyz.shape[0]
          ones = np.ones((N, 1), dtype=np.float64)
          pts_hom = np.hstack([points_xyz, ones]).T  # (4, N)

          # Transform to camera coordinate frame
          pts_cam = T_cam_lidar @ pts_hom             # (4, N)

          # Keep only points in front of the camera (positive Z)
          in_front = pts_cam[2, :] > 0.1
          pts_cam = pts_cam[:, in_front]

          # Project to image plane
          pts_proj = K @ pts_cam[:3, :]               # (3, M)
          pts_proj /= pts_proj[2:3, :]                # normalize by Z

          u = pts_proj[0, :].astype(int)
          v = pts_proj[1, :].astype(int)
          depth = pts_cam[2, :]

          # Keep only pixels within image bounds
          valid = (u >= 0) & (u < image_w) & (v >= 0) & (v < image_h)
          return np.stack([u[valid], v[valid]], axis=1), depth[valid]


      def colorize_depth(depths: np.ndarray,
                          max_depth: float = 50.0) -> np.ndarray:
          """Map depth values to BGR colors using a jet colormap."""
          normalized = np.clip(depths / max_depth, 0.0, 1.0)
          normalized = (normalized * 255).astype(np.uint8)
          colored = cv2.applyColorMap(normalized, cv2.COLORMAP_JET)
          return colored.squeeze()  # (M, 3)


      def overlay_projection(image_bgr: np.ndarray,
                              pixels: np.ndarray,
                              colors: np.ndarray,
                              dot_size: int = 3) -> np.ndarray:
          """Draw colored LiDAR dots onto the image."""
          result = image_bgr.copy()
          for (u, v), color in zip(pixels, colors):
              cv2.circle(result, (u, v), dot_size,
                         color.tolist(), -1)
          return result

   **Usage in a ROS 2 node or standalone script:**

   .. code-block:: python

      # After receiving one synchronized camera + LiDAR message pair:

      K = build_intrinsic_matrix(image_w=1920, image_h=1080, fov_deg=90.0)
      T = build_extrinsic(lidar_loc=(0.0, 0.0, 2.8),      # <-- yours
                          camera_loc=(1.5, 0.0, 2.4))

      pixels, depths = project_lidar_to_image(
          points_xyz, K, T, image_w=1920, image_h=1080)
      colors = colorize_depth(depths, max_depth=50.0)
      overlay = overlay_projection(image_bgr, pixels, colors)

      cv2.imwrite('results/projection_correct.png', overlay)

   **Deliverables:**

   Run your projection three times and save all three overlays. This is the
   same experiment as L2 Exercise 5, so you have seen the failure modes
   before.

   .. list-table::
      :widths: 34 30 36
      :header-rows: 1
      :class: compact-table

      * - Run
        - File
        - What it should show
      * - Correct extrinsic
        - ``results/projection_correct.png``
        - Points land on the objects that produced them
      * - Rotation left as identity
        - ``results/projection_no_rotation.png``
        - Almost nothing survives the in-front test
      * - One sign of the rotation flipped
        - ``results/projection_wrong_sign.png``
        - Plenty of points, recognisable shape, wrong place

   Report, for each of the three runs, the **number of points that land on
   the image**. Also report your **4x4 extrinsic matrix**, printed to three
   decimal places, and the team letter it was built from. That matrix is
   what the grader recomputes from :ref:`gp1-team-config`.

   Then answer this in a short paragraph:

   .. admonition:: The question worth 5 of the 15 points
      :class: important

      Two of those runs are wrong. **Which failure would be more dangerous
      in a real vehicle, and why?** Answer in terms of what a downstream
      consumer of your data would see, not in terms of the picture.

   All three images must come from a real CARLA run, not mocked data.

   .. admonition:: What each of the three should look like
      :class: note

      These were produced by the reference solution on a single CARLA tick,
      so they are what a correct implementation gives you, not an artist's
      impression.

   .. figure:: /_static/images/GP1/gp1_projection_correct.png
      :alt: The camera image with LiDAR points overlaid and coloured by depth. Points follow the wall on the left, outline the lamp post, cover the building facade on the right, and carpet the road surface, grading from blue nearby to red far away.
      :align: center
      :width: 92%

      **Correct.** Points land on the things that produced them. The lamp
      post is outlined, the kerb and planters are picked out, and the depth
      colouring grades smoothly from blue nearby to red at range. This is
      what "geometrically correct" in the rubric means.

   .. figure:: /_static/images/GP1/gp1_projection_no_rotation.png
      :alt: The same camera image with no LiDAR points drawn on it at all.
      :align: center
      :width: 92%

      **Rotation left as identity.** Nothing at all. Every point fails the
      in-front test, because with the axes unrelabelled that test is
      applied to the vertical axis rather than the optical one.

   .. figure:: /_static/images/GP1/gp1_projection_wrong_sign.png
      :alt: The same camera image with LiDAR points overlaid, but the scene is inverted: the road surface is painted across the sky and the building points sit below the horizon.
      :align: center
      :width: 92%

      **One sign flipped.** This is the one worth studying. It has
      essentially the same number of points as the correct version, 6354
      against 6343, the shape is recognisable, and at a glance it looks like
      a working result. The road is painted across the sky.

   .. danger::

      **Compare the point counts in those three captions.**

      The blank image announces itself. The inverted one does not: same
      count, plausible structure, wrong answer. If you were checking
      "did my projection produce output" rather than "did it produce the
      right output", you would ship it.

      That is the whole reason the deliverable asks which failure is more
      dangerous.

   .. tip::

      Sanity checks before you go hunting for bugs.

      - A point 10 m in front of the LiDAR should come out at a depth of
        8.5 m when the camera is mounted 1.5 m further forward. If you get
        11.5 m, your translation sign is backwards.
      - With a roof LiDAR and a forward camera, expect very roughly a fifth
        to a quarter of the sweep to land on the image. If you get zero,
        the rotation is wrong rather than the translation.
      - Project a point and then project it back. The round trip should
        return the number you started with.


Suggested Schedule
------------------

This plan finishes on **day 18 of 21**, leaving three days of slack. The
slack is the point: it absorbs a CARLA reinstall, a teammate falling ill, or
one stubborn bug, without anyone working the night before the deadline.

.. list-table::
   :widths: 12 30 34 24
   :header-rows: 1
   :class: compact-table

   * - Days
     - Milestone
     - Done when
     - Rough effort
   * - 1--3
     - Task 1, and synchronous mode running
     - ``colcon build`` clean, node connects, server ticks under your
       control
     - 3 h
   * - 4--9
     - Task 2, all seven sensors
     - Every topic appears in ``ros2 topic list`` and carries sensor
       timestamps
     - 14 h
   * - 10--12
     - Tasks 3 and 4
     - Bag replays, RViz2 shows all displays, ``rates.md`` written
     - 8 h
   * - 13--16
     - Task 5
     - Three overlays saved with point counts, paragraph drafted
     - 6 h
   * - 17--18
     - Report, screenshots, submission
     - Checklist below fully ticked
     - 4 h
   * - 19--21
     - **Slack**
     - Nothing scheduled
     - 0 h

That is roughly **43 person-hours**, or about 11 hours each across three
weeks for a team of four.

.. tip::

   **Split the work by sensor, not by task.** Tasks 2 to 4 all touch the
   same node, so four people editing it in sequence will spend more time
   merging than coding. One person per sensor group, working in parallel
   behind the conversion helpers, avoids that.

.. admonition:: If you run short of time
   :class: warning

   Submit something that runs rather than something that is complete. A
   pipeline with **RGB camera, LiDAR, GNSS and IMU** publishing, recorded to
   a bag, visible in RViz2, plus the correct Task 5 overlay, earns most of
   the marks. Depth, semantic segmentation and RADAR are worth 15 points
   between them.

   A submission that does not build earns almost nothing regardless of how
   much code is in it, so **freeze and verify a working state on day 16**
   even if features are missing.


Folder Structure
----------------

Submit your repository with the following exact layout. Graders will check
the structure automatically before running your code.

.. code-block:: text

   GP1_Team{X}/
   ├── ads_pipeline/                  # ROS 2 package root
   │   ├── ads_pipeline/              # Python module (same name as package)
   │   │   ├── __init__.py
   │   │   ├── sensor_manager.py      # Task 2 (required)
   │   │   └── lidar_projection.py    # Task 5 (required)
   │   ├── config/
   │   │   └── carla_config.yaml      # Provided + your modifications
   │   ├── launch/
   │   │   ├── sensors_launch.py      # Task 1 (required)
   │   │   └── record_launch.py       # Task 3 (required)
   │   ├── rviz/
   │   │   └── ads_pipeline.rviz      # Task 4 (required)
   │   ├── resource/
   │   │   └── ads_pipeline
   │   ├── package.xml
   │   └── setup.py
   ├── data/
   │   └── rosbag/                    # Bag file or download link in README
   │       └── sensor_bag_<timestamp>/
   ├── results/
   │   ├── projection_correct.png     # Task 5 (required)
   │   ├── projection_no_rotation.png  # Task 5 (required)
   │   ├── projection_wrong_sign.png   # Task 5 (required)
   │   └── rviz_screenshot.png        # Task 4 (required)
   └── report.pdf


.. important::

   **Submission Instructions**

   1. Push your complete ``GP1_Team{X}/`` directory to your team's GitHub
      repository under the ``gp1`` branch.
   2. Submit the GitHub repository link AND a ``report.pdf`` on Canvas by
      the deadline.
   3. ``report.pdf`` must include: team member names and contributions,
      a description of any deviations from the required folder structure,
      the timestamp synchronization analysis (Task 3), and the RViz2
      screenshot (Task 4) embedded in the document.
   4. Tag your submission commit: ``git tag gp1-final && git push --tags``


Submission Checklist
--------------------

.. admonition:: Before Submitting -- Check Every Item
   :class: tip

   **Package & Build**

   - [ ] ``colcon build --packages-select ads_pipeline`` succeeds with no
         errors or warnings.
   - [ ] ``ros2 launch ads_pipeline sensors_launch.py`` starts all nodes
         without crashing.
   - [ ] ``carla_config.yaml`` is loaded correctly (verify with
         ``ros2 param list /sensor_manager``).

   **Sensor Spawning (Task 2)**

   - [ ] All 7 sensors appear in CARLA (verify with
         ``client.get_world().get_actors()``).
   - [ ] All 7 ROS 2 topics publish data (``ros2 topic hz``).
   - [ ] Vehicle blueprint is configurable via ROS 2 parameter.

   **Data Recording (Task 3)**

   - [ ] Bag contains all 7 topics (``ros2 bag info``).
   - [ ] Bag duration is >= 2 minutes.
   - [ ] Playback verified (``ros2 bag play`` + ``ros2 topic echo``).
   - [ ] Timestamp synchronization analysis included in report.

   **Visualization (Task 4)**

   - [ ] RViz2 config saved to ``rviz/ads_pipeline.rviz``.
   - [ ] ``results/rviz_screenshot.png`` shows all displays with live data.

   **LiDAR Projection (Task 5)**

   - [ ] All three Task 5 overlays saved, with the point count for each.
   - [ ] Paragraph answering which failure is more dangerous.
   - [ ] Points are colored by depth (not a single flat color).
   - [ ] Only forward-facing points appear (no points behind the camera).

   **Repository**

   - [ ] Folder structure matches the required layout exactly.
   - [ ] ``report.pdf`` submitted on Canvas.
   - [ ] Commit tagged ``gp1-final`` and pushed.
   - [ ] Peer evaluation submitted on Canvas (individual grade component).


Grading Rubric
--------------

Total: **100 points** (scaled to 15% of final project grade).

.. list-table::
   :widths: 40 15 45
   :header-rows: 1
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - Package structure & launch files
     - 10
     - Correct ``package.xml``, ``setup.py``, ``colcon build`` succeeds,
       launch file loads YAML parameters. **-5** if build fails.
   * - Sensor spawning
     - 30
     - All 7 sensors attached and publishing on correct topics. All
       parameters configurable via YAML. **-5 per missing sensor.**
       **-10** if blueprint not configurable.
   * - Data recording & playback
     - 25
     - Bag contains all 7 topics, duration >= 2 min, playback demonstrated,
       timestamp analysis present. **-10** if bag is missing or < 1 min.
   * - RViz2 visualization
     - 20
     - Screenshot shows all 4 displays active simultaneously. Config saved
       to ``rviz/ads_pipeline.rviz``. **-5 per missing display.**
   * - LiDAR-camera projection
     - 15
     - **5** correct overlay, points on the objects that produced them,
       depth-coloured. **5** both failure cases produced, with point counts.
       **5** the paragraph on which failure is more dangerous. **-3** if
       depth colouring is missing.

.. note::

   **Individual grade** = 60% project grade + 40% peer review score.
   Submit peer evaluations on Canvas within 48 hours of the project deadline.


Common Mistakes
---------------

.. danger::

   **These mistakes are seen every semester. Avoid them.**

   - **Hard-coding sensor parameters.** If your node contains lines like
     ``bp.set_attribute('image_size_x', '1920')`` with no YAML lookup,
     you will lose points on Task 2. Every parameter must come from
     ``carla_config.yaml`` via ``self.get_parameter(...)``.

   - **Not destroying actors on shutdown.** CARLA will accumulate ghost
     actors across runs if your node does not call ``actor.destroy()`` in a
     cleanup handler. Always register a ``destroy_callback`` and test it
     by pressing ``Ctrl+C``.

   - **Committing the bag file to Git.** Bag files can be gigabytes. Use
     ``.gitignore`` to exclude the ``data/rosbag/`` directory and provide a
     cloud download link instead.

   - **Wrong coordinate frame in projection.** CARLA uses a left-handed
     system. Forgetting to convert coordinates before the projection will
     produce a mirrored or completely wrong overlay. Test with a single known
     point first.

   - **RViz2 TF errors.** If you skip publishing static TF transforms between
     ``base_link`` and each sensor frame, RViz2 will display nothing. Check
     ``ros2 run tf2_tools view_frames`` to diagnose transform tree issues.

   - **Not tagging the submission commit.** Graders check out the
     ``gp1-final`` tag. If it is missing, the most recent commit on the
     ``gp1`` branch is graded -- which may not be your intended submission.


Tips for Success
----------------

.. tip::

   **Start early -- CARLA setup takes time.**
   Allocate the first two days of Week 3 entirely to verifying that CARLA
   starts, your team's machines can connect, and a basic Python client script
   can spawn a vehicle. All subsequent tasks depend on this working.

.. tip::

   **Develop and test one sensor at a time.**
   Get the RGB camera publishing and visible in RViz2 before adding LiDAR.
   Add LiDAR and verify. Add GNSS and verify. Debugging seven sensors at once
   is significantly harder than debugging one at a time.

.. tip::

   **Use ``ros2 topic hz`` and ``ros2 topic echo`` constantly.**
   These two commands are your best debugging tools. If a topic shows 0 Hz,
   the sensor callback is not firing -- check whether the CARLA actor was
   actually spawned and whether ``actor.listen(callback)`` was called.

.. tip::

   **Commit frequently to GitHub.**
   Use feature branches (``git checkout -b task2-sensors``) and open pull
   requests for each task. This protects against data loss and gives you a
   clear history for the peer evaluation.

.. tip::

   **Reuse the provided RViz2 config.**
   The provided ``ads_pipeline.rviz`` already has the correct display types
   added. You only need to set the topic names. Rebuilding from scratch wastes
   time and often results in missing displays.
