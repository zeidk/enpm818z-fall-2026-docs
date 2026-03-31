====================================================
Lecture
====================================================



Programming Paradigms
====================================================

Different ways to organize and think about code.

Refer to ``paradigms_demo.py`` to follow along with the examples below.


.. dropdown:: What Is a Programming Paradigm?
   :open:

   A **programming paradigm** is a fundamental style or approach to organizing and structuring code. It defines how you think about problems and express solutions.

   **Three Major Paradigms**

   - **Procedural** -- You tell the computer *how* to do something step by step. Code is organized around statements that change program state.
   - **Object-Oriented (OOP)** -- You organize code around objects that bundle data (attributes) and behavior (methods). Emphasis on encapsulation, inheritance, and polymorphism.
   - **Functional** -- You express computation as the evaluation of mathematical functions. Emphasis on immutability, pure functions, and avoiding side effects.

   .. note::

      Python is a **multi-paradigm** language. You can mix procedural, object-oriented, and functional styles in the same program.


.. dropdown:: Comparing Approaches
   :open:

   **Same Problem, Three Paradigms**

   Task: Given a list of numbers, compute the sum of all even numbers.

   .. code-block:: python

      # Imperative
      nums = [1, 2, 3, 4, 5, 6]
      total = 0
      for n in nums:
          if n % 2 == 0:
              total += n
      print(total)  # 12

   .. code-block:: python

      # Functional
      nums = [1, 2, 3, 4, 5, 6]
      total = sum(filter(
          lambda x: x % 2 == 0,
          nums
      ))
      print(total)  # 12

   .. code-block:: python

      # Object-Oriented
      class NumberProcessor:
          def __init__(self, numbers: list[int]):
              self._numbers = numbers

          def sum_even(self) -> int:
              return sum(n for n in self._numbers if n % 2 == 0)

      processor = NumberProcessor([1, 2, 3, 4, 5, 6])
      print(processor.sum_even())  # 12


.. dropdown:: Key Principles of Functional Programming
   :open:

   Functional programming is built on a small set of principles that promote predictable, testable, and composable code.

   - **Pure Functions** -- A function whose output depends only on its inputs and produces no side effects (no modifying external state, no I/O). Given the same inputs, a pure function always returns the same output.

     - Think of a mathematical function like f(x) = x^2 + 1: for any input x, the output is always the same, and computing f(3) = 10 does not change anything else in the world.

   - **Immutability** -- Data is not modified after creation. Instead of changing an object, you create a new one.

     - For example, rather than sorting a list in place with ``my_list.sort()``, a functional approach uses ``sorted(my_list)`` to produce a new sorted list while leaving the original unchanged.

   - **First-Class Functions** -- Functions can be assigned to variables, passed as arguments, and returned from other functions.
   - **Higher-Order Functions** -- Functions that take other functions as arguments or return functions as results.
   - **Avoiding Side Effects** -- Minimize or isolate operations that change state outside the function's scope.

   **Example: Pure vs. Impure**

   .. code-block:: python

      # Pure function (no side effects, depends only on inputs)
      def add(a: int, b: int) -> int:
          return a + b


      # Impure function (side effect: modifies external state)
      results = []

      def add_and_store(a: int, b: int) -> int:
          result = a + b
          results.append(result)  # Side effect!
          return result


Callables
====================================================

Objects that behave like functions.

Refer to ``callables_demo.py`` to follow along with the examples below.


.. dropdown:: What Is a Callable?
   :open:

   A **callable** is any object that can be called using parentheses ``()``. In Python, several types of objects are callable:

   - **Functions** defined with ``def``
   - **Lambda** expressions
   - **Classes** (calling a class creates an instance)
   - **Instances** of classes that define the ``__call__`` method
   - **Built-in functions** like ``len``, ``print``, ``range``

   .. code-block:: python

      def do_nothing():
          pass

      print(callable(do_nothing))  # True
      print(callable(lambda x: x))  # True
      print(callable(int))  # True (classes are callable)
      print(callable(42))  # False (integers are not callable)
      print(callable("hello"))  # False


First-Class Functions
====================================================

Functions as objects you can assign, pass, and return.

Refer to ``first_class_demo.py`` to follow along with the examples below.


