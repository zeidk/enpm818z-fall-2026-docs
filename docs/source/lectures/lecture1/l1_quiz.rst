====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 1: Course Introduction,
including environment setup, the Python execution pipeline, Python variables,
data types, mutability, and basic Python concepts.

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

   What is the primary role of the **lexer** in the Python execution pipeline?

   A. Executes bytecode instructions one at a time.

   B. Breaks source code into tokens (keywords, identifiers, operators, literals).

   C. Converts the Abstract Syntax Tree into bytecode.

   D. Validates syntax and builds a parse tree.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Breaks source code into tokens (keywords, identifiers, operators, literals).

   The lexer (tokenizer) is the first stage of the execution pipeline. It reads the source code character by character and groups them into tokens like keywords, identifiers, operators, and literals.


.. admonition:: Question 2
   :class: hint

   Which of the following best describes **CPython**?

   A. A version of Python that compiles directly to machine code.

   B. The reference implementation of Python, written in C.

   C. A Python implementation optimized for microcontrollers.

   D. A just-in-time compiler for Python code.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The reference implementation of Python, written in C.

   CPython is the default and most widely used implementation of Python. The interpreter itself is written in C, which is why it's called "CPython." When you run ``python3``, you're running CPython.


.. admonition:: Question 3
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      x = [1, 2, 3]
      y = x
      y.append(4)
      print(x)

   A. ``[1, 2, 3]``

   B. ``[1, 2, 3, 4]``

   C. ``[4]``

   D. An error occurs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``[1, 2, 3, 4]``

   When ``y = x`` is executed, both variables reference the same list object. Modifying the list through ``y`` also affects ``x`` because they point to the same memory location. This is called aliasing.


.. admonition:: Question 4
   :class: hint

   Which of the following data types is **mutable** in Python?

   A. ``int``

   B. ``str``

   C. ``tuple``

   D. ``list``

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ``list``

   Lists are mutable, meaning their contents can be changed in place without creating a new object. Integers, strings, and tuples are immutable -- any modification creates a new object.


.. admonition:: Question 5
   :class: hint

   What does the ``id()`` function return in Python?

   A. The data type of an object.

   B. A unique integer representing the object's memory address.

   C. The size of an object in bytes.

   D. The hash value of an object.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A unique integer representing the object's memory address.

   The ``id()`` function returns a unique identifier for an object, which in CPython corresponds to the object's memory address. This ID remains constant for the object's lifetime.


.. admonition:: Question 6
   :class: hint

   What is the correct way to check if a variable ``x`` is ``None``?

   A. ``if x == None:``

   B. ``if x is None:``

   C. ``if x = None:``

   D. ``if x.isNone():``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``if x is None:``

   Since ``None`` is a singleton (only one instance exists), using ``is`` for identity comparison is the correct and idiomatic approach. While ``==`` would work, ``is`` is more explicit and slightly faster.


.. admonition:: Question 7
   :class: hint

   Which statement about Python's **dynamic typing** is correct?

   A. Variable types must be declared before use.

   B. Types are checked at compile time.

   C. A variable can be rebound to objects of different types during execution.

   D. Dynamic typing prevents type-related runtime errors.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- A variable can be rebound to objects of different types during execution.

   In Python, variables are names that reference objects, and the type is associated with the object, not the variable. A variable can be reassigned to objects of any type during execution.


.. admonition:: Question 8
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      a = 10
      b = 10
      print(a is b)

   A. ``True``

   B. ``False``

   C. ``10``

   D. An error occurs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- ``True``

   CPython caches small integers (typically -5 to 256) for efficiency. Since both ``a`` and ``b`` are assigned to 10, they reference the same cached integer object, so ``a is b`` returns ``True``.


.. admonition:: Question 9
   :class: hint

   Where does CPython cache bytecode for imported modules?

   A. In the ``__bytecode__`` directory.

   B. In the ``__pycache__`` directory.

   C. In the system's temporary folder.

   D. Bytecode is never cached.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- In the ``__pycache__`` directory.

   When a module is imported, CPython compiles it to bytecode and caches the ``.pyc`` files in a ``__pycache__`` directory. This speeds up subsequent imports by avoiding recompilation.


