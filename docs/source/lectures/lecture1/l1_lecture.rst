====================================================
Lecture
====================================================



Course Overview
---------------

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **What You Will Learn**

    - Specifically designed for students who want to learn robotics with direct applications.
    - Focus on Python programming and its applications with mobile robots using ROS 2.
    - Students will perform small hands-on exercises in class to gain a deeper understanding of how the application of Python to ROS can be used in real-world challenges.
    - The final project will be to control one or multiple mobile robots in a Gazebo environment using Nav2 and behavior trees.

.. tip::

   **Key Questions**: Do you need robotics knowledge for this course? Do you need prior programming knowledge to take this course?


Course Structure
----------------

.. grid:: 1 3 3 3
    :gutter: 2

    .. grid-item-card:: 📖 Before Class
        :class-card: sd-border-secondary

        - Get the lecture materials from Canvas and/or Github.
        - Complete pre-work activities.

    .. grid-item-card:: 🏫 During Class
        :class-card: sd-border-secondary

        - Questions and discussions on the previous lecture(s).
        - Quiz (if any).
        - Lecture — attend class with your laptop and required software installed.
        - Participation is very important.

    .. grid-item-card:: 📝 After Class
        :class-card: sd-border-secondary

        - Review the slides.
        - Re-run the code provided to you.
        - Start working on the next assignment (if any).


Grading Structure
-----------------

.. list-table::
   :widths: 60 20
   :header-rows: 1
   :class: compact-table

   * - Component
     - Weight
   * - Individual Assignments (2)
     - 30%
   * - Quizzes (5)
     - 15%
   * - Participation/Engagement
     - 5%
   * - Team Projects (2)
     - 30%
   * - Final Project
     - 20%
   * - **Total**
     - **100%**

.. warning::

   **No Final Exam**

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ⏰ Late Policy
        :class-card: sd-border-warning

        - **10%** deduction per calendar day late
        - Maximum **30%** reduction (3 days)
        - Work submitted more than 3 days late earns **zero**

    .. grid-item-card:: 🤖 AI Policy
        :class-card: sd-border-warning

        - AI tools **NOT permitted** for individual assignments
        - AI tools **permitted** for team projects and final project with documentation


Course Schedule
---------------

.. list-table::
   :widths: 5 50 35
   :header-rows: 1
   :class: compact-table

   * - Wk
     - Topic
     - Deliverable
   * - 1
     - Course Introduction
     -
   * - 2
     - Python Fundamentals — Part I
     -
   * - 3
     - Python Fundamentals — Part II
     - Assignment 1 Handed Out
   * - 4
     - Python Functions
     - Quiz 1
   * - 5
     - Object-Oriented Programming — Part I
     - Assignment 1 Due, Assignment 2 Handed Out
   * - 6
     - Object-Oriented Programming — Part II
     - Quiz 2
   * - 7
     - ROS 2 Foundations
     - Assignment 2 Due
   * - 8
     - *Spring Break*
     - —
   * - 9
     - ROS 2 Executors and Custom Messages
     - Quiz 3, Project 1 Handed Out
   * - 10
     - ROS 2 Services and Parameters
     -
   * - 11
     - Transforms, Coordinate Frames, and Sensor Integration
     - Project 1 Due, Project 2 Handed Out
   * - 12
     - ROS 2 Actions and Lifecycle Nodes
     - Quiz 4
   * - 13
     - Navigation Stack Foundations (Nav2)
     - Project 2 Due, Final Project Handed Out
   * - 14
     - Behavior Trees
     - Quiz 5
   * - 15
     - Final Project Work Session and Status Check
     - Final Project Due (May 08)


Quiz Policy
-----------

- Quizzes are taken during class hours between 7:00pm and 7:20pm.
- If you are not a remote/online student and you cannot come to class:

  - Do not take the quiz.
  - Take the quiz another day with a 10% penalty.
  - No penalty if you are excused (doctor's note, supervisor's note, etc).

- No proctor needed.
- Closed-notes quizzes only (no slides and no software to test code).

.. note::

   **Online/Remote Students**: Email the instructor with day and time you plan to take quizzes.


Peer Reviews
------------

