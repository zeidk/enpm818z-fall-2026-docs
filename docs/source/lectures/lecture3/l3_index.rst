====================================================
L3: Perception I -- Object Detection (YOLO to DETR)
====================================================

Overview
--------

This lecture covers the foundations of visual perception for autonomous driving,
progressing from traditional computer vision to modern deep learning approaches.
You will learn how perception fits into the AV stack, understand the taxonomy
of perception tasks, and study two landmark object detection architectures:
YOLO (CNN-based) and DETR (transformer-based). The lecture concludes with a
hands-on comparison of both models on CARLA data.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Define perception and explain its role in the AV stack (sensing ->
  perception -> planning -> control).
- Describe the taxonomy of perception tasks: low-level processing, mid-level
  understanding, and high-level reasoning.
- Explain why traditional CV methods (HOG, SIFT) failed for robust AV
  perception and how deep learning changed the field.
- Trace the YOLO architecture evolution from v1 (2015) to v11 (2024).
- Explain the backbone-neck-head architecture and the difference between
  anchor-based and anchor-free detection.
- Describe the DETR architecture: encoder-decoder transformer, object queries,
  and bipartite matching.
- Compare YOLO and DETR on speed, accuracy, and failure modes.
- Train and deploy an object detector on CARLA data as a ROS 2 node.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l3_lecture
   l3_quiz
   l3_references


Next Steps
----------

- In the next lecture, we will cover **Perception II: BEV Perception &
  Occupancy Networks**:

  - Bird's-Eye View representation and why it matters for AV planning.
  - BEVFormer and camera-to-BEV projection.
  - 3D occupancy networks.

- Start working on **A2: Object Detection -- YOLO vs. DETR** (posted Week 6).
- Read the `Ultralytics YOLOv8 documentation <https://docs.ultralytics.com/>`_.
- Read the `DETR paper <https://arxiv.org/abs/2005.12872>`_ (Carion et al., 2020).
