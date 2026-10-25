====================================================
References
====================================================

These are the sources the L8 slides cite, grouped by the lecture's sections,
in the order the slides first cite each source. A source cited in several
sections is listed once, where the slides first cite it. The sections The
Scene, Scoring, Several Futures and Using the Map cite no new source. One
source is cited only in the appendix (:doc:`l8_appendix`); it has its own
group at the end.

.. dropdown:: Introduction
   :class-container: sd-border-secondary
   :open:

   How often the predictor runs, the prediction windows of the public
   datasets, and the three kinds of motion model.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Apollo's prediction module
         :link: https://github.com/ApolloAuto/apollo/blob/master/modules/prediction/prediction_component.cc
         :class-card: sd-border-secondary

         **Apollo Auto**

         *Apollo prediction module: prediction_component.cc.* Source code.
         Accessed 24 October 2026.

         ``Proc`` runs on each ``PerceptionObstacles`` message and writes
         the prediction.

      .. grid-item-card:: Autoware's map-based prediction, source
         :link: https://github.com/autowarefoundation/autoware_universe/blob/main/perception/autoware_map_based_prediction/lib/map_based_prediction_node/callbacks.cpp
         :class-card: sd-border-secondary

         **Autoware Foundation**

         *autoware_map_based_prediction: callbacks.cpp.* Source code.
         Accessed 24 October 2026.

         ``objectsCallback`` runs on each ``TrackedObjects`` message and
         publishes the predicted objects.

      .. grid-item-card:: Argoverse
         :class-card: sd-border-secondary

         **Chang, M.-F., Lambert, J., Sangkloy, P., Singh, J., Bak, S.,
         Hartnett, A., Wang, D., Carr, P., Lucey, S., Ramanan, D. and Hays,
         J. (2019)**

         "Argoverse: 3D Tracking and Forecasting with Rich Maps."
         *Proceedings of the IEEE/CVF Conference on Computer Vision and
         Pattern Recognition (CVPR)*, 8748 to 8757.

         Observes 2 s and predicts 3 s. Also cited in Scoring, for ADE and
         FDE.

      .. grid-item-card:: Argoverse 2
         :class-card: sd-border-secondary

         **Wilson, B., Qi, W., Agarwal, T., Lambert, J., Singh, J.,
         Khandelwal, S., Pan, B., Kumar, R., Hartnett, A., Pontes, J. K.,
         Ramanan, D., Carr, P. and Hays, J. (2021)**

         "Argoverse 2: Next Generation Datasets for Self-Driving Perception
         and Forecasting." *Proceedings of the Neural Information Processing
         Systems Track on Datasets and Benchmarks.*

         Observes 5 s and predicts 6 s. Also cited in Scoring (ADE, FDE and
         the miss rate: "within 2.0 meters of ground truth according to
         endpoint error"), in Several Futures (minADE and minFDE) and in
         Learned Predictors (training and scores).

      .. grid-item-card:: Waymo Open Motion Dataset
         :class-card: sd-border-secondary

         **Ettinger, S., Cheng, S., Caine, B., Liu, C., Zhao, H., Pradhan,
         S., Chai, Y., Sapp, B., Qi, C., Zhou, Y., Yang, Z., Chouard, A.,
         Sun, P., Ngiam, J., Vasudevan, V., McCauley, A., Shlens, J. and
         Anguelov, D. (2021)**

         "Large Scale Interactive Motion Forecasting for Autonomous Driving:
         The Waymo Open Motion Dataset." *Proceedings of the IEEE/CVF
         International Conference on Computer Vision (ICCV)*, 9710 to 9719.

         Observes 1 s and predicts 8 s. Also cited in Scoring (thresholds
         that depend on the horizon and the speed), in Several Futures (mAP)
         and in Learned Predictors (training and scores).

      .. grid-item-card:: Three kinds of motion model
         :link: https://doi.org/10.1186/s40648-014-0001-z
         :class-card: sd-border-secondary

         **Lefèvre, S., Vasquez, D. and Laugier, C. (2014)**

         "A survey on motion prediction and risk assessment for intelligent
         vehicles." *ROBOMECH Journal*, 1(1).
         doi:10.1186/s40648-014-0001-z.

         Physics-based, maneuver-based and interaction-aware models. Also
         cited in Using the Map and Other Drivers.


.. dropdown:: Physics Models
   :class-container: sd-border-secondary

   The motion models with a constant turn rate.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: CTRV and CTRA
         :class-card: sd-border-secondary

         **Schubert, R., Richter, E. and Wanielik, G. (2008)**

         "Comparison and Evaluation of Advanced Motion Models for Vehicle
         Tracking." *Proceedings of the 11th International Conference on
         Information Fusion (FUSION 2008)*, Cologne, Germany, 730 to 735.

         Constant turn rate and velocity, and constant turn rate and
         acceleration. Also cited in the appendix, for CTRA's integrals in
         closed form.


.. dropdown:: Learned Predictors
   :class-container: sd-border-secondary

   Three well-known designs, what Waymo and Tesla say they use, and
   pedestrians and cyclists (with the Tempe crash).

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: VectorNet
         :link: https://arxiv.org/abs/2005.04259
         :class-card: sd-border-secondary

         **Gao, J., Sun, C., Zhao, H., Shen, Y., Anguelov, D., Li, C. and
         Schmid, C. (2020)**

         "VectorNet: Encoding HD Maps and Agent Dynamics from Vectorized
         Representation." *Proceedings of the IEEE/CVF Conference on
         Computer Vision and Pattern Recognition (CVPR).* arXiv:2005.04259.

         "Observed agent trajectories and map features are represented as
         sequence of vectors".

      .. grid-item-card:: MultiPath
         :class-card: sd-border-secondary

         **Chai, Y., Sapp, B., Bansal, M. and Anguelov, D. (2019)**

         "MultiPath: Multiple Probabilistic Anchor Trajectory Hypotheses for
         Behavior Prediction." *Proceedings of the 3rd Conference on Robot
         Learning (CoRL 2019)*, Proceedings of Machine Learning Research,
         volume 100, 86 to 99.

         A probability for each anchor trajectory, with offsets and
         uncertainties.

      .. grid-item-card:: MTR (Motion Transformer)
         :link: https://arxiv.org/abs/2209.13508
         :class-card: sd-border-secondary

         **Shi, S., Jiang, L., Dai, D. and Schiele, B. (2022)**

         "Motion Transformer with Global Intention Localization and Local
         Movement Refinement." *Advances in Neural Information Processing
         Systems 35 (NeurIPS 2022).* arXiv:2209.13508.

         "a small set of learnable motion query pairs", each in charge of
         one motion mode.

      .. grid-item-card:: Waymo's onboard models
         :link: https://waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving/
         :class-card: sd-border-secondary

         **Waymo (2025)**

         *Demonstrably Safe AI for Autonomous Driving.* Waymo blog, 9
         December 2025. Accessed 24 October 2026.

         A "World Decoder" uses the sensor inputs "to predict other road
         users behaviors"; the car runs smaller models "optimized for
         real-time onboard deployment".

      .. grid-item-card:: Tesla AI Day 2022
         :link: https://www.youtube.com/watch?v=ODSJsviD_SU
         :class-card: sd-border-secondary

         **Tesla (2022)**

         *Tesla AI Day 2022.* Video, 30 September 2022, planning part, at
         1:06:27. Accessed 24 October 2026.

         "Relying purely on collision checks with marginal predictions will
         only get you so far because you will miss out on a lot of valid
         interactions".

      .. grid-item-card:: Tesla Q1 2024 Update
         :link: https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q1-2024-Update.pdf
         :class-card: sd-border-secondary

         **Tesla (2024)**

         *Q1 2024 Update.* Shareholder update, 23 April 2024. Accessed 24
         October 2026.

         FSD runs on "end-to-end neural networks".

      .. grid-item-card:: Social LSTM
         :class-card: sd-border-secondary

         **Alahi, A., Goel, K., Ramanathan, V., Robicquet, A., Fei-Fei, L.
         and Savarese, S. (2016)**

         "Social LSTM: Human Trajectory Prediction in Crowded Spaces."
         *Proceedings of the IEEE Conference on Computer Vision and Pattern
         Recognition (CVPR)*, 961 to 971.

         Each person's prediction depends on the people near them.

      .. grid-item-card:: The Tempe crash
         :link: https://www.ntsb.gov/investigations/AccidentReports/Reports/HAR1903.pdf
         :class-card: sd-border-secondary

         **National Transportation Safety Board (2019)**

         *Collision Between Vehicle Controlled by Developmental Automated
         Driving System and Pedestrian, Tempe, Arizona, March 18, 2018.*
         Report NTSB/HAR-19/03, Investigation HWY18MH010, adopted 19
         November 2019. Washington, DC.

         "The ADS detected the pedestrian 5.6 seconds before impact", but
         it never "predicted her path": when perception changed an object's
         class, the system "no longer considered the tracking history of
         that object". Cited for pedestrians and cyclists: a predictor with
         no history has nothing to predict from.


.. dropdown:: Other Drivers
   :class-container: sd-border-secondary

   Intent, a driver following another car, gap acceptance, and how the AV's
   actions change what others do.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Autoware's map-based prediction
         :link: https://github.com/autowarefoundation/autoware_universe/blob/main/perception/autoware_map_based_prediction/README.md
         :class-card: sd-border-secondary

         **Autoware Foundation**

         *autoware_map_based_prediction*, README of the package,
         autoware_universe repository. Accessed 14 October 2026.

         A car drifting toward a lane boundary may change lanes. Also cited
         in the appendix: "a module to predict the future paths (and their
         probabilities) of other vehicles and pedestrians according to the
         shape of the map and the surrounding environment".

      .. grid-item-card:: The Intelligent Driver Model (IDM)
         :link: https://doi.org/10.1103/PhysRevE.62.1805
         :class-card: sd-border-secondary

         **Treiber, M., Hennecke, A. and Helbing, D. (2000)**

         "Congested traffic states in empirical observations and microscopic
         simulations." *Physical Review E*, 62(2), 1805 to 1824.
         doi:10.1103/PhysRevE.62.1805.

         The IDM and its values: :math:`T` = 1.6 s, :math:`a_{\max}` =
         0.73 m/s², :math:`b` = 1.67 m/s², :math:`\delta` = 4, :math:`s_0` =
         2 m.

      .. grid-item-card:: Critical headway
         :link: https://mctranswordpresssa.blob.core.windows.net/uploads/2022/01/TWSC.pdf
         :class-card: sd-border-secondary

         **McTrans Center, University of Florida**

         *HCS Two-Way Stop Controlled Intersections Users Guide.* Glossary,
         base critical headway and base follow-up headway, from the Highway
         Capacity Manual's defaults. Accessed 14 October 2026.

         The base critical headway for a left turn from the major street of
         a two-lane road: 4.1 s.

      .. grid-item-card:: The AV's actions affect other drivers
         :class-card: sd-border-secondary

         **Sadigh, D., Sastry, S., Seshia, S. A. and Dragan, A. D. (2016)**

         "Planning for Autonomous Cars that Leverage Effects on Human
         Actions." *Robotics: Science and Systems XII (RSS)*, Ann Arbor,
         Michigan.

         "an autonomous car's actions will actually affect what other cars
         will do in response, whether the car is aware of it or not".


.. dropdown:: Cited Only in the Appendix
   :class-container: sd-border-secondary

   Waymo's threshold scaling, from :doc:`l8_appendix`.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Waymo's speed scaling
         :link: https://waymo.com/open/challenges/2021/motion-prediction/
         :class-card: sd-border-secondary

         **Waymo LLC**

         *Motion Prediction, 2021 Waymo Open Dataset Challenge.* Accessed
         24 October 2026.

         The miss rate's thresholds are multiplied by a scale from the
         initial speed: 0.5 below 1.4 m/s, 1 above 11 m/s, a straight line
         between.



.. rubric:: Map data and images

The lanes in every top view are CARLA's ``Town01.xodr``, read
offline with the CARLA Python API. The vehicle icons in the figures were
created by Stone from the `Noun Project <https://thenounproject.com>`_.
