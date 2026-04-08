====================================================
Lecture
====================================================


Segmentation for Autonomous Driving
-------------------------------------

.. admonition:: Recap from ENPM673
   :class: note

   In ENPM673, you studied semantic segmentation fundamentals: pixel-wise
   classification, the encoder-decoder paradigm (U-Net), mIoU evaluation,
   and the distinction between semantic, instance, and panoptic segmentation.
   This lecture focuses on how these techniques are **deployed in autonomous
   driving** and introduces AV-specific architectures and tasks.

Object detection from L3 gives us **where objects are** (bounding boxes) but
not **what every pixel is**. In autonomous driving, dense pixel-level
understanding is critical: the planner needs to know which surfaces are safe to
drive on, where lane boundaries lie, and which regions are occupied by
obstacles of any shape -- information that bounding boxes alone cannot provide.


DeepLabv3+ Architecture
~~~~~~~~~~~~~~~~~~~~~~~~

While U-Net established the encoder-decoder paradigm for segmentation,
autonomous driving demands architectures that can capture **multi-scale
context** efficiently. DeepLabv3+ (Chen et al., 2018) addresses this with
**atrous (dilated) convolutions** and **Atrous Spatial Pyramid Pooling
(ASPP)** -- techniques that enlarge the receptive field without sacrificing
spatial resolution. DeepLabv3+ and its variants remain widely used in
production AV perception stacks because they offer a strong accuracy-latency
trade-off on high-resolution driving imagery.

.. tab-set::

   .. tab-item:: Dilated Convolutions

      Standard convolution at stride 2 reduces spatial resolution. Dilated
      convolutions insert "holes" (zeros) between kernel weights, increasing
      the **receptive field** without downsampling:

      .. math::

         y[i] = \sum_k x[i + r \cdot k] \cdot w[k]

      where :math:`r` is the dilation rate. Rate :math:`r=2` doubles the
      receptive field with the same number of parameters.

      For AV perception this is essential: objects such as trucks or road
      barriers span a wide range of scales in a single frame due to
      perspective projection. Dilated convolutions let the network "see"
      large structures while retaining the fine resolution needed for
      accurate boundary delineation.

   .. tab-item:: ASPP

      Atrous Spatial Pyramid Pooling applies parallel dilated convolutions
      at multiple rates (e.g., 6, 12, 18) and pools at different scales,
      then concatenates the results. This captures objects at multiple scales
      in a single forward pass.

      In driving scenes the same class (e.g., *vehicle*) can appear at
      vastly different scales depending on distance. ASPP's multi-rate
      design ensures that both nearby and far-away instances are encoded
      with rich contextual features without requiring explicit multi-scale
      input pyramids.

   .. tab-item:: Encoder-Decoder

      DeepLabv3+ adds a lightweight decoder on top of the ASPP module:

      1. ASPP encoder produces low-resolution features.
      2. Low-level encoder features (1/4 resolution) are extracted via a
         1x1 conv.
      3. Upsampled ASPP features are concatenated with low-level features.
      4. Two 3x3 convolutions refine boundaries.
      5. Bilinear upsampling to full resolution.

      The explicit fusion of low-level (edge/texture) and high-level
      (semantic) features is particularly important for driving tasks such
      as curb detection and lane boundary segmentation, where pixel-precise
      boundaries directly affect downstream planning accuracy.


Driveable Surface and Lane Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two specialized segmentation tasks critical for AV systems:

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Driveable Surface
      :class-card: sd-border-info

      Segment all pixels belonging to navigable road surface. Key challenges:
      varying lighting, wet roads (reflections), construction zones, unmarked
      rural roads. Often implemented as a binary or ternary segmentation
      (directly driveable / alternatively driveable / not-driveable).

      **Why it matters for planning.** The planner's trajectory generator
      operates over *free space* -- the region where the ego vehicle can
      physically drive without collision. The driveable surface mask, once
      projected into BEV or 3-D, defines this free-space boundary. Without
      it, the planner must rely solely on object detections and HD-map lanes,
      which fail in unmapped areas or when obstacles have unusual shapes
      (e.g., road debris, fallen trees).

   .. grid-item-card:: Lane Detection
      :class-card: sd-border-info

      Detect lane markings as pixel masks or parametric curves.

      **Classical approaches** use edge detection and Hough transforms but
      fail under occlusion and complex topology. **Modern deep-learning
      methods** treat lane detection as a structured prediction task:

      - **CLRNet** (Zheng et al., 2022) performs row-based anchor detection:
        it predicts lateral lane offsets at a discrete set of row positions,
        then refines them with cross-layer feature aggregation.
      - Many recent approaches predict **polynomial or spline coefficients**
        (e.g., cubic B-splines) per lane instance rather than per-pixel
        masks, yielding a compact, smooth representation directly usable by
        the planner's path-following controller.

