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
   mkdir -p ~/enpm818z_ws/src
   cd ~/enpm818z_ws/src

   # Clone the ROS 2 package repository
   git clone https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros.git

   # Return to workspace root
   cd ~/enpm818z_ws

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

   # Check that the package is available
   ros2 pkg list | grep l2_carla_demo

   # Check its executables
   ros2 pkg executables l2_carla_demo

Expected output:

.. code-block:: text

   l2_carla_demo carla_bridge
   l2_carla_demo rate_report

.. note::
   The repository is ``enpm818z-fall-2026-carla-ros``; the ROS 2 **package**
   inside it is ``l2_carla_demo``. Those are different names and both are
   used: you clone the first and you build, run and launch the second.

   The plain Python demos live in a separate repository,
   `enpm818z-fall-2026-carla-python
   <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python>`_. Those
   are CARLA clients and need no workspace and no build.

---------------------------------------------------------
Step 4: Setup Environment Configuration
---------------------------------------------------------

Create Setup Script
~~~~~~~~~~~~~~~~~~~

The setup function does two jobs: it configures the ROS 2 environment, and it
defines the commands you will use to run the server.

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: table-hover

   * - **Command**
     - **What it does**
   * - ``carla_basic [quality]``
     - Starts the server and blocks until it actually accepts connections.
       Quality defaults to ``Epic``; pass ``Low`` on a weaker GPU.
   * - ``carla_log``
     - Follows the server's output. This is where a crash explains itself.
   * - ``carla_stop`` / ``carla_kill``
     - Stops the server and removes every CARLA container.

Add the following function to your ``~/.bashrc``:

.. code-block:: bash

   nano ~/.bashrc

   # Add this function at the end:
   carla_setup() {
       CARLA_WS="$HOME/enpm818z_ws"
       ROS_SETUP="/opt/ros/jazzy/setup.bash"

       # ---- start the server ------------------------------------------
       carla_basic() {
           docker rm -f carla >/dev/null 2>&1
           docker run -d --name carla \
               --runtime=nvidia \
               --gpus all \
               --net=host \
               -v /dev/shm:/dev/shm \
               -e NVIDIA_VISIBLE_DEVICES=all \
               -e NVIDIA_DRIVER_CAPABILITIES=all \
               carlasim/carla:0.9.16 \
               /bin/bash -c "./CarlaUE4.sh -RenderOffScreen -vulkan -nosound -quality-level=${1:-Epic}" >/dev/null || return 1

           # The container can die during startup. Say so, and show why,
           # instead of waiting for a port that will never open.
           printf 'starting CARLA'
           while ! ss -ltn 2>/dev/null | grep -q ':2000 '; do
               if [ -z "$(docker ps -q -f name=carla)" ]; then
                   printf '\nthe server died before it accepted connections. Its output:\n'
                   docker logs carla 2>&1 | tail -20
                   return 1
               fi
               printf '.'
               sleep 2
           done

           # The RPC port opens before the level has finished loading, so a
           # client that connects the moment it sees the port can sit there
           # waiting. Wait for a call that needs the level to be up.
           printf ' level'
           while ! python3 -c 'import carla, sys
   c = carla.Client("localhost", 2000); c.set_timeout(5.0)
   try:
       c.get_world().get_map()
   except Exception:
       sys.exit(1)' >/dev/null 2>&1; do
               printf '.'
               sleep 2
           done
           printf '\nready on localhost:2000\n'
       }

       # ---- stop it and clean up --------------------------------------
       carla_stop() {
           local ids
           ids=$(docker ps -a --format '{{.ID}} {{.Image}}' | awk '$2 ~ /carla/ {print $1}')
           if [ -n "$ids" ]; then
               echo "$ids" | xargs docker rm -f >/dev/null 2>&1
               echo "removed $(echo "$ids" | wc -l) CARLA container(s)"
           else
               echo "no CARLA containers"
           fi
           return 0
       }

       alias carla_kill='carla_stop'
       alias carla_log='docker logs -f carla'

       # ---- ROS 2 environment -----------------------------------------
       export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
       export ROS_DOMAIN_ID=42
       unset ROS_LOCALHOST_ONLY

       # Only force a Fast DDS profile if one is actually present. Pointing
       # FASTRTPS_DEFAULT_PROFILES_FILE at a file that does not exist gives
       # you default behaviour and a false sense of having configured it.
       if [ -f "$CARLA_WS/src/fastdds_udp.xml" ]; then
           export FASTRTPS_DEFAULT_PROFILES_FILE="$CARLA_WS/src/fastdds_udp.xml"
           export RMW_FASTRTPS_USE_QOS_FROM_XML=1
       else
           unset FASTRTPS_DEFAULT_PROFILES_FILE
           unset RMW_FASTRTPS_USE_QOS_FROM_XML
       fi

       if [ -f "$ROS_SETUP" ]; then
           source "$ROS_SETUP"
       else
           echo "Error: ROS 2 not found at $ROS_SETUP"
           return 1
       fi

       if [ -f "$CARLA_WS/install/setup.bash" ]; then
           source "$CARLA_WS/install/setup.bash"
       else
           echo "Warning: CARLA workspace not built. Run: cd $CARLA_WS && colcon build"
       fi

       ros2 daemon stop >/dev/null 2>&1
       ros2 daemon start >/dev/null 2>&1

       echo "CARLA environment ready:  carla_basic | carla_log | carla_stop"
   }

   # Auto-run setup when starting new terminal
   carla_setup

