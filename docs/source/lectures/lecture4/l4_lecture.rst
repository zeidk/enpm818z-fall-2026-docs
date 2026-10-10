====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L4, the slides shown in class and
   the reading slides that go with them, in the same order and with the same
   sections. They add what the speaker notes say aloud, so you can read them
   at home. Material the deck keeps in its appendix (one neuron, learning the
   weights, activations, convolution in detail, AP in detail, decoding one
   YOLO cell, word vectors, YOLO sizes) is on :doc:`the appendix page
   <l4_appendix>`.

.. important::

   **This is not an AI lecture.** It is about how an automated vehicle finds
   the objects around it: cars, people, signs. The networks are tools. You
   learn what you need to read their output, grade it, and choose one for an
   AV, not how to invent new ones. The basics of neural networks are in
   :doc:`the appendix <l4_appendix>` ("CNN Fundamentals").


.. _l4-lec-introduction:

Introduction
------------

The Step We Skipped
~~~~~~~~~~~~~~~~~~~

In Lecture 3, the AV predicted its position with its wheels and IMU, and each
time the camera matched an emergency exit sign against the HD map, the Kalman
filter updated. In the worked example, the sign match put the AV **53.0 m**
into the tunnel, with :math:`\sigma = 1` m.

We took that measurement as given. But a camera does not report "exit sign,
53.0 m". It reports pixels. Something has to find the sign in the image and
draw a box around it. That something is a **detector**: it finds the objects
in an image and draws a box around each one. This lecture builds it.

.. figure:: /_static/images/L4/lecture_bridge.png
   :alt: A flowchart. Top row, joined by arrows: Camera image, pixels only, labeled L2; Detector, a box around the exit sign, highlighted in green and labeled today (L4); Distance, from the size of the box, labeled L2 camera model; Kalman update, 53.0 m, sigma = 1 m, labeled L3. A second arrow leaves the detector for a bottom row: Cars, people, a box around each one; then Tracking, one Kalman filter per object, labeled L5.
   :width: 90%
   :align: center

   Where the detector sits. The **camera image** holds pixels only (L2). The
   **detector** (today, highlighted) puts a box around the exit sign. The
   camera model from L2 turns the **size of the box** into a distance, and
   that distance is the measurement in L3's **Kalman update** (53.0 m,
   :math:`\sigma = 1` m). The same detector also boxes **cars and people**,
   and L5 follows each one over time with one Kalman filter per object.

- **From the box to a distance.** The HD map knows the sign's real size. The
  farther away the sign is, the smaller its box. The camera model from
  Lecture 2 turns that size into a distance, and that distance is what the
  Kalman filter uses.
- **The same detector boxes cars and people.** Next week, in Lecture 5, we
  follow each of them over time with one Kalman filter per object.
- **The classes are fixed by training.** The detectors in this lecture
  learned the 80 classes of the **COCO** dataset, a large set of everyday
  photos described in :ref:`l4-lec-pretrained`. A stop sign is one of them; an exit sign is not. To find
  exit signs, you would fine-tune the detector on your own images.

The detector is one part of a larger block of the AV's software, called
perception.


.. _l4-lec-perception:

Perception
----------

.. admonition:: Definition: perception
   :class: note

   Turning raw sensor data into a **description of the world** that the rest
   of the AV can act on: which objects are around, where they are, and where
   the AV may drive.

The detector answers the first two questions: which objects, and where. Where
the AV may drive comes from other parts, such as segmentation, next week.

.. figure:: /_static/images/L4/stack_pipeline.png
   :alt: Five boxes in a row joined by arrows: Sensors, Perception (highlighted in green), Prediction, Planning and Control, with the lecture that covers each below them: L2; L4, L5; L8; L9; L10. A second, curved arrow runs from Perception directly to Planning, over Prediction.
   :width: 90%
   :align: center

   Perception in the AV software. Lecture 2 gave you the sensors. Perception
   (L4 and L5) is the next box: pixels and points go in, a list of objects
   comes out. Then come prediction (L8), planning (L9) and control (L10).
   The curved arrow is a shortcut from perception straight to planning.

Two arrows leave perception:

- **Objects go to prediction first**, because the planner needs to know where
  they will be, not only where they are.
- **The drivable area, the lanes and the traffic lights go straight to
  planning.** Nothing predicts a red light.


.. _l4-lec-four-outputs:

The Four Outputs Perception Hands to the AV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Perception feeds several parts of an AV: prediction, planning and control all
use what it produces.

.. list-table::
   :widths: 25 45 30
   :header-rows: 1
   :class: compact-table

   * - **Output**
     - **What it says**
     - **Used by**
   * - **Objects**
     - class, position, size, heading, speed
     - prediction, planning
   * - **Drivable area**
     - where the AV may drive
     - planning
   * - **Lanes and markings**
     - where each lane is
     - planning, control
   * - **Lights and signs**
     - red or green, speed limit
     - planning

- **Objects:** every car, pedestrian and cyclist, with its class, where it
  is, how big it is, which way it points and how fast it moves.
- **Lights and signs are objects too.** A detector like the ones in this
  lecture puts a box around a traffic light or a stop sign. Reading red or
  green inside that box is one more step.

**This lecture: objects.** L5 covers the drivable area, the lanes and
**occupancy** (which parts of the ground are taken), seen from above.


.. _l4-lec-photo:

One Image for the Whole Lecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L4/bus.jpg
   :alt: A street scene: a blue and white electric city bus parked at the curb in front of a yellow building with balconies. A man in a light-colored fleece jacket and a man in a black coat walk toward the camera in front of the bus. A third person is cut off at the left edge and a fourth, walking, at the right edge.
   :width: 45%
   :align: center

   ``bus.jpg``, the sample image that ships with the
   `Ultralytics <https://docs.ultralytics.com/>`__ library: a city bus at the
   curb and people walking past it, 810 pixels wide and 1080 high.

The whole lecture uses this one image. It is the sample image that comes with
the Ultralytics library, the library both of our models come from.

- **Sizes are always width** :math:`\times` **height.** The image is
  :math:`810 \times 1080` pixels.
- **Every box, count and time in this lecture was measured**, on this image
  unless a section says otherwise, on a laptop GPU (RTX 4060). A few sections
  near the end use a CARLA frame. To run both models on your own CARLA
  frames, use ``lecture4/compare_detectors.py`` in the course Python
  repository.
- **Our two models.** **YOLOv8s**: YOLO stands for "you only look once"
  (Redmon et al., 2016), version 8, size s (small). **RT-DETR-L**: Real-Time
  DEtection TRansformer (Zhao et al., 2024), size L (large). Each one gets its
  own section.
- **Network.** Each model is a **network**, short for *neural network*: a
  function with adjustable numbers, its **weights**, set by training on
  examples. Image in, features or boxes out. YOLOv8s has 11.2 million
  weights and RT-DETR-L has 33.0 million, counted with PyTorch.

.. tip::

   The appendix builds a network from a single neuron up:
   :doc:`l4_appendix` ("One neuron").


.. _l4-lec-object-detection:

Object Detection
----------------

.. admonition:: Definition: object detection
   :class: note

   Given an image and a fixed set of :math:`C` classes, output a **set** of
   detections :math:`\{(c_i, s_i, b_i)\}_{i=1}^{N}`, one per object found,
   where :math:`c_i \in \{1, \dots, C\}` is the **class**,
   :math:`s_i \in [0, 1]` the **confidence**, and
   :math:`b_i = (x_0, y_0, x_1, y_1)` the **box**: its top-left and
   bottom-right corners, in pixels. :math:`N` changes from image to image.

Read it piece by piece. The input is an image and a fixed list of :math:`C`
classes: cars, people, cyclists, traffic lights. Each detection is three
things: :math:`c`, the class; :math:`s`, the confidence, a score between zero
and one for that class; and :math:`b`, the box.

Two details matter.

- **It is a set:** the order of the detections means nothing.
- :math:`N` **changes** from one image to the next. Our image has five
  objects; an empty road has none.

:math:`C` **comes from the training data**: a detector finds only the classes
its dataset labels. Our detectors' weights, ``yolov8s.pt`` and
``rtdetr-l.pt``, were trained on COCO, so for them :math:`C = 80`.

.. list-table::
   :widths: 55 15 30
   :header-rows: 1
   :class: compact-table

   * - **Dataset**
     - :math:`C`
     - **Kind**
   * - PASCAL VOC 2012
     - 20
     - everyday images
   * - COCO (2014 release)
     - 80
     - everyday images
   * - Open Images V7
     - 600
     - everyday images
   * - KITTI 2D benchmark
     - 3
     - driving
   * - Waymo Open (LiDAR)
     - 4
     - driving
   * - nuScenes detection
     - 10
     - driving

Driving datasets have far fewer classes, only what matters on the road. KITTI
scores 3: car, pedestrian and cyclist. Waymo's LiDAR set has 4: vehicle,
pedestrian, cyclist and sign. nuScenes has 10.

Detection has two halves, classification and localization. The next two
subsections take them one at a time.


.. _l4-lec-classification:

Classification
~~~~~~~~~~~~~~

.. figure:: /_static/images/L4/task_classification.png
   :alt: Our image with one label in a dark box at the top: label, police van. No boxes on the bus or on the people.
   :width: 45%
   :align: center

   Classification gives one label for the whole image: "police van". There is
   no box, and nothing about the people.

.. admonition:: Definition: classification
   :class: note

   Given an image :math:`x` and a fixed set of :math:`K` classes, output one
   score per class, :math:`p_1, \dots, p_K`, with :math:`p_k \ge 0` and
   :math:`\sum_k p_k = 1`. The **label** is the class with the highest score:
   :math:`\hat{y} = \arg\max_k p_k`.

Read :math:`\arg\max_k p_k` as "the :math:`k` whose :math:`p` is largest".
:math:`\max_k p_k` is the top score itself, 0.616. :math:`\arg\max_k p_k` is
**which** class has it: police van. The hat on :math:`\hat{y}` marks a
prediction.

The model here is **YOLOv8s-cls**, a separate model from the YOLOv8s
detector. It has its own weights, trained on **ImageNet**'s 1000 classes,
while the detector was trained on COCO's 80. Measured on our image:

- The label is "police van", score **0.616**.
- The runners-up are minibus, 0.374, and ambulance, 0.004. They are scores,
  not labels.
- The top three add up to 0.994, so the other 997 classes share
  :math:`1 - 0.994 = 0.006`, none of them exactly zero.

All 1000 numbers are scores. The one that belongs to the label gets its own
name, the **confidence**: here 0.616.

.. warning::

   **The confidence is not the chance of being right.** It is the share of
   the total that sits on "police van". And the answer is wrong: it is a city
   bus. The model could not say "bus": ImageNet has **no plain bus class**,
   only minibus, school bus and trolleybus.

Classification also says nothing about the four people, or about where
anything is. An AV has to know that a person is there, and where.


.. _l4-lec-localization:

Localization
~~~~~~~~~~~~

.. figure:: /_static/images/L4/task_localization.png
   :alt: Our image with one blue box around the bus and no class label. Yellow dots mark its corners: top-left (x0, y0) = (15.0, 228.5) and bottom-right (x1, y1) = (808.2, 748.1). White arrows at the top-left corner of the image show the axes: x to the right, y down.
   :width: 45%
   :align: center

   Localization gives one box and no class. Here it is YOLOv8s's box around
   the bus, shown on its own: from :math:`(15.0,\ 228.5)` to
   :math:`(808.2,\ 748.1)`. Pixel coordinates start at the top-left corner:
   :math:`x` runs right and :math:`y` runs down.

.. admonition:: Definition: localization
   :class: note

   Given an image :math:`W` pixels wide and :math:`H` high, and one object of
   interest, output **where** it is: one box
   :math:`b = (x_0, y_0, x_1, y_1)`, its top-left and bottom-right corners,
   with :math:`0 \le x_0 < x_1 \le W` and :math:`0 \le y_0 < y_1 \le H`. No
   class.

The conditions say the corners lie inside the image, with the left edge
before the right and the top above the bottom.

Classification told us what, not where. Localization tells us where, not
what. But our image holds **five** objects, and localization reports one. The
people are the ones an AV must not miss, so one box is not enough.

.. admonition:: Detection = classification + localization, for every object
   :class: tip

   A detector gives every object a class, its **confidence** (like the 0.616
   of the classification example) and a box: five times on our image. How a
   detector computes the confidence comes at the start of
   :ref:`l4-lec-grading`. Class and box are the two halves we grade, and the
   two halves every detector in this lecture predicts.


.. _l4-lec-ingredients:

The Seven Ingredients of a Detector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A detector needs seven ingredients, in two groups: those used once, offline,
to train the network, and those used on the AV, on every camera frame.

.. figure:: /_static/images/L4/ingredients.png
   :alt: Two gray lanes. Top lane, Training, once, offline: 1 Labeled images, every object boxed and named; 2 Network, backbone, neck and head; 3 Assignment rule, which prediction answers for which object; 4 Loss, how wrong the classes and boxes are. An arrow from Loss back to Network reads adjust the weights, repeat. A dashed arrow labeled trained weights goes down to the bottom lane, Inference, every frame, on the AV: camera image, then 2 Network with its trained weights, then 5 Clean-up, NMS or none, then detections: class, confidence and box. A bracket under this path reads 7 Time budget: 1 / 20 Hz = 50 ms per frame, for this whole path. Below the lanes, a dashed arrow from the detections leads to 6 Grade: IoU, precision, recall, mAP, against labeled images the network never trained on.
   :width: 90%
   :align: center

   The seven ingredients. **Top lane, training** (once, offline): labeled
   images (1) go through the network (2); the assignment rule (3) pairs
   predictions with objects; the loss (4) says how wrong they are, and the
   weights are adjusted and the loop repeats. **Bottom lane, inference**
   (every frame, on the AV): the camera image goes through the trained
   network (2) and the clean-up (5) to give detections. The time budget (7)
   covers that whole path. The grade (6) uses labeled images the network
   never trained on.

**Training, the top lane.**

- **1. Labeled images:** images where a person or a simulator has boxed and
  named every object. COCO's training set has 118,287.
- **2. Network:** backbone, neck and head, built in
  :ref:`l4-lec-features`.
- **3. Assignment rule.** A network makes far more predictions than there
  are objects: YOLOv8s makes one per grid cell, 6300 on our image, for 5
  objects. Training must pair each labeled object with the predictions that
  should have found it. YOLOv8s keeps the 10 cells that best combine class
  score and overlap. DETR makes a fixed number of guesses, called
  **queries**, and pairs each object with exactly one of them. Every
  prediction left over is trained to say: nothing here.
- **4. Loss:** one number for how wrong the paired classes and boxes are.
  Training adjusts the weights to make it smaller, and repeats. The appendix
  shows how (:doc:`l4_appendix`, "Learning the weights").

**Inference, the bottom lane:** running the trained network on new camera
images.

- **5. Clean-up** removes duplicate boxes: **NMS**, short for non-maximum
  suppression, for YOLO; nothing for DETR, whose pairing is one to one.
- **7. Time budget.** A camera at 20 frames a second gives each frame
  :math:`1/20` of a second, 50 ms, for this whole path, and the detector
  shares it with the rest of the AV.
- **6. Grade:** IoU to mAP, on images the network never trained on.


.. _l4-lec-how-models-learn:

How These Models Learn
~~~~~~~~~~~~~~~~~~~~~~

All of the models in this lecture are **deep learning**: a neural network with
many layers, whose weights are set by training. They differ in **what they
learn from**.

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - **Learns from**
     - **How**
     - **In these lectures**
   * - **Supervised:** labeled examples
     - boxes and classes drawn by people or written by a simulator
     - YOLO, RT-DETR; PointPillars, CenterPoint (L5)
   * - **Self-supervised:** images, no labels
     - a task made from the images themselves
     - DINOv2, DINOv3 backbones
   * - **Images with text**
     - images paired with captions
     - CLIP; Grounding DINO
   * - **Reinforcement:** rewards from acting
     - try, get a reward, adjust
     - **not used for detection**; driving policies, L11

- **Supervised learning** uses labeled examples. Someone drew a box around
  every car and person and named it, or a simulator like CARLA wrote the
  boxes out. YOLO, RT-DETR and the LiDAR detectors all learn this way, and so
  does fine-tuning on your own data.
- **Self-supervised learning** uses images with no labels at all: the model
  makes its own task from the images, for example matching two cropped views
  of the same image. DINOv2 and DINOv3 are trained this way; DINOv2's own
  title says "without supervision".
- **Images with text:** CLIP used 400 million image and text pairs from the
  internet, and Grounding DINO learns from boxes tied to phrases.
- **Reinforcement learning** learns by acting: try something, get a reward,
  adjust. It is not used to train detectors, because a detector does not
  act. It is used for driving policies, and Lecture 11 fine-tunes a learned
  planner with rewards for safety, comfort and progress.


.. _l4-lec-timeline:

Detection from 2016 to 2026
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detection moves fast. Every number below is from the model's paper or its
website. **mAP** is the grade defined in :ref:`l4-lec-grading`; a **T4** is a
data-center GPU from NVIDIA.

.. list-table::
   :widths: 10 20 70
   :header-rows: 1
   :class: compact-table

   * - **Year**
     - **Model**
     - **What it changed**
   * - 2016
     - YOLO
     - one pass over a grid: real-time detection (Redmon et al.)
   * - 2020
     - DETR
     - detection as a set: one box per object, no NMS (Carion et al.)
   * - 2023
     - YOLOv8
     - no preset box shapes; the small model scores 44.9 mAP (Ultralytics)
   * - 2024
     - RT-DETR
     - a real-time DETR: 53.0 mAP at 114 FPS (frames per second) on a T4
       (Zhao et al.)
   * - 2025
     - DINOv3, SAM 3
     - backbones trained without labels; segmentation from a typed phrase
       (Siméoni et al.; Carion et al.)
   * - 2026
     - YOLO26
     - YOLO without NMS: 48.6 mAP (small), 2.5 ms on a T4 (Ultralytics)
   * - 2026
     - RF-DETR
     - a DINOv2 backbone: 60.1 mAP at 17.2 ms on a T4 (Robinson et al.)

