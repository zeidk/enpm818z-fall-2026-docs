====================================================
Going Further
====================================================

.. admonition:: Reading material, not covered in class
   :class: note

   This page is the written version of the deck's appendix. It is **reading
   material**: we do not present it in class, and it is **not on the quiz**.

   Each section picks up a topic from the :doc:`lecture <l3_lecture>` and
   works it out with more numbers, more steps, or a hands-on to run at home.
   The sections follow the deck's order. Read the one you need, when you need
   it.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Section**
     - **What it adds to the lecture**
   * - `Why We Filter`_
     - Why an AV needs a filter at all, the learning objectives, and why there
       is almost no AI in this lecture.
   * - `Uncertainty in Depth`_
     - The base link, noise and bias, where readings land under a bell curve,
       the 2-D circles, and confidence intervals.
   * - `Kalman Filter in Detail`_
     - All four assumptions broken on a real AV, why no fixed matrix can make
       a cosine, and the shared map error fixed with one GNSS fix.
   * - `Motion Model in Detail`_
     - :math:`F`, :math:`\mathbf{w}`, :math:`Q` and :math:`B\,\mathbf{u}`, one
       piece at a time, on the braking example.
   * - `Measurement Model in Detail`_
     - :math:`H`, the sign match's error :math:`\mathbf{v}`, the surprise and
       :math:`R`, on the same example.
   * - `Kalman Filter Hands-On Files`_
     - The tunnel CSV and the script ``kf_tunnel.py``, part by part.
   * - `UKF in Detail`_
     - The unscented Kalman filter worked out with numbers, its code, its
       traps, and a hands-on against the EKF.
   * - `Particle Filter in Detail`_
     - The particle filter worked out with five particles, its code, its
       costs, and a hands-on that finds a lost AV.
   * - `Notation Reference`_
     - Every symbol in the lecture, in one place.


Why We Filter
-------------

This section explains why an AV needs a filter in the first place. First, the
sensors disagree, and none of them is lying. Second, the newest reading on
its own is not enough. Then come the lecture's learning objectives, and why
there is almost no AI in it.

The Sensors Disagree With Each Other
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L2 ended with sensors that are mounted, calibrated and timestamped. Once they
all run, a new problem appears that calibration does not solve.

- GNSS says the AV is **here**. LiDAR map matching, which lines up the laser
  scan with a stored map, says **slightly over there**. The wheel encoders say
  something else. Three sources, three answers.
- None of them is lying. None of them is exactly right.
- And L2 showed that one can be wrong **invisibly**. A GNSS fix between tall
  buildings arrives on time, looks normal, and is several meters off. Nothing
  announces the problem.

.. important::

   We have several numbers that disagree, arrive at different times, and may
   be quietly wrong. The **planner**, the part of the stack that decides where
   to drive, needs **one** answer.

   Producing that one answer is the job of a **filter**.

The Newest Reading Alone Is Not Enough
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each row of the table is one reason the newest reading, on its own, is not
enough.

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: compact-table

   * - **What goes wrong with it**
     - **What the filter does instead**
   * - No single sensor is enough
     - GNSS is absolute but slow, and gone in tunnels. An IMU is fast and
       always there, but it drifts. Together they beat either one.
   * - Readings arrive at different times
     - Sensors never line up. The filter carries an estimate forward, so there
       is an answer at *every* instant.
   * - Every reading is noisy
     - Steering on the last reading would make the AV twitch. The filter
       blends readings instead, in the correct proportion.
   * - Some quantities are not measured
     - In our model, the GNSS reading gives position only. The planner needs
       velocity, and the filter infers it from how position keeps changing.
   * - A sensor can fail or be rejected
     - The filter runs on prediction alone for that cycle, and says how much
       less certain that makes it.

The fourth row is the least obvious. It is why velocity ends up in the
filter's **state**, the list of numbers it tracks, even though no sensor in
our model reports it.

.. note::

   Velocity is not unmeasurable in general. RADAR measures it directly through
   the Doppler effect, and wheel speed sensors give speed. The point is that
   the state can hold quantities your sensors do not measure, and the filter
   still estimates them.

Learning Objectives
~~~~~~~~~~~~~~~~~~~

By the end of this lecture, you will be able to:

- Define **variance**, **standard deviation** and the **covariance matrix**
  :math:`P`.
- Say why the **Kalman gain** leans toward the more precise source, why the
  result beats **either input**, and on what assumption.
- Write down **predict** and **update**, and say what each term means.
- Name the **four assumptions**, and what the **EKF**, **UKF** and **particle
  filter** each replace.
- Build an **EKF**: :math:`f`, :math:`h`, their Jacobians, and :math:`Q_k`.
- Use the **innovation**, **NIS** and a **chi-square gate** to judge a running
  filter, and spot **divergence**.

Two are worth calling out. The second: combining two sources gives an
uncertainty smaller than either one you started with, and the lecture shows
why with numbers. The fifth: you build an EKF in GP3, and the lecture gives
you every piece of it.

.. admonition:: Not in this lecture
   :class: warning

   Detection, the step that turns pixels into boxes, is **L4**. Fusion
   architectures, learned fusion, data association (deciding which
   measurement belongs to which object) and the Tempe crash (Uber, 2018) are
   **L6**. Monte Carlo Localization is **L7**.

There Is Almost No AI in This Lecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a self-driving course, so you may expect a neural network in every
section. Everything in this lecture, and the tracking in L6, is classical
probability and linear algebra, and most of it is decades old.

.. list-table::
   :widths: 45 15 40
   :header-rows: 1
   :class: compact-table

   * - **Technique**
     - **Year**
     - **What it is**
   * - Mahalanobis distance (L6)
     - 1936
     - A distance
   * - Hungarian algorithm (GNN, L6)
     - 1955
     - An assignment
   * - Kalman filter
     - 1960
     - Closed-form algebra
   * - MHT (L6)
     - 1979
     - A hypothesis search
   * - JPDA (L6)
     - 1983
     - Weighted averaging
   * - Particle filter
     - 1993
     - Sample, then resample
   * - Unscented KF
     - 1997
     - Sample, then average

None of these is trained, and none has learned parameters. The same input
gives the same output every time, and you can work out by hand what each one
will do.

.. important::

   **The oldest part of the stack still decides where the AV is**, for three
   reasons.

   - Its uncertainty can be **tested** for honesty, and the lecture tests it.
     Getting a neural network to do that is still an open research problem.
   - It can be **inspected** when it goes wrong, which a safety case needs.
   - Under stated conditions it is **provably the best possible**.

   Old and testable beats new and unverifiable when a vehicle is involved.

So where is the AI? In everything that **produces** the measurements this
filter takes in: detection in **L4**, BEV in **L5**, learned fusion in
**L6**, prediction in **L9**, end-to-end driving in **L12**. Learned parts
turn pixels into objects. Classical estimation decides what to believe about
them over time, because that half has to be verifiable. **Know which half you
are debugging.**


Uncertainty in Depth
--------------------

This section takes the words from the lecture's Terminology section and works
each one out with numbers. First, why we track the AV at its rear axle. Then
noise and bias, what a bell curve says about where readings land, and last,
confidence intervals and the mistake most people make with them.

Why the Base Link Sits on the Rear Axle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An AV is about 4.5 m long, so when we say "the AV is at (103, 2.5)" we need
to say **which point on the body**. Autoware, like many AV stacks, uses the
middle of the rear axle, called the **base link**. There are three reasons.

1. **Its motion is simplest there.** The rear wheels do not steer, so this
   point always moves straight along the heading, even in a turn, and never
   sideways (if the tires do not slip, which is the kinematic model's
   assumption). With speed :math:`v`, heading :math:`\theta`, steering angle
   :math:`\delta` and wheelbase :math:`L` (front axle to rear axle), and a dot
   meaning "rate of change":

   .. math::

      \dot{x} = v\cos\theta, \qquad \dot{y} = v\sin\theta, \qquad
      \dot{\theta} = \frac{v}{L}\tan\delta

   Any other point on the body also slides sideways in a turn, which adds
   terms.

2. **The turn's center lies on the rear axle line.** In a turn, the AV
   circles a point on the line through its rear axle. Path-tracking
   controllers such as **pure pursuit** are built on this geometry.

3. **It is the standard.** Autoware, the open-source AV software, puts its
   base link at "the center of the rear axle of the vehicle", projected onto
   the ground. Localization reports where the base link is, planning plans
   where it should go, and control steers it there.

.. note::

   Autoware states the convention, not the reasons. The reasons come from
   the AV's kinematics.

An Estimate Is Wrong for Two Different Reasons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An estimate can be wrong for two very different reasons, and which one you
have decides what you can do about it.

.. list-table::
   :widths: 22 39 39
   :header-rows: 1
   :class: compact-table

   * - **Kind of error**
     - **What it looks like**
     - **If you average many readings**
   * - **Random error** (*noise*)
     - Readings scatter around some center. Each is wrong by a different
       amount, in a different direction.
     - It **averages away**. More readings, better answer.
   * - **Systematic error** (*bias*)
     - Every reading is shifted the same way, like a bathroom scale that
       always adds two pounds. The scatter can be tiny.
     - It **does not average away**. A thousand readings give a very precise
       wrong answer.

People use the words loosely, so here they are with their strict meanings
(the VIM and ISO 5725, see :doc:`l3_references`).

- **Precision** is how closely repeated readings agree. It is the word for
  **noise**.
- **Trueness** is how close their average sits to the truth. It is the word
  for **bias**.
- **Repeatability is not a third thing.** It is precision measured under the
  tightest conditions: same instrument, same operator, same setup, over a
  short time. Loosen those conditions and the same idea is called
  **reproducibility**.
- **Accuracy**, strictly, means **both at once**. A single reading is
  accurate only if the bias is small *and* the noise is small.

Where Readings Land, if the Noise Is a Bell Curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the noise follows a bell curve, about 68% of readings land within one
:math:`\sigma` of the mean, 95% within two, and 99.7% within three. Here are
those bands for the six GNSS :math:`x` readings of the parked AV, with mean
100.0 m and :math:`\sigma_x = 1.56` m.

.. list-table::
   :widths: 20 25 25 30
   :header-rows: 1
   :class: compact-table

   * - **Range**
     - **In meters**
     - **Expected inside**
     - **Of our six** :math:`x` **readings**
   * - :math:`\mu_x \pm 1\sigma_x`
     - 98.44 to 101.56
     - about 68%
     - 4 of 6, which is 67%
   * - :math:`\mu_x \pm 2\sigma_x`
     - 96.88 to 103.12
     - about 95%
     - 6 of 6
   * - :math:`\mu_x \pm 3\sigma_x`
     - 95.32 to 104.68
     - about 99.7%
     - 6 of 6

Two warnings matter more than the table.

- **Six readings prove nothing.** The counts land close to the expected
  shares, but that is luck plus a well-chosen example. The table is not
  evidence that the noise really is a bell curve.
- **These percentages are for one axis at a time.** In two dimensions they
  are different, and smaller (next subsection). It matters every time you
  draw an ellipse: it is the difference between an ellipse that means 95%
  and one that means 86%.

.. important::

   **Variance describes spread, not correctness.** Receiver B in the lecture
   had this exact :math:`\sigma` and was still 3.2 m off.

In Two Dimensions: How Far Out Is Unusual
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Take east and north errors, each with the same :math:`\sigma`, independent
of each other. A circle of radius :math:`r` around the expected position
holds this share of readings:

.. math::

   \text{share inside } r \;=\; 1 - e^{-r^2/2\sigma^2}

.. list-table::
   :widths: 20 25 30 25
   :header-rows: 1
   :class: compact-table

   * - **Radius** :math:`r`
     - **Inside, 2-D**
     - **Within** :math:`\pm r` **, 1-D**
     - **Outside, 2-D**
   * - :math:`1\sigma`
     - 39%
     - 68%
     - 6 in 10
   * - :math:`2\sigma`
     - 86%
     - 95%
     - 1 in 7
   * - :math:`2.45\sigma`
     - 95%
     - 98.6%
     - 1 in 20
   * - :math:`3\sigma`
     - 98.9%
     - 99.7%
     - 1 in 90

A reading has **two directions to miss in**, so a circle holds less than the
1-D band of the same size.

Read the circles as a scale for how unusual a reading is. **Our sign match**
in the lecture's measurement model, 1.67 m off with :math:`\sigma = 1` m, is
:math:`1.67\sigma` out: 75% of readings land closer and 1 in 4 lands
farther, so it is **ordinary**. Outside :math:`2\sigma` (about 1 in 7) is
unusual. Outside :math:`3\sigma` (1 in 90), suspect the reading itself.

.. note::

   The NIS test in the lecture's Checking the Covariance section does the
   same thing properly: it compares each surprise with the size the filter
   expected for it.

Confidence Has Two Meanings
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The word **confidence** has a loose everyday meaning and a strict statistical
one, and they are **not the same**.

- **Loose.** How confident the system is: small covariance, confident; large
  covariance, uncertain. This is how most engineers and most code comments
  use the word, *including this course*. That is fine, as long as you know it
  is informal.
- **Strict.** A **confidence interval** is a range built from your data *by
  a stated recipe*. The **confidence level**, such as 95%, describes how
  often that recipe succeeds.

Let us build one from the six :math:`x` readings. Their mean is 100.0 m. The
step people get wrong: the interval is about how uncertain **the mean** is,
not how spread out one reading is. So it uses :math:`s/\sqrt{n}` for
:math:`n` readings, not :math:`s`:

.. math::

   \frac{s}{\sqrt{6}} = \frac{1.710}{\sqrt{6}} = 0.698\ \text{m}

and not the 1.561 m spread of the readings. The 95% recipe multiplies it by
2.571, the :math:`t` value for :math:`n - 1 = 5` degrees of freedom:

.. math::

   100.0 \pm 1.79\ \text{m}, \qquad \text{so } 98.21 \text{ to } 101.79\ \text{m}

.. note::

   The 1.710 is the spread computed with the :math:`n - 1` divisor, which is
   what these recipes assume. With six readings that choice moves the answer
   by about 10%.

