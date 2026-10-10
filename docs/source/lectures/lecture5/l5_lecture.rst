====================================================
Lecture
====================================================

.. note::

   These notes follow the **main deck** of L5, the slides shown in class and
   the reading slides that go with them, in the same order and with the same
   sections. They add what the speaker notes say aloud, so you can read them
   at home. Material the deck keeps in its appendix (inside CenterPoint, one
   pixel onto the grid, Lift and Splat by hand, BEVFormer, the match distance
   with the math, and tracking in industry) is on :doc:`the appendix page
   <l5_appendix>`, "Going Further".


.. _l5-lec-introduction:

Introduction
------------

What L4 Left Missing
~~~~~~~~~~~~~~~~~~~~

Last week ended with a detector. It puts a box, a class and a confidence
around each object, but the box is in **pixels**, in **one image**, at **one
instant**. L4 also made a table of what perception hands to the rest of the
AV. Each row of that table is a reason for one of today's sections.

.. list-table::
   :widths: 28 18 30 24
   :header-rows: 1
   :class: compact-table

   * - **Output (L4's table)**
     - **Used by**
     - **Still missing after L4**
     - **Today**
   * - Objects: position, size, heading
     - prediction, planning
     - meters, not pixels
     - 1. 3D Detection
   * - Objects: speed
     - prediction, planning
     - the same object, frame to frame
     - 5. Tracking
   * - Drivable area, lanes
     - planning, control
     - the road itself, in meters
     - 2. Segmentation, 3. BEV
   * - Occupancy (L4: "which parts of the ground are taken")
     - planning
     - space taken by things with no class
     - 3. Occupancy
   * - All of the above
     -
     - one answer from camera, LiDAR and radar
     - 4. Fusion

- **Objects.** Prediction and planning need each object's position, size and
  heading in meters, not pixels. That is 3D detection. They also need each
  object's speed, and a speed needs the same object from one frame to the
  next. That is tracking.
- **The drivable area and the lanes.** The planner needs the road itself, in
  meters. That is segmentation, then the view from above, the **bird's-eye
  view** (BEV). L4 also promised **occupancy**: which parts of the ground are
  taken, by anything at all.
- **One answer.** Every row has to come as one answer, although the AV has a
  camera, a LiDAR and a radar. That is fusion.
- **Not today.** L4's fourth output, lights and signs, is not covered. L4's
  detector boxes the light, and reading its color is one more step.


.. _l5-lec-waymo:

Waymo's Driver, as Waymo Describes It
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before the sections, here is a real driver, as far as its maker describes it.
This is Waymo's architecture, as Waymo described it in a December 2025 post.
The drawing is ours; the block names and the outputs are Waymo's. Three terms
come first:

- An **encoder** is a network that turns raw inputs into features, the
  numbers from L4.
- A **VLM**, vision-language model, is a network trained on images and text
  together.
- A **decoder** is a network that turns features into outputs.

.. figure:: /_static/images/L5/waymo_stack.png
   :alt: A block diagram. Cameras, LiDAR and radar feed the Sensor Fusion Encoder, labeled think fast, which fuses all three over time into objects, semantics and embeddings; it is highlighted green and labeled today. Cameras also feed the Driving VLM, labeled think slow, tagged L12. Both feed the World Decoder, which outputs behavior predictions, high-definition maps, trajectories for the vehicle and validation signals, tagged L9 and L10. Its trajectories go to an onboard validation layer.
   :width: 90%
   :align: center

   Waymo's architecture, redrawn from Waymo's December 2025 post. Cameras,
   LiDAR and radar feed the **Sensor Fusion Encoder** ("think fast", today,
   in green). Cameras also feed the **Driving VLM** ("think slow", L12). Both
   feed the **World Decoder** (L9 and L10), and an **onboard validation
   layer** checks what it outputs.

- Cameras, LiDAR and radar go into one learned block, the **Sensor Fusion
  Encoder**, the part that "thinks fast".
- The **Driving VLM**, the part that "thinks slow", reads the cameras for
  rare and complex scenes. That is L12.
- The **World Decoder** predicts what others will do and plans the AV's path:
  L9 and L10. A separate validation layer checks the planned path.


.. _l5-lec-waymo-post:

What Waymo's Post Does and Does Not Say
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Sensor Fusion Encoder, the green block, is the part that does
perception. Waymo describes it in one sentence: it "fuses camera, lidar, and
radar inputs over time, producing objects, semantics, and rich embeddings for
downstream tasks". Read it piece by piece:

.. list-table::
   :widths: 42 58
   :header-rows: 1
   :class: compact-table

   * - **The encoder, in Waymo's words**
     - **What the post does and does not say**
   * - "fuses camera, lidar, and radar inputs"
     - sensor fusion: the Fusion section's job
   * - "over time"
     - inputs from several frames; tracking is not mentioned
   * - "objects, semantics"
     - elsewhere: "objects, semantic attributes, and roadgraph elements"
   * - "rich embeddings"
     - "a rich interface between model components"

The embeddings are learned features passed between Waymo's networks.

.. important::

   **The post never mentions tracking, BEV, occupancy or segmentation.** Waymo
   does not publish how the encoder works inside, so we cannot say which of
   today's methods it uses. For a stack where every job is a named module,
   look at Autoware, next.


.. _l5-lec-autoware:

Autoware: Each Job a Separate Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Waymo does not publish its internals. **Autoware**, the open-source AV
software, does. The figure is its reference perception design, redrawn and
simplified from its documentation.

**How to read it:** data flows from sensing at the top to planning at the
bottom, and each box is a separate program. A green tag gives the section of
this lecture that teaches that box: 1 3D Detection, 2 Segmentation, 3 BEV and
Occupancy, 4 Fusion, 5 Tracking.

.. figure:: /_static/images/L5/perception_stack.png
   :alt: A block diagram. Sensing, camera images, LiDAR point clouds and radar objects, feeds four parts. Obstacle segmentation and the occupancy grid map exchange data, and each sends its output to planning: obstacles and blind spots. A Detection group holds a 3D detector, tagged 1 and 3; camera 2D detection with projection fusion, tagged 2 and 4; and a radar pipeline. All three feed a multi-object tracker, tagged 5, then prediction, tagged L9, which sends dynamic objects to planning. The occupancy grid map is tagged 3. Traffic light recognition runs on its own and also feeds planning.
   :width: 80%
   :align: center

   Autoware's perception, simplified. **Sensing** feeds everything. On the
   left, **obstacle segmentation** and the **occupancy grid map** (tag 3) send
   obstacles and blind spots to planning. In the middle, the **Detection**
   group: a 3D detector (tags 1 and 3), camera 2D detection with projection
   fusion (tags 2 and 4) and a radar pipeline, all feeding the
   **multi-object tracker** (tag 5), then **prediction** (L9). Traffic light
   recognition feeds planning on its own.

- **On the left,** obstacle segmentation picks the LiDAR points that belong
  to obstacles. It is not the image segmentation of section 2. The occupancy
  grid map, section 3, marks blind spots. Both go straight to planning.
- **In the middle,** detection runs three pipelines. The **3D detector**,
  sections 1 and 3: Autoware's list includes CenterPoint and BEVFusion, both
  on a grid seen from above. **Camera detection with projection fusion**,
  sections 2 and 4: Autoware combines the LiDAR points with the camera's 2D
  detections or with its semantic segmentation. And **radar**.
- All three feed one **multi-object tracker**, section 5. Prediction, L9,
  follows, and the objects go to planning.

.. note::

   **Two words that mean something else here.** Autoware's **obstacle
   segmentation** picks the LiDAR points that belong to obstacles; it is not
   image segmentation. Autoware's **occupancy grid** is a 2D grid built from
   LiDAR, while section 3 also covers learned 3D occupancy from cameras.


.. _l5-lec-sa:

Situation Awareness in the AV's Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The idea comes from human factors research, from Mica Endsley, who defined it
in 1988 and built her model of it in 1995. Her definition has three parts,
and each part is one level.

.. admonition:: Definition: situation awareness (SA)
   :class: note

   "the perception of the elements in the environment within a volume of time
   and space, the comprehension of their meaning and the projection of their
   status in the near future" (Endsley, 2000). Also called situational
   awareness.

.. figure:: /_static/images/L5/sa_pipeline.png
   :alt: L4's pipeline: Sensors (L2), Perception (L4, L5, highlighted), Prediction (L9), Planning (L10) and Control (L11), joined by arrows, with a curved arrow from Perception straight to Planning labeled drivable area, lanes, lights. Braces above: Level 1 perception and Level 2 comprehension over Perception; Level 3 projection over Prediction; a larger brace labeled Situation awareness over both. A dashed line separates them from Decision over Planning and Action over Control, labeled outside awareness.
   :width: 80%
   :align: center

   Endsley's levels over L4's pipeline. **Level 1** (perception) and **Level
   2** (comprehension) sit over Perception (L4, L5); **Level 3**
   (projection) over Prediction (L9). Together they are **situation
   awareness**. Past the dashed line, outside awareness: **Decision** over
   Planning (L10) and **Action** over Control (L11). The curved arrow carries
   the drivable area, the lanes and the lights straight to planning.

- **Level 1, perception:** what is around the AV and where. It sits over the
  perception box.
- **Level 2, comprehension:** which object is which, and what each one is
  doing. It starts in perception too: that is tracking, the last section
  today.
- **Level 3, projection:** where each object will be in the next few
  seconds. That is the prediction box, L9.

**In the AV's terms,** for a car cutting in ahead (car B, next section):
Level 1 is a car 12 m ahead and 2 m to the right. Level 2 is the same car as
on the last sweep, turning toward the AV's lane. Level 3 is where it will be
in the next seconds.

Endsley's model shows SA "as a stage separate from decision making and
performance". So the dashed line is where awareness ends: planning is the
decision (L10) and control is the action (L11). Planning and control use the
picture; they are not part of it. A planner can only be as good as the
picture it is given.

The curved arrow carries the drivable area, the lanes and the lights from
perception straight to planning, with no prediction. They are Level 1
information, used directly.

**Today:** Level 1, and Level 2 through tracking.


.. _l5-lec-objectives:

Learning Objectives
~~~~~~~~~~~~~~~~~~~

By the end of this lecture, you will be able to:

- Read a **3D box** and say why LiDAR detectors work on a view from above.
- Say what **semantic** segmentation gives the planner, and why the road is
  segmented from above.
- Explain why the **bird's-eye view** helps, and what **occupancy** adds to
  boxes.
- Place a design in **early**, **intermediate** or **late** fusion, and
  project a LiDAR point into a camera box by hand.
- Run one cycle of a **multi-object tracker**: predict, gate, associate, and
  manage the track lifecycle.

There is one objective per section. Two of them you do by hand: projecting a
LiDAR point into a camera box, and one cycle of a tracker. Both use tools from
earlier lectures: the camera model from L2 and the Kalman filter from L3.


.. _l5-lec-3d:

3D Detection
------------

- **Where we are:** every box in L4 is in **pixels**, in one image.
- **In this section:** boxes in **meters** around the AV: 3D detection,
  mostly from LiDAR.
- **What it is for:** the planner and the tracker, which need where an
  object is on the road, not in the image.

A box in pixels says where a person is in the picture. The planner, and the
tracker at the end of today, need where the person is on the road, in
meters, and which way they are heading. And from L2, one camera cannot
measure depth directly.

.. admonition:: Definition: 3D box
   :class: note

   An object's center :math:`(x, y, z)` in meters, in the AV's frame
   (:math:`x` forward, :math:`z` up, :math:`y` sideways: right in CARLA, left
   in ROS); its size (length, width, height); and its heading
   :math:`\theta`, the angle from the AV's :math:`x` axis to the way the
   object faces, measured counterclockwise seen from above. That is 7
   numbers; many detectors add a velocity :math:`(v_x, v_y)`, for 9.

.. warning::

   **Watch** :math:`y`. In CARLA it points right; in ROS it points left. This
   is the axis trap from L2.

Who produces these boxes? The AV's **3D detector**, for example CenterPoint,
which Autoware runs and which comes later in this section. It reports one box
per object on every LiDAR sweep. We do not run one in class. From here on,
"the detector" means this 3D detector.


.. _l5-lec-box3d:

Reading a 3D Box: a Car Cutting In
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** The AV drives in its lane, 3.5 m wide. Ahead, a car, which we
call **car B**, leaves the right lane and turns toward the AV's lane. The
planner must decide now, brake or keep going: **how far into the AV's lane
does car B reach?** We follow car B through the whole lecture: its LiDAR
points, its cell on the grid from above, its points in a camera box, and its
track.

**What the AV has.** On every LiDAR sweep, the detector reports one box per
object in the AV's frame (:math:`x` forward, :math:`y` left). Car B's box
(values chosen for this example; in a real AV the detector computes them from
the points, on every sweep):

- center :math:`(12.0, -2.0)` m: 12 m ahead and 2 m to the right, minus
  because :math:`y` points left;
- size :math:`4.5 \times 1.9 \times 1.5` m;
- heading :math:`\theta = 30^\circ`, turned toward the AV's lane.

.. figure:: /_static/images/L5/box3d.png
   :alt: A top view, x forward to the right, y to the left, up the page. Two lanes: the AV's lane on top, with the AV at the origin facing +x and its centerline dashed, and the right lane below, separated by a dashed lane line. Car B, a light blue car drawn inside a dark blue box, centered at (12.0, -2.0), straddles the lane line, turned 30 degrees toward the AV's lane; an arrow marks its heading and the angle theta = 30 degrees.
   :width: 60%
   :align: center

   Car B from above. The AV is at the origin, facing :math:`+x`, in the top
   lane. Car B's box, centered at :math:`(12.0, -2.0)`, straddles the lane
   line, turned :math:`\theta = 30^\circ` toward the AV's lane.

**Car B is already in the AV's lane, even before we use the heading.**
Pointing straight, its left side would be at
:math:`y = -2.0 + 0.95 = -1.05` m: the center is 2 m right of the
centerline, and half of the 1.9 m width is 0.95 m. The lane edge is at 1.75
m, so that side would already be :math:`1.75 - 1.05 = 0.70` m into the AV's
lane.

Turned :math:`30^\circ`, car B's front reaches farther. The next two
subsections take the heading and the size and find the car's front-left
corner. The 7 numbers come from a trained network, on every sweep:
PointPillars and CenterPoint, later in this section.


.. _l5-lec-corner-dirs:

Finding the Corner: Two Directions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The question is still how far into the AV's lane car B reaches. Car B turns
left, toward that lane, so the corner to check is its **front-left corner**.
All we have is the detector's numbers: :math:`C = (12.0, -2.0)`,
:math:`l = 4.5` m, :math:`w = 1.9` m, :math:`\theta = 30^\circ`.

From the center :math:`C`, we move along two directions, each a vector of
length 1:

1. **Forward**, along the heading:

   .. math::

      \text{front center} = C + \tfrac{l}{2}(\cos\theta,\ \sin\theta)

2. **Left**, the heading turned :math:`90^\circ` counterclockwise:

   .. math::

      \text{front-left} = \text{front center} + \tfrac{w}{2}(-\sin\theta,\ \cos\theta)

A number times a vector multiplies each part:
:math:`\tfrac{l}{2}(\cos\theta,\ \sin\theta) = (\tfrac{l}{2}\cos\theta,\ \tfrac{l}{2}\sin\theta)`.

.. figure:: /_static/images/L5/corner_dirs.png
   :alt: Car B from above, a light blue car in a dark blue box turned by the heading angle theta from the x axis; an axis key shows x to the right and y, left, up. From the center C, a green arrow goes forward along the heading, half the length, to the front center, labeled l/2 forward, (cos theta, sin theta). From there an orange arrow goes half the width to the left, labeled then w/2 left, (minus sin theta, cos theta), and ends at the front-left corner, a red dot.
   :width: 50%
   :align: center

   The two directions. From the center :math:`C`, the **green arrow** goes
   half a length forward, to the front center. From there the **orange
   arrow** goes half a width to the left, to the **front-left corner** (red
   dot).


.. _l5-lec-corner-steps:

Step by Step: the Car's Front-Left Corner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Computed by hand from car B's numbers: :math:`C = (12.0, -2.0)`,
:math:`l/2 = 2.25` m, :math:`w/2 = 0.95` m, :math:`\theta = 30^\circ`.

1. **Front center.** :math:`2.25 \cos 30^\circ = 1.949` and
   :math:`2.25 \sin 30^\circ = 1.125`:

   .. math::

      F = C + \tfrac{l}{2}(\cos\theta,\ \sin\theta)
        = (12.0 + 2.25\cos 30^\circ,\ -2.0 + 2.25 \sin 30^\circ)
        = (13.95,\ -0.875)

2. **Front-left corner.** Left of a heading of :math:`30^\circ` means minus
   sine in :math:`x` and plus cosine in :math:`y`: :math:`-0.475` and
   :math:`+0.823`.

   .. math::

      P = F + \tfrac{w}{2}(-\sin\theta,\ \cos\theta)
        = (13.95 - 0.95\sin 30^\circ,\ -0.875 + 0.95 \cos 30^\circ)
        = (\mathbf{13.47},\ \mathbf{-0.05})

3. **How far in.** :math:`y = -0.05`: the corner is 5 cm from the AV's
   centerline, so it is :math:`1.75 - 0.05 =` **1.70 m** into the AV's lane,
   13.5 m ahead.

.. figure:: /_static/images/L5/corner_steps.png
   :alt: Car B from above, a light blue car in a dark blue box turned by theta; the AV's centerline y = 0 is a dashed gray line above it; an axis key shows x to the right and y, left, up. Marker 1: a green arrow from the center C along the heading to the front center F. Marker 2: an orange arrow from F to the left, ending at marker 3, the front-left corner, a red dot right on the centerline.
   :width: 52%
   :align: center

   The three steps. **1**: the green arrow from :math:`C` to the front
   center :math:`F`. **2**: the orange arrow from :math:`F` to the left.
   **3**: the front-left corner, which sits on the AV's centerline,
   :math:`y = 0`.

Pointing straight, car B would reach 0.70 m into the AV's lane; turned, it
reaches 1.70 m.

.. important::

   A box in pixels could not tell the planner this; the heading and the size
   in meters can.


.. _l5-lec-detector-strip:

How the Detector Gets Car B's Box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far, car B's box was given: the detector reported it, and we used it to
find how far car B reaches into the AV's lane. Now we open the detector, from
its input to its output. Each part answers one question, on the subsections
named under it in the figure.

.. figure:: /_static/images/L5/detector_strip.png
   :alt: Three panels joined by arrows. 1, Input: LiDAR points: a sketch of one sweep, gray points around and blue points on car B's rear and left side; under it, how many points reach car B?, LiDAR points thin out, Step by step: rings. 2, Network: a grid seen from above with a few filled cells, labeled pillars, seen from above, then an arrow to a box labeled 2D CNN (L4); under it, how does a network read a list of points?, Three ways to read, PointPillars. 3, Output: the box: car B, a light blue car in a dark blue box with a heading arrow, labeled center (x, y, z), l times w times h, heading theta; under it, how does it read off the 7 numbers?, CenterPoint.
   :width: 95%
   :align: center

   The detector in three parts, drawn as sketches. **1. Input:** the LiDAR
   points, blue on car B. **2. Network:** pillars seen from above, then a 2D
   CNN (L4). **3. Output:** car B's box, its 7 numbers.

- **Input.** The input is the LiDAR's points. The first question is how many
  of them even reach car B: :ref:`l5-lec-lidar-thin` and
  :ref:`l5-lec-rings`.
- **Network.** A network has to read a list of points. The method that works
  is to turn them into a grid seen from above, pillars, so the 2D networks of
  L4 apply: :ref:`l5-lec-point-forms` and :ref:`l5-lec-pointpillars`.
- **Output.** The network reads off car B's 7 numbers: that is CenterPoint,
  :ref:`l5-lec-centerpoint`.


.. _l5-lec-lidar-thin:

LiDAR Points Thin Out with Distance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** Before the detector can report car B, it has to recognize car
B from the LiDAR points that hit it. **The question:** how many rings of
points land on car B at 12 m, and on the same car at 50 m (a distance chosen
for comparison)?

**What we have.** A spinning LiDAR has **channels**: lasers stacked at fixed
vertical angles. As it turns, each channel traces one **ring** of points.

- We take **64 channels** (chosen; CARLA's default is 32, which would halve
  every count below).
- They are spread evenly from the highest laser at :math:`+10^\circ` to the
  lowest at :math:`-30^\circ` (CARLA's defaults), a :math:`40^\circ` span.
- Car B is 1.5 m tall (its box).

.. figure:: /_static/images/L5/lidar_channels.png
   :alt: Left, a side view at true scale, x in meters from the LiDAR: the AV on the road with its LiDAR on the roof, 1.8 m up at x = 0; a fan of beams, every 8th of the 64 channels, from 10 degrees up to 30 degrees down; the four steepest are drawn in red, magenta, violet and teal and hit the road within 7 m, the others in orange. A thick green mark between two neighboring drawn beams at x = 12 m is labeled gap at 12 m; a green arrow between the same two beams at x = 50 m is labeled at 50 m, 50/12 = 4.2 times wider. Right, from above: the AV inside four dotted circles in the same four colors, labeled minus 30 degrees, 3.1 m; minus 25.6 degrees, 3.8 m; minus 20.5 degrees, 4.8 m; minus 15.4 degrees, 6.5 m; captioned steeper channels hit the road closer, one ring each.
   :width: 100%
   :align: center

   **Left, from the side**, at true scale: every 8th of the 64 channels,
   leaving the LiDAR (1.8 m up) at fixed angles. The gap between two
   neighboring beams at 50 m is :math:`50/12 = 4.2` times the gap at 12 m.
   **Right, from above:** each steep channel meets the road in one ring, in
   the same colors: :math:`-30^\circ` at 3.1 m, :math:`-25.6^\circ` at 3.8 m,
   :math:`-20.5^\circ` at 4.8 m, :math:`-15.4^\circ` at 6.5 m.

- Each channel leaves the LiDAR at its own angle, and the lower ones hit the
  road close to the AV.
- As the LiDAR spins, each channel sweeps a cone, and where it meets the
  ground it draws a ring around the AV. A steeper channel hits the road
  closer: the red one, :math:`30^\circ` down, at 3.1 m; the teal one,
  :math:`15.4^\circ` down, at 6.5 m. The rings sit one inside the other, one
  per channel.
- Because the angles are fixed, two neighboring beams spread apart as they go
  out. **The gap between rings grows with distance, so a far car gets fewer
  rings.**


.. _l5-lec-rings:

Step by Step: Rings on Car B
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Computed by hand from the numbers above: 64 channels over :math:`40^\circ`,
car B 1.5 m tall, at 12 m and at 50 m.

1. **Angle between neighboring channels:**

   .. math::

      \frac{40^\circ}{64 - 1} = 0.635^\circ

2. **Gap on the car.** Picture a wall :math:`d` meters away. Two neighboring
   channels hit it :math:`d \tan 0.635^\circ` apart in height, one above the
   other:

   .. math::

      \text{on car B at 12 m: } 12 \times 0.01108 = \mathbf{0.133}\ \text{m}
      \qquad \text{at 50 m: } 50 \times 0.01108 = \mathbf{0.554}\ \text{m}

   Each ring crosses car B's back as a horizontal line, so the back gets a
   stack of lines that far apart.

3. **Ring lines on car B's back,** 1.5 m tall: its height over the gap.

   .. math::

      \text{at 12 m: } \frac{1.5}{0.133} = 11.3, \text{ so } \mathbf{11 \text{ or } 12}
      \qquad \text{at 50 m: } \frac{1.5}{0.554} = 2.7, \text{ so } \mathbf{2 \text{ or } 3}

   A count of lines cannot be a fraction. Which of the two it is depends on
   where the first line lands on the car.

A detector has to call that far car a car from 2 or 3 rings, a handful of
points.


.. _l5-lec-near-far:

The Same Car, Near and Far: LiDAR and Camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here are the counts drawn, with car B as the AV's sensors see it: from behind
and to its left, because it is turned :math:`30^\circ` toward the AV's lane.
All three drawings are to the same scale.

.. figure:: /_static/images/L5/lidar_rings.png
   :alt: Three drawings of car B, a light blue car seen from behind and to its left, its left side and two left wheels on the left and its rear, with a tail-light band, on the right; a 1.5 m height marker on the left. Left, LiDAR, car B at 12 m: thin orange horizontal ring lines cross the car, captioned 11 or 12 rings, 0.133 m apart. Middle, LiDAR, the same car at 50 m: 3 orange lines, captioned 2 or 3 rings, 0.554 m apart. Right, camera, the same car at 50 m: the car covered by 19 alternating dark and light horizontal bands, captioned 19 rows of pixels.
   :width: 92%
   :align: center

   Car B, 1.5 m tall. **Orange lines:** LiDAR rings. **Gray bands:** rows of
   camera pixels, shaded in turn. **Left:** LiDAR at 12 m, 11 or 12 rings,
   0.133 m apart. **Middle:** LiDAR at 50 m, 2 or 3 rings, 0.554 m apart.
   **Right:** the camera at 50 m, 19 rows of pixels.

The camera's count comes from the camera model of L2. An image 1280 px wide
with a :math:`90^\circ` field of view has :math:`f = 640` px, so the car at
50 m covers :math:`640 \times 1.5 / 50 =` **19** rows.

.. admonition:: Why the AV fuses its sensors
   :class: tip

   LiDAR measures distance well and sees little far away. The camera sees
   detail and guesses distance. That is why the AV **fuses** them
   (:ref:`l5-lec-fusion`).


.. _l5-lec-point-forms:

Three Ways to Read a Point Cloud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The question.** The LiDAR hands the detector car B's points as a **list**
of :math:`(x, y, z)` points, in no particular order: dense near the AV and
almost empty far away, as the last subsections showed. The CNNs of L4 need a
grid, where every pixel has neighbors at known places. How does a network
read a list?

It uses one of three forms. The figure draws them on car B seen from the
side, 10 m ahead of the AV's LiDAR (1.8 m up, 64 channels). We traced each of
the 64 channels: a point lands where a beam first hits car B or the road.
That gives 16 points, almost all on the rear of the car, the face turned
toward the AV.

.. figure:: /_static/images/L5/point_forms.png
   :alt: Three side views of car B, a light blue car with its rear toward the AV, which is off to the left, and the same 16 black LiDAR points: a vertical stack on the car's rear, a few on its rear deck and roof, and three on the road in front of it. Points: the dots alone, captioned the 16 points themselves, PointNet. Voxels: a grid of 0.5 m squares over the car, the 9 squares that hold a point filled green, captioned 9 of 52 cubes hold a point, VoxelNet, SECOND. Pillars: full-height orange columns over the 6 ground cells that hold a point, captioned 6 of 13 columns hold a point, PointPillars.
   :width: 95%
   :align: center

   The same 16 points on car B, three ways. **Points:** the points
   themselves (PointNet). **Voxels:** 0.5 m cubes; 9 of 52 hold a point
   (VoxelNet, SECOND). **Pillars:** one column per patch of ground, any
   height; 6 of 13 hold a point (PointPillars).

- **Points:** the network reads the list itself.
- **Voxels:** cut space into half-meter cubes and keep the ones that hold a
  point, 9 of 52. Most are empty.
- **Pillars:** one column per patch of ground, any height, 6 of 13.

**The trade:** pillars are faster; voxels keep detail in height. CenterPoint,
later in this section, can sit on either voxels or pillars.


.. _l5-lec-point-forms-papers:

The Three Forms, in the Papers' Words
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What each network does with the point cloud, from the papers:

.. list-table::
   :widths: 18 82
   :header-rows: 1
   :class: compact-table

   * - **Form**
     - **How the network reads it**
   * - **Points** (PointNet, Qi et al., 2017)
     - reads the list itself; it "directly consumes point clouds" and is built
       so that shuffling the list does not change its answer
   * - **Voxels** (VoxelNet, Zhou and Tuzel, 2018; SECOND, Yan et al., 2018)
     - cuts space into "equally spaced 3D voxels", small cubes, then runs 3D
       convolutions; **sparse** convolution computes only the cubes that hold
       points
   * - **Pillars** (PointPillars, next)
     - one column per ground cell, any height: the result is a 2D grid, so 2D
       convolutions apply

Most voxels are empty, so SECOND uses **sparse convolution**, which computes
only where there are points. That made voxel networks fast.


.. _l5-lec-pointpillars:

PointPillars: from Points to 3D Boxes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: PointPillars
   :class: note

   A LiDAR detector (Lang et al., 2019): it groups one sweep's points into
   **pillars** on a grid seen from above, turns them into an image of
   features, and runs the 2D networks of L4 on it. Its head, "the Single Shot
   Detector (SSD) setup", outputs each object's 7 numbers.

**The question:** from one sweep's **point cloud**, the :math:`(x, y, z)`
points, each with an intensity (how strongly it reflected), get car B's 7
numbers, on every sweep. LiDAR measures distance directly, so it is the
natural sensor for boxes in meters. PointPillars, from 2019, is the classic
way, and still a common baseline. **Every weight in PointPillars is set by
training.**

.. figure:: /_static/images/L5/pointpillars_steps.png
   :alt: Six panels joined by arrows, each a sketch seen from above, with an x and y key in the first. LiDAR points: car B, a faint light blue car turned 30 degrees, with its points in blue along its rear and its left side, and two gray points elsewhere. Step 1: pillars, one per cell: the same car and points under a 5 by 5 grid, the cells that hold points shaded orange. Step 2: one vector per pillar: one cell's points become a short column of numbers. Step 3: pseudo-image from above: the grid with each occupied cell in its own shade, car B faint underneath. Step 4: 2D CNN, then a head (SSD): a stack of shrinking feature maps, then two dashed preset boxes, at 0 and 90 degrees, on one cell. Output: car B's box, 7 numbers: car B as a light blue car in its dark blue box.
   :width: 100%
   :align: center

   PointPillars, Steps 1 to 4, from car B's LiDAR points (blue) to its box.
   **Step 1:** pillars, one per cell. **Step 2:** one vector per pillar.
   **Step 3:** a pseudo-image from above. **Step 4:** a 2D CNN, then a head
   (SSD). The small brace marks the head alone: the part CenterPoint
   replaces.


.. _l5-lec-pointpillars-steps:

PointPillars, Step by Step
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 18 82
   :header-rows: 0
   :class: compact-table

   * - .. image:: /_static/images/L5/pp_step1.png
          :alt: Step 1: a 5 by 5 grid seen from above over car B, a faint light blue car, and its LiDAR points in blue along its rear and left side; the cells that hold points are shaded orange.
          :width: 100%
     - **Step 1.** "The point cloud is discretized into an evenly spaced grid
       in the :math:`x`-:math:`y` plane, creating a set of **pillars**" (Lang
       et al., 2019): cells of :math:`0.16 \times 0.16` m on the ground. Each
       grid square collects every point above it: a pillar is a column of
       points.
   * - .. image:: /_static/images/L5/pp_step2.png
          :alt: Step 2: one orange cell with three blue points, an arrow, then a short column of four shaded numbers.
          :width: 100%
     - **Step 2.** A small network turns the points in each pillar into
       **one feature vector**.
   * - .. image:: /_static/images/L5/pp_step3.png
          :alt: Step 3: the same 5 by 5 grid, each occupied cell in its own shade of orange, car B faint underneath.
          :width: 100%
     - **Step 3.** Each vector sits at its cell: together they form a
       **pseudo-image**, an image of features seen from above. Each pillar is
       one pixel of it.
   * - .. image:: /_static/images/L5/pp_step4.png
          :alt: Step 4: a stack of three shrinking gray feature maps, an arrow, then two dashed preset boxes, at 0 and 90 degrees, on one cell.
          :width: 100%
     - **Step 4.** An image seen from above is still an image, so a 2D CNN
       (L4) reads it. Then the head, "the Single Shot Detector (SSD) setup",
       tries **preset boxes**, called **anchors**, of fixed shapes and angles
       at every cell, and keeps those that match an object, corrected to its
       7 numbers.

**Speed,** from the paper: 62 frames per second on an NVIDIA 1080 Ti GPU, on
KITTI, a driving benchmark recorded in Karlsruhe, Germany.

**Next:** CenterPoint keeps Steps 1 to 3 and the 2D CNN, and replaces the
head.


.. _l5-lec-centerpoint:

CenterPoint, Step 4a: a Heatmap per Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The question is the same: on the view from above, where exactly is car B, and
what are its 7 numbers? CenterPoint, from 2021, answers it by treating objects
as points.

.. admonition:: Definition: CenterPoint
   :class: note

   A detection head (Yin et al., 2021) that replaces the head of Step 4: it
   "rel[ies] on existing 3D backbones (VoxelNet or PointPillars)", finds each
   object as the peak of a heatmap, and reads its box at that peak (Steps 4a
   to 4c).

CenterPoint is a head, not a whole detector. The points still go through
pillars, the pseudo-image and the 2D CNN, and CenterPoint reads those
features. That is why its steps are 4a, 4b and 4c: a heatmap, its peaks, and
the box read at each peak.

**Step 4a.** From the backbone's features, the head predicts one **heatmap**
per class: car, truck, pedestrian, and so on. Each cell holds a number from 0
to 1: how likely it is that an object of that class has its center in that
cell.

**How it knows "car":** in training, the car heatmap is shown a bump "at the
center location" of every labeled car. The network learns to reproduce those
bumps from the features: the size and the shape of the points seen from
above. After training, a peak in the car heatmap means a car.

.. figure:: /_static/images/L5/centerpoint_step1.png
   :alt: Left, a stack of gray feature maps labeled features from the backbone, PointPillars without its head, or VoxelNet, with an arrow labeled head to a stack of heatmaps, one per class: truck and pedestrian behind, car in front. The car heatmap is a top view on a faint grid with the AV at the left and, around car B, a square patch of red cells, darkest in the middle, labeled around car B, darker, a center is more likely, each cell from 0 to 1.
   :width: 76%
   :align: center

   Step 4a. The **head** turns the backbone's features (PointPillars without
   its head, or VoxelNet) into one heatmap per class: car, truck,
   pedestrian, and more. On the **car** heatmap, the cells around car B are
   darker: a center is more likely there. The heatmap is drawn for this
   example, not computed by a network.