YOLOv8 is our first model, and RT-DETR is our second. DINOv3 is a backbone
trained without labels, and SAM 3 segments whatever a short phrase names.

.. admonition:: Two trends
   :class: tip

   - **The two families meet.** YOLO26 drops NMS, which was DETR's idea.
   - **Big pretrained backbones move into fast detectors.** RF-DETR puts a
     DINOv2 backbone into a real-time DETR.


.. _l4-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

By the end of this lecture, you will be able to:

- Say what a detector outputs, clean it up with **NMS**, and grade it with
  **IoU**, **precision**, **recall** and **AP**, all by hand.
- Explain how a **one-stage** detector predicts boxes from a grid.
- Compute **attention** for a few tokens.
- Explain how **DETR** matches queries to objects, and why it needs no NMS.


.. _l4-lec-roadmap:

How the Lecture Fits Together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/L4/lecture_roadmap.png
   :alt: The lecture's sections as boxes joined by arrows. Features branches into One-stage on top and Transformers below, which join at On the road. Grading sits between the two branches, with dashed arrows up to One-stage and down to Transformers. After On the road, two dashed gray boxes, 3D and Segmentation, are marked next lecture.
   :width: 75%
   :align: center

   The lecture as one chart. **Features** branches into **One-stage** and
   **Transformers**, which join at **On the road**. **Grading** sits between
   the branches with dashed arrows to both: it measures them, it is not a
   step they are built from. The dashed gray boxes, **3D** and
   **Segmentation**, are next lecture.

- **From Pixels to Features.** A camera gives the AV only numbers. A network
  turns them into **features**, numbers that say how strongly a pattern is
  there.
- **Grading a Detector.** IoU, precision, recall and mAP, to compare our two
  models with one number.
- **One-Stage Detectors** (YOLO). Every grid cell predicts a box, then a
  clean-up step keeps one box per object.
- **Transformers** (RT-DETR). Each **token**, a small piece of the image, is
  updated with information from all the others. The encoder reads the image;
  the decoder gives one box per object, with no clean-up.
- **Detection on the Road.** What decides how a detector does on an AV: the
  confidence cut, the training data, the time per frame, the weather.
- **Next lecture:** distances in meters, from **3D detection**, and the shape
  of things that are not boxes, like the road, from **segmentation**.


.. _l4-lec-features:

From Pixels to Features
-----------------------

- **Where we are:** perception has to turn camera images into objects.
- **In this section:** how a network turns the numbers of an image into
  **features**.
- **What it is for:** every detector in this lecture, YOLO and DETR alike,
  starts from features. Pixels in, features out. The two detectors differ
  only in what they do with the features.

We start from what the camera hands over: numbers. With plain arithmetic, by
hand, we find the edges in our image. Then we name what we built, **feature**
and **feature map**, and see how a network's layers do the same with learned
weights, and how a detector is built from a backbone, a neck and a head.


.. _l4-lec-numbers:

What the Computer Receives from the Camera: Numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A camera does not hand the computer a picture of a bus. It hands over
numbers, and nothing else.

.. figure:: /_static/images/L4/pixels_zoom.png
   :alt: Five panels. Our image with a small yellow square on the white lettering emisiones on the side of the bus. That square's 12 by 12 pixels, enlarged into visible blue and white squares, with the central 4 by 4 outlined in yellow. Then three 4 by 4 tables for red, green and blue, 0 to 255, each cell shaded from black at 0 to the full color at 255. The first three columns are dark blue pixels, such as red 20, green 83, blue 152; the last column is white-blue, such as red 177, green 200, blue 250.
   :width: 100%
   :align: center

   From the image to its numbers. The **yellow square** sits on the white
   lettering on the side of the bus. Zoomed to :math:`12 \times 12` pixels,
   each square is one pixel, one flat color. The three tables are the red,
   green and blue values of the central :math:`4 \times 4`, drawn black at 0
   and full color at 255, so a brighter cell means a larger number.

- **Each pixel is three numbers** from 0 (none) to 255 (full): how much red,
  green and blue.
- **In the central** :math:`4 \times 4`, the first three columns are the dark
  blue of the bus: little red, some green, more blue, like 20, 83, 152. The
  last column is the white of the letter: all three high, like 177, 200, 250.
- **Our image:** :math:`810 \times 1080 \times 3 = 2{,}624{,}400` numbers.
  Nowhere in that list is there a bus or a person, only numbers. The rest of
  this lecture turns these numbers into "bus".


.. _l4-lec-edges-feature:

Edges: One Kind of Feature among Many
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: feature
   :class: note

   One number computed for **one place** in the image: how strongly one
   pattern is present there.

Edges come first, because they are the simplest pattern there is: two
neighboring pixels differ. Every object's outline is an edge, where it meets
the background, and so is every lane marking on the road. The table shows
edges and a few other features.

.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * - **Feature**
     - **What it finds**
     - **Where an AV uses it**
   * - **Edges**
     - where brightness changes: outlines, lane markings
     - this section; the first layer of a CNN
   * - **Color**
     - regions of one color: the blue bus
     - a CNN's first layer too (see :ref:`l4-lec-channel`)
   * - **Gradient histograms** (HOG)
     - the outline shape of a region
     - pedestrian detection before CNNs (Dalal and Triggs, 2005)
   * - **Keypoints** (corners)
     - points found again in the next frame
     - visual SLAM: where the AV is (ORB-SLAM, Mur-Artal et al., 2015)
   * - **Learned features**
     - whatever training finds useful
     - every detector in this lecture

**HOG** describes the shape of an outline in a region. Before CNNs, it was how
computers found pedestrians. **Keypoints** are corners a computer can find
again in the next frame. Visual SLAM uses them to work out where the AV is,
which is a localization topic, not detection.

For many years people designed these features by hand. Today a network
learns its own, and they include edges and color. So the plan: edges by hand,
with a filter we choose, then a network that learns many features at once,
edges among them.


.. _l4-lec-five-steps:

Finding Edges with Arithmetic: Five Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** find the **edges** inside the image, using only arithmetic on its
numbers. An edge is a line where one region meets another and the brightness
changes sharply: a white letter on the blue bus, a light-colored jacket
against the street. It is not the border of the picture.

.. figure:: /_static/images/L4/five_steps.png
   :alt: A flowchart of five steps. Inside a dashed frame labeled a test, by hand: we pick two windows: 1 Pick two 3 by 3 windows by eye, one edge, one flat; 2 Multiply each window by a filter we choose; 3 Add the products: one number, the response; 4 Compare the edge's response with the flat one's. An arrow leads to a green frame labeled every window: nobody picks, holding 5 Slide the filter over the whole image: a response everywhere.
   :width: 100%
   :align: center

   The five steps. Steps 1 to 4, inside the dashed frame, are a test we run
   by hand on two windows we pick. Step 5, in green, runs the same filter at
   every window, with nobody picking.

1. **Pick** two small windows, one on an edge and one on a flat area. We pick
   them by eye, not the computer: they are a test.
2. **Multiply** each window by a **filter**, a small grid of weights we
   choose.
3. **Add** the products into one number, the **response**.
4. **Compare** the two responses.
5. **Slide** the filter over the whole image.

.. tip::

   **Why by hand:** a network's first layer does Steps 2, 3 and 5, multiply,
   add and slide, at every window, with weights it learned. It never picks
   windows and never compares one with another: Steps 1 and 4 are only our
   test.


Step 1: Pick Two Windows, One on an Edge, One Flat
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We pick two small windows, :math:`3 \times 3` pixels each, by looking at the
image. If our filter gives a large number at the first and a small one at the
second, it works, and in Step 5 it runs everywhere.

.. figure:: /_static/images/L4/edge_windows.png
   :alt: Three panels. Our image, with a yellow square on the lettering emisiones on the side of the bus and a green square on the flat white roof panel at the front of the bus. Then the 3 by 3 gray levels at each square, drawn in gray with their values. At the letter's edge, outlined in yellow, row by row: 65.3, 47.0, 212.7; 114.0, 40.7, 237.0; 92.0, 59.7, 236.3, so the right column is bright and the other two dark. On the flat roof, outlined in green, row by row: 195.7, 197.7, 197.7; 197.7, 193.7, 189.7; 189.7, 188.7, 186.7, all close to each other.
   :width: 90%
   :align: center

   The two windows. **Yellow**, at the letter's edge: two dark columns on the
   left, one bright column on the right. **Green**, on the flat white roof at
   the front of the bus: all nine numbers are close, 186.7 to 197.7.

Each number is one pixel's **gray level**: the mean of its red, green and
blue, from 0 (black) to 255 (white). Example, the middle row on the left: the
pixel has red 73, green 111 and blue 158, so its gray level is

.. math::

   (73 + 111 + 158) / 3 = 114.0

Those three numbers are in the tables above: the yellow window is the
bottom-right :math:`3 \times 3` of the :math:`4 \times 4` pixels.

**Why gray?** An edge is a change in brightness, and brightness needs one
number per pixel, not three. A :math:`3 \times 3` window is then 9 numbers to
multiply, not :math:`3 \times 3 \times 3 = 27`, and the edge, dark blue next
to white, shows up just as clearly. A real network keeps all 3 colors: two
colors of the same brightness, like a red sign on a green tree, look alike in
gray, and their edge would vanish.


Step 2: Multiply the Window by a Filter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: filter
   :class: note

   A small grid of weights, not a Kalman filter. Its goal: turn a window of
   pixels into one number that says how strongly one pattern, here an edge,
   is there. Lay it on the window and multiply each pixel by the weight on
   top of it.

Careful with the word: this is not the Kalman filter of Lecture 3. In image
processing, a filter is a small grid of weights.

**Why** :math:`3 \times 3`? It is the smallest grid with a center pixel and a
neighbor on every side. The VGG paper, which made :math:`3 \times 3` the
standard, calls it "the smallest size to capture the notion of left/right,
up/down, center". Our window is :math:`3 \times 3` because the filter is.

.. figure:: /_static/images/L4/filter_steps.png
   :alt: Four panels. The 12 by 12 gray pixels at the letter's edge, with the 3 by 3 window outlined in yellow and enlarged next to it as its gray levels: left column 65.3, 114.0, 92.0; middle column 47.0, 40.7, 59.7; right column 212.7, 237.0, 236.3. A times sign, then the filter's weights: minus 1 in the left column in blue, 0 in the middle in white, plus 1 in the right column in red. An equals sign, then the products cell by cell: minus 65.3, minus 114.0, minus 92.0 in blue; three zeros; 212.7, 237.0, 236.3 in red.
   :width: 100%
   :align: center

   Multiplying the yellow window by the filter. Left to right: the window on
   the zoomed pixels, its nine gray levels, the filter (-1 in the left
   column in **blue**, 0 in the middle, +1 in the right column in **red**),
   and the nine products, cell by cell.

**Where the weights come from:** we chose them. Minus one on the left and
plus one on the right make the sum equal to the right column minus the left
column, and that difference is what an edge looks like in numbers. This is a
classic hand-made edge filter. A network's weights are **set by training**
instead; :ref:`l4-lec-layer` and :ref:`l4-lec-channel` show what YOLOv8s's
trained filters find.

Multiply cell by cell and you get the last grid: the left column turns
negative, the middle column turns into zeros, the right column stays as it
is. **Blue** cells pull the response down; **red** cells push it up.


The Response: One Number per Window
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: response
   :class: note

   The sum of the products of a filter's weights and the pixels under them:
   one number for one window. For a :math:`3 \times 3` filter :math:`w` on a
   window :math:`x`:

   .. math::

      r = \sum_{i=1}^{3} \sum_{j=1}^{3} w_{ij}\, x_{ij}
      \qquad \text{(9 products, added)}

   :math:`i` counts the rows and :math:`j` the columns.

For our filter (-1 left, 0 middle, +1 right), the response is the **right
column minus the left column**.

**Its range.** A pixel is 0 to 255, so a column of 3 pixels adds to 0 to
:math:`3 \times 255 = 765`. The largest response is an all-white right column
next to an all-black left one: :math:`765 - 0 = +765`. Swap them and you get
:math:`0 - 765 = -765`.


Step 3: Add the Products, the Response at the Edge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L4/letter_edge.png
   :alt: A pixel-level close-up of the letters e, m and i of emisiones, white on the blue side of the bus. A small yellow square, labeled 3 x 3 window with an arrow, sits at the top of the first stroke of the m: the dark blue gap between the e and the m on its left, the m's white stroke on its right.
   :width: 60%
   :align: center

   Where the window is: on the "m" of "emisiones", at the top of its first
   stroke. The left two columns are the dark blue gap between the "e" and
   the "m"; the right column is the m's white stroke.

Add the nine products from Step 2:

.. math::

   \begin{bmatrix} -65.3 & 0 & 212.7 \\ -114.0 & 0 & 237.0 \\ -92.0 & 0 & 236.3 \end{bmatrix}

1. Right column: :math:`212.7 + 237.0 + 236.3 = 686.0`.
2. Left column: :math:`65.3 + 114.0 + 92.0 = 271.3`, subtracted (weights
   -1).
3. Middle column: 0.
4. Response: :math:`686.0 - 271.3 = \mathbf{414.7}`.

**In words:** this filter measures how much brighter the right column is than
the left column. At the edge of the letter the right column is much brighter,
so the response is large.


Step 4: Compare the Edge with the Flat Roof
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A single number, 414.7, means little until we compare it with a place that
has no edge. So we run the same filter on the flat roof (green window).

.. figure:: /_static/images/L4/filter_steps_flat.png
   :alt: Four panels. The 12 by 12 gray pixels on the flat white roof, with the 3 by 3 window outlined in green and enlarged next to it as its gray levels: left column 195.7, 197.7, 189.7; middle column 197.7, 193.7, 188.7; right column 197.7, 189.7, 186.7. A times sign, then the same filter: minus 1 in the left column in blue, 0 in the middle, plus 1 in the right column in red. An equals sign, then the products: minus 195.7, minus 197.7, minus 189.7 in blue; three zeros; 197.7, 189.7, 186.7 in red.
   :width: 100%
   :align: center

   The same filter on the green window. All nine gray levels are close, so
   the blue and red products nearly cancel.

1. Right column: :math:`197.7 + 189.7 + 186.7 = 574.1`.
2. Left column: :math:`195.7 + 197.7 + 189.7 = 583.1`.
3. Response: :math:`574.1 - 583.1 = \mathbf{-9.0}`. The right column is 9.0
   darker.

**414.7 at the letter's edge, -9.0 on the flat roof.** The response is large
at the edge and close to zero on the flat roof. That is what makes the filter
an edge detector.


Reading the Response: Sign and Size
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The sign of the response matters too. Here are three windows from our image,
each placed at its measured response, on one line from -765 to +765.

.. figure:: /_static/images/L4/response_scale.png
   :alt: A number line from -765 through 0 to +765, blue on the negative side and red on the positive side, with a gray shaded band for the range measured on our image, -743.3 to 728.3. Three 3 by 3 gray windows sit above the line at their responses: -317.7 in blue, left brighter, edge the other way; -9.0, alike, no edge; 414.7 in red, right brighter, edge.
   :width: 90%
   :align: center

   Three responses on one line. **414.7** (red): our window on the "m",
   right side much brighter, an edge. **-9.0**: the flat roof, both sides
   alike, no edge. **-317.7** (blue): three pixels further along the same
   "m", where the white stroke is on the left and the dark blue on the
   right, an edge facing the other way. The shaded band is the range of
   responses measured on our image, -743.3 to 728.3, close to the limits.

**Large either way: an edge, and the sign gives its direction. Near 0: no
edge.**


Step 5: Slide the Filter over the Whole Image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We have the response at two windows. Now we compute it at every window: put
the filter at the top-left corner, compute, move one pixel to the right,
compute again, and so on, row after row.

- **Every pixel or every window?** Both. Each window is centered on one
  pixel, and the next window is one pixel over, so the windows overlap. That
  gives one response per pixel.
- **Except the border.** The outermost ring of pixels gets none, because a
  window centered there would stick out of the image. So
  :math:`810 \times 1080` pixels give :math:`808 \times 1078` responses.
- Sliding a filter over an image like this has a name: a **convolution**.

.. figure:: /_static/images/L4/edge_filter.png
   :alt: Two panels. Left, our image. Right, the size of the same filter's response at every pixel, drawn dark where the response is large: the outlines of the bus, the letters, the windows, the balconies and the people appear as dark lines on white. The long top edge of the bus roof is faint.
   :width: 85%
   :align: center

   The size of the response at every pixel, drawn **dark where it is
   large**, plus or minus. The outlines of the bus, the letters and the
   people appear. The flat roof, where we got -9.0, stays white.

.. admonition:: Only left-to-right changes
   :class: tip

   Look at the long top edge of the bus roof: it is faint. That edge runs
   left to right, so the brightness changes from top to bottom, not from left
   to right. Every column of the window then holds the same numbers, and
   right minus left is 0. This filter finds only one direction of edge. A
   filter with -1 on top and +1 on the bottom would find the other.

One filter of nine weights already draws the outlines of the bus, the
letters and the people. Next we name what we built: each response is a
feature, and the whole grid is a feature map.


.. _l4-lec-our-feature:

Our Response Is a Feature, and So Is YOLOv8s's
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Back to the word from the start of the section: a feature is one number for
one place, saying how strongly one pattern is there. Each response we
computed is one.

.. admonition:: Our feature
   :class: tip

   The pattern is the **vertical edge**, the place is the letter's edge, and
   the number is our response, **414.7**. Every response of Step 5 is a
   feature for the same pattern, at its own place.

