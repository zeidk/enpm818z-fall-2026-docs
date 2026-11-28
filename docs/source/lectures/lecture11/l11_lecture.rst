====================================================
Lecture
====================================================

.. note::

   These notes follow the **interactive deck** of L11, the slides shown in
   class, with the same seven sections, the same parts and the same slide
   titles. You can read them at home. The deck links some slides to a
   **"More detail"** box on this page: a closed box right after the part it
   explains. Click its title to open it. Nothing in a "More detail" box is on
   the quiz.

   The hands-on commands are in the part "Hands-on code" of the section
   "Imitation Learning". The papers and pages behind these notes are on
   :doc:`the References page <l11_references>`, numbered as in the deck.

   You can also try the slides: :doc:`the interactive slides <l11_interactive>`
   run in your browser.


.. _l11-lec-introduction:

Introduction
------------

An automated driving system (ADS) is built in one of two ways: a modular stack
of parts that people design and test one at a time, like your GP1 to GP4
stack, or one end-to-end network trained from data. Companies use one, the
other, or a hybrid of both. This lecture shows how an end-to-end driver
learns, why it fails, and how to compare the two designs.

Who builds which design
~~~~~~~~~~~~~~~~~~~~~~~

An ADS is built as a modular stack, as one end-to-end network, or as a hybrid
of the two. Companies have chosen differently.

- **Modular stack.** People design each part and test it on its own:
  perception, localization, planning, control. Your GP1 to GP4 stack is one.
  Two open-source stacks: Autoware, "a layered architecture that clarifies
  the role of each module" (Autoware Foundation, Architecture 1.0), and Baidu's
  Apollo, which documents each module, from perception to control (Baidu
  Apollo, README).
- **End-to-end.** One network from sensors to driving. Tesla says it uses
  "end-to-end neural networks" (Tesla, 2024). Wayve, led by Alex Kendall,
  sells end-to-end driving (Kendall, 2025).
- **Hybrid.** Large learned models inside a structure that people designed.
  Waymo builds its driver this way, with a few specialized models instead of
  one network (Waymo, 2026).

.. dropdown:: More detail: Waymo's driver, box by box
   :class-container: more-detail
   :icon: info
   :name: l11-more-waymo-hybrid

   All quotes are from Waymo's post (Waymo, 2026).

   - **Cameras, lidar, radar, HD map:** what the driver reads; the HD map
     counts as one more input.
   - **Waymo Foundation Model** (learned): one large model that drives,
     "thinking fast and slow".

     - **Fast:** turns the sensor data into "instantaneous, real-time
       control".
     - **Slow:** a vision-language model (VLM), a network that reads images
       and answers in words. It reasons about rare scenes, such as a police
       officer's hand signals, but is "too slow for real-time control".

   - **A proposed trajectory:** the path the AV plans to drive.
   - **Validation layer:** a separate, AI-based system that checks every
     proposed path "against hard physics-based constraints and traffic laws".
     It is "a hard backstop".
   - **Driving decisions:** what the car does.

   Waymo adds the check because a pure end-to-end network risks "black box
   failures".

This lecture builds the end-to-end side, then compares it with the stack you
know.

The Modular and the End-to-End Driver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A modular driver splits driving into parts that people design and test one at a time: perception, localization, planning, control. An end-to-end driver gives the whole job to one neural network trained from data, from the sensors to a trajectory or to commands. The difference is who decides what passes between the steps: people, or the training.

End-to-end learning
^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: End-to-end learning
   :class: note

   "End-to-end learning refers to training a possibly complex learning system
   by applying gradient-based learning to the system as a whole" (Glasmachers,
   2017).

Four fields use it. In each, one neural network goes from the raw input to
the final output and skips a step that people used to design:

.. list-table::
   :header-rows: 1
   :widths: 16 10 74
   :class: compact-table

   * - Field
     - Year
     - What the one network does
   * - Speech
     - 2014
     - Audio to text, "without requiring an intermediate phonetic
       representation" (Graves and Jaitly, 2014).
   * - Translation
     - 2014
     - An English sentence to a French one: "a general end-to-end approach to
       sequence learning" (Sutskever, Vinyals and Le, 2014).
   * - Robot arms
     - 2016
     - Camera images to motor torques, such as "screwing a cap onto a
       bottle" (Levine et al., 2016).
   * - Driving
     - 2016
     - Camera pixels to steering commands (NVIDIA; Bojarski et al., 2016).
       This is today's topic.

End-to-end driving, defined
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: End-to-end driving
   :class: note

   "We define end-to-end autonomous driving systems as fully differentiable
   programs that take raw sensor data as input and produce a plan and/or
   low-level control actions as output" (Chen et al., 2024).

- **Differentiable** means every part can be trained together, from the
  error at the output back to the sensors.
- **In your stack,** people chose what flows between the parts (boxes, a
  pose, a route) and tuned each part on its own score: detection on mAP
  (mean average precision), and the EKF (the Kalman filter that estimates
  the AV's pose) on its error.
- **In an end-to-end driver,** the network chooses what flows inside it, and
  one score at the output trains it all.

.. dropdown:: More detail: the modular pipeline each field used before
   :class-container: more-detail
   :icon: info
   :name: l11-more-modular-before

   In each of the four fields, a chain of designed steps came first. The
   slide's hover cards draw the chain and quote the paper that names it.

   - **Speech.** Audio, then feature extraction (mel-scale filterbanks), then a
     neural network that classifies each frame, then a hidden Markov model with
     a pronunciation dictionary (words to phonemes), then text. Before
     end-to-end learning, the neural network was "only a single component in a
     complex pipeline" (Graves and Jaitly, 2014).
   - **Translation.** A sentence in one language, split into phrases, each
     phrase translated (a phrase table), the phrases reordered, then a language
     model and a decoder pick the best sentence in the other language.
     Sutskever et al. compare with "a phrase-based SMT system" (Sutskever,
     Vinyals and Le, 2014). In such a system, "the foreign input sentence is
     segmented into a sequence of phrases"; "Each foreign phrase is translated
     into an English phrase. The English phrases may be reordered" (Koehn, Och
     and Marcu, 2003).
   - **Robot arms.** Camera images, then perception (a vision pipeline), state
     estimation, the policy, and a hand-designed controller such as a PD
     controller, then motor torques. Practical policy search "often
     require[s] hand-engineered components for perception, state estimation,
     and low-level control" (Levine et al., 2016).
   - **Driving.** A camera image, then lane marking detection, path planning
     and control, then steering. NVIDIA contrasts its network with an
     "explicit decomposition of the problem, such as lane marking detection,
     path planning, and control" (Bojarski et al., 2016). Your GP1 to GP4
     stack is a larger one.

The modular driver
^^^^^^^^^^^^^^^^^^

People build and test each of the five steps one at a time:

1. **Image and points:** the camera image and the LiDAR points.
2. **Objects:** what the detector and the tracker find.
3. **Pose and map:** where the AV is, and the objects on the map.
4. **Trajectory:** the path the planner chooses.
5. **Commands:** steering, throttle and brake.

You built this stack in GP1 to GP4. Each arrow between two steps carries
something that a person chose.

The end-to-end driver
^^^^^^^^^^^^^^^^^^^^^


.. figure:: /_static/images/L11/l11_nvidia_network.png
   :class: white-figure
   :alt: NVIDIA's network from left to right, with steering as its only output. A camera image of 3 planes of 66 by 200, a sketch of a road seen from a front camera: sky, green grass, trees and a building at the side, a gray road with white lane lines, two vehicles ahead with red rear lights and a small person near the road; the next plane covers part of it. A normalization layer. Five convolutional layers, drawn as shrinking green blocks: 5 by 5 with 24@31 by 98, 5 by 5 with 36@14 by 47, 5 by 5 with 48@5 by 22, 3 by 3 with 64@3 by 20, and 3 by 3 with 64@1 by 18. A flatten layer of 1164 numbers. Three fully connected layers, drawn as thin blue slabs: 100, 50 and 10. One output value in red, steering: 1 divided by the turning radius.
   :width: 85%
   :align: center

   NVIDIA's network of 2016: camera pixels in, steering out.

.. admonition:: Reading the figure
   :class: tip

   - **Camera image and normalization:** the input, 3 planes of 66 by 200 pixels, drawn as a sketch of the lecture's road seen from the AV's front camera (the same scene as the slide's top view: a car ahead, a car in the left lane, a pedestrian on the right sidewalk), and its normalization layer. The next plane covers part of the sketch.
   - **Five convolutional layers (green):** they find features. Each block is smaller than the one before.
   - **Flatten, then three fully connected layers (blue):** 1164 numbers, then 100, 50 and 10.
   - **Output (red):** one value, the steering, written as 1 divided by the turning radius.
   - The blocks are drawn to show the trend in layer size, not to scale.

One neural network goes from the sensors to a trajectory or to commands, with
no designed step between. Each new camera image goes into the one neural
network, and a new trajectory or new commands come out. No step in between
was designed by people.

The slide also shows a road scene with a pedestrian. In its third step, when
the one network's commands come out, the AV steers 0.7 m to the left, and it
stays there until the camera no longer sees the pedestrian. In the Sensors
step the slide shows the camera image.

NVIDIA's network of 2016 is an example: camera pixels in, steering out. It
has 9 layers: a normalization layer, 5 convolutional layers and 3 fully
connected layers. The authors give "about 27 million connections and 250
thousand parameters" (Bojarski et al., 2016). The slide draws each layer as a
box sized by the layer's size, to show the trend and not to scale.

Inside a Tesla Model 3
^^^^^^^^^^^^^^^^^^^^^^


.. figure:: /_static/images/L11/l11_tesla_inside.png
   :class: white-figure
   :alt: A see-through 3D Tesla Model 3 seen from a three-quarter view, at rest. Teal blocks mark the sensors: three at the top of the windshield, one in each door pillar and each front fender, one at the rear and one behind the front bumper. Dark numbered tags stand on gray blocks inside the car: 2 on the computer behind the glovebox, 3 on the high voltage battery under the floor, 4 on the rear drive unit, 5 on the front drive unit and 6 on the 12 V battery under the hood. At the bottom left, a label reads 1 Sensors.
   :width: 80%
   :align: center

   A Tesla Model 3 seen from inside.

.. admonition:: Reading the figure
   :class: tip

   - **Teal blocks:** the sensors, tag 1 below.
   - **Tags 2 to 6:** the car computer, the high voltage battery, the rear drive unit, the front drive unit and the 12 V battery, as the list below names them.
   - The slide is a 3D view you can turn. This picture is its first view, before any click.

Tesla says it uses "end-to-end neural networks" (Tesla, 2024). Waymo sits
between the two designs: it describes "fewer, high-capacity, specialized
foundation models", not "a single, black box" (Waymo, 2026).

The slide shows a see-through 3D Model 3 that you can turn, seen from the
side, from above or from three quarters. It is scaled to Tesla's wheelbase
(Tesla, Model 3 Owner's Manual); the places of the parts are drawn by eye.
Six tags mark what is inside:

1. **The sensors:** eight cameras, and a radar on some cars (Tesla, Model 3
   Owner's Manual). Three cameras "are mounted to the windshield above the
   rear view mirror", "a camera is mounted in each door pillar" and "to each
   front fender", one "above the rear license plate". The radar ("if
   equipped") "is mounted behind the front bumper".
2. **The car computer,** bolted to the bulkhead behind the glovebox (Tesla,
   Model 3 Service Manual). Tesla, 2019: the onboard computer "runs the new
   Tesla-developed neural net for vision, sonar and radar processing
   software" (Tesla, Autopilot, 2019).
3. **The high voltage battery** "is located under the floor pan. A large
   section of the undercarriage houses the high voltage battery" (Tesla,
   Emergency Response Guide).
4. **The rear drive unit** "is located between the rear wheels". It turns the
   battery's direct current into the alternating current "that the drive
   units use to power the wheels" (Tesla, Emergency Response Guide).
5. **The front drive unit, on dual motor cars.** It ("if equipped- Dual Motor
   vehicles only") "is located between the front wheels" (Tesla, Emergency
   Response Guide).
6. **The 12 V battery** "is located under the hood and the plastic access
   panel". It runs the airbags, windows, door locks, touchscreen and lights
   (Tesla, Emergency Response Guide).

The Model 3's eight cameras
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each camera looks its own way and reaches its own distance. The table gives
the maximum distance as Tesla's 2019 page lists it, and the field of view
(FOV) when that page gives one: it gives two angles only. "n/a" means the
page gives none.

.. list-table::
   :header-rows: 1
   :widths: 40 30 30
   :class: compact-table

   * - Camera or sensor
     - Max. distance (m)
     - FOV
   * - Narrow forward
     - 250
     - n/a
   * - Main forward
     - 150
     - n/a
   * - Wide forward
     - 60
     - 120°
   * - Forward looking side
     - 80
     - 90°
   * - Rearward looking side
     - 100
     - n/a
   * - Rear
     - 50
     - n/a
   * - Radar (some cars)
     - 160
     - n/a

The places come from the owner's manual (Tesla, Model 3 Owner's Manual) and
the distances and the two angles from Tesla's 2019 page (Tesla, Autopilot,
2019). The slide draws the directions, the camera order and the other angles
by eye, and its arrows and wedges are not to scale.

What End-to-End Gains
~~~~~~~~~~~~~~~~~~~~~

An end-to-end driver is trained as a whole, from the sensors to the output. A 2024 survey lists what that gains over a modular stack; each gain has a price, which the lecture weighs once the clone has shown it.

Gain 1: one goal for all parts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In a modular stack, each part is trained for its own goal: the detector is
scored on mAP, and the planner aims for safe, comfortable driving.
End-to-end, every part, including the features it passes on, is trained for
one goal: driving well. NVIDIA saw it: trained on steering alone, its network
found road features, though "We never explicitly trained it to detect, for
example, the outline of roads" (Bojarski et al., 2016).

Gain 2: no information lost
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In a modular stack, each part passes on only the few things it chose, so a
mistake early on carries through every later part. An object the detector
misses never reaches the planner. End-to-end, no person picks what passes
between the steps. Each layer hands the next one all its learned features:
many numbers that describe the whole scene, not a short list of objects. A
pedestrian that a separate detector would miss is still in those numbers, so
it can still shape the plan.

Gain 3: less computing
^^^^^^^^^^^^^^^^^^^^^^

In a modular stack, each task, for example finding cars, finding lanes and
reading signs, has its own feature extractor: the part of a network that
turns the camera image into features, patterns such as edges and shapes.
Three tasks run three extractors on the same image, so the same kind of work
is done three times. End-to-end, one shared extractor turns the camera image
into features once, and all three tasks read those same features. The
extractor runs one time instead of three, so the car computes less.

Gain 4: better with more data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The whole driver is one network trained on driving data. Training it on more
driving, on more roads and in more weather and traffic, may make it drive
better. This is a hope, not a measured result: no amount of data covers every
situation, and collecting it costs time and money. Alex Kendall, CEO of Wayve,
makes the same point: with unlimited data, "this is really just a lookup data
table", and "that's not economically or technically feasible" (Kendall, 2025).

Ways to Learn a Driver
~~~~~~~~~~~~~~~~~~~~~~

A network that drives has to be trained. It can copy an expert's driving, or learn by trial from a reward, and the field sorts its methods into these two branches.

Expert, defined
^^^^^^^^^^^^^^^

.. admonition:: Definition: Expert
   :class: note

   The driver whose behavior a learner imitates: its demonstrations show the
   desired behavior. "The purpose of imitation learning is to efficiently
   learn a desired behavior by imitating an expert's behavior" (Osa et al.,
   2018).

Three kinds of expert appear in this lecture:

- **A person.** "In many cases, the experts are human operators" (Osa et
  al., 2018). NVIDIA recorded its human drivers on a real car (Bojarski et
  al., 2016).
- **A program.** Our lap's expert is a controller that reads the true
  offset: privileged information, known only to the simulator.
- **A trained driver.** Roach's expert is "a reinforcement learning expert
  that maps bird's-eye view images to continuous low-level actions" (Zhang et
  al., 2021).

What an expert gives:

- **It drives well.** Methods that learn a cost assume "the demonstrations
  are (approximately) optimal" (Osa et al., 2018).
- **Its demonstrations never cover everything:** "collecting expert
  demonstrations to cover all situations is usually too expensive and
  time-consuming" (Osa et al., 2018). Section "Imitation Learning" shows what
  that gap does to the clone.

Two ways to learn a driver
^^^^^^^^^^^^^^^^^^^^^^^^^^

A driver can copy an expert, or learn from a reward. Chen et al. sort more
than 270 papers into imitation learning (IL) and reinforcement learning (RL)
(Chen et al., 2024). The map has two branches, and each points to the
section that covers it. A box on the slide takes you to that section:

- **Imitation learning (IL):** learn from an expert's demonstrations.

  - **Behavior cloning** "reduces the problem to supervised learning" (Chen
    et al., 2024). Section "Imitation Learning".
  - **Inverse optimal control** uses "expert demonstrations to learn a reward
    function" (Chen et al., 2024). Section "Imitation Learning", Part 7.

- **Reinforcement learning (RL):** learn from a reward, by trial, with no
  expert to copy. An RL driver has run on a real car. Section
  "Reinforcement Learning".

What the network outputs: "planned trajectories or control signals" (Chen et
al., 2024). A trajectory still has to become steering and throttle: that
"needs additional controllers" (Chen et al., 2024).

The Running Example
~~~~~~~~~~~~~~~~~~~

Ideas about learning to drive are easiest to test on a small case where everything is known: one lap of Town01, an expert that keeps the AV in its lane, and a clone that learns from the expert's recording.

One lap, one expert, one clone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Today's running example is small on purpose, so that everything in it can be
measured. It is one lap of CARLA's Town01, driven by an expert and by a
clone.

1. **The road:** one lap of CARLA's Town01, read from its map. GP4 drives
   Town01 too.
2. **The expert:** keeps the AV in its lane. It sees where the AV really is.
3. **The clone:** learns from a recording of the expert, then drives alone.
   It sees what a noisy lane detector reports.
4. **What is measured:** how often each one finishes the lap on 20 test laps, and
   why the clone does not.

A **training run** is one recording of the expert and the clone trained on it.
The notes follow run 6, and compare it with nine other runs in the part
"DAgger" of "Fixing the Clone". Test lap 18 shows the failure: 649 m after
the start, the clone's right wheels reach the lane line. From there the lap counts
as not finished (red ring on the slide). Why it drifts is the subject of "Why the
Clone Fails".

Everything runs in numpy on a laptop, with no CARLA server: the hands-on
script ``l11_handson.py`` reproduces the lap, fit, error and DAgger numbers
on this page.

Terms used in this lecture
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 24 76
   :class: compact-table

   * - Term
     - Meaning
   * - Policy
     - A rule from what the car senses (its observation) to what it does (its
       action).
   * - Expert
     - The driver whose actions are copied: a person, or a program that reads
       the true state from the simulator (the ground truth).
   * - Clone
     - The learned policy, trained to copy the expert.
   * - State
     - Where the car is and how it moves: on our lap, its place on the lap
       (which sets the curve ahead), its offset from the lane center, its
       heading error.
   * - Open loop
     - Scoring on recorded inputs: the policy's output never moves the car.
   * - Closed loop
     - Scoring by driving: the policy's output moves the car, and the new
       state is its next input.
   * - Waypoints
     - A few future positions of the car, which a controller then follows.
   * - Privileged information
     - What only the simulator knows, such as the true state of every car and
       lane.

Learning objectives
^^^^^^^^^^^^^^^^^^^

Six steps tell one story: the two designs, how to learn one, what is inside
it, how to score it, and how to choose. After this lecture, you can:

1. **Introduction.** Compare a **modular** driver, built from parts that
   people design, with an **end-to-end** driver, one network trained from
   data, and say which companies use which.
2. **Imitation learning.** Train a network by **behavior cloning**, which is
   supervised learning on an expert's driving, then score it, see why it
   fails and fix it. Then place cost learning and a model of the world beside
   it. Four steps:

   - **Train the clone.** Fit it to one recorded lap of the expert's driving.
   - **Score the clone.** On recorded data (**open loop**), and by letting it
     drive (**closed loop**).
   - **Why the clone fails.** Three reasons: **compounding error**,
     **causal confusion** and **averaging**.
   - **Fixing the clone.** The fixes, mainly **DAgger** and the route's
     **command** at a junction.

3. **Reinforcement learning.** Place **reinforcement learning**, learning from
   a reward with no expert to copy, beside imitation.
4. **Inside the networks.** Read published drivers such as **TransFuser** and
   **UniAD**, and driving **VLA models**.
5. **Scoring a driver.** Tell **open-loop** from **closed-loop** evaluation,
   and read the benchmarks that score drivers in closed loop.
6. **Modular or end-to-end?** Weigh what end-to-end costs, and compare the two
   kinds of driver fairly.


.. _l11-lec-imitation-learning:

Imitation Learning
------------------

Imitation learning trains a driver from an expert's demonstrations. This
section trains the clone by **behavior cloning**, copying the expert's actions,
then scores it, shows why it fails and how to fix it, and ends with two other
ways to learn from the same demonstrations.

.. admonition:: Definition: Imitation learning
   :class: note

   Learning a policy from an expert's demonstrations, the recorded examples of
   the expert doing the task. Osa et al.: "Imitation learning is a class of
   methods that reproduces desired behavior based on expert demonstrations"
   (Osa et al., 2018).

- **Behavior cloning is one kind of imitation learning.** It copies the
  expert's actions by supervised learning: each recorded input is paired with
  the expert's action.
- **The other kind learns the reward first.** "BC and IRL form two major
  classes of imitation learning methods" (Osa et al., 2018); IRL is inverse
  reinforcement learning.
- **This section uses behavior cloning** to train the clone on our lap.

The imitation learning family
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Osa et al. split imitation learning into two branches, then split each branch
by whether it uses a model of the dynamics, how the state changes after an
action (Osa et al., 2018). The quotes in this list are
from that survey unless another source is named.

- **Imitation learning:** learn from an expert. It "reproduces desired
  behavior based on expert demonstrations". Its two branches: copy the
  expert's actions, or recover the reward behind them.

  - **Behavior cloning:** learn the action directly. It learns "a policy that
    directly maps from the input to the action/trajectory", by supervised
    learning. The survey says behavioral cloning. Our clone learns this way.

    - **Model-free:** no model of the dynamics. These methods learn the policy
      "without learning/estimating system dynamics nor recovering the reward
      function". The survey lists the ALVINN (1988) and DAgger (2011) papers
      here. Our clone and DAgger (:ref:`l11-lec-fixing`) are model-free.
    - **Model-based:** uses the dynamics. These methods "learn a policy using
      information about the system dynamics": how the state changes after an
      action. MILE (:ref:`l11-lec-beyond-bc`) is "a Model-based Imitation
      LEarning approach" (Hu et al., 2022).

  - **Inverse reinforcement learning:** learn the reward, then the action. It
    recovers the reward from demonstrations assumed "(approximately) optimal",
    then finds the policy that maximizes it. It is also called inverse optimal
    control; cost learning (:ref:`l11-lec-beyond-bc`) is on this branch (Chen et
    al., 2024).

    - **Model-free:** these methods "do not require prior knowledge of the
      system dynamics". They update the reward and the policy "using
      sampling-based methods".
    - **Model-based:** these methods "assume that the dynamics of the system,
      e.g. state transition probabilities, are known". The survey's Table 2.2:
      "model-based methods are dominant in inverse reinforcement learning".

**To learn more:** Osa et al., *An Algorithmic Perspective on Imitation
Learning*, 2018, free on `arXiv <https://arxiv.org/abs/1811.06711>`__. Chapter
2 sorts the methods as this tree does; Chapter 3 covers behavior cloning,
DAgger included.

The Expert and Its Recording
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Behavior cloning learns a driving policy from an expert's recorded examples. Who the expert is, and what each recorded example holds, decide what the clone can learn.

Behavior cloning
^^^^^^^^^^^^^^^^

.. admonition:: Definition: Behavior cloning
   :class: note

   Learning a driving policy from an expert's recorded examples by supervised
   learning: each example pairs what the expert saw with what the expert did,
   and the policy is trained to give the expert's action for the expert's
   input. A **policy** is a rule from what the AV sees to what it does.

The idea is old:

- **1988, ALVINN:** a neural network that "takes images from a camera and a
  laser range finder as input and produces as output the direction the
  vehicle should travel". It was trained on simulated road images (Pomerleau,
  1988).
- **2016, NVIDIA:** "We trained a convolutional neural network (CNN) to map
  raw pixels from a single front-facing camera directly to steering
  commands", from about 72 hours of driving (Bojarski et al., 2016).

ALVINN, NVIDIA's network and our clone all learn the same way: record an
expert, then fit a policy from what it saw to what it did. Our clone trains in
simulation, as ALVINN did, and outputs a steering command, as NVIDIA's network
does.

.. list-table::
   :header-rows: 1
   :widths: 14 22 22 20 22

   * -
     - Training data
     - Input
     - Policy
     - Output
   * - ALVINN, 1988
     - simulated road images
     - a camera and a laser range finder
     - a neural network
     - the direction to travel
   * - Our clone
     - a simulated lap, with a program as the expert
     - offset, heading and curvature ahead
     - a linear policy with four weights
     - a steering angle
   * - NVIDIA, 2016
     - human drivers, about 72 hours
     - one front camera
     - a convolutional neural network
     - a steering command (1/r)

Who the expert is
^^^^^^^^^^^^^^^^^

In our example the expert is a program. On real roads, as in NVIDIA's 2016
work, it is a human driver. The table compares the two.

.. list-table::
   :header-rows: 1
   :widths: 20 38 42
   :class: compact-table

   * -
     - Our example
     - NVIDIA, 2016 (Bojarski et al., 2016)
   * - Who drives
     - a program we wrote, not CARLA's autopilot
     - human drivers, told to "drive as they usually do"
   * - What it reads
     - the true offset and heading (simulator only)
     - the road, through the windshield
   * - Which car
     - the same simulated AV
     - "a 2016 Lincoln MKZ" or "a 2013 Ford Focus with cameras placed in
       similar positions"
   * - How its action is kept
     - stored at every step
     - steering from the CAN bus, "captured simultaneously" with time-stamped
       video

One dataset from two cars
^^^^^^^^^^^^^^^^^^^^^^^^^

NVIDIA recorded its drivers on a Lincoln MKZ and a Ford Focus. One network
learned from both, so neither its input nor its label may depend on which car
recorded it (Bojarski et al., 2016).

- **The input, the camera image.** The Focus had "cameras placed in similar
  positions to those in the Lincoln", so both cars record the same view of the
  road.
- **The label, the steering.** It is stored "as 1/r where r is the turning
  radius in meters": how tightly the path curves, not how far the wheels turn.
  On the same curve, two cars turn their wheels by different angles, but r is
  the same. NVIDIA: "to make our system independent of the car geometry".
- **Why 1/r, not r.** Driving straight, r is infinite and 1/r is 0: "to
  prevent a singularity when driving straight".

For example, on a curve of radius 20 m, a car with a 2.6 m wheelbase turns its
wheels atan(2.6 / 20) = 7.4° and a car with a 3.0 m wheelbase atan(3.0 / 20) =
8.5° (wheelbases chosen for this example). Both record 1/r = 0.050 per meter.

Recording a human expert
^^^^^^^^^^^^^^^^^^^^^^^^


.. figure:: /_static/images/L11/l11_nvidia_collect.png
   :class: white-figure
   :alt: A block diagram. A steering wheel box, human driver, points down to a box CAN bus: steering as 1/r. Three camera boxes in a row, left, center and right, point down to a wide box NVIDIA DRIVE PX: video and steering, time-stamped. The CAN bus box points right into the DRIVE PX box, and the DRIVE PX box points right to a small box, solid-state drive.
   :width: 90%
   :align: center

   NVIDIA's recording setup.

.. admonition:: Reading the figure
   :class: tip

   - **Top row:** the human driver's steering wheel and the left, center and right cameras.
   - **CAN bus:** carries the steering, stored as 1/r.
   - **NVIDIA DRIVE PX:** stores the time-stamped video and steering on a solid-state drive.

NVIDIA recorded its human drivers on a real car. Three cameras (left, center
and right) and the steering all feed one recorder, so the video and the
steering are captured together (Bojarski et al., 2016). The steering comes
from the CAN bus as 1/r, and the NVIDIA DRIVE PX stores the time-stamped video
and steering on a solid-state drive.

NVIDIA's expert is a human driver, so its recording pairs the camera video
with the driver's steering. Our lap's expert is a program, and its recording
is a table.

What the recording holds
^^^^^^^^^^^^^^^^^^^^^^^^

The recording holds one row every 0.05 s. The full lap has 3607 rows. Here are
three rows of run 6's recording (offset: plus is to the left):

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Time (s)
     - Along the lap (m)
     - Offset seen (m)
     - Heading seen (°)
     - Curvature ahead (1/m)
     - Expert's steering (°)
   * - 13.40
     - 107.2
     - −0.147
     - −0.02
     - 0.0020
     - 0.30
   * - 15.20
     - 121.9
     - 0.762
     - −0.91
     - 0.0969
     - 14.89
   * - 25.00
     - 200.5
     - −0.267
     - 0.50
     - 0.0000
     - −0.15

- **Input:** the three numbers the detector and the map give (offset seen,
  heading seen, curvature ahead).
- **Label:** the expert's steering. Time and distance only say where the row
  is.
- In the hands-on code, each column is one numpy array. Nothing is written to a
  file.

NVIDIA's rows are "single images sampled from the video, paired with the
corresponding steering command (1/r)", sampled at 10 frames per second. Views
from a left and a right camera, with labels changed to "steer the vehicle
back", show the neural network off-center states (Bojarski et al., 2016).

Behavior cloning in four steps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L11/bc_steps.png
   :class: dark-light themed-L11
   :alt: Four boxes in a row joined by arrows. Step 1, outlined dark: the expert drives; we record. Step 2: pairs: what the AV saw, steering. Step 3: fit a policy: supervised learning. Step 4, outlined rust: the clone drives alone.
   :width: 100%
   :align: center

   Behavior cloning, from recording to driving.

.. admonition:: Reading the figure
   :class: tip

   - **Step 1:** the expert drives and the drive is recorded.
   - **Step 2:** each observation is paired with the steering the expert gave.
   - **Step 3:** a policy is fitted to those pairs, by supervised learning.
   - **Step 4:** the clone drives alone.

1. **Record the expert.** Every 0.05 s, it stores the observation and the
   expert's steering. Snapshot at 200 m: offset −0.27 m, heading +0.5°,
   curvature 0; steering −0.15°.
