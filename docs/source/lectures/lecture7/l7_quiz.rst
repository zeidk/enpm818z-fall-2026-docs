====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 7: Object-Oriented
Programming II, including class and static methods, object relationships
(association, aggregation, composition), inheritance, ``super()``,
polymorphism, duck typing, abstract base classes, data classes,
``__slots__``, and ``typing.Protocol``.

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

   What is the key difference between a class method and a static method?

   A. A class method can only be called on instances; a static method can
      only be called on the class.

   B. A class method receives ``cls`` as its first argument and can access
      class state; a static method receives no implicit argument and has no
      access to instance or class state.

   C. A class method is faster than a static method.

   D. A static method can modify class attributes; a class method cannot.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A class method receives ``cls`` as its first argument and can
   access class state; a static method receives no implicit argument and
   has no access to instance or class state.

   ``@classmethod`` passes the class itself as ``cls``, allowing access
   to class attributes and enabling subclass-aware construction.
   ``@staticmethod`` receives neither ``self`` nor ``cls`` and behaves
   like a plain function that lives in the class namespace for
   organizational reasons.


.. admonition:: Question 2
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      class Robot:
          total_robots = 0

          def __init__(self, name: str):
              self._name = name
              Robot.total_robots += 1

          @classmethod
          def get_fleet_size(cls) -> str:
              return f"Fleet size: {cls.total_robots}"

      Robot("Scout")
      Robot("Hauler")
      print(Robot.get_fleet_size())

   A. ``Fleet size: 0``

   B. ``Fleet size: 1``

   C. ``Fleet size: 2``

   D. ``AttributeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``Fleet size: 2``

   Each call to ``Robot(...)`` increments the class attribute
   ``total_robots`` by 1. After two instances are created,
   ``total_robots`` is 2. ``get_fleet_size()`` is a class method that
   reads the class attribute via ``cls.total_robots``.


.. admonition:: Question 3
   :class: hint

   Which object relationship is best described as "the part cannot exist
   independently of the whole"?

   A. Association

   B. Aggregation

   C. Composition

   D. Inheritance

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Composition

   In composition, the parts are created inside the whole's ``__init__``
   and their lifetime is tied to the whole. Destroying the whole destroys
   the parts. Example: a ``Robot`` owns its ``Sensor``\(s); the sensors
   have no meaning outside the robot that created them.


.. admonition:: Question 4
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      class Animal:
          def __init__(self, name: str, age: int):
              self._name = name
              self._age = age

      class Dog(Animal):
          def __init__(self, name: str, age: int, breed: str):
              super().__init__(name, age)
              self._breed = breed

      rex = Dog("Rex", 5, "Labrador")
      print(rex._name, rex._age, rex._breed)

   A. ``AttributeError``

   B. ``Rex 5 Labrador``

   C. ``None None Labrador``

   D. ``TypeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``Rex 5 Labrador``

   ``Dog.__init__`` calls ``super().__init__(name, age)``, which
   delegates to ``Animal.__init__`` and sets ``_name`` and ``_age``.
   ``Dog.__init__`` then sets ``_breed``. All three attributes are
   available on the instance.


.. admonition:: Question 5
   :class: hint

   What happens when you try to instantiate a class that inherits from
   ``ABC`` and does not implement all of its abstract methods?

   A. The instance is created but the missing methods raise
      ``NotImplementedError`` when called.

   B. Python raises ``TypeError`` at instantiation time.

   C. Python raises ``AttributeError`` at instantiation time.

   D. The instance is created successfully; no error is raised.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Python raises ``TypeError`` at instantiation time.

   Python checks at instantiation time whether all abstract methods have
   been implemented. If any are missing, it raises ``TypeError`` with a
   message listing the unimplemented methods. This catches the omission
   at the earliest possible point, not when the method is first called.


.. admonition:: Question 6
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      class Animal:
          def __init__(self, name: str):
              self._name = name

      class Cat(Animal):
          def make_sound(self) -> None:
              print(f"{self._name} says: Meow")

      class Dog(Animal):
          def make_sound(self) -> None:
              print(f"{self._name} says: Woof")

      animals = [Cat("Kitty"), Dog("Rex")]
      for a in animals:
          a.make_sound()

   A. ``TypeError: make_sound not defined on Animal``

   B. ``Kitty says: Meow`` then ``Rex says: Woof``

   C. ``Meow`` then ``Woof``

   D. ``AttributeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``Kitty says: Meow`` then ``Rex says: Woof``

   This is duck typing in action. ``Cat`` and ``Dog`` each define
   ``make_sound()`` independently. The loop calls the method on each
   object without checking its type. Python resolves the correct
   implementation at runtime based on the actual type of each object.


