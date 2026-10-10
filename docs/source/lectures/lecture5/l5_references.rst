====================================================
References
====================================================

These are the sources the L5 slides cite, grouped by topic, in the order the
slides first cite each group. A source cited in several sections is listed
once, where the slides first cite it. Every entry of the lecture's
bibliography is cited by a slide. The appendix (:doc:`l5_appendix`) cites
only sources that the main slides also cite: CenterPoint, BEVFormer,
Autoware's perception packages and the Waymo Open Dataset.


.. dropdown:: Situation Awareness and Real Driving Stacks
   :class-container: sd-border-secondary
   :open:

   The Introduction: what situation awareness is, and how two real stacks
   describe their perception.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Situation awareness
         :class-card: sd-border-secondary

         **Endsley, M. R. (2000)**

         "Theoretical Underpinnings of Situation Awareness: A Critical
         Review." In Endsley, M. R. and Garland, D. J. (eds.), *Situation
         Awareness Analysis and Measurement*. Lawrence Erlbaum Associates,
         Mahwah, NJ. The definition is credited there to Endsley (1988); the
         three-level model is from Endsley (1995), *Human Factors* 37(1), 32
         to 64.

         The definition of situation awareness and its three levels, and SA
         "as a stage separate from decision making and performance".

      .. grid-item-card:: Waymo's driver
         :link: https://waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving/
         :class-card: sd-border-secondary

         **Waymo AI Team (2025)**

         *Demonstrably Safe AI for Autonomous Driving.* 9 December 2025.
         Accessed 7 October 2026.

         The Sensor Fusion Encoder, the Driving VLM and the World Decoder,
         and the one sentence that describes the encoder.

      .. grid-item-card:: Autoware's perception design
         :link: https://github.com/autowarefoundation/autoware-documentation/blob/main/docs/design/autoware-architecture-v1/components/perception/reference_implementation.md
         :class-card: sd-border-secondary

         **Autoware Foundation**

         *Perception Component Reference Implementation Design.* Diagram
         reference-implementaion-perception-diagram.drawio.svg, commit
         f43b960. Accessed 7 October 2026.

         The source of the lecture's Autoware diagram: each job a separate
         module, tagged with the section that teaches it.


