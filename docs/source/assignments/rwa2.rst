====================================================
RWA 2: Search and Rescue Mission Planner
====================================================


Overview
========

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Due Date**
     - March 23, 2026, 11:59 PM EST
   * - **Total Points**
     - 50 points (Design: 6 pts, Implementation: 44 pts)
   * - **Submission**
     - Canvas (ZIP file: ``firstname_lastname_rwa2.zip`` containing the project folder)
   * - **Collaboration**
     - Individual work only. AI tools are NOT permitted (see policy below).
   * - **Late Policy**
     - 10% deduction per calendar day, up to 3 days. Zero after 3 days.


.. dropdown:: Description
   :open:

   You are tasked with building a **Search and Rescue Mission Planner**, a Python program that models a disaster response operation. The system coordinates heterogeneous robots (aerial drones and ground crawlers) to search a disaster zone composed of sectors with varying hazard levels and terrain types. Each robot carries a sensor payload, has operational constraints (battery, altitude limits, terrain restrictions), and must be assigned to compatible sectors.

   This assignment has two phases:

   - **Phase 1 (Design):** Analyze the use case below and produce a single UML class diagram (PDF).
   - **Phase 2 (Implementation):** Translate your design into working Python code that demonstrates abstraction, encapsulation, inheritance, polymorphism, composition, aggregation, and association.

   This assignment tests your understanding of Object-Oriented Programming (Lectures 6 and 7).

   .. note::

      **Lightened design phase.** We have intentionally reduced the design deliverable to a single UML class diagram so that you can focus the majority of your time on implementation. A well-drawn class diagram is the most valuable design artifact: it forces you to think through attributes, methods, types, and relationships before writing code.


.. dropdown:: AI and Academic Integrity Policy
   :open:

   .. danger::

      **AI tools are NOT permitted for any part of this assignment.** This includes but is not limited to: ChatGPT, GitHub Copilot, Claude, Gemini, Cursor, Amazon CodeWhisperer, Tabnine, and any other AI-powered code generation or completion tool.

      **Before starting this assignment:**

      - **Disable GitHub Copilot** in VS Code: go to the Extensions panel, find GitHub Copilot, and click Disable.
      - **Disable any other AI extensions** (Tabnine, Amazon CodeWhisperer, Cursor AI, etc.).
      - **Do not use AI chatbots** to generate code, docstrings, class structures, or UML diagrams.

      You may use AI tools to generate **docstring documentation** for your classes and methods only **after** you have written the code yourself. The code, logic, and design must be entirely your own work.

      You may reference the lecture slides, the L6 Design Phase PDF, official Python documentation, and your own class notes. Violations will result in a zero on the assignment and will be reported to the Office of Student Conduct.