2. **Form the pairs.** Each sample becomes one row of the array X (offset,
   heading, curvature ahead, 1) and one entry of y (the expert's steering).
3. **Fit a policy.** The clone steers by

   .. math::

      \text{steering} = w_1 \cdot \text{offset} + w_2 \cdot \text{heading}
      + w_3 \cdot \text{curvature} + w_4 \cdot 1

   Least squares picks the weights closest to the expert's steering. The
   weight :math:`w_4` (the column of 1s) is a fixed offset.
4. **Deploy the clone.** It steers with no expert, so its own steering decides
   what it observes next.

Steps 1 to 3 are the same as training a detector: inputs, labels, a loss.
Step 4 is new. The trained policy's outputs move the AV, and the AV's new
position decides the next input. A detector's outputs never change its next
image.

The Lap and the Expert
~~~~~~~~~~~~~~~~~~~~~~

The expert is a controller with three terms: it steers for the curve ahead, then back to the lane center. Its road is one lap of Town01, read from the town's map.

One lap of Town01 is our road
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every drive in this lecture, the expert's and the clone's, is one lap of
CARLA's Town01.

.. figure:: /_static/images/L11/l11_lap.png
   :class: dark-light themed-L11
   :alt: A top view of CARLA Town01's lanes as light gray dots, with the outer loop drawn as a thick dark line, a rounded rectangle about 395 m wide and 330 m tall. A dot on the top side tagged S marks the start, with an arrow pointing left: the lap runs counterclockwise. The four corners are tagged 1 to 4, starting top left. A small square on the bottom side near x 325 m is tagged J.
   :width: 70%
   :align: center

   One lap of Town01's outer loop.

.. admonition:: Reading the figure
   :class: tip

   The axes are the map's x (east) and y (north), in meters.

   - **The thick dark line** is the lap. **S** is the start, and the arrow
     shows the direction: counterclockwise.
   - **Tags 1 to 4** are the four left turns, starting at the top left.
   - **J** is a junction on the lap that the part "Route Commands" uses.
   - **The light gray dots** are the other lanes of the town.

The lap is read from the town's map:

- one lap, counterclockwise from S, measured on the town's map: **1442.6 m**;
- four left turns, tagged 1 to 4; the sharpest has a radius of 9.8 m;
- at junction J, 769 m along the lap, the route can go left or straight;
- the lane is 4.0 m wide.

**Chosen for this example:** 8 m/s (about 29 km/h), 20 steps per second, an
AV 2.0 m wide with a 2.9 m wheelbase. Nothing here is measured from a real
car.

The lane and the sharpest turn, to scale
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A wheel leaves the lane when the AV's center is 1.0 m from the lane center,
and turn 1 needs 16.5° of steering.

1. The lane is 4.0 m wide and the AV 2.0 m wide (chosen), so a wheel leaves
   the lane when the AV's center is more than (4.0 − 2.0) / 2 = 1.0 m from
   the lane center.
2. Turn 1, the sharpest, has a radius of 9.8 m. The front wheels turn
   arctan(2.9 / 9.8) = 16.5°. The AV is 4.5 m long (chosen).

The expert's steering rule
^^^^^^^^^^^^^^^^^^^^^^^^^^

Two terms first. The **offset** is how far the AV's center is from the lane
center, with left positive. The **heading error** is the AV's angle to the
lane. The expert steers for the curve, then back to the lane center. Its rule
has three terms, with three numbers, all chosen for this example:

1. steer for the curve 2.4 m ahead (0.3 s at 8 m/s), as the road's curvature
   asks;
2. steer back 3.44° for every meter of offset;
3. steer back 0.80° for every degree of heading error.

The slide has sliders for the curve radius, the offset and the heading error.
In its example the road curves left at the sharpest turn, the AV is 0.5 m
left of the lane center and its heading error is 2°, so the wheel turns (left
positive) 16.5° − 1.72° − 1.60° = 13.17°. The slide adds the unrounded
values.

The expert's three terms, one at a time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each of the expert's three terms is drawn on its own. With the slide's chosen
values, a radius of 9.8 m, an offset of 1.0 m and a heading error of 5°:

1. **The curve term,** read 2.4 m ahead: arctan(2.9 / 9.8) = 16.5° left.
2. **The offset term,** 1.00 m left of the center: 3.44 × offset = 3.44°
   back to the right.
3. **The heading term,** 5.0° of heading error: 0.8 × error = 4.0° back to
   the right.

The slide's dashed line shows where the AV goes if it holds that steering for
13 m.

.. dropdown:: More detail: the AV's motion and the expert, as equations
   :class-container: more-detail
   :icon: info
   :name: l11-more-av-model

   **The state.** Three numbers describe the AV on the road: the distance
   along the lane :math:`s`, the offset :math:`e` (left positive) and the
   heading error :math:`\psi`. The other symbols are speed
   :math:`v` = 8 m/s, wheelbase :math:`L` = 2.9 m, the steering angle
   :math:`\delta`, the lane's curvature :math:`\kappa(s)` read from the map,
   and the time step :math:`\Delta t` = 0.05 s. Everything but
   :math:`\kappa` is chosen for this example.

   **The motion.** A kinematic bicycle model, written in lane coordinates:

   .. math::

      \dot s = \frac{v\cos\psi}{1 - \kappa e}, \qquad
      \dot e = v \sin\psi, \qquad
      \dot\psi = \frac{v}{L}\tan(\delta + g) - \kappa \dot s

   The term :math:`g` is the random push on the steering. It changes at
   every step: :math:`g \leftarrow a g + \sqrt{1 - a^2}\,\sigma_g\,\xi`, with
   :math:`a = e^{-\Delta t / 2\,\mathrm{s}}`, :math:`\sigma_g` = 0.4° and
   :math:`\xi` a new draw from a standard normal distribution (mean 0,
   spread 1).

   **The two drivers.**

   - The expert steers
     :math:`\delta^* = \arctan\!\big(L\,\kappa(s + 0.3\,v)\big) - 0.06\,e - 0.8\,\psi`.
     The first term steers for the curve 0.3 s ahead. The 0.06 rad per
     meter of offset is the 3.44° per meter on the slide
     (0.06 × 180 / π = 3.44).
   - The clone steers
     :math:`\delta = w_1 \hat e + w_2 \hat\psi + w_3 \kappa(s + 0.3\,v) + w_4`.
     It reads the lane detector's numbers, not the truth:
     :math:`\hat e = e + 0.35\,\xi_1` m and
     :math:`\hat\psi = \psi + 0.3^\circ\,\xi_2`, each with a new draw at every
     step. The weights :math:`w_1` to :math:`w_4` are set by training.

   **Two limits.** Steering is limited to ±30°, and a drive stops if the
   offset passes 1.6 m in either direction.

The expert drives a test lap
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L11/expert_drive.png
   :class: dark-light themed-L11
   :alt: The expert's offset in meters against the distance along the lap, 0 to 1443 m. Dashed gray lines at plus and minus 1.0 m mark where a wheel leaves the lane. The dark line stays between about minus 0.5 and plus 0.5 m, with a short swing at each of the four turns, tagged 1 to 4 above the plot.
   :width: 95%
   :align: center

   The expert's offset along the lap.

.. admonition:: Reading the figure
   :class: tip

   The horizontal axis is the distance driven along the lap. The vertical
   axis is the offset, left positive.

   - **The dark line** is the expert. It stays within about half a meter and
     swings a little at each turn, tagged **1** to **4** above the plot.
   - **The dashed gray lines** at plus and minus 1.0 m are where a wheel
     leaves the lane.

Every driver also gets a random push on the steering, like wind gusts or the
slope of the road (chosen: 0.4°). Measured on 20 test laps, the expert
finishes **all 20**, and its largest offset is 0.75 m. The slide has a player
that shows the expert's path on each test lap.

Training the Clone
~~~~~~~~~~~~~~~~~~

The clone sees the lane only through a noisy detector, never the true state. Training it is supervised learning: a least-squares fit on one recorded lap, whose weights can be set beside the expert's.

What the clone sees
^^^^^^^^^^^^^^^^^^^

The expert reads the true offset and heading, as a simulator's autopilot can.
This is **privileged information**: a state only the simulator knows. The
clone sees the lane through a noisy lane detector. The recorded noise is
scaled by σ, and 0.35 m is chosen:

.. list-table::
   :header-rows: 1
   :widths: 32 32 36
   :class: compact-table

   * - Input
     - The expert reads
     - The clone reads
   * - Offset
     - the truth
     - the truth ± 0.35 m
   * - Heading error
     - the truth
     - the truth ± 0.3°
   * - Curvature ahead
     - the map
     - the map

The sign ± is the noise's standard deviation, drawn again at every step. The
noise σ = 0.35 m is 2.3 times the 0.154 m spread of the true offset on the
whole lap (0.35 / 0.154 = 2.27).

Five readings of one true offset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The detector gives a different number on each of five steps in a row, for one
true offset. The noise slider sets how far the readings spread.

1. The expert reads the true offset, about −0.05 m.
2. The clone's detector reported −0.27, −0.06, 0.28, −0.23 and −0.05 m on
   five steps in a row (0.05 s apart, run 6, 200 m along the lap). The pale
   band on the slide is ± 0.35 m of the 1.0 m of room: 0.35 / 1.0 = 0.35.

Training the clone
^^^^^^^^^^^^^^^^^^

The clone is trained by least squares on one recorded lap: four weights
fitted to all the pairs.

1. **Record:** the expert drives one lap: 1442.6 / 8 = 180.33 s. At 20 steps
   per second, 180.33 × 20 = 3606.6, so the recording holds 3607 pairs.
2. **Each pair:** the three numbers the detector reported, and the steering
   the expert gave.
3. **Fit:** the policy is steering = :math:`w_1` · offset + :math:`w_2` ·
   heading + :math:`w_3` · curvature + :math:`w_4`. Choose the four weights
   so its steering is closest to the expert's over all pairs (least squares).

Three of the pairs:

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Pair
     - Offset seen (m)
     - Heading seen (°)
     - Curvature (1/m)
     - Steering (°)
   * - 1: a straight stretch, 200 m
     - −0.27
     - 0.50
     - 0.0000
     - −0.15
   * - 2: entering turn 1, 107 m
     - −0.15
     - −0.02
     - 0.0020
     - 0.30
   * - 3: in the middle of turn 1, 122 m
     - 0.76
     - −0.91
     - 0.0969
     - 14.89

This is supervised learning with a squared loss, like a detector's box
regression, but the solution has a closed form: no gradient descent.

.. dropdown:: More detail: the least-squares solution
   :class-container: more-detail
   :icon: info
   :name: l11-more-least-squares

   Stack the :math:`N` = 3607 pairs in a table :math:`X`. Row :math:`k` of
   :math:`X` holds the numbers the clone read at step :math:`k`,
   :math:`[\hat e_k,\ \hat\psi_k,\ \kappa_k,\ 1]`, and :math:`y_k` is the
   expert's steering at that step. The last number, 1, is the input of the
   constant weight :math:`w_4`. Behavior cloning chooses the weights
   :math:`w = (w_1, w_2, w_3, w_4)` with the smallest sum of squared
   differences:

   .. math::

      w = \arg\min_{w} \sum_{k=1}^{N} \big(x_k^\top w - y_k\big)^2
      \quad\Longrightarrow\quad
      X^\top X\, w = X^\top y .

   - **Four unknowns, four equations.** The call ``numpy.linalg.lstsq(X, y)``
     solves them.
   - **DAgger solves the same equations.** Only :math:`X` and :math:`y` grow:
     they gain the states the clone reached, with the expert's labels for
     them.
   - **A neural network** replaces :math:`x^\top w` with a deeper function,
     and the closed form with gradient descent. The loss is the same.

The clone's and expert's weights
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The clone's weights next to the expert's show what the fit learned. Each noise
level on the slide is its own training run, with the same seed. The deck's
clone has σ = 0.35.

.. list-table::
   :header-rows: 1
   :widths: 52 16 16 16
   :class: compact-table

   * - Weight on
     - Expert
     - Clone
     - Ratio
   * - offset (deg of steering per m)
     - 3.44
     - 0.38
     - 0.11
   * - heading error (deg per deg)
     - 0.80
     - 0.74
     - 0.93
   * - curvature ahead (m; the expert's is the 2.9 m wheelbase)
     - 2.9
     - 2.58
     - 0.89

The ratio is the clone's weight divided by the expert's. For the offset,
0.38 / 3.44 = 0.11. The weights are those of training run 6, trained at
detector noise 0.35 m. In the four-step equation they have signs and degrees:
:math:`w_3 = 2.58\,\text{m} \times 57.3 = 148^\circ\!\cdot\text{m}`.

The clone learned the curve and the heading nearly right, and the offset
**9 times too weak** (3.44 / 0.38 = 9.05): it barely steers back toward the
center. The part "Why the Weight Is Small" says why.

One state, two drivers
^^^^^^^^^^^^^^^^^^^^^^

Both drivers start in the same state, 0.50 m left of the lane center (chosen),
with no gusts and no detector noise, and drive 4 s. The expert steers back to
the center, and the clone's smaller offset weight leaves it off to the side.

1. **The expert** steers 0.50 × 3.44 = 1.72° right at the start, and is 0.02 m
   off the center after 4 s.
2. **The clone's** offset weight gives 0.19° (0.50 × 0.38), and its constant
   weight 0.12° the other way: 0.188° − 0.125° = 0.063°, about 0.06° right at
   the start. After 4 s it is 0.46 m off the center.

Scoring the Clone
~~~~~~~~~~~~~~~~~

Scored on the expert's recorded data, the clone looks good. Then it drives
alone, and a wheel leaves the lane.

Scored on Recorded Data
^^^^^^^^^^^^^^^^^^^^^^^

The clone is trained. First it is scored the way a detector is: on recorded
data, where its outputs never move the AV. Scored this way, open loop, the
clone looks good.

Scored on recorded data
"""""""""""""""""""""""

.. admonition:: Definition: Open-loop error
   :class: note

   The policy's error on recorded inputs: it reads each recorded input and its
   output is compared with the expert's. Its outputs never move the AV.

On a second recorded expert lap, not used for training:

- the clone's steering differs from the expert's by **0.37°** on average;
- the steering the AV needs in a turn of radius 9.8 m is about
  arctan(2.9 / 9.8) = 16.5°, and 0.37° is 2.2% of that (0.37 / 16.5 = 0.022).

The slide has a slider for the turn radius, which is chosen for this example.
The sharpest turn of the lap is 9.8 m.

Open loop on turn 1
"""""""""""""""""""

In open loop on turn 1, the clone's steering differs from the expert's by at
most 0.46° in each of four recorded states. On a second expert lap, not used
for training, in four recorded states on turn 1:

- the clone's steering differs from the expert's by 0.46°, 0.20°, 0.31° and
  0.36°: 0.33° on average. The whole lap averages 0.37°;
- the turn needs up to arctan(2.9 / 9.8) = 16.5° of steering;
- each AV on the slide is a recorded state: the clone's steering never moves
  it, and the next state is the recorded one.

The Clone Drives
^^^^^^^^^^^^^^^^

Open loop said the clone steers almost as the expert does. Now the clone
drives alone, closed loop, on the 20 test laps.

Closed-loop evaluation
""""""""""""""""""""""

.. admonition:: Definition: Closed-loop evaluation
   :class: note

   The policy drives: its outputs move the AV, and the AV's new state gives the
   next input. It is scored on what happens: route completed, collisions,
   rules broken.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40
   :class: compact-table

   * -
     - Open loop
     - Closed loop
   * - Next input
     - the recorded one
     - the result of the policy's own action
   * - Score
     - average error against the expert's output (steering in degrees, or
       distance in meters)
     - share of the route completed, infractions
   * - Needs
     - a dataset
     - a simulator, or a car
   * - Our clone
     - 0.37°
     - 5 laps of 20

Where the next input comes from
"""""""""""""""""""""""""""""""

Open loop and closed loop differ in one thing: where the policy's next input
comes from. In open loop the recorded input arrives whatever the policy said.
The policy's output is only compared with the expert's output, and it never
moves the AV. In closed loop the policy's output moves the AV, and the new
state is the next input.

Open loop and closed loop on turn 1
"""""""""""""""""""""""""""""""""""

An open-loop test never moves the AV; a closed-loop test does.

1. **Open loop:** each AV is a recorded state, and the clone's steering never
   moves it. The next state is the recorded one.
2. **Closed loop:** the clone's steering moves the AV, and where it ends up is
   the next input.

The slide draws the road straight, with offsets stretched two times and
vehicles to scale.

The clone drives
""""""""""""""""

.. figure:: /_static/images/L11/bc_drive.png
   :class: dark-light themed-L11
   :alt: Offset from lane center against distance along the lap, 0 to 1443 m. Dashed gray lines at plus and minus 1.0 m, tagged 1. A thin gray line, tagged 2, is the expert on the same test lap and stays within about 0.5 m. A rust line, tagged 3 beside its highest point near 1170 m, is the clone: it swings wider at each turn, drifts down to minus 1.0 m near 649 m, where a dark circle tagged 4 marks the first time a wheel leaves the lane, comes back, then drifts up to about plus 1.0 m near 1100 m and reaches plus 1.3 m at 1170 m.
   :width: 95%
   :align: center

   The clone's offset on one test lap.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** the dashed gray lines at plus and minus 1.0 m, where a wheel
     leaves the lane.
   - **Tag 2:** the expert on the same test lap, with the same gusts. It stays
     within about half a meter.
   - **Tag 3:** the clone, in rust. It swings wider than the expert at each
     turn and drifts. Its highest point, near 1170 m, reaches plus 1.3 m.
   - **Tag 4:** the dark circle near 649 m, the first time a wheel leaves the
     lane (the offset reaches minus 1.0 m).

The clone drives alone, and a wheel leaves the lane after 649 m.

Where the clone's wheel leaves the lane
"""""""""""""""""""""""""""""""""""""""

The wheel leaves the lane on a straight road, 649 m after the start. Stepping
back along the clone's path to that place:

- at 0 m before the place, the clone is 1.00 m right of the lane center
  (offset −1.00 m): its right wheels are on the lane line;
- the slide's rust line is its path over the 12 m before that place.

The clone on the 20 test laps
"""""""""""""""""""""""""""""

The clone drives all 20 test laps, and 15 of them end with a wheel leaving the
lane. It finishes **5**. On average it drives 56% of the lap before a wheel
leaves (a lap that finishes counts as 100%). Each test lap has new gusts and
new detector noise. Test lap 18, the lap on the earlier slides, is the median
of the 15 failures.

This is one training run, one recorded lap. Another recording gives another
count, and the part "DAgger" shows ten of them: they finish 2 to 9 laps of
20. A clone that was within 0.37° of the expert on recorded data finishes 5
laps of 20. That gap is what the next part explains.


Why the Clone Fails
~~~~~~~~~~~~~~~~~~~

Scoring the clone gave a driver that copies the expert within 0.37° and finishes only 5 of 20 laps. A clone that scores well on recorded data can fail on the road in three ways: its small errors compound, it learns the wrong cause, or it averages two right answers.

Where the Error Grows
^^^^^^^^^^^^^^^^^^^^^

The clone's steering error is not the same everywhere: it depends on how far the AV is from the lane center. Where the expert never drove, the recording has nothing to teach.

The clone's error grows with the offset
"""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/L11/error_vs_offset.png
   :class: dark-light themed-L11
   :alt: Bar chart. The average size of the clone's steering error, in degrees, for four ranges of how far the AV really is from the lane center: 0.00 to 0.25 m, 0.44; 0.25 to 0.50 m, 1.09; 0.50 to 0.75 m, 1.78; 0.75 to 1.00 m, 2.41.
   :width: 75%
   :align: center

   The clone's steering error against the AV's true offset.

.. admonition:: Reading the figure
   :class: tip

   Each bar groups the steps of the clone's 20 test laps by how far the AV
   really was from the lane center. Its height is the average size of the
   clone's steering error in those steps, in degrees.

   - **0.00 to 0.25 m:** 0.44°, over 27,755 steps.
   - **0.25 to 0.50 m:** 1.09°, over 22,078 steps.
   - **0.50 to 0.75 m:** 1.78°, over 14,719 steps.
   - **0.75 to 1.00 m:** 2.41°, over 5,884 steps.

The error is measured on the clone's 20 test laps. At every step, the
clone's steering is compared with what the expert would have steered in that
same state. Near the center the clone is off by 0.44°. At 0.75 m to 1.00 m,
it is off by 2.41°, 5.5 times more (2.41 / 0.44 = 5.48). The slide adds a
fifth bar, 3.16° for 1.00 m to 1.60 m (1,704 steps), as extra: beyond 1.0 m a
wheel is out of the lane.

How a small error compounds, drawn
""""""""""""""""""""""""""""""""""

Four starting offsets show the same result. If the AV holds the expert's
steering for 18 m, it comes back more than if it holds the clone's, which
steers back less. The slide draws four offsets, the middle of each range of
the last chart. The first: the AV is 0.125 m left of the center. The expert
steers 0.43° toward the center, the clone 0.01° away from the center: it
steers back less by the average error, 0.44°. Held for 18 m, the two paths end
0.43 m apart. These are four offsets, not one drive.

A small error, step by step
"""""""""""""""""""""""""""

1. Near the center the clone is off by 0.44°: it steers back too little, so a
   gust or a turn sends it farther out than the expert.
2. Farther out, the expert would steer back 3.44° per meter, the clone only
   0.38°: the error grows to 1.09° (0.25 to 0.50 m).
3. Farther out still, it grows again: 1.78°, then 2.41°.
4. Each step starts where the last one left the AV, so the errors add up
   instead of averaging out. A wheel leaves the lane.

The offsets on the slide are the middle of each range (chosen for this
sketch), along the road and not to scale.

Compounding error
"""""""""""""""""

.. admonition:: Definition: Compounding error
   :class: note

   The policy's own mistakes take it to states its training data did not
   cover, where it makes larger mistakes.

In open loop this cannot happen: the next input is the recorded one, whatever
the policy said. Closed loop, each step starts from where the last one left
the AV, so the errors add up. The errors on the last slide came from the
clone's own 20 test laps, not from the expert's recording.

Where the expert never drove
""""""""""""""""""""""""""""

.. figure:: /_static/images/L11/coverage.png
   :class: dark-light themed-L11
   :alt: Two histograms of the true offset from the lane center, from minus 1.6 to plus 1.6 m. Tagged 1, dark: the expert's recorded lap, a narrow peak around zero, almost all within plus or minus 0.3 m. Tagged 2, rust: the clone's 20 test laps, wide and flat, spread from about minus 1.4 to plus 1.4 m.
   :width: 75%
   :align: center

   Where the expert and the clone spend their time.

.. admonition:: Reading the figure
   :class: tip

   The horizontal axis is the true offset from the lane center (left
   positive). The vertical axis is the share of time steps, as a density.

   - **Tag 1, dark:** the expert's recorded lap, which is the training data.
     It is a narrow peak around zero.
   - **Tag 2, rust:** the clone on its 20 test laps. It is wide and flat.

The clone's test laps reach wide offsets, but the expert's recording stays
near the center. The slide's limit slider shows which offsets lie beyond a
limit. The expert's recording has a spread of 0.154 m and never passes 0.61 m.
Beyond ±0.6 m: the recording has 0.2% of its steps, the clone's test laps
21.5%. At 0.61 m the clone is at 20%: states with no example at all.

Where the expert's recording ends
"""""""""""""""""""""""""""""""""

The expert's recording covers only offsets within ±0.61 m of the lane center.
The clone drives at offsets the recording never shows, up to the 1.0 m where
a wheel leaves the lane. On the clone's 20 test laps it spends 20% of its
steps beyond 0.61 m. Inside the range the clone has examples; outside it, none.

Why the Weight Is Small
^^^^^^^^^^^^^^^^^^^^^^^

The clone's weight on the offset is 9 times too weak. The cause is the detector's noise, and more data does not remove it.

How big the noise is next to the lane
"""""""""""""""""""""""""""""""""""""

The detector's noise is wider than the spread of the real offset, so most of
what the detector reports is noise. Two spreads, in the recording of run 6:

1. the spread of the true offset in the recording: ±0.154 m;
2. the spread of the offset the detector reports: ±0.389 m.

The slide's bar compares the squares: 0.154 × 0.154 / (0.389 × 0.389) =
0.0237 / 0.1513 = 0.16, so about 16% of the spread the clone sees is real
offset, and 84% is everything else. The slider sets the noise; the deck's clone
has σ = 0.35 (chosen for this example), and each noise level is its own
training run.

Why the offset weight is small
""""""""""""""""""""""""""""""

.. figure:: /_static/images/L11/bc_fit.png
   :class: dark-light themed-L11
   :alt: Scatter plot of steering in degrees against the offset the detector reports, in meters, for the expert's lap on straight road. The gray points, tagged 3, form a flat cloud from about minus 1.2 to plus 1.3 m wide and about 2 degrees tall, with a few points higher up. A dark line, tagged 1, falls steeply from plus 4.5 degrees at minus 1.3 m to minus 4.5 at plus 1.3 m. A rust line, tagged 2, through the middle of the cloud is almost flat.
   :width: 75%
   :align: center

   The recorded pairs, the expert's rule and the clone's fit.

.. admonition:: Reading the figure
   :class: tip

   Each gray dot is one recorded pair on straight road: the offset the
   detector reported (horizontal) and the steering the expert gave (vertical).

   - **Tag 1, dark:** the expert's rule, 3.44° per meter. It falls steeply.
   - **Tag 2, rust:** the clone's fit, 0.38° per meter. It is almost flat.
   - **Tag 3:** the recorded pairs. They form a flat cloud.

The noise hides the offset, so the fit gives the offset a small weight.

1. The expert stays near the center: its true offset varies by 0.15 m
   (0.154 m).
2. The detector adds noise: 0.35 m is 2.3 times that (0.35 / 0.154 = 2.3).
3. So most of the spread in "offset seen" is noise, and the expert's steering
   does not follow noise. The cloud is flat, and a line fit to a flat cloud
   is flat.

The fitted weight is 0.38° per meter (the expert's is 3.44), and the clone
finishes 5 of 20 laps. Given these pairs, a flat line is the best fit.

.. dropdown:: More detail: how much the noise shrinks the weight, by hand
   :class-container: more-detail
   :icon: info
   :name: l11-more-noise-shrinks-weight

   Take one input :math:`x`, seen through noise :math:`n` that is
   independent of :math:`x`. Least squares on the noisy reading
   :math:`\hat x = x + n` shrinks the true slope by the share of the spread
   that is real:

   .. math::

      \text{factor} = \frac{\sigma_x^2}{\sigma_x^2 + \sigma_n^2}.

   **On the expert's lap (training run 6):**

   1. The true offset's spread is :math:`\sigma_x` = 0.154 m, measured on the
      recorded lap. The detector's noise is :math:`\sigma_n` = 0.35 m, chosen
      for this example.
   2. Factor: :math:`0.154^2 / (0.154^2 + 0.35^2) = 0.0237 / (0.0237 + 0.1225)
      = 0.162`.
   3. Predicted weight: 3.44 × 0.162 = 0.56° per meter.
   4. Fitted weight: 0.38° per meter. The one-input formula is a rough guide:
      the fit has four inputs, and on curves the heading and the curvature
      take part of the offset's share.

   **With a quieter detector of 0.117 m** (0.35 / 3, chosen for this
   example): :math:`0.0237 / (0.0237 + 0.0137) = 0.63`. Predicted weight:
   3.44 × 0.63 = 2.2° per meter. Fitted weight: 1.85°.

More data does not help
"""""""""""""""""""""""

Five times the data barely changes the weight or the laps finished, but a
detector three times quieter does. Each clone is trained on the same recorded
lap (training run 6) and tested on the same 20 laps:

.. list-table::
   :header-rows: 1
   :widths: 40 15 25 20
   :class: compact-table

   * - Training data
     - Pairs
     - Offset weight (deg/m)
     - Laps finished
   * - 1 expert lap, detector 0.35 m
     - 3607
     - 0.38
     - 5 of 20
   * - 5 expert laps, detector 0.35 m
     - 18,035
     - 0.42
     - 6 of 20
   * - 1 expert lap, detector 0.117 m
     - 3607
     - 1.85
     - 20 of 20

- Five times the data moves the weight from 0.38 to 0.42, and the laps from 5
  to 6. Ten training runs show that a new recording alone moves the count by
  several laps: 2 to 9 of 20. So 5 to 6 is not a change you can read.
- A detector three times quieter (0.35 / 3 = 0.117) lets the fit see the
  offset: the weight is 1.85° per meter (0.38 before) and 20 of 20 laps
  finish.

.. dropdown:: More detail: an early fix, add recoveries to the data
   :class-container: more-detail
   :icon: info
   :name: l11-more-early-fix

   If the expert never drifts, the data has no example of a recovery. Early
   work made the examples up: it showed the network drifted views, with the
   steering that corrects them.

   - **1990, Pomerleau:** "each original image is shifted and rotated in
     software to create 14 additional images". He wrote that "Using
     transformed training patterns allows the network to learn how to recover
     from driving errors" (Pomerleau, 1990).
   - **2016, NVIDIA:** "The network must learn how to recover from mistakes.
     Otherwise the car will slowly drift off the road." "Images for two
     specific off-center shifts can be obtained from the left and the right
     camera" (Bojarski et al., 2016).

   Both make up off-center states from the expert's own drive. The label for
   a shifted view must be made up too (how hard to steer back): the expert
   never gave it. DAgger, in the part before this one, takes another way: it records the states the
   clone really reaches, and asks the expert for the label.

   The part "Recovery Data" shows how NVIDIA's network and ChauffeurNet make
   such views today.

The general result
""""""""""""""""""

Mistakes can grow with the square of the time. Ross and Bagnell bound behavior
cloning's cost (Ross and Bagnell, 2010):

- :math:`\varepsilon` is how often the policy makes a mistake on the states
  the **expert** visits (the open-loop error rate).
- Its cost over a drive of :math:`T` steps can grow up to :math:`T^2\varepsilon`,
  not :math:`T\varepsilon`. The paper says the cost "grows quadratically
  :math:`O(T^2)` in the task horizon :math:`T` rather than as :math:`O(T)`".
- In words: one mistake can take the policy off the expert's states, and from
  there it may keep making mistakes for the rest of the drive.

The slide plots both curves on logarithmic axes (the left gridlines are 100
times apart, the bottom ones 10 times). For our lap, with :math:`T` = 3,607
steps (1442.6 / 8 × 20) and :math:`\varepsilon` = 0.01 (chosen):

1. The bound: 3,607² × 0.01 = 130,104.
2. If mistakes did not compound: 3,607 × 0.01 = 36.07.

.. dropdown:: More detail: behavior cloning's bound, as the paper states it
   :class-container: more-detail
   :icon: info
   :name: l11-more-bc-bound

   **The symbols.** :math:`T` is the number of steps. :math:`J(\pi)` is a
   policy's total cost over :math:`T` steps, with a cost of at most 1 per
   step. :math:`\pi^*` is the expert and :math:`\hat\pi` is the clone.
   :math:`e_{\hat\pi}(s)` is the clone's 0-1 loss in state :math:`s`: 1 if it
   does not act as the expert would, 0 if it does. :math:`d_{\pi^*}` is the
   distribution of states the expert visits.

   **The theorem** (Theorem 2.1 in Ross and Bagnell, 2010): "Let
   :math:`\hat\pi` be such that :math:`E_{s\sim d_{\pi^*}}[e_{\hat\pi}(s)] \le
   \varepsilon`. Then :math:`J(\hat\pi) \le J(\pi^*) + T^2\varepsilon`."

   In plain words: if the clone's average mistake rate on the expert's own
   states is at most :math:`\varepsilon`, its total cost is at most the
   expert's plus :math:`T^2\varepsilon`.

   **Why** :math:`T^2`. The authors write: "as soon as :math:`\hat\pi` makes a
   mistake, it could end up in new states that were not visited by
   :math:`\pi^*`, and always incur maximal cost of 1 at each step from then
   on". They also write that "this bound is tight".

   **In mistakes, not cost.** The DAgger paper puts the same result as "as
   many as :math:`T^2\varepsilon` mistakes in expectation" (Ross, Gordon and
   Bagnell, 2011).

The bound is a worst case
"""""""""""""""""""""""""

The bound says what can happen, not a curve our lap must follow. It says what
can happen when one mistake sends the policy to states it never saw. Our lap
measures the same mechanism: 0.37° on the expert's states, and 15 of 20 test
laps lost once the clone drives.

Causal Confusion
^^^^^^^^^^^^^^^^

Our clone failed through what it could see: the detector's noise hid the offset. A clone can also fail through what it chooses to look at, a cue that comes with the right action in the recording without causing it.

Causal confusion
""""""""""""""""

Causal confusion makes the clone brake for the brake light. De Haan et al.
trained two clones with the same network on the same driving, with one
difference in the image (de Haan, Jayaraman and Levine, 2019).

- **Clone A** sees the windshield and the dashboard. Training loss: low. On
  the road: it does not drive well.
- **Clone B** sees the same image with the dashboard masked out. Training
  loss: low. On the road: it drives well.

The reason: "the dashboard has an indicator light that comes on immediately
when the brake is applied, and model A wrongly learns to apply the brake only
when the brake light is on". "Even though the brake light is the effect of
braking, model A could achieve low training error by misidentifying it as the
cause instead". More inputs can make a clone worse: "access to more
information can yield worse performance".

The inertia problem
"""""""""""""""""""

A stopped car learns to stay stopped. Codevilla et al. trained behavior
cloning in CARLA and found a failure that comes from the recording itself
(Codevilla et al., 2019).

- In the recording, a stopped car nearly always stays stopped: "When the ego
  vehicle is stopped (e.g., at a red traffic light), the probability it stays
  static is indeed overwhelming in the training data".
- The clone learns "a spurious correlation between low speed and no
  acceleration".
- On the road, this gives "excessive stopping and difficult restarting".
- The authors trace it to the same cause: "the inertia problem stemming from
  causal confusion".

In both cases the clone fits its recording, and the failure shows only when it
drives.

Averaging
^^^^^^^^^

At junction J the route can go left or straight, and the camera image is the same for both. From a recording that holds both answers for one image, the clone learns their average, which is neither.

The image does not say which way
""""""""""""""""""""""""""""""""

Junction J is on our lap, but our lap only goes straight through it. Suppose
the recording held expert drives both ways through J, half going straight and
half turning left. The camera sees the same junction each time.

.. figure:: /_static/images/L11/junction.png
   :class: dark-light themed-L11
   :alt: Top view of junction J in Town01, about 60 m across. The AV, drawn as a car facing right, sits in a gray lane coming from the left. The lane goes straight on to the right, its centerline a solid dark line tagged 1, and also turns left and up, its centerline a dashed dark line tagged 2. A rust arc, tagged 3, starts where the lanes split and curves up between them, through the corner, missing both lanes.
   :width: 60%
   :align: center

   Junction J: straight on, left, and the average of the two.

.. admonition:: Reading the figure
   :class: tip

   The axes are the map's x (east) and y (north), in meters. The AV comes
   from the left.

   - **Tag 1, solid dark line:** the center line of the lane that goes
     straight on.
   - **Tag 2, dashed dark line:** the center line of the lane that turns left.
   - **Tag 3, rust arc:** the path of a clone fit to both drives. It starts
     where the lanes split and curves up between them, through the corner,
     and misses both lanes.

1. **Straight:** the expert steers 0°.
2. **Left:** the turn's radius is 10.9 m (17.1 m of arc for 90°), so the
   expert steers arctan(2.9 / 10.9) = 14.9°.
3. **A clone fit to both** by least squares gives about the average:
   14.9 / 2 = 7.45°, a circle of radius 2.9 / tan(7.45°) = 22.2 m. After 34 m
   (a length chosen for this example) it is 9.1 m from the nearest point of
   the left lane's center line, measured on the map.

Codevilla et al. say it the same way: "when a car approaches an intersection,
the camera input is not sufficient to predict whether the car should turn
left, right, or go straight" (Codevilla et al., 2018).

.. _l11-lec-fixing:

Fixing the Clone
~~~~~~~~~~~~~~~~

The last part gave three causes: the clone drives where the recording never was, learns the wrong cause, and averages two right answers. Each fix targets one cause: data from the states where the clone drifts, or an input that tells two answers apart. Causal confusion has no fix that works on real driving yet.

DAgger
^^^^^^

DAgger is not a network: it is a way to train one. It lets the clone drive and asks the expert what it would steer in each state the clone reaches, so the training data covers the states the clone really visits.

.. admonition:: Definition: DAgger (dataset aggregation)
   :class: note

   A way to train a behavior cloning policy, not a network. It repeats: the
   current policy drives, the expert labels every state it reached, those pairs
   join all the data so far, and the policy is trained again on all of it. Ross
   et al.: "an iterative algorithm that trains a deterministic policy" (Ross,
   Gordon and Bagnell, 2011).

Where it sits: among the ways to train an end-to-end driver, imitation learning
holds behavior cloning, and DAgger is a loop around behavior cloning's training.

- **The network does not change.** DAgger starts from "any policy in Π", Π
  being the kind of policy chosen: here the clone's four weights; it could be
  NVIDIA's network, with about 250 thousand.
- **The training step does not change.** "Train classifier π̂\ :sub:`i+1` on
  D", the next policy on all the pairs: the same least squares as the clone.
- **The data changes.** It keeps "building up the set of inputs that the
  learned policy is likely to encounter during its execution".

DAgger
""""""

.. figure:: /_static/images/L11/dagger_loop.png
   :class: dark-light themed-L11
   :alt: A loop of four boxes. A box on the left, Start: behavior cloning, points to Step 1, outlined rust: the newest clone drives one lap. Step 1 points right to Step 2, outlined dark: the expert labels every state it reached. Step 2 points down to Step 3: add the pairs to all the data so far. Step 3 points left to Step 4, outlined green: refit the clone on all the data. Step 4 points up to Step 1.
   :width: 86%
   :align: center

   The DAgger loop.

.. admonition:: Reading the figure
   :class: tip

   DAgger starts from behavior cloning, then loops.

   - **Step 1, rust:** the newest clone drives one lap.
   - **Step 2, dark:** the expert labels every state the clone reached.
   - **Step 3:** those pairs are added to all the data so far.
   - **Step 4, green:** the clone is refit on all of it, and the loop goes
     back to step 1.

DAgger ("dataset aggregation") is from Ross, Gordon and Bagnell, 2011. Its
card on the slide:

- **Fixes:** compounding error: the clone fails in states the expert's
  recording never shows.
- **Who drives:** the newest clone. The expert drives the first lap only.
- **Who labels:** the expert, in every state the clone reaches.
- **The data:** every labeled pair so far, :math:`D \leftarrow D \cup D_i`.
  The clone is trained again on all of it.
- **Our clone:** finishes 5 of 20 test laps; 16 after one DAgger lap, 19
  after two (training run 6).
- **Ten runs:** DAgger finishes 19 of 20 in 10 of 10 training runs.
- **Costs:** an expert who can label any state, and a safe place for a bad
  clone to drive.
- **Hands-on:** ``python3 l11_handson.py --part dagger``.

Laps and runs are from the hands-on model (numpy, test laps 100 to 119). The
paper's algorithm has two key lines: "Aggregate datasets: :math:`D \leftarrow
D \cup D_i`" and "Train classifier :math:`\hat\pi_{i+1}` on :math:`D`".
:math:`D` is all the labeled pairs so far, and :math:`D_i` the pairs from
iteration :math:`i`. The slide shows the four steps on a straight stretch of
the first DAgger lap in run 6, from 1,092 to 1,148 m, where the newest clone
drifts left of the lane center.

Who drives, who labels
""""""""""""""""""""""

The clone steers the AV, and the expert's label for each state goes into the
data. In iteration :math:`i` the paper drives with a mix: "Let :math:`\pi_i =
\beta_i \pi^* + (1 - \beta_i)\hat\pi_i`" (Ross, Gordon and Bagnell, 2011).

- :math:`\pi_i` is the driver in iteration :math:`i`, :math:`\pi^*` is the
  expert, :math:`\hat\pi_i` is the clone after :math:`i - 1` refits, and
  :math:`\beta_i` is the share of steps the expert drives.
- **Our choice:** :math:`\beta_1 = 1` (iteration 1 is the expert's lap:
  behavior cloning), then :math:`\beta_i = 0` (the clone drives alone).
- **Labels:** always the expert's, whoever drove.

For example, at 640 m on a test lap the AV executes the clone's steering,
−0.5°, and the data stores the expert's label for that state, −2.5°. The AV is
0.71 m left of the lane center there.

So the data now holds the states the clone itself reaches. The next fit is
judged on the states where the last clone made its mistakes.

Data after five DAgger laps
"""""""""""""""""""""""""""

.. figure:: /_static/images/L11/dagger_coverage.png
   :class: dark-light themed-L11
   :alt: Two histograms of the true offset in the labeled data. Tagged 1, dark, small: the expert's lap alone, 3607 steps, narrow around zero. Tagged 2, green, tall: all data after iteration 6, 21642 steps, wider, from about minus 1.1 to plus 1.3 m.
   :width: 66%
   :align: center

   The labeled data before and after five DAgger laps.

.. admonition:: Reading the figure
   :class: tip

   The horizontal axis is the true offset (left positive). The vertical axis
   is the number of labeled time steps.

   - **Tag 1, dark:** the expert's lap alone (iteration 1). It is small and
     narrow around zero.
   - **Tag 2, green:** all the data after iteration 6, which is the expert's
     lap and five DAgger laps. It is taller and wider.

Five DAgger laps add states the expert's own lap never reached. The data now
covers the drift away from the lane center.

- Labeled states: 3607 × 6 = 21,642 (each lap is 3607 steps: a wheel left the
  lane on two DAgger laps, but no lap reached 1.6 m off center, where a lap
  stops).
- True offset beyond 0.5 m: 2.0% of the expert's lap, 10.8% of all the data.
  The spread (standard deviation) goes from 0.154 m to 0.293 m.

Laps finished and offset weight
"""""""""""""""""""""""""""""""

.. figure:: /_static/images/L11/dagger_iters.png
   :class: dark-light themed-L11
   :alt: Two line plots against DAgger iteration 1 to 6, iteration 1 being behavior cloning, drawn as a rust dot. Left: test laps finished, of 20: 5 at iteration 1 (tagged 1), 16 at iteration 2, then 19 at iterations 3 to 6; a dashed dark line at 20 is the expert, tagged 2. Right: steer back per meter of offset, in degrees: 0.38 at iteration 1, 1.44 at iteration 2, 1.54 at iteration 3, then slowly down to 1.32 at iteration 6; a dashed dark line at 3.44 is the expert, tagged 2.
   :width: 100%
   :align: center

   Test laps finished and the offset weight, by DAgger iteration.

.. admonition:: Reading the figure
   :class: tip

   Both plots have the DAgger iteration on the horizontal axis. Iteration 1
   is behavior cloning (the rust dot).

   - **Left plot:** test laps finished, out of 20. Tag **1** marks the first
     rise, from behavior cloning to the first DAgger lap. Tag **2** is the
     expert, at 20.
   - **Right plot:** the weight on the offset, in degrees of steering back
     per meter. Tag **2** is the expert, at 3.44.

Each DAgger iteration changes how many test laps the clone finishes and its
offset weight, the degrees it steers back per meter of offset. One DAgger lap
lifts the clone from 5 to 16 finished laps, and the second to 19, where it
stays. At iteration 6: 19 of 20 laps finished, offset weight 1.32 degrees per
meter.

The weight goes from 0.38° per meter to 1.44 after one lap, peaks at 1.54,
and ends at 1.32. It stays below the expert's (1.32° against 3.44° per
meter): the detector's noise still hides part of the offset, but the weight is
now strong enough to keep the lane.

Drive each clone
""""""""""""""""

The slide lets you pick an iteration and a test lap, and watch that clone
drive the lap. A plot compares its offset from the lane center with the
expert's. Behavior cloning (iteration 1) finishes 5 of 20 test laps. On test
lap 18, a wheel leaves the lane at 649 m.

Ten training runs
"""""""""""""""""

.. figure:: /_static/images/L11/seeds.png
   :class: dark-light themed-L11
   :alt: Dot plot of test laps finished, of 20, for ten training runs numbered 1 to 10. Rust circles, tagged 1, for behavior cloning: 5, 8, 4, 9, 4, 5, 6, 7, 3 and 2. Green squares, tagged 2, for DAgger after iteration 6: 19 in every run.
   :width: 75%
   :align: center

   Laps finished in ten training runs.

.. admonition:: Reading the figure
   :class: tip

   Each run records a new expert lap and new DAgger laps. All clones are
   tested on the same 20 laps.

   - **Tag 1, rust circles:** behavior cloning, from 2 to 9 laps of 20.
   - **Tag 2, green squares:** DAgger after iteration 6, 19 laps in every run.

The result is not luck: behavior cloning's lap count varies by run, and
DAgger's does not. Run 6, the one the notes follow, finished 5 with behavior
cloning and 19 with DAgger.

- Behavior cloning finishes 2 to 9 laps of 20 over the ten runs (the median
  is 5). DAgger finishes 19 in every run.
- DAgger always misses test lap 8. The expert's own largest offset, 0.75 m
  (the limit is 1.0 m), is on that lap, so it is the hardest lap.

The spread among behavior cloning runs is large, which is why one run alone
says little.

What DAgger costs
"""""""""""""""""

DAgger fixes the drift, but it has three costs:

1. **An expert who can label any state.** A program that reads the
   simulator's state can. A human must say what they would steer in a state
   they did not drive, often from a recording, after the fact.
2. **A place for a bad clone to drive.** The first DAgger lap is driven by the
   behavior-cloned clone, which left its lane on 15 of 20 test laps. Such laps
   belong in a simulator, or with a safety driver.
3. **A guarantee with conditions.** The paper's bound is linear in :math:`T`,
   where behavior cloning's was quadratic, under conditions on the expert's
   ability to recover and on the class of policies.

.. dropdown:: More detail: DAgger's guarantee and its conditions
   :class-container: more-detail
   :icon: info
   :name: l11-more-dagger-guarantee

   **The theorem** (Theorem 3.2 in Ross, Gordon and Bagnell, 2011): "if
   :math:`N` is :math:`\tilde O(uT)` there exists a policy
   :math:`\hat\pi \in \hat\pi_{1:N}` s.t. :math:`J(\hat\pi) \le J(\pi^*) +
   uT\varepsilon_N + O(1)`."

   **The symbols:**

   - :math:`N` is the number of DAgger iterations, and
     :math:`\hat\pi_{1:N}` is the set of clones they produce.
   - :math:`u` is how much one wrong action can cost the expert afterward,
     when the expert takes over. An expert that recovers quickly has a small
     :math:`u`.
   - :math:`\varepsilon_N` is the error of the best policy in the class, on
     all the states the clones visited.
   - :math:`T` and :math:`J` are as in the bound for behavior cloning.

   **What it says.** The extra cost grows linearly in :math:`T`, against
   :math:`T^2` for behavior cloning, when :math:`u` and :math:`\varepsilon_N`
   are small. Both are conditions, and our example meets them only in part.
   The clone is a linear policy, and it cannot copy the expert exactly through
   the detector's noise, so :math:`\varepsilon_N` is not zero. That shows in
   the offset weight, which stopped at 1.32° per meter against the expert's
   3.44°.

A bad clone needs a safe place to drive
"""""""""""""""""""""""""""""""""""""""

The first DAgger lap is driven by a bad clone, which can drift toward the next
lane. The slide's AV offset slider shows how close it gets to another car. The
run stops when the AV is 1.6 m off the center (chosen). The AV's left side is
then 1.6 + 1.0 = 2.6 m from the lane center. A 2.0 m wide car in the middle of
the next lane has its near side 4.0 − 1.0 = 3.0 m from it. The gap: 3.0 − 2.6 =
0.40 m. The other car and the next lane (4.0 m wide) are chosen for this
example, not measured.

DAgger's idea at fleet scale
""""""""""""""""""""""""""""

A company with a fleet uses the same idea as DAgger: find where the learned
driver does poorly, and train more there.

- **DAgger, on our lap.** The clone drives; the expert labels every state the
  clone reaches; those states join the training data.
- **Wayve, on a fleet.** Alex Kendall, its CEO: they use unsupervised learning
  "to be able to cluster and find unusual or anomaly […] experiences", then
  "find the scenarios that our system is […] performing poorly at and then
  drive the learning curriculum on those" (Kendall, 2025).

Both put the training data where the learned driver fails.

Recovery Data
^^^^^^^^^^^^^

DAgger adds the states the clone reaches, but it needs an expert who can label any state. Recovery data adds off-center states to the recording itself, each labeled with the way back.

Recovery data
"""""""""""""

Recovery data shows the clone off-center views, each labeled with the way back
to the lane. "The network must learn how to recover from mistakes" (Bojarski
et al., 2016), but a careful driver rarely leaves the lane and real mistakes
are unsafe on a public road, so the views are made.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40
   :class: compact-table

   * - Who
     - How the off-center states are made
     - The label
   * - NVIDIA, 2016 (Bojarski et al., 2016)
     - Two side cameras give two off-center views; the other shifts and all
       rotations are made from the nearest camera's image.
     - The steering "back to the desired location and orientation in two
       seconds".
   * - ChauffeurNet, 2018 (Bansal, Krizhevsky and Ogale, 2018)
     - The expert's path is jittered: its midpoint up to 0.5 m in each axis,
       its heading up to π/3 rad (60°). A smooth path through the moved point.
     - Moves that collide or leave the road are kept, so the model "can then
       experience and avoid such behaviors".

Like DAgger, both add states the expert never drove. Unlike DAgger, no expert
labels them: the label comes from geometry.

Training on off-center views
""""""""""""""""""""""""""""


.. figure:: /_static/images/L11/l11_nvidia_train.png
   :class: white-figure
   :alt: A block diagram of NVIDIA's training loop. A box Recorded steering angle points to a box Adjust for the shift and rotation, whose output, desired steering, runs along the top to a circle with a minus sign. Three camera boxes of equal width, left, center and right, feed a box Random shift and rotation, which feeds an orange box CNN. The CNN's output, proposed, goes to the same circle. The circle's output, error, goes to a box Backpropagation: adjust the weights, which points up to the CNN.
   :width: 85%
   :align: center

   NVIDIA's training loop on off-center views.

.. admonition:: Reading the figure
   :class: tip

   - **Cameras and random shift:** the three cameras give the images, and a random shift and rotation makes more off-center views.
   - **Recorded steering angle:** adjusted for the shift and rotation, which gives the desired steering.
   - **CNN (orange):** proposes a steering. The circle subtracts it from the desired steering, which gives the error.
   - **Backpropagation:** the error adjusts the CNN's weights.

NVIDIA's loop trains on off-center views, each labeled with the way back
(Bojarski et al., 2016). Its parts, as the slide draws them:

1. The **left, center and right cameras** give the images.
2. A **random shift and rotation** makes more off-center views.
3. The recorded steering angle is adjusted for the shift and rotation, which
   gives the desired steering.
4. The **CNN** proposes a steering. The error against the desired steering
   goes back through the network, and backpropagation adjusts the weights.

Real side views and made shifts give the network off-center states; each one is
labeled with the steering that leads back to the lane.

A Privileged Teacher
^^^^^^^^^^^^^^^^^^^^

Our expert already reads privileged information: the true offset, which only the simulator knows. A teacher that sees the true state can train a student that sees only the cameras.

A privileged teacher
""""""""""""""""""""

A driver that cheats by seeing the true state trains a student that sees only
the cameras. Training happens in two stages. The first stage is the teacher,
the second the student.

.. list-table::
   :header-rows: 1
   :widths: 24 38 38
   :class: compact-table

   * -
     - The teacher
     - The student
   * - Learning by Cheating, 2019 (Chen et al., 2019)
     - It "cheats by observing the ground-truth layout of the environment and
       the positions of all traffic participants".
     - The teacher "trains a purely vision-based sensorimotor agent". Result:
       "100% success rate on all tasks in the original CARLA benchmark".
   * - Roach, 2021 (Zhang et al., 2021)
     - "a reinforcement learning expert that maps bird's-eye view images to
       continuous low-level actions".
     - "a baseline end-to-end agent with monocular camera-input achieves
       expert-level performance".

Our lap has the same split: the expert reads the true offset, the clone a noisy
lane detector.

Hands-on code
"""""""""""""

Clone the expert, then run DAgger, in the course's Python repo, folder
``lecture11``
(`README <https://github.com/rubixcubic/enpm818z-fall-2026-carla-python/tree/main/lecture11>`__).
It has five parts. Everything runs on a laptop with numpy and matplotlib,
without CARLA:

.. code-block:: bash

   python3 l11_handson.py --part road     # the lap and the expert
   python3 l11_handson.py --part bc       # fit, then drive
   python3 l11_handson.py --part shift    # error by offset
   python3 l11_handson.py --part dagger   # DAgger, slider
   python3 l11_handson.py --part eval     # open vs closed loop

The options ``--detector-noise`` (meters, default 0.35), ``--gust``
(degrees, default 0.4), ``--seed`` (the expert's recorded lap and DAgger's
laps, default 6, the run in these notes) and ``--iterations`` (default 6)
change the example. The ``bc`` part prints the offset weight, in degrees of
steering back per meter of offset, for the expert and the clone.

Try three things:

1. Run ``--part bc`` with ``--detector-noise 0.1``. Does the clone keep the
   lane? What happened to the offset weight?
2. Run ``--part dagger`` with ``--gust 0.6``. How many laps does the expert
   finish? And DAgger?
3. Change ``--seed`` (the default is 6). Which numbers move, and by how much?
   This is how you see the spread for yourself.

Route Commands
^^^^^^^^^^^^^^

The fixes so far add states near the drift. Averaging needs another fix: its recording holds two answers for one image. The input that tells them apart is the route's command, which picks one head of the network.

Three commands at junction J
""""""""""""""""""""""""""""

At junction J, the route gives the AV one of three commands, and each command
picks one path. The network has four heads: follow lane, left, straight and right. The map
has no right turn at J, so the data has no path for the right head.

1. **Follow lane:** stay in the lane.
2. **Left:** take the left branch (a 90° turn).
3. **Straight:** take the straight branch.

Conditional imitation
"""""""""""""""""""""

The route's command picks which head of the network gives the steering,
throttle and brake.

.. figure:: /_static/images/L11/cil_branches.png
   :class: dark-light themed-L11
   :alt: A diagram. Camera image and Speed feed a blue box, Shared layers. From it, four blue boxes: Follow lane head, Left head, Straight head, Right head. Only the Straight head connects to the output box, Steering, throttle, brake. A dashed arrow from a box below, Command from the route: Straight, points up to that connection, labeled picks the Straight head.
   :width: 84%
   :align: center

   A conditional imitation network with one head for each command.

.. admonition:: Reading the figure
   :class: tip

   - **Shared layers:** the camera image and the speed go in. These first
     layers are used for every command.
   - **Four heads:** follow lane, left, straight and right. Each head is a
     small part of the network that produces the steering, throttle and brake
     for one command.
   - **The dashed arrow:** the command from the route, here "Straight", picks
     which head connects to the output. The other three heads are not used at
     that moment.

With the command "straight", the Straight head outputs 0° at J, the expert's
steering when it goes straight.

Codevilla et al. use "a set of four commands: continue (follow the road), left
(turn left at the next intersection), straight (go straight at the next
intersection), and right" (Codevilla et al., 2018). The command "acts as a
switch that selects between specialized sub-modules". The route planner
supplies the command, and that is how a learned driver follows the route your
planner chose.

CARLA's Leaderboard, which has since closed (CARLA Team, Leaderboard), gave
every agent its route with these commands. For example, ``RoadOption.LEFT``
means "Turn left at the intersection" (CARLA Team, Leaderboard 2.1 criteria).

.. _l11-lec-beyond-bc:

Beyond Behavior Cloning
~~~~~~~~~~~~~~~~~~~~~~~

Behavior cloning copies the expert's actions. The same demonstrations can teach other things: a cost that makes the expert's path the cheapest (inverse optimal control, on the map), or a model of the world learned with the policy.

Cost learning
^^^^^^^^^^^^^

Cost learning learns a cost from the expert, then drives the cheapest
trajectory. The survey's definition: "end-to-end approaches learn a reasonable
cost c(·) and use algorithmic trajectory samplers to select the trajectory τ*
with the minimum cost" (Chen et al., 2024).

1. **Learn the cost:** a loss that makes "the expert demonstration to have a
   minimal cost while others have high costs".
2. **Sample** candidate trajectories with an algorithm, not with the network.
3. **Drive** the one with the lowest learned cost.

Example: the Neural Motion Planner outputs "a cost volume defining the
goodness of each position that the self-driving car can take within the
planning horizon", then it samples trajectories "and choose[s] the one with
the minimum learned cost" (Zeng et al., 2019).

A model of the world
^^^^^^^^^^^^^^^^^^^^

MILE learns a model of the world together with the driving policy. It is still
imitation learning, with a second thing learned beside the policy.

- MILE is "a Model-based Imitation LEarning approach to jointly learn a model
  of the world and a policy for autonomous driving" (Hu et al., 2022).
- Result: "MILE improves upon prior state-of-the-art by 31% in driving score
  on the CARLA simulator when deployed in a completely new town and new
  weather conditions". The score is measured while the car drives: closed
  loop.

Two ways to learn from demonstrations beyond copying the actions: learn a
cost, or learn a model of the world with the policy.


.. _l11-lec-reinforcement-learning:

Reinforcement Learning
----------------------

Imitation learning needs an expert to copy. Reinforcement learning, the map's
second branch, drops the expert: the driver learns by trial, from a reward. It
needs room to fail, which is why it has mostly stayed in simulation.

Reinforcement learning, defined
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Reinforcement learning
   :class: note

   Learning a policy by trial and error, from a reward instead of an expert.
   "Reinforcement learning (RL) is a field of learning by trial and error"
   (Chen et al., 2024); it "tries to obtain a policy that maximizes an
   expected reward" (Osa et al., 2018).

The loop, step by step
~~~~~~~~~~~~~~~~~~~~~~

The loop has four parts. The deck takes them one per slide, on one try of the
search: round 1's best, whose weights the search drew at random.

1. **The policy steers.** It is the clone's rule: each thing the AV sees times
   a weight, added up. Round 1's best weights are +3.45° per meter of offset,
   −2.65° per degree of heading and +79.53° per unit of curvature (1/m). At
   step 5 the detector reads an offset of −0.41 m and a heading of +0.89°, so
   the terms are −1.42° and −2.36° (the curvature term is 0) and the policy
   steers −3.78°. The offset
   weight is positive: the farther left the AV sits, the more it steers left, a
   rule no expert uses.
2. **The car moves one step.** The simulator turns the wheels for 0.05 s; at 8
   m/s the AV moves 0.4 m. The detector then reads the new offset and heading,
   with noise: that reading is the next state. Over the first 12 steps the AV
   stays within 1.7 cm of the lane center, while the detector puts it anywhere
   from 0.93 m right to 0.64 m left of it, and the steering follows the
   readings.
3. **The reward.** Each step in the lane adds +0.4 m. A wheel leaves the lane at
   the end of turn 1, 134.4 m after the start, about 336 steps: the try ends,
   with a reward of 134.4 m. A try that finishes the lap earns the whole lap.
4. **Learn from the round.** A round is 30 tries, each with weights drawn
   at random around the current guess. The 6 with the largest reward set the
   next guess, their average, and how far around it the next 30 are drawn, as
   far as the 6 lie apart. Round 1 draws around weights
   of 0; in round 3, 19 of 30 tries finish the lap; after 15 rounds (450 tries)
   the guess is −5.1° per meter of offset and −2.20° per degree of heading, not
   the expert's −3.44 and −0.80, and it finishes every test lap.

No expert says what the right action was: the reward alone decides which
weights survive.

A reward for lane keeping
~~~~~~~~~~~~~~~~~~~~~~~~~

On our lap, the reward is the distance driven before a wheel leaves the lane.
Kendall et al. used the same idea on a real car: "the distance travelled by the
vehicle without the safety driver taking control" (Kendall et al., 2018).

- **Round 1's best try** drove 134.4 m. Turn 1 runs from about 110 m to 134 m,
  and a wheel left the lane at its end: the episode ended there, with a reward
  of 134.4 m.
- **The learned policy** drove the whole lap (1442.6 m long) with no wheel out
  of the lane: a reward of 1442.8 m, the distance its 0.05 s steps covered.

No one labels an action: the reward only says how far the AV got.

Learning by trial, episode by episode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The search drove 450 episodes on our lap, 15 rounds of 30, with no expert. It
started from weights of 0; each round kept its 6 best tries and drew new
weights around them (a cross-entropy search; these settings were chosen for
this example).

- In round 1, 25 of the 30 tries left the lane before turn 1, and none got
  past its end.
- The first whole lap came at episode 36, in round 2.
- The learned weights finish **20 of 20** test laps; the clone finished 5 of
  20.
- They are not the expert's weights: the offset weight is 5.1 deg/m, against
  the expert's 3.4 deg/m.

Kendall et al.'s real car learned the same task the same way. On a 250 m road,
one version drove the route "after only 11 training episodes"; the task took
"under thirty minutes of training", "all done on on-board computers" (Kendall
et al., 2018). "We demonstrate the first application of deep reinforcement
learning to autonomous driving".

Why imitation leads in driving
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RL learned to follow a lane on a real car, but imitation learning still leads
end-to-end driving. The survey gives the reasons (Chen et al., 2024):

- **Room to fail:** "RL requires an environment that allows potentially unsafe
  actions to be executed".
- **Data:** "RL requires significantly more data to train than IL", so "almost
  all papers that use RL in driving have only investigated the technique in
  simulation".
- **A reward to design:** behavior cloning "does not require hand-crafted
  reward design, which is crucial for RL".
- **The result so far:** "To date, no report has shown results for end-to-end
  training with RL that are competitive with IL".

Where a simulator can absorb the failures, RL works: Roach's expert, the
teacher of the part "A Privileged Teacher", was trained with RL.

.. _l11-lec-inside-the-networks:

Inside the Networks
-------------------

The last two sections gave ways to train a driver; this one opens the networks
they train. It first opens NVIDIA's network to show how its features are
learned, then covers two published end-to-end drivers, TransFuser and UniAD,
then the models that also read and write text. You see which parts of your stack such a network
replaces, and which it keeps.

How a Network Learns Its Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Behavior cloning trains an end-to-end network only on the expert's steering,
yet inside it the network learns features such as lane lines.

PilotNet, layer by layer
^^^^^^^^^^^^^^^^^^^^^^^^

NVIDIA's network has "9 layers, including a normalization layer, 5
convolutional layers and 3 fully connected layers" (Bojarski et al., 2016).
The learned weights of each layer are counted from its sizes: filters times
kernel times input planes, plus one bias per filter; or inputs times outputs,
plus one bias per output.

.. list-table::
   :header-rows: 1
   :widths: 22 40 38

   * - Layer
     - What it holds
     - Learned weights
   * - Input
     - 3 YUV planes of 66 by 200 pixels (Y is brightness, U and V are color)
     - none
   * - Normalization
     - "hard-coded and is not adjusted in the learning process"
     - none
   * - Convolution 1
     - 24 filters, 5 by 5, stride 2: maps of 31 by 98
     - 24 × (5×5×3) + 24 = 1,824
   * - Convolution 2
     - 36 filters, 5 by 5, stride 2: maps of 14 by 47
     - 36 × (5×5×24) + 36 = 21,636
   * - Convolution 3
     - 48 filters, 5 by 5, stride 2: maps of 5 by 22
     - 48 × (5×5×36) + 48 = 43,248
   * - Convolution 4
     - 64 filters, 3 by 3: maps of 3 by 20
     - 64 × (3×3×48) + 64 = 27,712
   * - Convolution 5
     - 64 filters, 3 by 3: maps of 1 by 18
     - 64 × (3×3×64) + 64 = 36,928
   * - Flatten
     - 1,164 numbers, as the paper's figure gives them (its 64 maps of 1 by 18
       make 64 × 18 = 1,152)
     - none
   * - Fully connected
     - 100, then 50, then 10 neurons
     - 116,500 + 5,050 + 510
   * - Output
     - "the inverse turning radius"
     - 11

They add up to 253,419, the paper's "250 thousand parameters". Training sets
them all "to minimize the mean squared error" between the network's steering
and the human's.

A small network learns a feature
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The deck trains a tiny version of the same idea in the page, live. The setup
is chosen for the example:

- **The input:** one camera row across the road ahead, 48 pixels of 0.2 m:
  grass, the gray road and two bright lane lines 2 m either side of the lane
  center, with a little noise. The AV's offset shifts the lines.
- **The label:** the expert's steering on a straight road, −3.44° per meter of
  offset.
- **The network:** a filter of 5 weights slid along the row gives 44 values;
  negatives are set to 0 (ReLU), which makes the feature map. A readout, 44
  more weights, adds the map into a steering. With 2 biases, 51 weights in all;
  the filter and readout weights start random, the biases at 0.
- **The training:** 4,000 steps of gradient descent on the squared error, each
  on one of 400 recorded rows: every weight moves a little in the direction
  that shrinks the error on that row.

At the start, the feature map is near zero almost everywhere. After training,
it peaks at the lane lines, is lower and flat on the road and zero on the
grass: the filter learned to find the lines from the steering label alone.
Each step does the same thing: a forward pass gives a steering, the error is
predicted minus label, and the chain rule (the derivative of the error through
each layer) says how each weight should move to shrink it.

What PilotNet's features show
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NVIDIA looked at the first two layers of feature maps for two images
(Bojarski et al., 2016):

- **An unpaved road:** "the feature map activations clearly show the outline
  of the road".
- **A forest, no road:** "the feature maps contain mostly noise, i. e., the CNN
  finds no useful information in this image".
- **What it means:** "the CNN learned to detect useful road features on its
  own, i. e., with only the human steering angle as training signal".
- **No clean line inside:** "it is not possible to make a clean break between
  which parts of the network function primarily as feature extractor and which
  serve as controller".

Fusion and the Stack in One Network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NVIDIA's end-to-end network of 2016 (:ref:`l11-lec-introduction`) has one
camera image in and a steering command out. TransFuser and UniAD are end-to-end
networks of the same kind, built later. They read more sensors, keep parts of
the stack inside the network, and output a trajectory. All three follow the
same chain: sensors, one neural network, then a trajectory or a steering
command.

.. list-table:: Three networks, one chain
   :header-rows: 1
   :widths: 16 22 34 28

   * - Network
     - Sensors
     - One neural network
     - Trajectory or steering
   * - NVIDIA (Bojarski et al., 2016)
     - One front camera
     - Convolution layers, then fully connected layers
     - A steering command, "the inverse turning radius"
   * - TransFuser (Prakash et al., 2021)
     - Camera and LiDAR
     - Two branches, fused "using attention"
     - Waypoints, then two PID controllers (not learned)
   * - UniAD (Hu et al., 2023)
     - Several cameras
     - The stack's tasks (track, map, motion, occupancy, planner) as modules
       of the network
     - The AV's future waypoints

TransFuser
^^^^^^^^^^

TransFuser fuses a camera image and a LiDAR grid with attention, then
predicts waypoints.

.. figure:: /_static/images/L11/transfuser.png
   :class: dark-light themed-L11
   :alt: A diagram. Camera image feeds a row of four blue conv boxes; LiDAR, seen from above, feeds a second row of four conv boxes. Between each pair, a blue attn box exchanges with both rows. Both rows end in a blue Waypoint predictor box, which sends waypoints to a gray box, Two PID controllers, which outputs steering, throttle, brake. A note says learned (blue): trained by imitation.
   :width: 100%
   :align: center

   TransFuser, at the level of its blocks.

.. admonition:: Reading the figure
   :class: tip

   - **conv:** convolution layers. The top row reads the camera image, and
     the bottom row reads the LiDAR points seen from above.
   - **attn:** attention, the building block of transformers. Between each
     pair of conv boxes it lets the two branches exchange features. The
     figure shows four pairs, at four resolutions.
   - **Waypoint predictor:** both branches end in it. Everything in blue is
     trained by imitation; the gray dashed part is not learned.
   - **Two PID controllers (gray):** they turn the waypoints into steering,
     throttle and brake. This last step is not learned.

The authors' aim is "to integrate image and LiDAR representations using
attention" (Prakash, Chitta and Geiger, 2021). The predictor works in "an
auto-regressive waypoint prediction framework". They also write: "We use two
PID controllers for lateral and longitudinal control". A PID controller turns
a target into steering or throttle by feedback on its error. They are the same
kind of controllers you built.

TransFuser was tested closed loop in CARLA, on the CARLA Leaderboard, which
has since closed (Chitta et al., 2023; CARLA Team, Leaderboard).

TransFuser's inputs in 3D
^^^^^^^^^^^^^^^^^^^^^^^^^

TransFuser takes one front camera and a LiDAR grid. The slide shows both in
3D, and you can turn the scene and show the camera's view, the points, or the
grid.

- **The camera:** "the front camera with a FOV of 100°" (Prakash, Chitta and
  Geiger, 2021).
- **The points:** one CARLA sweep in Town01 with the course's LiDAR, 32
  channels, 50 m.
- **The grid:** "the points within 32m in front of the ego-vehicle and 16m to
  each of the sides", in 0.125 m cells.
- **Two bins,** "on/below and above the ground plane": gray and teal on the
  slide, split at 0.2 m (chosen).

UniAD
^^^^^

UniAD puts the stack's modules inside one neural network, trained together
toward planning. The slide draws the chain: several cameras, bird's-eye
features, then five modules (Track, Map, Motion, Occupancy and Planner), and
the output, the AV's future waypoints. A click on a module's button tells you
what it does.

UniAD "incorporates full-stack driving tasks in one network". "Tasks are
communicated with unified query interfaces to facilitate each other toward
planning" (Hu et al., 2023). A **query** is a learned vector that collects
what one module needs from the bird's-eye features. It replaces the
hand-designed message between two parts.

For example, Track tracks the objects around the AV. It has its own queries,
learned vectors that collect what it needs from the bird's-eye features. Its
output can be read out, as the output of the matching part of your stack can.

UniAD won Best Paper at CVPR 2023 (CVPR 2023). Its planning is scored open
loop, on recorded nuScenes drives (Zhai et al., 2023). The section "Scoring a
Driver" comes back to this.

UniAD's input in 3D
^^^^^^^^^^^^^^^^^^^

UniAD sees the road with six cameras and turns what they see into one
bird's-eye grid. You can pick a camera to light the cells it sees.

- **The cameras,** from nuScenes, UniAD's data: "Front and side cameras have a
  70° FOV and are offset by 55°. The rear camera has a FOV of 110°" (Caesar et
  al., 2020).
