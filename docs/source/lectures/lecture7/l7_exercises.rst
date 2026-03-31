====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 7. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``lecture7/`` workspace folder.


.. dropdown:: Exercise 1 -- Robot Hierarchy
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice single and hierarchical inheritance, ``super()``, method
    overriding, and runtime type inspection with ``isinstance()`` and
    ``issubclass()``.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture7/robot_hierarchy.py`` that implements the
    following. Each class and method must include type hints and a
    Google-style docstring.

    1. **``Robot`` base class** (provided skeleton -- implement it fully):

       - ``__init__(self, name: str, battery: int = 100)``
       - Instance attributes: ``_name`` (``str``), ``_battery`` (``int``)
       - ``perform_task(self, task_name: str) -> None`` that prints
         ``"<n> performing: <task_name>"`` and decreases ``_battery``
         by 10. If ``_battery < 10``, print ``"<n> needs recharging!"``
         and do not perform the task.
       - ``recharge(self) -> None`` that sets ``_battery`` to 100 and
         prints ``"<n> fully recharged!"``.
       - ``__repr__(self) -> str`` that returns
         ``"Robot(name='<n>', battery=<battery>)"``.

    2. **``MobileRobot(Robot)``**:

       - ``__init__(self, name: str, max_speed: float, terrain_type: str, battery: int = 100)``
         that calls ``super().__init__()`` then sets ``_max_speed``
         (``float``, m/s) and ``_terrain_type`` (``str``).
       - ``move(self, direction: str) -> None`` that prints
         ``"<n> moving <direction> at up to <max_speed> m/s"``.
       - ``__repr__(self) -> str`` that returns
         ``"MobileRobot(name='<n>', battery=<battery>, max_speed=<max_speed>)"``.

    3. **``ManipulatorRobot(Robot)``**:

       - ``__init__(self, name: str, arm_reach: float, payload_capacity: float, battery: int = 100)``
         that calls ``super().__init__()`` then sets ``_arm_reach``
         (``float``, m) and ``_payload_capacity`` (``float``, kg).
       - ``move(self, direction: str) -> None`` that prints
         ``"<n> repositioning <direction>"``.
       - ``pick_up(self, obj: str) -> None`` that prints
         ``"<n> picking up: <obj>"``.
       - ``deliver(self, obj: str, zone: str) -> None`` that prints
         ``"<n> delivering <obj> to zone <zone>"``.
       - ``__repr__(self) -> str`` that returns
         ``"ManipulatorRobot(name='<n>', battery=<battery>, arm_reach=<arm_reach>)"``.

    4. In the ``if __name__ == "__main__"`` block:

    .. code-block:: python

       if __name__ == "__main__":
           scout = MobileRobot("Scout", max_speed=1.5, terrain_type="indoor")
           arm   = ManipulatorRobot("Arm-1", arm_reach=0.8, payload_capacity=2.0)

           scout.move("north")
           scout.perform_task("navigate to zone B")

           arm.move("left")
           arm.pick_up("widget-42")
           arm.deliver("widget-42", "dropoff")

           print(scout)
           print(arm)

           # isinstance checks
           print(isinstance(scout, MobileRobot))      # True
           print(isinstance(scout, Robot))             # True
           print(isinstance(scout, ManipulatorRobot))  # False

           # issubclass checks
           print(issubclass(MobileRobot, Robot))       # True
           print(issubclass(ManipulatorRobot, Robot))  # True

    **Expected output:**

    .. code-block:: text

       Scout moving north at up to 1.5 m/s
       Scout performing: navigate to zone B
       Arm-1 repositioning left
       Arm-1 picking up: widget-42
       Arm-1 delivering widget-42 to zone dropoff
       MobileRobot(name='Scout', battery=90, max_speed=1.5)
       ManipulatorRobot(name='Arm-1', battery=100, arm_reach=0.8)
       True
       True
       False
       True
       True


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture7/robot_hierarchy.py``
    - The program must run without errors and produce output matching the
      expected format above.
    - Every class and method must include type hints and a Google-style
      docstring.


