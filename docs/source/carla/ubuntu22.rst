==================================================================
CARLA Setup Guide - Ubuntu 22.04 (Native)
==================================================================

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Component**
     - **Version/Details**
   * - Course
     - ENPM818Z -- On-Road Automated Vehicles
   * - Ubuntu Version
     - 22.04 (Jammy Jellyfish)
   * - CARLA Version
     - 0.9.16
   * - Installation Method
     - Native (No Docker)

---------------------------------------------------------
Overview
---------------------------------------------------------

This guide walks you through setting up CARLA 0.9.16 on Ubuntu 22.04 using a **native installation** (no Docker required). You will use a **custom ROS 2 bridge package** that bypasses CARLA's native ROS 2 implementation due to a known bug (see :ref:`known-issue-ubuntu22`).

**What You'll Install:**

- CARLA 0.9.16 standalone application
- CARLA Python API
- Custom ROS 2 bridge package

.. note::
   **Why Native?** Native CARLA installation is simpler than Docker, requires no special configuration, and provides direct access to the Python API. Perfect for development and learning!

---------------------------------------------------------
Prerequisites
---------------------------------------------------------

System Requirements
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Component**
     - **Requirement**
   * - Operating System
     - Ubuntu 22.04 (Jammy Jellyfish)
   * - ROS 2 Distribution
     - Already installed
   * - GPU
     - NVIDIA GPU (recommended), AMD/Intel also work
   * - RAM
     - Minimum 8 GB, Recommended 16 GB
   * - Disk Space
     - ~10 GB for CARLA and dependencies
   * - Python
     - 3.10 (comes with Ubuntu 22.04)

Verify Your Ubuntu Version
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   lsb_release -a

You should see ``Ubuntu 22.04`` in the output.

---------------------------------------------------------
Step 1: Download and Install CARLA 0.9.16
---------------------------------------------------------

Download CARLA
~~~~~~~~~~~~~~

.. code-block:: bash

   # Create directory for CARLA
   mkdir -p ~/carla
   cd ~/carla

   # Download CARLA 0.9.16 (this will take 5-10 minutes)
   wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/CARLA_0.9.16.tar.gz

   # Extract (this will take a few minutes)
   tar -xzf CARLA_0.9.16.tar.gz

   # Verify extraction
   ls -lh CARLA_0.9.16/

You should see directories like ``CarlaUE4/``, ``PythonAPI/``, etc.

Make CARLA Executable
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd CARLA_0.9.16
   chmod +x CarlaUE4.sh

Test CARLA
~~~~~~~~~~

.. code-block:: bash

   # Run CARLA (will take 30-60 seconds to start)
   ./CarlaUE4.sh -quality-level=Low

You should see the CARLA window open with a 3D city environment. Press ``Ctrl+C`` in the terminal to stop CARLA.

.. tip::
   **First Launch:** CARLA's first launch may take longer as it compiles shaders. Subsequent launches will be faster.

---------------------------------------------------------
Step 2: Install CARLA Python API
---------------------------------------------------------

The Python API is already included with CARLA, but we need to install it:

.. code-block:: bash

   # Navigate to Python API directory
   cd ~/carla/CARLA_0.9.16/PythonAPI/carla/dist

   # Find the .whl file for Python 3.10
   ls carla-0.9.16-cp310-cp310-linux_x86_64.whl

   # Install the wheel file
   pip3 install carla-0.9.16-cp310-cp310-linux_x86_64.whl

   # Verify installation
   python3 -c "import carla; print(f'CARLA Python API: {carla.__version__}')"

Expected output: ``CARLA Python API: 0.9.16``

---------------------------------------------------------
Step 3: Install Additional Dependencies
---------------------------------------------------------

.. code-block:: bash

   # Install required Python packages
   pip3 install numpy pygame

   # Verify installations
   python3 -c "import numpy; import pygame; print('Dependencies OK')"

---------------------------------------------------------
Step 4: Clone and Build the ROS 2 Bridge Package
---------------------------------------------------------

