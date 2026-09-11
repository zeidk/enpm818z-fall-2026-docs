====================================================
Lecture
====================================================

.. note::

   These notes accompany the L2 slide deck (v1.0) and carry more detail than
   the slides do. Where the two disagree, these notes are the authoritative
   version.

.. important::

   **Fusion is not in this lecture.** Today is what each sensor measures, what
   it cannot, and how to place and calibrate sensors so that combining them is
   possible at all. The filter that combines them is
   :doc:`L3 <../lecture3/l3_index>`.

   You should not be able to fuse anything after today. You should be able to
   place sensors so that fusion is possible.

.. important::

   Installing CARLA is **not** covered in lecture. It is setup-guide material
   (:doc:`Ubuntu 22.04 </carla/ubuntu22>`,
   :doc:`Ubuntu 24.04 </carla/ubuntu24>`), and having it running is the Week 3
   setup milestone.


Introduction
------------

Two Problems
~~~~~~~~~~~~

Perception, prediction, planning and control all take sensor output as their
input. An object the sensors never reported cannot be tracked, cannot be
predicted, and cannot be avoided. **The sensor suite bounds what the finished
system can do**, however good the software above it is.

Two problems follow, and the second is the one most students do not expect.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Problem 1 -- Sensors
      :class-header: bg-primary text-white

      Different kinds of sensor fail in different ways. A camera classifies
      but measures range poorly. LiDAR measures range precisely but cannot
      read a sign. RADAR keeps working in weather that defeats both.

      That is the argument for mixing modalities rather than fitting more
      copies of the best one.

   .. grid-item-card:: Problem 2 -- Calibration
      :class-header: bg-warning

      Fusing two sensors assumes you know **where** each one sits and **when**
      each one measured. Get either wrong and they report the same object
      twice, in two places.

      The error scales with range: one degree of extrinsic error is
      **1.75 m at 100 m**, about the width of a car.

.. admonition:: The standing counterexample
   :class: important

   Tesla runs roughly eight surround cameras and no LiDAR or radar in the
   perception stack. There is plenty of redundancy there, but all of it is
   correlated. Whether that is sufficient is an open question, and it is
   revisited in :ref:`l2-tesla-case`.


Learning Objectives
~~~~~~~~~~~~~~~~~~~

By the end of tonight you should be able to:

- Given a sensor suite, state what it measures, what it does not, how each
  part degrades, and whether its calibration still holds at the range you
  actually care about.
- Place and calibrate sensors so that fusing them is possible.


Closing the Loop
~~~~~~~~~~~~~~~~

Lecture 1 defined the dynamic driving task, the ODD and the six SAE levels,
and ended on two failures that both began in perception.

- **Tempe was not one broken component.** It was an object detected early,
  classified unstably, never tracked, and therefore never acted on.
- Before you can fuse anything, the sensors must agree on where they are
  looking. That is calibration, and it is most of this lecture.
- **GP1 is built on tonight**, but it is not posted until **Week 3**, after
  L3. What is due in Week 3 is the **setup milestone**: CARLA running, ROS 2
  workspace built, sensors publishing. That milestone is individual and
  pass/fail.

.. tip::

   **Why the lecture opens in the simulator.** The sensor offsets hard-coded
   in the CARLA demo are exactly what the calibration section is about, so
   you will have seen the problem before you are given the theory.


CARLA
-----

Why Simulate
~~~~~~~~~~~~

CARLA (Car Learning to Act) is an open-source automated driving simulator
built on Unreal Engine, developed at the Computer Vision Center of the
Autonomous University of Barcelona.

- Lecture 1 ended on two incidents whose common feature was **a scenario
  nobody had enumerated**. Simulation is how scenarios get enumerated.
- Demonstrating safety on public roads alone is impractical. Simulation is
  the only way to accumulate the exposure.
- You can produce a pedestrian crossing at night in heavy rain a thousand
  times, with ground truth, and nobody is harmed.
- **Perfect labels are free**, which is what makes GP2 possible at all.

.. seealso::

   Read :doc:`Simulation for Automated Driving </preread/simulation>` after
   tonight and before GP1.


What CARLA Gives You
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: table-hover

   * - **Area**
     - **What is provided**
   * - Sensors
     - RGB, depth and semantic cameras, LiDAR, RADAR, IMU, GNSS with noise
       models, collision and lane-invasion detectors
   * - Environments
     - Multiple towns covering residential, urban and highway; dynamic
       weather; day and night
   * - Traffic
     - Pedestrians, cyclists and vehicles with behaviour models, driven by
       the Traffic Manager
   * - Interfaces
     - A Python API, and ROS 2 connectivity

.. important::

   The **depth** and **semantic segmentation** cameras are *ground truth*,
   not hardware. No vehicle carries either. Use them to check your work,
   never to depend on.

This course uses **CARLA 0.9.16**. Client and server versions must match
exactly. Native on Ubuntu 22.04, Docker on Ubuntu 24.04; both are documented
in the :doc:`setup guides </carla/carla>`.


Client-Server Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 18 82
   :header-rows: 1

   * - **Component**
     - **Role**
   * - Server
     - Runs the simulation. It is a game engine, and it will use your GPU.
   * - Client
     - Your Python scripts, connecting over TCP. The server can run on a
       different machine, or in a container.
   * - Bridge
     - Publishes CARLA sensor data onto ROS 2 topics and turns ROS 2 control
       messages back into CARLA actor commands.

**Vocabulary to learn tonight:** *world* (the simulated environment),
*actors* (vehicles, pedestrians, sensors), *blueprints* (templates for
creating actors), *waypoints* (points on the road network), and the *Traffic
Manager* (NPC behaviour).


The Course ROS 2 Bridge
~~~~~~~~~~~~~~~~~~~~~~~

CARLA 0.9.16 introduced native ROS 2 support through a ``--ros2`` flag, which
removes the need for the old external ``carla-ros-bridge``.

.. danger::

   **But there is a bug.** The native interface generates topic names
   containing a double slash, for example ``/carla//camera/image``. ROS 2
   validates topic names strictly and rejects consecutive slashes.

   The consequences: ``ros2 topic echo`` fails, ``ros2 topic hz`` fails,
   RViz2 cannot subscribe, and your own nodes receive nothing.

   **Nothing crashes to tell you.** Naming and wire-format mistakes fail
   silently. You will meet this class of bug in your own projects.

The course therefore ships its own small bridge package, which publishes
valid topic names and exposes exactly the interface the projects need.


Synchronous Mode
~~~~~~~~~~~~~~~~

Left to itself the server ticks as fast as the hardware allows and hands your
client whatever happened to be ready when it asked.

- Sensor streams arrive at irregular, unrepeatable times, and two runs of the
  same script disagree.
- You then debug timing errors **you created**, on top of the ones the
  physics gives you for free.

The fix is three lines:

.. code-block:: python

   settings = world.get_settings()
   settings.synchronous_mode = True
   settings.fixed_delta_seconds = 0.05      # 20 Hz
   world.apply_settings(settings)
   # then drive the clock yourself
   world.tick()

Each sensor's own rate is its ``sensor_tick``.

.. warning::

   **Do this before you write anything else.** Retrofitting synchronous mode
   into a working asynchronous pipeline means re-checking every callback you
   have already written.


.. _l2-where-simulation-ends:

Where the Simulation Ends
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: table-striped

   * - **Fidelity**
     - **What falls in this band**
   * - Modelled well
     - Geometry, road networks, traffic rules, actor kinematics, sensor
       placement and extrinsics, timing and message flow, gross weather
       effects
   * - Modelled roughly
     - Material appearance and reflectance, LiDAR returns in rain and fog,
       RADAR multipath, camera artefacts such as bloom, rolling shutter and
       lens flare
   * - Not modelled
     - Sensor degradation and dirt, calibration drift, hardware faults, real
       human behaviour in its full variety, the appearance statistics a real
       deployment would see

