====================================================
Grading a Detector and a Tracker
====================================================

.. admonition:: Read this before GP2, Task 3
   :class: important

   This page is **pre-read material** for :doc:`GP2 </assignments/gp2>`.
   L4 introduced IoU, precision, recall and AP; this page takes them one
   step at a time, with figures and worked examples, and adds the scores
   GP2 uses for tracking.

This page explains, step by step, every score GP2 asks you to compute. Every number here comes from our **demo drive**: the same
recorder and the same traffic as yours, but with the GP1 starter's
placeholder rig (camera 1.5 m forward, 1.6 m up, no pitch, 1280 x 720,
90 deg). No team has that rig, so these numbers are not anyone's answers.

Why GP2 Needs Its Own Test
--------------------------

Both models come with published scores. Those scores were measured on
COCO, a set of photos: different cameras, different streets, daylight
mostly, and objects of every size. They do not say how a model does on
**your** camera, at **your** height and pitch, on CARLA's streets, at night.

To get that number you need three things:

1. **Images from your camera.** The recorder saves them.
2. **The right answer for every image:** where each car and each person
   really is. This is the **ground truth**. Task 1 builds it.
3. **A rule that compares the detector's boxes with the ground truth** and
   turns the result into one number. Task 3 builds it.

The rest of this page is about steps 2 and 3.


Ground Truth from the Simulator
-------------------------------

In a real drive, people draw the ground-truth boxes by hand. CARLA does not
need them: it knows every actor's 3D box. Task 1 turns those 3D boxes into
the 2D boxes a perfect detector would draw.

**Step 1: project the 8 corners.** For each corner :math:`P` (world frame,
CARLA axes), the camera's pose gives the point in the camera's optical frame,
and :math:`K` gives the pixel, as in L2 and GP1:

.. math::

   \begin{bmatrix} x \\ y \\ z \end{bmatrix} = R\,P + t, \qquad
   u = f\,\frac{x}{z} + c_u, \qquad v = f\,\frac{y}{z} + c_v

Here :math:`z` is the depth along the optical axis (forward), :math:`x`
points right and :math:`y` down, :math:`f` is the focal length in pixels and
:math:`(c_u, c_v)` the image center. The box around the 8 projected
corners says where the actor can be.

**Step 2: keep only the pixels that show the actor.** The projected box is
loose. A 3D box seen at an angle covers road and sky around the car. Inside
that loose box, a pixel belongs to the actor when:

- its **semantic tag** is the actor's class (CARLA tags cars 14, trucks 15,
  buses 16, pedestrians 12), and
- its **depth** lies within the actor's own depth range, from its nearest
  corner to its farthest, plus 0.5 m on each side. A nearer pixel is
  something in front of the actor; a farther one is something behind it.

The final box is drawn around those pixels. An actor with fewer than 64
such pixels is hidden, and it is left out.

.. figure:: /_static/images/GP2/gp2_loose_vs_tight.png
   :alt: A camera frame from the demo drive. A black and white police car is parked at the left of the road, 5.5 to 10.7 meters away, seen at an angle. An orange box, the projection of its 3D box, reaches past the car on the left and well below it. A green box, drawn around the pixels that show the car, fits the car's outline.
   :align: center
   :width: 90%

   A police car 5.5 to 10.7 m ahead, seen at an angle. **Orange:** the
   projection of its 3D box. **Green:** the box around the pixels that
   show it. RT-DETR-L's box (score 0.94, not drawn) overlaps the green box
   with IoU 0.955 and the orange box with IoU 0.672.

**Why step 2 matters.** On our demo drive, graded against the loose boxes,
RT-DETR-L scores an mAP\@0.5 of 0.608 by day. Graded against the tight boxes,
the same detections score 0.895. The detector did not change; the answer
key did. With loose boxes, a correct detection fails the IoU test because
the answer key is wrong.

**Two corrections the starter makes for you.**

