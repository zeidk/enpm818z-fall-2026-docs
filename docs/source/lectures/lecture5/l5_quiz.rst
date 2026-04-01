====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 5: Perception III --
Segmentation, Tracking & Temporal Reasoning. Topics include semantic,
instance, and panoptic segmentation; U-Net and DeepLabv3+; multi-object
tracking (SORT, DeepSORT, ByteTrack); tracking metrics (MOTA, MOTP, IDF1);
and temporal reasoning for improved perception.

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

   Which segmentation task assigns a unique instance ID to each individual
   object AND provides a label for every pixel in the image (including
   background "stuff" regions)?

   A. Semantic segmentation

   B. Instance segmentation

   C. Panoptic segmentation

   D. Binary segmentation

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Panoptic segmentation

   Panoptic segmentation unifies semantic and instance segmentation. Every
   pixel receives a class label (like semantic segmentation), and every
   "thing" (countable object like a car or pedestrian) also receives a unique
   instance ID. "Stuff" regions (road, sky) get class labels but no instance
   IDs.


.. admonition:: Question 2
   :class: hint

   What is the primary architectural innovation of **U-Net** that allows it
   to produce high-resolution segmentation masks?

   A. Atrous (dilated) convolutions at multiple dilation rates.

   B. Skip connections that concatenate encoder feature maps with decoder
      feature maps at the same resolution.

   C. A Region Proposal Network that identifies candidate object locations.

   D. A deformable attention mechanism over learned reference points.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Skip connections that concatenate encoder feature maps with decoder
   feature maps at the same resolution.

   U-Net's encoder progressively downsamples the input to extract
   high-level semantic features, while the decoder upsamples back to full
   resolution. The skip connections from encoder to decoder at matching
   resolutions provide fine-grained spatial detail (edges, boundaries) that
   would otherwise be lost during downsampling.


.. admonition:: Question 3
   :class: hint

   In **DeepLabv3+**, what is the purpose of Atrous Spatial Pyramid Pooling
   (ASPP)?

   A. To extract region proposals for instance segmentation.

   B. To apply dilated convolutions at multiple rates in parallel, capturing
      multi-scale contextual information in a single forward pass.

   C. To warp features from previous frames using ego-motion.

   D. To perform bilinear interpolation for upsampling the feature map.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To apply dilated convolutions at multiple rates in parallel,
   capturing multi-scale contextual information in a single forward pass.

   ASPP uses several parallel dilated convolutional branches with different
   dilation rates (e.g., 6, 12, 18) plus global average pooling. Each branch
   captures context at a different scale without reducing spatial resolution.
   The outputs are concatenated and passed to the decoder.


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

   Which segmentation architecture adds a **mask prediction head** to a
   two-stage detector framework to produce instance-level binary masks?

   A. U-Net

   B. DeepLabv3+

   C. Mask R-CNN

   D. SegNet

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Mask R-CNN

   Mask R-CNN extends Faster R-CNN by adding a third head alongside the
   classification and bounding box regression heads. For each detected region
   proposal, this mask head predicts a 28x28 binary mask per class using a
   small FCN. RoIAlign (instead of RoIPool) ensures pixel-precise feature
   alignment for accurate mask prediction.


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
   commonly used in production BEV perception stacks (as covered in L4)?

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

   **True or False:** In semantic segmentation, two pedestrians standing
   next to each other will receive different instance IDs but the same
   class label.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Semantic segmentation only assigns class labels -- it has no concept of
   instances. Both pedestrians would receive the class label "pedestrian"
   but NO instance IDs. Differentiating individual instances requires
   instance segmentation or panoptic segmentation.


.. admonition:: Question 12
   :class: hint

   **True or False:** U-Net's skip connections are the primary mechanism
   that allows the network to recover fine spatial detail that is lost
   during encoding (downsampling).

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   During encoding, spatial resolution is progressively reduced (via max
   pooling or strided convolutions) to build high-level semantic features.
   Skip connections directly copy encoder feature maps at each resolution
   to the corresponding decoder level, bypassing the bottleneck. This
   allows the decoder to combine high-level semantics (from the bottleneck)
   with fine spatial detail (from the encoder skip).


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

   **True or False:** The Panoptic Quality (PQ) metric can be decomposed
   into a recognition quality component and a segmentation quality component.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   PQ = RQ * SQ, where:
   RQ (Recognition Quality) = TP / (TP + 0.5*FP + 0.5*FN) measures how
   well the model detects objects (like F1 score).
   SQ (Segmentation Quality) = average IoU of matched pairs measures how
   well the masks are segmented.
   This decomposition allows analysis of whether errors come from missed
   detections or poor mask quality.


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
