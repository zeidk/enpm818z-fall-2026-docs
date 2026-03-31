====================================================
Changelog
====================================================

All notable changes to the ENPM605 Spring 2026 course documentation are recorded here.


.. dropdown:: v1.3.0 -- L8 Documentation Released (2026-03-21)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Lecture Notes (l8_lecture.rst)

   - Added "What Is ROS?" section: overview, where ROS is used
     (transportation, manufacturing, specialized domains, emerging
     areas), and ROS 1 vs. ROS 2 comparison table.
   - Added "ROS 2 Architecture" section: process definition, monolithic
     vs. distributed design (with figures), core components (nodes,
     topics, services, actions, when to use each), pick-up-a-part
     task example with figure, DDS overview (application domains, key
     properties, resources), and QoS overview (four core policies,
     supported vendors, runtime inspection commands).
   - Added "Publish/Subscribe Model" section: node/topic/message
     definitions, four pub/sub rules, four communication patterns
     (one-to-many, many-to-one, multi-topic, bidirectional) each with
     a figure, introspection tools reference, and ``ros2 run`` vs.
     ``ros2 launch`` comparison table.
   - Added "ROS 2 Setup" section: workspace layout and setup commands,
     colcon build flags, Python package creation workflow, package
     layout with directory descriptions, ``package.xml`` fields and
     dependency tags, and ``setup.py`` entry points and data files.
   - Added "Writing Nodes" section: interfaces (three kinds, standard
     message packages, ``.msg`` to code pipeline, primitive types vs.
     ``std_msgs``, introspection commands, composite message example),
     minimal procedural node, OOP node with separate class and entry
     point, spinning (thread definition with figure, main thread and
     executor figure, why spinning is required, ``try/except/finally``
     pattern, spinning alternatives), timers and callbacks, publishers
     (create, message instantiation options, publish in timer callback,
     run and inspect), QoS (four policies, default vs. explicit profile,
     predefined profiles, compatibility rules, diagnostics), and
     subscribers (create, named vs. lambda callbacks, complete node).
   - Added "Communication Scenarios" section: three scenarios (no
     subscriber, fast subscriber, slow subscriber) each with a
     detailed timing table, plus a summary comparison table and
     diagnostic commands.

   .. rubric:: Index (l8_index.rst)

   - Overview, learning objectives, toctree, and next steps for L8.

   .. rubric:: Exercises (l8_exercises.rst)

   - Exercise 1: Periodic Logger -- OOP node with timer callback
     and ROS 2 clock.
   - Exercise 2: String Publisher -- publisher with ``std_msgs/String``
     and introspection verification.
   - Exercise 3: String Subscriber -- named callback subscriber,
     end-to-end verification with Exercise 2.
   - Exercise 4: QoS Mismatch Investigation -- BEST_EFFORT publisher
     vs. RELIABLE subscriber, silent failure diagnosis, fix and
     written reflection.

   .. rubric:: Quiz (l8_quiz.rst)

   - 10 multiple choice questions covering DDS, colcon, node
     lifecycle, QoS policies, spinning, message types, and timing
     scenarios.
   - 10 true/false questions covering spin placement, publisher
     behavior, package.xml/setup.py consistency, TRANSIENT_LOCAL,
     symlink-install, print vs. logger, silent failures, and
     ros2 run.
   - 4 essay questions: monolithic vs. distributed architecture,
     QoS policies with examples, spinning and the executor, and the
     three communication timing scenarios.

   .. rubric:: Glossary (l8_glossary.rst)

   - 30 terms defined across 14 letter sections: Action, ament_python,
     Callback, colcon, DDS, Durability, Entry Point, Executor,
     Interface, Launch File, Message, Middleware, Node, package.xml,
     Process, Publisher, QoS, Queue Depth, rclpy, Reliability, ROS 2
     Workspace, rosdep, RTPS, Service, Spinning, Subscriber, setup.py,
     Thread, Timer, Topic, Workspace Overlay.

   .. rubric:: References (l8_references.rst)

   - Lecture 8 card summarizing all topics covered.
   - ROS 2 Official Documentation: Jazzy docs, beginner tutorials,
     rclpy API, QoS concepts, logging, colcon docs.
   - DDS and Middleware: OMG DDS Portal, DDS Foundation, Fast DDS,
     ROS 2 DDS vendor guide.
   - External Tutorials: Articulated Robotics, The Construct,
     Real Python OOP review.
   - Style and Best Practices: ROS 2 Python style guide, PEP 8.
   - Recommended Reading: Koubaa ROS 2 series, Programming Robots
     with ROS 2, Silberschatz OS Concepts, OMG DDS Specification.