.. admonition:: BEV Projection Simplifies Lane Detection
   :class: tip

   Both tasks benefit enormously from the BEV representation introduced in
   L4. In perspective view, foreshortening makes lane width and curvature
   appear non-uniform -- lanes converge toward the horizon and curvature
   is compressed at distance. In BEV, lanes become **uniform-width curves**
   that are simpler to predict, fit with polynomials, and post-process.
   Several state-of-the-art lane detectors (PersFormer, Anchor3DLane) now
   predict lanes directly in BEV space, side-stepping perspective distortion
   entirely.


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


CARLA Hands-On: Segmentation and Object Tracking
--------------------------------------------------

This exercise uses CARLA's ground-truth semantic camera and vehicle
detections to implement segmentation visualization and a basic SORT tracker.


Task 1: Semantic Segmentation from CARLA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CARLA provides a ground-truth semantic segmentation camera that assigns
class labels to every pixel. This lets you explore segmentation output
without training a model.

.. code-block:: python

   import carla
   import numpy as np
   import cv2

   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   world = client.get_world()
   bp_lib = world.get_blueprint_library()

   # Spawn ego vehicle
   vehicle_bp = bp_lib.find('vehicle.tesla.model3')
   spawn_point = world.get_map().get_spawn_points()[0]
   vehicle = world.spawn_actor(vehicle_bp, spawn_point)
   vehicle.set_autopilot(True)

   # Spawn semantic segmentation camera
   seg_bp = bp_lib.find('sensor.camera.semantic_segmentation')
   seg_bp.set_attribute('image_size_x', '1280')
   seg_bp.set_attribute('image_size_y', '720')
   seg_bp.set_attribute('fov', '90')
   seg_cam = world.spawn_actor(
       seg_bp,
       carla.Transform(carla.Location(x=1.5, z=2.4)),
       attach_to=vehicle)

   # CARLA semantic labels (subset)
   LABEL_COLORS = {
       0: (0, 0, 0),        # Unlabeled
       1: (70, 70, 70),     # Building
       4: (128, 64, 128),   # Road
       5: (244, 35, 232),   # Sidewalk
       6: (107, 142, 35),   # Vegetation
       7: (0, 0, 142),      # Vehicle
       9: (0, 0, 230),      # Traffic Light
       10: (220, 20, 60),   # Pedestrian
       12: (220, 220, 0),   # Traffic Sign
       24: (157, 234, 50),  # Lane Marking
   }

   def seg_callback(image):
       """Colorize semantic segmentation output."""
       array = np.frombuffer(image.raw_data, dtype=np.uint8)
       array = array.reshape((image.height, image.width, 4))
       labels = array[:, :, 2]  # semantic tag is in the red channel

       colored = np.zeros((image.height, image.width, 3), dtype=np.uint8)
       for label_id, color in LABEL_COLORS.items():
           colored[labels == label_id] = color

       # Compute driveable surface mask (road + lane markings)
       driveable = ((labels == 4) | (labels == 24)).astype(np.uint8) * 255

       cv2.imshow("Semantic Segmentation", colored)
       cv2.imshow("Driveable Surface", driveable)
       cv2.waitKey(1)

   seg_cam.listen(seg_callback)


Task 2: Compute Segmentation Metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def compute_miou(pred_labels, gt_labels, num_classes):
       """Compute mean Intersection over Union across all classes."""
       ious = []
       for c in range(num_classes):
           pred_c = (pred_labels == c)
           gt_c = (gt_labels == c)
           intersection = np.logical_and(pred_c, gt_c).sum()
           union = np.logical_or(pred_c, gt_c).sum()
           if union > 0:
               ious.append(intersection / union)
       return np.mean(ious) if ious else 0.0

   # Usage: compare a model's predictions against CARLA ground truth
   # miou = compute_miou(model_output, carla_gt_labels, num_classes=23)


Task 3: Implement a Basic SORT Tracker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This implements the core SORT algorithm: Kalman filter prediction +
IoU-based Hungarian matching.

