====================================================
Glossary
====================================================

:ref:`A <glossary-a>` · :ref:`B <glossary-b>` · :ref:`C <glossary-c>` · :ref:`D <glossary-d>` · :ref:`E <glossary-e>` · :ref:`F <glossary-f>` · :ref:`G <glossary-g>` · :ref:`H <glossary-h>` · :ref:`I <glossary-i>` · :ref:`J <glossary-j>` · :ref:`K <glossary-k>` · :ref:`L <glossary-l>` · :ref:`M <glossary-m>` · :ref:`N <glossary-n>` · :ref:`O <glossary-o>` · :ref:`P <glossary-p>` · :ref:`Q <glossary-q>` · :ref:`R <glossary-r>` · :ref:`S <glossary-s>` · :ref:`T <glossary-t>` · :ref:`U <glossary-u>` · :ref:`V <glossary-v>` · :ref:`W <glossary-w>` · :ref:`Y <glossary-y>` · :ref:`Z <glossary-z>`

.. only:: html

   .. raw:: html

      <div id="glossary-search-wrap" style="margin: 1.2em 0 0.6em 0;">
        <input
          id="glossary-search"
          type="search"
          placeholder="Filter terms..."
          autocomplete="off"
          spellcheck="false"
          style="
            width: 100%;
            max-width: 480px;
            padding: 0.45em 0.75em;
            font-size: 1em;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
          "
        />
        <span
          id="glossary-search-count"
          style="margin-left: 0.8em; font-size: 0.88em; color: #666;"
        ></span>
      </div>

      <div id="glossary-lecture-filter"
           style="margin: 0 0 1.4em 0; display: flex; flex-wrap: wrap; gap: 0.35em; align-items: center;">
        <span style="font-size: 0.88em; color: #666; margin-right: 0.3em;">Lecture:</span>
        <button type="button" data-lecture="all"
                style="padding: 0.25em 0.7em; font-size: 0.85em; border: 1px solid #888;
                       background: #444; color: #fff; border-radius: 3px; cursor: pointer;">
          All
        </button>
        <!-- L1..L14 buttons inserted by JS -->
      </div>

      <script>
      (function () {
        /* Run after the DOM is ready. */
        function initGlossarySearch() {
          var input  = document.getElementById('glossary-search');
          var count  = document.getElementById('glossary-search-count');
          var filterBar = document.getElementById('glossary-lecture-filter');
          if (!input || !filterBar) return;

          var TOTAL_LECTURES = 14;
          var activeLecture = null;  /* null = "All" */

          /* Build L1..L14 buttons. */
          for (var i = 1; i <= TOTAL_LECTURES; i++) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.dataset.lecture = 'L' + i;
            btn.textContent = 'L' + i;
            btn.style.cssText =
              'padding: 0.25em 0.6em; font-size: 0.85em; ' +
              'border: 1px solid #ccc; background: #fff; color: #333; ' +
              'border-radius: 3px; cursor: pointer;';
            filterBar.appendChild(btn);
          }

          /* Cache lecture tags per <dt> so we don't rescan the DOM on every keystroke.
             A "tag" is the visible text of any link inside the dd block matching ^L\d+$. */
          var dtIndex = [];  /* { dt, dds, tags: Set<string>, text: lowercased dt text } */
          document.querySelectorAll('dl.glossary dt').forEach(function (dt) {
            var dds = [];
            var node = dt.nextElementSibling;
            while (node && node.tagName === 'DD') {
              dds.push(node);
              node = node.nextElementSibling;
            }
            var tags = new Set();
            dds.forEach(function (dd) {
              dd.querySelectorAll('a').forEach(function (a) {
                var t = a.textContent.trim();
                if (/^L\d+$/.test(t)) tags.add(t);
              });
            });
            dtIndex.push({ dt: dt, dds: dds, tags: tags, text: dt.textContent.toLowerCase() });
          });

          function getLetterSection(el) {
            var node = el;
            while (node && node !== document.body) {
              if (node.id && /^glossary-[a-z]$/i.test(node.id)) return node;
              node = node.parentElement;
            }
            return null;
          }

          function paintButtons() {
            filterBar.querySelectorAll('button').forEach(function (b) {
              var isActive = (b.dataset.lecture === 'all' && activeLecture === null) ||
                             (b.dataset.lecture === activeLecture);
              if (isActive) {
                b.style.background = '#444';
                b.style.color = '#fff';
                b.style.borderColor = '#888';
              } else {
                b.style.background = '#fff';
                b.style.color = '#333';
                b.style.borderColor = '#ccc';
              }
            });
          }

          function run() {
            var query = input.value.trim().toLowerCase();
            var visible = 0;

            dtIndex.forEach(function (entry) {
              var textMatch = !query || entry.text.indexOf(query) !== -1;
              var lectureMatch = !activeLecture || entry.tags.has(activeLecture);
              var match = textMatch && lectureMatch;

              entry.dt.style.display = match ? '' : 'none';
              entry.dds.forEach(function (dd) { dd.style.display = match ? '' : 'none'; });
              if (match) visible++;
            });

            /* Hide letter-section headings + dl when every term inside is hidden. */
            document.querySelectorAll('dl.glossary').forEach(function (dl) {
              var anyVisible = Array.prototype.some.call(
                dl.querySelectorAll('dt'),
                function (dt) { return dt.style.display !== 'none'; }
              );
              dl.style.display = anyVisible ? '' : 'none';

              var section = getLetterSection(dl);
              if (section) {
                section.style.display = anyVisible ? '' : 'none';
              } else {
                var prev = dl.previousElementSibling;
                while (prev) {
                  if (prev.tagName === 'H2' || prev.tagName === 'H1') {
                    prev.style.display = anyVisible ? '' : 'none';
                    break;
                  }
                  prev = prev.previousElementSibling;
                }
              }
            });

            /* Result count: show whenever a filter is active. */
            if (query || activeLecture) {
              count.textContent = visible === 1
                ? '1 term found'
                : visible + ' terms found';
            } else {
              count.textContent = '';
            }
          }

          /* Wire up the lecture-chip clicks (event delegation). */
          filterBar.addEventListener('click', function (e) {
            var btn = e.target.closest('button[data-lecture]');
            if (!btn) return;
            var lec = btn.dataset.lecture;
            activeLecture = (lec === 'all') ? null : lec;
            paintButtons();
            run();
          });

          input.addEventListener('input', run);
          input.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') { input.value = ''; run(); input.blur(); }
          });

          paintButtons();
        }

        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', initGlossarySearch);
        } else {
          initGlossarySearch();
        }
      })();
      </script>

----


.. _glossary-a:

A
=

.. glossary::

   Accuracy
      How close a measurement is to the true value. Strictly (ISO
      5725-1), accuracy means both at once: small bias (good trueness)
      and small noise (good precision). A sensor with a steady offset
      can be highly precise and still inaccurate. See Bias, Trueness and
      Precision (Measurement). :doc:`L2 </lectures/lecture2/l2_index>` ·
      :doc:`L3 </lectures/lecture3/l3_index>`

   Activation Function
      The function a neuron applies to its weighted sum, written
      :math:`\sigma` (here not the standard deviation). Without one, depth
      adds nothing: a weighted sum of weighted sums is still one weighted
      sum, so a hundred stacked layers act like one. ReLU and SiLU are
      two examples, and YOLOv8 uses SiLU. See Neuron.
      :doc:`L4 </lectures/lecture4/l4_index>`

   ADAS
      Advanced Driver Assistance Systems. Systems that do part of the
      DDT while the human monitors continuously and stays the fallback,
      always and immediately. SAE Levels 1 and 2. Examples: adaptive
      cruise, lane keeping, hands-off highway. Capability does not
      decide it: a very capable system that still needs an attentive
      driver is an ADAS. :doc:`L1 </lectures/lecture1/l1_lecture>`

   ADS
      Automated Driving System. A system that performs all of the DDT
      within its ODD. The system, not the human, monitors the road. It
      covers SAE Levels 3, 4 and 5. The levels differ in who handles
      the fallback: at Level 3 the human, on request; at Levels 4 and 5
      the system itself. Not to be confused with UMD's Accessibility
      and Disability Service, which shares the abbreviation.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   AEB
      Automatic Emergency Braking. A momentary intervention that applies the
      brakes to avoid or mitigate a collision. Despite taking control of the
      vehicle it is classified as **SAE Level 0**, because the human never
      stops performing the DDT. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Anchor Box
      A preset box shape that a detector adjusts to fit each object.
      L4's YOLOv8 uses none: each grid cell predicts four distances
      from its center to the box edges, so YOLOv8 is called
      anchor-free. :doc:`L4 </lectures/lecture4/l4_index>`

   A* Search
      A heuristic graph-search algorithm that finds the shortest path from
      start to goal by expanding the node with the lowest :math:`f(n) =
      g(n) + h(n)`, where :math:`g` is the cost so far and :math:`h` is an
      admissible heuristic. Used for global route planning on the road
      graph and for grid/lattice-based motion planning. L8 · L10

   Angle Wrapping
      Bringing every angle back into the range -180° to 180°, with
      ``np.arctan2(np.sin(a), np.cos(a))``. 179° and -179° are 2° apart,
      not 358°. Subtract them the naive way and the filter sees a huge
      surprise and swings the AV almost all the way around. An EKF wraps
      in three places: inside :math:`f`, in the surprise
      :math:`\boldsymbol{\nu}`, and in :math:`\hat{\mathbf{x}}` after the
      update. :doc:`L3 </lectures/lecture3/l3_index>`

   Angular Resolution
      The smallest angular separation at which two returns can still be
      told apart. Because it is an angle, the width it covers grows with
      range: 2 degrees spans 3.5 m at 100 m, which is a car and the
      motorcycle beside it. :doc:`L2 </lectures/lecture2/l2_index>`

   AP (Average Precision)
      The area under the precision-recall line for one class. At each
      recall, the line keeps the best precision at that recall or
      beyond. In L4's example (3 people, 5 detections ranked by
      confidence), AP = 0.333 + 0.333 + 0.250 = 0.917. The average of
      AP over all classes is mAP. Papers often write mAP@0.5:0.95
      simply as "AP". :doc:`L4 </lectures/lecture4/l4_index>`

   ASIL
      Automotive Safety Integrity Level. Defined by ISO 26262 to classify
      the severity of safety risks. Ranges from ASIL A (lowest) to ASIL D
      (highest), determining the rigor of development and testing required. :doc:`L1 </lectures/lecture1/l1_lecture>` · L14

   ASPP
      Atrous Spatial Pyramid Pooling. The multi-scale context module in
      DeepLabv3+ that applies parallel dilated convolutions at several
      rates (e.g., 6, 12, 18) and pools at multiple scales, then
      concatenates the outputs. That captures objects at varying scales in
      a single forward pass. :doc:`L5 </lectures/lecture5/l5_index>`

   Attention
      A step that gives each token a new vector: a weighted average of
      all the tokens, where each weight says how much that token
      matters to it. The weights are computed from the tokens for each
      image, and add up to 1:
      :math:`\text{softmax}(QK^\top/\sqrt{d})\,V`. One attention layer
      reads every cell of the image, where one :math:`3 \times 3`
      convolution reads only the 8 neighbors. :math:`N` tokens make
      :math:`N^2` pairs. :doc:`L4 </lectures/lecture4/l4_index>`

   Automated Driving Feature
      SAE J3016's name for Levels 3 to 5. The system performs the
      entire DDT within its ODD. The three levels differ in who handles
      the DDT fallback: the human on request at Level 3, the system
      itself at Levels 4 and 5. Contrast Driver Support Feature.
      :doc:`L1 </lectures/lecture1/l1_index>`

   Axis Trap
      The mismatch between two names for the same three directions. The
      intrinsic matrix :math:`K` assumes the optical convention: *x*
      right, *y* down, *z* forward along the optical axis. CARLA, like
      most robotics and game engines, uses *x* forward, *y* right, *z*
      up. A permutation matrix :math:`P` relabels the axes before
      :math:`K` sees them. Leave :math:`P` out and you get no error and
      a garbage image: every point lands off the image. Get one sign
      wrong and the scene comes out upside down. Derive :math:`P` from
      your own convention rather than copying it.
      :doc:`L2 </lectures/lecture2/l2_index>`


.. _glossary-b:

B
=

.. glossary::

   Backbone
      The first part of a detector: a CNN, or a ViT, that turns the
      image into feature maps. YOLOv8s's backbone turns a
      :math:`480 \times 640` image into three maps, at strides 8, 16 and
      32, with 128, 256 and 512 channels. A backbone is often
      pretrained on a large image collection, then reused. See Neck and
      Head (Detection). :doc:`L4 </lectures/lecture4/l4_index>`

   Backpropagation
      The algorithm that computes the gradients of the loss for all the
      weights at once, working backward from the output. Gradient descent
      then uses those gradients to move the weights.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Base Link
      The one agreed point on the AV that its position refers to: the
      middle of the rear axle, as in Autoware. The rear wheels do not
      steer, so if the tires do not slip, this point always moves along
      the heading, never sideways. In the L3 road frame, the AV at
      (103.0, 2.5) means its base link is 103.0 m along the road and
      2.5 m across from the survey marker.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Baseline
      The distance between the two optical centres of a stereo pair,
      written B. Depth error grows as z squared over Bf, so the baseline
      is the only term a designer controls, and it is bounded by the
      width of the vehicle. :doc:`L2 </lectures/lecture2/l2_index>`

   Bearing
      The angle between the AV's nose and a target, written
      :math:`\beta`, positive to the left. For a sign at
      :math:`(x_s, y_s)` it is
      :math:`\operatorname{atan2}(\Delta y, \Delta x) - \theta`: the
      direction to the sign measured from east, minus the heading. With
      the range :math:`r`, it is what the camera reports in L3's EKF.
      It is an angle, so its surprise must be wrapped.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Behavior Cloning
      An imitation learning approach where a policy is trained by supervised
      regression on expert state-action pairs. Simple but suffers from
      distribution shift and compounding errors that grow as
      :math:`O(\epsilon T^2)`. L12

   Behavior Planning
      The strategic decision-making layer that selects high-level maneuvers
      (lane follow, lane change, yield, stop) based on the current driving
      context. Often implemented as a finite state machine (FSM). L9

   Belief
      The probability of every possible state, given everything measured
      so far: for every position the AV could be at, how likely it is to
      really be there. A Kalman filter keeps it as one bell curve (the
      estimate sets the peak, the covariance :math:`P` sets the width),
      so it has a single peak. A particle filter keeps it as weighted
      particles, so it can have several, such as two identical ceiling
      lights 25 m apart. :doc:`L3 </lectures/lecture3/l3_index>`

   BEV
      Bird's-Eye View. A top-down representation of the driving scene that
      projects sensor data into an ego-centric 2D plane. The dominant
      perception paradigm in modern AV systems. See also: BEVFormer. :doc:`L4 </lectures/lecture4/l4_index>` · :doc:`L5 </lectures/lecture5/l5_index>`

   BEVFormer
      A transformer-based BEV construction method (Li et al., ECCV 2022)
      that uses learnable BEV queries with spatial cross-attention and
      temporal self-attention to build BEV features from multi-camera images. :doc:`L5 </lectures/lecture5/l5_index>`

   BEVFusion
      A multi-sensor BEV fusion framework that unifies camera and LiDAR
      features in a shared BEV space using learned attention-weighted
      aggregation. L6

   Bias
      A systematic error that shifts every reading the same way. Unlike
      noise it does not average away, however many readings you take,
      and a Kalman filter does not remove it, because it breaks the
      no-bias assumption; in L3 we widen :math:`Q` to cover it. Two
      sensors can have identical variance and very different bias:
      receivers A and B both scatter by 1.561 m, but B's average sits
      3.2 m ahead, far more than the 0.64 m (:math:`\sigma/\sqrt{6}`)
      that noise alone would explain. Finding bias needs the truth from
      outside. :doc:`L2 </lectures/lecture2/l2_index>` ·
      :doc:`L3 </lectures/lecture3/l3_index>`

   Bias (Neuron)
      The one extra number :math:`b` that a neuron adds to its weighted
      sum before the activation:
      :math:`y = \sigma(w_1 x_1 + w_2 x_2 + \dots + b)`. Training sets it
      together with the weights. Not the measurement bias of L2 and L3:
      see Bias. :doc:`L4 </lectures/lecture4/l4_index>`

   Bicycle Model
      A simplified kinematic vehicle model that merges the two front wheels
      and two rear wheels into single virtual wheels. Used as the foundation
      for motion planning and control. L10 · L11

   Bipartite Matching
      The Hungarian algorithm used by DETR to find an optimal one-to-one
      assignment between predicted objects and ground truth during training.
      Eliminates the need for NMS. :doc:`L4 </lectures/lecture4/l4_index>`

   Blueprint Library
      In CARLA, the collection of blueprints. A blueprint is a
      template for creating an actor (a vehicle, pedestrian or
      sensor), with attributes such as color or a sensor's settings.
      Nothing exists in the world until you spawn an actor from one.
      :doc:`L2 </lectures/lecture2/l2_index>`

   B-Spline
      A piecewise polynomial curve with local control point support, used
      for smooth trajectory representation in motion planning. Changes to
      one control point only affect a local segment of the curve. L11

   ByteTrack
      A multi-object tracking method (Zhang et al., 2022) that recovers
      occluded objects by performing a second association pass using
      low-confidence detections that other trackers would discard. L6


