====================================================
References
====================================================


.. dropdown:: Semantic Segmentation
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: U-Net
         :link: https://arxiv.org/abs/1505.04597
         :class-card: sd-border-secondary

         **Ronneberger et al., MICCAI 2015**

         Encoder-decoder with skip connections. The foundational architecture
         for dense prediction tasks.

      .. grid-item-card:: DeepLabv3+
         :link: https://arxiv.org/abs/1802.02611
         :class-card: sd-border-secondary

         **Chen et al., ECCV 2018**

         Atrous convolutions and ASPP for multi-scale context. State-of-the-art
         semantic segmentation architecture.

      .. grid-item-card:: SegFormer
         :link: https://arxiv.org/abs/2105.15203
         :class-card: sd-border-secondary

         **Xie et al., NeurIPS 2021**

         Transformer-based segmentation with hierarchical feature extraction
         and a lightweight MLP decoder head.

      .. grid-item-card:: CLRNet (Lane Detection)
         :link: https://arxiv.org/abs/2203.10350
         :class-card: sd-border-secondary

         **Zheng et al., CVPR 2022**

         Cross Layer Refinement Network for accurate lane detection using
         lane-specific prior and multi-scale feature fusion.


.. dropdown:: Instance and Panoptic Segmentation
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Mask R-CNN
         :link: https://arxiv.org/abs/1703.06870
         :class-card: sd-border-secondary

         **He et al., ICCV 2017**

         Extends Faster R-CNN with a mask prediction head. Foundation of
         instance segmentation.

      .. grid-item-card:: Panoptic Segmentation
         :link: https://arxiv.org/abs/1801.00868
         :class-card: sd-border-secondary

         **Kirillov et al., CVPR 2019**

         Defines the panoptic segmentation task and the PQ metric.

      .. grid-item-card:: Panoptic-DeepLab
         :link: https://arxiv.org/abs/1911.10194
         :class-card: sd-border-secondary

         **Cheng et al., CVPR 2020**

         Bottom-up panoptic segmentation with semantic and instance
         prediction branches.


.. dropdown:: Multi-Object Tracking
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: SORT
         :link: https://arxiv.org/abs/1602.00763
         :class-card: sd-border-secondary

         **Bewley et al., ICIP 2016**

         Simple Online and Realtime Tracking using Kalman filter and
         Hungarian algorithm. Runs at 260 Hz.

      .. grid-item-card:: DeepSORT
         :link: https://arxiv.org/abs/1703.07402
         :class-card: sd-border-secondary

         **Wojke et al., ICIP 2017**

         Extends SORT with a deep appearance descriptor for robust
         re-identification after occlusion.

      .. grid-item-card:: ByteTrack
         :link: https://arxiv.org/abs/2110.06864
         :class-card: sd-border-secondary

         **Zhang et al., ECCV 2022**

         Uses every detection including low-confidence ones for robust
         tracking. State-of-the-art on MOT17.

      .. grid-item-card:: StrongSORT
         :link: https://arxiv.org/abs/2202.13514
         :class-card: sd-border-secondary

         **Du et al., 2022**

         Enhanced SORT with better Kalman filter motion model and stronger
         appearance features for improved performance.


.. dropdown:: Datasets and Benchmarks
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: MOTChallenge
         :link: https://motchallenge.net/
         :class-card: sd-border-secondary

         **Benchmark for MOT evaluation**

         MOT17 and MOT20 datasets with standardized MOTA/IDF1 evaluation.

         +++

         - `Leaderboard <https://motchallenge.net/results/MOT17/>`_

      .. grid-item-card:: Cityscapes
         :link: https://www.cityscapes-dataset.com/
         :class-card: sd-border-secondary

         **Cordts et al., CVPR 2016**

         5000 finely annotated urban driving images for semantic and
         instance segmentation benchmarking.

      .. grid-item-card:: nuScenes Panoptic
         :link: https://nuscenes.org/panoptic
         :class-card: sd-border-secondary

         **Fong et al., CVPR 2022**

         Panoptic segmentation annotations for the nuScenes LiDAR point
         clouds, enabling 3D panoptic benchmarking.


.. dropdown:: Survey Papers and Textbooks
   :class-container: sd-border-secondary

   - Garcia-Garcia, A. et al. (2018). *A Survey on Deep Learning Techniques
     for Image and Video Semantic Segmentation.* Applied Soft Computing.
   - Luo, W. et al. (2021). *Multiple Object Tracking: A Literature Review.*
     Artificial Intelligence, 293.
   - Ciaparrone, G. et al. (2020). *Deep Learning in Video Multi-Object
     Tracking: A Survey.* Neurocomputing, 381.
   - HOTA metric: Luiten, J. et al. (2021). *HOTA: A Higher Order Metric for
     Evaluating Multi-Object Tracking.* IJCV.