.. code-block:: python

   from scipy.optimize import linear_sum_assignment

   class KalmanBoxTracker:
       """Kalman filter tracker for a single bounding box."""
       _count = 0

       def __init__(self, bbox):
           """Initialize with bounding box [x1, y1, x2, y2]."""
           self.id = KalmanBoxTracker._count
           KalmanBoxTracker._count += 1

           # State: [cx, cy, area, aspect_ratio, vx, vy, va]
           cx = (bbox[0] + bbox[2]) / 2
           cy = (bbox[1] + bbox[3]) / 2
           area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
           aspect = (bbox[2] - bbox[0]) / max(bbox[3] - bbox[1], 1)

           self.state = np.array([cx, cy, area, aspect, 0, 0, 0],
                                 dtype=np.float64)
           self.hits = 1
           self.age = 0
           self.time_since_update = 0

       def predict(self):
           """Constant-velocity prediction."""
           self.state[:3] += self.state[4:7]  # update position with velocity
           self.age += 1
           self.time_since_update += 1
           return self._state_to_bbox()

       def update(self, bbox):
           """Update state with matched detection."""
           cx = (bbox[0] + bbox[2]) / 2
           cy = (bbox[1] + bbox[3]) / 2
           area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

           # Simple exponential moving average (alpha = 0.7)
           alpha = 0.7
           old_cx, old_cy, old_area = self.state[:3]
           self.state[4] = alpha * (cx - old_cx) + (1 - alpha) * self.state[4]
           self.state[5] = alpha * (cy - old_cy) + (1 - alpha) * self.state[5]
           self.state[6] = alpha * (area - old_area) + (1-alpha) * self.state[6]
           self.state[0] = cx
           self.state[1] = cy
           self.state[2] = area
           self.hits += 1
           self.time_since_update = 0

       def _state_to_bbox(self):
           """Convert state back to [x1, y1, x2, y2]."""
           cx, cy, area, aspect = self.state[:4]
           w = np.sqrt(max(area * aspect, 1))
           h = max(area / w, 1)
           return np.array([cx - w/2, cy - h/2, cx + w/2, cy + h/2])


   def iou_batch(bb_det, bb_trk):
       """Compute IoU between all pairs of detection and track boxes."""
       # bb_det: (M, 4), bb_trk: (N, 4) -- [x1, y1, x2, y2]
       M, N = len(bb_det), len(bb_trk)
       iou_matrix = np.zeros((M, N))
       for m in range(M):
           for n in range(N):
               x1 = max(bb_det[m, 0], bb_trk[n, 0])
               y1 = max(bb_det[m, 1], bb_trk[n, 1])
               x2 = min(bb_det[m, 2], bb_trk[n, 2])
               y2 = min(bb_det[m, 3], bb_trk[n, 3])
               inter = max(0, x2 - x1) * max(0, y2 - y1)
               area_d = ((bb_det[m, 2] - bb_det[m, 0])
                         * (bb_det[m, 3] - bb_det[m, 1]))
               area_t = ((bb_trk[n, 2] - bb_trk[n, 0])
                         * (bb_trk[n, 3] - bb_trk[n, 1]))
               iou_matrix[m, n] = inter / max(area_d + area_t - inter, 1e-6)
       return iou_matrix


   class SORTTracker:
       """Simple Online and Realtime Tracking."""

       def __init__(self, max_age=5, min_hits=3, iou_threshold=0.3):
           self.max_age = max_age
           self.min_hits = min_hits
           self.iou_threshold = iou_threshold
           self.trackers = []

       def update(self, detections):
           """
           Update tracks with new detections.

           Args:
               detections: np.array of shape (M, 4) -- [x1, y1, x2, y2]

           Returns:
               np.array of shape (K, 5) -- [x1, y1, x2, y2, track_id]
           """
           # Predict existing tracks
           predicted = []
           for trk in self.trackers:
               predicted.append(trk.predict())
           predicted = np.array(predicted) if predicted else np.empty((0, 4))

           # Associate detections to tracks via Hungarian algorithm
           if len(detections) > 0 and len(predicted) > 0:
               iou_matrix = iou_batch(detections, predicted)
               row_idx, col_idx = linear_sum_assignment(-iou_matrix)

               matched, unmatched_dets, unmatched_trks = [], [], []
               for m, t in zip(row_idx, col_idx):
                   if iou_matrix[m, t] >= self.iou_threshold:
                       matched.append((m, t))
                   else:
                       unmatched_dets.append(m)
                       unmatched_trks.append(t)

               unmatched_dets += [m for m in range(len(detections))
                                  if m not in row_idx]
               unmatched_trks += [t for t in range(len(predicted))
                                  if t not in col_idx]
           else:
               matched = []
               unmatched_dets = list(range(len(detections)))
               unmatched_trks = list(range(len(predicted)))

           # Update matched tracks
           for m, t in matched:
               self.trackers[t].update(detections[m])

           # Create new tracks for unmatched detections
           for m in unmatched_dets:
               self.trackers.append(KalmanBoxTracker(detections[m]))

           # Remove dead tracks
           self.trackers = [t for t in self.trackers
                            if t.time_since_update <= self.max_age]

           # Return confirmed tracks
           results = []
           for trk in self.trackers:
               if trk.hits >= self.min_hits:
                   bbox = trk._state_to_bbox()
                   results.append([*bbox, trk.id])
           return np.array(results) if results else np.empty((0, 5))


