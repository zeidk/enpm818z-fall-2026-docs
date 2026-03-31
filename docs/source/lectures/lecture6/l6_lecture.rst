====================================================
Lecture
====================================================



Introduction to OOP
====================================================

Core principles of object-oriented programming.



.. dropdown:: What Is OOP?
   :open:

   **Object-Oriented Programming** is a paradigm that models software as a collection of **objects** that interact with one another. Each object bundles data (attributes) and behavior (methods) together.

   Python is a **multi-paradigm** language: it supports procedural, functional, and object-oriented styles. OOP features appear throughout the standard library and most major frameworks, so familiarity with OOP is essential for effective Python development.

   **Core Principles**

   - **Encapsulation** -- Bundles related data and methods into a single object. In Python, access control is by convention (e.g., leading underscores) rather than enforced by the language.
   - **Abstraction** -- Exposes only essential features through a well-defined interface (e.g., abstract base classes) while hiding the underlying implementation.
   - **Inheritance** -- Enables new classes to reuse and extend the functionality of existing ones.
   - **Polymorphism** -- Allows different objects to be used interchangeably when they share a common interface. Python achieves this naturally through duck typing.

   .. note::

      Python is a **multi-paradigm** language. You can mix procedural, object-oriented, and functional styles in the same program.


.. dropdown:: Benefits and Trade-offs
   :open:

   **Advantages**

   - **Modularity** -- Decomposes complex problems into manageable, self-contained components.
   - **Reusability** -- Promotes code reuse through inheritance and composition.
   - **Flexibility** -- Enables dynamic behavior via duck typing and interchangeable implementations.
   - **Maintainability** -- Facilitates localized changes and clearer code organization.

   **Trade-offs**

   - **Learning Curve** -- Requires understanding abstract concepts and design patterns.
   - **Design Overhead** -- Demands more upfront planning and structure.
   - **Verbosity** -- Object-oriented programs can be more verbose than procedural or functional alternatives.

   .. warning::

      OOP is not a one-size-fits-all solution. Not all problems map naturally to objects and classes. Modern Python emphasizes **composition over inheritance**: prefer combining simple objects rather than building deep class hierarchies.


Design Phase
====================================================

Translating a real-world problem into a workable structure before writing any code.



.. dropdown:: Design Workflow
   :open:

   **From Problem to Code**

   The design phase bridges the gap between a real-world problem and working code. The workflow is iterative: you will revisit earlier steps as you discover new information.

   1. **Requirement Analysis** -- Understand *what* the system must do.
   2. **Business Rules** -- Capture the constraints and invariants the system must enforce.
   3. **Noun/Verb Analysis** -- Extract candidate classes, attributes, and methods from the requirements.
   4. **Modeling** -- Visualize structure (class diagrams) and behavior (sequence and activity diagrams).
   5. **Implementation** -- Translate the design into code.

   .. note::

      This workflow is iterative. Your first pass will not be perfect. Revisit and refine as you learn more about the domain.


.. dropdown:: Requirement Analysis
   :open:

   **Step 1: Understanding What the System Must Do**

   **Requirement analysis** identifies **what** the system must do (functional requirements) and **how well** it must do it (non-functional requirements).

   **Competition Domain**

   A `robotics competition <https://youtu.be/DLQCaRLb3TE?si=CSCnujfqYE4dGYBQ&t=2490>`_ involves teams of robots collaborating to complete tasks in an arena. We are building a **competition management system**: the software an organizer would use to coordinate teams, assign tasks, track battery levels, and record results.

   **Key Functional Requirements**

   - Track which robots belong to which teams and their operational status.
   - Assign, prioritize, and schedule tasks for robots.
   - Monitor robot attributes such as battery level and sensor configuration.
   - Model the arena layout, including obstacles and target zones.
   - Record competition progress and results.

    .. note::
        
        See the **Design Phase PDF** (:download:`DesignPhase_ENPM605_Spring2026.pdf <DesignPhase_ENPM605_Spring2026.pdf>`) for the complete requirement analysis, clarifying questions, and use case descriptions. This document demonstrates what a real design document looks like: it captures domain context, functional requirements, and behavioral scenarios in a structured format that serves as the blueprint for implementation.



.. dropdown:: Business Rules
   :open:

   **Step 2: Constraints the System Must Enforce**

   **Business rules** define what is allowed, required, and prohibited. They directly influence class design: which validations go into methods, which attributes need constraints, and which relationships must be enforced.

   **Competition Domain Rules**

   - A robot's battery level must be between 0 and 100.
   - A robot cannot accept a task unless its status is "active".
   - Each robot belongs to exactly one team; a team has at most ``max_robots`` robots.
   - A task's priority must be one of: "low", "medium", "high", "critical".
   - When battery drops below 10%, status changes to "needs_recharge".
   - When a task is completed, the team's score is updated automatically.
   - Battery drain = task duration x drain rate.
   - Team score = sum of points for each completed task.

   .. note::

      See the **Design Phase PDF** for the full set of business rules organized by category (constraints, triggers, computations, authorization).


