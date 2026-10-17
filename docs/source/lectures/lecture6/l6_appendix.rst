====================================================
Going Further
====================================================

.. admonition:: Reading material, not covered in class
   :class: note

   This page is the written version of the deck's appendix. It is **reading
   material**: we do not present it in class, and it is **not on the quiz**.

   Each section picks up a topic from the :doc:`lecture <l6_lecture>` and
   works it out with more numbers or more steps. The sections follow the
   deck's order. Read the one you need, when you need it.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Section**
     - **What it adds to the lecture**
   * - :ref:`l6-app-bound`
     - Where the 0.29 m error bound comes from: the room in a turn, the
       heading's share, the failure rate and the 95% value.
   * - :ref:`l6-app-rtk`
     - Why RTK's leftover error can be centimeters (the carrier wave), and
       how to read NOAA's map of reference stations.
   * - :ref:`l6-app-icp-hand`
     - ICP step 2 on one small example, one step at a time, then the same
       turn found with the SVD, and when the turn is not unique.
   * - :ref:`l6-app-score`
     - Four ways to score how far the scan is off: point to point, point to
       line, GICP and NDT, with what each one measures and when it is
       better.
   * - :ref:`l6-app-ndt`
     - The formula for NDT's score of one pose.
   * - :ref:`l6-app-lf`
     - MCL's likelihood field, drawn around a corner.
   * - :ref:`l6-app-integrity`
     - How a filter checks its own updates (NIS), what that check misses,
       and how a protection level turns it into a warning.
   * - :ref:`l6-app-pg`
     - The three-pose graph of the SLAM section, written out as a weighted
       least-squares problem and solved step by step.
   * - :ref:`l6-app-ape`
     - Two ways to score a trajectory: the absolute error and the relative
       error.


.. _l6-app-bound:

The Error Bound
---------------

This section continues the slide "Step 1: how much room the lane leaves
the AV" in the Introduction of the lecture (:ref:`l6-lec-bound`). It shows
where Reid et al. (2019) get 0.29 m.


The 0.33 m in a Turn, and the Heading's Share
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Symbols: the lane center's radius :math:`r` and the lane width :math:`w`;
the AV's width :math:`w_v` and length :math:`l_v`; the box around the AV is
:math:`x` wide and :math:`y` long. Reid et al.'s equations (Reid et al.,
2019):

.. math::

   \Big(\frac{y}{2}\Big)^2 + \Big(r - \frac{w}{2} + x\Big)^2
   = \Big(r + \frac{w}{2}\Big)^2, \qquad
   \text{room: } \frac{x - w_v}{2} \text{ sideways}, \quad
   \frac{y - l_v}{2} \text{ along the road}

1. With :math:`r = 20` m, :math:`w = 3.0` m, :math:`w_v = 2.1` m and
   :math:`l_v = 5.8` m, we solve for equal room both ways: 0.328 m (box
   2.76 m by 6.46 m). The paper reads 0.33 m off its Figure 14.
2. The heading's share (the paper's equation 17, with the same angle error
   :math:`\delta` about every axis):
   :math:`\delta_{\mathrm{lat}} + (\delta_{\mathrm{lon}} + \delta_{\mathrm{vert}} + l_v/2)\,\delta \le 0.33`
   m. Here :math:`\delta_{\mathrm{lat}}`, :math:`\delta_{\mathrm{lon}}` and
   :math:`\delta_{\mathrm{vert}}` are the allowed position errors sideways,
   along the road and up. :math:`\delta` alone is the heading error in
   radians.
3. With :math:`\delta = 0.5^\circ = 0.00873` rad,
   :math:`\delta_{\mathrm{lon}} = 0.29` m and the paper's
   :math:`\delta_{\mathrm{vert}} = 1.40` m:
   :math:`(0.29 + 1.40 + 2.90) \times 0.00873 = 0.040` m.
4. :math:`\delta_{\mathrm{lat}} = 0.33 - 0.04 = 0.29` m.


Once in :math:`10^8` Hours, and the 95% Value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The rate** (Reid et al., 2019):

1. The target: road travel as safe as commercial aviation, a hundred times
   safer than today.
2. The paper splits that over the AV's systems and gives localization
   :math:`10^{-9}` failures per mile.
3. At 10 to 85 miles per hour, :math:`10^{-9}` per mile is :math:`10^{-8}`
   to :math:`8.5 \times 10^{-8}` per hour. The paper uses :math:`10^{-8}` per
   hour.

**The 95% value**, if the errors were Gaussian (the paper's assumption for
this step):

1. A Gaussian error stays within :math:`5.73\sigma` all but :math:`10^{-8}`
   of the time (both sides together), and within :math:`1.96\sigma` 95% of
   the time.
2. :math:`0.29 \times 1.96 / 5.73 = 0.099`, so 0.10 m.


.. _l6-app-rtk:

RTK
---

This section continues two slides in the GNSS and RTK section of the
lecture (:ref:`l6-lec-gnss`): "RTK, step 4: the AV subtracts the base's
error" and "RTK, step 1: a base station on a surveyed point".


Why RTK Reaches Centimeters: the Carrier Wave
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The four RTK steps in the GNSS and RTK section subtract the base's error
from the AV's. How small the leftover gets depends on what the receivers
measure.

- A plain receiver times the **code** the satellite sends.
- RTK also measures the **carrier**, the radio wave itself (GMV, 2011). The
  carrier's wavelength is short, so the leftover error can be centimeters.

