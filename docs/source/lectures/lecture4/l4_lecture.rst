====================================================
Lecture
====================================================



Introduction to Functions
====================================================

Reusable blocks of code that perform a specific task.

Create a file called ``functions_basics_demo.py`` to follow along with the examples below.


.. dropdown:: What Is a Function?
   :open:

   In Python, a **function** is a named block of organized, reusable code that is designed to perform a single, related action.

   **Why Use Functions?**

   - **Modularity** -- Break down complex processes into smaller, manageable pieces. This modular approach makes it easier to understand, develop, and test your code.
   - **Code Reuse** -- Once a function is written, it can be used multiple times throughout your program, reducing the chances of errors and inconsistencies.
   - **Easier Maintenance** -- Making a change in one function can affect the entire program if that function is used throughout. This centralized approach makes it easier to update and maintain your programs.
   - **Foundation for Advanced Concepts** -- Functions form the basis for understanding closures, decorators, and concurrency.


.. dropdown:: Basic Structure
   :open:

   **Anatomy of a Function**

   - **Function Definition** -- Begins with the ``def`` keyword, followed by the function name, parentheses ``()`` containing any parameters, and a colon ``:``.
   - **Parameters (Optional)** -- Variables listed inside the parentheses that act as placeholders for the values you pass into the function.
   - **Docstring (Recommended)** -- A documentation string immediately following the function definition.
   - **Function Body** -- The indented block of code that executes when the function is called.
   - **Return Statement (Optional)** -- Sends a value back to the caller using ``return``. If omitted, the function returns ``None``.

   .. note::

      **Syntax**:

      .. code-block:: python

         def function_name(param1, param2):
             """Documentation string."""
             # function body
             return something

   **Example**

   .. code-block:: python

      def greet(name):
          """
          Print a greeting message to the user.

          Args:
              name (str): The name of the user.
          """
          print(f"Hello, {name}!")

      greet("Alice")  # Hello, Alice!

   .. tip::

      To access the docstring of any function, use ``print(greet.__doc__)`` or the built-in ``help(greet)``.


.. dropdown:: Best Practices and Conventions
   :open:

   - **Use** ``snake_case`` **for function names** -- All lowercase with underscores separating words. Class names use ``PascalCase``, but functions and variables always use ``snake_case``.

     .. code-block:: python

        def compute_distance(x1, y1, x2, y2):  # Good
        def ComputeDistance(x1, y1, x2, y2):   # Bad (PascalCase is for classes)

   - **Start with a verb** -- Function names should describe an action: ``get_``, ``compute_``, ``is_``, ``has_``, ``create_``, ``update_``, ``validate_``. Use ``is_``/``has_`` for functions returning booleans.

     .. code-block:: python

        def compute_area(length, width):  # Good (verb + noun)
        def area(length, width):          # Acceptable but less descriptive
        def is_valid(sensor_id):          # Good (boolean return)

   - **Always include a docstring** -- Every function should have a docstring explaining what it does, its parameters, and its return value.
   - **Do one thing well** -- A function should perform a single, well-defined task. If a function does too many things, split it into smaller functions.
   - **Keep functions short** -- If a function exceeds 20-30 lines, consider refactoring.
   - **Add type hints** -- Annotate parameters and return types for clarity.

   **References**: `PEP 8: Function and Variable Names <https://peps.python.org/pep-0008/#function-and-variable-names>`_ | `PEP 257: Docstring Conventions <https://peps.python.org/pep-0257/>`_ | `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html#316-naming>`_


.. dropdown:: Google-Style Docstrings
   :open:

   When writing docstrings, use a consistent convention. The **Google style** is widely used in Python projects.

   .. code-block:: python

      def compute_distance(x1, y1, x2, y2):
          """Compute the Euclidean distance between two 2D points.

          Args:
              x1 (float): X-coordinate of the first point.
              y1 (float): Y-coordinate of the first point.
              x2 (float): X-coordinate of the second point.
              y2 (float): Y-coordinate of the second point.

          Returns:
              float: The Euclidean distance between the two points.
          """
          return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

      print(compute_distance(0, 0, 3, 4))  # 5.0

   .. warning::

      For brevity, some examples in these slides omit docstrings. This is **not** good practice. Always include a docstring when you define a function, whether for assignments, projects, or professional code.