- **The grid** comes from "an off-the-shelf BEV encoder in BEVFormer" (Hu et
  al., 2023): 200 × 200 cells of 0.512 m (Li et al., 2022). The slide shades
  the cells that two cameras see darker.

What each of UniAD's tasks outputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each of UniAD's five tasks gives its own output (Hu et al., 2023). The slide
draws each output on one road scene, as a sketch and not as UniAD's output:

1. **Track:** agents tracked with the same id over time.
2. **Map:** lanes and dividers.
3. **Motion:** each agent's future path.
4. **Occupancy:** which cells will be taken.
5. **Planner:** the AV's waypoints.

Your stack and UniAD, part by part
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

UniAD does the tasks your stack does. The table compares the two part by part:
what passes between parts, how each is trained, how you find a failure, and
what data each needs.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40
   :class: compact-table

   * -
     - Your stack (GP1 to GP4)
     - UniAD
   * - Between parts
     - ROS topics you defined: boxes, a pose, a path
     - learned queries
   * - Trained or tuned
     - each part on its own score
     - all parts together, with the planning loss
   * - When it fails
     - read each topic to find the part
     - each module's output can be read out; the queries are vectors, not
       messages a person reads
   * - Data it needs
     - labels for each part
     - labels for every module, and driving

UniAD keeps your stack's tasks and their names. What it removes is the
hand-designed message between them.