- After team projects and the final project are submitted, you will give your teammates a score from 1-10 indicating their productive involvement.

  - You cannot rate yourself.
  - You get 1 pt by just emailing your peer reviews for your teammates.

- 60% of your overall score will be based on your assignment/project grade and 40% will be based on your peer reviews from your group.

.. dropdown:: 📊 Peer Review Example
    :open:
    :icon: table

    - Your group got 30/30 pts on an assignment/project.
    - Your average peer review from your teammates is 4/10 pts.
    - You emailed your peer review for your teammates: Your average peer review becomes 5/10 pts (50%).

    **Grade breakdown:**

    - Assignment portion: 60% of 30 = 18 pts
    - Peer review portion: 40% of 30 = 12 pts × 50% = 6 pts
    - Your final grade: 18 + 6 = **24/30 pts**


Final Project
-------------

.. card::
    :class-card: sd-border-primary sd-border-3

    **Autonomous Mobile Robot Navigation**

    The final project involves developing a ROS 2 package that enables a mobile robot to autonomously navigate through a simulated environment in Gazebo Harmonic.

    The project integrates:

    - Sensor processing
    - Coordinate transforms
    - Nav2 navigation
    - Application-level behavior trees using *py_trees*

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ⚙️ What Nav2 Handles (You Configure)
        :class-card: sd-border-secondary

        - Path planning and trajectory following
        - Obstacle avoidance via costmaps (subscribes to sensor topics directly)
        - Recovery behaviors (spin, backup, wait)

    .. grid-item-card:: 🌳 What You Build with py_trees
        :class-card: sd-border-secondary

        - **Application-level behavior tree** that coordinates high-level tasks:

          - Patrol a sequence of waypoints (calls ``/navigate_to_pose`` action)
          - React to events (e.g., object detected → investigate)
          - Handle task priorities (high-priority task interrupts patrol)

        - Your behavior tree calls Nav2 action servers — it does **not** replace Nav2's internal navigation logic.

.. note::

   Week 15 is reserved as a work session and status check.


Software & Hardware
====================================================

Operating System
----------------

.. card::
    :class-card: sd-border-primary sd-shadow-sm

    **Ubuntu 24.04 LTS (Noble Numbat)**

    Use this course as an opportunity to learn Linux. You should at least know the following shell commands (terminal):

    ``ls``, ``pwd``, ``cd``, ``mv``, ``mkdir``, ``rm``, ``source``, ``touch``, ``man``, and ``grep``.

Minimum Hardware
----------------

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **CPU**
     - Intel i5 or equivalent, 4+ cores
   * - **RAM**
     - 8 GB minimum, 16 GB recommended
   * - **Storage**
     - 50 GB free space

.. note::

   Docker containers will be provided to ensure a consistent development environment across all platforms.


Development Tools
-----------------

.. list-table::
   :widths: 20 30 30
   :header-rows: 1
   :class: compact-table

   * - Software
     - Description
     - Download/Install
   * - Visual Studio Code
     - Light, cross-platform IDE
     - `Visual Studio Code <https://code.visualstudio.com/>`_
   * - Docker Desktop
     - Containerized development
     - `Docker Desktop <https://www.docker.com/products/docker-desktop/>`_
   * - ROS 2 Jazzy
     - Robot Operating System
     - `ROS Jazzy <https://docs.ros.org/en/jazzy/>`_
   * - Gazebo Harmonic
     - Simulation environment
     - `Gazebo Harmonic <https://gazebosim.org/docs/harmonic/getstarted/>`_

.. important::

   **To Do**: Install Visual Studio Code and Docker Desktop before the in-class exercise.


Environment Setup
====================================================

This section walks through configuring Visual Studio Code and Docker for Python development.

.. grid:: 1 3 3 3
    :gutter: 2

    .. grid-item-card:: 1️⃣ Install VS Code
        :class-card: sd-border-primary

        Download and install from `Visual Studio Code <https://code.visualstudio.com/>`_. Available for Windows, macOS, and Linux.

    .. grid-item-card:: 2️⃣ Install Docker
        :class-card: sd-border-primary

        Download and install `Docker Desktop <https://www.docker.com/products/docker-desktop/>`_. Verify installation with ``docker --version``.

    .. grid-item-card:: 3️⃣ Install Extensions
        :class-card: sd-border-primary

        Install the required VS Code extensions (see below).