Function Calls
====================================================

Invoking functions, returning values, and understanding redefinitions.

Create a file called ``function_calls_demo.py`` to follow along with the examples below.


.. dropdown:: Calling a Function
   :open:

   To call a function, use the function's name followed by parentheses containing the arguments that match the function's parameters.

   .. code-block:: python

      # function definition
      def add(a, b):
          return a + b

      # function call
      result = add(1, 2)
      print(f"{result=}")  # result=3

   **Steps Involved in a Function Call**

   1. **Name Resolution** -- Python looks up the function name to find its definition.
   2. **Argument Matching** -- Arguments are matched with parameters in order.
   3. **New Scope Creation** -- A new local scope is created for the function.
   4. **Body Execution** -- The code inside the function runs.
   5. **Return Value** -- The result (or ``None``) is sent back to the caller.
   6. **Cleanup** -- The local scope is discarded.


.. dropdown:: Multiple Return Values
   :open:

   A function can return multiple values as a tuple, which can be unpacked by the caller.

   .. code-block:: python

      def rectangle_info(length, width):
          area = length * width
          perimeter = 2 * (length + width)
          return area, perimeter  # Returns a tuple

      # Tuple unpacking
      area, perimeter = rectangle_info(5, 3)
      print(f"{area=}, {perimeter=}")  # area=15, perimeter=16

   .. note::

      ``return area, perimeter`` is equivalent to ``return (area, perimeter)``. Python implicitly creates a tuple.


.. dropdown:: Function Redefinitions
   :open:

   In Python, function names are just variables bound to function objects. Redefining a function replaces the old binding.

   .. code-block:: python

      def greet():
          print("Hello!")

      greet()  # Hello!

      # Redefining the function
      def greet():
          print("Hi there!")

      greet()  # Hi there!  (the original version is gone)

   .. warning::

      Python does **not** warn you when you redefine a function. The new definition silently replaces the previous one. Be careful with naming!


Function Arguments
====================================================

Understanding how data flows into functions.

Create a file called ``function_arguments_demo.py`` to follow along with the examples below.


.. dropdown:: Positional Arguments
   :open:

   **Positional arguments** are arguments that must be passed in the correct order when calling a function. The order must match the order in which the parameters were defined.

   .. code-block:: python

      def display_info(name, age):
          print(f"{name=}, {age=}")

      # Correct usage
      display_info("Alice", 30)  # name='Alice', age=30

      # Incorrect usage - values get swapped
      display_info(30, "Alice")  # name=30, age='Alice'


.. dropdown:: Default Arguments
   :open:

   **Default arguments** allow you to specify values that parameters take if no argument is provided during the function call.

   .. code-block:: python

      def display_info(name, age=35):
          print(f"{name=}, {age=}")

      display_info("Bob")        # name='Bob', age=35
      display_info("Alice", 30)  # name='Alice', age=30

   **Ordering Rule**

   Parameters with default values **must come after** those without default values.

   .. code-block:: python

      # Correct
      def func(a, b, c=10, d=20):
          pass

      # SyntaxError: non-default argument follows default argument
      # def func(a, b=10, c, d=20):
      #     pass


.. dropdown:: Danger: Mutable Default Values
   :open:

   Default values are evaluated **once** when the function is defined, not each time it is called. Using a mutable object (like a list) as a default value can lead to surprising behavior.

   .. code-block:: python

      # BAD: Mutable default value
      def add_item_bad(item, items=[]):
          items.append(item)
          return items

      print(add_item_bad("apple"))   # ['apple']
      print(add_item_bad("banana"))  # ['apple', 'banana'] -- Surprise!

   .. code-block:: python

      # GOOD: Use None and create a new list each time
      def add_item_good(item, items=None):
          if items is None:
              items = []
          items.append(item)
          return items

      print(add_item_good("apple"))   # ['apple']
      print(add_item_good("banana"))  # ['banana']


