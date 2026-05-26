====================================================
Glossary
====================================================

:ref:`A <glossary-a>` · :ref:`B <glossary-b>` · :ref:`C <glossary-c>` · :ref:`D <glossary-d>` · :ref:`E <glossary-e>` · :ref:`F <glossary-f>` · :ref:`G <glossary-g>` · :ref:`H <glossary-h>` · :ref:`I <glossary-i>` · :ref:`J <glossary-j>` · :ref:`K <glossary-k>` · :ref:`L <glossary-l>` · :ref:`M <glossary-m>` · :ref:`N <glossary-n>` · :ref:`O <glossary-o>` · :ref:`P <glossary-p>` · :ref:`Q <glossary-q>` · :ref:`R <glossary-r>` · :ref:`S <glossary-s>` · :ref:`T <glossary-t>` · :ref:`U <glossary-u>` · :ref:`V <glossary-v>` · :ref:`W <glossary-w>` · :ref:`Y <glossary-y>`

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

   ADAS
      Advanced Driver Assistance Systems. Systems that support the human
      driver in performing parts of the Dynamic Driving Task. Corresponds
      to SAE Levels 1--2. Examples: Adaptive Cruise Control, Lane Keeping
      Assist. :doc:`L1 </lectures/lecture1/l1_lecture>`

   ADS
      Automated Driving Systems. Systems that perform the entire Dynamic
      Driving Task without human intervention within a specified ODD.
      Corresponds to SAE Levels 3--5. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Anchor Box
      A predefined bounding box shape (width, height) used by object
      detectors like YOLO v3--v7 as a reference for predicting object
      locations. Anchor-free detectors (YOLOv8+, DETR) eliminate these. :doc:`L4 </lectures/lecture4/l4_lecture>`

   A* Search
      A heuristic graph-search algorithm that finds the shortest path from
      start to goal by expanding the node with the lowest :math:`f(n) =
      g(n) + h(n)`, where :math:`g` is the cost so far and :math:`h` is an
      admissible heuristic. Used for global route planning on the road
      graph and for grid/lattice-based motion planning. :doc:`L8 </lectures/lecture8/l8_lecture>` · :doc:`L10 </lectures/lecture10/l10_lecture>`

   ASIL
      Automotive Safety Integrity Level. Defined by ISO 26262 to classify
      the severity of safety risks. Ranges from ASIL A (lowest) to ASIL D
      (highest), determining the rigor of development and testing required. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_lecture>`

   ASPP
      Atrous Spatial Pyramid Pooling. The multi-scale context module in
      DeepLabv3+ that applies parallel dilated convolutions at several
      rates (e.g., 6, 12, 18) and pools at multiple scales, then
      concatenates the outputs -- capturing objects at varying scales in
      a single forward pass. :doc:`L5 </lectures/lecture5/l5_lecture>`


.. _glossary-b:

B
=

.. glossary::

   Backbone
      The feature extraction component of an object detection architecture.
      In YOLO, this is typically CSPDarknet or similar CNN that extracts
      hierarchical features from the input image. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Bayer Pattern
      The colour filter array placed over a monochrome camera sensor
      (typically RGGB) so that each pixel records only one colour channel.
      Demosaicing reconstructs full RGB images. Determines per-channel
      resolution and low-light noise behaviour. :doc:`L2 </lectures/lecture2/l2_lecture>`

   Behavior Cloning
      An imitation learning approach where a policy is trained by supervised
      regression on expert state-action pairs. Simple but suffers from
      distribution shift and compounding errors that grow as
      :math:`O(\epsilon T^2)`. :doc:`L12 </lectures/lecture12/l12_lecture>`

   Behavior Planning
      The strategic decision-making layer that selects high-level maneuvers
      (lane follow, lane change, yield, stop) based on the current driving
      context. Often implemented as a finite state machine (FSM). :doc:`L9 </lectures/lecture9/l9_lecture>`

   BEV
      Bird's-Eye View. A top-down representation of the driving scene that
      projects sensor data into an ego-centric 2D plane. The dominant
      perception paradigm in modern AV systems. See also: BEVFormer. :doc:`L5 </lectures/lecture5/l5_lecture>`

   BEVFormer
      A transformer-based BEV construction method (Li et al., ECCV 2022)
      that uses learnable BEV queries with spatial cross-attention and
      temporal self-attention to build BEV features from multi-camera images. :doc:`L5 </lectures/lecture5/l5_lecture>`

   BEVFusion
      A multi-sensor BEV fusion framework that unifies camera and LiDAR
      features in a shared BEV space using learned attention-weighted
      aggregation. :doc:`L6 </lectures/lecture6/l6_lecture>`

   Bicycle Model
      A simplified kinematic vehicle model that merges the two front wheels
      and two rear wheels into single virtual wheels. Used as the foundation
      for motion planning and control. :doc:`L10 </lectures/lecture10/l10_lecture>` · :doc:`L11 </lectures/lecture11/l11_lecture>`

   Bipartite Matching
      The Hungarian algorithm used by DETR to find an optimal one-to-one
      assignment between predicted objects and ground truth during training.
      Eliminates the need for NMS. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Blueprint Library
      In CARLA, a collection of templates for creating actors (vehicles,
      pedestrians, sensors) with configurable attributes like color and
      sensor parameters. :doc:`L1 </lectures/lecture1/l1_lecture>`

   B-Spline
      A piecewise polynomial curve with local control point support, used
      for smooth trajectory representation in motion planning. Changes to
      one control point only affect a local segment of the curve. :doc:`L11 </lectures/lecture11/l11_lecture>`

   ByteTrack
      A multi-object tracking method (Zhang et al., 2022) that recovers
      occluded objects by performing a second association pass using
      low-confidence detections that other trackers would discard. :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _glossary-c:

C
=

.. glossary::

   Calibration (Extrinsic)
      The process of determining the 6-DOF transformation (rotation +
      translation) between sensors or between a sensor and the vehicle
      frame. Essential for multi-sensor fusion. :doc:`L2 </lectures/lecture2/l2_lecture>`

   Calibration (Intrinsic)
      The process of determining a camera's internal parameters: focal
      lengths (fx, fy), principal point (cx, cy), and distortion
      coefficients. Typically performed using checkerboard patterns. :doc:`L2 </lectures/lecture2/l2_lecture>`

   CARLA
      CAR Learning to Act. An open-source autonomous driving simulator
      built on Unreal Engine 4, providing realistic urban/highway
      environments, sensor simulation, and a Python API. :doc:`L1 </lectures/lecture1/l1_lecture>`

   CIoU Loss
      Complete Intersection over Union loss. A bounding box regression
      loss used in YOLO that penalizes overlap, center distance, and
      aspect ratio simultaneously. :doc:`L4 </lectures/lecture4/l4_lecture>`

   CNN
      Convolutional Neural Network. A class of deep neural networks that
      use convolutional layers to extract spatial features from images.
      The backbone architecture for most object detectors. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Collision Detection
      The geometric test that determines whether a candidate path or
      trajectory intersects any obstacle (often expressed as inflated
      bounding boxes, OBBs, or Minkowski sums). Run at every node
      expansion during sampling- and graph-based planning. :doc:`L10 </lectures/lecture10/l10_lecture>`

   Complementarity Principle
      The observation (Luo, 1989) that different sensor technologies have
      unique strengths and weaknesses that balance each other out, making
      multi-sensor fusion essential for robust perception. :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L3 </lectures/lecture3/l3_lecture>`

   Configuration Space
      The space of all possible vehicle configurations, typically
      :math:`(x, y, \theta)` for a planar robot. Obstacles are mapped into
      configuration space to simplify collision checking during planning. :doc:`L10 </lectures/lecture10/l10_lecture>`

   Cooperative Perception
      Multiple vehicles or roadside units sharing sensor data via V2X
      communication to build a collective, extended understanding of the
      driving scene beyond any single vehicle's sensor range. :doc:`L14 </lectures/lecture14/l14_lecture>`

   Cross-Attention Fusion
      A deep learning fusion approach that uses transformer cross-attention
      mechanisms to learn how features from one sensor modality should
      attend to features from another (e.g., camera features attending to
      LiDAR features in BEVFusion). :doc:`L6 </lectures/lecture6/l6_lecture>`

   Cross-Track Error
      The lateral distance between the vehicle (typically measured at the
      front axle for Stanley, rear axle for Pure Pursuit) and the nearest
      point on the reference path. Drives the steering correction in both
      controllers. :doc:`L11 </lectures/lecture11/l11_lecture>`

   CTRA
      Constant Turn Rate and Acceleration. A physics-based motion prediction
      model that assumes constant yaw rate and longitudinal acceleration.
      More realistic than constant-velocity models for curving trajectories. :doc:`L9 </lectures/lecture9/l9_lecture>`

   C-V2X
      Cellular Vehicle-to-Everything. A 3GPP-based V2X communication
      standard (LTE-V2X, NR-V2X/5G) that leverages cellular infrastructure
      for vehicle communication. Competing with DSRC for V2X deployment. :doc:`L14 </lectures/lecture14/l14_lecture>`


