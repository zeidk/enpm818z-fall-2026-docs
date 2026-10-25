====================================================
Foxglove: A Second Viewer for ROS 2
====================================================

.. admonition:: Read this after L8
   :class: important

   This page is **reading material** for L8. In the group projects you watch
   your ROS 2 topics in RViz. Foxglove is a second viewer: it shows the same
   topics, live or from a recording, and it puts a 3D view, a camera image,
   plots and the log in one window. This page takes you from installing it to
   recording a drive and replaying it, on a demo that shows L8's predictions
   live on CARLA.

**What you need:** ROS 2 Jazzy, the course workspace with the
`enpm818z-fall-2026-carla-ros <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros>`__
repository built, and a CARLA server, as for the L2 demo.

**The numbers on this page** come from one run of the demo on Town01, with
its defaults: 8 traffic cars, a 5 s horizon and a point every 0.1 s. The
demo's settings are in its ``config/l8_scene.yaml``, each with a comment that
says whether it copies L8 or was chosen for the demo.


What Foxglove Is
----------------

Foxglove is a program that shows robot data: 3D scenes, images, plots, logs
and raw messages, each in its own **panel**. A set of panels, arranged in one
window, is a **layout**. You save a layout to a file and open it again later,
or give it to someone else.

Foxglove reads data from two kinds of source:

- **Live:** a running ROS 2 system, through ``foxglove_bridge``, a ROS 2 node
  that serves your topics over a WebSocket (a network connection that stays
  open, so the bridge can send each message as it arrives).
- **Recorded:** a file made with ``ros2 bag``, in the MCAP format
  (``.mcap``). Foxglove opens it with no ROS 2 running.

How it compares with RViz, the viewer the group projects use:

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * -
     - **RViz**
     - **Foxglove**
   * - How it gets data
     - It is a ROS 2 node: it runs on a computer in the same ROS 2 network
     - Through ``foxglove_bridge``, over a WebSocket, so it can run on another
       computer: ``ws://ROBOT_IP:8765``
   * - Recordings
     - Needs ``ros2 bag play`` to publish them again
     - Opens an ``.mcap`` file directly, with a timeline to move through it
   * - In one window
     - 3D displays and images
     - 3D, images, plots, the log, raw messages and the graph of nodes and
       topics, each in a panel
   * - Account
     - None
     - A free Foxglove account (below)

The two do not compete: keep RViz for the group projects, and use Foxglove
when you want plots, the log or a recording next to the 3D view.


Getting It
----------

1. **Create a free Foxglove account.** Foxglove's getting-started guide lists
   it as the first step (`Getting started guide
   <https://docs.foxglove.dev/docs/getting-started-guide>`__). Sign up with
   your umd.edu address: Foxglove's Academic plan is "free of charge" for
   "students, researchers, and educators" who sign up with an ``.edu`` or
   ``.ac`` email address (`Foxglove pricing <https://foxglove.dev/pricing>`__).
2. **Install the desktop app.** Download the Linux ``.deb`` from
   `foxglove.dev/download <https://foxglove.dev/download>`__, then:

   .. code-block:: bash

      sudo apt install ./foxglove-studio-*.deb

3. **Install the bridge** for your ROS 2 version
   (`Foxglove's ROS 2 guide
   <https://docs.foxglove.dev/docs/getting-started/frameworks/ros2>`__):

   .. code-block:: bash

      sudo apt install ros-$ROS_DISTRO-foxglove-bridge


Connecting to a Live System
---------------------------

Any running ROS 2 system works. Start the bridge next to it:

.. code-block:: bash

   ros2 launch foxglove_bridge foxglove_bridge_launch.xml

The bridge listens on port **8765**. In Foxglove, choose **Open
connection**, then **Foxglove WebSocket**, and enter ``ws://localhost:8765``.
From another computer, replace ``localhost`` with the robot's IP address.


The Demo: L8's Predictions, Live
--------------------------------

The package ``l8_foxglove_demo`` (`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l8_foxglove_demo/README.md>`__)
starts three things with one command:

1. **The L2 bridge**, with RViz off. It spawns the AV with its camera and
   LiDAR, and owns the simulation clock, as in L2.
2. **foxglove_bridge**, on port 8765.
3. **The node** ``l8_scene``. It spawns 8 traffic cars at the spawn points
   nearest the AV (chosen), and every 0.1 s it publishes each car's box and
   its constant-velocity (CV) prediction, 5 s ahead: L8's model, horizon and
   step.

.. code-block:: bash

   cd ~/enpm818z_ws
   colcon build --symlink-install --packages-select l2_carla_demo l8_foxglove_demo
   source install/setup.bash
   ros2 launch l8_foxglove_demo l8_foxglove.launch.py

Start the CARLA server first and give it 30 to 60 s to load the level. Then,
in Foxglove:

