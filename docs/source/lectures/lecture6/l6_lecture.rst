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
     - Average localization quality over matched pairs, where :math:`c_t`
       is the number of matches at time :math:`t`. **Read the definition
       of** :math:`d_t^i` **before interpreting it:** if it is a distance
       error, lower is better; if it is IoU overlap (the MOTChallenge
       convention), higher is better. The two conventions are both in
       common use and are reported as the same metric name.
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


End-to-End Transformer MOT
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tracking-by-detection treats association as a separate, hand-designed
step. **Transformer MOT** dissolves that boundary the same way DETR
dissolved NMS in L4: by making association an emergent property of
attention rather than an algorithm bolted on afterwards.

.. tab-set::

   .. tab-item:: TrackFormer (2022)

      Extends DETR with **track queries**. Alongside DETR's usual object
      queries (which spawn new tracks), each existing track carries its
      own query forward from the previous frame. That query attends to
      the current frame's features and directly outputs the object's new
      position -- keeping its identity implicitly, with no IoU matrix and
      no Hungarian algorithm at inference.

   .. tab-item:: MOTR (2022)

      Similar track-query concept, with the focus on end-to-end temporal
      modelling: queries are updated across a whole video clip during
      training, so the network learns long-term association behaviour
      rather than just frame-to-frame matching.

   .. tab-item:: Why it has not taken over

      Two practical obstacles keep tracking-by-detection dominant in
      production. First, **detection dominates the metrics**: ByteTrack
      with a strong detector still beats most end-to-end trackers on
      MOTA, because a better detector helps immediately while an
      end-to-end tracker must relearn everything. Second, **modularity
      is worth a lot** -- a separable detector and tracker can be
      validated, profiled, and swapped independently, which matters
      enormously for the safety case in L14.

.. admonition:: The recurring pattern
   :class: tip

   You have now seen the same architectural move three times: DETR
   replaced NMS with learned set prediction (L4), BEVFormer replaced
   geometric projection with learned attention (L5), and TrackFormer
   replaces the Hungarian algorithm with learned queries. In each case a
   hand-designed combinatorial step becomes a learned one -- and in each
   case adoption depends on whether the learned version is worth giving
   up the modularity.


3D Multi-Object Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~

Everything above tracks boxes in the **image plane**. A planner cannot
use that: it needs objects tracked in metric space, which is what L4's 3-D
detectors and L5's BEV representation produce. Fortunately the algorithm
barely changes -- the state vector does.

.. list-table::
   :widths: 22 39 39
   :header-rows: 1
   :class: compact-table

   * - Aspect
     - 2D image tracking
     - 3D / BEV tracking
   * - State
     - :math:`[c_x, c_y, s, r, \dot{c}_x, \dot{c}_y, \dot{s}]`
     - :math:`[x, y, z, \theta, l, w, h, \dot{x}, \dot{y}, \dot{z}]`
   * - Association metric
     - IoU between 2-D boxes
     - 3-D/BEV IoU, or centre distance, or Mahalanobis
   * - Motion model
     - Constant velocity in pixels (breaks under ego motion)
     - Constant velocity in **world** coordinates
   * - Ego motion
     - Confounds everything
     - Compensated using the L7 pose estimate

.. admonition:: Ego-motion compensation is the key difference
   :class: important

   In image space, a parked car "moves" whenever the ego vehicle does,
   so the constant-velocity model is fitting the wrong thing entirely.
   In 3-D you transform tracks into a **world or map frame** using the
   ego pose from L7, and then a parked car has genuinely zero velocity.
   The motion model finally matches reality, and tracking through
   occlusion improves dramatically as a result.

**AB3DMOT** (Weng et al., 2020) is the standard baseline and is
deliberately minimal: a 3-D Kalman filter with a constant-velocity model
plus greedy 3-D IoU association -- essentially SORT lifted into 3-D. Its
lesson mirrors ByteTrack's: with good detections, a simple tracker is
hard to beat. **CenterPoint** (L4) goes further and has the detector
regress per-object velocity directly, so association becomes little more
than matching predicted to detected centres.


Integration with the Perception Pipeline
------------------------------------------

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

