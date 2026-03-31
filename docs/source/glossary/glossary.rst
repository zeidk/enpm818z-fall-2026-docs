====================================================
Glossary
====================================================

:ref:`A <glossary-a>` · :ref:`B <glossary-b>` · :ref:`C <glossary-c>` · :ref:`D <glossary-d>` · :ref:`E <glossary-e>` · :ref:`F <glossary-f>` · :ref:`G <glossary-g>` · :ref:`H <glossary-h>` · :ref:`I <glossary-i>` · :ref:`J <glossary-j>` · :ref:`K <glossary-k>` · :ref:`L <glossary-l>` · :ref:`M <glossary-m>` · :ref:`N <glossary-n>` · :ref:`O <glossary-o>` · :ref:`P <glossary-p>` · :ref:`Q <glossary-q>` · :ref:`R <glossary-r>` · :ref:`S <glossary-s>` · :ref:`T <glossary-t>` · :ref:`U <glossary-u>` · :ref:`V <glossary-v>` · :ref:`W <glossary-w>`

----


.. _glossary-a:

A
=

.. glossary::

   Abstract Class
      A class that cannot be instantiated directly and is designed to be
      subclassed. Defined by inheriting from ``ABC`` (or setting
      ``ABCMeta`` as the metaclass). May contain both abstract methods
      (which subclasses must override) and concrete methods (which are
      inherited as-is). Shown in UML with an italicized name and a
      circled **A** marker.

   Abstract Method
      A method declared with the ``@abstractmethod`` decorator inside an
      abstract class. It has no required implementation in the base class
      (the body is typically ``pass`` or ``...``). Any concrete subclass
      that does not implement all abstract methods cannot be instantiated.
      Python raises a ``TypeError`` at instantiation time, catching the
      omission early.

   Abstraction
      The principle of hiding complex implementation details behind a
      simple interface. Users interact with an object through its public
      methods without needing to know how those methods work internally.
      Example: calling ``robot.move("north")`` without knowing about motor
      controllers or path planning.

   Action
      A ROS 2 communication primitive for long-running, interruptible
      tasks. Unlike a service, an action provides continuous **feedback**
      while executing and a final **result** when complete. The client
      can cancel the goal at any time. Defined in ``.action`` files
      containing a goal, result, and feedback section. Example use:
      navigating a robot to a goal pose.

   Aggregation
      A "has-a" relationship where the contained object (the part) can
      exist independently of the container (the whole). Parts are created
      outside the container and passed in. Example: a ``Team`` has
      ``Robot``\(s), but dissolving the team does not destroy the robots.
      Represented in UML by a hollow diamond on the container side.

   Aliasing
      When two or more variable names refer to the same object in memory.
      Modifying the object through one name affects all aliases. Use
      ``.copy()`` or constructor calls to create independent copies.

   ament_python
      The build type used with ``ros2 pkg create`` for pure-Python
      ROS 2 packages. Relies on ``setuptools`` and ``setup.py`` for
      installation. Contrast with ``ament_cmake``, which is used for
      C++ packages.

   Argument
      A value passed to a function when it is called. Arguments are
      assigned to the function's parameters. Python supports positional
      arguments, keyword arguments, and unpacking with ``*`` and ``**``.

   ``*args``
      A parameter prefix that collects any extra positional arguments
      into a tuple. Defined as ``*args`` in the function signature.
      Example: ``def func(*args):`` allows ``func(1, 2, 3)`` where
      ``args`` is ``(1, 2, 3)``.

   Arithmetic Operator
      An operator that performs mathematical computation. Python's
      arithmetic operators are ``+``, ``-``, ``*``, ``/`` (true
      division), ``//`` (floor division), ``%`` (modulus), and ``**``
      (exponentiation).

   AST
   Abstract Syntax Tree
      A tree representation of the syntactic structure of source code
      produced by the parser. Each node represents a construct in the
      language (e.g., assignment, binary operation). Python exposes this
      through the :mod:`ast` module.

   Assignment Operator
      The ``=`` symbol in Python, which binds a name (variable) to an
      object. Unlike in some languages, ``=`` does not copy a value into
      a memory location -- it creates a reference from the name to the
      object.

   Association
      A general relationship between two objects where one object holds a
      reference to another for a period of time. Neither object owns the
      other, and both can exist independently. Can be unidirectional (only
      one class knows about the other) or bidirectional. Example: a
      ``Robot`` is assigned a ``Task``; the task exists before and after
      the robot executes it. The associated object is passed in as a
      parameter, not created inside the class.

   Augmented Assignment
      A shorthand that combines an arithmetic operation with
      assignment, e.g., ``x += 5`` is equivalent to ``x = x + 5``.
      Other forms include ``-=``, ``*=``, ``/=``, ``//=``, ``%=``,
      and ``**=``.


.. _glossary-b:

B
=

.. glossary::

   Base Case
      The condition in a recursive function that stops the recursion.
      Without a base case, the function will recurse until Python raises
      a ``RecursionError``. Example: ``if n <= 1: return 1`` in a
      factorial function.

   Behavior Tree
      A tree-structured model for task execution used in robotics and
      game AI. In this course, students build application-level behavior
      trees with the *py_trees* library to coordinate Nav2 navigation
      actions.

   bool
      Python's Boolean type, a subclass of ``int`` with exactly two
      instances: ``True`` (``1``) and ``False`` (``0``). The built-in
      ``bool()`` function converts any value to a Boolean using
      :term:`truthiness <Truthy>` rules.

   break
      A statement that immediately exits the innermost enclosing ``for``
      or ``while`` loop. When ``break`` executes, any ``else`` clause
      attached to the loop is skipped.

   Built-in Scope
      The outermost scope in the LEGB rule, containing Python's
      pre-defined names such as ``print``, ``len``, ``int``, ``True``,
      and ``None``. These are defined in the ``builtins`` module.

   Business Rule
      A constraint, trigger, or computation that the system must enforce
      as part of domain logic. Business rules directly influence class
      design by determining which validations go into methods, which
      attributes need constraints, and which relationships must be
      enforced. Identified with prefixes: BR-C (constraint), BR-T
      (trigger), BR-D (computation).

   Bytecode
      A low-level, platform-independent set of instructions generated by
      the Python compiler from the AST. Stored in ``.pyc`` files inside
      ``__pycache__/`` for imported modules. Executed by the interpreter
      loop.


.. _glossary-c:

C
=

