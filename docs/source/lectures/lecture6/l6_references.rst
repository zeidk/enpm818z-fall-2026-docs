====================================================
References
====================================================

These are the sources the L6 slides cite, grouped by the lecture's sections,
in the order the slides first cite each source. A source cited in several
sections is listed once, where the slides first cite it. Nine sources are
cited only in the appendix (:doc:`l6_appendix`); they have their own group at
the end.

.. tip::

   Two to read first: Reid et al. (2019) for the accuracy requirement, and
   the tutorial by Grisetti et al. (2010) for the pose graph.


.. dropdown:: Introduction
   :class-container: sd-border-secondary
   :open:

   How good a localizer must be, and the frame a map's pose lives in. The
   same bound returns in every section, and in the appendix on the error
   bound.

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

         The error bound, "the allowable maximum position error of the
         vehicle to ensure it is within the lane": 0.29 m on a local street,
         with 95% of errors within 0.10 m, passed at most once in
         :math:`10^8` hours of driving.

      .. grid-item-card:: Autoware's map frame
         :link: https://github.com/autowarefoundation/autoware_core/blob/main/map/autoware_map_projection_loader/README.md
         :class-card: sd-border-secondary

         **Autoware Foundation**

         *Autoware Core: autoware_map_projection_loader.* Accessed 15
         October 2026.

         How a map picks its frame: one MGRS (Military Grid Reference
         System) square, or a chosen latitude and longitude.


.. dropdown:: The Drive
   :class-container: sd-border-secondary
   :open:

   What an IMU is, and where it sits on a vehicle.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The IMU
         :link: https://arxiv.org/abs/2603.07143
         :class-card: sd-border-secondary

         **Berkane, S. (2026)**

         *Tutorial on Aided Inertial Navigation Systems: A Modern Treatment
         Using Lie-Group Theoretical Methods.* Technical report
         LaRSA-TR-2026-01, Robotics and Autonomous Systems Laboratory
         (LaRSA), Université du Québec en Outaouais. arXiv:2603.07143,
         version 2.

         The IMU "typically consists of three orthogonally mounted gyroscopes
         and three accelerometers".

      .. grid-item-card:: Where the IMU goes
         :link: https://support-centre.racelogic.co.uk/automotive/imu/imu05-imu05s/ug/mounting/
         :class-card: sd-border-secondary

         **Racelogic (2026)**

         *Mounting: IMU05/IMU05-S User Guide.* Racelogic Support Centre,
         updated 21 September 2026. Accessed 10 October 2026.

         On the roof "co-located with the GNSS antenna", or inside on the seat
         rails; IMU and antenna "on the same rigid body".


