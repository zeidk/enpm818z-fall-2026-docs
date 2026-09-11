==================================================================
CARLA ROS 2 Bridge
==================================================================

This page applies to **both** platforms -- the native Ubuntu 22.04 install and
the Ubuntu 24.04 Docker image. The bridge is an ordinary ROS 2 node that runs on
the host and talks to the CARLA server over the Python API, so it works the same
way on either. Only the ROS distribution and the command that starts the server
differ, and those are shown in tabs.

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Component**
     - **Version/Details**
   * - Course
     - ENPM818Z -- On-Road Automated Vehicles
   * - CARLA Version
     - 0.9.16
   * - Package
     - ``l2_carla_demo`` (custom course bridge, not ``carla-ros-bridge``)
   * - ROS 2 Distribution
     - Humble on 22.04, Jazzy on 24.04

.. admonition:: Pick your platform once
   :class: tip

   The tabs on this page are synchronised. Choose **Native (22.04)** or
   **Docker (24.04)** in any tab-set and every other tab-set switches with it.


---------------------------------------------------------
Before You Start
---------------------------------------------------------


Finish the setup guide for your platform first:

- :doc:`Ubuntu 22.04 -- native setup <ubuntu22>`
- :doc:`Ubuntu 24.04 -- Docker setup <ubuntu24>`

The server itself knows nothing about ROS 2. The bridge connects to it exactly
as any other Python client would.


---------------------------------------------------------
Step 1: Clone and Build the Bridge Package
---------------------------------------------------------


.. code-block:: bash

   mkdir -p ~/enpm818z_ws/src
   cd ~/enpm818z_ws/src
   git clone https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros.git
   cd ~/enpm818z_ws

Build it against your ROS distribution:

.. tab-set::

   .. tab-item:: Native (22.04)
      :sync: native

      .. code-block:: bash

         source /opt/ros/humble/setup.bash
         rosdep update
         rosdep install --from-paths src --ignore-src -r -y
         colcon build --symlink-install
         source install/setup.bash

   .. tab-item:: Docker (24.04)
      :sync: docker

      .. code-block:: bash

         source /opt/ros/jazzy/setup.bash
         colcon build --symlink-install
         source install/setup.bash

Verify the build:

.. code-block:: bash

   ros2 pkg list | grep l2_carla_demo
   ros2 pkg executables l2_carla_demo

Expected output:

.. code-block:: text

   l2_carla_demo carla_bridge
   l2_carla_demo rate_report


---------------------------------------------------------
Step 2: ROS 2 Environment Configuration
---------------------------------------------------------


Add a function to your shell startup file that sources ROS 2 and the workspace.

.. note::
   These instructions assume **bash**. If your terminal runs **zsh** (check with
   ``echo $SHELL``), use ``~/.zshrc`` instead and reload with
   ``source ~/.zshrc``. The function works unchanged in both shells.

.. code-block:: bash

   nano ~/.bashrc

Add the following at the **end** of that file, substituting your ROS
distribution on the ``ROS_SETUP`` line:

.. code-block:: bash

   # ---------------------------------------------------------------------------
   # ROS 2 environment for the CARLA bridge (ENPM818Z)
   #
   # Sources ROS 2 and the course workspace and sets the DDS configuration the
   # bridge expects. It does NOT start the CARLA server.
   #
   # carla_ros is called at the bottom of this file, so it runs in every new
   # terminal.
   # ---------------------------------------------------------------------------
   carla_ros() {
       CARLA_WS="$HOME/enpm818z_ws"
       ROS_SETUP="/opt/ros/jazzy/setup.bash"     # 22.04 native: /opt/ros/humble/setup.bash

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

       echo "ROS 2 environment ready for CARLA"
   }

   # Auto-run when starting a new terminal
   carla_ros

Save and reload:

.. code-block:: bash

   source ~/.bashrc

.. note::
   ``ROS_DOMAIN_ID`` must be the same on every machine that needs to see your
   topics, and different from your neighbour's if you do not want to see
   theirs. Pick one number and use it everywhere.


---------------------------------------------------------
Running CARLA with ROS 2
---------------------------------------------------------


Basic Workflow
~~~~~~~~~~~~~~

**Terminal 1: start the CARLA server**

.. tab-set::

   .. tab-item:: Native (22.04)
      :sync: native

      .. code-block:: bash

         cd ~/carla/CARLA_0.9.16
         ./CarlaUE4.sh -quality-level=Low -nosound -vulkan

      A CARLA window opens. Wait until the city is visible.

   .. tab-item:: Docker (24.04)
      :sync: docker

      .. code-block:: bash

         carla_basic

      It prints ``ready on localhost:2000`` when the level has finished
      loading.

      .. important::
         **No window appears, and that is correct.** The server runs with
         ``-RenderOffScreen``. To watch the simulation, use the viewer client
         described in :doc:`carla-python`.

**Terminal 2: run the bridge**

.. code-block:: bash

   source ~/enpm818z_ws/install/setup.bash
   ros2 launch l2_carla_demo demo.launch.py

That single launch file starts three things: the bridge node, RViz2 with a
prepared configuration, and a rate reporter. Running the bridge on its own is
also fine:

.. code-block:: bash

   ros2 run l2_carla_demo carla_bridge


---------------------------------------------------------
Package Overview
---------------------------------------------------------
Package Overview

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
Advanced Usage

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
Creating Your Own Nodes
---------------------------------------------------------
Creating Your Own Nodes

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
               '/carla/ego_vehicle/rgb_front/image',
               self.image_callback,
               10
           )

           self.bridge = CvBridge()
           self.get_logger().info('Subscriber started')

       def image_callback(self, msg):
           # Convert ROS Image to OpenCV format
           # The bridge publishes bgra8, exactly as CARLA delivers it.
           # Ask cv_bridge for bgr8 and it drops the alpha channel for you.
           cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

           # Process image (your code here)
           gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
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

.. _known-ros2-bug:
.. _known-issue-ubuntu22:
.. _known-issue-ubuntu24:

---------------------------------------------------------
Understanding the CARLA 0.9.16 ROS 2 Bug
---------------------------------------------------------
Understanding the CARLA 0.9.16 ROS 2 Bug

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
Troubleshooting
---------------------------------------------------------
Troubleshooting

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
Next Steps
---------------------------------------------------------


- :doc:`Using CARLA from Python <carla-python>` -- driving the server directly,
  without ROS 2.


---------------------------------------------------------
References
---------------------------------------------------------


- CARLA Documentation: https://carla.readthedocs.io/en/0.9.16/
- Python API Reference: https://carla.readthedocs.io/en/0.9.16/python_api/
- GitHub Issue (Double Slash Bug): https://github.com/carla-simulator/carla/issues/9278
- ROS 2 Humble: https://docs.ros.org/en/humble/
- ROS 2 Jazzy: https://docs.ros.org/en/jazzy/