Visual Studio Code
------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item::

        **Download & Install**

        - Download from `Visual Studio Code <https://code.visualstudio.com/>`_
        - Available for Windows, macOS, Linux
        - Lightweight, extensible, free

    .. grid-item::

        **Required Extensions**

        - `Python (Microsoft) <https://marketplace.visualstudio.com/items?itemName=ms-python.python>`_ — Python language support
        - `Dev Containers (Microsoft) <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers>`_ — Development in containers
        - `Container Tools (Microsoft) <https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-containers>`_ — Build, manage, and deploy containers


Docker Installation
-------------------

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **Installing Docker Desktop**

    1.  Download and install `Docker Desktop <https://www.docker.com/products/docker-desktop/>`_.

    2.  Verify your installation:

        .. code-block:: bash

           docker --version

    3.  Docker allows us to run isolated containers with all dependencies pre-installed.

    4.  We will use Dev Containers in VS Code to develop inside Docker containers.

.. note::

   **Linux Users**: You may need to add your user to the docker group:

   .. code-block:: bash

      sudo usermod -aG docker $USER

   Log out and log back in for changes to take effect.


Creating a Workspace
--------------------

1. Create a workspace where you will host all Python code for this course.

   - Example: ``~/enpm605/py_ws``

2. Open a terminal and run:

   .. code-block:: bash

      cd <path to workspace>
      code .

3. By starting VS Code in a folder, that folder becomes your "workspace".

4. VS Code stores workspace-specific settings in ``.vscode/settings.json``.

.. tip::

   Any ``settings.json`` file in a nested folder takes precedence over other ``settings.json`` files.


Running Python in VS Code
====================================================

Selecting the Python Interpreter
---------------------------------

In order to run Python code and get Python IntelliSense, you must tell VS Code which interpreter to use.

1. Open **Command Palette** with ``Ctrl+Shift+P``
2. Start typing **Python: Select Interpreter**
3. Select a Python 3 interpreter.


Creating a Python File
----------------------

Create the file ``running_demo.py`` inside the ``lecture1`` folder and add the following code:

.. code-block:: python
   :linenos:

   def greet(name):
       print("Hello", name)

   greet('Bob')


Execution Methods
-----------------

.. tab-set::

    .. tab-item:: Run Button

        Click the **Run Python File** button (top-right triangle icon).

    .. tab-item:: Context Menu

        Right-click on the Python file and select **Run Python File in Terminal**.

    .. tab-item:: Integrated Terminal

        Open terminal with ``Ctrl + j`` and run:

        .. code-block:: bash

           python3 running_demo.py

    .. tab-item:: Interactive Mode (REPL)

        1. ``Ctrl+Shift+P`` → Type **REPL** → Select **Python: Start Native Python REPL**
        2. Select code and press ``Shift+Enter`` to execute in REPL.


Debugging Python Code
---------------------

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: 🔧 Setup
        :class-card: sd-border-info

        1. **Set a breakpoint**: Click in the gutter or place your cursor on a line and press ``F9``
        2. Expand top-right triangle and select **Debug Python File** or press ``F5``
        3. Since this is your first time debugging this file, a configuration menu will open: Select **Python Debugger** then **Python File**.

    .. grid-item-card:: 🔍 Inspect
        :class-card: sd-border-info

        4. Use the debug toolbar to step through code, inspect variables, and evaluate expressions.
        5. You can also work with variables in the **Debug Console** using the ``>`` field at the bottom.


Python Linters
====================================================

What is a Linter?
-----------------

.. card::
    :class-card: sd-border-primary sd-shadow-sm

    **Definition**

    A **linter** analyzes your code for potential errors, style violations, and code smells (*"Refactoring: Improving the Design of Existing Code"* — M. Fowler *et al.*). Linters help enforce coding standards and catch bugs **before** runtime. The name comes from the original ``lint`` tool for C (1978).


Popular Python Linters
----------------------

