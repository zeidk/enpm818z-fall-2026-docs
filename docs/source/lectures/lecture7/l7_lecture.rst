====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L7, the slides shown in class and
   the reading slides that go with them, in the same order and with the same
   sections. You can read them at home. The deck keeps more material in its
   appendix, on :doc:`the appendix page <l7_appendix>`, "Going Further":

   - route, lane and navigation in other AV stacks;
   - the full definitions of path and trajectory;
   - where the map fits in the AV's architecture, and the scene model at
     Waymo and Tesla;
   - HD map formats: Lanelet, Lanelet2, and OpenDRIVE against Lanelet2;
   - a road's lanes and curves in OpenDRIVE, with road 333's turn step by
     step;
   - how traffic lights add waiting time to an edge cost;
   - the recap of Dijkstra and A*: edge costs that are not negative,
     admissible and consistent heuristics, and a heuristic in seconds for
     travel time;
   - route planning at scale: our trip on the waypoint graph, GP4's node
     limit, and routing a whole country.

   Dijkstra and A* on the intersection graph, one step at a time, are on
   :doc:`the search steps page <l7_search_steps>`. The hands-on commands are
   on :doc:`the Code page <l7_code>`. The papers and pages cited below are
   listed in full on :doc:`the References page <l7_references>`.


.. _l7-lec-introduction:

Introduction
------------

.. note::

   **L6** finds where **the AV is** on the map. **L7** finds **which lanes
   take it to the goal**.

We follow one trip in CARLA's Town01. On that trip we read the map file, turn
it into a graph, put the start and the goal on it, and search it. Then we
plan again when the road is blocked, and hand the route on as maneuvers.


.. _l7-lec-terms:

Terms of This Lecture
~~~~~~~~~~~~~~~~~~~~~

Before we define anything, here is a diagram of today's terms and how they
connect. It is a UML class diagram (Object Management Group, 2017). The key
at the bottom right says what each kind of line means.

.. figure:: /_static/images/L7/concept_uml.png
   :alt: A UML class diagram of the lecture's terms. Top row: RoadNetwork, made of one or more Road; Road made of one or more Carriageway; Carriageway made of one or more Lane. Route refers to one or more Lane, in order. RoutePlanner, with the operation plan(network, start, goal) returning a Route, uses RoadNetwork and creates Route. Lower part: ConfigurationSpace X, made of any number of Configuration, each with x, y and theta. Path, sigma from 0 to 1 into X, and Trajectory, pi from 0 to T into X, both use ConfigurationSpace. A key: a filled diamond line means is made of, a solid arrow refers to, a dashed open arrow depends on, with its label saying how (use, create); 1..* one or more, * any number.
   :width: 95%
   :align: center

   The lecture's terms as a UML class diagram. **Top:** the road side, from
   ``RoadNetwork`` down to ``Lane``, with ``Route`` and ``RoutePlanner``.
   **Bottom:** the motion side, ``ConfigurationSpace`` :math:`X` with its
   configurations, and ``Path`` and ``Trajectory``, which both use it. The
   key at the bottom right reads: a filled diamond line, "is made of"; a
   solid arrow, "refers to"; a dashed open arrow, "depends on", with its
   label saying how (use, create); "1..*", one or more; "*", any number.

- **The road side (top row).** A road network is made of roads, a road of
  carriageways, and a carriageway of lanes. A route refers to lanes, in
  order: ``{ordered}`` on the arrow means the lanes come in driving order.
  The route planner uses the road network and creates the route. Its
  operation ``plan(network, start, goal)`` takes a network, a start and a
  goal, and returns a route.
- **The motion side (lower part).** :math:`X` is the configuration space,
  the set of all configurations. A configuration is a position :math:`x`,
  :math:`y` in meters and a heading :math:`\theta`. A path :math:`\sigma`
  gives one configuration for each number from 0 (start) to 1 (goal). A
  trajectory :math:`\pi` gives one for each time from 0 to :math:`T`.

The next slides define the road terms, then route and route planning, one per
slide. The three motion terms share one slide; their full definitions are in
the appendix.


.. _l7-lec-road:

Road
~~~~

.. admonition:: Definition: Road
   :class: note

   "Line of communication (travelled way) open to public traffic, primarily
   for the use of road motor vehicles, using a stabilized base other than
   rails or air strips" (Eurostat, ITF and UNECE, 2019).

Three parts of this definition matter: a road is open to public traffic, it
is for road motor vehicles, and it is not rails or air strips. So a road is
where cars drive, not trains or planes.

The same entry goes on: "Roads also cover streets, bridges, tunnels,
supporting structures, junctions, crossings and interchanges" (Eurostat, ITF
and UNECE, 2019). Keep this second quote in mind: a road also covers
junctions and crossings, and in CARLA an intersection is made of roads too.

.. figure:: /_static/images/L7/road25.png
   :alt: A top view of part of Town01, x from 128 to 186 meters east, y from minus 68 to 12 meters north, lanes in light gray. A thick black line, tag 1, runs south along x 156 from y minus 11 to minus 46 meters, with an arrow pointing south: road 25's reference line. Gray dots run beside it on both sides: points along its two lanes. Black circles mark the intersection at its north end, tag 2, near y minus 2, and the one at its south end, tag 3, near y minus 55.
   :width: 50%
   :align: center

   Road 25 in Town01, from above, :math:`x` east and :math:`y` north in
   meters. **1:** the thick black line is the line the map file draws the
   road along; its arrow points south, the direction the file draws it.
   The gray dots beside it are points every 2 m on the road's two lanes.
   **2** and **3:** the intersections at the road's north and south ends
   (circled).

**In Town01:** the map file calls this road 25 (**1**). It is 35.18 m long,
between two intersections, **2** and **3**. On our route, those two are
intersections 6 and 5. The arrow shows only the direction the map file
draws the road: the road's two lanes carry traffic both ways. We define a
lane three slides from now.

96 of Town01's 122 roads are the short pieces inside its 12 intersections.
So when CARLA says "road", it often means a piece inside an intersection,
not a street.


.. _l7-lec-road-network:

Road Network
~~~~~~~~~~~~

.. admonition:: Definition: Road network
   :class: note

   "All roads in a given area" (Eurostat, ITF and UNECE, 2019).

.. figure:: /_static/images/L7/town01_overview.png
   :alt: A top view of all of Town01's lanes in gray, x from 0 to 400 meters east and y from minus 340 to 0 meters north: an outer loop with streets inside it. White circles with a dark ring mark the twelve intersections: three along the top street, three on the next street down, two on each of the next two streets, and two on the bottom street.
   :width: 70%
   :align: center

   All of Town01's lanes, from above, :math:`x` east and :math:`y` north in
   meters: an outer loop with streets inside it. The **white circles** mark
   the 12 intersections.

**In Town01:** the road network is the town's 122 roads. 26 run between
intersections, and 96 are short roads inside the 12 intersections (circled)
that join one street to the next.

Route planning searches this network. Everything today is about finding a
way through it.


.. _l7-lec-carriageway:

Carriageway
~~~~~~~~~~~

.. admonition:: Definition: Carriageway
   :class: note

   "Part of the road intended mainly for the movement of road vehicles";
   shoulders and the parts "intended for the parking of vehicles" are not
   part of it (Eurostat, ITF and UNECE, 2019).

A road is wider than the part cars drive on. The carriageway is the part
meant for moving vehicles.

.. figure:: /_static/images/L7/carriageway25.png
   :alt: A top view, to scale, of a 12 meter stretch of road 25, north up, x from about 147 to 165 meters east. Seven strips side by side, west to east: a light gray sidewalk, tag 1; a thin gray-brown shoulder, tag 2, its tag on a short line above it; a white driving strip with an arrow pointing south, tag 3; a dashed line, the reference line; a white driving strip with an arrow pointing north, tag 3; a thin gray-brown shoulder, tag 2; a light gray sidewalk, tag 1. A two-headed arrow below the two white strips is labeled 8.0 m.
   :width: 55%
   :align: center

   12 m of road 25, to scale, north up. From west to east: a sidewalk
   (**1**), a shoulder (**2**), the driving strip going south (**3**), the
   dashed reference line, the driving strip going north (**3**), a shoulder
   (**2**) and a sidewalk (**1**). The two-headed arrow under the two
   driving strips reads 8.0 m.

**In Town01:** the figure shows 12 m of road 25, to scale, with the widths
from its map file, ``Town01.xodr``. The dashed line is the line the file
draws the road along.

- Part of the road, but not of the carriageway: **1**, the sidewalks, 4.0 m
  each, and **2**, the shoulders, 0.3 m each.
- The carriageway: **3**, the two driving strips, 4.0 m each, one going
  south and one going north, so 4.0 + 4.0 = 8.0 m.


.. _l7-lec-lane:

Lane
~~~~

.. admonition:: Definition: Lane
   :class: note

   "One of the longitudinal strips into which a carriageway is divisible,
   whether or not defined by longitudinal road markings, which is wide enough
   for one moving line of motor vehicles other than motor cycles" (Eurostat,
   ITF and UNECE, 2019).

A lane is one strip of the carriageway, wide enough for one line of cars.
"Whether or not defined by markings" means that a lane can exist without any
paint.

.. figure:: /_static/images/L7/lane25.png
   :alt: A top view, to scale, of a 24 meter stretch of road 25, north up. Two long white strips side by side, each outlined in black and 4 meters wide, are the lanes, tag 1: the west one has an arrow pointing south, the east one an arrow pointing north. Light gray sidewalks and shoulders lie on both sides. To the right, a long two-headed arrow running north and south, tag 2, shows the longitudinal direction, along the road.
   :width: 50%
   :align: center

   24 m of road 25, from above, to scale. **1:** the two lanes, outlined in
   black: the west one carries traffic south, the east one north. **2:** the
   two-headed arrow shows the longitudinal direction, along the road. Gray:
   sidewalks and shoulders.

**In Town01:** the figure shows a 24 m stretch of road 25, from above, to
scale.

- **1:** its two lanes, 4.0 m wide each: one for traffic going south, one
  for traffic going north.
- **2:** *longitudinal* means along the road, the way the traffic moves.

Every road outside the intersections in Town01 has one lane each way. So in
Town01 the AV never changes lanes. It still has to start and end on the lane
that goes the right way.


.. _l7-lec-route:

Route
~~~~~

.. admonition:: Definition: Route
   :class: note

   "The route is made of a sequence of lanes on a static map" (Autoware
   Foundation, Mission Planner).

A *static* map is made before the drive, like ``Town01.xodr``.

.. figure:: /_static/images/L7/route_panel.png
   :alt: A top view of part of Town01, x from 65 to 215 meters east, y from minus 150 to 18 meters north. The lanes are light gray. The route is a thick blue line: from the start on a lower street it goes west, turns north at the intersection marked 1, turns east at the one marked 3, turns north at the one marked 5, turns east at the one marked 6, and ends at the goal on the top street. The marks 1, 3, 5 and 6 are gray numbers in gray rings.
   :width: 60%
   :align: center

   Our trip's route, the **thick blue line**, from its lower right end (the
   start) to its upper right end (the goal). It goes west, then turns north
   at intersection 1, east at 3, north at 5 and east at 6. The gray rings
   are our numbers for those intersections.

**On our trip**, from the blue line's lower right end to its upper right
end, the route is **9 lanes** and **260.6 m**: 5 lanes along the streets,
and 1 lane through each of the four marked intersections. The AV turns right
at 1, right at 3, left at 5 and right at 6. The numbers 1, 3, 5 and 6 are
our own names for these intersections; the intersection graph uses them
later. The map file calls them junctions 306, 171, 332 and 54.

The planner hands the route on as **waypoints** along those lanes, one about
every 2 m, 130 in all. GP4 Task 1 asks you to write the planner that
produces them.


.. _l7-lec-config:

Configuration Space
~~~~~~~~~~~~~~~~~~~

The next three terms come from motion planning.

.. admonition:: Definition: Configuration space
   :class: note

   "The state space for motion planning is a set of possible transformations
   that could be applied to the robot. This will be referred to as the
   configuration space" (LaValle, 2006).

