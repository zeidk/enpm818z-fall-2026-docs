References
==========


.. dropdown:: Lecture 6
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L6: Object-Oriented Programming I**

        Covers OOP principles (encapsulation, abstraction, inheritance, polymorphism), design phase (requirement analysis, business rules, noun/verb analysis, UML modeling), classes and objects, ``self``, ``__init__``, instance and class attributes, dunder methods (``__str__``, ``__repr__``, ``__eq__``, ``__add__``, ``__contains__``, ``__iter__``, ``__call__``), operator overloading, abstraction, encapsulation, and ``@property`` decorators.


.. dropdown:: Python Language References
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Python Tutorial: Classes
            :link: https://docs.python.org/3/tutorial/classes.html
            :class-card: sd-border-secondary

            **Python Tutorial**

            Official tutorial covering classes, objects, inheritance, and Python's object model.

            +++

            - Class definition
            - Instance and class attributes
            - Method resolution

        .. grid-item-card:: Data Model: Special Methods
            :link: https://docs.python.org/3/reference/datamodel.html#special-method-names
            :class-card: sd-border-secondary

            **Python Data Model**

            Comprehensive reference for all dunder methods in Python's data model.

            +++

            - ``__init__``, ``__repr__``, ``__str__``
            - Rich comparison methods
            - Numeric and container emulation

        .. grid-item-card:: Built-in Functions: ``property``
            :link: https://docs.python.org/3/library/functions.html#property
            :class-card: sd-border-secondary

            **Built-in Functions**

            Documentation for the ``property()`` built-in and the ``@property`` decorator.

            +++

            - Getter, setter, deleter
            - Descriptor protocol
            - Attribute access control

        .. grid-item-card:: Abstract Base Classes
            :link: https://docs.python.org/3/library/abc.html
            :class-card: sd-border-secondary

            **Standard Library -- abc**

            The ``abc`` module for defining abstract base classes and abstract methods.

            +++

            - ``ABC``, ``abstractmethod``
            - Interface enforcement
            - Preview for L7

        .. grid-item-card:: Errors and Exceptions
            :link: https://docs.python.org/3/tutorial/errors.html
            :class-card: sd-border-secondary

            **Python Tutorial**

            Official tutorial on exception handling, ``try``/``except``, ``raise``, and built-in exception types.

            +++

            - ``try``/``except``/``else``/``finally``
            - ``raise`` statement
            - ``TypeError``, ``ValueError``

        .. grid-item-card:: Glossary: ``__slots__``
            :link: https://docs.python.org/3/glossary.html#term-__slots__
            :class-card: sd-border-secondary

            **Python Glossary**

            Memory-efficient attribute storage using ``__slots__`` (advanced topic).

            +++

            - Fixed attribute sets
            - Memory optimization
            - Trade-offs with dynamic attributes


.. dropdown:: UML and Design Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: UML (Unified Modeling Language)
            :link: https://www.uml.org/
            :class-card: sd-border-secondary

            **Official UML Site**

            The standard for software modeling diagrams used in the design phase.

            +++

            - Class diagrams
            - Sequence diagrams
            - Activity diagrams

        .. grid-item-card:: PlantUML
            :link: https://plantuml.com/
            :class-card: sd-border-secondary

            **PlantUML**

            Text-based tool for creating UML diagrams from simple markup.

            +++

            - Class diagram syntax
            - Sequence diagram syntax
            - Integration with IDEs

        .. grid-item-card:: Mermaid
            :link: https://mermaid.js.org/
            :class-card: sd-border-secondary

            **Mermaid**

            JavaScript-based diagramming tool with Markdown integration.

            +++

            - Class diagrams
            - Flowcharts
            - GitHub/GitLab rendering


.. dropdown:: Style and Best Practices
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: PEP 8 -- Style Guide
            :link: https://peps.python.org/pep-0008/
            :class-card: sd-border-secondary

            **Coding Conventions**

            Guidelines for class naming, attribute access, and code formatting.

            +++

            - Class names: CamelCase
            - Non-public attributes: ``_leading_underscore``
            - Method naming: ``snake_case``

        .. grid-item-card:: Google Python Style Guide
            :link: https://google.github.io/styleguide/pyguide.html
            :class-card: sd-border-secondary

            **Google Style Guide**

            Style conventions used in this course for docstrings and code organization.

            +++

            - Google-style docstrings
            - Class documentation
            - Properties and type hints


.. dropdown:: External Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Real Python: OOP in Python 3
            :link: https://realpython.com/python3-object-oriented-programming/
            :class-card: sd-border-secondary

            **Real Python**

            Comprehensive introduction to OOP in Python with practical examples.

            +++

            - Classes and objects
            - Instance methods
            - Inheritance basics

        .. grid-item-card:: Real Python: Operator and Function Overloading
            :link: https://realpython.com/operator-function-overloading/
            :class-card: sd-border-secondary

            **Real Python**

            Guide to overloading operators and built-in functions for custom classes.

            +++

            - Dunder methods
            - Comparison operators
            - Arithmetic operators

        .. grid-item-card:: Real Python: Properties
            :link: https://realpython.com/python-property/
            :class-card: sd-border-secondary

            **Real Python**

            In-depth guide to the ``@property`` decorator and managed attributes.

            +++

            - Getters and setters
            - Validation
            - Computed attributes

        .. grid-item-card:: Real Python: Inheritance and Composition
            :link: https://realpython.com/inheritance-composition-python/
            :class-card: sd-border-secondary

            **Real Python**

            Guide to inheritance and composition in Python. Preview for L7.

            +++

            - "Is-a" vs. "has-a"
            - Composition over inheritance
            - Mixins


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Python Official Tutorial
            :link: https://docs.python.org/3/tutorial/
            :class-card: sd-border-secondary

            **Getting Started**

            Section 9 (Classes) covers class definition, scopes, inheritance, and iterators.

            +++

            - Class syntax
            - Inheritance
            - Iterators and generators

        .. grid-item-card:: Luciano Ramalho
            :class-card: sd-border-secondary

            **Fluent Python (2nd Edition)**

            Chapters 11-14 cover the Python data model, special methods, operator overloading, and interfaces. Essential reading for understanding how Python objects work.

        .. grid-item-card:: Mark Lutz
            :class-card: sd-border-secondary

            **Learning Python (5th Edition)**

            Chapters 26-32 cover OOP fundamentals: class coding basics, inheritance, class design, and advanced class topics.

        .. grid-item-card:: Brett Slatkin
            :class-card: sd-border-secondary

            **Effective Python (2nd Edition)**

            Items 37-44 cover classes and inheritance, including ``@property``, descriptors, and metaclasses.
