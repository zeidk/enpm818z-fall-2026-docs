====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L6, the slides shown in class and
   the reading slides that go with them, in the same order and with the same
   sections. You can read them at home. The deck keeps more material in its
   appendix, on :doc:`the appendix page <l6_appendix>`, "Going Further":

   - the error bound in detail;
   - RTK in more detail;
   - ICP step 2 solved by hand, one slide per step (Centroids, Center,
     Compare, Angle, Turn, Shift), and the SVD;
   - which way to score: point to point against point to line, GICP, and NDT
     on our map;
   - NDT's score;
   - the likelihood field;
   - integrity: NIS, the gate and the protection level;
   - the pose-graph least squares;
   - APE and RPE.

   The papers and pages cited below are listed in full on :doc:`the
   References page <l6_references>`.


.. _l6-lec-story:

Today's Story
-------------

L5 found where everything else is, relative to the AV. **Today we find where
the AV itself is**, and how far off it may be: 0.29 m on a local street
(:ref:`Introduction <l6-lec-introduction>`).

We follow one recorded drive through a CARLA town (:ref:`The Drive
<l6-lec-drive>`). **GNSS** gives the AV's position on Earth, a few meters off,
until tall buildings block the sky and the fixes stop (:ref:`GNSS and RTK
<l6-lec-gnss>`). The AV's own wheels and gyro carry the pose through the gap,
but their small errors add up (:ref:`Dead Reckoning <l6-lec-dr>`). An
**extended Kalman filter** combines the two: a pose that is smooth between
fixes and pulled back at each one, yet still drifting while GNSS is out
(:ref:`Fusion in the EKF <l6-lec-ekf>`).

A **map** stops the drift (:ref:`Against a Map <l6-lec-map>`): the LiDAR scan
is compared with the map, many guesses at once to find the AV (:ref:`Monte
Carlo Localization <l6-lec-mcl>`), then one guess moved until the scan lies on
the map (:ref:`Scan Registration <l6-lec-icp>`). Last, how that map is built
in the first place (:ref:`SLAM <l6-lec-slam>`).

**Losing GNSS removes one input, not the pose.**


.. _l6-lec-introduction:

Introduction
------------

**L5** finds where everything else is, **relative to the AV**. **L6** finds
where **the AV is in the world**.

.. figure:: /_static/images/L6/l5_to_l6.png
   :alt: Two top views side by side. Left, labeled L5, where everything else is, relative to the AV: the AV on a road with its own x forward and y left axes, and arrows from the AV to another car and to a pedestrian. Right, labeled L6, where the AV is in the world: a street grid with a frame at its bottom left corner, x east and y north, and an arrow from that corner to the AV on a road, labeled pose (x, y, theta).
   :width: 90%
   :align: center

   **Left, L5:** the AV sits at the origin of its own frame, :math:`x`
   forward and :math:`y` left, and the arrows go from the AV to another car
   and to a pedestrian. **Right, L6:** the frame is fixed at a corner of the
   street grid, :math:`x` east and :math:`y` north, and one arrow goes from
   that corner to the AV: its pose :math:`(x, y, \theta)`.


.. _l6-lec-bound:

Step 1: How Much Room the Lane Leaves the AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

How far off may the AV's position be? Reid et al. start from one goal: "to
keep the vehicle in its respective lane" (Reid et al., 2019).

.. figure:: /_static/images/L6/bound_lane.png
   :alt: Two top views of a lane 3.0 meters wide, with the AV drawn 2.1 meters wide and 5.8 meters long, driving to the right. Panel 1, straight road: rust arrows between the AV's sides and the lane edges, each labeled 0.45 m, and the lane width labeled lane 3.0 m. Panel 2, a turn of radius 20 meters: the lane bends upward in the middle; a rust dashed box around the AV, 0.33 m larger on every side, touches the inner edge at its middle and the outer edge at its two far corners, marked with rust dots; rust arrows labeled 0.33 m below the AV and in front of it.
   :width: 95%
   :align: center

   The lane and the AV, to scale. **1:** on a straight road, 0.45 m of room
   on each side. **2:** in a turn of radius 20 m, the dashed box keeps the
   same 0.33 m gap on all sides. It touches the inner edge at its middle and
   the outer edge at its two far corners (dots).

1. A local-street lane: 3.0 m wide. The largest passenger car: 2.1 m wide
   and 5.8 m long (US standards, in the paper).
2. Straight road: :math:`(3.0 - 2.1) / 2 = 0.45` m of room on each side.
3. In a turn of radius 20 m, the lane curves but the car does not, so the
   edges come closer: the inner one at the car's middle, the outer one at
   its corners (dots). The dashed box keeps the same gap on all sides; the
   largest gap that fits is 0.33 m. The bound must hold in turns too, so the
   paper uses 0.33 m, not 0.45 m.

.. tip::

   See :ref:`l6-app-bound` in :doc:`Going Further <l6_appendix>` for the
   bound's formulas.


.. _l6-lec-bound-2:

Step 2: the Heading Takes a Share, 0.29 m Is Left
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/bound_heading.png
   :alt: A top view of a lane, a double arrow at the left labeled lane 3.0 m. A black AV points along the lane, with a gray dotted line straight ahead from its center. A red AV on top of it is turned a little; a red line runs from its center along its turned heading, and a short red arrow between the dotted line and the red line is labeled 0.5 degrees. A label, the front swings sideways, points to the red AV's front. Below, a bar spanning a double arrow labeled 0.33 m is split into a short red part labeled 0.04 m and a long gray part labeled left for the position error: 0.29 m.
   :width: 75%
   :align: center

   The **black AV** is where the AV really is, pointing along the lane. The
   **red AV** is the pose the localizer reports, turned by a heading error
   labeled 0.5 degrees; the turn in the drawing is larger, so that it
   shows. The bar splits Step 1's 0.33 m: 0.04 m for the heading, 0.29 m
   left for the position error.

**The point:** Step 1's 0.33 m of room must cover every error, not only the
position error. A heading error uses part of it.

1. In the figure, the black AV is the actual AV, pointing along the lane.
   The red AV is the pose the localizer reports, turned by a heading error.
2. A heading error swings the front of the car sideways, toward the lane
   edge. The paper allows 0.5 degrees; by its formula, that uses 0.04 m of
   the 0.33 m.
3. What is left for the position error is :math:`0.33 - 0.04 = 0.29` m.


.. _l6-lec-bound-def:

The Error Bound: 0.29 m on a Local Street
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Steps 1 and 2 give the number the rest of the lecture checks against.

.. admonition:: Definition: error bound (the paper's alert limit)
   :class: note

   "The allowable maximum position error of the vehicle to ensure it is
   within the lane" (Reid et al., 2019). The error may pass it at most once
   in :math:`10^8` hours of driving. On a local street: 0.29 m, with 95% of
   errors within 0.10 m.

Today GNSS, dead reckoning, the fused filter and MCL are each scored against
this **0.29 m**.


.. _l6-lec-pose-twice:

We Needed the AV's Pose Twice Already
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **L5, the tracker:** it follows each object in a frame that stays fixed
  while the AV drives. To put each new detection into that frame, it needs
  where the AV is.
- **L5, sharing over V2X (vehicle-to-everything radio):** a message that says
  "a pedestrian at 4 m ahead of me" is useless to another car unless it also
  says where "me" is.

.. important::

   **Today:** a filter that predicts the pose from the AV's motion, then
   corrects it with sensors, on one recorded drive, and with a map that is a
   cloud of points.


.. _l6-lec-deliver:

What a Localizer Must Deliver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/localizer_io.png
   :alt: A block diagram. Five input boxes on the left, GNSS, IMU (yaw rate), wheel speed, LiDAR scan and map, each with an arrow into a central green block labeled Localizer. One arrow leaves it to the right, to a box labeled pose in the map frame: x, y, theta, plus how sure: covariance.
   :width: 85%
   :align: center

   The localizer. **Five inputs** (GNSS, IMU yaw rate, wheel speed, LiDAR
   scan, map) go in; **one output** comes out: the pose in the map frame,
   :math:`x, y, \theta`, plus how sure it is, a covariance.

The **localizer** is software that finds the AV's pose. Its inputs are:

- **GNSS**: where the AV is, from satellites (:ref:`GNSS and RTK
  <l6-lec-gnss>`).
- **IMU yaw rate** and **wheel speed**: how the AV turns and how fast it
  moves (:ref:`Dead Reckoning <l6-lec-dr>`).
- **LiDAR scan** and **map**: what the AV sees now, and the surroundings
  recorded before; matching them gives the pose (:ref:`Against a Map
  <l6-lec-map>`).

The localizer combines the inputs into one estimate, giving more weight to
the inputs it trusts more. Its output: the pose, and how sure it is (a
covariance, defined in :ref:`Fusion in the EKF <l6-lec-ekf>`).


.. _l6-lec-frames:

Two Frames: the Map's and the Vehicle's
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/frames.png
   :alt: A top view. The map frame's origin at the bottom left, x map to the right labeled east and y map up labeled north. An AV on a road, turned at an angle, with its own vehicle frame drawn at the AV: x AV forward along the AV and y AV to its left. The angle theta is marked in orange from a dashed line parallel to the map x axis to the vehicle x axis.
   :width: 70%
   :align: center

   The two frames. The **map frame** sits at the origin, bottom left:
   :math:`x_\text{map}` east, :math:`y_\text{map}` north. The **vehicle
   frame** sits on the AV: :math:`x_\text{AV}` forward, :math:`y_\text{AV}`
   left. The angle :math:`\theta` (orange) runs from the map's :math:`x`
   direction to the AV's :math:`x` axis.

- **Map frame:** fixed to the ground. Each map picks its own. Autoware uses
  one MGRS (Military Grid Reference System) square or a chosen latitude and
  longitude (Autoware Foundation, ``autoware_map_projection_loader``); our
  CARLA map uses the town's.
- **Vehicle frame:** fixed to the AV, with its origin at the middle of the
  rear axle.
- **Pose** :math:`(x, y, \theta)`: where the vehicle frame's origin sits in
  the map frame. :math:`\theta` is the angle from the map's :math:`x` axis to
  the AV's :math:`x` axis, counted counterclockwise.


.. _l6-lec-transform:

From the Vehicle Frame to the Map Frame: the Transform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A LiDAR or radar point arrives in the **vehicle frame**. To compare it with
the map, the AV moves it to the **map frame**.

.. admonition:: Definition: transform (vehicle frame to map frame)
   :class: note

   The rule that moves a point :math:`(p_x, p_y)` from the vehicle frame to
   the map frame, given the pose :math:`(x, y, \theta)`: turn it by
   :math:`\theta`, then shift it by :math:`(x, y)`.

   .. math::

      \begin{pmatrix} x_\text{map} \\ y_\text{map} \end{pmatrix}
      = \underbrace{\begin{pmatrix} \cos\theta & -\sin\theta \\
                    \sin\theta & \cos\theta \end{pmatrix}}_{R,\ \text{the turn}}
        \begin{pmatrix} p_x \\ p_y \end{pmatrix}
      + \underbrace{\begin{pmatrix} x \\ y \end{pmatrix}}_{t,\ \text{the shift}}

**Example (numbers chosen for this example):** the AV is at :math:`(5, 2)`,
facing :math:`\theta = 90^\circ` (north). A point is 10 m straight ahead, so
:math:`(p_x, p_y) = (10, 0)`.

1. Turned by :math:`90^\circ`: :math:`(0, 10)`.
2. Shifted by :math:`(5, 2)`: :math:`(5, 12)` in the map.

The lecture uses this transform throughout. The mapping pass transforms each
scan with the true pose, MCL with each particle's pose, and ICP searches for
the transform that puts the scan on the map.


.. _l6-lec-frame-uses:

What Each Frame Is For
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 28 36 36
   :header-rows: 1
   :class: compact-table

   * -
     - **Vehicle frame**
     - **Map frame**
   * - Fixed to
     - the AV: it moves and turns
     - the ground: it never moves
   * - Used to
     - describe what the sensors measure, relative to the AV; steer and set the
       speed
     - store the map, place GNSS fixes, plan the route, keep tracked objects
       (L5), share positions over V2X (L5)
   * - The AV drives 5 m toward a sign 20 m ahead
     - the sign was at :math:`x = 20` m; now it is at :math:`x = 15` m
     - the sign's :math:`(x, y)` does not change

The 20 m and 5 m are chosen for this example.

.. important::

   **Why the map frame:** readings taken at different times, or by different
   AVs, line up only in a frame that does not move. So the localizer reports
   the pose in the map frame, and the AV uses the pose to move each reading
   from its own frame into the map frame.


.. _l6-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

After this lecture, you can:

1. say what each localization sensor measures, and how each one goes wrong;
2. predict how dead reckoning drifts, and why a heading error matters most;
3. read a fused filter's error and its own uncertainty over a GNSS outage,
   and measure a run with the absolute pose error (APE);
4. localize against a map with Monte Carlo localization (MCL), and match a
   scan to a map with ICP (iterative closest point), one iteration in
   outline;
5. explain how a loop closure corrects a drifted trajectory in SLAM
   (simultaneous localization and mapping).


.. _l6-lec-drive:

The Drive
---------

- **Where we are:** a localizer reads five inputs and returns a pose.
- **In this section:** one recorded CARLA drive, used for every method
  today.
- **What it is for:** comparing methods on the same data: same route, same
  sensors, same errors.

**Two passes on one route in CARLA.**

1. **Mapping pass:** the AV drives the route, and each LiDAR scan is
   **transformed** to the map frame with the AV's true pose, which the
   simulator knows exactly. All the transformed scans together are the map:
   a cloud of points on walls, poles and curbs.
2. **Localization pass:** the AV drives the route again. Every method today
   must find the pose from its sensors and that map, never from the true
   pose.


.. _l6-lec-imu:

The IMU: Six Sensors in One Unit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: IMU (inertial measurement unit)
   :class: note

   The core sensing device of an inertial navigation system. It "typically
   consists of three orthogonally mounted gyroscopes and three
   accelerometers" (Berkane, 2026). Orthogonal means at right angles to each
   other.

The IMU is fixed to the AV, so it reports in the vehicle frame: :math:`x`
forward, :math:`y` left, :math:`z` up.

- Three **gyroscopes** say how fast the AV turns about :math:`x`, :math:`y`
  and :math:`z`.
- Three **accelerometers** say the acceleration along :math:`x`, :math:`y`
  and :math:`z`, gravity included.

Today we use **one** of the six: the gyroscope about :math:`z`, how fast the
AV turns left or right.

.. figure:: /_static/images/L6/imu_axes.png
   :alt: A product photo of a black IMU, the Memsense MS-IMU3050, its label printing small X, Y and Z axes. Three large axes leave its top face: x forward to the right, z up, and y left going back to the upper left. On each axis a blue double-headed straight arrow marks an accelerometer, and a curved arrow around the axis marks a gyroscope; the curved arrow around z is green. A key reads: accelerometer, along the axis; gyroscope, turn rate about it; the one we use, about z.
   :width: 55%
   :align: center

   The IMU's six sensors, on a real unit: the MS-IMU3050 by Memsense, an
   Inertial Labs company. On each axis, an **accelerometer** (straight blue
   arrow) measures along the axis, and a **gyroscope** (curved arrow)
   measures the turn rate about it. **Green:** the gyroscope about
   :math:`z`, the one we use.

**Where on the AV.** The IMU is bolted to the body: on the roof next to the
GNSS antenna, or inside on the seat rails (Racelogic, IMU05 user guide).


.. _l6-lec-sensor-outputs:

What Each Sensor Outputs
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: compact-table

   * - **Sensor**
     - **What it outputs**
   * - GNSS (satellite positioning)
     - a position fix, converted to :math:`(x, y)` in the map frame, in
       meters
   * - Wheel speed
     - the AV's speed :math:`v` along its own :math:`x` axis, in m/s, from how
       fast the wheels turn
   * - Gyro
     - the yaw rate :math:`\omega`: how fast the AV turns, in rad/s, positive
       to the left
   * - LiDAR (laser ranging)
     - a scan: the points it hits on walls, poles and curbs around the AV, as
       :math:`(x, y)` in the vehicle frame

.. admonition:: Definition: Gyro
   :class: note

   A **gyroscope**, or **gyro**, is one of the IMU's six sensors: it measures
   how fast the AV turns about one axis, in radians per second. Ours turns
   about :math:`z`, the vertical axis: its output is the **yaw rate**.


.. _l6-lec-sensors:

The Sensors, and the Errors We Gave Them
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CARLA's sensors are too clean, and CARLA has no wheel encoder. So the
recorder starts from the true motion and adds errors. **We chose all of
them** for this drive.

.. list-table::
   :widths: 20 22 58
   :header-rows: 1
   :class: compact-table

   * - **Sensor**
     - **Rate**
     - **Error added (chosen)**
   * - GNSS
     - 1 fix per second
     - noise :math:`\sigma = 1.5` m in :math:`x` and in :math:`y`; a fixed
       bias of 0.5 m east and 0.3 m south; **no fixes for 400 m**
   * - Wheel speed
     - 20 per second
     - reads 0.5% fast (a worn tire); noise :math:`\sigma = 0.05` m/s
   * - Gyro (yaw rate)
     - 20 per second
     - bias 0.001 rad/s; noise :math:`\sigma = 0.01` rad/s
   * - LiDAR
     - 10 scans per second
     - none added; we keep points within 0.3 m of sensor height, one per
       20 cm square

- **Noise** is random and new at each reading. :math:`\sigma` is its
  standard deviation.
- **Bias** is the same offset on every reading.
- **The outage.** The 400 m without fixes stands in for tall buildings:
  CARLA's GNSS sensor never loses the satellites.


.. _l6-lec-route:

The Route: Two Laps of a Downtown Block
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/l6_route.png
   :alt: A top view of CARLA's Town10HD map as gray points: building walls, poles and a large central building. A rounded rectangular route about 160 by 90 meters runs around the central building, with the start marked on its bottom side by the car. Most of the route is drawn thick and red for the GNSS outage; only the top right stretch is black.
   :width: 75%
   :align: center

   The route from above, :math:`x` east and :math:`y` north in meters. The
   **gray points** are the map: walls, poles and the central building. The
   route runs around the central building, with the start on its bottom
   side. **Red:** the GNSS outage, most of the route. **Black:** the stretch
   at the top right, outside the outage on both laps.

**Measured on the localization pass:**

- CARLA town Town10HD_Opt, driven counterclockwise by its autopilot, the
  Traffic Manager;
- 916 m in 125.7 s, two laps on one road (drawn over each other), 7.3 m/s;
- no GNSS from 250 m to 650 m along the route: 34.2 s to 89.0 s, 54.8 s;
- the map: 18,661 points from the mapping pass.


.. _l6-lec-gnss:

GNSS and RTK
------------

- **Where we are:** one drive, with errors we chose and know.
- **In this section:** what GNSS gets wrong in a city, and how RTK fixes
  most of it.
- **What it is for:** the only sensor today that says where the AV is on
  Earth without a map.

**GNSS** (global navigation satellite system) is "a general term describing
any satellite constellation" for positioning (GPS.gov). **GPS** is one GNSS:
the U.S. system, run by the U.S. Space Force (GPS.gov). Galileo (European
Union), GLONASS (Russia) and BeiDou (China) are others. A receiver times
signals from several satellites and solves for its position, with **no map
and no starting point**.


.. _l6-lec-gnss-wrong:

In a City, GNSS Goes Wrong in Two Ways
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Blocked sky**
     - **Multipath**
   * - Tall buildings hide most satellites. With too few in view, the
       receiver gives a poor fix, or none: an **outage**.
     - A signal bounces off a building before it reaches the antenna. The
       path is longer, so the receiver puts the AV in the wrong place.
   * - **What the AV sees:** fixes stop. It knows they stopped.
     - **What the AV sees:** a fix that looks normal and is meters off. It
       does **not** know.

You can average noise away; you cannot average away a bias. Multipath is a
bias that comes and goes as the AV drives.


.. _l6-lec-gnss-drive:

Our Drive's GNSS: Meters Off, and Then Nothing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/gnss_error.png
   :alt: GNSS position error in meters against time, 0 to 125 seconds, one blue dot per fix, one fix per second. The dots scatter between about 0.3 and 4 meters, one at 5.4. From 34 to 89 seconds a pink band labeled no fixes has no dots.
   :width: 85%
   :align: center

   GNSS error against time on our drive. Each **blue dot** is one fix, one
   per second; its height is how far the fix is from the truth. The dots
   scatter between about 0.3 m and 4 m, with one at 5.4 m. In the **pink
   band**, 34 s to 89 s, there are no fixes.

**Measured, 72 fixes, one dot per fix, 1 s apart:** median error 1.77 m, 95%
of fixes within 3.39 m, worst 5.44 m.

The local-street bound from :ref:`the start of the lecture <l6-lec-bound>`
is 0.29 m. The median fix is **6 times** too far off:

.. math::

   1.77 / 0.29 = 6.1

These errors are the noise and the bias we added: CARLA simulates no
multipath.


.. _l6-lec-handson0:

Hands-On, Part 1: Our Drive's GNSS Fixes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The hands-on is in the course's Python repo, folder ``lecture6`` (`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture6>`__).
Part 1 shows the GNSS fixes as they arrive. :doc:`l6_code` says how to run
it and what each panel shows.

.. figure:: /_static/images/L6/handson_gnss_top.png
   :alt: Two panels of the hands-on window. Left, the whole route from above: the true path so far in black, the GNSS fixes so far as blue dots joined by a thin blue GNSS-only path, the last fix circled at the top, and the AV drawn as a small car three times its size on the bottom side. The title reads t = 62 s: no fix for 28 s; the AV drove 193 m since the last one. Right, a close-up 40 meters across around the AV at true size: the car, the true path behind it, and no fixes nearby, only two old fixes from the first lap at the right edge.
   :width: 95%
   :align: center

   The top row of the window at 62 s, in the outage. **Left:** the whole
   route; the fixes stop at the circled one, the thin blue line is the
   GNSS-only path, and the AV is drawn 3 times its size. The title reads: no
   fix for 28 s, and the AV drove 193 m since the last one. **Right:** a
   close-up 40 m across around the AV, at true size, with no fixes nearby.

1. Press Play, or Step (one fix at a time) into the outage. How far does the
   AV drive before the next fix?
2. In the window's bottom right (not shown here), each fix's error appears
   as a point as the fix arrives. Where is the center of their errors?
   Compare it with the bias we chose (0.5 m east, 0.3 m south).


.. _l6-lec-rtk:

RTK, Step 1: a Base Station on a Surveyed Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**RTK** (real-time kinematic) corrects the AV's GNSS with a second receiver
nearby.

.. figure:: /_static/images/L6/rtk_step1.png
   :alt: A side view. A satellite at the top sends signals, drawn as dashed lines, to a base station on the left, a mast on a marker labeled base station on a surveyed point, and to the AV on the right, a car labeled the AV (rover), with an antenna.
   :width: 60%
   :align: center

   One **satellite** sends to both receivers: the **base station** on the
   left, on a surveyed point, and the **AV** on the right, here called the
   **rover**.

- The **base station** is a GNSS receiver fixed on a point whose position a
  surveyor measured.
- It sees the same satellites as the AV. Each signal is slowed by the air it
  crosses, the **atmosphere**. Near the base, the AV's signals cross nearly
  the same air, so they are slowed by nearly the same amount.

.. important::

   **In Maryland:** NOAA's reference stations are on its `CORS map
   <https://arcg.is/18fWq8>`__ (NOAA National Geodetic Survey). Live
   corrections come from three real-time networks: Trimble KeyNetGPS, Topcon
   TopNET live and Leica SmartNet (Gillins et al., 2019).

.. tip::

   See :ref:`l6-app-rtk` in :doc:`Going Further <l6_appendix>` for how to
   read NOAA's CORS map.


.. _l6-lec-rtk-2:

RTK, Step 2: the Base Measures Its Own Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/rtk_step2.png
   :alt: A side view. A satellite at the top sends signals, drawn as dashed lines, to a base station on the left, a mast on a marker labeled base station on a surveyed point, and to the AV on the right, a car labeled the AV (rover), with an antenna. Below the base, a panel labeled seen from above, with arrows for east and north: a cross labeled true point and a blue dot labeled GNSS says, up and to the right of it, joined by a rust arrow; below them, in rust, error: 1.2 m east, 0.8 m north.
   :width: 60%
   :align: center

   **Seen from above,** at the base: the **true point** (cross) and where
   the base's GNSS puts it (blue dot). The **rust arrow** is the base's
   error, 1.2 m east and 0.8 m north.

1. From the satellites, the base computes where it is.
2. It knows where it really is: the surveyed point.
3. The difference is its **error**. In our example (numbers chosen): 1.2 m
   east and 0.8 m north.


.. _l6-lec-rtk-3:

RTK, Step 3: the Base Sends Its Error to the AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/rtk_step3.png
   :alt: A side view. A satellite at the top sends signals, drawn as dashed lines, to a base station on the left, a mast on a marker labeled base station on a surveyed point, and to the AV on the right, a car labeled the AV (rover), with an antenna. Below the base, a panel labeled seen from above, with arrows for east and north: a cross labeled true point and a blue dot labeled GNSS says, up and to the right of it, joined by a rust arrow; below them, in rust, error: 1.2 m east, 0.8 m north. A green arrow from the base to the AV is labeled corrections: the base's error.
   :width: 60%
   :align: center

   The **green arrow:** the base sends its error to the AV as corrections.
   The panel below the base still shows that error, 1.2 m east and 0.8 m
   north.

- The base sends its error to every receiver nearby, as **corrections**.
  The AV receiving them is called a **rover**.
- It only helps nearby: RTK works "in the vicinity of a base station" (ESA
  Navipedia).
- A real-time network uses many base stations and fills in the corrections
  between them (Gillins et al., 2019).


.. _l6-lec-rtk-4:

RTK, Step 4: the AV Subtracts the Base's Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/rtk_step4.png
   :alt: A side view. A satellite at the top sends signals, drawn as dashed lines, to a base station on the left, a mast on a marker labeled base station on a surveyed point, and to the AV on the right, a car labeled the AV (rover), with an antenna. Below the base, a panel labeled seen from above, with arrows for east and north: a cross labeled true point and a blue dot labeled GNSS says, up and to the right of it, joined by a rust arrow; below them, in rust, error: 1.2 m east, 0.8 m north. A green arrow from the base to the AV is labeled corrections: the base's error. Below the AV, a second panel seen from above: a cross labeled truth, a blue dot up and to the right joined to it by a rust arrow and labeled raw fix: 1.3 m east, 0.7 m north, and a curved green arrow from the raw fix back to a green dot almost on the cross, labeled in green corrected: 0.1 m east, 0.1 m south.
   :width: 60%
   :align: center

   **Left panel,** at the base: its error, 1.2 m east and 0.8 m north.
   **Right panel,** at the AV: the **truth** (cross), the AV's **raw fix**
   (blue dot, rust arrow), 1.3 m east and 0.7 m north, and the **corrected**
   fix (green dot) after the base's error is subtracted (curved green
   arrow), 0.1 m east and 0.1 m south.