.. admonition:: This is a grading criterion, not a caveat
   :class: danger

   A detector trained only on CARLA will not transfer to real footage without
   adaptation. **The skills transfer completely. The weights do not.**

   "Our system achieves 0.83 mAP" is a claim about CARLA. Writing it as a
   claim about *driving* is the same error as quoting a benchmark number
   without its operating conditions, and it is marked the same way.


Live Demonstration
~~~~~~~~~~~~~~~~~~

All four demos use the same two repositories:

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - **Repository**
     - **Contents**
   * - `enpm818z-fall-2026-carla-python <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python>`_
     - The plain Python demos. One file per demo, under ``lecture2/``.
   * - `enpm818z-fall-2026-carla-ros <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros>`_
     - The ``l2_carla_demo`` ROS 2 package.

.. important::

   On the Docker setup the server runs **headless**, so no window appears when
   it starts. See :ref:`why-headless` for why. To watch the simulation, run the
   viewer client ``spectator_view.py`` -- see
   :doc:`Using CARLA from Python </carla/carla-python>`.


Demo 1: Connect and Inspect
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 1. start the server, wait until it answers
   # 2. run the demo
   python3 demo1_connect.py --town Town03
   # 3. optional, second terminal
   python3 spectator_view.py

**Watch for:** how long ``load_world`` takes. That is a full level load in a
game engine, and it is why the client timeout is generous. When your own
script times out here, the usual cause is a server that has not finished
loading, not your code.

A **blueprint is a template**. Nothing exists in the world until you spawn an
actor from one.


Demo 2: Spawn a Sensor Suite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python3 demo2_spawn_suite.py --seconds 60
   # while that runs, in a second terminal:
   python3 spectator_view.py

The viewer finds the ego this script spawned and follows it. Start the viewer
first and it spawns its own, so you watch the wrong car.

- ``try_spawn_actor`` returns ``None`` instead of raising when a spawn point
  is occupied. In a world with traffic, this matters.
- **The** ``Transform`` **passed when a sensor is attached is its extrinsic
  calibration.** It is hard-coded here. The rest of the lecture is about why
  those six numbers per sensor are the hardest part of building a suite.
- The delivered rate of each stream, printed at the end, is **not** the rate
  configured on the blueprint.


Demo 3: The Same Data in ROS 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # once, to build
   cd ~/enpm818z_ws
   colcon build --packages-select l2_carla_demo
   source install/setup.bash          # again in every new terminal

   # then
   ros2 launch l2_carla_demo demo.launch.py
   ros2 topic hz /carla/ego_vehicle/rgb_front/image

This is the interface your entire project is written against.

- **Watch the publish rate.** It is not the rate you configured, and it drops
  as the scene gets busy. Timing is a first-class concern here.
- In RViz2 the point cloud and the camera image appear in the same frame of
  reference, and that only works because someone specified the transforms
  correctly.


Demo 4: Weather
~~~~~~~~~~~~~~~

.. code-block:: bash

   python3 demo4_weather.py --view --seconds-per-preset 4
   python3 demo4_weather.py --contact-sheet out/weather.png

Six presets: clear noon, wet noon, hard rain, sunset, dense fog, night.

**The camera fails in two different ways**, which is why the script reports
two numbers for it:

.. list-table:: Measured, 0--255
   :widths: 34 22 22 22
   :header-rows: 1

   * - **Preset**
     - **LiDAR pts/sweep**
     - **Camera brightness**
     - **Camera contrast**
   * - clear noon
     - 11475
     - 128.1
     - 47.0
   * - hard rain
     - 11475
     - 115.2
     - 36.0
   * - dense fog
     - 11476
     - 161.7
     - 40.0
   * - night
     - 11471
     - 47.2
     - 29.9

Night takes the brightness. **Fog produces the brightest frame of the six**
and one of the flattest: the image is not dark, it is *uniform*, and a
detector needs edges rather than photons.

.. warning::

   **Now watch what does not happen.** LiDAR returns hold near 11,500 per
   sweep across all six presets. Rain and fog scatter a real LiDAR badly, and
   **CARLA's ray cast does not model that**: attenuation is a fixed
   blueprint attribute that the weather never touches.

   That is a limitation of the tool, not a fact about LiDAR. It is
   :ref:`l2-where-simulation-ends` made concrete. A degraded-weather result
   from CARLA numbers alone is not a result.


The Sensor Challenge
--------------------

Every sensor on a vehicle is good at something and blind to something else.
That is not a procurement problem to be solved by finding a better sensor. It
is a structural fact you design around.


The Complementarity Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Different sensing modalities have strengths and weaknesses that balance
each other. Combined, they are more robust than any one of them alone.**
(Luo, 1989.)

Reading the Venn diagram: a circle alone is what only that sensor gives you.
An overlap is what you get by combining that pair, and neither produces it
alone. The middle is all three, answering the three questions a planner
needs: **what it is, where it is, how fast it is going**.

.. admonition:: The question to sit with
   :class: hint

   If you were given two identical forward cameras, what have you gained?

   Protection against one camera dying, and nothing else. Sun glare blinds
   both at the same instant, because their weaknesses are identical.

   That distinction, **redundancy versus complementarity**, is the whole
   lecture in miniature.

This is not a claim that more sensors are always better. It is a claim that
the gaps must not be the same shape.


Four Words
~~~~~~~~~~

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: table-hover

   * - **Term**
     - **What it means in this course**
   * - Modality
     - A kind of sensing, **not** a piece of hardware. Two cameras are one
       modality; a camera and a RADAR are two. Complementarity is a claim
       about modalities, never about counts.
   * - Accuracy
     - How close a measurement is to the truth.
   * - Resolution
     - How close two things can be and still be told apart. **Independent of
       accuracy**: a sensor can report range to the centimetre and still
       merge two objects into one.
   * - Angular resolution
     - The smallest angular separation two returns can have and still be
       resolved. It is an angle, so the width it covers grows with range:
       :math:`2^\circ` is 3.5 m at 100 m, which is a car and the motorcycle
       beside it.

.. note::

   The word **frame** means three different things in this lecture: a
   coordinate frame, one image from a camera, and one LiDAR sweep. Where it
   is genuinely ambiguous the notes say *coordinate frame* or *image*.


Capability Comparison
~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Read the columns, not the rows.
   :widths: 28 18 18 18 18
   :header-rows: 1
   :class: table-striped

   * - **Capability**
     - **Camera**
     - **LiDAR**
     - **RADAR**
     - **IMU/GNSS**
   * - Day / night
     - Fair
     - Good
     - Good
     - n/a
   * - Adverse weather
     - Poor
     - Fair
     - **Good**
     - n/a
   * - Object classification
     - **Excellent**
     - Poor
     - Poor
     - n/a
   * - Range accuracy
     - Poor (mono)
     - **Excellent**
     - Good
     - Moderate
   * - Velocity measurement
     - Poor
     - Fair
     - **Excellent**
     - Good
   * - Angular resolution
     - **Excellent**
     - Good
     - Poor
     - n/a
   * - Cost
     - Low
     - High
     - Medium
     - Medium

**Every bold entry is a monopoly.** Only the camera classifies. Only RADAR
measures velocity directly and survives weather. Only LiDAR measures range
precisely. Remove any one column and something in the left-hand list has no
supplier.


Sensor Technologies
-------------------

Five modalities, one at a time. For each: what it physically measures, the
numbers that constrain your design, and the way it fails. **The failure mode
is the part you will be tested on by reality.**


The Camera: Specifications
~~~~~~~~~~~~~~~~~~~~~~~~~~

The richest semantic sensor, and the only one that reads traffic lights,
signs and road markings. Everything else on the vehicle measures geometry.

.. list-table::
   :widths: 24 76
   :header-rows: 1

   * - **Parameter**
     - **Range, and what it costs you**
   * - Resolution
     - 1--12+ MP. Sets the distance at which a pedestrian is still more than
       a few pixels tall.
   * - Frame rate
     - 30--60 Hz. **At 30 Hz and 30 m/s you move a metre between frames.**
   * - Dynamic range
     - 120+ dB. The tunnel-exit problem: sunlit road and shadowed interior
       in one frame.
   * - Field of view
     - 30--180°. Narrow sees far, wide sees around, so you fit both.

