====================================================
Code
====================================================

The L4 code is in the course Python repository,
`enpm818z-fall-2026-carla-python
<https://github.com/rubixcubic/enpm818z-fall-2026-carla-python>`_, folder
``lecture4/``. It needs no CARLA server: every script runs on images that are
already in the folder.

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: compact-table

   * - **File**
     - **What it is**
   * - ``compare_detectors.py``
     - The L4 live demo: YOLOv8s and RT-DETR-L on the same frames, side by
       side.
   * - ``yolo_one_stage.ipynb``
     - Approach 1, a one-stage CNN detector (YOLOv8s), step by step on the
       slides' photo.
   * - ``rtdetr_set_prediction.ipynb``
     - Approach 2, a set-prediction transformer (RT-DETR-L), step by step.
   * - ``frame.png``, ``frames/frame_00.png`` to ``frame_07.png``
     - CARLA camera frames, 1280 x 720, to run the detectors on.
       ``frame.png`` is the same image as ``frames/frame_06.png``.
   * - ``README.md``
     - Requirements, commands and the expected results.


Requirements
------------

.. code-block:: bash

   pip install ultralytics scipy jupyter

The README says it was tested with ultralytics 8.3.227, torch 2.9 and SciPy
1.16. A GPU is optional. The weights, ``yolov8s.pt`` (22.6 MB) and
``rtdetr-l.pt`` (66.5 MB), are not in the repository: Ultralytics downloads them
into the folder you run from on first use.


``compare_detectors.py``
------------------------

Runs both detectors on the same frames and reports how much they agree. It
does not compute mAP: there is no ground truth here, only the two models
against each other.

.. code-block:: bash

   cd enpm818z-fall-2026-carla-python/lecture4
   python3 compare_detectors.py                   # the slides' photo (bus.jpg)
   python3 compare_detectors.py frame.png         # one CARLA frame
   python3 compare_detectors.py frames/           # every frame in the folder
   python3 compare_detectors.py frames/ --save out/

.. list-table::
   :widths: 25 20 55
   :header-rows: 1
   :class: compact-table

   * - **Argument**
     - **Default**
     - **Meaning**
   * - ``path``
     - Ultralytics' ``bus.jpg``
     - An image or a folder of images.
   * - ``--conf``
     - 0.25
     - The confidence cut, the same for both models.
   * - ``--save``
     - none
     - A folder: write ``<name>_compare.png`` per frame instead of opening a
       window.
   * - ``--list``
     - off
     - List the frames it would run on, and stop.

**What it prints, per frame:** the number of objects and the time in ms for
each model, a table of the count and mean confidence per class, and how many
boxes the two models agree on (IoU of at least 0.5). With more than one frame
it adds a table over all frames, and at the end the median time per model.

**Expected,** from the README, on an RTX 4060 laptop GPU: about 9 ms for
YOLOv8s and 29 ms for RT-DETR-L.


``yolo_one_stage.ipynb``
------------------------

Follows the One-Stage Detectors slides on the same photo.

1. Run YOLOv8s.
2. Open the raw output: an 84 x cells matrix.
3. Decode one cell by hand: the box from the distribution focal loss bins,
   the class scores through a sigmoid.
4. Apply the confidence cut and NMS by hand.
5. Sweep the cut: 0.10, 0.25, 0.50, 0.75.
6. Time it: the median of 50 runs after 10 warm-up runs.

It ends with four exercises.

.. code-block:: bash

   jupyter notebook yolo_one_stage.ipynb


``rtdetr_set_prediction.ipynb``
-------------------------------

Follows the Transformers slides.

1. Run RT-DETR-L.
2. Open the 300 x 84 query matrix.
3. Measure the largest IoU between two boxes of the same class: why no NMS is
   needed.
4. The Hungarian pairing with the slides' numbers (4 queries, 2 objects),
   using ``scipy.optimize.linear_sum_assignment``, against a greedy pairing.
5. Attention by hand, on the slides' example.
6. Side by side with YOLOv8s.

It ends with four exercises.

.. code-block:: bash

   jupyter notebook rtdetr_set_prediction.ipynb
