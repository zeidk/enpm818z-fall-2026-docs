====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L6, the slides shown in class and
   the reading slides that go with them, in the same order and with the same
   sections. They add what the speaker notes say aloud, so you can read them
   at home. Material the deck keeps in its appendix (RTK in more detail, ICP
   by SVD and when the rotation is not unique, NDT's score, the likelihood
   field, the pose-graph least squares, and APE and RPE) is on :doc:`the
   appendix page <l6_appendix>`, "Going Further". The papers and pages cited
   below are listed in full on :doc:`the References page <l6_references>`.


.. _l6-lec-introduction:

Introduction
------------

**L5** finds where everything else is, **relative to the AV**. **L6** finds
where **the AV is in the world**.

Last week, in :doc:`L5 </lectures/lecture5/l5_index>`, we found the cars, the
people and the road around the AV, all measured from the AV itself: that car
is 12 m ahead, that person is 3 m to the left. Today we find where the AV
itself is in the world: on which street, in which lane, facing which way.
That answer is the AV's **pose**.

.. figure:: /_static/images/L6/l5_to_l6.png
   :alt: Two top views side by side. Left, labeled L5, where everything else is relative to the AV: the AV in the middle of a road with its own x forward and y left axes, and arrows from the AV to another car and to a pedestrian. Right, labeled L6, where the AV is in the world: a street grid with the map frame's origin at its bottom left corner, x east and y north, and an arrow from the origin to the AV on a road, labeled pose (x, y, theta).
   :width: 90%
   :align: center

   **Left, L5:** the AV sits at the origin of its own frame, :math:`x`
   forward and :math:`y` left, and the arrows go from the AV to another car
   and to a pedestrian. **Right, L6:** the frame is fixed to the map of the
   city, :math:`x` east and :math:`y` north, and one arrow goes from the map's
   origin to the AV: its pose :math:`(x, y, \theta)`.

On the left, everything is measured from the AV. On the right, the frame is
fixed to the map, and the AV is one more thing in it. Once we know the AV's
pose, every object from L5 gets a place on the map too: we only add the two
arrows.


.. _l6-lec-pose-twice:

We Needed the AV's Pose Twice Already
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **L5, the tracker.** The tracker follows each object in a frame that stays
  fixed while the AV drives. To put a new box into that frame, it needs to
  know where the AV is.
- **L5, sharing over V2X.** A message that says "a pedestrian at 4 m ahead of
  me" is useless to another car unless it also says where "me" is.
- **L3, the tunnel.** In :doc:`L3 </lectures/lecture3/l3_index>`, GNSS was
  lost in a tunnel. The wheels and the IMU predicted, and a sign matched
  against the HD map corrected. That was already localization.

.. important::

   Today is the same predict and update loop as in L3, with real sensor
   errors on one recorded drive, and with a map that is a cloud of many
   points instead of one sign.


.. _l6-lec-deliver:

What a Localizer Must Deliver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A **localizer** reads five inputs: GNSS, the IMU's yaw rate (how fast the
car turns), the wheel speed, the LiDAR scan and a map. It gives one answer:
the pose in the map frame, :math:`x`, :math:`y` and the heading
:math:`\theta`, plus how sure it is, as a covariance, as in L3.

.. figure:: /_static/images/L6/localizer_io.png
   :alt: A block diagram. Five input boxes on the left, GNSS, IMU yaw rate, wheel speed, LiDAR scan and map, each with an arrow into a central green block labeled Localizer. One arrow leaves it to the right, to a box labeled pose in the map frame: x, y, theta, plus how sure: covariance.
   :width: 85%
   :align: center

   The localizer. **Five inputs** (GNSS, IMU yaw rate, wheel speed, LiDAR
   scan, map) go in; **one output** comes out: the pose in the map frame,
   :math:`x, y, \theta`, plus how sure it is, a covariance.

.. _l6-lec-bound:

**How good is good enough?** One published answer, for a passenger car, is
from Reid et al. (2019):

- Local streets: "lateral and longitudinal error bounds of 0.29 m (0.10 m,
  95%)". Lateral means sideways; longitudinal means along the road.
- Freeways: "a required lateral error bound of 0.57 m (0.20 m, 95%)".

The **bound** is the error the AV must stay inside almost always. The paper
derives it at a failure rate of :math:`10^{-8}` per hour of driving: the
error goes past the bound less than once in 100 million hours of driving.

Keep **0.29 m** in mind. It is how far the car may be from where it thinks
it is, on a local street. Today we compare every method against that number.


.. _l6-lec-frames:

Two Frames: the Map's and the Vehicle's
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/frames.png
   :alt: A top view. The map frame's origin at the bottom left, x to the right labeled east and y up labeled north. A car on a road, turned at an angle, with its own vehicle frame drawn at the car: x forward along the car and y to its left. The angle theta is marked from a dashed line parallel to the map x axis to the vehicle x axis.
   :width: 70%
   :align: center

   The two frames. The **map frame** sits at the origin, bottom left:
   :math:`x_\text{map}` east, :math:`y_\text{map}` north. The **vehicle
   frame** sits on the car: :math:`x_\text{AV}` forward, :math:`y_\text{AV}`
   left. The angle :math:`\theta` (orange) runs from the map's :math:`x`
   direction to the car's :math:`x` axis.

- **Map frame:** fixed to the ground. :math:`x` points east and :math:`y`
  north, in meters, from an origin we choose.
- **Vehicle frame:** fixed to the AV. :math:`x` points forward and :math:`y`
  to the left. The LiDAR reports in this frame: it says "a wall 8 m to my
  left", not "a wall at 120 m north".
- **Pose** :math:`(x, y, \theta)`: where the vehicle frame's origin sits in
  the map frame, and :math:`\theta`, the angle from the map's :math:`x` axis
  to the AV's :math:`x` axis, counted counterclockwise.

.. warning::

   CARLA's :math:`y` axis points the other way, to the right (the warning
   from :doc:`L2 </lectures/lecture2/l2_index>`). Our recorded drive flips
   it, so both frames turn counterclockwise.


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
     - store the HD map, place GNSS fixes, plan the route, keep tracked objects
       (L5), share positions over V2X (L5)
   * - The AV drives 5 m toward a sign 20 m ahead
     - the sign was at :math:`x = 20` m; now it is at :math:`x = 15` m
     - the sign's :math:`(x, y)` does not change

The 20 m and 5 m are chosen for this example.

The **vehicle frame** moves and turns with the AV. We use it to describe what
the sensors measure, relative to the AV: every LiDAR point, camera box, radar
return, wheel speed and IMU rate arrives in it. We also use it to steer and
set the speed: those commands act along its axes.

The **map frame** never moves. We use it to store the HD map, to place each
GNSS fix (a position on the ground), to plan the route, and to keep tracked
objects over time, as the tracker from :doc:`L5 </lectures/lecture5/l5_index>`
did. Positions shared over V2X use it too.

The last row of the table shows the difference. A sign is 20 m straight
ahead, and the AV drives 5 m forward. In the vehicle frame the sign moved: it
is now 15 m ahead. In the map frame nothing moved: the sign keeps its
:math:`x` and :math:`y`.

.. important::

   **Why the map frame:** readings taken at different times, or by different
   AVs, line up only in a frame that does not move. So the localizer reports
   the pose in the map frame, and the AV uses the pose to move each reading
   from its own frame into the map frame. There it can be compared with the
   map and with older readings.


.. _l6-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

After this lecture, you can:

1. say what each localization sensor measures, and how each one goes wrong;
2. predict how dead reckoning drifts, and why a heading error matters most;
3. read a fused filter's error and its own uncertainty over a GNSS outage,
   and measure a run with the absolute pose error (APE);
4. localize against a map with Monte Carlo localization (MCL), and match a
   scan to a map with ICP, one iteration by hand;
5. check whether a localizer is honest, and say why it needs a second
   source;
6. explain how a loop closure corrects a drifted trajectory in SLAM.

Read them now, and again before the quiz.


.. _l6-lec-drive:

The Drive
---------

- **Where we are:** a localizer reads five inputs and returns a pose.
- **In this section:** one recorded CARLA drive, used for every method
  today.
- **What it is for:** comparing methods on the same data: same route, same
  sensors, same errors.

**Two passes on one route.** The drive was recorded twice in CARLA.

- The **mapping pass** records LiDAR scans at known poses. CARLA knows the
  true pose, so the scans are stitched into a map. A fleet does the same
  with a surveyed mapping car.
- The **localization pass** drives the same route again. That is the pass we
  localize. Every method today must find the pose from its sensors alone. It
  never gets the true pose.


.. _l6-lec-imu:

The IMU: Six Sensors in One Unit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You met the IMU in :doc:`L2 </lectures/lecture2/l2_index>`. It is not one
sensor: it is a unit of six.

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
  and :math:`z`, with gravity included: an accelerometer at rest reads
  gravity, pointing up.

Today we use **one** of the six: the gyroscope about :math:`z`, how fast the
AV turns left or right.

.. figure:: /_static/images/L6/imu_axes.png
   :alt: A product photo of a black IMU, the Memsense MS-IMU3050, its label printing small X, Y and Z axes. Three large axes leave its top face: x forward to the right, z up, and y left going back to the upper left. On each axis a blue double-headed straight arrow marks an accelerometer, and a curved arrow around the axis marks a gyroscope; the curved arrow around z is green. A key reads: accelerometer, along the axis; gyroscope, turn rate about it; the one we use, about z.
   :width: 55%
   :align: center

   The IMU's six sensors, on a real unit. On each axis, an **accelerometer**
   (straight blue arrow) measures along it and a **gyroscope** (curved arrow)
   measures the turn rate about it. The unit prints its own axes on its
   label: X, Y, and Z out of the top. Bolted with X forward, those are the
   vehicle frame. **Green:** the gyroscope about :math:`z`, the one we use.

**Where on the AV.** The IMU is bolted to the body, never loose, so it feels
every turn the car makes. Test cars often put it "on the vehicle roof,
co-located with the GNSS antenna", or inside: "Bolt the IMU to the seat rails
and place the GNSS antenna on the roof directly above" (Racelogic IMU05 user
guide). The IMU and the antenna "should be mounted on the same rigid body".


.. _l6-lec-sensor-outputs:

What Each Sensor Outputs
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: compact-table

   * - **Sensor**
     - **What it outputs**
   * - GNSS
     - a position fix :math:`(x, y)` in the map frame, in meters
   * - Wheel speed
     - the AV's speed :math:`v` along its own :math:`x` axis, in m/s, from how
       fast the wheels turn
   * - Gyro
     - the yaw rate :math:`\omega`: how fast the AV turns, in rad/s
   * - LiDAR
     - a scan: the points it hits on walls, poles and curbs around the AV, as
       :math:`(x, y)` in the vehicle frame

.. admonition:: Definition: Gyro
   :class: note

   A **gyroscope**, or **gyro**, is one of the IMU's six sensors: it measures
   how fast the AV turns about one axis, in radians per second. Ours turns
   about :math:`z`, the vertical axis: its output is the **yaw rate**.

The LiDAR's points come in the vehicle frame, the frame that moves with the
AV. How often each sensor reports, and the errors we gave them, come next.


.. _l6-lec-sensors:

The Sensors, and the Errors We Gave Them
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CARLA's sensors are too clean, and CARLA has no wheel encoder at all. So the
recorder starts from the true motion and adds errors. **We chose every one of
them** for this drive; none is measured from a real car.

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
     - CARLA's; a 2-D slice at sensor height, one point per 20 cm square

- **GNSS.** Remember L3: you can average noise away, never a bias.
- **The outage.** The 400 m without fixes stands in for a street between
  tall buildings. CARLA's GNSS sensor never loses the sky, so we remove the
  fixes ourselves.
- **Wheels and gyro.** The gyro measures how fast the car turns. Its bias,
  0.001 rad/s, is small.
- **LiDAR.** We keep a flat slice at the sensor's height and one point per
  20 cm square, so every scan is a 2-D picture of the walls around the car.


.. _l6-lec-route:

The Route: Two Laps of a Downtown Block
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/l6_route.png
   :alt: A top view of CARLA's Town10HD map as grey points: building walls, poles and a large central building. A rounded rectangular route about 160 by 90 meters runs around the central building, with the start marked on its bottom side by the car. Most of the route is drawn thick and red for the GNSS outage; only the top right stretch is black.
   :width: 75%
   :align: center

   The route from above, :math:`x` east and :math:`y` north in meters. The
   **grey points** are the map: walls, poles and the central block. The
   route runs around the central building, with the start on its bottom
   side. **Red:** the GNSS outage, most of the loop. **Black:** the stretch
   at the top right that has GNSS on both laps.

**Measured on the localization pass:**

- CARLA town Town10HD_Opt, driven counterclockwise by CARLA's autopilot;
- 916 m in 125.7 s, two laps, mean speed 7.3 m/s, a city speed;
- no GNSS from 250 m to 650 m along the route: 34.2 s to 89.0 s, 54.8 s,
  about 55 s. That covers the narrow street on the left and most of the
  second lap;
- the map: 18,661 points from the mapping pass.


.. _l6-lec-gnss:

GNSS and RTK
------------

- **Where we are:** one drive, with errors we chose and know.
- **In this section:** what GNSS gets wrong in a city, and how RTK fixes
  most of it.
- **What it is for:** the only sensor today that says where the AV is on
  Earth without a map.

.. admonition:: Definition: GNSS
   :class: note

   **GNSS** (global navigation satellite system) is "a general term
   describing any satellite constellation that provides positioning,
   navigation, and timing (PNT) services on a global or regional basis"
   (GPS.gov). **GPS** is not a brand: it is the U.S. system, "operated and
   maintained by the U.S. Space Force" (GPS.gov). Galileo (European Union),
   GLONASS (Russia) and BeiDou (China) are others. A receiver times the
   signals from several satellites and solves for its position.

Of everything on the car, only GNSS says where the AV is on Earth with **no
map and no starting point**. Every other sensor today needs one or the
other. So this section asks what goes wrong with GNSS in a city, and how far
a better receiver gets us.


.. _l6-lec-gnss-wrong:

In a City, GNSS Goes Wrong in Two Ways
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The two failures are very different for the AV.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Blocked sky**
     - **Multipath**
   * - Tall buildings hide most satellites. With too few in view, the
       receiver gives a poor fix, or none: an **outage**.
     - A signal bounces off a building before it reaches the antenna. The
       path is longer than the straight line, so the receiver puts the AV in
       the wrong place.
   * - **What the AV sees:** the fixes stop. It knows they stopped.
     - **What the AV sees:** a fix that looks normal and is meters off. It
       does **not** know.

In L3's words ("Noise and bias are two separate errors"): you can average
noise away, but not a bias. Multipath is a bias that comes and goes as the
AV drives. Our drive has the outage. The wrong fix that looks normal comes
back in :ref:`l6-lec-integrity`.


.. _l6-lec-gnss-drive:

Our Drive's GNSS: Meters Off, and Then Nothing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/gnss_error.png
   :alt: GNSS position error in meters against time, 0 to 125 seconds, one blue dot per fix. The dots scatter between about 0.3 and 4 meters, one at 5.4. From 34 to 89 seconds a pink band labeled no fixes has no dots.
   :width: 85%
   :align: center

   GNSS error against time on our drive. Each **blue dot** is one fix, one
   per second; its height is how far the fix is from the truth. The dots scatter between
   about 0.3 m and 4 m, with one at 5.4 m. In the **pink band**, 34 s to
   89 s, there are no fixes.

**Measured, 72 fixes, one per second** (one dot each, so two dots 1 s apart
sit close together on this axis: the first two are at 0 s and 1 s): median
error 1.77 m, 95% of fixes within 3.39 m,
worst 5.44 m. These errors come from the noise and the bias we chose: 1.5 m
of noise in each direction and a fixed bias of about half a meter.

Compare with the local-street bound, 0.29 m. The median fix is **6 times**
too far off:

.. math::

   1.77 / 0.29 = 6.1

Plain GNSS cannot keep a car in its lane. And in the pink band there is
nothing at all for 55 s. Those are the two problems the rest of today
solves.


.. _l6-lec-handson0:

Hands-On, Part 1: Our Drive's GNSS Fixes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the course's Python repo, folder ``lecture6``:

.. code-block:: bash

   python3 l6_handson.py --part gnss   # the fixes as they arrive

.. figure:: /_static/images/L6/handson_gnss.png
   :alt: The hands-on window in four panels with two buttons at the bottom, Play and Step: +1 s, shown at 62 seconds. Top left, the whole route from above: the true path so far in black, the GNSS fixes so far as blue dots joined by a thin blue GNSS-only path, the last fix circled at the top, and the AV drawn as a small car three times its size; the title reads t = 62 s, no fix for 28 s, the AV drove 193 m since the last one. Top right, a close-up 40 meters across around the AV at true size, with no fixes nearby. Bottom left, each fix's error east in blue and north in rust against time, dashed mean lines, and a pink band from 34 to 89 seconds with no dots. Bottom right, every fix's error as a point: the fixes up to 62 seconds in blue with the newest circled, the later ones in gray; a dashed 1.5 meter circle around the chosen bias, a plus for the chosen bias at 0.5 east and 0.3 south, and a cross for the measured mean of all 72 at 0.36 east and 0.49 south. The legend sits to the right of that panel.
   :width: 95%
   :align: center

   The window at 62 s, in the middle of the outage. **Top left:** the whole
   route; the fixes stop at the circled one, the thin blue line is the
   GNSS-only path, and the AV is drawn 3 times its size. **Top right:** a
   close-up 40 m across that follows the AV at true size; outside the outage
   it shows a dashed 1.5 m circle (the noise we chose) around the newest
   fix. **Bottom left:** each fix's error against time. **Bottom right:**
   the errors as points, blue so far and gray still to come: their center
   is the bias, their spread the noise.