.. list-table::
   :widths: 15 20 15 50
   :header-rows: 1
   :class: compact-table

   * - Tool
     - Type
     - Speed
     - Notes
   * - **Ruff**
     - Linter + Formatter
     - Extremely Fast
     - Written in Rust, replaces multiple tools
   * - Flake8
     - Linter
     - Fast
     - Lightweight, plugin ecosystem
   * - Pylint
     - Linter
     - Slow
     - Deep analysis, very thorough
   * - Black
     - Formatter
     - Fast
     - Opinionated, no configuration
   * - isort
     - Import Sorter
     - Fast
     - Sorts imports alphabetically

.. tip::

   **Recommendation**: Use **Ruff** — it combines linting, formatting, and import sorting in one tool, and is 10–100× faster than alternatives.


Ruff — The Modern Python Linter
---------------------------------

**Why Ruff?**

- **Blazingly fast** — Written in Rust, runs in milliseconds.
- **All-in-one** — Replaces Flake8, Black, isort, and many plugins.
- **Auto-fix** — Can automatically fix many issues with ``--fix``.
- **Drop-in replacement** — Compatible with existing Flake8/Black configurations.
- **Adopted by major projects** — FastAPI, pandas, Apache Airflow, pydantic.


Ruff in Action
--------------

.. tab-set::

    .. tab-item:: Code with Issues

        .. code-block:: python
           :linenos:

           import os
           import sys
           import math

           def calculate_area(radius):
               pi = 3.14159  # Magic number
               area=pi*radius**2  # No spaces
               return area

           x = 10
           if x == True:  # Compare to True
               print("yes")

    .. tab-item:: Ruff Output

        .. code-block:: text

           $ ruff check example.py
           example.py:1:8: F401 `os` imported but unused
           example.py:3:8: F401 `math` imported but unused
           example.py:6:10: PLR2004 Magic value used in comparison
           example.py:7:9: E225 Missing whitespace around operator
           example.py:11:6: E712 Comparison to `True` should be `if x:`
           Found 5 errors.

    .. tab-item:: Auto-fix

        .. code-block:: text

           $ ruff check --fix example.py  # Removes unused imports automatically
           Found 5 errors (2 fixed, 3 remaining).


Ruff in VS Code
----------------

Install the `Ruff extension <https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff>`_ from the VS Code marketplace and configure in ``.vscode/settings.json``:

.. code-block:: json

   {
       "editor.formatOnSave": true,
       "editor.defaultFormatter": "charliermarsh.ruff",
       "editor.codeActionsOnSave": {
           "source.fixAll.ruff": "explicit",
           "source.organizeImports.ruff": "explicit"
       },
       "ruff.lineLength": 100
   }

**What This Does:**

- **Format on save** — Automatically formats code when you save.
- **Fix all** — Applies safe auto-fixes on save.
- **Organize imports** — Sorts and removes unused imports on save.


Environment Verification
====================================================

Verify Your Setup
-----------------

1. Open VS Code in your workspace.
2. Create a file called ``verify_setup.py``.
3. Add the following code:

.. code-block:: python
   :linenos:

   import sys

   def main():
       print("=" * 40)
       print("Environment Verification")
       print("=" * 40)
       print(f"Python Version: {sys.version}")
       print("Setup successful!")
       print("=" * 40)

   if __name__ == "__main__":
       main()

4. Run the file using any of the methods discussed.
5. Verify you see the Python version and success message.


Expected Output
---------------

.. card::
    :class-card: sd-bg-light

    .. code-block:: console

       $ python3 verify_setup.py

       ========================================
       Environment Verification
       ========================================
       Python Version: 3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)]
       Setup successful!
       ========================================

.. tip::

   **Troubleshooting**: If you encounter errors, verify: (1) Python is installed, (2) VS Code Python extension is installed, (3) Correct interpreter is selected.


Python Execution Pipeline
====================================================

Understanding how Python code is executed from source to output.


Python is an Interpreted Language
---------------------------------

