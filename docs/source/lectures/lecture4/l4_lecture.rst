====================================================
Lecture
====================================================


Why Bird's-Eye View?
--------------------

In earlier perception lectures we processed sensor data in the native
coordinate frame of each sensor -- perspective images from cameras, 3D point
clouds from LiDAR. While these representations are natural for detection, they
carry a fundamental tension with the downstream stack:

.. admonition:: The Representation Mismatch Problem
   :class: note

   Motion planning and control operate in **metric 2D/3D world space**.
   Perspective camera images are **projective** -- depth is ambiguous, object
   sizes change with distance, and distances between objects are not preserved.
   Bringing perception outputs into a unified, metric top-down space simplifies
   every downstream module.

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Planning-Friendly
      :class-card: sd-border-info

      Path planners, trajectory optimizers, and behavior predictors all reason
      in flat ground-plane coordinates. A BEV map is a direct match.

   .. grid-item-card:: Natural for Fusion
      :class-card: sd-border-info

      Camera, LiDAR, and RADAR data can all be projected into the same BEV
      grid, enabling straightforward feature-level fusion without sensor-specific
      coordinate transforms at every module boundary.

   .. grid-item-card:: Scale Preservation
      :class-card: sd-border-info

      Object sizes and inter-object distances are metric and consistent across
      the scene. A pedestrian 5 m away looks the same size as one 50 m away.


Perspective vs. BEV vs. Occupancy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 27 27 26
   :header-rows: 1
   :class: compact-table

   * - Property
     - 2D Perspective Detection
     - BEV Detection
     - 3D Occupancy Network
   * - Output
     - 2D bounding boxes (u, v, w, h)
     - 3D boxes in BEV (x, y, yaw, l, w)
     - Per-voxel semantic label
   * - Depth info
     - Inferred / absent
     - Explicit
     - Explicit per voxel
   * - Planning utility
     - Low (needs unprojection)
     - High
     - Very high (arbitrary geometry)
   * - Handles irregular shapes
     - No (box assumption)
     - Partially
     - Yes
   * - Compute cost
     - Low
     - Medium
     - High


Camera-to-BEV Projection: Lift-Splat-Shoot
-------------------------------------------

Lift-Splat-Shoot (LSS), introduced by Philion & Fidler (NeurIPS 2020), is the
foundational camera-only BEV method. It comprises three stages.

Stage 1 -- Lift
~~~~~~~~~~~~~~~~

For each camera image pixel, LSS predicts a **depth distribution** over
:math:`D` discrete depth bins using a learned network head.

.. math::

   \mathbf{c}_{u,v} = \sum_{d=1}^{D} \alpha_{u,v,d} \cdot \mathbf{f}_{u,v}

where :math:`\alpha_{u,v,d}` is the softmax probability of depth bin :math:`d`
at pixel :math:`(u, v)`, and :math:`\mathbf{f}_{u,v}` is the 2D feature vector.

Each pixel is thus "lifted" into a **frustum of features** -- one feature vector
at each depth candidate. This creates a 3D tensor of shape
:math:`[D \times H \times W \times C]` per camera.

Stage 2 -- Splat
~~~~~~~~~~~~~~~~~

The frustum features are unprojected into a **voxel grid** in ego-vehicle
coordinates using known camera intrinsics and extrinsics. Each 3D point votes
into its corresponding voxel. The voxel pooling uses a **sum-pooling** over all
features landing in each voxel, giving a 3D occupancy-weighted feature volume.

.. code-block:: python

   # Pseudocode: frustum-to-voxel projection
   for cam in cameras:
       points_3d = unproject(frustum_depths, cam.intrinsics, cam.extrinsics)
       for point, feat in zip(points_3d, features):
           voxel_idx = world_to_voxel(point)
           voxel_grid[voxel_idx] += feat

Stage 3 -- Shoot
~~~~~~~~~~~~~~~~~

The 3D voxel grid is **collapsed along the Z-axis** (height) via max/mean
pooling to produce a 2D BEV feature map. This feature map is then passed to
standard 2D detection heads (e.g., a BEV anchor-free head) to predict 3D
object parameters.

.. admonition:: LSS Key Insight
   :class: tip

   LSS is fully differentiable end-to-end. The depth distribution is learned
   implicitly by the network, guided only by 3D bounding box supervision.
   No explicit depth labels are required during training.


BEVFormer: Attention-Based BEV Construction
--------------------------------------------

BEVFormer (Li et al., ECCV 2022) replaces LSS's geometry-based voxel projection
with a **Transformer attention mechanism** that queries image features at
learned 3D reference points.

