====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 4: Function Fundamentals,
including function definition and calling, arguments (positional, default,
keyword, ``*args``, ``**kwargs``), scopes (LEGB), pass-by-assignment,
type hints, docstrings, and recursion.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def greet(name, greeting="Hello"):
          return f"{greeting}, {name}!"

      print(greet("Alice"))

   A. ``"Hello, Alice!"``

   B. ``"Alice, Hello!"``

   C. ``TypeError``

   D. ``"None, Alice!"``

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- ``"Hello, Alice!"``

   The ``greeting`` parameter has a default value of ``"Hello"``. Since only ``name`` is provided, the default is used.


.. admonition:: Question 2
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def add_item(item, items=[]):
          items.append(item)
          return items

      print(add_item("a"))
      print(add_item("b"))

   A. ``['a']`` then ``['b']``

   B. ``['a']`` then ``['a', 'b']``

   C. ``['a', 'b']`` then ``['a', 'b']``

   D. ``TypeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``['a']`` then ``['a', 'b']``

   This is the mutable default argument trap. The default list ``[]`` is created once when the function is defined and shared across all calls. Each call appends to the same list object.


.. admonition:: Question 3
   :class: hint

   What does the ``*args`` parameter collect?

   A. All keyword arguments as a dictionary.

   B. All positional arguments as a tuple.

   C. All arguments as a list.

   D. Only the first extra argument.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- All positional arguments as a tuple.

   ``*args`` collects any extra positional arguments into a tuple. Keyword arguments are collected by ``**kwargs`` into a dictionary.


.. admonition:: Question 4
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      x = 10

      def modify():
          x = 20
          print(x)

      modify()
      print(x)

   A. ``20`` then ``20``

   B. ``20`` then ``10``

   C. ``10`` then ``10``

   D. ``UnboundLocalError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``20`` then ``10``

   The ``x = 20`` inside ``modify()`` creates a local variable that shadows the global ``x``. The global ``x`` remains ``10``.


.. admonition:: Question 5
   :class: hint

   In the LEGB rule, what does the "E" stand for?

   A. External

   B. Enclosing

   C. Environment

   D. Evaluated

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Enclosing

   LEGB stands for Local, Enclosing, Global, Built-in. The enclosing scope refers to the scope of an outer function when using nested functions.


.. admonition:: Question 6
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def func(a: int, b: str) -> bool:
          return str(a) == b

      result = func(42, "42")
      print(result)

   A. ``True``

   B. ``False``

   C. ``TypeError``

   D. ``"42"``

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- ``True``

   Type hints are not enforced at runtime. ``str(42)`` returns ``"42"``, which equals the second argument ``"42"``, so the function returns ``True``.


.. admonition:: Question 7
   :class: hint

   What happens when you pass a list to a function and the function appends an element to it?

   A. The original list is unchanged because Python uses pass-by-value.

   B. The original list is modified because lists are mutable and passed by assignment.

   C. The original list is replaced with a new list.

   D. A ``TypeError`` is raised.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The original list is modified because lists are mutable and passed by assignment.

   Python passes a reference to the list object. Since lists are mutable, in-place operations like ``append()`` modify the original object.


.. admonition:: Question 8
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def outer():
          count = 0
          def inner():
              nonlocal count
              count += 1
              return count
          return inner()

      print(outer())

   A. ``0``

   B. ``1``

   C. ``NameError``

   D. ``None``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``1``

   ``nonlocal count`` allows ``inner()`` to modify ``count`` in the enclosing scope. It increments from 0 to 1, and ``outer()`` returns the result of ``inner()``.


.. admonition:: Question 9
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def combine(*args, **kwargs):
          return (args, kwargs)

      print(combine(1, 2, x=3, y=4))

   A. ``([1, 2], {'x': 3, 'y': 4})``

   B. ``((1, 2), {'x': 3, 'y': 4})``

   C. ``(1, 2, 3, 4)``

   D. ``TypeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``((1, 2), {'x': 3, 'y': 4})``

   ``*args`` collects positional arguments ``1, 2`` as a tuple, and ``**kwargs`` collects keyword arguments as a dictionary.


