====================================================
Code
====================================================

The L6 hands-on is the folder ``lecture6/`` of
`enpm818z-fall-2026-carla-python
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python>`_. It has five
parts, all on **one recorded CARLA drive**, the same drive the lecture uses
for every method. It needs Python with ``numpy``, ``scipy`` and
``matplotlib``. It needs **no CARLA and no ROS**: the drive is already
recorded and ships with the folder.

.. list-table::
   :widths: 14 30 56
   :header-rows: 1
   :class: compact-table

   * - **Part**
     - **What it shows**
     - **Lecture section**
   * - ``gnss``
     - the GNSS fixes: scatter, bias and the outage
     - GNSS and RTK (hands-on, part 1)
   * - ``dr``
     - dead reckoning: wheels and gyro, no GNSS
     - Dead Reckoning (hands-on, part 2)
   * - ``ekf``
     - the fused filter: 8 runs, from results files
     - Fusion in the EKF (hands-on, part 3)
   * - ``mcl``
     - Monte Carlo localization (MCL) on the map
     - Against a Map (hands-on, part 4)
   * - ``icp``
     - ICP scan matching, one iteration at a time
     - Against a Map (hands-on, part 4)


Run It
------

Get the repository, then go to the folder:

.. code-block:: bash

   git clone https://github.com/rubixcubic/enpm818z-fall-2026-carla-python.git
   cd enpm818z-fall-2026-carla-python/lecture6

Each part opens a matplotlib window:

.. code-block:: bash

   python3 l6_handson.py --part gnss   # 1. the GNSS fixes: scatter, bias and the outage
   python3 l6_handson.py --part dr     # 2. dead reckoning: wheels + gyro, no GNSS
   python3 l6_handson.py --part ekf    # 3. the fused filter: 8 runs, from results files
   python3 l6_handson.py --part mcl    # 4. Monte Carlo localization on the map
   python3 l6_handson.py --part icp    # 5. ICP scan matching, one iteration at a time

   # variants for the questions below
   python3 l6_handson.py --part mcl --particles 200 --seed 1
   python3 l6_handson.py --part mcl --kidnap 40 0 10
   python3 l6_handson.py --part mcl --kidnap 40 0 10 --random 20
   python3 l6_handson.py --part icp --icp-start 4 -3 15
   python3 l6_handson.py --part icp --icp-start 6 -4 20

   # save a still instead of opening a window
   python3 l6_handson.py --part ekf --snapshot ekf.png


Options
~~~~~~~

.. list-table::
   :widths: 30 12 58
   :header-rows: 1
   :class: compact-table

   * - **Option**
     - **Part**
     - **What it does**
   * - ``--part gnss|dr|ekf|mcl|icp``
     - all
     - Which part to run. Required.
   * - ``--particles N``
     - ``mcl``
     - The number of particles. Default 2000.
   * - ``--seed S``
     - ``mcl``
     - The random seed. Default 818. The same seed gives the same run.
   * - ``--kidnap T EAST NORTH``
     - ``mcl``
     - At T seconds, every particle jumps EAST and NORTH meters, as if the
       AV had been moved without telling MCL.
   * - ``--random K``
     - ``mcl``
     - After each scan, K particles get random poses, any heading, near
       MCL's estimate. Default 0.
   * - ``--random-radius R``
     - ``mcl``
     - How near: within R meters of MCL's estimate. Default 20.
   * - ``--icp-start EAST NORTH DEG``
     - ``icp``
     - How far off the truth ICP starts: EAST meters east, NORTH meters
       north, DEG degrees of heading. Default ``1.5 -1.0 5``: 1.5 m east,
       1.0 m south and :math:`5^\circ` off.
   * - ``--time T``
     - ``gnss``
     - Opens at T seconds instead of the start. The figures on this site use
       ``--time 61.55``, the middle of the outage.
   * - ``--snapshot FILE``
     - all
     - Saves the figure as a PNG file instead of opening a window. ``ekf``
       saves its default run (outage on, wheels on, map matching off),
       ``gnss`` saves the start (or ``--time T``), and ``icp`` saves its last
       iteration.
   * - ``--html FILE``
     - all
     - Saves the figure as an HTML page instead of opening a window. It needs
       the ``mpld3`` package; without it, the script stops and suggests
       ``--snapshot``.


