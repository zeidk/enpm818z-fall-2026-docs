====================================================
Code
====================================================

The L7 hands-on is the folder ``lecture7/`` of
`enpm818z-fall-2026-carla-python
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture7>`_.
Every part follows **one trip in CARLA's Town01**, the same trip the lecture
uses: from S, the start, to G, the goal. The folder has three scripts:

- ``l7_handson.py``: the five hands-on parts, each in its own matplotlib
  window.
- ``read_map.py``: the code on the slide "Read the map file yourself, with
  no CARLA server". It prints three counts and opens no window.
- ``osm_to_map.py``: the code on the appendix slide "From your .osm file to
  a map, in Python" (:doc:`Going Further <l7_appendix>`). It turns an
  OpenStreetMap export into a CARLA map.

You need Python with ``numpy`` and ``matplotlib``. You need **no CARLA
server, no ROS and no GPU**. The ``map`` part, ``read_map.py`` and
``osm_to_map.py`` also need CARLA's Python package, which reads a map file on
its own, without a server.

.. important::

   **This folder has no search code.** A reference planner that is not
   public computed the routes, and the order in which Dijkstra and A* took
   nodes from their open sets, in advance. They are saved in ``l7_results/``.
   ``l7_handson.py`` replays and draws them. GP4 Task 1 asks you to write A*
   on CARLA's waypoint graph yourself.

.. list-table::
   :widths: 14 40 46
   :header-rows: 1
   :class: compact-table

   * - **Part**
     - **What it shows**
     - **Lecture slide**
   * - ``map``
     - Town01's map file: zoom, search, click
     - "Hands-on: the map file" and "In class: find our start in the map
       file" (Map to Graph)
   * - ``graph``
     - Town01's waypoint graph: 3107 nodes and 3143 edges
     - "Hands-on: Town01's graph" (Map to Graph)
   * - ``costs``
     - every edge's three costs, and the trip's route under each
     - "Hands-on: the edge costs" (Edge Costs)
   * - ``search``
     - Dijkstra and A*, replayed with a slider
     - "Hands-on: the trip, from graph to route" (Maneuvers); the numbers
       are in :ref:`l7-app-sec-scale` of :doc:`Going Further <l7_appendix>`
   * - ``replan``
     - an obstacle on the route, and the new route
     - "An obstacle on the road from 5 to 6" (Re-planning)


Run It
------

Get the repository, then go to the folder:

.. code-block:: bash

   git clone https://github.com/rubixcubic/enpm818z-fall-2026-carla-python.git
   cd enpm818z-fall-2026-carla-python/lecture7

Install CARLA's Python package. It reads ``Town01.xodr`` with no CARLA
server running:

.. code-block:: bash

   pip install carla==0.9.16

Each part opens a matplotlib window:

.. code-block:: bash

   python3 l7_handson.py --part map      # 0. Town01's map file: zoom, search, click
   python3 l7_handson.py --part graph    # 1. Town01's waypoint graph; scroll to zoom, drag to pan
   python3 l7_handson.py --part costs    # 2. every edge's three costs, and the trip's route under each
   python3 l7_handson.py --part search   # 3. Dijkstra and A*, replayed with a slider
   python3 l7_handson.py --part replan   # 4. an obstacle on the route, and the new route

   # save a still instead of opening a window
   python3 l7_handson.py --part graph --snapshot graph.png


Options
~~~~~~~

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Option**
     - **What it does**
   * - ``--part map|graph|costs|search|replan``
     - Which part to run. Required.
   * - ``--snapshot FILE``
     - Saves the figure as a PNG file instead of opening a window.
   * - ``--html FILE``
     - Saves the figure as an HTML page instead of opening a window. It needs
       the ``mpld3`` package (``pip install mpld3``); without it, the script
       stops and suggests ``--snapshot``.


The Two Scripts from the Slides
-------------------------------

Read the Map File: ``read_map.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the code of the slide "Read the map file yourself, with no CARLA
server". CARLA's Python package reads an OpenDRIVE file on its own (CARLA
Team, Python API reference):