A network computes the same kind of number.

.. figure:: /_static/images/L4/term_feature.png
   :alt: Left, one of YOLOv8s's maps on our image, dark purple with bright thin vertical lines, with a small yellow square on the bus lettering. An arrow leads right to the 5 by 5 numbers inside that square, from -0.3 to 20.0, colored from black for small to orange for large, with the center number, 16.7, outlined in yellow.
   :width: 90%
   :align: center

   The same kind of number from YOLOv8s, on the lettering of the bus. Left:
   one of its maps on our image. Right: the :math:`5 \times 5` numbers inside
   the yellow square. The center, **16.7**, is a strong vertical edge right
   there; numbers near 0 mean no such edge.

**Why 16.7 and not hundreds?** The network first divides every pixel by 255,
so its inputs run from 0 to 1, and its weights are its own, set by training.


.. _l4-lec-many-features:

One Place, Many Features
~~~~~~~~~~~~~~~~~~~~~~~~

414.7 is not "the" feature of that window. It is one feature, for one
pattern, the vertical edge. Change the computation and the same window gives
another. The same two windows give other features, one number per pattern,
each from its own computation:

.. list-table::
   :widths: 22 38 20 20
   :header-rows: 1
   :class: compact-table

   * - **Pattern**
     - **Computed as**
     - **Letter's edge** (yellow)
     - **Flat roof** (green)
   * - vertical edge
     - right column minus left column
     - **414.7**
     - -9.0
   * - horizontal edge
     - bottom row minus top row
     - 63.0
     - -26.0
   * - brightness
     - mean gray level of the 9 pixels
     - 122.7
     - 193.0
   * - blueness
     - mean of blue minus red, 9 pixels
     - 64.3
     - -17.0

- **Horizontal edge:** 63.0 at the letter, small next to 765, so little
  change from top to bottom.
- **Brightness:** 122.7 at the letter, darker than the white roof at 193.0.
- **Blueness:** 64.3 on the blue bus, -17.0 on the roof, which is slightly
  warm.

.. admonition:: A feature names a pattern and a place
   :class: tip

   We chose these four. YOLOv8s's first layer computes 32 at every place,
   with patterns set by training. Some of them are in :ref:`l4-lec-channel`.


.. _l4-lec-feature-map:

Feature Map: One Grid of Features, for One Pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: feature map
   :class: note

   The features for one pattern at **every place**: a grid of numbers. Drawn
   as an image, bright means a large number.

.. figure:: /_static/images/L4/term_map.png
   :alt: One feature map from YOLOv8s's first layer on our image, outlined in orange: mostly dark purple, with bright thin vertical lines along the side of the bus, the people's legs and coats, the building's windows and the strokes of the letters.
   :width: 45%
   :align: center

   One map from YOLOv8s's first layer, on our image. Its pattern is the
   vertical edge, like ours, and you can read the image in it: the side of
   the bus, the people's legs, the strokes of the letters.

- **Ours:** Step 5's edge map is a feature map, one feature per pixel,
  because our filter moved 1 pixel per step. It was drawn the other way,
  dark for large, but it is the same kind of grid.
- **YOLOv8s's**, in the figure, is smaller: :math:`240 \times 320` features.
  Its filter moves 2 pixels per step. The step size is called the
  **stride**, so this layer has a stride of 2.


.. _l4-lec-map-size:

YOLOv8s's Map: from 810 x 1080 Pixels to 240 x 320
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Why scale first?** YOLOv8s was trained on images 640 pixels on a side
(Ultralytics' default size), so it runs at that size. Scaling also cuts the
work: :math:`480 \times 640 = 307{,}200` pixels instead of
:math:`810 \times 1080 = 874{,}800`. That is
:math:`874{,}800 / 307{,}200 \approx 2.8`, so almost three times less work.

1. **Scale factor.** The long side, 1080, becomes 640:
   :math:`640 / 1080 = 0.593`.
2. **Short side,** by the same factor, so the shape is kept and the people are
   not squeezed: :math:`810 \times 0.593 = 480`. The input is
   :math:`480 \times 640`.
3. **No padding.** The network's coarsest grid, stride 32 (see
   :ref:`l4-lec-cnn`), needs sides that are multiples of 32.
   :math:`480 = 15 \times 32` and :math:`640 = 20 \times 32` already are, so
   the library adds no padding.
4. **Stride 2.** The first layer's filter moves 2 pixels per step:
   :math:`480 / 2 = 240` places across, :math:`640 / 2 = 320` down. The map is
   :math:`240 \times 320 = 76{,}800` features, one per :math:`2 \times 2`
   block of pixels.

.. admonition:: Why exactly half
   :class: tip

   The layer adds a 1-pixel border of zeros around its input, so a
   :math:`3 \times 3` window fits on the edge pixels too. Our Step 5 added
   none and lost the border: :math:`808 \times 1078`.


.. _l4-lec-layer:

Layer: One Step of the Network's Computation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A network does what we did in Step 5, many times at once.

.. figure:: /_static/images/L4/term_layer.png
   :alt: Our image, labeled image in, an arrow into a green box labeled layer 1, and an arrow out to a stack of 32 dark feature maps, the front one outlined in orange, labeled 32 maps out.
   :width: 90%
   :align: center

   YOLOv8s's first layer: the image goes in, 32 feature maps come out. The
   front map, outlined in orange, is the vertical-edge map from the last
   subsection.

.. admonition:: Definition: layer
   :class: note

   One step of a network's computation: a set of filters, each slid over the
   layer's input, each giving one feature map. Layers run one after another;
   each works on the maps the layer before it produced.

**YOLOv8s's first layer, measured:** 32 filters, each :math:`3 \times 3`
pixels :math:`\times` 3 colors :math:`= 27` weights. The image goes in, 32
maps come out. Nobody chose the weights: training set them.

- **The size is set by the designers, the weights by training.** YOLOv8s's
  architecture file, ``yolov8.yaml``, writes 3 for the filter size and 2 for
  the stride on every ``Conv`` line. Training never changes the size.
- **Most networks stack small** :math:`3 \times 3` **filters.** Three in a row
  see a :math:`7 \times 7` area with :math:`3 \times 9 = 27` weights, where
  one :math:`7 \times 7` filter needs :math:`7 \times 7 = 49`, per pair of
  input and output channels.
- **Two more steps follow each filter** inside the layer: it adds a learned
  offset, and it squeezes negative results close to zero. That is why
  YOLOv8s's :math:`5 \times 5` numbers around 16.7 never go far below zero.
  The appendix covers both (:doc:`l4_appendix`, "Activation").


.. _l4-lec-channel:

Channel: One Feature Map per Pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A layer looks for many patterns at once, and each pattern gets its own map.

.. admonition:: Definition: channel
   :class: note

   One feature map in a layer's output. A layer outputs **many channels**,
   one per filter: YOLOv8s's first layer outputs 32.

.. figure:: /_static/images/L4/term_channels.png
   :alt: Eight of the 32 maps from YOLOv8s's first layer on our image, labeled channel 0, 1, 2, 5, 9, 12, 17 and 26. Channels 1 and 9 are bright on the blue side of the bus; channel 5 is bright on the light, warm areas such as the building and the man's jacket; channel 2, outlined in orange, shows thin vertical edges; channel 26 shows horizontal edges such as the bus roof; channels 0, 12 and 17 show fine texture.
   :width: 90%
   :align: center

   Eight of the 32 channels of YOLOv8s's first layer, on our image.

The 32 filters each look for their own pattern on the same image, and each
writes its own map. Training, not us, decides each pattern, and some match
nothing we would name. They are different patterns:

- **Channels 1 and 9** light up on the blue side of the bus.
- **Channel 5** lights up on the light, warm areas: the building and the
  man's jacket.
- **Channel 2**, outlined in orange, is the map from
  :ref:`l4-lec-feature-map`. It finds vertical edges: its weights, added over
  the three colors, are positive on the left and negative on the right, the
  mirror of our filter.
- **Channel 26** finds horizontal edges.

Deeper layers output more channels, 512 at the end of YOLOv8s's backbone, for
larger patterns.


.. _l4-lec-deeper:

What Deeper Layers Respond To
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first layer finds edges and colors. Each deeper layer works on the maps
of the layer before it, so it can respond to larger patterns. Here is YOLOv8s
at three depths, on our image, measured.

.. figure:: /_static/images/L4/layer_features.png
   :alt: Four panels from YOLOv8s. First, its 32 first-layer filters, each 3 by 3 pixels in color, many showing a light-to-dark step or a single color. Then three feature maps, each one channel drawn bright where it responds strongly. Stride 2, 240 by 320 cells, 32 channels, 1 shown: a faint copy of the image with thin bright outlines. Stride 8, 60 by 80 cells, 128 channels, 1 shown: patchy bright texture over the bus and the building. Stride 32, 15 by 20 cells, 512 channels, 1 shown: a few coarse bright blocks where the people stand, dark elsewhere.
   :width: 100%
   :align: center

   YOLOv8s, measured. **Left:** its 32 first-layer filters, learned, drawn
   as :math:`3 \times 3` color patches; many are edge and color detectors.
   **Then three depths.** Each map shows the one channel most active on the
   man in the light-colored jacket compared with the rest of the image.

- **Stride 2** (:math:`240 \times 320` cells): it still looks like the image,
  with outlines.
- **Stride 8** (:math:`60 \times 80` cells): it responds to texture.
- **Stride 32** (only :math:`15 \times 20` cells, but 512 channels): the
  chosen channel lights up in coarse blocks where the **people** are.

Each panel is one channel out of many, chosen for this figure, not the whole
story. Still, it shows the pattern of every CNN: going deeper, the grid gets
coarser, the channels get more numerous, and each cell responds to larger
things: edges, then textures and parts, then objects.


.. _l4-lec-cnn:

A CNN: Smaller Grids, More Channels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each of those layers does what we did by hand in Step 5, a convolution, with
many learned filters. A network built from layers of convolutions is a
**CNN**, a convolutional neural network.

.. figure:: /_static/images/L4/cnn_stack.png
   :alt: YOLOv8s's backbone drawn as 3D blocks after the image, which lies on a slanted plane: input 480 by 640, 3 colors; stride 2, 240 by 320, 32 channels; stride 4, 120 by 160, 64 channels; then, darker and in bold, stride 8, 60 by 80, 128 channels; stride 16, 30 by 40, 256 channels; stride 32, 15 by 20, 512 channels. Each block is shorter and thicker than the one before. A note says drawn to show the trend, not to scale.
   :width: 90%
   :align: center

   YOLOv8s's backbone, measured. Deeper means a **smaller** grid and **more**
   channels. The blocks show the trend, not the scale; the numbers under
   them are measured. The three darker blocks, strides 8, 16 and 32, are the
   ones a one-stage detector predicts from.

- **The input** is 480 pixels wide by 640 high; the detector shrinks the
  image to that size first. Each layer slides small filters over the layer
  before and writes down how strongly each filter responds at each place.
- **Stride 8** means one cell per :math:`8 \times 8` pixels:
  :math:`480 / 8 = 60` and :math:`640 / 8 = 80`, a grid 60 wide and 80 high.
- **Stride 32** means one cell per :math:`32 \times 32` pixels:
  :math:`480 / 32 = 15` and :math:`640 / 32 = 20`. YOLOv8s keeps 512
  channels there, so 512 numbers per cell.
- **Small grids see big patterns**, like a whole bus; big grids see small
  ones, like a distant person.

Keep the three darker blocks in mind, strides 8, 16 and 32. A one-stage
detector predicts a box from every cell of all three.

.. tip::

   The appendix, CNN Fundamentals, has the details: neurons, the convolution
   arithmetic, stride and padding, activations, pooling, training and
   fine-tuning (:doc:`l4_appendix`, "Convolution").


.. _l4-lec-backbone:

Backbone, Neck and Head
~~~~~~~~~~~~~~~~~~~~~~~

Almost every detector has the same three parts, and the CNN above is the
first of them.

.. figure:: /_static/images/L4/backbone_neck_head_callouts.png
   :alt: Four boxes joined by arrows: image, backbone (features), neck (mix the scales), head (classes, boxes), shaded darker green from left to right. A dotted line drops from each box to a note. Input: the image scaled to 480 by 640 pixels, 3 numbers each. Backbone: a CNN; three feature maps out, strides 8, 16, 32; 128, 256, 512 channels. Neck: mixes the three maps; the coarse one knows bus, the fine one where its edges are. Head: a few convolutions at every cell; 144 numbers, decoded to 84: a box, 80 scores.
   :width: 90%
   :align: center

   The three parts of a detector, with YOLOv8s's numbers, measured.

- **Backbone.** The image, scaled to :math:`480 \times 640`, goes into the
  CNN from the last subsection. It turns the image into three feature maps,
  at strides 8, 16 and 32, with 128, 256 and 512 channels. A backbone is
  often trained first on a huge collection of labeled images, then reused.
- **Neck.** It mixes the map sizes. A small map's cells respond to whole
  objects like the bus; a big map's cells mark where its edges are. The neck
  combines the two.
- **Head.** It turns features into the answer: classes and boxes.

**What a head looks like.** In YOLOv8s it is a few small convolutions run
over each of the three maps, whose cells hold 128, 256 and 512 numbers. At
every cell the output is 144 numbers: 80 class scores, one per COCO class,
and 64 for the box. The box is four distances, one per side, and each
distance comes as 16 bins; the network takes their weighted average, so the
64 become 4, and 144 becomes 84 per cell. Since the head is a convolution,
the same head weights run at every cell, which is how all 6300 cells can
predict: :math:`4800 + 1200 + 300` on the three grids. The appendix decodes
one cell by hand (:doc:`l4_appendix`, "Decoding one cell").

**RT-DETR-L has the same three parts:** a CNN backbone, but its neck adds a
transformer layer and its head is a transformer decoder (see
:ref:`l4-lec-transformers`). That difference is most of this lecture.


.. _l4-lec-pretrained:

Starting from a Pretrained Backbone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Almost nobody trains those parts from zero, and there is a good reason.

.. admonition:: Pretrained and fine-tuned
   :class: tip

   **Pretrained:** trained first on a large, general image collection, then
   **fine-tuned**, trained a little more, on your own data. Example:
   ImageNet's 1000-class set, 1.2 million training images. Edges and simple
   shapes look much the same in CARLA and in real images, so the early layers
   need little change.

The deeper layers do need to adapt. Fine-tuning takes far less data and time
than training from zero, because the network starts with features that
already work. Later, in :ref:`l4-lec-domain-gap` and in the live demo, you see
a COCO model on CARLA frames.

.. admonition:: Foundation backbones
   :class: tip

   **Foundation backbones** go further: they are trained on far more images,
   often without labels or with captions. CLIP, DINOv2, and DINOv3 (Meta,
   2025, the newest of the DINO line) are examples. Their features work for
   many tasks at once, which is why AV teams rarely train a backbone from
   scratch. Later you see a DINOv2 backbone inside one of the newest
   detectors.

**Both our detectors start from weights pretrained on COCO**, a common
detection dataset: 118,287 training images in 80 everyday classes, each
object boxed by a person.


.. _l4-lec-grading:

Grading a Detector
------------------

- **Where we are:** a network turns the image into feature maps.
- **In this section:** how to **grade** a detector: IoU, true and false
  positives, precision, recall, mAP.
- **What it is for:** comparing our two detectors with one number, mAP, as
  papers do. IoU also works inside NMS, YOLO's clean-up step.

Grading is a measuring tool, not a step of the detector. On the chart in
:ref:`l4-lec-roadmap` it sits between the two branches, with dashed arrows to
both. It comes before the detectors because the rest of the lecture compares
two of them, and a comparison needs a grade.

Everything starts from the confidence, so here is where it comes from.

.. admonition:: Definition: confidence
   :class: note

   The number from 0 to 1 that comes with each box: how strongly the
   detector scores the class it names for that box. The head gives a raw
   score per class, any number; a **sigmoid**,

   .. math::

      \frac{1}{1 + e^{-x}},

   maps it into 0 to 1, and the highest class wins. It is **not** the
   probability of being right, and 0.5 in one model is not 0.5 in another.

You will see RT-DETR give higher numbers than YOLO to the same people, so the
confidences of two models cannot be compared.

A real detection, from YOLOv8s on our image: ``person 0.89 (49.9, 401.8) to
(244.5, 901.8)``. That is the man in the light-colored jacket. Grading ranks
every box by its confidence, from the surest down.


.. _l4-lec-iou:

IoU: How Much Two Boxes Overlap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A detector's box is never exactly the true box, so we need one number that
says how well two boxes agree.

.. figure:: /_static/images/L4/iou_example.png
   :alt: A grid in pixels, x to the right and y down, with two boxes. The ground truth, solid black, runs from 2 to 8 across and 2 to 10 down. The detection, dashed orange, runs from 3 to 9 across and 3 to 11 down. Their overlap, shaded green, runs from 3 to 8 across and 3 to 10 down, and is labeled overlap 35.
   :width: 50%
   :align: center

   Two boxes on a pixel grid, :math:`x` to the right and :math:`y` down, as
   in an image. **Black:** the **ground truth**, where the object really is.
   **Orange dashed:** the detection, what the detector said. **Green:** their
   overlap.

.. admonition:: Definition: intersection over union (IoU)
   :class: note

   The overlap of two boxes, divided by the area they cover together.

   .. math::

      \text{IoU} = \frac{\text{overlap}}{\text{area}_1 + \text{area}_2 - \text{overlap}}

Why subtract the overlap in the bottom line? Because adding the two areas
counts the overlap twice. The box corners are chosen for this example:

1. Each box: :math:`6 \times 8 = 48`.
2. Overlap: :math:`5 \times 7 = 35`.
3. Covered by either box, the **union**: :math:`48 + 48 - 35 = 61` (the
   overlap counted once).
