====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 2: Python Fundamentals -- Part I,
including packages and modules, indentation, Boolean types, operators, numeric
types, strings, and control flow.

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

   What is the difference between a **module** and a **package** in Python?

   A. A module is a folder; a package is a single ``.py`` file.

   B. A module is a single ``.py`` file; a package is a folder containing ``.py`` files with an ``__init__.py``.

   C. A module contains only functions; a package contains only classes.

   D. There is no difference; the terms are interchangeable.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A module is a single ``.py`` file; a package is a folder containing ``.py`` files with an ``__init__.py``.

   A module is any single Python file that can be imported. A package is a directory containing one or more modules plus an ``__init__.py`` file (which can be empty) that marks it as a package.


.. admonition:: Question 2
   :class: hint

   Which import approach is **recommended** for clarity and avoiding namespace pollution?

   A. ``import shape.square``

   B. ``from shape.square import *``

   C. ``from shape.square import compute_area, compute_perimeter``

   D. ``import shape.square as s``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``from shape.square import compute_area, compute_perimeter``

   This approach explicitly imports only the names you need, making it clear where each function comes from and avoiding namespace pollution. Wildcards (``*``) can silently overwrite existing names.


.. admonition:: Question 3
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      print(17 // 5)
      print(17 % 5)

   A. ``3`` and ``2``

   B. ``3.4`` and ``2``

   C. ``3`` and ``0.4``

   D. ``4`` and ``2``

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- ``3`` and ``2``

   ``17 // 5`` is floor division, which returns ``3`` (the quotient rounded down). ``17 % 5`` is the modulus operator, which returns ``2`` (the remainder).


.. admonition:: Question 4
   :class: hint

   Which of the following values is considered **truthy** in Python?

   A. ``0``

   B. ``""`` (empty string)

   C. ``[]`` (empty list)

   D. ``" "`` (string with a single space)

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ``" "`` (string with a single space)

   A string containing a space is non-empty and therefore truthy. Empty containers (``[]``, ``""``) and zero values (``0``) are falsy.


.. admonition:: Question 5
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      print(0 or "default")
      print("hello" and "world")

   A. ``0`` and ``"hello"``

   B. ``"default"`` and ``"world"``

   C. ``False`` and ``True``

   D. ``"default"`` and ``"hello"``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``"default"`` and ``"world"``

   The ``or`` operator returns the first truthy value (``"default"`` since ``0`` is falsy). The ``and`` operator returns the last value if all are truthy (``"world"``), or the first falsy value otherwise.


.. admonition:: Question 6
   :class: hint

   What is the correct way to check if a variable ``x`` is ``None``?

   A. ``if x == None:``

   B. ``if x is None:``

   C. ``if x = None:``

   D. ``if x.is_none():``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``if x is None:``

   The ``is`` operator checks identity (same object in memory). For ``None``, this is the correct approach since there is only one ``None`` object in Python. Using ``==`` would work but is not idiomatic.


.. admonition:: Question 7
   :class: hint

   Given the string ``greeting = "hello"``, what does ``greeting[-2]`` return?

   A. ``"h"``

   B. ``"o"``

   C. ``"l"``

   D. ``"e"``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``"l"``

   Negative indices count from the end. ``greeting[-1]`` is ``"o"``, so ``greeting[-2]`` is the second-to-last character, ``"l"``.


.. admonition:: Question 8
   :class: hint

   What is the output of ``"hello"[1:4]``?

   A. ``"hel"``

   B. ``"ell"``

   C. ``"ello"``

   D. ``"hell"``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``"ell"``

   Slicing ``[1:4]`` extracts characters at indices 1, 2, and 3 (stop index is exclusive). From ``"hello"``, these are ``"e"``, ``"l"``, ``"l"``.


.. admonition:: Question 9
   :class: hint

   Which of the following correctly reverses the string ``"Python"`` using slicing?

   A. ``"Python"[::1]``

   B. ``"Python"[::-1]``

   C. ``"Python"[-1::]``

   D. ``"Python"[0:-1:-1]``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``"Python"[::-1]``

   A stride of ``-1`` reverses the string. The result is ``"nohtyP"``.


.. admonition:: Question 10
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      x = 5
      print(1 < x < 10)

   A. ``True``

   B. ``False``

   C. ``SyntaxError``

   D. ``5``

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- ``True``

   Python supports chained comparisons. ``1 < x < 10`` is equivalent to ``1 < x and x < 10``. Since ``x = 5``, both conditions are true.


.. admonition:: Question 11
   :class: hint

   Why should you avoid comparing floats with ``==``?

   A. Python does not support float comparisons.

   B. Floats are stored with limited precision, causing rounding errors.

   C. The ``==`` operator only works with integers.

   D. Comparing floats raises a ``TypeError``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Floats are stored with limited precision, causing rounding errors.

   Floating-point numbers use IEEE 754 representation, which cannot exactly represent all decimal values. For example, ``0.1 + 0.2 == 0.3`` returns ``False``. Use ``math.isclose()`` instead.


.. admonition:: Question 12
   :class: hint

   What does the ``__name__`` variable contain when a Python script is run directly?

   A. The filename of the script.

   B. ``"__main__"``

   C. ``None``

   D. The module's import path.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``"__main__"``

   When a script is run directly, Python sets its ``__name__`` variable to ``"__main__"``. When imported as a module, ``__name__`` is set to the module's name.


.. admonition:: Question 13
   :class: hint

   Which string formatting method is **recommended** for Python 3.6+?

   A. ``"Name: %s" % name``

   B. ``"Name: {}".format(name)``

   C. ``f"Name: {name}"``

   D. ``"Name: " + name``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``f"Name: {name}"``

   F-strings (formatted string literals) are the recommended approach for Python 3.6+. They are faster, more readable, and support inline expressions.


.. admonition:: Question 14
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      a = [1, 2, 3]
      b = [1, 2, 3]
      print(a == b)
      print(a is b)

   A. ``True`` and ``True``

   B. ``True`` and ``False``

   C. ``False`` and ``True``

   D. ``False`` and ``False``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``True`` and ``False``

   ``a == b`` compares values (both lists contain the same elements, so ``True``). ``a is b`` compares identity (they are different objects in memory, so ``False``).


.. admonition:: Question 15
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      score = 75
      if score >= 90:
          grade = "A"
      elif score >= 80:
          grade = "B"
      elif score >= 70:
          grade = "C"
      else:
          grade = "F"
      print(grade)

   A. ``"A"``

   B. ``"B"``

   C. ``"C"``

   D. ``"F"``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``"C"``

   The conditions are evaluated in order. ``75 >= 90`` is ``False``, ``75 >= 80`` is ``False``, but ``75 >= 70`` is ``True``, so ``grade`` is assigned ``"C"``.


----


True or False
=============

.. admonition:: Question 16
   :class: hint

   **True or False:** Python uses braces ``{}`` to define code blocks, similar to C++ and Java.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Python uses indentation (whitespace) to define code blocks, not braces. This is a fundamental difference from C-style languages.


.. admonition:: Question 17
   :class: hint

   **True or False:** The expression ``not []`` evaluates to ``True`` because an empty list is falsy.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   An empty list ``[]`` is falsy in Python. The ``not`` operator inverts the Boolean value, so ``not []`` evaluates to ``True``.


.. admonition:: Question 18
   :class: hint

   **True or False:** In Python, strings are mutable, meaning you can change individual characters after creation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Strings in Python are immutable. You cannot change individual characters; instead, you must create a new string. Attempting ``s[0] = "X"`` raises a ``TypeError``.


.. admonition:: Question 19
   :class: hint

   **True or False:** The ``in`` operator can be used to check if a substring exists within a string.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The ``in`` operator works with strings to check for substrings. For example, ``"ell" in "hello"`` returns ``True``.


.. admonition:: Question 20
   :class: hint

   **True or False:** Python integers have unlimited precision, meaning they can grow arbitrarily large.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Unlike many languages where integers have fixed sizes (32-bit or 64-bit), Python integers can grow to arbitrary size, limited only by available memory.


.. admonition:: Question 21
   :class: hint

   **True or False:** The expression ``10 // -3`` evaluates to ``-3`` because floor division rounds toward negative infinity.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``10 // -3`` evaluates to ``-4``, not ``-3``. Floor division rounds toward negative infinity, so ``-3.33...`` rounds down to ``-4``.


.. admonition:: Question 22
   :class: hint

   **True or False:** Wildcard imports (``from module import *``) are recommended because they save typing.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Wildcard imports should be avoided because they pollute the namespace and can silently overwrite existing names, making code harder to understand and debug.


.. admonition:: Question 23
   :class: hint

   **True or False:** The conditional expression ``status = "adult" if age >= 18 else "minor"`` is valid Python syntax.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   This is Python's conditional (ternary) expression syntax. It assigns ``"adult"`` if the condition is true, otherwise ``"minor"``.


.. admonition:: Question 24
   :class: hint

   **True or False:** Adding a path to ``sys.path`` makes packages discoverable for all future Python sessions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``sys.path.insert()`` only affects the current Python session. The path resets when you start a new Python interpreter. For persistent changes, use ``PYTHONPATH``, ``.pth`` files, or ``pip install -e``.


.. admonition:: Question 25
   :class: hint

   **True or False:** The ``bool`` type in Python is a subclass of ``int``, where ``True`` equals ``1`` and ``False`` equals ``0``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``bool`` is indeed a subclass of ``int``. You can verify this with ``isinstance(True, int)`` which returns ``True``. Arithmetic with Booleans is valid: ``True + True == 2``.


----


Essay Questions
===============

.. admonition:: Question 26
   :class: hint

   **Explain why wildcard imports (** ``from module import *`` **) should be avoided.** Describe the problem of namespace pollution and provide an example of how it can cause bugs.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Wildcard imports (``from module import *``) bring all public names from a module into the current namespace.
   - This causes namespace pollution where names from different modules can silently overwrite each other.
   - Example: If both ``shape.square`` and ``shape.circle`` define ``compute_area()``, the second import overwrites the first without warning.
   - Best practice is to use explicit named imports so it's clear where each function originated.


.. admonition:: Question 27
   :class: hint

   **Describe how Python's short-circuit evaluation works with** ``and`` **and** ``or`` **operators.** Explain what values these operators return when used with non-Boolean operands and provide an example use case.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``and`` returns the first falsy value, or the last value if all are truthy.
   - ``or`` returns the first truthy value, or the last value if all are falsy.
   - These operators return the actual operand, not necessarily ``True`` or ``False``.
   - Common pattern: ``name = user_input or "Anonymous"`` provides a default value when ``user_input`` is empty or falsy.


.. admonition:: Question 28
   :class: hint

   **Explain the difference between** ``==`` **and** ``is`` **operators.** When should you use each one, and why is ``is`` recommended for ``None`` checks?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``==`` compares values (whether two objects have the same content).
   - ``is`` compares identity (whether two references point to the same object in memory).
   - Use ``is`` for ``None`` checks because there is exactly one ``None`` object in Python, making identity comparison both correct and idiomatic.
   - Never rely on ``is`` for integers or strings due to interning optimizations that vary by implementation.


.. admonition:: Question 29
   :class: hint

   **Describe three methods for making Python packages discoverable** (i.e., available for import from anywhere). For each method, explain when it would be most appropriate to use.

   *(3-5 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``sys.path.insert()``: Adds path for the current script only; good for quick fixes and sibling packages.
   - ``PYTHONPATH`` environment variable: Affects the terminal session; good for development and testing.
   - ``.pth`` files in site-packages: System-wide and permanent; good for shared libraries across projects.
   - ``pip install -e .`` (editable install): Most robust and professional approach; works from anywhere and changes take effect immediately without reinstalling.


.. admonition:: Question 30
   :class: hint

   **Explain string slicing syntax** ``[start:stop:stride]`` **and demonstrate how to extract a substring and reverse a string.** Use the string ``"Python"`` in your examples.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Syntax: ``[start:stop:stride]`` where start is inclusive, stop is exclusive, and stride is the step size.
   - Extracting substring: ``"Python"[0:2]`` returns ``"Py"``; ``"Python"[2:]`` returns ``"thon"``.
   - Reversing: ``"Python"[::-1]`` returns ``"nohtyP"`` because a stride of ``-1`` steps backward through the string.
   - Defaults: start defaults to 0, stop defaults to end, stride defaults to 1.