.. card::
    :class-card: sd-border-primary sd-shadow-sm

    **Pipeline Stages**

    * **Source code** — Human-readable code written in Python syntax (``.py`` files).
    * **Lexer (Tokenizer)** — Breaks source code into tokens (keywords, identifiers, operators, literals).
    * **Parser** — Analyzes token sequence, validates syntax, and builds a parse tree.
    * **Abstract Syntax Tree (AST)** — Simplified tree representation focusing on semantic meaning.
    * **Bytecode Compiler** — Converts AST to low-level instructions (``.pyc`` files in ``__pycache__``).

      * Bytecode is generated in memory for executed scripts.
      * For imported modules, bytecode is cached in ``__pycache__`` to speed up future imports.

    * **Interpreter Loop** — Executes bytecode instructions via a fetch-decode-execute cycle.

.. note::

   **Pipeline Flow**: Source Code → Lexer → Parser → AST → Bytecode Compiler → Interpreter Loop → Output


Compilation vs. Runtime Phases
------------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🔨 Compilation Phase
        :class-card: sd-border-info

        - Happens once when module is first imported or run.
        - Lexer → Parser → AST → Bytecode
        - **Syntax errors** caught here (before any code runs).
        - Recompilation only if source file changes.

    .. grid-item-card:: ▶️ Runtime Phase
        :class-card: sd-border-info

        - Happens every time the code executes.
        - Interpreter loop reads and executes bytecode.
        - **Runtime errors** occur here (``NameError``, ``TypeError``, etc.).
        - Stack-based execution model.
        - Manages memory and garbage collection.


Compiled vs. Interpreted Languages
-----------------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ⚙️ Compiled Languages
        :class-card: sd-border-secondary

        A compiler translates source code directly into native machine code. The CPU executes the binary directly — no intermediary.

        - **Advantage**: Faster execution; optimizations applied at compile time.
        - **Disadvantage**: Platform-specific binaries; longer compile times.
        - **Examples**: C, C++, Rust, Go

        ``Source → Compiler → Machine Code → CPU``

    .. grid-item-card:: 🐍 Interpreted Languages
        :class-card: sd-border-secondary

        Source code is compiled to intermediate bytecode. An interpreter executes bytecode instruction by instruction.

        - **Advantage**: Portable; same bytecode runs on any platform with the interpreter.
        - **Disadvantage**: Slower; interpreter overhead on each instruction.
        - **Examples**: Python, JavaScript, Ruby

        ``Source → Compiler → Bytecode → Interpreter → CPU``

.. note::

   Python is sometimes called a "compiled interpreted language": it compiles to bytecode, then interprets that bytecode. The bytecode is not native machine code.


CPython — The Reference Implementation
---------------------------------------

.. card::
    :class-card: sd-border-warning sd-border-3

    **What is CPython?**

    - **CPython** is the reference (default) implementation of Python.
    - The interpreter itself is written in C — hence the name "CPython".
    - When you run ``python3 script.py``, you are running a C program that:

      - Lexes, parses, and compiles your code to bytecode.
      - Executes bytecode via an evaluation loop (``_PyEval_EvalFrameDefault`` in ``ceval.c``).

    - The "Python Virtual Machine" (PVM) is not a separate program — it's the interpreter loop inside CPython.

**Key Characteristics:**

- Best compatibility with C extensions — libraries like NumPy, pandas, and TensorFlow are partially written in C for performance and only fully support CPython.
- Has the **Global Interpreter Lock (GIL)** — limits true multi-threaded parallelism.
- CPython 3.13 introduced experimental free-threaded builds (no GIL).
- CPython 3.14 promotes free-threading to **officially supported** (but still optional).

  - Install with: ``python3.14t`` (the "t" suffix indicates free-threaded)
  - Single-threaded overhead reduced from ~40% to ~5-10%

**Check your implementation:**

.. code-block:: bash

   python3 --version && python3 -c "import sys; print(sys.implementation)"


Inspecting the Pipeline
------------------------

Create a file called ``internals_demo.py`` to explore Python's internals.

