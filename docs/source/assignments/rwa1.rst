====================================================
RWA 1: Robot Fleet Monitor
====================================================



Overview
========

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Due Date**
     - February 25, 2026, 11:59 PM EST
   * - **Total Points**
     - 30 points
   * - **Submission**
     - Canvas (ZIP file: ``robot_fleet_monitor.zip`` containing the project folder)
   * - **Collaboration**
     - Individual work only. AI tools are NOT permitted.
   * - **Late Policy**
     - 10% deduction per calendar day, up to 3 days. Zero after 3 days.


Description
===========

You are tasked with building a **Robot Fleet Monitor**, a Python program that manages and analyzes a fleet of mobile robots. The program will model robot data using Python's built-in types, process sensor readings, classify robot states, and generate formatted status reports. This assignment tests your understanding of variables, data types, operators, control flow, loops, strings, lists, tuples, and functions (Lectures 1 through 4).


Learning Objectives
===================

By completing this assignment, you will strengthen and demonstrate the following skills:

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: Data Modeling with Built-in Types
        :class-card: sd-border-info

        Practice using dictionaries, lists, tuples, strings, and numeric types to represent structured data for a robotics application.

    .. grid-item-card:: Control Flow and Iteration
        :class-card: sd-border-info

        Apply conditional logic (``if``/``elif``/``else``) and loops (``for``/``while``) to classify data, enforce boundaries, and process collections of robots.

    .. grid-item-card:: Function Design and Decomposition
        :class-card: sd-border-info

        Break a complex problem into well-defined, reusable functions with clear inputs, outputs, type hints, and Google-style docstrings.

    .. grid-item-card:: Pass-by-Assignment and Mutability
        :class-card: sd-border-info

        Understand how mutable objects (dicts, lists) behave when passed to functions and practice both in-place modification and returning new values.

    .. grid-item-card:: String Formatting and Report Generation
        :class-card: sd-border-info

        Use f-strings and string methods to produce clean, aligned, human-readable output from program data.

    .. grid-item-card:: Code Quality and Documentation
        :class-card: sd-border-info

        Develop professional habits including consistent naming conventions, meaningful comments, comprehensive docstrings, and linting compliance.

    .. grid-item-card:: Modular Code Organization
        :class-card: sd-border-info

        Structure a Python project across multiple modules, using imports to connect components, reinforcing separation of concerns.

    .. grid-item-card:: Systems Thinking in Robotics
        :class-card: sd-border-info

        Gain experience modeling a simplified robotics scenario (fleet management, sensor data, battery monitoring) that mirrors patterns found in real-world autonomous systems.


Project Structure
=================

Your submission must follow the modular project structure shown below. Each module groups related functionality, and ``main.py`` imports from the other modules to orchestrate the program.

.. code-block:: text

   robot_fleet_monitor/
   |-- robot.py       # Part 1: Robot data model
   |-- sensors.py     # Part 2 & 3: Sensor simulation and data analysis
   |-- status.py      # Part 4: Battery and status classification
   |-- report.py      # Part 5: Report generation
   |-- main.py        # Part 6: Main program (entry point)


.. list-table::
   :widths: 15 30 55
   :header-rows: 1
   :class: compact-table

   * - Module
     - Functions
     - Description
   * - ``robot.py``
     - ``create_robot()``
     - Part 1: Builds and validates the robot dictionary
   * - ``sensors.py``
     - ``simulate_readings()``, ``compute_statistics()``, ``classify_readings()``
     - Part 2: Generates sensor data and drains battery. Part 3: Computes statistics and classifies readings
   * - ``status.py``
     - ``classify_battery()``, ``update_robot_status()``
     - Part 4: Classifies battery level and updates robot status
   * - ``report.py``
     - ``generate_report()``
     - Part 5: Produces formatted status report string
   * - ``main.py``
     - ``main()``
     - Part 6: Creates fleet, runs pipeline, prints reports and summary


