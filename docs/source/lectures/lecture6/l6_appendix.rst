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
   * - `RTK`_
     - Why RTK's leftover error can be centimeters: the carrier wave.
   * - `ICP by SVD`_
     - The rotation of ICP's Step 4 in general, from the SVD of :math:`H`,
       and when that rotation is not unique.
   * - `NDT`_
     - The score NDT gives one pose.
   * - `The Likelihood Field`_
     - How MCL scores one scan point, and why each number in the score was
       chosen.
   * - `Pose-Graph Least Squares`_
     - The three-pose graph of the SLAM section, written out as a weighted
       least-squares problem and solved step by step.
   * - `APE and RPE`_
     - Two ways to score a trajectory: the absolute error and the relative
       error.


The Error Bound
---------------

This section continues the Introduction of the :doc:`lecture <l6_lecture>`:
where Reid et al. (2019) get 0.29 m.


The 0.33 m in a Turn, and the Heading's Share
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Symbols: lane center radius :math:`r`, lane width :math:`w`; car width
:math:`w_v` and length :math:`l_v`; the box around the car is :math:`x` wide
and :math:`y` long. The paper's equations:

.. math::

   \Big(\frac{y}{2}\Big)^2 + \Big(r - \frac{w}{2} + x\Big)^2
   = \Big(r + \frac{w}{2}\Big)^2, \qquad
   \text{room: } \frac{x - w_v}{2} \text{ sideways}, \quad
   \frac{y - l_v}{2} \text{ along the road}

1. With :math:`r = 20` m, :math:`w = 3.0` m, :math:`w_v = 2.1` m and
   :math:`l_v = 5.8` m, we solve for equal room both ways: 0.328 m (box
   2.76 m by 6.46 m). The paper reads 0.33 m off its Figure 14.
2. The heading's share (the paper's equation 17, the same angle error
   :math:`\delta` about every axis):
   :math:`\delta_{\mathrm{lat}} + (\delta_{\mathrm{lon}} + \delta_{\mathrm{vert}} + l_v/2)\,\delta \le 0.33`
   m. Here :math:`\delta_{\mathrm{lat}}`, :math:`\delta_{\mathrm{lon}}` and
   :math:`\delta_{\mathrm{vert}}` are the allowed position errors sideways,
   along the road and up.
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

1. Missing at most :math:`10^{-8}` of the time is about :math:`5.73\sigma`;
   95% is :math:`1.96\sigma`.
2. :math:`0.29 \times 1.96 / 5.73 = 0.099`, so 0.10 m.


RTK
---

This section continues the GNSS and RTK section of the
:doc:`lecture <l6_lecture>`.


Why RTK Reaches Centimeters: the Carrier Wave
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The four RTK steps in the lecture subtract the base's error from the AV's.
How small the leftover gets depends on what the receivers measure.

- A plain receiver times the **code** the satellite sends.
- RTK also measures the **carrier**, the radio wave itself (Navipedia). The
  carrier's wavelength is short, so the leftover error can be centimeters.

.. important::

   "RTK, which achieves performances in the range of a few centimetres, is a
   technique commonly used in surveying applications" (GMV, ESA Navipedia,
   2011).


ICP by SVD
----------

This section continues the Against a Map section of the
:doc:`lecture <l6_lecture>`: Step 4 of the ICP worked example, and what can
go wrong with it.


Step 4 in General: the Rotation from the SVD of H
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The lecture found the rotation with a short form that works only in 2-D. The
general recipe is Kabsch's (Kabsch, 1976), and it works in 2-D or 3-D. Write
the **SVD** (singular value decomposition) of the cross-covariance :math:`H`
as :math:`H = U S V^\top`. Then

.. math::

   R = V \begin{pmatrix} 1 & 0 \\ 0 & d \end{pmatrix} U^\top,
   \qquad d = \det(V U^\top)

:math:`d = -1` means the best fit is a mirror image, which no car can do.
Putting :math:`d` in the middle matrix turns it back into a rotation.

**Our three pairs.** The lecture's worked example gave

.. math::

   H = \begin{pmatrix} -2 & 2 \\ -8 & 2 \end{pmatrix}

Its SVD, from the figure generator, rounded:

.. math::

   U = \begin{pmatrix} -0.290 & -0.957 \\ -0.957 & 0.290 \end{pmatrix},\quad
   S = \begin{pmatrix} 8.606 & 0 \\ 0 & 1.394 \end{pmatrix},\quad
   V^\top = \begin{pmatrix} 0.957 & -0.290 \\ -0.290 & -0.957 \end{pmatrix}

