====================================================
Lecture
====================================================



Loops
====================================================

Repeating actions with ``for`` and ``while`` loops.

Create a file called ``loops_demo.py`` to follow along with the examples below.


.. dropdown:: The ``range()`` Function
   :open:

   The ``range()`` function generates an immutable sequence of integers. It is one of the most commonly used tools for looping in Python.

   .. note::

      **Syntax**: ``range(stop)`` or ``range(start, stop)`` or ``range(start, stop, step)``

   - ``start`` — Starting value (default: 0, inclusive)
   - ``stop`` — Ending value (exclusive, never included!)
   - ``step`` — Increment between values (default: 1)

   .. code-block:: python

      # range() returns a range object, not a list
      r = range(5)
      print(r)        # range(0, 5)
      print(type(r))  # <class 'range'>

      # Convert to list to see all values
      print(list(range(5)))  # [0, 1, 2, 3, 4]

   .. warning::

      The ``stop`` value is **never included**. ``range(5)`` gives ``[0, 1, 2, 3, 4]``, not ``[0, 1, 2, 3, 4, 5]``!


.. dropdown:: Basic ``range()`` Usage
   :open:

   .. code-block:: python

      # range(stop) - generates 0 to stop-1
      print(list(range(5)))       # [0, 1, 2, 3, 4]

      # range(start, stop) - generates start to stop-1
      print(list(range(2, 7)))    # [2, 3, 4, 5, 6]

      # range(start, stop, step) - with custom increment
      print(list(range(0, 10, 2)))  # [0, 2, 4, 6, 8]
      print(list(range(1, 10, 2)))  # [1, 3, 5, 7, 9]

      # Negative step - counting backwards
      print(list(range(5, 0, -1)))  # [5, 4, 3, 2, 1]
      print(list(range(10, 0, -2))) # [10, 8, 6, 4, 2]


.. dropdown:: ``range()`` Tricks: Indexing, Slicing, and Membership
   :open:

   .. code-block:: python

      # Get the length of a range without converting to list
      r = range(0, 1000000)
      print(len(r))           # 1000000 (instant, no memory used!)

      # Check membership efficiently - O(1) constant time!
      print(500000 in r)      # True (very fast!)
      print(999999 in r)      # True
      print(1000000 in r)     # False (stop value not included)

      # Indexing works on range objects
      r = range(10, 20)
      print(r[0])             # 10 (first element)
      print(r[-1])            # 19 (last element)
      print(r[5])             # 15

      # Slicing returns a new range object
      print(r[2:5])           # range(12, 15)
      print(list(r[2:5]))     # [12, 13, 14]


.. dropdown:: ``range()`` Tricks: Memory Efficiency
   :open:

   ``range()`` is a **lazy iterator** — it generates values on demand, not all at once.

   .. code-block:: python

      import sys

      # A list stores all values in memory
      big_list = list(range(1000000))
      print(sys.getsizeof(big_list))  # ~8,000,000+ bytes (8 MB)

      # A range object only stores start, stop, step
      big_range = range(1000000)
      print(sys.getsizeof(big_range))  # 48 bytes (always!)

      # Even a massive range uses the same tiny amount of memory
      huge_range = range(1000000000000)  # One trillion!
      print(sys.getsizeof(huge_range))   # Still just 48 bytes

   .. tip::

      **Best Practice**: Use ``range()`` directly in loops. Only convert to a list if you actually need to store all values.


.. dropdown:: The ``for`` Loop
   :open:

   The ``for`` loop iterates over any iterable object (strings, ranges, and more).

   .. code-block:: python

      # Iterate over a string
      message = "Hello"
      for char in message:
          print(char, end=" ")  # H e l l o

      print()  # Newline

      # Iterate over a range
      for i in range(5):
          print(i, end=" ")  # 0 1 2 3 4

      print()

      # Using range for repetition
      for _ in range(3):  # _ indicates we don't need the value
          print("Robot activated!")