.. note::

   ``report.py`` will need to import ``compute_statistics`` and ``classify_readings`` from ``sensors.py``, and ``classify_battery`` from ``status.py``. Similarly, ``main.py`` will import from all other modules. This gives you practice with cross-module dependencies.


----


Requirements
============


Part 1: Robot Data Model (5 pts)
--------------------------------

**Module:** ``robot.py``

Create a function that builds and returns a robot data structure.

Function: ``create_robot``
^^^^^^^^^^^^^^^^^^^^^^^^^^

Constructs a dictionary representing a single robot in the fleet. This function initializes the robot with its configuration (name, type, speed, sensors) along with default runtime state (full battery, idle status, and an empty readings list).

.. code-block:: python

   def create_robot(name: str, robot_type: str, max_speed: float, sensors: list[str]) -> dict:

- Returns a dictionary with the following keys:

  - ``"name"`` (str): the robot's name
  - ``"type"`` (str): the robot type (e.g., ``"mobile"``, ``"arm"``)
  - ``"max_speed"`` (float): the maximum speed in m/s
  - ``"sensors"`` (list[str]): a list of sensor names
  - ``"battery"`` (float): initialized to ``100.0``
  - ``"status"`` (str): initialized to ``"idle"``
  - ``"readings"`` (list[float]): initialized to an empty list

.. important::

   **Validation:** If ``max_speed`` is negative, set it to ``0.0``. If ``sensors`` is empty, set it to ``["default"]``.


Part 2: Sensor Simulation (5 pts)
----------------------------------

**Module:** ``sensors.py``

Function: ``simulate_readings``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simulates a robot collecting sensor data over time. Each call generates a sequence of readings using a deterministic formula and appends them to the robot's data, while draining its battery to reflect energy consumption during sensing operations.

.. code-block:: python

   def simulate_readings(robot: dict, num_readings: int, base_value: float, variation: float) -> None:

- The ``robot`` parameter is the dictionary created by ``create_robot()`` in Part 1.
- Generates ``num_readings`` sensor readings and appends them to ``robot["readings"]``.
    - Each reading is computed as: ``base_value + (variation * ((i % 5) - 2))`` where ``i`` is the loop index (0-based).
- Each reading should be rounded to 2 decimal places.
- For each reading generated, decrease ``robot["battery"]`` by ``0.5`` (battery cannot go below ``0.0``).
- This function modifies the robot dictionary in place and returns ``None``.


.. dropdown:: Worked Example
    :class-container: sd-border-info
    :open:

    Suppose you create a robot and then call ``simulate_readings``:

    .. code-block:: python

       robot = create_robot("TurtleBot3", "mobile", 0.26, ["lidar", "camera", "imu"])
       simulate_readings(robot, 5, 2.5, 0.5)

    **Before the call**, the dictionary looks like this:

    .. code-block:: python

       {
           "name": "TurtleBot3",
           "type": "mobile",
           "max_speed": 0.26,
           "sensors": ["lidar", "camera", "imu"],
           "battery": 100.0,
           "status": "idle",
           "readings": []
       }

    **During the call**, with ``base_value=2.5``, ``variation=0.5``, and ``num_readings=5``, the formula ``base_value + (variation * ((i % 5) - 2))`` produces:

    .. list-table::
       :widths: 10 25 25 20
       :header-rows: 1
       :class: compact-table

       * - i
         - (i % 5) - 2
         - Calculation
         - Reading
       * - 0
         - -2
         - ``2.5 + (0.5 * -2)``
         - 1.5
       * - 1
         - -1
         - ``2.5 + (0.5 * -1)``
         - 2.0
       * - 2
         - 0
         - ``2.5 + (0.5 * 0)``
         - 2.5
       * - 3
         - 1
         - ``2.5 + (0.5 * 1)``
         - 3.0
       * - 4
         - 2
         - ``2.5 + (0.5 * 2)``
         - 3.5

    Each reading also drains the battery by 0.5, so after 5 readings the battery drops from 100.0 to 97.5.

    **After the call**, the dictionary has been modified in place:

    .. code-block:: python

       {
           "name": "TurtleBot3",
           "type": "mobile",
           "max_speed": 0.26,
           "sensors": ["lidar", "camera", "imu"],
           "battery": 97.5,
           "status": "idle",
           "readings": [1.5, 2.0, 2.5, 3.0, 3.5]
       }

    Notice that ``simulate_readings`` does not return anything. It modifies the original ``robot`` dictionary directly because dictionaries are mutable objects (pass-by-assignment).


