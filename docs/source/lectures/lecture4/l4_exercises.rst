====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises built on the Lecture 4 slides shown in class, and on
the same running example: ``bus.jpg``, the Ultralytics sample image, 810 x
1080 pixels, with a city bus and four people, run through YOLOv8s and
RT-DETR-L. Exercises 1 to 5 are paper and arithmetic: an edge filter, the
grade of a detector, one YOLO cell and NMS, attention, and DETR's matching.
Exercise 6 mixes paper (the time budget, the confidence cut, the domain gap)
with ``compare_detectors.py`` from the course code.

.. note::

   Exercises 1 to 5 can be done with a calculator, but you will learn more by
   writing ten lines of NumPy and checking your arithmetic against it. The
   course code is in the ``lecture4/`` folder of the course Python
   repository (see :doc:`l4_code`). It needs no CARLA server: the frames are
   already in the folder. The two notebooks, ``yolo_one_stage.ipynb`` and
   ``rtdetr_set_prediction.ipynb``, reproduce the numbers used below.

   All pixel coordinates on this page follow the slides: :math:`x` runs right
   and :math:`y` runs down from the top-left corner of the image, and sizes
   are width x height.


.. dropdown:: Exercise 1. From Pixels to an Edge Feature
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compute a filter's response by hand on the lecture's two windows, see
   that a feature names a pattern and a place, and follow the sizes through
   the first layers of YOLOv8s.

   .. raw:: html

      <hr>

   **Part A. The two windows**

   On the slides, two :math:`3 \times 3` windows are picked by eye: one on the
   edge of the white letter "m" on the side of the bus, one on the flat white
   roof. Each number is a pixel's **gray level**, the mean of its red, green
   and blue, from 0 (black) to 255 (white):

   .. code-block:: text

      Letter's edge (yellow)        Flat roof (green)
       65.3   47.0  212.7           195.7  197.7  197.7
      114.0   40.7  237.0           197.7  193.7  189.7
       92.0   59.7  236.3           189.7  188.7  186.7

   1. The middle-left pixel of the edge window has red 73, green 111 and
      blue 158. Check its gray level.
   2. The filter has weights :math:`-1` in its left column, 0 in the middle
      and :math:`+1` on the right. We chose these weights. Compute its
      **response** (the sum of the nine products) on both windows, one
      column at a time.
   3. What are the largest and smallest responses this filter can give on
      any window? Explain from the range of a pixel.
   4. Change the computation to the bottom row minus the top row (a
      horizontal edge). Compute it on both windows. Which kind of edge is
      the letter's edge?
   5. Compute the **brightness**, the mean gray level of the nine pixels, on
      both windows.

   .. raw:: html

      <hr>

   **Part B. Every window**

   6. In Step 5 of the lecture, the filter is centered on each pixel in turn,
      one pixel apart, with no border added. How many responses does the
      810 x 1080 image give? Why is the pixel ring at the border left out?
   7. In the edge map, the long top edge of the bus roof is faint. Explain
      why, from what this filter computes.

   .. raw:: html

      <hr>

   **Part C. Sizes inside YOLOv8s**

   8. YOLOv8s runs at 640 pixels on the long side. Compute the scale factor
      and the input size for our image. Does the library need to add padding,
      given that the network needs sides that are multiples of 32?
   9. The first layer has 32 filters, each :math:`3 \times 3` pixels over 3
      colors, moving 2 pixels per step (a **stride** of 2), with a 1-pixel
      border of zeros. How many weights does one filter have? How many
      features does one of its maps hold?
   10. The backbone hands three maps to the neck, at strides 8, 16 and 32.
       Compute the grid of each map on the :math:`480 \times 640` input, its
       number of cells, and the total. The head predicts a box at every cell.

   .. raw:: html

      <hr>

   **Deliverable**

   The column sums for questions 2 and 4, a table of the three features
   (vertical edge, horizontal edge, brightness) at both windows, and a
   sentence each for questions 3, 6 and 7.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`(73 + 111 + 158)/3 = 342/3 = 114.0`.

      Question 2: at the letter's edge, the right column adds to
      :math:`212.7 + 237.0 + 236.3 = 686.0` and the left column to
      :math:`65.3 + 114.0 + 92.0 = 271.3`, which counts with a minus sign.
      The middle column adds nothing. Response:
      :math:`686.0 - 271.3 = \mathbf{414.7}`. On the flat roof the right
      column adds to :math:`197.7 + 189.7 + 186.7 = 574.1` and the left to
      :math:`195.7 + 197.7 + 189.7 = 583.1`. Response:
      :math:`574.1 - 583.1 = \mathbf{-9.0}`: the right column is 9.0 darker,
      which is close to zero.

      Question 3: a pixel is 0 to 255, so a column of three adds to 0 to
      :math:`3 \times 255 = 765`. The largest response is an all-white right
      column next to an all-black left one: :math:`765 - 0 = +765`. Swap them
      and you get :math:`-765`. A large response either way means an edge,
      and its sign says which way the edge faces. Near 0 means none.

      Question 4: at the letter's edge, the bottom row adds to
      :math:`92.0 + 59.7 + 236.3 = 388.0` and the top row to
      :math:`65.3 + 47.0 + 212.7 = 325.0`, so the response is **63.0**,
      small next to 765. On the roof: :math:`565.1 - 591.1 = -26.0`. The
      letter's edge is a vertical edge (414.7), with little change from top
      to bottom.

      Question 5: the nine gray levels at the letter's edge add to 1104.7,
      and :math:`1104.7/9 = 122.7`. On the roof they add to 1737.3, and
      :math:`1737.3/9 = 193.0`. The letter's window is darker, because two of
      its three columns are the dark blue of the bus.

      These three numbers for one window are three **features** for one
      place: a feature always names a pattern and a place. The slide adds a
      fourth, blueness (the mean of blue minus red): 64.3 at the letter and
      :math:`-17.0` on the roof. YOLOv8s's first layer computes 32 features
      at every place, with patterns set by training.

      Question 6: a window centered on a pixel of the outer ring would stick
      out of the image, so that ring gets no response. That leaves
      :math:`808 \times 1078` responses: one per pixel, except the border.
      This sliding of a filter over an image is a **convolution**.

      Question 7: the top edge of the roof runs left to right, so the
      brightness changes from top to bottom, not from left to right. Every
      column of the window then holds about the same numbers, and right
      minus left is close to 0. This filter finds only one direction of edge.
      The bottom-minus-top filter of question 4 finds the other.

      Question 8: the factor is :math:`640/1080 = 0.593`, so the short side
      becomes :math:`810 \times 0.593 = 480`. The input is
      :math:`480 \times 640`. :math:`480 = 15 \times 32` and
      :math:`640 = 20 \times 32`, so no padding is needed.

      Question 9: :math:`3 \times 3 \times 3 = 27` weights per filter. The
      zero border lets the window fit on the edge pixels too, so the map is
      exactly half the input on each side: :math:`480/2 = 240` places across
      and :math:`640/2 = 320` down, :math:`240 \times 320 = 76{,}800`
      features per map, and 32 such maps, one per filter.

      Question 10: divide the input by the stride.

      .. list-table::
         :widths: 20 30 20 30
         :header-rows: 1
         :class: compact-table

         * - **Stride**
           - **Grid**
           - **Cells**
           - **Channels**
         * - 8
           - :math:`480/8 \times 640/8 = 60 \times 80`
           - 4800
           - 128
         * - 16
           - :math:`30 \times 40`
           - 1200
           - 256
         * - 32
           - :math:`15 \times 20`
           - 300
           - 512
         * - **All three**
           -
           - **6300**
           -

      Deeper means a smaller grid and more channels. The fine grid, stride
      8, has small cells for small objects; the coarse one, stride 32, for
      large ones.


