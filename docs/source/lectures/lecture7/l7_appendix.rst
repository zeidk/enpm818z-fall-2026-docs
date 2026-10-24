====================================================
Going Further
====================================================

.. admonition:: Reading material, not covered in class
   :class: note

   This page is the written version of the deck's appendix. It is **reading
   material**: we do not present it in class, and it is **not on the quiz**.

   Each section picks up a topic from the :doc:`lecture <l7_lecture>` and
   adds definitions, sources or more numbers. The sections follow the deck's
   order. Read the one you need, when you need it. Every step of both
   searches, worked by hand, is on its own page: :doc:`l7_search_steps`.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Section**
     - **What it adds to the lecture**
   * - :ref:`l7-app-sec-route`
     - What "route" and "navigation" mean in Autoware and in ROS 2's Nav2,
       and what they mean in this course.
   * - :ref:`l7-app-sec-motion`
     - The formal definitions of a path and a trajectory, on our trip.
   * - :ref:`l7-app-sec-hdmaps`
     - What an HD map is used for, where the map fits in the AV's
       architecture, the scene model at Waymo and Tesla, where an AV's map
       comes from, and what can go wrong with an HD map.
   * - :ref:`l7-app-sec-formats`
     - The HD map formats in use, the lanelet, Lanelet2, and OpenDRIVE
       against Lanelet2.
   * - :ref:`l7-app-sec-osm`
     - The conversion from an OpenStreetMap export to a CARLA map, in
       Python.
   * - :ref:`l7-app-sec-opendrive`
     - The geometry element of ``Town01.xodr`` read attribute by attribute,
       how the file stores a road's lanes and draws a curve, and road 333's
       turn worked step by step.
   * - :ref:`l7-app-sec-segments`
     - Town01's 160 waypoint pairs, counted, and a junction element read
       attribute by attribute.
   * - :ref:`l7-app-sec-costs`
     - The top speed in all of Town01's turns, the expected wait at a traffic
       light as a cost, and the three costs in code.
   * - :ref:`l7-app-sec-searches`
     - Dijkstra and A* in words, why costs must not be negative, admissible
       and consistent heuristics, and the two searches compared on the toy
       graph.
   * - :ref:`l7-app-sec-scale`
     - Both searches on Town01's full waypoint graph, GP4's node limit, and
       how a navigation service routes a whole country.


.. _l7-app-sec-route:

Route Planning
--------------

This section continues the slide "Route planning in industry" in the
Introduction of the :doc:`lecture <l7_lecture>`.


.. _l7-app-stacks:

Route, Lane and Navigation in Other Stacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A **stack** is the full set of programs that drive the AV.

- **A route need not name the lane.** Autoware's older design page says its
  route "doesn't explicitly indicate which specific lanes to take" (Autoware
  Foundation, Planning component design). Its current mission planner (see
  the slide "Route" in the lecture) calls the route "a sequence of lanes".
  The planners after it choose the lane.
- **"Navigation" is wider in robotics.** ROS 2's Nav2 "provides perception,
  planning, control, localization, visualization, behaviors, and much more"
  (Nav2 project, Nav2 documentation). In Nav2, navigation is the whole
  stack.

.. note::

   In this course, a route names the lanes (GP4 publishes waypoints along
   them), and route planning is one module of the stack.


.. _l7-app-sec-motion:

Motion Terms
------------

This section continues the slide "Route, path and trajectory" in the
Introduction of the :doc:`lecture <l7_lecture>`. That slide names the three
motion terms; here are their formal definitions, on our trip.


.. _l7-app-path:

Path
~~~~

.. figure:: /_static/images/L7/path_panel.png
   :alt: A close top view of the route's right turn at intersection 1, x from about 77 to 117 meters east, y from minus 137 to minus 101 meters north. The route is a blue line coming from the east along y minus 129, curving through the turn and going north along x 92. Small black arrows sit on the line every few meters, each pointing the way the AV faces there: west on the straight, turning through the curve, north after it.
   :width: 55%
   :align: center

   The route's right turn at intersection 1, from above (:math:`x` east and
   :math:`y` north, in meters). The blue line is the route; each black arrow
   points the way the AV faces at that point. The light gray lines are the
   other lanes through the intersection.

.. admonition:: Definition: path
   :class: note

   A continuous function :math:`\sigma(\alpha)\colon [0, 1] \to X`, where
   :math:`X` is the configuration space of the vehicle (Paden et al.,
   2016).

A configuration is a position :math:`x`, :math:`y` in meters and a heading
:math:`\theta`. The configuration space :math:`X` is the set of all
configurations. :math:`\alpha` says how far along the path we are: it runs
from 0 at the start to 1 at the goal, and :math:`\sigma(\alpha)` is the
configuration there.

**On our trip:** :math:`\sigma(0) = (133.6, -129.4, 180^\circ)`, the start,
and :math:`\sigma(1) = (196.1, -2.0, 0^\circ)`, the goal, facing east. In
the turn at intersection 1, the arrows show :math:`\theta` swinging from
180° to 90°.

A path "does not prescribe how this path should be followed" (Paden et al.,
2016): it says where, not when, so it has no times. L9 plans a path.


.. _l7-app-trajectory:

Trajectory
~~~~~~~~~~

.. figure:: /_static/images/L7/traj_panel.png
   :alt: The same close view of the right turn at intersection 1. Black dots on the blue route, one second apart, labeled 5 s at the right end, then 6, 7, 8 s along the straight, 9 s in the turn, and 10, 11, 12 s going north. The dots are about 7 meters apart on the straight before the turn and about 3 to 4 meters apart in the turn.
   :width: 55%
   :align: center

   The same turn. Each black dot is where the AV is at the time beside it,
   from 5 s to 12 s, one second apart. The dots are farther apart on the
   straight and closer together in the turn.

.. admonition:: Definition: trajectory
   :class: note

   "a time-parametrized function :math:`\pi(t)\colon [0, T] \to X`
   prescribing the evolution of the configuration of the vehicle in time",
   where ":math:`T` is the planning horizon" (Paden et al., 2016).

