====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Working
   through this page is good preparation for one. Memorizing the answers
   below is not.

This quiz covers Lecture 4: what perception and object detection are, from
pixels to features, grading a detector (IoU, precision, recall, AP and mAP),
one-stage detectors and NMS, attention and the transformer's encoder and
decoder, DETR and RT-DETR, and detection on the road. Every question can be
answered from the slides shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 22)
===================================

.. admonition:: Question 1
   :class: hint

   What does perception do for the AV?

   A. It steers the AV and controls its speed.

   B. **It turns raw sensor data into a description of the world that the
      rest of the AV can act on: which objects are around, where they are,
      and where the AV may drive.**

   C. It plans the AV's path through an intersection.

   D. It calibrates the sensors before each drive.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Perception sits between the sensors (L2) and prediction and planning. It
   hands four outputs to the rest of the AV: objects, the drivable area,
   lanes and markings, and lights and signs. Objects go to prediction first,
   because the planner needs to know where they will be. The drivable area,
   the lanes and the lights go straight to planning: nothing predicts a red
   light. This lecture covers objects.


.. admonition:: Question 2
   :class: hint

   Which statement describes the output of an object detector, as the
   lecture defines it?

   A. One class label for the whole image, with a score for each class.

   B. One box around the most important object, with no class.

   C. **A set of detections, each a class, a confidence from 0 to 1 and a
      box given by its top-left and bottom-right corners in pixels. The
      number of detections changes from image to image.**

   D. A fixed list of 80 detections, one per COCO class, in a set order.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Each detection is :math:`(c_i, s_i, b_i)`: class, confidence and box
   :math:`(x_0, y_0, x_1, y_1)`. It is a set, so the order means nothing, and
   :math:`N` changes: our image has five objects, an empty road has none.
   **A** is classification and **B** is localization. Detection is both, for
   every object in the image.


.. admonition:: Question 3
   :class: hint

   A classifier trained on ImageNet's 1000 classes labels our image "police
   van" with a score of 0.616. The image shows a city bus. What does the
   0.616 tell you?

   A. That the label is right 61.6 percent of the time

   B. **The share of the total score that went to "police van": its
      confidence, which is not the chance of being right**

   C. That the image is 61.6 percent covered by the van

   D. That 616 of the 1000 classes agree on "police van"

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The model outputs 1000 scores that add up to 1, and the label is the
   class with the highest one. That score is the confidence. Here the answer
   is wrong: ImageNet has no plain bus class, only minibus, school bus and
   trolleybus. The runners-up are minibus 0.374 and ambulance 0.004, and the
   other 997 share :math:`1 - 0.994 = 0.006`. And the classifier says nothing
   about the four people, or about where anything is.


.. admonition:: Question 4
   :class: hint

   A :math:`3 \times 3` window of gray levels sits on the edge of a white
   letter on the bus. Its left column adds to 271.3, its middle column to
   147.4 and its right column to 686.0. The filter has weights :math:`-1` on
   the left, 0 in the middle and :math:`+1` on the right. What is its
   response?

   A. 1104.7

   B. 271.3

   C. **414.7**

   D. :math:`-414.7`

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The response is the sum of the nine products: the right column counts
   with :math:`+1`, the left with :math:`-1`, the middle not at all. So
   :math:`686.0 - 271.3 = 414.7`: the right column is much brighter, a
   vertical edge. On the flat roof the same filter gives :math:`-9.0`, close
   to zero. **A** is the sum of all nine pixels, and **D** would be an edge
   that faces the other way.


.. admonition:: Question 5
   :class: hint

   YOLOv8s scales our :math:`810 \times 1080` image to
   :math:`480 \times 640`. Its first layer slides 32 filters of
   :math:`3 \times 3` over 3 colors, with a stride of 2 and a 1-pixel border
   of zeros. What comes out?

   A. One map of :math:`480 \times 640`

   B. **32 maps, each** :math:`240 \times 320` **features**

   C. 32 maps, each :math:`478 \times 638`

   D. 27 maps, each :math:`240 \times 320`

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Each filter gives one feature map, also called a channel, so 32 filters
   give 32 maps. The stride of 2 moves the filter 2 pixels per step:
   :math:`480/2 = 240` places across and :math:`640/2 = 320` down. The zero
   border lets the window fit on the edge pixels, so nothing is lost there.
   27 is the number of weights in one filter, :math:`3 \times 3 \times 3`.