What the 95% Interval Does Not Mean
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: The wrong sentence
   :class: danger

   "There is a 95% chance the true coordinate lies between 98.21 and
   101.79 m." It sounds completely reasonable. It is not what the interval
   says.

What it does say: imagine repeating the whole exercise many times. Park the
AV, take six readings, build an interval the same way. **About 95% of the
intervals built that way would contain the true coordinate.**

The claim is about **the recipe**, not about the one interval you are
holding. Your interval either contains the true coordinate or it does not;
no probability is left in it, you just do not know which. It is like a 95%
free-throw shooter: once a shot is taken, it went in or it did not. Here we
know the truth, 100.0 m, because it was surveyed. On the road you would not.

This is the most misread idea in applied statistics, and not only by
students. Because it is so easy to get wrong, the measurement standards
avoid the word entirely: the GUM and the VIM say **coverage interval** and
**coverage probability** instead, so nobody has to guess which meaning was
intended.


Kalman Filter in Detail
-----------------------

This section holds the Kalman filter material the class skips, in the order
it belongs: the four assumptions broken on a real AV, why no fixed matrix can
make a cosine, and the shared map error worked out.

On a Real Vehicle, All Four Assumptions Break
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The lecture's What We Assumed slide listed the four conditions under which
the Kalman filter is provably the best possible estimate. The figure takes
that theorem apart, one assumption per panel.

.. figure:: /_static/images/L3/assumptions.png
   :alt: Four panels, one per assumption, green for what the Kalman filter assumes and orange for what the AV does: a straight line against a curving path; a bell curve against sign-match errors with a second lump 25 m out; fresh errors centered on zero against a lingering IMU bias; a narrow reported uncertainty band against a true error that wanders outside it.
   :width: 90%
   :align: center

   Green is what the filter assumes; orange is what the AV does. **Top left,
   linear:** the filter's rule is a straight line (the matrix :math:`F`), but
   an AV that steers follows a curve, the cosine from the motion model.
   **Top right, bell curve:** most sign-match errors sit under the bell,
   about a meter either way, but now and then the camera misreads a sign and
   matches the next one, a lump 25 m out that a bell curve says almost never
   happens (an illustration, not measured data). **Bottom left, no bias, no
   memory:** the filter assumes fresh errors centered on zero (green dots);
   an IMU bias (orange line) sits near +1 m and lingers. **Bottom right,**
   :math:`Q` **and** :math:`R` **known:** :math:`Q` is guessed, here too
   small, so the filter reports a narrow band while the true error wanders
   far outside it.

Each panel breaks the theorem in its own way.

- **Linear.** A matrix cannot make a cosine (next subsection).
- **Bell curve.** A wrong sign match is 25 m wrong. The filter treats it as
  an error that almost never happens, and believes it.
- **No bias, no memory.** The filter counts the IMU's repeated errors as
  fresh evidence each time, and trusts that sensor far too much.
- **Q and R known.** Nobody knows :math:`Q`; it is chosen and tuned.

So the optimality proof applies to no filter that has ever shipped. That is
why the lecture spends its second half on the alternatives and on checking
the covariance.

No Fixed Matrix Can Make a Cosine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The lecture's "model is not linear" slide said no fixed matrix makes a
cosine. Here is why, in two pieces: where the cosine comes from, and what a
matrix can do.

.. figure:: /_static/images/L3/cosine_step.png
   :alt: East and north axes. A dark blue arrow from the origin, labeled v delta t, points 30 degrees above east, at angle theta. A dashed line drops from its tip to the east axis, and a thick orange segment along the east axis, labeled v delta t cos theta, is the part of the step that goes east.
   :width: 60%
   :align: center

   One step of the AV: it moves :math:`v\,\Delta t` along its heading
   :math:`\theta` (blue), and only the orange part,
   :math:`v\,\Delta t\cos\theta`, goes east.

**Where the cosine comes from.** In one step of :math:`\Delta t` seconds the
AV covers :math:`v\,\Delta t` (speed times time), along the direction it
points, at angle :math:`\theta` from east. The state stores east and north,
and only part of that trip goes east: one side of a right triangle whose
slanted side is :math:`v\,\Delta t`. Cosine is that side divided by the
slanted one, so the east part is :math:`v\,\Delta t\cos\theta`, and

.. math::

   x_k = x_{k-1} + v\,\Delta t\cos\theta.

**What a matrix can do.** A matrix can only scale and add. Each number
:math:`F\mathbf{x}` produces is fixed weights times the old numbers, added
up. So if one input doubles, its effect on the output doubles.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Heading** :math:`\theta`
     - :math:`\cos\theta`
   * - 0°
     - 1.00
   * - 30°
     - 0.87
   * - 60°
     - 0.50
   * - 90°
     - 0.00

Double :math:`\theta` from 30° to 60° and :math:`\cos\theta` does not
double: **it drops**, from 0.87 to 0.50, and at 90° it reaches zero. No
fixed weight does that.

.. important::

   You **can** put the number :math:`\cos\hat\theta`, taken at the current
   estimate, into a matrix. That is exactly the EKF's :math:`F_k`. But then
   the matrix changes every step, and it is right only near
   :math:`\hat\theta`. That is the tangent the EKF draws.

Fixing the Shared Map Error: One GNSS Fix at the Exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The lecture's shared-error slide showed that when the HD map puts every exit
sign 2 m too far along, the prediction and the sign match are **both** 2 m
too far, so the error does not average out: the combined answer is 52.4 m
instead of 50.4 m, while the filter reports :math:`\pm 0.89` m. To fix it,
we need a source that does not use the map (GNSS at the tunnel exit) and the
map's error in the **state**.

Add the map offset :math:`b` to the state, :math:`\mathbf{x} = [\,p,\ b\,]`.
A sign match sees :math:`p + b`. GNSS does not use the map, so it sees
:math:`p` alone. The truth is :math:`p = 50.4` m and :math:`b = +2` m.

.. list-table::
   :widths: 34 22 22 22
   :header-rows: 1
   :class: compact-table

   * -
     - **Position** :math:`p`
     - **Map offset** :math:`b`
     - **Correlation of** :math:`p` **and** :math:`b`
   * - Tunnel: the filter gives :math:`p + b = 52.4` (:math:`\sigma` 0.89)
     - 52.40 (:math:`\sigma` 2.19)
     - 0 (:math:`\sigma` 2, we chose)
     - -0.91
   * - GNSS at the exit: :math:`z = 50.5` (:math:`\sigma` 1), surprise -1.90
     - :math:`K = 0.83`
     - :math:`K = -0.69`
     -
   * - After the GNSS fix
     - **50.83** (:math:`\sigma` 0.91)
     - **1.31** (:math:`\sigma` 1.11)
     - -0.68

Read it row by row.

- **Inside the tunnel** the filter knows :math:`p + b` well,
  52.4 m with :math:`\sigma` 0.89 m, but cannot split it. With :math:`b`
  unknown (:math:`\sigma` 2 m, which we chose), the link between :math:`p`
  and :math:`b` is -0.91: too far along in :math:`p` goes with too small a
  :math:`b`.
- **At the exit**, GNSS reads 50.5 m with :math:`\sigma` 1 m. The surprise is
  -1.90 m. The gain is 0.83 for :math:`p` and -0.69 for :math:`b`: the link
  carries the correction into the map offset.
- **After one fix**, :math:`p` moves back by 1.57 m to 50.83 m, 0.43 m from
  the truth instead of 2 m, and :math:`b` moves up by 1.31 m, against a true
  2 m.

.. important::

   GNSS sees :math:`p` alone, yet its surprise moves **both** numbers,
   through the link between them. One fix leaves 0.43 m of the 2 m error.
   Every later sign match subtracts :math:`\hat{b} = 1.31` m, and each new
   GNSS fix refines it.


Motion Model in Detail
----------------------

In class we saw the motion model as one equation. Here it is built one piece
at a time: first the rule :math:`F`, then its error :math:`\mathbf{w}` and the
size of that error, :math:`Q`. Then the control input: the AV knows it braked,
and :math:`B\,\mathbf{u}` tells the rule. Then what is left in
:math:`\mathbf{w}`, and last, predict in two lines of code.

The Motion Rule F
~~~~~~~~~~~~~~~~~

One step ago the AV was at (100, 20) m, driving east at 10 m/s. One step is
:math:`\Delta t = 0.1` s (10 steps a second, 10 Hz, which we chose for this
example). The state has four numbers, and each row of :math:`F` updates one of
them.

.. list-table::
   :widths: 22 14 20 16 28
   :header-rows: 1
   :class: compact-table

   * - **State**
     - **One step ago**
     - **Row of** :math:`F`
     - **The rule**
     - **Now, with** :math:`\Delta t = 0.1` **s**
   * - :math:`p_x`, east position
     - 100 m
     - :math:`[\,1\ \ 0\ \ \Delta t\ \ 0\,]`
     - :math:`p_x + \Delta t\,v_x`
     - :math:`100 + 0.1 \times 10 =` **101** m
   * - :math:`p_y`, north position
     - 20 m
     - :math:`[\,0\ \ 1\ \ 0\ \ \Delta t\,]`
     - :math:`p_y + \Delta t\,v_y`
     - :math:`20 + 0.1 \times 0 = 20` m
   * - :math:`v_x`, east velocity
     - 10 m/s
     - :math:`[\,0\ \ 0\ \ 1\ \ 0\,]`
     - :math:`v_x`
     - 10 m/s
   * - :math:`v_y`, north velocity
     - 0 m/s
     - :math:`[\,0\ \ 0\ \ 0\ \ 1\,]`
     - :math:`v_y`
     - 0 m/s

The four columns of :math:`F` line up with the four state numbers, in order:
:math:`p_x`, :math:`p_y`, :math:`v_x`, :math:`v_y`. The first row is
1, 0, :math:`\Delta t`, 0: keep :math:`p_x`, and add :math:`\Delta t` times the
east speed. :math:`\Delta t` **multiplies a speed**, which gives a distance:
distance = speed × time. The second row does the same for north, but the north
speed is zero, so it stays at 20. The last two rows keep the speeds. The AV
moved one meter east and kept its speed. That is the whole motion rule.

The Motion Rule F as a Matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same step, written as :math:`\mathbf{x}_k = F\,\mathbf{x}_{k-1}`, the way
textbooks write it. Every row is one line of the table above. Rows and columns
are in the state's order :math:`p_x, p_y, v_x, v_y`.

.. math::

   \underbrace{\begin{bmatrix} \mathbf{101} \\ 20 \\ 10 \\ 0 \end{bmatrix}}_{\text{now, } \mathbf{x}_k}
   \;=\;
   \underbrace{\begin{bmatrix}
     \mathbf{1} & \mathbf{0} & \mathbf{0.1} & \mathbf{0} \\
     0 & 1 & 0 & 0.1 \\
     0 & 0 & 1 & 0 \\
     0 & 0 & 0 & 1
   \end{bmatrix}}_{F \text{ with } \Delta t = 0.1\,\text{s}}
   \;
   \underbrace{\begin{bmatrix} 100 \\ 20 \\ 10 \\ 0 \end{bmatrix}}_{\text{one step ago, } \mathbf{x}_{k-1}}

Multiply out the bold first row: each entry times the state number in the
matching position, then add.

.. math::

   1 \times 100 \;+\; 0 \times 20 \;+\; 0.1 \times 10 \;+\; 0 \times 0 \;=\; \mathbf{101}

That is "position plus a tenth of a second of speed", written as one row. The
other rows work the same way. Notice what is missing: the
:math:`+\,\mathbf{w}`. This is only what the rule says. The next subsection
shows what really happened.

The Rule's Error w in One Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The rule assumed constant speed. But the AV **braked gently** for a slower car
ahead, at 1 m/s² (which we chose for this example): its speed drops by 1 m/s
every second. This simple rule **ignores the IMU**, so to the rule the brake is
an error.

.. list-table::
   :widths: 28 24 20 28
   :header-rows: 1
   :class: compact-table

   * - **State**
     - **Predicted,** :math:`F\mathbf{x}_{k-1}`
     - **True state**
     - :math:`\mathbf{w}` **= true minus predicted**
   * - :math:`p_x`, east position
     - 101 m
     - 100.995 m
     - **-0.005 m**
   * - :math:`p_y`, north position
     - 20 m
     - 20 m
     - 0
   * - :math:`v_x`, east velocity
     - 10 m/s
     - 9.9 m/s
     - **-0.1 m/s**
   * - :math:`v_y`, north velocity
     - 0 m/s
     - 0 m/s
     - 0

**Where the true state comes from**, braking at :math:`a = 1` m/s² for
:math:`\Delta t = 0.1` s:

- **Speed** drops by :math:`a\,\Delta t = 1 \times 0.1 = 0.1` m/s, to 9.9 m/s.
- **Position:** the speed fell steadily from 10 to 9.9, so it **averaged
  9.95 m/s**, and the AV went :math:`9.95 \times 0.1 = 0.995` m, not 1 m. It is
  short by 0.005 m, which is :math:`\tfrac{1}{2}a\,\Delta t^2`.

We know the true state only because we set up the example. The four
differences in the last column, together, are :math:`\mathbf{w}`, the rule's
error this step.

.. important::

   **The AV cannot measure** :math:`\mathbf{w}`: it would need its true
   position, which is exactly what it does not know. It only feels
   :math:`\mathbf{w}` later, when a sensor reading disagrees with what the
   filter expected.

Q Is the Size of Error the Filter Expects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`Q` says how big an error the filter should expect the rule to make.
That is its whole job. Here :math:`Q` is set for an AV that brakes or speeds
up by about 1 m/s², a gentle, everyday change. Its diagonal holds the typical
size of each part of :math:`\mathbf{w}`, squared.