The two laps cover the same road, so on the map the gap is hidden: the other
lap's fixes fill it. The gap shows in time. **Play** runs the drive from
start to finish; **Step: +1 s** moves one second, one fix, at a time. Watch
the distance since the last fix grow.

1. Press Play, or step into the outage. How far does the AV drive before the
   next fix?
2. In the window's bottom right, the fixes fill in as they arrive. Where is
   the center of the fixes' errors?
   Compare it with the bias we chose (0.5 m east, 0.3 m south).

The means come out close to the bias, not equal: a mean of a few dozen noisy
fixes still carries noise. See :doc:`l6_code` for what each part shows.


.. _l6-lec-rtk:

RTK, Step 1: a Base Station on a Surveyed Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Can a better receiver fix this? Partly, with **RTK** (real-time kinematic).
RTK corrects the AV's GNSS with a second receiver nearby, in four steps.

.. figure:: /_static/images/L6/rtk_step1.png
   :alt: A side view. A satellite at the top sends signals, drawn as dashed lines, to a base station on the left, a mast on a marker labeled base station on a surveyed point, and to the AV on the right, a car labeled the AV (rover), with an antenna.
   :width: 60%
   :align: center

   One **satellite** sends to both receivers: the **base station** on the
   left, on a surveyed point, and the **AV** on the right, here called the
   **rover**.

- The **base station** is a GNSS receiver fixed on a point whose position a
  surveyor measured. So it knows exactly where it is.
- It sees the same satellites as the AV, through nearly the same atmosphere.

.. important::

   **In Maryland:** NOAA's reference stations are on its `CORS map
   <https://arcg.is/18fWq8>`__ (NOAA National Geodetic Survey). Live
   corrections come from three real-time networks: Trimble KeyNetGPS, Topcon
   TopNET live and Leica SmartNet (Gillins et al., 2019).


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

1. From the satellites, the base computes where it is. Like any receiver,
   it is off.
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

   The **green arrow:** the base sends its error to the AV as
   corrections.

- The base sends its error to every receiver nearby, as **corrections**.
  The AV receiving them is called a **rover**.
- It only helps nearby, where the AV sees the same satellites through the
  same atmosphere: RTK works "in the vicinity of a base station" (ESA Navipedia).
- A real-time network uses many base stations and fills in the corrections
  between them (Gillins et al., 2019), so a rover is never far from one.


.. _l6-lec-rtk-4:

RTK, Step 4: the AV Subtracts the Base's Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/rtk_step4.png
   :alt: A side view. A satellite at the top sends signals, drawn as dashed lines, to a base station on the left, a mast on a marker labeled base station on a surveyed point, and to the AV on the right, a car labeled the AV (rover), with an antenna. Below the base, a panel labeled seen from above, with arrows for east and north: a cross labeled true point and a blue dot labeled GNSS says, up and to the right of it, joined by a rust arrow; below them, in rust, error: 1.2 m east, 0.8 m north. A green arrow from the base to the AV is labeled corrections: the base's error. Below the AV, a second panel seen from above: a cross labeled truth, a blue dot up and to the right joined to it by a rust arrow and labeled raw fix: 1.3 m east, 0.7 m north, and a curved green arrow from the raw fix back to a green dot almost on the cross, labeled in green corrected: 0.1 m east, 0.1 m south.
   :width: 60%
   :align: center

   **Seen from above,** at the AV: the **truth** (cross), the AV's **raw
   fix** (blue dot, rust arrow), 1.3 m east and 0.7 m north, and the
   **corrected** fix (green dot) after the base's error is subtracted
   (curved green arrow), 0.1 m east and 0.1 m south.

Numbers chosen for this example:

1. The AV's raw fix: 1.3 m east and 0.7 m north of the truth.
2. Most of that error is the one the base has, because both see the same
   satellites through the same atmosphere. Subtract the base's error, 1.2 m east
   and 0.8 m north.
3. East: 1.3 minus 1.2 leaves 0.1 m east. North: 0.8 is 0.1 more than 0.7,
   so the fix ends 0.1 m south.
4. That 0.1 m is the AV's own part: its noise, and its multipath from the
   building next to it, which the base does not share.

.. important::

   Our example leaves 0.1 m. Real RTK leaves less: it also measures the
   satellite's radio wave itself, the **carrier**, far finer than the timing
   a plain receiver uses. Near a base that gives "a few centimetres" (ESA
   Navipedia), well inside the 0.29 m error bound for local streets from
   :ref:`the start of the lecture <l6-lec-bound>` (Reid et al., 2019).

.. tip::

   See "Why RTK Reaches Centimeters: the Carrier Wave" in
   :doc:`Going Further <l6_appendix>`.


.. _l6-lec-rtk-limits:

What RTK Cannot Cancel
~~~~~~~~~~~~~~~~~~~~~~

So why not just buy RTK? Three reasons.

.. figure:: /_static/images/L6/rtk_limits.png
   :alt: Three side-view panels. Panel 1, a bounce at the AV: a satellite signal reaches the base station on the left directly, while the signal to the AV bounces off a tall glass tower first, drawn as a rust dashed line; caption base in the open, the bounce is at the AV only. Panel 2, no sky: the AV under a tunnel roof, the satellite's signals stop at the roof, marked with rust crosses; caption no satellites in view, no fix, with or without RTK. Panel 3, far from the base: the base on the left and the AV on the right, joined by a double arrow along the ground. Each one's signal crosses a different shaded patch, labeled atmosphere: the blue patch over the base is labeled delay 1, the rust patch over the AV delay 2; caption beyond 10 to 20 km: the delays differ.
   :width: 95%
   :align: center

   What RTK cannot cancel. **1:** the signal to the AV bounces off a glass
   tower; the base, in the open, does not see that bounce. **2:** under a
   roof no satellite is in view. **3:** far apart, the two signals cross
   different parts of the atmosphere and are delayed differently. **Rust** marks an error.

1. **A bounce at the AV.** RTK subtracts the base's error, so it removes
   only what the base and the AV share: the satellite clock, the orbit and
   the two atmosphere delays (ESA Navipedia). Here the signal to the AV
   bounces off the glass tower first. The bounced path is longer, so the
   AV's distance to that satellite comes out too long. Multipath comes
   mainly from an antenna close to reflecting structures (ESA Navipedia,
   Multipath). The base stands in the open and gets the same signal
   straight, so its error, and the correction it sends, has no bounce in
   it. Subtracting leaves the bounce in the AV's fix: multipath stays.
2. **No sky.** RTK still needs the satellites. Between tall
   buildings, in a tunnel or under a bridge, it stops like plain GNSS.
3. **Far from the base.** Each signal slows down as it crosses the
   atmosphere. ESA's Navipedia lists two of these delays among the errors,
   the ionospheric and the tropospheric delay, named after two layers of
   the atmosphere. Near the base, the two signals cross nearly the same
   atmosphere, so the delays are almost equal and the correction cancels
   them. RTK "can be used for distances of up to 10 or 20 kilometres"
   (Navipedia). A single base station is generally kept under 20 km,
   because farther away the atmospheric delays do not cancel well enough;
   real-time networks put a base station every 70 km or less (Gillins et
   al., 2019).

.. important::

   So the AV needs a second way to know where it is, one that works without
   the sky: the next three sections. First the car's own motion, then a
   map.


.. _l6-lec-check-gnss:

Check: GNSS
~~~~~~~~~~~

.. admonition:: Question
   :class: hint

   An RTK receiver reports a fix 2 cm from the truth in an open parking lot.
   The AV drives into a street lined with glass towers, and the fixes keep
   coming, each one looking normal. Is the AV still within a few
   centimeters?

.. dropdown:: Answer

   **Not necessarily.** A fix that arrives only tells you the sky is not
   fully blocked. It says nothing about bounces. Multipath at the car is not
   in the base station's correction, so a normal-looking fix can be meters
   off. To notice, the AV needs a second, independent source
   (:ref:`l6-lec-integrity`).


.. _l6-lec-dr:

Dead Reckoning
--------------

- **Where we are:** GNSS stops between tall buildings, RTK too.
- **In this section:** dead reckoning, the pose from the car's own speed and
  turn rate.
- **What it is for:** getting through an outage, and the predict step of
  every filter today.

When GNSS stops, the car still knows how fast it goes and how fast it turns.

.. admonition:: Definition: dead reckoning
   :class: note

   Start from a known pose, and add up how far the car drove and how much it
   turned. The wheels measure the speed :math:`v`; the gyro measures the
   turn rate :math:`\omega`, in rad/s.

Every :math:`\Delta t` seconds (0.05 s on our drive), the car moves
:math:`v\,\Delta t` meters in the direction it faces, then turns by
:math:`\omega\,\Delta t`:

.. math::

   x \mathrel{+}= v\cos\theta\,\Delta t, \qquad
   y \mathrel{+}= v\sin\theta\,\Delta t, \qquad
   \theta \mathrel{+}= \omega\,\Delta t

That is the whole method. It is also the predict step of every filter today.


.. _l6-lec-heading:

A Heading Error Grows with Every Meter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Which error hurts dead reckoning most? The heading. Suppose the AV believes
it faces :math:`1^\circ` off its true heading, and drives straight. How far
sideways is it after 100 m?

1. :math:`1^\circ = 0.01745` rad, and :math:`\sin 1^\circ = 0.01745`.
2. Sideways error :math:`= d \sin(\text{heading error})`, where :math:`d` is
   the distance driven. After 100 m:
   :math:`100 \times 0.01745 = 1.75` m. That is half a lane.
3. To stay under the 0.29 m bound, the car can drive
   :math:`0.29 / 0.01745 = 16.6` m. One degree, and the budget is gone
   after one block.

.. figure:: /_static/images/L6/heading_error.png
   :alt: A graph of sideways error in meters against distance driven, 0 to 200 meters. Three straight rust lines from the origin for heading errors of 0.5 degrees (dotted), 1 degree (solid) and 2 degrees (dashed), reaching about 1.75, 3.5 and 7 meters at 200 meters. A dot on the 1 degree line at 100 meters, labeled 100 m at 1 degree: 1.75 m. A red horizontal line at 0.29 meters is labeled 0.29 m bound, Reid et al.
   :width: 70%
   :align: center

   Sideways error against distance driven for three heading errors:
   :math:`0.5^\circ` (dotted), :math:`1^\circ` (solid) and :math:`2^\circ`
   (dashed). The dot marks 1.75 m after 100 m at :math:`1^\circ`. The **red
   line** is the 0.29 m bound (Reid et al.).

Each line is straight: a fixed heading error grows the sideways error by the
same amount every meter.


.. _l6-lec-bias:

A Gyro Bias Makes the Heading Error Itself Grow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our gyro has a bias: it reports 0.001 rad/s of turning when the car goes
straight. That looks tiny. Chosen for this example: speed
:math:`v = 10` m/s, gyro bias :math:`b = 0.001` rad/s (our drive's), the car
driving straight.

1. The heading error is no longer fixed. It grows: :math:`b\,t` after
   :math:`t` seconds. After 30 s it is 0.03 rad, :math:`1.7^\circ`.
2. The car drifts sideways at :math:`v` times the heading error, so the
   sideways speed grows too.
3. Adding up a speed that grows steadily gives

   .. math::

      \text{sideways error} \approx \frac{v\,b\,t^2}{2}
      = \frac{10 \times 0.001 \times 30^2}{2} = 4.5 \text{ m}

The program that integrates step by step gets 4.54 m.

.. figure:: /_static/images/L6/bias_growth.png
   :alt: A graph of sideways error in meters against time since the last fix, 0 to 60 seconds. A rust curve, integrated step by step for a car driving straight with a biased gyro, bends upward through dots labeled 0.52 meters at 10 seconds, 4.54 at 30 and 18.08 at 60. A dotted black curve, v b t squared over 2, lies on top of it.
   :width: 70%
   :align: center

   Sideways error against time since the last fix. The **rust curve** is
   integrated step by step: 0.52 m at 10 s, 4.54 m at 30 s, 18.08 m at
   60 s. The **dotted curve**, :math:`v\,b\,t^2/2`, lies on top of it.

.. important::

   **Twice the time, four times the error.** A fixed heading error grows
   with distance; a gyro bias grows with the square of time. That is why
   dead reckoning only bridges short gaps.


.. _l6-lec-dr-drive:

Dead Reckoning on Our Drive: 400 m Without GNSS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now the real drive. We start dead reckoning from the **true** pose at the
last fix, the best start it could have, and run it with the wheels and the
gyro only through the 400 m without GNSS.

.. figure:: /_static/images/L6/dr_drift.png
   :alt: Left: a top view of the outage part of the route, the truth in black and dead reckoning in rust, starting together at a dot labeled last fix at the top. The rust path slowly turns away from the black one, crossing it in places, and ends a few meters off. Right: position error in meters against distance since the last fix, 0 to 400 meters; it rises to about 2.8 meters by 70 meters, climbs to about 4.7 near 180 meters, dips to about 3.4, then climbs to a peak near 9.0 meters at about 330 meters and ends near 7.8.
   :width: 95%
   :align: center

   **Left:** the road from above, the truth in black and dead reckoning in
   rust, both starting at the last fix (top). **Right:** not a map, but the
   error against the distance driven since the last fix. It rises, dips
   twice, peaks near 9.0 m and ends near 7.8 m.

- On the left, the paths separate slowly on the straights and turn away
  from each other a little at every corner.
- **Measured:** 2.69 m after 100 m, 3.56 m after 200 m, worst 9.03 m at
  329 m, and 7.84 m at the end of the outage.
- The error does not grow smoothly: at some corners the paths cross again.
  But the trend is clear: 2.7 m after 100 m, 8.2 m after 300 m, against a
  bound of 0.29 m.

Dead reckoning bridges a short gap, never a long one.


.. _l6-lec-ekf:

Fusion in the EKF
-----------------

- **Where we are:** dead reckoning drifts; GNSS does not drift but can stop.
- **In this section:** the two together in L3's extended Kalman filter, on
  our drive.
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
     - position, with no drift
     - noisy; biased; stops between tall buildings
   * - Wheels and gyro
     - smooth, 20 times a second
     - drift: grows with distance and time

GNSS gives the position with no drift: a fix now is as good as a fix an hour
ago. But it is noisy, it can be biased, and it stops. The wheels and the gyro
are smooth and come 20 times a second, but they drift, and the last section
showed how fast. Each one is good where the other is bad. L3 gave us the tool
that combines them: the Kalman filter, and for a car that turns, the
**extended Kalman filter** (EKF).


.. _l6-lec-ekf-loop:

L3's Loop, with Our Sensors in It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The filter keeps a **state**, here :math:`x`, :math:`y`, the heading
:math:`\theta` and the speed :math:`v`, and its **covariance** :math:`P`:
how sure it is of each of those numbers (L3).

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Predict** (every 0.05 s)
     - **Update** (when a reading arrives)
   * - Move the state with the dead-reckoning rule of the last section,
       using the gyro. :math:`P` **grows**: the filter is less sure after
       every step it cannot check.
     - Compare the reading with what the state predicts, and move the state
       by a fraction :math:`K` of the surprise, L3's gain. :math:`P`
       **shrinks**. The wheels update the speed :math:`v` every 0.05 s, 20
       times a second. GNSS updates :math:`x` and :math:`y` once a second.

.. note::

   How the filter's matrices are built for this car is **GP3, Task 2**, so
   they are not shown here. Today we look at what the filter does, from
   results files.


.. _l6-lec-ekf-outage:

The Fused Filter in the Outage: Its Error, and Its Own 1σ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/ekf_runs.png
   :alt: Two graphs side by side of meters against time, 0 to 125 seconds, with the outage from 34 to 89 seconds shaded pink. Left, GNSS plus wheels plus gyro: the blue position error stays near 1 to 3 meters, climbs in the outage to peaks near 9 and 9.5 meters, and drops to under 1 meter after the first fix; the grey band of the filter's own 1 sigma grows in the outage only to about 4 meters. Right, with map matching added: after the first few seconds, where it reaches about 2.5 meters, the green error stays mostly under 0.5 meters with short bumps to about 1 meter, outage or not; the grey band stays near 0.2 meters.
   :width: 100%
   :align: center

   The fused filter on our drive. **Pink:** the outage. **Blue or green:**
   the real position error. **Grey:** the filter's own :math:`1\sigma`.
   **Left,** GNSS with wheels and gyro: the error climbs to about 9.5 m in
   the outage while the grey band grows only to about 4 m. **Right,** with
   map matching added: after the first few seconds (up to about 2.5 m), the
   error stays mostly under 0.5 m, with short bumps to about 1 m, outage or
   not.

The grey band is how big the filter thinks its error is: its own
:math:`1\sigma`, :math:`\sqrt{\sigma_x^2 + \sigma_y^2}`, taken from
:math:`P`.

**Left, GNSS with wheels and gyro.**

- Before the outage, :math:`1\sigma` is 0.75 m.
- In the outage, :math:`P` grows, as the last subsection said. At the worst
  moment :math:`1\sigma` is 3.93 m, but the real error is 9.50 m, **2.4
  times** larger: :math:`9.50 / 3.93 = 2.4`. The filter is less sure, but
  not unsure enough: it is **overconfident**. One reason: its model has no
  gyro bias, and the recorder added one.
- At the first fix after the outage, the large :math:`P` gives a large
  :math:`K`. One second after the first fix, the error is back to 0.60 m.
  This is L3's sawtooth, with one long tooth.

**Right, with map matching** (the subject of :ref:`l6-lec-map`): in the
outage, the worst error is 1.06 m, and the error looks the same outside the
outage. It stays near a quarter meter most of the time.


.. _l6-lec-ape:

One Number for a Whole Run: the Absolute Pose Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To compare runs we need one number per run.

.. admonition:: Definition: absolute pose error, APE (position part)
   :class: note

   At each time step, the distance from the estimated position to the true
   one. A run is summarized by the **RMSE** (root mean square error) of
   those distances: square them, average, take the root (Sturm et al.,
   2012).

**Worked example** (4 time steps, distances chosen for the example): 0.3,
0.4, 1.2 and 0.5 m.

1. Square: 0.09, 0.16, 1.44, 0.25.
2. Average: :math:`(0.09 + 0.16 + 1.44 + 0.25)/4 = 1.94/4 = 0.485`.
3. Root: :math:`\sqrt{0.485} = 0.70` m.

The plain average is 0.60 m. The RMSE is larger, because squaring weighs the
one bad step (1.2 m) more. For a car, one bad moment matters more than many
good ones, so that is the weighting we want.

We can compute APE only because CARLA knows the truth. A real car cannot.
That problem belongs to :ref:`l6-lec-integrity`.

.. tip::

   See "APE and RPE" in :doc:`Going Further <l6_appendix>`.


.. _l6-lec-ape-runs:

Eight Runs, One Score Each
~~~~~~~~~~~~~~~~~~~~~~~~~~

These are all eight runs of the hands-on, one APE each.

.. figure:: /_static/images/L6/ape_bars.png
   :alt: A bar chart of APE RMSE in meters for eight runs, blue without map and green with map. GNSS outage: wheels, no map 4.99; wheels, map 0.52; no wheels, no map 4.58; no wheels, map 27.66. GNSS always: wheels, no map 1.28; wheels, map 0.47; no wheels, no map 1.97; no wheels, map 1.38.
   :width: 90%
   :align: center

   APE RMSE for the eight runs. **Blue:** no map. **Green:** with map
   matching. GNSS outage: 4.99, 0.52, 4.58 and **27.66** m. GNSS always:
   1.28, 0.47, 1.97 and 1.38 m.

- **The map lowers APE most.** Through the outage, 4.99 m becomes 0.52 m.
  With GNSS all the way, 1.28 m becomes 0.47 m.
- **Wheels matter less in APE here.** Without them the outage run scores
  4.58 m against 4.99 m, but its worst moment is worse: 12.4 m against
  9.5 m.
- **One run fails:** outage, no wheels, with the map, 27.66 m. Map matching
  made it worse. :ref:`l6-lec-failed-run` explains why: ICP needs a good
  starting guess.


.. _l6-lec-handson1:

Hands-On, Part 2: the Fused Filter on Our Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the course's Python repo, folder ``lecture6``:

.. code-block:: bash

   python3 l6_handson.py --part dr     # dead reckoning only
   python3 l6_handson.py --part ekf    # the fused filter: 8 runs

The setup and the full commands are on :doc:`the Code page <l6_code>`.

.. admonition:: What to look at
   :class: hint

   1. ``--part dr``: where does the error start to grow fast? On a straight
      or in a turn? Think about the heading.
   2. ``--part ekf``: tick and untick **GNSS outage**, **wheels** and **map
      matching**. Each combination is one run of the filter, already
      computed and saved as a results file, so you can switch instantly.
   3. Watch two things: the **error** (blue) and the filter's **own**
      :math:`1\sigma` (grey). In the outage, does the grey band grow as fast
      as the error? If it does, the filter is honest about not knowing.
   4. Note the APE of each run. Which input lowers it most?


.. _l6-lec-check-fusion:

Check: Fusion
~~~~~~~~~~~~~

.. admonition:: Question
   :class: hint

   During the 400 m outage the filter runs only on predict steps. What
   happens to :math:`P`, and what happens at the first fix after the
   outage?

.. dropdown:: Answer

   :math:`P` **grows** at every predict step with no position update,
   because nothing checks the position. So the filter's :math:`1\sigma`
   widens all the way through the outage.

   At the first fix, :math:`P` is large, so **the gain** :math:`K` **is
   large**: the filter trusts its own position little, so it moves most of
   the way to the fix, and :math:`P` drops in one step. That is the
   sawtooth from L3, with one very long tooth.


.. _l6-lec-map:

Against a Map
-------------

- **Where we are:** the fused filter still drifts when GNSS stops. Nothing in
  it says where the car really is.
- **In this section:** finding the pose by matching what the LiDAR sees to a
  map: MCL, then ICP.
- **What it is for:** a position that does not drift and needs no sky.

**The idea.** The map stores where the walls, poles and curbs are, in the map
frame. The LiDAR sees some of them, in the vehicle frame. **Only one pose
puts the scan on top of the map.** Find that pose, and you have the AV's
pose, with no sky and no drift.

This section finds it two ways. First **MCL**, L3's particle filter given a
map. Then **ICP**, which slides the scan onto the map directly.


.. _l6-lec-mcl:

Monte Carlo Localization: L3's Particle Filter, Given a Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Monte Carlo localization (MCL)
   :class: note

   L3's particle filter with a map added (Dellaert et al., 1999). Each
   **particle** is one guess of the pose :math:`(x, y, \theta)`.

1. **Predict:** move every particle with the wheels and the gyro, the dead
   reckoning rule, plus a little random noise so the guesses spread out.
2. **Weigh:** for each particle, put the scan where that particle says the
   car is. Score each scan point by how close it lands to the map.
3. **Resample:** copy the heavy particles and drop the light ones, as in
   L3.

The estimate is the weighted mean of the particles. Their spread is how sure
MCL is.

.. figure:: /_static/images/L6/likelihood_field.png
   :alt: A heat map over a corner of two walls, one along x from 0 to 8 meters and one along y from 0 to 5 meters, drawn as dots. The color is darkest green on the walls and fades to pale green about 2 to 3 meters away. A color bar is labeled how likely a scan point is here.
   :width: 65%
   :align: center

   The scoring of Step 2 for two walls meeting at a corner, one along
   :math:`x` from 0 to 8 m and one along :math:`y` from 0 to 5 m. **Dark
   green** on the walls: a scan point there is likely. The color fades to
   pale green about 2 m to 3 m away, where a scan point is unlikely.

The picture is the scoring, called a **likelihood field**. A scan point that
lands on a wall is likely (dark green). A point in empty space, far from any
wall, is unlikely.

.. tip::

   See "The likelihood field" in :doc:`Going Further <l6_appendix>`.


.. _l6-lec-mcl-symmetry:

When Two Places Look the Same, MCL Can Pick the Wrong One
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here MCL starts knowing nothing. We chose a small world to show one failure
clearly.

**Chosen world:** a 20 m by 10 m box; 2000 particles anywhere in it, with any
heading; 10 scans.

.. figure:: /_static/images/L6/mcl_symmetry.png
   :alt: Two top views of a 20 by 10 meter box drawn as grey dots, each with the car near the bottom left at x 9, y 2, and green particles. Left, plain box: the particles have gathered in one tight cluster near x 11, y 8, the point opposite the car through the box's center. Right, with a small square pillar near the top right, at about x 14.5, y 7.5: the particles sit on the car.
   :width: 95%
   :align: center

   **Left, plain box:** the particles (green) gather opposite the car,
   near :math:`(11, 8)`, while the car is at :math:`(9, 2)`. **Right, with a
   small pillar near one end:** the particles sit on the car.

- **Plain box.** Turn it half a turn and it looks exactly the same. The scan
  cannot tell the two poses apart, so MCL picks one of them. In the run
  shown, it picked the wrong one: the particles sit opposite the car.
- **Over 20 runs** (seeds 0 to 19): in the plain box, **9** runs end on the
  mirror pose. With the pillar, **0**: the two poses now look different,
  and all 20 runs end on the car.

The lesson for real maps: a long street of identical blocks looks the same
in many places. MCL needs something distinctive, or a rough GNSS fix to rule
out the look-alikes. And when a localized car is suddenly moved, say towed,
MCL must recover from a confident wrong belief. That is the
**kidnapped-robot problem**.


.. _l6-lec-mcl-drive:

MCL on Our Drive: from a 20 m Circle to the Car in 2 s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is MCL on our drive, as in the hands-on. The car has just been switched
on. The first GNSS fix says "within about 20 m", and the heading is unknown.

**Start (chosen):** 2000 particles within 20 m of the first GNSS fix, each
with a random heading; one scan every 0.5 s.

.. figure:: /_static/images/L6/mcl_snapshots.png
   :alt: Three top views of the map near the car, each 60 meters wide, with green particles. Scan 1 at t 0 seconds: 2000 particles fill a circle about 40 meters across around the car. Scan 4 at 1.5 seconds: the particles form a short line just behind the car. Scan 16 at 7.5 seconds: the particles sit on the car.
   :width: 95%
   :align: center

   MCL on our drive, three moments. **Scan 1,** :math:`t = 0` s: the
   particles fill a circle 40 m across around the car. **Scan 4,**
   :math:`t = 1.5` s: a short line just behind the car. **Scan 16,**
   :math:`t = 7.5` s: on the car.

- After 4 scans, 1.5 s, only the particles whose scans landed on the walls
  are left: a short line just behind the car.
- **Measured:** the error is first under 1 m at the 5th scan, 2.0 s in.
  After 10 s, the median error is 0.20 m and the worst is 0.95 m.

Unlike the box, the street is not symmetric: the central building, the poles
and the side streets make each place look different.


.. _l6-lec-icp:

Scan Matching: Slide the Scan onto the Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MCL tries thousands of guesses. Scan matching takes one guess and improves
it.

**The problem.** If we knew which map point each scan point hit, the best
pose would be one formula. If we knew the pose, we would know the pairs. We
know neither.

.. figure:: /_static/images/L6/icp_three_phases.png
   :alt: Three boxes in a row with arrows. Box 1: pair each scan point with its nearest map point. Box 2: solve for the best rotation and shift (SVD). Box 3: move the scan; repeat until it stops improving. An arrow from box 3 back to box 1 is labeled not done yet: next round, and an arrow from box 3 leads to a green box labeled done: the pose.
   :width: 90%
   :align: center

   The ICP loop. **1. Pair** each scan point with its nearest map point.
   **2. Solve** for the best rotation and shift (SVD). **3. Move** the scan;
   repeat until it stops improving. Not done yet: back to Step 1. Done: the
   pose.

.. admonition:: Definition: ICP
   :class: note

   **ICP**, iterative closest point (Besl and McKay, 1992): guess the pairs
   from the nearest points, solve, move, guess again. Each round makes the
   pairs better.

The first pairs are partly wrong, but the move brings the scan closer, so
the next pairs are better. ICP stops when the fit stops improving.


.. _l6-lec-icp-steps13:

ICP by Hand, Steps 1 to 3: Centroids, then the Cross-Covariance H
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is one ICP fit by hand: Step 2 of the loop, the solve. Three scan points
:math:`p_i` and three map points :math:`q_i`, numbers chosen for the example,
already paired: :math:`p_1` with :math:`q_1`, and so on.

.. figure:: /_static/images/L6/icp_worked_before.png
   :alt: Three orange scan points p1 at 1, 0, p2 at 0, 2 and p3 at minus 1, minus 2, and three green open circles, the map points q1 at 2, 2, q2 at 0, 1 and q3 at 4, 0. Dotted lines join p1 to q1, p2 to q2 and p3 to q3.
   :width: 55%
   :align: center

   Before: **scan points** :math:`p_1 = (1, 0)`, :math:`p_2 = (0, 2)`,
   :math:`p_3 = (-1, -2)` (orange dots) and **map points**
   :math:`q_1 = (2, 2)`, :math:`q_2 = (0, 1)`, :math:`q_3 = (4, 0)` (green
   circles). Dotted lines join each pair.

1. **Centroids,** the average point of each set:

   .. math::

      \bar p = \Big(\frac{1 + 0 - 1}{3},\ \frac{0 + 2 - 2}{3}\Big) = (0, 0),
      \qquad
      \bar q = \Big(\frac{2 + 0 + 4}{3},\ \frac{2 + 1 + 0}{3}\Big) = (2, 1)

   The scan's centroid is the origin because the points were chosen that
   way.

2. **Center:** subtract the centroids, so both sets sit around the origin.
   :math:`p_i' = p_i - \bar p` is unchanged. :math:`q_i' = q_i - \bar q`
   gives :math:`(0, 1)`, :math:`(-2, 0)` and :math:`(2, -1)`.

3. **Cross-covariance** :math:`H = \sum_i p_i'\,q_i'^{\top}`: for each pair,
   multiply the scan point's coordinates by the map point's, and add over
   the pairs.

   .. math::

      H = \begin{pmatrix} -2 & 2 \\ -8 & 2 \end{pmatrix}

   Top left entry: :math:`\sum p_x' q_x' = 1 \cdot 0 + 0 \cdot (-2) + (-1)
   \cdot 2 = -2`. The other three entries come the same way.

:math:`H` holds everything the rotation needs: how the scan's spread lines
up with the map's.


.. _l6-lec-icp-steps45:

ICP by Hand, Steps 4 and 5: the Rotation, then the Shift
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. **Rotation.** In general you take the SVD of :math:`H`, as the appendix
   shows. In 2-D the SVD's answer has a short form:

   .. math::

      \alpha = \operatorname{atan2}\big(H_{12} - H_{21},\ H_{11} + H_{22}\big)
      = \operatorname{atan2}\big(2 - (-8),\ -2 + 2\big)
      = \operatorname{atan2}(10, 0) = 90^\circ

   .. math::

      R = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}

   :math:`R` turns every point a quarter turn counterclockwise.