.. dropdown:: Keyword Arguments
   :open:

   **Keyword arguments** allow you to pass arguments by explicitly naming the parameter, regardless of their position in the function call.

   .. code-block:: python

      def create_robot(name, robot_type, speed):
          print(f"{name}: {robot_type}, max speed={speed} m/s")

      # Using keyword arguments (order does not matter)
      create_robot(speed=0.26, name="TurtleBot3", robot_type="mobile")

   **Mixing Positional and Keyword Arguments**

   .. code-block:: python

      # Positional args must come before keyword args
      create_robot("TurtleBot3", speed=0.26, robot_type="mobile")

      # SyntaxError: positional argument follows keyword argument
      # create_robot(name="TurtleBot3", "mobile", speed=0.26)

   .. warning::

      Once you use a keyword argument in a function call, all subsequent arguments must also be keyword arguments.


.. dropdown:: Variable-Length Positional Arguments (``*args``)
   :open:

   ``*args`` (``args`` is a convention) allows a function to accept any number of positional arguments. Inside the function, ``args`` is a tuple.

   .. note::

      **Syntax**: ``def function_name(*args):``

   .. code-block:: python

      def compute_sum(*args):
          print(f"args = {args}")   # args is a tuple
          print(f"type = {type(args)}")
          return sum(args)

      print(compute_sum(1, 2, 3))        # 6
      print(compute_sum(10, 20, 30, 40)) # 100


.. dropdown:: Variable-Length Keyword Arguments (``**kwargs``)
   :open:

   ``**kwargs`` (``kwargs`` is a convention) allows a function to accept any number of keyword arguments. Inside the function, ``kwargs`` is a dictionary.

   .. note::

      **Syntax**: ``def function_name(**kwargs):``

   .. code-block:: python

      def print_robot_config(**kwargs):
          """Print all keyword arguments as key-value pairs."""
          for key, value in kwargs.items():
              print(f"  {key}: {value}")

      print_robot_config(name="UR5", joints=6, payload=5.0)
      # name: UR5
      # joints: 6
      # payload: 5.0


.. dropdown:: Combining ``*args`` and ``**kwargs``
   :open:

   .. code-block:: python

      def log_message(level, *args, **kwargs):
          print(f"[{level}] args={args}, kwargs={kwargs}")

      log_message("INFO", 1, 2, 3, user="Alice", action="login")
      # [INFO] args=(1, 2, 3), kwargs={'user': 'Alice', 'action': 'login'}

   **Parameter Ordering Rules**

   When defining a function, parameters must appear in this order:

   1. Standard positional parameters
   2. ``*args`` (variable-length positional)
   3. Keyword-only parameters (after ``*args``)
   4. ``**kwargs`` (variable-length keyword)

   .. code-block:: python

      def example(a, b, *args, option=True, **kwargs):
          print(f"{a=}, {b=}, {args=}, {option=}, {kwargs=}")

      example(1, 2, 3, 4, option=False, x=10)
      # a=1, b=2, args=(3, 4), option=False, kwargs={'x': 10}


.. dropdown:: Argument Packing
   :open:

   **Argument packing** is the process of collecting multiple arguments into a single parameter. This is what ``*args`` and ``**kwargs`` do: they *pack* multiple values into a tuple or dictionary.

   .. code-block:: python

      # *args packs positional arguments into a tuple
      def show_args(*args):
          print(f"Packed into tuple: {args}")

      show_args(1, 2, 3)  # Packed into tuple: (1, 2, 3)

      # **kwargs packs keyword arguments into a dict
      def show_kwargs(**kwargs):
          print(f"Packed into dict: {kwargs}")

      show_kwargs(x=10, y=20)  # Packed into dict: {'x': 10, 'y': 20}