**Degrades with** low light (noise and motion blur), rain on the lens, fog
and snow (contrast collapse), and direct sun (flare, saturation).

Every one of those is a **photometric** failure. The geometry was never
measured in the first place, which is where LiDAR comes in.


The Camera: Three Jobs
~~~~~~~~~~~~~~~~~~~~~~

- **Classification and recognition.** Every other sensor tells you something
  is there. The camera tells you *what* it is, and that label is what the
  planner reasons about. LiDAR and RADAR **detect**; the camera
  **classifies**.
- **Semantic segmentation and lane detection.** Pixel-level labelling of
  road, pavement and sky. No LiDAR equivalent at this resolution.
- **Traffic lights and signs.** Colour and text. A LiDAR sees a flat
  rectangular plate at a known height; only the camera knows it says STOP.

.. important::

   Nobody seriously proposes a stack with no vision in it. **The industry
   debate is whether vision is sufficient, never whether it is necessary.**


Camera Types
~~~~~~~~~~~~

.. list-table::
   :widths: 14 30 26 30
   :header-rows: 1
   :class: table-striped

   * - **Type**
     - **What it is for**
     - **Advantage**
     - **Disadvantage**
   * - Telephoto
     - Narrow FOV, long range. Highway ACC, reading signs hundreds of metres
       out.
     - Sees far, high angular detail.
     - Sees almost nothing to the side.
   * - Fisheye
     - 180°, surround view, parking, cross-traffic.
     - Full coverage from few units.
     - Heavy distortion; poor at range.
   * - Stereo
     - Two cameras, geometric depth by triangulation.
     - Depth is measured, not inferred.
     - Error grows as :math:`z^2`; **needs its own extrinsic calibration
       between the pair**.
   * - Monocular depth
     - One camera, depth inferred by a network.
     - Cheapest possible depth.
     - An estimate, with scale ambiguity.

Choosing stereo gives you depth **and** a calibration problem at the same
time.

Suppliers you will meet: Bosch (MPC3), Continental and Magna for forward
modules; Valeo for surround-view. Tesla HW4 (2023) moved the forward cameras
from roughly 1.2 MP to about 5 MP, specifically to push classification range.
Subaru EyeSight is the best-known production stereo pair.


Stereo
~~~~~~

Two ordinary cameras with optical centres :math:`O_L` and :math:`O_R`, a
known **baseline** :math:`B` apart, pointing the same way and shooting at the
same instant. A world point :math:`P` lands at a different pixel in each
image, :math:`p_l` and :math:`p_r`. That gap is the **disparity** :math:`d`.

.. math::

   z = \frac{B f}{d}

- :math:`z` -- the depth to :math:`P`. **The unknown.**
- :math:`B, f` -- baseline and focal length. Both known.
- :math:`d` -- the disparity in pixels. **The measurement.**

Near things shift a lot, far things shift a little.

.. list-table:: What 0.1 px of disparity error costs. :math:`B` = 20 cm, :math:`f` = 1000 px.
   :widths: 28 18 18 18 18
   :header-rows: 1

   * - **Range**
     - 10 m
     - 20 m
     - 50 m
     - 100 m
   * - Disparity
     - 20 px
     - 10 px
     - 4 px
     - 2 px
   * - Depth error
     - 0.05 m
     - 0.20 m
     - 1.25 m
     - **5.0 m**

Stereo is a real measurement, not a guess. But the error grows as
:math:`z^2/(Bf)`, and **the only term you control is the baseline, which is
bounded by the width of the car.** Hence LiDAR at long range.


Monocular
~~~~~~~~~

One camera. A network predicts a depth for every pixel from the cues you use
in a photograph: familiar size, perspective, occlusion, ground contact.

.. admonition:: Scale ambiguity is geometry, not a limitation of today's networks
   :class: warning

   A toy car 10 cm wide at 1 m and a real car 1.8 m wide at 18 m fill the
   viewing cone identically and land on the same pixels. **The image is the
   same image.** Depth is recoverable only up to an unknown scale, and no
   amount of training data recovers a number that was never in the image.

Scale must come from elsewhere: camera height above a flat road, known object
sizes, ego-motion from the wheels or IMU, or a few RADAR or LiDAR returns.
Production systems lean hardest on camera height, which is also why a
monocular stack degrades on a road that is not flat.

**And it fails plausibly.** Stereo returns nothing when it cannot match; a
monocular network always returns a full, confident map, including for an
object it has never seen.


LiDAR: Time of Flight
~~~~~~~~~~~~~~~~~~~~~

Direct 3-D geometry, independent of ambient light, because it brings its own.
Fire a very short laser pulse, start the clock, stop it when the reflection
comes back.

.. math::

   r = \frac{c\,t}{2}

- :math:`r` -- the range. The unknown.
- :math:`t` -- the round-trip time. **The only quantity the sensor measures.**
- :math:`c` -- the speed of light, a constant of nature, not something you
  calibrate.
- The **2** is because the pulse travels out and back.

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - **Quantity**
     - **Value**
   * - Laser wavelength
     - 905 nm (cheap silicon detectors) or 1550 nm (eye-safe at higher power,
       so longer range, and dearer)
   * - Round trip at 100 m
     - 667 ns
   * - Timing precision for ±2 cm
     - **133 ps**
   * - Points per second
     - 300 k -- 2 M+
   * - Beams
     - 16 -- 128

**133 picoseconds is why LiDAR is expensive.** You are not paying for the
laser. You are paying for a clock that resolves light travelling four
centimetres.


LiDAR: Types and Failure Modes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Mechanical spinning** uses a rotating assembly for a full 360°: bulky,
costly, with bearings that wear. **Solid-state** uses MEMS mirrors or
electronic beam steering: compact, robust, mass-manufacturable, but
forward-facing only.

The output is a **point cloud**: an unordered set of :math:`(x, y, z)`
returns, each with an intensity, and **no connectivity between them**.
Nothing tells you which points belong to the same object.

.. danger::

   **In fog the LiDAR does not go blind. It returns the fog.** The pulse
   scatters off the droplets and comes back early, so you have confident
   measurements of nothing.

   **A matte black car absorbs the pulse** and can simply not come back.
   Reflectivity is a property of the target, not of your sensor, so no amount
   of money fixes it. This is one of the strongest arguments for keeping
   RADAR.

Vertical resolution decays with range, so the far-field point cloud is far
sparser than the near-field one, and much sparser than the renderings you
have seen.


LiDAR: Spinning versus Solid-State
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 22 39 39
   :header-rows: 1

   * -
     - **Mechanical spinning**
     - **Solid-state**
   * - For
     - True 360° from one unit.
     - Compact, integrates into the body; no large moving parts; cheaper at
       volume.
   * - Against
     - Bulky, must sit high; bearings wear; expensive per unit.
     - Forward wedge only, so several are needed for coverage.
   * - Who uses it
     - Robotaxis and research fleets: Waymo, Zoox, Motional.
     - Production cars: Mercedes Drive Pilot, BMW, NIO, Li Auto, Xiaomi,
       Zeekr, BYD.

Underneath the aesthetics is an engineering point: **a bearing is a wear item
with a service life**, and automotive qualification is unkind to wear items.
Hesai, Huawei, RoboSense, Seyond and Valeo hold over 90% of the automotive
market between them.

.. warning::

   This moves fast. Volvo cancelled its Luminar contract in November 2025;
   the 2026 EX90 and ES90 ship with no LiDAR at all.


RADAR: Doppler and the Angular Weakness
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The all-weather sensor, and the only one that **measures velocity directly**
rather than differencing positions over time.

A siren sounds higher as the ambulance approaches and lower once it has
passed. Radio waves do the same. If the echo returns at a higher pitch than
it was sent, the object is closing; lower, and it is receding. How much the
pitch changed tells you how fast, from a single measurement.