Part 3: Data Analysis (6 pts)
------------------------------

**Module:** ``sensors.py``

Function: ``compute_statistics``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Analyzes a list of sensor readings and computes basic descriptive statistics. This function must calculate the average, minimum, and maximum values using manual iteration rather than built-in functions, reinforcing your understanding of loops and accumulators.

.. code-block:: python

   def compute_statistics(readings: list[float]) -> tuple[float, float, float]:

- Takes a list of sensor readings.
- Returns a tuple of ``(average, minimum, maximum)``, each rounded to 2 decimal places.
- If the list is empty, return ``(0.0, 0.0, 0.0)``.

.. warning::

   **Constraint:** Do NOT use the built-in ``min()``, ``max()``, or ``sum()`` functions. Use a loop to compute these values manually.


Function: ``classify_readings``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Categorizes each sensor reading into one of three bins (low, normal, or high) based on user-defined thresholds. This simulates a common pattern in robotics where raw sensor data is converted into meaningful operational categories.

.. code-block:: python

   def classify_readings(readings: list[float], low: float, high: float) -> dict[str, list[float]]:

- Classifies each reading into one of three categories based on thresholds:

  - ``"low"``: reading < ``low``
  - ``"normal"``: ``low`` <= reading <= ``high``
  - ``"high"``: reading > ``high``

- Returns a dictionary with keys ``"low"``, ``"normal"``, ``"high"``, each mapping to a list of readings in that category.


Part 4: Status Classification (4 pts)
--------------------------------------

**Module:** ``status.py``

Function: ``classify_battery``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Maps a numeric battery level to a human-readable status label. This function uses threshold-based classification to determine whether the battery is full, moderate, low, or critical.

.. code-block:: python

   def classify_battery(battery: float) -> str:

- Returns a status string based on the battery level:

  - ``battery >= 80``: return ``"FULL"``
  - ``50 <= battery < 80``: return ``"MODERATE"``
  - ``20 <= battery < 50``: return ``"LOW"``
  - ``battery < 20``: return ``"CRITICAL"``


Function: ``update_robot_status``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Determines the robot's operational state based on its current battery level. The function calls ``classify_battery()`` internally and then updates the robot's status to reflect whether it can continue operating, should remain idle, or needs to return to base for recharging.

.. code-block:: python

   def update_robot_status(robot: dict) -> None:

- The ``robot`` parameter is the dictionary created by ``create_robot()`` in Part 1.
- Calls ``classify_battery()`` to determine the battery classification, then updates ``robot["status"]`` accordingly:

  - ``"FULL"`` or ``"MODERATE"``: set status to ``"active"``
  - ``"LOW"``: set status to ``"idle"``
  - ``"CRITICAL"``: set status to ``"returning to base"``

- This function modifies the robot dictionary in place and returns ``None``.


.. dropdown:: Worked Example
    :class-container: sd-border-info
    :open:

    Suppose a robot has been through several sensor simulations and its battery has dropped to 35.0:

    .. code-block:: python

       robot = {
           "name": "TurtleBot3",
           "type": "mobile",
           "max_speed": 0.26,
           "sensors": ["lidar", "camera", "imu"],
           "battery": 35.0,
           "status": "idle",
           "readings": [1.5, 2.0, 2.5, 3.0, 3.5]
       }

       update_robot_status(robot)

    Inside the function, ``classify_battery(35.0)`` returns ``"LOW"`` (since ``20 <= 35.0 < 50``), so the function sets ``robot["status"]`` to ``"idle"``.

    **After the call:**

    .. code-block:: python

       robot["status"]   # "idle"

    If the battery were ``85.0`` instead, ``classify_battery(85.0)`` would return ``"FULL"``, and the status would be set to ``"active"``. If the battery were ``10.0``, the classification would be ``"CRITICAL"`` and the status would become ``"returning to base"``.