On the nuScenes detection benchmark, BEVFusion improves clearly over a
LiDAR-only baseline of the same design -- camera features add semantic
richness that particularly helps small and distant objects. Consult the
paper for current figures and be careful to compare val against val: the
reported numbers differ by several NDS points between the validation and
test splits, and between the MIT and Peking University papers that share
the name "BEVFusion."

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

      - Temporal context: motion, occlusion, noise averaging
      - Transformer MOT (TrackFormer, MOTR): track queries replace the
        Hungarian step, but modularity keeps tracking-by-detection ahead
      - 3D/BEV tracking: same filter, world-frame state, ego-motion
        compensated (AB3DMOT, CenterPoint)
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
       """Kalman filter tracker for a single bounding box.

       This is a real KF, using the machinery from L3: a state vector
       with an explicit covariance P, a process model (F, Q), and a
       measurement model (H, R). The covariance is the whole point --
       it is what lets the tracker express "I have not seen this object
       for four frames, so I am no longer confident where it is," which
       in turn is what makes gating and association work.

       State (SORT's parameterization, Bewley et al. 2016):
           x = [cx, cy, s, r, vx, vy, vs]^T
       where s is box AREA and r is aspect ratio (assumed constant, so
       it has no velocity term).
       """
       _count = 0

       def __init__(self, bbox, dt=1.0):
           self.id = KalmanBoxTracker._count
           KalmanBoxTracker._count += 1

           # --- Process model: constant velocity in (cx, cy, s) ---
           self.F = np.eye(7)
           self.F[0, 4] = dt      # cx += vx * dt
           self.F[1, 5] = dt      # cy += vy * dt
           self.F[2, 6] = dt      # s  += vs * dt

           # --- Measurement model: we observe (cx, cy, s, r) ---
           self.H = np.zeros((4, 7))
           self.H[:4, :4] = np.eye(4)

           # --- Noise. These are the tuning knobs. ---
           # R: detector noise. Area is measured far less reliably than
           # the centre, so it gets a much larger variance.
           self.R = np.diag([1.0, 1.0, 10.0, 0.01])
           # Q: how much we distrust constant velocity. Velocities are
           # unobserved at init, so give them large process noise.
           self.Q = np.diag([1.0, 1.0, 1.0, 0.01, 0.01, 0.01, 0.0001])

           # --- Initial state and covariance ---
           z = self._bbox_to_z(bbox)
           self.x = np.zeros(7)
           self.x[:4] = z
           self.P = np.diag([10., 10., 10., 10., 1000., 1000., 1000.])
           # Huge variance on the velocity block: after ONE detection we
           # genuinely have no idea how fast the object is moving, and
           # saying so lets the second detection dominate the estimate.

           self.hits = 1
           self.age = 0
           self.time_since_update = 0

       @staticmethod
       def _bbox_to_z(bbox):
           """[x1,y1,x2,y2] -> [cx, cy, area, aspect]."""
           w = max(bbox[2] - bbox[0], 1e-6)
           h = max(bbox[3] - bbox[1], 1e-6)
           return np.array([bbox[0] + w / 2, bbox[1] + h / 2, w * h, w / h])

       def predict(self):
           """KF predict step."""
           self.x = self.F @ self.x
           self.P = self.F @ self.P @ self.F.T + self.Q
           # Area must stay positive after prediction
           if self.x[2] <= 0:
               self.x[2] = 1e-6
           self.age += 1
           self.time_since_update += 1
           return self.to_bbox()

       def update(self, bbox):
           """KF update step with a matched detection."""
           z = self._bbox_to_z(bbox)
           y = z - self.H @ self.x                    # innovation
           S = self.H @ self.P @ self.H.T + self.R    # innovation covariance
           K = self.P @ self.H.T @ np.linalg.inv(S)   # Kalman gain
           self.x = self.x + K @ y

           # Joseph form -- keeps P symmetric positive-definite (see L3)
           I_KH = np.eye(7) - K @ self.H
           self.P = I_KH @ self.P @ I_KH.T + K @ self.R @ K.T

           self.hits += 1
           self.time_since_update = 0

       def mahalanobis(self, bbox):
           """Gating distance from L3 -- uses the covariance, unlike IoU."""
           z = self._bbox_to_z(bbox)
           y = z - self.H @ self.x
           S = self.H @ self.P @ self.H.T + self.R
           return float(np.sqrt(y.T @ np.linalg.inv(S) @ y))

       def to_bbox(self):
           """Convert state back to [x1, y1, x2, y2]."""
           cx, cy, s, r = self.x[:4]
           s = max(s, 1e-6)
           r = max(r, 1e-6)
           w = np.sqrt(s * r)
           h = s / w
           return np.array([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2])

.. admonition:: Why this must be a Kalman filter and not a moving average
   :class: important

   An exponential moving average can smooth a track, but it has no
   notion of **uncertainty**. That costs you three things SORT depends
   on:

   1. **Occlusion handling.** During a gap, :math:`P` grows through the
      predict step, so the tracker automatically becomes more willing to
      accept a re-detection that has drifted. A moving average has a
      fixed implicit trust level forever.
   2. **Principled gating.** The Mahalanobis distance above scales the
      residual by :math:`S`, so a confident track rejects distant
      matches while an uncertain one accepts them. A fixed IoU threshold
      cannot adapt.
   3. **Correct initialization.** Setting velocity variance to 1000 at
      birth means the second detection essentially defines the velocity.
      A moving average with :math:`\alpha = 0.7` would instead spend
      several frames crawling toward the truth.

   This is exactly the L3 machinery -- same predict/update cycle, same
   Joseph-form covariance update -- applied per track.

