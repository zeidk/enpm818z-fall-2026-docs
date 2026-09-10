====================================================
Quiz
====================================================

This quiz covers Lecture 2: the sensor modalities, the numbers that constrain
them, calibration, sensor placement, and the CARLA setup used for GP1. Every
question is answerable from the lecture slides.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to decide whether the statement holds
     as stated in the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-18)
================================

.. admonition:: Question 1
   :class: hint

   According to the complementarity principle, why does a vehicle carry
   several **kinds** of sensor rather than several copies of the best one?

   A. Regulations require at least three sensor types on every AV.

   B. Because the sensors fail in different ways, so their gaps are not the
      same shape.

   C. Because more sensors always produce a more accurate estimate.

   D. Because fusion algorithms require a minimum of three inputs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- because the gaps are not the same shape.

   Two identical forward cameras give protection against one camera dying and
   nothing else, because sun glare blinds both at the same instant. That is
   **redundancy**. Complementarity requires the failure modes to differ.


.. admonition:: Question 2
   :class: hint

   How many **modalities** are eight surround cameras?

   A. Eight

   B. Four

   C. One

   D. It depends on their focal lengths

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- one.

   A modality is a *kind* of sensing, not a piece of hardware. Complementarity
   is a claim about modalities, never about counts. This is why the Tesla
   suite is described as having plenty of redundancy, all of it correlated.


.. admonition:: Question 3
   :class: hint

   A camera runs at 30 Hz. The vehicle is travelling at 30 m/s. Roughly how
   far does the vehicle move between consecutive frames?

   A. 1 cm

   B. 10 cm

   C. 1 m

   D. 10 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- about 1 m.

   :math:`30\ \text{m/s} \div 30\ \text{Hz} = 1\ \text{m}`. This is why
   timestamping and synchronisation are first-class concerns rather than
   details, and it is the same order as the errors produced by a one-degree
   calibration mistake at 100 m.


.. admonition:: Question 4
   :class: hint

   In stereo vision, :math:`z = Bf/d`. Which term is the **measurement**?

   A. :math:`z`, the depth

   B. :math:`B`, the baseline

   C. :math:`f`, the focal length

   D. :math:`d`, the disparity

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- the disparity.

   :math:`B` and :math:`f` are both known from calibration. :math:`z` is what
   you want and never measure directly. :math:`d` is the only quantity the
   sensor actually produces.


.. admonition:: Question 5
   :class: hint

   Stereo depth error grows as :math:`z^2/(Bf)`. Which term can a vehicle
   designer realistically increase to reduce the error at long range?

   A. The focal length, without limit

   B. The baseline, but it is bounded by the width of the car

   C. The disparity

   D. None; the error is fixed by the sensor

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- the baseline, and it is bounded by the width of the car.

   That bound is why stereo is not a LiDAR replacement at long range. With
   :math:`B` = 20 cm and :math:`f` = 1000 px, a tenth of a pixel of disparity
   error is 5 cm at 10 m but **5 m at 100 m**.


.. admonition:: Question 6
   :class: hint

   Why can a single camera not recover **metric** depth, even in principle?

   A. Sensor noise is too high.

   B. Networks are not yet accurate enough.

   C. A small near object and a large far object fill the viewing cone
      identically, so the image is the same image.

   D. The frame rate is too low.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- scale ambiguity is geometric, not a limitation of current
   networks.

   A toy car 10 cm wide at 1 m and a real car 1.8 m wide at 18 m land on the
   same pixels. **No amount of training data recovers a number that was never
   in the image.** Scale must come from elsewhere: camera height, known object
   sizes, ego-motion, or a few RADAR/LiDAR returns.


