====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas. They exist so you can check your own
   understanding before **Quiz 1 (Week 4)** and before the **Week 3 setup
   milestone**, which *is* graded.

   Each exercise ends with a box giving the reasoning. Work the exercise
   first, then open it. Bring anything that does not resolve to office hours
   or to the start of L2.

Six exercises: four conceptual, two hands-on in CARLA.


.. dropdown:: Exercise 1 -- Classify These Systems
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Classify driving automation features by SAE J3016 level from behavior and
   operating limits alone.

   .. raw:: html

      <hr>

   **Specification**

   For each system below, give the **SAE level** and **the one fact in the
   description that decided it**. Company names are removed on purpose:
   classify the behavior and the operating limits, not the brand.

   .. list-table::
      :widths: 6 94
      :header-rows: 1
      :class: compact-table

      * -
        - System description
      * - **A**
        - Consumer sedan. Steers and controls speed on any marked road, city
          streets included. The driver must watch the road, and an interior
          camera checks that they are. No geofence. Marketed as
          "self-driving".
      * - **B**
        - Luxury sedan. Hands off and eyes off, but only on pre-mapped divided
          highways, below 60 km/h, in daylight, in dense traffic, never in
          rain. Outside those limits it asks the driver to take over within
          ten seconds. The manufacturer accepts liability while it is engaged.
      * - **C**
        - No steering wheel, no pedals. Runs with nobody on board responsible
          for driving, inside a mapped metropolitan area. When it gets stuck
          it stops, and a remote operator advises, but never takes the
          controls.
      * - **D**
        - Sidewalk delivery pod, 25 km/h, geofenced to a campus, no occupants.
          One remote operator watches about ten of them and can take the
          controls of any.
      * - **E**
        - Class 8 truck on a fixed highway corridor. The system steers, sets
          speed and changes lanes for the whole route. A safety driver sits in
          the seat throughout and must monitor and intervene.

   .. dropdown:: Answers and reasoning
      :icon: check-circle
      :class-container: sd-border-success

      - **A is Level 2.** The human monitors, so the human is responsible.
        Driving on city streets does not raise the level, and neither does the
        marketing name.
      - **B is Level 3.** Eyes off, inside a very narrow set of limits, with
        the human as the fallback when asked. The tell is **the manufacturer
        accepting liability**.
      - **C is Level 4.** The system handles its own fallback. A remote
        operator who only advises is not driving.
      - **D is also Level 4, but it is not the same as C.** C's operator
        *advises*, which J3016 calls **remote assistance**. D's operator can
        *take the controls*, which is **remote driving**. That is a separate
        mode, not the fallback, so the level does not change. But "a human
        watching a screen" is not one single thing.
      - **E is the trap, and it is Level 2.** The system does everything. A
        human is still required to monitor and intervene, so the human holds
        the driving task. **Same software, two different levels, depending
        only on what is asked of the person in the seat.**


.. dropdown:: Exercise 2 -- Write an ODD, Then Break It
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Experience the trade-off that a claimed ODD creates between ease of
   approval and usefulness of the product.

   .. raw:: html

      <hr>

   **Specification**

   Write an ODD for an **L4 shuttle** operating between three buildings on the
   University of Maryland campus. Cover each category:

   1. **Road types** -- which roads, lanes and intersections are included?
   2. **Speed range** -- minimum and maximum operating speed.
   3. **Weather** -- enumerate acceptable conditions (light rain: yes;
      snow > 2 in: no).
   4. **Time of day** -- daytime only, or also nighttime?
   5. **Traffic participants** -- vehicles, pedestrians, cyclists, scooters.
   6. **Connectivity** -- V2X, cellular, or standalone?
   7. **Fallback behavior** -- what happens when an ODD boundary is reached?

   Then, the part that matters:

   8. Write **three scenarios that are inside your ODD as written but that you
      did not intend to allow.**
   9. Tighten the ODD to exclude them, and **note what the product lost.**

   .. dropdown:: What you should notice
      :icon: check-circle
      :class-container: sd-border-success

      Every tightening makes approval easier (**Stage 6**) and the product
      less useful. That tension drives a great deal of behavior in this
      industry, and you have just felt it from the developer's side.

      Steps 8 and 9 are the ones that map onto the real failure mode. A vague
      ODD in **Stage 2** produces a weak scenario library in **Stage 4**, and
      **nobody outside the company is in the room to say so until Stage 5.**
      There is no correct answer here; there is only a documented one.


