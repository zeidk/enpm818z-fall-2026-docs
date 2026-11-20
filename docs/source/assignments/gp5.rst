====================================================
GP5: Vision-Language-Action Driving (Optional)
====================================================

.. important::

   **GP5 is optional and not graded.** It gives no points and no bonus, and
   nothing you do here counts toward your grade, the group-project grade or
   the Final Report. Nothing is due and nothing is submitted. It is for teams
   that want to try end-to-end driving on the pipeline they built.

.. card:: GP5: At a Glance
   :class-card: sd-shadow-sm

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Status**
        - Optional. Not graded. No points, no bonus.
      * - **Deadline**
        - None.
      * - **Submission**
        - None. You can show your result to the instructor (see
          :ref:`gp5-show`).
      * - **Lectures**
        - :doc:`L9 </lectures/lecture9/l9_index>` (Motion Planning, behavior)
          and :doc:`L10 </lectures/lecture10/l10_index>` (Trajectory
          Generation & Control): the parts of GP4 that your model replaces.
          L11, End-to-End Driving, VLA & Imitation Learning (taught on
          Thursday, December 3): the ideas behind GP5.
      * - **Team size**
        - Your GP4 team.
      * - **Starter code**
        - None. We have not written GP5 starter code or a reference solution.
          This page gives no measured results for that reason.
          :ref:`gp5-setup` lists the files you create and the GP4 files you
          reuse.
      * - **Prerequisites**
        - Your GP1 to GP3 pipeline working. GP4 helps: it gives you the
          closed loop and the scoring script.


Overview
--------

In GP1 to GP4 you built a **modular** pipeline: separate nodes sense, detect,
fuse, localize, plan and control. In GP5 you replace the last two stages with
one learned model. It reads the front camera image and a short text command
such as "turn left at the intersection", and it outputs the steering,
throttle and brake.

A model that takes images and language and outputs actions is called a
**vision-language-action (VLA)** model. Research systems such as DriveVLM
and NVIDIA's Alpamayo are VLA models built on large language models. Yours is
a much smaller one. It does not generate text, and it reads one of only six
fixed phrases (listed in Task 1). A text encoder turns each phrase into a
vector, so with six phrases the text input is a choice among six constant
vectors. Your model is a camera-driven policy with a six-way command, close
to the conditional imitation learning in the first reading below. Keep this in
mind when you compare it with the real VLA systems.

The model has three parts: two encoders from CLIP (a pre-trained model) and
an action decoder that you train. The figure follows one camera frame through
them, from left to right.

.. figure:: /_static/images/GP5/gp5_model.svg
   :alt: A diagram, left to right. Three inputs: the front camera image, the text command (for example "turn left at the intersection") and the speed in m/s. The image goes to the CLIP image encoder and the command to the CLIP text encoder; both are blue and marked frozen. Each encoder gives 512 numbers, and the speed is 1 number. The three are joined, inside a dashed outline, into one input of 1,025 numbers. It goes to the action decoder, a small MLP in orange marked trained. An arrow down from the decoder leads to a VehicleCmd box: steer from -1 to 1, throttle from 0 to 0.75, brake from 0 to 1. A legend: blue, frozen, the weights do not change; orange, trained, the only weights you train.
   :align: center
   :width: 100%

   The GP5 model.

