====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 3: Perception I -- Object
Detection (YOLO to DETR). Topics include the role of perception in the AV
stack, perception taxonomy, the deep learning revolution, YOLO architecture
and evolution, DETR and transformer-based detection, and the comparison
between CNN-based and transformer-based approaches.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-15)
=================================

.. admonition:: Question 1
   :class: hint

   What is the primary role of perception in the AV stack?

   A. To control the vehicle's steering and throttle.

   B. To transform raw sensor data into a structured, semantic understanding
      of the environment.

   C. To plan the vehicle's trajectory through an intersection.

   D. To calibrate sensors before each drive.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To transform raw sensor data into a structured, semantic
   understanding of the environment.

   Perception bridges sensing (raw data acquisition) and planning (decision-
   making). It converts unstructured sensor data into structured outputs
   like detected objects, lane geometry, and free space.


.. admonition:: Question 2
   :class: hint

   Which perception task assigns a **unique ID and pixel mask** to each
   individual object in the scene?

   A. Semantic segmentation

   B. Object detection

   C. Instance segmentation

   D. Panoptic segmentation

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Instance segmentation

   Instance segmentation gives each object a unique ID and pixel-level mask.
   Semantic segmentation labels all pixels by class (but doesn't distinguish
   individual objects). Panoptic segmentation combines both.


.. admonition:: Question 3
   :class: hint

   What was the key innovation of YOLO v1 (2015) compared to two-stage
   detectors like Faster R-CNN?

   A. It used a transformer encoder.

   B. It framed detection as a single regression problem -- one forward
      pass predicts all bounding boxes and classes.

   C. It used anchor-free detection.

   D. It eliminated the need for training data.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It framed detection as a single regression problem -- one
   forward pass predicts all bounding boxes and classes.

   Two-stage detectors (Faster R-CNN) first propose regions, then classify
   them. YOLO processes the entire image in a single pass, making it
   dramatically faster and enabling real-time detection.


.. admonition:: Question 4
   :class: hint

   In YOLO's backbone-neck-head architecture, what is the role of the
   **neck** (e.g., FPN + PAN)?

   A. Extract features from the raw image.

   B. Fuse features across multiple scales to detect objects of different
      sizes.

   C. Produce the final bounding box predictions.

   D. Apply non-maximum suppression.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Fuse features across multiple scales to detect objects of
   different sizes.

   The neck combines high-resolution features (good for small objects) with
   semantically rich features (good for large objects) through FPN (top-down)
   and PAN (bottom-up) pathways. Output scales: 80x80, 40x40, 20x20.


.. admonition:: Question 5
   :class: hint

   Starting from YOLOv8, what major architectural change was introduced?

   A. Switching from CNN to transformer backbone.

   B. Anchor-free detection with a decoupled head.

   C. Removing the neck entirely.

   D. Using only a single detection scale.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Anchor-free detection with a decoupled head.

   YOLOv8 eliminated predefined anchor boxes, instead directly predicting
   (x,y,w,h) with separate (decoupled) branches for classification and
   localization. This simplifies the architecture and improves flexibility.


.. admonition:: Question 6
   :class: hint

   What does DETR use instead of anchor boxes and NMS?

   A. Region proposals and selective search.

   B. Learned object queries and bipartite matching via the Hungarian
      algorithm.

   C. Grid cells with fixed aspect ratios.

   D. K-means clustering of bounding boxes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Learned object queries and bipartite matching via the Hungarian
   algorithm.

   DETR uses N learned object queries (e.g., 100) that attend to image
   features via cross-attention. During training, the Hungarian algorithm
   finds the optimal one-to-one assignment between predictions and ground
   truth, eliminating duplicate detections without NMS.


