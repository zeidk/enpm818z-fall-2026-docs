====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 3: Python Fundamentals -- Part II,
including loops, the ``range()`` function, iterables, lists, tuples,
dictionaries, sets, and comprehensions.

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

   What is the output of ``list(range(2, 10, 3))``?

   A. ``[2, 5, 8, 11]``

   B. ``[2, 5, 8]``

   C. ``[2, 4, 6, 8]``

   D. ``[3, 6, 9]``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``[2, 5, 8]``

   ``range(2, 10, 3)`` starts at 2, increments by 3, and stops before 10. Values: 2, 5, 8 (11 would exceed 10).


.. admonition:: Question 2
   :class: hint

   Which of the following correctly creates an empty set?

   A. ``empty = {}``

   B. ``empty = set()``

   C. ``empty = []``

   D. ``empty = set{}``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``empty = set()``

   ``{}`` creates an empty dictionary, not a set. Use ``set()`` for an empty set.


.. admonition:: Question 3
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      nums = [1, 2, 3]
      result = nums.append(4)
      print(result)

   A. ``[1, 2, 3, 4]``

   B. ``4``

   C. ``None``

   D. ``[4]``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``None``

   ``append()`` modifies the list in-place and returns ``None``. The list is changed, but the return value is ``None``.


.. admonition:: Question 4
   :class: hint

   Which method would you use to safely access a dictionary key that might not exist?

   A. ``dict[key]``

   B. ``dict.get(key)``

   C. ``dict.find(key)``

   D. ``dict.access(key)``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``dict.get(key)``

   ``.get()`` returns ``None`` (or a default value) if the key doesn't exist, while ``dict[key]`` raises ``KeyError``.


.. admonition:: Question 5
   :class: hint

   What is the output of ``(1, 2, 3) + (4, 5)``?

   A. ``[1, 2, 3, 4, 5]``

   B. ``(1, 2, 3, 4, 5)``

   C. ``TypeError``

   D. ``((1, 2, 3), (4, 5))``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``(1, 2, 3, 4, 5)``

   The ``+`` operator concatenates tuples, creating a new tuple with all elements.


.. admonition:: Question 6
   :class: hint

   What does the ``else`` clause do when attached to a ``for`` loop?

   A. Executes if the loop encounters an error.

   B. Executes if the loop completes without hitting ``break``.

   C. Executes on every iteration after the main body.

   D. Executes if the loop body is empty.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Executes if the loop completes without hitting ``break``.

   The ``else`` clause runs only if the loop exits normally (not via ``break``). Useful for search patterns.


.. admonition:: Question 7
   :class: hint

   What is the output of the following list comprehension?

   .. code-block:: python

      result = [x * 2 for x in range(5) if x % 2 == 0]
      print(result)

   A. ``[0, 2, 4, 6, 8]``

   B. ``[0, 4, 8]``

   C. ``[2, 4, 6, 8, 10]``

   D. ``[0, 2, 4]``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``[0, 4, 8]``

   The comprehension filters for even numbers (0, 2, 4) and doubles them (0, 4, 8).


.. admonition:: Question 8
   :class: hint

   Given ``a = {1, 2, 3}`` and ``b = {2, 3, 4}``, what is ``a & b``?

   A. ``{1, 2, 3, 4}``

   B. ``{2, 3}``

   C. ``{1, 4}``

   D. ``{1}``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``{2, 3}``

   ``&`` is the intersection operator, returning elements present in both sets.


.. admonition:: Question 9
   :class: hint

   What is the correct way to create a single-element tuple?

   A. ``t = (42)``

   B. ``t = (42,)``

   C. ``t = tuple(42)``

   D. ``t = [42]``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``t = (42,)``

   The trailing comma is required for single-element tuples. ``(42)`` is just the integer 42 in parentheses.


.. admonition:: Question 10
   :class: hint

   What does the ``continue`` statement do inside a loop?

   A. Exits the loop entirely.

   B. Skips to the next iteration of the loop.

   C. Restarts the loop from the beginning.

   D. Pauses the loop until a condition is met.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Skips to the next iteration of the loop.

   ``continue`` immediately starts the next iteration, skipping any remaining code in the current iteration.


.. admonition:: Question 11
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      d = {"a": 1, "b": 2}
      print(list(d.keys()))

   A. ``["a", "b"]``

   B. ``[1, 2]``

   C. ``[("a", 1), ("b", 2)]``

   D. ``{"a", "b"}``

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- ``["a", "b"]``

   ``.keys()`` returns a view of dictionary keys, which ``list()`` converts to a list.


.. admonition:: Question 12
   :class: hint

   Why is ``range()`` considered memory efficient?

   A. It stores all values in compressed format.

   B. It generates values on demand (lazy evaluation).

   C. It uses special integer optimization.

   D. It automatically garbage collects unused values.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It generates values on demand (lazy evaluation).

   ``range()`` only stores start, stop, and step (48 bytes total). Values are computed when needed.


.. admonition:: Question 13
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      from copy import copy
      a = [1, [2, 3]]
      b = copy(a)
      b[1].append(4)
      print(a)

   A. ``[1, [2, 3]]``

   B. ``[1, [2, 3, 4]]``

   C. ``[1, [4]]``

   D. ``TypeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``[1, [2, 3, 4]]``

   Shallow copy copies references to nested objects. ``b[1]`` and ``a[1]`` point to the same inner list.


.. admonition:: Question 14
   :class: hint

   Which of the following is NOT a valid way to iterate over a dictionary's key-value pairs?

   A. ``for k, v in d.items():``

   B. ``for k in d: v = d[k]``

   C. ``for k, v in d:``

   D. ``for (k, v) in d.items():``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``for k, v in d:``

   Iterating directly over a dictionary yields only keys, not key-value pairs. Use ``.items()`` for pairs.


