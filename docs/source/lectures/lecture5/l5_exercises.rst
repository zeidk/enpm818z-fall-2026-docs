====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 5. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``lecture5/`` workspace folder.


.. dropdown:: Exercise 1 -- First-Class Functions and Lambdas
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate your understanding of first-class functions, lambda
    expressions, and built-in higher-order functions (``map``, ``filter``,
    ``sorted``).


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture5/lambdas_and_hof.py`` that implements the
    following. Each named function must include type hints and a
    Google-style docstring.

    1. **``square``** -- A lambda function that squares a number. Assign it
       to a variable called ``square``. Test: ``square(5)`` returns ``25``.

    2. **``add``** -- A lambda function that takes two numbers and returns
       their sum. Assign it to a variable called ``add``. Test:
       ``add(3, 7)`` returns ``10``.

    3. **``is_even``** -- A lambda function that checks if a number is even.
       Returns ``True`` if even, ``False`` otherwise. Assign it to a
       variable called ``is_even``. Test: ``is_even(4)`` returns ``True``.

    4. **``to_upper``** -- A lambda function that converts a string to
       uppercase. Assign it to a variable called ``to_upper``. Test:
       ``to_upper("hello")`` returns ``"HELLO"``.

    5. **Sorting with lambdas** -- Given a list of tuples representing
       ``(name, age)``:

       .. code-block:: python

          people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]

       a) Use ``sorted()`` with a lambda to sort by age (ascending).
       b) Use ``sorted()`` with a lambda to sort by name length.

    In the ``if __name__ == "__main__"`` block, call each function/lambda
    with example arguments and print the results with labels.

    **Expected output:**

    .. code-block:: text

       === Lambda Functions ===
       square(5): 25
       add(3, 7): 10
       is_even(4): True
       is_even(7): False
       to_upper("hello"): HELLO

       === Sorting ===
       By age: [('Bob', 25), ('Alice', 30), ('Charlie', 35)]
       By name length: [('Bob', 25), ('Alice', 30), ('Charlie', 35)]


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture5/lambdas_and_hof.py``
    - The program must run without errors and produce output matching the
      expected format above.


.. dropdown:: Exercise 2 -- Write Your Own Decorators
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice writing decorators with ``*args``/``**kwargs``, using
    ``functools.wraps``, and transforming return values.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture5/custom_decorators.py`` that implements the
    following decorators and test functions. Each decorator and test
    function must include type hints and a Google-style docstring.

    1. **``greet``** -- A decorator that prints
       ``"Hello from <function_name>!"`` before executing the decorated
       function. Apply it to a function called ``say_goodbye()`` that prints
       ``"Goodbye!"``.

    2. **``repeat_twice``** -- A decorator that executes the decorated
       function two times. Apply it to a function called
       ``print_message()`` that prints ``"Hello"``.

    3. **``uppercase_result``** -- A decorator that converts the return
       value of a function to uppercase (assumes the function returns a
       string). Apply it to a function called ``get_name()`` that returns
       ``"alice"``.

    All decorators must use ``@functools.wraps`` to preserve metadata.

    In the ``if __name__ == "__main__"`` block, call each decorated
    function and print the results with labels.

    **Expected output:**

    .. code-block:: text

       === greet decorator ===
       Hello from say_goodbye!
       Goodbye!

       === repeat_twice decorator ===
       Hello
       Hello

       === uppercase_result decorator ===
       get_name() returned: ALICE


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture5/custom_decorators.py``
    - The program must run without errors and produce output matching the
      expected format above.


.. dropdown:: Exercise 3 -- Closures, Callables, and Partials
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice closures with ``nonlocal``, the ``callable()`` built-in, and
    ``functools.partial`` for argument freezing.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture5/closures_and_partials.py`` that implements the
    following. Each function must include type hints and a Google-style
    docstring.

    1. **``make_accumulator``** -- A closure that takes an initial value and
       returns a function. Each call to the returned function adds its
       argument to a running total and returns the new total.

       .. code-block:: python

          acc = make_accumulator(100)
          print(acc(10))  # 110
          print(acc(20))  # 130

    2. **``log_message``** -- A general logging function with the signature
       ``log_message(level: str, msg: str) -> str`` that returns a
       formatted string ``"[<level>] <msg>"``. Use ``functools.partial``
       to create a function ``log_info`` with ``level`` fixed to
       ``"INFO"``.

    In the ``if __name__ == "__main__"`` block, demonstrate both tasks
    with labeled output.

    **Expected output:**

    .. code-block:: text

       === Accumulator (closure) ===
       acc(10): 110
       acc(20): 130
       acc(5): 135

       === Partial: log_info ===
       log_info("System started"): [INFO] System started
       log_info("Sensor ready"): [INFO] Sensor ready


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture5/closures_and_partials.py``
    - The program must run without errors and produce output matching the
      expected format above.


.. dropdown:: Exercise 4 -- Data Processing Pipeline
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Combine decorators, closures, partials, and higher-order functions to
    build a simple data processing pipeline for sensor readings.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture5/pipeline.py`` that implements the following.
    Every function must have type hints and a Google-style docstring.

    1. **``log_call``** -- A decorator that prints the function name when
       called. Use ``@functools.wraps``.

    2. **``make_filter(threshold)``** -- A closure that returns a function.
       The returned function takes a list of numbers and returns only those
       above the threshold.

    3. **``convert_temp``** -- A function with the signature
       ``convert_temp(value: float, from_scale: str, to_scale: str) -> float``
       that converts between Celsius and Fahrenheit. Use
       ``functools.partial`` to create ``to_fahrenheit`` (from Celsius to
       Fahrenheit) and ``to_celsius`` (from Fahrenheit to Celsius).

    4. **Pipeline** -- In the ``if __name__ == "__main__"`` block:

       .. code-block:: python

          readings = [15.2, -3.0, 22.8, 8.1, -1.5, 30.0, 17.6]

       a) Filter out negative readings using ``make_filter(0)``.
       b) Convert each remaining reading to Fahrenheit using
          ``to_fahrenheit`` with ``map``.
       c) Sort the Fahrenheit results using ``sorted()`` with a lambda key.
       d) Apply ``@log_call`` to a function that orchestrates the pipeline.
       e) Print each stage's output with labels.

    **Expected output (values should be computed dynamically):**

    .. code-block:: text

       === Data Processing Pipeline ===
       Calling: process_readings
       Raw readings: [15.2, -3.0, 22.8, 8.1, -1.5, 30.0, 17.6]
       After filtering (> 0): [15.2, 22.8, 8.1, 30.0, 17.6]
       Converted to Fahrenheit: [59.36, 73.04, 46.58, 86.0, 63.68]
       Sorted (ascending): [46.58, 59.36, 63.68, 73.04, 86.0]


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture5/pipeline.py``
    - The program must run without errors and produce output matching the
      expected format above.
    - All calculations must be computed dynamically (no hard-coded results).
    - Every function must include type hints and a Google-style docstring.