.. dropdown:: What Does "First-Class" Mean?
   :open:

   In Python, functions are **first-class objects**. This means functions can be treated just like any other object (integers, strings, lists). Specifically, functions can be:

   - **Assigned to variables** -- Store a function reference in a variable name.
   - **Passed as arguments** -- Hand a function to another function as a parameter.
   - **Returned from functions** -- Have a function produce another function as output.
   - **Stored in data structures** -- Put functions in lists, dictionaries, or other containers.

   .. code-block:: python

      def compute_square(x):
          return x**2

      # Assigning a function to a variable
      f = compute_square  # No parentheses! f is now the function object
      print(f(5))  # 25
      print(type(f))  # <class 'function'>

   .. warning::

      ``f = compute_square`` assigns the function object. ``f = compute_square()`` calls the function and assigns the return value. These are very different!

   .. tip::

      When debugging callbacks or higher-order functions, print the function object itself (not its return value) to verify you are passing the right function. For example, ``print(do_nothing)`` shows ``<function do_nothing at 0x...>``, while ``print(do_nothing())`` calls the function and prints its return value.


.. dropdown:: Passing Functions as Arguments
   :open:

   **Callbacks and Higher-Order Functions**

   A **higher-order function** is a function that takes another function as an argument or returns one. The function passed in is sometimes called a **callback**.

   .. code-block:: python

      def apply_operation(func, a, b):
          """Apply the given function to a and b."""
          return func(a, b)

      def add(x, y):
          return x + y

      def multiply(x, y):
          return x * y

      print(apply_operation(add, 3, 4))  # 7
      print(apply_operation(multiply, 3, 4))  # 12

   .. note::

      **Robotics Application**: Callbacks are commonly used in ROS 2 subscriber nodes, where you pass a function that is invoked each time a new message arrives on a topic.


.. dropdown:: Returning Functions
   :open:

   **Factory Functions**

   A function can create and return a new function. This is the foundation for closures and decorators, which we will cover later in this lecture.

   .. code-block:: python

      def make_multiplier(factor):
          """Return a function that multiplies its input by factor."""
          def multiply_value(x):
              return x * factor
          return multiply_value  # Return the inner function object

      double = make_multiplier(2)
      triple = make_multiplier(3)

      print(double(5))  # 10
      print(triple(5))  # 15
      print(type(double))  # <class 'function'>

   .. note::

      **Key Insight**: Each call to ``make_multiplier`` creates a new ``multiply_value`` function with its own ``factor`` value. The inner function "remembers" the value of ``factor`` even after ``make_multiplier`` has returned. This is a closure.


.. dropdown:: Functions in Data Structures
   :open:

   **Storing Functions in Collections**

   Since functions are objects, they can be stored in lists, dictionaries, and other data structures. This pattern is useful for dispatch tables and plugin systems.

   .. code-block:: python

      def add(a, b):
          return a + b

      def multiply(a, b):
          return a * b

      # Dispatch table: map operation names to functions
      operations = {
          "add": add,
          "multiply": multiply,
      }

      op_name = "multiply"
      result = operations[op_name](6, 7)
      print(f"{op_name}(6, 7) = {result}")  # multiply(6, 7) = 42


.. dropdown:: Built-in Higher-Order Functions: ``map``
   :open:

   **``map``: Apply a Function to Every Element**

   ``map(func, iterable)`` applies ``func`` to each element and returns a lazy iterator. Wrap the result in ``list()`` to see all values.

   .. code-block:: python

      def compute_square(x):
          return x**2

      nums = [1, 2, 3, 4, 5]
      squared = list(map(compute_square, nums))
      print(squared)  # [1, 4, 9, 16, 25]

      # Also works with built-in functions
      words = ["hello", "world"]
      upper_words = list(map(str.upper, words))
      print(upper_words)  # ['HELLO', 'WORLD']

   .. note::

      ``map`` returns a lazy iterator, not a list. Wrap it in ``list()`` to materialize the results. We will see a more concise way to write the function argument when we cover **lambda functions** later in this lecture.