.. admonition:: Question 6
   :class: hint

   In a detector's backbone, neck and head, what does the **neck** do?

   A. It turns the image into feature maps.

   B. **It mixes the feature maps of different sizes: a coarse map's cells
      respond to whole objects like the bus, a fine map's cells mark exactly
      where its edges are.**

   C. It produces the classes and boxes.

   D. It removes duplicate boxes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   In YOLOv8s, the backbone, a CNN, hands three maps to the neck, at strides
   8, 16 and 32, with 128, 256 and 512 channels. The neck combines them. The
   head turns features into the answer, at every cell: 144 numbers, decoded
   to 84, a box and 80 class scores. Removing duplicates (**D**) is NMS,
   which runs after the network.


.. admonition:: Question 7
   :class: hint

   A ground-truth box runs from :math:`x = 2` to 8 and :math:`y = 2` to 10.
   A detection runs from :math:`x = 3` to 9 and :math:`y = 3` to 11. What is
   their IoU?

   A. 0.729

   B. **0.574**

   C. 0.365

   D. 1.0, because the boxes are the same size

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Each box is :math:`6 \times 8 = 48`. The overlap is
   :math:`5 \times 7 = 35`. The union, the area covered by either box, is
   :math:`48 + 48 - 35 = 61`, so IoU :math:`= 35/61 = 0.574`. **A** is
   :math:`35/48`, which forgets the area of the other box. **C** is
   :math:`35/(48 + 48)`, which counts the overlap twice.


.. admonition:: Question 8
   :class: hint

   Three people are really in an image. A detector gives 5 person boxes;
   3 match a person and 2 match nothing. You accept all 5. What are the
   precision and the recall?

   A. Precision 1.00, recall 0.60

   B. **Precision 0.60, recall 1.00**

   C. Precision 0.67, recall 0.67

   D. Precision 0.60, recall 0.60

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Precision :math:`= TP/(TP + FP) = 3/(3 + 2) = 0.60`: six in ten boxes are
   real people. Recall :math:`= TP/(TP + FN) = 3/(3 + 0) = 1.00`: every
   person is found. Accept only the top 2 (both right) and it flips:
   precision :math:`2/2 = 1.00`, recall :math:`2/3 = 0.67`.


.. admonition:: Question 9
   :class: hint

   One class, person, with 3 people in the ground truth. Five detections,
   sorted by confidence: 0.95 TP, 0.90 TP, 0.80 FP, 0.60 TP, 0.40 FP. What
   is the AP?

   A. 0.600

   B. 0.750

   C. **0.917**

   D. 1.000

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Each person found adds :math:`1/3` of recall, so the area under the step
   line is three strips :math:`1/3` wide. Their heights are the best
   precision at that recall or beyond: 1 (the first box), 1 (the second) and
   0.75 (the fourth, :math:`3/4`). AP :math:`= 0.333 + 0.333 + 0.250 =
   0.917`. **D** would need no false box before the last person is found.
   **A** is the precision of the whole list, 3/5.


.. admonition:: Question 10
   :class: hint

   YOLOv8s scores mAP@0.5:0.95 = 44.9 on COCO. Which description is right?

   A. 44.9 percent of the boxes are right at IoU 0.5.

   B. **The AP of each of COCO's 80 classes, averaged, at each of 10 IoU
      thresholds from 0.50 to 0.95 in steps of 0.05, averaged again: the
      area under the line is 0.449 on average.**

   C. The model finds 44.9 percent of the objects with confidence above
      0.95.

   D. The precision at a confidence cut of 0.25, averaged over 80 classes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   mAP@0.5:0.95 is stricter than mAP@0.5. A box with IoU 0.574, like the one
   on the IoU slide, counts as right only at 0.50 and 0.55: 2 of the 10
   thresholds. Papers write this number simply as "AP". It is computed at a
   confidence cut of 0.001, the Ultralytics validation default, because it
   scores the whole ranked list. Evaluate at 0.25 and your mAP comes out
   lower.