.. admonition:: Reading the figure
   :class: tip

   **The inputs (gray, left).** For every camera frame, your ``vla_node``
   has three inputs. The image comes from the front camera, on
   ``/carla/camera/rgb/image``. The speed, in m/s, comes from
   ``/carla/speedometer``. The text command is one of the
   six phrases of Task 1. It changes only when the route reaches a new
   ``RoadOption``, so long runs of frames share the same phrase.

   **The two encoders (blue).** CLIP was trained on 400 million images
   paired with text from the internet (Radford et al., in the readings
   below). It has two encoders, one for images and one for text, and each
   turns its input into a vector of 512 numbers. The training compared each
   image with many texts and taught the encoders to give the matching pair a
   higher similarity score (the cosine of the angle between the two vectors)
   than the pairs that do not match. GP5 uses these vectors as they are, so
   you do not change CLIP. The padlock says both encoders are **frozen**: their
   weights stay as downloaded and get no gradient while you train.

   **The joined input (dashed outline).** Your code puts the image vector,
   the text vector and the speed one after the other: 512 + 512 + 1 = 1,025
   numbers, and this is all the decoder sees. CLIP's two vectors, read as
   the ``image_embeds`` and ``text_embeds`` of the model's output (Task 2),
   are scaled to length 1, so their numbers are small: the root mean square of
   512 numbers whose squares add up to 1 is the square root of 1/512, about
   0.044. A speed of several m/s would be far larger than any of them, which
   is why Task 2 asks you to scale the speed. Use the same scaling in
   training and in the node.

   **The action decoder (orange).** This is a small MLP (a multi-layer
   perceptron: a few fully connected layers), and it is the only part that
   learns. It reads the 1,025 numbers and its last layer gives three. Your
   code squashes them into the ranges shown below it. You choose the
   number and size of its hidden layers.

   **The output (below the decoder).** The three numbers fill one
   ``ads_msgs/VehicleCmd``, which the node publishes on
   ``/control/vehicle_cmd`` once per camera frame. ``steer`` runs from -1
   to 1 and is positive to the left, the opposite of CARLA's sign (see
   "Mind the steering sign" in Task 1). ``throttle`` runs from 0 to 0.75,
   the ``max_throttle`` in the ``controller_config.yaml`` of GP4's starter
   code. CARLA's agent,
   your expert in Task 1, caps its own throttle at 0.75 too, so your data
   never asks for more. ``brake`` runs from 0 to 1.

   **What changes from frame to frame.** The image and the speed change at
   every frame. The text vector does not: with only six phrases, there are
   only six text vectors. You can compute them once and skip the text
   encoder (the speed-up in Task 2).

.. admonition:: Why not train CLIP too?
   :class: note

   CLIP ViT-B/16 has about 150 million parameters (149,620,737, counted in
   the ``transformers`` library). Training all of them needs much more data
   and GPU time than a course project has. A decoder with two hidden layers
   of 256, the example size of Task 2, has 329,219 parameters:
   (1,025 × 256 + 256) + (256 × 256 + 256) + (256 × 3 + 3) weights and
   biases.


.. _gp5-show:

What you can do with your result
--------------------------------

There is no submission, so there is nothing to upload. A team that finishes
Task 4 or Task 5 can show the drive and its comparison table to the
instructor: write to ``zeidk@umd.edu`` or come to office hours (by
appointment). Ask the instructor first if you want to mention GP5 in your
Final Report.


Learning Objectives
-------------------

After GP5, you can:

- Record expert driving demonstrations from CARLA, with the camera image,
  the controls, the speed and a text command for every frame.
- Use a pre-trained vision-language model (CLIP) as a frozen feature
  extractor for driving.
- Train a behavior-cloning model that maps those features to steering,
  throttle and brake.
- Condition the model on a text command, and test whether it follows
  different commands at the same junction.
- Run the model in the GP4 closed loop and score it with the GP4 script.
- Compare the learned driver with your modular GP4 driver, and explain the
  failures of each.


Your Pipeline in GP5
--------------------

Keep the GP1, GP2 and GP3 nodes and GP4's ``planner_node``. Remove GP4's
``behavior_node`` and ``controller_node``, and add a ``vla_node`` in their
place. Make your own launch file: copy ``gp4_launch.py`` and delete the two
nodes. Keep the planner for two reasons. The scoring script reads the
planner's ``/planning/path`` to know your route, and your route is also where
the text commands come from.

.. list-table::
   :widths: 24 76
   :header-rows: 1
   :class: compact-table

   * - **What**
     - **How the node does it**
   * - Image in
     - Subscribe to ``/carla/camera/rgb/image``, the front camera topic that
       GP2's ``detector_node`` reads by default.
   * - Speed in
     - Subscribe to ``/carla/speedometer``, the wheel-speed reading that
       GP4's ``ground_truth.py`` publishes (m/s in ``twist.linear.x``).
   * - Command in
     - One of the six phrases of Task 1. You decide how it reaches the node,
       for example on a topic you create.
   * - Command out
     - Publish one ``ads_msgs/VehicleCmd`` per camera frame on
       ``/control/vehicle_cmd``. ``steer`` is between -1 and 1 and **positive
       turns left**. ``throttle`` is between 0 and 0.75, the
       ``max_throttle`` in the ``controller_config.yaml`` of GP4's starter code.
       The controller is gone in GP5, so your node must keep the throttle at
       or under 0.75 itself. ``brake``
       is between 0 and 1.
   * - Lock step
     - Set the header stamp of each ``VehicleCmd`` to the stamp of the frame
       it answers, as GP4 Task 1 describes. Your GP1 ``sensor_manager`` waits
       for the command before it ticks the world, so a slow model slows the
       run but does not change what the car does. It ticks anyway after
       ``cmd_timeout_s`` (2.0 s by default) and logs the timeout.