Save and reload:

.. code-block:: bash

   source ~/.bashrc

Typical session:

.. code-block:: text

   $ carla_basic
   starting CARLA.. level.
   ready on localhost:2000

   $ python3 demo1_connect.py --town Town03
   ...

   $ carla_stop
   removed 1 CARLA container(s)

.. note::
   ``ROS_DOMAIN_ID`` must be the same on every machine that needs to see your
   topics, and different from your neighbour's if you do not want to see
   theirs. Pick one number and use it everywhere.

Why the Server Runs Headless
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The launch command contains ``-RenderOffScreen`` and passes **no** ``DISPLAY``
and **no** X11 socket. That is deliberate, and it is the difference between a
server that works and one that crashes.

.. danger::
   **Symptom.** The client connects, ``get_available_maps()`` succeeds, and
   then ``load_world()`` times out. The container is gone, and
   ``docker ps -a`` shows it **Exited (139)**, which is a segmentation fault.

   **Cause.** ``docker logs`` shows the real reason:

   .. code-block:: text

      MESA: warning: Driver does not support the 0xa788 PCI ID.
      Signal 11 caught.
      CommonUnixCrashHandler: Signal=11

   That PCI ID is an **Intel integrated GPU**. On a laptop with switchable
   graphics, the X server usually runs on the integrated chip, so giving the
   container a ``DISPLAY`` sends Unreal down the Mesa software path instead of
   onto the NVIDIA GPU, and it segfaults partway through loading a map.

   **Fix.** ``-RenderOffScreen`` skips X entirely and renders directly on the
   NVIDIA device. Note that the client-side error, a timeout, points at the
   wrong thing completely: the server did not run slowly, it died.

.. tip::
   Forcing NVIDIA offload (``__NV_PRIME_RENDER_OFFLOAD=1``,
   ``__VK_LAYER_NV_optimus=NVIDIA_only``) does remove the Mesa warning, but the
   windowed server still segfaults on the map load. Headless is not a
   workaround here, it is the configuration that works.

.. _seeing-the-simulation-ubuntu24:

Seeing the Simulation Without a Window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A headless server opens no window, so nothing appears when ``carla_basic``
finishes. To watch the simulation, run a **viewer client** instead. It renders
on your desktop's normal graphics path and never touches Unreal's:

.. code-block:: bash

   python3 spectator_view.py

Keys: ``TAB`` weather, ``C`` camera position, ``R`` autopilot, ``ESC`` quit.
The viewer is a passive observer, so it can be left open while a demo script
runs.

Why It Waits Twice
~~~~~~~~~~~~~~~~~~

``carla_basic`` prints ``starting CARLA..`` and then ``level.`` because those
are two different conditions:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - **Wait**
     - **What it means**
   * - port 2000 listening
     - The RPC server is up. It is **not** yet able to answer questions about
       the world.
   * - ``get_world().get_map()`` succeeds
     - The level has finished loading. Only now is a client guaranteed a
       prompt answer.

A client that connects on the first condition alone can appear to hang for a
long time with nothing to explain it.

Why the Container Is Not Removed Automatically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is no ``--rm`` in the ``docker run`` command, on purpose. When the server
crashes, its output is the only thing that says why, and ``--rm`` deletes the
container and its logs the instant it dies. Instead, ``carla_basic`` removes any
previous container by name before starting a new one, so nothing accumulates,
and ``carla_log`` or ``docker logs carla`` still works after a crash.