.. dropdown:: v1.2.0 -- L6 Lecture, Exercises, and Quiz Updated (2026-03-02)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Lecture Notes (l6_lecture.rst)

   - Added "How Do We Achieve Abstraction?" dropdown with three levels (Documentation, Public Interface, Abstract Classes as L7 preview)
   - Added "How to Achieve Encapsulation" summary dropdown
   - Split ``@property`` dropdown into four separate sections: intro, Defining a Getter, Defining a Setter with Validation, and Using Properties
   - Added "Encapsulation Summary" dropdown after Read-Only Properties
   - Updated Class Attributes dropdown: removed ``max_reach`` for clarity, added shadowing warning (``self`` vs class name)
   - Added full **Appendix: Exception Handling** section with 12 dropdowns covering: runtime errors, common built-in exceptions, ``try``/``except``, accessing the exception object, handling multiple exception types, ``else`` clause, ``finally`` clause, full ``try`` statement, ``raise`` statement, why ``raise`` matters for OOP, and ``return NotImplemented`` vs ``raise NotImplementedError``

   .. rubric:: Exercises (l6_exercises.rst)

   - Exercises 1, 2, and 3: added full ``if __name__ == "__main__"`` blocks from ``L6_exercises.py``
   - Updated expected output for all three exercises to match the provided main blocks

   .. rubric:: Quiz (l6_quiz.rst)

   - Updated quiz description to reference the exception handling appendix
   - Added 3 new questions (Q31--Q33) in a new "Exception Handling (Appendix)" section covering ``try``/``except`` output, ``else`` clause purpose, and ``ValueError`` vs ``TypeError``

   .. rubric:: Slides (ENPM605-L6-v1_0.tex)

   - Bumped version to v1.2
   - Restructured lecture into Design Phase and Implementation Phase sections
   - Added "Before We Start" slide referencing the appendix
   - Added Class Attributes slide with shadowing warning
   - Added "How Do We Achieve Abstraction?" slide (3 levels)
   - Added "How to Achieve Encapsulation" summary slide
   - Split ``@property`` content across separate slides (Pythonic Way, Getter, Setter, Using, Read-Only, Summary)
   - Added Exercise 1, 2, and 3 slides with specifications
   - Added full Appendix: Exception Handling section (overview, try/except, else, finally, full try, raise, raise for OOP, NotImplemented vs NotImplementedError)


.. dropdown:: v1.1.0 -- RWA 2 Released (2026-03-01)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: RWA 2: Search and Rescue Mission Planner (new)

   **Assignment Overview**

   - New assignment covering Object-Oriented Programming (Lectures 6 and 7)
   - Two-phase structure: Phase 1 (Design) and Phase 2 (Implementation)
   - Use case: Disaster Response Operation with aerial drones and ground crawlers searching a disaster zone divided into sectors
   - Total: 50 points (Design: 6 pts, Implementation: 44 pts)
   - Due: March 25, 2026

   **Phase 1: Design Document (6 pts)**

   - Deliverable: single UML class diagram in PDF format (``design_document.pdf``)
   - Design phase intentionally lightened to allow students to focus on implementation
   - Sequence diagram removed from requirements to reduce design workload

   **Phase 2: Implementation (44 pts)**

   - 7 classes across 6 modules: ``SensorPayload``, ``Robot`` (abstract), ``AerialDrone``, ``GroundCrawler``, ``Sector``, ``Mission``, ``DisasterZone``
   - OOP concepts exercised: abstraction (``abc.ABC``), encapsulation (``@property``), inheritance (2 subclasses), polymorphism (``search()``/``can_search()`` overrides), composition (Robot owns SensorPayload), aggregation (DisasterZone manages robots/sectors), association (Mission links robot to sector)
   - Dunder methods required: ``__str__``, ``__repr__``, ``__eq__``, ``__lt__``, ``__len__``, ``__contains__``
   - Main program (9 pts) demonstrates polymorphism, sorting, ``__contains__``, and report generation

   **AI Policy**

   - Explicit policy added: AI tools (Copilot, ChatGPT, Claude, etc.) are NOT permitted for code or design
   - Students instructed to disable GitHub Copilot and other AI extensions in VS Code before starting
   - Exception: AI may be used to generate docstring documentation **after** code is written by the student

   **Other Details**

   - Project naming convention: ``firstname_lastname_rwa2/``
   - Suggested 3-week timeline included with day-by-day breakdown
   - All major sections wrapped in ``.. dropdown::`` directives for collapsible navigation
   - Use case separated into subsections using ``.. rubric::`` directives (Robots, Common Robot Characteristics, Sensor Payload, Sectors, Missions, Disaster Zone)


.. dropdown:: v1.0.0 -- Initial Release (2026-01-27)
   :icon: tag
   :class-container: sd-border-success

   Initial release of the ENPM605 Spring 2026 course documentation.

   .. rubric:: Course Structure

   - Lectures 1 through 6 published with lecture notes, exercises, quizzes, glossaries, and references
   - Each lecture organized as a self-contained folder with RST files following a consistent structure

   .. rubric:: RWA 1: Robot Fleet Monitor

   - First assignment covering Lectures 1 through 4 (variables, data types, control flow, functions)
   - 30 points, 6 parts across 5 Python modules
   - Due: February 25, 2026
