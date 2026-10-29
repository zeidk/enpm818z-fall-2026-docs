====================================================
Going Further
====================================================

.. admonition:: Reading material, not covered in class
   :class: note

   This page is the written version of the deck's appendix. It is **reading
   material**: we do not present it in class, and it is **not on the quiz**.

   Each section picks up a topic from the :doc:`lecture <l8_lecture>` and
   adds the math, sources or more numbers. The sections follow the deck's
   order. Read the one you need, when you need it. The running example is
   the lecture's: one Town01 junction, with car A turning left across the
   AV's lane, and :math:`t` = 0 as now.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Section**
     - **What it adds to the lecture**
   * - :ref:`l8-app-sec-physics`
     - How the fit reads speed, heading, turn rate and braking from a track;
       how our test set is built.
   * - :ref:`l8-app-sec-scoring`
     - CV's uncertainty term by term, why the 95% region's radius is
       2.45 times :math:`\sigma`, and Waymo's miss rate and mAP.
   * - :ref:`l8-app-sec-map`
     - The three map scores written out, P(left) as car A approaches the
       junction, the map-aware predictor's results (on car A, on the test
       set, calibration, where it goes wrong), Autoware's map-based
       prediction, and hands-on part 3.
   * - :ref:`l8-app-sec-drivers`
     - Car B following car A, the Intelligent Driver Model (IDM) written out
       and worked by hand, its parameters, and the gap at which car B
       follows steadily.


.. _l8-app-sec-physics:

Physics Models
--------------

