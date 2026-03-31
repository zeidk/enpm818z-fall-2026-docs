====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 5: Advanced Functions,
including programming paradigms, first-class functions, lambda expressions,
closures, callables, decorators, ``functools.wraps``, stacking decorators,
decorators with arguments, and ``functools.partial``.

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

   What is the output of the following code?

   .. code-block:: python

      def make_multiplier(n):
          return lambda x: x * n

      double = make_multiplier(2)
      print(double(5))

   A. ``5``

   B. ``10``

   C. ``2``

   D. ``TypeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``10``

   ``make_multiplier(2)`` returns a lambda that multiplies its argument by ``2``. Calling ``double(5)`` evaluates ``5 * 2 = 10``.


.. admonition:: Question 2
   :class: hint

   Which of the following is NOT a valid use of a lambda?

   A. ``sorted(items, key=lambda x: x[1])``

   B. ``lambda x, y: x + y``

   C. ``lambda x: if x > 0: return x``

   D. ``list(map(lambda x: x**2, [1, 2, 3]))``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``lambda x: if x > 0: return x``

   Lambdas can only contain a single expression. ``if``/``return`` statements are not allowed. Conditional *expressions* (``x if x > 0 else 0``) are allowed, but statement-based ``if`` blocks are not.


.. admonition:: Question 3
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def outer():
          count = 0
          def inner():
              nonlocal count
              count += 1
              return count
          return inner

      f = outer()
      print(f(), f(), f())

   A. ``1 1 1``

   B. ``1 2 3``

   C. ``0 1 2``

   D. ``NameError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``1 2 3``

   ``outer()`` creates a closure. Each call to ``f()`` increments the captured ``count`` variable via ``nonlocal``. The three calls produce ``1``, ``2``, and ``3``.


.. admonition:: Question 4
   :class: hint

   What does the ``@`` syntax do in the following code?

   .. code-block:: python

      @my_decorator
      def my_function():
          pass

   A. It calls ``my_function`` and passes the result to ``my_decorator``.

   B. It is equivalent to ``my_function = my_decorator(my_function)``.

   C. It creates a new class called ``my_decorator``.

   D. It passes ``my_decorator`` as an argument to ``my_function``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It is equivalent to ``my_function = my_decorator(my_function)``.

   The ``@decorator`` syntax is syntactic sugar. Python calls the decorator with the function as its argument and replaces the function with the return value.


.. admonition:: Question 5
   :class: hint

   What is the purpose of ``functools.wraps``?

   A. It makes a function run faster.

   B. It copies the original function's metadata (name, docstring) onto the wrapper.

   C. It prevents a function from being decorated.

   D. It automatically adds type hints to the wrapper function.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It copies the original function's metadata (name, docstring) onto the wrapper.

   Without ``@wraps(func)``, the wrapper replaces the original function's ``__name__``, ``__doc__``, and other attributes. ``functools.wraps`` preserves these for introspection and debugging.


.. admonition:: Question 6
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      from functools import partial

      def power(base, exponent):
          return base ** exponent

      square = partial(power, exponent=2)
      print(square(5))

   A. ``10``

   B. ``25``

   C. ``32``

   D. ``TypeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``25``

   ``partial(power, exponent=2)`` creates a new function with ``exponent`` fixed to ``2``. Calling ``square(5)`` computes ``5 ** 2 = 25``.


.. admonition:: Question 7
   :class: hint

   When multiple decorators are stacked, in what order are they applied?

   .. code-block:: python

      @decorator_a
      @decorator_b
      def func():
          pass

   A. ``decorator_a`` is applied first, then ``decorator_b``.

   B. ``decorator_b`` is applied first, then ``decorator_a``.

   C. Both are applied simultaneously.

   D. The order depends on the function's arguments.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``decorator_b`` is applied first, then ``decorator_a``.

   Stacked decorators are applied bottom to top. This is equivalent to ``func = decorator_a(decorator_b(func))``. The innermost decorator (closest to the function) is applied first.


.. admonition:: Question 8
   :class: hint

   What does ``callable(42)`` return?

   A. ``True``

   B. ``False``

   C. ``42``

   D. ``TypeError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``False``

   Integers are not callable. Only objects that can be invoked with parentheses (functions, classes, objects with ``__call__``) return ``True`` from ``callable()``.


.. admonition:: Question 9
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def make_greeter(greeting):
          def greet(name):
              return f"{greeting}, {name}!"
          return greet

      hi = make_greeter("Hi")
      hello = make_greeter("Hello")
      print(hi("Bob"))

   A. ``"Hello, Bob!"``

   B. ``"Hi, Bob!"``

   C. ``"greeting, Bob!"``

   D. ``NameError``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``"Hi, Bob!"``

   Each call to ``make_greeter`` creates an independent closure. ``hi`` captures ``"Hi"`` and ``hello`` captures ``"Hello"``. They do not interfere with each other.


