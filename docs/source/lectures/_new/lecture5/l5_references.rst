====================================================
References
====================================================


.. dropdown:: Foundational BEV Papers
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Lift-Splat-Shoot (LSS)
         :link: https://arxiv.org/abs/2008.05711
         :class-card: sd-border-secondary

         **Philion & Fidler, NeurIPS 2020**

         Lifting image features into 3D space and splatting into a BEV grid.
         The seminal camera-only BEV method.

      .. grid-item-card:: BEVFormer
         :link: https://arxiv.org/abs/2203.17270
         :class-card: sd-border-secondary

         **Li et al., ECCV 2022**

         Learnable BEV queries with spatial cross-attention and temporal
         self-attention. State-of-the-art camera-only BEV detection.

      .. grid-item-card:: DETR3D
         :link: https://arxiv.org/abs/2110.06922
         :class-card: sd-border-secondary

         **Wang et al., CoRL 2021**

         3D object detection from multi-camera images using set-to-set
         prediction with 3D reference points and camera-based attention.

      .. grid-item-card:: BEVDet
         :link: https://arxiv.org/abs/2112.11790
         :class-card: sd-border-secondary

         **Huang et al., 2021**

         Adapts image backbones to BEV space using the LSS view transformer
         with improved data augmentation strategies.


.. dropdown:: 3D Occupancy Networks
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: MonoScene
         :link: https://arxiv.org/abs/2112.00726
         :class-card: sd-border-secondary

         **Cao & de Charette, CVPR 2022**

         First semantic scene completion from a single monocular camera.
         Introduced the camera-based occupancy prediction task.

      .. grid-item-card:: TPVFormer
         :link: https://arxiv.org/abs/2302.07817
         :class-card: sd-border-secondary

         **Huang et al., CVPR 2023**

         Tri-Perspective View representation for efficient 3D occupancy
         prediction without full 3D voxel attention.

      .. grid-item-card:: Occ3D
         :link: https://arxiv.org/abs/2304.14365
         :class-card: sd-border-secondary

         **Tian et al., NeurIPS 2023**

         Large-scale 3D occupancy benchmark on nuScenes and Waymo with
         dense annotations and standardized evaluation.

      .. grid-item-card:: OpenOccupancy
         :link: https://arxiv.org/abs/2303.03991
         :class-card: sd-border-secondary

         **Wang et al., 2023**

         Open-source occupancy prediction benchmark and augmented annotation
         framework for nuScenes.


.. dropdown:: Multi-Camera Fusion
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: BEVFusion (MIT)
         :link: https://arxiv.org/abs/2205.13542
         :class-card: sd-border-secondary

         **Liu et al., ICRA 2023**

         Efficient LiDAR-camera BEV fusion using a shared BEV feature space
         with camera-to-BEV transformation.

      .. grid-item-card:: BEVFusion (Nanjing)
         :link: https://arxiv.org/abs/2205.13790
         :class-card: sd-border-secondary

         **Liang et al., NeurIPS 2022**

         Multi-task multi-sensor fusion for 3D detection, segmentation,
         and map prediction in BEV space.

      .. grid-item-card:: Cross-View Transformers
         :link: https://arxiv.org/abs/2205.02833
         :class-card: sd-border-secondary

         **Zhou & Krähenbühl, NeurIPS 2022**

         Attention-based cross-view feature aggregation for BEV semantic
         map prediction from surround cameras.


.. dropdown:: Datasets and Benchmarks
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: nuScenes Dataset
         :link: https://www.nuscenes.org/
         :class-card: sd-border-secondary

         **Caesar et al., CVPR 2020**

         1000-scene dataset with 6-camera surround, LiDAR, RADAR, and
         3D bounding box + tracking annotations.

         +++

         - `Object Detection Leaderboard <https://nuscenes.org/object-det>`_
         - `Occupancy Prediction Benchmark <https://github.com/nutonomy/nuscenes-devkit>`_

      .. grid-item-card:: Waymo Open Dataset
         :link: https://waymo.com/open/
         :class-card: sd-border-secondary

         **Sun et al., CVPR 2020**

         1,950 scenes with 5-camera, 5-LiDAR sensor setup and high-quality
         3D annotations including occupancy flow.


.. dropdown:: Industry Resources
   :class-container: sd-border-secondary

   - `Tesla AI Day 2022 -- Occupancy Networks <https://youtu.be/ODSJsviD_SU>`_
   - `Andrej Karpathy: Tesla Autopilot and Multi-Task Learning <https://www.youtube.com/watch?v=hx7BXih7zx8>`_
   - `Waymo Research Blog -- Perception <https://waymo.com/research/>`_
   - `nuScenes Detection Metric Definition <https://www.nuscenes.org/object-det>`_


.. dropdown:: Textbooks and Survey Papers
   :class-container: sd-border-secondary

   - Ma, Y. et al. (2022). *Vision-Centric BEV Perception: A Survey.*
     arXiv:2208.02797.
   - Li, Z. et al. (2022). *Delving into the Devils of Bird's-Eye-View
     Perception: A Review, Evaluation and Recipe.* IEEE TPAMI.
   - Mao, J. et al. (2023). *A Survey on Occupancy Prediction for Autonomous
     Driving.* arXiv:2305.07922.