:math:`T` is where the plan ends in time: how far ahead in time the plan
reaches.

**On our trip** the plan covers the whole route, with speeds chosen for this
example, from rest at the start to rest at the goal. With those speeds the AV
reaches the goal at :math:`T = 45.9` s. :math:`T` follows from the speeds; it
is not a deadline. Nobody asked the AV to arrive by then, and faster speeds
would give a smaller :math:`T`. The lecture's Edge Costs section gives this
route 31.0 s, because it leaves out starting and stopping.

The dots are :math:`\pi(5\,\text{s}), \pi(6\,\text{s}), \dots`. Before the
turn they are 7.66 m apart; in the turn, 3.41 m apart: the AV slows down to
turn. L10 follows a trajectory, and GP4 Task 2 asks you to.


.. _l7-app-sec-hdmaps:

HD Maps
-------

This section continues the slide "HD map layers" in the HD Map part of the
:doc:`lecture <l7_lecture>`'s Map to Graph section.


.. _l7-app-map-uses:

What an HD Map Is Used For
~~~~~~~~~~~~~~~~~~~~~~~~~~

Elghazaly et al. (2023) list these uses:

.. list-table::
   :widths: 20 58 22
   :header-rows: 1
   :class: compact-table

   * - **Task**
     - **How the map helps**
     - **In this course**
   * - Localization
     - "matching map data with collected sensor data in real-time"
     - L6
   * - Perception
     - "improving the accuracy and reliability of perception"
     - L4, L5
   * - Routing
     - "the calculation of efficient, feasible and safe routes"
     - L7
   * - Prediction
     - "predict the likely paths and movements of other road users"
     - L8
   * - Motion planning
     - "the planning of feasible and collision-free trajectories that
       respect traffic rules"
     - L9

.. note::

   A map covers places the sensors cannot see: "maps can offer an unlimited
   range", which helps "especially in occluded zones" (Elghazaly et al.,
   2023). For example, the map still shows the lane behind a parked truck
   that hides it from the LiDAR.


.. _l7-app-map-arch:

Where the Map Fits in the AV's Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Ulbrich et al.'s functional architecture (Ulbrich et al., 2017), the map
is the fixed part of the AV's picture of the scene:

1. Perception finds the moving things: cars, cyclists, pedestrians (L4, L5).
2. Localization puts the AV on the map (L6).
3. The map gives the scenery: roads, lanes and rules (this lecture).
4. "Dynamic elements and the scenery are associated with each other to
   obtain an environment model." With the AV's own state added, it is the
   **scene model** (Ulbrich et al., 2017).
5. Planning uses the scene model: the route in this lecture; motion
   planning in L9.

.. note::

   Situation awareness has three levels: perceive the elements, understand
   what they mean, and predict what they will do (Endsley, 1995). The map
   serves the last two: Autoware's lane map is "required for ... predicting
   the trajectories of other vehicles and pedestrians" (Autoware
   Foundation, Map, components).


.. _l7-app-scene:

The Scene Model at Waymo and Tesla
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Waymo** uses one learned model for steps 4 and 5 of the list above. Its
  encoders feed a "World Decoder", which uses these inputs "to predict other
  road users behaviors, produce high-definition maps, generate trajectories
  for the vehicle, and signals for trajectory validation" (Waymo, 2025).
- **Tesla**, as reported from a 2025 talk: one end-to-end neural network
  that learns from video, maps and kinematic data (Humanoids Daily, 2025).
  We cite no architecture published by Tesla itself.

.. note::

   "World model" has two meanings. In the scene model above, it is the AV's
   picture of the scene now. Tesla's "neural world simulator" is a model that generates new video
   of the world for training and testing (Humanoids Daily, 2025).


.. _l7-app-map-sources:

Where an AV's Map Comes From
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Someone has to make these maps first. There are four ways:

.. list-table::
   :widths: 22 20 58
   :header-rows: 1
   :class: compact-table

   * - **Source**
     - **Example**
     - **How it is made**
   * - Survey cars with LiDAR
     - Waymo
     - "our team starts by manually driving our sensor equipped vehicles down
       each street, so our custom lidar can paint a 3D picture" (Waymo, 2020)
   * - Cameras on customers' cars
     - Mobileye REM (Road Experience Management)
     - "Millions of Mobileye-equipped ADAS vehicles sending data to the cloud
       in small data packets (10kb/km)" (Mobileye, REM)
   * - Shipped with the simulator
     - CARLA, ``Town01.xodr``
     - holds the geometric and connectivity layers and part of the semantic
       layer
   * - Volunteers' street map
     - OpenStreetMap
     - streets drawn by volunteers; CARLA converts it to OpenDRIVE (in the
       lecture's Map to Graph section)


.. _l7-app-map-wrong:

What Can Go Wrong with an HD Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Elghazaly et al. (2023) list the problems of building and keeping HD maps:

- **Out of date:** the road changes, "such as construction sites, road
  blockages, and modifications of road connections". "Errors in HD maps
  could lead to severe damage due to inappropriate decisions taken by the
  system."
- **Cost:** each mapping vehicle carries "an expensive suite of mapping
  devices with high-precision sensors".
- **Time and data:** collection is "time-consuming and labour-intensive",
  and mapping vehicles "generate large quantities of data".
- **No standard:** "there is no common agreement on how mapping data are
  represented".
- **Privacy:** maps "often contain sensitive information, such as the
  locations of buildings and infrastructure".


.. _l7-app-sec-formats:

Map Formats
-----------

This section continues the slide "When the map is loaded, and when it
changes" in the HD Map part of the :doc:`lecture <l7_lecture>`'s Map to
Graph section.


.. _l7-app-formats:

HD Map Formats in Practice
~~~~~~~~~~~~~~~~~~~~~~~~~~

``Town01.xodr`` is a text file. Other formats in use:

.. list-table::
   :widths: 24 46 30
   :header-rows: 1
   :class: compact-table

   * - **Format**
     - **Stored as**
     - **Used by**
   * - ASAM OpenDRIVE, ``.xodr``
     - XML text (ASAM, OpenDRIVE)
     - CARLA, this course
   * - Lanelet2, ``.osm``
     - XML text, as in Lanelet2's example map (FZI, Lanelet2 example map)
     - Autoware (Autoware Foundation, Map, interfaces)
   * - Point cloud, ``.pcd``
     - "a single PCD file or divided into multiple PCD files" (Autoware
       Foundation, Map, components)
     - Autoware, for localization
   * - Apollo HD map
     - protobuf; Apollo looks for the binary ``base_map.bin`` before
       ``.xml`` or ``.txt`` (Baidu Apollo, Apollo source)
     - Apollo
   * - NDS.Live, a Navigation Data Standard
     - "tiles, but also along driving paths", updated "over a data
       connection" (NDS Association, NDS.Live)
     - car and map makers (NDS Association, NDS.Live)

.. note::

   OpenDRIVE and Lanelet2 are XML text; Apollo loads a binary file first,
   and NDS.Live updates "only what needs updating" (NDS Association,
   NDS.Live).


.. _l7-app-lanelet-def:

Lanelet
~~~~~~~

.. figure:: /_static/images/L7/lanelet25.png
   :alt: A top view of road 25's southbound lane, x from about 148 to 161 meters east, y from minus 48 to minus 9 meters north. Two vertical black lines with a dot at each end and an arrowhead pointing south: tag 1 on the right, at x 156, the left border; tag 2 on the left, at x 152, the right border. The light shaded strip between them is tag 3, the drivable area.
   :width: 28%
   :align: center

   Road 25's southbound lane as a lanelet, from above (:math:`x` east and
   :math:`y` north, in meters). **1:** its left border. **2:** its right
   border. **3:** the drivable area between them. Each border is two points,
   and its arrowhead points south, the way the lane drives.