.. admonition:: Question 10
   :class: hint

   What is the purpose of a **linter** like Ruff?

   A. To compile Python code to machine code.

   B. To analyze code for potential errors, style violations, and code smells.

   C. To execute Python scripts in debug mode.

   D. To convert Python 2 code to Python 3.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To analyze code for potential errors, style violations, and code smells.

   A linter like Ruff analyzes source code to detect potential bugs, enforce coding standards (like PEP 8), and identify code smells before runtime. It helps catch issues early in development.


.. admonition:: Question 11
   :class: hint

   Which Python implementation would be best for running code on a microcontroller with limited RAM?

   A. CPython

   B. PyPy

   C. MicroPython

   D. Jython

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- MicroPython

   MicroPython is specifically designed for microcontrollers and embedded systems with limited resources. It requires only about 256KB of RAM, making it ideal for devices like ESP32 or Raspberry Pi Pico.


.. admonition:: Question 12
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      x = 10
      print(id(x))
      x = x + 1
      print(id(x) == id(10))

   A. The same ID is printed twice, then ``True``.

   B. Different IDs are printed, then ``True``.

   C. Different IDs are printed, then ``False``.

   D. An error occurs because integers don't have IDs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Different IDs are printed, then ``True``.

   Since integers are immutable, ``x + 1`` creates a new integer object. The first ``id(x)`` shows the ID of 10, then after ``x = x + 1``, x points to 11. However, ``id(10)`` returns the same ID as the original because 10 is still cached.


.. admonition:: Question 13
   :class: hint

   According to PEP 8, which naming convention should be used for **variables and functions**?

   A. ``camelCase``

   B. ``PascalCase``

   C. ``snake_case``

   D. ``UPPER_CASE``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``snake_case``

   PEP 8, Python's official style guide, recommends ``snake_case`` for variable and function names, ``PascalCase`` for class names, and ``UPPER_CASE`` for constants.


.. admonition:: Question 14
   :class: hint

   What does the following code print?

   .. code-block:: python

      def greet(name):
          print(f"Hello, {name}")

      result = greet("Alice")
      print(result)

   A. ``Hello, Alice`` followed by ``Hello, Alice``

   B. ``Hello, Alice`` followed by ``None``

   C. ``None`` followed by ``Hello, Alice``

   D. An error occurs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``Hello, Alice`` followed by ``None``

   The function ``greet()`` prints "Hello, Alice" but doesn't explicitly return anything. In Python, functions without a return statement return ``None`` by default, so ``result`` is ``None``.


.. admonition:: Question 15
   :class: hint

   Which of the following is a **valid** Python variable name?

   A. ``2fast``

   B. ``my-variable``

   C. ``class``

   D. ``_private_var``

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ``_private_var``

   Valid Python variable names must start with a letter or underscore, and can contain letters, digits, and underscores. ``2fast`` starts with a digit, ``my-variable`` contains a hyphen, and ``class`` is a reserved keyword.


----


True or False
=============

.. admonition:: Question 16
   :class: hint

   **True or False:** In Python, variables are direct storage locations that hold values, similar to C++.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   In Python, variables are names (references) bound to objects in memory, not direct storage locations. Unlike C++, the variable doesn't hold the value directly -- it points to an object that holds the value.


.. admonition:: Question 17
   :class: hint

   **True or False:** The ``==`` operator compares object identity, while ``is`` compares values.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   It's the opposite: ``==`` compares values (equality), while ``is`` compares identity (whether two references point to the same object in memory).


.. admonition:: Question 18
   :class: hint

   **True or False:** Python is sometimes called a "compiled interpreted language" because it compiles to bytecode, then interprets that bytecode.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Python first compiles source code to bytecode (an intermediate representation), then the interpreter executes that bytecode. The bytecode is not native machine code -- it runs on the Python Virtual Machine.


.. admonition:: Question 19
   :class: hint

   **True or False:** Strings in Python are mutable, meaning you can change individual characters after creation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Strings in Python are immutable. You cannot change individual characters in a string. Any operation that appears to modify a string actually creates a new string object.


.. admonition:: Question 20
   :class: hint

   **True or False:** The ``__pycache__`` directory contains cached bytecode files to speed up future imports of modules.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   When Python imports a module, it compiles the source to bytecode and caches it in ``__pycache__`` as ``.pyc`` files. This allows faster subsequent imports by skipping the compilation step if the source hasn't changed.