.. admonition:: Question 10
   :class: hint

   Which of the following is NOT true about Python type hints?

   A. They improve code readability and documentation.

   B. They are enforced at runtime by the Python interpreter.

   C. They enable static analysis tools like ``mypy``.

   D. They can specify ``Optional`` for values that may be ``None``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- They are enforced at runtime by the Python interpreter.

   Type hints are not enforced at runtime. They serve as documentation and enable static analysis tools like ``mypy``, but Python ignores them during execution.


.. admonition:: Question 11
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def factorial(n):
          if n <= 1:
              return 1
          return n * factorial(n - 1)

      print(factorial(5))

   A. ``5``

   B. ``15``

   C. ``120``

   D. ``RecursionError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``120``

   ``factorial(5) = 5 * 4 * 3 * 2 * 1 = 120``. Each recursive call reduces ``n`` by 1 until the base case ``n <= 1`` returns 1.


.. admonition:: Question 12
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def modify(data):
          data = [99, 99, 99]

      original = [1, 2, 3]
      modify(original)
      print(original)

   A. ``[99, 99, 99]``

   B. ``[1, 2, 3]``

   C. ``[]``

   D. ``None``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``[1, 2, 3]``

   Reassigning ``data = [99, 99, 99]`` inside the function creates a new local binding. The original list referenced by ``original`` is not affected because reassignment does not mutate the object.


.. admonition:: Question 13
   :class: hint

   What does a function return if it has no ``return`` statement?

   A. ``0``

   B. An empty string ``""``

   C. ``None``

   D. It raises an error.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``None``

   Functions without an explicit ``return`` statement (or with a bare ``return``) implicitly return ``None``.


.. admonition:: Question 14
   :class: hint

   Which correctly unpacks a function's return value?

   .. code-block:: python

      def get_coords():
          return 3.5, 7.2

   A. ``x, y = get_coords()``

   B. ``(x, y) = get_coords()``

   C. Both A and B are correct.

   D. Neither A nor B is correct.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Both A and B are correct.

   Python supports tuple unpacking with or without parentheses. ``get_coords()`` returns a tuple, and both syntaxes correctly unpack the two values.


.. admonition:: Question 15
   :class: hint

   What is the correct order of parameters in a function signature?

   A. ``def func(*args, a, b, **kwargs):``

   B. ``def func(a, b, *args, **kwargs):``

   C. ``def func(**kwargs, a, b, *args):``

   D. ``def func(a, **kwargs, b, *args):``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``def func(a, b, *args, **kwargs):``

   The correct order is: positional parameters, then ``*args`` for extra positional arguments, then ``**kwargs`` for extra keyword arguments.


----


True or False
=============

.. admonition:: Question 16
   :class: hint

   **True or False:** In Python, a function can return multiple values as a tuple.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Python functions can return multiple values separated by commas, which are automatically packed into a tuple. The caller can unpack them using tuple unpacking.


.. admonition:: Question 17
   :class: hint

   **True or False:** Default argument values are evaluated once when the function is defined, not each time it is called.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Default values are evaluated once at function definition time. This is why mutable defaults (like lists or dictionaries) can cause unexpected behavior across multiple calls.


.. admonition:: Question 18
   :class: hint

   **True or False:** The ``global`` keyword allows a function to create a new global variable that did not exist before.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The ``global`` keyword can both modify an existing global variable and create a new one if it does not already exist in the module scope.


.. admonition:: Question 19
   :class: hint

   **True or False:** ``**kwargs`` collects extra keyword arguments into a list.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``**kwargs`` collects extra keyword arguments into a **dictionary**, not a list. Each keyword becomes a key, and its argument becomes the corresponding value.


.. admonition:: Question 20
   :class: hint

   **True or False:** A recursive function without a base case will run forever without error.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Python has a maximum recursion depth (default 1000). A recursive function without a base case will hit this limit and raise a ``RecursionError``, not run forever.


