====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 6: Perception III --
Tracking, Temporal Reasoning & Deep Fusion. Topics include multi-object
tracking (SORT, DeepSORT, ByteTrack); track lifecycle management;
tracking metrics (MOTA, MOTP, IDF1); temporal reasoning for improved
perception; and deep-learning fusion (cross-attention, BEVFusion).

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-10)
=================================

.. admonition:: Question 1
   :class: hint

   In a tracking-by-detection system, how is a new track typically promoted
   from **tentative** to **confirmed**, and when is a track **deleted**?

   A. A track is confirmed after a single detection and deleted after a
      single missed frame.

   B. A track is confirmed once it is matched to detections for several
      consecutive frames, and deleted after it goes unmatched for more than
      a set number of frames (``max_age``).

   C. Tracks are never deleted; they persist for the entire sequence.

   D. Confirmation and deletion are decided by the detector confidence alone,
      independent of matching history.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A track is confirmed once it is matched to detections for several
   consecutive frames, and deleted after it goes unmatched for more than a set
   number of frames (``max_age``).

   Track lifecycle management avoids reacting to spurious single-frame
   detections (require ``n_init`` consecutive hits to confirm) and tolerates
   short occlusions (keep coasting a track on Kalman prediction until
   ``max_age`` misses accumulate, then delete it).


.. admonition:: Question 2
   :class: hint

   The **MOTP** (Multi-Object Tracking Precision) metric measures:

   A. The fraction of ground-truth objects that were tracked without any
      ID switch.

   B. The average localization accuracy (e.g., IoU or distance error) of the
      matched track-detection pairs.

   C. The number of false positives per frame.

   D. The ratio of confirmed tracks to tentative tracks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The average localization accuracy (e.g., IoU or distance error)
   of the matched track-detection pairs.

   MOTP captures *how precisely* matched objects are localized, independent of
   how many are detected. It is complementary to MOTA (which counts FN, FP, and
   ID switches): a tracker can have high MOTA but mediocre MOTP if boxes are
   consistently matched but loosely localized.


.. admonition:: Question 3
   :class: hint

   Why is a shared **BEV feature space** an effective representation for deep
   **LiDAR-camera fusion**?

   A. It discards camera features and keeps only LiDAR points.

   B. It removes the need for extrinsic calibration between the sensors.

   C. Both modalities can be projected into the same top-down metric grid,
      where their features are spatially aligned and can be combined per cell.

   D. It converts LiDAR points into RGB images so a 2D CNN can process them.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Both modalities can be projected into the same top-down metric
   grid, where their features are spatially aligned and can be combined per
   cell.

   LiDAR provides accurate geometry and camera provides dense semantics. A
   shared BEV grid gives a common, metric, ego-centered coordinate frame in
   which a camera BEV feature and a LiDAR BEV feature for the same location
   line up, so they can be concatenated or fused with attention per cell.


.. admonition:: Question 4
   :class: hint

   In the **SORT** tracker, how are detections in a new frame associated with
   existing tracks?

   A. By comparing appearance embeddings (CNN features) from each detection
      and track.

   B. By using a Kalman filter to predict track positions and then solving a
      bipartite matching problem minimizing IoU distance via the Hungarian
      algorithm.

   C. By computing optical flow between frames and linking detections along
      flow vectors.

   D. By comparing 3D LiDAR point cloud segments across frames.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- By using a Kalman filter to predict track positions and then
   solving a bipartite matching problem minimizing IoU distance via the
   Hungarian algorithm.

   SORT propagates each track's state (position, velocity) forward with a
   Kalman filter to predict where it should be in the new frame. It then
   constructs an IoU-based cost matrix between predicted track boxes and new
   detections, and solves the optimal assignment with the Hungarian algorithm.


.. admonition:: Question 5
   :class: hint

   What key limitation of SORT does **DeepSORT** address?

   A. SORT cannot run in real time on embedded hardware.

   B. SORT fails at long-range detection because it uses only IoU for matching
      and has no appearance model to re-identify objects after occlusion.

   C. SORT cannot handle more than 10 simultaneous tracks.

   D. SORT requires LiDAR input and cannot process camera-only data.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- SORT fails at long-range detection because it uses only IoU for
   matching and has no appearance model to re-identify objects after occlusion.

   When an object is occluded, SORT's track dies (no IoU match available).
   When the object reappears, SORT assigns a new ID -- an "ID switch." DeepSORT
   addresses this by maintaining a CNN-based appearance embedding gallery per
   track, enabling re-identification based on visual similarity even after
   long occlusions.