.. list-table::
   :widths: 16 28 24 32
   :header-rows: 1
   :class: compact-table

   * - **State**
     - :math:`Q` **diagonal**
     - **Typical size**
     - **This step's** :math:`\mathbf{w}`
   * - :math:`p_x`
     - 0.000025 m²
     - 0.005 m
     - -0.005 m
   * - :math:`p_y`
     - 0.000025 m²
     - 0.005 m
     - 0
   * - :math:`v_x`
     - 0.01 (m/s)²
     - 0.1 m/s
     - -0.1 m/s
   * - :math:`v_y`
     - 0.01 (m/s)²
     - 0.1 m/s
     - 0

Compare the typical sizes with this step's actual :math:`\mathbf{w}`: they are
the same, so **this brake is exactly a normal-sized error**, and the filter
will not be surprised by it.

.. warning::

   Set :math:`Q` **too small** and the filter thinks the rule is nearly
   perfect, so an ordinary brake looks impossible. It becomes overconfident,
   which is the dangerous direction. Set it **too big** and the filter doubts
   its own rule so much that it chases every noisy reading. Nobody can measure
   :math:`Q`, so you choose it, then tune it.

The Typical Sizes in Q Come From the Acceleration Sigma
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The numbers above come from one assumption: the AV's speed can change without
warning by about :math:`\sigma_a = 1` m/s², which we chose. Everything else is
arithmetic. Over one step, an unexpected acceleration :math:`a` does two
things.

.. list-table::
   :widths: 18 22 28 32
   :header-rows: 1
   :class: compact-table

   * - **Part of** :math:`\mathbf{w}`
     - **It changes by**
     - **Typical size**
     - **Squared:** :math:`Q` **diagonal**
   * - speed
     - :math:`\Delta t\,a`
     - :math:`0.1 \times 1 =` **0.1** m/s
     - :math:`0.1^2 = 0.01` (m/s)²
   * - position
     - :math:`\tfrac{1}{2}\Delta t^2 a`
     - :math:`0.005 \times 1 =` **0.005** m
     - :math:`0.005^2 = 0.000025` m²

.. note::

   **Why square?** :math:`Q` is a covariance, and a covariance stores sizes
   *squared*, like :math:`\sigma^2`. Take the square root to get back a size
   you can picture.

The Whole Covariance Matrix Q
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is all of :math:`Q`, with rows and columns in the state's order
:math:`p_x, p_y, v_x, v_y`.

.. math::

   Q \;=\;
   \begin{bmatrix}
     \mathbf{0.000025} & 0 & 0.0005 & 0 \\
     0 & \mathbf{0.000025} & 0 & 0.0005 \\
     0.0005 & 0 & \mathbf{0.01} & 0 \\
     0 & 0.0005 & 0 & \mathbf{0.01}
   \end{bmatrix}

- **The diagonal** (bold): the typical size of each part of
  :math:`\mathbf{w}`, squared, from the last subsection.
- **0.0005** (row :math:`p_x`, column :math:`v_x`, and its mirror) is
  :math:`0.005 \times 0.1`, the typical position error times the typical speed
  error. It is **positive** because one surprise brake makes **both** errors
  at once, the same way: the AV is slower *and* behind. So if the position is
  off, the speed is off too, in the same direction. Not two separate
  accidents.
- **The zeros** (wherever an east number meets a north number, for example
  row :math:`p_x`, column :math:`p_y`): east and north errors are
  **unrelated**. Braking along the tunnel says nothing about drifting
  sideways. Zero covariance means no link.

Telling the Rule About the Brake With B u
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AV knows it braked, because the IMU measured it. So we move the brake out
of the error and into the prediction, by adding one term:

.. math::

   \mathbf{x}_k \;=\; F\,\mathbf{x}_{k-1} \;+\;
   \underbrace{B\,\mathbf{u}_k}_{\text{what the AV knows it did}} \;+\; \mathbf{w}

**Before**, the brake was part of :math:`\mathbf{w}`, because the rule did not
know about it. **Now** the IMU measured it, so it moves into
:math:`B\,\mathbf{u}_k`, and :math:`\mathbf{w}` keeps only what is still
unknown.

- :math:`\mathbf{u}_k` **is the control input**: what the AV knows it did this
  step. Here, the acceleration the IMU measures,
  :math:`\mathbf{u} = [\,a_x,\ a_y\,]`.
- :math:`B` **turns** :math:`\mathbf{u}` **into changes of the state.**
  Accelerating at :math:`a` for :math:`\Delta t` adds :math:`\Delta t\,a` to
  the velocity and :math:`\tfrac{1}{2}\Delta t^2 a` to the position: with
  :math:`\Delta t = 0.1` s, :math:`0.1\,a` and :math:`0.005\,a`. That is the
  same physics we used for the true-state column.
- :math:`\mathbf{w}` **now only covers what the AV cannot know:** IMU noise,
  tire slip, a small slope. So :math:`Q` can be smaller: the lecture's
  hands-on uses :math:`\sigma_a = 0.5` m/s² (we chose it) instead of 1.

The EKF later uses the same idea: its control input is the speed and turn rate
from the wheel encoders and the IMU.

With the Brake Fed In, the Rule Lands on the True State
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The IMU measures the brake: :math:`\mathbf{u} = [\,-1,\ 0\,]` m/s². With
:math:`\Delta t = 0.1` s, :math:`B` multiplies each acceleration by
:math:`\tfrac{1}{2}\Delta t^2 = 0.005` for a position, or by
:math:`\Delta t = 0.1` for a velocity.

.. list-table::
   :widths: 12 18 30 20 20
   :header-rows: 1
   :class: compact-table

   * - **State**
     - :math:`F\,\mathbf{x}_{k-1}`
     - :math:`B\,\mathbf{u}`
     - **Sum**
     - **True state**
   * - :math:`p_x`
     - 101 m
     - :math:`0.005 \times (-1) = -0.005`
     - **100.995 m**
     - 100.995 m
   * - :math:`p_y`
     - 20 m
     - 0
     - 20 m
     - 20 m
   * - :math:`v_x`
     - 10 m/s
     - :math:`0.1 \times (-1) = -0.1`
     - **9.9 m/s**
     - 9.9 m/s
   * - :math:`v_y`
     - 0 m/s
     - 0
     - 0 m/s
     - 0 m/s

**The prediction now lands on the true state**, and not by chance: :math:`B`
uses the same physics we used for the true state, and here the IMU read the
brake **exactly**, -1 m/s². Same formula, same number in, same answer out. A
real IMU might read -1.03; then the prediction lands close but not exactly,
and that small miss is what stays in :math:`\mathbf{w}`.

Brake in w Against Brake in B u
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same brake, 1 m/s², same step, :math:`\Delta t = 0.1` s. The true state after
one step is 100.995 m and 9.9 m/s.

.. list-table::
   :widths: 34 33 33
   :header-rows: 1
   :class: compact-table

   * -
     - **Brake in** :math:`\mathbf{w}`: :math:`F\mathbf{x}_{k-1}`
     - **Brake out of** :math:`\mathbf{w}`: :math:`F\mathbf{x}_{k-1} + B\,\mathbf{u}`
   * - Predicted :math:`p_x`, one step
     - 101 m
     - **100.995 m**
   * - Predicted :math:`v_x`, one step
     - 10 m/s
     - **9.9 m/s**
   * - :math:`\mathbf{w}` this step (:math:`p_x`, :math:`v_x`)
     - -0.005 m, -0.1 m/s
     - 0, 0
   * - Off after 1 s of braking (:math:`p_x`, :math:`v_x`)
     - 0.5 m, 1 m/s
     - 0, 0
   * - :math:`Q` has to cover
     - every brake and speed-up
     - only what the IMU misses
   * - Hands-on: RMS error along the tunnel
     - 3.58 m
     - **1.06 m**

One step looks small, but it adds up. Brake for one full second and the left
column is off by half a meter and 1 m/s (:math:`\tfrac{1}{2}at^2` and
:math:`at` with :math:`t = 1` s), while the right column is still on the true
state. On the left, :math:`Q` must cover every brake and speed-up, so the
filter is uncertain all the time; on the right, it only covers what the IMU
gets wrong.

.. important::

   Same filter, same data. Feeding the brake in through :math:`B\,\mathbf{u}`
   makes the prediction **right**, not just more uncertain, and lets
   :math:`Q` stay **small**. In the hands-on, removing it (the
   ``--no-control`` option of ``kf_tunnel.py``) takes the error along the
   tunnel from 1.06 m to 3.58 m.

What Is Left in w Is the IMU's Own Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same step: :math:`\Delta t = 0.1` s, the AV braking at -1 m/s². North stays 0
in every row.

.. list-table::
   :widths: 50 25 25
   :header-rows: 1
   :class: compact-table

   * - :math:`\mathbf{w}`
     - **east position**
     - **east velocity**
   * - the brake still in :math:`\mathbf{w}`
     - -0.005 m
     - -0.1 m/s
   * - after :math:`B\,\mathbf{u}`, a perfect IMU
     - 0
     - 0
   * - after :math:`B\,\mathbf{u}`, the script's IMU at :math:`t = 11` s
     - +0.00125 m
     - +0.025 m/s

- **First row:** the rule does not know the AV is braking, so every step it
  puts the AV 5 mm too far along and 0.1 m/s too fast. Both numbers are
  negative because :math:`\mathbf{w}` is true minus model.
- **Second row:** with a perfect IMU, :math:`B\,\mathbf{u}` predicts the brake
  exactly and :math:`\mathbf{w}` is zero.
- **Third row**, from the hands-on script: at 11 s the IMU reads -1.25, but
  the AV really brakes at -1.00. The true and predicted states differ only in
  that number, and everything else cancels:

.. math::

   \mathbf{w} \;=\; \text{true} - \text{predicted}
   \;=\; \bigl(F\mathbf{x}_{k-1} + B \times (-1.00)\bigr) - \bigl(F\mathbf{x}_{k-1} + B \times (-1.25)\bigr)
   \;=\; B \times 0.25

That is :math:`0.005 \times 0.25 = 0.00125` m in position and
:math:`0.1 \times 0.25 = 0.025` m/s in speed.

.. important::

   Two things changed. **Size:** 0.1 m/s became 0.025 m/s, four times
   smaller. **Direction:** the brake made the rule wrong the same way every
   step, ten times a second, so the errors piled up. The IMU's misreading
   changes direction from step to step: at 10.9, 11.0 and 11.1 s it reads
   -0.77, -1.25 and -0.55 against a true -1.00, so errors in both directions
   partly cancel. That is what :math:`\mathbf{w}` should be: centered on zero.
   Smaller and centered on zero is why :math:`Q` can shrink.

Beyond Braking, the Formula Stays the Same
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AV does more than brake, and the formula does not change:

.. math::

   \mathbf{x}_k \;=\; F\,\mathbf{x}_{k-1} + B\,\mathbf{u}_k + \mathbf{w}

- **The IMU measures all acceleration**, whatever causes it: brake,
  throttle, bumps. One :math:`\mathbf{u}` covers them all.
- **Several known inputs are stacked:** :math:`\mathbf{u} = [\,u_1,\ u_2\,]`,
  one column of :math:`B` each, so :math:`B\,\mathbf{u} = B_1 u_1 + B_2 u_2`.
- **Anything not measured stays in** :math:`\mathbf{w}`: IMU noise and bias,
  tire slip, wind, a slope. A slope is sneaky: on a slope the accelerometer
  reads part of gravity. And if you feed in the planner's commanded
  acceleration instead of the measured one, the gap between commanded and
  actual goes into :math:`\mathbf{w}` too.
- **Turning is the exception.** The IMU measures in the AV's own frame,
  forward and sideways. Turning that into east and north needs the heading, a
  cosine and a sine, and then the model is no longer a matrix. That is the
  problem the **EKF** handles, with :math:`\mathbf{u}` equal to speed and turn
  rate.

Predict in Code Is Two Lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These two lines are the predicted-state and predicted-uncertainty equations
from the lecture.

.. code-block:: python

   x = F @ x + B @ u      # predicted state: rule + what the AV did
   P = F @ P @ F.T + Q    # uncertainty: w enters only as Q

In Python with NumPy, ``@`` is **matrix multiplication** (rows times columns,
the way you multiply matrices by hand) and ``.T`` is the **transpose**. So
``F @ x`` is :math:`F\mathbf{x}`, and ``F @ P @ F.T`` is :math:`FPF^\top`. A
plain ``*`` would multiply entry by entry, which is not what the equation
says.

.. important::

   :math:`+\,B\,\mathbf{u}` **must be written in the code.** Leave it out and
   the brake falls back into :math:`\mathbf{w}`: in the hands-on, the error
   along the tunnel more than triples, from about 1 m to 3.5 m.

   :math:`\mathbf{w}` **never appears.** Its average, zero, adds nothing to
   the predicted state; its size goes in as :math:`Q`.


Measurement Model in Detail
---------------------------

This section builds the measurement model one piece at a time, on the same
example: the reading the sign match should give if our prediction is right,
the matrix :math:`H` that picks those numbers out of the state, the error
:math:`\mathbf{v}` and the surprise, and :math:`R`, how big that error usually
is.

The Expected Reading for the Predicted State
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The motion model predicted (100.995, 20) m, doing 9.9 m/s east. The sign match
gives only two numbers, an east position and a north position. Each row of
:math:`H` makes one.

.. list-table::
   :widths: 28 28 16 28
   :header-rows: 1
   :class: compact-table

   * - **Reading**
     - **Row of** :math:`H`
     - **The rule**
     - **Expected reading**
   * - :math:`z_x`, east position
     - :math:`[\,1\ \ 0\ \ 0\ \ 0\,]`
     - :math:`p_x`
     - **100.995 m**
   * - :math:`z_y`, north position
     - :math:`[\,0\ \ 1\ \ 0\ \ 0\,]`
     - :math:`p_y`
     - **20 m**

The four columns of :math:`H` line up with the state: :math:`p_x`,
:math:`p_y`, :math:`v_x`, :math:`v_y`. The 1 keeps a position. The zeros drop
the velocities, because a sign match does not measure velocity. No
arithmetic, no time: :math:`H` just picks.

The Measurement Matrix H
~~~~~~~~~~~~~~~~~~~~~~~~