.. important::

   "RTK, which achieves performances in the range of a few centimetres, is a
   technique commonly used in surveying applications" (GMV, 2011).


.. _l6-app-cors:

Reading NOAA's CORS Map
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/noaa_cors_legend.png
   :alt: A screenshot of the legend of NOAA's CORS map, titled NOAA CORS Network (sm scale). Sixteen marker types in four colors: blue for 1 sec, green for 5 sec, orange for 15 sec and red for 30 sec. In each color, a round pin for GPS and a square pin for GNSS, each filled, and hollow versions labeled Non-operational, some listed as, for example, 5 sec GPS 1 sec GNSS Non-operational.
   :width: 50%
   :align: center

   The legend of NOAA's CORS map: color gives the sampling rate, the pin's
   shape gives GPS or GNSS, and a hollow pin means "Non-operational".

Each marker on NOAA's map is one **CORS** (Continuously Operating Reference
Station): a GNSS receiver on a surveyed point, like the base station of RTK
step 1. NOAA collects their measurements and shares them free. After
processing, positions "can approach a few centimeters" (NOAA NGS, CORS
Network item).

- **1, 5, 15 or 30 sec** (the color): the sampling rate, how often the
  station records. It "is valid for 30 days. After that the data are
  decimated to 30 seconds" (NOAA NGS, All NGS CORS Sites).
- **GPS** (round pin): the station tracks the U.S. GPS satellites only.
  **GNSS** (square pin): it also tracks other constellations.
- **Filled**: the station is running. **Hollow**, "Non-operational": it is
  not running now.

**Not live:** "most data are available within 1 hour" of recording (NOAA
NGS, NCN Data and Products). An AV gets live corrections from a real-time
network (RTK, step 1).


.. _l6-app-icp-hand:

ICP by SVD
----------

This section continues the slide "ICP step 2 in general: six steps" of the
lecture (:ref:`l6-lec-icp`). Step 2 of ICP takes the :math:`n` pairs
:math:`(p_i, q_i)` of step 1 and finds the turn :math:`R` and the shift
:math:`t` that best put the scan points on their map points. Here are its
six steps on one small example, then steps 4 and 5 done another way, with
the SVD.


ICP Step 2: Centroids
~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/icp_step2_centroids.png
   :alt: Three pairs joined by dotted lines: orange dots p1 at 1, 0, p2 at 0, 2 and p3 at minus 1, minus 2; green circles q1 at 2, 2, q2 at 0, 1 and q3 at 4, 0. An orange cross at 0, 0 with tag 1 and a green cross at 2, 1 with tag 2.
   :width: 60%
   :align: center

   The three pairs, joined by dotted lines: scan points :math:`p_i`
   (orange dots) and map points :math:`q_i` (green circles). **1:** the scan
   centroid. **2:** the map centroid.

Three pairs (chosen), matched by step 1: :math:`p_1 = (1, 0) \to q_1 = (2, 2)`,
:math:`p_2 = (0, 2) \to q_2 = (0, 1)` and
:math:`p_3 = (-1, -2) \to q_3 = (4, 0)`. We made them fit exactly: one turn
and one shift put every :math:`p_i` on its :math:`q_i`.

**Purpose:** find the middle of each set.

**Output:** the centroids :math:`\bar p = \frac{1}{n}\sum_i p_i` and
:math:`\bar q = \frac{1}{n}\sum_i q_i`.

**Example** (:math:`n = 3`):

1. :math:`\bar p = \big((1 + 0 - 1)/3,\ (0 + 2 - 2)/3\big) = (0, 0)`, tag **1**.
2. :math:`\bar q = \big((2 + 0 + 4)/3,\ (2 + 1 + 0)/3\big) = (2, 1)`, tag **2**.


ICP Step 2: Center
~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/icp_step2_center.png
   :alt: The three pairs after centering, joined by dotted lines: p1 prime at 1, 0, p2 prime at 0, 2 and p3 prime at minus 1, minus 2; q1 prime at 0, 1, q2 prime at minus 2, 0 and q3 prime at 2, minus 1. Both centroid crosses at 0, 0, tag 3.
   :width: 60%
   :align: center

   The pairs after centering. **3:** both centroids now sit at the origin.

**Purpose:** remove the shift, so only a turn is left.

**Output:** the centered points :math:`p_i' = p_i - \bar p` and
:math:`q_i' = q_i - \bar q`.

**Example:**

1. :math:`p_i' = p_i - (0, 0) = p_i`.
2. :math:`q_1' = (2, 2) - (2, 1) = (0, 1)`;
   :math:`q_2' = (0, 1) - (2, 1) = (-2, 0)`;
   :math:`q_3' = (4, 0) - (2, 1) = (2, -1)`.
3. Both centroids now sit at the origin, tag **3**.

**Why the shift is gone:** :math:`q_i = R\,p_i + t` for every pair, so
:math:`q_i - \bar q = R\,(p_i - \bar p)`, and :math:`t` cancels.


ICP Step 2: Compare
~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: cross-covariance of the pairs, H
   :class: note

   :math:`H = \sum_i p_i'\, q_i'^{\top}`, a :math:`2 \times 2` matrix. Entry
   :math:`H_{ab}` adds, over the pairs, coordinate :math:`a` of
   :math:`p_i'` times coordinate :math:`b` of :math:`q_i'` (1 is :math:`x`,
   2 is :math:`y`).