One element of the configuration space is a **configuration**: it says
where the robot is. For a car, "configuration can be expressed as the planar
coordinate of a point on the car together with the car's heading" (Paden et
al., 2016): :math:`(x, y, \theta)`. We write :math:`X` for the configuration
space, the set of all configurations.

.. figure:: /_static/images/L7/configuration.png
   :alt: A close top view of the start, x from about 120 to 146 meters east, y from minus 136 to minus 121 meters north. The AV, a black top-view car, faces west on its lane. A dark dot on its rear axle is labeled (x, y). A gray dashed line points east from the dot; an arc from that line, over the top, to a black arrow pointing west is labeled theta, the heading, 180 degrees.
   :width: 70%
   :align: center

   Our start, from above. The AV faces west on its lane. The **dot** on its
   rear axle is :math:`(x, y)`. The arc labeled :math:`\theta` runs from the
   gray dashed line, pointing east, over the top to the black arrow,
   pointing west.

At our start, :math:`(x, y) = (133.6, -129.4)` m is the middle of the rear
axle, the AV's base link from L3. :math:`\theta = 180^\circ`, measured
counterclockwise from east, so the AV faces west.


.. _l7-lec-motion-terms:

Route, Path and Trajectory
~~~~~~~~~~~~~~~~~~~~~~~~~~

A route says which lanes. Two more words say how the AV moves along them.
People often mix up the three.

.. figure:: /_static/images/L7/route_path_traj.png
   :alt: Three panels of the same trip. Panel 1, Route: which lanes, in order: part of Town01 with the route as a thick blue line from the start west to intersection 1, north to 3, east to 5, north to 6 and east to the goal; gray rings mark 1, 3, 5 and 6. Panel 2, Path: points with heading: a close view of the right turn at intersection 1, with small black arrows along the blue line pointing west on the straight, turning through the curve, and north after it. Panel 3, Trajectory: the path, and when: the same turn with black dots one second apart, labeled 5 s, 7 s, 9 s and 11 s, farther apart on the straight and closer in the turn.
   :width: 95%
   :align: center

   **1, Route:** which lanes, in order, the blue line through intersections
   1, 3, 5 and 6. **2, Path:** points with heading, a close view of the
   right turn at 1; the small black arrows point west on the straight, turn
   through the curve, and point north after it. **3, Trajectory:** the path,
   and when; the same turn with a black dot every second, labeled 5 s, 7 s,
   9 s and 11 s.

1. **Route:** which lanes, in order. That is what we plan today: route
   planning.
2. **Path:** where the AV goes, a chain of **configurations**
   :math:`(x, y, \theta)`: a position in meters and a heading, measured
   counterclockwise from east. A path has no times. Its curvature is how
   sharply it bends. L9 plans paths.
3. **Trajectory:** the path, and when. Here we computed it before the drive.
   We gave every point of the path a speed: the speed limit, 11.18 m/s, but
   slower in a turn so that the sideways acceleration stays under 2.0. The
   AV speeds up at most 1.5 and brakes at most 2.0, from rest to rest. All
   three limits are in meters per second squared, and all are chosen for
   this example. L10 follows trajectories.

The time at each point is the distance divided by the speed, added up along
the path. Panels 2 and 3 zoom in on the turn at 1. The dots in panel 3 show
where the AV is after each second; they bunch up in the turn, where the AV
is slower. A real AV's motion planner computes the trajectory while it
drives, a short stretch ahead at a time: that is L9.

.. tip::

   See *Path* and *Trajectory* in :doc:`Going Further <l7_appendix>` for the
   full definitions.


.. _l7-lec-route-planning:

Route Planning
~~~~~~~~~~~~~~

The last term puts the others together.

.. admonition:: Definition: Route planning
   :class: note

   In Paden et al.'s survey: the AV "must select a route through the road
   network from its current position to the requested destination". With the
   road network as a directed graph whose edge weights are the cost of each
   road segment, that is "the problem of finding a minimum-cost path" (Paden
   et al., 2016).

So route planning means choosing a route through the road network, from
where the AV is to where it must go. Paden et al. turn that into a graph
problem: find a minimum-cost path. Here a **path** is a path in the graph, a
chain of graph edges. It is not the path :math:`(x, y, \theta)` of
:ref:`l7-lec-motion-terms`.

Each part of the definition is a section of this lecture:

- the road network as a **directed graph**: :ref:`Map to Graph
  <l7-lec-map-to-graph>`, and Lane Changes;
- the **cost** of each road segment: Edge Costs;
- the **current position** and the **destination** on the graph: the trip's
  start S and goal G, in :ref:`The Trip <l7-lec-trip>`;
- **finding a minimum-cost path**: Search, and At Scale.

You know Dijkstra and A* from the planning course, so Search and At Scale
are recapped in :doc:`Going Further <l7_appendix>`. Both searches on the
intersection graph, one step at a time, are on :doc:`the search steps page
<l7_search_steps>`.


.. _l7-lec-planner-io:

What the Route Planner Reads and Writes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In GP4, route planning is one ROS 2 node. The figure shows what it reads and
what it writes, as a UML component diagram. A **ball on a line** means a node
provides that data: it publishes it. A **socket** around the ball means a
node requires the data: it subscribes to it.

.. figure:: /_static/images/L7/planner_io.png
   :alt: A UML component diagram. On the left, three components: localization_node (GP3), fusion_node (GP3) and CARLA world. Each provides an interface, drawn as a ball on a line, that planner_node requires, drawn as a socket around the ball: /localization/pose of type geometry_msgs/PoseStamped, /perception/fused_objects of type vision_msgs/Detection3DArray, and carla.Map, from the OpenDRIVE file. planner_node (GP4 Task 1), with the parameters goal_x and goal_y, provides /planning/path of type nav_msgs/Path, which controller_node (GP4 Task 2) requires. A key: a ball on a line provides (publishes); a socket requires (subscribes to). Five numbered dark tags: 1 below the pose line, 2 below the objects line, 3 below the map line, 4 beside the parameters inside planner_node, 5 below the /planning/path line.
   :width: 95%
   :align: center

   GP4's planner node and what connects to it. **Left:** GP3's
   ``localization_node`` (**1**, ``/localization/pose``), GP3's
   ``fusion_node`` (**2**, ``/perception/fused_objects``) and the CARLA world
   (**3**, ``carla.Map``, from the OpenDRIVE file). **Middle:**
   ``planner_node``, GP4 Task 1, with its parameters ``goal_x`` and
   ``goal_y`` (**4**). **Right:** ``/planning/path`` (**5**) to
   ``controller_node``, GP4 Task 2.

The planner node (GP4 Task 1) has three inputs, a goal and one output:

- **1:** the AV's pose, from your GP3 localization node: what we built in
  L6.
- **2:** the objects on the road, from your GP3 fusion node: L5. The planner
  needs them to know when an object blocks the route.
- **3:** the map. It does not come on a topic: the planner reads it from the
  CARLA world through the Python API, and CARLA built it from the OpenDRIVE
  file.
- **4:** the goal, given as two parameters, ``goal_x`` and ``goal_y`` in
  meters: a point with no heading.
- **5:** the route, as waypoints to the goal, on ``/planning/path``. Your
  controller in GP4 Task 2 follows it. ROS calls it a path.


.. _l7-lec-industry:

Route Planning in Industry
~~~~~~~~~~~~~~~~~~~~~~~~~~

Other AV software has the same module: from a pose, a map and a goal to a
route. Apollo and Autoware are open source, so their documents name their
search. Waymo describes routing only for its riders.

.. list-table::
   :widths: 14 18 48 20
   :header-rows: 1
   :class: compact-table

   * - **Stack or company**
     - **Its name**
     - **What its documentation says**
     - **Its search**
   * - Apollo
     - Routing
     - "generates high level navigation information" from map data and a
       start and end location (Apollo Auto, Routing)
     - A* (Apollo Auto, routing navigator)
   * - Autoware
     - Mission planning
     - "calculates routes from the current location to the destination,
       utilizing map data" (Autoware Foundation, Planning component design)
     - Dijkstra, in the Lanelet2 map library (FZI, Lanelet2 routing graph)
   * - Waymo
     - Routing
     - its maps "help every Waymo car plan its route before your trip
       starts" (Waymo, Routing)
     - not published

.. note::

   In this course, **route planning** is this module, and GP4 searches with
   A*, as Apollo does.

.. tip::

   See *Route, lane and navigation in other stacks* in :doc:`Going Further
   <l7_appendix>`.


.. _l7-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

After this lecture, you can:

1. read a **map file** and turn it into a **routing graph**: say what a node
   and an edge are, and where they come from in OpenDRIVE;
2. say how **traffic rules and lanes** enter the graph: missing edges,
   driving directions, lane change edges;
3. choose an **edge cost** (distance, travel time, a left-turn penalty) and
   predict how it changes the route;
4. recall **Dijkstra and A*** from the planning course (recap in the
   appendix), and say what GP4's A* heuristic must satisfy: it never
   overestimates, in the units of the edge costs;