.. admonition:: Question 7
   :class: hint

   Which of the following correctly describes the difference between
   aggregation and composition?

   A. Aggregation uses a hollow diamond in UML; composition uses a filled
      diamond. In aggregation the part can outlive the whole; in
      composition the part is destroyed with the whole.

   B. Aggregation uses a filled diamond in UML; composition uses a hollow
      diamond. In aggregation the part is destroyed with the whole; in
      composition it can outlive the whole.

   C. Aggregation and composition are identical; they differ only in UML
      notation.

   D. Aggregation implies inheritance; composition does not.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- Aggregation uses a hollow diamond; composition uses a filled
   diamond. In aggregation the part can outlive the whole; in composition
   the part is destroyed with the whole.

   The key distinction is lifetime dependency. In aggregation, parts are
   created outside and passed in; deleting the container leaves the parts
   intact. In composition, parts are created inside ``__init__`` and
   owned exclusively by the whole.


.. admonition:: Question 8
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      from dataclasses import dataclass

      @dataclass
      class Animal:
          name: str
          age: int
          weight: float

      kitty = Animal("Kitty", 3, 4.2)
      print(kitty)

   A. ``<__main__.Animal object at 0x...>``

   B. ``Animal(name='Kitty', age=3, weight=4.2)``

   C. ``{'name': 'Kitty', 'age': 3, 'weight': 4.2}``

   D. ``TypeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``Animal(name='Kitty', age=3, weight=4.2)``

   ``@dataclass`` auto-generates ``__repr__`` from the class's
   type-annotated fields. The generated representation lists each field
   name and value in declaration order.


.. admonition:: Question 9
   :class: hint

   What does ``super()`` return?

   A. The parent class itself.

   B. A new instance of the parent class.

   C. A proxy object that routes method calls to the next class in the MRO.

   D. The ``__init__`` method of the parent class.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- A proxy object that routes method calls to the next class in
   the MRO.

   ``super()`` does not return the parent class directly. It returns a
   proxy that knows your position in the MRO and delegates calls to the
   appropriate next class in the chain. This is what makes ``super()``
   work correctly in multiple inheritance scenarios.


.. admonition:: Question 10
   :class: hint

   What is the primary advantage of ``__slots__`` over a regular class?

   A. It allows dynamic addition of new attributes at runtime.

   B. It replaces ``__dict__`` with a fixed structure, reducing memory
      usage and speeding up attribute access.

   C. It automatically generates ``__init__``, ``__repr__``, and
      ``__eq__``.

   D. It prevents a class from being subclassed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It replaces ``__dict__`` with a fixed structure, reducing
   memory usage and speeding up attribute access.

   Every regular instance carries a ``__dict__`` that costs roughly
   232 bytes. ``__slots__`` replaces it with a compact array of named
   slots. The trade-off is that dynamic attribute assignment is no longer
   allowed after instantiation.


.. admonition:: Question 11
   :class: hint

   Which of the following is true about ``typing.Protocol``?

   A. A class must explicitly inherit from the Protocol to be considered
      compatible.

   B. A class satisfies a Protocol if it has the required methods,
      regardless of its class hierarchy.

   C. Protocols replace abstract base classes entirely.

   D. Protocols can only be used with ``isinstance()`` checks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A class satisfies a Protocol if it has the required methods,
   regardless of its class hierarchy.

   This is structural subtyping: compatibility is determined by structure
   (the presence of the required methods), not by declaration (explicit
   inheritance). No import or inheritance of the Protocol is needed in
   the implementing class.


.. admonition:: Question 12
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      class Animal:
          pass

      class Cat(Animal):
          pass

      kitty = Cat()
      print(isinstance(kitty, Cat))
      print(isinstance(kitty, Animal))
      print(issubclass(Animal, Cat))

   A. ``True``, ``True``, ``True``

   B. ``True``, ``True``, ``False``

   C. ``True``, ``False``, ``False``

   D. ``False``, ``True``, ``False``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``True``, ``True``, ``False``

   ``isinstance(kitty, Cat)`` is ``True`` because ``kitty`` is a ``Cat``.
   ``isinstance(kitty, Animal)`` is ``True`` because ``Cat`` is a
   subclass of ``Animal`` (is-a relationship). ``issubclass(Animal, Cat)``
   is ``False`` because the parent is not a subclass of its child.


