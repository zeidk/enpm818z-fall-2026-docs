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
:math:`D` discrete depth bins using a learned network head. The pixel's
context feature :math:`\mathbf{f}_{u,v} \in \mathbb{R}^C` is then spread
across those bins by an **outer product** with the depth distribution:

.. math::

   \mathbf{c}_{u,v,d} = \alpha_{u,v,d} \cdot \mathbf{f}_{u,v},
   \qquad d = 1, \ldots, D

where :math:`\alpha_{u,v,d}` is the softmax probability of depth bin
:math:`d` at pixel :math:`(u, v)`, with
:math:`\sum_{d} \alpha_{u,v,d} = 1`.

.. important::

   Note that this is **not** a sum over :math:`d`. Summing would collapse
   the distribution back to :math:`\mathbf{f}_{u,v}` (since the
   probabilities sum to 1) and destroy exactly the depth information the
   Lift step exists to create. The output has an extra dimension, not one
   fewer.

Each pixel is thus "lifted" into a **frustum of features** -- one weighted
feature vector at each depth candidate. This creates a 4-D tensor of shape
:math:`[D \times H \times W \times C]` per camera.

.. admonition:: What the network is really saying
   :class: tip

   If the network is confident a pixel is at 12 m, :math:`\alpha` is
   sharply peaked there and the feature appears at essentially one depth.
   If it is uncertain, the same feature is smeared across many depths at
   reduced magnitude. Downstream pooling then lets confident predictions
   dominate the BEV cell they land in -- **soft depth estimation falls out
   of the architecture** rather than requiring a separate depth loss.

Stage 2 -- Splat
~~~~~~~~~~~~~~~~~

The frustum features are unprojected into **pillars** on a BEV grid in
ego-vehicle coordinates, using known camera intrinsics and extrinsics.
Every frustum point from every camera votes into the BEV cell it lands in,
and the features falling in each cell are **sum-pooled**. Collapsing the
vertical dimension is part of this step -- the result is a 2-D BEV feature
map, ready for a standard 2-D detection or segmentation head.

.. code-block:: python

   # Pseudocode: frustum-to-BEV pillar pooling
   for cam in cameras:
       points_3d = unproject(frustum_depths, cam.intrinsics, cam.extrinsics)
       for point, feat in zip(points_3d, features):
           bev_idx = world_to_bev_cell(point)   # x-y only; z is collapsed
           bev_grid[bev_idx] += feat            # sum-pool

.. note::

   Doing this naively -- a Python loop over millions of frustum points --
   is hopeless. LSS makes it fast with the "cumulative sum trick": sort
   points by BEV cell index, take a cumulative sum over the feature
   tensor, then subtract at the cell boundaries. That turns the whole
   pooling operation into a sort plus a prefix sum, both of which are
   fast and differentiable on GPU.

Stage 3 -- Shoot
~~~~~~~~~~~~~~~~~

**Shoot** is the planning stage, and it is the part of the name most
often misremembered. Having built the BEV representation, LSS "shoots" a
fixed set of **candidate ego trajectories** (templates clustered from
recorded human driving) into the BEV cost map, scores each one, and
selects the best.

.. warning::

   A common misreading is that "Shoot" refers to collapsing the voxel
   grid down to BEV. It does not -- that height collapse belongs to
   **Splat**. Shoot is what makes the paper's title
   *"Lift, Splat, Shoot: Encoding Images from Arbitrary Camera Rigs by
   Implicitly Unprojecting to 3D"* end in a planning verb: the whole
   pipeline was designed to be trained end-to-end **for planning**, not
   just for perception.

.. admonition:: LSS Key Insight
   :class: tip

   LSS is fully differentiable end-to-end. The depth distribution is learned
   implicitly by the network, guided only by downstream supervision --
   no explicit depth labels are required during training.


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
   :widths: 30 15 15 25 15
   :header-rows: 1
   :class: compact-table

   * - Method
     - mAP
     - NDS
     - Backbone
     - Split
   * - DETR3D
     - 34.9
     - 42.5
     - ResNet-101
     - val
   * - BEVFormer-S (no temporal)
     - 37.5
     - 44.8
     - ResNet-101
     - val
   * - BEVFormer (with temporal)
     - 41.6
     - 51.7
     - ResNet-101
     - val
   * - BEVFormer-Base
     - 48.1
     - 56.9
     - VoVNet-99
     - test

