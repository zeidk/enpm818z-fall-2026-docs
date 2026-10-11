====================================================
SLAM with a LiDAR
====================================================

.. admonition:: Read this after L6
   :class: important

   This page is **reading material** for :doc:`L6 </lectures/lecture6/l6_index>`.
   L6 ended with a pose graph of three nodes and a LiDAR drift it did not
   correct. This page builds the whole thing: the SLAM problem, the three
   families of solutions, a LiDAR front end, loop detection, and a back end
   that removes the drift from our L6 drive. Its companion,
   :doc:`Visual SLAM </preread/slam-visual>`, does the same with a camera on
   the same route.

**Every number on this page was measured.** Two sets of data:

- **A simulated world** for EKF-SLAM and FastSLAM: a robot drives two laps
  of a circle among 24 landmarks. All its settings are chosen for the
  example and listed where they are used.
- **The L6 drive** for graph SLAM: the same recording the L6 hands-on used,
  1,256 2-D LiDAR scans at 10 Hz over two laps of one block in CARLA's
  Town10HD, 916 m in all, with a median of 461 points per scan and the true
  pose of every scan.

The code that measured them is ours, written in Python with NumPy and
SciPy. The code for the L6 drive is in the course repository, in
`lecture6/slam <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture6/slam>`__: run it and you get the same numbers, then change
a value and see what happens. The EKF-SLAM and FastSLAM simulation is not
published: GP3 asks you to build an EKF yourself. The solve times quoted
below are from one desktop PC and tell you how the costs compare, not what a
real-time system needs.


What SLAM Is
------------

.. admonition:: Definition: SLAM
   :class: note

   "SLAM is a process by which a mobile robot can build a map of an
   environment and at the same time use this map to deduce its location"
   (Durrant-Whyte and Bailey, 2006).

**What the robot knows.** At each time step :math:`t` it knows:

- its **controls** :math:`u_{1:t}`: what the wheels and the gyro said it
  did, or what it told the motors;
- its **measurements** :math:`z_{1:t}`: the scans, the images, the ranges
  to landmarks.

**What it wants.** Two unknowns:

- its **path** :math:`x_{1:t}`: one pose :math:`x_t` per step, its position
  and heading :math:`(x, y, \theta)` on flat ground;
- the **map** :math:`m`: a list of landmarks, a grid of occupied cells, or
  a cloud of points.

Written as a probability, SLAM asks for

.. math::

   p(x_{1:t},\, m \mid z_{1:t},\, u_{1:t})

the path and the map, given everything measured. A filter keeps only the
newest pose, :math:`p(x_t, m \mid z_{1:t}, u_{1:t})`, and forgets the
older ones. A graph keeps the whole path. That choice splits the methods
below.

**Why the two unknowns cannot be solved one at a time.**

1. With the true path, mapping is easy: place every scan at its pose and
   draw. L6's mapping pass did this with CARLA's true poses.
2. With a true map, localization is easy: L6 did it with MCL and ICP.
3. With neither, every landmark is placed from a pose that is itself
   uncertain. The pose error goes into the landmark's position. Later the
   robot uses that landmark to find its pose, and the old error comes back.
   So the errors of the robot and of every landmark it has seen are
   **correlated**: they are not independent of each other.

That correlation is the reason SLAM works. When the robot comes back to a
place it mapped early, when its pose was still sure, the old landmarks pull
its pose back. Through the correlations, that correction also moves every
landmark mapped since. This is the **loop closure** from L6, and the rest of
this page measures it.

**Three families.** Each one keeps a different description of the same
unknowns:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Family
     - What it keeps
     - What it costs
   * - EKF-SLAM
     - one Gaussian over the newest pose and every landmark
     - every observation updates every number: quadratic in the landmarks
   * - FastSLAM
     - many particles; each holds one path and a small Gaussian per landmark
     - linear in particles times landmarks, less with a tree
   * - Graph SLAM
     - every pose, joined by measured motions; solved as least squares
     - a sparse linear system per iteration


EKF-SLAM: One Gaussian over the Robot and the Map
-------------------------------------------------

The simulated world
~~~~~~~~~~~~~~~~~~~

All values are chosen for the example.

- A robot drives two laps of a circle of radius 20 m at 2 m/s. One lap
  takes 62.8 s; with a time step of 0.1 s, the two laps are 1,256 steps.
- 24 landmarks stand at random between 14 and 26 m from the center.
- **Odometry:** the speed reads with noise of standard deviation 0.10 m/s,
  the turn rate with 1°/s.
- **Sensor:** range and bearing to every landmark within 12 m; range noise
  0.20 m, bearing noise 2°. Each landmark carries its ID, so the filter
  always knows which landmark it sees. That is the **data association**
  L6 named, given for free here so the page can show the filters
  themselves.

**Dead reckoning,** odometry alone, ends **2.38 m** from the true pose after
the two laps.


The state: 51 numbers
~~~~~~~~~~~~~~~~~~~~~

EKF-SLAM stacks the robot's pose and every landmark into one vector:

.. math::

   \mu = (x,\ y,\ \theta,\ m_{1,x},\ m_{1,y},\ \dots,\ m_{N,x},\ m_{N,y})

With :math:`N = 24` landmarks, that is :math:`3 + 2 \times 24 = 51`
numbers. The filter keeps their mean :math:`\mu` and their
:math:`51 \times 51` **covariance** :math:`\Sigma`. The diagonal holds each
number's variance. The off-diagonal terms hold how the error of one number
goes with the error of another: the correlations above.