.. dropdown:: Built-in Higher-Order Functions: ``filter``
   :open:

   **``filter``: Keep Elements That Satisfy a Condition**

   ``filter(func, iterable)`` keeps only the elements for which ``func`` returns ``True``.

   .. code-block:: python

      def check_even(x):
          return x % 2 == 0

      nums = [1, 2, 3, 4, 5, 6]
      evens = list(filter(check_even, nums))
      print(evens)  # [2, 4, 6]

      def check_positive(x):
          return x > 0

      readings = [12.5, -3.1, 8.0, -0.5, 15.2]
      valid = list(filter(check_positive, readings))
      print(valid)  # [12.5, 8.0, 15.2]

   .. note::

      Like ``map``, ``filter`` also returns a lazy iterator. If ``func`` is ``None``, ``filter`` removes all falsy values (``0``, ``""``, ``None``, etc.).


.. dropdown:: Built-in Higher-Order Functions: ``sorted`` with ``key``
   :open:

   **``sorted``: Sort by a Custom Criterion**

   The ``key`` parameter of ``sorted`` accepts a function that extracts a comparison value from each element.

   .. code-block:: python

      # Sort strings by length
      words = ["banana", "apple", "cherry", "date"]
      by_length = sorted(words, key=len)
      print(by_length)  # ['date', 'apple', 'banana', 'cherry']

      # Sort tuples by second element using a named function
      def extract_score(pair):
          return pair[1]

      students = [("Alice", 88), ("Bob", 95), ("Charlie", 72)]
      by_score = sorted(students, key=extract_score)
      print(by_score)  # [('Charlie', 72), ('Alice', 88), ('Bob', 95)]

      # Reverse order
      by_score_desc = sorted(students, key=extract_score, reverse=True)
      print(by_score_desc)  # [('Bob', 95), ('Alice', 88), ('Charlie', 72)]


.. dropdown:: List Comprehensions vs. ``map``/``filter``
   :open:

   List comprehensions are often more readable than ``map`` and ``filter``, especially for simple transformations.

   .. code-block:: python

      nums = [1, 2, 3, 4, 5]

      # Using map + filter
      result_1 = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, nums)))
      print(result_1)  # [4, 16]

      # Using list comprehension (preferred)
      result_2 = [x ** 2 for x in nums if x % 2 == 0]
      print(result_2)  # [4, 16]

   .. note::

      **Guideline**: Prefer list comprehensions when the transformation is simple and the ``lambda`` would be short. Use ``map``/``filter`` when you already have a named function to pass.


Lambda Functions
====================================================

Small, anonymous, single-expression functions.

Refer to ``lambda_demo.py`` to follow along with the examples below.


.. dropdown:: Definition and Syntax
   :open:

   **What Is a Lambda?**

   A **lambda** is a small anonymous function defined with the ``lambda`` keyword. It can take any number of parameters but contains only a **single expression** (no statements, no multi-line logic).

   .. note::

      **Syntax**: ``lambda parameters: expression``

   .. code-block:: python

      # Regular function
      def add(a, b):
          return a + b

      # Equivalent lambda
      add_lambda = lambda a, b: a + b

      print(add(3, 4))  # 7
      print(add_lambda(3, 4))  # 7

   .. warning::

      Assigning a lambda to a variable (like ``add_lambda = lambda ...``) is discouraged by PEP 8. If you need a named function, use ``def``. Lambdas are intended for short, inline use.


.. dropdown:: Common Use Cases: Inline Sorting Keys
   :open:

   Lambdas are most commonly used as short, throwaway functions for arguments like ``key`` in ``sorted``.

   .. code-block:: python

      # Sort a list of tuples by the second element
      pairs = [(1, "banana"), (3, "apple"), (2, "cherry")]
      sorted_pairs = sorted(pairs, key=lambda pair: pair[1])
      print(sorted_pairs)
      # [(3, 'apple'), (1, 'banana'), (2, 'cherry')]

      # Sort robots by speed (descending)
      robots = [
          {"name": "TurtleBot", "speed": 0.26},
          {"name": "Spot", "speed": 1.6},
          {"name": "Atlas", "speed": 2.5},
      ]
      fastest_first = sorted(robots, key=lambda r: r["speed"], reverse=True)
      for r in fastest_first:
          print(f"  {r['name']}: {r['speed']} m/s")