.. dropdown:: Use Case: Disaster Response Operation
   :open:

   Read the following domain description carefully. You will use it to build your class diagram and then implement the system.


   .. rubric:: Robots

   A regional **disaster response agency** coordinates search and rescue operations after natural disasters. The agency deploys a fleet of heterogeneous **robots** to search a **disaster zone**. Each disaster zone is divided into multiple **sectors** that must be systematically searched.

   The agency operates two types of robots:

   - **Aerial drones** fly over sectors to perform wide-area surveillance. Each drone has a maximum altitude (in meters) and cannot operate in sectors where the required search altitude exceeds its limit. Drones consume battery at a rate of 5% per search operation. When a drone searches a sector, it performs an aerial sweep and reports the percentage of the sector area it was able to cover.

   - **Ground crawlers** traverse terrain on wheels or tracks. Each crawler has a maximum speed (in m/s) and a set of terrain types it can handle (e.g., "rubble", "mud", "pavement"). A crawler cannot be assigned to a sector if the sector's terrain type is not in the crawler's capability list. Crawlers consume battery at a rate of 8% per search operation. When a crawler searches a sector, it performs a ground sweep and reports the number of survivors located.


   .. rubric:: Common Robot Characteristics

   All robots share the following characteristics:

   - Every robot has a **name** (string), a **battery level** (integer, 0 to 100), and an **operational status** (one of: "standby", "active", "low_battery", "offline").
   - A robot's battery level must always be between 0 and 100 inclusive. Setting it outside this range is an error.
   - A robot cannot perform a search if its status is not "active".
   - When a robot's battery drops below 20%, its status automatically changes to "low_battery".
   - When a robot's battery reaches 0%, its status automatically changes to "offline".
   - A robot can be recharged, which sets its battery to 100% and its status to "standby".
   - Every robot carries a **sensor payload** that it owns. The sensor payload is created when the robot is created and cannot exist independently. If the robot is destroyed, so is its payload.


   .. rubric:: Sensor Payload

   A **sensor payload** represents the suite of instruments a robot carries. Every payload has a **weight** (in kg, must be positive) and a list of **instrument names** (e.g., ["thermal camera", "lidar"]). The payload provides a method to check whether it contains a specific instrument.


   .. rubric:: Sectors

   A **sector** represents a region of the disaster zone that must be searched. Each sector has:

   - A **sector ID** (string, e.g., "S-01")
   - A **terrain type** (string, e.g., "urban", "forest", "flood", "rubble")
   - A **hazard level** (integer, 1 to 5, where 5 is the most dangerous)
   - A **search difficulty** value (float, 1.0 to 10.0, representing how hard the sector is to search)
   - A flag indicating whether the sector has been **searched** (initially False)
   - Sectors with terrain "urban" or "forest" have a **required search altitude** (float, in meters) for aerial operations. Other sectors have this set to ``None``.

   A sector cannot be assigned to a robot if the sector has already been searched. A sector's hazard level must be between 1 and 5 inclusive.


   .. rubric:: Missions

   A **mission** represents a single assignment of a robot to a sector. Each mission records:

   - The **robot** assigned (association: neither the mission nor the robot owns the other)
   - The **sector** being searched (association: neither the mission nor the sector owns the other)
   - The **mission status** (one of: "pending", "in_progress", "completed", "failed")
   - A **result** string (initially empty, populated when the mission completes)

   When a mission is executed:

   1. The robot's status must be "active"; otherwise the mission fails immediately.
   2. The robot must be compatible with the sector (``robot.can_search(sector)``); otherwise the mission fails.
   3. The sector must not have been searched already; otherwise the mission fails.
   4. The mission status changes to "in_progress".
   5. The robot performs the search (``robot.search(sector)``), which drains battery and produces a result.
   6. If the robot's battery dropped below 20% during the search, the mission fails.
   7. Otherwise, the sector is marked as searched, the result is recorded, and the mission is completed.


   .. rubric:: Disaster Zone

   The **disaster zone** manages the overall operation. It maintains:

   - A collection of **sectors** (aggregation: the zone manages sectors, but sectors could exist independently).
   - A collection of **robots** (aggregation: the zone manages robots, but robots could exist independently).

   The disaster zone provides methods to add robots and sectors, query available robots and unsearched sectors, and generate a status report.
   
.. dropdown:: Learning Objectives
   :open:

   By completing this assignment, you will strengthen and demonstrate the following skills:

   .. grid:: 1 2 2 2
       :gutter: 2

       .. grid-item-card:: OOP Design Process
           :class-card: sd-border-info

           Practice the design workflow: analyze a domain description and produce a UML class diagram showing structure, types, and relationships.

       .. grid-item-card:: Abstraction and Encapsulation
           :class-card: sd-border-info

           Define clean public interfaces using abstract methods and ``@property`` decorators. Protect internal state with non-public attributes and validated setters.

       .. grid-item-card:: Inheritance and Polymorphism
           :class-card: sd-border-info

           Build a class hierarchy where specialized robot types inherit from a common base class. Override methods so that each type searches differently while sharing the same interface.

       .. grid-item-card:: Composition, Aggregation, and Association
           :class-card: sd-border-info

           Model real-world relationships: a robot *owns* its sensor payload (composition), a disaster zone *manages* robots and sectors (aggregation), and a mission *links* a robot to a sector (association).

       .. grid-item-card:: Dunder Methods and Operator Overloading
           :class-card: sd-border-info

           Implement ``__str__``, ``__repr__``, ``__eq__``, ``__lt__``, ``__len__``, and ``__contains__`` to integrate your classes with Python's built-in operations.

       .. grid-item-card:: Code Quality and Documentation
           :class-card: sd-border-info

           Write professional code with type hints, Google-style docstrings, consistent naming, and linting compliance.