.. _l5-lec-centerpoint-4b:

CenterPoint, Step 4b: Each Peak Is One Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Finding the objects:** a **peak** is a cell whose value is higher than all
of its neighbors. Each peak is the center of one object. For car B, the peak
sits at :math:`(12.0, -2.0)` m, its center from the 3D box above.

.. figure:: /_static/images/L5/centerpoint_step2.png
   :alt: The same heatmap with a dark red dot on its darkest cell, labeled the peak, a cell higher than all its neighbors, car B's center, (12.0, -2.0).
   :width: 92%
   :align: center

   Step 4b. The **peak**, the dark red dot, is a cell higher than all its
   neighbors: car B's center, :math:`(12.0, -2.0)`.

There are no preset boxes, unlike PointPillars' SSD head in Step 4: a car
turning at :math:`45^\circ` is still one peak. That is one reason CenterPoint
caught on.


.. _l5-lec-centerpoint-4c:

CenterPoint, Step 4c: Read the Box at the Peak
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The rest of car B's numbers.** At the peak's cell, more outputs of the
network give the size, the heading and the velocity. With the center from
Step 4b, that is the full box: car B's 7 numbers, plus its velocity.

.. figure:: /_static/images/L5/centerpoint_step3.png
   :alt: The same heatmap and peak, now with car B's dark blue box, turned 30 degrees, around the peak, and a green arrow along its heading labeled velocity 4.0 m/s. A label reads: read at the peak, size 4.5 by 1.9 by 1.5 m, heading 30 degrees as sine and cosine, velocity 4.0 m/s.
   :width: 92%
   :align: center

   Step 4c. Read at the peak: size :math:`4.5 \times 1.9 \times 1.5` m,
   heading :math:`30^\circ` as :math:`(\sin\theta, \cos\theta)`, velocity
   4.0 m/s (green arrow). Around the peak, car B's box.