.. admonition:: Question 7
   :class: hint

   What is the key advantage of DETR's transformer encoder over a CNN?

   A. It processes images faster than any CNN.

   B. It captures **global context** -- every position attends to all other
      positions via self-attention.

   C. It uses less GPU memory.

   D. It does not require any training data.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It captures global context -- every position attends to all
   other positions via self-attention.

   CNNs have a limited receptive field determined by kernel size and depth.
   Transformers use self-attention to model relationships between all spatial
   positions simultaneously, enabling global reasoning from the first layer.


.. admonition:: Question 8
   :class: hint

   What problem does **Deformable DETR** solve compared to the original
   DETR?

   A. It adds anchor boxes back to the architecture.

   B. It uses deformable attention to attend to sparse key positions,
      achieving 10x faster convergence and better small object detection.

   C. It replaces the transformer with a CNN.

   D. It removes the bipartite matching loss.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It uses deformable attention to attend to sparse key positions,
   achieving 10x faster convergence and better small object detection.

   Original DETR attends to all positions (quadratic cost) and converges
   slowly (500 epochs). Deformable DETR samples a small set of key
   positions around a reference point, dramatically reducing computation
   and improving performance on small objects.


.. admonition:: Question 9
   :class: hint

   What is **mAP@0.5:0.95** and why is it a stricter metric than
   mAP@0.5?

   A. It measures speed at different batch sizes.

   B. It averages precision across IoU thresholds from 0.5 to 0.95,
      requiring tighter bounding box alignment.

   C. It counts only detections with confidence above 0.95.

   D. It measures recall at 50% to 95% thresholds.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It averages precision across IoU thresholds from 0.5 to 0.95,
   requiring tighter bounding box alignment.

   mAP@0.5 only requires 50% overlap between predicted and ground truth
   boxes. mAP@0.5:0.95 averages across thresholds (0.5, 0.55, ..., 0.95),
   penalizing imprecise localization. It is the primary COCO benchmark.


.. admonition:: Question 10
   :class: hint

   Which YOLO loss component penalizes the overlap, center distance, and
   aspect ratio between predicted and ground truth boxes simultaneously?

   A. Binary cross-entropy loss.

   B. Mean squared error loss.

   C. CIoU (Complete Intersection over Union) loss.

   D. Focal loss.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- CIoU (Complete Intersection over Union) loss.

   CIoU combines IoU with penalties for center point distance and aspect
   ratio difference, providing a more informative gradient signal than
   simple IoU or L1/L2 losses for bounding box regression.


.. admonition:: Question 11
   :class: hint

   Why did traditional CV methods (HOG + SVM, SIFT) fail for robust AV
   perception?

   A. They were too computationally expensive.

   B. They required manual feature engineering, were fragile to appearance
      variation, and could not generalize across diverse conditions.

   C. They only worked with LiDAR data.

   D. They achieved higher accuracy than deep learning.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- They required manual feature engineering, were fragile to
   appearance variation, and could not generalize across diverse conditions.

   Hand-crafted features like HOG work in controlled settings but fail under
   varying lighting, weather, viewpoints, and object appearance. Deep
   learning learns features automatically from data, enabling much better
   generalization.


.. admonition:: Question 12
   :class: hint

   What event is widely considered the start of the deep learning
   revolution in computer vision?

   A. The release of OpenCV in 2000.

   B. AlexNet winning the ImageNet competition in 2012.

   C. The invention of the Kalman Filter in 1960.

   D. The first self-driving car demo by DARPA in 2005.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- AlexNet winning the ImageNet competition in 2012.

   AlexNet was the first GPU-trained CNN to win ImageNet by a large margin,
   reducing top-5 error from 26% to 16%. This demonstrated that deep
   convolutional networks could dramatically outperform hand-crafted
   features.


.. admonition:: Question 13
   :class: hint

   In the YOLO dataset format, what do the five values per line represent?

   A. ``<image_id> <x_min> <y_min> <x_max> <y_max>``

   B. ``<class_id> <x_center> <y_center> <width> <height>`` (normalized)

   C. ``<class_name> <confidence> <x> <y> <area>``

   D. ``<class_id> <top_left_x> <top_left_y> <bottom_right_x> <bottom_right_y>``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``<class_id> <x_center> <y_center> <width> <height>`` (normalized)

   YOLO format uses center coordinates and dimensions, all normalized to
   [0, 1] relative to image dimensions. One line per object, one label
   file per image.