.. admonition:: Question 11
   :class: hint

   What makes YOLO a **one-stage** detector?

   A. It uses a transformer encoder.

   B. **It predicts classes and boxes in one pass, from every cell of its
      feature maps, with no step that first proposes regions.**

   C. It looks at only one object per image.

   D. It needs no clean-up step after the network.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   A two-stage detector, such as Faster R-CNN, first proposes regions that
   may hold an object, then classifies each one. A one-stage detector skips
   the proposals and predicts straight from the grid; "you only look once"
   is named for that. **D** is false for YOLOv8s: it finds each object about
   ten times and needs NMS.


.. admonition:: Question 12
   :class: hint

   On the stride-32 grid, one cell is 54 image pixels on a side. The cell
   in column 2, row 12 (counting from zero) has its center at (135, 675) in
   image pixels, with :math:`y` down. It predicts the distances 85.0 to the
   left, 275.7 up, 111.4 to the right and 227.4 down. What is its box?

   A. (50.0, 902.4) to (246.4, 399.3)

   B. **(50.0, 399.3) to (246.4, 902.4)**

   C. (220.0, 950.7) to (23.6, 447.6)

   D. (85.0, 275.7) to (111.4, 227.4)

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Each distance gives one edge. Left: :math:`135 - 85.0 = 50.0`. Top:
   :math:`675 - 275.7 = 399.3`; :math:`y` grows downward, so up means
   subtract. Right: :math:`135 + 111.4 = 246.4`. Bottom:
   :math:`675 + 227.4 = 902.4`. The four distances come from one run of the
   network, with no search: YOLOv8 predicts boxes with no preset shapes,
   which is why it is called anchor-free.


.. admonition:: Question 13
   :class: hint

   YOLOv8s predicts at :math:`4800 + 1200 + 300 = 6300` cells on our image.
   Above the 0.25 cut, 49 boxes are left for 5 objects. Why about ten per
   object?

   A. Because the image has ten people.

   B. Because each of the three grids predicts every object three times.

   C. **Because training teaches the 10 cells that fit each object best to
      predict it** (``tal_topk=10``), **so on a new image each object comes
      out about ten times.**

   D. Because NMS has already run once.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   The count is 10 boxes on the bus and 9, 9, 11 and 10 on the four people,
   49 in all. The cells come from three grids on the :math:`480 \times 640`
   input: stride 8 gives :math:`60 \times 80 = 4800`, stride 16
   :math:`30 \times 40 = 1200`, stride 32 :math:`15 \times 20 = 300`.
   Something has to keep one box per object, and that is NMS: 49 in, 5 out.


.. admonition:: Question 14
   :class: hint

   NMS deletes a box when its IoU with a kept box is above 0.7. Why does it
   compare only boxes **of the same class**?

   A. To make NMS faster.

   B. **Because a pedestrian stepping out from behind a parked car overlaps
      the car's box, and the car's box, often the more confident one, would
      delete the pedestrian.**

   C. Because boxes of different classes never overlap.

   D. Because the IoU of boxes of different classes cannot be computed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   On an AV, deleting a pedestrian is the worst possible mistake, so NMS
   runs per class. Its weak spot is within one class: two people standing
   close really do overlap. Lower the threshold and one real person is
   deleted; raise it and duplicates survive.


.. admonition:: Question 15
   :class: hint

   To fine-tune YOLO on your own images, each image gets a label file. The
   man's box is centered at (147.2, 651.8) and is :math:`194.6 \times 500.0`
   pixels, in an :math:`810 \times 1080` image. Person is class 0 in COCO's
   list. Which line describes him?

   A. ``0 49.9 401.8 244.5 901.8``

   B. ``person 0.1817 0.6035 0.2402 0.4630``

   C. **Class 0, then 0.1817 0.6035 0.2402 0.4630**

   D. ``0 0.0616 0.3720 0.3019 0.8350``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   One line per object: the class number, then the box center and size,
   each divided by the image's width or height, so every number lies
   between 0 and 1. :math:`147.2/810 = 0.1817`, :math:`651.8/1080 = 0.6035`,
   :math:`194.6/810 = 0.2402`, :math:`500.0/1080 = 0.4630`. **A** gives the
   corners in pixels, **B** the class name instead of its number, and **D**
   the corners divided by the image size.