Numbers chosen for this example:

1. Raw fix (blue dot): 1.3 m east, 0.7 m north.
2. Subtract the base's error (left panel): 1.2 m east, 0.8 m north.
3. East: 1.3 minus 1.2 leaves 0.1 m east. North: 0.8 is 0.1 more than 0.7,
   so 0.1 m south (green dot).
4. Left over: :math:`\sqrt{0.1^2 + 0.1^2} = 0.14` m, the AV's own noise and
   multipath.

.. important::

   Steps 1 to 4 use the signal's timing. RTK also times the radio wave
   itself, the **carrier**: "a few centimetres" near a base (ESA Navipedia),
   well inside the 0.29 m error bound for local streets (Reid et al., 2019).

.. tip::

   See :ref:`l6-app-rtk` in :doc:`Going Further <l6_appendix>` for why the
   carrier gives centimeters.


.. _l6-lec-rtk-limits:

What the AV Cannot Correct with RTK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/rtk_limits.png
   :alt: Three side-view panels. Panel 1, a bounce at the AV: a satellite signal reaches the base station on the left directly, while the signal to the AV bounces off a tall glass tower first, drawn as a rust dashed line; caption base in the open, the bounce is at the AV only. Panel 2, no sky: the AV under a tunnel roof, the satellite's signals stop at the roof, marked with rust crosses; caption no satellites in view, no fix, with or without RTK. Panel 3, far from the base: the base on the left and the AV on the right, joined by a double arrow along the ground. Each one's signal crosses a different shaded patch, labeled atmosphere: the blue patch over the base is labeled delay 1, the rust patch over the AV delay 2; caption beyond 10 to 20 km: the delays differ.
   :width: 95%
   :align: center

   Three errors RTK leaves in the AV's fix. **1:** a bounce at the AV. The
   signal to the AV bounces off a glass tower; the base, in the open, gets
   its signal straight. **2:** no sky. Under a tunnel roof no satellite is
   in view, so there is no fix, with or without RTK. **3:** far from the
   base. Beyond 10 to 20 km, the two signals cross different patches of
   atmosphere, so their delays (delay 1 and delay 2) differ. **Rust** marks
   an error.

1. **A bounce at the AV.** A bounce lengthens the AV's path to the
   satellite. Bounces come from structures by the antenna (ESA Navipedia,
   Multipath). The base, in the open, has no bounce, so its correction holds
   none to subtract.
2. **No sky.** No satellites, no fix: RTK stops like plain GNSS.
3. **Far from the base.** The atmosphere delays each signal. RTK is used up
   to 10 or 20 km from the base (ESA Navipedia): farther away, the two
   delays differ (Gillins et al., 2019).

.. important::

   So the AV keeps GNSS and adds a second source beside it: one that keeps
   working without satellites (**2**), and that, compared with GNSS, shows
   when a fix is wrong (**1**).


.. _l6-lec-dr:

Dead Reckoning
--------------

- **Where we are:** GNSS stops between tall buildings, RTK too.
- **In this section:** dead reckoning, the pose from the AV's own speed and
  turn rate.
- **What it is for:** a position while GNSS is out, and the step that moves
  the pose forward between readings in the EKF and in MCL, later today.

.. admonition:: Definition: dead reckoning (DR)
   :class: note

   "A method for determining the estimated position of a vessel by advancing
   from a known fix of position along the vessel's ordered course and speed"
   (National Geospatial-Intelligence Agency, 2019, *The American Practical
   Navigator*). For the AV: start from a known pose, then add up how far it
   drove (wheel speed) and how much it turned (gyro).


.. _l6-lec-dr-step:

One Dead-Reckoning Step: Move Along the Heading, Then Turn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/dr_step.png
   :alt: A top view of one dead-reckoning step. The AV at its position, labeled now: (x, y, theta), faces about 30 degrees above a dashed line to the right; an orange arc from that line marks theta. A solid green line labeled v delta t runs from the AV along its heading to a second AV, labeled after delta t. Two dashed green arrows split that move: one to the right, labeled x plus-equals v cos theta delta t, then one up, labeled y plus-equals v sin theta delta t. The second AV is turned further left; an orange arrow from a gray dashed line along the old heading, labeled theta plus-equals omega delta t, shows the turn. A gray note says one step, drawn far longer than 0.05 s.
   :width: 80%
   :align: center

   One step, drawn far longer than 0.05 s so it shows. **Green:** the move,
   :math:`v\,\Delta t` along the heading, split into its :math:`x` and
   :math:`y` parts (dashed). **Orange:** the heading :math:`\theta` and the
   turn :math:`\omega\,\Delta t`.

The wheels measure the speed :math:`v`. The gyro measures the turn rate
:math:`\omega`, in rad/s. Every :math:`\Delta t` seconds (0.05 s on our
drive), the AV moves :math:`v\,\Delta t` meters in the direction it faces.
Split along the map's axes, that is :math:`v\cos\theta\,\Delta t` along
:math:`x` (east) and :math:`v\sin\theta\,\Delta t` along :math:`y` (north).
Then it turns by :math:`\omega\,\Delta t`. Each step adds each right side to
its left side:

.. math::

   x \mathrel{+}= v\cos\theta\,\Delta t, \qquad
   y \mathrel{+}= v\sin\theta\,\Delta t, \qquad
   \theta \mathrel{+}= \omega\,\Delta t


.. _l6-lec-heading:

A Heading Error Grows with Every Meter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In dead reckoning, the heading is the starting heading plus every turn the
gyro reported, so the gyro's small errors add up. On our drive the heading
was :math:`6.0^\circ` off by the end of the outage (measured). Say it is
:math:`1^\circ` off and the AV drives straight. How far sideways is it after
100 m?

1. :math:`1^\circ = 0.01745` rad, and :math:`\sin 1^\circ = 0.01745`.
2. Sideways error after a distance :math:`d` :math:`= d \sin(\text{heading
   error}) = 100 \times 0.01745 = 1.75` m.
3. To stay under the 0.29 m bound: :math:`0.29 / 0.01745 = 16.6` m of
   driving.

.. figure:: /_static/images/L6/heading_error.png
   :alt: A graph of sideways error in meters against distance driven, 0 to 200 meters. Three straight rust lines from the origin for heading errors of 0.5 degrees (dotted), 1 degree (solid) and 2 degrees (dashed), reaching about 1.75, 3.5 and 7 meters at 200 meters. A dot on the 1 degree line at 100 meters, labeled 100 m at 1 degree: 1.75 m. A red horizontal line at 0.29 meters is labeled 0.29 m bound, Reid et al. A red dot where the 1 degree line meets the bound, at 16.6 meters, labeled 16.6 m at 1 degree: the 0.29 m is used up.
   :width: 70%
   :align: center

   Sideways error against distance driven, for heading errors of
   :math:`0.5^\circ` (dotted), :math:`1^\circ` (solid) and :math:`2^\circ`
   (dashed). On the :math:`1^\circ` line: 1.75 m after 100 m, and the 0.29 m
   used up after 16.6 m. The **red line** is the 0.29 m bound (Reid et al.).


.. _l6-lec-bias:

A Gyro Bias Makes the Heading Error Itself Grow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On the last slide the heading was off by a fixed :math:`1^\circ`, and the
sideways error grew with every meter. Now the gyro itself is biased. The AV
drives straight at :math:`v = 10` m/s (chosen). Its gyro reports
:math:`b = 0.001` rad/s of turning that is not there (our chosen bias).

1. The heading error grows with time: every second, the heading picks up
   another 0.001 rad, so after :math:`t` seconds the heading error is
   :math:`b\,t`. After 30 s it is 0.03 rad, :math:`1.7^\circ`.
2. The AV drifts sideways at :math:`v\,b\,t` (:math:`v` times the heading
   error). At 10 m/s, that is 0 at the last fix and 0.3 m/s after 30 s.
   Plotted against time, this sideways speed is a straight line from 0.
3. The distance is the area under that line, a triangle:

   .. math::

      \tfrac12 \times t \times v\,b\,t = \frac{v\,b\,t^2}{2}
      = \frac{10 \times 0.001 \times 30^2}{2} = 4.5 \text{ m after 30 s}

A program that steps every 0.05 s gets 4.54 m. After 60 s it gets 18.08 m:
**twice the time, four times the error**, because :math:`t` is squared.

.. figure:: /_static/images/L6/bias_growth.png
   :alt: A graph of sideways error in meters against time since the last fix, 0 to 60 seconds. A rust curve, integrated step by step for the AV driving straight with a biased gyro, bends upward and reaches 0.52 meters at 10 seconds, 4.54 at 30 and 18.08 at 60. A dotted black curve, v b t squared over 2, lies on top of it.
   :width: 70%
   :align: center

   Sideways error against time since the last fix. The **rust curve** is
   integrated step by step: 0.52 m at 10 s, 4.54 m at 30 s, 18.08 m at
   60 s. The **dotted curve**, :math:`v\,b\,t^2/2`, lies on top of it.

So a fixed heading error grows with distance, and a gyro bias grows with the
square of time. That is why dead reckoning only bridges short gaps. Next:
what it does on our drive, 400 m without GNSS.


.. _l6-lec-dr-drive:

Dead Reckoning on Our Drive: 400 m Without GNSS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/dr_drift.png
   :alt: Left: a top view of the outage part of the route, the truth in black and dead reckoning in rust, starting together at a dot labeled last fix at the top. The rust path slowly turns away from the black one, crossing it in places, and ends a few meters off. Right: position error in meters against distance since the last fix, 0 to 400 meters; it rises to about 2.7 meters by 100 meters, bumps to about 4.7 meters near 180 meters, dips, then climbs to a peak near 9.0 meters at about 330 meters and ends near 7.8.
   :width: 95%
   :align: center

   **Left:** the road from above, the truth in black and dead reckoning in
   rust, both starting at the last fix (top). **Right:** not a map, but the
   position error against the distance driven since the last fix.

Dead reckoning starts from the **true** pose at the last fix and uses only
the wheels and the gyro. **Measured:** 2.69 m after 100 m, worst 9.03 m at
329 m.

**Corners.** CARLA's own gyro reads a little more turning than the AV makes
in a turn. So most of the :math:`6.0^\circ` heading error comes at the
corners (measured), and the next straight drifts faster. After a corner, the
old sideways error points along the new road, so the two paths can cross.


.. _l6-lec-handson-dr:

Hands-On, Part 2: Dead Reckoning on Our Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This part runs dead reckoning with the wheels and the gyro only, in the
course's Python repo, folder ``lecture6``. The commands are in Part 2 of
:doc:`the Code page <l6_code>` and in the folder's
`README <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture6>`__.

.. admonition:: What to look at
   :class: hint

   1. The window has a tick box for each error we chose: **gyro bias** and
      **wheels 0.5 % fast**. With both ticked, watch the heading error
      (bottom right). Where does it step up: on the straights or at the
      corners?
   2. Untick **gyro bias**. How much smaller is the worst position error?
      Tick it again and untick **wheels 0.5 % fast**. Which error matters
      more?
   3. Untick both. The heading still ends off. What is left in the signals?

Dead reckoning steers nothing here: CARLA drove the AV while the sensors
were recorded (:ref:`l6-lec-drive`), and dead reckoning runs afterward, on
the recording.


.. _l6-lec-dr-summary:

Where Dead Reckoning Leaves Us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Summary: dead reckoning
   :class: tip

   - **A way to localize without satellites:** from the last known pose, add
     up the wheels' speed and the gyro's turn rate. Smooth, 20 times a
     second.
   - **Nothing corrects its errors.** A heading error grows the sideways
     error with every meter (:math:`1^\circ`: 1.75 m after 100 m); a gyro
     bias makes it grow with time squared; on our drive, each corner added
     heading error.
   - **On our drive:** 2.69 m after 100 m and 9.03 m at worst, 31 times the
     0.29 m bound (:math:`9.03 / 0.29 = 31`).
   - **So:** good for a short gap (16.6 m at :math:`1^\circ`), never alone
     for long.

**Next:** keep dead reckoning between fixes, and let each GNSS fix pull it
back: an extended Kalman filter (EKF).


.. _l6-lec-ekf:

Fusion in the EKF
-----------------

- **Where we are:** dead reckoning drifts; GNSS does not drift but can stop.
- **In this section:** GNSS and dead reckoning together in an extended
  Kalman filter (EKF), on our drive and through its GNSS outage.
- **What it is for:** a pose that is smooth between fixes, and pulled back
  when a fix arrives.

.. list-table::
   :widths: 24 34 42
   :header-rows: 1
   :class: compact-table

   * - **Source**
     - **Good at**
     - **Bad at**
   * - GNSS
     - where the AV is: each fix is measured anew, so its error does not grow
     - each fix is meters off (noise, bias); no fix between tall buildings
   * - Wheels and gyro
     - how the AV moved since the last step, 20 times a second, with no jumps
       and no satellites
     - errors add up: the position error grows with distance and time


.. _l6-lec-ekf-loop:

The EKF Loop, with Our Sensors in It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Kalman filter keeps a **state**, its best guess of :math:`x`, :math:`y`,
:math:`\theta` and the speed :math:`v`, and a **covariance** :math:`P`, a
:math:`4 \times 4` matrix. Its diagonal holds :math:`\sigma_x^2`,
:math:`\sigma_y^2`, :math:`\sigma_\theta^2` and :math:`\sigma_v^2`.
:math:`\sigma_x` (one standard deviation, :math:`1\sigma`) is the error in
:math:`x` the filter expects. A larger :math:`P` means the filter is less
sure.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Predict** (every 0.05 s)
     - **Update** (when a reading arrives)
   * - Move the state with the dead-reckoning rule of the last section,
       using the gyro's :math:`\omega` and the state's :math:`v`. :math:`P`
       **grows**: the filter is less sure after every step it cannot check.
     - Compare the reading with what the state predicts: the difference is
       the **innovation**. Move the state by a fraction :math:`K` of it.
       :math:`K` is near 1 when :math:`P` is large next to the reading's
       noise, and near 0 when :math:`P` is small. :math:`P` **shrinks**.
       The wheels give a reading of :math:`v` every 0.05 s. GNSS gives
       :math:`x` and :math:`y` once a second.

**Extended:** the predict rule uses :math:`\cos\theta` and
:math:`\sin\theta`, which are not linear. At each step the EKF replaces them
with a linear fit around the current state, so the Kalman filter's equations
still apply.


.. _l6-lec-ekf-outage:

The Fused Filter in the Outage: Its Error, and Its Own 1σ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our drive has a **GNSS outage**: no fix from 34.2 s to 89.0 s, the 400 m
that dead reckoning drove alone in the last section. Here is one run of the
filter over the whole drive, fusing GNSS, the wheels and the gyro.

.. figure:: /_static/images/L6/ekf_run_nomap.png
   :alt: A graph of meters against time, 0 to 125 seconds, the outage from 34 to 89 seconds shaded pink, titled GNSS plus wheels plus gyro. The blue position error stays near 1 to 3 meters, climbs in the outage to peaks near 9 and 9.5 meters, and drops to under 1 meter at the first fix; the grey band of the filter's own 1 sigma grows in the outage only to about 4 meters.
   :width: 70%
   :align: center

   GNSS, wheels and gyro. **Pink:** the outage. **Blue:** the filter's
   position error against the truth. **Gray:** the error the filter
   expects, its :math:`1\sigma`, :math:`\sqrt{\sigma_x^2 + \sigma_y^2}`
   from :math:`P`.

- In the outage no fix arrives: the filter has only the wheels and the gyro.
- Its error grows to 9.50 m while it expects 3.93 m (its :math:`1\sigma`).
- The real error is **2.4 times** larger (:math:`9.50 / 3.93 = 2.4`) and
  stays above the gray band the whole outage.
- One second after the first fix, the error is 0.60 m.


.. _l6-lec-ekf-map:

The Fused Filter with Map Matching: Its Error, and Its Own 1σ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same drive and the same outage, a second run of the filter. This run
adds map matching, the subject of the next section (:ref:`l6-lec-map`).

.. figure:: /_static/images/L6/ekf_run_map.png
   :alt: A graph of meters against time, 0 to 125 seconds, the outage shaded pink, titled GNSS plus wheels plus gyro plus map matching. The green error starts near 2.5 meters for the first few seconds, then stays mostly under 0.5 meters with short bumps to about 1 meter, outage or not; the grey band stays near 0.2 meters.
   :width: 70%
   :align: center

   GNSS, wheels, gyro and map matching (note the smaller scale). **Pink:**
   the outage. **Green:** the filter's position error against the truth.
   **Gray:** its :math:`1\sigma`, as in the last figure.

- Each LiDAR scan, matched to the map, corrects the pose, outage or not.
- The worst error in the outage is 1.06 m while the filter expects 0.22 m.
- At those bumps, the real error is **4.8 times** larger
  (:math:`1.06 / 0.22 = 4.8`).


.. _l6-lec-ape:

One Number for a Whole Run: the Absolute Pose Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To compare runs of the filter, each run needs one number for its whole
error.

.. admonition:: Definition: absolute pose error, APE (position part)
   :class: note

   At each time step :math:`k`, the distance :math:`e_k` from the estimated
   position to the true one. A run of :math:`N` steps is summarized by the
   RMSE (root mean square error) of those distances. Sturm et al. (2012)
   call it ATE:

   .. math::

      \mathrm{APE}_{\mathrm{RMSE}} = \sqrt{\frac{1}{N}\sum_{k=1}^{N} e_k^2}

- A **step** :math:`k` (:math:`k = 1, \dots, N`) is one moment where the
  filter gives a pose, every 0.05 s.
- A **run** is one pass of the filter over a drive, from start to end,
  :math:`N` steps long. Our drive has 2,513 steps. The filter starts 3 to 4 s
  in, once GNSS gives it a first pose, so a run has :math:`N = 2{,}433` or
  :math:`2{,}453`.
- An **error**, :math:`e_k`, is how far the filter's position is from the
  true position at step :math:`k`, in meters.

The name reads the formula from the outside in: the **root** of the
**mean** of the **squared** errors. The next part builds it from the inside
out.

.. tip::

   See :ref:`l6-app-ape` in :doc:`Going Further <l6_appendix>`.


.. _l6-lec-rmse:

The RMSE, One Piece at a Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \mathrm{APE}_{\mathrm{RMSE}} = \sqrt{\frac{1}{N}\sum_{k=1}^{N} e_k^2}

The example run (made up, not measured): :math:`N = 4` steps with errors 0.3,
0.4, 1.2 and 0.5 m.

1. :math:`e_k^2`, **square each error**, so a big error counts much more
   than a small one: 0.09, 0.16, 1.44, 0.25. The 1.2 m error is 4 times the
   0.3 m one; its square is :math:`1.44 / 0.09 = 16` times.
2. :math:`\sum_{k=1}^{N}`, **add them up**: one number for the whole run,
   1.94 m\ :sup:`2`.
3. :math:`\frac{1}{N}`, **divide by the number of steps**. The sum grows
   with every step, so a long run would score worse just for being long.
   This gives the average squared error per step:
   :math:`1.94 / 4 = 0.485` m\ :sup:`2`. It is not a distance yet: m\ :sup:`2`
   only says the errors were squared.
4. :math:`\sqrt{\ }`, **take the root** to get back to meters:
   :math:`\sqrt{0.485} = 0.70` m.

**Reading 0.70 m:** over the run, the filter is typically about 0.70 m from
the true position, with the large errors weighing more. The plain average of
the four errors is lower: :math:`(0.3 + 0.4 + 1.2 + 0.5) / 4 = 2.4 / 4 =
0.60` m. The RMSE is higher because squaring made the 1.2 m error count
more. The run fails the 0.29 m bound, which is a maximum: one step is 1.2 m
off.


.. _l6-lec-ape-switches:

Eight Runs of the Filter: Three Switches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every run is the same EKF, fusing the gyro with whatever the switches turn
on. We run it eight times, once for each setting of three switches
(:math:`2 \times 2 \times 2 = 8`). In the figure below, each switch has its
own place: the panel, the bar group or the bar color.

- **GNSS** (panel): a fix every second (left), or the same with no fix for
  400 m (right).
- **Wheel speed** (group): read, the filter updates its speed :math:`v` from
  the wheels every 0.05 s. Not read, it keeps :math:`v` from the last step,
  and only a GNSS fix or a map match corrects it.
- **Map matching** (color): blue without, green with.

Each run gets one APE RMSE, over its :math:`N = 2{,}433` (GNSS always) or
:math:`2{,}453` (outage) steps: its score in the figure below.


.. _l6-lec-ape-runs:

Eight Runs, One Score Each
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/ape_bars.png
   :alt: Two panels of bars, APE RMSE in meters from 0 to 6, with a red dashed line at the 0.29 m bound. Blue bars: no map matching; green bars: with map matching. Left, GNSS always: wheel speed read, 1.28 blue and 0.47 green; wheel speed not read, 1.97 blue and 1.38 green. Right, GNSS outage of 400 m: wheel speed read, 4.99 blue and 0.52 green; wheel speed not read, 4.58 blue, and a green bar that reaches the top of the axis, with a break mark of two slanted lines across it and the value 27.66 printed above it.
   :width: 90%
   :align: center

   APE RMSE of the eight runs. **Left panel:** GNSS always. **Right
   panel:** GNSS outage, 400 m. **Blue:** no map matching. **Green:** with
   map matching. The **red dashed line** is the 0.29 m bound.

Each bar is one run's APE RMSE.

- **With wheel speed read, the map lowers APE most:** 4.99 m to 0.52 m
  through the outage.
- **One run gets lost:** outage, wheel speed not read, map matching
  (27.66 m). Its bar is broken by the two slanted lines because 27.66 m does
  not fit on the 6 m axis. Its story is in :ref:`l6-lec-failed-run`.
- **No run meets the 0.29 m bound:** the best is 0.47 m
  (:ref:`why <l6-lec-why-bound>`).


.. _l6-lec-ape-always:

Eight Runs: the Four with GNSS Always
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/ape_bars_always.png
   :alt: A bar chart titled GNSS always, APE RMSE in meters from 0 to 6, with a red dashed line at 0.29 m, the bound. Wheel speed read: bar 1, blue, no map matching, 1.28; bar 2, green, with map matching, 0.47. Wheel speed not read: bar 3, blue, 1.97; bar 4, green, 1.38. Each bar has a black numbered tag above its value. A legend: blue no map matching, green with map matching, red dashed 0.29 m bound.
   :width: 55%
   :align: center

   The four runs with GNSS always. Tags **1** to **4** number the runs, as
   in the list below. **Blue:** no map matching. **Green:** with map
   matching. The **red dashed line** is the 0.29 m bound.

A GNSS fix every second in all four runs.

1. **Wheel speed, no map: 1.28 m.** The wheels and the gyro carry the pose
   between fixes.
2. **Wheel speed, map: 0.47 m.** Plus a map match about once a second: the
   best of the eight runs.
3. **No wheel speed, no map: 1.97 m.** Only GNSS corrects the speed:
   :math:`1.97 - 1.28 = 0.69` m worse than run 1.
4. **No wheel speed, map: 1.38 m.** The map helps
   (:math:`1.97 - 1.38 = 0.59` m less than run 3), but less than with wheel
   speed; 5 map matches were rejected as too far from the prediction.


.. _l6-lec-ape-outage:

Eight Runs: the Four with a GNSS Outage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/ape_bars_outage.png
   :alt: A bar chart titled GNSS outage, 400 m, APE RMSE in meters from 0 to 6, with a red dashed line at 0.29 m, the bound. Wheel speed read: bar 1, blue, no map matching, 4.99; bar 2, green, with map matching, 0.52. Wheel speed not read: bar 3, blue, 4.58; bar 4, green, reaching the top of the axis with a break mark of two slanted lines, labeled 27.66. Each bar has a black numbered tag above its value. A legend: blue no map matching, green with map matching, red dashed 0.29 m bound.
   :width: 55%
   :align: center

   The four runs with a GNSS outage. Tags **1** to **4** number the runs, as
   in the list below. **Blue:** no map matching. **Green:** with map
   matching. Bar **4** is broken because 27.66 m does not fit on the 6 m
   axis.

No GNSS fix for 400 m (34.2 to 89.0 s) in all four runs.

1. **Wheel speed, no map: 4.99 m.** In the outage only the wheels and the
   gyro move the pose: dead reckoning drifts until GNSS returns.
2. **Wheel speed, map: 0.52 m.** Map matching takes over from GNSS: almost
   as good as with GNSS always (0.47 m).
3. **No wheel speed, no map: 4.58 m.** Nothing measures the speed in the
   outage. It ends close to run 1 (:math:`4.99 - 4.58 = 0.41` m apart):
   without GNSS or a map, neither run can correct its drift.
4. **No wheel speed, map: 27.66 m.** Map matching loses the AV and does not
   find it again until GNSS returns: :ref:`l6-lec-failed-run`.


.. _l6-lec-why-bound:

Why the Best Run Misses the 0.29 m Bound
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our best run (GNSS always, wheel speed read, map matching) scores 0.47 m. It
misses the 0.29 m bound for two reasons.

**It starts meters off.** The filter starts at 4.05 s from a GNSS fix, and
GNSS is meters off. Map matching needs a good first guess of the pose (next
section), so the filter skips it until its own :math:`\sigma` is small
enough: the first match comes at 8.0 s. Until then the error is 0.6 to
2.4 m; right after the match, 0.15 m. Scored only from 8.0 s on, the run
gets 0.38 m: still above the bound.

**It drifts between map matches.** A map match comes about once a second
and brings the pose to about 0.2 m from the truth. In the second until the
next match, the pose drifts again, most in turns. So even in the good part
of the run, the error moves up and down around the bound.

The bound is a limit for every step, not an average. In this run, about one
step in three is above 0.29 m.

.. important::

   To meet the bound, the error must stay under 0.29 m at every step, and a
   map match alone already leaves the filter about 0.2 m off.


.. _l6-lec-handson1:

Hands-On, Part 3: the Fused Filter on Our Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This part shows the fused filter's eight runs, in the course's Python repo,
folder ``lecture6``. The commands are in Part 3 of :doc:`the Code page
<l6_code>` and in the folder's
`README <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture6>`__.

.. admonition:: What to look at
   :class: hint

   1. Tick and untick **GNSS outage**, **wheels** and **map matching**. Each
      combination is one run of the filter, computed in advance as a
      results file.
   2. Watch two things: the **error** (blue) and the filter's **own**
      :math:`1\sigma` (the shaded band). In the outage, does the band grow
      as fast as the error?
   3. Note the APE of each run. Which input lowers it most?


.. _l6-lec-map:

Against a Map
-------------

- **In this section:** finding the pose by matching what the LiDAR sees to a
  map: MCL (Monte Carlo localization), then ICP (iterative closest point).
- **What it is for:** a position that does not drift and keeps working when
  the GNSS signal is lost.

The fused filter still drifts when GNSS stops.

**The idea.** The map stores where the walls, poles and curbs are, in the map
frame. The LiDAR sees some of them, in the vehicle frame. **In most places,
only one pose puts the scan on top of the map.** Find it, and you have the
AV's pose.


.. _l6-lec-mcl:

Monte Carlo Localization
~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Monte Carlo localization (MCL)
   :class: note

   A localization method that keeps its belief of where the robot is as "a
   set of :math:`N` weighted, random samples or particles" (Fox et al.,
   1999). For the AV: **each particle is one guess of the pose**
   :math:`(x, y, \theta)`, and its weight says how well the scan,
   transformed to the map frame with that guess, fits the map.