.. dropdown:: Common Use Cases: ``map`` and ``filter``
   :open:

   .. code-block:: python

      # Convert sensor readings from Celsius to Fahrenheit
      celsius = [0.0, 20.0, 37.5, 100.0]
      fahrenheit = list(map(lambda c: c * 9 / 5 + 32, celsius))
      print(fahrenheit)  # [32.0, 68.0, 99.5, 212.0]

      # Filter out negative sensor readings
      readings = [12.5, -3.1, 8.0, -0.5, 15.2]
      valid = list(filter(lambda x: x >= 0, readings))
      print(valid)  # [12.5, 8.0, 15.2]

   **Lambda with Default Arguments**

   .. code-block:: python

      # Lambda with a default parameter
      compute_power = lambda base, exp=2: base**exp
      print(compute_power(3))  # 9
      print(compute_power(3, 3))  # 27


.. dropdown:: Limitations
   :open:

   **What Lambdas Cannot Do**

   Lambdas are restricted to a single expression. They cannot contain:

   - **Statements** -- No ``if``/``else`` blocks (but conditional *expressions* are allowed), no ``for``/``while`` loops, no ``try``/``except``.
   - **Assignments** -- No ``x = ...`` inside a lambda.
   - **Multiple expressions** -- Only one expression is evaluated and returned.
   - **Docstrings** -- Lambdas cannot have documentation strings.
   - **Type hints** -- Lambda parameters cannot be annotated.

   .. code-block:: python

      # Conditional expression in a lambda (valid)
      classify = lambda x: "positive" if x > 0 else "non-positive"
      print(classify(5))  # "positive"
      print(classify(-3))  # "non-positive"

      # Multi-line logic is NOT possible in a lambda
      # Use a regular function instead

   .. note::

      **Rule of Thumb**: If a lambda is hard to read on one line, use a ``def`` function instead.


Closures
====================================================

Functions that remember their enclosing scope.

Refer to ``closures_demo.py`` to follow along with the examples below.


.. dropdown:: What Is a Closure?
   :open:

   A **closure** is a function that retains access to variables from its enclosing scope, even after the enclosing function has finished executing. Three conditions must be met:

   - There must be a **nested function** (a function defined inside another function).
   - The nested function must **reference a variable** from the enclosing function's scope (a "free variable").
   - The enclosing function must **return** the nested function.

   .. code-block:: python

      def make_greeter(greeting):
          """Return a function that greets with the given greeting."""
          def greet(name):
              return f"{greeting}, {name}!"
          return greet

      hello = make_greeter("Hello")
      howdy = make_greeter("Howdy")

      print(hello("Alice"))  # Hello, Alice!
      print(howdy("Bob"))  # Howdy, Bob!


.. dropdown:: Practical Example: Logger Factory
   :open:

   **Configurable Logger**

   Closures are useful for creating pre-configured utility functions.

   .. code-block:: python

      def make_logger(prefix: str):
          """Return a logging function with a fixed prefix."""
          def log(message: str) -> None:
              print(f"[{prefix}] {message}")
          return log

      info = make_logger("INFO")
      error = make_logger("ERROR")
      debug = make_logger("DEBUG")

      info("System started")  # [INFO] System started
      error("Sensor timeout")  # [ERROR] Sensor timeout
      debug("x = 42")  # [DEBUG] x = 42


.. dropdown:: Stateful Closures
   :open:

   Closures can maintain mutable state across calls without using global variables or classes. Use ``nonlocal`` to modify the captured variable.

   .. code-block:: python

      def make_counter(start=0):
          """Return a counter function that increments on each call."""
          count = start

          def increment():
              nonlocal count
              count += 1
              return count
          return increment

      counter_a = make_counter()
      print(counter_a())  # 1
      print(counter_a())  # 2
      print(counter_a())  # 3

      counter_b = make_counter(10)
      print(counter_b())  # 11

   .. note::

      Each call to ``make_counter`` creates an independent closure with its own ``count`` variable. The two counters do not share state.


.. dropdown:: How Closures Capture State
   :open:

   Understanding the mechanism behind closures helps explain why they work even after the enclosing function returns.

   **Step 1: Python Inserts a Cell Object**

   During ``make_counter(start=0)``, Python sees that the inner function ``increment()`` references ``count`` from the enclosing scope. Instead of letting ``count`` point directly to the integer ``0``, Python inserts a **cell object** between them. This indirection exists so that both the enclosing scope and the inner function can share the same variable.

   **Step 2: ``make_counter`` Returns the Inner Function**

   When ``make_counter`` executes ``return increment``, Python attaches the cell object to the function's ``__closure__`` tuple. Now two references point to the same cell: the local variable ``count`` (from the still-active scope) and ``counter_a.__closure__``.

   **Step 3: Scope Is Discarded, Cell Survives**

   After ``make_counter`` returns, its local scope and the ``count`` variable are discarded. However, the cell object is **not** garbage collected because ``counter_a.__closure__`` still references it, and the ``int(0)`` stays alive because the cell's ``cell_contents`` still references it.

   **Step 4: Each Call Mutates the Cell**

   Each call to ``counter_a()`` follows the same steps: read ``cell_contents``, compute the increment, write the new value back, and return. The ``nonlocal count`` declaration tells Python to modify the cell's contents in place rather than creating a new local variable.