.. glossary::

   Callback
      A function passed as an argument to another function, or registered
      with a framework, to be called at a later time. In Python generally,
      callbacks are used in event-driven programming. In ROS 2 specifically,
      a callback is registered with the executor and invoked automatically
      when a triggering event occurs -- an incoming topic message, a timer
      expiration, a service request, or an action goal. Callbacks only
      execute while the node is spinning and should be kept fast; a slow
      callback blocks the executor and starves other pending callbacks.

   Callable
      Any object that can be invoked using parentheses ``()``. In Python,
      callables include functions defined with ``def``, lambda expressions,
      classes (calling a class creates an instance), instances with a
      ``__call__`` method, and built-in functions. Use ``callable(obj)``
      to check.

   Call Stack
      The data structure Python uses to track active function calls. Each
      function call creates a frame object that is pushed onto the stack.
      When the function returns, its frame is popped. The stack enables
      nested and recursive function calls.

   CamelCase
      A naming convention where each word starts with a capital letter
      and no underscores are used. In Python, class names follow
      CamelCase by convention (e.g., ``RobotArm``, ``SensorFusion``),
      while functions and variables use ``snake_case``.

   Cell Object
      An internal CPython mechanism used to share variables between
      enclosing and nested functions. Cell objects are mutable containers
      that hold a single reference, enabling the ``nonlocal`` keyword
      to work across scope boundaries.

   Chained Assignment
      Binding multiple names to the same object in a single statement,
      e.g., ``x = y = 10``. All names reference the identical object.

   Chained Comparison
      A Python feature that allows multiple relational operators in a
      single expression, e.g., ``1 < x < 10`` is equivalent to
      ``1 < x and x < 10``. Each operand is evaluated at most once.

   Class
      A blueprint that defines the attributes (data) and methods
      (functions) that its objects will have. Defined using the ``class``
      keyword followed by the name in CamelCase. In Python 3, all
      classes implicitly inherit from ``object``.

   Class Attribute
      An attribute defined inside the class body but outside any method.
      Shared by all instances of the class. Accessed via the class name
      (``ClassName.attr``) or via any instance. Commonly used for
      constants and counters (e.g., ``total_robots``).

   Class Method
      A method defined with the ``@classmethod`` decorator. It receives
      the class itself as its first argument (conventionally named
      ``cls``) rather than an instance. Class methods can access and
      modify class-level state and are commonly used as factory methods
      or alternative constructors. Calling ``cls(...)`` inside a class
      method ensures correct behavior in subclasses.

   Closure
      A function that retains access to variables from its enclosing
      scope, even after the enclosing function has finished executing.
      Three conditions are required: a nested function, a reference to a
      free variable from the enclosing scope, and the enclosing function
      returning the nested function. The captured variables are stored in
      cell objects accessible via ``__closure__``.

   Code Smell
      A surface-level indicator in source code that suggests a deeper
      problem. The term was coined by Martin Fowler in *Refactoring:
      Improving the Design of Existing Code*. Linters like Ruff detect
      common code smells automatically.

   colcon
      The official build tool for ROS 2 (collective construction). It
      replaces the ROS 1 build tools (``catkin_make``, ``catkin build``).
      Builds all packages found under ``src/``, supports parallel builds,
      and produces ``build/``, ``install/``, and ``log/`` directories.
      Key flags: ``--symlink-install`` (links Python files instead of
      copying), ``--packages-select <pkg>`` (builds one package only).

   Compiled Language
      A language whose source code is translated directly into native
      machine code by a compiler before execution. Examples: C, C++,
      Rust, Go.

   Comprehension
      A concise syntax for creating collections by transforming and/or
      filtering elements from an iterable. Python supports list
      comprehensions (``[x for x in iter]``), dictionary comprehensions
      (``{k: v for k, v in iter}``), set comprehensions
      (``{x for x in iter}``), and generator expressions
      (``(x for x in iter)``).

   Composition
      A "has-a" relationship where the contained objects (the parts)
      cannot exist independently of the container (the whole). Parts are
      created inside the container's ``__init__`` and their lifetime is
      tied to the whole. Example: a ``Robot`` owns its ``Sensor``\(s);
      destroying the robot destroys its sensors. Represented in UML by a
      filled diamond on the container side.

   Concatenation
      Joining strings end-to-end. In Python, use the ``+`` operator
      for a small number of strings or ``str.join()`` for joining
      many strings efficiently.

   Concrete Class
      A class that provides implementations for all abstract methods it
      inherits and can therefore be instantiated directly. Shown in UML
      with a circled **C** marker.

   Conditional Expression
   Ternary Expression
      A single-line ``if``/``else`` construct that produces a value:
      ``value_if_true if condition else value_if_false``. Useful for
      simple assignments but should not replace multi-line ``if``
      blocks for complex logic.

   Container
      A lightweight, isolated environment that packages an application
      with its dependencies. In this course, Docker containers ensure
      a consistent development environment across platforms. See also
      :term:`Docker`, :term:`Dev Containers`.

   continue
      A statement that skips the rest of the current loop iteration and
      proceeds to the next iteration. Unlike ``break``, the loop
      continues running.

   CPython
      The reference (default) implementation of Python, written in C.
      When you run ``python3``, you are running CPython. It compiles
      source code to :term:`bytecode` and executes it via an evaluation
      loop. CPython 3.14 introduces officially supported free-threaded
      builds (``python3.14t``).

   Cython
      A superset of Python that compiles to C, then to native machine
      code. Used to write high-performance C extensions with
      Python-like syntax.


.. _glossary-d:

D
=

.. glossary::

   Data Class
      A class decorated with ``@dataclass`` (from the ``dataclasses``
      module, introduced in Python 3.7) that auto-generates ``__init__``,
      ``__repr__``, and ``__eq__`` from its type-annotated fields. Type
      hints are required; fields without annotations are ignored. Supports
      default values, mutable defaults via ``field(default_factory=...)``,
      post-initialization logic via ``__post_init__``, and immutable
      variants via ``frozen=True``. Best suited to classes whose primary
      purpose is storing data.

   DDS (Data Distribution Service)
      An open, data-centric publish-subscribe middleware standard managed
      by the Object Management Group (OMG). DDS is the communication
      layer beneath ROS 2. It provides decentralized discovery,
      transport-independent messaging (UDP, TCP, shared memory), and
      fine-grained QoS control. The underlying wire protocol is RTPS
      (Real-Time Publish-Subscribe). Common ROS 2 implementations include
      Fast DDS (eProsima), Cyclone DDS (Eclipse), and Connext DDS (RTI).

   Deep Copy
      A copy operation that recursively duplicates all nested objects,
      creating a completely independent copy. Performed using
      ``copy.deepcopy()``. Contrast with :term:`Shallow Copy`.

   Default Argument
      A parameter value specified in the function definition that is used
      when the caller does not provide that argument. Default values are
      evaluated once at definition time, not at each call. Mutable
      defaults (like lists) should be avoided; use ``None`` instead.

   Default Value Pattern
      A common Python idiom using ``or`` to provide fallback values:
      ``name = user_input or "Anonymous"``. When ``user_input`` is
      empty or falsy, ``"Anonymous"`` is assigned instead.

   Design Phase
      The process of translating a real-world problem into a workable
      software structure before writing any code. Includes requirement
      analysis, business rules, noun/verb analysis, UML modeling, and
      implementation planning.

   Design Smell
      A sign in your code that something is structurally wrong with your
      design, even if the code technically works. Not a bug -- the program
      runs -- but the design will cause problems as the codebase grows.
      Analogous to "code smell" but applied at the class and relationship
      level. Classic example: a base class carrying ``None`` values for
      attributes that only apply to some subclasses, signaling that
      specialization is needed.

   Dev Containers
      A VS Code feature that allows development inside a Docker
      container. The ``ms-vscode-remote.remote-containers`` extension
      opens a project folder in a containerized environment with all
      dependencies pre-installed.

   Decorator
      A function that takes another function as input, adds functionality,
      and returns a new function (or the same function modified). The
      ``@decorator`` syntax placed above a function definition is syntactic
      sugar for ``func = decorator(func)``. Decorators are used for
      cross-cutting concerns such as logging, timing, access control, and
      caching.

   Decorator Factory
      A function that accepts arguments and returns a decorator. Used when
      a decorator itself needs to be parameterized. Requires three levels
      of nesting: ``factory(args) -> decorator(func) -> wrapper(*args, **kwargs)``.
      Example: ``@repeat(3)`` where ``repeat`` is the factory.

   Dictionary
   dict
      A mutable mapping type that stores key-value pairs. Keys must be
      :term:`hashable <Hashable>`. Since Python 3.7, dictionaries
      maintain insertion order. Access values with ``d[key]`` or
      ``d.get(key)``.

   Dictionary Comprehension
      A concise syntax for creating dictionaries:
      ``{key_expr: val_expr for item in iterable if condition}``.
      Returns a new ``dict`` object.

   Difference
      A set operation returning elements in the first set but not in
      the second. Performed with ``-`` operator or ``.difference()``
      method. ``{1, 2, 3} - {2, 3, 4}`` returns ``{1}``.

   Dispatch Table
      A dictionary that maps keys (such as strings) to functions. Used to
      select and call a function based on a runtime value, replacing long
      ``if``/``elif`` chains. Example:
      ``operations = {"add": add, "multiply": multiply}``.

   Docstring
      A string literal that appears as the first statement in a function,
      class, or module. Used to document the purpose, parameters, and
      return value. Accessible at runtime via ``func.__doc__``. This
      course uses Google-style docstrings with ``Args`` and ``Returns``
      sections.

   Docker
      A platform for building and running :term:`containers <Container>`.
      Docker Desktop provides a GUI and CLI (``docker``) for managing
      containers on Windows, macOS, and Linux.

   Dot Notation
      The syntax used to access attributes and methods on an object:
      ``obj.attribute`` or ``obj.method()``. Python uses dot notation for
      all member access.

   Duck Typing
      The runtime mechanism Python uses to achieve polymorphism. An object
      is compatible with an interface if it has the required methods,
      regardless of its type or class hierarchy. The name comes from the
      saying: "If it walks like a duck and quacks like a duck, then it
      must be a duck." Python checks what an object can do, not what it
      is. Duck typing is flexible but provides no compile-time guarantee;
      abstract base classes and protocols add that safety net.

   Dunder Method
      A Python method with double leading and trailing underscores (e.g.,
      ``__init__``, ``__str__``, ``__add__``). Dunder methods enable
      operator overloading and integration with built-in functions.
      "Dunder" is short for "double underscore."

   Durability (QoS)
      A QoS policy that controls whether messages are cached for
      late-joining subscribers. ``TRANSIENT_LOCAL`` retains the last
      published message and delivers it to any subscriber that connects
      after the fact. ``VOLATILE`` (default) discards messages
      immediately if no matching subscriber is currently connected.

   Dynamic Typing
      A type system where the type is associated with the value (object),
      not the variable name. A variable can be rebound to objects of
      different types during execution. Types are checked at runtime.