MCL repeats three steps: 1. predict, 2. weigh, 3. resample.


.. _l6-lec-mcl-predict:

1. Predict
~~~~~~~~~~

Move every particle by what the wheels and the gyro measured, plus a little
random noise, because those sensors are not exact.

.. figure:: /_static/images/L6/mcl_idea_predict.png
   :alt: A close view of one lane with a faint grey car facing right: about fifty short green arrows, the particles, spread around the car, all pointing roughly right. A 1 m scale bar.
   :width: 70%
   :align: center

   **Predict.** 50 particles (placed for this example), green arrows, spread
   around the true pose (faint car), which MCL does not know.


.. _l6-lec-mcl-weigh:

2. Weigh
~~~~~~~~

Give every particle a weight: place the scan as if the AV stood at that
particle's pose, and score how well the scan points land on the map.

.. figure:: /_static/images/L6/mcl_idea_weigh.png
   :alt: The whole street with blue map squares: a building front with two doorways at the top, three poles, and a building corner at the bottom. In the lower lane, a rust car and, 2 m behind it and turned slightly left, a grey car. Rust dots, the rust car's scan, lie on the map squares. Grey open circles, the grey car's scan, lie off the walls, shifted and tilted. A 5 m scale bar.
   :width: 60%
   :align: center

   **Weigh.** Each car is one particle, drawn with its scan. Square points
   (blue): the map. Rust points: the heaviest particle, 0.42 m from the true
   pose; its scan lands on the map. Gray points: a particle 2.0 m behind the
   true pose, turned :math:`4.7^\circ`; its scan lands off the map, and its
   weight is :math:`6.6 \times 10^{-17}` of the rust one's.


.. _l6-lec-mcl-transform:

2. Weigh: One Real Scan, Transformed with Each Particle's Pose
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The LiDAR takes **one** scan, from where the AV really is. It stores each
point as a position relative to the AV, :math:`(p_x, p_y)`: :math:`p_x`
forward, :math:`p_y` left.

MCL takes no new scan for a particle and predicts none. It asks: **if the AV
stood at this particle's pose** :math:`(x, y, \theta)`, where would these
points be on the map? It **transforms** them to the map frame with that pose:
turn by :math:`\theta`, then shift by :math:`(x, y)`:

.. math::

   x_\text{map} = x + p_x \cos\theta - p_y \sin\theta, \qquad
   y_\text{map} = y + p_x \sin\theta + p_y \cos\theta

**Example (chosen):** one scan point 10 m straight ahead,
:math:`(p_x, p_y) = (10, 0)`.

1. Particle A at :math:`(5, 2)`, :math:`\theta = 0^\circ`: the point lands at
   :math:`(5 + 10,\ 2) = (15, 2)`.
2. Particle B at :math:`(5, 2)`, :math:`\theta = 90^\circ`: the point lands
   at :math:`(5,\ 2 + 10) = (5, 12)`.

The same scan lands in a different place for each particle. Only a particle
near the true pose puts the points on the walls. :ref:`l6-lec-mcl-score`
gives the score.


.. _l6-lec-mcl-resample:

3. Resample
~~~~~~~~~~~

Draw a new set of particles from the old ones: heavy particles are copied,
often several times, and light ones are dropped.

.. figure:: /_static/images/L6/mcl_idea_resample.png
   :alt: The same close view as the Predict figure: eight green arrows of different widths near the middle of the faint car.
   :width: 70%
   :align: center

   **Resample.** All 50 new particles are copies of 8 old ones. A wider arrow
   means more copies; the widest has 19. The particles now gather near the
   true pose (faint car).


.. _l6-lec-mcl-eq:

MCL, Written Out: the Steps as Equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`N` particles :math:`\mathbf{x}^{(i)} = (x, y, \theta)`,
:math:`i = 1, \dots, N`, each with a weight :math:`w^{(i)}` (Dellaert et al.,
1999). Our code, ``mcl.py``:

1. **Start:** :math:`N = 2000` particles, spread evenly inside a circle of
   radius 20 m (chosen) around the first GNSS fix. Each heading
   :math:`\theta` is drawn evenly from :math:`-180^\circ` to
   :math:`180^\circ`: one fix gives a position but no heading, so the start
   assumes nothing about which way the AV faces. Every weight is
   :math:`w^{(i)} = 1/N`: no scan has been compared yet, so no particle is
   more likely than another.
2. **Predict:** one dead-reckoning step per particle, each with its own noise
   on the speed and the turn rate (next subsection).
3. **Weigh:**
   :math:`w^{(i)} \leftarrow w^{(i)}\, p(\mathbf{z} \mid \mathbf{x}^{(i)}, m)`:
   the scan :math:`\mathbf{z}` placed at the particle's pose, scored against
   the map :math:`m` (60 scan points, each with the likelihood field).
4. **Normalize:** :math:`w^{(i)} \leftarrow w^{(i)} / \sum_j w^{(j)}`.
5. **Estimate:** :math:`\hat{\mathbf{x}} = \sum_i w^{(i)}\, \mathbf{x}^{(i)}`
   (the heading averaged as an angle).
6. **Resample** when
   :math:`N_\text{eff} = 1 / \sum_i \big(w^{(i)}\big)^2 < N/2`, then
   :math:`w^{(i)} = 1/N`. :math:`N_\text{eff}`, the **effective number of
   particles**, counts how many particles really carry the weight: :math:`N`
   when all weights are equal, 1 when one particle has it all.


.. _l6-lec-mcl-spread:

Predict
~~~~~~~

.. figure:: /_static/images/L6/mcl_predict_spread.png
   :alt: A top view of a straight stretch of the route, x east from 52 to 87 meters, y north near minus 25 meters. A black dot labeled start, 8 s into the drive, and the black true path running east. Three green clouds of particles along the path: a small oval labeled 1 s later (9 s): spread 0.33 m, a round cloud labeled 3 s later (11 s): spread 0.79 m, and a larger cloud labeled 5 s later (13 s): spread 1.26 m. Each cloud holds the same 2000 particles; 25 of them carry a dark green arrow for their heading, all pointing east.
   :width: 95%
   :align: center

   Predict alone, no scans: the same 2000 particles 1, 3 and 5 s after the
   start (black dot). Arrows: the headings of 25 particles.

**Chosen:** all 2000 particles start on the AV's true pose, 8 s into the
drive (black dot). Then predict runs alone, with no scans. Each step moves
every particle by the wheels' speed and the gyro's turn rate, plus its own
noise (:math:`\sigma_v = 0.3\ \text{m}/\sqrt{\text{s}}`,
:math:`\sigma_\omega = 0.03\ \text{rad}/\sqrt{\text{s}}`). The arrows show
the headings of 25 particles.

The figure shows the same particles 1, 3 and 5 s later. Their **spread**,
the root mean square distance from the cloud's own center, grows: 0.33,
0.79, 1.26 m. With no scan, MCL grows less sure at every step. The next scan
shrinks the spread.


.. _l6-lec-mcl-score:

Weigh: Scoring One Scan Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**When:** at each scan, every 0.5 s; predict runs in between. (The Predict
example above used no scans, to show predict alone.)

**Where** :math:`d` **comes from:** for one particle, transform the scan to
the map frame with its pose. For each scan point, :math:`d` is its distance
to the nearest map point; the code computes it. The map was made before,
from scans of the same route stitched at their true poses. MCL uses no
ground truth.

**The score** :math:`p(d)` says how well one scan point fits the map. If the
point lands on a wall or pole of the map (:math:`d = 0`), it scores 0.93, the
highest. The farther it lands from the nearest one, the lower its score, down
to 0.033 past 3 m. It never reaches 0.

.. list-table::
   :widths: 40 12 12 12 12 12
   :header-rows: 1
   :class: compact-table

   * - :math:`d`, distance to the nearest map point
     - 0
     - 0.5 m
     - 1 m
     - 2 m
     - over 3 m
   * - :math:`p(d)`, the point's score
     - 0.93
     - 0.83
     - 0.58
     - 0.16
     - 0.033


.. _l6-lec-mcl-formula:

Weigh: the Score's Formula
~~~~~~~~~~~~~~~~~~~~~~~~~~

The scores above come from the **likelihood field**, adapted from Thrun et
al. (2005, Sec. 6.4):

.. math::

   p(d) = z_\text{hit}\, e^{-d^2/(2\sigma^2)} + z_\text{rand}/d_\text{max}

.. list-table::
   :widths: 16 64 20
   :header-rows: 1
   :class: compact-table

   * - **Symbol**
     - **What it is**
     - **Ours (chosen)**
   * - :math:`p(d)`
     - the score of one scan point: how well it fits the map
     -
   * - :math:`d`
     - the distance from the scan point, placed in the map, to the nearest
       map point
     -
   * - :math:`z_\text{hit}`
     - the weight of the first term, the bell curve: the score at
       :math:`d = 0` comes mostly from it
     - 0.9
   * - :math:`\sigma`
     - the width of the bell: how fast the score falls as :math:`d` grows
     - 1.0 m
   * - :math:`z_\text{rand}`
     - the weight of the second term, the floor: the share kept for points
       that hit something the map lacks
     - 0.1
   * - :math:`d_\text{max}`
     - how far the code looks for a map point; past it, the first term is 0
     - 3 m

With our values: :math:`p(d) = 0.9\, e^{-d^2/2} + 0.1/3`. The next subsection
says why we chose these values.


.. _l6-lec-mcl-values:

Weigh: Why These Values
~~~~~~~~~~~~~~~~~~~~~~~

- **A wide** :math:`\sigma`\ **, 1.0 m:** with 2000 particles over a whole
  street, the one nearest the truth is often a meter or a few degrees off. A
  narrow bell would score it like a wrong one.
- **A floor,** :math:`z_\text{rand}/d_\text{max} = 0.1/3 = 0.033`\ **:** a
  point that hits something the map lacks, a parked car say, still scores
  0.033, so one such point cannot zero a good particle. Thrun et al. divide
  :math:`z_\text{rand}` by the sensor's maximum range; our code divides by
  :math:`d_\text{max}`.
- **60 points per scan:** neighboring beams are not independent, and
  multiplying hundreds of their scores makes one particle take all the weight
  after one scan.

.. tip::

   The field drawn around a corner: see :ref:`l6-app-lf` in Going Further.


.. _l6-lec-mcl-weigh-example:

Weigh Three Particles, Then Normalize
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/mcl_weigh_example.png
   :alt: Three panels, particle A, B and C, each with a green wall along the bottom labeled map: a wall and three rust scan points above it. A: the points are 0.1, 0.2 and 0.1 meters from the wall, scores 0.929, 0.916 and 0.929. B: 1.0, 1.3 and 0.9 meters, scores 0.579, 0.420 and 0.634. C: 2.0, 3.5 and 2.5 meters, scores 0.155, 0.033 and 0.073.
   :width: 95%
   :align: center

   Three particles, three scan points each, a wall as the map. Each point is
   labeled with its distance :math:`d` and its score :math:`p`. Distances
   chosen.

Each scan point :math:`d` meters from the map scores
:math:`p(d) = 0.9\,e^{-d^2/2} + 0.1/3` (:ref:`l6-lec-mcl-formula`), and only
:math:`0.1/3 = 0.033` past 3 m (C's 3.5 m point). The distances are chosen;
all three particles start with equal weights.

1. Multiply each particle's scores: A = 0.790, B = 0.154, C = 0.0004.
2. Divide by their sum, 0.944: weights A = 0.836, B = 0.163, C = 0.0004.


.. _l6-lec-mcl-neff:

Resample: When?
~~~~~~~~~~~~~~~

**The question:** resampling copies some particles and drops others, so
afterward there are fewer different guesses. When the weights are nearly
equal, no particle fits the map better than the others. Resampling would
then drop guesses almost at random, and the cloud would get no closer to the
AV. So MCL first asks how many particles really carry the weight.

.. admonition:: Definition: effective number of particles
   :class: note

   .. math::

      N_\text{eff} = \frac{1}{\sum_i w_i^2}

   - All :math:`N` weights equal, :math:`w_i = 1/N`:
     :math:`\sum_i w_i^2 = N \times 1/N^2 = 1/N`, so :math:`N_\text{eff} = N`.
   - One particle has all the weight, :math:`w = 1`:
     :math:`\sum_i w_i^2 = 1`, so :math:`N_\text{eff} = 1`.

**The rule in our code:** resample only when fewer than half of the particles
really carry the weight, that is, when :math:`N_\text{eff} < N/2` (the cutoff
:math:`N/2` is chosen). With our 2000 particles: when :math:`N_\text{eff}`
drops below 1000. After resampling, every particle's weight is :math:`1/N`
again, and the next scan weighs them anew.


.. _l6-lec-mcl-neff-example:

Resample: When? An Example
~~~~~~~~~~~~~~~~~~~~~~~~~~

Take the three particles A, B and C of :ref:`l6-lec-mcl-weigh-example`, with
weights 0.836, 0.163 and 0.0004.

1. :math:`N = 3`, so the cutoff is :math:`N/2 = 3/2 = 1.5`.
2. Square each weight and add them up:
   :math:`\sum_i w_i^2 = 0.836^2 + 0.163^2 + 0.0004^2 = 0.6989 + 0.0266 + 0.0000 = 0.7255`.
3. :math:`N_\text{eff} = 1/0.7255 = 1.38`: about 1.4 of the 3 particles carry
   the weight.
4. 1.38 is under the cutoff 1.5, so MCL resamples.

.. important::

   Most of the weight sits on A (0.836), so the three particles count as
   fewer than two. Resampling then copies A twice, keeps B once and drops C
   (next two subsections).


.. _l6-lec-mcl-how:

Resample: How?
~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/mcl_resample.png
   :alt: A bar from 0 to 1 cut into three segments, one per particle, as wide as its weight: A 0.836 and B 0.163; C, 0.0004, is too thin to see and is marked by a line at the right end. Three rust arrows point down at 0.200, 0.533 and 0.867, labeled N = 3 pointers: first at r/N, then every 1/N. The first two land in A, the third in B.
   :width: 90%
   :align: center

   The weights of A, B and C laid end to end on a bar from 0 to 1, and
   :math:`N = 3` pointers: the first at :math:`r/N`, then one every
   :math:`1/N`.

1. Lay the weights end to end on a bar from 0 to 1, one piece per particle.
2. A **pointer** is a spot on that bar. Draw one random number :math:`r`
   between 0 and 1, the **random start** (here 0.6, chosen). Put :math:`N`
   pointers at :math:`(r + k)/N`, :math:`k = 0, \dots, N-1`. Here
   :math:`r = 0.6` and :math:`N = 3`: :math:`(0.6 + 0)/3 = 0.200`,
   :math:`(0.6 + 1)/3 = 0.533`, :math:`(0.6 + 2)/3 = 0.867`.
3. Copy the particle under each pointer: A twice, B once, C dropped. On
   average a particle gets :math:`N \times` its weight copies: A
   :math:`3 \times 0.836 = 2.51` and B :math:`3 \times 0.163 = 0.49`. The
   random start rounds them to whole copies.

This is **systematic resampling**.


.. _l6-lec-mcl-new:

Resample: the New Particles on the AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The last subsection copied A twice, B once and C not at all. The example
gives no poses, only how far each particle's scan points land from the wall.
Moving a particle away from the wall moves its whole scan the same distance.
So each particle is drawn that far from the true pose (faint car), at the
mean of its three distances: A 0.13 m, B 1.07 m, C 2.67 m.

.. figure:: /_static/images/L6/mcl_resample_cars.png
   :alt: Two top views side by side, titled before resampling and after resampling, each with a faint grey car facing right 2 m above a green wall labeled map: a wall, and a 1 m scale bar. Before: three green arrows of the same width pointing right, A on the car labeled weight 0.836, B just above the car labeled weight 0.163, and C higher up labeled weight 0.0004. After: a wider arrow at A's place labeled A: 2 copies, a thin arrow at B's place labeled B: 1 copy, and no arrow at C's place, labeled C: 0 copies, dropped.
   :width: 95%
   :align: center

   **Left, before resampling:** A, B and C with their weights. **Right, after
   resampling:** A has 2 copies, B 1 copy, and C is dropped.

A's two copies have exactly the same pose, so they lie on top of each other
and look like one arrow: the figure draws it twice as wide. The figure in
:ref:`l6-lec-mcl-resample` draws copies the same way. The next predict step
gives each copy its own noise, so the copies move apart again.


.. _l6-lec-mcl-symmetry:

When Two Places Look the Same, MCL Can Pick the Wrong One
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/mcl_symmetry.png
   :alt: Two top views of a 20 by 10 meter room whose walls are grey lines. In both, the AV is drawn in black near the bottom at x 8.5, y 2, facing right. Panel 1, plain room: a cluster of dark green particles and a light green car, MCL's estimate, sit near the top at x 11.5, y 8, facing left. Panel 2, room with a small square pillar at about x 14.5, y 7.5: the particles and the light green car sit on the black AV.
   :width: 95%
   :align: center

   **1** Plain room: the particles (dark green) and MCL's estimate (light
   green car) sit near the top, facing left, while the AV (black) is near
   the bottom, facing right. **2** Room with a pillar: the particles and the
   estimate sit on the AV.

**The world (chosen):** a closed room, 20 m by 10 m; its walls are the map.
The AV (black) drives 4.5 m to the right and takes 10 scans. MCL starts with
2000 particles anywhere in the room, each heading drawn evenly from
:math:`-180^\circ` to :math:`180^\circ`. The light green car is MCL's
estimate, the particles' weighted average.

- **1, plain room**, only four walls: it looks the same turned half a turn,
  so the scan fits the mirror pose just as well. In this run (chosen), MCL
  picked it: 6.6 m off, facing left.
- **2, room with a pillar:** only the true pose sees the pillar where the map
  has it. MCL lands on the AV, 0.2 m off.


.. _l6-lec-mcl-gnss:

A GNSS Fix Keeps MCL off the Look-Alike Place
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the plain room every scan fits the mirror pose as well as the true one.
So more scans, or new particles placed at random, cannot undo a wrong
choice. MCL needs information from outside the map: a GNSS fix. In these
runs the fix has a random error with :math:`\sigma = 1` m in :math:`x` and in
:math:`y`, and the particles go in a 3 m disk around it (both chosen).