.. admonition:: Question 7
   :class: hint

   Which failure behaviour is more dangerous, and why?

   A. Stereo, because it returns nothing when it cannot match.

   B. Monocular depth, because it always returns a full, confident map,
      including for objects it has never seen.

   C. They are equally dangerous.

   D. Neither; both raise an exception.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- monocular depth fails *plausibly*.

   This is the lecture's recurring theme: the dangerous failures are the quiet
   ones. A stereo pair that cannot match tells you so; a monocular network
   gives you a confident answer that is wrong.


.. admonition:: Question 8
   :class: hint

   LiDAR range is :math:`r = ct/2`. To achieve ±2 cm of range accuracy, what
   timing precision is required?

   A. 133 microseconds

   B. 133 nanoseconds

   C. 133 picoseconds

   D. 133 femtoseconds

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- 133 picoseconds.

   Two centimetres of range is a four centimetre round trip, and light travels
   about 30 cm per nanosecond. **That number is why LiDAR is expensive.** You
   are paying for the clock, not the laser.


.. admonition:: Question 9
   :class: hint

   What happens to a LiDAR in dense fog?

   A. It goes blind and reports nothing.

   B. It returns the fog: the pulse scatters off droplets and comes back
      early.

   C. It is unaffected, because it brings its own light.

   D. It reports the correct range with a larger variance.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- it returns the fog.

   That is worse than blindness, because you now have **confident measurements
   of nothing**. Note also that a matte black car may absorb the pulse and not
   return at all, and reflectivity is a property of the target, so no amount of
   money fixes it.


.. admonition:: Question 10
   :class: hint

   A 2° RADAR beam is roughly how wide at 100 m?

   A. 0.35 m

   B. 1.0 m

   C. 3.5 m

   D. 35 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- about 3.5 m.

   That is a car and the motorcycle beside it in a single return. RADAR knows
   exactly how fast that blob is closing and very little about its shape:
   excellent radial information, poor cross-range information, which is the
   reverse of the camera.


.. admonition:: Question 11
   :class: hint

   You are driving at 100 km/h and a stationary sign gantry is ahead. Why
   might the RADAR return be discarded?

   A. The gantry produces no echo.

   B. The gantry produces no Doppler shift.

   C. The gantry's Doppler shift exactly matches the road surface and other
      scenery, so by that test it is clutter.

   D. The gantry is outside the RADAR's range.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- its Doppler shift matches the scenery.

   The echo always comes back; metal reflects whether or not it is moving. A
   stationary object *does* produce a Doppler shift when you are moving, set by
   your own speed, which is exactly the shift produced by the road, the signs
   and the bridge. Production stacks discard those returns because reporting
   every manhole cover would brake the car constantly. **A stopped vehicle in
   your lane fails the same test.**


.. admonition:: Question 12
   :class: hint

   Why does an IMU's position error grow without bound?

   A. Its bias is unusually large.

   B. Position comes from integrating acceleration twice, which integrates the
      errors twice as well.

   C. It loses signal in tunnels.

   D. Its sample rate is too low.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- double integration.

   A tiny constant bias becomes a steadily growing speed error and a position
   error that grows faster still. An IMU never measures position; it measures
   acceleration and angular rate. Nothing in the sensor ever tells you how far
   off you are.


.. admonition:: Question 13
   :class: hint

   Which GNSS failure is the **more dangerous** for a fusion filter?

   A. Blocked signal, because the receiver loses the fix.

   B. Multipath, because a normal-looking fix arrives and is several metres
      out.

   C. Both are equally dangerous.

   D. Neither; GNSS is a solved input.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- multipath.

   Blockage is the honest failure: fewer satellites, worse fix or none, and the
   receiver says so. Multipath produces a fix that looks perfectly normal
   because the bounced path is longer, so the receiver places the satellite too
   far away and the car in the wrong place.


.. admonition:: Question 14
   :class: hint

   Which sensor covers the near field below the bumper line, where every
   high-mounted sensor is blind?

   A. Long-range RADAR

   B. Telephoto camera

   C. Ultrasonic

   D. Roof LiDAR

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ultrasonic.

   Range of only 0.2--5 m and useless above walking pace, but it is the
   cheapest sensor on the vehicle and it covers the one volume the expensive
   ones cannot see. A production vehicle typically carries eight to twelve.