The same step as a matrix, written as :math:`H\,\hat{\mathbf{x}}^-`, the
expected reading. The columns of :math:`H` are the four state numbers; its
rows are the two readings :math:`z_x` and :math:`z_y`.

.. math::

   \underbrace{\begin{bmatrix} \mathbf{100.995} \\ 20 \end{bmatrix}}_{\text{expected reading}}
   \;=\;
   \underbrace{\begin{bmatrix}
     \mathbf{1} & \mathbf{0} & \mathbf{0} & \mathbf{0} \\
     0 & 1 & 0 & 0
   \end{bmatrix}}_{H}
   \;
   \underbrace{\begin{bmatrix} 100.995 \\ 20 \\ 9.9 \\ 0 \end{bmatrix}}_{\text{predicted state, } \hat{\mathbf{x}}^-}

The first row, multiplied out:

.. math::

   1 \times 100.995 \;+\; 0 \times 20 \;+\; 0 \times 9.9 \;+\; 0 \times 0 \;=\; \mathbf{100.995}

Notice the shape. :math:`F` was 4 by 4: four numbers in, four out. :math:`H`
is **2 by 4**: four state numbers in, two readings out. The shape of
:math:`H` tells you what the sensor can see.

The Sign Match's Error This Time, v
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The sign match gives :math:`\mathbf{z}_k = (102.4,\ 19.1)` m. Compare it with
the **true position**, the ground truth.

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1
   :class: compact-table

   * - **Reading**
     - **Measured,** :math:`\mathbf{z}`
     - **True,** :math:`H\mathbf{x}`
     - :math:`\mathbf{v}` **= measured minus true**
   * - :math:`z_x`, east
     - 102.4 m
     - 100.995 m
     - **1.405 m**
   * - :math:`z_y`, north
     - 19.1 m
     - 20 m
     - **-0.9 m**

- **Measured,** :math:`\mathbf{z}`: what the sign match reports. These two
  numbers are **chosen for this example**; the hands-on CSV has real ones.
- **True,** :math:`H\mathbf{x}`: the true state
  :math:`[100.995,\ 20,\ 9.9,\ 0]` from the braking example in the motion
  model, pushed through :math:`H`: keep :math:`p_x` and :math:`p_y`, drop the
  velocities.
- :math:`\mathbf{v}`: subtract row by row, :math:`102.4 - 100.995 = 1.405`
  and :math:`19.1 - 20 = -0.9`. Those two numbers are the sensor's error this
  time.

The same catch as with :math:`\mathbf{w}`: **the AV cannot compute this
table**, because the true column is the ground truth. What it *can* compute is
the **surprise**.

The Surprise Is Measured Minus Expected
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: surprise
   :class: important

   The reading we got minus the reading we expected. Its textbook name is the
   **innovation**, written :math:`\nu` (the Greek letter nu):

   .. math::

      \nu = \mathbf{z} - H\hat{\mathbf{x}}^-

   With one number it was :math:`z - \hat{x}^-`; :math:`H` turns the state
   into a reading.

.. list-table::
   :widths: 34 22 22 22
   :header-rows: 1
   :class: compact-table

   * -
     - **Measured,** :math:`\mathbf{z}`
     - **Expected,** :math:`H\hat{\mathbf{x}}^-`
     - **Surprise,** :math:`\nu`
   * - worked example, east
     - 102.4 m
     - 100.995 m
     - **1.405 m**
   * - worked example, north
     - 19.1 m
     - 20 m
     - **-0.9 m**
   * - hands-on, :math:`t = 9.3` s, along
     - 111.15 m
     - 110.41 m
     - **0.74 m**
   * - hands-on, :math:`t = 9.3` s, across
     - -1.95 m
     - -2.09 m
     - **0.14 m**

In the worked example **the surprise equals** :math:`\mathbf{v}`, because
there the prediction *is* the true state: we started from the true state, fed
the brake in through :math:`B\,\mathbf{u}`, and the IMU was perfect. The
hands-on has no such luxury.

.. important::

   **No ground truth is needed:** the filter always has :math:`\mathbf{z}` and
   :math:`\hat{\mathbf{x}}^-`. **But the surprise mixes two errors.** The
   script knows the truth, so we can split the hands-on's 0.74 m: about
   0.39 m is the sign match's own error, :math:`\mathbf{v}`, and 0.34 m is the
   prediction's error. The filter cannot split them from one reading.
   Weighing them is the gain's job.

R Is the Size of Error to Expect From the Sign Match
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We did this for :math:`Q`; now the sensor gets the same treatment. In this
worked example the sign match has :math:`\sigma = 1` m on each axis (the
hands-on uses 1 m along the tunnel and 0.2 m across). :math:`R` holds it,
squared, because :math:`R` is a covariance.

.. list-table::
   :widths: 16 22 30 32
   :header-rows: 1
   :class: compact-table

   * - **Reading**
     - **Typical size**
     - **Squared:** :math:`R` **diagonal**
     - **This time's** :math:`\mathbf{v}`
   * - :math:`z_x`
     - 1 m
     - :math:`1^2 = 1` m²
     - 1.405 m
   * - :math:`z_y`
     - 1 m
     - :math:`1^2 = 1` m²
     - -0.9 m

.. important::

   **Unlike** :math:`Q`, :math:`R` **can be measured.** :math:`Q` says how
   wrong our model is, and if we knew that, we would use a better model. For
   :math:`R`, drive a surveyed tunnel, compare each sign match with the known
   true position, and compute the spread. That spread is :math:`\sigma`.

This time's errors, 1.405 m and -0.9 m, are both **within about
1.5** :math:`\sigma`: ordinary noise. A 10 m error would not be, and the
lecture comes back to that with gating.

The Whole of R, a Covariance Matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rows and columns are the two readings, :math:`z_x` and :math:`z_y`.

.. math::

   R \;=\; \begin{bmatrix} \mathbf{1} & 0 \\ 0 & \mathbf{1} \end{bmatrix}

- **The diagonal** (bold): each reading's typical error, squared.
- **The zeros:** the east error and the north error are assumed
  **unrelated**: knowing the sign match is off to the east says nothing about
  north. That is an assumption. For a real sensor it is only roughly true, but
  it is the usual starting point.
- :math:`R` **is 2 by 2**, one row and column per reading. :math:`Q` was 4 by
  4, one per state number. Each covariance matches the thing it describes.


Kalman Filter Hands-On Files
----------------------------

This is a hands-on to do at home: the same tunnel filter as in class, on your
own laptop. The steps to run and explore it are in the lecture's Hands-On
subsection; this section walks through the files one by one. The scripts need
only ``numpy`` and ``matplotlib`` (plus ``python3-tk`` for the live window).

.. code-block:: bash

   cd enpm818z-fall-2026-carla-python/lecture3/tunnel_kf
   python3 kf_tunnel.py --make-csv                        # the data
   python3 kf_tunnel.py tunnel_drive.csv                  # the live window
   python3 kf_tunnel.py tunnel_drive.csv --html kf.html   # no desktop? a web page

The CSV, tunnel_drive.csv
~~~~~~~~~~~~~~~~~~~~~~~~~

The script writes the CSV with a fixed random seed, so everyone gets the same
drive. The AV cruises, brakes from 8 to 12 s, and speeds up again from 20 to
24 s.

.. list-table::
   :widths: 30 46 24
   :header-rows: 1
   :class: compact-table

   * - **Columns**
     - **What they hold**
     - **Filter uses it as**
   * - ``t``
     - time, one row every 0.1 s
     - :math:`\Delta t`
   * - ``imu_ax``, ``imu_ay``
     - IMU acceleration (m/s²), noise 0.3 and a bias of 0.05 along the tunnel
     - the control input :math:`\mathbf{u}`
   * - ``sign_x``, ``sign_y``, ``sign_id``
     - a sign match (m): :math:`\sigma` 1 m along, 0.2 m across; **empty on
       432 of 451 rows**
     - the measurement :math:`\mathbf{z}`
   * - ``true_x`` to ``true_vy``
     - the true position and speed
     - **nothing**: scoring only

The sign columns are empty on most rows because a sign only comes into view
every couple of seconds. Open the file and read two rows. At time zero no sign
is in view, so the sign columns are empty. At 0.9 s, sign number one is
matched: the camera says 10.537 m, while the AV is truly at 10.8 m. That
quarter-meter gap is the sign match's error, :math:`\mathbf{v}`.

The Script, kf_tunnel.py
~~~~~~~~~~~~~~~~~~~~~~~~

One file, in five parts. Only one of them is the Kalman filter.

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Part**
     - **What it does**
   * - constants at the top
     - :math:`\Delta t = 0.1` s, a sign every 25 m, the brake, and the sign
       match's 0.2 m across
   * - ``make_csv()``
     - simulates the drive and writes ``tunnel_drive.csv``
   * - ``load_csv()``
     - reads the CSV into one array per column
   * - ``run_kf()``
     - **the Kalman filter**: builds :math:`F`, :math:`B`, :math:`Q`,
       :math:`H`, :math:`R`, then runs predict and update over every row
   * - ``build_figure()``, ``main()``
     - the live window with its sliders, and the command-line options

.. tip::

   **Read** ``run_kf()`` **first**; everything else is data and drawing, so
   skip it the first time. Every line in ``run_kf()`` is an equation from the
   lecture.

The Filter, run_kf()
~~~~~~~~~~~~~~~~~~~~

Here is the heart of the script, simplified to fit on one screen.

.. code-block:: python

   for k in range(n):                        # one pass per CSV row
       if k > 0:                             # PREDICT, on every row
           u = [imu_ax[k-1], imu_ay[k-1]]    # the IMU: control input u
           x = F @ x + B @ u                 # predicted state
           P = F @ P @ F.T + Q               # predicted uncertainty
       if sign_x[k] is not empty:            # UPDATE, only on 19 rows
           z = [sign_x[k], sign_y[k]]        # the sign match
           nu = z - H @ x                    # the surprise
           S = H @ P @ H.T + R               # its expected size
           K = P @ H.T @ inv(S)              # the gain
           x = x + K @ nu                    # new estimate
           P = (I - K @ H) @ P               # new uncertainty

- **One pass per row.** On every row we predict: the IMU reading is the
  control input :math:`\mathbf{u}`, then two lines give the predicted state
  and the predicted uncertainty, line for line as in the lecture.
- **Only if the row has a sign match**, 19 rows out of 451, we update: the
  surprise, its expected size :math:`S`, the gain :math:`K`, the new estimate,
  and the new uncertainty, in the same order as the lecture's update.
- **Before the loop**, the function builds :math:`F`, :math:`B` and :math:`H`
  once. It builds :math:`Q` and :math:`R` from the two sliders
  (``--sigma-a``, default 0.5 m/s², and ``--sigma-sign``, default 1 m, both
  values we chose), and starts from the belief handed over at the tunnel
  entrance.

That is the whole Kalman filter: about ten lines inside a loop.


UKF in Detail
-------------

The lecture names the unscented Kalman filter (UKF) as the second of three
alternatives to the plain Kalman filter, and skips its details. This section
works it out with real numbers: the idea, the drive with five points, how far
out the points go and how much each counts, the full recipe, the update, the
code and the traps, a check, and a hands-on that puts the UKF next to the
EKF.

Keep the Curve, Swap the Bell Curve for Points
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Alternative 2 of 3.** The EKF fakes a straight line, and misses the bend
when the uncertainty is wide.

- **In this section:** the **UKF**. Keep the real curve, and swap the bell
  curve for a few points.
- **What it is for:** a wide :math:`P`, and models that are only code. Its
  cost is :math:`2n+1` calls to the model per step.

**The idea.** Skip the slope. Try a few **what-ifs**. Take the AV from the
lecture's banana example: :math:`20 \pm 0.5` m out, heading
:math:`0 \pm 12°`. What if the heading is 21° off, left or right? What if the
AV went 0.9 m farther? Drive each one with the **real** model, and see where
it lands. The spread of the landing spots is the new uncertainty. (The 21°
and the 0.9 m are the UKF's step sizes for this example; they are worked out
below.)

.. admonition:: Definition: unscented Kalman filter (UKF)
   :class: important

   A Kalman filter for curved models that **needs no tangents**. It pushes a
   few chosen points through the **real** function and rebuilds the mean and
   covariance from where they land.

Why not just keep the EKF? A tangent is only good near where you drew it. When
:math:`P` is wide, after a long stretch with no sign match or in a hard turn,
the curve bends across the area that matters, and one tangent gets it wrong.
Some models also come as somebody else's code, with no formula to take a slope
of. The cost is :math:`2n+1` calls to the model per step, where :math:`n` is
how many numbers are in the state. There is no Jacobian of :math:`f` or
:math:`h`; only :math:`Q_k` still uses :math:`G`, as in the EKF.

EKF Against UKF: Where Each One Cheats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both filters must turn "a bell curve pushed through a curve" back into a bell
curve. A bell curve goes in, something lopsided comes out, and both have to
cheat to get a bell curve back. They cheat in **opposite** places.

.. figure:: /_static/images/L3/ukf_story_1_idea.png
   :alt: Two panels on the curve x equals 20 cos theta with a blue heading bell centered at 30 degrees. Left, EKF: an orange tangent at 30 degrees stands in for the faded curve, and the whole bell is kept. Right, UKF: the real curve is bold, and the bell is replaced by three green points at about 9, 30 and 51 degrees, weighted 1/6, 2/3 and 1/6, each going up to the real curve.
   :width: 90%
   :align: center

   The same example in both panels: :math:`x = 20\cos\theta`, with the
   heading belief (blue bell, centered at 30°) along the bottom. **Left, EKF
   (orange):** it keeps the bell exactly and swaps the curve for its tangent
   at 30°. Near 30° that is fine; far out in the bell's tails, the line and
   the curve disagree. **Right, UKF (green):** it keeps the real curve and
   swaps the bell for three points, the middle and one step out on each side,
   weighted 2/3, 1/6 and 1/6. Each point goes through the real curve, so
   nothing about the bend is lost.

