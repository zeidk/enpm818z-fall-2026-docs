====================================================
Exercises
====================================================

Six take-home exercises built on the Lecture 2 slides. Exercises 1--3 are
paper and arithmetic. Exercises 4--5 need CARLA running. Exercise 6 is a
design argument.

.. important::

   **What comes with a script and what does not.**

   Exercise 4 is ``demo2_spawn_suite.py`` from Demo 2, in
   `enpm818z-fall-2026-carla-python
   <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python>`_. Read it
   and modify it.

   **Exercise 5 has no starter script, deliberately.** It is the core of GP1,
   and the axis permutation only teaches you something if you get it wrong
   yourself first. Everything you need is in the lecture notes.


.. dropdown:: Exercise 1 -- Which Sensor Would Have Seen It?
   :icon: eye
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Reason about failure modes in terms of physics rather than brand.

   .. raw:: html

      <hr>

   **Specification**

   For each scene, state which modality sees it, which misses it, and **why**.
   One or two sentences each.

   .. list-table::
      :widths: 6 94
      :header-rows: 1

      * -
        - **Scene**
      * - A
        - A ladder has fallen from a truck and lies flat across your lane on a
          dry motorway. You are closing at 110 km/h.
      * - B
        - A cyclist with no lights, wearing dark clothing, crossing an unlit
          junction.
      * - C
        - A car emerging from a side road hidden behind a parked van, in
          daylight.
      * - D
        - A variable message sign reading *queue ahead*, in fog.
      * - E
        - Your vehicle is stopped at a red light in a multi-storey car park
          when a pedestrian steps in front of the bumper.

   .. raw:: html

      <hr>

   **Deliverable**

   A short table: scene, sensors that see it, sensors that miss it, physical
   reason. Then name the scene you found hardest and say why.

   .. dropdown:: Guidance
      :color: success

      - **A** is the zero-Doppler case with an extra twist: a flat ladder also
        has a small radar cross-section and a low profile, so it is a poor
        LiDAR target too. Camera classification is the realistic answer, and
        it is not a confident one.
      - **B** is Tempe in sensor terms. No ambient light nearly blinds the
        camera; dark non-reflective clothing is the LiDAR's worst target.
      - **C** is about **occlusion**, not sensing: no modality sees through the
        van. The answer is coverage and overlap, and slowing down.
      - **D** is camera-only for the text, and fog is exactly when the camera
        loses contrast. Compare with the fog measurements in the notes: the
        image gets *brighter* and flatter.
      - **E** is the near field below the bumper line, plus the third row of
        the zero-Doppler table: you are stopped and the pedestrian is barely
        moving, so nothing stands out. Ultrasonics and a wide near camera.


.. dropdown:: Exercise 2 -- Depth Arithmetic
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Show for yourself why stereo is not a LiDAR replacement at range, and why
   monocular scale must come from outside the image.

   .. raw:: html

      <hr>

   **Specification**

   1. A stereo pair has :math:`B` = 20 cm and :math:`f` = 1000 px. Using
      :math:`z = Bf/d`, complete the table for a disparity error of 0.1 px.

      .. list-table::
         :widths: 25 25 25 25
         :header-rows: 1

         * - **Range**
           - **Disparity (px)**
           - **Depth error (m)**
           - **Comparable to**
         * - 10 m
           -
           -
           -
         * - 50 m
           -
           -
           -
         * - 100 m
           -
           -
           -
         * - 200 m
           -
           -
           -

   2. You are asked to halve the depth error at 100 m. Evaluate each option
      and say which is available on a passenger car: double :math:`B`, double
      :math:`f`, halve the disparity error.

   3. A monocular network reports 18 m for an object. State two independent
      pieces of information that could fix the scale, and one road condition
      that breaks the most commonly used one.

   .. raw:: html

      <hr>

   **Deliverable**

   The completed table, a short paragraph on part 2, and three sentences on
   part 3.

   .. dropdown:: Guidance
      :color: success

      Part 1: disparity is 20, 4, 2 and 1 px; depth error is about 0.05, 1.25,
      5.0 and 20 m. Error grows as :math:`z^2/(Bf)`.

      Part 2: doubling :math:`B` is bounded by the width of the car. Doubling
      :math:`f` narrows the field of view, so you lose the periphery and
      typically need another camera. Halving the disparity error is a matching
      and calibration problem and is the least controllable.

      Part 3: camera height above a flat road, known object sizes, ego-motion
      from wheels or IMU, or a few RADAR/LiDAR returns. Production stacks lean
      hardest on camera height, which is why a monocular stack degrades on a
      crest, a dip or a banked road.