.. dropdown:: Suggested Timeline
   :open:

   This assignment is designed to be completed over 3 weeks. The following timeline is a suggestion to help you pace your work.

   .. list-table::
      :widths: 18 12 70
      :header-rows: 1
      :class: compact-table

      * - Period
        - Duration
        - Tasks
      * - **Week 1**
        - Days 1--3
        - Read the use case carefully. Draw the UML class diagram on paper or using a tool. Identify all classes, attributes, methods, relationships, and multiplicity. Finalize ``design_document.pdf``.
      * - **Week 1--2**
        - Days 4--7
        - Implement and test ``SensorPayload`` and ``Sector`` (the two simplest classes with no dependencies on other custom classes). Write tests in each module's ``if __name__ == "__main__"`` block.
      * - **Week 2**
        - Days 8--12
        - Implement and test the ``Robot`` abstract base class and the two subclasses (``AerialDrone``, ``GroundCrawler``). This is the most complex part. Focus on property validation, automatic status triggers, and the polymorphic ``search()`` and ``can_search()`` methods.
      * - **Week 2--3**
        - Days 13--16
        - Implement and test ``Mission`` (focus on the 7-step ``execute()`` logic) and ``DisasterZone`` (aggregation, query methods, report generation).
      * - **Week 3**
        - Days 17--19
        - Implement ``main.py``. Wire everything together and demonstrate all OOP concepts (polymorphism, sorting, ``__contains__``, report).
      * - **Week 3**
        - Days 20--21
        - Code quality pass: add/review docstrings, type hints, and inline comments. Test the full program end to end. Package and submit.

   .. tip::

      Do not leave the ``Robot`` hierarchy for the last week. It is the most complex part and will take the most debugging time. Start it no later than Day 8.


.. dropdown:: Project Structure
   :open:

   Your submission must follow the directory structure shown below. Replace ``firstname_lastname`` with your actual name in lowercase (e.g., ``john_doe_rwa2``).

   .. code-block:: text

      firstname_lastname_rwa2/
      |-- design_document.pdf     # Phase 1: UML class diagram
      |-- sensor_payload.py       # SensorPayload class
      |-- robot.py                # Robot base class, AerialDrone, GroundCrawler
      |-- sector.py               # Sector class
      |-- mission.py              # Mission class
      |-- disaster_zone.py        # DisasterZone class
      |-- main.py                 # Main program (entry point)


   .. list-table::
      :widths: 22 78
      :header-rows: 1
      :class: compact-table

      * - File
        - Description
      * - ``design_document.pdf``
        - Phase 1 deliverable: UML class diagram.
      * - ``sensor_payload.py``
        - ``SensorPayload`` class (composition target, owned by ``Robot``).
      * - ``robot.py``
        - ``Robot`` abstract base class, ``AerialDrone`` subclass, ``GroundCrawler`` subclass.
      * - ``sector.py``
        - ``Sector`` class representing a region of the disaster zone.
      * - ``mission.py``
        - ``Mission`` class linking a robot to a sector (association).
      * - ``disaster_zone.py``
        - ``DisasterZone`` class managing robots and sectors (aggregation).
      * - ``main.py``
        - Entry point. Creates entities, runs missions, demonstrates all OOP concepts.


----


Phase 1: Design Document (6 pts)
==================================


.. dropdown:: UML Class Diagram (6 pts)
   :open:

   Using the use case description above, produce a **single UML class diagram** and submit it as a **PDF file** named ``design_document.pdf``. Place it inside your project folder alongside the Python files.

   You may use any tool: `PlantUML <https://plantuml.com/>`_, `Mermaid <https://mermaid.js.org/>`_, `draw.io <https://app.diagrams.net/>`_, `Lucidchart <https://www.lucidchart.com/>`_, or hand-drawn and scanned.

   The class diagram must include:

   - **All 7 classes**: ``Robot`` (abstract), ``AerialDrone``, ``GroundCrawler``, ``SensorPayload``, ``Sector``, ``Mission``, ``DisasterZone``
   - **For each class**: attributes (with types and visibility: ``+`` public, ``-`` private/non-public) and methods (with parameter types and return types)
   - ``Robot`` must be marked as abstract (italicized name or ``<<abstract>>`` stereotype), and ``search()`` and ``can_search()`` must be marked as abstract methods
   - **All relationships** with correct UML notation:

     - **Inheritance**: ``AerialDrone`` and ``GroundCrawler`` extend ``Robot`` (solid line with hollow arrowhead)
     - **Composition**: ``Robot`` owns ``SensorPayload`` (solid line with filled diamond on the ``Robot`` side)
     - **Aggregation**: ``DisasterZone`` manages ``Robot`` and ``Sector`` collections (solid line with hollow diamond on the ``DisasterZone`` side)
     - **Association**: ``Mission`` references ``Robot`` and ``Sector`` (solid line with open arrow)

   - **Multiplicity labels** on all relationship lines (e.g., ``1`` to ``1``, ``1`` to ``*``)

   .. important::

      The class diagram must be detailed enough that another developer could implement the system from the diagram alone.


