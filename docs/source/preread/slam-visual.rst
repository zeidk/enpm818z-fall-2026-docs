====================================================
Visual SLAM
====================================================

.. admonition:: Read this after L6, and after SLAM with a LiDAR
   :class: important

   This page is **reading material** for :doc:`L6 </lectures/lecture6/l6_index>`.
   It uses the SLAM problem, the pose graph and the Gauss-Newton solve from
   :doc:`SLAM with a LiDAR </preread/slam-lidar>`, and replaces the LiDAR
   front end with a camera. L6 listed the steps of ORB-SLAM without numbers,
   because our drive had no camera. This page records one and runs each step.

**The recording.** We drove the L6 route again in CARLA's Town10HD: the
same car, the same two laps, no other traffic. This time two cameras look
forward from the roof, side by side.

.. list-table::
   :widths: 35 65
   :header-rows: 0
   :class: compact-table

   * - Images
     - 1024 x 512 pixels, grayscale, 90° field of view
   * - Rate
     - 10 Hz: 1,256 image pairs over 914 m
   * - Baseline
     - 0.54 m between the two cameras (chosen to match KITTI, below)
   * - Mount
     - 1.2 m forward and 1.7 m up from the car's reference point, looking
       straight ahead
   * - Truth
     - the left camera's true pose for every pair, from CARLA

KITTI, the best-known driving dataset, uses "a baseline of roughly 54 cm"
(Geiger, Lenz and Urtasun, 2012). **Every number on this page was measured
on this recording** with our own Python code, using OpenCV for the image
steps. The code is ours; the methods are the ones the cited papers
describe, sometimes simplified, and the page says where.


The Camera Model
----------------

A camera measures **directions**, not distances. The **pinhole model**,
the one GP1 and GP2 use, maps a point :math:`(X, Y, Z)` in the camera's
**optical frame** (:math:`X` right, :math:`Y` down, :math:`Z` forward) to
the pixel

.. math::

   u = f\,\frac{X}{Z} + c_u, \qquad v = f\,\frac{Y}{Z} + c_v

with :math:`f` the focal length in pixels and :math:`(c_u, c_v)` the image
center. For our camera:

1. :math:`f = \dfrac{W}{2\tan(\text{FOV}/2)} = \dfrac{1024}{2 \tan 45°}
   = 512` pixels.
2. :math:`(c_u, c_v) = (512, 256)`, the middle of the image.

The point :math:`(2X, 2Y, 2Z)`, twice as far along the same ray, lands on
the same pixel. **One image cannot tell those two points apart.** Every
method on this page is a way to get the missing distance back: a second
camera beside the first, a second image after the car has moved, or a
second sensor.


Step 1: Find Points You Can Find Again
--------------------------------------

To measure motion between two images, the front end needs points it can
find in both: the corner of a window, the base of a lamp post. Not a
patch of plain wall, which looks the same one pixel to the left.


FAST: a fast corner test
~~~~~~~~~~~~~~~~~~~~~~~~

FAST (Rosten and Drummond, 2006) tests each pixel against a ring around it:
"The segment test criterion operates by considering a circle of sixteen
pixels around the corner candidate p." The pixel is a corner "if there
exists a set of n contiguous pixels in the circle which are all brighter
than the intensity of the candidate pixel Ip plus a threshold t, or all
darker than Ip − t". The original detector used :math:`n = 12`; the paper
found that ":math:`n = 9` is the most repeatable".


ORB: FAST with an orientation, and a binary description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A corner alone is a location. To match it in another image, the front end
also needs a **descriptor**: a short summary of the patch around it.

ORB (Rublee et al., 2011) gives both: "we call it ORB (Oriented FAST and
Rotated BRIEF)".

- **Oriented FAST:** FAST corners, each with a direction computed from its
  patch, so the description can be turned to match before comparing.
- **Rotated BRIEF:** "a bit string description of an image patch
  constructed from a set of binary intensity tests". Each bit answers one
  question: is pixel A of the patch brighter than pixel B? ORB uses 256
  such tests: "We also choose a vector length n = 256."
- **Comparing two descriptors** is counting the bits that differ, the
  **Hamming distance**: from 0 (the same) to 256. A computer does that with
  one XOR and one bit count.