.. dropdown:: Noun/Verb Analysis
   :open:

   **Step 3: From Natural Language to OOP**

   **Noun/verb analysis** extracts candidate classes, attributes, and methods from a problem description. Nouns map to classes or attributes; verbs map to methods; adjectives map to attribute values; relationships ("has a", "is a") map to composition or inheritance.

   *"A robotics* **competition** *involves* **teams** *of* **robots** *collaborating to complete* **tasks** *in an* **arena**. *Each* **robot** *is equipped with* **sensors** *to perceive its environment and must navigate, pick up objects, and deliver them to target* **zones**."

   .. list-table:: Noun/verb extraction for the robotics competition domain
      :widths: 15 25 25 25
      :header-rows: 1
      :class: compact-table

      * - Class
        - Attributes
        - Methods
        - Relationships
      * - Robot
        - name, battery, status
        - move(), pick_up(), deliver(), recharge()
        - has Sensors, belongs to Team
      * - Sensor
        - type, range, accuracy
        - read(), calibrate()
        - belongs to Robot
      * - Task
        - name, priority, duration
        - assign(), complete(), cancel()
        - assigned to Robot
      * - Arena
        - width, height, obstacles, zones
        - add_obstacle(), get_zone()
        - contains Robots
      * - Team
        - name, score, max_robots
        - add_robot(), remove_robot()
        - has Robots

   .. note::

      Not every noun becomes a class and not every verb becomes a method. See the **Design Phase PDF** for the filtering rationale and the full extraction walkthrough.


.. dropdown:: Modeling
   :open:

   **Step 4: Visualizing Structure and Behavior**

   `UML <https://www.uml.org/>`_ (Unified Modeling Language) provides standardized diagrams to capture different aspects of the system. We use three diagram types in this course:

   - **Class Diagrams** -- Show classes, their attributes and methods, and relationships (composition, aggregation, association, inheritance).
   - **Sequence Diagrams** -- Show how objects interact over time by exchanging method calls.
   - **Activity Diagrams** -- Show the flow of control through a process (similar to flowcharts, but with support for concurrency and swimlanes).

   **Competition Domain Relationships**

   - **Composition** -- A ``Robot`` owns its ``Sensor``\(s). Destroying the robot destroys its sensors.
   - **Aggregation** -- A ``Team`` has ``Robot``\(s). Dissolving the team does not destroy the robots.
   - **Association** -- A ``Robot`` is assigned a ``Task``. Neither owns the other.
   - **Inheritance** (L7) -- ``MobileRobot`` and ``ManipulatorRobot`` are types of ``Robot``.

   .. note::

      See the **Design Phase PDF** for UML notation details, the full class diagram, sequence diagrams, and activity diagrams for the competition domain.


.. dropdown:: From Design to Implementation
   :open:

   **Step 5: Translating the Design into Code**

   For this lecture, we implement the ``Robot`` and ``Sensor`` classes. The remaining classes (``Task``, ``Team``, ``Arena``) and their relationships will be covered in L7.

   **Project Structure**

   .. code-block:: text

      robotics_competition/
          robot.py      # Robot class
          sensor.py     # Sensor class
          task.py       # Task class (L7)
          team.py       # Team class (L7)
          arena.py      # Arena class (L7)
          main.py       # Entry point

   .. note::

      Each class lives in its own module. This promotes modularity and makes the code easier to maintain, test, and extend. The design phase is iterative: revisit and refine as you implement.


Implementation Phase: Classes and Objects
====================================================

Translating the design into working code.

Refer to ``L6_classes_objects.py`` to follow along with the examples below.


.. dropdown:: What Is a Class?
   :open:

   A **class** is a blueprint that defines the attributes (data) and methods (functions) that its objects will have.

   .. code-block:: python

      class ClassName:
          """Docstring describing the class."""

          def __init__(self, param1: type, param2: type = default):
              self.attribute1 = param1
              self.attribute2 = param2

          def method1(self, arg: type):
              # Use self.attribute1, self.attribute2, arg, etc.
              ...

          def method2(self):
              # Operate on the object's attributes
              ...

   - The ``class`` keyword starts the definition, followed by the class name in **CamelCase**.
   - By default, every class implicitly inherits from ``object``.
   - Inside the class body we define methods. The first parameter of every method is ``self``, which refers to the object calling the method.


.. dropdown:: What Is an Object?
   :open:

   An **object** (or **instance**) is a concrete realization of a class. Multiple objects can be created from the same blueprint, each with its own attribute values.

   .. code-block:: python

      # Creating objects from the class
      obj1 = ClassName(value1, value2)
      obj2 = ClassName(value3)          # value4 uses the default

      # Calling methods on each object
      obj1.method1(some_arg)   # self refers to obj1
      obj2.method1(other_arg)  # self refers to obj2

      # Accessing attributes
      print(obj1.attribute1)   # value1
      print(obj2.attribute1)   # value3

   - Each object is independent: modifying ``obj1`` does not affect ``obj2``.
   - Each object maintains its own copy of the attributes defined in ``__init__``.
   - All objects share the same method definitions. When you call ``obj1.method1(arg)``, Python passes ``obj1`` as ``self`` automatically.
   - Access attributes and methods using dot notation: ``obj.attribute`` or ``obj.method()``.


