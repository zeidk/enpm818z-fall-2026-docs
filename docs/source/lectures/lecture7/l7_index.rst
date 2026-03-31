====================================================
L7: Object-Oriented Programming -- Part II
====================================================

Overview
--------

This lecture extends the OOP foundation from L6 into more advanced class
design. You will learn how class methods and static methods differ from
instance methods, how to implement the three object relationships
(association, aggregation, and composition) identified in the design
phase, and how to build class hierarchies using inheritance and
``super()``. The lecture then covers polymorphism through duck typing and
method overriding, and abstract base classes as a way to enforce a
consistent interface across subclasses. Three additional topics are
included for your information: data classes for reducing boilerplate,
``__slots__`` for memory-efficient attribute storage, and
``typing.Protocol`` for structural subtyping without inheritance. All
examples continue with the Robotics Competition Management System
running domain introduced in L6.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Distinguish between class methods, static methods, and instance methods.
- Explain and implement association, aggregation, and composition.
- Use inheritance to create class hierarchies with ``super()``.
- Understand generalization and specialization in class design.
- Apply polymorphism through duck typing and method overriding.
- Define abstract base classes with the ``abc`` module.
- Use ``typing.Protocol`` for structural subtyping and flexible interfaces.
- Use ``__slots__`` to restrict attributes and reduce memory overhead.
- Use ``@dataclass`` to reduce boilerplate for data-centric classes.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   l7_lecture
   l7_exercises
   l7_quiz
   l7_references


Next Steps
----------

- In the next lecture, we will begin working with ROS 2:

  - What ROS 2 is and why it matters for robotics
  - Nodes, topics, messages, and the ROS 2 computation graph
  - Writing your first publisher and subscriber in Python
  - Building and running ROS 2 packages

- Review and experiment with all code snippets and exercises from today's
  lecture.
- Practice building class hierarchies with abstract base classes.
- Read the `ROS 2 Jazzy Beginner Tutorials
  <https://docs.ros.org/en/jazzy/Tutorials.html>`_.