- **A pyramid.** ORB looks for corners in the image and in smaller and
  smaller copies of it, so a window found close up can be found again from
  far away.

.. figure:: /_static/images/SLAM/visual_orb.png
   :alt: A grayscale street view from the left camera, frame 300: tall buildings on both sides, palm trees, a bus shelter on the right, the road ahead. About 4000 colored dots mark ORB features, colored by pyramid level from 0, dark blue, to 7, yellow. They cluster on the buildings, trees, the bus shelter and the sidewalk edge; the road surface and the sky have almost none.
   :align: center
   :width: 90%

   Frame 300, left camera: the 4,000 ORB features we asked for (chosen),
   colored by pyramid level. 0 is the full image; each level is a smaller
   copy.

What the figure shows:

- The features sit on texture: windows, leaves, the bus shelter, the curb.
  The road and the sky have almost none. A camera needs texture, which is
  why L6 listed "dark, texture-less" as its weak case.
- Only **21.7%** of the 4,000 are found at full size (level 0). The rest
  come from the smaller copies.

**Matching** between two images: for each feature in the first, find the
two nearest descriptors in the second by Hamming distance. Keep the match
only if the nearest is clearly better than the second nearest: distance
below 0.8 times the second's (0.8 is chosen). A feature on a row of
identical windows has two near-equal candidates and is dropped.


Step 2: Depth from Two Cameras
------------------------------

.. figure:: /_static/images/SLAM/visual_stereo_pair.png
   :alt: Two grayscale images side by side, labeled left camera and right camera, 0.54 meters to the right. The same street scene, shifted slightly. A red horizontal line crosses both images at the same row, through the sidewalk, the bus shelter and a planter.
   :align: center
   :width: 100%

   Frame 300 from both cameras. The red line is the same image row in
   both. Every object on it in the left image is also on it in the right
   image, a little to the left.


Disparity gives depth
~~~~~~~~~~~~~~~~~~~~~

The two cameras are the same, face the same way, and the right one sits
:math:`b = 0.54` m to the right. A point at :math:`(X, Y, Z)` in the left
camera's frame is at :math:`(X - b, Y, Z)` in the right camera's. Its
pixels:

.. math::

   u_L = f\,\frac{X}{Z} + c_u, \qquad u_R = f\,\frac{X - b}{Z} + c_u,
   \qquad v_L = v_R

So a match is always on **the same row**, and the shift between the two,
the **disparity** :math:`d`, gives the depth:

.. math::

   d = u_L - u_R = \frac{f\,b}{Z} \qquad\Longrightarrow\qquad
   Z = \frac{f\,b}{d}

For our rig, :math:`f\,b = 512 \times 0.54 = 276.48` pixel meters.


Far points are measured badly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Disparity shrinks as :math:`1/Z`. A small error :math:`\Delta d` in the
disparity changes the depth by about

.. math::

   \Delta Z \approx \frac{Z^2}{f\,b}\,\Delta d

the derivative of :math:`Z = fb/d`, rewritten with :math:`d = fb/Z`.

.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * - Depth :math:`Z`
     - Disparity :math:`d = 276.48 / Z`
     - Depth error for 1 pixel of disparity error
   * - 5 m
     - 55.3 px
     - :math:`25 / 276.48 = 0.09` m
   * - 10 m
     - 27.6 px
     - :math:`100 / 276.48 = 0.36` m
   * - 20 m
     - 13.8 px
     - :math:`400 / 276.48 = 1.45` m
   * - 40 m
     - 6.9 px
     - :math:`1600 / 276.48 = 5.79` m

Doubling the distance makes the error 4 times larger. We drop every point
farther than **40 m** (chosen): there, a 1-pixel error is already 5.79 m of
depth. A wider baseline :math:`b` makes every error smaller in the same
proportion.


Finding the disparity: semi-global matching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Matching ORB features left to right gives a disparity only at corners, and
only to the nearest pixel. A **dense** method finds one at almost every
pixel. Semi-global matching (SGM, Hirschmüller, 2008) compares small
patches along the row and then smooths the result: "This leads to the new
idea of aggregating matching costs in 1D from all directions equally." It
sums, for each pixel and each candidate disparity, the costs along straight
paths that end at that pixel: "The number of paths must be at least eight
and should be 16 for providing a good coverage of the 2D image."