.. note::

   The controlled comparison here is **BEVFormer-S vs BEVFormer** -- same
   backbone, same split, differing only in temporal self-attention:
   +4.1 mAP and +6.9 NDS purely from adding multi-frame context.

   The BEVFormer-Base row uses both a stronger backbone **and** the test
   split, so its higher numbers are not evidence about temporal
   attention. Comparing across splits is a standard way to accidentally
   overstate a result; always check the split column before drawing a
   conclusion from a leaderboard.


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


Segmentation for Autonomous Driving
-------------------------------------

.. admonition:: Recap from ENPM673
   :class: note

   In ENPM673, you studied semantic segmentation fundamentals: pixel-wise
   classification, the encoder-decoder paradigm (U-Net), mIoU evaluation,
   and the distinction between semantic, instance, and panoptic segmentation.
   This lecture focuses on how these techniques are **deployed in autonomous
   driving** and introduces AV-specific architectures and tasks.

Object detection from L4 gives us **where objects are** (bounding boxes) but
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

   Both tasks benefit enormously from the BEV representation introduced
   earlier in this lecture. In perspective view, foreshortening makes lane
   width and curvature appear non-uniform -- lanes converge toward the
   horizon and curvature is compressed at distance. In BEV, lanes become
   **uniform-width curves** that are simpler to predict, fit with
   polynomials, and post-process. Several state-of-the-art lane detectors
   (PersFormer, Anchor3DLane) now predict lanes directly in BEV space,
   side-stepping perspective distortion entirely.


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
              = \underbrace{\frac{\sum_{(p,g) \in TP} \text{IoU}(p,g)}{|TP|}}_{\text{SQ (Segmentation Quality)}}
                \times
                \underbrace{\frac{|TP|}{|TP| + \frac{1}{2}|FP| + \frac{1}{2}|FN|}}_{\text{RQ (Recognition Quality)}}

The factorization is the useful part: **RQ** is an F\ :sub:`1` score over
segments -- did you find the right objects? -- while **SQ** is the mean IoU
of the segments you did match -- how well did you delineate them? A low PQ
tells you little on its own; the split tells you whether to work on
detection or on boundaries.


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

   Classical multi-sensor fusion (KF/EKF/UKF, data association,
   weighted averaging) was covered in **L3: Probabilistic State
   Estimation & Fusion**; deep-learning fusion of camera + LiDAR in
   BEV space (cross-attention, BEVFusion) is covered in **L6:
   Perception III**.


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
     - Average Scale Error: :math:`1 - \text{IoU}` between predicted and GT
       box sizes after aligning translation and orientation. It is an
       *error*, so lower is better.
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

   .. grid-item-card:: Occupancy
      :class-card: sd-border-primary

      - Occupancy networks: per-voxel semantic prediction, handles arbitrary geometry
      - Evaluation: mIoU per class on nuScenes/Waymo benchmarks
      - Tesla: camera-only 4D occupancy; others fuse LiDAR for higher accuracy

   .. grid-item-card:: Segmentation
      :class-card: sd-border-primary

      - DeepLabv3+: dilated convolutions + ASPP for multi-scale context
      - Driveable surface + lane detection as specialised seg tasks
      - Instance / Panoptic seg (Mask R-CNN), unified PQ metric

.. note::

   The progression from 2D detection (L4) to BEV detection (L5) to occupancy
   prediction (L5 advanced) mirrors how the industry has evolved from early
   prototype systems to production AV stacks. Segmentation completes the
   picture: pixel-level scene understanding feeds both BEV reconstruction
   and downstream planning.


CARLA Hands-On: BEV Grid & Semantic Segmentation
------------------------------------------------------------

This exercise walks through the core steps of constructing a BEV
representation from CARLA's multi-camera setup (Tasks 1-4) and then
explores semantic segmentation with CARLA's ground-truth labels
(Tasks 5-6).


