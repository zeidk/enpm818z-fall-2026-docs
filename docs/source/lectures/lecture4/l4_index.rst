================================================================
L4: Perception II -- BEV Perception & Occupancy Networks
================================================================

Overview
--------

This lecture extends the perception pipeline from L3 into the Bird's-Eye View
(BEV) representation, explaining why top-down spatial maps are better suited
for downstream planning and multi-sensor fusion. You will study two landmark
architectures -- Lift-Splat-Shoot (LSS) and BEVFormer -- and then progress
to 3D Occupancy Networks, which replace object bounding boxes with dense,
per-voxel semantic predictions of the complete scene.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain why BEV is a preferred representation for autonomous driving
  planning and multi-sensor fusion.
- Describe the Lift-Splat-Shoot (LSS) pipeline for camera-to-BEV projection
  including depth estimation, voxel pooling, and BEV feature extraction.
- Explain BEVFormer's learnable BEV queries, spatial cross-attention, and
  temporal self-attention mechanisms.
- Compare 2D perspective detection, BEV detection, and 3D occupancy prediction
  in terms of representational power and planning utility.
- Define 3D occupancy networks and explain per-voxel semantic prediction.
- Describe how multi-camera views are fused in BEV space.
- Summarize how Tesla and other industry players adopt BEV perception.
- Interpret nuScenes benchmark metrics (mAP, NDS) in the context of modern
  BEV methods.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l4_lecture
   l4_quiz
   l4_references

Next Steps
----------

- The next lecture covers **Perception III -- Segmentation, Tracking & Temporal
  Reasoning**: semantic, instance, and panoptic segmentation; multi-object
  tracking (SORT, DeepSORT, ByteTrack); and using temporal context to improve
  perception quality.
- Review the BEVFormer paper: Li et al. (2022) ``BEVFormer: Learning Bird's-Eye-View
  Representation from Multi-Camera Images via Spatiotemporal Transformers.``
- Explore the `nuScenes leaderboard <https://nuscenes.org/object-det>`_ to see
  where current BEV methods rank in 3D object detection.
