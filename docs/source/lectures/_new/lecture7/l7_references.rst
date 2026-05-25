====================================================
References
====================================================


.. dropdown:: Localization Fundamentals
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Probabilistic Robotics
         :link: https://probabilistic-robotics.org/
         :class-card: sd-border-secondary

         **Thrun, Burgard & Fox (2005)**

         The definitive reference for probabilistic localization and SLAM.
         Chapters 4-7 cover EKF localization, particle filter, and SLAM.

      .. grid-item-card:: State Estimation for Robotics
         :link: https://www.cambridge.org/core/books/state-estimation-for-robotics/
         :class-card: sd-border-secondary

         **Barfoot (2017)**

         Rigorous treatment of state estimation using Lie groups (SE(3)),
         Kalman filters, and factor graphs. Graduate-level reference.

      .. grid-item-card:: Monte Carlo Localization
         :link: https://papers.nips.cc/paper/1998/hash/c88d8d0a6097754525e02c2246d8d27f-Abstract.html
         :class-card: sd-border-secondary

         **Dellaert et al. (1999)**

         Original MCL paper. Landmark paper introducing particle filter
         localization for mobile robots.

      .. grid-item-card:: AMCL (ROS)
         :link: https://wiki.ros.org/amcl
         :class-card: sd-border-secondary

         **ROS Navigation Stack**

         Adaptive Monte Carlo Localization implementation. Standard
         localization package for ROS-based robots.


.. dropdown:: Scan Matching and ICP
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ICP (Besl & McKay, 1992)
         :link: https://ieeexplore.ieee.org/document/121791
         :class-card: sd-border-secondary

         **Besl & McKay, TPAMI 1992**

         Original point-to-point ICP paper. Foundation of all scan
         matching approaches.

      .. grid-item-card:: Point-to-Plane ICP
         :link: https://www.cs.princeton.edu/~smr/papers/icpstability.pdf
         :class-card: sd-border-secondary

         **Chen & Medioni, 1992 / Low, 2004**

         Point-to-plane variant with faster convergence on planar surfaces.

      .. grid-item-card:: NDT (Normal Distributions Transform)
         :link: https://ieeexplore.ieee.org/document/1249285
         :class-card: sd-border-secondary

         **Biber & Strasser, IROS 2003**

         NDT represents the target as a grid of Gaussians. Robust to
         outliers; used in Autoware for LiDAR localization.

      .. grid-item-card:: GICP
         :link: https://journals.sagepub.com/doi/10.1177/0278364910388359
         :class-card: sd-border-secondary

         **Segal et al., RSS 2009**

         Generalized ICP: maximum-likelihood formulation treating both
         clouds as Gaussian distributions.

      .. grid-item-card:: Open3D
         :link: http://www.open3d.org/
         :class-card: sd-border-secondary

         **Zhou, Park & Koltun (2018)**

         Open-source library for 3D data processing. Includes ICP,
         RANSAC, point cloud visualization, and mesh tools.

         +++

         - `ICP Tutorial <http://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html>`_


.. dropdown:: LiDAR SLAM Systems
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: LOAM
         :link: https://www.ri.cmu.edu/pub_files/2014/7/Ji_LidarMapping_RSS2014_v8.pdf
         :class-card: sd-border-secondary

         **Zhang & Singh, RSS 2014**

         LiDAR Odometry and Mapping. Feature-based LiDAR SLAM. Seminal
         paper achieving top results on KITTI at publication.

      .. grid-item-card:: LeGO-LOAM
         :link: https://github.com/RobustFieldAutonomyLab/LeGO-LOAM
         :class-card: sd-border-secondary

         **Shan & Englot, IROS 2018**

         Lightweight and Ground-Optimized LOAM. Adds explicit ground
         segmentation and pose graph backend with loop closure.

         +++

         - `LeGO-LOAM on GitHub <https://github.com/RobustFieldAutonomyLab/LeGO-LOAM>`_

      .. grid-item-card:: LIO-SAM
         :link: https://arxiv.org/abs/2007.00258
         :class-card: sd-border-secondary

         **Shan et al., IROS 2020**

         Tightly-coupled LiDAR-IMU SLAM via factor graph smoothing.
         Current state-of-the-art for outdoor LiDAR SLAM.

         +++

         - `LIO-SAM on GitHub <https://github.com/TixiaoShan/LIO-SAM>`_

      .. grid-item-card:: KISS-ICP
         :link: https://arxiv.org/abs/2209.15397
         :class-card: sd-border-secondary

         **Vizzo et al., RA-L 2023**

         Simple adaptive threshold ICP achieving competitive accuracy
         with minimal complexity. Winner of multiple SLAM benchmarks.

         +++

         - `KISS-ICP on GitHub <https://github.com/PRBonn/kiss-icp>`_


.. dropdown:: SLAM Backends and Factor Graphs
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: g2o
         :link: https://github.com/RainerKuemmerle/g2o
         :class-card: sd-border-secondary

         **Kümmerle et al., ICRA 2011**

         General framework for graph-based nonlinear optimization.
         Standard backend for 2D and 3D SLAM pose graphs.

      .. grid-item-card:: GTSAM
         :link: https://gtsam.org/
         :class-card: sd-border-secondary

         **Dellaert & GTSAM Contributors**

         Georgia Tech Smoothing and Mapping library. Factor graph
         framework supporting IMU, GPS, LiDAR, and visual factors.

         +++

         - `Python API <https://gtsam.org/docs/python.html>`_

      .. grid-item-card:: Scan Context
         :link: https://arxiv.org/abs/2109.13494
         :class-card: sd-border-secondary

         **Kim & Kim, IROS 2018 / TITS 2021**

         Compact global descriptor for LiDAR-based place recognition.
         Rotation-invariant and efficient for large-scale retrieval.


.. dropdown:: Datasets and Evaluation
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: KITTI Odometry Benchmark
         :link: https://www.cvlibs.net/datasets/kitti/eval_odometry.php
         :class-card: sd-border-secondary

         **Geiger et al., IJRR 2013**

         Standard LiDAR SLAM evaluation benchmark with 22 sequences.

      .. grid-item-card:: EVO Trajectory Evaluation
         :link: https://github.com/MichaelGrupp/evo
         :class-card: sd-border-secondary

         **Grupp (2017)**

         Python tool for evaluating SLAM trajectories (APE, RPE).
         Supports TUM, KITTI, EuRoC, and ROS bag formats.

      .. grid-item-card:: MulRan Dataset
         :link: https://sites.google.com/view/mulran-pr/
         :class-card: sd-border-secondary

         **Kim et al., ICRA 2020**

         Multi-experience range dataset for place recognition evaluation
         across seasons and conditions.
