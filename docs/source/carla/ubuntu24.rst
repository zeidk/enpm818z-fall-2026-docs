==================================================================
CARLA Setup Guide - Ubuntu 24.04 (Docker)
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
     - 24.04 (Noble Numbat)
   * - CARLA Version
     - 0.9.16
   * - Installation Method
     - Docker

---------------------------------------------------------
Overview
---------------------------------------------------------

This guide walks you through setting up CARLA 0.9.16 on Ubuntu 24.04 using Docker. You will use a **custom ROS 2 bridge package** that bypasses CARLA's native ROS 2 implementation due to a known bug (see :ref:`known-issue-ubuntu24`).

**What You Will Install:**

- Docker runtime with NVIDIA GPU support
- CARLA 0.9.16 Docker image
- CARLA Python client (via pip)
- Custom ROS 2 bridge package

.. note::
   **Why Docker?** CARLA 0.9.16 does not have native support for Ubuntu 24.04. Running CARLA inside a Docker container is the supported workaround -- the containerized CARLA server interfaces directly with the ROS 2 environment running on the host system.

---------------------------------------------------------
Terminology
---------------------------------------------------------

.. admonition:: Key Terms

   **Host**
      The physical or virtual machine (your Ubuntu 24.04 system) on which Docker is installed. The host runs the Docker engine and provides the underlying hardware resources -- CPU, GPU, memory, and network -- to containers. In this guide, ROS 2 and the CARLA Python client run directly on the host.

   **Container**
      A lightweight, isolated runtime environment created from a Docker image. A container packages an application and all its dependencies so it runs consistently regardless of the host OS. In this guide, the CARLA server runs inside a container while communicating with the host over the network.

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
     - Ubuntu 24.04 (Noble Numbat)
   * - ROS 2 Distribution
     - Already installed
   * - GPU
     - NVIDIA GPU (recommended for performance)
   * - RAM
     - Minimum 8 GB, Recommended 16 GB
   * - Disk Space
     - ~15 GB for Docker image and dependencies
   * - Python
     - 3.12 (comes with Ubuntu 24.04)

Verify Your Ubuntu Version
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   lsb_release -a

You should see ``Ubuntu 24.04`` in the output.

---------------------------------------------------------
Step 1: Pull CARLA Docker Image
---------------------------------------------------------

Download the CARLA 0.9.16 Docker image:

.. code-block:: bash

   # Pull CARLA image (this may take 10-15 minutes)
   docker pull carlasim/carla:0.9.16

   # Verify image is downloaded
   docker images | grep carla

Expected output:

.. code-block:: text

   carlasim/carla:0.9.16             98d224668ad0       20.7GB             0B

---------------------------------------------------------
Step 2: Install Additional Dependencies
---------------------------------------------------------

.. code-block:: bash

   # Install required Python packages
   pip3 install numpy pygame

   # Install CARLA Python client
   pip3 install carla==0.9.16

   # Verify installations
   python3 -c "import numpy; import pygame; import carla; print('All dependencies OK')"

**Command breakdown:**

- ``pip3 install numpy pygame`` — Installs two Python packages using pip:

  - **NumPy** — A numerical computing library used for array operations, linear algebra, and mathematical transformations. CARLA scripts use NumPy to process sensor data (e.g., converting raw camera/lidar buffers into arrays) and to perform coordinate transformations.
  - **Pygame** — A multimedia library for creating graphical windows and handling keyboard/mouse input. CARLA's example scripts use Pygame to render the simulation camera feed in a display window and to capture user input for manual vehicle control.

- ``pip3 install carla==0.9.16`` — Installs the CARLA Python client library, pinned to version **0.9.16** to match the Docker server image pulled in Step 1. This library provides the Python API (``carla.Client``, ``carla.World``, ``carla.Vehicle``, etc.) that your scripts use to connect to the CARLA server, spawn actors, attach sensors, and control the simulation.

- ``python3 -c "import numpy; import pygame; import carla; print('All dependencies OK')"`` — Runs a one-line Python script that attempts to import all three packages. If any package is missing or improperly installed, Python will raise an ``ImportError`` and you will know which dependency needs to be reinstalled. If all imports succeed, it prints ``All dependencies OK``.

---------------------------------------------------------
Step 2.5: Download Additional Maps (Town04)
---------------------------------------------------------

CARLA's base installation includes limited maps. For highway scenarios (e.g., behavioral planning assignments), you need **Town04** which has a dedicated multi-lane highway loop.

Download Additional Maps
~~~~~~~~~~~~~~~~~~~~~~~~

Download the additional maps package on your **host machine**:

.. code-block:: bash

   cd ~/Downloads
   wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/AdditionalMaps_0.9.16.tar.gz

