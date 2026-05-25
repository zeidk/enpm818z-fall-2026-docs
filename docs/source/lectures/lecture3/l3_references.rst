====================================================
References
====================================================


.. dropdown:: Kalman Filter Theory
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Original Kalman Filter Paper
         :link: https://www.cs.unc.edu/~welch/kalman/media/pdf/Kalman1960.pdf
         :class-card: sd-border-secondary

         **Kalman, R.E. (1960)**

         "A New Approach to Linear Filtering and Prediction Problems."
         Transactions of the ASME -- Journal of Basic Engineering.

      .. grid-item-card:: EKF and UKF Overview
         :link: https://groups.seas.harvard.edu/courses/cs281/papers/unscented.pdf
         :class-card: sd-border-secondary

         **Julier & Uhlmann (1997)**

         "A New Extension of the Kalman Filter to Nonlinear Systems."
         The paper introducing the Unscented Transform and UKF.

      .. grid-item-card:: Probabilistic Robotics
         :link: https://probabilistic-robotics.org/
         :class-card: sd-border-secondary

         **Thrun, Burgard & Fox (2005)**

         The definitive textbook on probabilistic robotics. Chapters 3-4
         cover Kalman filters, EKF, UKF, and particle filters in depth.

      .. grid-item-card:: filterpy Python Library
         :link: https://filterpy.readthedocs.io/
         :class-card: sd-border-secondary

         **Roger Labbe**

         Python library implementing KF, EKF, UKF, and particle filters.
         Companion to the "Kalman and Bayesian Filters in Python" textbook.

         +++

         - `GitHub <https://github.com/rlabbe/filterpy>`_
         - `Jupyter Book <https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python>`_


.. dropdown:: Multi-Sensor Fusion Architectures
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: BEVFusion (MIT)
         :link: https://arxiv.org/abs/2205.13542
         :class-card: sd-border-secondary

         **Liu et al., ICRA 2023**

         Efficient LiDAR-camera BEV fusion using shared BEV space with
         cross-attention feature fusion. 70.2 NDS on nuScenes.

      .. grid-item-card:: BEVFusion (Nanjing)
         :link: https://arxiv.org/abs/2205.13790
         :class-card: sd-border-secondary

         **Liang et al., NeurIPS 2022**

         Multi-task multi-sensor fusion for detection, map segmentation,
         and motion prediction in unified BEV space.

      .. grid-item-card:: DeepFusion
         :link: https://arxiv.org/abs/2203.08195
         :class-card: sd-border-secondary

         **Li et al., CVPR 2022**

         LiDAR-camera fusion using point-to-voxel cross-attention for
         3D object detection.

      .. grid-item-card:: CenterFusion
         :link: https://arxiv.org/abs/2011.04841
         :class-card: sd-border-secondary

         **Nabati & Qi, WACV 2021**

         Camera-RADAR fusion for 3D object detection using pillar-based
         radar point cloud association.


.. dropdown:: Data Association
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Hungarian Algorithm
         :link: https://en.wikipedia.org/wiki/Hungarian_algorithm
         :class-card: sd-border-secondary

         **Kuhn-Munkres Algorithm**

         Optimal bipartite graph matching in O(n^3). Standard for global
         nearest neighbor data association.

         +++

         - `scipy.optimize.linear_sum_assignment <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html>`_

      .. grid-item-card:: JPDA Survey
         :link: https://ieeexplore.ieee.org/document/989947
         :class-card: sd-border-secondary

         **Fortmann, Bar-Shalom & Scheffe (1983)**

         Original Joint Probabilistic Data Association paper for tracking
         in cluttered environments.

      .. grid-item-card:: Bar-Shalom et al.
         :class-card: sd-border-secondary

         **Bar-Shalom, Y., Willett, P.K., & Tian, X. (2011)**

         *Tracking and Data Fusion: A Handbook of Algorithms.*
         YBS Publishing. Comprehensive reference for all association methods.


.. dropdown:: Particle Filters
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Monte Carlo Localization
         :link: https://people.eecs.berkeley.edu/~pabbeel/cs287-fa12/slides/mcl.pdf
         :class-card: sd-border-secondary

         **Dellaert et al. (1999)**

         Original MCL paper: particle filter for robot localization.
         Foundation of AMCL used in ROS.

      .. grid-item-card:: Particle Filters Tutorial
         :link: https://www.irisa.fr/aspi/legland/ref/arulampalam02a.pdf
         :class-card: sd-border-secondary

         **Arulampalam et al. (2002)**

         "A Tutorial on Particle Filters for Online Nonlinear/Non-Gaussian
         Bayesian Tracking." IEEE Transactions on Signal Processing.


.. dropdown:: Survey Papers
   :class-container: sd-border-secondary

   - Faion, F. et al. (2021). *A Survey on Data Fusion Techniques for
     Autonomous Driving.* IEEE Intelligent Transportation Systems Magazine.
   - Yeong, D.J. et al. (2021). *Sensor and Sensor Fusion Technology in
     Autonomous Vehicles: A Review.* Sensors, 21(6), 2140.
   - Liang, M. et al. (2022). *BEVFusion: A Simple and Robust LiDAR-Camera
     Fusion Framework.* arXiv:2205.13790.
