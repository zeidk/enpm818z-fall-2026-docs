====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 8: Introduction to
ROS 2, including the distributed architecture, DDS, pub/sub model,
workspace setup, node design (minimal and OOP), spinning, timers,
publishers, subscribers, QoS policies, and communication timing
scenarios.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement
     is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   What is the primary role of DDS in ROS 2?

   A. It is a build tool that compiles ROS 2 packages.

   B. It is the middleware layer that handles node discovery, message
      transport, and QoS enforcement between nodes.

   C. It is the Python client library used to write ROS 2 nodes.

   D. It is a visualization tool for inspecting the ROS 2 computation
      graph.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- DDS is the middleware layer that handles node discovery,
   message transport, and QoS enforcement between nodes.

   DDS (Data Distribution Service) sits beneath the ``rclpy``/``rclcpp``
   API and transparently handles participant discovery via multicast,
   serialization/deserialization of messages, transport over UDP/TCP/shared
   memory, and enforcement of per-topic QoS policies. Node developers
   interact only with the ROS 2 API; DDS operates invisibly underneath.


.. admonition:: Question 2
   :class: hint

   What is the correct order of ``colcon build`` output directories?

   A. ``src/``, ``build/``, ``install/``, ``log/``

   B. ``build/``, ``install/``, ``log/`` (``src/`` is not created by
      colcon)

   C. ``build/``, ``log/``, ``dist/``

   D. ``install/``, ``dist/``, ``log/``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``build/``, ``install/``, ``log/`` (``src/`` is not created
   by colcon).

   ``colcon build`` scans the existing ``src/`` directory for packages
   and creates ``build/`` (intermediate artifacts), ``install/`` (final
   install tree including ``setup.bash``), and ``log/`` (build logs).
   The ``src/`` directory is created manually by the developer before
   the first build.


.. admonition:: Question 3
   :class: hint

   What happens if you call ``ros2 run first_pkg minimal_node`` and the
   node contains no ``rclpy.spin()`` call?

   A. The node runs indefinitely, waiting for callbacks.

   B. The node raises a ``RuntimeError`` because spin is mandatory.

   C. The node starts, executes its ``main()`` body, and exits
      immediately.

   D. The node silently blocks without doing anything.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The node starts, executes its ``main()`` body, and exits
   immediately.

   Without ``rclpy.spin()``, the main thread is never handed to the
   executor. The node registers with the ROS 2 runtime, executes any
   code after ``rclpy.init()``, and then reaches ``rclpy.shutdown()``
   and exits. No callbacks ever fire. ``ros2 node list`` will show
   nothing because the process has already terminated.


.. admonition:: Question 4
   :class: hint

   Which ``create_publisher()`` argument controls how many undelivered
   messages are buffered before the oldest is dropped?

   A. The message type.

   B. The topic name.

   C. The queue depth (third positional argument).

   D. The ``reliability`` policy.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The queue depth (third positional argument).

   Under the default ``KEEP_LAST`` history policy, the queue depth
   (``depth``) determines how many messages are held in the buffer.
   When the queue is full, the oldest message is evicted to make room
   for the newest incoming message. Passing an integer as the third
   argument to ``create_publisher()`` sets this depth with all other
   QoS policies at their defaults.


.. admonition:: Question 5
   :class: hint

   A subscriber with ``RELIABLE`` reliability policy tries to connect
   to a publisher with ``BEST_EFFORT`` reliability. What happens?

   A. The subscriber receives all messages but logs a warning.

   B. DDS silently refuses the connection; no messages are delivered
      and no error is raised.

   C. ROS 2 raises a ``QoSIncompatibleError`` at runtime.

   D. The subscriber falls back to ``BEST_EFFORT`` automatically.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- DDS silently refuses the connection; no messages are
   delivered and no error is raised.

   A ``RELIABLE`` subscriber requires guaranteed delivery; a
   ``BEST_EFFORT`` publisher cannot provide that guarantee. DDS
   therefore refuses to establish the connection. The failure is
   completely silent -- no exception, no warning in the log. This is
   one of the most common silent bugs in ROS 2. Diagnose with
   ``ros2 topic info /topic -v``.


