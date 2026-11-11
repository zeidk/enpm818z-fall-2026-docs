====================================================
Code
====================================================

The L9 hands-on is the folder ``lecture9/`` of
`enpm818z-fall-2026-carla-python
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture9>`_.
It uses the lecture's two scenes: **one road from CARLA's Town03 map**, with
the obstacle, a parked car, in the AV's lane, and **one parking garage**.

You need Python with ``numpy`` and ``matplotlib``. You need **no CARLA
server, no ROS and no GPU**. The road was read once from CARLA's Town03 map
by ``export_scene.py``.

The lecture also shows the same planner running in CARLA, a ROS 2 package;
see `The Demo in CARLA`_ below.

.. list-table::
   :widths: 14 50 36
   :header-rows: 1
   :class: compact-table

   * - **Part**
     - **What it shows**
     - **Lecture section**
   * - ``scene``
     - the road in the map and in the Frenet frame, with a point P you move
       with the :math:`s` and :math:`d` sliders
     - "Hands-On, Part 1: the Road in Two Frames" (The Frenet Frame)
   * - ``sample``
     - every candidate path from the AV at :math:`s` = 60 m, checked and
       scored, and a table of the cheapest
     - "Hands-On, Part 2: Sample, Score, Drive" (Sampling Paths)
   * - ``drive``
     - planning again every 0.5 s while the AV passes the obstacle
     - "Hands-On, Part 2: Sample, Score, Drive" (Sampling Paths)
   * - ``rrt``
     - an RRT growing in the garage, toward the free spot you pick
     - "Hands-On, Part 3: the Garage" (Garage Planners)
   * - ``search``
     - the grid search and hybrid A* results, computed in advance
     - "Hands-On, Part 3: the Garage" (Garage Planners)


Run It
------

Get the repository, then go to the folder:

.. code-block:: bash

   git clone https://github.com/rubixcubic/enpm818z-fall-2026-carla-python.git
   cd enpm818z-fall-2026-carla-python/lecture9

Each part opens a matplotlib window. The commands of the lecture's three
hands-on slides:

.. code-block:: bash

   # Part 1: the road in two frames
   python3 l9_handson.py --part scene    # map and Frenet views

   # Part 2: sample, score, drive
   python3 l9_handson.py --part sample   # candidates, costs
   python3 l9_handson.py --part drive    # re-plan every 0.5 s

   # Part 3: the garage
   python3 l9_handson.py --part rrt                       # the tree grows
   python3 l9_handson.py --part rrt --seed 7              # another seed
   python3 l9_handson.py --part rrt --goal-spot bottom2   # a free spot near the AV
   python3 l9_handson.py --part search                    # results only

To save a still instead of opening a window:

.. code-block:: bash

   python3 l9_handson.py --part sample --snapshot sample.png

The in-class spreadsheet exercise uses ``candidates.csv`` from the same
folder. Open it in Excel, Google Sheets or LibreOffice Calc. If you need the
file again:

.. code-block:: bash

   python3 export_candidates.py   # writes candidates.csv from l9common.py


What Each Part Shows
~~~~~~~~~~~~~~~~~~~~

