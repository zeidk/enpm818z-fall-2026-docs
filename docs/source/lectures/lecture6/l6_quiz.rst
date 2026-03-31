====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 6: Object-Oriented
Programming I, including OOP principles, design phase (requirement
analysis, business rules, noun/verb analysis), classes and objects,
``self``, ``__init__``, instance and class attributes, dunder methods,
operator overloading, abstraction, encapsulation, ``@property``, and
exception handling (appendix).

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

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self.name = name
              self.battery = battery

      scout = Robot("Scout")
      print(scout.battery)

   A. ``None``

   B. ``100``

   C. ``TypeError``

   D. ``"Scout"``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``100``

   The ``battery`` parameter has a default value of ``100``. Since no value was passed for ``battery``, it defaults to ``100``.


.. admonition:: Question 2
   :class: hint

   What does ``self`` refer to in a Python method?

   A. The class itself.

   B. The module the class is defined in.

   C. The specific instance that called the method.

   D. The parent class.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The specific instance that called the method.

   When you call ``obj.method(arg)``, Python translates this to ``ClassName.method(obj, arg)``. The ``self`` parameter receives the instance that called the method.


.. admonition:: Question 3
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      class Counter:
          count = 0

          def __init__(self):
              Counter.count += 1

      a = Counter()
      b = Counter()
      c = Counter()
      print(Counter.count)

   A. ``0``

   B. ``1``

   C. ``3``

   D. ``AttributeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``3``

   ``count`` is a class attribute shared by all instances. Each call to ``__init__`` increments it by 1. After three instances are created, ``Counter.count`` is ``3``.


.. admonition:: Question 4
   :class: hint

   Which dunder method is called when you use ``print()`` on an object?

   A. ``__repr__``

   B. ``__str__``

   C. ``__print__``

   D. ``__format__``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``__str__``

   ``print()`` calls ``str()`` on the object, which invokes ``__str__``. If ``__str__`` is not defined, Python falls back to ``__repr__``.


.. admonition:: Question 5
   :class: hint

   What should a dunder method return when it does not know how to handle the other operand's type?

   A. ``None``

   B. ``False``

   C. ``raise NotImplementedError``

   D. ``NotImplemented``

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ``NotImplemented``

   Returning the singleton ``NotImplemented`` (not raising ``NotImplementedError``) signals to Python that the operation is not supported for this type combination. Python then tries the reflected operation on the other operand.


.. admonition:: Question 6
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      class Sensor:
          def __init__(self, sensor_type: str, range_m: float):
              self.sensor_type = sensor_type
              self.range_m = range_m

          def __eq__(self, other):
              if isinstance(other, Sensor):
                  return self.range_m == other.range_m
              return NotImplemented

      lidar = Sensor("lidar", 50.0)
      camera = Sensor("camera", 50.0)
      print(lidar == camera)

   A. ``False``

   B. ``True``

   C. ``NotImplemented``

   D. ``TypeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``True``

   The ``__eq__`` method compares sensors by ``range_m``. Both sensors have ``range_m = 50.0``, so they are considered equal regardless of their ``sensor_type``.


.. admonition:: Question 7
   :class: hint

   What happens when you assign a value to a property that has no setter defined?

   A. The value is silently ignored.

   B. ``AttributeError`` is raised.

   C. The value is assigned to a new instance attribute with the same name.

   D. ``TypeError`` is raised.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``AttributeError`` is raised.

   If a property has only a getter (no ``@property_name.setter``), attempting to assign a value raises ``AttributeError: property 'name' of 'ClassName' object has no setter``.


.. admonition:: Question 8
   :class: hint

   What is the difference between an instance attribute and a class attribute?

   A. Instance attributes are defined with ``self``; class attributes are defined with ``cls``.

   B. Instance attributes belong to a specific object; class attributes are shared by all instances.

   C. Instance attributes are private; class attributes are public.

   D. There is no difference; the terms are interchangeable.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Instance attributes belong to a specific object; class attributes are shared by all instances.

   Instance attributes are created in ``__init__`` using ``self.attr = value`` and each object gets its own copy. Class attributes are defined in the class body (outside any method) and are shared across all instances.