- **A car beside the AV** can have corners behind the camera. Those corners
  have no pixel. ``clip_near`` cuts the 3D box at 0.1 m in front of the
  camera before it is projected, so the front of the car still gets a box.
- **A walking person** reaches past CARLA's walker box, which is tight
  around the body at rest (0.4 to 0.5 m across). ``widen_walker`` makes it
  0.3 m wider in every horizontal direction. We checked this against
  CARLA's instance camera, which labels every pixel with the actor it
  shows: without the margin, 32% of our pedestrian boxes matched it with
  IoU 0.9 or more; with it, 98.7%.


IoU: How Well Two Boxes Overlap
-------------------------------

**IoU** (intersection over union) compares a detected box :math:`D` with a
ground-truth box :math:`G`:

.. math::

   \text{IoU}(D, G) = \frac{\text{area}(D \cap G)}{\text{area}(D \cup G)}

1 means the same box; 0 means no overlap at all. A detection counts as
finding an object only when their IoU reaches a **threshold** :math:`t`
that you choose before grading.

.. figure:: /_static/images/GP2/gp2_iou_examples.png
   :alt: Three panels. In each, a green square (the ground truth) and a dashed red square of the same size (the detection) shifted to the right, their overlap shaded. Left: IoU 0.50, shifted 33 percent of a box width. Middle: IoU 0.75, shifted 14 percent. Right: IoU 0.90, shifted 5 percent.
   :align: center
   :width: 95%

   **Green:** the ground truth. **Dashed red:** a detection of the same
   size, shifted right. A shift of a third of the box width already brings
   IoU down to 0.5; IoU 0.9 allows only a 5% shift.

For two boxes of the same size, shifted by a share :math:`s` of their
width, the overlap is :math:`1 - s` of a box and the union :math:`1 + s`
boxes, so :math:`\text{IoU} = (1 - s)/(1 + s)`. At :math:`s = 1/3`:
:math:`(2/3)/(4/3) = 0.5`.


Matching: Which Detections Are Right in One Frame
-------------------------------------------------

With a threshold :math:`t`, each detection is either right or wrong, and
each object is either found or missed:

- **True positive (TP):** a detection matched to an object.
- **False positive (FP):** a detection matched to nothing. Either it
  overlaps nothing enough, or the object it overlaps is already taken.
- **False negative (FN):** an object no detection matched.

The matching rule, the one L4's appendix and COCO use:

1. Sort the frame's detections by confidence, highest first.
2. Go down the list. Each detection looks at the objects of its own class
   that are **not yet taken**, and takes the one with the highest IoU, if
   that IoU is at least :math:`t`.
3. A detection that takes an object is a TP, and the object is taken. A
   detection that finds nothing is an FP.
4. Objects never taken are FN.

**A worked example,** with numbers chosen for the example. One frame, two
people A and B, three detections, threshold 0.5:

.. list-table::
   :widths: 18 18 30 34
   :header-rows: 1
   :class: compact-table

   * - Detection
     - Confidence
     - IoU with A, with B
     - Result
   * - d1
     - 0.9
     - 0.8, 0.0
     - **TP**: takes A
   * - d2
     - 0.8
     - 0.6, 0.0
     - **FP**: A is taken, a duplicate
   * - d3
     - 0.7
     - 0.0, 0.4
     - **FP**: 0.4 is below 0.5

B is an **FN**. So one frame gives 1 TP, 2 FP and 1 FN. d2 shows why NMS
matters (L4): a duplicate box always costs a false positive.


Precision and Recall
--------------------

Two shares describe a set of detections:

.. math::

   \text{precision} = \frac{TP}{TP + FP}, \qquad
   \text{recall} = \frac{TP}{TP + FN} = \frac{TP}{\text{number of objects}}

- **Precision** answers: *of the boxes the detector gave, how many were
  right?* Low precision means the AV brakes for things that are not there.
- **Recall** answers: *of the objects that were there, how many did the
  detector find?* Low recall means the AV does not see a person who is
  there.

