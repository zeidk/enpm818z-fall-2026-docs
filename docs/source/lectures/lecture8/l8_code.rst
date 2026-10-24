====================================================
Code
====================================================

The L8 hands-on is the folder ``lecture8/`` of
`enpm818z-fall-2026-carla-python
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture8>`_.
Every part uses **one junction of CARLA's Town01**, the same scene the
lecture uses: the AV driving east, car A ahead of it on the other lane,
braking and about to turn left across the AV's lane, and car B following A.

You need Python with ``numpy`` and ``matplotlib``. You need **no CARLA
server, no ROS and no GPU**.

.. list-table::
   :widths: 14 46 40
   :header-rows: 1
   :class: compact-table

   * - **Part**
     - **What it shows**
     - **Lecture slide**
   * - ``scene``
     - the junction, the AV, car A and car B over time, and the tracked
       positions the AV sees
     - "Hands-on, part 1: the scene" (The Scene)
   * - ``physics``
     - CV, CTRV and CTRA for car A, from any "now", against the truth
     - "Hands-on, part 2: physics models" (Physics Models)
   * - ``modes``
     - map-aware prediction: car A's two futures and their probabilities
     - "Hands-on, part 3: two futures and their probabilities" (Using the
       Map)
   * - ``interact``
     - car B behind A (the IDM), and A's gap to the AV
     - "Hands-on, part 4: drivers who react" (Other Drivers)


Run It
------

Get the repository, then go to the folder:

.. code-block:: bash

   git clone https://github.com/rubixcubic/enpm818z-fall-2026-carla-python.git
   cd enpm818z-fall-2026-carla-python/lecture8

Each part opens a matplotlib window:

.. code-block:: bash

   python3 l8_handson.py --part scene      # 1. the junction, the AV, car A and car B over time
   python3 l8_handson.py --part physics    # 2. CV, CTRV and CTRA for car A, from any "now"
   python3 l8_handson.py --part modes      # 3. map-aware prediction: two futures, their probabilities
   python3 l8_handson.py --part interact   # 4. car B behind A (IDM), and A's gap to the AV

   # save a still instead of opening a window
   python3 l8_handson.py --part physics --snapshot physics.png

Every part has a **now** slider, under the plots: the moment the
predictors predict from. Drag it to predict from another moment, from
−0.5 s to 3 s (the ``scene`` part from −2 s). :math:`t` = 0 is the
lecture's "now", 2.0 s into car A's braking.


Options
~~~~~~~

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Option**
     - **What it does**
   * - ``--part scene|physics|modes|interact``
     - Which part to run. Required.
   * - ``--now T``
     - Opens at T seconds instead of 0.
   * - ``--snapshot FILE``
     - Saves a still as a PNG file instead of opening a window.
   * - ``--html FILE``
     - Saves an animation over "now" as an HTML page; open it in a browser.


The Scene
---------

Junction 54 of Town01, a T-junction at :math:`x` = 156 m, :math:`y` = −2 m.
The lanes come from CARLA's ``Town01.xodr``, read by ``export_scene.py``
through ``carla.Map`` with no CARLA server, and saved in ``l8_scene.npz``.
The map frame has :math:`x` east and :math:`y` north, in meters (CARLA's
:math:`y` is flipped, as in L6).

- **The AV** drives east at 8 m/s, straight on.
- **Car A** drives west, brakes at 1.0 m/s² from 8 m/s and turns left at
  5.0 m/s, across the AV's lane. It turns only if the AV is at least 4.1 s
  from the crossing when A is 6 m before the junction (its gap); otherwise
  it waits.
- **Car B** follows car A and goes straight on. The Intelligent Driver Model
  (IDM) drives it.

The predictors read only each car's **track**: its position every 0.1 s,
with a 0.05 m error. Everything after "now" is the truth they must guess.
Run 2 (the check box in part 4) moves the AV 24 m closer, so A's gap is
3.0 s and A waits.

.. important::

   **The motion is simulated, and every number above is chosen.** CARLA only
   gives the lanes.


What Each Part Shows
--------------------