1. :math:`\det(V U^\top) = +1`: no mirror, so :math:`d = 1`.
2. So :math:`R = V U^\top`. One entry worked out, the top right:
   :math:`0.957 \times (-0.957) + (-0.290) \times 0.290 = -1.000`. All four
   entries give

   .. math::

      R = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}

   the :math:`90^\circ` quarter turn the lecture found with the short form.


When the Rotation Is Not Unique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the pairs fixed, the 2-D rotation
:math:`\alpha = \operatorname{atan2}(H_{12} - H_{21},\ H_{11} + H_{22})` is
**not unique only when both arguments are 0**. A second singular value of 0
alone is not enough: :math:`H = \begin{pmatrix} 0 & 2 \\ 0 & 0 \end{pmatrix}`
has :math:`S = (2, 0)` and still gives one rotation, :math:`90^\circ`.

- **All points on one line** (a single straight wall): for fixed pairs the
  rotation can still be found. The trouble is the pairing: shifted along the
  wall, each scan point finds an equally near map point, so ICP cannot tell
  how far along the wall the AV is. The course code stops with an error when
  the second singular value is near 0, to be safe.
- The lecture's example uses three centered points that are not on one line,
  so nothing in it depends on this case.

.. admonition:: On the road
   :class: important

   A long tunnel or a straight wall with no features leaves the position
   **along** it unknown. ICP's fit looks perfect, and is not. That is another
   reason to check every source against a second one.


NDT
---

This section continues the Against a Map section of the
:doc:`lecture <l6_lecture>`, where NDT, the normal distributions transform,
was named.


NDT's Score for One Pose
~~~~~~~~~~~~~~~~~~~~~~~~

NDT cuts the map into cells. For each cell :math:`c` with map points, it
keeps the mean :math:`\boldsymbol{\mu}_c` and the covariance
:math:`\Sigma_c` of those points (Biber and Strasser, 2003). To score a pose,
place the scan at that pose. Each scan point :math:`\mathbf{s}` falls in some
cell :math:`c`, and

.. math::

   \text{score} = \sum_{\mathbf{s}} \exp\!\Big(-\tfrac{1}{2}\,
   (\mathbf{s} - \boldsymbol{\mu}_c)^\top\,\Sigma_c^{-1}\,
   (\mathbf{s} - \boldsymbol{\mu}_c)\Big)

- The term in the exponent is the squared Mahalanobis distance of
  :doc:`L3 </lectures/lecture3/l3_index>`. It is small along a wall's long
  axis and large across it. So a point near a wall but slid along it scores
  well, and a point off the wall scores badly.
- NDT improves the pose by moving it uphill on the score, step by step, from
  a starting guess. As for ICP, that guess is the filter's pose.


The Likelihood Field
--------------------

This section continues the Against a Map section of the
:doc:`lecture <l6_lecture>`, where MCL weighs each particle by how well its
scan lands on the map.


How MCL Scores One Scan Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Place a scan point in the map where a particle says the car is. Let :math:`d`
be the distance from that point to the nearest map point. The course code
adapts the likelihood field of Thrun et al. (2005, Sec. 6.4):

.. math::

   p(d) = z_\text{hit}\, e^{-d^2 / (2\sigma^2)} + z_\text{rand} / d_\text{max}

The score is a bell curve in :math:`d`, plus a small constant. The values
are chosen: :math:`\sigma = 1.0` m, :math:`z_\text{hit} = 0.9`,
:math:`z_\text{rand} = 0.1` and :math:`d_\text{max} = 3` m. Beyond
:math:`d_\text{max}`, only the second term counts. Thrun et al. divide
:math:`z_\text{rand}` by the sensor's maximum range; the course code divides
by :math:`d_\text{max}`.

- **Why** :math:`z_\text{rand}`: a point that hits a parked car the map
  lacks is not impossible. Without the constant, one such point would zero
  the weight of a good particle.
- **Why a wide** :math:`\sigma`: with 2000 particles over a whole street, the
  particle nearest the truth is often a meter or a few degrees off. A narrow
  field would score it like a wrong one, and it must score better.
- **Why 60 points per scan:** neighboring beams hit the same wall, so they
  are not independent. Multiplying hundreds of them makes one particle take
  all the weight after a single scan.


Pose-Graph Least Squares
------------------------

This section continues the SLAM section of the :doc:`lecture <l6_lecture>`:
the three-pose graph whose loop closure left a gap of :math:`(0.1, 0.7)`,
0.71 m.