Vision-Language-Action Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The last part gave end-to-end networks that output waypoints. Vision-language-action (VLA) models add language, in and out: they also read and write text. They are the newest driving models, and they add time to every decision.

Vision-language-action model (VLA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Vision-language-action model (VLA)
   :class: note

   A vision-language model (one that reads images and text and writes text)
   trained to output actions too: "we express the actions as text tokens and
   incorporate them directly into the training set of the model in the same
   way as natural language tokens. We refer to such category of models as
   vision-language-action models (VLA)" (Brohan et al., 2023).

- The term comes from RT-2, a robot manipulation model (2023).
- For driving, the action is a trajectory, written as numbers in text, and the
  model can also write why.
- Koopman warns that such reasons may not be the real cause: "a lot of the
  explanations are just sort of telling a story" (Koopman, 2025).

For example, the model writes the next waypoints as text: (8, 0), (16, 0),
(24, 0), (32, 0), each in meters ahead of the AV and meters to its left. The
example is chosen: waypoints 1 s apart at 8 m/s, on a straight lane.

Four driving VLAs
^^^^^^^^^^^^^^^^^

These are claims by the makers, so the table quotes their words instead of
describing the models. On the slide, a click on a row shows the quotes.

.. list-table::
   :header-rows: 1
   :widths: 18 82
   :class: compact-table

   * - Model
     - What its authors report
   * - DriveVLM
     - "reasoning modules for scene description, scene analysis, and
       hierarchical planning"; a dual version deployed "on a production
       vehicle" (Tian et al., 2025)
   * - EMMA (Waymo)
     - built on "a multi-modal large language model foundation like Gemini";
       outputs "trajectories and 3D locations" "as natural language text".
       Limits it lists: "up to 4" frames, no LiDAR or radar, more compute
       (Hwang et al., 2025)
   * - LINGO-2 (Wayve)
     - "the first closed-loop vision-language-action driving model (VLAM)
       tested on public roads", driving in Central London (Wayve, 2024)
   * - Alpamayo 1 (NVIDIA)
     - named Alpamayo-R1 in its paper: "integrates Chain of Causation
       reasoning with trajectory planning" (NVIDIA, 2025); open weights,
       "ready for non-commercial use" (NVIDIA, Alpamayo-R1-10B model card).
       Newer: Alpamayo 2 Super, with its own model card, and Alpamayo 2 Edge,
       "a 2B-parameter reasoning vision-language-action model" with "64
       waypoints spanning 0.1 through 6.4 seconds" (NVIDIA, Alpamayo 2 Edge
       model card).

