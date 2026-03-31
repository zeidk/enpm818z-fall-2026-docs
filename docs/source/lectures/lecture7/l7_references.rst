References
==========


.. dropdown:: Lecture 7
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L7: Object-Oriented Programming II**

        Covers class methods (``@classmethod``, factory methods), static
        methods (``@staticmethod``), object relationships (association,
        aggregation, composition), inheritance (``super()``,
        generalization, specialization, MRO, ``isinstance()``,
        ``issubclass()``), polymorphism, duck typing, operator
        overloading, abstract base classes (``ABC``,
        ``@abstractmethod``), data classes (``@dataclass``, ``field()``,
        ``__post_init__``, ``frozen=True``), ``__slots__``, and
        ``typing.Protocol``.


.. dropdown:: Python Language References
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Python Tutorial: Classes
            :link: https://docs.python.org/3/tutorial/classes.html
            :class-card: sd-border-secondary

            **Python Tutorial**

            Official tutorial covering classes, inheritance, MRO, and
            Python's object model.

            +++

            - Inheritance syntax
            - ``super()`` and MRO
            - Multiple inheritance

        .. grid-item-card:: Built-in: classmethod
            :link: https://docs.python.org/3/library/functions.html#classmethod
            :class-card: sd-border-secondary

            **Built-in Functions**

            Documentation for the ``@classmethod`` and ``@staticmethod``
            decorators.

            +++

            - ``cls`` parameter
            - Factory method pattern
            - Subclass-aware construction

        .. grid-item-card:: abc -- Abstract Base Classes
            :link: https://docs.python.org/3/library/abc.html
            :class-card: sd-border-secondary

            **Standard Library -- abc**

            The ``abc`` module for defining abstract base classes and
            abstract methods.

            +++

            - ``ABC``, ``ABCMeta``
            - ``@abstractmethod``
            - Interface enforcement

        .. grid-item-card:: dataclasses module
            :link: https://docs.python.org/3/library/dataclasses.html
            :class-card: sd-border-secondary

            **Standard Library -- dataclasses**

            Full reference for ``@dataclass``, ``field()``,
            ``__post_init__``, and ``frozen=True``.

            +++

            - Auto-generated methods
            - ``field(default_factory=...)``
            - Frozen and hashable instances

        .. grid-item-card:: typing.Protocol
            :link: https://docs.python.org/3/library/typing.html#typing.Protocol
            :class-card: sd-border-secondary

            **Standard Library -- typing**

            Documentation for ``Protocol`` and structural subtyping.

            +++

            - Structural vs. nominal typing
            - ``@runtime_checkable``
            - Static type checking with mypy

        .. grid-item-card:: Python Data Model: __slots__
            :link: https://docs.python.org/3/reference/datamodel.html#slots
            :class-card: sd-border-secondary

            **Python Data Model**

            Reference for ``__slots__``, its memory implications, and
            behavior in inheritance hierarchies.

            +++

            - Replacing ``__dict__``
            - Memory and access-time benefits
            - ``__slots__`` with inheritance


.. dropdown:: UML and Design Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: PlantUML Class Diagrams
            :link: https://plantuml.com/class-diagram
            :class-card: sd-border-secondary

            **PlantUML**

            Syntax reference for class diagrams including association,
            aggregation, composition, and inheritance notation.

            +++

            - Diamond notation (hollow vs. filled)
            - Inheritance arrows
            - Cardinality

        .. grid-item-card:: Mermaid
            :link: https://mermaid.js.org/
            :class-card: sd-border-secondary

            **Mermaid**

            JavaScript-based diagramming tool with Markdown integration
            for class and relationship diagrams.

            +++

            - Class diagrams
            - Relationship syntax
            - GitHub/GitLab rendering