.. admonition:: Definition: lanelet
   :class: note

   "A Lanelet represents one *atomic* section of a lane. Atomic means that
   along a Lanelet, traffic rules (including possible lane changes to other
   Lanelets) do not change" (FZI, Lanelet2 primitives).

"A Lanelet consists of exactly one left and exactly one right Linestring.
Together they form the drivable area of the Lanelet" (FZI, Lanelet2
primitives). A **linestring** is "an ordered list of points with linear
interpolation in between" (FZI, Lanelet2 primitives): the points are joined
by straight lines.

**In Town01:** road 25's southbound lane as a lanelet. Seen by an AV
driving south, its left border **1** is the road's reference line, its right
border **2** is 4.0 m west, and **3** is the drivable area. The road is straight, so each border is two
points.


.. _l7-app-lanelet2:

Lanelet2
~~~~~~~~

Autoware's map "must be in Lanelet2 format, with additional modifications
required by Autoware" (Autoware Foundation, Map, components). **Lanelet2**
(Poggenhans et al., 2018) builds a map from lanelets: it stores each lane by
its two borders, instead of as an offset from a road's reference line.
"Regulatory elements are a generic way to express traffic rules. They are
referenced by Lanelets or areas for which they apply" (FZI, Lanelet2
primitives).

.. note::

   The rest of the lecture uses OpenDRIVE through CARLA.


.. _l7-app-lanelet:

OpenDRIVE against Lanelet2
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * -
     - **OpenDRIVE**
     - **Lanelet2**
   * - a lane is
     - an offset from a road's reference line (lines, arcs in Town01)
     - the area between a left and a right linestring (FZI, Lanelet2
       primitives)
   * - traffic rules
     - signals placed along a road
     - regulatory elements, referenced by lanelets (FZI, Lanelet2
       primitives)
   * - file
     - XML, ``.xodr`` (ASAM, OpenDRIVE)
     - read and written through an IO interface, for example OSM files
   * - used by
     - CARLA (this course)
     - Autoware

.. note::

   For routing, both give the same graph: lanes as nodes or chains of nodes,
   "this lane leads to that one" as edges, and a cost per edge.


.. _l7-app-sec-osm:

OpenStreetMap
-------------

This section continues the slide "A map of your own, from OpenStreetMap" in
the From Map File to Graph part of the :doc:`lecture <l7_lecture>`'s Map to
Graph section.


.. _l7-app-osm-code:

From Your .osm File to a Map, in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   osm = open("maps/umd_engineering.osm").read()
   settings = carla.Osm2OdrSettings()
   settings.proj_string = ("+proj=tmerc +lat_0=38.99 +lon_0=-76.939"
                           " +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m")
   settings.center_map = False      # keep its origin
   settings.use_offsets = False
   xodr = carla.Osm2Odr.convert(osm, settings)  # OpenDRIVE text
   m = carla.Map("campus", xodr)    # a map object

``proj_string`` sets how latitude and longitude become meters: x = 0, y = 0
is at latitude 38.99, longitude −76.939. With ``center_map`` on, the
converter would move the origin to the center of the road map, and
``use_offsets`` would shift it too. Both stay off, so the origin stays where
``proj_string`` puts it.

In class we run this code on the copy of the ``.osm`` file in the course
package, not on the file you just exported. ``osm_to_map.py``, in the folder
``lecture7``, does it for any export:

.. code-block:: bash

   python3 osm_to_map.py <location of map.osm>


.. _l7-app-sec-opendrive:

OpenDRIVE
---------

This section continues the slide "One road in Town01.xodr" in the From Map
File to Graph part of the :doc:`lecture <l7_lecture>`'s Map to Graph
section.


.. _l7-app-odr-geometry:

Reading a Geometry Element
~~~~~~~~~~~~~~~~~~~~~~~~~~

Road 25's ``<geometry>`` (**4** in the lecture's listing) draws its
**reference line**, the line the file draws the road along. Lanes are
numbered from it: 1 on its left (driving north here), −1 on its right
(driving south).