.. _gp5-setup:

Setting Up the Project
----------------------

GP5 has no starter: you create every new file yourself. It runs on your GP4
code, so start from your GP4 submission.

1. Start the ``gp5`` branch from your GP4 submission:

   .. code-block:: bash

      cd ~/enpm818z_ws/src/GP1_TeamX && git checkout -b gp5 gp4-final

2. Install the Python packages that GP1 to GP4 did not need: ``torch``,
   ``transformers`` and ``Pillow`` for the model, and ``networkx`` and
   ``shapely`` for CARLA's ``agents`` module (its ``requirements.txt`` lists
   them):

   .. code-block:: bash

      python3 -m pip install --user --break-system-packages torch transformers Pillow networkx shapely

   ``--user`` and ``--break-system-packages`` work as in GP2. We have not
   tested this install on the course machines. Check that PyTorch sees your
   GPU; this prints ``True`` when it does:

   .. code-block:: bash

      python3 -c "import torch; print(torch.cuda.is_available())"

3. Make CARLA's ``agents`` module importable. Task 1's expert,
   ``BasicAgent``, and ``GlobalRoutePlanner`` are in it. The ``carla``
   package that ``pip`` installs (0.9.16) does not include it, so point
   Python to the copy that comes with CARLA:

   .. tab-set::

      .. tab-item:: Native (22.04)
         :sync: native

         .. code-block:: bash

            echo 'export PYTHONPATH="$PYTHONPATH:$HOME/carla/CARLA_0.9.16/PythonAPI/carla"' >> ~/.bashrc
            source ~/.bashrc

      .. tab-item:: Docker (24.04)
         :sync: docker

         Copy the module out of the CARLA container once (``docker cp``
         works while the container is stopped too):

         .. code-block:: bash

            mkdir -p ~/carla_agents
            docker cp carla-server:/workspace/PythonAPI/carla/agents ~/carla_agents/
            echo 'export PYTHONPATH="$PYTHONPATH:$HOME/carla_agents"' >> ~/.bashrc
            source ~/.bashrc

   Check:

   .. code-block:: bash

      python3 -c "from agents.navigation.basic_agent import BasicAgent; print('agents OK')"

4. Create the new files of the folder structure below. The names are ours:
   any names work if your ``setup.py`` and launch file use them.

5. Add the node to ``setup.py``, in ``console_scripts``:

   .. code-block:: python

      'vla_node = ads_pipeline.vla_node:main',

   In ``gp5_launch.py``, give ``vla_config.yaml`` to the node the way
   ``gp4_launch.py`` gives ``controller_config.yaml`` to the controller: a
   launch argument that names the YAML file, passed as the node's
   ``parameters``.

6. Keep the data out of git: add ``gp5_data/`` to ``.gitignore``. Frames,
   labels and model checkpoints all go there.

7. The first time you load CLIP, ``from_pretrained`` downloads
   ``openai/clip-vit-base-patch16`` to ``~/.cache/huggingface``. Load it
   once while you are online, before you need it in the car.

Folder Structure
~~~~~~~~~~~~~~~~

GP5 adds these files to your repository, on the ``gp5`` branch. Everything
else stays as you left it in GP4.

