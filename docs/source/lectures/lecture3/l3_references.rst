====================================================
References
====================================================


.. dropdown:: Formal Definitions: Variance and Confidence
   :class-container: sd-border-secondary
   :open:

   These are the sources behind the definitions in the **Words We Need
   First** section of the lecture. The first two are standards documents
   rather than textbooks, so they are the ones to quote if anyone asks you
   what a term officially means.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Statistics vocabulary
         :link: https://www.iso.org/standard/40145.html
         :class-card: sd-border-secondary

         **ISO 3534-1:2006**

         *Statistics. Vocabulary and symbols. Part 1: General statistical
         terms and terms used in probability.*

         The standards body definitions of **variance**, **standard
         deviation**, **confidence interval** and **confidence level**.

      .. grid-item-card:: Measurement uncertainty
         :link: https://www.bipm.org/en/committees/jc/jcgm/publications
         :class-card: sd-border-secondary

         **JCGM 100:2008 (GUM)** and **JCGM 200:2012 (VIM)**

         *Guide to the Expression of Uncertainty in Measurement*, and the
         *International Vocabulary of Metrology*.

         VIM is the same document L2 quoted for the definition of
         calibration. Both deliberately avoid the word "confidence" and use
         **coverage interval** and **coverage probability** instead.

         +++

         Free to download from the BIPM.

      .. grid-item-card:: Probability and statistics
         :class-card: sd-border-secondary

         **Casella, G. and Berger, R. L. (2002)**

         *Statistical Inference*, 2nd edition. Duxbury.

         The standard graduate treatment of variance, estimators and
         confidence intervals.

      .. grid-item-card:: Credible intervals
         :class-card: sd-border-secondary

         **Gelman, A. et al. (2013)**

         *Bayesian Data Analysis*, 3rd edition. CRC Press.

         Credible regions, which is what a Kalman filter's covariance
         ellipse actually is. Chapter 1 covers the distinction from
         confidence intervals directly.


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
         Transactions of the ASME, Journal of Basic Engineering.

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


.. dropdown:: Filter Consistency and Divergence
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The standard reference
         :class-card: sd-border-secondary

         **Bar-Shalom, Y., Li, X.-R., & Kirubarajan, T. (2001)**

         *Estimation with Applications to Tracking and Navigation.* Wiley.

         The definitive treatment of filter **consistency**: NIS, NEES,
         and the chi-square tests used in this lecture. If you read one
         thing beyond the notes, read the consistency chapter.

      .. grid-item-card:: Divergence
         :link: https://ieeexplore.ieee.org/document/1099836
         :class-card: sd-border-secondary

         **Fitzgerald, R.J. (1971)**

         *Divergence of the Kalman Filter.* IEEE Transactions on Automatic
         Control, 16(6).

         The classic analysis of why a filter becomes confidently wrong,
         and why shrinking :math:`P` is the mechanism.

      .. grid-item-card:: Tuning Q and R
         :link: https://ieeexplore.ieee.org/document/1099422
         :class-card: sd-border-secondary

         **Mehra, R.K. (1970)**

         *On the Identification of Variances and Adaptive Kalman
         Filtering.* IEEE Transactions on Automatic Control, 15(2).

         The origin of adaptive noise-covariance estimation. Useful
         background on why :math:`Q` resists measurement.

      .. grid-item-card:: Gating in practice
         :class-card: sd-border-secondary

         **Blackman, S. & Popoli, R. (1999)**

         *Design and Analysis of Modern Tracking Systems.* Artech House.

         Practical treatment of validation gates, track lifecycle and
         M-of-N confirmation logic as actually deployed.


.. dropdown:: Survey Papers
   :class-container: sd-border-secondary

   - Faion, F. et al. (2021). *A Survey on Data Fusion Techniques for
     Autonomous Driving.* IEEE Intelligent Transportation Systems Magazine.
   - Yeong, D.J. et al. (2021). *Sensor and Sensor Fusion Technology in
     Autonomous Vehicles: A Review.* Sensors, 21(6), 2140.
   - Liang, M. et al. (2022). *BEVFusion: A Simple and Robust LiDAR-Camera
     Fusion Framework.* arXiv:2205.13790.