Task 4: Run the Tracker on CARLA Vehicles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def get_vehicle_bboxes_2d(world, camera_actor, K):
       """Get 2D bounding boxes for all vehicles visible to a camera."""
       vehicles = world.get_actors().filter('vehicle.*')
       ego_id = vehicle.id
       cam_transform = camera_actor.get_transform()
       world_to_cam = np.array(cam_transform.get_inverse_matrix())

       bboxes = []
       for v in vehicles:
           if v.id == ego_id:
               continue

           # Get vehicle center in world frame
           v_loc = v.get_transform().location
           v_world = np.array([v_loc.x, v_loc.y, v_loc.z, 1.0])

           # Transform to camera frame
           v_cam = world_to_cam @ v_world
           if v_cam[2] < 1.0:  # behind camera
               continue

           # Project to pixel coordinates
           px = K[0, 0] * v_cam[0] / v_cam[2] + K[0, 2]
           py = K[1, 1] * v_cam[1] / v_cam[2] + K[1, 2]

           # Approximate bounding box size based on distance
           half_w = max(30, 2000 / v_cam[2])
           half_h = max(20, 1500 / v_cam[2])

           x1 = max(0, int(px - half_w))
           y1 = max(0, int(py - half_h))
           x2 = min(1280, int(px + half_w))
           y2 = min(720, int(py + half_h))

           if x2 > x1 and y2 > y1:
               bboxes.append([x1, y1, x2, y2])

       return np.array(bboxes) if bboxes else np.empty((0, 4))

   # ── Main tracking loop ────────────────────────────────────────────
   tracker = SORTTracker(max_age=5, min_hits=3, iou_threshold=0.3)
   # Assign unique colors per track ID
   track_colors = {}

   def tracking_callback(image):
       array = np.frombuffer(image.raw_data, dtype=np.uint8)
       frame = array.reshape((image.height, image.width, 4))[:, :, :3].copy()

       detections = get_vehicle_bboxes_2d(world, cameras['front'], K)
       tracks = tracker.update(detections)

       for trk in tracks:
           x1, y1, x2, y2, tid = trk.astype(int)
           if tid not in track_colors:
               track_colors[tid] = tuple(
                   int(c) for c in np.random.randint(50, 255, 3))
           color = track_colors[tid]
           cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
           cv2.putText(frame, f"ID:{tid}", (x1, y1 - 8),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

       cv2.imshow("SORT Tracker", frame)
       cv2.waitKey(1)

   cameras['front'].listen(tracking_callback)

.. admonition:: Exercise Tasks
   :class: tip

   1. **Visualize CARLA semantic segmentation** using the ground-truth camera.
      Identify the driveable surface, lane markings, and vehicle pixels.
   2. **Run the SORT tracker** on CARLA vehicle detections. Observe how track
      IDs are assigned and maintained as vehicles move through the scene.
   3. **Stress-test with occlusion**: Drive through a busy intersection and
      observe ID switches when vehicles occlude each other. Count the number
      of ID switches over 100 frames.
   4. **Implement ByteTrack's two-pass association**: Modify the
      ``SORTTracker.update()`` method to split detections into high-confidence
      and low-confidence sets, run two rounds of Hungarian matching, and
      compare the ID switch count against basic SORT.
   5. **Compute tracking metrics**: Using CARLA's ground-truth vehicle
      positions as reference, compute MOTA and IDF1 for your tracker over
      a 30-second driving sequence.

.. admonition:: Assignment Unlocked -- GP2: Perception -- YOLO vs DETR
   :class: important

   You now have the foundational knowledge from **L3--L5** to begin
   **GP2: Perception -- YOLO vs DETR**. In GP2 you will collect a labeled
   dataset from CARLA, fine-tune both YOLOv8 and RT-DETR, deploy each as a
   ROS 2 perception node, and perform a rigorous comparison across weather
   and lighting conditions.

   :doc:`Go to GP2 </assignments/gp2>`