.. dropdown:: Exercise 2. Grading a Detector: IoU, Precision, Recall and AP
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Grade detections by hand, from the overlap of two boxes up to the one
   number papers report.

   .. raw:: html

      <hr>

   **Part A. IoU**

   The box corners on the IoU slide are chosen for that example, in pixels.
   The **ground truth** (where the object really is) runs from :math:`x = 2`
   to 8 and :math:`y = 2` to 10. The detection runs from :math:`x = 3` to 9
   and :math:`y = 3` to 11.

   1. Compute each box's area, the overlap, the **union** (the area covered
      by either box) and the **IoU**. Say in words what the IoU means.
   2. mAP@0.5:0.95 counts a detection as right at 10 IoU thresholds, 0.50,
      0.55, up to 0.95, one at a time. At how many of them is this detection
      right?
   3. A separate example, chosen for this exercise: two boxes, each
      :math:`10 \times 10`, overlap in a :math:`5 \times 10` strip. What is
      their IoU? Is the detection right at the usual threshold of 0.5?

   .. raw:: html

      <hr>

   **Part B. Precision and recall**

   The slides' example, chosen for it: one class, person. **3 people** are in
   the ground truth, and the detector gives 5 person boxes. Sorted by
   confidence:

   .. list-table::
      :widths: 25 25 50
      :header-rows: 1
      :class: compact-table

      * - **Box**
        - **Confidence**
        - **Right?** (IoU at least 0.5)
      * - 1
        - 0.95
        - true positive (TP)
      * - 2
        - 0.90
        - TP
      * - 3
        - 0.80
        - false positive (FP)
      * - 4
        - 0.60
        - TP
      * - 5
        - 0.40
        - FP

   4. Walk down the list. After each box, write the TPs and FPs so far, the
      **precision** :math:`TP/(TP + FP)` and the **recall**
      :math:`TP/(TP + FN)`, where FN is the number of people not yet found.
   5. Two separate choices: accept all 5 boxes, or accept only the top 2.
      Give the precision and recall of each, and say what each pair means for
      an AV: which one risks a missed pedestrian, and which one a hard brake
      for nothing?
   6. A separate run, chosen for this exercise: a detector finds all 3 people
      but also draws 3 boxes on empty road. Precision? Recall?

   .. raw:: html

      <hr>

   **Part C. AP and mAP**

   7. Plot the five (recall, precision) points of question 4. Draw the step
      line that keeps, at each recall, the best precision at that recall or
      beyond. Compute **AP**, the area under it.
   8. A separate run on the same five boxes: suppose box 3 (0.80) had been
      right and box 4 (0.60) wrong. Compute the AP again. What does an AP of
      1 tell you?
   9. If no box at all had matched the third person, what is the highest
      recall the detector could reach, at any cut?
   10. YOLOv8s scores **mAP@0.5:0.95 = 44.9** on COCO's validation images.
       Explain the two averages behind that number. Then explain why the
       published number is computed at a confidence cut of 0.001, and what
       happens to your mAP if you evaluate at 0.25.

   .. raw:: html

      <hr>

   **Deliverable**

   The IoU arithmetic, the table of question 4, the precision-recall plot
   with the step line, both AP values, and two or three sentences for
   question 10.

   .. dropdown:: Guidance
      :color: success

      Question 1: each box is :math:`6 \times 8 = 48`. The overlap runs from
      3 to 8 across and 3 to 10 down: :math:`5 \times 7 = 35`. The union is
      :math:`48 + 48 - 35 = 61`: adding the two areas counts the overlap
      twice, so it is subtracted once. IoU :math:`= 35/61 = \mathbf{0.574}`:
      57 percent of the area the two boxes cover is covered by both. IoU is 1
      for the same box and 0 for boxes that do not touch.

      Question 2: :math:`0.574 \ge 0.50` and :math:`0.574 \ge 0.55`, but
      :math:`0.574 < 0.60`. It is right at **2 of the 10** thresholds. That
      is why mAP@0.5:0.95 rewards boxes that fit tightly, and why it comes
      out lower than mAP@0.5.

      Question 3: overlap :math:`5 \times 10 = 50`; union
      :math:`100 + 100 - 50 = 150`; IoU :math:`= 50/150 = 0.333`. It is below
      0.5, so the detection is wrong at the usual threshold, even though half
      of each box is shared.

      Question 4:

      .. list-table::
         :widths: 16 16 16 26 26
         :header-rows: 1
         :class: compact-table

         * - **Conf.**
           - **TP so far**
           - **FP so far**
           - **Precision**
           - **Recall**
         * - 0.95
           - 1
           - 0
           - 1/1 = 1.00
           - 1/3 = 0.33
         * - 0.90
           - 2
           - 0
           - 2/2 = 1.00
           - 2/3 = 0.67
         * - 0.80
           - 2
           - 1
           - 2/3 = 0.67
           - 2/3 = 0.67
         * - 0.60
           - 3
           - 1
           - 3/4 = 0.75
           - 3/3 = 1.00
         * - 0.40
           - 3
           - 2
           - 3/5 = 0.60
           - 3/3 = 1.00

      Question 5: all 5 boxes: 3 TP, 2 FP, 0 FN, so precision
      :math:`3/5 = 0.60` and recall :math:`3/3 = 1.00`. Six in ten boxes are
      real people, and every person is found. Top 2 only: 2 TP, 0 FP, 1 FN,
      so precision :math:`2/2 = 1.00` and recall :math:`2/3 = 0.67`. Every
      box is a real person, but 1 person in 3 is missed. Low recall is a
      missed pedestrian, the dangerous case. Low precision is a phantom
      pedestrian, which can mean a hard brake for nothing. Accepting more
      boxes raises recall and lowers precision.

      Question 6: precision :math:`3/(3 + 3) = 0.5`, recall
      :math:`3/(3 + 0) = 1.0`.

      Question 7: each person found adds :math:`1/3` of recall, so the area
      is three strips, each :math:`1/3` wide. The best precision at recall
      :math:`1/3` or beyond is 1; at :math:`2/3` or beyond, still 1 (the
      second box); at 1, it is 0.75 (the fourth box). AP
      :math:`= 0.333 + 0.333 + 0.250 = \mathbf{0.917}`. Read it as: while
      finding all 3 people, on average 91.7 percent of the boxes accepted
      were right.

      Question 8: the order is now TP, TP, TP, FP, FP. Precision is 1.00 at
      recall 0.33, 0.67 and 1.00, so the three strips all have height 1 and
      AP :math:`= 1.0`. An AP of 1 means no false box comes before the last
      person is found. The two false boxes now rank below every real one, so
      they cost nothing.

      Question 9: :math:`2/3 = 0.67`. A person that no box matches is a false
      negative at every cut, so recall never reaches 1.

      Question 10: first, AP is computed one class at a time, and COCO's 80
      APs are averaged into one mean AP. Second, that is repeated at the 10
      IoU thresholds, 0.50 to 0.95, and averaged again. 44.9 means the area
      under the line, averaged over 80 classes and 10 thresholds, is 0.449;
      papers write it as "AP". The cut is 0.001, the Ultralytics validation
      default, because mAP scores the whole ranked list, down to the least
      sure box. At 0.25, the default for drawing boxes, you throw away the
      bottom of the list, and your mAP comes out lower than the published
      number.


