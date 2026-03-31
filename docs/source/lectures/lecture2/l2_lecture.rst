====================================================
Lecture
====================================================



Packages and Modules
====================================================

Organizing Python code into reusable units.

Create a file called ``packages_demo.py`` to follow along with the examples below.


.. dropdown:: What Are They?
   :open:

   Modular programming breaks a large task into smaller, manageable subtasks called **modules**.

   .. grid:: 1 2 2 2
       :gutter: 3

       .. grid-item-card:: 📄 Module
           :class-card: sd-border-info

           - A single ``.py`` file.
           - Contains functions, classes, and variables.
           - Example: ``math_utils.py``

       .. grid-item-card:: 📁 Package
           :class-card: sd-border-info

           - A folder containing ``.py`` files.
           - Must include ``__init__.py`` (can be empty).
           - Example: ``shape/``

   .. note::

      Since Python 3.3, ``__init__.py`` is technically optional (namespace packages), but it is **required** for regular packages and should always be included.

   .. note::

      Python has a large collection of `standard modules <https://docs.python.org/3/py-modindex.html>`_. Standard and user-defined modules are imported the same way.


.. dropdown:: Making Packages Discoverable — Adding to ``sys.path``
   :open:

   Python can only import packages that are on its **module search path** (``sys.path``). If your script and package live in **sibling directories** (e.g., ``lecture2/`` and ``shape/``), Python may not find the package by default.

   .. code-block:: python

      import sys
      import os

      # Add the parent directory to sys.path
      sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

   - ``__file__`` — path to the current script.
   - ``os.path.abspath()`` — resolves to a full absolute path.
   - ``os.path.dirname()`` — goes up one directory level.
   - ``sys.path.insert(0, ...)`` — adds the path to the front of the search list.

   .. tip::

      Place this at the **very top** of your script, before any other imports that depend on the path.


.. dropdown:: Import Strategies
   :open:

   There are four common ways to import names from a module.

   **Approach 1 — Full module path:**

   .. code-block:: python

      import shape.square
      result = shape.square.compute_area(4)

   **Approach 2 — Alias:**

   .. code-block:: python

      import shape.square as sq
      result = sq.compute_area(4)

   **Approach 3 — Import specific names (recommended):**

   .. code-block:: python

      from shape.square import compute_area, compute_perimeter
      result = compute_area(4)

   **Approach 4 — Wildcard (avoid):**

   .. code-block:: python

      from shape.square import *  # Namespace pollution risk!


.. dropdown:: Why Avoid Wildcard Imports?
   :open:

   ``import *`` dumps **every** name from a module into your current namespace, which can silently overwrite existing variables or functions.

   .. code-block:: python

      from shape.square import *    # brings in compute_area, compute_perimeter
      from shape.circle import *    # also brings in compute_area, compute_perimeter

      result = compute_area(4)      # Which version is this? circle!

   - ``compute_area`` from ``square`` is **silently overwritten** by ``circle``'s version.
   - No error, no warning — your code just computes the wrong thing.
   - Readers cannot tell which module a function came from.

   .. tip::

      **Best practice**: Use explicit named imports so it is always clear where each name originated.

      .. code-block:: python

         from shape.square import compute_area as square_area
         from shape.circle import compute_area as circle_area


.. dropdown:: Importing Packages from Anywhere
   :open:

   So far we have seen how to import **sibling packages** using ``sys.path.insert()``. But what if the package is located **somewhere else** on the system?

   Python provides several methods to make packages discoverable. In all cases, the path you add should be the **parent directory** of the package, not the package directory itself.

   .. list-table::
      :widths: 40 30
      :header-rows: 1
      :class: compact-table

      * - Package location
        - Path to add
      * - ``/opt/libs/my_utils/``
        - ``/opt/libs``
      * - ``/home/alice/projects/common/shared_tools/``
        - ``/home/alice/projects/common``


