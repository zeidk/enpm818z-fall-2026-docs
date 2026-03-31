====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 6. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``lecture6/`` workspace folder.


.. dropdown:: Exercise 1 -- Building a Robot Class
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate your understanding of class definitions, the ``__init__``
    constructor, the ``self`` parameter, instance attributes, and class
    attributes.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture6/robot_basics.py`` that implements the
    following. Each class and method must include type hints and a
    Google-style docstring.

    1. **``Robot`` class** with:

       - ``__init__(self, name: str, battery: int = 100)``
       - Instance attributes: ``name``, ``battery``, ``tasks_completed``
         (default ``0``)
       - A class attribute ``total_robots`` that tracks how many Robot
         instances have been created. Increment it in ``__init__``.

    2. **``perform_task(self, task_name: str) -> None``** method that:

       - If ``battery >= 10``: prints ``"<name> performing: <task_name>"``,
         decreases battery by 10, and increments ``tasks_completed``.
       - Otherwise: prints ``"<name> needs recharging!"``.

    3. **``recharge(self) -> None``** method that sets battery back to 100
       and prints ``"<name> fully recharged!"``.

    4. In the ``if __name__ == "__main__"`` block:

       - Create two Robot instances.
       - Have each robot perform several tasks.
       - Print each robot's ``tasks_completed`` and ``battery`` after the
         tasks.
       - Print ``Robot.total_robots``.

    .. code-block:: python

       if __name__ == '__main__':
           # Create two Robot instances
           robot1 = Robot("Atlas")
           robot2 = Robot("Spot", 50)

           # Have them perform several tasks
           robot1.perform_task("welding")
           robot1.perform_task("painting")
           robot1.perform_task("inspection")

           robot2.perform_task("delivery")
           robot2.perform_task("sorting")
           robot2.perform_task("scanning")
           robot2.perform_task("lifting")
           robot2.perform_task("packing")
           robot2.perform_task("cleaning")  # battery hits 0 after this

           # This one should trigger the recharge warning
           robot2.perform_task("assembly")

           # Recharge and continue
           robot2.recharge()
           robot2.perform_task("assembly")

           # Print final state
           print(f"\n{robot1.name}: tasks={robot1.tasks_completed}, battery={robot1.battery}")
           print(f"{robot2.name}: tasks={robot2.tasks_completed}, battery={robot2.battery}")
           print(f"Total robots created: {Robot.total_robots}")

    **Expected output:**

    .. code-block:: text

       Atlas performing: welding
       Atlas performing: painting
       Atlas performing: inspection
       Spot performing: delivery
       Spot performing: sorting
       Spot performing: scanning
       Spot performing: lifting
       Spot performing: packing
       Spot performing: cleaning
       Spot needs recharging!
       Spot fully recharged!
       Spot performing: assembly

       Atlas: tasks=3, battery=70
       Spot: tasks=6, battery=90
       Total robots created: 2


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture6/robot_basics.py``
    - The program must run without errors and produce output matching the
      expected format above.


.. dropdown:: Exercise 2 -- Dunder Methods for a Robot Class
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice implementing dunder methods for string representations,
    comparison operators, arithmetic operators, and the ``__len__``
    protocol.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture6/robot_dunders.py`` that implements the
    following. Each class and method must include type hints and a
    Google-style docstring.

    1. **``Robot`` class** with:

       - ``__init__(self, name: str, battery: int = 100)``
       - Instance attributes: ``name``, ``battery``, ``tasks_completed``
         (default ``0``)

    2. **String representations:**

       - ``__str__`` returns ``"<name> [<battery>%]"``
       - ``__repr__`` returns ``"Robot('<name>', <battery>)"``

    3. **Comparison operators:**

       - ``__eq__`` so two robots are equal if their battery levels are
         equal (regardless of name). Return ``NotImplemented`` for
         non-Robot types.
       - ``__gt__`` so robots can be compared by battery level. Return
         ``NotImplemented`` for non-Robot types.

    4. **Arithmetic operator:**

       - ``__add__`` so adding two Robots returns a new Robot with name
         ``"merged"`` and the sum of their batteries **capped at 100**.

    5. **Length protocol:**

       - ``__len__`` returns ``tasks_completed``.

    6. In the ``if __name__ == "__main__"`` block, test all dunder
       methods:

    .. code-block:: python

       if __name__ == "__main__":
           scout = Robot("Scout", 60)
           hauler = Robot("Hauler", 60)

           # __str__: human-readable output
           print(scout)  # Scout [60%]

           # __repr__: developer output, looks like valid Python
           print(repr(scout))  # Robot('Scout', 60)

           # __eq__: compare by battery level
           print(scout == hauler)  # True  (both have battery 60)
           print(scout == Robot("X", 90))  # False (different battery)

           # __add__: merge two robots, battery capped at 100
           print(scout + hauler)  # merged [100%]  (60 + 60 = 120, capped to 100)
           print(scout + Robot("X", 20))  # merged [80%]   (60 + 20 = 80, no cap needed)

           # __gt__: compare by battery level
           print(scout > Robot("X", 40))  # True  (60 > 40)
           print(scout > hauler)  # False (60 > 60 is False)

           # __len__: number of tasks completed
           scout.tasks_completed = 3
           print(len(scout))  # 3
           print(len(hauler))  # 0  (default, no tasks performed yet)

    **Expected output:**

    .. code-block:: text

       Scout [60%]
       Robot('Scout', 60)
       True
       False
       merged [100%]
       merged [80%]
       True
       False
       3
       0


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture6/robot_dunders.py``
    - The program must run without errors and produce output matching the
      expected format above.