.. dropdown:: From Blueprint to Instances
   :open:

   The blueprint specifies **what every robot arm will have** and **what it can do**. Each arm built from that blueprint is an independent instance with its own state.

   .. code-block:: python

      class RobotArm:
          """Blueprint for a robot arm."""

          def __init__(self, station: int):
              self.station = station
              self.joint_angle = 0.0
              self.gripping = False

          def pick_up(self):
              self.gripping = True

          def rotate(self, angle: float):
              self.joint_angle += angle

   **Creating Objects**

   Each call to the class creates a new, independent object. All objects share the same structure but maintain their own state.

   .. code-block:: python

      # Three arms built from the same blueprint
      arm_1 = RobotArm(station=1)
      arm_2 = RobotArm(station=2)
      arm_3 = RobotArm(station=3)

      arm_1.pick_up()         # arm_1 is gripping, others are not
      arm_2.rotate(45.0)      # arm_2 rotated, others unchanged

      print(arm_1.gripping)      # True
      print(arm_2.joint_angle)   # 45.0
      print(arm_3.gripping)      # False

   .. note::

      ``arm_1``, ``arm_2``, and ``arm_3`` are three **objects** (instances) created from the same **class** (blueprint). Modifying one does not affect the others.


.. dropdown:: How ``self`` Works
   :open:

   The ``self`` parameter refers to the instance of the class. When you call a method on an instance, Python automatically passes the instance as the first argument. By convention this parameter is named ``self``.

   **What You Write**

   .. code-block:: python

      def rotate(self, angle: float):
          self.joint_angle += angle

      arm_1 = RobotArm(station=1)
      arm_1.rotate(45.0)

   **What Python Does**

   .. code-block:: python

      def rotate(arm_1, angle: float):
          arm_1.joint_angle += angle

      arm_1 = RobotArm(station=1)
      RobotArm.rotate(arm_1, 45.0)

   .. note::

      **Key Insight**: ``arm_1.rotate(45.0)`` is syntactic sugar for ``RobotArm.rotate(arm_1, 45.0)``. Python automatically fills in ``self`` for you.


.. dropdown:: The Constructor: ``__init__``
   :open:

   ``__init__`` is a special method (a "dunder" method) called automatically when a new instance is created. It initializes the object's attributes.

   .. code-block:: python

      class RobotArm:
          def __init__(self, station: int):
              self.station = station
              self.joint_angle = 0.0
              self.gripping = False

      if __name__ == "__main__":
          arm = RobotArm(station=1)
          print(arm.station)       # 1
          print(arm.joint_angle)   # 0.0
          print(arm.gripping)      # False

   - When ``RobotArm(station=1)`` is called, Python creates a new instance and passes it as ``self`` to ``__init__``.
   - Inside ``__init__``, we set instance variables using ``self.attribute = value``.
   - It is not mandatory to define ``__init__``, but it is best practice to initialize all attributes there.

   .. warning::

      ``__init__`` is **not** a constructor in the strict sense. It is an initializer. The actual constructor is ``__new__``, which is rarely overridden.

   **Initialize All Attributes in ``__init__``**

   To make your code less error-prone, initialize **all** attributes in the ``__init__`` method, even if you set them to empty values or ``None``.

   .. code-block:: python

      class RobotArm:
          def __init__(self, station: int):
              self.station = station
              self.joint_angle = 0.0
              self.gripping = False
              self.log: list[str] = []     # Always initialize here

          def pick_up(self, item: str):
              self.gripping = True
              self.last_item = item        # Bad: new attribute outside __init__

   .. warning::

      Creating new attributes outside ``__init__`` (like ``self.last_item`` above) is discouraged. It makes the class harder to understand and undermines encapsulation.


.. dropdown:: Instance Attributes
   :open:

   Instance attributes belong to a specific object. Each object maintains its own copy, so modifying one object does not affect any other.

   .. code-block:: python

      class RobotArm:
          def __init__(self, station: int):
              self.station = station        # Instance attribute
              self.joint_angle = 0.0        # Instance attribute
              self.gripping = False         # Instance attribute

      if __name__ == "__main__":
          arm_1 = RobotArm(station=1)
          arm_2 = RobotArm(station=2)

          arm_1.joint_angle = 45.0

          print(arm_1.joint_angle)  # 45.0
          print(arm_2.joint_angle)  # 0.0  (unaffected)

   - Instance attributes are created inside ``__init__`` using ``self.attribute = value``.
   - Each object gets its own copy: ``arm_1.joint_angle`` and ``arm_2.joint_angle`` are independent.
   - Instance attributes cannot be accessed through the class itself: ``RobotArm.station`` raises ``AttributeError``.


.. dropdown:: Class Attributes
   :open:

   Class attributes are defined directly in the class body, outside any method. They are shared by all instances and accessed through the class name.

   .. code-block:: python

      class RobotArm:
          total_arms = 0          # Class attribute (shared)

          def __init__(self, station: int):
              self.station = station      # Instance attribute (unique)
              self.joint_angle = 0.0      # Instance attribute (unique)
              self.gripping = False       # Instance attribute (unique)
              RobotArm.total_arms += 1

      if __name__ == "__main__":
          arm_1 = RobotArm(station=1)
          arm_2 = RobotArm(station=2)
          print(RobotArm.total_arms)    # 2 (accessed via class)
          print(arm_1.total_arms)       # 2 (accessed via instance)
          print(arm_2.total_arms)       # 2

   - Class attributes are defined outside ``__init__``, directly in the class body.
   - All instances share the same class attribute. Modifying it via ``RobotArm.total_arms`` is visible everywhere.
   - Always modify class attributes through the **class name** (``RobotArm.total_arms += 1``), not through ``self``. Using ``self.total_arms += 1`` creates a new instance attribute that shadows the class attribute.


Implementation Phase: Dunder Methods
====================================================

Customizing how your objects interact with built-in Python operations.

Refer to ``L6_classes_objects.py`` to follow along with the examples below.