.. tab-set::

    .. tab-item:: View Tokens (Lexer Output)

        .. code-block:: python
           :linenos:

           import io
           import tokenize

           code = "x = 5 + 3"
           tokens = tokenize.generate_tokens(io.StringIO(code).readline)

           for tok in tokens:
               print(tok)

    .. tab-item:: View AST (Parser Output)

        .. code-block:: python
           :linenos:

           import ast

           code = "x = 5 + 3"
           tree = ast.parse(code)
           print(ast.dump(tree, indent=2))

    .. tab-item:: View Bytecode (Compiler Output)

        .. code-block:: python
           :linenos:

           import dis

           def example():
               x = 5 + 3
               return x

           dis.dis(example)

        **Sample Output:**

        .. code-block:: text

           27    RESUME                0
           28    LOAD_SMALL_INT        8
                 STORE_FAST            0 (x)
           29    LOAD_FAST_BORROW      0 (x)
                 RETURN_VALUE

        .. tip::

           ``5 + 3`` becomes ``LOAD_SMALL_INT 8``: the compiler optimizes constant expressions!


Alternative Python Implementations
-----------------------------------

.. list-table::
   :widths: 20 80
   :class: compact-table

   * - **PyPy**
     - Written in RPython; uses JIT compilation for 4–10× speedup on long-running code.
   * - **Jython**
     - Compiles to Java bytecode; runs on the JVM; access to Java libraries; no GIL.
   * - **IronPython**
     - Compiles to .NET IL; runs on the CLR; access to .NET libraries; no GIL.
   * - **MicroPython**
     - Optimized for microcontrollers (ESP32, Raspberry Pi Pico); minimal RAM (~256KB).
   * - **GraalPy**
     - Runs on GraalVM with JIT; polyglot interoperability with other languages.
   * - **Cython**
     - Superset of Python that compiles to C, then to native binaries.

.. list-table::
   :widths: 30 15 55
   :header-rows: 1
   :class: compact-table

   * - Use Case
     - Best Choice
     - Why
   * - General development
     - CPython
     - Best compatibility, largest ecosystem
   * - Performance-critical long-running apps
     - PyPy
     - JIT compilation speeds up hot paths
   * - Integration with Java ecosystem
     - Jython
     - Direct Java library access
   * - Integration with .NET ecosystem
     - IronPython
     - Direct .NET library access
   * - Embedded systems / IoT
     - MicroPython
     - Minimal footprint, hardware access
   * - Data science / ML
     - CPython
     - NumPy, pandas, TensorFlow require C extensions


Introduction to Python Variables
====================================================

A preview of Python fundamentals — covered in depth next week.

Create a file called ``variables_demo.py`` to follow along with the examples below.


What is a Variable?
-------------------

.. card::
    :class-card: sd-border-primary sd-shadow-sm

    **Variables in Python**

    - A **variable** is a name that refers to a value stored in memory.
    - Variables are created using the **assignment operator** (``=``).
    - No need to declare the type — Python figures it out automatically.

.. tab-set::

    .. tab-item:: 🐍 Python (Dynamic)

        .. code-block:: python

           # No type declaration needed
           name = "Alice"
           age = 25
           gpa = 3.85
           is_student = True

    .. tab-item:: ⚙️ C++ (Static)

        .. code-block:: cpp

           // Must declare types
           std::string name = "Alice";
           int age = 25;
           double gpa = 3.85;
           bool is_student = true;

.. note::

   Python is **dynamically typed** — variable types are determined at runtime, not compile time.


Assignment Styles
-----------------

The assignment operator (``=``) binds a name to an object.

.. code-block:: python

   # Standard assignment
   name = "Guido van Rossum"

   # Chained assignment (same object, multiple names)
   x = y = 10

   # Multiple assignment (unpacking)
   name, age, role = "Guido van Rossum", 64, "BDFL Emeritus"

   # Swapping values (no temp variable needed!)
   a, b = 1, 2
   a, b = b, a  # a=2, b=1


Everything is an Object
-----------------------

In Python, **everything is an object**. Variables are references (names) bound to objects in memory, not direct storage locations.

.. code-block:: python

   x = 2

- ``x`` is a **name** (reference)
- ``2`` is an **object** in memory
- The name ``x`` is bound to the object ``2``

.. code-block:: python

   print(type(10))       # <class 'int'>
   print(type(3.14))     # <class 'float'>
   print(type("hello"))  # <class 'str'>
   print(type(print))    # <class 'builtin_function_or_method'>


Object Identity
---------------

Every object has a unique identity — an integer representing its memory address. Use ``id()`` to inspect it.

