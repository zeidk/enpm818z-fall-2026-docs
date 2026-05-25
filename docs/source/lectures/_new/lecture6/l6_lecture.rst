====================================================
Lecture
====================================================


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


Integration with the L4-L5 Pipeline
-------------------------------------

The full perception pipeline for autonomous driving:

.. list-table::
   :widths: 15 85
   :class: compact-table

   * - **L3**
     - State estimation backbone: Kalman filter family + data association
       (used by tracking below) and weighted-averaging fusion for redundant
       sensors.
   * - **L4**
     - Raw sensor inputs → 2D / 3D object detection (LiDAR PointPillars /
       VoxelNet, camera DETR / YOLO) → bounding boxes with class and
       confidence.
   * - **L5 (BEV + Occupancy)**
     - Multi-camera images → BEV feature construction (LSS, BEVFormer) →
       BEV detection heads → 3D boxes or occupancy voxels in ego frame.
   * - **L5 (Segmentation)**
     - Camera images → semantic / panoptic segmentation → driveable
       surface mask, lane lines, free-space boundaries. BEV projection for
       planning.
   * - **L6 (Tracking)**
     - 3D bounding boxes from L4 / L5 → Kalman filter state prediction
       (from L3) → Hungarian / ByteTrack association → confirmed tracks
       with IDs and velocity estimates.
   * - **L6 (Deep Fusion)**
     - LiDAR + camera BEV features → cross-attention / BEVFusion →
       fused BEV representation feeding tracking and downstream tasks.
   * - **Output**
     - Per-object tracks with state history: position, velocity,
       orientation, class, ID. Input to prediction (L9) and planning
       (L10-L11) modules.

.. admonition:: Real-World Performance Trade-offs
   :class: warning

   In production AV systems, tracking must run within a strict latency budget
   (typically <50 ms total for the perception stack). Appearance-based methods
   (DeepSORT) improve ID consistency but add compute. ByteTrack's approach of
   using all detections (not just high-confidence) significantly reduces ID
   switches at negligible compute cost -- a favorable engineering trade-off.


Deep Learning Fusion: Cross-Attention
---------------------------------------

Beyond the classical Kalman / weighted-averaging fusion covered in L3,
modern AV stacks increasingly fuse modalities through **learned
attention mechanisms** -- particularly in BEV space, where the
representation from L5 makes camera and LiDAR features spatially
comparable.

Cross-Attention Fusion
~~~~~~~~~~~~~~~~~~~~~~~

Given LiDAR BEV features :math:`\mathbf{F}_L \in \mathbb{R}^{H \times W \times C}`
and camera BEV features :math:`\mathbf{F}_C \in \mathbb{R}^{H \times W \times C}`:

.. math::

   \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V

   Q = \mathbf{F}_L W_Q, \quad K = \mathbf{F}_C W_K, \quad V = \mathbf{F}_C W_V

The LiDAR features **query** the camera features -- each LiDAR BEV cell
attends to the most relevant camera BEV cells, learning to weight
semantic camera information based on geometric LiDAR context.

BEVFusion (MIT) Example
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **Camera branch**
     - LSS-based camera-to-BEV transform → camera BEV features
   * - **LiDAR branch**
     - Voxel encoder → sparse 3D conv → BEV feature map
   * - **Fusion**
     - Concatenate camera + LiDAR BEV features → channel fusion conv
   * - **Output**
     - Fused BEV features → detection/segmentation heads

Performance on nuScenes: 70.2 NDS vs. 65.0 for LiDAR-only -- camera
fusion adds semantic richness that improves small object detection.

.. note::

   Cross-attention fusion sits *downstream* of the BEV construction
   covered in L5. The tracker (Tasks above) consumes whatever object
   detections come out of this fused BEV -- the better the fusion, the
   cleaner the input to MOT.


Summary
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Tracking
      :class-card: sd-border-primary

      - MOT paradigm: tracking-by-detection
      - SORT: Kalman filter + IoU Hungarian matching
      - DeepSORT: adds appearance embedding for re-ID
      - ByteTrack: uses low-confidence detections for occlusion recovery
      - Metrics: MOTA (accuracy), IDF1 (identity), HOTA (balanced)

   .. grid-item-card:: Temporal & Deep Fusion
      :class-card: sd-border-primary

      - Temporal context: motion, occlusion, intent
      - Tracking-by-detection vs end-to-end transformer MOT
      - Cross-attention fusion of camera + LiDAR BEV features
      - BEVFusion: concatenate-then-conv vs. attention-based fusion


CARLA Hands-On: Multi-Object Tracking
--------------------------------------------------

This exercise implements a basic SORT tracker on CARLA vehicle
detections, relying on the Kalman filter taught in L3 and consuming
detection outputs from L4 / L5.


Task 1: Implement a Basic SORT Tracker
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


Task 2: Run the Tracker on CARLA Vehicles
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