Decorators
====================================================

Wrapping functions to extend their behavior without modification.

Refer to ``decorators_demo.py`` to follow along with the examples below.


.. dropdown:: What Is a Decorator?
   :open:

   A **decorator** is a function that takes another function as input, adds some functionality, and returns a new function. Decorators allow you to extend or modify the behavior of functions without changing their source code.

   **The Manual Way (Without ``@`` Syntax)**

   .. code-block:: python

      def trace_calls(func):
          def wrapper():
              print("Before the function call")
              func()
              print("After the function call")
          return wrapper

      def say_hello():
          print("Hello!")

      # Manually applying the decorator
      say_hello = trace_calls(say_hello)
      say_hello()
      # Before the function call
      # Hello!
      # After the function call


.. dropdown:: The ``@`` Syntax
   :open:

   **Syntactic Sugar**

   The ``@decorator`` syntax is shorthand for applying a decorator. It is placed directly above the function definition.

   .. code-block:: python

      def trace_calls(func):
          def wrapper():
              print("Before the function call")
              func()
              print("After the function call")
          return wrapper

      @trace_calls
      def say_hello():
          print("Hello!")

      # This is equivalent to: say_hello = trace_calls(say_hello)
      say_hello()
      # Before the function call
      # Hello!
      # After the function call


.. dropdown:: Handling Arguments
   :open:

   Our ``trace_calls`` from the previous section defines ``wrapper()`` with no parameters. What happens if we try to decorate a function that takes arguments?

   .. code-block:: python

      @trace_calls
      def greet(name):
          print(f"Hello, {name}!")

      greet("Alice")
      # TypeError: wrapper() takes 0 positional arguments but 1 was given

   .. warning::

      After decoration, ``greet`` is replaced by ``wrapper``. When we call ``greet("Alice")``, Python actually calls ``wrapper("Alice")``, but ``wrapper`` accepts no arguments. We need a more flexible approach.

   **Decorating Functions with Arguments**

   To make a decorator work with *any* function, the wrapper should accept ``*args`` and ``**kwargs``.

   .. code-block:: python

      def trace_calls(func):
          def wrapper(*args, **kwargs):
              print(f"Before calling {func.__name__}")
              result = func(*args, **kwargs)
              print(f"After calling {func.__name__}")
              return result
          return wrapper

      @trace_calls
      def greet(name):
          print(f"Hello, {name}!")

      @trace_calls
      def say_hello():
          print("Hello!")

      greet("Alice")
      say_hello()


.. dropdown:: Preserving Metadata
   :open:

   **The Problem: Metadata Is Lost**

   When you wrap a function with a decorator, the wrapper replaces the original function. This means the original function's name, docstring, and other metadata are lost.

   .. code-block:: python

      import time

      def measure_time(func):
          """Measure and print the execution time of a function."""
          def wrapper(*args, **kwargs):
              start = time.perf_counter()
              result = func(*args, **kwargs)
              elapsed = time.perf_counter() - start
              print(f"{func.__name__} took {elapsed:.4f}s")
              return result
          return wrapper

      @measure_time
      def compute_sum(n: int) -> int:
          """Compute sum of range(n)."""
          return sum(range(n))

      print(compute_sum.__name__)  # 'wrapper'  (not 'compute_sum'!)
      print(compute_sum.__doc__)   # None       (docstring is lost!)

   **The Fix: ``functools.wraps``**

   ``functools.wraps`` is itself a decorator that you apply to your wrapper function. It copies the original function's ``__name__``, ``__doc__``, ``__module__``, and other attributes onto the wrapper so that introspection tools see the original function's identity.

   .. code-block:: python

      from functools import wraps
      import time

      def measure_time(func):
          @wraps(func)  # Copies metadata from func to wrapper
          def wrapper(*args, **kwargs):
              start = time.perf_counter()
              result = func(*args, **kwargs)
              elapsed = time.perf_counter() - start
              print(f"{func.__name__} took {elapsed:.4f}s")
              return result
          return wrapper

      @measure_time
      def compute_sum(n: int) -> int:
          """Compute sum of range(n)."""
          return sum(range(n))

      print(compute_sum.__name__)  # 'compute_sum'
      print(compute_sum.__doc__)   # 'Compute sum of range(n).'

   .. warning::

      Always use ``@functools.wraps(func)`` in your wrapper functions. Without it, debugging tools, documentation generators, and introspection code will show the wrong function name and docstring.