----


Phase 2: Implementation (44 pts)
=================================


.. dropdown:: Part 1: SensorPayload Class (3 pts)
   :open:

   **Module:** ``sensor_payload.py``

   Implement the ``SensorPayload`` class. This class represents the instrument suite a robot carries. It is a component owned by a robot (composition: the payload cannot exist independently of its robot).

   **Requirements:**

   - ``__init__(self, weight: float, instruments: list[str])``

     - ``_weight``: non-public, validated via property (must be positive, raise ``ValueError`` otherwise)
     - ``_instruments``: non-public, a list of instrument name strings

   - **Properties:**

     - ``weight`` (read-only): returns the payload weight
     - ``instruments`` (read-only): returns the list of instruments

   - **Dunder methods:**

     - ``__str__``: returns ``"Payload(<weight>kg, <n> instruments)"`` where ``<n>`` is the number of instruments
     - ``__repr__``: returns ``"SensorPayload(<weight>, <instruments>)"``
     - ``__contains__``: allows ``"lidar" in payload`` syntax to check if an instrument is present

   - **Example:**

     .. code-block:: python

        payload = SensorPayload(2.5, ["thermal camera", "lidar"])
        print(payload)                    # Payload(2.5kg, 2 instruments)
        print("lidar" in payload)         # True
        print("sonar" in payload)         # False


.. dropdown:: Part 2: Robot Base Class and Subclasses (16 pts)
   :open:

   **Module:** ``robot.py``

   Implement the ``Robot`` abstract base class and two concrete subclasses: ``AerialDrone`` and ``GroundCrawler``.


   **Robot (Abstract Base Class) -- 10 pts**

   - ``__init__(self, name: str, battery: int, payload: SensorPayload)``

     - ``_name``: non-public (read-only property)
     - ``_battery``: non-public, validated via property (0 to 100 inclusive, raise ``ValueError`` otherwise)
     - ``_status``: non-public, initialized to ``"standby"``
     - ``_payload``: non-public (composition: the robot owns this payload)

   - **Properties:**

     - ``name`` (read-only)
     - ``battery`` (getter and setter): setter validates range and triggers automatic status changes:

       - If battery drops below 20, set status to ``"low_battery"``
       - If battery reaches 0, set status to ``"offline"``

     - ``status`` (getter and setter): setter validates that the value is one of ``"standby"``, ``"active"``, ``"low_battery"``, ``"offline"`` (raise ``ValueError`` otherwise)
     - ``payload`` (read-only): returns the ``SensorPayload`` object

   - **Methods:**

     - ``activate(self) -> None``: sets status to ``"active"`` if battery >= 20, otherwise raises ``RuntimeError``
     - ``recharge(self) -> None``: sets battery to 100 and status to ``"standby"``
     - ``search(self, sector: Sector) -> str``: **abstract method** (use ``abc.abstractmethod``). Each subclass implements this differently. Returns a result string.
     - ``can_search(self, sector: Sector) -> bool``: **abstract method**. Returns whether this robot is compatible with the given sector.

   - **Dunder methods:**

     - ``__str__``: returns ``"<n> [<status>] (Battery: <battery>%)"``
     - ``__repr__``: returns ``"<ClassName>('<n>', <battery>)"``
     - ``__eq__``: two robots are equal if they have the same name
     - ``__lt__``: compares robots by battery level (enables sorting)

   .. important::

      ``Robot`` must inherit from ``abc.ABC`` and declare ``search`` and ``can_search`` as abstract methods. Attempting to instantiate ``Robot`` directly must raise ``TypeError``.


   **AerialDrone -- 3 pts**

   - ``__init__(self, name: str, battery: int, payload: SensorPayload, max_altitude: float)``

     - ``_max_altitude``: non-public (read-only property, must be positive)

   - **Overrides:**

     - ``can_search(self, sector)``: returns ``True`` if the sector has a ``required_altitude`` that is not ``None`` and ``required_altitude <= max_altitude``. Returns ``False`` otherwise.
     - ``search(self, sector)``: drains battery by **5%**, performs an aerial sweep, and returns ``"Aerial sweep of <sector_id>: covered <X>% of area"`` where ``<X>`` is computed as ``max(10, int(100 - sector.search_difficulty * 8))``.


   **GroundCrawler -- 3 pts**

   - ``__init__(self, name: str, battery: int, payload: SensorPayload, max_speed: float, terrain_capabilities: list[str])``

     - ``_max_speed``: non-public (read-only property, must be positive)
     - ``_terrain_capabilities``: non-public (read-only property)

   - **Overrides:**

     - ``can_search(self, sector)``: returns ``True`` if the sector's terrain type is in the crawler's ``terrain_capabilities``.
     - ``search(self, sector)``: drains battery by **8%**, performs a ground sweep, and returns ``"Ground sweep of <sector_id>: located <N> survivors"`` where ``<N>`` is computed as ``max(0, int(10 - sector.search_difficulty * 1.5))``.