Part 5: Report Generation (5 pts)
----------------------------------

**Module:** ``report.py``

Function: ``generate_report``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Builds a complete, formatted status report for a single robot by combining its configuration, battery status, sensor statistics, and reading classifications into a multi-line string. This function integrates the outputs of ``compute_statistics``, ``classify_readings``, and ``classify_battery`` to produce a human-readable summary.

.. code-block:: python

   def generate_report(robot: dict) -> str:

Returns a formatted multi-line string report. Use f-strings for formatting. The report must follow the format shown below. The values shown are illustrative; your output will differ based on the robots you create and the simulation parameters you use.

.. code-block:: text

   ========================================
   ROBOT STATUS REPORT
   ========================================
   Name       : TurtleBot3
   Type       : mobile
   Status     : active
   Battery    : 85.00% [FULL]
   Max Speed  : 0.26 m/s
   Sensors    : lidar, camera, imu
   ----------------------------------------
   SENSOR READINGS SUMMARY
   ----------------------------------------
   Total Readings : 10
   Average        : 2.50
   Minimum        : 1.50
   Maximum        : 3.50
   ----------------------------------------
   READING CLASSIFICATION (low=1.5, high=3.0)
   ----------------------------------------
   Low     : 2 readings
   Normal  : 5 readings
   High    : 3 readings
   ========================================


- Use thresholds ``low=1.5`` and ``high=3.0`` for reading classification inside the report. These thresholds represent boundaries for expected sensor behavior:

  - Readings below ``1.5`` suggest a weak signal or sensor underperformance.
  - Readings between ``1.5`` and ``3.0`` (inclusive) fall within the normal operating range.
  - Readings above ``3.0`` may indicate an anomaly such as obstacle proximity or sensor saturation.

- The sensors list should be displayed as a comma-separated string.
- Battery should display with 2 decimal places followed by the classification in brackets.
- If the robot has no readings, the summary section should display ``0`` for all values.


Part 6: Main Program (5 pts)
-----------------------------

**Module:** ``main.py``

Create a ``main()`` function that orchestrates the entire program. Call it from an ``if __name__ == "__main__"`` guard. All program logic must live inside ``main()``, not at the module level. Import the necessary functions from ``robot``, ``sensors``, ``status``, and ``report`` modules.

The ``main()`` function must:

1. Create at least 3 robots with different configurations using ``create_robot()``.
2. Store the robots in a list.
3. Simulate readings for each robot using a ``for`` loop with different ``base_value`` and ``variation`` parameters.
4. Update each robot's status using ``update_robot_status()``.
5. Print the report for each robot using ``generate_report()``.
6. After all reports, print a fleet summary showing:

   - Total number of robots
   - Number of robots in each status category (active, idle, returning to base)
   - The robot with the lowest battery level (print its name and battery percentage)