.. dropdown:: What Are Dunder Methods?
   :open:

   **Dunder methods** (short for "double underscore") are special methods with names like ``__name__``. They allow your objects to interact with built-in Python operations such as ``print()``, ``len()``, ``+``, ``==``, ``in``, and more.

   **Method Overriding**

   When you write a dunder method in your class, you **override** the default behavior inherited from ``object``. This lets you customize how Python treats your objects.

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self.name = name
              self.battery = battery

      scout = Robot("Scout")
      print(scout)  # <__main__.Robot object at 0x7fe4dc66bbb0>
      # Not very useful! Let's fix this by overriding __str__


.. dropdown:: The ``__str__`` Method
   :open:

   ``__str__`` is called by ``print()`` and ``str()``. It should return a **human-readable** string intended for end users, log messages, or display output.

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self.name = name
              self.battery = battery

          def __str__(self) -> str:
              return f"{self.name} (Battery: {self.battery}%)"

      scout = Robot("Scout")
      print(scout)        # Scout (Battery: 100%)
      print(str(scout))   # Scout (Battery: 100%)

   - If ``__str__`` is not defined, Python falls back to ``__repr__``.
   - Focus on readability: this is what the user sees.
   - Think of ``__str__`` as the "pretty" representation.


.. dropdown:: The ``__repr__`` Method
   :open:

   ``__repr__`` is called by ``repr()`` and used in the REPL, debugger, and when objects appear inside containers. The string it returns should look like the code you would type to create that object. That way, a developer reading a log or debugging output can immediately see how to reproduce it.

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self.name = name
              self.battery = battery

          def __repr__(self) -> str:
              return f"Robot(name='{self.name}', battery={self.battery})"

      scout = Robot("Scout")
      print(repr(scout))  # Robot(name='Scout', battery=100)
      # You could copy that output and paste it as valid Python:
      # scout_copy = Robot(name='Scout', battery=100)

      robots = [Robot("Scout"), Robot("Hauler", 80)]
      print(robots)       # [Robot(name='Scout', battery=100), ...]

   - When you print a ``list``, Python calls ``__repr__`` on each element, not ``__str__``.
   - A good ``__repr__`` looks like a valid constructor call: ``Robot(name='Scout', battery=100)``.
   - If you only implement one, implement ``__repr__``. It serves as the fallback for ``__str__``.


.. dropdown:: ``__str__`` vs. ``__repr__``
   :open:

   .. list-table:: Comparing ``__str__`` and ``__repr__``
      :widths: 25 35 35
      :header-rows: 1
      :class: compact-table

      * -
        - ``__str__``
        - ``__repr__``
      * - Audience
        - End users
        - Developers
      * - Called by
        - ``print()``, ``str()``, f-strings
        - ``repr()``, REPL, debugger
      * - Inside containers
        - Not used
        - Used when objects are inside lists, dicts, etc.
      * - Goal
        - Human-readable
        - Should look like the code you would write to create the object
      * - Fallback
        - Falls back to ``__repr__`` if not defined
        - Falls back to default ``object.__repr__``

   .. code-block:: python

      scout = Robot("Scout", 80)

      print(scout)            # Scout (Battery: 80%)             __str__
      print(repr(scout))      # Robot(name='Scout', battery=80)  __repr__
      print(f"Bot: {scout}")  # Bot: Scout (Battery: 80%)        __str__
      print([scout])          # [Robot(name='Scout', battery=80)] __repr__

   .. note::

      **Rule of thumb**: Always implement ``__repr__``. Add ``__str__`` when you need a friendlier output for end users.


.. dropdown:: What Is Operator Overloading?
   :open:

   Python already knows how ``+`` works for integers and strings. **Operator overloading** lets you teach Python what ``+`` (or any operator) should do when applied to *your own* classes. This is different from **method overriding**, where a parent class already provides a version of a method, but the child class provides its own version to replace it.

   **Example**

   Same operator, different types. The behavior depends on the operands.

   .. code-block:: python

      # + already works for int and str
      print(3 + 4)         # 7
      print("ab" + "cd")   # abcd

      # We can teach + to work for Sensor objects too
      print(lidar + camera) # Sensor(...)


.. dropdown:: Operators and Their Dunder Methods
   :open:

   Every Python operator corresponds to a dunder method. When you use an operator with your objects, Python calls the corresponding method.

   .. list-table:: Common dunder methods for operator overloading
      :widths: 15 35 25
      :header-rows: 1
      :class: compact-table

      * - Operator
        - Dunder Method
        - Example
      * - ``+``
        - ``__add__(self, other)``
        - ``a + b``
      * - ``-``
        - ``__sub__(self, other)``
        - ``a - b``
      * - ``*``
        - ``__mul__(self, other)``
        - ``a * b``
      * - ``==``
        - ``__eq__(self, other)``
        - ``a == b``
      * - ``!=``
        - ``__ne__(self, other)``
        - ``a != b``
      * - ``<``
        - ``__lt__(self, other)``
        - ``a < b``
      * - ``>``
        - ``__gt__(self, other)``
        - ``a > b``
      * - ``<=``
        - ``__le__(self, other)``
        - ``a <= b``
      * - ``>=``
        - ``__ge__(self, other)``
        - ``a >= b``
      * - ``len()``
        - ``__len__(self)``
        - ``len(a)``
      * - ``in``
        - ``__contains__(self, item)``
        - ``x in a``
      * - ``()``
        - ``__call__(self, ...)``
        - ``a(...)``
      * - ``for...in``
        - ``__iter__(self)``
        - ``for x in a``