.. dropdown:: Part 3: Sector Class (4 pts)
   :open:

   **Module:** ``sector.py``

   Implement the ``Sector`` class.

   **Requirements:**

   - ``__init__(self, sector_id: str, terrain_type: str, hazard_level: int, search_difficulty: float, required_altitude: float | None = None)``

     - ``_sector_id``: non-public (read-only property)
     - ``_terrain_type``: non-public (read-only property)
     - ``_hazard_level``: non-public, validated via property (1 to 5 inclusive, raise ``ValueError``)
     - ``_search_difficulty``: non-public, validated via property (1.0 to 10.0, raise ``ValueError``)
     - ``_searched``: non-public, initialized to ``False``
     - ``_required_altitude``: non-public (read-only property, can be ``None``)

   - **Properties:** ``sector_id``, ``terrain_type``, ``hazard_level``, ``search_difficulty``, ``searched`` (getter and setter), ``required_altitude``

   - **Dunder methods:**

     - ``__str__``: returns ``"Sector <sector_id> (<terrain_type>, hazard=<hazard_level>)"``
     - ``__repr__``: returns ``"Sector('<sector_id>', '<terrain_type>', <hazard_level>, <search_difficulty>)"``
     - ``__eq__``: two sectors are equal if they have the same ``sector_id``


.. dropdown:: Part 4: Mission Class (6 pts)
   :open:

   **Module:** ``mission.py``

   Implement the ``Mission`` class. A mission links a robot to a sector (association: the mission references both but owns neither).

   **Requirements:**

   - ``__init__(self, robot: Robot, sector: Sector)``

     - ``_robot``: non-public (read-only property)
     - ``_sector``: non-public (read-only property)
     - ``_status``: non-public, initialized to ``"pending"``
     - ``_result``: non-public, initialized to ``""``

   - **Properties:** ``robot``, ``sector``, ``status`` (read-only), ``result`` (read-only)

   - **Methods:**

     - ``execute(self) -> bool``:

       1. If the robot's status is not ``"active"``, set mission status to ``"failed"``, set result to ``"Robot not active"``, and return ``False``.
       2. If the robot cannot search the sector (``robot.can_search(sector)`` returns ``False``), set mission status to ``"failed"``, set result to ``"Robot incompatible with sector"``, and return ``False``.
       3. If the sector has already been searched, set mission status to ``"failed"``, set result to ``"Sector already searched"``, and return ``False``.
       4. Set mission status to ``"in_progress"``.
       5. Call ``robot.search(sector)`` to perform the search (this drains battery and returns a result string).
       6. If the robot's status changed to ``"low_battery"`` or ``"offline"`` during the search, set mission status to ``"failed"``, set result to ``"Robot battery depleted during mission"``, and return ``False``.
       7. Otherwise, mark the sector as searched, set mission status to ``"completed"``, store the result string from the search, and return ``True``.

   - **Dunder methods:**

     - ``__str__``: returns ``"Mission: <robot_name> -> <sector_id> [<status>]"``
     - ``__repr__``: returns ``"Mission(<robot_repr>, <sector_repr>)"``