.. admonition:: Question 6
   :class: hint

   What does ``--symlink-install`` do when passed to ``colcon build``?

   A. It builds only the packages that have changed since the last
      build.

   B. It creates symbolic links to Python source files and config
      files in ``install/``, so edits take effect without rebuilding.

   C. It links the workspace to the base ROS 2 installation
      automatically.

   D. It enables incremental compilation for C++ packages.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It creates symbolic links to Python source files and config
   files in ``install/``, so edits take effect without rebuilding.

   Without ``--symlink-install``, ``colcon build`` copies Python files
   into ``install/``. Any edit to the source requires a rebuild to
   take effect. With ``--symlink-install``, ``install/`` contains
   symlinks back to the source files; a change to a ``.py`` file is
   immediately visible on the next ``ros2 run``. Note: new entry points
   and data file declarations in ``setup.py`` still require a rebuild.


.. admonition:: Question 7
   :class: hint

   In an OOP-based ROS 2 node, why is the spin loop placed in the
   entry point script rather than inside the node class?

   A. Because ``rclpy.spin()`` can only be called from a ``__main__``
      block.

   B. Because placing it in the class would cause a recursion error.

   C. To keep the class reusable by any executor or entry point script
      without modification.

   D. Because ROS 2 automatically adds a spin loop to all Node
      subclasses.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- To keep the class reusable by any executor or entry point
   script without modification.

   The node class defines behavior (publishers, subscribers, timers,
   callbacks). The entry point script handles initialization,
   spinning, cleanup, and shutdown. Keeping the spin loop out of the
   class means the same class can be instantiated by different scripts,
   handed to different executors (single-threaded, multi-threaded), or
   combined with other nodes in a single process -- all without
   changing the class itself.


.. admonition:: Question 8
   :class: hint

   What is the correct import and instantiation for a ``geometry_msgs``
   ``Pose`` message?

   A.
      .. code-block:: python

         from geometry_msgs import Pose
         pose = Pose.new()

   B.
      .. code-block:: python

         from geometry_msgs.msg import Pose
         pose = Pose()

   C.
      .. code-block:: python

         import geometry_msgs
         pose = geometry_msgs.Pose()

   D.
      .. code-block:: python

         from rclpy.msgs import Pose
         pose = Pose()

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``from geometry_msgs.msg import Pose`` followed by
   ``pose = Pose()``.

   All ROS 2 message classes live in the ``.msg`` subpackage of their
   package (e.g., ``std_msgs.msg``, ``geometry_msgs.msg``). They are
   imported directly and instantiated with ``MsgType()``. All numeric
   fields default to ``0`` or ``0.0`` on construction.


.. admonition:: Question 9
   :class: hint

   A publisher runs at 2 Hz with QoS depth 3 (``KEEP_LAST``). The
   subscriber callback takes 1.7 s to complete. After the queue fills
   up, what happens to new incoming messages?

   A. New messages are discarded by the publisher and never enter the
      queue.

   B. New messages are buffered in an unlimited overflow area.

   C. The oldest message in the queue is evicted to make room for the
      newest message.

   D. The publisher slows down automatically to match the subscriber.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The oldest message in the queue is evicted to make room
   for the newest message.

   Under the ``KEEP_LAST`` history policy, the queue has a fixed
   capacity equal to ``depth``. When the queue is full and a new
   message arrives, the oldest buffered message is dropped. The
   subscriber always processes the most recent available data, but may
   miss intermediate messages entirely. Increasing the depth only
   delays the first drop; it does not eliminate message loss when the
   subscriber is persistently slower than the publisher.


.. admonition:: Question 10
   :class: hint

   Which command shows the publishing frequency of the ``/counter``
   topic in a running ROS 2 system?

   A. ``ros2 topic info /counter``

   B. ``ros2 topic echo /counter``

   C. ``ros2 topic hz /counter``

   D. ``ros2 node info /counter``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``ros2 topic hz /counter``

   ``ros2 topic hz`` subscribes to the topic and measures the average
   message arrival rate in Hz. It is the primary tool for confirming
   that a publisher is running at the expected frequency. ``echo``
   prints message contents; ``info`` shows metadata and QoS; ``node info``
   describes a node, not a topic.


