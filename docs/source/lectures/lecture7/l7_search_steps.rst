.. _l7-search-steps:

=============================
Dijkstra and A*, Step by Step
=============================

This page is reading material. The lecture recaps both searches in four
slides and keeps their results. Here you work every step on the intersection graph cut
from the trip's Town01 streets.


.. _l7-steps-toy:

The Intersection Graph
----------------------

Seven Intersections from Our Trip's Streets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_on_map.png
   :alt: A top view with axes x, east, in meters and y, north, in meters. Town01's lanes in light gray, with the intersection graph drawn over them: nine white circles labeled S, 1 to 7 and G, joined by straight black lines. S sits on a street east of node 1. Node 1 has node 2 below it and node 3 above it; node 3 joins node 4 above and node 5 to the right; nodes 4 and 5 both join node 6, which joins G to its right; node 5 also joins node 7 far to the east.
   :width: 85%
   :align: center

   The intersection graph drawn over Town01's lanes (light gray). The axes are
   :math:`x` east and :math:`y` north, in meters.

- **Nodes:** S (the AV's start), G (the goal), and seven intersections, 1 to
  7, at their centers.
- **Edges:** the roads between them. Each length is measured along the lane,
  center to center, and rounded to whole meters.
- Two lanes per road: each edge goes both ways, with one length (the two
  lanes differ by at most 1.66 m). S and G sit in one lane, so they have one
  edge each.


The Intersection Graph We Search by Hand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_base.png
   :alt: The intersection graph alone, to scale, nodes as white circles. Edge lengths in meters beside each edge: S to 1, 41, with an arrow from S to 1; 1 to 2, 67; 1 to 3, 75; 3 to 4, 55; 3 to 5, 64; 4 to 6, 66; 5 to 6, 53; 5 to 7, 179; 6 to G, 40, with an arrow from 6 to G.
   :width: 75%
   :align: center

   The intersection graph, to scale. The number beside each edge is its length in
   meters.

- Edge costs: lengths in meters.
- S has an arrow: the AV faces west, toward 1. G has one: it is reached from
  6.
- The intersection graph keeps three choices: south at 1 (toward 2),
  straight on at 3 (toward 4), and east at 5 (toward 7).

The intersection graph counts each road to an intersection's center; the waypoint graph
follows the lane through the turn. So their totals differ a little, as you
will see.


.. _l7-steps-dijkstra:

Dijkstra
--------

Dijkstra's search grows the set of nodes whose cheapest cost from S is known,
one node at a time, always the closest one next. Here it runs by hand on the
intersection graph, with distance as the cost.


Three Words for a Search: g, Open, Done
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: cost so far, :math:`g(n)`
   :class: note

   The cost of the cheapest route from the start to node :math:`n` found so
   far, in the units of the edge costs (here, meters).

- **Open set:** the nodes reached but not yet taken, each with its
  :math:`g` and the node it was reached **from**.
- **Take** a node: remove the one with the lowest :math:`g` from the open
  set. Its :math:`g` is now final: it is **done**.
- **Check** a road from the taken node :math:`u` to a node :math:`v` that is
  not done: the cost through :math:`u` is :math:`g(u)` plus the edge's cost.
  If it is lower than what the open set holds for :math:`v` (or :math:`v` is
  new), store it, with "from :math:`u`".


Dijkstra in Five Lines
~~~~~~~~~~~~~~~~~~~~~~

#. Put the start in the open set with :math:`g = 0`.
#. Take the open node :math:`u` with the lowest :math:`g`. If the open set is
   empty, there is no route: stop.
#. If :math:`u` is the goal: stop, and read the route back through "from".
#. For each edge from :math:`u` to a node :math:`v` that is not done: if
   :math:`g(u) + \text{cost}` is lower than :math:`v`'s :math:`g`, set
   :math:`v`'s :math:`g` to it and its "from" to :math:`u`.
#. Go to line 2.

Ties: when two open nodes have the same :math:`g`, take either; the route's
cost is the same. In GP4 the open set is a priority queue; choosing and
writing it is part of Task 1.

In every step figure below, amber marks the node taken in that step, a black
ring marks an open node, and gray marks a done node.


Dijkstra, Step 1: Start at S
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_dij_1.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node S is amber: taken from the open set in this step. Black rings, open: 1. Thick amber edges from S to 1.
   :width: 70%
   :align: center

   Amber: taken now (S). Ring: open (1). Thick amber edge: S to 1.

#. Put S in the open set with :math:`g = 0`. Take it.
#. Check its roads:

   - 1: :math:`0 + 41 = 41`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g` (m)
     - **from**
   * - 1
     - 41
     - S

Done: S.


Dijkstra, Step 2: Take Node 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_dij_2.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 1 is amber: taken from the open set in this step. Gray, done: S. Black rings, open: 2 and 3. Thick amber edges from 1 to 2 and 3.
   :width: 70%
   :align: center

   Amber: taken now (1). Ring: open (2 and 3). Gray: done (S). Thick amber
   edges: 1 to 2 and 1 to 3.

#. Take 1: :math:`g = 41`. Its :math:`g` is final.
#. Check its roads:

   - 2: :math:`41 + 67 = 108`
   - 3: :math:`41 + 75 = 116`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g` (m)
     - **from**
   * - 2
     - 108
     - 1
   * - 3
     - 116
     - 1

Done: S, 1.


Dijkstra, Step 3: Take Node 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_dij_3.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 2 is amber: taken from the open set in this step. Gray, done: S and 1. Black rings, open: 3.
   :width: 70%
   :align: center

   Amber: taken now (2). Ring: open (3). Gray: done (S and 1). No edge is
   thick: 2 has no road to a node that is not done.

#. Take 2: :math:`g = 108` (the lowest; next is 116). Its :math:`g` is
   final.
#. Check its roads: none leads to a node that is not done.

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g` (m)
     - **from**
   * - 3
     - 116
     - 1

Done: S, 1, 2.


Dijkstra, Step 4: Take Node 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_dij_4.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 3 is amber: taken from the open set in this step. Gray, done: S, 1 and 2. Black rings, open: 4 and 5. Thick amber edges from 3 to 4 and 5.
   :width: 70%
   :align: center

   Amber: taken now (3). Ring: open (4 and 5). Gray: done (S, 1 and 2).
   Thick amber edges: 3 to 4 and 3 to 5.

#. Take 3: :math:`g = 116`. Its :math:`g` is final.
#. Check its roads:

   - 4: :math:`116 + 55 = 171`
   - 5: :math:`116 + 64 = 180`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g` (m)
     - **from**
   * - 4
     - 171
     - 3
   * - 5
     - 180
     - 3

Done: S, 1, 2, 3.


Dijkstra, Step 5: Take Node 4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_dij_5.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 4 is amber: taken from the open set in this step. Gray, done: S, 1, 2 and 3. Black rings, open: 5 and 6. Thick amber edge from 4 to 6.
   :width: 70%
   :align: center

   Amber: taken now (4). Ring: open (5 and 6). Gray: done (S, 1, 2 and 3).
   Thick amber edge: 4 to 6.

#. Take 4: :math:`g = 171` (the lowest; next is 180). Its :math:`g` is
   final.
#. Check its roads:

   - 6: :math:`171 + 66 = 237`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g` (m)
     - **from**
   * - 5
     - 180
     - 3
   * - 6
     - 237
     - 4

Done: S, 1, 2, 3, 4.


Dijkstra, Step 6: Take Node 5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_dij_6.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 5 is amber: taken from the open set in this step. Gray, done: S, 1, 2, 3 and 4. Black rings, open: 6 and 7. Thick amber edges from 5 to 6 and 7.
   :width: 70%
   :align: center

   Amber: taken now (5). Ring: open (6 and 7). Gray: done (S, 1, 2, 3 and
   4). Thick amber edges: 5 to 6 and 5 to 7.

#. Take 5: :math:`g = 180` (the lowest; next is 237). Its :math:`g` is
   final.
#. Check its roads:

   - 6: :math:`180 + 53 = 233`, less than 237: replace, from 5
   - 7: :math:`180 + 179 = 359`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g` (m)
     - **from**
   * - 6
     - 233
     - 5
   * - 7
     - 359
     - 5

Done: S, 1, 2, 3, 4, 5.


Dijkstra, Step 7: Take Node 6
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_dij_7.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 6 is amber: taken from the open set in this step. Gray, done: S, 1, 2, 3, 4 and 5. Black rings, open: G and 7. Thick amber edge from 6 to G.
   :width: 70%
   :align: center

   Amber: taken now (6). Ring: open (G and 7). Gray: done (S, 1, 2, 3, 4
   and 5). Thick amber edge: 6 to G.

#. Take 6: :math:`g = 233` (the lowest; next is 359). Its :math:`g` is
   final.
#. Check its roads:

   - G: :math:`233 + 40 = 273`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g` (m)
     - **from**
   * - G
     - 273
     - 6
   * - 7
     - 359
     - 5

Done: S, 1, 2, 3, 4, 5, 6.


Dijkstra, Step 8: Take G, the Route Is Final
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_dij_8.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node G is amber: taken from the open set. The route S, 1, 3, 5, 6, G is drawn as thick blue edges. Gray, done: S, 1, 2, 3, 4, 5 and 6. Black rings, still open: 7.
   :width: 70%
   :align: center

   Amber: taken now (G). Ring: still open (7). Gray: done (S, 1, 2, 3, 4, 5
   and 6). Thick blue edges: the route S, 1, 3, 5, 6, G.

#. Take G: :math:`g = 273` (the lowest; next is 359). Its :math:`g` is
   final.
#. G is the goal: stop. Read the route back through "from": G, 6, 5, 3, 1,
   S.
#. Route S, 1, 3, 5, 6, G: :math:`41 + 75 + 64 + 53 + 40 = 273` m.

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g` (m)
     - **from**
   * - 7
     - 359
     - 5

Done: S, 1, 2, 3, 4, 5, 6, G.


What Dijkstra Did on the Intersection Graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Result**
     - **On the intersection graph**
   * - route
     - S, 1, 3, 5, 6, G: 273 m
   * - nodes taken
     - 8 of 9: S, 1, 2, 3, 4, 5, 6, G
   * - taken but not on the route
     - 2 (south, away from G) and 4
   * - never taken
     - 7 (:math:`g = 359`, more than G's 273)

- Dijkstra takes nodes in order of :math:`g` alone. Node 2 lies away from G,
  but its :math:`g` (108) was the lowest, so it went first.
- On the waypoint graph, the same route: through intersections 1, 3, 5 and
  6, 260.6 m. The intersection graph's 273 m counts each turn to the intersection's center;
  the AV cuts the corner.


Check: Dijkstra
~~~~~~~~~~~~~~~

**Question.** Suppose the road from 5 to 6 were 60 m instead of 53 m. Which
route would Dijkstra return, and at what cost?

.. dropdown:: Answer
   :class-container: sd-border-success

   **S, 1, 3, 4, 6, G, at 277 m.** Through 4, node 6 costs
   :math:`171 + 66 = 237`; through 5 it would cost :math:`180 + 60 = 240`,
   which is not lower, so 6 keeps "from 4". Then G costs
   :math:`237 + 40 = 277`.


.. _l7-steps-astar:

A*
--

Dijkstra took node 2, which lies away from G, because it looked only at the
cost so far. A* also asks how far each node still is from the goal.


A* Takes the Node with the Lowest f = g + h
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: heuristic, :math:`h(n)`
   :class: note

   An estimate of the cost from node :math:`n` to the goal, in the same units
   as the edge costs, computed without searching.

- :math:`g(n)`: the cost from the start to :math:`n`, as in Dijkstra.
- :math:`f(n) = g(n) + h(n)`: an estimate of the whole route's cost through
  :math:`n`.
- A* is Dijkstra's five lines with one change: line 2 takes the open node
  with the lowest :math:`f`, not the lowest :math:`g`.
- With :math:`h = 0` everywhere, A* is Dijkstra.


Our Heuristic: the Straight Line to G
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_h.png
   :alt: The intersection graph with its edge lengths, all nodes white. A dashed black straight line runs from node 3 to G, crossing the block between them and the edge from 5 to 6, labeled 117 m beside the line.
   :width: 70%
   :align: center

   The dashed line is the straight line from node 3 to G: 117 m.

:math:`h(n)`: the straight-line distance from :math:`n` to G, measured on the
map, in meters, rounded.

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Node**
     - :math:`h` (m)
     - **Node**
     - :math:`h` (m)
   * - S
     - 142
     - 4
     - 105
   * - 1
     - 165
     - 5
     - 66
   * - 2
     - 221
     - 6
     - 40
   * - 3
     - 117
     - 7
     - 149
   * -
     -
     - G
     - 0

Node 2 is the farthest from G (221 m), node 6 the closest (40 m).


A*, Step 1: Start at S
~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_ast_1.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node S is amber: taken from the open set in this step. Black rings, open: 1. Thick amber edge from S to 1.
   :width: 70%
   :align: center

   Amber: taken now (S). Ring: open (1). Thick amber edge: S to 1.

#. Put S in the open set with :math:`g = 0`, :math:`f = 0 + 142 = 142`. Take
   it.
#. Check its roads:

   - 1: :math:`g = 0 + 41 = 41`, :math:`f = 41 + 165 = 206`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g`
     - :math:`h`
     - :math:`f`
     - **from**
   * - 1
     - 41
     - 165
     - 206
     - S

Done: S.


A*, Step 2: Take Node 1
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_ast_2.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 1 is amber: taken from the open set in this step. Gray, done: S. Black rings, open: 3 and 2. Thick amber edges from 1 to 2 and 3.
   :width: 70%
   :align: center

   Amber: taken now (1). Ring: open (3 and 2). Gray: done (S). Thick amber
   edges: 1 to 2 and 1 to 3.

#. Take 1: :math:`f = 206`. Its :math:`g` is final.
#. Check its roads:

   - 2: :math:`g = 41 + 67 = 108`, :math:`f = 108 + 221 = 329`
   - 3: :math:`g = 41 + 75 = 116`, :math:`f = 116 + 117 = 233`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g`
     - :math:`h`
     - :math:`f`
     - **from**
   * - 3
     - 116
     - 117
     - 233
     - 1
   * - 2
     - 108
     - 221
     - 329
     - 1

Done: S, 1.


A*, Step 3: Take Node 3
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_ast_3.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 3 is amber: taken from the open set in this step. Gray, done: S and 1. Black rings, open: 5, 4 and 2. Thick amber edges from 3 to 4 and 5.
   :width: 70%
   :align: center

   Amber: taken now (3). Ring: open (5, 4 and 2). Gray: done (S and 1).
   Thick amber edges: 3 to 4 and 3 to 5.

#. Take 3: :math:`f = 233` (the lowest; next is 329). Its :math:`g` is
   final.
#. Check its roads:

   - 4: :math:`g = 116 + 55 = 171`, :math:`f = 171 + 105 = 276`
   - 5: :math:`g = 116 + 64 = 180`, :math:`f = 180 + 66 = 246`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g`
     - :math:`h`
     - :math:`f`
     - **from**
   * - 5
     - 180
     - 66
     - 246
     - 3
   * - 4
     - 171
     - 105
     - 276
     - 3
   * - 2
     - 108
     - 221
     - 329
     - 1

Done: S, 1, 3.


A*, Step 4: Take Node 5
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_ast_4.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 5 is amber: taken from the open set in this step. Gray, done: S, 1 and 3. Black rings, open: 6, 4, 2 and 7. Thick amber edges from 5 to 6 and 7.
   :width: 70%
   :align: center

   Amber: taken now (5). Ring: open (6, 4, 2 and 7). Gray: done (S, 1 and
   3). Thick amber edges: 5 to 6 and 5 to 7.

#. Take 5: :math:`f = 246` (the lowest; next is 276). Its :math:`g` is
   final.
#. Check its roads:

   - 6: :math:`g = 180 + 53 = 233`, :math:`f = 233 + 40 = 273`
   - 7: :math:`g = 180 + 179 = 359`, :math:`f = 359 + 149 = 508`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g`
     - :math:`h`
     - :math:`f`
     - **from**
   * - 6
     - 233
     - 40
     - 273
     - 5
   * - 4
     - 171
     - 105
     - 276
     - 3
   * - 2
     - 108
     - 221
     - 329
     - 1
   * - 7
     - 359
     - 149
     - 508
     - 5

Done: S, 1, 3, 5.


A*, Step 5: Take Node 6
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_ast_5.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 6 is amber: taken from the open set in this step. Gray, done: S, 1, 3 and 5. Black rings, open: G, 4, 2 and 7. Thick amber edges from 6 to 4 and G.
   :width: 70%
   :align: center

   Amber: taken now (6). Ring: open (G, 4, 2 and 7). Gray: done (S, 1, 3
   and 5). Thick amber edges: 6 to 4 and 6 to G.

#. Take 6: :math:`f = 273` (the lowest; next is 276). Its :math:`g` is
   final.
#. Check its roads:

   - 4: :math:`g = 233 + 66 = 299`, not less than 171: keep 171
   - G: :math:`g = 233 + 40 = 273`, :math:`f = 273 + 0 = 273`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g`
     - :math:`h`
     - :math:`f`
     - **from**
   * - G
     - 273
     - 0
     - 273
     - 6
   * - 4
     - 171
     - 105
     - 276
     - 3
   * - 2
     - 108
     - 221
     - 329
     - 1
   * - 7
     - 359
     - 149
     - 508
     - 5

Done: S, 1, 3, 5, 6.


A*, Step 6: Take G, the Route Is Final
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_ast_6.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node G is amber: taken from the open set. The route S, 1, 3, 5, 6, G is drawn as thick blue edges. Gray, done: S, 1, 3, 5 and 6. Black rings, still open: 4, 2 and 7.
   :width: 70%
   :align: center

   Amber: taken now (G). Ring: still open (4, 2 and 7). Gray: done (S, 1, 3,
   5 and 6). Thick blue edges: the route S, 1, 3, 5, 6, G.

#. Take G: :math:`f = 273` (the lowest; next is 276). Its :math:`g` is
   final.
#. G is the goal: stop. Read the route back through "from": G, 6, 5, 3, 1,
   S.
#. Route S, 1, 3, 5, 6, G: :math:`41 + 75 + 64 + 53 + 40 = 273` m.

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g`
     - :math:`h`
     - :math:`f`
     - **from**
   * - 4
     - 171
     - 105
     - 276
     - 3
   * - 2
     - 108
     - 221
     - 329
     - 1
   * - 7
     - 359
     - 149
     - 508
     - 5

Done: S, 1, 3, 5, 6, G.


Dijkstra Against A* on the Intersection Graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * -
     - **Dijkstra**
     - **A\***
   * - route
     - S, 1, 3, 5, 6, G
     - S, 1, 3, 5, 6, G
   * - cost
     - 273 m
     - 273 m
   * - nodes taken
     - 8: S, 1, 2, 3, 4, 5, 6, G
     - 6: S, 1, 3, 5, 6, G

- **Node 2:** :math:`f = 108 + 221 = 329`. A* reached G at 273 before 329
  came up.
- **Node 4:** :math:`f = 171 + 105 = 276`, just above G's 273. The route
  through 4 is 277 m, only 4 m longer.
- A* took only the six nodes of the route: here :math:`h` led it straight
  along the route.


An Admissible Heuristic Never Overestimates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: admissible heuristic
   :class: note

   :math:`h` is admissible if, for every node :math:`n`, :math:`h(n)` is no
   more than the true cost of the cheapest route from :math:`n` to the goal.
   With an admissible :math:`h`, A* returns a cheapest route.

**The straight line is admissible for distance:** every road from :math:`n`
to G is at least as long as the straight line between them. On the
intersection graph:

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * -
     - S
     - 1
     - 2
     - 3
     - 4
     - 5
     - 6
     - 7
     - G
   * - :math:`h`
     - 142
     - 165
     - 221
     - 117
     - 105
     - 66
     - 40
     - 149
     - 0
   * - true cost to G
     - 273
     - 232
     - 299
     - 157
     - 106
     - 93
     - 40
     - 272
     - 0


An Overestimate: What If h(5) Were 150?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Imagine a heuristic that is wrong at one node: :math:`h(5) = 150`, while the
true cost from 5 to G is :math:`53 + 40 = 93`. The value 150 is chosen for
this example; every other :math:`h` stays the straight line.

- Steps 1 and 2 are the same as before: take S, then 1.
- From step 3 on, node 5 looks worse than it is: :math:`f = 180 + 150 = 330`
  instead of 246.
- The next four steps run A* again from step 3.

.. important::

   GP4's planner stub warns: "An inadmissible heuristic still returns a path,
   just not the shortest, and nothing reports the difference."


Overestimate, Step 3: Take Node 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_wrong_3.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 3 is amber: taken from the open set in this step. Gray, done: S and 1. Black rings, open: 4, 2 and 5. Thick amber edges from 3 to 4 and 5.
   :width: 70%
   :align: center

   Amber: taken now (3). Ring: open (4, 2 and 5). Gray: done (S and 1).
   Thick amber edges: 3 to 4 and 3 to 5.

#. Take 3: :math:`f = 233` (the lowest; next is 329). Its :math:`g` is
   final.
#. Check its roads:

   - 4: :math:`g = 116 + 55 = 171`, :math:`f = 171 + 105 = 276`
   - 5: :math:`g = 116 + 64 = 180`, :math:`f = 180 + 66 = 246`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g`
     - :math:`h`
     - :math:`f`
     - **from**
   * - 4
     - 171
     - 105
     - 276
     - 3
   * - 2
     - 108
     - 221
     - 329
     - 1
   * - 5
     - 180
     - 66
     - 330
     - 3

Done: S, 1, 3.


Overestimate, Step 4: Take Node 4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_wrong_4.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 4 is amber: taken from the open set in this step. Gray, done: S, 1 and 3. Black rings, open: 6, 2 and 5. Thick amber edge from 4 to 6.
   :width: 70%
   :align: center

   Amber: taken now (4). Ring: open (6, 2 and 5). Gray: done (S, 1 and 3).
   Thick amber edge: 4 to 6.

#. Take 4: :math:`f = 276` (the lowest; next is 329). Its :math:`g` is
   final.
#. Check its roads:

   - 6: :math:`g = 171 + 66 = 237`, :math:`f = 237 + 40 = 277`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g`
     - :math:`h`
     - :math:`f`
     - **from**
   * - 6
     - 237
     - 40
     - 277
     - 4
   * - 2
     - 108
     - 221
     - 329
     - 1
   * - 5
     - 180
     - 66
     - 330
     - 3

Done: S, 1, 3, 4.


Overestimate, Step 5: Take Node 6
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_wrong_5.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node 6 is amber: taken from the open set in this step. Gray, done: S, 1, 3 and 4. Black rings, open: G, 2 and 5. Thick amber edges from 6 to 5 and G.
   :width: 70%
   :align: center

   Amber: taken now (6). Ring: open (G, 2 and 5). Gray: done (S, 1, 3 and
   4). Thick amber edges: 6 to 5 and 6 to G.

#. Take 6: :math:`f = 277` (the lowest; next is 329). Its :math:`g` is
   final.
#. Check its roads:

   - 5: :math:`g = 237 + 53 = 290`, not less than 180: keep 180
   - G: :math:`g = 237 + 40 = 277`, :math:`f = 277 + 0 = 277`

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g`
     - :math:`h`
     - :math:`f`
     - **from**
   * - G
     - 277
     - 0
     - 277
     - 6
   * - 2
     - 108
     - 221
     - 329
     - 1
   * - 5
     - 180
     - 66
     - 330
     - 3

Done: S, 1, 3, 4, 6.


Overestimate, Step 6: Take G, the Route Is Final
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L7/toy_wrong_6.png
   :alt: The intersection graph, as in the earlier figure, with edge lengths beside the edges. Node G is amber: taken from the open set. The route S, 1, 3, 4, 6, G is drawn as thick rust edges. Gray, done: S, 1, 3, 4 and 6. Black rings, still open: 2 and 5. Never reached: 7, a plain white circle.
   :width: 70%
   :align: center

   Amber: taken now (G). Ring: still open (2 and 5). Gray: done (S, 1, 3, 4
   and 6). Thick rust edges: the route S, 1, 3, 4, 6, G. Node 7 is never
   reached.

#. Take G: :math:`f = 277` (the lowest; next is 329). Its :math:`g` is
   final.
#. G is the goal: stop. Read the route back through "from": G, 6, 4, 3, 1,
   S.
#. Route S, 1, 3, 4, 6, G: :math:`41 + 75 + 55 + 66 + 40 = 277` m.

.. list-table::
   :widths: auto
   :header-rows: 1
   :class: compact-table

   * - **Open**
     - :math:`g`
     - :math:`h`
     - :math:`f`
     - **from**
   * - 2
     - 108
     - 221
     - 329
     - 1
   * - 5
     - 180
     - 66
     - 330
     - 3

Done: S, 1, 3, 4, 6, G.


The Overestimate Cost 4 m, and Nothing Said So
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

- Same number of steps, a route 4 m longer, and the search ends normally.
- The fault does not show in the output: you find it only by checking that
  :math:`h` never exceeds the true cost, or by comparing with Dijkstra.


For Travel Time, h Must Be in Seconds Too
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With travel time as the cost, the straight line in meters is not in the
costs' units. Divide it by the highest speed on any road:

.. math::

   h(n) = \frac{\text{straight line from } n \text{ to G}}{v_{\max}}, \qquad
   v_{\max} = 11.18\text{ m/s in Town01}

No route can be faster than driving the straight line at the top speed, so
this :math:`h` is admissible.

**Measured on the full waypoint graph**, travel-time costs:

- :math:`h` in seconds, as above: the fastest route, 27.7 s, through 4.
- :math:`h` left in meters (the units mistake): every :math:`h` is 11.18
  times too large. A* returns the route through 5: 31.0 s,
  :math:`31.0 - 27.7 = 3.3` s slower, and reports nothing.


Check: Heuristics
~~~~~~~~~~~~~~~~~

**Question.** A team uses :math:`h(n)` = the distance from :math:`n` to G
along the :math:`x` axis plus the distance along the :math:`y` axis (the
"city block" distance), with distance costs. Town01's streets run east-west
and north-south. Is this :math:`h` admissible?

.. dropdown:: Answer
   :class-container: sd-border-success

   **No.** A lane cuts the corner in a turn, so a route can be shorter than
   the two straight legs. Measured on Town01's waypoint graph, with our G:
   the city block distance is more than the true cost at 560 of the 3107
   nodes, by up to 14.5 m. The straight line is more at none.
