====================================================
L6: Object-Oriented Programming — Part I
====================================================

Overview
--------

This lecture introduces object-oriented programming (OOP) in Python, covering both the design and implementation of classes. You will learn how to analyze a problem domain using requirement analysis, business rules, and noun/verb analysis, then translate that design into working Python code. The implementation phase covers class and object creation, the ``self`` parameter, the ``__init__`` constructor, instance and class attributes, dunder methods for operator overloading and string representations, and encapsulation using ``@property`` decorators. All examples use a Robotics Competition Management System as the running domain.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain the core principles of object-oriented programming (OOP).
- Gather requirements and identify business rules from a domain description.
- Apply noun/verb analysis to extract candidate classes, attributes, and methods.
- Apply a design process to identify objects, define classes, and model behavior.
- Define classes with attributes and methods using proper Python syntax.
- Understand the role of ``self`` and the ``__init__`` constructor.
- Distinguish between instance attributes and class attributes.
- Override dunder methods: ``__str__``, ``__repr__``, ``__eq__``, and operator methods.
- Understand abstraction and encapsulation as OOP principles.
- Use ``@property`` to create getters and setters the Pythonic way.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   l6_lecture
   l6_exercises
   l6_quiz
   l6_references

Next Steps
----------

- In the next lecture, we will cover Object-Oriented Programming II:

  - Class methods and static methods
  - Relationships: association, aggregation, composition
  - Inheritance (``MobileRobot``, ``ManipulatorRobot``) and ``super()``
  - Polymorphism and duck typing
  - Abstract base classes (``Task`` interface)
  - Data classes

- Review and experiment with all code snippets and exercises from today's lecture.
- Practice writing classes with properties and dunder methods.
- Read `Real Python: Inheritance and Composition <https://realpython.com/inheritance-composition-python/>`_.
