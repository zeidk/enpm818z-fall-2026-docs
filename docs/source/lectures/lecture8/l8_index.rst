====================================================
L8: Introduction to ROS 2
====================================================

Overview
--------

This lecture introduces ROS 2 as the middleware framework for building
distributed robotic applications. You will learn the architecture and
core design philosophy of ROS 2, set up a workspace, and write your
first Python nodes. The lecture covers how nodes communicate
asynchronously using topics, messages, publishers, and subscribers,
and introduces Quality of Service (QoS) policies that govern how
messages are delivered. The lecture concludes with a detailed analysis
of three publisher-subscriber timing scenarios to build intuition about
what happens when nodes run at different speeds. All hands-on examples
use the ``first_pkg`` Python package created during the lecture.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain the ROS 2 distributed architecture and core components.
- Set up a ROS 2 workspace and shell environment.
- Create and build Python packages with ``colcon``.
- Write minimal and OOP-based ROS 2 nodes using ``rclpy``.
- Use timers and callback functions to drive periodic behavior.
- Implement publishers that send messages on a topic.
- Implement subscribers that receive and process topic messages.
- Configure Quality of Service (QoS) profiles.
- Analyze publisher-subscriber communication under different timing
  scenarios.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   l8_lecture
   l8_exercises
   l8_quiz
   l8_references


Next Steps
----------

- In the next lecture, we will cover parameters and executors:

  - Declaring and reading node parameters
  - Passing parameters from launch files
  - Single-threaded and multi-threaded executors
  - Callback groups for concurrent execution

- Complete the exercises from this lecture before the next class.
- Read `Using Parameters in a Class (Python)
  <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html>`_.
