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
       CTRV and CTRA written out; how our test set is built.
   * - :ref:`l8-app-sec-scoring`
     - CV's uncertainty term by term, why the 95% region's radius is
       2.45 times :math:`\sigma`, and Waymo's miss rate and mAP.
   * - :ref:`l8-app-sec-map`
     - The three map scores written out, P(left) as car A approaches the
       junction, and Autoware's map-based prediction.
   * - :ref:`l8-app-sec-learned`
     - What a learned predictor reads and writes, three well-known designs,
       how they are trained and scored, and pedestrians and cyclists.
   * - :ref:`l8-app-sec-drivers`
     - The terms of the Intelligent Driver Model (IDM), one by one, and the
       gap at which car B follows steadily.


.. _l8-app-sec-physics:

Physics Models
--------------

This section continues the slides "Step 1: read car A's motion from its
track", "Constant turn rate: CTRV and CTRA" and "Error against horizon, on
2417 predictions" in the Physics Models section of the :doc:`lecture
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


.. _l8-app-ctrv:

CTRV, Written Out
~~~~~~~~~~~~~~~~~

In CTRV, the speed :math:`v` and the turn rate :math:`\omega` are fixed, and
the heading turns: :math:`\theta(t) = \theta_0 + \omega t`. The position is
the velocity added up over time:

.. math::

   x(h) = x_0 + \int_0^h v\cos(\theta_0 + \omega t)\,dt
        = x_0 + \frac{v}{\omega}\big[\sin(\theta_0 + \omega h) - \sin\theta_0\big]

.. math::

   y(h) = y_0 + \int_0^h v\sin(\theta_0 + \omega t)\,dt
        = y_0 + \frac{v}{\omega}\big[\cos\theta_0 - \cos(\theta_0 + \omega h)\big]

1. The path is a circle of radius :math:`v / \omega`.
2. When :math:`\omega \to 0`:
   :math:`\sin(\theta_0 + \omega h) - \sin\theta_0 \approx \omega h \cos\theta_0`,
   so :math:`x(h) \to x_0 + v h \cos\theta_0`: constant velocity.
3. The code divides by :math:`\omega`, so it switches to CV for small
   :math:`|\omega|` (``l8sim.py``: below 0.001 rad/s).


.. _l8-app-ctra:

CTRA: CTRV with a Changing Speed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The heading turns as in CTRV, :math:`\theta(t) = \theta_0 + \omega t`, and
the speed changes at a constant rate :math:`a`: :math:`v(t) = v_0 + a t`.

.. math::

   x(h) = x_0 + \int_0^h (v_0 + a t)\cos(\theta_0 + \omega t)\,dt, \qquad
   y(h) = y_0 + \int_0^h (v_0 + a t)\sin(\theta_0 + \omega t)\,dt

- Schubert, Richter and Wanielik give the integrals in closed form
  (Schubert et al., 2008). Our code (``l8sim.py``) adds them up in steps of
  0.01 s instead.
- A braking car's speed reaches 0 and would then go negative: the car would
  drive backward. The code holds the speed at 0 from then on.
- Car A from :math:`t` = 0: braking at 0.96 m/s² from 5.99 m/s, it would
  stop after 5.99 / 0.96 = 6.2 s, past our 5 s horizon.


.. _l8-app-testset:

How the Test Set Is Built
~~~~~~~~~~~~~~~~~~~~~~~~~

Everything is in ``l8sim.test_set()``, and every number is chosen.

1. The six ways through junction 54, at cruising speeds of 6, 7, 8, 9 and
   10 m/s, four random seeds each: 6 × 5 × 4 = 120 drives.
2. Each drive draws a braking between 0.8 and 2.0 m/s² and a sideways
   acceleration in the turn between 1.5 and 2.5 m/s². After the turn the car
   speeds up at 1.0 m/s². The speed wanders by 0.3 m/s² (a slow random
   change).
