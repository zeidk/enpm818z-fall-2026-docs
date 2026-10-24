====================================================
References
====================================================

These are the sources the L7 slides cite, grouped by the lecture's sections,
in the order the slides first cite each source. A source cited in several
sections is listed once, where the slides first cite it. The sections Lane
Changes, Edge Costs, At Scale and Re-planning cite no new source. Fourteen
sources are cited only in the appendix (:doc:`l7_appendix`); they have their
own group at the end.

.. dropdown:: Introduction
   :class-container: sd-border-secondary
   :open:

   The definitions of the lecture's terms, the notation of its diagrams, and
   what other AV software calls route planning and how it searches.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: UML notation
         :link: https://www.omg.org/spec/UML/2.5.1/PDF
         :class-card: sd-border-secondary

         **Object Management Group (2017)**

         *OMG Unified Modeling Language (OMG UML), Version 2.5.1.* Document
         formal/17-12-05. Accessed 22 October 2026.

         The notation of the class diagram of the lecture's terms. Also cited
         in Map to Graph, for the activity diagram of the steps from a map
         file to a graph.

      .. grid-item-card:: Road, road network, carriageway, lane
         :link: https://ec.europa.eu/eurostat/web/products-manuals-and-guidelines/-/ks-gq-19-004
         :class-card: sd-border-secondary

         **Eurostat, International Transport Forum and United Nations
         Economic Commission for Europe (2019)**

         *Glossary for Transport Statistics*, 5th edition. Publications
         Office of the European Union. Entries B.I-01 Road, B.I-04 Road
         network, B.I-12 Carriageway and B.I-13 Lane. Accessed 17 October
         2026.

         The definitions of the four road terms. A road network is "All
         roads in a given area"; "Roads also cover streets, bridges,
         tunnels, supporting structures, junctions, crossings and
         interchanges".

      .. grid-item-card:: Route
         :link: https://github.com/autowarefoundation/autoware_core/blob/main/planning/autoware_mission_planner/README.md
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *Mission Planner* (``autoware_core/planning/autoware_mission_planner/README.md``).
         Accessed 17 October 2026.

         The definition of a route: "The route is made of a sequence of
         lanes on a static map".

      .. grid-item-card:: Configuration space
         :link: https://lavalle.pl/planning/
         :class-card: sd-border-secondary

         **LaValle, S. M. (2006)**

         *Planning Algorithms.* Cambridge University Press. Chapter 4, The
         Configuration Space. Online at https://lavalle.pl/planning/.

         "The state space for motion planning is a set of possible
         transformations that could be applied to the robot. This will be
         referred to as the configuration space".

      .. grid-item-card:: Configuration, route planning, path, trajectory
         :link: https://doi.org/10.1109/TIV.2016.2578706
         :class-card: sd-border-secondary

         **Paden, B., Čáp, M., Yong, S. Z., Yershov, D. and Frazzoli, E.
         (2016)**

         "A Survey of Motion Planning and Control Techniques for Self-Driving
         Urban Vehicles." *IEEE Transactions on Intelligent Vehicles*, 1(1),
         33 to 55. doi:10.1109/TIV.2016.2578706.

         A car's configuration, "the planar coordinate of a point on the car
         together with the car's heading". Route planning: the AV "must select
         a route through the road network from its current position to the
         requested destination", "the problem of finding a minimum-cost
         path". Also cited in the appendix on path and trajectory.

      .. grid-item-card:: Apollo's routing
         :link: https://github.com/ApolloAuto/apollo/blob/master/modules/routing/README.md
         :class-card: sd-border-secondary

         **Apollo Auto (2026)**

         *Routing* (``modules/routing/README.md``). Accessed 16 October 2026.

         Apollo's routing module "generates high level navigation
         information" from map data and a start and end location.

      .. grid-item-card:: Apollo's search
         :link: https://github.com/ApolloAuto/apollo/blob/master/modules/routing/core/navigator.cc
         :class-card: sd-border-secondary

         **Apollo Auto (2026)**

         *Routing navigator* (``modules/routing/core/navigator.cc``).
         Accessed 17 October 2026. Creates an ``AStarStrategy`` (line 159).

         Apollo's routing searches with A*.

      .. grid-item-card:: Autoware's mission planning
         :link: https://docs.autoware.org/main/design/autoware-architecture-v1/components/planning/
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *Planning component design (Autoware architecture v1, components).*
         Accessed 16 October 2026.

         Mission planning "calculates routes from the current location to the
         destination, utilizing map data". In the appendix on other stacks:
         this older design's route "doesn't explicitly indicate which
         specific lanes to take".

      .. grid-item-card:: Autoware's search
         :link: https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_routing/src/RoutingGraph.cpp
         :class-card: sd-border-secondary

         **FZI Forschungszentrum Informatik (2026)**

         *Lanelet2 routing graph* (``lanelet2_routing/src/RoutingGraph.cpp``).
         Accessed 17 October 2026. ``shortestPath`` runs a
         ``DijkstraStyleSearch`` (line 340); Autoware's route handler calls
         it.

         Autoware's search: Dijkstra, in the Lanelet2 map library.

      .. grid-item-card:: Waymo's routing
         :link: https://support.google.com/waymo/answer/9796072?hl=en
         :class-card: sd-border-secondary

         **Waymo (2026)**

         *Routing (Waymo Help).* Accessed 22 October 2026.

         Waymo's maps "help every Waymo car plan its route before your trip
         starts". Waymo describes routing only for its riders: its search is
         not published.