.. dropdown:: 3D Detection
   :class-container: sd-border-secondary
   :open:

   From LiDAR points to a 3D box: the sensor, the three forms of a point
   cloud, PointPillars and CenterPoint, and how a 3D detector is scored.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: CARLA's LiDAR
         :link: https://carla.readthedocs.io/en/0.9.16/ref_sensors/#lidar-sensor
         :class-card: sd-border-secondary

         **CARLA Team**

         *Sensors Reference: LIDAR Sensor (CARLA 0.9.16).* Accessed 7
         October 2026.

         CARLA's default LiDAR: 32 channels, from :math:`+10^\circ` to
         :math:`-30^\circ`. The lecture keeps the angles and chooses 64
         channels.

      .. grid-item-card:: PointNet
         :class-card: sd-border-secondary

         **Qi, C. R., Su, H., Mo, K. and Guibas, L. J. (2017)**

         "PointNet: Deep Learning on Point Sets for 3D Classification and
         Segmentation." *Proceedings of the IEEE Conference on Computer
         Vision and Pattern Recognition (CVPR)*.

         Points as a list: a network that "directly consumes point clouds"
         and gives the same answer however the list is shuffled.

      .. grid-item-card:: VoxelNet
         :class-card: sd-border-secondary

         **Zhou, Y. and Tuzel, O. (2018)**

         "VoxelNet: End-to-End Learning for Point Cloud Based 3D Object
         Detection." *Proceedings of the IEEE Conference on Computer Vision
         and Pattern Recognition (CVPR)*.

         Points as voxels: "equally spaced 3D voxels", read with 3D
         convolutions.

      .. grid-item-card:: SECOND
         :link: https://doi.org/10.3390/s18103337
         :class-card: sd-border-secondary

         **Yan, Y., Mao, Y. and Li, B. (2018)**

         "SECOND: Sparsely Embedded Convolutional Detection." *Sensors*,
         18(10), 3337. doi:10.3390/s18103337.

         Sparse convolution: compute only the voxels that hold points.

      .. grid-item-card:: PointPillars
         :link: https://arxiv.org/abs/1812.05784
         :class-card: sd-border-secondary

         **Lang, A. H., Vora, S., Caesar, H., Zhou, L., Yang, J. and
         Beijbom, O. (2019)**

         "PointPillars: Fast Encoders for Object Detection from Point
         Clouds." *Proceedings of the IEEE/CVF Conference on Computer Vision
         and Pattern Recognition (CVPR)*. arXiv:1812.05784.

         Pillars of :math:`0.16 \times 0.16` m, a pseudo-image seen from
         above, a 2D CNN and the SSD head; 62 frames per second on a 1080 Ti.

      .. grid-item-card:: CenterPoint
         :link: https://arxiv.org/abs/2006.11275
         :class-card: sd-border-secondary

         **Yin, T., Zhou, X. and Krähenbühl, P. (2021)**

         "Center-based 3D Object Detection and Tracking." *Proceedings of the
         IEEE/CVF Conference on Computer Vision and Pattern Recognition
         (CVPR)*. arXiv:2006.11275.

         Objects as heatmap peaks, the box read at each peak, and the
         velocity head. Also cited in the appendix and in tracking in
         industry.

      .. grid-item-card:: nuScenes detection metrics
         :link: https://github.com/nutonomy/nuscenes-devkit
         :class-card: sd-border-secondary

         **Motional**

         *nuScenes Detection Task: evaluation metrics (devkit README).*
         Accessed 28 September 2026.

         Matching by center distance (0.5, 1, 2 and 4 m), the five errors,
         and the nuScenes detection score (NDS).

      .. grid-item-card:: L-shape fitting
         :class-card: sd-border-secondary

         **Zhang, X., Xu, W., Dong, C. and Dolan, J. M. (2017)**

         "Efficient L-Shape Fitting for Vehicle Detection Using Laser
         Scanners." *IEEE Intelligent Vehicles Symposium (IV)*, 54 to 59.

         The box fit with no learning in the hands-on package
         ``l5_box_demo``.


.. dropdown:: In Industry
   :class-container: sd-border-secondary
   :open:

   What real AV software runs, from each maker's own documentation. First
   cited on "3D detection in industry"; Autoware's packages come back for
   BEV, fusion and tracking.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Autoware's perception packages
         :link: https://github.com/autowarefoundation/autoware_universe/tree/main/perception
         :class-card: sd-border-secondary

         **Autoware Foundation**

         *Autoware Universe: perception packages.* READMEs and source at
         commit 9ceaccf. Accessed 7 October 2026.

         CenterPoint on PointPillars in TensorRT, the camera BEV packages and
         BEVFusion, the fusion packages, and the tracker.

      .. grid-item-card:: Baidu Apollo
         :link: https://github.com/ApolloAuto/apollo/blob/master/RELEASE.md
         :class-card: sd-border-secondary

         **Baidu Apollo**

         *Apollo Release Notes (RELEASE.md).* Accessed 7 October 2026.

         CenterPoint as the default LiDAR model since release 9.0; visual BEV
         detection and an occupancy network in release 10.0.

      .. grid-item-card:: CUDA-PointPillars
         :link: https://github.com/NVIDIA-AI-IOT/CUDA-PointPillars
         :class-card: sd-border-secondary

         **NVIDIA**

         *CUDA-PointPillars.* Accessed 7 October 2026.

         PointPillars in TensorRT: 6.84 ms per frame on an Orin.

      .. grid-item-card:: CUDA-CenterPoint
         :link: https://github.com/NVIDIA-AI-IOT/Lidar_AI_Solution/tree/master/CUDA-CenterPoint
         :class-card: sd-border-secondary

         **NVIDIA**

         *CUDA-CenterPoint.* Accessed 7 October 2026.

         CenterPoint at 65.64 NDS and 23 frames per second on an Orin.

      .. grid-item-card:: Waymo Open Dataset
         :class-card: sd-border-secondary

         **Sun, P., Kretzschmar, H., Dotiwalla, X., Chouard, A. and others
         (2020)**

         "Scalability in Perception for Autonomous Driving: Waymo Open
         Dataset." *Proceedings of the IEEE/CVF Conference on Computer Vision
         and Pattern Recognition (CVPR)*.

         12.6 million labeled 3D boxes with tracking IDs, and 3D tracking
         ranked by MOTA.