.. admonition:: Question 16
   :class: hint

   Three tokens, a wheel, a bus window and the sky, have keys (1, 0),
   (0.6, 0.8) and (-0.5, 0.2), with :math:`d = 2`. The wheel's query is
   (1, 0.5). What attention weights does the wheel give the three tokens?

   A. 0.333, 0.333, 0.333

   B. 0.625, 0.625, -0.25

   C. **0.422, 0.422, 0.157**

   D. 0.5, 0.5, 0

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   1. Scores :math:`q \cdot k`: :math:`1 \times 1 + 0.5 \times 0 = 1.0`,
      :math:`1 \times 0.6 + 0.5 \times 0.8 = 1.0` and
      :math:`1 \times (-0.5) + 0.5 \times 0.2 = -0.4`.
   2. Divide by :math:`\sqrt{2} = 1.414`: 0.707, 0.707 and :math:`-0.283`.
   3. Raise :math:`e` to each: 2.028, 2.028 and 0.754, sum 4.810.
   4. Divide by the sum: 0.422, 0.422 and 0.157.

   **B** divides the raw scores by their sum, 1.6, and gives the sky a weight
   below zero. Softmax keeps every weight positive and never exactly zero,
   which rules out **D**.


.. admonition:: Question 17
   :class: hint

   In :math:`\text{softmax}(QK^\top/\sqrt{d})\,V`, what is each part for?

   A. :math:`Q` holds what each token passes on, :math:`V` what it looks
      for.

   B. **Each row of** :math:`QK^\top` **scores one token's query against
      every key; dividing by** :math:`\sqrt{d}` **keeps the scores from
      growing with the vector length; softmax turns them into positive
      weights that add to 1; the weights then average the values.**

   C. :math:`\sqrt{d}` is the number of tokens, so the result is an average
      over tokens.

   D. Softmax picks the single best key and drops all the others.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The query is what a token is looking for, the key what a token can offer,
   and the value what it passes on if chosen. In "The boat reached the
   bank", the query of "bank" asks "water or money?", the key of "boat" says
   "water", and the value of "boat" flows into "bank". All three come from
   matrices set by training. **D** is wrong: softmax gives every token some
   weight.


.. admonition:: Question 18
   :class: hint

   Why does ViT add a learned **position embedding** to every token?

   A. To make the tokens longer.

   B. To mark which token is the class token.

   C. **Because the encoder layers treat the tokens as a set: shuffle them
      and every output is the same, only shuffled. Without position, a patch
      would mean the same at the top of the image as at the bottom.**

   D. To scale the pixel values to 0 to 1.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   ViT-Base learns 197 position vectors, one per token, the class token
   included. In the sentence, "the bank reached the boat" has the same words
   as "the boat reached the bank", and means something else: the position
   embedding is the word order.


.. admonition:: Question 19
   :class: hint

   In training, DETR pairs each object with one query. Costs, chosen for
   the slide: query 1 costs 0.2 for the person and 0.3 for the bus; query 2
   costs 0.3 and 0.9; query 3 costs 0.8 and 0.8; query 4 costs 0.9 and 0.7.
   Which pairing does the Hungarian algorithm choose?

   A. Query 1 for the person and query 4 for the bus, total 0.9

   B. **Query 2 for the person and query 1 for the bus, total 0.6**

   C. Query 1 for both, total 0.5

   D. Query 3 for both objects, because its costs are equal

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   **A** is the greedy pairing: take the cheapest pair first (query 1 and
   the person, 0.2), and the bus is left with query 4 (0.7), total 0.9. That
   used up query 1, which the bus needed. The Hungarian algorithm always
   finds the best total, :math:`0.3 + 0.3 = 0.6`; in Python it is SciPy's
   ``linear_sum_assignment``. **C** and **D** give one query two objects,
   which the pairing forbids. Queries 3 and 4 get no object and learn to
   answer "no object".