.. admonition:: Question 21
   :class: hint

   **True or False:** In Python, ``True`` is a subclass of ``int`` and equals ``1``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``bool`` is a subclass of ``int`` in Python. ``True`` equals ``1`` and ``False`` equals ``0``. You can verify this with ``isinstance(True, int)`` which returns ``True``, and ``True + True`` equals ``2``.


.. admonition:: Question 22
   :class: hint

   **True or False:** The Global Interpreter Lock (GIL) in CPython allows true multi-threaded parallelism for CPU-bound tasks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The GIL (Global Interpreter Lock) prevents true parallel execution of Python bytecode in threads. Only one thread can execute Python bytecode at a time, limiting parallelism for CPU-bound tasks. (Note: CPython 3.13+ offers experimental free-threaded builds.)


.. admonition:: Question 23
   :class: hint

   **True or False:** When you assign ``b = a`` where ``a`` is a list, both ``a`` and ``b`` reference the same object in memory.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   When you assign ``b = a`` where ``a`` is a list, both variables become references to the same list object in memory. This is called aliasing. Modifying the list through either variable affects both.


.. admonition:: Question 24
   :class: hint

   **True or False:** Syntax errors in Python are caught during the runtime phase, not the compilation phase.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Syntax errors are caught during the compilation phase, before any code executes. The parser validates syntax while building the parse tree. Runtime errors (like ``NameError``, ``TypeError``) occur during execution.


.. admonition:: Question 25
   :class: hint

   **True or False:** The ``None`` object in Python is a singleton, meaning there is only one instance of it in memory.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``None`` is a singleton in Python -- there is exactly one ``None`` object in memory. This is why we use ``is None`` instead of ``== None``; we're checking if a variable references that single ``None`` object.


----


Essay Questions
===============

.. admonition:: Question 26
   :class: hint

   **Explain the difference between the compilation phase and the runtime phase in Python's execution pipeline.** What types of errors are caught in each phase?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The compilation phase happens once when a module is first imported or run. It includes lexing, parsing, AST generation, and bytecode compilation.
   - Syntax errors are caught during compilation, before any code executes.
   - The runtime phase happens every time code executes. The interpreter reads and executes bytecode instructions.
   - Runtime errors (NameError, TypeError, ValueError, etc.) occur during execution when invalid operations are attempted.


.. admonition:: Question 27
   :class: hint

   **Describe the concept of aliasing in Python.** Explain what happens when you assign one variable to another with mutable objects, and why this can lead to unexpected behavior.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Aliasing occurs when multiple variable names reference the same object in memory.
   - When you assign ``b = a`` where ``a`` is a mutable object (like a list), both names point to the same object.
   - Modifying the object through one name affects all aliases because they share the same underlying object.
   - To avoid this, create an independent copy using ``b = a.copy()`` or ``b = list(a)``.


.. admonition:: Question 28
   :class: hint

   **Explain the difference between mutable and immutable objects in Python.** Provide examples of each type and describe what happens when you modify them.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Immutable objects (int, float, str, tuple) cannot be changed after creation. Any modification creates a new object with a different ID.
   - Mutable objects (list, dict, set) can be modified in place. The object's ID remains the same after modification.
   - Example: Adding to a list with ``append()`` modifies the same object, but ``x = x + 1`` for an integer creates a new integer object.
   - Understanding mutability is crucial for avoiding bugs with function arguments and variable assignments.


.. admonition:: Question 29
   :class: hint

   **Compare CPython with PyPy.** Describe the key differences between these Python implementations and when you might choose one over the other.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - CPython is the reference implementation, written in C. It has the best compatibility with C extensions and the largest ecosystem.
   - PyPy uses Just-In-Time (JIT) compilation, achieving significant speedups for long-running code by compiling hot paths to machine code.
   - Use CPython for general development and when you need C extension compatibility (NumPy, pandas, TensorFlow).
   - Use PyPy for performance-critical applications that don't rely heavily on C extensions.


.. admonition:: Question 30
   :class: hint

   **Explain why Python uses the** ``is`` **operator for** ``None`` **comparisons instead of** ``==`` **.** What is the difference between identity and equality comparison?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``None`` is a singleton -- only one ``None`` object exists in Python's memory.
   - The ``is`` operator checks identity (same object in memory), while ``==`` checks equality (same value).
   - Since there's only one ``None`` object, checking identity with ``is`` is the correct and idiomatic approach.
   - Using ``is`` is also slightly faster because it compares memory addresses directly rather than calling equality methods.