.. list-table::
   :widths: 28 72
   :header-rows: 1

   * - **Parameter**
     - **Value**
   * - Frequency
     - 76--81 GHz band; 77 GHz typical, 79 GHz for imaging radar
   * - Modulation
     - FMCW, a frequency-modulated chirp. Comparing the echo's sweep against
       the outgoing one yields range and Doppler together.
   * - Range resolution
     - 0.1--1.0 m
   * - Velocity accuracy
     - ±0.1 km/h, **measured directly**
   * - Angular resolution
     - **1--10°, the weakness**

A 2° beam is 0.7 m wide at 20 m and **3.5 m wide at 100 m**. At 100 m a car
and a motorcycle beside it fall in one beam and return one blob. RADAR knows
exactly how fast that blob is closing, and very little about its shape.
Excellent radial information, poor cross-range information, which is exactly
the reverse of the camera.


.. _l2-zero-doppler:

Zero-Doppler Filtering
~~~~~~~~~~~~~~~~~~~~~~

RADAR is excellent in weather and measures velocity directly. So why does
anyone still fit LiDAR? Because of this.

**The echo always comes back.** Metal reflects whether or not it is moving.
The question is only whether anything makes it stand out.

.. list-table::
   :widths: 14 20 32 34
   :header-rows: 1
   :class: table-striped

   * - **You**
     - **The object**
     - **Its Doppler shift**
     - **What happens**
   * - Moving
     - Moving differently
     - Stands out from the ground
     - Reported. This is what RADAR is good at.
   * - Moving
     - Stationary
     - **Exactly matches** the road, signs and bridges
     - Discarded as clutter. It looks like scenery.
   * - Stationary
     - Stationary
     - None, from anything
     - Nothing stands out at all.

The road is full of stationary metal: manhole covers, bridge joints, sign
gantries, a discarded exhaust pipe. Reporting all of it would brake the car
constantly, so production stacks throw those returns away. **A stopped
vehicle in your lane fails exactly the same test.**

.. danger::

   This is not a defect. It is a deliberate engineering compromise, and it is
   implicated in a series of real crashes into stopped vehicles and parked
   emergency vehicles.

   It is also the strongest single argument for not deleting LiDAR, which has
   no equivalent blind spot: **a laser does not care whether the thing it hit
   was moving.**


RADAR: Range Classes and Balance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 16 18 66
   :header-rows: 1

   * - **Class**
     - **Range**
     - **Job**
   * - Short (SRR)
     - < 30 m
     - Blind spot, cross-traffic, parking. Corner-mounted, wide FOV.
   * - Mid (MRR)
     - 30--80 m
     - Lane change, cut-in detection.
   * - Long (LRR)
     - 80--250 m
     - Highway ACC, forward collision warning. Narrow FOV.
   * - Imaging
     - 79 GHz
     - Many more channels; angular resolution approaching a coarse LiDAR.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: Advantages
      :class-header: bg-success text-white

      - Works in rain, fog, snow and darkness. The only sensor here that
        genuinely does.
      - Measures velocity directly from Doppler.
      - Long range from a cheap, small, easily hidden module.
      - Unaffected by lighting, sun angle or lens contamination.

   .. grid-item-card:: Disadvantages
      :class-header: bg-danger text-white

      - Angular resolution 1--10°: objects merge at range.
      - Multipath produces ghost objects that were never there.
      - Zero-Doppler filtering discards stationary objects.
      - **Cannot classify.** It has no idea what it has found.

That last row on each side is the pairing that matters: RADAR's inability to
classify is precisely the camera's monopoly.


Why the IMU Drifts
~~~~~~~~~~~~~~~~~~

An IMU does not perceive the world at all. It feels acceleration and turning,
much as your inner ear does, and it feels them continuously.

**To get a position out of acceleration you have to add the readings up
twice**: once for speed, again for distance. Adding up the readings also adds
up their errors. A tiny constant bias becomes a steadily growing speed error,
and a position error that grows faster still.

Walk across a room blindfolded, counting paces. Fine for three metres.
Hopeless for thirty. Nothing ever tells you how far off you are.

.. list-table::
   :widths: 20 80

   * - Measures
     - Linear acceleration and angular rate, **never position directly**
   * - Rate
     - > 100 Hz, continuous, and it never loses signal
   * - Strength
     - Smooth and fast. Works in a tunnel, a car park, anywhere
   * - Weakness
     - **Drifts without bound.** The error only ever grows


GNSS, and the Cleanest Complementarity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GNSS times signals from satellites and reports where you are on the globe. It
is **the only absolute reference on the vehicle**: everything else measures
change, this measures position.

.. list-table::
   :widths: 20 80

   * - Measures
     - Absolute position on the globe
   * - Rate
     - 1--20 Hz, slow next to an IMU
   * - Strength
     - **Does not drift, ever.** Today's error is the same size as last
       year's
   * - Weakness
     - Blocked in tunnels and car parks; multipath in urban canyons

The IMU carries the estimate between fixes; each GNSS fix pulls the
accumulated drift back to zero. **Fast and drifting meets slow and bounded**,
and the two error characteristics are exact opposites. This is the cleanest
example of complementarity in the lecture, and the classic Kalman filter
application, worked in L3.


The Urban Canyon
~~~~~~~~~~~~~~~~

Tall buildings on both sides break a GNSS fix in two different ways.

- **Blocked is the honest failure.** Fewer satellites means a worse fix, or
  none, and the receiver says so.
- **Multipath is the dangerous one.** The signal arrives by a bounced path,
  which is longer than the direct one, so the receiver places the satellite
  further away than it is and the car in the wrong place. **The fix still
  arrives, looks perfectly normal, and is several metres out.**

With enough of both, the vehicle falls back to dead reckoning on the IMU
alone, and the error grows the whole time. A fusion filter therefore has to
be able to distrust an input that looks fine, which is next week.


Ultrasonic: What It Is For
~~~~~~~~~~~~~~~~~~~~~~~~~~

A short pulse of sound at about 40 kHz, too high to hear, and the echo is
timed. Same time-of-flight principle as LiDAR, but sound travels far slower
than light, so the timing is easy and the electronics are cheap.

- **Parking.** Distance to the kerb, the wall, the car behind you.
- **Low-speed automatic braking.** Stopping before the bollard you cannot see
  over the bonnet.
- **The near field below the bumper line**, where every other sensor is
  blind. Cameras and LiDAR are mounted high and look outward, so the metre
  around the car is the ultrasonics' alone.

A production vehicle typically carries eight to twelve, along the front and
rear bumpers.

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - **Advantages**
     - **Disadvantages**
   * - A few dollars each, and already in every bumper.
     - Range of only 0.2--5 m. Useless above walking pace.
   * - Works in the dark and in fog, and on glass and other surfaces that
       defeat optical sensors.
     - Reports a distance, not a direction. Cannot classify or measure
       velocity.

**The cheapest sensor on the vehicle covers the one volume the expensive ones
cannot see.** Tesla removed ultrasonics in 2022 and replaced them with
vision, which is a live experiment rather than a settled answer.


The Suite, Side by Side
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 14 22 30 34
   :header-rows: 1
   :class: table-striped

   * - **Sensor**
     - **Measures**
     - **Fails when**
     - **On the vehicle because**
   * - Camera
     - Colour, texture, semantics
     - Dark, glare, fog, dirty lens
     - It is the only thing that can read
   * - LiDAR
     - Range, precisely, in 3-D
     - Fog, rain, matte black targets
     - Direct geometry independent of light
   * - RADAR
     - Range and radial velocity
     - Poor cross-range; ghosts; zero-Doppler
     - It works when the weather has taken the others
   * - Ultrasonic
     - Very short range
     - Above 5 m; wind; packed snow
     - It covers the near field nothing else sees
   * - IMU
     - Acceleration, angular rate
     - Drifts without bound
     - High rate, never loses signal
   * - GNSS
     - Absolute global position
     - Tunnels, urban canyons, multipath
     - It is the only absolute reference