In the example above, precision is :math:`1/3` and recall is :math:`1/2`.

The two pull against each other through the **confidence cut**. Keep only
boxes above confidence 0.9 and you keep few boxes, mostly right: high
precision, low recall. Keep everything above 0.1 and you find more objects
but keep more mistakes: higher recall, lower precision. Every cut gives one
(precision, recall) pair.


The Precision-Recall Curve and AP
---------------------------------

Instead of picking one cut, AP looks at all of them at once.

1. Pool the detections of every frame and sort them by confidence, highest
   first. Each one is already marked TP or FP by the matching.
2. Go down the list. After each detection, compute precision and recall
   **so far**. Each step is one cut, just below that detection's
   confidence. Plotted, the pairs form the **precision-recall (PR)
   curve**.
3. Make precision never rise as recall grows: at each recall, take the best
   precision at that recall **or beyond**.
4. Read that line at the 101 recalls 0, 0.01, ..., 1.00, and average the
   101 values. A recall the detector never reaches counts as 0. That
   average is the **AP** (average precision) of one class at one IoU
   threshold.

L4's appendix example: 3 people, 5 detections, threshold 0.5.

.. list-table::
   :widths: 14 16 12 29 29
   :header-rows: 1
   :class: compact-table

   * - Step
     - Confidence
     - Right?
     - Precision so far
     - Recall so far
   * - 1
     - 0.95
     - TP
     - 1/1 = 1.00
     - 1/3 = 0.33
   * - 2
     - 0.90
     - TP
     - 2/2 = 1.00
     - 2/3 = 0.67
   * - 3
     - 0.80
     - FP
     - 2/3 = 0.67
     - 2/3 = 0.67
   * - 4
     - 0.60
     - TP
     - 3/4 = 0.75
     - 3/3 = 1.00
   * - 5
     - 0.40
     - FP
     - 3/5 = 0.60
     - 3/3 = 1.00

.. figure:: /_static/images/GP2/gp2_pr_l4_example.png
   :alt: A precision against recall plot. Five red dots numbered 1 to 5 mark the table's steps: 1 at recall 0.33 and precision 1.00, 2 at 0.67 and 1.00, 3 at 0.67 and 0.67, 4 at 1.00 and 0.75, 5 at 1.00 and 0.60. A blue step line runs at precision 1.00 from recall 0 to 0.67, then drops to 0.75 until recall 1.00, with small blue dots on it at every 0.01 of recall; the area under it is shaded. The title reads: AP = average of the 101 blue dots = 0.916.
   :align: center
   :width: 80%

   **Red:** the five steps of the table. **Blue:** the best precision at
   each recall or beyond, read at 101 recalls. Step 3 sits below the line:
   step 4 reaches more recall with better precision, so it sets the line.

The 101 values, in three steps:

1. Recalls 0 to 0.66 read precision 1.00: 67 values.
2. Recalls 0.67 to 1.00 read 0.75: 34 values. (Recall 2/3 is 0.667, just
   below 0.67, so 0.67 already reads the next step.)
3. Average: :math:`(67 \times 1.00 + 34 \times 0.75)/101 = 92.5/101 = 0.916`.

**Why grading keeps boxes down to confidence 0.001.** The curve needs the
whole ranked list. Cutting at 0.5 before grading throws away the low part
of the list, so the curve stops early and every recall beyond that point
counts as 0. Your ``detector_core.predict`` uses 0.001 for grading; the ROS
node uses 0.5, because a planner should not see weak boxes.


From AP to mAP\@0.5
-------------------

GP2 has two classes, vehicle and pedestrian, and each gets its own AP.

**mAP** is the **mean of the per-class APs**. The "\@0.5" names the **IoU
threshold** used in the matching. So:

.. math::

   \text{mAP@0.5} = \frac{\text{AP}_{\text{vehicle}}(t = 0.5) +
   \text{AP}_{\text{pedestrian}}(t = 0.5)}{2}