A slow model needs a fast partner
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L11/vla.png
   :class: dark-light themed-L11
   :alt: A diagram. Camera images and Text: route, question feed a blue box, Vision-language model, marked slow: about 0.4 s per answer. It writes two outputs: Text out: what it sees and plans; and Coarse trajectory, written as numbers, which goes to a box Fast planner refines it, marked fast: every control step.
   :width: 90%
   :align: center

   A vision-language model and a fast planner.

.. admonition:: Reading the figure
   :class: tip

   - **Inputs (left, gray):** camera images, and text with the route and a
     question.
   - **Vision-language model (blue):** slow, about 0.4 s per answer. It writes
     two outputs.
   - **Text out:** what it sees and plans, in words.
   - **Coarse trajectory:** a rough path, written as numbers. A **fast
     planner** refines it at every control step.

A slow model answers late, so DriveVLM-Dual hands its coarse trajectory to "a
classical planner for high-frequency trajectory refinement" (Tian et al.,
2025). The slide draws the animation 10 times slower than real time.

How far does the AV drive during one answer? At our 8 m/s:

1. DriveVLM's vision-language model, on an NVIDIA OrinX chip in the car, has
   "an average inference speed of 410 ms" (Tian et al., 2025). The AV drives
   0.41 × 8 = 3.3 m per answer.