**No two rows fail for the same reason.** That is the complementarity
principle stated as a bill of materials, and it is the test to apply to any
suite you are asked to justify.


Discussion 1 -- Which Sensor Would Have Seen It?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each scene: which modality **sees it**, which one **misses it**, and
**why**, in terms of the physics rather than the brand.

.. list-table::
   :widths: 6 94
   :header-rows: 1

   * -
     - **Scene**
   * - A
     - A fire truck stopped across your lane on a clear, dry motorway. You
       are closing at 110 km/h.
   * - B
     - A pedestrian in dark non-reflective clothing, crossing an unlit road
       at night, away from a crossing.
   * - C
     - A motorcycle filtering between two lanes of traffic, 90 m ahead, in
       heavy rain.
   * - D
     - A temporary roadworks sign reading *lane closed 400 m*, in bright
       low-angle winter sun.
   * - E
     - You exit a 600 m tunnel into daylight, on a curve, in a dense urban
       canyon.

.. dropdown:: Discussion 1 -- answers
   :color: success
   :icon: check-circle

   **A. RADAR sees it and may discard it.** Zero Doppler, so the stationary
   filter is the danger (:ref:`l2-zero-doppler`). LiDAR sees it plainly and
   the camera sees it if the contrast holds. This is last week's failure
   class, and the argument against a RADAR-only forward channel.

   **B. LiDAR is the answer, and only just.** No ambient light, so the camera
   is nearly blind. Dark non-reflective clothing is also the LiDAR's worst
   target, so expect few returns. RADAR sees a slow, small, low-RCS mover
   against clutter. This is Tempe, in sensor terms.

   **C. Nobody covers it well, which is the point.** At 90 m a 2° RADAR beam
   is over 3 m wide, so the motorcycle merges with the cars. Rain attenuates
   LiDAR. The camera can classify it if it can see it through the spray.
   Expect disagreement, and let it stand.

   **D. Camera only, no contest.** No other sensor reads text. Then the
   twist: low-angle sun is precisely when the camera saturates, so the one
   sensor that can do the job is the one being blinded. What does redundancy
   even mean here?

   **E. The compound case.** The camera hits the dynamic-range wall at the
   tunnel mouth, GNSS has just lost lock and the urban canyon gives multipath
   when it returns, and the IMU has been dead-reckoning for 600 m and has
   drifted. LiDAR and RADAR are fine. This is why the fusion filter must know
   which inputs to distrust.

   **Which scene had no good answer?** C, and that is honest.


Calibration
-----------

A LiDAR reports metres from itself. A camera reports rows and columns of
pixels. **Nothing in either measurement says whether the two are looking at
the same object.** Calibration supplies the numbers that connect them, so
both can be expressed in one common frame and compared.

.. admonition:: The formal definition (VIM, 2012)
   :class: note

   An operation that, under specified conditions, "establishes a relation
   between the quantity values with measurement uncertainties provided by
   measurement standards and corresponding indications with associated
   measurement uncertainties", and then uses that relation to obtain a
   measurement result from an indication.

   **In plain terms:** you compare the sensor against something you already
   trust, and keep the numbers that turn its raw readings into real-world
   quantities. They are not in the data. You measure them once, and then keep
   checking them.


Why Bother
~~~~~~~~~~

- A LiDAR cluster says something is 23 m ahead and 1.8 m wide, to the
  centimetre, **but it has no idea what that something is**.
- A camera says *that is a pedestrian*. It can estimate range too, but far
  less well.
- The two statements are in **different coordinate systems**, so there is no
  way even to ask whether they describe the same object.
- Calibration puts them in one frame. It takes two pieces: the **extrinsic**
  between the two sensors, and the camera's **intrinsics**. Apply the
  extrinsic, then the intrinsics, and a LiDAR point becomes an exact pixel.

So you calibrate **the camera** (its own optics) and **the pair** (how they
sit relative to each other). The LiDAR's internal calibration normally comes
from the factory and you leave it alone.

.. important::

   **Calibration is not fusion.** Calibration tells you which pixel a LiDAR
   point lands on. It does not tell you whether the thing at that pixel and
   the thing the laser hit are the same object. Deciding that is **data
   association**; merging the two into a single estimate is **fusion**. Both
   are L3.

**What goes wrong without it:** the label lands on the wrong object, so the
pedestrian's identity gets attached to the parked car beside them; one real
object becomes two tracked objects; and **it fails quietly**, with numbers
that stay plausible and worsen with range.


Intrinsic Calibration
~~~~~~~~~~~~~~~~~~~~~

**Inside one sensor.** How a ray of light arriving from the world becomes a
pixel at a particular row and column. Nothing to do with any other sensor.

Take a point at :math:`(X, Y, Z)` in front of the camera. Divide by :math:`Z`
to get the direction it lies in, since everything along that direction lands
on the same pixel. Multiply by the focal length to turn a direction into
pixels. Then add an offset, because pixel :math:`(0,0)` is the corner of the
image, not the lens axis:

.. math::

   u = f_x \frac{X}{Z} + c_x, \qquad v = f_y \frac{Y}{Z} + c_y

.. math::

   K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}

- :math:`K` is those two lines packed into one matrix.
- :math:`f_x, f_y` -- how zoomed in the lens is, in pixels. Bigger :math:`f`,
  more pixels per degree, narrower view.
- :math:`c_x, c_y` -- where the lens axis actually meets the sensor. **Never
  exactly the middle.**
- Plus distortion coefficients: radial (barrel and pincushion) and tangential.

You have done this in ENPM673. **Zhang's method**: photograph a planar
checkerboard from many angles, detect the corners, solve for :math:`K` and
the distortion.

.. note::

   Intrinsics belong to the **camera and lens**, so they travel with the
   camera and do not change when you move it, and they are far more stable
   than extrinsics: calibrate once at build time, then check rarely.

   Not immune, though. Across −40 to +85 °C the focal length and principal
   point shift enough to matter, which is why some automotive cameras carry a
   temperature sensor for exactly this.


Extrinsic Calibration
~~~~~~~~~~~~~~~~~~~~~

**Between two things.** Where one sensor sits relative to another, or
relative to the vehicle. **This is the one that makes fusion possible, and
the one that goes wrong.**

.. math::

   T = \begin{bmatrix} R & t \\ 0 & 1 \end{bmatrix} \in SE(3)

- :math:`R` turns it, :math:`t` slides it. *Rigid* means solid brick: you may
  carry it and spin it, never bend or stretch it.
- **Six numbers, no more.** Three for which way it points, three for where it
  is.
- :math:`SE(3)` is the set of those rigid motions; :math:`R \in SO(3)` is the
  turning alone.

.. warning::

   **Both properties from the previous slide are now false.** An extrinsic
   belongs to the *installation*, not to the sensor, so it is wrong the
   moment anything is remounted. And it is **not stable**: vibration, thermal
   expansion and knocks move sensors relative to each other over months.

   That is why extrinsics get monitored and re-estimated while the vehicle
   drives, and intrinsics are revisited far less often.


.. _l2-frame-convention:

Right to Left
~~~~~~~~~~~~~

A coordinate frame is an agreed origin and set of axes. The LiDAR reports
points in its frame, the camera in its own, the vehicle in a third.

.. admonition:: The convention used for the rest of this course
   :class: important

   :math:`T_{A \leftarrow B}` takes a point **in frame** :math:`B` and
   returns it **in frame** :math:`A`. Say it aloud as "**A from B**".

Chains compose, and the inner frames cancel:

.. math::

   T_{A \leftarrow C} = T_{A \leftarrow B}\, T_{B \leftarrow C}

Inversion flips the arrow: :math:`T_{B \leftarrow A} = (T_{A \leftarrow B})^{-1}`.
Applied to a point, :math:`p_A = R\,p_B + t`, so spin it, then slide it.

**Read a chain the way you cancel fractions.** In
:math:`T_{C \leftarrow V}\, T_{V \leftarrow L}` the two :math:`V`\ s meet in
the middle and vanish, leaving :math:`C \leftarrow L`. If they do not meet you
have written it backwards, and you know that **before** running any code.