.. admonition:: Question 20
   :class: hint

   The original DETR (2020) scored 42.0 mAP on COCO, the same as Faster
   R-CNN with the same backbone, but needed 500 training epochs. What did
   **RT-DETR** change to run in real time?

   A. It added NMS back after the decoder.

   B. It replaced the transformer with a CNN.

   C. **Its encoder runs attention only inside the coarsest map (stride 32),
      and convolutions mix the three map sizes.**

   D. It cut the number of queries to 10.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Attention scores every token against every token, :math:`N^2` pairs, and
   the coarsest map has the fewest cells. RT-DETR-L scores 53.0 mAP at 114
   frames per second on an NVIDIA T4 with TensorRT, :math:`1000/114 = 8.8`
   ms per image. Before it, Deformable DETR let each query attend to a few
   sampling points instead of every cell, and needed 10 times fewer epochs
   than DETR. RT-DETR's decoder has 300 queries and needs no NMS.


.. admonition:: Question 21
   :class: hint

   The GP1 camera runs at 20 Hz. On the lecture's laptop GPU, plugged in,
   RT-DETR-L takes 29.9 ms per image. What share of the time per frame does
   it use?

   A. 15 percent

   B. 30 percent

   C. **60 percent**

   D. 167 percent: it does not fit

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   20 Hz is a new frame every :math:`1000/20 = 50` ms, and
   :math:`29.9/50 = 0.60`. YOLOv8s, at 9.1 ms, uses 18 percent. Both fit,
   but the detector shares the 50 ms with tracking, prediction and
   planning. With six cameras on one GPU, each frame gets
   :math:`50/6 \approx 8` ms, and neither model fits as measured.


.. admonition:: Question 22
   :class: hint

   On our image, at a confidence cut of 0.75, YOLOv8s reports 4 objects and
   RT-DETR-L reports 5. At 0.25, YOLOv8s reports 5 and RT-DETR-L reports 9.
   The image holds 5 real objects. What should you conclude?

   A. RT-DETR-L is better at every cut.

   B. Use 0.75 for both models, because it removes the wrong boxes.

   C. **The same cut means different things for different models: choose it
      per model, on validation data, and for an AV lean low, because a
      missed person costs more than a phantom object.**

   D. The cut does not matter, because mAP is computed at 0.001.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   At 0.75, YOLOv8s misses the person cut off at the left edge, who scored
   0.61. At 0.25, RT-DETR-L adds four wrong objects: a hydrant, a traffic
   light and two ties. At 0.5 both report exactly the five. Validation data
   means labeled images kept out of training; one image does not choose a
   cut. **D** confuses grading with use: on the AV, the cut decides which
   boxes the rest of the software sees.


----


True or False (Questions 23 to 33)
==================================

.. admonition:: Question 23
   :class: hint

   YOLO is a two-stage detector that first proposes regions, then
   classifies them.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   YOLO is one-stage: it predicts classes and boxes in one pass, from every
   cell of its grids. Faster R-CNN is the two-stage example in the lecture:
   it proposes regions first, then classifies each.


.. admonition:: Question 24
   :class: hint

   DETR needs NMS after its decoder to remove duplicate boxes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   In training, the Hungarian matching gives each object to exactly one
   query, so a second query on the same object is paired with nothing and
   learns to answer "no object". The queries also attend to each other in
   the decoder. RT-DETR-L keeps 9 of its 300 rows above 0.25 on our image,
   with no NMS.


.. admonition:: Question 25
   :class: hint

   A confidence of 0.5 from YOLOv8s means the same as a confidence of 0.5
   from RT-DETR-L.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A confidence is a raw class score squeezed into 0 to 1 by a sigmoid,
   :math:`1/(1 + e^{-x})`. It is not the probability of being right, and it
   is not comparable between models: RT-DETR-L gives the same people
   higher numbers than YOLOv8s (the cut-off person: 0.86 against 0.61).


.. admonition:: Question 26
   :class: hint

   Fine-tuning means training a detector from scratch on your own images.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Fine-tuning starts from a network pretrained on a large, general image
   collection and trains it a little more on your own data. Edges and simple
   shapes look much the same in CARLA and in real images, so the early
   layers need little change. It takes far less data and time than training
   from zero. Both of the lecture's detectors start from weights pretrained
   on COCO.