.. dropdown:: GNSS and RTK
   :class-container: sd-border-secondary
   :open:

   What GNSS is, what RTK is, how close it gets, where it works, and who
   provides it in Maryland. Also cited in the appendix on RTK.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: GPS and the other GNSS
         :link: https://www.gps.gov/other-global-navigation-satellite-systems-gnss
         :class-card: sd-border-secondary

         **U.S. Government, GPS.gov**

         *Other Global Navigation Satellite Systems (GNSS)*, and *GPS.gov:
         Official U.S. Government Information about the Global Positioning
         System (GPS)* (https://www.gps.gov/). Accessed 10 October 2026.

         GNSS is "a general term describing any satellite constellation"; GPS
         is "a U.S.-owned utility", "operated and maintained by the U.S. Space
         Force".

      .. grid-item-card:: NOAA CORS Network
         :link: https://geodesy.noaa.gov/CORS/
         :class-card: sd-border-secondary

         **NOAA National Geodetic Survey**

         *The NOAA CORS Network (NCN).* Accessed 10 October 2026. Station
         map: https://arcg.is/18fWq8.

         Reference stations whose GNSS data improve the precision of
         positions after the fact.

      .. grid-item-card:: Real-time networks in Maryland
         :link: https://fig.net/resources/proceedings/fig_proceedings/fig2019/papers/ts05e/TS05E_gillins_heck_et_al_10077.pdf
         :class-card: sd-border-secondary

         **Gillins, D., Heck, J., Scott, G., Jordan, K. and Hippenstiel, R.
         (2019)**

         *Accuracy of GNSS Observations from Three Real-Time Networks in
         Maryland, USA.* FIG Working Week 2019, Hanoi, Vietnam, paper 10077.

         "In Maryland of the United States, three independent RTNs are
         available": Trimble KeyNetGPS, Topcon TopNET live and Leica
         SmartNet. A single base station "generally limits baseline lengths
         to less than 20 km", because farther away "atmospheric delay errors
         do not sufficiently cancel"; networks space their bases "every 70
         km or less".

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

         **Sanz Subirana, J., Juan Zornoza, J. M. and Hernández-Pajares, M.
         (2011)**

         *Multipath.* European Space Agency, Navipedia (Technical University
         of Catalonia). Accessed 10 October 2026.

         "The interference by multipath is generated when a signal arrives,
         by different ways, at the antenna." "Its principal cause is the
         antenna closeness to the reflecting structures".


.. dropdown:: Dead Reckoning
   :class-container: sd-border-secondary
   :open:

   Where the method and its name come from.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Dead reckoning
         :link: https://msi.nga.mil/Publications/APN
         :class-card: sd-border-secondary

         **National Geospatial-Intelligence Agency (2019)**

         *The American Practical Navigator (Bowditch), Volume I.* Pub. No. 9.
         National Geospatial-Intelligence Agency. Chapter 9, Dead Reckoning,
         Article 900.

         "A method for determining the estimated position of a vessel by
         advancing from a known fix of position along the vessel's ordered
         course and speed".


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

         The absolute pose error (APE, which the paper calls ATE) summarized
         by the RMSE; in the appendix, the relative pose error (RPE) as the
         drift.


.. dropdown:: Against a Map
   :class-container: sd-border-secondary
   :open:

   Matching the LiDAR scan to a map: MCL, scan registration with ICP and its
   k-d tree, scenes that cannot pin down the pose, and what a real stack and
   deployed fleets run.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Monte Carlo localization and random particles
         :link: https://rse-lab.cs.washington.edu/papers/sampling-aaai-99.pdf
         :class-card: sd-border-secondary

         **Fox, D., Burgard, W., Dellaert, F. and Thrun, S. (1999)**

         "Monte Carlo Localization: Efficient Position Estimation for Mobile
         Robots." *Proceedings of the Sixteenth National Conference on
         Artificial Intelligence (AAAI-99)*, Orlando, FL, 343 to 349.

         MCL keeps its belief as "a set of :math:`N` weighted, random
         samples or particles". "The added samples are essential for
         relocalization in the rare event that the robot loses track of its
         position."

      .. grid-item-card:: Monte Carlo localization
         :link: https://doi.org/10.1109/ROBOT.1999.772544
         :class-card: sd-border-secondary

         **Dellaert, F., Fox, D., Burgard, W. and Thrun, S. (1999)**

         "Monte Carlo Localization for Mobile Robots." *Proceedings of the
         IEEE International Conference on Robotics and Automation (ICRA)*,
         1322 to 1328. doi:10.1109/ROBOT.1999.772544.

         MCL written out: start, predict, weigh, normalize, estimate,
         resample.

      .. grid-item-card:: Probabilistic Robotics
         :class-card: sd-border-secondary

         **Thrun, S., Burgard, W. and Fox, D. (2005)**

         *Probabilistic Robotics.* Intelligent Robotics and Autonomous
         Agents. MIT Press, Cambridge, MA. ISBN 978-0-262-20162-9.

         The likelihood field (Sec. 6.4) that the course's MCL code adapts.
         The book divides :math:`z_\text{rand}` by the sensor's maximum
         range; our code divides by :math:`d_\text{max}`.

      .. grid-item-card:: KLD sampling
         :link: https://doi.org/10.1177/0278364903022012001
         :class-card: sd-border-secondary

         **Fox, D. (2003)**

         "Adapting the Sample Size in Particle Filters Through KLD-Sampling."
         *The International Journal of Robotics Research*, 22(12), 985 to
         1003. doi:10.1177/0278364903022012001.

         "A small number of samples if the density is focused", a large number
         when the samples must cover a large part of the space.

      .. grid-item-card:: Robust MCL
         :link: https://doi.org/10.1016/S0004-3702(01)00069-8
         :class-card: sd-border-secondary

         **Thrun, S., Fox, D., Burgard, W. and Dellaert, F. (2001)**

         "Robust Monte Carlo Localization for Mobile Robots." *Artificial
         Intelligence*, 128(1 and 2), 99 to 141.
         doi:10.1016/S0004-3702(01)00069-8.

         Adding random samples and similar fixes are "mathematically
         questionable".

      .. grid-item-card:: NDT and scan registration
         :link: https://doi.org/10.1109/IROS.2003.1249285
         :class-card: sd-border-secondary

         **Biber, P. and Strasser, W. (2003)**

         "The Normal Distributions Transform: A New Approach to Laser Scan
         Matching." *Proceedings of the IEEE/RSJ International Conference on
         Intelligent Robots and Systems (IROS)*, 3, 2743 to 2748.
         doi:10.1109/IROS.2003.1249285.

         Matching range scans is "a basic component of many localization and
         mapping algorithms". NDT: the map as cells, each with a mean and a
         covariance; a pose scored by how likely each scan point is under
         its cell's ellipse. Also cited in the appendix on NDT.

      .. grid-item-card:: ICP
         :link: https://doi.org/10.1109/34.121791
         :class-card: sd-border-secondary

         **Besl, P. J. and McKay, N. D. (1992)**

         "A Method for Registration of 3-D Shapes." *IEEE Transactions on
         Pattern Analysis and Machine Intelligence*, 14(2), 239 to 256.
         doi:10.1109/34.121791.

         ICP "requires only a procedure to find the closest point on a
         geometric entity to a given point", and it "always converges
         monotonically to the nearest local minimum of a mean-square
         distance metric".

      .. grid-item-card:: The k-d tree
         :link: https://doi.org/10.1145/361002.361007
         :class-card: sd-border-secondary

         **Bentley, J. L. (1975)**

         "Multidimensional Binary Search Trees Used for Associative
         Searching." *Communications of the ACM*, 18(9), 509 to 517.
         doi:10.1145/361002.361007.

         The k-d tree: split on one key per level, the keys taken in turn.

      .. grid-item-card:: Nearest neighbors in log N
         :link: https://doi.org/10.1145/355744.355745
         :class-card: sd-border-secondary

         **Friedman, J. H., Bentley, J. L. and Finkel, R. A. (1977)**

         "An Algorithm for Finding Best Matches in Logarithmic Expected Time."
         *ACM Transactions on Mathematical Software*, 3(3), 209 to 226.
         doi:10.1145/355744.355745.

         "The expected computation to perform each search is proportional to
         logN."

      .. grid-item-card:: The best rotation
         :link: https://doi.org/10.1107/S0567739476001873
         :class-card: sd-border-secondary

         **Kabsch, W. (1976)**

         "A Solution for the Best Rotation to Relate Two Sets of Vectors."
         *Acta Crystallographica Section A*, 32(5), 922 to 923.
         doi:10.1107/S0567739476001873.

         The best turn and shift for a set of pairs, ICP's step 2. In the
         appendix: the turn from the SVD of :math:`H`, in 2-D or 3-D, with
         the check that turns a mirror image back into a rotation.

      .. grid-item-card:: Degeneracy
         :link: https://doi.org/10.1109/ICRA.2016.7487211
         :class-card: sd-border-secondary

         **Zhang, J., Kaess, M. and Singh, S. (2016)**

         "On Degeneracy of Optimization-based State Estimation Problems."
         *IEEE International Conference on Robotics and Automation (ICRA)*,
         809 to 816. doi:10.1109/ICRA.2016.7487211.

         What to do when a scan cannot see one direction. "Scarcity of
         texture features for vision sensors and lack of geometrical
         structures for range sensors." Also cited in SLAM.

      .. grid-item-card:: Autoware's NDT scan matcher
         :link: https://autowarefoundation.github.io/autoware_core/main/localization/autoware_ndt_scan_matcher/
         :class-card: sd-border-secondary

         **Autoware Foundation**

         *Autoware Core: autoware_ndt_scan_matcher.* Accessed 10 October
         2026. The package moved from Autoware Universe to Autoware Core.

         "A package for position estimation using the NDT scan matching
         method", and "the Monte Carlo method" to "estimate initial
         position": MCL to start, scan matching to follow.

      .. grid-item-card:: Baidu Apollo's localization
         :link: https://doi.org/10.1109/ICRA.2018.8461224
         :class-card: sd-border-secondary

         **Wan, G., Yang, X., Cai, R., Li, H., Zhou, Y., Wang, H. and Song,
         S. (2018)**

         "Robust and Precise Vehicle Localization Based on Multi-Sensor
         Fusion in Diverse City Scenes." *IEEE International Conference on
         Robotics and Automation (ICRA)*, 4670 to 4677.
         doi:10.1109/ICRA.2018.8461224.

         GNSS (with RTK), LiDAR map matching and an IMU fused in an
         error-state Kalman filter, "deployed in a large autonomous driving
         fleet".

      .. grid-item-card:: Waymo's maps
         :link: https://waymo.com/blog/2020/09/the-waymo-driver-handbook-mapping/
         :class-card: sd-border-secondary

         **The Waymo Team (2020)**

         *The Waymo Driver Handbook: How our highly-detailed maps help unlock
         new locations for autonomous driving.* Waymo blog, 21 September
         2020. Accessed 15 October 2026.

         Maps that "help our cars navigate places even where GPS struggles,
         like tunnels or between skyscrapers".


.. dropdown:: SLAM
   :class-container: sd-border-secondary
   :open:

   Building the map and finding the pose at the same time, LiDAR and camera
   front ends, and what is still open.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: SLAM front end and back end
         :link: https://doi.org/10.1109/TRO.2016.2624754
         :class-card: sd-border-secondary

         **Cadena, C., Carlone, L., Carrillo, H., Latif, Y., Scaramuzza, D.,
         Neira, J., Reid, I. and Leonard, J. J. (2016)**

         "Past, Present, and Future of Simultaneous Localization and Mapping:
         Toward the Robust-Perception Age." *IEEE Transactions on Robotics*,
         32(6), 1309 to 1332. doi:10.1109/TRO.2016.2624754.

         "The front-end abstracts sensor data into models that are amenable for
         estimation, while the back-end performs inference". Also the survey
         behind what is still open in SLAM.

      .. grid-item-card:: Graph-based SLAM
         :link: https://doi.org/10.1109/MITS.2010.939925
         :class-card: sd-border-secondary

         **Grisetti, G., Kümmerle, R., Stachniss, C. and Burgard, W. (2010)**

         "A Tutorial on Graph-Based SLAM." *IEEE Intelligent Transportation
         Systems Magazine*, 2(4), 31 to 43. doi:10.1109/MITS.2010.939925.

         The pose graph: find the poses that disagree least with all edges,
         each weighted by how sure it is. Also cited in the appendix on
         pose-graph least squares.

      .. grid-item-card:: ORB-SLAM
         :link: https://doi.org/10.1109/TRO.2015.2463671
         :class-card: sd-border-secondary

         **Mur-Artal, R., Montiel, J. M. M. and Tardós, J. D. (2015)**

         "ORB-SLAM: A Versatile and Accurate Monocular SLAM System." *IEEE
         Transactions on Robotics*, 31(5), 1147 to 1163.
         doi:10.1109/TRO.2015.2463671.

         ORB features; "depth cannot be recovered from a single image".

      .. grid-item-card:: LOAM
         :link: https://doi.org/10.15607/RSS.2014.X.007
         :class-card: sd-border-secondary

         **Zhang, J. and Singh, S. (2014)**

         "LOAM: Lidar Odometry and Mapping in Real-time." *Proceedings of
         Robotics: Science and Systems (RSS)*, Berkeley, USA.
         doi:10.15607/RSS.2014.X.007.

         Feature points "on sharp edges and planar surfaces"; a LiDAR's
         "insensitivity to ambient lighting and optical texture".

      .. grid-item-card:: ORB-SLAM3
         :link: https://doi.org/10.1109/TRO.2021.3075644
         :class-card: sd-border-secondary

         **Campos, C., Elvira, R., Gómez Rodríguez, J. J., Montiel, J. M. M.
         and Tardós, J. D. (2021)**

         "ORB-SLAM3: An Accurate Open-Source Library for Visual,
         Visual-Inertial, and Multimap SLAM." *IEEE Transactions on
         Robotics*, 37(6), 1874 to 1890. doi:10.1109/TRO.2021.3075644.

         Pure monocular SLAM: "scale is unknown"; an IMU makes it observable.

      .. grid-item-card:: Scan Context
         :link: https://doi.org/10.1109/IROS.2018.8593953
         :class-card: sd-border-secondary

         **Kim, G. and Kim, A. (2018)**

         "Scan Context: Egocentric Spatial Descriptor for Place Recognition
         Within 3D Point Cloud Map." *IEEE/RSJ International Conference on
         Intelligent Robots and Systems (IROS)*, 4802 to 4809.
         doi:10.1109/IROS.2018.8593953.

         A descriptor of one LiDAR scan that "provides candidates for
         loop-closure".

      .. grid-item-card:: DBoW2
         :link: https://doi.org/10.1109/TRO.2012.2197158
         :class-card: sd-border-secondary

         **Gálvez-López, D. and Tardós, J. D. (2012)**

         "Bags of Binary Words for Fast Place Recognition in Image Sequences."
         *IEEE Transactions on Robotics*, 28(5), 1188 to 1197.
         doi:10.1109/TRO.2012.2197158.

         "If they are similar enough, a loop closure is detected."

      .. grid-item-card:: Visual localization in changing conditions
         :link: https://doi.org/10.1109/CVPR.2018.00897
         :class-card: sd-border-secondary

         **Sattler, T., Maddern, W., Toft, C., Torii, A., Hammarstrand, L.,
         Stenborg, E., Safari, D., Okutomi, M., Pollefeys, M., Sivic, J.,
         Kahl, F. and Pajdla, T. (2018)**

         "Benchmarking 6DOF Outdoor Visual Localization in Changing
         Conditions." *IEEE/CVF Conference on Computer Vision and Pattern
         Recognition (CVPR)*, 8601 to 8610. doi:10.1109/CVPR.2018.00897.

         Camera localization must handle "day-night changes, as well as
         weather and seasonal variations"; "long-term localization is far
         from solved".

      .. grid-item-card:: Cartographer
         :link: https://doi.org/10.1109/ICRA.2016.7487258
         :class-card: sd-border-secondary

         **Hess, W., Kohler, D., Rapp, H. and Andor, D. (2016)**

         "Real-Time Loop Closure in 2D LIDAR SLAM." *IEEE International
         Conference on Robotics and Automation (ICRA)*, 1271 to 1278.
         doi:10.1109/ICRA.2016.7487258.

         Scans matched into submaps; loop closures found in the background.

      .. grid-item-card:: Visual-inertial odometry
         :link: https://doi.org/10.1109/TRO.2018.2853729
         :class-card: sd-border-secondary

         **Qin, T., Li, P. and Shen, S. (2018)**

         "VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State
         Estimator." *IEEE Transactions on Robotics*, 34(4), 1004 to 1020.
         doi:10.1109/TRO.2018.2853729.

         A camera and an IMU together follow how the AV moves in 3-D,
         including the true size of the motion.

      .. grid-item-card:: LVI-SAM
         :link: https://doi.org/10.1109/ICRA48506.2021.9561996
         :class-card: sd-border-secondary

         **Shan, T., Englot, B., Ratti, C. and Rus, D. (2021)**

         "LVI-SAM: Tightly-coupled Lidar-Visual-Inertial Odometry via
         Smoothing and Mapping." *IEEE International Conference on Robotics
         and Automation (ICRA)*, 5692 to 5698.
         doi:10.1109/ICRA48506.2021.9561996.

         The camera's estimate as the starting guess for scan matching; the
         system keeps working when either the camera part or the LiDAR part
         fails.

      .. grid-item-card:: Hierarchical localization
         :link: https://doi.org/10.1109/CVPR.2019.01300
         :class-card: sd-border-secondary

         **Sarlin, P.-E., Cadena, C., Siegwart, R. and Dymczyk, M. (2019)**

         "From Coarse to Fine: Robust Hierarchical Localization at Large
         Scale." *IEEE/CVF Conference on Computer Vision and Pattern
         Recognition (CVPR)*, 12708 to 12717. doi:10.1109/CVPR.2019.01300.

         Find the likely places by comparing the image with stored images of
         the whole map, then match details to get the pose.

      .. grid-item-card:: SLAM, Part I
         :link: https://doi.org/10.1109/MRA.2006.1638022
         :class-card: sd-border-secondary

         **Durrant-Whyte, H. and Bailey, T. (2006)**

         "Simultaneous Localization and Mapping: Part I." *IEEE Robotics &
         Automation Magazine*, 13(2), 99 to 110.
         doi:10.1109/MRA.2006.1638022.

         By 2006, "the general SLAM method" was "a well understood and
         established part of robotics", with "many practical issues to
         overcome, especially in more complex outdoor environments".


.. dropdown:: Going Further Only
   :class-container: sd-border-secondary
   :open:

   Sources cited only in the appendix, :doc:`l6_appendix`: NOAA's CORS map,
   the ways to score a scan, integrity, and trajectory evaluation.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: NOAA's CORS map
         :link: https://noaa.maps.arcgis.com/home/item.html?id=99dc0ccc01f6449aa41a84fc57fe4171
         :class-card: sd-border-secondary

         **NOAA National Geodetic Survey**

         *NOAA Continuously Operating Reference Stations (CORS) Network
         (ArcGIS item).* Accessed 15 October 2026.

         After processing, positions from the stations' data "can approach a
         few centimeters".

      .. grid-item-card:: All NGS CORS sites
         :link: https://geodesy.noaa.gov/CORS/sort_sites.shtml
         :class-card: sd-border-secondary

         **NOAA National Geodetic Survey**

         *All NGS CORS Sites.* Accessed 15 October 2026.

         A station's sampling rate "is valid for 30 days. After that the data
         are decimated to 30 seconds".

      .. grid-item-card:: NCN data and products
         :link: https://www.ngs.noaa.gov/CORS/data.shtml
         :class-card: sd-border-secondary

         **NOAA National Geodetic Survey**

         *NCN Data and Products.* Accessed 15 October 2026.

         Not live: "most data are available within 1 hour".

      .. grid-item-card:: Point to plane
         :link: https://doi.org/10.1109/ROBOT.1991.132043
         :class-card: sd-border-secondary

         **Chen, Y. and Medioni, G. (1991)**

         "Object Modeling by Registration of Multiple Range Images."
         *Proceedings of the IEEE International Conference on Robotics and
         Automation (ICRA)*, Sacramento, CA, 2724 to 2729.
         doi:10.1109/ROBOT.1991.132043.

         "We minimize the distance from points to planes."

      .. grid-item-card:: Point to line
         :link: https://doi.org/10.1109/ROBOT.2008.4543181
         :class-card: sd-border-secondary

         **Censi, A. (2008)**

         "An ICP Variant Using a Point-to-Line Metric." *Proceedings of the
         IEEE International Conference on Robotics and Automation (ICRA)*,
         Pasadena, CA, 19 to 25. doi:10.1109/ROBOT.2008.4543181.

         "PLICP is more precise, and requires less iterations. However, it is
         less robust to very large initial displacement errors."

      .. grid-item-card:: Generalized-ICP
         :link: https://doi.org/10.15607/RSS.2009.V.021
         :class-card: sd-border-secondary

         **Segal, A., Haehnel, D. and Thrun, S. (2009)**

         "Generalized-ICP." *Robotics: Science and Systems V*.
         doi:10.15607/RSS.2009.V.021.

         GICP models "locally planar surface structure from both scans", and
         is "more robust to incorrect correspondences".

      .. grid-item-card:: 3-D NDT
         :link: https://doi.org/10.1002/rob.20204
         :class-card: sd-border-secondary

         **Magnusson, M., Lilienthal, A. J. and Duckett, T. (2007)**

         "Scan Registration for Autonomous Mining Vehicles Using 3D-NDT."
         *Journal of Field Robotics*, 24(10), 803 to 827.
         doi:10.1002/rob.20204.

         3-D NDT was "faster and slightly more reliable than the standard ICP
         algorithm", with "a more memory-efficient scan surface
         representation".

      .. grid-item-card:: GNSS integrity
         :link: https://doi.org/10.1109/TITS.2017.2766768
         :class-card: sd-border-secondary

         **Zhu, N., Marais, J., Bétaille, D. and Berbineau, M. (2018)**

         "GNSS Position Integrity in Urban Environments: A Review of
         Literature." *IEEE Transactions on Intelligent Transportation
         Systems*, 19(9), 2762 to 2778. doi:10.1109/TITS.2017.2766768.

         The definitions of integrity, the alert limit and the protection
         level.

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
`Noun Project <https://thenounproject.com>`_. The IMU photo is a product image
of the MS-IMU3050 by Memsense, an Inertial Labs company.