Install Maps into Docker Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 1. Start CARLA container with a name
   docker run --privileged --gpus all --net=host \
     -e DISPLAY=$DISPLAY \
     -e XDG_RUNTIME_DIR=/tmp/runtime-carla \
     -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
     --name carla-server \
     -it carlasim/carla:0.9.16

   # 1b. In a NEW terminal, verify the container is running
   docker ps --filter "name=carla-server"

   # 2. In the same NEW terminal, copy the maps to the container
   docker cp ~/Downloads/AdditionalMaps_0.9.16.tar.gz carla-server:/workspace/

   # 3. Enter the container as root to extract
   docker exec -it --user root carla-server bash

   # 4. Inside the container, extract and import the maps
   cd /workspace
   tar -xzf AdditionalMaps_0.9.16.tar.gz
   ./ImportAssets.sh
   rm AdditionalMaps_0.9.16.tar.gz

   # 5. Exit the container
   exit

   # 6. Restart CARLA to load the new maps
   docker stop carla-server
   docker start -ai carla-server

.. note::

   ``./ImportAssets.sh`` produces **no output on success**. It silently moves files from
   ``/workspace/Import/`` into ``CarlaUE4/Content/``. You can verify the maps were installed by
   checking that the ``Import/`` directory is now empty and that the map files exist:

   .. code-block:: bash

      ls Import/                              # Should be empty
      ls CarlaUE4/Content/Carla/Maps/ | grep Town04  # Should show Town04 files

   


Verify Maps Installation
~~~~~~~~~~~~~~~~~~~~~~~~

After installing the maps, make sure the CARLA server is running before verifying. In one terminal,
start (or restart) the container so it loads the newly imported maps:

.. code-block:: bash

   # Remove the old container if it still exists
   docker rm carla-server 2>/dev/null

   # Start CARLA
   docker run --privileged --gpus all --net=host \
     -e DISPLAY=$DISPLAY \
     -e XDG_RUNTIME_DIR=/tmp/runtime-carla \
     -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
     --name carla-server \
     -it carlasim/carla:0.9.16

Wait 30-60 seconds for CARLA to fully initialize. Then, in a **second terminal**, run the
following Python script to query the available maps:

.. code-block:: bash

   python3 -c "
   import carla
   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   maps = client.get_available_maps()
   print('Available maps:')
   for m in sorted(maps):
       print(f'  - {m.split(\"/\")[-1]}')
   "

Expected output should include:

.. code-block:: text

   Available maps:
     - Town01
     - Town02
     - Town03
     - Town04
     - Town04_Opt
     - Town05
     - ...

Load Town04
~~~~~~~~~~~

To load Town04 for highway scenarios:

.. code-block:: python

   import carla

   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)

   # Load Town04 (highway map)
   world = client.load_world('Town04')
   print("Town04 loaded successfully!")

---------------------------------------------------------
Step 3: Clone and Build the ROS 2 Bridge Package
---------------------------------------------------------

Clone the Repository
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create workspace
   mkdir -p ~/carla_ws/src
   cd ~/carla_ws/src

   # Clone the repository
   git clone -b ubuntu24 https://github.com/zeidk/enpm818z-fall-2026-carla.git carla_ros2_bridge

   # Return to workspace root
   cd ~/carla_ws

Build the Package
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Source ROS 2
   source /opt/ros/jazzy/setup.bash

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
   carla_ros2_bridge carla_camera_publisher_with_display
   carla_ros2_bridge carla_image_subscriber

---------------------------------------------------------
Step 4: Setup Environment Configuration
---------------------------------------------------------

Create Setup Script
~~~~~~~~~~~~~~~~~~~

Add the following function to your ``~/.bashrc``:

.. code-block:: bash

   nano ~/.bashrc

   # Add this function at the end:
   carla_setup() {
       # Configuration
       CARLA_WS="/home/$USER/carla_ws"

       echo "Setting up CARLA ROS 2 environment..."

       # Setup environment variables
       export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
       export ROS_DOMAIN_ID=0
       unset ROS_LOCALHOST_ONLY
       unset FASTRTPS_DEFAULT_PROFILES_FILE

       # Source ROS 2
       if [ -f "/opt/ros/jazzy/setup.bash" ]; then
           source /opt/ros/jazzy/setup.bash
       else
           echo "Error: ROS 2 not found at /opt/ros/jazzy"
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

       # Create CARLA Docker alias
       alias carla='xhost +local:root && docker run \
           --rm \
           --privileged \
           --runtime=nvidia \
           --gpus all \
           --net=host \
           --ipc=host \
           -v /dev/shm:/dev/shm \
           -e DISPLAY=$DISPLAY \
           -e XDG_RUNTIME_DIR=/tmp/runtime-carla \
           -e NVIDIA_VISIBLE_DEVICES=all \
           -e NVIDIA_DRIVER_CAPABILITIES=all \
           -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
           carlasim/carla:0.9.16 \
           /bin/bash -c "./CarlaUE4.sh -nosound -quality-level=Low -vulkan"'

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

       cd "$CARLA_WS"
   }

   # Auto-run setup when starting new terminal
   carla_setup