.. admonition:: Question 14
   :class: hint

   What does **RT-DETR** achieve that the original DETR could not?

   A. Higher accuracy than any other detector.

   B. Real-time inference speed competitive with YOLO, while maintaining
      the NMS-free transformer architecture.

   C. Training without any labeled data.

   D. Detection of 3D bounding boxes from monocular images.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Real-time inference speed competitive with YOLO, while
   maintaining the NMS-free transformer architecture.

   The original DETR was slow and required 500 epochs to converge. RT-DETR
   uses an efficient hybrid encoder to achieve real-time speed while keeping
   the clean end-to-end design (no anchors, no NMS).


.. admonition:: Question 15
   :class: hint

   At 60 mph (27 m/s), how far does a vehicle travel during 100 ms of
   perception latency?

   A. 0.27 m

   B. 2.7 m

   C. 27 m

   D. 100 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- 2.7 m

   At 27 m/s, the vehicle travels 27 x 0.1 = 2.7 meters during 100 ms.
   This illustrates why perception latency is safety-critical -- every
   millisecond matters for reaction distance.


----


True or False (Questions 16-25)
================================

.. admonition:: Question 16
   :class: hint

   **True or False:** YOLO is a two-stage detector that first proposes
   regions, then classifies them.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   YOLO is a single-stage detector. It predicts all bounding boxes and
   class probabilities in a single forward pass, without a separate region
   proposal step. Two-stage detectors like Faster R-CNN use the region
   proposal approach.


.. admonition:: Question 17
   :class: hint

   **True or False:** DETR requires Non-Maximum Suppression (NMS) as a
   post-processing step.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   DETR eliminates NMS by using bipartite matching (Hungarian algorithm)
   during training, which ensures each prediction corresponds to at most
   one ground truth object. This produces non-duplicate predictions by
   design.


.. admonition:: Question 18
   :class: hint

   **True or False:** Transfer learning means training a model from scratch
   on your target dataset.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Transfer learning means starting with a model pre-trained on a large
   dataset (e.g., COCO, ImageNet) and fine-tuning it on your target
   dataset. This leverages learned features and typically requires less
   data and training time than training from scratch.