.. figure:: /_static/images/L6/icp_step2_compare.png
   :alt: The centered points as arrows from the origin: orange p1 prime to 1, 0, p2 prime to 0, 2, p3 prime to minus 1, minus 2; green q1 prime to 0, 1, q2 prime to minus 2, 0, q3 prime to 2, minus 1.
   :width: 50%
   :align: center

   The centered points as arrows from the origin: :math:`p_i'` in orange,
   :math:`q_i'` in green.

**Purpose:** add up, over all pairs, how each :math:`p_i'` lines up with its
:math:`q_i'`.

**Output:** :math:`H`.

**Example**, from :math:`p'`: :math:`(1, 0), (0, 2), (-1, -2)` and
:math:`q'`: :math:`(0, 1), (-2, 0), (2, -1)`:

.. math::

   H_{11} &= 1 \cdot 0 + 0 \cdot (-2) + (-1) \cdot 2 = -2 \\
   H_{12} &= 1 \cdot 1 + 0 \cdot 0 + (-1)(-1) = 2 \\
   H_{21} &= 0 \cdot 0 + 2 \cdot (-2) + (-2) \cdot 2 = -8 \\
   H_{22} &= 0 \cdot 1 + 2 \cdot 0 + (-2)(-1) = 2

.. math::

   H = \begin{pmatrix} -2 & 2 \\ -8 & 2 \end{pmatrix}


ICP Step 2: Angle
~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/icp_step2_angle.png
   :alt: The same arrows as the last figure, with a dashed quarter-circle arc from each orange p prime arrow counterclockwise to its green q prime arrow, one arc labeled 90 degrees.
   :width: 50%
   :align: center

   The same arrows. Each dashed arc goes counterclockwise from a
   :math:`p_i'` to its :math:`q_i'`: a quarter turn, 90°.

**Purpose:** find the turn angle :math:`\alpha` that lines the pairs up best.

**Output:** :math:`\alpha = \operatorname{atan2}(H_{12} - H_{21},\ H_{11} + H_{22})`.

**Why:** the formula uses two sums of :math:`H`.

- :math:`H_{11} + H_{22} = \sum_i p_i' \cdot q_i'`, the dot products: do the
  :math:`q_i'` point the same way as their :math:`p_i'`?
- :math:`H_{12} - H_{21} = \sum_i (p'_x q'_y - p'_y q'_x)`, the cross
  products: are the :math:`q_i'` turned left of their :math:`p_i'`?

If each :math:`q_i'` is :math:`p_i'` turned by :math:`\alpha`, the two sums
are :math:`\cos\alpha` and :math:`\sin\alpha` times
:math:`\sum_i |p_i'|^2 = 1 + 4 + 5 = 10`.

**Example:** :math:`-2 + 2 = 0` and :math:`2 - (-8) = 10`, so
:math:`\cos\alpha = 0/10 = 0` and :math:`\sin\alpha = 10/10 = 1`. So
:math:`\alpha = \operatorname{atan2}(10, 0) = 90^\circ`, a quarter turn
left.


ICP Step 2: Turn
~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/icp_step2_turn.png
   :alt: Faint orange circles at the centered scan points 1, 0, 0, 2 and minus 1, minus 2, each with a curved grey arrow to an orange dot inside a green circle: R p1 prime equals q1 prime at 0, 1; R p2 prime equals q2 prime at minus 2, 0; R p3 prime equals q3 prime at 2, minus 1.
   :width: 55%
   :align: center

   Each centered scan point (faint circle) turned by :math:`R` lands on its
   centered map point: :math:`R\,p_i' = q_i'`.

**Purpose:** build the rotation matrix of :math:`\alpha`, to turn points
with.

**Output:**
:math:`R = \begin{pmatrix} \cos\alpha & -\sin\alpha \\ \sin\alpha & \cos\alpha \end{pmatrix}`.

**Example:** :math:`\cos 90^\circ = 0` and :math:`\sin 90^\circ = 1`, so
:math:`R = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}`.

**Check** each pair:

1. :math:`R\,p_1' = (0 \cdot 1 - 1 \cdot 0,\ 1 \cdot 1 + 0 \cdot 0) = (0, 1) = q_1'`.
2. :math:`R\,p_2' = (-2, 0) = q_2'`, and :math:`R\,p_3' = (2, -1) = q_3'`.
3. :math:`\det R = 0 \cdot 0 - (-1) \cdot 1 = 1`: a turn, not a mirror.


ICP Step 2: Shift
~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/icp_worked_after.png
   :alt: Titled After: R P plus t lands on Q. The three moved scan points, R p plus t, drawn as orange dots, each sitting inside its green map circle q1 at 2, 2, q2 at 0, 1 and q3 at 4, 0.
   :width: 55%
   :align: center

   After the turn and the shift, each moved scan point
   :math:`R\,p_i + t` (orange dot) sits inside its map point :math:`q_i`
   (green circle).

**Purpose:** put the turned scan on the map: move the turned scan centroid
onto the map centroid.

**Output:** :math:`t = \bar q - R\,\bar p`.

**Example:** :math:`R\,\bar p = R\,(0, 0) = (0, 0)`, so
:math:`t = (2, 1) - (0, 0) = (2, 1)`.

**Check** each pair, :math:`R\,p_i + t`:

1. :math:`(0, 1) + (2, 1) = (2, 2) = q_1`.
2. :math:`(-2, 0) + (2, 1) = (0, 1) = q_2`.
3. :math:`(2, -1) + (2, 1) = (4, 0) = q_3`.