On our demo drive, by day, RT-DETR-L has AP 0.911 for vehicles and 0.879
for pedestrians:

.. math::

   \text{mAP@0.5} = \frac{0.911 + 0.879}{2} = 0.895

In words: lower RT-DETR-L's confidence cut step by step, from the point
where it finds nothing to the point where it finds all it can. At each
step, ask what share of its boxes so far are right (IoU 0.5 or more with a
real object of the same class). **Averaged over the recall from 0 to 1,
and over the two classes, that share is 0.895.**

.. important::

   **Three things mAP\@0.5 is not.**

   - **Not a confidence.** The 0.5 is the IoU threshold. The confidence cut
     does not appear in mAP at all: AP already averages over every cut.
   - **Not the mean precision at one cut.** It averages precision over
     recall, from 0 to 1, after the "best at this recall or beyond" step.
   - **Not comparable across datasets.** 0.895 is RT-DETR-L on our drive,
     with our ground truth. COCO's published number is a different test.


mAP\@0.5:0.95: How Tight the Boxes Are
--------------------------------------

IoU 0.5 is lenient: the IoU figure shows a box shifted by a third of its
width still passing. **mAP\@0.5:0.95** repeats the whole calculation at 10
thresholds, 0.50, 0.55, ..., 0.95, and averages the 10 mAPs. Papers often
write it as COCO's "AP".

.. figure:: /_static/images/GP2/gp2_ap_vs_iou.png
   :alt: A line plot of mAP, the mean of the two classes, against the IoU threshold from 0.50 to 0.95. Four lines: YOLOv8s clear and RT-DETR-L clear solid, YOLOv8s night and RT-DETR-L night dashed. All four fall as the threshold rises, slowly at first and steeply above 0.8, to between 0.06 and 0.09 at 0.95. RT-DETR-L clear is the highest everywhere, starting at 0.895. The legend gives the averages: YOLOv8s clear 0.501, RT-DETR-L clear 0.627, YOLOv8s night 0.449, RT-DETR-L night 0.546.
   :align: center
   :width: 80%

   mAP at each of the 10 thresholds on the demo drive. The average of each
   line's 10 points is its mAP\@0.5:0.95 (in the legend).

What the plot says:

- **Every detector loses points as the threshold rises.** At 0.95, a box
  must almost coincide with the ground truth; few do.
- **mAP\@0.5 says whether the detector finds the object. mAP\@0.5:0.95 adds
  how well the box fits it.** A planner that needs the distance to a car
  from the bottom edge of its box cares about the fit.
- The gap between the solid and the dashed lines is what the night costs.


Reading Our PR Curves
---------------------

.. figure:: /_static/images/GP2/gp2_pr_curves.png
   :alt: Two precision against recall plots for the clear demo drive at IoU threshold 0.5. Left, vehicles: RT-DETR-L in red stays near precision 1 until recall 0.7 and reaches recall 0.98; YOLOv8s in blue starts dropping near recall 0.4 and ends at recall 0.78. Legend: YOLOv8s AP 0.719, RT-DETR-L AP 0.911. Right, pedestrians: both stay near precision 1 until about recall 0.6; YOLOv8s ends at recall 0.90, RT-DETR-L at 0.98. Legend: YOLOv8s AP 0.812, RT-DETR-L AP 0.879. On each curve an open circle marks where confidence 0.5 cuts.
   :align: center
   :width: 100%

   The demo drive by day, IoU threshold 0.5. The open circles mark where
   the ROS node's confidence cut, 0.5, lands on each curve.

- **Where a curve ends is the most recall the detector can give, at any
  cut.** YOLOv8s's vehicle curve ends at recall 0.78: about 22% of the
  vehicles in our ground truth get no box from it with IoU 0.5, even at
  confidence 0.001. RT-DETR-L reaches 0.98.