.. admonition:: Question 6
   :class: hint

   **ByteTrack's** key innovation over SORT/DeepSORT is:

   A. Using a Transformer-based detector instead of YOLO.

   B. Performing a second association pass that matches low-confidence
      detections to unmatched tracks, recovering occluded objects.

   C. Replacing the Kalman filter with an LSTM for state prediction.

   D. Running tracking in BEV space instead of image space.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Performing a second association pass that matches low-confidence
   detections to unmatched tracks, recovering occluded objects.

   ByteTrack observes that occluded objects often produce low-confidence
   (but valid) detections that SORT/DeepSORT discard. ByteTrack first
   associates high-confidence detections, then in a second pass associates
   remaining (unmatched) tracks with low-confidence detections, significantly
   reducing ID switches at essentially zero additional compute.


.. admonition:: Question 7
   :class: hint

   The **MOTA** (Multi-Object Tracking Accuracy) metric penalizes which three
   types of errors?

   A. False positives, false negatives, and localization errors.

   B. False positives, false negatives, and ID switches.

   C. ID switches, localization errors, and classification errors.

   D. False negatives, velocity errors, and ID switches.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- False positives, false negatives, and ID switches.

   MOTA = 1 - (FN + FP + IDSW) / GT. It penalizes all three error types:
   missed detections (FN), spurious detections (FP), and identity switches
   (IDSW) where a track's ID changes on the same object. MOTA does NOT
   penalize localization errors -- that is captured by MOTP.


.. admonition:: Question 8
   :class: hint

   In **BEVFusion**'s cross-attention fusion, what role do the LiDAR BEV
   features play in the attention mechanism?

   A. They serve as Values (V) -- providing the content that is read out.

   B. They serve as Queries (Q) -- asking "what camera features are relevant
      to this spatial location?"

   C. They serve as Keys (K) -- indexing which camera features to attend to.

   D. They are not used in the attention; only camera features are fused.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- They serve as Queries (Q) -- asking "what camera features are
   relevant to this spatial location?"

   In cross-attention fusion: LiDAR BEV features → Q (queries); Camera BEV
   features → K (keys) and V (values). The LiDAR features "query" the
   camera features: for each LiDAR BEV cell (which knows geometry), the
   attention mechanism selectively retrieves relevant semantic information
   from the camera BEV. This is directional fusion where geometry guides
   semantic information retrieval.


.. admonition:: Question 9
   :class: hint

   Why is the **IDF1** metric preferred over MOTA for evaluating tracking
   algorithms in autonomous driving applications?

   A. IDF1 is faster to compute than MOTA.

   B. IDF1 focuses on ID consistency over time, which is critical for
      trajectory prediction -- knowing it is the same car across frames
      matters more than counting detections.

   C. IDF1 penalizes localization errors more strictly than MOTA.

   D. IDF1 requires no ground-truth annotations.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- IDF1 focuses on ID consistency over time, which is critical for
   trajectory prediction -- knowing it is the same car across frames matters
   more than counting detections.

   MOTA is dominated by detection quality (FP/FN). A tracker with many ID
   switches can still achieve high MOTA if the detector is good. For
   downstream prediction, consistent IDs are essential -- the predictor must
   know it is tracking the same pedestrian over 2 seconds. IDF1 directly
   measures this identity consistency.


.. admonition:: Question 10
   :class: hint

   Which approach for **temporal reasoning** in autonomous driving is most
   commonly used in production BEV perception stacks?

   A. 3D convolutions over a video volume (C3D, SlowFast).

   B. LSTM hidden state over flattened image features.

   C. Warping the previous BEV feature map to the current ego frame using
      ego-motion and computing temporal cross-attention.

   D. Optical flow estimation between consecutive camera frames.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Warping the previous BEV feature map to the current ego frame
   using ego-motion and computing temporal cross-attention.

   BEVFormer's temporal self-attention is the dominant approach in modern
   production-adjacent stacks. It uses known ego-motion (from odometry/
   localization) to spatially align previous BEV features with the current
   frame, then applies attention to selectively integrate temporal information.
   This is efficient, interpretable, and achieves large gains (+4-7 NDS).


----


True or False (Questions 11-15)
================================

.. admonition:: Question 11
   :class: hint

   **True or False:** MOTP measures the localization precision of matched
   track-detection pairs, while MOTA measures detection and identity errors;
   the two metrics are complementary.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   MOTP answers "how precisely are the matched objects localized?" (average
   IoU or distance error of matches), while MOTA answers "how many objects
   were missed, hallucinated, or swapped?" (FN + FP + IDSW). A complete
   tracking evaluation reports both, since a tracker can score well on one and
   poorly on the other.