.. dropdown:: Argument Unpacking
   :open:

   **Argument unpacking** is the reverse: spreading elements of a sequence or mapping into individual arguments during a function call.

   .. code-block:: python

      def add(a, b, c):
          return a + b + c

      # Unpack a list/tuple with *
      values = [1, 2, 3]
      print(add(*values))  # print(add(1,2,3)) -> 6

      # Unpack a dictionary with **
      params = {"a": 10, "b": 20, "c": 30}
      print(add(**params))  # print(add(a=10, b=20, c=30)) -> 60

   .. note::

      ``*`` unpacks sequences into positional arguments. ``**`` unpacks dictionaries into keyword arguments. The dictionary keys must match the parameter names.


Scopes
====================================================

Where variables live and how Python resolves names.

Create a file called ``scopes_demo.py`` to follow along with the examples below.


.. dropdown:: The LEGB Rule
   :open:

   A **scope** is the region of a program where a variable is accessible. Python resolves names using the **LEGB rule**, searching in this order:

   - **L -- Local**: Names defined inside the current function.
   - **E -- Enclosing**: Names in the scope of any enclosing (outer) functions.
   - **G -- Global**: Names defined at the top level of the module.
   - **B -- Built-in**: Names pre-defined in Python (``len``, ``print``, ``True``, etc.).

   .. code-block:: python

      x = "global"          # Global scope

      def outer():
          x = "enclosing"   # Enclosing scope
          def inner():
              x = "local"   # Local scope
              print(x)       # "local" (L found first)
          inner()

      outer()


.. dropdown:: Local Scope (L)
   :open:

   The local scope includes names defined inside the current function, including its parameters.

   .. code-block:: python

      def local_test(local_param):
          local_var = "I am local var"
          print(local_param)  # Accessible
          print(local_var)    # Accessible

      local_test("I am local param")
      # print(local_var)    # NameError: name 'local_var' is not defined
      # print(local_param)  # NameError: name 'local_param' is not defined

   .. note::

      Variables created inside a function exist only while the function is executing. They are discarded when the function returns.


.. dropdown:: Enclosing Scope (E)
   :open:

   The enclosing scope applies to nested functions. The inner function can access variables from the outer function.

   .. code-block:: python

      def outer_func():
          enclosing_var = "I am enclosing"

          def inner_func():
              local_var = "I am local"
              print(enclosing_var)  # Accessible as an enclosing variable
              print(local_var)      # Accessible as a local variable

          inner_func()

      outer_func()


.. dropdown:: Nested Functions
   :open:

   A **nested function** (or inner function) is a function defined inside another function. The inner function has access to variables in the enclosing (outer) function's scope.

   **Why Use Nested Functions?**

   - **Encapsulation** -- Hide helper logic that is only relevant inside the outer function. The inner function is invisible to the rest of the program.
   - **Closures** -- The inner function can "remember" variables from the enclosing scope even after the outer function has returned (covered in L5).
   - **Decorators** -- Built on nested functions that wrap and extend other functions (covered in L5).


.. dropdown:: The ``nonlocal`` Keyword
   :open:

   To **modify** an enclosing variable from the inner function, use ``nonlocal``. Without it, assigning creates a new local variable.

   .. code-block:: python
      :linenos:

      def outer_func():
          count = 0
          def inner_func():
              nonlocal count
              count += 1
          inner_func()
          print(count)  # 1

      outer_func()

   .. tip::

      **Question:** What happens if you comment out line 4?


.. dropdown:: Global Scope (G)
   :open:

   The global scope includes names defined at the top level of a Python file.

   .. code-block:: python

      global_var = "I am global"

      def my_func():
          print(global_var)  # Accessible (reading is fine)

      my_func()

   **The** ``global`` **Keyword**

   To **rebind** a global variable inside a function, use the ``global`` keyword.

   .. code-block:: python

      global_var = "I am global"

      def my_func():
          global global_var
          global_var = "Modified inside function"

      my_func()
      print(global_var)  # "Modified inside function"

   .. warning::

      Overusing ``global`` makes code harder to debug and test. Prefer passing values as arguments and returning results instead.