Task 1: Set Up a Multi-Camera Rig
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spawn six cameras to achieve 360-degree surround coverage, mimicking a
production AV sensor configuration.

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

   # Define 6-camera rig (position, yaw)
   camera_configs = [
       {'name': 'front',       'x':  1.5, 'y':  0.0, 'z': 2.4, 'yaw':   0},
       {'name': 'front_left',  'x':  1.0, 'y': -0.5, 'z': 2.4, 'yaw': -60},
       {'name': 'front_right', 'x':  1.0, 'y':  0.5, 'z': 2.4, 'yaw':  60},
       {'name': 'back',        'x': -1.5, 'y':  0.0, 'z': 2.4, 'yaw': 180},
       {'name': 'back_left',   'x': -1.0, 'y': -0.5, 'z': 2.4, 'yaw':-120},
       {'name': 'back_right',  'x': -1.0, 'y':  0.5, 'z': 2.4, 'yaw': 120},
   ]

   IMAGE_W, IMAGE_H, FOV = 800, 600, 90
   cameras = {}

   for cfg in camera_configs:
       cam_bp = bp_lib.find('sensor.camera.rgb')
       cam_bp.set_attribute('image_size_x', str(IMAGE_W))
       cam_bp.set_attribute('image_size_y', str(IMAGE_H))
       cam_bp.set_attribute('fov', str(FOV))
       transform = carla.Transform(
           carla.Location(x=cfg['x'], y=cfg['y'], z=cfg['z']),
           carla.Rotation(yaw=cfg['yaw']))
       cam = world.spawn_actor(cam_bp, transform, attach_to=vehicle)
       cameras[cfg['name']] = cam

   # Also spawn a depth camera co-located with the front camera
   # (to provide ground-truth depth for the LSS exercise)
   depth_bp = bp_lib.find('sensor.camera.depth')
   depth_bp.set_attribute('image_size_x', str(IMAGE_W))
   depth_bp.set_attribute('image_size_y', str(IMAGE_H))
   depth_bp.set_attribute('fov', str(FOV))
   depth_cam = world.spawn_actor(
       depth_bp,
       carla.Transform(carla.Location(x=1.5, z=2.4)),
       attach_to=vehicle)

   print(f"Spawned {len(cameras)} RGB cameras + 1 depth camera.")


Task 2: Build Camera Intrinsics and Extrinsics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def get_camera_intrinsic(image_w, image_h, fov):
       """Compute the 3x3 camera intrinsic matrix from CARLA parameters."""
       focal = image_w / (2.0 * np.tan(np.radians(fov / 2.0)))
       K = np.array([
           [focal,  0.0,   image_w / 2.0],
           [0.0,    focal, image_h / 2.0],
           [0.0,    0.0,   1.0]
       ])
       return K

   def get_extrinsic_matrix(camera_actor):
       """Get the 4x4 camera-to-world extrinsic matrix."""
       transform = camera_actor.get_transform()
       return np.array(transform.get_matrix())

   K = get_camera_intrinsic(IMAGE_W, IMAGE_H, FOV)
   print(f"Intrinsic matrix:\n{K}")

   for name, cam in cameras.items():
       E = get_extrinsic_matrix(cam)
       print(f"{name} extrinsic (camera-to-world):\n{E[:3]}\n")


Task 3: Simplified LSS -- Lift Depth to 3D and Splat to BEV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using the ground-truth depth from CARLA's depth camera, implement the core
LSS steps: "lift" pixels to 3D points and "splat" them into a BEV grid.