.. dropdown:: Combining ``range()`` with Strings
   :open:

   .. code-block:: python

      message = "Python"

      # Access characters by index
      for i in range(len(message)):
          print(f"Index {i}: {message[i]}")
      # Index 0: P
      # Index 1: y
      # ...

      # Print every other character
      for i in range(0, len(message), 2):
          print(message[i], end="")  # Pto

      print()

      # Print string in reverse using range
      for i in range(len(message) - 1, -1, -1):
          print(message[i], end="")  # nohtyP


.. dropdown:: The ``enumerate()`` Function
   :open:

   When you need both the index and value, use ``enumerate()`` instead of ``range(len(...))``.

   .. code-block:: python

      message = "Robot"

      # Less Pythonic way
      for i in range(len(message)):
          print(f"{i}: {message[i]}")

      # More Pythonic way with enumerate()
      for index, char in enumerate(message):
          print(f"{index}: {char}")

      # Start counting from 1 instead of 0
      for index, char in enumerate(message, start=1):
          print(f"Character {index}: {char}")
      # Character 1: R
      # Character 2: o
      # ...


.. dropdown:: The ``while`` Loop
   :open:

   The ``while`` loop repeats as long as a condition is ``True``.

   .. code-block:: python

      # Basic while loop - counting
      count = 0
      while count < 5:
          print(count, end=" ")
          count += 1  # Don't forget to update!
      # Output: 0 1 2 3 4

      # Building a string character by character
      result = ""
      i = 0
      word = "Hello"
      while i < len(word):
          result += word[i].upper()
          i += 1
      print(result)  # HELLO

   .. warning::

      Always ensure the loop condition will eventually become ``False``, or you'll create an infinite loop!


.. dropdown:: Loop Control: ``break``, ``continue``, and ``else``
   :open:

   .. tab-set::

       .. tab-item:: ``break``

           Exit the loop immediately.

           .. code-block:: python

              # Find first vowel in a string
              word = "python"
              for char in word:
                  if char in "aeiou":
                      print(f"First vowel: {char}")
                      break
              # Output: First vowel: o

       .. tab-item:: ``continue``

           Skip to the next iteration.

           .. code-block:: python

              # Print only consonants
              word = "hello"
              for char in word:
                  if char in "aeiou":
                      continue
                  print(char, end=" ")
              # Output: h l l

       .. tab-item:: ``else``

           Runs if the loop completes without ``break``.

           .. code-block:: python

              # Search for a character
              word = "robot"
              target = "x"

              for char in word:
                  if char == target:
                      print(f"Found {target}!")
                      break
              else:
                  print(f"{target} not found")
              # Output: x not found

   .. note::

      The ``else`` clause after a loop is a unique Python feature — useful for search patterns!


Iterables
====================================================

Objects that can be traversed element by element.


.. dropdown:: What Are Iterables?
   :open:

   An **iterable** is an object that can be "iterated over", meaning its elements can be accessed one at a time in sequence.

   .. grid:: 1 2 2 2
       :gutter: 3

       .. grid-item-card:: Sequence Types
           :class-card: sd-border-info

           - Lists
           - Strings
           - Tuples

       .. grid-item-card:: Other Iterables
           :class-card: sd-border-info

           - Dictionaries (keys, values, items)
           - Sets and frozensets
           - Files, range objects, generators

   .. code-block:: python

      # We've already seen iterating over strings and ranges
      for char in "Hi":
          print(char, end=" ")  # H i

      for num in range(3):
          print(num, end=" ")  # 0 1 2

      # Soon we'll iterate over lists, dicts, and sets!


.. dropdown:: In-Place vs Out-of-Place Operations
   :open:

   .. grid:: 1 2 2 2
       :gutter: 3

       .. grid-item-card:: In-Place Operations
           :class-card: sd-border-warning

           - Modify the original object directly
           - Do not create a new object
           - Common with mutable types
           - Usually return ``None``

           .. code-block:: python

              fruits = ["apple", "banana"]
              result = fruits.append("kiwi")
              print(result)  # None
              print(fruits)  # ['apple', 'banana', 'kiwi']

       .. grid-item-card:: Out-of-Place Operations
           :class-card: sd-border-success

           - Create and return a new object
           - Leave the original unchanged
           - Required for immutable types
           - Return the new value

           .. code-block:: python

              text = "hello"
              upper_text = text.upper()
              print(text)        # hello
              print(upper_text)  # HELLO

   .. warning::

      Always check whether a method modifies in-place or returns a new object. Assigning the result of an in-place operation often leads to bugs!


