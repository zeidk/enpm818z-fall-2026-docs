====================================================
Lecture
====================================================


Semantic Segmentation
----------------------

Object detection from L3 gives us **where objects are** (bounding boxes) but
not **what every pixel is**. Semantic segmentation provides a dense,
pixel-level classification that is essential for understanding driveable space,
lane structure, and arbitrary obstacles.

.. admonition:: Definition
   :class: note

   **Semantic segmentation** assigns a class label to every pixel in an image.
   Unlike detection, there is no "instance" concept -- all pixels belonging to
   the same class receive the same label, regardless of how many separate
   objects there are.

The Segmentation Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 80
   :class: compact-table

   * - **Input**
     - RGB image :math:`I \in \mathbb{R}^{H \times W \times 3}`
   * - **Output**
     - Label map :math:`S \in \{1, \ldots, K\}^{H \times W}`, one label per pixel
   * - **Loss**
     - Pixel-wise cross-entropy (or weighted variant for class imbalance)
   * - **Metric**
     - Mean IoU (mIoU) across all classes


U-Net Architecture
~~~~~~~~~~~~~~~~~~~

U-Net (Ronneberger et al., 2015), originally designed for medical imaging, has
become a standard backbone for segmentation due to its **encoder-decoder
structure with skip connections**.

.. code-block:: text

   Encoder (Contracting Path)        Decoder (Expanding Path)
   ─────────────────────────         ──────────────────────────
   Input (H x W x 3)                 Logits (H x W x K)
       │ Conv + Pool                      │ Up-Conv + Conv
   H/2 x W/2 x 64          ──skip──   H/2 x W/2 x 64
       │ Conv + Pool                      │ Up-Conv + Conv
   H/4 x W/4 x 128         ──skip──   H/4 x W/4 x 128
       │ Conv + Pool                      │ Up-Conv + Conv
   H/8 x W/8 x 256         ──skip──   H/8 x W/8 x 256
       │ Conv + Pool                      │ Up-Conv + Conv
   H/16 x W/16 x 512       ──skip──   H/16 x W/16 x 512
       │ Bottleneck (H/32 x W/32 x 1024) │

Key properties:

- **Skip connections** concatenate encoder feature maps with decoder feature
  maps at the same resolution, preserving fine spatial detail.
- **No fully connected layers** -- the network is fully convolutional, allowing
  arbitrary input sizes.
- **Symmetric structure** enables pixel-precise localization from high-level
  semantic features.


DeepLabv3+ Architecture
~~~~~~~~~~~~~~~~~~~~~~~~

DeepLabv3+ (Chen et al., 2018) uses **atrous (dilated) convolutions** and
**Atrous Spatial Pyramid Pooling (ASPP)** to capture multi-scale context
without reducing spatial resolution.

.. tab-set::

   .. tab-item:: Dilated Convolutions

      Standard convolution at stride 2 reduces spatial resolution. Dilated
      convolutions insert "holes" (zeros) between kernel weights, increasing
      the **receptive field** without downsampling:

      .. math::

         y[i] = \sum_k x[i + r \cdot k] \cdot w[k]

      where :math:`r` is the dilation rate. Rate :math:`r=2` doubles the
      receptive field with the same number of parameters.

   .. tab-item:: ASPP

      Atrous Spatial Pyramid Pooling applies parallel dilated convolutions
      at multiple rates (e.g., 6, 12, 18) and pools at different scales,
      then concatenates the results. This captures objects at multiple scales
      in a single forward pass.

   .. tab-item:: Encoder-Decoder

      DeepLabv3+ adds a lightweight decoder on top of the ASPP module:

      1. ASPP encoder produces low-resolution features.
      2. Low-level encoder features (1/4 resolution) are extracted via a
         1x1 conv.
      3. Upsampled ASPP features are concatenated with low-level features.
      4. Two 3x3 convolutions refine boundaries.
      5. Bilinear upsampling to full resolution.


