====================================================
References
====================================================

These are the sources of the L11 deck and of its "More detail" boxes,
grouped by the lecture's sections, in the order the lecture first uses each
one. Authors, titles, venues and years are those of the deck's bibliography
file. A source used in several sections is listed once, where the lecture
first uses it. Several sources are quoted only in a "More detail" box of the
lecture; their cards say so. A source with no link has no web address in the
bibliography file.


.. dropdown:: Introduction
   :class-container: sd-border-secondary
   :open:

   The definition of end-to-end driving.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: End-to-end driving: challenges and frontiers
         :link: https://arxiv.org/abs/2306.16927
         :class-card: sd-border-secondary

         **Chen, L., Wu, P., Chitta, K., Jaeger, B., Geiger, A. and Li, H.
         (2024)**

         *End-to-End Autonomous Driving: Challenges and Frontiers.* IEEE
         Transactions on Pattern Analysis and Machine Intelligence, 46(12),
         10164 to 10183. DOI 10.1109/TPAMI.2024.3435937.

         Quoted for the definition of end-to-end driving: "fully
         differentiable programs that take raw sensor data as input and
         produce a plan and/or low-level control actions as output".


.. dropdown:: Behavior Cloning
   :class-container: sd-border-secondary
   :open:

   The first and the best known cases of learning to drive from an expert's
   recorded examples.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ALVINN
         :class-card: sd-border-secondary

         **Pomerleau, D. A. (1988)**

         *ALVINN: An Autonomous Land Vehicle in a Neural Network.* In
         Touretzky, D. (ed.), Advances in Neural Information Processing
         Systems, volume 1, pages 305 to 313. Morgan-Kaufmann.

         Quoted for the 1988 network that took images from a camera and a
         laser range finder and gave the direction to travel. It was trained
         on simulated road images.

      .. grid-item-card:: End to end learning for self-driving cars
         :link: https://arxiv.org/abs/1604.07316
         :class-card: sd-border-secondary

         **Bojarski, M. et al. (2016)**

         *End to End Learning for Self-Driving Cars.* arXiv:1604.07316.

         Quoted for the convolutional network that maps raw pixels from one
         front-facing camera directly to steering commands, trained on about
         72 hours of driving. Quoted again, in a "More detail" box, for its
         off-center views from the left and right cameras.

      .. grid-item-card:: Rapidly adapting neural networks
         :class-card: sd-border-secondary

         **Pomerleau, D. A. (1990)**

         *Rapidly Adapting Artificial Neural Networks for Autonomous
         Navigation.* In Advances in Neural Information Processing Systems,
         volume 3, pages 429 to 435. Morgan-Kaufmann.

         Quoted in a "More detail" box for shifting and rotating each image
         to create extra training images, so the network learns to recover.


.. dropdown:: Compounding Error
   :class-container: sd-border-secondary
   :open:

   Why small mistakes grow when the policy drives.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Efficient reductions for imitation learning
         :class-card: sd-border-secondary

         **Ross, S. and Bagnell, J. A. (2010)**

         *Efficient Reductions for Imitation Learning.* Proceedings of the
         Thirteenth International Conference on Artificial Intelligence and
         Statistics (AISTATS), JMLR Workshop and Conference Proceedings,
         volume 9, pages 661 to 668.

         Quoted for the bound on behavior cloning's total cost, which grows
         as :math:`O(T^2)` in the horizon :math:`T`. Its theorem is stated in
         a "More detail" box.


.. dropdown:: DAgger
   :class-container: sd-border-secondary
   :open:

   The training loop that adds the states the clone reaches.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: DAgger
         :link: https://arxiv.org/abs/1011.0686
         :class-card: sd-border-secondary

         **Ross, S., Gordon, G. J. and Bagnell, J. A. (2011)**

         *A Reduction of Imitation Learning and Structured Prediction to
         No-Regret Online Learning.* Proceedings of the Fourteenth
         International Conference on Artificial Intelligence and Statistics
         (AISTATS), JMLR Workshop and Conference Proceedings, volume 15,
         pages 627 to 635. arXiv:1011.0686.

         Quoted for the algorithm (aggregate the datasets, train on the
         union), the mix of expert and clone that drives in each iteration,
         and, in a "More detail" box, the theorem that bounds DAgger's cost.