.. admonition:: Question 27
   :class: hint

   Precision is the share of the real objects that the detector found.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   That is recall, :math:`TP/(TP + FN)`. Precision is the share of the boxes
   drawn that are real objects, :math:`TP/(TP + FP)`. Low recall is a missed
   pedestrian; low precision is a phantom one.


.. admonition:: Question 28
   :class: hint

   In one :math:`3 \times 3` convolution layer on the stride-32 grid, the
   man's cell reads every cell of the image, the far end of the bus
   included.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   One :math:`3 \times 3` convolution reads the cell and its 8 neighbors,
   nothing else. Each further layer reaches one cell further on every side:
   2 layers read :math:`5 \times 5` cells, 3 layers :math:`7 \times 7`. One
   attention layer, by contrast, brings all 300 cells of that grid into the
   man's cell.


.. admonition:: Question 29
   :class: hint

   ViT-Base's encoder takes in 197 tokens of 768 numbers and gives back 197
   tokens of 768 numbers, in the same order.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   196 patch tokens plus the class token go in, and the same 197 come out
   after 12 layers. The encoder changes what each token holds, not how many
   there are: a patch's token comes out also describing what surrounds it,
   and the class token comes out holding a summary of the image, from which
   the head reads "minibus".


.. admonition:: Question 30
   :class: hint

   In each encoder layer, a block's input is added back to its output, so
   the block only has to learn a correction to what it received.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   ViT applies a norm before every block and adds the input back after every
   block. Learning only a correction is what lets deep stacks train, the same
   idea as ResNet. The two blocks are multi-head attention, where tokens
   exchange information, and the MLP, which works on each token on its own
   (768 to 3072 to 768).


.. admonition:: Question 31
   :class: hint

   RT-DETR's 300 queries are learned vectors, the same for every image, as
   in the original DETR.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   RT-DETR starts its 300 queries at the 300 cells of the encoder output
   that score highest as objects, so they depend on the image. The original
   DETR used 100 learned vectors.


.. admonition:: Question 32
   :class: hint

   A transformer detector needs less training data than a CNN-only
   detector.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The lecture names more training data as part of the price of a
   transformer, along with time: 29.9 ms for RT-DETR-L against 9.1 ms for
   YOLOv8s on our image. What it buys is context: in one layer, every part
   of the image can change every other part.


.. admonition:: Question 33
   :class: hint

   The same detector on the same laptop takes the same time per image
   whether the laptop is plugged in or on battery.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Plugged in, the whole call took 9.1 ms (YOLOv8s) and 29.9 ms
   (RT-DETR-L). On battery it took 13.3 ms and 42.0 ms:
   :math:`13.3/9.1 = 1.46` and :math:`42.0/29.9 = 1.40`, so 46 and 40
   percent slower. An AV's computer has the same issue with heat and power,
   so measure latency in the conditions you will drive in.


----


Short Answer (Questions 34 to 39)
=================================

.. admonition:: Question 34
   :class: hint

   Compare YOLOv8s and RT-DETR-L on our image and on COCO. Why can you not
   conclude from these numbers alone that "transformers are more accurate
   and slower"?

.. dropdown:: Answer
   :class-container: sd-border-success

   On our image, YOLOv8s reports 5 objects and RT-DETR-L 9: the same five
   real objects, all more confident (lowest person 0.86 against 0.61), plus
   four wrong ones just above the 0.25 cut. YOLOv8s takes 9.1 ms and
   RT-DETR-L 29.9 ms on the laptop GPU. On COCO, RT-DETR-L scores 53.0 mAP
   against 44.9.

   But the two models are not the same size: 33.0 million weights against
   11.2 million. Part of both gaps is size. YOLOv8l, with 43.7 million
   weights, scores 52.9, almost level with RT-DETR-L. When you compare two
   detectors, say whether their sizes match.


.. admonition:: Question 35
   :class: hint

   Explain why YOLO needs NMS and DETR does not. Where does each one's weak
   spot with crowds come from?