.. important::

   **EKF:** keeps the bell curve, swaps the curve for its tangent.
   **UKF:** keeps the **real** curve, swaps the bell curve for :math:`2n+1`
   weighted points. The EKF approximates the function; the UKF approximates
   the belief.

The Mean Comes Out Right
~~~~~~~~~~~~~~~~~~~~~~~~

Now the numbers for that picture: which cheat costs less? It is the same curve
as the lecture's EKF picture, 20 m driven with heading :math:`30 \pm 12°`.

.. figure:: /_static/images/L3/bell_3_ekf.png
   :alt: The EKF panel: the curve 20 cos theta with its dashed orange tangent at 30 degrees, and a dashed orange output bell centered on 17.32 m over the gray lopsided histogram of the true output. EKF 17.32 plus or minus 2.09 m, true 16.95 plus or minus 2.11 m.
   :width: 60%
   :align: center

   **EKF:** one tangent at 30° gives an output bell (dashed orange) at
   :math:`17.32 \pm 2.09` m. The gray histogram is the true, lopsided output.
   The width is close, but the mean is 0.37 m too far, because a tangent
   cannot see the bend.

.. figure:: /_static/images/L3/bell_4_ukf.png
   :alt: The UKF panel: three green points on the input bell at 9.2, 30 and 50.8 degrees, weighted 1/6, 2/3 and 1/6, go up to the real curve and land at 19.74, 17.32 and 12.64 m. A green bell fitted to them is centered on 16.94 m over the gray true histogram. UKF 16.94 plus or minus 2.12 m, true 16.95 plus or minus 2.11 m.
   :width: 60%
   :align: center

   **UKF:** three points on the input bell, at 9.2°, 30° and 50.8°, go up to
   the real curve and across. They land at 19.74, 17.32 and 12.64 m. The
   green bell fitted to them is :math:`16.94 \pm 2.12` m.

Average the three landing spots with the weights: two thirds for the middle,
a sixth for each of the others. That gives 16.94 m, and their weighted spread
gives :math:`\pm 2.12` m. The truth, from 400,000 samples, is
:math:`16.95 \pm 2.11` m. Three calls to the function, and the mean is right
to a centimeter.

Sigma Points Stand In for the Bell Curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: sigma points
   :class: important

   :math:`2n+1` points whose **weighted average is the mean** and whose
   **weighted spread is the covariance**. :math:`n` is the size of the state
   (Julier and Uhlmann, 1997).

They are a small, fixed set that stands in for the whole bell curve. Three
cases come up in this lecture.

.. list-table::
   :widths: 50 25 25
   :header-rows: 1
   :class: compact-table

   * - **Where**
     - **State**
     - **Points**
   * - the picture above
     - :math:`\theta`
     - :math:`n = 1`: 3
   * - the drive below
     - :math:`d`, :math:`\theta`
     - :math:`n = 2`: 5
   * - the curved-tunnel hands-on
     - :math:`x`, :math:`y`, :math:`\theta`
     - :math:`n = 3`: 7

Seven calls to the model per step is cheap.

Place, Push, Rebuild: The Drive in Pictures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AV drives :math:`20 \pm 0.5` m with its heading known to :math:`\pm 12°`.
Two numbers in the state, distance and heading, so :math:`n = 2` and **five
sigma points**.

.. figure:: /_static/images/L3/ukf_story_2_drive.png
   :alt: Three panels. 1, place: heading against distance driven, a blue ellipse with five green points, chi 0 at the center weighted 1/3 and chi 1 to chi 4 one step out along each axis weighted 1/6. 2, push through the real f: east against north, a gray banana-shaped cloud of 4,000 possible AVs around 20 m east, with the five points landing on it. 3, rebuild a bell: a green UKF ellipse centered at 19.57 m and a dashed orange EKF ellipse centered at 20.00 m over the cloud.
   :width: 95%
   :align: center

   **1, place:** the middle point :math:`\chi_0` is the estimate itself,
   weighted 1/3. The other four, weighted 1/6 each, are one step out and one
   step back along each direction: :math:`\chi_1` and :math:`\chi_3` about
   0.9 m farther and shorter (20.9 and 19.1 m), :math:`\chi_2` and
   :math:`\chi_4` about 21° right and left. **2, push through the real**
   :math:`f`: each point goes through the real motion model, cosine and sine
   and all. The gray cloud is 4,000 possible AVs, the real banana. The two
   turned points land short of 20 m and about 7 m to the sides, right on the
   banana's arms. **3, rebuild a bell:** the weighted average of the five
   landing spots is 19.57 m (green); the truth is 19.57 m; the EKF's tangent
   says 20.00 m (dashed orange).

.. important::

   **Five calls to the real model see the bend** that one tangent misses: the
   banana pulls the mean short. UKF 19.57 m, true 19.57 m, EKF 20.00 m. The
   UKF's spread along the drive is 0.79 m against a true 0.78 m; the EKF says
   0.5 m.

Place, Push, Rebuild as Equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same three steps, written so you could code them.

1. **Place** :math:`2n+1` sigma points :math:`\chi_i`: the mean, plus one step
   out and one step back along each of :math:`n` directions. Point :math:`i`
   gets a weight :math:`W_i`; the weights add to 1.

2. **Push** each one through the real motion model :math:`f`.
   :math:`\mathcal{Y}_i` is where it lands. No derivatives anywhere:

   .. math::

      \mathcal{Y}_i = f(\chi_i, \mathbf{u})

3. **Rebuild** the prediction from where they land:

   .. math::

      \hat{\mathbf{x}}^- = \sum_i W_i\,\mathcal{Y}_i
      \qquad
      P^- = \sum_i W_i\,(\mathcal{Y}_i - \hat{\mathbf{x}}^-)(\mathcal{Y}_i - \hat{\mathbf{x}}^-)^\top + Q_k

The predicted state is the weighted average of the landing spots. The
predicted uncertainty is their weighted spread: for each point, take how far
it landed from the new mean, multiply that difference by itself (the matrix
version of squaring it), weight it, and add them all up. Then add
:math:`Q_k`, because the model still makes its usual error each step.
:math:`Q_k` is the same as in the EKF: the wheel and gyro noise, carried into
:math:`x`, :math:`y` and :math:`\theta` by :math:`G`.

The Catch: Still One Bell Curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

However cleverly the UKF places its points, it always rebuilds **one** mean
and **one** covariance: one bell curve, one peak.

.. figure:: /_static/images/L3/ukf_story_3_peaks.png
   :alt: Position along the tunnel from 0 to 65 m. The real belief, gray, has two narrow peaks at 20 and 45 m, each labeled a light. A wide, low dashed orange bell covers both, with its mean at 32.5 m, labeled one bell curve: its mean sits between the lights, where the AV is not.
   :width: 85%
   :align: center

   An illustration, not a filter run. A stretch of tunnel with no exit sign in
   view, only identical lights 25 m apart. A match on a light fits this light
   or the next one, so the real belief (gray) has two peaks, at 20 m and
   45 m. One bell curve forced onto it (dashed orange) puts its mean at
   32.5 m, halfway between the lights, the one place the camera says the AV
   is not.

When the honest answer is "one of two lights", a bell curve puts the AV
**between** them, and its ellipse even looks reasonable. The EKF has the same
problem. Neither can say "here **or** there". That is the particle filter's
job, in the next section.

EKF or UKF: When to Use Each
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 24 38 38
   :header-rows: 1
   :class: compact-table

   * -
     - **EKF**
     - **UKF**
   * - Approximates
     - the **function**
     - the **belief**
   * - You write
     - :math:`f`, :math:`h` and **Jacobians**
     - :math:`f`, :math:`h` (and :math:`G` for :math:`Q`)
   * - Good when
     - uncertainty is **small**
     - uncertainty is **wide**

- **What you must write.** For the UKF, :math:`f` and :math:`h` only. That
  removes a bug: a hand-derived Jacobian with one wrong sign gives a filter
  that runs, settles down, and is wrong.
- **Cost.** A Jacobian each, against :math:`2n+1` calls to the function each.
  For a state of three or four numbers those are similar, and the UKF is
  sometimes cheaper once you count the work of computing the Jacobian at all.
- **When.** The EKF is enough when the uncertainty is small compared with how
  much the function bends: then the curve is nearly straight across the area
  that matters. The UKF earns its place when the covariance is wide: at
  start-up, after a long stretch with no sign match, in a hard turn. Exactly
  the banana.

.. important::

   **Neither can handle two peaks.** Both still carry one mean and one
   covariance.

The Same Drive, Done With Five Points
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This subsection and the next ones work the UKF out by hand. It is the same AV
as the lecture's EKF animation, so we can compare: it drives 20 m, give or
take 0.5 m, with its heading known to 12°.

.. figure:: /_static/images/L3/ukf_sigma_points.png
   :alt: Left: distance driven against heading, a blue one-sigma ellipse at 20 m and 0 degrees with five green sigma points, chi 1 and chi 3 at 20.87 and 19.13 m, chi 2 and chi 4 at plus and minus 20.8 degrees. Right: along against lateral distance, 500 blue samples forming a banana, five green crosses where the sigma points land, the heading points at 18.7 m and plus or minus 7.1 m, a green UKF ellipse at 19.57 m and a dashed orange EKF ellipse at 20 m.
   :width: 90%
   :align: center

   **Left:** the belief before the drive, in distance driven and heading. The
   blue ellipse is the uncertainty; the five green dots are the sigma points:
   :math:`\chi_0` at the mean, :math:`\chi_1` and :math:`\chi_3` one step out
   and back in distance (20.87 and 19.13 m), :math:`\chi_2` and
   :math:`\chi_4` one step out and back in heading (:math:`\pm 20.8°`).
   **Right:** each point pushed through the real function, distance times
   cosine and sine of the heading. The blue dots are 500 samples, the real
   banana. The crosses are where the points landed: the two heading points
   landed **short**, at 18.7 m and :math:`\pm 7.1` m to the side, because an
   AV pointed 20° off does not get as far forward. The green UKF ellipse
   moves back with the real cloud, to 19.57 m, and is wider along the track;
   the dashed orange EKF ellipse stays at 20 m with the along-track width it
   started with.

Five calls to the function, and the UKF saw the banana.

Step Length Is About 1.7 Sigma From the Mean
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \chi_0 = \hat{\mathbf{x}} \qquad
   \chi_i = \hat{\mathbf{x}} + \sqrt{n+\kappa}\;L_i \qquad
   \chi_{n+i} = \hat{\mathbf{x}} - \sqrt{n+\kappa}\;L_i

Start with a single number. If :math:`P` is a variance, its square root is the
standard deviation :math:`\sigma`: one step along the only direction there
is.

For a matrix, :math:`L_i` is column :math:`i` of :math:`L`, the **matrix
square root** of :math:`P` (:math:`LL^\top = P`): one direction to step in,
already :math:`1\sigma` long. When :math:`P` is diagonal, as in the drive
example, the columns are the axes of the ellipse. When it is not, they are
still a correct set of directions, just not the axes you would draw. Code gets
:math:`L` with one call, usually named **Cholesky**; you never work it out by
hand.

:math:`\kappa` is a knob for how far out the points sit. The usual choice for
a bell curve is :math:`n + \kappa = 3`, so one step is
:math:`\sqrt{3} \approx 1.7\,\sigma`. That is where the what-ifs came from:
:math:`\sqrt{3} \times 12° \approx 21°`, and
:math:`\sqrt{3} \times 0.5 \approx 0.87` m.

The Weights Say How Much Each Point Counts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   W_0 = \frac{\kappa}{n+\kappa} \qquad\qquad
   W_i = \frac{1}{2\,(n+\kappa)} \quad \text{for the other } 2n

They always add up to 1. All three cases in this lecture keep
:math:`n + \kappa = 3`.

.. list-table::
   :widths: 40 15 20 25
   :header-rows: 1
   :class: compact-table

   * - **Case**
     - :math:`\kappa`
     - **Center**
     - **Each other**
   * - picture, :math:`n = 1`
     - 2
     - 2/3
     - 1/6 (two)
   * - drive, :math:`n = 2`
     - 1
     - 1/3
     - 1/6 (four)
   * - hands-on, :math:`n = 3`
     - 0
     - **0**
     - 1/6 (six)

In the hands-on, :math:`\kappa = 0`: the script still places the center point,
it just gets weight zero.

.. warning::

   Many libraries use a scaled version with three knobs, :math:`\alpha`,
   :math:`\beta` and :math:`\kappa`. Same idea, different weights, so their
   numbers will not match this table.

The Recipe With Numbers: the Five Drive Points
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AV: :math:`20 \pm 0.5` m, heading :math:`0 \pm 12°`. With :math:`n = 2`
and :math:`\kappa = 1`, one step is :math:`\sqrt{3}\,\sigma`: 0.87 m in
distance, or 21° in heading.

.. list-table::
   :widths: 15 15 35 35
   :header-rows: 1
   :class: compact-table

   * - **Point**
     - :math:`W_i`
     - **Placed at**
     - **Lands at** :math:`x`
   * - :math:`\chi_0`
     - 1/3
     - 20.0 m, 0°
     - 20.00 m
   * - :math:`\chi_1`
     - 1/6
     - 20.9 m, 0°
     - 20.87 m
   * - :math:`\chi_3`
     - 1/6
     - 19.1 m, 0°
     - 19.13 m
   * - :math:`\chi_2`
     - 1/6
     - 20.0 m, +21°
     - **18.70 m**
   * - :math:`\chi_4`
     - 1/6
     - 20.0 m, -21°
     - **18.70 m**

- :math:`\chi_0` is the mean, and lands at 20 m, because an AV pointed
  straight goes straight. :math:`\chi_1` and :math:`\chi_3`, one step farther
  and one step shorter, land exactly where they were placed, again because
  the heading is zero.
- :math:`\chi_2` and :math:`\chi_4` are the interesting ones: 20 m with the
  heading turned 21° either way. They land at 18.70 m, about 7 m to the side:
  short.
- Rebuild the mean: a third of 20, plus a sixth of each of the other four.