.. dropdown:: Commands
   :class-container: sd-border-secondary
   :open:

   A learned driver that follows the route, and the shortcuts a clone can
   learn instead of the task.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Conditional imitation learning
         :link: https://arxiv.org/abs/1710.02410
         :class-card: sd-border-secondary

         **Codevilla, F., Müller, M., López, A., Koltun, V. and Dosovitskiy,
         A. (2018)**

         *End-to-end Driving via Conditional Imitation Learning.* 2018 IEEE
         International Conference on Robotics and Automation (ICRA), pages
         4693 to 4700. DOI 10.1109/ICRA.2018.8460487.

         Quoted for why the camera input is not enough at an intersection, for
         the four commands, and for the command that acts as a switch between
         specialized sub-modules.

      .. grid-item-card:: Limits of behavior cloning
         :link: https://arxiv.org/abs/1904.08980
         :class-card: sd-border-secondary

         **Codevilla, F., Santana, E., López, A. M. and Gaidon, A. (2019)**

         *Exploring the Limitations of Behavior Cloning for Autonomous
         Driving.* Proceedings of the IEEE/CVF International Conference on
         Computer Vision (ICCV), pages 9328 to 9337. DOI
         10.1109/ICCV.2019.00942.

         Quoted in a "More detail" box for the limits of behavior cloning in
         CARLA, including "the inertia problem".

      .. grid-item-card:: Causal confusion
         :link: https://arxiv.org/abs/1905.11979
         :class-card: sd-border-secondary

         **de Haan, P., Jayaraman, D. and Levine, S. (2019)**

         *Causal Confusion in Imitation Learning.* Advances in Neural
         Information Processing Systems, volume 32. Curran Associates, Inc.

         Quoted in a "More detail" box for the brake-light example and the
         finding that "access to more information can yield worse
         performance".


.. dropdown:: Architectures
   :class-container: sd-border-secondary
   :open:

   TransFuser and UniAD.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: TransFuser (CVPR 2021)
         :link: https://arxiv.org/abs/2104.09224
         :class-card: sd-border-secondary

         **Prakash, A., Chitta, K. and Geiger, A. (2021)**

         *Multi-Modal Fusion Transformer for End-to-End Autonomous Driving.*
         Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern
         Recognition (CVPR), pages 7077 to 7087. DOI
         10.1109/CVPR46437.2021.00700.

         Quoted for the aim of fusing image and LiDAR features with attention,
         the auto-regressive waypoint prediction framework, and the two PID
         controllers.

      .. grid-item-card:: TransFuser (TPAMI 2023)
         :link: https://arxiv.org/abs/2205.15997
         :class-card: sd-border-secondary

         **Chitta, K., Prakash, A., Jaeger, B., Yu, Z., Renz, K. and Geiger, A.
         (2023)**

         *TransFuser: Imitation With Transformer-Based Sensor Fusion for
         Autonomous Driving.* IEEE Transactions on Pattern Analysis and
         Machine Intelligence, 45(11), 12878 to 12895. DOI
         10.1109/TPAMI.2022.3200245.

         Cited for the closed-loop test of TransFuser in CARLA.

      .. grid-item-card:: UniAD (CVPR 2023)
         :link: https://arxiv.org/abs/2212.10156
         :class-card: sd-border-secondary

         **Hu, Y. et al. (2023)**

         *Planning-oriented Autonomous Driving.* Proceedings of the IEEE/CVF
         Conference on Computer Vision and Pattern Recognition (CVPR), pages
         17853 to 17862. DOI 10.1109/CVPR52729.2023.01712.

         Quoted for the full-stack driving tasks in one network and the
         unified query interfaces.

      .. grid-item-card:: CVPR 2023 awards
         :link: https://cvpr.thecvf.com/Conferences/2023/Awards
         :class-card: sd-border-secondary

         **CVPR 2023**

         *CVPR 2023 Awards.* Web page, accessed 2026-10-14.

         Cited for UniAD's Best Paper award.