.. _glossary-d:

D
=

.. glossary::

   DAgger
      Dataset Aggregation. An iterative imitation learning algorithm that
      addresses distribution shift by collecting new training data under
      the learner's own policy, then re-labeling with the expert's actions.
      Reduces per-step regret from :math:`O(\epsilon T^2)` (BC) to
      :math:`O(\epsilon)`. :doc:`L12 </lectures/lecture12/l12_lecture>`

   Data Association
      The problem of deciding which incoming measurement corresponds to
      which existing track (or that it is a new object / clutter). Solved
      by nearest-neighbour, Hungarian/GNN, JPDA, or MHT depending on the
      ambiguity tolerated. :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`

   DDS
      Data Distribution Service. An OASIS/OMG standard for real-time
      publish-subscribe communication. The middleware layer underlying
      ROS 2, providing configurable QoS policies for message delivery. :doc:`L14 </lectures/lecture14/l14_lecture>`

   DDT
      Dynamic Driving Task. All real-time operational and tactical
      functions required to operate a vehicle in on-road traffic, including
      steering, acceleration, monitoring, and object detection. Excludes
      strategic functions like trip scheduling. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Dead Reckoning
      Estimating current position by integrating motion measurements
      (wheel odometry, IMU) from a known prior pose. Accumulates drift
      over time without external corrections. :doc:`L7 </lectures/lecture7/l7_lecture>`

   DeepLabv3+
      A semantic segmentation architecture (Chen et al., 2018) using atrous
      (dilated) convolutions and Atrous Spatial Pyramid Pooling (ASPP) to
      capture multi-scale context without reducing spatial resolution. :doc:`L5 </lectures/lecture5/l5_lecture>`

   DeepSORT
      Deep Simple Online and Realtime Tracking (Wojke et al., 2017).
      Extends SORT with a deep appearance descriptor (128-D embedding)
      for re-identification after occlusion. :doc:`L6 </lectures/lecture6/l6_lecture>`

   DETR
      DEtection TRansformer. A transformer-based object detector that
      frames detection as a set prediction problem. Uses object queries
      and bipartite matching instead of anchors and NMS. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Diffusion-Based Planning
      Motion planning via iterative denoising of trajectories, learned
      from expert demonstrations. Models the trajectory distribution as
      a diffusion process and generates plans by reverse diffusion.
      Examples: Diffusion Planner (ICLR 2025), DiffusionDrive (CVPR 2025). :doc:`L10 </lectures/lecture10/l10_lecture>`

   Dijkstra
      A classical shortest-path graph search algorithm that expands nodes
      in order of accumulated cost from the source. Equivalent to A* with
      zero heuristic; preferred when no useful heuristic is available. :doc:`L8 </lectures/lecture8/l8_lecture>` · :doc:`L10 </lectures/lecture10/l10_lecture>`

   Dilated Convolution
      A convolution that inserts "holes" (zeros) between kernel weights,
      enlarging the receptive field without downsampling spatial resolution.
      Foundation of DeepLabv3+'s ASPP module. Also called *atrous*
      convolution. :doc:`L5 </lectures/lecture5/l5_lecture>`

   Disparity
      The horizontal pixel difference between where the same 3D point
      appears in left and right stereo camera images. Used to compute
      depth: ``depth = (B x f) / d``. :doc:`L2 </lectures/lecture2/l2_lecture>`

   Distribution Shift
      The mismatch between the state distribution seen during training and
      the distribution encountered during deployment. A key failure mode
      of behavior cloning where small errors compound over time. :doc:`L12 </lectures/lecture12/l12_lecture>`

   Domain Randomization
      Varying simulation parameters (lighting, textures, weather, sensor
      noise) during training to improve robustness and sim-to-real transfer
      of learned models. :doc:`L13 </lectures/lecture13/l13_lecture>`

   Doppler Effect
      The frequency shift in a reflected signal caused by the relative
      motion of the target. RADAR uses this to directly measure the
      velocity of moving objects. :doc:`L2 </lectures/lecture2/l2_lecture>`

   DriveTransformer
      An end-to-end autonomous driving model (ICLR 2025) that uses shared
      attention across all perception, prediction, and planning tasks,
      achieving high throughput through task-parallel processing. :doc:`L12 </lectures/lecture12/l12_lecture>`

   DriveVLM
      A Vision-Language-Action model for autonomous driving (Tian et al.,
      2024) that combines a vision-language reasoning model with a fast
      driving policy, producing chain-of-thought scene descriptions
      alongside action outputs. :doc:`L12 </lectures/lecture12/l12_lecture>`

   DSRC
      Dedicated Short-Range Communications (IEEE 802.11p). The original
      V2X communication technology operating in the 5.9 GHz band.
      Competing with C-V2X for industry adoption. :doc:`L14 </lectures/lecture14/l14_lecture>`

   Dynamic Range
      The ratio between the brightest and darkest elements a camera sensor
      can capture simultaneously. Measured in dB; 120 dB means a million-
      to-one brightness ratio. :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _glossary-e:

E
=

.. glossary::

   End-to-End Driving
      An approach where a single neural network maps raw sensor input
      directly to driving actions, bypassing the traditional modular
      pipeline (perception -> planning -> control). :doc:`L12 </lectures/lecture12/l12_lecture>`

   EKF
      Extended Kalman Filter. A non-linear extension of the Kalman Filter
      that uses Jacobian matrices to linearize the system at each time
      step. The standard fusion filter for IMU + GNSS + wheel odometry in
      AV localization. :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L7 </lectures/lecture7/l7_lecture>`


