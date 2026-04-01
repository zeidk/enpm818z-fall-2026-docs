====================================================
Glossary
====================================================

:ref:`A <glossary-a>` · :ref:`B <glossary-b>` · :ref:`C <glossary-c>` · :ref:`D <glossary-d>` · :ref:`E <glossary-e>` · :ref:`F <glossary-f>` · :ref:`G <glossary-g>` · :ref:`H <glossary-h>` · :ref:`I <glossary-i>` · :ref:`K <glossary-k>` · :ref:`L <glossary-l>` · :ref:`M <glossary-m>` · :ref:`N <glossary-n>` · :ref:`O <glossary-o>` · :ref:`P <glossary-p>` · :ref:`R <glossary-r>` · :ref:`S <glossary-s>` · :ref:`T <glossary-t>` · :ref:`U <glossary-u>` · :ref:`V <glossary-v>` · :ref:`W <glossary-w>` · :ref:`Y <glossary-y>`

----


.. _glossary-a:

A
=

.. glossary::

   ADAS
      Advanced Driver Assistance Systems. Systems that support the human
      driver in performing parts of the Dynamic Driving Task. Corresponds
      to SAE Levels 1--2. Examples: Adaptive Cruise Control, Lane Keeping
      Assist.

   ADS
      Automated Driving Systems. Systems that perform the entire Dynamic
      Driving Task without human intervention within a specified ODD.
      Corresponds to SAE Levels 3--5.

   Anchor Box
      A predefined bounding box shape (width, height) used by object
      detectors like YOLO v3--v7 as a reference for predicting object
      locations. Anchor-free detectors (YOLOv8+, DETR) eliminate these.

   ASIL
      Automotive Safety Integrity Level. Defined by ISO 26262 to classify
      the severity of safety risks. Ranges from ASIL A (lowest) to ASIL D
      (highest), determining the rigor of development and testing required.


.. _glossary-b:

B
=

.. glossary::

   Backbone
      The feature extraction component of an object detection architecture.
      In YOLO, this is typically CSPDarknet or similar CNN that extracts
      hierarchical features from the input image.

   BEV
      Bird's-Eye View. A top-down representation of the driving scene that
      projects sensor data into an ego-centric 2D plane. The dominant
      perception paradigm in modern AV systems. See also: BEVFormer.

   Bipartite Matching
      The Hungarian algorithm used by DETR to find an optimal one-to-one
      assignment between predicted objects and ground truth during training.
      Eliminates the need for NMS.

   Blueprint Library
      In CARLA, a collection of templates for creating actors (vehicles,
      pedestrians, sensors) with configurable attributes like color and
      sensor parameters.


.. _glossary-c:

C
=

.. glossary::

   Calibration (Extrinsic)
      The process of determining the 6-DOF transformation (rotation +
      translation) between sensors or between a sensor and the vehicle
      frame. Essential for multi-sensor fusion.

   Calibration (Intrinsic)
      The process of determining a camera's internal parameters: focal
      lengths (fx, fy), principal point (cx, cy), and distortion
      coefficients. Typically performed using checkerboard patterns.

   CARLA
      CAR Learning to Act. An open-source autonomous driving simulator
      built on Unreal Engine 4, providing realistic urban/highway
      environments, sensor simulation, and a Python API.

   CIoU Loss
      Complete Intersection over Union loss. A bounding box regression
      loss used in YOLO that penalizes overlap, center distance, and
      aspect ratio simultaneously.

   CNN
      Convolutional Neural Network. A class of deep neural networks that
      use convolutional layers to extract spatial features from images.
      The backbone architecture for most object detectors.

   Complementarity Principle
      The observation (Luo, 1989) that different sensor technologies have
      unique strengths and weaknesses that balance each other out, making
      multi-sensor fusion essential for robust perception.


.. _glossary-d:

D
=

.. glossary::

   DDT
      Dynamic Driving Task. All real-time operational and tactical
      functions required to operate a vehicle in on-road traffic, including
      steering, acceleration, monitoring, and object detection. Excludes
      strategic functions like trip scheduling.

   DETR
      DEtection TRansformer. A transformer-based object detector that
      frames detection as a set prediction problem. Uses object queries
      and bipartite matching instead of anchors and NMS.

   Disparity
      The horizontal pixel difference between where the same 3D point
      appears in left and right stereo camera images. Used to compute
      depth: ``depth = (B x f) / d``.

   Doppler Effect
      The frequency shift in a reflected signal caused by the relative
      motion of the target. RADAR uses this to directly measure the
      velocity of moving objects.

   Dynamic Range
      The ratio between the brightest and darkest elements a camera sensor
      can capture simultaneously. Measured in dB; 120 dB means a million-
      to-one brightness ratio.