.. dropdown:: Segmentation
   :class-container: sd-border-secondary
   :open:

   A class for every pixel or point, the kinds of segmentation, the datasets,
   the well-known models, and segmentation in Autoware. Most of these are
   cited on the reading slides.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Panoptic segmentation
         :link: https://arxiv.org/abs/1801.00868
         :class-card: sd-border-secondary

         **Kirillov, A., He, K., Girshick, R., Rother, C. and Dollár, P.
         (2019)**

         "Panoptic Segmentation." *Proceedings of the IEEE/CVF Conference on
         Computer Vision and Pattern Recognition (CVPR)*, 9396 to 9405.
         arXiv:1801.00868.

         The third kind: a class for every pixel, and an object id on
         things.

      .. grid-item-card:: SegFormer
         :link: https://arxiv.org/abs/2105.15203
         :class-card: sd-border-secondary

         **Xie, E., Wang, W., Yu, Z., Anandkumar, A., Alvarez, J. M. and
         Luo, P. (2021)**

         "SegFormer: Simple and Efficient Design for Semantic Segmentation
         with Transformers." *Advances in Neural Information Processing
         Systems (NeurIPS)*, 34, 12077 to 12090. arXiv:2105.15203.

         The semantic model of the pipeline slide and of ``l5_seg_demo``.

      .. grid-item-card:: Mask R-CNN
         :link: https://arxiv.org/abs/1703.06870
         :class-card: sd-border-secondary

         **He, K., Gkioxari, G., Dollár, P. and Girshick, R. (2017)**

         "Mask R-CNN." *Proceedings of the IEEE International Conference on
         Computer Vision (ICCV)*, 2980 to 2988. arXiv:1703.06870.

         An instance model: a two-stage detector plus a small mask for each
         box.

      .. grid-item-card:: Mask2Former
         :link: https://arxiv.org/abs/2112.01527
         :class-card: sd-border-secondary

         **Cheng, B., Misra, I., Schwing, A. G., Kirillov, A. and Girdhar, R.
         (2022)**

         "Masked-Attention Mask Transformer for Universal Image
         Segmentation." *Proceedings of the IEEE/CVF Conference on Computer
         Vision and Pattern Recognition (CVPR)*, 1290 to 1299.
         arXiv:2112.01527.

         One model for semantic, instance and panoptic segmentation.

      .. grid-item-card:: Cityscapes
         :link: https://arxiv.org/abs/1604.01685
         :class-card: sd-border-secondary

         **Cordts, M., Omran, M., Ramos, S., Rehfeld, T., Enzweiler, M.,
         Benenson, R., Franke, U., Roth, S. and Schiele, B. (2016)**

         "The Cityscapes Dataset for Semantic Urban Scene Understanding."
         *Proceedings of the IEEE Conference on Computer Vision and Pattern
         Recognition (CVPR)*, 3213 to 3223. arXiv:1604.01685.

         5000 finely labeled images from 50 cities, 19 classes graded; the
         training data of the lecture's SegFormer.

      .. grid-item-card:: SemanticKITTI
         :link: https://arxiv.org/abs/1904.01416
         :class-card: sd-border-secondary

         **Behley, J., Garbade, M., Milioto, A., Quenzel, J., Behnke, S.,
         Stachniss, C. and Gall, J. (2019)**

         "SemanticKITTI: A Dataset for Semantic Scene Understanding of LiDAR
         Sequences." *Proceedings of the IEEE/CVF International Conference
         on Computer Vision (ICCV)*, 9296 to 9306. arXiv:1904.01416.

         Over 43,000 labeled LiDAR scans, 19 classes graded.

      .. grid-item-card:: Autoware's segmentation packages
         :link: https://autowarefoundation.github.io/autoware_universe/main/perception/
         :class-card: sd-border-secondary

         **Autoware Foundation**

         *Autoware Universe: autoware_ground_segmentation,
         autoware_tensorrt_yolox and segmentation_pointcloud_fusion.*
         Accessed 8 October 2026.

         Removing the ground points, and passing the camera's classes to the
         LiDAR points.

      .. grid-item-card:: Ultralytics segmentation head
         :link: https://github.com/ultralytics/ultralytics
         :class-card: sd-border-secondary

         **Ultralytics**

         *Ultralytics 8.3.227: the segmentation head (nn/modules/head.py,
         Segment; nn/modules/block.py, Proto) and mask assembly
         (utils/ops.py, process_mask).* Accessed 8 October 2026.

         How YOLOv8s-seg builds a mask: 32 prototype masks and 32 numbers per
         object.

      .. grid-item-card:: YOLACT
         :link: https://arxiv.org/abs/1904.02689
         :class-card: sd-border-secondary

         **Bolya, D., Zhou, C., Xiao, F. and Lee, Y. J. (2019)**

         "YOLACT: Real-Time Instance Segmentation." *Proceedings of the
         IEEE/CVF International Conference on Computer Vision (ICCV)*, 9156
         to 9165. arXiv:1904.02689.

         Prototype masks and a few numbers per object, the idea YOLOv8s-seg
         uses.

      .. grid-item-card:: FCN
         :link: https://arxiv.org/abs/1411.4038
         :class-card: sd-border-secondary

         **Long, J., Shelhamer, E. and Darrell, T. (2015)**

         "Fully Convolutional Networks for Semantic Segmentation."
         *Proceedings of the IEEE Conference on Computer Vision and Pattern
         Recognition (CVPR)*, 3431 to 3440. arXiv:1411.4038.

         Every layer a convolution: any image size in, a score per pixel
         out.

      .. grid-item-card:: U-Net
         :link: https://arxiv.org/abs/1505.04597
         :class-card: sd-border-secondary

         **Ronneberger, O., Fischer, P. and Brox, T. (2015)**

         "U-Net: Convolutional Networks for Biomedical Image Segmentation."
         *Medical Image Computing and Computer-Assisted Intervention
         (MICCAI)*, 234 to 241. arXiv:1505.04597.

         A contracting path, then a symmetric expanding path that reuses
         copied feature maps.

      .. grid-item-card:: DeepLabv3+
         :link: https://arxiv.org/abs/1802.02611
         :class-card: sd-border-secondary

         **Chen, L.-C., Zhu, Y., Papandreou, G., Schroff, F. and Adam, H.
         (2018)**

         "Encoder-Decoder with Atrous Separable Convolution for Semantic
         Image Segmentation." *Proceedings of the European Conference on
         Computer Vision (ECCV)*, 833 to 851. arXiv:1802.02611.

         Atrous (dilated) convolution at several scales, and a decoder for
         sharp edges.

      .. grid-item-card:: Segment Anything (SAM)
         :link: https://arxiv.org/abs/2304.02643
         :class-card: sd-border-secondary

         **Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C.,
         Gustafson, L., Xiao, T., Whitehead, S., Berg, A. C., Lo, W.-Y.,
         Dollár, P. and Girshick, R. (2023)**

         "Segment Anything." *Proceedings of the IEEE/CVF International
         Conference on Computer Vision (ICCV)*. arXiv:2304.02643.

         Promptable segmentation: a point or a box in, a mask out. Trained on
         "over 1 billion masks on 11M licensed and privacy respecting
         images".

      .. grid-item-card:: RangeNet++
         :link: https://www.ipb.uni-bonn.de/pdfs/milioto2019iros.pdf
         :class-card: sd-border-secondary

         **Milioto, A., Vizzo, I., Behley, J. and Stachniss, C. (2019)**

         "RangeNet++: Fast and Accurate LiDAR Semantic Segmentation."
         *Proceedings of the IEEE/RSJ International Conference on Intelligent
         Robots and Systems (IROS)*, 4213 to 4220.
         doi:10.1109/IROS40897.2019.8967762.

         The scan as a range image, one row per laser ring: 12 frames per
         second on a desktop GPU, 5 on an embedded one.

      .. grid-item-card:: Cylinder3D
         :link: https://arxiv.org/abs/2011.10033
         :class-card: sd-border-secondary

         **Zhu, X., Zhou, H., Wang, T., Hong, F., Ma, Y., Li, W., Li, H. and
         Lin, D. (2021)**

         "Cylindrical and Asymmetrical 3D Convolution Networks for LiDAR
         Segmentation." *Proceedings of the IEEE/CVF Conference on Computer
         Vision and Pattern Recognition (CVPR)*, 9939 to 9948.
         arXiv:2011.10033.

         Cylinder-shaped cells that grow with distance: 89 percent of its
         cells hold points, against 61 for cubes.

      .. grid-item-card:: SAM 3
         :link: https://arxiv.org/abs/2511.16719
         :class-card: sd-border-secondary

         **Carion, N., Gustafson, L., Hu, Y.-T., Debnath, S., Hu, R. and
         others (2025)**

         "SAM 3: Segment Anything with Concepts." arXiv:2511.16719.

         A short phrase in, such as the paper's "yellow school bus", and a
         mask for every matching object out.