5. say when a planner must **plan again** (GP4's two triggers), and why it
   must not switch routes back and forth;
6. turn a route into **maneuvers** for the planners after route planning.


.. _l7-lec-trip:

The Trip
--------

One trip in CARLA's Town01 is the example for every method today.

**What it is for:** comparing costs and searches on the same start and goal.

**Town01** is a small CARLA town: a grid of two-lane streets with twelve
T-intersections (circled). Its map is the OpenDRIVE file ``Town01.xodr``,
which we read with the CARLA Python API and no CARLA server running (CARLA
Team, Python API reference).

.. figure:: /_static/images/L7/town01_overview.png
   :alt: A top view of all of Town01's lanes in gray, x from 0 to 400 meters east and y from minus 340 to 0 meters north: an outer loop with streets inside it. White circles with a dark ring mark the twelve intersections: three along the top street, three on the next street down, two on each of the next two streets, and two on the bottom street.
   :width: 70%
   :align: center

   Town01 from above, :math:`x` east and :math:`y` north in meters. The
   **white circles** mark its twelve T-intersections.


.. _l7-lec-trip-town01:

The Trip in Town01
~~~~~~~~~~~~~~~~~~

One trip runs through the whole lecture.

.. figure:: /_static/images/L7/trip_overview.png
   :alt: A top view of all of Town01's lanes in light gray: an outer loop about 400 meters wide and 330 meters tall with a grid of streets inside. Tag 1, the start, sits on a horizontal street in the middle left, near x 134 and y minus 129 meters, with a black arrow pointing west. The intersection 41 meters west of it, near x 93, is circled, and a two-headed line below the street between them is labeled 41 m. Tag 2, the goal, sits on the top street near x 196 and y minus 2 meters, with an arrow pointing east. The intersection 40 meters west of it, near x 157, is circled, with a two-headed line labeled 40 m. Axes: x east and y north, in meters.
   :width: 75%
   :align: center

   The trip in Town01. **1:** the start, with an arrow pointing west; the
   circled intersection is 41 m west of it. **2:** the goal on the top
   street, with an arrow pointing east; the circled intersection is 40 m
   west of it.

- **1, the start, S:** the AV is 41 m east of the center of intersection 1
  (circled) and drives west.
- **2, the goal, G:** 40 m east of the center of intersection 6 (circled), on
  the top street, driving east.
- The map frame is L6's: :math:`x` east, :math:`y` north, in meters. CARLA's
  own :math:`y` points south, so we flip its sign.

The start and the goal are chosen for this lecture. GP4's Town01 test route
is a different one.


.. _l7-lec-trip-known:

What the AV Knows, and What It Must Produce
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before the AV drives that trip, here is what it has and what it lacks.

.. figure:: /_static/images/L7/trip_line_vs_route.png
   :alt: A top view of part of Town01, x from 60 to 215 meters east, y from minus 150 to 22 meters north, lanes in light gray. Tag 1, the start, on a lower street near x 134; tag 2, the goal, on the top street near x 196. A dashed black straight line joins them, tag 3; it crosses blocks where there are no lanes. A thick blue line, the route, follows the lanes: west, north, east, north and east, turning four times.
   :width: 60%
   :align: center

   **1:** the start. **2:** the goal. **3:** the dashed straight line between
   them, which crosses blocks where there are no lanes. The **thick blue
   line** is the route along the lanes: west, north, east, north and east.

- **Known:** before the drive, the map ``Town01.xodr`` and the goal point;
  while driving, the AV's pose, from localization (L6).
- **Not known:** which lanes to take. The map gives only which lane leads to
  which.
- **To produce:** the route, a list of waypoints about every 2 m from the AV
  to the goal.

.. note::

   **3:** the straight line is 141.9 m. No lane runs along it. The shortest
   drivable route, the blue line, turns four times and is 260.6 m long. A
   planner has to search for it.


.. _l7-lec-map-to-graph:

Map to Graph
------------

We see what an HD map is, then turn a map file into a graph a computer can search.

**What it is for:** the searches at scale run on this graph; GP4 searches the same kind of graph.

We have our trip: a start and a goal 141.9 m apart. Before a computer can
search for a route, it needs the roads as a graph. This section builds that
graph. We start with the map itself: what an HD map is, what it holds, and
how real AV stacks make and update one. Then we come back to Town01's own map
file.

.. figure:: /_static/images/L7/map_pipeline.png
   :alt: A UML activity diagram in two rows. It starts at a black dot, then a diamond, a choice. For your own area, the flow goes down to the object .osm file (OpenStreetMap), into the action Osm2Odr.convert(), and into the object map file (.xodr). For Town01, which comes with CARLA, the flow goes straight to the map file. The map file flows into the action carla.Map(name, text), which flows into the object carla.Map. Row 2: carla.Map flows into the object segments, then the action sample every 2 m, join in driving order, the object waypoint graph, the action keep S, G and 7 intersections, and the object intersection graph.
   :width: 95%
   :align: center

   The plan for this section, from a map file to the intersection graph.
   **Top row:** a choice (diamond); for your own area, an ``.osm`` file from
   OpenStreetMap goes through ``Osm2Odr.convert()`` to a map file; for
   Town01, the map file comes with CARLA. ``carla.Map(name, text)`` reads the
   map file into a ``carla.Map``. **Bottom row:** segments, then "sample
   every 2 m, join in driving order", the waypoint graph, then "keep S, G and
   7 intersections", the intersection graph.

The figure is a UML activity diagram (Object Management Group, 2017). The
black dot is the start. The diamond is a choice, with each branch's condition
in [brackets]. A rounded box is a step the code runs; a plain box is the
data that step makes. Arrows give the order. Read the top row, then the
bottom row:

- **Top row.** Town01's map file, a ``.xodr`` file, comes with CARLA. For
  your own area, you export an ``.osm`` file from OpenStreetMap, and
  ``Osm2Odr.convert()`` turns it into a ``.xodr``. Either way,
  ``carla.Map`` reads the text and gives us a ``carla.Map`` object.
- **Bottom row.** The ``carla.Map`` gives us its segments when we call its
  method ``get_topology()``. We put a waypoint every 2 m along them and join
  them in driving order: that is the waypoint graph, 3107 nodes for Town01.
  For the examples by hand, we keep only S, G and seven intersections: the
  intersection graph.

Each box is explained when its step comes up. Before each step, the diagram
is shown again with that step outlined in yellow. The file format,
OpenDRIVE, comes with the first step.


.. _l7-lec-hdmap:

HD Map
~~~~~~

.. admonition:: Definition: HD map (high-definition map)
   :class: note

   A map of the road for automated vehicles. "Centimetre-level positional
   accuracy and the availability of lane-level geometric and semantic
   information are the essential features found in most HD maps"
   (Elghazaly et al., 2023).

- **Lane-level:** the map stores each lane, its width, its borders and where
  it leads, not only the street.
- **Geometric:** where things are and their shape, such as the two borders
  of a lane: on road 25, 4.0 m apart.
- **Semantic:** what things are and the rules they carry, such as a traffic
  light, or road 25's speed limit, 25 mph.
- There is no single standard: "there are no clear guidelines or a standard
  of what information constitutes an HD map" (Elghazaly et al., 2023).


.. _l7-lec-hdmap-look:

What an HD Map Looks Like
^^^^^^^^^^^^^^^^^^^^^^^^^

Here are two HD maps of the kind the definition describes.

.. figure:: /_static/images/L7/hdmap_examples.png
   :alt: Two point-cloud maps side by side, each a 3D view from above at an angle, white and gray dots on black. Left: a long two-lane road with buildings and trees beside it, a circular loop at its left end and an oval loop at the upper right; green lines mark the lane borders and center lines along the road. Right: a rounded-rectangle test track with three lanes drawn in green, two crossings marked with dark blue stripes near its right end, and poles and trees around it; small viewer controls show in the top corners.
   :width: 95%
   :align: center

   Two HD maps of test tracks, seen from above at an angle, white and gray
   dots on black. **Left:** a long road with buildings and trees beside it,
   a loop at each end, and green lane lines along it. **Right:** a
   rounded-rectangle track with three green lanes, two crossings in dark
   blue stripes near its right end, and poles and trees around it.

Both are HD maps of test tracks, seen from above at an angle:

- The white and gray dots are a point cloud: the base the map is drawn on.
- The green lines, drawn on the point cloud, are each lane's borders and
  center line. On the right, the dark blue stripes mark two crossings.

.. admonition:: Definition: Point cloud
   :class: note

   The 3D points a LiDAR measured on the surfaces around it, like L6's map of
   18,661 points.


.. _l7-lec-hdmap-layers:

HD Map Layers
^^^^^^^^^^^^^

Each map maker stores an HD map its own way. A survey by Elghazaly and
colleagues sorts the data into "six distinct layers" (Elghazaly et al.,
2023), and we use their six layers all lecture. HERE's HD Live Map groups the
same data into three models: road centerline, HD lane and HD localization
(MathWorks, HERE HD Live Map Layers).

.. list-table::
   :widths: 22 42 36
   :header-rows: 1
   :class: compact-table

   * - **Layer**
     - **What it holds**
     - **In this course**
   * - Base map
     - 3D points or images of the area
     - L6: a map of 18,661 LiDAR points
   * - Geometric
     - the shape of each lane: points, lines, polygons
     - L7: lane widths and curves
   * - Semantic
     - traffic lights, road signs, crossings
     - L7: waiting at lights, in edge costs
   * - Road connectivity
     - which lane leads to which
     - L7: the graph we search
   * - Priors
     - what was learned from past drives
     - not used
   * - Real-time
     - "Real time updated map information"
     - not used

- **Base map** is the raw 3D picture, like our L6 point cloud.
- **Geometric** is the shape of each lane. **Semantic** says what things
  are: lights, signs, crossings.
- **Road connectivity** says which lane leads to which. Our graph comes from
  this layer.
- **Priors** are what a fleet of cars learned from past drives about things
  that change over time: how traffic usually flows, where accidents happen,
  how a light usually cycles, which days a street allows parking. The AV
  uses them to predict, not only to react.
- **Real-time** is the live part: jams, closed roads, construction, the
  state of the lights, sent by other cars or by roadside equipment.
  ``Town01.xodr`` has neither priors nor a real-time layer: CARLA's map never
  changes. In GP4, your own sensors find a blocked road instead.

**From which sensors:** a survey vehicle collects the data with "a
combination of sensors, such as GPS, IMU, LiDARs, and cameras". The other
layers are then "extracted from" the base map (Elghazaly et al., 2023). At
the end of this subsection we ask whether ``Town01.xodr`` is an HD map.


.. _l7-lec-hdmap-uses:

What an HD Map Is Used For
^^^^^^^^^^^^^^^^^^^^^^^^^^

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
     - L7, today
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

.. tip::

   See *Where the map fits in the AV's architecture* and *The scene model at
   Waymo and Tesla* in :doc:`Going Further <l7_appendix>`.


.. _l7-lec-hdmap-sources:

Where an AV's Map Comes From
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Someone has to make these maps first. There are four ways:

.. list-table::
   :widths: 22 20 58
   :header-rows: 1
   :class: compact-table

   * - **Source**
     - **Example**
     - **How it is made**
   * - Survey cars with lidar
     - Waymo
     - "our team starts by manually driving our sensor equipped vehicles down
       each street, so our custom lidar can paint a 3D picture" (Waymo, 2020)
   * - Cameras on customers' cars
     - Mobileye REM (Road Experience Management)
     - "Millions of Mobileye-equipped ADAS vehicles sending data to the cloud
       in small data packets (10kb/km)" (Mobileye, REM)
   * - Shipped with the simulator
     - CARLA, ``Town01.xodr``
     - comes with the town; holds the geometric, semantic and connectivity
       layers
   * - Volunteers' street map
     - OpenStreetMap
     - streets drawn by volunteers; CARLA converts it to OpenDRIVE (later
       today)


.. _l7-lec-hdmap-loading:

When the Map Is Loaded, and When It Changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every AV loads its map before the trip. What happens during the trip differs.

.. list-table::
   :widths: 16 40 44
   :header-rows: 1
   :class: compact-table

   * - **Stack**
     - **Before the trip**
     - **During the trip**
   * - CARLA (this course)
     - The client gets the ``.xodr`` from the server once and builds a
       ``carla.Map`` from it (later today) (CARLA Team, Maps and
       navigation).
     - The map stays the same: "To change the map, the world has to change
       too" (CARLA Team, Maps and navigation).
   * - Autoware
     - Loads a Lanelet2 map and a point cloud map "before launching"
       (Autoware Foundation, Map interface).
     - With a divided point cloud map, it loads "the pointcloud map according
       to the vehicle's position" (Autoware Foundation, divided pointcloud
       map).
   * - Waymo
     - The car carries its map on board (Waymo, 2020).
     - It compares sensor data "with its on-board map", reroutes when a road
       changed, and tells the fleet (Waymo, 2020).
   * - HERE HD Live Map
     - Map layers cut into squares (tiles), from a cloud service (MathWorks,
       HERE HD Live Map Layers).
     - "Continuously updated map data" (MathWorks, HERE HD Live Map Layers).

.. note::

   Our planner reads ``Town01.xodr`` once, before the trip. It plans again
   when the route is blocked or the AV drifts off it (Re-planning, later
   today).

.. tip::

   See *HD map formats in practice*, *Lanelet* and *Lanelet2* in
   :doc:`Going Further <l7_appendix>`.


.. _l7-lec-hdmap-problems:

What Can Go Wrong with an HD Map
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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


.. _l7-lec-hdmap-town01:

Town01.xodr Against the Six HD Map Layers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Is ``Town01.xodr`` an HD map? Here it is layer by layer, from
:ref:`l7-lec-hdmap-layers`:

.. list-table::
   :widths: 20 38 42
   :header-rows: 1
   :class: compact-table

   * - **Layer**
     - **What it holds**
     - **In** ``Town01.xodr``
   * - Base map
     - 3D points or images of the area
     - no; CARLA ships it as a separate 190 MB point cloud (CARLA Team,
       autoware-contents)
   * - Geometric
     - the shape of each lane: points, lines, polygons
     - yes: the line each road is drawn along, lane widths
   * - Semantic
     - traffic lights, road signs, crossings
     - in part: 36 traffic lights, 22 speed signs; no stop lines or crossings
   * - Road connectivity
     - which lane leads to which
     - yes: junctions list which lane leads to which
   * - Priors
     - what was learned from past drives
     - no
   * - Real-time
     - "Real time updated map information"
     - no: "To change the map, the world has to change too" (CARLA Team,
       Maps and navigation)

.. note::

   **So:** ``Town01.xodr`` has the geometric and connectivity layers and part
   of the semantic layer. It is the lane-level part of an HD map, with no
   base layer and nothing that changes while the AV drives.


.. _l7-lec-file-to-graph:

From Map File to Graph
~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The parts that follow walk through the pipeline at the start of
   :ref:`l7-lec-map-to-graph`, one step at a time: the ``.osm`` file, the map
   file, ``carla.Map``, the segments, the waypoint graph and the intersection
   graph. Before each step, the diagram is shown again with that step
   outlined in yellow.


.. _l7-lec-osm:

A Map from OpenStreetMap
^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L7/map_pipeline_osm.png
   :alt: A UML activity diagram in two rows. It starts at a black dot, then a diamond, a choice. For your own area, the flow goes down to the object .osm file (OpenStreetMap), into the action Osm2Odr.convert(), and into the object map file (.xodr). For Town01, which comes with CARLA, the flow goes straight to the map file. The map file flows into the action carla.Map(name, text), which flows into the object carla.Map. Row 2: carla.Map flows into the object segments, then the action sample every 2 m, join in driving order, the object waypoint graph, the action keep S, G and 7 intersections, and the object intersection graph. The object .osm file and the action Osm2Odr.convert() are outlined in yellow.
   :width: 90%
   :align: center

   The pipeline, with the ``.osm`` file (OpenStreetMap) and
   ``Osm2Odr.convert()`` outlined in yellow.

First, where a map file comes from when you map an area yourself. You export
its streets from OpenStreetMap as an ``.osm`` file, and
``Osm2Odr.convert()`` turns it into a map file.

**OpenDRIVE** is the map format CARLA uses: "a common base for describing
road networks with extensible markup language (XML) syntax, using the file
extension xodr" (ASAM, ASAM OpenDRIVE).


.. _l7-lec-osm-campus:

A Map of Your Own, from OpenStreetMap
"""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/L7/campus_map.png
   :alt: A top view in meters of the streets around the University of Maryland's Kim Engineering Building, drawn as thin dark lane lines: a grid of campus roads in the middle and left, a highway with ramps crossing diagonally at the lower right, and a long road running east. An orange square marks the Kim Engineering Building, with tag 1 beside it, near the middle top. Axes: x east, y north.
   :width: 75%
   :align: center

   The streets around the University of Maryland's Kim Engineering Building,
   converted from OpenStreetMap, :math:`x` east and :math:`y` north in
   meters. Each dark line is the center of a lane. **1:** the orange square
   is the Kim building. Map data © OpenStreetMap contributors (ODbL).

1. Export an area from `openstreetmap.org
   <https://www.openstreetmap.org/export#map=16/38.99000/-76.93900>`__:
   your browser saves it as ``map.osm``.
2. ``carla.Osm2Odr.convert()`` turns the ``.osm`` text into OpenDRIVE text
   (CARLA Team, Generate maps with OpenStreetMap). The code is in the next
   part.
3. Read it with `carla.Map
   <https://carla.readthedocs.io/en/0.9.16/python_api/#carla.Map>`__: it
   builds the roads, lanes and waypoints from that text.

In the figure, **1** is the Kim building, and each line is the center of a
lane. The point :math:`(0, 0)` is at latitude 38.99, longitude −76.939. The
map has 314 roads, 46 intersections and 9144 waypoints at 2 m.


.. _l7-lec-osm-python:

From Your .osm File to a Map, in Python
"""""""""""""""""""""""""""""""""""""""

The steps of the last part, in Python:

.. code-block:: python

   osm = open("maps/umd_engineering.osm").read()
   settings = carla.Osm2OdrSettings()
   settings.proj_string = ("+proj=tmerc +lat_0=38.99 +lon_0=-76.939"
                           " +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m")
   settings.center_map = False      # keep its origin
   settings.use_offsets = False
   xodr = carla.Osm2Odr.convert(osm, settings)  # OpenDRIVE text
   m = carla.Map("campus", xodr)    # a map object

``proj_string`` sets how latitude and longitude become meters: :math:`x = 0`,
:math:`y = 0` is at latitude 38.99, longitude −76.939. With ``center_map``
on, the converter would move the origin to the center of the road map. With
``use_offsets`` on, it would shift the origin by an offset. Both stay off, so
the origin stays where ``proj_string`` puts it.

In class we run this code on the copy of the ``.osm`` file in the course
package, not on the file you just exported. ``osm_to_map.py``, in the folder
``lecture7``, does it for any export:

.. code-block:: bash

   python3 osm_to_map.py <location of map.osm>


.. _l7-lec-mapfile:

The Map File
^^^^^^^^^^^^

.. figure:: /_static/images/L7/map_pipeline_file.png
   :alt: A UML activity diagram in two rows. It starts at a black dot, then a diamond, a choice. For your own area, the flow goes down to the object .osm file (OpenStreetMap), into the action Osm2Odr.convert(), and into the object map file (.xodr). For Town01, which comes with CARLA, the flow goes straight to the map file. The map file flows into the action carla.Map(name, text), which flows into the object carla.Map. Row 2: carla.Map flows into the object segments, then the action sample every 2 m, join in driving order, the object waypoint graph, the action keep S, G and 7 intersections, and the object intersection graph. The object map file (.xodr) is outlined in yellow.
   :width: 90%
   :align: center

   The pipeline, with the map file (``.xodr``) outlined in yellow.

Next, the map file the rest of today uses: ``Town01.xodr``, which comes with
CARLA. We read one road of it.


.. _l7-lec-odr-road:

One Road in Town01.xodr
"""""""""""""""""""""""

Road 25, shortened from the file: numbers rounded, lanes and signals cut.
The highlighted lines are the four parts explained below the listing:
**1** is lines 1 and 2, **2** lines 4 to 7, **3** line 10, and **4** lines
13 to 17.

.. code-block:: xml
   :linenos:
   :emphasize-lines: 1-2,4-7,10,13-17

   <road name="Road 25"
     length="35.18" id="25" junction="-1">
    <link>
     <predecessor elementType="junction"
       elementId="54"/>
     <successor elementType="junction"
       elementId="332"/>
    </link>
    <type s="0" type="town">
     <speed max="25" unit="mph"/>
    </type>
    <planView>
     <geometry s="0" x="156.07"
       y="-11.02" hdg="-1.572"
       length="35.18">
      <line/>
     </geometry>
    </planView>
    ...
   </road>

1. **The road:** id 25, 35.18 m long. ``junction="-1"`` means it is not
   inside a junction.
2. **Its ends:** junction 54 at the start, junction 332 at the end.
3. **Its type,** ``town``, and its speed limit: 25 mph = 25 × 0.44704 =
   11.18 m/s.
4. **Its reference line,** the line the file draws the road along (next
   part): here one straight piece, ``<line/>``.

The listing cuts two more things:

- **Its lanes:** one 4.0 m driving lane on each side of the line (next
  part).
- **A junction** lists which lane leads to which (later in this section).

.. tip::

   See *A road's lanes in Town01.xodr*, *How the map draws a curve* and
   *Road 333's turn, step by step* in :doc:`Going Further <l7_appendix>`.


.. _l7-lec-odr-geometry:

Reading a Geometry Element
""""""""""""""""""""""""""

Road 25's ``<geometry>`` (**4**) draws its **reference line**, the line the
file draws the road along. Lanes are numbered from it: 1 on its left
(driving north here), −1 on its right (driving south).

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
2. The end, 35.18 m later: x = 156.07 + 35.18 cos(−90.07°) = 156.02 m and
   y = −11.02 + 35.18 sin(−90.07°) = −46.20 m. That point is junction 332.


.. _l7-lec-carla-map:

carla.Map
^^^^^^^^^

.. figure:: /_static/images/L7/map_pipeline_map.png
   :alt: A UML activity diagram in two rows. It starts at a black dot, then a diamond, a choice. For your own area, the flow goes down to the object .osm file (OpenStreetMap), into the action Osm2Odr.convert(), and into the object map file (.xodr). For Town01, which comes with CARLA, the flow goes straight to the map file. The map file flows into the action carla.Map(name, text), which flows into the object carla.Map. Row 2: carla.Map flows into the object segments, then the action sample every 2 m, join in driving order, the object waypoint graph, the action keep S, G and 7 intersections, and the object intersection graph. The action carla.Map(name, text) and the object carla.Map are outlined in yellow.
   :width: 90%
   :align: center

   The pipeline, with ``carla.Map(name, text)`` and the ``carla.Map`` object
   outlined in yellow.

Next, reading the map file in Python. ``carla.Map(name, text)`` takes a name
you choose and the text of the map file. It builds a map object we can ask
questions, with no CARLA server.


.. _l7-lec-read-map:

Read the Map File Yourself, with No CARLA Server
""""""""""""""""""""""""""""""""""""""""""""""""

CARLA's Python package reads an OpenDRIVE file on its own (CARLA Team,
Python API reference). Install it with ``pip install carla==0.9.16``. The
code below is ``read_map.py`` in the course's Python repo, folder
``lecture7`` (`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture7>`__).
Run it there with ``python3 read_map.py``.

.. code-block:: python

   import carla
   text = open("maps/Town01.xodr").read()
   m = carla.Map("Town01", text)      # no server needed
   wps = m.generate_waypoints(2.0)    # every 2 m, every lane
   segs = m.get_topology()            # (start, end) of each segment

.. list-table::
   :widths: 70 30
   :header-rows: 1
   :class: compact-table

   * - **Measured on Town01**
     - **Count**
   * - waypoints at 2 m, ``len(wps)``
     - 3266
   * - (start, end) waypoint pairs (next part), ``len(segs)``
     - 160
   * - traffic lights, ``<signal>`` of type 1000001 in the file
     - 36


.. _l7-lec-handson-map:

Hands-On: the Map File
""""""""""""""""""""""

``python3 l7_handson.py --part map``, in the folder ``lecture7``, opens
``Town01.xodr`` in a window, with no CARLA server. :doc:`The Code page
<l7_code>` and the folder's `README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture7>`__
give the setup and the commands.

.. figure:: /_static/images/L7/handson_map.png
   :alt: A screenshot of the map window: Town01 from above, x from 0 to 400 meters east and y from minus 330 to 0 meters north, drawn as dots along every lane, dark on the roads and amber inside the twelve intersections. A legend names the two kinds of dot. Under the map, a hint line, a Search box holding road 25, an x, y box holding 133.6, minus 129.4, and three buttons: Zoom in, Zoom out and Whole map.
   :width: 70%
   :align: center

   The map window, titled "Town01.xodr read offline: 122 roads, 3266
   waypoints at 2 m". **Dark dots:** waypoints on a road. **Amber dots:**
   waypoints inside an intersection. Below the map: a hint line, the
   **Search** box (here ``road 25``), the **x, y** box (here
   ``133.6, -129.4``), and the buttons **Zoom in**, **Zoom out** and
   **Whole map**.

.. admonition:: What to look at
   :class: hint

   - Each dot is a waypoint, 2 m apart: dark on a road, amber in an
     intersection.
   - Scroll, or use the buttons, to zoom.
   - **Search** takes an ID: ``road 25``, ``lane 25 -1`` (road 25, lane −1)
     or ``junction 332``. The **x, y** box finds the lane point nearest a
     point.
   - Click a waypoint: the window prints its road, its lane, and the line of
     ``Town01.xodr`` to open.


.. _l7-lec-find-start:

In Class: Find Our Start in the Map File
""""""""""""""""""""""""""""""""""""""""

Run ``python3 l7_handson.py --part map``, or follow on the screen.

1. Type our start, S, :math:`x = 133.6`, :math:`y = -129.4` m (the middle of
   the AV's rear axle), in the **x, y** box and press Enter. The window
   prints its road, its lane and :math:`s`.
2. Open ``Town01.xodr`` at the line it prints. Read the road's length, its
   speed limit, and the junction at each end (``predecessor``,
   ``successor``).
3. Lane 1 lies left of the road's reference line, and the file marks it
   backward, so it drives against :math:`s`, the distance along that line.


.. _l7-lec-segments:

Segments
^^^^^^^^

.. figure:: /_static/images/L7/map_pipeline_segments.png
   :alt: A UML activity diagram in two rows. It starts at a black dot, then a diamond, a choice. For your own area, the flow goes down to the object .osm file (OpenStreetMap), into the action Osm2Odr.convert(), and into the object map file (.xodr). For Town01, which comes with CARLA, the flow goes straight to the map file. The map file flows into the action carla.Map(name, text), which flows into the object carla.Map. Row 2: carla.Map flows into the object segments, then the action sample every 2 m, join in driving order, the object waypoint graph, the action keep S, G and 7 intersections, and the object intersection graph. The object segments is outlined in yellow.
   :width: 90%
   :align: center

   The pipeline, with the segments outlined in yellow.

Next, cutting the map into pieces a graph can use. The map's method
``get_topology()`` returns every lane of every road as a segment.


.. _l7-lec-segments-cut:

CARLA Cuts Every Lane at the Intersections
""""""""""""""""""""""""""""""""""""""""""

A route can change only where a lane leads to more than one lane. CARLA cuts
lanes there, and where the file starts a new road.

.. admonition:: Definition: Segment
   :class: note

   One lane of one road, in driving order. ``get_topology()`` returns each
   as two waypoints: "The first one is the origin and the second one
   represents another road end that can be reached" (CARLA Team, Python API
   reference).

.. figure:: /_static/images/L7/zoom_segments.png
   :alt: A top view, x from 86 to 170 meters east and y from minus 67 to minus 43 meters north, of the street between intersection 3 on the left and intersection 5 on the right. All lanes are light gray lines with light gray dots every 2 meters. Two segments are drawn thick and dark, each with dark dots on it and an arrow for its direction. Tag 1: the eastbound lane of the street, from a white circle at x 101.4 to a white circle at x 145.0, y minus 59.5. Tag 2: from that second white circle, a curve turning left through intersection 5 to a white circle at x 158.0, y minus 46.2.
   :width: 95%
   :align: center

   The street between intersection 3 (left) and intersection 5 (right).
   **Light gray:** the other lanes, with a dot every 2 m. **1:** one segment,
   the eastbound lane, from the white circle at :math:`x = 101.4` m to the
   one at :math:`x = 145.0` m. **2:** the next segment, a curve turning left
   through intersection 5, from that second white circle to the one at
   (158.0, −46.2) m. The arrows show each segment's direction.

- **1:** road 9's eastbound lane (lane −1), from intersection 3 to
  intersection 5: one segment, 43.6 m between its white ends.
- **2:** road 334, a short road inside intersection 5 that makes the left
  turn: the next segment, which starts where **1** ends.


.. _l7-lec-segments-count:

Town01's 160 Waypoint Pairs
"""""""""""""""""""""""""""

``get_topology()`` returns 160 pairs of waypoints for Town01, one pair per
segment and way out. Counted from the map:

1. Outside the intersections: 26 roads with one lane each way, so 26 × 2 =
   52 lanes.
2. 36 of those lanes end where the AV can go two ways, so each is listed
   twice, once for each lane it leads into: 52 + 36 = 88 pairs. Segment
   **1** of the last figure is one of them.
3. Through the intersections: 72 segments, 24 left turns, 24 right turns and
   24 straight on. So 88 + 72 = 160 pairs, for 52 + 72 = 124 segments.


.. _l7-lec-wpgraph:

The Waypoint Graph
^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L7/map_pipeline_wpgraph.png
   :alt: A UML activity diagram in two rows. It starts at a black dot, then a diamond, a choice. For your own area, the flow goes down to the object .osm file (OpenStreetMap), into the action Osm2Odr.convert(), and into the object map file (.xodr). For Town01, which comes with CARLA, the flow goes straight to the map file. The map file flows into the action carla.Map(name, text), which flows into the object carla.Map. Row 2: carla.Map flows into the object segments, then the action sample every 2 m, join in driving order, the object waypoint graph, the action keep S, G and 7 intersections, and the object intersection graph. The action sample every 2 m, join in driving order and the object waypoint graph are outlined in yellow.
   :width: 90%
   :align: center

   The pipeline, with "sample every 2 m, join in driving order" and the
   waypoint graph outlined in yellow.

Next, building the graph a search runs on: a waypoint every 2 m along each
segment, joined in driving order.

.. admonition:: Definition: Waypoint
   :class: note

   "A 3D-directed point in the CARLA world corresponding to an OpenDRIVE
   lane" (CARLA Team, Maps and navigation): a position on a lane, with the
   lane's heading there.


.. _l7-lec-routing-graph:

The Routing Graph: Waypoints Joined in Driving Order
""""""""""""""""""""""""""""""""""""""""""""""""""""

Segments are pieces of lanes; a search needs nodes and edges. CARLA's
waypoints give both.

.. admonition:: Definition: Directed graph
   :class: note

   A set of **nodes** and a set of **edges**, each edge an ordered pair
   (from, to) with a **cost**. An edge can be followed only from its first
   node to its second.

In CARLA's waypoint graph:

- a **node** is a waypoint, every 2 m along every lane;
- an **edge** goes from a waypoint to the next one along its lane, "in the
  direction of the lane" (CARLA Team, Maps and navigation); its cost is the
  length between them;
- the graph is **directed**: the AV cannot drive against its lane, so each
  edge points one way. The other lane of the road is its own chain of nodes.


.. _l7-lec-successors:

At an Intersection, One Node Has Two Successors
"""""""""""""""""""""""""""""""""""""""""""""""

The figure shows intersection 5 (junction 332): dots are nodes, gray arrows
are edges. A node's **successors** are the nodes its edges lead to.

.. figure:: /_static/images/L7/zoom_graph.png
   :alt: Intersection 5 as a graph, x from 126 to 186 meters east and y from minus 65 to minus 29 meters north: black dots for nodes, small gray arrows for the edges, every arrow pointing along its lane. Tag 1, with a short line, marks a white node where the southbound lane meets the intersection. Two thick dark lines leave it: one curves right and ends with an arrowhead pointing west at a second white node, tag 2, on the westbound lane; the other curves left and ends with an arrowhead pointing east on the eastbound lane.
   :width: 75%
   :align: center

   Intersection 5 as a graph: black dots are nodes, small gray arrows are
   edges, each pointing along its lane. **1:** the white node where the
   southbound lane meets the intersection. Two thick lines leave it: one
   curves right and ends pointing west at the white node **2**, on the
   westbound lane; the other curves left and ends pointing east, on the
   eastbound lane.

- **1, a split:** the lane meets the intersection, and the AV can go two
  ways. Two edges leave this node; the thick lines are the two ways that
  follow.
- **2, a merge:** two lanes from the intersection join one lane. Two edges
  arrive at this node.

Every other node has one edge in and one edge out. Town01 has 36 splits: 12
intersections with 3 roads into each.


.. _l7-lec-odr-junction:

A Junction Lists Which Lane Leads to Which
""""""""""""""""""""""""""""""""""""""""""

The file says which lanes those two edges lead to:

.. code-block:: xml

   <junction id="332"
     name="junction332">
    <connection id="0"
      incomingRoad="25"
      connectingRoad="333"
      contactPoint="start">
     <laneLink from="-1" to="-1"/>
    </connection>
    <connection id="3"
      incomingRoad="25"
      connectingRoad="339"
      contactPoint="start">
     <laneLink from="-1" to="-1"/>
    </connection>
     ...

This is junction 332, at the south end of road 25. The listing shows two of
its connections, from the file:

- Road 25's lane −1 (driving south) goes on into road 333 or road 339: the
  two ways out of the split in the last figure.
- ``laneLink from="-1" to="-1"``: lane −1 of road 25 continues in lane −1 of
  road 333, the right turn, or of road 339, the left turn. Roads 333 and 339
  are short roads inside the junction.
- ``name`` is a text label; our code uses the ``id``.


.. _l7-lec-odr-junction-read:

Reading a Junction Element
""""""""""""""""""""""""""

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


.. _l7-lec-rules-shape:

Traffic Rules Are in the Graph's Shape
""""""""""""""""""""""""""""""""""""""

Only the connections the file lists become edges, so the traffic rules are
in the graph.

.. figure:: /_static/images/L7/t_movements.png
   :alt: A top view in meters of intersection 306 in Town01, x from 76 to 114 meters east: two lanes running north and south on the left and two lanes to the east, with gray arrows showing each lane's driving direction. Six dark paths cross the intersection, each ending in an arrowhead. Tag 1: the two straight paths, solid lines, one south in the left lane and one north in the right lane. Tag 2: the two right turns, dashed, from the south into the east road and from the east road north. Tag 3: the two left turns, dotted, from the north into the east road and from the east road south. Tag 4: a faint gray dashed U-turn arc between the two north-south lanes below the intersection, with no arrowhead, crossed out with a dark x.
   :width: 60%
   :align: center

   Intersection 1 (junction 306), from above. Gray arrows show each lane's
   driving direction. **1:** the two straight paths (solid). **2:** the two
   right turns (dashed). **3:** the two left turns (dotted). **4:** a faint
   gray U-turn between the two north-south lanes, crossed out.

- This is intersection 1 on our route. The gray arrows show each lane's
  driving direction, and its edges point only that way.
- There are six ways through, one ``connection`` each in the file: **1**
  straight on (solid), **2** right turns (dashed), **3** left turns
  (dotted), two of each.
- **4:** a U-turn has no connection, so it has no edge, and no search can
  return it. ``Town01.xodr`` has 0 U-turn connections.


.. _l7-lec-town01-graph:

Town01's Graph
""""""""""""""

We built the graph the way CARLA's own route planner samples the map: each
segment from ``get_topology()``, a waypoint every 2 m along it, and segments
that meet share a node.

.. list-table::
   :widths: 44 56
   :header-rows: 1
   :class: compact-table

   * - **Measured**
     - **Town01, 2 m**
   * - nodes
     - 3107
   * - of them inside intersections
     - 652
   * - edges
     - 3143 = 3107 + 36: one edge out of each node, two out of each of the
       36 splits
   * - edge length: median (min, max)
     - 2.00 m (1.38, 4.03)
   * - lane length, all edges together
     - 6400.4 m

.. note::

   Where a lane ends and a single lane continues, the graph keeps one node,
   not two: 3266 − 3107 = 159 fewer nodes than ``generate_waypoints`` gives.
   At a split, each way out starts with its own node (see the hands-on
   next). After that, we search a nine-node graph by hand.


.. _l7-lec-handson-graph:

Hands-On: Town01's Graph
""""""""""""""""""""""""

``python3 l7_handson.py --part graph`` draws the real graph: all 3107 nodes
and 3143 edges. :doc:`The Code page <l7_code>` has the commands.

.. figure:: /_static/images/L7/handson_graph.png
   :alt: A screenshot of the graph window zoomed on one intersection, x from 78 to 124 meters east and y from minus 87 to minus 47 meters north. Dark dots 2 meters apart along two north-south lanes and two east-west lanes, joined by gray arrows that point the way each lane drives; curved chains of arrows cross the intersection. Two nodes are amber. Amber rings mark two points that each hold two nodes: one 2 meters after the lower amber node, one at the top of the left lane. A box at the bottom reads: node 224, at 92.4, minus 68.1 meters, heading 90 degrees, road 183, lane 1, in an intersection; successors: node 225, 2.00 meters, and node 2934, 2.00 meters; the two successors are 0.00 meters apart, ringed, and the two ways are more than 1 meter apart about 7 meters after this node.
   :width: 75%
   :align: center

   The graph window, zoomed on intersection 3. **Dark dots:** nodes.
   **Gray arrows:** edges, pointing the way each lane drives. **Amber
   dots:** splits, nodes with two successors. **Amber rings:** two nodes at
   one point, where a split's two ways start together. The box at the bottom
   is what a click on node 224 prints.

.. admonition:: What to look at
   :class: hint

   - Seen whole, the window shows the lanes in gray and the 36 splits in
     amber.
   - Scroll to zoom in at the mouse; drag to pan. Under 120 m across, nodes
     are dots and edges are arrows, the way the AV drives (here,
     intersection 3).
   - Click a node: the box prints its successors and each edge's length.
     Node 224, amber, has two successors, both 2.00 m ahead at one point
     (ringed): straight on and a right turn, which part about 7 m on.


.. _l7-lec-toy:

The Intersection Graph
^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L7/map_pipeline_toy.png
   :alt: A UML activity diagram in two rows. It starts at a black dot, then a diamond, a choice. For your own area, the flow goes down to the object .osm file (OpenStreetMap), into the action Osm2Odr.convert(), and into the object map file (.xodr). For Town01, which comes with CARLA, the flow goes straight to the map file. The map file flows into the action carla.Map(name, text), which flows into the object carla.Map. Row 2: carla.Map flows into the object segments, then the action sample every 2 m, join in driving order, the object waypoint graph, the action keep S, G and 7 intersections, and the object intersection graph. The action keep S, G and 7 intersections and the object intersection graph are outlined in yellow.
   :width: 90%
   :align: center

   The pipeline, with "keep S, G and 7 intersections" and the intersection
   graph outlined in yellow.

