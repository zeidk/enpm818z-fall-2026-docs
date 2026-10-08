====================================================
References
====================================================

These are the sources the L4 slides cite, grouped by topic, in the order the
slides first cite each group. The appendix, CNN Fundamentals, has its own
dropdown. A note at the end lists the entries of the lecture's bibliography
that no slide cites.


.. dropdown:: Detectors
   :class-container: sd-border-secondary
   :open:

   The two models used on every slide, YOLOv8s and RT-DETR-L, and the
   detectors the lecture compares them with.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: YOLO
         :class-card: sd-border-secondary

         **Redmon, J., Divvala, S., Girshick, R. and Farhadi, A. (2016)**

         "You Only Look Once: Unified, Real-Time Object Detection."
         *Proceedings of the IEEE Conference on Computer Vision and Pattern
         Recognition (CVPR)*.

         The name of the first model and of the **one-stage** family: one
         pass over a grid, and detection became real time.

      .. grid-item-card:: RT-DETR
         :link: https://arxiv.org/abs/2304.08069
         :class-card: sd-border-secondary

         **Zhao, Y., Lv, W., Xu, S., Wei, J., Wang, G., Dang, Q., Liu, Y. and
         Chen, J. (2024)**

         "DETRs Beat YOLOs on Real-time Object Detection." *Proceedings of
         the IEEE/CVF Conference on Computer Vision and Pattern Recognition
         (CVPR)*. arXiv:2304.08069.

         The second model, the Real-Time DEtection TRansformer: attention
         only inside the coarsest map, convolutions to mix the three map
         sizes, 53.0 mAP at 114 FPS on a T4 for RT-DETR-L.

      .. grid-item-card:: Ultralytics documentation
         :link: https://docs.ultralytics.com/
         :class-card: sd-border-secondary

         **Ultralytics**

         *Ultralytics Documentation: YOLOv8, YOLO11, YOLO26 and RT-DETR model
         pages.* Accessed 30 September 2026.

         The library both models come from, and the source of the published
         numbers: YOLOv8s at 44.9 mAP, YOLOv8l at 52.9, RT-DETR-L at 114
         FPS, YOLO26, and the default settings (cut 0.25, NMS at IoU 0.7).

      .. grid-item-card:: DETR
         :link: https://arxiv.org/abs/2005.12872
         :class-card: sd-border-secondary

         **Carion, N., Massa, F., Synnaeve, G., Usunier, N., Kirillov, A. and
         Zagoruyko, S. (2020)**

         "End-to-End Object Detection with Transformers." *European
         Conference on Computer Vision (ECCV)*. arXiv:2005.12872.

         Detection as a set: object queries, the Hungarian matching and no
         NMS. Also the 42.0 mAP after 500 training epochs, and the 6.0 AP lost
         on large objects without the encoder.

      .. grid-item-card:: Faster R-CNN
         :class-card: sd-border-secondary

         **Ren, S., He, K., Girshick, R. and Sun, J. (2015)**

         "Faster R-CNN: Towards Real-Time Object Detection with Region
         Proposal Networks." *Advances in Neural Information Processing
         Systems (NeurIPS)*.

         The **two-stage** example: first propose regions that may hold an
         object, then classify each one.

      .. grid-item-card:: Deformable DETR
         :link: https://arxiv.org/abs/2010.04159
         :class-card: sd-border-secondary

         **Zhu, X., Su, W., Lu, L., Li, B., Wang, X. and Dai, J. (2021)**

         "Deformable DETR: Deformable Transformers for End-to-End Object
         Detection." *International Conference on Learning Representations
         (ICLR)*. arXiv:2010.04159.

         Each query attends to a few sampling points instead of every cell,
         with 10 times fewer training epochs than DETR.

      .. grid-item-card:: RF-DETR
         :link: https://arxiv.org/abs/2511.09554
         :class-card: sd-border-secondary

         **Robinson, I., Robicheaux, P., Popov, M., Ramanan, D. and Peri, N.
         (2026)**

         "RF-DETR: Neural Architecture Search for Real-Time Detection
         Transformers." *International Conference on Learning
         Representations (ICLR)*. arXiv:2511.09554.

         A real-time DETR with a DINOv2 backbone: 60.1 mAP at 17.2 ms on a T4,
         and 20 times as fast as Grounding DINO (tiny).


