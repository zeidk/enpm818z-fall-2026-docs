====================================================
Exercises
====================================================

This page contains three take-home exercises that reinforce the concepts
from Lecture 3. Each exercise asks you to **write code from scratch**
based on a specification — no starter code is provided.

All files should be created inside your ``lecture3/`` workspace folder.


.. dropdown:: Exercise 1 – Loop Challenges
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate your mastery of ``for`` loops, ``while`` loops, ``range()``,
    and loop control statements (``break``, ``continue``, ``else``) by
    implementing several algorithmic patterns.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture3/loop_challenges.py`` that implements the following
    tasks. Each task must print its result with a clear label.

    1. **FizzBuzz** — Using a ``for`` loop and ``range()``, print numbers from
       1 to 30. However:

       - If the number is divisible by 3, print ``"Fizz"`` instead.
       - If the number is divisible by 5, print ``"Buzz"`` instead.
       - If divisible by both 3 and 5, print ``"FizzBuzz"`` instead.

       Print all values on a single line separated by spaces.

    2. **Prime Checker** — Write a ``while`` loop that finds all prime numbers
       between 2 and 50. A prime number is only divisible by 1 and itself.

       Use a nested ``for`` loop with ``break`` and ``else`` to check primality.
       Print the primes as a comma-separated list.

    3. **Digit Sum** — Given ``number = 987654321``, use a ``while`` loop to
       compute the sum of all digits. You must extract digits using modulus
       (``% 10``) and integer division (``// 10``). Do NOT convert to a string.

    4. **Pattern Printing** — Using nested ``for`` loops and ``range()``, print
       the following right-aligned triangle pattern (5 rows):

       .. code-block:: text

              *
             **
            ***
           ****
          *****

       Hint: Use string multiplication and right-align formatting.

    5. **Countdown with Skip** — Using a ``for`` loop with ``range()`` and
       ``continue``, print a countdown from 20 to 1, but skip all numbers
       divisible by 3. Print on a single line.

    **Expected output:**

    .. code-block:: text

       Task 1 - FizzBuzz:
       1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz Fizz 22 23 Fizz Buzz 26 Fizz 28 29 FizzBuzz

       Task 2 - Primes (2-50):
       2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47

       Task 3 - Digit Sum of 987654321:
       45

       Task 4 - Triangle Pattern:
           *
          **
         ***
        ****
       *****

       Task 5 - Countdown (skip multiples of 3):
       20 19 17 16 14 13 11 10 8 7 5 4 2 1


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture3/loop_challenges.py``
    - The program must run without errors and produce output matching the
      expected format above.


.. dropdown:: Exercise 2 – Collection Manipulations
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice creating, modifying, and querying lists, tuples, dictionaries,
    and sets by implementing a simple inventory management system for a
    robot parts warehouse.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture3/inventory_manager.py`` that does the following:

    1. **Initialize inventory** — Create a dictionary ``inventory`` where:

       - Keys are part names (strings): ``"servo_motor"``, ``"lidar_sensor"``,
         ``"camera_module"``, ``"battery_pack"``, ``"wheel_assembly"``
       - Values are tuples of ``(quantity, unit_price)``:
         ``(25, 45.99)``, ``(10, 299.50)``, ``(15, 89.00)``, ``(30, 125.00)``,
         ``(20, 55.50)``

    2. **List all parts** — Using a ``for`` loop and ``.items()``, print each
       part with its quantity and total value (quantity × unit_price).
       Format prices to 2 decimal places.

    3. **Low stock alert** — Using a list comprehension, create a list
       ``low_stock`` containing part names where quantity is below 20.
       Print the list.

    4. **Total inventory value** — Calculate and print the total value of
       all inventory (sum of quantity × unit_price for all parts).

    5. **Part categories** — Create two sets:

       - ``sensors``: ``{"lidar_sensor", "camera_module", "ultrasonic_sensor"}``
       - ``actuators``: ``{"servo_motor", "stepper_motor", "wheel_assembly"}``

       Using set operations, find and print:

       a. Parts that are sensors AND in inventory (intersection)
       b. Parts that are actuators OR sensors (union)
       c. Actuators NOT in inventory (difference)

    6. **Restock operation** — Using tuple unpacking, iterate through the
       inventory and create a new dictionary ``restocked`` where each part
       with quantity < 20 has its quantity increased by 15. Print the
       restocked inventory.

    7. **Part lookup** — Implement a lookup that checks if ``"gps_module"``
       exists in inventory. Use the ``.get()`` method with a default value
       of ``(0, 0.00)`` and print an appropriate message.

    **Expected output:**

    .. code-block:: text

       === Inventory List ===
       servo_motor: 25 units @ $45.99 each = $1149.75
       lidar_sensor: 10 units @ $299.50 each = $2995.00
       camera_module: 15 units @ $89.00 each = $1335.00
       battery_pack: 30 units @ $125.00 each = $3750.00
       wheel_assembly: 20 units @ $55.50 each = $1110.00

       === Low Stock Alert ===
       Parts below 20 units: ['lidar_sensor', 'camera_module']

       === Total Inventory Value ===
       $10339.75

       === Category Analysis ===
       Sensors in inventory: {'lidar_sensor', 'camera_module'}
       All sensors or actuators: {'lidar_sensor', 'camera_module', 'ultrasonic_sensor', 'servo_motor', 'stepper_motor', 'wheel_assembly'}
       Actuators not in inventory: {'stepper_motor'}

       === Restocked Inventory ===
       servo_motor: 25 units
       lidar_sensor: 25 units
       camera_module: 30 units
       battery_pack: 30 units
       wheel_assembly: 20 units

       === Part Lookup ===
       gps_module not found in inventory (default: 0 units @ $0.00)


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture3/inventory_manager.py``
    - The program must run without errors and produce output matching the
      expected format above.
    - Use appropriate data structures for each task (no hard-coding results).


.. dropdown:: Exercise 3 – Robot Fleet Analyzer
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Combine all concepts from Lecture 3 — loops, lists, tuples, dictionaries,
    sets, and comprehensions — to build a data analysis tool for a fleet of
    autonomous delivery robots.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture3/fleet_analyzer.py`` that does the following:

    1. **Define fleet data** — Create a list ``fleet`` containing dictionaries
       for 5 robots. Each robot dictionary has:

       - ``"id"``: ``"R001"`` through ``"R005"``
       - ``"model"``: Use models ``"Scout"``, ``"Hauler"``, ``"Scout"``,
         ``"Sprinter"``, ``"Hauler"`` (in order)
       - ``"battery_pct"``: ``78``, ``23``, ``91``, ``45``, ``67`` (in order)
       - ``"deliveries_today"``: ``12``, ``5``, ``18``, ``9``, ``14`` (in order)
       - ``"status"``: ``"active"``, ``"charging"``, ``"active"``, ``"active"``,
         ``"maintenance"`` (in order)

    2. **Fleet summary** — Using a ``for`` loop, print a formatted table of
       all robots showing ID, model, battery %, and status. Use string
       formatting to align columns.

    3. **Active robots** — Using a list comprehension with a condition,
       create a list ``active_ids`` containing only the IDs of robots with
       ``status == "active"``. Print the list.

    4. **Battery analysis** — Using loops and conditionals:

       a. Find the robot with the lowest battery (print its ID and battery %)
       b. Calculate the average battery percentage across all robots
       c. Count how many robots have battery below 50%

    5. **Delivery statistics** — Using list comprehension and built-in
       functions:

       a. Create a list of all delivery counts
       b. Print the total deliveries, maximum, minimum, and average

    6. **Model inventory** — Using a dictionary and a loop, count how many
       robots of each model are in the fleet. Print as ``"Model: count"``.

    7. **Status sets** — Create a set ``all_statuses`` containing all unique
       status values in the fleet. Also create a set ``ideal_statuses``
       containing ``{"active", "standby"}``. Using set operations, find:

       a. Statuses that are NOT ideal (difference)
       b. Whether all fleet statuses are ideal (subset check)

    8. **Tuple unpacking report** — Create a list of tuples where each tuple
       is ``(id, battery_pct, deliveries_today)``. Using a ``for`` loop with
       tuple unpacking, print robots that have made more than 10 deliveries
       AND have battery above 50%.

    **Expected output:**

    .. code-block:: text

       === Fleet Summary ===
       ID      Model      Battery   Status
       ----------------------------------------
       R001    Scout      78%       active
       R002    Hauler     23%       charging
       R003    Scout      91%       active
       R004    Sprinter   45%       active
       R005    Hauler     67%       maintenance

       === Active Robots ===
       ['R001', 'R003', 'R004']

       === Battery Analysis ===
       Lowest battery: R002 at 23%
       Average battery: 60.80%
       Robots below 50%: 2

       === Delivery Statistics ===
       Total deliveries: 58
       Maximum: 18
       Minimum: 5
       Average: 11.60

       === Model Inventory ===
       Scout: 2
       Hauler: 2
       Sprinter: 1

       === Status Analysis ===
       All statuses: {'active', 'charging', 'maintenance'}
       Non-ideal statuses: {'charging', 'maintenance'}
       All statuses ideal: False

       === High Performers (>10 deliveries AND >50% battery) ===
       R001: 12 deliveries, 78% battery
       R003: 18 deliveries, 91% battery
       R005: 14 deliveries, 67% battery


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture3/fleet_analyzer.py``
    - The program must run without errors and produce output matching the
      expected format above.
    - All calculations must be computed dynamically (no hard-coded results).
    - Use appropriate data structures and Pythonic patterns (comprehensions
      where suitable).