====================================================================
L5: Perception II -- BEV, Occupancy & Segmentation
====================================================================

Overview
--------

This lecture extends the perception pipeline from L4 (Detection) along
two complementary axes: **representation** -- moving from per-image
bounding boxes to the Bird's-Eye View (BEV) and full 3D occupancy --
and **density** -- moving from sparse detections to dense, per-pixel
segmentation. You will study two landmark BEV architectures
(Lift-Splat-Shoot and BEVFormer), 3D Occupancy Networks, and
DeepLabv3+-style segmentation including driveable surface and lane
detection. The lecture closes with industry adoption notes,
nuScenes benchmarks, and a CARLA exercise that builds a BEV grid
from a multi-camera rig and explores CARLA's semantic-segmentation
ground truth.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain why BEV is a preferred representation for autonomous driving
  planning and multi-sensor fusion.
- Describe the Lift-Splat-Shoot (LSS) pipeline for camera-to-BEV
  projection including depth estimation, voxel pooling, and BEV
  feature extraction.
- Explain BEVFormer's learnable BEV queries, spatial cross-attention,
  and temporal self-attention mechanisms.
- Compare 2D perspective detection, BEV detection, and 3D occupancy
  prediction in terms of representational power and planning utility.
- Define 3D occupancy networks and explain per-voxel semantic
  prediction.
- Describe how multi-camera views are fused in BEV space.
- Explain DeepLabv3+'s use of dilated convolutions and ASPP for
  multi-scale segmentation.
- Implement driveable-surface and lane segmentation pipelines, and
  reason about their role in trajectory planning.
- Distinguish semantic, instance, and panoptic segmentation; compute
  Panoptic Quality (PQ).
- Summarize how Tesla and other industry players adopt BEV perception.
- Interpret nuScenes benchmark metrics (mAP, NDS) in the context of
  modern BEV methods.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l5_lecture
   l5_exercises
   l5_quiz
   l5_references

Next Steps
----------

- The next lecture covers **Perception III -- Tracking, Temporal
  Reasoning & Deep-Learning Fusion**: multi-object tracking (SORT,
  DeepSORT, ByteTrack, transformer-based MOT), temporal context for
  perception, and cross-attention / BEVFusion as the modern
  deep-learning fusion paradigm built on top of the BEV
  representation introduced here.
- Review the BEVFormer paper: Li et al. (2022) ``BEVFormer: Learning
  Bird's-Eye-View Representation from Multi-Camera Images via
  Spatiotemporal Transformers.``
- Explore the `nuScenes leaderboard <https://nuscenes.org/object-det>`_
  to see where current BEV methods rank in 3D object detection.
