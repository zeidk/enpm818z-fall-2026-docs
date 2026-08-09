====================================================
Lecture
====================================================


Foundations of Perception
-------------------------

What Is Perception?
~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition
   :class: note

   **Perception** is the process by which an autonomous system transforms
   unstructured, noisy sensor data into a structured, semantic understanding
   of the surrounding environment.

Without perception, an AV cannot distinguish between a pedestrian and a
plastic bag, cannot determine if the road ahead is clear, and cannot make
informed decisions about navigation and safety.

**Perception in the AV stack:**

.. list-table::
   :widths: 15 45 40
   :header-rows: 1
   :class: compact-table

   * - Module
     - Function
     - Key Question
   * - **Sensing**
     - Physical sensors + signal processing
     - "What raw data do we have?"
   * - **Perception**
     - Semantic world representation
     - "What is out there?"
   * - **Planning**
     - Route, behavior, trajectory generation
     - "What should we do?"
   * - **Control**
     - Actuator commands
     - "How do we do it?"

.. important::

   No amount of sophisticated planning or control can compensate for
   perception failures. Perception is the foundation of the entire AV stack.


Perception Inputs and Outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Inputs:**

- Camera images (1920x1200 at 30--60 Hz)
- LiDAR point clouds (100K--1M points at 10--20 Hz)
- RADAR returns (10--20 Hz)
- GNSS/IMU (50--200 Hz)

**Outputs:**

- Detected objects with class labels, 3D bounding boxes, and tracking IDs
- Lane geometry (polynomial/spline boundaries)
- Traffic light states with position and confidence
- Free space (drivable corridor)
- HD map alignment


Taxonomy of Perception Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Mid-Level Understanding

      Extracts semantic meaning from sensor data.

      - **Object detection:** YOLO, Faster R-CNN, PointPillars, CenterPoint
      - **Semantic segmentation:** FCN, U-Net, DeepLabv3+
      - **Instance segmentation:** Mask R-CNN, YOLACT
      - **Panoptic segmentation:** Combines semantic + instance
      - **Lane detection:** SCNN, LaneNet, PolyLaneNet
      - **Traffic sign/light recognition**

   .. tab-item:: High-Level Reasoning

      Interprets the scene over time for decision-making.

      - **Multi-object tracking (MOT):** DeepSORT, ByteTrack
      - **Scene understanding:** Occupancy grids, HD map integration
      - **Behavior/intent prediction:** RNNs, Transformers, GNNs
      - **Anomaly detection**

**Key terminology:**

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **Detection**
     - Locating objects (bounding box + confidence).
   * - **Classification**
     - Assigning a category label to an object.
   * - **Semantic segmentation**
     - All pixels of the same class share a label (e.g., "road").
   * - **Instance segmentation**
     - Each object gets a unique ID + pixel mask.
   * - **Panoptic segmentation**
     - Combines semantic (stuff) + instance (things).
   * - **Tracking**
     - Estimating current/past states from observations over time.
   * - **Prediction**
     - Forecasting future states of other agents.


.. admonition:: Recap from ENPM673
   :class: note

   In ENPM673, you learned the fundamentals of convolutional neural networks:
   convolution and pooling operations, stride and padding, activation functions,
   fully connected layers, and back-propagation. You also studied how CNNs learn
   hierarchical feature representations -- edges in early layers, textures and
   shapes in middle layers, and high-level object templates in deeper layers --
   replacing hand-crafted descriptors such as SIFT and HOG. You explored key
   architectures (AlexNet, VGGNet) and saw why classical computer vision methods,
   while effective in constrained settings, struggle with the appearance variation
   and scale diversity encountered in real-world scenes.

   In this lecture, we apply these foundations to two state-of-the-art object
   detection architectures designed for real-time autonomous driving: **YOLO**
   and **DETR**.


Detection Fundamentals: IoU, NMS, and mAP
------------------------------------------

Three primitives underpin every detector in this lecture. They are worth
pinning down before the architectures, because the architectures are
largely defined by how they handle them.

Intersection over Union (IoU)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**IoU** measures how well two boxes overlap -- the currency of both
training targets and evaluation:

.. math::

   \text{IoU}(A, B) = \frac{|A \cap B|}{|A \cup B|}

It ranges from 0 (disjoint) to 1 (identical). A detection is normally
counted as correct if its IoU with a ground-truth box of the same class
exceeds a threshold, conventionally 0.5.

.. admonition:: Why IoU and not centre distance?
   :class: tip

   IoU is **scale-invariant**: being 10 px off matters enormously for a
   distant pedestrian and barely at all for a nearby truck, and IoU
   captures that automatically. This is also why IoU appears inside the
   loss (as CIoU/GIoU) rather than a plain L2 on box coordinates.