4. IoU :math:`= 35 / 61 = \mathbf{0.574}`.

Read it like this: of everything the two boxes cover, **57 percent** is
covered by both. With the usual cut of 0.5, this detection counts as right.
IoU is 1 when the boxes match exactly and 0 when they do not touch.

You meet IoU twice in this lecture: to decide whether a detection is right,
and in the next section inside the clean-up step called NMS. It comes back
again in tracking next week.


.. _l4-lec-tp-fp:

Right or Wrong: True and False Positives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A box can look right and still be wrong, so every detection is compared with
the **ground truth**: the boxes a person drew by hand, or the boxes a
simulator like CARLA writes out.

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Name**
     - **Meaning**
   * - **True positive (TP)**
     - matches a not-yet-matched ground-truth box of its class with IoU at
       least a threshold that the evaluator sets, often 0.5
   * - **False positive (FP)**
     - matches nothing: a box on no object, or a second box on an object
       already matched
   * - **False negative (FN)**
     - a ground-truth object no detection matched

Each ground-truth box can be matched only once, and the detections are
matched from the most confident down. A second box on a person who is
already matched is a false positive, which is why duplicates hurt the score.

From those counts come two scores:

.. math::

   \text{precision} = \frac{TP}{TP + FP}
   \qquad\qquad
   \text{recall} = \frac{TP}{TP + FN}

- **Precision:** of the boxes you drew, the share that is right.
- **Recall:** of the real objects, the share you found.

They pull against each other. Report every box and recall goes up but
precision falls. Report only the surest and precision goes up but recall
falls.


.. _l4-lec-pr-numbers:

Precision and Recall in Numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Chosen for this example (the same detections as in the next subsection):
**3 people** are really there, and the detector gives 5 person boxes, sorted
by confidence. Here are two separate choices of which boxes to accept:

.. list-table::
   :widths: 24 10 10 10 23 23
   :header-rows: 1
   :class: compact-table

   * - **Boxes accepted**
     - **TP**
     - **FP**
     - **FN**
     - **Precision**
     - **Recall**
   * - all 5
     - 3
     - 2
     - 0
     - :math:`3/(3+2) = 0.60`
     - :math:`3/(3+0) = 1.00`
   * - only the top 2
     - 2
     - 0
     - 1
     - :math:`2/(2+0) = 1.00`
     - :math:`2/(2+1) = 0.67`

- **All 5:** three boxes match a person, two match nothing, nobody is
  missed. 6 in 10 boxes are real people, and every person is found.
- **Only the top 2:** both are right, so there is no false box. But one
  person in 3 has no box.

**Accepting more boxes raises recall and lowers precision.** On an AV, low
recall is a missed pedestrian, which is dangerous. Low precision is a
phantom pedestrian, which can mean a hard brake for nothing.


.. _l4-lec-ap:

Precision and Recall, Box by Box, and AP
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A detector does not give one answer but a ranked list of boxes, and precision
and recall change as you accept more of that list, from the surest box down.

The numbers are chosen for this example, and they are for **one class**,
person: 3 people in the ground truth, and 5 detections sorted by confidence.
AP is always computed one class at a time.

.. list-table::
   :widths: 16 16 34 34
   :header-rows: 1
   :class: compact-table

   * - **Conf.**
     - **Right?**
     - **Precision**
     - **Recall**
   * - 0.95
     - TP
     - 1/1 = 1.00
     - 1/3 = 0.33
   * - 0.90
     - TP
     - 2/2 = 1.00
     - 2/3 = 0.67
   * - 0.80
     - FP
     - 2/3 = 0.67
     - 2/3 = 0.67
   * - 0.60
     - TP
     - 3/4 = 0.75
     - 3/3 = 1.00
   * - 0.40
     - FP
     - 3/5 = 0.60
     - 3/3 = 1.00

Walk down the table. The first box is right: precision one out of one,
recall one out of three. The second is right too. The third is wrong:
precision drops to two out of three. The fourth finds the last person:
recall reaches three out of three. The fifth is wrong again.

.. figure:: /_static/images/L4/pr_example.png
   :alt: A plot of precision, the share of boxes that are right, against recall, the share of real people found, both from 0 to 1. Five orange points, one after each detection: (0.33, 1.0), (0.67, 1.0), (0.67, 0.67), (1.0, 0.75) and (1.0, 0.6). A blue step line runs at 1.0 up to recall 0.67, drops to 0.75 up to recall 1.0, then down to 0.6. The area under it is shaded and labeled area = AP = 0.917.
   :width: 60%
   :align: center

   Each row of the table as an **orange point**, precision against recall.
   The **blue line** keeps, at each recall, the best precision you can get at
   that recall or beyond. The shaded area under it is AP.

.. admonition:: Definition: AP (average precision)
   :class: note

   The area under the blue line, for one class.

Each person found adds :math:`\tfrac13` of recall, so the area is three
strips, :math:`\tfrac13` wide, at heights 1, 1 and 0.75:

.. math::

   \text{AP} = 0.333 + 0.333 + 0.250 = \mathbf{0.917}

**Read it as:** while finding all 3 people, on average 91.7 percent of the
boxes accepted were right. An AP of 1 would mean no false box comes before
the last person is found. It is one number that rewards finding everyone
without drawing extra boxes.

.. tip::

   COCO reads the line slightly differently. The appendix shows how
   (:doc:`l4_appendix`, "AP in detail").


.. _l4-lec-map:

From AP to mAP: What "mAP 44.9" Means
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Papers report one number, mAP, such as 44.9. It is built from the AP we just
computed.

1. **One class:** AP, the area under its precision-recall line. Our person
   example: 0.917.
2. **All classes:** average their APs, the **mean** AP. COCO has 80 classes,
   so 80 APs, one per class, are averaged into one number.
3. **How strict "right" is:** mAP@0.5 counts a box as right at IoU
   :math:`\ge 0.5`, a loose fit.
4. **mAP@0.5:0.95**, the COCO standard: steps 1 and 2 at 10 IoU thresholds,
   0.50, 0.55, ..., 0.95, averaged. Our IoU example's box (0.574) is right at
   0.50 and 0.55 only: 2 of 10. So this mAP rewards boxes that fit tightly.

.. admonition:: YOLOv8s: mAP@0.5:0.95 = 44.9
   :class: tip

   On COCO's validation images
   (`Ultralytics <https://docs.ultralytics.com/models/yolov8/>`__): averaged
   over 80 classes and 10 thresholds, the area under the line is 0.449.
   Papers write mAP@0.5:0.95 simply as "AP", so Ultralytics' 44.9 is what a
   paper calls 44.9 AP. On your own data, report both mAPs.

.. warning::

   **Trap:** mAP is computed at a confidence cut of **0.001**, the
   Ultralytics validation default, not 0.25, its prediction default. mAP
   scores the whole ranked list, down to the least sure box. Evaluate at
   0.25, the cut you use for pictures, and you throw away the bottom of the
   list: your mAP comes out lower than the published numbers.


.. _l4-lec-one-stage:

One-Stage Detectors
-------------------

- **Where we are:** a detection is a class, a confidence and a box; IoU and
  mAP grade it.
- **In this section:** the **first way** to get boxes: predict at every grid
  cell, then clean up the duplicates.
- **What it is for:** **YOLO**, our first model, about 3 times as fast as our
  second model on our image.

.. admonition:: Definition: one-stage detector
   :class: note

   A detector that predicts classes and boxes in **one pass** of the
   network, from every cell of its feature maps, then cleans up the
   duplicates (NMS, in this section). **YOLO** ("you only look once",
   Redmon et al., 2016) is the best-known family.

**One stage against two.** Older detectors, like Faster R-CNN (Ren et al.,
2015), worked in two stages: first propose regions that may hold an object,
then classify each one. A **two-stage** detector does both. A one-stage
detector skips the proposals and predicts straight from the grid. YOLO, "you
only look once", is named for exactly that.

**Why it matters here:** YOLO is the first of our two models. On our image
YOLOv8s takes 9.1 ms and RT-DETR-L takes 29.9 ms, both measured:
:math:`29.9 / 9.1 \approx 3.3`, so RT-DETR-L takes about three times as long.
We use YOLO; we do not take its versions apart.

Keep two weaknesses in mind for the next section:

- A convolution mixes only neighboring cells, so information from far parts
  of the image reaches a cell only after many layers.
- The duplicates need NMS.


.. _l4-lec-grid:

Where YOLO's Boxes Come From: the Grid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A one-stage detector gets its boxes from a grid. Here is the coarsest one,
stride 32: :math:`480/32 = 15` cells across and :math:`640/32 = 20` down. The
original image is 810 pixels wide, so one cell is :math:`810/15 = 54` image
pixels on a side.

.. figure:: /_static/images/L4/grid_cells.png
   :alt: Two panels. Left, titled the stride-32 grid: our image with a white grid over it, 15 cells across and 20 down; one cell on the man in the light-colored jacket, near his waist, is filled orange, an orange box surrounds him, and a dashed white frame marks the zoomed area. Right, titled zoom: one cell's box: the orange cell with a white dot at its center, and four white arrows from the dot to the four edges of the orange box, labeled 275.7 up, 85.0 to the left, 111.4 to the right and 227.4 down.
   :width: 70%
   :align: center

   **Left:** the stride-32 grid on our image. The orange cell holds the
   center of the man's box. **Right:** the zoomed area. From the dot at the
   cell's center, four arrows reach the four edges of the box: 85.0 pixels to
   the left, 275.7 up, 111.4 to the right and 227.4 down.

**Each cell predicts** 80 class scores, one per COCO class, and one box,
written as **four distances from its center**. With no preset box shapes,
YOLOv8 is called **anchor-free**.

The orange cell is column 2, row 12, counting from zero. Its center is at
:math:`(135,\ 675)` in image pixels, with :math:`y` down. Its person score is
**0.86**; every other class is near zero. Each distance gives one edge:

1. Left edge: :math:`135 - 85.0 = 50.0`.
2. Top edge: :math:`675 - 275.7 = 399.3`. :math:`y` grows downward, so up
   means subtract.
3. Right edge: :math:`135 + 111.4 = 246.4`.
4. Bottom edge: :math:`675 + 227.4 = 902.4`.

That is his box. The cell diagonally below it, column 3, row 13, predicts
almost the same box at **0.887**. That box survives the clean-up, so from
here on it is the man's cell.


.. _l4-lec-one-pass:

One Pass, No Search: Every Cell Answers at Once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Does the detector start at the cell's center and look around to grow the box?
No. The network runs once on the image, and that one run gives **every** cell
its 80 scores and its 4 distances at the same time. Measured, YOLOv8s:

.. figure:: /_static/images/L4/cell_reach.png
   :alt: Two panels of our image. Left, titled person score per cell: the stride-32 grid of 15 by 20 cells, with cells tinted orange where their person score is high; only cells on people are tinted, around the man in the light jacket, the man beside him and the person cut off at the right edge. Two neighboring cells on the man are outlined in dark blue and labeled 0.86 and 0.887. Right, titled what cell (3, 13) reads: the image faded to gray except where pixels change that cell's person score; the man, the bus behind him and the second man stay visible, while the street and the building are faded. A small dark square marks the cell, on the man's leg, and an orange box surrounds the man.
   :width: 75%
   :align: center

   **Left:** the person score of each of the 300 cells at stride 32, from a
   single run; the darker the orange, the higher the score. Our two cells
   score 0.86 and 0.887. **Right:** what cell (3, 13) reads. Bright pixels
   change its person score; faded pixels do not.

- **Left.** 31 of the 300 cells score above 0.25 for person, all on people.
  Our two cells each give their own, almost identical box. No cell waits for
  another or asks another.
- **Right.** For each pixel, we measured how much the cell's person score
  would change if that pixel changed a little. That is the **gradient**, the
  same tool training uses. Only **1.5 percent** of that influence comes from
  inside the cell's own 54 pixels. About half, **48.6 percent**, comes from
  inside the man's box, and the rest from around him: the bus behind him and
  the second man. That is how a 54-pixel cell can draw a box 195 pixels wide
  and 500 tall.
- **Box size.** The size is the sum of the distances, for cell (3, 13): left
  plus right is :math:`139.1 + 55.5 = 194.6` wide; top plus bottom is
  :math:`327.2 + 172.8 = 500.0` tall. Each distance is a weighted average of
  16 numbers the head outputs; the appendix decodes one
  (:doc:`l4_appendix`, "Decoding one cell").

So there is no search: the box comes straight out of the run.


.. _l4-lec-local:

What One Cell Reads: a 3 x 3 Window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The grid tells us where each prediction is made. Now: what can one cell see
when it makes it?

.. figure:: /_static/images/L4/local_conv.png
   :alt: Our image with the stride-32 grid of 15 by 20 cells, titled Convolution: a 3 x 3 window. The man's cell, on his leg, is orange; the 3 by 3 block of cells around it is shaded blue, with short white lines from the 8 neighboring cells into his cell.
   :width: 45%
   :align: center

   One :math:`3 \times 3` convolution on the stride-32 grid. It reads the
   man's cell (orange) and its **8 neighbors** (blue). Nothing else in the
   image reaches his cell in that layer.

- A cell's prediction comes from the CNN's feature maps, on the stride-32
  grid.
- One :math:`3 \times 3` convolution reads the man's cell and the 8 cells
  around it. That is all. The far end of the bus does not exist for this
  layer.
- The same filter slides over every cell, like the edge filter from
  :ref:`l4-lec-five-steps`, only now its weights are set by training.
  YOLOv8s's head ends with exactly this: two :math:`3 \times 3`
  convolutions, then a :math:`1 \times 1`, on each grid.
- Each further layer reaches one cell further on every side: 2 layers read
  :math:`5 \times 5` cells, 3 layers read :math:`7 \times 7`. The far end of
  the bus reaches his cell only after many layers.

.. admonition:: The intuition
   :class: tip

   A CNN works **locally**. Each layer passes information one cell further,
   neighbor to neighbor, like a message passed along a row of people.

Keep this picture. In :ref:`l4-lec-attention` we draw the same cell again,
and one attention layer reads every cell at once.


.. _l4-lec-ten-times:

Before Clean-up: Each Person Found about Ten Times
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

6300 cells each predict a box. Look at the raw output of YOLOv8s, before any
clean-up, and you find each person about ten times.

.. figure:: /_static/images/L4/nms_before_after.png
   :alt: Two copies of our image. Left, titled Before NMS: 49 boxes, drawn so closely on top of each other that each object looks like it has one thick box; labels count them: 10 boxes on the bus, 11 on the person cut off at the left edge, 9 on the man in the light jacket, 9 on the man in the black coat, and 10 on the person at the right edge. Right, titled After NMS: 5 boxes, one per object: bus 0.92, and person 0.61, 0.89, 0.88 and 0.89.
   :width: 90%
   :align: center

   **Left, before NMS:** 49 boxes. Each object seems to have one thick box,
   but each is about ten boxes nearly on top of each other: 10 on the bus,
   and 9 to 11 on each person. **Right, after NMS:** 5 boxes, one per
   object.

YOLOv8s predicts a box at every cell of its **three grids**, the three map
sizes from :ref:`l4-lec-cnn`. Each grid is the :math:`480 \times 640` input
divided by its stride:

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - **Stride**
     - **Grid**
     - **Cells**
   * - 8
     - :math:`480/8 \times 640/8 = 60 \times 80`
     - 4800
   * - 16
     - :math:`30 \times 40`
     - 1200
   * - 32
     - :math:`15 \times 20`
     - 300
   * - **all three**
     -
     - **6300**

Why three grids? The fine one, stride 8, has small cells for small objects;
the coarse one, stride 32, for large ones. YOLOv8's own file labels them
small, medium and large. Keep the boxes with confidence above 0.25, the
Ultralytics default, and **49** are left: :math:`10 + 9 + 9 + 10 + 11 = 49`,
about 10 per object.

.. admonition:: Why about 10?
   :class: tip

   During training, the library picks the 10 grid cells whose boxes fit each
   object best and teaches all 10 to predict that object. The setting is
   ``tal_topk=10``. So on a new image each object comes out about ten times.
   Something has to keep one of each.


.. _l4-lec-nms:

NMS: Keeping One Box per Object, in Four Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: non-maximum suppression (NMS)
   :class: note

   A clean-up step after a detector: keep the most confident box, and
   delete every box that overlaps it too much.

Think of ten witnesses reporting the same pedestrian, each pointing at a
slightly different spot. NMS keeps the most confident report and drops the
ones that describe the same place.

1. Sort all boxes by confidence, highest first.
2. Keep the top box.
3. Delete every box **of the same class** whose IoU with it is above
   **0.7** (the `Ultralytics <https://docs.ultralytics.com/usage/cfg/>`__
   default). Those are its duplicates.
4. Repeat with the boxes that are left. On our image: 49 in, **5** out.

**Why only boxes of the same class?** Picture a pedestrian stepping out from
behind a parked car. Their boxes overlap a lot. If NMS compared across
classes, the car's box, often the more confident one, would delete the
pedestrian. On an AV that is the worst possible mistake, so NMS runs per
class.

.. warning::

   **The trade-off: crowds.** Two people standing close together really do
   overlap. Set the threshold low, and NMS deletes one of the two real
   people. Set it high, and duplicates of the same person survive. No setting
   is right for every scene. The transformer detector in the next section is
   built so that it needs no NMS at all.


.. _l4-lec-train-yolo:

Training YOLO on Your Own Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To train YOLO on your own data, for example CARLA frames, you need label files
in its format. There is one text file per image and one line per object: the
class number, then the box center and its width and height, each divided by
the image's width or height, so every number lies between 0 and 1. The class
number is the position in your class list; in COCO's list, 0 is person.

.. code-block:: text

   0 0.1817 0.6035 0.2402 0.4630    # class cx cy w h