.. dropdown:: Exercise 3. YOLO: One Cell's Box, the Duplicates and NMS
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Decode a box from one grid cell by hand, see why each person comes out
   about ten times, and run NMS on two of those boxes.

   .. raw:: html

      <hr>

   **Part A. A box from one cell**

   At stride 32, YOLOv8s's grid has :math:`480/32 = 15` cells across and
   :math:`640/32 = 20` down. On the 810-pixel-wide image, one cell is
   :math:`810/15 = 54` image pixels on a side. Each cell predicts 80 class
   scores, one per COCO class, and a box written as four distances from the
   cell's center. Cells are counted from zero.

   1. Compute the center of the cell in column 2, row 12, in image pixels.
   2. That cell scores person 0.86. Its four distances are 85.0 to the left,
      275.7 up, 111.4 to the right and 227.4 down. Compute the box's four
      edges, its width and its height. Remember that :math:`y` grows
      downward.
   3. The cell diagonally below, column 3, row 13, scores person 0.887. Its
      distances are 139.1 to the left, 327.2 up, 55.5 to the right and 172.8
      down. Compute its center, its four edges and its size. Compare with the
      box on the Grading a Detector divider slide:
      ``person 0.89 (49.9, 401.8) to (244.5, 901.8)``.
   4. Both cells give their boxes from the same single run of the network.
      Does the detector start at a cell's center and search around it to grow
      the box? What does the cell (3, 13) read to draw a box 195 pixels wide
      from a 54-pixel cell?

   .. raw:: html

      <hr>

   **Part B. Duplicates and NMS**

   5. Above the 0.25 cut, YOLOv8s keeps 49 boxes on our image: 10 on the bus
      and 9, 9, 11 and 10 on the four people. Check the total. Why does each
      object come out about ten times?
   6. NMS: sort by confidence, keep the top box, delete every box of the same
      class whose IoU with it is above 0.7 (the Ultralytics default), and
      repeat. Compute the IoU between the boxes of questions 2 and 3. Which
      of the two survives?
   7. Why does NMS compare only boxes of the same class? Use a pedestrian
      stepping out from behind a parked car.
   8. Two people stand close together, and their boxes overlap. What goes
      wrong if you lower the NMS threshold? If you raise it?

   .. raw:: html

      <hr>

   **Part C. A label line for training**

   9. To fine-tune YOLO on your own images, each image gets a text file with
      one line per object: the class number, then the box center and size,
      divided by the image's width and height. Person is class 0 in COCO's
      list. Write the line for the man's box of question 3.

   .. raw:: html

      <hr>

   **Deliverable**

   Both boxes with their arithmetic, the IoU of question 6, the label line,
   and a sentence each for questions 4, 5, 7 and 8.

   .. dropdown:: Guidance
      :color: success

      Question 1: the center is half a cell in from the cell's corner:
      :math:`x = 2.5 \times 54 = 135` and :math:`y = 12.5 \times 54 = 675`.

      Question 2:

      1. Left edge: :math:`135 - 85.0 = 50.0`.
      2. Top edge: :math:`675 - 275.7 = 399.3` (up means subtract, since
         :math:`y` grows downward).
      3. Right edge: :math:`135 + 111.4 = 246.4`.
      4. Bottom edge: :math:`675 + 227.4 = 902.4`.

      Width :math:`85.0 + 111.4 = 196.4`, height
      :math:`275.7 + 227.4 = 503.1`.

      Question 3: center :math:`(3.5 \times 54,\ 13.5 \times 54) = (189, 729)`.

      1. Left: :math:`189 - 139.1 = 49.9`.
      2. Top: :math:`729 - 327.2 = 401.8`.
      3. Right: :math:`189 + 55.5 = 244.5`.
      4. Bottom: :math:`729 + 172.8 = 901.8`.

      Size :math:`139.1 + 55.5 = 194.6` wide and
      :math:`327.2 + 172.8 = 500.0` tall. This is the box on the divider
      slide, where 0.887 is rounded to 0.89: the man in the light-colored
      jacket.

      Question 4: no search. One run gives every cell its 80 scores and 4
      distances at once, and no cell waits for another. Cell (3, 13) reads
      far beyond its own 54 pixels: measured with the gradient, only 1.5
      percent of what moves its person score comes from inside its cell, and
      48.6 percent from inside the man's box. The rest comes from around him.

      Question 5: :math:`10 + 9 + 9 + 11 + 10 = 49`. During training, the
      library picks the 10 cells whose boxes fit each object best and teaches
      all 10 to predict that object (the setting ``tal_topk=10``). So on a
      new image each object comes out about ten times.

      Question 6: the overlap runs from :math:`x = 50.0` to 244.5 (194.5
      wide) and from :math:`y = 401.8` to 901.8 (500.0 tall):
      :math:`194.5 \times 500.0 = 97{,}250`. The areas are
      :math:`196.4 \times 503.1 = 98{,}808.8` and
      :math:`194.6 \times 500.0 = 97{,}300`. Union:
      :math:`98{,}808.8 + 97{,}300 - 97{,}250 = 98{,}858.8`. IoU
      :math:`= 97{,}250 / 98{,}858.8 = 0.984`. That is above 0.7, so the two
      boxes are duplicates. NMS keeps the more confident one, cell (3, 13) at
      0.887, and deletes the 0.86 box. On the whole image, 49 boxes go in and
      5 come out.

      Question 7: the pedestrian's box and the parked car's box overlap a
      lot. If NMS compared across classes, the car's box, often the more
      confident one, would delete the pedestrian. On an AV that is the worst
      possible mistake, so NMS runs per class.

      Question 8: lower the threshold and NMS deletes one of the two real
      people, because their real overlap now counts as a duplicate. Raise it
      and duplicates of the same person survive. No setting is right for
      every scene. The transformer detector of Exercise 5 needs no NMS at
      all.

      Question 9: center :math:`((49.9 + 244.5)/2,\ (401.8 + 901.8)/2) =
      (147.2,\ 651.8)`, size :math:`194.6 \times 500.0`, in an
      :math:`810 \times 1080` image:

      .. code-block:: text

         0 0.1817 0.6035 0.2402 0.4630    # class cx cy w h

      from :math:`147.2/810 = 0.1817`, :math:`651.8/1080 = 0.6035`,
      :math:`194.6/810 = 0.2402` and :math:`500.0/1080 = 0.4630`.