.. list-table::
   :widths: 70 30
   :header-rows: 1
   :class: compact-table

   * - **Run (seeds 0 to 19)**
     - **Ends on the mirror**
   * - Plain room, particles anywhere
     - 9 of 20
   * - Room with a pillar, particles anywhere
     - 0 of 20
   * - Plain room, particles around a GNSS fix
     - 0 of 20
   * - Plain room, the 9 wrong runs restarted around a fix, 10 more scans
     - 0 of 9

A seed fixes one run's random draws. A run ends on a pose when more than
half of the weight lies within 1.5 m of it.

**Spotting a wrong choice:** compare MCL's estimate with the fix. In the 9
wrong runs they were 5.5 to 8.0 m apart, far more than the fix's error. With
the fix about :math:`\sqrt{1^2+1^2} = 1.4` m off, the 3 m disk reaches about
4.4 m from the AV, short of the mirror pose, 6.7 m away.


.. _l6-lec-mcl-drive:

MCL on Our Drive: from a 20 m Circle to the AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/mcl_snapshots.png
   :alt: Three top views of the map in grey around the AV, drawn in black, with dark green particles and a light green car for MCL's estimate. Scan 1 at t 0 seconds, 44 meters wide: 2000 particles fill a circle 40 meters across around a blue cross, the GNSS fix, just below the AV; the estimate is 3.06 meters off. Scan 4 at 1.5 seconds, zoomed in to 16 meters wide: the particles form a short line behind the AV and the estimate is 1.66 meters behind it. Scan 16 at 7.5 seconds, 16 meters wide: the particles and the estimate sit on the AV, 0.02 meters off.
   :width: 95%
   :align: center

   MCL on our drive, three moments. **Scan 1,** :math:`t = 0` s: the
   particles fill a circle 40 m across around the GNSS fix (blue cross); the
   estimate is 3.06 m off. **Scan 4,** :math:`t = 1.5` s: a short line
   behind the AV; 1.66 m off. **Scan 16,** :math:`t = 7.5` s: on the AV,
   0.02 m off.

**The start:** MCL needs a rough idea of where the AV is. At the start of the
drive, GNSS works: we take one fix (blue :math:`+`, 2.05 m from the AV) and
spread 2000 particles within 20 m of it (chosen). Each heading is drawn
evenly from :math:`-180^\circ` to :math:`180^\circ`, because a fix has no
heading.

**After that, MCL uses no GNSS:** the wheels and the gyro move the particles,
and each scan, one every 0.5 s, weighs them against the map.

Gray: the map; dark green: particles; light green car: MCL's estimate. Scans
4 and 16 are zoomed in.

.. tip::

   Hands-on, part 4: run MCL on our drive yourself. The setup and the
   commands are on :doc:`the Code page <l6_code>`.


.. _l6-lec-mcl-count:

How Many Particles: Finding the AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Why compare:** the number of particles is MCL's main cost. Weighing one
scan takes 6 ms with 200 particles and 59 ms with 2000 (measured, our Python
code). What do ten times the particles buy? Five runs of each, from the same
20 m start:

.. figure:: /_static/images/L6/mcl_particle_count_find.png
   :alt: Two graphs side by side, 200 particles and 2000 particles, five runs each, error of MCL's estimate in meters from 0 to 15 against time since the first scan from 0 to 70 seconds, a red dashed line at 0.29 m and a grey dotted line at 2 m. Left: three runs drop below 1 meter within a few seconds; two start near 9 and 14 meters and stay between 5 and 10 meters until about 60 seconds, then drop. Right: two runs drop quickly; three start between 10 and 13 meters and drop below 2 meters at about 14, 15 and 34 seconds.
   :width: 95%
   :align: center

   The error of MCL's estimate during the first 70 s, five runs (seeds 0 to
   4) with 200 particles (left) and with 2000 (right). Red dashed line: the
   0.29 m bound. Gray dotted line: 2 m.

**The 10 m at the start:** the first scan already weighs the particles, and
the weight can land on a wrong place about 10 m away where the scan also
fits. The cloud gathers there: its spread is 0.2 to 0.4 m while it is 10 m
off.

**The result:** with 2000, every run is within 2 m of the AV by 33.5 s. With
200, two runs stay 5 to 10 m off until 60.5 and 64.0 s.


.. _l6-lec-mcl-count-found:

How Many Particles: Once the AV Is Found
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/mcl_particle_count_found.png
   :alt: Two graphs side by side, 200 particles and 2000 particles, five runs each, error of MCL's estimate in meters from 0 to 1.5 against time since the first scan from 70 to 125 seconds, with a red dashed line at 0.29 m. In both, all five lines rise and fall together: peaks near 80, 90, 110 and 122 seconds, up to about 1 meter, and near 0.05 meters between them.
   :width: 95%
   :align: center

   The same runs from 70 s on, 200 particles (left) and 2000 (right). Red
   dashed line: the 0.29 m bound.

- **More particles do not help now.** After 70 s, all ten runs rise and fall
  at the same moments of the drive, to 0.80 to 1.11 m at worst, with 200 or
  2000. The peaks come from the drive, not from the number of particles.
- With 2000, 43 to 53 % of scans after the first 10 s are above the 0.29 m
  bound (red).

So the best number changes during a run: many particles while the AV could
be anywhere, few once they gather on it. **KLD sampling** (KLD stands for
Kullback-Leibler distance) sets the number this way at each step (Fox,
2003).


.. _l6-lec-mcl-lost:

When MCL Loses the AV: Add Random Particles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/mcl_kidnap.png
   :alt: Three top views of the 20 by 10 meter room with a small square pillar near x 14.5, y 7.5. The AV is drawn in black, the particles in dark green, and MCL's estimate as a light green car. Panel 1, just after the AV is moved: the AV is at x 3, y 5; the particles and the estimate are still near x 9, y 2, where the AV was. Panel 2, 10 seconds later with no random particles: the AV is at x 12.5, y 5; the particles and the estimate are near x 17, y 4, about 4.5 meters away. Panel 3, 10 seconds later with 100 random particles per scan: random dots are spread over the room, and the particles and the estimate sit on the AV.
   :width: 100%
   :align: center

   **Panel 1 (left),** just after the AV is moved: the particles and the
   estimate are still where the AV was. **Panel 2 (middle),** 10 s later
   with no random particles: the particles stay away from the AV. **Panel 3
   (right),** 10 s later with 100 random particles per scan: the particles
   and the estimate sit on the AV.

**The problem:** resampling only copies particles MCL already has. If none is
near the AV, MCL stays lost. This is the **kidnapped robot** problem.

**Chosen test:** MCL has found the AV in the room. We move the AV to
:math:`x = 3` m, :math:`y = 5` m without telling MCL, and it drives on for
10 s, 20 scans (panel 1).

**The fix** (next subsection): after each scan, swap some particles for
random poses.

**Measured over 20 runs**, back on the AV after 10 s (over half the weight
within 1.5 m):

- no random particles: **0** of 20 (panel 2);
- 20 per scan: **12** of 20;
- 100 per scan: **17** of 20.


.. _l6-lec-mcl-random-how:

How Random Particles Bring MCL Back to the AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After the move, every particle is near the old pose, where the AV no longer
is. Resampling copies only those, so on its own MCL never reaches the AV.
Random particles add new guesses:

1. After each scan, swap some of the 2000 particles for random poses:
   anywhere in the room, any heading.
2. Sooner or later one lands near the AV, facing about the right way. Its
   scan fits the map, so the next scan gives it a high weight. The old
   cloud's scans do not fit.
3. Resampling copies that particle many times, and the cloud moves to the AV
   (panel 3 of the figure above).

The more random particles per scan, the more chances to land near the AV:
within 10 s, 12 of 20 runs find it with 20 per scan, 17 of 20 with 100.

.. tip::

   Hands-on, part 4: kidnap the AV yourself. The setup and the commands are
   on :doc:`the Code page <l6_code>`.


.. _l6-lec-mcl-random-cost:

Random Particles: Where the Idea Comes From, and Its Cost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **The idea:** after each step, replace a few particles with random poses.
  "The added samples are essential for relocalization in the rare event that
  the robot loses track of its position" (Fox et al., 1999). How many is a
  design choice: the paper says "a small number".
- **The cost:** the authors call such fixes "mathematically questionable";
  they no longer converge to the true answer as :math:`N` grows (Thrun et
  al., 2001).
- **The course code**, ``mcl.py``, adds them only when asked
  (``--random``). Measured on our drive, with a 10 m jump at 40 s and 20
  random particles per scan: 2 of 5 runs never return. Their estimate
  wanders 64 and 101 m off (median) while the particles' spread stays under
  0.4 m.
- **Compute cost** (measured, our Python code): weighing one scan takes 6, 59
  and 569 ms with 200, 2000 and 20,000 particles. Our MCL weighs a scan every
  0.5 s, so 20,000 would not keep up.

.. tip::

   Hands-on, part 4: kidnap the AV yourself. The setup and the commands are
   on :doc:`the Code page <l6_code>`.


.. _l6-lec-icp:

Scan Registration
~~~~~~~~~~~~~~~~~

- **Where we are:** MCL finds the AV from many guesses, weighed one scan at a
  time.
- **In this section:** **scan registration**: one guess, moved until the scan
  lies on the map. MCL scored many fixed guesses instead. ICP (iterative
  closest point) is one way to do it.
- **What it is for:** a precise pose, handed to the filter as one more
  update.

.. admonition:: Definition: Scan registration (also called scan matching)
   :class: note

   Finding the rotation and shift that best line up a range scan with a
   reference: another scan, or, here, the map. For our AV the rotation and
   shift are its pose :math:`(x, y, \theta)`. Matching range scans is "a basic
   component of many localization and mapping algorithms" (Biber and
   Strasser, 2003).


.. _l6-lec-icp-idea:

Scan Registration: Find the Pose That Puts the Scan on the Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MCL weighs thousands of guesses at once. Scan registration takes **one**
guess and moves it until the scan lies on the map.

.. figure:: /_static/images/L6/scan_matching_idea.png
   :alt: Three top views of the same street, a 5 m scale bar in the third. Each shows green squares, the map points: a building front with two doorways along the top, three poles along the top curb, and a building corner below the bottom curb. A dashed center line splits the road into two lanes. Panel 1: a grey car in the lower lane, turned slightly left, tag 3; grey dots, the scan placed at that car's pose, lie above and to the left of the green walls, tag 2. Panel 2: the same grey car and grey dots, with short black lines joining each grey dot to its nearest green square, tag 4, and a black arrow curving down to the right in front of the car, tag 5. Panel 3: a black car in the lower lane facing right, tag 7; small rust dots sit on every green square, tag 6. Tag 1 marks the map points in each panel.
   :width: 95%
   :align: center

   **1** Map points, in the map frame. **2** The scan, placed at the guessed
   pose **3**. **4** Each scan point paired with its nearest map point.
   **5** The pose moves so the paired points come together. **6** At the
   right pose, the scan lies on the map. **7** That pose: the AV's. Street,
   poses and guess chosen for this example.

**The problem:** the move **5** needs the pairs **4**, but pairs made at the
guess **3** are partly wrong: some scan points meet the wrong map point.
Right pairs need the right pose **7**. We know neither the pose nor the
pairs.


.. _l6-lec-icp-loop:

ICP: Guess the Pairs, Solve, Move, Repeat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: ICP (iterative closest point)
   :class: note

   A method to **register** two point sets, that is, to find the rotation
   and shift that put one on the other. It "requires only a procedure to find
   the closest point on a geometric entity to a given point", and it "always
   converges monotonically to the nearest local minimum of a mean-square
   distance metric" (Besl and McKay, 1992).

.. figure:: /_static/images/L6/icp_three_phases.png
   :alt: A loop of three boxes with arrows. Box 1: pair each scan point with its nearest map point. Box 2: solve for the best rotation and shift (SVD). Box 3: move the scan; repeat until it stops improving. An arrow from box 3 back to box 1 is labeled not done yet: next round, and an arrow from box 3 leads to a separate green box, done: the pose.
   :width: 90%
   :align: center

   The ICP loop. **1. Pair** each scan point with its nearest map point.
   **2. Solve** for the best rotation and shift (SVD). **3. Move** the scan;
   repeat until it stops improving. Not done yet: next round, back to
   Step 1. Done: the pose.

Pairs need the pose, and the pose needs the pairs, so ICP guesses and
repeats three steps:

- **Step 1** pairs scan points with map points.
- **Step 2** solves for the turn and the shift.
- **Step 3** moves the scan and repeats until the update is tiny.

Around the loop come a **start** (a predicted pose) and a **check** before
the result is used. On one scan of our drive, ICP started :math:`5^\circ`,
1.5 m east and 1.0 m south off the truth (chosen). It took 28 rounds and
ended 0.02 m from the truth. The details follow below.


.. _l6-lec-icp-objective:

What ICP Minimizes: One Pair
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/icp_objective_vehicle.png
   :alt: Titled 1. The scan, as the LiDAR measures it: the AV facing right, with the middle of its rear axle at the origin, axes x AV forward and y AV left, a 1 m scale bar, and rust scan points along an L: a column on the left and a row below; one point on the left column is circled and labeled p i.
   :width: 55%
   :align: center

   **1. The scan, as the LiDAR measures it**, relative to the AV:
   :math:`x_{AV}` forward, :math:`y_{AV}` left, the origin at the middle of
   the rear axle. One scan point, :math:`p_i`, is circled.

.. figure:: /_static/images/L6/icp_objective_map.png
   :alt: Titled 2. The same scan, transformed with a guessed pose: green squares of the map, an L-shaped wall along the x and y axes in meters; a faint grey AV labeled the AV at the guess; the rust scan points placed near the wall but turned and shifted, each joined by a thin grey line to its nearest map point. One pair is highlighted: a circled rust point labeled R p i plus t, a boxed green square labeled q i, and the black line between them labeled e i equals 0.78 m.
   :width: 65%
   :align: center

   **2. The same scan, transformed with a guessed pose**, in the map frame.
   Green: the map, an L-shaped wall. Each scan point is joined to its nearest
   map point. One pair is marked: :math:`R\,p_i + t`, :math:`q_i` and the
   distance :math:`e_i = 0.78` m.

ICP looks for the transform :math:`(R, t)`, a turn :math:`R` by
:math:`\theta` and a shift :math:`t = (x, y)`: the AV's pose (Besl and McKay,
1992).

- :math:`p_i`: one scan point, as the LiDAR measures it, relative to the AV
  (first figure).
- :math:`R\,p_i + t`: the same point, transformed to the map frame with a
  guessed pose (second figure).
- :math:`q_i`: the map point paired with it, the nearest one. :math:`e_i`:
  the distance between the two, one per pair; here :math:`e_i = 0.78` m.


.. _l6-lec-icp-sum:

What ICP Minimizes: the Sum over Every Pair
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every scan point gives one pair and one distance :math:`e_i`. ICP adds up
the squared distances into one number, the **error** :math:`E` (in
m\ :sup:`2`), which depends on the guessed pose :math:`(R, t)` (Besl and
McKay, 1992):

.. math::

   E(R, t) = \sum_i e_i^2, \qquad e_i = \lVert R\,p_i + t - q_i \rVert

- **At the guess** of the last figure, the 14 pairs give
  :math:`E = 6.29` m\ :sup:`2` (the distances run from 0.11 m to 1.49 m).
- **At the true pose**, every scan point lands on its map point: every
  :math:`e_i` is 0, and so is :math:`E`.
- **ICP's job:** change :math:`R` (the turn) and :math:`t` (the shift) until
  :math:`E` is as small as it can get. The smaller :math:`E`, the better the
  scan sits on the map.


.. _l6-lec-icp-start:

Before the Loop: Start 4 m Ahead
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A made-up scene (chosen). **Green:** the map. **Black:** the AV, where it
really is. **Gray:** ICP's start, and its scan. **Rust:** where ICP ends, and
its scan.

.. figure:: /_static/images/L6/icp_start_ahead_before.png
   :alt: Titled before ICP: the start. A top view in meters: green map points along y equals 4 and down a side wall at x equals 10, two green poles. The black AV at the origin facing right. A gray car 4 meters ahead of it, and the gray scan, the same walls shifted 4 meters to the right.
   :width: 55%
   :align: center

   **Before ICP.** The start is 4 m ahead of the AV, not turned. Its gray
   scan lies 4 m to the right of the green walls.

.. figure:: /_static/images/L6/icp_start_ahead_after.png
   :alt: The same scene after ICP, titled after ICP: 18 rounds. The rust car sits on the black AV, and the rust scan lies on the green walls and poles.
   :width: 55%
   :align: center

   **After 18 rounds,** ICP ends 0.10 m off: the rust car sits on the black
   AV, and the rust scan lies on the green walls.


.. _l6-lec-icp-start-right:

Before the Loop: Start 4 m to the Right
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same scene and the same distance, 4 m, in another direction.

.. figure:: /_static/images/L6/icp_start_right_before.png
   :alt: Titled before ICP: the start. The same scene. A gray car 4 meters to the right of the black AV, below it, and the gray scan, the same walls shifted 4 meters down, so its top wall runs through the black AV.
   :width: 55%
   :align: center

   **Before ICP.** The start is 4 m to the AV's right, not turned. Its gray
   scan lies 4 m below the green walls.

.. figure:: /_static/images/L6/icp_start_right_after.png
   :alt: The same scene after ICP, titled after ICP: 13 rounds. The rust scan lies across the side wall at an angle, and the rust car ends below and to the right of the black AV, turned.
   :width: 55%
   :align: center

   **After 13 rounds,** ICP stops 7.55 m off and turned :math:`18^\circ`:
   the rust scan lies across the wrong walls, with only 90 of its 126 points
   paired.

**Same distance, another end.** ICP starts from the filter's pose, so the
filter must keep that pose close to the truth.


.. _l6-lec-icp-pairs:

ICP Step 1: Pair Each Scan Point with Its Nearest Map Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/icp_pairs.png
   :alt: The map around the middle scan, green points, and the scan at the 5 degree start, rust points. A thin black line joins most scan points to their nearest map point; a few long red dashed lines, at the top left and near a pole, are pairs 3 m or longer. Legend: pair kept (under 3 m): 495; pair dropped (3 m or more): 7.
   :width: 70%
   :align: center

   The pairs at the first round from the :math:`5^\circ` start. Green: map
   points. Rust: scan points at the start pose. Thin black lines: pairs kept
   (under 3 m), 495. Red dashes: pairs dropped (3 m or more), 7.

1. For each scan point, find the nearest map point: that is its pair.
2. Drop pairs 3 m or longer (our gate, chosen): a scan point with nothing
   near it in the map would pull the fit the wrong way.

**Measured** on the middle scan of our drive, with ICP started 1.5 m east,
1.0 m south and :math:`5^\circ` off the truth (chosen): of its 502 points,
495 are kept (thin lines) and 7 dropped (red dashes).

**The cost:** our map has 18,661 points (the mapping pass's scans, one point
kept per 0.2 m square). Checking all of them for each scan point takes
:math:`502 \times 18{,}661 = 9{,}367{,}822` distances per round of ICP. A k-d
tree finds the same pairs with far fewer distances: the next five parts
show how.


.. _l6-lec-kd-tree:

Why a k-d Tree: Step 1 Asks One Question 502 Times
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 1 asks, for each of the 502 scan points: which of the 18,661 map points
is nearest? Checked one by one:

1. One round: :math:`502 \times 18{,}661 = 9{,}367{,}822` distances.
2. One scan: from the :math:`5^\circ` start, ICP took 28 rounds (Step 3):
   :math:`28 \times 9{,}367{,}822 = 262{,}299{,}016` distances.

And the LiDAR sends 10 scans a second; our filter matches one every second.

.. admonition:: Definition: k-d tree
   :class: note

   "The multidimensional binary search tree (or k-d tree, where k is the
   dimensionality of the search space)", "a data structure for storage of
   information to be retrieved by associative searches" (Bentley, 1975): it
   searches by the values themselves, here the coordinates. Our map points
   have two, :math:`x` and :math:`y`: :math:`k = 2`.

**What it does:** you build it once from the map. It cuts the plane into
boxes, each cut through one map point, :math:`x` and :math:`y` in turn. A
nearest-point search then opens only the boxes near the scan point, not all
18,661 points. Next: build it, then search it.


.. _l6-lec-kd-build:

Building the k-d Tree
~~~~~~~~~~~~~~~~~~~~~

The slide steps through five frames, one level of the tree per frame. Eight
map points (chosen) on a 10 m by 10 m square. In each figure a ring marks
the point that splits at that level (Bentley, 1975), and a shade marks the
part it splits. Solid lines split on :math:`x`, dashed lines on :math:`y`.

**Frame 1 of 5: Level 0, split on** :math:`x`.

.. figure:: /_static/images/L6/kd_tree_level0.png
   :alt: Titled level 0: split on x. Eight green points on a 10 by 10 meter square shaded blue, each labeled with its coordinates: (1, 8), (2, 3), (4, 7), (5, 4), (6, 9), (7, 2), (8, 1), (9, 6). The point (6, 9) is ringed and its label is in bold; a solid line at x equals 6 splits the square.
   :width: 55%
   :align: center

   Level 0: :math:`(6, 9)` splits the whole square with the line :math:`x = 6`.

1. List the points in order of :math:`x`: :math:`(1, 8)`, :math:`(2, 3)`,
   :math:`(4, 7)`, :math:`(5, 4)`, :math:`(6, 9)`, :math:`(7, 2)`,
   :math:`(8, 1)`, :math:`(9, 6)`.
2. Take the middle point. With 8 there are two middle ones, the 4th and the
   5th; our code takes the later one, the 5th: :math:`(6, 9)`.
3. The line :math:`x = 6` cuts the square in two: 4 points left of it, 3
   right.

:math:`(6, 9)` is the **root** of the tree. The rule: take the middle point
when the count is odd (the 2nd of 3), and the later of the two middle ones
when it is even (the 3rd of 4, the 2nd of 2).

**Frame 2 of 5: Level 1, split each half on** :math:`y`.

.. figure:: /_static/images/L6/kd_tree_level1.png
   :alt: Titled level 1: split on y. The left half of the square, left of x equals 6, is shaded blue and the right half yellow. In the left half, (4, 7) is ringed and a dashed line at y equals 7 splits it; in the right half, (7, 2) is ringed and a dashed line at y equals 2 splits it.
   :width: 55%
   :align: center

   Level 1: :math:`(4, 7)` splits the left half with :math:`y = 7`;
   :math:`(7, 2)` splits the right half with :math:`y = 2`.

1. **Left half** (blue), 4 points in order of :math:`y`: :math:`(2, 3)`,
   :math:`(5, 4)`, :math:`(4, 7)`, :math:`(1, 8)`. The 3rd, :math:`(4, 7)`,
   splits it with the dashed line :math:`y = 7`.
2. **Right half** (yellow), 3 points in order of :math:`y`: :math:`(8, 1)`,
   :math:`(7, 2)`, :math:`(9, 6)`. The 2nd, :math:`(7, 2)`, splits it with
   the dashed line :math:`y = 2`.

:math:`(4, 7)` and :math:`(7, 2)` are the root's two **children**: one for
each side of the line :math:`x = 6`.

**Frame 3 of 5: Level 2, split each of the four parts on** :math:`x`.

.. figure:: /_static/images/L6/kd_tree_level2.png
   :alt: Titled level 2: split on x. Four parts shaded: lower left blue, upper left lavender, lower right yellow, upper right grey. (5, 4), (1, 8), (8, 1) and (9, 6) are ringed, each with a solid vertical line through it: x equals 5, 1, 8 and 9.
   :width: 55%
   :align: center

   Level 2: :math:`(5, 4)`, :math:`(1, 8)`, :math:`(8, 1)` and
   :math:`(9, 6)` each split their part with a solid line.

1. **Lower left** (blue: left of :math:`x = 6`, below :math:`y = 7`), 2
   points in order of :math:`x`: :math:`(2, 3)`, :math:`(5, 4)`. The 2nd,
   :math:`(5, 4)`, splits it with the solid line :math:`x = 5`.
2. **Upper left** (lavender), **lower right** (yellow) and **upper right**
   (grey) hold one point each: :math:`(1, 8)`, :math:`(8, 1)` and
   :math:`(9, 6)`. A point alone is its part's middle point, so it splits
   the part with a solid line through it.

Solid lines split on :math:`x`, dashed lines on :math:`y`.

**Frame 4 of 5: Level 3, split on** :math:`y`.

.. figure:: /_static/images/L6/kd_tree_level3.png
   :alt: Titled level 3: split on y. Only the part left of x equals 5 and below y equals 7 is shaded blue; (2, 3) is ringed and a dashed line at y equals 3 splits that part. All earlier lines are drawn.
   :width: 55%
   :align: center

   Level 3: :math:`(2, 3)` splits the last part with :math:`y = 3`.

1. Only :math:`(2, 3)` is left. It is alone in its part (blue), left of
   :math:`x = 5` and below :math:`y = 7`.
2. It splits that part with the dashed line :math:`y = 3`.

Every point is now a **node**: 8 nodes on 4 levels, each with the two sides
of its line as children. The split takes :math:`x` and :math:`y` in turn:
:math:`x` at levels 0 and 2, :math:`y` at 1 and 3.

**Frame 5 of 5: The finished tree.**

.. figure:: /_static/images/L6/kd_tree_full.png
   :alt: Titled the finished tree. Boxes joined by branches. The root (6, 9), x equals 6, at the top; its left child (4, 7), y equals 7, on the branch x less than 6, and its right child (7, 2), y equals 2, on the branch x greater than 6. Under (4, 7): (5, 4), x equals 5, for y less than 7, and (1, 8), x equals 1, for y greater than 7. Under (7, 2): (8, 1), x equals 8, for y less than 2, and (9, 6), x equals 9, for y greater than 2. Under (5, 4): (2, 3), y equals 3, for x less than 5, and a dotted branch marked empty.
   :width: 60%
   :align: center

   The finished tree: each box is a node, its point and the line it splits
   with. Each branch is labeled with its side of the line.

Each box is a **node**: a point and the line it splits with. The root,
:math:`(6, 9)`, is at the top; each level of the build is one row.

- Each node has a **left child** on the smaller side of its line
  (:math:`x < 6`, :math:`y < 7`) and a **right child** on the larger side.
- :math:`(5, 4)` has no right child: no point lies right of :math:`x = 5`,
  left of :math:`x = 6` and below :math:`y = 7`.
- A node with no children is a **leaf**: :math:`(2, 3)`, :math:`(1, 8)`,
  :math:`(8, 1)`, :math:`(9, 6)`.

Going down from the root to a leaf passes at most 4 nodes, one per level,
not all 8 points.


.. _l6-lec-kd-query:

Searching the k-d Tree: the Query and What We Look For
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/kd_query.png
   :alt: Titled 1 query, 8 map points, 8 distances. The eight green map points on a 10 by 10 meter square, each labeled with its coordinates and its distance from a blue star labeled query at (7.5, 5): (1, 8) 7.16 m, (6, 9) 4.27 m, (4, 7) 4.03 m, (5, 4) 2.69 m, (2, 3) 5.85 m, (7, 2) 3.04 m, (8, 1) 4.03 m, and (9, 6) 1.80 m in bold blue, joined to the query by a blue line.
   :width: 55%
   :align: center

   One query (blue star), 8 map points, 8 distances. The nearest,
   :math:`(9, 6)` at 1.80 m, is joined to the query.

.. admonition:: Definition: Query
   :class: note

   The point we search the tree for. In ICP Step 1 it is one scan point,
   transformed to the map frame with the current guess: :math:`R\,p_i + t`.

- **What we look for:** the map point nearest the query. It becomes the
  scan point's pair :math:`q_i`, and their distance is :math:`e_i`.
- **The tree holds the map points** and is built once. The queries change:
  one per scan point, 502 on our middle scan, again in every round as the
  guess moves.
- **Our example** (chosen): the query :math:`(7.5, 5)` and the 8 map points
  of the build. Checking all 8 finds :math:`(9, 6)`, 1.80 m away.

Next: the tree finds the same point after 5 distances, not 8.


.. _l6-lec-kd-search:

Searching the k-d Tree: the Nearest Point, Fast
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The slide steps through seven frames, one step of the search per frame. Each
figure shows the plane with the eight points and their lines (left) and the
tree (right). **Blue:** the query, the node looked at now, and the circle of
the best distance so far. **Rust ring:** a distance measured. **Grey,
dashed:** a side skipped. On every step the query is :math:`(7.5, 5)`, one
scan point; all 7 steps find its one pair.

**Step 1: the root.**

.. figure:: /_static/images/L6/kd_search_step0.png
   :alt: Left, the plane: the root (6, 9) ringed in blue and rust, a blue line from the query star at (7.5, 5) to it, and a dotted blue circle of that radius around the query. Right, the tree: the root box (6, 9), x equals 6, filled blue, labeled 4.27 m.
   :width: 95%
   :align: center

   Step 1: the root :math:`(6, 9)`, 4.27 m from the query.

Search for the map point nearest the query :math:`(7.5, 5)`. The root
:math:`(6, 9)` is 4.27 m away: the best so far. The query's :math:`x`, 7.5,
is more than 6, so go to the right child.

**Step 2: down the query's side.**

.. figure:: /_static/images/L6/kd_search_step1.png
   :alt: Left, the plane: (6, 9) has a rust ring; (7, 2) is ringed in blue and rust, joined to the query by a blue line, and the dotted circle around the query is smaller. Right, the tree: the root box outlined rust with 4.27 m; the box (7, 2), y equals 2, filled blue, labeled 3.04 m.
   :width: 95%
   :align: center

   Step 2: :math:`(7, 2)`, 3.04 m away; the circle shrinks.

:math:`(7, 2)` is 3.04 m away, closer: the best so far, and the circle
shrinks. The query's :math:`y`, 5, is more than 2, so go to the right child.

**Step 3: a leaf.**

.. figure:: /_static/images/L6/kd_search_step2.png
   :alt: Left, the plane: (9, 6) ringed in blue and rust, joined to the query by a blue line; the dotted circle around the query now has radius 1.80 m. Right, the tree: the root and (7, 2) outlined rust with 4.27 m and 3.04 m; the leaf (9, 6), x equals 9, filled blue, labeled 1.80 m.
   :width: 95%
   :align: center

   Step 3: the leaf :math:`(9, 6)`, 1.80 m away.

:math:`(9, 6)` is 1.80 m away: the best so far. It has no children, so the
way down ends. A closer point would lie inside the 1.80 m circle: go back up
and check the sides not taken.

**Step 4: back at** :math:`(7, 2)`.

.. figure:: /_static/images/L6/kd_search_step3.png
   :alt: Left, the plane: (7, 2) ringed in blue; a black two-headed arrow labeled 3.0 m runs from the query down to the line y equals 2; the 1.80 m circle does not reach it; (8, 1) is grey. Right, the tree: (7, 2) filled blue; its branch y less than 2 dashed and the box (8, 1) grey and dashed.
   :width: 95%
   :align: center

   Step 4: the side :math:`y < 2` is 3.0 m away; :math:`(8, 1)` is skipped.

Its other side, :math:`y < 2`, is 3.0 m from the query, more than 1.80 m:
the circle does not reach it. Skip it: :math:`(8, 1)` is never measured.

**Step 5: back at the root.**

.. figure:: /_static/images/L6/kd_search_step4.png
   :alt: Left, the plane: a black two-headed arrow labeled 1.5 m from the query to the line x equals 6, inside the 1.80 m circle; (4, 7) ringed in blue and rust. Right, the tree: (4, 7), y equals 7, filled blue, labeled 4.03 m; (6, 9), (7, 2) and (9, 6) outlined rust; (8, 1) grey and dashed.
   :width: 95%
   :align: center

   Step 5: the line :math:`x = 6` is 1.5 m away, inside the circle; search
   that side. :math:`(4, 7)` is 4.03 m away.

Its other side, :math:`x < 6`, is 1.5 m away, less than 1.80 m: the circle
crosses :math:`x = 6`, so search that side. :math:`(4, 7)` is 4.03 m away,
not closer. The query's :math:`y`, 5, is less than 7, so go to the left
child.

**Step 6:** :math:`(5, 4)`.

.. figure:: /_static/images/L6/kd_search_step5.png
   :alt: Left, the plane: (5, 4) ringed in blue and rust; a black two-headed arrow labeled 2.5 m from the query to the line x equals 5, outside the 1.80 m circle; (2, 3) grey. Right, the tree: (5, 4), x equals 5, filled blue, labeled 2.69 m; its branch x less than 5 dashed and the box (2, 3) grey and dashed.
   :width: 95%
   :align: center

   Step 6: :math:`(5, 4)`, 2.69 m away; the side :math:`x < 5` is 2.5 m
   away, so :math:`(2, 3)` is skipped.

:math:`(5, 4)` is 2.69 m away, not closer. The query's side,
:math:`x > 5`, is empty. The other side, :math:`x < 5`, is 2.5 m away, more
than 1.80 m: skip it, with :math:`(2, 3)`.

**Step 7: back at** :math:`(4, 7)`.

.. figure:: /_static/images/L6/kd_search_step6.png
   :alt: Left, the plane: (4, 7) ringed in blue; a black two-headed arrow labeled 2.0 m from the query up to the line y equals 7, outside the 1.80 m circle; (1, 8) grey. Right, the tree: (4, 7) filled blue; its branch y greater than 7 dashed and the box (1, 8) grey and dashed; five boxes outlined rust with their distances, (9, 6) at 1.80 m in bold.
   :width: 95%
   :align: center

   Step 7: the side :math:`y > 7` is 2.0 m away, so :math:`(1, 8)` is
   skipped. Five rust boxes: five distances measured.

Its other side, :math:`y > 7`, is 2.0 m away, more than 1.80 m: skip it,
with :math:`(1, 8)`. Nothing is left to check. **Answer:** :math:`(9, 6)`,
1.80 m, after 5 of the 8 distances.


.. _l6-lec-kd-code:

Searching the k-d Tree: the Pseudocode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   best = (None, inf)            # 1

   def search(node, q):
     if node is None: return     # 2
     d = dist(q, node.p)         # 3
     if d < best.d: best = (node.p, d)
     a = node.axis               # 4
     diff = q[a] - node.p[a]
     if diff > 0:
       near, far = node.right, node.left
     else:
       near, far = node.left, node.right
     search(near, q)             # 5
     if abs(diff) < best.d:      # 6
       search(far, q)

   search(root, q)

In words, for one query ``q``. A node holds a point ``p``, the axis it splits
on, and two children.

1. No best point yet, at an infinite distance. Start at the root.
2. No node here (an empty side): go back.
3. Measure the query's distance to ``p``. If it is the closest so far, keep
   it as ``best``.
4. ``diff``: how far the query is from the node's line, along its axis.
   Above 0, the query is on the larger side (the right child).
5. Search the query's side first: the near child.
6. Back at this node: if the line is closer than ``best``, a closer point
   may sit across it, so search the far child too. If not, skip it.

Our query, :math:`(7.5, 5)`: 5 distances, not 8. On a big map the expected
cost "is proportional to log N" (Friedman, Bentley and Finkel, 1977).


.. _l6-lec-icp-general:

ICP Step 2 in General: Six Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 2 takes the :math:`n` pairs :math:`(p_i, q_i)` of Step 1 and finds, in
one go, the turn :math:`R` and the shift :math:`t` that best put the scan
points on their map points (Kabsch, 1976). As in ``icp.py``:

.. list-table::
   :widths: 14 40 46
   :header-rows: 1
   :class: compact-table

   * - **Step**
     - **Purpose**
     - **Output**
   * - 1. Centroids
     - the middle of each set
     - :math:`\bar p = \frac{1}{n}\sum_i p_i`,
       :math:`\bar q = \frac{1}{n}\sum_i q_i`
   * - 2. Center
     - remove the shift: only a turn is left
     - :math:`p_i' = p_i - \bar p`, :math:`q_i' = q_i - \bar q`
   * - 3. Compare
     - how the centered pairs line up
     - :math:`H = \sum_i p_i'\, q_i'^{\top}`, :math:`2 \times 2`
   * - 4. Angle
     - the turn that lines the pairs up best
     - :math:`\alpha = \operatorname{atan2}(H_{12} - H_{21},\ H_{11} + H_{22})`
   * - 5. Turn
     - the rotation matrix of that angle
     - :math:`R = \begin{pmatrix} \cos\alpha & -\sin\alpha \\ \sin\alpha & \cos\alpha \end{pmatrix}`
   * - 6. Shift
     - put the turned scan centroid on the map centroid
     - :math:`t = \bar q - R\,\bar p`

