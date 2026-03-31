References
==========


.. dropdown:: 🏛️ Lecture 3
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 — L3: Python Fundamentals — Part II**

        Covers loops (``for``, ``while``), the ``range()`` function, iterables, in-place vs out-of-place operations, lists and list comprehensions, tuples and unpacking, dictionaries, and sets with mathematical operations.


.. dropdown:: 🐍 Python Language References
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🔄 for Statements
            :link: https://docs.python.org/3/tutorial/controlflow.html#for-statements
            :class-card: sd-border-secondary

            **Tutorial — Control Flow**

            ``for`` loops, iteration over sequences, and the ``range()`` function.

            +++

            - Loop syntax
            - ``break`` and ``continue``
            - ``else`` clause

        .. grid-item-card:: 🔢 The range Type
            :link: https://docs.python.org/3/library/stdtypes.html#range
            :class-card: sd-border-secondary

            **Standard Library — range**

            Complete reference for ``range()`` objects and their properties.

            +++

            - Memory efficiency
            - Indexing and slicing
            - Membership testing

        .. grid-item-card:: 📋 Lists
            :link: https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
            :class-card: sd-border-secondary

            **Tutorial — Data Structures**

            List methods, list comprehensions, and common operations.

            +++

            - ``append()``, ``extend()``, ``insert()``
            - ``sort()``, ``reverse()``
            - List comprehensions

        .. grid-item-card:: 📦 Tuples and Sequences
            :link: https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
            :class-card: sd-border-secondary

            **Tutorial — Data Structures**

            Tuple creation, unpacking, and use cases.

            +++

            - Tuple packing/unpacking
            - Immutability
            - Single-element tuples

        .. grid-item-card:: 📖 Dictionaries
            :link: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
            :class-card: sd-border-secondary

            **Tutorial — Data Structures**

            Dictionary creation, access patterns, and iteration.

            +++

            - Key-value pairs
            - ``get()``, ``keys()``, ``values()``, ``items()``
            - Dictionary comprehensions

        .. grid-item-card:: 🎯 Sets
            :link: https://docs.python.org/3/tutorial/datastructures.html#sets
            :class-card: sd-border-secondary

            **Tutorial — Data Structures**

            Set operations, methods, and use cases.

            +++

            - Union, intersection, difference
            - ``add()``, ``remove()``, ``discard()``
            - Set comprehensions

        .. grid-item-card:: 📋 Sequence Types
            :link: https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
            :class-card: sd-border-secondary

            **Standard Library — Sequences**

            Complete reference for list, tuple, and range types.

            +++

            - Common operations
            - Mutable vs immutable
            - Slicing syntax

        .. grid-item-card:: 📖 Mapping Types
            :link: https://docs.python.org/3/library/stdtypes.html#mapping-types-dict
            :class-card: sd-border-secondary

            **Standard Library — dict**

            Complete reference for dictionary methods and operations.

            +++

            - All dict methods
            - View objects
            - Ordering guarantee

        .. grid-item-card:: 🎯 Set Types
            :link: https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset
            :class-card: sd-border-secondary

            **Standard Library — set**

            Complete reference for set and frozenset operations.

            +++

            - Mathematical operations
            - Modification methods
            - Frozenset (immutable)

        .. grid-item-card:: 📋 Copy Module
            :link: https://docs.python.org/3/library/copy.html
            :class-card: sd-border-secondary

            **Standard Library — copy**

            Shallow and deep copy operations for compound objects.

            +++

            - ``copy()`` vs ``deepcopy()``
            - Handling nested objects
            - Custom copy behavior


.. dropdown:: 📏 Style and Best Practices
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📏 PEP 8 — Style Guide
            :link: https://peps.python.org/pep-0008/
            :class-card: sd-border-secondary

            **Coding Conventions**

            Guidelines for loops, comprehensions, and collection usage.

            +++

            - Loop variable naming
            - Comprehension line length
            - Whitespace in collections

        .. grid-item-card:: 📝 PEP 274 — Dict Comprehensions
            :link: https://peps.python.org/pep-0274/
            :class-card: sd-border-secondary

            **Dictionary Comprehensions**

            The PEP that introduced dictionary comprehension syntax.

            +++

            - Syntax specification
            - Use cases
            - Performance notes

        .. grid-item-card:: 📝 PEP 3132 — Extended Unpacking
            :link: https://peps.python.org/pep-3132/
            :class-card: sd-border-secondary

            **Extended Iterable Unpacking**

            The PEP that introduced ``*rest`` syntax for unpacking.

            +++

            - Star expressions
            - Multiple assignment
            - Use cases


.. dropdown:: 📚 Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📘 Python Official Tutorial
            :link: https://docs.python.org/3/tutorial/
            :class-card: sd-border-secondary

            **Getting Started**

            Sections 4 (control flow) and 5 (data structures) cover this lecture's topics.

            +++

            - Loops and conditionals
            - Lists, tuples, dicts, sets
            - Comprehensions

        .. grid-item-card:: Mark Lutz
            :class-card: sd-border-secondary

            **Learning Python (5th Edition)**

            Chapters 8–14 cover iteration, lists, dictionaries, tuples, and comprehensions in depth.

        .. grid-item-card:: Luciano Ramalho
            :class-card: sd-border-secondary

            **Fluent Python (2nd Edition)**

            Part II covers sequences, dictionaries, sets, and their protocols. Excellent for understanding Python's data model.

        .. grid-item-card:: Brett Slatkin
            :class-card: sd-border-secondary

            **Effective Python (2nd Edition)**

            Items 11–18 cover comprehensions, generators, and iteration best practices.