.. admonition:: Question 10
   :class: hint

   Which of the following correctly describes a higher-order function?

   A. A function that uses recursion.

   B. A function that takes another function as an argument or returns a function.

   C. A function defined inside a class.

   D. A function with more than three parameters.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A function that takes another function as an argument or returns a function.

   Higher-order functions operate on other functions. Examples include ``map``, ``filter``, ``sorted`` (with ``key``), and any decorator.


.. admonition:: Question 11
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      nums = [1, 2, 3, 4, 5]
      result = list(filter(lambda x: x % 2 == 0, nums))
      print(result)

   A. ``[1, 3, 5]``

   B. ``[2, 4]``

   C. ``[1, 2, 3, 4, 5]``

   D. ``[]``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``[2, 4]``

   ``filter`` keeps elements for which the lambda returns ``True``. The lambda checks if a number is even (``x % 2 == 0``), so only ``2`` and ``4`` are kept.


.. admonition:: Question 12
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def repeat(n):
          def decorator(func):
              def wrapper(*args, **kwargs):
                  for _ in range(n):
                      func(*args, **kwargs)
              return wrapper
          return decorator

      @repeat(2)
      def say_hi():
          print("Hi")

      say_hi()

   A. ``Hi`` (printed once)

   B. ``Hi`` (printed twice)

   C. ``TypeError``

   D. Nothing is printed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``Hi`` (printed twice)

   ``@repeat(2)`` creates a parameterized decorator. ``repeat(2)`` returns ``decorator``, which wraps ``say_hi`` so that calling it executes the original function ``2`` times.


.. admonition:: Question 13
   :class: hint

   Which of the following is a requirement for a closure?

   A. The inner function must be defined with ``lambda``.

   B. The inner function must reference a variable from the enclosing function's scope.

   C. The enclosing function must use the ``global`` keyword.

   D. The inner function must accept ``*args`` and ``**kwargs``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The inner function must reference a variable from the enclosing function's scope.

   A closure requires: a nested function, a reference to a free variable from the enclosing scope, and the enclosing function returning the nested function.


.. admonition:: Question 14
   :class: hint

   What is the output of the following code?

   .. code-block:: python

      def compute_square(x):
          return x ** 2

      f = compute_square
      print(f(4))
      print(type(f))

   A. ``16`` then ``<class 'int'>``

   B. ``16`` then ``<class 'function'>``

   C. ``TypeError``

   D. ``None`` then ``<class 'function'>``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``16`` then ``<class 'function'>``

   ``f = compute_square`` assigns the function object (not the return value) to ``f``. Calling ``f(4)`` returns ``16``, and ``type(f)`` is ``<class 'function'>``.


.. admonition:: Question 15
   :class: hint

   What is the key difference between ``map`` and ``filter``?

   A. ``map`` transforms each element; ``filter`` selects elements based on a condition.

   B. ``map`` returns a list; ``filter`` returns a tuple.

   C. ``map`` works with strings only; ``filter`` works with numbers only.

   D. ``map`` modifies the original list; ``filter`` creates a copy.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- ``map`` transforms each element; ``filter`` selects elements based on a condition.

   ``map(func, iterable)`` applies ``func`` to every element and returns the transformed values. ``filter(func, iterable)`` returns only those elements for which ``func`` returns ``True``. Both return lazy iterators.


----


True or False
=============

.. admonition:: Question 16
   :class: hint

   **True or False:** In Python, functions are first-class objects and can be assigned to variables, passed as arguments, and returned from other functions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Functions in Python are first-class objects. They can be assigned to variables, passed to other functions as arguments, returned from functions, and stored in data structures like lists and dictionaries.


.. admonition:: Question 17
   :class: hint

   **True or False:** A lambda function can contain multiple statements separated by semicolons.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Lambda functions are restricted to a single expression. They cannot contain statements (assignments, loops, ``try``/``except``, etc.). For multi-line logic, use a regular ``def`` function.


.. admonition:: Question 18
   :class: hint

   **True or False:** A closure's captured variables are destroyed when the enclosing function returns.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The captured variables survive through cell objects stored in the inner function's ``__closure__`` tuple. Even after the enclosing function returns and its local scope is discarded, the cell objects keep the captured values alive.


.. admonition:: Question 19
   :class: hint

   **True or False:** ``functools.partial`` calls the original function immediately with the frozen arguments.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``functools.partial`` does not call the function. It returns a new callable with some arguments pre-filled. The function is only called when you invoke the partial object with the remaining arguments.