.. dropdown:: External Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Real Python: Inheritance and Composition
            :link: https://realpython.com/inheritance-composition-python/
            :class-card: sd-border-secondary

            **Real Python**

            In-depth guide to inheritance and composition with practical
            examples and trade-off analysis.

            +++

            - "Is-a" vs. "has-a"
            - Composition over inheritance
            - Mixins

        .. grid-item-card:: Real Python: super()
            :link: https://realpython.com/python-super/
            :class-card: sd-border-secondary

            **Real Python**

            Detailed walkthrough of ``super()``, the MRO, and
            cooperative multiple inheritance.

            +++

            - Proxy object mechanics
            - MRO and C3 linearization
            - Multiple inheritance patterns

        .. grid-item-card:: Real Python: Abstract Base Classes
            :link: https://realpython.com/python-interface/
            :class-card: sd-border-secondary

            **Real Python**

            Guide to defining interfaces in Python using ABCs and
            Protocols.

            +++

            - ``ABC`` and ``@abstractmethod``
            - Protocols vs. ABCs
            - When to use each

        .. grid-item-card:: Real Python: Data Classes
            :link: https://realpython.com/python-data-classes/
            :class-card: sd-border-secondary

            **Real Python**

            Comprehensive guide to ``@dataclass``, ``field()``,
            ``__post_init__``, frozen instances, and comparison with
            named tuples and regular classes.

            +++

            - ``@dataclass`` basics
            - Mutable defaults and ``field()``
            - Frozen data classes

        .. grid-item-card:: Real Python: Instance, Class, and Static Methods
            :link: https://realpython.com/instance-class-and-static-methods-demystified/
            :class-card: sd-border-secondary

            **Real Python**

            Side-by-side comparison of the three method types with
            practical use cases.

            +++

            - ``self`` vs. ``cls`` vs. no implicit arg
            - Factory method pattern
            - When to use each type

        .. grid-item-card:: Real Python: __slots__
            :link: https://realpython.com/python-slots/
            :class-card: sd-border-secondary

            **Real Python**

            Deep dive into ``__slots__``, memory profiling, and
            inheritance considerations.

            +++

            - Memory benchmarks
            - ``__slots__`` with properties
            - Limitations and trade-offs

        .. grid-item-card:: Real Python: Protocols in Python
            :link: https://realpython.com/python-protocol/
            :class-card: sd-border-secondary

            **Real Python**

            Guide to ``typing.Protocol``, structural subtyping, and
            ``@runtime_checkable``.

            +++

            - Structural vs. nominal typing
            - Protocol vs. ABC decision guide
            - mypy integration

        .. grid-item-card:: Python Glossary: Duck Typing
            :link: https://docs.python.org/3/glossary.html#term-duck-typing
            :class-card: sd-border-secondary

            **Python Glossary**

            Official definition of duck typing and its role in Python's
            object model.

            +++

            - Duck typing definition
            - Relationship to polymorphism
            - EAFP programming style


.. dropdown:: Style and Best Practices
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: PEP 8 -- Style Guide
            :link: https://peps.python.org/pep-0008/
            :class-card: sd-border-secondary

            **Coding Conventions**

            Guidelines for class naming, method organization, and
            inheritance patterns.

            +++

            - Class names: CamelCase
            - Method naming: ``snake_case``
            - Abstract class conventions

        .. grid-item-card:: Google Python Style Guide
            :link: https://google.github.io/styleguide/pyguide.html
            :class-card: sd-border-secondary

            **Google Style Guide**

            Style conventions used in this course for docstrings and
            code organization.

            +++

            - Google-style docstrings
            - Class and method documentation
            - Type hints


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Luciano Ramalho
            :class-card: sd-border-secondary

            **Fluent Python (2nd Edition)**

            Chapters 11-14 cover the Python data model, special methods,
            interfaces, protocols, and ABCs. Chapters 22-24 cover dynamic
            attributes and descriptors. Essential reading for a deep
            understanding of Python's object model.

        .. grid-item-card:: Mark Lutz
            :class-card: sd-border-secondary

            **Learning Python (5th Edition)**

            Chapters 29-32 cover advanced OOP topics: class design,
            advanced inheritance, operator overloading, and class
            decorators.

        .. grid-item-card:: Brett Slatkin
            :class-card: sd-border-secondary

            **Effective Python (2nd Edition)**

            Items 37-44 cover classes and inheritance, including
            ``super()``, ``@classmethod``, ``@staticmethod``,
            ``@property``, descriptors, and metaclasses.

        .. grid-item-card:: Gamma et al.
            :class-card: sd-border-secondary

            **Design Patterns (Gang of Four)**

            The foundational reference for object-oriented design
            patterns. Factory Method, Composite, and Strategy are
            directly relevant to the patterns introduced in this lecture.