.. list-table::
   :widths: 14 40 46
   :header-rows: 1
   :class: compact-table

   * - **Attribute**
     - **ASAM's definition** (ASAM, Road reference line)
     - **Road 25**
   * - ``s``
     - "s-coordinate of start position" (m)
     - 0: the piece starts where the road starts; :math:`s` is the distance
       along the reference line
   * - ``x``, ``y``
     - "Start position (x inertial)", "(y inertial)" (m)
     - (156.07, −11.02), in the map frame: :math:`x` east, :math:`y` north
   * - ``hdg``
     - "Start orientation (inertial heading)" (rad)
     - −1.572 rad, measured counterclockwise from east
   * - ``length``
     - "Length of the element's reference line" (m)
     - 35.18

1. The heading in degrees: −1.572 × 180 / π = −90.07°, so the line points
   south.
2. The end, 35.18 m later: x = 156.07 + 35.18 cos(−90.07°) = 156.03 m and
   y = −11.02 + 35.18 sin(−90.07°) = −46.20 m. That point is junction 332.


.. _l7-app-odr-lanes:

A Road's Lanes in Town01.xodr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Road 25, shortened (numbers rounded, attributes cut). The highlighted lines
are the ones the list below explains.

.. code-block:: xml
   :emphasize-lines: 3,6,7,10,11,12,13

   <lanes>
     <laneSection s="0">
       <left>
         <lane id="3" type="sidewalk"> ...
         <lane id="2" type="shoulder"> ...
         <lane id="1" type="driving">
           <width sOffset="0" a="4.0"/>
         </lane>
       </left>
       <center> ... </center>
       <right>
         <lane id="-1" type="driving">
           <width sOffset="0" a="4.0"/>
         </lane>
         <lane id="-2" type="shoulder"> ...
         <lane id="-3" type="sidewalk"> ...

- **1** (``<left>``, ``<center>`` and ``<right>``): lanes are numbered out
  from the reference line: positive on its left, negative on its right, 0
  the line itself.
- **2** (each ``<lane ... type="driving">``): each lane has a type; only
  ``driving`` lanes enter the routing graph.
- **3** (each ``<width .../>``): a width polynomial in :math:`s`, the
  distance along the reference line. Here it is a constant 4.0 m.
- In this file, lane −1 is marked ``travelDir="forward"`` (along the line)
  and lane 1 ``"backward"``.


.. _l7-app-odr-curve:

How the Map Draws a Curve
~~~~~~~~~~~~~~~~~~~~~~~~~

Road 333, shortened from the file: numbers rounded; ``s``, ``x``, ``y`` and
``hdg`` cut.

.. code-block:: xml

   <road id="333" junction="332">
    <planView>
     <geometry length="3.08">
      <line/>
     </geometry>
     <geometry length="6.45">
      <arc curvature="-0.1216"/>
     </geometry>
     <geometry length="6.45">
      <arc curvature="-0.1216"/>
     </geometry>
     <geometry length="2.81">
      <line/>
     </geometry>
    </planView>

Road 333 is the right turn from road 25 inside junction 332.

- **1** (the first ``<geometry>``): a reference line is a chain of pieces:
  lines, arcs and spirals. Town01 uses only lines and arcs.
- **2** (the first ``<arc>``): an arc has a constant **curvature**
  :math:`\kappa`, in 1/m: how sharply it bends. Its radius is
  :math:`r = 1/|\kappa|`. A negative :math:`\kappa` is a "right curve
  (clockwise motion)" (ASAM, OpenDRIVE 1.9.0, Section 9).
- A spiral's curvature changes "linear from the start to the end", so a line
  can lead into an arc "without causing leaps in the curvature" (ASAM,
  OpenDRIVE 1.9.0, Section 9).


.. _l7-app-road333:

Road 333's Turn, Step by Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the file: two arcs, each 6.45 m long, with curvature −0.1216 per meter
(the arc marked **2** above).

1. Radius of the reference line: :math:`r` = 1 / 0.1216 = 8.22 m.
2. Each arc turns the line by its length times its curvature:
   6.45 × 0.1216 = 0.784 rad. The two together: 2 × 0.784 = 1.57 rad, about
   90°.
3. The AV drives the middle of lane −1. The lane is 4.0 m wide, so its
   middle is 2.0 m right of the line, on the inside of the turn: radius
   8.22 − 2.0 = 6.22 m.

.. note::

   The lecture's Edge Costs section does the same for road 312, our trip's
   right turn at intersection 1: 7.67 − 2.00 = 5.67 m.


.. _l7-app-sec-segments:

Segments and Junctions
----------------------

This section continues the slides "CARLA cuts every lane at the
intersections" and "A junction lists which lane leads to which" in the From
Map File to Graph part of the :doc:`lecture <l7_lecture>`'s Map to Graph
section.


.. _l7-app-pairs:

Town01's 160 Waypoint Pairs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``get_topology()`` returns 160 pairs of waypoints for Town01, one pair per
segment and way out. Counted from the map:

1. Outside the intersections: 26 roads with one lane each way, so 26 × 2 =
   52 lanes.
2. 36 of those lanes end where the AV can go two ways, so each is listed
   twice, once for each lane it leads into: 52 + 36 = 88 pairs. Segment
   **1** of the lecture's slide "CARLA cuts every lane at the intersections"
   is one of them.
3. Through the intersections: 72 segments, 24 left turns, 24 right turns and
   24 straight on. So 88 + 72 = 160 pairs, for 52 + 72 = 124 segments.


.. _l7-app-junction-el:

Reading a Junction Element
~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is junction 332's first connection, attribute by attribute, as ASAM
OpenDRIVE defines them (ASAM, Junctions and connecting roads):