.. dropdown:: Answer
   :class-container: sd-border-success

   YOLO's training teaches about 10 cells to predict each object, so on a
   new image each object comes out about ten times (49 boxes for 5 objects).
   NMS keeps the most confident box and deletes same-class boxes whose IoU
   with it is above 0.7. Two real people standing close also overlap, so the
   threshold can delete a real person or keep a duplicate.

   DETR's training pairs each object with exactly one query (the Hungarian
   algorithm), and every other query learns to answer "no object". Its
   queries also attend to each other in the decoder. Duplicates are trained
   away instead of cleaned up, so there is no threshold to get wrong.


.. admonition:: Question 36
   :class: hint

   Describe the backbone, the neck and the head with YOLOv8s's numbers on
   our image, and say how RT-DETR-L's three parts differ.

.. dropdown:: Answer
   :class-container: sd-border-success

   The image is scaled to :math:`480 \times 640`. The **backbone**, a CNN,
   turns it into three feature maps at strides 8, 16 and 32, with 128, 256
   and 512 channels; it is often pretrained on a large image collection. The
   **neck** mixes the map sizes, so the coarse map's sense of a whole bus
   meets the fine map's exact edges. The **head** runs a few small
   convolutions at every cell and outputs 144 numbers per cell, decoded to
   84: a box and 80 class scores, at all 6300 cells.

   RT-DETR-L has the same three parts with a CNN backbone, but its neck adds
   a transformer layer and its head is a transformer decoder with 300
   queries.


.. admonition:: Question 37
   :class: hint

   Both COCO-trained models run on the GP1 CARLA camera frame. YOLOv8s finds
   2 cars at 0.50 and 0.51 and 2 potted plants; RT-DETR-L finds 1 car at
   0.38 and 10 potted plants. Explain this with the domain gap, and say how
   you would shrink the gap.

.. dropdown:: Answer
   :class-container: sd-border-success

   The domain gap is the difference between the images a model was trained
   on and the images it sees in use. COCO is everyday images, where potted
   plants are common, and CARLA's rendered cars look different from real
   ones: the gap here is both simulation to real and everyday images to
   roads. So the cars come out at low confidence and the flower planters look
   like potted plants.

   You see the gap when mAP on your own data falls below the published mAP.
   You shrink it by fine-tuning on data from where you drive. The classes may
   not match either: COCO has no cyclist, only a person and a bicycle.


.. admonition:: Question 38
   :class: hint

   An AV waits at a crosswalk. Its camera sees a bus facing it, two
   pedestrians crossing (the second partly hidden behind the first) and a
   third pedestrian far away. For each of the three, how does a one-stage
   CNN like YOLO handle it, and how does a transformer like RT-DETR?

.. dropdown:: Answer
   :class-container: sd-border-success

   **The bus (large):** in a CNN each cell reads its neighbors, so the far
   end of the bus arrives only after many layers. A transformer links the
   whole image in one layer. When DETR's authors removed its encoder layers,
   it lost 6.0 AP on large objects.

   **The two pedestrians:** YOLO finds each about ten times, and NMS can
   delete the hidden person if the two boxes overlap enough. A transformer
   gives one box per object, with no NMS.

   **The far pedestrian (small):** YOLO has its fine stride-8 grid. The
   original DETR was weaker on small objects; RT-DETR adds feature maps at
   several scales. The price of the transformer is time (29.9 ms against
   9.1 ms on our image) and more training data.


.. admonition:: Question 39
   :class: hint

   Attention is "a weighted average of all the tokens". Explain where the
   weights come from, why they are not fixed like a filter's weights, and
   what the result did for the wheel token in the lecture's example.

.. dropdown:: Answer
   :class-container: sd-border-success

   Each token's vector is multiplied by three matrices, set by training, to
   make a query, a key and a value. A token's query is scored against every
   key (the dot product, divided by :math:`\sqrt{d}`), and softmax turns the
   scores into positive weights that add to 1. The matrices are fixed after
   training, but the weights are computed from the tokens themselves, so
   they change with every image. A filter's weights are the same on every
   image.

   In the example, the wheel gave weights 0.422 to itself, 0.422 to the
   window and 0.157 to the sky. Its value went from (1, 0), "wheel", to
   (0.42, 0.42), "wheel, and part of something with windows": that is how a
   network learns that this wheel belongs to a bus.