.. dropdown:: BEV and Occupancy
   :class-container: sd-border-secondary
   :open:

   The view from above: the grid, filling it from cameras, maps built on the
   fly, occupancy, and the BEV in cars.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: BEVFormer
         :link: https://doi.org/10.1007/978-3-031-20077-9_1
         :class-card: sd-border-secondary

         **Li, Z., Wang, W., Li, H., Xie, E., Sima, C., Lu, T., Qiao, Y. and
         Dai, J. (2022)**

         "BEVFormer: Learning Bird's-Eye-View Representation from
         Multi-Camera Images via Spatiotemporal Transformers." *Computer
         Vision, ECCV 2022*, Lecture Notes in Computer Science, Springer, 1
         to 18. doi:10.1007/978-3-031-20077-9_1.

         The lecture's grid: :math:`200 \times 200` cells of 0.512 m. The
         appendix covers how BEVFormer fills it.

      .. grid-item-card:: nuScenes
         :link: https://arxiv.org/abs/1903.11027
         :class-card: sd-border-secondary

         **Caesar, H., Bankiti, V., Lang, A. H., Vora, S., Liong, V. E., Xu,
         Q., Krishnan, A., Pan, Y., Baldan, G. and Beijbom, O. (2020)**

         "nuScenes: A Multimodal Dataset for Autonomous Driving."
         *Proceedings of the IEEE/CVF Conference on Computer Vision and
         Pattern Recognition (CVPR)*. arXiv:1903.11027.

         The six cameras of the nuScenes car: :math:`70^\circ` each,
         :math:`55^\circ` apart, the rear one :math:`110^\circ`.

      .. grid-item-card:: Lift-Splat-Shoot
         :link: https://doi.org/10.1007/978-3-030-58568-6_12
         :class-card: sd-border-secondary

         **Philion, J. and Fidler, S. (2020)**

         "Lift, Splat, Shoot: Encoding Images from Arbitrary Camera Rigs by
         Implicitly Unprojecting to 3D." *Computer Vision, ECCV 2020*,
         Lecture Notes in Computer Science, Springer, 194 to 210.
         doi:10.1007/978-3-030-58568-6_12.

         A probability for each depth bin along a pixel's ray, and each cell
         adds up what lands in it.

      .. grid-item-card:: MapTR
         :class-card: sd-border-secondary

         **Liao, B., Chen, S., Wang, X., Cheng, T., Zhang, Q., Liu, W. and
         Huang, C. (2023)**

         "MapTR: Structured Modeling and Learning for Online Vectorized HD
         Map Construction." *International Conference on Learning
         Representations (ICLR)*.

         Online mapping from cameras: lane lines as polylines, crosswalks as
         polygons; 25.1 frames per second on an RTX 3090 for its smallest
         version.

      .. grid-item-card:: Occ3D
         :link: https://doi.org/10.52202/075280-2809
         :class-card: sd-border-secondary

         **Tian, X., Jiang, T., Yun, L., Mao, Y., Yang, H., Wang, Y., Wang,
         Y. and Zhao, H. (2023)**

         "Occ3D: A Large-Scale 3D Occupancy Prediction Benchmark for
         Autonomous Driving." *Advances in Neural Information Processing
         Systems 36 (Datasets and Benchmarks Track)*, 64318 to 64330.
         doi:10.52202/075280-2809.

         Free, occupied and unobserved voxels, "general objects", and the
         0.4 m grid: 640,000 voxels every frame.

      .. grid-item-card:: Nissan's Around View Monitor
         :link: https://global.nissannews.com/en/releases/release-cebab286602dd889d775d066d038e490-071012-01-e
         :class-card: sd-border-secondary

         **Nissan Motor Co., Ltd. (2007)**

         *Nissan to Introduce World's First Around View Monitor.* 12 October
         2007.

         A bird's-eye image from four 180-degree cameras, for the driver when
         parking.

      .. grid-item-card:: Tesla AI
         :link: https://www.tesla.com/AI
         :class-card: sd-border-secondary

         **Tesla**

         *AI & Robotics.* Archived 2025-07-04 at web.archive.org. Accessed 7
         October 2026.

         Bird's-eye-view networks that output the road layout and 3D objects
         directly in the top-down view.

      .. grid-item-card:: Tesla AI Day 2022
         :link: https://www.youtube.com/watch?v=ODSJsviD_SU
         :class-card: sd-border-secondary

         **Tesla (2022)**

         *Tesla AI Day 2022.* Chapter "FSD | Occupancy Network" at 1:12:11.

         Tesla's occupancy network.