.. dropdown:: Mutable Globals: No ``global`` Needed for In-Place Modifications
   :open:

   You do **not** need the ``global`` keyword to modify a mutable global object in place, because you are not rebinding the name.

   .. code-block:: python

      fruits = ["apple", "banana", "cherry"]

      def add_to_list(item):
          fruits.append(item)  # In-place mutation, no rebinding

      add_to_list("orange")
      print(fruits)  # ['apple', 'banana', 'cherry', 'orange']

   .. note::

      **Why?** ``fruits.append(item)`` modifies the existing list object. The name ``fruits`` still points to the same object. The ``global`` keyword is only needed when you want to *reassign* the name itself (e.g., ``fruits = [...]``).


.. dropdown:: Built-in Scope (B)
   :open:

   The built-in scope includes names pre-defined in Python:

   - **Functions**: ``len``, ``print``, ``id``, ``range``, ``type``, etc.
   - **Types**: ``int``, ``str``, ``list``, ``dict``, etc.
   - **Constants**: ``True``, ``False``, ``None``
   - **Exception classes**: ``ValueError``, ``TypeError``, etc.

   .. code-block:: python

      # List all built-in names
      print(dir(__builtins__))

   .. warning::

      Avoid shadowing built-in names! For example, never name a variable ``list``, ``dict``, ``type``, or ``id``. This hides the built-in and can cause confusing errors.

   .. code-block:: python

      list = [1, 2, 3]          # Shadows the built-in list()
      print(list)                # [1, 2, 3] -- works fine here

      nums = list(range(5))      # TypeError: 'list' object is not callable
      # Python thinks 'list' is [1, 2, 3], not the built-in list()


Pass-by-Assignment
====================================================

How Python passes arguments to functions.

Create a file called ``pass_by_assignment_demo.py`` to follow along with the examples below.


.. dropdown:: How Python Passes Arguments
   :open:

   Python's argument-passing mechanism is called **pass-by-assignment** (sometimes called "pass-by-object-reference"). It is neither purely pass-by-value nor pass-by-reference.

   - **Function arguments are passed by object reference** -- When you pass an argument, Python passes a reference to the object, not a copy.
   - **Immutable objects** (int, str, tuple) -- Changes inside the function create a new object; the original remains unchanged.
   - **Mutable objects** (list, dict, set) -- In-place modifications inside the function affect the original object.
   - **Reassignment creates a new binding** -- If you reassign a parameter to a new object inside a function, this does not affect the original variable outside.


.. dropdown:: Immutable vs Mutable Examples
   :open:

   .. tab-set::

       .. tab-item:: Immutable

           .. code-block:: python

              def update_number(x):
                  x = 10  # Creates a new local binding

              num = 5
              update_number(num)
              print(num)  # 5 (unchanged)

       .. tab-item:: Mutable

           .. code-block:: python

              def update_list(a_list):
                  a_list.append(4)  # Modifies the original object in place

              my_list = [1, 2, 3]
              update_list(my_list)
              print(my_list)  # [1, 2, 3, 4] (modified!)

   .. note::

      ``a_list.append(4)`` mutates the existing list. But ``a_list = [10, 20]`` would rebind the local name ``a_list`` to a new list, leaving the original unchanged.