Smith, Self and Cheeseman described this representation and called it the
**stochastic map**: "It contains estimates of the spatial relationships,
their uncertainties, and their inter-dependencies" (Smith, Self and
Cheeseman, 1990).


Step 1: predict. Only the robot moves
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With speed :math:`v` and turn rate :math:`\omega` from odometry, over
:math:`\Delta t`:

.. math::

   x \leftarrow x + v \cos\theta\,\Delta t, \qquad
   y \leftarrow y + v \sin\theta\,\Delta t, \qquad
   \theta \leftarrow \theta + \omega\,\Delta t

The landmarks do not move, so their part of :math:`\mu` stays. In the
covariance, only the robot's 3 rows and 3 columns change: the robot block
grows by the odometry noise, and the robot-to-landmark terms are turned
by the motion's Jacobian. The cost is linear in the size of the state.


Step 2: update. One landmark changes every number
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The robot measures landmark :math:`i` at range :math:`r` and bearing
:math:`\phi`. From the state, the filter predicts what it should have
measured. With :math:`\delta_x = m_{i,x} - x`, :math:`\delta_y = m_{i,y} -
y` and :math:`q = \delta_x^2 + \delta_y^2`:

.. math::

   \hat{z} = \begin{bmatrix} \sqrt{q} \\
   \operatorname{atan2}(\delta_y, \delta_x) - \theta \end{bmatrix}

The prediction depends on 5 numbers only: the robot's 3 and the
landmark's 2. So its Jacobian :math:`H` (2 rows, 51 columns) is zero
except in those 5 columns. Then the usual Kalman update, with :math:`Q` the
sensor noise:

.. math::

   K = \Sigma H^\top (H \Sigma H^\top + Q)^{-1}, \qquad
   \mu \leftarrow \mu + K (z - \hat{z}), \qquad
   \Sigma \leftarrow \Sigma - K H \Sigma

:math:`H` is sparse, but :math:`\Sigma` is full, so the gain :math:`K =
\Sigma H^\top (\dots)^{-1}` is a full column of 51 rows. **One
measurement of one landmark moves every landmark,** in proportion to how
its error is correlated with the robot's and with that landmark's. The last
step, :math:`\Sigma - K H \Sigma`, touches all :math:`51 \times 51` entries.

A landmark seen for the first time is placed at
:math:`(x + r\cos(\phi + \theta),\ y + r\sin(\phi + \theta))`, and its
variance starts very large (we chose :math:`10^6` m²), so the first update
sets it from the measurement.


The loop closure, measured
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/SLAM/toy_ekf_slam.png
   :alt: Two panels. Left: a top view of the circular path in gray, the dead-reckoning path in red, which ends about 2.4 meters off, 24 black landmark dots, and small blue 3-sigma ellipses around the EKF-SLAM landmark estimates, smallest near the start at the right of the circle. Right: uncertainty in meters against time in seconds. A red line, the robot's 1-sigma position uncertainty, climbs from 0 to 0.575 meters at about 50 seconds, drops sharply at a green dashed line labeled loop closure, a lap-1 landmark seen again, then rises to about 0.26 meters near 96 seconds and falls to about 0.05 at the end. A blue line, the mean 1-sigma of the landmarks seen so far, rises in steps to about 0.35 meters, drops at the same moment, and settles near 0.16 meters.
   :align: center
   :width: 100%

   **Left:** the true path (gray), dead reckoning (red), the true landmarks
   (black) and EKF-SLAM's landmarks with their 3-sigma ellipses (blue).
   **Right:** the robot's position uncertainty (red) and the mean
   uncertainty of the landmarks seen so far (blue), each as 1 sigma:
   :math:`\sqrt{\sigma_x^2 + \sigma_y^2}`.

What the right panel shows, step by step:

1. **Lap 1, before the closure.** Every step adds odometry noise, and new
   landmarks are mapped from the less and less sure pose. The robot's 1
   sigma climbs to **0.575 m**. Each new landmark is placed from the
   robot's pose, so it starts at least as unsure as the robot was. The
   landmarks' mean climbs in steps, one per new landmark, to **0.344 m**.
2. **The closure, at 50.7 s.** The robot sees a landmark it last saw more
   than 20 s before, one it mapped near the start. 0.5 s later, the robot's
   1 sigma is **0.253 m** and the landmarks' mean **0.236 m**. Landmarks the
   robot does not see at that moment get surer too: their errors were
   correlated with the robot's.
3. **Lap 2.** The robot's uncertainty rises again, to **0.259 m** at
   96.1 s, then falls. 96.1 s is 33.3 s into lap 2, about half a lap: the
   robot is on the far side of the circle from the start. The map is held
   in place by the first pose. Landmarks far from the start are less sure
   of where they are in that frame, and a robot that sees only them can be
   no surer than they are.
4. **At the end:** the robot's 1 sigma is **0.045 m** and the landmarks'
   mean **0.163 m**. The true errors are smaller: the robot ends **0.038 m**
   from its true pose, and the landmarks are **0.051 m** off on average,
   **0.092 m** at most. Dead reckoning ended 2.38 m off.

.. figure:: /_static/images/SLAM/toy_ekf_correlation.png
   :alt: A 51 by 51 square heat map of the absolute correlation between every pair of state numbers at the end of the run, on a scale from 0, dark purple, to 1, yellow. The diagonal is yellow. Most of the square is green to yellow, above 0.6, with a few dark rows and columns.
   :align: center
   :width: 60%

   The absolute correlation between every pair of numbers in the state at
   the end, :math:`|\Sigma_{ij}| / \sqrt{\Sigma_{ii}\Sigma_{jj}}`. Index 0
   to 2 is the robot, then 2 per landmark. Most pairs are above 0.6.