.. dropdown:: Stacking Decorators
   :open:

   **Applying Multiple Decorators**

   Multiple decorators can be applied to a single function. They are applied from **bottom to top** (innermost first).

   .. code-block:: python

      def apply_bold(func):
          @wraps(func)
          def wrapper(*args, **kwargs):
              return f"<b>{func(*args, **kwargs)}</b>"
          return wrapper

      def apply_italic(func):
          @wraps(func)
          def wrapper(*args, **kwargs):
              return f"<i>{func(*args, **kwargs)}</i>"
          return wrapper

      # @apply_bold @apply_italic def greet <=> greet = apply_bold(apply_italic(greet))
      @apply_bold      # executed second
      @apply_italic    # executed first
      def greet(name):
          return f"Hello, {name}"

      print(greet("Alice"))  # <b><i>Hello, Alice</i></b>


.. dropdown:: Decorators with Arguments
   :open:

   **Parameterized Decorators**

   Sometimes you want to pass arguments to a decorator itself. This requires an extra layer of nesting: a decorator factory that returns the actual decorator.

   .. code-block:: python

      def repeat(n: int):
          """Decorator factory: repeat the function call n times."""
          def decorator(func):
              @wraps(func)
              def wrapper(*args, **kwargs):
                  result = None
                  for _ in range(n):
                      result = func(*args, **kwargs)
                  return result
              return wrapper
          return decorator

      @repeat(3)
      def say_hello():
          print("Hello!")

      say_hello()
      # Hello!
      # Hello!
      # Hello!

   **Understanding the Three Layers**

   - ``repeat(n)`` -- The decorator factory. Called with the argument ``n`` and returns the actual decorator.
   - ``decorator(func)`` -- The actual decorator. Takes the function to be decorated and returns the wrapper.
   - ``wrapper(*args, **kwargs)`` -- The wrapper function. Replaces the original function and adds the repeated-call behavior.

   .. code-block:: python

      # @repeat(3) is processed in two steps:
      # Step 1: repeat(3) is called, returning 'decorator'
      # Step 2: decorator(say_hello) is called, returning 'wrapper'
      # So: say_hello = repeat(3)(say_hello)

   .. note::

      **Pattern**: Whenever you need a decorator that accepts arguments, use three nested functions: ``factory(args) -> decorator(func) -> wrapper(*args, **kwargs)``.


Partial Functions
====================================================

Pre-filling function arguments for convenience and reuse.

Refer to ``partial_demo.py`` to follow along with the examples below.


.. dropdown:: What Is ``functools.partial``?
   :open:

   ``functools.partial`` creates a new function with some arguments of the original function **pre-filled** ("frozen"). The new function takes fewer arguments.

   .. note::

      **Syntax**: ``partial(func, *args, **kwargs)``

   .. code-block:: python

      from functools import partial

      def compute_power(base, exponent):
          return base ** exponent

      # Create specialized functions by freezing one argument
      square = partial(compute_power, exponent=2)
      cube = partial(compute_power, exponent=3)

      print(square(5))  # 25
      print(cube(5))    # 125

   .. note::

      **Key Insight**: ``partial`` does not call the function. It returns a new callable with some arguments already set. You supply the remaining arguments when you call the partial.