.. code-block:: python

   # BEV grid parameters, expressed in the EGO frame.
   # CARLA/UE ego axes: x FORWARD, y RIGHT, z UP.
   BEV_X_RANGE = (-50.0, 50.0)   # meters, behind <-> ahead
   BEV_Y_RANGE = (-50.0, 50.0)   # meters, left <-> right
   BEV_RESOLUTION = 0.5           # meters per cell

   def parse_carla_depth_image(depth_image):
       """Decode CARLA's depth camera into metres.

       CARLA encodes depth across the BGR channels as a 24-bit integer
       normalized to the far plane (1000 m). Reading the raw bytes as an
       image and treating them as depth gives nonsense.
       """
       array = np.frombuffer(depth_image.raw_data, dtype=np.uint8)
       array = array.reshape((depth_image.height, depth_image.width, 4))
       b = array[:, :, 0].astype(np.float32)
       g = array[:, :, 1].astype(np.float32)
       r = array[:, :, 2].astype(np.float32)
       normalized = (r + g * 256.0 + b * 256.0 * 256.0) / (256.0**3 - 1)
       return normalized * 1000.0        # metres

   def depth_image_to_ego_points(depth_array, K, cam_to_ego):
       """Lift a depth image to 3D points in the EGO frame (LSS 'Lift').

       Two conventions collide here and both must be handled:
         * K assumes OPTICAL axes  (x right, y down, z forward)
         * CARLA transforms use UE axes (x forward, y right, z up)
       """
       H, W = depth_array.shape
       u, v = np.meshgrid(np.arange(W), np.arange(H))

       # Back-project pixels into the OPTICAL camera frame
       x_opt = (u - K[0, 2]) * depth_array / K[0, 0]
       y_opt = (v - K[1, 2]) * depth_array / K[1, 1]
       z_opt = depth_array

       # Optical -> UE axes (the inverse of the L2 permutation):
       #   UE x (fwd)   =  optical z
       #   UE y (right) =  optical x
       #   UE z (up)    = -optical y
       x_ue, y_ue, z_ue = z_opt, x_opt, -y_opt

       ones = np.ones_like(x_ue)
       cam_points = np.stack([x_ue, y_ue, z_ue, ones], axis=-1).reshape(-1, 4)

       # Camera -> ego. Build cam_to_ego from the two world transforms:
       #   T_ego<-cam = (T_world<-ego)^-1 @ T_world<-cam
       return (cam_to_ego @ cam_points.T).T[:, :3]

   def splat_to_bev(points_ego, bev_x_range, bev_y_range, resolution,
                    z_range=(-2.0, 4.0)):
       """Splat EGO-frame points into a 2D BEV grid (LSS 'Splat' stage).

       The grid is ego-centred, so the vehicle really is at the middle
       cell -- splatting world-frame points here would place the ego
       marker correctly only if the car sat at the world origin.
       """
       bev_w = int((bev_y_range[1] - bev_y_range[0]) / resolution)  # y -> cols
       bev_h = int((bev_x_range[1] - bev_x_range[0]) / resolution)  # x -> rows
       bev_grid = np.zeros((bev_h, bev_w), dtype=np.float32)

       # Drop the road surface and anything above the vehicle envelope
       zmask = (points_ego[:, 2] > z_range[0]) & (points_ego[:, 2] < z_range[1])
       pts = points_ego[zmask]

       # Ego x (forward) -> row, ego y (right) -> column
       ri = ((pts[:, 0] - bev_x_range[0]) / resolution).astype(int)
       ci = ((pts[:, 1] - bev_y_range[0]) / resolution).astype(int)

       valid = (ri >= 0) & (ri < bev_h) & (ci >= 0) & (ci < bev_w)
       ri, ci = ri[valid], ci[valid]

       # Accumulate point counts per cell (sum-pooling, as in LSS)
       np.add.at(bev_grid, (ri, ci), 1.0)

       # Row 0 is the rear of the grid; flip so "up" on screen is forward
       return np.flipud(bev_grid)

   # Usage (inside the depth camera callback):
   # depth_array = parse_carla_depth_image(depth_image)
   # world_to_ego = np.array(vehicle.get_transform().get_inverse_matrix())
   # cam_to_world = np.array(depth_cam.get_transform().get_matrix())
   # cam_to_ego   = world_to_ego @ cam_to_world
   # points = depth_image_to_ego_points(depth_array, K, cam_to_ego)
   # bev = splat_to_bev(points, BEV_X_RANGE, BEV_Y_RANGE, BEV_RESOLUTION)