Last, the **intersection graph**: S, G and seven intersections of the same
streets, joined by the roads between them. It is small enough to search by
hand.


.. _l7-lec-toy-map:

The Intersection Graph on the Map
"""""""""""""""""""""""""""""""""

.. figure:: /_static/images/L7/toy_on_map.png
   :alt: Town01's lanes in light gray, with the intersection graph drawn over them: nine white circles labeled S, 1 to 7 and G, joined by straight black lines. S sits on a street east of node 1. Node 1 has node 2 below it and node 3 above it; node 3 joins node 4 above and node 5 to the right; nodes 4 and 5 both join node 6, which joins G to its right; node 5 also joins node 7 far to the east.
   :width: 70%
   :align: center

   The intersection graph drawn over Town01's lanes (light gray): nine
   nodes, S, 1 to 7 and G, joined by straight black lines. S lies east of
   1; 2 is below 1 and 3 above it; 3 joins 4 and 5; 4 and 5 both join 6,
   which joins G; 5 also joins 7, far to the east.

- **Nodes:** S, G, the intersections 1, 3, 5 and 6 on our route, and 2, 4
  and 7 beside it. Each intersection node sits at the center of CARLA's
  rectangle around that intersection. The rectangle reaches into the side
  street, so some edges tilt.
- **Edges:** the roads between the nodes, in whole meters along the lane.
- One edge stands for a street's two lanes, one each way, with their average
  length. The two lanes' lengths differ by 1.66 m at most.


.. _l7-lec-toy-lengths:

Edge Lengths in the Intersection Graph
""""""""""""""""""""""""""""""""""""""

Each edge of the intersection graph needs a cost. Here, the cost is its
length.

.. figure:: /_static/images/L7/toy_base.png
   :alt: The intersection graph alone, to scale, nodes as white circles. Edge lengths in meters beside each edge: S to 1, 41, with an arrow from S to 1; 1 to 2, 67; 1 to 3, 75; 3 to 4, 55; 3 to 5, 64; 4 to 6, 66; 5 to 6, 53; 5 to 7, 179; 6 to G, 40, with an arrow from 6 to G.
   :width: 65%
   :align: center

   The intersection graph alone, to scale, with each edge's length in
   meters: S to 1, 41 (arrow from S); 1 to 2, 67; 1 to 3, 75; 3 to 4, 55;
   3 to 5, 64; 4 to 6, 66; 5 to 6, 53; 5 to 7, 179; 6 to G, 40 (arrow
   into G).

- The cost of each edge is its length in meters.
- G has an arrow because it is reached only from 6.
- Three edges leave our route, so the search has choices: south at 1
  (toward 2), straight on at 3 (toward 4), and east at 5 (toward 7).

Our route is 41 + 75 + 64 + 53 + 40 = 273 m on the intersection graph and
260.6 m on the waypoint graph: 12.4 m more on the intersection graph. This
graph measures to each intersection's center, and the lanes cut through the
turns.


.. _l7-lec-check-graph:

Check: the Graph
""""""""""""""""

.. admonition:: Question
   :class: hint

   The street between S and node 1 has two lanes, one each way. Why does the
   intersection graph give S only one edge, S to 1, and no edge from 1 back
   to S?

.. dropdown:: Answer
   :color: success
   :icon: check-circle

   **S is a point in the westbound lane.** The AV starts there facing west,
   so it can only drive toward 1. A route back to S would arrive in the
   westbound lane from the east, through the intersection at the street's
   other end, which is outside the intersection graph. In the waypoint graph
   the two lanes are separate chains of nodes, so the one-way start comes
   from the graph itself.


.. _l7-lec-lanes:

Lane Changes
------------

The AV must be in the right lane before a turn, and lane change edges get it there.

**What it is for:** GP4's second town, Town03, has roads with two lanes each way.

In Town01, every road has one lane each way, so the road the AV takes also
fixes its lane. The graph needs only two kinds of edge: along a lane, and
through an intersection.

GP4 also runs in Town03, where many roads have two lanes the same way, and
the lane decides the turns. On road 4 (the map file numbers each road), only
the left lane can turn left at junction 238 (the map file's number for that
intersection).

So the graph needs a third kind of edge, the **lane change**, and a route
must use one to reach the right lane before the intersection. Without it, an
AV in the right lane has no route to that left turn.


.. _l7-lec-edge-kinds:

Three Kinds of Edge
~~~~~~~~~~~~~~~~~~~

Town03's road 4 has two lanes driving south toward junction 238, so its graph
needs a third kind of edge.

.. figure:: /_static/images/L7/edge_kinds.png
   :alt: Town03's road 4 approaching junction 238 from the north, drawn as a graph: dark dots every 4 meters along two southbound lanes, joined by gray arrows pointing south; dashed gray arrows cross between the two lanes in X shapes; at the intersection, chains of arrows turn right to the west, go straight on, or turn left to the east. Three edges are dark and tagged: tag 1, an arrow along the west lane; tag 2, a dashed arrow from the west lane to the east lane; tag 3, a short arrow at the end of the east lane, just before its arrows split into the left turn and the straight way.
   :width: 60%
   :align: center

   Road 4 drawn as a graph, in meters (:math:`x` east, :math:`y` north).
   Dark dots are nodes; gray arrows run south along the two lanes, and dashed
   gray arrows cross between them in X shapes. At the bottom, the west lane's
   arrows turn right to the west or go straight on; the east lane's go
   straight on or turn left to the east. **1**, **2** and **3** are the three
   dark edges.

- **1 Lane follow:** the AV stays in its lane. The edge joins a waypoint to
  the next one in the same lane.
- **2 Lane change:** the AV moves to the lane beside it. The edge joins a
  waypoint to one two nodes ahead in that lane (8 m in this drawing).
- **3 Through an intersection:** the AV crosses. The edge joins a lane's
  last waypoint to the first waypoint of a turn, or of the straight way
  across.

Dots are nodes, 4 m apart here (2 m in the real graph). Dashed arrows change
lanes; only every third pair is drawn.


.. _l7-lec-road4:

Road 4's Five Lanes
~~~~~~~~~~~~~~~~~~~

OpenDRIVE numbers a road's lanes outward from its **reference line**, the
line the file draws the road along: 1, 2, 3 on its left and −1, −2 on its
right, looking the way the reference line points (south). Here are 20 m of
Town03's road 4, before junction 238.

.. figure:: /_static/images/L7/road4_lanes.png
   :alt: A top view of 20 meters of Town03's road 4, five lanes side by side, tagged 1 to 5 from west to east. Lanes 1 and 2 have arrows pointing south, lanes 4 and 5 arrows pointing north, and the shaded middle lane, tag 3, an arrow pointing both ways. Solid lines run along the outer edges; broken lines separate lanes 1 and 2, and lanes 4 and 5; each side of the middle lane has a double line, one broken and one solid.
   :width: 45%
   :align: center

   Road 4 from above, in meters. Tags **1** to **5** mark the five lanes from
   west to east. The arrows show the way each lane drives: **1** and **2**
   south, **4** and **5** north, and the shaded middle lane **3** both ways.

- **1** Lane −2 and **2** lane −1 drive south.
- **3** Lane 1, in the middle, is a center lane that traffic from both
  directions may use (OpenDRIVE type ``bidirectional``), so its arrow points
  both ways.
- **4** Lane 2 and **5** lane 3 drive north.
- The lines are painted as ``Town03.xodr`` gives them. A broken line may be
  crossed; a solid line may not. On a double line, the half on the AV's side
  decides.
- The tags are not lane numbers: tags 1 to 5 mark lanes −2, −1, 1, 2, 3.


.. _l7-lec-lane-change-field:

Where a Lane Change Is Allowed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each CARLA waypoint has a field, ``lane_change``, that says to which side an
AV on it may change lanes: ``NONE`` (neither), ``Left``, ``Right`` or
``Both`` (CARLA Team, 2026, *Maps and navigation*). Left and right are seen
from the AV, facing the way its lane drives.

.. figure:: /_static/images/L7/lane_change_marks.png
   :alt: A top view of 20 meters of Town03's road 4, five lanes side by side, labeled with their lane numbers minus 2, minus 1, 1, 2 and 3 from west to east. Lanes minus 2 and minus 1 have arrows pointing south, lanes 2 and 3 arrows pointing north, and the shaded middle lane 1 an arrow pointing both ways. Solid lines run along the outer edges; broken lines separate lanes minus 2 and minus 1, and lanes 2 and 3; each side of the middle lane has a double line, one broken and one solid. Curved arrows show the allowed moves: purple from lane minus 2 into lane minus 1, from lane minus 1 into the middle lane, and from lane 3 into lane 2; orange from lane minus 1 into lane minus 2, and from lane 2 into lane 3.
   :width: 45%
   :align: center

   The same 20 m of road 4, now labeled with the lane numbers. The curved
   arrows are the moves the map allows. **Purple:** moves to the AV's left
   (lane −2 into −1, lane −1 into the center lane 1, lane 3 into 2).
   **Orange:** moves to the AV's right (lane −1 into −2, lane 2 into 3). **Gray:** the way
   each lane drives.

- Lane −2 says ``Left``: an AV there may move only to its left, into lane −1.
- Lane −1 says ``Both``: an AV there may move right, into lane −2, or left,
  into the center lane.