.. admonition:: Question 9
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      class Robot:
          def __init__(self, name: str):
              self._name = name
              self._battery = 100

          @property
          def battery(self) -> int:
              return self._battery

          @battery.setter
          def battery(self, value: int):
              if not isinstance(value, int) or not (0 <= value <= 100):
                  raise ValueError("Invalid battery")
              self._battery = value

      scout = Robot("Scout")
      scout.battery = 80
      print(scout.battery)

   A. ``100``

   B. ``80``

   C. ``ValueError``

   D. ``AttributeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``80``

   ``scout.battery = 80`` triggers the setter, which validates that ``80`` is a valid integer in [0, 100] and assigns it. ``scout.battery`` then triggers the getter and returns ``80``.


.. admonition:: Question 10
   :class: hint

   In the noun/verb analysis technique, what do nouns and verbs typically map to in OOP?

   A. Nouns map to methods; verbs map to attributes.

   B. Nouns map to classes or attributes; verbs map to methods.

   C. Nouns map to modules; verbs map to functions.

   D. Nouns map to variables; verbs map to operators.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Nouns map to classes or attributes; verbs map to methods.

   In noun/verb analysis, nouns from the problem description become candidate classes or attributes, verbs become candidate methods, and relational phrases ("has a", "is a") inform class relationships.


.. admonition:: Question 11
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      class Robot:
          def __init__(self, name: str):
              self.name = name
              self.log: list[str] = []

          def __contains__(self, item: str):
              return item in self.log

          def __call__(self, task: str):
              self.log.append(task)

      scout = Robot("Scout")
      scout("pick widget")
      print("pick widget" in scout)

   A. ``True``

   B. ``False``

   C. ``TypeError``

   D. ``["pick widget"]``

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- ``True``

   ``scout("pick widget")`` triggers ``__call__``, which appends ``"pick widget"`` to the log. ``"pick widget" in scout`` triggers ``__contains__``, which checks the log and returns ``True``.


.. admonition:: Question 12
   :class: hint

   What is the primary purpose of ``__init__``?

   A. To create the object in memory.

   B. To initialize the object's attributes after it has been created.

   C. To define the class's methods.

   D. To destroy the object when it is no longer needed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To initialize the object's attributes after it has been created.

   ``__init__`` is an initializer, not a constructor. The actual object creation happens in ``__new__`` (rarely overridden). ``__init__`` sets up the object's initial state by assigning values to its attributes.


.. admonition:: Question 13
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      class Robot:
          def __init__(self, name: str, battery: int = 100):
              self.name = name
              self.battery = battery

          def __repr__(self) -> str:
              return f"Robot('{self.name}', {self.battery})"

      robots = [Robot("Scout", 80), Robot("Hauler", 60)]
      print(robots)

   A. ``[Scout (80%), Hauler (60%)]``

   B. ``[Robot('Scout', 80), Robot('Hauler', 60)]``

   C. ``[<Robot object>, <Robot object>]``

   D. ``TypeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``[Robot('Scout', 80), Robot('Hauler', 60)]``

   When you print a list, Python calls ``__repr__`` on each element (not ``__str__``). The ``__repr__`` method returns the string that looks like a valid constructor call.


.. admonition:: Question 14
   :class: hint

   Which of the following correctly describes operator overloading?

   A. A child class replaces a method inherited from its parent class.

   B. Teaching Python what an existing operator should do when applied to your own class.

   C. Using multiple operators in a single expression.

   D. Defining multiple functions with the same name but different parameters.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Teaching Python what an existing operator should do when applied to your own class.

   Operator overloading lets you give meaning to operators like ``+``, ``==``, and ``>`` for your custom classes by implementing the corresponding dunder methods (``__add__``, ``__eq__``, ``__gt__``).