.. _glossary-e:

E
=

.. glossary::

   Editable Install
      Installing a Python package in development mode using
      ``pip install -e .``. Changes to the source code take effect
      immediately without reinstalling. Requires a ``pyproject.toml``
      file. The most portable and professional approach for making
      packages discoverable.

   Encapsulation
      The bundling of data (attributes) with the methods that operate on
      that data, while restricting direct access to internal state. In
      Python, encapsulation is achieved by convention: prefix non-public
      attributes with an underscore (``_attr``) and provide controlled
      access through ``@property`` decorators.

   Enclosing Scope
      The scope of an outer function when using nested functions. In the
      LEGB rule, Python checks the enclosing scope after the local scope.
      Variables in the enclosing scope can be read by inner functions and
      modified using the ``nonlocal`` keyword.

   Entry Point
      A mapping in ``setup.py`` (under ``console_scripts``) that
      associates a command name with a Python function. The format is
      ``'<command> = <module>:<function>'``. After building the
      workspace, ``ros2 run <pkg> <command>`` invokes that function.
      A new ``colcon build`` is required after adding or changing entry
      points.

   enumerate()
      A built-in function that returns an iterator of tuples, each
      containing an index and the corresponding value from an iterable.
      ``enumerate(["a", "b"], start=1)`` yields ``(1, "a"), (2, "b")``.
      More Pythonic than ``range(len(...))``.

   Equality
      Comparison of **values** using the ``==`` operator. Two distinct
      objects can be equal if they contain the same data. Contrast with
      :term:`Identity`.

   Escape Sequence
      A backslash-prefixed character combination inside a string
      literal that represents a special character, e.g., ``\n``
      (newline), ``\t`` (tab), ``\\`` (literal backslash), ``\"``
      (literal double quote). Suppressed by using a raw string
      (``r"..."``).

   Executor
      The ROS 2 component responsible for managing the spin loop and
      dispatching callbacks to threads. When you call
      ``rclpy.spin(node)``, ROS 2 creates a default single-threaded
      executor internally and hands it your node. The executor maintains
      a queue of pending callbacks and dispatches them one by one.
      Multiple nodes can be added to one executor.

   else Clause (Loop)
      An optional clause after a ``for`` or ``while`` loop that executes
      only if the loop completes normally (without ``break``). Useful
      for search patterns where you need to know if an item was found.


.. _glossary-f:

F
=

.. glossary::

   Factory Method
      A class method that constructs and returns a new instance with a
      predefined or computed configuration. Uses ``cls(...)`` rather than
      the class name directly, so the factory works correctly in
      subclasses. Example: ``Robot.create_scout()`` returns a ``Robot``
      configured as a scout without the caller needing to know the default
      values. Factory methods can also return collections of instances.

   Falsy
      A value that evaluates to ``False`` when passed to ``bool()``.
      Python's falsy values are: ``0``, ``0.0``, ``""``, ``[]``,
      ``()``, ``{}``, ``set()``, ``None``, and ``False`` itself.
      Contrast with :term:`Truthy`.

   First-Class Object
      An entity that can be assigned to a variable, passed as an argument,
      returned from a function, and stored in a data structure. In Python,
      functions are first-class objects, which means they can be
      manipulated like any other value (integers, strings, lists).

   Floor Division
      Integer division that rounds toward negative infinity, performed
      by the ``//`` operator. ``10 // 3`` is ``3``; ``10 // -3`` is
      ``-4`` (not ``-3``).

   for Loop
      A control structure that iterates over items in an :term:`iterable`.
      Syntax: ``for item in iterable:``. The loop variable takes each
      value from the iterable in turn.

   Formatter
      A tool that automatically rewrites source code to conform to a
      consistent style (indentation, spacing, line length). Ruff and
      Black are popular Python formatters.

   Frame Object
      A heap-allocated ``PyFrameObject`` struct created by CPython for
      each function call. Contains the local variables array
      (``f_localsplus``), a pointer to the globals dictionary
      (``f_globals``), the builtins dictionary (``f_builtins``), and a
      back-pointer to the caller's frame (``f_back``).

   Free Variable
      A variable referenced inside a function that is not defined in that
      function's local scope. In the context of closures, free variables
      are defined in the enclosing function's scope and captured by the
      inner function via cell objects.

   fromkeys()
      A ``dict`` class method that creates a new dictionary with keys
      from an iterable and all values set to a specified default.
      ``dict.fromkeys(["a", "b"], 0)`` returns ``{"a": 0, "b": 0}``.

   Frozen Data Class
      A data class created with ``@dataclass(frozen=True)``. All fields
      are immutable after construction; any attempt to assign to a field
      raises ``FrozenInstanceError``. Frozen instances are hashable and
      can be used as dictionary keys or set members. Suitable for records
      that should never change after creation, such as sensor readings or
      event logs.

   f-string
   Formatted String Literal
      A string literal prefixed with ``f`` or ``F`` that allows embedded
      Python expressions inside curly braces: ``f"Hello, {name}"``.
      Introduced in Python 3.6. Supports format specifiers such as
      ``.2f`` (two decimal places) and ``>20`` (right-align in 20
      characters).

   ``functools.partial``
      A function from the ``functools`` module that creates a new callable
      with some arguments of the original function pre-filled ("frozen").
      The returned partial object has ``.func``, ``.args``, and
      ``.keywords`` attributes for introspection.

   ``functools.wraps``
      A decorator from the ``functools`` module that copies metadata
      (``__name__``, ``__doc__``, ``__module__``, ``__qualname__``,
      ``__annotations__``, ``__dict__``, ``__wrapped__``) from the
      original function onto a wrapper function. Essential for preserving
      introspection in decorators.

   Function
      A named, reusable block of code defined with the ``def`` keyword.
      Functions accept input through parameters, execute a body of
      statements, and optionally return a value. They are first-class
      objects in Python.

   Functional Programming
      A programming paradigm that expresses computation as the evaluation
      of mathematical functions. Emphasizes pure functions, immutability,
      avoiding side effects, and higher-order functions. Python supports
      functional programming alongside procedural and object-oriented
      styles.


.. _glossary-g:

G
=