.. dropdown:: Fusion and Cooperative Situational Awareness
   :class-container: sd-border-secondary
   :open:

   Where the sensors meet, frustum association, and V2X on the road today.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: BEVFusion
         :link: https://doi.org/10.1109/ICRA48891.2023.10160968
         :class-card: sd-border-secondary

         **Liu, Z., Tang, H., Amini, A., Yang, X., Mao, H., Rus, D. L. and
         Han, S. (2023)**

         "BEVFusion: Multi-Task Multi-Sensor Fusion with Unified Bird's-Eye
         View Representation." *2023 IEEE International Conference on
         Robotics and Automation (ICRA)*, 2774 to 2781.
         doi:10.1109/ICRA48891.2023.10160968.

         Intermediate fusion: camera and LiDAR features joined on one BEV
         grid.

      .. grid-item-card:: DBSCAN
         :link: https://cdn.aaai.org/KDD/1996/KDD96-037.pdf
         :class-card: sd-border-secondary

         **Ester, M., Kriegel, H.-P., Sander, J. and Xu, X. (1996)**

         "A Density-Based Algorithm for Discovering Clusters in Large Spatial
         Databases with Noise." *KDD-96 Proceedings*, AAAI Press, 226 to 231.

         The clustering of frustum association, Step 3: car B's 41 points
         apart from the wall's 9.

      .. grid-item-card:: The U.S. V2X plan
         :link: https://www.its.dot.gov/research_areas/emerging_tech/pdf/Accelerate_V2X_Deployment_final.pdf
         :class-card: sd-border-secondary

         **U.S. Department of Transportation (2024)**

         *Saving Lives with Connectivity: A Plan to Accelerate V2X
         Deployment.* ITS Joint Program Office, 16 August 2024. Archived
         2024-08-16 at web.archive.org.

         Goals for V2X radios at the roadside by the end of 2028, 2031 and
         2036.

      .. grid-item-card:: The 5.9 GHz band
         :link: https://docs.fcc.gov/public/attachments/FCC-20-164A1.pdf
         :class-card: sd-border-secondary

         **Federal Communications Commission (2020)**

         *Use of the 5.850 to 5.925 GHz Band: First Report and Order, Further
         Notice of Proposed Rulemaking, and Order of Proposed Modification.*
         FCC 20-164. ET Docket No. 19-138. Adopted November 18, 2020.

         30 MHz kept for transportation, C-V2X required, and DSRC that "has
         barely been deployed".