Clone the Repository
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create workspace
   mkdir -p ~/carla_ws/src
   cd ~/carla_ws/src

   # Clone the repository
   git clone -b ubuntu22 https://github.com/zeidk/enpm818z-fall-2026-carla.git carla_ros2_bridge

   # Return to workspace root
   cd ~/carla_ws

Build the Package
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Source ROS 2
   source /opt/ros/humble/setup.bash

   # Install dependencies
   rosdep update
   rosdep install --from-paths src --ignore-src -r -y

   # Build
   colcon build --symlink-install

   # Source the workspace
   source install/setup.bash

Verify the build:

.. code-block:: bash

   # Check if package is available
   ros2 pkg list | grep carla_ros2_bridge

   # Check executables
   ros2 pkg executables carla_ros2_bridge

Expected output:

.. code-block:: text

   carla_ros2_bridge carla_bridge
   carla_ros2_bridge carla_camera_publisher
   carla_ros2_bridge carla_image_subscriber

---------------------------------------------------------
Step 5: Setup Environment Configuration
---------------------------------------------------------

Create Setup Script
~~~~~~~~~~~~~~~~~~~

Add the following function to your ``~/.bashrc``:

.. code-block:: bash

   # Open bashrc
   nano ~/.bashrc

   # Add this function at the end:
   carla_setup() {
       # Configuration
       CARLA_WS="/home/$USER/carla_ws"
       CARLA_ROOT="/home/$USER/carla/CARLA_0.9.16"

       echo "Setting up CARLA ROS 2 environment..."

       # Setup environment variables
       export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
       export ROS_DOMAIN_ID=0
       unset ROS_LOCALHOST_ONLY
       unset FASTRTPS_DEFAULT_PROFILES_FILE

       # Source ROS 2
       if [ -f "/opt/ros/humble/setup.bash" ]; then
           source /opt/ros/humble/setup.bash
       else
           echo "Error: ROS 2 not found at /opt/ros/humble"
           return 1
       fi

       # Source CARLA workspace
       if [ -d "$CARLA_WS" ]; then
           if [ -f "$CARLA_WS/install/setup.bash" ]; then
               source "$CARLA_WS/install/setup.bash"
               echo "Sourced CARLA workspace"
           else
               echo "Warning: CARLA workspace not built"
               echo "   Run: cd $CARLA_WS && colcon build"
           fi
       fi

       # Reset ROS 2 daemon
       echo "Restarting ROS 2 daemon..."
       ros2 daemon stop > /dev/null 2>&1
       sleep 1
       ros2 daemon start > /dev/null 2>&1

       # Create CARLA alias
       alias carla="cd $CARLA_ROOT && ./CarlaUE4.sh -quality-level=Low -nosound -vulkan"

       echo "CARLA Setup Complete!"
       echo ""
       echo "Usage:"
       echo "   1. Start CARLA:  carla"
       echo "   2. Run ROS 2 bridge:"
       echo "      ros2 run carla_ros2_bridge carla_camera_publisher"
       echo ""
       echo "Environment:"
       echo "   ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
       echo "   RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"
       echo "   CARLA_ROOT=$CARLA_ROOT"

       cd "$CARLA_WS"
   }

   # Auto-run setup when starting new terminal
   carla_setup

Save and reload:

.. code-block:: bash

   source ~/.bashrc

.. _known-issue-ubuntu22:

---------------------------------------------------------
Understanding the CARLA 0.9.16 ROS 2 Bug
---------------------------------------------------------

Issue Description
~~~~~~~~~~~~~~~~~

CARLA 0.9.16 introduced **native ROS 2 support** via the ``--ros2`` flag and ``enable_for_ros()`` API. However, there is a **critical bug** in the topic name generation.

**The Bug:**

CARLA creates topic names with double slashes: ``/carla//camera/image``

**Why This Matters:**

ROS 2 strictly validates topic names and rejects topics with consecutive slashes as invalid. This means:

- ``ros2 topic echo`` does not work
- ``ros2 topic hz`` does not work
- ``rviz2`` cannot subscribe to topics
- Custom nodes fail to receive data

**Example:**

.. code-block:: bash

   # CARLA publishes (broken):
   /carla//front_camera/image  # Double slash

   # ROS 2 rejects this with:
   Invalid topic name: topic name must not contain repeated '/'