.. _glossary-f:

F
=

.. glossary::

   FMEA
      Failure Mode and Effects Analysis. A systematic method for
      identifying potential failure modes in a system, assessing their
      impact, and designing mitigations (e.g., sensor redundancy). :doc:`L14 </lectures/lecture14/l14_lecture>`

   Focal Loss
      A modified cross-entropy loss (Lin et al., 2017) that down-weights
      easy examples to focus training on hard, misclassified cases.
      Critical for one-stage detectors dealing with extreme
      foreground/background class imbalance. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Foundation Model
      A large neural network pre-trained on broad data at scale and
      adaptable to many downstream tasks (e.g., GPT, CLIP). In AV, used
      as VLA backbones (DriveVLM, NVIDIA Alpamayo) and as world-model
      starting points. :doc:`L12 </lectures/lecture12/l12_lecture>` · :doc:`L13 </lectures/lecture13/l13_lecture>`

   FPN
      Feature Pyramid Network. A neck architecture that fuses features
      across multiple scales via a top-down pathway with lateral
      connections, enabling detection of objects at different sizes. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Frenet Frame
      A curvilinear coordinate system :math:`(s, d)` defined along a road
      centerline, where :math:`s` is the arc-length along the path and
      :math:`d` is the lateral offset. Simplifies trajectory planning on
      curved roads. :doc:`L11 </lectures/lecture11/l11_lecture>`

   FSM
      Finite State Machine. A classical approach to behavior planning using
      discrete states (lane follow, lane change, stop, yield) and
      transition rules. Simple, interpretable, but brittle for complex
      scenarios. :doc:`L9 </lectures/lecture9/l9_lecture>`

   Fusion Architecture
      The strategy for combining data from multiple sensors. Three main
      types: early fusion (raw data), intermediate/mid-level fusion
      (features), and late fusion (detection outputs). :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _glossary-g:

G
=

.. glossary::

   GAIA-3
      Wayve's 15-billion-parameter generative driving world model
      (December 2025) that predicts realistic future driving video
      conditioned on actions and text prompts. :doc:`L13 </lectures/lecture13/l13_lecture>`

   GNN
      Graph Neural Network. A neural network operating on graph-structured
      data. Used in trajectory prediction to model interactions between
      agents, where nodes represent agents and edges represent
      relationships. :doc:`L9 </lectures/lecture9/l9_lecture>`

   GNSS
      Global Navigation Satellite System. Provides absolute position
      (latitude, longitude, altitude). Includes GPS (US), GLONASS
      (Russia), Galileo (EU), BeiDou (China). :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L7 </lectures/lecture7/l7_lecture>`


.. _glossary-h:

H
=

.. glossary::

   HARA
      Hazard Analysis and Risk Assessment. An ISO 26262 process for
      systematically identifying potential hazards, assessing their
      severity, exposure, and controllability, and assigning ASIL levels. :doc:`L14 </lectures/lecture14/l14_lecture>`

   HD Map
      High-Definition map with centimeter-accurate road geometry, lane
      markings, traffic signs, and semantic annotations. Used for precise
      localization by matching live sensor data against the map. :doc:`L7 </lectures/lecture7/l7_lecture>` · :doc:`L8 </lectures/lecture8/l8_lecture>`

   Head (Detection)
      The final component of an object detection architecture that
      produces bounding box coordinates and class predictions. Can be
      anchor-based (YOLO v3--v7) or anchor-free (YOLOv8+, DETR). :doc:`L4 </lectures/lecture4/l4_lecture>`

   HOTA
      Higher Order Tracking Accuracy. A tracking evaluation metric that
      balances detection quality and association quality equally via
      their geometric mean, addressing biases in MOTA and IDF1. :doc:`L6 </lectures/lecture6/l6_lecture>`

   Hungarian Algorithm
      An optimization algorithm that finds the minimum-cost one-to-one
      assignment between two sets. Used by DETR for bipartite matching
      between predictions and ground truth, and by SORT/DeepSORT for
      association between predicted tracks and new detections. :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L4 </lectures/lecture4/l4_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _glossary-i:

I
=

.. glossary::

   ICP
      Iterative Closest Point. An algorithm for aligning two point clouds
      by iteratively finding closest-point correspondences and minimizing
      the alignment error. Core algorithm for scan matching in SLAM and
      LiDAR odometry. :doc:`L7 </lectures/lecture7/l7_lecture>`

   IDF1
      Identity F1 Score. A tracking evaluation metric computed as the F1
      score of correct identity assignments. Emphasizes consistent ID
      maintenance over raw detection accuracy. :doc:`L6 </lectures/lecture6/l6_lecture>`

   IMU
      Inertial Measurement Unit. Measures linear acceleration
      (accelerometers) and angular velocity (gyroscopes) at high
      frequency (>100 Hz). Suffers from drift over time. :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L7 </lectures/lecture7/l7_lecture>`

   Instance Segmentation
      A perception task that assigns each object a unique ID and
      pixel-level mask, distinguishing individual instances of the same
      class (e.g., car #1 vs. car #2). :doc:`L5 </lectures/lecture5/l5_lecture>`

   IoU
      Intersection over Union. The ratio of the overlap area to the
      union area of a predicted and ground truth bounding box. Used as
      the primary metric for evaluating detection localization. :doc:`L4 </lectures/lecture4/l4_lecture>`

   ISO 26262
      International standard for functional safety of road vehicle
      electrical and electronic systems. Defines ASIL levels to classify
      risk severity. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_lecture>`

   ISO 21448 (SOTIF)
      Safety of the Intended Functionality. Addresses safety hazards that
      occur without a system failure (e.g., sensor limitations). A
      critical complement to ISO 26262. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_lecture>`


.. _glossary-j:

J
=

.. glossary::

   JPDA
      Joint Probabilistic Data Association. A probabilistic data
      association method for multi-target tracking in clutter that
      considers all possible measurement-to-track assignments weighted
      by their probabilities. :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _glossary-k:

K
=

.. glossary::

   Kalman Filter
      An optimal recursive estimator for linear systems with Gaussian
      noise. Uses a predict-update cycle to fuse noisy sensor measurements
      over time. Foundation of IMU+GNSS fusion and the state-update step
      inside SORT and DeepSORT. :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>` · :doc:`L7 </lectures/lecture7/l7_lecture>`

   Kalman Gain
      The blending factor in the Kalman Filter that determines how much
      weight to give to the new measurement vs. the prediction. High
      trust in sensor = high gain; high trust in prediction = low gain. :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _glossary-l:

L
=

.. glossary::

   Lanelet2
      An open lane-graph map format (Poggenhans et al., 2018) widely used
      by Autoware and many research stacks. Represents drivable lanes as
      typed line strings with explicit topological connectivity. :doc:`L8 </lectures/lecture8/l8_lecture>`

   Lattice Planner
      A motion planning approach that performs graph search on a
      pre-computed state lattice of kinematically feasible motion
      primitives. Combines the completeness of graph search with
      kinematic feasibility. :doc:`L10 </lectures/lecture10/l10_lecture>`

   LiDAR
      Light Detection and Ranging. Uses laser pulses and time-of-flight
      to measure distances, producing 3D point clouds. Key specs: range,
      points per second, accuracy, beam count. :doc:`L2 </lectures/lecture2/l2_lecture>`

   LiDAR Odometry
      Estimating ego-motion by matching consecutive LiDAR scans using
      algorithms like ICP or feature-based methods (LOAM). More robust
      than visual odometry in low-light and textureless environments. :doc:`L7 </lectures/lecture7/l7_lecture>`

   Lift-Splat-Shoot (LSS)
      A foundational camera-to-BEV projection method (Philion & Fidler,
      NeurIPS 2020) that predicts per-pixel depth distributions (Lift),
      projects features into a voxel grid (Splat), and collapses to BEV
      (Shoot). Fully differentiable end-to-end. :doc:`L5 </lectures/lecture5/l5_lecture>`

   LOAM
      LiDAR Odometry and Mapping. A foundational LiDAR SLAM system that
      separates high-frequency odometry (edge and planar feature matching)
      from low-frequency mapping for real-time operation. :doc:`L7 </lectures/lecture7/l7_lecture>`

   Long-Tail Scenarios
      Rare but safety-critical driving events (e.g., a mattress on the
      highway, a child running into the road) that are underrepresented
      in training data. The primary data challenge in AV development. :doc:`L13 </lectures/lecture13/l13_lecture>` · :doc:`L14 </lectures/lecture14/l14_lecture>`

   Loop Closure
      Detection of a previously visited location during SLAM, used to
      correct accumulated drift by adding a constraint in the pose graph.
      Methods include scan context, visual bag-of-words, and neural
      descriptors. :doc:`L7 </lectures/lecture7/l7_lecture>`


.. _glossary-m:

M
=

.. glossary::

   Mahalanobis Distance
      A distance metric that accounts for the covariance (uncertainty)
      of a distribution. Used in data association to determine whether a
      measurement is statistically consistent with a predicted track state. :doc:`L3 </lectures/lecture3/l3_lecture>`

   mAP
      Mean Average Precision. The primary metric for evaluating object
      detectors. mAP@0.5 uses a single IoU threshold; mAP@0.5:0.95
      averages across thresholds for stricter evaluation. :doc:`L4 </lectures/lecture4/l4_lecture>` · :doc:`L5 </lectures/lecture5/l5_lecture>`

   Mask R-CNN
      An instance segmentation model (He et al., 2017) that extends Faster
      R-CNN with a mask head predicting a binary segmentation mask for each
      detected bounding box, enabling pixel-level object delineation. :doc:`L5 </lectures/lecture5/l5_lecture>`

   MCL
      Monte Carlo Localization. A particle filter-based localization
      algorithm that represents the robot's belief as a set of weighted
      samples. AMCL (Adaptive MCL) dynamically adjusts particle count.
      Standard localization algorithm in ROS. :doc:`L7 </lectures/lecture7/l7_lecture>`

   MHT
      Multiple Hypothesis Tracking. A data association method that
      maintains a tree of hypotheses for measurement-to-track assignments,
      deferring hard decisions to resolve ambiguity over time. :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`

   MOTA
      Multi-Object Tracking Accuracy. A tracking metric computed as
      :math:`1 - (FN + FP + IDSW) / GT`, penalizing false negatives,
      false positives, and identity switches. Range: :math:`(-\infty, 1]`. :doc:`L6 </lectures/lecture6/l6_lecture>`

   MOTP
      Multi-Object Tracking Precision. The average overlap (IoU) between
      true positives and their assigned ground-truth boxes. Complements
      MOTA by measuring localisation quality independently of identity
      switches. :doc:`L6 </lectures/lecture6/l6_lecture>`

   MPC
      Model Predictive Control. A receding-horizon optimization-based
      controller that solves a finite-horizon optimal control problem at
      each time step, applying only the first control action. Dominant
      controller in production AV systems. :doc:`L11 </lectures/lecture11/l11_lecture>`

   MRC
      Minimal Risk Condition. A pre-planned safe response when a critical
      system failure is detected (e.g., safely pulling over and stopping). :doc:`L14 </lectures/lecture14/l14_lecture>`

   Multi-Modal Prediction
      A trajectory prediction output that represents several plausible
      futures simultaneously (typically as :math:`K` weighted trajectory
      modes), capturing the inherent uncertainty in other agents'
      intentions. :doc:`L9 </lectures/lecture9/l9_lecture>`

   Multi-Object Tracking (MOT)
      The task of maintaining consistent identity for detected objects
      across consecutive frames. Methods: SORT, DeepSORT, ByteTrack,
      transformer-based MOT. :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _glossary-n:

N
=

.. glossary::

   Neck
      The multi-scale feature fusion component of a detection
      architecture, positioned between the backbone and head. Examples:
      FPN, PAN, BiFPN. :doc:`L4 </lectures/lecture4/l4_lecture>`

   NDS
      nuScenes Detection Score. A composite ranking metric for 3D object
      detection on nuScenes, combining mAP with five true-positive error
      metrics (translation, scale, orientation, velocity, attribute). :doc:`L5 </lectures/lecture5/l5_lecture>`

   NDT
      Normal Distributions Transform. A point cloud registration method
      that represents clouds as a grid of Gaussian distributions.
      Used in Autoware for LiDAR-based localization. Faster than ICP
      for large-scale matching. :doc:`L7 </lectures/lecture7/l7_lecture>`

   NMS
      Non-Maximum Suppression. A post-processing step that removes
      duplicate detections by suppressing overlapping bounding boxes
      with lower confidence. Not needed in DETR. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Nonholonomic Constraint
      A motion constraint that limits achievable velocities but not the
      configuration space itself. A car cannot move sideways instantaneously
      (no lateral velocity in the body frame) -- planners must respect this
      when generating paths. :doc:`L10 </lectures/lecture10/l10_lecture>`

   nuScenes
      A widely used AV benchmark dataset (Caesar et al., 2020) with
      synchronized 6-camera, 5-radar, 1-LiDAR, IMU, and GPS data over
      1000 driving scenes. Standard evaluation for BEV detection and
      tracking; uses the NDS composite score. :doc:`L5 </lectures/lecture5/l5_lecture>`

   NVIDIA Cosmos
      NVIDIA's family of world foundation models for physical AI,
      designed to generate realistic driving video and enable
      simulation-based AV training and evaluation. :doc:`L13 </lectures/lecture13/l13_lecture>`


.. _glossary-o:

O
=

.. glossary::

   Object Query
      In DETR, a learned embedding that is input to the transformer
      decoder. Each query attends to the encoded image features via
      cross-attention and specializes in detecting one object. :doc:`L4 </lectures/lecture4/l4_lecture>`

   ODD
      Operational Design Domain. The specific operating conditions
      (geographic, environmental, traffic) under which an ADS is designed
      to function safely. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Occupancy Network (3D)
      A perception architecture that predicts the semantic state of every
      voxel in a 3D volume around the vehicle, capturing arbitrary geometry
      beyond what bounding boxes can represent. Key methods: MonoScene,
      TPVFormer, Occ3D. :doc:`L5 </lectures/lecture5/l5_lecture>`

   OES
      Operating Envelope Specification. A formal, machine-readable format
      proposed by NIST for precisely defining an ADS's ODD. :doc:`L1 </lectures/lecture1/l1_lecture>`

   OpenDRIVE
      An ASAM open standard for describing road networks (geometry,
      lanes, signals, junctions) in XML. Widely used as an interchange
      format between map providers, simulators (including CARLA), and
      planning stacks. :doc:`L8 </lectures/lecture8/l8_lecture>`


.. _glossary-p:

P
=

.. glossary::

   PAN
      Path Aggregation Network. A neck architecture that adds a bottom-up
      pathway to FPN, improving information flow for accurate localization.
      Used in YOLO v4+. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Panoptic Segmentation
      A perception task that combines semantic segmentation (labeling
      "stuff" like road, sky) with instance segmentation (identifying
      individual "things" like cars, pedestrians). :doc:`L5 </lectures/lecture5/l5_lecture>`

   Particle Filter
      A non-parametric filter that approximates probability distributions
      using a set of weighted random samples (particles). Can handle
      arbitrary non-linear and non-Gaussian systems. :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L7 </lectures/lecture7/l7_lecture>`

   Perception
      The process by which an autonomous system transforms unstructured
      sensor data into a structured, semantic understanding of the
      surrounding environment. :doc:`L4 </lectures/lecture4/l4_lecture>` · :doc:`L5 </lectures/lecture5/l5_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`

   PID Controller
      Proportional-Integral-Derivative controller. A classical feedback
      controller used for longitudinal speed control in AVs. The three
      terms correct present error (P), accumulated past error (I), and
      predicted future error (D). :doc:`L11 </lectures/lecture11/l11_lecture>`

   Pinhole Camera Model
      The idealized projective camera model that maps 3D world points to
      2D image coordinates via the intrinsic matrix
      :math:`K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}`.
      Underlies intrinsic calibration and stereo geometry. :doc:`L2 </lectures/lecture2/l2_lecture>`

   Pose Graph Optimization
      The SLAM backend formulation that represents the robot trajectory
      as a graph of poses (nodes) and relative constraints (edges), then
      optimizes all poses jointly to minimize constraint errors. :doc:`L7 </lectures/lecture7/l7_lecture>`

   Precision
      The fraction of detections that are correct: TP / (TP + FP).
      High precision means few false positives. :doc:`L4 </lectures/lecture4/l4_lecture>`

   PRM
      Probabilistic Road Map. A multi-query sampling-based planner that
      pre-computes a graph of collision-free configurations connected by
      feasible paths, then searches this graph for start-to-goal queries. :doc:`L10 </lectures/lecture10/l10_lecture>`

   Pure Pursuit
      A geometric path-following controller that steers the vehicle toward
      a lookahead point on the reference path. The steering angle is
      computed from the curvature of the arc connecting the rear axle to
      the lookahead point. :doc:`L11 </lectures/lecture11/l11_lecture>`


.. _glossary-q:

Q
=

.. glossary::

   QoS
      Quality of Service. Configurable DDS policies governing message
      delivery in ROS 2, including reliability (best-effort vs. reliable),
      durability (transient-local vs. volatile), deadline, and lifespan.
      Critical for tuning real-time AV communication. :doc:`L14 </lectures/lecture14/l14_lecture>`

   Quintic Polynomial Trajectory
      A 5th-degree polynomial trajectory that matches position, velocity,
      and acceleration boundary conditions at start and end points,
      producing smooth, jerk-minimized motion profiles for comfort. :doc:`L11 </lectures/lecture11/l11_lecture>`


.. _glossary-r:

R
=

.. glossary::

   RADAR
      Radio Detection and Ranging. Uses radio waves to detect objects,
      measure distance, and directly measure velocity via the Doppler
      effect. Operates in all weather conditions. Standard automotive
      frequency: 77 GHz. :doc:`L2 </lectures/lecture2/l2_lecture>`

   Recall
      The fraction of real objects that the detector successfully found:
      TP / (TP + FN). High recall means few missed detections. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Reinforcement Learning (RL)
      Learning by optimizing a reward function through trial and error.
      Used in AV systems for planner fine-tuning (e.g., NVIDIA's
      end-to-end stack) and scenario-based policy improvement. :doc:`L12 </lectures/lecture12/l12_lecture>`

   Reprojection Error
      The distance (in pixels) between a known 3D point projected onto
      the image using calibrated parameters and its actual observed
      position. Used to validate calibration quality; should be < 2 px. :doc:`L2 </lectures/lecture2/l2_lecture>`

   ResNet
      Residual Network. A CNN architecture (He et al., 2016) that
      introduced skip connections, enabling training of very deep
      networks (50--152 layers) without degradation. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Rolling Shutter
      A camera readout mode where image rows are exposed sequentially
      rather than simultaneously. Produces "jello"-like distortion of
      fast-moving objects and complicates calibration in dynamic scenes;
      global-shutter sensors avoid this at higher cost. :doc:`L2 </lectures/lecture2/l2_lecture>`

   ROS 2
      Robot Operating System 2. An open-source middleware framework for
      building robotic systems, built on DDS for real-time communication.
      Industry standard for AV development. Used throughout ENPM818Z for
      the ``ads_pipeline`` package. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_lecture>`

   RRT
      Rapidly-Exploring Random Tree. A sampling-based motion planning
      algorithm that incrementally builds a tree of feasible configurations
      by random sampling. RRT* is its asymptotically optimal variant. :doc:`L10 </lectures/lecture10/l10_lecture>`

   RT-DETR
      Real-Time DETR. A transformer-based detector with an efficient
      hybrid encoder that achieves real-time speed competitive with YOLO
      while maintaining the NMS-free architecture. :doc:`L4 </lectures/lecture4/l4_lecture>`

   RTK-GPS
      Real-Time Kinematic GPS. A GNSS technique using carrier-phase
      measurements and a nearby base station to achieve centimeter-level
      positioning accuracy. Essential for high-precision AV localization. :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L7 </lectures/lecture7/l7_lecture>`


.. _glossary-s:

S
=

.. glossary::

   SAE J3016
      The Society of Automotive Engineers standard that defines six levels
      of driving automation (Level 0--5), the industry-standard
      classification system. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Scan Matching
      Aligning a new LiDAR scan to a previous scan or map by finding the
      rigid transformation that minimizes inter-point distance. Algorithms
      include ICP, NDT, and feature-based variants -- the workhorse of
      LiDAR localization and SLAM. :doc:`L7 </lectures/lecture7/l7_lecture>`

   Semantic Segmentation
      A perception task that assigns a class label to every pixel in an
      image (e.g., road, sidewalk, vehicle) without distinguishing
      individual instances. :doc:`L5 </lectures/lecture5/l5_lecture>`

   Sim-to-Real Gap
      The distributional mismatch between simulation-generated data and
      real-world sensor data. A fundamental challenge for training AV
      models in simulation. Mitigations include domain randomization,
      neural rendering, and fine-tuning on real data. :doc:`L13 </lectures/lecture13/l13_lecture>`

   SLAM
      Simultaneous Localization and Mapping. The problem of building a
      map of an unknown environment while simultaneously tracking the
      agent's pose within it. Comprises a frontend (scan matching,
      feature extraction) and backend (pose graph optimization, loop
      closure). :doc:`L7 </lectures/lecture7/l7_lecture>`

   SORT
      Simple Online and Realtime Tracking (Bewley et al., 2016). A
      minimal, efficient multi-object tracker using a Kalman filter for
      state prediction and the Hungarian algorithm for IoU-based data
      association. :doc:`L6 </lectures/lecture6/l6_lecture>`

   SOTIF
      See :term:`ISO 21448 (SOTIF)`. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_lecture>`

   Stanley Controller
      A lateral path-following controller (developed for the DARPA Grand
      Challenge) that computes steering based on both heading error and
      cross-track error measured at the front axle. More aggressive
      correction than Pure Pursuit at high cross-track errors. :doc:`L11 </lectures/lecture11/l11_lecture>`

   Stereo Vision
      Depth estimation using two cameras separated by a known baseline.
      Computes depth from the disparity between left and right images. :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _glossary-t:

T
=

.. glossary::

   Time-of-Flight (ToF)
      The operating principle of LiDAR. Measures the round-trip time of a
      laser pulse to compute distance: ``distance = (c x dt) / 2``. :doc:`L2 </lectures/lecture2/l2_lecture>`

   Tracking-by-Detection
      The dominant MOT paradigm: at each frame, run an object detector,
      then associate the new detections with existing tracks (via
      KF prediction + Hungarian / cosine appearance matching). Decouples
      the detector and the tracker. :doc:`L6 </lectures/lecture6/l6_lecture>`

   Transfer Learning
      Starting with a model pre-trained on a large dataset (e.g., COCO)
      and fine-tuning it on a smaller target dataset. Reduces training
      time and data requirements. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Trajectory Prediction
      Forecasting the future positions and states of other traffic agents
      (vehicles, pedestrians, cyclists) over a prediction horizon.
      Methods range from physics-based (CTRA) to transformer-based
      models generating multi-modal trajectory distributions. :doc:`L9 </lectures/lecture9/l9_lecture>`

   Transformer
      A neural network architecture (Vaswani et al., 2017) based on
      self-attention mechanisms that model relationships between all
      positions in a sequence simultaneously. Used in DETR, BEVFormer,
      and modern AV perception. :doc:`L4 </lectures/lecture4/l4_lecture>` · :doc:`L5 </lectures/lecture5/l5_lecture>`