.. dropdown:: Tracking
   :class-container: sd-border-secondary
   :open:

   The tracker's loop, the match distance, the four ways to associate, and
   the Tempe crash.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: SORT
         :link: https://doi.org/10.1109/ICIP.2016.7533003
         :class-card: sd-border-secondary

         **Bewley, A., Ge, Z., Ott, L., Ramos, F. and Upcroft, B. (2016)**

         "Simple Online and Realtime Tracking." *2016 IEEE International
         Conference on Image Processing (ICIP)*, 3464 to 3468.
         doi:10.1109/ICIP.2016.7533003.

         The lecture's loop (predict, associate, update, manage) on image
         boxes.

      .. grid-item-card:: Mahalanobis distance
         :class-card: sd-border-secondary

         **Mahalanobis, P. C. (1936)**

         "On the Generalised Distance in Statistics." *Proceedings of the
         National Institute of Sciences of India*, 2(1), 49 to 55.

         The score :math:`\varepsilon`: the miss divided by the uncertainty,
         squared.

      .. grid-item-card:: The Hungarian algorithm
         :link: https://doi.org/10.1002/nav.3800020109
         :class-card: sd-border-secondary

         **Kuhn, H. W. (1955)**

         "The Hungarian Method for the Assignment Problem." *Naval Research
         Logistics Quarterly*, 2(1 to 2), 83 to 97.
         doi:10.1002/nav.3800020109.

         How GNN finds the pairing with the lowest total distance.

      .. grid-item-card:: JPDA
         :link: https://doi.org/10.1109/JOE.1983.1145560
         :class-card: sd-border-secondary

         **Fortmann, T. E., Bar-Shalom, Y. and Scheffe, M. (1983)**

         "Sonar Tracking of Multiple Targets Using Joint Probabilistic Data
         Association." *IEEE Journal of Oceanic Engineering*, 8(3), 173 to
         184. doi:10.1109/JOE.1983.1145560.

         A probability-weighted blend of every detection in the gate.

      .. grid-item-card:: MHT
         :link: https://doi.org/10.1109/TAC.1979.1102177
         :class-card: sd-border-secondary

         **Reid, D. B. (1979)**

         "An Algorithm for Tracking Multiple Targets." *IEEE Transactions on
         Automatic Control*, 24(6), 843 to 854. doi:10.1109/TAC.1979.1102177.

         Multiple hypothesis tracking: several explanations kept across
         frames until later frames decide.

      .. grid-item-card:: Tempe, March 2018
         :link: https://www.ntsb.gov/investigations/AccidentReports/Reports/HAR1903.pdf
         :class-card: sd-border-secondary

         **National Transportation Safety Board (2019)**

         *Collision Between Vehicle Controlled by Developmental Automated
         Driving System and Pedestrian, Tempe, Arizona, March 18, 2018.*
         NTSB/HAR-19/03. Washington, DC, November 2019. Investigation
         HWY18MH010, adopted 19 November 2019.

         The timeline (5.6 s, 5.2 s, 1.2 s) and the sentence on the tracking
         history dropped at each change of class.


.. rubric:: Image credits

The vehicle icons in the lecture's figures were created by Stone from the
`Noun Project <https://thenounproject.com>`_.