.. dropdown:: VLA
   :class-container: sd-border-secondary
   :open:

   Vision-language-action models, and four driving models from their makers.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: RT-2
         :link: https://arxiv.org/abs/2307.15818
         :class-card: sd-border-secondary

         **Brohan, A. et al. (2023)**

         *RT-2: Vision-Language-Action Models Transfer Web Knowledge to
         Robotic Control.* Proceedings of The 7th Conference on Robot Learning,
         Proceedings of Machine Learning Research, volume 229, pages 2165 to
         2183.

         Quoted for the definition of a vision-language-action model.

      .. grid-item-card:: DriveVLM
         :link: https://arxiv.org/abs/2402.12289
         :class-card: sd-border-secondary

         **Tian, X. et al. (2025)**

         *DriveVLM: The Convergence of Autonomous Driving and Large
         Vision-Language Models.* Proceedings of The 8th Conference on Robot
         Learning (CoRL 2024), Proceedings of Machine Learning Research,
         volume 270, pages 4698 to 4726.

         Quoted for the reasoning modules, the dual version on a production
         vehicle, the average inference speed of 410 ms on an NVIDIA OrinX
         chip, and the hand-over to a classical planner.

      .. grid-item-card:: EMMA (Waymo)
         :link: https://arxiv.org/abs/2410.23262
         :class-card: sd-border-secondary

         **Hwang, J.-J. et al. (2025)**

         *EMMA: End-to-End Multimodal Model for Autonomous Driving.*
         Transactions on Machine Learning Research.

         Quoted for the multi-modal large language model foundation, the text
         outputs, and the limits its authors list.

      .. grid-item-card:: Alpamayo-R1 (NVIDIA)
         :link: https://arxiv.org/abs/2511.00088
         :class-card: sd-border-secondary

         **NVIDIA (2025)**

         *Alpamayo-R1: Bridging Reasoning and Action Prediction for
         Generalizable Autonomous Driving in the Long Tail.* arXiv:2511.00088.

         Quoted for Chain of Causation reasoning with trajectory planning, and
         for the 99 ms on an NVIDIA RTX 6000 Pro Blackwell.

      .. grid-item-card:: Alpamayo-R1-10B model card
         :link: https://huggingface.co/nvidia/Alpamayo-R1-10B
         :class-card: sd-border-secondary

         **NVIDIA**

         *Alpamayo-R1-10B model card (renamed Alpamayo 1).* Web page,
         accessed 2026-11-20.

         Cited for the open weights, "ready for non-commercial use".

      .. grid-item-card:: Alpamayo 2 Super model card
         :link: https://huggingface.co/nvidia/Alpamayo2-Super
         :class-card: sd-border-secondary

         **NVIDIA**

         *Alpamayo 2 Super model card.* Web page, accessed 2026-11-20.

         Cited as NVIDIA's newer model, with its own model card.

      .. grid-item-card:: Alpamayo 2 Edge model card
         :link: https://huggingface.co/nvidia/Alpamayo2-Edge
         :class-card: sd-border-secondary

         **NVIDIA**

         *Alpamayo 2 Edge model card.* Web page, accessed 2026-11-21.

         Quoted for its size, 2B parameters, and its 64 waypoints from 0.1 to
         6.4 seconds.

      .. grid-item-card:: Running AV Reasoning Models Within Onboard Compute and Latency Limits
         :link: https://developer.nvidia.com/blog/running-av-reasoning-models-within-onboard-compute-and-latency-limits/
         :class-card: sd-border-secondary

         **Marco Pavone and Boris Ivanovic (NVIDIA, November 10, 2026)**

         *Running AV Reasoning Models Within Onboard Compute and Latency
         Limits.* NVIDIA Technical Blog, accessed 2026-11-21.

         Quoted for Alpamayo 2 Edge's 160 ms to 190 ms on NVIDIA DRIVE AGX
         Thor-X.

      .. grid-item-card:: LINGO-2
         :link: https://wayve.ai/thinking/lingo-2-driving-with-language/
         :class-card: sd-border-secondary

         **Wayve (2024)**

         *LINGO-2: Driving with Natural Language.* Web page, April 17, 2024,
         accessed 2026-10-14.

         Quoted for "the first closed-loop vision-language-action driving
         model (VLAM) tested on public roads".