.. dropdown:: The Trip
   :class-container: sd-border-secondary
   :open:

   How the lecture reads CARLA's maps in Python. Also cited in Map to Graph.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: CARLA's Python API
         :link: https://carla.readthedocs.io/en/0.9.16/python_api/
         :class-card: sd-border-secondary

         **CARLA Team (2026)**

         *Python API reference (CARLA 0.9.16 documentation).* Accessed 14
         October 2026.

         ``carla.Map`` reads ``Town01.xodr`` with no CARLA server running,
         after ``pip install carla==0.9.16``. In Map to Graph:
         ``get_topology()`` returns each segment as two waypoints, "The first
         one is the origin and the second one represents another road end
         that can be reached".


.. dropdown:: Map to Graph
   :class-container: sd-border-secondary
   :open:

   What an HD map is, holds and is used for, where AV maps come from and when
   they change, and the OpenDRIVE file read from a map file to a graph.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: HD maps
         :link: https://doi.org/10.1109/OJITS.2023.3295502
         :class-card: sd-border-secondary

         **Elghazaly, G., Frank, R., Harvey, S. and Safko, S. (2023)**

         "High-Definition Maps: Comprehensive Survey, Challenges, and Future
         Perspectives." *IEEE Open Journal of Intelligent Transportation
         Systems*, 4, 527 to 550. doi:10.1109/OJITS.2023.3295502. Quoted from
         the accepted manuscript,
         https://orbilu.uni.lu/bitstream/10993/55774/1/OJ_ITS_2023.pdf.

         "Centimetre-level positional accuracy and the availability of
         lane-level geometric and semantic information are the essential
         features found in most HD maps". The "six distinct layers", the
         tasks a map helps with ("maps can offer an unlimited range"), and
         the problems of building and keeping HD maps.

      .. grid-item-card:: HERE HD Live Map
         :link: https://www.mathworks.com/help/driving/ug/here-hd-live-map-layers.html
         :class-card: sd-border-secondary

         **MathWorks (2026)**

         *HERE HD Live Map Layers.* Automated Driving Toolbox documentation,
         R2026b. Accessed 17 October 2026.

         HERE's three models: road centerline, HD lane and HD localization.
         Map layers cut into squares (tiles), from a cloud service, with
         "Continuously updated map data".

      .. grid-item-card:: Waymo's maps
         :link: https://waymo.com/blog/2020/09/the-waymo-driver-handbook-mapping/
         :class-card: sd-border-secondary

         **Waymo (2020)**

         *The Waymo Driver Handbook: How our highly-detailed maps help unlock
         new locations for autonomous driving.* Accessed 17 October 2026.

         "Our team starts by manually driving our sensor equipped vehicles
         down each street, so our custom lidar can paint a 3D picture". The
         car carries its map on board, compares sensor data "with its
         on-board map", reroutes when a road changed, and tells the fleet.

      .. grid-item-card:: Mobileye REM
         :link: https://www.mobileye.com/technology/rem/
         :class-card: sd-border-secondary

         **Mobileye (2026)**

         *REM: Road Experience Management.* Accessed 17 October 2026.

         Maps from cameras on customers' cars: "Millions of
         Mobileye-equipped ADAS vehicles sending data to the cloud in small
         data packets (10kb/km)".

      .. grid-item-card:: CARLA's maps and waypoints
         :link: https://carla.readthedocs.io/en/0.9.16/core_map/
         :class-card: sd-border-secondary

         **CARLA Team (2026)**

         *Maps and navigation (CARLA 0.9.16 documentation).* Accessed 14
         October 2026.

         The client builds a ``carla.Map`` from the server's ``.xodr``, and
         "To change the map, the world has to change too". A waypoint is "A
         3D-directed point in the CARLA world corresponding to an OpenDRIVE
         lane"; the waypoint graph's edges go "in the direction of the lane".
         Also cited in Lane Changes, for each waypoint's ``lane_change``
         field.

      .. grid-item-card:: Autoware's map loading
         :link: https://docs.autoware.org/main/design/autoware-architecture-v1/interfaces/components/map/
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *Map (Autoware architecture v1, interfaces).* Accessed 22 October
         2026.

         Autoware loads a Lanelet2 map and a point cloud map "before
         launching". Also cited in the appendix on map formats.

      .. grid-item-card:: Autoware's divided point cloud map
         :link: https://docs.autoware.org/main/tutorials/others/using-divided-map/
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *Using divided pointcloud map (Autoware tutorials).* Accessed 22
         October 2026.

         With a divided point cloud map, Autoware loads "the pointcloud map
         according to the vehicle's position".

      .. grid-item-card:: Town01's point cloud
         :link: https://bitbucket.org/carla-simulator/autoware-contents
         :class-card: sd-border-secondary

         **CARLA Team (2026)**

         *autoware-contents: point cloud maps* (``maps/point_cloud_maps``).
         Accessed 17 October 2026. Point cloud maps for Town01 to Town07 and
         Town10HD; ``Town01.pcd`` is 190 MB.

         Town01's base map is not in ``Town01.xodr``: CARLA ships it as a
         separate 190 MB point cloud.

      .. grid-item-card:: ASAM OpenDRIVE
         :link: https://www.asam.net/standards/detail/opendrive/
         :class-card: sd-border-secondary

         **ASAM e.V. (2026)**

         *ASAM OpenDRIVE.* Current version 1.9.0; ``Town01.xodr`` declares
         revision 1.4. Accessed 14 October 2026.

         OpenDRIVE is "a common base for describing road networks with
         extensible markup language (XML) syntax, using the file extension
         xodr". Also cited in the appendix on map formats.

      .. grid-item-card:: Maps from OpenStreetMap
         :link: https://carla.readthedocs.io/en/0.9.16/tuto_G_openstreetmap/
         :class-card: sd-border-secondary

         **CARLA Team (2026)**

         *Generate maps with OpenStreetMap (CARLA 0.9.16 documentation).*
         Accessed 17 October 2026.

         ``carla.Osm2Odr.convert()`` turns the text of an ``.osm`` file into
         OpenDRIVE text.

      .. grid-item-card:: The geometry element
         :link: https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/v1.9.0/specification/09_geometries/09_02_road_reference_line.html
         :class-card: sd-border-secondary

         **ASAM e.V. (2026)**

         *ASAM OpenDRIVE 1.9.0 Specification, Section 9.2: Road reference
         line.* Table 18, attributes of the geometry element. Accessed 22
         October 2026.

         The definitions of a ``<geometry>`` element's attributes, read on
         road 25: ``s``, "s-coordinate of start position"; ``x`` and ``y``,
         the start position; ``hdg``, "Start orientation (inertial
         heading)"; ``length``, "Length of the element's reference line".

      .. grid-item-card:: Junctions
         :link: https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/v1.9.0/specification/12_junctions/12_04_connecting_roads.html
         :class-card: sd-border-secondary

         **ASAM e.V. (2026)**

         *ASAM OpenDRIVE 1.9.0 Specification, Sections 12.2 and 12.4: Common
         junctions, Connecting roads.* Tables 56, 61 and 62: attributes of
         connection and laneLink. Accessed 22 October 2026.

         The definitions of a junction's connection, read on junction 332:
         ``incomingRoad``, "ID of the incoming road"; ``connectingRoad``, "ID
         of the connecting road"; ``contactPoint``; and the ``laneLink``
         attributes ``from`` and ``to``.


