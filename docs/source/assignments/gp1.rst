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
        - 3 weeks (Week 2 -- Week 5)
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

GP1 establishes the **foundation of your team's ADS pipeline**. You will create
the ``ads_pipeline`` ROS 2 package that all subsequent group projects (GP2
through GP4) will extend and build upon. A well-structured, maintainable package
here pays dividends for the entire semester.

By the end of GP1, your team will have:

- A properly structured ROS 2 Python package connected to CARLA.
- An ego vehicle spawned with a **full sensor suite** (camera, LiDAR, RADAR,
  GNSS, IMU) and all parameters configurable via YAML.
- Sensor data recorded to a ``ros2 bag`` file and verified through playback.
- An RViz2 visualization showing all sensor streams simultaneously.
- A working **LiDAR-to-camera projection** demonstrating cross-sensor
  calibration.

.. important::

   This package is the ``ads_pipeline`` skeleton. Every file you create here
   will be inherited by GP2, GP3, and GP4. Follow the provided folder structure
   exactly -- future GPs assume it.


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
- Apply extrinsic calibration to project LiDAR points onto a camera image.


Provided Resources
------------------

The following files are distributed on Canvas and the course GitHub. Download
them **before** starting each task:

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - File
     - Description
   * - ``package.xml`` (template)
     - Pre-filled with required dependencies; add your node entry points.
   * - ``setup.py`` (template)
     - Entry points section for you to fill in for each node.
   * - ``carla_config.yaml``
     - Default sensor parameters (resolution, FOV, channels, range). Edit to
       experiment with configurations.
   * - ``sensors_launch.py``
     - Example launch file demonstrating how to pass YAML parameters to a node.
   * - ``ads_pipeline.rviz``
     - Pre-configured RViz2 layout with display types already added; you only
       need to connect the correct topic names.

.. note::

   Provided scripts are starting points. You are expected to extend them
   significantly. Simply submitting unmodified templates receives no credit.


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

   1. Create the package scaffold:

      .. code-block:: bash

         cd ~/ros2_ws/src
         ros2 pkg create --build-type ament_python ads_pipeline \
             --dependencies rclpy sensor_msgs nav_msgs cv_bridge std_msgs

   2. Replace the generated ``package.xml`` and ``setup.py`` with the provided
      templates, then fill in your team's details and entry points.
   3. Create the ``config/``, ``launch/``, and ``rviz/`` directories inside
      the package.
   4. Copy ``carla_config.yaml`` and ``ads_pipeline.rviz`` into their
      respective directories.
   5. Declare the data directories in ``setup.py`` so they are installed:

      .. code-block:: python

         data_files=[
             ('share/ament_index/resource_index/packages',
                 ['resource/' + package_name]),
             ('share/' + package_name, ['package.xml']),
             ('share/' + package_name + '/launch',
                 glob('launch/*.py')),
             ('share/' + package_name + '/config',
                 glob('config/*.yaml')),
             ('share/' + package_name + '/rviz',
                 glob('rviz/*.rviz')),
         ],

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
   hard-coded values.

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
      from cv_bridge import CvBridge
      import numpy as np


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
              array = np.frombuffer(
                  carla_image.raw_data, dtype=np.uint8)
              array = array.reshape(
                  (carla_image.height, carla_image.width, 4))
              array = array[:, :, :3]          # Drop alpha
              msg = self.bridge.cv2_to_imgmsg(array, 'rgb8')
              msg.header.stamp = self.get_clock().now().to_msg()
              msg.header.frame_id = 'camera_rgb_front'
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
   3. Set the **Fixed Frame** to ``map`` or the frame published by your GNSS
      node.
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
   as ``projection_result.png``.

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
          """Build the 4x4 extrinsic transform from LiDAR to camera frame.
          Both locations are (x, y, z) in CARLA vehicle coordinates."""
          # Translation vector: camera position minus LiDAR position
          tx = camera_loc[0] - lidar_loc[0]
          ty = camera_loc[1] - lidar_loc[1]
          tz = camera_loc[2] - lidar_loc[2]

          # For co-planar sensors with no rotation difference, R = I
          # Replace with actual rotation if sensors are angled differently
          R = np.eye(3, dtype=np.float64)
          t = np.array([[tx], [ty], [tz]], dtype=np.float64)

          T = np.hstack([R, t])            # 3x4
          T = np.vstack([T, [0, 0, 0, 1]]) # 4x4
          return T


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
      T = build_extrinsic(lidar_loc=(0.0, 0.0, 2.8),
                           camera_loc=(1.5, 0.0, 2.4))

      pixels, depths = project_lidar_to_image(
          points_xyz, K, T, image_w=1920, image_h=1080)
      colors = colorize_depth(depths, max_depth=50.0)
      overlay = overlay_projection(image_bgr, pixels, colors)

      cv2.imwrite('results/projection_result.png', overlay)

   **Deliverable:** ``results/projection_result.png`` -- a side-by-side or
   overlaid image showing LiDAR points projected onto the RGB frame, colored
   by depth. The image must be captured from a real CARLA run (not mocked
   data).

   .. tip::

      CARLA uses a **left-handed coordinate system** (Y points right, Z up)
      while OpenCV / ROS 2 conventions differ. If your projected points are
      mirrored or rotated, apply a coordinate frame conversion before the
      projection step:

      .. code-block:: python

         # CARLA LiDAR -> ROS 2 / OpenCV convention
         pts_ros = points_xyz[:, [1, 2, 0]]  # (y, z, x) -> (x, y, z)
         pts_ros[:, 1] *= -1                 # flip y for right-hand rule


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
   │   ├── projection_result.png      # Task 5 (required)
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

   - [ ] ``results/projection_result.png`` saved and visible.
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
     - Projection geometrically correct, points depth-colored, saved as
       ``projection_result.png``. **-7** if points are in wrong location
       (calibration error). **-5** if no depth coloring.

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
   Allocate the first two days of Week 2 entirely to verifying that CARLA
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