- **The open circle is what the AV gets at run time.** At confidence 0.5,
  YOLOv8s finds 50% of the vehicles with precision 0.95; RT-DETR-L finds
  85% with precision 0.85. More found, more false boxes: that is the
  trade-off a cut makes.
- **AP is close to the area under the curve,** after step 3 makes the
  curve fall only. A curve that stays high longer has the larger AP.


Scoring the Tracker: ID Switches and MOTA
-----------------------------------------

A tracker is graded on something a detector cannot be: **does each object
keep one ID over time?** The ground truth carries every actor's CARLA ID,
so ``grade.py`` can check.

In each frame, it pairs every ground-truth box with at most one confirmed
track of the same class (Hungarian algorithm, IoU 0.5 or more). Then:

- **Miss** (:math:`m_t`): a ground-truth box with no track.
- **False track** (:math:`fp_t`): a track with no ground-truth box.
- **ID switch** (:math:`mme_t`): an actor matched to a different track ID
  than the last time it was matched.

**MOTA** (multiple object tracking accuracy, Bernardin and Stiefelhagen,
2008) puts the three together, summed over all frames before dividing:

.. math::

   \text{MOTA} = 1 - \frac{\sum_t (m_t + fp_t + mme_t)}{\sum_t g_t}

with :math:`g_t` the number of ground-truth boxes in frame :math:`t`.
**A worked example,** with numbers chosen for the example: 1000
ground-truth boxes over a drive, 200 misses, 50 false tracks, 10 ID
switches give :math:`1 - 260/1000 = 0.74`. MOTA can go below 0 when the
tracker makes more errors than there are objects.

.. figure:: /_static/images/GP2/gp2_track_timeline.png
   :alt: Two timeline panels, YOLOv8s on top and RT-DETR-L below, for six actors of the clear demo drive: pedestrians 346, 286, 328 and 321 and vehicles 210 and 256, over about 23 seconds. A gray line shows the frames where each actor is in the ground truth; colored bars show when a confirmed track covers it, one color per track ID; black crosses mark ID switches. Pedestrian 328 is in the ground truth from about 1 to 3.5 seconds and again from 8.7 to 12.5 seconds. YOLOv8s: 7 switches, 5 of them on pedestrian 321 between 4 and 8 seconds, whose bar is broken into many pieces; it covers pedestrian 328 only from 10 seconds. RT-DETR-L: 3 switches, one each on pedestrians 346 and 328 and vehicle 210; it covers pedestrian 328 briefly near 3 seconds and again from 10 seconds with a new color.
   :align: center
   :width: 100%

   Six actors of the demo drive by day, tracked at confidence 0.5. **Gray:**
   the actor is in the ground truth. **A colored bar:** a confirmed track
   covers it, one color per track ID. **A cross:** an ID switch. Gray with
   no bar over it is a miss.

What the timeline shows:

- **Gaps come before switches.** YOLOv8s loses pedestrian 321 again and
  again between 4 and 8 s. Each time the track misses frames, and the new
  detection can start a new track: a new ID.
- **Gray with no bar is a miss.** Pedestrian 328 is in the ground truth
  from 0.8 to 3.6 s, while its box is only 12 to 31 px tall. YOLOv8s never
  tracks it then; RT-DETR-L does for under 1 s. Every one of those frames
  counts against MOTA.
- **An object that comes back gets a new ID.** Pedestrian 328 leaves the
  ground truth at 3.6 s and returns at 8.7 s. RT-DETR-L's earlier track
  was deleted after 5 frames with no match, so the person gets a new
  track at 10 s, and ``grade.py`` counts an ID switch.

**The truth row.** ``grade.py`` also runs your tracker on the ground truth
itself, a perfect detector. On our demo drive that gave MOTA 0.874 and 5
ID switches. Even a perfect detector loses a little: every new track waits
2 frames before it is reported, and a box that moves too far between two
frames fails the IoU 0.3 gate and starts a new track. **If your truth row
is much lower than ours, look for the bug in your tracker before you blame
a detector.**