5. **Shift:** the map's centroid minus :math:`R` times the scan's centroid:
   :math:`t = \bar q - R\,\bar p = (2, 1) - (0, 0) = (2, 1)`.

**Check one pair:** :math:`R\,p_1 = (0, 1)`; add :math:`t`:
:math:`(0, 1) + (2, 1) = (2, 2) = q_1`.

.. figure:: /_static/images/L6/icp_worked_after.png
   :alt: The three moved scan points, R p plus t, drawn as orange dots, each sitting inside its green map circle q1 at 2, 2, q2 at 0, 1 and q3 at 4, 0.
   :width: 55%
   :align: center

   After: the moved scan, :math:`R\,p_i + t` (orange dots), lands on the
   map points :math:`q_1`, :math:`q_2` and :math:`q_3` (green circles).

All three moved points land on their map points. On the car, the pairs come
from nearest neighbors, so they are partly wrong at first, and the loop
repeats until the fit stops improving.

.. tip::

   See "The SVD, and when the rotation is not unique" in :doc:`Going Further
   <l6_appendix>`.


.. _l6-lec-icp-drive:

ICP on One Scan of Our Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is ICP on one real scan from the middle of the drive. We start it off
the truth on purpose.

**Start (chosen):** :math:`5^\circ` off, 1.5 m east and 1.0 m south of the
truth.

.. figure:: /_static/images/L6/icp_iterations.png
   :alt: Three top views, each with green map points and rust scan points. Start: the scan is turned and shifted, its walls crossing the map's at a small angle. After iteration 1: closer, still crossing. After iteration 28: the scan's walls, poles and car outlines lie on the map's.
   :width: 95%
   :align: center

   ICP on one scan. **Green:** the map. **Rust:** the scan. **Start:** the
   scan is turned and shifted, its walls crossing the map's at a small
   angle. **After iteration 1:** closer, still crossing. **After iteration
   28:** the scan's walls and poles lie on the map's.

**Measured:** 28 iterations. The RMSE of the pairs goes from 1.32 m to
0.06 m, and the final pose is 0.02 m and :math:`0.02^\circ` from the truth.
That is the kind of update the filter gets once a second in the "map
matching" runs.


.. _l6-lec-failed-run:

The Run That Failed: No Wheels, No GNSS, One Rejected Match
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the failed run from the bar chart: outage, no wheels, map matching
(27.66 m APE). Measured, in that run:

1. 35 s to 44 s: one ICP pose per second, all accepted.
2. 45 s: the NIS gate rejects one match.
3. 46 s: ICP runs, but its fit fails the quality check and is dropped.
4. Nothing measures the speed now: no wheels, no GNSS. At 46.5 s the
   filter's position :math:`\sigma` passes 2 m, the limit we chose for
   starting ICP, so ICP stops.
5. The filter coasts on the gyro alone: 65.6 m off at 79.2 s. GNSS returns
   at 89.0 s and pulls it back.

.. important::

   ICP keeps the AV localized only while it has a good starting guess. Once
   lost, the AV needs a method that searches widely: MCL, as Autoware does to
   "estimate initial position" (Autoware Foundation,
   ``autoware_ndt_scan_matcher`` documentation).


.. _l6-lec-icp-filter:

The Matched Pose Is One More Update for the Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Matching fits with the filter from :ref:`l6-lec-ekf` in two ways.

- **The filter gives ICP its start.** ICP needs a starting guess close to
  the truth, or it slides into the wrong fit, like the mirror pose in the
  box. The filter's own pose is that guess.
- **ICP gives the filter an update.** ICP's answer, a pose
  :math:`(x, y, \theta)`, goes back to the filter as one more update. It is
  like a GNSS fix, but it also measures the heading, and it keeps coming in
  the outage. That is the "map matching" box in the hands-on: compare the
  runs with and without it.
- Before the filter accepts the pose, the NIS test of L3 checks that it is
  not wildly off (:ref:`l6-lec-integrity`).

.. admonition:: Autoware does the same
   :class: note

   Autoware, the open-source driving stack, uses **NDT**, another scan
   matcher: "a package for position estimation using the NDT scan matching
   method". It also uses "the Monte Carlo method" to "estimate initial
   position" (Autoware Foundation, ``autoware_ndt_scan_matcher``
   documentation). So: MCL to find the car once, scan matching to follow
   it.


.. _l6-lec-handson2:

Hands-On, Part 3: MCL and ICP on Our Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python3 l6_handson.py --part mcl    # particle filter
   python3 l6_handson.py --part icp    # ICP on one scan

The setup and the full commands are on :doc:`the Code page <l6_code>`.

.. admonition:: What to look at
   :class: hint

   1. ``--part mcl``: the particles start anywhere within 20 m of the first
      GNSS fix, with any heading: the car has just been switched on. How
      long until the spread is under 1 m? Where does the error rise again?
      Look at what the LiDAR sees there.
   2. ``--part mcl --particles 200``: does it still find the car? Try three
      values of ``--seed``. How large is the error now?
   3. ``--part icp``: drag the slider, one iteration at a time. How many
      iterations until the RMSE stops falling? Which walls pull the scan
      into place first?
   4. ``--part icp --icp-start 4 -3 15``, then ``6 -4 20``: start 5 m and
      :math:`15^\circ` off, then 7.2 m and :math:`20^\circ` off. Which one
      still lands on the walls?

.. dropdown:: What the drive shows for Questions 2 and 4

   - **200 particles.** On this drive MCL still finds the car on every seed
     tried, but less precisely: after 10 s the median error is 0.29 m to
     0.78 m, against 0.20 m to 0.34 m with 2000 particles. Fewer particles
     cover the start more thinly.
   - **A far start.** From 5 m and :math:`15^\circ` off, ICP still lands,
     10 cm from the truth. From 7.2 m and :math:`20^\circ` off it does not:
     it ends 7 m off, on the wrong walls. This is why ICP needs a good
     starting guess.


.. _l6-lec-ndt:

NDT: Match the Scan to a Smooth Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NDT is what Autoware runs. It skips ICP's pairs.

.. admonition:: Definition: NDT
   :class: note

   **NDT**, the normal distributions transform (Biber and Strasser, 2003):

   1. Cut the map into cells (here 2.5 m, chosen).
   2. In each cell, fit a mean and a covariance to the map points: one
      ellipse, long and thin along a wall.
   3. Score a pose by how likely each scan point is under its cell's
      ellipse, and move the pose to raise the score.

.. figure:: /_static/images/L6/ndt_cells.png
   :alt: The 20 by 10 meter box with its pillar, drawn as grey dots with a little noise, under a grid of 2.5 meter cells. In the cells with points, green ellipses: long and thin along each wall, wider and tilted in the corner cells, and round in the pillar's cell.
   :width: 80%
   :align: center

   NDT on the box with its pillar, under a grid of 2.5 m cells. Each
   **green ellipse** is one cell's mean and covariance: long and thin along
   a wall, wider and tilted in the corners, round at the pillar.

- "How likely" uses the Mahalanobis distance from L3.
- There are no nearest-point pairs, so the score changes smoothly as the
  pose moves: no jumps when a nearest neighbor switches.
- The map is also smaller: a few numbers per cell instead of every point.

.. tip::

   See "NDT's score" in :doc:`Going Further <l6_appendix>`.


.. _l6-lec-other-maps:

Other Maps, Other Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~

The LiDAR point map is one kind of map. Here are others, to place them.

- **Lane markings against an HD vector map.** A camera finds the painted lane
  lines; the map stores them as lines with coordinates. Matching the two
  fixes the **sideways** position, the one a heading error spoils fastest.
  L7 teaches HD maps and Lanelet2.
- **Visual odometry:** the motion between two camera images, from features
  that move between them. It drifts like dead reckoning. With one camera the
  scale is unknown, because one camera cannot measure depth (L2).
- **Visual SLAM:** visual odometry plus a map of the features it saw, so a
  place seen again can correct the drift (:ref:`l6-lec-slam`).
- **Learned localization:** a network that says which known place an image
  shows (place recognition), or that estimates the motion between frames.

.. important::

   Every method above still hands a pose to a filter. The integrity checks
   of the next section need a model of each source's error, so a source
   whose errors cannot be described is hard to trust (L3's argument about
   verifiability).


.. _l6-lec-integrity:

Integrity
---------

- **Where we are:** GNSS, wheels, gyro and the map, fused into one pose.
- **In this section:** how the AV checks that pose without knowing the
  truth.
- **What it is for:** knowing when the pose cannot be trusted, and saying
  so.

On the drive we measured every error against the truth. A real car never
knows the truth. So how does it know its pose is good?

.. admonition:: Definition: integrity
   :class: note

   "A measure of trust that can be placed in the correctness of the
   information supplied by a navigation system", including "the ability of
   the system to provide timely warnings to users when the system should
   not be used" (Zhu et al., 2018).

Integrity has two halves: be right, and when you might be wrong, say so in
time.


.. _l6-lec-nis-drive:

Is Our Filter Honest? Its NIS over the Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is L3's honesty test on our filter, in the run with the outage, wheels
and the map. Each dot is the NIS of one update.

.. figure:: /_static/images/L6/integrity_nis.png
   :alt: NIS on a log scale against time, 0 to 125 seconds, blue dots for GNSS fixes and green dots for map poses. Most dots lie between 0.1 and 10, with a few blue dots lower. Two dashed lines: green at 11.34 for the map pose, blue at 9.21 for GNSS. One blue dot near 105 seconds lies above 9.21; no green dot lies above 11.34.
   :width: 85%
   :align: center

   NIS against time, on a log scale. **Blue:** GNSS fixes (2 numbers).
   **Green:** map poses (3 numbers). The dashed lines are the gates: 9.21
   for GNSS, 11.34 for a map pose. One blue dot, near 105 s, is above 9.21;
   no green dot is above 11.34.

- **Expected, if the filter is honest** (L3): the NIS averages about 1 per
  number the sensor reports, so 2 for a fix and 3 for a pose.
- **Measured:** GNSS 2.12 over 68 fixes, which is honest. Map 2.50 over 118
  poses, a little below 3, so the filter slightly overestimates the map's
  error. That is the safe side.
- **The gates** are set at 0.99, so we expect about 1 in 100 honest updates
  above the line. One GNSS fix of the 68 is above 9.21; no map pose is above
  11.34.


.. _l6-lec-nis-mistakes:

The NIS Gate Makes Two Kinds of Mistake
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L3 gave us the test:

.. math::

   \varepsilon = \boldsymbol{\nu}^{\top} S^{-1} \boldsymbol{\nu}

Here :math:`\boldsymbol{\nu}` is the surprise, the difference between the
reading and what the filter predicted, and :math:`S` is the surprise the
filter expects. :math:`\varepsilon` is the NIS: the surprise squared over the
expected surprise. The filter rejects an update when :math:`\varepsilon` is
too large for the number of values it reports. At 0.99, too large means
above **9.21** for a GNSS fix (:math:`x`, :math:`y`) and above **11.34** for
a matched pose (:math:`x`, :math:`y`, :math:`\theta`). Both bounds come from
the chi-square distribution.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **False alarm:** a good update is rejected
     - **Missed fault:** a bad update is accepted
   * - A street full of parked trucks that the map does not have makes the
       scan match badly, and the filter drops a pose that was right.
       **Cost:** the filter coasts on dead reckoning a little longer.
     - A multipath fix 3 m off (chosen) arrives while :math:`P` is large,
       after the outage. Then :math:`S` is large, so :math:`\varepsilon`
       stays small, the gate lets the fix through, and the filter moves 3 m
       the wrong way. This is the dangerous one.