.. admonition:: Question 13
   :class: hint

   What is the correct way to declare a mutable default field in a
   ``@dataclass``?

   A. ``tags: list[str] = []``

   B. ``tags: list[str] = list``

   C. ``tags: list[str] = field(default_factory=list)``

   D. ``tags: list[str] = field(default=[])``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``tags: list[str] = field(default_factory=list)``

   Mutable defaults like ``[]`` cannot be used directly because Python
   would share the same list across all instances. ``field(default_factory=list)``
   calls ``list()`` for each new instance, producing an independent empty
   list. Option D is invalid because ``field(default=...)`` requires an
   immutable value.


.. admonition:: Question 14
   :class: hint

   In the following code, what is the MRO of ``Dog``?

   .. code-block:: python

      class Animal:
          pass

      class Dog(Animal):
          pass

   A. ``Dog -> object``

   B. ``Dog -> Animal``

   C. ``Dog -> Animal -> object``

   D. ``Animal -> Dog -> object``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``Dog -> Animal -> object``

   In single inheritance the MRO is the chain from child to parent,
   ending with ``object``. Every Python class ultimately inherits from
   ``object``, which always appears last. Inspect it with
   ``Dog.__mro__``.


.. admonition:: Question 15
   :class: hint

   Which decorator is required to allow ``isinstance()`` checks against a
   ``typing.Protocol`` at runtime?

   A. ``@abstractmethod``

   B. ``@classmethod``

   C. ``@runtime_checkable``

   D. ``@staticmethod``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``@runtime_checkable``

   By default, ``isinstance()`` cannot check Protocol conformance at
   runtime. Adding ``@runtime_checkable`` to the Protocol enables this
   check. It only verifies the presence of the required methods, not
   their signatures. Full type safety still requires a static type checker
   such as ``mypy``.


----


True or False
=============

.. admonition:: Question 16
   :class: hint

   **True or False:** A static method can access and modify class
   attributes via ``cls``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   A static method receives neither ``self`` nor ``cls``. It has no
   implicit access to instance or class state. To read or modify a class
   attribute inside a static method, you would have to reference the
   class name directly (e.g., ``Robot.total_robots``), which is
   considered poor style. Use a class method instead.


.. admonition:: Question 17
   :class: hint

   **True or False:** In aggregation, deleting the container object also
   destroys the contained objects.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   In aggregation the parts can outlive the whole. Parts are created
   outside the container and passed in. Deleting the container leaves the
   parts intact as long as another reference to them exists. This is the
   key distinction from composition, where the parts' lifetime is tied
   to the whole.


.. admonition:: Question 18
   :class: hint

   **True or False:** ``super().__init__()`` should always be called as
   the first line of a child class's ``__init__``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Calling ``super().__init__()`` first ensures that parent attributes
   are initialized before the child tries to use them. If the child sets
   attributes that depend on parent state before calling
   ``super().__init__()``, those parent attributes do not yet exist and
   an ``AttributeError`` will follow.


.. admonition:: Question 19
   :class: hint

   **True or False:** An abstract class can contain concrete methods
   (methods with a full implementation) alongside abstract methods.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   An abstract class can mix abstract and concrete methods. Concrete
   methods are inherited by all subclasses as-is. Abstract methods define
   the interface that each subclass must implement. This is a common
   pattern: the base class provides shared behavior through concrete
   methods and enforces a contract through abstract methods.


.. admonition:: Question 20
   :class: hint

   **True or False:** Duck typing checks the type label of an object to
   determine whether it is compatible with an interface.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Duck typing checks what an object *can do* (the methods it has), not
   what it *is* (its type or class hierarchy). If an object has the
   required method, it is compatible, regardless of its class. The name
   comes from: "If it walks like a duck and quacks like a duck, then it
   must be a duck."


.. admonition:: Question 21
   :class: hint

   **True or False:** A ``@dataclass(frozen=True)`` instance can be used
   as a dictionary key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``frozen=True`` prevents field modification after creation and
   automatically generates ``__hash__``, making the instance hashable.
   Hashable objects can be used as dictionary keys or stored in sets.
   A regular ``@dataclass`` sets ``__hash__`` to ``None`` by default
   (making it unhashable) because mutable objects should not be hashed.


.. admonition:: Question 22
   :class: hint

   **True or False:** When using ``__slots__``, a child class must
   redeclare all slots from its parent class.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Each class in the hierarchy should declare only the new attributes it
   introduces. Python merges ``__slots__`` from all classes in the chain
   automatically. Redeclaring a parent slot in the child wastes memory
   and can cause subtle bugs.


.. admonition:: Question 23
   :class: hint

   **True or False:** A class must explicitly inherit from a
   ``typing.Protocol`` to satisfy it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   A class satisfies a Protocol through structural subtyping: if it has
   the required methods and attributes, it is compatible, regardless of
   its class hierarchy. No import or inheritance of the Protocol is
   needed in the implementing class. This is the key difference from
   ABCs, which require explicit inheritance (nominal typing).