.. glossary::

   Gazebo Harmonic
      A robotics simulation environment used in this course. Students
      build and test robot behaviors in Gazebo before deploying to
      real hardware.

   Generalization
      A bottom-up design activity in which common attributes and behaviors
      shared by multiple classes are identified and moved into a new shared
      base class. The result is a parent class that captures what all
      subclasses have in common, reducing duplication. Contrast with
      specialization.

   GIL
   Global Interpreter Lock
      A mutex in :term:`CPython` that allows only one thread to execute
      Python bytecode at a time. Limits true multi-threaded parallelism
      for CPU-bound tasks. CPython 3.13+ offers experimental
      free-threaded builds without the GIL.

   Global Scope
      The module-level scope containing variables defined outside of any
      function. In the LEGB rule, Python checks the global scope after
      local and enclosing scopes. The ``global`` keyword allows a
      function to modify variables in this scope.

   ``global`` Keyword
      A statement that declares a variable inside a function as referring
      to the module-level (global) variable of the same name. Without it,
      assignment inside a function creates a new local variable.

   GraalPy
      A Python implementation running on GraalVM with JIT compilation
      and polyglot interoperability with other languages (Java,
      JavaScript, Ruby, etc.).


.. _glossary-h:

H
=

.. glossary::

   Hashable
      An object is hashable if it has a hash value that never changes
      during its lifetime and can be compared to other objects.
      Immutable built-in types (``int``, ``str``, ``tuple``) are
      hashable. Mutable types (``list``, ``dict``, ``set``) are not.
      Only hashable objects can be dictionary keys or set elements.

   Higher-Order Function
      A function that takes one or more functions as arguments, returns a
      function, or both. Built-in examples include ``map``, ``filter``,
      and ``sorted`` (with its ``key`` parameter). Decorators are also
      higher-order functions.


.. _glossary-i:

I
=

.. glossary::

   Identity
      The unique integer (memory address) associated with every Python
      object, returned by ``id()``. Two names have the same identity
      only if they reference the exact same object. Tested with the
      ``is`` operator. Contrast with :term:`Equality`.

   Identity Operator
      The ``is`` and ``is not`` operators, which test whether two
      names reference the exact same object in memory (same ``id``).
      Use ``is`` only for :term:`None` checks; use ``==`` for value
      comparison.

   Immutable
      An object that cannot be changed after creation. Operations that
      appear to modify an immutable object actually create a new object.
      Examples: ``int``, ``float``, ``str``, ``tuple``, ``bool``,
      ``NoneType``.

   Immutability
      The property of an object whose state cannot be changed after
      creation. In functional programming, immutability is preferred
      because it eliminates side effects and makes code easier to reason
      about. Python's built-in immutable types include ``int``, ``str``,
      ``tuple``, and ``frozenset``.

   import
      A statement that makes names from another :term:`module <Module>`
      or :term:`package <Package>` available in the current namespace.
      Common forms: ``import math``, ``from math import sqrt``,
      ``import math as m``.

   In-Place Operation
      An operation that modifies an object directly rather than creating
      a new object. List methods like ``append()``, ``sort()``, and
      ``reverse()`` are in-place and return ``None``. Contrast with
      :term:`Out-of-Place Operation`.

   Indentation
      Whitespace at the beginning of a line that defines a code block
      in Python. PEP 8 prescribes **4 spaces** per level. Mixing tabs
      and spaces causes ``IndentationError``.

   Inheritance
      A mechanism that allows a class (the child or derived class) to
      reuse and extend the attributes and methods of another class (the
      parent or base class). Represents an "is-a" relationship. Python
      supports single, multi-level, multiple, and hierarchical inheritance.
      The child uses ``super().__init__()`` to delegate parent attribute
      initialization. Prefer composition over inheritance when the
      relationship is "has-a" rather than "is-a".

   Instance
      A concrete realization of a class, also called an object. Created
      by calling the class as if it were a function:
      ``obj = ClassName(args)``. Each instance has its own attribute
      values and operates independently of other instances.

   Instance Attribute
      An attribute that belongs to a specific object. Created inside
      ``__init__`` using ``self.attr = value``. Each instance maintains
      its own copy, so modifying one instance does not affect others.

   Instance Method
      A standard method that receives the instance as its first argument
      (conventionally named ``self``). Has access to both instance state
      and class state. The most common method type in Python. Contrast
      with class methods and static methods.

   Integer Cache
      A CPython implementation detail where small integers (typically
      ``-5`` through ``256``) are pre-allocated and reused. Two
      variables assigned the same small integer may share the same
      ``id()``. Do not rely on this behavior in production code.

   IntelliSense
      A code-completion and assistance feature in Visual Studio Code
      that provides context-aware suggestions, parameter hints, and
      documentation as you type.

   Interface (ROS 2)
      A typed data contract shared between nodes. Defined in plain-text
      ``.msg`` (messages), ``.srv`` (services), or ``.action`` (actions)
      files. At build time these files are compiled into
      language-specific Python and C++ code. The same ``.msg`` file
      generates Python, C++, and other bindings -- publishers and
      subscribers must use the same interface type to communicate.

   Interning
      A CPython optimization that reuses the same object for small
      integers (typically ``-5`` through ``256``) and compile-time
      string constants. Never rely on interning for correctness.

   Interpreted Language
      A language whose source code is compiled to intermediate
      :term:`bytecode` and executed by an interpreter rather than
      directly by the CPU. Python, JavaScript, and Ruby are interpreted
      languages.

   Intersection
      A set operation returning elements present in both sets. Performed
      with ``&`` operator or ``.intersection()`` method.
      ``{1, 2, 3} & {2, 3, 4}`` returns ``{2, 3}``.

   IronPython
      A Python implementation that compiles to .NET Intermediate
      Language (IL) and runs on the Common Language Runtime (CLR).
      Provides access to .NET libraries and does not have a
      :term:`GIL`.

   Iterable
      Any object capable of returning its elements one at a time. This
      includes sequences (lists, strings, tuples), mappings
      (dictionaries), sets, files, and generators. An iterable can be
      used in a ``for`` loop or passed to functions like ``list()``,
      ``sum()``, or ``enumerate()``.

   Iterator
      An object representing a stream of data that returns successive
      items via the ``__next__()`` method. Iterators remember their
      position in the data stream. All iterators are iterables, but
      not all iterables are iterators.

   ``__init__``
      A special dunder method called automatically when a new instance is
      created. Used to initialize the object's attributes. It is an
      initializer, not a constructor; the actual constructor is
      ``__new__``, which is rarely overridden.


.. _glossary-j:

J
=

.. glossary::

   JIT Compilation
   Just-In-Time Compilation
      A technique where bytecode is compiled to native machine code at
      runtime, typically for frequently executed ("hot") code paths.
      :term:`PyPy` uses JIT compilation to achieve significant speedups
      over :term:`CPython`.

   Jython
      A Python implementation that compiles to Java bytecode and runs on
      the Java Virtual Machine (JVM). Provides direct access to Java
      libraries and does not have a :term:`GIL`.


.. _glossary-k:

K
=

.. glossary::

   Key (Dictionary)
      The identifier used to access a value in a dictionary. Keys must
      be :term:`hashable <Hashable>` (immutable). Common key types are
      strings, integers, and tuples.

   Keyword Argument
      An argument passed to a function by explicitly naming the
      parameter: ``func(name="Alice")``. Keyword arguments can appear in
      any order and make function calls more readable.

   ``**kwargs``
      A parameter prefix that collects any extra keyword arguments into
      a dictionary. Defined as ``**kwargs`` in the function signature.
      Example: ``def func(**kwargs):`` allows ``func(x=1, y=2)`` where
      ``kwargs`` is ``{'x': 1, 'y': 2}``.


.. _glossary-l:

L
=