.. warning::

   **CARLA does not put** :math:`V` **at the rear axle.** An actor's transform
   sits near the body centre, so read the simulator's origin rather than
   assuming the textbook one.


.. _l2-gp1-chain:

The GP1 Chain and the Axis Trap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calibration gives you each sensor's pose in the vehicle frame,
:math:`T_{V \leftarrow L}` and :math:`T_{V \leftarrow C}`. What you need is
camera-from-LiDAR:

.. math::

   T_{C \leftarrow L} = T_{C \leftarrow V}\, T_{V \leftarrow L}
                      = (T_{V \leftarrow C})^{-1} T_{V \leftarrow L}

The inner :math:`V` cancels. Then project, with the perspective division:

.. math::

   u \sim K\, P\, T_{C \leftarrow L}\, p_L

.. danger::

   **The axis trap.** :math:`K` assumes the **optical** convention: *x*
   right, *y* down, *z* forward along the optical axis. CARLA, like most
   robotics and game engines, uses *x* forward, *y* right, *z* up. The same
   three physical directions under different names, so you must **relabel**
   them before :math:`K` ever sees them:

   .. math::

      P = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & -1 \\ 1 & 0 & 0 \end{bmatrix}

   Read row 1 as "optical *x* is body *y*".

   Signs depend on the handedness of your source frame, so **derive**
   :math:`P` from your own convention rather than copying it. Omit :math:`P`
   altogether and you get **no error and a garbage image**. Budget an evening
   for this in GP1.


Time Synchronisation
~~~~~~~~~~~~~~~~~~~~

Extrinsics tell you **where** each sensor was. They say nothing about
**when**. Fusing a camera image with a LiDAR sweep captured 30 ms later is a
calibration error that no amount of :math:`T_{C \leftarrow L}` will fix.

.. list-table:: How far the ego vehicle travels during a synchronisation error
   :widths: 30 20 20 30
   :header-rows: 1

   * - **Timing error**
     - **At 50 km/h**
     - **At 110 km/h**
     - **Comparable to**
   * - 33 ms (one 30 Hz frame)
     - 0.46 m
     - **1.01 m**
     - Half a car length at speed
   * - 10 ms
     - 0.14 m
     - 0.31 m
     - A wheel's width
   * - 1 ms
     - 0.01 m
     - 0.03 m
     - Below LiDAR noise

- Worse for closing objects: two vehicles approaching head-on at 110 km/h
  close at 61 m/s, so 10 ms of skew is 0.61 m of range error.
- **A spinning LiDAR does not capture a sweep instantaneously.** Points in
  one "frame" are stamped across a whole rotation, so motion compensation
  matters.
- Production stacks distribute one clock: PTP (IEEE 1588) over automotive
  Ethernet, or GNSS-disciplined time, and every sensor timestamps at capture.


Validating a Calibration
~~~~~~~~~~~~~~~~~~~~~~~~

**A calibration is not finished when the optimiser converges. It is finished
when you can state its error and show it holds at range.**

- **Reprojection error.** Project known 3-D points into the image and measure
  the pixel residual. Report the **distribution**, not the mean: the tail is
  what breaks association.
- **Check at range, not on the bench.** 9 cm at 5 m, 1.75 m at 100 m. A
  calibration validated only up close is not validated.
- **Edge alignment.** Overlay depth discontinuities on image edges. A
  systematic offset along one axis points at a specific rotation term.
- **Cross-check the chain.** Project LiDAR to camera and back. Round-trip
  error should be numerical noise; if it is not, the **composition** is
  wrong, not the calibration. Four lines of code, and the cheapest bug-finder
  you have.

Typical acceptance for a production LiDAR--camera pair: rotation error below
about 0.1° and translation below a couple of centimetres. **0.1° is 17 cm at
100 m**, about a third of a car width. That is the tolerance the whole
downstream stack inherits.


Discussion 2 -- One Degree
~~~~~~~~~~~~~~~~~~~~~~~~~~

Your LiDAR-to-camera extrinsic rotation is wrong by **one degree**. Nothing
else is wrong.

1. Fill in the lateral error at each range. (It is :math:`r\theta`.)
2. At which range does this first break **object association**, deciding that
   this LiDAR cluster and that camera box are the same car?
3. Would you notice this on a calibration bench in the lab? Would you notice
   it on the road?

.. dropdown:: Discussion 2 -- answers
   :color: success
   :icon: check-circle

   **The numbers:** 0.17 m at 10 m, 0.87 m at 50 m, **1.75 m at 100 m**,
   3.49 m at 200 m.

   **Comparable to:** nothing at 10 m. Half a car width at 50 m. **A whole
   car width at 100 m.** A full lane at 200 m.

   **Question 2.** Association breaks somewhere between 50 and 100 m, because
   that is where the error exceeds the object you are trying to match. Past
   that the box and the cluster no longer overlap, and fusion does not
   degrade gracefully: it starts confidently pairing the wrong things, which
   is worse than not fusing at all.

   **Question 3, the real lesson.** On a bench you would not notice: at 5 m
   the error is 9 cm and looks like noise. It only appears at range, which is
   exactly where you cannot easily verify it. This is why calibration is
   validated with quantitative reprojection metrics over the full range, not
   by eye on a checkerboard at arm's length.

   **Extension.** A 0.1° error gives 17 cm at 100 m, which is why sub-degree
   accuracy is the specification.


Calibration in Practice
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Three families. The trade is always accuracy against how easily you can repeat it.
   :widths: 18 44 38
   :header-rows: 1

   * - **Method**
     - **How**
     - **Trade**
   * - Target-based
     - A checkerboard or AprilTag board visible to both sensors at once;
       least-squares over many poses.
     - Most accurate. Needs a controlled setup, hard to repeat in the field.
   * - Targetless
     - Align natural structure: LiDAR intensity edges against image edges, or
       mutual information.
     - Runs on recorded driving data. Less accurate, sensitive to scene and
       initialisation.
   * - Motion-based
     - Each sensor estimates its own ego-motion; solve the hand-eye problem
       :math:`AX = XB`.
     - No target at all. **Needs real rotation and translation**, so driving
       in a straight line is degenerate.

Tools you will meet: OpenCV ``stereoCalibrate``, Kalibr (ETH Zurich,
camera--IMU), the Autoware calibration toolkit, MATLAB's Lidar Toolbox.

GP1 uses CARLA's published extrinsics, so you get exact ground truth. That is
a luxury you will never have again.


Calibration Drifts
~~~~~~~~~~~~~~~~~~

Vibration, thermal expansion and mechanical shock move sensors relative to
each other. **A vehicle calibrated perfectly in January is not calibrated in
July.**

- **Monitor.** Track reprojection consistency between LiDAR points and camera
  features continuously.
- **Correct.** Apply small incremental updates by sliding-window
  optimisation while driving.
- **Escalate.** A large deviation is **not** silently corrected. It is
  flagged for inspection, or triggers a minimal risk condition.

.. important::

   A vehicle that has lost confidence in its own calibration no longer knows
   where its measurements are pointing, and the correct response is to stop
   safely, not to keep driving on numbers it cannot trust.

   Silently auto-correcting a large deviation hides a mechanical fault, which
   converts a detectable hardware problem into an undetectable perception
   problem.


System Design
-------------

Where the sensors go, what happens when one dies, and what everybody else in
the industry actually built. **This section is where the physics turns into
money.**


Placement and Coverage
~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Four requirements
      :class-header: bg-primary text-white

      - **360°**, no blind spots.
      - **Range diversity**: near (< 30 m), mid (30--80 m), far (80 m+).
      - **Redundancy where it matters most**: forward needs camera *and*
        LiDAR *and* RADAR.
      - **Overlap** between neighbours, so a track survives the handover.

   .. grid-item-card:: Typical pattern
      :class-header: bg-secondary text-white

      - **Forward:** long-range RADAR + telephoto camera + primary LiDAR.
      - **Sides:** short-range corner RADARs + fisheye cameras.
      - **Rear:** camera + short-range RADARs for cross-traffic.