.. dropdown:: Exercise 2 -- Abstract Robot Interface
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice defining abstract base classes with the ``abc`` module,
    enforcing interface contracts with ``@abstractmethod``, mixing
    abstract and concrete methods, and verifying that Python raises
    ``TypeError`` when an abstract class is instantiated directly.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture7/robot_abstract.py`` that implements the
    following. Each class and method must include type hints and a
    Google-style docstring.

    1. **``Robot`` abstract base class** (inherits from ``ABC``):

       - ``__init__(self, name: str, battery: int = 100)`` that sets
         ``_name`` and ``_battery``.
       - ``@abstractmethod move(self, direction: str) -> None``
       - Concrete ``perform_task(self, task_name: str) -> None`` that
         prints ``"<n> performing: <task_name>"`` and decreases
         ``_battery`` by 10. If ``_battery < 10``, print
         ``"<n> needs recharging!"`` and do not perform the task.
       - Concrete ``recharge(self) -> None`` that sets ``_battery`` to
         100 and prints ``"<n> fully recharged!"``.

    2. **``MobileRobot(Robot)``**:

       - ``__init__(self, name: str, max_speed: float, terrain_type: str, battery: int = 100)``
         that calls ``super().__init__()`` then sets ``_max_speed``
         and ``_terrain_type``.
       - ``move(self, direction: str) -> None`` that prints
         ``"<n> moving <direction> at up to <max_speed> m/s"``.

    3. **``ManipulatorRobot(Robot)``**:

       - ``__init__(self, name: str, arm_reach: float, payload_capacity: float, battery: int = 100)``
         that calls ``super().__init__()`` then sets ``_arm_reach``
         and ``_payload_capacity``.
       - ``move(self, direction: str) -> None`` that prints
         ``"<n> repositioning <direction>"``.

    4. In the ``if __name__ == "__main__"`` block:

    .. code-block:: python

       if __name__ == "__main__":
           # Confirm Robot cannot be instantiated directly
           try:
               r = Robot("Base")
           except TypeError as e:
               print(f"TypeError: {e}")

           scout = MobileRobot("Scout", max_speed=1.5, terrain_type="indoor")
           arm   = ManipulatorRobot("Arm-1", arm_reach=0.8, payload_capacity=2.0)

           scout.move("north")
           scout.perform_task("navigate to zone B")

           arm.move("left")
           arm.perform_task("pick widget")

           arm.recharge()          # inherited concrete method

    **Expected output:**

    .. code-block:: text

       TypeError: Can't instantiate abstract class Robot without an implementation for abstract method 'move'
       Scout moving north at up to 1.5 m/s
       Scout performing: navigate to zone B
       Arm-1 repositioning left
       Arm-1 performing: pick widget
       Arm-1 fully recharged!


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture7/robot_abstract.py``
    - The program must run without errors and produce output matching the
      expected format above.
    - Every class and method must include type hints and a Google-style
      docstring.


