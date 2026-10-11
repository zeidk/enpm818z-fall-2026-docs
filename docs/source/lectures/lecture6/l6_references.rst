====================================================
References
====================================================

These are the sources the L6 slides cite, grouped by topic, in the order the
slides first cite each group. A source cited in several sections is listed
once, where the slides first cite it. Every entry of the lecture's
bibliography is cited by a slide. Three of them are cited only in the
appendix (:doc:`l6_appendix`), and they have their own group at the end:
Kabsch, Thrun et al., and Zhang and Scaramuzza.

.. tip::

   Two to read first: Reid et al. (2019) for the accuracy requirement, and
   the tutorial by Grisetti et al. (2010) for the pose graph.


.. dropdown:: Localization Requirements
   :class-container: sd-border-secondary
   :open:

   The Introduction: how good a localizer must be. The same bound returns in
   Dead Reckoning and as the alert limit in Integrity.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Localization requirements
         :link: https://doi.org/10.4271/12-02-03-0012
         :class-card: sd-border-secondary

         **Reid, T. G. R., Houts, S. E., Cammarata, R., Mills, G., Agarwal,
         S., Vora, A. and Pandey, G. (2019)**

         "Localization Requirements for Autonomous Vehicles." *SAE
         International Journal of Connected and Automated Vehicles*, 2(3),
         173 to 190. doi:10.4271/12-02-03-0012. arXiv:1906.01061.

         For a passenger car on local streets, "lateral and longitudinal
         error bounds of 0.29 m (0.10 m, 95%)"; on freeways, "a required
         lateral error bound of 0.57 m (0.20 m, 95%)", derived at a failure
         rate of :math:`10^{-8}` per hour of driving.