**Why** :math:`(\sin\theta, \cos\theta)`: :math:`359^\circ` and
:math:`1^\circ` are neighbors but far apart as numbers; their sines and
cosines are close.

The values shown are car B's chosen ones, the numbers the 3D box started
from. The 4.0 m/s is the speed car B's track uses in :ref:`l5-lec-tracking`.

.. tip::

   See "Inside CenterPoint" in :doc:`Going Further <l5_appendix>`: how the
   heads are read, and how velocity comes from two frames.


.. _l5-lec-3d-industry:

3D Detection in Industry
~~~~~~~~~~~~~~~~~~~~~~~~

Which of these detectors run in real AV software, from each maker's own
documentation. **TensorRT** (L4) is NVIDIA's engine that runs a trained
network fast. **Orin** is NVIDIA's computer for cars.

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - **Who**
     - **What they use, from their own documentation**
   * - **Autoware** (open-source AV software)
     - ``autoware_lidar_centerpoint``: "CenterPoint uses a PointPillars-based
       network to inference with TensorRT", trained on nuScenes (about 28k
       LiDAR frames) and TIER IV's own (about 11k).
   * - **Baidu Apollo**
     - "centerpoint, maskpillars, pointpillars, cnnseg"; since release 9.0
       CenterPoint is the default LiDAR model.
   * - **NVIDIA**
     - PointPillars in TensorRT: **6.84 ms** per frame on an Orin, the in-car
       computer. CenterPoint: 65.64 NDS at 23 frames per second on Orin.
   * - **Waymo**
     - Its open dataset: 12.6 million labeled 3D boxes, with tracking IDs, and
       a public 3D detection leaderboard.

- **Autoware**, the open-source AV software stack that many companies build
  on, runs CenterPoint on a PointPillars backbone, exported to TensorRT. It
  was trained on nuScenes plus about 11,000 frames of the company TIER IV's
  own data: the domain gap from L4, closed with local data.
- **Baidu's Apollo** ships four LiDAR models, and since release 9.0
  CenterPoint is the default.
- **NVIDIA** publishes PointPillars at 6.84 ms per frame on Orin, and
  CenterPoint at 23 frames per second. That fits the budget of a 10 Hz LiDAR
  with room to spare. NDS, the nuScenes detection score, is defined in the
  next subsection.
- **Waymo** released 12.6 million labeled 3D boxes so that everyone can
  compare detectors on the same data.

**So:** the models of this section are what ships. Open stacks run
CenterPoint on PointPillars, exported to TensorRT to fit the time budget.


.. _l5-lec-nds:

Scoring a 3D Detector: mAP and NDS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3D boxes need their own grade, because IoU in pixels no longer applies. The
standard is **nuScenes**, a driving dataset with 3D boxes.

- **Matching.** Not IoU, but the distance between centers on the ground: a
  detection matches a real object when their centers are within 0.5, 1, 2
  or 4 m. Compute AP at each distance and average: that is nuScenes'
  **mAP**.
- **Five errors of the matched boxes:** position (m), size
  (:math:`1 -` IoU), heading (rad), velocity (m/s), and **attribute**, the
  object's state such as moving, parked or stopped (:math:`1 -` accuracy).
  Each error becomes a score, one minus the error, never below zero.

.. math::

   \text{NDS} = \frac{1}{10}\Big[\, 5 \times \text{mAP} + \sum_{i=1}^{5}
   \max(1 - \text{error}_i,\ 0) \,\Big]

.. admonition:: Definition: nuScenes detection score (NDS)
   :class: note

   mAP gets a weight of five, each of the five scores a weight of one, and
   the sum is divided by ten. So half of NDS is "did you find it", and half
   is "is the box right". Definition from the nuScenes devkit.


.. admonition:: Where that leaves us: 3D detection
   :class: tip

   - A 3D box gives **7 numbers**: center, size and heading, in meters in the
     AV's frame; with velocity, 9. From them, car B, centered 2 m to the
     right, reaches **1.70 m** into the AV's lane: its front-left corner is
     5 cm from the centerline.
   - LiDAR points thin out: about **11** rings on car B at 12 m, **2 or 3**
     at 50 m.
   - LiDAR detectors work **from above**. PointPillars turns the points into
     an image of :math:`0.16 \times 0.16` m pillars, so L4's 2D tools apply.
     CenterPoint finds each object as a peak and reads its velocity
     directly: 65.5 NDS on the nuScenes test set, as its paper reports.

Keep "from above" in mind. It comes back in :ref:`l5-lec-bev`, for cameras.


.. _l5-lec-3d-handson:

Hands-On: 3D Boxes from LiDAR, in CARLA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This one is for after class.

- **What it does:** the ROS 2 package ``l5_box_demo`` finds 3D boxes in each
  LiDAR sweep with no learning, by **L-shape fitting** (Zhang et al., 2017):
  it clusters the LiDAR points, fits a rotated box to each cluster, and
  grades the boxes against CARLA's true boxes.
- **To run it:** the commands, the tasks and the measured results are on
  :ref:`the Code page <l5-box-demo>` and in the package's
  `README <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l5_box_demo/README.md>`__.

.. admonition:: What to look at
   :class: hint

   - **The box center against the bare centroid.** The fitted box center
     lands closer to the truth; the centroid falls short, as in
     :ref:`l5-lec-frustum`.
   - **Boxes on walls and trees.** Nothing here knows classes.
   - **A heading known only up to** :math:`180^\circ`. One sweep cannot tell
     a car's front from its back.

That gap is what trained detectors like CenterPoint close.



.. _l5-lec-segmentation:

Segmentation
------------

- **Where we are:** boxes, in pixels and in meters.
- **In this section:** going below the box: a class for **every pixel**.
- **What it is for:** objects with odd shapes (a cyclist, a fallen branch, a
  truck towing a trailer), and the road itself: the drivable area and lanes
  have no box.

A box around a person also contains road and part of a bus. And some of what
the AV needs, the drivable area, the lane lines and the curbs, has no sensible
box at all. Three subsections were shown in class: what semantic
segmentation gives, one CARLA frame segmented, and why the road is segmented
from above. Masks, instance segmentation and SAM are reading material, in the
subsections between them.


.. _l5-lec-semantic:

Semantic Segmentation: a Class for Every Pixel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** The AV drives behind car B. The detector boxed car B, but the
planner also needs where the AV *may* drive: the road, the lane markings, the
curb. None of these has a box. **The question:** in the front camera's image,
which pixels are road, and which are lane marking?

.. admonition:: Definition: semantic segmentation
   :class: note

   A class for **every pixel** of the image: road, sidewalk, car, person,
   sky. Two people next to each other get the same class; it does not tell
   them apart.

Telling two people apart is the job of instance segmentation, in the reading
below.

- **Its output:** a grid the size of the image, one class number per pixel.
  The front camera is the lecture's camera, :math:`1280 \times 720` pixels:
  :math:`1280 \times 720 = 921{,}600` numbers per frame.
- **Where the classes come from:** on an AV, a trained network computes them
  from the image, in real time. In CARLA, a semantic segmentation camera
  writes the **true** class of each pixel, with no network. In CARLA's
  documentation, class 1 is road and class 2 is sidewalk.


.. _l5-lec-seg-carla:

A Class for Every Pixel, in CARLA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** The AV is on a city street in CARLA (Town10HD), with two cars
ahead. **What we have:** one moment captured by our script: the front camera
(left) and CARLA's semantic segmentation camera mounted at the same place
(right), both :math:`1280 \times 720`.

.. figure:: /_static/images/L5/seg_example.png
   :alt: Two images of the same street from the AV's front camera in CARLA. Left, the camera image: a four-lane city street with a double yellow center line, dashed white lane lines, a small blue car on the left, a dark jeep ahead on the right, a bus shelter on the right sidewalk, buildings and trees. Right, the semantic segmentation of the same view: the road purple, lane markings bright green, sidewalks pink, the cars dark blue, buildings dark gray, trees olive green, poles light gray, the bus shelter teal, the sky blue, and the AV's own hood dark blue at the bottom. A legend names the nine colors: road, lane marking, sidewalk, car, building, vegetation, pole, static object (bus shelter), sky.
   :width: 93%
   :align: center

   **Left:** the front camera image. **Right:** CARLA's true classes for the
   same view, one color per class: road purple, lane markings green,
   sidewalks pink, cars dark blue. The AV's own hood is the dark blue at the
   bottom.

- **The right image is the truth,** straight from the simulator. On a real AV
  there is no such camera: a trained network has to produce this picture
  from the left image alone, every frame.
- **Every pixel has a class,** shown as a color. Both cars are the same dark
  blue: semantic segmentation does not tell them apart.
- **The things that have no box are all there:** the road, every lane
  marking, the sidewalks. That is what the planner needs from this section.


.. _l5-lec-mask:

Mask: the Pixels of One Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Back to L4's bus photo. **YOLOv8s-seg**, the segmentation version of L4's
YOLOv8s, found the man in the light-colored jacket. **The question:** how
much of his box is really him?

.. admonition:: Definition: mask
   :class: note

   A grid the size of the image: 1 for every pixel of one object, 0 for every
   other pixel.

The same kind of grid can also hold a whole class, every person at once.
That is what semantic segmentation gives.

.. figure:: /_static/images/L5/mask_example.png
   :alt: Left: the bus photo, a street in Madrid with a blue electric bus and several people, with a dark red box around the man in the light-colored jacket, labeled his box: 99,437 px. An arrow labeled his box, enlarged leads to the right panel: the same box drawn at the photo's height, his mask in orange on a light gray background. Legend: orange 1, him, 51,476 px; gray 0, the rest, 47,961 px.
   :width: 55%
   :align: center

   **Left:** L4's bus photo, with the man's box (99,437 px). **Right:** his
   box, enlarged. **Orange** is 1, him (51,476 px); **gray** is 0, the rest
   (47,961 px).

Measured with YOLOv8s-seg on the photo:

1. **His box:** :math:`196.93 \times 504.93 \approx 99{,}437` pixels.
2. **His mask:** :math:`51{,}476` pixels are 1.
3. :math:`51{,}476 / 99{,}437 =` **51.8%** of his box is him. The other
   48.2% is street and bus.

For avoiding a person, the box is usually enough. The mask gives the exact
outline: where an arm or a bag sticks out, or the exact edge of the road.


.. _l5-lec-instance:

Semantic and Instance Segmentation on Our Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The question:** on the same photo, how many people are there, and which
pixels belong to each? Semantic segmentation labels every pixel but cannot
tell two people apart.

.. admonition:: Definition: instance segmentation
   :class: note

   Every object's **own pixels**: one mask per object.

**What we have:** YOLOv8s-seg's masks, measured: 6 masks, the bus, four
people and a tie. YOLOv8s-seg is an instance model. It starts from
detection: it finds each object's box, then marks which pixels inside the
box belong to it.

.. figure:: /_static/images/L5/seg_types.png
   :alt: The image twice with the same six masks from YOLOv8s-seg. Left, colored by class: the bus in blue, every person in the same orange, the tie in green. Right, colored by object: each mask in a different color.
   :width: 60%
   :align: center

   The same six masks, colored two ways. **Left, semantic view:** one color
   per class, so every person is the same orange. **Right, instance:** one
   color per object.

- **Right, instance:** each mask has its own color, so you can count the
  people, and, at the end of this lecture, track each one.
- **Left, semantic view:** the same masks, which we colored one color per
  class. You know where "person" is, not how many. A real semantic model
  would also label the road and the building.

On an AV you use both: semantic segmentation for things that are not
objects, like the drivable area and the lane lines; instances for things you
have to predict and avoid, like people and cars.


.. _l5-lec-seg-kinds:

Three Kinds of Segmentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Semantic and instance segmentation are two separate tasks, and each one
misses something. Semantic cannot count: two people side by side are one
"person" region. Instance cannot do the road: the road is not an object, so
it gets no mask at all. A third task, panoptic segmentation, named by
Kirillov and colleagues in 2019, does both at once.

.. admonition:: Definition: panoptic segmentation
   :class: note

   Every pixel gets a class. Every pixel of a countable object (a **thing**,
   such as a person or a car) also gets the id of its object. Road, sky and
   grass (**stuff**) get a class only.

.. list-table::
   :widths: 22 22 26 30
   :header-rows: 1
   :class: compact-table

   * -
     - **Semantic**
     - **Instance**
     - **Panoptic**
   * - Each pixel gets
     - a class
     - an object id, if it is on an object
     - a class, plus an object id on things
   * - The road and the sky
     - a class
     - nothing
     - a class
   * - Two people side by side
     - both "person"
     - person 1, person 2
     - person 1, person 2
   * - Example model
     - SegFormer
     - Mask R-CNN, YOLOv8s-seg
     - Mask2Former

SegFormer is the model in our ROS package; YOLOv8s-seg is the one on the bus
photo; Mask2Former does all three.


.. _l5-lec-seg-tree:

The Kinds of Segmentation, as a Tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instance segmentation is not a subset of semantic segmentation: each gives
something the other lacks. Panoptic takes one part from each.

.. figure:: /_static/images/L5/seg_tree.png
   :alt: A tree. The root box: Segmentation, a label for every pixel (or every LiDAR point). Four branches, left to right. Semantic: a class per pixel, things and stuff, no object ids; example SegFormer. Panoptic: a class per pixel and an id on things, one label per pixel; example Mask2Former. Instance: a mask per object, things only, with ids, masks may overlap; example YOLOv8s-seg. Promptable: a mask for what you point at, no fixed class list; example SAM. A dashed green arrow labeled its stuff goes from Semantic to Panoptic, and a dashed orange arrow labeled its things goes from Instance to Panoptic. Below: any kind can run on a camera image, LiDAR points, or a grid seen from above (next section). A key: things are countable objects (a person, a car); stuff is regions you do not count (road, sky, grass).
   :width: 100%
   :align: center

   The kinds of segmentation. All of them give a label for every pixel, or
   every LiDAR point. **Semantic** (SegFormer), **panoptic** (Mask2Former),
   **instance** (YOLOv8s-seg) and **promptable** (SAM). The **green** dashed
   arrow carries semantic's stuff into panoptic; the **orange** one carries
   instance's things.