.. dropdown:: Example Output
    :class-container: sd-border-info
    :open:

    The following is an example of what the full program output might look like when run with 3 robots. Your exact values will differ based on the robots you create and the simulation parameters you choose.

    .. code-block:: text

       ========================================
       ROBOT STATUS REPORT
       ========================================
       Name       : TurtleBot3
       Type       : mobile
       Status     : active
       Battery    : 95.00% [FULL]
       Max Speed  : 0.26 m/s
       Sensors    : lidar, camera, imu
       ----------------------------------------
       SENSOR READINGS SUMMARY
       ----------------------------------------
       Total Readings : 10
       Average        : 2.50
       Minimum        : 1.50
       Maximum        : 3.50
       ----------------------------------------
       READING CLASSIFICATION (low=1.5, high=3.0)
       ----------------------------------------
       Low     : 2 readings
       Normal  : 5 readings
       High    : 3 readings
       ========================================

       ========================================
       ROBOT STATUS REPORT
       ========================================
       Name       : Jackal
       Type       : mobile
       Status     : active
       Battery    : 85.00% [FULL]
       Max Speed  : 2.00 m/s
       Sensors    : lidar, gps
       ----------------------------------------
       SENSOR READINGS SUMMARY
       ----------------------------------------
       Total Readings : 30
       Average        : 5.00
       Minimum        : 3.00
       Maximum        : 7.00
       ----------------------------------------
       READING CLASSIFICATION (low=1.5, high=3.0)
       ----------------------------------------
       Low     : 0 readings
       Normal  : 6 readings
       High    : 24 readings
       ========================================

       ========================================
       ROBOT STATUS REPORT
       ========================================
       Name       : UR5
       Type       : arm
       Status     : returning to base
       Battery    : 10.00% [CRITICAL]
       Max Speed  : 1.00 m/s
       Sensors    : force_torque, camera
       ----------------------------------------
       SENSOR READINGS SUMMARY
       ----------------------------------------
       Total Readings : 180
       Average        : 1.00
       Minimum        : 0.00
       Maximum        : 2.00
       ----------------------------------------
       READING CLASSIFICATION (low=1.5, high=3.0)
       ----------------------------------------
       Low     : 72 readings
       Normal  : 108 readings
       High    : 0 readings
       ========================================

       ========================================
       FLEET SUMMARY
       ========================================
       Total Robots   : 3
       Active         : 2
       Idle           : 0
       Returning      : 1
       ----------------------------------------
       Lowest Battery : UR5 (10.00%)
       ========================================


----


Grading Rubric
==============

.. list-table::
   :widths: 35 8 57
   :header-rows: 1
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - Part 1: Robot Data Model
     - 5
     - Correct dictionary structure with all keys (2 pts). Input validation for max_speed and sensors (2 pts). Proper type hints in function signature (1 pt).
   * - Part 2: Sensor Simulation
     - 5
     - Correct reading formula and rounding (2 pts). Battery drain logic with floor at 0.0 (2 pts). In-place modification of robot dictionary (1 pt).
   * - Part 3: Data Analysis
     - 6
     - ``compute_statistics``: correct manual loop for avg/min/max without built-in functions (3 pts). ``classify_readings``: correct threshold logic and dictionary output (3 pts).
   * - Part 4: Status Classification
     - 4
     - ``classify_battery``: correct threshold boundaries (2 pts). ``update_robot_status``: correct mapping from battery status to robot status (2 pts).
   * - Part 5: Report Generation
     - 5
     - Exact format match with proper alignment (2 pts). Correct use of f-strings with formatting specifiers (1 pt). Integration of ``compute_statistics`` and ``classify_readings`` (2 pts).
   * - Part 6: Main Program
     - 5
     - Creates 3+ robots and stores in a list (1 pt). Correct loop to simulate, update, and report (2 pts). Fleet summary with status counts and lowest battery (2 pts).
   * - **TOTAL**
     - **30**
     -


Code Quality Requirements
=========================

.. warning::

   The following are mandatory and will result in point deductions if missing.

- **Docstrings:** Every function must have a Google-style docstring with a description, ``Args`` section, and ``Returns`` section.
- **Type hints:** All function parameters and return types must have type annotations.
- **Inline comments:** Include comments that explain non-obvious logic (e.g., the reading formula, battery drain, threshold classification).
- **Naming conventions:** Use ``snake_case`` for all function and variable names. Function names must start with a verb.
- **No global variables:** All data should be passed through function parameters and return values.
- **Linting:** Ensure Ruff is enabled in VS Code and that no linting errors or warnings appear. You can also run ``ruff check`` from the terminal as a final check.

.. admonition:: Deductions
   :class: caution

   Missing docstrings (-1 pt per function, up to -5 pts). Missing type hints (-0.5 pt per function, up to -3 pts). Poor or missing comments (-1 pt). Naming violations (-1 pt). Linting errors (-1 pt).


----


Pre-Submission Checklist
========================

Before submitting, verify that your project meets all of the following requirements. Each item is graded and missing items will result in point deductions.