.. dropdown:: Exercise 3 -- Calibration Error Budget
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Put numbers on the two calibration errors that are invisible on a bench.

   .. raw:: html

      <hr>

   **Specification**

   1. **Angle.** Your LiDAR-to-camera extrinsic rotation is wrong by
      :math:`\theta`. Lateral error is :math:`r\theta`. Complete the table.

      .. list-table::
         :widths: 20 26 26 28
         :header-rows: 1

         * - **Range**
           - :math:`\theta = 1.0^\circ`
           - :math:`\theta = 0.1^\circ`
           - **Comparable to (1.0°)**
         * - 10 m
           -
           -
           -
         * - 50 m
           -
           -
           -
         * - 100 m
           -
           -
           -
         * - 200 m
           -
           -
           -

   2. At which range does the 1.0° error first exceed the width of a car
      (1.8 m)? What does that mean for **object association**?

   3. **Time.** Complete the distance travelled during a synchronisation error
      of 33 ms, 10 ms and 1 ms, at 50 km/h and at 110 km/h. Then repeat for
      two vehicles approaching head-on at 110 km/h each.

   4. A production acceptance threshold is rotation error below about 0.1°.
      Using your own numbers, argue that this is a requirement rather than
      perfectionism.

   .. raw:: html

      <hr>

   **Deliverable**

   Both completed tables and a short written argument for part 4.

   .. dropdown:: Guidance
      :color: success

      Part 1 at 1.0°: 0.17 m, 0.87 m, 1.75 m, 3.49 m. At 0.1°: 1.7 cm, 8.7 cm,
      17 cm, 35 cm.

      Part 2: between 50 and 100 m. Past that the camera box and the LiDAR
      cluster no longer overlap, so association does not merely degrade, it
      starts **confidently pairing the wrong things**, which is worse than not
      fusing at all.

      Part 3: 33 ms is 0.46 m at 50 km/h and 1.01 m at 110 km/h. Head-on, the
      closing rate is about 61 m/s, so 10 ms is 0.61 m of range error.

      Part 4: at 100 m, 0.1° is 17 cm, about a third of a car width. The whole
      downstream stack inherits that tolerance.


.. dropdown:: Exercise 4 -- Spawn and Re-Place a Sensor Suite (CARLA)
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Confirm for yourself that a sensor's attachment transform **is** its
   extrinsic calibration, and that mounting numbers must be derived rather
   than copied.

   .. raw:: html

      <hr>

   **Setup**

   .. code-block:: bash

      # server running and answering on localhost:2000
      python3 demo2_spawn_suite.py --seconds 60

   .. raw:: html

      <hr>

   **Specification**

   1. Run it unmodified and record the delivered rate of each of the five
      streams. Compare each against the rate configured on the blueprint and
      explain any difference.
   2. Print ``vehicle.bounding_box.extent`` for **three** different vehicle
      blueprints. Show that the roof height is near ``2*extent.z`` and the
      front bumper near ``extent.x``, and state what happens if you treat
      ``extent`` as a full size.
   3. Move the camera 0.5 m **backwards** and re-run. The image changes; the
      published extrinsic changes too. Explain in one sentence why a
      downstream consumer that was not told about the change now produces
      wrong results without any error being raised.
   4. Change the LiDAR from 32 to 16 channels. Report the mean points per
      sweep before and after, and describe what happens to the point cloud
      **far** from the vehicle specifically.
   5. Re-attach one sensor with ``AttachmentType.SpringArmGhost`` instead of
      ``Rigid``. Describe what this does to the sensor-to-vehicle transform,
      and why that invalidates everything in the calibration section.

   .. raw:: html

      <hr>

   **Deliverable**

   A short report with the rate table, the three extents, and one paragraph
   for each of parts 3, 4 and 5.