The correlation matrix is why the update must touch every number. Dropping
the off-diagonal terms to save time would throw away the links that let one
closure correct the whole map.


The cost: quadratic in the landmarks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"The observation update step requires that all landmarks and the joint
covariance matrix be updated every time an observation is made. Naively,
this means computation grows quadratically with the number of landmarks"
(Durrant-Whyte and Bailey, 2006).

We timed one update (one landmark, one measurement) on the same circle
with more landmarks, and took the median over the first 300 steps:

.. list-table::
   :widths: 25 25 50
   :header-rows: 1
   :class: compact-table

   * - Landmarks :math:`N`
     - State size :math:`3 + 2N`
     - Time per update (median)
   * - 24
     - 51
     - 0.030 ms
   * - 100
     - 203
     - 0.113 ms
   * - 200
     - 403
     - 0.371 ms
   * - 400
     - 803
     - 1.562 ms

From 403 to 803 numbers, the state about doubles and the time grows
:math:`1.562 / 0.371 = 4.2` times: quadratic. The small states are
dominated by the fixed cost of each call. A city map holds far more than
400 landmarks, so EKF-SLAM in this plain form does not scale to one.

**Its other limits.**

- **Linearization.** :math:`H` is computed at the current estimate. When
  the estimate is far off, as before a large loop closure, the linear
  model is wrong, and the update can be too.
- **Data association.** Here every landmark carried its ID. A real
  front end must decide which landmark it sees, and one wrong decision is
  folded into all 51 numbers for good. A filter cannot undo an update.


FastSLAM: Many Robots, Each with Its Own Small Maps
---------------------------------------------------

FastSLAM (Montemerlo et al., 2002) starts from one fact. **If the path
were known, the landmarks would be independent of each other:** each
landmark's error would come only from its own measurements. The paper
writes the posterior as a path part times one part per landmark:

.. math::

   p(s^t, \theta \mid z^t, u^t, n^t) =
   p(s^t \mid z^t, u^t, n^t)\,
   \prod_k p(\theta_k \mid s^t, z^t, u^t, n^t)

In the paper's letters, :math:`s^t` is the path, :math:`\theta_k` the
landmark :math:`k`, and :math:`n^t` the **correspondences**, which
landmark each measurement saw. The condition matters: "all individual
landmark estimation problems are independent if one knew the robot's path
:math:`s^t` and the correspondence variables :math:`n^t`" (Montemerlo et
al., 2002). Both must be known.

**The algorithm** keeps :math:`M` particles. Each particle is one guess of
the path, plus :math:`N` small EKFs, one :math:`2 \times 2` Gaussian per
landmark. At each step:

1. **Move every particle** with the odometry, plus noise drawn at random.
   Each particle drifts its own way.
2. **Update each particle's landmark EKFs** with the measurements, as if
   that particle's path were true. Each EKF has 2 numbers, so this is
   cheap.
3. **Weigh each particle** by how well its own map predicted the
   measurements: the product, over the landmarks seen, of the Gaussian
   :math:`\mathcal{N}(z;\, \hat{z},\, Z)`, with :math:`Z` the predicted
   measurement's covariance.
4. **Resample** when a few particles carry most of the weight. We used
   the rule from GMapping: "We resample each time :math:`N_{eff}` drops
   below the threshold of :math:`N/2` where :math:`N` is the number of
   particles" (Grisetti, Stachniss and Burgard, 2007), with
   :math:`N_{eff} = 1 / \sum_i w_i^2` for normalized weights :math:`w_i`.

L6's MCL used the same predict, weigh and resample loop with a fixed map.
Here every particle also builds its own map.


FastSLAM on the same world, measured
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same world, same odometry, same measurements as EKF-SLAM above. We ran
FastSLAM with 5, 20 and 100 particles, 3 times each with a different random
seed for the particles. The error is the distance from the mean of the
particles to the true pose at the end.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Particles :math:`M`
     - Robot error at the end, 3 runs
     - Lap-1 histories left at the end
   * - 5
     - 0.188, 0.915, 0.948 m
     - 1, 1, 1
   * - 20
     - 0.125, 0.246, 0.308 m
     - 1, 1, 1
   * - 100
     - 0.013, 0.084, 0.029 m
     - 1, 1, 1
   * - EKF-SLAM
     - 0.038 m (one run, no randomness)
     -

**Read the error column first.** With 5 particles, two of three runs end
more than 0.9 m off. With 100, all three are within 0.084 m, close to
EKF-SLAM's 0.038 m. A particle filter needs enough particles to have one
near the truth.

**Then the last column.** At the end of lap 1 we tagged the :math:`M`
particles alive then. By the end of lap 2, in all 9 runs, every particle
descends from the same one. Resampling copies good particles and drops the
rest, and each copy carries its parent's whole path. After enough
resampling, the particles agree on the old part of the path: one
history is left, and whatever error it holds can no longer be corrected by
choosing another. More particles did not prevent it here.

**The cost.** Each step updates :math:`M` particles, but only the landmarks
seen, so it does not grow with the map. Resampling copies whole
particles, and that does: "A naive implementation of this idea leads to an
algorithm that requires O(M K) time, where M is the number of particles in
the particle filter and K is the number of landmarks" (Montemerlo et al.,
2002). Our code is that naive version. The paper stores each particle's
landmarks in a balanced binary tree, so copies share the landmarks that did
not change: "Our approach makes it possible to execute a FastSLAM
iteration in O(M log K) time" (Montemerlo et al., 2002).