.. dropdown:: Inspecting Partial Objects
   :open:

   .. code-block:: python

      def compute_power(base, exponent):
          return base ** exponent

      # Freezing a keyword argument
      square = partial(compute_power, exponent=2)
      print(square.func)      # <function compute_power at 0x...>
      print(square.args)      # ()
      print(square.keywords)  # {'exponent': 2}
      print(square(10))       # 100

      # Freezing a positional argument (fills left to right)
      power_of_ten = partial(compute_power, 10)
      print(power_of_ten.func)      # <function compute_power at 0x...>
      print(power_of_ten.args)      # (10,)
      print(power_of_ten.keywords)  # {}
      print(power_of_ten(3))        # 1000  (10 ** 3)

   Partial objects expose three useful attributes:

   - ``.func`` -- The original function.
   - ``.args`` -- Positional arguments that were frozen (filled left to right).
   - ``.keywords`` -- Keyword arguments that were frozen.


.. dropdown:: Practical Example: Unit Conversion
   :open:

   **Robotics Application: Unit Conversion**

   .. code-block:: python

      def convert_distance(value, from_unit, to_unit):
          """Convert between distance units."""
          # Lookup table: how many meters one unit equals
          to_meters = {"m": 1.0, "cm": 0.01, "ft": 0.3048, "in": 0.0254}
          # Step 1: Convert the input value to meters (common denominator)
          meters = value * to_meters[from_unit]
          # Step 2: Convert from meters to the target unit
          return meters / to_meters[to_unit]

      # Create specialized converters by freezing from_unit and to_unit
      ft_to_m = partial(convert_distance, from_unit="ft", to_unit="m")
      cm_to_in = partial(convert_distance, from_unit="cm", to_unit="in")

      # Only 'value' remains as an argument
      print(f"{ft_to_m(10):.2f} m")    # 3.05 m
      print(f"{cm_to_in(100):.2f} in")  # 39.37 in


.. dropdown:: Partial vs. Lambda vs. Closure
   :open:

   **Three Ways to Pre-Fill Arguments**

   .. code-block:: python

      def compute_power(base, exponent):
          return base ** exponent

      # Using partial
      square_partial = partial(compute_power, exponent=2)

      # Using lambda
      square_lambda = lambda base: compute_power(base, exponent=2)

      # Using closure
      def make_power_func(exp):
          def compute_value(base):
              return compute_power(base, exp)
          return compute_value
      square_closure = make_power_func(2)

      # All produce the same result
      print(square_partial(5), square_lambda(5), square_closure(5))
      # 25 25 25

   .. note::

      **When to use which?** ``partial`` is best for simple argument freezing and works well with introspection tools. Lambda is good for very short inline use. Closures offer the most flexibility for complex logic.


Putting It All Together
====================================================

This section combines the concepts from the entire lecture into a comprehensive exercise.


Summary
--------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card::
        :class-card: sd-border-primary

        - **Paradigms** -- Imperative, OOP, and functional styles; Python is multi-paradigm
        - **First-Class Functions** -- Assign, pass, return, and store functions like any object
        - **Lambdas** -- Anonymous single-expression functions for inline use
        - **Closures** -- Functions that capture and retain enclosing scope variables

    .. grid-item-card::
        :class-card: sd-border-primary

        - **Callables** -- The ``__call__`` method makes instances callable
        - **Decorators** -- Wrap functions to add behavior; use ``@wraps`` to preserve metadata
        - **Stacking/Parameterized** -- Multiple decorators; three-layer pattern for arguments
        - **Partials** -- ``functools.partial`` freezes arguments for reuse

.. list-table:: Concepts at a Glance
   :widths: 25 30 30
   :header-rows: 1
   :class: compact-table

   * - Concept
     - Mechanism
     - Use Case
   * - First-class function
     - ``f = do_nothing``
     - Callbacks, dispatch tables
   * - Lambda
     - ``lambda x: x + 1``
     - Short inline sort keys
   * - Closure
     - Nested function + free variable
     - Stateful factories
   * - Callable class
     - ``__call__`` method
     - Complex stateful behavior
   * - Decorator
     - ``@decorator`` syntax
     - Logging, timing, validation
   * - Partial
     - ``functools.partial``
     - Argument freezing

.. note::

   **Reminder**: Review and experiment with all provided code before next class.


Preview: What's Next in L6
---------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: L6: Object-Oriented Programming I
        :class-card: sd-border-primary

        - Classes and objects
        - Attributes and methods
        - Constructors and ``__init__``
        - Encapsulation and properties
        - Dunder methods

.. note::

   Today's lecture gives you the advanced function concepts that are essential for understanding object-oriented programming, decorators in frameworks, and functional patterns used throughout Python.