.. list-table::
   :widths: 22 32 46
   :header-rows: 1
   :class: compact-table

   * - **Attribute**
     - **ASAM's definition**
     - **In junction 332**
   * - ``junction id``
     - the junction's ID
     - 332; the roads inside it say ``junction="332"``
   * - ``connection id``
     - "Unique ID within the junction"
     - 0
   * - ``incomingRoad``
     - "ID of the incoming road"
     - 25: the road that leads into the junction
   * - ``connectingRoad``
     - "ID of the connecting road": a path across the junction
     - 333: a short road inside the junction, the right turn
   * - ``contactPoint``
     - "Contact point on the @connectingRoad"
     - ``start``: road 333 begins where road 25 ends, so traffic drives it
       from its :math:`s = 0`
   * - ``laneLink from``
     - "ID of the incoming lane"
     - −1: road 25's lane −1, driving south
   * - ``laneLink to``
     - "ID of the connection lane"
     - −1: road 333's lane −1

So, from road 25's lane −1, the AV may drive on into lane −1 of road 333,
the right turn. Connection 3 does the same for road 339, the left turn.


.. _l7-app-sec-costs:

Edge Costs
----------

This section continues the slides "The radius from the waypoints" and
"Routes under three costs" in the Edge Costs section of the
:doc:`lecture <l7_lecture>`.


.. _l7-app-turn-speed:

Top Speed in Town01's Turns
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/turn_speed.png
   :alt: A graph, not a map: top speed in meters per second against the curve's radius in meters, 0 to 90. A solid dark curve rises from 0 and becomes flat at about 11.2 meters per second from a radius of about 62 meters on. Dots on it: tag 1 at radius 7.2 and speed 3.8, tag 2 at radius 11.5 and speed 4.8, tag 3 where it becomes flat. Tag 4 points at the flat part. A dotted gray line marks 11.18 meters per second across the graph, and a dashed gray curve, tag 5, keeps rising above the flat part.
   :width: 75%
   :align: center

   A graph, not a map: the top speed (m/s) against the curve's radius
   :math:`r` (m). **1** and **2** the median right and left turns. **3**
   :math:`\sqrt{2.0\, r}` meets the speed limit at
   :math:`r = 11.18^2 / 2.0 = 62.5` m. **4** the speed limit, above 62.5 m.
   **5** :math:`\sqrt{2.0\, r}` alone (dashed).

1. The limit on sideways acceleration: :math:`a_{\mathrm{lat}} = 2.0` m/s²,
   chosen for this example.
2. **1** In Town01's 24 right-turn lanes, the median edge radius is 7.2 m:
   √(2.0 × 7.2) = √14.4 = 3.79 m/s.
3. **2** In its 24 left-turn lanes, it is 11.5 m: √(2.0 × 11.5) = √23 =
   4.80 m/s.
4. On a straight lane, the AV drives at the speed limit, 11.18 m/s.

The solid line is the top speed: the lower of :math:`\sqrt{2.0\, r}` and the
speed limit (dotted).

.. note::

   **Travel time of an edge:** its length divided by the lower of the speed
   limit and the curve's top speed. A meter of the median left turn takes
   11.18 / 4.80 = 2.3 times as long as a straight meter; a meter of the
   median right turn, 11.18 / 3.79 = 2.9 times.


.. _l7-app-lights:

Traffic Lights Add Waiting Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Town01.xodr`` has 36 traffic lights. With travel time as the cost, an edge
through a light can add the time the AV expects to wait there.

**An example**, with a light chosen for it: red for 30 s of every 60 s.

1. The AV arrives at a random moment, so it meets red 30 / 60 = 0.5 of the
   time.
2. Arriving during red, it waits half the red on average: 30 / 2 = 15 s.
3. Expected wait at this light: 0.5 × 15 = 7.5 s.

.. note::

   With waits in the cost, a longer route through fewer lights can be the
   fastest. In GP4 the behavior node, not the planner, stops at red: it
   reads the light's state on ``/traffic/light_state``.


.. _l7-app-costcode:

The Three Costs in Code
~~~~~~~~~~~~~~~~~~~~~~~

The costs in the lecture's Edge Costs section were computed this way, for
all 3143 edges at once: edge ``i`` goes from node ``ef[i]`` to node
``et[i]`` and is ``el[i]`` meters long.

.. code-block:: python

   turn = np.radians(wrap_deg(yaw[et] - yaw[ef]))  # rad
   kappa = np.abs(turn) / el          # curvature: 1 / radius
   kappa = np.maximum(kappa, 1e-12)   # never exactly 0
   v = np.minimum(v_limit, np.sqrt(a_lat / kappa))  # m/s
   cost_distance = el                           # 1. meters
   cost_time = el / v                           # 2. seconds
   cost_left = el + np.where(is_left, P, 0.0)   # 3. meters

- ``yaw`` holds each node's heading in degrees, and ``wrap_deg`` brings a
  change of heading into −180 to 180 degrees.
- ``v_limit`` is the speed limit, 11.18 m/s (25 mph); ``a_lat`` is
  2.0 m/s² and ``P`` is 30 m, both chosen.
- A straight edge has ``kappa`` 0. ``np.maximum`` keeps the division finite,
  so the speed limit sets ``v``.
- ``is_left`` is true on the first edge of each left turn, so a left turn
  adds ``P`` once.


.. _l7-app-sec-searches:

Searches
--------

This section is the recap that the :doc:`lecture <l7_lecture>`'s Search
section points to. You know Dijkstra and A* from the planning course, so
their recap is here, in words and numbers. Every
step of both searches on the toy graph is on :doc:`l7_search_steps`.

**S** is the trip's start node and **G** its goal node. The **toy graph**
has S, G and seven intersections, 1 to 7, as its nodes, and the roads
between them as edges, each with its length in meters. It is drawn in
:ref:`l7-steps-toy`.


.. _l7-app-search-recap:

Dijkstra and A*
~~~~~~~~~~~~~~~

Both searches build routes out from S until they reach G.

.. admonition:: Definition: heuristic, :math:`h(n)`
   :class: note

   An estimate of the cost from node :math:`n` to the goal, in the same units
   as the edge costs, computed without searching.

Each node :math:`n` keeps :math:`g(n)`, the cost of the cheapest route from S
to :math:`n` found so far. The **open set** holds the nodes reached but not
yet taken.