Our Solution
~~~~~~~~~~~~

The **custom ROS 2 bridge package** you installed:

1. **Bypasses CARLA's native ROS 2** -- does not use ``enable_for_ros()``
2. **Uses the Python API directly** -- gets data via ``camera.listen()`` callbacks
3. **Publishes to clean topics** -- ``/carla/camera/image`` (no double slash)
4. **Works with all ROS 2 tools** -- full compatibility

This is why we do not use the ``--ros2`` flag with CARLA.

GitHub Issue Reference
~~~~~~~~~~~~~~~~~~~~~~

This is a known issue tracked here: https://github.com/carla-simulator/carla/issues/9278

Expected to be fixed in future CARLA releases, but for now our bridge is the correct solution.

---------------------------------------------------------
Running CARLA with ROS 2
---------------------------------------------------------

Basic Workflow
~~~~~~~~~~~~~~

**Terminal 1: Start CARLA Server**

.. code-block:: bash

   carla

Wait for the CARLA window to open and the world to load (~30 seconds).

**Terminal 2: Run ROS 2 Bridge**

.. code-block:: bash

   source ~/.bashrc
   ros2 run carla_ros2_bridge carla_camera_publisher

You should see:

.. code-block:: text

   ============================================================
   CARLA Camera Publisher Node
   ============================================================
   Connecting to CARLA at localhost:2000...
   Connected to CARLA 0.9.16
   Spawned vehicle at Location(x=..., y=..., z=...)
   Autopilot enabled
   Camera spawned and attached
   Camera listening
   ============================================================
   Publishing to:
     /carla/camera/image
     /carla/camera/camera_info
     /carla/vehicle/odometry
   ============================================================

**Terminal 3: Verify Topics**

.. code-block:: bash

   # List topics
   ros2 topic list | grep carla

   # Check image topic rate
   ros2 topic hz /carla/camera/image

   # Echo camera info
   ros2 topic echo /carla/camera/camera_info --once

**Terminal 4: Run Test Subscriber**

.. code-block:: bash

   ros2 run carla_ros2_bridge carla_image_subscriber

You should see:

.. code-block:: text

   [INFO] [carla_image_subscriber]: Received first image!
   [INFO] [carla_image_subscriber]:   Size: 800x600
   [INFO] [carla_image_subscriber]:   Encoding: rgb8
   [INFO] [carla_image_subscriber]: Frame 30: ~20.0 Hz

---------------------------------------------------------
Package Overview
---------------------------------------------------------

The ``carla_ros2_bridge`` package contains the following nodes:

carla_camera_publisher
~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Main bridge node that connects to CARLA, spawns a vehicle with camera, and publishes sensor data.

**Subscriptions:** None

**Publications:**

.. list-table::
   :widths: 35 25 40
   :header-rows: 1
   :class: compact-table

   * - **Topic**
     - **Type**
     - **Description**
   * - ``/carla/camera/image``
     - sensor_msgs/Image
     - RGB camera images at ~20 Hz
   * - ``/carla/camera/camera_info``
     - sensor_msgs/CameraInfo
     - Camera calibration parameters
   * - ``/carla/vehicle/odometry``
     - nav_msgs/Odometry
     - Vehicle pose and velocity at 20 Hz

**Parameters:**

.. list-table::
   :widths: 25 15 15 45
   :header-rows: 1
   :class: compact-table

   * - **Parameter**
     - **Type**
     - **Default**
     - **Description**
   * - ``carla_host``
     - string
     - localhost
     - CARLA server hostname
   * - ``carla_port``
     - int
     - 2000
     - CARLA server port
   * - ``image_width``
     - int
     - 800
     - Camera image width (pixels)
   * - ``image_height``
     - int
     - 600
     - Camera image height (pixels)
   * - ``camera_fov``
     - float
     - 110.0
     - Camera field of view (degrees)
   * - ``camera_x``
     - float
     - 1.6
     - Camera X position relative to vehicle (forward)
   * - ``camera_z``
     - float
     - 1.2
     - Camera Z position relative to vehicle (up)
   * - ``spawn_vehicle``
     - bool
     - true
     - Automatically spawn vehicle
   * - ``autopilot``
     - bool
     - true
     - Enable autopilot