1. **Open connection**, **Foxglove WebSocket**, ``ws://localhost:8765``.
2. **Layouts**, **Import from file...**, and pick
   ``install/l8_foxglove_demo/share/l8_foxglove_demo/foxglove/l8_layout.json``.

.. note::

   **The predictions start from CARLA's true velocity**, not from a tracker.
   The demo is about the viewer. In L8, the velocity came from a fit to a
   noisy track, and CV's error grew with the horizon even with no turn ahead.

What the node publishes:

.. list-table::
   :widths: 30 30 40
   :header-rows: 1
   :class: compact-table

   * - **Topic**
     - **Type**
     - **What**
   * - ``/l8/vehicles``
     - ``visualization_msgs/MarkerArray``
     - each car's box (its true pose and size) and a label with its speed
   * - ``/l8/predictions``
     - ``visualization_msgs/MarkerArray``
     - each car's CV path, 5 s ahead, with a dot every second
   * - ``/l8/ego/speed``
     - ``std_msgs/Float32``
     - the AV's speed, in m/s
   * - ``/l8/nearest/speed``
     - ``std_msgs/Float32``
     - the speed of the car nearest the AV, in m/s
   * - ``/l8/nearest/distance``
     - ``std_msgs/Float32``
     - that car's distance to the AV, in m

The node also writes a warning to the log when a car's CV path comes within
2 m of the AV's own CV path **at the same time**: 2 m is half of a 4 m lane,
L8's miss threshold. Two paths that cross the same point at different times
never meet, so the node compares the two predictions time by time, every
0.1 s up to 5 s. One warning from our run: "car 205: its CV path comes 2.0 m
from the AV's in 5.0 s".

On our run, the five ``/l8`` topics arrived at 10.0 Hz, the LiDAR at 20 Hz
(one sweep per simulation step) and the camera at about 15.7 Hz.


The Panels
----------

The layout has five panels: the 3D view and the camera on top, the plot, the
log and the raw messages below.

3D
~~

The 3D panel draws anything with a position: point clouds, markers,
transforms, paths (`3D panel
<https://docs.foxglove.dev/docs/visualization/panels/3d>`__). In the demo:

- **the LiDAR**, ``/carla/ego_vehicle/lidar``, colored by its ``intensity``
  field with the Turbo color map;
- **the boxes**, ``/l8/vehicles``: dark for the AV, orange for the other
  cars, each with its speed above it;
- **the predictions**, ``/l8/predictions``: blue for each car's CV path, gray
  for the AV's own, a dot every second.

The view follows the AV's frame, ``ego_vehicle``, which the L2 bridge
publishes on ``/tf``. Foxglove has three ways to follow a frame: **Pose**
(position and full orientation, the layout's choice), **Heading** (position
and yaw, with the horizon kept level) and **Position** (position only).

Image
~~~~~

The Image panel shows ``/carla/ego_vehicle/rgb_front/image``, the AV's front
camera. Match a car you see in the image with its box in the 3D view: its
label gives its number and speed.

Plot
~~~~

The Plot panel draws numbers from messages against time (`Plot panel
<https://docs.foxglove.dev/docs/visualization/panels/plot>`__). Each series
is a **message path**: a topic and a field, for example ``/l8/ego/speed.data``.
The layout plots the AV's speed and the nearest car's speed, in m/s. When the
AV stops at a red light, its line drops to 0.

Log
~~~

The Log panel shows ROS 2 log messages, ``rcl_interfaces/msg/Log`` on
``/rosout`` (`Log panel
<https://docs.foxglove.dev/docs/visualization/panels/log>`__). You can set a
minimum severity, show or hide each node, and filter by search terms, a
comma-separated list where any term matches. In the demo, set the minimum to
**Warn** to keep only the 2 m warnings.

Raw Messages
~~~~~~~~~~~~

The Raw Messages panel shows the latest message on a message path, as a tree
you can open and close (`Raw Messages panel
<https://docs.foxglove.dev/docs/visualization/panels/raw-messages>`__). The
layout shows ``/l8/nearest/distance``. Its **diff** mode marks what changed
between messages: green for additions, red for deletions and yellow for
changes.

Topic Graph
~~~~~~~~~~~

Not in the layout: add it yourself (exercise 5). The Topic Graph panel draws
the nodes, the topics and the services, and which node publishes or
subscribes to which topic (`Topic Graph panel
<https://docs.foxglove.dev/docs/visualization/panels/topic-graph>`__). It
needs a live connection; it does not work on a recording.

.. admonition:: Why there is no Map panel
   :class: note

   Foxglove's Map panel places a GNSS position on a world map. The L2 bridge
   publishes ``/carla/ego_vehicle/gnss``, but Town01's map file places its
   origin at latitude 0, longitude 0 (``+lat_0=0 +lon_0=0`` in
   ``Town01.xodr``): the AV would drive on open sea.


Layouts
-------