.. dropdown:: Search
   :class-container: sd-border-secondary
   :open:

   The two searches you know from the planning course. Their recap is in the
   appendix.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Dijkstra's algorithm
         :link: https://doi.org/10.1007/BF01386390
         :class-card: sd-border-secondary

         **Dijkstra, E. W. (1959)**

         "A note on two problems in connexion with graphs." *Numerische
         Mathematik*, 1(1), 269 to 271. doi:10.1007/BF01386390.

         Dijkstra's search, which takes the open node with the lowest cost
         so far.

      .. grid-item-card:: A*
         :link: https://doi.org/10.1109/TSSC.1968.300136
         :class-card: sd-border-secondary

         **Hart, P. E., Nilsson, N. J. and Raphael, B. (1968)**

         "A Formal Basis for the Heuristic Determination of Minimum Cost
         Paths." *IEEE Transactions on Systems Science and Cybernetics*,
         4(2), 100 to 107. doi:10.1109/TSSC.1968.300136.

         A*, which adds a heuristic, an estimate of the cost to the goal.
         GP4's planner searches with A*.


.. dropdown:: Maneuvers
   :class-container: sd-border-secondary
   :open:

   CARLA's own route planner.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: CARLA's GlobalRoutePlanner
         :link: https://github.com/carla-simulator/carla/tree/0.9.16/PythonAPI/carla/agents/navigation
         :class-card: sd-border-secondary

         **CARLA Team (2026)**

         *global_route_planner.py and local_planner.py (CARLA 0.9.16,
         PythonAPI/carla/agents/navigation).* Accessed 17 October 2026.

         ``GlobalRoutePlanner`` builds its graph from ``get_topology()``,
         runs A* (``networkx``'s ``astar_path``), and returns each waypoint
         of the route with a ``RoadOption``.


.. dropdown:: Going Further Only
   :class-container: sd-border-secondary
   :open:

   Sources cited only in the appendix, :doc:`l7_appendix`: route words in
   other stacks, the map in the AV's architecture, map formats and Lanelet2,
   curves in OpenDRIVE, and routing a whole country.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Nav2
         :link: https://docs.nav2.org/rolling/index.html
         :class-card: sd-border-secondary

         **Nav2 project (2026)**

         *Nav2 documentation.* Accessed 16 October 2026.

         ROS 2's Nav2 "provides perception, planning, control, localization,
         visualization, behaviors, and much more": in robotics,
         "navigation" is the whole stack, not one module.

      .. grid-item-card:: A functional architecture
         :link: https://arxiv.org/abs/1703.08557
         :class-card: sd-border-secondary

         **Ulbrich, S., Reschka, A., Rieken, J., Ernst, S., Bagschik, G.,
         Dierkes, F., Nolte, M. and Maurer, M. (2017)**

         *Towards a Functional System Architecture for Automated Vehicles.*
         arXiv:1703.08557.

         The map as the fixed part of the AV's picture of the scene: "Dynamic
         elements and the scenery are associated with each other to obtain an
         environment model." With the AV's own state added, it is the scene
         model.

      .. grid-item-card:: Situation awareness
         :link: https://doi.org/10.1518/001872095779049543
         :class-card: sd-border-secondary

         **Endsley, M. R. (1995)**

         "Toward a Theory of Situation Awareness in Dynamic Systems." *Human
         Factors*, 37(1), 32 to 64. doi:10.1518/001872095779049543.

         Three levels of situation awareness: perceive the elements,
         understand what they mean, and predict what they will do.

      .. grid-item-card:: Autoware's map
         :link: https://docs.autoware.org/main/design/autoware-architecture-v1/components/map/
         :class-card: sd-border-secondary

         **Autoware Foundation (2026)**

         *Map (Autoware architecture v1, components).* Accessed 14 October
         2026.

         The lane map is "required for ... predicting the trajectories of
         other vehicles and pedestrians"; the map "must be in Lanelet2
         format, with additional modifications required by Autoware"; a point
         cloud map is "a single PCD file or divided into multiple PCD files".

      .. grid-item-card:: Waymo's World Decoder
         :link: https://blog.waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving
         :class-card: sd-border-secondary

         **Waymo (2025)**

         *Demonstrably Safe AI For Autonomous Driving.* 9 December 2025.
         Accessed 22 October 2026.

         A "World Decoder" that uses its encoders' inputs "to predict other
         road users behaviors, produce high-definition maps, generate
         trajectories for the vehicle, and signals for trajectory
         validation".

      .. grid-item-card:: Tesla, as reported
         :link: https://www.humanoidsdaily.com/feed/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus
         :class-card: sd-border-secondary

         **Humanoids Daily (2025)**

         *Tesla AI Chief Details Unified World Simulator for FSD and
         Optimus.* 24 October 2025. Accessed 22 October 2026.

         As reported from a 2025 talk: one end-to-end neural network that
         learns from video, maps and kinematic data, and a "neural world
         simulator" that generates new video for training and testing. The
         slides cite no architecture published by Tesla itself.

      .. grid-item-card:: A Lanelet2 map file
         :link: https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_maps/res/mapping_example.osm
         :class-card: sd-border-secondary

         **FZI Forschungszentrum Informatik (2026)**

         *Lanelet2 example map* (``lanelet2_maps/res/mapping_example.osm``).
         Accessed 22 October 2026.

         A Lanelet2 map stored as XML text in an ``.osm`` file.

      .. grid-item-card:: Apollo's HD map files
         :link: https://github.com/ApolloAuto/apollo
         :class-card: sd-border-secondary

         **Baidu Apollo (2026)**

         *Apollo source: config_gflags.cc (base_map_filename) and
         hdmap_impl.cc (LoadMapFromFile).* Accessed 22 October 2026.

         Apollo's HD map is stored as protobuf; Apollo looks for the binary
         ``base_map.bin`` before ``.xml`` or ``.txt``.

      .. grid-item-card:: NDS.Live
         :link: https://nds-association.org/
         :class-card: sd-border-secondary

         **NDS Association (2026)**

         *What is NDS? NDS.Live.* Accessed 22 October 2026.

         Map data in "tiles, but also along driving paths", updated "over a
         data connection", sending "only what needs updating".

      .. grid-item-card:: Lanelets
         :link: https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_core/doc/LaneletPrimitives.md
         :class-card: sd-border-secondary

         **FZI Forschungszentrum Informatik (2026)**

         *Lanelet2: Lanelet primitives (documentation).* Accessed 14 October
         2026.

         "A Lanelet represents one atomic section of a lane"; it "consists of
         exactly one left and exactly one right Linestring"; "Regulatory
         elements are a generic way to express traffic rules".

      .. grid-item-card:: Lanelet2
         :link: https://doi.org/10.1109/ITSC.2018.8569929
         :class-card: sd-border-secondary

         **Poggenhans, F., Pauls, J.-H., Janosovits, J., Orf, S., Naumann,
         M., Kuhnt, F. and Mayr, M. (2018)**

         "Lanelet2: A High-Definition Map Framework for the Future of
         Automated Driving." *2018 21st International Conference on
         Intelligent Transportation Systems (ITSC)*, 1672 to 1679.
         doi:10.1109/ITSC.2018.8569929.

         Lanelet2 builds a map from lanelets: each lane by its two borders,
         instead of an offset from a road's reference line.

      .. grid-item-card:: Arcs and spirals
         :link: https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/v1.9.0/specification/09_geometries/09_05_arc.html
         :class-card: sd-border-secondary

         **ASAM e.V. (2026)**

         *ASAM OpenDRIVE 1.9.0 Specification, Section 9: Geometries.*
         Sections 9.4 Spiral and 9.5 Arc. Accessed 22 October 2026.

         A negative curvature is a "right curve (clockwise motion)". A
         spiral's curvature changes "linear from the start to the end", so a
         line can lead into an arc "without causing leaps in the curvature".

      .. grid-item-card:: Contraction hierarchies
         :link: https://doi.org/10.1007/978-3-540-68552-4_24
         :class-card: sd-border-secondary

         **Geisberger, R., Sanders, P., Schultes, D. and Delling, D. (2008)**

         "Contraction Hierarchies: Faster and Simpler Hierarchical Routing in
         Road Networks." *Experimental Algorithms*, Lecture Notes in Computer
         Science. Springer, 319 to 333. doi:10.1007/978-3-540-68552-4_24.

         The nodes are ranked, and shortcut edges skip the lower-ranked ones.
         A request then searches from both ends, toward higher-ranked nodes
         only.

      .. grid-item-card:: OSRM
         :link: https://github.com/Project-OSRM/osrm-backend/blob/master/README.md
         :class-card: sd-border-secondary

         **Project OSRM (2026)**

         *osrm-backend README.* Accessed 17 October 2026.

         A "high performance routing engine written in C++ designed to run on
         OpenStreetMap data", with contraction hierarchies and Multi-Level
         Dijkstra; its README recommends the latter for most uses.


.. rubric:: Map data

Town01's map is CARLA's ``Town01.xodr`` (CARLA 0.9.16), read offline with the
CARLA Python API. The campus map of the Kim Engineering Building's streets
uses map data © OpenStreetMap contributors (ODbL). The GP4 quotes are from the
course's GP4 page.