Architecture Overview
~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: BEV Queries

      BEVFormer maintains a **grid of learnable BEV query embeddings**
      :math:`Q \in \mathbb{R}^{H \times W \times C}`, one per BEV grid cell.
      Each query represents "what is the content of this grid cell in the
      world?" and is updated by attending to relevant image regions.

   .. tab-item:: Spatial Cross-Attention

      For each BEV query at world position :math:`(x, y)`:

      1. Sample :math:`N_z` 3D reference points at different heights
         :math:`z_1, \ldots, z_{N_z}` above the ground plane.
      2. Project each 3D reference point into all camera images using
         calibration parameters.
      3. Sample image features at the projected pixel locations using
         deformable attention.
      4. Aggregate these multi-camera, multi-height features to update the
         BEV query.

      .. math::

         \text{SCA}(Q_p, F) = \frac{1}{|V_{hit}|} \sum_{i \in V_{hit}}
         \sum_{j=1}^{N_z} \text{DeformAttn}(Q_p, \mathcal{P}(p, i, j), F_i)

   .. tab-item:: Temporal Self-Attention

      BEVFormer exploits past BEV feature maps by warping the previous frame's
      BEV into the current ego frame using the ego-motion transform and then
      computing cross-attention between current queries and the warped history:

      .. math::

         \text{TSA}(Q_p, \{Q_t, Q_{t-1}'\}) =
         \text{DeformAttn}(Q_p, p, \text{concat}(Q_t, Q_{t-1}'))

      This allows the network to integrate velocity cues, occlusion reasoning,
      and multi-frame context without explicit tracking.

BEVFormer Performance on nuScenes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 35 20 20 25
   :header-rows: 1
   :class: compact-table

   * - Method
     - mAP
     - NDS
     - Backbone
   * - DETR3D
     - 34.9
     - 42.5
     - ResNet-101
   * - BEVFormer-S (no temporal)
     - 37.5
     - 44.8
     - ResNet-101
   * - BEVFormer (with temporal)
     - 41.6
     - 51.7
     - ResNet-101
   * - BEVFormer-Base
     - 48.1
     - 56.9
     - VoVNet-99

.. note::

   The gap between BEVFormer-S and BEVFormer highlights the impact of temporal
   self-attention: +4.1 mAP and +6.9 NDS purely from adding multi-frame context.


Multi-Camera Fusion in BEV Space
----------------------------------

Modern AV systems use 6--12 cameras to achieve full 360-degree surround
coverage. Fusing these in BEV space requires careful handling of:

Camera Rig Setup
~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * - Camera Position
     - Field of View
     - Primary Coverage
   * - Front
     - 60-120 deg
     - Long-range forward, traffic lights
   * - Front-Left / Front-Right
     - 90-120 deg
     - Intersection cross-traffic, lane changes
   * - Side-Left / Side-Right
     - 90 deg
     - Blind spots, adjacent lanes
   * - Rear
     - 120 deg
     - Vehicles approaching from behind

Overlap and Consistency
~~~~~~~~~~~~~~~~~~~~~~~~

Regions covered by multiple cameras can be fused by aggregating features in the
shared BEV cells. Strategies include:

- **Max pooling** -- Take the strongest activation. Simple, works well when
  one camera has a clear view.
- **Attention-weighted sum** -- Learn a confidence weight per camera per BEV
  cell. Used in cross-view transformers and BEVFusion.
- **Feature concatenation + projection** -- Concatenate multi-camera features
  at each BEV cell and project with a learned MLP.

.. admonition:: Extrinsic Calibration Is Critical
   :class: warning

   BEV fusion assumes all cameras are accurately calibrated to the vehicle
   frame. Even 1-degree extrinsic error causes significant object position
   errors at 50 m range. Online calibration monitoring is an active research
   area.


3D Occupancy Networks
----------------------

While BEV detection predicts bounding boxes for known object classes,
**3D Occupancy Networks** predict the semantic state of every voxel in a 3D
volume around the vehicle.

Motivation
~~~~~~~~~~~

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Beyond Bounding Boxes
      :class-card: sd-border-warning

      Bounding boxes fail for irregular shapes: construction barriers,
      overhanging vegetation, parked vehicles partially occluded. Occupancy
      captures arbitrary geometry.

   .. grid-item-card:: Complete Scene Representation
      :class-card: sd-border-warning

      Planning systems benefit from knowing not just ``where objects are``
      but ``what the free space is`` -- critical for path clearance checks.

Output Representation
~~~~~~~~~~~~~~~~~~~~~~

The scene is divided into a 3D voxel grid, e.g., :math:`200 \times 200 \times 16`
voxels covering :math:`[-50\text{m}, +50\text{m}] \times [-50\text{m},
+50\text{m}] \times [-5\text{m}, +3\text{m}]`. Each voxel receives:

- A **semantic label**: one of :math:`K` classes (free, vehicle, pedestrian,
  cyclist, vegetation, building, etc.) plus ``unknown/occluded``.
- Optionally, a **flow vector** indicating velocity of dynamic voxels
  (MonoOcc, UniOcc extensions).

.. math::

   \hat{y}_{i,j,k} = \text{argmax}_{c} \; p(c \mid \mathbf{v}_{i,j,k})

where :math:`\mathbf{v}_{i,j,k}` is the feature vector at voxel
:math:`(i, j, k)`.

Key Methods
~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: MonoScene (2022)

      First occupancy prediction from a **single monocular camera**. Uses 2D-3D
      feature projection with a U-Net-like 3D decoder. Introduced the nuScenes
      occupancy prediction benchmark.

   .. tab-item:: TPVFormer (2023)

      Extends BEVFormer to a **Tri-Perspective View** (top, front, side) to
      capture full 3D geometry without full 3D voxel attention. Computationally
      efficient while maintaining accuracy.

   .. tab-item:: OpenOccupancy / Occ3D

      Large-scale annotation frameworks for training occupancy networks on
      nuScenes and Waymo. Defines standard evaluation metrics:
      **mIoU** (mean Intersection over Union) per semantic class.

Occupancy vs. Detection: When to Use Which
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - Scenario
     - BEV Detection Adequate?
     - Occupancy Needed?
   * - Counting vehicles in parking lot
     - Yes
     - No
   * - Navigating construction zone
     - No (irregular obstacles)
     - Yes
   * - Freespace for lane change
     - Partially
     - Yes (accurate boundaries)
   * - Traffic light / sign detection
     - Yes
     - No (2D sufficient)


Industry Adoption
------------------

Tesla's Approach
~~~~~~~~~~~~~~~~~

Tesla's FSD v12 perception stack relies heavily on BEV representation. Key
architectural choices:

.. card::
   :class-card: sd-border-success sd-shadow-sm

   **Tesla Occupancy Network (announced 2022 AI Day)**

   - Input: 8 cameras (front, B-pillar front/rear, fisheye rears, main rear)
   - BEV feature construction via **video-based transformer** (not just single
     frame -- full temporal context)
   - Output: 4D occupancy (3D space + time), predicting future occupancy states
     enabling implicit trajectory prediction
   - Trained on **billions of frames** of auto-labeled data via Tesla's
     in-house data engine
   - No LiDAR -- camera-only, with depth inferred entirely from monocular
     multi-frame parallax and learned depth priors

Waymo, Cruise, and Others
~~~~~~~~~~~~~~~~~~~~~~~~~~

Most Tier-1 AV companies use LiDAR as the primary BEV input (point clouds are
already in 3D metric space) and fuse camera BEV features at the feature level.
The dominant paradigm for LiDAR-based BEV is:

1. Voxelize point cloud into a 3D grid.
2. Apply 3D sparse convolution (Sparse ConvNet, VoxelNet) to extract features.
3. Compress to BEV by collapsing the Z-axis.
4. Apply 2D detection head or dense occupancy prediction head.

.. seealso::

   Multi-sensor BEV fusion of camera + LiDAR + RADAR is covered in depth in
   **L6: Multi-Sensor Fusion**.


nuScenes Benchmark Metrics
---------------------------

The nuScenes dataset is the standard benchmark for BEV perception evaluation.

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Metric
     - Definition
   * - **mAP**
     - Mean Average Precision over 10 classes at 4 BEV distance thresholds
       (0.5m, 1m, 2m, 4m). Higher is better.
   * - **NDS**
     - nuScenes Detection Score: weighted combination of mAP and 5 attribute
       errors (ATE, ASE, AOE, AVE, AAE). Single scalar for ranking.
   * - **ATE**
     - Average Translation Error: 2D center distance in BEV (meters).
   * - **ASE**
     - Average Scale Error: 3D IoU between predicted and GT box sizes.
   * - **AOE**
     - Average Orientation Error: yaw angle error (radians).
   * - **mIoU**
     - Mean IoU across semantic classes (used for occupancy benchmarks).

.. math::

   \text{NDS} = \frac{1}{10} \left[ 5 \cdot \text{mAP} +
   \sum_{mtp \in \mathcal{TP}} (1 - \min(1, mtp)) \right]


Summary
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: BEV Foundations
      :class-card: sd-border-primary

      - BEV is metric, planning-friendly, and enables natural multi-sensor fusion
      - LSS: predict depth per pixel, lift to frustum, splat to voxel, shoot to BEV
      - BEVFormer: learnable queries + spatial cross-attention + temporal attention

   .. grid-item-card:: Occupancy & Industry
      :class-card: sd-border-primary

      - Occupancy networks: per-voxel semantic prediction, handles arbitrary geometry
      - Evaluation: mIoU per class on nuScenes/Waymo benchmarks
      - Tesla: camera-only 4D occupancy; others fuse LiDAR for higher accuracy

.. note::

   The progression from 2D detection (L3) to BEV detection (L4) to occupancy
   prediction (L4 advanced) mirrors how the industry has evolved from early
   prototype systems to production AV stacks.