.. glossary::

   Lambda
      A small anonymous function defined with the ``lambda`` keyword.
      Limited to a single expression (no statements, no multi-line logic,
      no docstrings, no type hints). Commonly used as short inline
      callbacks for ``sorted(key=...)``, ``map``, and ``filter``. PEP 8
      discourages assigning lambdas to variable names.

   Launch File
      A Python script (``*.launch.py``) that starts multiple ROS 2
      nodes from a single command using ``ros2 launch``. All node output
      appears in one terminal, prefixed by node name. A single Ctrl-C
      stops the entire system. Preferred over ``ros2 run`` for
      integration testing and running a complete system.

   Lazy Evaluation
      A strategy where values are computed only when needed. ``range()``
      uses lazy evaluation -- it doesn't store all values in memory but
      generates them on demand. This makes ``range(1000000000)`` use
      the same memory as ``range(10)``.

   Lazy Iterator
      An object that produces values one at a time on demand rather than
      computing all values upfront. ``map`` and ``filter`` return lazy
      iterators in Python 3. Wrap in ``list()`` to materialize all
      results.

   LEGB Rule
      The order in which Python resolves variable names: Local, Enclosing,
      Global, Built-in. Python searches each scope in this order and uses
      the first match found. This is the fundamental mechanism for
      variable name resolution in Python.

   Lexer
   Tokenizer
      The first stage of the Python execution pipeline. Breaks source
      code into a stream of tokens (keywords, identifiers, operators,
      literals, etc.). Python exposes this through the :mod:`tokenize`
      module.

   Linter
      A static analysis tool that scans source code for potential errors,
      style violations, and :term:`code smells <Code Smell>` without
      executing the code. The name originates from the ``lint`` tool for
      C (1978). See also :term:`Ruff`.

   List
      A mutable, ordered sequence of objects. Created with square
      brackets ``[1, 2, 3]`` or the ``list()`` constructor. Elements
      can be of any type, including other lists (nested lists).

   List Comprehension
      A concise syntax for creating lists:
      ``[expression for item in iterable if condition]``. More readable
      and often faster than equivalent ``for`` loops with ``append()``.

   Local Scope
      The innermost scope, containing variables defined inside the
      current function (including parameters). Local variables are stored
      in a fast-access array (``f_localsplus``) on the frame object and
      accessed via ``LOAD_FAST``/``STORE_FAST`` bytecode instructions.

   Logical Operator
      The ``and``, ``or``, and ``not`` operators, which combine or
      negate Boolean expressions. Python's logical operators use
      :term:`short-circuit evaluation`. With non-boolean values,
      ``and`` returns the first falsy value (or the last value if all
      truthy), and ``or`` returns the first truthy value (or the last
      value if all falsy). ``not`` always returns a ``bool``.


.. _glossary-m:

M
=

.. glossary::

   Mapping Type
      A container that associates keys with values. The primary mapping
      type in Python is :term:`dict`. Mappings support key-based
      access (``d[key]``) and key membership testing (``key in d``).

   Membership Operator
      The ``in`` and ``not in`` operators, which test whether an
      element exists within a sequence (string, list, tuple, set, or
      dict keys). ``"h" in "hello"`` evaluates to ``True``.

   Message
      A packet of data exchanged over a topic. Defined in ``.msg``
      files as a list of typed fields (IDL primitive types or nested
      message types). Publishers fill and send message objects;
      subscribers receive them in callback functions. Standard message
      packages (``std_msgs``, ``geometry_msgs``, ``sensor_msgs``, etc.)
      ship precompiled with ROS 2.

   Method
      A function defined inside a class that operates on instances of
      that class. The first parameter is conventionally named ``self``,
      which refers to the instance calling the method. Methods are
      invoked using dot notation: ``obj.method(args)``.

   Method Resolution Order (MRO)
      The sequence Python follows when searching for a method or attribute
      in a class hierarchy. Computed using the C3 linearization algorithm,
      which produces a consistent, predictable order that respects the
      hierarchy and never visits the same class twice. In single
      inheritance the MRO is simply the chain from child to parent to
      ``object``. Inspect it via ``ClassName.__mro__``. ``super()`` calls
      the next class in the MRO, not necessarily the direct parent.

   Method Overriding
      When a subclass provides its own implementation of a method that
      already exists in the parent class. The method name and signature
      remain the same; the subclass version replaces the parent version
      when called on a subclass instance. Used to specialize inherited
      behavior. Note: implementing dunder methods such as ``__str__`` or
      ``__eq__`` is overriding (not overloading), because every Python
      class already inherits these from ``object``.

   Middleware
      Software that sits between the operating system and application
      code, providing common services such as communication, discovery,
      and data serialization. In ROS 2, DDS is the middleware layer.
      It handles all network transport, participant discovery, and QoS
      enforcement transparently, so node developers interact only with
      the ``rclpy``/``rclcpp`` API.

   MicroPython
      A Python implementation optimized for microcontrollers (ESP32,
      Raspberry Pi Pico) with minimal RAM requirements (~256 KB).

   Modular Programming
      A software design approach that breaks a program into separate,
      reusable units (:term:`modules <Module>` and :term:`packages
      <Package>`), each responsible for a specific piece of
      functionality.

   Module
      A single ``.py`` file containing functions, classes, and
      variables. Modules are imported with the ``import`` statement
      and are the basic unit of code organization in Python.

   Modulus
      The remainder after floor division, computed by the ``%``
      operator. ``7 % 3`` is ``1``. Useful for checking divisibility
      (``n % 2 == 0`` tests whether ``n`` is even).

   Multiple Assignment
      Binding several names to several values in a single statement
      using tuple unpacking, e.g.,
      ``name, age, role = "Guido", 64, "BDFL"``.

   Mutable
      An object that can be changed in place after creation. The
      object's ``id()`` remains the same even as its contents change.
      Examples: ``list``, ``dict``, ``set``.


.. _glossary-n:

N
=

.. glossary::

   Name Mangling
      A Python mechanism triggered by a double leading underscore
      (``__attr``). Python renames the attribute to
      ``_ClassName__attr`` to reduce the chance of accidental access
      from subclasses. Rarely needed in practice.

   Namespace
      A mapping from names to objects. Every module, function, and
      class has its own namespace. :term:`Wildcard imports
      <Wildcard Import>` pollute the current namespace.

   Namespace Pollution
      When too many names are imported into the current namespace,
      increasing the risk of accidental name collisions. Caused
      primarily by :term:`wildcard imports <Wildcard Import>`.

   Nav2
      The ROS 2 Navigation Stack. Provides autonomous navigation
      capabilities including path planning, obstacle avoidance via
      costmaps, and recovery behaviors. Configured (not written) by
      students; called via action servers from :term:`behavior trees
      <Behavior Tree>`.

   Nested Condition
      An ``if`` statement inside another ``if`` block. While sometimes
      necessary, deeply nested conditions can often be simplified using
      ``elif`` chains or combined Boolean expressions.

   Nested Function
      A function defined inside another function. The inner function has
      access to variables in the enclosing function's scope. Nested
      functions are the foundation for closures and decorators.

   Node
      The fundamental unit of a ROS 2 application. A node is a single
      OS process (or a named entity within a process) that performs one
      specific task. Nodes discover each other automatically via DDS
      and communicate through topics, services, and actions. In Python,
      nodes are typically written as classes that inherit from
      ``rclpy.node.Node``.

   None
      Python's null value -- the sole instance of the ``NoneType``
      class. A :term:`singleton` used to represent the absence of a
      value. Always compare with ``is None``, not ``== None``.

   ``nonlocal`` Keyword
      A statement that declares a variable inside a nested function as
      referring to a variable in the enclosing function's scope. Without
      it, assignment inside the inner function would create a new local
      variable instead of modifying the enclosing one.

   Noun/Verb Analysis
      A technique for extracting candidate classes (nouns) and methods
      (verbs) from a natural-language problem description. Nouns map to
      classes or attributes, verbs map to methods, and relational phrases
      ("has a", "is a") map to composition or inheritance relationships.


.. _glossary-o:

O
=