.. important::

   **Weighted average: 19.57 m.** The truth, from 500 samples, is 19.58 m. The
   EKF says 20.00 m. The along-track spread from the same five values is
   0.79 m, against an exact 0.78 m; the EKF says 0.5 m, and would say 0.5 m no
   matter how far the AV drove. The improvement came from two points that
   landed short, and the average noticed.

The Update Without a Jacobian
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The update is the same recipe, through :math:`h` this time. Place fresh sigma
points around :math:`\hat{\mathbf{x}}^-`, and push each through the
measurement model: :math:`\mathcal{Z}_i = h(\chi_i)` is the reading that
point expects (in the curved tunnel, a range and a bearing).

.. math::

   \hat{\mathbf{z}} = \sum_i W_i\,\mathcal{Z}_i
   \qquad
   S = \sum_i W_i\,(\mathcal{Z}_i - \hat{\mathbf{z}})(\mathcal{Z}_i - \hat{\mathbf{z}})^\top + R

.. math::

   P_{xz} = \sum_i W_i\,(\chi_i - \hat{\mathbf{x}}^-)(\mathcal{Z}_i - \hat{\mathbf{z}})^\top
   \qquad
   K = P_{xz}\,S^{-1}

The weighted average of the expected readings is :math:`\hat{\mathbf{z}}`.
Their weighted spread, plus :math:`R`, is :math:`S`: how big the surprise
should be, the same :math:`S` as before, found a different way.

One line is new: :math:`P_{xz}`. For each point, take how far it sits from
the prediction, and how far its expected reading sits from
:math:`\hat{\mathbf{z}}`, and multiply the two. It says how the state and the
reading **move together**: if the AV were a bit farther east, would the range
be longer or shorter? It takes the place of :math:`P^- H^\top`, and it comes
from the points, not from a Jacobian. Then the new estimate is the prediction
plus :math:`K` times the surprise, as always.

UKF Against EKF, Line by Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the table to copy. The UKF column shows what the points replace.

.. list-table::
   :widths: 16 38 46
   :header-rows: 1
   :class: compact-table

   * -
     - **EKF**
     - **UKF**
   * - **Predict**
     - :math:`\hat{\mathbf{x}}^- = f(\hat{\mathbf{x}}, \mathbf{u})`
     - :math:`\hat{\mathbf{x}}^- = \sum W_i\,\mathcal{Y}_i`
   * -
     - :math:`P^- = F_k P F_k^\top + Q_k`
     - :math:`P^- =` spread of :math:`\mathcal{Y}_i` :math:`+\,Q_k`
   * - **Update**
     - :math:`\hat{\mathbf{z}} = h(\hat{\mathbf{x}}^-)`
     - :math:`\hat{\mathbf{z}} = \sum W_i\,\mathcal{Z}_i`
   * -
     - :math:`S = H_k P^- H_k^\top + R`
     - :math:`S =` spread of :math:`\mathcal{Z}_i` :math:`+\,R`
   * -
     - :math:`K = P^- H_k^\top S^{-1}`
     - :math:`K = P_{xz}\,S^{-1}`
   * -
     - :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^- + K\nu`
     - :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^- + K\nu`
   * -
     - :math:`P = (I - KH_k)\,P^-`
     - :math:`P = P^- - K S K^\top`

:math:`\nu = \mathbf{z} - \hat{\mathbf{z}}` in both. Every UKF entry built
from :math:`\mathcal{Y}_i`, :math:`\mathcal{Z}_i` or :math:`P_{xz}` comes from
the points: **no** :math:`F_k`, **no** :math:`H_k`, so no Jacobian to get
wrong.

The last line looks different but means the same thing. In the Kalman filter,
:math:`KS = P^- H^\top`, so :math:`P^- - KSK^\top` equals
:math:`(I - KH)\,P^-`. The UKF uses the form that needs no :math:`H`.

The UKF in Code
~~~~~~~~~~~~~~~

From ``run_ukf()`` in ``curved_tunnel/ukf_curve.py``, trimmed.

.. code-block:: python

   # PREDICT: place, push through the real f, rebuild
   X, W = sigma_points(x, P)                     # 1. place
   Y = f(X, u)                                   # 2. push, through the real f
   x, P, _ = mean_and_cov(Y, W, 2)               # 3. rebuild (row 2 is an angle)
   P = P + ek.process_noise(x, u, ek.SIGMA_V, sigma_w)   # plus Q, as always

   # UPDATE: the same recipe, through h
   X, W = sigma_points(x, P)
   Z = h(X, sign)
   zhat, S, Rz = mean_and_cov(Z, W, 1)        # Rz: each reading minus zhat
   S = S + Rm
   Dx = X - x
   Dx[:, 2] = wrap(Dx[:, 2])
   Pxz = (W[:, None] * Dx).T @ Rz            # how state and reading move together
   K = Pxz @ np.linalg.inv(S)                # the same gain, no Jacobian
   nu = z - zhat
   nu[1] = wrap(nu[1])
   x = x + K @ nu
   x[2] = wrap(x[2])
   P = P - K @ S @ K.T

- **Predict is four lines:** the three steps, plus :math:`Q`.
  ``sigma_points`` places the points, ``f`` pushes all seven at once, and
  ``mean_and_cov`` rebuilds the mean and :math:`P`.
- **Update** is the same recipe through ``h``. ``mean_and_cov`` gives
  :math:`\hat{\mathbf{z}}` and the spread that becomes :math:`S`. Then comes
  :math:`P_{xz}`, from the state differences and the reading differences, and
  then the gain.
- **The last five lines** are the Kalman filter you already know, with the
  same two angle wraps as the EKF.

Compare with the lecture's EKF code. The EKF needed ``jacobian_f`` and
``jacobian_h``; this needs neither. It needs ``sigma_points`` and
``mean_and_cov`` instead, and those two stay the same for every model you
will ever write.

Three Traps When You Build a UKF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   **1. Average angles with care.** Headings of 179° and -179° are only 2°
   apart, both pointing almost due west, but their plain average is 0°: due
   east, the opposite direction. Take each angle relative to one reference
   point, wrap the differences, average those, and add the reference back:
   ``mean_and_cov()`` does this. The EKF never averages angles, so this trap
   is new.

   **2. Cholesky needs a healthy** :math:`P`. It raises an error when
   :math:`P` is not symmetric and positive. Do not catch the error and carry
   on: treat it as a bug report. :math:`P` went bad somewhere upstream, often
   from rounding, or from a :math:`Q` or :math:`R` that is far too small.

   **3. Wrap** :math:`\nu` **and** :math:`\hat{\mathbf{x}}`, exactly as in the
   EKF, in the same two places.

Check: the UKF
~~~~~~~~~~~~~~

Answer each one before opening the answers.

1. The EKF approximates the curve. What does the UKF approximate instead?
2. With :math:`n = 2` and :math:`\kappa = 1`: how many sigma points, and what
   are their weights?
3. What takes the place of :math:`P^- H^\top` in the UKF gain, and where does
   it come from?
4. Can a UKF say "under this light *or* the next one"?

.. dropdown:: Check: the UKF. Answers
   :color: success
   :icon: check-circle

   1. **The bell curve.** The UKF keeps the real function and replaces the
      bell curve with a handful of points, then pushes each point through the
      real curve.
   2. :math:`2n+1` **is five points.** The center gets
      :math:`\kappa/(n+\kappa)`, a third. Each of the other four gets a sixth.
      They add to one.
   3. :math:`P_{xz}`, **how the state and the reading move together.** It
      comes from the sigma points: each point's distance from the prediction,
      times its expected reading's distance from :math:`\hat{\mathbf{z}}`,
      weighted and added up.
   4. **No.** It still carries one mean and one covariance: one peak. That is
      exactly the problem the particle filter is for.

UKF Hands-On: UKF Against EKF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **In this section:** ``ukf_curve.py``, the **same curved tunnel as the
  EKF hands-on, plus an unlit stretch**, with three beliefs side by side.
- **What it is for:** seeing the UKF stay on the exact belief in the dark,
  where the EKF drifts off it, and what happens after the first match.

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Line**
     - **What it is**
   * - **exact belief**
     - 4,000 possible AVs, each driven with its own random wheel and gyro
       noise and weighed against every sign match: the **referee**
   * - **EKF**
     - one tangent at the estimate, for the whole ellipse
   * - **UKF**
     - 7 sigma points pushed through the real :math:`f` and :math:`h`

A filter is right when its mean and its ellipse sit on the referee's cloud.
The window has two sliders: how well the heading is known at the tunnel
entrance (``--heading-sigma``, default 12°), and an unlit stretch at the
start where the camera matches no sign at all (``--dark``, default 5 s).
Together they make the banana.

.. code-block:: bash

   cd enpm818z-fall-2026-carla-python/lecture3/curved_tunnel
   python3 ekf_curve.py --make-csv     # writes curve_drive.csv, if you have not yet
   python3 ukf_curve.py                # UKF against EKF against exact, live window

.. admonition:: What to look for
   :class: tip

   - **Raise the heading** :math:`\sigma` **or the unlit stretch:** the EKF
     drifts further from the exact belief.
   - **At the first match** both snap back, and neither follows the cloud at
     once.

Step 1: Watch the Size of the Belief
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/tunnel_ukf_size.png
   :alt: The largest position sigma in meters over 21 seconds for the exact belief (thick gray), the EKF (dashed orange) and the UKF (green). The unlit stretch from 0 to 5 s is shaded. All three grow from 1 m to about 14 m, drop to about 1 m at the first sign match near 6.8 s, then stay below about 1.3 m. A black line marks 6 s.
   :width: 80%
   :align: center

   The top-right plot of the window: the size of each belief, as its largest
   position :math:`\sigma`. Gray is the **exact** belief, from 4,000
   simulated AVs; dashed orange the **EKF**; green the **UKF**. The shaded
   band is the unlit stretch. The black line is the moment shown in the
   window, 6 s.

In the dark no sign is matched, so all three grow, to about **14 m**, and
they grow together: the EKF gets the **largest** :math:`\sigma` right (its
spread along the drive is still too small). The first sign match, near 6.8 s,
shrinks all three to about 1 m. The clearer failure is not the size; the next
plot shows where it is: the middle of the belief.

Step 2: Watch How Far Off Each Mean Is
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/tunnel_ukf_offset.png
   :alt: How far each filter's mean is from the exact one, in meters, over 21 seconds, with the unlit stretch shaded. The EKF, dashed orange, climbs in a straight line to 1.45 m just before the first match near 6.8 s, then drops to about 0.2 m. The UKF, green, stays near 0.03 m until that match, then jumps to about 1.1 m and steps down at each later match to about 0.1 m by 21 s.
   :width: 80%
   :align: center

   The bottom-right plot of the window: how far each filter's **mean** is from
   the exact belief's mean. Dashed orange is the EKF, green the UKF, the
   shaded band the unlit stretch, and the black line 6 s.

- **Until the first match (6.8 s)** the **EKF** climbs in a straight line to
  **1.45 m** off: it keeps the middle of a straight ellipse, but the real
  belief is a banana. The **UKF** stays at **0.03 m**. That is the banana,
  caught by seven calls to the function.
- **After the match**, to be honest about it, the UKF is the one farther off:
  about 1.1 m at first, shrinking to 0.1 m by 21 s. A belief 14 m wide meets
  a measurement good to 1 m; the UKF's points sit on both sides of the sign,
  so it corrects cautiously. Neither filter follows the exact belief at once.
  That moment is where a bell curve, any bell curve, runs out.

Step 3: Move the Sliders
^^^^^^^^^^^^^^^^^^^^^^^^

Guess each row first, then check. The table gives each mean's distance from
the exact belief, just before the first sign match.

.. list-table::
   :widths: 40 30 30
   :header-rows: 1
   :class: compact-table

   * - **Heading** :math:`\sigma` **, unlit**
     - **EKF**
     - **UKF**
   * - 3°, 5 s
     - 0.12 m
     - 0.04 m
   * - 12°, 5 s (default)
     - 1.45 m
     - 0.03 m
   * - 12°, 9 s
     - 1.90 m
     - 0.03 m
   * - 25°, 5 s
     - **6.03 m**
     - 0.01 m

At 3° the two filters agree to within a few centimeters: across so small an
uncertainty the curve is nearly straight, and a tangent is good enough. At
12° the EKF is 1.45 m off; give it 9 s in the dark and it is 1.90 m. At 25°
it is 6.03 m off. The UKF stays within a few centimeters of the exact belief
in every row.

.. important::

   **Small uncertainty: they agree.** Wide uncertainty on a curve, before the
   first match: the EKF's tangent misses, and the UKF's points do not. This is
   the rule from the EKF-or-UKF table, now with numbers.

   The exact belief is itself 4,000 simulated AVs, so its own mean wanders by a
   few centimeters: read the UKF column as "within a few hundredths, at most
   0.1 m".


Particle Filter in Detail
-------------------------

The particle filter is the lecture's third alternative. This section works it
out on paper and in code: why we drop the bell curve, the three steps as
equations, five particles by hand, how it differs from the UKF, the code and
the traps, a check, and a hands-on where a crowd of guesses finds an AV that
has no idea where it is.

A Crowd of Possible States
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Alternative 3 of 3.** Every Kalman filter, the EKF and the UKF included,
keeps one bell curve: one peak. The EKF and the UKF dropped the straight-line
model. The particle filter drops the single bell curve.

- **In this section:** a filter that keeps a **crowd of guesses** and no bell
  curve.
- **What it is for:** an AV that could be in **one of several places**, with
  one peak at each.

**The idea.** The UKF tried a few guesses, then squeezed them back into a bell
curve. The particle filter keeps **thousands** of guesses and never squeezes
them. Each step, move every guess the way the AV moved. When the camera sees
something, score each guess against what the camera saw: copy the good ones,
drop the bad ones. The crowd that is left is the belief. **The cost:** the
number of guesses you need grows fast with the size of the state.

.. admonition:: Definition: particle filter
   :class: important

   A filter that stores the belief as a **crowd of weighted guesses**, called
   particles, instead of one bell curve. So the belief can be **in several
   places at once**.