Step 2's answer: turn 90° left, then shift by :math:`(2, 1)`.


The SVD: Any Matrix Is a Turn, a Stretch, a Turn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In 3-D, steps 4 and 5 become one: the SVD of :math:`H`.

.. admonition:: Definition: singular value decomposition (SVD)
   :class: note

   Any real matrix :math:`H` can be written :math:`H = U S V^{\top}`.
   :math:`U` and :math:`V` keep lengths: each turns, or turns and mirrors.
   :math:`S` is diagonal, with entries :math:`s_1 \ge s_2 \ge 0`, the
   singular values: it stretches along the axes.

.. figure:: /_static/images/L6/svd_intuition.png
   :alt: Four panels with a light grey curve and two arrows from the origin, one black and one grey. Panel 1, axes from minus 1 to 1: a circle; the black arrow points right and slightly down, the grey arrow down and slightly left. Panel 2: the same circle; the black arrow lies along the x axis, the grey arrow along the y axis. Panel 3, axes from minus 8 to 8: a flat ellipse along x; the black arrow about 8.6 long along x, the grey arrow about 1.4 long along y. Panel 4: the same ellipse tilted steeply; the black arrow points down and slightly left, about 8.6 long; the grey arrow short.
   :width: 100%
   :align: center

   Our :math:`H`. **1:** a circle and :math:`V`'s two columns. **2:** after
   :math:`V^{\top}`: turned and mirrored onto the axes. **3:** after
   :math:`S`: stretched by :math:`s_1 = 8.606` and :math:`s_2 = 1.394`.
   **4:** after :math:`U`: turned and mirrored again. Going from 1 to 4 is
   :math:`H` applied to the circle.

So the SVD splits a matrix into its turns and its stretch. ICP needs only
the turn in :math:`H`: the next part does steps 4 and 5 in one.


ICP Step 2: Angle and Turn by the SVD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Why it works.** In our pairs each :math:`q_i'` is :math:`p_i'` turned by
:math:`R`, so

.. math::

   H = \sum_i p_i'\, q_i'^{\top} = \sum_i p_i'\,(R\,p_i')^{\top}
     = \underbrace{\Big(\sum_i p_i'\, p_i'^{\top}\Big)}_{\text{spread of the scan}}\, R^{\top}

The spread is :math:`\begin{pmatrix} 2 & 2 \\ 2 & 8 \end{pmatrix}`. Times
:math:`R^{\top}`, it gives
:math:`H = \begin{pmatrix} -2 & 2 \\ -8 & 2 \end{pmatrix}`. So :math:`H` is a
spread times a turn, and the SVD separates the two.

1. **SVD of H** (the computer does it): :math:`S = \operatorname{diag}(8.606, 1.394)`,
   the spread's two values. :math:`U` and :math:`V` hold the turns (the
   numbers are in the next part). Drop :math:`S`: it says how the points
   are spread, not how the scan is turned.
2. **Keep the turns.** The spread is symmetric, so its SVD is
   :math:`W S W^{\top}`, and :math:`H = W S\,(R W)^{\top}`. So
   :math:`U = W`, :math:`V = R W`, and
   :math:`R = V U^{\top} = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}`, a
   quarter turn left, 90°.
3. **Check:** :math:`R\,p_1' = (0, 1) = q_1'`, and
   :math:`\det(V U^{\top}) = +1`: a turn, not a mirror. The next part shows
   how a :math:`-1` is fixed.

With noisy pairs, the same steps give the turn that lines the pairs up best
(Kabsch, 1976).


.. _l6-app-icp-svd:

ICP Step 2: Angle and Turn by the SVD, the Numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The best rotation, in 2-D or 3-D (Kabsch, 1976): write the SVD
:math:`H = U S V^{\top}`, then

.. math::

   R = V \begin{pmatrix} 1 & 0 \\ 0 & d \end{pmatrix} U^{\top},
   \qquad d = \det(V U^{\top})

:math:`d = -1` means the best fit is a mirror image. Putting :math:`d` in the
middle matrix turns it back into a rotation.

**Our three pairs.** The course code computed the SVD (rounded here).
:math:`V^{\top}` is symmetric here, so :math:`V` is the same matrix:

.. math::

   U = \begin{pmatrix} -0.290 & -0.957 \\ -0.957 & 0.290 \end{pmatrix},\quad
   S = \begin{pmatrix} 8.606 & 0 \\ 0 & 1.394 \end{pmatrix},\quad
   V^{\top} = \begin{pmatrix} 0.957 & -0.290 \\ -0.290 & -0.957 \end{pmatrix}

1. :math:`\det(V U^{\top}) = +1`: no mirror, so :math:`d = 1`.
2. So :math:`R = V U^{\top}`. The top right entry:
   :math:`0.957 \times (-0.957) + (-0.290) \times 0.290 = -1.000`. All four
   entries give :math:`\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}`, the
   90° of the Angle step.


.. _l6-app-icp-degenerate:

When the Rotation Is Not Unique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the pairs fixed, the 2-D rotation
:math:`\alpha = \operatorname{atan2}(H_{12} - H_{21},\ H_{11} + H_{22})` is
**not unique only when both arguments are 0**. A second singular value of 0
alone is not enough: :math:`H = \begin{pmatrix} 0 & 2 \\ 0 & 0 \end{pmatrix}`
has :math:`S = (2, 0)` and still gives one rotation, 90°.