.. dropdown:: Exercise 5 -- Project LiDAR into the Camera Image (no starter script)
   :icon: alert
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   **Goal**

   Execute the whole calibration section once. **This is the core of GP1.**

   .. raw:: html

      <hr>

   **Specification**

   Starting from your Exercise 4 script, capture one frame in which the camera
   image and the LiDAR sweep come from the **same tick**, and overlay the
   LiDAR points on the image, coloured by depth.

   You need, in this order:

   .. math::

      p_{img} \sim K\, P\, T_{C \leftarrow V}\, T_{V \leftarrow L}\, p_L

   1. Get :math:`T_{V \leftarrow L}` and :math:`T_{V \leftarrow C}` from the
      mounting transforms you passed in. Form :math:`T_{C \leftarrow L}` and
      **write down the chain before you code it**, checking that the inner
      frames cancel.
   2. Build :math:`K` from the camera blueprint's ``image_size_x`` and ``fov``.
   3. Derive :math:`P` **from your own convention**. Do not copy it from the
      notes: state which axis of the optical frame corresponds to which axis
      of the body frame, and get the signs from that.
   4. Keep only points in front of the camera, apply the perspective division,
      and discard points outside the image.
   5. Colour by depth and save the overlay.

   Then, deliberately:

   6. Run it again **without** :math:`P`. Record how many points land on the
      image.
   7. Run it again with **one sign of** :math:`P` **wrong**. Record how many
      points land, and look at the result.

   .. raw:: html

      <hr>

   **Deliverable**

   Three images (correct, no permutation, one sign wrong), the point counts
   for each, and a paragraph answering: **which of the two wrong versions is
   more dangerous in a real system, and why?**

   .. dropdown:: What to expect
      :color: warning

      Synchronising the two streams matters. In synchronous mode each sensor
      produces one message per tick, so a queue per sensor and one ``get()``
      per ``world.tick()`` pairs them exactly. Free-running callbacks let a
      loaded machine attribute a frame to the wrong tick.

      Omitting :math:`P` entirely throws essentially **every** point off the
      image, so you get a blank overlay. Getting **one sign** wrong keeps the
      same number of points on the image, in a recognisable shape, in the
      wrong place. Nothing raises in either case.

      The second is the dangerous one, and that is the answer the deliverable
      is asking for.


.. dropdown:: Exercise 6 -- Spend the Budget
   :icon: law
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Turn the physics into a defensible design under a constraint.

   .. raw:: html

      <hr>

   **Specification**

   You have **$5,000 per vehicle** for the entire sensor suite. Choose **one**
   ODD:

   - **A -- Highway.** Divided motorway only, 60--130 km/h, all weather
     including rain and light snow, day and night, driver supervising.
   - **B -- Urban.** City streets below 50 km/h, dense pedestrians and
     cyclists, frequent occlusion, parked cars either side, fair weather and
     daylight only.

   Produce:

   1. A bill of materials with approximate costs summing to $5,000 or less.
   2. A coverage argument: which requirement each item satisfies (360°, range
      diversity, forward redundancy, neighbour overlap).
   3. **What you cut**, and which capability you lost with it.
   4. For every redundant pair in your suite, name the **single event** that
      takes them both.
   5. One failure your suite does **not** cover, and what you would tell the
      safety case about it.

   .. raw:: html

      <hr>

   **Deliverable**

   Two pages maximum. Part 5 carries the most credit.

   .. dropdown:: Guidance
      :color: success

      The strongest answers show the **inversion**: a highway suite spends on
      range and weather, an urban suite spends on coverage, and the same money
      produces opposite designs. A suite that serves both ODDs has not used
      the ODD.

      A common weak answer buys one of everything and calls it redundant. Ask
      what happens when the single forward camera is blinded.

      For part 5, the answer being looked for has the shape: *"we do not cover
      heavy snow, so the ODD excludes it, and the system must detect snow and
      hand back."* That is L1 and L2 used together.