Grid maps with particles: GMapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A LiDAR in a city sees walls, not 24 named landmarks. So the map in each
particle can be an **occupancy grid** instead:

.. admonition:: Definition: occupancy grid
   :class: note

   The ground is cut into square cells. Each cell holds the probability
   that something occupies it. Each LiDAR beam is a measurement of two
   kinds: the cell where it ended is more likely occupied, and every cell
   it crossed on the way is more likely free.

Each cell keeps its **log odds**, :math:`\ell = \ln\frac{p}{1 - p}`, which
starts at 0 (:math:`p = 0.5`, unknown). Then every beam adds a fixed
amount: a positive one to the cell it ends in, a negative one to each cell
it crosses. Adding is all the update needs, and :math:`p = 1 - 1/(1 +
e^{\ell})` turns the sum back into a probability. Our grids below use 0.2 m
cells, +0.85 for a hit and -0.4 for a pass (both chosen).

GMapping (Grisetti, Stachniss and Burgard, 2007) is FastSLAM with a grid
in every particle, and it attacks the problem the last column above shows.
Two changes:

- **A better proposal.** Instead of moving particles by odometry alone,
  "We propose an approach to compute an accurate proposal distribution
  taking into account not only the movement of the robot but also the most
  recent observation". New particles are drawn near where the scan fits,
  not only where odometry says.
- **Resample less often.** "We present an approach to selectively carry out
  resampling operations which seriously reduces the problem of particle
  depletion": the :math:`N_{eff} < N/2` rule we used above.

We did not run GMapping. The grid maps on this page come from the graph
SLAM poses below.


Graph SLAM: Every Pose, Solved at Once
--------------------------------------

L6 introduced the pose graph and solved a three-node one by hand. Graph
SLAM keeps every pose (or every keyframe) and finds them all together.
The tutorial by Grisetti et al. (2010) splits it in two:

"in graph-based SLAM the problem is decoupled in two tasks: constructing
the graph from the raw measurements (graph construction), determining the
most likely configuration of the poses given the edges of the graph (graph
optimization). The graph construction is usually called front-end and it
is heavily sensor dependent, while the second part is called back-end and
relies on an abstract representation of the data which is sensor
agnostic."

This section is the back end. The next two are the LiDAR front end.


Nodes, edges and the error of one edge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Node** :math:`i`: a pose :math:`x_i = (x_i, y_i, \theta_i)` in the map
  frame. These are the unknowns.
- **Edge** :math:`(i, j)`: a measurement :math:`z_{ij}` of where pose
  :math:`j` is, **seen from pose** :math:`i`: forward, left, and the turn
  from :math:`i` to :math:`j`. It comes with an **information matrix**
  :math:`\Omega_{ij}`, the inverse of its covariance: large for a sure
  edge, small for an unsure one.

From the current guesses of the two poses, the relative pose is

.. math::

   h(x_i, x_j) = \begin{bmatrix}
   \cos\theta_i\,(x_j - x_i) + \sin\theta_i\,(y_j - y_i) \\
   -\sin\theta_i\,(x_j - x_i) + \cos\theta_i\,(y_j - y_i) \\
   \theta_j - \theta_i
   \end{bmatrix}

the step from :math:`i` to :math:`j`, turned into :math:`i`'s own axes.
The edge's **error** is what the poses say minus what was measured:

.. math::

   e_{ij} = h(x_i, x_j) - z_{ij}

with the angle wrapped to :math:`(-\pi, \pi]`. The back end looks for the
poses that make the total weighted error smallest:

.. math::

   F(x) = \sum_{(i,j)} e_{ij}^\top\, \Omega_{ij}\, e_{ij}

L6's three-node example was this sum with positions only, so it was
linear. With the headings in, :math:`h` holds sines and cosines of the
unknowns, and the solver has to iterate.


Gauss-Newton: one step
~~~~~~~~~~~~~~~~~~~~~~

Each iteration replaces each :math:`e_{ij}` by a straight-line version
around the current guess and solves for the step :math:`\Delta x` that
makes the straight-line sum smallest.

**Step 1: the Jacobians of one edge.** With :math:`c = \cos\theta_i`,
:math:`s = \sin\theta_i`, :math:`\Delta_x = x_j - x_i`, :math:`\Delta_y =
y_j - y_i`, the derivatives of :math:`e_{ij}` with respect to pose
:math:`i` and pose :math:`j` are

.. math::

   A_{ij} = \begin{bmatrix}
   -c & -s & -s\,\Delta_x + c\,\Delta_y \\
   s & -c & -c\,\Delta_x - s\,\Delta_y \\
   0 & 0 & -1 \end{bmatrix}, \qquad
   B_{ij} = \begin{bmatrix}
   c & s & 0 \\
   -s & c & 0 \\
   0 & 0 & 1 \end{bmatrix}

The edge depends on no other pose, so its derivative with respect to
every other pose is zero.

**Step 2: add up the normal equations.** :math:`H` has one
:math:`3 \times 3` block per pair of nodes, :math:`b` one 3-vector per
node. Each edge adds to four blocks of :math:`H` and two of :math:`b`:

.. math::

   H_{ii} \mathrel{+}= A_{ij}^\top \Omega_{ij} A_{ij}, \quad
   H_{ij} \mathrel{+}= A_{ij}^\top \Omega_{ij} B_{ij}, \quad
   H_{ji} \mathrel{+}= B_{ij}^\top \Omega_{ij} A_{ij}, \quad
   H_{jj} \mathrel{+}= B_{ij}^\top \Omega_{ij} B_{ij}

.. math::

   b_i \mathrel{+}= A_{ij}^\top \Omega_{ij}\, e_{ij}, \qquad
   b_j \mathrel{+}= B_{ij}^\top \Omega_{ij}\, e_{ij}

**Step 3: solve and move.** Solve :math:`H \Delta x = -b`, the linear
system Grisetti et al. (2010) write as their equation (15), then set
:math:`x \leftarrow x + \Delta x`.

**Step 4: hold one pose.** Shift or turn every pose together and no edge
changes, so the system has no single answer. We hold node 0 at its
starting value: it is the start of the drive, where the AV knows its pose.

**Step 5: repeat** until the step is tiny. We stop when no number moves by
more than :math:`10^{-6}`.


Why the solve is fast: H is sparse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each edge touches the blocks of its two nodes only. So the block
:math:`H_{ij}` is nonzero only if an edge joins :math:`i` and
:math:`j`. Grisetti et al. (2010): "The matrix H is the information matrix
of the system ... It is sparse by construction, having non-zeros between
poses connected by a constraint. Its number of non-zero blocks is twice the
number of constrains plus the number of nodes. This allows to solve Eq.
(15) by sparse Cholesky factorization."

On our drive, below: 387 nodes and 549 edges.

1. :math:`H` has :math:`387 \times 387 = 149{,}769` blocks.
2. Nonzero blocks: :math:`2 \times 549 + 387 = 1{,}485`. We counted them
   in our graph: 1,485.
3. Share nonzero: :math:`1{,}485 / 149{,}769 = 0.99\%`.

.. figure:: /_static/images/SLAM/lidar_sparsity.png
   :alt: A square plot, 387 nodes by 387 nodes, titled 387 nodes, nonzero blocks of H. A thick black line runs down the main diagonal. Two thinner diagonal lines run parallel to it, offset by about 194 nodes, one above and one below, with a few small gaps.
   :align: center
   :width: 55%

   The nonzero blocks of :math:`H` for our drive. **The main diagonal:**
   each node and the odometry edges to its neighbors. **The two lines
   offset by about 194 nodes:** loop edges, each joining a lap-2 keyframe to
   the lap-1 keyframe at the same place. The rest of the square is zero.

Compare EKF-SLAM: its covariance was full, because it kept only the newest
pose and folded the old ones in. Graph SLAM keeps the old poses, and keeping
them is what keeps :math:`H` sparse.


The LiDAR Front End: Odometry from Scans
----------------------------------------

The front end turns raw scans into edges. First the odometry edges, which
join poses in a row.


Scan to scan, or scan to submap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L6's odometry ran ICP between each scan and the one before. Each match has
a small error, and the next match starts from it: the errors add up. Two
ways to run the same ICP:

- **Scan to scan:** match scan :math:`k` against scan :math:`k-1`.
- **Scan to submap:** match scan :math:`k` against the points of the last
  10 keyframes, each placed at its estimated pose (10 is chosen). A new
  keyframe starts every 2 m of travel (chosen).

Both start ICP from the last motion repeated and pair points within 1 m.

.. figure:: /_static/images/SLAM/lidar_odometry_compare.png
   :alt: A top view, x east against y north in meters, of two laps around a rectangular block about 160 by 95 meters, starting at a black dot at the bottom near x 0, y minus 25. The black truth and the blue scan-to-submap path lie almost on top of each other. The red scan-to-scan path drifts outward on the left and bottom sides, ending at about x minus 10, y minus 35.
   :align: center
   :width: 80%

   The truth (black), scan-to-scan odometry (red) and scan-to-submap
   odometry (blue) over the two laps.

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - Over 916 m
     - Scan to scan
     - Scan to submap
   * - Error at the end
     - 11.26 m
     - 1.07 m
   * - RMSE over the drive
     - 7.10 m
     - 0.77 m
   * - Largest error
     - 12.04 m
     - 1.72 m
   * - Heading error at the end
     - 0.66°
     - -1.02°

**Why the submap helps.** Scan to scan, scan :math:`k` is placed relative to
scan :math:`k-1`, which was placed relative to :math:`k-2`, and so on: every
small error stays in the chain. Against a submap, scan :math:`k` is matched
against points from the last 20 m, so an error made at one step is not
passed on unchanged. The submap also holds more points and more walls, so
each match has more to hold on to. Scan-to-submap odometry still drifts:
1.07 m after 916 m. Only a loop closure can remove that.


Other ways to match scans
~~~~~~~~~~~~~~~~~~~~~~~~~

L6 solved point-to-point ICP by hand and named point-to-line. Three more
methods are in wide use.

- **Generalized-ICP** (Segal, Haehnel and Thrun, 2009) models the surface
  near each point, in both scans: "This can be thought of as
  'plane-to-plane'." Point-to-point ICP is an exact special case of it.
  Point-to-plane is only "a limiting case of Generalized-ICP".
- **NDT,** the normal distributions transform (Biber and Straßer, 2003),
  matches a scan to a smooth map instead of to points. L6 used it. The
  paper is 2-D: "the 2D space around the robot is subdivided regularly into
  cells with constant size". Each cell "that contains at least three points"
  gets the mean and covariance of its points, a Gaussian. The paper used
  cells of "100 cm by 100 cm" and "four overlapping grids" to reduce the
  effect of where the cell borders fall.