We use OpenCV's version of it (``StereoSGBM``: 128 disparities, 5 x 5
blocks, chosen), which returns each disparity in sixteenths of a pixel.
Each ORB feature reads its disparity from that map.

.. figure:: /_static/images/SLAM/visual_disparity.png
   :alt: Two panels for frame 300. Left, disparity in pixels from 0 to about 80: the road near the bottom is bright, up to 80 pixels, fading upward; buildings far ahead are dark, under 10 pixels; the sky is white, meaning no value. Right, depth in meters, cut at 60: the road near the car is dark, under 10 meters; the buildings and trees ahead are yellow, 60 meters or more; the right-hand building is green, around 30 to 40 meters.
   :align: center
   :width: 100%

   Frame 300. **Left:** the disparity :math:`d` from SGM; white has no
   value. **Right:** the depth :math:`Z = fb/d`, cut at 60 m for display.

In frame 300, **79.6%** of the pixels get a disparity. The sky gets none:
it has no texture and no depth to measure. Of the 4,000 ORB features,
**1,535** get a depth under 40 m and become 3-D points. Over the whole
drive, the median is **1,383** per frame.

**Why we use dense disparity.** An earlier version of our code took each
feature's disparity from its ORB match in the right image, to the nearest
pixel. Its odometry (Step 4) drifted to an RMSE of 16.03 m and ended
21.97 m off in height. With SGM's disparity, the same odometry has an RMSE
of 7.72 m and ends 1.79 m off in height. Depth errors go straight into
the motion estimate.


Step 3: One Camera Gives the Direction, Not the Distance
--------------------------------------------------------

Without the right camera, depth must come from motion: the same point seen
from two places. For two images of one camera, the geometry is the
**essential matrix** :math:`E`. With :math:`x_1` and :math:`x_2` the
directions (normalized image coordinates) to the same point in the two
images:

.. math::

   x_2^\top E\, x_1 = 0, \qquad E = [t]_\times R

where :math:`R` and :math:`t` are the rotation and translation between the
two camera poses and :math:`[t]_\times` is the matrix that computes
:math:`t \times (\cdot)`. Nistér's algorithm finds :math:`E` from five
matches: "The problem is to find the possible solutions for relative
camera motion between two calibrated views given five corresponding
points" (Nistér, 2003). "Once the essential matrix is known, R, t and the
camera matrices can be recovered from it."

**The catch.** Multiply :math:`t` by any number :math:`s` and the equation
still holds: :math:`x_2^\top [s\,t]_\times R\, x_1 = s \cdot 0 = 0`. So
:math:`E` fixes the **direction** of travel but not its **length**. Scale
the whole scene and the motion by :math:`s`, and the two images do not
change.

**Measured,** left camera only, frames 300 and 302 (0.2 s apart):

1. 792 ORB matches; RANSAC (next step) kept **402** as consistent with one
   :math:`E`.
2. The recovered direction of travel is **1.2°** from the true one.
3. The recovered length is **1.0**: OpenCV returns a unit vector. The car
   really moved **1.597 m**.

A one-camera SLAM therefore builds a map in its own unit, which drifts as
the run goes on. "Monocular vision-only systems are incapable of recovering
the metric scale" (Qin, Li and Shen, 2018). The fixes are a second camera,
as on this page, or an IMU, which measures acceleration in meters per
second squared: with one, "the metric scale, as well as roll and pitch
angles" become "observable" (Qin, Li and Shen, 2018).


Step 4: Track the Camera from Frame to Frame
--------------------------------------------

With stereo, frame :math:`k` gives 3-D points, and frame :math:`k+1` gives
the pixels where the same points appear now. Finding the camera pose from
3-D points and their pixels is the **Perspective-n-Point** problem (PnP).
Find :math:`R` and :math:`t` (frame :math:`k` to frame :math:`k+1`) that
make the **reprojection error** smallest:

.. math::

   \sum_i \left\| p_i - \pi(R\,P_i + t) \right\|^2