1. **scene:** the stretch of Town03's road 67, from the map, and the same
   road in the Frenet frame: :math:`s` is the distance along the reference
   path (the right lane's center) and :math:`d` the distance across it,
   positive to the left. Move P with the sliders. The title converts P to
   the map and back.
2. **sample:** the 31 candidates of the lecture: 10 end offsets times 3
   maneuver lengths, plus stop behind. Each one is checked with three
   circles around the AV and three around the obstacle, and scored with
   the four cost terms. Green is the cheapest, gray kept, rust collides,
   purple dashed too sharp, black dotted stop behind. The sliders change
   four weights (comfort, clearance, lane and progress; the center weight
   stays at 2) and where the obstacle is parked (:math:`s` from 80 to
   140 m). The table on the right ranks the nine cheapest candidates, with
   each cost term. A dropped candidate has a total of ``inf``, so it ranks
   last.
3. **drive:** the planner runs every 0.5 s. The AV drives the first 0.5 s of
   the cheapest path, then plans again from where it is. The slider steps
   through the plans.
4. **rrt:** a rapidly exploring random tree from the AV's start in the garage
   to the point in front of a free spot. Each new node is a 1.5 m step from
   the nearest node toward a random point, checked with the AV's three
   circles. The slider shows the tree as it grows. ``--goal-spot`` picks the
   free spot: ``top7``, the lecture's goal (the default), or ``bottom2`` and
   ``bottom3``, the two free spots near the AV.
5. **search:** results only, read from ``l9_results/garage_search.json``:
   the small grid's step numbers, the grid search path through the garage,
   and hybrid A*'s path, forward solid and reverse dashed, with every pose
   it expanded, always for the lecture's goal, ``top7``. The folder has no
   search code: GP4 asks you to write A* on the lane graph, not these garage
   searches.


Options
~~~~~~~

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Option**
     - **What it does**
   * - ``--part scene|sample|drive|rrt|search``
     - Which part to run. Required.
   * - ``--seed S``
     - The RRT's random seed (``rrt`` only). Default 4, as in the lecture.
   * - ``--goal-spot top7|bottom2|bottom3``
     - The free spot the RRT drives to (``rrt`` only). Default ``top7``, as
       in the lecture.
   * - ``--snapshot out.png``
     - Save a still to ``out.png`` instead of opening a window.
   * - ``--html out.html``
     - Save a page instead of opening a window. Needs ``mpld3``
       (``pip install mpld3``).


The Files
---------

.. list-table::
   :widths: 34 66
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **What it is**
   * - ``l9_handson.py``
     - the five parts above
   * - ``candidates.csv``
     - the candidate paths for the spreadsheet exercise
   * - ``export_candidates.py``
     - writes ``candidates.csv`` from ``l9common.py``
   * - ``l9common.py``
     - the road, the Frenet frame, the S curve, the circles, the costs and
       the RRT
   * - ``export_scene.py``
     - reads ``Town03.xodr`` with ``carla.Map`` (offline) and writes
       ``l9_scene.npz``
   * - ``l9_scene.npz``
     - the right and left lane centers every 0.5 m, and the town's lanes for
       the overview
   * - ``l9_results/garage_search.json``
     - the grid search and hybrid A* results (data only)
   * - ``tests/``
     - the tests: ``python3 -m pytest -q tests``

**Frames.** The map frame is in meters, :math:`x` as CARLA's :math:`x` and
:math:`y` as minus CARLA's :math:`y`, so the frame is right-handed. Headings
are counterclockwise from :math:`+x`.


Chosen Values
-------------

The road is measured from the map. Everything else is chosen for the
lecture and set at the top of ``l9common.py``:

.. list-table::
   :widths: 24 76
   :header-rows: 1
   :class: compact-table

   * - **Value**
     - **Chosen**
   * - the AV
     - 4.5 m by 1.9 m, base link 0.9 m in from the rear bumper; wheelbase
       2.875 m (chosen for the lecture) and steering limit 0.7 rad (GP4's)
   * - the AV's start
     - :math:`s` = 60 m on the right lane's center, 10 m/s
   * - the obstacle
     - 4.5 m by 1.9 m, centered at :math:`s` = 118 m, :math:`d` = −0.3 m
   * - horizon
     - 70 m
   * - weights
     - comfort 2 per m/s², clearance 4 per m, lane 2 per lane and 2 per m
       off center, progress 0.5 per m
   * - limits
     - a gap under 0.3 m is a collision; more than 3 m/s² sideways is too
       sharp
   * - garage
     - 36 m by 18 m, one 7 m aisle, spots 2.6 m by 5.5 m


The Demo in CARLA
-----------------

The ROS 2 package ``l9_planning_demo``, in the course's ROS repository
(`README
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l9_planning_demo/README.md>`_),
runs the same planner on the same stretch of Town03, with the obstacle at
:math:`s` = 118 m. This is the lecture's slide "Demo: the Same Planner in
CARLA". Start CARLA first, then build the package and launch it:

.. code-block:: bash

   carla_start                       # CARLA 0.9.16 server
   cd ~/enpm818z_ws
   colcon build --packages-select l9_planning_demo
   source install/setup.bash
   ros2 launch l9_planning_demo demo.launch.py
   # or, with three parked cars:
   ros2 launch l9_planning_demo demo_obstacles.launch.py

In a second terminal, change a weight while it runs:

.. code-block:: bash

   ros2 param set /planning_demo w_clearance 10.0

- RViz draws every candidate in the colors of the lecture, and the AV's
  circles; its Camera panel shows CARLA's view from behind the AV.
- Every 0.5 s the AV moves along the first 0.5 s of the cheapest path, then
  plans again. The demo places the AV on the path; it does not steer or
  brake. The next class adds the controller that drives it.
- A changed weight takes effect at the next plan: the path changes while you
  watch.

``demo.launch.py`` parks one car at :math:`s` = 118 m, :math:`d` = −0.3 m, as
in the lecture. ``demo_obstacles.launch.py`` parks three: at :math:`s` = 78 m
in the left lane, 118 m in the right lane (the lecture's car) and 165 m in the
right lane. Both launch files take ``host:=``, ``port:=`` (default 2000) and
``rviz:=`` (default ``true``). The node ticks the server in synchronous mode,
so run no other client that ticks at the same time. The README lists every
parameter and what to do if something goes wrong.
