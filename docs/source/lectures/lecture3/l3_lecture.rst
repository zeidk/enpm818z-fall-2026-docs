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

   .. tab-item:: Low-Level Processing

      Operates at the pixel/sub-pixel level. Fast, but not semantic.

      - **Edge detection:** Canny, Sobel
      - **Corner detection:** Harris, FAST
      - **Optical flow:** Lucas-Kanade, FlowNet
      - **Depth estimation:** SGM, PSMNet
      - **Feature descriptors:** SIFT, SURF, ORB

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


The Deep Learning Revolution
-----------------------------

Why Traditional CV Failed
~~~~~~~~~~~~~~~~~~~~~~~~~

Classical methods (HOG + SVM for pedestrians, SIFT for matching) required
extensive manual feature engineering, were fragile to appearance variation,
and could not generalize across conditions. They worked in controlled settings
but failed in the diversity of real-world driving.

**Key milestones in the DL revolution:**

.. list-table::
   :widths: 15 25 60
   :header-rows: 1
   :class: compact-table

   * - Year
     - Model
     - Key Innovation
   * - 2012
     - AlexNet
     - First GPU-trained CNN; won ImageNet by large margin
   * - 2014
     - VGGNet
     - 16--19 layers, uniform 3x3 filters
   * - 2014
     - GoogLeNet
     - Inception modules for multi-scale features
   * - 2015
     - ResNet
     - Residual connections; 50--152 layers without degradation
   * - 2015
     - Faster R-CNN
     - Region Proposal Network for two-stage detection
   * - 2015
     - **YOLO v1**
     - Single-stage detection: one forward pass predicts all boxes
   * - 2020
     - **DETR**
     - Transformer-based detection: no anchors, no NMS

**Why DL works:** Hierarchical feature learning -- early layers learn edges,
middle layers learn shapes, deep layers learn object templates. Key enablers:
large-scale datasets (ImageNet 14M images, COCO 330K, nuScenes), GPU
acceleration, improved optimization (Adam, batch norm, residual connections),
and transfer learning.


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
     - COCO mAP
   * - v1
     - 2015
     - Single-stage detection, 7x7 grid
     - 63.4% (VOC)
   * - v2
     - 2017
     - Batch norm, anchor boxes, Darknet-19
     - 78.6% (VOC)
   * - v3
     - 2018
     - FPN multi-scale, Darknet-53, 3 detection scales
     - 57.9%
   * - v4
     - 2020
     - CSPDarknet53, Mosaic augmentation, PAN, CIoU loss
     - 43.5%
   * - v5
     - 2020
     - PyTorch native, model scaling (n/s/m/l/x), AutoAugment
     - 50.7%
   * - v7
     - 2022
     - E-ELAN, SOTA at the time
     - 56.8%
   * - v8
     - 2023
     - **Anchor-free**, decoupled head, multi-task (det/seg/pose)
     - 53.9%
   * - v10
     - 2024
     - NMS-free training, dual label assignment
     - 54.4%
   * - v11
     - 2024
     - C3k2 blocks, SPPF modifications
     - 54.7%


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

   In Assignment A2, you will fine-tune both YOLO and DETR on the same CARLA
   dataset and compare their performance under different conditions (day/night,
   rain, occlusion).


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
           cv_image = self.bridge.imgmsg_to_cv2(msg, 'rgb8')
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
       perception. *Covered in L4.*
   * - **3D Occupancy Networks**
     - Predict per-voxel semantic occupancy, handling arbitrary-shaped
       obstacles that bounding boxes miss. *Covered in L4.*
   * - **Multi-Task Learning**
     - Single backbone with multiple heads (detection + segmentation + lane
       detection). Example: Tesla HydraNet.
   * - **3D Object Detection**
     - LiDAR-based (PointPillars, CenterPoint) and camera-based (FCOS3D)
       methods for 3D bounding boxes.
   * - **End-to-End Perception**
     - UniAD, DriveTransformer unify perception-prediction-planning.
       *Covered in L11.*
