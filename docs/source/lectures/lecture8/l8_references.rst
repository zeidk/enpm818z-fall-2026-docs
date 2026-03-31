References
==========


.. dropdown:: Lecture 8
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L8: Introduction to ROS 2**

        Covers the ROS 2 distributed architecture, DDS middleware and
        QoS policies, the publish/subscribe model (nodes, topics,
        messages, rules, patterns), workspace setup and ``colcon``
        builds, Python package creation (``package.xml``, ``setup.py``,
        ``ament_python``), writing minimal and OOP-based nodes with
        ``rclpy``, spinning and the executor model, timers and
        callbacks, publishers (``create_publisher``, ``Int64``,
        ``QoSProfile``), subscribers (``create_subscription``, named
        callbacks), and three pub/sub communication timing scenarios
        (no subscriber, fast subscriber, slow subscriber).


.. dropdown:: ROS 2 Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ROS 2 Jazzy Documentation
            :link: https://docs.ros.org/en/jazzy/
            :class-card: sd-border-secondary

            **docs.ros.org**

            The official ROS 2 Jazzy documentation hub. Starting point
            for all ROS 2 concepts, tutorials, and API references.

            +++

            - Concepts overview
            - Tutorials (beginner to advanced)
            - API reference

        .. grid-item-card:: ROS 2 Beginner Tutorials
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries.html
            :class-card: sd-border-secondary

            **Beginner: Client Libraries**

            Step-by-step tutorials for writing nodes, publishers,
            subscribers, services, and actions in Python.

            +++

            - Creating a workspace
            - Writing a simple publisher/subscriber
            - Writing a simple service/client

        .. grid-item-card:: rclpy API Reference
            :link: https://docs.ros.org/en/jazzy/p/rclpy/
            :class-card: sd-border-secondary

            **rclpy**

            Full Python API reference for the ``rclpy`` client library.

            +++

            - ``Node`` class
            - ``create_publisher``, ``create_subscription``
            - ``create_timer``, ``spin``, ``shutdown``

        .. grid-item-card:: ROS 2 QoS Settings
            :link: https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Quality-of-Service-Settings.html
            :class-card: sd-border-secondary

            **QoS Concepts**

            Detailed explanation of all QoS policies, compatibility
            rules, and predefined profiles.

            +++

            - Reliability, durability, history, deadline
            - Compatibility matrix
            - Predefined profiles

        .. grid-item-card:: ROS 2 Logging
            :link: https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Logging.html
            :class-card: sd-border-secondary

            **About Logging**

            How the ROS 2 logging system works, severity levels, and
            configuration options.

            +++

            - Log levels: DEBUG, INFO, WARN, ERROR, FATAL
            - ``/rosout`` topic
            - Log file output

        .. grid-item-card:: colcon Documentation
            :link: https://colcon.readthedocs.io/
            :class-card: sd-border-secondary

            **colcon**

            Official documentation for the colcon build tool.

            +++

            - ``colcon build`` flags
            - ``--symlink-install``
            - Package discovery


.. dropdown:: DDS and Middleware
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: OMG DDS Portal
            :link: https://www.omg.org/omg-dds-portal/
            :class-card: sd-border-secondary

            **Object Management Group**

            Official DDS standard, specification downloads, and
            community resources.

            +++

            - DDS specification
            - RTPS wire protocol
            - Vendor landscape

        .. grid-item-card:: DDS Foundation
            :link: https://www.dds-foundation.org/
            :class-card: sd-border-secondary

            **DDS Foundation**

            Use cases, QoS reference, webinar series, and historical
            overview of DDS adoption.

            +++

            - QoS policy reference
            - Application domain case studies
            - Interoperability

        .. grid-item-card:: eProsima Fast DDS
            :link: https://fast-dds.docs.eprosima.com/
            :class-card: sd-border-secondary

            **Fast DDS Documentation**

            Documentation for the default ROS 2 DDS implementation
            (eProsima Fast DDS).

            +++

            - Configuration
            - QoS profiles
            - Discovery settings

        .. grid-item-card:: ROS 2 DDS Vendor Guide
            :link: https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Different-Middleware-Vendors.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Middleware Vendors**

            Comparison of supported RMW implementations for Jazzy:
            Fast DDS, Cyclone DDS, Connext DDS, GurumDDS.

            +++

            - Switching RMW at runtime
            - Vendor feature comparison
            - Installation instructions


.. dropdown:: External Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Articulated Robotics: ROS 2 Tutorials
            :link: https://articulatedrobotics.xyz/category/ros2-tutorials/
            :class-card: sd-border-secondary

            **Articulated Robotics**

            Practical video and written tutorials for ROS 2 from
            workspace setup through navigation.

            +++

            - Workspace setup
            - Publisher/subscriber patterns
            - Launch files

        .. grid-item-card:: The Construct: ROS 2 Basics
            :link: https://www.theconstructsim.com/ros2-for-beginners/
            :class-card: sd-border-secondary

            **The Construct**

            Browser-based ROS 2 environment with guided courses for
            beginners through advanced users.

            +++

            - Interactive exercises
            - No local install required
            - Structured curriculum

        .. grid-item-card:: Real Python: Python Classes (OOP)
            :link: https://realpython.com/python3-object-oriented-programming/
            :class-card: sd-border-secondary

            **Real Python**

            Review of Python OOP concepts underlying OOP node design:
            classes, inheritance, ``__init__``, ``super()``.

            +++

            - Class definition and instantiation
            - Inheritance and ``super()``
            - Instance and class attributes


.. dropdown:: Style and Best Practices
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ROS 2 Python Style Guide
            :link: https://docs.ros.org/en/jazzy/Contributing/Code-Style-Language-Versions.html
            :class-card: sd-border-secondary

            **ROS 2 Coding Standards**

            Official style guidelines for Python and C++ ROS 2 code.

            +++

            - Naming conventions
            - Node class structure
            - Docstring style

        .. grid-item-card:: PEP 8 -- Python Style Guide
            :link: https://peps.python.org/pep-0008/
            :class-card: sd-border-secondary

            **Coding Conventions**

            Python style guide applied throughout ROS 2 Python code.

            +++

            - ``snake_case`` for topic names and variables
            - Class naming: ``CamelCase``
            - Import ordering


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Anis Koubaa (Ed.)
            :class-card: sd-border-secondary

            **Robot Operating System (ROS): The Complete Reference
            (Vol. 1-7)**

            A multi-volume series covering ROS and ROS 2 from
            fundamentals through advanced applications. Relevant
            chapters cover distributed architectures, DDS, and
            communication patterns.

        .. grid-item-card:: Open Robotics
            :class-card: sd-border-secondary

            **Programming Robots with ROS 2**

            Hands-on guide to writing ROS 2 applications in Python and
            C++, covering nodes, topics, services, actions, parameters,
            and launch files.

        .. grid-item-card:: Silberschatz, Galvin, and Gagne
            :class-card: sd-border-secondary

            **Operating System Concepts (10th Edition)**

            Chapter 3 (Processes) and Chapter 4 (Threads) provide the
            OS-level background for understanding ROS 2 process
            isolation, the main thread, and the executor spin loop.

        .. grid-item-card:: Object Management Group
            :class-card: sd-border-secondary

            **DDS Specification v1.4**

            The formal OMG specification for the Data Distribution
            Service. Appendix A contains the complete QoS policy
            reference with compatibility rules and default values.