.. code-block:: text

   GP1_Team{X}/
   ├── ads_pipeline/
   │   ├── ads_pipeline/
   │   │   ├── sensor_manager.py      # yours, from GP1 to GP4: unchanged
   │   │   ├── ground_truth.py        # Given in GP4: /carla/speedometer
   │   │   ├── planner_node.py        # Given in GP4: /planning/path
   │   │   ├── vla_model.py           # Task 2: yours, new
   │   │   └── vla_node.py            # Task 4: yours, new
   │   ├── config/
   │   │   └── vla_config.yaml        # Task 4: yours, new
   │   ├── launch/
   │   │   ├── gp4_launch.py          # Given in GP4
   │   │   └── gp5_launch.py          # Task 4: yours, new
   │   ├── routes/
   │   │   ├── <rig>.yaml             # Given in GP4: your test route
   │   │   └── town01_points.json     # Given in GP4: Task 1's spawn points
   │   ├── tools/evaluate_run.py      # Given in GP4: Task 5's scores
   │   └── setup.py                   # + vla_node
   ├── gp5/
   │   ├── collect_expert.py          # Task 1: yours, new
   │   ├── dataset.py                 # Task 2: yours, new
   │   └── train.py                   # Task 3: yours, new
   └── gp5_data/                      # not in git: your data and checkpoints

The ``gp5/`` scripts are plain Python, not ROS 2 nodes: they talk to CARLA
directly (Task 1) or only read files (Tasks 2 and 3).

Where each file comes from
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 20 50
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **Status**
     - **What it does**
   * - ``gp5/collect_expert.py``
     - **Yours, new** (Task 1)
     - Drives Town01 routes with ``BasicAgent`` and saves, for every frame,
       the image, the controls, the speed, the text command and the episode
       number. Mount the camera as your rig does (``carla_config.yaml``:
       position, image size, field of view), so the training images look
       like the ones the node sees.
   * - ``gp5/dataset.py``
     - **Yours, new** (Task 2)
     - A PyTorch ``Dataset`` over ``gp5_data/``: one item per frame.
   * - ``ads_pipeline/vla_model.py``
     - **Yours, new** (Task 2)
     - The model: frozen CLIP, the joined input and the decoder. It lives in
       the package so that both ``train.py`` and ``vla_node.py`` import
       the same code.
   * - ``gp5/train.py``
     - **Yours, new** (Task 3)
     - Trains the three models of the ablation and reports the validation
       MAE. Saves each model to ``gp5_data/``.
   * - ``ads_pipeline/vla_node.py``
     - **Yours, new** (Task 4)
     - Reads the camera, the speed and the command, runs the model, and
       publishes one ``VehicleCmd`` per camera frame (Your Pipeline in GP5).
   * - ``config/vla_config.yaml``
     - **Yours, new** (Task 4)
     - The node's settings: the checkpoint path, the speed scale used in
       training, and the 0.75 throttle limit.
   * - ``launch/gp5_launch.py``
     - **Yours, new** (Task 4)
     - A copy of ``gp4_launch.py`` without ``behavior_node`` and
       ``controller_node``, and with ``vla_node``.
   * - ``ground_truth.py``, ``planner_node.py``, ``gp4_launch.py``,
       ``routes/``, ``tools/evaluate_run.py``
     - Given in GP4
     - Used as they are. GP5 changes none of them.
   * - ``sensor_manager.py`` and your GP2 and GP3 nodes
     - Yours, from GP1 to GP4
     - Used as they are.


Task 1: Collect Expert Data
---------------------------

**Goal:** record driving that the model can copy. The expert is CARLA's own
agent.

For every frame, record:

- the front camera image;
- the steering, throttle and brake the expert applied;
- the car's speed;
- a text command;
- the number of the driving run (the "episode"), which you need in Task 3.

**The text commands.** CARLA's ``GlobalRoutePlanner`` gives each waypoint of
a route a ``RoadOption``. The ``agents`` module in CARLA's ``PythonAPI/carla``
folder also has ``BasicAgent``, which drives a route and exposes the
``RoadOption`` of the waypoint it is steering to. Map each ``RoadOption`` to
one phrase:

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - ``RoadOption``
     - Text command
   * - ``LANEFOLLOW``
     - follow the road
   * - ``LEFT``
     - turn left at the intersection
   * - ``RIGHT``
     - turn right at the intersection
   * - ``STRAIGHT``
     - go straight through the intersection
   * - ``CHANGELANELEFT``
     - change to the left lane
   * - ``CHANGELANERIGHT``
     - change to the right lane

``RoadOption`` also has ``VOID``, for no option. Map it to "follow the road".
Town01's roads are one lane each way (GP4, Task 2), so the two lane-change
phrases may never appear in Town01 data. Count your frames per phrase before
you train.