.. admonition:: Question 21
   :class: hint

   **True or False:** Type hints in Python are enforced at runtime by the interpreter.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Type hints are not enforced at runtime. They are metadata used by developers, IDEs, and static analysis tools like ``mypy`` for type checking.


.. admonition:: Question 22
   :class: hint

   **True or False:** In the LEGB rule, Python checks the local scope before the global scope.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The LEGB order is Local, Enclosing, Global, Built-in. Python checks the local scope first, so a local variable will shadow a global variable with the same name.


.. admonition:: Question 23
   :class: hint

   **True or False:** Reassigning a parameter inside a function always modifies the original variable outside the function.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Reassigning a parameter inside a function creates a new local binding and does not affect the original variable. Only in-place mutations on mutable objects affect the original.


.. admonition:: Question 24
   :class: hint

   **True or False:** A Google-style docstring should include a description, an ``Args`` section, and a ``Returns`` section.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A Google-style docstring includes a one-line description of the function, an ``Args`` section listing each parameter and its type/description, and a ``Returns`` section describing the return value.


.. admonition:: Question 25
   :class: hint

   **True or False:** The ``nonlocal`` keyword is used to modify a variable in the enclosing function's scope.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The ``nonlocal`` keyword allows a nested (inner) function to modify a variable defined in the enclosing (outer) function's scope, rather than creating a new local variable.


----


Essay Questions
===============

.. admonition:: Question 26
   :class: hint

   **Explain the LEGB rule in Python.** Describe what each letter stands for and the order in which Python searches for a variable name.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - LEGB stands for Local, Enclosing, Global, Built-in.
   - Local: variables defined inside the current function.
   - Enclosing: variables in the scope of outer functions (for nested functions).
   - Global: variables defined at the module level.
   - Built-in: names in Python's ``builtins`` module (e.g., ``print``, ``len``, ``int``).
   - Python searches in this exact order and uses the first match found.


.. admonition:: Question 27
   :class: hint

   **Explain the difference between pass-by-assignment with mutable and immutable objects.** Provide an example of each showing different behavior.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Python passes object references, not values or pointers.
   - Immutable objects (int, str, tuple): modifications inside a function create a new object; the original is unchanged. Example: adding to an integer parameter does not affect the caller's variable.
   - Mutable objects (list, dict, set): in-place modifications (like ``append()``) affect the original object. Example: appending to a list parameter modifies the caller's list.
   - Reassignment inside a function always creates a new local binding, regardless of mutability.


.. admonition:: Question 28
   :class: hint

   **Explain the mutable default argument problem.** Why is ``def func(items=[])`` dangerous, and what is the recommended alternative?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Default argument values are evaluated once at function definition time, not at each call.
   - If the default is a mutable object (like a list or dict), all calls share the same object.
   - This causes unexpected accumulation of values across calls.
   - The fix is to use ``None`` as the default and create a new object inside the function: ``if items is None: items = []``.


.. admonition:: Question 29
   :class: hint

   **Describe the two essential components of a recursive function.** What happens if one of them is missing?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A recursive function needs a **base case** (the stopping condition) and a **recursive case** (where the function calls itself with a simpler input).
   - Without a base case, the function will recurse indefinitely until Python raises a ``RecursionError`` (default depth limit of 1000).
   - Without a recursive case, the function is just a regular function with no recursion.
   - Example: factorial uses ``n <= 1`` as the base case and ``n * factorial(n - 1)`` as the recursive case.


.. admonition:: Question 30
   :class: hint

   **Explain why type hints are useful even though Python does not enforce them at runtime.** Give at least two benefits.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Type hints improve **readability** by making function signatures self-documenting.
   - They enable **static analysis** tools like ``mypy`` to catch type errors before runtime.
   - IDEs use them for **autocompletion** and better code navigation.
   - They make **refactoring** safer by surfacing type mismatches across the codebase.
   - They serve as **documentation** that stays in sync with the code (unlike comments that may become outdated).