What Each Part Shows
--------------------

Part 1: The GNSS Fixes (``--part gnss``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The GNSS fixes as they arrive, against the true route. A fix comes once a
second, then none for the outage. The window opens at the start. **Play**
runs the drive from start to finish, one second of driving per tick (about
13 s in all); press it again to pause. **Step: +1 s** moves one second, one
fix, at a time. **Reset** stops and goes back to the start. Four panels:

- **Top left, the whole route:** the truth so far in black, the fixes so far
  as blue dots, the **GNSS-only path** (the fixes joined in order: where the
  AV would think it drove from GNSS alone), the last fix circled, and the AV,
  drawn 3 times its size so it shows at this zoom. Inside the outage, the
  title says how long since the last fix and how far the AV drove since.
- **Top right, a close-up** 40 m across that follows the AV, at true size,
  with a dashed 1.5 m circle (the noise we chose) around the last fix.
- **Bottom left:** not a map. Each fix's error, east and north, against
  time. The dashed lines are the mean errors; the shaded band is the time
  from the last fix before the outage to the first fix after it.
- **Bottom right:** the same errors as points, filling in as the fixes
  arrive: blue so far, gray still to come, the newest circled. Their center
  is the bias, their spread the noise, next to the bias and the 1.5 m we
  chose.

On our drive the script measures 72 fixes, a mean error of 0.36 m east and
0.49 m south, and a spread of 1.47 m east and 1.49 m north. The errors we
chose were a bias of 0.5 m east and 0.3 m south and noise of 1.5 m: a mean of
72 noisy fixes is only that close. From the last fix to the first fix after
it: 55.0 s and 401 m.

The AV is drawn with ``l6common.draw_av``: its base link (the middle of the
rear axle) sits on the AV's position, turned to its heading.

**What to look for:** the two laps cover the same road, so on the map the
gap is hidden: the other lap's fixes fill it. The gap shows in time. Step
into the outage and watch the distance since the last fix grow.


Part 2: Dead Reckoning (``--part dr``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pose from the wheel speed and the gyro's yaw rate alone, with no GNSS,
against the truth. **Dead reckoning** starts from a known pose and adds up
how far the AV drove and how much it turned. The script starts it from the
true pose at the last fix before the outage, as the lecture does, and runs it
through the outage to the next fix, 401 m on.

- **Left:** the road from above, the truth in black and dead reckoning in
  rust.
- **Right, top:** not a map. The position error against the distance driven
  since the last fix.
- **Right, bottom:** the heading error against the same distance.
- **Check boxes** (under the map): the errors we chose. Untick **gyro bias**
  to subtract the 0.001 rad/s from every gyro reading; untick **wheels 0.5 %
  fast** to divide every wheel reading by 1.005. Dead reckoning runs again
  at once. What stays is the sensors' noise and CARLA's own gyro, which
  reports a little more turning than the AV makes in a corner.

**What to look for:** where does the heading error step up, on the straights
or at the corners? Which chosen error, when removed, shrinks the position
error most? The Dead Reckoning section of the lecture explains both.


Part 3: The Fused Filter (``--part ekf``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important::

   **This part shows precomputed results files, not a filter.** The eight
   runs were computed in advance and saved in ``ekf_results/`` (one ``.npz``
   file per run, and ``manifest.json``). The folder has **no filter code**.
   You build the filter yourself in GP3, Task 2.

Three check boxes on the left pick the run: **GNSS outage**, **wheels** and
**map matching**. Each combination is one run of the filter, so the eight
combinations are the eight runs, and you can switch between them instantly.
The window opens on outage on, wheels on, map matching off.

The window has one panel: the filter's real position error against time
(blue line), and the filter's **own** :math:`1\sigma`, how big it thinks its
error is (shaded band). The title gives the run's APE RMSE and its worst
error. APE, the absolute pose error, is the distance from the estimated
position to the true one at each time step, summarized by the RMSE (square,
average, take the root).

**What to look for:** in the outage, does the shaded band grow as fast as
the error? Note the APE of each run: which input lowers it most?


Part 4: Monte Carlo Localization (``--part mcl``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MCL is the particle filter of :doc:`L3 </lectures/lecture3/l3_index>`,
given a map. Each particle is one guess of the pose. The AV has just been
switched on: 2000 particles start anywhere within 20 m of the first GNSS
fix, with any heading. MCL weighs them with one scan every 0.5 s.

The script runs MCL over the whole drive before the window opens. It prints
a line to say it is computing; the window opens about 12 s later (measured
on the machine these pages were checked on, 2000 particles).

- **Left:** the map in gray, MCL's estimate (the weighted mean of the
  particles) in green, and the truth in black.
- **Right:** MCL's error and the spread of its particles, against time.
  With ``--kidnap``, a dotted line marks the moment every particle jumps.

Measured with the default seed: the error is first under 1 m at the 5th
scan, 2.0 s after the first scan; after the first 10 s its median is 0.20 m
and its worst 0.95 m.

**What to look for:** how long until the error is under 1 m? Is a small
spread the same as a small error? Where does the error rise again? Then cut
the particles with ``--particles 200`` and try three values of ``--seed``:
does MCL still find the AV, and how fast? Then kidnap it with
``--kidnap 40 0 10``, and try ``--random 20``.


Part 5: ICP (``--part icp``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ICP, iterative closest point, on one LiDAR scan from the middle of the drive.
The scan starts off the truth by ``--icp-start`` and is matched to the map.
Drag the **iteration** slider to step through the fit: 0 is the start, and
the title gives the RMSE of the pairs at each iteration. The plot shows the
map points within 40 m of the AV (gray) and the scan (rust).

On the slides, the default start (:math:`5^\circ` off, 1.5 m east and 1.0 m
south of the truth) takes 28 iterations; the RMSE of the pairs falls from
1.32 m to 0.06 m, and the final pose is 0.02 m and :math:`0.02^\circ` from
the truth.

**What to look for:** how many iterations until the RMSE stops falling?
Which walls pull the scan into place first? Then start it far off:
``--icp-start 4 -3 15`` is 5 m and :math:`15^\circ` off, and
``--icp-start 6 -4 20`` is 7.2 m and :math:`20^\circ` off. Which one still
lands on the walls?


The Data
--------

``record_drive.py`` drove one route in CARLA twice:

- The **mapping pass** recorded LiDAR scans at the true poses and stitched
  them into the map, ``l6_map.npz``.
- The **localization pass** drove the route again. It is ``l6_drive.csv``
  and ``l6_scans.npz``. Every method gets only its sensors, never the true
  pose.

``l6_drive_meta.json`` lists the town, the route and every value below.
Measured on the localization pass:

- CARLA town ``Town10HD_Opt``, driven counterclockwise by CARLA's autopilot;
- 916 m in 125.7 s, two laps of a downtown block, mean speed 7.3 m/s;
- no GNSS from 250 m to 650 m along the route: 34.2 s to 89.0 s, 54.8 s;
- the map: 18,661 points from the mapping pass.

**Frames.** The **map frame** is fixed to the ground: :math:`x` east and
:math:`y` north, in meters. CARLA's :math:`y` points the other way, so the
recorder flips it. The **vehicle frame** is fixed to the AV: :math:`x`
forward and :math:`y` left.


The Drive File
~~~~~~~~~~~~~~

``l6_drive.csv`` has one row every 0.05 s:

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Column**
     - **Meaning**
   * - ``t``
     - time (s), one row every 0.05 s
   * - ``x``, ``y``, ``theta``
     - where the AV **really** is. Ground truth: never read it inside a
       filter.
   * - ``v``
     - the AV's **true** speed (m/s)
   * - ``gyro_z``
     - what the gyro **says** the yaw rate is (rad/s)
   * - ``wheel_v``
     - what the wheels **say** the speed is (m/s)
   * - ``gnss_x``, ``gnss_y``
     - the GNSS fix (m), once a second. Empty between fixes and during the
       outage.

``l6_scans.npz`` holds the scans in the vehicle frame. Read them with
``l6common.load_scans``.


The Sensor Errors
~~~~~~~~~~~~~~~~~

CARLA's sensors are too clean, and CARLA has no wheel encoder. So the
recorder starts from the true motion and adds these errors. **Every value is
chosen**; none is measured from a real car.

.. list-table::
   :widths: 18 22 60
   :header-rows: 1
   :class: compact-table

   * - **Sensor**
     - **Rate**
     - **Error added (chosen)**
   * - GNSS
     - 1 fix per second
     - noise :math:`\sigma = 1.5` m in :math:`x` and in :math:`y`; a fixed
       bias of 0.5 m east and 0.3 m south; no fixes for 400 m
   * - Wheel speed
     - 20 per second
     - reads 0.5% fast (a worn tire); noise :math:`\sigma = 0.05` m/s
   * - Gyro (yaw rate)
     - 20 per second
     - bias 0.001 rad/s; noise :math:`\sigma = 0.01` rad/s
   * - LiDAR
     - 10 scans per second
     - none added; we keep points within 0.3 m of sensor height, one per
       20 cm square

The 400 m without fixes stands in for a street between tall buildings:
CARLA's GNSS sensor never loses the sky.


The Code
--------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **What it holds**
   * - ``l6common.py``
     - loading the drive, dead reckoning, and the absolute pose error (APE)
   * - ``icp.py``
     - ICP's step 2, the best turn and shift for a set of pairs, and the ICP
       loop. It follows the lecture's six steps (centroids, center,
       compare, angle, turn, shift), but finds the angle and the turn in one
       go with the SVD of :math:`H`, with a check that :math:`R` never
       mirrors. In 2-D this gives the same turn as the lecture's atan2
       formula.
   * - ``mcl.py``
     - the likelihood field, and predict, weigh and resample
   * - ``record_drive.py``
     - the recorder (needs CARLA; you do not need to run it)
   * - ``l6_handson.py``
     - the five parts

The likelihood field's formula and its values, and why each was chosen,
are on the Weigh slides of :doc:`l6_lecture`; :doc:`Going Further
<l6_appendix>` draws the field around a corner. Going Further also has ICP's
step 2 on a worked example, the SVD form of the turn, and why the course
code stops with an error when all the points lie on one line.


Run the Tests
~~~~~~~~~~~~~

From ``lecture6/``:

.. code-block:: bash

   python3 -m pytest tests -q

The tests check the shared code (dead reckoning, APE, loading the files),
the ICP fit (including the three-pair worked example of Going Further and
points on one line), MCL (finding the pose in a box with a pillar, and the
kidnap and random-particle options), and that each of the five parts saves
a snapshot.
On the machine these pages were checked on (2026-10-16), the 34 tests passed
in 6 s.


Hands-on Exercises
------------------

The reference numbers come from the shipped drive (CARLA ``Town10HD_Opt``,
two laps, 916 m in 125.7 s; no GNSS from 250 m to 650 m along the route,
34.2 s to 89.0 s) and the default seed 818, unless a seed is named.

1. **Dead reckoning.** In ``--part dr``, watch the heading error. Where does
   it step up: on the straights or at the corners? Untick **gyro bias**, then
   **wheels 0.5 % fast**: which error matters more?

   *Reference:* with both errors ticked, dead reckoning is 2.69 m off after
   100 m, at worst 9.03 m (at 329 m), and 7.84 m at the next fix, 401 m on;
   the heading ends :math:`6.0^\circ` off, almost all of it gained in the
   turns. Without the gyro bias the worst error is 4.33 m; without the
   wheel error, 9.24 m; without both, 4.49 m, with the heading still
   :math:`2.8^\circ` off from the sensors' noise and CARLA's own gyro.

2. **The fused filter.** In ``--part ekf``, compare the APE of the eight
   runs. Which input lowers it most? During the outage, does the filter's
   :math:`1\sigma` grow as fast as its error?

   *Reference (APE RMSE as on the slides, worst error as in the window's
   title, m):*

   .. list-table::
      :widths: 20 20 20 20 20
      :header-rows: 1
      :class: compact-table

      * - **GNSS**
        - **Wheels**
        - **Map**
        - **APE RMSE**
        - **Worst**
      * - outage
        - yes
        - no
        - 4.99
        - 9.50
      * - outage
        - yes
        - yes
        - 0.52
        - 2.49
      * - outage
        - no
        - no
        - 4.58
        - 12.36
      * - outage
        - no
        - yes
        - 27.66
        - 65.62
      * - always
        - yes
        - no
        - 1.28
        - 2.61
      * - always
        - yes
        - yes
        - 0.47
        - 2.38
      * - always
        - no
        - no
        - 1.97
        - 5.93
      * - always
        - no
        - yes
        - 1.38
        - 6.81

   The window's title prints two APEs rounded the other way, 0.51 and
   27.67 m: the stored values are 0.515 and 27.665 m. With wheels and no
   map, the filter's :math:`1\sigma` is 3.93 m at the outage's worst moment,
   where the real error is 9.50 m. The run "outage, no wheels, map" loses
   the map at 45 s and stays lost until GNSS returns at 89.0 s: the lecture's
   slide "The run that failed" explains why.

3. **MCL.** In ``--part mcl``, run ``--particles 200`` with five seeds, then
   2000 particles with the same seeds. Does every run find the AV? How fast?

   *Reference (seeds 0 to 4):* every run finds the AV in the end. With 200
   particles, seeds 1 and 4 stay 5 to 10 m off until 64.0 s and 60.5 s; with
   2000, every run is within 2 m of the AV by 33.5 s. Median error after the
   first 10 s: 0.29, 0.78, 0.29, 0.37, 0.70 m with 200 particles; 0.28,
   0.21, 0.27, 0.20, 0.34 m with 2000.

4. **ICP.** In ``--part icp``, raise ``--icp-start`` until ICP stops landing
   on the walls. How far off can it start?

   *Reference (middle scan):* ``1.5 -1 5``, ``3 -2 10`` and ``4 -3 15`` land
   within 0.10 m of the truth; ``6 -4 20`` ends 7.09 m off.

5. **Kidnap MCL.** Run ``--part mcl --kidnap 40 0 10`` with seeds 0 to 4:
   at 40 s every particle jumps 10 m north. Does MCL find the AV again? Then
   try ``--kidnap 40 0 30``. Then add ``--random 20`` and ``--random 100`` to
   ``--kidnap 40 0 10``: do random particles help?

   *Reference (seconds after the jump until the error is first under 1 m,
   seeds 0 to 4):* ``--kidnap 40 0 10``: 21.6, 16.6, 16.6, 45.1, 10.6.
   ``--kidnap 40 0 30``: never, 72.1, never, never, never. With
   ``--random 20``: 4.6, never, 21.1, 6.1, never. With ``--random 100``:
   3.6, 11.1, 2.6, 1.6, 10.1. The two runs that never return with 20 random
   particles end 29.8 m (seed 1) and 73.4 m (seed 4) off, while their
   spread stays small: a small spread does not mean MCL is right.