Lists
====================================================

Python's versatile, ordered, mutable sequence type.

Create a file called ``lists_demo.py`` to follow along with the examples below.


.. dropdown:: The List Type
   :open:

   A Python list (``list``) is an **ordered** and **mutable** sequence of objects.

   .. list-table::
      :widths: 15 15 30 15 15
      :header-rows: 1
      :class: compact-table

      * - Name
        - Type
        - Example
        - Mutable
        - Ordered
      * - List
        - ``list``
        - ``[1, 'hello', 3.5]``
        - Yes
        - Yes

   .. code-block:: python

      # Lists can contain any objects
      numbers = [1, 2, 3, 4, 5]
      mixed = [1, "hello", 3.14, True, None]
      nested = [[1, 2], [3, 4], [5, 6]]

      # Lists with same items in different order are different
      a = [1, 2, 3]
      b = [3, 2, 1]
      print(a == b)  # False


.. dropdown:: Creating Lists
   :open:

   There are several ways to create lists:

   **Square brackets** with comma-separated values:

   .. code-block:: python

      fruits = ["apple", "banana", "cherry"]
      empty = []

   **``list()`` constructor** with an iterable:

   .. code-block:: python

      chars = list("hello")       # ['h', 'e', 'l', 'l', 'o']
      nums = list(range(5))       # [0, 1, 2, 3, 4]
      empty = list()              # []

   **List comprehension**:

   .. code-block:: python

      squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

   **Repetition operator**:

   .. code-block:: python

      zeros = [0] * 5             # [0, 0, 0, 0, 0]


.. dropdown:: Indexing and Slicing
   :open:

   Lists support the same indexing and slicing operations as strings.

   .. code-block:: python

      fruits = ["apple", "banana", "cherry", "date", "elderberry"]

      # Indexing
      print(fruits[0])      # apple
      print(fruits[-1])     # elderberry

      # Slicing
      print(fruits[1:4])    # ['banana', 'cherry', 'date']
      print(fruits[::2])    # ['apple', 'cherry', 'elderberry']

      # Modifying elements (lists are mutable!)
      fruits[0] = "apricot"
      print(fruits)         # ['apricot', 'banana', 'cherry', 'date', 'elderberry']

      # Modifying slices
      fruits[1:3] = ["blueberry"]
      print(fruits)         # ['apricot', 'blueberry', 'date', 'elderberry']


.. dropdown:: Common List Methods
   :open:

   **Adding elements:**

   .. code-block:: python

      fruits = ["apple"]
      fruits.append("banana")        # Add to end: ['apple', 'banana']
      fruits.extend(["kiwi", "mango"])  # Add multiple: ['apple', 'banana', 'kiwi', 'mango']
      fruits.insert(1, "cherry")     # Insert at index: ['apple', 'cherry', 'banana', ...]

   **Removing elements:**

   .. code-block:: python

      fruits = ["apple", "banana", "apple", "cherry"]
      fruits.remove("apple")    # Remove first occurrence: ['banana', 'apple', 'cherry']
      last = fruits.pop()       # Remove and return last: 'cherry'
      first = fruits.pop(0)     # Remove and return at index: 'banana'
      fruits.clear()            # Remove all: []

   **Searching and sorting:**

   .. code-block:: python

      nums = [3, 1, 4, 1, 5, 9, 2, 6]
      print(nums.index(4))      # 2 (first occurrence)
      print(nums.count(1))      # 2 (count occurrences)

      nums.sort()               # In-place sort: [1, 1, 2, 3, 4, 5, 6, 9]
      nums.sort(reverse=True)   # Descending: [9, 6, 5, 4, 3, 2, 1, 1]
      nums.reverse()            # In-place reverse

      # sorted() returns a new list (out-of-place)
      original = [3, 1, 4]
      new_list = sorted(original)  # [1, 3, 4], original unchanged