.. dropdown:: GNSS and RTK
   :class-container: sd-border-secondary
   :open:

   What RTK is, how close it gets, where it works, and who provides it in
   Maryland. Also cited in the appendix on RTK.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: RTK
         :link: https://gssc.esa.int/navipedia/index.php/Real_Time_Kinematics
         :class-card: sd-border-secondary

         **GMV (2011)**

         *Real Time Kinematics.* European Space Agency, Navipedia. Accessed
         10 October 2026.

         RTK as "a differential GNSS technique" with "carrier measurements"
         and corrections from a base station; "performances in the range of
         a few centimetres", "in the vicinity of a base station"; "the
         ionospheric delay and the tropospheric delay" among the errors that
         cancel; it "can be used for distances of up to 10 or 20
         kilometres".

      .. grid-item-card:: Multipath
         :link: https://gssc.esa.int/navipedia/index.php/Multipath
         :class-card: sd-border-secondary

         **Sanz Subirana, J., Juan Zornoza, J. M., Hernández-Pajares, M.
         (2011)**

         *Multipath.* European Space Agency, Navipedia (Technical University
         of Catalonia). Accessed 10 October 2026.

         "The interference by multipath is generated when a signal arrives,
         by different ways, at the antenna." "Its principal cause is the
         antenna closeness to the reflecting structures".

      .. grid-item-card:: GPS and the other GNSS
         :link: https://www.gps.gov/other-global-navigation-satellite-systems-gnss
         :class-card: sd-border-secondary

         **U.S. Government, GPS.gov**

         *Other Global Navigation Satellite Systems (GNSS)* and the GPS.gov home
         page (https://www.gps.gov/). Accessed 10 October 2026.

         GNSS is "a general term describing any satellite constellation"; GPS
         is "a U.S.-owned utility", "operated and maintained by the U.S. Space
         Force".

      .. grid-item-card:: Where the IMU goes
         :link: https://support-centre.racelogic.co.uk/automotive/imu/imu05-imu05s/ug/mounting/
         :class-card: sd-border-secondary

         **Racelogic (2026)**

         *Mounting: IMU05/IMU05-S User Guide.* Racelogic Support Centre,
         updated 21 September 2026. Accessed 10 October 2026.

         On the roof "co-located with the GNSS antenna", or inside on the seat
         rails; IMU and antenna "on the same rigid body".

      .. grid-item-card:: The IMU
         :link: https://arxiv.org/abs/2603.07143
         :class-card: sd-border-secondary

         **Berkane, S. (2026)**

         *Tutorial on Aided Inertial Navigation Systems: A Modern Treatment
         Using Lie-Group Theoretical Methods.* Technical report
         LaRSA-TR-2026-01, Robotics and Autonomous Systems Laboratory,
         Université du Québec en Outaouais. arXiv:2603.07143, version 2.

         The IMU "typically consists of three orthogonally mounted gyroscopes
         and three accelerometers".

      .. grid-item-card:: Who steers in CARLA
         :link: https://carla.readthedocs.io/en/0.9.16/adv_traffic_manager/
         :class-card: sd-border-secondary

         **CARLA Team**

         *Traffic Manager (CARLA 0.9.16).* Accessed 11 October 2026.

         A PID controller "estimates the throttle, brake, and steering input
         needed to reach a target value", from the simulation's state and the
         map's waypoints.

      .. grid-item-card:: Real-time networks in Maryland
         :link: https://fig.net/resources/proceedings/fig_proceedings/fig2019/papers/ts05e/TS05E_gillins_heck_et_al_10077.pdf
         :class-card: sd-border-secondary

         **Gillins, D., Heck, J., Scott, G., Jordan, K., Hippenstiel, R.
         (2019)**

         *Accuracy of GNSS Observations from Three Real-Time Networks in
         Maryland, USA.* FIG Working Week 2019, Hanoi, Vietnam, paper 10077.

         "In Maryland of the United States, three independent RTNs are
         available": Trimble KeyNetGPS, Topcon TopNET live and Leica
         SmartNet. A single base station "generally limits baseline lengths
         to less than 20 km", because farther away "atmospheric delay errors
         do not sufficiently cancel"; networks space their bases "every 70
         km or less".

      .. grid-item-card:: NOAA CORS Network
         :link: https://geodesy.noaa.gov/CORS/
         :class-card: sd-border-secondary

         **NOAA National Geodetic Survey**

         *The NOAA CORS Network (NCN).* Accessed 10 October 2026. Station
         map: https://arcg.is/18fWq8.

         Reference stations whose GNSS data improve the precision of
         positions after the fact.


.. dropdown:: Fusion in the EKF
   :class-container: sd-border-secondary
   :open:

   One number to score a whole run. Also cited in the appendix on APE and
   RPE.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: APE and RPE
         :link: https://doi.org/10.1109/IROS.2012.6385773
         :class-card: sd-border-secondary

         **Sturm, J., Engelhard, N., Endres, F., Burgard, W. and Cremers, D.
         (2012)**

         "A Benchmark for the Evaluation of RGB-D SLAM Systems."
         *Proceedings of the IEEE/RSJ International Conference on
         Intelligent Robots and Systems (IROS)*, 573 to 580.
         doi:10.1109/IROS.2012.6385773.

         The absolute pose error (APE) summarized by the RMSE; in the
         appendix, the relative pose error (RPE) as the drift.


.. dropdown:: Against a Map
   :class-container: sd-border-secondary
   :open:

   Matching the LiDAR scan to a map: MCL, ICP, and the scan matcher a real
   stack runs.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Monte Carlo localization
         :link: https://doi.org/10.1109/ROBOT.1999.772544
         :class-card: sd-border-secondary

         **Dellaert, F., Fox, D., Burgard, W. and Thrun, S. (1999)**

         "Monte Carlo Localization for Mobile Robots." *Proceedings of the
         IEEE International Conference on Robotics and Automation (ICRA)*,
         1322 to 1328. doi:10.1109/ROBOT.1999.772544.

         MCL: each particle is one guess of the pose; predict, weigh,
         resample.

      .. grid-item-card:: ICP
         :link: https://doi.org/10.1109/34.121791
         :class-card: sd-border-secondary

         **Besl, P. J. and McKay, N. D. (1992)**

         "A Method for Registration of 3-D Shapes." *IEEE Transactions on
         Pattern Analysis and Machine Intelligence*, 14(2), 239 to 256.
         doi:10.1109/34.121791.

         Iterative closest point: guess the pairs from the nearest points,
         solve, move, guess again.

      .. grid-item-card:: Random particles for relocalization
         :link: https://rse-lab.cs.washington.edu/papers/sampling-aaai-99.pdf
         :class-card: sd-border-secondary

         **Fox, D., Burgard, W., Dellaert, F. and Thrun, S. (1999)**

         "Monte Carlo Localization: Efficient Position Estimation for Mobile
         Robots." *AAAI-99*, 343 to 349.

         "The added samples are essential for relocalization in the rare event
         that the robot loses track of its position."

      .. grid-item-card:: Robust MCL
         :link: https://doi.org/10.1016/S0004-3702(01)00069-8
         :class-card: sd-border-secondary

         **Thrun, S., Fox, D., Burgard, W. and Dellaert, F. (2001)**

         "Robust Monte Carlo Localization for Mobile Robots." *Artificial
         Intelligence*, 128(1 to 2), 99 to 141.

         Adding random samples and similar fixes are "mathematically
         questionable".

      .. grid-item-card:: KLD sampling
         :link: https://doi.org/10.1177/0278364903022012001
         :class-card: sd-border-secondary

         **Fox, D. (2003)**

         "Adapting the Sample Size in Particle Filters Through KLD-Sampling."
         *The International Journal of Robotics Research*, 22(12), 985 to 1003.

         "A small number of samples if the density is focused", a large number
         when the samples must cover a large part of the space.

      .. grid-item-card:: The k-d tree
         :link: https://doi.org/10.1145/361002.361007
         :class-card: sd-border-secondary

         **Bentley, J. L. (1975)**

         "Multidimensional Binary Search Trees Used for Associative
         Searching." *Communications of the ACM*, 18(9), 509 to 517.

         The k-d tree: split on one key per level, the keys taken in turn.

      .. grid-item-card:: Nearest neighbors in log N
         :link: https://doi.org/10.1145/355744.355745
         :class-card: sd-border-secondary

         **Friedman, J. H., Bentley, J. L. and Finkel, R. A. (1977)**

         "An Algorithm for Finding Best Matches in Logarithmic Expected Time."
         *ACM Transactions on Mathematical Software*, 3(3), 209 to 226.

         "The expected computation to perform each search is proportional to
         logN."

      .. grid-item-card:: Point to plane
         :link: https://doi.org/10.1109/ROBOT.1991.132043
         :class-card: sd-border-secondary

         **Chen, Y. and Medioni, G. (1991)**

         "Object Modeling by Registration of Multiple Range Images." *IEEE
         ICRA*, 2724 to 2729.

         "We minimize the distance from points to planes."

      .. grid-item-card:: Point to line
         :link: https://doi.org/10.1109/ROBOT.2008.4543181
         :class-card: sd-border-secondary

         **Censi, A. (2008)**

         "An ICP Variant Using a Point-to-Line Metric." *IEEE ICRA*, 19 to 25.

         "PLICP is more precise, and requires less iterations. However, it is
         less robust to very large initial displacement errors."

      .. grid-item-card:: Autoware's NDT scan matcher
         :link: https://autowarefoundation.github.io/autoware_core/main/localization/autoware_ndt_scan_matcher/
         :class-card: sd-border-secondary

         **Autoware Foundation**

         *Autoware Core: autoware_ndt_scan_matcher.* Accessed 10 October
         2026. The package moved from Autoware Universe to Autoware Core.

         "A package for position estimation using the NDT scan matching
         method", and "the Monte Carlo method" to "estimate initial
         position": MCL to start, scan matching to follow.

      .. grid-item-card:: NDT
         :link: https://doi.org/10.1109/IROS.2003.1249285
         :class-card: sd-border-secondary

         **Biber, P. and Strasser, W. (2003)**

         "The Normal Distributions Transform: A New Approach to Laser Scan
         Matching." *Proceedings of the IEEE/RSJ International Conference on
         Intelligent Robots and Systems (IROS)*, 3, 2743 to 2748.
         doi:10.1109/IROS.2003.1249285.

         The map as cells, each with a mean and a covariance; a pose scored
         by how likely each scan point is under its cell's ellipse. Also
         cited in the appendix on NDT.


.. dropdown:: Integrity
   :class-container: sd-border-secondary
   :open:

   How the AV checks its pose without knowing the truth.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: GNSS integrity
         :link: https://doi.org/10.1109/TITS.2017.2766768
         :class-card: sd-border-secondary

         **Zhu, N., Marais, J., Bétaille, D. and Berbineau, M. (2018)**

         "GNSS Position Integrity in Urban Environments: A Review of
         Literature." *IEEE Transactions on Intelligent Transportation
         Systems*, 19(9), 2762 to 2778. doi:10.1109/TITS.2017.2766768.

         The definitions of integrity, the alert limit and the protection
         level.


.. dropdown:: SLAM
   :class-container: sd-border-secondary
   :open:

   Building the map and finding the pose at the same time.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Graph-based SLAM
         :link: https://doi.org/10.1109/MITS.2010.939925
         :class-card: sd-border-secondary

         **Grisetti, G., Kümmerle, R., Stachniss, C. and Burgard, W. (2010)**

         "A Tutorial on Graph-Based SLAM." *IEEE Intelligent Transportation
         Systems Magazine*, 2(4), 31 to 43. doi:10.1109/MITS.2010.939925.

         The pose graph: find the poses that disagree least with all edges,
         each weighted by how sure it is. Also cited in the appendix on
         pose-graph least squares.

      .. grid-item-card:: SLAM front end and back end
         :link: https://doi.org/10.1109/TRO.2016.2624754
         :class-card: sd-border-secondary

         **Cadena, C., Carlone, L., Carrillo, H., Latif, Y., Scaramuzza, D.,
         Neira, J., Reid, I. and Leonard, J. J. (2016)**

         "Past, Present, and Future of Simultaneous Localization and Mapping."
         *IEEE Transactions on Robotics*, 32(6), 1309 to 1332.

         "The front-end abstracts sensor data into models that are amenable for
         estimation, while the back-end performs inference".

      .. grid-item-card:: LOAM
         :link: https://doi.org/10.15607/RSS.2014.X.007
         :class-card: sd-border-secondary

         **Zhang, J. and Singh, S. (2014)**

         "LOAM: Lidar Odometry and Mapping in Real-time." *Robotics: Science
         and Systems*.

         Feature points "on sharp edges and planar surfaces"; a LiDAR's
         "insensitivity to ambient lighting and optical texture".

      .. grid-item-card:: Cartographer
         :link: https://doi.org/10.1109/ICRA.2016.7487258
         :class-card: sd-border-secondary

         **Hess, W., Kohler, D., Rapp, H. and Andor, D. (2016)**

         "Real-Time Loop Closure in 2D LIDAR SLAM." *IEEE ICRA*, 1271 to 1278.

         Scans matched into submaps; loop closures found in the background.

      .. grid-item-card:: ORB-SLAM
         :link: https://doi.org/10.1109/TRO.2015.2463671
         :class-card: sd-border-secondary

         **Mur-Artal, R., Montiel, J. M. M. and Tardós, J. D. (2015)**

         "ORB-SLAM: A Versatile and Accurate Monocular SLAM System." *IEEE
         Transactions on Robotics*, 31(5), 1147 to 1163.

         ORB features; "depth cannot be recovered from a single image".

      .. grid-item-card:: ORB-SLAM3
         :link: https://doi.org/10.1109/TRO.2021.3075644
         :class-card: sd-border-secondary

         **Campos, C., Elvira, R., Gómez Rodríguez, J. J., Montiel, J. M. M.
         and Tardós, J. D. (2021)**

         "ORB-SLAM3." *IEEE Transactions on Robotics*, 37(6), 1874 to 1890.

         Pure monocular SLAM: "scale is unknown"; an IMU makes it observable.

      .. grid-item-card:: DBoW2
         :link: https://doi.org/10.1109/TRO.2012.2197158
         :class-card: sd-border-secondary

         **Gálvez-López, D. and Tardós, J. D. (2012)**

         "Bags of Binary Words for Fast Place Recognition in Image Sequences."
         *IEEE Transactions on Robotics*, 28(5), 1188 to 1197.

         "If they are similar enough, a loop closure is detected."

      .. grid-item-card:: Scan Context
         :link: https://doi.org/10.1109/IROS.2018.8593953
         :class-card: sd-border-secondary

         **Kim, G. and Kim, A. (2018)**

         "Scan Context: Egocentric Spatial Descriptor for Place Recognition
         Within 3D Point Cloud Map." *IEEE/RSJ IROS*, 4802 to 4809.

         A descriptor of one LiDAR scan that "provides candidates for
         loop-closure".

      .. grid-item-card:: Degeneracy
         :link: https://doi.org/10.1109/ICRA.2016.7487211
         :class-card: sd-border-secondary

         **Zhang, J., Kaess, M. and Singh, S. (2016)**

         "On Degeneracy of Optimization-based State Estimation Problems."
         *IEEE ICRA*, 809 to 816.

         "Scarcity of texture features for vision sensors and lack of
         geometrical structures for range sensors."


.. dropdown:: Going Further Only
   :class-container: sd-border-secondary
   :open:

   Sources cited only in the appendix, :doc:`l6_appendix`.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The best rotation
         :link: https://doi.org/10.1107/S0567739476001873
         :class-card: sd-border-secondary

         **Kabsch, W. (1976)**

         "A Solution for the Best Rotation to Relate Two Sets of Vectors."
         *Acta Crystallographica Section A*, 32(5), 922 to 923.
         doi:10.1107/S0567739476001873.

         The rotation from the SVD of :math:`H`, in 2-D or 3-D, with the
         check that turns a mirror image back into a rotation.

      .. grid-item-card:: Probabilistic Robotics
         :class-card: sd-border-secondary

         **Thrun, S., Burgard, W. and Fox, D. (2005)**

         *Probabilistic Robotics.* Intelligent Robotics and Autonomous
         Agents. MIT Press, Cambridge, MA. ISBN 978-0-262-20162-9.

         The likelihood field (Sec. 6.4) that the course's MCL code adapts.

      .. grid-item-card:: Trajectory evaluation
         :link: https://doi.org/10.1109/IROS.2018.8593941
         :class-card: sd-border-secondary

         **Zhang, Z. and Scaramuzza, D. (2018)**

         "A Tutorial on Quantitative Trajectory Evaluation for
         Visual(-Inertial) Odometry." *Proceedings of the IEEE/RSJ
         International Conference on Intelligent Robots and Systems (IROS)*,
         7244 to 7251. doi:10.1109/IROS.2018.8593941.

         Why a system with no global reference is scored by the relative
         error.


.. rubric:: Image credits

The vehicle icons in the lecture's figures were created by Stone from the
`Noun Project <https://thenounproject.com>`_.