3. Tracks: a position every 0.1 s, with a 0.05 m error, as in our scene.
4. A prediction every 0.5 s, while the car is between 50 m before the
   junction and its exit, with 2 s of history and 5 s of future: 2417
   predictions.
5. "A turn" means that the true heading changes by more than 20° in the next
   5 s: 1088 of the predictions. The other 1329 are "no turn".


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
   car A: 0.00057 m², 0.00055 m²/s and 0.00074 m²/s².
2. :math:`q\,h^3/3` is a speed that wanders at random, with
   :math:`q` = 0.5 × 0.5 = 0.25 (chosen). It is the same term as L3's
   process noise for a constant-velocity model.
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
   wrong lane) versus longitudinal (e.g. wrong speed profile)." (Ettinger et
   al., 2021)

- A mode matches when its error **across** the lane is under
  :math:`\lambda_{lat}` and its error **along** the lane is under
  :math:`\lambda_{lon}`. At 3, 5 and 8 s: :math:`\lambda_{lat}` = 1, 1.8
  and 3 m; :math:`\lambda_{lon}` = 2, 3.6 and 6 m.
- Both are multiplied by a scale from the road user's speed at the start:
  0.5 below 1.4 m/s, 1 above 11 m/s, a straight line between (Waymo, 2021
  challenge page); "so that we do not over-penalize faster agents"
  (Ettinger et al., 2021). At our 8 m/s: 0.5 + 0.5 × (8 − 1.4) / (11 − 1.4)
  = 0.84, so at 5 s :math:`\lambda_{lat}` = 1.8 × 0.84 = 1.51 m.
- mAP (mean average precision): the modes are ranked by their confidence,
  and the miss rate's match decides the true and false positives. "The
  final mAP metric averages over eight different ground truth trajectory
  shapes."


.. _l8-app-sec-map:

Using the Map
-------------

This section continues the slides "Step 4: Bayes' rule turns the scores
into probabilities" and "Where map-aware prediction goes wrong" in the Using
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
     - 0.4222
     - 0.0640

1. Left: 0.5 × 0.872 × 0.973 × 0.995 = 0.4222. Straight on: 0.5 × 0.132 ×
   0.973 × 0.995 = 0.0640.
2. P(left) = 0.4222 / (0.4222 + 0.0640) = 0.868; P(straight on) = 0.132.

Multiplying the three treats them as independent: a simplification.


.. _l8-app-pleft:

P(left) as Car A Approaches
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/p_left_time.png
   :alt: P(left turn) against time from minus 4 to 3 seconds, 0 to 1. A green line stays at 0.5 until about minus 1.5 seconds, rises through 0.6 at minus 1 and 0.87 at 0, and reaches about 0.99 after 1 second. A dashed orange vertical line at minus 2, tag 1: A starts braking. A gray dotted vertical line at 0, tag 2: now.
   :width: 70%
   :align: center

   P(left), the probability of the left-turn mode, against time, 0 = now.
   **1:** the dashed orange line, :math:`t` = −2 s, when A starts braking.
   **2:** the gray dotted line, now.

**1** A starts braking, :math:`t` = −2 s. **2** Now, :math:`t` = 0.
P(left) at :math:`t` = −2, −1, 0 and +1 s: 0.50, 0.60, 0.87 and 0.99. At
−2 s A still drives 8 m/s, the street's speed: no evidence yet. Each second
of braking adds some.


.. _l8-app-autoware:

In Industry: Autoware's Map-Based Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Autoware's ``map_based_prediction`` package does what we did, with lanelets
(L7) as the lanes (Autoware Foundation, map-based prediction):

.. note::

   "``map_based_prediction`` is a module to predict the future paths (and
   their probabilities) of other vehicles and pedestrians according to the
   shape of the map and the surrounding environment."

1. "Get reference path: Create a reference path for the object from the
   associated lanelet."
2. "Predict object maneuver: Generate predicted paths for the object.
   Assign probability to each maneuver of Lane Follow, Left Lane Change,
   and Right Lane Change based on the object history and the reference path
   obtained in the first step."

