====================================================
Exercises
====================================================

This page contains three take-home exercises that reinforce the concepts
from Lecture 2.  Each exercise asks you to **write code from scratch**
based on a specification — no starter code is provided.

All files should be created inside your ``lecture2/`` workspace folder.


.. dropdown:: Exercise 1 – Operator Expressions
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate your understanding of arithmetic, relational, logical, and
    membership operators by writing a program that computes and reports
    mission statistics for an autonomous drone.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture2/mission_stats.py`` that does the following:

    1. Define the following variables (use the exact names shown):

       - ``total_distance``: ``134.7`` (km)
       - ``flight_time``: ``2.75`` (hours)
       - ``num_waypoints``: ``8``
       - ``battery_capacity``: ``5000`` (mAh)
       - ``battery_remaining``: ``1820`` (mAh)
       - ``approved_altitudes``: a list containing ``30``, ``60``, ``90``, and ``120``
       - ``requested_altitude``: ``75``

    2. Using **only** the variables above and Python operators, compute and
       print each of the following on its own line.  Format every
       floating-point result to **two decimal places** using an f-string.

       a. Average speed (``total_distance / flight_time``).
       b. Distance per waypoint segment — there are ``num_waypoints - 1``
          segments between waypoints.
       c. The number of **complete** 30 km legs that fit into
          ``total_distance`` (use floor division).
       d. The leftover distance after those complete legs (use modulus).
       e. Battery percentage remaining (as a float, not an integer).
       f. Whether ``requested_altitude`` is in ``approved_altitudes``
          (print the Boolean directly).
       g. A single Boolean expression that is ``True`` when **all three**
          of the following conditions hold:

          - Battery percentage is above 25%.
          - Average speed is less than 60 km/h.
          - ``requested_altitude`` is **not** in ``approved_altitudes``.

    **Expected output** (your exact numbers should match):

    .. code-block:: text

       Average speed:          48.98 km/h
       Distance per segment:   19.24 km
       Complete 30 km legs:    4
       Leftover distance:      14.70 km
       Battery remaining:      36.40%
       Altitude approved:      False
       All conditions met:     True


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture2/mission_stats.py``
    - The program must run without errors and produce output that matches
      the expected values above.


.. dropdown:: Exercise 2 – String Processing
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice string indexing, slicing, methods, and f-string formatting by
    writing a program that parses and reformats raw sensor log messages.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture2/log_parser.py`` that does the following:

    1. Define a variable ``raw_log`` with this exact value:

       .. code-block:: python

          raw_log = "ts=1706817600;level=WARNING;src=IMU_03;msg=Gyro drift exceeded 0.05 rad/s"

    2. **Without hard-coding any index numbers**, write code that extracts
       each field from the raw log.  You must use string methods such as
       ``.split()``, ``.find()``, ``.index()``, or slicing relative to
       delimiters — not fixed numeric positions.  Store the results in four
       variables:

       - ``timestamp`` — the value after ``ts=`` (as a string)
       - ``level`` — the value after ``level=``
       - ``source`` — the value after ``src=``
       - ``message`` — the value after ``msg=``

    3. Using the extracted variables, print the following reformatted
       output.  All formatting must be done with f-strings.

       a. A header line: ``===== LOG ENTRY =====``
       b. The timestamp right-aligned in a 20-character field.
       c. The level converted to lowercase.
       d. The source with the first ``"_"`` replaced by ``" #"``
          (e.g., ``"IMU_03"`` becomes ``"IMU #03"``).
       e. The message in title case.
       f. The total character count of the original ``raw_log``.
       g. A reversed copy of the ``level`` string.
       h. A footer line: ``=`` repeated to match the length of the header.

    **Expected output:**

    .. code-block:: text

       ===== LOG ENTRY =====
       Timestamp:          1706817600
       Level:     warning
       Source:    IMU #03
       Message:   Gyro Drift Exceeded 0.05 Rad/S
       Log length: 76
       Reversed level: GNINRAW
       =====================


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture2/log_parser.py``
    - The program must run without errors and produce output that matches
      the expected values above.
    - No index numbers may be hard-coded (e.g., ``raw_log[3:13]`` is not
      acceptable).


.. dropdown:: Exercise 3 – Control Flow
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write conditional logic from scratch to implement a multi-factor
    decision system for an autonomous forklift operating in a warehouse.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture2/forklift_decision.py`` that does the following:

    1. Define the following variables at the top of your file:

       - ``payload_kg``: ``320.0``
       - ``max_capacity_kg``: ``500.0``
       - ``aisle_width``: ``2.8`` (meters)
       - ``fork_width``: ``1.2`` (meters)
       - ``battery_pct``: ``42.0``
       - ``obstacle_ahead``: ``False``
       - ``operator_override``: ``False``

    2. **Task A — Load classification**: Using ``if``/``elif``/``else``,
       classify the load and print the result:

       - If ``payload_kg`` is ``0``: print ``"Load status: EMPTY"``
       - If ``payload_kg`` is up to 50% of ``max_capacity_kg``: print
         ``"Load status: LIGHT"``
       - If ``payload_kg`` is between 50% and 85% (inclusive) of
         ``max_capacity_kg``: print ``"Load status: MODERATE"``
       - If ``payload_kg`` is above 85% but at or below 100% of
         ``max_capacity_kg``: print ``"Load status: HEAVY — reduce speed"``
       - If ``payload_kg`` exceeds ``max_capacity_kg``: print
         ``"Load status: OVERLOADED — cannot proceed"``

       You must compute the thresholds from the variables (do **not**
       hard-code ``250``, ``425``, etc.).

    3. **Task B — Clearance check**: Compute the clearance on each side
       as ``(aisle_width - fork_width) / 2``.  Using a **ternary
       expression**, set a variable ``clearance_ok`` to ``True`` if the
       per-side clearance is at least ``0.5`` meters, otherwise ``False``.
       Print the per-side clearance (two decimal places) and whether it is
       acceptable.

    4. **Task C — Go / No-Go decision**: Write a single compound
       ``if``/``elif``/``else`` block that prints **exactly one** of the
       following outcomes:

       - ``"DECISION: HALTED — obstacle detected"`` — if
         ``obstacle_ahead`` is ``True`` and ``operator_override`` is
         ``False``.
       - ``"DECISION: OVERRIDE — proceeding with caution"`` — if
         ``obstacle_ahead`` is ``True`` but ``operator_override`` is also
         ``True``.
       - ``"DECISION: RETURN TO CHARGE"`` — if ``battery_pct`` is below
         ``20`` and there is no obstacle.
       - ``"DECISION: PROCEED"`` — if none of the above apply.

    5. **Task D — Test your logic**: Change the input variables to produce
       each of the following scenarios and verify your output is correct:

       - An overloaded forklift with an obstacle ahead.
       - An empty forklift with low battery and no obstacle.
       - A heavy forklift with operator override active and tight
         clearance.

       Add a comment block at the bottom of your file showing the variable
       values you used for each test and the corresponding output.

    **Expected output for the default values:**

    .. code-block:: text

       Load status: MODERATE
       Per-side clearance: 0.80 m — Acceptable: True
       DECISION: PROCEED


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture2/forklift_decision.py``
    - The program must run without errors and produce the expected output
      for the default variable values.
    - The comment block at the bottom must include at least three
      additional test scenarios with their outputs.