In 3-D, steps 4 and 5 become one: the SVD of :math:`H`, with a check that
:math:`R` turns and never mirrors.

.. tip::

   See :ref:`l6-app-icp-hand` in Going Further: the six steps on an example.


.. _l6-lec-icp-drive:

ICP Step 3: Move the Scan and Repeat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The slide steps through three frames. Each is a zoomed top view around the
AV, in meters. **Green:** map points: a long wall with a corner, two rows of
poles and a parked car's outline. **Black:** the AV at its true pose.
**Light rust car:** ICP's pose. **Rust dots:** the scan, transformed with
ICP's pose.

**Frame 1 of 3: The start.**

.. figure:: /_static/images/L6/icp_iter_start.png
   :alt: Titled start. A top view, x east from about minus 35 to 15 meters, y north from about minus 44 to minus 18 meters. Green map points: a long wall near y minus 38 that steps down to y minus 40 at x 0, a corner at x minus 29, poles near y minus 20 and minus 33, and a parked car's outline near x 12, y minus 34. The black AV near x minus 7, y minus 25, and a light rust car beside it, shifted and turned. The rust scan wall crosses the green wall at a small angle, and each rust pole sits beside its green pole.
   :width: 90%
   :align: center

   The start: the rust car sits beside the black AV, and the rust wall
   crosses the green wall.

The middle scan of our drive, transformed to the map frame with ICP's
starting pose (chosen): 1.5 m east, 1.0 m south and :math:`5^\circ` off the
truth, 1.80 m in all. The rust car sits beside the black AV; the rust wall
crosses the green wall, and each pole sits beside its map point. RMSE of the
pairs (the root mean square of their distances): 1.32 m. Each round pairs
(Step 1), solves (Step 2) and moves the scan.

**Frame 2 of 3: After iteration 1.**

.. figure:: /_static/images/L6/icp_iter_1.png
   :alt: Titled after iteration 1. The same view. The light rust car overlaps the black AV more closely, and the rust scan wall crosses the green wall at a smaller angle.
   :width: 90%
   :align: center

   After iteration 1: closer, still crossing.

One move brings the pose to 1.47 m and :math:`3.6^\circ` off the truth: the
rust car is closer to the black AV, and the rust wall crosses the green wall
at a smaller angle; RMSE 0.96 m. One round is not enough: the pairs were
made at a wrong pose, so the move goes only part of the way. ICP pairs again
from the new pose and repeats.

**Frame 3 of 3: After iteration 28.**

.. figure:: /_static/images/L6/icp_iter_last.png
   :alt: Titled after iteration 28. The same view. The rust car covers the black AV, and the rust scan's wall, poles and parked car lie on the green map points.
   :width: 90%
   :align: center

   After iteration 28: the scan lies on the map.

The pose is 0.02 m and :math:`0.02^\circ` off the truth: the rust car covers
the black AV, and the scan's wall, poles and parked car lie on the map; RMSE
0.06 m. **ICP stops** (our code's choices) when the RMSE changes by less
than :math:`10^{-6}`, when the move is smaller than :math:`10^{-6}`, or
after 30 rounds. Here: 28 rounds.


.. _l6-lec-icp-code:

ICP in Our Code: the Whole Loop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``icp.py``, the function the hands-on runs (abridged: the history it keeps
for the plots is left out):

.. code-block:: python

   def icp(source, target, R0, t0, max_iter=30, tol=1e-6, max_dist=2.0):
       R, t = R0, t0
       tree = cKDTree(target)                       # the k-d tree, built once
       for _ in range(max_iter):
           moved = apply(R, t, source)              # the scan at the current pose
           dist, idx = tree.query(moved)            # step 1: nearest map point
           keep = dist < max_dist                   # drop far pairs
           # step 2: the best rotation and shift for the kept pairs
           dR, dt, _ = best_rigid_transform(moved[keep], target[idx[keep]])
           R, t = dR @ R, dR @ t + dt               # step 3: add the correction
           rmse = np.sqrt(np.mean(dist[keep] ** 2))
           # stop when the correction or the change in rmse is below tol
       return R, t

The ICP parts of this lecture and the hands-on call it with
``max_dist=3.0``; the filter runs keep the default, 2.0.


.. _l6-lec-icp-metrics:
.. _l6-lec-icp-four-ways:

Four Ways to Score How Far the Scan Is Off
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/residual_kinds.png
   :alt: Four small panels, each with one rust scan point above a wall of green map points. Panel 1, point to point: a black line from the scan point to the nearest map point. Panel 2, point to line: a black line straight down to the dashed wall line, and a green arrow, the wall's normal. Panel 3, GICP: a flat green ellipse around the map point and a flat rust ellipse around the scan point, joined by a black line. Panel 4, NDT: a grid of cells; the cells along the wall each hold a flat green ellipse with a cross at its center; a dotted line from the scan point to the center of the cell below it.
   :width: 95%
   :align: center

   One scan point (rust) above a wall of map points (green), scored four
   ways: **1** point to point, **2** point to line, **3** GICP, **4** NDT.

1. **Point to point** (our ICP): the straight-line distance from each scan
   point to the nearest map point.
2. **Point to line**: only the distance across the wall, perpendicular to
   it. Moving a scan point along the wall leaves that distance, and so the
   error, the same: the point need not land on a map sample, but nothing
   holds it in place along the wall.
3. **GICP** (generalized ICP): every point of both sets gets a flat ellipse
   along its surface; a pair costs mostly what lies across both surfaces.
4. **NDT**: the map is cut into cells, each kept as one ellipse of its
   points; a scan point scores by how well it fits the ellipse of the cell
   it lands in. No nearest-point search.

All four need a start near the truth.

.. tip::

   See :ref:`l6-app-score` in Going Further: which way, when.


.. _l6-lec-icp-which:

Which Way for an AV, and When
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 16 42 42
   :header-rows: 1
   :class: compact-table

   * - **Way**
     - **Best when**
     - **Weak when**
   * - Point to point
     - the start may be far off: on our street it still ended 0.41 m off
       from a 4.7 m start
     - the map samples flat walls: it stops short (0.41 m on our street)
   * - Point to line
     - a good prediction (the EKF) and building fronts: it ended exact on our
       street
     - the start is far off: it slid 6.5 m along the front
   * - GICP
     - scan to scan (both sets are samples), or many wrong pairs (traffic,
       clutter)
     - time is short: it fits a surface at every point of both sets
   * - NDT
     - a big map: on ours, 4,985 numbers instead of 37,322, and no
       nearest-point search
     - the cell size is badly chosen, or cells are sparse: 674 of our points
       are left out

**Few features** (a highway with only guard rails, a tunnel): no way of
scoring fixes the position **along** the road, because every shift along it
scores the same. That comes from the scene, not the score (next part):
another sensor (GNSS, odometry) must fix that direction.


.. _l6-lec-icp-degenerate:

Some Scenes Cannot Pin Down the Pose
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/scan_degeneracy.png
   :alt: Three top views in meters, each with the AV at the center facing right and green map walls. One wall: a straight wall 4 meters to the left of the AV; a black two-headed arrow along the road under the AV; title one wall: 0.000. A corridor: walls 4 meters on both sides; the same two-headed arrow; title a corridor: 0.000. A corner: a wall on the left that turns and closes the road 8 meters ahead; no arrow; title a corner: 0.297.
   :width: 95%
   :align: center

   Three scenes: one wall, a corridor, a corner. The two-headed arrow marks
   the direction the scan cannot fix. The number above each scene is
   measured.

- **One wall** (left): 1 m further along the road, the AV would see the same
  wall at the same distance. The scan tells how far the AV is from the wall
  and which way it points, but not how far along the road it is.
- **A corridor** (middle), like a tunnel: the same on both sides.
- **A corner** (right), **no problem**: the wall ahead tells how far along
  the road the AV is, the side wall how far across. Any move changes one of
  those distances, so the scan pins the position.

The number above each scene (measured): 0 means one direction (here, along
the road) where moving the AV does not change the scan at all; the larger it
is, the better every direction is fixed.


.. _l6-lec-icp-blind:

When the Scan Is Blind Along the Road: What to Do
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What goes wrong:** with one wall or in a corridor (a tunnel, a highway with
only guard rails), ICP still gives a position along the road. Nothing warns
that this part is a guess: the scan looks the same wherever the AV is along
the road.

**The fix**, each time ICP runs (Zhang, Kaess and Singh, 2016):

1. Check which directions the scan can see: the number in
   :ref:`l6-lec-icp-degenerate`. Near 0, one direction is blind.
2. Keep ICP's answer where the scan can see: the distance to the walls, and
   the heading.
3. Take the position along the road from somewhere else: the EKF's
   prediction, dead reckoning with the gyro's turn rate and the speed the
   wheels measure.

The AV is never without a position: in the blind direction it falls back on
the prediction, which drifts until a corner, a sign or GNSS fixes it again.


.. _l6-lec-icp-filter:

A Match Is a Measurement: Predict, Register, Check, Fuse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/registration_pipeline.png
   :alt: A flow chart. Box 1 Predict, the filter's pose, arrow to box 2 Register, ICP from that pose, arrow to box 3 Check, is the fit usable? An arrow labeled pass goes to box 4 Fuse, filter update; a dashed arrow labeled fail goes down to box 5 Recover, search wider (MCL). A line from Fuse back over the top into Predict is labeled the next prediction starts from the fused pose.
   :width: 85%
   :align: center

   **1** Predict, **2** Register, **3** Check: pass goes to **4** Fuse, fail
   goes to **5** Recover. The next prediction starts from the fused pose.

- **1 Predict:** the EKF (:ref:`l6-lec-ekf`) gives its pose and how unsure
  it is (:math:`\sigma`).
- **2 Register:** run ICP from that pose only when the EKF is sure enough:
  from a far start ICP locks onto the wrong spot (on our street, 6.5 m wrong
  from 1.88 m off).
- **3 Check** the fit: are the pairs close (RMSE)? Is most of the scan
  paired? Does the pose agree with the prediction (NIS,
  :ref:`l6-app-integrity`)? Is every direction seen
  (:ref:`the corridor <l6-lec-icp-degenerate>`)?
- **4 Fuse:** the EKF combines its prediction with ICP's pose, weighing each
  by how sure it is, as with a GNSS fix. ICP adds the heading and works in
  the outage.
- **5 Recover** if the check fails: search wider, with MCL
  (:ref:`l6-lec-mcl`).

Autoware uses MCL to "estimate initial position", then NDT "for position
estimation" (Autoware Foundation, ``autoware_ndt_scan_matcher``
documentation).

.. tip::

   See :ref:`l6-app-integrity` in Going Further: integrity, NIS, the gate and
   the protection level.


.. _l6-lec-failed-run:

The Run That Failed: No Wheel Speed and No GNSS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What we switched off:** GNSS from 34.2 s to 89.0 s, and the wheel speeds
for the whole run. Only the gyro (how fast the AV turns) and ICP were left.
Result: the position was 27.66 m off on average over the drive (APE RMSE).
What happened, measured:

1. **35 s to 44 s, ICP works:** every second it matches the scan to the map,
   the match passes the checks, and the EKF uses it.
2. **45 s:** a match is thrown out: it puts the AV too far from where the
   EKF expected it (the NIS check, :ref:`l6-app-integrity`).
3. **46 s:** the next match is thrown out too: the scan does not line up
   well with the map (its RMSE is too large).
4. **46.5 s:** nothing now tells the EKF how far the AV moves: no wheel
   speeds, no GNSS, no ICP. It grows too unsure to give ICP a good start, so
   ICP is no longer run.
5. **To 89 s:** the EKF knows only how the AV turns, not how far it goes:
   65.6 m off at 79.2 s. GNSS returns at 89.0 s and brings it back.

.. important::

   **The lesson:** ICP keeps the AV located only while it starts from a good
   guess. After two rejected matches it never got one again. To find itself
   again, the AV needs a method that searches widely: MCL. Autoware does the
   same: MCL to find the start, then scan matching (Autoware Foundation,
   ``autoware_ndt_scan_matcher`` documentation).


.. _l6-lec-icp-cases:

Case Studies: Deployed Fleets Match a Map Where GNSS Struggles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Baidu Apollo** fuses GNSS (with RTK), LiDAR map matching and an IMU in an
error-state Kalman filter: the same parts as this lecture. It "adaptively
uses information from complementary sensors such as GNSS, LiDAR, and IMU to
achieve high localization accuracy and resilience in challenging scenes,
such as urban downtown, highways, and tunnels", with "5-10cm RMS accuracy",
"deployed in a large autonomous driving fleet" (Wan et al., 2018).

**Waymo:** "We've built an incredibly detailed set of mapping technologies
that help our cars navigate places even where GPS struggles, like tunnels or
between skyscrapers." Maps are "like memory for the Waymo Driver that
complements what it's actually seeing on the road" (The Waymo Team, 2020).

**What they share with our drive:** a map made before the drive, a scan
matched to it, and a filter that fuses the match with GNSS and motion
sensors. So losing GNSS removes one input, not the pose.

**What they do not publish:** their thresholds, and how long they keep
driving without GNSS.


.. _l6-lec-handson2:

Hands-On, Part 4: MCL and ICP on Our Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The code is in the course's Python repo, folder ``lecture6`` (`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture6>`__).
The setup and the commands are on :doc:`the Code page <l6_code>`. Part 4
runs ``l6_handson.py`` with ``--part mcl`` (the particle filter) and
``--part icp`` (ICP on one scan).

.. admonition:: What to look at
   :class: hint

   1. ``--part mcl``: the particles start anywhere within 20 m of the first
      GNSS fix, with any heading. How long until the spread is under 1 m?
      Where does the error rise again?
   2. ``--part mcl --particles 200``: does it still find the AV? Try three
      values of ``--seed``. How large is the error now?
   3. ``--part mcl --kidnap 40 0 10``: at 40 s every particle jumps 10 m
      north. Does MCL find the AV again? Then ``--kidnap 40 0 30``. Then add
      ``--random 20`` to the first: do random particles help? (Seeds 0 to
      4.)
   4. ``--part icp``: drag the slider. How many iterations until the RMSE
      stops falling? Which walls pull the scan into place first?
   5. ``--part icp --icp-start 4 -3 15``, then ``6 -4 20``: start 5 m and
      :math:`15^\circ` off, then 7.2 m and :math:`20^\circ` off. Which one
      still lands on the walls?


.. _l6-lec-other-maps:

Other Maps, Other Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~

- **Where we are:** ICP matches a LiDAR scan to a map of points.
- **In this subsection:** other maps and other sensors: lane markings,
  visual odometry, visual SLAM, learned localization.
- **What it is for:** knowing what else can give a pose. Each still hands
  its pose to a filter.

The list:

- **Lane markings against an HD (high-definition) vector map.** A camera
  finds the painted lane lines. The map stores them as lines with
  coordinates. Matching the two fixes the **sideways** position, the one a
  heading error spoils fastest. L7 teaches HD maps.
- **Visual odometry:** the motion between two camera images, from features
  that move between them. It drifts like dead reckoning. With one camera the
  scale is unknown, because one camera cannot measure depth (L2).
- **Visual SLAM:** visual odometry plus a map of the features it saw, so a
  place seen again can correct the drift (:ref:`l6-lec-slam`).
- **Learned localization:** a network that says which known place an image
  shows (place recognition), or that estimates the motion between camera
  images.

.. important::

   Every method above still hands a pose to a filter. The integrity checks
   (:ref:`l6-app-integrity` in Going Further) need a model of each source's
   error, so a source whose errors cannot be described is hard to trust.


.. _l6-lec-slam:

SLAM
----

- **Where we are:** matching against a map needs the map first.
- **In this section:** SLAM (simultaneous localization and mapping):
  building the map and finding the pose at the same time.
- **What it is for:** how the map we matched against is made, and how drift
  is removed after the fact.

**Why SLAM.** Our map was made with the AV's true pose, which only a
simulator knows. A real mapping car must find its pose from the scans it
maps. SLAM does both at once.


.. _l6-lec-slam-lost-gnss:

Lost GNSS: Is SLAM the Answer?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/lidar_odometry.png
   :alt: A top view of lap 1 of the route, x east and y north in meters. The black truth starts and ends at a dot labeled start. The green LiDAR odometry path, scan to scan, follows it but drifts outward on the left and bottom sides and ends below and left of the start; a red line joins the two ends, labeled after 458 m: 6.08 m off.
   :width: 75%
   :align: center

   Lap 1 of our drive: the truth (black) and the LiDAR odometry, scan to
   scan (green). After 458 m the odometry ends 6.08 m from the truth.

- **Where a map exists: no.** The AV localizes against the map: 0.52 m off
  on average on our drive, the 400 m outage included (:ref:`l6-lec-map`).
- **Where no map exists:** the first drive through a place, a road outside
  the mapped area, or a road rebuilt since it was mapped. SLAM keeps a pose,
  but the pose drifts: 6.08 m off after our 458 m lap (the figure).
- **Only a loop closure removes the drift.** Back at a place it has seen,
  the AV recognizes it. The next subsections show how.


.. _l6-lec-slam-front-back:

SLAM Has Two Parts: a Front End and a Back End
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: front end and back end of SLAM
   :class: note

   "The front-end abstracts sensor data into models that are amenable for
   estimation, while the back-end performs inference on the abstracted data
   produced by the front-end" (Cadena et al., 2016).