.. dropdown:: Part 5: DisasterZone Class (6 pts)
   :open:

   **Module:** ``disaster_zone.py``

   Implement the ``DisasterZone`` class. This class manages the overall operation using aggregation (it holds references to robots and sectors but does not own them).

   **Requirements:**

   - ``__init__(self, name: str)``

     - ``_name``: non-public (read-only property)
     - ``_robots``: non-public, initialized to an empty list
     - ``_sectors``: non-public, initialized to an empty list
     - ``_missions``: non-public, initialized to an empty list

   - **Properties:** ``name`` (read-only)

   - **Methods:**

     - ``add_robot(self, robot: Robot) -> None``: adds a robot to the zone. Raise ``ValueError`` if a robot with the same name already exists.
     - ``add_sector(self, sector: Sector) -> None``: adds a sector to the zone. Raise ``ValueError`` if a sector with the same ID already exists.
     - ``get_available_robots(self) -> list[Robot]``: returns robots with status ``"active"`` or ``"standby"``.
     - ``get_unsearched_sectors(self) -> list[Sector]``: returns sectors where ``searched`` is ``False``.
     - ``create_mission(self, robot: Robot, sector: Sector) -> Mission``: creates a ``Mission`` object, appends it to ``_missions``, and returns it.
     - ``generate_report(self) -> str``: returns a formatted multi-line string summarizing the operation (see format below).

   - **Dunder methods:**

     - ``__len__``: returns the total number of robots in the zone
     - ``__contains__``: allows ``"robot_name" in zone`` syntax to check if a robot with that name is in the zone
     - ``__str__``: returns ``"DisasterZone '<n>': <r> robots, <s> sectors"``

   - **Report format:**

     .. code-block:: text

        ========================================
        DISASTER ZONE: <n>
        ========================================
        Robots     : <total_robots>
        Available  : <available_count>
        Sectors    : <total_sectors>
        Searched   : <searched_count>
        Unsearched : <unsearched_count>
        ----------------------------------------
        MISSION LOG
        ----------------------------------------
        [<status>] <robot_name> -> <sector_id>: <r>
        [<status>] <robot_name> -> <sector_id>: <r>
        ...
        ========================================

     If there are no missions, print ``No missions executed.`` in the mission log section.


.. dropdown:: Part 6: Main Program (9 pts)
   :open:

   **Module:** ``main.py``

   Create a ``main()`` function that demonstrates all OOP concepts. Call it from an ``if __name__ == "__main__"`` guard. All program logic must live inside ``main()``.

   The ``main()`` function must:

   1. Create a ``DisasterZone`` with a descriptive name (e.g., ``"Hurricane Delta Response"``).
   2. Create **at least 4 sectors** with a mix of terrain types. At least 2 should have a ``required_altitude`` value (for aerial drones) and at least 2 should have terrain types suitable for ground crawlers. Use different hazard levels and search difficulties.
   3. Create **at least 3 robots**: at least 1 ``AerialDrone`` and at least 1 ``GroundCrawler``. Give each a ``SensorPayload`` with different instruments and weights.
   4. Add all sectors and robots to the disaster zone.
   5. Activate all robots.
   6. Create and execute **at least 4 missions**, including:

      - At least one **successful** aerial drone mission
      - At least one **successful** ground crawler mission
      - At least one **failed** mission (e.g., incompatible robot/sector pairing)

   7. **Demonstrate polymorphism:** iterate over a list containing both drones and crawlers and call ``search()`` on each with an appropriate sector, printing the results to show that different robot types produce different output.
   8. **Demonstrate sorting:** sort robots by battery level using ``sorted()`` (enabled by ``__lt__``) and print the sorted list.
   9. **Demonstrate** ``__contains__``: use the ``in`` keyword to check if a robot name is in the disaster zone and if an instrument is in a payload. Print the results.
   10. Print the disaster zone report using ``generate_report()``.

   .. dropdown:: Example Output (Partial)
       :class-container: sd-border-info

       The following shows the kind of output your program should produce. Your exact values will differ based on the entities you create.

       .. code-block:: text

          === Activating Robots ===
          SkyEye-1 [active] (Battery: 100%)
          TrackBot [active] (Battery: 100%)
          SkyEye-2 [active] (Battery: 100%)

          === Executing Missions ===
          Mission: SkyEye-1 -> S-01 [completed]
          Mission: TrackBot -> S-03 [completed]
          Mission: SkyEye-2 -> S-04 [failed]
          Mission: TrackBot -> S-02 [completed]

          === Polymorphism Demo ===
          SkyEye-1: Aerial sweep of S-02: covered 52% of area
          TrackBot: Ground sweep of S-04: located 5 survivors

          === Sorting by Battery ===
          TrackBot [active] (Battery: 84%)
          SkyEye-1 [active] (Battery: 90%)
          SkyEye-2 [active] (Battery: 95%)

          === Contains Demo ===
          "SkyEye-1" in zone: True
          "MegaBot" in zone: False
          "lidar" in SkyEye-1 payload: True

          ========================================
          DISASTER ZONE: Hurricane Delta Response
          ========================================
          Robots     : 3
          Available  : 3
          Sectors    : 4
          Searched   : 3
          Unsearched : 1
          ----------------------------------------
          MISSION LOG
          ----------------------------------------
          [completed] SkyEye-1 -> S-01: Aerial sweep of S-01: covered 68% of area
          [completed] TrackBot -> S-03: Ground sweep of S-03: located 5 survivors
          [failed] SkyEye-2 -> S-04: Robot incompatible with sector
          [completed] TrackBot -> S-02: Ground sweep of S-02: located 7 survivors
          ========================================