.. dropdown:: Comparison Operators
   :open:

   .. code-block:: python

      class Sensor:
          def __init__(self, sensor_type: str, range_m: float):
              self.sensor_type = sensor_type
              self.range_m = range_m

          def __eq__(self, other) -> bool:
              if isinstance(other, Sensor):
                  return self.range_m == other.range_m
              return NotImplemented

          def __gt__(self, other) -> bool:
              if isinstance(other, Sensor):
                  return self.range_m > other.range_m
              return NotImplemented

      lidar = Sensor("lidar", 50.0)
      camera = Sensor("camera", 30.0)
      print(lidar == camera)  # False
      print(lidar > camera)   # True


.. dropdown:: Arithmetic Operators
   :open:

   .. code-block:: python

      class Sensor:
          def __init__(self, sensor_type: str, range_m: float):
              self.sensor_type = sensor_type
              self.range_m = range_m

          def __add__(self, other):
              if isinstance(other, Sensor):
                  return Sensor("fused", self.range_m + other.range_m)
              elif isinstance(other, (int, float)):
                  return Sensor(self.sensor_type, self.range_m + other)
              return NotImplemented

          def __repr__(self) -> str:
              return f"Sensor('{self.sensor_type}', {self.range_m})"

      lidar = Sensor("lidar", 50.0)
      camera = Sensor("camera", 30.0)
      print(lidar + camera)   # Sensor('fused', 80.0)
      print(lidar + 10.0)     # Sensor('lidar', 60.0)

   .. note::

      Return ``NotImplemented`` (not ``raise NotImplementedError``) when the operand type is unsupported. This tells Python to try the reflected operation on the other operand.


.. dropdown:: Making Objects Iterable, Searchable, and Callable
   :open:

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self.name = name
              self.battery = battery
              self.log: list[str] = []

          def __iter__(self):
              return iter(self.log)

          def __contains__(self, task_name: str):
              return task_name in self.log

          def __call__(self, task_name: str):
              self.log.append(task_name)
              print(f"{self.name} assigned: {task_name}")

      scout = Robot("Scout")
      scout("pick widget")              # Scout assigned: pick widget
      scout("navigate to zone B")       # Scout assigned: navigate to zone B
      for entry in scout:               # Uses __iter__
          print(entry)                  # pick widget, then navigate to zone B
      print("pick widget" in scout)     # True (uses __contains__)


Implementation Phase: Abstraction and Encapsulation
====================================================

Controlling access to an object's internal state.

Refer to ``L6_classes_objects.py`` to follow along with the examples below.


.. dropdown:: What Is Abstraction?
   :open:

   **Abstraction** refers to hiding the complex implementation details of an object and showing only the essential features. The user interacts with an interface without needing to know how operations are implemented internally.

   **Real-World Analogy**

   Think of a robot's ``move()`` method: you call ``scout.move("north")`` without needing to know about motor controllers, PID loops, wheel encoders, or path planning algorithms. The robot hides its internal complexity behind a simple interface.

   **Python Example**

   Python built-in functions like ``len()`` are abstractions. You know ``len()`` returns the number of items in a sequence, but you do not need to know how it is implemented internally. The developers can change the internal implementation without affecting your code.

   .. note::

      **Separation of Concerns**: Abstraction separates *what* an object does from *how* it does it. This makes code easier to maintain and extend.


.. dropdown:: How Do We Achieve Abstraction?
   :open:

   Abstraction in Python is achieved at multiple levels. In this lecture we focus on the first two. The third level uses inheritance, which we cover in L7.

   .. code-block:: python

      class Robot:
          """A robot that performs tasks.

          The caller only needs to know that recharge() restores
          the battery. How it works internally is hidden.
          """

          def __init__(self, name: str, battery: int = 100):
              self.name = name
              self.battery = battery

          def recharge(self):
              """Restore battery to full."""
              # Internal details hidden:
              # - validate current state
              # - reset drain counter
              # - log the recharge event
              self.battery = 100

      if __name__ == "__main__":
          scout = Robot("Scout")
          scout.recharge()        # Simple interface
          print(scout.battery)    # 100

   **Level 1: Documentation**

   - A docstring describes *what* a class or method does without exposing *how*.
   - The end-user reads the docstring, not the source code.

   **Level 2: Public Interface**

   - Public methods (e.g., ``recharge()``) define what the object can do.
   - Internal logic (validation, logging, state management) is hidden inside the method body.
   - The end-user only sees a simple interface.

   **Level 3: Abstract Classes (L7)**

   - Python's ``abc`` module lets you define abstract methods that subclasses **must** implement.
   - This enforces a contract: every subclass guarantees the same interface.
   - We will cover this in Lecture 7.


.. dropdown:: What Is Encapsulation?
   :open:

   **Encapsulation** is the bundling of data (attributes) with the methods that operate on that data. The goal is to allow an object to manage its own state and prevent external code from modifying it in invalid ways.

   **The Problem Without Encapsulation**

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self.name = name
              self.battery = battery

          def perform_task(self, task_name: str):
              self.battery -= 10

      if __name__ == "__main__":
          scout = Robot("Scout")
          scout.battery = "full"     # No validation!
          scout.perform_task("pick") # TypeError: unsupported operand type(s)

   .. warning::

      Without encapsulation, external code can set ``battery`` to a string, causing methods to break. Encapsulation prevents this by controlling how attributes are accessed and modified.