.. dropdown:: Exercise 4. Attention by Hand, and the Sizes Inside a ViT
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run the attention formula by hand on three tokens, and count what goes
   into and out of the Vision Transformer (ViT-Base) on our image.

   .. raw:: html

      <hr>

   **Part A. Attention for three tokens**

   .. math::

      \text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d}}\right) V

   The slides' example, with every number chosen for it: three patch tokens,
   a wheel, a bus window and the sky, with vectors of length :math:`d = 2`.
   The queries, keys and values are picked directly, instead of being
   computed with trained matrices. Values are written as (wheel-ness,
   window-ness).

   .. list-table::
      :widths: 25 25 25 25
      :header-rows: 1
      :class: compact-table

      * - **Token**
        - **Query** :math:`q`
        - **Key** :math:`k`
        - **Value** :math:`v`
      * - wheel
        - (1, 0.5)
        - (1, 0)
        - (1, 0)
      * - window
        - (0.5, 1)
        - (0.6, 0.8)
        - (0, 1)
      * - sky
        - (-2, 0)
        - (-0.5, 0.2)
        - (0, 0)

   1. For the wheel's query, compute the score :math:`q \cdot k` against all
      three keys, divide by :math:`\sqrt{2}`, raise :math:`e` to each result,
      and divide by their sum. Then compute the wheel's new value, the
      weighted sum of the three values. What does the new value say about
      the wheel?
   2. Why raise :math:`e` to the scores before dividing by their sum? Divide
      the wheel's raw scores by their sum instead, and look at the sky's
      weight.
   3. Repeat question 1 for the sky's query. Why does the sky still get some
      weight from the wheel and the window?
   4. Stack the three rows of weights (the window's are 0.312, 0.477 and
      0.211). What shape is the result, what does each row add up to, and
      which part of the formula is it?

   .. raw:: html

      <hr>

   **Part B. Counting inside ViT-Base**

   ViT-Base squeezes the image to :math:`224 \times 224` pixels, cuts it into
   :math:`16 \times 16` patches, and uses vectors of :math:`D = 768` numbers.

   5. How many patches are there, and how many numbers does each patch hold?
   6. The embedding multiplies each patch's line of pixel values by a learned
      matrix :math:`E` of size :math:`768 \times D`. How many weights does
      :math:`E` hold? Does each patch get its own :math:`E`?
   7. One class token is put in front, and a learned position vector is
      added to every token. How many tokens go into the encoder, how many
      position vectors are learned, and how many tokens come out after the 12
      encoder layers? Why is the position needed at all?
   8. Feature 1 of our orange patch starts with its first pixel, red 214.
      The network rescales each value with ImageNet's mean (0.485) and spread
      (0.229) for red. Compute the rescaled value. The 768 products then add
      to :math:`-0.282`, and the layer's learned offset is 0.022. What is
      feature 1?
   9. Attention scores every token against every token, so :math:`N` tokens
      make :math:`N^2` pairs. Compute the pairs for the 196 ViT patches, for
      the 300 cells of our image's stride-32 map and for the 1200 cells of its
      stride-16 map. What happens to the pairs if you halve the patch size?

   .. raw:: html

      <hr>

   **Deliverable**

   The score, weight and value table for the wheel and for the sky, the
   counts of Part B, and a sentence each for questions 2, 3 and 9.

   .. dropdown:: Guidance
      :color: success

      Question 1: the scores multiply the two first numbers, multiply the two
      second numbers, and add.

      .. list-table::
         :widths: 16 22 18 14 14
         :header-rows: 1
         :class: compact-table

         * - **Key of**
           - :math:`q \cdot k`
           - :math:`\div \sqrt{2}`
           - :math:`e^x`
           - **Weight**
         * - wheel
           - :math:`1 \times 1 + 0.5 \times 0 = 1.0`
           - 0.707
           - 2.028
           - 0.422
         * - window
           - :math:`1 \times 0.6 + 0.5 \times 0.8 = 1.0`
           - 0.707
           - 2.028
           - 0.422
         * - sky
           - :math:`1 \times (-0.5) + 0.5 \times 0.2 = -0.4`
           - :math:`-0.283`
           - 0.754
           - 0.157

      The sum is :math:`2.028 + 2.028 + 0.754 = 4.810`, so
      :math:`2.028/4.810 = 0.422` and :math:`0.754/4.810 = 0.157`. The weights
      add to 1, up to rounding. New value:
      :math:`0.422\,(1, 0) + 0.422\,(0, 1) + 0.157\,(0, 0) = (0.42, 0.42)`.
      The wheel said only "wheel", (1, 0). Now it says "wheel, and part of
      something with windows". That is how a network learns that this wheel
      belongs to a bus.

      Question 2: the raw scores add to :math:`1.0 + 1.0 - 0.4 = 1.6`, and
      the sky's share would be :math:`-0.4/1.6 = -0.25`, below zero. The
      wheel would then take the sky's value away instead of mixing it in.
      :math:`e^x` is positive for every :math:`x`, and a higher score still
      gives a larger number. Raising :math:`e` and dividing by the sum
      together are the **softmax**.

      Question 3: scores :math:`-2 \times 1 + 0 = -2` (wheel),
      :math:`-2 \times 0.6 + 0 = -1.2` (window) and
      :math:`-2 \times (-0.5) + 0 = 1.0` (sky). Divided by 1.414:
      :math:`-1.414`, :math:`-0.849` and 0.707. Raised: 0.243, 0.428 and
      2.028, sum 2.699. Weights: **0.090, 0.159 and 0.751**. New value:
      :math:`0.090\,(1, 0) + 0.159\,(0, 1) = (0.09, 0.16)`. The sky keeps most
      of its weight on itself and stays close to (0, 0). It still takes a
      little from the bus, because softmax never gives exactly zero.

      Question 4: a :math:`3 \times 3` matrix, one row per query (wheel,
      window, sky) and one column per key. Each row adds to 1. It is
      :math:`\text{softmax}(QK^\top/\sqrt{d})`; the network computes all rows
      at once, then multiplies by :math:`V`.

      Question 5: :math:`224/16 = 14` patches across and 14 down, so
      :math:`14 \times 14 = 196` patches. 16 divides 224 exactly, so no pixel
      is left over. Each patch holds :math:`16 \times 16 \times 3 = 768`
      numbers.

      Question 6: :math:`768 \times 768 = 589{,}824` weights, set by training.
      The same :math:`E` serves all 196 patches.

      Question 7: :math:`196 + 1 = 197` tokens go in, 197 position vectors are
      learned (the class token gets one too), and 197 tokens come out, in the
      same order: the encoder changes what each token holds, not how many
      there are. Without position, the encoder treats the tokens as a set:
      shuffle them and every output is the same, only shuffled. A patch would
      mean the same at the top of the image as at the bottom.

      Question 8: :math:`(214/255 - 0.485)/0.229 = (0.8392 - 0.485)/0.229 =
      0.3542/0.229 = 1.547`. Feature 1 is :math:`-0.282 + 0.022 = -0.26`, the second number
      of our patch's token (the code counts from zero).

      Question 9: :math:`196^2 = 38{,}416`, :math:`300^2 = 90{,}000` and
      :math:`1200^2 = 1{,}440{,}000` pairs, for every layer and every image.
      Halving the patch size gives 4 times the tokens and
      :math:`4^2 = 16` times the pairs. That is why detection transformers
      attend over the coarse map, or let each query look at only a few chosen
      points.