.. admonition:: Question 20
   :class: hint

   **True or False:** The ``nonlocal`` keyword is required to read a variable from an enclosing scope inside a nested function.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   You can *read* variables from an enclosing scope without ``nonlocal``. The ``nonlocal`` keyword is only required when you want to *modify* (reassign) a variable in the enclosing scope.


.. admonition:: Question 21
   :class: hint

   **True or False:** Decorators can only be applied to functions, not to classes or methods.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Decorators can be applied to functions, methods, and classes. For example, ``@staticmethod``, ``@classmethod``, and ``@dataclass`` are all commonly used decorators applied to methods or classes.


.. admonition:: Question 22
   :class: hint

   **True or False:** ``map`` and ``filter`` return lists in Python 3.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   In Python 3, ``map`` and ``filter`` return lazy iterators, not lists. You must wrap the result in ``list()`` to materialize all values.


.. admonition:: Question 23
   :class: hint

   **True or False:** PEP 8 discourages assigning a lambda to a variable name.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   PEP 8 states that assigning a lambda to a variable (e.g., ``f = lambda x: x + 1``) defeats the purpose of lambdas. If you need a named function, use ``def`` instead. Lambdas are intended for short, inline use.


.. admonition:: Question 24
   :class: hint

   **True or False:** Two closures created by the same enclosing function share the same captured state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Each call to the enclosing function creates a new, independent closure with its own set of captured variables. Two closures from the same factory do not share state.


.. admonition:: Question 25
   :class: hint

   **True or False:** A parameterized decorator (decorator with arguments) requires three levels of nested functions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A parameterized decorator uses three layers: the decorator factory (takes the arguments), the decorator (takes the function), and the wrapper (replaces the function). The pattern is ``factory(args) -> decorator(func) -> wrapper(*args, **kwargs)``.


----


Essay Questions
===============

.. admonition:: Question 26
   :class: hint

   **Explain what a closure is and the three conditions required for one to exist.** Provide a brief example.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A closure is a function that retains access to variables from its enclosing scope even after the enclosing function has returned.
   - Three conditions: (1) a nested function exists, (2) the nested function references a free variable from the enclosing scope, and (3) the enclosing function returns the nested function.
   - Python uses cell objects to keep the captured variables alive after the enclosing scope is discarded.
   - Example: a ``make_counter`` function that returns an ``increment`` function which remembers and updates a ``count`` variable.


.. admonition:: Question 27
   :class: hint

   **Explain why ``functools.wraps`` is important when writing decorators.** What happens if you omit it?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - When a decorator wraps a function, the wrapper function replaces the original. Without ``@wraps``, the original function's ``__name__``, ``__doc__``, ``__module__``, and other metadata are lost.
   - ``functools.wraps`` copies these attributes from the original function onto the wrapper.
   - This is important for debugging (stack traces show the correct name), documentation generators, and any tool that inspects function metadata.
   - Best practice: always use ``@functools.wraps(func)`` in every decorator wrapper.


.. admonition:: Question 28
   :class: hint

   **Compare ``functools.partial``, lambda expressions, and closures as ways to pre-fill function arguments.** When would you prefer each approach?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``functools.partial`` is best for simple argument freezing; it preserves introspection via ``.func``, ``.args``, and ``.keywords`` attributes.
   - Lambda expressions are good for short, inline transformations where the logic fits in a single expression.
   - Closures offer the most flexibility: they can contain complex logic, maintain mutable state, and perform additional processing beyond simple argument binding.
   - Rule of thumb: use ``partial`` for straightforward cases, lambda for one-liners, and closures when you need state or multi-step logic.


.. admonition:: Question 29
   :class: hint

   **Explain how stacked decorators are applied.** Given ``@A`` on top of ``@B`` on top of a function ``f``, describe the order of execution.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Stacked decorators are applied bottom to top: ``@B`` is applied first, then ``@A``.
   - The equivalent expression is ``f = A(B(f))``.
   - At call time, the outermost wrapper (from ``A``) executes first, then the wrapper from ``B``, then the original function ``f``.
   - This means the decorator closest to the function definition is applied first during decoration, but its wrapper is called last during execution.


.. admonition:: Question 30
   :class: hint

   **Describe the difference between a pure function and an impure function.** Why do functional programming advocates prefer pure functions?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A pure function depends only on its inputs and produces no side effects (no modifying external state, no I/O). Given the same inputs, it always returns the same output.
   - An impure function may modify global variables, mutate arguments, perform I/O, or depend on external state, making its behavior harder to predict.
   - Pure functions are preferred because they are easier to test, debug, and reason about. They also enable safe parallelism since they do not share mutable state.
   - In practice, most programs need some impure functions (for I/O, logging, etc.), but minimizing side effects improves code quality.
