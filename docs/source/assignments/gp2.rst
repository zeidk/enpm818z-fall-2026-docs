====================================================
GP2: Perception -- YOLO vs DETR
====================================================

.. card::
   :class-card: sd-bg-dark sd-text-white sd-shadow-sm

   **GP2 -- At a Glance**

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 3 weeks (Week 5 -- Week 8)
      * - **Weight**
        - 40 points (40% of final project)
      * - **Lectures**
        - L3--L5
      * - **Team Size**
        - 4 students
      * - **Submission**
        - Canvas + GitHub repository link (same repo as GP1)

   .. note::

      GP2 is the **highest-weighted project** in the course (40%) because it
      requires collecting a custom dataset, training two fundamentally different
      deep learning architectures, and performing a rigorous quantitative and
      qualitative comparison.


Overview
--------

GP2 adds the **perception layer** to the ``ads_pipeline`` package your team
built in GP1. You will collect labeled training data directly from CARLA,
fine-tune both a CNN-based detector (YOLOv8) and a transformer-based detector
(RT-DETR), deploy each as a ROS 2 node, and perform a comprehensive comparison
across four environmental conditions.

By the end of GP2, your team will have:

- A **labeled driving dataset** of 2,000+ images collected from multiple
  CARLA towns and weather conditions.
- A **fine-tuned YOLOv8s model** evaluated on CARLA data across clear,
  rain, night, and fog conditions.
- A **fine-tuned RT-DETR-L model** evaluated with identical metrics and
  conditions for a fair comparison.
- A **ROS 2 detector node** that subscribes to the GP1 camera topic and
  publishes ``Detection2DArray`` messages, switchable between YOLO and DETR
  via a launch-time parameter.
- A **5--7 page comparison report** with quantitative tables and failure case
  analysis.

.. important::

   GP2 **extends** -- it does not replace -- the ``ads_pipeline`` package from
   GP1. You will add new files to the existing package. Do not start a new
   package. Graders will look for ``sensor_manager.py`` from GP1 alongside the
   new ``detector_node.py`` in the same package.


Learning Objectives
-------------------

After completing GP2, you will be able to:

- Collect and label a custom object detection dataset from a simulator.
- Convert bounding box annotations between CARLA, YOLO, and COCO formats.
- Fine-tune a CNN-based one-stage detector (YOLOv8) on a custom dataset.
- Fine-tune a transformer-based detector (RT-DETR) on the same dataset.
- Evaluate object detectors using standard metrics: mAP@0.5, mAP@0.5:0.95,
  precision, recall, and inference latency.
- Identify and analyze model failure modes through qualitative case studies.
- Integrate a deep learning inference pipeline into a ROS 2 node.
- Recommend the appropriate model architecture given operational constraints
  (speed, accuracy, weather robustness).


Provided Resources
------------------

All files below are on Canvas and the course GitHub. Download them before
starting each task.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - File
     - Description
   * - ``data_collector.py``
     - Drives the CARLA ego vehicle (autopilot), captures RGB images, and
       simultaneously extracts ground-truth 2D bounding boxes from CARLA's
       semantic sensor. Saves images and raw label JSONs.
   * - ``carla_to_yolo.py``
     - Converts raw CARLA bounding box JSONs to YOLO ``.txt`` format
       (normalized ``cx cy w h``). Handles class remapping.
   * - ``carla_to_coco.py``
     - Converts raw CARLA bounding box JSONs to COCO ``instances.json``
       format required by RT-DETR / Hugging Face Transformers.
   * - ``yolov8s.pt``
     - COCO pre-trained YOLOv8s weights (Ultralytics). Use as the starting
       checkpoint for fine-tuning.
   * - ``rtdetr-l.pt``
     - RT-DETR-L pre-trained weights. Use as the starting checkpoint.
   * - ``evaluate.py``
     - Unified evaluation framework. Runs both models on the test split and
       outputs mAP, precision, recall, and per-class AP in a
       ``comparison_table.csv``.
   * - ``data.yaml`` (example)
     - YOLOv8 dataset configuration template. Fill in your paths and class
       list.

.. note::

   ``data_collector.py`` relies on the ``sensor_manager.py`` node from GP1
   being active. Start CARLA and your GP1 launch file before running the
   collector script.


Tasks
-----