.. dropdown:: How to Achieve Encapsulation
   :open:

   - Prefix all attributes with a leading underscore to signal they are non-public.
   - Provide controlled access through getter and setter decorators (``@property``).


.. dropdown:: Public vs. Non-Public Members
   :open:

   Python uses naming conventions (not access modifiers like Java or C++) to signal whether attributes are intended to be public or non-public.

   - ``name`` -- **Public**. Freely accessible from outside the class.
   - ``_name`` -- **Non-public by convention**. Signals "do not access directly". Python does not enforce this, but violating the convention is considered bad practice.
   - ``__name`` -- **Name mangling**. Python renames it to ``_ClassName__name`` to avoid accidental access. Rarely needed.

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self._name = name        # Non-public by convention
              self._battery = battery  # Non-public by convention

      scout = Robot("Scout")
      scout._battery = "full"  # Still possible, but violates the convention

   .. note::

      The underscore prefix is a **social contract**: it tells other developers "this attribute is internal; use the provided interface instead."


.. dropdown:: Traditional Getters and Setters
   :open:

   In languages like Java, you write explicit getter and setter methods. Python supports this, but it is not the preferred approach.

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self._name = name
              self._battery = battery

          def get_battery(self) -> int:
              return self._battery

          def set_battery(self, battery: int):
              if isinstance(battery, int) and 0 <= battery <= 100:
                  self._battery = battery
              else:
                  raise ValueError("Battery must be an integer between 0 and 100")

      scout = Robot("Scout")
      scout.set_battery(80)            # Works
      # scout.set_battery("full")     # ValueError
      print(scout.get_battery())       # 80

   .. note::

      This works, but it is not Pythonic. The ``@property`` decorator provides a cleaner solution.


.. dropdown:: The ``@property`` Decorator
   :open:

   **The Pythonic Way**

   The ``@property`` decorator transforms a method into a read-only attribute. Combined with a corresponding setter, it allows you to add validation and control over how an attribute is accessed and modified, all without changing the external interface.

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self._name = name       # non-public attribute
              self._battery = battery  # non-public attribute

   - Attributes prefixed with ``_`` signal that they should not be accessed directly.
   - External code interacts with these attributes through properties instead.


.. dropdown:: Defining a Getter
   :open:

   Applying ``@property`` to a method turns it into a getter. When external code accesses ``robot.battery``, Python automatically calls this method and returns its result.

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self._name = name
              self._battery = battery

          @property
          def battery(self) -> int:
              """The battery level of the robot."""
              return self._battery

   - The method name (``battery``) becomes the attribute name used by external code.
   - Accessing ``robot.battery`` calls this method behind the scenes.
   - Without a setter, the attribute is read-only.


.. dropdown:: Defining a Setter with Validation
   :open:

   The ``@battery.setter`` decorator defines what happens when external code assigns a value to ``robot.battery``. This is where you enforce constraints on incoming data.

   .. code-block:: python

      @battery.setter
      def battery(self, value: int):
          if not isinstance(value, int) or not (0 <= value <= 100):
              raise ValueError(
                  "Battery must be an integer between 0 and 100"
              )
          self._battery = value

   - The decorator name must match the property: ``@battery.setter``.
   - Invalid values raise an exception before the attribute is modified.
   - The non-public attribute ``_battery`` is only updated if validation passes.


.. dropdown:: Using Properties
   :open:

   From the caller's perspective, properties look and feel exactly like regular attributes. The validation logic is completely hidden behind the assignment syntax.

   .. code-block:: python

      if __name__ == '__main__':
          scout = Robot("Scout")
          print(scout.battery)      # 100  (calls the getter)
          scout.battery = 80         # OK   (calls the setter with validation)
          print(scout.battery)       # 80   (calls the getter)
          # scout.battery = "full"  # ValueError!

   - ``scout.battery`` on the right side of an expression triggers the getter.
   - ``scout.battery = 80`` on the left side triggers the setter.
   - Assigning an invalid value such as ``"full"`` raises a ``ValueError``.
   - The caller never needs to know that validation is happening.


.. dropdown:: Read-Only Properties
   :open:

   If you define only the getter (no setter), the property becomes read-only.

   .. code-block:: python

      class Robot:
          def __init__(self, name: str):
              self._name = name

          @property
          def name(self) -> str:
              return self._name

          @name.setter
          def name(self, value):
              raise AttributeError("Cannot rename a robot after creation")

      scout = Robot("Scout")
      print(scout.name)      # Scout
      # scout.name = "Bob"   # AttributeError: Cannot rename a robot after creation


.. dropdown:: Encapsulation Summary
   :open:

   - Prefix non-public attributes with an underscore (``_name``).
   - Use ``@property`` for controlled access instead of explicit getters/setters.
   - While the ``property()`` built-in function works, the decorator syntax is preferred.


Putting It All Together
====================================================

This section combines the concepts from the entire lecture into a comprehensive exercise.


Summary
--------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card::
        :class-card: sd-border-primary

        - **OOP Fundamentals** -- Objects bundle data and behavior; Python is multi-paradigm
        - **Design Phase** -- Identify objects, define classes, establish relationships, model behavior
        - **Classes and Objects** -- Classes are blueprints; objects are instances with their own state
        - **``self`` and ``__init__``** -- ``self`` refers to the instance; ``__init__`` initializes attributes

    .. grid-item-card::
        :class-card: sd-border-primary

        - **Attributes** -- Instance attributes are per-object; class attributes are shared
        - **Dunder Methods** -- Customize ``print()``, operators, ``in``, ``for``, and callable behavior
        - **Abstraction** -- Hide implementation details behind a clean interface
        - **Encapsulation** -- Use ``_prefix`` convention and ``@property`` to protect state

