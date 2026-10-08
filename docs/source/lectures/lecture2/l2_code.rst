====================================================
Code
====================================================

L2 uses two repositories. Every script and node here needs a running CARLA
0.9.16 server (see :doc:`Using CARLA from Python </carla/carla-python>`).

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Repository**
     - **What L2 uses from it**
   * - `enpm818z-fall-2026-carla-python
       <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python>`_
     - Folder ``lecture2/``: Demos 1, 2 and 4, the LiDAR-to-camera projection,
       and the viewer.
   * - `enpm818z-fall-2026-carla-ros
       <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros>`_
     - The ROS 2 package ``l2_carla_demo``: Demo 3, and the sensor topics that
       the L3 and L5 packages subscribe to.

Every Python script connects to ``localhost:2000`` by default; pass ``--host``
and ``--port`` to change that.


Python scripts: ``lecture2/``
-----------------------------

.. list-table::
   :widths: 28 72
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **What it is**
   * - ``carla_common.py``
     - Shared helpers, not run on its own: connect with a readable error,
       synchronous mode that restores the settings on exit, an actor pool that
       destroys everything (also on Ctrl+C), the ego vehicle, sensor mounts
       derived from the vehicle's bounding box, and the camera intrinsics.
   * - ``demo1_connect.py``
     - Demo 1: connect, load a town, inspect the blueprint library.
   * - ``demo2_spawn_suite.py``
     - Demo 2: spawn the ego vehicle and the full sensor suite, and compare
       the configured rates with the delivered ones.
   * - ``demo4_weather.py``
     - Demo 4: cycle the weather presets and report what each one does to each
       sensor.
   * - ``lidar_to_camera.py``
     - The calibration section run once: LiDAR points projected into the
       camera image, plus two deliberately wrong versions.
   * - ``spectator_view.py``
     - A window that follows the ego vehicle, for watching a headless server.
       It never ticks the simulator.


``demo1_connect.py``
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python3 demo1_connect.py --town Town03

Arguments: ``--town`` (default ``Town03``). It prints the client and server
versions, the available maps, the number of vehicle and sensor blueprints, the
default attributes of the RGB camera (size, field of view, ``sensor_tick``) and
the number of spawn points. It writes no files.


``demo2_spawn_suite.py``
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python3 demo2_spawn_suite.py --seconds 20 --save-dir out/

.. list-table::
   :widths: 25 20 55
   :header-rows: 1
   :class: compact-table

   * - **Argument**
     - **Default**
     - **Meaning**
   * - ``--seconds``
     - 20
     - How long to drive.
   * - ``--save-dir``
     - none
     - Write every 20th camera frame to ``<save-dir>/rgb/``.
   * - ``--no-autopilot``
     - off
     - Leave the vehicle parked.

The suite: an RGB camera (1280 x 720, 90 degree field of view), a 32-channel
LiDAR (50 m, 300,000 points per second, 20 Hz), a radar (30 x 10 degrees,
100 m), an IMU and a GNSS. It prints the vehicle's half-sizes, the mount
positions it derived, the camera intrinsics, then, per sensor, the messages
received and the delivered rate, with the mean LiDAR points per sweep and radar
detections per scan.


``demo4_weather.py``
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python3 demo4_weather.py --view
   python3 demo4_weather.py --seconds-per-preset 4 --save-dir out/weather

.. list-table::
   :widths: 28 17 55
   :header-rows: 1
   :class: compact-table

   * - **Argument**
     - **Default**
     - **Meaning**
   * - ``--seconds-per-preset``
     - 4
     - Time spent in each weather.
   * - ``--save-dir``
     - none
     - Write one camera image per preset, ``<preset>.png``.
   * - ``--view``
     - off
     - Open a window (needs ``pygame``).
   * - ``--contact-sheet``
     - none
     - An image path: all presets in one 2 x 3 image.

The presets: clear noon, wet noon, hard rain, sunset, dense fog and night. For
each one it prints the mean LiDAR returns and radar detections per scan, and the
camera's brightness and contrast (0 to 255).


``lidar_to_camera.py``
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python3 lidar_to_camera.py --out out/projection.png
   python3 lidar_to_camera.py --no-permutation --out out/projection_none.png
   python3 lidar_to_camera.py --bad-sign --out out/projection_flipped.png

.. list-table::
   :widths: 25 20 55
   :header-rows: 1
   :class: compact-table

   * - **Argument**
     - **Default**
     - **Meaning**
   * - ``--out``
     - ``projection.png``
     - The overlay image.
   * - ``--no-permutation``
     - off
     - Leave out the axis permutation P: every point lands off the image, so
       the overlay is blank.
   * - ``--bad-sign``
     - off
     - Use P with one sign wrong: the points land and the shape is
       recognizable, but the scene is upside down. This is the axis trap.
   * - ``--weather``
     - none
     - A preset name from ``demo4_weather.py``.
   * - ``--compare``
     - none
     - A path: the correct and the ``--bad-sign`` overlays, both built from the
       same captured frame, side by side.
   * - ``--warmup``
     - 30
     - Ticks to wait before capturing.

It prints the frame it captured and how many of the LiDAR points land on the
image, and for the two wrong modes, what went wrong.


``spectator_view.py``
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python3 spectator_view.py              # follows the ego, spawns one if none
   python3 spectator_view.py --no-spawn   # only watches