This line is the man in the light-colored jacket, from YOLOv8s's box: center
:math:`(147.2,\ 651.8)`, size :math:`194.6 \times 500.0`, in an
:math:`810 \times 1080` image. So :math:`147.2/810 = 0.1817` and
:math:`651.8/1080 = 0.6035`, and the same for the size.

.. code-block:: python

   from ultralytics import YOLO
   model = YOLO("yolov8s.pt")      # COCO-pretrained
   model.train(data="data.yaml", epochs=50, imgsz=640)  # 50 passes
   metrics = model.val()           # mAP, precision, recall

A few lines of Python: import the library, load the pretrained weights, train
on your data, and validate, which prints mAP@0.5, mAP@0.5:0.95, precision and
recall. ``data.yaml`` lists where your images are and the names of your
classes. Fifty **epochs** means fifty passes over the training images.


.. _l4-lec-transformers:

Transformers
------------

- **Where we are:** a CNN mixes only neighboring cells, and YOLO's
  duplicates need NMS.
- **In this section:** the **transformer**, the other way to build the
  network.
- **What it is for:** RT-DETR, our second model, and next week's bird's-eye
  view models and L11's driving models.

.. admonition:: Definition: transformer
   :class: note

   A network of stacked layers. Each layer has two steps: **attention**,
   where every **token** (one piece of the input, such as an image patch)
   takes in information from all the other tokens, then a small network
   applied to each token on its own.

First come the transformer's two halves, encoder and decoder, then what it
gives over a CNN-only detector on the road, and what it costs. Then the
encoder, part by part, on the Vision Transformer, and the decoder, from DETR
to RT-DETR.


.. _l4-lec-encdec:

The Transformer: an Encoder and a Decoder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The transformer was built for translation, in 2017 (Vaswani et al.). The
**encoder** reads the input; the **decoder** writes the output.

.. figure:: /_static/images/L4/transformer_encdec.png
   :alt: Two stacks of boxes side by side, data flowing up. Left, the encoder: tokens in, Embedding, a plus with position, then a dashed frame repeated N times holding Multi-head self-attention and MLP. Right, the decoder: decoder input, the text so far (DETR: object queries), Embedding, a plus with position, then a dashed frame repeated N times holding Multi-head self-attention, masked for text only, Multi-head cross-attention and MLP, then Linear and predictions. A green arrow labeled encoder output runs from the top of the encoder into the decoder's cross-attention. A line below: Not drawn: each block has a Norm before it, and its input is added back after it.
   :width: 70%
   :align: center

   The transformer, after Vaswani et al. (2017), Figure 1. **Left, the
   encoder:** tokens in, embedding, position added, then a layer of
   self-attention and an MLP, repeated :math:`N` times. **Right, the
   decoder:** its input (the text so far, or DETR's object queries),
   embedding, position, then a layer of self-attention, cross-attention and
   an MLP, repeated :math:`N` times, then a linear layer that makes the
   predictions. The **green arrow** carries the encoder's output into the
   decoder's cross-attention.

- **Embedding and position.** Each input is first embedded, turned into a
  vector, and its position is added.
- **Encoder.** It repeats one layer :math:`N` times. In each, every token
  takes in all the others, which is **self-attention**, and then a small
  network, the **MLP** (multilayer perceptron), works on each token alone.
- **Decoder.** It repeats a layer with three steps. Its inputs take in each
  other. Then they take in the encoder's output, the green arrow: that is
  **cross-attention**. Then the MLP. At the top, a linear layer makes the
  predictions.
- **Masked, for text.** When the decoder writes a sentence one word at a
  time, each word may look only at the words before it. While it writes
  "atteint", it cannot see "la rive" yet. **DETR** (DEtection TRansformer),
  the first detection transformer, does not write one box at a time; it
  decodes all its queries at once, so it uses no mask.
- **Not drawn:** a normalization before each block, and each block's input
  added back after it. :ref:`l4-lec-encoder-layer` opens one layer.

ViT, the Vision Transformer, uses only the encoder; DETR and RT-DETR use both
halves.

**In a sentence:** the encoder reads "The boat reached the bank"; the decoder
writes "Le bateau a atteint la rive", one word at a time, looking back at the
English. The whole section keeps this sentence.


.. _l4-lec-scenario:

Scenario: Why a Second Kind of Network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Why learn a second kind of network at all? Here is a scene, made up for this
example.

.. figure:: /_static/images/L4/av_scenario.jpeg
   :alt: A pencil-style drawing on graph paper. Left: a small AV approaches a crosswalk with a red traffic light, then waits at the crosswalk, seen from behind. A camera icon and an arrow point to the right part, titled camera data perspective, AV sensor view: a bus facing the camera fills much of the view, labeled bus, object ID BUS-01; to its right two pedestrians walk across the crosswalk, the second partly behind the first, labeled pedestrian-01, active crossing, and pedestrian-02; further back a small figure is labeled pedestrian-03, distant, far away.
   :width: 95%
   :align: center

   **Left:** the AV drives up to a crosswalk and waits at the red light.
   **Right:** what its front camera sees: a bus facing the AV fills much of
   the image, two pedestrians cross together, the second partly hidden
   behind the first, and a third pedestrian is far away and small.

Three objects, three kinds of trouble for a detector: one very large, two that
overlap, one very small. Here is how each kind of network handles each one.

.. list-table::
   :widths: 22 36 42
   :header-rows: 1
   :class: compact-table

   * -
     - **One-stage CNN** (YOLO)
     - **Transformer** (RT-DETR)
   * - **The bus** (large)
     - each cell reads its neighbors; the far end arrives only after many
       layers
     - one layer links the whole image; without it, DETR loses 6.0 AP on
       large objects (Carion et al., 2020)
   * - **Two pedestrians** (one partly hidden)
     - about 10 boxes each; NMS can delete the hidden person
     - one box per object, no NMS
   * - **Far pedestrian** (small)
     - the fine stride-8 grid
     - DETR was weaker here; RT-DETR adds multi-scale features

- **The bus.** A transformer links the whole image in one layer: that is
  **context**. The authors of DETR removed its encoder layers, the part that
  links the whole image, and lost 3.9 AP overall and 6.0 AP on large
  objects.
- **The two pedestrians.** YOLO finds each about ten times, and NMS deletes
  boxes that overlap the best one too much. If the two pedestrians overlap
  enough, a real person is deleted. A transformer outputs one box per object,
  with no NMS; :ref:`l4-lec-decoder` shows how.
- **The far pedestrian** is small, and that was a weak spot: the original
  DETR did worse on small objects. RT-DETR fixes much of that by using
  feature maps at several scales, like YOLO's three grids.

.. admonition:: So, mostly context
   :class: tip

   In one transformer layer, every part of the image can change every other
   part. And the boxes are predicted together, so two of them do not end up
   on the same object, with no NMS. **The price:** 29.9 ms against 9.1 ms on
   our image, and more training data. RT-DETR-L also keeps a CNN backbone,
   with the transformer on top.


.. _l4-lec-analogy:

One Analogy for This Section: an Image Read like a Sentence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Transformers were invented for text, so the easiest way into them is to read
our image the way a transformer reads a sentence. One sentence for the whole
section: **"The boat reached the bank."**

Each part we meet has a partner in that sentence. The numbers are the parts
in the order we meet them.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **In the transformer**
     - **In the sentence**
   * - image, 1. patch
     - the sentence, one word
   * - 2. pixel values, embedding :math:`E`
     - the word's letters; a learned vector per word, as in word2vec
   * - 2. token
     - the word as the model holds it: its vector
   * - 4. position
     - word order: "the bank reached the boat" has the same words
   * - 5. attention
     - each word reads the others: "bank" reads "boat"
   * - 5. query, key, value
     - "bank" asks: water or money? "boat" answers: water
   * - 6. encoder layer
     - one reading of the sentence; ViT-Base reads it 12 times
   * - 6. contextual embedding
     - "bank" after reading: the river kind
   * - 3., 7. class token, head
     - a blank word in front that ends up holding the gist
   * - decoder (DETR)
     - writing a translation, looking back at the original

Most subsections that follow end with an **In a sentence** line that works
the part out on these five words.


.. _l4-lec-encoder:

Encoder
~~~~~~~

- **Where we are:** a transformer has two halves, and its main gain is
  context.
- **In this subsection:** the **encoder**, part by part, through the Vision
  Transformer (ViT): patches, embedding, class token, position, attention,
  the encoder layer, the head.
- **What it is for:** every transformer detector reads its input with an
  encoder. RT-DETR's reads the feature map of its CNN backbone.

.. admonition:: Definition: encoder
   :class: note

   The half of a transformer that reads the input: a stack of layers, each
   self-attention then an MLP. Tokens in, the same number of tokens out, each
   now carrying the context of the others.

The **Vision Transformer** (ViT) is the plain transformer for images. The
parts below are numbered as in the ViT figure two subsections on.


The Encoder: Tokens in, the Same Number of Tokens out
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before we open the encoder, here is what goes in and what comes out, for
ViT-Base on our image.

.. list-table::
   :widths: 24 38 38
   :header-rows: 1
   :class: compact-table

   * -
     - **In**
     - **Out**, after 12 layers
   * - **What**
     - 197 tokens: 196 patches and the class token
     - 197 tokens, in the same order
   * - **Size**
     - :math:`197 \times 768`
     - :math:`197 \times 768`
   * - **A patch's token**
     - its own :math:`16 \times 16` pixels, and where they were
     - its patch, plus information from the other 196 tokens
   * - **The class token**
     - a learned start vector, the same for every image
     - a summary of the whole image

The encoder does not add or remove tokens; it changes what each one holds.

**Our image.** The token of a patch on the man's jacket goes in describing only
its own pixels. After 12 layers, the same token also carries information from
the other tokens: the bus behind him, the street below. The class token,
which started empty of any image, now holds a summary of the whole image. The
head reads "minibus" from it.

**In a sentence:** going in, "bank" could be the river or the money kind.
Going out, after 12 layers, it also carries "boat" and stands for the river
kind.

How a token gets information from the others is **attention**, part 5 in the
next figure.


ViT-Based Architecture
^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L4/vit_arch_flow.png
   :alt: The Vision Transformer, ViT-Base, step by step, in nine panels. Top row, joined by arrows: Input image, our image at 224 by 224 by 3; 1 Patches, the image with a 14 by 14 grid, 196 patches, 16 by 16; 2 Embedding, four sample patches, each with an arrow to a short blue bar, times E, 196 by D; 3 Class token, an orange bar labeled CLS put in front of the blue bars, in front, 197 by D; 4 Position, each bar plus a gray bar, plus learned, 197 by D. An arrow leads to the bottom row: 6 Encoder layer, repeated 12 times: Norm, 5 Multi-head attention, plus, Norm, MLP, plus, with two arrows carrying each block's input to its plus sign, 197 by D in, 197 by D out; 7 Class token, the orange CLS bar kept, 1 by D; 7 Head, Linear, 768 to 1000, 1000 scores; Prediction: minibus 0.451, trolleybus 0.282, police van 0.013, passenger car 0.008, answer minibus.
   :width: 100%
   :align: center

   ViT-Base (Dosovitskiy et al., 2021) on our image, :math:`D = 768`: an
   **encoder** and a linear **head**, no decoder. The green numbers are the
   parts that follow. Prediction measured with torchvision's ViT-B/16.

Read it from left to right, then along the bottom.

1. **Patches.** The image, squeezed to :math:`224 \times 224`, is cut into
   196 patches of :math:`16 \times 16`.
2. **Embedding.** The matrix :math:`E` turns each patch into a vector of
   :math:`D` numbers, 768 here: 196 tokens.
3. **Class token.** An extra token, the class token, is put in front.
4. **Position.** A learned position vector is added to every one of the 197.
   The paper does it in that order, so there are 197 position vectors, not
   196.
5. **Multi-head attention**, inside part 6, where every token takes in all
   the others.
6. **Encoder layer**, repeated 12 times: a norm, then multi-head attention,
   then the input added back; then a norm, the MLP on each token, and the
   input added back again. 197 tokens in, 197 out.
7. **Class token and head.** Keep only the class token and multiply it by the
   head, one linear layer, 768 to 1000: one score per ImageNet class. On our
   image the top answer is **minibus, 0.451**, then trolleybus, 0.282.

**Where is the decoder?** There is none. A decoder is for many outputs that
depend on each other, like the words of a translation or DETR's boxes. One
label for the whole image needs only the head, which reads it from the class
token. :ref:`l4-lec-decoder` adds a decoder, to output boxes.


1. Patch: the Image Cut into Squares
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A transformer works on a list of pieces, so an image has to be cut up first.

.. admonition:: Definition: patch
   :class: note

   A small square of the image, cut on a fixed grid: here
   :math:`16 \times 16` pixels. Its :math:`16 \times 16 \times 3 = 768` pixel
   values are the input for that square.

.. figure:: /_static/images/L4/vit_patches.png
   :alt: Our image squeezed to 224 by 224 pixels, with a white grid cutting it into 14 by 14 squares of 16 by 16 pixels. One square on the man's jacket, row 7, column 3 counting from 0, is outlined in orange.
   :width: 50%
   :align: center

   Our image squeezed to :math:`224 \times 224` and cut into
   :math:`16 \times 16` patches. The **orange square**, on the man's jacket,
   is the patch we follow for the rest of the section.

Our image is squeezed to :math:`224 \times 224` pixels, the input size of the
original Vision Transformer. Squeezing an :math:`810 \times 1080` image into a
square distorts it a little. Cut into :math:`16 \times 16` squares, it gives
:math:`14 \times 14 = 196` patches.

Detectors often skip the patches and use the cells of a CNN feature map
instead: each cell already describes its square well. RT-DETR does that.

**In a sentence:** cut the sentence into words, "The", "boat", "reached",
"the", "bank": 5 words. Cut the image into squares: 196 patches.


1. Counting the Patches: 224 / 16 = 14 per Side
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L4/patch_count.png
   :alt: Our image squeezed to 224 by 224 pixels, with arrows marking 224 pixels across the top and 224 pixels down the side. A white grid cuts it into squares, numbered 1 to 14 along the top and 1 to 14 down the side. The top-left square is outlined in blue and labeled one patch: 16 x 16 pixels.
   :width: 55%
   :align: center

   The patches counted on the grid: 14 across, 14 down. The blue square in
   the corner is the first patch, :math:`16 \times 16` pixels.

1. The image: :math:`224 \times 224` pixels.
2. One patch: :math:`16 \times 16` pixels.
3. Across: :math:`224 / 16 = 14` patches.
4. Down: :math:`224 / 16 = 14` patches.
5. All of them: :math:`14 \times 14 = \mathbf{196}` patches.

16 divides 224 exactly, so no pixel is left over at the edges. Each patch
holds :math:`16 \times 16 \times 3 = 768` numbers.

.. admonition:: Why 224
   :class: tip

   ViT was trained on :math:`224 \times 224` images; the paper says "all
   training is done on resolution 224". So it learned this
   :math:`14 \times 14` layout of patches. To use it as trained, every image
   is resized to :math:`224 \times 224` first, **smaller ones too**; Hugging
   Face's ViT preprocessing does it by default. A smaller image, say
   :math:`100 \times 100`, is stretched up to 224. The new pixels are blends
   of their neighbors, so the image gains pixels but no detail.

The other way is to keep a different size: the patches stay
:math:`16 \times 16` and their number changes. :math:`384 \times 384` gives
:math:`24 \times 24 = 576` patches. Then the learned layout must be stretched
to match, which the paper does when it fine-tunes at 384.

**In a sentence:** our sentence is 1 row of 5 words; our image is 14 rows of
14 patches.


2. Embedding, Step 1: Each Patch as One Line of 768 Numbers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: embedding
   :class: note

   Turning each piece of the input into a vector of :math:`D` numbers that
   the network can compare and combine. ViT does it in two steps:
   **1.** read each patch's pixels into one line of 768 numbers;
   **2.** multiply that line by a learned matrix :math:`E`.

The first step only rearranges numbers.

.. figure:: /_static/images/L4/vit_flatten.png
   :alt: Three panels from our image, all real pixel values. Cut into patches: the image squeezed to 224 by 224 with a 14 by 14 grid, one patch on the man's jacket outlined in orange; 224 x 224 x 3, 14 x 14 = 196 patches. One patch: that patch enlarged, 16 x 16 x 3, light jacket on the left and blue bus on the right, and below it the same patch read row by row into a strip of 768 numbers, drawn in gray. All 196 patches, stacked: a gray matrix of 196 rows and 768 columns of pixel values, one row per patch, our patch's row outlined in orange.
   :width: 100%
   :align: center

   **Left:** the image, cut into 196 patches; the orange square is one of
   them. **Middle:** that patch, enlarged, :math:`16 \times 16` pixels with
   three colors each, read row by row into one line of 768 numbers.
   **Right:** all 196 lines stacked into a :math:`196 \times 768` matrix of
   real pixel values; the orange row is our patch.

**Step 1:** each patch is read row by row, :math:`16 \times 16 \times 3 =
768` numbers, and the 196 lines are stacked: a :math:`196 \times 768` matrix.
Nothing has been learned yet.

**In a sentence:** step 1 only lines up the letters of "bank" in a row, b, a,
n, k: its spelling, not its meaning. Our patch's row of 768 values is its
spelling.


2. Embedding, Step 2: the Learned Matrix E
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Step 2:** multiply by :math:`E`, a :math:`768 \times D` matrix of weights
**set by training**, like every other weight. This is where learning starts.

.. figure:: /_static/images/L4/vit_embed.png
   :alt: A matrix product. Left: the real 196 by 768 matrix of pixel values, drawn in gray, with our patch's row in orange, labeled orange: our patch, 768 numbers. Times E, 768 by D, learned, drawn as a tan rectangle with one column in blue, labeled column j: 768 weights. Equals the tokens, 196 by D, drawn green, with one cell in orange labeled feature j of our patch, equal to the orange row times the blue column, 768 products, added.
   :width: 90%
   :align: center

   The embedding as a matrix product. In the pixel matrix, a **row** is a
   patch (orange: ours). In :math:`E`, a **column** is a feature (blue:
   column :math:`j`, 768 weights). Their 768 products, added, give one number:
   **feature** :math:`j` **of our patch**, the orange cell of the result.

That is what our :math:`3 \times 3` filter did, nine products added, only now
with 768. :math:`E` has :math:`D` columns, so each patch gets :math:`D`
features.

**The result.** Each patch's row meets **all 768 columns**, so it gets 768
numbers, each saying how strongly the patch matches one learned pattern: like
our edge filter, but 768 filters, each used once per patch. In ViT-Base
:math:`D = 768`, so :math:`E` holds :math:`768 \times 768 = 589{,}824`
weights, and the same :math:`E` serves all 196 patches. The paper calls the
result the patch embeddings; each output row is one **token**, named a few
subsections on.

**In a sentence:** **word2vec** gives each word a learned vector; :math:`E`
gives each patch one. The appendix shows word2vec's vectors
(:doc:`l4_appendix`, "Vectors you can add").


2. Embedding: Our Patches as Vectors, Before and After
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is what the vectors of our own image look like.

.. figure:: /_static/images/L4/vit_patch_map.png
   :alt: Two plots, not pictures of space, with axes labeled first summary number and second summary number. Each of our 196 patches is drawn as its own small thumbnail at the two numbers that best summarize its vector, framed by its region from YOLOv8s's boxes: orange for person, blue for bus, gray for other. Left, titled before the encoder: E vectors, 5 nearest neighbors, same region: 49 percent: the frames of all three colors are mixed in one cloud. Right, titled after the 12 encoder layers, 84 percent: gray patches gather at the bottom left, blue bus patches at the bottom right, orange patches of the people toward the top.
   :width: 100%
   :align: center

   Each of the 196 patches drawn as its own small picture, placed at the two
   numbers that best summarize its 768. **This is a plot, not a map of the
   image.** The frame color is the patch's region, taken from YOLOv8s's
   boxes: orange a person, blue the bus, gray everything else.

- **Left, the vectors straight out of** :math:`E`. The colors are mixed:
  patches sit near patches that look alike, light near light, dark near
  dark, whatever they belong to.
- **Right, the same patches after the 12 encoder layers.** The bus patches
  gather at the bottom right, the gray patches at the bottom left, the people
  toward the top.

**The score.** For each patch, take the 5 patches whose vectors are most like
its own, wherever they sit in the image, and count how many share its region
(frame color). Averaged over all 196 patches, that is **49 percent** before
the encoder and **84 percent** after. If the vectors were placed at random,
it would be 35 percent.

So :math:`E` groups patches by how they look, and the encoder groups them by
what they belong to.

**In a sentence:** before reading, "bank" sits near "band": they look alike.
After, it sits near "boat": they go together.


2. Embedding, Step 2 with Numbers: Feature 1 of Our Patch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is one feature of our patch worked out with real numbers: our orange
patch times column 1 of :math:`E`. Every number comes from torchvision's
ViT-B/16 with ImageNet weights, on our image. The code counts from zero, so
feature 1 is the second number of the token; feature 0 is the first. The
first pixel of the patch is :math:`(214, 190, 159)`.

.. list-table::
   :widths: 28 24 24 24
   :header-rows: 1
   :class: compact-table

   * - **Input**
     - **Value, rescaled**
     - **Weight in column 1**
     - **Product**
   * - pixel 1, red
     - 1.547
     - -0.0076
     - -0.0118
   * - pixel 1, green
     - 1.291
     - -0.0153
     - -0.0198
   * - pixel 1, blue
     - 0.967
     - -0.0084
     - -0.0081
   * - 765 more
     - ...
     - ...
     - ...

1. **Rescale** each value the way the weights were trained: divide by 255,
   subtract ImageNet's mean for that color, divide by its spread. For the
   red of the first pixel:

   .. math::

      (214/255 - 0.485)/0.229 = 1.547

2. **Multiply** each of the 768 values by its weight in column 1. The first
   three products are all small and negative.
3. **Add** the 768 products: -0.282. Of the 768, 368 are positive and push
   the feature up, and 400 are negative and push it down.
4. **Add the layer's learned offset**, 0.022:
   :math:`-0.282 + 0.022 = \mathbf{-0.26}`, the second number of our token
   (next subsection).

Each of the 768 features is made the same way, with its own column.


2. Embedding: What the 768 Columns of E Look Like
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each column of :math:`E` holds 768 weights, one per pixel value, so we can draw
it as a :math:`16 \times 16` color patch. It is our :math:`3 \times 3` edge
filter again, bigger, in color, and set by training.

Drawn one at a time, a column looks like noise. So, as the ViT paper does, we
draw the patterns the columns share, their **principal components**. The
paper says they resemble plausible basis functions for the fine structure
within each patch. Measured on torchvision's ViT-B/16:

.. figure:: /_static/images/L4/vit_E_patterns.png
   :alt: Twelve small 16 by 16 color patches, patterns 1 to 12, the main patterns shared by the columns of E. Pattern 1, green above magenta, labeled top against bottom. Patterns 2 and 3, a magenta or blue spot inside a ring of another color, labeled center against surround. Pattern 5, outlined in orange, green on the left and magenta on the right, labeled left against right: like our edge filter. The others show finer stripes, checkers and spots near the center.
   :width: 95%
   :align: center

   The 12 main patterns shared by the columns of :math:`E`. **Pattern 5**,
   outlined in orange, is left against right, green beside magenta: a
   vertical edge in color, the same idea as the filter we built by hand.
   **Pattern 1** is top against bottom. **Patterns 2 and 3** are a spot
   inside a ring. The rest are finer stripes and checkers.

Feature :math:`j` says how strongly a patch matches column :math:`j`: positive
for the pattern, negative for its opposite. These 12 patterns cover only **21
percent** of how the columns vary, so most columns mix many patterns, and no
single column has a name.


2. Embedding Output: One Token per Patch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The embedding gave us one vector per patch. That vector has a name used for
the rest of the section.

.. admonition:: Definition: token
   :class: note

   One piece of the input, turned into a vector of :math:`D` numbers. For an
   image, one embedded patch; in a language model, a word or part of a word,
   which is where the name comes from.

.. figure:: /_static/images/L4/vit_token.png
   :alt: Our patch, 16 x 16 x 3, light jacket on the left and blue bus on the right, and an arrow to its token: a strip of 768 thin colored bars, red for positive and blue for negative values, titled its token: 768 numbers, set by E. Below: (0.02, -0.26, 0.10, 0.02, ..., 0.10), and red: positive, blue: negative; -2.93 to 2.32.
   :width: 100%
   :align: center

   A real token: our orange patch through the embedding of torchvision's
   ViT-B/16, ImageNet weights, on our image squeezed to
   :math:`224 \times 224`. 768 numbers, drawn as bars, red for positive and
   blue for negative. The first four are 0.02, -0.26, 0.10 and 0.02, and the
   values range from -2.93 to 2.32.

Each of those numbers includes the learned offset from the last worked
example. No single number means anything on its own; together they describe
the patch for the network.

Our image gives 196 such tokens, a :math:`196 \times 768` matrix; the class
token (next) makes 197. From here on the transformer never looks at a pixel
again: attention, the norm and the MLP all work on tokens.

**In a sentence:** "bank" becomes a list of 768 numbers, the same list
wherever the word appears. That list is its token.


3. Class Token: One Extra Token for the Answer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At the end, the head turns **one** row of 768 numbers into the answer for the
whole image. But we have 196 rows, one per patch, and each one describes only
its own :math:`16 \times 16` place. Which one should the head read? None of
them.

.. admonition:: Definition: class token
   :class: note

   One extra token put in front of the patch tokens (Dosovitskiy et al.,
   2021). Its 768 numbers are set by training and are the same for every
   image. The encoder mixes every patch into it, and the head reads the
   answer from it alone.

Going in, the class token says nothing about our picture. On our image:

1. **In:** row 0 is the class token, rows 1 to 196 are our patches:
   :math:`197 \times 768` numbers.
2. Each of the 12 encoder layers mixes all 196 patches into row 0 (part 5
   shows how).
3. **Out:** the head reads row 0 only and ignores the other 196. 768 numbers
   become 1000 class scores. Top score: **minibus, 0.451**.

**In a sentence:** put a blank word, CLS, in front: "CLS The boat reached the
bank". CLS is no word of the sentence. After the encoder it holds all five,
and a reader of CLS alone can say: a river, not money.


4. Position Embedding: Where Each Token Came From
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After the embedding, each token says what its patch looks like, but not where
it was.

.. admonition:: Definition: position embedding
   :class: note

   A learned vector for each token position, added to the token, so the
   network knows where its patch was in the image.

- **Why:** the encoder layers treat the tokens as a set. Shuffle the 196
  tokens and every output comes out the same, only shuffled. A patch of sky
  would mean the same at the top of the image as at the bottom.
- **How many:** 197, one per token, the class token included:
  :math:`197 \times D` numbers.
- **The paper says it plainly:** "Position embeddings are added to the patch
  embeddings to retain positional information" (Dosovitskiy et al., 2021).

**In a sentence:** the same 5 words in two orders, "The boat reached the
bank" and "The bank reached the boat". They mean different things, but
without position the model sees the same set. The position embedding is the
word order.


.. _l4-lec-attention:

5. Attention: Each Token Takes in the Others
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Part 5, attention, is the step where tokens share information.

.. admonition:: Definition: attention
   :class: note

   A step that gives each token a new vector: a weighted average of all the
   tokens, where each weight says how much that token matters to it. The
   weights are computed from the tokens, for each image, and add up to 1.

The weights are not fixed like a filter's: they are computed from the tokens
themselves, for each image.

.. figure:: /_static/images/L4/global_attn.png
   :alt: Our image with the stride-32 grid of 15 by 20 cells, titled Attention: all 300 cells. The man's cell, on his leg, is orange, and thin orange lines run from every cell of the grid into his cell.
   :width: 45%
   :align: center

   One attention layer on the detector's stride-32 grid: all 300 cells feed
   the man's cell (orange). The lines are drawn all alike: they show which
   cells are read, not how much each one counts.

The figure uses the detector's stride-32 grid from :ref:`l4-lec-local`, 300
cells, not ViT's 196 patches; attention works the same on either. Each cell
is a token. There, one :math:`3 \times 3` convolution read the man's cell and
its 8 neighbors. Here, **one attention layer brings in all 300 cells**.

Attention is the only place where tokens share information. The norm and the
MLP in the layer work on one token at a time. So everything a token learns
about the rest of the image, it learns here.

**Multi-head** attention means several attentions side by side, each with its
own learned weights, so one head can follow shape and another color. ViT-Base
has 12 heads.

**In a sentence:** to read "bank", look at the 4 other words: "boat" gets the
largest weight, "The" almost none. The new "bank" is their weighted average.

.. tip::

   The appendix compares a CNN and a transformer side by side
   (:doc:`l4_appendix`, "CNN and transformer").


5. Query, Key and Value
^^^^^^^^^^^^^^^^^^^^^^^

Each token has to find out which other tokens matter to it. So each token's
vector is multiplied by three weight matrices, set by training like every
other weight, to make three new vectors:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * -
     - **What it is**
     - **In "The boat reached the bank"**
   * - **Query** :math:`q`
     - what this token is looking for
     - "bank" asks: water or money?
   * - **Key** :math:`k`
     - what this token can offer
     - "boat" says: about water
   * - **Value** :math:`v`
     - what it passes on if chosen
     - what "boat" hands to "bank"

The better a key matches the query, the more of that word's value flows into
"bank". "Reached" says little. The formula, from the 2017 paper that
introduced transformers (Vaswani et al.):

.. math::

   \text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d}}\right) V