- **Edge and plane features** (LOAM; Zhang and Singh, 2014): instead of all
  points, keep the few on sharp edges and on flat surfaces: "both
  algorithms extract feature points located on sharp edges and planar
  surfaces, and match the feature points to edge line segments and planar
  surface patches, respectively." LOAM runs a fast, rough odometry and a
  slow, careful mapping: odometry "at a frequency around 10Hz", mapping "at
  a frequency of 1Hz".


Two problems a real LiDAR adds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Motion during the sweep.** A spinning LiDAR takes about 0.1 s to sweep
  at 10 Hz, and the car moves meanwhile. Points at the end of the sweep are
  measured from a different pose than points at the start. **De-skewing**
  moves every point to where it would be from one pose, using the motion
  measured during the sweep. In LIO-SAM, the IMU gives that motion: "The
  estimated motion from inertial measurement unit (IMU) pre-integration
  de-skews point clouds and produces an initial guess for lidar odometry
  optimization" (Shan et al., 2020).
- **Places with nothing to hold.** L6 showed that a straight road between
  two flat walls gives ICP nothing along the road: the scan fits equally
  well a little forward or back (Zhang, Kaess and Singh, 2016). The
  odometry edge is then unsure in one direction, and its information matrix
  should say so.


Loop Closure: Recognizing a Place with Scan Context
---------------------------------------------------

Odometry edges only join poses in a row. To find **loop edges**, the front
end must notice that the AV is back somewhere it has been, without trusting
its drifted pose. L6 showed why: on lap 1's closure, ICP started from the
odometry's guess ended 7.57 m off, at a wrong minimum.


The descriptor: a polar grid around the car
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scan Context** (Kim and Kim, 2018) describes a scan by what lies around
the car, ring by ring and sector by sector:

1. Cut the area within 50 m into **20 rings** (2.5 m each) and **60
   sectors** (6° each). The paper: "In this paper, we used Ns = 60 and
   Nr = 20." The 50 m is our choice.
2. Fill each cell from the points in it. Our 2-D scans have no height, so
   each of our cells holds its **number of points**.
3. The result is a :math:`20 \times 60` image of the scan.

.. figure:: /_static/images/SLAM/lidar_scan_context.png
   :alt: Two stacked heat maps, range in meters from 0 to 50 upward, bearing around the car from 0 to 360 degrees across, 6 degrees per sector. Top, lap 1, keyframe 0; bottom, lap 2, keyframe 194. Both show the same pattern: a U-shaped band of cells between 25 and 50 meters on the left, from 0 to 140 degrees, and another U-shaped band between 13 and 30 meters on the right, from 200 to 340 degrees.
   :align: center
   :width: 85%

   The Scan Context of keyframe 0 (lap 1) and keyframe 194 (lap 2). Brighter
   cells hold more points. The two keyframes are 0.56 m apart; their
   pictures nearly match.


Step 1: propose with the ring key
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comparing every new scan with every old one would be slow. So each scan
also gets a **ring key**: for each of the 20 rings, its share of the
points. If the car turns on the spot, points move from sector to sector but
stay in their ring. "Ring key is a rotation-invariant descriptor, which is
extracted from a scan context" (Kim and Kim, 2018).

For each new keyframe, we look up the 10 nearest ring keys in a k-d tree
(L6's fast nearest-neighbor search) and keep those at least 100 m earlier
along the path (chosen), so a car that is just driving on is not "closing a
loop" with itself.


Step 2: compare, and read the yaw from the shift
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For up to 3 candidates, compare the full :math:`20 \times 60` grids. The
same place, seen after a turn, gives the same grid with its columns
shifted. So the comparison tries every shift: "we calculate distances with
all possible column-shifted scan contexts and find the minimum distance"
(Kim and Kim, 2018).

Our distance, for one shift, is 1 minus the mean cosine similarity of
matching columns: 0 for identical grids. We keep a candidate if its
smallest distance is under 0.35 (chosen). The best shift also gives the
yaw between the two scans, "at :math:`2\pi/N_s` resolution": with 60
sectors, to the nearest 6°.

For the pair in the figure: distance **0.057**, best shift **0 sectors**
(both cars faced the same way), true distance between the two poses
**0.56 m**.


Step 3: verify with ICP
~~~~~~~~~~~~~~~~~~~~~~~

Scan Context says "this looks like that place". ICP says exactly where:
it matches the two scans, starting from zero shift and the yaw from Step 2,
pairing points within 2 m. The paper suggests this: the shift "may serve as
a good initial value for further localization refinement such as Iterated
Closest Point (ICP)". We accept the loop if ICP's final RMSE is under
0.25 m (chosen). The ICP result is the loop edge :math:`z_{ij}`.


Loops on our drive, measured
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 387 keyframes, so 387 lookups.
2. **195** candidates passed the Scan Context distance gate.
3. ICP rejected **32**: their scans did not fit within 0.25 m.
4. **163** loop edges were accepted.
5. **All 163 are right.** We call a loop right when its measured relative
   pose is within 1 m and 5° of the true one.

The ICP check matters: a candidate from Scan Context alone is a guess about
the place, not a measurement of the pose. The Visual SLAM page shows what
happens when a wrong loop gets through.

Simpler systems skip the descriptor. LIO-SAM uses "a naive but effective
Euclidean distance-based loop closure detection approach" (Shan et al.,
2020): it looks for old poses near the current estimate. That works while
the drift is small compared with the search radius.


