====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 5: Perception II -- BEV,
Occupancy & Segmentation. Topics include the motivation for BEV
representations, Lift-Splat-Shoot, BEVFormer, 3D occupancy networks, and
semantic / instance / panoptic segmentation (U-Net, DeepLabv3+, Mask R-CNN,
Panoptic Quality).

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

   Which of the following best describes why **Bird's-Eye View (BEV)** is
   preferred for autonomous driving planning over perspective camera images?

   A. BEV requires less compute than perspective images.

   B. BEV preserves metric distances and object sizes, directly matching the
      coordinate system used by motion planners.

   C. BEV images can be captured directly by a single wide-angle camera.

   D. BEV eliminates the need for sensor calibration.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- BEV preserves metric distances and object sizes, directly matching
   the coordinate system used by motion planners.

   In perspective images, depth is ambiguous and object sizes decrease with
   distance. BEV places all objects in a metric top-down map where distances
   and sizes are consistent -- directly compatible with path planning,
   trajectory prediction, and control modules.


.. admonition:: Question 2
   :class: hint

   In the **Lift-Splat-Shoot** (LSS) pipeline, what does the **Lift** stage do?

   A. Converts a 3D voxel grid to a 2D BEV feature map.

   B. Applies a detection head to the BEV feature map.

   C. Predicts a depth distribution per pixel and creates a 3D frustum of
      features for each camera.

   D. Warps the previous frame's BEV features to the current ego frame.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Predicts a depth distribution per pixel and creates a 3D frustum
   of features for each camera.

   The Lift stage takes the 2D image feature map and, for each pixel, predicts
   a softmax distribution over discrete depth bins. Each pixel's feature is
   weighted by its depth probabilities and replicated along the camera ray,
   creating a 3D frustum (a tensor of shape D x H x W x C per camera).


.. admonition:: Question 3
   :class: hint

   In **BEVFormer**, what is the role of **Spatial Cross-Attention**?

   A. It warps previous BEV frames into the current ego coordinate frame.

   B. It fuses BEV features from LiDAR and camera modalities.

   C. It allows each BEV query to attend to relevant features in all camera
      images by projecting 3D reference points onto image planes.

   D. It compresses the 3D voxel grid into a 2D BEV by max-pooling along Z.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It allows each BEV query to attend to relevant features in all
   camera images by projecting 3D reference points onto image planes.

   For each BEV grid cell query, BEVFormer samples several 3D reference points
   at different heights, projects them into each camera image using calibration
   parameters, and samples image features at those projected locations via
   deformable attention. This provides geometry-guided feature aggregation
   across all cameras.


.. admonition:: Question 4
   :class: hint

   A 3D Occupancy Network outputs which of the following?

   A. A set of 3D bounding boxes with class labels.

   B. A 2D semantic segmentation map in the camera image plane.

   C. A per-voxel semantic label across a 3D volume around the vehicle.

   D. A depth map for each camera in the rig.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- A per-voxel semantic label across a 3D volume around the vehicle.

   Occupancy networks divide the scene into a 3D voxel grid and assign each
   voxel a semantic class (free, vehicle, pedestrian, vegetation, etc.) plus
   an unknown/occluded category. This dense representation captures arbitrary
   scene geometry that cannot be represented by bounding boxes.


.. admonition:: Question 5
   :class: hint

   Which of the following scenarios is **best handled by a 3D occupancy
   network** rather than a standard 3D bounding box detector?

   A. Counting the exact number of vehicles in a parking lot.

   B. Detecting and tracking traffic lights at intersections.

   C. Navigating a construction zone with irregular barriers and debris.

   D. Classifying pedestrian gestures at a crosswalk.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Navigating a construction zone with irregular barriers and debris.

   Bounding box detectors assume rectangular box shapes for all objects.
   Construction barriers, debris piles, and irregular obstacles do not fit
   this assumption. Occupancy networks capture arbitrary geometry per voxel,
   making them far more suitable for construction zones and novel obstacle
   shapes.


.. admonition:: Question 6
   :class: hint

   In BEV multi-camera fusion, why is **extrinsic calibration** so critical?

   A. It determines the resolution of each camera image.

   B. It controls the field of view overlap between adjacent cameras.

   C. It maps each camera's 3D frustum features into the correct position in
      the shared ego-vehicle BEV grid -- errors cause spatial misalignment
      and ghost detections.

   D. It sets the depth bin resolution for the LSS depth distribution.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It maps each camera's 3D frustum features into the correct
   position in the shared ego-vehicle BEV grid -- errors cause spatial
   misalignment and ghost detections.

   BEV fusion relies on accurate knowledge of each camera's position and
   orientation relative to the vehicle frame (extrinsic calibration). Even a
   1-degree rotation error causes object position errors of ~0.87 m at 50 m
   range, creating duplicated or misplaced detections in the fused BEV map.