Grading, Submission, and Policies
==================================

.. dropdown:: Grading Rubric
   :open:

   .. list-table::
      :widths: 35 8 57
      :header-rows: 1
      :class: compact-table

      * - Component
        - Points
        - Criteria
      * - **Phase 1: Design Document**
        - **6**
        -
      * - UML Class Diagram
        - 6
        - All 7 classes present with attributes, methods, types, and visibility (2 pts). Abstract class and abstract methods correctly notated (1 pt). All relationships with correct UML notation: composition, aggregation, association, inheritance (2 pts). Multiplicity labels on all relationship lines (1 pt).
      * - **Phase 2: Implementation**
        - **44**
        -
      * - Part 1: SensorPayload
        - 3
        - Correct attributes with validation (1 pt). ``__contains__`` works correctly (1 pt). ``__str__`` and ``__repr__`` (1 pt).
      * - Part 2: Robot Hierarchy
        - 16
        - Abstract base class with ``abc.ABC`` and abstract methods (2 pts). Properties with validation and automatic status triggers (4 pts). Two subclasses with correct ``can_search`` logic (3 pts). Two subclasses with correct ``search`` implementation and drain rates (3 pts). ``activate()`` and ``recharge()`` (2 pts). Dunder methods: ``__str__``, ``__repr__``, ``__eq__``, ``__lt__`` (2 pts).
      * - Part 3: Sector
        - 4
        - Correct attributes with validation (2 pts). Optional ``required_altitude`` handled correctly (1 pt). Dunder methods (1 pt).
      * - Part 4: Mission
        - 6
        - ``execute()`` follows the 7-step logic correctly (4 pts). Handles all failure cases (1 pt). Dunder methods (1 pt).
      * - Part 5: DisasterZone
        - 6
        - Add methods with duplicate checks (1 pt). Query methods for available robots and unsearched sectors (1 pt). ``generate_report()`` with correct format (2 pts). ``__len__``, ``__contains__``, ``__str__`` (2 pts).
      * - Part 6: Main Program
        - 9
        - Creates required entities and adds to zone (1 pt). Executes 4+ missions including at least one failure (2 pts). Demonstrates polymorphism with a loop over mixed robot types (2 pts). Demonstrates sorting by battery and ``__contains__`` (2 pts). Prints disaster zone report (2 pts).
      * - **TOTAL**
        - **50**
        -


.. dropdown:: Code Quality Requirements
   :open:

   .. warning::

      The following are mandatory and will result in point deductions if missing.

   - **Docstrings:** Every class and every method must have a Google-style docstring with a description, ``Args`` section (where applicable), and ``Returns`` section (where applicable).
   - **Type hints:** All method parameters and return types must have type annotations.
   - **Inline comments:** Include comments that explain non-obvious logic (e.g., drain rate calculations, compatibility checks, status transitions).
   - **Naming conventions:** Use ``snake_case`` for all method and variable names. Use ``CamelCase`` for class names.
   - **No global variables:** All data should be passed through constructors, method parameters, and return values.
   - **Linting:** Ensure Ruff is enabled in VS Code and that no linting errors or warnings appear.

   .. admonition:: Deductions
      :class: caution

      Missing docstrings (-1 pt per class/method, up to -5 pts). Missing type hints (-0.5 pt per method, up to -3 pts). Poor or missing comments (-1 pt). Naming violations (-1 pt). Linting errors (-1 pt).


----


