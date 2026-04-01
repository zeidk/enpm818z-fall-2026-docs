====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 4: Perception II -- BEV
Perception & Occupancy Networks. Topics include the motivation for BEV
representations, Lift-Splat-Shoot, BEVFormer, multi-camera fusion, 3D
occupancy networks, nuScenes metrics, and industry adoption.

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

   What is the purpose of **Temporal Self-Attention** in BEVFormer?

   A. To apply attention across all pixels in a single camera image.

   B. To integrate previous BEV feature maps (warped to the current frame)
      with the current BEV queries, providing multi-frame context.

   C. To synchronize feature extraction across all cameras in the rig.

   D. To reduce compute by skipping attention for static background cells.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To integrate previous BEV feature maps (warped to the current
   frame) with the current BEV queries, providing multi-frame context.

   Temporal Self-Attention warps the prior frame's BEV using ego-motion
   estimates and then computes cross-attention between the current BEV queries
   and the concatenated current + warped-past features. This provides velocity
   cues, helps with occluded objects, and significantly boosts detection of
   moving objects (up to +6.9 NDS on nuScenes).


.. admonition:: Question 5
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


.. admonition:: Question 6
   :class: hint

   Which nuScenes metric is a **composite score** combining mAP with five
   attribute error terms?

   A. mIoU

   B. ATE

   C. NDS

   D. AOE

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- NDS (nuScenes Detection Score)

   NDS is the primary ranking metric on nuScenes. It is computed as a
   weighted combination of mAP and five True Positive metrics: Average
   Translation Error (ATE), Average Scale Error (ASE), Average Orientation
   Error (AOE), Average Velocity Error (AVE), and Average Attribute Error
   (AAE). A single NDS scalar enables fair ranking of methods.


.. admonition:: Question 7
   :class: hint

   In the **Splat** stage of LSS, what operation converts the 3D frustum
   features into a voxel grid?

   A. Deformable attention over reference points in image space.

   B. Unprojection of frustum features into ego-vehicle coordinates using
      camera intrinsics and extrinsics, then sum-pooling into voxels.

   C. Warping the image feature map using a homography transformation.

   D. Applying 3D sparse convolution to the point cloud.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Unprojection of frustum features into ego-vehicle coordinates
   using camera intrinsics and extrinsics, then sum-pooling into voxels.

   The Splat stage uses known camera calibration to unproject the 3D frustum
   points (which are in camera space) into the world/ego-vehicle 3D space.
   Multiple frustum points that land in the same voxel are aggregated via
   sum-pooling, producing a dense 3D feature volume.


.. admonition:: Question 8
   :class: hint

   Tesla's occupancy network (as described at AI Day 2022) takes which sensors
   as input?

   A. LiDAR + 8 cameras

   B. RADAR + front camera

   C. 8 cameras only (no LiDAR)

   D. LiDAR + RADAR (no cameras)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- 8 cameras only (no LiDAR)

   Tesla's approach is camera-only. Their 8-camera rig provides surround
   coverage and the network infers depth via multi-frame parallax and learned
   depth priors. Tesla has argued this matches human driving (eyes only) and
   enables lower hardware costs at scale.


.. admonition:: Question 9
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


.. admonition:: Question 10
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


----


True or False (Questions 11-15)
================================

.. admonition:: Question 11
   :class: hint

   **True or False:** The Lift-Splat-Shoot method requires explicit depth
   sensor supervision (e.g., LiDAR depth labels) during training.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   LSS learns its depth distribution implicitly from 3D bounding box
   supervision alone. The depth prediction network is trained end-to-end
   alongside the detection head -- no explicit depth ground truth labels are
   required. This is one of LSS's key advantages: it works with camera-only
   setups.


.. admonition:: Question 12
   :class: hint

   **True or False:** BEVFormer's temporal self-attention warps the previous
   BEV feature map into the current ego frame using ego-motion estimates before
   computing attention.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Before computing temporal self-attention, BEVFormer applies the ego-motion
   transformation (from vehicle odometry or localization) to spatially align
   the previous BEV frame with the current ego frame. This alignment is
   necessary so that a stationary object at the same world position aligns in
   both BEV grids, while moving objects will have a visible offset.


.. admonition:: Question 13
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


.. admonition:: Question 14
   :class: hint

   **True or False:** The nuScenes NDS metric rewards methods that have both
   high detection recall (mAP) and low attribute errors (e.g., position,
   size, orientation, velocity).

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   NDS = (1/10) * [5 * mAP + sum over TP metrics of (1 - min(1, error))].
   It equally rewards accurate detection (mAP) and precise attribute
   estimation (ATE, ASE, AOE, AVE, AAE). A method with high mAP but poor
   velocity estimation will score lower than one with balanced performance
   across all attributes.


.. admonition:: Question 15
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