**Example with custom parameters:**

.. code-block:: bash

   ros2 run carla_ros2_bridge carla_camera_publisher \
       --ros-args \
       -p image_width:=1280 \
       -p image_height:=720 \
       -p camera_fov:=90.0 \
       -p autopilot:=false

carla_image_subscriber
~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Example subscriber node for testing. Displays image statistics.

**Subscriptions:**

.. list-table::
   :widths: 35 25 40
   :header-rows: 1
   :class: compact-table

   * - **Topic**
     - **Type**
     - **Description**
   * - ``/carla/camera/image``
     - sensor_msgs/Image
     - Camera images

**Publications:** None

**Parameters:**

.. list-table::
   :widths: 25 15 15 45
   :header-rows: 1
   :class: compact-table

   * - **Parameter**
     - **Type**
     - **Default**
     - **Description**
   * - ``topic``
     - string
     - /carla/camera/image
     - Topic to subscribe to

---------------------------------------------------------
Advanced Usage
---------------------------------------------------------

Visualizing in RViz2
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   rviz2

In RViz2: click **Add** then **By topic**, select ``/carla/camera/image`` and choose **Image**, then set Fixed Frame to ``camera_link``.

Recording Data
~~~~~~~~~~~~~~

.. code-block:: bash

   # Record camera and odometry
   ros2 bag record /carla/camera/image /carla/vehicle/odometry

   # Record all CARLA topics
   ros2 bag record -r "/carla/.*"

   # Play back recorded data
   ros2 bag play <bag_file>

Custom Resolution
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # High resolution
   ros2 run carla_ros2_bridge carla_camera_publisher \
       --ros-args \
       -p image_width:=1920 \
       -p image_height:=1080

   # Lower resolution for better performance
   ros2 run carla_ros2_bridge carla_camera_publisher \
       --ros-args \
       -p image_width:=640 \
       -p image_height:=480

---------------------------------------------------------
Troubleshooting
---------------------------------------------------------

CARLA Won't Start
~~~~~~~~~~~~~~~~~

**Symptom:** Black screen or crash on launch

**Solutions:**

1. Check graphics drivers:

   .. code-block:: bash

      nvidia-smi

2. Try OpenGL instead of Vulkan:

   .. code-block:: bash

      cd ~/carla/CARLA_0.9.16
      ./CarlaUE4.sh -opengl -quality-level=Low

3. Check system requirements are met (8 GB RAM minimum)

Cannot Connect to CARLA
~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** ``Failed to connect to CARLA: timeout``

**Solutions:**

1. Wait for CARLA to fully load (30-60 seconds after window appears)

2. Check CARLA is running:

   .. code-block:: bash

      ps aux | grep CarlaUE4
      netstat -tuln | grep 2000

3. Verify Python API:

   .. code-block:: bash

      python3 -c "import carla; c = carla.Client('localhost', 2000); c.set_timeout(5.0); print(c.get_server_version())"

No Topics Visible
~~~~~~~~~~~~~~~~~

**Symptom:** ``ros2 topic list`` does not show ``/carla/camera/image``

**Solutions:**

1. Verify bridge node is running:

   .. code-block:: bash

      ros2 node list

2. Check for errors in bridge terminal output

3. Restart ROS 2 daemon:

   .. code-block:: bash

      ros2 daemon stop
      ros2 daemon start

4. Re-source workspace:

   .. code-block:: bash

      source ~/.bashrc

Build Errors
~~~~~~~~~~~~

**Symptom:** ``colcon build`` fails

**Solutions:**

1. Clean workspace:

   .. code-block:: bash

      cd ~/carla_ws
      rm -rf build install log
      colcon build --symlink-install

2. Install dependencies:

   .. code-block:: bash

      rosdep update
      rosdep install --from-paths src --ignore-src -r -y

3. Check ROS 2 is sourced:

   .. code-block:: bash

      echo $ROS_DISTRO

Python API Import Error
~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** ``ModuleNotFoundError: No module named 'carla'``

**Solutions:**