2. Alpamayo 1 reports 99 ms on an NVIDIA RTX 6000 Pro Blackwell (NVIDIA,
   2025): 0.099 × 8 = 0.8 m.
3. Alpamayo 2 Edge runs on NVIDIA DRIVE AGX Thor-X, a chip made for cars:
   "160 ms to 190 ms depending on the amount of reasoning" (Pavone and
   Ivanovic, 2026): 0.16 × 8 = 1.3 m to 0.19 × 8 = 1.5 m.
4. Our lane keeper steers every 0.05 s: 0.05 × 8 = 0.4 m.

These times are the authors' reports, on different chips, not a comparison of
the models. The slide has a speed slider, and its speed of 8 m/s is chosen for
this example. A slower answer means more road driven before the next one.


.. _l11-lec-scoring:

Scoring a Driver
----------------

The last section gave the newest models, and "Scoring the Clone" showed open
loop and closed loop on our lap. This section applies that lesson to published
results. It covers why open loop misleads, the benchmarks and NVIDIA's
simulator that score in closed loop, and how GP4 scores your own stack.

Benchmarks and NVIDIA's Simulator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A better open-loop score can lose in closed loop, on our lap and on a published benchmark. Only a closed-loop score, where the driver's actions move the car, can judge a driver.

Open loop against closed loop on our lap
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L11/open_closed.png
   :class: dark-light themed-L11
   :alt: Two bar charts. Left, open loop on the expert's recorded lap, mean clone minus expert steering in degrees: bar 1, rust, 0.37; bar 2, green, 0.47. Right, closed loop, test laps finished of 20: bar 1, rust, 5; bar 2, green, 19; bar 3, dark, 20.
   :width: 100%
   :align: center

   The same drivers, scored open loop and closed loop.

.. admonition:: Reading the figure
   :class: tip

   Bar **1** is behavior cloning, bar **2** is DAgger after iteration 6, and
   bar **3** is the expert.

   - **Left, open loop:** the error on a second recorded lap of the expert,
     not used for training: behavior cloning 0.37°, DAgger 0.47°. Behavior
     cloning looks better.
   - **Right, closed loop:** test laps finished, out of 20: behavior cloning
     5, DAgger 19, the expert 20. Behavior cloning is much worse.

On our lap, the clone has the lower open-loop error but finishes fewer laps
than DAgger. In run 6 the clone has the lower open-loop error (0.37° against
0.47°) and finishes 5 laps of 20; DAgger finishes 19. The expert has no
open-loop error: it is the source of the labels.

Behavior cloning has the **lower** open-loop error in all 10 training runs,
and the fewer finished laps in all 10. It fits the expert's own states best.
DAgger's fit also covers the states where the AV drifts, so on the expert's
states alone it fits slightly worse.

Drive our lap
^^^^^^^^^^^^^

The slide lets you drive our lap yourself, in closed loop, with the clone
(behavior cloning), DAgger at iteration 6, or the expert, on any test lap.
With the clone on test lap 18, a wheel leaves the lane at 649 m along the lap.

Closed loop on recorded video
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. figure:: /_static/images/L11/l11_nvidia_closed_loop.png
   :class: white-figure
   :alt: A block diagram of a loop. A box Recorded video, with the human's steering, sends a frame to a box Shift and rotate the frame, which sends an image to an orange box CNN. The CNN sends steering down to a box Vehicle model: update position and heading. That box sends the new pose back up to the shift and rotate box. It also points right to a box: off center by more than 1 m, an intervention, reset to the lane.
   :width: 90%
   :align: center

   NVIDIA's closed loop on recorded video.

.. admonition:: Reading the figure
   :class: tip

   - **Recorded video:** gives a frame.
   - **Shift and rotate the frame:** moves the frame to the pose the car now has.
   - **CNN (orange):** reads the image and gives a steering.
   - **Vehicle model:** updates the position and heading, which gives the new pose that goes back to the frame step.
   - **Intervention:** counted when the car is off center by more than 1 m, then the car is reset to the lane.

NVIDIA tested its network in closed loop before the road, with no simulated
world: it shifts each recorded frame to the new pose (Bojarski et al., 2016).
The loop, as the slide draws it:

1. **Recorded video,** with the human's steering, gives a frame.
2. The frame is **shifted and rotated** to the pose the car now has.
3. The **CNN** reads the image and gives a steering.
4. A **vehicle model** updates the position and the heading, which gives the
   new pose.
5. An **intervention** is counted when the car is off center by more than 1 m,
   and the car is reset to the lane.

NVIDIA's closed loop needs no simulated world: it moves the recorded video to
where the network's steering would have put the car. On our lap, the simulator
plays this role.

What AD-MLP is given
^^^^^^^^^^^^^^^^^^^^

AD-MLP plans from the AV's own past motion and the route command, with no
camera. It gets the AV's past positions (4 frames), its velocity and
acceleration, and the route command (left, straight or right), and outputs the
future positions (6 frames) (Zhai et al., 2023). "73.9% of the nuScenes data
involve scenarios of driving straightforwardly" (Li et al., 2024). The dots on
the slide are not to scale.

A model without cameras scores as well
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

AD-MLP (Zhai et al., 2023) plans from the AV's own past motion and the route
command, "without using any perception or prediction information such as
camera images or LiDAR". Their Table 1, nuScenes, open loop, averaged over 1,
2 and 3 s:

.. list-table::
   :header-rows: 1
   :widths: 36 19 23 22
   :class: compact-table

   * - Planner
     - Cameras
     - Average distance error (m)
     - Collision (%)
   * - UniAD
     - yes
     - 1.03
     - 0.31
   * - VAD-Base
     - yes
     - 0.37
     - 0.14
   * - AD-MLP
     - no
     - 0.29
     - 0.19

AD-MLP, with no cameras at all, has the lowest distance error: 0.29 m. Its
collision rate is between the two. So an open-loop score on nuScenes does not
show that a model sees the road. Li et al. (2024) give a reason: "73.9% of the
nuScenes data involve scenarios of driving straightforwardly", and models
given the AV's speed "tend to rely predominantly on the ego vehicle's status".
Nothing here is closed loop. It tells you how little this open-loop score
measures.

Two benchmarks that score a plan
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NAVSIM and Bench2Drive both score a plan, but they test it in different ways.

- **NAVSIM** (2024) uses real recorded drives. Its authors say: "Our
  simulation is non-reactive, i.e., the evaluated policy and environment do
  not influence each other". The planner is "only queried in the initial frame
  of each scene", and its 4 s plan gets the PDM Score: collisions and leaving
  the drivable area cancel the score, and progress, time to collision and
  comfort are averaged (Dauner et al., 2024). The plan never moves the AV, so
  compounding error cannot show.
- **Bench2Drive** (2024) runs in CARLA: "the first benchmark for evaluating
  E2E-AD systems' multiple abilities in a closed-loop manner", with "44
  interactive scenarios" over "220 routes" (Jia et al., 2024).

NAVSIM is a middle ground: real sensor data and a score that checks the plan,
but the plan never moves the AV. Only a closed loop shows compounding error.

NAVSIM replays, Bench2Drive reacts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NAVSIM replays the other car's recorded motion, and Bench2Drive lets the other
vehicles react to the AV. The slide sketches both.

1. **NAVSIM:** the planner is queried once, at the start. Its 4 s plan stays
   fixed, and the other car's recorded motion is replayed (Dauner et al.,
   2024).
2. **Bench2Drive:** the other vehicles react to the AV, as in a car cutting in
   (Jia et al., 2024).

GP4
~~~

The benchmarks score published drivers in closed loop. GP4 does the same for your own stack: its script scores a drive.

GP4 scores your stack in closed loop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

GP4 runs your stack: your commands decide where the AV goes next. You run your
route twice, once with your EKF pose and once with the true pose, among 40
vehicles and 80 walkers. The script ``tools/evaluate_run.py`` scores each
drive until the AV first comes within 2 m of the goal, and reports:

- route completion: 1 at arrival; otherwise 1 minus the road distance left
  over the route's length;
- collisions and pedestrian hits;
- red-light violations: crossing a stop line on red faster than 1 m/s;
- cross-track error and mean speed.

For grading, the grader runs your code on a held-out route and compares with
the reference solution: route completion at least 0.8 times the reference's,
and no more red-light violations or pedestrian hits than the reference. The
:doc:`GP4 page </assignments/gp4>` has the full rubric.

What GP4's script measures on a drive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The script measures five things on each drive. From ``tools/evaluate_run.py``:

1. the road distance left to the goal (a 2 m circle) over the route's length;
2. a collision;
3. a person inside the box 2.5 m ahead and behind and 1.1 m to each side, with
   the AV above 0.5 m/s;
4. the stop line crossed on red above 1 m/s;
5. the distance to the planned path.

The slide's picture is a sketch.

GP4 route completion
^^^^^^^^^^^^^^^^^^^^

Route completion has three values. All three values on the slide are chosen
for this example, and the slide has a slider for each: the route's length, the
road distance left, and the reference's completion. For example, with a route
of 1200 m, 300 m left, and a reference completion of 1.00:

1. Route completion = 1 − 300 / 1200 = 0.75.
2. Needed: 0.8 × 1.00 = 0.80. The AV fails this part of the rule.