The Back End on Our Drive
-------------------------

The graph
~~~~~~~~~

- **Nodes:** the 387 keyframes, starting from scan-to-submap odometry.
- **Odometry edges:** 386, one between each pair of keyframes in a row,
  :math:`z_{ij}` from the odometry. Information: we treat each as good to
  5 cm in x and y and 0.5° in heading (chosen).
- **Loop edges:** the 163 above, :math:`z_{ij}` from ICP, treated as good to
  10 cm and 1° (chosen).

Each information matrix is diagonal, with :math:`1/\sigma^2` for each
number: for odometry,
:math:`\Omega = \operatorname{diag}(1/0.05^2,\ 1/0.05^2,\ 1/(0.5°)^2)`, with
the angle in radians.


The solve, measured
~~~~~~~~~~~~~~~~~~~

1. **Before:** the poses come from the odometry, so every odometry edge
   agrees with them exactly. The whole cost :math:`F` comes from the loop
   edges: **8,714.8**.
2. **Iteration 1:** :math:`F` falls to **7.6**.
3. **Iterations 2 to 4** move the poses by less and less, and the run stops:
   4 iterations, **0.09 s** in Python.
4. **APE** (L6's absolute pose error: the distance of each keyframe from
   its true position, summarized by the RMSE): **0.79 m before, 0.24 m
   after**. Largest error: **1.66 m before, 0.43 m after**.


The same back end on worse odometry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The scan-to-submap odometry was already good. To see what the back end can
take, we built the same graph on the **scan-to-scan** odometry, 11.26 m off
at the end. Same 387 keyframes, same 163 loop pairs, each measured again by
ICP between the same two scans.

.. figure:: /_static/images/SLAM/lidar_graph_before_after.png
   :alt: Two top views of the block, with the truth as a thick gray line. Left, titled before, RMSE 7.07 meters: red keyframes from scan-to-scan odometry, with lap 2 drawn outside lap 1 on the left and bottom sides, joined by thin green loop edges. Right, titled after, RMSE 1.56 meters: blue optimized keyframes lie on the gray truth almost everywhere, with a small bulge on the right side near x 110, y 0.
   :align: center
   :width: 100%

   **Left, before:** keyframes from scan-to-scan odometry (red) and the loop
   edges (green, every 4th drawn). **Right, after:** the optimized
   keyframes (blue). The truth is gray.

- APE RMSE: **7.07 m before, 1.56 m after**, in 5 iterations.
- Largest error: **12.04 m before, 3.02 m after**, on the bulge at the right
  side of the block.

The loop edges pull lap 2 onto lap 1, and lap 1's drift is spread along it.
The back end cannot remove an error that both laps share, because no edge
measures it. With the scan-to-submap odometry, less such error is there to
begin with: 0.24 m against 1.56 m.


The map
~~~~~~~

.. figure:: /_static/images/SLAM/lidar_maps.png
   :alt: Two occupancy grid maps of the block, white for free space, dark for walls, gray for unknown. Left, from scan-to-scan odometry: the walls of the inner block appear twice, as two offset outlines, and the outer walls are blurred. Right, from the optimized poses: one sharp outline of the inner block and sharp outer walls.
   :align: center
   :width: 100%

   Occupancy grids built from the 387 keyframe scans, 0.2 m cells. **Left:**
   at the scan-to-scan odometry poses. **Right:** at the optimized poses.
   White is free, dark is occupied, gray is unknown.

On the left, each wall of the inner block appears twice: once from each
lap. This is the doubled wall of L6's SLAM definition. On the right, the
same scans at the optimized poses give one wall.


Scoring a SLAM Run
------------------

L6 defined both scores. Here is why a SLAM run needs both.

- **APE (also called ATE)** checks the whole trajectory against the truth:
  "The global consistency can be evaluated by comparing the absolute
  distances between the estimated and the ground truth trajectory" (Sturm
  et al., 2012). The benchmark first aligns the two trajectories with one
  rigid motion. We did not align: our runs start at the true first pose.
- **RPE** checks motion over a fixed interval :math:`\Delta`: it "measures
  the local accuracy of the trajectory over a fixed time interval
  :math:`\Delta`. Therefore, the relative pose error corresponds to the
  drift of the trajectory" (Sturm et al., 2012).

This page reports APE. A loop closure moves whole stretches of the path at
once, and APE is the score that compares whole stretches with the truth.


LiDAR SLAM in Practice
----------------------

Real systems use the same parts as this page, with a 3-D LiDAR and an IMU.

- **LOAM** (Zhang and Singh, 2014): edge and plane features, a fast
  odometry and a slow mapping step, as above.
- **LIO-SAM** (Shan et al., 2020) puts everything in one factor graph, a
  pose graph whose edges can come from any sensor: "The four types of
  factors are: (a) IMU preintegration factors, (b) lidar odometry factors,
  (c) GPS factors, and (d) loop closure factors." The paper treats GPS as
  optional. "The factor graph is optimized upon the insertion of a new
  node using incremental smoothing and mapping with the Bayes tree
  (iSAM2)".
- **FAST-LIO2** (Xu et al., 2022) skips features: "directly registering raw
  points to the map (and subsequently update the map, i.e., mapping)
  without extracting features." It keeps the map in "an incremental k-d
  tree data structure, ikd-Tree, that enables incremental updates (i.e.,
  point insertion, delete) and dynamic re-balancing."


What to Remember
----------------

- SLAM estimates the path and the map together because their errors are
  correlated. A loop closure works through those correlations.
