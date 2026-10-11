====================================================
Code
====================================================

The L6 hands-on is the folder ``lecture6/`` of
`enpm818z-fall-2026-carla-python
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python>`_. It has four
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
   * - ``dr``
     - dead reckoning: wheels and gyro, no GNSS
     - Dead Reckoning
   * - ``ekf``
     - the fused filter: 8 runs, from results files
     - Fusion in the EKF; Integrity (its NIS)
   * - ``mcl``
     - Monte Carlo localization (MCL) on the map
     - Against a Map
   * - ``icp``
     - ICP scan matching, one iteration at a time
     - Against a Map


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
   * - ``--icp-start EAST NORTH DEG``
     - ``icp``
     - How far off the truth ICP starts: EAST meters east, NORTH meters
       north, DEG degrees of heading. Default ``1.5 -1.0 5``: 1.5 m east,
       1.0 m south and :math:`5^\circ` off.
   * - ``--snapshot FILE``
     - all
     - Saves the figure as a PNG file instead of opening a window. ``ekf``
       saves its default run (outage on, wheels on, map matching off),
       ``gnss`` saves the middle of the outage, and ``icp`` saves its last
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
second, then none for the outage. The window opens in the middle of the
outage; drag the time slider to move through the drive.

- **Left:** the road from above. The truth so far in black, the fixes so far
  as blue dots, the AV now as a black dot, and the last fix circled. Inside
  the outage, the title says how long since the last fix and how far the AV
  drove since.
- **Right:** not a map. Each fix's error, east and north, against time. The
  dashed lines are the mean errors; the shaded band is the time from the last
  fix before the outage to the first fix after it.

On our drive the script measures 72 fixes, a mean error of 0.36 m east and
0.49 m south, and a spread of 1.47 m east and 1.49 m north. The errors we
chose were a bias of 0.5 m east and 0.3 m south and noise of 1.5 m: a mean of
72 noisy fixes is only that close. From the last fix to the first fix after
it: 55.0 s and 401 m.

**What to look for:** the two laps cover the same road, so on the map the
gap is hidden: the other lap's fixes fill it. The gap shows in time. Move the
slider into the outage and watch the distance since the last fix grow.