.. dropdown:: Predict the Outputs
   :open:

   .. code-block:: python

      def edit_inputs(fruits, animals, age):
          fruits.append('cherry')
          fruits[0] = 'mango'
          fruits = ['quince', 'pear']
          animals = ['elephant']
          age += 1

      fruits = ["apple", "banana"]
      animals = ["bear", "tiger"]
      age = 40

      print(fruits, animals, age)
      edit_inputs(fruits, animals, age)
      print(fruits, animals, age)

   .. dropdown:: Reveal Answer
       :class-container: sd-border-success

       .. code-block:: text

          ['apple', 'banana'] ['bear', 'tiger'] 40
          ['mango', 'banana', 'cherry'] ['bear', 'tiger'] 40

       - ``fruits.append('cherry')`` and ``fruits[0] = 'mango'`` mutate the original list.
       - ``fruits = ['quince', 'pear']`` rebinds the local name, so the original is not affected by this line.
       - ``animals = ['elephant']`` rebinds the local name; the original list is unchanged.
       - ``age += 1`` creates a new int locally; the original ``age`` is unchanged.


Type Hints
====================================================

Annotating functions with expected types for clarity and tooling.

Create a file called ``type_hints_demo.py`` to follow along with the examples below.


.. dropdown:: Introduction to Type Hints
   :open:

   **Type hints** (also called type annotations) allow you to specify the expected types of function parameters and return values. They are **not enforced** at runtime but improve readability and enable static analysis tools like ``mypy``.

   .. note::

      **Syntax**: ``def func(param: type) -> return_type:``

   .. code-block:: python

      def add(a: int, b: int) -> int:
          return a + b

      def greet(name: str) -> None:
          print(f"Hello, {name}!")

      # Type hints are NOT enforced at runtime
      result = add("hello", " world")  # Works! Returns "hello world"


.. dropdown:: Why Use Type Hints?
   :open:

   - **Documentation** -- Makes function signatures self-documenting.
   - **IDE Support** -- Enables better autocompletion and error detection.
   - **Static Analysis** -- Tools like ``mypy`` can catch type errors before runtime.
   - **Team Communication** -- Makes the expected interface clear to other developers.


.. dropdown:: ``Optional`` -- A Value That Might Be ``None``
   :open:

   ``Optional[X]`` means the value is either of type ``X`` or ``None``. This is common for functions that may fail to find a result.

   .. code-block:: python

      from typing import Optional

      def find_index(items: list[str], target: str) -> Optional[int]:
          """Return the index of target in items, or None."""
          for i, item in enumerate(items):
              if item == target:
                  return i
          return None

      sensors = ["lidar", "camera", "imu"]
      result = find_index(sensors, "camera")
      print(result)  # 1

      result = find_index(sensors, "radar")
      print(result)  # None

   .. note::

      ``Optional[int]`` is equivalent to ``Union[int, None]``. It signals to the caller that the return value must be checked before use.


.. dropdown:: ``Union`` -- One of Several Types
   :open:

   ``Union[X, Y]`` means the value can be of type ``X`` or type ``Y``. This is useful when a function accepts or returns more than one type.

   .. code-block:: python

      from typing import Union

      def normalize(data: Union[str, list]) -> list[str]:
          """Convert input to a list of strings."""
          if isinstance(data, str):
              return [data]
          return [str(item) for item in data]

      print(normalize("hello"))       # ['hello']
      print(normalize([1, 2, 3]))     # ['1', '2', '3']

   .. note::

      Use ``Union`` when a function genuinely needs to handle multiple types. If you find yourself using ``Union`` with many types, consider whether the function is doing too much.


.. dropdown:: Python 3.10+ Simplified Syntax
   :open:

   Starting with Python 3.10, you can use the ``|`` operator instead of importing ``Optional`` and ``Union`` from the ``typing`` module.

   .. code-block:: python

      # Before Python 3.10
      from typing import Optional, Union

      def find_item(name: str) -> Optional[int]:
          ...

      def process(data: Union[str, list]) -> str:
          ...

   .. code-block:: python

      # Python 3.10+ (no import needed)
      def find_item(name: str) -> int | None:
          ...

      def process(data: str | list) -> str:
          ...

   .. tip::

      Use the ``|`` syntax if your project targets Python 3.10 or later. It is more readable and requires no imports.