.. admonition:: Question 15
   :class: hint

   What naming convention signals that an attribute is non-public in Python?

   A. Prefixing with ``public_``

   B. Suffixing with ``_private``

   C. Prefixing with a single underscore (``_name``)

   D. Using all uppercase letters (``NAME``)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Prefixing with a single underscore (``_name``)

   A single leading underscore signals "non-public by convention." Python does not enforce this, but other developers understand that the attribute should be accessed through the provided interface (e.g., a ``@property``) rather than directly.


----


True or False
=============

.. admonition:: Question 16
   :class: hint

   **True or False:** In Python, ``__init__`` is the constructor that creates the object in memory.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``__init__`` is an initializer, not a constructor. It sets up the object's attributes after the object has already been created. The actual constructor is ``__new__``, which is rarely overridden.


.. admonition:: Question 17
   :class: hint

   **True or False:** Class attributes are shared by all instances of a class.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Class attributes are defined in the class body outside any method. All instances share the same class attribute. If you modify it through the class (``ClassName.attr = value``), the change is visible to all instances.


.. admonition:: Question 18
   :class: hint

   **True or False:** If ``__str__`` is not defined on a class, calling ``print()`` on an instance will raise an error.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   If ``__str__`` is not defined, Python falls back to ``__repr__``. If neither is defined, Python uses the default ``object.__repr__``, which returns something like ``<__main__.Robot object at 0x7f...>``.


.. admonition:: Question 19
   :class: hint

   **True or False:** The ``@property`` decorator allows you to access a method as if it were an attribute.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The ``@property`` decorator transforms a method into a read-only attribute. Combined with a setter, it provides a clean interface: ``obj.attr`` triggers the getter, and ``obj.attr = value`` triggers the setter with validation.


.. admonition:: Question 20
   :class: hint

   **True or False:** In Python, a single leading underscore (``_name``) makes an attribute truly private and inaccessible from outside the class.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Python does not enforce access control. A single leading underscore is a convention that signals "non-public," but the attribute is still accessible from outside the class. Python relies on the "consenting adults" principle.


.. admonition:: Question 21
   :class: hint

   **True or False:** ``return NotImplemented`` and ``raise NotImplementedError`` serve the same purpose.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``return NotImplemented`` is a signal to Python's runtime inside dunder methods, telling Python to try the reflected operation on the other operand. ``raise NotImplementedError`` is a standard exception used in abstract or stub methods to indicate that a subclass must provide an implementation.


.. admonition:: Question 22
   :class: hint

   **True or False:** Every Python class implicitly inherits from ``object``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   In Python 3, all classes implicitly inherit from ``object`` if no explicit base class is specified. This is why all objects have default implementations of dunder methods like ``__repr__`` and ``__eq__``.


.. admonition:: Question 23
   :class: hint

   **True or False:** Creating new attributes outside ``__init__`` (e.g., inside other methods) is considered best practice.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   All attributes should be initialized in ``__init__``, even if they start as empty values or ``None``. Creating attributes in other methods makes the class harder to understand and can lead to ``AttributeError`` if a method is called before the attribute is set.


.. admonition:: Question 24
   :class: hint

   **True or False:** When you print a list of objects, Python calls ``__str__`` on each element.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   When you print a list, Python calls ``__repr__`` on each element, not ``__str__``. The ``__str__`` method is only called when you use ``print()`` or ``str()`` directly on a single object.


.. admonition:: Question 25
   :class: hint

   **True or False:** Abstraction and encapsulation are the same concept.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Abstraction is about hiding *what* an object does internally behind a clean interface. Encapsulation is about bundling data and methods together and controlling *how* the data is accessed. They are related but distinct: abstraction focuses on interface design, encapsulation focuses on data protection.


----


Essay Questions
===============

.. admonition:: Question 26
   :class: hint

   **Explain the difference between a class and an object (instance).** Provide a brief example.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A class is a blueprint that defines the structure and behavior (attributes and methods) that its objects will have.
   - An object (instance) is a concrete realization of a class with its own independent state.
   - Multiple objects can be created from the same class, each with different attribute values.
   - Example: ``Robot`` is a class; ``scout = Robot("Scout")`` creates an object with its own name and battery.


