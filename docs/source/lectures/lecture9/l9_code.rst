====================================================
Code
====================================================

The L9 hands-on is the folder ``lecture9/`` of
`enpm818z-fall-2026-carla-python
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture9>`_.
It uses the lecture's two scenes: **one road from CARLA's Town03 map**, with
a car parked in the AV's lane, and **one parking garage**.

You need Python with ``numpy`` and ``matplotlib``. You need **no CARLA
server, no ROS and no GPU**.

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
     - planning again every 0.5 s while the AV passes the parked car
     - "Hands-On, Part 2: Sample, Score, Drive" (Sampling Paths)
   * - ``rrt``
     - an RRT growing in the garage
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

Each part opens a matplotlib window:

.. code-block:: bash

   python3 l9_handson.py --part scene    # 1. the road in the map and in the Frenet frame
   python3 l9_handson.py --part sample   # 2. candidate paths, their costs, the cheapest
   python3 l9_handson.py --part drive    # 3. re-planning every 0.5 s while passing the car
   python3 l9_handson.py --part rrt      # 4. an RRT growing in the garage
   python3 l9_handson.py --part search   # 5. grid search and hybrid A* results (read only)

   # another random seed for the RRT
   python3 l9_handson.py --part rrt --seed 7

   # save a still instead of opening a window
   python3 l9_handson.py --part sample --snapshot sample.png

The two in-class exercises use the same folder:

.. code-block:: bash

   # Exercise: score every candidate in a spreadsheet.
   # Open candidates.csv in Excel, Google Sheets or LibreOffice Calc.
   python3 export_candidates.py                 # writes candidates.csv again, if you need it

   # Exercise: a fifth cost term. Write edge_cost in l9_exercise.py, then:
   python3 l9_check.py                          # PASS or FAIL for five paths
   python3 l9_handson.py --part sample --extra  # the table gets an "extra" column


What Each Part Shows
~~~~~~~~~~~~~~~~~~~~

1. **scene:** the stretch of Town03's road 67, from the map, and the same
   road in the Frenet frame: :math:`s` is the distance along the reference
   path (the right lane's center) and :math:`d` the distance across it,
   positive to the left. Move P with the sliders. The title converts P to
   the map and back.
2. **sample:** the 31 candidates of the lecture: 10 end offsets times 3
   maneuver lengths, plus stop behind. Each one is checked with three
   circles around the AV and three around the parked car, and scored with
   the four cost terms. Green is the cheapest, gray kept, rust collides,
   purple dashed too sharp, black dotted stop behind. The sliders change the
   four weights and where the car is parked (:math:`s` from 80 to 140 m).
   The table on the right ranks the nine cheapest candidates, with each
   cost term. A dropped candidate has a total of ``inf``, so it ranks last.
3. **drive:** the planner runs every 0.5 s. The AV drives the first 0.5 s of
   the cheapest path, then plans again from where it is. The slider steps
   through the plans.
4. **rrt:** a rapidly exploring random tree from the AV's start in the garage
   to the point in front of the free spot. Each new node is a 1.5 m step from
   the nearest node toward a random point, checked with the AV's three
   circles. The slider shows the tree as it grows.
5. **search:** results only, read from ``l9_results/garage_search.json``:
   the small grid's step numbers, the grid search path through the garage,
   and hybrid A*'s path, forward solid and reverse dashed, with every pose
   it expanded. The folder has no search code: GP4 asks you to write A* on
   the lane graph yourself.


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
   * - ``l9_exercise.py``
     - the code exercise: you write ``edge_cost``
   * - ``l9_check.py``
     - checks your ``edge_cost``
   * - ``l9common.py``
     - the road, the Frenet frame, the S curve, the circles, the costs (with
       a hook for a fifth term) and the RRT
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
   * - the parked car
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