- **EKF-SLAM** keeps one Gaussian over everything. Each update touches every
  number, so its cost grows with the square of the map. On our 24-landmark
  world it ended 0.038 m from the truth; its cost per update grew 4.2 times
  when the state doubled from 403 to 803 numbers.
- **FastSLAM** keeps particles, each a path and small landmark EKFs. It
  needs enough particles (5 were not enough here), and resampling leaves one
  history of the old path in every one of our 9 runs.
- **Graph SLAM** keeps every keyframe. Gauss-Newton on a sparse :math:`H`
  (0.99% nonzero on our drive) solved 387 keyframes in 4 iterations.
- **The front end** decides the result: scan-to-submap odometry drifted
  1.07 m where scan to scan drifted 11.26 m, and the back end ended at
  0.24 m and 1.56 m from them.
- **Loop detection** needs two stages: Scan Context to propose (195
  candidates) and ICP to verify (163 kept, all right).


References
----------

- Biber, P. and Straßer, W. (2003). "The Normal Distributions Transform: A
  New Approach to Laser Scan Matching." *IEEE/RSJ International Conference
  on Intelligent Robots and Systems (IROS)*, vol. 3, 2743 to 2748.
  `doi:10.1109/IROS.2003.1249285 <https://doi.org/10.1109/IROS.2003.1249285>`__
- Durrant-Whyte, H. and Bailey, T. (2006). "Simultaneous Localization and
  Mapping: Part I." *IEEE Robotics & Automation Magazine*, 13(2), 99 to 110.
  `doi:10.1109/MRA.2006.1638022 <https://doi.org/10.1109/MRA.2006.1638022>`__
- Grisetti, G., Kümmerle, R., Stachniss, C. and Burgard, W. (2010). "A
  Tutorial on Graph-Based SLAM." *IEEE Intelligent Transportation Systems
  Magazine*, 2(4), 31 to 43.
  `doi:10.1109/MITS.2010.939925 <https://doi.org/10.1109/MITS.2010.939925>`__
- Grisetti, G., Stachniss, C. and Burgard, W. (2007). "Improved Techniques
  for Grid Mapping With Rao-Blackwellized Particle Filters." *IEEE
  Transactions on Robotics*, 23(1), 34 to 46.
  `doi:10.1109/TRO.2006.889486 <https://doi.org/10.1109/TRO.2006.889486>`__
- Kim, G. and Kim, A. (2018). "Scan Context: Egocentric Spatial Descriptor
  for Place Recognition within 3D Point Cloud Map." *IEEE/RSJ International
  Conference on Intelligent Robots and Systems (IROS)*, 4802 to 4809.
  `doi:10.1109/IROS.2018.8593953 <https://doi.org/10.1109/IROS.2018.8593953>`__
- Montemerlo, M., Thrun, S., Koller, D. and Wegbreit, B. (2002). "FastSLAM:
  A Factored Solution to the Simultaneous Localization and Mapping
  Problem." *AAAI-02 Proceedings*, 593 to 598.
  `PDF <https://cdn.aaai.org/AAAI/2002/AAAI02-089.pdf>`__
- Segal, A. V., Haehnel, D. and Thrun, S. (2009). "Generalized-ICP."
  *Robotics: Science and Systems V*.
  `doi:10.15607/RSS.2009.V.021 <https://doi.org/10.15607/RSS.2009.V.021>`__
- Shan, T., Englot, B., Meyers, D., Wang, W., Ratti, C. and Rus, D. (2020).
  "LIO-SAM: Tightly-coupled Lidar Inertial Odometry via Smoothing and
  Mapping." *IEEE/RSJ International Conference on Intelligent Robots and
  Systems (IROS)*, 5135 to 5142.
  `doi:10.1109/IROS45743.2020.9341176 <https://doi.org/10.1109/IROS45743.2020.9341176>`__
- Smith, R., Self, M. and Cheeseman, P. (1990). "Estimating Uncertain
  Spatial Relationships in Robotics." In *Autonomous Robot Vehicles*,
  Springer, 167 to 193.
  `doi:10.1007/978-1-4613-8997-2_14 <https://doi.org/10.1007/978-1-4613-8997-2_14>`__.
  Quoted from the authors' full-length version,
  `arXiv:1304.3111 <https://arxiv.org/abs/1304.3111>`__.
- Sturm, J., Engelhard, N., Endres, F., Burgard, W. and Cremers, D. (2012).
  "A Benchmark for the Evaluation of RGB-D SLAM Systems." *IEEE/RSJ
  International Conference on Intelligent Robots and Systems (IROS)*, 573
  to 580.
  `doi:10.1109/IROS.2012.6385773 <https://doi.org/10.1109/IROS.2012.6385773>`__
- Xu, W., Cai, Y., He, D., Lin, J. and Zhang, F. (2022). "FAST-LIO2: Fast
  Direct LiDAR-Inertial Odometry." *IEEE Transactions on Robotics*, 38(4),
  2053 to 2073.
  `doi:10.1109/TRO.2022.3141876 <https://doi.org/10.1109/TRO.2022.3141876>`__
- Zhang, J. and Singh, S. (2014). "LOAM: Lidar Odometry and Mapping in
  Real-time." *Robotics: Science and Systems X*.
  `doi:10.15607/RSS.2014.X.007 <https://doi.org/10.15607/RSS.2014.X.007>`__
- Zhang, J., Kaess, M. and Singh, S. (2016). Cited through
  :doc:`L6's references </lectures/lecture6/l6_references>`.