.. dropdown:: Collection Type Hints
   :open:

   .. code-block:: python

      # Python 3.9+ - use built-in types directly
      def process_readings(readings: list[float]) -> float:
          return sum(readings) / len(readings)

      def get_config() -> dict[str, int]:
          return {"timeout": 30, "retries": 3}

      def get_coordinates() -> tuple[float, float]:
          return (3.14, 2.72)

      # Variable-length tuple (all same type)
      def get_ids() -> tuple[int, ...]:
          return (1, 2, 3, 4, 5)

      # Combining with functions
      def transform(items: list[str],
                    func: callable) -> list[str]:
          return [func(item) for item in items]


Recursive Functions
====================================================

Functions that call themselves to solve problems.

Create a file called ``recursion_demo.py`` to follow along with the examples below.


.. dropdown:: What Is Recursion?
   :open:

   A **recursive function** is a function that calls itself within its own definition. Every recursive function needs:

   - A **base case** -- the condition that stops the recursion.
   - A **recursive case** -- the function calling itself with a simpler input.

   **Example: Factorial**

   .. code-block:: python

      def factorial(n: int) -> int:
          """Compute n! recursively."""
          if n == 0:           # Base case
              return 1
          else:                # Recursive case
              return n * factorial(n - 1)

      print(factorial(5))  # 120  (5 * 4 * 3 * 2 * 1)

   .. warning::

      Without a proper base case, recursion leads to infinite calls and a ``RecursionError``. Python's default recursion limit is 1000 calls.


.. dropdown:: Tracing the Call Stack
   :open:

   Each recursive call creates a new frame on the call stack:

   .. list-table::
      :widths: 40 40
      :header-rows: 1
      :class: compact-table

      * - Call
        - Returns
      * - ``factorial(5)``
        - ``5 * factorial(4)``
      * - ``factorial(4)``
        - ``4 * factorial(3)``
      * - ``factorial(3)``
        - ``3 * factorial(2)``
      * - ``factorial(2)``
        - ``2 * factorial(1)``
      * - ``factorial(1)``
        - ``1 * factorial(0)``
      * - ``factorial(0)``
        - ``1`` (base case)

   The results then propagate back up: ``1 -> 1 -> 2 -> 6 -> 24 -> 120``

   .. note::

      Each call to ``factorial`` has its own local variable ``n``. This is possible because each call gets its own scope on the call stack.


Summary
--------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card::
        :class-card: sd-border-primary

        - **Function Basics** -- ``def``, parameters, docstrings, ``return``, multiple return values
        - **Arguments** -- Positional, default, keyword, ``*args``, ``**kwargs``
        - **Packing/Unpacking** -- ``*`` for sequences, ``**`` for dicts

    .. grid-item-card::
        :class-card: sd-border-primary

        - **Scopes** -- LEGB rule, ``global``, ``nonlocal``
        - **Pass-by-Assignment** -- Mutable vs immutable behavior in function calls
        - **Type Hints** -- Annotations for parameters and return types
        - **Recursion** -- Base case, recursive case, call stack

.. list-table:: Argument Types at a Glance
   :widths: 25 30 30
   :header-rows: 1
   :class: compact-table

   * - Argument Type
     - Syntax
     - Key Rule
   * - Positional
     - ``func(a, b)``
     - Order matters
   * - Default
     - ``func(a, b=10)``
     - Must follow non-defaults
   * - Keyword
     - ``func(b=10, a=5)``
     - Order does not matter
   * - ``*args``
     - ``func(*args)``
     - Packed into a tuple
   * - ``**kwargs``
     - ``func(**kwargs)``
     - Packed into a dict

.. note::

   **Reminder**: Review and experiment with all provided code before next class.


Preview: What's Next in L5
---------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: L5: Advanced Functions
        :class-card: sd-border-primary

        - Programming paradigms (procedural, functional, OOP)
        - First-class functions and lambdas
        - Closures and callables
        - Decorators
        - Partial functions

.. note::

   Today's lecture gives you the function fundamentals that are essential for understanding the advanced function concepts in L5 and object-oriented programming later in the course.