1. Re-install CARLA Python API:

   .. code-block:: bash

      cd ~/carla/CARLA_0.9.16/PythonAPI/carla/dist
      pip3 install --force-reinstall carla-0.9.16-cp310-cp310-linux_x86_64.whl

2. Verify installation:

   .. code-block:: bash

      python3 -c "import carla; print(carla.__file__)"

---------------------------------------------------------
Performance Optimization
---------------------------------------------------------

For Better Performance
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Lower graphics quality
   ./CarlaUE4.sh -quality-level=Low -nosound -vulkan

   # Reduce camera resolution
   ros2 run carla_ros2_bridge carla_camera_publisher \
       --ros-args -p image_width:=640 -p image_height:=480

   # Run headless (no graphics window)
   ./CarlaUE4.sh -RenderOffScreen -quality-level=Low

For Better Quality
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Higher graphics
   ./CarlaUE4.sh -quality-level=Epic -vulkan

   # Higher resolution
   ros2 run carla_ros2_bridge carla_camera_publisher \
       --ros-args -p image_width:=1920 -p image_height:=1080

CARLA Command-Line Options
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Option**
     - **Description**
   * - ``-quality-level=Low``
     - Low graphics quality (fastest)
   * - ``-quality-level=Epic``
     - Highest graphics quality
   * - ``-nosound``
     - Disable audio (reduces CPU usage)
   * - ``-vulkan``
     - Use Vulkan renderer (NVIDIA preferred)
   * - ``-opengl``
     - Use OpenGL (fallback for compatibility)
   * - ``-RenderOffScreen``
     - Headless mode (no window)
   * - ``-windowed``
     - Run in window (not fullscreen)
   * - ``-ResX=1280 -ResY=720``
     - Set window resolution

---------------------------------------------------------
Creating Your Own Nodes
---------------------------------------------------------

Subscriber Template
~~~~~~~~~~~~~~~~~~~

Create your own subscriber to process CARLA images:

.. code-block:: python

   import rclpy
   from rclpy.node import Node
   from sensor_msgs.msg import Image
   from cv_bridge import CvBridge
   import cv2

   class MyCarlaSubscriber(Node):
       def __init__(self):
           super().__init__('my_carla_subscriber')

           self.subscription = self.create_subscription(
               Image,
               '/carla/camera/image',
               self.image_callback,
               10
           )

           self.bridge = CvBridge()
           self.get_logger().info('Subscriber started')

       def image_callback(self, msg):
           # Convert ROS Image to OpenCV format
           cv_image = self.bridge.imgmsg_to_cv2(msg, 'rgb8')

           # Process image (your code here)
           gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
           edges = cv2.Canny(gray, 50, 150)

           # Display (optional)
           cv2.imshow('CARLA Camera', cv_image)
           cv2.imshow('Edges', edges)
           cv2.waitKey(1)

           self.get_logger().info('Processed frame')

   def main():
       rclpy.init()
       node = MyCarlaSubscriber()
       rclpy.spin(node)
       cv2.destroyAllWindows()
       rclpy.shutdown()

   if __name__ == '__main__':
       main()

---------------------------------------------------------
Comparison with Ubuntu 24.04 Setup
---------------------------------------------------------

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - **Aspect**
     - **Ubuntu 22.04 (This Guide)**
     - **Ubuntu 24.04**
   * - Ubuntu Version
     - 22.04 (Jammy)
     - 24.04 (Noble)
   * - Python Version
     - 3.10
     - 3.12
   * - Installation
     - Native (tar.gz)
     - Docker
   * - Setup Complexity
     - Simpler
     - More complex (Docker config)
   * - GPU Setup
     - Direct
     - Requires nvidia-docker
   * - Functionality
     - Identical
     - Identical

Both setups use the same ROS 2 package and provide identical functionality.

---------------------------------------------------------
References
---------------------------------------------------------

- CARLA Documentation: https://carla.readthedocs.io/en/0.9.16/
- CARLA Downloads: https://github.com/carla-simulator/carla/releases/tag/0.9.16
- Python API Reference: https://carla.readthedocs.io/en/0.9.16/python_api/
- GitHub Issue (Double Slash Bug): https://github.com/carla-simulator/carla/issues/9278