.. glossary::

   Object
      A concrete realization of a class (synonym for instance). Objects
      bundle data (attributes) and behavior (methods) together. Multiple
      objects can be created from the same class, each with independent
      state.

   Operator Overloading
      A form of polymorphism in which the same operator (``+``, ``==``,
      ``<``, etc.) behaves differently depending on the type of object it
      is applied to. Achieved by implementing the corresponding dunder
      method in the class (e.g., ``__add__`` for ``+``, ``__eq__`` for
      ``==``). See also: method overriding.

   Operator Precedence
      The rules that determine which operator is evaluated first when
      an expression contains multiple operators. In Python (highest to
      lowest): ``**``, unary ``+``/``-``, ``*``/``/``/``//``/``%``,
      ``+``/``-``, comparisons, ``not``, ``and``, ``or``. Use
      parentheses for clarity.

   ``Optional``
      A type hint from the ``typing`` module indicating that a value can
      be of a specified type or ``None``. ``Optional[int]`` is equivalent
      to ``Union[int, None]``. In Python 3.10+, the shorthand
      ``int | None`` can be used instead.

   Out-of-Place Operation
      An operation that returns a new object without modifying the
      original. The built-in ``sorted()`` function is out-of-place,
      returning a new list. String methods are out-of-place because
      strings are :term:`immutable <Immutable>`. Contrast with
      :term:`In-Place Operation`.


.. _glossary-p:

P
=

.. glossary::

   package.xml
      The manifest file for a ROS 2 package. It declares the package
      name, version, license, maintainer, and all build/runtime
      dependencies. ``ament`` reads it to determine build order;
      ``rosdep`` reads it to install missing system dependencies.
      ``package.xml`` and ``setup.py`` must always agree on package
      name and version.

   Package
      A directory containing ``.py`` files (modules) and optionally an
      ``__init__.py`` file. Packages allow hierarchical organization of
      modules, e.g., ``shape.square``.

   Parameterized Decorator
      A decorator that accepts arguments. Implemented as a decorator
      factory: a function that takes the decorator's arguments and returns
      the actual decorator. Uses three nested functions:
      ``factory(args) -> decorator(func) -> wrapper(*args, **kwargs)``.

   Parameter
      A variable listed in a function's definition that receives a value
      when the function is called. Parameters define the function's
      interface. Distinguished from arguments: parameters are in the
      definition, arguments are in the call.

   Parser
      The second stage of the Python execution pipeline. Receives
      tokens from the :term:`lexer` and validates them against Python's
      grammar to produce a parse tree, which is then simplified into
      an :term:`AST`.

   Pass-by-Assignment
      Python's argument-passing mechanism, sometimes called
      "pass-by-object-reference." The function receives a reference to
      the object, not a copy. In-place mutations on mutable objects
      affect the original; reassignment creates a new local binding
      without affecting the caller.

   PEP 8
      Python Enhancement Proposal 8 -- the official style guide for
      Python code. Prescribes ``snake_case`` for variables and
      functions, ``UPPER_CASE`` for constants, and ``PascalCase``
      for classes.

   Polymorphism
      A design principle meaning "many forms." Different objects respond
      to the same interface in their own way. In Python, polymorphism is
      achieved through duck typing (method presence at runtime) and
      method overriding (subclass specialization). A polymorphic function
      calls the same method on a mixed collection of objects and receives
      different, type-appropriate behavior from each, without knowing the
      concrete types involved.

   Positional Argument
      An argument matched to a parameter by its position in the function
      call. The first argument is assigned to the first parameter, the
      second to the second, and so on.

   Process
      A program in execution. Each ROS 2 node typically runs as a
      separate OS process with its own isolated memory space, PID, CPU
      time allocation, and file descriptors. Process isolation is the
      key to fault containment in a distributed ROS 2 system: a crashed
      node does not take down other nodes.

   Programming Paradigm
      A fundamental style or approach to organizing and structuring code.
      The three major paradigms are procedural (step-by-step instructions),
      object-oriented (data and behavior bundled in objects), and
      functional (computation as function evaluation). Python supports all
      three as a multi-paradigm language.

   Property
      A Python mechanism (via the ``@property`` decorator) that allows
      controlled access to an attribute through getter and setter methods
      while preserving attribute-style syntax. The getter is triggered by
      ``obj.attr`` and the setter by ``obj.attr = value``. Used
      throughout OOP to enforce validation on assignment.

   ``@property``
      A built-in decorator that transforms a method into a read-only
      attribute. Combined with ``@attr.setter``, it provides validation
      and control over attribute access without changing the external
      interface. Preferred over explicit getter/setter methods in Python.

   Protocol
      A class defined with ``typing.Protocol`` that describes an interface
      through structural subtyping. A class satisfies a Protocol if it
      has the required methods and attributes, regardless of its class
      hierarchy. No explicit inheritance from the Protocol is needed.
      Contrast with ABCs, which require the subclass to explicitly inherit
      from the base class (nominal typing). Adding ``@runtime_checkable``
      allows ``isinstance()`` checks at runtime, though only method
      presence (not signatures) is verified.

   Proxy Object
      A wrapper that intercepts calls and forwards them to another object
      on your behalf. ``super()`` returns a proxy object: it does not give
      you the parent class directly but a middleman that knows your
      position in the MRO and routes method calls to the correct next
      class in the chain. This is what makes ``super()`` work correctly
      in multiple inheritance, where the next class is not always the
      obvious direct parent.

   Publisher
      A ROS 2 object that sends messages on a named topic. Created with
      ``self.create_publisher(MsgType, "topic_name", qos_depth)``.
      Publishers send messages regardless of whether any subscriber is
      listening. Messages are published from timer or event callbacks,
      not from blocking ``while`` loops.

   Pure Function
      A function whose output depends only on its inputs and that produces
      no side effects. Given the same inputs, a pure function always
      returns the same output. Pure functions do not modify external state,
      perform I/O, or depend on mutable global variables.

   py_trees
      A Python library for building :term:`behavior trees <Behavior
      Tree>`. Used in the final project to coordinate high-level robot
      tasks (waypoint patrol, event response) by calling Nav2 action
      servers.

   PyPy
      A Python implementation written in RPython that uses :term:`JIT
      compilation` to achieve 4--10x speedups on long-running programs.

   ``pyproject.toml``
      A configuration file used by Python packaging tools. Defines
      build system requirements, project metadata (name, version,
      description), and dependencies. Required for
      :term:`editable installs <Editable Install>`.

   ``PYTHONPATH``
      An environment variable listing directories that Python adds to
      ``sys.path`` at startup. Session-specific by default; add to
      ``~/.bashrc`` for persistence. Useful during development and
      testing.

   ``.pth`` File
      A text file placed in Python's :term:`site-packages` directory
      where each line is a path added to ``sys.path`` at startup.
      Provides a system-wide way to make packages discoverable without
      modifying code.


.. _glossary-q:

Q
=

.. glossary::

   QoS (Quality of Service)
      The set of policies that govern how messages are delivered between
      publishers and subscribers in DDS/ROS 2. The four most relevant
      policies are Reliability, Durability, History, and Deadline.
      Publisher and subscriber QoS must be compatible or DDS silently
      refuses the connection -- no error and no data. An incompatible
      QoS mismatch is one of the most common causes of a subscriber
      that receives nothing.

   Queue Depth
      The ``depth`` parameter of a QoS profile (or the integer shorthand
      passed to ``create_publisher``/``create_subscription``). Under the
      ``KEEP_LAST`` history policy, the queue holds at most ``depth``
      undelivered messages. When the queue is full, the oldest message
      is evicted to make room for the newest. A queue depth of 1
      means only the most recent message is ever buffered.


.. _glossary-r:

R
=