.. admonition:: Question 7
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


.. admonition:: Question 8
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


.. admonition:: Question 9
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


.. admonition:: Question 10
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


----


True or False (Questions 11-15)
================================

.. admonition:: Question 11
   :class: hint

   **True or False:** 3D occupancy networks evaluate primarily using mAP
   (mean Average Precision) as their main metric.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   3D occupancy networks are evaluated using **mIoU** (mean Intersection over
   Union) across semantic voxel classes. mAP is used for bounding box
   detection benchmarks. Since occupancy produces dense per-voxel predictions,
   IoU-based metrics that compare predicted and ground-truth voxel masks are
   the appropriate choice.


.. admonition:: Question 12
   :class: hint

   **True or False:** BEV detection completely eliminates the need for
   perspective-view camera features and processes only top-down image data.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   BEV detection methods like LSS and BEVFormer start from perspective-view
   camera images and transform those features into BEV space. The perspective
   images are the input; BEV is the output representation. Only LiDAR-based
   methods can directly produce BEV features without perspective images.


.. admonition:: Question 13
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


.. admonition:: Question 14
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


.. admonition:: Question 15
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


----


Essay Questions (Questions 16-18)
===================================

.. admonition:: Question 16
   :class: hint

   **Compare and contrast Lift-Splat-Shoot (LSS) and BEVFormer** as approaches
   for camera-to-BEV transformation. What are the key architectural differences
   and the trade-offs of each?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - LSS uses explicit geometry: it predicts a per-pixel depth distribution,
     lifts features into a 3D frustum, and splats them into a voxel grid using
     camera calibration. It is conceptually simple and does not require
     Transformer attention mechanisms.
   - BEVFormer uses learnable BEV queries that attend to image features via
     deformable attention at geometrically-projected 3D reference points. It
     is more flexible and can be extended with temporal attention.
   - LSS trade-off: depends on accurate depth prediction; depth errors propagate
     into BEV position errors. BEVFormer trade-off: higher computational cost
     due to attention; requires careful tuning of query initialization and
     reference point sampling.
   - BEVFormer with temporal attention significantly outperforms LSS on nuScenes
     (41.6 vs. ~32 mAP for comparable backbones), at higher compute cost.


.. admonition:: Question 17
   :class: hint

   **Explain why 3D occupancy networks represent an advance over bounding box
   detection** for autonomous driving. Give two concrete scenarios where
   occupancy prediction is superior.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Bounding boxes assume rectangular box shapes, which fail for non-rigid
     or irregular objects. Occupancy networks assign a semantic label to every
     voxel independently, capturing arbitrary geometry.
   - Scenario 1: construction zone -- barriers, debris, and scaffolding have
     complex non-box shapes. Occupancy correctly maps the free space boundary
     while a box detector would fail or produce very loose boxes.
   - Scenario 2: overhanging tree branches or low-clearance obstacles -- a
     3D box cannot represent objects that extend into part of the vehicle's
     path. Occupancy precisely maps which voxels are occupied.
   - Additionally, occupancy provides a direct "free space" representation
     needed for trajectory optimization, while box detection requires a
     separate freespace estimation step.


.. admonition:: Question 18
   :class: hint

   **Describe Tesla's BEV occupancy network approach** and explain why Tesla
   chose a camera-only strategy instead of adding LiDAR. What are the
   potential advantages and risks of this approach?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - Tesla uses 8 cameras to produce a 4D occupancy prediction (3D space +
     predicted future states) using a video transformer trained on billions
     of auto-labeled frames from its fleet.
   - Tesla argues cameras are sufficient because humans drive with eyes only,
     and a sufficiently powerful neural network can infer depth from multi-frame
     parallax and learned scene priors.
   - Advantages: lower hardware cost (LiDAR adds $1,000-$10,000+ per unit),
     massively scalable data collection from the existing fleet, no sensor
     interference or point sparsity at long range.
   - Risks: camera-based depth inference is less reliable in low-texture
     scenes, fog, rain, and low-light conditions compared to LiDAR. Validation
     of safety margins is harder without a ground-truth depth sensor. Most
     Tier-1 robotaxi competitors (Waymo, Cruise) retain LiDAR for redundancy.