- :math:`Q`, :math:`K`, :math:`V`: all the queries, keys and values, one row
  per token.
- :math:`QK^{\top}` scores every query against every key.
- :math:`d` is the length of each vector. Dividing by :math:`\sqrt{d}` keeps
  the scores from growing with :math:`d`.
- **Softmax** turns the scores into weights that are positive and add up to
  1. Then the weights average the values.

It looks heavy. The next three steps do it by hand with three tokens.


5. Attention by Hand, Step 1: Score Each Key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Chosen for this example: three patch tokens, a **wheel**, a **bus window** and
the **sky**, with vectors of length :math:`d = 2`. In a real network, each
query, key and value is the token's vector times a matrix set by training;
here we skip that and pick them directly. We ask what the wheel attends to, so
we take the wheel's query, :math:`q = (1, 0.5)`, and score it against every
key, its own included.

.. list-table::
   :widths: 14 17 21 21 13 14
   :header-rows: 1
   :class: compact-table

   * - **Token**
     - **Key** :math:`k`
     - **First numbers**
     - **Second numbers**
     - **Score** :math:`q \cdot k`
     - :math:`\div \sqrt{2}`
   * - wheel
     - (1, 0)
     - :math:`1 \times 1 = 1`
     - :math:`0.5 \times 0 = 0`
     - 1.0
     - 0.707
   * - window
     - (0.6, 0.8)
     - :math:`1 \times 0.6 = 0.6`
     - :math:`0.5 \times 0.8 = 0.4`
     - 1.0
     - 0.707
   * - sky
     - (-0.5, 0.2)
     - :math:`1 \times (-0.5) = -0.5`
     - :math:`0.5 \times 0.2 = 0.1`
     - -0.4
     - -0.283

1. **Score** :math:`q \cdot k` (the **dot product**): multiply the two first
   numbers, multiply the two second numbers, and add. Large: the key matches
   the query. Below zero: it points the other way.
2. **Divide by** :math:`\sqrt{d} = \sqrt{2} = 1.414`:
   :math:`1.0 / 1.414 = 0.707` and :math:`0.4 / 1.414 = 0.283`, so the sky
   gets 0.283 below zero. With long vectors the sums get large, and this
   division keeps them in range.

The wheel and the window both score 1.0: the wheel is as interested in the
window as in itself. The sky scores below zero: its key points away from what
the wheel looks for.

**In a sentence:** the query of "bank" matches the key of "boat", as the
wheel's query matches the window's key: a high score.


5. Attention by Hand, Step 2: Weights and the New Value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Step 1 gave the wheel three scores: 0.707 for itself, 0.707 for the window,
and 0.283 below zero for the sky. Now we turn them into weights.

1. **Raise** :math:`e` to each score: :math:`e^{0.707} = 2.028` (wheel and
   window), :math:`e^{-0.283} = 0.754` (sky). All are positive, so no weight
   can come out below 0, and a higher score still gives a larger number.
2. **Divide** each by their sum, :math:`2.028 + 2.028 + 0.754 = 4.810`:
   :math:`2.028 / 4.810 = 0.422` and :math:`0.754 / 4.810 = 0.157`. The
   weights add to 1, up to rounding. These two operations together are the
   **softmax**.
3. **Multiply** each value by its weight and add, first numbers with first
   numbers, second with second. The values are chosen for this example, as
   (wheel-ness, window-ness); the sky has nothing to pass on.

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1
   :class: compact-table

   * - **Token**
     - **Weight**
     - **Value** :math:`v`
     - **Weight** :math:`\times` :math:`v`
   * - wheel
     - 0.422
     - (1, 0)
     - (0.422, 0)
   * - window
     - 0.422
     - (0, 1)
     - (0, 0.422)
   * - sky
     - 0.157
     - (0, 0)
     - (0, 0)
   * - **New value of the wheel**, the sum
     -
     -
     - **(0.42, 0.42)**

**Why make every weight positive?** Divide the raw scores by their sum
instead, 1.6, and the sky gets 0.25 below zero: the wheel would take the sky's
value away instead of mixing it in.

The wheel said :math:`(1, 0)`, "wheel". Now it says "wheel, and part of
something with windows", which is how a network learns that this wheel
belongs to a bus. The sky still gets 0.157: softmax never gives exactly zero.

**In a sentence:** the new "bank" takes most of its value from "boat", so it
now reads as the side of a river.


5. Attention by Hand, Step 3: the Window and the Sky
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We did this for the wheel's query only. The window and the sky have queries
too. Same keys and values as before; the two queries are chosen for this
example. The window looks mostly for window-ness: :math:`q = (0.5, 1)`. The
sky looks away from wheels: :math:`q = (-2, 0)`.

**Window**, :math:`q = (0.5, 1)`:

.. list-table::
   :widths: 28 24 24 24
   :header-rows: 1
   :class: compact-table

   * - **Key of**
     - wheel
     - window
     - sky
   * - :math:`q \cdot k`
     - 0.5
     - 1.1
     - -0.05
   * - :math:`\div \sqrt{2}`
     - 0.354
     - 0.778
     - -0.035
   * - :math:`e^{x}`
     - 1.425
     - 2.177
     - 0.966
   * - :math:`\div` sum 4.568
     - **0.312**
     - **0.477**
     - **0.211**

New value: :math:`0.312\,(1, 0) + 0.477\,(0, 1) = \mathbf{(0.31, 0.48)}`.

**Sky**, :math:`q = (-2, 0)`:

.. list-table::
   :widths: 28 24 24 24
   :header-rows: 1
   :class: compact-table

   * - **Key of**
     - wheel
     - window
     - sky
   * - :math:`q \cdot k`
     - -2
     - -1.2
     - 1.0
   * - :math:`\div \sqrt{2}`
     - -1.414
     - -0.849
     - 0.707
   * - :math:`e^{x}`
     - 0.243
     - 0.428
     - 2.028
   * - :math:`\div` sum 2.699
     - **0.090**
     - **0.159**
     - **0.751**

New value: :math:`0.090\,(1, 0) + 0.159\,(0, 1) = \mathbf{(0.09, 0.16)}`.