.. dropdown:: List Comprehensions
   :open:

   List comprehensions provide a compact way to create lists from iterables.

   .. note::

      **Syntax**: ``[expression for item in iterable if condition]``

   .. code-block:: python

      # Basic comprehension
      squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

      # With condition (filtering)
      evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

      # With transformation
      words = ["hello", "world"]
      upper = [w.upper() for w in words]  # ['HELLO', 'WORLD']

      # Conditional expression (ternary in comprehension)
      labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
      # ['even', 'odd', 'even', 'odd', 'even']


.. dropdown:: Shallow vs Deep Copy
   :open:

   .. grid:: 1 2 2 2
       :gutter: 3

       .. grid-item-card:: Shallow Copy
           :class-card: sd-border-warning

           - Copies top-level elements
           - Nested objects share references
           - Methods: ``copy()``, ``list()``, slice ``[:]``

           .. code-block:: python

              from copy import copy

              a = [1, [2, 3]]
              b = copy(a)  # or a.copy() or a[:]
              b[0] = 99
              b[1].append(4)

              print(a)  # [1, [2, 3, 4]]
              print(b)  # [99, [2, 3, 4]]

           .. only:: html
            
           .. raw:: html

               <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                  <img src="../_static/images/L3/shallow_light.png"
                     alt="Example of a shallow copy"
                     class="only-light"
                     style="width:100%; border-radius:8px;">
                  <img src="../_static/images/L3/shallow_dark.png"
                     alt="Example of a shallow copy"
                     class="only-dark"
                     style="width:100%; border-radius:8px;">
               </div>

       .. grid-item-card:: Deep Copy
           :class-card: sd-border-success

           - Recursively copies all nested objects
           - Completely independent copy
           - Method: ``deepcopy()``

           .. code-block:: python

              from copy import deepcopy

              a = [1, [2, 3]]
              b = deepcopy(a)
              b[0] = 99
              b[1].append(4)

              print(a)  # [1, [2, 3]]
              print(b)  # [99, [2, 3, 4]]

           .. only:: html
            
           .. raw:: html

               <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                  <img src="../_static/images/L3/deep_light.png"
                     alt="Example of a deep copy"
                     class="only-light"
                     style="width:100%; border-radius:8px;">
                  <img src="../_static/images/L3/deep_dark.png"
                     alt="Example of a deep copy"
                     class="only-dark"
                     style="width:100%; border-radius:8px;">
               </div>

   .. warning::

      Using ``=`` does NOT copy a list! It creates an alias (both names point to the same object).


Tuples
====================================================

Immutable sequences for fixed collections of items.

Create a file called ``tuples_demo.py`` to follow along with the examples below.


.. dropdown:: The Tuple Type
   :open:

   A Python tuple (``tuple``) is an **ordered** and **immutable** sequence of objects.

   .. list-table::
      :widths: 15 15 30 15 15
      :header-rows: 1
      :class: compact-table

      * - Name
        - Type
        - Example
        - Mutable
        - Ordered
      * - Tuple
        - ``tuple``
        - ``(1, 'hello', 3.5)``
        - No
        - Yes

   .. code-block:: python

      # Creating tuples
      coordinates = (3.5, 7.2)
      rgb = (255, 128, 0)
      mixed = (1, "hello", [1, 2])  # Can contain mutable objects

      # Important: commas make the tuple, not parentheses!
      single = (42,)   # Tuple with one element
      not_tuple = (42) # Just an integer!

   .. note::

      Tuples are ideal for representing fixed collections like coordinates, RGB values, or database records.


.. dropdown:: Creating Tuples
   :open:

   **Parentheses** (optional but recommended):

   .. code-block:: python

      point = (3, 4)
      empty = ()

   **Comma-separated values** (tuple packing):

   .. code-block:: python

      point = 3, 4           # Same as (3, 4)
      singleton = 42,        # Tuple with one element

   **``tuple()`` constructor**:

   .. code-block:: python

      from_list = tuple([1, 2, 3])    # (1, 2, 3)
      from_string = tuple("abc")      # ('a', 'b', 'c')
      from_range = tuple(range(3))    # (0, 1, 2)

   .. warning::

      For a single-element tuple, you **must** include the trailing comma: ``(42,)`` not ``(42)``