Reading the coverage figure: coverage darkens where sensors overlap. **The
LiDAR is a ring, not a disc**, because its beams leave the roof at a limited
downward angle and never strike the ground beside the vehicle. The hatched
patch ahead of the bumper lies inside that hole **and** outside both front
corner RADARs, which are turned outward for cross-traffic. Ultrasonics and a
wide near camera exist to close it.

.. important::

   **The overlap requirement is the non-obvious one.** Adjacent sensors must
   overlap, or a tracked object dies at the seam and is reborn as a new
   object with no history. That is a tracking failure that looks like a
   perception failure, which is exactly what happened at Tempe.


Placement in CARLA
~~~~~~~~~~~~~~~~~~

A mounting is a ``carla.Transform``: ``Location`` in **metres**, ``Rotation``
in **degrees** as ``(pitch, yaw, roll)``. With ``attach_to=vehicle`` it is
read **relative to the vehicle**: *x* forward, *y* right, *z* up, about the
vehicle actor's origin, which is near the body centre and **not** the rear
axle.

.. list-table::
   :widths: 22 40 38
   :header-rows: 1

   * - **Role**
     - **Transform**
     - **Why there**
   * - Forward camera
     - ``Location(x=1.5, z=1.4)``
     - Behind the mirror.
   * - Roof LiDAR
     - ``Location(z=1.8)``
     - Clear line of sight all round.
   * - Corner RADAR
     - ``Location(x=2.2, y=0.9, z=0.5)``, ``Rotation(yaw=45)``
     - Bumper height, turned out for cross-traffic.
   * - Rear camera
     - ``Location(x=-2.0, z=1.0)``, ``Rotation(yaw=180)``
     - Reversing, rear cross-traffic.

.. warning::

   **Do not copy those numbers, derive them.** Blueprints differ in size, so
   read the body with ``vehicle.bounding_box.extent``. It is the **half**-size
   in metres, so the roof is near ``2*extent.z`` and the bumper near
   ``extent.x``. Assume it is a full size and you mount the camera inside the
   bodywork, which returns a perfectly valid image of upholstery.

   **Use** ``AttachmentType.Rigid``, **always.** ``SpringArm`` *smooths* the
   sensor's motion for video, so the sensor-to-vehicle transform is no longer
   constant, and the whole calibration section assumed it was.


Design for Failure
~~~~~~~~~~~~~~~~~~

- **No single point of failure.** If the forward LiDAR is blinded by snow,
  RADAR must still see the stopped vehicle. That requirement is what forces
  the modality mix, not a preference for variety.
- **Degraded modes, defined in advance.** Name the minimum sensor set for
  each capability. Lose a sensor and you disable lane-keeping but retain ACC
  at reduced speed on RADAR, **decided at design time, not invented at
  runtime**.
- **Detect and declare.** Continuous self-diagnostics. Missing data, or data
  wildly inconsistent with the other sensors, must raise a fault, hand back
  to the driver, or execute the MRC.

.. important::

   **Redundancy only counts if the failures are independent.** Two cameras
   mounted side by side are redundant against hardware death and useless
   against sun glare, which blinds both at the same instant.

   Ask of every redundant pair: **what single event takes them both?** Sun,
   fog, mud, a stone.


What Industry Built
~~~~~~~~~~~~~~~~~~~

.. list-table:: A snapshot, not a specification. Counts are generation-specific and change often.
   :widths: 16 28 14 24 18
   :header-rows: 1

   * - **Company**
     - **Philosophy**
     - **Cameras**
     - **LiDAR**
     - **RADAR**
   * - Waymo
     - LiDAR-centric
     - 29
     - 5
     - 6
   * - Tesla
     - Vision-only
     - 8
     - 0
     - 0
   * - Aurora
     - Long-range LiDAR
     - yes
     - FirstLight, 400 m+
     - imaging
   * - Mobileye
     - Camera-first
     - 8--11
     - optional
     - optional
   * - Zoox
     - Purpose-built, symmetric
     - yes
     - four corners
     - yes

**There is no best configuration.** Each is a coherent answer to a different
question about ODD, cost and fusion architecture. A geofenced robotaxi with a
mapped ODD can afford five LiDARs and amortise them over a fleet; a consumer
car sold at volume cannot.

.. warning::

   These numbers move. Waymo's figures describe the 5th-generation Driver;
   the 6th deliberately reduced sensor count to cut cost. Tesla removed radar
   in 2021--22 and has since reintroduced a high-definition radar on some
   vehicles. **Check the current published specification before you rely on
   any number here.**


.. _l2-tesla-case:

The Tesla Case
~~~~~~~~~~~~~~

Everyone else covers the camera's gaps by adding a modality. Tesla removed
them and covers the gaps with data, time and learned priors instead. Whatever
you think of the bet, the engineering answers are specific.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: How the missing sensor is replaced
      :class-header: bg-success text-white

      - **Range becomes a learning problem.** An offline pipeline
        reconstructs the scene in 3-D using the full video, future frames,
        many passes by many cars and unlimited compute. That reconstruction
        is the training target: the car predicts in one instant what the
        offline labeller knew in hindsight.
      - **Unknown objects: occupancy.** A class-agnostic 3-D grid answers
        *is this cube occupied, and which way is it moving*. You do not have
        to recognise a fallen mattress to avoid it.
      - **Video, not frames.** A moving camera has a baseline over time, so
        parallax is real geometry, and occluded objects persist.
      - **No arbitration step.** One backbone, one bird's-eye
        representation, so no moment where two modalities disagree and
        something has to referee.

   .. grid-item-card:: What the bet actually gives up
      :class-header: bg-danger text-white

      - **It is not a lack of redundancy.** There is spatial redundancy
        (overlapping fields of view), focal (several forward focal lengths),
        temporal (video) and proprioceptive (IMU, wheel odometry).
      - **It is a lack of failure-mode diversity.** Sun glare, fog, spray and
        mud degrade all the cameras at once. Eight of the same sensor gives
        coverage, not decorrelation.
      - **And there is no independent runtime cross-check.** A single
        modality cannot check itself against an independent physical
        measurement, so a perception error has nothing to disagree with.

That last point is a **validation** problem. It is L13's problem, and it does
not go away with a better network.


HD Maps as a Prior
~~~~~~~~~~~~~~~~~~

An **HD map** is a centimetre-accurate map of the road built in advance: lane
boundaries, stop lines, crossings, traffic-light positions. The map on your
phone gets you to the street; this one tells the vehicle where its lane edge
is to within a few centimetres.

It is a **prior**: information you already hold *before* you measure
anything. Not a sensor, since nothing about it is live, but it enters the
stack where a sensor does, and it brings a failure mode of its own.

- **What you get:** lane geometry and traffic-light positions known before
  you see them, centimetre localisation by matching a live scan against the
  map, and a standing sanity check on perception.
- **What it costs:** the map must be **built, stored and kept current**. A
  stop line moved two metres makes the prior wrong, and **a confidently wrong
  prior is worse than none at all**.

.. important::

   This is why the industry table looks the way it does. **Waymo maps, and
   launches city by city. Tesla does not, and ships everywhere.** One choice,
   most of the difference between those two rows.

Map *layers* and map-based localisation are **L7**; the formats that encode
them (OpenDRIVE, Lanelet2) and routing are **L8**.


What a Map Is
~~~~~~~~~~~~~

An HD map is **vector geometry registered to a survey point cloud**. The
green lines in the figure are lane boundaries and centrelines, hand-checked
data rather than something a sensor produced; the grey is the LiDAR scan they
were drawn against. Matching a live scan to that cloud is what gives
centimetre localisation.


What It Takes to Have One
~~~~~~~~~~~~~~~~~~~~~~~~~

Four bands in the map-creation pipeline: data collection by a survey vehicle,
automated processing (point-cloud registration and feature extraction),
**human annotation and verification**, then map creation and validation.

