====================================================
Code
====================================================

L3 has two kinds of code. The Python scripts run every filter of the lecture on
recorded data, with no simulator: they need only Python 3, ``numpy`` and
``matplotlib``. The ROS 2 package runs a filter live, on the sensors of the L2
bridge in CARLA.

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Repository**
     - **What L3 uses from it**
   * - `enpm818z-fall-2026-carla-python
       <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python>`_
     - Folder ``lecture3/``: the four filters on one dataset, and three
       interactive tunnels (Kalman filter, EKF and UKF, particle filter).
   * - `enpm818z-fall-2026-carla-ros
       <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros>`_
     - The ROS 2 package ``l3_ekf_demo``, which subscribes to ``l2_carla_demo``.


Four filters, one dataset: ``lecture3/``
----------------------------------------

The AV drives a curvy road for 60 s. Its wheel speed and yaw rate are measured
every 0.1 s, and a GNSS fix arrives once a second with :math:`\sigma = 2` m.
Every filter of the lecture runs on that same drive, prints its error and its
NIS, and saves a figure.

.. code-block:: bash

   cd enpm818z-fall-2026-carla-python/lecture3
   python3 make_dataset.py          # writes the two CSV files (already included)
   python3 kf_cv.py                 # then ekf.py, ukf.py, pf.py

.. list-table::
   :widths: 25 45 30
   :header-rows: 1
   :class: compact-table

   * - **Script**
     - **What it runs, and its arguments**
     - **Figure it writes**
   * - ``kf_cv.py``
     - The plain Kalman filter, GNSS only, state
       :math:`[p_x, p_y, v_x, v_y]`. ``--sigma-a`` (5.0 m/s²) sets Q.
     - ``kalman_filter.png``
   * - ``ekf.py``
     - The EKF: the AV turns, state :math:`[x, y, \theta]`, input
       :math:`[v, \omega]`. ``--heading-error`` (0 degrees) at the start;
       ``--gate`` skips a fix whose NIS is above 9.21; ``--check-jacobian``
       compares the Jacobian with finite differences and stops.
     - ``ekf.png``
   * - ``ukf.py``
     - The UKF on the same AV, no Jacobian, 7 sigma points.
       ``--heading-error``.
     - ``ukf.png``
   * - ``pf.py``
     - The particle filter. ``--particles`` (1000), ``--jitter`` (0.3 m after
       resampling), ``--global`` (start with no idea where the AV is).
     - ``particle_filter.png``

Every script also takes ``--data`` (default ``l3_drive.csv``). Give it
``l3_drive_multipath.csv``, the same drive with four GNSS fixes pushed 8 to
12 m off, to test the gate. ``l3common.py`` holds what the four share: the data
loader, the RMSE and NIS report, the plot, and the NIS limits (95 percent band
0.051 to 7.378 for two numbers, gate 9.21). Each figure is written next to the
script; running ``ekf.py`` again overwrites ``ekf.png``.

``README.md`` in the folder has six exercises, each with the numbers you
should see.


Interactive: the tunnel Kalman filter, ``lecture3/tunnel_kf/``
---------------------------------------------------------------

The running example of the lecture: the AV in a tunnel, GNSS lost, the IMU's
acceleration as the input, and an exit sign every 25 m matched against the HD
map. See also :ref:`l3-kf-hands-on`.

.. code-block:: bash

   cd lecture3/tunnel_kf
   python3 kf_tunnel.py                       # the live window
   python3 kf_tunnel.py --html tunnel_kf.html # a page that plays in a browser

.. list-table::
   :widths: 25 20 55
   :header-rows: 1
   :class: compact-table

   * - **Argument**
     - **Default**
     - **Meaning**
   * - ``csv``
     - ``tunnel_drive.csv``
     - The drive: 45 s, 451 rows, 19 sign matches.
   * - ``--make-csv``
     - off
     - Write the dataset again and stop.
   * - ``--sigma-a``
     - 0.5
     - Sets Q.
   * - ``--sigma-sign``
     - 1.0
     - Sets R, the sign match's :math:`\sigma` in meters.
   * - ``--no-control``
     - off
     - Predict without the IMU (no :math:`Bu`).
   * - ``--html``
     - none
     - A self-contained page, about 20 MB.
   * - ``--snapshot``, ``--frame``
     - none, 11.0
     - A PNG of the window at time ``--frame``.
   * - ``--panels PREFIX``
     - none
     - ``PREFIX_sigma.png`` and ``PREFIX_error.png``.

The window has sliders for Q and R, a box to turn the IMU on and off, and play,
pause and restart. The console prints the error along the tunnel, the final
:math:`\sigma` and the percent of time the truth is inside :math:`1\sigma`.
Needs ``python3-tk`` for the window.


Interactive: EKF and UKF on a curve, ``lecture3/curved_tunnel/``
----------------------------------------------------------------

A tunnel that bends 120 degrees, a camera that measures range and bearing to
the signs: the measurement is no longer a straight line, so the EKF is needed.

.. code-block:: bash

   cd lecture3/curved_tunnel
   python3 ekf_curve.py --check-jacobian
   python3 ekf_curve.py
   python3 ukf_curve.py