.. admonition:: Mind the steering sign
   :class: warning

   CARLA's ``VehicleControl.steer`` is positive to the **right**. GP4's
   ``VehicleCmd.steer`` is positive to the **left**. Pick one convention for
   your dataset and your model's output, and convert once, in one place.
   A wrong sign drives the car off the road at the first bend.

**Choosing routes.** Train and test on different routes. Your test route is
your rig's ``routes/<rig>.yaml`` from GP4. Collect the training data on
other Town01 routes (``routes/town01_points.json`` lists the spawn points),
and keep your test route out of it. Town01 is small, so some roads will
overlap. Say how much in your comparison.

**Variety.** Vary the weather with CARLA's weather presets (GP2 uses
``ClearNoon`` and ``ClearNight``), and the traffic. How many frames you need
is not known: we have not trained this model, so we cannot give a minimum.
Watch the model's error on a validation set (Task 3) and collect more when it
stops improving.

.. admonition:: Data quality tips
   :class: tip

   - **Drop most stopped frames.** At 20 Hz (GP1's ``fixed_delta_seconds`` is
     0.05 s), a car that waits 30 s at a red light gives 600 almost identical
     frames. Keep only a fraction of them.
   - **Balance the commands.** Turns are rarer than lane following. Collect
     extra data at junctions, or give the turn frames more weight when you
     train.


Task 2: Build the Model
-----------------------

**Goal:** a PyTorch model with the three parts of the Overview.

What the model does, part by part (you write the code):

- **CLIP, frozen.** Load ``openai/clip-vit-base-patch16`` with
  ``from_pretrained`` and freeze it: its weights get no gradient.
- **Two vectors.** CLIP turns the camera image into an image vector and the
  command into a text vector, 512 numbers each, already scaled to length 1.
- **One input.** Join the two vectors and the speed in m/s:
  512 + 512 + 1 = 1,025 numbers. Scale the speed the same way in training
  and in the node.
- **The decoder.** A small MLP that you train. Its last layer gives three
  numbers.
- **The command's ranges.** Squash the three numbers into the ranges of
  ``VehicleCmd``: steer from -1 to 1, throttle from 0 to 0.75 and brake
  from 0 to 1.

A size check: with two hidden layers of 256, the decoder has
(1,025 × 256 + 256) + (256 × 256 + 256) + (256 × 3 + 3) = 329,219
trainable parameters, while CLIP's 149,620,737 stay frozen.

.. admonition:: A version trap
   :class: tip

   In recent ``transformers`` versions (5.19.0 here),
   ``get_image_features`` returns an output object, not a tensor. Read the
   ``image_embeds`` and ``text_embeds`` of the model's output instead.

**What you write:** the model, a dataset class that loads the images, commands, speeds
and controls of Task 1, the training loop, and your choice of hidden size,
learning rate, dropout and batch size. We have no tested values to give you.

.. admonition:: A speed-up
   :class: tip

   The text encoder sees only six phrases. Compute their six vectors once,
   keep them, and skip the text encoder during training and driving.


Task 3: Train and Validate
--------------------------

**Goal:** a trained model, and offline numbers for it.

- Train with an MSE loss on the three outputs and an optimizer such as AdamW.
  Stop when the validation loss stops improving.
- **Split by episode, not by frame.** Consecutive frames are almost the same
  image. If neighbors land in both the training and the validation set, the
  validation loss looks good for the wrong reason. Put each whole run in
  exactly one of train, validation and test.
- Report the mean absolute error (MAE) of steering, throttle and brake on the
  validation set.

**Ablation (three models).** Train and report all three:

1. **Vision only:** feed ``[image vector, 512 zeros, speed]``. This is plain
   behavior cloning.
2. **Full VLA:** image, text and speed.
3. **Language only:** no image. We expect this one to do poorly, which would
   confirm that the full model uses the image. We have not run it.


Task 4: Drive It
----------------

**Goal:** your ``vla_node`` drives your rig's GP4 route in the closed loop.

Run your launch file (Your Pipeline in GP5) with the model in place of the
behavior and controller nodes. Drive your rig's route
from ``routes/<rig>.yaml``, with the same traffic settings as your GP4 runs
(``traffic.vehicles`` and ``traffic.walkers`` in your YAML), so that the two
comparisons are fair.

The traffic differs from run to run, even with the same seed (GP4, Task 5),
so run the VLA several times and say how many.