A Belief as a Crowd of Dots
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L3/pf_belief.png
   :alt: Two panels of distance along against across the tunnel. Left, one peak: 300 blue dots in an oval inside the tunnel, with a dashed orange ellipse and center dot over them; the two pictures agree. Right, two peaks: two identical lights 25 m apart, each with a cluster of blue dots under it, and a long dashed orange ellipse fitted to all the dots, centered halfway between the lights.
   :width: 90%
   :align: center

   **Left, one peak:** the same belief drawn two ways. The dashed ellipse is
   the Kalman way, one mean and one covariance; the 300 blue dots are the
   particle way, dense in the middle and thinner toward the edges. They say
   the same thing, so with one peak nothing is lost by drawing dots. **Right,
   two peaks:** the camera matched a light, and two identical lights 25 m
   apart both fit. The dots form a cluster under each light, nothing in
   between. One mean and one covariance fitted to the same dots give the long
   dashed ellipse: long enough to cover both lights, but centered halfway
   between them, the one place we know the AV is not.

The planner and the controller would be told "you are between the lights,
roughly". The dots would have told them "you are under one of these two
lights".

.. admonition:: Definition: particle
   :class: important

   One complete guess at the state, with a **weight** that says how much the
   filter believes it. A particle filter carries :math:`N` of them, hundreds
   to thousands, and together they *are* the belief: dense where the filter
   thinks the AV is, empty where it does not. No ellipse anywhere.

The Particle Filter Fits No Bell Curve at All
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same curve again, 20 m driven with heading :math:`30 \pm 12°`, done by the
UKF and by a particle filter.

.. figure:: /_static/images/L3/bell_4_ukf.png
   :alt: The UKF panel: three green sigma points on the input bell, at 9.2, 30 and 50.8 degrees, pushed through the curve 20 cos theta, and a green bell fitted to their landing spots, centered on 16.94 m, over the gray lopsided histogram of the true output.
   :width: 60%
   :align: center

   **UKF:** a few **chosen** points go through the real curve, then a bell
   curve is fitted to where they land. The mean came out right, but the
   output is still forced into a bell curve.

.. figure:: /_static/images/L3/bell_5_pf.png
   :alt: The particle filter panel: 200 blue dots drawn at random from the input bell, pushed through the same curve, landing in the gray lopsided histogram of the true output, piled up just under 20 m with a tail below. No bell is fitted. Mean 16.82 m, true 16.95 m.
   :width: 60%
   :align: center

   **Particle filter:** 200 **random** points from the input belief go through
   the same real curve. They fill the lopsided shape, piled up just under 20 m
   with a tail below. No bell curve is fitted: the dots **are** the belief.

The particles' mean is 16.82 m; the true value is 16.95 m. Two hundred random
points give a slightly noisy answer, and more points give less noise. That is
the price of random points. The gain: the crowd can take any shape, even two
separate clumps.

When the Answer Is One of Two Places
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recall: a **belief** is which states are possible, and how likely each one
is. A Kalman filter, an EKF and a UKF all store it as one bell curve, with one
peak. But a belief can have two peaks, or three, or twenty.

**Back in the tunnel:** the lights are identical, one every 25 m. The camera
matches a light against the HD map, and **the match fits every light**
equally well. If the AV has no idea where it is, that one match gives a peak
under every light in the tunnel.

.. important::

   One bell curve has one center, so it puts the AV **between two lights**:
   the one place the camera says it is not. It even reports a
   reasonable-looking covariance, because nothing in the equations knows
   anything went wrong.

So we drop the bell curve and let the crowd be in two places at once.

One Cycle: Predict, Weigh, Resample
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is the same loop as the Kalman filter: **predict**, then **update**. Here
it is in one dimension, with 40 particles.

.. figure:: /_static/images/L3/pf_cycle.png
   :alt: Three strips on an axis of position along the tunnel in meters. 1, predict: 40 gray dots near 8 m move 10 m per second for 1 s to blue dots near 18 m, more spread out. 2, weigh: an orange bell curve centered on a sign match at 20.5 m with sigma 1.5 m, and blue dots sized by weight, large near 20.5 and tiny far away. 3, resample: 40 green dots of equal size clustered between 18 and 21 m, stacked where copies of the same particle were drawn.
   :width: 90%
   :align: center

   **1, predict:** the gray dots are the crowd from the last cycle, near
   8 m. Every one moves with the motion model, 10 m/s for 1 s, and lands near
   18 m (blue). Each also gets its own random kick, so the blue crowd is more
   spread out than the gray one: the kick plays the role of :math:`Q`, and
   where the Kalman ellipse grew, the crowd spreads. **2, weigh:** a sign
   match arrives at :math:`z = 20.5` m with :math:`\sigma = 1.5` m. Each
   particle is scored by how likely that reading is if the AV were there; the
   orange curve is that score along the road (the sensor's bell curve, turned
   around), and each dot's size shows its score. Nothing moves: the crowd gets
   weighed. This is the update. **3, resample:** draw 40 new particles from the
   old ones, in proportion to weight. Heavy particles are copied several times
   (the stacks are copies of the same particle); light ones are not drawn and
   vanish. All weights are equal again, and the crowd is dense near the match.

That crowd goes straight back into strip 1, and the loop repeats.

When to Use a Particle Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important::

   **Use it when** the belief has **several peaks**: "where on this map am
   I?"

   **Avoid it when** the state is **big**, or the belief has **one peak**.

   **Ask about the shape of the belief, not how curved the model is.**

People often pick a particle filter whenever a problem looks hard. That is
the wrong test. A strongly curved model with one peak is a UKF problem. A
gently curved model with three possible answers is a particle filter problem.
The curve does not decide it; the number of peaks does. Examples with several
peaks: "where on this whole map am I?", a robot picked up and moved somewhere
unknown (the kidnapped robot problem), or a map match that fits several
places. With many quantities in the state, or one peak, a Kalman filter does
the same job with a thousandth of the work.

.. note::

   Monte Carlo Localization (Dellaert et al., 1999), this filter used on a
   real map, is :doc:`L7 <../lecture7/l7_index>`.

The Three Steps as Equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: likelihood :math:`p(\mathbf{z} \mid \mathbf{x})`
   :class: important

   How likely the reading :math:`\mathbf{z}` is, **if** the AV were at
   :math:`\mathbf{x}` (up to a constant). For one sign match with noise
   :math:`\sigma`, it is the sensor's bell curve taken at the gap between the
   reading and what :math:`h` says the AV would see from :math:`\mathbf{x}`:

   .. math::

      \exp\!\big(-(\mathbf{z} - h(\mathbf{x}))^2 / 2\sigma^2\big)

   Close gives a high score, far a low one.

1. **Predict:** move every particle with **its own** draw of the noise:
   :math:`\mathbf{x}^{(i)} \leftarrow f\big(\mathbf{x}^{(i)}, \mathbf{u} + \text{noise}^{(i)}\big)`.
   That random kick is how a particle filter does :math:`Q`.
2. **Weigh:** :math:`w^{(i)} \leftarrow w^{(i)}\, p(\mathbf{z} \mid \mathbf{x}^{(i)})`,
   then divide by the sum so the weights add to 1. Nothing moves. This is the
   whole update.
3. **Resample:** draw :math:`N` particles, particle :math:`i` with
   probability :math:`w^{(i)}`. Heavy ones get copied, light ones vanish.
   Reset every weight to :math:`1/N`.

No mean, no covariance, no gain, no Jacobian anywhere.

The Recipe With Numbers: Five Particles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Five particles, so you can check every number by hand. After predict they sit
at 8, 9, 10, 11 and 13 m. A sign match arrives at :math:`z = 10.5` m, with
:math:`\sigma = 1` m. Score each particle by how likely that reading is if the
AV were there: :math:`\exp\!\big(-(z - x)^2 / 2\sigma^2\big)`.

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1
   :class: compact-table

   * - **Particle**
     - **Score**
     - **Weight**
     - **Copies kept**
   * - 8 m
     - 0.04
     - 0.02
     - 0
   * - 9 m
     - 0.32
     - 0.15
     - 1
   * - 10 m
     - 0.88
     - **0.40**
     - 2
   * - 11 m
     - 0.88
     - **0.40**
     - 2
   * - 13 m
     - 0.04
     - 0.02
     - 0

- **Score.** The particle at 10 m is half a meter from the match: score
  0.88. The one at 8 m is 2.5 m off: score 0.04.
- **Weight** = score ÷ sum of scores. The five scores add up to about 2.18.
  The two near the match now hold 40% each; the two far away hold 2% each.
- **Estimate.** Here the crowd has one peak, so the weighted average,
  10.28 m, is a fine estimate. With two peaks it would not be.
- **Copies kept.** Resample: draw five new particles with those
  probabilities. The expected number of copies is five times the weight, so
  the two near the match get about two copies each, the two far away almost
  none. The column is one draw.

.. important::

   **Nothing is averaged into a place the AV is not**: every survivor was
   already on the list. That is why the crowd can sit under two lights at
   once and the ellipse cannot.

How the Particle Filter Differs From the UKF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 18 37 45
   :header-rows: 1
   :class: compact-table

   * -
     - **UKF**
     - **Particle filter**
   * - **Belief**
     - :math:`\hat{\mathbf{x}}` and :math:`P`
     - :math:`N` particles :math:`\mathbf{x}^{(i)}`, weights :math:`w^{(i)}`
   * - **Points**
     - :math:`2n+1`, chosen, thrown away after each step
     - :math:`N`, random, thousands, kept
   * - **Predict**
     - push through :math:`f`, rebuild, :math:`+\,Q_k`
     - push each through :math:`f` with its own noise
   * - **Update**
     - gain :math:`K` moves :math:`\hat{\mathbf{x}}`
     - weigh by :math:`p(\mathbf{z} \mid \mathbf{x}^{(i)})` (resample after)
   * - **Answer**
     - :math:`\hat{\mathbf{x}}`
     - the heaviest cluster
   * - **Shape**
     - one peak
     - any shape

Both push points through the real :math:`f`. Only the UKF squeezes them back
into a bell curve. The particle filter moves nothing in the update: it only
weighs.

The Three Steps in Code
~~~~~~~~~~~~~~~~~~~~~~~

From ``run_pf()`` in ``pf_tunnel/pf_tunnel.py``, trimmed. The state is one
number, the distance along the tunnel, so ``parts`` is an array of :math:`N`
distances.

.. code-block:: python

   # PREDICT: every particle moves by its own draw of the wheel noise.
   v = d["wheel_v"][k - 1] + rng.normal(0, sigma_wheel, N)
   parts = parts + v * DT

   # WEIGH: the update. Nothing moves; the crowd gets scored.
   w = w * likelihood(parts, d["match"][k], d["match_dist"][k], mp, sigma_cam)
   w = w / w.sum()

   # RESAMPLE when the effective number of particles gets too small.
   if 1.0 / np.sum(w**2) < N / 2:
       pos = (rng.random() + np.arange(N)) / N          # systematic resampling
       idx = np.minimum(np.searchsorted(np.cumsum(w), pos), N - 1)
       parts, w = parts[idx], np.full(N, 1.0 / N)

- **Predict is two lines.** Every particle gets the wheel speed plus its own
  random noise, and moves by speed times :math:`\Delta t`.
- **Weigh is two lines.** Multiply by the likelihood, then divide by the sum.
- **Resample is four lines**, with two details. It runs only when the crowd
  needs it (next subsection). And it uses one random number, not :math:`N`:
  :math:`N` evenly spaced pointers walk along the running total of the
  weights, and each pointer picks the particle it lands in. This is called
  **systematic resampling**, and it loses fewer good particles than :math:`N`
  separate draws.

The whole filter is eight lines plus the likelihood function.

Three Traps When You Build a Particle Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   **1. Put a floor under the likelihood.** Say the camera mistakes a
   reflection for a light, and the reading fits no particle. Every likelihood
   is almost zero, so the sum is almost zero, and dividing by it blows up or
   wipes out the good particles. The script adds a floor of
   :math:`10^{-3}`, so one bad reading can only nudge the weights.

   **2. Resample only when needed.** Each resample copies some particles and
   drops others, so the crowd gets less varied every time. The effective
   count

   .. math::

      N_\text{eff} = \frac{1}{\sum_i \big(w^{(i)}\big)^2}

   counts the particles that still matter: :math:`N` when all weigh the same,
   1 when one holds it all. The script resamples when
   :math:`N_\text{eff} < N/2`. (The cycle figure resampled every time, just to
   keep the picture simple.)

   **3. Run it more than once.** A particle filter is random, so one run
   proves nothing. ``--trials 40`` runs the same drive 40 times with fresh
   random numbers and counts how often it settles on the right place.

What It Costs, and How It Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Three costs. The second one is the dangerous one.
   :class: danger

   **1. It gets expensive fast.** You need about a fixed number of particles
   per quantity, multiplied together. Ten per quantity: 100 for
   :math:`[x, y]`, 1,000 for :math:`[x, y, \theta]`, a million for six. The
   Kalman family costs about :math:`n^3`, where :math:`n` is the size of the
   state: for six, a couple of hundred operations. That is why nobody runs a
   particle filter on a fifteen-quantity state.

   **2. It collapses quietly.** After a few resamples, most particles are
   copies of a few ancestors: in the cycle figure, 40 particles came back as
   16 different ones after one resample. With too few particles, the crowd
   ends up on one peak and silently drops the others. **No error is raised.**
   You get an answer, and it looks fine. It is the same failure as a diverging
   EKF: a confident number with nothing behind it.

   **3. Do not average two peaks.** The weighted average of a cluster under
   one light and a cluster under the next is, again, halfway between them.
   Report the heaviest cluster, or both, or say "not yet resolved" and let the
   next few readings settle it. Carrying the crowd is what lets the filter say
   that.

Check: the Particle Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~

Answer each one before opening the answers.

1. What is a particle, and what does its weight say?
2. What does the likelihood :math:`p(\mathbf{z} \mid \mathbf{x}^{(i)})`
   measure, and what does it do to a weight?