----


True / False
============

.. admonition:: Question 11
   :class: hint

   **True or False:** ``rclpy.spin(node)`` must be called inside the
   node class's ``__init__`` method.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``rclpy.spin(node)`` belongs in the **entry point script**, not
   inside the node class. The spin loop is part of the application
   lifecycle (initialize, spin, cleanup), not part of the node's
   behavior. Keeping it in the entry point makes the class reusable
   by different executors and scripts without modification.


.. admonition:: Question 12
   :class: hint

   **True or False:** A ROS 2 publisher sends messages only when at
   least one subscriber is connected.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   A publisher sends messages regardless of whether any subscriber is
   listening (Rule 3 of the pub/sub model). If no subscriber is
   connected and the durability policy is ``VOLATILE`` (the default),
   messages are discarded by DDS immediately. The publisher is
   completely unaware of whether subscribers exist.


.. admonition:: Question 13
   :class: hint

   **True or False:** ``package.xml`` and ``setup.py`` must agree on
   the package name and version.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The ROS 2 build system reads both files and expects consistency.
   A mismatch between the ``name`` field in ``setup.py`` and the
   ``<name>`` tag in ``package.xml``, or between their ``version``
   values, causes a build error. Always update both files together.


.. admonition:: Question 14
   :class: hint

   **True or False:** ``TRANSIENT_LOCAL`` durability ensures that a
   subscriber which joins after the publisher has already sent messages
   will receive the last cached message.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``TRANSIENT_LOCAL`` durability causes the publisher to cache its
   last published message. When a new subscriber connects, DDS
   immediately delivers the cached message to it, even if the
   publisher sent it long before the subscriber existed. Both the
   publisher and subscriber must use ``TRANSIENT_LOCAL`` for this to
   work; a ``VOLATILE`` publisher paired with a ``TRANSIENT_LOCAL``
   subscriber is an incompatible QoS combination.


.. admonition:: Question 15
   :class: hint

   **True or False:** ``colcon build --symlink-install`` means you
   never need to rebuild after adding a new entry point to ``setup.py``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``--symlink-install`` symlinks Python source files and config files
   so that edits to existing ``.py`` files take effect without
   rebuilding. However, adding a **new** entry point or data file
   declaration to ``setup.py`` requires a full ``colcon build`` run,
   because entry points are registered in the install tree during the
   build step, not via symlinks.


.. admonition:: Question 16
   :class: hint

   **True or False:** A subscriber can exist on a topic with no active
   publisher.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   This is Rule 4 of the pub/sub model. A subscriber can be started
   before any publisher exists. It will simply never receive a message
   until a compatible publisher appears. DDS handles the discovery
   automatically when both sides eventually become active.


.. admonition:: Question 17
   :class: hint

   **True or False:** Using ``print()`` instead of
   ``node.get_logger().info()`` in a ROS 2 node is acceptable for
   production code.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   In ROS 2 nodes, ``print()`` should never be used. The ROS 2 logger
   routes messages to the terminal, to timestamped log files, and to
   the ``/rosout`` topic simultaneously. This allows messages to be
   captured, filtered by severity, and replayed. ``print()`` bypasses
   all of these mechanisms and produces output that cannot be filtered,
   timestamped by ROS 2, or subscribed to remotely.


.. admonition:: Question 18
   :class: hint

   **True or False:** A topic name mismatch between a publisher and a
   subscriber causes ROS 2 to raise a runtime exception.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   A topic name mismatch is a **silent failure**. DDS simply never
   establishes a connection between the publisher and subscriber
   because they are on different named channels. No exception is
   raised and no warning is printed. The subscriber callback never
   fires. This is why introspection tools like ``ros2 topic list``
   and ``ros2 topic info`` are essential for debugging communication
   problems.