An overconfident filter makes false alarms; an underconfident one misses
faults. That is why L3 insisted that the filter be honest.


.. _l6-lec-protection:

Say When the Error Could Be Too Large: the Protection Level
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second half of integrity is saying so in time. Both terms below are
quoted from Zhu et al. (2018).

- **Alert limit:** "the largest position error allowable for safe
  operation". For a car on a local street, take Reid's 0.29 m (Reid et al.,
  2019).
- **Protection level:** "a statistical error bound computed so as to
  guarantee that the probability of the absolute position error exceeding
  the said number is smaller than or equal to the target integrity risk".
  The localizer computes it from its own covariance and error models, so
  that the true error goes past it only with a tiny, chosen probability.
- **The rule:** if the protection level is above the alert limit, warn. The
  pose cannot be used for lane-level driving right now.

.. important::

   **Two independent sources.** The simplest protection is a second source
   that fails for a different reason. GNSS fails under a blocked sky; map
   matching fails where the map is wrong. If they agree, both are likely
   right. If they disagree, the AV at least knows that one is wrong. What the
   car does then, keeping the AV safe when one source fails, is L13.


.. _l6-lec-slam:

SLAM
----

- **Where we are:** matching against a map needs the map first.
- **In this section:** SLAM, building the map and finding the pose at the
  same time.
- **What it is for:** how the map we matched against is made, and how drift
  is removed after the fact.

Everything in :ref:`l6-lec-map` assumed a map. Where does the map come from?
Our mapping pass took a shortcut: CARLA gave the true pose for every scan. A
real mapping car has no true pose. It has to build the map and find its pose
at the same time.

.. admonition:: Definition: SLAM
   :class: note

   **SLAM**, simultaneous localization and mapping. With no map, the AV
   places each scan at the pose odometry gives. Odometry drifts, so the map
   drifts with it: the same wall, seen twice, lands in two places. Drive
   around a block, and a wall seen at the start and again at the end shows
   up twice.


.. _l6-lec-pose-graph:

A Pose Graph: Poses as Nodes, Measured Motions as Edges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Graph-based SLAM keeps a **pose graph**.

.. figure:: /_static/images/L6/pose_graph_terms.png
   :alt: Three circles x1, x2 and x3. Solid arrows x1 to x2 and x2 to x3 are labeled odometry edge. A dashed blue arrow from x3 back to x1 is labeled loop closure edge. A legend reads node: a pose; edge: a measured motion between two poses.
   :width: 60%
   :align: center

   A pose graph with three nodes, :math:`x_1`, :math:`x_2` and :math:`x_3`.
   Two **odometry edges** (solid) join poses in a row; a **loop closure
   edge** (dashed, blue) goes from :math:`x_3` back to :math:`x_1`. A node
   is a pose; an edge is a measured motion between two poses.

- **Node:** one pose of the AV, kept with the scan taken there.
- **Odometry edge:** the motion between two poses in a row, from the wheels
  and the gyro, or from scan matching (ICP between two scans in a row).
- **Loop closure edge:** the AV is back somewhere it has been. ICP between
  the new scan and the old scan from that place measures the motion between
  two poses that are far apart in time. This is the important edge.
- **Solve:** find the poses that disagree least with all edges, each edge
  weighted by how sure it is. That is a least-squares problem. The tutorial
  by Grisetti et al. (2010) is the reference.


.. _l6-lec-loop-closure:

A Loop Closure Finds the Gap Odometry Left
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the smallest graph with a loop: three positions, two odometry edges
and one loop closure. All numbers are chosen for the example.

- Odometry :math:`p_1 \to p_2`: :math:`(10.3, 0.4)`, and
  :math:`p_2 \to p_3`: :math:`(-5.2, 8.3)`, each with :math:`\sigma = 0.5` m.
  Odometry is unsure.
- Loop closure :math:`p_3 \to p_1`: :math:`(-5.0, -8.0)`, with
  :math:`\sigma = 0.1` m. It comes from ICP, so it is sure.

.. figure:: /_static/images/L6/pose_graph.png
   :alt: Two panels with three nodes p1, p2 and p3 joined by rust odometry edges and a green dashed loop closure edge. Left, before, odometry only: the loop closure from p3 ends 0.71 meters from p1, labeled gap 0.71 m. Right, after, with the loop closure: the dashed edge ends on p1, and p2 and p3 have moved slightly.
   :width: 85%
   :align: center

   **Left, before** (odometry only): the loop closure from :math:`p_3`
   misses :math:`p_1` by a gap of 0.71 m. **Right, after** (with the loop
   closure): the gap is gone, and :math:`p_2` and :math:`p_3` have moved a
   little.

**Around the loop.** If the three edges were perfect, they would add up to
:math:`(0, 0)`: you end where you started.

1. In :math:`x`: :math:`10.3 - 5.2 - 5.0 = 0.1`.
2. In :math:`y`: :math:`0.4 + 8.3 - 8.0 = 0.7`.
3. The gap is :math:`(0.1, 0.7)`, 0.71 m long.

On the right, the solved graph: the gap is gone, and :math:`p_2` and
:math:`p_3` have moved a little. The next subsection says by how much, and
why.


.. _l6-lec-unsure-edges:

The Unsure Edges Take Most of the Correction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For one loop, the least-squares answer has a short form: **each edge takes a
share of the gap in proportion to its variance** :math:`\sigma^2`.

1. Variances: :math:`0.5^2 = 0.25` for each odometry edge, and
   :math:`0.1^2 = 0.01` for the loop. Total: :math:`0.25 + 0.25 + 0.01 =
   0.51`.
2. Shares: :math:`0.25/0.51 = 0.49` (49%) for each odometry edge;
   :math:`0.01/0.51 = 0.02` (2%) for the loop.
3. Move :math:`p_2` back by its edge's share of the gap :math:`(0.1, 0.7)`:
   :math:`p_2 = (10.3, 0.4) - 0.49 \times (0.1, 0.7) = (10.25, 0.06)`.
4. :math:`p_3` moves once for each odometry edge:
   :math:`p_3 = p_2 + (-5.2, 8.3) - 0.49 \times (0.1, 0.7) = (5.00, 8.01)`.

.. important::

   The sure edge, the loop closure, barely bends; the unsure ones take the
   correction. A city map is the same problem with thousands of nodes and
   hundreds of loops, solved as one least-squares problem.

.. tip::

   See "The least squares, written out" in :doc:`Going Further
   <l6_appendix>`.


.. _l6-lec-fleet-map:

How a Fleet's Map Is Made
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Mapping drives:** a car records LiDAR, GNSS, wheels and IMU, often over
   several drives of the same streets.
2. **Pose graph:** one graph from all of it, with odometry edges, GNSS where
   the sky is open, and loop closures wherever streets are seen again.
3. **Solve,** then place every scan at its corrected pose. That gives one
   point map, like the one we matched against.
4. **Localize against it** on every later drive: MCL to start, scan matching
   to follow, as in :ref:`l6-lec-map`.

.. important::

   SLAM builds the map once, offline, with time and people to check it. The
   AV on the road then localizes against a fixed map, which keeps the online
   problem small and checkable.


.. _l6-lec-next:

Next Class
----------

.. admonition:: Today
   :class: important

   L5 found where everything else is, relative to the AV; **L6 found where
   the AV is in the world.**

   - GNSS gives an absolute position until the sky is blocked.
   - Dead reckoning bridges the gap and drifts, with the square of time for
     a gyro bias.
   - The EKF fuses them.
   - A map removes the drift (MCL, ICP).
   - Integrity checks say when the pose cannot be trusted.
   - SLAM builds the map.

- **L7, Navigation and Route Planning:** now that the AV knows its pose on
  the map, find a route to the goal.

**Before next class**

- Run the four hands-on parts (``dr``, ``ekf``, ``mcl`` and ``icp``) on
  :doc:`the Code page <l6_code>`.
- **Read the appendix** (:doc:`l6_appendix`) on ICP and the pose graph.


.. rubric:: Image credits

The vehicle icons in the figures on this page were created by Stone from the
`Noun Project <https://thenounproject.com>`_. The IMU photo is a product image of the
MS-IMU3050 by Memsense, an Inertial Labs company.