``carla_stop`` removes every container built from a CARLA image, not just the
one named ``carla``. A crashed container stays in the list in the exited state
while still holding its name, and containers started by an older alias sit there
under generated names such as ``modest_montalcini``.

Why ``--ros2`` Is Not Used
~~~~~~~~~~~~~~~~~~~~~~~~~~

CARLA 0.9.16 can publish ROS 2 topics itself with a ``--ros2`` flag, and the
launch command above does not use it. See
:ref:`Understanding the CARLA 0.9.16 ROS 2 Bug <known-issue-ubuntu24>` below for
why. The course uses its own bridge package instead.

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
3. **Publishes to clean topics** -- ``/carla/ego_vehicle/rgb_front/image`` (no double slash)
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

**Terminal 1: start the CARLA server**

.. code-block:: bash

   carla_basic

It prints ``ready on localhost:2000`` when the level has finished loading.

.. important::
   **No window appears, and that is correct.** The server runs with
   ``-RenderOffScreen``. To watch the simulation, use the viewer client
   described under :ref:`seeing-the-simulation-ubuntu24`.

**Terminal 2: run the bridge**

.. code-block:: bash

   source ~/enpm818z_ws/install/setup.bash
   ros2 launch l2_carla_demo demo.launch.py

That single launch file starts three things: the bridge node, RViz2 with a
prepared configuration, and a rate reporter. Running the bridge on its own is
also fine:

.. code-block:: bash

   ros2 run l2_carla_demo carla_bridge

You should see:

.. code-block:: text

   [INFO] [carla_bridge]: spawned 6 actors
   [INFO] [carla_bridge]: ticking at 20 Hz on Carla/Maps/Town10HD_Opt

**Terminal 3: verify the topics**

.. code-block:: bash

   ros2 topic list | grep carla
   ros2 topic hz /carla/ego_vehicle/rgb_front/image
   ros2 topic echo /carla/ego_vehicle/imu --once

The topic list:

.. code-block:: text

   /carla/ego_vehicle/gnss
   /carla/ego_vehicle/imu
   /carla/ego_vehicle/lidar
   /carla/ego_vehicle/radar_front
   /carla/ego_vehicle/rgb_front/camera_info
   /carla/ego_vehicle/rgb_front/image

.. note::
   ``ros2 topic hz`` will report something like **14.7 Hz, then 18.7 Hz**
   against a configured 20 Hz. That gap is real and it is worth looking at:
   the rate you set on a blueprint is a request, not a guarantee, and it falls
   as the scene gets busier. Timing is a first-class concern in this course.


---------------------------------------------------------
Package Overview
---------------------------------------------------------

The ``l2_carla_demo`` package contains two nodes and one launch file.

carla_bridge
~~~~~~~~~~~~

Spawns an ego vehicle with a full sensor suite and publishes every stream onto
ROS 2 topics. It also owns the simulation clock: it puts the server into
synchronous mode and calls ``world.tick()`` from a timer, so **do not run a
second client that also ticks**.

.. list-table:: Published topics
   :widths: 42 30 28
   :header-rows: 1
   :class: table-striped

   * - **Topic**
     - **Type**
     - **Notes**
   * - ``/carla/ego_vehicle/rgb_front/image``
     - ``sensor_msgs/Image``
     - ``bgra8``, as CARLA delivers it
   * - ``/carla/ego_vehicle/rgb_front/camera_info``
     - ``sensor_msgs/CameraInfo``
     - latched; intrinsics never change
   * - ``/carla/ego_vehicle/lidar``
     - ``sensor_msgs/PointCloud2``
     - fields ``x y z intensity``
   * - ``/carla/ego_vehicle/radar_front``
     - ``sensor_msgs/PointCloud2``
     - fields ``x y z velocity``
   * - ``/carla/ego_vehicle/imu``
     - ``sensor_msgs/Imu``
     -
   * - ``/carla/ego_vehicle/gnss``
     - ``sensor_msgs/NavSatFix``
     -
   * - ``/tf``, ``/tf_static``
     - ``tf2_msgs/TFMessage``
     - the sensor extrinsics, as transforms

Sensor data is published **best effort**, so a dropped frame is preferred to a
stalled pipeline. ``camera_info`` is latched instead, so a subscriber that
starts late still receives the intrinsics.

Parameters come from ``config/sensors.yaml``. The useful ones:

.. list-table::
   :widths: 32 20 48
   :header-rows: 1

   * - **Parameter**
     - **Default**
     - **Meaning**
   * - ``town``
     - ``""``
     - map to load; empty keeps whatever is loaded
   * - ``delta``
     - ``0.05``
     - simulation step, so 20 Hz
   * - ``vehicle``
     - ``vehicle.tesla.model3``
     - ego blueprint
   * - ``image_width`` / ``image_height``
     - ``1280`` / ``720``
     - camera resolution
   * - ``camera_fov``
     - ``90.0``
     - degrees
   * - ``lidar_channels``
     - ``32``
     - beams

For example, at a lower resolution:

.. code-block:: bash

   ros2 run l2_carla_demo carla_bridge --ros-args \
       -p image_width:=640 -p image_height:=360

.. important::
   **Sensor mounting positions are not parameters.** The node derives them from
   the ego vehicle's own bounding box, because every blueprint is a different
   size and copied numbers put sensors inside bodywork. Note that
   ``bounding_box.extent`` is a **half**-size in metres.

rate_report
~~~~~~~~~~~

Subscribes to all five sensor topics and prints their delivered rates side by
side, plus the spread between the newest and oldest timestamp in the set. That
spread is the number to look at before fusing anything: two measurements you
combine should describe the same instant, and these do not.

.. code-block:: bash

   ros2 run l2_carla_demo rate_report

demo.launch.py
~~~~~~~~~~~~~~

Starts the bridge, RViz2 and the rate report together.

.. code-block:: bash

   ros2 launch l2_carla_demo demo.launch.py
   ros2 launch l2_carla_demo demo.launch.py town:=Town03 rviz:=false

Coordinate Frames
~~~~~~~~~~~~~~~~~

CARLA uses **x forward, y right, z up** (left-handed). ROS REP-103 uses
**x forward, y left, z up** (right-handed). Every ``y`` changes sign on the way
out, and so does every rotation about ``x`` and ``z``. The package does this in
one place, ``conversions.py``. Get it wrong and RViz shows a scene that looks
fine until you notice the traffic is driving on the wrong side of the road.

The camera has two frames. ``ego_vehicle/rgb_front`` follows the ROS body
convention. Its child ``ego_vehicle/rgb_front_optical`` is **x right, y down,
z along the optical axis**, which is what the intrinsic matrix ``K`` expects.
That child transform is the axis permutation from the lecture, written as a
``tf`` instead of a matrix.


---------------------------------------------------------
Advanced Usage
---------------------------------------------------------

Visualizing in RViz2
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   ros2 launch l2_carla_demo demo.launch.py

The launch file already starts RViz2 with a prepared configuration showing the
LiDAR cloud, the RADAR detections coloured by range rate, the camera image and
the transform tree, with the fixed frame set to ``ego_vehicle``.

To open RViz2 by hand instead, run ``rviz2``, click **Add** then **By topic**,
and pick the topics you want. Set **Fixed Frame** to ``ego_vehicle``. For the
sensor topics you must also set **Reliability Policy** to **Best Effort**, or
the display will stay empty with no error.

Recording Data
~~~~~~~~~~~~~~

.. code-block:: bash

   # Record the camera and the LiDAR
   ros2 bag record /carla/ego_vehicle/rgb_front/image /carla/ego_vehicle/lidar

   # Record every CARLA topic, and the transforms, which you will need
   ros2 bag record -r "/carla/.*" /tf /tf_static

   # Play back recorded data
   ros2 bag play <bag_file>

Custom Resolution
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Higher resolution
   ros2 run l2_carla_demo carla_bridge \
       --ros-args -p image_width:=1920 -p image_height:=1080

   # Lower resolution, for a machine that is struggling
   ros2 run l2_carla_demo carla_bridge \
       --ros-args -p image_width:=640 -p image_height:=360

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

**Symptom:** ``ros2 topic list`` does not show ``/carla/ego_vehicle/rgb_front/image``

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

      cd ~/enpm818z_ws
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
   ros2 run l2_carla_demo carla_bridge \
       --ros-args -p image_width:=640 -p image_height:=360

   # Fewer LiDAR beams
   ros2 run l2_carla_demo carla_bridge --ros-args -p lidar_channels:=16

``carla_basic`` takes the graphics quality as an argument, so no editing is
needed: ``carla_basic Low``.

For Better Quality
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Higher resolution
   ros2 run l2_carla_demo carla_bridge \
       --ros-args -p image_width:=1920 -p image_height:=1080

``Epic`` is already the default for ``carla_basic``.

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