.. admonition:: Question 19
   :class: hint

   **True or False:** Semantic segmentation distinguishes between
   individual instances of the same class (e.g., car #1 vs. car #2).

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Semantic segmentation assigns a class label to every pixel but does
   not distinguish individual instances. All car pixels get the same
   "car" label. Instance segmentation is needed to separate individual
   objects of the same class.


.. admonition:: Question 20
   :class: hint

   **True or False:** ResNet's key innovation was residual connections
   (skip connections) that enabled training of much deeper networks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Residual connections allow gradients to flow directly through skip
   paths, solving the vanishing gradient problem in very deep networks.
   This enabled training of 50--152+ layer networks without degradation,
   a breakthrough that underpins most modern CNN architectures.


.. admonition:: Question 21
   :class: hint

   **True or False:** In DETR, object queries are learned parameters that
   each specialize in detecting one object in the scene.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   DETR uses N learned object queries (typically 100) as inputs to the
   transformer decoder. Each query attends to the encoder output via
   cross-attention and specializes in detecting one object (or predicting
   "no object"). They are learned during training.


.. admonition:: Question 22
   :class: hint

   **True or False:** YOLO's FPN (Feature Pyramid Network) neck enables
   detection of objects at multiple scales by fusing features from
   different backbone layers.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   FPN creates a top-down pathway that combines semantically rich
   low-resolution features with high-resolution features via lateral
   connections. This allows the network to detect both large objects
   (at coarse scales) and small objects (at fine scales).


.. admonition:: Question 23
   :class: hint

   **True or False:** Transformers are more data-efficient than CNNs,
   requiring less training data to achieve good performance.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Transformers are generally more data-hungry than CNNs because they lack
   the built-in inductive biases of convolutions (locality, translation
   equivariance). They need larger datasets to learn spatial relationships
   that CNNs capture by design.


.. admonition:: Question 24
   :class: hint

   **True or False:** Precision measures the fraction of real objects that
   the detector successfully found.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Precision measures the fraction of detections that are correct:
   TP / (TP + FP). The metric described (fraction of real objects found)
   is **recall**: TP / (TP + FN).


.. admonition:: Question 25
   :class: hint

   **True or False:** The same ROS 2 node pattern (subscribe to image,
   run inference, publish detections) works for both YOLO and DETR.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The ROS 2 integration pattern is model-agnostic. The node subscribes to
   ``/carla/camera/image``, converts the image, runs inference (regardless
   of whether the model is YOLO or DETR), and publishes a
   ``Detection2DArray`` message.


----


Essay Questions (Questions 26-30)
==================================

.. admonition:: Question 26
   :class: hint

   **Compare YOLO and DETR** across at least four dimensions. In what
   scenarios would you choose one over the other for an AV application?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - YOLO: CNN-based, local context, fast (1-5 ms), requires NMS (except
     v10), mature and production-ready.
   - DETR: Transformer-based, global context, cleaner design (no anchors,
     no NMS), needs more training data, slower (improving with RT-DETR).
   - Choose YOLO for real-time production systems where latency is critical.
   - Choose DETR when global reasoning matters (e.g., detecting heavily
     occluded objects, complex scenes) and compute budget allows it.


.. admonition:: Question 27
   :class: hint

   **Explain how bipartite matching in DETR eliminates the need for NMS.**
   What problem does NMS solve in YOLO, and why doesn't DETR have this
   problem?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - YOLO produces many overlapping predictions for the same object. NMS
     removes duplicates by suppressing lower-confidence boxes that overlap
     with a higher-confidence box.
   - DETR uses the Hungarian algorithm during training to enforce a
     one-to-one assignment between predictions and ground truth objects.
   - Each object query learns to detect at most one object, so duplicate
     predictions do not arise by design.


.. admonition:: Question 28
   :class: hint

   **Explain the YOLO backbone-neck-head architecture.** What does each
   component do, and why is multi-scale feature fusion important for AV
   perception?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Backbone: Extracts hierarchical features from the image (edges ->
     textures -> object parts -> objects).
   - Neck (FPN + PAN): Fuses features across scales so the detector can
     handle objects of different sizes.
   - Head: Produces final bounding box and class predictions.
   - Multi-scale fusion is critical for AV perception because the scene
     contains both large nearby vehicles and small distant pedestrians.


.. admonition:: Question 29
   :class: hint

   **Why did deep learning replace traditional CV methods** (HOG, SIFT,
   etc.) for AV perception? What were the key enablers of this transition?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Traditional methods required hand-crafted features that were fragile
     and couldn't generalize across diverse conditions.
   - Deep learning learns features automatically from data, adapting to
     variation in lighting, weather, viewpoints, and object appearance.
   - Key enablers: large-scale datasets (ImageNet, COCO), GPU acceleration,
     improved training techniques (batch norm, residual connections), and
     transfer learning.


.. admonition:: Question 30
   :class: hint

   **Describe how you would deploy a YOLO-based perception node** in a
   ROS 2 system connected to CARLA. What topics would it subscribe to
   and publish?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The node subscribes to ``/carla/camera/image`` (``sensor_msgs/Image``).
   - In the callback, it converts the ROS image to OpenCV format using
     ``cv_bridge``, runs YOLO inference, and constructs a
     ``Detection2DArray`` message with bounding boxes and class labels.
   - It publishes detections on a topic like ``/perception/detections``.
   - This same pattern works for any detector (YOLO, DETR, etc.) since the
     ROS 2 interface is model-agnostic.