.. dropdown:: Exercise 3 -- Encapsulated Sensor
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice encapsulation with non-public attributes, ``@property``
    decorators, read-only properties, and setter validation.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture6/sensor_encapsulated.py`` that implements the
    following. Each class and method must include type hints and a
    Google-style docstring.

    1. **``Sensor`` class** with:

       - ``__init__(self, sensor_type: str, range_m: float = 10.0)``
       - Non-public attributes: ``_sensor_type``, ``_range_m``

    2. **Read-only property** ``sensor_type`` that cannot be changed after
       creation. The setter should raise ``AttributeError``.

    3. **Property** ``range_m`` with a setter that:

       - Raises ``ValueError`` if ``range_m`` is set to a negative number.
       - Raises ``TypeError`` if ``range_m`` is not ``int`` or ``float``.

    4. **Methods:**

       - ``calibrate(offset: float) -> None`` adjusts ``_range_m`` by the
         given offset.
       - ``read() -> float`` returns ``_range_m`` with simulated noise
         (e.g., multiply by a random factor between 0.95 and 1.05).

    5. **``__str__``** returns ``"Sensor(<type>): range=<range_m>m"``.

    6. In the ``if __name__ == "__main__"`` block:

    .. code-block:: python

       if __name__ == "__main__":
           lidar = Sensor("lidar", 50.0)
           print(lidar)            # Sensor(lidar): range=50.0m
           lidar.calibrate(2.5)
           print(lidar)            # Sensor(lidar): range=52.5m
           lidar.calibrate(-5.0)
           print(lidar)            # Sensor(lidar): range=47.5m

    **Expected output:**

    .. code-block:: text

       Sensor(lidar): range=50.0m
       Sensor(lidar): range=52.5m
       Sensor(lidar): range=47.5m


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture6/sensor_encapsulated.py``
    - The program must run without errors and produce output matching the
      expected format above.


.. dropdown:: Exercise 4 -- Robot with Sensor Suite
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Combine classes, dunder methods, and encapsulation into a system where
    a ``Robot`` manages a collection of ``Sensor`` objects. This exercise
    ties together all concepts from the lecture.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture6/robot_with_sensors.py`` that implements the
    following. Every class and method must have type hints and a
    Google-style docstring.

    1. **``Sensor`` class** with:

       - Non-public attributes: ``_sensor_type``, ``_range_m``,
         ``_accuracy``
       - Properties for ``range_m`` (validated: must be positive) and
         ``sensor_type`` (read-only)
       - ``__str__`` and ``__repr__``
       - ``__gt__`` comparing by ``range_m``
       - ``__add__`` that returns a new Sensor with type ``"fused"``,
         summed ranges, and averaged accuracies

    2. **``Robot`` class** with:

       - Non-public attributes: ``_name``, ``_battery``, ``_sensors``
         (list)
       - Properties for ``battery`` (validated 0--100) and ``name``
         (read-only)
       - ``add_sensor(sensor: Sensor) -> None`` method
       - ``__contains__`` to check if a sensor type is in the robot
       - ``__iter__`` to iterate over the robot's sensors
       - ``__len__`` to get number of sensors

    3. In the ``if __name__ == "__main__"`` block:

       - Create a Robot, add multiple sensors.
       - Iterate over sensors and print each one.
       - Check membership (e.g., ``"lidar" in robot``).
       - Fuse two sensors with ``+`` and print the result.

    **Expected output:**

    .. code-block:: text

       === Robot Sensors ===
       Scout has 3 sensors:
         Sensor(lidar): range=50.0m
         Sensor(camera): range=30.0m
         Sensor(ultrasonic): range=10.0m

       === Membership ===
       Has lidar: True
       Has radar: False

       === Sensor Fusion ===
       Fused: Sensor(fused): range=80.0m


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture6/robot_with_sensors.py``
    - The program must run without errors and produce output matching the
      expected format above.
    - All calculations must be computed dynamically (no hard-coded
      results).
    - Every class and method must include type hints and a Google-style
      docstring.