- **Semantic** labels the road and the sky but cannot count people.
  **Instance** counts the people but leaves the road blank, and its masks may
  overlap.
- **Panoptic** sits between them on purpose. It takes the stuff from
  semantic, the road and the sky, and the things from instance, the people
  and the cars, with exactly one label per pixel.
- **Promptable** is a different kind of task: there is no fixed list of
  classes; you point at something and get its mask. That is SAM, below.
- None of this is tied to the camera. The same kinds run on LiDAR points,
  and, in the next section, on a grid seen from above.


.. _l5-lec-seg-sensors:

Which Sensors Segment
~~~~~~~~~~~~~~~~~~~~~

Camera pixels and LiDAR points can both get classes, and an AV can pass the
camera's classes to its LiDAR points.

.. list-table::
   :widths: 15 20 30 35
   :header-rows: 1
   :class: compact-table

   * - **Sensor**
     - **What gets a class**
     - **Strength; limit**
     - **Example**
   * - Camera
     - each pixel
     - color and texture: lane markings, the road's edge, signs; no distance
     - Cityscapes: 5000 finely labeled images from 50 cities, 19 classes
       graded
   * - LiDAR
     - each 3D point
     - distance, day or night; sparse far away (the rings, earlier)
     - SemanticKITTI: over 43,000 labeled scans, 19 classes graded; Autoware
       removes the ground points
   * - Camera, then LiDAR
     - each point, from the class of the pixel it lands on
     - drops points on the road, building, vegetation or sky; needs the L2
       calibration
     - Autoware's segmentation pointcloud fusion

- **Camera.** Color and texture are what tell a lane marking from the road,
  and the big labeled datasets are camera images.
- **LiDAR.** Each point is a 3D position, so the class comes with a distance,
  at night as well. The simplest LiDAR segmentation is ground or not ground:
  Autoware runs a node that removes the ground points.
- **Camera, then LiDAR.** Autoware runs a camera segmentation network,
  projects the LiDAR points onto its output, and drops the points that land
  on classes such as road, building, vegetation or sky. That only works if
  each point lands on the right pixel: the L2 calibration.
- **Radar** returns too few points to label a scene this way, so it does not
  appear in the table.


.. _l5-lec-seg-pipeline-semantic:

Pipeline: Semantic Segmentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The CARLA frame from before, through **SegFormer-B0**, trained on
Cityscapes: the model in our ROS package ``l5_seg_demo``. We ran it on this
frame; every image and size below is measured from its output.

.. figure:: /_static/images/L5/segp_semantic.png
   :alt: Semantic segmentation pipeline, left to right. The CARLA camera image, 1280 by 720, a city street with a double yellow center line and buildings. An arrow to the encoder, four green blocks that get smaller, labeled 1/4 to 1/32 of the size. An arrow to the decoder, three orange blocks that get larger, labeled back up to 1/4. An arrow to two of the 19 score maps, 180 by 320: road, black over the lower part of the image, and car, white with small black spots where the cars are. An arrow labeled each pixel: highest score, to the output: a class per pixel, 1280 by 720, with the road purple, sidewalk pink, cars dark blue, buildings dark gray and trees green, and a legend for those five colors.
   :width: 100%
   :align: center

   SegFormer-B0 on the CARLA frame. The **encoder** shrinks the image to 1/4
   to 1/32 of its size; the **decoder** brings it back up to 1/4; two of the
   **19 score maps** (:math:`180 \times 320`) are shown, "road" and "car",
   black where the score is high; each pixel takes its **highest score**,
   giving a class per pixel at :math:`1280 \times 720`.

1. **The encoder** shrinks the image to 1/4, 1/8, 1/16 and 1/32 of its size
   and finds patterns at each scale. Small maps see large patterns, like a
   whole car; large maps keep fine detail, like a lane line.
2. **The decoder** brings all four back to 1/4 and gives 19 scores per
   cell, one per Cityscapes class:
   :math:`720/4 \times 1280/4 = 180 \times 320` cells.
3. **The scores are resized** to :math:`1280 \times 720`; each pixel takes
   the class with the highest score.

The class image is the network's answer, not CARLA's truth. It has no
lane-marking class, because Cityscapes counts the markings as road.


.. _l5-lec-seg-pipeline-instance:

Pipeline: Instance Segmentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L4's bus photo through YOLOv8s-seg: it detects each object as in L4, and
adds one mask per object. We ran it and pulled out the pieces; every image
and size below is measured.

.. figure:: /_static/images/L5/segp_instance.png
   :alt: Instance segmentation pipeline, left to right. The bus photo, 810 by 1080. An arrow to a green box, backbone plus neck (L4), which splits in two. Top: the detection head, per object: box, class, score (L4), and 32 numbers. Bottom: three gray prototype masks of the whole image, 160 by 120, each times the man's number for it, then dots for the rest of the 32. Both lead to the man's sum: a gray image where the people are darker, with a dark red box around the man in the light-colored jacket, labeled his 32 numbers times the 32 masks, added; his box. An arrow labeled keep: in his box, above 0, leads to the output: the photo with one colored mask per object, six in all: the man in orange, the bus in red, the other people in blue, green and purple.
   :width: 90%
   :align: center

   YOLOv8s-seg on the bus photo (:math:`810 \times 1080`). The **backbone
   and neck** (L4) feed two heads: the **detection head** (box, class, score
   and 32 numbers per object) and **32 prototype masks** of the whole image
   (:math:`160 \times 120`, 3 shown). The man's 32 numbers times the 32
   masks, added, give his sum; kept inside **his box** where it is above 0,
   it gives his mask. The output has one mask per object, 6 in all.

1. **Backbone and neck,** as in L4. The photo goes in at
   :math:`640 \times 480`.
2. **Two heads at once.** The detection head gives each object what L4's
   gave, a box, a class and a score, plus 32 numbers. The prototype head
   gives 32 masks for the whole image, each :math:`160 \times 120`. They
   are not masks of any one object; they are patterns, like "people" or "the
   bus".
3. **An object's mask** is its own mix of those patterns: its 32 numbers
   times the 32 masks, added, kept inside its box where the sum is above 0.
   For the man, the sum is dark on both people and on the bus outline; cut to
   his box, only he is left. YOLACT (2019) introduced this idea.


.. _l5-lec-seg-models:

Well-Known Segmentation Models, Camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 8 16 16 60
   :header-rows: 1
   :class: compact-table

   * - **Year**
     - **Model**
     - **Kind**
     - **Main idea**
   * - 2015
     - FCN
     - semantic
     - every layer is a convolution, so any image size goes in and a score per
       pixel comes out; deep coarse layers are combined with shallow fine ones
   * - 2015
     - U-Net
     - semantic
     - a contracting path, then a symmetric expanding path that reuses copied
       feature maps; built for medical images
   * - 2018
     - DeepLabv3+
     - semantic
     - atrous (dilated) convolution sees several scales; a decoder sharpens
       the object edges
   * - 2021
     - SegFormer
     - semantic
     - a Transformer encoder at four scales and a small MLP decoder: our
       ``l5_seg_demo``
   * - 2017
     - Mask R-CNN
     - instance
     - a two-stage detector plus a mask branch: a small mask for each box
       (:math:`28 \times 28` in its FPN version)
   * - 2019
     - YOLACT
     - instance
     - prototype masks and a few numbers per object; YOLOv8s-seg works the
       same way
   * - 2022
     - Mask2Former
     - all three
     - one model for semantic, instance and panoptic segmentation
   * - 2023
     - SAM
     - a mask you ask for
     - any object you point at (below)

- **The top four are semantic.** FCN was the first network made only of
  convolutions. U-Net shrinks the image and then grows it back, reusing what
  it saw on the way down; it is still everywhere. DeepLabv3+ adds dilated
  convolutions, which see several scales at once. SegFormer swaps the encoder
  for a Transformer.
- **The next two are instance models.** Mask R-CNN takes a two-stage
  detector, like the ones in L4, and adds a small mask for each box. YOLACT
  uses prototypes, as in the pipeline above.
- **Mask2Former** does all three kinds with one model, and **SAM** gives a
  mask for whatever you point at.


.. _l5-lec-seg-lidar:

Segmenting LiDAR Points
~~~~~~~~~~~~~~~~~~~~~~~

A LiDAR scan is a set of 3D points, not an image. Two well-known models give
each point a class, in two different ways.

.. list-table::
   :widths: 20 45 35
   :header-rows: 1
   :class: compact-table

   * - **Model**
     - **How**
     - **Measured in the paper**
   * - RangeNet++ (2019)
     - lays the scan out as a range image (one row per laser ring), runs a 2D
       network on it, then puts the classes back on the 3D points
     - 12 frames per second on a desktop GPU, 5 on an embedded one (full
       resolution)
   * - Cylinder3D (2021)
     - cuts space into cylinder-shaped cells that grow with distance, then
       runs 3D convolutions
     - 89% of its cells hold points, against 61% for cubes

- **RangeNet++** turns the scan into an image: one row per laser ring, one
  column per direction, and the range as the pixel value. A normal 2D network
  labels it, and the labels go back onto the 3D points. For comparison, the
  LiDAR spins at about 10 turns per second.
- **Cylinder3D** stays in 3D. Its cells widen with distance because points
  thin out with distance, the rings from the 3D Detection section, so cubes
  far away would be mostly empty.

Both are graded on **SemanticKITTI**, the LiDAR counterpart of Cityscapes.


.. _l5-lec-sam:

Segment Anything: a Mask for Whatever You Point At
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** Someone labeling training data needs the bus's mask, and the
bus is not one of the classes a segmentation model was trained on. **The
question:** can one box, drawn around it, give the mask?

.. admonition:: Segment Anything (SAM)
   :class: tip

   SAM (2023) is **promptable**: a point or a box in, a mask out, for objects
   it was never trained on. Trained on "over 1 billion masks on 11M licensed
   and privacy respecting images", from the paper.

.. figure:: /_static/images/L5/sam_point.png
   :alt: The image with YOLOv8s's bus box drawn as a dashed blue rectangle labeled prompt: the detector's box. Inside it, the SAM mask colors the bus green and leaves out the people standing in front of it and the pavement.
   :width: 40%
   :align: center

   The prompt is the detector's box around the bus (dashed blue). The mask
   that comes out (green) covers the bus and leaves out the people in front
   of it and the pavement.

- **Measured** with **MobileSAM**, a smaller and faster SAM, by L4's figure
  script: YOLOv8s's bus box in, a mask out, covering
  :math:`260{,}882 / 412{,}163 =` **63%** of the box. The people and the
  pavement are left out: the difference between a box and a mask.
- **Newest:** SAM 3 (November 2025) also takes a phrase, "yellow school
  bus" (the paper's example), and returns a mask for every matching object in
  the image, not just the one you pointed at.
- **On an AV:** mostly offline, in the lab, to **label** training data. Draw
  a box, get a mask, correct it, move on.


.. _l5-lec-labeling:

Labeling Millions of Frames
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** The segmentation network in the AV learns from frames whose
every pixel is already labeled, and a company needs millions of them. **The
question:** who draws those labels? Nobody draws them all by hand. The usual
pipeline:

1. **Collect:** the fleet records drives; triggers flag the rare and hard
   moments: rare objects, near misses, disagreements between sensors.
2. **Auto-label offline:** large, slow models, with the whole drive
   available, the future included, draw boxes and masks. The labeling model
   can use what happened a second later, which the AV never can.
3. **Review:** people check and correct the labels, using prompt tools like
   SAM.
4. **Train** the small, fast model that runs in the AV.

.. important::

   The model in the AV is only as good as the labels. A simulator skips most
   of this: **CARLA writes the labels for you**, from its own scene data, as
   in the CARLA frame above. They can still be wrong, for example around
   hidden objects, so check them: open random images with their labels drawn
   on.


.. _l5-lec-seg-road:

Segmenting the Road Itself
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** the same CARLA moment. **The question:** where are the lane
lines *in meters*, on the ground, where the planner works?

**What we have:** the semantic image (CARLA's true classes) and CARLA's
depth camera, which gives each pixel's true distance. This is a shortcut
only a simulator gives. Our capture script puts every pixel of the semantic
image on the ground, on a grid of 0.2 m cells seen from above.

.. figure:: /_static/images/L5/seg_bev.png
   :alt: Left, the semantic segmentation image from the CARLA slide, with the note that a lane marking is 9 pixels wide at 10 m and 4 pixels wide at 20 m, measured. Right, the same pixels put on a grid seen from above, x ahead from 0 to 50 m up the page and y from 20 m left to 20 m right; the camera is a black dot at the bottom middle. Marker 1: near the camera the lane markings are straight and parallel green lines. Marker 2: far away the purple road splits into separate thin rows. Marker 3: white wedges where no pixel lands, behind the cars and between rows.
   :width: 78%
   :align: center

   **Left, in the image:** a lane marking is 9 pixels wide at 10 m and 4
   pixels wide at 20 m (measured). **Right, from above,** in meters, with
   :math:`x` ahead up the page and :math:`y` to the left; the camera is the
   black dot. **1:** near, the lane markings are straight and parallel.
   **2:** far, the road splits into separate rows. **3:** white, no pixel
   lands there.

- In the camera image, a lane line far ahead is only a few pixels wide: the
  capture script measured 9 pixels at 10 m and 4 at 20 m.
- Near the AV, **marker 1**, the lane lines are straight and parallel, in
  meters.
- Far away, **marker 2**, the road breaks into separate rows, because a meter
  of far road is less than one image row.
- **Marker 3**, the white wedges, are places no pixel reaches: behind the
  cars.

An AV has no camera that gives true depth: a network must estimate it and
fill the gaps, on the grid seen from above. That is the next section.

.. tip::

   See "One Pixel onto the Grid" in :doc:`Going Further <l5_appendix>`: one
   pixel of this figure placed on the grid, step by step.


.. admonition:: Where that leaves us: segmentation
   :class: tip

   Semantic segmentation gives a class per pixel, :math:`921{,}600` of them
   in one frame of the front camera, computed by a network on an AV, given
   as truth by CARLA. Objects get boxes (and masks, in the reading); the road
   gets classes. A far lane line is a few pixels wide (4 at 20 m in CARLA),
   so current stacks give the road's classes on the BEV grid: the next
   section.


.. _l5-lec-seg-handson:

Hands-On: Segmenting CARLA's Camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This one is for after class.

- **What it does:** the ROS 2 package ``l5_seg_demo`` runs a trained network
  (SegFormer-B0, trained on Cityscapes, the network from the pipeline above)
  on the bridge's front camera, and grades it pixel by pixel against CARLA's
  semantic camera mounted at the same place.
- **To run it:** the commands, the tasks and the measured results are on
  :ref:`the Code page <l5-seg-demo>` and in the package's
  `README <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l5_seg_demo/README.md>`__.
  The network needs one extra Python package, ``transformers``; its weights
  download on the first run.

.. admonition:: What to look at
   :class: hint

   - **The IoU of each class** in the log, printed every 10 seconds.
   - **Lane markings called road.** Cityscapes has no lane-marking class; in
     our runs the network called over 99 percent of them road.
   - **Thin poles called building.** Thin objects, poles and traffic lights,
     are mostly called building.
   - ``instances:=true`` adds YOLOv8s-seg masks.



.. _l5-lec-bev:

BEV and Occupancy
-----------------

- **Where we are:** a class per pixel, and boxes in meters from LiDAR.
  PointPillars and CenterPoint already worked from above.
- **In this section:** one map of the ground around the AV, seen from above,
  built from **cameras**; then which parts of the space are taken, by
  anything.
- **What it is for:** the planner works on the ground, in meters; a map from
  above is in its units.

.. admonition:: Definition: bird's-eye view (BEV)
   :class: note

   A grid laid on the ground around the AV, seen from above. Every cell has
   the same size in meters, for example :math:`0.5 \times 0.5` m, and holds
   what perception found there: a car, road, a lane line.


.. _l5-lec-far-road:

The Camera Squeezes the Far Road into a Few Rows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** The AV's front camera looks down a straight, flat road. The
planner needs that road in meters, near and far. **The question:** how many
image rows does one meter of road get, 10 m ahead and 50 m ahead?

**What we have:** the pinhole model (L2), drawn from the side. The camera
looks level.

- :math:`h`: the camera's height above the road: 1.5 m (chosen for this
  example).
- :math:`d`: how far ahead a road point is, in meters.
- :math:`f`: the focal length, in pixels:
  :math:`f = (1280/2)/\tan 45^\circ = 640` px for our CARLA camera (1280 px
  wide, :math:`90^\circ` field of view, the default camera in our CARLA
  setup).
- :math:`v`: how many pixel rows below the horizon that point lands.