.. _glossary-e:

E
=

.. glossary::

   End-to-End Driving
      An approach where a single neural network maps raw sensor input
      directly to driving actions, bypassing the traditional modular
      pipeline (perception -> planning -> control).

   EKF
      Extended Kalman Filter. A non-linear extension of the Kalman Filter
      that uses Jacobian matrices to linearize the system at each time
      step.


.. _glossary-f:

F
=

.. glossary::

   FMEA
      Failure Mode and Effects Analysis. A systematic method for
      identifying potential failure modes in a system, assessing their
      impact, and designing mitigations (e.g., sensor redundancy).

   FPN
      Feature Pyramid Network. A neck architecture that fuses features
      across multiple scales via a top-down pathway with lateral
      connections, enabling detection of objects at different sizes.

   Fusion Architecture
      The strategy for combining data from multiple sensors. Three main
      types: early fusion (raw data), intermediate/mid-level fusion
      (features), and late fusion (detection outputs).


.. _glossary-g:

G
=

.. glossary::

   GNSS
      Global Navigation Satellite System. Provides absolute position
      (latitude, longitude, altitude). Includes GPS (US), GLONASS
      (Russia), Galileo (EU), BeiDou (China).


.. _glossary-h:

H
=

.. glossary::

   Head (Detection)
      The final component of an object detection architecture that
      produces bounding box coordinates and class predictions. Can be
      anchor-based (YOLO v3--v7) or anchor-free (YOLOv8+, DETR).

   Hungarian Algorithm
      An optimization algorithm that finds the minimum-cost one-to-one
      assignment between two sets. Used by DETR for bipartite matching
      between predictions and ground truth.


.. _glossary-i:

I
=