.. dropdown:: Tuple Unpacking
   :open:

   Tuple unpacking assigns each element to a separate variable.

   .. code-block:: python

      # Basic unpacking
      coordinates = (3.5, 7.2)
      x, y = coordinates
      print(f"x={x}, y={y}")  # x=3.5, y=7.2

      # Swap values elegantly
      a, b = 10, 20
      a, b = b, a  # Now a=20, b=10

      # Ignore values with underscore
      point = (1, 2, 3)
      x, _, z = point  # Ignore the y-coordinate

      # Extended unpacking with *
      first, *rest = [1, 2, 3, 4, 5]
      print(first)  # 1
      print(rest)   # [2, 3, 4, 5]


.. dropdown:: Tuples Are Immutable
   :open:

   You cannot modify tuple elements after creation.

   .. code-block:: python

      point = (3, 4, 5)

      # These will raise TypeError:
      # point[0] = 10
      # del point[1]

      # However, mutable objects inside tuples CAN be modified!
      data = (1, 2, [3, 4])
      data[2].append(5)     # OK!
      print(data)           # (1, 2, [3, 4, 5])

      # But you cannot replace the list itself
      # data[2] = [10, 20]  # TypeError!

   .. note::

      **Why use tuples?** They're hashable (can be dict keys), faster than lists, and signal intent that data shouldn't change.


Dictionaries
====================================================

Key-value mappings for fast lookups.

Create a file called ``dictionaries_demo.py`` to follow along with the examples below.


.. dropdown:: The Dictionary Type
   :open:

   A Python dictionary (``dict``) is an **ordered** (since Python 3.7) and **mutable** mapping of unique keys to values.

   .. list-table::
      :widths: 15 15 30 15 15
      :header-rows: 1
      :class: compact-table

      * - Name
        - Type
        - Example
        - Mutable
        - Ordered
      * - Dictionary
        - ``dict``
        - ``{'a': 1, 'b': 2}``
        - Yes
        - Yes

   .. code-block:: python

      # Robot configuration dictionary
      robot = {
          "name": "TurtleBot3",
          "type": "mobile",
          "max_speed": 0.26,
          "sensors": ["lidar", "camera", "imu"]
      }

      print(robot["name"])      # TurtleBot3
      print(robot["max_speed"]) # 0.26


.. dropdown:: Creating Dictionaries
   :open:

   **Curly braces** with key-value pairs:

   .. code-block:: python

      d = {"name": "Alice", "age": 30}
      empty = {}

   **``dict()`` constructor**:

   .. code-block:: python

      d = dict(name="Alice", age=30)              # Keyword arguments
      d = dict([("name", "Alice"), ("age", 30)])  # List of tuples
      d = dict({"name": "Alice"}, age=30)         # Mixed

   **Dictionary comprehension**:

   .. code-block:: python

      squares = {x: x**2 for x in range(5)}
      # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

   **``dict.fromkeys()``**:

   .. code-block:: python

      keys = ["a", "b", "c"]
      d = dict.fromkeys(keys, 0)  # {'a': 0, 'b': 0, 'c': 0}


.. dropdown:: Accessing and Modifying
   :open:

   .. code-block:: python

      robot = {"name": "UR5", "joints": 6}

      # Accessing values
      print(robot["name"])         # UR5
      print(robot.get("speed"))    # None (no KeyError!)
      print(robot.get("speed", 0)) # 0 (default value)

      # Adding/modifying items
      robot["speed"] = 1.0         # Add new key
      robot["joints"] = 7          # Modify existing

      # Removing items
      del robot["speed"]           # Remove key (KeyError if missing)
      value = robot.pop("joints")  # Remove and return value
      robot.clear()                # Remove all items

      # Check if key exists
      if "name" in robot:
          print(robot["name"])


.. dropdown:: Iterating Over Dictionaries
   :open:

   .. code-block:: python

      robot = {"name": "TurtleBot", "type": "mobile", "speed": 0.26}

      # Iterate over keys (default)
      for key in robot:
          print(key, end=" ")  # name type speed

      # Iterate over values
      for value in robot.values():
          print(value, end=" ")  # TurtleBot mobile 0.26

      # Iterate over key-value pairs
      for key, value in robot.items():
          print(f"{key}: {value}")
      # name: TurtleBot
      # type: mobile
      # speed: 0.26

   .. note::

      View objects (``keys()``, ``values()``, ``items()``) are dynamic — they reflect changes to the dictionary.