Part 2: Dead Reckoning (``--part dr``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pose from the wheel speed and the gyro's yaw rate alone, with no GNSS,
against the truth. **Dead reckoning** starts from a known pose and adds up
how far the car drove and how much it turned. The script starts it from the
true pose at the last fix before the outage, as the lecture does, and runs it
through the outage to the next fix, 401 m on.

- **Left:** the road from above, the truth in black and dead reckoning in
  rust.
- **Right:** not a map. It is the position error against the distance
  driven since the last fix.

**What to look for:** where does the error start to grow fast? On a straight
or in a turn? Think about the heading. The Dead Reckoning section of the
lecture shows why a heading error matters most.


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

- **Top:** the filter's real position error (blue line), and the filter's
  **own** :math:`1\sigma`, how big it thinks its error is (shaded band). The
  title gives the run's APE RMSE and its worst error. APE, the absolute pose
  error, is the distance from the estimated position to the true one at each
  time step, summarized by the RMSE (square, average, take the root).
- **Bottom:** the NIS of each update (the honesty test of
  :doc:`L3 </lectures/lecture3/l3_index>`), blue dots for GNSS fixes and
  green dots for poses from map matching.

**What to look for:** in the outage, does the shaded band grow as fast as
the error? If it does, the filter is honest about not knowing. Note the APE
of each run: which input lowers it most?


Part 4: Monte Carlo Localization (``--part mcl``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MCL is the particle filter of :doc:`L3 </lectures/lecture3/l3_index>`,
given a map. Each particle is one guess of the pose. The car has just been
switched on: 2000 particles start anywhere within 20 m of the first GNSS
fix, with any heading. MCL weighs them with one scan every 0.5 s.

- **Left:** the map in gray, MCL's estimate (the weighted mean of the
  particles) in green, and the truth in black.
- **Right:** MCL's error and the spread of its particles, against time.

On the slides, this start gives an error first under 1 m at the 5th scan,
2.0 s in; after 10 s, a median error of 0.20 m and a worst of 0.95 m.

**What to look for:** how long until the spread is under 1 m? Where does
the error rise again, and what does the LiDAR see there? Then cut the
particles with ``--particles 200`` and try three values of ``--seed``: does
MCL still find the car, and how large is the error now?


Part 5: ICP (``--part icp``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ICP, iterative closest point, on one LiDAR scan from the middle of the drive.
The scan starts off the truth by ``--icp-start`` and is matched to the map.
Drag the **iteration** slider to step through the fit: 0 is the start, and
the title gives the RMSE of the pairs at each iteration. The plot shows the
map points within 40 m of the car (gray) and the scan (rust).

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
     - CARLA's; a flat 2-D slice at sensor height, one point per 20 cm
       square

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
     - the five-step rigid fit (SVD) and the ICP loop. The five steps are
       the lecture's: centroids, centering, the cross-covariance
       :math:`H`, the rotation, the shift.
   * - ``mcl.py``
     - the likelihood field, and predict, weigh and resample
   * - ``record_drive.py``
     - the recorder (needs CARLA; you do not need to run it)
   * - ``l6_handson.py``
     - the four parts

The likelihood field's numbers, and why each was chosen, are in
:doc:`Going Further <l6_appendix>`. So is the general form of ICP's rotation
step, and why the course code stops with an error when all the points lie
on one line.


Run the Tests
~~~~~~~~~~~~~

From ``lecture6/``:

.. code-block:: bash

   python3 -m pytest tests -q

The tests check the shared code (dead reckoning, APE, loading the files),
the ICP fit (including the lecture's three-pair worked example and points
on one line), MCL (finding the pose in a box with a pillar), and that each
of the four parts saves a snapshot. On the machine these pages were checked
on, the 29 tests passed in 165 s.


Hands-on Exercises
------------------

The reference numbers come from the shipped drive (CARLA ``Town10HD_Opt``,
two laps, 916 m in 125.7 s; no GNSS from 250 m to 650 m along the route,
34.2 s to 89.0 s) and the default seed 818, unless a seed is named.

1. **Dead reckoning.** In ``--part dr``, find the stretch where the error
   grows fastest. Explain it with the heading error, not the speed error.

   *Reference:* started from the true pose at the last fix before the
   outage, dead reckoning is 2.69 m off after 100 m, 3.56 m after 200 m,
   8.24 m after 300 m, at worst 9.03 m (at 329 m), and 7.84 m at the end of
   the outage. ``--part dr`` itself starts at the beginning of the drive, so
   its curve is not the same one.

2. **The fused filter.** In ``--part ekf``, compare the APE of the eight
   runs. Which input lowers it most? During the outage, does the filter's
   :math:`1\sigma` grow as fast as its error?

   *Reference (APE RMSE and worst error, m):*

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
        - 2.62
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

   With wheels and no map, the filter's :math:`1\sigma` is 3.93 m at the
   outage's worst moment, where the real error is 9.50 m. The run "outage,
   no wheels, map" loses the map at 45 s and stays lost until GNSS returns:
   find out why in its NIS plot.

3. **MCL.** In ``--part mcl``, run ``--particles 200`` with five seeds. How
   many of them find the car? Then try 2000 particles.

   *Reference (seeds 0 to 4, median error after the first 10 s):* 200
   particles: 0.29, 0.78, 0.29, 0.37, 0.70 m; 2000 particles: 0.28, 0.21,
   0.27, 0.20, 0.34 m. All ten runs find the car.

4. **ICP.** In ``--part icp``, raise ``--icp-start`` until ICP stops landing
   on the walls. How far off can it start?

   *Reference (middle scan):* ``1.5 -1 5``, ``3 -2 10`` and ``4 -3 15`` land
   within 0.10 m of the truth; ``6 -4 20`` ends 7.09 m off.