- **Front end:** turns raw scans or images into the edges of a **pose
  graph** (next subsection: the AV's poses, joined by measured motions). The
  edges are the motion between poses in a row (odometry), and loop closures
  when a place is seen again. The front end also decides which measurement
  belongs to which point of the map: the **data association**.
- **Back end:** solves the pose graph, in the next subsections. It works the
  same way whatever sensor made the edges.

.. important::

   So a LiDAR SLAM and a visual SLAM differ in the front end. Their back
   ends can be the same (:ref:`l6-lec-slam-compare`).


.. _l6-lec-pose-graph:

A Pose Graph: Poses as Nodes, Measured Motions as Edges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/pose_graph_terms.png
   :alt: Three circles x1, x2 and x3. Solid gray arrows x1 to x2 and x2 to x3 are labeled odometry edge. A dashed blue arrow from x3 back to x1 is labeled loop closure edge. A legend reads node: a pose; edge: a measured motion between two poses.
   :width: 60%
   :align: center

   A pose graph with three nodes, :math:`x_1`, :math:`x_2` and :math:`x_3`.
   Two **odometry edges** (solid) join poses in a row. A **loop closure
   edge** (dashed, blue) goes from :math:`x_3` back to :math:`x_1`. A node
   is a pose; an edge is a measured motion between two poses.

- **Node:** one pose of the AV, kept with the scan taken there. There is not
  one node per scan. Our code adds a new node each time the AV has moved
  2 m (our code's choice), so the drive's 1,256 scans give 387 nodes
  (measured).
- **Odometry edge:** the motion between two poses in a row, from the
  wheels, the gyro or scan registration.
- **Loop closure edge:** not a drive. The AV drives only
  :math:`x_1 \to x_2 \to x_3`. At :math:`x_3` it is back near where it was
  at :math:`x_1`. ICP between the two scans measures where :math:`x_3` is,
  seen from :math:`x_1` (as our code stores it).
- **Solve:** find the poses that disagree least with all edges, each edge
  weighted by how sure it is (Grisetti et al., 2010).


.. _l6-lec-pose-graph-python:

A Pose Graph in Python: What a Node and an Edge Hold
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # nodes: (n, 3), one pose per row
   nodes = np.array([[x0, y0, th0],
                     [x1, y1, th1]])
   keys = [0, 4]     # scan of each node
   scans = [...]     # (N, 2) each

   # an edge: (i, j, z, Omega)
   z = between(nodes[i], nodes[j])
   # z: node j seen from node i
   s, a = 0.05, np.radians(0.5)
   Omega = np.diag([1 / s**2,
                    1 / s**2,
                    1 / a**2])
   edges = [(i, i + 1, z, Omega)]

- **Node:** the pose :math:`(x, y, \theta)` in the map frame: 3 numbers,
  one row of ``nodes``. The scan stays in its own list. ``keys[i]`` says
  which scan belongs to node :math:`i`.
- **Edge:** three things. Which two nodes it joins (:math:`i`, :math:`j`).
  The measured motion :math:`z`, node :math:`j` seen from node :math:`i`.
  How sure the edge is, :math:`\Omega`, the inverse of its covariance.
  Our choices: :math:`\sigma` = 5 cm and :math:`0.5^\circ` per 2 m step for
  odometry, and 10 cm and :math:`1^\circ` for a loop closure.
- **Solve:** moves only the nodes. The edges are measurements and stay
  fixed.
- **Sizes on our drive** (measured):

  1. 387 nodes: :math:`387 \times 3 \times 8` bytes :math:`\approx` 9.3 kB.
     They are joined by 386 odometry edges.
  2. One scan holds 461 points (median): :math:`461 \times 2 \times 8`
     bytes :math:`\approx` 7.4 kB.
  3. So the scans take the memory, not the graph.


.. _l6-lec-loop-closure:

A Loop Closure Finds the Gap Odometry Left
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/pose_graph.png
   :alt: Two panels with three nodes p1, p2 and p3 joined by rust odometry edges and a green dashed loop closure edge, and an L-shaped building corner of green squares left of and below p1. Left, titled before: the corner seen twice: filled squares where p1 saw the corner, and hollow squares about 0.7 meters higher and slightly to the right, where p3's pose places it; the loop closure from p3 ends short of p1, labeled gap 0.71 m. Right, titled after the solve: one corner: the filled and hollow squares coincide, the dashed edge ends on p1, and faint gray lines show where the edges to p2 and p3 were before.
   :width: 85%
   :align: center

   **Left, odometry only:** the corner seen twice, and a gap of 0.71 m where
   the loop closure from :math:`p_3` misses :math:`p_1`. **Right, after the
   solve:** one corner, and the old path in gray. Values chosen for this
   example.

**Left, odometry only.** At :math:`p_1` the AV sees a building corner
(filled squares). It drives to :math:`p_2` and :math:`p_3`, and each step
adds a little error. Back near the start, it sees the same corner again.
ICP between the two scans measures where :math:`p_3` sits from
:math:`p_1`: the loop closure. Placed from :math:`p_3`'s drifted pose, the
corner lands 0.71 m off (hollow squares). The map holds the corner twice.

**Right, after the solve.** The poses move until the edges agree as well as
they can (gray: the old path). The two views of the corner now coincide.
The whole path is corrected, not only the last pose.


.. _l6-lec-unsure-edges:

The Unsure Edges Take Most of the Correction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the last subsection the loop misses by 0.71 m: following the three
measured motions from :math:`p_1` does not lead back to :math:`p_1`. The
solve spreads that gap over the edges, each edge in proportion to its
variance :math:`\sigma^2`. The less sure an edge, the more it bends. The
values, chosen for this example:

- :math:`\sigma = 0.5` m for the odometry edge :math:`p_1` to :math:`p_2`.
- :math:`\sigma = 0.3` m for the odometry edge :math:`p_2` to :math:`p_3`.
- :math:`\sigma = 0.1` m for the loop closure, which ICP measured.

.. figure:: /_static/images/L6/pose_graph_shares.png
   :alt: A horizontal bar under an arrow labeled the 0.71 m gap, shared out as corrections, cut into three pieces. A wide rust piece: odometry edge p1 to p2, corrected by 0.51 m (71%). A narrower rust piece: odometry edge p2 to p3, corrected by 0.18 m (26%). A thin green piece at the right end: loop closure p3 to p1, corrected by 0.020 m (3%).
   :width: 85%
   :align: center

   The 0.71 m gap, shared out as corrections. The odometry edge
   :math:`p_1` to :math:`p_2` takes 0.51 m (71%), the odometry edge
   :math:`p_2` to :math:`p_3` takes 0.18 m (26%), and the loop closure takes
   0.020 m (3%).

1. The variances are :math:`0.5^2 = 0.25`, :math:`0.3^2 = 0.09` and
   :math:`0.1^2 = 0.01`, together 0.35. Each share is its variance over
   0.35:

   - :math:`p_1` to :math:`p_2`: :math:`0.25/0.35 = 71\%` of the gap,
     0.51 m.
   - :math:`p_2` to :math:`p_3`: :math:`0.09/0.35 = 26\%`, 0.18 m.
   - The loop closure: :math:`0.01/0.35 = 3\%`, 0.02 m.

2. The measurements stay; only the poses move. The edge from :math:`p_1` to
   :math:`p_2` measured :math:`(\Delta x, \Delta y) = (10.3, 0.4)` m
   (chosen). After the solve, :math:`p_2 - p_1 = (10.23, -0.10)` m. That is
   0.51 m away from the measurement, almost all of it along :math:`y`.

.. important::

   A city map is the same problem, with thousands of poses and hundreds of
   loops.

.. tip::

   The least squares, written out: see :ref:`l6-app-pg` in Going Further.


.. _l6-lec-slam-compare:

LiDAR SLAM and Visual SLAM: Different Front Ends, One Back End
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 18 41 41
   :header-rows: 1
   :class: compact-table

   * -
     - **LiDAR SLAM**
     - **Visual SLAM**
   * - Measures
     - distances to surfaces, in meters
     - images; one image has no depth (Mur-Artal et al., 2015)
   * - Front end
     - matches scans (ICP, NDT), or edge and plane points (LOAM; Zhang and
       Singh, 2014)
     - tracks feature points from image to image (ORB features; Campos et
       al., 2021)
   * - Map
     - a point cloud
     - 3-D feature points, sparse
   * - Scale
     - in meters, from the ranges
     - one camera: "scale is unknown"; stereo or an IMU gives meters (Campos
       et al., 2021)
   * - Loop closure
     - a scan descriptor (Scan Context; Kim and Kim, 2018), then ICP
     - a bag of visual words (DBoW2; Gálvez-López and Tardós, 2012)
   * - Weak when
     - "lack of geometrical structures" (Zhang, Kaess and Singh, 2016): one
       wall, no hold along the road
     - "scarcity of texture features" (Zhang, Kaess and Singh, 2016); night,
       weather, season (Sattler et al., 2018)
   * - Examples
     - LOAM, Cartographer (Hess et al., 2016)
     - ORB-SLAM3

The names in the table:

- **NDT:** normal distributions transform.
- **LOAM:** LiDAR Odometry and Mapping.
- **ORB:** a corner detector with a binary descriptor (next subsections).
- **Scan Context:** a short summary of a whole scan.
- **Bag of visual words:** an image summed up as counts of typical feature
  patterns.

A LiDAR is insensitive "to ambient lighting and optical texture" (Zhang and
Singh, 2014). A camera sees appearance: "two rooms may look identical for a
2D laser scanner [...] while a camera may discern them from appearance cues"
(Cadena et al., 2016).


.. _l6-lec-slam-lidar:

LiDAR SLAM on Our Drive: the Drift, and the Loop Closure That Finds It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/lidar_odometry.png
   :alt: A top view of lap 1 of the route, x east and y north in meters. The black truth starts and ends at a dot labeled start. The green LiDAR odometry path, scan to scan, follows it but drifts outward on the left and bottom sides and ends below and left of the start; a red line joins the two ends, labeled after 458 m: 6.08 m off.
   :width: 75%
   :align: center

   Lap 1: the truth (black) and the LiDAR odometry, scan to scan (green).
   The red line is the gap where the loop should close: 6.08 m after 458 m.

1. **Odometry:** ICP between each scan and the one before (1 m gate,
   chosen). 1,256 scans at 10 Hz, 461 points each (median).
2. **Drift, measured:** 6.08 m and :math:`0.78^\circ` off after lap 1
   (458 m); 11.26 m after the whole drive (916 m).
3. **Loop closure:** lap 1 ends with the AV 2.97 m from its start (truth).

   - ICP started from the odometry's guess, which is 6.08 m wrong, ends
     7.57 m off: a local minimum.
   - ICP started from zero offset ("same place", as place recognition would
     propose) ends 0.11 m and :math:`0.05^\circ` off.

4. **Back end:** that edge would let the pose graph share out the 6.08 m,
   as in :ref:`l6-lec-unsure-edges`. The reading page :doc:`SLAM with a
   LiDAR </preread/slam-lidar>` runs that solve.


.. _l6-lec-slam-visual:

Visual SLAM, Step by Step: ORB-SLAM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our drive has no camera recording, so this subsection has no measured
numbers. The reading page :doc:`Visual SLAM </preread/slam-visual>` records
the same route with two cameras and runs each step.

1. **Find corners.** In each image, find small spots that stand out, such as
   a window corner. Give each one a code of 256 yes/no brightness
   comparisons. The same corner gets nearly the same code in the next image,
   so it can be found again (ORB features; Mur-Artal et al., 2015).
2. **Follow them.** How the corners shift from image to image gives how the
   camera moved and where each corner is in 3-D: the odometry edges. One
   camera sees direction but not distance, so the size of the motion stays
   unknown until a second camera or an IMU gives it (Campos et al., 2021).
3. **Keep some images.** Keep a keyframe now and then, with its 3-D corners
   (the reading page's code keeps one every 2 m). The keyframes and their
   corners are the map.
4. **Recognize places.** Sort each keyframe's corner codes into a fixed list
   of common "visual words" and count them. Two keyframes with very similar
   counts are probably the same place: a loop closure (Gálvez-López and
   Tardós, 2012). The reading page's code then checks it with the corners'
   3-D positions.
5. **Fix the drift.** The same pose-graph solve as for the LiDAR.


.. _l6-lec-camera-adds:

What a Camera Adds to LiDAR Localization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A LiDAR measures shape; a camera measures appearance. They fail in different
places: range sensors with a "lack of geometrical structures", cameras with a
"scarcity of texture features" (Zhang, Kaess and Singh, 2016).

1. **A better prediction.** A camera and an IMU together can follow how the
   AV moves in 3-D, including the true size of the motion: visual-inertial
   odometry, or VIO (Qin et al., 2018). VIO can give ICP its starting pose
   (step 1 of the pipeline). It still drifts, like any odometry.
2. **Help where the LiDAR is weak.** In a tunnel or along a long bare wall,
   the LiDAR cannot tell where the AV is along the road, but the camera can
   still see signs and markings. LVI-SAM uses the camera's estimate as the
   starting guess for scan matching. It keeps working when either the camera
   part or the LiDAR part fails (Shan et al., 2021).
3. **Finding the AV with no starting pose.** ICP needs a start. A camera can
   compare the current image with stored images of the whole map to find the
   likely places first, then match details to get the pose (Sarlin et al.,
   2019). For the LiDAR, MCL does this job.

**The limit: appearance changes.** Camera localization must handle "day-night
changes, as well as weather and seasonal variations", and "long-term
localization is far from solved" (Sattler et al., 2018).


.. _l6-lec-calib-sync:

Fusing a Camera and a LiDAR: Calibration and Time Sync
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A camera's view and a LiDAR's points line up only if the AV knows where each
sensor sits and when each reading was taken. Here are two small errors, with
values chosen for this example.

1. **Mounting:** the camera's turn relative to the LiDAR is off by
   :math:`0.5^\circ`. A point 20 m away moves by
   :math:`20 \times \tan 0.5^\circ = 20 \times 0.00873 = 0.17` m.
2. **Time:** the two clocks differ by 10 ms, and the AV drives at 20 m/s. A
   point moves by :math:`0.010 \times 20 = 0.20` m.

Each error alone is more than half of the 0.29 m bound of a local street
(:ref:`l6-lec-bound`): :math:`0.17 / 0.29 = 0.59` and
:math:`0.20 / 0.29 = 0.69`. So where each sensor sits (calibration) and one
shared clock (time sync) are measured and checked, not assumed.


.. _l6-lec-fleet-map:

How a Fleet's Map Is Made
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Mapping drives.** A mapping vehicle drives the streets and records its
   LiDAR scans, GNSS fixes, wheel speeds and IMU readings. It can drive the
   same streets several times, so that each place is seen more than once.
2. **Pose graph.** Each recorded pose becomes a node. Odometry edges join
   poses in a row. Where satellites are in view, a GNSS fix becomes an edge
   that ties one pose to a measured position. Where the vehicle sees a
   street again, a loop closure joins the two poses.
3. **Solve.** The solve moves the poses until they agree as well as possible
   with all the edges. Then every scan is placed at its corrected pose, and
   together the scans make one point map.
4. **Localize against it.** On every later drive, the AV finds itself on
   this map: MCL gives the first pose, and scan registration keeps it up to
   date, as in :ref:`l6-lec-map`.

.. important::

   SLAM builds the map once, offline, with time to check it. The AV on the
   road then localizes against a fixed map, which keeps the online problem
   small and checkable.


.. _l6-lec-slam-40-years:

SLAM after 40 Years: What Is Solved, What Is Not
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**How old.** In 2016 a survey described "astonishing progress over the last
30 years" (Cadena et al., 2016).

1. SLAM research started about :math:`2016 - 30 = 1986`.
2. So it is about :math:`2026 - 1986 = 40` years old.

By 2006 "the general SLAM method" was "a well understood and established
part of robotics", with "many practical issues to overcome, especially in
more complex outdoor environments" (Durrant-Whyte and Bailey, 2006).

**Still open**, by a 2016 survey (Cadena et al., 2016):

- **Maps that stay right for years.** The world changes: trees lose their
  leaves, buildings go up, roads are rebuilt. A map slowly goes wrong, and
  keeping maps of whole cities up to date is not solved.
- **Maps that know what things are.** Our map is only points. A more useful
  map also knows that this is a lane, that is a door, and that a parked car
  will leave.
- **Knowing when to trust it.** SLAM gives a map and a pose, but it cannot
  yet promise how far off they may be.
- **Deciding "same place".** Before a loop closure can help, the AV must
  decide that two scans show the same place, and a wrong yes bends the whole
  map (Durrant-Whyte and Bailey, 2006). On our drive, ICP started from the
  odometry's guess matched the loop 7.57 m off; started from the right
  place, 0.11 m off.


.. _l6-lec-next:

Next Class
----------

.. admonition:: Today
   :class: important

   **L6 found where the AV is in the world.**

   - GNSS gives an absolute position until the sky is blocked.
   - Dead reckoning bridges the gap and drifts.
   - The EKF fuses them.
   - A map removes the drift (MCL, ICP).
   - SLAM builds the map.

How often each method runs on our drive:

.. list-table::
   :widths: 22 30 48
   :header-rows: 1
   :class: compact-table

   * - **Method**
     - **How often (our drive)**
     - **What it gives**
   * - GNSS fix
     - once a second
     - :math:`x`, :math:`y`, a few meters off
   * - Wheel speed, gyro
     - every 0.05 s
     - speed, turn rate
   * - EKF predict
     - every 0.05 s
     - the pose, moved forward
   * - LiDAR scan
     - 10 a second
     - the points around the AV
   * - MCL
     - every 0.5 s
     - the pose from the map, no start needed
   * - ICP map match
     - about once a second
     - the pose :math:`(x, y, \theta)`, once the EKF is sure
   * - SLAM node
     - every 2 m (0.3 s at speed)
     - a pose kept with its scan
   * - Loop closure
     - when a place is seen again
     - an edge that removes the drift

- **L7, Route Planning:** with the AV's pose on the map, find
  a route to the goal.

**Before next class**

- Run the four hands-on parts on :doc:`the Code page <l6_code>`.
- Read the appendix in :doc:`Going Further <l6_appendix>` on ICP
  (:ref:`l6-app-icp-hand`) and on the pose graph (:ref:`l6-app-pg`).
- Read the two SLAM reading pages: :doc:`SLAM with a LiDAR
  </preread/slam-lidar>` and :doc:`Visual SLAM </preread/slam-visual>`.


.. rubric:: Image credits

The vehicle icons in the figures on this page were created by Stone from the
`Noun Project <https://thenounproject.com>`_. The IMU photo is a product image of the
MS-IMU3050 by Memsense, an Inertial Labs company.