Sets
====================================================

Unordered collections of unique elements.

Create a file called ``sets_demo.py`` to follow along with the examples below.


.. dropdown:: The Set Type
   :open:

   A Python set (``set``) is an **unordered**, **mutable** collection that contains no duplicate elements.

   .. list-table::
      :widths: 15 15 30 15 15
      :header-rows: 1
      :class: compact-table

      * - Name
        - Type
        - Example
        - Mutable
        - Ordered
      * - Set
        - ``set``
        - ``{'a', 'b', 'c'}``
        - Yes
        - No

   .. code-block:: python

      # Sets automatically remove duplicates
      numbers = {1, 2, 2, 3, 3, 3}
      print(numbers)  # {1, 2, 3}

      # Creating sets
      fruits = {"apple", "banana", "cherry"}
      from_list = set([1, 2, 2, 3])  # {1, 2, 3}
      empty_set = set()  # NOT {} (that's an empty dict!)

   .. warning::

      Use ``set()`` to create an empty set. ``{}`` creates an empty **dictionary**!


.. dropdown:: Mathematical Set Operations
   :open:

   .. code-block:: python

      a = {1, 2, 3, 4}
      b = {3, 4, 5, 6}

      # Union: elements in either set
      print(a | b)              # {1, 2, 3, 4, 5, 6}
      print(a.union(b))         # Same result

      # Intersection: elements in both sets
      print(a & b)              # {3, 4}
      print(a.intersection(b))  # Same result

      # Difference: elements in a but not in b
      print(a - b)              # {1, 2}
      print(a.difference(b))    # Same result

      # Symmetric difference: elements in either but not both
      print(a ^ b)                      # {1, 2, 5, 6}
      print(a.symmetric_difference(b))  # Same result


.. dropdown:: Modifying Sets
   :open:

   **Adding elements:**

   .. code-block:: python

      s = {1, 2, 3}
      s.add(4)          # {1, 2, 3, 4}
      s.update([5, 6])  # {1, 2, 3, 4, 5, 6}

   **Removing elements:**

   .. code-block:: python

      s = {1, 2, 3, 4, 5}
      s.remove(3)    # {1, 2, 4, 5} - raises KeyError if missing
      s.discard(99)  # No error if missing
      x = s.pop()    # Remove and return arbitrary element
      s.clear()      # Remove all: set()

   .. note::

      **Use cases for sets**: Removing duplicates, membership testing, and finding common/unique elements between collections.


Summary
--------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card::
        :class-card: sd-border-primary

        - **Loops** — ``for``, ``while``, ``break``/``continue``/``else``
        - **range()** — Lazy iterator; memory efficient; indexing, slicing, membership
        - **Iterables** — Objects that can be traversed; in-place vs out-of-place
        - **Lists** — Ordered, mutable sequences; comprehensions; copy methods

    .. grid-item-card::
        :class-card: sd-border-primary

        - **Tuples** — Ordered, immutable sequences; unpacking
        - **Dictionaries** — Key-value mappings; view objects
        - **Sets** — Unordered unique collections; set operations

.. list-table:: Data Structure Comparison
   :widths: 20 20 20 20
   :header-rows: 1
   :class: compact-table

   * - Type
     - Mutable
     - Ordered
     - Duplicates
   * - ``list``
     - Yes
     - Yes
     - Yes
   * - ``tuple``
     - No
     - Yes
     - Yes
   * - ``dict``
     - Yes
     - Yes
     - Keys: No
   * - ``set``
     - Yes
     - No
     - No

.. note::

   **Reminder**: Review and experiment with all provided code before next class.


Preview: What's Next in L4
---------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📖 L4: Functions — Part I
        :class-card: sd-border-primary

        - Defining and calling functions
        - Parameters and arguments
        - Return values
        - Scope and namespaces
        - Type hints
        - Docstrings

.. note::

   Today's lecture gives you the data structures and iteration tools that you will use constantly when writing functions in L4 and beyond.