Task 4: Visualize and Analyze the BEV Grid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def visualize_bev(bev_grid, title="BEV Occupancy"):
       """Display the BEV grid as a heatmap."""
       # Normalize for visualization
       bev_vis = np.clip(bev_grid, 0, 50)  # cap at 50 points per cell
       bev_vis = (bev_vis / 50.0 * 255).astype(np.uint8)
       bev_colored = cv2.applyColorMap(bev_vis, cv2.COLORMAP_JET)

       # Mark ego vehicle at center
       center = (bev_grid.shape[1] // 2, bev_grid.shape[0] // 2)
       cv2.circle(bev_colored, center, 5, (0, 255, 0), -1)
       cv2.putText(bev_colored, "EGO", (center[0]+8, center[1]+5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

       cv2.imshow(title, bev_colored)
       cv2.waitKey(1)

.. admonition:: Exercise Tasks
   :class: tip

   1. **Run the multi-camera rig** and display all six camera views in a
      tiled window.
   2. **Implement the LSS pipeline** using CARLA's ground-truth depth camera.
      Visualize the resulting BEV occupancy grid.
   3. **Multi-camera BEV fusion**: Extend the pipeline to use all six cameras
      (each with a co-located depth camera). Merge all BEV grids using
      sum-pooling and compare coverage against a single front camera.
   4. **Vary the BEV resolution**: Test 0.25 m, 0.5 m, and 1.0 m resolution.
      How does resolution affect object visibility and compute time?
   5. **Compare to LiDAR BEV**: Spawn a 64-channel LiDAR, project its point
      cloud into the same BEV grid, and compare the camera-based vs.
      LiDAR-based BEV representations side-by-side.

.. note::

   In a real LSS implementation, the depth distribution is *learned* by a
   neural network rather than using ground-truth depth. This exercise uses
   CARLA's depth camera as a stand-in to focus on the geometric concepts.
   The learned depth version is what makes LSS end-to-end differentiable.


Task 5: Semantic Segmentation from CARLA
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

   # CARLA semantic tags (CityScapes-aligned scheme, CARLA 0.9.14+).
   # These IDs CHANGED in CARLA 0.9.12 -- older tutorials use the legacy
   # set where Road=7 and Car=10, which will silently produce a black
   # image on 0.9.16. Verify against the "Semantic segmentation sensor"
   # table in the CARLA docs for YOUR version before trusting them.
   ROAD, ROADLINE, SIDEWALK = 1, 24, 2
   LABEL_COLORS = {
       0:  (0, 0, 0),        # Unlabeled
       1:  (128, 64, 128),   # Roads
       2:  (244, 35, 232),   # SideWalks
       3:  (70, 70, 70),     # Building
       7:  (250, 170, 30),   # TrafficLight
       8:  (220, 220, 0),    # TrafficSign
       9:  (107, 142, 35),   # Vegetation
       12: (220, 20, 60),    # Pedestrian
       14: (0, 0, 142),      # Car
       15: (0, 0, 70),       # Truck
       16: (0, 60, 100),     # Bus
       24: (157, 234, 50),   # RoadLine
   }

   def seg_callback(image):
       """Colorize semantic segmentation output."""
       array = np.frombuffer(image.raw_data, dtype=np.uint8)
       array = array.reshape((image.height, image.width, 4))
       # raw_data is BGRA, so index 2 is the RED channel, which is where
       # CARLA stores the semantic tag.
       labels = array[:, :, 2]

       colored = np.zeros((image.height, image.width, 3), dtype=np.uint8)
       for label_id, color in LABEL_COLORS.items():
           colored[labels == label_id] = color

       # Driveable surface mask (road + lane markings)
       driveable = ((labels == ROAD) | (labels == ROADLINE))
       driveable = driveable.astype(np.uint8) * 255

       cv2.imshow("Semantic Segmentation", colored)
       cv2.imshow("Driveable Surface", driveable)
       cv2.waitKey(1)

   seg_cam.listen(seg_callback)

.. admonition:: Confirm the tag IDs before you build on them
   :class: warning

   If your colorized output is mostly black, or the "driveable surface"
   mask is empty, the tag IDs are wrong for your CARLA build. Print what
   is actually in the image rather than guessing:

   .. code-block:: python

      print(np.unique(labels, return_counts=True))

   The tag covering most of the lower half of a forward-facing camera is
   the road. Alternatively, use CARLA's own palette by listening with
   ``carla.ColorConverter.CityScapesPalette``, which sidesteps the ID
   table entirely for visualization (though you still need raw tags for
   the mask).


Task 6: Compute Segmentation Metrics
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


.. note::

   **GP2** builds on this lecture, but wait for L6 before starting: the
   assignment requires tracking as well as detection, and the tracker is
   covered there. Use the time to collect and label your CARLA dataset.