.. list-table:: Concepts at a Glance
   :widths: 25 30 30
   :header-rows: 1
   :class: compact-table

   * - Concept
     - Mechanism
     - Use Case
   * - Class definition
     - ``class MyClass:``
     - Blueprint for objects
   * - Constructor
     - ``__init__(self, ...)``
     - Initialize attributes
   * - String representation
     - ``__str__``, ``__repr__``
     - Human/debug output
   * - Operators
     - ``__add__``, ``__eq__``, etc.
     - Custom arithmetic/comparison
   * - Encapsulation
     - ``_attr`` + ``@property``
     - Controlled attribute access

.. note::

   **Reminder**: Review and experiment with all provided code before next class.


Preview: What's Next in L7
---------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: L7: Object-Oriented Programming II
        :class-card: sd-border-primary

        - Class methods and static methods
        - Relationships: association, aggregation, composition
        - Inheritance (``MobileRobot``, ``ManipulatorRobot``) and ``super()``
        - Polymorphism and duck typing
        - Abstract base classes (``Task`` interface)
        - Data classes

.. note::

   Today's lecture gives you the OOP fundamentals that are essential for understanding relationships, inheritance, and polymorphism in the next lecture.


Appendix: Exception Handling
====================================================

This appendix introduces exception handling, a prerequisite for understanding how classes validate their own data. The ``raise`` statement and ``try``/``except`` blocks are used throughout the OOP implementation to enforce business rules and keep objects in a valid state.



.. dropdown:: What Happens When Things Go Wrong?
   :open:

   Programs encounter errors at runtime: invalid input, missing files, impossible calculations. Without a mechanism to handle these errors, the program crashes immediately.

   .. code-block:: python

      def compute_speed(distance: float, time: float) -> float:
          return distance / time

      speed = compute_speed(100.0, 0.0)  # ZeroDivisionError!
      print(f"Speed: {speed}")  # This line never runs

   Python uses **exceptions** to signal that something went wrong. An unhandled exception terminates the program and prints a traceback.


.. dropdown:: Common Built-in Exceptions
   :open:

   .. list-table:: Common built-in exceptions in Python
      :widths: 25 55
      :header-rows: 1
      :class: compact-table

      * - Exception
        - Raised When
      * - ``ZeroDivisionError``
        - Dividing by zero
      * - ``TypeError``
        - Wrong type for an operation
      * - ``ValueError``
        - Right type but invalid value
      * - ``IndexError``
        - List index out of range
      * - ``KeyError``
        - Dictionary key not found
      * - ``FileNotFoundError``
        - File does not exist
      * - ``AttributeError``
        - Accessing a nonexistent attribute
      * - ``NotImplementedError``
        - Method not yet implemented

   .. note::

      All exceptions inherit from ``BaseException``. The ones we typically catch inherit from ``Exception``.


.. dropdown:: The ``try``/``except`` Block
   :open:

   A ``try``/``except`` block lets you catch an exception and respond to it instead of letting the program crash.

   .. code-block:: python

      def compute_speed(distance: float, time: float) -> float:
          return distance / time

      try:
          speed = compute_speed(100.0, 0.0)
          print(f"Speed: {speed}")
      except ZeroDivisionError:
          print("Error: time cannot be zero")

   - Code inside ``try`` runs normally until an exception occurs.
   - If the exception matches the type in ``except``, that block runs instead of crashing.
   - If no exception occurs, the ``except`` block is skipped entirely.


.. dropdown:: Accessing the Exception Object
   :open:

   You can capture the exception object using ``as`` to inspect its message or pass it along.

   .. code-block:: python

      values = [10, 20, 30]

      try:
          print(values[5])
      except IndexError as e:
          print(f"Caught an error: {e}")

   - The variable ``e`` holds the exception instance.
   - Printing ``e`` displays the error message.
   - This is useful for logging errors or displaying user-friendly messages.


.. dropdown:: Handling Multiple Exception Types
   :open:

   You can handle different exceptions separately, or group them in a single ``except`` clause.

   **Separate Handlers**

   .. code-block:: python

      try:
          result = int("abc") / 0
      except ValueError:
          print("Invalid value")
      except ZeroDivisionError:
          print("Cannot divide by 0")

   **Grouped Handler**

   .. code-block:: python

      try:
          result = int("abc") / 0
      except (ValueError, ZeroDivisionError) as e:
          print(f"Error: {e}")

   .. warning::

      Avoid catching bare ``except:`` or ``except Exception:`` unless you have a good reason. Overly broad handlers can hide bugs by silently swallowing unexpected errors.


.. dropdown:: The ``else`` Clause
   :open:

   The ``else`` clause runs only when the ``try`` block completes without raising an exception. It separates the code that might fail from the code that should only run on success.

   .. code-block:: python

      def parse_battery(value: str) -> int:
          try:
              level = int(value)
          except ValueError:
              print(f"Cannot parse '{value}' as an integer")
              return -1
          else:
              print(f"Successfully parsed battery level: {level}")
              return level

      parse_battery("85")     # Successfully parsed battery level: 85
      parse_battery("full")   # Cannot parse 'full' as an integer

   - Code in ``else`` only executes if ``try`` raised no exception.
   - This keeps the ``try`` block minimal: only wrap the code that might fail.
   - Without ``else``, you would place the success logic inside ``try``, which risks accidentally catching exceptions from that logic too.