The rule also needs no more red-light violations or pedestrian hits than the
reference.


.. _l11-lec-modular-or-e2e:

Modular or End-to-End?
----------------------

Scoring a Driver gave closed-loop scores and showed why open-loop ones
mislead. This section uses them to compare the two designs: first what
end-to-end costs, then the two designs side by side and how to compare them
fairly, then GP5. Your final report evaluates your modular pipeline, and
end-to-end driving is the optional GP5.

What End-to-End Costs
~~~~~~~~~~~~~~~~~~~~~

The four gains of the first section come with costs, and the same survey lists four. The last is the problem the clone showed on our lap: it drives into states the expert never showed.

Cost 1: hard to open, a black box
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In your stack, you read each topic and find the part that failed. An
end-to-end network has no topics inside to read, so people call it a black
box. Alex Kendall, CEO of Wayve, replies that it is "naive" to expect a
complex intelligent machine to be "strictly interpretable to the point where
you can point to a single line of code" (Kendall, 2025).

Cost 2: no proof of safety
^^^^^^^^^^^^^^^^^^^^^^^^^^

An end-to-end network learns how to drive from data, so no math proves that it
always drives safely. Tests cover only the states someone tried.

Why testing cannot prove safety
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phil Koopman, who studies the safety of self-driving cars, gives two reasons
why testing alone cannot show that a learned driver is safe (Koopman, 2025).

1. **Covering every neuron.** A chip test can exercise every gate and show that
   it is there. A network is different: "if you exercise all the neurons in an
   artificial neural network, it doesn't prove anything".
2. **Driving more miles.** Brute-force testing takes about a billion miles,
   "and you've probably retrained the machine learning 100 times in that
   billion miles. So none of it counts".

The design and the result come apart: "Did the machine learning learn what I
wanted to? I don't know. Let's drive it around and find out".

Two views on proving safety
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The skeptic and the advocate agree on the problem: training data alone does
not make a learned driver safe.

- **Phil Koopman,** who studies the safety of self-driving cars: testing a
  learned driver proves little, since over a billion test miles "none of it
  counts" (Koopman, 2025).
- **Alex Kendall,** CEO of Wayve, which sells end-to-end driving: "we can't
  just pump more data in" and "hope that hallucinations go away". The design
  must be "functionally safe", with "a […] robust […] behavioral safety case"
  (Kendall, 2025).

Both say a learned driver needs a safety argument beyond its data. Kendall
calls building one a matter of "architectural challenges".

Cost 3: rare cases, the long tail
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A long tail means many rare situations, each with few examples in the driving
data. A network that learns only from data learns those cases poorly, and for
end-to-end driving this problem is especially serious. The slide's example is a
stopped car in the lane: one rare situation among many, each with few examples.

A heavy tail, not only a long one
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Koopman separates two problems: a long tail is rare events, and a heavy tail
is a great many different rare events (Koopman, 2025). His words: "Long tail is
rare events, but a heavy tail means there's a lot of things. So maybe this is
once per billion miles, but if you have a billion of them, you're going to see
one every mile. And if you fix it, that doesn't help you".

His example, worked out (the arithmetic is ours, if sightings come
independently, as a Poisson count): an event that happens once per billion
miles, and 100 million miles of driving data.

1. Expected sightings: 100,000,000 / 1,000,000,000 = 0.1.
2. Chance of never seeing it: :math:`e^{-0.1}` = 0.90.

So the data most likely holds no example of it at all; in his words, "you've
never seen it probably".

Cost 4: states the expert never showed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The network learns from the states the expert drove through, but when it
drives, the states it reaches differ from the expert's. Today's running example
measures what that does. The slide shows a straight stretch of test lap 18,
from 558 to 652 m, from the lap data and not as a sketch. The expert stays
within the band its recording covers (0.61 m). The clone drifts out of the
band to the lane limit (1.0 m), where its right wheels reach the line. Offsets
are stretched three times and vehicles are to scale.

Comparing the Designs
~~~~~~~~~~~~~~~~~~~~~

The modular stack and the end-to-end driver can be set side by side, even inside one car. A fair comparison scores both the same way.

The two designs, side by side
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The two designs differ in what they are built from and what they need.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40
   :class: compact-table

   * -
     - Modular (your stack)
     - End-to-end
   * - Built from
     - parts people design, each with its own test
     - one neural network trained on driving data
   * - Between parts
     - messages people chose: boxes, a pose, a path
     - whatever the neural network learned
   * - Trained for
     - each part's own score
     - the driving output
   * - Debugging
     - read each topic, find the part
     - look at outputs and any readable parts inside (UniAD)
   * - Data it needs
     - labels for each part, such as boxes for a detector
     - driving data; for DAgger, an expert that can label any state

Both are tested the same way at the end: closed loop, on the routes and
scenarios that matter.

.. dropdown:: More detail: what two companies say about their own systems
   :class-container: more-detail
   :icon: info
   :name: l11-more-company-claims

   Companies have said where they sit between the two designs. These are
   company statements, quoted with their dates. No outside test has checked
   them.

   - **Tesla, Q4 and FY 2023 Update (an investor update published in 2024):**
     "V12 utilizes end-to-end training". In words: Tesla says its V12 software
     is trained end to end (Tesla, 2024).
   - **Tesla, Q1 2024 Update (published in 2024):** "We believe a scalable and
     profitable autonomy business can be realized through a vision-only
     architecture with end-to-end neural networks, trained on billions of
     miles of real-world data". In words: Tesla says it believes cameras
     alone and end-to-end networks can support a profitable autonomy business
     (Tesla, 2024).
   - **Waymo, blog post of December 9, 2025:** "Its innovative architecture
     provides significant benefits over the pure end-to-end or modular
     approaches." In words: Waymo says its design is better than either pure
     design. It "supports full end-to-end signal backpropagation during
     training", so the error at the output trains all the parts together. It
     also keeps "compact, materialized structured representations like
     objects, semantic attributes, and roadgraph elements", which are readable
     objects and roads inside the network (Waymo, 2025).

   - **Waymo, "10 AI Lessons from Driving 200+ Million Fully Autonomous
     Miles" (August 26, 2026):** it describes "fewer, high-capacity,
     specialized foundation models", not "a single, black box" (Waymo, 2026).

   Waymo's description sits between the modular stack and the end-to-end
   driver: trained end to end, with readable objects and roads inside.

Where the line between them blurs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Real systems are not purely one design or the other, even in the words of an
end-to-end advocate.

- **Modular stacks learn too.** Alex Kendall, CEO of Wayve: "anyone who's
  worth a grain of salt will use deep learning in various parts of the stack"
  (Kendall, 2025).
- **Some sit in between.** Waymo describes "fewer, high-capacity, specialized
  foundation models", not "a single, black box" (Waymo, 2026).
- **Mixing is not free.** In Kendall's view, hybrid approaches "can get the
  worst of both worlds or just add cost and complexity" (Kendall, 2025).

The question is less "which design" than where to draw the line between
learned parts and written rules.

One car, two designs
^^^^^^^^^^^^^^^^^^^^

Either design runs on this car; only the program changes. The slide shows the
Model 3 again, with a switch between "Your stack" and "End-to-end", and
underlined words that you can click. Koopman calls sensors a data choice:
"lots and lots of lower quality data", or "a much smaller amount of very high
quality data" (Koopman, 2025).

Either way, the commands reach the drive units, which "power the wheels"
(Tesla, Emergency Response Guide), and the "electronically-assisted braking and
steering systems" (Tesla, Model 3 Owner's Manual).

If this car ran your stack (a hypothetical):

1. The cameras send their images to the computer.
2. Your parts run there in a chain: perception, then localization, then
   planning, then control.
3. Each part is tuned on its own score.
4. People chose the messages between the parts.

A fair comparison, in four steps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A fair comparison of two drivers needs four steps:

1. **Same routes and scenarios,** none used in training or tuning. Your final
   report does this for your modular pipeline: three scenarios the instructor
   provides, unseen during development.
2. **Closed loop,** with the same metrics: route completion, collisions, red
   lights, as GP4's script reports them.
3. **Several runs,** and report the spread: our clone finished 2 to 9 laps of
   20 depending only on the training run.
4. **Say what each one was given:** sensors, the map, the route, privileged
   information (a state only the simulator knows, like the expert's true
   offset). CARLA's Leaderboard banned "any privilege information offered by
   the CARLA simulator" (CARLA Team, Leaderboard 2.1 criteria).

Handling a new exception
^^^^^^^^^^^^^^^^^^^^^^^^

In Koopman's view, a new exception costs the two designs different work: a few
lines of code, or a data collection job (Koopman, 2025). His example: blue stop
signs, found in parking lots in Hawaii.

- **Modular stack.** "if you notice something weird, it's not so bad writing a
  manual rule to handle it": blue stop signs go into the detector's training
  data, and the planner stays as it is, "because a stop sign's a stop sign".
- **End-to-end.** "if you discover […] an exception, you have to retrain the
  whole thing": the network must learn that blue stop signs are stop signs
  "without it necessarily knowing what a stop sign really is".

"You haven't changed the need to handle the exceptions, but you've converted it
from a programming job of a few lines of code into a data collection job".

.. _l11-lec-gp5:

GP5: An Optional Project
~~~~~~~~~~~~~~~~~~~~~~~~

GP5 is optional and not graded: it keeps your GP1 to GP3 nodes and GP4's planner, and replaces GP4's behavior and controller nodes with a learned model.

The Project
^^^^^^^^^^^

GP5 is an optional end-to-end project on your own stack. It keeps most of your nodes and puts one learned node in place of two.

GP5, an optional project
""""""""""""""""""""""""

**GP5 is optional and not graded:** no points, no bonus, nothing due and
nothing submitted. It does not count toward the group-project grade or the
final report. The full description is on :doc:`the GP5 page
</assignments/gp5>`.

- **What you do:** keep your GP1 to GP3 nodes and GP4's planner, remove GP4's
  behavior and controller nodes, and add one learned model in their place. It
  reads the front camera image and a short text command, and outputs steering,
  throttle and brake.
- **What you get:** no starter code and no reference solution. The GP5 page
  lists the files you create and the GP4 files you reuse.
- **Your team:** your GP4 team. You can show the drive and a comparison table
  to the instructor, by email or in office hours.

Today's lecture gives the ideas behind GP5, and GP4's closed loop and scoring
script test your model.

GP5 in the node graph
"""""""""""""""""""""


.. figure:: /_static/images/L11/l11_gp5_nodes.png
   :class: white-figure
   :alt: A node graph. A large rounded box tagged 1, GP1 to GP3, holds five boxes: sensor_manager, detector_node, localization_node, fusion_node and tracker_node. An arrow labeled tracks, pose goes from it to planner_node. From planner_node, a dashed arrow goes to two crossed-out dashed boxes, behavior_node then controller_node, tagged 2. A solid arrow from planner_node and an arrow labeled camera image, speed from the GP1 to GP3 box both go to a blue box, vla_node, tagged 3. The label route command sits beside these arrows. An arrow labeled vehicle command leaves vla_node.
   :width: 95%
   :align: center

   GP5 replaces two nodes with one.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** your GP1 to GP3 nodes, kept, and GP4's planner_node.
   - **Tag 2:** behavior_node and controller_node, crossed out: removed.
   - **Tag 3:** vla_node, added. It reads the camera image and the speed, takes the route command, and publishes the vehicle command.

GP5 replaces two nodes with one learned model:

1. **Kept:** your GP1 to GP3 nodes (``sensor_manager``, ``detector_node``,
   ``localization_node``, ``fusion_node``, ``tracker_node``) and GP4's
   ``planner_node``.
2. **Removed:** GP4's ``behavior_node`` and ``controller_node``.
3. **Added:** ``vla_node``.

The GP1 to GP3 nodes send tracks and the pose to the planner. ``vla_node``
reads the camera image and the speed, takes the text command from the route,
and publishes the vehicle command.

GP5's Model
^^^^^^^^^^^

The project adds one node, ``vla_node``, in place of your behavior and controller nodes. Inside it is a model of which you train only one part.

GP5's model in three parts
""""""""""""""""""""""""""


.. figure:: /_static/images/L11/l11_gp5_model_parts.png
   :class: white-figure
   :alt: A block diagram. A box Front camera image feeds a dashed box CLIP image encoder (frozen), which gives a box 512. A box follow the road feeds a dashed box CLIP text encoder (frozen), which gives a box 512. Under the text encoder, six small squares in a row, the first one filled orange, are labeled six constant vectors. A box Speed gives a box 1. The three boxes 512, 512 and 1 feed a box Joined input: 512 + 512 + 1 = 1,025. It feeds a blue box Small decoder (trained), and a label says 3 numbers: steering, throttle, brake.
   :width: 95%
   :align: center

   GP5's model: two frozen encoders, one trained decoder.

.. admonition:: Reading the figure
   :class: tip

   - **Dashed boxes:** the two CLIP encoders, frozen. You do not train them.
   - **Six squares:** the six constant vectors, one for each fixed command. One is chosen (orange).
   - **Joined input:** the two 512-number vectors and the speed, 1,025 numbers.
   - **Blue box:** the small decoder, the part you train. It gives steering, throttle and brake.

GP5's model has two frozen encoders, one trained decoder and six fixed
commands.

- **Two frozen CLIP encoders** (CLIP is a pre-trained image and text model),
  one for the image and one for the text command, each giving 512 numbers.
  You do not train them.
- **One input:** the two vectors and the speed, 512 + 512 + 1 = 1,025 numbers.
- **A small decoder** that you train, a multi-layer perceptron (a few fully
  connected layers). It gives three numbers (steering, throttle and brake),
  kept in the ranges of the vehicle command.
- **Six fixed commands,** such as "follow the road" and "turn left at the
  intersection". With six phrases, the text input is a choice among six
  constant vectors.

GP5's model, drawn
""""""""""""""""""


.. figure:: /_static/images/L11/l11_gp5_model_drawn.png
   :class: white-figure
   :alt: A block diagram with three numbered tags. Three input boxes, image, command and speed. Image goes to a box CLIP image and command goes to a box CLIP text; a circled tag 1 sits between these two boxes. Arrows labeled 512 from each CLIP box, and an arrow labeled 1 from speed, go to a dashed box 1,025, tagged 2. An arrow leads to a blue box decoder, tagged 3, and then to an output box: steer, throttle, brake.
   :width: 95%
   :align: center

   GP5's model, drawn.

.. admonition:: Reading the figure
   :class: tip

   - **Tag 1:** two frozen CLIP encoders, 512 numbers each.
   - **Tag 2:** with the speed, one input of 512 + 512 + 1 = 1,025 numbers.
   - **Tag 3:** the decoder, the only part you train.

The slide draws how the image, the command and the speed become one input and
then a vehicle command. Its three tags:

1. two frozen CLIP encoders, 512 numbers each;
2. with the speed, one input of 512 + 512 + 1 = 1,025 numbers;
3. the decoder is the only part you train.

Where GP5's model sits
""""""""""""""""""""""

GP5's model fits into the family of end-to-end drivers from this lecture. It
is close to conditional imitation: a camera-driven policy with a six-way
command. It is much smaller than DriveVLM or Alpamayo, and it does not write
text.

Where that leaves us
^^^^^^^^^^^^^^^^^^^^

.. admonition:: Where that leaves us
   :class: tip

   - Behavior cloning is supervised learning on an expert's drive. Our clone
     (run 6) copied the expert within 0.37° and finished 5 test laps of 20;
     ten runs finish 2 to 9.
   - Its error grew from 0.44° near the center to 2.41° near the lane's edge:
     compounding error, in states the recording never showed.
   - DAgger adds those states, labeled by the expert: 19 of 20 laps, in 10 of
     10 training runs.
   - Junctions need the route's command. End-to-end neural networks range from
     TransFuser to UniAD to VLAs; their authors report 0.41 s (DriveVLM) and
     0.099 s (Alpamayo 1), on different chips.
   - Judge any driver in closed loop: open-loop scores favored the clone that
     failed.


.. _l11-lec-next-class:

Next Class
----------

L12, Thursday, December 10, 2026: Simulation, Scenario-Based Testing and World
Models. It covers where closed-loop tests like today's come from, and how to
choose them. L11 trained a driver from an expert: three ways it fails, four
fixes, the other ways to learn a driver, and why only a closed-loop test can
judge one.

- **Before then:** run the five hands-on parts: ``road``, ``bc``, ``shift``,
  ``dagger`` and ``eval``.
- **December 10 and after:** Quiz 5 is that day, and GP4 is due at L12. The
  final report is due on December 17; it was posted with GP4 on November 19.
  GP5, the end-to-end project, is optional and not graded: nothing is due.