.. admonition:: Question 24
   :class: hint

   **True or False:** Implementing ``__str__`` and ``__repr__`` in a
   Python class is an example of method overloading.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Implementing ``__str__`` and ``__repr__`` is method *overriding*, not
   overloading. Every Python class already inherits these methods from
   ``object``. Providing your own version replaces the inherited one.
   Method overloading (defining multiple versions of a method with
   different signatures) is not natively supported in Python.


.. admonition:: Question 25
   :class: hint

   **True or False:** ``@abstractmethod`` can only be applied to methods
   that have no body (i.e., ``pass`` or ``...``).

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   An abstract method can have a body. The subclass can call it
   explicitly via ``super().method_name()``, which is useful when the
   base class provides a default behavior that subclasses extend rather
   than replace entirely. In practice, abstract methods with a body are
   rare; an empty body is the norm.


----


Essay Questions
===============

.. admonition:: Question 26
   :class: hint

   **Explain the difference between association, aggregation, and
   composition.** Give a robotics competition example for each.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Association is a general "uses-a" relationship where both objects
     exist independently and neither owns the other. Example: a ``Robot``
     is assigned a ``Task``; the task exists before and after the robot
     executes it.
   - Aggregation is a "has-a" relationship where the part can outlive the
     whole. Parts are created outside the container and passed in.
     Example: a ``Team`` has ``Robot``\(s); dissolving the team does not
     destroy the robots.
   - Composition is a stronger "has-a" relationship where the part cannot
     exist without the whole. Parts are created inside the whole's
     ``__init__``. Example: a ``Robot`` owns its ``Sensor``\(s);
     destroying the robot destroys its sensors.


.. admonition:: Question 27
   :class: hint

   **Explain what polymorphism is and how duck typing achieves it in
   Python.** Why are abstract base classes useful even when duck typing
   already works?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Polymorphism means different objects respond to the same interface in
     their own way. In Python, duck typing is the mechanism: an object is
     compatible if it has the required methods, regardless of its type.
   - Duck typing is flexible but provides no compile-time or
     instantiation-time guarantee. Nothing stops a developer from
     forgetting to implement a required method in a new subclass.
   - Abstract base classes close this gap: ``@abstractmethod`` forces
     Python to raise ``TypeError`` at instantiation time if a required
     method is missing, catching the omission as early as possible.


.. admonition:: Question 28
   :class: hint

   **Explain what ``super()`` returns and why it should be called at the
   start of a child class's ``__init__``.** What goes wrong if you forget
   to call it?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``super()`` returns a proxy object that routes method calls to the
     next class in the MRO. It does not return the parent class directly.
   - It should be called first in the child ``__init__`` so that parent
     attributes are initialized before the child tries to use them.
   - If ``super().__init__()`` is omitted entirely, the parent attributes
     are never set and any method that accesses them will raise
     ``AttributeError``.
   - If it is called after child code that depends on parent attributes,
     those parent attributes do not exist yet, causing the same error.


.. admonition:: Question 29
   :class: hint

   **Compare ABCs and Protocols as mechanisms for defining interfaces in
   Python.** When would you choose one over the other?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ABCs (nominal typing) require the implementing class to explicitly
     inherit from the base class. They enforce the interface at
     instantiation time and are well-suited when subclasses share
     concrete behavior (inherited methods with a body).
   - Protocols (structural typing) require no inheritance. A class
     satisfies a Protocol simply by having the right methods. They are
     better for describing interfaces that unrelated classes can satisfy,
     especially across library or module boundaries.
   - Choose ABCs when you want shared base behavior and strong enforcement
     at instantiation time. Choose Protocols when you want loose coupling
     and flexibility, particularly for type-annotating function parameters.


.. admonition:: Question 30
   :class: hint

   **What is generalization and what is specialization in class design?**
   Describe a scenario where each is the appropriate design activity.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Generalization is a bottom-up activity: you start with several
     concrete classes, identify shared attributes and methods, and move
     them into a new base class. Example: noticing that ``Cat``, ``Dog``,
     and ``Bird`` all have ``name``, ``age``, and ``eat()`` and creating
     an ``Animal`` base class to hold them.
   - Specialization is a top-down activity: you start with a general base
     class and create derived classes that extend or override it for a
     specific context. Example: starting from a ``Robot`` base class and
     creating ``MobileRobot`` (adds ``_speed``) and ``ManipulatorRobot``
     (adds ``_reach_m``).
   - A design smell that signals specialization is needed: a base class
     carrying ``None`` values for attributes that only apply to some
     subclasses (e.g., ``wingspan = None`` on a ``Cat``).