.. admonition:: Question 19
   :class: hint

   **True or False:** ``ros2 run`` can start multiple nodes from a
   single command.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``ros2 run <package> <executable>`` starts exactly **one** node per
   invocation and blocks the terminal until Ctrl-C is pressed. To
   start multiple nodes from a single command, use
   ``ros2 launch <package> <launch_file>``, which reads a launch file
   and starts all declared nodes in one terminal.


.. admonition:: Question 20
   :class: hint

   **True or False:** The ``resource/`` directory inside a Python ROS 2
   package can be safely deleted to clean up the package layout.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The ``resource/`` directory contains a marker file required by the
   ROS 2 ament package index. Without it, the package cannot be found
   by ``ros2 pkg list`` or other ROS 2 tooling after building. It must
   never be deleted.


----


Essay Questions
===============

.. admonition:: Question 21
   :class: hint

   **Explain the difference between a monolithic and a distributed
   robotic software architecture.** What are the key advantages of the
   distributed approach that ROS 2 enables?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - In a monolithic architecture, all robot software runs in one large
     program. Changing one component risks breaking everything, and a
     single crash takes down the entire system.
   - In a distributed architecture (ROS 2), each component runs as a
     separate OS process (node). Nodes communicate via message passing
     over named topics; they are decoupled and unaware of each other's
     identity.
   - Key advantages: fault isolation (a crashed node does not kill
     others), modularity (nodes can be independently developed, tested,
     and replaced), scalability (the system grows by adding nodes), and
     collaboration (teams work on different nodes in parallel).


.. admonition:: Question 22
   :class: hint

   **Describe the four core QoS policies in ROS 2.** For each policy,
   give a concrete example of when you would choose one setting over
   the other.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - **Reliability**: ``RELIABLE`` for commands or critical state
     (gripper trigger, navigation goal); ``BEST_EFFORT`` for
     high-frequency sensor data (IMU at 200 Hz) where losing an
     occasional message is acceptable.
   - **Durability**: ``TRANSIENT_LOCAL`` for data published once but
     needed by nodes that start later (robot URDF description, static
     map); ``VOLATILE`` for continuous streams where only current
     data matters.
   - **History**: ``KEEP_LAST`` with a chosen depth for bounded memory
     use; ``KEEP_ALL`` only when no message can ever be dropped
     (e.g., event logs with strict audit requirements).
   - **Deadline**: set on sensor topics to detect a failed sensor driver
     -- if no message arrives within the deadline, a callback fires
     to alert the system.


.. admonition:: Question 23
   :class: hint

   **Explain what spinning is in ROS 2 and why a node without a spin
   loop is essentially non-functional.** What is the role of the
   executor during spinning?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Spinning hands the calling thread to the ROS 2 executor, which
     continuously checks for pending callbacks and dispatches them one
     by one.
   - Without spinning, the executor never runs. Timer callbacks never
     fire, subscriber callbacks never receive messages, service
     requests are never processed, and action goals are never handled.
     The node is registered but completely passive.
   - ``rclpy.spin(node)`` is the event loop of a ROS 2 node.
     ``rclpy.spin_once()`` processes one batch and returns, useful
     for interleaving ROS processing with other work.


.. admonition:: Question 24
   :class: hint

   **Describe the three communication timing scenarios covered in the
   lecture** (no subscriber, fast subscriber, slow subscriber). What
   is the key risk in the slow subscriber scenario and how would you
   diagnose it?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - **No subscriber**: DDS discards all messages immediately (with
     ``VOLATILE`` durability). No buffering occurs. The publisher
     runs normally with no performance impact.
   - **Fast subscriber**: the callback completes before the next
     message arrives. The queue never builds up; no messages are
     dropped. This is the ideal scenario.
   - **Slow subscriber**: the callback takes longer than the publish
     interval. The queue fills up and the oldest messages are evicted
     (``KEEP_LAST``). The subscriber continuously processes stale
     data and can never catch up. Increasing queue depth only delays
     the first drop.
   - Diagnose with ``ros2 topic hz /topic`` (confirms publish rate)
     and ``ros2 topic info /topic -v`` (checks QoS). If hz is correct
     but the callback fires less often, the callback is the bottleneck.