The Three-Pose Graph, Written Out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The unknowns are :math:`p_2` and :math:`p_3`; :math:`p_1 = (0, 0)` is fixed.
Each edge says "this difference should equal what I measured". The measured
motions, chosen for the lecture's example, are
:math:`z_{12} = (10.3, 0.4)` and :math:`z_{23} = (-5.2, 8.3)` from odometry,
each with :math:`\sigma = 0.5` m, and the loop closure
:math:`z_{31} = (-5.0, -8.0)` with :math:`\sigma = 0.1` m. The solver
minimizes the squared misses, each divided by its edge's variance (Grisetti
et al., 2010):

.. math::

   \frac{\|p_2 - p_1 - z_{12}\|^2}{0.5^2}
   + \frac{\|p_3 - p_2 - z_{23}\|^2}{0.5^2}
   + \frac{\|p_1 - p_3 - z_{31}\|^2}{0.1^2}

The minimum is the corrected graph. The poses hold positions only, so
:math:`x` and :math:`y` are two separate problems. For :math:`x`, the gap is
0.1 m:

1. Total variance around the loop: :math:`0.25 + 0.25 + 0.01 = 0.51`.
2. Each odometry edge gives up :math:`0.1 \times 0.25/0.51 = 0.049` m; the
   loop gives up :math:`0.1 \times 0.01/0.51 = 0.002` m.
3. :math:`p_{2,x} = 10.3 - 0.049 = 10.251`, and
   :math:`p_{3,x} = 10.251 - 5.2 - 0.049 = 5.002`.
4. Check: :math:`p_1 - p_3 = -5.002`, which misses
   :math:`z_{31,x} = -5.0` by the loop's 0.002.

For :math:`y`, the same steps with the gap 0.7 give
:math:`p_{2,y} = 0.057` and :math:`p_{3,y} = 8.014`. The figure generator's
least-squares solve gives the same numbers.

.. note::

   With headings in the poses, the problem is no longer linear, and real
   solvers iterate. Each step is still this kind of weighted least squares.


APE and RPE
-----------

This section continues the Fusion in the EKF section of the
:doc:`lecture <l6_lecture>`, where APE scored each run.


Two Ways to Score a Trajectory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Absolute error** (APE, also called ATE) compares each estimated pose
  with the true one: "the global consistency can be evaluated by comparing
  the absolute distances between the estimated and the ground truth
  trajectory" (Sturm et al., 2012). The lecture's APE is its position part,
  summarized by the RMSE.
- **Relative error** (RPE) compares motions over a fixed interval: did the
  estimate move as far, and turn as much, as the truth in those seconds? It
  "measures the local accuracy of the trajectory over a fixed time interval
  :math:`\Delta`. Therefore, the relative pose error corresponds to the drift
  of the trajectory" (Sturm et al., 2012).
- **Why both:** "since VO/VIO systems do not have a global reference (global
  position and yaw), the estimation quality can be evaluated by measuring
  the relative relations between the states at different times" (Zhang and
  Scaramuzza, 2018). VO is visual odometry; VIO is visual-inertial odometry.

.. admonition:: Which score fits which system
   :class: important

   A GNSS-aided filter has a global reference, so APE is the fair score.
   Dead reckoning and odometry alone have none: their APE only grows, and
   RPE says how fast.


Sources for This Page
---------------------

The full reading list for the lecture is in :doc:`l6_references`. This page
cites:

- GMV (2011). `Real Time Kinematics
  <https://gssc.esa.int/navipedia/index.php/Real_Time_Kinematics>`_.
  European Space Agency, Navipedia.
- Kabsch, W. (1976). "A Solution for the Best Rotation to Relate Two Sets of
  Vectors." *Acta Crystallographica Section A*, 32(5), 922 to 923.
- Biber, P. and Strasser, W. (2003). "The Normal Distributions Transform: A
  New Approach to Laser Scan Matching." IROS.
- Thrun, S., Burgard, W. and Fox, D. (2005). *Probabilistic Robotics.* MIT
  Press.
- Grisetti, G., Kümmerle, R., Stachniss, C. and Burgard, W. (2010). "A
  Tutorial on Graph-Based SLAM." *IEEE Intelligent Transportation Systems
  Magazine*.
- Sturm, J., Engelhard, N., Endres, F., Burgard, W. and Cremers, D. (2012).
  "A Benchmark for the Evaluation of RGB-D SLAM Systems." IROS.
- Zhang, Z. and Scaramuzza, D. (2018). "A Tutorial on Quantitative
  Trajectory Evaluation for Visual(-Inertial) Odometry." IROS.