.. admonition:: Question 12
   :class: hint

   **True or False:** The Kalman filter used inside a SORT tracker typically
   assumes a constant-velocity motion model for each object.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   SORT models each track with a linear constant-velocity Kalman filter (state
   includes box center, scale, aspect ratio, and their velocities). Between
   frames it predicts the box forward assuming constant velocity; the IoU
   matching then corrects the estimate. The constant-velocity assumption is
   why fast maneuvers and long occlusions cause the prediction to drift.


.. admonition:: Question 13
   :class: hint

   **True or False:** SORT uses a deep convolutional neural network to
   compute appearance embeddings for matching detections to tracks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   SORT does NOT use appearance embeddings. Its matching relies solely on
   IoU between predicted bounding boxes (from the Kalman filter) and new
   detections, solved via the Hungarian algorithm. Appearance embeddings
   were introduced in DeepSORT, which is the extension of SORT that adds
   a CNN-based re-identification module.


.. admonition:: Question 14
   :class: hint

   **True or False:** In BEVFusion, LiDAR and camera features are combined in
   a shared bird's-eye-view representation rather than being concatenated at
   the raw sensor level.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   BEVFusion transforms both the camera features (via a view transform such as
   LSS) and the LiDAR features into a common BEV grid, then fuses them there.
   Fusing in a shared, spatially-aligned BEV space is what makes the fusion
   robust to calibration noise and lets a single downstream head consume both
   modalities.


.. admonition:: Question 15
   :class: hint

   **True or False:** In the tracking-by-detection paradigm, the detector
   and tracker are trained jointly end-to-end to optimize tracking performance
   directly.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   In tracking-by-detection, the detector and tracker are completely
   independent modules. The detector is trained separately (often on static
   image datasets) and produces detection outputs. The tracker then processes
   these outputs to maintain object identities. This modularity allows
   improving either component independently but means the detector is not
   optimized for tracking.


----


Essay Questions (Questions 16-18)
===================================

.. admonition:: Question 16
   :class: hint

   **Compare SORT, DeepSORT, and ByteTrack** in terms of their key design
   choices, strengths, and weaknesses. Which would you choose for a
   production AV system and why?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - SORT: Kalman filter + IoU Hungarian matching. Extremely fast (260 Hz),
     minimal compute. Weakness: no appearance model, poor re-ID after
     occlusion, frequent ID switches in crowded scenes.
   - DeepSORT: adds CNN appearance embedding gallery. Improves re-ID but
     adds compute (CNN inference per detection crop) and requires a
     separate re-ID training dataset.
   - ByteTrack: uses all detections (high + low confidence) in two-pass
     association. Matches SORT speed with significantly fewer ID switches.
     No appearance model needed.
   - For production AV: ByteTrack or ByteTrack + lightweight appearance
     model is the best trade-off -- low latency, robust to occlusion, no
     re-ID dataset dependency. DeepSORT suits pedestrian-heavy scenarios
     where re-ID matters most.


.. admonition:: Question 17
   :class: hint

   **Explain the difference between MOTA and IDF1 as tracking metrics.**
   Give a concrete example where a tracker with high MOTA has poor IDF1,
   and explain why IDF1 matters for autonomous driving.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - MOTA = 1 - (FN + FP + IDSW) / GT. It is dominated by detection
     quality -- a perfect detector with frequent ID switches can achieve
     high MOTA.
   - IDF1 measures F1 score for correct identity assignments across the
     full track lifetime, directly measuring ID consistency.
   - Concrete example: a tracker that detects every vehicle correctly
     (zero FP/FN) but switches the ID of Vehicle A and Vehicle B at every
     occlusion would have MOTA near 1.0 but IDF1 near 0.5.
   - For AV: downstream prediction modules track a vehicle's trajectory
     to predict where it will be in 3 seconds. If IDs switch frequently,
     the predictor mixes trajectories of different vehicles -- producing
     catastrophically wrong predictions. High IDF1 is therefore safety-critical.


.. admonition:: Question 18
   :class: hint

   **Describe three ways that temporal reasoning improves perception quality**
   in autonomous driving beyond what a single-frame detector can provide.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Velocity estimation: observing the same object across multiple frames
     provides direct velocity measurements via state propagation (Kalman
     filter) or feature-level optical flow. Single frames provide no velocity.
   - Occlusion handling: an object invisible in frame t was visible in frame
     t-1. A temporal model (tracker, temporal BEV attention) can propagate
     the estimated state through the occlusion window, maintaining awareness
     of the object.
   - Noise suppression: random detection noise is temporally uncorrelated.
     Averaging estimates over multiple frames (or Kalman filter smoothing)
     reduces variance in position and classification confidence, while true
     object signals are correlated across frames and survive averaging.
   - Additionally: attribute estimation (classification confidence improves
     with multiple views of the same object from different angles as the
     vehicle moves).
