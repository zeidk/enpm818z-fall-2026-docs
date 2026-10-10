====================================================
L4: Perception I, Detecting Objects
====================================================

Overview
--------

**L3 used a camera measurement without asking where it came from. This
lecture builds the step that produces it: the detector.**

In L3, the Kalman filter updated each time the camera matched an exit sign
against the HD map. In the worked example, the sign match put the AV 53.0 m
into the tunnel, with :math:`\sigma = 1` m. But a camera reports pixels, not
"exit sign, 53.0 m". A **detector** finds the objects in an image and draws a
box around each one. It is one part of **perception**, the part of the AV's
software that turns raw sensor data into a description of the world: which
objects are around, where they are, and where the AV may drive. Perception
hands four outputs to the rest of the AV: objects, the drivable area, lanes
and markings, and lights and signs. This lecture covers the first one,
objects.

The whole lecture runs on one image, ``bus.jpg``, the sample image that ships
with the Ultralytics library: 810 x 1080 pixels, a city bus at the curb and
four people. Every box, count and time on the slides was measured on it, on a
laptop GPU (RTX 4060), with two models. **YOLOv8s** is YOLO ("you only look
once"), version 8, size s (small). **RT-DETR-L** is the Real-Time DEtection
TRansformer, size L (large).

The lecture first defines **object detection**: given an image and a fixed
set of classes, output a set of detections, each a class, a confidence and a
box. Detection is classification (what) and localization (where), done for
every object in the image. Then it follows five sections:

- **From Pixels to Features.** The camera hands the AV only numbers, 2,624,400
  of them for our image. An edge filter worked by hand gives a response of
  414.7 at the edge of a letter on the bus and :math:`-9.0` on its flat roof.
  That response is a **feature**. A **CNN** computes many features at every
  place, with weights set by training, and a detector is built from a
  backbone, a neck and a head.
- **Grading a Detector.** **IoU**, true and false positives, **precision**,
  **recall**, **AP** and **mAP**, each worked by hand. This section is a
  measuring tool for the two detectors, not a step they are built from.
- **One-Stage Detectors.** YOLOv8s predicts a box at every one of its 6300
  grid cells in one pass, so it finds each person about ten times. **NMS**
  (non-maximum suppression) keeps one box per object: 49 boxes in, 5 out.
- **Transformers.** **Attention**, computed by hand for three tokens. The
  **encoder**, part by part, through the Vision Transformer (ViT). The
  **decoder** as DETR uses it: a fixed set of object queries, each paired with
  one object by the **Hungarian algorithm**, so no NMS is needed. RT-DETR makes
  this fast enough for real time.
- **Detection on the Road.** What decides how a detector does on an AV: the
  **confidence cut**, the **domain gap** between training images and road
  images, the **latency** against a time budget of 50 ms per frame, and the
  weather.

A live demo then runs both detectors side by side on a CARLA frame.

.. important::

   **This is not an AI lecture.** It is about how an automated vehicle finds
   the objects around it. The networks are tools: the lecture covers what you
   need to read their output, grade it and choose one for an AV, not how to
   invent new ones. The appendix, CNN Fundamentals, has the basics for anyone
   who wants them.

.. note::

   **Not in this lecture.** 3D detection, segmentation, the bird's-eye view
   (BEV), fusion and tracking are :doc:`L5 <../lecture5/l5_index>`,
   "Perception II: 3D Detection, BEV, Fusion & Tracking". 3D detection and
   segmentation moved there from this lecture. They stay on this lecture's
   section strip as dashed gray boxes marked "next lecture".

.. admonition:: This week
   :class: warning

   - **Next week (week 6):** Quiz 2. **GP1 is due, and GP2 is posted, on
     Sunday, October 11.** GP2's two detectors are YOLOv8s and RT-DETR-L,
     which is why every example in this lecture uses them.
   - **Perception is two lectures now:** L4 this week and L5 next week. The
     old third perception lecture was folded into them.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Say what a detector outputs, clean it up with **NMS**, and grade it with
  **IoU**, **precision**, **recall** and **AP**, all by hand.
- Explain how a **one-stage** detector predicts boxes from a grid.
- Compute **attention** for a few tokens.
- Explain how **DETR** matches queries to objects, and why it needs no NMS.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l4_lecture
   l4_appendix
   l4_code
   l4_exercises
   l4_quiz
   l4_references


Next Steps
----------

- In the next lecture we cover **L5: Perception II, 3D Detection, BEV, Fusion
  & Tracking**:

  - **3D Detection:** positions in meters, from LiDAR (PointPillars,
    CenterPoint).
  - **Segmentation:** the shape of things that are not boxes, such as the
    road.
  - **BEV and Occupancy:** the scene seen from above, built from cameras
    (Lift-Splat-Shoot, BEVFormer), and which parts of the ground are taken.
  - **Fusion:** camera and LiDAR together.
  - **Tracking:** following each object over time, with one Kalman filter
    per object.

- **Before next class:**

  - Run ``compare_detectors.py`` from the ``lecture4/`` folder of the course
    Python repository on your own CARLA frames (see :doc:`l4_code`). Count
    the wrong boxes above the 0.25 cut and the people each model misses, and
    read the median time per frame.
  - Work through the two notebooks, ``yolo_one_stage.ipynb`` and
    ``rtdetr_set_prediction.ipynb``. Every number on the slides is
    reproduced there.
  - **Read the** :doc:`appendix <l4_appendix>`, CNN Fundamentals: neurons,
    the convolution arithmetic, stride and padding, activations, pooling,
    training and fine-tuning.
  - Work through the L4 exercises and the quiz.
  - **Quiz 2** is next week. **GP1 is due on Sunday, October 11.**

- **How the lectures connect.** L2 gave the sensors and the camera model. L3
  gave the filter that combines measurements, and took the camera's
  measurement as given. L4 gives the detector that produces it: a box around
  the exit sign, whose size gives its distance through the camera model, and
  a box around every car and person. L5 follows those objects over time.