.. figure:: /_static/images/L5/pinhole_side.png
   :alt: Side view, not to scale. A camera, a black dot, h above a flat road, with a dashed level line through it marked level (horizon). A green ray goes down from the camera to a road point d ahead on the road. A vertical image plane stands f in front of the camera; the ray crosses it v below the level line, marked in orange.
   :width: 50%
   :align: center

   The pinhole model from the side, not to scale. The camera sits :math:`h`
   above a flat road and looks level. The green ray to a road point
   :math:`d` ahead crosses the image plane, :math:`f` in front of the camera,
   :math:`v` below the level line (orange).

The two triangles have the same shape, so

.. math::

   \frac{v}{f} = \frac{h}{d}, \quad\text{so}\quad v = \frac{f\,h}{d}

1. **From 10 m to 11 m ahead:**
   :math:`\frac{640 \times 1.5}{10} - \frac{640 \times 1.5}{11} = 96.0 - 87.3 =`
   **8.7** rows.
2. **From 50 m to 51 m ahead:**
   :math:`\frac{640 \times 1.5}{50} - \frac{640 \times 1.5}{51} = 19.20 - 18.82 =`
   **0.38** rows.
3. :math:`8.7 / 0.38 \approx 23`: the near meter of road gets 23 times the
   rows of the far meter.

Far away, a whole car length fits in two rows.


.. _l5-lec-same-meter:

The Same Meter of Road, Near and Far
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is that answer drawn: the same two meters of road in the camera image
(top) and from above (bottom). The drawing is computed with the same pinhole
model, :math:`f = 640` px and :math:`h = 1.5` m.

.. figure:: /_static/images/L5/far_road_rows.png
   :alt: Top left, a sketch of the camera image, 1280 by 720 pixels, with the horizon dashed and the AV's lane, 3.5 m wide, as a gray triangle meeting at the horizon; a thin green band crosses the lane near the top of the triangle and a tiny box marks the far band near the horizon. Two zooms at one square per pixel: 10 to 11 m covers 8.7 rows, a block of green pixel rows; 50 to 51 m covers 0.38 rows, a single orange line inside one row. Bottom, the same road from above, d from 0 to 55 m ahead of the camera, with the AV at the left: the green band at 10 to 11 m and the orange band at 50 to 51 m have the same width, labeled from above: the same 1 m of road.
   :width: 98%
   :align: center

   **Top:** the camera image (:math:`1280 \times 720`) and two zooms, one
   square per pixel. The meter from **10 to 11 m** (green) covers **8.7
   rows**; the meter from **50 to 51 m** (orange) covers **0.38 rows**, less
   than one row. **Bottom, from above:** the same two meters have the same
   width, because that is what they are on the road.

.. admonition:: Why the view from above
   :class: tip

   In a BEV grid of 0.5 m cells, every meter of road is **2 cells**, near or
   far. Distances on the grid are distances on the road.


.. _l5-lec-bev-grid:

The BEV Grid: from Meters to a Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** Car B must go on the grid, so that every sensor that sees it
writes into the same cell. **The question:** which cell holds car B's center,
:math:`(12.0, -2.0)` m, from the detector's box (:ref:`l5-lec-box3d`)?

**What we have:** BEVFormer's grid. It is not computed: it is fixed by the
network's design (Li et al., 2022). It has :math:`200 \times 200` cells over
:math:`-51.2` to :math:`51.2` m in :math:`x` and :math:`y`, centered on the
AV. :math:`i` counts cells along :math:`x` (forward), :math:`j` along
:math:`y` (left); :math:`\lfloor\cdot\rfloor` rounds down.

1. **Cell size:** :math:`102.4 / 200 =` **0.512** m, about half a meter.
2. **Cell of a point:** shift by 51.2 so the grid starts at zero, divide by
   the cell size and round down:
   :math:`i = \left\lfloor (x + 51.2) / 0.512 \right\rfloor`, and the same
   for :math:`j` with :math:`y`.
3. **Car B's center,** :math:`(12.0, -2.0)` m:

   .. math::

      i = \lfloor 63.2 / 0.512 \rfloor = \lfloor 123.4 \rfloor = \mathbf{123}
      \qquad
      j = \lfloor 49.2 / 0.512 \rfloor = \lfloor 96.1 \rfloor = \mathbf{96}

4. :math:`200 \times 200 =` **40,000** cells, each holding a feature
   vector. The grid moves with the AV, and every sensor writes into the
   **same** cells. That is what makes fusion on the grid easy later.

.. figure:: /_static/images/L5/bev_grid.png
   :alt: A square grid seen from above, lines every 20 cells, x and y from -51.2 to 51.2 m. The corner at the bottom left is i = 0, j = 0; i counts along x, forward, to the right, and j along y, left, up. The AV sits at the center. Car B, a small blue box ahead and to the right of the AV, is labeled car B, center (12.0, -2.0) m. A zoom at the upper right shows car B's outline and its center dot inside a green cell: cell (i, j) = (123, 96).
   :width: 45%
   :align: center

   BEVFormer's grid, :math:`-51.2` to :math:`51.2` m in :math:`x` and
   :math:`y`, lines every 20 cells. Cell :math:`(0, 0)` is the bottom-left
   corner; :math:`i` counts along :math:`x` (forward, right) and :math:`j`
   along :math:`y` (left, up). The AV is at the center. The zoom shows car
   B's center in cell :math:`(i, j) = (123, 96)`.


.. _l5-lec-ipm:

Before Learning: Inverse Perspective Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** The AV has only its front camera, no depth sensor, and wants
the road seen from above. **The question:** where on the ground is each
pixel?

**The oldest answer:** assume **every pixel is on flat ground**. Then the
camera model of :ref:`l5-lec-far-road` runs backward:

.. math::

   v = \frac{f\,h}{d} \quad\Longrightarrow\quad d = \frac{f\,h}{v}

Same camera (:math:`f = 640` px; :math:`h = 1.5` m, chosen). Take a pixel 96
rows below the horizon (read off the image):

1. :math:`d = 640 \times 1.5 / 96 =` **10.0** m ahead.
2. Do that for every pixel below the horizon, and draw each one at its
   :math:`(x, y)` on the ground: a picture of the road from above.

.. admonition:: Definition: inverse perspective mapping (IPM)
   :class: note

   Redrawing an image as the ground seen from above, by assuming everything
   in it lies on the road. No learning, no depth sensor: exact for lane
   markings on a flat road, because lane markings really are on the ground.


.. _l5-lec-ipm-image:

IPM on a Whole Image: Lane Lines Right, the Car Wrong
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** The same camera (:math:`f = 640` px, 1.5 m up, looking level)
on a synthetic road made by a script, not CARLA: three lane lines and a car
1.5 m tall, its rear 10 m ahead (chosen). **The question:** where does IPM
put the lane lines, and the car?

.. figure:: /_static/images/L5/ipm_example.png
   :alt: Left, the front camera image of a synthetic road: two lanes with white lane lines meeting at the horizon, dashed at the middle of the image, and a blue car ahead whose roof touches the horizon. An arrow marks the bottom of the car, where it meets the road, 96 rows below the horizon, so d = 640 times 1.5 over 96 = 10 m. Right, the IPM top view, x from 0 to 40 m to the right and y, left, up: the lane lines are straight and parallel, a red dashed rectangle marks where the car really is, 10 to 14.5 m, and a blue wedge, where IPM puts the car's pixels, starts at 10 m and widens past 40 m.
   :width: 100%
   :align: center

   **Left, the front camera image:** the bottom of the car, on the road, is
   96 rows below the horizon, so :math:`d = 640 \times 1.5 / 96 = 10` m.
   **Right, IPM's top view:** the lane lines are straight and parallel. The
   **red dashed** box is where the car really is; the **blue** wedge is where
   IPM puts the car's pixels.

Measured on the script's output:

- The **bottom of the car**, where it meets the road, is 96 rows below the
  horizon, so IPM puts it at 10 m: right.
- The **lane lines** come out straight and parallel, as they are on the road.
- The **car** does not: its pixels land from 10 m to past 40 m. Every part of
  it above the road is placed too far.


.. _l5-lec-ipm-breaks:

IPM Breaks for Anything Above the Road
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The question:** where does IPM put each part of a car that stands on the
road? **What we have** (chosen): a car 1.5 m tall, 10 m ahead; the camera
1.5 m up. A point :math:`z` meters up is :math:`h - z` below the camera, so
it shows :math:`v = f\,(h - z)/d` rows below the horizon. IPM then says
:math:`d = f\,h/v`.

.. figure:: /_static/images/L5/ipm_side.png
   :alt: A side view, x forward to the right, from 0 to 20 m. On the left, the AV, a black car icon facing right, with its camera on the roof at x = 0, h = 1.5 m above flat ground. Ahead, the car, a gray car icon facing right, 1.5 m tall, its back at 10 m. Three rays from the camera: green to the bottom of the car, on the ground at 10 m; orange to the back of the car 0.75 m up, continued dashed to the ground at 20 m, where an orange cross is labeled IPM puts it at 20 m; red, level with the camera, to the car's roof top, continued dashed and labeled roof top: never meets the ground.
   :width: 100%
   :align: center

   Three rays from the AV's camera (:math:`h = 1.5` m) to the car ahead.
   **Green:** to the bottom of the car, on the ground at 10 m. **Orange:**
   to the back of the car, 0.75 m up; IPM continues it to the ground and puts
   it at 20 m. **Red:** to the roof top, level with the camera; it never
   meets the ground.

1. **The bottom of the car,** on the road:
   :math:`v = 640 \times 1.5 / 10 = 96` rows, so :math:`d = 10` m.
   **Right.**
2. **The back of the car, 0.75 m up.** From behind, the camera sees the
   car's back. The point is 0.75 m below the camera, so
   :math:`v = 640 \times 0.75 / 10 = 48` rows. IPM assumes it is on the road:
   :math:`d = 640 \times 1.5 / 48 =` **20** m. **Twice too far.**
3. **The roof top, 1.5 m up:** level with the camera, :math:`v = 0`, so
   :math:`d` is **infinite**.

In an IPM picture every car is smeared into a long streak pointing away from
the camera. **IPM is fine for lane markings and useless for objects.** To
place objects from cameras, the network has to learn depth. That is
Lift-Splat-Shoot.


.. _l5-lec-lss:

Lift-Splat-Shoot: Pixels Pushed Out to the Grid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** Six cameras around the AV, as on the nuScenes car: 70° each,
55° apart, and a wider one, 110°, at the back (Caesar et al., 2020), and no
depth sensor. **The question:** how do we fill the BEV grid when no pixel's
depth is known? The first method that made this work from cameras alone, in
2020, is **Lift-Splat-Shoot** (Philion and Fidler, 2020). It answers in three
steps.

.. figure:: /_static/images/L5/lss_cameras.png
   :alt: The AV seen from above, front up, with six camera wedges around it: one straight ahead labeled 70 degrees, two more on each side, and one straight back labeled 110 degrees; neighboring wedges overlap a little.
   :width: 15%
   :align: center

   The six cameras of the nuScenes car, from above, front up: 70° ahead,
   110° at the back.

.. figure:: /_static/images/L5/lss_pipeline.png
   :alt: Three panels joined by arrows, all seen from above with the AV at the bottom, its front up. Lift: a short line in front of the AV is the camera image, with one pixel marked on it; a ray goes from the camera through the pixel out into the scene, cut by ticks into five depth bins, each with a bar whose length is its probability, the longest in the middle bin. Splat: the same ray on a grid of cells, and the five cells it crosses shaded, the darkest in the middle. Shoot: the same grid with three candidate paths from the AV, the straight one highlighted.
   :width: 74%
   :align: center

   The three steps, all seen from above. **1. Lift:** a ray from the camera
   through one pixel, cut into five depth bins; each bar's length is that
   bin's probability. **2. Splat:** the five cells the ray crosses, shaded
   by what lands in them. **3. Shoot:** candidate paths on the filled grid.

1. **Lift.** A CNN (L4) gives each pixel a **feature** and a **probability
   for each depth bin** along its ray, both set by training, and spreads the
   feature over the bins, weighted. The network does not guess one depth.
   The longest bar is near the real depth, but the others are not zero. All
   the pixels of one camera together fill a **frustum**: the wedge of space
   that camera sees.
2. **Splat.** Each bin falls in one BEV cell; the cell adds up all that lands
   in it, from every camera. So all cameras end up in one grid.
3. **Shoot.** In the paper, a planner scores candidate paths on the filled
   grid. The step that matters to us is the grid itself: BEV features built
   from cameras, trained end to end.

The features and the probabilities come out of the trained network on every
frame.

.. tip::

   See "Lift and Splat, by Hand" in :doc:`Going Further <l5_appendix>` for
   one lift and one splat worked with chosen numbers, and "BEVFormer" for a
   second way to fill the grid from cameras.


.. _l5-lec-bev-heads:

One BEV Grid, Several Heads
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** This frame's grid is filled. The planner needs car B's box, the
lanes, the free space and the map. **The question:** how do we get all of
them without reading the cameras once per task? Small networks called
**heads**, set by training, each read the same grid for one job:

.. list-table::
   :widths: 24 46 30
   :header-rows: 1
   :class: compact-table

   * - **Head**
     - **Output, per cell or per object**
     - **Used by**
   * - **3D detection**
     - a heatmap of centers, then a 3D box at each peak (CenterPoint's head)
     - tracking, prediction
   * - **Map segmentation**
     - a class per cell: drivable area, lane divider, crosswalk
     - planning
   * - **Occupancy**
     - free, occupied or unobserved, with height (below)
     - planning
   * - **Vectorized map**
     - each lane line as a list of points
     - planning

- The **detection head** works like CenterPoint's, from
  :ref:`l5-lec-centerpoint`: a heatmap of centers on the grid, and a box at
  each peak. Those boxes go to tracking.
- The **map segmentation head** gives every cell a class. That is the road
  segmentation postponed from the Segmentation section; here every cell is
  half a meter, near or far.
- The **vectorized map head** draws each lane line as a list of points, the
  way an HD map stores it.

.. important::

   One grid, built once per frame, is **shared by every head**: the cameras
   are read once, not once per task. That is why one BEV network can do all
   of these at once.


.. _l5-lec-online-map:

Maps Built on the Fly
~~~~~~~~~~~~~~~~~~~~~

**Scenario.** In L3 the AV matched signs against an HD map, drawn ahead of
time. Now road work moved a lane after the map was drawn, so the map is
wrong. **The question:** can the AV draw the lane lines, road edges and
crosswalks itself, from its own sensors, every frame? That is **online
mapping**, on the BEV grid.

- **Vectorized map:** each element as a short list of points, as an HD map
  stores it: a lane line as a **polyline** (points joined by straight lines),
  a crosswalk as a **polygon** (a closed polyline). A planner can follow a
  list of points.
- **MapTR** (Liao et al., 2023), cameras only: "online vectorized HD map
  construction". It reads the cameras into a BEV grid, then outputs each map
  element as a set of points. The paper reports 25.1 frames per second on an
  RTX 3090 GPU for its smallest version.

.. figure:: /_static/images/L5/vector_map.png
   :alt: Two top views of the same made-up road, the AV at the left facing right. Left, raster: a class in every 1 m cell; three lane lines that bend gently left drawn as staircases of dark cells, and a crosswalk as a block of orange cells. Right, vector: a short list of points; the same three lane lines as smooth polylines with 7 dots each, and the crosswalk as an orange polygon with 4 corner dots.
   :width: 98%
   :align: center

   The same road, made up for the drawing, two ways. **Left, raster:** a
   class in every 1 m cell; the lane lines become staircases of cells.
   **Right, vector:** each lane line is 7 points, and the crosswalk is a
   polygon with 4 corners.


.. _l5-lec-occupancy:

Occupancy: Which Space Is Taken
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** A fallen branch lies in the AV's lane. A detector only finds
classes it was trained on, and no detector was trained on branches, so there
is no box. To the planner the branch does not exist, but it is solid. **The
question:** how does the planner know that space is taken?

.. admonition:: Definition: 3D occupancy
   :class: note

   The space around the AV cut into **voxels**, small cubes. Each voxel is
   **free**, **occupied** or **unobserved**; an occupied voxel also gets a
   class (Tian et al., 2023, Occ3D).

**Unobserved** means no sensor saw it. A branch has no class, but it
**occupies** voxels. The Occ3D benchmark labels such things "general
objects".

.. figure:: /_static/images/L5/occupancy.png
   :alt: A block of small cubes, voxels, around the AV, seen at an angle. Most are empty and drawn as faint outlines. Colored ones are occupied: blue for a car, orange for a pedestrian, and brown for a fallen branch that no detector class covers. The AV is dark gray, on the left. A hatched patch of ground behind the car, as seen from the AV, marks voxels no sensor can see: unobserved.
   :width: 55%
   :align: center

   A drawing of occupancy. Occupied voxels: the **AV** (dark gray), a
   **car** (blue), a **pedestrian** (orange) and a **fallen branch** (tan),
   which has no class but is still occupied. The rest is **free**, except the
   hatched patch behind the car, which is **unobserved**: no sensor sees it.

**Grid size,** fixed by the Occ3D-nuScenes benchmark: 0.4 m voxels,
:math:`-40` to :math:`40` m in :math:`x` and :math:`y`, :math:`-1` to
:math:`5.4` m in :math:`z`: :math:`80 \times 80 \times 6.4` m.

1. :math:`80/0.4 = 200` cells each way, and :math:`6.4 / 0.4 = 16` layers.
2. :math:`200 \times 200 \times 16 =` **640,000** voxels, every frame.

Occupancy is built from cameras the same way as the BEV, with height added.
On an AV it runs next to the detector: boxes for objects you must predict,
occupancy for everything you must not hit.


.. _l5-lec-bev-industry:

BEV and Occupancy in Industry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

How real stacks use the BEV and occupancy grids, in each maker's own words:

.. list-table::
   :widths: 18 82
   :header-rows: 1
   :class: compact-table

   * - **Who**
     - **What they say, in their own words**
   * - **Nissan, 2007**
     - "world's first Around View Monitor": a "bird's eye image" from four
       180-degree cameras, **for the driver** when parking.
   * - **Tesla**
     - "Our birds-eye-view networks take video from all cameras to output the
       road layout, static infrastructure and 3D objects directly in the
       top-down view"; an "Occupancy Network" at AI Day 2022.
   * - **Baidu Apollo**
     - Release 10.0: "visual BEV (Bird's Eye View) object detection and
       occupancy network", 5 Hz on one Orin, using BEVFormer (appendix).
   * - **Autoware**
     - Camera BEV packages (BEVFormer, BEVDet, StreamPETR) and
       ``autoware_bevfusion``.
   * - **Autoware**
     - An occupancy grid from LiDAR: free up to each point, occupied at it,
       "UNKNOWN" behind it. The intersection module finds occlusions in "the
       unknown cells of the occupancy grid map" and slows the AV.

- **The view from above reached cars long before networks did.** Nissan's
  Around View Monitor stitched four wide-angle cameras into a bird's-eye
  image. That image was for the driver, to park; no planner read it.
- **Today the grid is what the planner reads.** Tesla's sentence describes
  the heads above: the road layout and 3D objects, output directly in the
  top-down view. Baidu's Apollo added BEV detection and occupancy in release
  10.0.
- **Autoware** ships BEVFormer and two other camera BEV detectors, plus
  BEVFusion, which comes back in the Fusion section.
- **Occupancy is older than networks.** Autoware builds a grid from LiDAR:
  free along each beam up to the point it hit, occupied at the point, unknown
  behind it. Its intersection module looks for unknown cells where cross
  traffic could come from, and slows the AV before it can see: the hatched
  patch of the occupancy figure, used to make a decision.

**So:** from a picture for a driver (2007) to the map a planner reads, the
BEV grid and the occupancy grid are now standard outputs of perception.


.. admonition:: Where that leaves us: BEV and occupancy
   :class: tip

   - In the image, the meter from 50 to 51 m gets **0.38** rows against
     **8.7** for 10 to 11 m. On BEVFormer's grid every cell is 0.512 m: car
     B, at :math:`(12.0, -2.0)`, sits in cell :math:`(123, 96)` of 40,000.
   - **IPM** is exact for lane markings, but puts the back of a car, 0.75 m
     up, at **20 m** instead of 10.
   - **Lift-Splat-Shoot** learns a probability per depth and adds what lands
     in each cell.
   - **Occupancy** adds height and catches what has no class: 640,000 voxels
     per frame on the Occ3D benchmark.


.. _l5-lec-bev-handson:

Hands-On: Four Views from Above, in CARLA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This one is for after class.

- **What it does:** the ROS 2 package ``l5_bev_demo`` builds this section's
  views of one CARLA scene, with no learning: a LiDAR height map, a LiDAR
  occupancy grid, camera IPM, and a semantic lift-splat with CARLA's true
  depth.
- **To run it:** the commands, the tasks and the measured results are on
  :doc:`the Code page <l5_code>` and in the package's
  `README <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l5_bev_demo/README.md>`__.
  Start the L2 bridge first, because it owns the clock. A snapshot command
  saves the four views as pictures.

.. admonition:: What to look at
   :class: hint

   - **Buildings smeared** outward in the IPM view: IPM breaks above the
     road.
   - **The far road splitting into rows** in the semantic view.
   - **Gray unknown wedges** behind objects in the occupancy grid.



.. _l5-lec-fusion:

Fusion
------

- **Where we are:** LiDAR boxes, camera masks and a BEV grid, each from its
  own sensor.
- **In this section:** where in the pipeline the camera and the LiDAR meet;
  then how to join a camera box to its LiDAR points; then sensors on
  **other** vehicles.
- **What it is for:** one picture of the scene, not one per sensor.

So far each method used one sensor. The AV has both a camera and a LiDAR,
and needs one picture, not two. One question sits under every fusion design:
**at what point in the pipeline do the sensors meet?** There are three
answers, and your constraints usually decide which one you get. You often do
not choose.


.. _l5-lec-fusion-scenario:

Scenario: One Car B, Two Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Car B cuts in, 12 m ahead and 2 m to the right, turned :math:`30^\circ`
toward the AV's lane. At the same instant the front camera takes an image
(green) and the LiDAR takes a sweep (orange); both see car B. The planner
needs **one** car B, not two. **The question for the next three
subsections:** at which stage of the pipeline do the camera's data and the
LiDAR's data join: at the start, in the middle, or at the end?

.. figure:: /_static/images/L5/fusion_scenario.png
   :alt: A top view, x forward to the right. The AV at the left, facing right, in its lane marked by two dashed lines. Its front camera's 90 degree view spreads to the right as a green wedge, labeled front camera: 90 degree view. Ahead and to the right, car B, light blue, turned 30 degrees toward the AV's lane, labeled car B, cutting in: (12.0, -2.0) m, 30 degrees. Orange dots line car B's back and left side, labeled LiDAR: points on car B's back and left side.
   :width: 65%
   :align: center

   Car B, cutting in at :math:`(12.0, -2.0)` m, :math:`30^\circ`. The
   **green** wedge is what the front camera sees (a :math:`90^\circ` view).
   The **orange** dots are the LiDAR's points on car B's back and left side,
   the two faces turned toward the AV.

In the next three subsections, the figure on top is the same pipeline each
time: camera and LiDAR, each from raw data to features to objects. The
**FUSE** bar is the only thing that moves.


.. _l5-lec-fusion-early:

Early Fusion: Combine the Raw Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The camera's data and the LiDAR's data join at the very **start**, before
anything interprets them.

.. figure:: /_static/images/L5/fusion_early.png
   :alt: Two sensor lanes, camera and LiDAR, each starting at raw data. A FUSE bar joins them immediately, and a single lane then runs through features and objects to one answer for the planner.
   :width: 62%
   :align: center

   Early fusion. The **FUSE** bar joins the camera's pixels and the LiDAR's
   points as raw data; one lane then runs through features and objects to
   one answer for the planner.

.. figure:: /_static/images/L5/fusion_scn_early.png
   :alt: Car B as the AV's front camera sees it, from behind and to its left. Top left, the camera's pixels of car B, in green text: camera, pixels. Bottom left, the LiDAR's points on car B alone, eleven orange rings, in orange text: LiDAR, points. Arrows from both lead to the right: car B with the orange rings drawn on its pixels, labeled each point paired with its pixel.
   :width: 45%
   :align: center

   What is combined: the camera's **pixels** of car B and the LiDAR's
   **points** on it, joined so that each point is paired with its pixel.

- **Combined:** the raw data. Each LiDAR point on car B is paired with the
  pixel it lands on, and one network reads the pairs. Nothing is thrown away
  yet. We work that projection out by hand in :ref:`l5-lec-frustum`.
- **The upside:** this is the most information available anywhere in the
  system, and the only design where a target too weak for either sensor
  alone can still be found.
- **Cost:** calibration to a fraction of a degree and timing to milliseconds
  (L2), or a pixel meets the wrong point. The extrinsic calibration has to be
  that good because you pair a pixel with a point; the timestamps, because
  the AV moved between them. And there is no second opinion: one bad sensor
  spoils the single stream.


.. _l5-lec-fusion-mid:

Intermediate Fusion: Combine Learned Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each sensor's network runs part of the way first, to its features: the
numbers from L4 that say how strongly a pattern is there. It has not yet said
"car". **The question:** what gets joined, and who decides how much each
sensor counts?

.. figure:: /_static/images/L5/fusion_intermediate.png
   :alt: Two sensor lanes each running from raw data to learned features. A FUSE bar joins them after the feature stage, and a single lane continues to objects and one answer.
   :width: 62%
   :align: center

   Intermediate fusion. Each lane runs from raw data to learned features;
   the **FUSE** bar joins them there, and one lane continues to objects and
   one answer.

.. figure:: /_static/images/L5/fusion_scn_mid.png
   :alt: A top view on a 1 m grid, x forward to the right. The AV at the left, facing right; car B ahead and to the right, about 12 m ahead, turned 30 degrees toward the AV's lane. The eight cells under car B are shaded, and each holds a green dot, a camera feature, and an orange dot, a LiDAR feature. A legend names the two dots; a caption says: both in the cells under car B.
   :width: 45%
   :align: center

   What is combined, from above: each cell under car B holds a **camera
   feature** (green) and a **LiDAR feature** (orange).

- **Combined:** learned features (L4) from both sensors, in the BEV cells
  under car B. One network, trained on both, reads them: **training** decides
  how much each sensor counts. Nobody writes the rule, so it can learn that
  the camera counts for more in daylight and the LiDAR for more in fog.
- **BEVFusion** (Liu et al., 2023) works this way. It lifts the camera
  features to the grid, takes the LiDAR features from above as PointPillars
  did, and joins them there, because both now describe the same cells of
  ground. The paper reports 1.3 percent higher mAP and NDS than the best
  before it on nuScenes, at 1.9 times lower computation cost.
- **Cost:** training data with every sensor present, and a rule that lives
  in the weights: hard to explain, harder to certify. You cannot point at the
  line of code that decided to trust the LiDAR. For a safety case, that is a
  real problem.


.. _l5-lec-fusion-late:

Late Fusion: Combine the Finished Answers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each sensor finishes its own job before anything is shared. **The question:**
how do two finished answers become one?

.. figure:: /_static/images/L5/fusion_late.png
   :alt: Two sensor lanes each running all the way through raw data, features and objects. A FUSE bar joins them only at the end, and a single arrow leads to one answer.
   :width: 62%
   :align: center

   Late fusion. Each lane runs all the way through raw data, features and
   objects; the **FUSE** bar joins them only at the end.

.. figure:: /_static/images/L5/fusion_scn_late.png
   :alt: Two answers about car B. Left, in green: the camera's answer, car B seen from behind and to its left with a green box around it, labeled camera: a car, at this box in the image. Right, in orange: the LiDAR's answer, car B seen from above inside an orange rotated box with a black center dot, labeled LiDAR: an object, near (12.0, -2.0) m. Arrows from both lead down to one box: one car B, by a filter (L3).
   :width: 45%
   :align: center

   What is combined: two statements. The **camera** says "a car, at this box
   in the image" (green); the **LiDAR** says "an object, near
   :math:`(12.0, -2.0)` m" (orange). A filter (L3) makes them one car B.

- **Combined:** two finished answers: the camera's box in the image (L4) and
  the LiDAR's 3D box (:ref:`l5-lec-3d`). We fuse the two statements, not the
  pixels and points behind them, and a filter from L3 joins them into one
  car B.
- **Why:** each path is built, tested and certified on its own, and a failed
  sensor just stops reporting.
- **Cost:** each sensor threw away everything except its conclusion. Two
  sensors that each **half-see** a pedestrian can each round that down to
  nothing, and you get two confident reports of an empty road.


.. _l5-lec-fusion-which:

Which One, and When
~~~~~~~~~~~~~~~~~~~

**Scenario:** you build the fusion for an AV like ours. **The question:**
which of the three designs do your sensors, your data and your team allow?
The useful question is not which one is best, but what your situation
already forces on you.

.. list-table::
   :widths: 16 46 38
   :header-rows: 1
   :class: compact-table

   * - **Use**
     - **When your situation looks like this**
     - **What you accept**
   * - **Early**
     - Sensors on **one rig**, calibrated to a fraction of a degree and
       synchronized to milliseconds; targets **too faint for one sensor**.
     - Huge data volume; **one bad sensor spoils everything**.
   * - **Intermediate**
     - Training data with **every sensor present**, and a team that can
       retrain the joint model.
     - The rule lives in the weights: **hard to explain, harder to certify**.
   * - **Late**
     - Sensors from **different vendors**, at different rates, some sending
       finished object lists; each path **tested on its own**.
     - Each sensor already threw away all but its conclusion.

.. important::

   **Most production stacks are late**, because the constraints come first:
   a radar that sends a finished object list over **CAN**, the vehicle's
   internal data bus, has **already chosen late fusion for you**. The three
   mix: one tightly synchronized camera and LiDAR pair on one rig (one rigid
   mount) fused early, everything else late.


.. _l5-lec-frustum:

Frustum Association
~~~~~~~~~~~~~~~~~~~

Give Car B's Camera Box a Distance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Scenario.** Car B cuts in, 12 m ahead and to the right. On every frame the
AV has two answers about it:

- The **camera detector** (L4) reports a box on car B, in pixels: :math:`u`
  from 640 to 925, :math:`v` from 355 to 485 (values chosen for this
  example). It says *car*; it does not say *how far*.
- The **LiDAR** sweep holds points in meters, in the AV's frame: some on car
  B, some on things around and behind it. Points carry no class: they know
  how far, but not what they hit.

**The question:** which LiDAR points are car B's, and where is car B? The
camera's finished box picks the LiDAR's raw points: the camera answers
*what*, the LiDAR answers *how far*. **The plan, one step per subsection:**

1. Project every LiDAR point into the image (the camera model of L2).
2. Keep the points that land inside car B's box.
3. Cluster them, and keep car B's cluster.
4. Turn car B's points into one position, for the tracker (next section).


Step 1: Project a LiDAR Point into the Image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**What we have.**

- **The camera's mount** (chosen): at :math:`(1.6, 0, 1.5)` m on the AV,
  that is, 1.6 m ahead of the base link and 1.5 m up, looking straight ahead
  and level. Its frame: :math:`x_c` right, :math:`y_c` down, :math:`z_c`
  forward, out of the lens.
- **Its image:** :math:`1280 \times 720`, :math:`90^\circ` field of view, so
  :math:`f = 640` px and the center is :math:`(c_u, c_v) = (640, 360)` (L2).
- **One LiDAR point** :math:`P`: the middle of car B's rear face, half a
  length, 2.25 m, back from the center along the heading:
  :math:`(12.0 - 2.25\cos 30^\circ,\ -2.0 - 2.25\sin 30^\circ) = (10.05, -3.125)`,
  1.0 m up (chosen).

.. figure:: /_static/images/L5/project_point.png
   :alt: Two panels. Left, from above: the AV at the left facing right, its camera a green dot on its roof; car B ahead and to the right, turned 30 degrees; the orange point P on the middle of car B's rear face. A green dashed line runs straight ahead from the camera, labeled z_c = 8.45 m, then turns right down to P, labeled x_c = 3.125 m. Right, the camera's image, 1280 by 720, with its center (640, 360) marked where the two center lines cross; car B's camera box drawn dashed in green, right of and below the center; the orange point P at (876.7, 397.9), inside the box.
   :width: 79%
   :align: center

   **Left, from above:** from the camera (green dot), :math:`P` (orange) on
   car B's rear face is :math:`z_c = 8.45` m ahead and :math:`x_c = 3.125` m
   to the right. **Right, the camera's image** (:math:`1280 \times 720`):
   :math:`P` lands at :math:`(876.7, 397.9)`, inside car B's camera box
   (dashed green), right of and below the center :math:`(640, 360)`.

1. **Into the camera's frame:** :math:`z_c = 10.05 - 1.6 = 8.45` m ahead of
   the lens; :math:`x_c = 3.125` m (right is :math:`-y`);
   :math:`y_c = 1.5 - 1.0 = 0.5` m below the lens. Here the calibration is
   only a shift and a swap of axes, because the camera looks straight ahead.
2. **The pinhole model (L2):**

   .. math::

      u = f\,\frac{x_c}{z_c} + c_u = 640 \times \frac{3.125}{8.45} + 640 = 236.7 + 640 = \mathbf{876.7}

   .. math::

      v = f\,\frac{y_c}{z_c} + c_v = 640 \times \frac{0.5}{8.45} + 360 = 37.9 + 360 = \mathbf{397.9}


Step 2: Keep the Points Inside the Box
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**The test, computed here.** The camera detector's box on car B (values
chosen) runs :math:`u` from 640 to 925 and :math:`v` from 355 to 485. The
point from Step 1 lands at :math:`(876.7, 397.9)`:
:math:`640 \le 876.7 \le 925` and :math:`355 \le 397.9 \le 485`, so it is
**inside**: keep it. Every point of the sweep goes through Steps 1 and 2; a
point outside the box is dropped.

