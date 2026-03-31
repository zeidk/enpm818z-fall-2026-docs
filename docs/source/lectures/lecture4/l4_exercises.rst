====================================================
Exercises
====================================================

This page contains three take-home exercises that reinforce the concepts
from Lecture 4. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``lecture4/`` workspace folder.


.. dropdown:: Exercise 1 -- Function Basics and Arguments
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate your understanding of function definitions, multiple return
    values, default arguments, keyword arguments, ``*args``, and ``**kwargs``
    by implementing a set of utility functions for robot configuration.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture4/robot_config.py`` that implements the following
    functions. Each function must include type hints and a Google-style
    docstring.

    1. **``compute_distance``** -- Takes two tuples representing 2D
       coordinates ``(x1, y1)`` and ``(x2, y2)``. Returns the Euclidean
       distance rounded to 2 decimal places. Use the formula:
       ``sqrt((x2 - x1)**2 + (y2 - y1)**2)``. Import ``sqrt`` from the
       ``math`` module.

    2. **``configure_motor``** -- Takes a required ``name`` (str) and optional
       keyword arguments: ``speed`` (float, default ``1.0``), ``direction``
       (str, default ``"forward"``), and ``enabled`` (bool, default ``True``).
       Returns a dictionary with keys ``"name"``, ``"speed"``, ``"direction"``,
       and ``"enabled"``.

    3. **``compute_statistics``** -- Takes ``*args`` (any number of floats).
       Returns a tuple of ``(count, total, average)`` rounded to 2 decimal
       places. If no arguments are given, return ``(0, 0.0, 0.0)``.

    4. **``build_command``** -- Takes a required ``action`` (str) and
       ``**kwargs`` for additional parameters. Returns a formatted string:
       ``"ACTION: <action> | PARAMS: key1=val1, key2=val2, ..."``. If no
       kwargs are given, the params section should say ``"none"``.

    5. **``swap_coordinates``** -- Takes two tuples ``(x1, y1)`` and
       ``(x2, y2)`` and returns them swapped as a tuple of tuples:
       ``((x2, y2), (x1, y1))``. Demonstrate tuple unpacking when calling.

    In the ``if __name__ == "__main__"`` block, call each function with
    example arguments and print the results with labels.

    **Expected output:**

    .. code-block:: text

       === Distance ===
       Distance from (0, 0) to (3, 4): 5.0

       === Motor Configuration ===
       Default: {'name': 'left_wheel', 'speed': 1.0, 'direction': 'forward', 'enabled': True}
       Custom: {'name': 'right_wheel', 'speed': 2.5, 'direction': 'reverse', 'enabled': False}

       === Statistics ===
       Stats for (10.5, 20.3, 30.7, 40.1): (4, 101.6, 25.4)
       Stats for (): (0, 0.0, 0.0)

       === Command Builder ===
       build_command('move', x=10, y=20): ACTION: move | PARAMS: x=10, y=20
       build_command('stop'): ACTION: stop | PARAMS: none

       === Swap ===
       Before: a=(1, 2), b=(3, 4)
       After:  a=(3, 4), b=(1, 2)


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture4/robot_config.py``
    - The program must run without errors and produce output matching the
      expected format above.