.. code-block:: python

   a = 10
   b = 10.5
   c = "hello"

   print(id(a))  # e.g., 9793376
   print(id(b))  # e.g., 140409546886992
   print(id(c))  # e.g., 140409536180784

   # What about literals?
   print(id(10))      # Same as id(a)?
   print(id("hello")) # Same as id(c)?

.. warning::

   The actual ``id()`` values change each time you run the program, but they remain constant for each object during its lifetime.


Dynamic Typing
--------------

**What is Dynamic Typing?**

- The type is associated with the **value (object)**, not the variable name.
- A variable can be rebound to objects of different types during execution.
- Types are checked at **runtime**, not compile time.

**Variable Rebinding:**

.. code-block:: python

   x = "hello"
   print(type(x))  # <class 'str'>

   x = 10.5
   print(type(x))  # <class 'float'>

.. warning::

   While flexible, rebinding to different types can lead to bugs. We'll discuss **type hints** in L2 to make code safer.


Basic Data Types
----------------

.. list-table::
   :widths: 12 10 20 30 8
   :header-rows: 1
   :class: compact-table

   * - Category
     - Type
     - Examples
     - Notes
     - Mutable
   * - Numeric
     - ``int``
     - ``42``, ``-7``, ``0``
     - Unlimited precision
     - No
   * - Numeric
     - ``float``
     - ``3.14``, ``-0.001``
     - 64-bit (IEEE 754)
     - No
   * - Numeric
     - ``bool``
     - ``True``, ``False``
     - Subclass of ``int``
     - No
   * - Text
     - ``str``
     - ``"hello"``, ``'world'``
     - Immutable sequence
     - No
   * - Null
     - ``NoneType``
     - ``None``
     - Singleton object
     - No
   * - Sequence
     - ``list``
     - ``[1, 2, 3]``
     - Ordered, changeable
     - Yes
   * - Sequence
     - ``tuple``
     - ``(1, 2, 3)``
     - Ordered, unchangeable
     - No
   * - Mapping
     - ``dict``
     - ``{"a": 1}``
     - Key-value pairs
     - Yes
   * - Set
     - ``set``
     - ``{1, 2, 3}``
     - Unordered, unique
     - Yes

.. note::

   We'll cover sequence types (``list``, ``tuple``), mappings (``dict``), and sets in detail in L3.


Mutable vs. Immutable Objects
------------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🔒 Immutable Objects
        :class-card: sd-border-info

        - Cannot be changed after creation
        - Modifying creates a **new** object
        - Examples: ``int``, ``float``, ``str``, ``tuple``

        .. code-block:: python

           x = 10
           print(id(x))  # 9793376

           x = x + 1     # New object created!
           print(id(x))  # 9793408 (different)

    .. grid-item-card:: 🔓 Mutable Objects
        :class-card: sd-border-info

        - Can be changed in place
        - Same object, modified content
        - Examples: ``list``, ``dict``, ``set``

        .. code-block:: python

           my_list = [1, 2, 3]
           print(id(my_list))  # 140234567890

           my_list.append(4)   # Same object!
           print(id(my_list))  # 140234567890 (same)

.. important::

   Understanding mutability is crucial for avoiding bugs when passing objects to functions or assigning variables.


Variables are References
------------------------

**Aliasing: Multiple Names, Same Object**

When you assign one variable to another, both names reference the **same object**.

.. code-block:: python

   a = [1, 2, 3]
   b = a  # b references same list

   print(id(a))  # e.g., 140234567890
   print(id(b))  # Same address!
   print(a is b) # True

   b.append(4)
   print(a)  # [1, 2, 3, 4] -- both changed!

.. warning::

   This behavior with mutable objects is a common source of bugs! To create an independent copy, use ``b = a.copy()`` or ``b = list(a)``.


The ``None`` Type
------------------

.. card::
    :class-card: sd-border-secondary sd-shadow-sm

    **What is None?**

    - ``None`` represents the **absence of a value** or a null value.
    - It is the sole instance of the ``NoneType`` class: a **singleton**.
    - Common uses: default function arguments, uninitialized variables, indicating "no result".