Functionality
-------------

- ☐ The program runs without errors: ``python3 main.py``
- ☐ All 8 functions produce correct output for the given specifications.
- ☐ The report format matches the expected output (alignment, spacing, delimiters).
- ☐ The fleet summary displays status counts and the robot with the lowest battery.


Code Quality
------------

- ☐ **Type hints:** Every function parameter and return type has a type annotation (e.g., ``def create_robot(name: str, ...) -> dict:``).
- ☐ **Docstrings:** Every function has a Google-style docstring with a one-line description, ``Args`` section, and ``Returns`` section.
- ☐ **Inline comments:** Non-obvious logic is explained with comments (e.g., the reading formula, battery floor, threshold meaning).
- ☐ **Naming:** All functions and variables use ``snake_case``. Function names start with a verb (e.g., ``create_``, ``compute_``, ``classify_``).
- ☐ **No global variables:** All data is passed through function parameters and return values. No mutable state at module level.
- ☐ **Imports:** Each module uses explicit named imports (e.g., ``from sensors import compute_statistics``). No wildcard imports.


Linting
-------

- ☐ Ruff is enabled in VS Code and no linting errors or warnings appear in any Python file.

You can also run Ruff from the terminal as a final check:

.. code-block:: bash

   cd robot_fleet_monitor/
   ruff check robot.py sensors.py status.py report.py main.py


File Headers
------------

- ☐ Every Python file includes a comment block at the top with your name, UID, and module description.

.. code-block:: python

   # Name: <Your Name>
   # UID: <Your UID>
   # Module: robot.py - Robot data model creation and validation


Packaging
---------

- ☐ Removed ``__pycache__/``, ``.pyc``, and ``.ruff_cache/`` before zipping.
- ☐ ZIP file contains only the ``robot_fleet_monitor/`` folder with the five ``.py`` files.
- ☐ Verified ZIP contents with ``unzip -l``.

Before zipping, remove any build artifacts or temporary files that may have been generated:

.. code-block:: bash

   cd robot_fleet_monitor/
   rm -rf __pycache__/ *.pyc .ruff_cache/
   cd ..
   zip -r robot_fleet_monitor.zip robot_fleet_monitor/

Verify your ZIP has the correct structure by inspecting its contents:

.. code-block:: bash

   unzip -l robot_fleet_monitor.zip

You should see only the five ``.py`` files inside the ``robot_fleet_monitor/`` folder. No ``__pycache__/``, ``.pyc``, or ``.ruff_cache/`` files should be present.


----


Hints
=====

.. tip::

   - Use ``\n`` (newline) and string concatenation or multi-line f-strings to build the report in ``generate_report()``.
   - To join a list into a comma-separated string: ``", ".join(sensors)``
   - Remember that modifying a mutable object (like a dict or list) inside a function affects the original (pass-by-assignment).
   - Test each function independently before integrating into the main program.
   - The formula ``(i % 5) - 2`` produces the pattern: -2, -1, 0, 1, 2, -2, -1, 0, 1, 2, ...


----


Submission
==========

- Submit a ZIP file named ``robot_fleet_monitor.zip`` on Canvas.
- The ZIP must contain a single folder named ``robot_fleet_monitor/`` with exactly five Python files: ``robot.py``, ``sensors.py``, ``status.py``, ``report.py``, and ``main.py``.
- The ZIP must not contain ``__pycache__/``, ``.pyc`` files, ``.ruff_cache/``, or any other build artifacts.
- The program should run without errors when executed with ``python3 main.py`` from inside the ``robot_fleet_monitor/`` directory.
- Do not submit Jupyter notebooks, extra files, or nested ZIP archives.
- Ensure your name and UID are in a comment at the top of every Python file.


----


Academic Integrity
==================

.. danger::

   This is an individual assignment. You may not collaborate with other students, share code, or use AI tools (ChatGPT, Copilot, Claude, etc.). You may reference the lecture slides, official Python documentation, and your own class notes. Violations will result in a zero on the assignment and will be reported to the Office of Student Conduct.