with :math:`P_i` a 3-D point from frame :math:`k`, :math:`p_i` its matched
pixel in frame :math:`k+1`, and :math:`\pi` the pinhole projection above.


RANSAC: ignore the wrong matches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some matches are wrong: a window paired with the next window, or, in
traffic, a point on a car that moved. One wrong match far away can pull a least-squares solution
anywhere. **RANSAC** (random sample consensus) finds the answer most matches
agree on:

1. Pick a few matches at random, the fewest that fix a pose.
2. Solve for the pose from them alone.
3. Count the **inliers**: matches whose reprojection error under that pose
   is below 2 pixels (chosen).
4. Repeat (200 tries, chosen), and keep the pose with the most inliers.
5. Refine that pose by least squares on its inliers only (OpenCV's
   Levenberg-Marquardt refinement).

.. figure:: /_static/images/SLAM/visual_matches.png
   :alt: Frame 301 from the left camera with short line segments drawn from each feature's position in frame 300 to its match in frame 301. Green segments, labeled kept by RANSAC, 256, are short and mostly horizontal, on the bus shelter, the sidewalk and the buildings on the right. Red segments, labeled rejected, 166, include several long lines that cross the image between unrelated places.
   :align: center
   :width: 90%

   Frame 300 to frame 301. Each line joins a feature's position in frame
   300 to its match in frame 301. **Green:** kept by RANSAC (256).
   **Red:** rejected (166).

For this pair: 1,535 3-D points from frame 300, 422 matches into frame 301,
256 kept. Over the whole drive the medians are 404 matches and 250 inliers.
If fewer than 20 inliers were left (chosen), our code would repeat the last
motion; that never happened on this drive.

**Chaining the poses.** Each PnP gives the motion from one frame to the
next. The camera's pose in the map is the product of all of them since the
start: the same chaining as L6's dead reckoning and scan-to-scan ICP, with
the same drift.


Stereo visual odometry, measured
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/SLAM/visual_trajectory.png
   :alt: A top view, x east against y north in meters, of the two laps. The black truth is a rounded rectangle from about x minus 48 to 110 and y minus 28 to 67. The red stereo visual odometry follows the right side closely but runs inside the top side by 5 to 10 meters and outside the bottom-left corner by up to about 12 meters, with lap 2 farther off than lap 1. It ends at about x 0, y minus 35, legend: 11.28 meters off at the end.
   :align: center
   :width: 80%

   The truth (black) and stereo visual odometry (red), two laps.

.. list-table::
   :widths: 50 50
   :header-rows: 0
   :class: compact-table

   * - Error at the end
     - 11.28 m, which is 1.23 m per 100 m driven
   * - RMSE over the drive
     - 7.72 m
   * - Largest error
     - 14.94 m
   * - Heading error at the end
     - 3.82°
   * - Height error at the end
     - 1.79 m (the road is flat, so all of it is drift)

The camera estimates all 6 degrees of freedom: position in 3-D and three
angles. So it can drift in height and tilt, which a 2-D LiDAR cannot. On the
same route, LiDAR scan-to-scan odometry ended 11.26 m off and scan to
submap 1.07 m (:doc:`SLAM with a LiDAR </preread/slam-lidar>`).


Step 5: Keyframes and Bundle Adjustment
---------------------------------------

Tracking frame to frame repeats the LiDAR's scan-to-scan problem: every
error stays in the chain. Visual SLAM systems keep **keyframes**, images
chosen as the car moves, and a local map of 3-D points seen from several of
them.

- **Bundle adjustment** refines the keyframe poses and the 3-D points
  together, so that every point projects as close as possible to where it
  was seen, in every keyframe that saw it: the reprojection error above,
  summed over all keyframes and all points. A point seen from many
  keyframes holds them all together, as the submap held the LiDAR scans.
- **ORB-SLAM** (Mur-Artal, Montiel and Tardós, 2015) "incorporates three
  threads that run in parallel: tracking, local mapping and loop closing."
  Its keyframes form a **covisibility graph**: "Each node is a keyframe and
  an edge between two keyframes exists if they share observations of the
  same map points (at least 15)".

