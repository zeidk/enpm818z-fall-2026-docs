====================================================
References
====================================================

These are the sources the L3 slides cite, in the order the slides cite
them, grouped by topic. A last dropdown lists further reading from the
lecture's bibliography that no slide cites.


.. dropdown:: Formal Definitions: Uncertainty, Noise and Bias
   :class-container: sd-border-secondary
   :open:

   These are the sources behind the definitions in the **Terminology**
   section and its appendix. All three are standards documents rather than
   textbooks, so they are the ones to quote if anyone asks you what a term
   officially means.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Metrology vocabulary
         :link: https://www.bipm.org/en/committees/jc/jcgm/publications
         :class-card: sd-border-secondary

         **JCGM 200:2012 (VIM)**

         *International Vocabulary of Metrology: Basic and General
         Concepts and Associated Terms.* BIPM, 2012.

         The definition of **measurement uncertainty** (clause 2.26) on the
         Uncertainty slide, and of **precision** (2.15, the word for noise)
         and **trueness** (2.14, the word for bias). The same document L2
         quoted for the definition of calibration.

         +++

         Free to download from the BIPM.

      .. grid-item-card:: Measurement uncertainty
         :link: https://www.bipm.org/en/committees/jc/jcgm/publications
         :class-card: sd-border-secondary

         **JCGM 100:2008 (GUM)**

         *Evaluation of Measurement Data: Guide to the Expression of
         Uncertainty in Measurement.* BIPM, 2008.

         With the VIM, it avoids the word "confidence" and says
         **coverage interval** and **coverage probability** instead (the
         confidence-interval slides in the appendix).

         +++

         Free to download from the BIPM.

      .. grid-item-card:: Accuracy, trueness and precision
         :class-card: sd-border-secondary

         **ISO 5725-1:2023**

         *Accuracy (Trueness and Precision) of Measurement Methods and
         Results. Part 1: General Principles and Definitions.* ISO, 2023.

         Uses **accuracy** as the umbrella term: a reading is accurate only
         if the bias is small **and** the noise is small.


.. dropdown:: Filters
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The Kalman filter
         :link: https://doi.org/10.1115/1.3662552
         :class-card: sd-border-secondary

         **Kalman, R. E. (1960)**

         "A New Approach to Linear Filtering and Prediction Problems."
         *Journal of Basic Engineering*, 82(1), 35 to 45.

         The paper behind the Kalman filter definition: a recursive
         estimator that predicts and updates, and has the smallest
         expected squared error when the models are linear and the noise
         is Gaussian.

      .. grid-item-card:: The unscented transform and the UKF
         :link: https://doi.org/10.1117/12.280797
         :class-card: sd-border-secondary

         **Julier, S. J. and Uhlmann, J. K. (1997)**

         "A New Extension of the Kalman Filter to Nonlinear Systems."
         *Proceedings of SPIE 3068, Signal Processing, Sensor Fusion, and
         Target Recognition VI*, 182 to 193.

         The source of the **sigma points**: :math:`2n+1` points whose
         weighted average is the mean and whose weighted spread is the
         covariance (UKF appendix).

      .. grid-item-card:: Monte Carlo Localization
         :link: https://doi.org/10.1109/ROBOT.1999.772544
         :class-card: sd-border-secondary

         **Dellaert, F., Fox, D., Burgard, W. and Thrun, S. (1999)**

         "Monte Carlo Localization for Mobile Robots." *Proceedings of the
         IEEE International Conference on Robotics and Automation (ICRA)*,
         1322 to 1328.

         The particle filter applied to robot localization (particle filter
         appendix). Monte Carlo Localization itself is
         L6.


.. dropdown:: Checking the Covariance
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The standard reference
         :class-card: sd-border-secondary

         **Bar-Shalom, Y., Li, X.-R. and Kirubarajan, T. (2001)**

         *Estimation with Applications to Tracking and Navigation: Theory,
         Algorithms and Software.* Wiley, New York.

         The source of the **NIS** consistency test and the chi-square band
         used in the last section of the lecture, and of the notation
         :math:`\nu` for the innovation (other textbooks write
         :math:`\mathbf{y}`).


.. dropdown:: Further Reading
   :class-container: sd-border-secondary

   These are in the lecture's bibliography file but are not cited on a
   slide.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Probabilistic Robotics
         :link: https://probabilistic-robotics.org/
         :class-card: sd-border-secondary

         **Thrun, S., Burgard, W. and Fox, D. (2005)**

         *Probabilistic Robotics.* MIT Press, Cambridge, MA.

         Chapters 3 and 4 cover the Kalman filter, EKF, UKF and particle
         filter in depth.

      .. grid-item-card:: Statistics vocabulary
         :link: https://www.iso.org/standard/40145.html
         :class-card: sd-border-secondary

         **ISO 3534-1:2006**

         *Statistics: Vocabulary and Symbols. Part 1: General Statistical
         Terms and Terms Used in Probability.* ISO, 2006.

         The standards body definitions of **variance**, **standard
         deviation**, **confidence interval** and **confidence level**.

      .. grid-item-card:: Probability and statistics
         :class-card: sd-border-secondary

         **Casella, G. and Berger, R. L. (2002)**

         *Statistical Inference*, 2nd edition. Duxbury, Pacific Grove, CA.

         The standard graduate treatment of variance, estimators and
         confidence intervals.

      .. grid-item-card:: Credible intervals
         :class-card: sd-border-secondary

         **Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari,
         A. and Rubin, D. B. (2013)**

         *Bayesian Data Analysis*, 3rd edition. CRC Press, Boca Raton, FL.

         Credible regions, and how they differ from confidence intervals.

      .. grid-item-card:: CARLA
         :link: https://proceedings.mlr.press/v78/dosovitskiy17a.html
         :class-card: sd-border-secondary

         **Dosovitskiy, A., Ros, G., Codevilla, F., López, A. and
         Koltun, V. (2017)**

         "CARLA: An Open Urban Driving Simulator." *Proceedings of the 1st
         Annual Conference on Robot Learning (CoRL)*, PMLR 78, 1 to 16.

         The simulator set up in L2.

   The bibliography file also holds the sources for Mahalanobis distance,
   the Hungarian algorithm, JPDA, MHT and the Tempe crash report. Those
   topics are taught in L5.