- **All points on one line** (a single straight wall): for fixed pairs, the
  rotation can still be found. The trouble is the pairing. Shifted along the
  wall, each scan point finds an equally near map point, so ICP cannot tell
  how far along the wall the AV is. The course code stops with an error when
  the second singular value is near 0, to be safe.
- The example solved by hand at the start of this section uses three
  centered points that are not on one line, so nothing in it depends on
  this case.

.. admonition:: On the road
   :class: important

   A long tunnel or a straight wall with no features leaves the position
   **along** it unknown. ICP's fit looks perfect, and is not. That is another
   reason to check it against a second source.


.. _l6-app-score:

Which Way to Score
------------------

This section continues the slide "Four ways to score how far the scan is
off" in the Against a Map section of the lecture (:ref:`l6-lec-icp`): which
way to score, and when.


Point to Point and Point to Line: What Each One Measures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 2 makes the error :math:`E = \sum_i e_i^2` small. The two ways differ
in what :math:`e_i` is. The map only **samples** a surface. Here the surface
is a straight wall (a building front), with one map point every 1 m
(chosen).

.. figure:: /_static/images/L6/icp_p2p_p2l.png
   :alt: Two panels, titled point to point and point to line, each with a green dashed horizontal line, the wall, green squares on it every 1 m from 0 to 6, and three rust dots above it at x 1.45, 3.3 and 4.55. Left: black lines from each rust dot to its nearest green square, labeled 0.75, 0.54 and 0.83. Right: black vertical lines from each rust dot down to the dashed line, labeled 0.60, 0.45 and 0.70, and small green arrows pointing up from the squares at x 1, 3 and 5.
   :width: 95%
   :align: center

   Squares: map points. Dashed line: the wall. Dots: scan points. Arrows:
   the wall's normal :math:`n`, perpendicular to it. **Left:** point to
   point. **Right:** point to line.

- **Point to point** (our ICP), left: the error is the distance to the
  nearest map point, 0.75, 0.54 and 0.83 m. It includes the gap along the
  wall to the nearest sample (0.45, 0.30 and 0.45 m). That gap comes from
  where the samples sit, yet it pulls the scan along the wall.
- **Point to line** (point to plane in 3-D), right: the error is the
  distance along :math:`n` only, 0.60, 0.45 and 0.70 m. Moving a scan point
  along the wall leaves this distance the same, so the gap along the wall
  costs nothing (Chen and Medioni, 1991).


Point to Point or Point to Line: the Start Decides
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/score_start_sweep.png
   :alt: A line plot. Across: how far the start is off, 0 to 5 m, the heading off 6.4 degrees per m. Up: the error where ICP ends, 0 to 7 m. Point to point, a solid black line with circles: about 0.4 m from 0.6 to 4.7 m, then 1.24 m at 5 m. Point to line, a dashed grey line with squares: 0 up to 1.56 m, then about 6.5 m from 1.88 to 4.06 m, then about 1 m.
   :width: 75%
   :align: center

   Across: how far the start is off, in meters (the heading is off 6.4° per
   meter). Up: the error where ICP ends. Solid black: point to point.
   Dashed grey: point to line.

**Measured** on the registration example's street: a building front with two
recesses set back 1.2 m, poles and a corner. Every run uses the same scan.
The start is the example's offset (1.25 m, 8°) times 0.25 to 4.

- **Close start**, up to 1.56 m and 10°: point to line ends exact. Point to
  point stops 0.22 to 0.41 m short, along the street.
- **Far start**, 1.88 to 4.06 m: point to line slides 6.5 m along the front,
  and puts its second recess onto the first. Point to point still ends
  0.41 m off, for starts up to 4.69 m.
- **5 m, 32°**: both fail.

**So:** use point to line when the start is close, and point to point when
it may be far. Point to line is "less robust to very large initial
displacement errors" (Censi, 2008).


GICP: When Both Point Sets Are Only Samples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/gicp_two_scans.png
   :alt: A corner of two walls, along x and along y. Green squares, the map points, every 1 m, each with a flat green ellipse along its wall. Rust dots, the scan points, sampled halfway between the map points and drawn at a guess 0.4 m off in x and y, each with a flat rust ellipse along its wall. Thin black lines join each scan point to its nearest map point.
   :width: 50%
   :align: center

   A corner of two walls. Green squares: map points, every 1 m. Rust dots:
   scan points, sampled halfway between the map points and drawn at a guess
   0.4 m off in :math:`x` and :math:`y`. Each point has a flat ellipse along
   its wall. Black lines: the pairs.

**What it measures.** Point to line uses the surface shape around the map
point only. GICP, generalized ICP, models "locally planar surface structure
from both scans" (Segal et al., 2009). Every point, map and scan, gets a
flat ellipse along its surface, and a gap along both surfaces costs little.

**Better when:**

- both sets are samples, as in scan to scan matching: their points never
  sit on each other (here they are 0.5 m apart along the walls);
- many pairs are wrong: GICP is "more robust to incorrect correspondences,
  and thus makes it easier to tune the maximum match distance parameter"
  (Segal et al., 2009). In our code that parameter is the 3 m gate.

In the paper's tests, GICP outperforms "both standard ICP and
point-to-plane".

**Cost:** a surface fit at every point of both sets. Our code has no GICP,
so nothing is measured here.


.. _l6-app-score-ndt:

NDT: How It Scores a Pose
~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/ndt_cells.png
   :alt: The 20 by 10 meter box with its pillar, drawn as grey dots with a little noise, under a grid of 2.5 meter cells. In every cell with points, a green ellipse: long and thin along each wall, rounder in the corner cells and in the pillar's cell.
   :width: 80%
   :align: center

   MCL's room, 20 m by 10 m with its pillar, under a grid of 2.5 m cells.
   Each cell's points get one green ellipse: long and thin along a wall,
   rounder in the corners and at the pillar.

**NDT**, the normal distributions transform (Biber and Strasser, 2003),
replaces the map's points with one ellipse per cell:

1. Cut the map into square cells (here MCL's room, with 2.5 m cells,
   chosen).
2. In each cell, fit a mean and a covariance to its points. That gives one
   ellipse, the shape of the points there.
3. Place the scan at a pose. Each scan point scores by how likely it is
   under its cell's ellipse. Move the pose to raise the total.

**What it measures:** NDT has no nearest-point pairs, so no pair jumps to
another map point when the pose moves. The score is "piecewise continuous
and differentiable" (Biber and Strasser, 2003). The formula is in
:ref:`l6-app-ndt`.


NDT on Our Map: Cells Instead of Points
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/ndt_our_map.png
   :alt: A 30 by 20 meter crop of our CARLA map, grey map points under a grid of 2.5 meter cells. Each cell with 5 or more points has a green outlined ellipse: thin lines along the straight walls, small ellipses on poles and short walls, and round ellipses over the dense curved bands at the right.
   :width: 70%
   :align: center

   A 30 m by 20 m crop of our CARLA map under 2.5 m cells. Each cell with 5
   or more points gets a green ellipse: thin along the straight walls,
   small on poles and short walls, round over the dense curved bands at the
   right.

**Measured** on our whole map, with 2.5 m cells (chosen):

- 18,661 points fall in 1,277 cells. 997 cells hold 5 or more points and
  get an ellipse (our rule, chosen).
- Stored: :math:`997 \times 5 = 4{,}985` numbers (a mean is 2 numbers, a
  covariance 3) instead of :math:`18{,}661 \times 2 = 37{,}322`.
- No nearest-point search: a scan point's cell is its coordinates divided
  by 2.5 m, rounded down.

**Better when the map is big:** 3-D NDT was "faster and slightly more
reliable than the standard ICP algorithm", with "a more memory-efficient
scan surface representation" (Magnusson et al., 2007).

**Cost:** the cell size is a choice, and the 674 points in cells with fewer
than 5 points are left out.


.. _l6-app-ndt:

NDT
---

This section continues :ref:`l6-app-score-ndt` above.


NDT's Score for One Pose
~~~~~~~~~~~~~~~~~~~~~~~~

For each cell :math:`c` with map points, NDT keeps the mean
:math:`\boldsymbol{\mu}_c` and the covariance :math:`\Sigma_c` of those
points (Biber and Strasser, 2003). Place the scan at a pose. Each scan point
:math:`\mathbf{s}` falls in some cell :math:`c`, and

.. math::

   \text{score} = \sum_{\mathbf{s}} \exp\!\Big(-\tfrac{1}{2}\,
   (\mathbf{s} - \boldsymbol{\mu}_c)^\top\,\Sigma_c^{-1}\,
   (\mathbf{s} - \boldsymbol{\mu}_c)\Big)

- The term in the exponent is the squared Mahalanobis distance, a distance
  counted in units of the spread. It is small along a wall's long axis and
  large across it.
- NDT improves the pose by moving it uphill on the score, step by step,
  from a starting guess. As for ICP, that guess is the filter's pose.


.. _l6-app-lf:

The Likelihood Field
--------------------

This section continues the slide "Weigh: why these values" in the Monte
Carlo Localization part of the lecture (:ref:`l6-lec-mcl`).


The Likelihood Field, Drawn Around a Corner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/likelihood_field.png
   :alt: A heat map over a corner of two walls, one along x from 0 to 8 meters and one along y from 0 to 5 meters, drawn as dots. The color is darkest green on the walls and fades to pale green about 2 to 3 meters away. A color bar is labeled how likely a scan point is here.
   :width: 75%
   :align: center

   The score :math:`p(d)` at every place around two walls (chosen): darkest
   on the walls, fading over about 2 to 3 m. The color bar reads "how likely
   a scan point is here".

This is the :math:`p(d)` of the lecture's slide "Weigh: the score's
formula", :math:`p(d) = 0.9\, e^{-d^2/2} + 0.1/3` with our values, drawn at
every place around two walls (chosen). It is highest on the walls and fades
over about 2 to 3 m. A scan point that lands in the dark band scores well.


.. _l6-app-integrity:

Integrity
---------

This section continues the slide "A match is a measurement: predict,
register, check, fuse" in the Against a Map section of the lecture
(:ref:`l6-lec-map`).


Integrity: Checking the Pose Without Knowing the Truth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A localizer must also know when its pose cannot be trusted, and say so. The
parts below show how a filter checks its own updates on our drive (NIS),
what the check can miss, and how a protection level turns that into a
warning.

.. admonition:: Definition: integrity
   :class: note

   "A measure of trust that can be placed in the correctness of the
   information supplied by a navigation system", including "the ability of
   the system to provide timely warnings to users when the system should not
   be used" (Zhu et al., 2018).