.. figure:: /_static/images/L5/projection_image.png
   :alt: The front camera's image as a 1280 by 720 pixel frame, u to the right and v down from the top-left corner (0, 0). A dashed line marks row 360 to the image center, (c_u, c_v) = (640, 360). A blue rectangle, the detector's box on car B, spans u from 640 to 925 and v from 355 to 485. A red dot inside it is the LiDAR point on car B, (876.7, 397.9), labeled inside: keep.
   :width: 66%
   :align: center

   The camera's image, :math:`u` to the right and :math:`v` down from the
   top-left corner :math:`(0, 0)`. The **blue** box is the detector's box on
   car B, :math:`u` from 640 to 925 and :math:`v` from 355 to 485. The
   **red** dot, the LiDAR point at :math:`(876.7, 397.9)`, is inside: keep.


Step 3: Cluster the Frustum, Keep the Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The box is flat, but the space it sees is a wedge, wider the farther you go.

.. admonition:: Definition: frustum
   :class: note

   The wedge of space a camera box sees: every point that projects inside
   the box.

That includes points behind car B.

.. figure:: /_static/images/L5/frustum.png
   :alt: A top view, x forward to the right, y left, up the page. The AV at the origin facing right, its camera at the front. Two lines from the camera spread to the right: the frustum of the camera box, from straight ahead to the right. Inside it, car B, a light blue car in a dark blue box turned 30 degrees, with 41 LiDAR points along its rear face and its left side; their centroid, a red cross at (10.99, -1.89), sits about 1 m nearer the AV than the box center, a black dot at (12.0, -2.0). Farther right, a wall 8 m to the right of the AV, from x = 20 to 30 m, with 9 points.
   :width: 80%
   :align: center

   The **frustum** of car B's camera box, from above (green). Inside it:
   car B with its LiDAR points along its rear face and left side, and a
   **wall** 8 m to the right, from 20 to 30 m, with 9 points. The **red
   cross** is the centroid of car B's points, :math:`(10.99, -1.89)`; the
   **black dot** is the box center, :math:`(12.0, -2.0)`.

**We have** 50 points in the box (count chosen), some on a wall behind car
B. **Which are car B's?** **DBSCAN** (Ester et al., 1996), a clustering
method, groups points that have enough neighbors within a set distance. The
engineer chooses both settings. Here it finds:

- **41** points on car B, 9 to 14 m ahead;
- **9** points on the wall, 20 to 30 m ahead.

Car B is the big, near cluster. Keep it.


Step 4: the Centroid Falls Short of the Center
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**The question:** one position for car B, for the tracker. The simplest
choice is the **centroid** of its 41 points, their average. The LiDAR hits
car B only on the two faces turned toward the AV. The counts are chosen, the
points are spread evenly, and the face middles come from car B's box.

1. 15 points along its rear face, middle :math:`(10.05, -3.125)`; 26 along
   its left side, middle :math:`(11.53, -1.18)`.
2. **Centroid**, the weighted average:

   .. math::

      x = \frac{15 \times 10.05 + 26 \times 11.53}{41} = \mathbf{10.99}
      \qquad
      y = \frac{15 \times (-3.125) + 26 \times (-1.18)}{41} = \mathbf{-1.89}

3. The box center is :math:`(12.0, -2.0)`: the centroid is **1.0 m short**.
   A meter matters: it is the gap the planner keeps.

.. important::

   LiDAR sees only the near faces, so the bare centroid sits **toward the
   AV**. Real stacks fit a box to the cluster, or run a 3D detector on it.
   Then the position, with the camera's class *car*, goes to the tracker: the
   next section.


.. _l5-lec-fusion-industry:

Fusion in Industry
~~~~~~~~~~~~~~~~~~

How a real stack fuses camera and LiDAR: Autoware's packages, sorted by
where the sensors meet. **ROI**, region of interest, is a box in the image.

.. list-table::
   :widths: 30 52 18
   :header-rows: 1
   :class: compact-table

   * - **Package**
     - **What it does, in its own words**
     - **Meets**
   * - ``pointpainting``
     - LiDAR points projected into the camera detector's output: "the class
       scores are appended to each point"; then CenterPoint
     - early
   * - ``bevfusion``
     - camera and LiDAR features on one BEV grid
     - intermediate
   * - ``roi_cluster_fusion``
     - "The clusters are projected onto image planes"; a cluster that
       overlaps a camera box (IoU) takes its label
     - late
   * - ``roi_detected_object``
     - LiDAR objects take the labels of the camera's boxes
     - late
   * - ``segmentation_pointcloud``
     - points projected onto the segmentation mask: each takes its pixel's
       class, to filter the cloud
     - early

- **Point painting** is early: each LiDAR point is projected into the camera
  detector's output, takes on its class scores, and the painted cloud goes to
  CenterPoint.
- **BEVFusion** is intermediate: both sensors' features on one BEV grid.
- **ROI cluster fusion** is late, and it is frustum association turned
  around: cluster the LiDAR points first, project each cluster into the
  image, and where it overlaps a camera box, measured with IoU from L4, the
  cluster takes the box's label.
- **Segmentation** shows up here too: the camera's segmentation mask labels
  the LiDAR points, and Autoware uses that to filter the point cloud, for
  example to drop points on vegetation before they become false obstacles.

One open stack ships **all three** levels side by side. That is what "the
three mix" meant in :ref:`l5-lec-fusion-which`.


.. _l5-lec-csa:

Cooperative Situational Awareness
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sensors on Other Vehicles
^^^^^^^^^^^^^^^^^^^^^^^^^

**Scenario.** Later on the same drive, the AV follows a truck. Ahead of the
truck, a pedestrian is about to step into the road: no sensor on the AV can
see her. A connected car ahead, C, can. **The question:** how can the AV use
what C sees? Fusion does not have to stop at the AV's own sensors.

.. admonition:: Definition: cooperative situational awareness (CSA)
   :class: note

   Situational awareness shared between connected agents: vehicles and
   roadside units send what they perceive (detections, tracks, free space),
   and each agent fuses it with its own.

- **Why:** see past an occlusion, something that blocks the view; see
  farther, around a corner or onto a ramp before you reach it; get a second,
  independent view of the same object.
- **How it arrives:** over **V2X** (vehicle-to-everything) radio, as finished
  object lists: **late fusion**, with the same filters as before. Raw camera
  and LiDAR data are too large to send.
- **What each message needs:** the object's position, its uncertainty, a
  time stamp, and the **sender's own pose**: where the sender is and which
  way it faces.


A Pedestrian the AV Cannot See
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/L5/csa_pedestrian.png
   :alt: A top view of a straight road, x pointing right, all vehicles driving right. The AV, a black car, at x = 70 m, behind a truck from 78 to 90 m. A connected car C, a green car, at x = 100 m. A pedestrian at x = 115 m, 3 m to the left of the lane center. The truck's shadow, a gray wedge from the AV, covers the pedestrian. C's camera view, a green wedge, reaches the pedestrian. A dashed arrow from C to the AV is labeled V2X.
   :width: 92%
   :align: center

   The AV at 70 m, behind a truck (78 to 90 m). The **truck's shadow**, the
   gray wedge, covers the pedestrian at 115 m: the AV's sensors cannot see
   her. **C's camera view**, the green wedge, reaches her, and C sends
   "pedestrian 15 m ahead, 3 m left" to the AV over **V2X** (dashed arrow).

Level 1 of situation awareness fails here, so Levels 2 and 3 never start.

**The question:** where is the pedestrian, seen from the AV? **What we
have** (map frame: :math:`x` along the road, :math:`y` left; positions chosen
for this example):

- C's message, *pedestrian 15 m ahead, 3 m left of me*, with C's own pose,
  :math:`(100, 0)` facing :math:`+x`, from C's localization (L7);
- the AV's own position, :math:`(70, 0)`, from its localization.

**Computed here:**

1. **In the map frame:** :math:`(100 + 15,\ 0 + 3) = (115, 3)`.
2. **From the AV:** :math:`115 - 70 =` **45** m ahead and **3** m left.

.. warning::

   **That needed C's own position.** If C is wrong about where it is by a
   meter, the pedestrian is placed a meter wrong. The two errors add, the way
   variances added in L3. That is why the sender's pose and its uncertainty
   go in the message.


V2X on the Road Today
^^^^^^^^^^^^^^^^^^^^^

**Why this subsection:** the pedestrian story needs a car C, or a roadside
unit, that can send. How many can, today? The U.S. DOT plan of August 2024,
"Saving Lives with Connectivity", sets goals for V2X radios at the roadside.
The **National Highway System** is the main U.S. highways.

.. list-table::
   :widths: 20 38 42
   :header-rows: 1
   :class: compact-table

   * - **By the end of**
     - **National Highway System**
     - **Signalized intersections, top 75 metro areas**
   * - 2028
     - 20%
     - 25%
   * - 2031
     - 50%
     - 50%
   * - 2036
     - fully deployed
     - 85%

We are at the start of that table, so an AV cannot count on a message, only
use one when it comes.

**The radio:** in 2020 the FCC kept 30 MHz of the 5.9 GHz band for
transportation and required **C-V2X** (V2X over cellular radio), noting that
the older **DSRC** (dedicated short-range communications) "has barely been
deployed".


Discussion
^^^^^^^^^^

.. admonition:: Discussion
   :class: hint

   We do not have widespread cooperative situational awareness between
   automated vehicles today. Several challenges stand in the way, and they
   are connected. **Which ones?** Take five minutes with your neighbors. Name
   the challenges, and say how they connect.

.. dropdown:: What to listen for
   :color: success
   :icon: check-circle

   - **Few vehicles are equipped,** and the benefit only appears when many
     are: nobody buys the first radio.
   - **Trust:** a message can be wrong, or faked. A false pedestrian makes
     the AV brake for nothing; messages must be signed, and the AV must check
     them against its own sensors.
   - **Time and position:** a message is late by the time it arrives, and
     the sender's own position error is added to the object's, as on the
     pedestrian example.
   - **Standards and radio:** senders and receivers must agree on the
     message format and the radio. In the US, the FCC in 2020 cut the band
     kept for vehicle radio from 75 to 30 MHz and moved it from DSRC to
     C-V2X, noting that DSRC had barely been deployed.
   - **Bandwidth:** only object lists fit, so CSA is late fusion and inherits
     its cost: what the sender threw away is gone.
   - **Liability:** who is at fault when a shared detection was wrong?


.. admonition:: Where that leaves us: fusion
   :class: tip

   - Sensors meet **early** (raw data), **in the middle** (features, as in
     BEVFusion) or **late** (finished answers). Most production stacks are
     late.
   - **Frustum association on car B:** the camera's box picks the LiDAR's
     points. Its rear-face point projects to :math:`(876.7, 397.9)`, inside
     the box; 41 of 50 points cluster on car B; their centroid
     :math:`(10.99, -1.89)` is **1.0 m short** of its center.
   - **CSA:** another vehicle's detection, moved by its pose: the pedestrian
     **45 m** ahead of the AV, though the AV never saw it.



.. _l5-lec-tracking:

Tracking
--------

- **Where we are:** one picture of the scene, frame by frame. The detector
  does not know that the person in this frame is the person from the last
  one.
- **In this section:** the same object from one frame to the next: one
  Kalman filter per object, the filter of L3, and the decision of which
  detection belongs to which filter. The hard part is not the filter; it is
  that decision.
- **What it is for:** Level 2 of situation awareness: identity and velocity,
  which prediction (L9) needs.

.. admonition:: Definition: track
   :class: note

   One object followed over time: an **ID**, a state estimate with its
   covariance from a Kalman filter (L3), and a **status**: whether the
   planner is told about it yet.

The statuses come in :ref:`l5-lec-lifecycle`.


.. _l5-lec-kf-per-object:

One Kalman Filter per Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** New 3D boxes arrive, :math:`\Delta t = 0.1` s after the last
(chosen). They come from the LiDAR detector, or fused with the camera: the
tracker needs boxes in meters, and a camera box alone has no distance.
First: **where should car B be now?**

**What we have:** car B's track, from its filter's last update (L3), in fixed
ground coordinates, so a parked car stays put while the AV drives past. The
origin is put where the AV is now, to match the 3D box.

- Position :math:`(12.0, -2.0)` m.
- Speed 4.0 m/s along its heading of :math:`30^\circ` (chosen), so
  :math:`v = (3.46,\ 2.00)` m/s: 3.46 forward and 2.00 left. A real track
  gets its velocity from several frames, or from CenterPoint.
- State :math:`\mathbf{x} = [\,p_x,\ p_y,\ v_x,\ v_y\,]^\top`, constant
  velocity, L3's :math:`F`:

.. math::

   \hat{\mathbf{x}}^{-} = F\,\hat{\mathbf{x}} \qquad
   F = \begin{bmatrix} 1 & 0 & \Delta t & 0\\ 0 & 1 & 0 & \Delta t\\
                       0 & 0 & 1 & 0\\ 0 & 0 & 0 & 1 \end{bmatrix}

Here :math:`\hat{\mathbf{x}}` is the estimate after the last update and
:math:`\hat{\mathbf{x}}^{-}` is the prediction.

1. :math:`p_x`: :math:`12.0 + 3.46 \times 0.1 =` **12.35** m.
2. :math:`p_y`: :math:`-2.0 + 2.00 \times 0.1 =` **-1.80** m.
3. :math:`v_x, v_y`: unchanged, 3.46 and 2.00 m/s.

.. figure:: /_static/images/L5/track_predict.png
   :alt: A top view with a 1 m scale bar and a small x and y, left, arrow pair. Car B is a light blue car inside a dark blue rectangle turned 30 degrees. A gray arrow from its center, labeled v = (3.46, 2.00) m/s, drawn as 1 s of travel, points along the heading. A blue dot, after the last update at (12.0, -2.0) m, sits in a small blue ellipse. A short red arrow leads to a red dot, predicted 0.1 s later at (12.35, -1.80) m, inside a larger dashed red ellipse: P grows by Q (sketch).
   :width: 46%
   :align: center

   Car B's track. The **blue** dot is the estimate after the last update,
   :math:`(12.0, -2.0)` m. The **red** dot is the prediction 0.1 s later,
   :math:`(12.35, -1.80)` m. The gray arrow is the velocity, drawn as 1 s of
   travel. The ellipses are a sketch: :math:`P` grows by :math:`Q`.

**Next:** which new box is car B? The one nearest :math:`(12.35, -1.80)`;
the subsections below say how to measure "near".

.. admonition:: Question
   :class: hint

   Why isn't the heading in the state :math:`\mathbf{x}`?

.. dropdown:: Answer
   :color: success
   :icon: check-circle

   The velocity carries it: the direction of :math:`v`, the arc tangent of
   2.00 over 3.46, is :math:`30^\circ`. And :math:`F` stays a matrix; heading
   in the state needs :math:`\cos\theta`, so the EKF of L3. The cost: a
   stopped car has no heading, and a turn is predicted straight. Real
   trackers add heading with an EKF.


.. _l5-lec-track-loop:

Every Frame, the Same Loop
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** On every **frame**, the detector delivers a new list of boxes
(from the LiDAR detector, or fused with the camera), with no IDs: it does not
know that this frame's car B is last frame's car B. **The question:** which
box continues which track? The tracker answers in four steps, on every frame.

.. figure:: /_static/images/L5/track_loop.png
   :alt: Four boxes in a row joined by arrows: 1. Predict every track (Kalman filter); 2. Associate: pair detections with tracks; 3. Update matched tracks (Kalman filter); 4. Manage the rest: start, coast, delete. New detections from this frame enter box 2 from above. Confirmed tracks leave box 4 to the right, to prediction and planning. An arrow labeled next frame runs from box 4 back to box 1. Boxes 2 and 4 are green.
   :width: 95%
   :align: center

   The tracker's loop. **1. Predict** every track; **2. Associate** this
   frame's detections with tracks; **3. Update** the matched tracks; **4.
   Manage** the rest: start, coast, delete. Confirmed tracks go to prediction
   and planning, and the loop runs again on the next frame. Steps 2 and 4 are
   in green.

- **Steps 1 and 3** are the Kalman filter of L3, one per track.
- **Steps 2 and 4**, in green, are new: they are the rest of this section.
  The pairing is where trackers fail, and managing the rest decides when a
  track starts and when it ends.