3. The crowd is under two lights. Why is the weighted average the worst
   answer to report?
4. You use too few particles. How does the filter fail, and does it warn you?

.. dropdown:: Check: the particle filter. Answers
   :color: success
   :icon: check-circle

   1. **A particle is one complete guess at the state.** Its weight says how
      much the filter believes that guess, after scoring it against the
      measurements.
   2. **How likely the reading is if the AV were at that particle.** The
      weight is multiplied by it, so particles that explain the reading get
      heavier, and resampling then copies them.
   3. **The average of two clusters sits halfway between them**, between the
      lights: the one place the camera says the AV is not. Report the
      heaviest cluster, or both.
   4. **It collapses quietly.** The crowd ends up in one place, sometimes the
      wrong one, and nothing raises an error. It looks just as confident as
      when it is right. You will see it happen in the hands-on.

Particle Filter Hands-On: Finding a Lost AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **In this section:** the AV's computer restarts in a **700 m tunnel**:
  23 identical lights, 25 m apart, and **five SOS niches** (emergency phone
  niches), spaced irregularly on purpose.
- **What it is for:** watching a crowd of guesses find the AV when it has no
  idea where it is.

The AV knows its speed from the wheel encoders, and nothing else. A light
match fits 23 places at once; a niche match fits five. The gaps between
niches all differ, so after two or three niches only one place in the tunnel
explains the whole sequence.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Column or file**
     - **What it is**
   * - ``wheel_v``
     - wheel speed (noise 0.3 m/s): the **control input**
   * - ``match``, ``match_dist``
     - light or niche, and how far ahead it is (:math:`\sigma` 1 m): the
       **measurement**. Empty on most rows (24 matches, 5 of them niches)
   * - ``true_s``
     - the truth, distance along the tunnel: **never used by the filter**
   * - ``tunnel_map.csv``
     - the HD map: where every light and niche is

.. admonition:: What to look for
   :class: tip

   - **The crowd:** 23 clusters, one per light; 18 as the first lights rule
     places out; 4 after the first niche; one by 21 s.
   - **The orange average** sits in empty tunnel between clusters until the
     crowd is in one place.
   - **Fewer particles:** sometimes it settles on the wrong place, with no
     warning.

Step 1: Run the Script
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   cd enpm818z-fall-2026-carla-python/lecture3/pf_tunnel
   python3 pf_tunnel.py --make-csv       # the data and the map
   python3 pf_tunnel.py                  # the live window
   python3 pf_tunnel.py --trials 40      # how often is it right?
   python3 pf_tunnel.py --html pf.html   # no desktop? a web page

The third command matters: particle filters are random, so one run proves
nothing. ``--trials 40`` runs the same drive 40 times with fresh random
numbers and counts how often it settles on the right place.

The filter is ``run_pf()``: predict, weigh, resample. Predict moves every
particle with its own noisy copy of the wheel speed. Weigh scores each
particle against the camera's reading. Look at the likelihood function: for a
light match, it adds up a bell curve for **every** light in the map, because
the reading could have come from any of them. That one line lets the belief
have 23 peaks.

Step 2: Watch the Belief
^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/tunnel_pf_belief.png
   :alt: The belief 12 s in, as weight per place along the 700 m tunnel. Three spikes: the tallest, about 0.55, near 193 m, under a dashed black line at the AV's true position; a medium one near 567 m; a small one near 417 m. Elsewhere the weight is nearly zero.
   :width: 95%
   :align: center

   The middle plot of the window, 12 s in: how much weight sits at each place
   along the whole 700 m tunnel. The dashed black line is the AV's true
   position.

The belief is in **three places at once**: near 193 m, 417 m and 567 m. The
lights all look alike, so three stretches of tunnel fit what the camera has
seen so far. The AV's true position is under the **tallest** spike. A bell
curve could not draw this: it would put one peak at the weighted average,
about 340 m, in **empty tunnel**, the one place nothing fits.

Step 3: Watch the Crowd Settle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L3/tunnel_pf_clusters.png
   :alt: How many places the crowd of particles is in, log scale, over 45 s: 23 at the start, then 17, then 4 at the first niche match near 2 s, 3 near 8 s, 2 at 14 s and 1 at 21 s. Green lines mark niche matches, a black line marks 12 s.
   :width: 60%
   :align: center

   How many places the crowd is in. Green lines are SOS niche matches; the
   black line is 12 s, the moment in Step 2.

.. figure:: /_static/images/L3/tunnel_pf_error.png
   :alt: The error in meters, log scale, over 45 s. The weighted average, orange, is 100 to 250 m off until 21 s, stepping down at each niche match, then drops below 1 m. The heaviest cluster, blue, is below 1 m from the first niche match near 2 s on.
   :width: 60%
   :align: center

   The error of two answers, on a log scale: the **heaviest cluster** (blue)
   and the **weighted average** (orange). Green lines are niche matches.

- **How many places.** 23 at the start, one under every light. Niches are not
  evenly spaced, so each one rules places out: 4 after the first, then 3,
  then 2, then 1 at 21 s.
- **Two ways to answer "where am I?".** The heaviest cluster is within a
  meter from about 2 s on. The weighted average stays 100 m or more off until
  the crowd is in one place.

.. important::

   With a particle filter, how you read the answer matters. While the belief
   has several peaks, report the heaviest one, never the average.

Step 4: Move the Sliders
^^^^^^^^^^^^^^^^^^^^^^^^

Before you touch the slider, guess how many particles you need. Forty runs
each, same drive, fresh random numbers:

.. list-table::
   :widths: 60 40
   :header-rows: 1
   :class: compact-table

   * - **Setting**
     - **Right place**
   * - 5,000 particles
     - 40 of 40
   * - 2,000 particles (default)
     - 40 of 40, by 21 s
   * - 500 particles
     - 33 of 40
   * - 100 particles
     - 11 of 40
   * - 30 particles
     - **1 of 40**
   * - camera :math:`\sigma = 0.2` m (:math:`R` too small)
     - 31 of 40

Two thousand is enough every time. Five hundred fails about one run in six.
At a hundred it is right about a quarter of the time, and at thirty almost
never. The last row tells the filter the camera is five times better than it
is (``--camera-sigma 0.2``), so :math:`R` is too small: good particles get
thrown away over small disagreements. The same overconfidence as before, in a
new form.

.. warning::

   **The failures are quiet:** one tight cluster, a confident answer, in the
   wrong place. The crowd collapsed onto a peak before the niches could rule
   it out, and the right place ran out of particles. No error, no warning.
   Set 100 particles and press **New draw** until you see one.


Notation Reference
------------------

Every symbol is introduced where it is first used in the lecture. These
tables collect them in one place, as a lookup.

Statistics
~~~~~~~~~~

.. list-table::
   :widths: 18 24 58
   :header-rows: 1
   :class: compact-table

   * - **Symbol**
     - **Name**
     - **Meaning**
   * - :math:`\mu`
     - mean
     - The average. Subscripted per axis: :math:`\mu_x`, :math:`\mu_y`.
   * - :math:`\mathbb{E}[\,\cdot\,]`
     - expectation
     - The average of what is inside, over every possible outcome, not just
       the readings we have.
   * - :math:`\operatorname{Var}(x)`
     - variance
     - How spread out the readings are, in *squared* units.
   * - :math:`\sigma`
     - standard deviation
     - The square root of the variance, back in the original units. **Most
       uncertainties in this course are quoted this way.**
   * - :math:`\operatorname{Cov}(x,y)`
     - covariance
     - How much the errors in :math:`x` and :math:`y` move together. Zero
       when they are unrelated.
   * - :math:`\mathcal{N}(\mu, \sigma^2)`
     - normal distribution
     - A bell curve with that mean and variance.

.. tip::

   Read :math:`\mathbf{w} \sim \mathcal{N}(0, Q)` aloud as: *the noise*
   :math:`\mathbf{w}` *is drawn from a bell curve centered on zero with
   covariance* :math:`Q`.

The State and the Two Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 18 24 58
   :header-rows: 1
   :class: compact-table

   * - **Symbol**
     - **Name**
     - **Meaning**
   * - :math:`x, y`
     - coordinates
     - Along and across the road (east and north in the motion-model appendix
       and the EKF). *Not bold.*
   * - :math:`\mathbf{x}`
     - the state
     - **Bold**: a whole vector being estimated, for example
       :math:`[p_x\ p_y\ v_x\ v_y]^\top`.
   * - :math:`\hat{\mathbf{x}}`
     - x-hat
     - The filter's **estimate**. The hat always means "our best guess at",
       never the truth.
   * - :math:`\hat{\mathbf{x}}^-`
     - x-hat-minus
     - The estimate **after predicting, before using the measurement**. The
       minus marks every predicted quantity.
   * - :math:`P`
     - state covariance
     - How uncertain the filter is, and how those uncertainties are linked.
       :math:`P^-` is its predicted version.
   * - :math:`F`
     - transition matrix
     - How the state changes on its own over one step.

Errors, Inputs and the Nonlinear Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 18 24 58
   :header-rows: 1
   :class: compact-table

   * - **Symbol**
     - **Name**
     - **Meaning**
   * - :math:`\mathbf{w}`, :math:`\mathbf{v}`
     - process error, measurement error
     - The unknown errors of one step's motion and of one reading, each drawn
       from :math:`\mathcal{N}(0, \cdot)`.
   * - :math:`Q`
     - process noise
     - How *wrong* :math:`F`'s prediction can be: the covariance of
       :math:`\mathbf{w}`. **Tuned, not measured.** In the tunnel it is built
       from :math:`\sigma_a`, the acceleration the IMU gets wrong.
   * - :math:`H`
     - measurement matrix
     - Which parts of the state the sensor observes.
   * - :math:`R`
     - measurement noise
     - How noisy the sensor is: the covariance of :math:`\mathbf{v}`.
       Measured, from the datasheet, or set, **never guessed**.
   * - :math:`B`
     - control matrix
     - Turns the control input :math:`\mathbf{u}` into changes of the state.
   * - :math:`\mathbf{z}`, :math:`\mathbf{u}`
     - measurement, control
     - What the sensor reported; what the vehicle did during the step:
       :math:`[a_x,\ a_y]` from the IMU in the KF, :math:`[v,\ \omega]` in the
       EKF.
   * - :math:`\Delta t`, :math:`k`
     - step length, time index
     - :math:`\Delta t`: the time between steps, 0.1 s. :math:`\mathbf{x}_k`
       is the state now, :math:`\mathbf{x}_{k-1}` one step ago.
   * - :math:`f, h`
     - nonlinear models
     - The nonlinear versions of :math:`F` and :math:`H`, used by the EKF,
       UKF and particle filter.
   * - :math:`\partial f/\partial \mathbf{x}`
     - Jacobian
     - The table of slopes of :math:`f`: how much each output moves when each
       input is nudged. The EKF's :math:`F_k` and :math:`H_k`;
       :math:`G = \partial f/\partial \mathbf{u}` builds :math:`Q_k`.

The Update and the UKF
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 18 24 58
   :header-rows: 1
   :class: compact-table

   * - **Symbol**
     - **Name**
     - **Meaning**
   * - :math:`\nu`
     - the innovation
     - Measurement minus predicted measurement. **The surprise.**
   * - :math:`S`
     - innovation covariance
     - How large the filter *expected* that surprise to be.
   * - :math:`K`
     - Kalman gain
     - What fraction of the surprise the filter acts on.
   * - :math:`\chi_i`, :math:`W_i`
     - sigma points, weights
     - The UKF's :math:`2n+1` stand-in points for the belief, and how much
       each counts. :math:`n` is the state size.
   * - :math:`\kappa`
     - spread
     - How far out the sigma points sit; :math:`n + \kappa = 3` is usual.
   * - :math:`\mathcal{Y}_i`, :math:`\mathcal{Z}_i`, :math:`P_{xz}`
     - pushed points, cross-covariance
     - The sigma points after :math:`f` and after :math:`h`; how state and
       reading move together, which replaces :math:`P^- H^\top`.

The Particle Filter, the Test, and Double Duty
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 18 24 58
   :header-rows: 1
   :class: compact-table

   * - **Symbol**
     - **Name**
     - **Meaning**
   * - :math:`\mathbf{x}^{(i)}`, :math:`w^{(i)}`
     - particle, weight
     - One of :math:`N` guesses at the state, and how much the particle filter
       believes it.
   * - :math:`p(\mathbf{z} \mid \mathbf{x})`, :math:`N_{\text{eff}}`
     - likelihood, effective count
     - How likely the reading is if the state were :math:`\mathbf{x}`; how
       many particles still carry real weight (resample when below
       :math:`N/2`).
   * - :math:`\varepsilon`
     - the NIS
     - Normalized innovation squared, :math:`\nu^\top S^{-1}\nu`: the honesty
       check.
   * - :math:`\chi^2_m`
     - chi-square
     - The spread of values :math:`\varepsilon` should show if the filter is
       honest, with :math:`m` degrees of freedom.
   * - :math:`m`
     - degrees of freedom
     - How many numbers the sensor reports at once. Two, for a sign match
       giving :math:`x` and :math:`y`.

.. admonition:: Two symbols do double duty
   :class: warning

   :math:`x` is a road coordinate in plain italics and a whole state vector
   in bold :math:`\mathbf{x}`. The typeface is the only difference. And
   :math:`n` counts readings in :math:`\sigma/\sqrt{n}`, but counts the size
   of the state in the UKF's :math:`2n+1` sigma points. :math:`w` is the
   process error (:math:`\mathbf{w}`), a sigma-point weight (:math:`W_i`) and
   a particle weight (:math:`w^{(i)}`); :math:`\chi` is a sigma point
   (:math:`\chi_i`) and the chi-square band (:math:`\chi^2_m`).

.. note::

   **Other textbooks write the innovation as** :math:`\mathbf{y}`. We use
   :math:`\nu` because :math:`y` is already the across-road coordinate, and
   the two would collide in exactly the formulas where clarity matters most.
   The tracking literature (Bar-Shalom et al., 2001) uses :math:`\nu` too.