.. dropdown:: Evaluation
   :class-container: sd-border-secondary
   :open:

   Open loop against closed loop, and two benchmarks.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Open-loop evaluation in nuScenes
         :link: https://arxiv.org/abs/2305.10430
         :class-card: sd-border-secondary

         **Zhai, J.-T. et al. (2023)**

         *Rethinking the Open-Loop Evaluation of End-to-End Autonomous Driving
         in nuScenes.* Technical report, arXiv:2305.10430.

         Quoted for AD-MLP, which plans without cameras, and used for its
         Table 1.

      .. grid-item-card:: Ego status in open-loop driving
         :link: https://arxiv.org/abs/2312.03031
         :class-card: sd-border-secondary

         **Li, Z. et al. (2024)**

         *Is Ego Status All You Need for Open-Loop End-to-End Autonomous
         Driving?* Proceedings of the IEEE/CVF Conference on Computer Vision
         and Pattern Recognition (CVPR), pages 14864 to 14873. DOI
         10.1109/CVPR52733.2024.01408.

         Quoted for the share of nuScenes data that is straight driving, and
         for models that rely on the AV's own status.

      .. grid-item-card:: NAVSIM
         :link: https://arxiv.org/abs/2406.15349
         :class-card: sd-border-secondary

         **Dauner, D. et al. (2024)**

         *NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and
         Benchmarking.* Advances in Neural Information Processing Systems
         (Datasets and Benchmarks Track), volume 37, pages 28706 to 28719. DOI
         10.52202/079017-0902.

         Quoted for the non-reactive simulation and the PDM Score.

      .. grid-item-card:: Bench2Drive
         :link: https://arxiv.org/abs/2406.03877
         :class-card: sd-border-secondary

         **Jia, X., Yang, Z., Li, Q., Zhang, Z. and Yan, J. (2024)**

         *Bench2Drive: Towards Multi-Ability Benchmarking of Closed-Loop
         End-To-End Autonomous Driving.* Advances in Neural Information
         Processing Systems (Datasets and Benchmarks Track), volume 37, pages
         819 to 844. DOI 10.52202/079017-0025.

         Quoted for the closed-loop benchmark in CARLA, with 44 interactive
         scenarios over 220 routes.


.. dropdown:: Modular or End-to-End
   :class-container: sd-border-secondary
   :open:

   The CARLA Leaderboard's rules, and what two companies say about their own
   systems.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: CARLA Leaderboard
         :link: https://leaderboard.carla.org/
         :class-card: sd-border-secondary

         **CARLA Team**

         *CARLA Autonomous Driving Leaderboard.* Web page, accessed
         2026-11-20.

         Cited for the statement that the Leaderboard has since closed.

      .. grid-item-card:: Leaderboard 2.1 evaluation criteria
         :link: https://leaderboard.carla.org/evaluation_v2_1/
         :class-card: sd-border-secondary

         **CARLA Team**

         *Evaluation Criteria for the Leaderboard 2.1.* Web page, accessed
         2026-10-14.

         Quoted for the route commands (``RoadOption.LEFT``) and for the ban
         on "any privilege information offered by the CARLA simulator".

      .. grid-item-card:: Tesla Q4 and FY 2023 update
         :link: https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q4-2023-Update.pdf
         :class-card: sd-border-secondary

         **Tesla, Inc. (2024)**

         *Q4 and FY 2023 Update.* Online document, accessed 2026-10-14.

         Quoted in a "More detail" box: "V12 utilizes end-to-end training".

      .. grid-item-card:: Tesla Q1 2024 update
         :link: https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q1-2024-Update.pdf
         :class-card: sd-border-secondary

         **Tesla, Inc. (2024)**

         *Q1 2024 Update.* Online document, accessed 2026-10-14.

         Quoted in a "More detail" box for the vision-only architecture with
         end-to-end neural networks.

      .. grid-item-card:: Waymo, demonstrably safe AI
         :link: https://waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving/
         :class-card: sd-border-secondary

         **Waymo (December 9, 2025)**

         *Demonstrably Safe AI For Autonomous Driving.* Web page, accessed
         2026-10-14.

         Quoted in a "More detail" box for Waymo's description of its
         architecture.


Image credits
-------------

The vehicle icon in the figures was created by Stone from the Noun Project
(https://thenounproject.com).