Arguments: ``--width`` 1280, ``--height`` 720, ``--no-spawn``. Keys: TAB
changes the weather, C the camera (chase, bonnet, overhead), R toggles the
autopilot, ESC or Q quits. Start it **after** the script you want to watch: it
follows the vehicle whose ``role_name`` is ``ego``, and spawns its own if there
is none. Needs ``pygame``.


ROS 2 package: ``l2_carla_demo``
--------------------------------

The bridge between CARLA and ROS 2 that the rest of the course is written
against. It is a small node of our own rather than CARLA's built-in
``--ros2`` flag, because in 0.9.16 that flag builds topic names with a doubled
slash, which ROS 2 rejects (see :doc:`CARLA ROS 2 bridge </carla/carla-ros2>`).

.. code-block:: bash

   cd ~/enpm818z_ws
   colcon build --symlink-install --packages-select l2_carla_demo
   source install/setup.bash
   ros2 launch l2_carla_demo demo.launch.py
   ros2 launch l2_carla_demo demo.launch.py town:=Town03 rviz:=false

Give the server 30 to 60 s to load its level first, or the client times out.

**Launch arguments:** ``host`` (localhost), ``port`` (2000), ``town`` (empty:
keep the loaded map; ``Town03`` is the one used in class), ``rviz`` (true),
``rate_report`` (true), ``gnss_noise_m`` (0.0: CARLA's default, no GNSS noise;
the L3 EKF hands-on uses 1.5, the standard deviation per axis in meters).


Node ``carla_bridge``
~~~~~~~~~~~~~~~~~~~~~

Puts the server in synchronous mode and calls ``world.tick()`` from a timer:
**it owns the simulation clock**, so no other client may tick. It spawns a
``vehicle.tesla.model3`` with ``role_name`` ``ego`` at the first free spawn
point, on autopilot (CARLA's Traffic Manager, also put in synchronous mode so
the vehicle actually drives), and attaches the sensors rigidly at mounts derived from
the vehicle's own bounding box. On Ctrl+C it destroys every actor and puts the
server back in its original mode.

.. list-table::
   :widths: 35 20 45
   :header-rows: 1
   :class: compact-table

   * - **Parameter** (``config/sensors.yaml``)
     - **Value**
     - **Meaning**
   * - ``delta``
     - 0.05
     - The simulation step: 20 Hz.
   * - ``vehicle``
     - ``vehicle.tesla.model3``
     - The ego blueprint.
   * - ``autopilot``
     - true
     -
   * - ``image_width``, ``image_height``
     - 1280, 720
     -
   * - ``camera_fov``
     - 90.0
     - Degrees.
   * - ``lidar_channels``
     - 32
     -
   * - ``lidar_range``
     - 50.0
     - Meters.
   * - ``lidar_points_per_second``
     - 300000
     - One full turn per simulation step.

.. list-table::
   :widths: 45 25 30
   :header-rows: 1
   :class: compact-table

   * - **Topic**
     - **Type**
     - **Frame**
   * - ``/carla/ego_vehicle/rgb_front/image``
     - ``Image`` (bgra8)
     - ``ego_vehicle/rgb_front_optical``
   * - ``/carla/ego_vehicle/rgb_front/camera_info``
     - ``CameraInfo`` (latched)
     - ``ego_vehicle/rgb_front_optical``
   * - ``/carla/ego_vehicle/lidar``
     - ``PointCloud2`` (x, y, z, intensity)
     - ``ego_vehicle/lidar``
   * - ``/carla/ego_vehicle/radar_front``
     - ``PointCloud2`` (x, y, z, velocity)
     - ``ego_vehicle/radar_front``
   * - ``/carla/ego_vehicle/imu``
     - ``Imu``
     - ``ego_vehicle/imu``
   * - ``/carla/ego_vehicle/gnss``
     - ``NavSatFix``
     - ``ego_vehicle/gnss``
   * - ``/carla/ego_vehicle/marker``
     - ``Marker`` (latched)
     - ``ego_vehicle``

Sensor topics are best effort; the camera intrinsics are latched, so a late
subscriber still gets them. In RViz, an Image display must be set to **Best
Effort**: its default, Reliable, does not connect to a best-effort topic and
shows nothing. The marker is the AV's body for RViz, its bounding box from
CARLA (4.79 x 2.16 x 1.49 m for the Tesla Model 3), sent once and drawn with the
``ego_vehicle`` frame. **TF:** ``map -> ego_vehicle`` at every tick, and
static transforms from ``ego_vehicle`` to each sensor, plus
``ego_vehicle/rgb_front -> ego_vehicle/rgb_front_optical``, the axis
permutation from the calibration slides. Every stamp is the simulation time.


Node ``rate_report``
~~~~~~~~~~~~~~~~~~~~

Subscribes to the five sensor topics and prints, every 2 s, the rate each one
actually delivers, computed from the message stamps over the last 5 s. The
point: the delivered rate is not the configured rate, and it drops as the scene
gets busy.


``conversions.py``
~~~~~~~~~~~~~~~~~~

Every CARLA measurement to its ROS 2 message, with each frame decision in the
open: CARLA's y axis points right, ROS's points left, so every y flips sign and
so do the rotations about x and z. The GP1 starter imports these functions
instead of rewriting them.