.. dropdown:: Exercise 3 -- ``__slots__`` and Memory Comparison
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice using ``__slots__`` to restrict instance attributes, measure
    the memory savings over regular instances, and extend a slotted class
    through inheritance.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture7/robot_slots.py`` that implements the
    following. Each class and method must include type hints and a
    Google-style docstring.

    1. **``Pose`` class** (without ``__slots__``):

       - ``__init__(self, x: float, y: float, heading: float)`` that sets
         ``_x``, ``_y``, and ``_heading``.
       - Read-only ``@property`` for each attribute: ``x``, ``y``,
         ``heading``.
       - ``__repr__(self) -> str`` that returns
         ``"Pose(x=<x>, y=<y>, heading=<heading>)"``.

    2. **``PoseSlotted`` class** (identical behavior to ``Pose`` but
       declares ``__slots__ = ("_x", "_y", "_heading")``):

       - Same ``__init__``, properties, and ``__repr__`` as ``Pose``.
       - Verify that assigning a dynamic attribute (e.g.,
         ``pose._extra = 1``) raises ``AttributeError``.

    3. **Memory comparison**: create 1000 instances of each class and
       compare total memory use. For ``Pose``, total memory per instance
       is ``sys.getsizeof(instance) + sys.getsizeof(instance.__dict__)``.
       For ``PoseSlotted``, total memory per instance is
       ``sys.getsizeof(instance)`` only. Print the difference.

    4. **``StampedPose(PoseSlotted)``**:

       - Adds ``_timestamp: float`` via ``__slots__ = ("_timestamp",)``.
         Do not redeclare ``_x``, ``_y``, or ``_heading``.
       - ``__init__(self, x: float, y: float, heading: float, timestamp: float)``
         that calls ``super().__init__(x, y, heading)`` then sets
         ``_timestamp``.
       - Read-only ``@property timestamp``.
       - ``__repr__(self) -> str`` that returns
         ``"StampedPose(x=<x>, y=<y>, heading=<heading>, timestamp=<timestamp>)"``.

    5. In the ``if __name__ == "__main__"`` block:

    .. code-block:: python

       if __name__ == "__main__":
           import sys

           # Verify dynamic attribute restriction
           ps = PoseSlotted(1.0, 2.0, 0.0)
           try:
               ps._extra = "dynamic"
           except AttributeError as e:
               print(f"AttributeError: {e}")

           # Memory comparison
           poses   = [Pose(float(i), float(i), 0.0) for i in range(1000)]
           slotted = [PoseSlotted(float(i), float(i), 0.0) for i in range(1000)]

           pose_mem    = sum(sys.getsizeof(p) + sys.getsizeof(p.__dict__) for p in poses)
           slotted_mem = sum(sys.getsizeof(p) for p in slotted)

           print(f"Pose total (1000 instances):        {pose_mem} bytes")
           print(f"PoseSlotted total (1000 instances): {slotted_mem} bytes")
           print(f"Memory saved:                       {pose_mem - slotted_mem} bytes")

           # StampedPose
           sp = StampedPose(1.0, 2.0, 0.5, timestamp=1712345678.0)
           print(sp)
           print(sp.x, sp.y, sp.heading, sp.timestamp)

    **Expected output (values are approximate):**

    .. code-block:: text

       AttributeError: 'PoseSlotted' object has no attribute '_extra'
       Pose total (1000 instances):        280000 bytes
       PoseSlotted total (1000 instances): 56000 bytes
       Memory saved:                       224000 bytes
       StampedPose(x=1.0, y=2.0, heading=0.5, timestamp=1712345678.0)
       1.0 2.0 0.5 1712345678.0

    .. note::

       Exact byte counts will vary by Python version and platform. The
       important result is that ``PoseSlotted`` uses significantly less
       memory than ``Pose``.


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture7/robot_slots.py``
    - The program must run without errors and produce output consistent
      with the expected format above.
    - Every class and method must include type hints and a Google-style
      docstring.


.. dropdown:: Exercise 4 -- Protocols and Structural Subtyping
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice defining a ``typing.Protocol``, implementing it in
    independent classes without inheritance, writing a polymorphic
    function that accepts any conforming type, and using
    ``@runtime_checkable`` for ``isinstance()`` checks.


    .. raw:: html

       <hr>


    **Specification**

    Create a file ``lecture7/robot_protocols.py`` that implements the
    following. Each class and method must include type hints and a
    Google-style docstring.

    1. **``Executable`` protocol** (``@runtime_checkable``):

       - ``execute(self, robot_name: str) -> bool``

    2. **``PickTask``** (no shared base class with ``DeliverTask``):

       - ``execute(self, robot_name: str) -> bool`` that prints
         ``"<robot_name> picks an object"`` and returns ``True``.

    3. **``DeliverTask``** (no shared base class with ``PickTask``):

       - ``execute(self, robot_name: str) -> bool`` that prints
         ``"<robot_name> delivers to destination"`` and returns ``True``.

    4. **``SleepTask``**: a class with no ``execute()`` method (add
       ``sleep(self, duration: float) -> None`` instead). Used to confirm
       that it does not satisfy ``Executable``.

    5. **``dispatch(task: Executable, robot_name: str) -> bool``**:
       a module-level function that calls ``task.execute(robot_name)``
       and returns its result.

    6. In the ``if __name__ == "__main__"`` block:

    .. code-block:: python

       if __name__ == "__main__":
           pick    = PickTask()
           deliver = DeliverTask()
           sleep   = SleepTask()

           dispatch(pick,    "Scout")
           dispatch(deliver, "Arm-1")

           # isinstance checks via @runtime_checkable
           print(isinstance(pick,    Executable))   # True
           print(isinstance(deliver, Executable))   # True
           print(isinstance(sleep,   Executable))   # False

    **Expected output:**

    .. code-block:: text

       Scout picks an object
       Arm-1 delivers to destination
       True
       True
       False


    .. raw:: html

       <hr>


    **Deliverables**

    - ``lecture7/robot_protocols.py``
    - The program must run without errors and produce output matching the
      expected format above.
    - Every class and method must include type hints and a Google-style
      docstring.