Part 1: The Scene (``--part scene``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The three road users over time, and the tracked positions the AV sees. The
title gives the time and each road user's speed.

**What to look for:** drag the now slider from −2 to 3 s. At which time can
you first tell, by eye, that car A is slowing down? That it turns?


Part 2: Physics Models (``--part physics``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Car A's future from constant velocity (CV), constant turn rate and velocity
(CTRV) and constant turn rate and acceleration (CTRA), against the truth, on
the left. On the right, each one's error against the horizon; the title
gives each model's error at 5 s (its FDE).

**What to look for:**

1. At now = 0: read each model's error at 5 s in the right panel's title
   (FDE). Which is smallest, and why?
2. Move now from 0 to 3.0 s, 0.5 s at a time. When does CTRV beat CV at 5 s?
   When does it lose?
3. Where is CTRA worst: while A brakes, or while it speeds up after the
   turn?


Part 3: Two Futures and Their Probabilities (``--part modes``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The map gives car A two lanes, straight on and left. Each lane is one
future, drawn with a line width that shows its probability. The probability
comes from how well the lane explains A's speed, its heading and its offset
from the lane's center (Bayes' rule). On the right: P(left) against time.

**What to look for:**

1. Move now from −0.5 to 1.0 s. Watch the line widths (the probabilities)
   and P(left) on the right.
2. In ``l8sim.py``, set ``SIG_V = 0.5``, then ``2.0``. ``SIG_V`` is the
   :math:`\sigma` of the speed likelihood, 1.0 m/s in the lecture. What
   happens to P(left) at :math:`t` = 0, and why?
3. Set ``A_LAT = 1.5``. ``A_LAT`` is the sideways acceleration the
   predictor assumes in a turn, 2.0 m/s² in the lecture. Does the left
   mode's FDE go down? Why?

Set each value back after you try it: the other parts use the same file.


Part 4: Drivers Who React (``--part interact``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Left:** car A's meters driven against time: the truth, the most likely
mode, and the same mode with the gap rule. **Right:** car B's speed: the
truth, CV, and the IDM behind A's predicted future. Tick **AV 24 m closer**
for run 2.

**What to look for:**

1. Run 1: compare B's speed from CV and from the IDM. When do they part?
2. Tick **AV 24 m closer** (run 2). Read A's gap in the title. Which of the
   two "most likely mode" lines matches the truth?
3. In ``l8sim.py``, set ``GAP = 2.5``. ``GAP`` is the critical headway, 4.1 s
   in the lecture. What does A do in run 2 now? And car B, behind it?


The Files
---------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **What it is**
   * - ``l8sim.py``
     - the scene, the true motion, the track, the fit, the predictors, the
       scores and the test set
   * - ``l8_handson.py``
     - the four parts
   * - ``export_scene.py``
     - writes ``l8_scene.npz`` from ``Town01.xodr``; needs CARLA's Python
       package (``pip install carla==0.9.16``), no server
   * - ``l8_scene.npz``
     - the lanes of junction 54
   * - ``tests/``
     - the tests, below

The numbers on the slides come from ``l8sim.py``, through the slides' figure
generator.

**Values we chose,** all at the top of ``l8sim.py``: a track every 0.1 s
with a 0.05 m error, 2 s of history, the last 1.5 s used for the fit, a 5 s
horizon; a cruising speed of 8 m/s; a sideways acceleration in a turn of
2.0 m/s² (``A_LAT``) and an expected braking of 1.0 m/s² before a turn;
the spreads of the three likelihoods, 1.0 m/s (``SIG_V``), 8° and 0.7 m;
CV's speed drift, 0.5 m/s per :math:`\sqrt{\text{s}}`; car A's decision
point, 6 m before the junction. **From sources:** the 2.0 m miss threshold
(Argoverse), the 4.1 s critical headway (``GAP``, the Highway Capacity
Manual's value), and the IDM's :math:`T`, :math:`a_{\max}`, :math:`b`,
:math:`\delta` and :math:`s_0` (Treiber et al., 2000), with our own desired
speed of 9 m/s.


Run the Tests
~~~~~~~~~~~~~

From ``lecture8/``:

.. code-block:: bash

   python3 -m pytest -q tests

The tests check the fit, CV by hand, that CTRV stays on its circle and
becomes CV when it does not turn, ADE, FDE and the minimum over modes, the
IDM's steady gap, that the mode probabilities add up to 1 and favor the
turn, that the two runs share their history, and that each part saves a
snapshot. One test checks that no public file in the folder holds group
project solution code. One test compares the code with the slides' numbers;
it is skipped when the slides' files are not on your computer.


Foxglove, Next to RViz
----------------------

The last slide of L8 introduces Foxglove, a second viewer for ROS 2 next to
RViz (`Foxglove's ROS 2 guide
<https://docs.foxglove.dev/docs/getting-started/frameworks/ros2>`__). It
connects to a running ROS 2 system through ``foxglove_bridge``, and it opens
ROS 2 recordings (``.mcap`` files).

.. code-block:: bash

   sudo apt install ros-$ROS_DISTRO-foxglove-bridge
   ros2 launch foxglove_bridge foxglove_bridge_launch.xml
   # in Foxglove: Open connection, Foxglove WebSocket,
   #   then the address ws://localhost:8765
   ros2 bag record -s mcap --all   # a recording Foxglove opens

- Foxglove needs a free account. Sign up with your umd.edu address: the
  Academic plan costs nothing.
- **Post-work:** record 30 s of your GP stack and open the recording in
  Foxglove.