Save and reload:

.. code-block:: bash

   source ~/.bashrc

.. _known-issue-ubuntu24:

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

**Symptom:** ``docker: Error response from daemon...``

**Solutions:**

1. Verify Docker is running:

   .. code-block:: bash

      sudo systemctl status docker
      sudo systemctl start docker

2. Check GPU access:

   .. code-block:: bash

      docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

3. Allow X11 forwarding:

   .. code-block:: bash

      xhost +local:root

XDG_RUNTIME_DIR Errors on Startup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** CARLA container starts but prints repeated errors:

.. code-block:: text

   error: XDG_RUNTIME_DIR not set in the environment.

**Explanation:** ``XDG_RUNTIME_DIR`` is a Linux environment variable that points to a per-user
directory (typically ``/run/user/<UID>``) used by display servers and Wayland/X11 compositors to
store runtime sockets. When Docker runs the CARLA process inside the container, this variable is
not set by default, so libraries that look for it (e.g., Vulkan, SDL, PulseAudio) emit these warnings.

**These errors are usually harmless** — CARLA will still run and render correctly as long as GPU
access and X11 forwarding are configured properly. However, if you want to suppress them or if
CARLA fails to render, try the following:

1. Set the variable explicitly when launching the container:

   .. code-block:: bash

      docker run --privileged --gpus all --net=host \
        -e XDG_RUNTIME_DIR=/tmp/runtime-carla \
        -e DISPLAY=$DISPLAY \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
        --name carla-server \
        -it carlasim/carla:0.9.16

2. Ensure X11 forwarding is allowed on the host before starting the container:

   .. code-block:: bash

      xhost +local:root

3. If you are on a **Wayland** session (default on Ubuntu 24.04), you may also need to set
   ``WAYLAND_DISPLAY`` or switch to an X11 session at the login screen.

Cannot Connect to CARLA
~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** ``Failed to connect to CARLA: timeout``

**Solutions:**

1. Wait for CARLA to fully load (30-60 seconds after window appears)

2. Check CARLA container is running:

   .. code-block:: bash

      docker ps

   You should see output similar to:

   .. code-block:: text

      CONTAINER ID   IMAGE                      STATUS          NAMES
      a1b2c3d4e5f6   carlasim/carla:0.9.16      Up 2 minutes    carla-server

   - If the ``STATUS`` column says ``Up``, the container is running.
   - If the container is not listed, it may have exited. Run ``docker ps -a`` to see all containers
     (including stopped ones). The ``STATUS`` column will show the exit code
     (e.g., ``Exited (1) 30 seconds ago``), which can help diagnose why it stopped.
   - To restart a stopped container: ``docker start -ai carla-server``

3. Verify CARLA is listening on its default port (2000):

   .. code-block:: bash

      netstat -tuln | grep 2000

   Expected output:

   .. code-block:: text

      tcp   0   0   0.0.0.0:2000   0.0.0.0:*   LISTEN

   If there is no output, CARLA has not finished starting yet or crashed during initialization.
   Check the container logs for errors:

   .. code-block:: bash

      docker logs carla-server

4. Verify the CARLA Python client can connect:

   .. code-block:: bash

      python3 -c "import carla; c = carla.Client('localhost', 2000); c.set_timeout(2.0); print(c.get_server_version())"

   This should print the server version (e.g., ``0.9.16``). If it raises a timeout error, CARLA
   is either still loading or the ``--net=host`` flag was not used when starting the container.

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

2. Verify dependencies:

   .. code-block:: bash

      rosdep install --from-paths src --ignore-src -r -y

3. Check ROS 2 is sourced:

   .. code-block:: bash

      echo $ROS_DISTRO

---------------------------------------------------------
Performance Optimization
---------------------------------------------------------

For Better Performance
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Reduce camera resolution
   ros2 run carla_ros2_bridge carla_camera_publisher \
       --ros-args -p image_width:=640 -p image_height:=480

To adjust CARLA graphics quality, edit the ``carla`` alias in ``~/.bashrc`` and change ``-quality-level=Low`` to the desired level, then run ``source ~/.bashrc``.

For Better Quality
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Higher resolution
   ros2 run carla_ros2_bridge carla_camera_publisher \
       --ros-args -p image_width:=1920 -p image_height:=1080

To use ``-quality-level=Epic``, edit the ``carla`` alias in ``~/.bashrc`` accordingly.

---------------------------------------------------------
Comparison with Ubuntu 22.04 Setup
---------------------------------------------------------

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - **Aspect**
     - **Ubuntu 22.04**
     - **Ubuntu 24.04 (This Guide)**
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
- Docker Documentation: https://docs.docker.com/
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/
- GitHub Issue (Double Slash Bug): https://github.com/carla-simulator/carla/issues/9278