.. dropdown:: Exercise 3 -- Choose a Minimal Risk Condition
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice treating the MRC as a design artifact with stated assumptions,
   rather than as an obviously safe default.

   .. raw:: html

      <hr>

   **Specification**

   For each situation, choose an MRC from the candidate list in the lecture
   notes, then state **the assumption it makes** and **the sensing that would
   verify that assumption**.

   1. A Level 4 robotaxi loses its primary LiDAR mid-block on a two-lane city
      street.
   2. A Level 3 highway pilot reaches the end of its mapped corridor and the
      driver does not respond to the request to intervene.
   3. A driverless shuttle detects a flat tire while crossing a railway level
      crossing.
   4. A robotaxi's compute stack reboots while stopped at a red light with
      passengers aboard.

   .. dropdown:: What you should notice
      :icon: check-circle
      :class-container: sd-border-success

      At least one of these has **no safe answer** from the candidate list --
      case 3, where stopping is lethal and moving may be impossible. That is
      the point. **An MRC list that always has an answer is a list that has
      not been stress-tested.**

      Notice also that case 2 is **not a fault at all**: nothing broke, the
      vehicle simply reached the edge of its ODD, and it still needs a
      complete handover. Most fallbacks in service are of that kind.


.. dropdown:: Exercise 4 -- Diagnose a Failure at the System Level
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Practice the sixth learning outcome: deciding whether a hazard is a
   malfunction (ISO 26262) or occurs with no malfunction (ISO 21448 / SOTIF),
   and what follows for testing.

   .. raw:: html

      <hr>

   **Specification**

   Take this description: *a vehicle brakes hard for a shadow cast across the
   road by an overpass, and is rear-ended.*

   1. Which module produced the wrong output?
   2. Is this an **ISO 26262** hazard (something malfunctioned) or an
      **ISO 21448 / SOTIF** hazard (everything worked as designed)?
   3. Which stage of the seven-stage pipeline should have caught it, and what
      artifact from that stage would have contained it?
   4. Would fixing the module in your answer to (1) **alone** have prevented
      the outcome?

   .. dropdown:: What you should notice
      :icon: check-circle
      :class-container: sd-border-success

      **Nothing malfunctioned.** The perception stack correctly reported a
      dark region and the planner correctly braked for what it was told was an
      obstacle. That makes it **SOTIF**.

      The artifact that should have contained it is the list of **triggering
      conditions** produced by the SOTIF analysis in **Stage 2**, which
      becomes the test library in **Stage 4**.

      And **no** -- fixing the shadow classifier alone leaves the general class
      of false-positive hard braking untouched. This is the same shape of
      answer as both case studies in the lecture.


.. dropdown:: Exercise 5 -- Explore CARLA Maps
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Get comfortable with the CARLA Python client by querying the simulator for
   map and waypoint information. **This also verifies that your Week 3 setup
   milestone environment actually works.**

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

   .. dropdown:: If it fails
      :icon: check-circle
      :class-container: sd-border-success

      The overwhelmingly common cause is a **client/server version
      mismatch**, or connecting before the server has finished loading the
      level. Check ``pip3 show carla`` against your server version, and wait
      30--60 seconds after starting the server. **A timeout usually means the
      server is not up yet, not that your code is wrong.**


.. dropdown:: Exercise 6 -- Weather and Perception
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Observe how weather affects camera image quality, and reason about what
   that implies for a perception stack and for fusion.

   .. raw:: html

      <hr>

   **Specification**

   Create the file ``weather_experiment.py`` that performs the following:

   1. Spawn an ego vehicle with an **RGB camera** (800 × 600, FOV 90°) in
      Town03.
   2. For each weather preset below, set the weather, wait 2 seconds for the
      scene to stabilize, and **save one snapshot** to disk:

      - ``carla.WeatherParameters.ClearNoon``
      - ``carla.WeatherParameters.HardRainNoon``
      - ``carla.WeatherParameters.ClearSunset``
      - ``carla.WeatherParameters.SoftFogNoon``

   3. Clean up all actors before exiting.

   **Written analysis** (for yourself -- 3--4 sentences per condition):

   - Can you clearly see lane markings?
   - Are distant objects (> 50 m) visible?
   - Are there reflections or glare that would affect a detector?
   - Which condition is **most challenging** for a camera-only system, and
     why?

   .. dropdown:: What you should notice
      :icon: check-circle
      :class-container: sd-border-success

      Glare at sunset is usually worse for a detector than heavy rain, and it
      is the cleanest illustration of a **SOTIF** hazard you can produce in an
      afternoon: the camera is not broken, the sun is simply in the wrong
      place. Nothing about that failure is fixed by redundancy in the same
      sensor.

      If you add a LiDAR and repeat the experiment, watch the **return count**
      in fog and rain. Then ask the question that GP3 will force you to answer
      properly: **what should your fusion stage do when two sensors
      disagree?**