A lane change is detected from the distance to each lane boundary and the
time to reach it (Autoware Foundation, map-based prediction).


.. _l8-app-sec-learned:

Learned Predictors
------------------

This section is the Learned Predictors section of the :doc:`lecture
<l8_lecture>`. Our map-aware predictor used lanes as modes, and
probabilities from rules we chose (a turn speed, a :math:`\sigma`). A
learned predictor learns the turn speeds, :math:`\sigma`'s and priors that
we chose by hand, from recorded driving.


.. _l8-app-learned-io:

What a Learned Predictor Reads and Writes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L8/learned_io.png
   :alt: A block diagram. Three gray input boxes on the left: 1. every road user's last few seconds of track; 2. the map's lanes, as polylines (lists of points); 3. traffic lights, the road user's type (car, cyclist). Each has an arrow into a central box: a neural network, weights set by training. Two green arrows lead out to two green boxes: K future tracks for each road user, and one probability for each of them.
   :width: 90%
   :align: center

   A learned predictor. Its inputs: **1** every road user's last few
   seconds of track; **2** the map's lanes, as polylines (lists of points);
   **3** traffic lights and the road user's type (car, cyclist). A neural
   network, with weights set by training, writes :math:`K` future tracks for
   each road user and one probability for each of them.

- The output is the same as our map-aware predictor's: :math:`K` modes and
  their probabilities.
- What changes: the turn speeds, the :math:`\sigma`'s and the priors we
  chose by hand are **set by training** on recorded tracks.


.. _l8-app-learned-designs:

Three Well-Known Designs
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 45 35
   :header-rows: 1
   :class: compact-table

   * - **Model**
     - **Main idea, in the paper's words**
     - **In our terms**
   * - VectorNet (Gao et al., 2020)
     - "Observed agent trajectories and map features are represented as
       sequence of vectors"
     - the lanes and the tracks as lists of points, as in our
       ``l8_scene.npz``
   * - MultiPath (Chai et al., 2019)
     - "predicts a discrete distribution over the anchors and, for each
       anchor, regresses offsets from anchor waypoints along with
       uncertainties"
     - anchors play our candidate lanes' part; each gets a probability, a
       shift and a :math:`\sigma`
   * - MTR (Shi et al., 2022)
     - "a small set of learnable motion query pairs. Each motion query pair
       takes charge of trajectory prediction and refinement for a specific
       motion mode"
     - one learned slot per kind of future (turn left, go straight, ...)

MTR "ranks 1st on the leaderboards of Waymo Open Motion Dataset", in its
authors' words, 2022 (Shi et al., 2022).


.. _l8-app-learned-train:

How Learned Predictors Are Trained and Scored
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Data:** recorded scenes, each cut into an observed part and a future
   part. Argoverse 2 observes 5 s and predicts 6 s (Wilson et al., 2021).
   Waymo's dataset observes 1 s and predicts 8 s, at 10 Hz (Ettinger et al.,
   2021).
2. **Training**, in one common form: the network predicts :math:`K` modes;
   the one nearest the true future is moved toward it, and its probability
   is raised.
3. **Scores:** minADE, minFDE and the miss rate (Argoverse 2); the miss
   rate and mAP (Waymo). The same scores as ours, on the benchmark's test
   scenes.

.. note::

   **Why CV still matters:** it is the baseline every learned model is
   compared with, and the fallback when the learned model meets a road user
   it was not trained for. On our test set with no turn, CV's mean error
   stays under 2 m for 3 s.


.. _l8-app-learned-peds:

Pedestrians and Cyclists
~~~~~~~~~~~~~~~~~~~~~~~~

- They follow few lanes: a pedestrian can turn on the spot and step off the
  curb. Sidewalks and crosswalks help some.
- They move in groups and avoid each other. Social LSTM learns that from
  crowds: each person's prediction depends on the people near them (Alahi et
  al., 2016).