.. code-block:: python

   # Declaring a variable with no value yet
   result = None

   # Function that doesn't explicitly return anything
   def greet(name):
       print(f"Hello, {name}")

   x = greet("Alice")  # Prints "Hello, Alice"
   print(x)            # None
   print(type(x))      # <class 'NoneType'>

.. important::

   Always use ``is`` (not ``==``) to compare with ``None``:

   ✅ ``if x is None:``

   ❌ ``if x == None:``


Identity vs. Equality
---------------------

**The** ``is`` **vs.** ``==`` **Operators**

- ``==`` compares **values** (equality)
- ``is`` compares **identity** (same object in memory)

.. code-block:: python

   a = [1, 2, 3]
   b = [1, 2, 3]
   c = a

   print(a == b)  # True  (same values)
   print(a is b)  # False (different objects)
   print(a is c)  # True  (same object)

.. tip::

   **Rule of thumb**: Use ``==`` for value comparison. Use ``is`` only for ``None`` checks or when you specifically need identity comparison.


Variable Naming Rules
---------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ✅ Rules (Must Follow)
        :class-card: sd-border-success

        - Must start with letter or underscore
        - Can contain letters, digits, underscores
        - Case-sensitive (``Name`` ≠ ``name``)
        - Cannot be a reserved keyword

        .. code-block:: python

           # Valid names
           my_variable = 1
           _private = 2
           camelCase = 3
           var123 = 5

           # Invalid names
           # 2fast = 10      # starts with digit
           # my-var = 5      # contains hyphen
           # class = "test"  # reserved keyword

    .. grid-item-card:: 📏 Conventions (PEP 8)
        :class-card: sd-border-success

        - ``snake_case`` for variables/functions
        - ``UPPER_CASE`` for constants
        - ``PascalCase`` for classes
        - Be descriptive but concise

        .. code-block:: python

           # Good style (PEP 8)
           student_name = "Alice"
           MAX_RETRIES = 3
           total_count = 0

           # Avoid
           x = "Alice"  # Too vague
           studentName = "Alice"  # camelCase
           STUDENTNAME = "Alice"  # ALL CAPS

.. tip::

   Follow `PEP 8 <https://peps.python.org/pep-0008/>`_ — Python's official style guide. We'll enforce it in assignments.


Reserved Keywords
-----------------

These words have special meaning and **cannot** be used as variable names.

.. code-block:: text

   False     None      True      and       as        assert
   async     await     break     class     continue  def
   del       elif      else      except    finally   for
   from      global    if        import    in        is
   lambda    nonlocal  not       or        pass      raise
   return    try       while     with      yield

.. code-block:: python

   # Check keywords programmatically
   import keyword

   print(keyword.iskeyword("if"))  # True
   print(keyword.iskeyword("hello"))  # False
   print(keyword.kwlist)  # List of all Python keywords

.. note::

   If you accidentally use a keyword as a variable name, Python will raise a ``SyntaxError``.


The ``print()`` Function
-------------------------

The ``print()`` function outputs to the screen. It's a **variadic function**: accepts any number of arguments.

.. code-block:: python

   # Print literals
   print("Hello")          # Hello
   print(3)                # 3
   print(2.4)              # 2.4

   # Print expressions
   print(2 + 3)            # 5
   print("*" * 10)         # **********

   # Multiple arguments (separated by space by default)
   print("Welcome", "to", "ENPM", 605)  # Welcome to ENPM 605

   # Custom separator and end
   print("a", "b", "c", sep="-")        # a-b-c
   print("No newline", end="")          # No newline after


Preview: What's Next in L2
--------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📖 L2: Python Basics — Part I
        :class-card: sd-border-primary

        - Packages and modules
        - Importing (``import``, ``from``)
        - Operators (arithmetic, relational, logical)
        - Boolean type and truth testing
        - String operations and methods
        - Indexing and slicing
        - Control flow (``if``/``elif``/``else``)

    .. grid-item-card:: 📘 L3: Python Basics — Part II
        :class-card: sd-border-primary

        - Lists and list methods
        - Tuples and unpacking
        - Dictionaries
        - Sets
        - Loops (``for``, ``while``)
        - List comprehensions

.. note::

   Today's introduction gives you enough to start experimenting. L2 will build on these concepts systematically.