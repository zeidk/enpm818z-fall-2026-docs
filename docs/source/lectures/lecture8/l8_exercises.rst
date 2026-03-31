====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 8. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``~/enpm605_ws/src/first_pkg/``
workspace.


.. dropdown:: Exercise 1 -- Periodic Logger
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice creating an OOP-based ROS 2 node with a timer callback,
    proper spin/shutdown lifecycle, and the ROS 2 logger.


    .. raw:: html

       <hr>


    **Specification**

    Create the file
    ``first_pkg/periodic_logger.py`` that implements the following.

    1. **``PeriodicLogger(Node)``** class:

       - ``__init__(self, node_name: str, period: float = 1.0)``
         that calls ``super().__init__(node_name)``, stores
         ``_period`` and ``_count = 0``, and creates a timer with
         the given period.
       - ``_timer_callback(self) -> None``: logs
         ``"[<count>] Tick at <timestamp>"`` using the ROS 2 logger
         and increments ``_count``. Retrieve the current ROS 2 time
         with ``self.get_clock().now().to_msg()``.

    2. **``scripts/run_periodic_logger.py``** entry point:

       - Initialize ``rclpy``, instantiate ``PeriodicLogger`` with
         node name ``"periodic_logger"`` and period ``0.5``.
       - Wrap the spin in a ``try/except KeyboardInterrupt`` block.
       - Destroy the node and call ``rclpy.shutdown()`` in the
         ``finally`` block.

    3. Register the entry point in ``setup.py``:

       .. code-block:: python

          'periodic_logger = scripts.run_periodic_logger:main',

    **Expected behavior**

    Running ``ros2 run first_pkg periodic_logger`` should produce
    approximately two log lines per second:

    .. code-block:: text

       [INFO] [<timestamp>] [periodic_logger]: [0] Tick at sec: 1741200001 nanosec: 123456789
       [INFO] [<timestamp>] [periodic_logger]: [1] Tick at sec: 1741200001 nanosec: 623456789
       [INFO] [<timestamp>] [periodic_logger]: [2] Tick at sec: 1741200002 nanosec: 123456789

    **Verification commands**

    .. code-block:: console

       ros2 node list           # should show /periodic_logger
       ros2 node info /periodic_logger
       ros2 topic hz /rosout    # should show ~2 Hz


.. dropdown:: Exercise 2 -- String Publisher
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice creating a publisher that sends ``std_msgs/String``
    messages, registering it as a node executable, and inspecting it
    with ROS 2 introspection tools.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``first_pkg/string_publisher.py`` that implements
    the following.

    1. **``StringPublisher(Node)``** class:

       - ``__init__(self, node_name: str)`` that calls
         ``super().__init__(node_name)``, creates a publisher on
         the topic ``"greeting"`` with message type
         ``std_msgs/msg/String`` and queue depth ``10``, initializes
         ``_count = 0``, creates a ``String()`` message object, and
         creates a timer with period ``1.0`` s.
       - ``_timer_callback(self) -> None``: sets
         ``self._message.data`` to
         ``f"Hello from ROS 2 -- message {self._count}"``,
         publishes the message, logs it with the ROS 2 logger,
         and increments ``_count``.

    2. **Entry point** ``scripts/run_string_publisher.py``:

       - Standard lifecycle: ``rclpy.init()``, instantiate
         ``StringPublisher("string_publisher")``, ``rclpy.spin()``,
         ``destroy_node()``, ``rclpy.shutdown()``.

    3. Register in ``setup.py``:

       .. code-block:: python

          'string_publisher = scripts.run_string_publisher:main',

    **Verification**

    After building and running, in a second terminal:

    .. code-block:: console

       ros2 topic list -t           # /greeting [std_msgs/msg/String]
       ros2 topic echo /greeting    # prints each message
       ros2 topic hz /greeting      # should show ~1.0 Hz
       rqt_graph                    # node -> topic visible


.. dropdown:: Exercise 3 -- String Subscriber
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice creating a subscriber with a named callback, running
    both publisher and subscriber simultaneously, and verifying
    end-to-end communication.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``first_pkg/string_subscriber.py`` that implements
    the following.

    1. **``StringSubscriber(Node)``** class:

       - ``__init__(self, node_name: str)`` that calls
         ``super().__init__(node_name)``, creates a subscription on
         topic ``"greeting"`` with message type
         ``std_msgs/msg/String``, queue depth ``10``, and a named
         callback.
       - ``_subscriber_callback(self, msg: String) -> None``:
         logs ``f"Received: {msg.data}"`` using the ROS 2 logger.

    2. **Entry point** ``scripts/run_string_subscriber.py``:

       - Standard lifecycle matching Exercise 2.

    3. Register in ``setup.py``:

       .. code-block:: python

          'string_subscriber = scripts.run_string_subscriber:main',

    **Expected behavior**

    Run the publisher from Exercise 2 in Terminal 1 and this
    subscriber in Terminal 2:

    .. code-block:: text

       [INFO] [<timestamp>] [string_subscriber]: Received: Hello from ROS 2 -- message 0
       [INFO] [<timestamp>] [string_subscriber]: Received: Hello from ROS 2 -- message 1
       [INFO] [<timestamp>] [string_subscriber]: Received: Hello from ROS 2 -- message 2

    **Verification**

    .. code-block:: console

       ros2 topic info /greeting -v    # shows publisher and subscriber counts
       rqt_graph                       # both nodes connected via /greeting


.. dropdown:: Exercise 4 -- QoS Mismatch Investigation
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Observe the effects of QoS incompatibility first-hand and use
    introspection tools to diagnose the problem.


    .. raw:: html

       <hr>


    **Specification**

    This exercise has two parts.

    **Part A -- Create a BEST_EFFORT publisher**

    Modify a copy of ``string_publisher.py`` saved as
    ``first_pkg/qos_publisher.py``. Change the publisher to use an
    explicit ``QoSProfile`` with ``ReliabilityPolicy.BEST_EFFORT``,
    ``DurabilityPolicy.VOLATILE``, ``HistoryPolicy.KEEP_LAST``, and
    ``depth=10``. Keep the topic name ``"qos_test"`` and message type
    ``std_msgs/msg/String``. Register as ``'qos_publisher = ...'``
    in ``setup.py``.

    **Part B -- Create a RELIABLE subscriber**

    Create ``first_pkg/qos_subscriber.py`` with a
    ``QoSProfile`` using ``ReliabilityPolicy.RELIABLE`` and all other
    policies at their defaults. Subscribe to ``"qos_test"``.
    Register as ``'qos_subscriber = ...'`` in ``setup.py``.

    **Investigation steps**

    1. Run both nodes simultaneously.
    2. Observe that the subscriber callback is never invoked.
    3. Run ``ros2 topic info /qos_test -v`` and note the QoS printed
       for publisher and subscriber.
    4. Run ``ros2 doctor --report | grep qos`` and record the output.
    5. Fix the mismatch by changing the subscriber to
       ``ReliabilityPolicy.BEST_EFFORT`` and confirm that messages are
       now received.

    **Written reflection (include as a comment block at the top of
    qos_subscriber.py)**

    Answer these questions in 3-5 sentences:

    - What did ``ros2 topic info -v`` show before and after the fix?
    - Why does DDS produce no error when QoS is incompatible?
    - In what real-world scenario would a QoS mismatch cause a
      hard-to-debug failure?