**Where the command comes from while driving.** The model needs the text
command at every frame. Compute it from your route in the same way as in
Task 1, for example with ``GlobalRoutePlanner`` between your route's start
and goal. GP4 forbids ``GlobalRoutePlanner`` inside the GP4 planner node
because the planner is the thing GP4 grades. In GP5, the planner node is
unchanged and the model only follows commands.


Task 5: Compare and Write Up
----------------------------

**Goal:** say what the learned driver does better and worse than your GP4
driver, with numbers.

Score each VLA run with GP4's script, ``python3 -m tools.evaluate_run --bag
<run> --out <file>.json``. It reports route completion, collisions,
pedestrian hits, red-light violations, cross-track error and mean speed. Keep
the topics that script reads in your bag: ``/ground_truth/ego``,
``/ground_truth/collision``, ``/ground_truth/objects``, ``/planning/path``
and ``/ground_truth/traffic_light``. The cross-track error is measured against the planner's
path, which the model does not read. It still tells you how far the car
drove from the route.

Measure one more number yourself: the time the model takes per frame, and the
GPU you measured it on.

.. list-table::
   :widths: 40 30 30
   :header-rows: 1
   :class: compact-table

   * - **Metric**
     - **GP4 (modular)**
     - **GP5 (VLA)**
   * - Route completion
     - your result
     - your result
   * - Collisions and pedestrian hits
     - your result
     - your result
   * - Red-light violations
     - your result
     - your result
   * - Cross-track error and mean speed
     - your result
     - your result
   * - Model time per frame
     - not applicable
     - your result

Then write down, for yourself or for the instructor:

1. The three ablation results of Task 3.
2. The table above, and what it shows.
3. At least three failures of the VLA driver. For each: what happened, why
   your modular pipeline did better or worse, and what the VLA driver would
   need to avoid it.
4. A test of the command: at the same junction, give "turn left at the
   intersection" in one run and "go straight through the intersection" in
   another, and say whether the car does what it is told.
5. Your view: which approach is more promising, and why.

.. note::

   The goal is not to beat your modular pipeline. We expect a small model
   trained on little data to do worse on the rules, such as stopping at a red
   light, because no part of it encodes a rule: it copies what the expert
   did. We have not measured this. The goal is to see the trade-offs and the
   failures of end-to-end driving, and what your runs show is your own
   result.


Hardware
--------

The hardware table in the :doc:`syllabus </syllabus/index>` applies. CARLA,
your GP2 detector and CLIP will share one GPU. We have not measured how much
memory the three need together.
You need ``torch``, ``transformers`` and ``Pillow``, besides the packages of
GP1 to GP4 (:ref:`gp5-setup`, step 2).


Further Reading
---------------

- **Conditional imitation learning:** Codevilla, F., Müller, M., López, A.,
  Koltun, V. and Dosovitskiy, A. (2018). *End-to-end Driving via Conditional
  Imitation Learning.* ICRA 2018. A driving policy that follows a high-level
  command, as yours does.
- **DAgger:** Ross, S., Gordon, G. and Bagnell, J. A. (2011). *A Reduction of
  Imitation Learning and Structured Prediction to No-Regret Online Learning.*
  AISTATS 2011 (arXiv:1011.0686). How to fix the drift of a cloned policy.
- **DriveVLM:** Tian, X. et al. *DriveVLM: The Convergence of Autonomous
  Driving and Large Vision-Language Models.* CoRL 2024 (arXiv:2402.12289).
- **Alpamayo-R1:** NVIDIA (2025). *Alpamayo-R1: Bridging Reasoning and Action
  Prediction for Generalizable Autonomous Driving in the Long Tail.*
  arXiv:2511.00088.
- **LINGO-2:** Wayve (2024). *LINGO-2: Driving with Natural Language.*
  https://wayve.ai/thinking/lingo-2-driving-with-language/
- **RT-2:** Brohan, A. et al. (2023). *RT-2: Vision-Language-Action Models
  Transfer Web Knowledge to Robotic Control.* CoRL 2023 (arXiv:2307.15818).
  A VLA model for robot arms.
- **CLIP:** Radford, A. et al. (2021). *Learning Transferable Visual Models
  From Natural Language Supervision.* The source of the frozen encoders.