``ekf_curve.py``: ``--gyro-noise`` (2.0 deg/s), ``--range-noise``
(1.0 m), ``--check-jacobian``, ``--wrong-sign``, and the same ``--make-csv``,
``--html``, ``--snapshot``/``--frame`` (9.0) and ``--panels`` as above. The
window has a box that puts a wrong sign in the Jacobian.

``ukf_curve.py``: the UKF next to the EKF on the same drive, both compared
with the exact belief from 4000 particles. ``--heading-sigma`` (12 degrees at
the entrance), ``--dark`` (5 s without a sign), plus ``--html``, ``--snapshot``,
``--frame`` (5.0) and ``--panels``.

The data: ``curve_drive.csv``, 212 rows, 9 sign matches. ``README.md`` has the
tables and four exercises.


Interactive: the particle filter, ``lecture3/pf_tunnel/``
---------------------------------------------------------

The AV restarts inside a 700 m tunnel and does not know where it is. The camera
sees 23 identical lights and 5 irregular SOS niches (``tunnel_map.csv``).

.. code-block:: bash

   cd lecture3/pf_tunnel
   python3 pf_tunnel.py                 # the live window
   python3 pf_tunnel.py --trials 40     # how often it settles on the right place

Arguments: ``--particles`` (2000), ``--camera-sigma`` (1.0 m), ``--map``
(``tunnel_map.csv``), ``--trials N``, and ``--make-csv``, ``--html``,
``--snapshot``/``--frame`` (12.0), ``--panels`` as above. The window has Pause,
Restart and New draw buttons and sliders for the particle count and R. The data:
``pf_drive.csv``, 451 rows, 24 matches.


ROS 2 package: ``l3_ekf_demo``
------------------------------

A filter running live on the L2 bridge's GNSS and IMU in CARLA, with the NIS
logged so the covariance can be checked rather than believed. Only ``truth``
talks to CARLA, and it never ticks: the bridge owns the clock.

.. code-block:: bash

   cd ~/enpm818z_ws
   colcon build --symlink-install --packages-select l2_carla_demo l3_ekf_demo
   source install/setup.bash
   ros2 launch l2_carla_demo demo.launch.py rviz:=false     # terminal 1
   ros2 launch l3_ekf_demo ekf.launch.py                    # terminal 2

**Launch arguments:** ``log_csv`` (``l3_log.csv``), ``rviz`` (true),
``role_name`` (``ego``, the name the L2 bridge gives its vehicle). The launch
starts ``truth``, ``logger``, ``ekf`` and RViz, which shows the truth in green
and the estimate in blue with its covariance ellipse.

.. list-table::
   :widths: 18 82
   :header-rows: 1
   :class: compact-table

   * - **Node**
     - **What it does**
   * - ``truth``
     - CARLA's true pose of the AV, which a real vehicle never has, on
       ``/carla/ego_vehicle/odometry_truth`` (``Odometry``), stamped with the
       simulation time like the sensors. Parameters: ``host``, ``port``,
       ``role_name`` (``ego``). The filter never subscribes to it.
   * - ``logger``
     - Task 1: GNSS, IMU and truth into one CSV (columns ``t, source, a, b``;
       GNSS rows are in degrees). Parameter ``out`` (``l3_log.csv``).
   * - ``ekf``
     - Tasks 2 and 3: the filter, state :math:`[p_x, p_y, v_x, v_y]` in the
       same frame as the bridge's ``map`` and the truth (:math:`x` east,
       :math:`y` north). IMU acceleration, rotated from the AV's axes by the
       IMU's heading, drives predict; GNSS drives update. CARLA's GNSS is
       mirrored (latitude grows with CARLA's :math:`+y`, which is south), so
       the node flips north before the update. Publishes
       ``/l3/ekf/odometry`` (with the covariance) and ``/l3/ekf/nis``. Every 10 s it reports the percent of NIS values inside
       the 95 percent band; after 10 rejected fixes in a row it reports the
       filter unhealthy.
   * - ``plot_nis``
     - Not a node: Task 3's plot of the NIS against its band.

**The parameters** (``config/ekf.yaml``): ``gnss_sigma_m`` 1.5 (R),
``accel_process_sigma`` 1.5 m/s² (Q, "the knob"), ``nis_dof`` 2, the band
``nis_lo_chi2`` 0.051 to ``nis_hi_chi2`` 7.378, ``nis_gate_chi2`` 9.21,
``gate_enabled`` false (Exercise 5 turns it on), ``max_consecutive_rejects``
10, and ``latch_first_fix`` true (the first GNSS fix is the local origin).

.. code-block:: bash

   # the nodes one by one, from the package folder
   ros2 run l3_ekf_demo truth
   ros2 run l3_ekf_demo logger --ros-args -p out:=drive.csv
   ros2 run l3_ekf_demo ekf --ros-args --params-file config/ekf.yaml

   # Task 3: record the NIS, then plot it
   ros2 topic echo --csv /l3/ekf/nis > nis.csv
   ros2 run l3_ekf_demo plot_nis --ros-args -p csv:=nis.csv -p out:=nis.png
   # or: ros2 run l3_ekf_demo plot_nis --csv nis.csv --out nis.png