- **The output:** confirmed tracks, each with an ID, a position and a
  velocity, go to prediction (L9) and planning.

**SORT**, "Simple Online and Realtime Tracking" (Bewley et al., 2016), is
this loop on image boxes, with the Hungarian algorithm for the pairing, which
comes below.


.. _l5-lec-four-decisions:

Four Decisions Every Frame
~~~~~~~~~~~~~~~~~~~~~~~~~~

In L3 every measurement belonged to the one thing we tracked. With more than
one object, that is no longer given.

**Scenario**, a sketch: three predicted tracks (step 1), four new boxes. Each
dashed ellipse is a **gate** (L3): the region around a track's prediction
where a detection is close enough to belong to it. A box outside a track's
gate cannot belong to that track. The tracker must decide:

1. which detection belongs to which track;
2. which detections are **new objects** that need a track;
3. which are **clutter**, false detections from noise or reflections;
4. which tracks got **nothing**, and whether they still exist.

.. figure:: /_static/images/L5/four_decisions.png
   :alt: A sketch, not to scale, of one frame seen from above: a two-lane road with the AV at the left facing right. Three predicted tracks are hollow circles, each in a dashed gate ellipse. Red dots are this frame's detections. One sits inside the gate of the track ahead of the AV, labeled 1: matched, inside a gate, and one inside the gate of a track in the left lane, labeled 1: matched. A red dot on the road near its right edge, outside every gate, is labeled 2: new object?. A red dot just off the road is labeled 3: clutter?. The farthest track has no detection in its gate, labeled 4: nothing this frame.
   :width: 95%
   :align: center

   One frame, a sketch, not to scale. Hollow circles are predicted tracks,
   each in its dashed gate; red dots are this frame's detections. **1:**
   matched, inside a gate (twice). **2:** a new object?, outside every gate.
   **3:** clutter?, off the road. **4:** a track with nothing this frame.

.. admonition:: Definition: data association
   :class: note

   Deciding which measurement belongs to which track, before any filter uses
   it.

Everyone thinks about the first decision. Real systems break on the last
two.


.. _l5-lec-wrong-match:

A Wrong Match Is Not a Small Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Association is a yes-or-no decision inside a filter that otherwise works with
smooth numbers, and that is what makes it dangerous.

.. important::

   A filter fed **noisy** measurements gets a little worse. A filter fed
   **another object's** measurements does not get a little worse: it
   settles, precisely and confidently, on a path **that never happened**.
   There is no "slightly wrong object".

The checks of L3, the **NIS** (normalized innovation squared) and the gate,
test whether the measurements fit the **track**. They cannot tell whether the
track follows the **right object**.


.. _l5-lec-gate:

A Match Depends on the Track's Uncertainty
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** The tracker follows car B. From the last frames, its Kalman
filter predicted where car B is now (the cross) and how far off that
prediction may be (the shaded circle: the predicted uncertainty, from L3).
This frame, a box lands 2 m from the cross. Is it car B? Two meters alone
cannot say. It depends on the size of the circle.

.. figure:: /_static/images/L5/nis_terms_plain.png
   :alt: A sketch of one track seen from above. A cross, the predicted position, sits in a shaded circle, labeled shaded, the uncertainty: how far from the cross the box may land. A green arrow runs from the cross to a black dot, labeled box: this frame's detection, and the miss: from the predicted position to the box, d m. A dashed circle around both, about three times the radius of the shaded circle, is labeled gate: close enough to match, about 3 times the uncertainty.
   :width: 60%
   :align: center

   One track. The **cross** is the predicted position; the **shaded**
   circle is the uncertainty, how far from the cross the box may land. The
   **green** arrow is the miss, :math:`d` m, from the prediction to this
   frame's box. The **dashed** circle is the gate, about 3 times the
   uncertainty.

.. admonition:: Definition: gate
   :class: note

   The region around a track's predicted position where a box can belong to
   that track. Ours: about 3 times the track's uncertainty, where 99 percent
   of the real car's boxes land if the uncertainty is honest (99 percent is
   our choice).

A box **outside** the gate cannot be car B. The gate is not a fixed number of
meters: a sure track (small circle) has a small gate, an unsure one a large
gate.

.. tip::

   See "The Match Distance" in :doc:`Going Further <l5_appendix>`: the same
   distance written with the math, as the NIS of L3.


.. _l5-lec-same-2m:

The Same 2 m, Two Answers
~~~~~~~~~~~~~~~~~~~~~~~~~

Two tracks, each with a box 2 m from its cross (uncertainties chosen for this
example). **Left:** car B, followed for many frames, so the filter is sure:
0.1 m. **Right:** a track started one frame ago, so it is unsure: 3 m.

.. figure:: /_static/images/L5/mahalanobis_plain.png
   :alt: Two panels, each with its own scale. Left, car B's track: sure. A blue cross in a tiny shaded circle, uncertainty 0.1 m, inside a dashed gate of 0.30 m; a box 2 m away is far outside; text: 2 m is 20 times its uncertainty: outside the gate; a 1 m scale bar. A legend: cross, predicted position; shaded, the uncertainty; dashed, the gate, about 3 times the uncertainty; each panel has its own scale. Right, a new track: unsure. A gray cross in a shaded circle, uncertainty 3 m, a box 2 m away inside it, and a dashed gate of 9.1 m around both; text: 2 m is less than its uncertainty: inside the gate; a 5 m scale bar.
   :width: 97%
   :align: center

   The same 2 m on two tracks; each panel has its own scale. **Left, car B's
   track, sure:** uncertainty 0.1 m, gate 0.30 m; the box is 20 times its
   uncertainty away, outside the gate. **Right, a new track, unsure:**
   uncertainty 3 m, gate 9.1 m; the box is less than one uncertainty away,
   inside the gate.

- **Left:** car B's gate is about 0.30 m. The box is 20 uncertainties away,
  far outside. Not car B.
- **Right:** the new track's gate is about 9 m. The same 2 m is less than one
  uncertainty, inside. It can be this track's car.

.. admonition:: The score
   :class: tip

   The tracker keeps this as one number, the squared **Mahalanobis
   distance** (Mahalanobis, 1936):

   .. math::

      \varepsilon = (\text{miss} \div \text{uncertainty})^2

   Left: :math:`20^2 = 400`. Right: :math:`(2 \div 3)^2 = 0.44`. The gate:
   :math:`\varepsilon < 9.21`, which is :math:`3.03^2`: the same three
   uncertainties.

.. tip::

   See "The Match Distance" in :doc:`Going Further <l5_appendix>`: the 2 m
   example, worked with the matrices.


.. _l5-lec-associate:

Four Ways to Associate
~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** Car B cuts in just behind car D; their gates overlap, so one
box can fall inside both. **The question:** given :math:`\varepsilon` for
every pair of track and box inside the gate, which pairs does the tracker
pick? Four answers, ordered by how much each one commits:

.. list-table::
   :widths: 12 42 46
   :header-rows: 1
   :class: compact-table

   * - **Method**
     - **How it works**
     - **What it costs**
   * - **NN**
     - Nearest neighbor: each track in turn takes its nearest detection
       inside the gate, if still free.
     - Simple and fast, but **the answer depends on which track goes first**;
       two crossing objects can swap identities.
   * - **GNN**
     - Global nearest neighbor: of the pairings that match the most tracks,
       the one with the lowest *total* distance, by the Hungarian algorithm
       (Kuhn, 1955).
     - One small optimization per frame, and no order effect. **The usual
       default.**
   * - **JPDA**
     - Joint probabilistic data association: updates each track with a
       probability-weighted blend of every detection in its gate (Fortmann et
       al., 1983).
     - Good in heavy clutter, but it struggles to start tracks and **can
       blend two objects into one**.
   * - **MHT**
     - Multiple hypothesis tracking: keeps several explanations across
       frames until later frames decide (Reid, 1979).
     - The most capable and the most expensive: old hypotheses must be
       pruned.

- **NN** commits at once, in an arbitrary order.
- **GNN** looks at the whole frame before it commits.
- **JPDA** does not commit within a frame: it blends.
- **MHT** does not commit across frames.

.. important::

   **Gate first** (:math:`\varepsilon < 9.21`): it removes most clutter
   before any of these runs, so each one runs faster and makes fewer
   mistakes. Exercise 11 on the :doc:`Exercises page <l5_exercises>` runs NN
   and GNN on one frame.


.. _l5-lec-lifecycle:

The Track Lifecycle
~~~~~~~~~~~~~~~~~~~

**Scenario.** A box matches no track: a new car, or a reflection? A confirmed
pedestrian walks behind a van: gone, or hidden? A track is not created the
moment something is detected, and not deleted the moment a detection is
missed. Each track has a **status**. **M of N** means at least M detections
in the last N frames; M and N are set by tuning.

.. figure:: /_static/images/L5/track_lifecycle.png
   :alt: A state diagram. An arrow from the label a detection that matched no track enters Tentative, where the planner is not told. Tentative leads to Confirmed, green, where the planner is told, when the track passes M of N, for example 3 detections in 5 frames. Confirmed leads to Coasting, predicted forward, like a pedestrian behind a van, on no detection, and back on detected again. Tentative leads to Deleted, red, removed, when it fails M of N. Coasting leads to Deleted when it goes too long with no detection.
   :width: 95%
   :align: center

   The four statuses. A detection that matched no track starts a
   **Tentative** track (the planner is not told). It becomes **Confirmed**
   (green, the planner is told) when it passes M of N, for example 3
   detections in 5 frames, or **Deleted** (red) when it fails. A confirmed
   track with no detection is **Coasting**, predicted forward, and returns to
   Confirmed when detected again; after too long with no detection it is
   Deleted.

- **Tentative:** a detection matched no track, so a new track starts, and
  nothing downstream is told.
- **Confirmed:** it passed an M of N test, say 3 detections in 5 frames; 3
  of 5 is only an example. Now it counts as a real object and the planner is
  told. Too strict, and you are slow to see real objects; too loose, and you
  confirm false alarms.
- **Coasting:** detections stopped, but the track is kept. A pedestrian who
  walked behind a van still exists.
- **Deleted:** it coasted too long.

.. important::

   Start a track on every detection and you track every false alarm. Delete
   on the first miss and every occlusion erases a pedestrian.

.. tip::

   See "Tracking in Industry" in :doc:`Going Further <l5_appendix>`: how
   real trackers set these rules.


.. _l5-lec-coasting:

Between Confirmed and Coasting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario.** A confirmed pedestrian walks behind a parked van. Every frame,
the tracker first predicts every track forward, hers too. Then one of three
things happens:

1. **No detection in the gate.** The Kalman filter has nothing to update
   with, so the track moves on its prediction alone. Its uncertainty grows
   every frame, and so does its gate. The track is now **Coasting**, and the
   planner is still told, so it can slow down for a pedestrian it cannot see.
2. **A detection inside the grown gate.** The pedestrian steps out from
   behind the van. The filter updates, the uncertainty shrinks, and the track
   is **Confirmed** again, with the same ID.
3. **No detection for too long.** After 1 s with none (our tracker's
   setting), the track is **Deleted**.

.. important::

   Coasting keeps the identity. When the pedestrian reappears, she gets her
   old track and its velocity back. Without coasting, she would start a new
   tentative track, and the planner would hear about her only after M of N
   frames.


.. _l5-lec-tempe:

Tempe, March 2018: What the Tracker Did
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario** (L1). Tempe, Arizona, at night. A developmental test vehicle in
automated mode hits a pedestrian walking a bicycle across the road, outside
a crosswalk. **The question:** the system detected her 5.6 s before impact;
why did it not brake in time? Every time below is from the NTSB report.

.. figure:: /_static/images/L5/tempe_timeline.png
   :alt: A time axis of seconds before impact, from 6 on the left to 0, impact, on the right. A tick at 5.6 s: radar detects her (as a vehicle). A tick at 5.2 s: LiDAR detects her (as an unknown object). A yellow band from 5.6 to 1.2 s: class keeps changing: vehicle, other, bicycle; the tracking history is dropped at each change. A red tick at 1.2 s: her location is in the path: emergency. A red band from 1.2 to 0.2 s: braking held back 1 s, by design.
   :width: 98%
   :align: center

   The timeline, in seconds before impact, from the NTSB report. 5.6 s:
   radar detects her (as a vehicle). 5.2 s: LiDAR detects her (as an unknown
   object). **Yellow**, 5.6 to 1.2 s: her class keeps changing, and the
   tracking history is dropped at each change. **Red**, from 1.2 s: her
   location is in the path, an emergency, and braking is held back 1 s by
   design.

- **5.6 s** before impact the radar detected her, as a vehicle; at **5.2 s**
  the LiDAR detected her, as an unknown object. She was in the sensor data
  from then on.
- **The yellow band.** Between 5.6 and 1.2 s her class kept changing:
  vehicle, other, bicycle, never pedestrian. The report says what the
  software did with each change, in its words: "If the perception process
  changed the classification of a detected object, it **no longer considered
  the tracking history** of that object." So it never predicted her path
  across the road.
- **1.2 s.** Only when her location was in the vehicle's path did the system
  see an emergency. Braking was then held back for one second by design, and
  the operator, who was looking down, did not take over in time.


.. _l5-lec-tempe-terms:

Tempe, in Tracking Terms
~~~~~~~~~~~~~~~~~~~~~~~~

**The question:** what did dropping the tracking history do? The report says
that with each new class, the system saw her as **a new object**. In our
words, each change started a new track. A track restarted every few frames
never builds a history:

1. No history, so **no velocity** estimate.
2. No velocity, so **no predicted path** across the road.
3. No predicted path, so **nothing to brake for** until 1.2 s.

.. important::

   The vehicle's detection saw her and its filter did its job, on a track
   that kept starting over. **The fix is in the design: track the object,
   and classify it separately.** A track's ID must not depend on its class.


.. admonition:: Where that leaves us: tracking
   :class: tip

   - **One Kalman filter per object:** predict all tracks (car B to
     :math:`(12.35, -1.80)`), associate, update the matched ones, manage the
     rest.
   - **Distance:** :math:`\varepsilon = \boldsymbol{\nu}^\top S^{-1}\boldsymbol{\nu}`,
     the NIS of L3 (written out in the appendix), gate 9.21. The same 2 m
     gave 400 for a well-known track and 0.44 for a new one.
   - **Association:** GNN, not NN. In Exercise 11, NN gives 13.0 or 11.3
     depending on the order, and GNN gives 11.3.
   - **Lifecycle:** tentative, confirmed, coasting, deleted. Tempe: a track
     that keeps starting over gives **no velocity, no path, no brake**.


.. _l5-lec-tracking-handson:

Hands-On: a Tracker on CARLA's Traffic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This one is for after class too.

- **What it does:** the ROS 2 package ``l5_tracking_demo`` runs this
  section's tracker on CARLA's traffic: one Kalman filter per object, the
  gate :math:`\varepsilon < 9.21`, GNN or NN, and the track lifecycle (M of
  N). Detections come from the LiDAR, clustered, or from CARLA's own objects
  with noise added (``source:=truth``). With evaluation on, it grades the
  tracks against CARLA's ground truth.
- **To run it:** the commands, the tasks and the measured results are on
  :ref:`the Code page <l5-tracking-demo>` and in the package's
  `README <https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros/blob/main/l5_tracking_demo/README.md>`__.

.. admonition:: Try
   :class: hint

   - ``association:=nn`` against the default GNN, and count the ID switches.
   - ``source:=truth flip_prob:=0.3 reset_on_class_change:=true`` to see
     Tempe: a new track on every class change, with flipping labels. The
     velocity never builds up.


.. _l5-lec-next:

Next Class
----------

.. admonition:: Today
   :class: important

   - **Level 1, perception:** 3D boxes in meters; a class per pixel; the BEV
     grid and occupancy from cameras; camera and LiDAR fused, and other
     vehicles' detections too.
   - **Level 2, comprehension:** one Kalman filter per object, data
     association with the NIS gate, and a lifecycle that keeps identity
     stable.

- **L7, Localization and SLAM:** where the AV itself is. We needed that twice
  today without saying so: the CSA example needed the sender's position, and
  the tracker's fixed frame needs the AV's.
- **Level 3, projection,** where everyone will be in a few seconds, is L9,
  Prediction.

**Before next class**

- Run the four hands-on packages on the :doc:`Code page <l5_code>`:
  ``l5_box_demo``, ``l5_seg_demo``, ``l5_bev_demo`` and
  ``l5_tracking_demo``.
- **Read the appendix** (:doc:`l5_appendix`): inside CenterPoint, one pixel
  onto the grid, Lift and Splat by hand, BEVFormer, the match distance, and
  tracking in industry.
- Work through the :doc:`L5 exercises <l5_exercises>`.


.. rubric:: Image credits

The vehicle icons in the figures on this page were created by Stone from the
`Noun Project <https://thenounproject.com>`_.