The Filter's NIS Over the Drive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L6/integrity_nis.png
   :alt: NIS on a log scale against time, 0 to 125 seconds, blue dots for GNSS fixes and green dots for map poses. Almost all dots lie between 0.1 and 10. Two dashed lines: green at 11.34 for the map pose, blue at 9.21 for GNSS. One blue dot near 105 seconds lies above 9.21; no green dot lies above 11.34 (the one rejected pose is not plotted).
   :width: 90%
   :align: center

   NIS on a log scale against time. Blue: GNSS fixes (2 numbers each).
   Green: map poses (3 numbers each). Dashed lines: the gates, 9.21 for
   GNSS and 11.34 for a map pose.

**NIS** (normalized innovation squared) is the surprise
:math:`\boldsymbol{\nu}` of an update (the innovation), squared and divided
by the spread :math:`S` the filter predicted for it:
:math:`\varepsilon = \boldsymbol{\nu}^{\top} S^{-1} \boldsymbol{\nu}`. The run
is the one with the outage, the wheels and the map.

- **Expected**, if the filter's :math:`S` is right: the average NIS equals
  the number of values, 2 for a fix and 3 for a pose.
- **Measured:** GNSS averages 2.12 over 68 fixes. One fix, at 105 s, is
  above 9.21. Our run does not gate GNSS, so the filter used it.
- **Measured:** the map averages 2.50 over the 118 accepted poses. One more
  pose, at 123 s, scored above 11.34 and was rejected.


What the NIS Averages Say, and What They Miss
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. If the filter is honest, the NIS of a reading with :math:`k` values
   follows the **chi-square distribution**: mean :math:`k`, spread
   :math:`\sqrt{2k}`. An average of :math:`n` values moves by about
   :math:`\sqrt{2k/n}` by chance.
2. GNSS: :math:`\sqrt{2 \times 2/68} = 0.24`. The average 2.12 is half of
   that above 2, so it fits.
3. Map: :math:`\sqrt{2 \times 3/118} = 0.23`. The average 2.50 is 2.2 of
   those below 3 (1.75 once the gate's cut of the top 1% is counted). So the
   filter expects map poses to miss a little more than they do.
4. An average is not proof. In this same run, the worst error in the outage
   is 1.06 m, 4.8 times the filter's :math:`\sigma` of 0.22 m (see
   :ref:`l6-lec-ekf`). NIS compares each update with the filter's own
   prediction. It never sees the truth.


The NIS Gate Makes Two Kinds of Mistake
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The NIS test rejects an update when :math:`\varepsilon` is too large for the
number of values it reports. The bound is set so that an honest update
passes 99 times in 100: **9.21** for a GNSS fix (:math:`x`, :math:`y`) and
**11.34** for a matched pose (:math:`x`, :math:`y`, :math:`\theta`). Both come
from the chi-square distribution (how NIS spreads when the filter is
honest). Our run gates only map poses.

- **False alarm:** a good update is rejected. At 0.99, 1 good update in 100
  scores above the bound by chance alone, and the filter drops it. The cost:
  the filter coasts on dead reckoning a little longer.
- **Missed fault:** a bad update is accepted. Say a multipath fix 3 m off
  (chosen) arrives while :math:`P` is large, after the outage. Then
  :math:`S` is large, so :math:`\varepsilon` stays small, and the filter
  moves most of the 3 m the wrong way.


.. _l6-app-integrity-pl:

Say When the Error Could Be Too Large: the Protection Level
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Alert limit:** "the largest position error allowable for safe
  operation" (Zhu et al., 2018). For a passenger car on a local street, it
  is Reid's 0.29 m (Reid et al., 2019).
- **Protection level:** "a statistical error bound computed so as to
  guarantee that the probability of the absolute position error exceeding
  the said number is smaller than or equal to the target integrity risk"
  (Zhu et al., 2018). In plain words: a radius the error stays inside,
  except with a tiny probability chosen in advance.
- **The rule:** if the protection level is above the alert limit, warn. The
  pose cannot be used for lane-level driving now.

.. admonition:: Two independent sources
   :class: important

   GNSS and map matching fail for different reasons (the sky, the map). If
   they agree, both are likely right. If they disagree, the AV knows that
   one is wrong. Lecture 13 (System Integration) covers keeping the AV safe
   when one fails.


.. _l6-app-pg:

Pose-Graph Least Squares
------------------------

This section continues the slide "The unsure edges take most of the
correction" in the SLAM section of the lecture (:ref:`l6-lec-slam`): the
three-pose graph whose loop closure left a gap of :math:`(0.1, 0.7)` m,
0.71 m long.


The Three-Pose Graph, Written Out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The unknowns are :math:`p_2` and :math:`p_3`; :math:`p_1 = (0, 0)` is fixed.
Each edge says "this difference should equal what I measured". The solver
minimizes the squared misses, each divided by its edge's variance (Grisetti
et al., 2010):

.. math::

   \frac{\|p_2 - p_1 - z_{12}\|^2}{0.5^2}
   + \frac{\|p_3 - p_2 - z_{23}\|^2}{0.3^2}
   + \frac{\|p_1 - p_3 - z_{31}\|^2}{0.1^2}

:math:`z_{12}`, :math:`z_{23}` and :math:`z_{31}` are the measured motions of
the lecture's slide: :math:`(10.3, 0.4)`, :math:`(-5.2, 8.3)` and
:math:`(-5.0, -8.0)`. The poses hold positions only, so :math:`x` and
:math:`y` are two separate problems. For :math:`x`, the gap is 0.1 m:

1. Total variance around the loop: :math:`0.25 + 0.09 + 0.01 = 0.35`.
2. The edge :math:`p_1` to :math:`p_2` gives up
   :math:`0.1 \times 0.25/0.35 = 0.071` m. The edge :math:`p_2` to
   :math:`p_3` gives up :math:`0.1 \times 0.09/0.35 = 0.026` m. The loop
   gives up :math:`0.1 \times 0.01/0.35 = 0.003` m.
3. :math:`p_{2,x} = 10.3 - 0.071 = 10.229`, and
   :math:`p_{3,x} = 10.229 - 5.2 - 0.026 = 5.003`.
4. Check: :math:`p_1 - p_3 = -5.003`, which misses
   :math:`z_{31,x} = -5.0` by the loop's 0.003.

For :math:`y`, the same steps with the gap 0.7 give
:math:`p_{2,y} = 0.4 - 0.5 = -0.100` and
:math:`p_{3,y} = -0.100 + 8.3 - 0.18 = 8.020`.


.. _l6-app-ape:

APE and RPE
-----------

This section continues the slide "One number for a whole run: the
absolute pose error" in the Fusion in the EKF section of the lecture
(:ref:`l6-lec-ekf`), where APE scored each run.


Two Ways to Score a Trajectory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Absolute error** (APE, also called ATE, the absolute trajectory error):
  "the global consistency can be evaluated by comparing the absolute
  distances between the estimated and the ground truth trajectory" (Sturm
  et al., 2012). The lecture's APE is its position part, summarized by the
  RMSE.
- **Relative error** (RPE): it "measures the local accuracy of the
  trajectory over a fixed time interval :math:`\Delta`. Therefore, the
  relative pose error corresponds to the drift of the trajectory" (Sturm et
  al., 2012).
- **Why both:** "since VO/VIO [visual and visual-inertial odometry] systems
  do not have a global reference (global position and yaw), the estimation
  quality can be evaluated by measuring the relative relations between the
  states at different times" (Zhang and Scaramuzza, 2018).

.. admonition:: Which score fits which system
   :class: important

   A GNSS-aided filter has a global reference, so APE is the fair score.
   Dead reckoning and odometry alone have none: nothing pulls their error
   back (our dead reckoning: 2.69 m after 100 m, 9.03 m at worst), and RPE
   says how fast they drift.


Sources for This Page
---------------------

The full reading list for the lecture is in :doc:`l6_references`. This page
cites:

- Reid, T. G. R., Houts, S. E., Cammarata, R., Mills, G., Agarwal, S.,
  Vora, A. and Pandey, G. (2019). "Localization Requirements for Autonomous
  Vehicles." *SAE International Journal of Connected and Automated
  Vehicles*, 2(3), 173 to 190.
- GMV (2011). `Real Time Kinematics
  <https://gssc.esa.int/navipedia/index.php/Real_Time_Kinematics>`_.
  European Space Agency, Navipedia.
- NOAA National Geodetic Survey. `NOAA Continuously Operating Reference
  Stations (CORS) Network (ArcGIS item)
  <https://noaa.maps.arcgis.com/home/item.html?id=99dc0ccc01f6449aa41a84fc57fe4171>`_.
  Accessed 2026-10-15.
- NOAA National Geodetic Survey. `All NGS CORS Sites
  <https://geodesy.noaa.gov/CORS/sort_sites.shtml>`_. Accessed 2026-10-15.
- NOAA National Geodetic Survey. `NCN Data and Products
  <https://www.ngs.noaa.gov/CORS/data.shtml>`_. Accessed 2026-10-15.
- Kabsch, W. (1976). "A Solution for the Best Rotation to Relate Two Sets of
  Vectors." *Acta Crystallographica Section A*, 32(5), 922 to 923.
- Chen, Y. and Medioni, G. (1991). "Object Modeling by Registration of
  Multiple Range Images." ICRA, 2724 to 2729.
- Censi, A. (2008). "An ICP Variant Using a Point-to-Line Metric." ICRA,
  19 to 25.
- Segal, A., Haehnel, D. and Thrun, S. (2009). "Generalized-ICP." Robotics:
  Science and Systems V.
- Biber, P. and Strasser, W. (2003). "The Normal Distributions Transform: A
  New Approach to Laser Scan Matching." IROS, 2743 to 2748.
- Magnusson, M., Lilienthal, A. J. and Duckett, T. (2007). "Scan
  Registration for Autonomous Mining Vehicles Using 3D-NDT." *Journal of
  Field Robotics*, 24(10), 803 to 827.
- Zhu, N., Marais, J., Bétaille, D. and Berbineau, M. (2018). "GNSS Position
  Integrity in Urban Environments: A Review of Literature." *IEEE
  Transactions on Intelligent Transportation Systems*, 19(9), 2762 to 2778.
- Grisetti, G., Kümmerle, R., Stachniss, C. and Burgard, W. (2010). "A
  Tutorial on Graph-Based SLAM." *IEEE Intelligent Transportation Systems
  Magazine*, 2(4), 31 to 43.
- Sturm, J., Engelhard, N., Endres, F., Burgard, W. and Cremers, D. (2012).
  "A Benchmark for the Evaluation of RGB-D SLAM Systems." IROS, 573 to 580.
- Zhang, Z. and Scaramuzza, D. (2018). "A Tutorial on Quantitative
  Trajectory Evaluation for Visual(-Inertial) Odometry." IROS, 7244 to 7251.