.. code-block:: python

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
                   bbox = trk.to_bbox()
                   results.append([*bbox, trk.id])
           return np.array(results) if results else np.empty((0, 5))


Task 2: Run the Tracker on CARLA Vehicles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important::

   **Track real detections, not ground truth.** It is tempting to feed
   the tracker CARLA's actor list, but that defeats the exercise: ground
   truth never misses an object, never produces a false positive, never
   occludes, and carries **no confidence score** -- so there would be
   nothing for the tracker to fix and no way to attempt ByteTrack's
   two-tier association in Task 4.

   Use the YOLO detector from L4. Ground truth still has a role, but as
   the *reference* against which you score MOTA and IDF1 in Task 5 --
   not as the tracker's input.

.. code-block:: python

   from ultralytics import YOLO

   detector = YOLO('yolov8s.pt')          # or your GP2 fine-tuned model
   VEHICLE_CLASSES = {1, 2, 3, 5, 7}      # COCO: bicycle, car, motorcycle,
                                          #       bus, truck

   def detect_vehicles(frame_bgr, conf_threshold=0.1):
       """Run YOLO and return boxes WITH confidence scores.

       Note the low threshold: ByteTrack needs the low-confidence
       detections that a conventional 0.5 cutoff would discard, so we
       keep them and let the tracker decide.
       """
       results = detector(frame_bgr, verbose=False, conf=conf_threshold)[0]

       dets = []
       for box in results.boxes:
           if int(box.cls[0]) not in VEHICLE_CLASSES:
               continue
           x1, y1, x2, y2 = box.xyxy[0].tolist()
           dets.append([x1, y1, x2, y2, float(box.conf[0])])

       return np.array(dets) if dets else np.empty((0, 5))

   # ── Main tracking loop ────────────────────────────────────────────
   tracker = SORTTracker(max_age=5, min_hits=3, iou_threshold=0.3)
   track_colors = {}

   def tracking_callback(image):
       array = np.frombuffer(image.raw_data, dtype=np.uint8)
       # CARLA delivers BGRA; slicing to 3 channels gives BGR, which is
       # what both YOLO and cv2 expect. Do not convert to RGB here.
       frame = array.reshape((image.height, image.width, 4))[:, :, :3].copy()

       dets = detect_vehicles(frame)              # (M, 5): box + score

       # Basic SORT ignores the score column; ByteTrack (Task 4) uses it.
       tracks = tracker.update(dets[:, :4] if len(dets) else dets)

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

.. note::

   For **Task 5** you need ground-truth boxes as a reference. Project
   each vehicle actor's ``bounding_box`` vertices into the image using
   the UE-to-optical permutation from L2 (projecting only the actor
   *centre*, and guessing a box size from range, gives boxes too
   inaccurate to score against). Then match tracks to ground truth by
   IoU per frame and count false negatives, false positives, and
   identity switches to assemble MOTA.

.. admonition:: Exercise Tasks
   :class: tip

   1. **Run the SORT tracker** on live YOLO detections. Observe how track
      IDs are assigned and maintained as vehicles move through the scene.
   2. **Inspect the covariance**: Print ``np.trace(trk.P)`` for one track
      each frame. Watch it grow while the object is occluded and collapse
      when a detection re-associates. This is the behaviour a moving
      average cannot reproduce.
   3. **Stress-test with occlusion**: Drive through a busy intersection and
      observe ID switches when vehicles occlude each other. Count the number
      of ID switches over 100 frames.
   4. **Implement ByteTrack's two-pass association**: Modify
      ``SORTTracker.update()`` to split detections at
      :math:`\tau_{high} = 0.6`, match the high-confidence set to all
      tracks first, then match the low-confidence set to whatever tracks
      remain unmatched. Compare the ID-switch count against basic SORT.
   5. **Swap IoU for Mahalanobis gating**: Use ``trk.mahalanobis(det)``
      to reject implausible pairings before the Hungarian step (a
      :math:`\chi^2` gate at 4 degrees of freedom, 95%, is about 9.49).
      Does it help most where boxes are small and IoU is brittle?
   6. **Compute tracking metrics**: Using CARLA's ground-truth vehicle
      boxes as reference, compute MOTA and IDF1 for your tracker over
      a 30-second driving sequence.

.. admonition:: Assignment Unlocked -- GP2: Perception
   :class: important

   You now have the foundational knowledge from **L4--L6** to begin
   **GP2: Perception**. In GP2 you will collect a labeled dataset from
   CARLA, fine-tune both YOLOv8 and RT-DETR, deploy each as a ROS 2
   perception node, add the tracker from this lecture, and perform a
   rigorous comparison across weather and lighting conditions.

   :doc:`Go to GP2 </assignments/gp2>`