We did not run bundle adjustment. Our keyframes, one every 2 m of travel
(chosen), are used only for loop closure and the pose graph: **384**
keyframes.


Step 6: Loop Closure with a Bag of Visual Words
-----------------------------------------------

To close a loop, the front end must recognize a place from an image. ORB-SLAM
"has embedded a bags of words place recognition module, based on DBoW2, to
perform loop detection and relocalization" (Mur-Artal, Montiel and Tardós,
2015).

.. admonition:: Definition: bag of visual words
   :class: note

   A **vocabulary** of typical descriptors, the **words**, is built in
   advance by clustering many descriptors. Each image is then described by
   which words its features are closest to, and how often: a histogram
   over the vocabulary. Where the features are in the image is ignored,
   which is why it is called a bag.


Our vocabulary, step by step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Sample descriptors:** 200 ORB descriptors from every third keyframe.
2. **Cluster them** into **500 words** (chosen) with k-means, treating each
   descriptor's 256 bits as 256 numbers, 0 or 1.
3. **Describe each keyframe:** give each of its 4,000 features the nearest
   word, and count how many features fall on each word.
4. **Weigh rare words up** (tf-idf). A word found in almost every keyframe,
   say, a texture of the road edge, says little about where you are. Each
   word's count is multiplied by :math:`\ln(N / n_w)`, with :math:`N` the
   number of keyframes and :math:`n_w` the number that contain the word.
5. **Compare two keyframes** by the cosine of the angle between their
   weighted histograms: 1 for the same mix of words, 0 for no word in
   common.

Two simplifications, to keep in mind. Our vocabulary comes from this
drive's own images; a real system builds it in advance, from other images.
And it is flat: one list of 500 words. DBoW2 (Gálvez-López and Tardós,
2012) builds a tree and works on the bits directly: "For the first time, we
build a vocabulary tree that discretizes a binary descriptor space, and use
the tree to speed up correspondences for geometrical verification." For
each word it keeps the list of images that contain it, the usual
**inverse index**, and for each image its features, a **direct index**.


Propose, then verify
~~~~~~~~~~~~~~~~~~~~

For each keyframe :math:`i`:

1. Among the keyframes at least 100 m earlier along the car's own odometry
   (chosen, as for the LiDAR), take the one most similar to :math:`i`.
2. If the similarity is 0.30 or more (chosen), it is a **candidate**.
3. **Verify** with PnP: the candidate's stereo 3-D points against keyframe
   :math:`i`'s features. Accept the loop if RANSAC keeps 60 inliers or more
   (chosen). The PnP pose is the loop edge.

**Measured on our drive:**

1. **341** candidates passed the similarity gate.
2. PnP rejected **231** of them.
3. **110** loops were accepted. **108** are right: within 1 m and 5° of the
   true relative pose.
4. **2 are wrong,** off by **19.89 m** and **39.54 m**.

.. figure:: /_static/images/SLAM/visual_bow_similarity.png
   :alt: A 384 by 384 heat map of word similarity between keyframes, from 0, dark purple, to 1, yellow. The main diagonal is bright. Two parallel bright diagonals run about 192 keyframes off it, one above and one below. Several bright square blocks appear, for example keyframes 50 to 80 with each other and with keyframes 245 to 275, and keyframes 140 to 170 with 335 to 365. Other areas are green, around 0.5 to 0.7.
   :align: center
   :width: 65%

   The similarity of every keyframe to every other. The main diagonal is
   each keyframe with itself. The two diagonals about 192 keyframes off it
   are lap 2 against lap 1 at the same place: the loops we want.

**Perceptual aliasing.** Look at the bright **squares**, not only the
diagonals. Keyframes 50 to 80 are all very similar to each other, and to
keyframes 245 to 275, the same stretch on lap 2. Along that stretch, every
image looks like every other one, so the similarity cannot say which one
is the same place. The numbers say the same. When the most similar old
keyframe was truly the same place (within 5 m), its median similarity was
**0.892**. When it was somewhere else, the median was still **0.728**.
Similarity alone separates them poorly, so the gate is set low and PnP does
the real check. On repeated façades, even PnP can be fooled: that is where
the 2 wrong loops come from.