1. S goes in the open set, with :math:`g = 0`.
2. Take the open node with the lowest score: :math:`g` for **Dijkstra**,
   :math:`f = g + h` for **A***. If the open set is empty, there is no route.
3. If the node taken is G, stop.
4. For each neighbor not yet taken: if the route through the taken node is
   cheaper than the neighbor's :math:`g` (or it has none), set its :math:`g`
   to that cost, note where it came from, and put it in the open set. Go back
   to step 2.
5. The route: follow the "came from" notes from G back to S.

With :math:`h = 0` at every node, A* is Dijkstra.


.. _l7-app-negative:

Edge Costs Must Not Be Negative
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dijkstra is sure to find the cheapest route if no edge cost is negative.

.. figure:: /_static/images/L7/negative_edge.png
   :alt: Three nodes S, A and B. An arrow from S to A labeled 2, an arrow from S to B labeled 5, and an arrow from B to A labeled minus 4.
   :width: 40%
   :align: center

   Three nodes. The edge from S to A costs 2, the edge from S to B costs 5,
   and the edge from B to A costs −4.

The costs are chosen for this example. Dijkstra always takes the cheapest
open node and treats its cost as final.

1. From S, A costs 2 and B costs 5. A is cheaper, so Dijkstra takes A and
   fixes its cost at 2.
2. Next, Dijkstra takes B, at 5. Through B, A would cost 5 − 4 = 1, less
   than 2.

A is already taken, so Dijkstra keeps 2, the wrong cost. Dijkstra assumes
that adding an edge to a route never makes it cheaper, and a negative edge
breaks that.

.. note::

   Distance, time and penalties are never negative, so every cost in this
   lecture is safe. To favor a road, give it a smaller positive cost, never a
   negative one.


.. _l7-app-admissible:

An Admissible Heuristic Never Overestimates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Whether A* still finds the cheapest route depends on :math:`h`. A* is sure
to find the cheapest route if its :math:`h` never guesses too high:

.. admonition:: Definition: admissible heuristic
   :class: note

   :math:`h` is admissible if, for every node :math:`n`, :math:`h(n)` is no
   more than the true cost of the cheapest route from :math:`n` to the goal.
   With an admissible :math:`h`, A* returns a cheapest route, if it may take
   a node again when it finds a cheaper way to it; the straight line never
   needs that (:ref:`l7-app-consistent`).

**Why it matters:** A* stops when it takes G. If :math:`h` guesses too high
at a node on the best route, that node looks worse than it is, and A* can
reach G another way first. :ref:`l7-app-overestimate` below shows this with
:math:`h(5) = 150`.

**The straight line is admissible for distance:** every road from :math:`n`
to G is at least as long as the straight line between them. On the toy
graph:

.. list-table::
   :widths: 28 8 8 8 8 8 8 8 8 8
   :header-rows: 1
   :class: compact-table

   * -
     - **S**
     - **1**
     - **2**
     - **3**
     - **4**
     - **5**
     - **6**
     - **7**
     - **G**
   * - :math:`h`, straight line (m)
     - 142
     - 165
     - 221
     - 117
     - 105
     - 66
     - 40
     - 149
     - 0
   * - cheapest route to G (m)
     - 273
     - 232
     - 299
     - 157
     - 106
     - 93
     - 40
     - 272
     - 0

The top row is :math:`h` and the bottom row is the true cost. In every
column, the top is at most the bottom. The closest is node 4: 105 against
106.

For S: :math:`h = \sqrt{62.5^2 + 127.4^2} = 141.9`, rounded to 142. The
cheapest route is 41 + 75 + 64 + 53 + 40 = 273, so 142 is well below it.


.. _l7-app-compare:

Dijkstra against A* on the Toy Graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every step of both searches is on :doc:`l7_search_steps`.

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * -
     - **Dijkstra**
     - **A***
   * - route
     - S, 1, 3, 5, 6, G
     - S, 1, 3, 5, 6, G
   * - cost
     - 273 m
     - 273 m
   * - nodes taken
     - 8: S, 1, 2, 3, 4, 5, 6, G
     - 6: S, 1, 3, 5, 6, G

- **Node 2:** :math:`g` = 41 + 67 = 108, :math:`f` = 108 + 221 = 329. A*
  took G at :math:`f` = 273 first, so it never took node 2.
- **Node 4:** :math:`g` = 41 + 75 + 55 = 171, :math:`f` = 171 + 105 = 276,
  just above 273, so A* skipped it too. The route through 4 is
  171 + 66 + 40 = 277 m.
- Dijkstra took 2 and 4 because their :math:`g` (108 and 171) is below 273.
  It never took 7 (:math:`g` = 359).


.. _l7-app-overestimate:

An Overestimating Heuristic
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Imagine :math:`h(5) = 150` (chosen for this example), while the true cost
from 5 to G is 53 + 40 = 93. Every other :math:`h` stays the straight line.
Node 5, reached at :math:`g` = 41 + 75 + 64 = 180 m, then looks worse than it
is: :math:`f` = 180 + 150 = 330 instead of 180 + 66 = 246.

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * -
     - :math:`h` **admissible**
     - :math:`h(5) = 150`
   * - route
     - S, 1, 3, 5, 6, G
     - S, 1, 3, 4, 6, G
   * - cost
     - 273 m
     - 277 m
   * - nodes taken
     - 6
     - 6

With node 5 at :math:`f` = 330, A* takes node 4 (:math:`f` = 276) first and
takes G through 4 at 277, before it takes node 5: a route 4 m longer.

.. note::

   GP4's planner stub warns: "An inadmissible heuristic still returns a
   path, just not the shortest, and nothing reports the difference."


.. _l7-app-time-h:

For Travel Time, h Must Be in Seconds Too
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Divide the straight line by the highest speed on any road:

.. math::

   h(n) = \frac{\text{straight line from } n \text{ to G}}{v_{\max}}, \qquad
   v_{\max} = 11.18\text{ m/s in Town01}

No route can be faster than driving the straight line at the top speed, so
this :math:`h` is admissible.