.. dropdown:: The ``finally`` Clause
   :open:

   The ``finally`` clause runs unconditionally, whether an exception occurred or not. It is used for cleanup actions that must always execute.

   .. code-block:: python

      def read_config(filename: str):
          file = None
          try:
              file = open(filename)
              data = file.read()
              print(f"Loaded {len(data)} characters")
          except FileNotFoundError:
              print(f"'{filename}' not found")
          finally:
              if file is not None:
                  file.close()
              print("Cleanup complete")

      read_config("robot.cfg")
      # 'robot.cfg' not found
      # Cleanup complete

   - ``finally`` executes after ``try``, ``except``, and ``else``, regardless of the outcome.
   - Common use cases: closing files, releasing network connections, resetting hardware.
   - The ``finally`` block runs even if a ``return`` statement is reached inside ``try`` or ``except``.


.. dropdown:: The Full ``try`` Statement
   :open:

   All four clauses can be combined. The execution order is always: ``try``, then ``except`` or ``else``, then ``finally``.

   .. code-block:: python

      def read_sensor(value: str) -> float:
          try:
              reading = float(value)
          except ValueError:
              print(f"Invalid: {value}")
              reading = 0.0
          else:
              print(f"Valid: {reading}")
          finally:
              print("Read attempt complete")
          return reading

      read_sensor("42.5")
      # Valid: 42.5
      # Read attempt complete

      read_sensor("bad")
      # Invalid: bad
      # Read attempt complete

   .. note::

      **Rule of thumb**: Use ``else`` to keep the ``try`` block minimal. Use ``finally`` for cleanup that must happen regardless of success or failure. Neither clause is required, but both improve code clarity when used appropriately.


.. dropdown:: The ``raise`` Statement
   :open:

   The ``raise`` statement lets you **signal an error explicitly** when your code detects an invalid condition. This is how you enforce rules and constraints in your own functions and classes.

   .. code-block:: python

      def set_battery(level: int):
          if not isinstance(level, int):
              raise TypeError("Battery level must be an integer")
          if not (0 <= level <= 100):
              raise ValueError("Battery level must be between 0 and 100")
          print(f"Battery set to {level}%")

      set_battery(80)       # Battery set to 80%
      set_battery("full")   # TypeError: Battery level must be an integer
      set_battery(150)      # ValueError: Battery level must be between 0 and 100

   - ``raise ExceptionType("message")`` creates an exception object and immediately stops normal execution.
   - Choose the exception type that best describes the problem: ``TypeError`` for wrong types, ``ValueError`` for invalid values.
   - The caller can catch these exceptions with ``try``/``except``.


.. dropdown:: Why ``raise`` Matters for OOP
   :open:

   Later in this lecture, we write classes that validate their own data. The ``raise`` statement is the mechanism that makes this possible.

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              if not isinstance(battery, int) or not (0 <= battery <= 100):
                  raise ValueError("Battery must be an integer between 0 and 100")
              self._name = name
              self._battery = battery

      robot = Robot("Scout", 80)   # OK
      robot = Robot("Scout", 200)  # ValueError!

   .. note::

      **Key Idea**: Classes use ``raise`` to reject invalid data at the point of entry. This keeps objects in a valid state and prevents bugs from propagating through the rest of the program.


.. dropdown:: ``return NotImplemented`` vs. ``raise NotImplementedError``
   :open:

   These look similar but serve completely different purposes.

   **``return NotImplemented``**

   - ``NotImplemented`` is a **value**, not an exception. You ``return`` it, never ``raise`` it.
   - Used inside dunder methods (``__eq__``, ``__gt__``, ``__add__``, etc.).
   - When Python receives ``NotImplemented``, it tries the reflected method on the other operand (e.g., ``other.__eq__(self)``).

   .. code-block:: python

      class Sensor:
          def __init__(self, sensor_type: str, range_m: float):
              self.sensor_type = sensor_type
              self.range_m = range_m

          def __eq__(self, other):
              if isinstance(other, Sensor):
                  return self.range_m == other.range_m
              return NotImplemented

      if __name__ == "__main__":
          lidar = Sensor("lidar", 50.0)
          camera = Sensor("camera", 50.0)
          ultrasonic = Sensor("ultrasonic", 30.0)
          print(lidar == camera)      # True
          print(lidar == ultrasonic)  # False
          print(lidar == "lidar")     # False

   **``raise NotImplementedError``**

   - ``NotImplementedError`` is an **exception**. You ``raise`` it, never ``return`` it.
   - Used in methods that are meant to be overridden by subclasses (covered in L7).
   - Calling the method without overriding it crashes immediately with a clear error message.

   .. code-block:: python

      class Robot:
          def __init__(self, name: str):
              self.name = name

          def move(self, direction: str):
              raise NotImplementedError("Subclasses must implement move()")

      if __name__ == "__main__":
          robot = Robot("Base")
          robot.move("north")
          # NotImplementedError: Subclasses must implement move()

   .. warning::

      A common mistake is writing ``raise NotImplemented`` (without "Error"). This technically works but raises a confusing ``TypeError`` instead. Always use ``raise NotImplementedError``.