Step 7: A Back End That Survives Wrong Loops
--------------------------------------------

The back end is the SE(2) pose graph from
:doc:`SLAM with a LiDAR </preread/slam-lidar>`: 384 keyframe nodes, 383
odometry edges, 110 loop edges, the same information matrices (5 cm and
0.5° for odometry, 10 cm and 1° for loops, chosen). The graph is flat:
:math:`x`, :math:`y` and heading. It does not touch the 1.79 m height drift.

Plain least squares trusts every edge. A loop edge that is 40 m wrong but
claims 10 cm of accuracy adds :math:`(40/0.1)^2 = 160{,}000` to the cost.
The cheapest way to shrink that is to bend the graph toward it.


A robust kernel: wrong loops count less
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before each Gauss-Newton step, give each loop edge a weight from how badly
it disagrees with the current poses, and multiply its :math:`\Omega` by
the weight. We used the **Cauchy** weight:

.. math::

   w = \frac{1}{1 + \chi^2 / c^2}, \qquad \chi^2 = e^\top \Omega\, e

with :math:`c = 3` (chosen). An edge that fits (:math:`\chi^2` near 0) keeps
a weight near 1. At :math:`\chi^2 = c^2 = 9`, the weight is 0.5. An edge
that misses by 20 m with :math:`\sigma = 0.1` m has
:math:`\chi^2 \approx (20 / 0.1)^2 = 40{,}000` and a weight near
:math:`1/(1 + 40{,}000/9) \approx 0.0002`. Solving again and again with new
weights is called **iteratively reweighted least squares**.

The SLAM literature has several versions of this idea:

- **Switchable constraints** (Sünderhauf and Protzel, 2012) start from the
  same problem: "Current SLAM back-ends are based on least squares
  optimization and thus are not robust against outliers like data
  association errors and false positive loop closure detections." Each
  loop edge gets a switch variable that the optimizer can turn down: it
  "can drive it from its original value to zero, thus increasing the
  covariance associated with this factor until infinity."
- **Dynamic covariance scaling** (Agarwal et al., 2013) "dynamically
  scales the information matrix of each non-incremental edge", by a factor
  that "considers the magnitude of the current error".


The two back ends, measured
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/SLAM/visual_graph.png
   :alt: Three top views of the block with the truth as a thick gray line and the keyframes in blue. Left, before, RMSE 7.67 meters: the visual odometry drifting off the truth, with two orange wrong loop edges near the bottom left. Middle, plain least squares, 9.73 meters: the left side of the path is bent inward, up to about 20 meters from the truth, and the bottom-left corner is pulled away from it. Right, with a robust kernel, 1.81 meters: the keyframes lie on the truth almost everywhere; the two orange edges lie along the bottom street.
   :align: center
   :width: 100%

   **Left:** before. **Middle:** plain least squares. **Right:** with the
   Cauchy weights. **Orange:** the 2 wrong loop edges. Truth in gray.

.. list-table::
   :widths: 34 22 22 22
   :header-rows: 1
   :class: compact-table

   * -
     - Before
     - Plain
     - Cauchy
   * - APE RMSE
     - 7.67 m
     - 9.73 m
     - 1.81 m
   * - Largest error
     - 14.94 m
     - 22.38 m
     - 3.28 m
   * - Iterations
     -
     - 20 (our cap)
     - 12

1. **Plain:** 108 right loops and 2 wrong ones. The result is **worse than
   no back end at all**: 9.73 m against 7.67 m. The wrong loops bend the
   whole left side of the block.
2. **Cauchy:** at the end, the right loops have a median weight of
   **0.983**; the 2 wrong ones have **0.0002** or less. The wrong loops
   are switched off, the right ones kept, and the error drops to 1.81 m.

Robust kernels do not replace checking loops. If many wrong loops agree
with each other, they can outweigh the right ones.


Beyond Feature Points
---------------------

ORB-SLAM is one design among several. Four other ideas, each in a widely
used system:

- **Direct methods** skip features and compare pixel brightness itself.
  DSO (Engel, Koltun and Cremers, 2018) "optimizes a photometric error
  defined directly on the images", and "Since our method does not depend
  on keypoint detectors or descriptors, it can naturally sample pixels from
  across all image regions that have intensity gradient": edges and soft
  texture count too.