.. admonition:: Question 27
   :class: hint

   **Explain the difference between ``__str__`` and ``__repr__``.** When would you implement each one?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``__str__`` is for human-readable output (used by ``print()`` and ``str()``); ``__repr__`` is for developer-oriented output (used by ``repr()``, the REPL, and inside containers).
   - A good ``__repr__`` should look like the code you would type to create that object, enabling a developer to reproduce it from the output.
   - If you only implement one, implement ``__repr__``; it serves as the fallback for ``__str__``.
   - When printing a list, Python calls ``__repr__`` on each element, not ``__str__``.


.. admonition:: Question 28
   :class: hint

   **Explain how the ``@property`` decorator provides encapsulation in Python.** Why is it preferred over explicit getter/setter methods?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The ``@property`` decorator allows you to add validation and computed access to attributes while preserving attribute-style syntax (``obj.attr`` instead of ``obj.get_attr()``).
   - The non-public attribute (``_attr``) stores the actual data, while the property provides the controlled interface.
   - It is preferred because it is Pythonic: the caller does not need to know that validation is happening, and you can add validation later without changing the external interface.
   - The setter can reject invalid values by raising exceptions, keeping the object in a valid state.


.. admonition:: Question 29
   :class: hint

   **Describe the five-step design workflow covered in this lecture.** Why is the workflow described as iterative?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The five steps are: requirement analysis (what the system must do), business rules (constraints and invariants), noun/verb analysis (extracting classes, attributes, and methods), modeling (UML diagrams for structure and behavior), and implementation (translating to code).
   - The workflow is iterative because your first pass will not be perfect. Implementing code often reveals gaps in the requirements or design that require revisiting earlier steps.
   - Each step informs the next: business rules shape class validation, noun/verb analysis produces the initial class structure, and modeling reveals missing relationships.
   - The design phase is not a one-time activity; it is refined throughout development.


.. admonition:: Question 30
   :class: hint

   **What is operator overloading?** 

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Operator overloading teaches Python what an existing operator (like ``+`` or ``==``) should do when applied to your class, by implementing the corresponding dunder method (e.g., ``__add__``, ``__eq__``).
   - Overloading example: implementing ``__add__`` on ``Sensor`` so that ``lidar + camera`` returns a new fused sensor.


----


Exception Handling (Appendix)
=============================

.. admonition:: Question 31
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def compute_speed(distance: float, time: float) -> float:
          return distance / time

      try:
          speed = compute_speed(100.0, 0.0)
          print(f"Speed: {speed}")
      except ZeroDivisionError:
          print("Cannot divide by zero")

   A. ``Speed: inf``

   B. ``Cannot divide by zero``

   C. ``ZeroDivisionError: float division by zero``

   D. ``None``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``Cannot divide by zero``

   Dividing by ``0.0`` raises a ``ZeroDivisionError``. The ``except`` block catches it and prints the error message instead of crashing.


.. admonition:: Question 32
   :class: hint

   What is the purpose of the ``else`` clause in a ``try``/``except`` block?

   A. It runs when an exception is raised.

   B. It runs only when the ``try`` block completes without raising an exception.

   C. It runs regardless of whether an exception occurred.

   D. It replaces the ``except`` block for unknown exception types.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It runs only when the ``try`` block completes without raising an exception.

   The ``else`` clause separates the code that might fail (inside ``try``) from the code that should only run on success. The ``finally`` clause is the one that runs unconditionally.


.. admonition:: Question 33
   :class: hint

   Which exception type should you raise when a function receives an argument of the correct type but with an invalid value (e.g., a negative battery level)?

   A. ``TypeError``

   B. ``ValueError``

   C. ``AttributeError``

   D. ``NotImplementedError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``ValueError``

   ``ValueError`` is used when the type is correct but the value is invalid. ``TypeError`` is used when the type itself is wrong. For example, passing ``-10`` (an ``int``) when only positive integers are allowed is a ``ValueError``, but passing ``"full"`` (a ``str``) when an ``int`` is expected is a ``TypeError``.
