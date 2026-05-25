========================================================================
L6: Perception III -- Tracking, Temporal Reasoning & Deep Fusion
========================================================================

Overview
--------

This lecture completes the perception pipeline by linking single-frame
detections into persistent object tracks and by fusing modalities with
learned attention. It builds directly on the Kalman / EKF / UKF
machinery taught in L3 (SORT and DeepSORT rest on those filters) and
on the BEV representation from L5 (cross-attention and BEVFusion
operate in BEV space). The lecture closes with a CARLA exercise
implementing a basic SORT tracker on the detections produced by your
L4 / L5 perception stack.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Formulate the multi-object tracking (MOT) problem and the
  tracking-by-detection paradigm.
- Describe the SORT, DeepSORT, and ByteTrack algorithms and their key
  design choices, and connect SORT's state estimation to the Kalman
  filter from L3.
- Evaluate tracking performance using MOTA, MOTP, and IDF1 metrics.
- Explain how temporal reasoning -- using sequences of frames --
  improves perception beyond single-frame methods.
- Describe how tracking integrates with the L4 (Detection) /
  L5 (BEV + Occupancy + Segmentation) pipeline.
- Explain cross-attention fusion of camera and LiDAR BEV features.
- Describe BEVFusion as a representative modern deep-learning fusion
  architecture and its trade-offs vs. classical fusion from L3.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l6_lecture
   l6_exercises
   l6_quiz
   l6_references

Next Steps
----------

- The next lecture covers **Localization & SLAM**: GNSS / RTK, dead
  reckoning, visual / LiDAR odometry, probabilistic localization with
  EKF (built on L3), SLAM frontend (ICP, feature extraction), and
  SLAM backend (pose graphs, loop closure).
- Review the ByteTrack paper: Zhang et al. (2022) for an efficient,
  highly accurate modern tracker used in production systems.
- Explore the MOTChallenge benchmark at `https://motchallenge.net
  <https://motchallenge.net>`_ to understand evaluation protocols.
- (Follow-up content) The current Temporal Reasoning section can be
  extended with transformer-based MOT (MOTR, TrackFormer) and video
  transformer methods; this is on the v2 polish list.