.. admonition:: Question 15
   :class: hint

   What is the output of ``[1, 2, 3][1:1]``?

   A. ``[1]``

   B. ``[2]``

   C. ``[]``

   D. ``[1, 2]``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``[]``

   Slice ``[1:1]`` has start equal to stop, resulting in an empty list.


----


True or False
=============

.. admonition:: Question 16
   :class: hint

   **True or False:** Lists in Python are mutable, meaning you can change their elements after creation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Lists are mutable. You can modify, add, or remove elements using methods like ``append()``, ``pop()``, or direct index assignment.


.. admonition:: Question 17
   :class: hint

   **True or False:** Dictionaries in Python 3.7+ maintain insertion order.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Since Python 3.7, dictionaries maintain insertion order as part of the language specification.


.. admonition:: Question 18
   :class: hint

   **True or False:** The expression ``5 in range(1, 10, 2)`` evaluates to ``True``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``range(1, 10, 2)`` produces the sequence 1, 3, 5, 7, 9. The value 5 is in this range, so the expression evaluates to ``True``. The ``in`` operator on range objects runs in O(1) constant time.


.. admonition:: Question 19
   :class: hint

   **True or False:** Tuples can be used as dictionary keys because they are immutable and hashable.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Tuples are immutable and hashable (if all their elements are hashable), making them valid dictionary keys.


.. admonition:: Question 20
   :class: hint

   **True or False:** ``enumerate()`` returns a list of tuples containing index-value pairs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``enumerate()`` returns an enumerate object (an iterator), not a list. Convert with ``list()`` to get a list of tuples.


.. admonition:: Question 21
   :class: hint

   **True or False:** The ``pop()`` method on a list modifies the list in-place and returns the removed element.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``pop()`` removes an element at a given index (default: last), modifies the list in-place, and returns the removed value.


.. admonition:: Question 22
   :class: hint

   **True or False:** Set elements must be unique, but they can be of any type including lists.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Set elements must be hashable. Lists are mutable and unhashable, so they cannot be set elements.


.. admonition:: Question 23
   :class: hint

   **True or False:** The expression ``range(5) == range(0, 5, 1)`` evaluates to ``True``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Two ranges are equal if they produce the same sequence. ``range(5)`` and ``range(0, 5, 1)`` both produce ``[0, 1, 2, 3, 4]``.


.. admonition:: Question 24
   :class: hint

   **True or False:** Using ``a = b`` where ``b`` is a list creates an independent copy of the list.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``a = b`` creates an alias -- both names reference the same object. Use ``copy()`` or slicing for an independent copy.


.. admonition:: Question 25
   :class: hint

   **True or False:** Dictionary comprehensions can include conditional filtering similar to list comprehensions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Dictionary comprehensions support ``if`` conditions: ``{k: v for k, v in items if condition}``.


----


Essay Questions
===============

.. admonition:: Question 26
   :class: hint

   **Explain the difference between shallow copy and deep copy for nested lists.** Provide an example showing when shallow copy might cause unexpected behavior.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Shallow copy creates a new object but copies references to nested objects, not the objects themselves.
   - Deep copy recursively copies all nested objects, creating completely independent copies.
   - Example: ``a = [1, [2, 3]]; b = copy(a); b[1].append(4)`` modifies both ``a`` and ``b``'s inner list.
   - Use ``deepcopy()`` when you need truly independent copies of nested structures.


.. admonition:: Question 27
   :class: hint

   **Describe when you would choose a tuple over a list.** Give at least two practical scenarios where tuples are the better choice.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Tuples are immutable, making them hashable and usable as dictionary keys.
   - Use tuples for fixed collections where the data shouldn't change (coordinates, RGB values, database records).
   - Tuples signal intent -- readers know the data is meant to be constant.
   - Tuples are slightly faster than lists and use less memory.
   - Example scenarios: function returning multiple values, dictionary keys, data that represents a fixed record.


.. admonition:: Question 28
   :class: hint

   **Explain why** ``range()`` **is memory efficient compared to creating a list of the same values.** How does this affect performance when iterating over large sequences?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``range()`` is a lazy iterator that only stores start, stop, and step (48 bytes regardless of size).
   - A list stores every value in memory (8+ bytes per integer).
   - For ``range(1000000)``: range uses 48 bytes; equivalent list uses ~8 MB.
   - This matters when iterating over large sequences -- ``range()`` has constant memory usage.


.. admonition:: Question 29
   :class: hint

   **Compare and contrast** ``for`` **loops and** ``while`` **loops.** When would you prefer one over the other? Provide an example use case for each.

   *(3-5 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``for`` loops iterate over known sequences or ranges -- best when you know how many iterations.
   - ``while`` loops continue until a condition is false -- best when iteration count is unknown.
   - ``for`` is preferred for iterating over collections (lists, strings, dicts).
   - ``while`` is preferred for user input validation, reading until EOF, or state-based loops.
   - Example ``for``: processing each item in a list. Example ``while``: prompting until valid input.


.. admonition:: Question 30
   :class: hint

   **Explain the difference between in-place and out-of-place operations using list methods as examples.** Why is it important to know which type a method uses?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - In-place methods modify the original object and return ``None`` (e.g., ``list.sort()``, ``list.append()``).
   - Out-of-place methods return a new object, leaving the original unchanged (e.g., ``sorted()``, ``str.upper()``).
   - Important because assigning an in-place result often leads to bugs: ``x = x.sort()`` sets ``x`` to ``None``.
   - Check documentation or test return values to know which type a method uses.