.. code-block:: python

   import carla
   text = open("maps/Town01.xodr").read()
   m = carla.Map("Town01", text)      # no server needed
   wps = m.generate_waypoints(2.0)    # every 2 m, every lane
   segs = m.get_topology()            # (start, end) waypoint pairs

``maps/Town01.xodr`` is CARLA 0.9.16's map file for Town01, unchanged.
``generate_waypoints(2.0)`` puts a point every 2 m along the middle of every
lane. ``get_topology()`` returns a list of (start, end) waypoint pairs: each
pair is one lane of one road, listed once for each lane it can lead into. The
script also counts the traffic lights: the
``<signal>`` elements of type 1000001, OpenDRIVE's code for a traffic light.

Run it from ``lecture7/``. It takes no options:

.. code-block:: bash

   python3 read_map.py

It prints the slide's three counts, measured on Town01:

.. code-block:: text

   waypoints at 2 m, len(wps): 3266
   topology segments, len(segs): 160
   traffic lights in the file: 36


Your Own Map: ``osm_to_map.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the code of the appendix slide "From your .osm file to a map, in
Python", in :doc:`Going Further <l7_appendix>`. It turns an OpenStreetMap
export into OpenDRIVE text, then into a CARLA map:

.. code-block:: python

   osm = open("maps/umd_engineering.osm").read()
   settings = carla.Osm2OdrSettings()
   settings.proj_string = ("+proj=tmerc +lat_0=38.99 +lon_0=-76.939"
                           " +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m")
   settings.center_map = False      # keep its origin
   settings.use_offsets = False
   xodr = carla.Osm2Odr.convert(osm, settings)  # OpenDRIVE text
   m = carla.Map("campus", xodr)    # a map object

``proj_string`` sets how latitude and longitude become meters: on the slide,
:math:`x = 0`, :math:`y = 0` is at latitude 38.99, longitude −76.939. With
``center_map`` on, the converter would move the origin to the center of the
road map, and ``use_offsets`` would shift it too. Both stay off, so the
origin stays where ``proj_string`` puts it.

The script does not use the slide's fixed numbers. It reads the edges of the
exported box from the file (its ``<bounds>`` element) and puts ``lat_0`` and
``lon_0`` at the middle of that box, so the projection is centered on the
file's own area.

**With no argument**, it converts ``maps/umd_engineering.osm``, the campus
around the Kim building (map data © OpenStreetMap contributors, ODbL):

.. code-block:: bash

   python3 osm_to_map.py

It prints 314 roads, 46 intersections and 9144 waypoints at 2 m, the numbers
on the slide "A map of your own, from OpenStreetMap".

**With your own export:**

1. On `openstreetmap.org
   <https://www.openstreetmap.org/export#map=16/38.99000/-76.93900>`_, export
   an area. Your browser saves it as ``map.osm``.
2. Give the script the file's location, for example:

   .. code-block:: bash

      python3 osm_to_map.py ~/Downloads/map.osm

   Use the folder your browser saved it in. A bare file name is also looked
   for in ``lecture7/maps/``.

The script writes ``my_area.xodr`` into the folder you run it from. Open it in
a text editor, or read it with ``carla.Map`` as ``read_map.py`` reads
Town01. The converter prints many warnings about map features it skips; they
are normal.


What Each Part Shows
--------------------