.. _glossary-c:

C
=

.. glossary::

   Calibration
      Comparing a sensor against something you already trust, and
      keeping the numbers that turn its raw readings into real-world
      quantities. The VIM (2012) gives the formal definition. The
      numbers are not in the data: you measure them once, then keep
      checking them. For a LiDAR and a camera it takes two pieces: the
      camera's intrinsics and the extrinsic between the two sensors.
      Calibration is not fusion. It tells you which pixel a LiDAR point
      lands on, not whether both sensors see the same object.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Calibration (Extrinsic)
      See Extrinsic Calibration. :doc:`L2 </lectures/lecture2/l2_index>`

   Calibration (Intrinsic)
      See Intrinsic Calibration. :doc:`L2 </lectures/lecture2/l2_index>`

   CARLA
      CAR Learning to Act. An open-source autonomous driving simulator
      built on Unreal Engine, providing realistic urban/highway
      environments, sensor simulation, and a Python API.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Channel
      One feature map in a layer's output. A layer outputs one channel
      per filter: 32 for YOLOv8s's first layer, 512 at the end of its
      backbone. Deeper layers have smaller grids and more channels.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Chi-Square Gate
      A test that throws away a reading whose NIS exceeds a threshold
      taken from the chi-square distribution. For a sign match reporting
      :math:`x` and :math:`y` (2 degrees of freedom), the 99 percent
      line is 9.21. See Gating. :doc:`L3 </lectures/lecture3/l3_index>` ·
      :doc:`L5 </lectures/lecture5/l5_index>`

   Class Token
      One extra token put in front of the patch tokens (Dosovitskiy et
      al., 2021). Its 768 numbers are set by training and are the same
      for every image. The encoder mixes every patch into it, and the
      head reads the answer from it alone.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Classification
      Given an image and a fixed set of :math:`K` classes, output one
      score per class, :math:`p_1, \dots, p_K`, each at least 0 and
      adding up to 1. The label is the class with the highest score,
      :math:`\hat{y} = \arg\max_k p_k`. It gives one label for the
      whole image and no box. On L4's street image, YOLOv8s-cls says
      "police van" with a score of 0.616; the image shows a city bus.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Closed-Loop Evaluation
      Evaluating a system in a setting where its own decisions change what
      happens next, so errors compound as they do on a road. The only way to
      observe recovery, or a small error growing into a large one. Contrast
      :term:`Open-Loop Evaluation`. L13

   CNN
      Convolutional Neural Network. A network built mostly from
      convolutions. One layer reads only a small window (3 by 3 cells),
      with the same filter everywhere, so its cost grows with the number
      of cells and it learns from less data than a transformer. YOLOv8s
      is a CNN. RT-DETR-L uses a CNN backbone, then a transformer.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Collision Detection
      The geometric test that determines whether a candidate path or
      trajectory intersects any obstacle (often expressed as inflated
      bounding boxes, OBBs, or Minkowski sums). Run at every node
      expansion during sampling- and graph-based planning. L10

   Complementarity
      See Complementarity Principle. :doc:`L2 </lectures/lecture2/l2_index>`

   Complementarity Principle
      Different sensing modalities have strengths and weaknesses that
      balance each other. Combined, they are more robust than any one of
      them alone (Luo, 1989). In L2's Venn diagram, a circle alone is what
      only that sensor gives, an overlap is what a pair gives together, and
      the middle answers what a planner needs: what it is, where it is, how
      fast it is going. :doc:`L2 </lectures/lecture2/l2_index>`

   Concept-to-Road Pipeline
      The seven stages an ADS goes through to reach a public road:
      Framework, Specify, Build, Validate, Argue, Approve, and Operate
      and monitor. It is not a release. It is a negotiation between a
      developer, standards bodies and a regulator. Stage 4 takes almost
      all the calendar time, and the vehicle runs at Level 2 the whole
      way through it. Every software update in Stage 7 changes the
      system that the approval in Stage 6 was granted for.
      :doc:`L1 </lectures/lecture1/l1_index>`

   Concrete Scenario
      A :term:`Logical Scenario` with every parameter fixed to a value, and
      therefore the only scenario layer that can actually be executed. One
      logical scenario yields thousands of concrete ones, which is why test
      selection is a sampling problem. L13

   Confidence (Detection)
      The number from 0 to 1 that comes with each box: how strongly the
      detector scores the class it names for that box. The head gives a
      raw score per class, a sigmoid maps it into 0 to 1, and the
      highest class wins. It is not the probability of being right, and
      0.5 in one model is not 0.5 in another. Not the confidence of a
      confidence interval. :doc:`L4 </lectures/lecture4/l4_index>`

   Confidence Interval
      A range built from data by a stated procedure. A 95 percent
      confidence level means that about 95 percent of intervals built
      that way would contain the true value. It does **not** mean there
      is a 95 percent probability that the true value lies inside the
      one interval you are holding. :doc:`L3
      </lectures/lecture3/l3_index>`

   Confidence Level
      The proportion of intervals produced by a repeated procedure that
      would contain the true value. A statement about the procedure, not
      about any single interval. See Confidence Interval. :doc:`L3
      </lectures/lecture3/l3_index>`

   Configuration Space
      The space of all possible vehicle configurations, typically
      :math:`(x, y, \theta)` for a planar robot. Obstacles are mapped into
      configuration space to simplify collision checking during planning. L10

   Contextual Embedding
      A token's vector after the encoder layers: it describes its patch
      together with what surrounds it, because attention mixed in the
      other tokens. In L4, the same patch pasted into a CARLA frame
      starts with the same vector as in the street image (similarity 1)
      and ends near 0.3 after 12 layers. Contrast Static Embedding.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Conspicuity
      The DDT subtask of making the vehicle's presence and intent visible to
      other road users: lights, indicators, horn, gestures. A genuine gap in
      the field, and not covered in this course: a vehicle that cannot
      signal its intent to a human is hard to share a road with. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Control Input
      What the AV knows it did during one step, written
      :math:`\mathbf{u}`, fed into the motion model through :math:`B` in
      the Kalman filter or :math:`f` in the EKF. In the L3 tunnel it is
      the IMU's acceleration; in the EKF it is the wheel speed and the
      gyro's turn rate, :math:`[v, \omega]`, whose noise builds
      :math:`Q_k`. :doc:`L3 </lectures/lecture3/l3_index>`

   Control Matrix
      The matrix :math:`B` that turns the control input
      :math:`\mathbf{u}` into changes of the state. Accelerating at
      :math:`a` for :math:`\Delta t` adds :math:`\Delta t\,a` to a
      velocity and :math:`\tfrac{1}{2}\Delta t^2 a` to a position: with
      :math:`\Delta t = 0.1` s, that is :math:`0.1\,a` and
      :math:`0.005\,a`. In the L3 hands-on, leaving :math:`B\mathbf{u}`
      out of the predict step takes the error along the tunnel from
      1.06 m to 3.58 m. :doc:`L3 </lectures/lecture3/l3_index>`

   Convolution
      The operation every CNN is built on. Slide a small grid of weights,
      the filter, over the input. At each position, multiply cell by cell
      and add, so each position gives one output number. A 3 by 3 filter
      on a 5 by 5 input gives a 3 by 3 output. A filter spans all input
      channels, so a layer with kernel size :math:`k` has
      :math:`k \times k \times C_\text{in} \times C_\text{out}` weights:
      864 for YOLOv8s's first layer (measured). Strictly the operation is
      cross-correlation, but the weights are learned, so the flip makes
      no difference. :doc:`L4 </lectures/lecture4/l4_index>`

   Cooperative Perception
      Multiple vehicles or roadside units sharing sensor data via V2X
      communication to build a collective, extended understanding of the
      driving scene beyond any single vehicle's sensor range. L14

   Coordinate Frame
      An agreed origin and set of axes. The LiDAR reports points in its
      own frame, the camera in its own, and the vehicle in a third, so
      two readings can be compared only after a transform puts them in
      one frame. In L2 the word *frame* also means one camera image or
      one LiDAR sweep. Where the meaning is unclear, the notes say
      *coordinate frame* or *image*.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Covariance
      How much the errors in two quantities move together: the same
      recipe as variance, but multiply each :math:`x` distance from its
      mean by the :math:`y` distance, then average. Positive: too far
      ahead usually comes with too far left. Zero when the two are
      unrelated. Two variances give the width and height of a cloud of
      readings; the covariance gives its lean.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Covariance Matrix
      A square matrix holding variances on the diagonal and covariances
      off it. In a Kalman filter, P is the covariance of the error: the
      gap between the estimate and where the AV truly is. Off-diagonal
      terms appear on their own during prediction, because advancing
      position using velocity links the two.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Correlated Errors
      Errors that move together, so knowing one tells you something
      about the other. In L3's leaning cloud of readings, 48 of the 62
      readings ahead of the truth are also to the left; in the upright
      cloud, 32 of 62, about half. Covariance measures it. In the
      tunnel filter, predict ties speed to position (correlation
      +0.79), and that link is how a sign match, which reads only
      position, also corrects speed.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Coverage Interval
      The term the GUM and the VIM use in place of confidence interval,
      paired with coverage probability in place of confidence level.
      Metrology prefers these because they avoid the common misreading
      of the word confidence. :doc:`L3 </lectures/lecture3/l3_index>`

   Credible Region
      A Bayesian region that contains the true value with a stated
      probability, given the model; it differs from a confidence
      interval (see the L3 references). In two dimensions, with
      independent east and north errors of the same :math:`\sigma`, a
      circle must reach :math:`2.45\sigma` to hold 95 percent of
      readings, against :math:`2\sigma` on one axis.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Cross-Attention
      Attention in which the queries come from a different set than the
      keys and values. In DETR's decoder, the object queries ask the
      image tokens "is my object here?". BEVFormer uses it to fill a
      map of the ground from camera images. Contrast Self-Attention.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Cross-Attention Fusion
      A deep learning fusion approach that uses transformer cross-attention
      mechanisms to learn how features from one sensor modality should
      attend to features from another (e.g., camera features attending to
      LiDAR features in BEVFusion). L6

   Cross-Covariance
      In the UKF update, :math:`P_{xz}`: how the state and the reading
      move together. For each sigma point, multiply how far it sits
      from the prediction by how far its expected reading sits from
      :math:`\hat{\mathbf{z}}`, weight the product, and add them all up.
      It takes the place of :math:`P^- H^\top` in the gain,
      :math:`K = P_{xz} S^{-1}`, and comes from the points, not from a
      Jacobian. :doc:`L3 </lectures/lecture3/l3_index>`

   Cross-Entropy Loss
      The loss that training makes smaller for classification: minus the
      natural log of the probability the network gave the correct class,
      :math:`L = -\ln p_\text{correct}`. With softmax outputs 0.659, 0.242
      and 0.099 for bus, person and car, the loss is 0.417 if the truth
      is bus, 1.417 if person and 2.317 if car. A network that is sure
      and right scores 0. The less probability the network gives the
      truth, the larger the loss. :doc:`L4 </lectures/lecture4/l4_index>`

   Cross-Track Error
      The lateral distance between the vehicle (typically measured at the
      front axle for Stanley, rear axle for Pure Pursuit) and the nearest
      point on the reference path. Drives the steering correction in both
      controllers. L11

   CTRA
      Constant Turn Rate and Acceleration. A physics-based motion prediction
      model that assumes constant yaw rate and longitudinal acceleration.
      More realistic than constant-velocity models for curving trajectories. L9

   C-V2X
      Cellular Vehicle-to-Everything. A 3GPP-based V2X communication
      standard (LTE-V2X, NR-V2X/5G) that leverages cellular infrastructure
      for vehicle communication. Competing with DSRC for V2X deployment. L14


.. _glossary-d:

D
=