.. admonition:: Question 15
   :class: hint

   Which pair of properties describes **intrinsic** calibration?

   A. Belongs to the installation; drifts with vibration and temperature.

   B. Belongs to the camera and lens; comparatively stable, so calibrate once
      and check rarely.

   C. Belongs to the vehicle; must be re-estimated every drive.

   D. Belongs to the LiDAR; supplied by the factory.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Intrinsics travel with the camera and do not change when you move it.
   Extrinsics are the opposite on both counts: they belong to the installation
   and they drift, which is why production stacks monitor and re-estimate them
   online. Intrinsic stability is only *relative*: thermal drift across
   −40 to +85 °C is real.


.. admonition:: Question 16
   :class: hint

   How many independent numbers does a rigid transform :math:`T \in SE(3)`
   contain?

   A. Three

   B. Six

   C. Nine

   D. Twelve

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- six.

   Three for orientation and three for position. The matrix has sixteen
   entries, but :math:`R \in SO(3)` is constrained and the bottom row is
   fixed.


.. admonition:: Question 17
   :class: hint

   You have :math:`T_{V \leftarrow L}` and :math:`T_{V \leftarrow C}` and you
   need camera-from-LiDAR. Which expression is correct?

   A. :math:`T_{V \leftarrow C}\, T_{V \leftarrow L}`

   B. :math:`(T_{V \leftarrow C})^{-1} T_{V \leftarrow L}`

   C. :math:`T_{V \leftarrow L}\, (T_{V \leftarrow C})^{-1}`

   D. :math:`(T_{V \leftarrow L})^{-1} T_{V \leftarrow C}`

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`T_{C \leftarrow L} = T_{C \leftarrow V}\, T_{V \leftarrow L} =
   (T_{V \leftarrow C})^{-1} T_{V \leftarrow L}`. Read it the way you cancel
   fractions: the two :math:`V`\ s meet in the middle and vanish, leaving
   :math:`C \leftarrow L`. If they do not meet, it is written backwards, and
   you know that before running any code.


.. admonition:: Question 18
   :class: hint

   You project LiDAR points into a CARLA camera image and omit the axis
   permutation :math:`P`. What happens?

   A. Python raises a dimension mismatch.

   B. CARLA rejects the transform.

   C. Nothing raises, and the points land somewhere wrong.

   D. The points land correctly; :math:`P` is optional.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- nothing raises.

   :math:`K` assumes the optical convention (*x* right, *y* down, *z* forward
   along the optical axis); CARLA uses *x* forward, *y* right, *z* up. The
   same three physical directions under different names. Omitting :math:`P`
   entirely throws the points off the image; getting **one sign** of
   :math:`P` wrong is worse, because the points land, the shape is
   recognisable, and the scene is upside down.


----


True or False (Questions 19-28)
===============================

.. admonition:: Question 19
   :class: hint

   Calibration decides whether a LiDAR cluster and a camera bounding box are
   the same object.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Calibration tells you which pixel a LiDAR point lands on. Deciding that the
   cluster and the box are the same object is **data association**; merging
   them into one estimate is **fusion**. Both are L3. Calibration makes the
   question askable; it does not answer it.


.. admonition:: Question 20
   :class: hint

   A LiDAR point cloud is an ordered image-like grid with known connectivity
   between neighbouring points.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   It is an unordered set of :math:`(x, y, z)` returns with intensity and **no
   connectivity**. Nothing in the data says which points belong to the same
   object. Vertical resolution also decays with range, so the far field is far
   sparser than it looks in renderings.


.. admonition:: Question 21
   :class: hint

   Two identical cameras mounted side by side provide complementary sensing.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   They provide **competitive** (redundant) sensing, and only against component
   failure. They share every environmental failure mode: sun, fog, mud, spray.
   Ask of every redundant pair, *what single event takes them both?*