.. dropdown:: Method 1 — ``PYTHONPATH`` Environment Variable
   :open:

   Set the ``PYTHONPATH`` environment variable in your shell **before** running the script. Python adds every directory in ``PYTHONPATH`` to ``sys.path`` automatically at startup.

   .. code-block:: console

      # Add one directory (append to existing PYTHONPATH)
      export PYTHONPATH="/opt/libs:$PYTHONPATH"
      python3 my_script.py

      # Add multiple directories
      export PYTHONPATH="/opt/libs:/home/alice/projects/common:$PYTHONPATH"
      python3 my_script.py

   Now your script can import directly with no code changes:

   .. code-block:: python

      import my_utils            # Found in /opt/libs/
      import shared_tools        # Found in /home/alice/projects/common/

   .. warning::

      ``PYTHONPATH`` is session-specific — it resets when you close the terminal. Add it to your ``~/.bashrc`` to make it permanent.


.. dropdown:: Method 2 — ``.pth`` Files
   :open:

   Drop a ``.pth`` file into Python's ``site-packages`` directory. Each line is a path that gets added to ``sys.path`` automatically at startup.

   First, find your ``site-packages`` directory:

   .. code-block:: console

      python3 -c "import site; print(site.getsitepackages())"

   Then create a ``.pth`` file in that directory:

   .. code-block:: text

      # /usr/lib/python3.12/site-packages/enpm605.pth
      /opt/libs
      /home/alice/projects/common

   Now every Python script on the system can import from those paths:

   .. code-block:: python

      import my_utils        # Found in /opt/libs/
      import shared_tools    # Found in /home/alice/projects/common/

   .. tip::

      This is a system-wide change. Use this for packages you want available to **all** your projects.


.. dropdown:: Method 3 — Editable Install (``pip3 install``)
   :open:

   The most robust approach. Add a ``pyproject.toml`` to your package and install it in **editable mode**.

   .. code-block:: toml
      :caption: shape/pyproject.toml

      [build-system]
      requires = ["setuptools"]
      build-backend = "setuptools.build_meta"

      [project]
      name = "shape2"
      version = "0.1.0"
      description = "Simple shape geometry utilities for ENPM605"
      requires-python = ">=3.10"

   Then install it:

   .. code-block:: console

      cd <path to shape>
      pip3 install -e . --break-system-packages

   - Works from **anywhere** — no path manipulation needed.
   - The ``-e`` flag means changes take effect **immediately** without reinstalling.
   - This is how real Python projects manage dependencies.

   .. tip::

      **Recommended**: This is the most portable and professional approach.


.. dropdown:: Summary of Discovery Approaches
   :open:

   .. list-table::
      :widths: 25 20 30
      :header-rows: 1
      :class: compact-table

      * - Method
        - Scope
        - Best for
      * - ``sys.path.insert()``
        - Single script
        - Quick fixes, sibling packages
      * - ``PYTHONPATH``
        - Terminal session
        - Development and testing
      * - ``.pth`` files
        - System-wide
        - Shared libraries across projects
      * - ``pip3 install``
        - System-wide
        - Reusable packages (recommended)

   .. note::

      For this course, we will primarily use ``sys.path.insert()`` and ``pip3 install``


.. dropdown:: The ``__name__`` Guard
   :open:

   When a module is run directly, its ``__name__`` is set to ``"__main__"``. When imported, ``__name__`` is set to the module's name.

   .. code-block:: python

      from shape.triangle import compute_area

      print(compute_area(3, 2))

   .. note::

      This pattern allows a module to serve both as an importable library and as a standalone script.


Indentation
====================================================

Unlike C++ or Java which use braces ``{}``, Python uses **indentation** to define blocks of code.

Create a file called ``indentation_demo.py`` to follow along.


.. dropdown:: Python's Block Structure
   :open:

   .. tab-set::

       .. tab-item:: 🐍 Python

           .. code-block:: python

              def greeting(name):
                  print("Hello", name)
                  if name == "Alice":
                      print("Welcome back!")

       .. tab-item:: ⚙️ C++

           .. code-block:: cpp

              void greeting(std::string name) {
                  std::cout << "Hello " << name << '\n';
                  if (name == "Alice") {
                      std::cout << "Welcome back!\n";
                  }
              }

   .. warning::

      Mixing tabs and spaces causes ``IndentationError``. Configure your editor to use **4 spaces** per indent level (PEP 8 standard).