Driveable Surface and Lane Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two specialized segmentation tasks critical for AV systems:

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Driveable Surface
      :class-card: sd-border-info

      Segment all pixels belonging to navigable road surface. Key challenges:
      varying lighting, wet roads (reflections), construction zones, unmarked
      rural roads. Often implemented as a binary segmentation (driveable /
      not-driveable).

   .. grid-item-card:: Lane Detection
      :class-card: sd-border-info

      Detect lane markings as pixel masks or parametric curves. Methods range
      from simple Hough-transform line detection to deep learning approaches
      (LaneNet, CLRNet) that predict lane curves with instance-level grouping.

.. admonition:: Tip: BEV Segmentation
   :class: tip

   Both tasks benefit enormously from the BEV representation (L4). Perspective
   foreshortening makes lane width and curvature appear non-uniform. In BEV,
   lanes are uniform-width curves -- simpler to predict and post-process.


Instance and Panoptic Segmentation
------------------------------------

.. list-table::
   :widths: 25 38 37
   :header-rows: 1
   :class: compact-table

   * - Task
     - What it produces
     - Distinguishes instances?
   * - Semantic segmentation
     - Per-pixel class label
     - No
   * - Instance segmentation
     - Per-pixel class + instance ID for "things"
     - Yes (for countable objects)
   * - Panoptic segmentation
     - Per-pixel class label for all pixels; instance IDs for "things"
     - Yes (unified)

Mask R-CNN
~~~~~~~~~~~

Mask R-CNN (He et al., 2017) extends Faster R-CNN by adding a **mask head** --
a small fully convolutional network that predicts a binary segmentation mask
for each detected bounding box:

1. **Region Proposal Network (RPN)** -- proposes candidate bounding boxes.
2. **RoIAlign** -- extracts aligned feature maps from each proposal.
3. **Box and class heads** -- predict refined box and class (as in Faster R-CNN).
4. **Mask head** -- predicts a :math:`28 \times 28` binary mask per class for
   each proposal, applied in parallel with the box head.

.. math::

   \mathcal{L} = \mathcal{L}_{cls} + \mathcal{L}_{box} + \mathcal{L}_{mask}

Panoptic Segmentation
~~~~~~~~~~~~~~~~~~~~~~

Panoptic segmentation unifies semantic and instance segmentation:

- **"Things"** (countable objects: cars, pedestrians): assigned instance IDs.
- **"Stuff"** (amorphous regions: road, sky, vegetation): assigned class label only.

The **Panoptic Quality (PQ)** metric:

.. math::

   \text{PQ} = \frac{\sum_{(p,g) \in TP} \text{IoU}(p,g)}
                {|TP| + \frac{1}{2}|FP| + \frac{1}{2}|FN|}
              = \underbrace{\frac{|TP|}{|TP| + \frac{1}{2}|FP| + \frac{1}{2}|FN|}}_{\text{SQ-like recognition}}
                \times
                \underbrace{\frac{\sum \text{IoU}}{|TP|}}_{\text{SQ segmentation quality}}


Multi-Object Tracking (MOT)
-----------------------------

Detection gives us objects in a single frame. **Multi-Object Tracking (MOT)**
maintains consistent identities for all objects across a video sequence.

Problem Formulation
~~~~~~~~~~~~~~~~~~~~

Given detections :math:`\mathcal{D}_t = \{d_1, d_2, \ldots\}` at each frame
:math:`t`, produce **tracks** :math:`\mathcal{T} = \{T_1, T_2, \ldots\}` where
each track is a sequence of states associated with the same physical object:

.. math::

   T_i = \{(t, s_t^i) : t \in [t_{start}^i, t_{end}^i]\}

where :math:`s_t^i` is the state (position, velocity, class) of track :math:`i`
at time :math:`t`.

Challenges: occlusion, similar-looking objects, appearance changes, variable
frame rate, missed detections, false positives from the detector.


SORT: Simple Online and Realtime Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SORT (Bewley et al., 2016) is a minimal, highly efficient tracker built on
two components:

.. tab-set::

   .. tab-item:: Kalman Filter State

      Each track maintains a Kalman Filter state:

      .. math::

         \mathbf{x} = [u, v, s, r, \dot{u}, \dot{v}, \dot{s}]^T

      where :math:`(u, v)` is the bounding box center, :math:`s` is scale
      (area), :math:`r` is aspect ratio (constant), and the dots denote
      velocities. The state is propagated with a constant-velocity model.

   .. tab-item:: Hungarian Algorithm

      At each frame, detections and tracks are associated using the **Hungarian
      algorithm** (optimal bipartite matching) on an IoU cost matrix:

      .. math::

         C_{ij} = 1 - \text{IoU}(\hat{b}_i, d_j)

      where :math:`\hat{b}_i` is the predicted bounding box of track :math:`i`
      and :math:`d_j` is detection :math:`j`. Pairs below a minimum IoU
      threshold are rejected.

   .. tab-item:: Track Management

      - **New track**: created for unmatched detections.
      - **Confirmed track**: promoted after 3 consecutive matches.
      - **Dead track**: removed after :math:`T_{lost}` frames without a match.

SORT achieves real-time tracking (260 Hz on a standard CPU for 6 tracks)
but re-assigns IDs after occlusion because it uses no appearance features.


DeepSORT
~~~~~~~~~

DeepSORT (Wojke et al., 2017) extends SORT with a **deep appearance
descriptor** to handle re-identification after occlusion:

1. A CNN (trained on person re-ID datasets) extracts a 128-dimensional
   appearance embedding for each detection crop.
2. Each track maintains a **gallery** of the last 100 appearance embeddings.
3. The cost matrix combines IoU distance and **cosine appearance distance**:

   .. math::

      C_{ij} = \lambda \cdot d_{appear}(i, j) + (1 - \lambda) \cdot d_{IoU}(i, j)

4. Tracks are confirmed/tentative/deleted as in SORT.

The appearance matching allows DeepSORT to correctly re-identify an object
returning from a long occlusion, at the cost of slightly higher compute.


ByteTrack
~~~~~~~~~~

ByteTrack (Zhang et al., 2022) addresses a fundamental issue in tracking:
SORT and DeepSORT only associate **high-confidence** detections with tracks,
discarding low-confidence detections as noise.

ByteTrack's insight: **low-confidence detections often correspond to occluded
or distant objects** -- exactly the objects most likely to cause ID switches.

.. admonition:: ByteTrack Algorithm
   :class: note

   1. Run detector; split detections into high-score (:math:`\tau_{high} = 0.6`)
      and low-score (:math:`\tau_{low} = 0.1` to :math:`\tau_{high}`).
   2. **First association**: match high-score detections to all tracks via
      IoU-based Hungarian matching.
   3. **Second association**: match low-score detections to **unmatched tracks**
      from step 2 -- recovering occluded objects.
   4. Initialize new tracks from unmatched high-score detections only.

ByteTrack achieves state-of-the-art on MOT17 (80.3 MOTA, 77.3 IDF1) at
30 FPS, with no appearance model required.


Tracking Metrics
~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 15 40 45
   :header-rows: 1
   :class: compact-table

   * - Metric
     - Formula
     - Interpretation
   * - **MOTA**
     - :math:`1 - \frac{\sum_t (FN_t + FP_t + IDSW_t)}{\sum_t GT_t}`
     - Overall tracking accuracy; penalizes FN, FP, and ID switches. Range: :math:`(-\infty, 1]`.
   * - **MOTP**
     - :math:`\frac{\sum_{i,t} d_t^i}{\sum_t c_t}`
     - Average localization precision for matched pairs (IoU or distance). Higher = better.
   * - **IDF1**
     - :math:`\frac{2 \cdot IDTP}{2 \cdot IDTP + IDFP + IDFN}`
     - F1 score for correct identity assignments. Emphasizes consistent ID maintenance.
   * - **HOTA**
     - Geometric mean of detection and association accuracy
     - Balances detection quality and track association quality equally.

.. admonition:: Metric Intuition
   :class: tip

   - MOTA is dominated by detection quality (FP/FN). A perfect detector with
     random IDs can still score high MOTA.
   - IDF1 better captures ID consistency -- important for downstream tasks
     like trajectory prediction.
   - HOTA (newer metric) explicitly balances both.


Temporal Reasoning
-------------------

Single-frame perception has fundamental limits: a fast-moving car is a static
snapshot, an occluded pedestrian is invisible, noise has no temporal structure.
**Temporal reasoning** uses multiple frames to overcome these limits.

