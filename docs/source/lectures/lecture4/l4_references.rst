References
==========


.. dropdown:: 🏛️ Lecture 4
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L4: Function Fundamentals**

        Covers function definition and calling, arguments (positional, default, keyword, ``*args``, ``**kwargs``), scopes and the LEGB rule, pass-by-assignment, type hints (``Optional``, ``Union``, pipe syntax), Google-style docstrings, and recursion.


.. dropdown:: 🐍 Python Language References
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🔧 Defining Functions
            :link: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
            :class-card: sd-border-secondary

            **Tutorial -- Control Flow**

            Function definition, parameters, return values, and default arguments.

            +++

            - ``def`` keyword
            - Default values
            - Keyword arguments

        .. grid-item-card:: 📦 More on Defining Functions
            :link: https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions
            :class-card: sd-border-secondary

            **Tutorial -- Control Flow**

            Advanced argument handling, ``*args``, ``**kwargs``, and unpacking.

            +++

            - Arbitrary argument lists
            - Unpacking argument lists
            - Lambda expressions

        .. grid-item-card:: 🔍 Scopes and Namespaces
            :link: https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces
            :class-card: sd-border-secondary

            **Tutorial -- Classes**

            Python's scope rules, the LEGB lookup order, and namespace mechanics.

            +++

            - Local, enclosing, global, built-in
            - ``global`` and ``nonlocal``
            - Name resolution

        .. grid-item-card:: 📝 typing Module
            :link: https://docs.python.org/3/library/typing.html
            :class-card: sd-border-secondary

            **Standard Library -- typing**

            Type hints, ``Optional``, ``Union``, and generic types.

            +++

            - Basic annotations
            - ``Optional`` and ``Union``
            - Generic collections

        .. grid-item-card:: 🔄 Pass by Reference FAQ
            :link: https://docs.python.org/3/faq/programming.html#how-do-i-write-a-function-with-output-parameters-call-by-reference
            :class-card: sd-border-secondary

            **Python FAQ**

            Explanation of how Python passes arguments and why it is neither pass-by-value nor pass-by-reference.

            +++

            - Object references
            - Mutable vs immutable
            - Output parameters

        .. grid-item-card:: 🔁 Recursion
            :link: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
            :class-card: sd-border-secondary

            **Tutorial -- Control Flow**

            Recursive function examples and the Fibonacci sequence.

            +++

            - Base case and recursive case
            - Stack depth
            - ``sys.getrecursionlimit()``

        .. grid-item-card:: 📋 Function Annotations
            :link: https://docs.python.org/3/tutorial/controlflow.html#function-annotations
            :class-card: sd-border-secondary

            **Tutorial -- Control Flow**

            How to use function annotations for parameter and return type hints.

            +++

            - Annotation syntax
            - ``__annotations__`` dict
            - PEP 3107

        .. grid-item-card:: 📖 Docstring Conventions
            :link: https://peps.python.org/pep-0257/
            :class-card: sd-border-secondary

            **PEP 257**

            Docstring conventions for modules, functions, classes, and methods.

            +++

            - One-line docstrings
            - Multi-line docstrings
            - ``__doc__`` attribute


.. dropdown:: 📏 Style and Best Practices
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📏 PEP 8 -- Style Guide
            :link: https://peps.python.org/pep-0008/
            :class-card: sd-border-secondary

            **Coding Conventions**

            Guidelines for function naming, parameter formatting, and documentation.

            +++

            - Function naming (``snake_case``)
            - Argument formatting
            - Blank lines around functions

        .. grid-item-card:: 📝 PEP 484 -- Type Hints
            :link: https://peps.python.org/pep-0484/
            :class-card: sd-border-secondary

            **Type Hints**

            The PEP that introduced type hints to Python.

            +++

            - Annotation syntax
            - ``typing`` module
            - Gradual typing

        .. grid-item-card:: 📝 PEP 604 -- Union with X | Y
            :link: https://peps.python.org/pep-0604/
            :class-card: sd-border-secondary

            **Simplified Union Syntax**

            The PEP that introduced ``X | Y`` syntax as an alternative to ``Union[X, Y]`` in Python 3.10+.

            +++

            - Pipe operator for unions
            - ``isinstance()`` support
            - ``Optional`` replacement

        .. grid-item-card:: 📋 Google Python Style Guide
            :link: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
            :class-card: sd-border-secondary

            **Docstrings Section**

            Google's conventions for writing docstrings, including ``Args``, ``Returns``, and ``Raises`` sections.

            +++

            - Function docstrings
            - Args and Returns format
            - Module and class docstrings


.. dropdown:: 📚 Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📘 Python Official Tutorial
            :link: https://docs.python.org/3/tutorial/
            :class-card: sd-border-secondary

            **Getting Started**

            Section 4.7 (Defining Functions) and Section 4.8 (More on Defining Functions) cover this lecture's topics.

            +++

            - Functions and arguments
            - ``*args`` and ``**kwargs``
            - Lambda expressions

        .. grid-item-card:: Mark Lutz
            :class-card: sd-border-secondary

            **Learning Python (5th Edition)**

            Chapters 16-21 cover function basics, scopes, arguments, and advanced function topics in depth.

        .. grid-item-card:: Luciano Ramalho
            :class-card: sd-border-secondary

            **Fluent Python (2nd Edition)**

            Chapters 7-9 cover first-class functions, type hints, decorators, and closures. Excellent for understanding functions as objects.

        .. grid-item-card:: Brett Slatkin
            :class-card: sd-border-secondary

            **Effective Python (2nd Edition)**

            Items 19-26 cover function arguments, return values, closures, and decorators with practical best practices.