Boolean Type
====================================================

Truth values, truthiness, and the ``bool()`` function.

Create a file called ``boolean_demo.py`` to follow along with the examples below.


.. dropdown:: The ``bool`` Type
   :open:

   Python provides the Boolean type ``bool`` with exactly two values: ``True`` and ``False``.

   - ``bool`` is a subclass of ``int``: ``True`` is ``1`` and ``False`` is ``0``.
   - In a condition, any non-zero value or non-empty sequence evaluates to ``True``.
   - The built-in ``bool()`` function converts a value to a Boolean.

   .. grid:: 1 2 2 2
       :gutter: 3

       .. grid-item-card:: ❌ Falsy Values
           :class-card: sd-border-danger

           .. code-block:: python

              print(bool(0))       # False
              print(bool(0.0))     # False
              print(bool(""))      # False
              print(bool([]))      # False
              print(bool({}))      # False
              print(bool(None))    # False

       .. grid-item-card:: ✅ Truthy Values
           :class-card: sd-border-success

           .. code-block:: python

              print(bool(1))       # True
              print(bool(-2))      # True
              print(bool("hi"))    # True
              print(bool([1, 2]))  # True
              print(bool(" "))     # True (space!)
              print(bool(0.001))   # True

   .. tip::

      **Pythonic idiom**: Use truthiness directly in conditions — write ``if my_list:`` instead of ``if len(my_list) > 0:``.


Operators
====================================================

Arithmetic, relational, logical, membership, and identity operators.

Create a file called ``operators_demo.py`` to follow along with the examples below.


