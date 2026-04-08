====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 3. Exercises cover object detection architectures,
inference benchmarking, and evaluation metrics.


.. dropdown:: Exercise 1 -- YOLO Architecture Analysis
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Develop a deeper understanding of the YOLOv8 detection pipeline by
   reasoning about grid sizes, anchor-free design, and post-processing.


   .. raw:: html

      <hr>


   **Specification**

   Answer the following questions in writing:

   1. YOLOv8 uses a feature pyramid with three detection heads at
      strides 8, 16, and 32. If the input image is ``640 × 640``,
      what is the **grid size** at each stride?
   2. YOLOv8 is an **anchor-free** detector. Explain in 2--3 sentences
      what this means and how it differs from anchor-based detectors
      like YOLOv5.
   3. The model outputs ``(cx, cy, w, h, class_scores)`` per grid cell.
      Why is **Non-Maximum Suppression (NMS)** still needed as a
      post-processing step?
   4. Name **one advantage** and **one disadvantage** of NMS.

   **Deliverable**

   Written answers (one paragraph per question).


.. dropdown:: Exercise 2 -- DETR Object Queries
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Understand how DETR uses learned object queries and bipartite
   matching instead of NMS.


   .. raw:: html

      <hr>


   **Specification**

   Answer the following questions in writing:

   1. DETR uses a fixed set of **100 object queries** that are decoded
      into detections. What happens if a scene contains more than 100
      objects?
   2. DETR uses **bipartite matching** (Hungarian algorithm) during
      training to assign predictions to ground-truth objects. Why is
      this preferred over the anchor/NMS assignment used in YOLO?
   3. What is the computational complexity of the Hungarian algorithm
      in terms of the number of queries :math:`N`?
   4. RT-DETR improves inference speed over the original DETR. Name
      **two specific techniques** it uses to achieve this.

   **Deliverable**

   Written answers (2--4 sentences per question).


.. dropdown:: Exercise 3 -- Inference Speed Benchmark
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Quantitatively compare YOLOv8 and RT-DETR inference performance on
   CARLA data.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``inference_benchmark.py`` that performs the
   following:

   1. Load both ``yolov8s.pt`` and ``rtdetr-l.pt`` using the
      Ultralytics library.
   2. Collect **100 frames** from a CARLA RGB camera (640 × 480).
   3. For each model, run inference on all 100 frames and record:

      - Per-frame inference time (ms)
      - Number of detections per frame (confidence > 0.5)

   4. Print a summary table:

      .. list-table::
         :widths: 30 35 35
         :header-rows: 1
         :class: compact-table

         * - Metric
           - YOLOv8s
           - RT-DETR-L
         * - Mean inference time (ms)
           -
           -
         * - Std inference time (ms)
           -
           -
         * - Mean detections/frame
           -
           -

   **Deliverable**

   The script and a completed results table. Include a 2--3 sentence
   comparison of the two models.


.. dropdown:: Exercise 4 -- Detection Under Adverse Conditions
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Evaluate how weather and lighting conditions impact object detection
   quality.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``weather_detection.py`` that performs the following:

   1. Spawn an ego vehicle with an RGB camera in Town03.
   2. Collect **20 frames** under each of these four conditions:

      - ``ClearNoon``
      - ``HardRainNoon``
      - ``ClearNight``
      - ``SoftFogNoon``

   3. Run YOLOv8s inference on all 80 frames and compute per condition:

      - **Mean confidence** of all detections.
      - **Total detection count**.
      - **False positive estimate** -- detections with no matching
        CARLA ground-truth bounding box within 5 pixels.

   4. Print a results table with one row per condition.

   **Written analysis**

   - Which condition causes the **largest drop** in detection quality?
   - Why does that condition specifically degrade camera-based
     detection?
   - Propose one sensor or algorithmic solution to improve robustness
     in that condition.

   **Deliverable**

   The script, results table, and written analysis (5--8 sentences).


.. dropdown:: Exercise 5 -- mAP Computation by Hand
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Understand the Average Precision metric by computing it manually
   from a small set of detection results.


   .. raw:: html

      <hr>


   **Specification**

   A detector produces the following results on a single image (sorted
   by confidence). Ground truth contains **3 cars**.

   .. list-table::
      :widths: 20 20 30
      :header-rows: 1
      :class: compact-table

      * - Detection
        - Confidence
        - Correct? (IoU > 0.5)
      * - D1
        - 0.95
        - Yes (TP)
      * - D2
        - 0.88
        - Yes (TP)
      * - D3
        - 0.80
        - No (FP)
      * - D4
        - 0.72
        - Yes (TP)
      * - D5
        - 0.60
        - No (FP)

   1. Compute **precision** and **recall** at each detection threshold
      (i.e., after including D1, after D1+D2, after D1+D2+D3, etc.).
      Fill in a table with columns: Detection, TP, FP, Precision,
      Recall.
   2. Sketch the **precision-recall curve** (by hand or using
      matplotlib).
   3. Compute **AP@0.5** using the all-point interpolation method.
   4. If the detector missed one of the three ground-truth cars
      entirely, what is the maximum possible recall?

   **Deliverable**

   Completed precision/recall table, PR curve sketch, and final AP
   value with work shown.