**Measured on the full waypoint graph**, with travel-time costs:

- :math:`h` in seconds, as above: the fastest route, 27.7 s, through 4.
- :math:`h` left in meters (the units mistake): every :math:`h` is 11.18
  times too large. A* returns the route through 5: 31.0 s,
  31.0 − 27.7 = 3.3 s slower, and reports nothing.


.. _l7-app-check-h:

Check: Heuristics
~~~~~~~~~~~~~~~~~

**Question.** A team uses :math:`h(n)` = the distance from :math:`n` to G
along the :math:`x` axis plus the distance along the :math:`y` axis (the
"city block" distance), with distance costs. Town01's streets run east-west
and north-south. Is this :math:`h` admissible?

.. dropdown:: Answer
   :class-container: sd-border-success

   **No.** In a turn, the lane curves inside the corner, so it is shorter
   than the two straight legs. Measured on Town01's waypoint graph, with our
   G: the city block distance is more than the true cost at 560 of the 3107
   nodes, by up to 14.5 m. The straight line is never more than the true
   cost.


.. _l7-app-final:

Why a Taken Node's Cost Is Final
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dijkstra takes node :math:`u` with the lowest :math:`g` in the open set.
Suppose some route :math:`R` from S to :math:`u` were cheaper than
:math:`g(u)`.

1. :math:`R` starts at S, which is taken. Follow :math:`R` until its first
   node :math:`v` that is not taken. The node before :math:`v` was taken
   before :math:`u`, so its cost is final (this same argument, one node
   earlier) and its road to :math:`v` was checked: the open set holds for
   :math:`v` a cost no more than :math:`R`'s cost up to :math:`v`.
2. The rest of :math:`R`, from :math:`v` to :math:`u`, has no negative
   edges, so :math:`R`'s cost up to :math:`v` is no more than :math:`R`'s
   whole cost.
3. So :math:`g(v) \le \text{cost}(R) < g(u)`: :math:`v` has a lower
   :math:`g` than :math:`u`, and Dijkstra would have taken :math:`v` first.
   That is a contradiction, so no cheaper :math:`R` exists.

.. note::

   Step 2 is where a negative edge breaks the proof: with the −4 of
   :ref:`l7-app-negative`, the rest of a route can lower its cost.


.. _l7-app-consistent:

Admissible and Consistent
~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: consistent heuristic
   :class: note

   For every edge from :math:`n` to :math:`m`:
   :math:`h(n) \le \text{cost}(n, m) + h(m)`, and
   :math:`h(\text{goal}) = 0`.

- A consistent :math:`h` is admissible: add the inequality along any route
  from :math:`n` to the goal.
- With a consistent :math:`h`, a node A* takes has its final :math:`g`, as
  in Dijkstra; with an :math:`h` that is only admissible, A* may have to
  take a node again.
- The straight line is consistent: the straight line from :math:`n` to G is
  no longer than the road from :math:`n` to :math:`m` plus the straight line
  from :math:`m` to G.

On the toy graph (rounded meters), the tightest edges are 4 to 6,
where 105 ≤ 66 + 40 = 106, and 6 to G, where 40 ≤ 40 + 0. Every other edge
has more room.


.. _l7-app-sec-scale:

At Scale
--------

This section is the material that the :doc:`lecture <l7_lecture>`'s At Scale
section points to. It runs the same two searches on Town01's full waypoint
graph, 3107 nodes, to show how much work A*'s heuristic saves on a real map,
and why GP4 stops a search after ``max_astar_nodes``, 10,000 nodes.


.. _l7-app-scale:

Our Trip on the Waypoint Graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same two searches, on all 3107 nodes of Town01, run in advance by a
reference planner:

.. figure:: /_static/images/L7/scale_search.png
   :alt: Two top views of Town01's lanes side by side, each with the trip's route as a blue line from S to G and the nodes the search took as amber dots. Left, Dijkstra, 543 nodes taken: amber spreads in every direction from the route, south along the left street to the bottom of the town, west along the top street to the town's edge, and east along two cross streets. Right, A*, 196 nodes taken: amber covers the route and only short stubs off it, near intersections 1 and 3 and east of 5.
   :width: 100%
   :align: center

   Town01's lanes (light gray) with the trip's route (blue) from S to G and,
   in amber, the nodes each search took. Left, Dijkstra, 543 nodes: amber
   reaches the bottom of the town, the west end of the top street and two
   cross streets. Right, A*, 196 nodes: amber stays on the route, with short
   stubs off it.

Distance costs, the same route for both: 260.6 m. Nodes taken from the open
set, the goal included: Dijkstra 543, A* 196, which is 196 / 543 = 36% of
Dijkstra's.


.. _l7-app-node-limit:

Travel Time and GP4's Node Limit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each search for our trip, with distance or travel-time costs:

.. list-table::
   :widths: 28 32 20 20
   :header-rows: 1
   :class: compact-table

   * - **Cost, search**
     - **h**
     - **Nodes taken**
     - **Route**
   * - distance, Dijkstra
     - 0
     - 543
     - 260.6 m
   * - distance, A*
     - straight line (m)
     - 196
     - 260.6 m
   * - time, Dijkstra
     - 0
     - 524
     - 27.7 s
   * - time, A*
     - straight line / 11.18 (s)
     - 236
     - 27.7 s
   * - time, A*, wrong units
     - straight line (m)
     - 175
     - 31.0 s

.. important::

   **GP4 caps the search** at ``max_astar_nodes: 10000`` and asks that the
   planner "does not crash on no-path scenarios". Town01 has 3107 nodes, so
   a correct search takes at most 3107: reaching 10000 means a bug. A search
   with no route ends when the open set is empty. In both cases your node
   must report that no route was found, and keep running.


.. _l7-app-country:

Routing a Whole Country
~~~~~~~~~~~~~~~~~~~~~~~

Town01's graph has 3107 nodes. A navigation service answers many requests on
one much larger road graph, so it prepares the graph once, in advance, and
each request then searches far fewer nodes.