Why Temporal Context Matters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Velocity Estimation
      :class-card: sd-border-success

      Observing the same object across consecutive frames provides direct
      velocity estimates via optical flow or Kalman filter -- impossible from
      a single frame without additional assumptions.

   .. grid-item-card:: Occlusion Handling
      :class-card: sd-border-success

      An object occluded in frame :math:`t` was visible in frame :math:`t-1`.
      Temporal models can propagate its estimated state through occlusion gaps.

   .. grid-item-card:: Noise Reduction
      :class-card: sd-border-success

      Random detection noise is uncorrelated across frames. Temporal smoothing
      (Kalman filter, temporal attention) averages out noise while preserving
      true object motion.

Methods for Temporal Perception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Method
     - Mechanism
   * - **Recurrent Networks (LSTM/GRU)**
     - Maintain a hidden state that accumulates frame history. Used in
       early video object detection models.
   * - **3D Convolutions**
     - Apply convolutions along both spatial and temporal dimensions
       simultaneously (C3D, SlowFast, Video Swin).
   * - **Temporal BEV Attention**
     - BEVFormer-style: warp previous BEV frame to current ego pose, then
       cross-attend with current queries (most practical for AV systems).
   * - **Optical Flow**
     - Estimate dense pixel motion between frames; used to warp features
       or as an explicit velocity prior.

Tracking-by-Detection Paradigm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The dominant MOT paradigm in autonomous driving:

.. code-block:: text

   Frame t:
   ┌──────────────┐     ┌──────────────────┐     ┌────────────────────┐
   │  Detector    │────>│  State Predictor │────>│  Data Association  │
   │  (YOLO,      │     │  (Kalman Filter) │     │  (Hungarian Algo / │
   │   DETR, etc) │     │  Predict track   │     │   Appearance dist) │
   └──────────────┘     │  positions to t  │     └────────┬───────────┘
                        └──────────────────┘              │
                                                   ┌──────▼──────────┐
                                                   │  Track Update   │
                                                   │  + Management   │
                                                   │  (new/dead)     │
                                                   └─────────────────┘

The detector is completely independent of the tracker. This means improving
either component independently improves overall tracking.


Integration with the L3-L4 Pipeline
-------------------------------------

The full perception pipeline for autonomous driving:

.. list-table::
   :widths: 15 85
   :class: compact-table

   * - **L3**
     - Raw sensor inputs → 3D object detection (LiDAR PointPillars/VoxelNet,
       camera DETR/YOLO) → 3D bounding boxes with class and confidence.
   * - **L4**
     - Multi-camera images → BEV feature construction (LSS, BEVFormer) →
       BEV detection heads → 3D boxes or occupancy voxels in ego frame.
   * - **L5 (segmentation)**
     - Camera images → semantic/panoptic segmentation → driveable surface mask,
       lane lines, free space boundaries. BEV projection for planning.
   * - **L5 (tracking)**
     - 3D bounding boxes from L3/L4 → Kalman filter state prediction →
       Hungarian / ByteTrack association → confirmed tracks with IDs and
       velocity estimates.
   * - **Output**
     - Per-object tracks with state history: position, velocity, orientation,
       class, ID. Input to prediction and planning modules.

.. admonition:: Real-World Performance Trade-offs
   :class: warning

   In production AV systems, tracking must run within a strict latency budget
   (typically <50 ms total for the perception stack). Appearance-based methods
   (DeepSORT) improve ID consistency but add compute. ByteTrack's approach of
   using all detections (not just high-confidence) significantly reduces ID
   switches at negligible compute cost -- a favorable engineering trade-off.


Summary
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Segmentation
      :class-card: sd-border-primary

      - Semantic: per-pixel class labels (U-Net, DeepLabv3+)
      - Instance: per-object masks (Mask R-CNN)
      - Panoptic: unified things + stuff (PQ metric)
      - Specialized: driveable surface, lane detection

   .. grid-item-card:: Tracking & Temporal
      :class-card: sd-border-primary

      - MOT paradigm: tracking-by-detection
      - SORT: Kalman filter + IoU Hungarian matching
      - DeepSORT: adds appearance embedding for re-ID
      - ByteTrack: uses low-confidence detections for occlusion recovery
      - Metrics: MOTA (accuracy), IDF1 (identity), HOTA (balanced)