**After one attention step**, as (wheel-ness, window-ness): wheel
:math:`(0.42, 0.42)`, window :math:`(0.31, 0.48)`, sky :math:`(0.09, 0.16)`.
The wheel and the window now each carry some of the other: both are part of
the same bus. The sky keeps most of its weight on itself, so it stays close to
:math:`(0, 0)`. It still takes a little from the bus, because softmax never
gives exactly zero.

Stack the three rows of weights and you get a :math:`3 \times 3` matrix: that
is :math:`\text{softmax}(QK^{\top}/\sqrt{d})`, the matrix form, one row per
query. The network computes all rows at once.

**In a sentence:** every word asks its own question at the same time: "bank"
looks for what it is about, "boat" for where it went.


5. Self-Attention and Cross-Attention
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Attention comes in two kinds, depending on who asks the questions.

.. list-table::
   :widths: 22 42 36
   :header-rows: 1
   :class: compact-table

   * -
     - **Queries come from**
     - **Used in**
   * - **Self-attention**
     - the same tokens as the keys and values: the image attends to itself
     - Vision Transformer (this subsection), DETR's encoder
   * - **Cross-attention**
     - a **different** set: for example, one query per object to be found
     - DETR's decoder, BEVFormer (L5)

- **Self-attention:** the queries, keys and values all come from the same
  tokens, as in the wheel example.
- **Cross-attention:** the queries come from a different set. For example, a
  set of queries, one per object we hope to find, each asking the image
  tokens "is my object here?". DETR's decoder works this way, and next week
  BEVFormer uses it to fill a map of the ground from camera images.

The position embeddings from part 4 are why this works on images: without
them, attention could not tell one patch's place from another's.

**In a sentence:** self: "bank" reads "boat", in the same sentence. Cross:
while writing "rive", the French reads the English "bank".


.. _l4-lec-encoder-layer:

6. Inside One Encoder Layer
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Part 6 is the whole encoder layer, which ViT-Base repeats 12 times.

.. figure:: /_static/images/L4/transformer_layer.png
   :alt: One encoder layer as a row of blocks: tokens in, 197 by D; Norm; Multi-head attention, 12 heads, labeled tokens exchange information; a plus sign; Norm; MLP, 2 layers, 768 to 3072 to 768, labeled each token on its own; a plus sign; tokens out, 197 by D. Two arrows labeled add the input back carry each block's input around it to its plus sign.
   :width: 100%
   :align: center

   One encoder layer. **Multi-head attention** (12 heads), where tokens
   exchange information, then the **MLP**, which works on each token on its
   own. A norm comes before each block, and each block's input is added back
   after it.

- **MLP:** a small network of 2 layers, run on each token on its own: 768
  numbers in, 3072 in the middle, 768 out.
- **Norm:** rescales each token's numbers before each block, which keeps
  them in a range the next block handles well.
- **Add the input back:** each block's input is added to its output, so the
  block only learns a correction to what it received. That is what lets deep
  stacks of layers train, the same idea as ResNet.
- The paper says it this way: "Layernorm (LN) is applied before every block,
  and residual connections after every block" (Dosovitskiy et al., 2021).
  ViT-Base stacks 12 such layers.

**In a sentence:** one layer is one reading. "bank" takes in "boat"
(attention), then is processed alone: water, so a river bank (MLP). Adding the
input back keeps the last reading and only adds corrections. The next reading
starts from that. ViT-Base reads 12 times.


6. Static and Contextual Embeddings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Back to the word "bank". In "The boat reached the bank" and in "The bank
raised its rates" it is the same word, but it means two different things. A
**static** embedding gives "bank" one vector, whatever the sentence. A
**contextual** embedding gives it a different vector in each sentence,
because it also looks at the words around it.

Images work the same way. A patch of blue paint could be the side of a bus or
a piece of sky. On its own, the patch cannot tell. Its neighbors can.

The embedding of part 2 is **static**: a patch's vector depends only on its
own pixels and its place, never on the rest of the image.

.. admonition:: Definition: contextual embedding
   :class: note

   A token's vector after the encoder layers: it describes its patch
   together with what surrounds it, because attention mixed in the other
   tokens.

.. figure:: /_static/images/L4/vit_context.png
   :alt: Left: our image, and a CARLA frame of a city street with cars, both squeezed to 224 by 224, with the same orange-outlined patch from our image pasted at the same place in both. Right: a line chart of how alike the patch's two vectors are, from 1, the same, down to 0, against the layer: 0 before the encoder, then 1 to 12 after each encoder layer. It starts at 1, labeled the same vector: static, stays near 1 after layer 1, and falls steadily to about 0.3 after layer 12, labeled very different after 12 layers: contextual.
   :width: 100%
   :align: center

   The same :math:`16 \times 16` pixels in two scenes, measured with
   torchvision's ViT-B/16. **Left:** our orange patch, and the same patch
   pasted at the same place into a CARLA frame. **Right:** how alike the
   patch's two vectors are (1 means the same), before the encoder (0) and
   after each of the 12 layers.

Before the encoder, the two vectors are exactly the same: 1. After each layer
they drift apart, and after 12 layers the measure is about 0.3. The pixels did
not change; the context did.

**In a sentence:** "bank" in "The boat reached the bank" and in "The bank
raised its rates": one static vector, two contextual ones.


7. Head: from Tokens to a Class, the Whole ViT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Part 7, the head, and with it the whole Vision Transformer on our image.

.. figure:: /_static/images/L4/vit_tokens.png
   :alt: Four drawn panels of ViT-Base, numbered by the parts of the architecture figure. 3. Class token + 4. position: a green matrix of 197 by D with its top row in orange, labeled class token, plus a purple matrix E_pos, 197 by D; both learned, D = 768. 6. Encoder: 12 layers: a stack of 12 layers, each drawn as tokens on the left linked to every token on the right, with the class token in orange at the top; every token attends to every token, 197 x D in, 197 x D out. 7. Keep the class token: an orange bar, the class token, 1 x D. 7. Head: the 1 x D bar times a D x 1000 matrix gives a 1 x 1000 strip of class scores.
   :width: 100%
   :align: center

   ViT-Base as matrices, numbered by the parts of the architecture figure.
   **3 and 4:** the class token row (orange) in front of the 196 rows, plus
   a learned position matrix, both :math:`197 \times D`, :math:`D = 768`.
   **6:** 12 encoder layers, every token attending to every token.
   **7:** keep the class token's row, :math:`1 \times D`, and multiply it by
   a :math:`D \times 1000` matrix: 1000 class scores.

- **Parts 3 and 4.** Put one more learned row in front, the class token: 197
  rows. Add a learned position vector to every row, so each token knows where
  its patch came from; attention alone would not know.
- **Part 6.** Twelve encoder layers. In each one, every token attends to
  every other token, then a small network processes each token.
  :math:`197 \times D` in, :math:`197 \times D` out.
- **Part 7.** Keep only the class token's row. Through attention it has
  gathered information from all 196 patches. The head multiplies it by a
  :math:`D \times 1000` matrix: one score per ImageNet class.

The paper's own claim: "a pure transformer applied directly to sequences of
image patches can perform very well on image classification tasks"
(Dosovitskiy et al., 2021). No convolutions. ViTs are now common backbones;
the DINOv2 backbone inside RF-DETR is one.

**In a sentence:** put a blank CLS in front: "CLS The boat reached the bank".
CLS means nothing on its own, reads along with the others through all 12
readings, and ends up holding the gist, a boat arriving at a river. The head
reads one label from it, say the topic: travel.


The Cost of Attention: N² Pairs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Attention scores every token against every token, and that has a cost:
:math:`N` tokens make :math:`N^2` pairs.

.. list-table::
   :widths: 56 18 26
   :header-rows: 1
   :class: compact-table

   * - **Tokens**
     - :math:`N`
     - **Pairs** :math:`N^2`
   * - :math:`224 \times 224` image, :math:`16 \times 16` patches
     - 196
     - 38,416
   * - our image at :math:`480 \times 640`, stride 32
     - 300
     - 90,000
   * - our image at :math:`480 \times 640`, stride 16
     - 1200
     - **1,440,000**

That is for every layer and every image.

.. admonition:: Halve the patch size and the pairs grow 16 times
   :class: tip

   Half the patch size gives four times the tokens, and the pairs grow with
   the square: :math:`4^2 = 16`. That is the problem every detection
   transformer has had to solve. The two common answers: attend only over the
   coarse map, or let each query look at just a **few chosen points** instead
   of everything. Both come back in the Decoder subsection.


.. _l4-lec-decoder:

Decoder
~~~~~~~

- **Where we are:** the encoder gives every token the context of the whole
  image.
- **In this subsection:** the **decoder**, as DETR uses it: the **second
  way** to get boxes. A fixed set of **object queries** read the encoder's
  output, each answering for one object or for none, with no NMS.
- **What it is for:** RT-DETR, our second model.

Instead of a box at every grid cell and a clean-up step, the decoder keeps a
fixed set of object queries, 100 in the original paper. Each query is a
vector, and like every weight, training sets it. Each one takes in the whole
image with attention and gives one answer: one object, or no object.

.. admonition:: Definition: DETR (DEtection TRansformer)
   :class: note

   A detector that predicts a **set**: :math:`N` **object queries** give
   :math:`N` answers, each a class and a box, or "no object"
   (:math:`\varnothing`, the empty-set sign) (Carion et al., 2020). In DETR
   each query is a vector **learned in training**; :math:`N = 100`. RT-DETR
   has no :math:`\varnothing` class: a query whose scores are all low found
   nothing.

**In a sentence:** the decoder writes the answer, one blank per possible
object, while looking back at what the encoder read.


Our Image through RT-DETR-L, Step by Step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L4/rtdetr_flow.png
   :alt: Nine boxes in two rows, with the size measured after each step of RT-DETR-L on our image. Top row, left to right: 1 Image, 640 by 640 by 3; 2 Backbone, CNN, stride 32, 20 by 20 by 2048; 3 Shrink depth, 1 by 1 conv, 20 by 20 by 256; 4 Tokens, 20 by 20 cells, 400 by 256; 5 Encoder, 1 layer, 8 heads, 400 by 256, highlighted green. Bottom row, right to left: 6 Mix 3 sizes, convolutions, 8400 by 256; 7 Queries, top 300 cells, 300 by 256; 8 Decoder, 6 layers, 300 by 256, highlighted green; 9 Heads, box plus 80 scores, 300 by 84. A green arrow runs from step 6 to step 8, labeled encoder output: every decoder layer reads it (cross-attention). A note reads measured, our image.
   :width: 100%
   :align: center

   RT-DETR-L on our image, with the size measured after each step. The two
   transformer parts, the **encoder** (5) and the **decoder** (8), are
   highlighted. The **green arrow** is the encoder output, which every
   decoder layer reads by cross-attention.

1. **Image**, resized to :math:`640 \times 640`.
2. **Backbone:** a CNN gives a :math:`20 \times 20` map with 2048 channels at
   stride 32.
3. **Shrink depth:** a :math:`1 \times 1` convolution shrinks the depth to
   256.
4. **Tokens:** the 400 cells become 400 tokens of 256 numbers, with a
   position encoding added.
5. **Encoder:** one encoder layer, attention with 8 heads, over the 400
   tokens. After it, every cell has taken in the whole image.
6. **Mix 3 sizes:** convolutions mix this map with the stride-8 and
   stride-16 maps: :math:`6400 + 1600 + 400 = 8400` cells of 256 numbers.
   This is the **encoder output**.
7. **Queries:** RT-DETR starts its 300 queries at the 300 cells that score
   highest as objects. DETR used 100 learned vectors instead.
8. **Decoder:** six decoder layers. In each, the queries attend to each
   other, then read the encoder output again (green) at
   :math:`8 \times 3 \times 4 = 96` points per query (8 heads times 3 sizes
   times 4 points), not all 8400.
9. **Heads:** two small heads give each query a box and 80 scores:
   :math:`300 \times 84`.

The encoder output is used twice: its 300 best-scoring cells start the queries
(step 7), and every decoder layer reads it again (step 8).

**Compared with the 2017 decoder** in :ref:`l4-lec-encdec`: same shape, four
changes. The input is the queries, not the text so far. Self-attention has no
mask, because all 300 answers are written at once. Cross-attention reads 96
points. And there are six layers.

How does each query learn which object is its own? That is the next part.

**In a sentence:** the decoder fills blanks, "object 1: ?", "object 2: ?", and
so on, 300 at once, each reading the encoded image the way the French reads
the English.


Matching Queries to Objects: the Hungarian Algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RT-DETR makes 300 guesses, called queries, and our image has 5 objects. To
learn, the network has to know which guess should have found which object.
So in training, each object is paired with exactly **one** query, which
learns to find it.

Chosen for this example: 4 queries and 2 objects, a person and the bus. Each
cell is a **cost**: how bad that query is as an answer for that object. Low
means it gives the right class and puts its box in the right place.

.. list-table::
   :widths: 34 33 33
   :header-rows: 1
   :class: compact-table

   * - **Cost**
     - **person**
     - **bus**
   * - query 1
     - 0.2
     - **0.3** (best pairing)
   * - query 2
     - **0.3** (best pairing)
     - 0.9
   * - query 3
     - 0.8
     - 0.8
   * - query 4
     - 0.9
     - 0.7

- **Cheapest pair first:** query 1 takes the person (0.2), so the bus needs
  another query; the cheapest left is query 4 (0.7). Total
  :math:`0.2 + 0.7 = \mathbf{0.9}`.
- **Best:** query 2 takes the person, query 1 the bus. Total
  :math:`0.3 + 0.3 = \mathbf{0.6}`. Taking the cheapest pair first used up
  query 1, which the bus needed.
- The **Hungarian algorithm**, from 1955, always finds the best total. You do
  not need its steps: in Python it is one call to SciPy's
  ``linear_sum_assignment``.
- Queries 3 and 4 get no object, so training teaches them to say "no object"
  (:math:`\varnothing`).

Next week the same algorithm pairs detections with tracks.

**In a sentence:** the answer key says "boat bank", a student wrote "bank boat
bank", and word order does not matter. Match each key word to one written
word. The extra "bank" matches nothing: it should have been left blank.


Why DETR Needs No NMS
^^^^^^^^^^^^^^^^^^^^^

That one-to-one matching is why DETR needs no NMS.

.. admonition:: One object, one query
   :class: tip

   The matching gives each object to exactly one query during training. A
   second query that also points at the person is paired with nothing, so
   training pushes it to answer :math:`\varnothing`. Duplicates are **trained
   away** instead of cleaned up afterwards.

.. admonition:: And the queries talk to each other
   :class: tip

   Inside the decoder, the queries also attend to each other
   (self-attention). So one query can see that another has already taken the
   person, and look for something else.

Remember NMS's weakness with crowds, two real people standing close. DETR does
not have that threshold to get wrong.

**In a sentence:** two blanks both start to write "bank"; they read each
other, so one stays blank. No word is written twice.


RT-DETR-L's Output: One 300 x 84 Matrix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RT-DETR's whole answer is one matrix: one row per query, **300 rows**, and
**84 columns**. Measured on our image:

.. math::

   \begin{array}{r|cccc|cccc}
    & c_x & c_y & w & h & \text{person} & \text{bicycle} & \cdots & \text{toothbrush} \\ \hline
   \text{query 1} & 0.913 & 0.589 & 0.174 & 0.448 & 0.949 & \cdot & \cdots & \cdot \\
   \text{query 2} & \cdot & \cdot & \cdot & \cdot & \cdot & \cdot & \cdots & \cdot \\
   \vdots & & & & & & & & \\
   \text{query 300} & \cdot & \cdot & \cdot & \cdot & \cdot & \cdot & \cdots & \cdot
   \end{array}

1. **The box**, in the first four columns: center :math:`(c_x, c_y)` and size
   :math:`(w, h)`, as fractions of the image. The first query's box is
   centered 0.913 of the way across: :math:`0.913 \times 810 = 739.5` pixels
   from the left, the person at the right edge, with a person score of 0.949.
   The other 80 columns are sigmoid scores, one per class.
2. **No "no object" column.** Unlike the original DETR, a query that found
   nothing simply has all 80 scores low.
3. **Keep the rows whose best score is above 0.25: 9.** That is the end:
   **no NMS**, because training already made each object belong to one
   query. Compare YOLOv8s: :math:`84 \times 6300`, 49 above the cut, and NMS
   to get down to 5.


From DETR to RT-DETR: Making It Fast
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DETR is clean, yet it did not replace YOLO right away: it was slow to train.

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Model**
     - **What changed**
   * - **DETR** (2020)
     - 42.0 mAP on COCO, the same as Faster R-CNN with the same backbone, but
       after **500 training epochs** (passes over the data) (Carion et al.)
   * - **Deformable DETR**
     - each query attends to a **few sampling points** near where it looks,
       not every cell: 10 times fewer epochs (Zhu et al., 2021)
   * - **RT-DETR** (2024)
     - attention only inside the coarsest map, convolutions to mix the three
       sizes; RT-DETR-L **53.0 mAP at 114 FPS** on a T4 (Zhao et al.;
       Ultralytics)
   * - **RF-DETR** (2026)
     - a DINOv2 backbone (a foundation ViT); the first real-time detector
       above 60 mAP: 60.1 at 17.2 ms on a T4 (Robinson et al.)

- **DETR.** Faster R-CNN was the standard detector of the time, in two
  stages: first propose regions that may hold an object, then classify each
  one. DETR matched it, but needed 500 passes over the training data. The
  cost from part 5 hurt it: attention over every cell of the feature map,
  :math:`N^2` pairs.
- **Deformable DETR** fixed the attention: each query looks at a few sampling
  points near where it is looking, not at every cell. Its paper reports ten
  times fewer training epochs than DETR.