.. dropdown:: Pre-Submission Checklist
   :open:


   **Functionality**

   - ☐ The program runs without errors: ``python3 main.py``
   - ☐ ``Robot`` cannot be instantiated directly (``abc.ABC`` enforced).
   - ☐ Both robot types correctly implement ``search()`` and ``can_search()``.
   - ☐ Properties validate input and raise appropriate exceptions on invalid data.
   - ☐ Battery setter triggers automatic status changes at the correct thresholds.
   - ☐ ``Mission.execute()`` handles all success and failure cases per the 7-step specification.
   - ☐ ``DisasterZone`` correctly manages robots and sectors with duplicate checks.
   - ☐ The report format matches the specified layout.
   - ☐ Polymorphism is demonstrated: a loop over mixed robot types calls ``search()`` with different behavior.


   **Design Document**

   - ☐ ``design_document.pdf`` is present in the project folder.
   - ☐ UML class diagram includes all 7 classes with attributes, methods, types, visibility, relationships, and multiplicity.
   - ☐ ``Robot`` is marked as abstract with abstract methods clearly indicated.
   - ☐ Composition, aggregation, association, and inheritance use correct UML notation.


   **Code Quality**

   - ☐ **Type hints:** Every method parameter and return type has a type annotation.
   - ☐ **Docstrings:** Every class and method has a Google-style docstring.
   - ☐ **Naming:** Classes use ``CamelCase``, methods and variables use ``snake_case``.
   - ☐ **No global variables:** All data is managed through classes, constructors, and methods.
   - ☐ **Imports:** Each module uses explicit named imports. No wildcard imports.


   **Linting**

   - ☐ Ruff is enabled in VS Code and no linting errors or warnings appear in any Python file.


   **File Headers**

   - ☐ Every Python file includes a comment block at the top with your name, UID, and module description.

   .. code-block:: python

      # Name: <Your Name>
      # UID: <Your UID>
      # Module: robot.py - Robot abstract base class and subclasses


   **Packaging**

   - ☐ Removed ``__pycache__/``, ``.pyc``, and ``.ruff_cache/`` before zipping.
   - ☐ ZIP file is named ``firstname_lastname_rwa2.zip`` (e.g., ``john_doe_rwa2.zip``).
   - ☐ ZIP contains only the ``firstname_lastname_rwa2/`` folder with the six ``.py`` files and ``design_document.pdf``.
   - ☐ Verified ZIP contents with ``unzip -l``.

   .. code-block:: bash

      cd firstname_lastname_rwa2/
      rm -rf __pycache__/ *.pyc .ruff_cache/
      cd ..
      zip -r firstname_lastname_rwa2.zip firstname_lastname_rwa2/

   Verify your ZIP has the correct structure:

   .. code-block:: bash

      unzip -l firstname_lastname_rwa2.zip

   You should see the six ``.py`` files and ``design_document.pdf`` inside the ``firstname_lastname_rwa2/`` folder. No ``__pycache__/``, ``.pyc``, or ``.ruff_cache/`` files should be present.


----


.. dropdown:: Hints

   .. tip::

      - **Start with the class diagram.** Drawing it first forces you to think through attributes, methods, and relationships before writing any code.
      - **Implement and test bottom-up:** ``SensorPayload`` first, then ``Sector``, then ``Robot`` and its subclasses, then ``Mission``, and finally ``DisasterZone``.
      - Use Python's ``abc`` module: ``from abc import ABC, abstractmethod``.
      - To make ``Robot`` abstract, inherit from ``ABC`` and decorate ``search()`` and ``can_search()`` with ``@abstractmethod``.
      - The ``__contains__`` dunder method lets you use the ``in`` keyword: ``def __contains__(self, item): ...``
      - The ``__lt__`` dunder method enables ``sorted()`` to work on your objects without a ``key`` function.
      - Test each class independently before integrating. Create a small test in each module's ``if __name__ == "__main__"`` block.
      - For UML notation, refer to the Design Phase PDF from L6 as a model.
      - You may draw diagrams by hand and scan them, or use tools like `PlantUML <https://plantuml.com/>`_, `Mermaid <https://mermaid.js.org/>`_, `draw.io <https://app.diagrams.net/>`_, or `Lucidchart <https://www.lucidchart.com/>`_.


----


.. dropdown:: Submission

   - Submit a ZIP file named ``firstname_lastname_rwa2.zip`` on Canvas (e.g., ``john_doe_rwa2.zip``).
   - The ZIP must contain a single folder named ``firstname_lastname_rwa2/`` with exactly six Python files (``sensor_payload.py``, ``robot.py``, ``sector.py``, ``mission.py``, ``disaster_zone.py``, ``main.py``) and the design document (``design_document.pdf``).
   - The ZIP must not contain ``__pycache__/``, ``.pyc`` files, ``.ruff_cache/``, or any other build artifacts.
   - The program should run without errors when executed with ``python3 main.py`` from inside the project directory.
   - Do not submit Jupyter notebooks, extra files, or nested ZIP archives.
   - Ensure your name and UID are in a comment at the top of every Python file.