- Their uncertainty grows fast: at 1.4 m/s (chosen, a walking pace) a
  pedestrian can be anywhere within 1.4 × 3 = 4.2 m after 3 s.

.. note::

   Tempe again: a track that restarts at every new class has no history,
   and a predictor with no history has nothing to predict from (NTSB, 2019).


.. _l8-app-sec-drivers:

Other Drivers
-------------

This section continues the slide "The Intelligent Driver Model (IDM), by
hand" in the Other Drivers section of the :doc:`lecture <l8_lecture>`.


.. _l8-app-idm:

The IDM's Terms, One by One
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- :math:`1 - (v / v_0)^4`: on an empty road, speed up, less and less as the
  speed :math:`v` nears the desired speed :math:`v_0`. The exponent, 4, is
  the paper's :math:`\delta`.
- :math:`(s^* / s)^2`: brake when the gap :math:`s` is smaller than the
  desired gap :math:`s^*`.
- :math:`s^* = s_0 + vT + v\,\Delta v / (2\sqrt{a_{\max} b})`: a standstill
  distance :math:`s_0`, a time gap :math:`T`, and more room when closing in
  fast (:math:`\Delta v` is how fast the follower closes in).

The paper's Table I (Treiber et al., 2000): :math:`v_0` = 120 km/h,
:math:`T` = 1.6 s, :math:`a_{\max}` = 0.73 m/s², :math:`b` = 1.67 m/s²,
:math:`\delta` = 4, :math:`s_0` = 2 m. We keep all but :math:`v_0`, which is
a highway's; ours is 9 m/s (chosen).

**Steady following** (:math:`\Delta v` = 0, no acceleration):
:math:`s = s^* / \sqrt{1 - (v / v_0)^4}`. At :math:`v` = 8 m/s:

1. :math:`s^*` = 2 + 8 × 1.6 = 14.8 m.
2. 1 − (8/9)⁴ = 0.376.
3. :math:`s` = 14.8 / √0.376 = 24.1 m.

Our simulation starts car B at :math:`t` = −6 s, at 8 m/s with 24 m between
A's rear and B's front: near that steady gap.


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
- Wilson, B. et al. (2021). "Argoverse 2: Next Generation Datasets for
  Self-Driving Perception and Forecasting." NeurIPS Track on Datasets and
  Benchmarks.
- Autoware Foundation. `autoware_map_based_prediction, README
  <https://github.com/autowarefoundation/autoware_universe/blob/main/perception/autoware_map_based_prediction/README.md>`_.
  Accessed 2026-10-14.
- Gao, J., Sun, C., Zhao, H., Shen, Y., Anguelov, D., Li, C. and Schmid, C.
  (2020). "VectorNet: Encoding HD Maps and Agent Dynamics from Vectorized
  Representation." CVPR. arXiv:2005.04259.
- Chai, Y., Sapp, B., Bansal, M. and Anguelov, D. (2019). "MultiPath:
  Multiple Probabilistic Anchor Trajectory Hypotheses for Behavior
  Prediction." CoRL 2019, PMLR 100, 86 to 99.
- Shi, S., Jiang, L., Dai, D. and Schiele, B. (2022). "Motion Transformer
  with Global Intention Localization and Local Movement Refinement."
  NeurIPS 2022. arXiv:2209.13508.
- Alahi, A., Goel, K., Ramanathan, V., Robicquet, A., Fei-Fei, L. and
  Savarese, S. (2016). "Social LSTM: Human Trajectory Prediction in Crowded
  Spaces." CVPR, 961 to 971.
- National Transportation Safety Board (2019). *Collision Between Vehicle
  Controlled by Developmental Automated Driving System and Pedestrian,
  Tempe, Arizona, March 18, 2018.* NTSB/HAR-19/03.
- Treiber, M., Hennecke, A. and Helbing, D. (2000). "Congested traffic
  states in empirical observations and microscopic simulations." *Physical
  Review E*, 62(2), 1805 to 1824.