This section continues the slides "Step 1: read car A's motion from its
track", "Constant turn rate: CTRV and CTRA" and "Error against horizon, on
2476 predictions" in the Physics Models section of the :doc:`lecture
<l8_lecture>`.


.. _l8-app-fit:

Reading Speed, Heading, Turn Rate and Braking from a Track
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Take the track's last 1.5 s: 16 positions :math:`(x_i, y_i)` at times
:math:`\tau_i` = −1.5, −1.4, ..., 0 s (0 is now). Fit, separately for
:math:`x` and for :math:`y`, a curve with constant acceleration:

.. math::

   x(\tau) = x_0 + v_x\,\tau + \tfrac12\,a_x\,\tau^2

1. **Least squares:** find the :math:`x_0`, :math:`v_x` and :math:`a_x` that
   make the sum of :math:`\big(x_i - x(\tau_i)\big)^2` smallest. In matrix
   form, the rows :math:`[\,1,\ \tau_i,\ \tau_i^2/2\,]` make the matrix
   :math:`X`, and :math:`\mathbf{x}` is the column of the 16 :math:`x_i`.
   Then :math:`[x_0, v_x, a_x]^\top = (X^\top X)^{-1} X^\top \mathbf{x}`.
   The same is done for :math:`y`.
2. **Speed and heading:** the speed is
   :math:`v = \sqrt{v_x^2 + v_y^2}`, and the heading is
   :math:`\theta = \operatorname{atan2}(v_y, v_x)`, the direction of travel
   measured counterclockwise from east.
3. **Turn rate:** :math:`\omega = (v_x a_y - v_y a_x) / v^2`. This is the
   part of the acceleration across the motion, divided by the speed.
4. **Acceleration along the motion:** :math:`(v_x a_x + v_y a_y) / v`;
   negative is braking.

For car A: :math:`v` = 5.99 m/s, :math:`\theta` = −178.14° (1.86° south of
west), :math:`\omega` = 0.049 rad/s, braking 0.96 m/s².


.. _l8-app-testset:

How the Test Set Is Built
~~~~~~~~~~~~~~~~~~~~~~~~~

Everything is in ``l8sim.test_set()``, and every number is chosen.

1. The six ways through the junction, at cruising speeds of 6, 7, 8, 9 and
   10 m/s, four random seeds each: 6 × 5 × 4 = 120 drives.
2. Each drive draws a braking between 0.8 and 2.0 m/s² and a sideways
   acceleration in the turn between 1.5 and 2.5 m/s². After the turn the car
   speeds up at 1.0 m/s². The speed wanders by 0.3 m/s² (a slow random
   change), and the driver steers it back toward the cruising speed.
3. Tracks: a position every 0.1 s, with a 0.05 m error, as in our scene.
4. From each drive, we scored one prediction every 0.5 s, while the car is
   between 50 m before the junction and its exit, with 2 s of history and
   5 s of future: 2476 predictions.
5. "A turn" means that the true heading changes by more than 20° in the next
   5 s: 1095 of the predictions. The other 1381 are "no turn".


.. _l8-app-sec-scoring:

Scoring
-------

This section continues the slides "A miss" and "CV's 95% region" in the
Scoring section of the :doc:`lecture <l8_lecture>`.


.. _l8-app-cvvar:

CV's Uncertainty, Term by Term
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each axis, the variance of CV's predicted position at horizon :math:`h`
is:

.. math::

   \sigma^2(h) = \sigma_p^2 + 2h\,\sigma_{pv} + h^2\sigma_v^2 + q\,\frac{h^3}{3}

1. :math:`\sigma_p^2`, :math:`\sigma_{pv}` and :math:`\sigma_v^2` say how
   uncertain the fit's position and velocity are (variance of the position,
   their covariance, variance of the velocity). They come from the 0.05 m
   track errors; our code uses a straight-line fit's formula for them. For
   car A: 0.00057 m², 0.00055 m²/s and 0.00074 m²/s². The prediction takes
   its velocity from the constant-acceleration fit, whose velocity error is
   larger (0.103 against 0.027 m/s), so the region is too small at the
   shortest horizons.
2. :math:`q\,h^3/3` is a speed that wanders at random, with
   :math:`q` = 0.5 × 0.5 = 0.25 m²/s³ (chosen). It is a close relative of
   L3's process noise: there the acceleration was constant over each 0.1 s
   step; here it changes all the time, which gives :math:`q\,h^3/3`.
3. At :math:`h` = 5 s: the fit part is 0.00057 + 2 × 5 × 0.00055 + 25 ×
   0.00074 = 0.0245 m²; the wander is 0.25 × 125 / 3 = 10.42 m²; so
   :math:`\sigma = \sqrt{10.44}` = 3.23 m.

From :math:`h` = 1 s on, the wander is almost all of it: CV's uncertainty is
about what the driver does next, not about the track.


.. _l8-app-chi2:

Why the 95% Region's Radius Is 2.45σ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the error is Gaussian with the same :math:`\sigma` along :math:`x` and
:math:`y`, the squared distance in units of :math:`\sigma`,
:math:`d^2/\sigma^2`, follows a chi-square distribution with 2 degrees of
freedom (L3, L6: the NIS). :math:`d` is the distance between the predicted
and the true position.

1. For 2 degrees of freedom: :math:`P(d^2/\sigma^2 \le c) = 1 - e^{-c/2}`.
2. Set it to 0.95: :math:`e^{-c/2}` = 0.05, so :math:`c = -2\ln 0.05` =
   5.991.
3. Radius: :math:`\sigma\sqrt{5.991} = 2.448\,\sigma`. At :math:`h` = 5 s:
   2.448 × 3.23 = 7.91 m.
4. The truth is inside when :math:`d^2/\sigma^2 \le 5.991`. Count those over
   many predictions: an honest region holds about 95% of them.


.. _l8-app-womd:

Waymo's Miss Rate and mAP
~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   "A single distance threshold to determine IsMatch is insufficient: we
   want a stricter criteria for slower moving and closer-in-time
   predictions, and also different criteria for lateral deviation (e.g.
   wrong lane) versus longitudinal (e.g. wrong speed profile)" (Ettinger et
   al., 2021).

- A mode (one of several predicted futures, defined in Several Futures in
  the :doc:`lecture <l8_lecture>`) matches when its error **across** the
  lane is under
  :math:`\lambda_{lat}` and its error **along** the lane is under
  :math:`\lambda_{lon}`. At 3, 5 and 8 s: :math:`\lambda_{lat}` = 1, 1.8
  and 3 m; :math:`\lambda_{lon}` = 2, 3.6 and 6 m.
- Both are multiplied by a scale from the road user's speed at the start:
  0.5 below 1.4 m/s, 1 above 11 m/s, a straight line between (Waymo, 2021
  challenge page); "so that we do not over-penalize faster agents"
  (Ettinger et al., 2021). Car A at 5.99 m/s: 0.5 + 0.5 × (5.99 − 1.4) /
  (11 − 1.4) = 0.74, so at 5 s :math:`\lambda_{lat}` = 1.8 × 0.74 =
  1.33 m.
- mAP (mean average precision): the modes are ranked by their confidence,
  and the miss rate's match decides the true and false positives. "The
  final mAP metric averages over eight different ground truth trajectory
  shapes".


.. _l8-app-sec-map:

Using the Map
-------------

This section continues the slides "Step 4: Bayes' rule turns the scores
into probabilities" and "Results" in the Using
the Map section of the :doc:`lecture <l8_lecture>`.


.. _l8-app-bayes:

All Three Scores, Written Out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each mode :math:`m`, multiply its prior :math:`P(m)` by three
likelihoods, :math:`L_v` (speed), :math:`L_\theta` (heading) and
:math:`L_d` (offset from the lane's center), each
:math:`L = e^{-\frac12(\Delta/\sigma)^2}`. Then divide by the sum over the
modes. :math:`\Delta` is the difference between what the track shows and
what the mode expects, and :math:`\sigma` is its spread (chosen).

.. list-table::
   :widths: 25 35 20 20
   :header-rows: 1
   :class: compact-table

   * - **Score**
     - **Difference; σ (chosen)**
     - **Left**
     - **Straight on**
   * - speed :math:`L_v`
     - −0.524 and −2.012 m/s; 1.0 m/s
     - 0.872
     - 0.132
   * - heading :math:`L_\theta`
     - 1.86°; 8°
     - 0.973
     - 0.973
   * - offset :math:`L_d`
     - 0.07 m; 0.7 m
     - 0.995
     - 0.995
   * - prior × all three
     -
     - 0.4221
     - 0.0639

1. Left: 0.5 × 0.872 × 0.973 × 0.995 = 0.4221. Straight on: 0.5 × 0.132 ×
   0.973 × 0.995 = 0.0639.
2. P(left) = 0.4221 / (0.4221 + 0.0639) = 0.869; P(straight on) = 0.131.

Multiplying the three treats them as independent: a simplification.


.. _l8-app-pleft:

P(left) as Car A Approaches
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/p_left_time.png
   :alt: P(left turn) against time from minus 4 to 3 seconds, 0 to 1. A magenta line stays at 0.5 until about minus 1.5 seconds, rises through 0.6 at minus 1 and 0.87 at 0, and reaches about 0.99 after 1 second. A dashed green vertical line at minus 2, tag 1: car A starts braking. A gray dotted vertical line at 0, tag 2: now.
   :width: 70%
   :align: center

   P(left), the probability of the left-turn mode, against time, 0 = now.
   **1:** the dashed green line, :math:`t` = −2 s, when car A starts braking.
   **2:** the gray dotted line, now.

**1** Car A starts braking, :math:`t` = −2 s. **2** Now, :math:`t` = 0.
P(left) at :math:`t` = −2, −1, 0 and +1 s: 0.50, 0.60, 0.87 and 0.99. More
than 17.3 m from the junction, a driver about to turn could still drive
8 m/s: :math:`\sqrt{5.42^2 + 2 \times 1.0 \times 17.3}` = 8.0. So both
paths expect 8 m/s, and P(left) stays 0.5. Closer in, each second of braking
adds evidence.


.. _l8-lec-map-truth:

The Map-Aware Prediction Against the Truth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/modes_vs_truth.png
   :alt: The close-up of the junction with car A at x 175. The thick magenta left-turn mode, p = 0.87, curves into the side road; the magenta dashed straight-on mode, p = 0.13, runs west. The black truth follows the magenta left-turn line into the side road, its dots a little short of the magenta dots.
   :width: 70%
   :align: center

   Car A's two modes against the truth, a dot every second. Thick magenta:
   the left turn, probability 0.87. Dashed magenta: straight on, 0.13. Black:
   the truth. Its dots fall a little short of the left mode's dots.

The left mode's error at 1 to 5 s: 0.20, 0.62, 1.04, 1.46 and 1.88 m.

The mode picks the correct lane but drives it a little too fast: it turns at
5.42 m/s, and car A turns at 5.0 m/s (our choice for the truth). 5.42 − 5.0 =
0.42 m/s too fast, so the mode gets about 0.42 m farther ahead of car A every second.

CV, for comparison: FDE 12.35 m.


.. _l8-lec-map-test:

Map-Aware Prediction on the Test Set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/test_scores.png
   :alt: A bar chart of mean FDE at 5 seconds, in meters, on the test set's predictions with a turn ahead. Blue CV 20.8, purple CTRV 19.1, dark gold CTRA 18.3, magenta map most likely mode 5.0, and a hatched magenta bar, map best of the modes, 1.8. A gray dotted line at 2 meters.
   :width: 70%
   :align: center

   Mean FDE at 5 s on the test set's predictions with a turn ahead. Blue:
   CV. Purple: CTRV. Dark gold: CTRA. Magenta: the map's most likely mode.
   Hatched magenta: the best of the map's modes (minFDE). Gray dotted line:
   2 m, the miss threshold.

With a turn ahead (1095 predictions):

- The true path is the most likely mode 84% of the time.
- Still, the most likely mode misses 50.5% of the time (mean FDE 4.98 m):
  the correct lane, at the wrong speed.

With no turn, the most likely mode does worse than CV: FDE 3.91 against
3.64 m, and it misses more (49.5 against 35.9%). In 1 of 10 of these
predictions, its most likely mode is the wrong lane.

.. note::

   **So:** near a junction, the most likely mode is the correct path (84%), often at
   the wrong speed; with no turn ahead, CV does better, so the AV keeps a
   CV mode too.


.. _l8-lec-calibration:

Calibration: How Often the Probabilities Come True
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Calibration
   :class: note

   A predictor is calibrated when, of all the futures it gives a
   probability :math:`p`, a fraction :math:`p` comes true (Guo et al.,
   2017). Of 100 modes given 0.8, about 80 should be the true path.

Our test set: every mode of every prediction (4896 modes), in four groups by
its probability. Each dot is a group; its bar shows how far chance alone
moves it.

.. figure:: /_static/images/L8/reliability.png
   :alt: A square plot of share that came true, 0 to 1, against probability given, 0 to 1 (each dot is placed at its group's mean). A gray dashed diagonal, tag 1. Four magenta dots with error bars: near 0.06 and 0.09, at 0.5 and 0.5, at 0.81 and 0.73 with a long bar, tag 2, below the diagonal, and near 0.99 and 0.98.
   :width: 55%
   :align: center

   The share of each group's modes that came true against the probability
   given (the group's mean). Each dot: a group; its bar: how far chance
   alone moves it. **1:** the diagonal, where a perfectly calibrated
   predictor's dots sit. **2:** the group of car A's 0.87 (0.7 to 0.9):
   given 0.810 on average, came true 0.729.

The table gives the same four groups:

.. list-table::
   :widths: 28 24 24 24
   :header-rows: 1
   :class: compact-table

   * - **Probability given**
     - **Mean given**
     - **Came true**
     - **Modes**
   * - 0 to 0.3
     - 0.061
     - 0.091
     - 904
   * - 0.3 to 0.7
     - 0.500
     - 0.500
     - 3032
   * - 0.7 to 0.9
     - 0.810
     - 0.729
     - 240
   * - 0.9 to 1
     - 0.986
     - 0.976
     - 720

Modes from one drive are not independent, so chance is counted by redrawing
whole drives at random: it moves the 0.729 by about 0.06. The gap,
0.810 − 0.729 = 0.081, is only 1.3 times that: this test set cannot show
whether the predictor is too sure in the group of car A's 0.87.


.. _l8-lec-disc-calibration:

Discussion: Trusting the Probabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Discussion
   :class: hint

   Our modes given 0.810 came true 0.729 of the time, and chance alone moves
   that by about 0.06. **What would you check before you trust these
   probabilities in a car? What goes wrong in the planner if they are too
   sure?** Three minutes with your neighbors.

.. dropdown:: What to listen for
   :color: success
   :icon: check-circle

   - **More drives.** Chance is counted by drives, and it shrinks with the
     square root of their number, so four times the drives about halves the
     0.06.
   - **Groups, not only the total.** A predictor can be calibrated on average
     and too sure in some scenes, such as left turns. Check those scenes on
     their own.
   - **Too sure hurts the planner.** If a 0.87 came true only 0.73 of the time,
     the other future would happen 0.27 of the time, not 0.13: about twice as
     often as the planner expects, so it is less ready for it than it should
     be.
   - **The fix:** rescale the probabilities on drives kept out of training,
     then draw the calibration plot again.


.. _l8-lec-map-wrong:

Where Map-Aware Prediction Goes Wrong
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **The speed along the path.** The correct lane at the wrong speed still
   misses: our test set's drivers turn at 1.5 to 2.5 m/s² sideways, and the
   predictor assumes 2.0.
2. **A driver who does not look like the rule.** A car cruising at 6 m/s on
   an 8 m/s street looks like a car about to turn.
3. **Off the map.** A car that leaves its lane (a U-turn, parking, avoiding
   something) has no lane to follow. Pedestrians and cyclists often have no
   lane to follow.
4. **A wrong map.** If roadworks close a lane, the map is out of date.

.. note::

   Keep a CV mode next to the lane modes. When no lane fits (a large offset
   or heading gap on every lane), the CV mode gets most of the probability.

.. tip::

   See "In industry: Autoware's map-based prediction" in :doc:`Going
   Further <l8_appendix>`.


.. _l8-app-autoware:

In Industry: Autoware's Map-Based Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Autoware's ``map_based_prediction`` package does what we did, with lanelets
(L7) as the lanes (Autoware Foundation, map-based prediction):

.. note::

   "``map_based_prediction`` is a module to predict the future paths (and
   their probabilities) of other vehicles and pedestrians according to the
   shape of the map and the surrounding environment".

1. "Get reference path: Create a reference path for the object from the
   associated lanelet".
2. "Predict object maneuver: Generate predicted paths for the object.
   Assign probability to each maneuver of Lane Follow, Left Lane Change,
   and Right Lane Change based on the object history and the reference path
   obtained in the first step".

Autoware detects a lane change from the distance to each lane boundary and
the time to reach it (Autoware Foundation, map-based prediction).


.. _l8-lec-handson-modes:

Hands-On, Part 3: Two Futures and Their Probabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``modes`` part of the hands-on script draws car A's two futures, with
line widths that show their probabilities, and P(left) against time on the
right. The commands are on :doc:`the Code page <l8_code>`.

.. admonition:: What to look at
   :class: hint

   1. Move now from −0.5 to 1.0 s. Watch the line widths (the
      probabilities) and P(left) on the right.
   2. In ``l8sim.py``, set ``SIG_V = 0.5``, then ``2.0``. ``SIG_V`` is the
      :math:`\sigma` of Step 3, 1.0 m/s in the lecture. What happens to
      P(left) at :math:`t` = 0, and why?
   3. Set ``A_LAT = 1.5``. ``A_LAT`` is the sideways acceleration of Step 2,
      2.0 m/s² in the lecture. Does the left mode's FDE go down? Why?


.. _l8-app-sec-drivers:

Other Drivers
-------------

This section continues the slide "Following: the IDM" in the Other Drivers
section of the :doc:`lecture <l8_lecture>`.


.. _l8-lec-b-slows:

Car B Slows Because Car A Slows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/b_speed.png
   :alt: Car B's speed in meters per second against time from minus 2 to 5 seconds, a gray dotted vertical line at 0 labeled now. The black truth falls from 8.0 to about 6.5 at 3.2 seconds, then rises to about 7.3 at 5 seconds. A blue line, CV, stays flat at 7.76 from 0 to 5 seconds. A magenta dashed line, the IDM behind car A's likely future, follows the truth down to about 6.75 at 3 seconds and back up to about 7.6.
   :width: 70%
   :align: center

   Car B's speed against time; the dotted line is now. Black: the truth.
   Blue: CV, which holds B's speed. Magenta dashed: the IDM, a driver model,
   following car A's most likely future.

At :math:`t` = 0 there are 22.3 m between car A's rear and B's front. Car A brakes
for its turn, so B must slow too, until car A leaves its lane.

- CV keeps B at 7.76 m/s: FDE 3.55 m.
- A driver model (the IDM, next) that follows car A's most likely future: FDE
  0.92 m.

In truth, B is slowest at :math:`t` = 3.2 s, at 6.48 m/s.

.. note::

   To predict B, predict car A first. A predictor that treats each road user
   alone cannot.


.. _l8-lec-idm:

The Intelligent Driver Model (IDM): B's Acceleration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A model of a driver following another car (Treiber et al., 2000):

.. math::

   a = a_{\max}\Big[\,1 - \Big(\frac{v}{v_0}\Big)^{4} - \Big(\frac{s^*}{s}\Big)^2\,\Big]

- :math:`a`: B's acceleration; :math:`v`: B's speed; :math:`s`: the gap from
  B's front to car A's rear; :math:`s^*`: the gap B wants (next section).
- :math:`a_{\max}` = 0.73 m/s²: B's top acceleration (the paper's value).
  :math:`v_0` = 9 m/s: the speed B would like to drive (chosen).
- :math:`1 - (v / v_0)^4`: on an empty road, B speeds up, less and less as
  :math:`v` nears :math:`v_0`.
- :math:`(s^* / s)^2`: grows as the gap :math:`s` shrinks; it is 1 when
  :math:`s` equals the gap B wants, :math:`s^*`. B brakes when this term is larger than the free-road
  term (step 5 of :ref:`l8-lec-idm-hand`).

.. tip::

   See "The IDM's parameters, and steady following" in :doc:`Going Further
   <l8_appendix>`.


.. _l8-lec-idm-gap:

The IDM: the Gap B Wants
~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   s^* = s_0 + v\,T + \frac{v\,\Delta v}{2\sqrt{a_{\max}\,b}}

- :math:`s_0` = 2 m: the smallest gap, even when B stands still.
- :math:`v\,T`, with :math:`T` = 1.6 s: B keeps 1.6 s of driving between
  itself and car A.
- :math:`\Delta v`: B's speed minus car A's, how fast B closes in. With
  :math:`b` = 1.67 m/s², a comfortable braking, the last term makes the gap B
  wants larger when B closes in fast.
- :math:`T`, :math:`b` and :math:`s_0` are the paper's values (Treiber et
  al., 2000).


.. _l8-lec-idm-hand:

The IDM, by Hand, for Car B
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. From the tracks: :math:`v` = 7.76 m/s, car A's 5.99, so :math:`\Delta v` =
   7.76 − 5.99 = 1.77 m/s; :math:`s` = 22.25 m.
2. The gap B wants: :math:`\sqrt{a_{\max}\,b} = \sqrt{0.73 \times 1.67}` =
   1.104, so :math:`s^*` = 2 + 7.76 × 1.6 + 7.76 × 1.77 / (2 × 1.104) =
   2 + 12.42 + 6.22 = 20.64 m.
3. The free-road term: 1 − (7.76 / 9)⁴ = 1 − 0.553 = 0.447.
4. The gap term: (20.64 / 22.25)² = 0.861.
5. The gap term is 0.861 − 0.447 = 0.414 larger, so B's acceleration
   :math:`a` is 0.73 × 0.414 = **0.30** m/s² of braking: B starts to brake.


.. _l8-app-idm:

The IDM's Parameters, and Steady Following
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The exponent 4 in :math:`(v / v_0)^4` is the paper's :math:`\delta`. The
paper's Table I (Treiber et al., 2000): :math:`v_0` = 120 km/h,
:math:`T` = 1.6 s, :math:`a_{\max}` = 0.73 m/s², :math:`b` = 1.67 m/s²,
:math:`\delta` = 4, :math:`s_0` = 2 m. We keep all but :math:`v_0`, which is
a highway's; ours is 9 m/s (chosen).

**Steady following:** set :math:`a` = 0 and :math:`\Delta v` = 0 in the
IDM, so :math:`1 - (v/v_0)^4 = (s^*/s)^2` and
:math:`s = s^* / \sqrt{1 - (v / v_0)^4}`. At :math:`v` = 8 m/s:

1. :math:`s^*` = 2 + 8 × 1.6 = 14.8 m.
2. 1 − (8/9)⁴ = 0.376.
3. :math:`s` = 14.8 / √0.376 = 24.1 m.

Our simulation starts car B at :math:`t` = −6 s, at 8 m/s with 24 m between
car A's rear and B's front: near that steady gap.


Sources for This Page
---------------------

The full reading list for the lecture is in :doc:`l8_references`. This page
cites:

- Schubert, R., Richter, E. and Wanielik, G. (2008). "Comparison and
  Evaluation of Advanced Motion Models for Vehicle Tracking." Proceedings of
  the 11th International Conference on Information Fusion (FUSION 2008),
  Cologne, Germany, 730 to 735.
- Ettinger, S. et al. (2021). "Large Scale Interactive Motion Forecasting
  for Autonomous Driving: The Waymo Open Motion Dataset." ICCV, 9710 to
  9719.
- Waymo LLC. `Motion Prediction, 2021 Waymo Open Dataset Challenge
  <https://waymo.com/open/challenges/2021/motion-prediction/>`_. Accessed
  2026-10-24.
- Autoware Foundation. `autoware_map_based_prediction, README
  <https://github.com/autowarefoundation/autoware_universe/blob/main/perception/autoware_map_based_prediction/README.md>`_.
  Accessed 2026-10-14.
- Treiber, M., Hennecke, car A. and Helbing, D. (2000). "Congested traffic
  states in empirical observations and microscopic simulations." *Physical
  Review E*, 62(2), 1805 to 1824.