- **Contraction hierarchies** (Geisberger et al., 2008): the nodes are
  ranked, and shortcut edges are added that skip the lower-ranked ones. A
  request then searches from both ends, toward higher-ranked nodes only.
- **OSRM**, a "high performance routing engine written in C++ designed to
  run on OpenStreetMap data", offers contraction hierarchies and Multi-Level
  Dijkstra, and its README recommends the latter for most uses (Project
  OSRM, osrm-backend README).

.. note::

   On Town01, A* took 196 nodes for our trip: no preparation needed. GP4
   asks for A*.


Sources for This Page
---------------------

The full reading list for the lecture is in :doc:`l7_references`. This page
cites:

- Autoware Foundation (2026). `Planning component design (Autoware
  architecture v1, components)
  <https://docs.autoware.org/main/design/autoware-architecture-v1/components/planning/>`_.
  Accessed 2026-10-16.
- Nav2 project (2026). `Nav2 documentation
  <https://docs.nav2.org/rolling/index.html>`_. Accessed 2026-10-16.
- Paden, B., Čáp, M., Yong, S. Z., Yershov, D. and Frazzoli, E. (2016). "A
  Survey of Motion Planning and Control Techniques for Self-Driving Urban
  Vehicles." *IEEE Transactions on Intelligent Vehicles*, 1(1), 33 to 55.
- Elghazaly, G., Frank, R., Harvey, S. and Safko, S. (2023).
  "High-Definition Maps: Comprehensive Survey, Challenges, and Future
  Perspectives." *IEEE Open Journal of Intelligent Transportation Systems*,
  4, 527 to 550. doi:10.1109/OJITS.2023.3295502.
- Waymo (2020). `The Waymo Driver Handbook: How our highly-detailed maps
  help unlock new locations for autonomous driving
  <https://waymo.com/blog/2020/09/the-waymo-driver-handbook-mapping/>`_.
  Accessed 2026-10-17.
- Mobileye (2026). `REM: Road Experience Management
  <https://www.mobileye.com/technology/rem/>`_. Accessed 2026-10-17.
- Ulbrich, S., Reschka, A., Rieken, J., Ernst, S., Bagschik, G., Dierkes,
  F., Nolte, M. and Maurer, M. (2017). "Towards a Functional System
  Architecture for Automated Vehicles." arXiv:1703.08557.
- Endsley, M. R. (1995). "Toward a Theory of Situation Awareness in Dynamic
  Systems." *Human Factors*, 37(1), 32 to 64.
- Autoware Foundation (2026). `Map (Autoware architecture v1, components)
  <https://docs.autoware.org/main/design/autoware-architecture-v1/components/map/>`_.
  Accessed 2026-10-14.
- Autoware Foundation (2026). `Map (Autoware architecture v1, interfaces)
  <https://docs.autoware.org/main/design/autoware-architecture-v1/interfaces/components/map/>`_.
  Accessed 2026-10-22.
- Waymo (2025). `Demonstrably Safe AI For Autonomous Driving
  <https://blog.waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving>`_.
  Accessed 2026-10-22.
- Humanoids Daily (2025). `Tesla AI Chief Details Unified World Simulator
  for FSD and Optimus
  <https://www.humanoidsdaily.com/feed/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus>`_.
  Accessed 2026-10-22.
- ASAM e.V. (2026). `ASAM OpenDRIVE
  <https://www.asam.net/standards/detail/opendrive/>`_. Accessed
  2026-10-14.
- ASAM e.V. (2026). `ASAM OpenDRIVE 1.9.0 Specification, Section 9.2: Road
  reference line
  <https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/v1.9.0/specification/09_geometries/09_02_road_reference_line.html>`_
  (Table 18, attributes of the geometry element). Accessed 2026-10-22.
- ASAM e.V. (2026). `ASAM OpenDRIVE 1.9.0 Specification, Sections 12.2 and
  12.4: Common junctions, Connecting roads
  <https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/v1.9.0/specification/12_junctions/12_04_connecting_roads.html>`_
  (Tables 56, 61 and 62: attributes of connection and laneLink). Accessed
  2026-10-22.
- ASAM e.V. (2026). `ASAM OpenDRIVE 1.9.0 Specification, Section 9:
  Geometries
  <https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/v1.9.0/specification/09_geometries/09_05_arc.html>`_
  (Sections 9.4 Spiral and 9.5 Arc). Accessed 2026-10-22.
- FZI Forschungszentrum Informatik (2026). `Lanelet2: Lanelet primitives
  (documentation)
  <https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_core/doc/LaneletPrimitives.md>`_.
  Accessed 2026-10-14.
- FZI Forschungszentrum Informatik (2026). `Lanelet2 example map,
  lanelet2_maps/res/mapping_example.osm
  <https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_maps/res/mapping_example.osm>`_.
  Accessed 2026-10-22.
- Poggenhans, F., Pauls, J.-H., Janosovits, J., Orf, S., Naumann, M., Kuhnt,
  F. and Mayr, M. (2018). "Lanelet2: A High-Definition Map Framework for the
  Future of Automated Driving." ITSC, 1672 to 1679.
- Baidu Apollo (2026). `Apollo source: config_gflags.cc (base_map_filename)
  and hdmap_impl.cc (LoadMapFromFile)
  <https://github.com/ApolloAuto/apollo>`_. Accessed 2026-10-22.
- NDS Association (2026). `What is NDS? NDS.Live
  <https://nds-association.org/>`_. Accessed 2026-10-22.
- Geisberger, R., Sanders, P., Schultes, D. and Delling, D. (2008).
  "Contraction Hierarchies: Faster and Simpler Hierarchical Routing in Road
  Networks." *Experimental Algorithms*, Lecture Notes in Computer Science,
  Springer, 319 to 333.
- Project OSRM (2026). `osrm-backend README
  <https://github.com/Project-OSRM/osrm-backend/blob/master/README.md>`_.
  Accessed 2026-10-17.