.. glossary::

   range()
      A built-in function that returns an immutable sequence of integers.
      Syntax: ``range(stop)`` or ``range(start, stop, step)``. The
      ``stop`` value is never included. ``range()`` is memory-efficient
      because it uses :term:`lazy evaluation`.

   Raw String
      A string literal prefixed with ``r`` that treats backslashes as
      literal characters: ``r"C:\Users\notes"`` contains two literal
      backslashes. Useful for file paths and regular expressions.

   rclpy
      The Python client library for ROS 2. It wraps the underlying
      ``rcl`` C library and exposes the full ROS 2 API in Python:
      ``rclpy.init()``, ``rclpy.spin()``, ``rclpy.shutdown()``, and
      the ``Node`` class with ``create_publisher()``,
      ``create_subscription()``, ``create_timer()``, and more.

   Rebinding
      Reassigning a variable name to a different object. In Python,
      this does not modify the original object -- it changes which
      object the name refers to.

   Recursion
      A programming technique where a function calls itself to solve a
      problem by breaking it into smaller sub-problems. Every recursive
      function requires a :term:`Base Case` and a recursive case.
      Python limits recursion depth to 1000 by default.

   Relational Operator
      An operator that compares values and returns ``True`` or
      ``False``: ``==``, ``!=``, ``>``, ``<``, ``>=``, ``<=``.
      Python supports :term:`chained comparisons <Chained Comparison>`.

   Reliability (QoS)
      A QoS policy controlling message delivery guarantees.
      ``RELIABLE`` retransmits dropped packets until delivery is
      confirmed. ``BEST_EFFORT`` sends without retransmission, offering
      lower latency at the cost of possible message loss. A
      ``RELIABLE`` subscriber will not connect to a ``BEST_EFFORT``
      publisher.

   REPL
   Read-Eval-Print Loop
      An interactive programming environment that reads user input,
      evaluates it, prints the result, and loops. Python provides a
      built-in REPL via ``python3`` or the VS Code Native Python REPL.

   Requirement Analysis
      The process of identifying **what** the system must do (functional
      requirements) and **how well** it must do it (non-functional
      requirements). The first step in the design workflow.

   Reserved Keyword
      A word with special meaning in Python that cannot be used as a
      variable name (e.g., ``if``, ``class``, ``return``). Python 3
      has 35 reserved keywords. Use ``keyword.iskeyword()`` to check.

   ROS 2
   Robot Operating System 2
      A middleware framework for robotics development. This course uses
      ROS 2 Jazzy Jalisco for robot communication, sensor integration,
      and task coordination.

   ROS 2 Workspace
      A directory containing all packages, dependencies, and build
      artifacts for a ROS 2 project. The standard layout has four
      subdirectories: ``src/`` (source packages), ``build/``
      (intermediate build artifacts), ``install/`` (final install tree
      including ``setup.bash``), and ``log/`` (build logs). Always run
      ``colcon build`` from the workspace root, not from inside
      ``src/``.

   rosdep
      A command-line tool that reads ``package.xml`` files and
      installs all declared system dependencies automatically. Run
      ``rosdep install --from-paths ./src --ignore-packages-from-source -y``
      from the workspace root to install all missing dependencies in
      one command.

   RTPS (Real-Time Publish-Subscribe)
      The wire protocol underlying DDS. RTPS defines how DDS
      implementations discover participants and exchange data over the
      network. Because all vendors implement RTPS, DDS nodes from
      different vendors can interoperate on the same network.

   Ruff
      A fast Python :term:`linter` and :term:`formatter` written in
      Rust. Replaces Flake8, Black, isort, and many plugins. Runs
      10--100x faster than pure-Python alternatives.

   ``__repr__``
      A dunder method called by ``repr()``, the REPL, the debugger, and
      when objects appear inside containers (lists, dicts). Should return
      a string that looks like the code you would type to create the
      object (e.g., ``Robot('Scout', 100)``). Serves as the fallback for
      ``__str__`` if ``__str__`` is not defined.

   ``return`` Statement
      A statement that exits a function and optionally sends a value back
      to the caller. Multiple values can be returned as a tuple.
      Functions without a ``return`` statement implicitly return ``None``.


.. _glossary-s:

S
=

.. glossary::

   Scope
      The region of a program where a variable name is accessible. Python
      uses the :term:`LEGB Rule` to determine which scope a name belongs
      to. Each function call creates a new local scope.

   ``self``
      The conventional name for the first parameter of instance methods.
      Refers to the specific instance that called the method. Python
      passes it automatically: ``obj.method(arg)`` is translated to
      ``ClassName.method(obj, arg)``.

   Sequence Type
      A container that stores elements in a specific order and supports
      indexing, slicing, and iteration. Built-in sequence types include
      ``list``, ``tuple``, ``str``, ``bytes``, and ``range``.

   Service
      A ROS 2 communication primitive for synchronous request-response
      interactions. One node (the client) sends a request; another
      node (the server) processes it and returns a response. Services
      block until a response arrives. Defined in ``.srv`` files.
      Example use: trigger the gripper, query the current map, save state.

   Set
      A mutable, unordered collection of unique :term:`hashable
      <Hashable>` elements. Created with curly braces ``{1, 2, 3}`` or
      the ``set()`` constructor. Supports mathematical operations like
      union, intersection, and difference.

   Set Comprehension
      A concise syntax for creating sets:
      ``{expression for item in iterable if condition}``. Automatically
      removes duplicates.

   Shadowing
      When a variable in an inner scope has the same name as a variable
      in an outer scope, hiding the outer variable. For example, a local
      variable named ``x`` shadows a global variable named ``x`` within
      that function.

   Shallow Copy
      A copy of a container (e.g., ``list.copy()``, ``dict.copy()``)
      that creates a new container object but does not recursively
      copy the objects contained within it. Sufficient when the
      contained objects are immutable.

   Short-Circuit Evaluation
      A behavior of :term:`logical operators <Logical Operator>` where
      the second operand is not evaluated if the result is already
      determined. ``and`` stops at the first falsy value; ``or`` stops
      at the first truthy value.

   Side Effect
      Any observable change that a function makes beyond returning a
      value. Examples include modifying a global variable, mutating a
      mutable argument, printing to the console, writing to a file, or
      making a network request. Functional programming aims to minimize
      side effects.

   Singleton
      An object of which only one instance exists in the entire
      program. ``None``, ``True``, and ``False`` are singletons in
      Python.

   ``site-packages``
      The directory where Python installs third-party packages. Its
      location can be found with
      ``python3 -c "import site; print(site.getsitepackages())"``.
      :term:`.pth files <.pth File>` placed here are processed at
      startup.

   Slicing
      Extracting a subsequence from a sequence using the syntax
      ``[start:stop:stride]``. ``start`` is inclusive, ``stop`` is
      exclusive, and ``stride`` defaults to ``1``. Negative indices
      count from the end.

   snake_case
      A naming convention where words are separated by underscores and
      all letters are lowercase, e.g., ``student_name``, ``max_speed``.
      Prescribed by :term:`PEP 8` for variable and function names.

   Specialization
      A top-down design activity in which a general base class is refined
      into derived classes that extend or override its behavior for a
      specific context. Each subclass carries only the attributes and
      methods unique to that type, avoiding ``None`` placeholders for
      inapplicable fields. Contrast with generalization.

   Spinning
      The act of activating the ROS 2 executor so it can process
      incoming callbacks. ``rclpy.spin(node)`` blocks the calling
      thread indefinitely and dispatches callbacks as they arrive.
      Without spinning, a node is registered but completely passive --
      no timer fires, no message is received. ``rclpy.spin_once()``
      processes one batch and returns; ``rclpy.spin_until_future_complete()``
      blocks until a Future resolves.

   Static Method
      A method defined with the ``@staticmethod`` decorator. It receives
      neither ``self`` nor ``cls`` and has no implicit access to instance
      or class state. Behaves like a regular function but lives in the
      class namespace for organizational clarity. Common uses: validation
      helpers, unit conversions, and pure computations logically related
      to the class.

   Static Typing
      A type system where the type of every variable is known at
      compile time and cannot change. Examples: C, C++, Java, Rust.
      Contrast with :term:`Dynamic Typing`.

   String Interning
      See :term:`Interning`.

   Structural Subtyping
      A typing model in which compatibility between a class and an
      interface is determined by the presence of the required methods and
      attributes, not by explicit inheritance. Implemented in Python via
      ``typing.Protocol``. Contrast with nominal typing (used by ABCs),
      where a class must explicitly inherit from the interface to be
      considered compatible.

   Subscriber
      A ROS 2 object that receives messages on a named topic. Created
      with ``self.create_subscription(MsgType, "topic_name", callback,
      qos_depth)``. The callback is invoked by the executor each time a
      message arrives. Topic name and message type must match the
      publisher exactly; a mismatch causes a silent failure.

   ``super()``
      A built-in function that returns a proxy object used to delegate
      method calls to the next class in the MRO. Always use the
      no-argument form ``super()`` in Python 3. Call
      ``super().__init__()`` as the first line of a child ``__init__``
      so that parent attributes are initialized before the child tries
      to use them. Can be used in any method, not just ``__init__``.

   Symmetric Difference
      A set operation returning elements in either set but not in both.
      Performed with ``^`` operator or ``.symmetric_difference()``
      method. ``{1, 2, 3} ^ {2, 3, 4}`` returns ``{1, 4}``.

   Syntactic Sugar
      Syntax that makes code easier to read or write but does not add new
      functionality. The ``@decorator`` syntax is syntactic sugar for
      ``func = decorator(func)``. Similarly, list comprehensions are
      syntactic sugar for loops that build lists.

   sys.path
      A list of directory paths that Python searches when resolving
      ``import`` statements. Modify with ``sys.path.insert()`` to
      add custom directories. Also populated automatically from
      :term:`PYTHONPATH` and :term:`.pth files <.pth File>`.

   setup.py
      The build script for a Python ROS 2 package. It tells ``colcon``
      how to install nodes (via ``entry_points``), launch files, and
      config files (via ``data_files``). Package name and version must
      match ``package.xml`` exactly. After adding a new entry point,
      ``colcon build`` must be run again; ``--symlink-install`` does
      not pick up new entry points automatically.

   ``__slots__``
      A class-level declaration that replaces the per-instance ``__dict__``
      with a fixed, compact structure containing only the listed attribute
      names. Reduces memory consumption (the ``__dict__`` alone costs
      roughly 232 bytes per instance) and speeds up attribute access.
      Prevents dynamic addition of attributes not listed in ``__slots__``.
      In an inheritance hierarchy, each class should declare only the new
      attributes it introduces; Python merges the slots from all classes
      in the chain automatically.

   ``__str__``
      A dunder method called by ``print()`` and ``str()``. Should return
      a human-readable string intended for end users and display output.
      If not defined, Python falls back to ``__repr__``.