.. glossary::

   IMU
      Inertial Measurement Unit. Measures linear acceleration
      (accelerometers) and angular velocity (gyroscopes) at high
      frequency (>100 Hz). Suffers from drift over time.

   Instance Segmentation
      A perception task that assigns each object a unique ID and
      pixel-level mask, distinguishing individual instances of the same
      class (e.g., car #1 vs. car #2).

   IoU
      Intersection over Union. The ratio of the overlap area to the
      union area of a predicted and ground truth bounding box. Used as
      the primary metric for evaluating detection localization.

   ISO 26262
      International standard for functional safety of road vehicle
      electrical and electronic systems. Defines ASIL levels to classify
      risk severity.

   ISO 21448 (SOTIF)
      Safety of the Intended Functionality. Addresses safety hazards that
      occur without a system failure (e.g., sensor limitations). A
      critical complement to ISO 26262.


.. _glossary-k:

K
=

.. glossary::

   Kalman Filter
      An optimal recursive estimator for linear systems with Gaussian
      noise. Uses a predict-update cycle to fuse noisy sensor measurements
      over time. Foundation of IMU+GNSS fusion.

   Kalman Gain
      The blending factor in the Kalman Filter that determines how much
      weight to give to the new measurement vs. the prediction. High
      trust in sensor = high gain; high trust in prediction = low gain.


.. _glossary-l:

L
=

.. glossary::

   LiDAR
      Light Detection and Ranging. Uses laser pulses and time-of-flight
      to measure distances, producing 3D point clouds. Key specs: range,
      points per second, accuracy, beam count.


.. _glossary-m:

M
=

.. glossary::

   mAP
      Mean Average Precision. The primary metric for evaluating object
      detectors. mAP@0.5 uses a single IoU threshold; mAP@0.5:0.95
      averages across thresholds for stricter evaluation.

   MRC
      Minimal Risk Condition. A pre-planned safe response when a critical
      system failure is detected (e.g., safely pulling over and stopping).

   Multi-Object Tracking (MOT)
      The task of maintaining consistent identity for detected objects
      across consecutive frames. Methods: DeepSORT, ByteTrack.


.. _glossary-n:

N
=

.. glossary::

   Neck
      The multi-scale feature fusion component of a detection
      architecture, positioned between the backbone and head. Examples:
      FPN, PAN, BiFPN.

   NMS
      Non-Maximum Suppression. A post-processing step that removes
      duplicate detections by suppressing overlapping bounding boxes
      with lower confidence. Not needed in DETR.


.. _glossary-o:

O
=

.. glossary::

   Object Query
      In DETR, a learned embedding that is input to the transformer
      decoder. Each query attends to the encoded image features via
      cross-attention and specializes in detecting one object.

   ODD
      Operational Design Domain. The specific operating conditions
      (geographic, environmental, traffic) under which an ADS is designed
      to function safely.

   OES
      Operating Envelope Specification. A formal, machine-readable format
      proposed by NIST for precisely defining an ADS's ODD.


.. _glossary-p:

P
=

.. glossary::

   PAN
      Path Aggregation Network. A neck architecture that adds a bottom-up
      pathway to FPN, improving information flow for accurate localization.
      Used in YOLO v4+.

   Panoptic Segmentation
      A perception task that combines semantic segmentation (labeling
      "stuff" like road, sky) with instance segmentation (identifying
      individual "things" like cars, pedestrians).

   Particle Filter
      A non-parametric filter that approximates probability distributions
      using a set of weighted random samples (particles). Can handle
      arbitrary non-linear and non-Gaussian systems.

   Perception
      The process by which an autonomous system transforms unstructured
      sensor data into a structured, semantic understanding of the
      surrounding environment.

   Precision
      The fraction of detections that are correct: TP / (TP + FP).
      High precision means few false positives.


.. _glossary-r:

R
=

.. glossary::

   RADAR
      Radio Detection and Ranging. Uses radio waves to detect objects,
      measure distance, and directly measure velocity via the Doppler
      effect. Operates in all weather conditions. Standard automotive
      frequency: 77 GHz.

   Recall
      The fraction of real objects that the detector successfully found:
      TP / (TP + FN). High recall means few missed detections.

   Reprojection Error
      The distance (in pixels) between a known 3D point projected onto
      the image using calibrated parameters and its actual observed
      position. Used to validate calibration quality; should be < 2 px.

   ResNet
      Residual Network. A CNN architecture (He et al., 2016) that
      introduced skip connections, enabling training of very deep
      networks (50--152 layers) without degradation.

   RT-DETR
      Real-Time DETR. A transformer-based detector with an efficient
      hybrid encoder that achieves real-time speed competitive with YOLO
      while maintaining the NMS-free architecture.


.. _glossary-s:

S
=

.. glossary::

   SAE J3016
      The Society of Automotive Engineers standard that defines six levels
      of driving automation (Level 0--5), the industry-standard
      classification system.

   Semantic Segmentation
      A perception task that assigns a class label to every pixel in an
      image (e.g., road, sidewalk, vehicle) without distinguishing
      individual instances.

   SOTIF
      See :term:`ISO 21448 (SOTIF)`.

   Stereo Vision
      Depth estimation using two cameras separated by a known baseline.
      Computes depth from the disparity between left and right images.


.. _glossary-t:

T
=

.. glossary::

   Time-of-Flight (ToF)
      The operating principle of LiDAR. Measures the round-trip time of a
      laser pulse to compute distance: ``distance = (c x dt) / 2``.

   Transfer Learning
      Starting with a model pre-trained on a large dataset (e.g., COCO)
      and fine-tuning it on a smaller target dataset. Reduces training
      time and data requirements.

   Transformer
      A neural network architecture (Vaswani et al., 2017) based on
      self-attention mechanisms that model relationships between all
      positions in a sequence simultaneously. Used in DETR, BEVFormer,
      and modern AV perception.


.. _glossary-u:

U
=

.. glossary::

   UKF
      Unscented Kalman Filter. A non-linear filter that uses
      deterministic "sigma points" passed through the true non-linear
      function, avoiding the need for Jacobian matrices.

   UNECE GTR
      United Nations Economic Commission for Europe Global Technical
      Regulation. The UNECE GTR on ADS (approved Jan 2026) is the first
      global safety framework for autonomous driving.


.. _glossary-v:

V
=

.. glossary::

   V2X
      Vehicle-to-Everything communication. Includes V2V (vehicle-to-
      vehicle), V2I (vehicle-to-infrastructure), and V2P (vehicle-to-
      pedestrian). Enables cooperative perception and situational
      awareness.

   ViT
      Vision Transformer. A transformer architecture (Dosovitskiy et al.,
      2021) that splits images into patches and processes them as a
      sequence, applying self-attention for image classification.


.. _glossary-w:

W
=

.. glossary::

   Waypoint
      In CARLA, a discrete point on the road network containing lane
      information, speed limits, and connectivity to other waypoints.
      Used for path planning and navigation.


.. _glossary-y:

Y
=

.. glossary::

   YOLO
      You Only Look Once. A family of single-stage object detectors that
      predict all bounding boxes and class probabilities in a single
      forward pass. Evolution: v1 (2015) to v11 (2024).