From Foxglove's `layouts page
<https://docs.foxglove.dev/docs/visualization/layouts>`__:

- **Import:** the **Layouts** menu, **Import from file...**, and pick a
  layout's JSON file.
- **Change:** open a panel's settings to choose its topics, or use its menu
  to split it and add another panel next to it. Changes not saved yet show a
  purple "unsaved" mark.
- **Save:** **Save changes** in the layout's menu, or **Revert** to go back.
- **Export:** **Export...** in the layout's menu writes it to a JSON file.
  Commit that file next to your code, so your team opens the same view.

A layout file only names topics and settings: it holds no data. The demo's
``l8_layout.json`` is a short JSON file that you can read.


Recording and Playback
----------------------

``ros2 bag`` writes MCAP files, which Foxglove opens directly. Record only
what you need: the camera and the LiDAR fill a disk fast. For the demo:

.. code-block:: bash

   ros2 bag record -s mcap -o l8_drive \
       /tf /tf_static /rosout /l8/vehicles /l8/predictions \
       /l8/ego/speed /l8/nearest/speed /l8/nearest/distance

Stop it with Ctrl+C after 30 s. Then open the ``.mcap`` file in the
``l8_drive`` folder: drag it onto Foxglove, press Ctrl+O, or choose **Open
local file(s)** (`Foxglove's ROS 2 guide
<https://docs.foxglove.dev/docs/getting-started/frameworks/ros2>`__). The same
layout works on the recording. A timeline appears at the bottom: play, pause,
and drag to any moment, and every panel shows the data of that moment.


Exercises
---------

Run the demo and import the layout first. Exercises 1 to 5 use the live
connection, and exercise 6 uses a recording.

.. admonition:: Exercise 1: a car and its prediction
   :class: hint

   Pick a car that is moving straight in the 3D view. Read its speed on its
   label. With CV, how far ahead of the car is the dot at 1 s? At 5 s? Check
   it against the grid (one square is 5 m in the layout).

   .. dropdown:: Answer

      CV keeps the velocity, so the dot at :math:`h` seconds is speed ×
      :math:`h` ahead: at 8.0 m/s, 8.0 × 1 = 8.0 m and 8.0 × 5 = 40.0 m,
      eight squares. A car that is turning still gets a straight blue path:
      CV has no turn in it, as in L8.

.. admonition:: Exercise 2: a warning, found
   :class: hint

   Set the Log panel's minimum severity to **Warn**. When a warning appears,
   find that car in the 3D view by the number on its label. Where do its blue
   path and the AV's gray path come close?

   .. dropdown:: Answer

      The warning names the car and the time, for example "car 205: its CV
      path comes 2.0 m from the AV's in 5.0 s". Look at the two dots for that
      second on the two paths: they are within 2 m. Often the car is waiting
      or crossing at a junction, and the warning goes away a moment later,
      once one of the two moves: a CV prediction changes every 0.1 s.

.. admonition:: Exercise 3: one more series
   :class: hint

   Add ``/l8/nearest/distance.data`` to the Plot panel. What happens to the
   line when the nearest car changes?

   .. dropdown:: Answer

      The line jumps: the topic always gives the distance to whichever car is
      nearest now, so when another car becomes the nearest, the distance
      changes at once instead of smoothly.

.. admonition:: Exercise 4: the LiDAR, colored by height
   :class: hint

   In the 3D panel's settings, open ``/carla/ego_vehicle/lidar`` and color it
   by ``z`` instead of ``intensity``. What stands out now? Then switch the
   follow mode from **Pose** to **Position**, and drive through a turn.

   .. dropdown:: Answer

      Colored by height, the road is one color and the cars, poles and walls
      stand out above it. With **Position**, the view no longer turns with
      the AV: the scene rotates on screen in a turn instead of staying ahead.

.. admonition:: Exercise 5: who publishes what
   :class: hint

   Split a panel and add a **Topic Graph**. Which node publishes
   ``/l8/predictions``? Then change a setting while it runs:

   .. code-block:: bash

      ros2 param set /l8_scene warn_distance 4.0

   What happens in the Log panel?

   .. dropdown:: Answer

      ``l8_scene`` publishes it. With 4.0 m, more pairs of paths come close
      enough, so warnings appear more often. The node reads the parameter on
      every check, so the change takes effect at once.

.. admonition:: Exercise 6: a recording
   :class: hint

   Record 30 s with the command above, stop the demo, and open the file.
   Drag the timeline to a warning in the Log panel. Does the Topic Graph
   still work?

   .. dropdown:: Answer

      The 3D view, the plot and the log all jump to that moment: every panel
      shows the recorded data at the time you choose. The Topic Graph stays
      empty: it needs a live connection.

.. admonition:: Post-work
   :class: important

   Record 30 s of your group project's stack, the topics your RViz shows, and
   open the recording in Foxglove. Build a layout for it and export it next
   to your code.