**The third band is the point.** A person checks every extracted feature
before it becomes map data. That step is why a mapped ODD grows city by city
rather than everywhere at once, and why the map is a standing cost rather
than a one-off build.


Data Rates
~~~~~~~~~~

.. list-table:: Uncompressed raw rates. Every one must be moved, timestamped and processed inside one frame period.
   :widths: 44 20 36
   :header-rows: 1

   * - **Source**
     - **Raw rate**
     - **Note**
   * - Camera 1280×720 RGB @ 30 Hz
     - 83 MB/s
     - The GP1 configuration
   * - Camera 1920×1080 RGB @ 30 Hz
     - 187 MB/s
     -
   * - Eight 1080p cameras @ 30 Hz
     - **1.5 GB/s**
     - A surround suite
   * - LiDAR 1.2 M points/s
     - 19 MB/s
     - 16 bytes per point
   * - LiDAR 2 M points/s
     - 32 MB/s
     -
   * - RADAR, a few hundred detections @ 20 Hz
     - 0.3 MB/s
     - Already an object list
   * - IMU @ 200 Hz
     - 0.01 MB/s
     - Negligible

**Cameras dominate by two orders of magnitude**, and that is before any
network runs on them. This is why RADAR ships an object list rather than raw
returns, why cameras are compressed or processed at the sensor, and why "just
add another camera" is a compute and thermal decision, not an optical one.


Keeping Sensors Usable
~~~~~~~~~~~~~~~~~~~~~~

Every specification in this lecture assumes a **clean aperture**. On a real
vehicle that aperture sits outdoors, often at bumper height, in whatever the
weather is doing.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: Contamination
      :class-header: bg-warning

      - Mud, salt spray, insects, road film.
      - Washers and wipers for camera and LiDAR apertures: a real fluid
        system, plumbed and refilled.
      - Heaters to clear ice and condensation.
      - Hydrophobic coatings to shed rain.

   .. grid-item-card:: Blockage detection
      :class-header: bg-info text-white

      - The system must notice it is blind. **An occluded camera returns a
        perfectly valid, perfectly useless image.**
      - Detected by loss of high-frequency content, static regions, or
        disagreement with the other sensors.
      - Response is the same ladder: warn, degrade, or MRC.

.. admonition:: The thesis of this lecture
   :class: danger

   **A dirty sensor does not report an error. It reports data.**

   Every failure mode in this lecture produces plausible output rather than
   an exception: glare, fog, matte black targets, zero-Doppler filtering,
   multipath, a one-degree extrinsic error, a millisecond of clock skew, a
   blocked lens. Not one of them raises.

   **The dangerous failures are the quiet ones.** That is why health
   monitoring and cross-validation are not optional extras.


Discussion 3 -- Spend the Budget
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You have **$5,000 per vehicle** for the whole sensor suite. Spend it, then
defend it.

.. list-table::
   :widths: 6 94
   :header-rows: 1

   * -
     - **Operational design domain**
   * - A
     - **Highway.** Divided motorway only, 60--130 km/h, all weather
       including rain and light snow, day and night. Hands-off but driver
       supervising. Long following distances, high closing speeds.
   * - B
     - **Urban.** City streets below 50 km/h, dense pedestrians and cyclists,
       frequent occlusion, parked cars either side, fair weather only,
       daylight only.

- State **what you cut** and what capability you lost with it.
- Name **one failure your suite does not cover**, and what you would tell the
  safety case about it.

.. dropdown:: Discussion 3 -- answers
   :color: success
   :icon: check-circle

   **A typical highway answer:** long-range RADAR around $2,000 (all-weather,
   high closing speed, direct velocity), telephoto camera $1,500
   (classification and signs at range), forward solid-state LiDAR $1,000 (the
   stationary-object cover RADAR cannot give), $500 of basic side sensing.
   360° is sacrificed, and that is defensible in a lane-keeping ODD.

   **A typical urban answer:** four corner RADARs $2,000 for genuine 360°,
   surround camera set $1,500 for classification and occlusion recovery, $500
   forward ADAS module for low-speed AEB. **LiDAR is cut entirely** to afford
   the coverage: at 50 km/h you need to see all around you far more than you
   need 200 m of range.

   **The point is the inversion.** Highway spends on range and weather; urban
   spends on coverage. Same money, opposite suite. Anyone who proposed one
   suite for both has not used the ODD.

   **On redundancy.** Most groups buy one of everything. What happens when
   the single forward camera is blinded? Did $5,000 give you complementarity,
   or a single point of failure with good specifications?

   **The last question matters most.** A team that says "we do not cover
   heavy snow, so the ODD excludes it and the system must detect snow and
   hand back" has understood L1 and L2 together. That is the answer to look
   for.


Why Fusion Works
----------------

A preview only. Enough to reason about placement, which is what this lecture
is for. The machinery is L3.

Three Relationships
~~~~~~~~~~~~~~~~~~~

.. list-table:: Luo's taxonomy. The third column is the one that changes where you bolt the sensor.
   :widths: 18 38 44
   :header-rows: 1

   * - **Relationship**
     - **What you get**
     - **Consequence for placement**
   * - Complementary
     - Different pieces of the puzzle. Camera classifies, LiDAR measures.
     - Fields of view must **overlap** wherever you need both properties at
       once.
   * - Competitive
     - The same information twice, for fault tolerance.
     - The two must **fail independently**; side-by-side mounting defeats the
       purpose.
   * - Cooperative
     - New information neither could produce alone, such as stereo depth.
     - **The geometry is the measurement:** the baseline sets the depth
       resolution.

.. important::

   Deliberately deferred to L3: fusion architectures (early, intermediate,
   late), inverse-variance weighting, the Kalman filter, EKF, UKF, particle
   filters, and data association.

   **You should not be able to fuse anything after today. You should be able
   to place sensors so that fusion is possible.**


CARLA Hands-On
--------------

Back to where the evening started, but now you know what the numbers mean.

Sensor Exploration
~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 6 38 56
   :header-rows: 1

   * -
     - **Task**
     - **What it teaches**
   * - 1
     - Spawn a vehicle, attach RGB camera, LiDAR, RADAR, IMU and GNSS.
     - The blueprint library, attachment transforms, and that **a sensor pose
       is an extrinsic**.
   * - 2
     - Collect and visualise each stream.
     - Rates differ, timestamps matter, and the point cloud is much sparser
       far away than it looks.
   * - 3
     - **Project the LiDAR points onto the camera image.**
     - The whole calibration section, executed. Includes the axis
       permutation.

.. important::

   **In class you watch. These three are your own work afterwards, and the
   practice for GP1.**

   - **Tasks 1 and 2 come with a script**, ``demo2_spawn_suite.py`` from
     Demo 2. Read it and change the mounting numbers.
   - **Task 3 has no script, deliberately.** It is GP1's core, and the axis
     permutation only teaches you something if you get it wrong yourself
     first. The chain is in :ref:`l2-gp1-chain`.

CARLA gives **exact** extrinsics, so Task 3 isolates the maths from
calibration error. GP1 then adds noise, and a real vehicle gives you neither
exact extrinsics nor a ground truth.

GP1's **depth** and **semseg** cameras are *ground truth*, not sensors. Check
your work with them, never depend on them.


Next Class
----------

**L3: Probabilistic State Estimation & Fusion**

- Fusion architectures: early, intermediate, late
- Uncertainty, and why inverse-variance weighting is the right average
- The Kalman filter, built from first principles, then EKF and UKF
- Data association: which measurement belongs to which track

**Before next class**

- The **setup milestone** is due, and **teams form**. **GP1 is posted.**
- Complete the CARLA sensor exercise from today. **Task 3 is the one that
  matters.**
- Read the `CARLA Sensor Reference
  <https://carla.readthedocs.io/en/0.9.16/ref_sensors/>`_.

**The through-line:** L1 gave you the vocabulary and the failures, L2 gave you
the sensors and the geometry that relates them, L3 gives you the filter that
combines them. Everything you calibrate today is what L3 fuses next week.