.. dropdown:: Task 1 -- Dataset Collection (15 pts)
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** Build a diverse, labeled dataset of 2,000+ images suitable for
   training both YOLO and DETR.

   **Requirements:**

   .. list-table::
      :widths: 35 65
      :class: compact-table

      * - **Image count**
        - >= 2,000 total (training + val + test)
      * - **Towns**
        - Minimum 3: Town01, Town03, Town05 (different road geometries)
      * - **Weather conditions**
        - Minimum 3: ``ClearNoon``, ``HardRainNoon``, ``ClearSunset``
      * - **Lighting cycles**
        - Both day and night (use CARLA's ``sun_altitude_angle``)
      * - **Classes**
        - ``vehicle``, ``pedestrian``, ``cyclist``,
          ``traffic_light``, ``stop_sign``
      * - **Split**
        - 70% train / 20% val / 10% test (stratified by town)

   **Collecting the data:**

   .. code-block:: bash

      # Start CARLA server
      ./CarlaUE4.sh -quality-level=Epic -resx=800 -resy=600

      # In a second terminal: start GP1 sensor nodes
      ros2 launch ads_pipeline sensors_launch.py

      # In a third terminal: run the provided collector script
      python3 data_collector.py \
          --town Town01 \
          --weather ClearNoon \
          --num-images 500 \
          --output-dir ~/gp2_data/raw/Town01_ClearNoon

      # Repeat for each town/weather combination

   **Converting to YOLO format** (run after all collection is done):

   .. code-block:: bash

      python3 carla_to_yolo.py \
          --input-dir ~/gp2_data/raw/ \
          --output-dir ~/gp2_data/yolo/ \
          --class-map vehicle:0 pedestrian:1 cyclist:2 \
                       traffic_light:3 stop_sign:4

   **Converting to COCO format** (for RT-DETR):

   .. code-block:: bash

      python3 carla_to_coco.py \
          --input-dir ~/gp2_data/raw/ \
          --output-dir ~/gp2_data/coco/ \
          --split train val test

   **Creating** ``data.yaml`` **(fill in your paths):**

   .. code-block:: yaml

      # training/data.yaml
      path: /home/<user>/gp2_data/yolo
      train: images/train
      val:   images/val
      test:  images/test

      nc: 5
      names:
        0: vehicle
        1: pedestrian
        2: cyclist
        3: traffic_light
        4: stop_sign

   **Dataset quality checklist:**

   - Confirm class balance: no single class should represent > 60% of
     all bounding boxes. If heavily imbalanced, collect more images of
     under-represented classes.
   - Verify label alignment: open 20 random images with their label overlays
     (``carla_to_yolo.py --visualize``) and confirm boxes are correctly placed.
   - Check for duplicates: consecutive autopilot frames are often nearly
     identical. Use the ``--skip-frames 5`` flag in ``data_collector.py`` to
     sample every 5th frame.

   **Deliverable:** ``training/dataset/`` directory and ``training/data.yaml``
   committed to the repository. Include a brief dataset statistics table in
   ``report.pdf`` (class counts, images per town/weather).

   .. tip::

      Collect in bulk from one town/weather at a time and convert immediately.
      This lets you catch label errors early before collecting thousands of
      images with the same bug.


.. dropdown:: Task 2 -- YOLO Training & Evaluation (25 pts)
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** Fine-tune YOLOv8s on your CARLA dataset, export the model, and
   evaluate it across four environmental conditions.

   **Training:**

   .. code-block:: python

      # training/train_yolo.py
      from ultralytics import YOLO
      import torch


      def train_yolo(data_yaml: str, weights: str = 'yolov8s.pt',
                     epochs: int = 100, imgsz: int = 640,
                     batch: int = 16, project: str = 'training_logs',
                     name: str = 'yolo_carla') -> None:
          """Fine-tune YOLOv8s on a custom CARLA dataset.

          Args:
              data_yaml: Path to the dataset YAML file.
              weights:   Pre-trained weights checkpoint (provided by instructor).
              epochs:    Number of training epochs. 100 is a good starting point.
              imgsz:     Input image size (square). 640 is the YOLOv8 default.
              batch:     Batch size. Reduce if you get CUDA out-of-memory errors.
              project:   Directory for saving training logs and checkpoints.
              name:      Subdirectory name for this run.
          """
          device = 'cuda' if torch.cuda.is_available() else 'cpu'
          print(f'Training on device: {device}')

          model = YOLO(weights)

          results = model.train(
              data=data_yaml,
              epochs=epochs,
              imgsz=imgsz,
              batch=batch,
              device=device,
              project=project,
              name=name,
              # Augmentation -- tune these for CARLA data
              hsv_h=0.015,     # Hue shift (helps with lighting variation)
              hsv_s=0.7,       # Saturation shift
              hsv_v=0.4,       # Value (brightness) shift
              flipud=0.0,      # No vertical flip for driving data
              fliplr=0.5,      # Horizontal flip (symmetric scenes)
              mosaic=1.0,      # Mosaic augmentation
              mixup=0.1,       # MixUp for regularization
              # Learning rate schedule
              lr0=0.01,
              lrf=0.01,
              warmup_epochs=3,
              cos_lr=True,
              # Logging
              plots=True,
              save=True,
              save_period=10,
              val=True,
          )

          print(f'Best mAP@0.5:0.95 = {results.results_dict["metrics/mAP50-95(B)"]:.4f}')


      def export_yolo(weights_path: str) -> None:
          """Export best checkpoint to ONNX and TensorRT for deployment."""
          model = YOLO(weights_path)
          model.export(format='onnx', dynamic=True, simplify=True)
          model.export(format='engine',   # TensorRT; requires tensorrt
                       half=True, device=0)


      if __name__ == '__main__':
          train_yolo(
              data_yaml='training/data.yaml',
              weights='yolov8s.pt',
              epochs=100,
          )

   **Launching training:**

   .. code-block:: bash

      cd ~/ros2_ws/src/GP2_Team{X}/training
      python3 train_yolo.py
      # Monitor: open training_logs/yolo_carla/results.png for live curves

   **Evaluation across conditions:**

   .. code-block:: bash

      # Use the provided evaluate.py script
      python3 evaluate.py \
          --model yolo \
          --weights training_logs/yolo_carla/weights/best.pt \
          --data training/data.yaml \
          --conditions ClearNoon HardRainNoon \
                        ClearNight SoftFogNoon \
          --output results/yolo_results/

   **Required metrics (for each of the 4 conditions):**

   .. list-table::
      :widths: 25 75
      :header-rows: 1
      :class: compact-table

      * - Metric
        - Description
      * - **mAP@0.5**
        - Mean average precision at IoU threshold 0.5.
      * - **mAP@0.5:0.95**
        - Mean average precision averaged over IoU 0.5--0.95 (COCO primary).
      * - **Precision**
        - TP / (TP + FP) -- how many detections are correct?
      * - **Recall**
        - TP / (TP + FN) -- how many ground-truth objects are found?
      * - **Inference time**
        - Mean latency in ms per image (GPU). Measure over 100 images.

   **Export the best model:**

   .. code-block:: bash

      python3 -c "
      from ultralytics import YOLO
      m = YOLO('training/training_logs/yolo_carla/weights/best.pt')
      m.export(format='onnx', dynamic=True)
      "
      cp training/training_logs/yolo_carla/weights/best.pt \
         ads_pipeline/models/yolo_best.pt

   **Deliverable:** Training logs in ``training/training_logs/``,
   ``results/yolo_results/`` directory with per-condition CSVs, and
   ``ads_pipeline/models/yolo_best.pt``.

   .. tip::

      Log training with Weights & Biases (``wandb``) for interactive loss
      curves. Add ``wandb=True`` to the ``model.train(...)`` call. This makes
      it trivial to compare YOLO and DETR training dynamics in your report.


.. dropdown:: Task 3 -- DETR Training & Evaluation (25 pts)
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** Fine-tune RT-DETR-L on the same CARLA dataset (COCO format),
   export the model, and evaluate with identical metrics and conditions
   as Task 2 for a fair comparison.

   **Why RT-DETR?**

   RT-DETR (Real-Time Detection Transformer) is an end-to-end transformer-based
   detector that eliminates the need for non-maximum suppression (NMS), making
   it architecturally very different from YOLO. Both models were trained on COCO,
   so a domain-adapted comparison on CARLA data reveals fundamental trade-offs
   between CNN and attention-based detectors.

   **Training:**

   .. code-block:: python

      # training/train_detr.py
      import torch
      from ultralytics import RTDETR


      def train_detr(data_yaml: str,
                     weights: str = 'rtdetr-l.pt',
                     epochs: int = 80,
                     imgsz: int = 640,
                     batch: int = 8,
                     project: str = 'training_logs',
                     name: str = 'detr_carla') -> None:
          """Fine-tune RT-DETR-L on a custom CARLA dataset (COCO format).

          Note: RT-DETR typically needs fewer epochs than YOLO because the
          transformer encoder converges faster on structured scene data.
          Batch size is smaller because the model is larger (~65M params).

          Args:
              data_yaml: Path to the dataset YAML file (same as YOLO).
              weights:   Pre-trained RT-DETR-L weights (provided).
              epochs:    Training epochs. 80 is recommended for RT-DETR-L.
              imgsz:     Input resolution. RT-DETR supports non-square.
              batch:     Reduce to 4 if you have < 16 GB VRAM.
              project:   Output directory for logs and checkpoints.
              name:      Subdirectory name for this training run.
          """
          device = 'cuda' if torch.cuda.is_available() else 'cpu'
          print(f'Training RT-DETR on device: {device}')

          model = RTDETR(weights)

          results = model.train(
              data=data_yaml,
              epochs=epochs,
              imgsz=imgsz,
              batch=batch,
              device=device,
              project=project,
              name=name,
              optimizer='AdamW',
              lr0=1e-4,            # Transformers prefer lower learning rate
              lrf=1e-5,
              warmup_epochs=5,
              weight_decay=1e-4,
              # Augmentation (more conservative for transformer)
              hsv_h=0.015,
              hsv_s=0.5,
              hsv_v=0.3,
              fliplr=0.5,
              mosaic=0.0,          # Mosaic can hurt transformer convergence
              mixup=0.0,
              # Logging
              plots=True,
              save=True,
              save_period=10,
              val=True,
          )

          best_map = results.results_dict.get(
              'metrics/mAP50-95(B)', float('nan'))
          print(f'Best mAP@0.5:0.95 = {best_map:.4f}')


      def export_detr(weights_path: str) -> None:
          """Export RT-DETR best checkpoint to ONNX."""
          model = RTDETR(weights_path)
          model.export(format='onnx', dynamic=True, simplify=True)


      if __name__ == '__main__':
          train_detr(
              data_yaml='training/data.yaml',
              weights='rtdetr-l.pt',
              epochs=80,
          )

   **Launching training:**

   .. code-block:: bash

      cd ~/ros2_ws/src/GP2_Team{X}/training
      python3 train_detr.py
      # Monitor: training_logs/detr_carla/results.png

   **Evaluation:**

   .. code-block:: bash

      python3 evaluate.py \
          --model detr \
          --weights training_logs/detr_carla/weights/best.pt \
          --data training/data.yaml \
          --conditions ClearNoon HardRainNoon \
                        ClearNight SoftFogNoon \
          --output results/detr_results/

   Use **exactly the same four conditions** as Task 2 so the comparison
   is valid.

   **Copying the best checkpoint into the package:**

   .. code-block:: bash

      cp training/training_logs/detr_carla/weights/best.pt \
         ads_pipeline/models/detr_best.pt

   **Deliverable:** Training logs in ``training/training_logs/``,
   ``results/detr_results/`` with per-condition CSVs, and
   ``ads_pipeline/models/detr_best.pt``.

   .. tip::

      RT-DETR uses a **hybrid encoder** (CNN backbone + transformer encoder +
      decoder). If training loss plateaus early, try unfreezing the backbone
      after epoch 20 with ``model.model.backbone.requires_grad_(True)``. This
      is not needed for YOLO and illustrates a key fine-tuning difference
      between the two architectures -- worth discussing in your report.


.. dropdown:: Task 4 -- ROS 2 Perception Node (20 pts)
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** Implement ``detector_node.py`` -- a ROS 2 node that runs
   real-time inference on the GP1 camera stream and publishes standard
   detection messages. The model (YOLO or DETR) must be switchable via a
   ROS 2 parameter without modifying source code.

   **Interface requirements:**

   .. list-table::
      :widths: 25 30 45
      :header-rows: 1
      :class: compact-table

      * - Direction
        - Topic / Parameter
        - Type
      * - Subscribe
        - ``/carla/camera/rgb/image``
        - ``sensor_msgs/Image``
      * - Publish
        - ``/perception/detections``
        - ``vision_msgs/Detection2DArray``
      * - Publish
        - ``/perception/annotated_image``
        - ``sensor_msgs/Image``
      * - Parameter
        - ``model_type`` (``yolo`` or ``detr``)
        - ``string``
      * - Parameter
        - ``model_path``
        - ``string`` (path to ``.pt`` file)
      * - Parameter
        - ``confidence_threshold``
        - ``double`` (default: 0.5)
      * - Parameter
        - ``device``
        - ``string`` (default: ``cuda``)

   **Implementation:**

   .. code-block:: python

      # ads_pipeline/detector_node.py
      import rclpy
      from rclpy.node import Node
      from sensor_msgs.msg import Image
      from vision_msgs.msg import Detection2DArray, Detection2D, \
          BoundingBox2D, ObjectHypothesisWithPose
      from cv_bridge import CvBridge
      import numpy as np
      import cv2
      import torch


      CLASS_NAMES = {
          0: 'vehicle',
          1: 'pedestrian',
          2: 'cyclist',
          3: 'traffic_light',
          4: 'stop_sign',
      }

      # Distinct BGR colors per class (for annotation overlay)
      CLASS_COLORS = {
          0: (255, 100,  50),   # vehicle    -- blue-orange
          1: ( 50, 255,  50),   # pedestrian -- green
          2: (255, 255,  50),   # cyclist    -- yellow
          3: ( 50,  50, 255),   # traffic_light -- red
          4: (200,  50, 200),   # stop_sign  -- purple
      }


      class DetectorNode(Node):
          def __init__(self):
              super().__init__('detector_node')

              # --- Parameters ---
              self.declare_parameter('model_type', 'yolo')
              self.declare_parameter('model_path', '')
              self.declare_parameter('confidence_threshold', 0.5)
              self.declare_parameter('device', 'cuda')

              model_type = self.get_parameter('model_type').value
              model_path = self.get_parameter('model_path').value
              self.conf_thresh = self.get_parameter(
                  'confidence_threshold').value
              device = self.get_parameter('device').value

              # --- Load model ---
              self.model = self._load_model(model_type, model_path, device)
              self.model_type = model_type
              self.bridge = CvBridge()

              # --- Publishers ---
              self.det_pub = self.create_publisher(
                  Detection2DArray, '/perception/detections', 10)
              self.img_pub = self.create_publisher(
                  Image, '/perception/annotated_image', 10)

              # --- Subscriber ---
              self.sub = self.create_subscription(
                  Image,
                  '/carla/camera/rgb/image',
                  self._image_callback,
                  10)

              self.get_logger().info(
                  f'DetectorNode ready | model={model_type} | '
                  f'threshold={self.conf_thresh:.2f} | device={device}')

          # ------------------------------------------------------------------
          def _load_model(self, model_type: str, path: str, device: str):
              if model_type == 'yolo':
                  from ultralytics import YOLO
                  model = YOLO(path)
                  model.to(device)
                  self.get_logger().info(f'Loaded YOLOv8 from {path}')
                  return model
              elif model_type == 'detr':
                  from ultralytics import RTDETR
                  model = RTDETR(path)
                  model.to(device)
                  self.get_logger().info(f'Loaded RT-DETR from {path}')
                  return model
              else:
                  raise ValueError(
                      f"Unknown model_type '{model_type}'. "
                      "Use 'yolo' or 'detr'.")

          # ------------------------------------------------------------------
          def _image_callback(self, msg: Image) -> None:
              bgr = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

              # Run inference
              results = self.model.predict(
                  bgr,
                  conf=self.conf_thresh,
                  verbose=False,
              )

              det_array_msg = self._results_to_ros(results, msg.header)
              annotated = self._draw_detections(bgr, results)

              self.det_pub.publish(det_array_msg)
              ann_msg = self.bridge.cv2_to_imgmsg(annotated, 'bgr8')
              ann_msg.header = msg.header
              self.img_pub.publish(ann_msg)

          # ------------------------------------------------------------------
          def _results_to_ros(self, results, header) -> Detection2DArray:
              array = Detection2DArray()
              array.header = header

              for r in results:
                  if r.boxes is None:
                      continue
                  boxes = r.boxes.xyxy.cpu().numpy()    # (N, 4) x1y1x2y2
                  confs = r.boxes.conf.cpu().numpy()    # (N,)
                  cls   = r.boxes.cls.cpu().numpy().astype(int)  # (N,)

                  for (x1, y1, x2, y2), conf, class_id in \
                          zip(boxes, confs, cls):
                      det = Detection2D()
                      det.header = header

                      bbox = BoundingBox2D()
                      bbox.center.position.x = float((x1 + x2) / 2)
                      bbox.center.position.y = float((y1 + y2) / 2)
                      bbox.size_x = float(x2 - x1)
                      bbox.size_y = float(y2 - y1)
                      det.bbox = bbox

                      hyp = ObjectHypothesisWithPose()
                      hyp.hypothesis.class_id = str(class_id)
                      hyp.hypothesis.score = float(conf)
                      det.results.append(hyp)

                      array.detections.append(det)

              return array

          # ------------------------------------------------------------------
          def _draw_detections(self, bgr: np.ndarray, results) -> np.ndarray:
              img = bgr.copy()
              for r in results:
                  if r.boxes is None:
                      continue
                  boxes = r.boxes.xyxy.cpu().numpy().astype(int)
                  confs = r.boxes.conf.cpu().numpy()
                  cls   = r.boxes.cls.cpu().numpy().astype(int)

                  for (x1, y1, x2, y2), conf, class_id in \
                          zip(boxes, confs, cls):
                      color = CLASS_COLORS.get(class_id, (200, 200, 200))
                      label = (f'{CLASS_NAMES.get(class_id, str(class_id))}'
                               f' {conf:.2f}')
                      cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                      cv2.putText(img, label, (x1, y1 - 8),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
              return img


      def main(args=None):
          rclpy.init(args=args)
          node = DetectorNode()
          try:
              rclpy.spin(node)
          except KeyboardInterrupt:
              pass
          finally:
              rclpy.shutdown()

   **Perception launch file** (add to ``launch/``):

   .. code-block:: python

      # launch/perception_launch.py
      import os
      from launch import LaunchDescription
      from launch.actions import IncludeLaunchDescription
      from launch.launch_description_sources import (
          PythonLaunchDescriptionSource)
      from launch_ros.actions import Node
      from ament_index_python.packages import get_package_share_directory


      def generate_launch_description():
          pkg_share = get_package_share_directory('ads_pipeline')

          sensors = IncludeLaunchDescription(
              PythonLaunchDescriptionSource(
                  os.path.join(pkg_share, 'launch', 'sensors_launch.py')))

          detector = Node(
              package='ads_pipeline',
              executable='detector_node',
              name='detector_node',
              parameters=[{
                  'model_type': 'yolo',          # switch to 'detr' here
                  'model_path': os.path.join(
                      pkg_share, '..', '..', '..', '..',
                      'src', 'ads_pipeline', 'models', 'yolo_best.pt'),
                  'confidence_threshold': 0.5,
                  'device': 'cuda',
              }],
              output='screen',
          )

          return LaunchDescription([sensors, detector])

   **Switching between YOLO and DETR at launch time:**

   .. code-block:: bash

      # Launch with YOLO (default)
      ros2 launch ads_pipeline perception_launch.py

      # Override to DETR without editing the launch file
      ros2 launch ads_pipeline perception_launch.py \
          model_type:=detr \
          model_path:=/path/to/detr_best.pt

   **Verifying the node:**

   .. code-block:: bash

      # In another terminal: check detection output
      ros2 topic echo /perception/detections
      ros2 topic hz /perception/annotated_image

      # View annotated stream in RViz2:
      # Add an Image display subscribed to /perception/annotated_image

   **Deliverable:** ``ads_pipeline/detector_node.py``,
   ``launch/perception_launch.py``, and ``config/detector_config.yaml``
   committed to the repository. The node must run without errors with both
   ``model_type:=yolo`` and ``model_type:=detr``.

   .. tip::

      Add ``detector_config.yaml`` to the ``config/`` directory with
      model path and threshold settings. Load it in the launch file using
      ``parameters=[detector_config_path]``. This avoids hard-coded paths
      inside the launch file and makes switching models even easier.


.. dropdown:: Task 5 -- Comparison Report (15 pts)
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** Produce a rigorous 5--7 page technical report that compares YOLO
   and DETR on your CARLA dataset. The report must go beyond raw numbers to
   provide analysis and a justified recommendation.

   **Required sections:**

   **1. Dataset Summary (0.5 pages)**

   - Total images, images per town, images per weather condition.
   - Class distribution table (number of bounding boxes per class).
   - Sample images from each condition (annotated with ground-truth boxes).

   **2. Quantitative Comparison Table**

   Fill in ``results/comparison_table.csv`` (generated by ``evaluate.py``)
   and reproduce it in the report. It must cover all 4 conditions:

   .. list-table::
      :widths: 20 10 10 10 10 10 10 10 10
      :header-rows: 2
      :class: compact-table

      * -
        - **ClearNoon**
        - **ClearNoon**
        - **HardRain**
        - **HardRain**
        - **Night**
        - **Night**
        - **Fog**
        - **Fog**
      * - **Model**
        - mAP50
        - FPS
        - mAP50
        - FPS
        - mAP50
        - FPS
        - mAP50
        - FPS
      * - YOLOv8s
        - --
        - --
        - --
        - --
        - --
        - --
        - --
        - --
      * - RT-DETR-L
        - --
        - --
        - --
        - --
        - --
        - --
        - --
        - --

   **3. Per-Class Performance Breakdown (0.5 pages)**

   For each class (vehicle, pedestrian, cyclist, traffic_light, stop_sign):
   AP@0.5 for YOLO vs DETR, both under ClearNoon. Which model is stronger
   for small objects (pedestrians, cyclists)? For fast-moving objects?

   **4. Qualitative Failure Analysis (1.5 pages, minimum 5 cases)**

   For each failure case:

   - Screenshot with ground-truth boxes (green) and predicted boxes (red).
   - **Which model failed** and under **which condition**.
   - **Root cause analysis:** Is it a localization error (wrong box size),
     classification error (right box, wrong class), a missed detection
     (false negative), or a false positive?
   - **Why** did the model fail here? (occlusion, low contrast, novel
     appearance, sensor noise, etc.)

   .. code-block:: text

      Example failure case structure:

      Case 3: RT-DETR misses cyclist in HardRainNoon
      ------------------------------------------------
      Condition:   HardRainNoon, Town03, 2 NPC vehicles, 1 cyclist
      Model:       RT-DETR-L
      Failure type: False negative (missed detection)
      IoU of best matching box: 0.23 (below 0.5 threshold)

      Analysis: The cyclist is partially occluded by a rain droplet
      artifact on the camera lens and appears at ~20 pixels wide (far
      distance). RT-DETR's encoder attends to large-scale features first;
      at this scale, the cyclist token is suppressed by the larger vehicle
      tokens in the same spatial region. YOLO's anchor-based head at the
      small-scale detection layer (P2) successfully detects the same cyclist
      with IoU 0.61 because it explicitly models small objects with
      dedicated anchors.

   **5. Recommendation (0.5 pages)**

   Given your results, recommend one model for each scenario:

   - **Real-time deployment on embedded hardware** (< 30 ms latency required)
   - **High-accuracy urban driving** (pedestrians and cyclists critical)
   - **Adverse weather robustness** (rain, fog, night)

   Support every recommendation with specific numbers from your tables.

   **Deliverable:** ``report.pdf`` (5--7 pages, PDF/A) submitted on Canvas.
   Also commit ``results/comparison_table.csv`` to the repository.

   .. tip::

      Use the provided ``evaluate.py --visualize-failures`` flag to
      automatically generate annotated failure case images. This saves
      significant time compared to manually finding and annotating failures.


Folder Structure
----------------

Your GP2 submission extends the GP1 folder in the **same repository**. The
``ads_pipeline`` package gains new files; do not delete GP1 files.

.. code-block:: text

   GP2_Team{X}/
   ├── ads_pipeline/                      # Extended from GP1 (same package)
   │   ├── ads_pipeline/                  # Python module
   │   │   ├── __init__.py
   │   │   ├── sensor_manager.py          # From GP1 (do not modify)
   │   │   ├── lidar_projection.py        # From GP1 (do not modify)
   │   │   └── detector_node.py           # NEW -- Task 4
   │   ├── config/
   │   │   ├── carla_config.yaml          # From GP1
   │   │   └── detector_config.yaml       # NEW -- Task 4
   │   ├── launch/
   │   │   ├── sensors_launch.py          # From GP1
   │   │   ├── record_launch.py           # From GP1
   │   │   └── perception_launch.py       # NEW -- Task 4
   │   ├── models/
   │   │   ├── yolo_best.pt               # NEW -- Task 2 output
   │   │   └── detr_best.pt               # NEW -- Task 3 output
   │   ├── rviz/
   │   │   └── ads_pipeline.rviz          # From GP1 (add detection display)
   │   ├── resource/
   │   │   └── ads_pipeline
   │   ├── package.xml                    # Updated: add vision_msgs dependency
   │   └── setup.py                       # Updated: add detector_node entry point
   ├── training/
   │   ├── dataset/
   │   │   ├── images/
   │   │   │   ├── train/                 # Training images
   │   │   │   ├── val/                   # Validation images
   │   │   │   └── test/                  # Test images
   │   │   └── labels/
   │   │       ├── train/                 # YOLO .txt label files
   │   │       ├── val/
   │   │       └── test/
   │   ├── data.yaml                      # Task 1 deliverable
   │   ├── train_yolo.py                  # Task 2 deliverable
   │   ├── train_detr.py                  # Task 3 deliverable
   │   └── training_logs/
   │       ├── yolo_carla/                # Ultralytics run outputs
   │       └── detr_carla/                # RT-DETR run outputs
   ├── results/
   │   ├── yolo_results/                  # Per-condition evaluation CSVs
   │   ├── detr_results/                  # Per-condition evaluation CSVs
   │   └── comparison_table.csv           # Task 5 deliverable
   └── report.pdf                         # Task 5 deliverable


.. important::

   **Submission Instructions**

   1. Push the extended ``GP2_Team{X}/`` directory to the ``gp2`` branch of
      your team's GitHub repository.
   2. Submit the GitHub repository link AND ``report.pdf`` on Canvas by the
      deadline (end of Week 8, 11:59 PM).
   3. Model weights (``yolo_best.pt``, ``detr_best.pt``) must be in
      ``ads_pipeline/models/`` and accessible from the repository. If files
      exceed GitHub's 100 MB limit, use Git LFS:
      ``git lfs track "*.pt"``
   4. The COCO dataset directory (``training/dataset/``) should be committed
      **only** if total size is < 500 MB. Otherwise, provide a download link
      in a ``README.md`` inside ``training/``.
   5. Tag your submission commit: ``git tag gp2-final && git push --tags``


Submission Checklist
--------------------

.. admonition:: Before Submitting -- Check Every Item
   :class: tip

   **Dataset (Task 1)**

   - [ ] >= 2,000 images total across all splits.
   - [ ] Minimum 3 CARLA towns represented.
   - [ ] Minimum 3 weather conditions represented.
   - [ ] Day and night images both present.
   - [ ] All 5 classes present in the dataset.
   - [ ] ``training/data.yaml`` committed and paths correct.
   - [ ] 20 label overlays manually verified (no misaligned boxes).

   **YOLO Training (Task 2)**

   - [ ] Training completed for >= 100 epochs (or until convergence).
   - [ ] ``training_logs/yolo_carla/results.png`` shows converging loss.
   - [ ] Best weights saved to ``ads_pipeline/models/yolo_best.pt``.
   - [ ] Evaluation run on all 4 conditions; CSVs in ``results/yolo_results/``.
   - [ ] ONNX export completed.

   **DETR Training (Task 3)**

   - [ ] Training completed for >= 80 epochs (or until convergence).
   - [ ] ``training_logs/detr_carla/results.png`` shows converging loss.
   - [ ] Best weights saved to ``ads_pipeline/models/detr_best.pt``.
   - [ ] Evaluation run on **identical** 4 conditions as YOLO.
   - [ ] CSVs in ``results/detr_results/``.

   **ROS 2 Node (Task 4)**

   - [ ] ``detector_node.py`` committed to ``ads_pipeline/ads_pipeline/``.
   - [ ] ``setup.py`` updated with ``detector_node`` entry point.
   - [ ] ``package.xml`` updated with ``vision_msgs`` dependency.
   - [ ] Node runs without error: ``ros2 launch ads_pipeline perception_launch.py``.
   - [ ] ``/perception/detections`` publishes ``Detection2DArray`` messages.
   - [ ] ``/perception/annotated_image`` visible in RViz2.
   - [ ] ``model_type:=detr`` override works without code changes.

   **Report (Task 5)**

   - [ ] 5--7 pages, PDF/A format.
   - [ ] Quantitative comparison table (all 4 conditions, both models).
   - [ ] Per-class AP breakdown.
   - [ ] >= 5 annotated failure cases with root cause analysis.
   - [ ] Recommendation section with numbers-backed justification.
   - [ ] ``results/comparison_table.csv`` committed to repository.

   **Repository**

   - [ ] Folder structure matches required layout.
   - [ ] ``report.pdf`` submitted on Canvas.
   - [ ] Commit tagged ``gp2-final`` and pushed.
   - [ ] GP1 files (``sensor_manager.py``, ``lidar_projection.py``) still
         present and unmodified.
   - [ ] Peer evaluation submitted on Canvas within 48 hours.


Grading Rubric
--------------

Total: **100 points** (scaled to 40% of final project grade).

.. list-table::
   :widths: 40 15 45
   :header-rows: 1
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - Dataset quality
     - 15
     - >= 2,000 images, >= 3 towns, >= 3 weather conditions, day + night,
       all 5 classes present, correct YOLO and COCO format conversion,
       reasonable class balance. **-5** if < 1,500 images.
       **-5** if labels are misaligned in > 10% of checked images.
   * - YOLO training & evaluation
     - 25
     - Training converges (loss curve), best checkpoint saved, evaluation
       on all 4 conditions with all required metrics. **-10** if only
       trained on ClearNoon. **-5** if no ONNX export.
   * - DETR training & evaluation
     - 25
     - Same criteria as YOLO. Must use identical evaluation conditions for
       fair comparison. **-10** if conditions differ from YOLO evaluation.
       **-5** if learning rate not tuned (default YOLO lr used for DETR).
   * - ROS 2 node
     - 20
     - Node launches, subscribes to GP1 camera topic, publishes
       ``Detection2DArray`` and annotated image, switches between YOLO and
       DETR via parameter. **-10** if model is not switchable at runtime.
       **-5** if annotated image is not published.
   * - Comparison report
     - 15
     - Quantitative table complete, >= 5 failure cases with analysis,
       per-class breakdown, justified recommendation. **-5** if fewer than
       3 failure cases analyzed. **-5** if recommendation has no
       quantitative support.

.. note::

   **Individual grade** = 60% project grade + 40% peer review score.
   GP2 peer evaluations are weighted more heavily in final grade
   calculations because this project has the highest team workload.


Common Mistakes
---------------

.. danger::

   **These mistakes are seen every semester. Avoid them.**

   - **Using the same evaluation conditions as the training split.**
     Evaluation must be performed on the **test split only**. Reporting
     validation set mAP as test mAP inflates your numbers and constitutes
     data leakage. Use ``evaluate.py --split test``.

   - **Comparing models on different image resolutions.**
     Both YOLO and DETR must be evaluated at the same input resolution
     (640x640 by default). Evaluating DETR at 800x800 while YOLO is at
     640x640 makes the comparison unfair and invalidates conclusions.

   - **Not accounting for CARLA's coordinate convention.**
     ``data_collector.py`` handles the conversion, but if you write your own
     collection script, remember that CARLA uses a left-handed coordinate
     system. Bounding boxes extracted directly from semantic data may be
     mirrored horizontally.

   - **Forgetting to update** ``setup.py`` **after adding** ``detector_node.py``.
     If the ``console_scripts`` entry is missing, ``ros2 run`` will fail with
     a "no executable found" error, and Task 4 will receive zero credit.

   - **Insufficient failure analysis.**
     Writing "the model failed because the image was dark" with no further
     reasoning receives minimal credit. Identify whether it is a false
     negative, false positive, or localization error, and explain the
     architectural reason (e.g., attention mechanism, anchor scale).

   - **Training DETR with YOLO hyperparameters.**
     RT-DETR uses AdamW and a lower learning rate (1e-4) compared to YOLO's
     SGD (lr0=0.01). Using YOLO defaults for DETR training will result in
     divergence or very poor convergence. Always check the architecture's
     recommended hyperparameters.

   - **Large model files crashing Git.**
     Files > 100 MB cannot be pushed to GitHub without Git LFS.
     Run ``git lfs track "*.pt"`` and ``git lfs install`` before adding
     model weights. Check with ``git lfs status`` before pushing.


Tips for Success
----------------

.. tip::

   **Allocate at least 3 full days for data collection.**
   Running ``data_collector.py`` for multiple towns and weather conditions
   is time-consuming. Start data collection at the beginning of Week 5. Do
   not leave it for Week 7 -- you will not have time to retrain if you
   discover label errors late.

.. tip::

   **Train on a GPU -- CPU training is impractical.**
   YOLOv8s on 2,000 images for 100 epochs takes approximately 2 hours on
   a mid-range GPU (RTX 3070) and 40+ hours on a CPU. Use the UMD Zaratan
   HPC cluster (``slurm`` job submission) or Google Colab Pro if your local
   machine lacks a GPU. The course GitHub has example SLURM job scripts.

.. tip::

   **Run a fast sanity-check training first.**
   Before committing to 100 epochs, run 5 epochs on a 200-image subset to
   verify that the pipeline works end-to-end (data loads, loss decreases,
   evaluation produces non-zero mAP). Catching pipeline bugs after 1 hour
   of training is much better than after 10 hours.

.. tip::

   **Use message_filters for synchronized camera + detection visualization.**
   If you want to display the annotated image alongside the raw sensor
   stream in RViz2, use ``message_filters.TimeSynchronizer`` to align
   ``/carla/camera/rgb/image`` and ``/perception/annotated_image`` by
   timestamp. This prevents RViz2 from showing mismatched frames.

.. tip::

   **Divide report writing across the team -- do not leave it to one person.**
   Assign: (1) dataset section, (2) YOLO section, (3) DETR section,
   (4) failure analysis. Each member writes their section; one member
   integrates. Starting the report in Week 6 rather than Week 8 avoids
   the most common source of late submissions for this project.