.. glossary::

   DAgger
      Dataset Aggregation. An iterative imitation learning algorithm that
      addresses distribution shift by collecting new training data under
      the learner's own policy, then re-labeling with the expert's actions.
      Reduces per-step regret from :math:`O(\epsilon T^2)` (BC) to
      :math:`O(\epsilon)`. L12

   Data Association
      The problem of deciding which incoming measurement corresponds to
      which existing track (or that it is a new object or clutter).
      Solved by nearest neighbor, Hungarian/GNN, JPDA, or MHT depending
      on the ambiguity tolerated.
      L6

   DDS
      Data Distribution Service. An OASIS/OMG standard for real-time
      publish-subscribe communication. The middleware layer underlying
      ROS 2, providing configurable QoS policies for message delivery. L14

   DDT
      Dynamic Driving Task. All real-time operational and tactical functions
      required to operate a vehicle in on-road traffic. SAE J3016 splits it
      into six subtasks: lateral control, longitudinal control, :term:`OEDR`
      detection, OEDR response, maneuver planning and :term:`Conspicuity`.
      Excludes strategic functions such as trip scheduling, destination
      choice and route selection, so a vehicle with a flawless route
      planner and nothing else is not automated at all. :doc:`L1 </lectures/lecture1/l1_lecture>`

   DDT Fallback
      The response required when a :term:`Driving Automation Feature` can no
      longer perform the :term:`DDT`. Triggered either by a **system failure**
      or by the vehicle **reaching the edge of its ODD**. Only the first is a
      fault, and the second is more common in service. At
      Level 3 it is performed by the human :term:`Fallback-Ready User` on
      request; at Levels 4 and 5 the system performs it itself. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Dead Reckoning
      Estimating current position by integrating motion measurements
      (wheel odometry, IMU) from a known prior pose. Accumulates drift
      over time without external corrections. :doc:`L3 </lectures/lecture3/l3_index>` · L7

   Decoder
      The half of a transformer that writes the output. Each layer has
      three steps: its inputs attend to each other (self-attention),
      then to the encoder's output (cross-attention), then an MLP. In
      DETR the inputs are object queries, all decoded at once, so no
      mask is used. RT-DETR-L has six decoder layers.
      :doc:`L4 </lectures/lecture4/l4_index>`

   DeepLabv3+
      A semantic segmentation architecture (Chen et al., 2018) using atrous
      (dilated) convolutions and Atrous Spatial Pyramid Pooling (ASPP) to
      capture multi-scale context without reducing spatial resolution. :doc:`L5 </lectures/lecture5/l5_index>`

   DeepSORT
      Deep Simple Online and Realtime Tracking (Wojke et al., 2017).
      Extends SORT with a deep appearance descriptor (128-D embedding)
      for re-identification after occlusion. L6

   Degraded Mode
      A reduced capability the vehicle falls back to when it loses a
      sensor. You name the minimum sensor set for each capability in
      advance. For example, losing a sensor disables lane-keeping but
      keeps ACC at reduced speed on RADAR. The mode is decided at design
      time, not invented at runtime.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Degrees of Freedom
      How many numbers a sensor reports at once, written :math:`m`. A
      sign match giving :math:`x` and :math:`y` has :math:`m = 2`. It
      selects which chi-square distribution the NIS should follow.
      :doc:`L3 </lectures/lecture3/l3_index>`

   DETR
      DEtection TRansformer (Carion et al., 2020). A detector that
      predicts a set: :math:`N` object queries give :math:`N` answers,
      each a class and a box, or "no object". Each query is a learned
      vector, and :math:`N = 100`. In training, the Hungarian algorithm
      pairs each object with exactly one query, so DETR needs no NMS. It
      matched Faster R-CNN at 42.0 mAP on COCO, but only after 500
      training epochs. :doc:`L4 </lectures/lecture4/l4_index>`

   Diffusion-Based Planning
      Motion planning via iterative denoising of trajectories, learned
      from expert demonstrations. Models the trajectory distribution as
      a diffusion process and generates plans by reverse diffusion.
      Examples: Diffusion Planner (ICLR 2025), DiffusionDrive (CVPR 2025). L10

   Dijkstra
      A classical shortest-path graph search algorithm that expands nodes
      in order of accumulated cost from the source. Equivalent to A* with
      zero heuristic; preferred when no useful heuristic is available. L8 · L10

   Dilated Convolution
      A convolution that inserts "holes" (zeros) between kernel weights,
      enlarging the receptive field without downsampling spatial resolution.
      Foundation of DeepLabv3+'s ASPP module. Also called *atrous*
      convolution. :doc:`L5 </lectures/lecture5/l5_index>`

   Disengagement
      Any moment during testing at which the automated system stops driving
      and a human takes over, either because the system requested it or
      because the safety driver judged intervention necessary. *Miles per
      disengagement* is test miles divided by the number of such events.
      Widely quoted as a safety comparison and largely useless for it: the
      definition is subjective, the data is self-reported, nothing is
      normalized for driving difficulty, and companies stop reporting once
      the safety driver is removed. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Disparity
      The horizontal pixel difference between where the same 3D point
      appears in left and right stereo camera images. Used to compute
      depth: ``depth = (B x f) / d``. :doc:`L2 </lectures/lecture2/l2_index>`

   Distribution Shift
      The mismatch between the state distribution seen during training and
      the distribution encountered during deployment. A key failure mode
      of behavior cloning where small errors compound over time. L12

   Divergence
      The failure in which a filter becomes more confident as it becomes
      less accurate: its reported covariance keeps shrinking while its
      true error grows. The update shrinks :math:`P` whether or not the
      reading was good, because the surprise does not appear in
      :math:`P = (I - KH)P^-`. In the EKF it is a feedback loop: a poor
      estimate puts the tangent in the wrong place, which gives a worse
      estimate. :doc:`L3 </lectures/lecture3/l3_index>`

   Domain Gap
      The difference between the images a model was trained on and the
      images it sees in use. The larger the gap, the worse the model
      does, even when it scored well on its own test set. On an AV it
      comes from simulation to real, everyday images to roads, weather
      and light, place, and sensor. You see it when mAP on your own
      data falls below the published mAP. You shrink it by fine-tuning
      on data from where you drive. See Sim-to-Real Gap.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Domain Randomization
      Varying simulation parameters (lighting, textures, weather, sensor
      noise) during training to improve robustness and sim-to-real transfer
      of learned models. L13

   Doppler Effect
      The frequency shift in a reflected signal caused by the relative
      motion of the target. RADAR uses this to directly measure the
      velocity of moving objects. :doc:`L2 </lectures/lecture2/l2_index>`

   DriveTransformer
      An end-to-end autonomous driving model (ICLR 2025) that uses shared
      attention across all perception, prediction, and planning tasks,
      achieving high throughput through task-parallel processing. L12

   DriveVLM
      A Vision-Language-Action model for autonomous driving (Tian et al.,
      2024) that combines a vision-language reasoning model with a fast
      driving policy, producing chain-of-thought scene descriptions
      alongside action outputs. L12

   Driver Support Feature
      SAE J3016's name for Levels 0 to 2. In all three, the human is
      driving, whatever the system is doing: the human performs or
      supervises the DDT. Capability varies a great deal across these
      levels, and the level does not move. Contrast Automated Driving
      Feature. :doc:`L1 </lectures/lecture1/l1_index>`

   Driving Automation Feature
      The unit that SAE J3016 actually classifies. A level applies to a
      **feature**, not to a vehicle. A single vehicle may offer several
      features at different levels; the level that applies at any moment is
      whichever feature is engaged. "This is a Level 2 car" is therefore a
      category error. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Driving Score
      The CARLA leaderboard's headline metric: :term:`Route Completion`
      multiplied by an infraction penalty
      :math:`P = 1/(1 + \sum_j c_j n_j)`. Coefficients range from 1.00 for a
      collision with a pedestrian down to 0.25 for running a stop sign.
      Used to score GP4. L13

   DSRC
      Dedicated Short-Range Communications (IEEE 802.11p). The original
      V2X communication technology operating in the 5.9 GHz band.
      Competing with C-V2X for industry adoption. L14

   Dynamic Range
      The ratio between the brightest and darkest elements a camera sensor
      can capture simultaneously. Measured in dB; 120 dB means a million-
      to-one brightness ratio. :doc:`L2 </lectures/lecture2/l2_index>`


.. _glossary-e:

E
=

.. glossary::

   Early Fusion
      Combining raw measurements before anything interprets them.
      Preserves the most information, but demands accurate calibration
      and tight timing, moves large amounts of data, and lets one bad
      sensor affect everything. L6

   Effective Number of Particles
      :math:`N_\text{eff} = 1/\sum_i (w^{(i)})^2`: how many particles
      still carry real weight. It is :math:`N` when all weigh the same
      and 1 when one particle holds all the weight. The L3 particle
      filter resamples when it falls below :math:`N/2`.
      :doc:`L3 </lectures/lecture3/l3_index>`

   End-to-End Driving
      An approach where a single neural network maps raw sensor input
      directly to driving actions, bypassing the traditional modular
      pipeline (perception -> planning -> control). L12

   EKF
      Extended Kalman Filter. See Extended Kalman Filter. :doc:`L3 </lectures/lecture3/l3_index>` ·
      L7

   Embedding
      Turning each piece of the input into a vector of :math:`D`
      numbers that the network can compare and combine. ViT does it in
      two steps: read each patch's pixels into one line of 768 numbers,
      then multiply that line by a learned :math:`768 \times D` matrix
      :math:`E`. In ViT-Base, :math:`D = 768`. See Token.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Encoder
      The half of a transformer that reads the input: a stack of
      layers, each self-attention then an MLP. Tokens in, the same
      number of tokens out, each now carrying the context of the
      others. ViT-Base stacks 12 encoder layers. RT-DETR-L uses one,
      over the 400 cells of its stride-32 map.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Epoch
      One pass over the training images: fifty epochs means fifty passes.
      How many epochs to run is chosen on the validation set, and fewer
      epochs is one remedy for overfitting.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Estimate
      The filter's best guess of the state, written with a hat,
      :math:`\hat{\mathbf{x}}` (x-hat). The hat always means "our best
      guess at", never the truth. A minus, :math:`\hat{\mathbf{x}}^-`,
      marks the prediction, before the next measurement corrects it;
      the minus marks every predicted quantity, as in :math:`P^-`. An
      estimate without an uncertainty is useless to a filter: with
      nothing to weigh, all it can do is trust every source equally.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Expectation
      The average of a quantity taken over all possible outcomes rather
      than over a finite sample. Written with E and square brackets.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Expected Reading
      What a sensor should report if the prediction were right: the
      measurement model run on the prediction, :math:`H\hat{\mathbf{x}}^-`
      (in the EKF, :math:`h(\hat{\mathbf{x}}^-)`). The surprise is the
      real reading minus this one. In L3's braking step it is
      :math:`(100.995,\ 20)` m. :doc:`L3 </lectures/lecture3/l3_index>`

   Extended Kalman Filter
      EKF. A Kalman filter for models that are curves, not straight
      lines. At every step it replaces each curve by its tangent at the
      estimate, then runs the ordinary Kalman equations: the estimate
      goes through the real :math:`f` and :math:`h`, and :math:`P` goes
      through the Jacobians :math:`F_k` and :math:`H_k`. Its failure
      mode is a feedback loop: a poor estimate gives a wrong tangent,
      which gives a worse estimate (divergence). It is the filter GP3
      uses, to fuse GNSS fixes with IMU and wheel-speed data.
      :doc:`L3 </lectures/lecture3/l3_index>` · L7

   Extrinsic Calibration
      The rigid transform describing where one sensor sits relative to
      another, or relative to the vehicle: a rotation and a translation, six
      numbers. Fusing two sensors needs it. It belongs to the installation
      rather than to the sensor, and it drifts with vibration, temperature
      and knocks. :doc:`L2 </lectures/lecture2/l2_index>`

.. _glossary-f:

F
=

.. glossary::

   Failure Boundary
      The conditions at which a system stops working, stated explicitly. A
      system with a known and reported boundary is more useful to a safety
      case than one with a high pass rate and no known limit. L13

   Fallback-Ready User
      The human occupant of a Level 3 vehicle who is not driving but must
      remain receptive to a request to intervene and be able to resume the
      :term:`DDT` within seconds. The role exists only at Level 3, and the
      few-seconds reacquisition of situational awareness it demands is a
      human-factors problem rather than a software one. :doc:`L1 </lectures/lecture1/l1_lecture>`

   False Negative (FN)
      A ground-truth object that no detection matched. Many false
      negatives mean low recall: on an AV, a missed pedestrian.
      :doc:`L4 </lectures/lecture4/l4_index>`

   False Positive (FP)
      A detection that matches nothing: a box on no object, or a second
      box on an object already matched. Many false positives mean low
      precision: on an AV, a phantom pedestrian that can cause a hard
      brake for nothing. :doc:`L4 </lectures/lecture4/l4_index>`

   Feature
      One number computed for one place in the image: how strongly one
      pattern is present there. L4's hand-made vertical-edge filter
      gives 414.7 at the edge of a letter on the bus and -9.0 on the
      flat roof. A network learns its own features, edges and colors
      among them. :doc:`L4 </lectures/lecture4/l4_index>`

   Feature Map
      The features for one pattern at every place in the image: a grid
      of numbers, drawn as an image where bright means large. YOLOv8s's
      first layer gives :math:`240 \times 320` maps from a
      :math:`480 \times 640` input, because its filter moves 2 pixels
      per step (stride 2). :doc:`L4 </lectures/lecture4/l4_index>`

   Filter (Convolution)
      A small grid of weights, not a Kalman filter. Laid on a window of
      pixels, it multiplies each pixel by the weight on top of it, and
      the sum (the response) says how strongly one pattern is there.
      L4's hand-made edge filter is :math:`3 \times 3`: -1 in the left
      column, 0 in the middle, +1 in the right. A network's filter
      weights are set by training. See Filter (Estimation).
      :doc:`L4 </lectures/lecture4/l4_index>`

   Filter (Estimation)
      Something that keeps a running estimate (best guess) of something
      no sensor gives you exactly, updates it whenever a measurement
      arrives, and reports how uncertain that guess is right now. It
      holds two things at all times: the estimate, and how much to
      trust it. The Kalman filter, EKF, UKF and particle filter are
      filters in this sense. See Filter (Convolution).
      :doc:`L3 </lectures/lecture3/l3_index>`

   Filter Consistency
      Whether a filter's reported covariance matches the errors it
      actually makes: an honest filter is neither overconfident nor
      underconfident. With ground truth (the hands-on), check that the
      true error stays inside :math:`\pm 1\sigma` about 68 percent of
      the time. Without it, use the NIS, built only from quantities the
      filter already computes, so the check can run continuously on a
      vehicle. :doc:`L3 </lectures/lecture3/l3_index>`

   Fine-Tuning
      Training a pretrained network a little more, on your own data.
      Replace the head so it outputs your classes (say 5, where COCO has
      80), and train with a small learning rate; optionally freeze the
      first layers, meaning you stop training them. The early layers
      (edges, simple shapes) need little change, and the deeper ones
      adapt. It needs a few thousand of your own images, not COCO's
      118,287. It is how you add classes a dataset lacks, such as exit
      signs, and how you shrink the domain gap.
      :doc:`L4 </lectures/lecture4/l4_index>`

   FMCW
      Frequency-Modulated Continuous Wave. The radar modulation that
      sweeps a frequency chirp and compares the returning echo against
      the outgoing sweep, which yields range and Doppler velocity
      together. :doc:`L2 </lectures/lecture2/l2_index>`

   FMEA
      Failure Mode and Effects Analysis. A systematic method for
      identifying potential failure modes in a system, assessing their
      impact, and designing mitigations (e.g., sensor redundancy). L14

   Foundation Model
      A large neural network pre-trained on broad data at scale and
      adaptable to many downstream tasks (e.g., GPT, CLIP). In AV, used
      as VLA backbones (DriveVLM, NVIDIA Alpamayo) and as world-model
      starting points. :doc:`L4 </lectures/lecture4/l4_index>` · L12 · L13

   Frenet Frame
      A curvilinear coordinate system :math:`(s, d)` defined along a road
      centerline, where :math:`s` is the arc-length along the path and
      :math:`d` is the lateral offset. Simplifies trajectory planning on
      curved roads. L11

   FSM
      Finite State Machine. A classical approach to behavior planning using
      discrete states (lane follow, lane change, stop, yield) and
      transition rules. Simple, interpretable, but brittle for complex
      scenarios. L9

   Functional Safety
      The scope of ISO 26262: hazards from things that break. A sensor
      fails, a chip flips a bit, code crashes. ISO 26262 ranks each
      hazard with an ASIL so the riskiest ones get the most
      engineering. Contrast SOTIF, where nothing breaks.
      :doc:`L1 </lectures/lecture1/l1_index>`

   Functional Scenario
      A scenario written in plain language so that humans can agree on it
      ("a vehicle cuts into my lane from the right"). The most abstract of
      the three scenario layers; refined into a :term:`Logical Scenario`. L13

   Fusion Architecture
      The strategy for combining data from multiple sensors. Three main
      types: early fusion (raw data), intermediate/mid-level fusion
      (features), and late fusion (detection outputs). L6