- Lane 1 has no waypoints (CARLA's ``generate_waypoints`` skips it), so our
  graph has no node there.
- Lane 2 says ``Right``: an AV there may move only to its right, into lane 3,
  not into the center lane.
- Lane 3 says ``Left``: an AV there may move only to its left, into lane 2.

Our graph adds a lane change edge only between lanes that drive the same way.
The move from lane −1 into the center lane gets no edge.


.. _l7-lec-lanes-towns:

Lanes and Lane Changes in Town01 and Town03
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These counts were measured with ``carla.Map`` on each town's file, with
waypoints every 2 m. A **road section** is a stretch of one road with a fixed
set of lanes. An **approach** is one road's lanes entering one intersection.

.. list-table::
   :widths: 56 22 22
   :header-rows: 1
   :class: compact-table

   * -
     - **Town01**
     - **Town03**
   * - waypoints
     - 3266
     - 7092
   * - road sections outside the intersections with 2 or more lanes the
       same way
     - 0 of 26
     - 37 of 68
   * - waypoints where the map allows a lane change
     - 0
     - 4241
   * - approaches to an intersection with 2 or more lanes
     - 0
     - 49 of 89
   * - of them, approaches whose lanes lead to different turns
     - 0
     - 22

.. note::

   At 22 of Town03's approaches, the turn decides which lane the AV must be
   in before it reaches the intersection.


.. _l7-lec-town03-left:

Turning Left in Town03
~~~~~~~~~~~~~~~~~~~~~~

In Town03 the route must pick the lane before a turn. Road 4 has two lanes
driving south, toward junction 238.

.. figure:: /_static/images/L7/town03_lanes.png
   :alt: A top view in meters of road 4 in Town03 approaching junction 238 from the north, with the other lanes in light gray. Two lanes drive south: the left one teal, tag 1, the right one brown, tag 2. At the bottom, the teal lane goes straight on or turns left, toward the east; the brown lane goes straight on or turns right, toward the west. Short dashed black arrows, tag 3, run diagonally from the brown lane to the teal lane along the approach.
   :width: 40%
   :align: center

   Road 4 from above, in meters. **1** the left lane (teal), which goes
   straight on or turns left to the east. **2** the right lane (brown), which
   goes straight on or turns right to the west. **3** dashed black arrows,
   lane changes from the brown lane to the teal one. Gray: the other lanes'
   centers.

- **1** The left lane (teal): left or straight on.
- **2** The right lane (brown): right or straight on.
- **3** Dashed arrows: lane changes from the right lane to the left one. The
  map allows them on all 92 m of road 4; the last 60 m are drawn, one every
  10 m.

The cost of a lane change edge is its length plus a penalty (not set in this
example). The search then decides where the AV changes lanes.


.. _l7-lec-check-lanes:

Check: Lane Changes
~~~~~~~~~~~~~~~~~~~

**Question.** In Town03, the AV drives south on road 4 in the right lane and
must turn left at junction 238. Which edges must its route contain, in order?

.. dropdown:: Answer
   :class-container: sd-border-success

   .. figure:: /_static/images/L7/town03_graph.png
      :alt: Town03's road 4 approaching junction 238 from the north, drawn as a graph: x from about minus 107 to minus 57 meters east, y from minus 140 to minus 85 meters north, other lanes in light gray. Dark dots every 4 meters along the two southbound lanes, joined by gray arrows pointing south. Dashed gray arrows cross between the two lanes in X shapes, one pair every 12 meters. At the intersection, the west lane's arrows go straight on south or turn right to the west; the east lane's go straight on south or turn left to the east. One thick dark route: tag 1, south along the west lane; tag 2, a dashed dark arrow into the east lane; tag 3, south along the east lane; tag 4, the left turn to the east, ending in an arrowhead.
      :width: 60%
      :align: center

      The route drawn thick and dark on road 4's graph: **1** south along the
      west lane (the AV's right lane), **2** a dashed arrow into the east lane,
      **3** south along the east lane (the AV's left lane), **4** the left turn
      to the east.

   Dots are nodes, 4 m apart here (2 m in the real graph). Dashed arrows
   change lanes; only every third pair is drawn.

   1. **1** Lane follow edges, right lane.
   2. **2** One lane change edge.
   3. **3** Lane follow edges, left lane.
   4. **4** The left turn through 238.

   From the right lane, the paths through 238 go only right or straight on,
   so a route with no lane change edge cannot turn left there.


.. _l7-lec-costs:

Edge Costs
----------

An edge can cost its length, its driving time, or its length plus a penalty for a left turn.

**What it is for:** the cost decides which route is "best"; the search only finds it.


.. _l7-lec-three-costs:

Three Costs for the Same Edge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The search adds up the costs of a route's edges and keeps the route with the
smallest total. We can set the cost of an edge :math:`\ell` meters long in
three ways:

1. **Distance.** The cost of the edge is its length, :math:`\ell` meters. The
   search then finds the shortest route.
2. **Travel time.** The cost is the time the AV will need for the edge,
   :math:`\ell / v` seconds, with :math:`v` worked out from the map before
   the drive: the speed limit, or less in a turn. The search then finds the
   fastest route. A 100 m edge costs 100 / 11.18 = 8.9 s at 25 mph
   (11.18 m/s), but 100 / 6.71 = 14.9 s at 15 mph (6.71 m/s): 6.0 s more.
3. **Left-turn penalty.** The cost is the edge's length in meters. The edge
   that starts a left turn costs :math:`P` meters more. To the search, every
   left turn then looks like :math:`P` extra meters of road.

.. note::

   - **The speed** :math:`v`: the speed limit is not a cost by itself, but it
     sets :math:`v` in :math:`\ell / v`.
   - **The penalty** :math:`P`: 30 m, chosen for this example. A route with no
     left turn then beats one with a left turn if it is less than 30 m
     longer. A left turn crosses oncoming traffic, so a planner may avoid it.


.. _l7-lec-turn-slow:

In a Turn, the AV Must Slow Down
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The travel-time cost needs the AV's speed on each edge. In a curve, a limit on
how hard the AV may accelerate toward the center caps that speed.

.. figure:: /_static/images/L7/turn_geometry.png
   :alt: A top view of a lane turning left: it comes from the left, curves through a quarter circle and leaves upward. A dark dot, tag 1, marks the circle's center. A dashed line, tag 2, runs from the center to the AV, which drives along the curve. An arrow along the lane ahead of the AV is tag 3; an arrow from the AV toward the center is tag 4.
   :width: 60%
   :align: center

   A left turn from above. The lane comes from the left and leaves upward.
   **1** the center of the circle the lane follows. **2** the radius
   :math:`r`, to the AV's base link (the middle of its rear axle). **3** the
   AV's velocity, along the lane. **4** its acceleration, toward the center.
   The arrows show directions only.

To follow a curve, the AV must accelerate toward the curve's center (**4**).
Passengers feel this as a push toward the outside.

- The acceleration is :math:`v^2 / r`, in m/s²: :math:`v` is the AV's speed
  (m/s) (**3**), and :math:`r` is the radius (m) (**2**) of the circle the
  lane follows.
- A small :math:`r` is a tight curve, so :math:`v^2 / r` is large.
- To keep the ride comfortable, we keep it at or below a limit
  :math:`a_{\mathrm{lat}}` ("lat" for lateral, sideways):
  :math:`v^2 / r \le a_{\mathrm{lat}}`.
- Multiply both sides by :math:`r` and take the square root: the top speed in
  a curve is :math:`\sqrt{a_{\mathrm{lat}}\, r}`.


.. _l7-lec-turn-speed:

Top Speed in Town01's Turns
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/turn_speed.png
   :alt: A graph, not a map: top speed in meters per second against the curve's radius in meters, 0 to 90. A solid dark curve rises from 0 and becomes flat at about 11.2 meters per second from a radius of about 62 meters on. Dots on it: tag 1 at radius 7.2 and speed 3.8, tag 2 at radius 11.5 and speed 4.8, tag 3 where it becomes flat. Tag 4 points at the flat part. A dotted gray line marks 11.18 meters per second across the graph, and a dashed gray curve, tag 5, keeps rising above the flat part.
   :width: 75%
   :align: center

   A graph, not a map: the top speed (m/s) against the curve's radius
   :math:`r` (m). **1** and **2** the median right and left turns. **3**
   :math:`\sqrt{2.0\, r}` meets the limit at
   :math:`r = 11.18^2 / 2.0 = 62.5` m. **4** the limit, above 62.5 m. **5**
   :math:`\sqrt{2.0\, r}` alone (dashed).

1. The limit: :math:`a_{\mathrm{lat}} = 2.0` m/s², chosen for this example.
2. **1** Town01's 24 right-turn lanes have a median radius of 7.2 m (from the
   map): √(2.0 × 7.2) = √14.4 = 3.79 m/s.
3. **2** Its 24 left-turn lanes have a median of 11.5 m:
   √(2.0 × 11.5) = √23 = 4.80 m/s.
4. On a straight lane, the AV drives at the speed limit, 11.18 m/s.

The solid line is the top speed: the lower of :math:`\sqrt{2.0\, r}` and the
speed limit (dotted).

.. note::

   **Travel time of an edge:** its length divided by the lower of the speed
   limit and the curve's top speed. A meter of the median left turn takes
   11.18 / 4.80 = 2.3 times as long as a straight meter; a meter of the
   median right turn, 11.18 / 3.79 = 2.9 times.


.. _l7-lec-costs-code:

The Three Costs in Code
~~~~~~~~~~~~~~~~~~~~~~~

The costs in this section were computed this way, for all 3143 edges at once:
edge ``i`` goes from node ``ef[i]`` to node ``et[i]`` and is ``el[i]`` meters
long.

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
- ``v_limit`` is 11.18 m/s, ``a_lat`` is 2.0 m/s² and ``P`` is 30 m, as in
  the last subsections.
- A straight edge has ``kappa`` 0. ``np.maximum`` keeps the division finite,
  so the speed limit sets ``v``.
- ``is_left`` is true on the first edge of each left turn, so a left turn
  adds ``P`` once.


.. _l7-lec-routes-costs:

Routes under Three Costs
~~~~~~~~~~~~~~~~~~~~~~~~

The same trip, searched once with each cost. Blue: the distance route; dashed
rust: the travel-time route, which the penalty also picks.

.. figure:: /_static/images/L7/routes_costs.png
   :alt: A top view of part of Town01's lanes, with intersections 1 to 6 marked by small gray numbered circles. A thick blue line, the shortest-distance route, runs from S west to intersection 1, north to 3, east to 5, north to 6 and east to G. A dashed rust line, the fastest route, shares the part from S to 3, then continues north to 4, east past 6 and on to G.
   :width: 50%
   :align: center

   Part of Town01 from above, in meters, with intersections 1 to 6 in gray
   circles. **Blue:** the distance route, from S through 1, 3, 5 and 6 to G.
   **Dashed rust:** the travel-time route, the same from S to 3, then north
   to 4 and east past 6 to G.

.. list-table::
   :widths: 34 26 20 20
   :header-rows: 1
   :class: compact-table

   * - **Cost**
     - **Through**
     - **length (m)**
     - **time (s)**
   * - distance
     - 1, 3, 5, 6
     - 260.6
     - 31.0
   * - travel time
     - 1, 3, 4, 6
     - 266.9
     - 27.7
   * - left-turn penalty
     - 1, 3, 4, 6
     - 266.9
     - 27.7

- **Rust:** 266.9 − 260.6 = 6.3 m longer, 31.0 − 27.7 = 3.3 s faster. It has
  two turns against blue's four, and each turn caps the speed.
- **Penalty:** blue's left turn at 5 adds 30 m to its cost:
  260.6 + 30 = 290.6 m, more than rust's 266.9 m. Any :math:`P` above 6.3 m
  picks rust.
- A search uses one cost. The rest of this lecture uses distance; in GP4 you
  choose.

.. tip::

   See "Traffic lights add waiting time" in :doc:`Going Further
   <l7_appendix>`.


.. _l7-lec-handson-costs:

Hands-On: the Edge Costs
~~~~~~~~~~~~~~~~~~~~~~~~

The ``costs`` part of the hands-on script shows every edge's three costs, and
the routes of the last subsection. The commands are on :doc:`the Code page
<l7_code>`.

.. figure:: /_static/images/L7/handson_costs.png
   :alt: A screenshot of the left panel of the costs window: every edge of Town01, light gray on the straight lanes and dark gray to black in the turns, with a scale under it from 0 to about 0.33 seconds per meter. Twenty-four small rings mark the left-turn edges; a legend says a left turn adds 30 meters in the penalty cost. A thick black mark near x 146 meters, y minus 59 meters is the clicked edge. A box at the bottom lists edge 0, node 0 to node 1, and edge 31, node 0 to node 33, a left turn: both 2.00 meters and 0.179 seconds at the speed limit; with the penalty, edge 0 costs 2.00 meters and edge 31 costs 32.00 meters.
   :width: 75%
   :align: center

   The left panel of the costs window. Every edge of Town01 is shaded by the
   seconds it takes to drive one meter (:math:`1/v`): light on the straight
   lanes, dark in the turns. Rings mark the left-turn edges. The black mark
   near :math:`x` = 146 m, :math:`y` = −59 m is the clicked edge, and the box
   at the bottom prints the costs of edges 0 and 31.

- Each edge is darker where one meter takes longer: the AV slows in the
  turns. Rings mark the 24 left-turn edges.
- Click an edge: it turns thick black, and the box prints its three costs.
  Here edges 0 and 31 leave node 0 along the same first 2 m, where the heading
  does not change yet. Both cost 2.00 m and 0.179 s, but edge 31 starts a
  left turn, so its penalty cost is 32.00 m.
- The window's right panel draws the three routes.


.. _l7-lec-search:

Search
------

You know Dijkstra (Dijkstra, 1959) and A* (Hart et al., 1968) from the planning course, so their recap is in the appendix.

**What it is for:** GP4 needs a heuristic that never overestimates, in the same units as the edge costs.

The recap, "Dijkstra and A*: the recap", is in :doc:`Going Further
<l7_appendix>`. Every step of both searches on the intersection graph is on
:doc:`l7_search_steps`.


.. _l7-lec-scale:

At Scale
--------

The appendix runs the same two searches on Town01's full waypoint graph, 3107 nodes.

**What it is for:** how much work A*'s heuristic saves on a real map, and why GP4 stops a search after ``max_astar_nodes``, 10,000 nodes.

The searches on Town01 are in :doc:`Going Further <l7_appendix>`. The same two
searches on the small intersection graph, step by step, are on
:doc:`l7_search_steps`.


.. _l7-lec-replan:

Re-planning
-----------

The planner searches again while the AV drives, and must not switch routes back and forth.

**What it is for:** GP4's planner must re-plan on two triggers.

The map does not know about a stalled truck, and the AV does not drive
exactly on its route. If the truck blocks the route, or the AV ends up too far
from it, the AV needs a new route.


.. _l7-lec-triggers:

GP4's Two Triggers
~~~~~~~~~~~~~~~~~~

While the AV drives, an object can block the route, or the AV can end up away
from it; GP4's planner then plans again. GP4 calls the route's waypoints the
**path**: the planner publishes them as a ``nav_msgs/Path`` message.

.. figure:: /_static/images/L7/triggers.png
   :alt: Two panels to scale, each with a straight blue path along x from 0 to 30 meters, black dots every 2 meters. Panel 1, trigger 1, an object within 3.0 m of the path: the AV at the left on the path; a red X 2.0 m beside the path at x 20 with a red circle of radius 3 meters around it; the three path points inside the circle are red. Panel 2, trigger 2, the AV more than 2.0 m off the path: the AV 2.5 m to the side of the path, with a double arrow from its rear axle down to the nearest path point, labeled 2.5 m.
   :width: 95%
   :align: center

   Two panels to scale, in meters. **Left, trigger 1:** the AV on the path;
   a red X 2.0 m beside the path at :math:`x` = 20 m, a red circle of 3.0 m
   around it, and the three waypoints inside it in red. **Right, trigger 2:**
   the AV 2.5 m to the side of the path, with a double arrow from its rear
   axle to the nearest waypoint.

1. **An obstacle on the path.** Perception reports an object whose center is
   within ``obstacle_clearance``, 3.0 m, of a waypoint. In panel 1, it is
   2.0 m beside the path, and three waypoints (red) are that close.
2. **The AV off the path.** The AV's base link is more than
   ``max_deviation``, 2.0 m, from the nearest waypoint. In panel 2, it is
   2.5 m away.

Blue line: the path; black dots: its waypoints, 2 m apart. Red X: the
object's center; red circle: the points within 3.0 m of it. 3.0 m and 2.0 m
are GP4's settings, in ``planner_config.yaml``; the object's 2.0 m and the
AV's 2.5 m (double arrows) are chosen for this example.


.. _l7-lec-replan-example:

An Obstacle on the Road from 5 to 6
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/replan.png
   :alt: A top view of the trip's area with intersections 3 to 6 marked by small gray circles. The AV, tag 1, drives north on the left street below intersection 3. The old route, thick blue, goes from the AV north to 3, east to 5, north to 6 and east to G. On the street from 5 to 6, tag 2: a red X inside a red circle of radius 3 meters on the blue route. The new route, dashed green, goes from the AV north past 3 to 4, then east past 6 to G.
   :width: 75%
   :align: center

   The trip's area from above, in meters, with intersections 3 to 6 in gray
   circles. **1** the AV, driving north below intersection 3. **Blue:** the
   old route, through 3, 5 and 6 to G. **2** the obstacle: a red X in a red
   circle, on the blue route from 5 to 6. **Dashed green:** the new route,
   north past 3 to 4, then east past 6 to G.

The AV (**1**) drives north, 23 m before the center of intersection 3 (a
position chosen for this example). Its blue route turns right at 3 and left
at 5.

1. Perception reports an obstacle (**2**) on the road from 5 to 6, 0.25 m
   from a blue waypoint (placed for this example). That is less than 3.0 m,
   so trigger 1 fires. The red circle shows the 3.0 m around the obstacle.
2. The planner deletes the 4 edges that start or end within 3.0 m of the
   obstacle. The graph no longer has a road from 5 to 6.
3. It searches again, from the waypoint nearest the AV to G. The new route
   (green, dashed) goes straight on at 3 and turns right at 4.
4. The new route is 178.9 m long; the blue route had 172.6 m left. The detour
   adds 178.9 − 172.6 = 6.3 m.


.. _l7-lec-replan-rules:

Re-plan from Where the AV Is, at a Fixed Rate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a trigger fires, the planner searches again. Three rules decide where
and when:

- **Start from the waypoint nearest the AV, not from S.** The AV has already
  driven part of the route. The new search starts at the waypoint nearest the
  AV, in the AV's lane and facing the way it drives.
- **Check at a fixed rate.** The planner checks the triggers twice a second
  (GP4's ``replan_frequency``, 2.0 Hz), so a new obstacle waits at most 0.5 s
  for the next check. At 8.0 m/s (the controller's default
  ``target_speed``), the AV drives up to 8.0 × 0.5 = 4.0 m in that time.
- **Check often, search rarely.** A check only measures distances to the
  route's waypoints, which is fast. A search runs only when a trigger fires.

.. note::

   GP4 notes that the CARLA API "is not thread-safe": it can break when two
   threads call it at the same time. With rclpy's default executor, a timer
   callback runs on the same thread as the node's other callbacks. So run the
   check in a timer callback, not in a thread of its own.


.. _l7-lec-hysteresis:

Do Not Switch Routes at Every Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A detector can miss an obstacle at one check and see it at the next. Each
column of the figure is one check. Rows 2 and 3 show the route the planner
picks: A (blue), the original route, or B (green), which goes around the
obstacle.

.. figure:: /_static/images/L7/hysteresis.png
   :alt: A timeline of ten checks, 0 to 4.5 seconds, 0.5 s apart. Row 1: red squares where the detector reports the obstacle, at 0, 1, 1.5 and 2.5 s; white squares elsewhere. Row 2, with no rule: the route at each check, green B whenever row 1 is red, blue A otherwise, so it changes five times. Row 3, with the rule: green B from 0 to 3.5 s, then blue A at 4 and 4.5 s, one change.
   :width: 80%
   :align: center

   Ten checks, 0 to 4.5 s, 0.5 s apart. **Row 1:** red where the detector
   reports the obstacle (0, 1, 1.5 and 2.5 s). **Row 2:** the route with no
   rule. **Row 3:** the route with the rule: B until 3.5 s, A from 4 s.

1. Row 1 is red when the detector reports the obstacle (pattern chosen for
   this example).
2. Row 2: B at every red check, A at every white one. The route changes 5
   times in 4.5 s.
3. Row 3, with a rule: B from the first red check, and back to A at the third
   white check in a row (3 is chosen). The route changes once, at 4 s.

.. note::

   A rule that waits before switching back is called **hysteresis**. Without
   it, L9's motion planner could get a new route to follow as often as every
   half second.


.. _l7-lec-check-replan:

Check: Re-planning
~~~~~~~~~~~~~~~~~~

**Question.** At one check, the localizer's pose is 2.3 m toward the other
lane; at the next check, it is back, as after a bad scan match in L6. The AV
itself never leaves its lane. What does trigger 2 do, and what should the
planner do?

.. dropdown:: Answer
   :class-container: sd-border-success

   **Trigger 2 fires**, because 2.3 m is more than 2.0 m. The planner throws
   away a good route and searches again because of one bad pose. The new
   start still lands on the AV's own lane, because it must face the way the
   AV drives, but the search is wasted. The planner should re-plan only when
   the deviation shows on 2 checks in a row (2 is chosen): hysteresis again.
   The 2.3 m is chosen for this example.


.. _l7-lec-maneuvers:

Maneuvers
---------

We turn the route into maneuvers, the move the AV makes at each intersection.

**What it is for:** what the next lectures' planners (L8, behavior; L9, motion planning) need from the route besides its waypoints.


.. _l7-lec-route-maneuvers:

Our Route as Four Maneuvers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/route_maneuvers.png
   :alt: A top view of part of Town01 with the trip's route in blue from S, west to intersection 1, north to 3, east to 5, north to 6 and east to G. Gray circles label the intersections 1, 3, 5 and 6.
   :width: 50%
   :align: center

   The trip's route in blue, in meters: from S west to intersection 1, north
   to 3, east to 5, north to 6 and east to G.

Besides the waypoints, the next lectures' planners (L8, L9) need what the AV
does at each intersection on the route.

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Intersection**
     - **Maneuver**
   * - 1
     - turn right
   * - 3
     - turn right
   * - 5
     - turn left
   * - 6
     - turn right

Between intersections, the AV follows its lane.

We label each intersection by how much the heading turns in it: more than 30°
left is a left turn, more than 30° right a right turn, less is straight on. We
chose 30°.


.. _l7-lec-following:

Following the Route While Driving
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Between re-plans, the AV's pose and the route give three things. On our trip,
with the AV 50.0 m along the route (chosen for this example):

1. **Where the AV is on the route:** the route waypoint nearest its pose, the
   same nearest-waypoint lookup as GP4's trigger 2 (:ref:`l7-lec-triggers`).
   Here, on the road from 1 to 3.
2. **Distance left:** 260.6 − 50.0 = 210.6 m.
3. **Next maneuver:** turn right at 3. The route enters intersection 3 at
   99.7 m, so it is 99.7 − 50.0 = 49.7 m ahead.

.. note::

   A navigation app shows the same three things: where you are, how far is
   left, and the next turn.


.. _l7-lec-grp:

CARLA's GlobalRoutePlanner Also Runs A* on get_topology()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A CARLA install has a route planner, ``GlobalRoutePlanner``, in
``PythonAPI/carla/agents/navigation`` (not in the pip package) (CARLA Team,
2026, ``global_route_planner.py``).

- It builds its graph from ``get_topology()``, as our graph does, and runs A*
  (``networkx``'s ``astar_path``).
- It returns each waypoint of the route with a ``RoadOption``:
  ``LANEFOLLOW``, ``LEFT``, ``RIGHT``, ``STRAIGHT``, ``CHANGELANELEFT``,
  ``CHANGELANERIGHT``, or ``VOID`` for none.

.. important::

   **GP4 Task 1** asks you to write A* yourself, in ``astar_waypoints``. You
   may use ``GlobalRoutePlanner`` only in your tests, to check your routes.
   Its costs differ from length: an edge costs the number of waypoints it
   samples along the road, one every ``sampling_resolution`` meters (set when
   you create the planner), so about its length divided by that spacing; a
   lane change costs 0. Compare it with your distance costs at the same 2 m
   spacing.


.. _l7-lec-handson-trip:

Hands-On: the Trip, from Graph to Route
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The hands-on script is in the course's Python repo, folder ``lecture7``
(`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture7>`__).
It has five parts: ``map`` (the map file), ``graph`` (the graph), ``costs``
(the three costs), ``search`` (the two searches) and ``replan`` (the new
route). The commands are on :doc:`the Code page <l7_code>`.

.. admonition:: What to look at
   :class: hint

   - **search:** the slider sets how many nodes each search has taken so far.
     Set it to 100: where are Dijkstra's first 100 nodes, and where are A*'s?
   - **map** needs CARLA's Python package (``pip install carla==0.9.16``).
     Click the map, and the window prints the line of ``Town01.xodr`` where
     that road starts. Open the file at that line.

You need no CARLA server. The script has no search code: it replays routes
and search orders saved in advance. You write the search in GP4.


.. _l7-lec-next:

Next Class
----------

.. admonition:: Today
   :class: important

   L6 found where the AV is; **L7 found which lanes take it to the goal.**
   Town01's map file became a directed graph of 3107 waypoints; in Town03,
   roads have several lanes, so the route must also pick the lane. Travel
   time picked a route 6.3 m longer but 3.3 s faster than distance. In the
   appendix, A* took 196 nodes from its open set where Dijkstra took 543. The
   route is planned again on GP4's two triggers and passed on as a turn at
   each intersection.

- **L8, Prediction and Behavior Modeling:** the other road users, and what
  they will do next.

**Before next class**

- Run the five hands-on parts on :doc:`the Code page <l7_code>`.
- On :doc:`l7_search_steps`, redo the A* steps with A*'s estimate at
  intersection 4, :math:`h(4)`, set to 120 m instead of 105 m, and see whether
  the route changes.


.. rubric:: Image credits

The vehicle icons in the figures on this page were created by Stone from the
`Noun Project <https://thenounproject.com>`_.

The map data in the figure of the streets around the Kim Engineering Building
is © OpenStreetMap contributors, under the Open Database License (ODbL).

The sources of the HD map images in the figure "What an HD map looks like" are [TBD].
