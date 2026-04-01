========================================================================
L5: Perception III -- Segmentation, Tracking & Temporal Reasoning
========================================================================

Overview
--------

This lecture completes the perception pipeline by covering two essential tasks
that go beyond object detection: **segmentation** (assigning semantic meaning
to every pixel or instance in the scene) and **multi-object tracking** (linking
detections across frames to maintain consistent object identities over time).
You will also study how temporal context -- reasoning over sequences of frames
rather than single images -- significantly improves perception quality and
enables velocity estimation for downstream prediction.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Distinguish semantic, instance, and panoptic segmentation and explain when
  each is appropriate.
- Describe the U-Net and DeepLabv3+ architectures for semantic segmentation.
- Explain driveable surface and lane detection as specialized segmentation tasks.
- Formulate the multi-object tracking (MOT) problem and the tracking-by-detection
  paradigm.
- Describe the SORT, DeepSORT, and ByteTrack algorithms and their key design
  choices.
- Evaluate tracking performance using MOTA, MOTP, and IDF1 metrics.
- Explain how temporal reasoning -- using sequences of frames -- improves
  perception beyond single-frame methods.
- Describe how segmentation and tracking integrate with the L3-L4 perception
  pipeline.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l5_lecture
   l5_quiz
   l5_references

Next Steps
----------

- The next lecture covers **Multi-Sensor Fusion**: Kalman filter theory (KF,
  EKF, UKF), particle filters, data association, and modern deep learning
  fusion approaches combining camera, LiDAR, and RADAR.
- Review the ByteTrack paper: Zhang et al. (2022) for an efficient, highly
  accurate modern tracker used in production systems.
- Explore the MOTChallenge benchmark at `https://motchallenge.net
  <https://motchallenge.net>`_ to understand evaluation protocols.