Non-Maximum Suppression (NMS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A CNN detector fires at **many** nearby locations for the same object,
producing a cluster of overlapping boxes. **NMS** is the post-processing
step that keeps one per object:

.. code-block:: text

   Sort all detections by confidence, descending
   While detections remain:
       Take the highest-confidence box B; add it to the output
       Discard every remaining box with IoU(B, box) > nms_threshold
                                       and the same class

Typical ``nms_threshold`` is 0.45--0.7.

.. admonition:: NMS is a real limitation, not just plumbing
   :class: warning

   NMS is a **hand-tuned, non-differentiable heuristic** sitting outside
   the network, and it fails in a specific way: when two objects of the
   same class genuinely overlap -- a pedestrian partially behind another,
   two cars in dense traffic -- NMS deletes the second one as a
   "duplicate." Its runtime also grows with the number of detections,
   which hurts the latency budget in crowded scenes.

   This is precisely what DETR's bipartite matching and YOLOv10's
   NMS-free training are designed to eliminate. When you read "no NMS
   required" later in this lecture, this is the problem being solved.

Mean Average Precision (mAP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For a given class, sweep the confidence threshold from high to low. Each
threshold yields a (precision, recall) pair; plotting them traces the
**precision-recall curve**, and **Average Precision (AP)** is the area
under it. **mAP** averages AP over all classes.

.. list-table::
   :widths: 22 78
   :class: compact-table

   * - **mAP@0.5**
     - AP computed with a single IoU threshold of 0.5. Lenient about
       localization quality. (Also written AP\ :sub:`50`.)
   * - **mAP@0.5:0.95**
     - AP averaged over IoU thresholds 0.5, 0.55, ..., 0.95, then
       averaged over classes. The COCO default, usually written just
       **AP**. Rewards precise localization and is always the lower
       number.

.. important::

   **mAP requires ground-truth labels.** It is a comparison between
   predictions and annotations -- you cannot compute it from predictions
   alone. This matters for the exercises at the end of this lecture: to
   report mAP on CARLA frames you must first export CARLA's ground-truth
   bounding boxes, not merely run the detector.


YOLO: You Only Look Once
--------------------------

YOLO revolutionized real-time object detection by framing detection as a
**single regression problem**: one forward pass predicts all bounding boxes
and class probabilities simultaneously.

YOLO Evolution
~~~~~~~~~~~~~~

.. list-table::
   :widths: 12 15 50 23
   :header-rows: 1
   :class: compact-table

   * - Version
     - Year
     - Key Innovation
     - Reported accuracy
   * - v1
     - 2015
     - Single-stage detection, 7x7 grid
     - 63.4 mAP\ :sub:`50` (VOC 2007)
   * - v2
     - 2017
     - Batch norm, anchor boxes, Darknet-19
     - 78.6 mAP\ :sub:`50` (VOC 2007)
   * - v3
     - 2018
     - FPN multi-scale, Darknet-53, 3 detection scales
     - 57.9 AP\ :sub:`50` / 33.0 AP (COCO)
   * - v4
     - 2020
     - CSPDarknet53, Mosaic augmentation, PAN, CIoU loss
     - 43.5 AP (COCO)
   * - v5
     - 2020
     - PyTorch native, model scaling (n/s/m/l/x), AutoAugment
     - 50.7 AP (COCO, v5x)
   * - v7
     - 2022
     - E-ELAN, SOTA at the time
     - 56.8 AP (COCO, v7-E6E)
   * - v8
     - 2023
     - **Anchor-free**, decoupled head, multi-task (det/seg/pose)
     - 53.9 AP (COCO, v8x)
   * - v10
     - 2024
     - NMS-free training, dual label assignment
     - 54.4 AP (COCO, v10x)
   * - v11
     - 2024
     - C3k2 blocks, SPPF modifications
     - 54.7 AP (COCO, v11x)

.. warning::

   **These numbers are not directly comparable.** Three different
   metrics appear in the column above:

   - **mAP**\ :sub:`50` **on VOC** (v1, v2) -- an easier dataset and a
     single, lenient IoU threshold.
   - **AP**\ :sub:`50` **on COCO** (the 57.9 for v3) -- COCO, but still a
     single IoU threshold.
   - **AP on COCO** (v4 onward) -- the modern default, averaged over IoU
     thresholds 0.50:0.05:0.95, which is far stricter.

   Read naively, the table suggests v3 (57.9) beats v8 (53.9). It does
   not: v3's comparable COCO AP is 33.0. Whenever you see a detection
   number quoted without its dataset *and* its IoU protocol, treat it as
   meaningless.

   Versions v6, v9, v12 and later releases are omitted for brevity; the
   family continues to iterate and the accuracy leader changes
   frequently. Check the current Ultralytics documentation rather than
   this table when choosing a model.


Architecture: Backbone-Neck-Head
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 3 3 3
   :gutter: 3

   .. grid-item-card:: Backbone (Feature Extraction)
      :class-card: sd-border-info

      Extracts hierarchical features from the input image.

      - CSPDarknet53 (v4--v7), C2f blocks (v8+)
      - Progressive downsampling: 640 -> 320 -> ... -> 20
      - Increasing channels: 3 -> 64 -> ... -> 1024
      - Residual connections, SiLU/Mish activation

   .. grid-item-card:: Neck (Multi-Scale Fusion)
      :class-card: sd-border-info

      Fuses features across scales for detecting objects of different sizes.

      - **FPN:** Top-down pathway + lateral connections
      - **PAN:** FPN + bottom-up pathway (v4, v5)
      - Output scales: 80x80 (small), 40x40 (medium), 20x20 (large)

   .. grid-item-card:: Head (Detection)
      :class-card: sd-border-info

      Produces final bounding boxes and class predictions.

      - **Anchor-based (v3--v7):** Predefined boxes, predict offsets
      - **Anchor-free (v8+):** Directly predict (x,y,w,h), decoupled head
      - NMS post-processing (or NMS-free in v10)


Loss Functions
~~~~~~~~~~~~~~

YOLO's training loss combines three components:

1. **Localization (box regression):** CIoU loss -- penalizes overlap, center
   distance, and aspect ratio simultaneously.
2. **Objectness (confidence):** Binary cross-entropy -- is there an object?
3. **Classification:** Binary cross-entropy per class (multi-label).


Training YOLO on Custom Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ultralytics import YOLO

   # Load pretrained model
   model = YOLO('yolov8s.pt')

   # Train on custom dataset
   results = model.train(
       data='data.yaml',    # Dataset config
       epochs=100,
       imgsz=640,
       batch=16,
       name='carla_detector',
       pretrained=True
   )

   # Evaluate
   metrics = model.val(data='data.yaml', split='test')

   # Export for deployment
   model.export(format='onnx')
   model.export(format='engine', half=True)  # TensorRT FP16

**Dataset format (YOLO):**

.. code-block:: text

   # Each label file: one line per object
   <class_id> <x_center> <y_center> <width> <height>
   # All values normalized to [0, 1]

**Dataset structure:**

.. code-block:: text

   dataset/
   ├── images/
   │   ├── train/
   │   ├── val/
   │   └── test/
   ├── labels/
   │   ├── train/
   │   ├── val/
   │   └── test/
   └── data.yaml

**Evaluation metrics:**

- **mAP@0.5** -- Mean Average Precision at IoU threshold 0.5.
- **mAP@0.5:0.95** -- Averaged across IoU thresholds 0.5 to 0.95 (stricter).
- **Precision** -- TP / (TP + FP). How many detections are correct?
- **Recall** -- TP / (TP + FN). How many real objects are found?
- **Inference time** -- Milliseconds per image.


DETR: Detection Transformer
-----------------------------

DETR (DEtection TRansformer) was introduced by Carion et al. (2020) and
represents a fundamentally different approach to object detection: **no
anchors, no NMS, end-to-end set prediction**.

.. admonition:: Key Insight
   :class: tip

   DETR treats object detection as a **set prediction problem**: given an
   image, predict a fixed-size set of objects in a single forward pass,
   using a transformer encoder-decoder architecture.


DETR Architecture
~~~~~~~~~~~~~~~~~

.. grid:: 1 2 2 4
   :gutter: 2

   .. grid-item-card:: 1. CNN Backbone
      :class-card: sd-border-primary

      ResNet-50 extracts a feature map from the input image.
      Output: flattened spatial features + positional encoding.

   .. grid-item-card:: 2. Transformer Encoder
      :class-card: sd-border-primary

      Self-attention over the feature map. Each position attends to
      all other positions -- **global context** from the start.

   .. grid-item-card:: 3. Transformer Decoder
      :class-card: sd-border-primary

      N learned **object queries** (e.g., 100) attend to encoder output
      via cross-attention. Each query specializes in detecting one object.

   .. grid-item-card:: 4. Prediction Heads
      :class-card: sd-border-primary

      Each query outputs a class label + bounding box (or "no object").
      **No NMS needed** -- bipartite matching ensures one prediction per
      object.


Bipartite Matching
~~~~~~~~~~~~~~~~~~

Instead of NMS, DETR uses the **Hungarian algorithm** to find the optimal
one-to-one assignment between predicted objects and ground truth during
training:

- Each prediction is matched to at most one ground truth object.
- Unmatched predictions are assigned the "no object" class.
- The matching cost combines classification loss and box loss (L1 + GIoU).

This eliminates duplicate detections by design.


DETR Variants
~~~~~~~~~~~~~

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Model
     - Key Improvement
     - Impact
   * - **Deformable DETR**
     - Deformable attention (attend to sparse key positions)
     - 10x faster convergence, better small object detection
   * - **DINO**
     - Contrastive denoising + mixed query selection
     - 63+ AP on COCO (SOTA)
   * - **RT-DETR**
     - Real-time DETR with efficient hybrid encoder
     - Competitive with YOLO on speed; no NMS


YOLO vs. DETR Comparison
--------------------------

.. list-table::
   :widths: 25 37 38
   :header-rows: 1
   :class: compact-table

   * - Dimension
     - YOLO (v8+)
     - DETR (RT-DETR)
   * - **Architecture**
     - CNN backbone + FPN neck + detection head
     - CNN backbone + transformer encoder-decoder
   * - **Context**
     - Local (CNN receptive field)
     - Global (self-attention from the start)
   * - **Post-Processing**
     - NMS required (except v10)
     - No NMS -- bipartite matching
   * - **Anchors**
     - Anchor-free (v8+)
     - No anchors (object queries)
   * - **Speed**
     - Very fast (1--5 ms on GPU)
     - Fast with RT-DETR; original DETR is slower
   * - **Small Objects**
     - Good (multi-scale FPN)
     - Improved with Deformable DETR
   * - **Training Data**
     - Efficient with moderate data
     - Needs more data (transformer data hunger)
   * - **Simplicity**
     - More components (anchors, NMS, FPN)
     - Cleaner end-to-end design
   * - **AV Suitability**
     - Production-ready, real-time
     - Emerging; RT-DETR closing the gap

.. tip::

   In **GP2: Perception**, you will fine-tune both YOLO and DETR on the same
   CARLA dataset and compare their performance under different conditions
   (day/night, rain, occlusion).


Deploying a Detector as a ROS 2 Node
--------------------------------------

The practical output of this lecture is a perception node that subscribes to
CARLA camera images and publishes detected objects.

.. code-block:: python

   import rclpy
   from rclpy.node import Node
   from sensor_msgs.msg import Image
   from vision_msgs.msg import Detection2DArray, Detection2D
   from cv_bridge import CvBridge
   from ultralytics import YOLO


   class YoloDetectorNode(Node):
       def __init__(self):
           super().__init__('yolo_detector')
           self.model = YOLO('best.pt')
           self.bridge = CvBridge()

           self.sub = self.create_subscription(
               Image, '/carla/camera/image',
               self.image_callback, 10)

           self.pub = self.create_publisher(
               Detection2DArray, '/perception/detections', 10)

       def image_callback(self, msg):
           # Ultralytics expects BGR for raw numpy input (it matches
           # cv2.imread convention). Converting to 'rgb8' here would swap
           # the red and blue channels and quietly degrade every
           # detection -- no error, just worse results.
           cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
           results = self.model(cv_image, verbose=False)

           det_array = Detection2DArray()
           det_array.header = msg.header

           for r in results[0].boxes:
               det = Detection2D()
               # ... populate bounding box and class ...
               det_array.detections.append(det)

           self.pub.publish(det_array)


   def main():
       rclpy.init()
       node = YoloDetectorNode()
       rclpy.spin(node)
       rclpy.shutdown()

This pattern applies identically to DETR -- swap ``YOLO('best.pt')`` for a
DETR model loaded via ``transformers`` or ``torch.hub``.


Industrial Perception Architectures
--------------------------------------

Understanding how leading AV companies deploy perception systems bridges
the gap between academic algorithms and real-world engineering.


Generic Perception Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most production autonomous vehicles follow a modular perception pipeline:

.. list-table::
   :widths: 20 80
   :class: compact-table

   * - **1. Sensor Layer**
     - Multiple cameras (360-degree coverage), LiDAR, RADAR, GNSS, IMU.
       Continuous data streams at 10--60 Hz.
   * - **2. Preprocessing**
     - Timestamp synchronization, calibration and coordinate frame
       transforms, image undistortion, noise filtering.
   * - **3. Perception Stack**
     - Detection (vehicles, pedestrians, cyclists, traffic signs/lights),
       segmentation (drivable area, lane boundaries), multi-object tracking
       with ID assignment, multi-sensor fusion into a unified world model.
   * - **4. Output**
     - Structured world model: objects with positions, velocities,
       trajectories. Delivered to planning at 10--30 Hz.


Industry Case Studies
~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Waymo

      **Philosophy:** Multi-sensor fusion, LiDAR-centric.

      - **Sensors:** 5 LiDARs, 29 cameras, 6 RADARs, high-precision
        GNSS/IMU (5th-generation Driver; the 6th generation reduces
        sensor count to lower cost).
      - **Approach:** LiDAR is the primary sensor for 3D detection and
        localization. Cameras add semantic richness (signs, lights, lane
        markings). RADAR for velocity and adverse weather.
      - **Architecture:** Modular pipeline (detection -> tracking ->
        prediction). PointPillars-style LiDAR detection + camera fusion.
        HD maps for localization priors.
      - **Scale:** Tens of millions of rider-only miles and 250K+ paid
        rides/week, both growing quickly -- check Waymo's current
        published figures rather than quoting these.
      - **Key trade-off:** Heavy sensor investment for maximum safety.

   .. tab-item:: Tesla

      **Philosophy:** Vision-only, end-to-end learning.

      - **Sensors:** 8 cameras (no LiDAR, no RADAR post-2023).
      - **Approach:** "Humans drive with vision; cars should too." Depth
        is inferred from monocular images and temporal parallax.
      - **Architecture:** HydraNet multi-task backbone processes all 8
        camera streams. BEV representation via spatial transformers.
        Occupancy network predicts 3D occupancy grid. Video module for
        temporal reasoning. FSD v12 is fully end-to-end.
      - **Training:** Auto-labeling pipeline on fleet data, Dojo
        supercomputer, shadow mode for edge case collection.
      - **Key trade-off:** Cost and scalability vs. depth uncertainty and
        weather sensitivity.

   .. tab-item:: Cruise (cautionary case)

      **Philosophy:** Multi-sensor with HD maps, urban robotaxi.

      - **Sensors:** 5 LiDARs, 21 cameras, 5 RADARs, GNSS/IMU.
      - **Approach:** Camera + LiDAR + RADAR fusion. HD maps for
        localization and environmental priors. Continuous Learner system
        for model updates.
      - **Status:** **Defunct.** Operations were suspended in late 2023
        after the pedestrian-dragging incident (see L1), California
        revoked the testing permit, and GM wound the robotaxi programme
        down in December 2024. Cruise appears here as a historical case
        study, not a current competitor.
      - **Key lesson:** Operational safety failures -- and the handling of
        their disclosure -- can end a program regardless of technical
        capability. Cruise's perception stack was competitive; that was
        not enough.

   .. tab-item:: Aurora

      **Philosophy:** Sensor diversity, long-range trucking.

      - **Sensors:** FirstLight LiDAR (400+ m range), imaging RADAR,
        cameras, thermal cameras for night vision.
      - **Approach:** Sensor diversity for robustness across conditions.
        Focus on highway autonomous trucking and logistics.
      - **Architecture:** Virtual Driver System with collaborative
        perception (truck convoys sharing sensor data).

   .. tab-item:: Mobileye

      **Philosophy:** Camera-first with formal safety (RSS).

      - **Sensors:** 8--11 cameras, optional RADAR/LiDAR ("True
        Redundancy" architecture).
      - **Approach:** EyeQ SoC optimized for vision processing. REM
        (Road Experience Management) for crowdsourced HD maps.
      - **RSS (Responsibility-Sensitive Safety):** Formal model defining
        "safe" vs. "unsafe" states mathematically. Guarantees the vehicle
        never causes an accident under RSS rules.
      - **Scale:** Tier-1 supplier to BMW, Nissan, Ford, Geely. Millions
        of vehicles with ADAS deployed.


Architectural Trade-Offs
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 22 39 39
   :header-rows: 1
   :class: compact-table

   * - Dimension
     - Option A
     - Option B
   * - **Sensing**
     - Camera-only (Tesla): Low cost, scalable, semantic-rich. But: depth
       uncertainty, weather sensitivity.
     - Multi-sensor fusion (Waymo): Redundant, accurate 3D, all-weather.
       But: high cost, complex calibration.
   * - **Pipeline**
     - Modular (Waymo, Mobileye): Interpretable, debuggable, swappable
       components. But: error propagation, hand-crafted interfaces.
     - End-to-end (Tesla FSD v12): Joint optimization, fewer rules. But:
       black-box, hard to debug, massive data requirement.
   * - **Mapping**
     - HD maps (Waymo, Cruise): Simplifies localization, provides priors.
       But: expensive to create/maintain, limits ODD.
     - Map-free (Tesla): Scales anywhere, adapts to changes. But: higher
       perception burden, less robust in ambiguous scenarios.
   * - **Processing**
     - Centralized (NVIDIA Drive AGX): Unified view, easier fusion, lower
       latency. But: single point of failure.
     - Distributed (per-sensor nodes): Fault isolation, parallel. But:
       synchronization challenges, network latency.
   * - **Safety**
     - Rule-based (Mobileye RSS): Interpretable, verifiable,
       regulatory-friendly. But: overly conservative.
     - Learned behavior (Tesla): Adapts to diverse scenarios. But:
       black-box, hard to validate.

.. note::

   The industry has not converged on a single winning architecture. Diverse
   approaches reflect different priorities: cost vs. safety, scalability vs.
   redundancy, interpretability vs. flexibility.


Deployment and Integration
----------------------------

Moving perception algorithms from research to production requires careful
attention to real-time constraints, model optimization, and system
integration.


Real-Time Performance Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - Constraint
     - Target
   * - End-to-end perception latency
     - < 100 ms total
   * - Sensor acquisition
     - 10--30 ms
   * - Detection / segmentation
     - 30--50 ms
   * - Tracking and fusion
     - 10--20 ms
   * - World model update rate
     - 10--30 Hz
   * - Camera streams processed
     - 5--10 simultaneously
   * - LiDAR points per frame
     - 100K--1M

.. important::

   At 60 km/h, a vehicle travels 1.67 m in 100 ms. Every millisecond of
   latency translates directly to stopping distance. Real-time performance
   is a safety requirement, not an optimization goal.


Model Optimization for Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Research models are too slow and large for embedded automotive hardware.
Production deployment requires systematic optimization:

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Technique
     - Description
   * - **Quantization**
     - Reduce weight precision from FP32 to INT8 or FP16. Typical speedup:
       2--4x with <1% accuracy loss. Supported by TensorRT, ONNX Runtime.
   * - **Pruning**
     - Remove weights or channels with minimal contribution. Structured
       pruning removes entire filters for hardware-friendly speedup.
   * - **Knowledge Distillation**
     - Train a small "student" model to mimic a large "teacher" model.
       Preserves much of the teacher's accuracy at a fraction of the compute.
   * - **Architecture Search (NAS)**
     - Automatically search for efficient architectures under latency
       constraints. Used by EfficientDet, NAS-FPN.
   * - **TensorRT / ONNX**
     - Framework-specific optimization: operator fusion, memory planning,
       kernel auto-tuning. Can achieve 5--10x speedup over naive PyTorch.

.. code-block:: python

   # Example: Export YOLO to TensorRT for deployment
   from ultralytics import YOLO

   model = YOLO('best.pt')
   model.export(format='engine',       # TensorRT format
                half=True,              # FP16 quantization
                imgsz=640,
                device=0)

   # Load optimized model for inference
   optimized = YOLO('best.engine')
   results = optimized.predict(source='image.jpg')


Hardware Platforms
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 25 50
   :header-rows: 1
   :class: compact-table

   * - Platform
     - TOPS
     - Used By
   * - **NVIDIA Drive AGX Orin**
     - 254 TOPS
     - Waymo, Mercedes-Benz, Volvo. Supports multiple concurrent DNN
       workloads. Dominant in L4 development.
   * - **Tesla FSD Computer (HW4)**
     - ~300 TOPS (est.)
     - Tesla. Custom SoC with dual redundant chips for fail-operational
       safety.
   * - **Mobileye EyeQ6**
     - 176 TOPS
     - BMW, Geely, Ford. Optimized for camera-centric ADAS and L2+.
   * - **Qualcomm Snapdragon Ride**
     - 100--700 TOPS
     - GM, BMW (ADAS). Mobile-derived platform with power efficiency.

.. tip::

   When choosing a model architecture, profile it on the target hardware
   early. A model that runs at 50 FPS on an RTX 4090 may only achieve 5 FPS
   on an embedded automotive SoC.


Software Integration: ROS 2 and Autoware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this course, perception nodes are integrated into the ADS pipeline using
ROS 2. In industry, frameworks like Autoware extend ROS 2 with production-
grade AV components.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Framework
     - Scope
     - Use Case
   * - **ROS 2**
     - General-purpose robotics middleware with DDS communication, QoS
       policies, and lifecycle management.
     - Course projects, research prototypes, component development.
   * - **Autoware**
     - Open-source full-stack AV software built on ROS 2. Includes
       perception (LiDAR detection, camera fusion), planning, and control.
     - Production AV development, industry R&D.
   * - **Apollo (Baidu)**
     - End-to-end AV platform with perception, planning, control, and
       simulation. Custom middleware (Cyber RT).
     - Chinese robotaxi deployments, academic research.

**Detector node integration pattern** (used in GP2):

1. Subscribe to camera images (``/carla/ego/camera/image``).
2. Run inference (YOLO or DETR) on each frame.
3. Publish detections as ROS 2 messages (``/perception/detections``).
4. Downstream nodes (tracker, planner) subscribe and consume.

.. seealso::

   The ROS 2 detector node code from the previous section provides a
   complete implementation of this pattern.


Beyond YOLO and DETR
----------------------

While YOLO and DETR are the focus of this lecture, the AV perception
landscape has evolved further:

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **BEV Perception**
     - Bird's-Eye View representations (BEVFormer, LSS) project camera
       features into a top-down view -- the dominant paradigm in modern AV
       perception. *Covered in L5.*
   * - **3D Occupancy Networks**
     - Predict per-voxel semantic occupancy, handling arbitrary-shaped
       obstacles that bounding boxes miss. *Covered in L5.*
   * - **Multi-Task Learning**
     - Single backbone with multiple heads (detection + segmentation + lane
       detection). Example: Tesla HydraNet.
   * - **3D Object Detection**
     - See the dedicated section below -- for an AV this is the detection
       problem that actually matters.
   * - **End-to-End Perception**
     - UniAD, DriveTransformer unify perception-prediction-planning.
       *Covered in L12.*


3D Object Detection from LiDAR
--------------------------------

Everything above operates on the image plane and returns 2-D boxes. A
planner cannot use a 2-D box: it needs to know **where the object is in
metric space**, how big it is, and which way it is facing. That means 3-D
detection, and in practice that means LiDAR.

The Representation Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A point cloud is **unordered, sparse, and irregular** -- everything a
convolution assumes it is not. The design space is essentially "how do we
make this look enough like a grid to convolve over it?"

.. list-table::
   :widths: 18 40 42
   :header-rows: 1
   :class: compact-table

   * - Approach
     - Idea
     - Trade-off
   * - **Point-based**
     - Operate on raw points with shared MLPs and symmetric pooling
       (PointNet, PointNet++).
     - Exact geometry, no quantization loss; slow and hard to scale to
       full driving scenes.
   * - **Voxel-based**
     - Quantize into a 3-D grid, encode each voxel, then use 3-D sparse
       convolution (VoxelNet, SECOND).
     - Accurate; sparse convolution needed to stay tractable.
   * - **Pillar-based**
     - Voxelize in x-y **only** -- infinitely tall "pillars" -- giving a
       2-D pseudo-image for a standard 2-D CNN (PointPillars).
     - Very fast, the usual production choice; loses fine vertical
       structure.

Key Architectures
~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: PointPillars (2019)

      The workhorse. Points are grouped into vertical pillars on a BEV
      grid, each pillar is encoded to a feature vector by a small
      PointNet, and the result is scattered into a 2-D pseudo-image.
      From there it is an ordinary 2-D CNN backbone plus an SSD-style
      detection head.

      **Why it won:** it eliminated 3-D convolution entirely, hitting
      real-time rates on automotive hardware with competitive accuracy.
      Most production LiDAR detectors are descendants of this design.

   .. tab-item:: CenterPoint (2021)

      Anchor-free, and the natural 3-D analogue of the anchor-free shift
      you saw in YOLOv8. Objects are represented as **centre points** on
      a BEV heatmap; the network regresses size, orientation, and
      velocity from the peak.

      **Why it matters for us:** predicting per-object velocity directly
      gives the tracker in **L6** a motion estimate for free, and
      centre-based representation sidesteps the awkward problem of
      defining 3-D anchor boxes for objects at arbitrary yaw.

   .. tab-item:: Camera-only 3D

      3-D boxes can also be regressed from images alone (FCOS3D,
      monocular depth-based methods). Far cheaper, but depth is
      *inferred* rather than measured, so range error grows quadratically
      with distance. This is the gap that BEV methods in **L5** attack.

Evaluation Differs from 2D
~~~~~~~~~~~~~~~~~~~~~~~~~~~

3-D detection is **not** scored with 2-D IoU:

- **KITTI** uses 3-D (or BEV) IoU with class-dependent thresholds
  (0.7 for cars, 0.5 for pedestrians and cyclists) and splits results by
  difficulty (easy / moderate / hard) based on occlusion and truncation.
- **nuScenes** abandons IoU altogether for matching, using a **centre
  distance** threshold instead, and then reports the attribute errors
  (translation, scale, orientation, velocity) separately. You will meet
  its NDS metric in **L5**.

.. admonition:: Where this lands in your project
   :class: tip

   GP2 asks for detection **and** tracking. 2-D detection from the camera
   is where you start, but the tracker in L6 consumes 3-D state. Plan for
   the transition: either lift 2-D detections into 3-D using LiDAR
   (frustum association, covered in GP3), or run a LiDAR detector
   directly.


CARLA Hands-On: Object Detection Pipeline
--------------------------------------------

This exercise builds a complete detection pipeline from CARLA camera data
using the YOLO and DETR models discussed in this lecture. You will collect
frames from a simulated vehicle, run inference with both architectures, and
compare their performance under varying conditions.


Task 1: Spawn Vehicle and Collect Camera Frames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import carla
   import numpy as np
   import os
   import time
   from datetime import datetime

   # ── Connect to CARLA ──────────────────────────────────────────────
   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   world = client.get_world()
   bp_lib = world.get_blueprint_library()

   # ── Spawn ego vehicle ─────────────────────────────────────────────
   vehicle_bp = bp_lib.find('vehicle.tesla.model3')
   spawn_point = world.get_map().get_spawn_points()[0]
   vehicle = world.spawn_actor(vehicle_bp, spawn_point)
   vehicle.set_autopilot(True)
   print(f"Spawned vehicle: {vehicle.type_id} at {spawn_point.location}")

   # ── Attach an RGB camera (1280x720, fov 90) ──────────────────────
   camera_bp = bp_lib.find('sensor.camera.rgb')
   camera_bp.set_attribute('image_size_x', '1280')
   camera_bp.set_attribute('image_size_y', '720')
   camera_bp.set_attribute('fov', '90')
   camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
   camera = world.spawn_actor(camera_bp, camera_transform,
                              attach_to=vehicle)

   # ── Create timestamped output directory ────────────────────────────
   timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
   output_dir = os.path.join('carla_frames', timestamp)
   os.makedirs(output_dir, exist_ok=True)
   print(f"Saving frames to: {output_dir}")

   # ── Collect frames with a counter ─────────────────────────────────
   frame_count = 0
   max_frames = 200

   def camera_callback(image):
       global frame_count
       if frame_count >= max_frames:
           return
       array = np.frombuffer(image.raw_data, dtype=np.uint8)
       array = array.reshape((image.height, image.width, 4))[:, :, :3]
       filepath = os.path.join(output_dir, f'frame_{frame_count:04d}.png')
       import cv2
       cv2.imwrite(filepath, array)
       frame_count += 1
       if frame_count % 50 == 0:
           print(f"Saved {frame_count}/{max_frames} frames")

   camera.listen(camera_callback)

   # ── Wait until all frames are collected ────────────────────────────
   while frame_count < max_frames:
       time.sleep(0.1)

   print(f"Collection complete: {frame_count} frames saved to {output_dir}")

   # ── Cleanup ────────────────────────────────────────────────────────
   camera.stop()
   camera.destroy()
   vehicle.destroy()


Task 2: Run YOLO Inference on CARLA Frames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import cv2
   import os
   import glob
   import time
   from ultralytics import YOLO

   # ── Load pretrained YOLOv8s ────────────────────────────────────────
   model = YOLO('yolov8s.pt')

   # ── Set up paths ───────────────────────────────────────────────────
   input_dir = 'carla_frames/<YOUR_TIMESTAMP>'   # Update with your directory
   output_dir = input_dir + '_yolo'
   os.makedirs(output_dir, exist_ok=True)

   frames = sorted(glob.glob(os.path.join(input_dir, '*.png')))
   print(f"Running YOLOv8s on {len(frames)} frames...")

   # ── Run inference on each frame ────────────────────────────────────
   inference_times = []
   for i, frame_path in enumerate(frames):
       img = cv2.imread(frame_path)

       t_start = time.perf_counter()
       results = model(img, verbose=False)[0]
       t_end = time.perf_counter()

       elapsed_ms = (t_end - t_start) * 1000
       inference_times.append(elapsed_ms)

       # ── Draw bounding boxes and class labels ──────────────────────
       for box in results.boxes:
           x1, y1, x2, y2 = map(int, box.xyxy[0])
           conf = float(box.conf[0])
           cls_id = int(box.cls[0])
           label = f"{model.names[cls_id]} {conf:.2f}"
           cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
           cv2.putText(img, label, (x1, y1 - 8),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

       # ── Display and save ──────────────────────────────────────────
       cv2.imshow("YOLOv8s Detections", img)
       cv2.waitKey(1)
       out_path = os.path.join(output_dir, os.path.basename(frame_path))
       cv2.imwrite(out_path, img)

       print(f"Frame {i:04d}: {elapsed_ms:.1f} ms, "
             f"{len(results.boxes)} detections")

   cv2.destroyAllWindows()

   avg_time = sum(inference_times) / len(inference_times)
   print(f"\nYOLOv8s average inference time: {avg_time:.1f} ms/frame")
   print(f"Annotated frames saved to: {output_dir}")


Task 3: Run DETR Inference on the Same Frames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import cv2
   import os
   import glob
   import time
   from ultralytics import RTDETR      # NOT YOLO -- RT-DETR has its own class

   # ── Load pretrained RT-DETR-L ──────────────────────────────────────
   model = RTDETR('rtdetr-l.pt')

   # ── Set up paths ───────────────────────────────────────────────────
   input_dir = 'carla_frames/<YOUR_TIMESTAMP>'   # Same directory as Task 2
   output_dir = input_dir + '_rtdetr'
   os.makedirs(output_dir, exist_ok=True)

   frames = sorted(glob.glob(os.path.join(input_dir, '*.png')))
   print(f"Running RT-DETR-L on {len(frames)} frames...")

   # ── Run inference on each frame ────────────────────────────────────
   inference_times = []
   for i, frame_path in enumerate(frames):
       img = cv2.imread(frame_path)

       t_start = time.perf_counter()
       results = model(img, verbose=False)[0]
       t_end = time.perf_counter()

       elapsed_ms = (t_end - t_start) * 1000
       inference_times.append(elapsed_ms)

       # ── Draw bounding boxes and class labels ──────────────────────
       for box in results.boxes:
           x1, y1, x2, y2 = map(int, box.xyxy[0])
           conf = float(box.conf[0])
           cls_id = int(box.cls[0])
           label = f"{model.names[cls_id]} {conf:.2f}"
           cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
           cv2.putText(img, label, (x1, y1 - 8),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

       # ── Display and save ──────────────────────────────────────────
       cv2.imshow("RT-DETR-L Detections", img)
       cv2.waitKey(1)
       out_path = os.path.join(output_dir, os.path.basename(frame_path))
       cv2.imwrite(out_path, img)

       print(f"Frame {i:04d}: {elapsed_ms:.1f} ms, "
             f"{len(results.boxes)} detections")

   cv2.destroyAllWindows()

   avg_time = sum(inference_times) / len(inference_times)
   print(f"\nRT-DETR-L average inference time: {avg_time:.1f} ms/frame")
   print(f"Annotated frames saved to: {output_dir}")


Task 4: Compare YOLO vs DETR
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Exercise Tasks
   :class: tip

   1. **Compare inference speed**: Compute the mean and standard deviation of
      per-frame inference time (ms/frame) across all 200 frames for both
      YOLOv8s and RT-DETR-L. Which model is faster and by how much?
   2. **Compare detection counts and confidence distributions**: For each
      model, compute the average number of detections per frame and plot a
      histogram of confidence scores. Which model produces more high-confidence
      detections?
   3. **Export ground truth**: mAP cannot be computed from predictions
      alone. Before the weather study, dump CARLA's ground-truth 2-D
      boxes for each saved frame, using
      ``world.get_level_bbs(carla.CityObjectLabel.Car)`` or by projecting
      each vehicle actor's ``bounding_box`` into the image (remembering
      the UE-to-optical axis permutation from L2). Save them in YOLO
      label format alongside the images.

      .. note::

         Only export boxes that are actually **visible**: filter to
         actors in front of the camera, within a sensible range (e.g.
         50 m), and not fully occluded. Counting occluded vehicles as
         ground truth will make every model look artificially bad on
         recall.

   4. **Weather robustness experiment**: Re-run Task 1 frame collection
      (with ground-truth export) under three weather conditions and
      repeat Tasks 2--3 on each set:

      - Clear day: ``world.set_weather(carla.WeatherParameters.ClearNoon)``
      - Heavy rain: ``world.set_weather(carla.WeatherParameters.HardRainNoon)``
      - Night: use a preset with ``sun_altitude_angle`` below the horizon
        (verify which night presets your CARLA build exposes).

      Now compute and compare mAP@0.5 degradation across weather
      conditions for both models.
   5. **Identify failure cases**: Examine the annotated frames and find
      examples of missed detections and false positives for each model.
      Explain which architecture (CNN-based YOLO vs. transformer-based DETR)
      handles these failure cases better and why.

Summary
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Fundamentals and 2D Detection
      :class-card: sd-border-primary

      - **IoU** is the scale-invariant overlap measure behind both the
        loss and the metrics; **NMS** removes duplicate boxes but deletes
        genuinely overlapping objects; **mAP** needs ground-truth labels
      - Always state the dataset *and* the IoU protocol with any number:
        AP\ :sub:`50` on VOC and AP@[.5:.95] on COCO are not comparable
      - **YOLO**: backbone-neck-head, anchor-free since v8, NMS-free
        training in v10. Fast, mature, production-ready
      - **DETR**: set prediction with object queries and bipartite
        matching -- no anchors, no NMS. RT-DETR made it real-time

   .. grid-item-card:: 3D Detection and Deployment
      :class-card: sd-border-primary

      - Point clouds are unordered and irregular; **PointPillars**
        (pillars to a 2-D pseudo-image) is the fast production default
      - **CenterPoint** is anchor-free in 3-D and regresses velocity
        directly, feeding the tracker in L6 for free
      - 3-D evaluation abandons 2-D IoU: KITTI uses 3-D IoU by difficulty,
        nuScenes uses centre distance plus attribute errors
      - Deployment is a real constraint: quantization, pruning,
        distillation and TensorRT, profiled on the *target* SoC -- 50 FPS
        on a workstation GPU can be 5 FPS on an automotive one

.. important::

   At 60 km/h a vehicle covers 1.67 m in 100 ms. Perception latency is a
   safety requirement, not an optimization target -- which is why this
   lecture spends as much time on deployment as on architecture.

.. note::

   This exercise provides the detection foundation for **GP2:
   Perception**, where you will train custom YOLO and DETR models
   on CARLA data and deploy them as ROS 2 perception nodes.
