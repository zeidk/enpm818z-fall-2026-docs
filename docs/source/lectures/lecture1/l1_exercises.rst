====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 1. Exercises mix conceptual analysis with hands-on CARLA
exploration.


.. dropdown:: Exercise 1 -- SAE Level Classification
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice classifying real-world driving systems using the SAE J3016
   taxonomy by identifying who performs the DDT, who monitors the
   environment, and who provides the fallback.


   .. raw:: html

      <hr>


   **Specification**

   For each system below, determine the **SAE level** (0--5). In the
   *Justification* column, state (a) who monitors the driving
   environment, and (b) who is the DDT fallback.

   .. list-table::
      :widths: 45 15 40
      :header-rows: 1
      :class: compact-table

      * - System
        - Level
        - Justification
      * - Tesla Autopilot (lane centering + adaptive cruise control)
        -
        -
      * - Mercedes DRIVE PILOT on a German Autobahn at < 60 km/h
        -
        -
      * - Waymo One robotaxi in Phoenix, AZ (no safety driver)
        -
        -
      * - A human driving a 2024 Corolla with ABS and ESC only
        -
        -
      * - Baidu Apollo Go in Wuhan with a remote safety operator
        -
        -

   **Deliverable**

   A completed copy of the table above with clear, one-sentence
   justifications for each row.


.. dropdown:: Exercise 2 -- ODD Specification
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice writing an Operational Design Domain (ODD) document for a
   hypothetical Level 4 autonomous campus shuttle.


   .. raw:: html

      <hr>


   **Specification**

   Write an ODD specification for an L4 shuttle operating between three
   buildings on the University of Maryland campus. Your document must
   address each of the following seven categories:

   1. **Road types** -- which roads, lanes, and intersections are
      included?
   2. **Speed range** -- minimum and maximum operating speed.
   3. **Weather conditions** -- enumerate acceptable conditions (e.g.,
      light rain: yes, snow > 2 in: no).
   4. **Time of day** -- daytime only, or also nighttime?
   5. **Traffic participants** -- types of road users the system must
      handle (vehicles, pedestrians, cyclists, scooters, etc.).
   6. **Connectivity requirements** -- V2X, cellular, or standalone?
   7. **Fallback behavior** -- what happens when an ODD boundary is
      reached (e.g., weather worsens)?

   **Deliverable**

   A one-page ODD document (plain text, Markdown, or PDF) with a clear
   entry for each category.


.. dropdown:: Exercise 3 -- Explore CARLA Maps
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Get comfortable with the CARLA Python client by querying the
   simulator for map and waypoint information.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``explore_maps.py`` that performs the following:

   1. Connect to a running CARLA server on ``localhost:2000``.
   2. Print all **available maps** (``client.get_available_maps()``).
   3. Load **Town03** and retrieve the map object.
   4. Generate waypoints at **2.0 m** spacing and print the total count.
   5. Count how many waypoints are at **junctions**
      (``waypoint.is_junction``).
   6. Print all **unique road IDs** present in the map.

   **Expected output**

   .. code-block:: text

      Available maps: ['/Game/Carla/Maps/Town01', '/Game/Carla/Maps/Town03', ...]
      Loaded: Town03
      Total waypoints (2.0 m spacing): 5832
      Junction waypoints: 743
      Unique road IDs: {0, 1, 2, 5, 7, ...}

   (Exact numbers will vary by CARLA version.)

   **Verification**

   .. code-block:: console

      python3 explore_maps.py    # all 6 items printed without errors


.. dropdown:: Exercise 4 -- Weather and Perception
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Observe how different weather conditions affect camera image quality
   and reason about the implications for perception.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``weather_experiment.py`` that performs the following:

   1. Spawn an ego vehicle with an **RGB camera** (800 × 600, FOV 90°)
      in Town03.
   2. For each of the following weather presets, set the weather, wait
      2 seconds for the scene to stabilize, and **save one snapshot**
      to disk:

      - ``carla.WeatherParameters.ClearNoon``
      - ``carla.WeatherParameters.HardRainNoon``
      - ``carla.WeatherParameters.ClearSunset``
      - ``carla.WeatherParameters.SoftFogNoon``

   3. Clean up all actors before exiting.

   **Written analysis**

   For each saved image, answer the following in a short write-up
   (3--4 sentences per condition):

   - Can you clearly see lane markings?
   - Are distant objects (> 50 m) visible?
   - Are there reflections or glare that would affect a detector?
   - Which condition is **most challenging** for a camera-only system
     and why?

   **Deliverable**

   Four saved images (``clear_noon.png``, ``hard_rain.png``,
   ``sunset.png``, ``fog.png``) and a short written analysis.


.. dropdown:: Exercise 5 -- Case Study Analysis
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Analyze a real-world AV incident to connect lecture concepts
   (perception, planning, safety) to engineering failures.


   .. raw:: html

      <hr>


   **Specification**

   Read the NTSB report summary for the **Uber ATG fatality
   (Tempe, AZ -- March 2018)** and answer the following questions:

   1. What object classifications did the perception system cycle
      between in the seconds before impact?
   2. How many seconds of reaction time would a human driver have
      needed to avoid the collision, according to the report?
   3. Name **two design decisions** in the ADS that contributed to the
      outcome.
   4. Propose **one architectural change** that could have mitigated
      the failure. Reference a concept from Lecture 1 (e.g.,
      redundancy, MRC, functional safety).

   **Deliverable**

   A written document (one to two pages) with numbered answers and
   references to specific findings in the NTSB report.