- **RT-DETR**, from 2024, made it real time. Its encoder runs attention only
  inside the coarsest map, stride 32, where there are few cells, and mixes
  the three map sizes with convolutions. RT-DETR-L scores 53.0 mAP at 114
  frames per second on an NVIDIA T4 with **TensorRT**, NVIDIA's speed-up
  library: :math:`1000 / 114 = 8.8` ms per image. That is our second model.
- **RF-DETR**, from Roboflow, published at ICLR 2026, puts a DINOv2 backbone,
  one of the foundation ViTs from :ref:`l4-lec-pretrained`, inside a
  real-time DETR. Its largest version is the first real-time detector above
  60 mAP on COCO: 60.1, at 17.2 ms per image on a T4 with TensorRT at half
  precision.

Transformers now lead on accuracy at real-time speed.


.. _l4-lec-compare:

YOLOv8s and RT-DETR-L on Our Image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We have two models, so here they are side by side on our image.

.. figure:: /_static/images/L4/det_compare.png
   :alt: Our image twice. Left, titled YOLOv8s: 5 objects: the bus at 0.92 and four people at 0.89, 0.88, 0.89 and 0.61. Right, titled RT-DETR-L: 9 objects: the bus at 0.96, four people at 0.95, 0.93, 0.95 and 0.86, and four extras in green: a traffic light at 0.28 on a sign board on the wall, a fire hydrant at 0.34 on a bollard, and two ties at 0.27 and 0.26 on the men's shirts.
   :width: 90%
   :align: center

   **Left, YOLOv8s:** 5 objects, the bus and four people. **Right,
   RT-DETR-L:** the same five, all more confident, plus four wrong objects in
   green, all just above the 0.25 cut: a traffic light on a sign board, a
   fire hydrant on a bollard, and two ties on the men's shirts.

.. list-table::
   :widths: 40 30 30
   :header-rows: 1
   :class: compact-table

   * -
     - **YOLOv8s**
     - **RT-DETR-L**
   * - objects
     - 5
     - 9
   * - lowest person
     - 0.61
     - 0.86
   * - time (RTX 4060)
     - **9.1 ms**
     - **29.9 ms**
   * - COCO mAP
     - 44.9
     - 53.0
   * - weights
     - 11.2 M
     - 33.0 M

Time: RTX 4060 Laptop, PyTorch, 640 input, median of 50 runs, image file in to
boxes out. mAP:
`Ultralytics <https://docs.ultralytics.com/models/rtdetr/>`__.

- **Confidence.** The person cut off at the left edge gets only 0.61 from
  YOLOv8s and 0.86 from RT-DETR-L. RT-DETR gives the people higher
  confidence, and also reports four **wrong** objects above the 0.25 cut.
- **Time.** 9.1 ms for YOLOv8s, 29.9 ms for RT-DETR-L, about three times
  slower. That is not the 8.8 ms of the last table, which was a T4 GPU with
  TensorRT's optimizations; ours is plain PyTorch on a laptop GPU.
- **Accuracy and size.** On COCO, RT-DETR-L is much more accurate, 53.0
  against 44.9, and much bigger: 33.0 million weights against 11.2 million.

.. warning::

   **Not a size match.** Do not read this as "transformers are more accurate
   and slower". Part of both gaps is size: a small model against a large one.
   Ultralytics lists YOLOv8m, 25.9 million weights, at 50.2, and YOLOv8l,
   43.7 million weights, at 52.9, almost level with RT-DETR-L. When you
   compare two detectors, say whether their sizes match.

This is the comparison in one place: accuracy against time, and the failure
cases you only see by looking at the images.


Choosing a Detector for Your AV
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We now have both families side by side: a one-stage CNN that reads close by,
and a transformer that reads the whole image. Which one goes on your AV?
There is no single answer, but there are good questions to ask.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Question on your AV**
     - **Leans toward**
   * - Tight time budget, small GPU, many cameras?
     - a small one-stage model (YOLO26n: 1.7 ms on a T4 GPU), exported to
       TensorRT
   * - Crowds, where NMS deletes real neighbors?
     - NMS-free: RT-DETR, RF-DETR, YOLO26
   * - Best accuracy at real-time speed?
     - a DETR whose backbone was pretrained on a huge image set (RF-DETR)
   * - Positions in meters, with a LiDAR?
     - a 3D detector: PointPillars, CenterPoint (L5)
   * - Classes not in any dataset?
     - fine-tune on your data; open vocabulary offline

- **The time budget** is how long the detector may take on one frame. A
  camera at 20 Hz sends a new frame every 50 ms, and the detector shares
  that time with tracking and planning. The budget is tight on a small GPU,
  or when several cameras share one GPU: with six cameras, for example, each
  frame gets :math:`50 / 6`, about 8 ms. Then pick a small one-stage model,
  exported to TensorRT: Ultralytics reports 1.7 ms for YOLO26 nano on a T4.
- **Crowds:** an NMS-free model avoids deleting a real person standing next
  to another.
- **Best accuracy in real time:** today that is a DETR with a foundation
  backbone, like RF-DETR.
- **Classes in no public dataset:** fine-tune on your own data, and use
  open-vocabulary models offline to find and label the rare ones (see
  :ref:`l4-lec-outside-80`).

**Then measure on your own data:** mAP, latency and the failure cases, on
images from where your AV drives.


.. _l4-lec-road:

Detection on the Road
---------------------

- **Where we are:** two detectors, YOLO and RT-DETR, and a grade (mAP) to
  compare them. But a benchmark score only says how a detector does on the
  benchmark's images.
- **In this section:** what decides how a detector does **on an AV**: the
  confidence cut, the training data, the time per frame, the weather.
- **What it is for:** choosing and testing a detector for a real AV: a
  confidence cut, data from where it drives, a time budget, bad weather.

Two new words come first: latency and domain gap.


.. _l4-lec-latency:

Latency: from a Frame to Its Boxes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: latency
   :class: note

   The time from a camera frame arriving to its boxes coming out of the
   detector.

On an AV, latency is a hard budget, so it pays to know where the time goes.
Ultralytics splits one call into three steps and reports each
(``result.speed``):

1. **Preprocess:** resize the frame so the long side is 640, and scale each
   pixel to 0 to 1.
2. **Network:** the backbone, neck and head.
3. **Postprocess:** turn the raw output into boxes; for YOLO, run NMS.

Measured on the same laptop, **on battery**, median of 50 runs:

.. list-table::
   :widths: 24 19 19 19 19
   :header-rows: 1
   :class: compact-table

   * - **Model**
     - **Step 1**
     - **Step 2**
     - **Step 3**
     - **Whole call**
   * - YOLOv8s
     - 1.8 ms
     - 4.8 ms
     - 2.0 ms
     - 13.3 ms
   * - RT-DETR-L
     - 2.4 ms
     - 34.4 ms
     - 0.5 ms
     - 42.0 ms

- **Where the time goes.** YOLOv8s spends 4.8 ms in the network and 2.0 in
  postprocess, which is mostly NMS. RT-DETR-L spends 34.4 ms in the network
  but only 0.5 in postprocess, because it has no NMS.
- **The whole call is longer than the three steps added up.** YOLOv8s's
  steps are :math:`1.8 + 4.8 + 2.0 = 8.6` ms, against 13.3 ms for the whole
  call; RT-DETR-L's are 37.3 ms against 42.0 ms. Reading the image file and
  Python's own overhead take the rest.
- **Power changes latency.** Plugged in, the whole call was 9.1 and 29.9 ms.
  On battery, the same models on the same hardware are 40 to 46 percent
  slower: :math:`13.3 / 9.1 = 1.46` and :math:`42.0 / 29.9 = 1.40`. An AV's
  computer has the same issue with heat and power, so measure latency in the
  conditions you will drive in.


.. _l4-lec-domain-gap:

Domain Gap: Training Images against Road Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: domain gap
   :class: note

   The difference between the images a model was trained on and the images
   it sees in use. The larger the gap, the worse the model does, even when it
   scored well on its own test set.

A model can score well on its own test set and still do badly on the road,
because that test set came from the same kind of images as its training set.
A model trained on COCO photos and run on CARLA frames has exactly this
problem. On an AV the gap comes from many places:

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Gap**
     - **On an AV**
   * - simulation to real
     - trained on CARLA, driven on a real street, or the reverse
   * - everyday images to roads
     - COCO's kitchens and parks against an AV's camera
   * - weather and light
     - trained in sunshine, driven at night or in fog
   * - place
     - other countries' signs, lane markings, vehicles
   * - sensor
     - a new camera: lens, resolution, mounting height

CARLA's rendered cars are not real cars, and another lens, a different
resolution, or a camera mounted higher changes every image.

- **How you see it:** mAP on your own data falls below the published mAP.
- **How you shrink it:** fine-tune on data from where you drive.


.. _l4-lec-confidence-cut:

Choosing the Confidence Cut
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every detector reports a confidence, and on an AV you have to choose where to
cut. A low cut reports more objects, wrong ones included. A high cut reports
fewer and can miss a real one. Here are the objects reported on our image, by
both models, at four cuts (measured). Our image has five real objects: the
bus and four people.

.. list-table::
   :widths: 20 35 45
   :header-rows: 1
   :class: compact-table

   * - **Cut**
     - **YOLOv8s**
     - **RT-DETR-L**
   * - 0.10
     - 7: a second bus, a tie
     - **41**: 14 potted plants, 8 handbags, ...
   * - 0.25 (default)
     - 5
     - 9: a hydrant, a light, 2 ties
   * - 0.50
     - 5
     - 5
   * - 0.75
     - 4: **misses a person**
     - 5

- **At 0.10**, YOLOv8s reports seven: a second bus box and a tie. RT-DETR-L
  reports 41, including 14 potted plants and 8 handbags.
- **At 0.25**, the default, YOLOv8s gets the five; RT-DETR-L gets nine: the
  five, plus a hydrant, a traffic light and two ties.
- **At 0.50**, both get exactly the five.
- **At 0.75**, RT-DETR-L still has all five, but YOLOv8s loses the cut-off
  person, who scored only 0.61.

.. admonition:: Choose the cut per model
   :class: tip

   The same cut means different things for different models. RT-DETR-L's
   four wrong boxes are gone by 0.50, and its five real objects are still
   there at 0.75; YOLOv8s loses a real person at 0.75. Choose the cut **per
   model**, on **validation data**, labeled images kept out of training. For
   an AV, lean low: a missed person costs far more than a phantom handbag,
   which the tracker can throw away later.


A COCO Model on a CARLA Frame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A model knows only the kind of images it trained on. Here is what a model
trained on COCO sees in a CARLA camera frame, measured with both models.

.. figure:: /_static/images/L4/carla_compare.png
   :alt: The same CARLA camera frame twice: a wide, empty, gray street under an overcast sky, with a sidewalk on the right lined with flower planters and lampposts, and buildings on both sides. Left, titled YOLOv8s: car, potted plant: two blue boxes on distant parked cars down the road and two on planters. Right, titled RT-DETR-L: car, potted plant: green boxes, small ones far down the road and many along the planters on the right, one on the base of a lamppost.
   :width: 100%
   :align: center

   Both COCO models on a CARLA camera frame. **Left, YOLOv8s:** 2 cars, at
   0.50 and 0.51, and 2 potted plants. **Right, RT-DETR-L:** 1 car, at 0.38,
   and **10 potted plants**, one of them the base of a lamppost.

YOLOv8s finds the two parked cars far down the road, but only at 0.50 and
0.51, and calls two flower planters potted plants. RT-DETR-L is worse here:
one car at 0.38, and ten potted plants.

**Why?** COCO is everyday images: kitchens, living rooms, streets. Potted
plants are common there, and CARLA's rendered cars look different from real
ones. This is the domain gap.

**And the classes may not even match.** Say your AV needs five classes:
vehicle, pedestrian, cyclist, traffic light and stop sign. COCO has no
"cyclist", only a person and a bicycle, and you do not need most of its 80
classes. Both reasons are why you collect your own data and fine-tune.


.. _l4-lec-outside-80:

Objects outside the 80 Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remember the exit sign from :ref:`l4-lec-introduction`. A detector trained on
COCO knows 80 classes, fixed when it was trained. An emergency exit sign is
not one of them, and neither is fallen cargo, such as a mattress on the
highway. There are two ways out:

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Approach**
     - **How**
   * - **Fine-tune**
     - label your own images, train the head on your classes
   * - **Open vocabulary**
     - the class is **text you type** at run time. Grounding DINO (2023):
       52.5 mAP on COCO without training on COCO (Liu et al.). SAM 3 (2025):
       a phrase in, every matching object out (Carion et al.)

- **Grounding DINO** takes category names or phrases.
- **SAM 3** takes a short phrase and returns every matching object, outlined
  pixel by pixel. That outline, a mask, is next lecture.

**Why not put them on the AV?** Speed. The RF-DETR paper reports that RF-DETR
runs 20 times as fast as Grounding DINO Tiny, and scores 1.2 AP more on a
benchmark made of 100 real-world datasets (Robinson et al., 2026). So today
open-vocabulary models mostly work offline: labeling data, and searching
recorded drives for the rare objects, the **long tail**, that a fixed class
list misses.


.. _l4-lec-budget:

The Time Budget: 50 ms per Frame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An AV's camera does not wait for the detector, so the detector gets a fixed
amount of time per frame. If it takes longer, frames queue up, and the AV
reacts to old images.

1. **The camera.** The GP1 camera runs at **20 Hz** (``sensor_tick`` 0.05
   s): a new frame every :math:`1000 / 20 = 50` ms.
2. **The detector must finish before the next frame**, and share that time
   with tracking, prediction and planning on the same computer.
3. **Measured on our image** (RTX 4060 laptop, plugged in, PyTorch, median of
   50 runs after 10 warm-up runs): YOLOv8s **9.1 ms**, RT-DETR-L **29.9 ms**.
   That is the whole call, image file in, boxes out: load, resize, network
   and, for YOLOv8s, NMS, one image at a time. On battery it was 13.3 and
   42.0 ms (see :ref:`l4-lec-latency`).

When you report a latency, say the same things, or nobody can compare your
number with anyone else's.

.. admonition:: Both fit, but not with much room
   :class: tip

   Both models fit in 50 ms on this GPU, but RT-DETR-L takes
   :math:`29.9 / 50 = 60` percent of the budget by itself. On a real AV you
   usually export the model to **TensorRT**, NVIDIA's inference engine,
   often in **half precision** (16-bit numbers instead of 32-bit), and times
   drop a lot: `Ultralytics <https://docs.ultralytics.com/models/rtdetr/>`__
   quotes RT-DETR-L at 114 frames per second on an NVIDIA T4 GPU, which is
   :math:`1000 / 114`, about 8.8 ms per frame. Whatever you measure, measure
   it the same way for both models.

.. tip::

   The appendix compares the YOLO model sizes (:doc:`l4_appendix`, "YOLO
   sizes").


Rain, Night and Fog
~~~~~~~~~~~~~~~~~~~

Weather changes the image before the detector ever sees it.

.. list-table::
   :widths: 18 42 40
   :header-rows: 1
   :class: compact-table

   * - **Condition**
     - **What changes in the image**
     - **What to look for**
   * - **Rain**
     - drops on the lens, reflections on the road
     - phantom objects in reflections
   * - **Night**
     - low contrast, headlight glare
     - missed pedestrians in dark clothes
   * - **Fog**
     - far objects fade
     - recall drops with distance

.. admonition:: Test in four conditions
   :class: tip

   Test a detector in **clear, rain, night and fog**. Report mAP **per
   condition**: an average over all four can hide a detector that fails
   completely at night. And show images of the failures, not just the
   numbers: a few annotated failure cases say more than a table.


.. _l4-lec-demo:

Live Demo
---------

YOLOv8s and RT-DETR-L on the same CARLA frame, side by side, instead of our
street image.

.. code-block:: bash

   cd enpm818z-fall-2026-carla-python/lecture4
   python3 compare_detectors.py frame.png    # or a folder of frames

The script is in the ``lecture4`` folder of the course Python repository:
give it one frame or a folder of frames. It loads YOLOv8s and RT-DETR-L, runs
both on the same frame, draws the boxes side by side, and prints, for each
class, how many objects each model found and their mean confidence, then the
median time per frame.

.. admonition:: What to watch
   :class: hint

   Each item maps onto a number from this lecture.

   - **Watch** how many objects each model finds, and at what confidence.
   - **Count** the wrong boxes above 0.25, which lower precision, and the
     people each one misses, which lower recall.
   - **Read** the median time per frame for each model: the latency.


Try Both Approaches Yourself: Two Notebooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The two approaches from this lecture, a one-stage CNN and a set-prediction
transformer, each have a notebook in the ``lecture4`` folder of the course
Python repository. Both run on our street image or on your own CARLA frame.

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Notebook**
     - **You do**
   * - ``yolo_one_stage.ipynb``
     - open the :math:`84 \times 6300` matrix, decode a cell by hand, write
       the confidence cut and NMS, time it
   * - ``rtdetr_set_prediction.ipynb``
     - open the :math:`300 \times 84` matrix, check that no NMS is needed,
       run the Hungarian algorithm, compute attention

- The **YOLO notebook** has you write the confidence cut and NMS yourself,
  and check that you get the same 5 objects as Ultralytics.
- The **RT-DETR notebook** checks that the kept boxes barely overlap, so NMS
  has nothing to do, runs the Hungarian algorithm on the cost table of
  :ref:`l4-lec-decoder`, and computes the wheel's attention.

Every number from the lecture is reproduced there: 49 then 5 boxes, RT-DETR's
9 queries, the man's box :math:`(49.9,\ 401.8)` to :math:`(244.5,\ 901.8)`,
and the attention weights 0.422, 0.422 and 0.157. Each notebook ends with
exercises, and the first one is always the same: run it on a frame from GP1.