.. dropdown:: Datasets and Their Classes
   :class-container: sd-border-secondary
   :open:

   A detector finds only the classes its dataset labels. These are the six
   class counts on the Object Detection slide.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: PASCAL VOC 2012
         :link: https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/
         :class-card: sd-border-secondary

         **Everingham, M., Van Gool, L., Williams, C. K. I., Winn, J. and
         Zisserman, A.**

         *The PASCAL Visual Object Classes Challenge 2012 (VOC2012).*
         Accessed 30 September 2026.

         20 classes of everyday images.

      .. grid-item-card:: COCO
         :class-card: sd-border-secondary

         **Lin, T.-Y., Maire, M., Belongie, S., Hays, J., Perona, P.,
         Ramanan, D., Dollár, P. and Zitnick, C. L. (2014)**

         "Microsoft COCO: Common Objects in Context." *European Conference on
         Computer Vision (ECCV)*.

         80 everyday classes. Both of the lecture's detectors are pretrained
         on COCO, and every mAP on the slides is a COCO mAP.

      .. grid-item-card:: Open Images V7
         :link: https://storage.googleapis.com/openimages/web/factsfigures_v7.html
         :class-card: sd-border-secondary

         **Google**

         *Open Images V7: Facts and Figures.* Accessed 30 September 2026.

         600 classes of everyday images.

      .. grid-item-card:: KITTI 2D benchmark
         :link: https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d
         :class-card: sd-border-secondary

         **Geiger, A., Lenz, P. and Urtasun, R.**

         *The KITTI Vision Benchmark Suite: 2D Object Detection Benchmark.*
         Accessed 30 September 2026.

         A driving benchmark that scores 3 classes: car, pedestrian and
         cyclist.

      .. grid-item-card:: Waymo Open Dataset
         :link: https://arxiv.org/abs/1912.04838v7
         :class-card: sd-border-secondary

         **Sun, P., Kretzschmar, H., Dotiwalla, X. and others (2020)**

         "Scalability in Perception for Autonomous Driving: Waymo Open
         Dataset." arXiv:1912.04838v7.

         The LiDAR set's 4 classes: vehicle, pedestrian, cyclist and sign.

      .. grid-item-card:: nuScenes detection task
         :link: https://github.com/nutonomy/nuscenes-devkit
         :class-card: sd-border-secondary

         **Motional**

         *nuScenes Detection Task: Evaluation Metrics (devkit README).*
         Accessed 28 September 2026.

         10 detection classes.


.. dropdown:: Features and Backbones
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Gradient histograms (HOG)
         :class-card: sd-border-secondary

         **Dalal, N. and Triggs, B. (2005)**

         "Histograms of Oriented Gradients for Human Detection." *IEEE
         Conference on Computer Vision and Pattern Recognition (CVPR)*, vol.
         1, 886 to 893.

         A hand-designed feature: how computers found pedestrians before
         CNNs.

      .. grid-item-card:: Keypoints for visual SLAM
         :class-card: sd-border-secondary

         **Mur-Artal, R., Montiel, J. M. M. and Tardós, J. D. (2015)**

         "ORB-SLAM: A Versatile and Accurate Monocular SLAM System." *IEEE
         Transactions on Robotics*, 31(5), 1147 to 1163.

         Corners found again in the next frame tell the AV where it is: a
         localization topic, not detection.

      .. grid-item-card:: DINOv3
         :link: https://arxiv.org/abs/2508.10104
         :class-card: sd-border-secondary

         **Siméoni, O., Vo, H. V., Seitzer, M., Baldassarre, F., Oquab, M.
         and others (2025)**

         "DINOv3." arXiv:2508.10104.

         A **foundation backbone**, trained without labels, whose features
         work for many tasks.