.. admonition:: Question 22
   :class: hint

   One degree of extrinsic rotation error produces about 1.75 m of lateral
   error at 100 m.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   :math:`r\theta = 100 \times (1^\circ \text{ in radians}) \approx 1.75` m,
   about the width of a car. At 10 m it is 17 cm, which looks like noise on a
   bench. **The error only becomes visible at exactly the range where you
   cannot easily verify it.**


.. admonition:: Question 23
   :class: hint

   In CARLA, ``vehicle.bounding_box.extent`` gives the full length, width and
   height of the vehicle.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.** It is the **half**-size in metres.

   The roof is near ``2*extent.z`` and the bumper near ``extent.x``. Treating
   it as a full size mounts the camera inside the bodywork, which returns a
   perfectly valid image of upholstery.


.. admonition:: Question 24
   :class: hint

   ``AttachmentType.SpringArm`` is the correct attachment for a sensor whose
   extrinsic calibration you intend to use.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.** Use ``AttachmentType.Rigid``, always.

   ``SpringArm`` *smooths* the sensor's motion for video, so the
   sensor-to-vehicle transform stops being constant, and every extrinsic in
   the calibration section assumed it was constant. SpringArm is right for a
   viewer camera and wrong for a sensor.


.. admonition:: Question 25
   :class: hint

   CARLA models LiDAR attenuation in rain and fog, so degraded-weather results
   from CARLA transfer directly to a real vehicle.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   In the Demo 4 measurements the LiDAR return count holds near 11,500 per
   sweep across **all six** weather presets. Attenuation is a fixed blueprint
   attribute that the weather never touches. Weather sits in the "modelled
   roughly, or not at all" band, so a degraded-weather claim from CARLA
   numbers alone is not a result.


.. admonition:: Question 26
   :class: hint

   Dense fog makes the camera image darker than at clear noon.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**, and this is the interesting one.

   In the measured table, fog gives the **brightest** frame of the six (about
   162, against 128 at clear noon) and one of the flattest. The image is not
   dark, it is **uniform**, and a detector needs edges rather than photons.
   Night is the opposite failure: brightness collapses to about 47.


.. admonition:: Question 27
   :class: hint

   An HD map is a sensor.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.** It is a **prior**: information you already hold before you
   measure anything.

   Nothing about it is live, but it enters the stack where a sensor does and
   brings its own failure mode. A stop line moved two metres makes the prior
   wrong, and **a confidently wrong prior is worse than none at all**.


.. admonition:: Question 28
   :class: hint

   In synchronous mode the client must call ``world.tick()`` to advance the
   simulation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Set ``synchronous_mode=True`` with a ``fixed_delta_seconds`` and drive the
   clock yourself. Every run then becomes reproducible and every timestamp
   exact. Do it before writing anything else: retrofitting it means
   re-checking every callback you have already written.


----


Short Answer (Questions 29-34)
==============================

.. admonition:: Question 29
   :class: hint

   A fire truck is stopped across your lane on a clear, dry motorway and you
   are closing at 110 km/h. Which sensors see it, which may miss it, and why?

.. dropdown:: Answer
   :class-container: sd-border-success

   **RADAR sees it and may discard it.** The truck is stationary, so its
   Doppler shift matches the road and scenery, and the zero-Doppler clutter
   filter throws the return away.

   **LiDAR sees it plainly**, because a laser does not care whether the target
   is moving. **The camera sees it** if the contrast holds.

   This is the strongest single argument against a RADAR-only forward channel,
   and it is implicated in real crashes into stopped and parked emergency
   vehicles.


.. admonition:: Question 30
   :class: hint

   Explain why the camera and RADAR are described as complementary, using
   angular resolution and classification.