Part 0: The Map File (``--part map``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The script reads ``maps/Town01.xodr`` with ``carla.Map("Town01", text)`` and
no server. In the terminal it prints what the file holds (122 roads, 96 of
them inside the 12 intersections, 36 traffic lights) and what CARLA makes of
it: 3266 waypoints at 2 m, and the 160 (start, end) waypoint pairs of
``get_topology()``, which the script prints as "160 topology segments". Then
it opens the window.

.. figure:: /_static/images/L7/handson_map.png
   :alt: A screenshot of the map window: Town01 from above, x from 0 to 400 meters east and y from minus 330 to 0 meters north, drawn as dots along every lane, dark on the roads and amber inside the twelve intersections. A legend names the two kinds of dot. Under the map, a hint line, a Search box holding road 25, an x, y box holding 133.6, minus 129.4, and three buttons: Zoom in, Zoom out and Whole map.
   :width: 75%
   :align: center

   The map window, showing the whole town (:math:`x` east and :math:`y` north,
   in meters). Each dot is a waypoint: dark on a road, amber inside an
   intersection. Under the map: a hint line, the **Search** box, the
   **x, y** box and three buttons. The line at the bottom prints what you
   click or search.

- **Zoom:** turn the mouse wheel (it zooms at the cursor), or use the
  **Zoom in**, **Zoom out** and **Whole map** buttons. This window has no
  drag to pan; to move the view, use the pan tool of matplotlib's toolbar. A
  click does nothing while that tool is on.
- **Search:** type an ID in the **Search** box, then press Enter:

  - ``road 25`` (or just ``25``): every waypoint of road 25. The line below
    gives the road's length, its two ends and the line of ``Town01.xodr``
    where the road starts.
  - ``lane 25 -1``: road 25, lane −1.
  - ``junction 332``: the waypoints inside intersection 332.
  - ``segment 12``: one of the 160 waypoint pairs of ``get_topology()``,
    numbered 0 to 159 (the script calls each pair a segment).
  - ``waypoint 100``: one waypoint.

  The match turns pink, and the view zooms to it.
- **x, y:** type a position in meters, :math:`x` east and :math:`y` north,
  then press Enter. ``133.6, -129.4`` is our start. CARLA's
  ``Map.get_waypoint`` finds the nearest lane point, and the window prints
  its road, its lane, :math:`s` (the distance along the road) and the line
  of ``Town01.xodr`` to open. Use this box rather than a click to get a
  position exactly: the drawn waypoints are 2 m apart.
- **Click** a waypoint: the window prints its road, its lane, :math:`s`, the
  lane's width, its junction if it is inside one, and the line of
  ``Town01.xodr`` where that road starts. Open the file at that line.

**In class: find our start in the map file.**

1. Type our start, S, :math:`x = 133.6`, :math:`y = -129.4` m (the middle of
   the AV's rear axle), in the **x, y** box and press Enter. The window
   prints its road, lane and :math:`s`.
2. Open ``Town01.xodr`` at the line it prints. Read the road's length, its
   speed limit, and the junction at each end (``predecessor``,
   ``successor``).
3. Lane 1 lies left of the road's reference line, so it drives against
   :math:`s`, the distance along that line. **Question:** which junction
   does the AV reach first, the predecessor or the successor, and which
   intersection of our route is it?

The answer is in :doc:`Exercise 1 on the Exercises page <l7_exercises>`.


Part 1: Town01's Graph (``--part graph``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The real routing graph: all 3107 nodes and 3143 edges. A node is a waypoint;
an edge joins it to the next node along its lane, the way the AV drives.

Seen whole, the nodes are 2 m apart and too close to tell apart. So the
window shows the lanes in gray and, in amber, the 36 **splits**: the nodes
with two successors, where a lane enters an intersection and the AV can go
two ways.

.. figure:: /_static/images/L7/handson_graph.png
   :alt: A screenshot of the graph window zoomed on one intersection, x from 78 to 124 meters east and y from minus 87 to minus 47 meters north. Dark dots 2 meters apart along two north-south lanes and two east-west lanes, joined by gray arrows that point the way each lane drives; curved chains of arrows cross the intersection. Two nodes are amber. Amber rings mark two points that each hold two nodes: one 2 meters after the lower amber node, one at the top of the left lane. A box at the bottom reads: node 224, at 92.4, minus 68.1 meters, heading 90 degrees, road 183, lane 1, in an intersection; successors: node 225, 2.00 meters, and node 2934, 2.00 meters; the two successors are 0.00 meters apart, ringed, and the two ways are more than 1 meter apart about 7 meters after this node.
   :width: 75%
   :align: center

   The graph window, zoomed on intersection 3. Dark dots are nodes; gray
   arrows are edges, pointing the way the AV drives. The two amber dots are
   splits. The amber rings mark points that hold two nodes. The box at the
   bottom is what a click on node 224 prints.

- **Zoom and pan:** scroll to zoom in at the mouse; drag with the left
  button to pan. Once the view is under 120 m across, every node is a dot and
  every edge an arrow.
- **Rings:** a split's two successors usually sit at one point, because the
  two ways out of an intersection leave along the same line and part a few
  meters on. An amber ring marks every point that holds two nodes.
- **Click** a node (press and release without moving): the box prints its
  position, heading, road, lane and successors, with each edge's length. For
  a split, it also says how far on its two ways part. A click on a ring
  lists both of its nodes, one for each way, and the split they follow.

**What to look for:** click node 224, the lower amber node in the figure. It
has two successors, both 2.00 m ahead at one point (ringed): straight on and
a right turn, which part about 7 m on.


Part 2: The Edge Costs (``--part costs``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every edge's three costs, and the routes of the slide "Routes under three
costs". The three costs of an edge are its length in meters; its travel
time, the length divided by the AV's speed on it; and its length plus 30 m
if it is a left turn (the penalty, chosen for this lecture). The costs were
computed in advance and saved in ``l7_results/routes.npz``.

.. figure:: /_static/images/L7/handson_costs.png
   :alt: A screenshot of the left panel of the costs window: every edge of Town01, light gray on the straight lanes and dark gray to black in the turns, with a scale under it from 0 to about 0.33 seconds per meter. Twenty-four small rings mark the left-turn edges; a legend says a left turn adds 30 meters in the penalty cost. A thick black mark near x 146 meters, y minus 59 meters is the clicked edge. A box at the bottom lists edge 0, node 0 to node 1, and edge 31, node 0 to node 33, a left turn: both 2.00 meters and 0.179 seconds at the speed limit; with the penalty, edge 0 costs 2.00 meters and edge 31 costs 32.00 meters.
   :width: 70%
   :align: center

   The left panel of the costs window. Each edge is shaded by the seconds it
   takes to drive one meter of it (the scale under the map): light on the
   straight lanes, dark in the turns. Rings mark the left-turn edges. The
   thick black mark is the clicked edge, and the box at the bottom is what
   the click prints.

- **Left panel:** every edge of Town01, darker where one meter takes longer:
  the AV slows in the turns. Rings mark the 24 left-turn edges. Scroll to
  zoom, drag to pan.
- **Click** an edge: it turns thick black, and the box prints its three
  costs, and whether its speed is the speed limit or is slowed by the curve.
  Where a lane splits, two edges leave the same node along the same first
  meters; the click lists both.
- **Right panel:** the same start and goal, searched once with each cost.
  The blue route (cost = distance) is 260.6 m and 31.0 s. The dashed rust
  route (cost = travel time) is 266.9 m and 27.7 s. The dotted route (cost =
  distance plus 30 m per left turn) is the same as the travel-time route.

**What to look for:** in the figure, edges 0 and 31 leave node 0 along the
same first 2 m, where the heading does not change yet. Both cost 2.00 m and
0.179 s, but edge 31 starts a left turn, so its penalty cost is 32.00 m.


Part 3: The Searches (``--part search``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two panels side by side: Dijkstra on the left, A* on the right, both with
distance costs. In each panel, amber dots are the nodes that search took from
its open set, in order. Both searches find the same route; Dijkstra took 543
nodes, A* 196.

- **The slider** (labeled "step", under the panels) sets how many nodes each
  search has taken so far. The window opens with the slider at its end.
- Each panel's title gives the nodes taken so far, out of that search's
  total. When a search reaches G, its title says "goal reached" and its
  route appears in blue. A* stops sooner, so it shows its route while
  Dijkstra still runs.

**What to look for:** set the slider to 100. Where are Dijkstra's first 100
nodes, and where are A*'s? :ref:`l7-app-scale` in :doc:`Going Further
<l7_appendix>` compares the two searches on this graph.


Part 4: Re-planning (``--part replan``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The window shows the slide "An obstacle on the road from 5 to 6". The AV
drives north, 23 m before the center of intersection 3 (a position chosen
for this example), when perception reports an obstacle on the road from 5
to 6.

- **Black triangle:** the AV when it sees the obstacle.
- **Red X and red circle:** the obstacle (placed for this example) and the
  3.0 m around it (GP4's ``obstacle_clearance``). The planner closes the
  edges within 3.0 m of it.
- **Blue line:** the old route, from the AV: 172.6 m left.
- **Dashed green line:** the new route, planned again from the AV:
  178.9 m. The detour adds 178.9 − 172.6 = 6.3 m.

**What to look for:** where does the new route leave the old one? It goes
straight on at 3 and turns right at 4, instead of turning right at 3 and
left at 5.


Optional: the Search in Rerun
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``rerun_search.py``, in the same folder, replays the two searches of
``--part search`` in the `Rerun <https://rerun.io>`__ viewer. The lecture
does not need it: in the folder's README, "its package and viewer take
several hundred megabytes". The README's section `Optional: the search in
Rerun
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/blob/main/lecture7/README.md#optional-the-search-in-rerun>`__
gives the details.

.. code-block:: bash

   pip install rerun-sdk
   python3 rerun_search.py

   # write a recording instead, and open it later
   python3 rerun_search.py --save search.rrd
   rerun search.rrd

Drag the time slider, or press play, to watch both searches take their
nodes; a search's route appears when it reaches G. Rerun's 2D views point
:math:`y` down, so the script flips :math:`y`: north stays up, and the axis
shows 130 where the map has :math:`y` = −130 m.


The Data
--------

- ``maps/Town01.xodr`` is CARLA 0.9.16's map file for Town01, unchanged.
  CARLA's assets are distributed under the CC-BY license (CARLA's README);
  the file is from the CARLA project,
  https://github.com/carla-simulator/carla.
- ``l7_town01_graph.npz`` holds Town01's waypoint graph, read offline from
  ``Town01.xodr`` with ``carla.Map(name, xodr_text)``: a node every 2 m along
  every lane, sampled the way CARLA's ``GlobalRoutePlanner`` samples it, and
  a directed edge from each node to the next one along its lane.
- ``l7_results/routes.npz`` holds the routes (lists of node numbers), the two
  search orders, the re-planned route, and the route's reference path with
  saved speeds. ``l7_results/summary.json`` holds every number, the values we
  chose, and the toy graph the slides search by hand.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Array in l7_town01_graph.npz**
     - **Meaning**
   * - ``node_xy``
     - position (m): :math:`x` east, :math:`y` north (CARLA's :math:`y`
       flipped, as in L6)
   * - ``node_yaw_deg``
     - heading (degrees, counterclockwise from east)
   * - ``node_road``, ``node_lane``
     - OpenDRIVE road and lane ID
   * - ``node_junction``, ``node_junction_id``
     - inside an intersection, and which one (−1: none)
   * - ``node_speed_limit``
     - m/s, from the road's ``<speed>`` in the file; NaN (no value) inside
       intersections
   * - ``edge_from``, ``edge_to``, ``edge_len``
     - directed edges and their lengths (m)
   * - ``edge_lane_change``
     - a lane change edge (none in Town01: one lane each way)
   * - ``seg_turn``
     - for each topology segment through an intersection: ``L``, ``R`` or
       ``S`` (left, right or straight)

**Values we chose:** a left-turn penalty of 30 m and the obstacle's position;
for the saved speeds, a sideways acceleration in a curve of at most
2.0 m/s², a speed-up of at most 1.5 m/s² and braking of at most 2.0 m/s².
**GP4's values:** ``obstacle_clearance`` 3.0 m, ``max_deviation`` 2.0 m,
``replan_frequency`` 2 Hz.


Run the Tests
~~~~~~~~~~~~~

From ``lecture7/``:

.. code-block:: bash

   python3 -m pytest -q tests

The tests check that each part saves a snapshot, that ``read_map.py`` and
``osm_to_map.py`` print the slides' numbers, and that the map window's
searches work. They also check the saved results: every route is a connected
path from S to G, Dijkstra and A* agree, and the re-planned route avoids the
obstacle. One test checks that no public file in the folder holds search
code. The tests
that need CARLA's Python package are skipped when it is not installed.