.. dropdown:: Attention and Transformers
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The transformer
         :link: https://arxiv.org/abs/1706.03762
         :class-card: sd-border-secondary

         **Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L.,
         Gomez, A. N., Kaiser, Ł. and Polosukhin, I. (2017)**

         "Attention Is All You Need." *Advances in Neural Information
         Processing Systems (NeurIPS)*. arXiv:1706.03762.

         The encoder and decoder diagram (its Figure 1) and the attention
         formula, :math:`\text{softmax}(QK^\top/\sqrt{d})\,V`.

      .. grid-item-card:: The Vision Transformer (ViT)
         :link: https://arxiv.org/abs/2010.11929
         :class-card: sd-border-secondary

         **Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai,
         X., Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly,
         S., Uszkoreit, J. and Houlsby, N. (2021)**

         "An Image is Worth 16x16 Words: Transformers for Image Recognition
         at Scale." *International Conference on Learning Representations
         (ICLR)*. arXiv:2010.11929.

         The Encoder subsection, part by part: patches, the class token, the
         position embedding, the encoder layer (norm before every block, the
         input added back after it) and the head.


.. dropdown:: Objects Outside the 80 Classes
   :class-container: sd-border-secondary
   :open:

   Open-vocabulary models, where the class is text you type at run time.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Grounding DINO
         :link: https://arxiv.org/abs/2303.05499
         :class-card: sd-border-secondary

         **Liu, S., Zeng, Z., Ren, T., Li, F., Zhang, H. and others (2023)**

         "Grounding DINO: Marrying DINO with Grounded Pre-Training for
         Open-Set Object Detection." arXiv:2303.05499.

         52.5 mAP on COCO without training on COCO.

      .. grid-item-card:: SAM 3
         :link: https://arxiv.org/abs/2511.16719
         :class-card: sd-border-secondary

         **Carion, N., Gustafson, L., Hu, Y.-T., Debnath, S., Hu, R. and
         others (2025)**

         "SAM 3: Segment Anything with Concepts." arXiv:2511.16719.

         A short phrase in, every matching object out, outlined pixel by
         pixel. Segmentation is :doc:`L5 <../lecture5/l5_index>`.


.. dropdown:: Appendix: CNN Fundamentals
   :class-container: sd-border-secondary

   Cited only in the appendix. The appendix also cites the Vision
   Transformer and the Ultralytics documentation, listed above.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: AlexNet
         :class-card: sd-border-secondary

         **Krizhevsky, A., Sutskever, I. and Hinton, G. E. (2012)**

         "ImageNet Classification with Deep Convolutional Neural Networks."
         *Advances in Neural Information Processing Systems (NeurIPS)*.

         A deep CNN trained on GPUs, with ReLU, that beat hand-designed
         features on ImageNet.

      .. grid-item-card:: VGG
         :link: https://arxiv.org/abs/1409.1556
         :class-card: sd-border-secondary

         **Simonyan, K. and Zisserman, A. (2015)**

         "Very Deep Convolutional Networks for Large-Scale Image
         Recognition." *International Conference on Learning Representations
         (ICLR)*. arXiv:1409.1556.

         Stacks of small :math:`3 \times 3` filters instead of large ones.

      .. grid-item-card:: ResNet
         :class-card: sd-border-secondary

         **He, K., Zhang, X., Ren, S. and Sun, J. (2016)**

         "Deep Residual Learning for Image Recognition." *Proceedings of the
         IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*.

         Skip connections, :math:`y = F(x) + x`, so a block learns only a
         correction.

      .. grid-item-card:: COCO evaluation code
         :link: https://github.com/cocodataset/cocoapi
         :class-card: sd-border-secondary

         **COCO Consortium**

         *COCO API: pycocotools/cocoeval.py.* Accessed 28 September 2026.

         How COCO computes AP for one class and one IoU threshold.

      .. grid-item-card:: word2vec
         :link: https://arxiv.org/abs/1301.3781
         :class-card: sd-border-secondary

         **Mikolov, T., Chen, K., Corrado, G. and Dean, J. (2013)**

         "Efficient Estimation of Word Representations in Vector Space."
         arXiv:1301.3781.

         Word vectors you can add: King minus Man plus Woman lands nearest
         Queen.

   The bibliography file also holds PointPillars (Lang et al., 2019),
   CenterPoint (Yin et al., 2021), Segment Anything (Kirillov et al., 2023)
   and nuScenes (Caesar et al., 2020), which no L4 slide cites. 3D detection
   and segmentation are taught in :doc:`L5 <../lecture5/l5_index>`.