.. _glossary-t:

T
=

.. glossary::

   Thread
      The smallest unit of execution inside a process. A process starts
      with one thread (the main thread). When ``rclpy.spin(node)`` is
      called, the main thread is handed to the ROS 2 executor which
      runs it in a loop dispatching callbacks. A slow callback blocks
      this thread and delays all other pending callbacks.

   Timer (ROS 2)
      A ROS 2 object that fires a callback at a fixed interval. Created
      with ``self.create_timer(period_seconds, callback)``. The timer
      only fires while the node is spinning. Timers are the standard
      mechanism for driving periodic behavior (e.g., publishing sensor
      data at a fixed rate) without blocking the executor thread.

   Token
      The smallest meaningful unit of source code produced by the
      :term:`lexer`. Examples include keywords (``def``), identifiers
      (``my_var``), operators (``+``), and literals (``42``).

   Topic
      A named, typed communication channel over which nodes exchange
      messages asynchronously. Publishers and subscribers are decoupled:
      they discover each other through DDS without knowing each other's
      identity. A topic has a fixed name (e.g., ``/scan``) and a fixed
      message type; both must match for a publisher-subscriber pair to
      exchange data.

   Truthy
      A value that evaluates to ``True`` when passed to ``bool()``.
      Any non-zero number, non-empty string, or non-empty collection
      is truthy. Contrast with :term:`Falsy`.

   Truthiness
      The concept that every Python object has an inherent Boolean
      value. Pythonic code leverages truthiness directly in conditions:
      ``if my_list:`` rather than ``if len(my_list) > 0:``.

   Tuple
      An immutable, ordered sequence of objects. Created with
      parentheses ``(1, 2, 3)`` or the ``tuple()`` constructor.
      Single-element tuples require a trailing comma: ``(42,)``. Tuples
      are :term:`hashable <Hashable>` if all their elements are hashable.

   Tuple Packing
      Creating a tuple by listing comma-separated values without
      parentheses: ``point = 3, 4`` creates the tuple ``(3, 4)``.

   Tuple Unpacking
      Assigning tuple elements to individual variables:
      ``x, y = (3, 4)`` assigns ``3`` to ``x`` and ``4`` to ``y``.
      Also works with lists and other iterables.

   Type Hint
      An optional annotation in Python source code that indicates the
      expected type of a variable, parameter, or return value (e.g.,
      ``def greet(name: str) -> None``).


.. _glossary-u:

U
=

.. glossary::

   Ubuntu
      A Linux distribution. This course uses Ubuntu 24.04 LTS (Noble
      Numbat) as the primary operating system.

   UML
      Unified Modeling Language. A standardized notation for visualizing
      software design. This course uses class diagrams (structure),
      sequence diagrams (object interaction over time), and activity
      diagrams (control flow).

   Union
      A set operation returning all elements from both sets (duplicates
      removed). Performed with ``|`` operator or ``.union()`` method.
      ``{1, 2, 3} | {2, 3, 4}`` returns ``{1, 2, 3, 4}``.

   Unpacking
      See :term:`Tuple Unpacking`. Extended unpacking uses ``*`` to
      capture multiple values: ``first, *rest = [1, 2, 3, 4]`` assigns
      ``1`` to ``first`` and ``[2, 3, 4]`` to ``rest``.


.. _glossary-v:

V
=

.. glossary::

   Variadic Function
      A function that accepts a variable number of arguments. Python's
      built-in ``print()`` is variadic -- it accepts any number of
      positional arguments.

   View Object
      An object providing a dynamic view of dictionary keys, values, or
      items. Returned by ``dict.keys()``, ``dict.values()``, and
      ``dict.items()``. Views reflect changes to the dictionary without
      creating a copy.

   Visual Studio Code
   VS Code
      A lightweight, extensible code editor by Microsoft. The primary
      IDE for this course, used with the Python, Dev Containers, and
      Ruff extensions.


.. _glossary-w:

W
=

.. glossary::

   while Loop
      A control structure that repeats as long as a condition is
      ``True``. Syntax: ``while condition:``. Must include logic to
      eventually make the condition ``False``, or the loop runs forever
      (infinite loop).

   Wildcard Import
      An import of the form ``from module import *`` that brings every
      public name from a module into the current namespace. Strongly
      discouraged because it causes :term:`namespace pollution` and
      makes it impossible to tell where a name originated.

   Workspace
      In VS Code, the root folder opened by the editor. VS Code stores
      workspace-specific settings in ``.vscode/settings.json``. For
      this course: ``~/enpm605/py_ws``.

   Workspace Overlay
      The practice of sourcing one ROS 2 installation on top of
      another. The later source takes precedence for package lookup.
      The standard order is: source the base ROS 2 installation first
      (``/opt/ros/jazzy/setup.bash``), then source your workspace
      (``install/setup.bash``). Never source two different ROS 2
      distributions in the same shell session.

   Wrapper Function
      The inner function in a decorator that replaces the original
      function. It typically accepts ``*args`` and ``**kwargs`` to work
      with any function signature, adds the decorator's behavior (such as
      logging or timing), calls the original function, and returns its
      result. Should always use ``@functools.wraps`` to preserve the
      original function's metadata.

   ``__init__.py``
      A file that marks a directory as a Python :term:`package`. May
      be empty or may contain package-level initialization code and
      ``__all__`` definitions to control wildcard imports.

   ``__name__``
      A special variable set to ``"__main__"`` when a module is run
      directly and to the module's own name when imported. The
      ``if __name__ == '__main__':`` guard prevents code from running
      on import.