- **A filter instead of a graph.** The MSCKF (Mourikis and Roumeliotis,
  2007) is an EKF with an IMU whose measurement model "does not require
  including the 3D feature position in the state vector of the EKF". The
  state holds the IMU and "a history of up to :math:`N_{max}` past poses of
  the camera", so the state stays small, unlike EKF-SLAM's.
- **Camera and IMU in one optimization.** VINS-Mono (Qin, Li and Shen, 2018)
  uses "a camera and a low-cost inertial measurement unit (IMU)", "the
  minimum sensor suite for metric six degrees-of-freedom (DOF) state
  estimation". It detects loops with DBoW2, like ORB-SLAM.
- **Learned front ends.** DROID-SLAM (Teed and Deng, 2021) "consists of
  recurrent iterative updates of camera pose and pixelwise depth through a
  Dense Bundle Adjustment layer": a trained network predicts how pixels
  move, and a bundle adjustment step inside the network turns that into
  poses and depth.

L6's comparison table also names ORB-SLAM3 (Campos et al., 2021), where
stereo or an IMU gives the map its scale.


LiDAR and Camera on the Same Route
----------------------------------

.. list-table::
   :widths: 34 33 33
   :header-rows: 1
   :class: compact-table

   * - Same route, two laps
     - 2-D LiDAR
     - Stereo camera
   * - Odometry, error at the end
     - 11.26 m scan to scan; 1.07 m scan to submap
     - 11.28 m frame to frame
   * - Odometry, RMSE
     - 7.10 m; 0.77 m
     - 7.72 m
   * - Loop candidates
     - 195 (Scan Context)
     - 341 (bag of words)
   * - Loops accepted
     - 163 (ICP)
     - 110 (PnP)
   * - Wrong loops accepted
     - 0
     - 2
   * - Pose graph, APE RMSE after
     - 0.24 m on scan to submap; 1.56 m on scan to scan, plain least squares
     - 9.73 m plain; 1.81 m with Cauchy weights

What the table says, for this simulated town:

- **Both front ends drift** about 11 m frame to frame. Matching against
  more than the last frame (the LiDAR's submap) cut that tenfold.
- **The camera's place recognition is less sure.** Similar façades make
  similar images. Its loops needed a robust back end; the LiDAR's did not.
- **Both back ends are the same code.** Only the edges differ, as L6 said:
  different front ends, one back end.

Our LiDAR is 2-D, in a flat town, and our camera images have no glare,
rain or night. On real streets, both front ends meet harder data.


What to Remember
----------------

- One image measures directions only. Depth comes from a second camera
  (:math:`Z = fb/d`), from motion (up to scale), or from an IMU.
- Stereo depth error grows with :math:`Z^2`: 0.36 m at 10 m but 5.79 m at
  40 m for 1 pixel of disparity error on our rig.
- ORB gives corners with 256-bit descriptors, compared by counting
  differing bits.
- PnP with RANSAC tracks the camera; our stereo odometry drifted 11.28 m
  over 914 m.
- A bag of words proposes loops; similar places score high too (0.728
  median against 0.892), so geometry must verify, and a robust back end
  must catch what slips through. On our drive, 2 wrong loops of 110 made
  plain least squares worse than no back end; Cauchy weights fixed it.


References
----------

- Agarwal, P., Tipaldi, G. D., Spinello, L., Stachniss, C. and Burgard, W.
  (2013). "Robust Map Optimization using Dynamic Covariance Scaling."
  *IEEE International Conference on Robotics and Automation (ICRA)*, 62 to
  69. `doi:10.1109/ICRA.2013.6630557 <https://doi.org/10.1109/ICRA.2013.6630557>`__
- Engel, J., Koltun, V. and Cremers, D. (2018). "Direct Sparse Odometry."
  *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 40(3),
  611 to 625. `doi:10.1109/TPAMI.2017.2658577 <https://doi.org/10.1109/TPAMI.2017.2658577>`__
- Gálvez-López, D. and Tardós, J. D. (2012). "Bags of Binary Words for Fast
  Place Recognition in Image Sequences." *IEEE Transactions on Robotics*,
  28(5), 1188 to 1197. `doi:10.1109/TRO.2012.2197158 <https://doi.org/10.1109/TRO.2012.2197158>`__
- Geiger, A., Lenz, P. and Urtasun, R. (2012). "Are we ready for Autonomous
  Driving? The KITTI Vision Benchmark Suite." *IEEE Conference on Computer
  Vision and Pattern Recognition (CVPR)*, 3354 to 3361.
  `doi:10.1109/CVPR.2012.6248074 <https://doi.org/10.1109/CVPR.2012.6248074>`__
- Hirschmüller, H. (2008). "Stereo Processing by Semiglobal Matching and
  Mutual Information." *IEEE Transactions on Pattern Analysis and Machine
  Intelligence*, 30(2), 328 to 341.
  `doi:10.1109/TPAMI.2007.1166 <https://doi.org/10.1109/TPAMI.2007.1166>`__
- Mourikis, A. I. and Roumeliotis, S. I. (2007). "A Multi-State Constraint
  Kalman Filter for Vision-aided Inertial Navigation." *IEEE International
  Conference on Robotics and Automation (ICRA)*, 3565 to 3572.
  `doi:10.1109/ROBOT.2007.364024 <https://doi.org/10.1109/ROBOT.2007.364024>`__
- Mur-Artal, R., Montiel, J. M. M. and Tardós, J. D. (2015). "ORB-SLAM: A
  Versatile and Accurate Monocular SLAM System." *IEEE Transactions on
  Robotics*, 31(5), 1147 to 1163.
  `doi:10.1109/TRO.2015.2463671 <https://doi.org/10.1109/TRO.2015.2463671>`__
- Nistér, D. (2003). "An Efficient Solution to the Five-Point Relative Pose
  Problem." *IEEE Conference on Computer Vision and Pattern Recognition
  (CVPR)*, 195 to 202. `doi:10.1109/CVPR.2003.1211470 <https://doi.org/10.1109/CVPR.2003.1211470>`__.
  The journal version: *IEEE Transactions on Pattern Analysis and Machine
  Intelligence*, 26(6), 756 to 770, 2004.
- Qin, T., Li, P. and Shen, S. (2018). "VINS-Mono: A Robust and Versatile
  Monocular Visual-Inertial State Estimator." *IEEE Transactions on
  Robotics*, 34(4), 1004 to 1020.
  `doi:10.1109/TRO.2018.2853729 <https://doi.org/10.1109/TRO.2018.2853729>`__
- Rosten, E. and Drummond, T. (2006). "Machine Learning for High-Speed
  Corner Detection." *Computer Vision, ECCV 2006*, Lecture Notes in Computer
  Science, 430 to 443. `doi:10.1007/11744023_34 <https://doi.org/10.1007/11744023_34>`__
- Rublee, E., Rabaud, V., Konolige, K. and Bradski, G. (2011). "ORB: An
  efficient alternative to SIFT or SURF." *International Conference on
  Computer Vision (ICCV)*, 2564 to 2571.
  `doi:10.1109/ICCV.2011.6126544 <https://doi.org/10.1109/ICCV.2011.6126544>`__
- Sünderhauf, N. and Protzel, P. (2012). "Switchable Constraints for Robust
  Pose Graph SLAM." *IEEE/RSJ International Conference on Intelligent Robots
  and Systems (IROS)*, 1879 to 1884.
  `doi:10.1109/IROS.2012.6385590 <https://doi.org/10.1109/IROS.2012.6385590>`__
- Teed, Z. and Deng, J. (2021). "DROID-SLAM: Deep Visual SLAM for
  Monocular, Stereo, and RGB-D Cameras." *Advances in Neural Information
  Processing Systems*, 34, 16558 to 16569.
  `NeurIPS page <https://proceedings.neurips.cc/paper/2021/hash/89fcd07f20b6785b92134bd6c1d0fa42-Abstract.html>`__
- Campos et al. (2021), ORB-SLAM3: cited through
  :doc:`L6's references </lectures/lecture6/l6_references>`.