.. dropdown:: Exercise 5. DETR and RT-DETR: One Query per Object
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Pair queries with objects by hand, see why that pairing removes the need
   for NMS, and follow our image through RT-DETR-L.

   .. raw:: html

      <hr>

   **Part A. The Hungarian algorithm**

   A DETR-style detector makes many guesses, called **object queries**. In
   training, each object is paired with exactly one query, which learns to
   find it. The slides' example, chosen for it: 4 queries, 2 objects. Each
   cell is a **cost**, how bad that query is as an answer for that object
   (low means the right class and a box in the right place).

   .. list-table::
      :widths: 34 33 33
      :header-rows: 1
      :class: compact-table

      * - **Cost**
        - **person**
        - **bus**
      * - query 1
        - 0.2
        - 0.3
      * - query 2
        - 0.3
        - 0.9
      * - query 3
        - 0.8
        - 0.8
      * - query 4
        - 0.9
        - 0.7

   1. Pair greedily: take the cheapest pair first, then the cheapest pair
      left. What is the total cost?
   2. List every way to give the person one query and the bus a different
      one. How many are there, and which has the lowest total?
   3. Check your answer with SciPy:

      .. code-block:: python

         import numpy as np
         from scipy.optimize import linear_sum_assignment

         cost = np.array([[0.2, 0.3],
                          [0.3, 0.9],
                          [0.8, 0.8],
                          [0.9, 0.7]])
         rows, cols = linear_sum_assignment(cost)
         print(rows, cols, cost[rows, cols].sum())

   4. Queries 3 and 4 get no object. What does training teach them? Explain
      why this pairing means DETR needs no NMS, and give the second reason
      the lecture names.

   .. raw:: html

      <hr>

   **Part B. Our image through RT-DETR-L**

   5. RT-DETR-L resizes the image to :math:`640 \times 640`. Its CNN backbone
      ends at stride 32. How many cells does that map have? A
      :math:`1 \times 1` convolution shrinks each cell to 256 numbers, and
      the cells become tokens for one encoder layer. How many tokens?
   6. After the encoder, convolutions mix the stride-32 map with the
      stride-8 and stride-16 maps. Compute the total number of cells of 256
      numbers.
   7. RT-DETR starts its 300 queries at the 300 cells that score highest as
      objects. Each of its 6 decoder layers reads the encoder output at
      8 heads x 3 map sizes x 4 points per query. How many points is that,
      against how many cells?
   8. RT-DETR-L's output is one :math:`300 \times 84` matrix. What are the
      300 rows and the 84 columns? Query 1's box center is at
      :math:`c_x = 0.913` as a fraction of the image width: how many pixels
      from the left of our 810-pixel-wide image? At most how many objects can
      RT-DETR-L report in one image?

   .. raw:: html

      <hr>

   **Deliverable**

   The greedy total, the list of pairings with the best one, SciPy's output,
   the counts of Part B, and a short paragraph for question 4.

   .. dropdown:: Guidance
      :color: success

      Question 1: query 1 takes the person (0.2). The bus now needs another
      query; the cheapest left is query 4 (0.7). Total
      :math:`0.2 + 0.7 = 0.9`.

      Question 2: :math:`4 \times 3 = 12` pairings.

      .. list-table::
         :widths: 30 70
         :header-rows: 1
         :class: compact-table

         * - **Person gets**
           - **Bus gets, and the total**
         * - query 1 (0.2)
           - query 2: 1.1; query 3: 1.0; query 4: 0.9
         * - query 2 (0.3)
           - **query 1: 0.6**; query 3: 1.1; query 4: 1.0
         * - query 3 (0.8)
           - query 1: 1.1; query 2: 1.7; query 4: 1.5
         * - query 4 (0.9)
           - query 1: 1.2; query 2: 1.8; query 3: 1.7

      The best is query 2 for the person and query 1 for the bus,
      :math:`0.3 + 0.3 = 0.6`. Taking the cheapest pair first used up query
      1, which the bus needed. The **Hungarian algorithm** always finds the
      best total; with 300 queries you do not list every pairing by hand.

      Question 3: it prints ``[0 1] [1 0] 0.6``: row 0 (query 1) gets column
      1 (bus), row 1 (query 2) gets column 0 (person), total 0.6. SciPy
      counts from zero.

      Question 4: they learn to answer "no object", :math:`\varnothing`. Each
      object is given to exactly one query, so a second query that also
      points at the person is paired with nothing, and training pushes it to
      answer no object. Duplicates are trained away instead of cleaned up
      afterwards. The second reason: inside the decoder the queries attend to
      each other (self-attention), so one query can see that another has
      already taken the person. With no NMS, there is no threshold to get
      wrong in a crowd.

      Question 5: :math:`640/32 = 20`, so :math:`20 \times 20 = 400` cells,
      and 400 tokens of 256 numbers.

      Question 6: stride 8 gives :math:`640/8 = 80`, so
      :math:`80 \times 80 = 6400` cells; stride 16 gives
      :math:`40 \times 40 = 1600`; stride 32 gives 400. Total
      :math:`6400 + 1600 + 400 = 8400`.

      Question 7: :math:`8 \times 3 \times 4 = 96` points per query, not all
      8400 cells. Looking at a few sampling points instead of every cell is
      the idea of Deformable DETR.

      Question 8: one row per query, 300. The 84 columns are the box (center
      :math:`c_x, c_y` and size :math:`w, h`, as fractions of the image) and
      80 sigmoid scores, one per COCO class. There is no "no object" column:
      a query whose 80 scores are all low found nothing.
      :math:`0.913 \times 810 = 739.5` pixels from the left: the person at the
      right edge, with a person score of 0.949. With 300 queries, RT-DETR-L
      can report at most 300 objects; the original DETR, with
      :math:`N = 100`, at most 100. On our image, 9 rows score above 0.25,
      and that is the final answer, with no NMS.