.. _glossary-u:

U
=

.. glossary::

   UKF
      Unscented Kalman Filter. A non-linear filter that uses
      deterministic "sigma points" passed through the true non-linear
      function, avoiding the need for Jacobian matrices. :doc:`L3 </lectures/lecture3/l3_lecture>`

   U-Net
      An encoder-decoder segmentation architecture (Ronneberger et al.,
      2015) with skip connections that concatenate encoder features with
      decoder features at matching resolutions, preserving fine spatial
      detail for pixel-precise segmentation. :doc:`L5 </lectures/lecture5/l5_lecture>`

   UNECE GTR
      United Nations Economic Commission for Europe Global Technical
      Regulation. The UNECE GTR on ADS (approved Jan 2026) is the first
      global safety framework for autonomous driving. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_lecture>`

   UniAD
      Unified Autonomous Driving (CVPR 2023 Best Paper). A landmark
      end-to-end architecture that jointly performs perception, prediction,
      and planning through a unified transformer framework with
      planning-oriented task design. :doc:`L12 </lectures/lecture12/l12_lecture>`


.. _glossary-v:

V
=

.. glossary::

   V-Model
      The ISO 26262 development lifecycle where each design stage (left
      side) is paired with a corresponding verification/test stage (right
      side), ensuring systematic validation from unit to system level. :doc:`L14 </lectures/lecture14/l14_lecture>`

   V2X
      Vehicle-to-Everything communication. Includes V2V (vehicle-to-
      vehicle), V2I (vehicle-to-infrastructure), and V2P (vehicle-to-
      pedestrian). Enables cooperative perception and situational
      awareness. :doc:`L14 </lectures/lecture14/l14_lecture>`

   Vista
      A generalizable driving world model (NeurIPS 2024) that learns to
      predict diverse future video from a small amount of driving data,
      enabling synthetic scenario generation for evaluation. :doc:`L13 </lectures/lecture13/l13_lecture>`

   ViT
      Vision Transformer. A transformer architecture (Dosovitskiy et al.,
      2021) that splits images into patches and processes them as a
      sequence, applying self-attention for image classification. :doc:`L4 </lectures/lecture4/l4_lecture>`

   Visual Odometry
      Estimating camera ego-motion by tracking visual features across
      consecutive frames. Methods include feature-based (ORB-SLAM) and
      direct (DSO) approaches. Provides drift-prone but high-frequency
      relative pose updates. :doc:`L7 </lectures/lecture7/l7_lecture>`

   VLA Model
      Vision-Language-Action model. A multimodal architecture that
      combines visual perception, language reasoning (chain-of-thought),
      and action prediction for autonomous driving. Examples: DriveVLM,
      NVIDIA Alpamayo. :doc:`L12 </lectures/lecture12/l12_lecture>`

   Voxel
      A volumetric pixel -- a discrete cell in a 3D grid. Used to
      represent point clouds (voxelization), BEV features, and 3D
      occupancy maps. Voxel size determines the trade-off between
      resolution and computational cost. :doc:`L5 </lectures/lecture5/l5_lecture>`

   VQ-VAE
      Vector Quantized Variational Autoencoder. A generative model that
      encodes inputs into discrete codebook tokens. Used in world models
      as a visual tokenizer to compress video frames into sequences of
      discrete tokens for autoregressive prediction. :doc:`L13 </lectures/lecture13/l13_lecture>`


.. _glossary-w:

W
=

.. glossary::

   Waypoint
      In CARLA, a discrete point on the road network containing lane
      information, speed limits, and connectivity to other waypoints.
      Used for path planning and navigation. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L8 </lectures/lecture8/l8_lecture>`

   World Model
      A learned model that predicts future scene states (typically video
      frames) conditioned on actions and current observations. Acts as
      a data-driven simulator for training, evaluation, and imagination-
      based planning. Examples: GAIA-3, NVIDIA Cosmos, Vista. :doc:`L13 </lectures/lecture13/l13_lecture>`


.. _glossary-y:

Y
=

.. glossary::

   YOLO
      You Only Look Once. A family of single-stage object detectors that
      predict all bounding boxes and class probabilities in a single
      forward pass. Evolution: v1 (2015) to v11 (2024). :doc:`L4 </lectures/lecture4/l4_lecture>`