.. dropdown:: Arithmetic Operators
   :open:

   .. list-table::
      :widths: 12 20 20 15
      :header-rows: 1
      :class: compact-table

      * - Operator
        - Operation
        - Example
        - Result
      * - ``+``
        - Addition
        - ``7 + 3``
        - ``10``
      * - ``-``
        - Subtraction
        - ``7 - 3``
        - ``4``
      * - ``*``
        - Multiplication
        - ``7 * 3``
        - ``21``
      * - ``/``
        - Division (float)
        - ``7 / 3``
        - ``2.333...``
      * - ``//``
        - Floor division
        - ``7 // 3``
        - ``2``
      * - ``%``
        - Modulus (remainder)
        - ``7 % 3``
        - ``1``
      * - ``**``
        - Exponentiation
        - ``2 ** 10``
        - ``1024``

   .. code-block:: python

      # Floor division always rounds toward negative infinity
      print(10 // 3)    # 3
      print(10 // -3)   # -4 (not -3!)

      # Augmented assignment operators
      x = 10
      x += 5   # x = x + 5 -> 15
      x *= 2   # x = x * 2 -> 30


.. dropdown:: Relational Operators
   :open:

   Relational operators compare **values** and return ``True`` or ``False``.

   Let ``a = 5`` and ``b = 3``:

   .. list-table::
      :widths: 12 25 25
      :header-rows: 1
      :class: compact-table

      * - Operator
        - Description
        - Example
      * - ``==``
        - Equal
        - ``a == b`` is ``False``
      * - ``!=``
        - Not equal
        - ``a != b`` is ``True``
      * - ``>``
        - Greater than
        - ``a > b`` is ``True``
      * - ``<``
        - Less than
        - ``a < b`` is ``False``
      * - ``>=``
        - Greater than or equal
        - ``a >= 5`` is ``True``
      * - ``<=``
        - Less than or equal
        - ``a <= b`` is ``False``

   .. code-block:: python

      # Python supports chained comparisons
      x = 5
      print(1 < x < 10)   # True (equivalent to 1 < x and x < 10)
      print(1 < x > 3)    # True


.. dropdown:: Logical Operators
   :open:

   Logical operators combine Boolean expressions.

   Let ``a = True`` and ``b = False``:

   .. list-table::
      :widths: 12 40 25
      :header-rows: 1
      :class: compact-table

      * - Operator
        - Description
        - Example
      * - ``and``
        - ``True`` if both operands are ``True``
        - ``a and b`` is ``False``
      * - ``or``
        - ``True`` if at least one is ``True``
        - ``a or b`` is ``True``
      * - ``not``
        - Reverses the logical state
        - ``not a`` is ``False``

   .. code-block:: python

      # Short-circuit evaluation
      x = 5
      print(x > 0 and x < 10)    # True
      print(x > 10 or x == 5)    # True
      print(not (x == 5))        # False


.. dropdown:: Logical Operators with Non-Boolean Values
   :open:

   Python's ``and`` and ``or`` don't always return ``True`` or ``False`` — they return **one of the actual operands**.

   - ``and`` — Returns the **first falsy** value. If all truthy, returns the **last** value.
   - ``or`` — Returns the **first truthy** value. If all falsy, returns the **last** value.
   - ``not`` — Always returns a ``bool``.

   .. code-block:: python

      # and: returns first falsy, or last value if all truthy
      print("hello" and 0)          # 0 ("hello" is truthy, so check 0 -> falsy)
      print("hello" and "world")    # "world" (both truthy, return last)

      # or: returns first truthy, or last value if all falsy
      print("hello" or 0)           # "hello" (truthy, stop immediately)
      print(0 or "default")         # "default" (0 is falsy, check next)

      # not: always returns a bool
      print(not "")                  # True (empty string is falsy)
      print(not "hello")             # False (non-empty string is truthy)

   .. tip::

      **Common pattern**: Use ``or`` to provide default values. Example: ``name = user_input or "Anonymous"`` assigns ``"Anonymous"`` when ``user_input`` is empty or falsy.


.. dropdown:: Membership and Identity Operators
   :open:

   .. grid:: 1 2 2 2
       :gutter: 3

       .. grid-item-card:: 🔍 Membership Operators
           :class-card: sd-border-info

           Test if an element belongs in a sequence.

           .. list-table::
              :widths: 15 40
              :header-rows: 1
              :class: compact-table

              * - Operator
                - Description
              * - ``in``
                - ``True`` if found
              * - ``not in``
                - ``True`` if not found

           .. code-block:: python

              x = "hello"
              print("h" in x)      # True
              print("he" in x)     # True
              print("O" in x)      # False
              print("z" not in x)  # True

       .. grid-item-card:: 🆔 Identity Operators
           :class-card: sd-border-info

           Compare memory locations of objects.

           .. list-table::
              :widths: 15 40
              :header-rows: 1
              :class: compact-table

              * - Operator
                - Description
              * - ``is``
                - Same object (same ``id``)
              * - ``is not``
                - Different objects

           .. code-block:: python

              a = [1, 2, 3]
              b = [1, 2, 3]
              c = a

              print(a == b)   # True (same values)
              print(a is b)   # False (different objects)
              print(a is c)   # True (same object)

   .. important::

      **Rule**: Use ``==`` for value comparison. Use ``is`` only for ``None`` checks.


.. dropdown:: Exercise 1: Operators (5 min)
   :open:

   Predict the output of each expression **before** running the code.

   .. code-block:: python

      # Arithmetic
      print(17 // 5)
      print(17 % 5)
      print(2 ** 0.5)
      print(-7 // 2)

      # Logical with non-boolean values
      print(0 or "default")
      print("hello" and "world")
      print(not [])

      # Chained comparison
      x = 15
      print(10 < x < 20)
      print(10 < x > 20)


Numeric Types
====================================================

Integers, floats, precision pitfalls, and interning.

Create a file called ``numeric_types_demo.py`` to follow along with the examples below.


.. dropdown:: Integers and Floats
   :open:

   .. list-table::
      :widths: 12 10 30 20
      :header-rows: 1
      :class: compact-table

      * - Name
        - Type
        - Description
        - Examples
      * - Integer
        - ``int``
        - Whole numbers (unlimited precision)
        - ``1``, ``-42``, ``2000``
      * - Float
        - ``float``
        - Decimal numbers (64-bit IEEE 754)
        - ``2.5``, ``-0.001``, ``1e10``
      * - Complex
        - ``complex``
        - Complex numbers
        - ``1+2j``, ``3+8j``

   .. grid:: 1 2 2 2
       :gutter: 3

       .. grid-item-card:: 🔢 Integer Type
           :class-card: sd-border-info

           .. code-block:: python

              # Python ints have unlimited precision
              big = 10 ** 100
              print(type(big))  # <class 'int'>

              # Convert to int
              print(int(3.7))          # 3 (truncates)
              print(int("42"))         # 42
              print(int("101011", 2))  # 43 (binary)

       .. grid-item-card:: 🔢 Float Type
           :class-card: sd-border-info

           .. code-block:: python

              # Float precision limits
              print(0.1 + 0.2)         # 0.30000000000000004
              print(0.1 + 0.2 == 0.3)  # False!

              # Convert to float
              print(float("3.5"))   # 3.5
              print(float(3))       # 3.0
              print(float("inf"))   # inf

   .. warning::

      Never compare floats with ``==``. Use ``math.isclose(a, b)`` or check ``abs(a - b) < epsilon`` instead.


.. dropdown:: Integer and String Interning
   :open:

   CPython caches ("interns") small integers and compile-time string constants to save memory and speed up comparisons.

   .. grid:: 1 2 2 2
       :gutter: 3

       .. grid-item-card:: 🔢 Integer Interning
           :class-card: sd-border-secondary

           .. code-block:: python

              a, b = 20, 20
              print(a is b)   # True (cached)

              a, b = -5, -5
              print(a is b)   # True (cached)

              # Large ints in the same statement
              a, b = 200000000000, 200000000000
              print(a is b)   # True (compile-time)

       .. grid-item-card:: 🔤 String Interning
           :class-card: sd-border-secondary

           .. code-block:: python

              a = "hello"
              b = "hello"
              c = "h" + "ello"   # Compile-time
              d = "".join(["h","e","l","l","o"])

              print(a is b)  # True
              print(a is c)  # True (folded at compile)
              print(a is d)  # False (runtime-built)

              import sys
              e = sys.intern(d)
              print(a is e)  # True (manually interned)

   .. warning::

      Never rely on interning for correctness. Always use ``==`` for value comparison. Use ``is`` only for ``None`` checks.


String Type
====================================================

Strings, escape sequences, formatting, methods, indexing, and slicing.

Create a file called ``strings_demo.py`` to follow along with the examples below.


.. dropdown:: String Basics
   :open:

   A Python string (``str``) is an **immutable** sequence of characters.

   .. code-block:: python

      # Single and double quotes are equivalent
      greeting = "Hello, World!"
      greeting2 = 'Hello, World!'

      # Triple quotes for multi-line strings
      description = """This is a
      multi-line string."""

      # String conversion
      number = 123
      number_str = str(number)
      print(type(number_str))  # <class 'str'>

   **Escape Sequences:**

   .. code-block:: python

      print("Line 1\nLine 2")          # Newline
      print("Col1\tCol2\tCol3")        # Tab
      print("She said: \"Hi!\"")       # Escaped quotes
      print('It\'s Python!')           # Escaped apostrophe
      print(r"C:\Users\tony\notes")    # Raw string (no escapes)


.. dropdown:: String Interpolation
   :open:

   There are three ways to format strings in Python.

   **Old-style (``%`` operator) — Legacy, avoid in new code:**

   .. code-block:: python

      name, age = "Alice", 25
      print("Name: %s, Age: %d" % (name, age))

   **str.format() — More flexible:**

   .. code-block:: python

      print("Name: {}, Age: {}".format(name, age))
      print("Name: {name}, Age: {age}".format(name="Alice", age=25))

   **f-strings (Python 3.6+) — Recommended:**

   .. code-block:: python

      print(f"Name: {name}, Age: {age}")
      print(f"Next year: {age + 1}")
      print(F"Pi: {3.14159:.2f}")      # Format specifier: 3.14. Note: uppercase F works as well
      print(f"{'hello':>20}")           # Right-align in 20 chars

   .. tip::

      **Use f-strings** for all new code. They are faster, more readable, and support inline expressions.


.. dropdown:: String Concatenation and Methods
   :open:

   .. grid:: 1 2 2 2
       :gutter: 3

       .. grid-item-card:: 🔗 Concatenation
           :class-card: sd-border-info

           .. code-block:: python

              # + operator
              first = "John"
              last = "Doe"
              full = first + " " + last

              # join() method (efficient)
              words = ["Hello", "World"]
              sentence = " ".join(words)
              print(sentence)  # Hello World

              # Repetition
              print("=" * 40)

       .. grid-item-card:: 🛠️ Common Methods
           :class-card: sd-border-info

           .. code-block:: python

              s = "Hello, World!"

              print(s.upper())       # HELLO, WORLD!
              print(s.lower())       # hello, world!
              print(s.capitalize())  # Hello, world!
              print(s.swapcase())    # hELLO, wORLD!
              print(s.strip())       # Remove whitespace
              print(s.replace("World", "Python"))
              print(s.split(", "))   # ['Hello', 'World!']
              print(s.find("World")) # 7
              print(s.count("l"))    # 3
              print(s.startswith("Hello"))  # True

   .. note::

      String methods return **new strings** — they never modify the original (strings are immutable).


.. dropdown:: Indexing
   :open:

   Strings are ordered sequences, so each character has a positional index.

   .. list-table::
      :widths: 15 10 10 10 10 10
      :header-rows: 0
      :class: compact-table

      * - **String**
        - ``'h'``
        - ``'e'``
        - ``'l'``
        - ``'l'``
        - ``'o'``
      * - **+ Index**
        - 0
        - 1
        - 2
        - 3
        - 4
      * - **− Index**
        - −5
        - −4
        - −3
        - −2
        - −1

   .. code-block:: python

      greeting = "hello"

      # Positive indexing
      print(greeting[0])    # 'h'
      print(greeting[4])    # 'o'

      # Negative indexing
      print(greeting[-1])   # 'o'
      print(greeting[-5])   # 'h'

      # Common errors
      # print(greeting[5])    # What is the output?
      # greeting[0] = 'H'    # What is the output?


.. dropdown:: Slicing
   :open:

   Slicing extracts a **substring** by specifying a range of indices using the syntax ``[start:stop:stride]``:

   - ``start``: Starting index (**inclusive**), defaults to 0.
   - ``stop``: Ending index (**exclusive**), defaults to end of string.
   - ``stride``: Step size, defaults to 1.

   .. code-block:: python

      greeting = "hello"  # 'h':0:-5, 'e':+1:-4, 'l':+2:-3, 'l':+3:-2, 'o':+4:-1

      # Basic slicing
      print(greeting[0:3])   # "hel"
      print(greeting[:3])    # "hel" (start defaults to 0)
      print(greeting[2:])    # "llo" (stop defaults to end)
      print(greeting[:])     # "hello" (entire string)

      # Negative indices
      print(greeting[-5:-2]) # "hel"
      print(greeting[-3:])   # "llo"

      # With stride
      print(greeting[::2])   # "hlo" (every 2nd character)
      print(greeting[::-1])  # "olleh" (reverse!)
      print(greeting[4:1:-1])# "oll"


.. dropdown:: Exercise 2: Strings (10 min)
   :open:

   **Part A**: Predict the outputs before running.

   .. code-block:: python

      text = "Learn Python, be happy!"
      print(text[6:12])
      print(text[-6:])
      print(text[::3])

   **Part B**: Using the variable ``quote = "Learn Python, be happy!"``

   - Task 1: Extract ``"Python"`` using only positive indices.
   - Task 2: Extract ``"Python"`` using only negative indices.
   - Task 3: Reverse ``"Python"`` to get ``"nohtyP"`` using slicing.
   - Task 4: Reverse the entire string.

   **Part C**: Print only the second half of a string.

   .. code-block:: python

      text = "HelloWorld"
      # second_half = ??
      # print(second_half)  # Expected: World


Control Flow
====================================================

Making decisions with ``if``, ``elif``, and ``else``.

Create a file called ``control_flow_demo.py`` to follow along with the examples below.


.. dropdown:: The ``if`` Statement
   :open:

   Selection determines which code block executes based on conditions.

   .. tab-set::

       .. tab-item:: Simple ``if``

           .. code-block:: python

              x = 10
              if x > 0:
                  print("x is positive")
              print("always runs")

       .. tab-item:: ``if``-``else``

           .. code-block:: python

              x = -3
              if x >= 0:
                  print("Non-negative")
              else:
                  print("Negative")

       .. tab-item:: ``if``-``elif``-``else``

           .. code-block:: python

              score = 85

              if score >= 90:
                  grade = "A"
              elif score >= 80:
                  grade = "B"
              elif score >= 70:
                  grade = "C"
              elif score >= 60:
                  grade = "D"
              else:
                  grade = "F"

              print(f"Grade: {grade}")  # Grade: B


.. dropdown:: Conditional Expressions
   :open:

   Python supports single-line conditional assignment (the ternary expression).

   .. code-block:: python

      age = 20
      status = "adult" if age >= 18 else "minor"
      print(status)  # "adult"

      # Equivalent to:
      if age >= 18:
          status = "adult"
      else:
          status = "minor"


.. dropdown:: Nested Conditions
   :open:

   .. code-block:: python

      temperature = 25
      humidity = 80

      if temperature > 30:
          if humidity > 70:
              print("Hot and humid")
          else:
              print("Hot and dry")
      elif temperature > 20:
          print("Pleasant")  # This runs
      else:
          print("Cool")


.. dropdown:: Exercise 3: Control Flow (10 min)
   :open:

   Write a program that determines if a year is a leap year.

   .. code-block:: python

      year = 2024

      # A year is a leap year if:
      # - Divisible by 4 AND not divisible by 100
      # - OR divisible by 400
      # Print "Leap year" or "Not a leap year"

   .. tip::

      Use ``%`` (modulus) to check divisibility. ``year % 4 == 0`` means divisible by 4.


Putting It All Together
====================================================


.. dropdown:: Exercise 4: Robot Status Monitor (15 min)
   :open:

   Write a program that monitors a robot's status using concepts from today's lecture.

   .. code-block:: python

      # Robot parameters
      robot_name = "Waffle_01"
      battery = 65
      speed = 0.8
      status_log = "IDLE:MOVING:CHARGING:MOVING:IDLE"

      # 1. Use an f-string to print: "Robot Waffle_01 | Battery: 65%"

      # 2. Classify battery level using if/elif/else:
      #    >= 80: "OK", 50-79: "LOW", 20-49: "WARNING", < 20: "CRITICAL"

      # 3. Use string methods to:
      #    a) Count how many times "MOVING" appears in status_log
      #    b) Split status_log by ":" into a list
      #    c) Check if the last status is "IDLE"

      # 4. Use slicing to extract the first status entry from status_log

      # 5. Create a formatted status message:
      #    "Waffle_01 | Battery: LOW | Speed: 0.80 m/s | States: 5"


Summary
--------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card::
        :class-card: sd-border-primary

        - **Packages & Modules** — Organize code; use ``from ... import ...`` (Approach 3)
        - **Indentation** — Defines code blocks; use 4 spaces
        - **Operators** — Arithmetic, relational, logical, membership, identity
        - **Boolean Type** — Truthiness, falsy values, ``bool()``

    .. grid-item-card::
        :class-card: sd-border-primary

        - **Numeric Types** — ``int`` (unlimited), ``float`` (IEEE 754), interning
        - **Strings** — Immutable sequences; f-strings, methods, indexing, slicing
        - **Control Flow** — ``if``/``elif``/``else``, ternary expressions

.. note::

   **Reminder**: Review and experiment with all provided code before next class.


Preview: What's Next in L3
---------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📖 L3: Python Fundamentals — Part II
        :class-card: sd-border-primary

        - Lists and list methods
        - Tuples and unpacking
        - Dictionaries
        - Sets
        - Loops (``for``, ``while``)
        - List comprehensions

.. note::

   Today's lecture gives you the foundational tools — operators, strings, and control flow — that you will use constantly from L3 onward.