.. dropdown:: Exercise 6. Detection on the Road
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Decide whether a detector fits an AV's time budget, choose a confidence
   cut, and see the domain gap on CARLA frames with the course code.

   .. raw:: html

      <hr>

   **Part A. The time budget**

   The GP1 camera runs at 20 Hz (``sensor_tick`` 0.05 s). Measured on the
   lecture's laptop GPU (RTX 4060), plugged in, with plain PyTorch, median of
   50 runs after 10 warm-up runs, from image file in to boxes out: YOLOv8s
   takes **9.1 ms** and RT-DETR-L **29.9 ms**.

   1. How long is one frame? What share of it does each model take? Who else
      needs part of that time?
   2. Six cameras share one GPU. How much time does each frame get? Do the
      two models fit, as measured? What does the lecture suggest instead?
   3. On battery, the same laptop measured:

      .. list-table::
         :widths: 22 18 18 18 24
         :header-rows: 1
         :class: compact-table

         * -
           - **Step 1** (preprocess)
           - **Step 2** (network)
           - **Step 3** (postprocess)
           - **Whole call**
         * - YOLOv8s
           - 1.8 ms
           - 4.8 ms
           - 2.0 ms
           - 13.3 ms
         * - RT-DETR-L
           - 2.4 ms
           - 34.4 ms
           - 0.5 ms
           - 42.0 ms

      Add the three steps for each model and compare with the whole call.
      Why is RT-DETR-L's Step 3 so short? How much slower is each whole call
      than when plugged in?
   4. Ultralytics quotes RT-DETR-L at 114 frames per second on an NVIDIA T4
      with TensorRT. Convert that to milliseconds per image. Can you compare
      it directly with the 29.9 ms above?

   .. raw:: html

      <hr>

   **Part B. The confidence cut**

   Objects reported on our image, which holds five real objects (the bus
   and four people), at four cuts (measured):

   .. list-table::
      :widths: 20 35 45
      :header-rows: 1
      :class: compact-table

      * - **Cut**
        - **YOLOv8s**
        - **RT-DETR-L**
      * - 0.10
        - 7: a second bus, a tie
        - 41: 14 potted plants, 8 handbags, ...
      * - 0.25 (default)
        - 5
        - 9: a hydrant, a light, 2 ties
      * - 0.50
        - 5
        - 5
      * - 0.75
        - 4: misses a person
        - 5

   5. At which cuts does each model report a wrong object, and at which does
      it miss a real one? The person YOLOv8s misses at 0.75 scored 0.61.
   6. Is 0.5 the right cut for both models on an AV? Say how you would choose
      the cut, and which mistake you would rather make.

   .. raw:: html

      <hr>

   **Part C. The domain gap**

   7. Name the five sources of **domain gap** listed in the lecture. Which of
      them does a COCO-trained model meet on a CARLA frame?
   8. On the GP1 CARLA camera frame, YOLOv8s reports 2 cars at 0.50 and 0.51
      and 2 potted plants; RT-DETR-L reports 1 car at 0.38 and 10 potted
      plants. Explain these results. Your AV needs five classes: vehicle,
      pedestrian, cyclist, traffic light and stop sign. Why is a COCO model
      not enough even without the gap?

   .. raw:: html

      <hr>

   **Part D. Run both detectors**

   .. code-block:: bash

      cd enpm818z-fall-2026-carla-python/lecture4
      python3 compare_detectors.py frames/                  # every frame in the folder
      python3 compare_detectors.py frames/ --conf 0.5       # a different cut
      python3 compare_detectors.py frames/ --save out/      # no desktop? write PNGs

   9. For each model, at the default cut of 0.25, record the objects found
      per frame, the wrong boxes above the cut, the people missed, and the
      median time per frame. Which wrong boxes lower precision, and which
      misses lower recall?
   10. Rerun at ``--conf 0.5``. What changes for each model?
   11. Weather: for rain, night and fog, say what changes in the image and
       what failure to look for. How would you report a detector's results
       across the four conditions, clear included?

   .. raw:: html

      <hr>

   **Deliverable**

   The arithmetic of Part A, a recommended cut per model with one sentence of
   reasoning, the table of Part D for both cuts, and a short paragraph each
   for Parts C and D.

   .. dropdown:: Guidance
      :color: success

      Question 1: :math:`1000/20 = 50` ms per frame. YOLOv8s takes
      :math:`9.1/50 = 18` percent of it and RT-DETR-L
      :math:`29.9/50 = 60` percent. Tracking, prediction and planning share
      the same computer and the same 50 ms. If the detector takes longer,
      frames queue up and the AV reacts to old images.

      Question 2: :math:`50/6 = 8.3` ms per frame, about 8 ms. Neither fits
      as measured: 9.1 ms and 29.9 ms are both above 8.3 ms. The lecture
      suggests a small one-stage model exported to TensorRT, NVIDIA's
      speed-up library: Ultralytics reports 1.7 ms for YOLO26n on a T4.

      Question 3: YOLOv8s's steps add to :math:`1.8 + 4.8 + 2.0 = 8.6` ms,
      against 13.3 ms for the whole call; RT-DETR-L's add to
      :math:`2.4 + 34.4 + 0.5 = 37.3` ms, against 42.0 ms. Reading the image
      file and Python's own overhead take the rest. RT-DETR-L's Step 3 is
      short because it has no NMS; YOLOv8s's 2.0 ms is mostly NMS. On
      battery, the whole call is :math:`13.3/9.1 = 1.46` and
      :math:`42.0/29.9 = 1.40` times as long: 46 and 40 percent slower, with
      the same models on the same hardware. Measure latency in the conditions
      you will drive in.

      Question 4: :math:`1000/114 = 8.8` ms per image. It is not comparable
      with 29.9 ms: that number is a T4 GPU with TensorRT, ours is plain
      PyTorch on a laptop GPU. When you report a latency, say the GPU, the
      software, the input size, how many runs, and what the time covers.

      Question 5: YOLOv8s reports wrong objects only at 0.10 (a second bus
      box and a tie) and misses the cut-off person at 0.75. RT-DETR-L reports
      wrong objects at 0.10 (41 objects) and 0.25 (the hydrant, the traffic
      light and two ties) and still has all five real objects at 0.75.

      Question 6: no. On this image 0.5 gives exactly the five objects for
      both models, but one image does not choose a cut. The same cut means
      different things for different models: RT-DETR's wrong boxes are gone
      by 0.5, and YOLO loses a real person at 0.75. Choose the cut per model,
      on validation data, which means labeled images kept out of training.
      For an AV, lean low: a missed person costs far more than a phantom
      handbag, which the tracker can throw away later.

      Question 7: simulation to real, everyday images to roads, weather and
      light, place (signs, lane markings and vehicles of another country),
      and the sensor (lens, resolution, mounting height). A COCO model on a
      CARLA frame meets at least the first two: CARLA's rendered cars are not
      real cars, and COCO is everyday images, not an AV's camera view.

      Question 8: COCO is full of everyday scenes where potted plants are
      common, and CARLA's rendered cars look different from the real cars in
      COCO, so the cars come out at low confidence and the flower planters
      look like potted plants. The domain gap shows as worse results than the
      published mAP. The classes do not match either: COCO has no cyclist,
      only a person and a bicycle, and most of its 80 classes are of no use
      to the AV. Both reasons are why you collect your own data and
      fine-tune.

      Question 9: measure it; the numbers depend on your frames and your GPU.
      Wrong boxes above the cut are false positives and lower precision.
      Missed people are false negatives and lower recall. Compare your median
      times with the lecture's 9.1 ms and 29.9 ms, and say on what hardware
      you measured.

      Question 10: expect fewer wrong boxes for both models, and look for a
      real object that drops below 0.5. That is the trade-off of Part B: a
      higher cut raises precision and can lower recall.

      Question 11: rain puts drops on the lens and reflections on the road:
      look for phantom objects in the reflections. Night lowers the contrast
      and adds headlight glare: look for missed pedestrians in dark clothes.
      Fog fades far objects: look for recall that drops with distance. Report
      mAP per condition, because an average over all four can hide a
      detector that fails completely at night, and show images of the
      failures, not just the numbers.