.. dropdown:: Exercise 2 -- Scope and Pass-by-Assignment
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Explore variable scoping (LEGB rule), the ``global`` and ``nonlocal``
    keywords, and pass-by-assignment behavior with mutable and immutable
    objects.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture4/scope_explorer.py`` that demonstrates each
    concept below. Each task must print clearly labeled output showing
    variable values before and after function calls.

    1. **Local vs. Global** -- Define a global variable ``mode = "manual"``.
       Write a function ``set_mode_local()`` that creates a local variable
       ``mode = "auto"`` and prints it. After calling the function, print the
       global ``mode`` to show it is unchanged.

    2. **The ``global`` keyword** -- Write a function ``set_mode_global()``
       that uses the ``global`` keyword to modify the module-level ``mode``
       variable to ``"autonomous"``. Print ``mode`` before and after the call.

    3. **Enclosing scope with ``nonlocal``** -- Write a function
       ``make_counter()`` that defines a local variable ``count = 0`` and a
       nested function ``increment()`` that uses ``nonlocal`` to increase
       ``count`` by 1 and returns it. Call ``increment()`` three times from
       inside ``make_counter()`` and print the result each time.

    4. **Pass-by-assignment with immutable** -- Write a function
       ``try_modify_int(x: int) -> None`` that adds 10 to ``x`` and prints
       the result inside the function. Call it with ``value = 5`` and print
       ``value`` after the call to show it is unchanged.

    5. **Pass-by-assignment with mutable** -- Write a function
       ``add_sensor(robot: dict, sensor: str) -> None`` that appends
       ``sensor`` to ``robot["sensors"]``. Call it and print the robot
       dictionary before and after to show the in-place modification.

    6. **Reassignment vs. mutation** -- Write a function
       ``reassign_list(data: list) -> None`` that reassigns ``data`` to a
       new list ``[99, 99, 99]`` and prints it inside the function. Call it
       with ``original = [1, 2, 3]`` and print ``original`` after the call
       to show the original is unchanged.

    **Expected output:**

    .. code-block:: text

       === Task 1: Local vs Global ===
       Inside set_mode_local(): auto
       Global mode after call: manual

       === Task 2: global keyword ===
       Before: manual
       After set_mode_global(): autonomous

       === Task 3: nonlocal with make_counter ===
       Increment 1: 1
       Increment 2: 2
       Increment 3: 3

       === Task 4: Immutable (int) ===
       Inside function: 15
       Outside after call: 5

       === Task 5: Mutable (dict) ===
       Before: {'name': 'TurtleBot', 'sensors': ['lidar']}
       After add_sensor: {'name': 'TurtleBot', 'sensors': ['lidar', 'camera']}

       === Task 6: Reassignment vs Mutation ===
       Inside function: [99, 99, 99]
       Outside after call: [1, 2, 3]


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture4/scope_explorer.py``
    - The program must run without errors and produce output matching the
      expected format above.


.. dropdown:: Exercise 3 -- Robot Toolkit
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Combine all concepts from Lecture 4 -- function definition, arguments,
    scope, pass-by-assignment, type hints, docstrings, and recursion -- to
    build a toolkit of reusable functions for a robot navigation system.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture4/robot_toolkit.py`` that implements the following
    functions. Every function must have type hints and a Google-style
    docstring.

    1. **``create_waypoint``** -- Takes ``name`` (str), ``x`` (float),
       ``y`` (float), and an optional ``priority`` (int, default ``0``).
       Returns a dictionary with keys ``"name"``, ``"x"``, ``"y"``, and
       ``"priority"``.

    2. **``compute_path_length``** -- Takes a list of waypoints (dicts from
       ``create_waypoint``). Computes the total Euclidean distance along the
       path (from waypoint 0 to 1, 1 to 2, etc.). Returns the total
       distance rounded to 2 decimal places. If the list has fewer than 2
       waypoints, return ``0.0``.

    3. **``sort_by_priority``** -- Takes a list of waypoints and returns a
       **new** list sorted by priority in descending order (highest first).
       The original list must not be modified. Use a loop (do NOT use the
       built-in ``sorted()`` or ``list.sort()``). Implement a simple
       selection sort.

    4. **``format_waypoint``** -- Takes a waypoint dictionary and returns a
       formatted string: ``"[P<priority>] <name> @ (<x>, <y>)"``.
       Example: ``"[P2] charger @ (5.0, 3.0)"``.

    5. **``print_path``** -- Takes a list of waypoints and an optional
       ``label`` (str, default ``"Path"``). Prints the label, then each
       waypoint using ``format_waypoint()``, then the total path length
       using ``compute_path_length()``.

    6. **``recursive_distance_sum``** -- Takes a list of float distances and
       returns their sum using recursion (no loops, no ``sum()``). Base case:
       empty list returns ``0.0``.

    In the ``if __name__ == "__main__"`` block:

    - Create at least 4 waypoints with different priorities.
    - Store them in a list and print the path using ``print_path()``.
    - Sort by priority and print the sorted path.
    - Demonstrate ``recursive_distance_sum()`` with a list of segment
      distances.

    **Expected output:**

    .. code-block:: text

       === Original Path ===
       Path:
         1. [P1] start @ (0.0, 0.0)
         2. [P3] obstacle @ (3.0, 4.0)
         3. [P0] waypoint_A @ (6.0, 4.0)
         4. [P2] charger @ (6.0, 8.0)
       Total distance: 12.0

       === Sorted by Priority ===
       Priority Path:
         1. [P3] obstacle @ (3.0, 4.0)
         2. [P2] charger @ (6.0, 8.0)
         3. [P1] start @ (0.0, 0.0)
         4. [P0] waypoint_A @ (6.0, 4.0)
       Total distance: 18.63

       === Recursive Distance Sum ===
       Distances: [5.0, 3.0, 4.0]
       Recursive sum: 12.0


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture4/robot_toolkit.py``
    - The program must run without errors and produce output matching the
      expected format above.
    - All calculations must be computed dynamically (no hard-coded results).
    - Every function must include type hints and a Google-style docstring.