.. dropdown:: Answer
   :class-container: sd-border-success

   RADAR has excellent radial information (range and, uniquely, direct
   velocity from Doppler) and poor cross-range information: 1--10° of angular
   resolution means a car and a motorcycle merge into one return at 100 m. It
   also cannot classify at all.

   The camera is the reverse: excellent angular resolution and the **only**
   sensor that classifies or reads text, but poor at range and defeated by
   darkness, glare and weather.

   Each one's monopoly is precisely the other's weakness, which is what
   complementary means.


.. admonition:: Question 31
   :class: hint

   Your LiDAR-to-camera extrinsic is wrong by one degree. Why would this pass
   a bench check and fail on the road?

.. dropdown:: Answer
   :class-container: sd-border-success

   The lateral error is :math:`r\theta`, so it scales with range: about 9 cm
   at 5 m, which looks like ordinary noise on a bench, but 1.75 m at 100 m,
   which is a whole car width.

   Object association therefore breaks somewhere between 50 and 100 m, where
   the error exceeds the object being matched. Past that point fusion does not
   degrade gracefully; it starts **confidently pairing the wrong things**,
   which is worse than not fusing at all.

   This is why calibration is validated with quantitative reprojection metrics
   over the full range, not by eye on a checkerboard at arm's length.


.. admonition:: Question 32
   :class: hint

   Why is the LiDAR coverage in the plan-view figure drawn as a **ring**
   rather than a disc, and what follows from that?

.. dropdown:: Answer
   :class-container: sd-border-success

   The beams leave the roof at a limited downward angle, so the ground
   immediately beside the vehicle is never struck. That near-field hole is
   real geometry, not a drawing convention.

   What follows is the blind spot just ahead of the bumper: it lies inside the
   LiDAR's hole **and** outside both front corner RADARs, which are turned
   outward for cross-traffic. Ultrasonics and a wide near camera exist to
   close it.


.. admonition:: Question 33
   :class: hint

   You have $5,000 per vehicle. Sketch a suite for a **highway** ODD and a
   suite for an **urban** ODD, and state what changes and why.

.. dropdown:: Answer
   :class-container: sd-border-success

   **Highway** buys range and weather: long-range RADAR (~$2,000), telephoto
   camera (~$1,500), forward solid-state LiDAR (~$1,000) for the
   stationary-object cover RADAR cannot give, plus ~$500 of basic side
   sensing. 360° coverage is sacrificed, which is defensible in a lane-keeping
   ODD.

   **Urban** buys coverage: four corner RADARs (~$2,000) for genuine 360°, a
   surround camera set (~$1,500) for classification and occlusion recovery,
   ~$500 forward ADAS module for low-speed AEB. **LiDAR is cut entirely**: at
   50 km/h you need to see all around you far more than you need 200 m of
   range.

   **The point is the inversion.** Same money, opposite suite. A design that
   serves both has not used the ODD.


.. admonition:: Question 34
   :class: hint

   The lecture claims that the dangerous sensor failures are the quiet ones.
   Support that claim with at least four examples from different parts of the
   lecture.

.. dropdown:: Answer
   :class-container: sd-border-success

   Any four of:

   - **Sun glare or fog** on a camera: a valid image, with the contrast gone.
   - **Fog on a LiDAR**: it returns the fog, so you get confident measurements
     of nothing.
   - **Zero-Doppler filtering**: a stopped vehicle is discarded as scenery, and
     no fault is raised.
   - **GNSS multipath**: a normal-looking fix that is several metres out.
   - **A one-degree extrinsic error**: plausible projections that are wrong,
     and only at range.
   - **A millisecond of clock skew**: correct data, combined at the wrong
     instant.
   - **A blocked lens**: a perfectly valid, perfectly useless image.
   - **Monocular depth**: a full, confident map, including for objects never
     seen.

   Not one of these raises an exception. That is why health monitoring,
   blockage detection and cross-validation are not optional extras, and why
   the fusion filter in L3 must be able to decide what to believe.