.. _glossary-g:

G
=

.. glossary::

   GAIA-3
      Wayve's 15-billion-parameter generative driving world model
      (December 2025) that predicts realistic future driving video
      conditioned on actions and text prompts. L13

   GAIA-4
      Wayve's world model announced August 2026, which added **closed-loop**
      simulation: the AI Driver's decisions change the generated future,
      rather than the scene replaying regardless. Uses a "world on rails"
      approach in which other road users keep their recorded trajectories,
      so it cannot evaluate negotiation. L13

   Gating
      Throwing away a reading that disagrees with the prediction by more
      than a threshold: in L3, a NIS above 9.21 for a sign match
      reporting :math:`x` and :math:`y`. It catches a wrong sign match,
      where the camera misreads a sign's number and the match is on
      time, normal-looking, and 25 m wrong. Its own failure mode: a
      filter that is already wrong rejects the good readings that would
      correct it, so count rejections in a row and raise an alarm past a
      limit. :doc:`L3 </lectures/lecture3/l3_index>` ·
      :doc:`L5 </lectures/lecture5/l5_index>`

   Gaussian
      A bell curve: one peak, with errors usually small and rarely
      large. :math:`\mathbf{w} \sim \mathcal{N}(0, Q)` reads "drawn from
      a bell curve centered on 0, with covariance :math:`Q`". On one
      axis, about 68 percent of readings land within one :math:`\sigma`
      of the mean, 95 percent within two and 99.7 percent within three.
      A Kalman filter keeps its belief as one Gaussian: the estimate
      sets where it peaks and :math:`P` sets how wide it is. A straight
      line turns a Gaussian into a Gaussian; a curve bends it into a
      lopsided shape, which is why the EKF is needed.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Geofence
      A boundary in the physical world, encoded in software, outside which a
      :term:`Driving Automation Feature` will not operate. One common way of
      expressing the geographic component of an :term:`ODD`. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Global Nearest Neighbor
      GNN (not the graph neural network of L9). Data association that
      solves a whole frame at once, choosing the set of pairings with the
      lowest total cost, usually with the Hungarian algorithm. Removes the
      order dependence that makes plain nearest-neighbor association
      unreliable.
      :doc:`L5 </lectures/lecture5/l5_index>` · L6

   GNN
      Graph Neural Network. A neural network operating on graph-structured
      data. Used in trajectory prediction to model interactions between
      agents, where nodes represent agents and edges represent
      relationships. Not the Global Nearest Neighbor data association of
      L5. L9

   GNSS
      Global Navigation Satellite System. Provides absolute position
      (latitude, longitude, altitude). Includes GPS (US), GLONASS
      (Russia), Galileo (EU), BeiDou (China). :doc:`L2 </lectures/lecture2/l2_index>` · L7

   Gradient
      How much one number changes when another changes a little. In
      training, the gradient :math:`\partial L / \partial w` says, for each
      weight, how the loss changes when that weight changes. The L4
      lecture uses the same tool on pixels: how much a cell's person score
      would change if one pixel changed a little. See Backpropagation and
      Gradient Descent. :doc:`L4 </lectures/lecture4/l4_index>`

   Gradient Descent
      The training step that moves every weight a little downhill, by the
      learning rate :math:`\eta` times its gradient:
      :math:`w \leftarrow w - \eta \, \partial L / \partial w`. In the L4
      example (numbers chosen for it), one weight gives
      :math:`\hat{y} = wx` with loss :math:`(wx - y)^2`, :math:`x = 2`,
      :math:`y = 6`, :math:`w = 1` and :math:`\eta = 0.05`. The loss is
      16, the gradient is -16, and one step gives :math:`w = 1.8`, which
      drops the loss to 5.76. Training repeats this step thousands of
      times or more. :doc:`L4 </lectures/lecture4/l4_index>`

   Ground Truth
      The true value of a quantity. Available in simulation and never
      available on a real vehicle. Used to check whether a filter's
      reported uncertainty matches the error it is actually making.
      :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>` ·
      :doc:`L4 </lectures/lecture4/l4_index>`

   GUM
      Guide to the Expression of Uncertainty in Measurement, JCGM
      100:2008. With the VIM, it supplies the formal definitions of
      coverage interval and coverage probability used in this course.
      :doc:`L3 </lectures/lecture3/l3_index>`

.. _glossary-h:

H
=

.. glossary::

   HARA
      Hazard Analysis and Risk Assessment. An ISO 26262 process for
      systematically identifying potential hazards, assessing their
      severity, exposure, and controllability, and assigning ASIL levels. :doc:`L1 </lectures/lecture1/l1_index>` ·
      L14

   Hardware-in-the-Loop (HIL)
      A test level in which real ECUs run the software with real timing while
      the world remains simulated. Catches latency, scheduling and resource
      limits that :term:`Software-in-the-Loop (SIL)` cannot. L13

   Hand-Eye Calibration
      Motion-based extrinsic calibration: each sensor estimates its own
      ego-motion, and you solve :math:`AX = XB` for the transform
      :math:`X` between them. It needs no target, but it needs real
      rotation and translation, so driving in a straight line is
      degenerate. The other two families are target-based (a
      checkerboard or AprilTag board seen by both sensors, most
      accurate, hard to repeat in the field) and targetless (aligning
      natural structure such as LiDAR intensity edges against image
      edges). :doc:`L2 </lectures/lecture2/l2_index>`

   HD Map
      High-Definition map with centimeter-accurate road geometry, lane
      markings, traffic signs, and semantic annotations. Used for
      precise localization by matching live sensor data against the map.
      In the L3 tunnel, it is what turns "I see an exit sign" into "I am
      here" (the sign match). :doc:`L2 </lectures/lecture2/l2_index>` ·
      :doc:`L3 </lectures/lecture3/l3_index>` ·
      L7 ·
      L8

   Head (Detection)
      The last part of a detector: it turns features into the answer,
      classes and boxes. In YOLOv8s it is a few small convolutions run
      at every cell of the three maps: 144 numbers per cell, 80 class
      scores and 64 for the box (four distances, each as 16 bins),
      decoded to 84. Because it is a convolution, the same weights run
      at all 6300 cells. RT-DETR-L's head is a transformer decoder.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Height Map
      A grid seen from above that stores, in each cell, the height of the
      tallest LiDAR point in that cell. The L5 hands-on first drops the
      points inside the AV's footprint, because the lowest beams hit its
      own roof. :doc:`L5 </lectures/lecture5/l5_index>`

   HOTA
      Higher Order Tracking Accuracy. A tracking evaluation metric that
      balances detection quality and association quality equally via
      their geometric mean, addressing biases in MOTA and IDF1. L6

   Hungarian Algorithm
      An optimization algorithm that finds the minimum-cost one-to-one
      assignment between two sets. Used by DETR for bipartite matching
      between predictions and ground truth, and by SORT/DeepSORT for
      association between predicted tracks and new detections.
      :doc:`L4 </lectures/lecture4/l4_index>` ·
      L6


.. _glossary-i:

I
=

.. glossary::

   ICP
      Iterative Closest Point. An algorithm for aligning two point clouds
      by iteratively finding closest-point correspondences and minimizing
      the alignment error. Core algorithm for scan matching in SLAM and
      LiDAR odometry. L7

   IDF1
      Identity F1 Score. A tracking evaluation metric computed as the F1
      score of correct identity assignments. Emphasizes consistent ID
      maintenance over raw detection accuracy. L6

   IMU
      Inertial Measurement Unit. Measures linear acceleration
      (accelerometers) and angular velocity (gyroscopes) at high
      frequency (>100 Hz). Suffers from drift over time. :doc:`L2 </lectures/lecture2/l2_index>` · L7

   Innovation
      The surprise: the reading the filter got minus the reading it
      expected, :math:`\nu = \mathbf{z} - H\hat{\mathbf{x}}^-` (in the
      EKF, :math:`\mathbf{z} - h(\hat{\mathbf{x}}^-)`). With a
      prediction of 50 m and a sign match of 53 m, it is 3 m. The only
      new information in a filter cycle, and the quantity the NIS
      checks. Many textbooks write it as :math:`\mathbf{y}`; L3 uses
      :math:`\nu` because :math:`y` is the across-road coordinate.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Innovation Covariance
      How large the filter expected the surprise to be, written
      :math:`S = H P^- H^\top + R`. With one number it is
      :math:`\sigma_\text{pred}^2 + \sigma_\text{meas}^2`, the bottom of
      the Kalman gain. Used by the Kalman gain, the NIS and the gate.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Instance Segmentation
      A perception task that assigns each object a unique ID and
      pixel-level mask, distinguishing individual instances of the same
      class (e.g., car #1 vs. car #2). :doc:`L5 </lectures/lecture5/l5_index>`

   Intermediate Fusion
      Combining learned features from each sensor. The network can learn
      which sensor to trust in which conditions, at the cost of needing
      training data with every modality present, and of being hard to
      interpret or certify. L6

   Intrinsic Calibration
      The parameters describing how a camera turns an incoming ray of
      light into a pixel: focal lengths, principal point and distortion
      coefficients. They belong to the camera and lens, so they travel
      with it and are far more stable than extrinsics. :doc:`L2
      </lectures/lecture2/l2_index>`

   Inverse-Variance Weighting
      Combining independent estimates with weights proportional to one
      over the variance. The precisions add, so the combined uncertainty
      is smaller than either input. The one-number Kalman update is
      exactly this: a prediction of 50 m (:math:`\sigma = 2` m) and a
      sign match of 53 m (:math:`\sigma = 1` m) give 52.4 m with
      :math:`\sigma = 0.89` m. The weight is :math:`1/\sigma^2`, so half
      the sigma gives four times the weight.
      :doc:`L3 </lectures/lecture3/l3_index>`

   IoU
      Intersection over Union. The ratio of the overlap area to the
      union area of a predicted and ground truth bounding box. Used as
      the primary metric for evaluating detection localization. :doc:`L4 </lectures/lecture4/l4_index>`

   IPM
      Inverse perspective mapping. Redrawing a camera image as the ground
      seen from above, by assuming everything in it lies on the road. It
      needs no learning and no depth sensor, and it is exact for lane
      markings on a flat road. Anything above the road breaks the
      assumption: in the L5 hands-on, buildings smear into long streaks
      pointing away from the AV. :doc:`L5 </lectures/lecture5/l5_index>`

   ISO 26262
      International standard for functional safety of road vehicle
      electrical and electronic systems. Defines ASIL levels to classify
      risk severity. :doc:`L1 </lectures/lecture1/l1_lecture>` · L14

   ISO 21448 (SOTIF)
      Safety of the Intended Functionality. Addresses safety hazards that
      occur without a system failure (e.g., sensor limitations). A
      critical complement to ISO 26262. :doc:`L1 </lectures/lecture1/l1_lecture>` · L14


   ISO 34502
      *Road vehicles: Test scenarios for automated driving systems:
      Scenario based safety evaluation framework* (2022). Part of the ISO
      34500 series: 34501 vocabulary, 34502 evaluation framework, 34503 ODD
      taxonomy, 34504 scenario categorization, 34505 test case generation. L13

   ISO/SAE 21434
      The automotive cybersecurity standard: things an attacker does
      on purpose. Its analysis, TARA, asks what an attacker could do
      and produces security goals in Stage 2 of the concept-to-road
      pipeline. Covered in the cybersecurity pre-read before L14.
      :doc:`L1 </lectures/lecture1/l1_index>`

.. _glossary-j:

J
=

.. glossary::

   Jacobian
      The table of slopes of a function with several inputs and outputs:
      nudge input :math:`j` a little, and output :math:`i` moves this
      much. The EKF uses :math:`F_k = \partial f/\partial \mathbf{x}` at
      the last estimate, :math:`H_k = \partial h/\partial \mathbf{x}` at
      the prediction, and :math:`G = \partial f/\partial \mathbf{u}` to
      build :math:`Q_k`, all rebuilt every step. A wrong sign still runs
      and converges, so test each Jacobian by nudging its inputs.
      :doc:`L3 </lectures/lecture3/l3_index>`

   JPDA
      Joint Probabilistic Data Association. A probabilistic data
      association method for multi-target tracking in clutter that
      considers all possible measurement-to-track assignments weighted
      by their probabilities. L6


.. _glossary-k:

K
=

.. glossary::

   Kalman Filter
      A recursive estimator: it keeps only an estimate and its
      covariance :math:`P`, and repeats two steps. Predict with a motion
      model (:math:`P` grows), then update with a measurement (:math:`P`
      shrinks). When the models are linear and the noise is Gaussian, no
      other estimator has a smaller expected squared error (Kalman,
      1960). Foundation of IMU and GNSS fusion and the state-update step
      inside SORT and DeepSORT. :doc:`L3 </lectures/lecture3/l3_index>`
      · L6 ·
      L7

   Kalman Gain
      :math:`K`, the fraction of the surprise the filter acts on: the
      update moves the estimate by :math:`K` times the surprise. It is
      computed from the two uncertainties, not chosen: with one number,
      :math:`K =
      \sigma_\text{pred}^2 / (\sigma_\text{pred}^2 + \sigma_\text{meas}^2)`.
      A prediction with :math:`\sigma = 2` m and a sign match with
      :math:`\sigma = 1` m give :math:`K = 0.8`: follow the sign match.
      A precise measurement pushes :math:`K` toward 1, an imprecise one
      toward 0. :doc:`L3 </lectures/lecture3/l3_index>`

   Kidnapped Robot Problem
      A robot picked up and moved somewhere unknown, so it has no idea
      where it is. Its belief has several peaks, which makes it a
      particle filter problem, not a Kalman filter one. The L3 particle
      filter hands-on is a version of it: the AV's computer restarts in
      a 700 m tunnel with 23 identical lights 25 m apart.
      :doc:`L3 </lectures/lecture3/l3_index>`


.. _glossary-l:

L
=

.. glossary::

   L-Shape Fitting
      Fitting a rotated box to a cluster of LiDAR points seen from above,
      with no learning (Zhang et al., 2017). For each direction
      :math:`\theta` from 0 to 89 degrees, in steps of 1 degree, take the
      rectangle with those axes that just holds the points. Score it by
      the sum over points of :math:`1/\max(d, d_0)`, where :math:`d` is a
      point's distance to its nearest edge. The best direction gives the
      box. One sweep shows a rectangle, not which end is the front, so
      the heading is known only modulo 180 degrees.
      :doc:`L5 </lectures/lecture5/l5_index>`

   Lanelet2
      An open lane-graph map format (Poggenhans et al., 2018) widely used
      by Autoware and many research stacks. Represents drivable lanes as
      typed line strings with explicit topological connectivity. L8

   Late Fusion
      Combining finished per-sensor results such as tracks, object lists
      or pose estimates. Modular, testable and robust to a failed
      sensor, but information is discarded before the combination
      happens. This is what GP3 uses. L6

   Latency
      The time from a camera frame arriving to its boxes coming out of
      the detector. On L4's street image (RTX 4060 laptop, plugged in,
      PyTorch, median of 50 runs): 9.1 ms for YOLOv8s, 29.9 ms for
      RT-DETR-L. On battery the same calls took 13.3 and 42.0 ms, so a
      latency is only useful with its conditions. See Time Budget.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Lateral Control
      The DDT subtask of steering: holding a lane, and turning. Covered
      in L11. :doc:`L1 </lectures/lecture1/l1_index>`

   Lattice Planner
      A motion planning approach that performs graph search on a
      pre-computed state lattice of kinematically feasible motion
      primitives. Combines the completeness of graph search with
      kinematic feasibility. L10

   Layer
      One step of a network's computation: a set of filters, each slid
      over the layer's input, each giving one feature map. Layers run
      one after another, each working on the maps the layer before it
      produced. YOLOv8s's first layer has 32 filters, each
      :math:`3 \times 3` pixels times 3 colors, so 27 weights, all set
      by training. :doc:`L4 </lectures/lecture4/l4_index>`

   LiDAR
      Light Detection and Ranging. Uses laser pulses and time-of-flight
      to measure distances, producing 3D point clouds. Key specs: range,
      points per second, accuracy, beam count. :doc:`L2 </lectures/lecture2/l2_index>`

   LiDAR Odometry
      Estimating ego-motion by matching consecutive LiDAR scans using
      algorithms like ICP or feature-based methods (LOAM). More robust
      than visual odometry in low-light and textureless environments. L7

   Lift-Splat-Shoot (LSS)
      A camera-only BEV method (Philion and Fidler, NeurIPS 2020) in three
      stages. Lift: predict a depth distribution for each pixel and spread
      its feature over the depth bins, a frustum of features. Splat: drop
      the frustum points into BEV cells with the camera intrinsics and
      extrinsics and sum-pool them, which collapses the height. Shoot:
      score a fixed set of candidate ego trajectories on the BEV cost map
      and pick the best. Fully differentiable, with no depth labels.
      :doc:`L5 </lectures/lecture5/l5_index>`

   Likelihood
      :math:`p(\mathbf{z} \mid \mathbf{x})`: how likely the reading
      :math:`\mathbf{z}` is, if the AV were at :math:`\mathbf{x}`. The
      particle filter weighs each particle by it. For one sign match
      with noise :math:`\sigma`, it is, up to a constant,
      :math:`\exp(-(\mathbf{z} - h(\mathbf{x}))^2 / 2\sigma^2)`.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Linearization
      Replacing a curved model by a straight line, its tangent at the
      current estimate, so that the Kalman equations apply. The EKF
      linearizes :math:`f` and :math:`h` at every step through their
      Jacobians. It is accurate only near the point of contact: in L3's
      range-to-a-landmark example, a poor estimate (:math:`\hat{x} = 10`
      m, AV at 16 m) gives a tangent that is too steep, and the
      correction lands at 14.77 m, 1.23 m short.
      :doc:`L3 </lectures/lecture3/l3_index>`

   LOAM
      LiDAR Odometry and Mapping. A foundational LiDAR SLAM system that
      separates high-frequency odometry (edge and planar feature matching)
      from low-frequency mapping for real-time operation. L7

   Localization (Detection)
      Given an image :math:`W` pixels wide and :math:`H` high and one
      object of interest, output where it is: one box
      :math:`b = (x_0, y_0, x_1, y_1)`, with
      :math:`0 \le x_0 < x_1 \le W` and :math:`0 \le y_0 < y_1 \le H`.
      No class. Pixel coordinates start at the top-left corner, with
      :math:`x` to the right and :math:`y` down. Not the same as
      working out where the AV is.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Logical Scenario
      A :term:`Functional Scenario` with its parameters named and given
      *ranges* (gap 5 to 30 m, closing speed 0 to 15 m/s). Still not runnable;
      fixing the values produces a :term:`Concrete Scenario`. L13

   Long-Tail Scenarios
      Rare but safety-critical driving events (e.g., a mattress on the
      highway, a child running into the road) that are underrepresented
      in training data. The primary data challenge in AV development. :doc:`L1 </lectures/lecture1/l1_index>` ·
      :doc:`L4 </lectures/lecture4/l4_index>` · L13 · L14

   Longitudinal Control
      The DDT subtask of acceleration and braking: speed and gap
      keeping. Covered in L11. :doc:`L1 </lectures/lecture1/l1_index>`

   Loop Closure
      Detection of a previously visited location during SLAM, used to
      correct accumulated drift by adding a constraint in the pose graph.
      Methods include scan context, visual bag-of-words, and neural
      descriptors. L7

   Loss
      A number :math:`L` that measures how wrong a network's output is.
      Training adjusts the weights to make it smaller. Classification
      uses cross-entropy loss. :doc:`L4 </lectures/lecture4/l4_index>`

   Luo's Taxonomy
      Three ways two sensors can relate, each with a consequence for
      where you mount them. **Complementary:** different pieces of the
      puzzle (the camera classifies, the LiDAR measures), so their
      fields of view must overlap wherever you need both at once.
      **Competitive:** the same information twice, for fault tolerance,
      so the two must fail independently. **Cooperative:** new
      information neither could produce alone, such as stereo depth, so
      the geometry is the measurement and the baseline sets the depth
      resolution. :doc:`L2 </lectures/lecture2/l2_index>`


.. _glossary-m:

M
=

.. glossary::

   Mahalanobis Distance
      A distance metric that accounts for the covariance (uncertainty)
      of a distribution. Used in data association to determine whether a
      measurement is statistically consistent with a predicted track
      state. L6

   Maneuver Planning
      The DDT subtask of deciding what to do next: change lane, wait,
      turn, overtake. Covered in L8 to L10.
      :doc:`L1 </lectures/lecture1/l1_index>`

   mAP
      Mean Average Precision. The primary metric for evaluating object
      detectors. mAP@0.5 uses a single IoU threshold; mAP@0.5:0.95
      averages across thresholds for stricter evaluation. :doc:`L4 </lectures/lecture4/l4_index>` · :doc:`L5 </lectures/lecture5/l5_index>`

   Mask R-CNN
      An instance segmentation model (He et al., 2017) that extends Faster
      R-CNN with a mask head predicting a binary segmentation mask for each
      detected bounding box, enabling pixel-level object delineation. :doc:`L5 </lectures/lecture5/l5_index>`

   Matching Cascade
      DeepSORT's name for matching the confirmed and coasting tracks to
      detections first, and the tentative tracks only to the detections
      left over. A new track has a large :math:`S`, so it looks close to
      everything. Without the cascade, GNN hands it an older track's
      detection whenever that lowers the total cost, and the object
      changes ID. In the L5 LiDAR runs, ID switches fell from 202 to 119
      with it. :doc:`L5 </lectures/lecture5/l5_index>`

   Matrix Square Root
      A matrix :math:`L` with :math:`LL^\top = P`: the matrix version of
      taking :math:`\sigma` from a variance. Each column :math:`L_i` is
      one direction to step in, already :math:`1\sigma` long, and the
      UKF places its sigma points along these columns. Code gets
      :math:`L` with one call, usually named Cholesky. It raises an
      error when :math:`P` is not symmetric and positive. Treat that
      error as a bug report, not something to catch and skip.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Max Pooling
      Keeping only the largest value in each window. With 2 by 2 windows,
      each 2 by 2 block becomes its maximum, so the size halves: a 4 by 4
      patch becomes 2 by 2. It keeps "there is an edge in this area" and
      drops the exact pixel, so the network is less sensitive to small
      shifts. YOLOv8 shrinks its maps with stride-2 convolutions instead,
      and uses max pooling only in its SPPF block, with 5 by 5 windows.
      :doc:`L4 </lectures/lecture4/l4_index>`

   MCL
      Monte Carlo Localization. A particle filter-based localization
      algorithm that represents the robot's belief as a set of weighted
      samples. AMCL (Adaptive MCL) dynamically adjusts particle count.
      Standard localization algorithm in ROS. :doc:`L3 </lectures/lecture3/l3_index>` · L7

   Mean
      The average of a set of readings, written with the Greek letter
      mu. :doc:`L3 </lectures/lecture3/l3_index>`

   Measurement Model
      The rule that predicts what a sensor should read, given the state
      at the same instant: :math:`\mathbf{z} = H\mathbf{x} + \mathbf{v}`
      in the Kalman filter,
      :math:`\mathbf{z} = h(\mathbf{x}) + \mathbf{v}` in the EKF. In the
      L3 tunnel, :math:`H` keeps the position and drops the velocity,
      which the sign match cannot see. No sensor is exact, so it comes
      with an error :math:`\mathbf{v}`.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Measurement Matrix
      The matrix :math:`H` that picks out the parts of the state a
      sensor observes: the expected reading is
      :math:`H\hat{\mathbf{x}}^-`. For the L3 sign match, :math:`H` is 2
      by 4: a 1 keeps each position, and the zeros drop the two
      velocities, which a sign match does not measure. Its shape tells
      you what the sensor can see. In the EKF, the Jacobian :math:`H_k`
      takes its place. :doc:`L3 </lectures/lecture3/l3_index>`

   Measurement Noise
      The random error :math:`\mathbf{v}` in a sensor reading, with
      covariance :math:`R`. Measured (by pointing the sensor at a known
      target and examining the spread), taken from the datasheet, or
      set, never guessed. For the L3 sign match we chose
      :math:`\sigma = 1` m on each axis, so :math:`R` has 1 m² on its
      diagonal; the hands-on uses 1 m along the tunnel and 0.2 m across.
      :doc:`L3 </lectures/lecture3/l3_index>`

   MHT
      Multiple Hypothesis Tracking. A data association method that
      maintains a tree of hypotheses for measurement-to-track
      assignments, deferring hard decisions to resolve ambiguity over
      time. L6

   mIoU
      Mean intersection over union, the usual score for segmentation.
      For each class :math:`c`, count pixels: TP (truth :math:`c` and
      network :math:`c`), FP (network :math:`c`, truth not) and FN
      (truth :math:`c`, network not). Then
      :math:`\mathrm{IoU}(c) = TP/(TP + FP + FN)`: the pixels both call
      :math:`c` over the pixels either calls :math:`c`. mIoU is the mean
      over the classes. In the L5 hands-on, SegFormer-B0 scores 0.339 to
      0.408 on CARLA over three runs.
      :doc:`L5 </lectures/lecture5/l5_index>`

   Modality
      A kind of sensing rather than a piece of hardware. Two cameras are
      one modality; a camera and a radar are two. Complementarity is a
      claim about modalities, never about counts. :doc:`L2
      </lectures/lecture2/l2_index>`

   M-of-N
      The rule that promotes a tentative track to confirmed, requiring M
      detections within N frames. It stops clutter from being reported
      as a real object, at the cost of a short delay before a genuine
      object is confirmed. :doc:`L5 </lectures/lecture5/l5_index>` · L6

   Monocular Depth
      Depth from one camera, inferred by a network from the cues you use
      in a photograph: familiar size, perspective, occlusion and ground
      contact. It is the cheapest depth there is, but it is an estimate
      with scale ambiguity. It also fails plausibly. Stereo returns
      nothing when it cannot match, but a monocular network always
      returns a full, confident depth map, even for an object it has
      never seen. :doc:`L2 </lectures/lecture2/l2_index>`

   MOTA
      Multi-Object Tracking Accuracy. A tracking metric computed as
      :math:`1 - (FN + FP + IDSW) / GT`, penalizing false negatives,
      false positives, and identity switches. Range: :math:`(-\infty, 1]`. L6

   Motion Model
      The rule that predicts the next state from the current one, using
      only how the AV moves: :math:`\mathbf{x}_k = F\mathbf{x}_{k-1} +
      B\mathbf{u}_k + \mathbf{w}` in the Kalman filter,
      :math:`f(\mathbf{x}_{k-1}, \mathbf{u}) + \mathbf{w}` in the EKF.
      It does not look at the world (no camera, no sign match). No rule
      is perfect, so it comes with an error :math:`\mathbf{w}`, whose
      size is :math:`Q`. :doc:`L3 </lectures/lecture3/l3_index>`

   MOTP
      Multi-Object Tracking Precision. The average overlap (IoU) between
      true positives and their assigned ground-truth boxes. Complements
      MOTA by measuring localisation quality independently of identity
      switches. L6

   MPC
      Model Predictive Control. A receding-horizon optimization-based
      controller that solves a finite-horizon optimal control problem at
      each time step, applying only the first control action. Dominant
      controller in production AV systems. L11

   MRC
      Minimal Risk Condition. The stable, low-risk state a vehicle reaches
      when a trip cannot be completed: the *where you end up* that follows
      the :term:`DDT Fallback`'s *who takes over*. Note that it is **not**
      triggered only by failures: leaving the ODD reaches it too.

      **An MRC is a design artifact.** Somebody decided in advance what
      "safe" means and validated it against a list of situations they thought
      of; if reality is not on the list, the vehicle still follows the list.
      Every candidate hides an assumption: stopping in place assumes traffic
      behind can react, pulling over assumes a shoulder exists and that
      nothing is trapped underneath. :doc:`L1 </lectures/lecture1/l1_lecture>` · L14

   Multi-Modal Prediction
      A trajectory prediction output that represents several plausible
      futures simultaneously (typically as :math:`K` weighted trajectory
      modes), capturing the inherent uncertainty in other agents'
      intentions. L9

   Multi-Object Tracking (MOT)
      The task of maintaining consistent identity for detected objects
      across consecutive frames. Methods: SORT, DeepSORT, ByteTrack,
      transformer-based MOT. L6

   Multipath
      A GNSS error in which the signal arrives by a reflected path
      rather than directly, so the receiver places the vehicle several
      meters from its true position. The fix arrives on time and looks
      entirely normal, which makes it more dangerous than a lost fix.
      :doc:`L2 </lectures/lecture2/l2_index>`

.. _glossary-n:

N
=

.. glossary::

   Neck
      The middle part of a detector, between the backbone and the head.
      It mixes the feature maps of different sizes: a small map's cells
      respond to whole objects like a bus, and a big map's cells mark
      where its edges are. RT-DETR-L's neck adds a transformer layer.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Neuron
      The small piece every network is built from: a weighted sum of its
      inputs, plus a bias, passed through an activation function,
      :math:`y = \sigma(w_1 x_1 + w_2 x_2 + \dots + b)`. In the L4
      example, :math:`(R, G, B) = (20, 83, 152)` with
      :math:`w = (0.5, -0.2, 0.1)` and :math:`b = -5` (chosen for the
      example) gives a sum of 8.6, then 3.6 with the bias, and ReLU
      outputs 3.6. :doc:`L4 </lectures/lecture4/l4_index>`

   NDS
      nuScenes Detection Score. A composite ranking metric for 3D object
      detection on nuScenes, combining mAP with five true-positive error
      metrics (translation, scale, orientation, velocity, attribute). :doc:`L5 </lectures/lecture5/l5_index>`

   NDT
      Normal Distributions Transform. A point cloud registration method
      that represents clouds as a grid of Gaussian distributions.
      Used in Autoware for LiDAR-based localization. Faster than ICP
      for large-scale matching. L7

   NIS
      Normalized innovation squared,
      :math:`\varepsilon = \nu^\top S^{-1} \nu`: the actual surprise
      over the size the filter expected. If the filter is honest, it
      averages about 1 per number the sensor reports and follows a
      chi-square distribution with :math:`m` degrees of freedom. In the
      L3 tunnel, 19 sign matches average 1.39 per match against an
      expected 2; by chance the average of 19 lands anywhere from 1.2 to
      3.0, so the filter is honest. Persistently above the band means
      overconfident (:math:`Q` or :math:`R` too small); below means
      underconfident. No ground truth needed.
      :doc:`L3 </lectures/lecture3/l3_index>`

   NMS
      Non-Maximum Suppression. A post-processing step that removes
      duplicate detections by suppressing overlapping bounding boxes
      with lower confidence. Not needed in DETR. :doc:`L4 </lectures/lecture4/l4_index>`

   Noise
      Random error that scatters readings around a center and averages
      away as more readings are taken: the average of :math:`n` readings
      wanders by about :math:`\sigma/\sqrt{n}`. Described by variance.
      Contrast with bias, which does not average away.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Nonholonomic Constraint
      A motion constraint that limits achievable velocities but not the
      configuration space itself. A car cannot move sideways instantaneously
      (no lateral velocity in the body frame), and planners must respect
      this when generating paths. L10

   Normal Distribution
      See Gaussian. :doc:`L3 </lectures/lecture3/l3_index>`

   nuScenes
      The standard benchmark dataset for BEV perception evaluation
      (Caesar et al., 2020). Detections are scored with mAP and the NDS
      composite score. The L5 CARLA hands-on grades its boxes with the
      nuScenes definitions. :doc:`L5 </lectures/lecture5/l5_index>`

   NVIDIA Cosmos
      NVIDIA's family of world foundation models for physical AI,
      designed to generate realistic driving video and enable
      simulation-based AV training and evaluation. L13


.. _glossary-o:

O
=

.. glossary::

   Object Detection
      Given an image and a fixed set of :math:`C` classes, output a set
      of detections, one per object found. Each detection is a class, a
      confidence from 0 to 1, and a box
      :math:`b = (x_0, y_0, x_1, y_1)`, its top-left and bottom-right
      corners in pixels. The order of the detections means nothing, and
      their number changes from image to image. :math:`C` comes from the
      training data: 80 for COCO. Detection is classification plus
      localization, for every object.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Object Query
      In DETR and RT-DETR, one of a fixed set of guesses that the
      decoder turns into one answer each: one object, or none. Each
      query reads the encoder's output by cross-attention. DETR uses 100
      vectors learned in training. RT-DETR starts its 300 queries at the
      300 encoder cells that score highest as objects.
      :doc:`L4 </lectures/lecture4/l4_index>`

   ODD
      Operational Design Domain. The specific set of operating
      conditions under which an ADS is designed to function safely.
      Four kinds of limit: geographic (certain highways, a geofenced
      area), environmental (no heavy snow, daytime only), traffic
      (speed limits, traffic density) and infrastructure (mapped roads,
      lane markings present, no active construction). If the vehicle is
      about to leave its ODD, it must perform the DDT fallback.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Occupancy Grid
      A grid seen from above in which every cell is free, occupied or
      unknown. The L5 ``lidar_bev`` node builds it from the LiDAR, along
      rays 1 degree apart: free up to the farthest return, occupied where
      a point is 0.3 to 2.5 m above the ground, unknown behind the
      nearest obstacle (Autoware's three steps). It uses no learning.
      Compare Occupancy Network (3D).
      :doc:`L5 </lectures/lecture5/l5_index>`

   Occupancy Network (3D)
      A perception architecture that predicts the semantic state of every
      voxel in a 3D volume around the vehicle, capturing arbitrary geometry
      beyond what bounding boxes can represent. Methods named in L5:
      MonoScene and TPVFormer. Occ3D is the benchmark.
      :doc:`L5 </lectures/lecture5/l5_index>`

   ODD Coverage
      The fraction of the claimed :term:`ODD` that a test campaign actually
      exercised. The coverage figure a safety case wants, and only ever as
      good as the ODD it is measured against. Not mileage, and not a pass
      rate. L13

   OEDR
      Object and Event Detection and Response. The :term:`DDT` subtask of
      monitoring the driving environment (detecting and classifying objects
      and events, and deciding on a response), and then executing that
      response. Detection is covered in L4 to L6; response in L10 and L11. :doc:`L1 </lectures/lecture1/l1_lecture>`

   OES
      Operating Envelope Specification. A formal, machine-readable format
      proposed by NIST for precisely defining an ADS's ODD. :doc:`L1 </lectures/lecture1/l1_lecture>`

   One-Stage Detector
      A detector that predicts classes and boxes in one pass of the
      network, from every cell of its feature maps, then removes the
      duplicates with NMS. YOLO is the best-known family. YOLOv8s
      predicts at 6300 cells: 4800, 1200 and 300 on its stride 8, 16
      and 32 grids. Contrast Two-Stage Detector.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Open-Loop Evaluation
      Replaying a fixed recording past a system, so its decisions cannot
      change what happens next. Correct for perception regression testing,
      and unable to evaluate driving: brake in a replay and the recorded
      world carries on regardless. Contrast
      :term:`Closed-Loop Evaluation`. L13

   OpenDRIVE
      An ASAM open standard for describing road networks (geometry,
      lanes, signals, junctions) in XML. Widely used as an interchange
      format between map providers, simulators (including CARLA), and
      planning stacks. L8


   OpenSCENARIO
      An ASAM interchange format describing *what happens* on a road network
      (actors, manoeuvres and triggers), as a companion to
      :term:`OpenDRIVE`, which describes the road itself. Makes a scenario
      portable between simulators. L13

   Overconfident
      Said of a filter whose reported uncertainty is smaller than the
      errors it actually makes. In the L3 tunnel hands-on, :math:`Q` far
      too small (:math:`\sigma_a = 0.01`, against the 0.5 m/s² we chose)
      keeps the true error inside the :math:`\pm 1\sigma` band only 25
      percent of the time instead of about 68, with an RMS error of 5.46
      m instead of 1.06 m. Dangerous, because nothing in the system
      detects it. See Underconfident.
      :doc:`L3 </lectures/lecture3/l3_index>`

.. _glossary-p:

P
=

.. glossary::

   Padding
      A border of zeros around a convolution's input, written :math:`p`,
      so the filter can also be centered on the edge pixels. With kernel
      size :math:`k` and stride :math:`s`, the output size along one
      direction is :math:`\lfloor (\text{in} + 2p - k)/s \rfloor + 1`.
      YOLOv8s's first layer (:math:`k = 3`, :math:`s = 2`, :math:`p = 1`)
      turns 640 into 320 and 480 into 240.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Panoptic Segmentation
      A perception task that combines semantic segmentation (labeling
      "stuff" like road, sky) with instance segmentation (identifying
      individual "things" like cars, pedestrians). :doc:`L5 </lectures/lecture5/l5_index>`

   Particle
      One complete guess at the state, with a weight that says how much
      the filter believes it. A particle filter carries :math:`N` of
      them, hundreds to thousands, and together they are its belief.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Particle Filter
      An alternative to the Kalman filter that stores the belief as a
      crowd of weighted guesses (particles) instead of one bell curve,
      so the belief can be in several places at once. Each cycle:
      predict (move every particle with :math:`f` and its own noise),
      weigh (by the likelihood), and resample. Use it when the belief
      has several peaks and the state is small; it scales badly as the
      state grows. :doc:`L3 </lectures/lecture3/l3_index>` ·
      L7

   Patch
      A small square of the image, cut on a fixed grid: in ViT,
      :math:`16 \times 16` pixels, so
      :math:`16 \times 16 \times 3 = 768` pixel values. A
      :math:`224 \times 224` image gives :math:`14 \times 14 = 196`
      patches. Detectors such as RT-DETR often use the cells of a CNN
      feature map instead. :doc:`L4 </lectures/lecture4/l4_index>`

   Perception
      The process by which an autonomous system transforms unstructured
      sensor data into a structured, semantic understanding of the
      surrounding environment. :doc:`L4 </lectures/lecture4/l4_index>` · :doc:`L5 </lectures/lecture5/l5_index>` · L6

   PID Controller
      Proportional-Integral-Derivative controller. A classical feedback
      controller used for longitudinal speed control in AVs. The three
      terms correct present error (P), accumulated past error (I), and
      predicted future error (D). L11

   Pinhole Camera Model
      The idealized projective camera model that maps 3D world points to
      2D image coordinates via the intrinsic matrix
      :math:`K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}`.
      Underlies intrinsic calibration and stereo geometry. :doc:`L2 </lectures/lecture2/l2_index>`

   Point Cloud
      The output of a LiDAR: an unordered set of x, y and z returns,
      each with an intensity, and with no connectivity between them.
      Nothing in the data says which points belong to the same object.
      :doc:`L2 </lectures/lecture2/l2_index>`

   PointPainting
      A fusion method (Vora et al., CVPR 2020) that projects every LiDAR
      point into the camera image and appends the segmentation network's
      class scores at that pixel to the point. The L5 ``seg_lidar`` node
      keeps only the winning class. The LiDAR and the camera sit in
      different places, so a point the camera cannot see, behind a car,
      still lands on the car's pixels and gets the class "car".
      :doc:`L5 </lectures/lecture5/l5_index>`

   Pose Graph Optimization
      The SLAM backend formulation that represents the robot trajectory
      as a graph of poses (nodes) and relative constraints (edges), then
      optimizes all poses jointly to minimize constraint errors. L7

   Position Embedding
      A learned vector for each token position, added to the token, so
      the network knows where its patch was in the image. Without it,
      the encoder treats the tokens as a set: shuffle them and the
      outputs only shuffle. ViT-Base has 197, one per token, the class
      token included. :doc:`L4 </lectures/lecture4/l4_index>`

   Precision
      The fraction of detections that are correct: TP / (TP + FP).
      High precision means few false positives. :doc:`L4 </lectures/lecture4/l4_index>`

   Precision (Measurement)
      How closely repeated readings agree (VIM 2.15): the word for
      noise. Not the detection metric of L4. See Trueness and Accuracy.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Predict Step
      The first half of every filter cycle: move the estimate forward
      one step with the motion model,
      :math:`\hat{\mathbf{x}}^- = F\hat{\mathbf{x}} + B\mathbf{u}` and
      :math:`P^- = FPF^\top + Q`, before any measurement arrives.
      :math:`P` always grows here. In the L3 tunnel, 22 predict steps
      with no sign match take the position :math:`\sigma` along the
      tunnel from 0.81 to 1.35 m, mostly through :math:`FPF^\top`.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Pretrained
      Trained first on a large, general image collection, then reused.
      Example: ImageNet's 1000-class set, 1.2 million training images.
      Both L4 detectors start from weights pretrained on COCO. See
      Fine-Tuning. :doc:`L4 </lectures/lecture4/l4_index>`

   Prior
      Information you already hold before you measure anything. An HD
      map is a prior. It is not a sensor, since nothing about it is
      live, but it enters the stack where a sensor does. A stop line
      moved two meters makes the map wrong, and a confidently wrong
      prior is worse than none at all.
      :doc:`L2 </lectures/lecture2/l2_index>`

   PRM
      Probabilistic Road Map. A multi-query sampling-based planner that
      pre-computes a graph of collision-free configurations connected by
      feasible paths, then searches this graph for start-to-goal queries. L10

   Process Noise
      How wrong the motion model's prediction can be: the covariance
      :math:`Q` of the process error :math:`\mathbf{w}`. It cannot be
      measured the way measurement noise can, because it describes the
      inadequacy of your own model: it is chosen, then tuned. In the L3
      tunnel it is built from :math:`\sigma_a = 0.5` m/s² (we chose it),
      the acceleration the IMU gets wrong. Too small a :math:`Q` is the
      usual cause of an overconfident filter.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Pure Pursuit
      A geometric path-following controller that steers the vehicle toward
      a lookahead point on the reference path. The steering angle is
      computed from the curvature of the arc connecting the rear axle to
      the lookahead point. L11


.. _glossary-q:

Q
=

.. glossary::

   QoS
      Quality of Service. Configurable DDS policies governing message
      delivery in ROS 2, including reliability (best-effort vs. reliable),
      durability (transient-local vs. volatile), deadline, and lifespan.
      Critical for tuning real-time AV communication. L14

   Query, Key and Value
      The three vectors attention makes from each token, each by its
      own weight matrix set by training. The query :math:`q` is what
      the token looks for, the key :math:`k` is what it can offer, and
      the value :math:`v` is what it passes on if chosen. Each query
      scores every key with the dot product, divided by
      :math:`\sqrt{d}`, where :math:`d` is the vector length. Softmax
      turns the scores into weights, which average the values.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Quintic Polynomial Trajectory
      A 5th-degree polynomial trajectory that matches position, velocity,
      and acceleration boundary conditions at start and end points,
      producing smooth, jerk-minimized motion profiles for comfort. L11


.. _glossary-r:

R
=

.. glossary::

   RADAR
      Radio Detection and Ranging. Uses radio waves to detect objects,
      measure distance, and directly measure velocity via the Doppler
      effect. Operates in all weather conditions. Standard automotive
      frequency: 77 GHz. :doc:`L2 </lectures/lecture2/l2_index>`

   Random Error
      See Noise. Readings scatter around some center, each wrong by a
      different amount in a different direction, and the error
      averages away as you take more readings.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Redundancy
      Duplicating a capability. It protects against a component failing
      but not against a shared environmental failure. Two identical
      forward cameras are redundant, and are blinded by the same sun
      glare at the same instant. :doc:`L2 </lectures/lecture2/l2_index>`

   Re-simulation
      Replaying recorded drives against a new software build, also called log
      replay. The regression test of AV development: it proves you have not
      broken what previously worked. Being :term:`Open-Loop Evaluation`, it
      is not by itself a validation of driving ability. L13

   Recall
      The fraction of real objects that the detector successfully found:
      TP / (TP + FN). High recall means few missed detections. :doc:`L4 </lectures/lecture4/l4_index>`

   Receptive Field
      The patch of the input image that can affect one cell of a feature
      map. It grows with depth: each new layer adds its kernel size minus
      one, times the total stride of the layers before it. Through
      YOLOv8s's five stride-2, 3 by 3 layers it grows 3, 7, 15, 31, 63,
      so a cell of the stride-32 map sees at least 63 by 63 pixels.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Recursive Estimator
      An estimator that never keeps the history of readings, only the
      current estimate and its covariance :math:`P`. The Kalman filter
      is one: each cycle starts from the last estimate and :math:`P`.
      Large :math:`P` means uncertain, small :math:`P` means confident.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Reinforcement Learning (RL)
      Learning by optimizing a reward function through trial and error.
      Used in AV systems for planner fine-tuning (e.g., NVIDIA's
      end-to-end stack) and scenario-based policy improvement. L12

   ReLU
      Rectified linear unit, :math:`\max(0, x)`: an activation function
      that keeps positive numbers and turns negative ones into zero. On
      the L4 bus image, edge responses of 414.7 and -9.0 become 414.7 and
      0: "edge here" and "nothing here".
      :doc:`L4 </lectures/lecture4/l4_index>`

   Remote Assistance
      A remote human **advising** an automated vehicle, for example
      confirming that it may proceed around an obstruction, without
      taking control of the driving task. Does not change the
      feature's level. Contrast :term:`Remote Driving`.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Remote Driving
      A remote human **taking the controls** of a vehicle. This is a distinct
      mode of operation, not a :term:`DDT Fallback`, and its availability
      does not change the level of the automated feature. Contrast
      :term:`Remote Assistance`. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Repeatability
      Precision measured under the tightest conditions: same
      instrument, same operator, same setup, over a short time. It is
      not a third kind of error next to precision and trueness. Loosen
      those conditions and the same idea is called reproducibility.
      See Precision (Measurement). :doc:`L3 </lectures/lecture3/l3_index>`

   Reproducibility
      Precision measured once the tight conditions of repeatability
      (same instrument, same operator, same setup, short time) are
      loosened. Like repeatability, it describes noise, not bias. See
      Repeatability. :doc:`L3 </lectures/lecture3/l3_index>`

   Reprojection Error
      The pixel residual between where calibration places a known 3-D
      point in the image and where it really appears. Report its
      distribution, not its mean, because the tail is what breaks
      association. Check it at range, not on the bench: a production
      LiDAR-camera pair aims for rotation error below about 0.1 degree,
      and 0.1 degree is 17 cm at 100 m.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Resampling
      The particle filter's last step in each cycle: draw :math:`N` new
      particles, each old particle :math:`i` with probability
      :math:`w^{(i)}`, and reset every weight to :math:`1/N`. Heavy
      particles are copied and light ones die out. The L3 script
      resamples only when the effective number of particles falls below
      :math:`N/2`. :doc:`L3 </lectures/lecture3/l3_index>`

   ResNet
      Residual Network (He et al., 2016). A CNN whose blocks add their
      input back to their output, :math:`y = F(x) + x` (a skip
      connection), so each block learns only a correction to its input.
      That made very deep networks trainable, and every transformer
      layer uses the same idea. :doc:`L4 </lectures/lecture4/l4_index>`

   Resolution
      How close two things can be and still be told apart. It is
      independent of accuracy: a sensor can report range to the
      centimeter and still merge two objects into one. See Angular
      Resolution. :doc:`L2 </lectures/lecture2/l2_index>`

   Response
      The sum of the products of a filter's weights and the pixels
      under them: one number for one window. For a :math:`3 \times 3`
      filter :math:`w` on a window :math:`x`,
      :math:`r = \sum_{i=1}^{3} \sum_{j=1}^{3} w_{ij} x_{ij}`, with
      :math:`i` the row and :math:`j` the column. Large either way
      means an edge, and the sign gives its direction. Near 0 means no
      edge. With pixels from 0 to 255, L4's edge filter runs from -765
      to +765. :doc:`L4 </lectures/lecture4/l4_index>`

   Road Frame
      The frame every number in L3 lives in. Origin: a survey marker at
      the roadside, :math:`(0, 0)`. Axes: :math:`x` runs along the road,
      :math:`y` across it, positive toward the far curb. Unit: the meter
      on both axes. Point on the AV: its base link. A position means
      nothing until you say which frame it is in: move the marker 50 m
      up the road, and the AV at :math:`(103.0,\ 2.5)` becomes
      :math:`(53.0,\ 2.5)` without moving. See Base Link.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Rolling Shutter
      A camera readout mode where image rows are exposed sequentially
      rather than simultaneously. Produces "jello"-like distortion of
      fast-moving objects and complicates calibration in dynamic scenes;
      global-shutter sensors avoid this at higher cost. :doc:`L2 </lectures/lecture2/l2_index>`

   ROS 2
      Robot Operating System 2. An open-source middleware framework for
      building robotic systems, built on DDS for real-time communication.
      Industry standard for AV development. Used throughout ENPM818Z for
      the ``ads_pipeline`` package. :doc:`L2 </lectures/lecture2/l2_index>` · L14

   Route Completion
      The percentage of a route's distance an agent covered. One of the two
      factors in the :term:`Driving Score`; driving off-road reduces it
      rather than incurring a separate penalty. GP4 requires at least
      70%. L13

   RRT
      Rapidly-Exploring Random Tree. A sampling-based motion planning
      algorithm that incrementally builds a tree of feasible configurations
      by random sampling. RRT* is its asymptotically optimal variant. L10

   RT-DETR
      Real-Time DETR. A transformer-based detector with an efficient
      hybrid encoder that achieves real-time speed competitive with YOLO
      while maintaining the NMS-free architecture. :doc:`L4 </lectures/lecture4/l4_index>`

   RTK-GPS
      Real-Time Kinematic GPS. A GNSS technique using carrier-phase
      measurements and a nearby base station to achieve centimeter-level
      positioning accuracy. Essential for high-precision AV localization. L7


.. _glossary-s:

S
=

.. glossary::

   SAE J3016
      The SAE taxonomy of driving automation, written jointly with ISO
      TC204/WG14. It defines six levels, 0 to 5. It classifies driving
      automation features, not vehicles, by who is responsible for the
      DDT, not by how capable the technology is. It is a Recommended
      Practice, not a regulation: it has no legal force by itself,
      though regulators reference it. See SAE Level.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   SAE Level
      One of the six levels in SAE J3016: 0 no automation, 1 driver
      assistance, 2 partial automation, 3 conditional automation, 4
      high automation, 5 full automation. A level says who is
      responsible for the DDT, not how good the engineering is, and it
      applies to a feature, not a vehicle. The most consequential jump
      is 2 to 3, and it is legal rather than technical: responsibility
      moves from the person to the manufacturer.
      :doc:`L1 </lectures/lecture1/l1_index>`

   Scale Ambiguity
      A single image cannot determine absolute size or distance, because
      a small near object and a large far one project onto identical
      pixels. Scale has to come from elsewhere: camera height, known
      object sizes, ego-motion, or another sensor. :doc:`L2
      </lectures/lecture2/l2_index>`

   Scan Matching
      Aligning a new LiDAR scan to a previous scan or map by finding the
      rigid transformation that minimizes inter-point distance. Algorithms
      include ICP, NDT, and feature-based variants. It is the workhorse of
      LiDAR localization and SLAM. L7

   Safety Case
      A written argument that a system is acceptably safe in a given context,
      in three parts: **claims** (what the system will not do), **arguments**
      (why that is believed) and **evidence** (results supporting each
      argument). A folder of test results is not a safety case, because it
      never states what the results were supposed to prove. Assembled in
      Stage 5 of the concept-to-road pipeline and read there, for the first
      time, by someone outside the developer. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Sawtooth
      The shape of a filter's :math:`\sigma` over time: it climbs at
      every predict step and drops at each update. In L3's simplified
      tunnel (predict at 10 Hz, a sign match every 2.5 s), :math:`\sigma`
      climbs from 1.000 to 1.756 m, drops to 0.869 m at the first match,
      then settles between about 0.9 and 2.0 m. With no sign matches it
      grows without limit: IMU drift.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Scenario-Based Testing
      Validating an ADS against a deliberately enumerated set of situations
      rather than against distance driven, which is infeasible: demonstrating
      human-equivalent safety statistically would take hundreds of millions
      of miles. Trades an impossible sampling problem for a hard
      completeness argument. L13

   SE(3)
      The set of rigid motions in 3-D: a rotation :math:`R` and a
      translation :math:`t`, written
      :math:`T = \begin{bmatrix} R & t \\ 0 & 1 \end{bmatrix}`. Rigid
      means you may carry and turn the object, never bend or stretch
      it. Six numbers, no more: three for which way it points, three
      for where it is. :math:`SO(3)` is the rotation alone. An
      extrinsic calibration is one element of SE(3).
      :doc:`L2 </lectures/lecture2/l2_index>`

   SegFormer
      A semantic segmentation network (Xie et al., NeurIPS 2021): a
      transformer encoder, with attention between image patches as in
      L4's ViT, then a small decoder that gives 19 scores per pixel, one
      per class. The L5 hands-on runs SegFormer-B0 trained on Cityscapes,
      photos of German streets, not CARLA. Its training labels have no
      lane-marking class, so it cannot find lane lines.
      :doc:`L5 </lectures/lecture5/l5_index>`

   Self-Attention
      Attention in which the queries, keys and values all come from the
      same tokens: the image attends to itself. Used in the ViT encoder
      and in DETR's encoder. In DETR's decoder the queries also attend
      to each other this way, so one query can see that another has
      already taken an object. Contrast Cross-Attention.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Semantic Segmentation
      A perception task that assigns a class label to every pixel in an
      image (e.g., road, sidewalk, vehicle) without distinguishing
      individual instances. :doc:`L5 </lectures/lecture5/l5_index>`

   Sensor Fusion
      Combining measurements from several sensors into a single estimate
      that is better than any one sensor could provide alone. :doc:`L2
      </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>`

   Shared Error
      An error two sources have in common, so combining them cannot
      cancel it. If the HD map puts every exit sign 2 m too far along,
      the prediction and the sign match are both 2 m too far, and the
      combined estimate stays 2 m off while the filter still reports
      :math:`\pm 0.89` m. The surprise cannot reveal it; only a source
      that does not use the map, such as GNSS at the tunnel exit, can.
      The Kalman filter assumes sources share nothing.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Sigma Points
      :math:`2n+1` points (:math:`n` is the size of the state) whose
      weighted average is the mean and whose weighted spread is the
      covariance (Julier and Uhlmann, 1997). The UKF pushes each through
      the real nonlinear function and rebuilds the mean and covariance
      from where they land, so it needs no Jacobian of :math:`f` or
      :math:`h`. For the state :math:`[x, y, \theta]` that is 7 runs of
      the model per step. :doc:`L3 </lectures/lecture3/l3_index>`

   Sigmoid
      :math:`1 / (1 + e^{-x})`: turns any number into one from 0 to 1.
      YOLOv8 scores each class on its own with a sigmoid, instead of one
      softmax over all classes. The man's raw person score of 2.056 gives
      a confidence of 0.887. :doc:`L4 </lectures/lecture4/l4_index>`

   Sign Match
      The measurement in L3's tunnel, where GNSS is lost: the camera
      matches an exit sign against the HD map, and the map turns "I see
      an exit sign" into a position for the AV. Each exit sign carries
      its own number, so a match says which sign. In the Kalman filter
      it reports position (:math:`x` and :math:`y`); in the EKF, range
      and bearing to the sign. :doc:`L3 </lectures/lecture3/l3_index>`

   Sim-to-Real Gap
      The distributional mismatch between simulation-generated data and
      real-world sensor data. A fundamental challenge for training AV
      models in simulation. Mitigations include domain randomization,
      neural rendering, and fine-tuning on real data. L13

   SLAM
      Simultaneous Localization and Mapping. The problem of building a
      map of an unknown environment while simultaneously tracking the
      agent's pose within it. Comprises a frontend (scan matching,
      feature extraction) and backend (pose graph optimization, loop
      closure). L7

   Softmax
      Turns raw scores :math:`s_1, \dots, s_K`, one per class, into numbers
      that are positive and add to 1:
      :math:`p_i = e^{s_i} / (e^{s_1} + e^{s_2} + \dots + e^{s_K})`.
      Scores (2.0, 1.0, 0.1) for bus, person and car, chosen for the
      example, become 0.659, 0.242 and 0.099. The order stays the same.
      Attention uses it, and so does YOLOv8s on each side's 16 distance
      bins. YOLOv8 scores classes with a sigmoid instead.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Software-in-the-Loop (SIL)
      A test level in which the real software runs against simulated sensors
      and vehicle dynamics. This is CARLA, and the level every project in
      this course occupies. Misses timing, hardware faults and real sensor
      noise. L13

   Solid-State LiDAR
      A LiDAR that steers its beams with MEMS mirrors or electronics
      instead of a rotating assembly. It is compact, robust, cheaper at
      volume and fits into the body, but it sees only a forward wedge,
      so a car needs several. Production cars use it. A mechanical
      spinning LiDAR sees a true 360 degrees from one unit, but it is
      bulky, must sit high and has bearings that wear. Robotaxi and
      research fleets use it. :doc:`L2 </lectures/lecture2/l2_index>`

   SORT
      Simple Online and Realtime Tracking (Bewley et al., 2016). A
      minimal, efficient multi-object tracker using a Kalman filter for
      state prediction and the Hungarian algorithm for IoU-based data
      association. L6

   SOTIF
      See :term:`ISO 21448 (SOTIF)`. :doc:`L1 </lectures/lecture1/l1_lecture>` · L14

   Standard Deviation
      The square root of the variance, written with the Greek letter
      sigma: how far a typical reading sits from the mean, in the same
      units as the measurement. The usual way to quote an uncertainty.
      For L3's six GNSS readings, :math:`\sigma_x = \sqrt{2.437} = 1.56`
      m along the road. :doc:`L3 </lectures/lecture3/l3_index>`

   Stanley Controller
      A lateral path-following controller (developed for the DARPA Grand
      Challenge) that computes steering based on both heading error and
      cross-track error measured at the front axle. More aggressive
      correction than Pure Pursuit at high cross-track errors. L11

   State Vector
      The state: the list of numbers that describes the AV at one
      moment, written in bold, such as :math:`[p_x\ p_y\ v_x\ v_y]^\top`
      in the L3 tunnel or :math:`[x, y, \theta]` in the EKF. It must
      hold everything the motion model needs, including quantities no
      sensor reports directly, such as velocity, which the filter
      infers. :doc:`L3 </lectures/lecture3/l3_index>`

   Static Embedding
      An embedding that gives a piece of the input one vector, whatever
      surrounds it: the word "bank" gets the same vector in every
      sentence. ViT's patch embedding is static: a patch's vector
      depends only on its own pixels and its place. Contrast Contextual
      Embedding. :doc:`L4 </lectures/lecture4/l4_index>`

   Stereo Vision
      Depth estimation using two cameras separated by a known baseline.
      Computes depth from the disparity between left and right images. :doc:`L2 </lectures/lecture2/l2_index>`

   Stride
      How many pixels a filter moves per step as it slides over its
      input, written :math:`s`. Stride 2 skips every other position, so
      the output is half the size: YOLOv8s's first layer turns a
      :math:`480 \times 640` input into a :math:`240 \times 320` map.
      YOLOv8s has five stride-2 layers, and :math:`2^5 = 32`, so its
      coarsest grid is :math:`15 \times 20` cells, one per
      :math:`32 \times 32` pixels. See Padding.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Surprise
      L3's plain name for the innovation :math:`\nu`: the reading we got
      minus the reading we expected. The Kalman gain sets what fraction
      of it the update acts on. See Innovation.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Synchronous Mode
      A CARLA setting in which the client drives the clock: the server
      advances one fixed step, such as ``fixed_delta_seconds = 0.05``
      (20 Hz), each time the client calls ``world.tick()``. Without it
      the server runs as fast as the hardware allows, sensor data
      arrives at irregular times, and two runs of the same script
      disagree. Turn it on before you write anything else.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Systematic Error
      See Bias. :doc:`L3 </lectures/lecture3/l3_index>`

   Systematic Resampling
      Resampling a particle filter with one random number instead of
      :math:`N`: :math:`N` evenly spaced pointers walk along the running
      total of the weights, and each pointer picks the particle it
      lands in. It loses fewer good particles than :math:`N` separate
      draws. The L3 particle filter script uses it. See Resampling.
      :doc:`L3 </lectures/lecture3/l3_index>`

.. _glossary-t:

T
=

.. glossary::

   TARA
      Threat Analysis and Risk Assessment. The ISO/SAE 21434 activity that
      asks what an attacker could do and produces security goals. Performed
      in Stage 2 of the concept-to-road pipeline, alongside :term:`HARA` and
      the SOTIF analysis. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Test Pyramid
      The progression MIL → SIL → HIL → VIL → proving ground → public road.
      Cost per scenario rises by orders of magnitude down the levels and
      realism rises with it, so millions of scenarios run at the top and
      dozens at the bottom. L13

   Time of Flight
      Measuring distance by timing how long a pulse takes to travel out
      and back. For LiDAR the range is c times t divided by 2, so 2 cm
      of range accuracy requires about 133 picoseconds of timing
      precision. :doc:`L2 </lectures/lecture2/l2_index>`

   Time-of-Flight (ToF)
      ToF. See Time of Flight. :doc:`L2 </lectures/lecture2/l2_index>`

   Time Budget
      How long the detector may take on one frame. A camera at 20 Hz
      sends a frame every :math:`1000/20 = 50` ms, and the detector
      shares that time with tracking, prediction and planning. With six
      cameras on one GPU, each frame gets :math:`50/6`, about 8 ms.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Time Synchronization
      Knowing when each sensor measured. Extrinsics tell you where each
      sensor was, never when. A camera image fused with a LiDAR sweep
      captured 30 ms later is an error that no extrinsic fixes. One
      30 Hz frame of skew (33 ms) at 110 km/h is 1.01 m of travel.
      Production stacks share one clock, through PTP (IEEE 1588) over
      automotive Ethernet or GNSS-disciplined time, and every sensor
      timestamps at capture. :doc:`L2 </lectures/lecture2/l2_index>`

   Token
      One piece of the input, turned into a vector of :math:`D`
      numbers. For an image, one embedded patch or one feature-map cell.
      In a language model, a word or part of a word, which is where the
      name comes from. ViT-Base on a :math:`224 \times 224` image has
      196 patch tokens plus the class token: 197.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Track Lifecycle
      The states a track passes through: tentative, confirmed, coasting
      and deleted. Track identity must not depend on classification,
      which is the architectural lesson of the Tempe crash. :doc:`L5 </lectures/lecture5/l5_index>` · L6

   Tracking-by-Detection
      The dominant MOT paradigm: at each frame, run an object detector,
      then associate the new detections with existing tracks (via
      KF prediction + Hungarian / cosine appearance matching). Decouples
      the detector and the tracker. L6

   Transfer Learning
      Starting from a pretrained network and fine-tuning it on your own
      data. See Pretrained and Fine-Tuning.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Transform (A from B)
      The course convention for frame transforms:
      :math:`T_{A \leftarrow B}` takes a point in frame :math:`B` and
      returns it in frame :math:`A`. Say it as "A from B". Chains
      compose and the inner frames cancel,
      :math:`T_{A \leftarrow C} = T_{A \leftarrow B}\, T_{B \leftarrow C}`,
      and inverting a transform flips the arrow. Applied to a point,
      :math:`p_A = R\,p_B + t`. If the inner frames do not meet, the
      chain is written backwards. :doc:`L2 </lectures/lecture2/l2_index>`

   Trajectory Prediction
      Forecasting the future positions and states of other traffic agents
      (vehicles, pedestrians, cyclists) over a prediction horizon.
      Methods range from physics-based (CTRA) to transformer-based
      models generating multi-modal trajectory distributions. L9

   Triggering Condition
      A specific environmental or operational circumstance that causes an
      otherwise-correctly-functioning system to behave hazardously.
      Enumerating triggering conditions is the output of a :term:`SOTIF`
      analysis in Stage 2 and the input to the scenario test library in
      Stage 4. Redundancy does not address them. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Transformer
      A neural network architecture (Vaswani et al., 2017) based on
      self-attention mechanisms that model relationships between all
      positions in a sequence simultaneously. Used in DETR, BEVFormer,
      and modern AV perception. :doc:`L4 </lectures/lecture4/l4_index>` · :doc:`L5 </lectures/lecture5/l5_index>`

   Transition Matrix
      The matrix :math:`F` that moves the state forward one step on its
      own: :math:`\mathbf{x}_k = F\mathbf{x}_{k-1}`. Each row updates one
      state number. With the L3 state :math:`[p_x\ p_y\ v_x\ v_y]^\top`
      and :math:`\Delta t = 0.1` s (chosen for the example), the first
      row is :math:`[\,1\ 0\ 0.1\ 0\,]`: keep :math:`p_x` and add 0.1 s
      times the east speed, so 100 m at 10 m/s becomes 101 m. A fixed
      matrix cannot make a cosine, so the EKF uses :math:`F_k` instead,
      rebuilt every step. :doc:`L3 </lectures/lecture3/l3_index>`

   True Positive (TP)
      A detection that matches a not-yet-matched ground-truth box of its
      class, with IoU at least a threshold the evaluator sets, often
      0.5. Detections are matched from the most confident down, and
      each ground-truth box can be matched only once.
      :doc:`L4 </lectures/lecture4/l4_index>`

   Trueness
      How close the average of repeated readings sits to the truth (VIM
      2.14): the word for bias. In L3, receivers A and B scatter by the
      same 1.561 m, but B's average sits 3.2 m ahead: same precision,
      worse trueness. :doc:`L3 </lectures/lecture3/l3_index>`

   Two-Stage Detector
      An older kind of detector that first proposes regions that may
      hold an object, then classifies each one. Faster R-CNN (Ren et
      al., 2015) is L4's example. Contrast One-Stage Detector.
      :doc:`L4 </lectures/lecture4/l4_index>`


.. _glossary-u:

U
=

.. glossary::

   UKF
      Unscented Kalman Filter. See Unscented Kalman Filter. :doc:`L3 </lectures/lecture3/l3_index>`

   Ultrasonic Sensor
      A sensor that sends a short pulse of sound at about 40 kHz and
      times the echo. It uses the same time-of-flight principle as
      LiDAR, but sound travels far slower than light, so the timing is
      easy and the electronics are cheap. A production vehicle carries
      eight to twelve along the bumpers. It covers the near field below
      the bumper line that every other sensor misses. Its range is only
      0.2 to 5 m, it reports a distance and not a direction, and it
      cannot classify or measure velocity.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Uncertainty
      A number attached to an estimate saying how far the truth could
      plausibly be from it. Formally, VIM clause 2.26 defines
      measurement uncertainty as a non-negative parameter characterizing
      the spread of values that could reasonably be attributed to the
      quantity being measured. Usually expressed as a standard
      deviation. :doc:`L3 </lectures/lecture3/l3_index>`

   Underconfident
      Said of a filter whose reported uncertainty is larger than the
      errors it actually makes. In the L3 tunnel hands-on, :math:`Q` too
      big (:math:`\sigma_a = 3`) keeps the true error inside the
      :math:`\pm 1\sigma` band 84 percent of the time instead of the
      honest 68 percent. Wasteful, but safe. See Overconfident.
      :doc:`L3 </lectures/lecture3/l3_index>`

   U-Net
      An encoder-decoder segmentation architecture (Ronneberger et al.,
      2015) with skip connections that concatenate encoder features with
      decoder features at matching resolutions, preserving fine spatial
      detail for pixel-precise segmentation. :doc:`L5 </lectures/lecture5/l5_index>`

   UNECE GTR
      United Nations Economic Commission for Europe Global Technical
      Regulation. Work toward a harmonized, **safety-case-based**
      international framework for ADS is underway at UNECE. Check its current
      status before citing it. :doc:`L1 </lectures/lecture1/l1_lecture>` · L14

   UNECE R157
      UN Regulation No. 157, covering the approval of Automated Lane Keeping
      Systems. The regulation that made the first Level 3 highway deployments
      possible under EU-style type approval. :doc:`L1 </lectures/lecture1/l1_lecture>`

   UniAD
      Unified Autonomous Driving (CVPR 2023 Best Paper). A landmark
      end-to-end architecture that jointly performs perception, prediction,
      and planning through a unified transformer framework with
      planning-oriented task design. L12

   Unscented Kalman Filter
      UKF. A Kalman filter for curved models that needs no tangents: it
      pushes :math:`2n+1` sigma points through the real function and
      rebuilds the mean and covariance from where they land. The
      alternative to the EKF when the model curves hard across the
      uncertainty, or exists only as code. You write :math:`f` and
      :math:`h` but no Jacobian of either (only :math:`Q_k` still uses
      :math:`G`). That removes a silent bug: a hand-derived Jacobian
      with one wrong sign gives a filter that runs, settles and is
      wrong. :doc:`L3 </lectures/lecture3/l3_index>`

   Update Step
      The second half of every filter cycle: correct the prediction with
      a measurement by acting on part of the surprise. It computes
      :math:`\boldsymbol{\nu} = \mathbf{z} - H\hat{\mathbf{x}}^-`,
      :math:`S = HP^-H^\top + R`, :math:`K = P^-H^\top S^{-1}`,
      :math:`\hat{\mathbf{x}} = \hat{\mathbf{x}}^- + K\boldsymbol{\nu}`
      and :math:`P = (I - KH)P^-`. :math:`P` shrinks by the same amount
      whether the reading was good or wildly wrong, because the surprise
      is not in the :math:`P` line. In the L3 tunnel at 9.3 s, a 0.74 m
      surprise with :math:`K = 0.65` moves the estimate 0.48 m, and the
      position :math:`\sigma` along the tunnel goes from 1.35 to 0.80 m.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Urban Canyon
      A street lined with tall buildings, where GNSS suffers both
      blockage, which is the honest failure, and multipath, which is
      not. :doc:`L2 </lectures/lecture2/l2_index>`

.. _glossary-v:

V
=

.. glossary::

   Validation
      Checking whether the system was the right thing to build. In
      Stage 4 of the concept-to-road pipeline it means scenario-based
      simulation, then closed course, then supervised on-road testing
      with a safety driver. Contrast Verification. You can pass one and
      fail the other. :doc:`L1 </lectures/lecture1/l1_index>`

   Variance
      How spread out a set of readings is: the average of the squared
      distances from the mean. Squaring removes the sign (the plain
      distances add up to zero) and weights large errors more heavily.
      The result is in squared units (L3's six GNSS readings give 2.437
      m² along the road), so its square root, the standard deviation, is
      usually quoted instead. :doc:`L3 </lectures/lecture3/l3_index>`

   VIM
      International Vocabulary of Metrology, JCGM 200:2012. The source
      of this course's formal definitions of calibration and of
      measurement uncertainty. :doc:`L2 </lectures/lecture2/l2_index>` ·
      :doc:`L3 </lectures/lecture3/l3_index>`

   V-Model
      The ISO 26262 development lifecycle where each design stage (left
      side) is paired with a corresponding verification/test stage (right
      side), ensuring systematic validation from unit to system level. L14

   V2X
      Vehicle-to-Everything communication. Includes V2V (vehicle-to-
      vehicle), V2I (vehicle-to-infrastructure), and V2P (vehicle-to-
      pedestrian). Enables cooperative perception and situational
      awareness. L14

   Vehicle-in-the-Loop (VIL)
      A test level in which a real vehicle on a rig or test pad is fed
      synthetic objects, combining real dynamics and actuation with injected
      traffic that cannot cause harm. L13

   Verification
      Checking whether you built the thing correctly, through unit and
      module checks in Stage 3 of the concept-to-road pipeline.
      Contrast Validation, which asks whether it was the right thing to
      build. :doc:`L1 </lectures/lecture1/l1_index>`

   Vista
      A generalizable driving world model (NeurIPS 2024) that learns to
      predict diverse future video from a small amount of driving data,
      enabling synthetic scenario generation for evaluation. L13

   ViT
      Vision Transformer. A transformer architecture (Dosovitskiy et al.,
      2021) that splits images into patches and processes them as a
      sequence, applying self-attention for image classification. :doc:`L4 </lectures/lecture4/l4_index>`

   Visual Odometry
      Estimating camera ego-motion by tracking visual features across
      consecutive frames. Methods include feature-based (ORB-SLAM) and
      direct (DSO) approaches. Provides drift-prone but high-frequency
      relative pose updates. L7

   VLA Model
      Vision-Language-Action model. A multimodal architecture that
      combines visual perception, language reasoning (chain-of-thought),
      and action prediction for autonomous driving. Examples: DriveVLM,
      NVIDIA Alpamayo. L12

   Voxel
      A volumetric pixel: a discrete cell in a 3D grid. Used to
      represent point clouds (voxelization), BEV features, and 3D
      occupancy maps. Voxel size determines the trade-off between
      resolution and computational cost. :doc:`L5 </lectures/lecture5/l5_index>`

   VQ-VAE
      Vector Quantized Variational Autoencoder. A generative model that
      encodes inputs into discrete codebook tokens. Used in world models
      as a visual tokenizer to compress video frames into sequences of
      discrete tokens for autoregressive prediction. L13


.. _glossary-w:

W
=

.. glossary::

   Waypoint
      In CARLA, a discrete point on the road network containing lane
      information, speed limits, and connectivity to other waypoints.
      Used for path planning and navigation. :doc:`L2 </lectures/lecture2/l2_index>` · L8

   White Noise
      Noise whose errors are unrelated from one moment to the next, with
      no drift or slow wander. Assumed by the Kalman filter. A sensor
      whose error wanders slowly breaks the assumption, and the filter
      will trust it too much. :doc:`L3 </lectures/lecture3/l3_index>`

   World Model
      A learned model that predicts future scene states (typically video
      frames) conditioned on actions and current observations. Acts as
      a data-driven simulator for training, evaluation, and imagination-
      based planning. Examples: GAIA-3, NVIDIA Cosmos, Vista. L13


.. _glossary-y:

Y
=

.. glossary::

   YOLO
      You Only Look Once (Redmon et al., 2016). The best-known family of
      one-stage detectors: one pass of the network predicts a class and
      a box at every grid cell, then NMS removes the duplicates. L4 uses
      YOLOv8s (2023, anchor-free, 44.9 mAP on COCO). YOLO26 (2026)
      drops NMS. :doc:`L4 </lectures/lecture4/l4_index>`


.. _glossary-z:

Z
=

.. glossary::

   Zero-Doppler Filtering
      Discarding radar returns whose Doppler shift matches the
      stationary world, so that the vehicle does not brake for manhole
      covers and sign gantries. A stopped vehicle in your lane fails
      exactly the same test, which is implicated in real crashes.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Zhang's Method
      The standard technique for camera intrinsic calibration:
      photograph a planar checkerboard from many angles, detect the
      corners, and solve for the intrinsic matrix and the distortion
      coefficients. :doc:`L2 </lectures/lecture2/l2_index>`
