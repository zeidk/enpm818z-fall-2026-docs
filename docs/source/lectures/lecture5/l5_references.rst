References
==========


.. dropdown:: 🏛️ Lecture 5
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L5: Advanced Functions**

        Covers programming paradigms (procedural, functional, object-oriented), first-class functions, lambda expressions, closures, callables, decorators (basic, stacking, parameterized), ``functools.wraps``, ``functools.partial``, and built-in higher-order functions (``map``, ``filter``, ``sorted`` with ``key``).


.. dropdown:: 🐍 Python Language References
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🔧 Functional Programming HOWTO
            :link: https://docs.python.org/3/howto/functional.html
            :class-card: sd-border-secondary

            **Python HOWTO**

            Comprehensive guide to functional programming in Python, including iterators, generators, and built-in functional tools.

            +++

            - Pure functions
            - ``map``, ``filter``, ``reduce``
            - Itertools

        .. grid-item-card:: 📝 Lambda Expressions
            :link: https://docs.python.org/3/reference/expressions.html#lambda
            :class-card: sd-border-secondary

            **Python Reference**

            Syntax and semantics of lambda expressions in Python.

            +++

            - Single expression functions
            - Anonymous functions
            - Inline callbacks

        .. grid-item-card:: 🔍 Data Model: ``__call__``
            :link: https://docs.python.org/3/reference/datamodel.html#object.__call__
            :class-card: sd-border-secondary

            **Python Data Model**

            The ``__call__`` special method that makes instances callable.

            +++

            - Callable objects
            - Instance invocation
            - Emulating functions

        .. grid-item-card:: 📦 Built-in: ``callable()``
            :link: https://docs.python.org/3/library/functions.html#callable
            :class-card: sd-border-secondary

            **Built-in Functions**

            The ``callable()`` function for checking if an object is callable.

            +++

            - Runtime check
            - Functions, classes, instances
            - ``__call__`` detection

        .. grid-item-card:: 🔄 ``functools.partial``
            :link: https://docs.python.org/3/library/functools.html#functools.partial
            :class-card: sd-border-secondary

            **Standard Library -- functools**

            Creating partial function objects with frozen arguments.

            +++

            - Argument freezing
            - ``.func``, ``.args``, ``.keywords``
            - Partial objects

        .. grid-item-card:: 📋 ``functools.wraps``
            :link: https://docs.python.org/3/library/functools.html#functools.wraps
            :class-card: sd-border-secondary

            **Standard Library -- functools**

            Preserving function metadata when writing decorators.

            +++

            - Metadata copying
            - ``__name__``, ``__doc__``
            - Decorator best practice

        .. grid-item-card:: 📖 Glossary: Decorator
            :link: https://docs.python.org/3/glossary.html#term-decorator
            :class-card: sd-border-secondary

            **Python Glossary**

            Official definition of decorators in the Python glossary.

            +++

            - ``@`` syntax
            - Function transformation
            - Class decorators

        .. grid-item-card:: 📝 PEP 318: Decorators
            :link: https://peps.python.org/pep-0318/
            :class-card: sd-border-secondary

            **PEP 318**

            The PEP that introduced decorator syntax for functions and methods.

            +++

            - ``@decorator`` syntax
            - Motivation and rationale
            - Design alternatives


.. dropdown:: 📏 Style and Best Practices
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📏 PEP 8 -- Style Guide
            :link: https://peps.python.org/pep-0008/
            :class-card: sd-border-secondary

            **Coding Conventions**

            Guidelines for function naming, lambda usage, and code formatting.

            +++

            - Lambda assignment discouraged
            - Function naming (``snake_case``)
            - Decorator formatting


.. dropdown:: 🌐 External Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🎯 Real Python: Primer on Decorators
            :link: https://realpython.com/primer-on-python-decorators/
            :class-card: sd-border-secondary

            **Real Python**

            Comprehensive tutorial on decorators, including first-class objects, closures, and practical examples.

            +++

            - First-class functions
            - Simple decorators
            - Advanced patterns

        .. grid-item-card:: 🔒 Real Python: Closures
            :link: https://realpython.com/python-closure/
            :class-card: sd-border-secondary

            **Real Python**

            In-depth guide to closures in Python with practical examples.

            +++

            - Free variables
            - ``nonlocal`` keyword
            - Closure applications

        .. grid-item-card:: 🔀 Real Python: Lambda Functions
            :link: https://realpython.com/python-lambda/
            :class-card: sd-border-secondary

            **Real Python**

            Guide to lambda functions, their syntax, use cases, and limitations.

            +++

            - Lambda syntax
            - Common patterns
            - When to avoid lambdas

        .. grid-item-card:: 🛠️ Real Python: functools
            :link: https://realpython.com/python-functools/
            :class-card: sd-border-secondary

            **Real Python**

            Overview of the ``functools`` module including ``partial``, ``wraps``, ``lru_cache``, and more.

            +++

            - ``partial`` objects
            - ``wraps`` decorator
            - Caching with ``lru_cache``

        .. grid-item-card:: 🔧 Real Python: Functional Programming
            :link: https://realpython.com/python-functional-programming/
            :class-card: sd-border-secondary

            **Real Python**

            Introduction to functional programming concepts in Python.

            +++

            - Pure functions
            - Immutability
            - ``map``, ``filter``, ``reduce``


.. dropdown:: 📚 Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📘 Python Official Tutorial
            :link: https://docs.python.org/3/tutorial/
            :class-card: sd-border-secondary

            **Getting Started**

            Section 4.7.5 (Lambda Expressions) and Section 4.7.6 (Documentation Strings) cover relevant topics for this lecture.

            +++

            - Lambda expressions
            - Functional tools
            - Code style

        .. grid-item-card:: Luciano Ramalho
            :class-card: sd-border-secondary

            **Fluent Python (2nd Edition)**

            Chapters 7-9 cover first-class functions, type hints, decorators, and closures. Excellent for understanding functions as objects.

        .. grid-item-card:: Mark Lutz
            :class-card: sd-border-secondary

            **Learning Python (5th Edition)**

            Chapters 19-21 cover advanced function topics including closures, decorators, and functional programming tools.

        .. grid-item-card:: Brett Slatkin
            :class-card: sd-border-secondary

            **Effective Python (2nd Edition)**

            Items 19-26 cover function arguments, return values, closures, and decorators with practical best practices.
